"""
Instructions — assembles sectioned content per operation.
"""
import re
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import AgileContextEngine


def _parse_rule_tags(content: str) -> set[str]:
    """Extract tags from YAML frontmatter. Returns empty set if no tags."""
    match = re.search(r"^---\s*\ntags:\s*\[([^\]]*)\]", content, re.MULTILINE | re.DOTALL)
    if match:
        return {t.strip() for t in match.group(1).split(",") if t.strip()}
    match = re.search(r"^---\s*\ntags:\s*(.+?)(?:\n|$)", content, re.MULTILINE)
    if match:
        return {t.strip() for t in match.group(1).split(",") if t.strip()}
    return set()


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
        content_dir = self.skill_path / "content"

        for sid in section_ids:
            text = self._get_section_content(sid, content_dir)
            if text:
                parts.append(text)
                parts.append("\n\n---\n\n")

        context = self._build_context_block()
        if context:
            parts.insert(0, context + "\n\n---\n\n")

        if operation in ("generate_slice", "run_slice", "validate_run", "validate_slice", "improve_strategy", "answer_questions", "proceed_slice") and self.engine.strategy_path:
            if self.engine.strategy_path.exists():
                strategy_content = self.engine.strategy_path.read_text(encoding="utf-8").strip()
                parts.append("## Strategy Document\n\n")
                parts.append(strategy_content)
                parts.append("\n\n---\n\n")

        return "".join(parts).rstrip() + "\n"

    def sections_included(self, operation: str) -> list[str]:
        return list(self.operation_sections.get(operation, []))

    def _get_section_content(self, section_id: str, content_dir: Path) -> str:
        if section_id.endswith(".validation.rules"):
            rules_dir = self.skill_path / "rules"
            if not rules_dir.exists():
                return ""
            components = getattr(self.engine, "components", None) or set()
            parts: list[str] = []
            for md in sorted(rules_dir.glob("*.md")):
                content = md.read_text(encoding="utf-8")
                if components:
                    rule_tags = _parse_rule_tags(content)
                    if rule_tags and not (rule_tags & components):
                        continue
                parts.append(content.strip())
                parts.append("\n\n---\n\n")
            return "".join(parts).rstrip() if parts else ""

        # Section-specific file mapping for split output (e.g. story_synthesizer)
        section_file_map = {
            "story_synthesizer.output.interaction_tree": "output/interaction-tree-output.md",
            "story_synthesizer.output.state_model": "output/state-model-output.md",
        }
        if section_id in section_file_map:
            fname = section_file_map[section_id]
        else:
            domain = section_id.split(".")[1] if "." in section_id else ""
            file_map = {
                "process": "process.md",
                "strategy": "strategy.md",
                "output": "output.md",
                "validation": "validation.md",
                "core": "core.md",
            }
            fname = file_map.get(domain, "process.md")
        path = content_dir / fname
        if not path.exists():
            return ""

        text = path.read_text(encoding="utf-8")
        marker = f"<!-- section: {section_id} -->"
        if marker not in text:
            return ""

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
        if self.engine.strategy_path:
            lines.append(f"**Strategy path:** `{self.engine.strategy_path}`")
        if self.engine.context_paths:
            lines.append("**Context paths:**")
            for p in self.engine.context_paths:
                lines.append(f"- `{p}`")
        if not lines:
            return ""
        return "## Context\n\n" + "\n".join(lines)
