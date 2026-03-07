#!/usr/bin/env python3
"""Build AGENTS.md from content. Thin entry point — delegates to engine."""
import sys
from pathlib import Path

_skill_dir = Path(__file__).resolve().parent.parent
_scripts_dir = Path(__file__).resolve().parent
# Engine lives in ace-shaping/scripts/ — this skill has it, others use sibling
if _skill_dir.name == "ace-shaping":
    _engine_dir = str(_scripts_dir)
else:
    _shaping_scripts = _skill_dir.parent / "ace-shaping" / "scripts"
    if not _shaping_scripts.exists() or not (_shaping_scripts / "engine.py").exists():
        print("ERROR: ace-shaping not found. Install ace-shaping first:")
        print("  npx skills add agilebydesign/agile-context-engine --skill ace-shaping --skill <this-skill>")
        sys.exit(1)
    _engine_dir = str(_shaping_scripts)
if _engine_dir not in sys.path:
    sys.path.insert(0, _engine_dir)

from engine import build_skill

if __name__ == "__main__":
    out = build_skill(_skill_dir, engine_root=_skill_dir)
    print(f"Wrote {out}")
