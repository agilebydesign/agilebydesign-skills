"""
AbdSkill — skill with Engine injected; operation_sections; instructions property.
"""
from pathlib import Path
from typing import TYPE_CHECKING

from rule_set import RuleSet
from instructions import Instructions

if TYPE_CHECKING:
    from engine import AgileContextEngine


class AbdSkill:
    """Abd-skill. Receives Engine at construction."""

    def __init__(self, path: str | Path, engine: "AgileContextEngine"):
        self.path = Path(path).resolve()
        self.engine = engine
        self.rule_set = RuleSet(self.path).load()
        self._operation_sections = self._load_operation_sections()
        self._instructions: Instructions | None = None

    @property
    def operation_sections(self) -> dict[str, list[str]]:
        return self._operation_sections

    @property
    def instructions(self) -> Instructions:
        if self._instructions is None:
            self._instructions = Instructions(
                operation_sections=self._operation_sections,
                skill_path=self.path,
                engine=self.engine,
            )
        return self._instructions

    def _load_operation_sections(self) -> dict[str, list[str]]:
        import json

        skill_config_path = self.path / "skill-config.json"
        default = {
            "create_strategy": [
                "shaping.process.intro",
                "shaping.strategy.phase",
                "shaping.strategy.criteria",
                "shaping.core.interaction",
                "shaping.core.state_concept",
            ],
            "generate_slice": [
                "shaping.process.intro",
                "shaping.strategy.slices.running",
                "shaping.strategy.corrections",
                "shaping.output.interaction_tree",
                "shaping.output.state_model",
                "shaping.validation.checklist",
                "shaping.validation.rules",
                "shaping.core.interaction",
                "shaping.core.state_concept",
            ],
            "improve_strategy": [
                "shaping.strategy.corrections",
                "shaping.validation.checklist",
            ],
        }
        if skill_config_path.exists():
            data = json.loads(skill_config_path.read_text(encoding="utf-8"))
            if "operation_sections" in data:
                return data["operation_sections"]
        return default
