"""
Chunk converted markdown into smaller pieces for agent memory.

Usage:
  python chunk_markdown.py --memory <memory_name>

Run from workspace root. Reads memory/<name>/*/converted/, writes memory/<name>/*/chunked/.
Run convert_to_markdown.py first.
"""

import re
import sys
from pathlib import Path

import os
ROOT = Path(os.environ["CONTENT_MEMORY_ROOT"]) if "CONTENT_MEMORY_ROOT" in os.environ else Path.cwd()

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


def chunk_file(md_path: Path, conv_root: Path, chunk_root: Path) -> int:
    text = md_path.read_text(encoding="utf-8")
    stem, source_path, source_url = md_path.stem, *_extract_source_ref(text)
    out_dir = chunk_root
    out_dir.mkdir(parents=True, exist_ok=True)

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
        out = out_dir / (f"{stem}__{label}.md" if len(chunks) > 1 else f"{stem}.md")
        out.write_text(content, encoding="utf-8")
        for ref in _find_image_refs(content):
            _copy_images([ref], conv_root, chunk_root)
        written += 1
    return written


def _run_memory_mode(memory_name: str) -> None:
    memory_root = MEMORY / memory_name
    if not memory_root.exists():
        print(f"Memory not found: {memory_root}")
        return

    md_files = sorted(
        f for f in memory_root.rglob("converted/*.md")
        if f.parent.name == "converted" and "images" not in f.parts
    )
    if not md_files:
        print(f"No markdown in {memory_root}/*/converted/")
        print("Run convert_to_markdown.py --memory <path> first.")
        return

    print(f"Memory: {memory_name}  ({len(md_files)} files) -> chunked/\n")
    total = 0
    for i, f in enumerate(md_files, 1):
        rel = f.parent.parent.relative_to(memory_root)
        conv_root, chunk_root = f.parent, memory_root / rel / "chunked"
        label = str(rel / f.name) if rel != Path(".") else f.name
        print(f"  [{i}/{len(md_files)}] {label} ... ", end="", flush=True)
        try:
            n = chunk_file(f, conv_root, chunk_root)
            total += n
            print(f"OK  ({n} chunks)")
        except Exception as e:
            print(f"FAIL  {e}")
    print(f"\nDone: {total} chunks.")


def main():
    if "--memory" in sys.argv:
        idx = sys.argv.index("--memory")
        if idx + 1 < len(sys.argv):
            _run_memory_mode(sys.argv[idx + 1])
            return
    print("Usage: python chunk_markdown.py --memory <memory_name>")
    print("  memory_name: name of folder under memory/ (e.g. CBE)")


if __name__ == "__main__":
    main()
