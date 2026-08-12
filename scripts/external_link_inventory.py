#!/usr/bin/env python3
"""Create a deterministic external-link inventory without network access."""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"!?\[[^\]]*\]\((https?://[^)\s]+)(?:\s+[^)]*)?\)")
EXCLUDED_PARTS = {".git", ".venv", "node_modules", "site", "build"}


def canonical_url(value: str) -> str:
    parsed = urlsplit(value.rstrip(".,;"))
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path, parsed.query, parsed.fragment))


def inventory() -> dict[str, set[str]]:
    links: dict[str, set[str]] = defaultdict(set)
    for path in sorted(ROOT.rglob("*.md")):
        relative = path.relative_to(ROOT)
        if EXCLUDED_PARTS.intersection(relative.parts):
            continue
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            links[canonical_url(match.group(1))].add(relative.as_posix())
    return links


def render(links: dict[str, set[str]]) -> str:
    lines = [f"External links: {len(links)}"]
    for url in sorted(links):
        lines.append(f"{url}\t{','.join(sorted(links[url]))}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write the inventory to this path")
    args = parser.parse_args()
    result = render(inventory())
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(result, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
