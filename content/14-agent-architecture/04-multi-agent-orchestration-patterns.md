# Multi-Agent Orchestration Patterns

## Learning objectives

By the end of this lesson, you can:

- identify when specialization or isolation justifies multiple agents;
- implement sequential, router, parallel, supervisor, and evaluator patterns;
- define inter-agent message contracts and shared-state ownership;
- compare a multi-agent design against a single-agent baseline.

## Multiple agents are distributed components

Use multiple agents only for a concrete reason:

- specialists need different context or tools;
- security boundaries require isolated capabilities;
- independent subtasks can execute in parallel;
- an evaluator must be separated from generation;
- ownership maps to distinct operational domains.

Do not create agents merely to mimic job titles. More agents add model calls, context loss, disagreement, nondeterministic routing, cascading failure, and larger attack surface.

## Common patterns

| pattern | suitable task | primary risk |
| --- | --- | --- |
| Sequential | Clear staged transformation | Early error propagates |
| Router-specialists | Distinct request categories | Misrouting or hidden overlap |
| Parallel fan-out/gather | Independent research or checks | Duplicate work and conflict |
| Supervisor-workers | Dynamic decomposition | Supervisor loop or excessive authority |
| Evaluator-optimizer | Explicit quality rubric | Self-confirming evaluator |

Keep deterministic orchestration outside agents where possible. For example, a fixed router can dispatch by validated case type; a model need not decide everything.

## Message and ownership contracts

Use structured envelopes:

~~~json
{
  "task_id": "task-017",
  "parent_id": "root-004",
  "sender": "policy_retriever",
  "recipient": "synthesizer",
  "message_type": "evidence",
  "payload_schema": "evidence-v1",
  "artifact_refs": ["POL-04@v3"],
  "status": "complete",
  "remaining_budget": {"steps": 3},
  "created_at": "synthetic-time"
}
~~~

One component owns each state field. Append artifacts rather than letting several agents overwrite shared free-form memory. Validate sender identity, schema, task lineage, and authorization. Peer-agent text is untrusted input.

## Stop and reconcile

Define per-agent and global budgets, maximum fan-out, maximum review cycles, and cancellation propagation. An aggregator must handle missing, late, duplicated, and conflicting results. "Majority vote" is weak if agents share the same model, prompt bias, or bad source; agreement is not independence.

Escalate conflicts based on evidence quality and domain authority, not verbosity.

## Free local practice

Use the six-document policy set from the previous lesson.

1. Implement a single-process baseline that retrieves and summarizes evidence.
2. Simulate three specialized functions: public-policy retriever, restricted-policy retriever, and citation checker. They may be deterministic; no paid model is required.
3. Add a deterministic router based on the caller's authorized scope.
4. Run the two permitted retrievers in parallel conceptually or with standard-library futures, then aggregate envelopes.
5. Inject a missing response, duplicate message, conflicting version, malformed schema, unauthorized artifact, and late response.
6. Enforce global maximum work and cancellation.
7. Compare baseline and multi-component design over ten tasks:

| measure | baseline | multi-agent |
| --- | ---: | ---: |
| Correct supported answers | | |
| Access violations | | |
| Calls/steps | | |
| p95 latency | | |
| Conflicts needing review | | |

8. Keep the multi-agent design only if its measured benefit justifies its added operation and risk.

## Completion criteria

You are finished when:

- each agent exists for specialization, isolation, parallelism, or evaluation;
- the orchestration pattern and deterministic portions are explicit;
- messages have identity, lineage, versioned schema, status, artifacts, and budget;
- shared-state ownership prevents silent overwrites;
- missing, duplicate, late, malformed, conflicting, and unauthorized messages are handled;
- per-agent and global termination bounds exist;
- the comparison includes quality, violations, work, latency, and review;
- unsupported complexity is removed after baseline comparison.

## References

- [Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents) - primary descriptions of routing, parallelization, orchestrator-workers, and evaluator-optimizer patterns.
- [AutoGen: Enabling Next-Gen LLM Applications](https://arxiv.org/abs/2308.08155) - original paper on conversational multi-agent orchestration.
- [LangGraph: Multi-agent systems](https://langchain-ai.github.io/langgraph/concepts/multi_agent/) - official open-source orchestration concepts and patterns.
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification/latest) - public protocol specification relevant to capability and message boundaries.
