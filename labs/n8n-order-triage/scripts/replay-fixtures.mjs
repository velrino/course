import { readFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { triageOrder } from "./policy.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
for (const name of ["standard-order.json", "manual-review-order.json", "boundary-order.json", "invalid-order.json"]) {
  const order = JSON.parse(await readFile(join(root, "fixtures", name), "utf8"));
  process.stdout.write(`${JSON.stringify({ fixture: name, ...triageOrder(order) })}\n`);
}
