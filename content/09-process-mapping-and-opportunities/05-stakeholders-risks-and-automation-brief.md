# Stakeholders, Risks, and the Automation Brief

## Learning objectives

By the end of this lesson, you can:

- identify decision owners, operators, affected people, and control functions;
- document risk as a scenario with causes, consequences, and controls;
- assign authority for launch, review, incident response, and shutdown;
- consolidate discovery evidence into an implementable automation brief.

## Stakeholders are not just approvers

Map people by their relationship to the process:

- **Recipient:** needs the outcome.
- **Affected person:** may experience a benefit or harm without operating the system.
- **Operator:** handles normal work.
- **Exception reviewer:** decides cases outside rules.
- **Process owner:** accountable for the service outcome.
- **System/data owner:** controls access and integrity.
- **Control functions:** privacy, security, legal, accessibility, audit, or worker representatives as appropriate.
- **Builder and support owner:** change and maintain the automation.

For each important decision, name exactly one accountable owner. "The team" cannot authorize a risky release or respond to an incident.

## Write risks as scenarios

Avoid labels such as "privacy risk." Use a causal statement:

> Because inbound files may contain unnecessary personal data, the workflow could copy it into execution logs, causing unauthorized retention and exposure.

Then record:

| field | purpose |
| --- | --- |
| Cause and event | What could make the scenario occur |
| Affected parties | Who bears the consequence |
| Likelihood and impact | Before controls |
| Preventive control | Reduces probability |
| Detective control | Reveals occurrence |
| Corrective control | Limits consequence and restores service |
| Owner and evidence | Who verifies the control |
| Residual risk | What remains after controls |

Useful controls include data minimization, allowlisted actions, schema validation, least-privilege credentials, human approval, immutable audit records, rate limits, rollback, and a kill switch. A policy sentence is not a control unless someone can test whether it works.

## The automation brief

Create one concise brief:

1. Problem, affected users, and current-state evidence.
2. In-scope trigger, unit of work, end states, and exclusions.
3. Proposed change and why eliminate/simplify options were insufficient.
4. Inputs, outputs, systems, permissions, and data classification.
5. Normal flow, exceptions, human decisions, and rollback.
6. Baseline, target, guardrails, and pilot decision rule.
7. Top risks, controls, owners, and residual-risk acceptance.
8. Open questions, dependencies, estimated effort, and expiry/review date.

The brief is a decision record, not a sales document. Record contrary evidence and assumptions explicitly.

## Free local practice

Use your selected low-risk process.

1. Build a stakeholder table with role, interest, impact, decision authority, consultation point, and contact channel. Use fictional roles if working alone.
2. Run a lightweight pre-mortem: imagine the pilot caused a serious failure. Write five plausible paths to that outcome.
3. Convert each into a risk scenario and design at least one preventive and one detective control.
4. Create a decision-rights table:

| decision | accountable | consulted | evidence required |
| --- | --- | --- | --- |
| Start shadow pilot | Process owner | Operator, data owner | Test report, data review |
| Enable writes | Process owner | Security, support | Guardrails passed |
| Stop automation | On-call operator | Process owner | Guardrail breach |

5. Assemble the automation brief and give it to another person. Ask them to state what the system may do, must never do, and who stops it. Fix any ambiguity.

## Completion criteria

You are finished when:

- affected people and frontline operators are represented, not only sponsors;
- every consequential decision has one accountable owner;
- at least five risks use cause-event-consequence language;
- controls are testable and include preventive, detective, and corrective coverage;
- residual risks and acceptance owners are explicit;
- the brief links scope, evidence, metrics, guardrails, rollback, and support;
- an independent reader can identify allowed actions and stop authority.

## References

- [NIST AI RMF 1.0](https://doi.org/10.6028/NIST.AI.100-1) - primary lifecycle framework for affected parties, accountability, governance, measurement, and risk treatment.
- [NIST AI RMF Playbook](https://airc.nist.gov/airmf-resources/playbook/) - public actions and documentation practices mapped to Govern, Map, Measure, and Manage.
- [OECD: Advancing accountability in AI](https://oecd.ai/en/accountability/) - guidance on assigning accountability and managing risk through the system lifecycle.
- [GOV.UK Service Manual: Map and understand a user's whole problem](https://www.gov.uk/service-manual/design/map-a-users-whole-problem) - public guidance for cross-organizational stakeholders and service ownership.
