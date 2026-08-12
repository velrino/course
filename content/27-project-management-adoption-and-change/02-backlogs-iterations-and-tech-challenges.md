# Backlogs, Iterations, and Technical Challenges

## Learning objectives

Turn outcomes and risks into a prioritized backlog, define testable increments, and use technical challenges to produce evidence rather than demos.

## Backlog structure

A useful backlog contains user outcomes, enabling technical work, risk controls, evaluation data, operations, documentation, and retirement tasks. If security and evaluation live in a separate "later" backlog, feature delivery will outrun evidence.

Write a user story only when the user and value are known. Pair it with acceptance criteria that can be tested. For system-level work, an outcome or risk story may be clearer:

> We need to determine whether retrieval preserves document-level permissions so that unauthorized passages never enter model context.

Prioritize by value, risk reduction, learning, dependency, and effort. A short experiment that invalidates a dangerous assumption can outrank a visible feature.

## Iterations and increments

In Scrum, a Sprint produces a usable Increment toward a Product Goal. For AI work, usable includes versioned data, reproducible evaluation, and operational controls. A notebook screenshot with undocumented prompts is not an increment.

Limit work in progress and keep changes small enough to attribute effects. Freeze an evaluation set while comparing prompts or models. Record a decision after each experiment: adopt, revise, reject, or gather different evidence.

## Technical Challenge format

Each challenge should contain:

- question or risk being tested;
- constraints and fixed baseline;
- artifact to build;
- evaluation cases and thresholds;
- timebox and resource limit;
- evidence package;
- decision and follow-up.

Challenges should include failure cases. "Make an agent" is not a challenge; "demonstrate that duplicated webhook delivery produces one ticket in 50 replay tests" is.

## Free local practice

Create a 20-item backlog for one capstone. Include at least four evaluation items, four safety or privacy items, two operations items, and two documentation items. Select a one-week technical challenge and define its baseline, cases, thresholds, and stop rule before implementation.

## Completion criteria

- Backlog priority reflects risk and learning, not only feature visibility.
- Acceptance criteria are observable.
- The challenge has a frozen baseline and predefined threshold.
- The completed increment includes reproducibility and operating evidence.

## References

- [The Scrum Guide](https://scrumguides.org/scrum-guide.html)
- [GOV.UK: Agile delivery](https://www.gov.uk/service-manual/agile-delivery)
- [GOV.UK: Writing user stories](https://www.gov.uk/service-manual/agile-delivery/writing-user-stories)
