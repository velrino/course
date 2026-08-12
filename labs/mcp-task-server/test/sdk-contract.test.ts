import assert from "node:assert/strict";
import { cp, mkdtemp, rm, symlink } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";
import { Client } from "@modelcontextprotocol/client";
import { StdioClientTransport } from "@modelcontextprotocol/client/stdio";

const labRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const target = process.env.LAB_TARGET ?? "solution";
const entry = join(labRoot, target, "src", "index.ts");

function cleanEnvironment(): Record<string, string> {
  return Object.fromEntries(Object.entries(process.env).filter((entry): entry is [string, string] => entry[1] !== undefined));
}

async function workspace(run: (root: string) => Promise<void>): Promise<void> {
  const temporary = await mkdtemp(join(tmpdir(), "mcp-task-lab-"));
  const root = join(temporary, "tasks");
  await cp(join(labRoot, "fixtures", "workspace"), root, { recursive: true });
  try { await run(root); } finally { await rm(temporary, { recursive: true, force: true }); }
}

async function connect(root: string, scope: "read" | "read-write") {
  const client = new Client({ name: "course-task-test-client", version: "1.0.0" });
  const transport = new StdioClientTransport({
    command: process.execPath,
    args: ["--import", "tsx", entry],
    cwd: labRoot,
    env: { ...cleanEnvironment(), TASKS_ROOT: root, TASK_SCOPE: scope },
    stderr: "pipe",
  });
  await client.connect(transport);
  return client;
}

function textJson(result: Awaited<ReturnType<Client["callTool"]>>): any {
  const block = result.content.find((item) => item.type === "text");
  assert.ok(block && block.type === "text");
  return JSON.parse(block.text);
}

test("read scope exposes only narrow read tools", async () => workspace(async (root) => {
  const client = await connect(root, "read");
  try {
    const listed = await client.listTools();
    assert.deepEqual(listed.tools.map((tool) => tool.name).sort(), ["get-task", "list-tasks"]);
    const result = await client.callTool({ name: "list-tasks", arguments: { status: "open" } });
    assert.equal(result.isError, undefined);
    assert.deepEqual(textJson(result).tasks.map((task: { id: string }) => task.id), ["prepare-release"]);
  } finally { await client.close(); }
}));

test("SDK validation rejects traversal-shaped and extra arguments", async () => workspace(async (root) => {
  const client = await connect(root, "read");
  try {
    const traversal = await client.callTool({ name: "get-task", arguments: { taskId: "../archive-invoices" } });
    assert.equal(traversal.isError, true);
    const extra = await client.callTool({ name: "get-task", arguments: { taskId: "prepare-release", path: "/etc/passwd" } });
    assert.equal(extra.isError, true);
  } finally { await client.close(); }
}));

test("missing and symbolic-link task files fail without leaking filesystem paths", async () => workspace(async (root) => {
  await symlink("/etc/passwd", join(root, "outside.json"));
  const client = await connect(root, "read");
  try {
    const missing = await client.callTool({ name: "get-task", arguments: { taskId: "does-not-exist" } });
    assert.equal(missing.isError, true);
    assert.equal(textJson(missing).error, "task_not_found");
    assert.doesNotMatch(JSON.stringify(missing), new RegExp(root.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
    const linked = await client.callTool({ name: "get-task", arguments: { taskId: "outside" } });
    assert.equal(linked.isError, true);
    assert.equal(textJson(linked).error, "unsafe_task_file");
  } finally { await client.close(); }
}));

test("read-write scope creates and idempotently completes a task", async () => workspace(async (root) => {
  const client = await connect(root, "read-write");
  try {
    const names = (await client.listTools()).tools.map((tool) => tool.name).sort();
    assert.deepEqual(names, ["complete-task", "create-task", "get-task", "list-tasks"]);
    const created = await client.callTool({
      name: "create-task",
      arguments: { taskId: "review-access", title: "Review access list", details: "Remove expired contractor accounts." },
    });
    assert.equal(textJson(created).task.status, "open");
    const duplicate = await client.callTool({
      name: "create-task",
      arguments: { taskId: "review-access", title: "Duplicate" },
    });
    assert.equal(duplicate.isError, true);
    assert.equal(textJson(duplicate).error, "task_exists");
    const first = await client.callTool({
      name: "complete-task",
      arguments: { taskId: "review-access", completionNote: "Expired accounts removed." },
    });
    const second = await client.callTool({ name: "complete-task", arguments: { taskId: "review-access" } });
    assert.equal(textJson(first).task.status, "completed");
    assert.equal(textJson(second).task.completedAt, textJson(first).task.completedAt);
  } finally { await client.close(); }
}));
