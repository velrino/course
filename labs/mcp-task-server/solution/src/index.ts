import { serveStdio } from "@modelcontextprotocol/server/stdio";
import { createTaskServer } from "./server.js";

const handle = serveStdio(() => createTaskServer());
console.error(`course-task-server listening on stdio with ${process.env.TASK_SCOPE ?? "read"} scope`);

process.on("SIGINT", () => {
  void handle.close();
});
