"""
Agile Context Engine — defines skill structure, scaffold, and build.
All structural logic lives here. Skill scripts are thin entry points.
"""
from pathlib import Path
from typing import Any


class AgileContextEngine:
    """Engine for scaffolding and building ace-skills."""

    def __init__(self, engine_root: str | Path | None = None):
        self.engine_root = Path(engine_root).resolve() if engine_root else None

    def get_skill_scaffold_spec(self) -> dict[str, Any]:
        """Returns canonical ace-skill structure."""
        return get_skill_scaffold_spec()

    def scaffold_skill(self, name: str, path: str | Path) -> Path:
        """Creates ace-skill directory with content/, rules/, scripts/."""
        return scaffold_skill(name, path, engine_root=self.engine_root)

    def build_skill(self, skill_path: str | Path) -> Path:
        """Assembles content into AGENTS.md."""
        return build_skill(skill_path, engine_root=self.engine_root)


# Content files in order for assembly
CONTENT_ORDER = [
    "core-definitions.md",
    "intro.md",
    "output-structure.md",
    "shaping-process.md",
    "validation.md",
]

# Optional content for skills with scripts
SCRIPT_INVOCATION = "script-invocation.md"


def get_skill_scaffold_spec() -> dict[str, Any]:
    """
    Returns the canonical ace-skill structure. Engine is single source of truth.
    No file — in-memory spec.
    """
    return {
        "content_files": CONTENT_ORDER + [SCRIPT_INVOCATION],
        "dirs": ["content", "rules", "scripts"],
        "root_files": ["SKILL.md", "README.md", "metadata.json"],
        "content_templates": {
            "core-definitions.md": "# Core Definitions\n\n",
            "intro.md": "# Intro\n\n",
            "output-structure.md": "# Output Structure\n\n",
            "shaping-process.md": "# Shaping Process\n\n",
            "validation.md": "# Validation\n\n",
            "script-invocation.md": "# Script Invocation\n\nHow to call scripts (params, when, what to expect).\n",
        },
        "rules_default": {"scanners": []},
    }


def scaffold_skill(name: str, path: str | Path, engine_root: str | Path | None = None) -> Path:
    """
    Creates an ace-skill directory with content/, rules/, scripts/, and standard files.
    Engine does the actual file/dir creation.
    """
    path = Path(path)
    if not path.is_absolute() and engine_root:
        path = Path(engine_root) / path
    path = path.resolve()

    spec = get_skill_scaffold_spec()

    # Create dirs
    for d in spec["dirs"]:
        (path / d).mkdir(parents=True, exist_ok=True)

    # Create content files
    for fname in spec["content_files"]:
        content_path = path / "content" / fname
        content_path.parent.mkdir(parents=True, exist_ok=True)
        template = spec["content_templates"].get(fname, "")
        if not content_path.exists():
            content_path.write_text(template, encoding="utf-8")

    # Create rules/scanners.json
    rules_dir = path / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    scanners_path = rules_dir / "scanners.json"
    if not scanners_path.exists():
        import json
        scanners_path.write_text(
            json.dumps(spec["rules_default"], indent=2),
            encoding="utf-8",
        )

    # Create scripts/build.py
    scripts_dir = path / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    build_script = scripts_dir / "build.py"
    if not build_script.exists():
        build_script.write_text(_BUILD_SCRIPT_TEMPLATE.format(skill_name=name), encoding="utf-8")

    # Create SKILL.md
    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        skill_md.write_text(
            f"# {name}\n\nAce-skill. Fill content pieces and run build.\n",
            encoding="utf-8",
        )

    # Create README.md
    readme = path / "README.md"
    if not readme.exists():
        readme.write_text(
            f"# {name}\n\nRun `python scripts/build.py` to assemble AGENTS.md.\n",
            encoding="utf-8",
        )

    # Create metadata.json
    metadata = path / "metadata.json"
    if not metadata.exists():
        import json
        metadata.write_text(
            json.dumps({"name": name, "version": "0.1.0"}, indent=2),
            encoding="utf-8",
        )

    return path


def build_skill(skill_path: str | Path, engine_root: str | Path | None = None) -> Path:
    """
    Assembles content/*.md into AGENTS.md per engine conventions.
    Order: core-definitions, intro, output-structure, shaping-process, validation.
    """
    skill_path = Path(skill_path)
    if not skill_path.is_absolute() and engine_root:
        skill_path = Path(engine_root) / skill_path
    skill_path = skill_path.resolve()

    content_dir = skill_path / "content"
    output_path = skill_path / "AGENTS.md"

    parts: list[str] = []
    for fname in CONTENT_ORDER:
        p = content_dir / fname
        if p.exists():
            parts.append(p.read_text(encoding="utf-8").strip())
            parts.append("\n\n---\n\n")

    # Optional: script-invocation at end
    script_inv = content_dir / SCRIPT_INVOCATION
    if script_inv.exists():
        parts.append(script_inv.read_text(encoding="utf-8").strip())
        parts.append("\n\n---\n\n")

    output_path.write_text("".join(parts).rstrip() + "\n", encoding="utf-8")
    return output_path


_BUILD_SCRIPT_TEMPLATE = '''#!/usr/bin/env python3
"""Build AGENTS.md from content. Thin entry point — delegates to engine."""
import sys
from pathlib import Path

# Add engine to path when run from skill dir
_skill_dir = Path(__file__).resolve().parent.parent
_engine_root = _skill_dir.parent.parent  # skills/ace-<name> -> skills -> repo root
if str(_engine_root) not in sys.path:
    sys.path.insert(0, str(_engine_root))

from src.engine import build_skill

if __name__ == "__main__":
    out = build_skill(_skill_dir, engine_root=_engine_root)
    print(f"Wrote {{out}}")
'''
