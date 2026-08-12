# Self-Hosting, Security, and Secrets

## Learning objectives

By the end of this lesson, you can:

- define a production-oriented n8n deployment boundary;
- protect encryption keys, credentials, endpoints, and administrative access;
- reduce the capability exposed by risky or community nodes;
- perform and review a backup, restore, and security audit.

## Self-hosting is an operational commitment

A production design needs:

- a supported pinned n8n version;
- persistent database and encryption key;
- TLS termination and a correct public base/webhook URL;
- restricted network exposure;
- named instance, database, backup, and incident owners;
- monitoring, retention, patching, and restore tests.

SQLite is convenient for a single-process local lab. PostgreSQL is the normal choice when moving toward queue mode or stronger operational database management. Do not copy a live database while it is changing and call that a tested backup.

## Secrets and least privilege

n8n encrypts stored credentials using its encryption key. Protect and back up that key separately; losing it can make credentials unusable, while exposing it with the database undermines their confidentiality.

Use:

- distinct credentials per environment and integration;
- minimum scopes and read-only access until writes are required;
- short rotation and revocation procedures;
- environment or supported secret-provider configuration;
- workflow access limited to people who need it;
- redaction and conservative execution-data retention.

Never commit .env files, exported credentials, database dumps, or live workflow samples. Workflow JSON may reveal URLs, business rules, table names, and credential references even when secret values are absent.

## Reduce executable capability

Code, Execute Command, file access, SSH, and unreviewed community nodes can expand the attack surface. Block nodes that the use cases do not need. Treat a community node as third-party code running with the instance's access: review source, maintenance, permissions, version, and update path.

Protect webhooks with authentication, input validation, body/rate limits at a reverse proxy, and network allowlists where feasible. Apply SSRF protections so user-controlled URLs cannot make the workflow probe internal services.

## Free local practice

Perform this only on the synthetic local instance.

1. Draw a data-flow diagram for browser, reverse proxy, n8n, database, external API, backup, and operator.
2. Mark trust boundaries, stored secrets, inbound ports, and outbound destinations.
3. Generate a new lab encryption key and store it outside the workflow directory; do not print it in notes.
4. Create separate read-only and fictional write credentials. Verify the first cannot perform the mock write.
5. Review the official environment variables for blocking unused nodes, securing cookies, webhook URLs, telemetry choice, and execution retention. Apply only settings you understand.
6. Run the n8n security audit using the documented CLI or API method and record findings, evidence, owner, and disposition.
7. Back up the volume/database, encryption key, and workflow exports. Restore into a separate local instance and run a synthetic smoke test.
8. Write rotation, patch, compromise, and shutdown steps. Include how to revoke external credentials first.

## Completion criteria

You are finished when:

- the deployment diagram shows trust and data boundaries;
- version, database, encryption key, TLS, URL, and ownership decisions are recorded;
- credentials are environment-specific and least-privilege;
- dangerous unused nodes and unreviewed community code are addressed;
- webhook authentication, validation, rate/body limits, and SSRF are considered;
- a security audit has dispositions rather than only output;
- backup restoration succeeds on a separate local instance;
- compromise and secret-rotation steps are executable.

## References

- [n8n documentation: Security overview](https://docs.n8n.io/hosting/securing/overview/) - official self-hosted hardening entry point.
- [n8n documentation: Security audit](https://docs.n8n.io/hosting/securing/security-audit/) - official CLI, API, and node audit methods and report categories.
- [n8n documentation: Environment variables](https://docs.n8n.io/hosting/configuration/environment-variables/) - official deployment, credential, database, endpoint, security, and retention settings.
- [n8n documentation: Blocking nodes](https://docs.n8n.io/hosting/securing/blocking-nodes/) - official control for disabling unnecessary high-risk capability.
- [OWASP API Security Top 10, 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) - public threat categories for exposed automation APIs.
