#!/usr/bin/env python3
"""Extract behavioral variation axes from chunks — mode/type/category differences."""
import argparse
import json
import re
from pathlib import Path

VARIATION_PATTERNS = [
    re.compile(r"(close|melee)\s+(?:vs\.?|versus|or)\s+(ranged|remote|distant)", re.IGNORECASE),
    re.compile(r"(different|various|multiple)\s+(types?|kinds?|categories|modes?|forms?|variants?)", re.IGNORECASE),
    re.compile(r"depending\s+on\s+(.+?)(?:\.|;|,|$)", re.IGNORECASE),
    re.compile(r"one\s+of\s+the\s+following", re.IGNORECASE),
    re.compile(r"(?:either|choose)\s+(.+?)\s+or\s+(.+?)(?:\.|;|$)", re.IGNORECASE),
    re.compile(r"(type|mode|category|kind|variant|form)\s*:\s*(.+?)(?:\.|;|$)", re.IGNORECASE),
    re.compile(r"each\s+(type|mode|category|kind)\s+(?:has|uses|requires|provides)", re.IGNORECASE),
]


def extract_variations(chunks_path: Path, chunk_index: dict) -> list[dict]:
    variations = []
    var_id = 0

    for chunk_info in chunk_index.get("chunks", []):
        chunk_path = chunks_path / chunk_info["path"]
        if not chunk_path.exists():
            continue
        content = chunk_path.read_text(encoding="utf-8", errors="replace")

        for line in content.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            for pattern in VARIATION_PATTERNS:
                for match in pattern.finditer(line):
                    variations.append({
                        "variation_id": f"var_{var_id:04d}",
                        "axis": match.group(0).strip()[:120],
                        "source_chunk": chunk_info["chunk_id"],
                        "raw": line[:200],
                    })
                    var_id += 1

    return variations


def main():
    parser = argparse.ArgumentParser(description="Extract variations from context chunks")
    parser.add_argument("--chunks", required=True, help="Path to chunk_index.json")
    parser.add_argument("--output", default=None, help="Output path for variations.json")
    args = parser.parse_args()

    index_path = Path(args.chunks).resolve()
    chunk_index = json.loads(index_path.read_text(encoding="utf-8"))
    chunks_path = Path(chunk_index["context_path"]).resolve()

    variations = extract_variations(chunks_path, chunk_index)

    output_path = Path(args.output) if args.output else index_path.parent.parent / "evidence" / "variations.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(variations, indent=2), encoding="utf-8")
    print(f"Extracted {len(variations)} variations -> {output_path}")


if __name__ == "__main__":
    main()
