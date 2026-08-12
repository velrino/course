import assert from "node:assert/strict";
import { test } from "node:test";
import { inspectSources, verifyTarget } from "../scripts/verify.mjs";

test("solution passes the static container contract", async () => {
  assert.deepEqual(await verifyTarget("solution"), []);
});

test("starter reports multiple actionable omissions", async () => {
  const errors = await verifyTarget("starter");
  assert.ok(errors.length >= 8);
  assert.ok(errors.some((error) => error.includes("non-root")));
  assert.ok(errors.some((error) => error.includes("TODO")));
});

test("verifier rejects a superficially healthy but privileged stack", () => {
  const errors = inspectSources({
    dockerfile: "FROM node:22-alpine\nUSER 0:0\nHEALTHCHECK CMD true\n",
    compose: "services:\n  app:\n    healthcheck: {}\n",
    server: 'const routes = ["/health/live", "/health/ready", "/counter", "/admin/failure", "x-failure-token"];',
  });
  assert.ok(errors.some((error) => error.includes("non-root") || error.includes("ownership")));
  assert.ok(errors.some((error) => error.includes("read-only")));
  assert.ok(errors.some((error) => error.includes("atomic")));
});
