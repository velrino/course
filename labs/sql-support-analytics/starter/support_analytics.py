#!/usr/bin/env python3
"""Runnable but incomplete starter for the SQLite analytics lab."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sqlite3
from typing import Any


HERE = Path(__file__).resolve().parent
WORKLOAD_QUERY = "SELECT * FROM tickets WHERE status <> 'resolved'"
CUSTOMER_SUMMARY_QUERY = "SELECT * FROM customers"
SLA_QUERY = "SELECT * FROM tickets WHERE status = 'resolved'"
TIMELINE_QUERY = "SELECT * FROM ticket_events WHERE ticket_id = ? ORDER BY occurred_at"
PLAN_QUERY = "SELECT ticket_id FROM tickets WHERE status = 'open' AND priority = 'high'"


def connect(path: str | Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    # TODO: enforce foreign keys for every connection.
    return connection


def _read(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return [
            {key: (value if value != "" else None) for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def initialize_database(connection: sqlite3.Connection, fixtures: Path) -> None:
    connection.executescript((HERE / "schema.sql").read_text())
    connection.executemany(
        "INSERT INTO customers VALUES (:customer_id,:name,:plan,:created_at)",
        _read(fixtures / "customers.csv"),
    )
    connection.executemany(
        "INSERT INTO agents VALUES (:agent_id,:name,:team)", _read(fixtures / "agents.csv")
    )
    connection.executemany(
        "INSERT INTO tickets VALUES (:ticket_id,:customer_id,:assigned_agent_id,:priority,:status,:subject,:opened_at,:resolved_at)",
        _read(fixtures / "tickets.csv"),
    )
    connection.executemany(
        """INSERT INTO ticket_events
           (ticket_id,event_type,actor,occurred_at,minutes_spent)
           VALUES (:ticket_id,:event_type,:actor,:occurred_at,:minutes_spent)""",
        _read(fixtures / "ticket_events.csv"),
    )
    connection.commit()


def build_report(connection: sqlite3.Connection) -> dict[str, Any]:
    # TODO: implement joins, pre-aggregation, and SLA ranking.
    return {"schema_version": 1, "workload": [], "customer_summary": [], "resolution_sla": []}


def ticket_timeline(connection: sqlite3.Connection, ticket_id: str):
    # TODO: add LAG and a cumulative SUM window.
    return [dict(row) for row in connection.execute(TIMELINE_QUERY, (ticket_id,))]


def resolve_ticket(connection, ticket_id, agent_id, resolved_at, minutes_spent):
    # TODO: make the ticket update and event insert one validated transaction.
    connection.execute(
        "UPDATE tickets SET status='resolved', assigned_agent_id=?, resolved_at=? WHERE ticket_id=?",
        (agent_id, resolved_at, ticket_id),
    )
    connection.commit()


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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    connection = connect(args.db)
    try:
        if args.command == "setup":
            initialize_database(connection, args.fixtures)
            output = {"database": str(args.db), "status": "initialized"}
        elif args.command == "report":
            output = build_report(connection)
        else:
            output = {"plan": query_plan(connection)}
        print(json.dumps(output, indent=2, sort_keys=True))
    finally:
        connection.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
