import { readFile } from "node:fs/promises";
import { WebhookProcessor, signPayload } from "../solution/src/webhook-processor.js";

const rawBody = await readFile(new URL("../fixtures/order.created.json", import.meta.url));
const secret = "demo-secret";
const timestamp = Math.floor(Date.now() / 1000);
const signatureHeader = `t=${timestamp},v1=${signPayload(rawBody, secret, timestamp)}`;
const processor = new WebhookProcessor({
  secret,
  handler: async (event) => ({ orderId: event.data.orderId }),
});

process.stdout.write(`${JSON.stringify(await processor.process({ rawBody, signatureHeader }))}\n`);
process.stdout.write(`${JSON.stringify(await processor.process({ rawBody, signatureHeader }))}\n`);
