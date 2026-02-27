"""
Chunk markdown into smaller pieces for agent memory.

Usage:
  python chunk_markdown.py --memory <domain> [--incremental]

Run from workspace root.
- Reads from: source/<domain>/**/*.md or memory/<domain>/**/*.md.
- Writes to: memory/<domain>/<topic>/ directly (no chunked/ subfolder)
- Excludes: paths containing "images", and chunk output files (stem__slide_*, stem__section_*)

--incremental: Only chunk files that are new or have been modified since last chunk.
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CONTENT_MEMORY_ROOT", os.getcwd()))
SOURCE = ROOT / "source"
MEMORY = ROOT / "memory"
MIN_CHUNK_LINES = 5


def _find_image_refs(text: str) -> list[str]:
    return re.findall(r"!\[[^\]]*\]\(<?([^)>]+)>?\)", text)


def _copy_images(refs: list[str], src_base: Path, dst_base: Path):
    import shutil
    for ref in refs:
        src = src_base / ref
        if not src.exists():
            continue
        dst = dst_base / ref
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copy2(str(src), str(dst))


def _chunk_by_slides(text: str) -> list[tuple[str, str]]:
    parts = re.split(r"(<!-- Slide number: \d+ -->)", text)
    chunks, current_label, current_lines = [], "preamble", []

    for part in parts:
        m = re.match(r"<!-- Slide number: (\d+) -->", part)
        if m:
            if current_lines and "".join(current_lines).strip():
                chunks.append((current_label, "".join(current_lines)))
            current_label = f"slide_{int(m.group(1)):02d}"
            current_lines = [part]
        else:
            current_lines.append(part)

    if current_lines and "".join(current_lines).strip():
        chunks.append((current_label, "".join(current_lines)))
    return chunks


def _chunk_by_headings(text: str) -> list[tuple[str, str]]:
    lines = text.split("\n")
    chunks, current_lines, chunk_idx = [], [], 0

    for line in lines:
        if re.match(r"^#{1,2}\s", line) and len(current_lines) >= MIN_CHUNK_LINES:
            chunks.append((f"section_{chunk_idx:02d}", "\n".join(current_lines)))
            current_lines, chunk_idx = [], chunk_idx + 1
        current_lines.append(line)

    if current_lines:
        chunks.append((f"section_{chunk_idx:02d}", "\n".join(current_lines)))
    return chunks


def _is_slide_deck(text: str) -> bool:
    return bool(re.search(r"<!-- Slide number: \d+ -->", text))


def _extract_source_ref(text: str) -> tuple[str | None, str | None]:
    m = re.search(r"<!--\s*Source:\s*([^|]+)\s*\|\s*([^>]+)\s*-->", text)
    return (m.group(1).strip(), m.group(2).strip()) if m else (None, None)


def _add_chunk_source_ref(content: str, source_path: str | None, source_url: str | None, location: str) -> str:
    if not source_path:
        return content
    loc = f", {location}" if location else ""
    url = f" | {source_url}" if source_url else ""
    return f"<!-- Source: {source_path}{loc}{url} -->\n\n" + content


def _needs_chunking(md_path: Path, chunk_root: Path) -> bool:
    md_mtime = md_path.stat().st_mtime
    stem = md_path.stem
    chunks = list(chunk_root.glob(f"{stem}*.md"))
    if not chunks:
        return True
    latest = max(c.stat().st_mtime for c in chunks)
    return md_mtime > latest


def _is_chunk_output(name: str) -> bool:
    return "__slide_" in name or "__section_" in name


def chunk_file(md_path: Path, conv_root: Path, chunk_root: Path, clear_existing: bool = False) -> int:
    text = md_path.read_text(encoding="utf-8")
    stem, source_path, source_url = md_path.stem, *_extract_source_ref(text)
    chunk_root.mkdir(parents=True, exist_ok=True)

    if clear_existing:
        for old in chunk_root.glob(f"{stem}*.md"):
            old.unlink()

    if _is_slide_deck(text):
        chunks = _chunk_by_slides(text)
    elif text.count("\n") > 200:
        chunks = _chunk_by_headings(text)
    else:
        chunks = [(stem, text)]

    def _loc(label: str) -> str:
        if label.startswith("slide_"):
            return f"slide {int(label.split('_')[1])}"
        if label.startswith("section_"):
            return f"section {int(label.split('_')[1]) + 1}"
        return ""

    written = 0
    for label, content in chunks:
        if not content.strip():
            continue
        content = _add_chunk_source_ref(content, source_path, source_url, _loc(label))
        out = chunk_root / (f"{stem}__{label}.md" if len(chunks) > 1 else f"{stem}.md")
        out.write_text(content, encoding="utf-8")
        for ref in _find_image_refs(content):
            _copy_images([ref], conv_root, chunk_root)
        written += 1
    return written


def _chunk_root_for_topic(mem_root: Path, topic_rel: Path) -> Path:
    """Chunks go in the topic folder, not inside converted/, workspace/, or markdown/."""
    parts = list(topic_rel.parts)
    for sub in ("converted", "workspace", "markdown"):
        if sub in parts:
            idx = parts.index(sub)
            return mem_root / Path(*parts[:idx])
    return mem_root / topic_rel


def _collect_md_files(root: Path, exclude_parts: set[str]) -> list[Path]:
    out = []
    for f in root.rglob("*.md"):
        if any(p in f.parts for p in exclude_parts):
            continue
        if _is_chunk_output(f.name):
            continue
        out.append(f)
    return sorted(out)


def _run_memory_mode(domain: str, incremental: bool) -> None:
    src_root = SOURCE / domain
    mem_root = MEMORY / domain

    # Prefer source (symlinks to content); fall back to memory
    if src_root.exists():
        read_root = src_root.resolve()  # follow symlinks
        read_label = f"source/{domain}"
    elif mem_root.exists():
        read_root = mem_root
        read_label = f"memory/{domain}"
    else:
        print(f"Neither source/{domain} nor memory/{domain} found.")
        return

    exclude = {"chunked", "images"}
    md_files = _collect_md_files(read_root, exclude)
    if not md_files:
        print(f"No markdown in {read_label}/")
        return

    mode = " (incremental)" if incremental else ""
    print(f"Chunk: {read_label}{mode}  ({len(md_files)} files) -> memory/{domain}/\n")
    total = 0
    skipped = 0

    for i, f in enumerate(md_files, 1):
        try:
            rel_to_read = f.parent.relative_to(read_root)
        except ValueError:
            rel_to_read = Path(".")
        topic_rel = rel_to_read
        conv_root = f.parent
        chunk_root = _chunk_root_for_topic(mem_root, topic_rel)
        label = str(topic_rel / f.name) if topic_rel != Path(".") else f.name

        print(f"  [{i}/{len(md_files)}] {label} ... ", end="", flush=True)
        if incremental and not _needs_chunking(f, chunk_root):
            print("SKIP (up to date)")
            skipped += 1
            continue
        try:
            clear_existing = incremental and chunk_root.exists()
            n = chunk_file(f, conv_root, chunk_root, clear_existing=clear_existing)
            total += n
            print(f"OK  ({n} chunks)")
        except Exception as e:
            print(f"FAIL  {e}")

    print(f"\nDone: {total} chunks." + (f" ({skipped} skipped)" if skipped else ""))


def main():
    if "--memory" not in sys.argv:
        print("Usage: python chunk_markdown.py --memory <domain> [--incremental]")
        print("  domain: e.g. CBE, GTB")
        print("  Reads from source/<domain>/ (or memory/ if no source), writes to memory/<domain>/")
        return
    idx = sys.argv.index("--memory")
    if idx + 1 >= len(sys.argv):
        print("Usage: python chunk_markdown.py --memory <domain> [--incremental]")
        return
    incremental = "--incremental" in sys.argv
    _run_memory_mode(sys.argv[idx + 1], incremental)


if __name__ == "__main__":
    main()
