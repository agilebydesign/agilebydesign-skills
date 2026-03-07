"""
Migrate memory folder from old structure to new structure.

Old: memory/<name>/chunked/*.md, memory/<name>/converted/*.md
New: memory/<name>/*.md (chunked files directly, no chunked subfolder; no converted in memory)

Usage:
  python migrate_memory_structure.py --path <memory_root>

Run from workspace root. Moves chunked/* contents up to parent, removes chunked/ and converted/.
"""

import shutil
import sys
from pathlib import Path


def migrate_dir(parent: Path) -> tuple[int, int]:
    """Migrate one directory. Returns (files_moved, dirs_removed)."""
    chunked_dir = parent / "chunked"
    converted_dir = parent / "converted"
    moved, removed = 0, 0

    if chunked_dir.is_dir():
        for item in chunked_dir.rglob("*"):
            if item.is_file():
                rel = item.relative_to(chunked_dir)
                dest = parent / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                if dest != item:
                    shutil.move(str(item), str(dest))
                    moved += 1
        try:
            shutil.rmtree(chunked_dir)
            removed += 1
        except OSError as e:
            print(f"    Warning: could not remove {chunked_dir}: {e}")

    if converted_dir.is_dir():
        try:
            shutil.rmtree(converted_dir)
            removed += 1
        except OSError as e:
            print(f"    Warning: could not remove {converted_dir}: {e}")

    return moved, removed


def main():
    path_arg = None
    if "--path" in sys.argv:
        idx = sys.argv.index("--path")
        if idx + 1 < len(sys.argv):
            path_arg = sys.argv[idx + 1]
    if not path_arg:
        print("Usage: python migrate_memory_structure.py --path <memory_root>")
        sys.exit(1)

    root = Path(path_arg)
    if not root.is_dir():
        print(f"Path not found: {root}")
        sys.exit(1)

    parents_to_migrate = set()
    for d in root.rglob("chunked"):
        if d.is_dir():
            parents_to_migrate.add(d.parent)
    for d in root.rglob("converted"):
        if d.is_dir():
            parents_to_migrate.add(d.parent)

    total_moved, total_removed = 0, 0
    for parent in sorted(parents_to_migrate, key=lambda p: len(p.parts)):
        moved, removed = migrate_dir(parent)
        total_moved += moved
        total_removed += removed
        if moved or removed:
            try:
                rel = parent.relative_to(root)
            except ValueError:
                rel = parent
            print(f"  {rel}: {moved} files moved, {removed} dirs removed")

    print(f"\nDone: {total_moved} files moved, {total_removed} dirs removed.")


if __name__ == "__main__":
    main()
