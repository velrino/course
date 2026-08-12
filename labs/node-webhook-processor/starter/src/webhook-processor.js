import { createHmac } from "node:crypto";

export class WebhookError extends Error {
  constructor(code, message, statusCode = 400, options = {}) {
    super(message, options);
    this.name = "WebhookError";
    this.code = code;
    this.statusCode = statusCode;
  }
}

export function signPayload(rawBody, secret, timestamp) {
  return createHmac("sha256", secret)
    .update(String(timestamp))
    .update(".")
    .update(rawBody)
    .digest("hex");
}

export function verifyWebhookSignature(_input) {
  // TODO 1: Parse t and v1, reject stale timestamps, and use timingSafeEqual.
  throw new WebhookError("not_implemented", "Signature verification is not implemented.");
}

export class WebhookProcessor {
  constructor({ secret, handler, logger = console.log, now = Date.now, sleep = () => {} }) {
    this.secret = secret;
    this.handler = handler;
    this.logger = logger;
    this.now = now;
    this.sleep = sleep;
    // TODO 2: Add completed and in-flight delivery stores.
  }

  async process(_delivery) {
    // TODO 3: Authenticate the raw bytes before JSON parsing.
    // TODO 4: Validate the event contract and reject replays/duplicates.
    // TODO 5: Retry only errors explicitly marked retryable.
    // TODO 6: Emit structured attempt, success, duplicate, and failure logs.
    throw new WebhookError("not_implemented", "Webhook processing is not implemented.");
  }
}
