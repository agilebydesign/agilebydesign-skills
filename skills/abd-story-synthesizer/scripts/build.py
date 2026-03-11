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


def _run_validate(target_path: Path | None = None) -> None:
    """Run scanners on interaction tree and Domain Model. Exit 1 if violations."""
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout.reconfigure(encoding="utf-8")
    from scanners.registry import run_scanners, scanner_mode

    mode = scanner_mode()
    print(f"Scanner mode: {mode}")

    engine_root = _skill_dir  # Always the synthesizer skill; never changes
    # Use workspace_path from config (skill_space_path) when set; else engine_root
    try:
        engine = AgileContextEngine(engine_root=engine_root).load()
        out_dir = (engine.workspace_path or engine_root) / "story-synthesizer"
    except FileNotFoundError:
        out_dir = engine_root / "story-synthesizer"
    if target_path and target_path.exists():
        paths = [target_path]
    else:
        paths = [
            out_dir / "interaction-tree.md",
            out_dir / "domain-model.md",
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


def _discover_context() -> None:
    """Scan skill_space_path for context* files/folders and update the skill space's abd-config.json."""
    engine_root = _skill_dir
    config_path = engine_root / "conf" / "abd-config.json"
    if not config_path.exists():
        print("ERROR: conf/abd-config.json not found. Set work area first.", file=sys.stderr)
        sys.exit(1)

    config = json.loads(config_path.read_text(encoding="utf-8"))
    skill_space = config.get("skill_space_path")
    if not skill_space:
        print("ERROR: skill_space_path not set in conf/abd-config.json. Set work area first.", file=sys.stderr)
        sys.exit(1)

    skill_space_path = Path(skill_space).resolve()
    if not skill_space_path.exists():
        print(f"ERROR: skill_space_path does not exist: {skill_space_path}", file=sys.stderr)
        sys.exit(1)

    discovered = []
    for item in skill_space_path.rglob("context*"):
        if any(part.startswith(".") for part in item.parts):
            continue
        if "node_modules" in item.parts or "__pycache__" in item.parts:
            continue
        if item.is_dir() and item.name == "context":
            discovered.append(str(item.resolve()))
        elif item.is_file() and item.stem == "context":
            discovered.append(str(item.resolve()))

    ss_config_path = skill_space_path / "conf" / "abd-config.json"
    ss_config_path.parent.mkdir(parents=True, exist_ok=True)
    ss_config = {}
    if ss_config_path.exists():
        try:
            ss_config = json.loads(ss_config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            ss_config = {}

    discovered_resolved = {str(Path(p).resolve()) for p in discovered}
    manual = [p for p in ss_config.get("context_paths", []) if str(Path(p).resolve()) not in discovered_resolved]
    merged = discovered + manual

    ss_config["context_paths"] = merged
    ss_config_path.write_text(json.dumps(ss_config, indent=2), encoding="utf-8")

    print(json.dumps({
        "skill_space_path": str(skill_space_path),
        "config_written_to": str(ss_config_path),
        "manual_paths": manual,
        "discovered_paths": discovered,
        "total_context_paths": len(merged),
    }, indent=2))


def _get_config() -> None:
    """Print engine_root, skill_space_path, config_path as JSON. Use when agent needs to know paths."""
    engine_root = _skill_dir
    config_path = engine_root / "conf" / "abd-config.json"
    result = {
        "engine_root": str(engine_root.resolve()),
        "config_path": str(config_path.resolve()),
        "skill_space_path": None,
    }
    if config_path.exists():
        try:
            engine = AgileContextEngine(engine_root=engine_root).load()
            if engine.workspace_path:
                p = str(engine.workspace_path.resolve())
                result["skill_space_path"] = p
                result["skill_path"] = p  # shorthand for skill_space_path
            result["strategy_path"] = str(engine.strategy_path.resolve()) if engine.strategy_path else None
            result["context_paths"] = [str(p) for p in engine.context_paths]
        except Exception:
            pass
    print(json.dumps(result, indent=2))


def _check_context(engine: AgileContextEngine) -> None:
    """Check if context is chunked and up to date. Warn if chunking needed."""
    if not engine.context_paths:
        print("## Context Warning\n", file=sys.stderr)
        print("No context paths configured. Run `discover_context` or set context_paths in skill space config.\n", file=sys.stderr)
        return

    memory_skill_path = Path.home() / ".agents" / "skills" / "abd-context-to-memory"
    has_memory_skill = memory_skill_path.exists()

    for ctx_path in engine.context_paths:
        if not ctx_path.exists():
            print(f"## Context Warning\n\nContext path does not exist: `{ctx_path}`\n", file=sys.stderr)
            continue

        source_files = list(ctx_path.rglob("*"))
        source_docs = [f for f in source_files if f.is_file() and f.suffix.lower() in (
            ".pdf", ".pptx", ".docx", ".xlsx",
        )]
        chunked_files = [f for f in source_files if f.is_file() and f.suffix.lower() in (".md", ".txt")]
        large_docs = [f for f in source_docs if f.stat().st_size > 100_000]
        has_enough_chunks = len(chunked_files) >= max(5, len(large_docs) * 3)

        if source_docs and not has_enough_chunks:
            print(f"## Context Warning\n", file=sys.stderr)
            print(f"Context at `{ctx_path}` has {len(source_docs)} unconverted document(s) ({', '.join(set(f.suffix for f in source_docs))}) but no markdown chunks.", file=sys.stderr)
            if has_memory_skill:
                print(f"\nRun the memory skill to convert and chunk:", file=sys.stderr)
                print(f"```", file=sys.stderr)
                print(f"python {memory_skill_path}/scripts/index_memory.py --path \"{ctx_path}\"", file=sys.stderr)
                print(f"```\n", file=sys.stderr)
            else:
                print(f"\nThe `abd-context-to-memory` skill is not installed. Install it to convert documents to chunks.\n", file=sys.stderr)
            continue

        if source_docs and chunked_files:
            newest_source = max(f.stat().st_mtime for f in source_docs)
            newest_chunk = max(f.stat().st_mtime for f in chunked_files)
            if newest_source > newest_chunk:
                stale_docs = [f.name for f in source_docs if f.stat().st_mtime > newest_chunk]
                print(f"## Context Warning\n", file=sys.stderr)
                print(f"Context at `{ctx_path}` has {len(stale_docs)} document(s) newer than chunks: {', '.join(stale_docs[:5])}", file=sys.stderr)
                if has_memory_skill:
                    print(f"\nRe-chunk to pick up changes:", file=sys.stderr)
                    print(f"```", file=sys.stderr)
                    print(f"python {memory_skill_path}/scripts/index_memory.py --path \"{ctx_path}\"", file=sys.stderr)
                    print(f"```\n", file=sys.stderr)
                else:
                    print(f"\nThe `abd-context-to-memory` skill is not installed. Install it to re-chunk documents.\n", file=sys.stderr)


def _get_instructions(operation: str, strategy_path: Path | None = None) -> None:
    """Load engine, get abd-story-synthesizer skill, print display_content(operation)."""
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout.reconfigure(encoding="utf-8")
    engine_root = _skill_dir  # Always the synthesizer skill; never changes
    config_path = _skill_dir / "conf" / "abd-config.json"
    if not config_path.exists():
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

    _check_context(engine)

    skill = engine.get_skill("abd-story-synthesizer") or (engine.skills[0] if engine.skills else None)
    if not skill:
        print("ERROR: No abd-story-synthesizer skill loaded.", file=sys.stderr)
        sys.exit(1)
    print(skill.instructions.display_content(operation))


if __name__ == "__main__":
    args = sys.argv[1:]

    if args and args[0] == "discover_context":
        _discover_context()
    elif args and args[0] == "get_config":
        _get_config()
    elif args and args[0] == "get_instructions":
        if len(args) < 2:
            print("Usage: python build.py get_instructions <operation> [--strategy path]", file=sys.stderr)
            print("Operations: create_strategy, run_slice, generate_slice, validate_run, validate_slice, improve_strategy, correct_run, correct_session, correct_skill, correct_all", file=sys.stderr)
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
            print("Usage: python build.py get_instructions <operation> [--strategy path]", file=sys.stderr)
            sys.exit(1)
        _get_instructions(operation, strategy_path=strategy_path)
    elif args and args[0] == "validate":
        target = Path(args[1]).resolve() if len(args) >= 2 else None
        _run_validate(target_path=target)
    else:
        out = build_skill(_skill_dir, engine_root=_skill_dir)
        print(f"Wrote {out}")
