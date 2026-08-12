# Docker Health and Persistence Stack Lab

Package a small stateful Node.js service as a hardened container, distinguish liveness from readiness, persist data through replacement, and observe a controlled health failure.

## Prerequisites

- Node.js 20 or later for local tests
- Docker Engine with the Compose v2 plugin for the container exercise
- `curl`

## Goals

- Run the application as a numeric non-root user.
- Keep the container root filesystem read-only.
- Persist mutable state in a named volume and update it atomically.
- Make liveness answer "is the process running?" and readiness answer "can it safely serve traffic?".
- Gate a dependent service on `service_healthy`.
- Inject and clear a readiness failure without killing the process.

## Architecture

```mermaid
flowchart LR
    Host[Host curl] -->|port 8080| App[Node app as UID 10001]
    App --> Live[/health/live]
    App --> Ready[/health/ready]
    App --> Counter[/counter]
    Counter --> Volume[(state-data volume)]
    Ready --> Volume
    Probe[One-shot readiness probe] -->|waits for healthy| Ready
    Failure[/admin/failure] -->|flag| Volume
```

## Layout

- `starter/` has explicit TODOs in the app, Dockerfile, and Compose file.
- `solution/` contains the reference stack.
- `test/app.test.mjs` runs the service directly with temporary state.
- `scripts/verify.mjs` statically checks container and Compose invariants.
- `fixtures/` records representative state and probe expectations.

## Verify without Docker

```bash
cd labs/docker-health-stack
npm test
npm run verify
```

The tests cover healthy operation, unauthorized and authorized failure injection, readiness degradation, recovery, concurrent increments, restart persistence, corrupt state, and static configuration omissions.

`npm run verify:starter` is expected to fail until all TODOs are complete.

## Run the Compose stack

```bash
FAILURE_TOKEN=choose-a-local-token docker compose -f solution/compose.yaml up --build -d
docker compose -f solution/compose.yaml ps
curl -sS http://127.0.0.1:8080/health/live
curl -sS http://127.0.0.1:8080/health/ready
curl -sS -X POST http://127.0.0.1:8080/counter
curl -sS http://127.0.0.1:8080/counter
```

Expected healthy responses include `{"status":"alive"}`, `{"status":"ready"}`, and a counter value that increases by one.

## Persistence exercise

Replace the app container without deleting the named volume:

```bash
docker compose -f solution/compose.yaml down
FAILURE_TOKEN=choose-a-local-token docker compose -f solution/compose.yaml up --build -d
curl -sS http://127.0.0.1:8080/counter
```

The value should survive. `docker compose down -v` intentionally deletes the volume and resets the lab.

## Failure injection

```bash
curl -i -X POST http://127.0.0.1:8080/admin/failure \
  -H 'content-type: application/json' \
  -H 'x-failure-token: choose-a-local-token' \
  -d '{"reason":"readiness drill"}'
sleep 20
docker compose -f solution/compose.yaml ps
curl -i http://127.0.0.1:8080/health/live
curl -i http://127.0.0.1:8080/health/ready
```

The process stays live, but readiness returns 503 and Docker eventually marks the container unhealthy. Recover it:

```bash
curl -i -X DELETE http://127.0.0.1:8080/admin/failure \
  -H 'x-failure-token: choose-a-local-token'
```

## Learner tasks

1. Implement distinct liveness and readiness behavior in the starter app.
2. Persist a non-negative counter under `DATA_DIR` using write-then-rename.
3. Serialize concurrent counter mutations.
4. Protect failure injection with a token and keep secrets out of responses and logs.
5. Create and select a numeric non-root image user.
6. Add image and Compose health checks against readiness.
7. Mount a named volume, make the root filesystem read-only, drop capabilities, and prevent privilege escalation.
8. Add a probe service gated by `condition: service_healthy`.

## Hints

- A liveness check should not depend on a database or writable volume; otherwise an orchestrator may restart a process that cannot fix the dependency.
- A read-only root filesystem still permits writes to explicitly mounted volumes and `tmpfs` paths.
- Write a complete temporary file and rename it over the target to avoid partial JSON after a crash.
- Do not expose an unauthenticated chaos endpoint in a real system.

## Completion criteria

- `npm test` and `npm run verify:starter` pass after completing the starter.
- The running process UID is not zero: `docker compose -f starter/compose.yaml exec app id`.
- A counter value survives `docker compose down` followed by `up`, but resets after `down -v`.
- Injected failure changes readiness to 503 while liveness remains 200.
- Clearing failure returns the container to healthy without replacement.
- The learner can identify which settings are application guarantees and which are container-runtime controls.

## References

- [Dockerfile HEALTHCHECK](https://docs.docker.com/reference/dockerfile/#healthcheck)
- [Compose healthcheck](https://docs.docker.com/reference/compose-file/services/#healthcheck)
- [Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/)
- [Docker volumes](https://docs.docker.com/engine/storage/volumes/)
- [Docker build security recommendations](https://docs.docker.com/build/building/best-practices/)
