# 13. Advanced n8n and Integrations

Integrate authenticated and paginated APIs, define reusable subworkflow contracts, and engineer resilience against rate limits, duplicates, partial failure, and restarts. Self-hosting, secrets, backup, monitoring, scaling, and release practice complete the operational path.

## Before you begin

Complete [Module 12](../12-n8n-fundamentals/index.md) and retain an exported working workflow. Review the HTTP and webhook contracts in [Module 06](../06-web-apis-and-webhooks/index.md).

## Lessons

1. [HTTP APIs, Authentication, and Pagination](01-http-apis-authentication-and-pagination.md)
2. [Subworkflows, Reuse, and Contracts](02-subworkflows-reuse-and-contracts.md)
3. [Resilience, Rate Limits, and Idempotency](03-resilience-rate-limits-and-idempotency.md)
4. [Self-Hosting, Security, and Secrets](04-self-hosting-security-and-secrets.md)
5. [Scaling, Monitoring, and Release Operations](05-scaling-monitoring-and-release-operations.md)

## Suggested artifact

Deliver a versioned n8n integration with credential boundaries, pagination, a typed subworkflow, rate-limit handling, idempotent writes, an error budget, health and backup checks, and a tested rollback runbook.

## Practice lab

[n8n Order Triage](https://github.com/velrino/course/tree/master/labs/n8n-order-triage) can be extended with subworkflows, failure routing, and operational controls from this module.

## Continue

Use the workflow baseline to decide where autonomy is justified in [Module 14: Agent Architecture](../14-agent-architecture/index.md).
