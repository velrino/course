# Design and Consume REST APIs

## Learning objectives

By the end of this lesson, you will be able to:

- model resource-oriented URLs and representations;
- consume JSON while handling authentication, errors, pagination, and limits;
- design stable error and idempotency behavior; and
- separate authentication from object-level authorization.

## REST is an architectural style

REST describes constraints such as client-server separation, stateless interactions, cacheability, a uniform interface, layered systems, and optional downloaded code. Many "REST APIs" are HTTP JSON APIs that apply these constraints to different degrees.

Resource-oriented design names things, not operations:

```text
GET    /tickets?status=open
POST   /tickets
GET    /tickets/42
PATCH  /tickets/42
DELETE /tickets/42
```

The request and response bodies are representations of resource state, not the resource itself. Use consistent identifiers and document whether clients or servers assign them.

## A client must handle more than `200`

A robust consumer handles:

- connection and TLS errors;
- timeouts;
- expected success codes and body schemas;
- empty bodies;
- structured application errors;
- authentication and authorization failures;
- rate limiting, often `429` plus retry guidance;
- pagination cursors or links;
- partial and stale data; and
- version or compatibility changes.

Use timeouts. Retry only appropriate failures, with bounds. Preserve an idempotency key when an API supports safe retry of a creation request.

## Authentication does not answer "which object?"

A bearer token proves possession and may identify a principal and scopes. The server must still verify access to the specific object on every request. `/accounts/42` must not become readable merely because the caller changes `41` to `42`. Broken object-level authorization is a major API risk.

Never put credentials in a query string. Query values are likely to appear in history and logs. Use the documented authorization header over HTTPS and protect the token at rest.

## Design errors as data

Return a stable machine-readable structure with a human message and correlation identifier:

```json
{
  "type": "https://example.test/problems/invalid-status",
  "title": "Invalid ticket status",
  "status": 422,
  "detail": "status must be open, pending, or closed",
  "instance": "/tickets/42",
  "request_id": "req_abc123"
}
```

Do not expose stack traces, SQL, filesystem paths, credentials, or internal service topology.

## Free local practice

Create a tiny read-only API as `api.py`:

```python
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

TICKETS = [{"id": 1, "status": "open"}, {"id": 2, "status": "closed"}]

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/tickets":
            body, status = json.dumps({"items": TICKETS, "next": None}).encode(), 200
        else:
            body, status = json.dumps({"title": "Not found", "status": 404}).encode(), 404
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

HTTPServer(("127.0.0.1", 8080), Handler).serve_forever()
```

Run `python3 api.py`, then inspect both paths with `curl -i`. Extend it with `GET /tickets/1`, returning `200`, while `/tickets/99` returns `404`. Do not add mutation or authentication yet.

## Completion criteria

- [ ] Your URLs identify resources and use method semantics consistently.
- [ ] The client checks status and content type before parsing JSON.
- [ ] Pagination and rate-limit behavior are documented.
- [ ] Object authorization is checked separately from token validity.
- [ ] Error responses are useful without leaking internal implementation details.

## References

- [Architectural Styles and the Design of Network-based Software Architectures](https://ics.uci.edu/~fielding/pubs/dissertation/top.htm) - Roy Fielding's original dissertation defining REST.
- [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457) - standard reusable format for machine-readable HTTP API errors.
- [OWASP API Security Top 10 - 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) - public list and explanations of major API security risks.
- [GitHub REST API Best Practices](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api) - concrete official guidance on authentication, rate limits, conditional requests, errors, and serial mutations.

## Continue

Next: [Describe APIs with OpenAPI](04-describe-apis-with-openapi.md)
