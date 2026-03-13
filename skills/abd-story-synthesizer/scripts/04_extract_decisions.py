#!/usr/bin/env python3
"""Extract decision/rule logic from chunks — conditional triggers and outcomes."""
import argparse
import json
import re
from pathlib import Path

DECISION_TRIGGERS = re.compile(
    r"(if|when|unless|must|may not|on success|on failure|provided that|as long as|except when|only if|in case of)\s+(.+?)(?:\.|;|$)",
    re.IGNORECASE,
)

OUTCOME_PATTERN = re.compile(
    r"(?:->|→|then|result(?:s? in)?|outcome)\s+(.+?)(?:\.|;|$)",
    re.IGNORECASE,
)


def extract_decisions(chunks_path: Path, chunk_index: dict) -> list[dict]:
    decisions = []
    dec_id = 0

    for chunk_info in chunk_index.get("chunks", []):
        chunk_path = chunks_path / chunk_info["path"]
        if not chunk_path.exists():
            continue
        content = chunk_path.read_text(encoding="utf-8", errors="replace")

        for line in content.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            for match in DECISION_TRIGGERS.finditer(line):
                trigger = match.group(1).strip()
                condition = match.group(2).strip()[:150]

                outcome_match = OUTCOME_PATTERN.search(line[match.end():])
                outcome = outcome_match.group(1).strip()[:120] if outcome_match else ""

                decisions.append({
                    "decision_id": f"dec_{dec_id:04d}",
                    "trigger": trigger,
                    "condition": condition,
                    "outcome": outcome,
                    "source_chunk": chunk_info["chunk_id"],
                    "raw": line[:200],
                })
                dec_id += 1

    return decisions


def main():
    parser = argparse.ArgumentParser(description="Extract decisions from context chunks")
    parser.add_argument("--chunks", required=True, help="Path to chunk_index.json")
    parser.add_argument("--output", default=None, help="Output path for decisions.json")
    args = parser.parse_args()

    index_path = Path(args.chunks).resolve()
    chunk_index = json.loads(index_path.read_text(encoding="utf-8"))
    chunks_path = Path(chunk_index["context_path"]).resolve()

    decisions = extract_decisions(chunks_path, chunk_index)

    output_path = Path(args.output) if args.output else index_path.parent.parent / "extracted" / "decisions.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(decisions, indent=2), encoding="utf-8")
    print(f"Extracted {len(decisions)} decisions -> {output_path}")


if __name__ == "__main__":
    main()
