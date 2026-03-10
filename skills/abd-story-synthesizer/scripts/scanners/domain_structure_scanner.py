"""Scanner for domain-ooa-composition-structure, domain-ooa-concept-roles,
domain-ooa-integrate-concepts, domain-ooa-module-folder-mapping rules. Regex-only (nerfed mode).
Checks domain model structural quality: concepts have properties AND operations,
concepts are grouped into modules, composition/aggregation preferred over inheritance.
"""
import re
from pathlib import Path
from .base import BaseScanner, Violation
from .domain_model_parser import parse_domain_model


class DomainCompositionScanner(BaseScanner):
    """Flags concepts that use inheritance instead of composition/aggregation."""
    rule_id = "domain-ooa-composition-structure"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        inheritance_pattern = re.compile(r"\b(inherits|extends|subclass|superclass)\b", re.IGNORECASE)
        for i, line in enumerate(content.split("\n"), 1):
            if inheritance_pattern.search(line) and not line.strip().startswith("#"):
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message="Inheritance language detected — prefer composition/aggregation",
                    location=f"{source}:{i}",
                    severity="warning",
                    snippet=line.strip()[:80],
                ))
        return violations


class DomainConceptRolesScanner(BaseScanner):
    """Flags concepts without both properties and operations (incomplete functional units)."""
    rule_id = "domain-ooa-concept-roles"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        modules = parse_domain_model(content)
        for mod in modules:
            for concept in mod.concepts:
                if not concept.properties and not concept.operations:
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        message=f"Concept '{concept.name}' has no properties or operations — incomplete functional unit",
                        location=f"{source}:{concept.line_no}",
                        severity="warning",
                        snippet=concept.name,
                    ))
                elif not concept.operations:
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        message=f"Concept '{concept.name}' has properties but no operations",
                        location=f"{source}:{concept.line_no}",
                        severity="info",
                        snippet=concept.name,
                    ))
        return violations


class DomainIntegrateConceptsScanner(BaseScanner):
    """Flags **Concept** references in interaction tree that don't exist in domain model."""
    rule_id = "domain-ooa-integrate-concepts"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        modules = parse_domain_model(content)
        known_concepts = set()
        for mod in modules:
            for concept in mod.concepts:
                known_concepts.add(concept.name.lower())

        concept_ref = re.compile(r"\*\*(\w+)\*\*")
        for i, line in enumerate(content.split("\n"), 1):
            if line.strip().startswith("#") or line.strip().startswith("|"):
                continue
            for m in concept_ref.finditer(line):
                name = m.group(1)
                if name.lower() not in known_concepts and name not in ("DO", "NOT", "DO NOT"):
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        message=f"**{name}** referenced but not found in Domain Model",
                        location=f"{source}:{i}",
                        severity="warning",
                        snippet=line.strip()[:80],
                    ))
        return violations


class DomainModuleMappingScanner(BaseScanner):
    """Flags domain model without module groupings."""
    rule_id = "domain-ooa-module-folder-mapping"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        modules = parse_domain_model(content)
        if modules and all(m.name == "default" for m in modules):
            total_concepts = sum(len(m.concepts) for m in modules)
            if total_concepts >= 3:
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message=f"{total_concepts} concepts without module grouping — group related concepts into modules",
                    location=source,
                    severity="warning",
                ))
        return violations
