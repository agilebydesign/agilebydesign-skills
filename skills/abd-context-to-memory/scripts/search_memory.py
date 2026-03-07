"""
Search memory using semantic (vector) retrieval.

Usage:
  python search_memory.py "agile transformation approach" [--k 5] [--format text|json]

Run from workspace root. Returns top-k chunks from the vector index.
Requires: pip install openai faiss-cpu numpy
Set OPENAI_API_KEY environment variable.
"""

import json
import os
import sys
from pathlib import Path

from _config import ROOT, ensure_root

ensure_root()
RAG_DIR = ROOT / "data" / "rag"
INDEX_FILE = RAG_DIR / "index.faiss"
METADATA_FILE = RAG_DIR / "metadata.json"
EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_K = 5


def _embed_query(query: str) -> list[float]:
    """Embed query via OpenAI API."""
    from openai import OpenAI

    client = OpenAI()
    resp = client.embeddings.create(model=EMBEDDING_MODEL, input=[query])
    return resp.data[0].embedding


def search(query: str, k: int = DEFAULT_K) -> list[dict]:
    """Return top-k chunks with content, source, and score."""
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is required.", file=sys.stderr)
        sys.exit(1)

    try:
        import numpy as np
        import faiss
    except ImportError as e:
        print(f"Missing dependency: {e}", file=sys.stderr)
        print("Run: pip install openai faiss-cpu numpy", file=sys.stderr)
        sys.exit(1)

    if not INDEX_FILE.exists() or not METADATA_FILE.exists():
        print("No vector index found. Run embed_and_index.py first.", file=sys.stderr)
        sys.exit(1)

    with open(METADATA_FILE, encoding="utf-8") as f:
        data = json.load(f)
    metadata = data["chunks"] if isinstance(data, dict) and "chunks" in data else data

    index = faiss.read_index(str(INDEX_FILE))

    q_embedding = np.array(_embed_query(query), dtype="float32")
    q_norm = np.linalg.norm(q_embedding)
    if q_norm > 0:
        q_embedding = (q_embedding / q_norm).astype("float32")
    q_embedding = q_embedding.reshape(1, -1)

    k = min(k, len(metadata))
    scores, indices = index.search(q_embedding, k)

    out = []
    for idx, score in zip(indices[0], scores[0]):
        if idx < 0 or idx >= len(metadata):
            continue
        m = metadata[idx]
        out.append({
            "content": m.get("content", ""),
            "source": m.get("source", m.get("path", "")),
            "path": m.get("path", ""),
            "score": round(float(score), 3),
        })
    return out


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("--"):
        print("Usage: python search_memory.py \"<query>\" [--k 5] [--format text|json]")
        return

    query = args[0]
    k = DEFAULT_K
    fmt = "text"
    i = 1
    while i < len(args):
        if args[i] == "--k" and i + 1 < len(args):
            k = int(args[i + 1])
            i += 2
        elif args[i] == "--format" and i + 1 < len(args):
            fmt = args[i + 1].lower()
            i += 2
        else:
            i += 1

    results = search(query, k=k)

    if fmt == "json":
        print(json.dumps(results, indent=2))
    else:
        for i, r in enumerate(results, 1):
            src = r.get("source") or r.get("path") or ""
            score = r.get("score")
            print(f"--- Result {i} ({src})" + (f" score={score}" if score else "") + " ---")
            print(r["content"][:500] + ("..." if len(r["content"]) > 500 else ""))
            print()


if __name__ == "__main__":
    main()
