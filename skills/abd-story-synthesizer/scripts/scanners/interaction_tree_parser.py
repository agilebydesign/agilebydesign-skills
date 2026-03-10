"""Structured parsing for interaction tree markdown. Pure stdlib — no external libraries."""
from dataclasses import dataclass
import re


@dataclass
class InteractionNode:
    """Structured node from parsed interaction tree."""
    node_type: str  # epic, story, step, scenario
    name: str
    line_no: int
    content: str
    children: list["InteractionNode"]


_SCENARIO_HEADING = re.compile(r"^#{4,6}\s+Scenario:\s*(.+)", re.IGNORECASE)


def has_ast_support() -> bool:
    return True


def parse_interaction_tree(content: str) -> list[InteractionNode]:
    """Parse markdown headings and step bullets into interaction nodes. Pure stdlib."""
    nodes: list[InteractionNode] = []
    lines = content.split("\n")
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("# ") and "Epic:" in stripped:
            nodes.append(InteractionNode("epic", stripped.split(":", 1)[-1].strip(), i, stripped, []))
        elif stripped.startswith("##") and "Epic:" in stripped:
            nodes.append(InteractionNode("epic", stripped.split(":", 1)[-1].strip(), i, stripped, []))
        elif "Story:" in stripped and stripped.startswith("#"):
            nodes.append(InteractionNode("story", stripped.split(":", 1)[-1].strip(), i, stripped, []))
        elif _SCENARIO_HEADING.match(stripped):
            nodes.append(InteractionNode("scenario", _SCENARIO_HEADING.match(stripped).group(1).strip(), i, stripped, []))
        elif stripped.startswith("- Step ") or stripped.startswith("* Step "):
            nodes.append(InteractionNode("step", stripped, i, stripped, []))
    return nodes
