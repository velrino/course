# Project: Stateful Support Routing

## Learning objectives

Integrate LangChain interfaces and LangGraph control flow in a bounded project with measurable behavior and no required paid service.

## Free local practice

## Project brief

Build a support-routing workflow that accepts a synthetic request, classifies its topic and urgency, retrieves a matching policy excerpt, proposes a response, and requires approval for high-impact categories. The system must never send a message; its final side effect is writing an approved draft to a local file or test database.

Implement two modes:

- **Deterministic mode:** keyword rules and fixed response templates.
- **Model mode:** an optional chat-model adapter that returns the same validated schemas.

The deterministic mode is the test oracle for control flow. Model mode may improve language flexibility, but it may not bypass policy, authorization, or approval nodes.

## Required graph

```text
validate input
  -> classify
  -> retrieve policy
  -> draft
  -> policy check
       -> ordinary queue
       -> human review
       -> reject
  -> persist approved draft
```

Record a reason code at every branch. Store source identifiers with the draft. Bound loops with a maximum attempt count and route exhausted attempts to review.

## Evaluation set

Create at least 30 synthetic cases across routine, ambiguous, urgent, prohibited, prompt-injection, missing-policy, and tool-failure categories. Measure:

- correct route rate;
- prohibited action rate;
- evidence citation coverage;
- schema failure rate;
- human-review rate;
- p50 and p95 execution time.

Inspect errors individually. A single average score cannot tell you whether failures are harmless formatting differences or dangerous routing mistakes.

## Deliverables

- Architecture and trust-boundary diagram.
- State schema and graph visualization.
- Deterministic and optional model adapters.
- Versioned evaluation cases and test runner.
- Approval screen or terminal interaction.
- Risk register, runbook, and short evaluation report.

## Completion criteria

- A fresh install can run deterministic mode without credentials.
- All prohibited cases end in review or rejection.
- External-looking actions are local fakes with idempotency tests.
- The report separates quality, safety, latency, and resource measures.
- Limitations and unsupported uses are explicit.

## References

- [LangChain tutorials](https://docs.langchain.com/oss/python/learn)
- [LangChain context engineering](https://docs.langchain.com/oss/python/langchain/context-engineering)
- [LangChain middleware](https://docs.langchain.com/oss/python/langchain/middleware/overview)
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
