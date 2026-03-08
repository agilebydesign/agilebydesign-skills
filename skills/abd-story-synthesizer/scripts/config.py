"""
Engine config — abd-config.json schema. Uses pydantic if available, else plain dict.
"""
from typing import Any

try:
    from pydantic import BaseModel

    class AbdConfig(BaseModel):
        """Engine config schema. Supports skill_space_path for workspace override."""

        skills: list[str]
        skills_config: dict | None = None
        constraints: list[dict] = []
        context_paths: list[str] = []
        skill_space_path: str | None = None

        class Config:
            extra = "ignore"

except ImportError:

    class AbdConfig:
        """Plain-dict fallback when pydantic not installed."""

        def __init__(
            self,
            skills: list[str],
            skills_config: dict | None = None,
            constraints: list[dict] | None = None,
            context_paths: list[str] | None = None,
            skill_space_path: str | None = None,
            **_: Any,
        ):
            self.skills = skills or []
            self.skills_config = skills_config
            self.constraints = constraints or []
            self.context_paths = context_paths or []
            self.skill_space_path = skill_space_path

        @classmethod
        def model_validate(cls, data: dict[str, Any]) -> "AbdConfig":
            return cls(
                skills=data.get("skills", []),
                skills_config=data.get("skills_config"),
                constraints=data.get("constraints", []),
                context_paths=data.get("context_paths", []),
                skill_space_path=data.get("skill_space_path"),
            )
