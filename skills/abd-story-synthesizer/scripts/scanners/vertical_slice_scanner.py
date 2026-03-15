"""Scanner for interaction-ensure-vertical-slices rule. Regex-only (nerfed mode).
Checks that SLICES (not stories) represent end-to-end vertical slices, not horizontal layers.
Flags slice descriptions that suggest horizontal slicing (e.g. "Design layer", "API only").
Stories within a slice are not checked — the rule applies to the slice level.
"""
import re
from pathlib import Path
from .base import BaseScanner, Violation

# Slice metadata: **Slice:** 1 — Basic character + core flow
SLICE_META = re.compile(r"^\s*\*\*Slice:\*\*\s*(.+)", re.IGNORECASE)
HORIZONTAL_SLICE = re.compile(
    r"(?:Design\s+layer|Implement\s+layer|API\s+only|UI\s+only|"
    r"Database\s+layer|Backend\s+only|Frontend\s+only|Test\s+suite\s+only)",
    re.IGNORECASE,
)


class VerticalSliceScanner(BaseScanner):
    """Flags slice descriptions that suggest horizontal slicing instead of vertical.
    Does NOT flag stories — vertical slice applies to slices, not individual stories."""

    rule_id = "interaction-ensure-vertical-slices"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            m = SLICE_META.match(line)
            if not m:
                continue
            desc = m.group(1).strip()
            if HORIZONTAL_SLICE.search(desc):
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message="Slice description suggests horizontal slice — use vertical, end-to-end slices",
                    location=f"{source}:{i}",
                    severity="warning",
                    snippet=desc[:80],
                ))

        return violations
