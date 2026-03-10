"""
Instructions — assembles sectioned content per operation.
"""
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import AgileContextEngine


class Instructions:
    """Assembles sections for an operation; injects context from engine."""

    def __init__(
        self,
        operation_sections: dict[str, list[str]],
        skill_path: Path,
        engine: "AgileContextEngine",
    ):
        self.operation_sections = operation_sections
        self.skill_path = Path(skill_path).resolve()
        self.engine = engine
        self._content_cache: dict[str, str] = {}

    def display_content(self, operation: str) -> str:
        """Assembles sections for operation; injects context from engine."""
        section_ids = self.operation_sections.get(operation, [])
        if not section_ids:
            return ""

        parts: list[str] = []
        pieces_dir = self.skill_path / "pieces"

        for sid in section_ids:
            text = self._get_section_content(sid, pieces_dir)
            if text:
                parts.append(text)
                parts.append("\n\n---\n\n")

        context = self._build_context_block()
        if context:
            parts.insert(0, context + "\n\n---\n\n")

        strategy_path = self.engine.strategy_path_override or self.engine.strategy_path
        if operation in ("generate_slice", "run_slice", "improve_strategy") and strategy_path:
            if Path(strategy_path).exists():
                strategy_content = Path(strategy_path).read_text(encoding="utf-8").strip()
                parts.append("## Strategy Document\n\n")
                parts.append(strategy_content)
                parts.append("\n\n---\n\n")

        return "".join(parts).rstrip() + "\n"

    def sections_included(self, operation: str) -> list[str]:
        return list(self.operation_sections.get(operation, []))

    def _get_section_content(self, section_id: str, pieces_dir: Path) -> str:
        if section_id.endswith(".rules") or "validation.rules" in section_id:
            rules_dir = self.skill_path / "rules"
            if not rules_dir.exists():
                return ""
            parts: list[str] = []
            for md in sorted(rules_dir.glob("*.md")):
                parts.append(md.read_text(encoding="utf-8").strip())
                parts.append("\n\n---\n\n")
            return "".join(parts).rstrip() if parts else ""

        # Map section_id prefix to pieces file:
        # story_synthesizer.interaction.model -> interaction.md
        # story_synthesizer.session.traversal -> session.md
        parts_split = section_id.split(".")
        if len(parts_split) < 2:
            return ""
        piece_name = parts_split[1]
        file_map = {
            "introduction": "introduction.md",
            "interaction": "interaction.md",
            "domain": "domain.md",
            "process": "process.md",
            "session": "session.md",
            "runs": "runs.md",
            "validation": "validation.md",
            "correct": "correct.md",
        }
        fpath = file_map.get(piece_name)
        if not fpath:
            return ""
        path = pieces_dir / fpath
        if not path.exists():
            return ""

        text = path.read_text(encoding="utf-8")
        marker = f"<!-- section: {section_id} -->"
        if marker not in text:
            return text.strip()

        start = text.index(marker) + len(marker)
        rest = text[start:]
        idx = rest.find("<!-- section:")
        if idx >= 0:
            return rest[:idx].strip()
        return rest.strip()

    def _build_context_block(self) -> str:
        lines: list[str] = [
            "**Execute these instructions.** You are the AI. Proceed directly to the task. Do not ask the user to paste, copy, or repeat these instructions elsewhere.",
            "",
        ]
        if self.engine.workspace_path:
            lines.append(f"**Workspace:** `{self.engine.workspace_path}`")
        if self.engine.strategy_path or self.engine.strategy_path_override:
            p = self.engine.strategy_path_override or self.engine.strategy_path
            lines.append(f"**Strategy path:** `{p}`")
        if self.engine.context_paths:
            lines.append("**Context paths:**")
            for path in self.engine.context_paths:
                lines.append(f"- `{path}`")
        if len(lines) <= 2:
            return ""
        return "## Context\n\n" + "\n".join(lines)
