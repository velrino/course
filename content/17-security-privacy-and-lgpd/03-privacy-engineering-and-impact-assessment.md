# Privacy Engineering and Impact Assessment

## Learning objectives

- Translate purpose limitation and necessity into system controls.
- Build a data inventory and lifecycle deletion plan.
- Draft a risk-based Relatorio de Impacto a Protecao de Dados Pessoais (RIPD).

## Make privacy behavior executable

Start with a data-flow inventory, not a privacy notice. Record collection point, purpose, data subject, categories, source, recipients, storage locations, access roles, legal hypothesis, retention trigger, deletion job, international flow, and system owner. Include prompts, retrieved passages, model responses, feedback, embeddings, backups, support tickets, and observability traces. Logs are a frequent unplanned copy of personal data.

Minimize at several layers. Do not collect an unnecessary field; redact before sending to a model; retrieve only records authorized for the current user; keep raw content out of telemetry; limit long-term memory; expire derived vectors when the source expires; and segregate tenants. Encryption does not make excessive collection necessary.

A RIPD documents processing that may generate high risk to principles, civil liberties, and fundamental rights. ANPD guidance recommends preparing it before processing begins when possible and reviewing it when purposes, technology, risk, or controls change. Under Article 38, minimum content includes data types, processing/security methodology, and the controller's analysis of safeguards and risk mitigation. A useful engineering version also describes necessity/proportionality, affected people, threat scenarios, likelihood/impact, residual risk, owners, evidence, consultation, and approval.

## Free local practice

Use the fictional AI workflow from the previous lesson. Create `data-inventory.csv` and a lifecycle diagram. For every store, implement or specify:

```text
retention trigger -> scheduled deletion -> backups/replicas -> vector deletion
-> verification query -> audit event -> exception process
```

Draft a concise RIPD in Markdown with: scope, roles, purposes, data flows, necessity, legal hypotheses for validation, affected groups, risks, controls, residual risks, and review date. Add at least eight privacy harms, not only data breaches: unfair exclusion, chilling effects, unwanted inference, inability to correct data, exposure to another tenant, excessive retention, secondary use, and opaque automated decisions.

Run two tests. First, submit a synthetic access request and trace all copies that must appear in the response. Second, delete that synthetic subject and verify absence from primary store, memory, vector index, cache, and scheduled backup-expiry record. Never use real personal data for the exercise.

## Completion criteria

- The inventory includes derived data, logs, embeddings, backups, and vendors.
- Every store has a retention trigger, deletion mechanism, and verification evidence.
- The RIPD distinguishes inherent risk, controls, and residual risk with owners.
- Access and deletion tabletop tests find every synthetic record or explain a lawful exception.

## References

- [ANPD RIPD questions and answers](https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/relatorio-de-impacto-a-protecao-de-dados-pessoais-ripd) - official scope, timing, responsibility, and minimum content guidance.
- [NIST Privacy Framework 1.0](https://www.nist.gov/privacy-framework/privacy-framework) - free framework for identifying and managing privacy risk.
- [NIST Privacy Risk Assessment Methodology](https://www.nist.gov/privacy-framework/nist-pram) - worksheets for data actions, problematic data actions, and controls.
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) - useful logging with exclusions and protection for sensitive fields.
