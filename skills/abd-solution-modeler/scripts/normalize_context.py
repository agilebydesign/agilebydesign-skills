#!/usr/bin/env python3
"""Phase 1: Normalize context into rule_chunks.json.

Accepts chunk_index.json (from abd-context-to-memory) or --context-path for raw markdown.
Output: rule_chunks.json with chunk_id, source, text per chunk.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent


def _stable_id(path: str, content: str) -> str:
    return hashlib.sha256(f"{path}:{content[:200]}".encode()).hexdigest()[:12]


def from_chunk_index(chunk_index_path: Path) -> list[dict]:
    """Read chunk_index.json, load each chunk file, produce rule_chunks."""
    data = json.loads(chunk_index_path.read_text(encoding="utf-8"))
    context_path = Path(data["context_path"]).resolve()
    chunks = data.get("chunks", [])

    rule_chunks = []
    for info in chunks:
        chunk_path = context_path / info["path"]
        if not chunk_path.exists():
            continue
        text = chunk_path.read_text(encoding="utf-8", errors="replace").strip()
        if not text:
            continue
        chunk_id = info.get("chunk_id", _stable_id(info["path"], text))
        rule_chunks.append({
            "chunk_id": chunk_id,
            "source": info["path"],
            "text": text,
        })
    return rule_chunks


def from_context_path(context_path: Path) -> list[dict]:
    """Scan folder for .md files, produce rule_chunks."""
    rule_chunks = []
    for md in sorted(context_path.rglob("*.md")):
        text = md.read_text(encoding="utf-8", errors="replace").strip()
        if not text:
            continue
        rel = str(md.relative_to(context_path))
        chunk_id = _stable_id(rel, text)
        rule_chunks.append({
            "chunk_id": chunk_id,
            "source": rel,
            "text": text,
        })
    return rule_chunks


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 1: Normalize context to rule_chunks.json")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--chunk-index", help="Path to chunk_index.json (from abd-context-to-memory)")
    group.add_argument("--context-path", help="Path to folder of markdown files")
    parser.add_argument("--output", "-o", help="Output path for rule_chunks.json")
    args = parser.parse_args()

    if args.chunk_index:
        rule_chunks = from_chunk_index(Path(args.chunk_index).resolve())
    else:
        ctx = Path(args.context_path).resolve()
        if not ctx.exists():
            print(f"Context path does not exist: {ctx}", file=sys.stderr)
            sys.exit(1)
        rule_chunks = from_context_path(ctx)

    from _config import output_dir
    out_dir = output_dir()
    output_path = Path(args.output).resolve() if args.output else out_dir / "rule_chunks.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(rule_chunks, indent=2), encoding="utf-8")
    print(f"Normalized {len(rule_chunks)} chunks -> {output_path}")


if __name__ == "__main__":
    main()
