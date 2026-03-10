"""Scanner for interaction-parent-granularity rule. Regex-only (nerfed mode).
Checks that parent nodes (epics) don't leak child-level detail in their statements.
Flags epics whose statements contain step-level language (When/Then, specific field names).
"""
import re
from pathlib import Path
from .base import BaseScanner, Violation

EPIC_HEADING = re.compile(r"^#{1,3}\s+Epic:\s*(.+)", re.IGNORECASE)
STEP_LANGUAGE = re.compile(
    r"\b(validates|checks|displays|saves|creates|deletes|"
    r"parses|filters|sorts|renders|calculates|processes)\s+"
    r"(the\s+)?(\w+\s+){0,2}(and\s+)?"
    r"(validates|checks|displays|saves|creates|deletes|"
    r"parses|filters|sorts|renders|calculates|processes)",
    re.IGNORECASE,
)
WHEN_THEN_IN_EPIC = re.compile(r"\bWhen\s+.+\bThen\s+", re.IGNORECASE)


class ParentGranularityScanner(BaseScanner):
    """Flags epic statements that contain child-level detail."""

    rule_id = "interaction-parent-granularity"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            m = EPIC_HEADING.match(line)
            if not m:
                continue
            statement = m.group(1)

            if WHEN_THEN_IN_EPIC.search(statement):
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message="Epic statement has When/Then step-level language — keep epic statements at scope level",
                    location=f"{source}:{i}",
                    severity="warning",
                    snippet=statement[:80],
                ))

            if STEP_LANGUAGE.search(statement):
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message="Epic statement lists multiple specific actions — describe scope, not individual steps",
                    location=f"{source}:{i}",
                    severity="warning",
                    snippet=statement[:80],
                ))

        return violations
