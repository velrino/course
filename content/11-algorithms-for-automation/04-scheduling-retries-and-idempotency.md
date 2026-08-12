# Scheduling, Retries, and Idempotency

## Learning objectives

By the end of this lesson, you can:

- distinguish scheduled, polled, event-driven, and manually triggered automation;
- classify failures as permanent, transient, throttled, or unknown;
- design exponential backoff with jitter and a retry budget;
- make repeated delivery safe with idempotency keys and durable records.

## Triggers have different failure modes

- **Schedule:** simple, but overlapping runs and missed windows need policy.
- **Polling:** works without webhooks, but creates latency, duplicate reads, and rate pressure.
- **Event/webhook:** fast, but delivery may be duplicated, delayed, or out of order.
- **Manual:** valuable for sensitive operations and recovery.

Assume at-least-once delivery unless a system provides and proves stronger semantics. "Exactly once" is usually an application property built from durable identity, uniqueness, and safe replay.

## Retry only recoverable work

Classify:

- permanent: invalid input or forbidden action; do not retry unchanged;
- transient: timeout or temporary unavailability; retry within budget;
- throttled: honor Retry-After when provided;
- unknown: stop or retry cautiously based on whether the prior side effect may have happened.

Use capped exponential backoff with jitter:

~~~text
delay = min(cap, base * 2^attempt) + random_jitter
~~~

Jitter prevents many workers from retrying simultaneously. A retry budget limits attempts and total elapsed time. After exhaustion, move the case to a durable failed-safe queue with context for human recovery.

## Idempotency before side effects

An idempotency key should represent one intended business operation, not merely one network request. Store:

| key | request_hash | status | external_reference | started_at | completed_at |
| --- | --- | --- | --- | --- | --- |

Algorithm:

1. Derive or receive a stable key.
2. Atomically reserve it with the request hash.
3. If an existing completed record has the same hash, return its result.
4. If the key exists with a different hash, reject the conflict.
5. Perform the side effect using the same key if the API supports it.
6. Persist the confirmed external reference.

An in-memory set is enough for a learning simulation, not for production across restarts.

## Free local practice

Build a Python simulator with the standard library.

1. Represent ten events, including three duplicates and one conflicting duplicate.
2. Use SQLite through Python's sqlite3 module for the idempotency table.
3. Simulate an external call that fails twice before succeeding.
4. Calculate retry delays, but replace actual sleeping with printed scheduled timestamps.
5. Respect a simulated Retry-After value.
6. Interrupt the script after reserving one key, restart it, and define how stale in-progress work is recovered.
7. Print counts for unique operations, deduplicated events, conflicts, attempts, successes, and exhausted cases.

Do not call a real paid API. Make the failure sequence deterministic by providing it as input.

## Completion criteria

You are finished when:

- trigger choice and its delivery assumptions are documented;
- permanent failures are not retried unchanged;
- retry delay is capped, jittered, and bounded by attempts and elapsed time;
- throttling instructions are honored;
- idempotency survives a local process restart;
- same-key/different-payload conflicts are rejected;
- uncertain prior side effects cannot be blindly repeated;
- exhausted work is retained for inspection and recovery.

## References

- [IETF RFC 9110: HTTP semantics, idempotent methods](https://datatracker.ietf.org/doc/html/rfc9110#section-9.2.2) - primary definition and retry implications of idempotency.
- [IETF RFC 6585: Additional HTTP status codes](https://datatracker.ietf.org/doc/html/rfc6585#section-4) - primary definition of 429 Too Many Requests and Retry-After behavior.
- [AWS Architecture Blog: Exponential backoff and jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/) - public engineering analysis and retry patterns.
- [Python sqlite3 module](https://docs.python.org/3/library/sqlite3.html) - official local transactional database interface used in the exercise.
