#!/usr/bin/env python3
"""Analyze and index existing chunks from abd-context-to-memory.

Validates chunk readiness, builds a chunk index with stable IDs,
source locations, and section mapping. Does NOT re-chunk.
"""
import argparse
import hashlib
import json
from pathlib import Path


def _stable_id(path: str, content: str) -> str:
    return hashlib.sha256(f"{path}:{content[:200]}".encode()).hexdigest()[:12]


def analyze_chunks(context_path: Path) -> dict:
    chunks = []
    seen_hashes: dict[str, str] = {}
    duplicates = []

    md_files = sorted(context_path.rglob("*.md"))
    if not md_files:
        return {"error": f"No markdown chunks found in {context_path}", "chunks": []}

    for md in md_files:
        content = md.read_text(encoding="utf-8", errors="replace").strip()
        if not content:
            continue

        content_hash = hashlib.md5(content.encode()).hexdigest()
        rel_path = str(md.relative_to(context_path))
        chunk_id = _stable_id(rel_path, content)

        if content_hash in seen_hashes:
            duplicates.append({
                "chunk_id": chunk_id,
                "path": rel_path,
                "duplicate_of": seen_hashes[content_hash],
            })
            continue

        seen_hashes[content_hash] = rel_path

        heading = ""
        for line in content.split("\n"):
            if line.startswith("#"):
                heading = line.lstrip("#").strip()
                break

        chunks.append({
            "chunk_id": chunk_id,
            "path": rel_path,
            "heading": heading,
            "char_count": len(content),
            "line_count": content.count("\n") + 1,
        })

    return {
        "context_path": str(context_path),
        "total_chunks": len(chunks),
        "total_duplicates": len(duplicates),
        "chunks": chunks,
        "duplicates": duplicates,
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze and index existing context chunks")
    parser.add_argument("--context-path", required=True, help="Path to chunked context directory")
    parser.add_argument("--output", default=None, help="Output path for chunk_index.json")
    args = parser.parse_args()

    context_path = Path(args.context_path).resolve()
    if not context_path.exists():
        print(f"Error: context path does not exist: {context_path}")
        return

    result = analyze_chunks(context_path)

    output_dir = Path(args.output).parent if args.output else context_path.parent / "normalized"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.output) if args.output else output_dir / "chunk_index.json"

    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Chunk index: {result['total_chunks']} chunks, {result['total_duplicates']} duplicates")
    print(f"Written to: {output_path}")


if __name__ == "__main__":
    main()
