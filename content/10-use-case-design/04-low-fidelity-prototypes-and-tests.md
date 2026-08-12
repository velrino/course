# Low-Fidelity Prototypes and Tests

## Learning objectives

By the end of this lesson, you can:

- choose the cheapest prototype capable of answering a high-risk question;
- run a structured usability or workflow test without leading the participant;
- simulate unfinished automation with a Wizard-of-Oz method;
- convert observations into decisions without overstating a tiny sample.

## Fidelity follows the question

Prototype only enough to learn:

| question | suitable prototype |
| --- | --- |
| Is the sequence understandable? | Paper screens or clickable slides |
| Does the handoff include enough evidence? | Sample queue card and role play |
| Can an API support the operation? | Narrow command-line spike in a sandbox |
| Is a classification useful? | Offline labeled examples and a human simulation |
| Can the service recover? | Failure injection on a local stub |

Visual polish can make participants hesitate to criticize and can consume effort before the concept is valid. Increase fidelity only after the earlier uncertainty is resolved.

## Wizard-of-Oz automation

In a Wizard-of-Oz test, a person secretly performs the proposed system behavior. This tests the interaction and operating model without building the automation.

Use a strict script:

1. Receive a synthetic input.
2. Apply the written decision table.
3. Return only outputs the proposed system could produce.
4. Measure response time and record exceptions.
5. Never pretend a consequential real action occurred.

This is especially useful for agent concepts. It reveals whether outputs and escalation are useful before model cost and variability complicate the result.

## A neutral test protocol

Write:

- research question and risk;
- participant profile based on relevant behavior, not decorative demographics;
- realistic task and starting state;
- prototype limits and safety statement;
- observations to capture;
- pass, revise, and stop thresholds.

Ask the participant to attempt a task. Avoid "Click the obvious review button." Use "You received this status and need to correct the request. Show what you would do." Observe actions, pauses, expectations, and errors. Ask follow-up questions after the attempt.

Do not treat five participants as a statistical proof. Small qualitative tests expose failure modes and mental-model gaps; they do not establish population accuracy.

## Free local practice

1. Select the highest-consequence assumption from your register.
2. Build a paper, slide, or static HTML prototype containing only the path required to test it.
3. Prepare five synthetic cases: two normal, one boundary, one duplicate, and one dependency failure.
4. Run the task with three people if available. If not, perform a cognitive walkthrough from three roles and clearly label this limitation.
5. Record an evidence table:

| observation | interpretation | severity | change | retest |
| --- | --- | --- | --- | --- |
| Participant retries after timeout | Status did not show request retained | High | Add receipt and state | Required |

6. Separate observation from interpretation. Quote only with consent and remove identifying details.
7. Revise once and rerun the failed task.
8. Archive the version, cases, protocol, raw notes, and decision.

## Completion criteria

You are finished when:

- the prototype addresses one named high-risk question;
- its fidelity is no higher than necessary;
- tasks and prompts do not reveal the intended answer;
- normal, boundary, duplicate, and failure cases are exercised;
- observations and interpretations are stored separately;
- the evidence leads to a continue, revise, or stop decision;
- at least one failed task is revised and retested;
- privacy, consent, and sample limitations are documented.

## References

- [GOV.UK Open Policy Making Toolkit: Prototyping and improving ideas](https://www.gov.uk/guidance/open-policy-making-toolkit/4-delivery-prototyping-and-improving-ideas) - public techniques for paper, touchpoint, role-play, and experience prototypes.
- [IDEO.org Design Kit: Determine what to prototype](https://www.designkit.org/methods/determine-what-to-prototype.html) - public method for isolating what a prototype needs to test.
- [GOV.UK Service Manual: Plan a round of user research](https://www.gov.uk/service-manual/user-research/plan-user-research-for-your-service) - public guidance for research questions, participant selection, and sessions.
- [W3C WAI: Involving users in web accessibility evaluation](https://www.w3.org/WAI/test-evaluate/involving-users/) - primary accessibility guidance for including disabled users alongside standards-based evaluation.
