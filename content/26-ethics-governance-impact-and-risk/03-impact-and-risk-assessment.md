# Impact and Risk Assessment

## Learning objectives

Build an evidence-based risk register, distinguish inherent from residual risk, and connect each control to tests and an accountable owner.

## Frame the assessment

Document the intended purpose, excluded purposes, users, affected populations, operating environment, decision consequences, geographic scope, data flows, models, tools, vendors, human roles, and fallback process. State the system boundary explicitly. Risk often hides in an integration or downstream use omitted from the diagram.

Identify hazards across quality, safety, security, privacy, discrimination, autonomy, labor, information integrity, intellectual property, accessibility, environmental impact, and legal compliance. Include accidental failure, foreseeable misuse, malicious abuse, and correlated failures at scale.

## Risk register fields

For each risk, record:

| Field | Purpose |
|---|---|
| Scenario | Cause, event, affected party, and consequence |
| Existing evidence | Incidents, tests, research, or explicit uncertainty |
| Inherent risk | Exposure before proposed controls |
| Preventive controls | Reduce likelihood or exposure |
| Detective controls | Reveal failure quickly |
| Corrective controls | Limit impact and restore service |
| Control test | Evidence that the control works |
| Residual risk | Exposure after tested controls |
| Owner and review date | Accountability and freshness |

Do not multiply arbitrary likelihood and severity numbers to manufacture precision. Use calibrated categories with definitions and record uncertainty. Catastrophic but poorly estimated outcomes still require consideration.

## Generative AI risks

The NIST Generative AI Profile identifies risks such as confabulation, harmful content, privacy, information integrity, information security, intellectual property, bias, human-AI configuration, and value-chain dependencies. Translate relevant categories into concrete scenarios for the actual system. A generic list is the start of assessment, not the result.

## Free local practice

Create at least 15 risk scenarios for a capstone. Select five material risks and specify prevention, detection, response, owner, and test evidence. Conduct a tabletop exercise for one model outage and one harmful tool action. Revise residual risk based on what the exercise reveals.

## Completion criteria

- Risks describe consequences to specific affected parties.
- Inherent and residual risk are separated.
- Every material control has an owner and test.
- The assessment can recommend stopping or narrowing the project.

## References

- [NIST Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [NIST AI Resource Center](https://airc.nist.gov/)
- [OECD robustness, security, and safety principle](https://oecd.ai/en/dashboards/ai-principles/P8)
