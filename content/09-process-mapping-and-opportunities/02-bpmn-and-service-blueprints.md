# BPMN and Service Blueprints

## Learning objectives

By the end of this lesson, you can:

- represent events, activities, decisions, handoffs, and exceptions consistently;
- choose between a flowchart, a BPMN model, and a service blueprint;
- avoid diagrams that look precise but omit responsibility or failure paths;
- validate a map by replaying real cases through it.

## Two views of the same service

**BPMN** describes control flow. Its small core vocabulary is enough for most discovery work:

- a circle is an event, such as an email arriving;
- a rounded rectangle is a task;
- a diamond is a gateway that routes based on a stated condition;
- arrows show sequence;
- pools or lanes show who is responsible;
- message flows show communication across participant boundaries.

A **service blueprint** aligns the user's journey with visible service interactions, backstage work, supporting systems, evidence, and pain points. BPMN answers "what executes next?" A blueprint answers "what does the person experience, and what organization makes that possible?" Use both when an automation could make an internal process faster while making the user's experience worse.

## Model meaning, not screen clicks

Name tasks with a verb and object: "Validate required fields," not "Spreadsheet." Give every exclusive gateway a question and label outgoing conditions: "Required evidence complete?" with "yes" and "no."

Keep these distinctions:

- **Task versus wait:** five minutes of work followed by two days awaiting approval are different elements.
- **Error versus business outcome:** an invalid invoice is an expected outcome; a database timeout is a system failure.
- **Sequence versus message:** another organization does not become your internal lane merely because you email it.
- **Current versus future state:** never blend them into one diagram. The gap is the evidence for change.

A large diagram is not automatically a better one. Start with 7-12 high-level activities, then expand only the risky or confusing subprocess.

## Replay as validation

Select three synthetic cases:

1. a normal case that should finish successfully;
2. an incomplete or invalid case;
3. a system failure or unavailable approver.

Place a token at the start and move it along the diagram. At each gateway, the available evidence must determine exactly one route, unless parallel work is intended. If you need spoken knowledge not present on the map, annotate the missing rule. If the token gets stuck, the process has an unresolved state.

## Free local practice

Use paper, [diagrams.net](https://www.diagrams.net/), or the free BPMN editor at [bpmn.io](https://demo.bpmn.io/). Map the process from the previous lesson.

1. Create lanes for the requester, operator, and system. Add an external participant only if one exists.
2. Add one explicit start event and at least three named end states: completed, rejected, and needs review.
3. Add tasks and gateways for the normal path.
4. Add a timer or error path for one operational failure.
5. Under the diagram, create a blueprint table:

| stage | user action | visible interaction | backstage action | system/evidence | pain point |
| --- | --- | --- | --- | --- | --- |
| Submit | Sends file | Confirmation | Queue created | Message ID | No expected response time |

6. Replay the three cases and maintain a correction log.
7. Export the diagram as SVG or PNG, but keep the editable source. Synthetic data only.

The expected artifact is not a beautiful diagram. It is a falsifiable model: a colleague can point to a missing route or a wrongly assigned responsibility.

## Completion criteria

You are finished when:

- every activity has a responsible lane and verb-object name;
- every gateway states a question and every route states a condition;
- waiting and active work are visibly different;
- success, expected rejection, human review, and technical failure can all terminate safely;
- the service blueprint includes the user-facing and backstage views;
- three case replays complete without relying on undocumented rules;
- current-state and proposed future-state elements are not mixed.

## References

- [Object Management Group: BPMN 2.0 specification](https://www.omg.org/spec/BPMN/2.0/About-BPMN) - normative notation specification and machine-readable schemas.
- [BPMN.io online modeler](https://demo.bpmn.io/) - free browser-based editor from the maintainers of the open-source BPMN toolkit.
- [GOV.UK Service Manual: Creating an experience map](https://www.gov.uk/service-manual/user-research/creating-an-experience-map) - public method for aligning stages, actions, touchpoints, and user needs.
- [GOV.UK Service Manual: Researching user experiences](https://www.gov.uk/service-manual/user-research/researching-user-experiences) - guidance for gathering the evidence behind a journey map.
