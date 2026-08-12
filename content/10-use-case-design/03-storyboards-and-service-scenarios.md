# Storyboards and Service Scenarios

## Learning objectives

By the end of this lesson, you can:

- use a storyboard to expose context, handoffs, feedback, and recovery;
- show both the user's experience and backstage automation;
- represent uncertainty and human intervention without pretending the happy path is complete;
- select scenes that answer a specific design question.

## Why storyboard an automation

A process diagram shows control flow; a storyboard shows the situation in which that flow matters. It makes visible what happens before a trigger, what the person believes, when the system communicates, and how someone recovers.

Use six to eight frames. Each frame should contain:

1. context and actor goal;
2. actor action;
3. visible system response;
4. backstage process or decision;
5. data crossing a boundary;
6. question, risk, or emotion worth testing.

Drawing quality is irrelevant. Boxes, arrows, and short captions are enough.

## Storyboard more than success

Create three related scenarios:

- **Normal:** the system handles an eligible, well-formed case.
- **Boundary:** the content is ambiguous or incomplete and a person must decide.
- **Failure and recovery:** a dependency fails after work starts, or a duplicate event arrives.

In each, show:

- how the user knows the request was received;
- what status they can see while waiting;
- what the automation is authorized to do;
- where a person reviews and what evidence they receive;
- what happens to partial work;
- how the user corrects, cancels, or appeals;
- what is recorded for later explanation.

Do not draw a model as a magical box labeled "AI." Name the narrow behavior: "proposes one of four categories with cited text," followed by schema validation and an authority check.

## From scenes to hypotheses

Attach one testable claim to each uncertain scene:

| scene | hypothesis | observation |
| --- | --- | --- |
| Missing field notice | User can correct without support | Identifies field and next action |
| Human review queue | Reviewer sees enough evidence | Decides without reopening source |
| Timeout | User understands work is retained | Can state current status |

The storyboard is successful when it reveals that the concept is wrong or incomplete early. It is not an illustration to defend a fixed solution.

## Free local practice

Use paper, a slide tool, [diagrams.net](https://www.diagrams.net/), or [Excalidraw](https://excalidraw.com/).

1. State one research question at the top, such as "Can a requester recover from a validation failure without contacting support?"
2. Draw a six-frame normal scenario.
3. Duplicate it and change the triggering example into an ambiguous input.
4. Create a third version where the downstream API times out after validation.
5. Below every frame, write visible response, backstage action, data used, and unresolved assumption.
6. Mark automated decisions with A, human decisions with H, and deterministic validation with D.
7. Walk another person through the frames without explaining missing details. Ask them what they believe happens next and what the system has already done.
8. Record misunderstandings as design defects, not user errors.

Use fictional identifiers and messages. Do not paste production screenshots containing personal data.

## Completion criteria

You are finished when:

- a specific research question determines what the storyboard contains;
- normal, ambiguous, and technical-failure scenarios exist;
- visible experience and backstage behavior are aligned in every frame;
- data boundaries, authorization, human review, and partial work are shown;
- the person can see status and recover, cancel, or appeal where relevant;
- every uncertain scene has a testable hypothesis;
- observed misunderstandings led to documented revisions.

## References

- [IDEO.org Design Kit: Methods](https://www.designkit.org/methods.html) - public human-centered design methods, including storyboards, role play, and prototype selection.
- [GOV.UK Open Policy Making Toolkit: Prototyping and improving ideas](https://www.gov.uk/guidance/open-policy-making-toolkit/4-delivery-prototyping-and-improving-ideas) - public guidance for touchpoint and experience prototypes.
- [GOV.UK Service Manual: Researching user experiences](https://www.gov.uk/service-manual/user-research/researching-user-experiences) - method for capturing actions, thoughts, feelings, and events over time.
- [GOV.UK Service Manual: Creating an experience map](https://www.gov.uk/service-manual/user-research/creating-an-experience-map) - guidance on consolidating stages, steps, channels, and needs.
