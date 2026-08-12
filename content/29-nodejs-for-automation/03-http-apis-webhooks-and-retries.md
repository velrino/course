# HTTP APIs, Webhooks, and Retries

Network automation must assume delay, partial failure, duplicated delivery, and untrusted input. A request timeout does not prove that the remote operation failed: the service may have committed the change before the response was lost. Retries are therefore a business decision as well as a transport mechanism.

Node provides a browser-compatible `fetch`, `AbortSignal`, an HTTP server, URL parsing, and cryptographic primitives. These are enough for a dependency-free local exercise and many small integrations.

## Learning objectives

- Apply deadlines, response-size limits, status checks, and URL policy to API calls.
- Retry only transient failures and only when an operation is safe to repeat.
- Use capped exponential backoff, jitter, and `Retry-After` guidance.
- Verify a webhook HMAC over the exact raw request bytes before parsing JSON.
- Bound webhook bodies, require delivery identifiers, and acknowledge only after durable enqueue.
- Explain why in-memory deduplication is insufficient across restarts or replicas.

## API and webhook contracts

For outbound calls, define allowed schemes and hosts, set an overall deadline, reject redirects when they could bypass the host policy, bound the response, and verify the media type before parsing. Keep credentials in an authorization header and redact that header from logs.

GET and other safe methods may normally be retried. A mutating request should be retried only when the receiving API offers an idempotency contract and the caller reuses the same key for every attempt. Retry selected transport errors, `429`, and temporary `5xx` responses; do not retry authentication errors or structural validation errors. Cap both attempts and elapsed time so a backlog cannot grow without bound.

For inbound webhooks, compute the documented message authentication code over the original bytes. Parsing and reserializing JSON changes bytes and invalidates the security model. Compare signatures with a timing-safe function, reject stale or replayed deliveries according to the provider contract, enqueue durably, and respond quickly. The event handler should not perform the entire business workflow before acknowledging.

## Free local practice

Create `src/api-client.js`:

```javascript
import { setTimeout as sleep } from "node:timers/promises";

const transientStatuses = new Set([429, 502, 503, 504]);
const localHosts = new Set(["127.0.0.1", "localhost", "[::1]"]);

function assertAllowedUrl(value) {
  const url = new URL(value);
  const secure = url.protocol === "https:";
  const local = url.protocol === "http:" && localHosts.has(url.hostname);
  if (!secure && !local) throw new Error("only HTTPS or loopback HTTP is allowed");
  return url;
}

function retryDelay(response, attempt) {
  const header = response.headers.get("retry-after");
  if (header) {
    const seconds = Number(header);
    const milliseconds = Number.isFinite(seconds)
      ? seconds * 1000
      : Date.parse(header) - Date.now();
    if (Number.isFinite(milliseconds)) return Math.max(0, Math.min(30_000, milliseconds));
  }
  return Math.min(30_000, 250 * (2 ** attempt) + Math.floor(Math.random() * 100));
}

async function readJsonLimited(response, maximumBytes = 1_048_576) {
  const type = response.headers.get("content-type") ?? "";
  if (!type.toLowerCase().includes("application/json")) {
    throw new Error(`expected JSON but received ${type || "no content type"}`);
  }

  const chunks = [];
  let size = 0;
  for await (const chunk of response.body) {
    size += chunk.byteLength;
    if (size > maximumBytes) throw new Error("response exceeds 1 MiB");
    chunks.push(Buffer.from(chunk));
  }
  return JSON.parse(Buffer.concat(chunks).toString("utf8"));
}

export async function requestJson(value, options = {}) {
  const url = assertAllowedUrl(value);
  const method = (options.method ?? "GET").toUpperCase();
  const attempts = options.attempts ?? 4;
  if (!Number.isInteger(attempts) || attempts < 1 || attempts > 10) {
    throw new RangeError("attempts must be an integer from 1 to 10");
  }
  const repeatable = method === "GET" || method === "HEAD" || Boolean(options.idempotencyKey);

  for (let attempt = 0; attempt < attempts; attempt += 1) {
    let response;
    try {
      response = await fetch(url, {
        method,
        redirect: "error",
        signal: AbortSignal.timeout(options.timeoutMs ?? 3000),
        headers: {
          accept: "application/json",
          ...(options.body ? { "content-type": "application/json" } : {}),
          ...(options.token ? { authorization: `Bearer ${options.token}` } : {}),
          ...(options.idempotencyKey ? { "idempotency-key": options.idempotencyKey } : {})
        },
        body: options.body ? JSON.stringify(options.body) : undefined
      });
    } catch (error) {
      if (!repeatable || attempt === attempts - 1) throw error;
      await sleep(Math.min(30_000, 250 * (2 ** attempt)));
      continue;
    }

    if (response.ok) return readJsonLimited(response);

    if (!repeatable || !transientStatuses.has(response.status) || attempt === attempts - 1) {
      await response.body?.cancel();
      throw new Error(`HTTP ${response.status} from ${url.origin}`);
    }

    const delay = retryDelay(response, attempt);
    await response.body?.cancel();
    await sleep(delay);
  }
  throw new Error("unreachable retry state");
}
```

Create `src/http-lab.js`. It simulates an unstable API and a webhook receiver that persists each delivery before returning `202`:

```javascript
import { createHash, createHmac, timingSafeEqual } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import { createServer } from "node:http";
import { join } from "node:path";

const secret = process.env.WEBHOOK_SECRET ?? "local-secret";
const queueDir = "var/webhook-queue";
let unstableCalls = 0;

function send(response, status, value) {
  response.writeHead(status, { "content-type": "application/json" });
  response.end(`${JSON.stringify(value)}\n`);
}

async function readBody(request, maximumBytes = 65_536) {
  const chunks = [];
  let size = 0;
  let tooLarge = false;
  for await (const chunk of request) {
    size += chunk.byteLength;
    if (size > maximumBytes) {
      tooLarge = true;
      continue;
    }
    chunks.push(Buffer.from(chunk));
  }
  if (tooLarge) throw new RangeError("request body is too large");
  return Buffer.concat(chunks);
}

function validSignature(raw, receivedValue) {
  const expected = Buffer.from(`sha256=${createHmac("sha256", secret).update(raw).digest("hex")}`);
  const received = Buffer.from(typeof receivedValue === "string" ? receivedValue : "");
  return expected.length === received.length && timingSafeEqual(expected, received);
}

async function enqueueOnce(deliveryId, raw) {
  await mkdir(queueDir, { recursive: true });
  const name = createHash("sha256").update(deliveryId).digest("hex");
  try {
    await writeFile(join(queueDir, `${name}.json`), raw, {
      flag: "wx",
      mode: 0o600,
      flush: true
    });
    return true;
  } catch (error) {
    if (error?.code === "EEXIST") return false;
    throw error;
  }
}

const server = createServer(async (request, response) => {
  try {
    if (request.method === "GET" && request.url === "/unstable") {
      unstableCalls += 1;
      if (unstableCalls < 3) {
        response.setHeader("retry-after", "0");
        return send(response, 503, { error: "temporary" });
      }
      return send(response, 200, { ok: true, attempts: unstableCalls });
    }

    if (request.method === "POST" && request.url === "/webhook") {
      const raw = await readBody(request);
      if (!validSignature(raw, request.headers["x-hub-signature-256"])) {
        return send(response, 401, { error: "invalid signature" });
      }
      const deliveryId = request.headers["x-delivery-id"];
      if (typeof deliveryId !== "string" || !deliveryId) {
        return send(response, 400, { error: "missing delivery id" });
      }
      JSON.parse(raw.toString("utf8"));
      const created = await enqueueOnce(deliveryId, raw);
      return send(response, 202, { queued: created, duplicate: !created });
    }

    send(response, 404, { error: "not found" });
  } catch (error) {
    const tooLarge = error instanceof RangeError;
    send(response, tooLarge ? 413 : 400, {
      error: tooLarge ? "payload too large" : "invalid request"
    });
  }
});

server.listen(8787, "127.0.0.1", () => {
  console.log("HTTP lab listening on http://127.0.0.1:8787");
});
```

Create `src/http-demo.js`:

```javascript
import { createHmac } from "node:crypto";
import { requestJson } from "./api-client.js";

console.log(await requestJson("http://127.0.0.1:8787/unstable"));

const secret = process.env.WEBHOOK_SECRET ?? "local-secret";
const raw = JSON.stringify({ event: "invoice.created", id: "inv-7" });
const signature = `sha256=${createHmac("sha256", secret).update(raw).digest("hex")}`;
const response = await fetch("http://127.0.0.1:8787/webhook", {
  method: "POST",
  headers: {
    "content-type": "application/json",
    "x-delivery-id": "delivery-001",
    "x-hub-signature-256": signature
  },
  body: raw
});
console.log(response.status, await response.json());
```

Run `node src/http-lab.js` in one terminal and `node src/http-demo.js` twice in another. The API should succeed after two `503` responses. The second webhook submission should be reported as a duplicate. Change the secret in only one process and confirm that the receiver rejects the event.

The local queue flushes each event before acknowledgment and demonstrates restart-safe deduplication on one filesystem, not a distributed production queue or a complete power-loss protocol. A real deployment also needs timestamp or replay-window policy, secret rotation, access controls, retention, directory durability where required, and coordinated uniqueness across replicas.

## Completion criteria

- Outbound requests have a deadline, bounded JSON response, redirect policy, and scheme/host policy.
- The demo retries temporary responses but does not blindly retry every status or non-idempotent mutation.
- A webhook with an invalid signature or oversized body is rejected before JSON processing.
- Reusing a delivery identifier does not create a second queue file, including after restarting the server.
- The receiver returns success only after the event is stored, and secrets never appear in logs.
- You can explain the ambiguous outcome of a timed-out mutating request.

## References

- [Node.js: Global `fetch` and `AbortSignal`](https://nodejs.org/api/globals.html)
- [Node.js: HTTP](https://nodejs.org/api/http.html)
- [Node.js: Crypto](https://nodejs.org/api/crypto.html)
- [HTTP Semantics, RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html)
- [GitHub: Validating webhook deliveries](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries)
- [GitHub: Best practices for using webhooks](https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks)

[Next lesson: Async Concurrency, Queues, and Idempotency](./04-async-concurrency-queues-and-idempotency.md)
