# Receive Webhooks Reliably and Securely

## Learning objectives

By the end of this lesson, you will be able to:

- distinguish a webhook from polling and an ordinary API call;
- verify origin using a signed raw payload;
- handle duplicates, retries, ordering, and slow work; and
- design observable recovery for missed deliveries.

## A webhook reverses who initiates notification

With polling, your application repeatedly asks a provider whether something changed. With a webhook, the provider sends an HTTP request to a receiver URL when an event occurs. The receiver is still an HTTP server and must treat the request as untrusted input.

A robust receiver follows this order:

1. enforce HTTPS in deployed environments;
2. read the raw request bytes within a size limit;
3. validate timestamp or replay window if the provider supplies one;
4. compute and compare the signature;
5. parse and validate the event schema;
6. check the event ID for prior processing;
7. persist or enqueue the accepted event;
8. return a successful response quickly; and
9. process slow business logic asynchronously.

Provider contracts differ. Use the exact signature algorithm, header, canonicalization, and retry policy in that provider's documentation.

## HMAC proves knowledge of a shared secret

A common design calculates an HMAC over the exact raw body using a secret shared by sender and receiver. The receiver independently calculates the digest and compares it with a constant-time function. Parsing and reserializing JSON before verification can change whitespace or key order and break the signature.

Do not log the secret or full sensitive payload. Rotate secrets with an overlap plan if the provider supports it.

## Delivery is commonly at least once

Assume duplicates and delayed delivery. Store a stable delivery or event ID and make processing idempotent. Events may arrive out of order, so use event versions, timestamps with caution, or fetch current state from the authoritative API when appropriate.

Do not return `2xx` before durably accepting the event, or it can be lost after a crash. Do not wait for a long workflow before acknowledging, or the sender may time out and redeliver. The boundary is durable acceptance.

## Free local practice

GitHub publishes a test secret, payload, and expected HMAC. Verify the vector locally:

```bash
python3 - <<'PY'
import hashlib
import hmac

secret = b"It's a Secret to Everybody"
payload = b"Hello, World!"
expected = "757107ea0eb2509fc211221cce984b8a37570b6d7586c22c46f4379c8b043e17"
actual = hmac.new(secret, payload, hashlib.sha256).hexdigest()
print("digest:", actual)
print("valid:", hmac.compare_digest(actual, expected))
print("tampered:", hmac.compare_digest(
    hmac.new(secret, payload + b"!", hashlib.sha256).hexdigest(), expected
))
PY
```

Then design an event table with unique `delivery_id`, received time, signature status, processing status, attempt count, and last error. Simulate receiving the same ID twice and show why only one business effect occurs.

## Completion criteria

- [ ] You explain webhook versus polling and their tradeoffs.
- [ ] You reproduced the official signature test vector and a tampered failure.
- [ ] Signature verification uses raw bytes and constant-time comparison.
- [ ] Duplicate delivery produces one business effect.
- [ ] Your design durably accepts quickly and supports replay or reconciliation.

## References

- [GitHub: Validating Webhook Deliveries](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries) - official HMAC-SHA256 procedure, constant-time comparison guidance, and public test vector used in the lab.
- [GitHub: Best Practices for Using Webhooks](https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks) - official guidance on minimal subscriptions, secrets, HTTPS, quick responses, event checks, redelivery, and unique IDs.
- [RFC 2104: HMAC](https://www.rfc-editor.org/rfc/rfc2104) - original standard construction for keyed-hash message authentication.
- [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html) - defensive guidance for HTTPS, access control, validation, content types, secrets, and audit logging.

## Continue

Next module: [Understand Images and Containers](../07-docker-and-infrastructure/01-understand-images-and-containers.md)
