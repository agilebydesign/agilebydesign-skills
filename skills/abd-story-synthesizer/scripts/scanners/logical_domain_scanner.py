"""Scanner for state-logical-domain-level rule. Detects implementation/technical terms in markdown."""
import re
from pathlib import Path

from .base import BaseScanner, Violation


# Terms that indicate implementation/technical level (regex-safe)
TECHNICAL_PATTERNS = [
    r"\bREST\s+API\b",
    r"\bINSERT\s+INTO\b",
    r"\bSELECT\s+.*\s+FROM\b",
    r"\bUPDATE\s+.*\s+SET\b",
    r"\bDELETE\s+FROM\b",
    r"\bCREATE\s+TABLE\b",
    r"\bJSON\b",
    r"\bXML\b",
    r"\bSQL\b",
    r"\bAPI\b",
    r"\bHTTP\s+\d{3}\b",
    r"\bDatabase\s+timeout\b",
    r"\bNetwork\s+unreachable\b",
    r"\bServer\s+crash\b",
    r"\bconfig\s+file\b",
    r"\b\.json\b",
    r"\b\.xml\b",
    r"\bclass\b",
    r"\bmethod\b",
    r"\bfunction\b",
    r"\bendpoint\b",
    r"\brequest/response\b",
]


class LogicalDomainScanner(BaseScanner):
    """Flags implementation/technical language in interaction tree and state model."""

    rule_id = "state-logical-domain-level"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            line_lower = line.lower()
            for pat in TECHNICAL_PATTERNS:
                if re.search(pat, line, re.IGNORECASE):
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            message="Implementation/technical term detected - keep at logical/domain level",
                            location=f"{source}:{i}",
                            severity="warning",
                            snippet=line.strip()[:100],
                        )
                    )
                    break

        return violations
