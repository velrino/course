# Transparency, Audit, and Documentation

## Learning objectives

Create documentation for users, operators, reviewers, and affected people; design traceability without excessive surveillance.

## Transparency for a purpose

Different audiences need different information. A user needs to know they are interacting with AI, what it can and cannot do, how data is used, and how to obtain help. An operator needs runbooks, thresholds, dependencies, and rollback procedures. A reviewer needs versioned evidence. A person affected by a decision needs a meaningful explanation and a way to challenge or correct it.

Do not expose secrets or security-sensitive internals in the name of transparency. Provide information sufficient for understanding, oversight, and contestability while protecting credentials and exploitable details.

## Documentation set

- **System card:** purpose, architecture, owners, users, data flows, capabilities, limitations, and prohibited uses.
- **Model card:** model origin, intended use, evaluation, limitations, and ethical considerations.
- **Dataset card:** provenance, composition, processing, rights, gaps, and maintenance.
- **Decision records:** alternatives, assumptions, evidence, approvals, and consequences.
- **Evaluation report:** cases, versions, metrics, slices, errors, and release thresholds.
- **Operations record:** changes, alerts, incidents, overrides, and retirement.

Traceability should connect an outcome to system version, input class, retrieved source identifiers, tool calls, policy checks, and approval without retaining unnecessary raw personal data. Define access and retention for logs. Audit logs must themselves be protected from alteration and unauthorized browsing.

## Explanations and appeal

An explanation should support a real action: understand, correct data, request human review, or contest an outcome. Generic statements that "AI was used" are insufficient. Do not present generated rationales as faithful descriptions of hidden model reasoning. Explain observable inputs, rules, evidence, uncertainty, and process instead.

## Free local practice

Write a two-page system card and a one-page user notice for a capstone. Design an audit event schema with data minimization. Simulate a complaint and demonstrate how an authorized reviewer reconstructs the relevant version and evidence, corrects an error, and records the remedy.

## Completion criteria

- Each audience receives actionable information.
- Logs support reconstruction without collecting everything.
- Affected people have correction, review, and appeal paths.
- Documentation versions match deployable system versions.

## References

- [OECD transparency and explainability principle](https://oecd.ai/en/dashboards/ai-principles/P7)
- [Model Cards for Model Reporting](https://research.google/pubs/model-cards-for-model-reporting/)
- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010)
- [Google People + AI Guidebook](https://pair.withgoogle.com/guidebook-v2/)
