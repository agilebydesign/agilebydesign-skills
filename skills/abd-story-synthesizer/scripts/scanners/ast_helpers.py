"""Optional AST/structured parsing for interaction tree. Falls back to None when unavailable (nerfed mode)."""
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_AST_AVAILABLE = False
_parse_tree: Any = None


@dataclass
class InteractionNode:
    """Structured node from parsed interaction tree."""
    node_type: str  # epic, story, step, scenario
    name: str
    line_no: int
    content: str
    children: list["InteractionNode"]


def has_ast_support() -> bool:
    return _AST_AVAILABLE


def parse_interaction_tree(content: str) -> list[InteractionNode] | None:
    """
    Parse markdown into structured interaction nodes when AST support available.
    Returns None in nerfed mode (caller uses line-by-line regex instead).
    """
    if not _AST_AVAILABLE or _parse_tree is None:
        return None
    try:
        return _parse_tree(content)
    except Exception:
        return None


# Optional: structured markdown parser (e.g. mistune, markdown-it-py)
# When available, parse headings and bullets into InteractionNode tree
try:
    import mistune
    _AST_AVAILABLE = True

    def _parse_tree(content: str) -> list[InteractionNode]:
        """Parse markdown headings/bullets into interaction nodes."""
        nodes: list[InteractionNode] = []
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("# "):
                nodes.append(InteractionNode("epic", stripped[2:].strip(), i, stripped, []))
            elif stripped.startswith("### "):
                nodes.append(InteractionNode("story", stripped[4:].strip(), i, stripped, []))
            elif stripped.startswith("- Step ") or stripped.startswith("* Step "):
                nodes.append(InteractionNode("step", stripped, i, stripped, []))
        return nodes
except ImportError:
    pass
