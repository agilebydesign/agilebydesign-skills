"""Scanner for domain-ooa-atomic-operations, domain-ooa-bidirectional-relationships,
domain-ooa-caller-receiver-state, domain-ooa-interaction-patterns,
domain-ooa-code-representation rules. Regex-only (nerfed mode).
Checks OOA-level domain model quality.
"""
import re
from pathlib import Path
from .base import BaseScanner, Violation
from .domain_model_parser import parse_domain_model


class DomainAtomicOpsScanner(BaseScanner):
    """Flags operations that combine multiple responsibilities (non-atomic)."""
    rule_id = "domain-ooa-atomic-operations"

    MULTI_OP = re.compile(r"\b(and|then|also|plus)\b", re.IGNORECASE)

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        modules = parse_domain_model(content)
        for mod in modules:
            for concept in mod.concepts:
                for op in concept.operations:
                    if self.MULTI_OP.search(op.name):
                        violations.append(Violation(
                            rule_id=self.rule_id,
                            message=f"Operation '{op.name}' on {concept.name} combines multiple actions — keep operations atomic",
                            location=f"{source}:{concept.line_no}",
                            severity="warning",
                            snippet=f"{concept.name}.{op.name}",
                        ))
        return violations


class DomainBidirectionalScanner(BaseScanner):
    """Flags concepts that reference each other without matching collaborators."""
    rule_id = "domain-ooa-bidirectional-relationships"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        concept_ref = re.compile(r"\*\*(\w+)\*\*")
        modules = parse_domain_model(content)
        concept_names = set()
        for mod in modules:
            for c in mod.concepts:
                concept_names.add(c.name)

        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            refs = concept_ref.findall(line)
            concept_refs_in_line = [r for r in refs if r in concept_names]
            if len(set(concept_refs_in_line)) >= 3:
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message=f"Line references {len(set(concept_refs_in_line))} concepts — check bidirectional relationships are modeled",
                    location=f"{source}:{i}",
                    severity="info",
                    snippet=line.strip()[:80],
                ))
        return violations


class DomainCallerReceiverScanner(BaseScanner):
    """Flags domain concepts without clear caller/receiver state flow."""
    rule_id = "domain-ooa-caller-receiver-state"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        modules = parse_domain_model(content)
        for mod in modules:
            for concept in mod.concepts:
                if concept.operations and not concept.properties:
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        message=f"Concept '{concept.name}' has operations but no properties — state should flow through properties",
                        location=f"{source}:{concept.line_no}",
                        severity="warning",
                        snippet=concept.name,
                    ))
        return violations


class DomainInteractionPatternsScanner(BaseScanner):
    """Flags operations that don't trace back to interactions in the tree."""
    rule_id = "domain-ooa-interaction-patterns"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        trigger_response = re.compile(r"(?:Trigger|Response|When|Then)\b.*\*\*(\w+)\*\*", re.IGNORECASE)
        interaction_concepts: set[str] = set()
        for line in content.split("\n"):
            for m in trigger_response.finditer(line):
                interaction_concepts.add(m.group(1).lower())

        modules = parse_domain_model(content)
        for mod in modules:
            for concept in mod.concepts:
                if concept.name.lower() not in interaction_concepts and interaction_concepts:
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        message=f"Concept '{concept.name}' not referenced in any Trigger/Response — ensure concepts trace to interactions",
                        location=f"{source}:{concept.line_no}",
                        severity="info",
                        snippet=concept.name,
                    ))
        return violations


class DomainCodeRepresentationScanner(BaseScanner):
    """Flags domain model content that uses code/implementation representation."""
    rule_id = "domain-ooa-code-representation"

    CODE_PATTERNS = re.compile(
        r"\b(class\s+\w+|def\s+\w+|function\s+\w+|import\s+\w+|"
        r"return\s+\w+|self\.\w+|this\.\w+|public\s+|private\s+|"
        r"protected\s+|static\s+|void\s+|int\s+\w+|str\s+\w+)\b",
    )

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        for i, line in enumerate(content.split("\n"), 1):
            stripped = line.strip()
            if stripped.startswith("```") or stripped.startswith("|"):
                continue
            if self.CODE_PATTERNS.search(stripped):
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message="Code/implementation syntax in domain model — use domain-level descriptions",
                    location=f"{source}:{i}",
                    severity="warning",
                    snippet=stripped[:80],
                ))
        return violations
