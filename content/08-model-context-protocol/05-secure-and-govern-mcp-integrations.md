# Secure and Govern MCP Integrations

## Learning objectives

By the end of this lesson, you will be able to:

- threat-model local and remote MCP trust boundaries;
- apply least privilege to servers, tools, credentials, and data;
- explain MCP authorization requirements and common anti-patterns; and
- define approval, audit, incident, and removal controls.

## Installing a server adds authority

An MCP server can expose useful capabilities and also read credentials, access files, call downstream APIs, or request side effects. Treat server installation and connection as supply-chain and permission decisions.

For a local stdio server, review:

- package source, maintainer, version, and lockfile;
- exact launch command and arguments;
- inherited environment variables;
- readable and writable filesystem paths;
- network access;
- update policy; and
- whether the host visibly identifies the supplying server for each tool.

Run with a dedicated low-privilege account or sandbox when practical. Do not mount a home directory or pass every environment variable because one tool needs one file or credential.

## Treat all descriptions and returned content as untrusted

Tool descriptions, prompts, resources, and tool results can contain malicious or compromised instructions. Hosts should retain provenance, separate data from policy, expose only relevant capabilities, validate tool arguments, and show consequential calls before execution.

A read-only tool can still leak sensitive data. A harmless-looking result can attempt prompt injection. Permissions must cover data visibility as well as side effects.

## Authorize remote servers correctly

For HTTP-based authorization, follow the current MCP authorization specification and OAuth security requirements. Important controls include:

- discover and validate protected-resource and authorization-server metadata;
- use HTTPS outside loopback development;
- bind requested tokens to the intended resource and validate audience;
- validate authorization issuer information;
- use PKCE for public clients;
- store tokens securely and keep scopes narrow;
- never log credentials; and
- obtain per-client, per-user consent where proxy behavior could create a confused deputy.

**Token passthrough is forbidden:** a server must not accept a token intended for itself and forward that token unchanged to an upstream API. Obtain and store a separate upstream credential with the correct audience.

Guard URL fetching against server-side request forgery. Validate destinations and redirects, block private and metadata networks where inappropriate, and apply egress policy.

## Govern the capability lifecycle

Maintain an inventory containing owner, server identity, transport, version, data classes, credentials, tools, scopes, users, last review, incidents, and removal steps. Log tool identity, target, authorization decision, result status, and trace ID while redacting sensitive arguments and output.

Define how to revoke a server, token, or tool; preserve investigation evidence; notify affected users; and restore state after a bad action.

## Free local practice: MCP threat model and release gate

Threat-model the study-review server with these cases:

1. a dependency update changes a tool description;
2. a resource contains an instruction to export local files;
3. a caller supplies an out-of-range score and huge string;
4. a future save tool is called twice;
5. a remote proxy receives a token for another audience;
6. an outbound URL redirects to a local metadata service; and
7. an operator needs to disable the server immediately.

For each, record asset, trust boundary, attacker or failure, preventive control, detection, response, owner, and a local test. A release passes only when high-severity cases have tested controls and a rollback or disable path.

## Completion criteria

- [ ] The inventory covers code, command, data, credentials, tools, scopes, and owner.
- [ ] Local execution is limited by account, environment, filesystem, and network policy.
- [ ] Remote tokens are validated for issuer and intended audience and are never passed through.
- [ ] Consequential tools require visible target-specific approval and idempotency controls.
- [ ] Every high-severity threat has prevention, detection, response, and a tested disable path.

## References

- [MCP Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices) - official threat analysis for confused deputies, token passthrough, SSRF, scope minimization, and other MCP-specific risks.
- [Understanding Authorization in MCP](https://modelcontextprotocol.io/docs/tutorials/security/authorization) - official conceptual walkthrough of protected resources, authorization servers, tokens, audiences, and consent.
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) - normative current authorization requirements for HTTP-based transports.
- [OAuth 2.0 Security Best Current Practice](https://www.rfc-editor.org/rfc/rfc9700) - IETF security requirements and attack mitigations underlying modern OAuth deployments.
- [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) - practical defense in depth for untrusted content, tool calls, least privilege, monitoring, and human approval.

## Continue

You completed the foundational sequence. Continue by applying these controls to workflow automation, retrieval, monitoring, and multi-agent modules.
