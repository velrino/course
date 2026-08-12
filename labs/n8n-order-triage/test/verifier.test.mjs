import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { test } from "node:test";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { triageOrder } from "../scripts/policy.mjs";
import { verifyFiles } from "../scripts/verify.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const fixture = async (name) => JSON.parse(await readFile(join(root, "fixtures", name), "utf8"));

test("solution workflows pass static and fixture verification", async () => {
  assert.deepEqual(await verifyFiles("solution", root), []);
});

test("starter verifier points to incomplete workflow behavior", async () => {
  const errors = await verifyFiles("starter", root);
  assert.ok(errors.length >= 5);
  assert.ok(errors.some((error) => error.includes("TODO")));
  assert.ok(errors.some((error) => error.includes("Respond Invalid")));
});

test("normal order follows the automatic path", async () => {
  const result = triageOrder(await fixture("standard-order.json"));
  assert.equal(result.route, "automatic");
  assert.deepEqual(result.validationErrors, []);
});

test("high risk and exact value boundary require manual review", async () => {
  assert.equal(triageOrder(await fixture("manual-review-order.json")).route, "manual_review");
  assert.equal(triageOrder(await fixture("boundary-order.json")).route, "manual_review");
});

test("invalid input takes an explicit error response path", async () => {
  const result = triageOrder(await fixture("invalid-order.json"));
  assert.equal(result.route, "invalid");
  assert.ok(result.validationErrors.length >= 4);
});

test("missing optional risk score defaults to zero", () => {
  const result = triageOrder({ orderId: "ord_x", customerId: "cus_x", currency: "BRL", totalCents: 999 });
  assert.equal(result.route, "automatic");
  assert.equal(result.riskScore, 0);
});
