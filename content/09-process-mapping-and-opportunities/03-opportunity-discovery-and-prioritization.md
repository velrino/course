# Opportunity Discovery and Prioritization

## Learning objectives

By the end of this lesson, you can:

- find automation opportunities from process evidence rather than tool enthusiasm;
- distinguish eliminate, simplify, standardize, assist, and automate options;
- score candidates transparently with sensitivity to uncertainty;
- reject unsuitable work before spending implementation effort.

## Improvement before automation

For each pain point, ask in this order:

1. **Eliminate:** does the step exist only because of an obsolete policy or duplicate record?
2. **Simplify:** can the input, rule, or number of handoffs be reduced?
3. **Standardize:** can variants share one schema and one definition of done?
4. **Assist:** can software prepare evidence while a person decides?
5. **Automate:** can the system execute a well-defined, reversible action?

Automating waste makes it faster and harder to see. A common example is copying an approval result into three spreadsheets. The best change may be one authoritative record, not a bot that maintains all three.

## Candidate signals and warning signs

Good early candidates are frequent, rules-based, digitally observable, low-consequence, reversible, and supported by stable inputs. They have a known owner and enough examples to test.

Warning signs include ambiguous goals, rare but catastrophic errors, discretionary decisions about people, constantly changing inputs, missing authority, and no safe rollback. Generative AI can help classify or summarize uncertain content, but it does not remove accountability. When consequences are meaningful, use AI to propose and a person to decide.

## A transparent score

Use a 0-5 scale for each dimension:

- volume and time saved;
- error or delay reduction;
- input readiness;
- rule clarity;
- reversibility and observability;
- implementation effort;
- harm, privacy, and compliance exposure.

One simple priority score is:

~~~text
benefit = volume + time_saved + quality_gain
readiness = input_readiness + rule_clarity + reversibility
cost_and_risk = effort + harm_exposure
priority = benefit + readiness - cost_and_risk
~~~

The formula is not truth. It exposes assumptions. Add confidence (low, medium, high) and run a sensitivity check: change every uncertain score by one point. If the ranking flips, gather more evidence before choosing.

Never use a high aggregate score to cancel a red-line constraint. An opportunity involving unlawful processing, unavailable consent, or irreversible harm is not made acceptable by large savings.

## Free local practice

From your current-state map, identify at least six pain points and create one candidate for each. Include at least one non-automation option.

Build a local CSV:

~~~csv
candidate,change_type,weekly_cases,minutes_saved,input_readiness,rule_clarity,reversibility,effort,harm_exposure,confidence
Rename study files,automate,25,1,5,5,5,1,0,high
Summarize private notes,assist,10,4,3,2,4,2,3,low
~~~

Score the candidates manually or with a spreadsheet formula. Then:

1. Write the evidence behind each score.
2. Identify one hard stop for each candidate.
3. Recalculate with uncertain values one point lower for benefits and one point higher for risk.
4. Choose one candidate for a reversible two-week experiment.
5. Write why the top-scoring candidate might still not be the right choice.

Use no real customer or employee data. The aim is decision quality, not model training.

## Completion criteria

You are finished when:

- at least six opportunities trace to named pain points in the current-state map;
- eliminate and simplify options were considered before automation;
- every score has evidence and a confidence label;
- hard-stop constraints remain separate from the numeric ranking;
- a sensitivity check shows whether the recommendation is stable;
- the selected experiment is low-risk, reversible, owned, and time-bounded;
- the rejected candidates have recorded reasons.

## References

- [GOV.UK Service Manual: Map and understand a user's whole problem](https://www.gov.uk/service-manual/design/map-a-users-whole-problem) - guidance on turning journey problems into an improvement backlog.
- [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) - primary outcomes for governing, mapping, measuring, and managing AI risk.
- [NIST AI RMF Playbook](https://airc.nist.gov/airmf-resources/playbook/) - public suggested actions for operationalizing risk-aware decisions.
- [OECD: Advancing accountability in AI](https://oecd.ai/en/accountability/) - lifecycle-based treatment of context, stakeholders, risk, and accountability.
