# Observability for AI Workflows

## Learning objectives

- Relate traces, metrics, logs, events, and user feedback.
- Define service-level indicators for quality, safety, latency, cost, and availability.
- Instrument without copying sensitive prompts into every telemetry system.

## Observe the whole request

A trace represents one request or workflow and contains nested spans for model calls, retrieval, tools, approvals, and downstream APIs. Metrics aggregate behavior over time. Logs explain discrete events. Feedback connects a trace to a user or reviewer outcome. Use a shared trace ID so an incident can be reconstructed without joining on raw personal text.

Useful span fields include operation, start/end time, status, model/provider, prompt-template version, input/output token counts, retriever and index version, retrieved document IDs and scores, tool name, retry count, approval request ID, and error class. Do not record hidden chain-of-thought. Raw messages and retrieved content may contain personal data, credentials, or proprietary material; default to hashes, lengths, classifications, and stable IDs. Enable sampled content capture only for a documented purpose with access, redaction, retention, and deletion controls.

Define indicators from user impact backward:

- end-to-end success and safe-abstention rate;
- p50/p95/p99 latency, including queue and approval time;
- tool failure, timeout, retry, and duplicate-effect rate;
- token and monetary cost per successful task;
- groundedness/correctness on sampled traces;
- security-policy blocks and confirmed incidents;
- retrieval hit rate on labeled traffic.

Averages conceal tails. Segment by workflow version, model, tool, language, tenant class, and input-size bucket while avoiding groups small enough to expose individuals.

## Free local practice

Instrument a fake three-step workflow: retrieve from a local dictionary, call a deterministic "model" function, and write a draft. Use Python's `time.perf_counter()`, `uuid`, `logging`, and JSON Lines. Emit one root event and child events containing `trace_id`, `span_id`, `parent_span_id`, operation, duration, status, version, and safe metadata.

Simulate 200 requests with a fixed random seed. Add controlled slowdowns and failures. Write a second script that computes success rate, error counts, p50/p95/p99 latency, retries per request, and approximate cost. Compare overall p95 with p95 by operation to find the bottleneck.

Add a redaction test containing an email address and fake API key. Assert neither raw value appears in telemetry. Document which content fields are disabled and how a privileged debugging sample would expire.

## Completion criteria

- One trace reconstructs model, retrieval, tool, and approval order.
- Metrics include tail latency and outcome/cost measures, not only request counts.
- A test proves known sensitive values are absent from default telemetry.
- Every event includes component and configuration versions needed to compare deployments.

## References

- [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/) - trace/span data model and context propagation.
- [OpenTelemetry metrics](https://opentelemetry.io/docs/concepts/signals/metrics/) - instruments and aggregation concepts.
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) - standard attributes and explicit content-sensitivity warnings.
- [Google SRE service-level objectives](https://sre.google/workbook/implementing-slos/) - selecting indicators and targets around user-visible behavior.
