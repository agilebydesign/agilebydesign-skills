"""
Orchestrate full pipeline: convert → chunk → embed → index.

Usage:
  python index_memory.py --path <source_folder>   # convert, chunk, embed (full pipeline)
  python index_memory.py --memory <memory_name>   # chunk + embed (chunks already exist or convert ran)
  python index_memory.py --replace                # rebuild entire index from all memory

Run from workspace root. Requires: markitdown, openai, faiss-cpu, numpy. Set OPENAI_API_KEY.

ROOT (memory storage) is derived from the source folder: parent of source path.
Set CONTENT_MEMORY_ROOT only when running --memory without a source (chunk+embed only).
"""

import os
import subprocess
import sys
from pathlib import Path

from _config import ROOT, ensure_root, get_default_context_folder

ensure_root()
SCRIPTS = Path(__file__).resolve().parent


def _run(script: str, args: list[str], content_root: Path | None = None) -> bool:
    """Run a script; return True on success.
    When content_root is set, use it as cwd and CONTENT_MEMORY_ROOT so memory lives with the source."""
    cmd = [sys.executable, str(SCRIPTS / script)] + args
    cwd = str(content_root) if content_root else str(ROOT)
    env = os.environ.copy()
    if content_root:
        env["CONTENT_MEMORY_ROOT"] = str(content_root)
    r = subprocess.run(cmd, cwd=cwd, env=env)
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

    # --path: convert → chunk → embed (or default: skill_space_path/context when no folder specified)
    path_idx = next((i for i, a in enumerate(args) if a == "--path"), None)
    src = None
    if path_idx is not None and path_idx + 1 < len(args):
        src = args[path_idx + 1]
    elif not any(a in args for a in ("--path", "--memory")):
        default = get_default_context_folder()
        if default is not None:
            src = str(default)
            print(f"Using default context folder: {src}\n")
    if src is not None:
        src_path = Path(src).resolve()
        content_root = src_path.parent  # memory lives alongside the source project
        memory_name = src_path.name
        print(f"Pipeline: convert -> chunk -> sync SharePoint -> embed for {src}")
        print(f"Memory root: {content_root}\n")
        if not _run("convert_to_markdown.py", ["--memory", src], content_root=content_root):
            sys.exit(1)
        if not _run("chunk_markdown.py", ["--path", src], content_root=content_root):
            sys.exit(1)
        if not _run("sync_sharepoint_urls.py", ["--memory", memory_name], content_root=content_root):
            sys.exit(1)
        embed_args = ["--memory", memory_name]
        if replace:
            embed_args.append("--replace")
        if not _run("embed_and_index.py", embed_args, content_root=content_root):
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
    print("  python index_memory.py --memory <memory_name>   # chunk + embed (convert already ran)")
    print("  python index_memory.py                          # if skill_space_path set: use <skill_space_path>/context")
    print("  python index_memory.py --replace                # rebuild entire index")


if __name__ == "__main__":
    main()
