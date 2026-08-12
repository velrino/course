# Python, PostgreSQL Security, and Operations

## Learning objectives

- Use Psycopg safely with parameters, transactions, and connection lifecycle.
- Apply roles, privileges, row-level security, migrations, backup, and restore testing.
- Deliver a database-backed automation capstone.

## Safe application access

Pass values separately from SQL text:

```python
cur.execute(
    "SELECT id, score FROM submissions WHERE student_id = %s",
    (student_id,),
)
```

Never quote the placeholder or interpolate strings. Values and SQL identifiers are different; if a table/column must be dynamic, choose it from a fixed allowlist and compose with `psycopg.sql.Identifier`. A model-generated SQL string is untrusted and should not receive a privileged connection.

Use connection and transaction context managers deliberately. Psycopg begins transactions even for ordinary queries by default; long "idle in transaction" sessions hold resources. Configure statement and lock timeouts and use a bounded pool for services. Avoid a pool for a short one-shot script unless measurement justifies it.

Create separate owner/migration and runtime roles. Revoke broad defaults and grant only required schema/table/sequence/function privileges. Row-level security can enforce per-row policies but does not replace correct roles, and table owners normally bypass it unless forced. Test policies with the actual runtime role.

Schema changes need versioned migrations, backward-compatible deployment order, and rollback/forward-fix plans. Backups are only credible after a restore test. Record recovery point/time objectives, retention, encryption, access, and a scheduled restore exercise.

## Free local practice

Run PostgreSQL locally with an existing installation or official container. Build a Python CLI for enrollments and submissions using Psycopg 3. Add migrations for the course schema and two roles: `course_owner` and least-privileged `course_app`.

Implement parameterized CRUD, the seat-limit transaction, idempotency keys, statement timeout, structured error mapping, and a small connection pool only if running a long-lived API. Test SQL-injection strings as data, permission denial for schema changes, rollback after a failed second statement, and cross-student access. Optionally add row-level security keyed by a transaction-local setting, then test missing/malicious settings.

Create a logical backup with `pg_dump`, restore it into a separate empty database, run row counts and integrity queries, and record duration. Never treat a backup command's exit code alone as restore evidence.

## Completion criteria

- All values are parameterized and dynamic identifiers come from an allowlist.
- Runtime credentials cannot migrate schema or access unrelated records.
- Transaction/error behavior is tested with the actual application role.
- A separate restored database passes documented integrity checks and recovery timing is recorded.

## References

- [Psycopg basic usage](https://www.psycopg.org/psycopg3/docs/basic/usage.html) - connections, cursors, parameters, and contexts.
- [Psycopg SQL parameters](https://www.psycopg.org/psycopg3/docs/basic/params.html) - safe values and identifier composition.
- [PostgreSQL privileges](https://www.postgresql.org/docs/current/ddl-priv.html) - object ownership, grants, and revocation.
- [PostgreSQL row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) - policies, default deny, owners, and enforcement.
- [PostgreSQL backup and restore](https://www.postgresql.org/docs/current/backup.html) - SQL dumps, filesystem backups, and continuous archiving.
