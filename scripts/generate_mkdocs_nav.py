#!/usr/bin/env python3
"""Generate the explicit MkDocs navigation from canonical document headings."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
CONFIG = ROOT / "mkdocs.yml"
BEGIN = "  # BEGIN GENERATED COURSE NAV"
END = "  # END GENERATED COURSE NAV"
MODULE_RE = re.compile(r"^\d{2}-[a-z0-9-]+$")
LESSON_RE = re.compile(r"^\d{2}-[a-z0-9-]+\.md$")


def title(path: Path) -> str:
    first_line = path.read_text(encoding="utf-8").splitlines()[0]
    if not first_line.startswith("# "):
        raise ValueError(f"{path.relative_to(ROOT)} does not begin with an H1")
    return first_line[2:].strip()


def quoted(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


def generated_lines() -> list[str]:
    lines = [
        f"  - {quoted('Home')}: {quoted('index.md')}",
        f"  - {quoted('Course Index')}: {quoted('00-course-index.md')}",
        f"  - {quoted('Practice Labs')}: {quoted('labs.md')}",
        f"  - {quoted('Image Provenance')}: {quoted('assets/images/README.md')}",
        f"  - {quoted('Modules')}:",
    ]
    modules = sorted(
        path for path in CONTENT.iterdir() if path.is_dir() and MODULE_RE.fullmatch(path.name)
    )
    for module in modules:
        index = module / "index.md"
        lines.append(f"      - {quoted(title(index))}:")
        lines.append(
            f"          - {quoted('Module overview')}: "
            f"{quoted(index.relative_to(CONTENT).as_posix())}"
        )
        lessons = sorted(path for path in module.glob("*.md") if LESSON_RE.fullmatch(path.name))
        for lesson in lessons:
            lines.append(
                f"          - {quoted(title(lesson))}: "
                f"{quoted(lesson.relative_to(CONTENT).as_posix())}"
            )
    lines.extend(
        [
            f"  - {quoted('Contributing')}: "
            f"{quoted('https://github.com/velrino/course/blob/master/CONTRIBUTING.md')}",
            f"  - {quoted('License')}: "
            f"{quoted('https://github.com/velrino/course/blob/master/LICENSE')}",
            f"  - {quoted('Third-Party Notices')}: "
            f"{quoted('https://github.com/velrino/course/blob/master/THIRD_PARTY_NOTICES.md')}",
        ]
    )
    return lines


def expected_config() -> str:
    current = CONFIG.read_text(encoding="utf-8")
    lines = current.splitlines()
    try:
        start = lines.index(BEGIN)
        finish = lines.index(END)
    except ValueError as error:
        raise ValueError("mkdocs.yml is missing generated-navigation markers") from error
    if finish <= start:
        raise ValueError("mkdocs.yml navigation markers are out of order")
    replacement = lines[: start + 1] + generated_lines() + lines[finish:]
    return "\n".join(replacement) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if mkdocs.yml is stale")
    args = parser.parse_args()
    expected = expected_config()
    current = CONFIG.read_text(encoding="utf-8")
    if args.check:
        if current != expected:
            print("mkdocs.yml navigation is stale; run scripts/generate_mkdocs_nav.py")
            return 1
        print("MkDocs navigation is current.")
        return 0
    CONFIG.write_text(expected, encoding="utf-8")
    print("Updated explicit navigation in mkdocs.yml.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
