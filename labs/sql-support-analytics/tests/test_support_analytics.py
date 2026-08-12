from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest


LAB = Path(__file__).resolve().parents[1]
IMPLEMENTATION = os.environ.get("SQL_ANALYTICS_IMPL", "solution")
MODULE_PATH = LAB / IMPLEMENTATION / "support_analytics.py"
SPEC = importlib.util.spec_from_file_location("support_analytics_under_test", MODULE_PATH)
assert SPEC and SPEC.loader
analytics = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analytics)


class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temporary.name) / "support.db"
        self.connection = analytics.connect(self.db_path)
        analytics.initialize_database(self.connection, LAB / "fixtures")

    def tearDown(self):
        try:
            self.connection.close()
        finally:
            self.temporary.cleanup()


class ReportTests(DatabaseTestCase):
    def test_report_matches_golden_file(self):
        expected = json.loads((LAB / "fixtures" / "expected-report.json").read_text())
        self.assertEqual(analytics.build_report(self.connection), expected)

    def test_timeline_uses_lag_and_cumulative_sum(self):
        timeline = analytics.ticket_timeline(self.connection, "T001")
        self.assertEqual([row["cumulative_minutes"] for row in timeline], [0, 20, 45])
        self.assertIsNone(timeline[0]["previous_event_at"])
        self.assertEqual(timeline[1]["previous_event_at"], "2026-01-02T09:00:00")

    def test_query_plan_uses_the_composite_index(self):
        plan = analytics.query_plan(self.connection)
        self.assertTrue(
            any("idx_tickets_status_priority" in detail for detail in plan),
            f"unexpected plan: {plan}",
        )


class ConstraintTests(DatabaseTestCase):
    def test_rejects_an_unknown_customer(self):
        values = ("T099", "C999", None, "low", "open", "Invalid", "2026-01-05", None)
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute("INSERT INTO tickets VALUES (?,?,?,?,?,?,?,?)", values)

    def test_rejects_an_invalid_priority(self):
        values = ("T099", "C001", None, "urgent", "open", "Invalid", "2026-01-05", None)
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute("INSERT INTO tickets VALUES (?,?,?,?,?,?,?,?)", values)

    def test_rejects_negative_event_minutes(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                """INSERT INTO ticket_events
                   (ticket_id,event_type,actor,occurred_at,minutes_spent)
                   VALUES ('T002','updated','Sam','2026-01-05T12:00:00',-1)"""
            )


class TransactionTests(DatabaseTestCase):
    def test_resolution_updates_ticket_and_appends_event(self):
        analytics.resolve_ticket(
            self.connection, "T002", "A003", "2026-01-05T16:00:00", 35
        )
        ticket = self.connection.execute(
            "SELECT status, assigned_agent_id, resolved_at FROM tickets WHERE ticket_id='T002'"
        ).fetchone()
        self.assertEqual(tuple(ticket), ("resolved", "A003", "2026-01-05T16:00:00"))
        last = analytics.ticket_timeline(self.connection, "T002")[-1]
        self.assertEqual((last["event_type"], last["minutes_spent"]), ("resolved", 35))

    def test_failed_event_rolls_back_ticket_update(self):
        with self.assertRaises(sqlite3.IntegrityError):
            analytics.resolve_ticket(
                self.connection, "T002", "A003", "2026-01-05T16:00:00", -10
            )
        ticket = self.connection.execute(
            "SELECT status, resolved_at FROM tickets WHERE ticket_id='T002'"
        ).fetchone()
        self.assertEqual(tuple(ticket), ("open", None))
        count = self.connection.execute(
            "SELECT COUNT(*) FROM ticket_events WHERE ticket_id='T002' AND event_type='resolved'"
        ).fetchone()[0]
        self.assertEqual(count, 0)

    def test_missing_ticket_is_a_clear_failure(self):
        with self.assertRaisesRegex(LookupError, "does not exist"):
            analytics.resolve_ticket(
                self.connection, "T999", "A003", "2026-01-05T16:00:00", 10
            )


if __name__ == "__main__":
    unittest.main()
