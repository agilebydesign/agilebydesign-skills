"""Scanner for domain-ooa-domain-language, domain-ooa-property-types,
domain-ooa-resource-concept-naming rules. Regex-only (nerfed mode).
Checks domain model language quality: standard types, domain naming, no technical terms.
"""
import re
from pathlib import Path
from .base import BaseScanner, Violation
from .domain_model_parser import parse_domain_model

STANDARD_TYPES = {
    "string", "number", "boolean", "list", "dictionary", "uniqueid", "instant",
}
STANDARD_TYPE_PATTERN = re.compile(r"^(List<\w+>|Dictionary<\w+,\s*\w+>)$", re.IGNORECASE)
TECHNICAL_NAMING = re.compile(
    r"\b(dto|dao|vo|entity|repository|service|controller|handler|"
    r"manager|helper|util|factory|impl|abstract|interface)\b",
    re.IGNORECASE,
)


class DomainPropertyTypesScanner(BaseScanner):
    """Flags properties that don't use standard types."""
    rule_id = "domain-ooa-property-types"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        modules = parse_domain_model(content)
        for mod in modules:
            for concept in mod.concepts:
                for prop in concept.properties:
                    type_lower = prop.type_name.lower()
                    if type_lower not in STANDARD_TYPES and not STANDARD_TYPE_PATTERN.match(prop.type_name):
                        violations.append(Violation(
                            rule_id=self.rule_id,
                            message=f"Property '{prop.name}' uses non-standard type '{prop.type_name}' — use String, Number, Boolean, List, Dictionary, UniqueID, Instant",
                            location=f"{source}:{concept.line_no}",
                            severity="warning",
                            snippet=f"{concept.name}.{prop.name}: {prop.type_name}",
                        ))
        return violations


class DomainNamingScanner(BaseScanner):
    """Flags concepts with technical naming patterns (DTO, DAO, Service, etc.)."""
    rule_id = "domain-ooa-domain-language"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        modules = parse_domain_model(content)
        for mod in modules:
            for concept in mod.concepts:
                if TECHNICAL_NAMING.search(concept.name):
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        message=f"Concept '{concept.name}' uses technical naming — use domain language",
                        location=f"{source}:{concept.line_no}",
                        severity="warning",
                        snippet=concept.name,
                    ))
        return violations


class DomainResourceNamingScanner(BaseScanner):
    """Flags concepts named after actions instead of resources/nouns."""
    rule_id = "domain-ooa-resource-concept-naming"

    ACTION_NAME = re.compile(r"^(Process|Handle|Manage|Execute|Perform|Do|Run|Validate|Check)\w+$")

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        modules = parse_domain_model(content)
        for mod in modules:
            for concept in mod.concepts:
                if self.ACTION_NAME.match(concept.name):
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        message=f"Concept '{concept.name}' named after action — concepts should be nouns/resources",
                        location=f"{source}:{concept.line_no}",
                        severity="warning",
                        snippet=concept.name,
                    ))
        return violations
