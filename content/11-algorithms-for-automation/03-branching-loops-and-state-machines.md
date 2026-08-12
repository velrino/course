# Branching, Loops, and State Machines

## Learning objectives

By the end of this lesson, you can:

- implement decision tables without overlapping or unreachable branches;
- choose bounded iteration, queue processing, or state transitions appropriately;
- model long-running work as an explicit finite-state machine;
- prevent infinite loops and illegal transitions.

## Branches must be complete and exclusive

Write a decision table before nested conditions. For each combination, specify an outcome or declare it impossible with evidence. Order matters when rules overlap:

~~~text
if unauthorized: reject
else if invalid: needs_review
else if duplicate: return_previous_result
else if high_consequence: await_approval
else: process
~~~

Security and validity checks precede convenience rules. A duplicate response must not reveal a previous result to an unauthorized caller.

Test branch boundaries: exactly at a threshold, just below, just above, missing, and wrong type. Avoid truthiness when zero, an empty list, or false are legitimate inputs.

## Pick the right repetition model

- Use a **for loop** when iterating a finite collection.
- Use a **while loop** only with an explicit progress measure and upper bound.
- Use a **queue** when work arrives over time or needs retry scheduling.
- Use a **state machine** when a case pauses across external events.

For batch work, isolate failures. One malformed item should be routed to a reject collection rather than terminating all valid items, unless atomicity is a requirement.

## State machines make time visible

Define states and allowed transitions:

| current | event | guard | next | side effect |
| --- | --- | --- | --- | --- |
| received | validate | schema valid | ready | record validation |
| received | validate | invalid | needs_review | notify reviewer |
| ready | authorize | allowed | processing | reserve idempotency key |
| processing | success | reference present | completed | store reference |
| processing | transient_failure | attempts < 3 | retry_wait | schedule retry |
| retry_wait | timer | still authorized | processing | increment attempt |
| any open | cancel | caller authorized | cancelled | prevent future action |

Reject any transition not in the table. Never change state and perform an external side effect without defining what happens if only one succeeds.

## Free local practice

Create a local Python state-machine simulator using only dictionaries and functions.

1. Encode allowed transitions as data, not a long chain of unrelated conditionals.
2. Accept a list of synthetic events containing case ID, event type, and timestamp.
3. Start every new case at received.
4. Reject events that are illegal in the current state and record why.
5. Add a maximum of three retries and a terminal failed_safe state.
6. Process a batch in which one case completes, one needs review, one is cancelled, one receives an illegal event, and one exhausts retries.
7. Print a transition log:

~~~text
case-04 | processing | transient_failure | retry_wait | attempt=2
~~~

8. Replay the same event stream. The resulting states and log must match exactly.

## Completion criteria

You are finished when:

- decision-table rows are complete, ordered, and tested at boundaries;
- authorization is checked before disclosing duplicate results;
- all loops have finite input or a progress measure and maximum;
- one bad batch item follows a documented policy;
- every state transition has an event, guard, next state, and effect;
- illegal transitions are rejected and logged;
- replaying identical events produces identical states;
- all cases reach a terminal or explicitly waiting state.

## References

- [Python Tutorial: More control flow tools](https://docs.python.org/3/tutorial/controlflow.html) - official behavior of if, for, while, match, break, and functions.
- [Python collections: deque](https://docs.python.org/3/library/collections.html#collections.deque) - official efficient queue and bounded-deque data type.
- [SCXML 1.0](https://www.w3.org/TR/scxml/) - W3C recommendation defining state-machine structure, events, transitions, and executable content.
- [GitHub Actions: Using jobs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-jobs) - official examples of dependencies, parallelism, conditional execution, and failure propagation.
