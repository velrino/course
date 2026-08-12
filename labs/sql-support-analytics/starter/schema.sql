PRAGMA foreign_keys = OFF;

-- TODO: add keys, foreign keys, checks, and indexes that encode the domain.
CREATE TABLE customers (customer_id TEXT, name TEXT, plan TEXT, created_at TEXT);
CREATE TABLE agents (agent_id TEXT, name TEXT, team TEXT);
CREATE TABLE tickets (
    ticket_id TEXT, customer_id TEXT, assigned_agent_id TEXT, priority TEXT,
    status TEXT, subject TEXT, opened_at TEXT, resolved_at TEXT
);
CREATE TABLE ticket_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT, ticket_id TEXT, event_type TEXT,
    actor TEXT, occurred_at TEXT, minutes_spent INTEGER
);
