"""
Convert source files to markdown. Writes to markdown/ subfolder in each folder.

Usage:
  python convert_to_markdown.py --source <path> [--memory <domain>]
  python convert_to_markdown.py --from source/CBE/domain_journeys_approach

Run from workspace root.
- Converts PDF, DOCX, etc. to .md in <folder>/markdown/ for each folder/subfolder
- .md files are skipped (no conversion needed)
- Use --source for a content path, or --from for a path under source/

Requires: pip install "markitdown[all]"
"""

import importlib.util
import os
import sys
from pathlib import Path

try:
    from markitdown import MarkItDown
except ImportError:
    print('Missing dependency. Run: pip install "markitdown[all]"')
    sys.exit(1)

ROOT = Path(os.environ.get("CONTENT_MEMORY_ROOT", os.getcwd()))
SOURCE = ROOT / "source"
MEMORY = ROOT / "memory"
CONTENT_MEMORY = ROOT / ".content-memory"

SUPPORTED = {
    ".pdf", ".pptx", ".docx", ".xlsx", ".xls",
    ".html", ".htm", ".txt", ".csv", ".json", ".xml",
}

_md = MarkItDown()


def _load_transformers(memory_name: str) -> dict:
    registry = {}
    seen = set()
    for base in [MEMORY / memory_name / "transformers", CONTENT_MEMORY / "transformers"]:
        if not base.is_dir():
            continue
        for py in sorted(base.glob("*.py")):
            if py.name.startswith("_"):
                continue
            try:
                spec = importlib.util.spec_from_file_location(py.stem, py)
                if spec is None or spec.loader is None:
                    continue
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                exts = getattr(mod, "EXTENSIONS", None)
                fn = getattr(mod, "convert", None)
                if exts is None or fn is None or not callable(fn):
                    continue
                for ext in exts:
                    ext = ext.lower() if ext.startswith(".") else f".{ext.lower()}"
                    if ext not in seen:
                        registry[ext] = fn
                        seen.add(ext)
            except Exception as e:
                print(f"  [transformers] Skip {py.name}: {e}")
    return registry


def _add_source_ref(text: str, rel_path: Path) -> str:
    if "<!-- Source:" in text[:200]:
        return text
    try:
        url = (ROOT / rel_path).as_uri()
        return f"<!-- Source: {rel_path.as_posix()} | {url} -->\n\n" + text
    except (ValueError, OSError):
        return text


def convert_one_in_place(src: Path, transformers: dict) -> Path | None:
    """Convert one file to markdown in folder/markdown/. Returns output path or None."""
    ext = src.suffix.lower()
    md_dir = src.parent / "markdown"
    md_dir.mkdir(parents=True, exist_ok=True)
    out = md_dir / (src.stem + ".md")

    if ext in transformers:
        text = transformers[ext](src)
    else:
        text = _md.convert(str(src)).text_content

    text = _add_source_ref(text, src.relative_to(ROOT))
    out.write_text(text, encoding="utf-8")
    return out


def _run_convert(path_arg: str, memory_name: str | None) -> None:
    p = Path(path_arg)
    if p.is_absolute():
        src_full = p.resolve()
    else:
        cand = ROOT / path_arg
        if path_arg.startswith("source/"):
            cand = ROOT / path_arg
        elif memory_name and not (ROOT / path_arg).exists() and (SOURCE / memory_name / path_arg).exists():
            cand = SOURCE / memory_name / path_arg
        if cand.exists():
            src_full = cand.resolve()
        else:
            src_full = (ROOT / path_arg).resolve()

    if not src_full.exists():
        print(f"Path not found: {src_full}")
        return

    domain = memory_name or (src_full.relative_to(ROOT).parts[0] if SOURCE in src_full.parents or MEMORY in src_full.parents else "default")
    transformers = _load_transformers(domain)
    supported = SUPPORTED | set(transformers.keys())
    if transformers:
        print(f"Transformers: {', '.join(sorted(transformers.keys()))}\n")

    files = sorted(
        f for f in src_full.rglob("*")
        if f.is_file() and f.suffix.lower() in supported and f.suffix.lower() != ".md"
    )
    if not files:
        print(f"No files to convert in {src_full}")
        return

    print(f"Convert in place: {src_full}  ({len(files)} files)\n")
    ok, fail = 0, 0
    for i, f in enumerate(files, 1):
        label = str(f.relative_to(src_full))
        print(f"  [{i}/{len(files)}] {label} ... ", end="", flush=True)
        try:
            out = convert_one_in_place(f, transformers)
            kb = out.stat().st_size // 1024
            print(f"OK  ({kb} KB)")
            ok += 1
        except Exception as e:
            print(f"FAIL  {e}")
            fail += 1

    print(f"\nDone: {ok} converted, {fail} failed.")


def main():
    from_arg = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--from"), None)
    source_arg = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--source"), None)
    memory_arg = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--memory"), None)

    path = from_arg or source_arg
    if path:
        _run_convert(path, memory_arg)
        return

    print("Usage: python convert_to_markdown.py --source <path> [--memory <domain>]")
    print("       python convert_to_markdown.py --from source/<domain>/<topic>")
    print("  Converts to <folder>/markdown/ for each folder")


if __name__ == "__main__":
    main()
