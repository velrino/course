# Resilience, Rate Limits, and Idempotency

## Learning objectives

By the end of this lesson, you can:

- configure retries only for errors likely to recover;
- respect rate limits with batching, delay, and Retry-After;
- prevent duplicate external effects across webhook redelivery and manual replay;
- route exhausted work into an inspectable recovery path.

## Failure policy by class

Build an explicit matrix:

| class | examples | action |
| --- | --- | --- |
| Validation | Missing field, bad type | No retry; return needs_review |
| Authorization | 401, 403 | No blind retry; alert credential/permission owner |
| Conflict | 409 | Reconcile by business key |
| Throttling | 429 | Honor Retry-After, reduce concurrency |
| Transient | Timeout, selected 5xx | Bounded retry with backoff |
| Unknown outcome | Connection lost after POST | Check by idempotency key before retry |

n8n's Retry On Fail can help at node level, but a fixed retry setting is not a full policy. When response-specific delays are required, route the result through Wait and a bounded attempt counter. Do not create a branch that loops without a maximum.

## Rate control

Use provider headers and documentation to determine the window. Combine:

- smaller batches;
- concurrency limits;
- Wait between batches;
- Retry-After for 429;
- queueing and backpressure;
- caching or incremental fetches to reduce demand.

Rate limit protection belongs before the dependency is saturated. Success under a manual test says little about parallel production load.

## Durable idempotency

For writes, require an event or operation ID from the caller when possible. Reserve it in a durable store before the action. n8n Data Tables can help in learning and some deployments; a database with a unique constraint and transaction is the stronger production pattern.

Record pending, completed, failed-safe, request hash, external reference, and timestamps. A duplicate completed request returns the stored outcome. A duplicate key with a different hash is a conflict. A stale pending record needs reconciliation, not automatic repetition.

## Free local practice

Use the local Mock Catalog API and client.

1. Make the mock return 429 twice with a Retry-After value, then 200 for a known event ID.
2. In the client, track attempt_count and max_attempts. Wait according to the mock without using long delays.
3. Store event_id and request hash before the simulated write in a Data Table or local PostgreSQL instance.
4. Send the same event three times. Verify only one mock resource is created.
5. Send the same event ID with a changed body. Return conflict and perform no write.
6. Simulate connection loss after creation but before the client receives the response. On retry, query by the operation ID and recover the original reference.
7. Exhaust one transient failure and send it to a failed-safe recovery workflow with reason, attempt count, and correlation ID.
8. Graph or tabulate attempts, waits, unique writes, duplicates, conflicts, and recoveries.

## Completion criteria

You are finished when:

- failure classes lead to different documented actions;
- 4xx validation/authorization errors are not blindly retried;
- Retry-After and maximum attempts are enforced;
- batch size and concurrency assumptions are stated;
- a durable unique key prevents duplicate writes;
- same-key/different-request conflicts are rejected;
- uncertain outcomes are reconciled before another write;
- exhausted cases remain recoverable with useful metadata.

## References

- [n8n documentation: Handle rate limits](https://docs.n8n.io/integrations/builtin/rate-limits/) - official batching, retry, and loop approaches for API limits.
- [n8n documentation: Node settings](https://docs.n8n.io/workflows/components/nodes/#node-settings) - official Retry On Fail and error behavior configuration.
- [n8n documentation: Wait node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait/) - official pause and resume mechanisms.
- [IETF RFC 9110: Idempotent methods](https://datatracker.ietf.org/doc/html/rfc9110#section-9.2.2) - primary retry and idempotency semantics.
- [IETF RFC 6585: 429 Too Many Requests](https://datatracker.ietf.org/doc/html/rfc6585#section-4) - primary throttling status definition.
