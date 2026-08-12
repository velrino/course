#!/usr/bin/env python3
"""Safe, idempotent invoice audit pipeline using only the standard library."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from decimal import Decimal, InvalidOperation
from typing import Any, TextIO


ALLOWED_CURRENCIES = {"BRL", "EUR", "GBP", "USD"}
INVOICE_ID = re.compile(r"^INV-\d{4}-\d{4}$")
PURCHASE_ORDER_ID = re.compile(r"^PO-\d{4}-\d{4}$")
MAX_AMOUNT = Decimal("1000000.00")
CENT = Decimal("0.01")


class ValidationError(ValueError):
    """Raised when an invoice or ledger violates the public contract."""


class UnsafePathError(ValueError):
    """Raised before following an unsafe filesystem path."""


class JsonLogger:
    def __init__(self, stream: TextIO = sys.stderr) -> None:
        self.stream = stream

    def emit(self, event: str, **fields: Any) -> None:
        payload = {"event": event, **fields}
        print(json.dumps(payload, sort_keys=True, separators=(",", ":")), file=self.stream)


def _money(value: Any, field: str, *, allow_zero: bool = False) -> Decimal:
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be a decimal string")
    try:
        amount = Decimal(value)
    except InvalidOperation as exc:
        raise ValidationError(f"{field} must be a decimal string") from exc
    if not amount.is_finite() or amount.as_tuple().exponent < -2:
        raise ValidationError(f"{field} must have at most two decimal places")
    if amount < 0 or (amount == 0 and not allow_zero) or amount > MAX_AMOUNT:
        raise ValidationError(f"{field} is outside the allowed range")
    return amount.quantize(CENT)


def _required_text(record: dict[str, Any], field: str, maximum: int = 120) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip() or len(value.strip()) > maximum:
        raise ValidationError(f"{field} must be non-empty text up to {maximum} characters")
    return value.strip()


def validate_invoice(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ValidationError("invoice must be a JSON object")

    invoice_id = _required_text(record, "invoice_id", 40)
    if not INVOICE_ID.fullmatch(invoice_id):
        raise ValidationError("invoice_id must match INV-YYYY-NNNN")

    purchase_order = _required_text(record, "purchase_order", 40)
    if not PURCHASE_ORDER_ID.fullmatch(purchase_order):
        raise ValidationError("purchase_order must match PO-YYYY-NNNN")

    supplier = _required_text(record, "supplier")
    currency = _required_text(record, "currency", 3).upper()
    if currency not in ALLOWED_CURRENCIES:
        raise ValidationError("currency is not supported")

    issued_on = _required_text(record, "issued_on", 10)
    try:
        dt.date.fromisoformat(issued_on)
    except ValueError as exc:
        raise ValidationError("issued_on must be a real ISO date") from exc

    amount = _money(record.get("amount"), "amount")
    raw_items = record.get("line_items")
    if not isinstance(raw_items, list) or not raw_items:
        raise ValidationError("line_items must be a non-empty array")
    if len(raw_items) > 100:
        raise ValidationError("line_items may contain at most 100 entries")

    items: list[dict[str, Any]] = []
    calculated_total = Decimal("0.00")
    for position, raw_item in enumerate(raw_items, start=1):
        if not isinstance(raw_item, dict):
            raise ValidationError(f"line item {position} must be an object")
        description = _required_text(raw_item, "description", 160)
        quantity = raw_item.get("quantity")
        if isinstance(quantity, bool) or not isinstance(quantity, int) or not 1 <= quantity <= 10000:
            raise ValidationError(f"line item {position} has an invalid quantity")
        unit_price = _money(raw_item.get("unit_price"), f"line item {position} unit_price")
        calculated_total += unit_price * quantity
        items.append(
            {
                "description": description,
                "quantity": quantity,
                "unit_price": f"{unit_price:.2f}",
            }
        )

    if calculated_total.quantize(CENT) != amount:
        raise ValidationError("amount does not equal the line-item total")

    return {
        "invoice_id": invoice_id,
        "supplier": supplier,
        "amount": f"{amount:.2f}",
        "currency": currency,
        "issued_on": issued_on,
        "purchase_order": purchase_order,
        "line_items": items,
    }


def _reject_symlink(path: Path, role: str) -> None:
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return
    if stat.S_ISLNK(mode):
        raise UnsafePathError(f"{role} must not be a symbolic link")


def read_lines(path: Path) -> list[str]:
    _reject_symlink(path, "input")
    if not path.is_file():
        raise UnsafePathError("input must be a regular file")
    return path.read_text(encoding="utf-8").splitlines()


def load_ledger(path: Path) -> set[str]:
    _reject_symlink(path, "ledger")
    if not path.exists():
        return set()
    if not path.is_file():
        raise UnsafePathError("ledger must be a regular file")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError("ledger must contain valid JSON") from exc
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValidationError("ledger has an unsupported schema")
    ids = data.get("processed_invoice_ids")
    if not isinstance(ids, list) or any(not isinstance(item, str) for item in ids):
        raise ValidationError("ledger invoice IDs must be an array of strings")
    if len(ids) != len(set(ids)):
        raise ValidationError("ledger invoice IDs must be unique")
    return set(ids)


def atomic_write_json(path: Path, payload: Any) -> None:
    _reject_symlink(path, "destination")
    parent = path.parent
    parent.mkdir(parents=True, exist_ok=True)
    _reject_symlink(parent, "destination directory")
    if not parent.is_dir():
        raise UnsafePathError("destination parent must be a directory")

    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=parent, prefix=f".{path.name}.", delete=False
        ) as handle:
            temporary_name = handle.name
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    finally:
        if temporary_name and os.path.exists(temporary_name):
            os.unlink(temporary_name)


def audit(
    input_path: Path,
    report_path: Path,
    ledger_path: Path,
    *,
    logger: JsonLogger | None = None,
) -> dict[str, Any]:
    logger = logger or JsonLogger()
    resolved_paths = [path.resolve(strict=False) for path in (input_path, report_path, ledger_path)]
    if len(set(resolved_paths)) != 3:
        raise UnsafePathError("input, report, and ledger paths must be different")

    processed = load_ledger(ledger_path)
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []

    for line_number, line in enumerate(read_lines(input_path), start=1):
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            rejected.append({"line": line_number, "reason": "invalid JSON"})
            logger.emit("invoice_rejected", line=line_number, reason="invalid JSON")
            continue

        try:
            invoice = validate_invoice(raw)
        except ValidationError as exc:
            rejected.append({"line": line_number, "reason": str(exc)})
            logger.emit("invoice_rejected", line=line_number, reason=str(exc))
            continue

        invoice_id = invoice["invoice_id"]
        if invoice_id in processed:
            skipped.append(
                {"line": line_number, "invoice_id": invoice_id, "reason": "already processed"}
            )
            logger.emit("invoice_skipped", line=line_number, invoice_id=invoice_id)
            continue

        processed.add(invoice_id)
        accepted.append(invoice)
        logger.emit("invoice_accepted", line=line_number, invoice_id=invoice_id)

    report = {
        "schema_version": 1,
        "counts": {
            "accepted": len(accepted),
            "rejected": len(rejected),
            "skipped": len(skipped),
        },
        "accepted": accepted,
        "rejected": rejected,
        "skipped": skipped,
    }
    ledger = {"schema_version": 1, "processed_invoice_ids": sorted(processed)}
    atomic_write_json(report_path, report)
    atomic_write_json(ledger_path, ledger)
    logger.emit("audit_completed", **report["counts"])
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="NDJSON invoice file")
    parser.add_argument("--report", type=Path, required=True, help="JSON report destination")
    parser.add_argument("--ledger", type=Path, required=True, help="JSON idempotency ledger")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        audit(args.input, args.report, args.ledger)
    except (OSError, ValidationError, UnsafePathError) as exc:
        JsonLogger().emit("audit_failed", reason=str(exc))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
