# Safety, Evaluation, and Human Oversight

## Learning objectives

By the end of this lesson, you can:

- threat-model an agent across goals, context, tools, memory, identities, and dependencies;
- evaluate outcomes, trajectories, safety, latency, and resource use;
- design human approval that provides evidence and real authority;
- produce an architecture decision and release gate for a bounded agent.

## Threat-model the whole loop

Test at least:

- direct and indirect prompt injection;
- goal or instruction manipulation;
- sensitive information disclosure;
- unauthorized or over-broad tool use;
- malformed model output and unsafe downstream interpretation;
- memory/context poisoning;
- forged peer-agent or tool result;
- identity/privilege confusion;
- unbounded loops and resource exhaustion;
- compromised model, tool, package, or knowledge source.

Prompts are not security boundaries. Enforce controls in code and infrastructure: capability allowlists, typed validation, least privilege, network egress rules, sandboxing, human gates, quotas, immutable audit events, and revocation.

## Evaluate task and trajectory

Build a versioned evaluation set from the use-case rules and observed failures. Include normal, boundary, adversarial, and operational cases.

Measure:

- outcome correctness and completion;
- correct refusal and safe escalation;
- tool selection and argument validity;
- prohibited-action and access-violation rate;
- grounding/citation correctness;
- unnecessary steps and loop rate;
- recovery from timeout, duplicate, and stale state;
- p50/p95 latency, tokens/model calls, tool calls, and monetary cost where applicable;
- human review rate, override rate, and time;
- business outcome and guardrail impact in shadow mode.

A final-answer score can hide dangerous attempted actions. Evaluate the action trace and controller denials as well.

## Human oversight that works

Approval must show:

- requested action and consequence;
- target resource and scope;
- evidence and uncertainty;
- relevant policy and prior steps;
- reversible preview or diff;
- approve, edit, reject, and escalate options;
- expiry and single-use binding to exact arguments.

Do not ask a person to approve hundreds of opaque actions at speed. That is rubber stamping. Route only meaningful exceptions, prioritize by risk, and measure reviewer load and disagreement.

## Release stages

1. offline fixtures and deterministic tool stubs;
2. adversarial and failure injection;
3. read-only integration sandbox;
4. shadow mode beside the current process;
5. limited users/data/actions with approvals;
6. gradual expansion only if outcome and guardrails hold;
7. continuous monitoring, regression evaluation, incident response, and periodic reauthorization.

Define an immediate stop for unauthorized action, data exposure, unbounded behavior, or loss of auditability.

## Free local practice

Produce and test an architecture package:

1. Component and trust-boundary diagram.
2. Tool/capability matrix and approval contracts.
3. State, memory, retention, and deletion model.
4. Threat model with preventive, detective, and corrective controls.
5. At least 30 synthetic evaluation cases: 10 normal, 5 boundary, 5 injection/poisoning, 5 authorization/tool misuse, and 5 dependency/retry/loop failures.
6. A local scripted controller run over all cases. A local open model is optional, never required.
7. Results by case category, not only an overall average.
8. Shadow-mode plan, guardrails, stop authority, rollback, incident runbook, and reevaluation triggers.
9. Architecture decision record comparing fixed workflow, model-assisted workflow, single agent, and multi-agent option.
10. Final go, revise, or reject recommendation signed by the process and risk owners. In solo study, state that role separation was simulated.

## Completion criteria

You are finished when:

- threats cover goal, context, tools, memory, identity, dependencies, and resources;
- authorization and safety controls exist outside prompts and model output;
- the evaluation set includes normal, boundary, adversarial, and operational cases;
- outcomes and action trajectories are both scored;
- results are segmented and include latency/resource/reviewer burden;
- approval is argument-bound, expiring, informative, and revocable;
- shadow mode, stop conditions, rollback, and incident ownership are explicit;
- the selected architecture beats the simpler baseline without breaching guardrails.

## References

- [NIST AI RMF Generative AI Profile](https://doi.org/10.6028/NIST.AI.600-1) - primary lifecycle risk actions for generative-AI systems.
- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/) - public threat and mitigation guidance for injection, disclosure, poisoning, output handling, and excessive agency.
- [OWASP: Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) - focused guidance on limiting tool functionality, permissions, and autonomy.
- [MITRE ATLAS](https://atlas.mitre.org/) - public knowledge base of adversarial tactics and techniques for AI-enabled systems.
- [AgentBench: Evaluating LLMs as Agents](https://arxiv.org/abs/2308.03688) - original benchmark paper showing the need to evaluate agents in multi-step interactive environments.
