"""Scanner for interaction-approximately-4-to-9-children rule. Regex-only (nerfed mode).
Counts children per parent node (stories per sub-epic, steps per story).
Flags nodes with fewer than 4 or more than 9 children.
"""
import re
from pathlib import Path
from .base import BaseScanner, Violation

HEADING = re.compile(r"^(#{1,6})\s+(.+)")
STEP_LINE = re.compile(r"^\s*[-*]\s+Step\s+\d+", re.IGNORECASE)


class HierarchySizingScanner(BaseScanner):
    """Flags parent nodes with fewer than 4 or more than 9 children."""

    rule_id = "interaction-approximately-4-to-9-children"
    MIN_CHILDREN = 4
    MAX_CHILDREN = 9

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        lines = content.split("\n")

        current_parent = ""
        current_parent_line = 0
        current_level = 0
        child_count = 0

        for i, line in enumerate(lines, 1):
            m = HEADING.match(line)
            if m:
                level = len(m.group(1))
                name = m.group(2).strip()

                if current_parent and current_level > 0 and level <= current_level:
                    v = self._check_count(current_parent, current_parent_line, child_count, source)
                    if v:
                        violations.append(v)
                    child_count = 0

                if "Epic:" in name or "Story:" in name:
                    current_parent = name
                    current_parent_line = i
                    current_level = level
                    child_count = 0
                elif current_level > 0 and level == current_level + 1:
                    child_count += 1

            if STEP_LINE.match(line) and current_parent and "Story:" in current_parent:
                child_count += 1

        if current_parent:
            v = self._check_count(current_parent, current_parent_line, child_count, source)
            if v:
                violations.append(v)

        return violations

    def _check_count(self, parent: str, line_no: int, count: int, source: str) -> Violation | None:
        if count == 0:
            return None
        if count < self.MIN_CHILDREN:
            return Violation(
                rule_id=self.rule_id,
                message=f"'{parent[:60]}' has {count} children (minimum {self.MIN_CHILDREN})",
                location=f"{source}:{line_no}",
                severity="warning",
                snippet=parent[:80],
            )
        if count > self.MAX_CHILDREN:
            return Violation(
                rule_id=self.rule_id,
                message=f"'{parent[:60]}' has {count} children (maximum {self.MAX_CHILDREN})",
                location=f"{source}:{line_no}",
                severity="warning",
                snippet=parent[:80],
            )
        return None
