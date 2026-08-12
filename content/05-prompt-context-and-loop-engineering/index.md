# 05. Prompt, Context, and Loop Engineering

Treat model interaction as a testable system contract. The module covers instructions, examples, structured output, context selection, retrieval, memory, tools, human checkpoints, stop conditions, and repeatable evaluation harnesses.

## Before you begin

Complete [Module 04](../04-llms-and-generative-ai/index.md) and bring one bounded task with examples of acceptable and unacceptable outputs. Local or deterministic model substitutes are sufficient.

## Lessons

1. [Write Clear Prompt Contracts](01-write-clear-prompt-contracts.md)
2. [Use Examples and Structured Outputs](02-use-examples-and-structured-outputs.md)
3. [Engineer Context, Retrieval, and Memory](03-engineer-context-retrieval-and-memory.md)
4. [Design Bounded Tool and Human Loops](04-design-bounded-tool-and-human-loops.md)
5. [Build Harnesses and Evaluation Loops](05-build-harnesses-and-evaluation-loops.md)

## Suggested artifact

Build a versioned prompt-and-context harness with a schema validator, at least ten representative cases, failure labels, a baseline, bounded retries, and an evaluation report that supports a release decision.

## Continue

Learn the transport contracts used by tools and automations in [Module 06: Web, APIs, and Webhooks](../06-web-apis-and-webhooks/index.md).
