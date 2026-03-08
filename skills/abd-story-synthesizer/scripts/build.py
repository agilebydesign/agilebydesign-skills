#!/usr/bin/env python3
"""Build AGENTS.md from content; get instructions for an operation; or run validation scanners."""
import json
import sys
from pathlib import Path

_skill_dir = Path(__file__).resolve().parent.parent
_scripts_dir = Path(__file__).resolve().parent
_shaping_scripts = _skill_dir.parent / "abd-shaping" / "scripts"
if not _shaping_scripts.exists() or not (_shaping_scripts / "engine.py").exists():
    print("ERROR: abd-shaping not found. Install abd-shaping first.", file=sys.stderr)
    sys.exit(1)
if str(_shaping_scripts) not in sys.path:
    sys.path.insert(0, str(_shaping_scripts))
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

from engine import AgileContextEngine, build_skill


def _run_validate(target_path: Path | None = None) -> None:
    """Run scanners on interaction tree and state model. Exit 1 if violations."""
    from scanners.registry import run_scanners, scanner_mode

    mode = scanner_mode()
    print(f"Scanner mode: {mode}")

    engine_root = _skill_dir.parent.parent if (_skill_dir.parent / "abd-shaping").exists() else _skill_dir.parent
    out_dir = engine_root / "story-synthesizer"
    if target_path and target_path.exists():
        paths = [target_path]
    else:
        paths = [
            out_dir / "interaction-tree.md",
            out_dir / "state-model.md",
        ]
        paths = [p for p in paths if p.exists()]

    if not paths:
        print("No validation targets found. Run on a slice first or pass path: python build.py validate [path]", file=sys.stderr)
        sys.exit(1)

    all_violations = []
    for p in paths:
        content = p.read_text(encoding="utf-8")
        violations = run_scanners(content, source_path=str(p))
        all_violations.extend(violations)

    for v in all_violations:
        print(f"[{v.severity}] {v.rule_id}: {v.message}")
        print(f"  {v.location}")
        if v.snippet:
            print(f"  snippet: {v.snippet[:80]}...")
        print()

    if all_violations:
        print(f"Validation found {len(all_violations)} violation(s) - create a violation report to address them")
    else:
        print("Validation passed: no violations")


def _get_instructions(operation: str, strategy_path: Path | None = None) -> None:
    """Load engine, get abd-story-synthesizer skill, print display_content(operation)."""
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
    engine = AgileContextEngine(engine_root=engine_root, strategy_path_override=strategy_path).load()
    skill = engine.get_skill("abd-story-synthesizer") or (engine.skills[0] if engine.skills else None)
    if not skill:
        print("ERROR: No abd-story-synthesizer skill loaded.", file=sys.stderr)
        sys.exit(1)
    print(skill.instructions.display_content(operation))


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "get_instructions":
        if len(sys.argv) < 3:
            print("Usage: python build.py get_instructions <operation> [--strategy path]", file=sys.stderr)
            print("Operations: create_strategy, run_slice, generate_slice, validate_run, validate_slice, improve_strategy", file=sys.stderr)
            sys.exit(1)
        strategy_path = None
        args = sys.argv[2:]
        if "--strategy" in args:
            idx = args.index("--strategy")
            if idx + 1 < len(args):
                strategy_path = Path(args[idx + 1]).resolve()
                args = args[:idx] + args[idx + 2:]
        operation = args[0] if args else None
        if not operation:
            print("Usage: python build.py get_instructions <operation> [--strategy path]", file=sys.stderr)
            sys.exit(1)
        _get_instructions(operation, strategy_path=strategy_path)
    elif len(sys.argv) >= 2 and sys.argv[1] == "validate":
        target = Path(sys.argv[2]).resolve() if len(sys.argv) >= 3 else None
        _run_validate(target_path=target)
    else:
        out = build_skill(_skill_dir, engine_root=_skill_dir)
        print(f"Wrote {out}")
