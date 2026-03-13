"""Scanner: flag domain concepts with generic resolver/handler/manager names."""
import re
from .base import BaseScanner, Violation


class GenericResolverScanner(BaseScanner):
    rule_id = "domain-ooa-no-generic-resolvers"

    GENERIC_NAMES = re.compile(
        r"\b\w*(Resolver|Handler|Manager|Processor|Dispatcher|Router|Helper|Utility|Utils)\b"
    )

    def scan(self, content: str, source_path=None) -> list[Violation]:
        violations = []

        for line in content.split("\n"):
            concept_match = re.match(r"^\*\*(\w[\w\s]*)\*\*", line)
            if concept_match:
                name = concept_match.group(1).strip()
                match = self.GENERIC_NAMES.search(name)
                if match:
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        message=f"Concept '{name}' uses generic name pattern '{match.group(1)}' — consider a specific domain object instead",
                        location=str(source_path or ""),
                        snippet=name,
                    ))

        return violations
