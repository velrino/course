"""Small build-time fixes that keep source Markdown useful on GitHub."""

from __future__ import annotations

import re


REFERENCE_BASE = "https://github.com/velrino/course/blob/master/references/"
MODULE_DIRECTORY_LINK = re.compile(r"\((\d{2}-[a-z0-9-]+)/\)")


def on_page_markdown(markdown, page, **_kwargs):
    """Adapt repository-relative source links to the published site."""
    if page.file.src_uri == "00-course-index.md":
        markdown = MODULE_DIRECTORY_LINK.sub(r"(\1/index.md)", markdown)
    return markdown.replace("../../references/", REFERENCE_BASE).replace(
        "../references/", REFERENCE_BASE
    )
