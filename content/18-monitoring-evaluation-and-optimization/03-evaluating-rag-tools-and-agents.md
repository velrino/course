# Evaluating RAG, Tools, and Agents

## Learning objectives

- Decompose end-to-end agent quality into independently testable layers.
- Evaluate trajectories and side effects, not only final prose.
- Diagnose failures using traces and counterfactual tests.

## Score the layer that can be fixed

An apparently wrong answer may originate in query rewriting, source coverage, chunking, retrieval, generation, routing, tool execution, state, or policy. Use layered evaluation:

1. **Retrieval:** relevant source found, rank, access filter, freshness, diversity.
2. **Response:** claim support, answer correctness, completeness, citation accuracy, abstention.
3. **Planning/routing:** appropriate agent/tool selected and unnecessary calls avoided.
4. **Tool use:** arguments valid and authorized, result handled correctly, side effect exactly once.
5. **Trajectory:** required state transitions occur within call/time/cost limits.
6. **Outcome:** the user's task is completed safely.

Do not demand one exact trajectory when several are valid. Define necessary events and forbidden events, such as "must verify customer before showing invoices," "must never call delete," and "at most one send." Use mocked tools with deterministic fixtures so agent changes can be compared without live side effects or changing APIs.

Counterfactual tests isolate causes. Provide perfect retrieved evidence to test generation; provide a gold plan to test tools; replace a tool result with an error to test recovery; remove a source to test abstention; reorder candidates to detect position sensitivity.

## Free local practice

Build a deterministic agent simulator with events like:

```json
{"type":"tool_call","name":"lookup_order","args":{"id":"A12"}}
{"type":"tool_result","status":"ok","order_status":"shipped"}
{"type":"final","status":"answered","citations":["policy:s2"]}
```

Create 20 scenarios and assertions over the event sequence. Include success, malformed tool result, timeout, access denial, stale document, conflicting source, duplicate call, and an injected instruction. Report pass rates separately for retrieval, policy, tool, trajectory, and final answer.

For five failures, run counterfactual substitutions to identify the failing layer. Add the confirmed failure and minimal regression case to the evaluation suite. Track total calls, wall time, and an estimated cost alongside quality; an agent that improves accuracy by looping indefinitely is not deployable.

## Completion criteria

- Results distinguish retrieval, response, policy, tool, trajectory, and outcome failures.
- All side-effect tests use fakes or a sandbox and assert exactly-once behavior.
- Counterfactual tests identify a root layer for at least five failures.
- Safety and resource limits are release requirements, not optional dashboard metrics.

## References

- [RAGAS metrics](https://docs.ragas.io/en/stable/concepts/metrics/) - retrieval and generation metric definitions.
- [RAGAS paper](https://arxiv.org/abs/2309.15217) - original reference-free RAG evaluation proposal.
- [LangSmith agent evaluation concepts](https://docs.langchain.com/langsmith/evaluate-complex-agent) - trajectory, single-step, and final-response evaluation patterns.
- [AgentBench paper](https://arxiv.org/abs/2308.03688) - primary research on evaluating agents across interactive environments.
