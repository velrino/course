import { createServer } from "node:http";

// TODO 1: Separate liveness from readiness.
// TODO 2: Persist the counter atomically under DATA_DIR.
// TODO 3: Add an authenticated failure-injection endpoint.
const server = createServer((request, response) => {
  if (request.url === "/health/live" || request.url === "/health/ready") {
    response.writeHead(200, { "content-type": "application/json" });
    response.end('{"status":"ok"}\n');
    return;
  }
  response.writeHead(501, { "content-type": "application/json" });
  response.end('{"error":"not_implemented"}\n');
});

server.listen(Number(process.env.PORT ?? 8080), "0.0.0.0");
