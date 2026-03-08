#!/usr/bin/env python3
"""Scaffold a new ace-skill. Thin entry point — delegates to engine."""
import argparse
import sys
from pathlib import Path

_skill_dir = Path(__file__).resolve().parent.parent
_shaping_scripts = _skill_dir.parent / "abd-shaping" / "scripts"
if not _shaping_scripts.exists() or not (_shaping_scripts / "engine.py").exists():
    print("ERROR: abd-shaping not found. Install abd-shaping first.")
    sys.exit(1)
if str(_shaping_scripts) not in sys.path:
    sys.path.insert(0, str(_shaping_scripts))

from engine import scaffold_skill


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a new ace-skill")
    parser.add_argument("--name", required=True, help="Skill name (e.g. ace-foo)")
    parser.add_argument(
        "--path",
        default=None,
        help="Output path (default: skills/<name> relative to repo root)",
    )
    args = parser.parse_args()

    path = args.path or f"skills/{args.name}"
    engine_root = _skill_dir.parent.parent  # repo root for relative paths
    result = scaffold_skill(args.name, path, engine_root=engine_root)
    print(f"Scaffolded {args.name} at {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
