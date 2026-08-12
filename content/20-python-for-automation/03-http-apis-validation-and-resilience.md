# HTTP APIs, Validation, and Resilience

## Learning objectives

- Consume HTTP APIs with timeouts, authentication, pagination, and schema validation.
- Retry only safe transient failures and respect server backpressure.
- Prevent secret leakage, server-side request forgery, and silent partial results.

## The network is an unreliable trust boundary

Set connect and read timeouts explicitly; an absent timeout can hang a scheduled job indefinitely. Check status codes before parsing, validate `Content-Type` and response size, then validate the decoded schema. A successful HTTP status does not prove a valid business response.

Classify failures. Authentication/authorization errors and invalid requests need correction, not retries. Timeouts, connection resets, `429`, and some `5xx` responses may be retried with bounded exponential backoff, jitter, and respect for `Retry-After`. Retry read-only requests more freely than writes. For creation/update, use a provider-supported idempotency key or reconcile before retrying.

Pagination must detect missing/repeated cursors and stop at a maximum page/item budget. Store checkpoints only after output is durably committed. If an API returns partial data, mark the run incomplete rather than publishing it as complete.

Never log bearer tokens or full authorization headers. Keep an allowlist of schemes/hosts when URLs can be influenced by input; block local/link-local addresses and redirects to unapproved destinations. Prefer a fixed base URL over arbitrary fetch functionality.

## Free local practice

Run a local mock API using Python's `http.server` or a test fixture. Make endpoints produce: two paginated pages, delayed response, `429` with `Retry-After`, transient `503`, invalid JSON, oversized response, repeated cursor, and duplicate write.

Build an adapter with `httpx` or `urllib.request` that has explicit timeouts, maximum bytes/pages, response validation, and typed errors. Use Pydantic or a hand-written validator for external records. Implement retries with an injectable sleep function so tests do not wait in real time.

For a fake POST, generate one idempotency key per logical operation and prove retries create one server record. Capture logs and assert the fake token never appears. Configure a fixed `http://127.0.0.1:PORT` base for the exercise; separately unit-test that arbitrary user-supplied URLs are rejected.

## Completion criteria

- Every request has bounded time, bytes, pages, and retry attempts.
- Schema/content errors and permanent HTTP errors are not retried blindly.
- A repeated write remains exactly once through idempotency or reconciliation.
- Tests prove tokens are redacted and destination restrictions cannot be bypassed by redirects.

## References

- [HTTP Semantics, RFC 9110](https://www.rfc-editor.org/rfc/rfc9110) - methods, status codes, safety, and idempotency semantics.
- [HTTPX documentation](https://www.python-httpx.org/) - sync/async client, timeouts, limits, and transports.
- [Pydantic validation](https://docs.pydantic.dev/latest/concepts/validators/) - boundary validation for structured data.
- [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) - destination allowlists and network-layer defenses.
