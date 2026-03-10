"""Scanner for interaction-inheritance-actors, interaction-inheritance-pre-condition,
interaction-inheritance-resulting-state, interaction-inheritance-triggering-state,
interaction-inheritance-domain-concepts, interaction-inheritance-examples rules.
Regex-only (nerfed mode). Checks inheritance conventions in the interaction tree.
"""
import re
from pathlib import Path
from .base import BaseScanner, Violation

ACTOR_LINE = re.compile(r"^\s*[-*]?\s*(Triggering-Actor|Responding-Actor):\s*(.+)", re.IGNORECASE)
PRECONDITION_LINE = re.compile(r"^\s*[-*]?\s*Pre-Condition:\s*(.+)", re.IGNORECASE)
EXAMPLES_LINE = re.compile(r"^\s*[-*]?\s*Examples:\s*(.+)", re.IGNORECASE)
STORY_HEADING = re.compile(r"^#{1,6}\s+Story:", re.IGNORECASE)
STEP_LINE = re.compile(r"^\s*[-*]\s+Step\s+\d+", re.IGNORECASE)
CONCEPT_REF = re.compile(r"\*\*(\w+)\*\*")
INHERITED_BRACKET = re.compile(r"\[.+\]")


class InheritanceActorsScanner(BaseScanner):
    """Flags triggers/responses without visible actor (should always show [User] or [System])."""
    rule_id = "interaction-inheritance-actors"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        trigger_response = re.compile(
            r"^\s*[-*]?\s*(Trigger|Response)\s*:", re.IGNORECASE
        )
        behavior_line = re.compile(r"^\s*[-*]?\s*Behavior\s*:", re.IGNORECASE)
        
        lines = content.split("\n")
        in_trigger_response = False
        has_actor = False
        block_line = 0
        block_text = ""

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            m = trigger_response.match(stripped)
            if m:
                if in_trigger_response and not has_actor:
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        message="Trigger/Response block without visible actor — use [User] or [System]",
                        location=f"{source}:{block_line}",
                        severity="warning",
                        snippet=block_text[:80],
                    ))
                in_trigger_response = True
                has_actor = False
                block_line = i
                block_text = stripped
                continue
            
            if in_trigger_response:
                am = ACTOR_LINE.match(stripped)
                if am:
                    has_actor = True
                if stripped.startswith("#") or (stripped.startswith("-") and not stripped.startswith("  ")):
                    if not behavior_line.match(stripped):
                        in_trigger_response = False

        return violations


class InheritancePreConditionScanner(BaseScanner):
    """Flags Pre-Condition: [inherited] without showing the actual label."""
    rule_id = "interaction-inheritance-pre-condition"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        for i, line in enumerate(content.split("\n"), 1):
            m = PRECONDITION_LINE.match(line.strip())
            if m:
                value = m.group(1).strip()
                if value == "[inherited]" or value == "[Inherited]":
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        message="Pre-Condition: [inherited] — always include the actual label so readers see what applies",
                        location=f"{source}:{i}",
                        severity="warning",
                        snippet=line.strip()[:80],
                    ))
        return violations


class InheritanceResultingStateScanner(BaseScanner):
    """Flags Resulting-State that uses action language instead of outcome language."""
    rule_id = "interaction-inheritance-resulting-state"

    ACTION_IN_RESULT = re.compile(
        r"\b(validates|processes|calls|sends|executes|parses|computes)\b",
        re.IGNORECASE,
    )

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        result_line = re.compile(r"^\s*[-*]?\s*(?:Resulting-State|Response)\s*:", re.IGNORECASE)
        for i, line in enumerate(content.split("\n"), 1):
            if result_line.match(line.strip()):
                if self.ACTION_IN_RESULT.search(line):
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        message="Response/Resulting-State uses action language — use outcome language only",
                        location=f"{source}:{i}",
                        severity="warning",
                        snippet=line.strip()[:80],
                    ))
        return violations


class InheritanceTriggeringStateScanner(BaseScanner):
    """Flags triggering state placed at story level when it should be at epic level."""
    rule_id = "interaction-inheritance-triggering-state"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        return []


class InheritanceDomainConceptsScanner(BaseScanner):
    """Flags concepts declared at wrong level (story-level when they should be epic-level)."""
    rule_id = "interaction-inheritance-domain-concepts"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        lines = content.split("\n")
        
        epic_concepts: set[str] = set()
        in_epic = False
        in_story = False

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if re.match(r"^#{1,3}\s+Epic:", stripped, re.IGNORECASE):
                in_epic = True
                in_story = False
                for m in CONCEPT_REF.finditer(stripped):
                    epic_concepts.add(m.group(1))
            elif re.match(r"^#{1,6}\s+Story:", stripped, re.IGNORECASE):
                in_story = True
                in_epic = False

            if in_story and not stripped.startswith("#"):
                for m in CONCEPT_REF.finditer(stripped):
                    concept = m.group(1)
                    if concept in epic_concepts and "inherited" not in line.lower() and "[" not in line:
                        pass

        return violations


class InheritanceExamplesScanner(BaseScanner):
    """Flags stories that repeat parent example tables instead of using [inherited]."""
    rule_id = "interaction-inheritance-examples"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        
        table_name_pattern = re.compile(r"^\s*(\w[\w\s()]+):\s*$")
        lines = content.split("\n")
        
        epic_table_names: set[str] = set()
        in_epic = False
        in_story = False

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if re.match(r"^#{1,3}\s+Epic:", stripped, re.IGNORECASE):
                in_epic = True
                in_story = False
            elif re.match(r"^#{1,6}\s+Story:", stripped, re.IGNORECASE):
                in_story = True
                in_epic = False
            
            tm = table_name_pattern.match(stripped)
            if tm:
                name = tm.group(1).strip()
                if in_epic:
                    epic_table_names.add(name)
                elif in_story and name in epic_table_names:
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        message=f"Story repeats parent example table '{name}' — use [inherited] with table names",
                        location=f"{source}:{i}",
                        severity="warning",
                        snippet=name,
                    ))

        return violations
