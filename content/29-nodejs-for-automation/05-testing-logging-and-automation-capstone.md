# Testing, Logging, and an Automation Capstone

An automation is maintainable when its behavior can be reproduced without the real vendor API and diagnosed without attaching a debugger to production. Node's built-in test runner, strict assertions, temporary directories, dependency injection, and structured logs provide that foundation without an additional framework.

The capstone is an inbox processor. It validates JSON records, calls an injected enrichment function, writes results atomically, skips work whose output already exists, quarantines permanently invalid input, and leaves transient failures available for retry.

## Learning objectives

- Test observable behavior with `node:test` and `node:assert/strict`.
- Replace network and clock dependencies through narrow function parameters.
- Use temporary directories so tests are isolated and repeatable.
- Emit structured logs with stable event names and per-job context.
- Distinguish permanent validation failures from retryable operational failures.
- Run failure drills and define measurable acceptance criteria for an automation.

## Tests and operational evidence

Tests should cover more than the successful example. Include malformed input, duplicates, timeouts, partial output, cancellation, retries, and restart behavior. Prefer a fake function injected at the API boundary over a global mock that knows implementation details. When an HTTP contract itself matters, run a local `node:http` server in the test.

Logs are event records, not prose. Emit newline-delimited JSON with an ISO timestamp, severity, stable event name, correlation or job ID, attempt, duration, and sanitized error category. Avoid raw input payloads because they may contain credentials or personal data. Metrics should separately count attempted, completed, skipped, retried, failed, and quarantined jobs; a single "processed" counter hides failures.

`AsyncLocalStorage` can attach correlation context across promise chains, but explicit parameters remain easier to reason about in core domain functions. Treat uncaught exceptions and unhandled rejections as fatal signals: record the failure, stop accepting work, finish bounded cleanup, and let a supervisor restart the process.

## Free local practice

Create `src/automation.js`:

```javascript
import { createHash, randomUUID } from "node:crypto";
import { access, mkdir, readFile, readdir, rename, rm, writeFile } from "node:fs/promises";
import { join } from "node:path";

export class ValidationError extends Error {}

function safeKey(value) {
  return createHash("sha256").update(value).digest("hex").slice(0, 16);
}

function validate(value) {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new ValidationError("record must be an object");
  }
  if (typeof value.id !== "string" || typeof value.title !== "string") {
    throw new ValidationError("id and title must be strings");
  }
  const id = value.id.trim();
  const title = value.title.trim();
  if (!id || !title) throw new ValidationError("id and title are required");
  return { id, title };
}

async function exists(path) {
  try {
    await access(path);
    return true;
  } catch (error) {
    if (error?.code === "ENOENT") return false;
    throw error;
  }
}

async function atomicWrite(path, value) {
  const temporary = `${path}.${process.pid}.${randomUUID()}.tmp`;
  try {
    await writeFile(temporary, `${JSON.stringify(value, null, 2)}\n`, {
      encoding: "utf8",
      flag: "wx",
      mode: 0o600
    });
    await rename(temporary, path);
  } finally {
    await rm(temporary, { force: true });
  }
}

export async function processInbox({ inbox, outbox, quarantine, enrich, log = () => {} }) {
  await Promise.all([
    mkdir(inbox, { recursive: true }),
    mkdir(outbox, { recursive: true }),
    mkdir(quarantine, { recursive: true })
  ]);
  const stats = { completed: 0, skipped: 0, invalid: 0, failed: 0 };
  const names = (await readdir(inbox, { withFileTypes: true }))
    .filter((entry) => entry.isFile() && entry.name.endsWith(".json"))
    .map((entry) => entry.name)
    .sort();

  for (const name of names) {
    const inputPath = join(inbox, name);
    try {
      const record = validate(JSON.parse(await readFile(inputPath, "utf8")));
      const digest = createHash("sha256").update(record.id).digest("hex");
      const outputPath = join(outbox, `${digest}.json`);
      if (await exists(outputPath)) {
        stats.skipped += 1;
        log("info", "job_skipped", { recordKey: safeKey(record.id) });
        continue;
      }

      const enriched = await enrich(record);
      await atomicWrite(outputPath, { record, enrichment: enriched });
      stats.completed += 1;
      log("info", "job_completed", { recordKey: safeKey(record.id) });
    } catch (error) {
      if (error instanceof SyntaxError || error instanceof ValidationError) {
        await rename(inputPath, join(quarantine, name));
        stats.invalid += 1;
        log("warn", "job_quarantined", { fileKey: safeKey(name), errorType: error.name });
      } else {
        stats.failed += 1;
        log("error", "job_failed", {
          fileKey: safeKey(name),
          errorType: error?.name ?? "UnknownError"
        });
      }
    }
  }
  return stats;
}
```

Create `src/log.js`:

```javascript
import { AsyncLocalStorage } from "node:async_hooks";

const context = new AsyncLocalStorage();

export function withLogContext(values, operation) {
  return context.run(Object.freeze({ ...values }), operation);
}

export function createLogger({ write = (line) => process.stdout.write(line), now = () => new Date() } = {}) {
  return (level, event, fields = {}) => {
    const record = {
      timestamp: now().toISOString(),
      ...context.getStore(),
      ...fields,
      level,
      event
    };
    write(`${JSON.stringify(record)}\n`);
  };
}
```

Create `src/run-capstone.js` as a fully local entry point:

```javascript
import { randomUUID } from "node:crypto";
import { processInbox } from "./automation.js";
import { createLogger, withLogContext } from "./log.js";

const log = createLogger();
const paths = {
  inbox: "var/capstone/inbox",
  outbox: "var/capstone/outbox",
  quarantine: "var/capstone/quarantine"
};

const stats = await withLogContext({ runId: randomUUID() }, async () => {
  const result = await processInbox({
    ...paths,
    log,
    enrich: async (record) => ({
      slug: record.title.toLowerCase().replaceAll(/[^a-z0-9]+/g, "-").replaceAll(/^-|-$/g, "")
    })
  });
  log("info", "run_finished", result);
  return result;
});

if (stats.failed > 0) process.exitCode = 1;
```

Run it without any external service:

```sh
mkdir -p var/capstone/inbox
printf '%s\n' '{"id":"doc-1","title":"Quarterly Report"}' > var/capstone/inbox/doc-1.json
node src/run-capstone.js
node src/run-capstone.js
```

The first run should complete one record, and the second should skip the already published result.

Create `test/automation.test.js`:

```javascript
import assert from "node:assert/strict";
import { mkdir, mkdtemp, readFile, readdir, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { processInbox } from "../src/automation.js";
import { createLogger, withLogContext } from "../src/log.js";

async function fixture(t) {
  const root = await mkdtemp(join(tmpdir(), "node-automation-"));
  t.after(() => rm(root, { recursive: true, force: true }));
  return {
    inbox: join(root, "inbox"),
    outbox: join(root, "outbox"),
    quarantine: join(root, "quarantine")
  };
}

test("processes valid input and skips the same output on replay", async (t) => {
  const paths = await fixture(t);
  await mkdir(paths.inbox, { recursive: true });
  await writeFile(join(paths.inbox, "one.json"), '{"id":"7","title":"Report"}');

  const options = { ...paths, enrich: async () => ({ status: "ready" }) };
  assert.deepEqual(await processInbox(options), {
    completed: 1, skipped: 0, invalid: 0, failed: 0
  });
  assert.deepEqual(await processInbox(options), {
    completed: 0, skipped: 1, invalid: 0, failed: 0
  });

  const [name] = await readdir(paths.outbox);
  const output = JSON.parse(await readFile(join(paths.outbox, name), "utf8"));
  assert.deepEqual(output, {
    record: { id: "7", title: "Report" },
    enrichment: { status: "ready" }
  });
});

test("quarantines permanently invalid input", async (t) => {
  const paths = await fixture(t);
  await mkdir(paths.inbox, { recursive: true });
  await writeFile(join(paths.inbox, "bad.json"), '{"id":"7"}');

  const stats = await processInbox({ ...paths, enrich: async () => ({}) });
  assert.equal(stats.invalid, 1);
  assert.deepEqual(await readdir(paths.quarantine), ["bad.json"]);
});

test("leaves transient failures in the inbox for retry", async (t) => {
  const paths = await fixture(t);
  await mkdir(paths.inbox, { recursive: true });
  await writeFile(join(paths.inbox, "retry.json"), '{"id":"8","title":"Retry"}');

  const stats = await processInbox({
    ...paths,
    enrich: async () => { throw new Error("temporary outage"); }
  });

  assert.equal(stats.failed, 1);
  assert.deepEqual(await readdir(paths.inbox), ["retry.json"]);
  assert.deepEqual(await readdir(paths.quarantine), []);
});

test("structured logger includes async job context", async () => {
  let line = "";
  const log = createLogger({
    write: (value) => { line = value; },
    now: () => new Date("2026-01-02T03:04:05.000Z")
  });

  await withLogContext({ jobId: "job-9" }, async () => {
    await Promise.resolve();
    log("info", "job_started", { attempt: 2 });
  });

  assert.deepEqual(JSON.parse(line), {
    timestamp: "2026-01-02T03:04:05.000Z",
    jobId: "job-9",
    attempt: 2,
    level: "info",
    event: "job_started"
  });
});
```

Run the suite:

```sh
npm test
```

Complete the capstone by replacing the local enrichment function with the API adapter from lesson 3, then reuse the bounded `mapLimit` and retry policy from lessons 3 and 4. An atomic idempotency claim from lesson 4 must surround the check and write before you enable concurrency; otherwise two files with the same business ID can race. Add these failure drills:

1. The enrichment dependency times out and later recovers.
2. Two files contain the same business ID.
3. The process receives `SIGTERM` with work in flight.
4. One input contains a secret-like field and logs remain free of its value.
5. A corrupt file is quarantined while valid files continue.

Record run counts and durations, but do not use high-cardinality record IDs as metric labels. Before deployment, pin dependencies with a lockfile, run `npm ci`, review `npm audit` findings in context, run under a least-privileged account, and define retention for inbox, output, quarantine, and logs.

## Completion criteria

- `npm test` passes repeatedly without network access and leaves no temporary directories behind.
- Tests prove successful processing, replay behavior, quarantine behavior, and asynchronous log context.
- A transient enrichment failure remains eligible for retry and is not quarantined as invalid data.
- The final CLI uses bounded concurrency, deadlines, classified retries, cancellation, atomic writes, and stable idempotency keys.
- Logs are valid JSON Lines, contain stable event names and correlation context, and exclude payloads, tokens, and personal data.
- All five failure drills have an asserted outcome rather than only manual observation.
- A short runbook documents startup, graceful shutdown, retry exhaustion, dead-letter or quarantine review, and safe replay.

## References

- [Node.js: Test runner](https://nodejs.org/api/test.html)
- [Node.js: Strict assertion mode](https://nodejs.org/api/assert.html#strict-assertion-mode)
- [Node.js: Async context and `AsyncLocalStorage`](https://nodejs.org/api/async_context.html)
- [Node.js: Performance measurement APIs](https://nodejs.org/api/perf_hooks.html)
- [Node.js: Process events and warnings](https://nodejs.org/api/process.html#process-events)
- [npm: `npm ci`](https://docs.npmjs.com/cli/v11/commands/npm-ci)
- [npm: `npm audit`](https://docs.npmjs.com/cli/v11/commands/npm-audit)
