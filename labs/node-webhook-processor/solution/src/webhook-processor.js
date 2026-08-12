import { createHmac, timingSafeEqual } from "node:crypto";

export class WebhookError extends Error {
  constructor(code, message, statusCode = 400, options = {}) {
    super(message, options);
    this.name = "WebhookError";
    this.code = code;
    this.statusCode = statusCode;
  }
}

function asBuffer(rawBody) {
  if (Buffer.isBuffer(rawBody)) return rawBody;
  if (typeof rawBody === "string") return Buffer.from(rawBody, "utf8");
  throw new WebhookError("invalid_body", "The raw request body must be a string or Buffer.");
}

export function signPayload(rawBody, secret, timestamp) {
  const body = asBuffer(rawBody);
  return createHmac("sha256", secret)
    .update(String(timestamp))
    .update(".")
    .update(body)
    .digest("hex");
}

function parseSignatureHeader(header) {
  if (typeof header !== "string") {
    throw new WebhookError("missing_signature", "The signature header is required.", 401);
  }

  const parts = Object.fromEntries(
    header.split(",").map((part) => {
      const [key, ...value] = part.trim().split("=");
      return [key, value.join("=")];
    }),
  );
  const timestamp = Number(parts.t);
  if (!Number.isInteger(timestamp) || !/^[a-f0-9]{64}$/i.test(parts.v1 ?? "")) {
    throw new WebhookError("malformed_signature", "Expected t=<unix-seconds>,v1=<sha256-hex>.", 401);
  }
  return { timestamp, digest: parts.v1.toLowerCase() };
}

export function verifyWebhookSignature({
  rawBody,
  signatureHeader,
  secret,
  nowMs = Date.now(),
  toleranceSeconds = 300,
}) {
  const { timestamp, digest } = parseSignatureHeader(signatureHeader);
  const ageSeconds = Math.abs(Math.floor(nowMs / 1000) - timestamp);
  if (ageSeconds > toleranceSeconds) {
    throw new WebhookError("stale_signature", "The signed delivery is outside the replay window.", 401);
  }

  const expected = Buffer.from(signPayload(rawBody, secret, timestamp), "hex");
  const received = Buffer.from(digest, "hex");
  if (expected.length !== received.length || !timingSafeEqual(expected, received)) {
    throw new WebhookError("invalid_signature", "The signature does not match the raw body.", 401);
  }
  return timestamp;
}

function parseEvent(rawBody) {
  let event;
  try {
    event = JSON.parse(asBuffer(rawBody).toString("utf8"));
  } catch (error) {
    throw new WebhookError("invalid_json", "The request body is not valid JSON.", 400, { cause: error });
  }

  if (
    event === null ||
    typeof event !== "object" ||
    Array.isArray(event) ||
    typeof event.id !== "string" ||
    event.id.length < 1 ||
    typeof event.type !== "string" ||
    event.type.length < 1 ||
    !Number.isFinite(Date.parse(event.occurredAt)) ||
    event.data === null ||
    typeof event.data !== "object" ||
    Array.isArray(event.data)
  ) {
    throw new WebhookError(
      "invalid_event",
      "An event needs non-empty id and type fields, an ISO timestamp, and an object data field.",
    );
  }
  return event;
}

const defaultSleep = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));

export class WebhookProcessor {
  constructor({
    secret,
    handler,
    logger = (entry) => process.stdout.write(`${JSON.stringify(entry)}\n`),
    now = Date.now,
    sleep = defaultSleep,
    maxAttempts = 3,
    baseDelayMs = 50,
    toleranceSeconds = 300,
  }) {
    if (!secret) throw new TypeError("secret is required");
    if (typeof handler !== "function") throw new TypeError("handler must be a function");
    this.secret = secret;
    this.handler = handler;
    this.logger = logger;
    this.now = now;
    this.sleep = sleep;
    this.maxAttempts = maxAttempts;
    this.baseDelayMs = baseDelayMs;
    this.toleranceSeconds = toleranceSeconds;
    this.completed = new Map();
    this.inFlight = new Map();
  }

  log(level, event, deliveryId, attempt, status, extra = {}) {
    this.logger({
      timestamp: new Date(this.now()).toISOString(),
      level,
      event,
      deliveryId,
      attempt,
      status,
      ...extra,
    });
  }

  async process({ rawBody, signatureHeader }) {
    verifyWebhookSignature({
      rawBody,
      signatureHeader,
      secret: this.secret,
      nowMs: this.now(),
      toleranceSeconds: this.toleranceSeconds,
    });
    const event = parseEvent(rawBody);

    if (this.completed.has(event.id)) {
      this.log("info", "duplicate_delivery", event.id, 0, "duplicate");
      return { status: "duplicate", deliveryId: event.id, result: this.completed.get(event.id) };
    }

    if (this.inFlight.has(event.id)) {
      this.log("info", "duplicate_in_flight", event.id, 0, "duplicate");
      const completed = await this.inFlight.get(event.id);
      return { status: "duplicate", deliveryId: event.id, result: completed.result };
    }

    const delivery = this.deliver(event);
    this.inFlight.set(event.id, delivery);
    try {
      return await delivery;
    } finally {
      this.inFlight.delete(event.id);
    }
  }

  async deliver(event) {
    for (let attempt = 1; attempt <= this.maxAttempts; attempt += 1) {
      this.log("info", "delivery_attempt", event.id, attempt, "attempting");
      try {
        const result = await this.handler(event);
        this.completed.set(event.id, result);
        this.log("info", "delivery_processed", event.id, attempt, "processed");
        return { status: "processed", deliveryId: event.id, attempts: attempt, result };
      } catch (error) {
        const retryable = error?.retryable === true;
        const exhausted = attempt === this.maxAttempts;
        this.log(
          retryable && !exhausted ? "warn" : "error",
          "delivery_failed",
          event.id,
          attempt,
          retryable && !exhausted ? "retrying" : "failed",
          { errorCode: error?.code ?? "handler_error" },
        );
        if (!retryable || exhausted) {
          throw new WebhookError("delivery_failed", "The event handler failed.", 502, { cause: error });
        }
        await this.sleep(this.baseDelayMs * 2 ** (attempt - 1));
      }
    }
    throw new WebhookError("delivery_failed", "The event handler failed.", 502);
  }
}
