# Problem Framing and User Needs

## Learning objectives

By the end of this lesson, you can:

- write an evidence-based problem statement without embedding a preferred solution;
- distinguish user needs, organizational outcomes, constraints, and feature requests;
- identify primary, secondary, and negatively affected actors;
- turn assumptions into questions that a prototype can answer.

## Start with the problem, not the bot

"We need an AI agent to answer email" is a solution claim. A testable problem statement is:

> Support coordinators spend a median of 12 minutes locating approved policy text for routine questions. In 18 of 60 sampled cases, the first response omitted a required next step, causing another contact.

Use this structure:

~~~text
[Actor] experiences [observable problem] while trying to [goal].
Evidence: [sample, observation, or artifact].
Consequence: [user and operational effect].
Current workaround: [what happens today].
We will not assume: [proposed solution].
~~~

Preserve the distinction between:

- **User need:** an outcome a person must achieve, independent of interface.
- **Organizational outcome:** a result such as fewer avoidable contacts or shorter wait.
- **Constraint:** a condition such as privacy law, operating hours, or a read-only API.
- **Feature request:** one possible implementation, such as a chatbot.

A user does not inherently need a dashboard. They may need to know whether their submission was accepted and what to do next.

## Actors and uneven consequences

List the primary user, frontline operator, subject of the data, approver, support staff, and anyone who might lose access or autonomy. One change may save staff time while making the process harder for people with limited connectivity or a different language.

Create an actor-outcome table:

| actor | goal | evidence of need | possible benefit | possible burden |
| --- | --- | --- | --- | --- |
| Requester | Know what is missing | Returned forms | Clear next action | Automated denial |
| Reviewer | See complete evidence | Observation | Less searching | Alert overload |

Do not invent personas with decorative demographics. Describe behavior, context, access needs, and evidence.

## Assumptions become research questions

Label each claim as known, assumed, or unknown. Rank assumptions by consequence if wrong and uncertainty. High-consequence, high-uncertainty claims are the first prototype targets.

Example:

- Assumption: requesters understand the category labels.
- Risk if wrong: valid cases are routed incorrectly.
- Test question: can five representative users choose the correct category using only the proposed wording?
- Evidence threshold: at least four succeed without hints; all misunderstandings are recorded.

## Free local practice

Use the automation brief from the previous module.

1. Rewrite the opportunity as a solution-neutral problem statement.
2. Extract every claim and mark its evidence source.
3. Create an actor-outcome table with at least four roles, including one affected person who does not operate the system.
4. Write three user needs in this form:

~~~text
As a [person in a context],
I need to [achieve an outcome],
so that [meaningful reason].
Evidence: [source].
~~~

5. Create an assumption register:

| assumption | uncertainty | consequence | test | pass evidence |
| --- | --- | --- | --- | --- |
| Input has an order ID | Medium | Medium | Inspect 20 synthetic variants | 19 parse; one safe rejection |

6. Remove any feature name from the problem and needs. Verify that more than one solution remains possible.

## Completion criteria

You are finished when:

- the problem names an actor, observable condition, evidence, and consequence;
- no tool, model, interface, or vendor is presented as the need;
- organizational outcomes and user needs are separately stated;
- at least one non-operator affected party and possible burden are included;
- claims are labeled known, assumed, or unknown;
- high-risk assumptions have answerable research questions and evidence thresholds;
- multiple plausible solutions still fit the framing.

## References

- [GOV.UK Service Manual: Learning about users and their needs](https://www.gov.uk/service-manual/user-research/start-by-learning-user-needs) - public guidance on evidence-based needs rather than assumptions or feature requests.
- [GOV.UK Service Manual: Writing user stories](https://www.gov.uk/service-manual/agile-delivery/writing-user-stories) - actor, need, goal, and acceptance guidance.
- [GOV.UK Service Manual: Scoping your service](https://www.gov.uk/service-manual/design/scoping-your-service) - guidance for matching scope to the user's wider goal.
- [NIST AI RMF: Map function](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) - primary framework outcomes for context, intended purpose, affected parties, impacts, and assumptions.
