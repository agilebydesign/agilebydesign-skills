"""
Orchestrate full pipeline: convert → chunk → embed → index.

Usage:
  python index_memory.py --path <source_folder>   # convert, chunk, embed (full pipeline)
  python index_memory.py --memory <memory_name>   # chunk + embed (chunks already exist or convert ran)
  python index_memory.py --replace                # rebuild entire index from all memory

Run from workspace root. Requires: markitdown, openai, faiss-cpu, numpy. Set OPENAI_API_KEY.
"""

import os
import subprocess
import sys
from pathlib import Path

from _config import ROOT, ensure_root

ensure_root()
SCRIPTS = Path(__file__).resolve().parent


def _run(script: str, args: list[str]) -> bool:
    """Run a script; return True on success."""
    cmd = [sys.executable, str(SCRIPTS / script)] + args
    r = subprocess.run(cmd, cwd=str(ROOT))
    return r.returncode == 0


def main():
    args = sys.argv[1:]
    replace = "--replace" in args
    if replace:
        args = [a for a in args if a != "--replace"]

    # Full rebuild: embed all memory with --replace
    if replace and not any(a in args for a in ("--path", "--memory")):
        if not _run("embed_and_index.py", ["--replace"]):
            sys.exit(1)
        print("Full index rebuilt.")
        return

    # --path: convert → chunk → embed
    path_idx = next((i for i, a in enumerate(args) if a == "--path"), None)
    if path_idx is not None and path_idx + 1 < len(args):
        src = args[path_idx + 1]
        memory_name = Path(src).name
        print(f"Pipeline: convert → chunk → sync SharePoint → embed for {src}\n")
        if not _run("convert_to_markdown.py", ["--memory", src]):
            sys.exit(1)
        if not _run("chunk_markdown.py", ["--path", src]):
            sys.exit(1)
        if not _run("sync_sharepoint_urls.py", ["--memory", memory_name]):
            sys.exit(1)
        embed_args = ["--memory", memory_name]
        if replace:
            embed_args.append("--replace")
        if not _run("embed_and_index.py", embed_args):
            sys.exit(1)
        print("\nDone: indexed.")
        return

    # --memory / --path: chunk → embed (assumes convert already ran or chunks exist)
    mem_idx = next((i for i, a in enumerate(args) if a == "--memory"), None)
    path_idx = next((i for i, a in enumerate(args) if a == "--path"), None)
    src = None
    if path_idx is not None and path_idx + 1 < len(args):
        src = args[path_idx + 1]
    elif mem_idx is not None and mem_idx + 1 < len(args):
        src = args[mem_idx + 1]
    if src:
        memory_name = Path(src).name
        print(f"Pipeline: chunk → sync SharePoint → embed for {src}\n")
        if not _run("chunk_markdown.py", ["--path", src]):
            sys.exit(1)
        if not _run("sync_sharepoint_urls.py", ["--memory", memory_name]):
            sys.exit(1)
        embed_args = ["--memory", memory_name]
        if replace:
            embed_args.append("--replace")
        if not _run("embed_and_index.py", embed_args):
            sys.exit(1)
        print("\nDone: indexed.")
        return

    print("Usage:")
    print("  python index_memory.py --path <source_folder>   # full pipeline")
    print("  python index_memory.py --path <source_folder>  # chunk + embed (convert already ran)")
    print("  python index_memory.py --replace                # rebuild entire index")


if __name__ == "__main__":
    main()
