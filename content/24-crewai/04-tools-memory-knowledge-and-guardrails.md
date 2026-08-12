# Tools, Memory, Knowledge, and Guardrails

## Learning objectives

Bound agent capabilities, distinguish memory from authoritative knowledge, and build guardrails that fail safely.

## Tools

Treat every tool as a security boundary. Use narrow schemas, allowlists, timeouts, output-size limits, and explicit error types. Validate both model-generated arguments and tool results. A web page, retrieved document, or tool response may contain instructions intended to manipulate the agent; label external content as data and do not merge it into trusted system instructions.

Run untrusted code or file transformations in an isolated environment with strict resource limits. Do not give a general shell, unrestricted filesystem, or broad database credentials to an agent when a purpose-built function will do.

## Memory and knowledge

Memory supports continuity across steps or sessions. Knowledge supplies material relevant to a task. Neither is automatically correct. Record provenance, timestamps, scope, and ownership. Define deletion and correction paths so a wrong or personal memory does not become permanent.

Use retrieval for large knowledge collections rather than copying them into every prompt. Keep authoritative records in their source systems. An embedding index is a derived representation that must be refreshed and access-filtered; it is not a new source of truth.

## Guardrails

Guardrails should check a specific property and return an actionable failure. Examples include schema validation, source coverage, allowed classification values, maximum amount, prohibited data patterns, and required approval. Place hard business rules in deterministic code. Model-based critique can supplement these checks but should not be the only control for a consequential action.

Guardrails need their own tests. Include valid inputs, boundary values, adversarial text, tool errors, and an unavailable checker. A guardrail that crashes open is worse than one that safely routes to review.

## Free local practice

Add one read-only tool, one knowledge source, and short-term state to the Flow from the previous lesson. Write a threat model for each. Implement three deterministic guardrails and inject a hostile instruction into retrieved content. Demonstrate that the content cannot expand tool permissions or skip approval.

## Completion criteria

- Each tool has least-privilege access and bounded input/output.
- Memory has provenance, retention, correction, and deletion rules.
- Knowledge access preserves source permissions.
- Guardrail failure stops or routes work safely.

## References

- [CrewAI documentation: Tools](https://docs.crewai.com/en/concepts/tools)
- [CrewAI documentation: Memory](https://docs.crewai.com/en/concepts/memory)
- [CrewAI documentation: Knowledge](https://docs.crewai.com/en/concepts/knowledge)
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)
