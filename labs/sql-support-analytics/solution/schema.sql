PRAGMA foreign_keys = ON;

CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY CHECK (customer_id GLOB 'C[0-9][0-9][0-9]'),
    name TEXT NOT NULL CHECK (length(trim(name)) BETWEEN 1 AND 120),
    plan TEXT NOT NULL CHECK (plan IN ('starter', 'pro', 'enterprise')),
    created_at TEXT NOT NULL CHECK (created_at GLOB '????-??-??')
);

CREATE TABLE agents (
    agent_id TEXT PRIMARY KEY CHECK (agent_id GLOB 'A[0-9][0-9][0-9]'),
    name TEXT NOT NULL UNIQUE CHECK (length(trim(name)) BETWEEN 1 AND 120),
    team TEXT NOT NULL CHECK (length(trim(team)) BETWEEN 1 AND 80)
);

CREATE TABLE tickets (
    ticket_id TEXT PRIMARY KEY CHECK (ticket_id GLOB 'T[0-9][0-9][0-9]'),
    customer_id TEXT NOT NULL REFERENCES customers(customer_id),
    assigned_agent_id TEXT REFERENCES agents(agent_id),
    priority TEXT NOT NULL CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    status TEXT NOT NULL CHECK (status IN ('open', 'pending', 'resolved')),
    subject TEXT NOT NULL CHECK (length(trim(subject)) BETWEEN 1 AND 200),
    opened_at TEXT NOT NULL,
    resolved_at TEXT,
    CHECK (
        (status = 'resolved' AND resolved_at IS NOT NULL) OR
        (status IN ('open', 'pending') AND resolved_at IS NULL)
    ),
    CHECK (resolved_at IS NULL OR resolved_at >= opened_at)
);

CREATE TABLE ticket_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id TEXT NOT NULL REFERENCES tickets(ticket_id) ON DELETE CASCADE,
    event_type TEXT NOT NULL CHECK (
        event_type IN ('opened', 'assigned', 'investigated', 'updated', 'resolved')
    ),
    actor TEXT NOT NULL CHECK (length(trim(actor)) BETWEEN 1 AND 120),
    occurred_at TEXT NOT NULL,
    minutes_spent INTEGER NOT NULL DEFAULT 0 CHECK (minutes_spent BETWEEN 0 AND 1440)
);

CREATE INDEX idx_tickets_status_priority
    ON tickets(status, priority);
CREATE INDEX idx_tickets_customer
    ON tickets(customer_id);
CREATE INDEX idx_events_ticket_time
    ON ticket_events(ticket_id, occurred_at);
