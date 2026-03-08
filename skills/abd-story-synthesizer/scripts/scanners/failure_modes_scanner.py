"""Scanner for interaction-failure-modes rule. Counts failure modes per interaction."""
import re
from pathlib import Path

from .base import BaseScanner, Violation


# Failure-Modes section pattern
FAILURE_MODES_HEADER = re.compile(r"^[-*]?\s*Failure-Modes?\s*:?\s*$", re.IGNORECASE)
FAILURE_ITEM = re.compile(r"^[-*]\s+(.+)$")
MAX_FAILURE_MODES = 3


class FailureModesScanner(BaseScanner):
    """Flags interactions with more than 3 failure modes."""

    rule_id = "interaction-failure-modes"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        lines = content.split("\n")

        in_failure_section = False
        failure_items: list[str] = []
        current_heading = ""
        line_no = 0

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped:
                if in_failure_section and failure_items:
                    if len(failure_items) > MAX_FAILURE_MODES:
                        violations.append(
                            Violation(
                                rule_id=self.rule_id,
                                message=f"Max {MAX_FAILURE_MODES} failure modes per interaction; found {len(failure_items)}",
                                location=f"{source}:{line_no}",
                                severity="warning",
                                snippet="; ".join(failure_items[:5]),
                            )
                        )
                    in_failure_section = False
                    failure_items = []
                continue

            if line.startswith("#") or line.startswith("###"):
                if failure_items and len(failure_items) > MAX_FAILURE_MODES:
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            message=f"Max {MAX_FAILURE_MODES} failure modes per interaction; found {len(failure_items)}",
                            location=f"{source}:{line_no}",
                            severity="warning",
                            snippet="; ".join(failure_items[:5]),
                        )
                    )
                in_failure_section = False
                failure_items = []
                current_heading = stripped
                line_no = i
                continue

            if FAILURE_MODES_HEADER.match(stripped):
                in_failure_section = True
                line_no = i
                failure_items = []
                continue

            if in_failure_section and FAILURE_ITEM.match(stripped):
                failure_items.append(FAILURE_ITEM.match(stripped).group(1).strip())

        if failure_items and len(failure_items) > MAX_FAILURE_MODES:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Max {MAX_FAILURE_MODES} failure modes per interaction; found {len(failure_items)}",
                    location=f"{source}:{line_no}",
                    severity="warning",
                    snippet="; ".join(failure_items[:5]),
                )
            )

        return violations
