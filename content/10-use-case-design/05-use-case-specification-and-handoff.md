# Use-Case Specification and Handoff

## Learning objectives

By the end of this lesson, you can:

- consolidate research, scenarios, rules, data, and operational constraints into one specification;
- distinguish preconditions, guarantees, alternative flows, and failure handling;
- create traceability from evidence to acceptance tests and metrics;
- hold a readiness review that can legitimately reject implementation.

## The behavioral contract

Use this compact specification:

~~~text
Use-case ID and version:
Outcome and evidence:
Primary actor and affected parties:
Trigger:
Preconditions:
Inputs and data classification:
Main flow:
Alternative and exception flows:
Allowed external actions:
Prohibited actions:
Human decisions and escalation:
Outputs and status model:
Postconditions and guarantees:
Audit events:
Metrics and guardrails:
Rollback and shutdown:
Open assumptions:
Owner and review date:
~~~

A **precondition** must be true before execution, such as a verified source and active credential. A **postcondition** is guaranteed after a path, such as "an accepted result has exactly one audit record." If a guarantee cannot be maintained during failure, weaken the claim or redesign the flow.

Define the status model explicitly. For example:

~~~text
received -> validating -> ready -> processing -> completed
                       \-> needs_review
             \-> rejected
processing -> retry_wait -> processing
processing -> failed_safe
~~~

For each transition, name the event, actor, validation, and side effect. A terminal failure should not leave the user believing work completed.

## Traceability

Create stable identifiers:

| need | story | rule | test | metric/risk |
| --- | --- | --- | --- | --- |
| N-01 know missing evidence | US-03 | R-07 required fields | AT-12 | M-02 recontact rate |

Traceability is not paperwork for its own sake. It exposes orphan features, untested rules, and metrics that no design decision supports.

## Readiness review

Review the specification with process owner, operator, implementation, support, and relevant data/security roles. Ask:

- Can we supply representative synthetic and approved test data?
- Is every write operation authorized and reversible?
- Are duplicates, retries, timeouts, and partial completion defined?
- Can an operator see, correct, and stop the system?
- Is there a baseline and a decision threshold?
- Who supports it outside the builder's availability?

"Not ready" is a valid and valuable outcome.

## Free local practice

1. Complete the template for the use case developed in this module.
2. Add a status-transition table with at least eight transitions.
3. Create a traceability matrix connecting every user need to a story, rule, test, and measure.
4. Insert links to the current-state map, storyboard, prototype evidence, decision table, and risk register.
5. Run a tabletop review using three cases: happy path, unauthorized duplicate, and downstream timeout after a write attempt.
6. Record all questions the specification cannot answer.
7. Classify each gap as blocker, pre-pilot task, or later improvement. Assign an owner and due condition.
8. Sign the readiness decision with a date and a review/expiry date. In solo study, sign each role separately and state the limitation.

## Completion criteria

You are finished when:

- trigger, preconditions, inputs, flows, statuses, postconditions, and owners are explicit;
- allowed and prohibited actions are unambiguous;
- every status transition has an event, actor, validation, and side effect;
- duplicates, partial failure, retry, cancellation, and human escalation are defined;
- needs trace through stories and rules to tests and measures;
- blockers have owners and cannot be silently converted into assumptions;
- the readiness review produces a documented go, revise, or stop decision.

## References

- [IETF RFC 2119: Key words for requirements](https://datatracker.ietf.org/doc/html/rfc2119) - primary definitions for unambiguous MUST, SHOULD, and MAY language.
- [GOV.UK Service Manual: Writing user stories](https://www.gov.uk/service-manual/agile-delivery/writing-user-stories) - public guidance on outcomes, acceptance, and backlog-ready stories.
- [Cucumber: Gherkin reference](https://cucumber.io/docs/gherkin/reference/) - official syntax and semantics for example-based behavioral specifications.
- [NIST Secure Software Development Framework 1.1](https://doi.org/10.6028/NIST.SP.800-218) - primary practices for requirements, risk, verification, provenance, and secure release.
