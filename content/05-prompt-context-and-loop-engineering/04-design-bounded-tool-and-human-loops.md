# Design Bounded Tool and Human Loops

## Learning objectives

By the end of this lesson, you will be able to:

- describe an observe-decide-act loop without relying on hidden reasoning text;
- define tools with narrow contracts and side-effect metadata;
- bound retries, cost, time, and completion; and
- place human approval before consequential actions.

## The harness executes the loop

An agent loop is application logic:

```text
receive goal and policy
-> present permitted tools and relevant state
-> model proposes a response or tool call
-> validate authorization and arguments
-> execute in the environment
-> return an observation
-> update inspectable state
-> stop, escalate, or repeat
```

The language model does not execute a tool by naming it. The harness decides whether a requested call is valid and authorized, runs the implementation, and returns the result.

Operational state should be concise and inspectable: current goal, completed actions, evidence, remaining budget, last error, and next allowed transitions. Do not require private chain-of-thought as an audit log. Record tool calls, results, decisions, and concise justifications that can be reviewed.

## Make tools narrow and predictable

A tool contract should include:

- purpose and non-purpose;
- typed input schema;
- typed output and error schema;
- read-only or side-effecting status;
- idempotency behavior;
- required permission and approval;
- timeout and rate limits; and
- sensitive fields that logs must redact.

Prefer `send_draft_for_approval(draft_id)` to an unrestricted `run_sql(query)` or `shell(command)`. Capability design is a security control.

## Bound every loop

Define:

- maximum steps and wall-clock time;
- token or compute budget;
- per-tool timeout;
- which transient failures may be retried;
- exponential delay and randomness where appropriate;
- duplicate detection or idempotency keys;
- terminal success evidence; and
- escalation after repeated or ambiguous failure.

Do not retry validation, authentication, or permission failures as though they were temporary. An endlessly persistent agent can multiply cost and side effects.

## Put approval at the action boundary

Require meaningful confirmation for external messages, purchases, data deletion, privilege changes, publication, or other consequential effects. The approval view should show target, action, important parameters, expected effect, and whether reversal is possible.

A human-in-the-loop design is complete only if the reviewer can reject, edit, defer, or escalate and the system respects that choice.

## Free local practice

Design a loop for these mock tools:

```text
search_notes(query) -> read-only
save_draft(title, body, idempotency_key) -> reversible local write
publish_draft(draft_id) -> external side effect
delete_all_notes(confirm_token) -> destructive
```

Write a transition table with states `planning`, `drafting`, `awaiting_approval`, `completed`, and `failed_safely`. Include:

- invalid arguments;
- tool timeout;
- duplicated save;
- denied publication;
- request to delete notes; and
- maximum-step exhaustion.

Simulate the table on paper for one successful and two failing runs. No model or paid API is required.

## Completion criteria

- [ ] The loop separates model proposals from harness execution.
- [ ] Every tool has schema, side-effect, permission, timeout, and idempotency behavior.
- [ ] Retryable and non-retryable errors are different.
- [ ] Success requires observable evidence, not the model saying "done."
- [ ] Consequential actions show exact effects before approval.

## References

- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) - original paper on interleaving reasoning and environment actions.
- [From Model to Agent: Equipping the Responses API with a Computer Environment](https://openai.com/index/equip-responses-api-computer-environment/) - current official description of a tight propose-execute-observe agent loop and the harness's role.
- [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) - practical system controls for untrusted inputs, tool permissions, output monitoring, and human approval.
- [AWS Builders' Library: Timeouts, Retries, and Backoff with Jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) - public engineering guidance on bounded distributed-system retries.

## Continue

Next: [Build Harnesses and Evaluation Loops](05-build-harnesses-and-evaluation-loops.md)
