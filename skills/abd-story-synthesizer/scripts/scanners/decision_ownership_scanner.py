"""Scanner: flag anemic domain concepts (properties without operations) and orphaned decisions."""
import re
from .base import BaseScanner, Violation


class DecisionOwnershipScanner(BaseScanner):
    rule_id = "domain-ooa-behavior-owns-decision"

    def scan(self, content: str, source_path=None) -> list[Violation]:
        violations = []
        current_concept = ""
        has_properties = False
        has_operations = False

        for line in content.split("\n"):
            concept_match = re.match(r"^\*\*(\w[\w\s]*)\*\*", line)
            if concept_match:
                if current_concept and has_properties and not has_operations:
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        message=f"Concept '{current_concept}' has properties but no operations — anemic model; decisions about this data likely live elsewhere",
                        location=str(source_path or ""),
                        snippet=current_concept,
                    ))
                current_concept = concept_match.group(1).strip()
                has_properties = False
                has_operations = False

            if re.match(r"^-\s+(String|Number|Boolean|List|Dictionary|UniqueID|Instant)", line):
                has_properties = True
            if re.match(r"^-\s+\w+\s+\w+\(", line) or re.match(r"^-\s+Operations:", line):
                has_operations = True

        if current_concept and has_properties and not has_operations:
            violations.append(Violation(
                rule_id=self.rule_id,
                message=f"Concept '{current_concept}' has properties but no operations — anemic model; decisions about this data likely live elsewhere",
                location=str(source_path or ""),
                snippet=current_concept,
            ))

        return violations
