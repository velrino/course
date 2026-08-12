#!/usr/bin/env python3
"""Run every reference lab contract without hiding command output."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Suite:
    name: str
    command: tuple[str, ...]
    dependency: str
    marker: Path | None = None


SUITES = (
    Suite(
        "Python invoice audit",
        (sys.executable, "-m", "unittest", "discover", "-s", "labs/python-invoice-audit/tests", "-v"),
        sys.executable,
    ),
    Suite(
        "SQL support analytics",
        (sys.executable, "-m", "unittest", "discover", "-s", "labs/sql-support-analytics/tests", "-v"),
        sys.executable,
    ),
    Suite(
        "Grounded RAG search",
        (sys.executable, "-m", "unittest", "discover", "-s", "labs/rag-grounded-search/tests", "-v"),
        sys.executable,
    ),
    Suite(
        "Node.js webhook processor",
        ("npm", "test", "--prefix", "labs/node-webhook-processor"),
        "npm",
    ),
    Suite(
        "n8n workflow contract",
        ("npm", "test", "--prefix", "labs/n8n-order-triage"),
        "npm",
    ),
    Suite(
        "Docker application and static contract",
        ("npm", "test", "--prefix", "labs/docker-health-stack"),
        "npm",
    ),
    Suite(
        "MCP TypeScript contract",
        ("npm", "run", "typecheck", "--prefix", "labs/mcp-task-server"),
        "npm",
        ROOT / "labs/mcp-task-server/node_modules/.bin/tsc",
    ),
    Suite(
        "MCP official-client behavior",
        ("npm", "test", "--prefix", "labs/mcp-task-server"),
        "npm",
        ROOT / "labs/mcp-task-server/node_modules/.bin/tsx",
    ),
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--require-all",
        action="store_true",
        help="treat a missing runtime or uninstalled MCP dependency as failure",
    )
    args = parser.parse_args()

    passed: list[str] = []
    failed: list[str] = []
    skipped: list[str] = []

    for suite in SUITES:
        unavailable = shutil.which(suite.dependency) is None
        uninstalled = suite.marker is not None and not suite.marker.exists()
        if unavailable or uninstalled:
            reason = f"missing {suite.dependency}" if unavailable else "run npm ci in labs/mcp-task-server"
            print(f"\nSKIP {suite.name}: {reason}", flush=True)
            (failed if args.require_all else skipped).append(suite.name)
            continue

        print(f"\n=== {suite.name} ===", flush=True)
        print("$ " + " ".join(suite.command), flush=True)
        result = subprocess.run(suite.command, cwd=ROOT, check=False)
        (passed if result.returncode == 0 else failed).append(suite.name)

    print("\n=== Lab summary ===")
    print(f"Passed:  {len(passed)}")
    print(f"Failed:  {len(failed)}")
    print(f"Skipped: {len(skipped)}")
    for name in failed:
        print(f"FAIL {name}")
    for name in skipped:
        print(f"SKIP {name}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
