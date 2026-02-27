"""
Convert workspace to markdown/, sync to memory, chunk.

Usage:
  python sync_and_chunk.py --workspace <topic> --memory <domain> [--incremental]

Run from workspace root.
1. Converts non-.md files to .md in <folder>/markdown/ (in workspace)
2. Syncs workspace/<topic> to memory/<domain>/<topic> (copy)
3. Chunks .md from memory, writes to memory/<domain>/<topic>/

--incremental: Skip convert if .md newer than existing; use incremental chunking.
"""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CONTENT_MEMORY_ROOT", os.getcwd()))
MEMORY = ROOT / "memory"
WORKSPACE = ROOT / "workspace"

SUPPORTED_CONVERT = {".pdf", ".pptx", ".docx", ".xlsx", ".xls", ".html", ".htm", ".txt", ".csv", ".json", ".xml"}
SUPPORTED_COPY = {".md"}


def _add_source_header(text: str, rel_path: Path) -> str:
    if "<!-- Source:" in text[:200]:
        return text
    try:
        url = (ROOT / rel_path).as_uri()
        return f"<!-- Source: {rel_path.as_posix()} | {url} -->\n\n" + text
    except (ValueError, OSError):
        return text


def _convert_in_place(src: Path, rel_from_workspace: Path) -> bool:
    ext = src.suffix.lower()
    if ext in SUPPORTED_COPY:
        return True
    if ext not in SUPPORTED_CONVERT:
        return False
    try:
        from markitdown import MarkItDown
        md = MarkItDown()
        result = md.convert(str(src))
        text = _add_source_header(result.text_content, rel_from_workspace)
        md_dir = src.parent / "markdown"
        md_dir.mkdir(parents=True, exist_ok=True)
        out = md_dir / (src.stem + ".md")
        out.write_text(text, encoding="utf-8")
        return True
    except Exception as e:
        print(f"    Convert FAIL: {e}")
        return False


def _run_sync(workspace_topic: str, domain: str, incremental: bool) -> None:
    src_root = WORKSPACE / workspace_topic
    if not src_root.exists():
        print(f"Workspace folder not found: {src_root}")
        return

    # 1. Convert non-.md in place (in workspace)
    supported = SUPPORTED_CONVERT | SUPPORTED_COPY
    files = [f for f in src_root.rglob("*") if f.is_file() and f.suffix.lower() in supported and f.suffix.lower() != ".md"]
    if files:
        print(f"\nConvert in place: {src_root}  ({len(files)} files)")
        ok = 0
        for f in sorted(files):
            rel = f.relative_to(src_root)
            md_path = f.parent / "markdown" / (f.stem + ".md")
            if incremental and md_path.exists() and f.stat().st_mtime <= md_path.stat().st_mtime:
                continue
            label = str(rel)
            print(f"  {label} ... ", end="", flush=True)
            if _convert_in_place(f, Path("workspace") / workspace_topic / rel):
                print("OK")
                ok += 1
            else:
                print("SKIP")
        if ok:
            print(f"  Converted: {ok} files")

    # 2. Sync workspace to memory (copy)
    import shutil
    mem_topic = MEMORY / domain / workspace_topic
    mem_topic.parent.mkdir(parents=True, exist_ok=True)
    if mem_topic.exists():
        for item in src_root.rglob("*"):
            if item.is_file():
                rel = item.relative_to(src_root)
                dst = mem_topic / rel
                if not dst.exists() or item.stat().st_mtime > dst.stat().st_mtime:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(str(item), str(dst))
    else:
        shutil.copytree(str(src_root), str(mem_topic))
    print(f"Synced: workspace/{workspace_topic} -> memory/{domain}/{workspace_topic}")

    # 3. Chunk
    scripts_dir = Path(__file__).parent
    chunk_script = scripts_dir / "chunk_markdown.py"
    inc_flag = ["--incremental"] if incremental else []
    print(f"\nChunking memory/{domain} ...")
    subprocess.run(
        [sys.executable, str(chunk_script), "--memory", domain] + inc_flag,
        cwd=str(ROOT),
        env={**os.environ, "CONTENT_MEMORY_ROOT": str(ROOT)},
    )


def main():
    if "--workspace" not in sys.argv or "--memory" not in sys.argv:
        print("Usage: python sync_and_chunk.py --workspace <topic> --memory <domain> [--incremental]")
        print("  topic:  folder under workspace/")
        print("  domain: memory domain (e.g. CBE)")
        return

    def get_arg(name: str) -> str | None:
        if name not in sys.argv:
            return None
        i = sys.argv.index(name) + 1
        return sys.argv[i] if i < len(sys.argv) else None

    topic = get_arg("--workspace")
    domain = get_arg("--memory")
    if not topic or not domain:
        print("Usage: python sync_and_chunk.py --workspace <topic> --memory <domain> [--incremental]")
        return

    incremental = "--incremental" in sys.argv
    _run_sync(topic, domain, incremental)


if __name__ == "__main__":
    main()
