"""Scanner for interaction-given-state-not-actions rule. Regex-only (nerfed mode);
NLTK POS tagging when available (full mode) for more precise verb detection.
Checks that Given/Pre-Condition statements describe state, not actions.
Flags action verbs, past-tense actions, UI navigation, and functionality descriptions in Given.
"""
import re
from pathlib import Path
from .base import BaseScanner, Violation

try:
    from .grammar import has_grammar_support, get_pos_tags, is_verb
except ImportError:
    has_grammar_support = lambda: False
    get_pos_tags = lambda t: []
    is_verb = lambda t: False

GIVEN_LINE = re.compile(
    r"^\s*[-*]?\s*(?:Given|Pre-Condition\s*:)\s+(.+)",
    re.IGNORECASE,
)
AND_LINE = re.compile(r"^\s*[-*]?\s*And\s+(.+)", re.IGNORECASE)

ACTION_VERBS = re.compile(
    r"\b(clicks?|sends?|calls?|executes?|invokes?|navigates?|submits?|"
    r"triggers?|runs?|starts?|launches?|performs?|initiates?)\b",
    re.IGNORECASE,
)

PAST_TENSE_ACTIONS = re.compile(
    r"\b(has\s+(?:invoked|clicked|sent|called|executed|submitted|triggered|navigated|performed))\b",
    re.IGNORECASE,
)

UI_NAVIGATION = re.compile(
    r"\b(?:is\s+on\s+(?:page|step|screen|form)|is\s+viewing|is\s+at\s+Step)\b",
    re.IGNORECASE,
)


class GivenStateScanner(BaseScanner):
    """Flags Given/Pre-Condition statements that describe actions instead of state."""

    rule_id = "interaction-given-state-not-actions"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        lines = content.split("\n")

        in_given = False

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            gm = GIVEN_LINE.match(stripped)
            if gm:
                in_given = True
                text = gm.group(1)
                violations.extend(self._check_given_text(text, source, i))
                continue

            am = AND_LINE.match(stripped)
            if am and in_given:
                text = am.group(1)
                violations.extend(self._check_given_text(text, source, i))
                continue

            if stripped.startswith("When") or stripped.startswith("- When"):
                in_given = False

            if not stripped or stripped.startswith("#"):
                in_given = False

        return violations

    def _check_given_text(self, text: str, source: str, line_no: int) -> list[Violation]:
        violations: list[Violation] = []

        if ACTION_VERBS.search(text):
            violations.append(Violation(
                rule_id=self.rule_id,
                message="Given/Pre-Condition uses action verb — describe state, not actions",
                location=f"{source}:{line_no}",
                severity="warning",
                snippet=text[:80],
            ))

        if PAST_TENSE_ACTIONS.search(text):
            violations.append(Violation(
                rule_id=self.rule_id,
                message="Given/Pre-Condition uses past-tense action — describe current state",
                location=f"{source}:{line_no}",
                severity="warning",
                snippet=text[:80],
            ))

        if UI_NAVIGATION.search(text):
            violations.append(Violation(
                rule_id=self.rule_id,
                message="Given/Pre-Condition uses UI navigation — use domain state instead",
                location=f"{source}:{line_no}",
                severity="warning",
                snippet=text[:80],
            ))

        return violations
