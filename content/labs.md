# Executable Practice Labs

The seven labs turn selected lessons into small, testable systems. Each lab is intentionally local, uses synthetic fixtures, and has a learner workspace separate from the reference solution. Read the matching modules first; the labs are practice environments, not substitutes for the design and safety reasoning in the lessons.

## Lab map

| Lab | Preparation | What you build | Runtime |
|---|---|---|---|
| [Docker Health Stack](https://github.com/velrino/course/tree/master/labs/docker-health-stack) | Modules 06-07 | A health-checked local service stack with operational controls | Docker Compose |
| [MCP Task Server](https://github.com/velrino/course/tree/master/labs/mcp-task-server) | Modules 06 and 08 | A bounded task server with typed MCP tool contracts | Node.js |
| [n8n Order Triage](https://github.com/velrino/course/tree/master/labs/n8n-order-triage) | Modules 11-13 | An importable order workflow with validation and failure routing | n8n and Docker |
| [RAG Grounded Search](https://github.com/velrino/course/tree/master/labs/rag-grounded-search) | Modules 15 and 18 | A cited local retrieval path with evaluation cases | Python |
| [Python Invoice Audit](https://github.com/velrino/course/tree/master/labs/python-invoice-audit) | Module 20 | A validated invoice-audit CLI with automated tests | Python |
| [SQL Support Analytics](https://github.com/velrino/course/tree/master/labs/sql-support-analytics) | Module 21 | A support schema, seed data, analytical queries, and checks | SQLite |
| [Node Webhook Processor](https://github.com/velrino/course/tree/master/labs/node-webhook-processor) | Module 29 | A replay-safe asynchronous webhook processor | Node.js |

## Start, solve, and test

1. Open the lab's `README.md` and run its prerequisite checks before reading implementation files.
2. Work in the `starter/` area and commit your first attempt. Keep input fixtures unchanged so results remain comparable.
3. Run the documented test command after each small change. Read the assertion and observed output before changing code again.
4. Compare your finished behavior with `solution/` only after your own implementation passes, or when a written debugging hypothesis has stalled.
5. Rerun the complete lab test and the repository's lab test runner before recording completion.

The reference solution is one defensible implementation, not a line-by-line answer key. A different design is valid when it satisfies the same contracts, failure behavior, tests, and safety boundaries.

## Evidence standard

Keep a short evidence record for each completed lab:

- exact setup and test commands, runtime versions, and final exit status;
- a concise architecture or data-flow diagram;
- one normal-case result and at least one deliberate failure result;
- the tests you added or changed and what risk each test covers;
- one design decision, one limitation, and the next improvement you would measure;
- confirmation that committed fixtures contain no secrets or personal data.

Evidence should let another learner reproduce the result from a fresh checkout. Screenshots can supplement commands and machine-readable test output, but should not replace them.
