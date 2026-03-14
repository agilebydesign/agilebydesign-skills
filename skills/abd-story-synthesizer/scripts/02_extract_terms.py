#!/usr/bin/env python3
"""Extract terms (noun phrases, defined terms, repeated vocabulary) from chunks.

Builds a concept index — terms are index entries, NOT class candidates.
"""
import argparse
import json
import re
from collections import Counter
from pathlib import Path


def _extract_noun_candidates(text: str) -> list[str]:
    """Extract capitalized phrases and bold terms as noun candidates."""
    candidates = []
    bold_pattern = re.compile(r"\*\*([A-Z][A-Za-z\s]+?)\*\*")
    candidates.extend(bold_pattern.findall(text))

    cap_pattern = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b")
    candidates.extend(cap_pattern.findall(text))

    heading_pattern = re.compile(r"^#+\s+(.+)$", re.MULTILINE)
    candidates.extend(heading_pattern.findall(text))

    return [c.strip() for c in candidates if len(c.strip()) > 2]


def extract_terms(chunks_path: Path, chunk_index: dict) -> list[dict]:
    terms_counter: Counter = Counter()
    term_occurrences: dict[str, list[str]] = {}

    for chunk_info in chunk_index.get("chunks", []):
        chunk_path = chunks_path / chunk_info["path"]
        if not chunk_path.exists():
            continue
        content = chunk_path.read_text(encoding="utf-8", errors="replace")
        candidates = _extract_noun_candidates(content)

        for term in candidates:
            normalized = term.strip()
            terms_counter[normalized] += 1
            if normalized not in term_occurrences:
                term_occurrences[normalized] = []
            if chunk_info["chunk_id"] not in term_occurrences[normalized]:
                term_occurrences[normalized].append(chunk_info["chunk_id"])

    terms = []
    for i, (term, count) in enumerate(terms_counter.most_common()):
        if count < 2:
            continue
        terms.append({
            "term_id": f"term_{i:04d}",
            "name": term,
            "aliases": [],
            "count": count,
            "occurrences": term_occurrences.get(term, []),
        })

    return terms


def main():
    parser = argparse.ArgumentParser(description="Extract terms from context chunks")
    parser.add_argument("--chunks", required=True, help="Path to chunk_index.json")
    parser.add_argument("--output", default=None, help="Output path for terms.json")
    args = parser.parse_args()

    index_path = Path(args.chunks).resolve()
    chunk_index = json.loads(index_path.read_text(encoding="utf-8"))
    chunks_path = Path(chunk_index["context_path"]).resolve()

    terms = extract_terms(chunks_path, chunk_index)

    output_path = Path(args.output) if args.output else index_path.parent.parent / "evidence" / "terms.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(terms, indent=2), encoding="utf-8")
    print(f"Extracted {len(terms)} terms -> {output_path}")


if __name__ == "__main__":
    main()
