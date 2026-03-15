#!/usr/bin/env python3
"""Orchestrate pipeline phases. Run phase N or full pipeline. AI phases: print instructions."""
import json
import subprocess
import sys
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent
_SCRIPTS_DIR = _SKILL_DIR / "scripts"
_PIECES_DIR = _SKILL_DIR / "pieces"
_CODE_PHASES = {1, 3, 4}
_AI_PHASES = {2, 5, 6, 7, 8, 9, 10, 11, 12, 13}
_ALL_PHASES = _CODE_PHASES | _AI_PHASES

_PHASE_FILES = {
    1: "normalize_context.md",
    2: "concept_guidance_v1.md",
    3: "evidence_extraction.md",
    4: "evidence_graph.md",
    5: "concept_guidance_v2.md",
    6: "interaction_tree_structure.md",
    7: "concept_model.md",
    8: "structural_model.md",
    9: "behavior_model.md",
    10: "variation_model.md",
    11: "refined_domain_model.md",
    12: "scenario_walkthrough.md",
    13: "validated_domain_model.md",
}


def _output_dir() -> Path:
    """Resolve output directory from config or default."""
    config_path = _SKILL_DIR / "conf" / "abd-config.json"
    if config_path.exists():
        try:
            cfg = json.loads(config_path.read_text(encoding="utf-8"))
            out = cfg.get("output_dir", "solution")
            workspace = cfg.get("solution_workspace")
            if workspace:
                return Path(workspace).resolve() / out
            return Path.cwd() / out
        except (json.JSONDecodeError, OSError):
            pass
    return Path.cwd() / "solution"


def _config() -> dict:
    """Load config."""
    config_path = _SKILL_DIR / "conf" / "abd-config.json"
    if config_path.exists():
        try:
            return json.loads(config_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _run_phase_1() -> bool:
    """Phase 1: normalize context. Returns True on success."""
    import os
    cfg = _config()
    out = _output_dir()
    chunk_index = os.environ.get("_ABD_CHUNK_INDEX") or cfg.get("chunk_index_path")
    context_path = os.environ.get("_ABD_CONTEXT_PATH") or cfg.get("context_path")

    args = [sys.executable, str(_SCRIPTS_DIR / "normalize_context.py"), "-o", str(out / "rule_chunks.json")]
    if chunk_index:
        idx = Path(chunk_index).resolve()
        if idx.exists():
            args = [sys.executable, str(_SCRIPTS_DIR / "normalize_context.py"), "--chunk-index", str(idx), "-o", str(out / "rule_chunks.json")]
        else:
            print(f"chunk_index_path not found: {idx}", file=sys.stderr)
            return False
    elif context_path:
        ctx = Path(context_path).resolve()
        if ctx.exists():
            args = [sys.executable, str(_SCRIPTS_DIR / "normalize_context.py"), "--context-path", str(ctx), "-o", str(out / "rule_chunks.json")]
        else:
            print(f"context_path not found: {ctx}", file=sys.stderr)
            return False
    else:
        print("Phase 1 requires chunk_index_path or context_path in conf/abd-config.json.", file=sys.stderr)
        return False

    r = subprocess.run(args, cwd=str(_SKILL_DIR))
    return r.returncode == 0


def _run_phase_3() -> bool:
    """Phase 3: guided evidence extraction. Returns True on success."""
    out = _output_dir()
    guidance = out / "concept_guidance_v1.json"
    if not guidance.exists():
        print("Phase 3 requires concept_guidance_v1.json from Phase 2. Run Phase 2 first.", file=sys.stderr)
        return False
    args = [
        sys.executable,
        str(_SCRIPTS_DIR / "evidence_extraction_guided.py"),
        "-i", str(out / "rule_chunks.json"),
        "-g", str(guidance),
        "-o", str(out),
    ]
    r = subprocess.run(args, cwd=str(_SKILL_DIR))
    return r.returncode == 0


def _run_phase_4() -> bool:
    """Phase 4: build evidence graph. Returns True on success."""
    out = _output_dir()
    args = [
        sys.executable,
        str(_SCRIPTS_DIR / "evidence_graph.py"),
        "-i", str(out),
        "-o", str(out / "evidence_graph.json"),
    ]
    r = subprocess.run(args, cwd=str(_SKILL_DIR))
    return r.returncode == 0


def _run_phase(phase: int) -> None:
    """Run a single phase. Code phases: invoke script. AI phases: print phase file."""
    if phase not in _ALL_PHASES:
        print(f"Unknown phase {phase}. Use 1–13.", file=sys.stderr)
        sys.exit(1)

    phase_file = _PIECES_DIR / "phases" / _PHASE_FILES[phase]
    if not phase_file.exists():
        print(f"Phase file missing: {phase_file}", file=sys.stderr)
        sys.exit(1)

    if phase in _CODE_PHASES:
        ok = False
        if phase == 1:
            ok = _run_phase_1()
        elif phase == 3:
            ok = _run_phase_3()
        elif phase == 4:
            ok = _run_phase_4()
        if not ok:
            sys.exit(1)
        return

    # AI phases: print phase file for agent to use
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout.reconfigure(encoding="utf-8")
    content = phase_file.read_text(encoding="utf-8")
    print(content)


def _run_pipeline(stop_at: int | None = None) -> None:
    """Run phases 1–N. Stop at checkpoint or stop_at."""
    end = min(stop_at or 13, 13)
    for n in range(1, end + 1):
        print(f"\n--- Phase {n} ---\n", file=sys.stderr)
        _run_phase(n)


def _main() -> None:
    args = sys.argv[1:]
    if not args:
        print("Usage: pipeline.py run <phase> [--chunk-index PATH] [--context-path PATH]")
        print("       pipeline.py pipeline [--stop N] [--chunk-index PATH] [--context-path PATH]")
        print("  run <phase>   Run phase 1–13. AI phases print instructions.")
        print("  pipeline     Run phases 1–N (default 13).")
        print("  --chunk-index PATH   Override config for Phase 1 (chunk_index.json)")
        print("  --context-path PATH  Override config for Phase 1 (folder of .md)")
        sys.exit(1)

    # Parse overrides
    chunk_override = None
    context_override = None
    if "--chunk-index" in args:
        i = args.index("--chunk-index")
        if i + 1 < len(args):
            chunk_override = args.pop(i + 1)
            args.pop(i)
    if "--context-path" in args:
        i = args.index("--context-path")
        if i + 1 < len(args):
            context_override = args.pop(i + 1)
            args.pop(i)

    # Store overrides for phase 1 (used by _run_phase_1)
    if chunk_override or context_override:
        import os
        os.environ["_ABD_CHUNK_INDEX"] = chunk_override or ""
        os.environ["_ABD_CONTEXT_PATH"] = context_override or ""

    cmd = args[0].lower()
    if cmd == "run":
        if len(args) < 2:
            print("Usage: pipeline.py run <phase>", file=sys.stderr)
            sys.exit(1)
        try:
            phase = int(args[1])
        except ValueError:
            print("Phase must be 1–13.", file=sys.stderr)
            sys.exit(1)
        _run_phase(phase)
    elif cmd == "pipeline":
        stop = None
        if "--stop" in args:
            i = args.index("--stop")
            if i + 1 < len(args):
                try:
                    stop = int(args[i + 1])
                except ValueError:
                    pass
        _run_pipeline(stop)
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _main()
