# Capstone: n8n Operations Automation

## Objective

Build a reliable workflow that receives synthetic service requests, validates them, enriches them from a local source, routes exceptions, and records an auditable result.

## Scenario

A fictional facilities team receives requests through a webhook. Routine requests with complete fields can be categorized and written to a local test database. Missing, duplicated, high-cost, or safety-related requests must enter a human review queue. No real message or work order is sent.

## Required workflow

1. Receive a webhook with a correlation identifier.
2. Authenticate the request with a test secret.
3. Validate a JSON schema and reject extra sensitive fields.
4. Detect duplicate delivery using an idempotency key.
5. Enrich the request from a local CSV or database.
6. Route through deterministic rules.
7. Optionally use a model only to propose a category from an allowlist.
8. Require approval for exceptions.
9. Store status and a minimal audit event.
10. Return a bounded response without internal error details.

## Evaluation

Create at least 40 requests covering valid categories, schema errors, duplicate webhooks, invalid authentication, high cost, safety keywords, prompt injection, database timeout, unavailable optional model, and retry after partial failure. Prove that duplicates create one record and that model failure falls back to rules or review.

Measure correct routing, duplicate side effects, review recall for high-risk cases, response time, and recovery success. Compare the optional model with the deterministic classifier.

## Deliverables

- Exported n8n workflow with credentials removed.
- Docker or documented local setup.
- Input schema, sample requests, and replay script.
- Evaluation results and error analysis.
- Data-flow diagram, threat model, runbook, and cleanup procedure.

## Completion criteria

- Replayed webhook delivery is idempotent.
- Invalid and high-risk inputs never take the automatic path.
- Secrets and personal data are absent from the export and logs.
- A fresh environment can reproduce the workflow.

## References

- [n8n documentation](https://docs.n8n.io/)
- [n8n Docker installation](https://docs.n8n.io/hosting/installation/docker/)
- [JSON Schema](https://json-schema.org/learn/getting-started-step-by-step)
- [HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html)
