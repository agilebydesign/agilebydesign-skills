#!/usr/bin/env python3
"""
Create response folder and symlink for proposal response workflow.

Usage:
  python setup_response.py --proposal <proposal_folder> [--project <project_root>]

Creates:
  1. <proposal_folder>/response/ (response artifacts)
  2. <project_root>/response -> <proposal_folder>/response (symlink/junction)

--proposal: Folder containing proposal material (e.g. workspace/jbom response)
--project: Project root for symlink (default: CONTENT_MEMORY_ROOT or cwd)

Run from workspace root. Requires ace-context-to-memory for convert/index.

Examples:
  python setup_response.py --proposal "workspace/jbom response"
  python setup_response.py --proposal "workspace/Scotia Talent Journey" --project .
"""
import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(os.environ.get("CONTENT_MEMORY_ROOT", Path.cwd()))
WORKSPACE = ROOT / "workspace"


def create_junction(link_path: Path, target_path: Path) -> bool:
    """Create junction on Windows (no admin required)."""
    link_path = link_path.resolve()
    target_path = target_path.resolve()
    try:
        subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link_path), str(target_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Junction failed: {e.stderr or e}", file=sys.stderr)
        return False


def create_symlink(link_path: Path, target_path: Path) -> bool:
    """Create symlink on Unix."""
    link_path = link_path.resolve()
    target_path = target_path.resolve()
    try:
        link_path.symlink_to(target_path, target_is_directory=True)
        return True
    except OSError as e:
        print(f"Symlink failed: {e}", file=sys.stderr)
        return False


def main():
    args = sys.argv[1:]
    proposal_idx = next((i for i, a in enumerate(args) if a in ("--proposal", "-p")), None)
    project_idx = next((i for i, a in enumerate(args) if a in ("--project", "-r")), None)

    def get_arg(idx):
        return args[idx + 1] if idx is not None and idx + 1 < len(args) else None

    if proposal_idx is None:
        print("Usage: python setup_response.py --proposal <proposal_folder> [--project <project_root>]")
        sys.exit(1)

    proposal_raw = get_arg(proposal_idx)
    if not proposal_raw:
        print("Usage: python setup_response.py --proposal <proposal_folder> [--project <project_root>]")
        sys.exit(1)

    proposal_path = (ROOT / proposal_raw).resolve() if not Path(proposal_raw).is_absolute() else Path(proposal_raw).resolve()
    project_root = Path(get_arg(project_idx) or ROOT).resolve() if project_idx is not None else ROOT

    if not proposal_path.exists():
        print(f"Proposal folder not found: {proposal_path}")
        sys.exit(1)

    if not proposal_path.is_dir():
        print(f"Proposal path is not a directory: {proposal_path}")
        sys.exit(1)

    response_folder = proposal_path / "response"
    response_folder.mkdir(parents=True, exist_ok=True)
    print(f"Created response folder: {response_folder}")

    link_path = project_root / "response"
    if link_path.exists():
        if link_path.resolve() == response_folder.resolve():
            print(f"Symlink already points to response folder: {link_path}")
        else:
            print(f"Path exists (not a symlink to response): {link_path}")
        sys.exit(0)

    project_root.mkdir(parents=True, exist_ok=True)

    if sys.platform == "win32":
        ok = create_junction(link_path, response_folder)
    else:
        ok = create_symlink(link_path, response_folder)

    if ok:
        print(f"Created: {link_path} -> {response_folder}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
