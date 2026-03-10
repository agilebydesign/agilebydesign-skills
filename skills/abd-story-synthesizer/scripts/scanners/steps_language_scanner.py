"""Scanner for interaction-steps-use-and-and-but-for-conditions,
interaction-outcome-oriented-language,
interaction-examples-background-vs-scenario-setup rules.
Regex-only (nerfed mode).
"""
import re
from pathlib import Path
from .base import BaseScanner, Violation


class AndButConditionsScanner(BaseScanner):
    """Flags misuse of And/But — And for contrasting, But for positive chains."""
    rule_id = "interaction-steps-use-and-and-but-for-conditions"

    BUT_POSITIVE = re.compile(r"\bBut\s+(?:also|additionally|displays|shows|saves|creates)\b", re.IGNORECASE)
    AND_NEGATIVE = re.compile(r"\bAnd\s+(?:not|never|no\s+|without|does\s+not)\b", re.IGNORECASE)

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        for i, line in enumerate(content.split("\n"), 1):
            stripped = line.strip()
            if self.BUT_POSITIVE.search(stripped):
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message="'But' used for positive outcome — use 'And' for additional reactions, 'But' for negative constraints",
                    location=f"{source}:{i}",
                    severity="warning",
                    snippet=stripped[:80],
                ))
            if self.AND_NEGATIVE.search(stripped):
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message="'And not...' — use 'But' for negative conditions/constraints",
                    location=f"{source}:{i}",
                    severity="warning",
                    snippet=stripped[:80],
                ))
        return violations


class OutcomeLanguageScanner(BaseScanner):
    """Flags response/outcome text that uses mechanism language instead of outcome language."""
    rule_id = "interaction-outcome-oriented-language"

    MECHANISM_LANGUAGE = re.compile(
        r"\b(visualiz(?:e|es|ing)|render(?:s|ing)?|generat(?:e|es|ing)\s+(?:a|the)\s+(?:view|display|output)|"
        r"implement(?:s|ing)?|architect(?:s|ing)?|engineer(?:s|ing)?)\b",
        re.IGNORECASE,
    )
    RESPONSE_CONTEXT = re.compile(r"^\s*[-*]?\s*(?:Then|Response|Resulting|Behavior)\b", re.IGNORECASE)

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        for i, line in enumerate(content.split("\n"), 1):
            stripped = line.strip()
            if self.RESPONSE_CONTEXT.match(stripped) and self.MECHANISM_LANGUAGE.search(stripped):
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message="Response uses mechanism language — use outcome language (artifacts, results, not how)",
                    location=f"{source}:{i}",
                    severity="warning",
                    snippet=stripped[:80],
                ))
        return violations


class BackgroundSetupScanner(BaseScanner):
    """Flags Background/Pre-Condition sections that contain When/Then (actions, not state)."""
    rule_id = "interaction-examples-background-vs-scenario-setup"

    WHEN_THEN = re.compile(r"\b(When|Then)\b")

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        lines = content.split("\n")
        in_precondition = False

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if re.match(r"^\s*[-*]?\s*(?:Pre-Condition|Background)\s*:", stripped, re.IGNORECASE):
                in_precondition = True
                continue
            if stripped.startswith("#") or re.match(r"^\s*[-*]?\s*(?:Trigger|Response|When)\s*:", stripped, re.IGNORECASE):
                in_precondition = False
            if in_precondition and self.WHEN_THEN.search(stripped):
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message="Pre-Condition/Background contains When/Then — use Given/And for state only",
                    location=f"{source}:{i}",
                    severity="warning",
                    snippet=stripped[:80],
                ))

        return violations
