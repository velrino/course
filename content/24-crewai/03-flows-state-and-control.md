# Flows, State, and Control

## Learning objectives

Model event-driven execution, constrain routes, and make state transitions recoverable and auditable.

## Flow design

A Flow coordinates methods through start events, listeners, routers, and shared state. Draw the state machine before writing decorators. Each state should have a clear entry condition, allowed next states, timeout, and terminal outcome.

Use typed state for values that cross steps. Do not use it as an unbounded scratchpad. Store identifiers instead of large records, redact sensitive inputs, and distinguish facts supplied by a user from values inferred by a model.

A router should return a small, documented set of route names. Validate model output before routing, and always define a fallback for unknown, missing, or low-confidence decisions. Limit cycles with a counter or deadline.

## Reliability boundaries

Listeners may cause external side effects. Make them idempotent and write an audit event containing the operation key, actor, target, result, and correlation identifier. A state transition is not proof that an external action succeeded. Represent uncertain outcomes and reconcile them with the external system.

Persistence helps resume work but also persists mistakes and sensitive data. Define retention, deletion, and migration behavior before storing long-running state. Test what happens when code changes while old executions remain resumable.

## Free local practice

Build a Flow with these states: `received`, `validated`, `researched`, `review_required`, `approved`, `rejected`, and `completed`. Use deterministic functions first. Add a retryable simulated research failure, an expiring review, and an idempotent local write.

Create a transition table and tests proving that no route reaches `completed` from an invalid or unapproved state. Restart the process halfway through and confirm that resumption does not repeat the side effect.

## Completion criteria

- State and route names form an explicit finite-state model.
- Every loop is bounded and every router has a safe fallback.
- External actions are idempotent and separately confirmed.
- Resume, expiry, and version-change behavior is tested.

## References

- [CrewAI documentation: Flows](https://docs.crewai.com/en/concepts/flows)
- [CrewAI documentation](https://docs.crewai.com/)
- [HTTP Semantics: Idempotent Methods](https://www.rfc-editor.org/rfc/rfc9110.html#name-idempotent-methods)
