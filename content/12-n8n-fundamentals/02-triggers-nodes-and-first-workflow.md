# Triggers, Nodes, and a First Workflow

## Learning objectives

By the end of this lesson, you can:

- distinguish manual, scheduled, polling, and webhook triggers;
- configure, test, rename, and connect nodes;
- build a deterministic intake-and-validation workflow;
- inspect node-level inputs and outputs instead of debugging by guesswork.

## Read a workflow left to right

Every execution begins at a trigger. The choice encodes a delivery model:

- Manual Trigger is for development and controlled operations.
- Schedule Trigger creates time-based work and needs overlap/timezone policy.
- Polling triggers periodically ask a service for changes.
- Webhook and app event triggers react to inbound delivery and must handle duplicates.

Nodes receive zero or more **items**, process them, and emit zero or more items. Name nodes by behavior, such as Validate Required Fields, not Edit Fields 3. Clear names make expressions, execution logs, and incident response understandable.

## Build a narrow workflow

For a case intake:

~~~text
Manual Trigger
  -> Create Synthetic Cases
  -> Normalize Fields
  -> Validate Required Fields
  -> Route Validity
      -> valid
      -> needs review
~~~

Keep pure transformations before external actions. This lets you execute repeatedly without sending duplicate messages or changing another system.

Use pinned data carefully. Pinned output is convenient for developing downstream nodes, but it is an example, not evidence that live input is identical. Unpin and run end-to-end before considering a workflow ready.

## Node configuration discipline

For each node, record:

- expected item shape;
- operation and important parameters;
- expression inputs;
- output shape;
- failure policy;
- whether it performs a side effect.

Test one node at a time while building, then the full workflow. Inspect the execution path and actual JSON after every transformation. A green node means the node did not throw an error; it does not prove the business result is correct.

## Free local practice

1. Create a new workflow with a Manual Trigger.
2. Add an Edit Fields node that emits three synthetic cases. If one node cannot conveniently create the list, use a Code node returning items with case_id, status, and amount.
3. Add an Edit Fields or Code node that trims case_id and lowercases status while preserving the original fields.
4. Add an If node that checks case_id is nonempty and status is in an allowlist.
5. On the valid branch, set result_status to ready.
6. On the invalid branch, set result_status to needs_review and an error reason.
7. Give every node a verb-object name and add a note containing its contract.
8. Run cases for valid, missing ID, and unknown status; inspect each node output.
9. Save and export the workflow. Do not activate it.

## Completion criteria

You are finished when:

- the trigger choice and delivery assumptions are stated;
- at least three synthetic items take the expected branches;
- normalization preserves original evidence;
- no side-effect node exists in this first workflow;
- nodes have behavioral names and documented input/output expectations;
- individual-node and full-workflow tests both pass;
- pinned data is not mistaken for live end-to-end validation;
- the workflow is exported and remains inactive.

## References

- [n8n documentation: A very quick quickstart](https://docs.n8n.io/try-it-out/quickstart/) - official introduction to building and executing a workflow.
- [n8n documentation: Tutorial, build your first workflow](https://docs.n8n.io/try-it-out/tutorial-first-workflow/) - official guided workflow tutorial.
- [n8n documentation: Trigger nodes](https://docs.n8n.io/integrations/builtin/node-types/#trigger-nodes) - official distinction between trigger and action nodes.
- [n8n documentation: Manual Trigger](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.manualworkflowtrigger/) - official node behavior used for safe development.
