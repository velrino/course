# Relational Modeling and Constraints

## Learning objectives

- Translate business facts into tables, keys, relationships, and constraints.
- Use normalization to prevent update, insertion, and deletion anomalies.
- Make the database reject invalid states even when application code fails.

## Model facts and invariants

A table represents one kind of fact; a row is one occurrence; a key identifies it. Choose stable surrogate primary keys when natural identifiers can change, but preserve business uniqueness with `UNIQUE` constraints. A foreign key states that a reference must exist. `NOT NULL`, `CHECK`, and exclusion constraints express further invariants close to the data.

For an order system, storing customer email, product name, and current price on every line causes anomalies. Customer email belongs to `customers`; product catalog data belongs to `products`; order-time unit price belongs to `order_items` because it is a historical fact. Many-to-many relationships use a junction table whose foreign keys and unique key define allowed pairs.

Normalization is a reasoning tool, not a mandate to split every column. First normal form uses atomic values suitable for the domain. In third normal form, non-key facts depend on the key, the whole key, and not another non-key fact. Denormalize only for measured needs, with a defined source of truth and synchronization rule.

Represent states explicitly. Use a constrained text value or reference table for a changing status vocabulary. Store timestamps with time zone for real instants. Avoid comma-separated IDs and polymorphic foreign keys that the database cannot enforce. Define deletion behavior deliberately: `RESTRICT`, `CASCADE`, or `SET NULL` describes business lifecycle, not convenience.

## Free local practice

Model a small course platform with students, courses, offerings, enrollments, lessons, and submissions. Write a glossary and at least ten invariants before SQL, such as "a student enrolls at most once per offering" and "score is between 0 and 100 or unknown."

Implement the schema in SQLite for zero-install practice or PostgreSQL locally. Enable foreign-key enforcement in SQLite. Include primary/foreign keys, `NOT NULL`, `UNIQUE`, `CHECK`, defaults only where semantically valid, and explicit delete actions.

Insert a valid dataset, then attempt violations: duplicate enrollment, missing student, score 120, null required title, and deletion of an offering with enrollments. Record which constraint rejects each case. Draw the functional dependencies and explain one normalization decision and one consciously derived field you did **not** store.

## Completion criteria

- Every table represents one stated kind of fact and has a stable key.
- At least ten business invariants are enforced or documented as application-only with a reason.
- Invalid inserts/deletes fail in the database, not only in UI validation.
- Delete behavior and historical facts such as submission score are intentional.

## References

- [PostgreSQL table constraints](https://www.postgresql.org/docs/current/ddl-constraints.html) - primary, unique, check, exclusion, and foreign-key constraints.
- [PostgreSQL data definition](https://www.postgresql.org/docs/current/ddl.html) - tables, defaults, generated columns, privileges, and schemas.
- [SQLite foreign keys](https://www.sqlite.org/foreignkeys.html) - enabling and enforcing referential integrity locally.
- [Codd, A Relational Model of Data for Large Shared Data Banks](https://doi.org/10.1145/362384.362685) - original relational-model paper.
