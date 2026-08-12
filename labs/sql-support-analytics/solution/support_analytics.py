#!/usr/bin/env python3
"""SQLite support analytics reference implementation."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sqlite3
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent

WORKLOAD_QUERY = """
SELECT COALESCE(a.name, 'Unassigned') AS agent,
       COUNT(*) AS open_tickets,
       SUM(CASE t.priority
             WHEN 'critical' THEN 4 WHEN 'high' THEN 3
             WHEN 'medium' THEN 2 ELSE 1 END) AS priority_points
FROM tickets AS t
LEFT JOIN agents AS a ON a.agent_id = t.assigned_agent_id
WHERE t.status IN ('open', 'pending')
GROUP BY COALESCE(a.name, 'Unassigned')
ORDER BY open_tickets DESC, agent
"""

CUSTOMER_SUMMARY_QUERY = """
WITH ticket_rollup AS (
    SELECT customer_id, COUNT(*) AS total_tickets,
           SUM(status = 'resolved') AS resolved_tickets,
           SUM(status <> 'resolved') AS open_tickets
    FROM tickets GROUP BY customer_id
),
event_rollup AS (
    SELECT t.customer_id, SUM(e.minutes_spent) AS support_minutes
    FROM tickets AS t JOIN ticket_events AS e ON e.ticket_id = t.ticket_id
    GROUP BY t.customer_id
)
SELECT c.customer_id, c.name, c.plan,
       COALESCE(tr.total_tickets, 0) AS total_tickets,
       COALESCE(tr.resolved_tickets, 0) AS resolved_tickets,
       COALESCE(tr.open_tickets, 0) AS open_tickets,
       COALESCE(er.support_minutes, 0) AS support_minutes
FROM customers AS c
LEFT JOIN ticket_rollup AS tr ON tr.customer_id = c.customer_id
LEFT JOIN event_rollup AS er ON er.customer_id = c.customer_id
ORDER BY c.customer_id
"""

SLA_QUERY = """
WITH durations AS (
    SELECT ticket_id, priority,
           ROUND((julianday(resolved_at) - julianday(opened_at)) * 24, 2)
             AS resolution_hours
    FROM tickets WHERE status = 'resolved'
)
SELECT ticket_id, priority, resolution_hours,
       ROW_NUMBER() OVER (
           PARTITION BY priority ORDER BY resolution_hours DESC, ticket_id
       ) AS slowest_rank
FROM durations
ORDER BY priority, slowest_rank
"""

TIMELINE_QUERY = """
SELECT event_id, event_type, occurred_at, minutes_spent,
       LAG(occurred_at) OVER (
           PARTITION BY ticket_id ORDER BY occurred_at, event_id
       ) AS previous_event_at,
       SUM(minutes_spent) OVER (
           PARTITION BY ticket_id ORDER BY occurred_at, event_id
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS cumulative_minutes
FROM ticket_events
WHERE ticket_id = ?
ORDER BY occurred_at, event_id
"""

PLAN_QUERY = "SELECT ticket_id FROM tickets WHERE status = 'open' AND priority = 'high'"


def connect(path: str | Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def _csv_rows(path: Path) -> Iterable[dict[str, str | None]]:
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            yield {key: (value if value != "" else None) for key, value in row.items()}


def initialize_database(connection: sqlite3.Connection, fixtures: Path) -> None:
    connection.executescript((HERE / "schema.sql").read_text(encoding="utf-8"))
    try:
        with connection:
            connection.executemany(
                "INSERT INTO customers VALUES (:customer_id, :name, :plan, :created_at)",
                _csv_rows(fixtures / "customers.csv"),
            )
            connection.executemany(
                "INSERT INTO agents VALUES (:agent_id, :name, :team)",
                _csv_rows(fixtures / "agents.csv"),
            )
            connection.executemany(
                """INSERT INTO tickets
                   (ticket_id, customer_id, assigned_agent_id, priority, status,
                    subject, opened_at, resolved_at)
                   VALUES (:ticket_id, :customer_id, :assigned_agent_id, :priority,
                           :status, :subject, :opened_at, :resolved_at)""",
                _csv_rows(fixtures / "tickets.csv"),
            )
            events = list(_csv_rows(fixtures / "ticket_events.csv"))
            for event in events:
                event["minutes_spent"] = int(event["minutes_spent"] or 0)
            connection.executemany(
                """INSERT INTO ticket_events
                   (ticket_id, event_type, actor, occurred_at, minutes_spent)
                   VALUES (:ticket_id, :event_type, :actor, :occurred_at, :minutes_spent)""",
                events,
            )
    except Exception:
        connection.rollback()
        raise


def _rows(connection: sqlite3.Connection, query: str, parameters: tuple[Any, ...] = ()):
    return [dict(row) for row in connection.execute(query, parameters)]


def build_report(connection: sqlite3.Connection) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "workload": _rows(connection, WORKLOAD_QUERY),
        "customer_summary": _rows(connection, CUSTOMER_SUMMARY_QUERY),
        "resolution_sla": _rows(connection, SLA_QUERY),
    }


def ticket_timeline(connection: sqlite3.Connection, ticket_id: str) -> list[dict[str, Any]]:
    return _rows(connection, TIMELINE_QUERY, (ticket_id,))


def resolve_ticket(
    connection: sqlite3.Connection,
    ticket_id: str,
    agent_id: str,
    resolved_at: str,
    minutes_spent: int,
) -> None:
    with connection:
        ticket = connection.execute(
            "SELECT status FROM tickets WHERE ticket_id = ?", (ticket_id,)
        ).fetchone()
        if ticket is None:
            raise LookupError(f"ticket {ticket_id} does not exist")
        if ticket["status"] == "resolved":
            raise ValueError(f"ticket {ticket_id} is already resolved")

        connection.execute(
            """UPDATE tickets
               SET status = 'resolved', assigned_agent_id = ?, resolved_at = ?
               WHERE ticket_id = ?""",
            (agent_id, resolved_at, ticket_id),
        )
        agent = connection.execute(
            "SELECT name FROM agents WHERE agent_id = ?", (agent_id,)
        ).fetchone()
        if agent is None:
            raise LookupError(f"agent {agent_id} does not exist")
        connection.execute(
            """INSERT INTO ticket_events
               (ticket_id, event_type, actor, occurred_at, minutes_spent)
               VALUES (?, 'resolved', ?, ?, ?)""",
            (ticket_id, agent["name"], resolved_at, minutes_spent),
        )


def query_plan(connection: sqlite3.Connection) -> list[str]:
    return [row[3] for row in connection.execute("EXPLAIN QUERY PLAN " + PLAN_QUERY)]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    setup = subparsers.add_parser("setup")
    setup.add_argument("--db", type=Path, required=True)
    setup.add_argument("--fixtures", type=Path, required=True)
    for command in ("report", "plan"):
        child = subparsers.add_parser(command)
        child.add_argument("--db", type=Path, required=True)
    resolve = subparsers.add_parser("resolve")
    resolve.add_argument("--db", type=Path, required=True)
    resolve.add_argument("--ticket", required=True)
    resolve.add_argument("--agent", required=True)
    resolve.add_argument("--resolved-at", required=True)
    resolve.add_argument("--minutes", type=int, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "setup" and args.db.exists():
        raise SystemExit(f"refusing to overwrite existing database: {args.db}")
    connection = connect(args.db)
    try:
        if args.command == "setup":
            initialize_database(connection, args.fixtures)
            print(json.dumps({"database": str(args.db), "status": "initialized"}))
        elif args.command == "report":
            print(json.dumps(build_report(connection), indent=2, sort_keys=True))
        elif args.command == "plan":
            print(json.dumps({"plan": query_plan(connection)}, indent=2))
        else:
            resolve_ticket(
                connection, args.ticket, args.agent, args.resolved_at, args.minutes
            )
            print(json.dumps({"status": "resolved", "ticket_id": args.ticket}))
    finally:
        connection.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
