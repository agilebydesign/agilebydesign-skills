"""Shared config for abd-solution-modeler scripts."""
import json
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent


def output_dir() -> Path:
    """Resolve output directory from conf/abd-config.json or default."""
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
