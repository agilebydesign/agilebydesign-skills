"""Scanner: flag domain concepts that look like orchestrators making domain decisions."""
import re
from .base import BaseScanner, Violation


class ThinOrchestrationScanner(BaseScanner):
    rule_id = "domain-ooa-thin-orchestration"

    ORCHESTRATOR_NAMES = re.compile(
        r"\b(Manager|Controller|Coordinator|Orchestrator|Dispatcher|Engine|Processor|Service)\b",
        re.IGNORECASE,
    )

    def scan(self, content: str, source_path=None) -> list[Violation]:
        violations = []
        current_concept = ""
        op_count = 0
        prop_count = 0

        for line in content.split("\n"):
            concept_match = re.match(r"^\*\*(\w[\w\s]*)\*\*", line)
            if concept_match:
                if current_concept and op_count > 5 and prop_count < 3:
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        message=f"Concept '{current_concept}' has {op_count} operations but only {prop_count} properties — may be a fat orchestrator",
                        location=str(source_path or ""),
                        snippet=current_concept,
                    ))
                current_concept = concept_match.group(1).strip()
                op_count = 0
                prop_count = 0

                if self.ORCHESTRATOR_NAMES.search(current_concept):
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        message=f"Concept '{current_concept}' has an orchestrator-style name — verify it stays thin",
                        location=str(source_path or ""),
                        severity="info",
                        snippet=current_concept,
                    ))

            if re.match(r"^-\s+\w+\s+\w+\(", line):
                op_count += 1
            elif re.match(r"^-\s+(String|Number|Boolean|List|Dictionary|UniqueID|Instant)", line):
                prop_count += 1

        if current_concept and op_count > 5 and prop_count < 3:
            violations.append(Violation(
                rule_id=self.rule_id,
                message=f"Concept '{current_concept}' has {op_count} operations but only {prop_count} properties — may be a fat orchestrator",
                location=str(source_path or ""),
                snippet=current_concept,
            ))

        return violations
