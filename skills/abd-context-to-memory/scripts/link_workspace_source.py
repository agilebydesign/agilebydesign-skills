"""
Link a folder into abd_content/source/ so skills can access it when adding to memory.

Usage:
  python link_workspace_source.py --path <folder_path> [--name <link_name>]
  python link_workspace_source.py --workspace <workspace_folder_name> [--name <link_name>]

Creates a junction (Windows) or symlink (Unix) at:
  source/<link_name> -> <target_folder>

--path: Any folder (absolute or relative to ROOT). Use for arbitrary folders.
--workspace: Shorthand for workspace/<name>/source (workspace RFQ folders).
--name: Link name under source/ (default: last component of target path).

Run from abd_content root, or set CONTENT_MEMORY_ROOT.

Examples:
  python link_workspace_source.py --path "C:/docs/RFQ materials" --name "JBOM"
  python link_workspace_source.py --path "workspace/Scotia Talent Journey/source" --name "JBOM Agile Support"
  python link_workspace_source.py --workspace "Scotia Talent Journey Based Operating Model" --name "JBOM Agile Support"

When to run: Before adding content to memory. Run on request when user wants to add
a folder's docs to memory and the link does not yet exist.
"""

import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(os.environ.get("CONTENT_MEMORY_ROOT", Path.cwd()))
WORKSPACE = ROOT / "workspace"
SOURCE = ROOT / "source"


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
    path_idx = next((i for i, a in enumerate(args) if a == "--path"), None)
    workspace_idx = next((i for i, a in enumerate(args) if a == "--workspace"), None)
    name_idx = next((i for i, a in enumerate(args) if a == "--name"), None)

    def get_arg(idx):
        return args[idx + 1] if idx is not None and idx + 1 < len(args) else None

    if path_idx is not None:
        target_raw = get_arg(path_idx)
        if not target_raw:
            print("Usage: python link_workspace_source.py --path <folder_path> [--name <link_name>]")
            sys.exit(1)
        target = (ROOT / target_raw).resolve() if not Path(target_raw).is_absolute() else Path(target_raw).resolve()
        default_name = target.name
    elif workspace_idx is not None:
        workspace_folder = get_arg(workspace_idx)
        if not workspace_folder:
            print("Usage: python link_workspace_source.py --workspace <folder_name> [--name <link_name>]")
            sys.exit(1)
        target = (WORKSPACE / workspace_folder / "source").resolve()
        default_name = workspace_folder
    else:
        print("Usage: python link_workspace_source.py --path <folder_path> [--name <link_name>]")
        print("   or: python link_workspace_source.py --workspace <folder_name> [--name <link_name>]")
        sys.exit(1)

    link_name = get_arg(name_idx) or default_name
    link_path = SOURCE / link_name

    if not target.exists():
        print(f"Target not found: {target}")
        sys.exit(1)

    if not target.is_dir():
        print(f"Target is not a directory: {target}")
        sys.exit(1)

    if link_path.exists():
        print(f"Path already exists: {link_path}")
        sys.exit(0)

    SOURCE.mkdir(parents=True, exist_ok=True)

    if sys.platform == "win32":
        ok = create_junction(link_path, target)
    else:
        ok = create_symlink(link_path, target)

    if ok:
        print(f"Created: source/{link_name} -> {target}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
