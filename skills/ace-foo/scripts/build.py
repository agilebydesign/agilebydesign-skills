#!/usr/bin/env python3
"""Build AGENTS.md from content. Thin entry point — delegates to engine."""
import sys
from pathlib import Path

# Add engine to path when run from skill dir
_skill_dir = Path(__file__).resolve().parent.parent
_engine_root = _skill_dir.parent.parent  # skills/ace-<name> -> skills -> repo root
if str(_engine_root) not in sys.path:
    sys.path.insert(0, str(_engine_root))

from src.engine import build_skill

if __name__ == "__main__":
    out = build_skill(_skill_dir, engine_root=_engine_root)
    print(f"Wrote {out}")
