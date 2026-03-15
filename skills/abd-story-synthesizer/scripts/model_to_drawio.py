#!/usr/bin/env python3
"""
Generate DrawIO class diagrams from domain-model.md.

Parses the domain model format:
  # Module: X
  ## ClassName : BaseClass
  - property : Type
  - operation() → ReturnType

And the Relationships table for edges.

Usage:
  python model_to_drawio.py <domain-model.md> [--output <file.drawio>]
"""

import argparse
import re
import sys
from pathlib import Path

# Add scripts dir for drawio_tools import
_scripts = Path(__file__).resolve().parent
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from drawio_tools import (
    load_drawio,
    save_drawio,
    create_empty_mxfile,
    get_page,
    add_page,
    find_cell_by_name,
    create_class_cell,
    create_edge,
    next_id,
    calc_cell_height,
)


# Domain model format: - name : Type or - name : Type (desc)
PROP_RE = re.compile(r"^-\s+(.+?)\s*:\s*(.+?)(?:\s*\([^)]*\))?\s*$")
# - op() → Return or - op(args) → Return
OP_RE = re.compile(r"^-\s+(.+?)\s*→\s*(.+?)\s*$")
# - op(args) or - op() without return
OP_NO_RETURN_RE = re.compile(r"^-\s+(\w+\([^)]*\))\s*$")
# ## ClassName or ## ClassName : Base
CLASS_HEADING = re.compile(r"^#+\s+(?:Module:\s*)?(.+)$")
CLASS_WITH_BASE = re.compile(r"^(.+?)\s*:\s*(.+)$")


def parse_domain_model(content: str):
    """Parse domain-model.md into modules, concepts, and relationships."""
    modules = []
    relationships = []
    lines = content.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Module: # Module: Name
        mod_match = re.match(r"^#\s+Module:\s*(.+)$", stripped, re.I)
        if mod_match:
            mod_name = mod_match.group(1).strip()
            mod = {"name": mod_name, "concepts": []}
            modules.append(mod)
            i += 1
            continue

        # Relationships table row: | From | To | Type |
        if stripped.startswith("|") and "---" not in stripped and "From" not in stripped:
            parts = [p.strip() for p in stripped.split("|") if p.strip()]
            if len(parts) >= 3:
                relationships.append({"from": parts[0], "to": parts[1], "type": parts[2]})
            i += 1
            continue

        # Class: ## ClassName or ## ClassName : Base
        class_match = re.match(r"^##\s+(.+)$", stripped)
        if class_match and not stripped.startswith("## Module"):
            raw = class_match.group(1).strip()
            base = None
            if " : " in raw:
                parts = raw.split(" : ", 1)
                name = parts[0].strip()
                base = parts[1].strip()
            else:
                name = raw

            # Skip Relationships, Aggregate root, etc.
            if name in ("Relationships", "Aggregate root") or name.startswith("**"):
                i += 1
                continue

            concept = {"name": name, "base": base, "properties": [], "operations": [], "stereotype": None}
            mod = modules[-1] if modules else None
            if mod:
                mod["concepts"].append(concept)

            i += 1
            while i < len(lines):
                ln = lines[i]
                s = ln.strip()
                # Next class or module
                if re.match(r"^#+\s+", ln) and not s.startswith("-"):
                    break
                # [foundational] or [value object]
                if s.startswith("[") and s.endswith("]"):
                    concept["stereotype"] = s[1:-1]
                    i += 1
                    continue
                # Property: - name : Type
                prop_m = PROP_RE.match(s)
                if prop_m:
                    left, right = prop_m.group(1).strip(), prop_m.group(2).strip()
                    # op() → Return has no colon before arrow in left
                    if "()" in left or "(" in left:
                        op_m = OP_RE.match(s)
                        if op_m:
                            concept["operations"].append(f"{op_m.group(1).strip()} → {op_m.group(2).strip()}")
                    else:
                        concept["properties"].append(f"{left} : {right}")
                    i += 1
                    continue
                # Operation: - op() → Return
                op_m = OP_RE.match(s)
                if op_m:
                    concept["operations"].append(f"{op_m.group(1).strip()} → {op_m.group(2).strip()}")
                    i += 1
                    continue
                # Operation without return: - op(args)
                op_no_ret = OP_NO_RETURN_RE.match(s)
                if op_no_ret:
                    concept["operations"].append(op_no_ret.group(1).strip())
                    i += 1
                    continue
                # Empty or other
                if not s or s.startswith("|") or s.startswith("---"):
                    i += 1
                    continue
                i += 1
            continue

        # Relationships table header
        if "| From" in stripped and "| To" in stripped:
            i += 1
            continue

        i += 1

    return modules, relationships


def props_ops_for_drawio(concept):
    """Convert concept to DrawIO format: + name : Type and + op() → Return."""
    props = [f"+ {p}" for p in concept["properties"]]
    ops = [f"+ {o}" for o in concept["operations"]]
    return props, ops


def _compute_tiers(modules, relationships):
    """Assign tier to each concept: 0 = base, 1 = extends tier 0, etc.
    Returns dict name -> tier."""
    name_to_tier = {}
    # Inheritance: From=parent, To=child. Child extends parent.
    child_to_parents = {}
    for rel in relationships:
        if rel["type"].lower() != "inheritance":
            continue
        parent = rel["from"]
        for child in (n.strip() for n in rel["to"].split(",")):
            child_to_parents.setdefault(child, []).append(parent)

    def tier_for(name):
        if name in name_to_tier:
            return name_to_tier[name]
        parents = child_to_parents.get(name, [])
        if not parents:
            name_to_tier[name] = 0
            return 0
        parent_tiers = [tier_for(p) for p in parents if p in _all_names]
        if not parent_tiers:
            name_to_tier[name] = 0
            return 0
        name_to_tier[name] = max(parent_tiers) + 1
        return name_to_tier[name]

    _all_names = {c["name"] for m in modules for c in m["concepts"]}
    for m in modules:
        for c in m["concepts"]:
            tier_for(c["name"])
    return name_to_tier


def generate_drawio(modules, relationships, output_path):
    """Create DrawIO file with one page containing all classes and edges.
    Layout: hierarchy flow (bases at top, children below), no overlaps."""
    mxfile = create_empty_mxfile()
    add_page(mxfile, "Domain Model")
    _, root = get_page(mxfile, "Domain Model")

    tiers = _compute_tiers(modules, relationships)
    # Group concepts by tier, preserve order within tier
    tier_to_concepts = {}
    for mod in modules:
        for concept in mod["concepts"]:
            t = tiers.get(concept["name"], 0)
            tier_to_concepts.setdefault(t, []).append(concept)

    name_to_id = {}
    col_width = 280
    min_row_height = 100
    cols_per_row = 5
    tier_gap = 60
    start_x, start_y = 40, 40

    bottom_y = start_y
    for tier in sorted(tier_to_concepts.keys()):
        concepts = tier_to_concepts[tier]
        y = bottom_y
        x = start_x
        row_max_h = 0
        for j, concept in enumerate(concepts):
            props, ops = props_ops_for_drawio(concept)
            h = calc_cell_height(len(props), len(ops), 0)
            row_max_h = max(row_max_h, h)
            cell = create_class_cell(
                root,
                concept["name"],
                base=concept.get("base"),
                properties=props,
                operations=ops,
                x=x,
                y=y,
            )
            name_to_id[concept["name"]] = cell.get("id")
            x += col_width
            if (j + 1) % cols_per_row == 0:
                x = start_x
                y += max(min_row_height, row_max_h) + 20
                row_max_h = 0
        bottom_y = y + max(min_row_height, row_max_h) + tier_gap

    # Add edges from Relationships table
    for rel in relationships:
        from_name, to_raw, rel_type = rel["from"], rel["to"], rel["type"].lower()
        to_names = [n.strip() for n in to_raw.split(",")]
        edge_type = rel_type if rel_type in ("inheritance", "composition", "aggregation", "association", "dependency") else "association"

        for to_name in to_names:
            if from_name not in name_to_id or to_name not in name_to_id:
                continue
            src_cell = find_cell_by_name(root, from_name)
            tgt_cell = find_cell_by_name(root, to_name)
            if src_cell is None or tgt_cell is None:
                continue
            # Inheritance: UML arrow child->parent. Table has From=parent, To=child.
            if edge_type == "inheritance":
                src_id, tgt_id = tgt_cell.get("id"), src_cell.get("id")
            else:
                src_id, tgt_id = src_cell.get("id"), tgt_cell.get("id")
            try:
                create_edge(root, src_id, tgt_id, edge_type)
            except ValueError:
                pass

    save_drawio(output_path, mxfile)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate DrawIO from domain-model.md")
    parser.add_argument("model", type=Path, help="Path to domain-model.md")
    parser.add_argument("--output", "-o", type=Path, default=None, help="Output .drawio path")
    args = parser.parse_args()

    model_path = args.model.resolve()
    if not model_path.exists():
        print(f"Error: {model_path} not found", file=sys.stderr)
        sys.exit(1)

    output_path = args.output or model_path.parent / "domain-class-diagram.drawio"
    output_path = output_path.resolve()

    content = model_path.read_text(encoding="utf-8")
    modules, relationships = parse_domain_model(content)

    total_concepts = sum(len(m["concepts"]) for m in modules)
    print(f"Parsed {len(modules)} modules, {total_concepts} classes, {len(relationships)} relationships")

    generate_drawio(modules, relationships, output_path)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
