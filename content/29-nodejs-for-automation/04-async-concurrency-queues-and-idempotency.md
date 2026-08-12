# Async Concurrency, Queues, and Idempotency

Launching a promise for every item in a large input is not a concurrency strategy. It can exhaust sockets, file descriptors, memory, or an API quota. A worker must bound in-flight work, propagate cancellation, classify failures, and preserve enough state to recover after a crash.

Most durable queues provide at-least-once delivery: a consumer may finish the side effect and crash before acknowledging, so the message returns. The consumer must therefore tolerate duplicates. "Exactly once" is usually achieved as an observable business result through idempotency and transactional boundaries, not by assuming that a handler executes only once.

## Learning objectives

- Contrast event-loop concurrency with CPU parallelism through worker threads.
- Implement a bounded promise worker pool.
- Retry transient failures with a cap and route exhausted jobs to a dead-letter collection.
- Use a stable business key and an atomic claim for local idempotency.
- Identify the crash window between an external side effect and a local completion marker.
- Handle `SIGINT` and `SIGTERM` by stopping new work and awaiting in-flight work.

## Queue and idempotency design

A queue message should carry a stable message ID, a business idempotency key, schema version, attempt count, and trace or correlation ID. The payload should be small; store large artifacts elsewhere with integrity metadata. Consumers validate the schema before side effects.

Set concurrency from measured constraints: downstream quotas, database connection limits, memory, and latency. Increasing concurrency can reduce throughput when a service begins throttling. CPU-heavy parsing, compression, or transformation still blocks the event loop; split that work into worker threads or separate processes only after profiling.

An idempotency record needs states and recovery semantics. A permanent lock created before a side effect can suppress legitimate recovery after a crash. A completion record written after the side effect leaves a duplicate window. For an external API, pass the same idempotency key to that API. For a database, put the business mutation and unique idempotency record in one transaction. Locks also need ownership and lease expiry in distributed systems.

## Free local practice

Create `src/queue-runner.js`. This exercise uses atomic local files to coordinate duplicate jobs in one directory:

```javascript
import { createHash, randomUUID } from "node:crypto";
import { mkdir, open, readFile, rename, unlink, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { setTimeout as sleep } from "node:timers/promises";

const stateDir = "var/job-state";
const attemptsById = new Map();

async function mapLimit(items, limit, task, signal) {
  if (!Number.isInteger(limit) || limit < 1) throw new RangeError("limit must be positive");
  const results = new Array(items.length);
  let next = 0;

  async function worker() {
    while (true) {
      if (signal?.aborted) return;
      const index = next;
      next += 1;
      if (index >= items.length) return;
      results[index] = await task(items[index], index);
    }
  }

  const workers = Array.from({ length: Math.min(limit, items.length) }, () => worker());
  await Promise.all(workers);
  return results;
}

function pathsFor(key) {
  const digest = createHash("sha256").update(key).digest("hex");
  return {
    done: join(stateDir, `${digest}.json`),
    lock: join(stateDir, `${digest}.lock`)
  };
}

async function readCompleted(path) {
  try {
    return JSON.parse(await readFile(path, "utf8"));
  } catch (error) {
    if (error?.code === "ENOENT") return null;
    throw error;
  }
}

async function runOnce(job, effect) {
  await mkdir(stateDir, { recursive: true });
  const paths = pathsFor(job.idempotencyKey);
  const previous = await readCompleted(paths.done);
  if (previous) return { state: "duplicate", result: previous.result };

  let handle;
  try {
    handle = await open(paths.lock, "wx", 0o600);
  } catch (error) {
    if (error?.code === "EEXIST") return { state: "busy" };
    throw error;
  }

  try {
    const result = await effect(job);
    const temporary = `${paths.done}.${process.pid}.${randomUUID()}.tmp`;
    try {
      await writeFile(temporary, `${JSON.stringify({ result })}\n`, { flag: "wx", mode: 0o600 });
      await rename(temporary, paths.done);
    } finally {
      await unlink(temporary).catch((error) => {
        if (error?.code !== "ENOENT") throw error;
      });
    }
    return { state: "completed", result };
  } finally {
    await handle.close();
    await unlink(paths.lock).catch((error) => {
      if (error?.code !== "ENOENT") throw error;
    });
  }
}

async function simulatedEffect(job, signal) {
  const attempt = (attemptsById.get(job.id) ?? 0) + 1;
  attemptsById.set(job.id, attempt);
  await sleep(100, undefined, { signal });
  if (job.id === "b" && attempt < 3) throw new Error("temporary dependency failure");
  return { id: job.id, value: job.value.toUpperCase() };
}

async function processJob(job, signal, maximumAttempts = 4) {
  for (let attempt = 1; attempt <= maximumAttempts; attempt += 1) {
    if (signal.aborted) throw signal.reason;
    try {
      const outcome = await runOnce(job, (value) => simulatedEffect(value, signal));
      if (outcome.state === "busy") throw new Error("idempotency key is busy");
      return { ...outcome, attempt };
    } catch (error) {
      if (signal.aborted || attempt === maximumAttempts) throw error;
      await sleep(200 * (2 ** (attempt - 1)), undefined, { signal });
    }
  }
}

const controller = new AbortController();
for (const signalName of ["SIGINT", "SIGTERM"]) {
  process.once(signalName, () => controller.abort(new Error(`received ${signalName}`)));
}

const jobs = [
  { id: "a", idempotencyKey: "account:7:month:2026-08", value: "first" },
  { id: "b", idempotencyKey: "account:8:month:2026-08", value: "retry" },
  { id: "a-copy", idempotencyKey: "account:7:month:2026-08", value: "duplicate" }
];
const deadLetters = [];

const results = (await mapLimit(jobs, 2, async (job) => {
  try {
    return await processJob(job, controller.signal);
  } catch (error) {
    if (controller.signal.aborted) return { state: "cancelled" };
    deadLetters.push({ job, error: error instanceof Error ? error.message : String(error) });
    return { state: "dead-lettered" };
  }
}, controller.signal)).filter(Boolean);

console.log(JSON.stringify({ results, deadLetters }, null, 2));
if (controller.signal.aborted) process.exitCode = 130;
else if (deadLetters.length > 0) process.exitCode = 1;
```

Run it twice:

```sh
node src/queue-runner.js
node src/queue-runner.js
```

The second run should read completion records instead of repeating completed effects. Delete `var/job-state`, run again, and press `Ctrl+C` during a retry to exercise cancellation. Then change `maximumAttempts` to 2 and observe job `b` move to the in-memory dead-letter collection.

This demo intentionally exposes two limitations. Its job source and dead-letter collection are not durable, and a process crash after `simulatedEffect` but before the rename can cause the effect to repeat. Repair the first with a real durable queue. Repair the second by making the effect itself idempotent, or by combining the mutation and completion record in one transactional data store. Do not solve stale `.lock` files by deleting every lock at startup when multiple workers may be alive; use owner identity and leases.

## Completion criteria

- At most two jobs are in flight in the practice runner.
- The temporary failure is retried with increasing delays and a strict attempt limit.
- Duplicate business keys resolve to one stored completion result, including on a later process run.
- An exhausted job is visible in dead-letter output rather than silently discarded.
- `SIGINT` aborts waits and no new process-level `process.exit()` call truncates cleanup.
- You can locate the remaining crash window and describe a transactional or downstream-idempotency repair.
- You can explain when `worker_threads` helps and why it is not required for ordinary network concurrency.

## References

- [Node.js: Do not block the event loop](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop)
- [Node.js: Timers promises API](https://nodejs.org/api/timers.html#timers-promises-api)
- [Node.js: Worker threads](https://nodejs.org/api/worker_threads.html)
- [Node.js: Process signals](https://nodejs.org/api/process.html#signal-events)
- [Node.js: File system `open`](https://nodejs.org/api/fs.html#fspromisesopenpath-flags-mode)
- [Amazon Builders' Library: Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

[Next lesson: Testing, Logging, and an Automation Capstone](./05-testing-logging-and-automation-capstone.md)
