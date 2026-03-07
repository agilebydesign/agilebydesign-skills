#!/usr/bin/env python3
"""
Sync SharePoint URLs in memory chunks. Run after chunk_markdown.

1. Replace source path with SharePoint URL when format is source/... | https://...
2. Fix URL order: path must be before query (?csf=1&web=1&e=...)
3. Add &wdSlideIndex=N (0-based) to *__slide_NN.md with .pptx URLs
4. Add &page=N to *__page_NN.md / *__section_NN.md with .pdf URLs

Usage:
  python scripts/sync_sharepoint_urls.py [--memory <memory_name>]

Operates on chunked .md files in memory/<memory_name>/. Run after chunk_markdown.
Run from workspace root. Set CONTENT_MEMORY_ROOT if workspace root differs.
"""

import os
import re
import sys
from pathlib import Path

from _config import ROOT, MEMORY, ensure_root

ensure_root()

# 1. Replace source path with SharePoint URL
SOURCE_PIPE_URL_RE = re.compile(
    r"(<!--\s*Source:\s*)source/[^|]+\s*\|\s*(https://[^\s>]+)(\s*-->)",
    re.IGNORECASE,
)

# 2. Fix URL order: path after ?query -> path before ?query
FIX_ORDER_RE = re.compile(
    r"(\?csf=1&web=1&e=[^/\s]+)(/[^\s>]+\.(?:pptx?|pdf|docx?|xlsx?))",
    re.IGNORECASE,
)

# 3. Add slide/page params
PPTX_SOURCE_RE = re.compile(
    r"(<!--\s*Source:\s*)(https://[^\s>]+\.pptx)(\?csf=1&web=1&e=[^\s&>]+)(&[^\s>]*)?(\s*-->)",
    re.IGNORECASE,
)
PDF_SOURCE_RE = re.compile(
    r"(<!--\s*Source:\s*)(https://[^\s>]+\.pdf)(\?csf=1&web=1&e=[^\s&>]+)(&[^\s>]*)?(\s*-->)",
    re.IGNORECASE,
)
SLIDE_FILENAME_RE = re.compile(r"__slide_(\d+)\.md$", re.IGNORECASE)
PAGE_FILENAME_RE = re.compile(r"__(?:page|section)_(\d+)\.md$", re.IGNORECASE)


def _step1_source_to_sharepoint(text: str) -> str:
    """Replace source path | SharePoint URL with SharePoint URL only."""
    return SOURCE_PIPE_URL_RE.sub(r"\1\2\3", text)


def _step2_fix_url_order(text: str) -> str:
    """Move path from after ?query to before ?query."""
    return FIX_ORDER_RE.sub(lambda m: m.group(2) + m.group(1), text)


def _step3_add_slide_links(text: str, path: Path) -> str:
    """Add wdSlideIndex (pptx) or page (pdf) to slide/page files."""
    slide_m = SLIDE_FILENAME_RE.search(path.name)
    page_m = PAGE_FILENAME_RE.search(path.name)
    slide_num = int(slide_m.group(1)) if slide_m else None
    page_num = int(page_m.group(1)) if page_m else None

    def repl_pptx(m):
        prefix, url, query, extra, suffix = m.group(1), m.group(2), m.group(3), m.group(4) or "", m.group(5)
        if "wdSlideIndex=" in (query + extra) or slide_num is None:
            return m.group(0)
        idx = slide_num - 1
        new_extra = f"{extra}&wdSlideIndex={idx}" if extra else f"&wdSlideIndex={idx}"
        return f"{prefix}{url}{query}{new_extra}{suffix}"

    def repl_pdf(m):
        prefix, url, query, extra, suffix = m.group(1), m.group(2), m.group(3), m.group(4) or "", m.group(5)
        if "page=" in (query + extra) or page_num is None:
            return m.group(0)
        new_extra = f"{extra}&page={page_num}" if extra else f"&page={page_num}"
        return f"{prefix}{url}{query}{new_extra}{suffix}"

    text = PPTX_SOURCE_RE.sub(repl_pptx, text)
    text = PDF_SOURCE_RE.sub(repl_pdf, text)
    return text


def update_file(path: Path) -> bool:
    """Apply all three steps. Returns True if changed."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return False
    orig = text
    text = _step1_source_to_sharepoint(text)
    text = _step2_fix_url_order(text)
    text = _step3_add_slide_links(text, path)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    memory_name = None
    if "--memory" in sys.argv:
        idx = sys.argv.index("--memory")
        if idx + 1 < len(sys.argv):
            memory_name = sys.argv[idx + 1]

    base = MEMORY / memory_name if memory_name else MEMORY
    if not base.exists():
        print(f"Memory path not found: {base}")
        sys.exit(1)
    md_files = sorted(base.rglob("*.md"))

    changed = 0
    for md in md_files:
        if update_file(md):
            changed += 1
            try:
                print(md.relative_to(base))
            except ValueError:
                print(md)
    print(f"\nSynced {changed} files with SharePoint URLs")


if __name__ == "__main__":
    main()
