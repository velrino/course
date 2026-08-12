# Scaling, Monitoring, and Release Operations

## Learning objectives

By the end of this lesson, you can:

- decide whether concurrency tuning, queue mode, or workflow redesign addresses a bottleneck;
- define service-level indicators across request, queue, execution, and outcome;
- plan a version upgrade and workflow release with rollback evidence;
- build a runbook that an operator other than the author can execute.

## Measure before scaling

Separate:

- request latency at the webhook edge;
- queue wait time before a worker starts;
- execution duration by workflow and node;
- dependency latency and rate-limit delay;
- success, retry, failed-safe, and backlog counts;
- business outcome and guardrail measures.

A slow dependency is not fixed by adding workers; more concurrency may worsen throttling. Large payloads may need early filtering or external object storage. A workflow with repeated nested scans may need an algorithmic fix.

## Queue-mode architecture

In queue mode, the main n8n instance handles management and delegates executions through Redis to workers; PostgreSQL stores shared state. Optional webhook processors can separate inbound traffic. All components must share compatible configuration and the same encryption key, and versions should be upgraded together.

Queue mode adds operational dependencies and does not guarantee unlimited throughput. Define worker concurrency based on CPU, memory, dependency quotas, execution duration, and database capacity. Apply backpressure and maximum execution time.

Review binary-data constraints in the current official documentation before queue deployment. Do not assume a laptop filesystem is shared among workers.

## Signals and alerts

Enable supported metrics and structured logs according to the deployment documentation. Useful service-level indicators include:

- accepted webhook requests;
- queue age and depth;
- execution success/error rate;
- p50/p95/p99 duration;
- retry and 429 rate;
- worker availability and saturation;
- database/Redis connectivity;
- business completion, review, duplicate, and guardrail rates.

An alert must name an owner and action. "Error rate high" is incomplete without window, threshold, runbook, and severity.

## Release and rollback

1. Pin and record the current application version.
2. Read release notes and breaking changes.
3. Back up database, encryption key, configuration, and workflows; test restore.
4. Test the candidate version against representative synthetic cases in a separate environment.
5. Export and review workflow changes; keep credentials environment-specific.
6. Deploy during an owned window, run smoke tests, and observe guardrails.
7. Roll back workflow definitions if needed. For application/database downgrades, follow official compatibility guidance; migrations may not be safely reversible.

Commercial source-control/environment features are not required for learning. Community Edition users can maintain reviewed exports in private version control, keep secrets separate, and use a documented manual promotion process.

## Free local practice

1. Use a local webhook workflow with a deterministic 100-300 ms delay.
2. Send 1, 5, and 20 concurrent synthetic requests with a shell script or local load tool.
3. Record accepted count, p95 response time, execution duration, failure count, and backlog/overlap behavior.
4. Repeat with reduced concurrency or batch size and explain the change.
5. Enable locally supported metrics/logging and create a one-page dashboard table. No hosted observability product is required.
6. Write two alerts: sustained error rate and oldest failed-safe item. Include threshold, window, severity, owner, and exact first actions.
7. Export workflows and back up the lab instance. Upgrade a separate disposable copy to a newer pinned version, run smoke cases, and prove the original remains restorable.
8. Give the runbook to another person, or execute it later without relying on memory. Record unclear steps.

## Completion criteria

You are finished when:

- bottlenecks are separated across edge, queue, workflow, dependency, and outcome;
- any scaling proposal includes capacity and rate-limit evidence;
- queue-mode components, shared configuration, and new failure modes are understood;
- logs and metrics omit secrets and unnecessary bodies;
- alerts have thresholds, windows, owners, and actions;
- the release plan includes notes review, backup, restore test, smoke test, and observation;
- rollback claims account for database migration compatibility;
- another operator can use the runbook without oral knowledge.

## References

- [n8n documentation: Scaling overview](https://docs.n8n.io/hosting/scaling/overview/) - official scaling and performance entry point.
- [n8n documentation: Configuring queue mode](https://docs.n8n.io/hosting/scaling/queue-mode/) - official main, Redis, worker, database, concurrency, and webhook processor architecture.
- [n8n documentation: Monitoring](https://docs.n8n.io/hosting/logging-monitoring/monitoring/) - official health and Prometheus metric endpoints.
- [n8n documentation: Performance and benchmarking](https://docs.n8n.io/hosting/scaling/performance-benchmarking/) - official load-testing considerations and benchmark tooling.
- [n8n documentation: Updating](https://docs.n8n.io/hosting/installation/updating/) - official release channel, version, and update guidance.
