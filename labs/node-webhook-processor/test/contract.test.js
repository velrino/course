import assert from "node:assert/strict";
import { test } from "node:test";

const target = process.env.LAB_TARGET ?? "solution";
const moduleUrl = new URL(`../${target}/src/webhook-processor.js`, import.meta.url);
const { WebhookError, WebhookProcessor, signPayload } = await import(moduleUrl);

const NOW = Date.parse("2026-08-11T15:00:00.000Z");
const SECRET = "test-secret-with-enough-entropy";

function event(overrides = {}) {
  return {
    id: "evt_001",
    type: "order.created",
    occurredAt: "2026-08-11T15:00:00.000Z",
    data: { orderId: "ord_001", totalCents: 2500 },
    ...overrides,
  };
}

function signedDelivery(payload = event(), timestamp = Math.floor(NOW / 1000)) {
  const rawBody = Buffer.from(JSON.stringify(payload));
  return {
    rawBody,
    signatureHeader: `t=${timestamp},v1=${signPayload(rawBody, SECRET, timestamp)}`,
  };
}

function processor(options = {}) {
  return new WebhookProcessor({
    secret: SECRET,
    handler: async () => ({ ok: true }),
    logger: () => {},
    now: () => NOW,
    sleep: async () => {},
    baseDelayMs: 10,
    ...options,
  });
}

test("accepts a valid delivery and emits structured attempt and success logs", async () => {
  const logs = [];
  const result = await processor({ logger: (entry) => logs.push(entry) }).process(signedDelivery());
  assert.equal(result.status, "processed");
  assert.equal(result.attempts, 1);
  assert.deepEqual(logs.map(({ event: name }) => name), ["delivery_attempt", "delivery_processed"]);
  for (const entry of logs) {
    assert.equal(typeof entry.timestamp, "string");
    assert.equal(entry.deliveryId, "evt_001");
    assert.equal(typeof entry.attempt, "number");
    assert.equal(typeof entry.status, "string");
  }
});

test("deduplicates a replayed delivery after one successful side effect", async () => {
  let calls = 0;
  const service = processor({ handler: async () => ({ sequence: ++calls }) });
  const first = await service.process(signedDelivery());
  const replay = await service.process(signedDelivery());
  assert.equal(first.status, "processed");
  assert.equal(replay.status, "duplicate");
  assert.equal(calls, 1);
  assert.deepEqual(replay.result, { sequence: 1 });
});

test("coalesces concurrent duplicate deliveries", async () => {
  let release;
  const gate = new Promise((resolve) => { release = resolve; });
  let calls = 0;
  const service = processor({ handler: async () => { calls += 1; await gate; return { ok: true }; } });
  const first = service.process(signedDelivery());
  const second = service.process(signedDelivery());
  release();
  const [a, b] = await Promise.all([first, second]);
  assert.equal(a.status, "processed");
  assert.equal(b.status, "duplicate");
  assert.equal(calls, 1);
});

test("rejects tampered bytes before invoking the handler", async () => {
  let calls = 0;
  const delivery = signedDelivery();
  delivery.rawBody = Buffer.from(`${delivery.rawBody.toString("utf8")} `);
  await assert.rejects(
    processor({ handler: async () => { calls += 1; } }).process(delivery),
    (error) => error instanceof WebhookError && error.code === "invalid_signature" && error.statusCode === 401,
  );
  assert.equal(calls, 0);
});

test("rejects a correctly signed but stale replay", async () => {
  const staleTimestamp = Math.floor(NOW / 1000) - 301;
  await assert.rejects(
    processor().process(signedDelivery(event(), staleTimestamp)),
    (error) => error.code === "stale_signature",
  );
});

test("uses exponential delays for transient failures", async () => {
  let calls = 0;
  const delays = [];
  const result = await processor({
    handler: async () => {
      calls += 1;
      if (calls < 3) throw Object.assign(new Error("upstream busy"), { retryable: true, code: "busy" });
      return { ok: true };
    },
    sleep: async (delay) => delays.push(delay),
  }).process(signedDelivery());
  assert.equal(result.attempts, 3);
  assert.deepEqual(delays, [10, 20]);
});

test("does not retry permanent handler failures", async () => {
  let calls = 0;
  await assert.rejects(
    processor({ handler: async () => { calls += 1; throw new Error("bad account"); } }).process(signedDelivery()),
    (error) => error.code === "delivery_failed" && error.statusCode === 502,
  );
  assert.equal(calls, 1);
});

test("rejects an invalid event contract after authenticating it", async () => {
  await assert.rejects(
    processor().process(signedDelivery({ id: "evt_bad", data: [] })),
    (error) => error.code === "invalid_event",
  );
});
