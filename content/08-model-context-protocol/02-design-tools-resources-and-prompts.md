# Design Tools, Resources, and Prompts

## Learning objectives

By the end of this lesson, you will be able to:

- choose among tools, resources, and prompts by control and semantics;
- write narrow, typed contracts for each primitive;
- separate discovery metadata from execution authorization; and
- design errors, caching, and side effects deliberately.

## Three server primitives express different intent

| Primitive | Typical controller | Purpose | Example |
| --- | --- | --- | --- |
| Tool | model, under host policy | compute or perform an action | create a review record |
| Resource | application | provide contextual data identified by URI | read a course syllabus |
| Prompt | user | invoke a reusable interaction template | start a module review |

The control labels describe protocol interaction patterns, not unconditional authority. A host must still confirm and authorize consequential tool calls.

Use a **resource** when the primary operation is reading addressable context without meaningful side effects. Use a **tool** for computation, queries requiring arguments, or actions. Use a **prompt** to package a user-selected workflow or message template. Do not expose the same capability three ways unless distinct user experience or interoperability needs justify it.

## Design tool contracts for safe selection

A tool needs:

- a precise verb-noun name;
- a description stating when to use and when not to use it;
- full JSON Schema for arguments and, when useful, output;
- bounds, enums, formats, and required fields;
- documented side effects and idempotency;
- permission and approval policy; and
- stable, actionable error behavior.

Avoid broad tools such as `execute_shell`, `run_sql`, or `call_api`. Narrow tools give the host a smaller permission surface and give the model a clearer choice.

Discovery is not authorization. Seeing `delete_review_history` in `tools/list` does not authorize calling it for this user, target, or moment.

## Make resources traceable

Resource URIs should be stable and meaningful, with media type, human-readable name, and provenance where applicable. Templates can represent parameterized identifiers such as `course://modules/{number}`.

The 2026-07-28 revision lets list and resource-read results communicate cache lifetime and scope. Servers must not mark user-specific data as globally shareable. Freshness and access checks happen even when content is cacheable.

## Prompts are user-facing interfaces

A prompt should have a clear title, description, arguments, and resulting messages. It may guide use of resources and tools, but it should not silently perform an action. Treat prompt text supplied by a server as untrusted configuration that the host can show and constrain.

## Free local practice

Design an MCP server for study review. Classify these capabilities:

1. retrieve the title and objectives for module 6;
2. calculate a review interval from a score;
3. save a review result;
4. offer a user-selected "Review this module" template; and
5. delete all history.

For each, write a name or URI, description, typed input/output, side effects, authorization, cache policy, and error cases. Reject at least one capability or redesign it to reduce authority.

## Completion criteria

- [ ] Every capability has a justified primitive type.
- [ ] Tool names and descriptions allow a reader to distinguish intended use.
- [ ] Schemas include bounds and required fields, not only broad strings.
- [ ] Side effects, idempotency, authorization, and approval are explicit.
- [ ] Resource cache scope cannot leak user-specific data.

## References

- [Understanding MCP Servers](https://modelcontextprotocol.io/docs/learn/server-concepts) - official conceptual guide to tools, resources, prompts, control models, and combined flows.
- [MCP Python SDK: Servers](https://py.sdk.modelcontextprotocol.io/servers/) - current v2 SDK guide to tools, resources, prompts, structured output, and errors.
- [MCP Python SDK: Protocol Versions](https://py.sdk.modelcontextprotocol.io/protocol-versions/) - current explanation of supported revisions and compatibility behavior.
- [JSON Schema 2020-12](https://json-schema.org/draft/2020-12) - specification used to express complete tool input and output schemas in the current MCP revision.

## Continue

Next: [Build a Local MCP Server](03-build-a-local-mcp-server.md)
