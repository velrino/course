import { createServer } from "node:http";
import { WebhookError, WebhookProcessor } from "./webhook-processor.js";

const secret = process.env.WEBHOOK_SECRET ?? "development-secret";
const port = Number(process.env.PORT ?? 3000);
const processor = new WebhookProcessor({
  secret,
  handler: async (event) => ({ acceptedType: event.type, orderId: event.data.orderId ?? null }),
});

function send(response, statusCode, body) {
  response.writeHead(statusCode, { "content-type": "application/json" });
  response.end(`${JSON.stringify(body)}\n`);
}

export const server = createServer(async (request, response) => {
  if (request.method !== "POST" || request.url !== "/webhooks/orders") {
    return send(response, 404, { error: "not_found" });
  }

  const chunks = [];
  let size = 0;
  for await (const chunk of request) {
    size += chunk.length;
    if (size > 1_000_000) {
      request.resume();
      return send(response, 413, { error: "body_too_large" });
    }
    chunks.push(chunk);
  }

  try {
    const result = await processor.process({
      rawBody: Buffer.concat(chunks),
      signatureHeader: request.headers["x-webhook-signature"],
    });
    return send(response, result.status === "duplicate" ? 200 : 202, result);
  } catch (error) {
    const known = error instanceof WebhookError;
    return send(response, known ? error.statusCode : 500, {
      error: known ? error.code : "internal_error",
      message: known ? error.message : "Unexpected server error.",
    });
  }
});

if (import.meta.url === `file://${process.argv[1]}`) {
  server.listen(port, "127.0.0.1", () => {
    process.stderr.write(`Webhook server listening at http://127.0.0.1:${port}\n`);
  });
}
