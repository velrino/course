# 18. Monitoring, Evaluation, and Optimization

Connect traces, logs, and metrics to reproducible evaluation sets and release decisions. The module defines task, retrieval, tool, agent, safety, cost, and latency measures, then uses controlled experiments and production gates to prevent intuition-driven optimization.

## Before you begin

Complete [Module 17](../17-security-privacy-and-lgpd/index.md) and bring a bounded system with known failure modes. You need representative synthetic cases and a deterministic baseline.

## Lessons

1. [Observability for AI Workflows](01-observability-for-ai-workflows.md)
2. [Building Reproducible Evaluation Sets](02-building-reproducible-evaluation-sets.md)
3. [Evaluating RAG, Tools, and Agents](03-evaluating-rag-tools-and-agents.md)
4. [Experiment Design and Optimization](04-experiment-design-and-optimization.md)
5. [Production Monitoring and Release Gates](05-production-monitoring-and-release-gates.md)

## Suggested artifact

Create a versioned evaluation set, trace schema, baseline/candidate comparison, confidence and slice analysis, quality-safety-latency dashboard, explicit release gate, canary plan, alerts, and rollback evidence.

## Practice lab

[RAG Grounded Search](https://github.com/velrino/course/tree/master/labs/rag-grounded-search) supplies a concrete system for retrieval, grounding, latency, and regression evaluation.

## Continue

Use these evaluation disciplines before adding coordinating agents in [Module 19: Multi-Agent Orchestration](../19-multi-agent-orchestration/index.md).
