# Value Measurement and Continuous Improvement

## Learning objectives

Measure operational value against a baseline, include total cost and harm, and make evidence-based scale, revise, or stop decisions.

## A balanced measurement model

Define measures before deployment across five dimensions:

| Dimension | Examples |
|---|---|
| Outcome | wait time, rework, resolution quality, access |
| Quality | task success, factual support, error severity |
| Safety and rights | unsafe action, privacy event, appeal, disparity |
| Operations | latency, availability, incident load, override rate |
| Economics and work | total cost, staff time, review burden, training |

Measure the current process first. Otherwise normal variation or seasonal change may be attributed to the new system. When feasible, compare matched groups or phased rollout periods and document confounders. A before-and-after chart alone does not establish causation.

## Total cost

Include discovery, data preparation, engineering, evaluation, security review, licenses, model and infrastructure usage, human review, monitoring, incident response, vendor management, retraining, and exit. Include opportunity cost and newly created manual work. Report ranges when future volume or pricing is uncertain.

## Improvement loop

Review failures by severity and mechanism, not only count. Connect each improvement to a hypothesized cause and rerun frozen regression cases. Add new cases for novel failures without rewriting history. Major changes repeat risk and release gates.

Use a decision cadence with four possible outcomes: continue unchanged, improve within scope, narrow or reduce autonomy, or retire. Scaling is not the default reward for completing a pilot.

## Free local practice

Build a measurement plan for your capstone. Define a baseline, target, guardrail, data source, owner, cadence, and decision threshold for at least ten measures. Estimate total cost for low, expected, and high volume. Write one scenario where strong productivity numbers should still cause the project to stop.

## Completion criteria

- Outcomes are compared with a credible baseline.
- Quality, safety, operations, economics, and work are all represented.
- Costs include human review and ongoing maintenance.
- Review decisions include narrowing and retirement.

## References

- [Google Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [GOV.UK: Measuring the success of your service](https://www.gov.uk/service-manual/measuring-success/measuring-the-success-of-your-service)
