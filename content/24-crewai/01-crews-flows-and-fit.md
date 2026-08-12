# Crews, Flows, and Architectural Fit

## Learning objectives

Explain CrewAI's two main orchestration styles, choose the least autonomous design that satisfies a task, and identify costs hidden by role-based metaphors.

## Two orchestration styles

A **Crew** coordinates agents with roles, goals, tools, and assigned tasks. It is useful when a problem benefits from open-ended delegation or specialized perspectives. A **Flow** expresses event-driven control, state, routing, and explicit steps. It is a better default when execution order, auditability, and failure behavior must be predictable.

A hybrid can place a Crew inside one bounded Flow step. The Flow owns validation, authorization, approval, and side effects; the Crew handles a narrow exploratory task and returns a validated result. This prevents a role metaphor from becoming an authorization model.

## Do you need multiple agents?

Multiple role prompts do not automatically create independent expertise. Agents may use the same model, share the same blind spots, amplify an early error, and consume more tokens and time. Before using a Crew, compare it with:

- one model call with a structured checklist;
- a deterministic pipeline;
- one agent with several tools;
- independent parallel samples followed by a deterministic aggregator;
- a human specialist at the uncertain step.

Choose multiple agents only when task decomposition is real, information or tools differ by role, outputs can be checked at boundaries, and the added coordination has a measurable benefit.

## Decision record

For each proposed agent, document its input, output schema, tools, data access, stopping condition, failure route, and why an ordinary function cannot do the work. For each handoff, document what evidence crosses the boundary and how the receiver validates it.

CrewAI is a framework, not a substitute for permissions, transactions, data governance, or monitoring. Keep those controls outside model discretion.

## Free local practice

Take one workflow from module 19. Design it three ways: a single deterministic Flow, a single agent inside a Flow, and a Crew inside a Flow. Estimate model calls, tool calls, failure points, and review effort for ten runs. Select one architecture and state what evaluation result would justify moving to a more complex option.

## Completion criteria

- You can distinguish a Crew from a Flow without relying on analogy.
- Every proposed agent has a non-agent baseline.
- Deterministic controls own consequential actions.
- Complexity is justified by a measurable hypothesis.

## References

- [CrewAI documentation](https://docs.crewai.com/)
- [CrewAI source repository](https://github.com/crewAIInc/crewAI)
- [LangChain: Frameworks, runtimes, and harnesses](https://docs.langchain.com/oss/python/concepts/products)
