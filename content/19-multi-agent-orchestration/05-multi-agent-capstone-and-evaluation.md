# Multi-Agent Capstone and Evaluation

## Learning objectives

- Build a bounded multi-agent workflow with inspectable contracts and events.
- Compare it fairly against a simpler baseline.
- Produce operational, security, and quality evidence for a deployment decision.

## Capstone: evidence review desk

Build a local system that receives a claim and returns a cited evidence brief. Use four logical components:

1. **Coordinator:** validates the request, selects workers, owns state/budget, and returns the brief.
2. **Source worker:** searches only a local corpus of public primary documents.
3. **Counter-evidence worker:** looks for exceptions or contradicting passages in the same corpus.
4. **Citation verifier:** deterministically checks that cited IDs exist and quoted spans support the structured claim.

The workers may be deterministic functions, local models, or an open-source framework. Framework use is optional; the architecture and evidence matter more. No component may access the open internet or write outside a sandbox during evaluation.

Define JSON contracts, a state diagram, permission matrix, call/time limits, partial-result policy, and termination conditions before implementation. Preserve disagreements. The final status must be `supported`, `contradicted`, `mixed`, or `insufficient_evidence`, with source IDs and warnings.

## Free local practice

Create 30 cases from the corpus: 10 direct, 5 requiring synthesis, 5 with exceptions, 5 conflicting/versioned, and 5 unsupported or adversarial. Freeze expected evidence and status first.

Compare three configurations on identical cases:

- deterministic retrieval plus template;
- one agent with all read-only tools;
- the multi-agent design.

Measure status accuracy, evidence recall, citation validity, unsupported-claim count, critical policy failures, calls, tokens if applicable, p95 latency, and estimated cost. Inject worker timeouts and malformed outputs in a separate reliability suite. Perform paired analysis and inspect every case where the complex design differs.

Create these artifacts: architecture diagram, contracts, threat model, event trace example, dataset manifest/hash, results by slice, incident/rollback runbook, and an architecture decision record. The correct conclusion may be to deploy the simpler baseline.

## Completion criteria

- The system completes all four statuses and preserves conflicting evidence.
- Permissions, budgets, schema validation, timeouts, and replay behavior have automated tests.
- All three configurations run against the same frozen cases and constraints.
- The decision record justifies deploy, revise, or reject using quality, safety, latency, and cost evidence.

## References

- [CrewAI crews documentation](https://docs.crewai.com/en/concepts/crews) - roles, tasks, processes, memory, and observability in an open-source framework.
- [AutoGen AgentChat tutorial](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/index.html) - agents, teams, state, and termination.
- [LangChain custom multi-agent workflows](https://docs.langchain.com/oss/python/langchain/multi-agent/custom-workflow) - mixing deterministic graph logic and agent nodes.
- [A2A Protocol specification](https://a2a-protocol.org/latest/specification/) - a framework-neutral reference for interoperable task and artifact exchange.
- [AgentBench paper](https://arxiv.org/abs/2308.03688) - evaluation of interactive agent behavior across environments.
