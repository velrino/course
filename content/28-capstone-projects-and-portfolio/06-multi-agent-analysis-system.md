# Capstone: Multi-Agent Analysis System

## Objective

Determine empirically whether multiple agents improve a bounded analysis task enough to justify their additional coordination, cost, and risk.

## Scenario

Given a small set of public reports, produce a comparison table and evidence-grounded memo. Candidate roles are source extractor, quantitative checker, contradiction finder, and editor. None may browse outside an allowlist or perform external writes.

## Required comparisons

Build four variants over the same tools and evaluation set:

1. deterministic extraction baseline;
2. one structured model call;
3. one agent with tools;
4. multiple specialized agents with an explicit coordinator.

Keep model settings and source corpus fixed where possible. Record every handoff as structured data with provenance. The coordinator may select or reject outputs but may not erase disagreement silently.

## Evaluation

Create at least 30 cases with direct evidence, conflicts, missing values, inconsistent units, outdated versions, duplicated text, and injected instructions. Measure claim support, numeric correctness, contradiction detection, abstention, route completion, model calls, tokens or estimated workload, latency, and failure amplification.

Run ablations by removing each role. Analyze correlation: several agents using one model are not independent reviewers. Include a human spot-check of material claims.

## Decision rule

Define before testing how much improvement justifies the multi-agent version. If the threshold is not met, the correct project conclusion is to recommend the simpler system. A negative result with sound evidence is a successful capstone.

## Deliverables

- Architecture and handoff schemas.
- Four runnable variants.
- Fixed corpus, evaluation cases, and comparison report.
- Trace samples showing success and error propagation.
- Risk, cost, and maintainability analysis.

## Completion criteria

- All variants use comparable evidence and tests.
- Handoffs preserve provenance and uncertainty.
- Conflicting results remain visible for resolution.
- The final recommendation follows the predefined decision rule.

## References

- [CrewAI documentation](https://docs.crewai.com/)
- [LangGraph multi-agent concepts](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [NIST AI Resource Center](https://airc.nist.gov/)
