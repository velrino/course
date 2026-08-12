# Transactions, Concurrency, and Idempotency

## Learning objectives

- Use transactions to preserve multi-statement invariants.
- Explain isolation anomalies, locks, deadlocks, and retry requirements.
- Make repeated application requests safe through database constraints.

## Correct alone is not correct concurrently

A transaction groups statements into one atomic outcome: commit all or roll back all. Keep transactions short and avoid user/network waits while holding locks. Put constraints in the database because two application processes can both pass a "check then insert" test before either writes.

Isolation levels define which concurrent effects are visible. PostgreSQL's default `READ COMMITTED` gives each statement a new snapshot; a read followed by a write may observe changed data. `REPEATABLE READ` provides a stable transaction snapshot but may abort conflicting transactions. `SERIALIZABLE` aims to behave like some serial order and requires applications to retry serialization failures. Row locks such as `SELECT ... FOR UPDATE` can coordinate updates, but lock order matters; inconsistent order can deadlock, and PostgreSQL aborts one participant.

Idempotency turns repeated logical requests into one result. Store a client-provided key with a request hash and outcome under a unique constraint. If the same key arrives with the same hash, return the prior outcome; with different content, reject it. This is stronger than checking whether a similar row "probably" exists.

PostgreSQL `INSERT ... ON CONFLICT` supports atomic upsert patterns, but define whether update-on-conflict is actually correct. For money or audit events, immutable append plus uniqueness is often safer than overwrite.

## Free local practice

Add `seat_limit` to offerings and write an enrollment transaction that must never exceed it. Open two database sessions and pause them between count/check and insert to reproduce an oversubscription race. Then fix it using an atomic design: lock the offering row before checking, or maintain a counter updated with a conditional statement and constraints.

Create an `idempotency_requests` table with unique key, request hash, status, and serialized result. Simulate two concurrent clients using the same key. Verify one enrollment and consistent responses. Repeat with the same key but different request data and require rejection.

In PostgreSQL, deliberately lock two rows in opposite order from two sessions to observe deadlock handling. Write pseudocode or Python that retries only serialization/deadlock failures with bounded backoff; authorization and constraint failures are terminal.

## Completion criteria

- A reproduced race demonstrates why application-only checking fails.
- The corrected transaction cannot exceed the seat limit under two concurrent clients.
- An idempotency key is bound to request content and stored result.
- Retry logic is bounded and restricted to explicitly transient transaction errors.

## References

- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html) - snapshots, anomalies, and isolation guarantees.
- [PostgreSQL explicit locking](https://www.postgresql.org/docs/current/explicit-locking.html) - table/row locks, deadlocks, and advisory locks.
- [PostgreSQL INSERT](https://www.postgresql.org/docs/current/sql-insert.html) - `ON CONFLICT` behavior and atomic alternatives.
- [Psycopg transaction management](https://www.psycopg.org/psycopg3/docs/basic/transactions.html) - Python commit, rollback, contexts, and retry implications.
- [SQLite transactions](https://www.sqlite.org/lang_transaction.html) - local concurrency and single-writer semantics.
