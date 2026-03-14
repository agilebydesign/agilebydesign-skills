"""Parses domain model markdown into structured concepts. Pure stdlib."""
import re
from dataclasses import dataclass, field


@dataclass
class DomainProperty:
    type_name: str
    name: str
    collaborators: list[str] = field(default_factory=list)

@dataclass
class DomainOperation:
    name: str
    params: list[str] = field(default_factory=list)
    collaborators: list[str] = field(default_factory=list)

@dataclass
class DomainConcept:
    name: str
    base_concept: str = ""
    module: str = ""
    properties: list[DomainProperty] = field(default_factory=list)
    operations: list[DomainOperation] = field(default_factory=list)
    line_no: int = 0

@dataclass
class DomainModule:
    name: str
    concepts: list[DomainConcept] = field(default_factory=list)
    line_no: int = 0


CONCEPT_HEADING = re.compile(r"^\*\*(\w[\w\s]*)\*\*\s*$")
CONCEPT_HEADING_MD = re.compile(r"^#{2,4}\s+(?!Module:)(\w[\w\s]*?)(?:\s*:\s*(\w[\w\s]*))?\s*$")
CONCEPT_WITH_BASE = re.compile(r"^(\w[\w\s]*)\s*:\s*(\w[\w\s]*)$")
MODULE_HEADING = re.compile(r"^#{2,4}\s+Module:\s*(.+)", re.IGNORECASE)
PROPERTY_LINE = re.compile(r"^[-*]\s+(String|Number|Boolean|List|Dictionary|UniqueID|Instant|List<\w+>|Dictionary<\w+,\s*\w+>)\s+(\w+)", re.IGNORECASE)
OPERATION_LINE = re.compile(r"^[-*]\s+Operations?:\s*(.+)", re.IGNORECASE)
COLLABORATOR_LINE = re.compile(r"^\s+([\w\s,]+)$")


def parse_domain_model(content: str) -> list[DomainModule]:
    """Parse domain model markdown into structured modules and concepts."""
    modules: list[DomainModule] = []
    lines = content.split("\n")
    
    current_module = DomainModule(name="default", line_no=1)
    current_concept: DomainConcept | None = None

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        mm = MODULE_HEADING.match(stripped)
        if mm:
            if current_concept:
                current_module.concepts.append(current_concept)
                current_concept = None
            if current_module.concepts:
                modules.append(current_module)
            current_module = DomainModule(name=mm.group(1).strip(), line_no=i)
            continue

        cm_md = CONCEPT_HEADING_MD.match(stripped)
        if cm_md:
            if current_concept:
                current_module.concepts.append(current_concept)
            name = cm_md.group(1).strip()
            base = (cm_md.group(2) or "").strip()
            current_concept = DomainConcept(name=name, base_concept=base, line_no=i)
            continue

        cm = CONCEPT_HEADING.match(stripped)
        if cm:
            if current_concept:
                current_module.concepts.append(current_concept)
            current_concept = DomainConcept(name=cm.group(1).strip(), line_no=i)
            continue

        if current_concept:
            pm = PROPERTY_LINE.match(stripped)
            if pm:
                current_concept.properties.append(
                    DomainProperty(type_name=pm.group(1), name=pm.group(2))
                )

            om = OPERATION_LINE.match(stripped)
            if om:
                ops_text = om.group(1)
                for op in ops_text.split(","):
                    op = op.strip()
                    if op:
                        current_concept.operations.append(DomainOperation(name=op))

    if current_concept:
        current_module.concepts.append(current_concept)
    if current_module.concepts:
        modules.append(current_module)

    return modules


def get_all_concept_names(modules: list[DomainModule]) -> set[str]:
    """Return all concept names from parsed domain model."""
    names: set[str] = set()
    for mod in modules:
        for concept in mod.concepts:
            names.add(concept.name)
    return names


def get_all_property_names(modules: list[DomainModule]) -> set[str]:
    """Return all property names from parsed domain model."""
    props: set[str] = set()
    for mod in modules:
        for concept in mod.concepts:
            for prop in concept.properties:
                props.add(prop.name)
    return props
