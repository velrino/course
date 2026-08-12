# Security Testing and Incident Response

## Learning objectives

- Turn AI abuse cases into repeatable security tests.
- Prepare containment, evidence preservation, communication, and recovery.
- Apply ANPD incident-communication requirements without guessing during a crisis.

## Test controls, not model politeness

Red-team inputs should exercise direct and indirect prompt injection, cross-tenant access, secret requests, encoded payloads, tool argument manipulation, path traversal, server-side request forgery, oversized files, repeated loops, output injection, and approval replay. The pass condition is deterministic: forbidden data never appears, a denied tool never executes, budgets stop the run, and an audit event is emitted. A model saying "I cannot" while a side effect occurred is a failure.

Maintain a versioned adversarial corpus. Include expected control and severity for each case. Run it when prompts, models, tools, permissions, retrievers, parsers, or policies change. Manual exploration discovers new failures; automated regression prevents their return.

An incident plan must name an incident commander, security, privacy/legal, engineering, communications, vendor contacts, and decision authority. Prepare steps to revoke keys, disable tools, isolate tenants, preserve logs and hashes, block malicious sources, restore known-good data, and validate that the threat is removed.

Under ANPD Resolution CD/ANPD No. 15/2024, when an incident may cause relevant risk or damage, the controller communicates it to ANPD and affected data subjects within three business days, subject to specific-law exceptions. The regulation and official channel govern content, staged communication, record keeping, and assessment. Do not wait for perfect certainty before activating counsel and the response team.

## Free local practice

Create `security-cases.jsonl` with at least 25 harmless cases against fake tools. Each line contains input, untrusted document, user/tenant, allowed tools, expected decision, forbidden substrings, maximum calls, and severity. Implement assertions over structured events, not only final text.

Then run a tabletop incident: a poisoned document caused attempted cross-tenant retrieval and one secret appeared in a trace. Produce a timeline and answer:

1. How is access contained now?
2. Which subjects, records, vendors, and countries may be involved?
3. What evidence is preserved, and who may access it?
4. Does the event meet the regulation's notification criteria? Escalate this decision to qualified counsel.
5. What preliminary and supplemental communications are prepared?
6. What tests prove safe restoration?

Record gaps as owners and deadlines. Repeat the tabletop after fixes.

## Completion criteria

- At least 25 adversarial cases have deterministic expected outcomes.
- Tests verify tool calls, data exposure, budgets, and audit records.
- The playbook names decision makers, containment actions, evidence sources, and recovery gates.
- The tabletop uses the current official ANPD rule and channel rather than an informal deadline summary.

## References

- [ANPD security incident communication channel and FAQ](https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/comunicado-de-incidente-de-seguranca-cis) - official criteria, three-business-day rule, and procedure.
- [ANPD regulatory index: Resolution CD/ANPD No. 15/2024](https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd) - official current-status entry for the incident regulation and its source records.
- [ANPD information-security guide for small processing agents](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/processo-guia-orientativo-sobre-seguranca-da-informacao-para-agentes-de-tratamento-de-pequeno-porte.pdf) - official practical safeguards.
- [OWASP GenAI Red Teaming Guide](https://genai.owasp.org/resource/genai-red-teaming-guide/) - structured adversarial testing for generative AI systems.
- [NIST Computer Security Incident Handling Guide](https://doi.org/10.6028/NIST.SP.800-61r2) - preparation, detection, containment, eradication, and recovery.
