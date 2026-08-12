#!/usr/bin/env python3
"""Validate the curriculum without third-party Python packages."""

from __future__ import annotations

import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
MODULE_RE = re.compile(r"^\d{2}-[a-z0-9-]+$")
LESSON_RE = re.compile(r"^\d{2}-[a-z0-9-]+\.md$")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
EXCLUDED_PARTS = {".git", ".venv", "node_modules", "site", "build"}


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not EXCLUDED_PARTS.intersection(path.relative_to(ROOT).parts)
    )


def module_directories() -> list[Path]:
    return sorted(
        path
        for path in CONTENT.iterdir()
        if path.is_dir() and MODULE_RE.fullmatch(path.name)
    )


def lesson_files(module: Path) -> list[Path]:
    return sorted(path for path in module.glob("*.md") if LESSON_RE.fullmatch(path.name))


def slugify(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"[`*_\[\]]", "", value)
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-")


def anchors(path: Path) -> set[str]:
    found: set[str] = set()
    counts: Counter[str] = Counter()
    open_fence: tuple[str, int] | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        fence_match = FENCE_RE.match(line)
        if fence_match:
            fence = fence_match.group(1)
            if open_fence is None:
                open_fence = (fence[0], len(fence))
            elif fence[0] == open_fence[0] and len(fence) >= open_fence[1]:
                open_fence = None
            continue
        if open_fence is not None:
            continue
        match = HEADING_RE.match(line)
        if match:
            base = slugify(match.group(2))
            if not base:
                continue
            suffix = counts[base]
            found.add(base if suffix == 0 else f"{base}_{suffix}")
            counts[base] += 1
        found.update(re.findall(r'<a\s+(?:name|id)=["\']([^"\']+)["\']', line))
    return found


def parse_link_target(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("<") and ">" in raw:
        return raw[1 : raw.index(">")]
    if " " in raw:
        raw = raw.split(" ", 1)[0]
    return raw


def resolve_target(source: Path, target: str) -> tuple[Path | None, str]:
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or target.startswith(("mailto:", "tel:", "data:")):
        return None, ""
    fragment = unquote(parsed.fragment)
    path_text = unquote(parsed.path)
    if not path_text:
        return source, fragment
    if path_text.startswith("/"):
        destination = ROOT / path_text.lstrip("/")
    else:
        destination = source.parent / path_text
    destination = Path(destination).resolve()
    if destination.is_dir():
        for index_name in ("index.md", "README.md"):
            candidate = destination / index_name
            if candidate.exists():
                destination = candidate
                break
    return destination, fragment


def check_links(files: list[Path], errors: list[str]) -> None:
    anchor_cache: dict[Path, set[str]] = {}
    for source in files:
        text = source.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target_text = parse_link_target(match.group(1))
            destination, fragment = resolve_target(source, target_text)
            if destination is None:
                continue
            label = source.relative_to(ROOT)
            try:
                destination.relative_to(ROOT)
            except ValueError:
                errors.append(f"{label}: internal link escapes the repository: {target_text}")
                continue
            if not destination.exists():
                errors.append(f"{label}: missing internal link target: {target_text}")
                continue
            if fragment and destination.suffix.lower() == ".md":
                if destination not in anchor_cache:
                    anchor_cache[destination] = anchors(destination)
                if fragment not in anchor_cache[destination]:
                    errors.append(f"{label}: missing anchor #{fragment} in {destination.relative_to(ROOT)}")


def check_structure(files: list[Path], errors: list[str]) -> None:
    for path in files:
        relative = path.relative_to(ROOT)
        lines = path.read_text(encoding="utf-8").splitlines()
        h1_count = 0
        open_fence: tuple[str, int] | None = None
        for line in lines:
            match = FENCE_RE.match(line)
            if match:
                fence = match.group(1)
                if open_fence is None:
                    open_fence = (fence[0], len(fence))
                elif fence[0] == open_fence[0] and len(fence) >= open_fence[1]:
                    open_fence = None
                continue
            if open_fence is None and re.match(r"^#\s+\S", line):
                h1_count += 1
        if h1_count != 1:
            errors.append(f"{relative}: expected exactly one H1, found {h1_count}")
        if open_fence is not None:
            errors.append(f"{relative}: unclosed {open_fence[0]} code fence")


def headings(path: Path) -> set[str]:
    return {
        match.group(2).strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if (match := HEADING_RE.match(line)) and len(match.group(1)) == 2
    }


def check_lesson_contracts(modules: list[Path], errors: list[str]) -> int:
    total = 0
    for module in modules:
        module_number = int(module.name[:2])
        lessons = lesson_files(module)
        total += len(lessons)
        if not lessons:
            errors.append(f"{module.relative_to(ROOT)}: module has no numbered lessons")
        for lesson in lessons:
            section_names = headings(lesson)
            relative = lesson.relative_to(ROOT)
            for required in ("Completion criteria", "References"):
                if required not in section_names:
                    errors.append(f"{relative}: missing '## {required}'")

            if module_number in set(range(1, 28)) | {29}:
                if "Learning objectives" not in section_names:
                    errors.append(f"{relative}: missing '## Learning objectives'")
                if not any(name == "Free local practice" or name.startswith("Free local practice:") for name in section_names):
                    errors.append(f"{relative}: missing a '## Free local practice' section")
            elif module_number == 0 and "Objectives" not in section_names:
                errors.append(f"{relative}: missing '## Objectives'")
            elif module_number == 28:
                has_objective = "Objective" in section_names or "Objectives" in section_names
                has_work = "Practice" in section_names or "Deliverables" in section_names
                if not has_objective:
                    errors.append(f"{relative}: missing objective section")
                if not has_work:
                    errors.append(f"{relative}: missing practice or deliverables section")
    return total


def check_modules_and_nav(modules: list[Path], errors: list[str]) -> None:
    nav_path = ROOT / "mkdocs.yml"
    nav = nav_path.read_text(encoding="utf-8") if nav_path.exists() else ""
    if len(modules) != 30:
        errors.append(f"content: expected 30 numbered module directories, found {len(modules)}")

    for module in modules:
        index = module / "index.md"
        if not index.exists():
            errors.append(f"{module.relative_to(ROOT)}: missing index.md")
        else:
            required = {"Before you begin", "Lessons", "Suggested artifact", "Continue"}
            missing = required - headings(index)
            if missing:
                errors.append(f"{index.relative_to(ROOT)}: missing sections: {', '.join(sorted(missing))}")

        if not any("```mermaid" in path.read_text(encoding="utf-8") for path in lesson_files(module)):
            errors.append(f"{module.relative_to(ROOT)}: no Mermaid visual map in numbered lessons")

        expected_nav = [index, *lesson_files(module)]
        for path in expected_nav:
            nav_value = path.relative_to(CONTENT).as_posix()
            if nav.count(f'"{nav_value}"') != 1:
                errors.append(f"mkdocs.yml: expected one nav entry for {nav_value}")


def main() -> int:
    errors: list[str] = []
    files = markdown_files()
    modules = module_directories()
    check_structure(files, errors)
    check_links(files, errors)
    lessons = check_lesson_contracts(modules, errors)
    check_modules_and_nav(modules, errors)

    if errors:
        print(f"Validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"Validated {len(files)} Markdown files, {len(modules)} modules, "
        f"{lessons} lessons, internal links, document structure, and visual coverage."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
