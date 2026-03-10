"""Scanner for interaction-atomic-steps rule. Regex + stdlib difflib only (nerfed mode).
Detects repeated base logic across multiple steps — flags when steps copy-paste
trigger/response patterns with minor variations instead of stating only what differs.
Uses difflib.SequenceMatcher (stdlib) — no external libraries required.
"""
import re
from pathlib import Path
from difflib import SequenceMatcher
from .base import BaseScanner, Violation

STEP_LINE = re.compile(r"^\s*-\s+Step\s+\d+:\s*(.+)", re.IGNORECASE)
THEN_AND = re.compile(r"^\s*[-*]?\s*(?:Then|And)\s+(.+)", re.IGNORECASE)
DUPLICATION_THRESHOLD = 0.75


class AtomicStepsScanner(BaseScanner):
    """Flags steps that repeat base logic from earlier steps instead of stating only what differs."""

    rule_id = "interaction-atomic-steps"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        lines = content.split("\n")

        current_scenario_steps: list[tuple[int, str]] = []
        in_steps = False

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            if stripped.startswith("#") and "step" in stripped.lower():
                if current_scenario_steps:
                    violations.extend(
                        self._check_step_duplication(current_scenario_steps, source)
                    )
                current_scenario_steps = []
                in_steps = True
                continue

            if stripped.startswith("#") and "step" not in stripped.lower():
                if current_scenario_steps:
                    violations.extend(
                        self._check_step_duplication(current_scenario_steps, source)
                    )
                current_scenario_steps = []
                in_steps = False
                continue

            if in_steps:
                sm = STEP_LINE.match(stripped)
                if sm:
                    current_scenario_steps.append((i, sm.group(1).strip()))

        if current_scenario_steps:
            violations.extend(
                self._check_step_duplication(current_scenario_steps, source)
            )

        return violations

    def _check_step_duplication(
        self, steps: list[tuple[int, str]], source: str
    ) -> list[Violation]:
        violations: list[Violation] = []
        if len(steps) < 3:
            return violations

        first_line, first_text = steps[0]
        for line_no, text in steps[1:]:
            ratio = SequenceMatcher(None, first_text.lower(), text.lower()).ratio()
            if ratio >= DUPLICATION_THRESHOLD:
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message=f"Step repeats {ratio:.0%} of base step — state only what differs",
                    location=f"{source}:{line_no}",
                    severity="warning",
                    snippet=text[:80],
                ))

        return violations
