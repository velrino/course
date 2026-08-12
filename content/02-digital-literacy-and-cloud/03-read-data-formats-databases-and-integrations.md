# Read Data Formats, Databases, and Integrations

## Learning objectives

By the end of this lesson, you will be able to:

- distinguish syntax, schema, and semantics;
- choose between common tabular, document, and relational representations;
- identify keys and relationships in a small data model; and
- describe an integration as a contract across a boundary.

## Data has more than a format

Syntax answers "can a parser read these bytes?" Schema answers "does the structure contain the expected fields and types?" Semantics answers "do the values mean what the producer and consumer think they mean?"

This JSON is syntactically valid but may still be wrong:

```json
{"customer_id":"42","total":"free","currency":"BRL"}
```

If the contract requires `total` to be a non-negative number, validation must reject it. If `customer_id` is a string by design, converting it to a number could also be a bug. Preserve identifiers as identifiers; do not assume every digit sequence is arithmetic data.

Common representations have different strengths:

- **CSV:** compact tables, but conventions for types, delimiters, encodings, and nested data need agreement.
- **JSON:** nested objects, arrays, strings, numbers, booleans, and null; common at API boundaries.
- **Markdown:** human-readable structured prose, not a reliable general-purpose application data format.
- **Relational tables:** rows constrained by a schema, with keys and relationships queried through SQL.

## Relational foundations

A table models one kind of entity or relationship. A primary key uniquely identifies a row. A foreign key references a key in another table and can enforce referential integrity.

```sql
CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customers(id),
  total_cents INTEGER NOT NULL CHECK (total_cents >= 0)
);
```

The database can enforce structural rules, but it cannot decide every business meaning. Whether a refund is allowed still belongs to application policy.

## An integration is a contract

An integration moves information or commands between components. Document:

- producer and consumer;
- transport and endpoint;
- authentication and authorization;
- request and response schema;
- timeouts, retries, and rate limits;
- duplicate and out-of-order behavior;
- error ownership; and
- sensitive fields and retention.

The happy path is only one case. A reliable integration makes failure behavior explicit.

## Free local practice

Python includes SQLite. Create a local database without installing a server:

```bash
python3 - <<'PY'
import sqlite3

db = sqlite3.connect("learning.db")
db.execute("PRAGMA foreign_keys = ON")
db.execute("CREATE TABLE IF NOT EXISTS topics (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS reviews (topic_id INTEGER REFERENCES topics(id), reviewed_on TEXT NOT NULL, score INTEGER CHECK(score BETWEEN 0 AND 3))")
db.execute("INSERT OR IGNORE INTO topics(name) VALUES (?)", ("HTTP",))
db.execute("INSERT INTO reviews(topic_id, reviewed_on, score) SELECT id, date('now'), 2 FROM topics WHERE name = ?", ("HTTP",))
for row in db.execute("SELECT topics.name, reviews.reviewed_on, reviews.score FROM reviews JOIN topics ON topics.id = reviews.topic_id"):
    print(row)
db.commit()
PY
```

Draw the tables, keys, and relationship. Then create a JSON representation of the printed row. List one syntactic, one schema, and one semantic validation for that JSON.

## Completion criteria

- [ ] You can give a different failure example for syntax, schema, and semantics.
- [ ] You identified the primary and foreign keys in the practice database.
- [ ] You executed a parameterized query rather than concatenating input into SQL.
- [ ] Your integration checklist includes failure, duplication, and sensitive-data handling.

## References

- [RFC 8259: The JavaScript Object Notation Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259) - normative JSON syntax and interoperability guidance.
- [SQLite Documentation](https://www.sqlite.org/docs.html) - official, free documentation for an embedded public-domain relational database.
- [SQLite Foreign Key Support](https://www.sqlite.org/foreignkeys.html) - official explanation of enabling and enforcing relationships.
- [OWASP Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html) - defensive guidance for treating external data as data rather than executable syntax.

## Continue

Next: [Build a Cloud Mental Model](04-build-a-cloud-mental-model.md)
