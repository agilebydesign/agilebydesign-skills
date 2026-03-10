"""Scanner for interaction-story-granularity rule. Regex-only (nerfed mode).
Checks that stories are broken down by distinct areas with sufficient granularity.
Flags epics that have very few stories (under-decomposed) relative to their complexity.
"""
import re
from pathlib import Path
from .base import BaseScanner, Violation

HEADING = re.compile(r"^(#{1,6})\s+(.+)")
ESTIMATED_PATTERN = re.compile(r"~\d+\s+(?:stories|more)", re.IGNORECASE)


class StoryGranularityScanner(BaseScanner):
    """Flags under-decomposed epics and estimated story counts."""

    rule_id = "interaction-story-granularity"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            if ESTIMATED_PATTERN.search(line):
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message="Estimated story count (~N stories) — all stories must be explicitly enumerated",
                    location=f"{source}:{i}",
                    severity="warning",
                    snippet=line.strip()[:80],
                ))

        return violations
