# 12. n8n Fundamentals

Build and inspect local n8n workflows using triggers, nodes, items, expressions, branching, merging, loops, webhooks, execution history, and error workflows. The goal is controlled data flow with evidence at every boundary.

## Before you begin

Complete [Module 11](../11-algorithms-for-automation/index.md). You should understand JSON and HTTP from [Module 06](../06-web-apis-and-webhooks/index.md) and be able to run n8n locally.

## Lessons

1. [Local Installation and the Editor](01-local-installation-and-editor-tour.md)
2. [Triggers, Nodes, and a First Workflow](02-triggers-nodes-and-first-workflow.md)
3. [Items, Expressions, and Data Mapping](03-items-expressions-and-data-mapping.md)
4. [Branching, Merging, and Looping](04-branching-merging-and-looping.md)
5. [Webhooks, Executions, and Error Workflows](05-webhooks-executions-and-error-workflows.md)

## Suggested artifact

Export a local workflow that validates webhook input, maps multiple items, takes success and failure branches, handles an empty collection, records a correlation ID, and routes terminal failures to an error workflow.

## Practice lab

[n8n Order Triage](https://github.com/velrino/course/tree/master/labs/n8n-order-triage) supplies an importable workflow and representative local inputs.

## Continue

Make the workflow reusable and operational in [Module 13: Advanced n8n and Integrations](../13-advanced-n8n-and-integrations/index.md).
