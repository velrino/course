# Vendors, International Transfers, and Data Security

## Learning objectives

- Evaluate model/API vendors as part of the processing chain.
- Identify and document international personal-data transfers.
- Implement secrets, access, retention, and supply-chain controls.

## Follow data beyond your application

A hosted model may receive prompts, files, retrieved context, identifiers, and telemetry. Before integration, determine which legal entity receives data, countries and subprocessors involved, purposes, retention, training/default reuse, deletion capability, security measures, incident duties, audit evidence, and contract precedence. Test actual API behavior and configuration; a marketing privacy page is not a technical control.

ANPD Resolution CD/ANPD No. 19/2024 regulates international transfers and provides mechanisms including adequacy decisions, standard contractual clauses, specific clauses subject to approval, and global corporate rules, while other Article 33 mechanisms may apply. A transfer still needs an Article 7 or 11 legal hypothesis, a legitimate and informed purpose, and necessity. Determine the valid mechanism with counsel; do not infer compliance from encryption or a vendor's global reputation.

Apply baseline technical controls:

- store credentials in a secret manager or protected environment, never source code or prompts;
- use separate identities per environment with minimum scopes and rotation;
- encrypt transport and storage, but also minimize plaintext exposure at runtime;
- restrict egress to approved endpoints and validate TLS;
- pin and scan dependencies and model artifacts; record hashes and licenses;
- define deletion and export procedures across provider, cache, vector store, logs, and backups;
- monitor privileged access without logging secret values or full personal content.

Local processing can reduce transfers but does not eliminate LGPD duties or security risk.

## Free local practice

Create a vendor assessment for one hypothetical hosted LLM and one local open-weight model. Do not create accounts. Use public terms and documentation and mark every unanswered question as a risk, not an assumed "yes." Compare data location, retention, training use, deletion, subprocessors, authentication, incident notification, model license, update channel, and operational cost.

Make a transfer map from user to application, model provider, observability provider, backups, and support. For each arrow record data fields, origin/destination country, purpose, legal hypothesis and transfer mechanism to be confirmed, encryption, retention, and owner.

Run `pip-audit` on a disposable Python project and generate a CycloneDX software bill of materials with `cyclonedx-py`. Replace a hard-coded fake token with an environment variable, add secret scanning with `gitleaks` or a pre-commit hook, and document a credential-revocation drill.

## Completion criteria

- Vendor unknowns are visible and assigned, not silently treated as compliant.
- Every international flow has a purpose, data scope, destination, and mechanism pending or confirmed.
- Secrets are absent from source, logs, prompts, and test fixtures.
- Dependencies/model artifacts have provenance, hashes, licensing notes, and an update response plan.

## References

- [ANPD Resolution CD/ANPD No. 19/2024](https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/resolucao-cd-anpd-no-19-de-23-de-agosto-de-2024) - official international-transfer regulation and standard clauses.
- [ANPD international data transfers portal](https://www.gov.br/anpd/pt-br/assuntos/assuntos-internacionais/transferencia-internacional-de-dados) - current official guidance and FAQs.
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) - credential lifecycle and operational controls.
- [Python Packaging advisory database](https://github.com/pypa/advisory-database) - public vulnerability data used by Python auditing tools.
- [SLSA provenance specification](https://slsa.dev/spec/v1.0/provenance) - artifact build and source provenance model.
