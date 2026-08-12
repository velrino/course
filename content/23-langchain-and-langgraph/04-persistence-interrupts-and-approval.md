# Persistence, Interrupts, and Approval

## Learning objectives

Design resumable execution, place approval before side effects, and prevent retries from duplicating external actions.

## Checkpoints and threads

A long-running workflow cannot depend only on process memory. A checkpointer stores graph state at execution boundaries. A thread identifier associates later invocations with the correct state history. Treat that identifier as access-controlled application data; guessing another user's thread must not expose their state.

Persistence enables recovery and inspection, but it also creates retention obligations. Decide which fields are stored, encrypted, redacted, expired, and available to support personnel. Avoid persisting secrets or raw personal data merely because the graph state accepts them.

## Interrupt before action

An interrupt pauses execution and returns information the application can present to a reviewer. The review record should show:

- the proposed action and exact target;
- the evidence used;
- important uncertainty and policy checks;
- what data will leave the system;
- approve, edit, reject, and expire options.

Place the interrupt before the first irreversible side effect. After resumption, re-check authorization and mutable facts. Approval from yesterday may not authorize a changed bank account, recipient, or document.

## Idempotency and replay

Durable runtimes may replay a node after interruption or failure. A node that sends an email, creates a ticket, or charges a card must tolerate repetition. Generate a stable operation key, store the result atomically, and return the prior result when the same key is seen again. Separate pure computation from side effects so replay boundaries are obvious.

Do not assume that a checkpoint and an external API call form one transaction. Model intermediate states such as `action_prepared`, `action_started`, and `action_confirmed`, then reconcile ambiguous outcomes.

## Free local practice

Extend the prior graph with a review interrupt. Store only a synthetic request. Simulate a crash immediately before and immediately after the external action. Resume both executions and demonstrate that the action occurs at most once. Add approval expiry and a changed-target check.

## Completion criteria

- Approval occurs before the side effect and displays the exact action.
- Resumption revalidates identity, authorization, and mutable facts.
- Duplicate execution is prevented with an idempotency strategy.
- State retention and deletion rules are documented.

## References

- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- [LangGraph durable execution](https://docs.langchain.com/oss/python/langgraph/durable-execution)
- [HTTP Semantics: Idempotent Methods](https://www.rfc-editor.org/rfc/rfc9110.html#name-idempotent-methods)
