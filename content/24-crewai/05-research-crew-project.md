# Project: Evidence-Grounded Research Crew

## Learning objectives

Build and evaluate a small Crew inside a controlled Flow, with transparent handoffs and a single-agent baseline.

## Free local practice

## Project brief

Given a folder of public documents, produce a short decision memo that cites exact source passages, identifies conflicts, and separates facts from recommendations. Use only local files in the required version. An optional extension may retrieve public web pages after adding domain allowlists and content-safety controls.

The Flow owns input validation, document selection, final schema validation, approval, and output persistence. The Crew may contain:

- an **extractor** that returns passages with source identifiers;
- an **analyst** that compares evidence and states uncertainty;
- a **reviewer** that checks whether each material claim is supported.

Do not let the reviewer rewrite unsupported prose into plausible prose. It must reject or flag it.

## Baselines and ablations

Compare the Crew with one structured model call and with a deterministic extractive baseline. Then remove one role at a time. If the full Crew does not improve predefined measures enough to justify added cost and failure paths, ship the simpler design.

## Evaluation

Create at least 25 cases containing direct support, no support, conflicting documents, outdated text, duplicated passages, prompt injection, and inaccessible files. Measure claim support, citation correctness, conflict detection, abstention when evidence is absent, runtime, and model calls.

Manually inspect a sample. Automated model judging may help triage but cannot be the sole evidence for factual grounding.

## Deliverables

- Architecture and data-flow diagram.
- Agent, task, and Flow configuration.
- Local corpus with provenance and licenses.
- Baselines, ablation results, and versioned evaluation cases.
- Threat model, approval step, and runbook.
- Decision memo plus a report on unsupported or conflicting claims.

## Completion criteria

- The project runs on non-sensitive local documents.
- Every material factual claim maps to a retrievable passage.
- Missing evidence causes abstention or review.
- The multi-agent design beats a simpler baseline on predefined measures or is rejected in the final recommendation.

## References

- [CrewAI documentation](https://docs.crewai.com/)
- [CrewAI examples repository](https://github.com/crewAIInc/crewAI-examples)
- [NIST AI Resource Center](https://airc.nist.gov/)
- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010)
