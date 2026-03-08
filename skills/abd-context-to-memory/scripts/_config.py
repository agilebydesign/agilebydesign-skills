"""Shared config: ROOT and MEMORY paths. Env CONTENT_MEMORY_ROOT overrides skill-config."""
import json
import os
import sys
from pathlib import Path

# Load .env from cwd (memory root when run via index_memory) or skill folder
try:
    from dotenv import load_dotenv
    for p in [Path.cwd(), Path(__file__).resolve().parent.parent]:
        env_file = p / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            break
except ImportError:
    pass

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


def _get_skill_space_path() -> Path | None:
    """Skill space path (e.g. project root). Priority:
    1. SKILL_SPACE_PATH env
    2. Project conf/abd-config.json (cwd or parents) — when running from project root
    3. skill-config.json
    4. abd-story-synthesizer conf/abd-config.json (skills repo fallback)
    """
    if "SKILL_SPACE_PATH" in os.environ:
        return _expand_path(os.environ["SKILL_SPACE_PATH"])
    # Check project config: conf/abd-config.json in cwd or parent dirs (when running from project)
    for check in [Path.cwd(), Path.cwd().parent]:
        abd_config = check / "conf" / "abd-config.json"
        if abd_config.exists():
            try:
                with open(abd_config, encoding="utf-8") as f:
                    cfg = json.load(f)
                if cfg.get("skill_space_path"):
                    return _expand_path(str(cfg["skill_space_path"]))
            except (json.JSONDecodeError, OSError):
                pass
    config_path = _SKILL_ROOT / "skill-config.json"
    if config_path.exists():
        try:
            with open(config_path, encoding="utf-8") as f:
                cfg = json.load(f)
            if "skill_space_path" in cfg:
                return _expand_path(str(cfg["skill_space_path"]))
        except (json.JSONDecodeError, OSError):
            pass
    # Fallback: sibling abd-story-synthesizer conf (skills repo)
    abd_config = _SKILL_ROOT.parent / "abd-story-synthesizer" / "conf" / "abd-config.json"
    if abd_config.exists():
        try:
            with open(abd_config, encoding="utf-8") as f:
                cfg = json.load(f)
            if "skill_space_path" in cfg:
                return _expand_path(str(cfg["skill_space_path"]))
        except (json.JSONDecodeError, OSError):
            pass
    return None


def get_default_context_folder() -> Path | None:
    """When skill_space_path is set and no folder specified, use {skill_space_path}/context.

    Returns None if skill_space_path is not set."""
    base = _get_skill_space_path()
    if base is None:
        return None
    return base / "context"


def ensure_root() -> None:
    """If ROOT does not exist, prompt user to set CONTENT_MEMORY_ROOT. Exit if unclear."""
    if ROOT.exists():
        return
    print("Memory path not found:", ROOT, file=sys.stderr)
    print("\nSet CONTENT_MEMORY_ROOT to the folder where memory should be stored.", file=sys.stderr)
    print("  Typically: the parent of your context/source folder (e.g. project root).", file=sys.stderr)
    print("  Example: set CONTENT_MEMORY_ROOT=C:\\dev\\my-project", file=sys.stderr)
    print("\nWhen running the full pipeline with --path, ROOT is derived from the source path.", file=sys.stderr)
    sys.exit(1)


ROOT = _get_root()
MEMORY = ROOT / "memory"
ASSETS = ROOT / "Assets"
