#!/usr/bin/env python3
"""Build AGENTS.md from content. Thin entry point — delegates to engine."""
import sys
from pathlib import Path

_skill_dir = Path(__file__).resolve().parent.parent
_shaping_scripts = _skill_dir.parent / "ace-shaping" / "scripts"
if not _shaping_scripts.exists() or not (_shaping_scripts / "engine.py").exists():
    print("ERROR: ace-shaping not found. Install ace-shaping first.")
    sys.exit(1)
if str(_shaping_scripts) not in sys.path:
    sys.path.insert(0, str(_shaping_scripts))

from engine import build_skill

if __name__ == "__main__":
    out = build_skill(_skill_dir, engine_root=_skill_dir)
    print(f"Wrote {out}")
