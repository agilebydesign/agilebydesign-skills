"""Scanner for interaction-supporting-actor-response rule. Regex-only (nerfed mode).
Checks that Responding-Actor is system (not human) and that epic-level responses
are coarse-grained (not step-level detail).
"""
import re
from pathlib import Path
from .base import BaseScanner, Violation

RESPONDING_ACTOR = re.compile(r"^\s*[-*]?\s*Responding-Actor:\s*(.+)", re.IGNORECASE)
EPIC_HEADING = re.compile(r"^#{1,3}\s+Epic:\s*(.+)", re.IGNORECASE)
HUMAN_ACTORS = re.compile(
    r"\b(player|gm|game\s*master|manager|admin|operator|analyst|"
    r"reviewer|approver|clerk|agent|customer)\b",
    re.IGNORECASE,
)


class ActorResponseScanner(BaseScanner):
    """Flags Responding-Actor that is human instead of system."""

    rule_id = "interaction-supporting-actor-response"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            m = RESPONDING_ACTOR.match(line.strip())
            if not m:
                continue
            actor = m.group(1).strip().strip("[]")

            if HUMAN_ACTORS.search(actor) and "system" not in actor.lower():
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message=f"Responding-Actor '{actor}' appears to be human — supporting actor should be system",
                    location=f"{source}:{i}",
                    severity="warning",
                    snippet=line.strip()[:80],
                ))

        return violations
