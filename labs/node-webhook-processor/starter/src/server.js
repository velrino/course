import { createServer } from "node:http";
import { WebhookProcessor } from "./webhook-processor.js";

const processor = new WebhookProcessor({
  secret: process.env.WEBHOOK_SECRET ?? "development-secret",
  handler: async (event) => ({ acceptedType: event.type }),
});

export const server = createServer(async (request, response) => {
  // TODO 7: Accept only POST /webhooks/orders and cap raw bodies at 1 MB.
  // TODO 8: Pass the untouched bytes and x-webhook-signature to processor.process.
  response.writeHead(501, { "content-type": "application/json" });
  response.end('{"error":"not_implemented"}\n');
});

if (import.meta.url === `file://${process.argv[1]}`) {
  server.listen(Number(process.env.PORT ?? 3000), "127.0.0.1");
}
