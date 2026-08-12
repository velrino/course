# Executable Learning Labs

These labs turn the course concepts into small systems you can run, break, test, and explain without a paid API or private dataset.

## How to use the labs

1. Read the linked course modules before opening a solution.
2. Work in the lab's `starter/` directory and run its tests to establish a baseline.
3. Complete the tasks in the lab README one at a time.
4. Compare behavior and tests with `solution/` only after recording your own attempt.
5. Keep test output, design decisions, and one failure analysis as portfolio evidence.

Every fixture is synthetic and safe to publish. Do not replace it with employer, client, health, financial, identity, or other sensitive data.

## Lab route

| Lab | Course preparation | What you build | Runtime |
|---|---|---|---|
| [Python Invoice Audit](python-invoice-audit/) | Modules 11 and 20 | A validated, idempotent batch processor with structured logs | Python standard library |
| [SQL Support Analytics](sql-support-analytics/) | Modules 11 and 21 | A constrained relational model, analytical queries, transactions, and query-plan checks | Python and SQLite |
| [Grounded RAG Search](rag-grounded-search/) | Modules 15 and 18 | Deterministic retrieval with citations, access control, abstention, and evaluation | Python standard library |
| [Node.js Webhook Processor](node-webhook-processor/) | Modules 06, 11, and 29 | An authenticated, replay-safe webhook receiver with retries and idempotency | Node.js built-ins |
| [n8n Order Triage](n8n-order-triage/) | Modules 12 and 13 | An importable workflow with branching, error handling, and a static contract verifier | n8n plus Node.js verifier |
| [Docker Health Stack](docker-health-stack/) | Module 07 | A non-root, health-checked service stack with persistence and failure injection | Docker Compose plus static verifier |
| [MCP Task Server](mcp-task-server/) | Modules 08, 14, and 17 | A typed stdio MCP server with narrow tools, path boundaries, and a real SDK client test | Node.js and the official MCP SDK |

## Evidence standard

A lab is complete when you can provide:

- a passing test run from your implementation;
- one deliberately triggered failure and its diagnosis;
- a short explanation of the system boundary and trust boundary;
- a comparison with the supplied solution or baseline;
- one limitation and a concrete next experiment.

Use [`run-all-tests.py`](run-all-tests.py) from this directory after installing the MCP lab dependencies. The runner reports passed, failed, and intentionally skipped suites without hiding individual command output.
