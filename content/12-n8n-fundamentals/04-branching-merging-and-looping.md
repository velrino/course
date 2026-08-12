# Branching, Merging, and Looping

## Learning objectives

By the end of this lesson, you can:

- implement exclusive and multi-way routing from a decision table;
- merge branches without confusing synchronization with data combination;
- process bounded batches while preserving per-item identity;
- test execution order and partial failure explicitly.

## Branches express policy

Use If for a binary decision and Switch for multiple named routes. Translate a reviewed decision table directly; avoid burying authorization or eligibility rules inside a long expression no one can audit.

Every route needs a destination. Add an otherwise/unknown path for unexpected values and stop safely. When several conditions could match, decide whether exactly one or multiple routes should execute and configure the node accordingly.

## Merge has several meanings

Before adding a Merge node, state which behavior you need:

- wait for branches before continuing;
- append items from both branches;
- combine matching records by a stable key;
- combine by position only when ordering and cardinality are guaranteed;
- choose one available input.

Position-based combination is fragile after filtering or asynchronous work. Prefer a case ID and verify cardinality. A join that produces zero or multiple matches should follow an explicit exception policy.

## Bounded loops and batches

Many nodes already process all incoming items, so a visible loop is not always required. Use Loop Over Items when you need batches, rate control, or a subgraph executed per batch.

Define:

- total item or page limit;
- batch size;
- continue condition;
- retry behavior;
- per-item versus batch failure policy;
- deduplication and correlation key.

A loop must progress. For pagination, require the next cursor to change and stop when it is absent or the maximum page count is reached.

## Free local practice

Build a workflow from ten synthetic case items.

1. Use Switch to route priority into urgent, standard, and invalid.
2. In each valid branch, set a service_level field.
3. Merge valid results by appending them; keep invalid records on a separate review route.
4. Add a local owner lookup dataset and merge it by owner_id. Route zero-match and multi-match results safely.
5. Process valid records in batches of three with Loop Over Items.
6. Within the loop, calculate a batch_index and retain case_id.
7. Simulate one invalid item. Test and record whether the design continues other items or stops the batch.
8. Verify the final valid count, invalid count, unique case IDs, and absence of duplicates.
9. Run the same workflow twice and compare ordered output.

## Completion criteria

You are finished when:

- Switch routes trace to a written decision table;
- unexpected values have a safe explicit route;
- the Merge mode is documented in business terms;
- joins use stable keys and handle zero/multiple matches;
- loop progress, maximum, and batch size are explicit;
- every item retains case_id across branches and merge;
- one bad item follows the intended isolation or atomicity policy;
- counts and identities reconcile at the end.

## References

- [n8n documentation: Splitting with conditionals](https://docs.n8n.io/flow-logic/splitting/) - official If and Switch branching concepts.
- [n8n documentation: Merging data](https://docs.n8n.io/flow-logic/merging/) - official Merge behaviors and data-combination concepts.
- [n8n documentation: Looping](https://docs.n8n.io/flow-logic/looping/) - official guidance on automatic item processing and explicit loops.
- [n8n documentation: Execution order](https://docs.n8n.io/flow-logic/execution-order/) - official multi-branch execution semantics.
