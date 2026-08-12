# Webhooks, Executions, and Error Workflows

## Learning objectives

By the end of this lesson, you can:

- receive and respond to a local webhook safely;
- distinguish test and production webhook behavior;
- inspect, retain, retry, and debug executions;
- route operational failures to a separate error workflow with useful context.

## Webhooks are public contracts

A Webhook node defines an HTTP method, path, authentication option, and response mode. Treat its request as untrusted even in a local lab:

1. authenticate the sender where possible;
2. limit body size and accepted content type at the edge;
3. parse and validate a schema;
4. reserve an idempotency key;
5. respond with a status that reflects accepted responsibility;
6. perform only authorized work.

n8n presents a test URL for development and a production URL used when the workflow is active. Test listeners are temporary. Do not expose either through a tunnel unless you understand that it creates an internet-reachable endpoint.

## Response timing

Respond immediately when the caller only needs an acknowledgment and work may continue asynchronously. Respond after completion only when the operation is short and the caller needs the result. Long synchronous flows risk timeouts even if work later succeeds.

Use status codes deliberately:

- 200 for a completed synchronous result;
- 202 when valid work has been accepted for later processing;
- 400 for malformed input;
- 401/403 for missing or insufficient authorization;
- 409 for an idempotency conflict;
- 429 for an enforced rate limit;
- 5xx for a server failure the caller may retry under policy.

## Error workflows and execution evidence

An error workflow starts with Error Trigger and receives failure context from another workflow. It should notify or record a concise operational event, not blindly retry every failure. Include workflow/execution identifier, failing node, timestamp, classification, and a link or recovery instruction. Exclude secrets and body content.

Execution history helps reproduce failures, but retention creates privacy and storage risk. Configure success/error retention according to operational need and data policy.

## Free local practice

1. Create a workflow with Webhook, validation, routing, and Respond to Webhook.
2. Accept only POST JSON containing event_id and case_id.
3. Return 202 with event_id for a valid synthetic request and 400 with reason codes for invalid input.
4. From a terminal, call the test endpoint:

~~~bash
curl -i -X POST http://localhost:5678/webhook-test/course-intake \
  -H 'Content-Type: application/json' \
  -d '{"event_id":"evt-001","case_id":"case-001"}'
~~~

5. Repeat the request and define duplicate behavior without a second side effect.
6. Create a separate workflow beginning with Error Trigger. Configure the intake workflow to use it.
7. Force a controlled error after validation. Verify the error workflow captures identifiers and failing node but not the request body.
8. Inspect the execution list, retry a failed execution with original data, and explain why a manual retry is or is not safe.
9. Keep the workflow inactive after the lab unless you need the local endpoint.

## Completion criteria

You are finished when:

- valid and invalid requests return documented status codes and schemas;
- duplicate event behavior is safe;
- test and production URLs are not confused;
- the error workflow records actionable context without body data or secrets;
- a forced error is visible in execution history and reaches Error Trigger;
- manual retry safety is evaluated against side effects and idempotency;
- retention and exposure decisions are documented;
- no internet tunnel or real data is used.

## References

- [n8n documentation: Webhook node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/) - official test/production URLs, authentication, methods, and response options.
- [n8n documentation: Respond to Webhook node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.respondtowebhook/) - official response control.
- [n8n documentation: Error handling](https://docs.n8n.io/flow-logic/error-handling/) - official error workflow and Error Trigger guidance.
- [n8n documentation: All executions](https://docs.n8n.io/workflows/executions/all-executions/) - official filtering, retry, and debug behavior.
- [IETF RFC 9110](https://datatracker.ietf.org/doc/html/rfc9110) - primary HTTP method, status, safety, and idempotency semantics.
