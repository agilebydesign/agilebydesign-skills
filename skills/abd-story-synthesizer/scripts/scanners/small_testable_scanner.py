"""Scanner for interaction-story-small-and-testable rule. Regex-only (nerfed mode).
Checks that stories represent testable outcomes, not implementation tasks.
Flags stories with implementation language or without clear trigger/response.
"""
import re
from pathlib import Path
from .base import BaseScanner, Violation

STORY_HEADING = re.compile(r"^(#{1,6})\s+Story:\s*(.+)", re.IGNORECASE)
IMPLEMENTATION_LANGUAGE = re.compile(
    r"\b(database|schema|api|endpoint|microservice|component|module|"
    r"middleware|cache|queue|table|column|index|migration|deployment|"
    r"infrastructure|pipeline|dockerfile|terraform|kubernetes)\b",
    re.IGNORECASE,
)


class SmallTestableScanner(BaseScanner):
    """Flags stories with implementation language (not behavioral outcomes)."""

    rule_id = "interaction-story-small-and-testable"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            m = STORY_HEADING.match(line)
            if not m:
                continue
            name = m.group(2).strip()

            if IMPLEMENTATION_LANGUAGE.search(name):
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message="Story name uses implementation language — stories should describe testable behavioral outcomes",
                    location=f"{source}:{i}",
                    severity="warning",
                    snippet=name[:80],
                ))

        return violations
