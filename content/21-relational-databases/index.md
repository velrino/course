# 21. Relational Databases

Model valid relational states, query them with SQL, protect invariants through transactions, and reason about concurrency and idempotency. Index and query-plan analysis lead into secure Python/PostgreSQL operations.

## Before you begin

Complete [Module 20](../20-python-for-automation/index.md) or possess equivalent programming skill. Install SQLite for the early work; PostgreSQL is introduced where its operational behavior matters.

## Lessons

1. [Relational Modeling and Constraints](01-relational-modeling-and-constraints.md)
2. [SQL Queries, Joins, Aggregates, and Windows](02-sql-queries-joins-aggregates-and-windows.md)
3. [Transactions, Concurrency, and Idempotency](03-transactions-concurrency-and-idempotency.md)
4. [Indexes, Query Plans, and Performance](04-indexes-query-plans-and-performance.md)
5. [Python, PostgreSQL Security, and Operations](05-python-postgresql-security-and-operations.md)

## Suggested artifact

Create a migration-backed database for an automation queue with constraints, representative queries, transaction and duplicate-delivery tests, before/after query plans, least-privilege roles, backups, and a restore drill.

## Practice lab

[SQL Support Analytics](https://github.com/velrino/course/tree/master/labs/sql-support-analytics) provides a reproducible schema, seed data, queries, and verification path.

## Continue

Use governed data to answer measured questions in [Module 22: Data Analysis and Statistics](../22-data-analysis-and-statistics/index.md).
