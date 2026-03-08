"""
Engine config — schema for abd-config.json. Plain dataclass, no pydantic.
"""


def load_abd_config(data: dict) -> "AbdConfig":
    """Parse config dict into AbdConfig. Ignores extra keys."""
    skills = data.get("skills", [])
    if not isinstance(skills, list):
        skills = []
    skills_config = data.get("skills_config")
    if skills_config is not None and not isinstance(skills_config, dict):
        skills_config = None
    constraints = data.get("constraints", [])
    if not isinstance(constraints, list):
        constraints = []
    context_paths = data.get("context_paths", [])
    if not isinstance(context_paths, list):
        context_paths = []
    return AbdConfig(
        skills=skills,
        skills_config=skills_config,
        constraints=constraints,
        context_paths=context_paths,
    )


class AbdConfig:
    """Engine config schema. Use load_abd_config() to parse from dict."""

    def __init__(
        self,
        *,
        skills: list[str],
        skills_config: dict | None = None,
        constraints: list[dict] | None = None,
        context_paths: list[str] | None = None,
    ):
        self.skills = skills
        self.skills_config = skills_config
        self.constraints = constraints or []
        self.context_paths = context_paths or []
