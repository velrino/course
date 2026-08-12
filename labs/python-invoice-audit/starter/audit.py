#!/usr/bin/env python3
"""Starter implementation for the invoice audit lab."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, TextIO


class ValidationError(ValueError):
    pass


class UnsafePathError(ValueError):
    pass


class JsonLogger:
    def __init__(self, stream: TextIO = sys.stderr) -> None:
        self.stream = stream

    def emit(self, event: str, **fields: Any) -> None:
        print(json.dumps({"event": event, **fields}, sort_keys=True), file=self.stream)


def validate_invoice(record: Any) -> dict[str, Any]:
    """TODO: enforce the complete invoice contract and normalize money."""
    if not isinstance(record, dict) or not record.get("invoice_id"):
        raise ValidationError("invoice_id is required")
    return record


def load_ledger(path: Path) -> set[str]:
    """TODO: safely load and validate an existing ledger."""
    return set()


def atomic_write_json(path: Path, payload: Any) -> None:
    """TODO: reject symlinks and replace a same-directory temporary file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def audit(
    input_path: Path,
    report_path: Path,
    ledger_path: Path,
    *,
    logger: JsonLogger | None = None,
) -> dict[str, Any]:
    logger = logger or JsonLogger()
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []

    # This parsing loop is intentionally runnable. The TODOs make the tests fail
    # for validation, idempotency, safe writes, and the full report contract.
    for line_number, line in enumerate(input_path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            accepted.append(validate_invoice(json.loads(line)))
            logger.emit("invoice_accepted", line=line_number)
        except (json.JSONDecodeError, ValidationError) as exc:
            rejected.append({"line": line_number, "reason": str(exc)})

    report = {
        "schema_version": 1,
        "counts": {"accepted": len(accepted), "rejected": len(rejected), "skipped": 0},
        "accepted": accepted,
        "rejected": rejected,
        "skipped": [],
    }
    atomic_write_json(report_path, report)
    # TODO: persist a validated, sorted ledger after the report succeeds.
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    args = parser.parse_args(argv)
    audit(args.input, args.report, args.ledger)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
