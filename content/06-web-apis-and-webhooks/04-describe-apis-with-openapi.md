# Describe APIs with OpenAPI

## Learning objectives

By the end of this lesson, you will be able to:

- explain what an OpenAPI Description does and does not guarantee;
- describe paths, operations, parameters, schemas, responses, and security;
- use an API contract to guide implementation and tests; and
- evolve a contract while identifying breaking changes.

## A machine-readable contract reduces guesswork

The OpenAPI Specification defines a language-agnostic description for HTTP APIs. Tools can use a description to render documentation, generate clients or server stubs, validate traffic, and create test cases.

The description is not the running service. It can be incomplete, stale, or implemented incorrectly. Test conformance in both directions: does the implementation match the contract, and does the contract describe the behavior users actually depend on?

Core objects include:

- `info` for title and API-document version;
- `servers` for base locations;
- `paths` and operation methods;
- parameters in path, query, header, or cookie;
- request-body content and schema;
- response codes, content, headers, and schemas;
- reusable `components`; and
- security schemes and per-operation requirements.

The `info.version` describes your API document or product; it is not the OpenAPI specification version in the top-level `openapi` field.

## Describe behavior, not only shapes

Document constraints and examples, but also:

- authorization and scopes;
- pagination and sorting;
- idempotency behavior;
- rate limits and retry signals;
- error formats;
- time and identifier formats;
- nullable versus omitted fields; and
- deprecation and compatibility policy.

A syntactically valid description can still leave these essential semantics ambiguous.

## Evolve deliberately

Removing a field, changing its type, making an optional field required, narrowing allowed values, or changing status behavior can break clients. Adding an optional response field is often compatible only if clients correctly ignore unknown fields.

Prefer additive evolution, publish deprecations, observe usage, and test known consumers. Version only when the compatibility cost justifies it; a path such as `/v1` does not replace a change policy.

## Free local practice

Create `openapi.json` for the ticket API:

```json
{
  "openapi": "3.1.0",
  "info": {"title": "Local Ticket API", "version": "0.1.0"},
  "servers": [{"url": "http://127.0.0.1:8080"}],
  "paths": {
    "/tickets": {
      "get": {
        "responses": {
          "200": {
            "description": "Ticket collection",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "required": ["items", "next"],
                  "properties": {
                    "items": {"type": "array", "items": {"$ref": "#/components/schemas/Ticket"}},
                    "next": {"type": ["string", "null"]}
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "Ticket": {
        "type": "object",
        "required": ["id", "status"],
        "properties": {
          "id": {"type": "integer"},
          "status": {"enum": ["open", "closed"]}
        }
      }
    }
  }
}
```

Parse it with `python3 -m json.tool openapi.json`. Compare it field by field with your running API. Add the `404` response and `/tickets/{ticket_id}` path, including a required integer path parameter.

## Completion criteria

- [ ] The description parses and includes paths, operations, schemas, and responses.
- [ ] Every implemented success and error response is documented.
- [ ] Path parameters are required and typed.
- [ ] You listed at least four behavioral rules not captured by body shape alone.
- [ ] You identified one additive and two breaking changes.

## References

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) - authoritative current specification published by the OpenAPI Initiative.
- [Learn OpenAPI](https://learn.openapis.org/) - official beginner learning material maintained by the OpenAPI Initiative.
- [JSON Schema Specification](https://json-schema.org/specification) - official schema resources used by OpenAPI 3.1 for data validation concepts.
- [Semantic Versioning 2.0.0](https://semver.org/) - public specification for communicating compatibility in version numbers; apply it only with an explicit definition of the public API.

## Continue

Next: [Receive Webhooks Reliably and Securely](05-receive-webhooks-reliably-and-securely.md)
