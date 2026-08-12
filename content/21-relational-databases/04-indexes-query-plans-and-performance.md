# Indexes, Query Plans, and Performance

## Learning objectives

- Read `EXPLAIN` plans and distinguish estimates from measured execution.
- Design indexes from query predicates, joins, ordering, and selectivity.
- Measure performance without compromising correctness or write operations.

## An index is a maintained data structure

Indexes can reduce reads but consume storage, slow writes, and require maintenance. Start with a slow, important query and representative data. Capture its SQL, parameters, result count, plan, timing distribution, and correctness. Do not add indexes from column names alone.

PostgreSQL `EXPLAIN` shows planner estimates; `EXPLAIN (ANALYZE, BUFFERS)` executes the query and reports actual rows/times and buffer activity. Use it only when executing the statement is safe. Large differences between estimated and actual rows suggest stale statistics, correlated columns, skew, or a predicate the planner cannot estimate well.

B-tree indexes support equality, ranges, and ordered access. A composite index is ordered by its leading columns, so column order follows query patterns. Partial indexes cover rows satisfying a stable predicate; expression indexes cover computed predicates; unique indexes enforce invariants. Foreign-key referencing columns are not automatically indexed by PostgreSQL and often need an index for joins/deletes.

Avoid wrapping an indexed column in an unmatched function, leading-wildcard searches, implicit type casts, and fetching unnecessary columns. Still, a sequential scan can be correct and faster for much of a small table. The goal is not "use an index"; it is predictable resource use and response time.

## Free local practice

Generate at least 100,000 submissions with skew: most old, a small active subset, and a few large offerings. Use PostgreSQL if available; SQLite's `EXPLAIN QUERY PLAN` is a lighter alternative.

Choose three queries: latest attempts for one offering, ungraded submissions, and student history ordered by time. Capture plans and median/p95 times over repeated runs. Add candidate indexes one at a time, rerun, and record read improvement plus insert cost and index size.

Test a composite index and reverse its column order. Create a partial index for ungraded rows if the predicate is stable. Run `ANALYZE` and compare row estimates. Remove any index that is redundant or does not improve the defined workload.

## Completion criteria

- Baseline and final plans, parameters, data distribution, and timings are preserved.
- Index choices reference actual predicates/order/joins and explain column order.
- Write/storage cost and redundant indexes are considered.
- Query results are proven unchanged after every performance modification.

## References

- [PostgreSQL using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html) - plan nodes, estimates, actual execution, and buffers.
- [PostgreSQL index types](https://www.postgresql.org/docs/current/indexes-types.html) - B-tree, hash, GiST, SP-GiST, GIN, and BRIN uses.
- [PostgreSQL multicolumn indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html) - leading-column behavior and skip scans.
- [PostgreSQL partial indexes](https://www.postgresql.org/docs/current/indexes-partial.html) - predicate-specific index design and limitations.
- [SQLite query planner](https://www.sqlite.org/queryplanner.html) - accessible explanation of search, sorting, and multi-column indexes.
