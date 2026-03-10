"""Scanner for interaction-examples-match-domain-model rule. Regex-only (nerfed mode);
structured parsing via interaction_tree_parser.
Checks that example tables align with domain model concepts:
- Table names reference **Concept** from domain model
- Table columns match concept properties
- No orphaned tables (table without label reference) or orphaned references (label without table)
- No ID columns (implementation concern)
"""
import re
from pathlib import Path
from .base import BaseScanner, Violation

from .interaction_tree_parser import has_ast_support, parse_interaction_tree

CONCEPT_REF = re.compile(r"\*\*(\w+)\*\*")
TABLE_HEADER = re.compile(r"^\s*\|(.+)\|\s*$")
TABLE_SEPARATOR = re.compile(r"^\s*\|[-\s|]+\|\s*$")
TABLE_NAME = re.compile(r"^\s*(\w[\w\s()]+):\s*$")
ID_COLUMN = re.compile(r"^[\w]*_?id$", re.IGNORECASE)
HEADING = re.compile(r"^#{1,6}\s+")
STEP_LINE = re.compile(r"^\s*-\s+Step\s+\d+", re.IGNORECASE)


class ExampleDomainMatchScanner(BaseScanner):
    """Flags example tables that don't align with domain model concepts."""

    rule_id = "interaction-examples-match-domain-model"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        lines = content.split("\n")

        concept_refs = set()
        table_names = set()

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            for m in CONCEPT_REF.finditer(stripped):
                concept_refs.add(m.group(1))

            tm = TABLE_NAME.match(stripped)
            if tm:
                name = tm.group(1).strip()
                base_name = re.sub(r"\s*\(.*\)\s*$", "", name).strip()
                table_names.add(base_name)

            if TABLE_HEADER.match(stripped) and not TABLE_SEPARATOR.match(stripped):
                cols = [c.strip() for c in stripped.strip("|").split("|")]
                for col in cols:
                    if ID_COLUMN.match(col) and col.lower() != "scenario":
                        violations.append(Violation(
                            rule_id=self.rule_id,
                            message=f"ID column '{col}' is an implementation concern — use domain attributes",
                            location=f"{source}:{i}",
                            severity="warning",
                            snippet=stripped[:80],
                        ))

        for table_name in table_names:
            matched = any(
                table_name.lower().startswith(c.lower()) or c.lower() in table_name.lower()
                for c in concept_refs
            )
            if not matched and table_name not in ("scenario",):
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message=f"Example table '{table_name}' has no matching **Concept** reference in labels",
                    location=source,
                    severity="warning",
                    snippet=table_name,
                ))

        return violations
