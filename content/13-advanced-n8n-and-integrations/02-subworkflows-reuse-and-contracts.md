# Subworkflows, Reuse, and Contracts

## Learning objectives

By the end of this lesson, you can:

- extract reusable behavior into an Execute Sub-workflow contract;
- distinguish code reuse from service or domain boundaries;
- version inputs and outputs without silently breaking callers;
- test a subworkflow separately and through its callers.

## Extract a capability, not arbitrary nodes

A useful subworkflow has one coherent responsibility, such as validate-case-v1, redact-log-record-v1, or call-catalog-with-retry-v1. Do not extract three nodes merely because they appear twice; extraction adds a dependency, execution boundary, permissions decision, and failure contract.

A subworkflow should define:

- name, owner, and version;
- input fields, types, required status, and data classification;
- output statuses and schemas;
- allowed side effects;
- timeout and failure behavior;
- idempotency expectations;
- compatibility and deprecation policy.

Keep policy-visible rules in named, reviewable workflows. Avoid a universal helper that changes behavior based on many flags; it becomes difficult to test and authorize.

## n8n execution model

The called workflow begins with Execute Sub-workflow Trigger. The caller uses Execute Sub-workflow and decides whether to wait for completion and how to pass items. Inspect the configured per-item/all-items behavior because it affects execution counts and side effects.

Treat the boundary like a function call:

~~~text
input:
  contract_version: "1"
  case_id: nonempty string
  payload: object

output:
  contract_version: "1"
  status: valid | needs_review
  reasons: array of reason codes
~~~

Reject unsupported contract versions. Preserve a correlation ID across the boundary.

## Change safely

Backward-compatible changes usually add an optional field or a new status that callers explicitly tolerate. Renaming a field, changing type, changing default, or introducing a side effect is breaking.

For a breaking change:

1. create a new version;
2. test old and new against shared fixtures;
3. migrate each caller;
4. observe error and outcome metrics;
5. disable the old version only after the usage inventory is empty;
6. retain a rollback/export until the review window closes.

## Free local practice

1. Extract normalization and validation from Module 12 into validate-case-v1.
2. Configure a typed input contract with contract_version, event_id, case_id, status, and amount.
3. Return only contract_version, event_id, case_id, result_status, and reason_codes.
4. Build two caller workflows: one processes one item; another sends a batch.
5. Test valid, missing, wrong type, unsupported version, and multiple-item cases.
6. Add an optional source_channel field without breaking callers.
7. Create a deliberate v2 breaking change in a copy, then document a migration rather than switching existing callers.
8. Build a usage table listing callers, owner, expected version, last tested date, and rollback export.

## Completion criteria

You are finished when:

- the subworkflow represents one named capability;
- input/output types, statuses, versions, side effects, and owner are explicit;
- unsupported versions fail safely with a reason code;
- correlation identity survives the call;
- single-item and batch behavior are both tested;
- an additive change preserves existing caller tests;
- a breaking change receives a new version and migration plan;
- callers and rollback artifacts are inventoried.

## References

- [n8n documentation: Sub-workflows](https://docs.n8n.io/flow-logic/subworkflows/) - official calling model, data passing, and execution behavior.
- [n8n documentation: Execute Sub-workflow node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflow/) - official caller configuration.
- [n8n documentation: Execute Sub-workflow Trigger](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflowtrigger/) - official input-definition and trigger behavior.
- [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) - public specification for communicating compatible and breaking changes.
