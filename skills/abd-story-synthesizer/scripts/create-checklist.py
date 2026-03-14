#!/usr/bin/env python3
"""Create or update checklists for Overall Context, Session, and Slice-Runs.

Usage:
  create-checklist overall [--workspace PATH]
  create-checklist session <name> [--workspace PATH]
  create-checklist run <session> <n> [--workspace PATH]
  create-checklist update <path> --step <n>

Examples:
  python create-checklist.py overall
  python create-checklist.py session discovery1
  python create-checklist.py run discovery1 1
  python create-checklist.py update story-synthesizer/discovery1/runs/run-1-checklist.md --step 3
"""
import argparse
import re
import sys
from pathlib import Path

_skill_dir = Path(__file__).resolve().parent.parent
_scripts_dir = Path(__file__).resolve().parent
_pieces_dir = _skill_dir / "pieces"
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))


def _get_workspace(workspace_arg: Path | None) -> Path:
    """Resolve workspace path from arg or config."""
    if workspace_arg and workspace_arg.exists():
        return workspace_arg.resolve()
    try:
        from engine import AgileContextEngine
        engine = AgileContextEngine(engine_root=_skill_dir).load()
        ws = engine.workspace_path
        if ws:
            return Path(ws).resolve()
    except Exception:
        pass
    # Fallback: assume story-synthesizer is under cwd
    cwd = Path.cwd()
    if (cwd / "story-synthesizer").exists():
        return cwd
    return cwd


def _create_overall(workspace: Path) -> Path:
    """Create overall-context-checklist.md from template."""
    template = _pieces_dir / "overall_context_checklist_template.md"
    if not template.exists():
        raise FileNotFoundError(f"Template not found: {template}")
    out_dir = workspace / "story-synthesizer"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "overall-context-checklist.md"
    out_path.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
    return out_path


def _create_session(workspace: Path, session_name: str) -> Path:
    """Create session checklist from template."""
    template = _pieces_dir / "session_checklist_template.md"
    if not template.exists():
        raise FileNotFoundError(f"Template not found: {template}")
    out_dir = workspace / "story-synthesizer" / session_name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "session-checklist.md"
    out_path.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
    return out_path


def _create_run(workspace: Path, session_name: str, run_n: int) -> Path:
    """Create run checklist from template."""
    template = _pieces_dir / "run_checklist_template.md"
    if not template.exists():
        raise FileNotFoundError(f"Template not found: {template}")
    out_dir = workspace / "story-synthesizer" / session_name / "runs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"run-{run_n}-checklist.md"
    out_path.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
    return out_path


def _update_step(path: Path, step_n: int) -> None:
    """Mark step N as done (☐ → ☑) in the checklist file."""
    if not path.exists():
        raise FileNotFoundError(f"Checklist not found: {path}")
    text = path.read_text(encoding="utf-8")
    # Match table rows with | N | ... | ☐ | and replace ☐ with ☑ for step N
    pattern = rf"(\|\s*{step_n}\s*\|[^|]*\|)\s*☐\s*(\|)"
    replacement = rf"\1 ☑ \2"
    new_text, count = re.subn(pattern, replacement, text)
    if count == 0:
        raise ValueError(f"Step {step_n} not found or already done in {path}")
    path.write_text(new_text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create or update checklists for Overall Context, Session, and Slice-Runs."
    )
    parser.add_argument("--workspace", type=Path, help="Workspace root (default: from config or cwd)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    overall_p = sub.add_parser("overall")
    overall_p.set_defaults(cmd="overall")

    session_p = sub.add_parser("session")
    session_p.add_argument("name", help="Session name (e.g. discovery1)")
    session_p.set_defaults(cmd="session")

    run_p = sub.add_parser("run")
    run_p.add_argument("session", help="Session name")
    run_p.add_argument("n", type=int, help="Run number (e.g. 1)")
    run_p.set_defaults(cmd="run")

    update_p = sub.add_parser("update")
    update_p.add_argument("path", type=Path, help="Path to checklist file")
    update_p.add_argument("--step", type=int, required=True, help="Step number to mark done")
    update_p.set_defaults(cmd="update")

    args = parser.parse_args()
    workspace = _get_workspace(getattr(args, "workspace", None))

    if args.cmd == "overall":
        out = _create_overall(workspace)
        print(f"Created {out}")
    elif args.cmd == "session":
        out = _create_session(workspace, args.name)
        print(f"Created {out}")
    elif args.cmd == "run":
        out = _create_run(workspace, args.session, args.n)
        print(f"Created {out}")
    elif args.cmd == "update":
        path = args.path if args.path.is_absolute() else (Path.cwd() / args.path)
        _update_step(path, args.step)
        print(f"Marked step {args.step} done in {path}")


if __name__ == "__main__":
    main()
