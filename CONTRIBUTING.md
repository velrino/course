# Contributing

Contributions should make the course more accurate, reproducible, accessible, or useful to independent learners. Keep all learner-facing material in English and prefer free, primary, and authoritative sources.

## Development setup

1. Create a Python 3.11 or newer virtual environment.
2. Install the documentation dependencies with `python -m pip install -r requirements-docs.txt`.
3. Run `python scripts/generate_mkdocs_nav.py --check` and regenerate the nav without `--check` after adding or renaming course pages.
4. Run `python scripts/validate_course.py`.
5. Preview the site with `mkdocs serve`.
6. Before opening a pull request, run `mkdocs build --strict --site-dir /tmp/course-site`.

## Lesson standard

Technical lessons must contain exactly one level-one heading and these level-two sections: `Learning objectives`, a heading beginning with `Free local practice`, `Completion criteria`, and `References`. Orientation and capstone lessons use their established objective and deliverable structures. Every new module needs a useful `index.md` and at least one Mermaid visual map.

Exercises should run with free local tools whenever practical. State prerequisites, commands, expected evidence, failure behavior, and completion criteria. Never include credentials, personal data, employer data, paid-only requirements, or unexplained generated output.

## Sources and licensing

- Link directly to official documentation, standards, legislation, public research, or original project documentation.
- Paraphrase sources and explain the engineering implications; do not assemble lessons from copied passages.
- Do not copy content from the third-party PDFs in `references/`. They are explicitly excluded from the MIT License; see [Third-Party Notices](THIRD_PARTY_NOTICES.md).
- Only contribute material you have the right to license under MIT. Identify separately licensed assets and their terms before adding them.

## Pull requests

Keep changes focused. Describe the learner outcome, list verification commands, and disclose any network service or paid dependency. Update `mkdocs.yml` when adding, removing, or renaming a lesson. The CI checks internal links, document structure, required sections, visual-map coverage, and the strict documentation build.
