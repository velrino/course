import assert from "node:assert/strict";
import { mkdtemp, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";
import { createHandler } from "../solution/app/server.mjs";

async function withState(run) {
  const dataDir = await mkdtemp(join(tmpdir(), "docker-health-lab-"));
  try { await run(dataDir); } finally { await rm(dataDir, { recursive: true, force: true }); }
}

async function call(handler, path, { method = "GET", headers = {}, body } = {}) {
  const request = {
    method,
    url: path,
    headers,
    async *[Symbol.asyncIterator]() {
      if (body !== undefined) yield Buffer.from(body);
    },
  };
  const response = {
    status: 0,
    chunks: [],
    writeHead(status) { this.status = status; },
    end(chunk = "") { this.chunks.push(Buffer.from(chunk)); },
  };
  await handler(request, response);
  const text = Buffer.concat(response.chunks).toString("utf8");
  return { status: response.status, json: () => JSON.parse(text) };
}

test("liveness remains up while injected failure makes readiness fail", async () => withState(async (dataDir) => {
  const handler = createHandler({ dataDir, failureToken: "test-token" });
  assert.equal((await call(handler, "/health/live")).status, 200);
  assert.equal((await call(handler, "/health/ready")).status, 200);
  assert.equal((await call(handler, "/admin/failure", { method: "POST", body: "{}" })).status, 403);
  assert.equal((await call(handler, "/admin/failure", {
      method: "POST",
      headers: { "content-type": "application/json", "x-failure-token": "test-token" },
      body: JSON.stringify({ reason: "exercise" }),
    })).status, 202);
  assert.equal((await call(handler, "/health/live")).status, 200);
  const notReady = await call(handler, "/health/ready");
  assert.equal(notReady.status, 503);
  assert.equal(notReady.json().checks.failureInjection, "active");
  assert.equal((await call(handler, "/admin/failure", {
    method: "DELETE",
    headers: { "x-failure-token": "test-token" },
  })).status, 200);
  assert.equal((await call(handler, "/health/ready")).status, 200);
}));

test("counter increments serialize and survive an app restart", async () => withState(async (dataDir) => {
  const options = { dataDir, failureToken: "test-token", now: () => new Date("2026-08-11T15:00:00.000Z") };
  const first = createHandler(options);
  const responses = await Promise.all(Array.from({ length: 10 }, () => call(first, "/counter", { method: "POST" })));
  assert.ok(responses.every((response) => response.status === 200));

  const second = createHandler(options);
  const persisted = (await call(second, "/counter")).json();
  assert.equal(persisted.value, 10);
  assert.equal(persisted.updatedAt, "2026-08-11T15:00:00.000Z");
}));

test("corrupt persisted state returns a controlled 500 without killing liveness", async () => withState(async (dataDir) => {
  await writeFile(join(dataDir, "counter.json"), "not-json\n");
  const handler = createHandler({ dataDir, failureToken: "test-token" });
  const response = await call(handler, "/counter");
  assert.equal(response.status, 500);
  assert.match(response.json().message, /Persistent state is invalid/);
  assert.equal((await call(handler, "/health/live")).status, 200);
  assert.equal((await call(handler, "/health/ready")).status, 503);
}));
