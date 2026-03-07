"""Shared config: ROOT and MEMORY paths. Env CONTENT_MEMORY_ROOT overrides skill-config."""
import json
import os
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
_SKILL_ROOT = _SCRIPTS.parent


def _expand_path(p: str) -> Path:
    """Expand ~ for portability (each user's home). Supports %VAR% on Windows."""
    s = p.strip()
    # Expand %VAR% (Windows)
    while "%" in s:
        i = s.find("%")
        j = s.find("%", i + 1)
        if j == -1:
            break
        var = s[i + 1 : j]
        val = os.environ.get(var, "")
        s = s[:i] + val + s[j + 1 :]
    return Path(s).expanduser()


def _get_root() -> Path:
    if "CONTENT_MEMORY_ROOT" in os.environ:
        return _expand_path(os.environ["CONTENT_MEMORY_ROOT"])
    config_path = _SKILL_ROOT / "skill-config.json"
    if config_path.exists():
        try:
            with open(config_path, encoding="utf-8") as f:
                cfg = json.load(f)
            if "content_memory_root" in cfg:
                return _expand_path(str(cfg["content_memory_root"]))
        except (json.JSONDecodeError, OSError):
            pass
    return Path.cwd()


def _discover_onedrive_folders() -> list[Path]:
    """Find OneDrive* folders under user home (personal, work, etc.)."""
    home = Path.home()
    if not home.exists():
        return []
    found = []
    for p in home.iterdir():
        if p.is_dir() and p.name.startswith("OneDrive"):
            found.append(p)
    return sorted(found, key=lambda x: x.name)


def ensure_root() -> None:
    """If ROOT does not exist, discover OneDrive folders and prompt user to choose. Exit if unclear."""
    if ROOT.exists():
        return
    # Path not found — help user pick the right OneDrive folder
    onedrives = _discover_onedrive_folders()
    print("Memory path not found:", ROOT, file=sys.stderr)
    if onedrives:
        print("\nMultiple OneDrive folders found. Which one contains your Assets/memory?", file=sys.stderr)
        for i, p in enumerate(onedrives, 1):
            assets = p / "Shared Documents" / "Assets"
            hint = " (has Shared Documents/Assets)" if assets.exists() else ""
            print(f"  {i}. {p}{hint}", file=sys.stderr)
        print("\nSet CONTENT_MEMORY_ROOT to your choice, e.g.:", file=sys.stderr)
        if onedrives:
            example = onedrives[0] / "Shared Documents" / "Assets"
            print(f"  set CONTENT_MEMORY_ROOT={example}", file=sys.stderr)
        print("\nOr edit skill-config.json content_memory_root.", file=sys.stderr)
    else:
        print("\nNo OneDrive folders found under", Path.home(), file=sys.stderr)
        print("Set CONTENT_MEMORY_ROOT to your Assets folder, or edit skill-config.json.", file=sys.stderr)
    sys.exit(1)


ROOT = _get_root()
MEMORY = ROOT / "memory"
ASSETS = ROOT / "Assets"
