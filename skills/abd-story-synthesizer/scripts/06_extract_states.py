#!/usr/bin/env python3
"""Extract stateful entities and explicit relationships from chunks."""
import argparse
import json
import re
from pathlib import Path

STATE_PATTERNS = [
    re.compile(r"(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:has|have|maintains?|tracks?|holds?|stores?|accumulates?|manages?)\s+(?:a\s+)?(.+?)(?:\.|;|$)", re.IGNORECASE),
    re.compile(r"(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:becomes?|transitions?\s+to|changes?\s+to|enters?|moves?\s+to)\s+(.+?)(?:\.|;|$)", re.IGNORECASE),
    re.compile(r"(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:is\s+)?(?:active|inactive|pending|expired|completed|cancelled|suspended|initialized|finalized)", re.IGNORECASE),
]

RELATIONSHIP_PATTERNS = [
    re.compile(r"(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:contains?|owns?|belongs?\s+to|is\s+part\s+of|includes?|consists?\s+of)\s+(.+?)(?:\.|;|$)", re.IGNORECASE),
    re.compile(r"(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:references?|depends?\s+on|uses?|requires?|collaborates?\s+with|interacts?\s+with)\s+(.+?)(?:\.|;|$)", re.IGNORECASE),
    re.compile(r"(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:is\s+a\s+type\s+of|extends?|inherits?\s+from|specializes?)\s+(.+?)(?:\.|;|$)", re.IGNORECASE),
]


def extract_states(chunks_path: Path, chunk_index: dict) -> tuple[list[dict], list[dict]]:
    states = []
    relationships = []
    s_id = 0
    r_id = 0

    for chunk_info in chunk_index.get("chunks", []):
        chunk_path = chunks_path / chunk_info["path"]
        if not chunk_path.exists():
            continue
        content = chunk_path.read_text(encoding="utf-8", errors="replace")

        for line in content.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            for pattern in STATE_PATTERNS:
                for match in pattern.finditer(line):
                    states.append({
                        "state_id": f"st_{s_id:04d}",
                        "entity": match.group(1).strip(),
                        "state_description": match.group(0).strip()[:150],
                        "source_chunk": chunk_info["chunk_id"],
                    })
                    s_id += 1

            for pattern in RELATIONSHIP_PATTERNS:
                for match in pattern.finditer(line):
                    relationships.append({
                        "relationship_id": f"rel_{r_id:04d}",
                        "from_entity": match.group(1).strip(),
                        "to_entity": match.group(2).strip()[:80],
                        "type": match.group(0).strip()[:150],
                        "source_chunk": chunk_info["chunk_id"],
                    })
                    r_id += 1

    return states, relationships


def main():
    parser = argparse.ArgumentParser(description="Extract states and relationships from chunks")
    parser.add_argument("--chunks", required=True, help="Path to chunk_index.json")
    parser.add_argument("--output-dir", default=None, help="Output directory")
    args = parser.parse_args()

    index_path = Path(args.chunks).resolve()
    chunk_index = json.loads(index_path.read_text(encoding="utf-8"))
    chunks_path = Path(chunk_index["context_path"]).resolve()

    states, relationships = extract_states(chunks_path, chunk_index)

    output_dir = Path(args.output_dir) if args.output_dir else index_path.parent.parent / "extracted"
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "states.json").write_text(json.dumps(states, indent=2), encoding="utf-8")
    (output_dir / "relationships.json").write_text(json.dumps(relationships, indent=2), encoding="utf-8")
    print(f"Extracted {len(states)} states, {len(relationships)} relationships -> {output_dir}")


if __name__ == "__main__":
    main()
