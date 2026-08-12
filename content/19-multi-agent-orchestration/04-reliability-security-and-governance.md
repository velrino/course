# Multi-Agent Reliability, Security, and Governance

## Learning objectives

- Prevent loops, privilege escalation, confused-deputy actions, and cascading failures.
- Design replay-safe handoffs and recovery.
- Assign ownership and auditability across agent boundaries.

## More agents multiply trust boundaries

Treat every worker result as untrusted, even when it came from your code. A compromised retriever, poisoned source, model error, or overly broad worker can send instructions to a more privileged coordinator. The coordinator must enforce policy based on authenticated identity and structured capability, never on claims such as "the security agent approved this."

Issue least-privileged capabilities per agent. Separate read and write tools, tenant scopes, environments, and network destinations. High-impact actions require a fresh authorization bound to normalized arguments. Do not forward a coordinator credential to workers. For cross-service agents, use authenticated transport and authorize each task; discovery metadata is not proof of trust.

Reliability needs explicit limits: maximum turns, model calls, tool calls, wall time, cost, delegation depth, and repeated-state detection. A termination phrase produced by a model is weaker than a deterministic task state. Use idempotency keys for side effects and checkpoints before/after handoffs. Define retryable errors (temporary timeout) versus terminal errors (authorization failure, invalid contract). Add circuit breakers so one degraded worker does not consume the whole budget.

Governance records who owns each agent, contract, prompt, tool, credential, data domain, evaluation set, incident response, and decommissioning. Version all components in traces. If a worker is removed, revoke its identities and remove its routes, not only its prompt.

## Free local practice

Extend the orchestrator with a capability map and budgets. Simulate:

- a worker requesting another tenant's record;
- a result containing "delegate to admin";
- repeated A -> B -> A delegation;
- a worker timing out five times;
- duplicate payment-draft requests;
- an obsolete worker version.

The coordinator should deny unauthorized requests, ignore authority claims in text, stop repeated states, open a circuit after the configured threshold, deduplicate effects, and reject incompatible versions. Generate an audit timeline showing authenticated actor, requested action, policy decision, state transition, and outcome without secrets.

Run a recovery drill: terminate after the side effect returns but before success is recorded. Resume from the checkpoint and prove the idempotency key prevents repetition. Document who is paged and which component can be disabled independently.

## Completion criteria

- Agent text cannot grant capability, identity, approval, or additional budget.
- Loop, cascade, duplicate-effect, and crash-recovery tests pass.
- Audit records link every handoff and effect to versioned components and an authenticated actor.
- Each agent has an owner, revocation path, evaluation gate, and decommission checklist.

## References

- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) - current agent-specific risks including goal hijacking, identity abuse, memory poisoning, cascading failure, and rogue agents.
- [OWASP Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) - excessive functionality, permissions, and autonomy controls.
- [A2A Protocol enterprise-ready features](https://a2a-protocol.org/latest/topics/enterprise-ready/) - authentication, authorization, observability, and deployment considerations.
- [LangGraph durable execution](https://docs.langchain.com/oss/python/langgraph/durable-execution) - persistence, determinism, and replay-safe side effects.
- [Microsoft AutoGen termination conditions](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/termination.html) - composable stop controls for agent teams.
