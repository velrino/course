# Testing, Complexity, and Observability

## Learning objectives

By the end of this lesson, you can:

- test pure rules, state transitions, integration contracts, and end-to-end behavior;
- reason about input growth and avoid accidental quadratic work;
- define logs, metrics, and traces around user and operational outcomes;
- construct a deterministic test harness for automation logic.

## Test at several boundaries

- **Unit tests:** pure normalization, validation, sorting, and decision rules.
- **Property tests:** invariants over many generated examples, such as "normalization is idempotent."
- **State-transition tests:** allowed and illegal events from every state.
- **Contract tests:** request/response schemas and error behavior at an API boundary.
- **Integration tests:** local stub, database, queue, or n8n node composition.
- **End-to-end tests:** representative path through the deployed workflow with synthetic data.

A test must control time, randomness, and external responses. Inject a clock and a predetermined failure sequence rather than waiting for real time or relying on a live service.

## Complexity matters at automation scale

If each of n records scans all n records for duplicates, work grows roughly as n squared. A set or map usually reduces membership checks to near constant average time, making the pass roughly linear.

Measure rather than guess:

1. Generate 100, 1,000, and 10,000 synthetic records.
2. Time the same operation after a warm-up.
3. Record input size, duration, memory, and environment.
4. Look at the growth ratio, not a single duration.

Also bound payload size, batch size, loop count, concurrency, and retained history. Correct logic can still exhaust memory or overload a dependency.

## Observable outcomes

Three signals answer different questions:

- **Logs:** what happened to a specific case? Use structured fields and correlation IDs.
- **Metrics:** is the service healthy over time? Track throughput, latency, errors, retries, backlog, and business guardrails.
- **Traces:** where did time and failure occur across steps and services?

Avoid logging request bodies, secrets, model prompts, or personal data by default. Log identifiers, versions, classifications, durations, and reason codes. Redaction after ingestion is weaker than not collecting the field.

## Free local practice

1. Put the pure functions from earlier lessons in automation.py.
2. Create tests with Python unittest; include normal, missing, boundary, duplicate, unauthorized, illegal-transition, and retry-exhaustion cases.
3. Add a test asserting that processing the same idempotency key twice produces one simulated side effect.
4. Create 100, 1,000, and 10,000 synthetic records. Compare list-based duplicate search with a set-based method.
5. Emit one JSON log per case:

~~~json
{"event":"case_completed","case_id":"case-007","duration_ms":18,"attempts":1,"rule_version":"v1"}
~~~

6. Aggregate logs locally to calculate success rate, p95 duration, retry rate, and failed-safe count.
7. Verify logs contain none of the synthetic email/body fields.
8. Write a short conclusion separating functional correctness, performance limits, and remaining operational risk.

## Completion criteria

You are finished when:

- pure, transition, contract, and end-to-end behaviors have distinct tests;
- time, randomness, and failures are controlled by the test;
- duplicates and retries prove the side-effect invariant;
- performance is measured across at least three input sizes;
- batch, payload, retry, and concurrency bounds are stated;
- logs are structured, correlated, and free of secret/body fields;
- metrics include technical health and business guardrails;
- the test report records failures and limits, not only passing totals.

## References

- [Python unittest framework](https://docs.python.org/3/library/unittest.html) - official standard-library framework for fixtures, assertions, suites, and test doubles.
- [Python timeit module](https://docs.python.org/3/library/timeit.html) - official method for repeatable small-code performance measurement.
- [OpenTelemetry: Signals](https://opentelemetry.io/docs/concepts/signals/) - official open standard concepts for traces, metrics, logs, and baggage.
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) - public guidance on useful security logging and data that should not be recorded.
