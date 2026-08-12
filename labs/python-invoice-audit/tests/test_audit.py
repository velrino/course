from __future__ import annotations

import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest


LAB = Path(__file__).resolve().parents[1]
IMPLEMENTATION = os.environ.get("INVOICE_AUDIT_IMPL", "solution")
MODULE_PATH = LAB / IMPLEMENTATION / "audit.py"
SPEC = importlib.util.spec_from_file_location("invoice_audit_under_test", MODULE_PATH)
assert SPEC and SPEC.loader
audit_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit_module)


def valid_invoice(**changes):
    invoice = {
        "invoice_id": "INV-2026-0100",
        "supplier": "Pine Street Books",
        "amount": "42.50",
        "currency": "USD",
        "issued_on": "2026-03-10",
        "purchase_order": "PO-2026-0110",
        "line_items": [
            {"description": "Reference manual", "quantity": 1, "unit_price": "42.50"}
        ],
    }
    invoice.update(changes)
    return invoice


class ValidationTests(unittest.TestCase):
    def test_normalizes_a_valid_invoice(self):
        normalized = audit_module.validate_invoice(valid_invoice(amount="42.5"))
        self.assertEqual(normalized["amount"], "42.50")
        self.assertEqual(normalized["currency"], "USD")

    def test_rejects_a_total_that_does_not_match_line_items(self):
        with self.assertRaisesRegex(audit_module.ValidationError, "line-item total"):
            audit_module.validate_invoice(valid_invoice(amount="41.00"))

    def test_rejects_invalid_dates_and_boolean_quantities(self):
        with self.assertRaisesRegex(audit_module.ValidationError, "ISO date"):
            audit_module.validate_invoice(valid_invoice(issued_on="2026-02-30"))
        bad = valid_invoice()
        bad["line_items"][0]["quantity"] = True
        with self.assertRaisesRegex(audit_module.ValidationError, "quantity"):
            audit_module.validate_invoice(bad)


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.input = self.root / "input.ndjson"
        self.report = self.root / "report.json"
        self.ledger = self.root / "ledger.json"

    def tearDown(self):
        self.temporary.cleanup()

    def run_audit(self):
        log_stream = io.StringIO()
        report = audit_module.audit(
            self.input,
            self.report,
            self.ledger,
            logger=audit_module.JsonLogger(log_stream),
        )
        logs = [json.loads(line) for line in log_stream.getvalue().splitlines()]
        return report, logs

    def test_fixture_matches_golden_report_and_structured_logs(self):
        self.input.write_bytes((LAB / "fixtures" / "invoices.ndjson").read_bytes())
        report, logs = self.run_audit()
        expected = json.loads((LAB / "fixtures" / "expected-first-report.json").read_text())
        expected_ledger = json.loads(
            (LAB / "fixtures" / "expected-first-ledger.json").read_text()
        )
        self.assertEqual(report, expected)
        self.assertEqual(json.loads(self.report.read_text()), expected)
        self.assertEqual(json.loads(self.ledger.read_text()), expected_ledger)
        self.assertEqual(len(logs), 6)
        self.assertEqual(logs[-1]["event"], "audit_completed")

    def test_repeated_run_is_idempotent(self):
        self.input.write_text(json.dumps(valid_invoice()) + "\n", encoding="utf-8")
        first, _ = self.run_audit()
        second, _ = self.run_audit()
        self.assertEqual(first["counts"]["accepted"], 1)
        self.assertEqual(second["counts"], {"accepted": 0, "rejected": 0, "skipped": 1})
        self.assertEqual(second["skipped"][0]["invoice_id"], "INV-2026-0100")

    def test_invalid_json_does_not_stop_the_next_record(self):
        self.input.write_text("not-json\n" + json.dumps(valid_invoice()) + "\n", encoding="utf-8")
        report, _ = self.run_audit()
        self.assertEqual(report["counts"], {"accepted": 1, "rejected": 1, "skipped": 0})
        self.assertEqual(report["rejected"], [{"line": 1, "reason": "invalid JSON"}])

    @unittest.skipUnless(hasattr(os, "symlink"), "symbolic links are unavailable")
    def test_rejects_a_symlink_destination_without_overwriting_target(self):
        self.input.write_text(json.dumps(valid_invoice()) + "\n", encoding="utf-8")
        target = self.root / "target.json"
        target.write_text("keep me", encoding="utf-8")
        self.report.symlink_to(target)
        with self.assertRaises(audit_module.UnsafePathError):
            self.run_audit()
        self.assertEqual(target.read_text(), "keep me")

    def test_rejects_corrupt_ledger_before_processing(self):
        self.input.write_text(json.dumps(valid_invoice()) + "\n", encoding="utf-8")
        self.ledger.write_text('{"schema_version":99}', encoding="utf-8")
        with self.assertRaisesRegex(audit_module.ValidationError, "ledger"):
            self.run_audit()
        self.assertFalse(self.report.exists())


if __name__ == "__main__":
    unittest.main()
