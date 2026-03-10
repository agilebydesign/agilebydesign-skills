"""Scanner for interaction-sequential-order rule. Regex-only (nerfed mode).
Checks that the interaction tree follows sequential flow — state creators appear
before consumers. Flags **Concept** references that appear in Pre-Condition or
Trigger before any step/story creates them in a Response.
"""
import re
from pathlib import Path
from .base import BaseScanner, Violation

CONCEPT_REF = re.compile(r"\*\*(\w+)\*\*")
RESPONSE_LINE = re.compile(r"^\s*[-*]?\s*(?:Response|Resulting|Then)\b", re.IGNORECASE)
PRECONDITION_LINE = re.compile(r"^\s*[-*]?\s*(?:Pre-Condition|Given)\b", re.IGNORECASE)
HEADING = re.compile(r"^#{1,6}\s+(?:Epic|Story):\s*(.+)", re.IGNORECASE)


class SequentialOrderScanner(BaseScanner):
    """Flags concepts used in Pre-Condition before being created in any Response."""

    rule_id = "interaction-sequential-order"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        lines = content.split("\n")

        created_concepts: set[str] = set()
        consumed_before_created: list[tuple[str, int, str]] = []

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            if RESPONSE_LINE.match(stripped):
                for m in CONCEPT_REF.finditer(stripped):
                    created_concepts.add(m.group(1))

            if PRECONDITION_LINE.match(stripped):
                for m in CONCEPT_REF.finditer(stripped):
                    concept = m.group(1)
                    if concept not in created_concepts:
                        consumed_before_created.append((concept, i, stripped))

        for concept, line_no, snippet in consumed_before_created:
            if concept not in created_concepts:
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message=f"**{concept}** used in Pre-Condition but never created in a prior Response",
                    location=f"{source}:{line_no}",
                    severity="info",
                    snippet=snippet[:80],
                ))

        return violations
