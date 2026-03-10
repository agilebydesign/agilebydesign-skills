"""Scanner for domain-synchronize-concepts and domain-logical-domain-level rules.
Regex-only (nerfed mode). The logical_domain_scanner already exists for the latter;
this scanner handles synchronize-concepts.
"""
import re
from pathlib import Path
from .base import BaseScanner, Violation

CONCEPT_REF = re.compile(r"\*\*(\w+)\*\*")
CONCEPT_HEADING = re.compile(r"^\*\*(\w[\w\s]*)\*\*\s*$")
EPIC_HEADING = re.compile(r"^#{1,3}\s+Epic:", re.IGNORECASE)


class DomainSyncScanner(BaseScanner):
    """Flags **Concept** references in interactions that have no Domain Model entry,
    and Domain Model concepts not referenced in any interaction."""
    rule_id = "domain-synchronize-concepts"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        lines = content.split("\n")

        interaction_concepts: set[str] = set()
        model_concepts: set[str] = set()
        in_domain_section = False

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            if "Domain Model" in stripped and stripped.startswith("#"):
                in_domain_section = True
                continue
            if stripped.startswith("#") and "Domain Model" not in stripped and in_domain_section:
                if EPIC_HEADING.match(stripped):
                    in_domain_section = False

            if in_domain_section:
                cm = CONCEPT_HEADING.match(stripped)
                if cm:
                    model_concepts.add(cm.group(1).strip())
            else:
                for m in CONCEPT_REF.finditer(stripped):
                    name = m.group(1)
                    if name not in ("DO", "NOT"):
                        interaction_concepts.add(name)

        for concept in interaction_concepts - model_concepts:
            if concept.lower() not in {c.lower() for c in model_concepts}:
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message=f"**{concept}** in interactions but missing from Domain Model — synchronize",
                    location=source,
                    severity="warning",
                    snippet=concept,
                ))

        for concept in model_concepts - interaction_concepts:
            if concept.lower() not in {c.lower() for c in interaction_concepts}:
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message=f"'{concept}' in Domain Model but not referenced in interactions — synchronize or remove",
                    location=source,
                    severity="info",
                    snippet=concept,
                ))

        return violations
