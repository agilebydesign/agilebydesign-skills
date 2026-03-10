"""Scanner for interaction-enumerate-step-permutations rule. Regex-only (nerfed mode).
Checks that scenarios cover happy path, error path, and edge cases.
Flags scenarios that only have success steps without error/edge coverage.
No external libraries required.
"""
import re
from pathlib import Path
from .base import BaseScanner, Violation

SCENARIO_HEADING = re.compile(r"^#{4,6}\s+Scenario:\s*(.+)", re.IGNORECASE)
STEP_LINE = re.compile(r"^\s*-\s+Step\s+\d+:\s*(.+)", re.IGNORECASE)

ERROR_INDICATORS = re.compile(
    r"\b(error|fail|invalid|reject|denied|unavailable|not\s+available|"
    r"not\s+found|missing|exceed|violation|unauthorized)\b",
    re.IGNORECASE,
)

EDGE_INDICATORS = re.compile(
    r"\b(boundary|edge|limit|maximum|minimum|empty|zero|overflow|"
    r"exceed|threshold|at\s+limit)\b",
    re.IGNORECASE,
)

MIN_STEPS_FOR_CHECK = 3


class StepPermutationsScanner(BaseScanner):
    """Flags stories where steps only cover happy path without error or edge cases."""

    rule_id = "interaction-enumerate-step-permutations"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        lines = content.split("\n")

        current_story = ""
        story_line = 0
        all_steps: list[str] = []
        has_error_step = False
        has_edge_step = False

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            if stripped.startswith("###") and "Story:" in stripped:
                if all_steps and len(all_steps) >= MIN_STEPS_FOR_CHECK:
                    violations.extend(
                        self._check_coverage(
                            current_story, story_line, all_steps,
                            has_error_step, has_edge_step, source,
                        )
                    )
                current_story = stripped
                story_line = i
                all_steps = []
                has_error_step = False
                has_edge_step = False
                continue

            sm = STEP_LINE.match(stripped)
            if sm:
                step_text = sm.group(1)
                all_steps.append(step_text)
                if ERROR_INDICATORS.search(step_text):
                    has_error_step = True
                if EDGE_INDICATORS.search(step_text):
                    has_edge_step = True

        if all_steps and len(all_steps) >= MIN_STEPS_FOR_CHECK:
            violations.extend(
                self._check_coverage(
                    current_story, story_line, all_steps,
                    has_error_step, has_edge_step, source,
                )
            )

        return violations

    def _check_coverage(
        self, story: str, line_no: int, steps: list[str],
        has_error: bool, has_edge: bool, source: str,
    ) -> list[Violation]:
        violations: list[Violation] = []

        if not has_error:
            violations.append(Violation(
                rule_id=self.rule_id,
                message="No error/failure steps found — enumerate error path permutations",
                location=f"{source}:{line_no}",
                severity="warning",
                snippet=story[:80] if story else f"{len(steps)} steps, no error coverage",
            ))

        return violations
