#!/usr/bin/env python3
"""
Run orchestrator for synthesis workflow.

Drives the full flow: create_strategy -> run_slice (per slice) -> validate.
Implements inner loop (validate -> correct -> re-run) and outer loop (run log).
Supports checkpointing and stop-on-repeated-errors.

Engine (abd-story-synthesizer) = always relative to orchestrator (sibling skill).
--skill-space = workspace root (e.g. mm3e); the content to synthesize.

CONFIG: abd-config.json lives in abd-story-synthesizer/conf/. Engine root is always
the synthesizer skill (never passed; never changes). skill_space_path in config
points to the skill space (content only: goal.md, context/, docs/).

Usage:
  python scripts/run_orchestrator.py --skill-space <path-to-workspace> [--slice N] [--checkpoint ...]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class OrchestratorConfig:
    skill_space_root: Path  # workspace root (e.g. mm3e); the content to synthesize
    workspace_path: Path
    skill_path: Path  # engine = abd-story-synthesizer, always relative to orchestrator
    slice_index: int | None
    checkpoint: str
    max_consecutive_failures: int
    max_inner_iterations: int = 5
    stop_on_correction: bool = False  # exit immediately when validation fails (no retries)
    strategy_only: bool = False  # stop after strategy creation (test run); skip slices
    test_mode: bool = False  # stop at every step; save state and exit (no input); user says "continue" to agent, agent re-runs
    max_runs: int | None = None  # (test_mode) max runs this session; None = unlimited


@dataclass
class RunState:
    run_number: int = 0
    consecutive_failures: int = 0
    current_slice: int = 0
    current_stage: str = ""
    status: str = "running"


def resolve_workspace_path(skill_space_root: Path) -> Path:
    """Workspace = skill_space_root. No abd-config in skill space."""
    return skill_space_root


def resolve_skill_path(_skill_space_root: Path) -> Path:
    """Engine (abd-story-synthesizer) is always relative to orchestrator. No config in skill space."""
    _orchestrator_skill_dir = Path(__file__).resolve().parents[1]  # abd-synthesis-orchestrator/
    _engine_path = _orchestrator_skill_dir.parent / "abd-story-synthesizer"
    if _engine_path.exists():
        return _engine_path.resolve()
    home = Path.home()
    default = home / ".agents" / "skills" / "abd-story-synthesizer"
    if default.exists():
        return default.resolve()
    raise FileNotFoundError(
        "Cannot find abd-story-synthesizer skill. Install as sibling of abd-synthesis-orchestrator."
    )


def run_build(
    skill_path: Path,
    skill_space_root: Path,
    operation: str,
    strategy_path: Path | None = None,
) -> subprocess.CompletedProcess:
    """Run build.py get_instructions or validate. Engine root is always the synthesizer skill (no CLI param)."""
    build_py = skill_path / "scripts" / "build.py"
    if not build_py.exists():
        raise FileNotFoundError(f"build.py not found at {build_py}")

    args = [sys.executable, str(build_py)]
    if operation == "validate":
        args.extend(["validate"])
    else:
        args.extend(["get_instructions", operation])
        if strategy_path and strategy_path.exists():
            args.extend(["--strategy", str(strategy_path)])

    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        cwd=str(skill_path),
        timeout=120,
    )


def run_validate(skill_path: Path, skill_space_root: Path) -> tuple[bool, str]:
    """Run validate. Returns (passed, combined_output)."""
    proc = run_build(skill_path, skill_space_root, "validate")
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode == 0, out


def checkpoint_exit_test_mode(
    workspace_path: Path,
    config: OrchestratorConfig,
    state: RunState,
    message: str,
    slice_count: int = 0,
    slices_to_run: list[int] | None = None,
    last_passed: bool = False,
) -> None:
    """
    Test mode: save state and exit. User reviews output, tells agent what to fix, says "continue", agent re-runs.
    """
    save_state(
        workspace_path, state, slice_count, slices_to_run or [], last_passed, stage=state.current_stage
    )
    print("\n" + "=" * 60)
    print(f"CHECKPOINT: {message}")
    print(f"  Slice: {state.current_slice}  Stage: {state.current_stage}  Run: {state.run_number}")
    print("  Inspect output, run log, and consolidated files.")
    print("  Tell the agent what to fix (or say 'continue'). Agent will re-run orchestrator to resume.")
    print("=" * 60)
    sys.exit(0)


def checkpoint_pause(
    config: OrchestratorConfig, state: RunState, message: str
) -> int:
    """
    Pause at checkpoint and wait for user input.
    Returns number of runs to do before next pause (1 = one step; in test_mode user can enter N).
    In test_mode, checkpoint_exit_test_mode is used instead (save and exit).
    """
    if config.checkpoint == "never":
        return 1
    print("\n" + "=" * 60)
    print(f"CHECKPOINT: {message}")
    print(f"  Slice: {state.current_slice}  Stage: {state.current_stage}  Run: {state.run_number}")
    print("  Inspect output, run log, and consolidated files.")
    print("  Press Enter to continue (or Ctrl+C to abort)...")
    print("=" * 60)
    try:
        raw = input().strip()
        if raw.isdigit():
            return max(1, int(raw))
        return 1
    except KeyboardInterrupt:
        print("\nAborted by user.")
        sys.exit(130)


def get_state_path(workspace_path: Path) -> Path:
    return workspace_path / "story-synthesizer" / "runs" / "orchestrator-state.json"


def save_state(
    workspace_path: Path,
    state: RunState,
    slice_count: int,
    slices_to_run: list[int],
    last_passed: bool,
    stage: str | None = None,
) -> None:
    """Persist state for resume (test mode)."""
    path = get_state_path(workspace_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "run_number": state.run_number,
        "current_slice": state.current_slice,
        "slice_count": slice_count,
        "slices_to_run": slices_to_run,
        "consecutive_failures": state.consecutive_failures,
        "last_validation_passed": last_passed,
        "stage": stage or state.current_stage,
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_state(workspace_path: Path) -> dict | None:
    """Load persisted state for resume (test mode)."""
    path = get_state_path(workspace_path)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def clear_state(workspace_path: Path) -> None:
    path = get_state_path(workspace_path)
    if path.exists():
        path.unlink()


def append_run_log(workspace_path: Path, run_number: int, corrections: str, do_do_not: str) -> None:
    """Append to run log (outer loop)."""
    runs_dir = workspace_path / "story-synthesizer" / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    log_path = runs_dir / f"run-{run_number}.md"
    ts = datetime.now().isoformat()
    block = f"\n\n---\n\n## Run {run_number} @ {ts}\n\n"
    if corrections:
        block += f"### Corrections\n\n{corrections}\n\n"
    if do_do_not:
        block += f"### DO / DO NOT\n\n{do_do_not}\n\n"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(block)


def load_run_log(workspace_path: Path) -> str:
    """Load combined run log for context (outer loop)."""
    runs_dir = workspace_path / "story-synthesizer" / "runs"
    if not runs_dir.exists():
        return ""
    parts = []
    for p in sorted(runs_dir.glob("run-*.md")):
        parts.append(p.read_text(encoding="utf-8"))
    return "\n\n---\n\n".join(parts) if parts else ""


def resolve_strategy_path(workspace_path: Path) -> Path:
    """Resolve strategy path (same order as synthesizer engine)."""
    candidates = [
        workspace_path / "story-synthesizer" / "strategy.md",
        workspace_path / "shaping" / "strategy.md",
        workspace_path / "docs" / "strategy.md",
    ]
    for p in candidates:
        if p.exists():
            return p
    return workspace_path / "story-synthesizer" / "strategy.md"


def get_slice_count(workspace_path: Path) -> int:
    """Get number of slices from strategy (default 10)."""
    strategy_path = resolve_strategy_path(workspace_path)
    if not strategy_path.exists():
        return 10
    text = strategy_path.read_text(encoding="utf-8")
    count = 0
    for line in text.splitlines():
        if "| **" in line and "|" in line:
            try:
                idx = line.index("| **") + 4
                rest = line[idx:]
                num = ""
                for c in rest:
                    if c.isdigit():
                        num += c
                    elif num:
                        count = max(count, int(num))
                        break
            except (ValueError, IndexError):
                pass
    return count if count > 0 else 10


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run orchestrator for synthesis workflow. Engine (synthesizer) is always relative to orchestrator."
    )
    parser.add_argument(
        "--skill-space",
        type=Path,
        required=True,
        metavar="PATH",
        help="Skill space root (workspace, e.g. mm3e) containing conf/abd-config.json",
    )
    parser.add_argument(
        "--slice",
        type=int,
        default=None,
        metavar="N",
        help="Run only slice N (1-based); default: all slices",
    )
    parser.add_argument(
        "--checkpoint",
        choices=["never", "stage", "slice", "run"],
        default="stage",
        help="When to pause for human verification (default: stage)",
    )
    parser.add_argument(
        "--max-consecutive-failures",
        type=int,
        default=3,
        metavar="N",
        help="Stop when same stage/slice fails N times in a row (default: 3)",
    )
    parser.add_argument(
        "--max-inner-iterations",
        type=int,
        default=5,
        metavar="N",
        help="Max validate->correct->re-run iterations per stage (default: 5)",
    )
    parser.add_argument(
        "--stop-on-correction",
        action="store_true",
        help="Exit immediately when validation fails (no retries); fix strategy/corrections and re-run",
    )
    parser.add_argument(
        "--strategy-only",
        action="store_true",
        help="Stop after strategy creation (test run); skip slice runs",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Stop at every step; prompt accepts N to do N runs then exit; state persisted for resume",
    )
    parser.add_argument(
        "--max-runs",
        type=int,
        default=None,
        metavar="N",
        help="(test-mode) Max runs this session; then exit and save state for resume",
    )
    args = parser.parse_args()

    skill_space_root = Path(args.skill_space).resolve()
    if not skill_space_root.exists():
        print(f"ERROR: Skill space not found: {skill_space_root}", file=sys.stderr)
        return 1

    try:
        skill_path = resolve_skill_path(skill_space_root)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    workspace_path = resolve_workspace_path(skill_space_root)
    config = OrchestratorConfig(
        skill_space_root=skill_space_root,
        workspace_path=workspace_path,
        skill_path=skill_path,
        slice_index=args.slice,
        checkpoint=args.checkpoint,
        max_consecutive_failures=args.max_consecutive_failures,
        max_inner_iterations=args.max_inner_iterations,
        stop_on_correction=args.stop_on_correction,
        strategy_only=args.strategy_only,
        test_mode=args.test_mode,
        max_runs=args.max_runs,
    )
    state = RunState()

    strategy_path = resolve_strategy_path(workspace_path)
    out_dir = workspace_path / "story-synthesizer"

    print(f"Skill space: {skill_space_root}")
    print(f"Workspace: {workspace_path}")
    print(f"Engine (synthesizer): {skill_path}")
    print(f"Checkpoint: {config.checkpoint}")
    print(f"Max consecutive failures: {config.max_consecutive_failures}")
    if config.stop_on_correction:
        print("Stop on correction: yes (exit on first validation failure)")
    if config.strategy_only:
        print("Strategy only: yes (stop after strategy creation)")
    if config.test_mode:
        print("Test mode: yes (stop at every step; save and exit; re-run to resume)")
        if config.max_runs:
            print(f"Max runs this session: {config.max_runs}")
    print()

    # Resume check: if we exited at create_strategy, strategy must exist to continue
    if config.test_mode:
        saved = load_state(workspace_path)
        if saved and saved.get("stage") == "create_strategy":
            if not strategy_path.exists():
                instr = workspace_path / "story-synthesizer" / "runs" / "create_strategy-instructions.md"
                print(f"Resuming: waiting for strategy.md. Run agent with {instr}, create strategy.md, then re-run.")
                sys.exit(0)
            clear_state(workspace_path)  # clear so we don't re-check

    # Phase 1: Create strategy (if missing)
    if not strategy_path.exists():
        print("[1/3] Creating strategy...")
        proc = run_build(skill_path, skill_space_root, "create_strategy")
        print(proc.stdout or "")
        if proc.stderr:
            print(proc.stderr, file=sys.stderr)
        if proc.returncode != 0:
            print("ERROR: create_strategy failed. Run the agent with the instructions above.", file=sys.stderr)
            return 1
        state.current_stage = "create_strategy"
        if config.test_mode:
            # Save instructions so user/agent can find them when resuming
            instr_path = out_dir / "runs" / "create_strategy-instructions.md"
            instr_path.parent.mkdir(parents=True, exist_ok=True)
            instr_path.write_text(proc.stdout or "", encoding="utf-8")
            print(f"  Instructions saved to: {instr_path}")
            checkpoint_exit_test_mode(
                config.workspace_path, config, state,
                "Strategy instructions printed. Run agent to produce strategy.md.",
                slice_count=0, slices_to_run=[], last_passed=False,
            )
        checkpoint_pause(config, state, "Strategy instructions printed. Run agent to produce strategy.md")
        if not strategy_path.exists():
            print("ERROR: strategy.md not found after checkpoint.", file=sys.stderr)
            return 1
    else:
        print("[1/3] Strategy exists, skipping create_strategy.")

    if config.strategy_only:
        print("\nStrategy-only run complete. Exiting.")
        return 0

    # Phase 2: Run slices
    effective_checkpoint = "run" if config.test_mode else config.checkpoint
    slice_count = get_slice_count(config.workspace_path)
    all_slices = (
        [config.slice_index] if config.slice_index is not None
        else list(range(1, slice_count + 1))
    )
    slices_to_run = list(all_slices)

    # Resume from state (test mode)
    runs_before_exit = config.max_runs  # None = unlimited
    runs_this_session = 0
    resumed_slice = None
    skip_to_validate = False  # True when resuming from waiting_validation
    if config.test_mode:
        saved = load_state(config.workspace_path)
        if saved:
            state.run_number = saved.get("run_number", 0)
            state.current_slice = saved.get("current_slice", 0)
            state.consecutive_failures = saved.get("consecutive_failures", 0)
            last_passed = saved.get("last_validation_passed", False)
            sc = saved.get("slice_count", slice_count)
            sl = saved.get("slices_to_run", slices_to_run)
            if saved.get("stage") == "waiting_validation":
                skip_to_validate = True
                slices_to_run = [s for s in sl if s >= state.current_slice]
                resumed_slice = state.current_slice
            elif last_passed:
                slices_to_run = [s for s in sl if s > state.current_slice]
            else:
                slices_to_run = [s for s in sl if s >= state.current_slice]
                resumed_slice = state.current_slice
            if slices_to_run:
                print(f"Resuming from slice {state.current_slice} (run {state.run_number})...")

    for slice_idx in slices_to_run:
        state.current_slice = slice_idx
        if slice_idx != resumed_slice:
            state.consecutive_failures = 0

        print(f"\n[2/3] Slice {slice_idx}/{slice_count}...")
        state.current_stage = "run_slice"

        for inner in range(config.max_inner_iterations):
            if not skip_to_validate:
                state.run_number += 1
                print(f"  Run {state.run_number} (inner iteration {inner + 1}/{config.max_inner_iterations})")

                proc = run_build(skill_path, skill_space_root, "run_slice", strategy_path)
                instructions = proc.stdout or ""
                if proc.stderr:
                    print(proc.stderr, file=sys.stderr)

                instructions_path = out_dir / "runs" / f"slice-{slice_idx}-run-{state.run_number}-instructions.md"
                instructions_path.parent.mkdir(parents=True, exist_ok=True)
                header = f"## Current slice: {slice_idx}\n\n"
                run_log_context = load_run_log(config.workspace_path)
                if run_log_context:
                    header += f"## Run Log (corrections from previous runs)\n\n{run_log_context}\n\n---\n\n"
                instructions_path.write_text(header + instructions, encoding="utf-8")
                print(f"  Instructions saved to: {instructions_path}")

                if config.checkpoint == "run":
                    if config.test_mode:
                        save_state(
                            config.workspace_path, state, slice_count, list(slices_to_run),
                            last_passed=False, stage="waiting_validation",
                        )
                        checkpoint_exit_test_mode(
                            config.workspace_path, config, state,
                            f"Run slice {slice_idx}. Execute agent with instructions, then re-run to continue.",
                            slice_count, list(slices_to_run), last_passed=False,
                        )
                    checkpoint_pause(config, state, f"Run slice {slice_idx}. Execute agent with instructions, then continue.")

            if skip_to_validate:
                instructions_path = out_dir / "runs" / f"slice-{slice_idx}-run-{state.run_number}-instructions.md"
                if not instructions_path.exists():
                    print(f"ERROR: {instructions_path} not found. Run agent with instructions first.", file=sys.stderr)
                    return 2
                skip_to_validate = False  # Only skip once; next iteration runs normally

            passed, validate_out = run_validate(skill_path, skill_space_root)
            if validate_out.strip():
                print(validate_out)

            if passed:
                print(f"  Validation PASSED for slice {slice_idx}")
                state.consecutive_failures = 0
                append_run_log(config.workspace_path, state.run_number, "", "Run passed.")
                runs_this_session += 1
                if config.test_mode and runs_before_exit and runs_this_session >= runs_before_exit:
                    save_state(config.workspace_path, state, slice_count, all_slices, last_passed=True)
                    print(f"\nTest mode: {runs_this_session} runs done. State saved. Re-run to continue.")
                    return 0
                if effective_checkpoint == "stage":
                    if config.test_mode:
                        checkpoint_exit_test_mode(
                            config.workspace_path, config, state,
                            f"Slice {slice_idx} passed. Re-run to continue.",
                            slice_count, list(slices_to_run), last_passed=True,
                        )
                    n = checkpoint_pause(config, state, f"Slice {slice_idx} passed. Proceed to next slice?")
                    if n > 1:
                        runs_before_exit = n
                break
            else:
                state.consecutive_failures += 1
                runs_this_session += 1
                print(f"  Validation FAILED (consecutive failures: {state.consecutive_failures})")
                append_run_log(
                    config.workspace_path,
                    state.run_number,
                    validate_out,
                    "Apply corrections and re-run.",
                )

                if config.test_mode and runs_before_exit and runs_this_session >= runs_before_exit:
                    save_state(config.workspace_path, state, slice_count, all_slices, last_passed=False)
                    print(f"\nTest mode: {runs_this_session} runs done. State saved. Re-run to continue.")
                    return 0

                if config.stop_on_correction:
                    print("\nStopped on correction. Fix strategy/corrections and re-run.", file=sys.stderr)
                    return 2

                if state.consecutive_failures >= config.max_consecutive_failures:
                    print(f"\nERROR: Stopping after {config.max_consecutive_failures} consecutive failures.", file=sys.stderr)
                    print("Fix strategy, rules, or content and re-run.", file=sys.stderr)
                    return 2

                if config.checkpoint in ("stage", "run"):
                    if config.test_mode:
                        checkpoint_exit_test_mode(
                            config.workspace_path, config, state,
                            "Validation failed. Apply corrections, re-run agent, then re-run to continue.",
                            slice_count, list(slices_to_run), last_passed=False,
                        )
                    checkpoint_pause(config, state, "Validation failed. Apply corrections, re-run agent, then continue.")
        else:
            print(f"\nERROR: Max inner iterations ({config.max_inner_iterations}) reached for slice {slice_idx}.", file=sys.stderr)
            return 2

        if effective_checkpoint == "slice":
            if config.test_mode:
                checkpoint_exit_test_mode(
                    config.workspace_path, config, state,
                    f"Slice {slice_idx} complete. Re-run to continue.",
                    slice_count, list(slices_to_run), last_passed=True,
                )
            n = checkpoint_pause(config, state, f"Slice {slice_idx} complete. Proceed to next slice?")
            if n > 1:
                runs_before_exit = n

    # Phase 3: Final validation
    print("\n[3/3] Final validation...")
    passed, validate_out = run_validate(skill_path, skill_space_root)
    if validate_out.strip():
        print(validate_out)
    if passed:
        if config.test_mode:
            clear_state(config.workspace_path)
        print("\nOrchestrator complete. Status: approved")
        return 0
    else:
        if config.test_mode:
            save_state(config.workspace_path, state, slice_count, all_slices, last_passed=False)
        print("\nOrchestrator complete. Status: needs-correction")
        return 2


if __name__ == "__main__":
    sys.exit(main())
