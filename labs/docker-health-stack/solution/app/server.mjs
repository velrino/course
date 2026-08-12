import { access, mkdir, readFile, rename, rm, writeFile } from "node:fs/promises";
import { constants } from "node:fs";
import { createServer } from "node:http";
import { join } from "node:path";
import { pathToFileURL } from "node:url";

const JSON_HEADERS = { "content-type": "application/json; charset=utf-8" };

function send(response, statusCode, body) {
  response.writeHead(statusCode, JSON_HEADERS);
  response.end(`${JSON.stringify(body)}\n`);
}

async function readJsonBody(request, limit = 16_384) {
  const chunks = [];
  let size = 0;
  for await (const chunk of request) {
    size += chunk.length;
    if (size > limit) throw Object.assign(new Error("Request body is too large."), { statusCode: 413 });
    chunks.push(chunk);
  }
  if (size === 0) return {};
  try {
    return JSON.parse(Buffer.concat(chunks).toString("utf8"));
  } catch (error) {
    throw Object.assign(new Error("Request body must be valid JSON."), { statusCode: 400, cause: error });
  }
}

export function createHandler({
  dataDir = process.env.DATA_DIR ?? "/data",
  failureToken = process.env.FAILURE_TOKEN ?? "lab-only",
  now = () => new Date(),
} = {}) {
  const statePath = join(dataDir, "counter.json");
  const failurePath = join(dataDir, "unhealthy.flag");
  let mutation = Promise.resolve();

  async function prepareDataDirectory() {
    await mkdir(dataDir, { recursive: true });
    await access(dataDir, constants.R_OK | constants.W_OK);
  }

  async function readCounter() {
    try {
      const parsed = JSON.parse(await readFile(statePath, "utf8"));
      if (!Number.isSafeInteger(parsed.value) || parsed.value < 0) {
        throw new Error("counter value must be a non-negative safe integer");
      }
      return parsed;
    } catch (error) {
      if (error.code === "ENOENT") return { value: 0, updatedAt: null };
      throw new Error(`Persistent state is invalid: ${error.message}`, { cause: error });
    }
  }

  async function incrementCounter() {
    const operation = mutation.then(async () => {
      await prepareDataDirectory();
      const current = await readCounter();
      const next = { value: current.value + 1, updatedAt: now().toISOString() };
      const temporaryPath = join(dataDir, `counter.${process.pid}.tmp`);
      await writeFile(temporaryPath, `${JSON.stringify(next)}\n`, { mode: 0o600 });
      await rename(temporaryPath, statePath);
      return next;
    });
    mutation = operation.catch(() => {});
    return operation;
  }

  async function readiness() {
    try {
      await prepareDataDirectory();
      await readCounter();
      await access(failurePath, constants.F_OK);
      return { ready: false, body: { status: "not_ready", checks: { stateDirectory: "writable", failureInjection: "active" } } };
    } catch (error) {
      if (error.code === "ENOENT") {
        return { ready: true, body: { status: "ready", checks: { stateDirectory: "writable", failureInjection: "inactive" } } };
      }
      return { ready: false, body: { status: "not_ready", checks: { stateDirectory: "unavailable", failureInjection: "unknown" } } };
    }
  }

  return async function handleRequest(request, response) {
    try {
      if (request.method === "GET" && request.url === "/health/live") {
        return send(response, 200, { status: "alive" });
      }
      if (request.method === "GET" && request.url === "/health/ready") {
        const result = await readiness();
        return send(response, result.ready ? 200 : 503, result.body);
      }
      if (request.method === "GET" && request.url === "/counter") {
        await prepareDataDirectory();
        return send(response, 200, await readCounter());
      }
      if (request.method === "POST" && request.url === "/counter") {
        return send(response, 200, await incrementCounter());
      }
      if ((request.method === "POST" || request.method === "DELETE") && request.url === "/admin/failure") {
        if (request.headers["x-failure-token"] !== failureToken) {
          return send(response, 403, { error: "forbidden" });
        }
        await prepareDataDirectory();
        if (request.method === "POST") {
          const body = await readJsonBody(request);
          await writeFile(failurePath, `${body.reason ?? "manual exercise"}\n`, { mode: 0o600 });
          return send(response, 202, { status: "failure_injected" });
        }
        await rm(failurePath, { force: true });
        return send(response, 200, { status: "failure_cleared" });
      }
      return send(response, 404, { error: "not_found" });
    } catch (error) {
      return send(response, error.statusCode ?? 500, {
        error: error.statusCode ? "invalid_request" : "internal_error",
        message: error.message,
      });
    }
  };
}

export function createApp(options = {}) {
  return createServer(createHandler(options));
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const port = Number(process.env.PORT ?? 8080);
  const server = createApp();
  server.listen(port, "0.0.0.0", () => {
    process.stderr.write(`Health lab listening on 0.0.0.0:${port}\n`);
  });
}
