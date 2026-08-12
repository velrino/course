# Capstone: Stateful Agent With Human Approval

## Objective

Build a stateful agent that can prepare an action but cannot execute the simulated action until a human reviews exact arguments and evidence.

## Scenario

A fictional procurement assistant reads a synthetic request, checks a local policy, retrieves catalog options, and prepares a draft purchase request. Requests above a threshold, with missing evidence, or outside policy go to review or rejection. The final action writes to a local fake procurement API.

## Required architecture

- Typed state with explicit status transitions.
- Separate model interpretation, deterministic policy, and tool execution.
- Read-only catalog and policy tools.
- Write tool with narrow schema, authorization check, operation key, and local target.
- Human approval showing supplier, item, amount, evidence, and changed facts.
- Persistent checkpoint and resume path.
- Bounded retries, timeout, cancellation, and kill switch.

Implement deterministic mode first. An optional LangGraph or CrewAI implementation may reuse the same domain functions and evaluation cases.

## Evaluation

Create at least 50 cases including valid requests, threshold boundaries, missing policy, changed price after approval, unauthorized user, duplicate resume, prompt injection, tool timeout, ambiguous tool result, and expired approval. Measure correct terminal state, unsafe-action rate, review coverage, duplicate actions, recovery, and latency.

Run crash tests immediately before and after the fake write. Prove at-most-once effect or document the reconciliation strategy for ambiguous outcomes.

## Deliverables

- State and sequence diagrams.
- Domain functions, graph or Flow, and local fake APIs.
- Approval interface and audit event schema.
- Evaluation suite and fault-injection results.
- Threat model, system card, runbook, and rollback demonstration.

## Completion criteria

- No consequential path bypasses code-enforced policy and approval.
- Approval is invalidated when material facts change.
- Resume and retry do not duplicate the action.
- The model can be removed without breaking control flow.

## References

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [CrewAI documentation](https://docs.crewai.com/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
