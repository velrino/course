import { serveStdio } from "@modelcontextprotocol/server/stdio";
import { createTaskServer } from "./server.js";

const handle = serveStdio(() => createTaskServer());
console.error("course-task-server starter listening on stdio");

process.on("SIGINT", () => {
  void handle.close();
});
