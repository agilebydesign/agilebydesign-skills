"""Scanner for interaction-consistent-steps-across-domains rule. Regex-only (nerfed mode).
Detects stories under the same epic that have inconsistent step depth — e.g. one story
has 6 steps and a sibling has 1 step, suggesting inconsistent exploration.
No external libraries required.
"""
import re
from pathlib import Path
from .base import BaseScanner, Violation

EPIC_HEADING = re.compile(r"^(#{1,3})\s+Epic:\s*(.+)", re.IGNORECASE)
STORY_HEADING = re.compile(r"^(#{1,4})\s+Story:\s*(.+)", re.IGNORECASE)
STEP_LINE = re.compile(r"^\s*-\s+Step\s+\d+", re.IGNORECASE)
DEPTH_RATIO_THRESHOLD = 3.0


class ConsistentStepsScanner(BaseScanner):
    """Flags sibling stories under the same epic with inconsistent step counts."""

    rule_id = "interaction-consistent-steps-across-domains"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        lines = content.split("\n")

        epics: dict[str, list[tuple[str, int, int]]] = {}
        current_epic = ""
        current_story = ""
        current_story_line = 0
        step_count = 0

        def flush_story():
            nonlocal current_story, step_count
            if current_story and current_epic:
                if current_epic not in epics:
                    epics[current_epic] = []
                epics[current_epic].append((current_story, current_story_line, step_count))
            current_story = ""
            step_count = 0

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            em = EPIC_HEADING.match(stripped)
            if em:
                flush_story()
                current_epic = em.group(2).strip()
                continue

            sm = STORY_HEADING.match(stripped)
            if sm:
                flush_story()
                current_story = sm.group(2).strip()
                current_story_line = i
                continue

            if STEP_LINE.match(stripped):
                step_count += 1

        flush_story()

        for epic_name, stories in epics.items():
            stories_with_steps = [(s, l, c) for s, l, c in stories if c > 0]
            if len(stories_with_steps) < 2:
                continue

            counts = [c for _, _, c in stories_with_steps]
            max_c = max(counts)
            min_c = min(counts)

            if min_c > 0 and max_c / min_c >= DEPTH_RATIO_THRESHOLD:
                for name, line_no, count in stories_with_steps:
                    if count == min_c:
                        violations.append(Violation(
                            rule_id=self.rule_id,
                            message=f"Story has {count} steps vs sibling with {max_c} — keep depth consistent across connected domains",
                            location=f"{source}:{line_no}",
                            severity="warning",
                            snippet=name[:80],
                        ))

        return violations
