# From Process to Algorithm

## Learning objectives

By the end of this lesson, you can:

- translate a process path into inputs, outputs, rules, state, and side effects;
- separate deterministic decisions from human judgment and probabilistic suggestions;
- express an automation as pseudocode and a directed dependency graph;
- identify termination conditions before implementation.

## An algorithm is an executable contract

A process map describes who does what. An algorithm must remove enough ambiguity that a machine can execute the permitted portion. Define:

- **Input schema:** required fields, types, ranges, and source.
- **Output schema:** statuses and data returned on every path.
- **Pure rules:** transformations that do not change an external system.
- **State:** facts that persist across steps or retries.
- **Side effects:** email, database write, file creation, or API call.
- **Invariants:** truths that must always hold.
- **Termination:** a bounded end state for every path.

Example invariant: "A case can be marked completed only if validation passed and exactly one authorized external write was confirmed."

## Classify each decision

Use three categories:

1. **Deterministic:** the same valid input always gives the same result. Required-field checks and numeric thresholds belong here.
2. **Probabilistic advisory:** a model proposes a label or summary; schema and policy checks still govern action.
3. **Human judgment:** authority, ethics, ambiguity, or consequences require a named person.

Do not use an LLM to decide a rule that can be encoded and tested directly. Do not disguise a policy decision as a confidence threshold.

## Write pseudocode before nodes

~~~text
function handle(event):
    require event.id
    if already_processed(event.id):
        return previous_result(event.id)

    normalized = normalize(event.payload)
    errors = validate(normalized)
    if errors:
        record(event.id, "needs_review", errors)
        return result("needs_review", errors)

    if requires_human_decision(normalized):
        record(event.id, "awaiting_approval")
        return result("awaiting_approval")

    outcome = perform_authorized_action(normalized, event.id)
    record(event.id, "completed", outcome.reference)
    return result("completed", outcome.reference)
~~~

Notice that duplicate detection precedes the side effect, and every early exit returns a defined status.

## Dependency graphs

Represent steps as a directed acyclic graph when branches can run independently:

~~~text
receive -> normalize -> validate -> authorize -> write -> confirm
                         \-> audit_metadata -----^
~~~

Parallelize only independent work. If authorization requires normalized fields, it cannot precede normalization. If the workflow contains a cycle, specify what changes on each iteration and what stops it.

## Free local practice

Take the use-case specification from the previous module.

1. Create input and output tables with name, type, required status, example, and validation.
2. Mark every step P for pure computation or S for side effect.
3. Mark every decision D, P, or H for deterministic, probabilistic, or human.
4. Write pseudocode for all normal and exception paths.
5. List at least three invariants and one termination rule for each loop.
6. Draw a dependency graph and topologically order its nodes.
7. Replay the acceptance examples by hand. Record input, path, state change, side effect, and result.

Do not write production code yet. The output is a reviewable algorithm independent of n8n or another orchestrator.

## Completion criteria

You are finished when:

- every input and output has an explicit type and validation;
- pure rules, persistent state, and side effects are visibly separate;
- duplicate detection happens before irreversible or repeated action;
- deterministic, probabilistic, and human decisions are labeled;
- every path returns a documented status;
- every loop has progress and a maximum bound;
- all use-case acceptance examples can be replayed without inventing a rule.

## References

- [Python Tutorial: More control flow tools](https://docs.python.org/3/tutorial/controlflow.html) - official explanations of conditionals, loops, functions, and match statements.
- [Python Tutorial: Data structures](https://docs.python.org/3/tutorial/datastructures.html) - official coverage of lists, queues, sets, mappings, and iteration.
- [GitHub Actions: Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) - official example of dependency graphs, conditional execution, and job outputs in a production automation system.
- [IETF RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119) - primary vocabulary for distinguishing mandatory and optional algorithm requirements.
