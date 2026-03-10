"""
Agile Context Engine — defines skill structure, scaffold, and build.
Self-contained in abd-story-synthesizer; self-contained; no dependency on other abd skills.
"""
import json
from pathlib import Path
from typing import Any

from config import AbdConfig
from abd_skill import AbdSkill


def _default_engine_root() -> Path:
    """Resolve engine root (parent of scripts/)."""
    return Path(__file__).resolve().parent.parent


class AgileContextEngine:
    """Engine for building and running abd-skills."""

    def __init__(
        self,
        engine_root: str | Path | None = None,
        strategy_path_override: str | Path | None = None,
    ):
        self.engine_root = Path(engine_root).resolve() if engine_root else _default_engine_root()
        self.config_path = self.engine_root / "conf" / "abd-config.json"
        self.strategy_path_override = Path(strategy_path_override).resolve() if strategy_path_override else None
        self.workspace_path: Path | None = None
        self.strategy_path: Path | None = None
        self.context_paths: list[Path] = []
        self.skills: list[AbdSkill] = []

    def load(self) -> "AgileContextEngine":
        """Load config; load skills; inject self into each skill."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")
        data = json.loads(self.config_path.read_text(encoding="utf-8"))
        config = AbdConfig.model_validate(data)

        # Context paths — read from skill space config, not the synthesizer's config
        self.context_paths = []

        # Skill paths: support absolute (e.g. global skills) or relative
        order = (config.skills_config or {}).get("order", config.skills)
        self.skills = []
        for rel_path in order:
            path = Path(rel_path)
            if path.is_absolute():
                skill_path = path.resolve()
            else:
                skill_path = (self.engine_root / rel_path).resolve()
            if skill_path.exists():
                skill = AbdSkill(skill_path, engine=self)
                self.skills.append(skill)

        if self.skills:
            if config.skill_space_path:
                self.workspace_path = Path(config.skill_space_path).resolve()
            else:
                self.workspace_path = self._skill_space_from_path(self.skills[0].path)
            self._load_skill_space_context_paths()
            self._update_strategy_path()
            self._create_output_dirs()
        return self

    def _load_skill_space_context_paths(self) -> None:
        """Load context_paths from the skill space's own conf/abd-config.json."""
        if not self.workspace_path:
            return
        ss_config_path = self.workspace_path / "conf" / "abd-config.json"
        if not ss_config_path.exists():
            return
        try:
            ss_data = json.loads(ss_config_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return
        for p in ss_data.get("context_paths", []):
            path = Path(p)
            resolved = path.resolve() if path.is_absolute() else (self.workspace_path / p).resolve()
            if resolved not in self.context_paths:
                self.context_paths.append(resolved)

    def _skill_space_from_path(self, skill_path: Path) -> Path:
        """Skill space = parent of .agents/skills (or parent of skills when in engine)."""
        p = skill_path.resolve()
        if p.parent.name == "skills" and p.parent.parent.name == ".agents":
            return p.parent.parent.parent
        if p.parent.name == "skills":
            return p.parent.parent
        return p.parent

    def get_skill(self, name: str) -> AbdSkill | None:
        """Get skill by name (e.g. abd-story-synthesizer)."""
        for s in self.skills:
            if s.path.name == name or name in str(s.path):
                return s
        return None

    def get_skill_scaffold_spec(self) -> dict[str, Any]:
        return get_skill_scaffold_spec()

    def scaffold_skill(self, name: str, path: str | Path) -> Path:
        return scaffold_skill(name, path, engine_root=self.engine_root)

    def build_skill(self, skill_path: str | Path) -> Path:
        return build_skill(skill_path, engine_root=self.engine_root)

    def _output_folder_for_skill(self, skill_name: str) -> str:
        """Strip abd- prefix: abd-story-synthesizer → story-synthesizer."""
        if skill_name.startswith("abd-"):
            return skill_name[4:]
        return skill_name

    def _create_output_dirs(self) -> None:
        if not self.workspace_path:
            return
        for skill in self.skills:
            skill_name = skill.path.name
            output_folder = self._output_folder_for_skill(skill_name)
            output_root = self.workspace_path / output_folder
            output_root.mkdir(parents=True, exist_ok=True)
            (output_root / "runs").mkdir(parents=True, exist_ok=True)

    def _update_strategy_path(self) -> None:
        if not self.workspace_path:
            self.strategy_path = None
            return
        if self.strategy_path_override and self.strategy_path_override.exists():
            self.strategy_path = self.strategy_path_override
            return
        candidates = [
            self.workspace_path / "story-synthesizer" / "strategy.md",
            self.workspace_path / "story-synthesizer" / "strategy.md",
            self.workspace_path / "docs" / "strategy.md",
        ]
        for p in candidates:
            if p.exists():
                self.strategy_path = p
                return
        self.strategy_path = self.workspace_path / "story-synthesizer" / "strategy.md"


CONTENT_ORDER = [
    "introduction.md",
    "interaction.md",
    "domain.md",
    "process.md",
    "session.md",
    "runs.md",
    "validation.md",
]


def get_skill_scaffold_spec() -> dict[str, Any]:
    return {
        "content_files": CONTENT_ORDER,
        "dirs": ["pieces", "rules", "scripts"],
        "root_files": ["SKILL.md", "README.md", "skill-config.json"],
        "content_templates": {
            "introduction.md": "# Introduction\n\n",
            "interaction.md": "# Interaction Model\n\n",
            "domain.md": "# Domain Model\n\n",
            "process.md": "# Process\n\n",
            "session.md": "# Sessions\n\n",
            "runs.md": "# Runs\n\n",
            "validation.md": "# Validation\n\n",
        },
        "rules_default": {"scanners": []},
    }


def scaffold_skill(name: str, path: str | Path, engine_root: str | Path | None = None) -> Path:
    path = Path(path)
    if not path.is_absolute() and engine_root:
        path = Path(engine_root) / path
    path = path.resolve()

    spec = get_skill_scaffold_spec()

    for d in spec["dirs"]:
        (path / d).mkdir(parents=True, exist_ok=True)

    for fname in spec["content_files"]:
        content_path = path / "pieces" / fname
        content_path.parent.mkdir(parents=True, exist_ok=True)
        template = spec["content_templates"].get(fname, "")
        if not content_path.exists():
            content_path.write_text(template, encoding="utf-8")

    rules_dir = path / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    scanners_path = rules_dir / "scanners.json"
    if not scanners_path.exists():
        scanners_path.write_text(json.dumps(spec["rules_default"], indent=2), encoding="utf-8")

    scripts_dir = path / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    build_script = scripts_dir / "build.py"
    if not build_script.exists():
        build_script.write_text(_BUILD_SCRIPT_TEMPLATE.format(skill_name=name), encoding="utf-8")

    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        skill_md.write_text(f"# {name}\n\nAbd-skill. Fill content pieces and run build.\n", encoding="utf-8")

    readme = path / "README.md"
    if not readme.exists():
        readme.write_text(f"# {name}\n\nRun `python scripts/build.py` to assemble AGENTS.md.\n", encoding="utf-8")

    skill_config = path / "skill-config.json"
    if not skill_config.exists():
        skill_config.write_text(json.dumps({"name": name, "version": "0.1.0"}, indent=2), encoding="utf-8")

    return path


def build_skill(skill_path: str | Path, engine_root: str | Path | None = None) -> Path:
    """Assembles pieces/*.md into AGENTS.md per engine conventions."""
    skill_path = Path(skill_path)
    if not skill_path.is_absolute() and engine_root:
        skill_path = Path(engine_root) / skill_path
    skill_path = skill_path.resolve()

    content_dir = skill_path / "pieces"
    output_path = skill_path / "AGENTS.md"

    content_order = CONTENT_ORDER
    skill_config_path = skill_path / "skill-config.json"
    if skill_config_path.exists():
        try:
            data = json.loads(skill_config_path.read_text(encoding="utf-8"))
            if "content_order" in data:
                content_order = data["content_order"]
        except (json.JSONDecodeError, KeyError):
            pass

    parts: list[str] = []
    for fname in content_order:
        p = content_dir / fname
        if p.exists():
            parts.append(p.read_text(encoding="utf-8").strip())
            parts.append("\n\n---\n\n")

    output_path.write_text("".join(parts).rstrip() + "\n", encoding="utf-8")
    return output_path


_BUILD_SCRIPT_TEMPLATE = '''#!/usr/bin/env python3
"""Build AGENTS.md from content. Self-contained — engine in same scripts/."""
import sys
from pathlib import Path

_skill_dir = Path(__file__).resolve().parent.parent
_scripts_dir = Path(__file__).resolve().parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

from engine import build_skill

if __name__ == "__main__":
    out = build_skill(_skill_dir, engine_root=_skill_dir)
    print(f"Wrote {{out}}")
'''
