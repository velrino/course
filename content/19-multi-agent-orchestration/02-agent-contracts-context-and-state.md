# Agent Contracts, Context, and State

## Learning objectives

- Define typed inputs, outputs, authority, budgets, and failure semantics for an agent.
- Pass minimum sufficient context without breaking message/tool invariants.
- Separate shared workflow state from private worker scratch space.

## Treat delegation as an API call

An agent contract should name purpose, accepted inputs, output schema, evidence requirements, tools, allowed resources, prohibited actions, timeout/call/token budgets, idempotency behavior, error types, and version. Descriptions drive model routing, so "helpful researcher" is weak. Prefer "find up to five primary public sources for the supplied question; return structured claims and URLs; never write files or contact people."

Use structured envelopes:

```json
{
  "task_id": "t-17",
  "objective": "verify claim",
  "inputs": {"claim": "..."},
  "constraints": {"domains": ["gov.br"], "max_sources": 5},
  "deadline": "...",
  "trace_id": "..."
}
```

The response should separate `status`, `result`, `evidence`, `warnings`, and `errors`. The coordinator must validate the schema and treat worker text as untrusted data, not new system instructions.

Context is a security and quality boundary. Pass the smallest information needed: task-specific source excerpts and stable IDs instead of an entire conversation. Summarize only with provenance because summaries can omit constraints. For tool-calling message histories, preserve the required pairing between a tool request and response; malformed histories cause errors or confusing behavior.

Use explicit state partitions: public workflow state, coordinator-only policy state, worker-local scratch state, and durable audit events. Define merge rules. Appending unique evidence records is safer than letting two parallel workers overwrite a shared `answer` field.

## Free local practice

Write JSON Schema files for a `research_worker` and `citation_checker`. Implement both as deterministic Python functions, not models. Make the worker return one valid result, one unknown field, one missing citation, one timeout, and one instruction-like string in its evidence.

Build a coordinator that validates with `jsonschema` or Pydantic, rejects incompatible versions, enforces deadlines, and stores append-only events. It must escape/quote worker evidence when constructing the next prompt. Implement a merge function that deduplicates sources by canonical URL and reports conflicts instead of selecting the last writer.

Create a context budget table showing what each component can read and why. Add a test proving the citation checker cannot access user profile data or invoke the research tool.

## Completion criteria

- Contracts define schemas, permissions, budgets, versions, and error behavior.
- Invalid, late, or instruction-bearing worker output cannot bypass coordinator policy.
- Parallel state has deterministic merge and conflict rules.
- Each agent receives only justified context and credentials.

## References

- [JSON Schema 2020-12 specification](https://json-schema.org/draft/2020-12) - public standard for interoperable structured contracts.
- [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/) - typed validation and serialization in Python.
- [LangChain handoffs](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs) - state-driven transitions and correct tool-message pairing.
- [A2A Protocol specification](https://a2a-protocol.org/latest/specification/) - agent discovery, tasks, messages, artifacts, and interoperability.
