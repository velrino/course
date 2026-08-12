import { pathToFileURL } from "node:url";
import { readFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { triageOrder } from "./policy.mjs";

const labRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");

async function readJson(path) {
  return JSON.parse(await readFile(path, "utf8"));
}

function reachableNames(workflow, startName) {
  const visited = new Set();
  const queue = [startName];
  while (queue.length > 0) {
    const current = queue.shift();
    if (visited.has(current)) continue;
    visited.add(current);
    const outputs = workflow.connections?.[current]?.main ?? [];
    for (const branch of outputs) {
      for (const edge of branch ?? []) queue.push(edge.node);
    }
  }
  return visited;
}

export async function verifyFiles(target = "solution", root = labRoot) {
  const errors = [];
  const workflowPath = join(root, target, "order-triage.workflow.json");
  let workflow;
  try {
    workflow = await readJson(workflowPath);
  } catch (error) {
    return [`Cannot parse ${workflowPath}: ${error.message}`];
  }

  const names = new Set(workflow.nodes?.map((node) => node.name) ?? []);
  const requiredNames = [
    "Receive Order",
    "Validate and Classify",
    "Order Invalid?",
    "Needs Manual Review?",
    "Prepare Invalid Response",
    "Prepare Manual Review",
    "Prepare Automatic Response",
    "Respond Invalid",
    "Respond Accepted",
  ];
  for (const name of requiredNames) {
    if (!names.has(name)) errors.push(`Missing required node: ${name}`);
  }

  const webhook = workflow.nodes?.find((node) => node.name === "Receive Order");
  if (webhook?.type !== "n8n-nodes-base.webhook") errors.push("Receive Order must be a Webhook node.");
  if (webhook?.parameters?.responseMode !== "responseNode") {
    errors.push("The Webhook must delegate responses to Respond to Webhook nodes.");
  }

  const classifier = workflow.nodes?.find((node) => node.name === "Validate and Classify");
  const code = classifier?.parameters?.jsCode ?? "";
  for (const token of ["orderId", "customerId", "currency", "totalCents", "riskScore", "validationErrors", "manual_review"]) {
    if (!code.includes(token)) errors.push(`Classifier does not mention required policy field: ${token}`);
  }
  if (/TODO/i.test(JSON.stringify(workflow))) errors.push("Workflow still contains TODO markers.");

  const reachable = reachableNames(workflow, "Receive Order");
  for (const responseName of ["Respond Invalid", "Respond Accepted"]) {
    if (!reachable.has(responseName)) errors.push(`${responseName} is not reachable from Receive Order.`);
  }

  if (target === "solution") {
    try {
      const errorWorkflow = await readJson(join(root, target, "error-handler.workflow.json"));
      if (!errorWorkflow.nodes?.some((node) => node.type === "n8n-nodes-base.errorTrigger")) {
        errors.push("The error workflow needs an Error Trigger node.");
      }
      if (!errorWorkflow.nodes?.some((node) => node.name === "Build Failure Record")) {
        errors.push("The error workflow needs a Build Failure Record node.");
      }
    } catch (error) {
      errors.push(`Cannot parse the error workflow: ${error.message}`);
    }
  }

  const expectedRoutes = await readJson(join(root, "fixtures", "expected-routes.json"));
  for (const [fixtureName, expectedRoute] of Object.entries(expectedRoutes)) {
    const actual = triageOrder(await readJson(join(root, "fixtures", fixtureName)));
    if (actual.route !== expectedRoute) {
      errors.push(`${fixtureName}: expected ${expectedRoute}, received ${actual.route}`);
    }
  }
  return errors;
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const target = process.argv[2] ?? "solution";
  const errors = await verifyFiles(target);
  if (errors.length > 0) {
    process.stderr.write(`Verification failed for ${target}:\n- ${errors.join("\n- ")}\n`);
    process.exitCode = 1;
  } else {
    process.stdout.write(`Verified ${target}: workflow structure, error path, and 4 fixture routes passed.\n`);
  }
}
