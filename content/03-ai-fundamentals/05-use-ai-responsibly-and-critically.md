# Use AI Responsibly and Critically

## Learning objectives

By the end of this lesson, you will be able to:

- analyze an AI system as a socio-technical system;
- create a risk register tied to people, context, and controls;
- verify generated claims and handle uncertainty; and
- define human oversight that changes outcomes rather than decorating a process.

## Trustworthiness is contextual

An AI system includes data collection, people, interfaces, models, tools, policies, monitoring, and the environment in which decisions have consequences. Model behavior cannot be assessed in isolation.

NIST identifies characteristics including validity and reliability, safety, security and resilience, accountability and transparency, explainability and interpretability, privacy enhancement, and fairness with harmful bias managed. These characteristics can conflict. More detailed logging may help accountability while increasing privacy risk; a smaller model may reduce cost while failing a critical language group. Tradeoffs must be recorded in the use context.

## Build a concrete risk register

Use rows that can drive action:

| Harm scenario | Affected parties | Cause | Likelihood | Severity | Prevention | Detection | Response | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Draft invents a refund policy | customer, support staff | unsupported generation | medium | high | retrieve approved policy; constrain task | sample audit; citation check | block send; escalate | support lead |

Avoid risks such as "AI could be biased" without mechanism or affected group. Ask whose data is missing, which historic decisions created labels, who bears each error, and who can contest an outcome.

## Generated content is an untrusted proposal

A fluent answer can be false. Treat generated text, code, citations, and tool arguments as untrusted input:

1. identify claims that can affect a decision;
2. locate primary or authoritative evidence;
3. open the cited source and confirm it supports the claim;
4. run code in an isolated, least-privileged environment;
5. validate tool arguments against a schema and authorization policy; and
6. preserve uncertainty when evidence is incomplete.

Do not ask a model to "be confident only when correct." Confidence language is generated text, not calibrated probability.

## Make human oversight effective

A human reviewer needs time, authority, relevant context, and a usable alternative. Requiring approval after hundreds of automated recommendations can create automation bias and rubber-stamping.

Design review around risk:

- show source data and material uncertainty;
- highlight changes and irreversible effects;
- allow edit, reject, and escalate;
- record reviewer reasons where appropriate;
- sample low-risk automated cases for audit; and
- pause the system when monitoring crosses a defined threshold.

## Free local practice: AI system card

Write a two-page system card for the study-planning assistant from the previous lesson. Include:

- intended and excluded uses;
- users and affected non-users;
- data sources and prohibited data;
- model and non-model components;
- evaluation tasks and subgroup slices;
- top five risk-register rows;
- human-control points;
- monitoring and shutdown thresholds; and
- unresolved limitations.

Then conduct a hostile review: invent three ways a well-intentioned user, malicious input, or failing dependency could cause harm. Update the controls.

## Completion criteria

- [ ] Risks name a scenario, cause, affected party, and owner.
- [ ] Every high-severity risk has prevention, detection, and response controls.
- [ ] Your verification process opens primary evidence rather than trusting a citation string.
- [ ] Human review has context, authority, and an alternative action.
- [ ] The system card states excluded uses and unresolved limitations.

## References

- [NIST AI Risk Management Framework 1.0](https://doi.org/10.6028/NIST.AI.100-1) - primary voluntary framework for trustworthy and responsible AI risk management.
- [NIST Generative AI Profile](https://doi.org/10.6028/NIST.AI.600-1) - public companion profile covering risks specific to generative AI.
- [People + AI Guidebook](https://pair.withgoogle.com/guidebook-v2/) - human-centered patterns for defining success, data, mental models, explanation, controls, and graceful failure.
- [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993) - original paper proposing structured reporting of intended uses, evaluation, and limitations.

## Continue

Next module: [Map the Generative AI Landscape](../04-llms-and-generative-ai/01-map-the-generative-ai-landscape.md)
