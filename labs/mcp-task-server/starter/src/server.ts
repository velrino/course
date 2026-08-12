import { McpServer } from "@modelcontextprotocol/server";
import * as z from "zod/v4";

export function createTaskServer(): McpServer {
  const server = new McpServer({ name: "course-task-server-starter", version: "1.0.0" });

  server.registerTool(
    "list-tasks",
    {
      description: "TODO: list only schema-valid task files inside TASKS_ROOT.",
      inputSchema: z.object({ status: z.enum(["open", "completed"]).optional() }).strict(),
    },
    async () => ({ content: [{ type: "text", text: JSON.stringify({ tasks: [] }) }] }),
  );

  // TODO 1: Create a TaskStore with strict task IDs and a fixed root.
  // TODO 2: Refuse symbolic links and never return absolute paths in errors.
  // TODO 3: Register get-task for every scope.
  // TODO 4: Register create-task and complete-task only for read-write scope.
  // TODO 5: Validate every tool argument with narrow Zod schemas.
  // TODO 6: Return safe isError tool results for expected store failures.
  return server;
}
