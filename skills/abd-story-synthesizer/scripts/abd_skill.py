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
        self.rule_set = RuleSet(self.path)
        self.rule_set.load()
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
                "story_synthesizer.process.intro",
                "story_synthesizer.strategy.iterative",
                "story_synthesizer.strategy.criteria",
                "story_synthesizer.core.interaction",
                "story_synthesizer.core.state_concept",
            ],
            "run_slice": [
                "story_synthesizer.process.intro",
                "story_synthesizer.strategy.slices.running",
                "story_synthesizer.strategy.corrections",
                "story_synthesizer.output.interaction_tree",
                "story_synthesizer.output.state_model",
                "story_synthesizer.validation.checklist",
                "story_synthesizer.validation.rules",
                "story_synthesizer.core.interaction",
                "story_synthesizer.core.state_concept",
            ],
            "generate_slice": [
                "story_synthesizer.process.intro",
                "story_synthesizer.strategy.slices.running",
                "story_synthesizer.strategy.corrections",
                "story_synthesizer.output.interaction_tree",
                "story_synthesizer.output.state_model",
                "story_synthesizer.validation.checklist",
                "story_synthesizer.validation.rules",
                "story_synthesizer.core.interaction",
                "story_synthesizer.core.state_concept",
            ],
            "correct_run": [
                "story_synthesizer.correct.run",
                "story_synthesizer.runs.corrections",
            ],
            "correct_session": [
                "story_synthesizer.correct.session",
            ],
            "correct_skill": [
                "story_synthesizer.correct.skill",
            ],
            "correct_all": [
                "story_synthesizer.correct.run",
                "story_synthesizer.runs.corrections",
                "story_synthesizer.correct.session",
                "story_synthesizer.correct.skill",
            ],
            "improve_strategy": [
                "story_synthesizer.strategy.corrections",
                "story_synthesizer.validation.checklist",
            ],
            "validate_run": [
                "story_synthesizer.validation.scope_run",
                "story_synthesizer.strategy.criteria",
                "story_synthesizer.output.interaction_tree",
                "story_synthesizer.output.state_model",
                "story_synthesizer.validation.checklist",
                "story_synthesizer.validation.rules",
            ],
            "validate_slice": [
                "story_synthesizer.validation.scope_slice",
                "story_synthesizer.strategy.criteria",
                "story_synthesizer.output.interaction_tree",
                "story_synthesizer.output.state_model",
                "story_synthesizer.validation.checklist",
                "story_synthesizer.validation.rules",
            ],
        }
        if skill_config_path.exists():
            data = json.loads(skill_config_path.read_text(encoding="utf-8"))
            if "operation_sections" in data:
                return data["operation_sections"]
        return default
