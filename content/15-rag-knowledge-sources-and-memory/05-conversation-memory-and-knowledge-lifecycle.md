# Conversation Memory and Knowledge Lifecycle

## Learning objectives

- Distinguish conversation state, long-term user memory, and the knowledge corpus.
- Design memory with explicit write, read, correction, expiry, and deletion rules.
- Prevent cross-user leakage and uncontrolled context growth.

## Memory is not one store

Use separate concepts even if they share infrastructure:

- **Working state** holds the current workflow position, recent tool results, and pending approvals. It is normally scoped to one thread.
- **Conversation history** preserves messages needed for continuity. Older turns may be summarized, but a summary is a lossy derived record.
- **Long-term memory** stores selected facts or preferences across threads. It requires an explicit reason to write and a way for the user to inspect and correct it.
- **Knowledge sources** are governed documents used by RAG. They have owners and versions and should not silently become user profiles.

Never let the model decide to store everything. Define a memory policy: eligible fields, purpose, legal basis where personal data is involved, namespace, confidence, provenance, retention, and deletion behavior. A useful record contains `subject_id`, `memory_type`, `value`, `source_event`, `created_at`, `expires_at`, and `supersedes`. Avoid storing secrets, authentication data, health information, or inferred sensitive traits unless the product has a legitimate, reviewed requirement.

Context windows are not durable memory. Sending the full transcript on every turn increases cost and makes old prompt injections persistent. Retrieve only the minimum relevant memory, keep system instructions separate, and treat stored user text as untrusted data.

## Free local practice

Implement a memory ledger with Python's built-in `sqlite3`. Create tables for `threads`, `events`, and `memories`. Enforce a composite namespace `(tenant_id, user_id)` and use parameterized SQL. Implement these operations:

```text
record_event(thread, role, content)
propose_memory(subject, type, value, provenance, expiry)
approve_memory(memory_id)
recall(subject, query, limit)
correct_memory(memory_id, replacement)
delete_subject(subject)
```

The `propose`/`approve` split makes writes reviewable. Correction should append a replacement and mark the old value superseded rather than rewriting history invisibly. `delete_subject` must remove messages, summaries, memories, and any corresponding vector records; test the negative result afterward.

Create two users with similar questions. Write one preference for only the first user. Verify with automated tests that the second user never recalls it. Add an expired record and ensure it is omitted. Store an instruction-like string, such as "ignore the policy," and verify that it is quoted as data rather than executed as an instruction.

## Completion criteria

- State, history, long-term memory, and knowledge are modeled separately.
- Cross-user, expiry, correction, and deletion tests pass.
- Every long-term memory has provenance and an explicit retention time or justified exception.
- A user-facing export can list what the system remembers without exposing another subject.

## References

- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) - checkpointed thread state, stores, and memory concepts.
- [LangGraph memory](https://docs.langchain.com/oss/python/langgraph/add-memory) - short- and long-term memory implementation patterns.
- [SQLite documentation](https://www.sqlite.org/docs.html) - public reference for a local durable store.
- [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) - treating external and persistent text as untrusted input.
