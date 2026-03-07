"""
Engine config — pydantic models for abd-config.json.
"""
from pydantic import BaseModel


class AceConfig(BaseModel):
    """Engine config schema. Strict — no extra fields."""

    skills: list[str]
    skills_config: dict | None = None
    constraints: list[dict] = []
    context_paths: list[str] = []

    class Config:
        extra = "ignore"  # ignore legacy skill_space_path
