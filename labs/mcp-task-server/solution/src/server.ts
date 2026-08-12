import { resolve } from "node:path";
import { McpServer } from "@modelcontextprotocol/server";
import * as z from "zod/v4";
import { StoreError, TaskIdSchema, TaskStore } from "./task-store.js";

const ScopeSchema = z.enum(["read", "read-write"]);

function jsonResult(value: unknown) {
  return { content: [{ type: "text" as const, text: JSON.stringify(value, null, 2) }] };
}

function errorResult(error: unknown) {
  const known = error instanceof StoreError;
  return {
    content: [{
      type: "text" as const,
      text: JSON.stringify({
        error: known ? error.code : "internal_error",
        message: known ? error.message : "Unexpected task server error.",
      }),
    }],
    isError: true,
  };
}

export function createTaskServer(environment: NodeJS.ProcessEnv = process.env): McpServer {
  const root = resolve(environment.TASKS_ROOT ?? "fixtures/workspace");
  const scope = ScopeSchema.catch("read").parse(environment.TASK_SCOPE);
  const store = new TaskStore(root);
  const server = new McpServer(
    { name: "course-task-server", version: "1.0.0" },
    { instructions: `Task workspace access is ${scope}. Use task IDs, never file paths.` },
  );

  server.registerTool(
    "list-tasks",
    {
      description: "List tasks in the configured workspace, optionally filtered by status.",
      inputSchema: z.object({ status: z.enum(["open", "completed"]).optional() }).strict(),
    },
    async ({ status }) => {
      try { return jsonResult({ tasks: await store.list(status) }); }
      catch (error) { return errorResult(error); }
    },
  );

  server.registerTool(
    "get-task",
    {
      description: "Read one task by its narrow task ID. File paths are not accepted.",
      inputSchema: z.object({ taskId: TaskIdSchema }).strict(),
    },
    async ({ taskId }) => {
      try { return jsonResult({ task: await store.get(taskId) }); }
      catch (error) { return errorResult(error); }
    },
  );

  if (scope === "read-write") {
    server.registerTool(
      "create-task",
      {
        description: "Create one new task. This tool exists only in a read-write server process.",
        inputSchema: z.object({
          taskId: TaskIdSchema,
          title: z.string().min(1).max(120),
          details: z.string().max(2000).optional(),
        }).strict(),
      },
      async ({ taskId, title, details }) => {
        try { return jsonResult({ task: await store.create({ id: taskId, title, ...(details === undefined ? {} : { details }) }) }); }
        catch (error) { return errorResult(error); }
      },
    );

    server.registerTool(
      "complete-task",
      {
        description: "Mark one existing task complete. Repeating the call is idempotent.",
        inputSchema: z.object({
          taskId: TaskIdSchema,
          completionNote: z.string().max(500).optional(),
        }).strict(),
      },
      async ({ taskId, completionNote }) => {
        try { return jsonResult({ task: await store.complete(taskId, completionNote) }); }
        catch (error) { return errorResult(error); }
      },
    );
  }

  return server;
}
