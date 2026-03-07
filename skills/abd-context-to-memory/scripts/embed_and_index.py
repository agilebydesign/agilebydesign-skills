"""
Embed chunked markdown and index for semantic search.

Uses OpenAI embeddings (pure Python, no native compilation).
Works on Python 3.13, Windows ARM64, and any platform.

Usage:
  python embed_and_index.py [--memory <memory_name>]
  python embed_and_index.py  # index all memory

Run from workspace root. Reads chunked .md from memory/<name>/ (no chunked subfolder).
Writes to data/rag/. Requires: pip install openai faiss-cpu numpy
Set OPENAI_API_KEY environment variable.
"""

import json
import os
import re
import sys
from pathlib import Path

from _config import ROOT, MEMORY, ensure_root

ensure_root()
RAG_DIR = ROOT / "data" / "rag"
EMBEDDINGS_FILE = RAG_DIR / "embeddings.npy"
METADATA_FILE = RAG_DIR / "metadata.json"
CHECKPOINT_EMBED = RAG_DIR / "checkpoint_embeddings.npy"
CHECKPOINT_PROGRESS = RAG_DIR / "checkpoint_progress.json"
CHECKPOINT_INTERVAL = 200  # save every N batches
EMBEDDING_MODEL = "text-embedding-3-small"
# text-embedding-3-small limit: 8191 tokens per input. ~4 chars/token.
MAX_CHARS_PER_CHUNK = 8000  # ~2000 tokens, safe under 8191
BATCH_SIZE = 8


def _split_long_chunk(text: str, max_chars: int = MAX_CHARS_PER_CHUNK) -> list[str]:
    """Split text into sub-chunks under max_chars. Prefer paragraph boundaries."""
    if len(text) <= max_chars:
        return [text]
    parts = []
    remaining = text
    while remaining:
        if len(remaining) <= max_chars:
            parts.append(remaining)
            break
        # Try to split at paragraph (double newline)
        chunk = remaining[: max_chars + 1]
        last_para = chunk.rfind("\n\n")
        if last_para > max_chars // 2:
            cut = last_para + 2
        else:
            # Fall back to single newline
            last_nl = chunk.rfind("\n")
            cut = last_nl + 1 if last_nl > max_chars // 2 else max_chars
        parts.append(remaining[:cut].strip())
        remaining = remaining[cut:].lstrip()
    return [p for p in parts if len(p) >= 20]


def _extract_source(text: str) -> str | None:
    m = re.search(r"<!--\s*Source:\s*([^|>]+)", text)
    return m.group(1).strip() if m else None


def _chunk_text_for_embed(text: str) -> str:
    """Strip HTML comments for embedding; keep meaningful content."""
    lines = []
    for line in text.split("\n"):
        if line.strip().startswith("<!--") and line.strip().endswith("-->"):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def collect_chunks(memory_name: str | None) -> list[tuple[Path, str, dict]]:
    """Collect chunk files from memory folder. Returns [(path, text, metadata), ...].
    Chunked files are in memory/<name>/*.md (no chunked subfolder).
    """
    chunks = []
    base = MEMORY / memory_name if memory_name else MEMORY
    if not base.exists():
        return chunks

    for md_path in base.rglob("*.md"):
        if "images" in md_path.parts:
            continue
        try:
            text = md_path.read_text(encoding="utf-8")
        except Exception:
            continue
        source = _extract_source(text)
        clean = _chunk_text_for_embed(text)
        if len(clean) < 20:
            continue
        try:
            rel = md_path.relative_to(MEMORY)
        except ValueError:
            rel = md_path
        meta = {
            "source": source or str(rel),
            "path": str(rel),
            "file": md_path.name,
        }
        chunks.append((md_path, clean, meta))
    return chunks


def _embed_with_openai(
    texts: list[str],
    metadata: list[dict],
    checkpoint_cb=None,
) -> list[list[float]]:
    """Call OpenAI embedding API. Batches requests. Supports checkpoint/resume."""
    from openai import OpenAI

    client = OpenAI()
    all_embeddings = []
    total = (len(texts) + BATCH_SIZE - 1) // BATCH_SIZE
    start_batch = 0

    # Resume from checkpoint if valid
    if CHECKPOINT_PROGRESS.exists():
        try:
            import numpy as np
            with open(CHECKPOINT_PROGRESS, encoding="utf-8") as f:
                prog = json.load(f)
            if prog.get("n_documents") == len(texts):
                start_batch = prog.get("last_batch", 0)
                if start_batch > 0 and CHECKPOINT_EMBED.exists():
                    all_embeddings = np.load(CHECKPOINT_EMBED).tolist()
                    if len(all_embeddings) == start_batch * BATCH_SIZE:
                        print(f"Resuming from batch {start_batch + 1}/{total}...", flush=True)
                    else:
                        start_batch = 0
                        all_embeddings = []
        except (json.JSONDecodeError, ValueError, OSError):
            pass

    for i in range(start_batch * BATCH_SIZE, len(texts), BATCH_SIZE):
        batch_num = i // BATCH_SIZE + 1
        if total > 1 and batch_num % 100 == 0:
            print(f"  batch {batch_num}/{total}...", flush=True)
        batch = texts[i : i + BATCH_SIZE]
        resp = client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
        for d in resp.data:
            all_embeddings.append(d.embedding)

        # Checkpoint every N batches
        if checkpoint_cb and batch_num % CHECKPOINT_INTERVAL == 0:
            checkpoint_cb(batch_num, all_embeddings, metadata[: len(all_embeddings)])
    return all_embeddings


def index_chunks(chunks: list[tuple[Path, str, dict]], replace: bool = False) -> int:
    """Embed chunks and save to FAISS + metadata."""
    if not chunks:
        return 0

    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is required.")
        print("Get an API key from https://platform.openai.com/api-keys")
        sys.exit(1)

    try:
        import numpy as np
        import faiss
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Run: pip install openai faiss-cpu numpy")
        sys.exit(1)

    RAG_DIR.mkdir(parents=True, exist_ok=True)

    # Split long chunks into sub-chunks under API token limit
    expanded = []
    for path, text, meta in chunks:
        for sub in _split_long_chunk(text):
            expanded.append((path, sub, meta))

    # Safety: truncate any chunk still over limit (avoids 400 from token overflow)
    documents = []
    for _, text, _ in expanded:
        if len(text) > MAX_CHARS_PER_CHUNK:
            text = text[:MAX_CHARS_PER_CHUNK]
        documents.append(text)

    new_metadata = []
    for path, text, meta in expanded:
        new_metadata.append({
            "path": meta.get("path", ""),
            "source": meta.get("source", meta.get("path", "")),
            "content": text,
        })

    def save_checkpoint(batch_idx: int, emb: list, _meta: list):
        np.save(CHECKPOINT_EMBED, np.array(emb, dtype="float32"))
        with open(CHECKPOINT_PROGRESS, "w", encoding="utf-8") as f:
            json.dump({"last_batch": batch_idx, "total_batches": (len(documents) + BATCH_SIZE - 1) // BATCH_SIZE, "n_documents": len(documents)}, f)

    if replace and CHECKPOINT_PROGRESS.exists():
        for f in (CHECKPOINT_EMBED, CHECKPOINT_PROGRESS):
            if f.exists():
                f.unlink()

    print(f"Calling OpenAI embedding API ({len(documents)} chunks)...")
    embeddings_list = _embed_with_openai(documents, new_metadata, checkpoint_cb=save_checkpoint)
    new_embeddings = np.array(embeddings_list, dtype="float32")

    # Clear checkpoint on success
    for f in (CHECKPOINT_EMBED, CHECKPOINT_PROGRESS):
        if f.exists():
            f.unlink()
    # L2 normalize for cosine similarity via dot product
    norms = np.linalg.norm(new_embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1
    new_embeddings = (new_embeddings / norms).astype("float32")

    if replace or not EMBEDDINGS_FILE.exists():
        all_embeddings = new_embeddings.astype("float32")
        all_metadata = new_metadata
    else:
        existing = np.load(EMBEDDINGS_FILE)
        with open(METADATA_FILE, encoding="utf-8") as f:
            existing_meta = json.load(f)
        # Dedupe by path: drop existing entries whose path is in new chunks
        new_paths = {m["path"] for m in new_metadata}
        keep = [i for i, m in enumerate(existing_meta) if m["path"] not in new_paths]
        all_embeddings = np.vstack([existing[keep], new_embeddings.astype("float32")])
        all_metadata = [existing_meta[i] for i in keep] + new_metadata

    np.save(EMBEDDINGS_FILE, all_embeddings)
    meta_out = {"model": EMBEDDING_MODEL, "chunks": all_metadata}
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(meta_out, f, ensure_ascii=False, indent=None)

    index = faiss.IndexFlatIP(all_embeddings.shape[1])
    index.add(all_embeddings)
    faiss.write_index(index, str(RAG_DIR / "index.faiss"))

    return len(chunks)


def main():
    memory_name = None
    if "--memory" in sys.argv:
        idx = sys.argv.index("--memory")
        if idx + 1 < len(sys.argv):
            memory_name = sys.argv[idx + 1]
    if memory_name is None and "--path" in sys.argv:
        idx = sys.argv.index("--path")
        if idx + 1 < len(sys.argv):
            memory_name = Path(sys.argv[idx + 1]).name
    replace = "--replace" in sys.argv

    chunks = collect_chunks(memory_name)
    if not chunks:
        scope = f"memory/{memory_name}" if memory_name else "memory/"
        print(f"No chunks found under {scope}")
        print("Run convert_to_markdown and chunk_markdown first.")
        return

    print(f"Indexing {len(chunks)} chunks...")
    n = index_chunks(chunks, replace=replace)
    print(f"Done: {n} chunks indexed to {RAG_DIR}")


if __name__ == "__main__":
    main()
