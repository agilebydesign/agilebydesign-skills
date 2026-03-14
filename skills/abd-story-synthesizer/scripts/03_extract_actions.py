#!/usr/bin/env python3
"""Extract behavioral facts as subject-verb-object patterns from chunks."""
import argparse
import json
import re
from pathlib import Path

SVO_PATTERNS = [
    re.compile(r"(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(makes?|rolls?|applies?|creates?|removes?|adds?|checks?|validates?|computes?|calculates?|determines?|selects?|triggers?|receives?|sends?|updates?|modifies?|sets?|gets?|returns?|executes?|performs?|initiates?|resolves?|assigns?|transfers?|consumes?|produces?|grants?|revokes?|enforces?)\s+(.+?)(?:\.|;|$)", re.IGNORECASE),
    re.compile(r"(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(can|must|should|may|shall)\s+(.+?)(?:\.|;|$)", re.IGNORECASE),
]


def extract_actions(chunks_path: Path, chunk_index: dict) -> list[dict]:
    actions = []
    action_id = 0

    for chunk_info in chunk_index.get("chunks", []):
        chunk_path = chunks_path / chunk_info["path"]
        if not chunk_path.exists():
            continue
        content = chunk_path.read_text(encoding="utf-8", errors="replace")

        for line in content.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            for pattern in SVO_PATTERNS:
                for match in pattern.finditer(line):
                    actions.append({
                        "action_id": f"act_{action_id:04d}",
                        "subject": match.group(1).strip(),
                        "verb": match.group(2).strip(),
                        "object": match.group(3).strip()[:120],
                        "source_chunk": chunk_info["chunk_id"],
                        "raw": match.group(0).strip()[:200],
                    })
                    action_id += 1

    return actions


def main():
    parser = argparse.ArgumentParser(description="Extract actions from context chunks")
    parser.add_argument("--chunks", required=True, help="Path to chunk_index.json")
    parser.add_argument("--output", default=None, help="Output path for actions.json")
    args = parser.parse_args()

    index_path = Path(args.chunks).resolve()
    chunk_index = json.loads(index_path.read_text(encoding="utf-8"))
    chunks_path = Path(chunk_index["context_path"]).resolve()

    actions = extract_actions(chunks_path, chunk_index)

    output_path = Path(args.output) if args.output else index_path.parent.parent / "evidence" / "actions.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(actions, indent=2), encoding="utf-8")
    print(f"Extracted {len(actions)} actions -> {output_path}")


if __name__ == "__main__":
    main()
