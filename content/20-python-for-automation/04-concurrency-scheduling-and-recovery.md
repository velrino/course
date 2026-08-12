# Concurrency, Scheduling, and Recovery

## Learning objectives

- Choose sequential, threaded, asynchronous, or process-based execution appropriately.
- Bound concurrency, cancellation, retries, and global deadlines.
- Design scheduled jobs with locking, checkpoints, and safe recovery.

## Concurrency is a resource policy

Use sequential code until measurement shows a bottleneck. Threads or `asyncio` suit waiting on I/O; processes can help CPU-heavy pure Python but add serialization and lifecycle costs. Never create one unbounded task per input. Use a semaphore, worker pool, or bounded queue based on downstream rate limits and local memory.

Structured concurrency ties child-task lifetime to a parent scope. If one required task fails, cancel or collect others according to an explicit partial-success policy. Cancellation is cooperative: use context managers and `finally` blocks, and shield only tiny operations that must complete to preserve integrity.

A scheduler may start the same job twice or restart after a crash. Use a lock with ownership and expiry, a run ID, durable checkpoints, and idempotent item processing. Record `planned`, `started`, `succeeded`, and `failed` states. A checkpoint must represent committed work; updating it before the output is durable loses data.

Retries belong around the smallest safe operation. Use a dead-letter/quarantine path after exhaustion. Cap total job time and provide a graceful shutdown that stops accepting work, waits or cancels within a deadline, and leaves resumable state.

## Free local practice

Create 50 fake API tasks with deterministic delays and failures. Implement sequential and `asyncio` versions. In the async version, use `TaskGroup`, `Semaphore(5)`, per-call timeout, and a global timeout. Record observed maximum concurrency and show that it never exceeds five.

Persist item status in SQLite with a unique `(job_name, item_id, input_hash)` key. Simulate termination after 20 items, restart, and verify completed items are not repeated. Start two job instances and use an atomic database claim so each item is handled at most once. Move permanent failures to a table with error class and attempt history.

Measure total time, p95 item time, peak in-flight count, success/failed/cancelled counts, and retry distribution. Choose a concurrency value from evidence rather than maximum speed; explain its relationship to rate limit and resource budget.

## Completion criteria

- Sequential and concurrent variants produce the same logical results.
- Concurrency and global/per-operation deadlines are enforced under failure.
- Crash recovery and two-runner tests do not duplicate committed work.
- Permanent failures remain inspectable and replay requires an explicit action.

## References

- [Python asyncio tasks](https://docs.python.org/3/library/asyncio-task.html) - task groups, timeouts, cancellation, and shielding.
- [Python concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) - thread and process executor interfaces.
- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html) - transactional local state for checkpoints and claims.
- [Tenacity documentation](https://tenacity.readthedocs.io/en/latest/) - optional open-source retry policies and hooks.
