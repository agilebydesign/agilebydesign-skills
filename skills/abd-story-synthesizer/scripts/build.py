#!/usr/bin/env python3
"""Build AGENTS.md from content; get instructions for an operation; or run validation scanners."""
import json
import sys
from pathlib import Path

_skill_dir = Path(__file__).resolve().parent.parent
_scripts_dir = Path(__file__).resolve().parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

from engine import AgileContextEngine, build_skill


def _parse_engine_root(args: list[str]) -> tuple[Path | None, list[str]]:
    """Extract --engine-root from args if present. Returns (engine_root or None, remaining_args)."""
    out: list[str] = []
    engine_root: Path | None = None
    i = 0
    while i < len(args):
        if args[i] == "--engine-root" and i + 1 < len(args):
            engine_root = Path(args[i + 1]).resolve()
            i += 2
            continue
        out.append(args[i])
        i += 1
    return engine_root, out


def _resolve_engine_root(override: Path | None) -> Path:
    """Resolve engine_root: --engine-root override, or project config, or skill dir."""
    if override:
        return override.resolve()
    project_config = _skill_dir.parent.parent / "conf" / "abd-config.json"
    if project_config.exists():
        return _skill_dir.parent.parent
    return _skill_dir.parent


def _run_validate(target_path: Path | None = None, engine_root_override: Path | None = None) -> None:
    """Run scanners on interaction tree and state model. Exit 1 if violations."""
    from scanners.registry import run_scanners, scanner_mode

    mode = scanner_mode()
    print(f"Scanner mode: {mode}")

    engine_root = _resolve_engine_root(engine_root_override)
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


def _get_instructions(operation: str, strategy_path: Path | None = None, engine_root_override: Path | None = None) -> None:
    """Load engine, get abd-story-synthesizer skill, print display_content(operation)."""
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout.reconfigure(encoding="utf-8")
    engine_root = _resolve_engine_root(engine_root_override)
    config_path = _skill_dir / "conf" / "abd-config.json"
    project_config = engine_root / "conf" / "abd-config.json"
    if not engine_root_override and not project_config.exists():
        alt = _skill_dir.parent.parent / "conf" / "abd-config.json"
        if alt.exists():
            engine_root = _skill_dir.parent.parent
            project_config = alt
    if not project_config.exists() and not config_path.exists():
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
    args = sys.argv[1:]
    engine_root_override, args = _parse_engine_root(args)

    if args and args[0] == "get_instructions":
        if len(args) < 2:
            print("Usage: python build.py get_instructions <operation> [--strategy path] [--engine-root path]", file=sys.stderr)
            print("Operations: create_strategy, run_slice, generate_slice, validate_run, validate_slice, improve_strategy", file=sys.stderr)
            sys.exit(1)
        strategy_path = None
        rest = args[1:]
        if "--strategy" in rest:
            idx = rest.index("--strategy")
            if idx + 1 < len(rest):
                strategy_path = Path(rest[idx + 1]).resolve()
                rest = rest[:idx] + rest[idx + 2:]
        operation = rest[0] if rest else None
        if not operation:
            print("Usage: python build.py get_instructions <operation> [--strategy path] [--engine-root path]", file=sys.stderr)
            sys.exit(1)
        _get_instructions(operation, strategy_path=strategy_path, engine_root_override=engine_root_override)
    elif args and args[0] == "validate":
        target = Path(args[1]).resolve() if len(args) >= 2 else None
        _run_validate(target_path=target, engine_root_override=engine_root_override)
    else:
        out = build_skill(_skill_dir, engine_root=_skill_dir)
        print(f"Wrote {out}")
