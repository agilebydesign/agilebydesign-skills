"""Scanner for interaction-ensure-vertical-slices rule. Regex-only (nerfed mode).
Checks that stories represent end-to-end vertical slices, not horizontal layers.
Flags stories whose names suggest horizontal slicing (e.g. "Design X", "Implement Y", "Test Z").
"""
import re
from pathlib import Path
from .base import BaseScanner, Violation

STORY_HEADING = re.compile(r"^#{1,6}\s+Story:\s*(.+)", re.IGNORECASE)
HORIZONTAL_VERBS = re.compile(
    r"^\s*\*?\*?(?:Design|Implement|Build|Code|Develop|Test|Deploy|"
    r"Configure|Setup|Install|Migrate|Refactor|Architect)\s+",
    re.IGNORECASE,
)


class VerticalSliceScanner(BaseScanner):
    """Flags story names that suggest horizontal slicing instead of vertical."""

    rule_id = "interaction-ensure-vertical-slices"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            m = STORY_HEADING.match(line)
            if not m:
                continue
            name = m.group(1).strip()
            name_clean = re.sub(r"\*\*\w+\*\*", "", name).strip()

            if HORIZONTAL_VERBS.match(name_clean):
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message="Story name suggests horizontal slice — use vertical, end-to-end slices",
                    location=f"{source}:{i}",
                    severity="warning",
                    snippet=name[:80],
                ))

        return violations
