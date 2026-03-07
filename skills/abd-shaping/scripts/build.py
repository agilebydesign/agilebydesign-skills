#!/usr/bin/env python3
"""Build AGENTS.md from content; or get assembled instructions for an operation."""
import json
import sys
from pathlib import Path

_skill_dir = Path(__file__).resolve().parent.parent
_scripts_dir = Path(__file__).resolve().parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

from engine import AgileContextEngine, build_skill


def _get_instructions(operation: str) -> None:
    """Load engine, get abd-shaping skill, print display_content(operation)."""
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout.reconfigure(encoding="utf-8")
    engine_root = _skill_dir
    config_path = _skill_dir / "conf" / "abd-config.json"
    project_config = _skill_dir.parent.parent / "conf" / "abd-config.json"
    if project_config.exists():
        engine_root = _skill_dir.parent.parent
    elif not config_path.exists():
        _skill_dir.joinpath("conf").mkdir(parents=True, exist_ok=True)
        config_path.write_text(
            json.dumps({
                "skills": ["."],
                "skills_config": {"order": ["."]},
                "context_paths": [],
            }, indent=2),
            encoding="utf-8",
        )
    engine = AgileContextEngine(engine_root=engine_root).load()
    skill = engine.get_skill("abd-shaping") or (engine.skills[0] if engine.skills else None)
    if not skill:
        print("ERROR: No abd-shaping skill loaded.", file=sys.stderr)
        sys.exit(1)
    print(skill.instructions.display_content(operation))


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "get_instructions":
        if len(sys.argv) < 3:
            print("Usage: python build.py get_instructions <operation>", file=sys.stderr)
            print("Operations: create_strategy, generate_slice, improve_strategy", file=sys.stderr)
            sys.exit(1)
        _get_instructions(sys.argv[2])
    else:
        out = build_skill(_skill_dir, engine_root=_skill_dir)
        print(f"Wrote {out}")
