# Feasibility, Value, and Metrics

## Learning objectives

By the end of this lesson, you can:

- test business, operational, data, technical, and responsible-use feasibility;
- define a baseline, target, guardrail, and measurement window;
- estimate value without hiding labor, review, or failure costs;
- design a pilot with a defensible go, revise, or stop decision.

## Five feasibility lenses

Evaluate a candidate across all five lenses:

| Lens | Key question | Evidence |
| --- | --- | --- |
| Outcome | Does the change solve a verified user or operational problem? | Interviews, map, demand |
| Process | Are rules, owner, exceptions, and escalation defined? | Decision table, SOP |
| Data | Are inputs lawful, representative, accessible, and sufficiently clean? | Sample audit, data owner |
| Technical | Can systems expose required events and actions reliably? | API test, permissions, sandbox |
| Operation | Can people monitor, correct, support, and retire it? | Runbook, staffing, rollback |

A successful demo answers only part of technical feasibility. A production decision also needs capacity, access, error recovery, auditability, and maintenance.

## Metrics as a system

Use four kinds of measures:

- **Outcome:** the result for the recipient, such as valid cases resolved within one day.
- **Flow:** throughput, active time, waiting time, and work in progress.
- **Quality:** accuracy, rework rate, false approvals, and escalation quality.
- **Guardrail:** privacy incidents, complaints, inequitable failure rates, or actions without authorization.

Define each metric completely:

~~~text
Name: first-pass completion rate
Numerator: cases completed without return or manual correction
Denominator: all eligible cases started in the period
Exclusions: cancelled test cases
Segment: input channel and case type
Source: execution log plus review outcome
Baseline window: previous four weeks
Target: 80% or better
Guardrail: zero unauthorized actions
Owner: process owner
~~~

An average can hide harm. Segment results by meaningful case type, channel, language, or affected group when lawful and appropriate.

## Estimate net value

Use ranges, not a single optimistic number:

~~~text
gross_hours = eligible_cases * minutes_saved / 60
net_hours = gross_hours - review_hours - support_hours - rework_hours
net_value = net_hours * loaded_hourly_cost - run_cost - amortized_build_cost
~~~

Also record nonfinancial value: shorter waits, fewer errors, better audit evidence, or reduced repetitive work. Do not claim "time saved" unless the released time can be used for a stated outcome.

## Free local practice

Create a pilot scorecard for the candidate selected previously.

1. Sample at least 20 synthetic cases with normal and exception variants.
2. Manually execute the current process and record outcome, active time, wait, and error.
3. Define one outcome metric, two flow/quality metrics, and two guardrails.
4. Estimate low, expected, and high scenarios for volume, saved time, review rate, and run cost.
5. Design a shadow-mode pilot: the prototype proposes an output, but it takes no external action. Compare its proposal with the manual result.
6. Precommit decision rules:

| decision | rule |
| --- | --- |
| Go | Target met and every guardrail respected |
| Revise | Quality gap is localized and no severe harm occurred |
| Stop | Unauthorized action, missing legal basis, or unbounded failure |

The exercise can be completed in a spreadsheet. Keep raw observations so another person can reproduce the calculation.

## Completion criteria

You are finished when:

- all five feasibility lenses have evidence, gaps, and an owner;
- every metric has numerator, denominator, source, window, segment, and owner;
- the baseline comes from observations rather than memory;
- review, support, failures, and run cost appear in the value estimate;
- low, expected, and high scenarios are shown;
- a shadow-mode pilot and explicit go/revise/stop rules exist;
- guardrails cannot be traded away for better average performance.

## References

- [GOV.UK Service Manual: Measuring the success of your service](https://www.gov.uk/service-manual/measuring-success/measuring-the-success-of-your-service) - public guidance on combining user outcomes, operational measures, and research.
- [GOV.UK Service Standard: Define what success looks like and publish performance data](https://www.gov.uk/service-manual/service-standard/point-10-define-success-publish-performance-data) - guidance for baselines, metrics, and measurement plans.
- [NIST AI RMF 1.0](https://doi.org/10.6028/NIST.AI.100-1) - primary framework for trustworthy characteristics and context-sensitive measurement.
- [NIST AI RMF: Framing risk](https://airc.nist.gov/airmf-resources/airmf/1-sec-risk/) - explains risk as likelihood and consequence rather than a single performance score.
