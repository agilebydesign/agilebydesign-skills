"""
DrawIO class diagram toolkit — core XML read/write functions.

All CLI commands use these shared functions to manipulate DrawIO files.
"""

import html
import re
import xml.etree.ElementTree as ET
from pathlib import Path


CELL_WIDTH = 260
CELL_MIN_HEIGHT = 80
LINE_HEIGHT = 16
SECTION_PAD = 8

CLASS_STYLE = (
    "verticalAlign=top;align=left;overflow=fill;"
    "fontSize=12;fontFamily=Helvetica;html=1;whiteSpace=wrap;"
)

CLASS_STYLE_IMPORT = (
    "verticalAlign=top;align=left;overflow=fill;"
    "fontSize=12;fontFamily=Helvetica;html=1;whiteSpace=wrap;"
    "dashed=1;dashPattern=8 4;strokeColor=#999999;fontColor=#666666;"
)

EDGE_ORTHOGONAL = "edgeStyle=orthogonalEdgeStyle;rounded=1;"

EDGE_STYLES = {
    "inheritance": "endArrow=block;endSize=16;endFill=0;html=1;",
    "composition": f"{EDGE_ORTHOGONAL}endArrow=none;html=1;startArrow=diamondThin;startFill=1;startSize=14;",
    "aggregation": f"{EDGE_ORTHOGONAL}endArrow=none;html=1;startArrow=diamondThin;startFill=0;startSize=14;",
    "association": f"{EDGE_ORTHOGONAL}endArrow=open;endSize=12;html=1;",
    "association-straight": "endArrow=open;endSize=12;html=1;",
    "composition-straight": "endArrow=none;html=1;startArrow=diamondThin;startFill=1;startSize=14;",
    "aggregation-straight": "endArrow=none;html=1;startArrow=diamondThin;startFill=0;startSize=14;",
    "dependency": "endArrow=open;endSize=12;dashed=1;html=1;",
    "dependency-orthogonal": f"{EDGE_ORTHOGONAL}endArrow=open;endSize=12;dashed=1;html=1;",
}


def escape(text):
    return html.escape(str(text), quote=True)


def unescape(text):
    return html.unescape(str(text))


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------

def load_drawio(path):
    """Load a DrawIO file. Returns (tree, root_element)."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    tree = ET.parse(str(path))
    return tree, tree.getroot()


def save_drawio(path, root_element):
    """Write an mxfile element tree to disk."""
    path = Path(path)
    tree = ET.ElementTree(root_element)
    ET.indent(tree, space="  ")
    tree.write(str(path), encoding="unicode", xml_declaration=False)


def create_empty_mxfile():
    """Create a new empty mxfile element."""
    return ET.fromstring('<mxfile host="drawio_tools.py"></mxfile>')


def get_page(mxfile, page_name=None):
    """Get a diagram page by name. Returns (diagram_element, root_cell_parent).
    If page_name is None, returns the first page."""
    diagrams = mxfile.findall("diagram")
    if page_name:
        for d in diagrams:
            if d.get("name") == page_name:
                model = d.find("mxGraphModel")
                root = model.find("root") if model is not None else None
                return d, root
        return None, None
    if diagrams:
        d = diagrams[0]
        model = d.find("mxGraphModel")
        root = model.find("root") if model is not None else None
        return d, root
    return None, None


def add_page(mxfile, page_name, page_width=1600, page_height=1200):
    """Add a new diagram page to the mxfile. Returns (diagram, root)."""
    diagram = ET.SubElement(mxfile, "diagram")
    diagram.set("id", f"page_{page_name.replace(' ', '_').lower()}")
    diagram.set("name", page_name)

    model = ET.SubElement(diagram, "mxGraphModel")
    model.set("dx", "1200")
    model.set("dy", "800")
    model.set("grid", "1")
    model.set("gridSize", "10")
    model.set("guides", "1")
    model.set("tooltips", "1")
    model.set("connect", "1")
    model.set("arrows", "1")
    model.set("fold", "1")
    model.set("page", "1")
    model.set("pageScale", "1")
    model.set("pageWidth", str(page_width))
    model.set("pageHeight", str(page_height))
    model.set("math", "0")
    model.set("shadow", "0")

    root = ET.SubElement(model, "root")
    cell0 = ET.SubElement(root, "mxCell")
    cell0.set("id", "0")
    cell1 = ET.SubElement(root, "mxCell")
    cell1.set("id", "1")
    cell1.set("parent", "0")

    return diagram, root


# ---------------------------------------------------------------------------
# Cell lookup
# ---------------------------------------------------------------------------

def next_id(root):
    """Find the next available integer cell id."""
    max_id = 1
    for cell in root.iter("mxCell"):
        try:
            max_id = max(max_id, int(cell.get("id", "0")))
        except ValueError:
            pass
    return max_id + 1


def _extract_class_name(value):
    """Extract class name from the HTML value of a class cell.
    The name is in the <b> tag. Stereotype (if any) is in a separate <i> tag."""
    if not value:
        return None
    match = re.search(r"<b>([^<]+)</b>", unescape(value))
    if match:
        name = match.group(1).strip()
        if " : " in name:
            name = name.split(" : ")[0].strip()
        return name
    return None


def find_cell_by_name(root, class_name):
    """Find a class mxCell by its displayed name."""
    for cell in root.findall("mxCell"):
        value = cell.get("value", "")
        extracted = _extract_class_name(value)
        if extracted == class_name:
            return cell
    return None


def find_cell_by_id(root, cell_id):
    """Find an mxCell by its id attribute."""
    for cell in root.findall("mxCell"):
        if cell.get("id") == str(cell_id):
            return cell
    return None


def get_all_classes(root):
    """Return list of (cell_id, class_name, x, y, w, h) for all class cells."""
    classes = []
    for cell in root.findall("mxCell"):
        if cell.get("vertex") != "1":
            continue
        name = _extract_class_name(cell.get("value", ""))
        if not name:
            continue
        geo = get_geometry(cell)
        if geo:
            classes.append((cell.get("id"), name, *geo))
    return classes


def get_all_edges(root):
    """Return list of (cell_id, edge_type, source_id, target_id) for all edges."""
    edges = []
    for cell in root.findall("mxCell"):
        if cell.get("edge") != "1":
            continue
        style = cell.get("style", "")
        source = cell.get("source", "")
        target = cell.get("target", "")
        edge_type = _classify_edge(style)
        edges.append((cell.get("id"), edge_type, source, target))
    return edges


def _classify_edge(style):
    """Determine edge type from style string."""
    if "endFill=0" in style and "endArrow=block" in style:
        return "inheritance"
    if "startFill=1" in style and "diamondThin" in style:
        return "composition"
    if "startFill=0" in style and "diamondThin" in style:
        return "aggregation"
    if "dashed=1" in style and "endArrow=open" in style:
        return "dependency"
    if "endArrow=open" in style:
        return "association"
    return "unknown"


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------

def get_geometry(cell):
    """Return (x, y, width, height) from a cell's mxGeometry, or None."""
    geo = cell.find("mxGeometry")
    if geo is None:
        return None
    return (
        float(geo.get("x", "0")),
        float(geo.get("y", "0")),
        float(geo.get("width", "0")),
        float(geo.get("height", "0")),
    )


def set_geometry(cell, x=None, y=None, w=None, h=None):
    """Update position and/or size on a cell's mxGeometry."""
    geo = cell.find("mxGeometry")
    if geo is None:
        geo = ET.SubElement(cell, "mxGeometry")
        geo.set("as", "geometry")
    if x is not None:
        geo.set("x", str(int(x)))
    if y is not None:
        geo.set("y", str(int(y)))
    if w is not None:
        geo.set("width", str(int(w)))
    if h is not None:
        geo.set("height", str(int(h)))


def check_overlaps(classes):
    """Return list of overlapping pairs: [(name_a, name_b), ...]."""
    overlaps = []
    for i, (_, name_a, xa, ya, wa, ha) in enumerate(classes):
        for j, (_, name_b, xb, yb, wb, hb) in enumerate(classes):
            if j <= i:
                continue
            if xa < xb + wb and xa + wa > xb and ya < yb + hb and ya + ha > yb:
                overlaps.append((name_a, name_b))
    return overlaps


# ---------------------------------------------------------------------------
# Class cell builder
# ---------------------------------------------------------------------------

def calc_cell_height(props_count, ops_count, inv_count):
    """Compute cell height from content line counts."""
    sections = 2
    if inv_count > 0:
        sections = 3
    content_lines = props_count + ops_count + inv_count
    return max(CELL_MIN_HEIGHT, 30 + content_lines * LINE_HEIGHT + sections * SECTION_PAD)


def build_class_html(name, base=None, properties=None, operations=None, invariants=None, stereotype=None):
    """Build the HTML value string for a UML class cell."""
    properties = properties or []
    operations = operations or []
    invariants = invariants or []

    base_label = f" : {escape(base)}" if base else ""
    stereotype_html = f'<i style="font-size:9px;color:#888;">{escape(stereotype)}</i><br/>' if stereotype else ""

    props_html = ""
    for p in properties:
        props_html += f"+ {escape(p)}<br/>"
    if not props_html:
        props_html = "<br/>"

    ops_html = ""
    for o in operations:
        ops_html += f"+ {escape(o)}<br/>"
    if not ops_html:
        ops_html = "<br/>"

    label = (
        f'<p style="margin:0px;margin-top:4px;text-align:center;">'
        f'{stereotype_html}'
        f'<b>{escape(name)}{base_label}</b></p>'
        f'<hr size="1"/>'
        f'<p style="margin:0px;margin-left:4px;font-size:10px;">{props_html}</p>'
        f'<hr size="1"/>'
        f'<p style="margin:0px;margin-left:4px;font-size:10px;">{ops_html}</p>'
    )

    if invariants:
        inv_html = ""
        for inv in invariants:
            short = inv[:80] + "..." if len(inv) > 80 else inv
            inv_html += f"<i>{escape(short)}</i><br/>"
        label += (
            f'<hr size="1"/>'
            f'<p style="margin:0px;margin-left:4px;font-size:9px;color:#666;">{inv_html}</p>'
        )

    return label


def parse_class_html(value):
    """Extract (name, base, properties, operations, invariants) from class cell HTML."""
    text = unescape(value)

    name = None
    base = None
    match = re.search(r"<b>([^<]+)</b>", text)
    if match:
        raw = match.group(1).strip()
        if " : " in raw:
            name, base = raw.split(" : ", 1)
            name = name.strip()
            base = base.strip()
        else:
            name = raw

    sections = re.split(r'<hr size="1"\s*/?>', text)

    properties = []
    operations = []
    invariants = []

    def extract_items(section_html):
        items = []
        for line in re.findall(r"\+\s*([^<]+)", section_html):
            line = line.strip()
            if line:
                items.append(line)
        return items

    def extract_invariants(section_html):
        items = []
        for line in re.findall(r"<i>([^<]+)</i>", section_html):
            line = line.strip()
            if line:
                items.append(line)
        return items

    if len(sections) >= 3:
        properties = extract_items(sections[1])
        operations = extract_items(sections[2])
    if len(sections) >= 4:
        invariants = extract_invariants(sections[3])

    return name, base, properties, operations, invariants


# ---------------------------------------------------------------------------
# Cell creation
# ---------------------------------------------------------------------------

def create_class_cell(root, name, base=None, properties=None, operations=None,
                      invariants=None, x=40, y=40, imported_from=None):
    """Create and append a class mxCell to root. Returns the cell element.
    If imported_from is set, the class is rendered with dashed border and the
    source module name shown as a stereotype."""
    properties = properties or []
    operations = operations or []
    invariants = invariants or []

    cell_id = str(next_id(root))
    stereotype = f"\u00ABfrom: {imported_from}\u00BB" if imported_from else None
    label = build_class_html(name, base, properties, operations, invariants, stereotype=stereotype)
    height = calc_cell_height(len(properties), len(operations), len(invariants))
    if imported_from:
        height += LINE_HEIGHT

    style = CLASS_STYLE_IMPORT if imported_from else CLASS_STYLE
    cell = ET.SubElement(root, "mxCell")
    cell.set("id", cell_id)
    cell.set("value", label)
    cell.set("style", style)
    cell.set("vertex", "1")
    cell.set("parent", "1")

    geo = ET.SubElement(cell, "mxGeometry")
    geo.set("x", str(int(x)))
    geo.set("y", str(int(y)))
    geo.set("width", str(CELL_WIDTH))
    geo.set("height", str(int(height)))
    geo.set("as", "geometry")

    return cell


def update_class_cell(cell, name=None, base=None, properties=None,
                      operations=None, invariants=None):
    """Update an existing class cell's content. Recalculates height."""
    old_name, old_base, old_props, old_ops, old_invs = parse_class_html(
        unescape(cell.get("value", ""))
    )

    new_name = name if name is not None else old_name
    new_base = base if base is not None else old_base
    new_props = properties if properties is not None else old_props
    new_ops = operations if operations is not None else old_ops
    new_invs = invariants if invariants is not None else old_invs

    label = build_class_html(new_name, new_base, new_props, new_ops, new_invs)
    cell.set("value", label)

    height = calc_cell_height(len(new_props), len(new_ops), len(new_invs))
    set_geometry(cell, h=height)


# ---------------------------------------------------------------------------
# Edge creation
# ---------------------------------------------------------------------------

def create_edge(root, source_id, target_id, edge_type, label=""):
    """Create and append an edge mxCell. Returns the cell element."""
    if edge_type not in EDGE_STYLES:
        raise ValueError(f"Unknown edge type: {edge_type}. Use: {list(EDGE_STYLES.keys())}")

    cell_id = str(next_id(root))
    cell = ET.SubElement(root, "mxCell")
    cell.set("id", cell_id)
    cell.set("value", label or "")
    cell.set("style", EDGE_STYLES[edge_type])
    cell.set("edge", "1")
    cell.set("parent", "1")
    cell.set("source", str(source_id))
    cell.set("target", str(target_id))

    geo = ET.SubElement(cell, "mxGeometry")
    geo.set("relative", "1")
    geo.set("as", "geometry")

    return cell


# ---------------------------------------------------------------------------
# Deletion
# ---------------------------------------------------------------------------

def delete_cell(root, cell):
    """Remove a cell from root."""
    root.remove(cell)


def delete_class_and_edges(root, class_name):
    """Remove a class cell and all edges connected to it."""
    cell = find_cell_by_name(root, class_name)
    if cell is None:
        return False

    cell_id = cell.get("id")
    edges_to_remove = []
    for edge in root.findall("mxCell"):
        if edge.get("edge") != "1":
            continue
        if edge.get("source") == cell_id or edge.get("target") == cell_id:
            edges_to_remove.append(edge)

    for e in edges_to_remove:
        root.remove(e)
    root.remove(cell)
    return True


def delete_edge_between(root, source_name, target_name):
    """Remove edge(s) between two named classes. Returns count removed."""
    source_cell = find_cell_by_name(root, source_name)
    target_cell = find_cell_by_name(root, target_name)
    if source_cell is None or target_cell is None:
        return 0

    source_id = source_cell.get("id")
    target_id = target_cell.get("id")

    to_remove = []
    for edge in root.findall("mxCell"):
        if edge.get("edge") != "1":
            continue
        s, t = edge.get("source", ""), edge.get("target", "")
        if (s == source_id and t == target_id) or (s == target_id and t == source_id):
            to_remove.append(edge)

    for e in to_remove:
        root.remove(e)
    return len(to_remove)


# ---------------------------------------------------------------------------
# Domain model sync (DrawIO -> markdown)
# ---------------------------------------------------------------------------

def read_classes_from_page(root):
    """Read all class data from a DrawIO page root. Returns list of concept dicts."""
    concepts = []
    for cell in root.findall("mxCell"):
        if cell.get("vertex") != "1":
            continue
        value = cell.get("value", "")
        name = _extract_class_name(value)
        if not name:
            continue
        full_name, base, props, ops, invs = parse_class_html(value)
        concepts.append({
            "name": full_name or name,
            "base": base,
            "properties": props,
            "operations": ops,
            "invariants": invs,
        })
    return concepts


def concept_to_md(concept):
    """Render a single concept dict to domain-model.md format."""
    name = concept["name"]
    base = concept.get("base")
    header = f"**{name}**" + (f" : {base}" if base else "")

    lines = [header]

    for p in concept.get("properties", []):
        lines.append(f"- {p}")

    ops = concept.get("operations", [])
    if ops:
        lines.append("- Operations:")
        for o in ops:
            lines.append(f"  - {o}")

    for inv in concept.get("invariants", []):
        lines.append(f"- Invariant: {inv}")

    return "\n".join(lines)


def parse_model_sections(md_text):
    """Parse domain-model.md into sections by foundational model name."""
    lines = md_text.split("\n")
    sections = {}
    current_name = None
    current_start = None
    preamble_lines = []
    domain_model_started = False
    concepts_lines = []
    extensions_lines = []
    in_extensions = False

    def _flush():
        if current_name:
            sections[current_name] = {
                "preamble": "\n".join(preamble_lines),
                "concepts_text": "\n".join(concepts_lines),
                "extensions_text": "\n".join(extensions_lines),
                "start": current_start,
            }

    for i, line in enumerate(lines):
        if line.startswith("## ") and not line.startswith("###"):
            _flush()
            current_name = line[3:].strip()
            current_start = i
            preamble_lines = []
            concepts_lines = []
            extensions_lines = []
            domain_model_started = False
            in_extensions = False
        elif line.strip() == "### Domain Model":
            domain_model_started = True
        elif line.strip().startswith("### Extensions"):
            in_extensions = True
        elif current_name and not domain_model_started and not in_extensions:
            preamble_lines.append(line)
        elif current_name and in_extensions:
            extensions_lines.append(line)
        elif current_name and domain_model_started and not in_extensions:
            concepts_lines.append(line)

    _flush()
    return sections


def parse_concepts_from_md(concepts_text):
    """Parse concept blocks from the concepts portion of a model section."""
    concepts = []
    current = None

    in_operations = False
    for line in concepts_text.split("\n"):
        stripped = line.strip()

        if stripped.startswith("**") and not stripped.startswith("**Rollable extensions"):
            match = re.match(r"\*\*(\w+)\*\*(?:\s*:\s*(\w+))?", stripped)
            if match:
                if current:
                    concepts.append(current)
                current = {
                    "name": match.group(1),
                    "base": match.group(2),
                    "properties": [],
                    "operations": [],
                    "invariants": [],
                }
                in_operations = False
            continue

        if current is None:
            continue

        if stripped == "- Operations:":
            in_operations = True
            continue

        if stripped.startswith("- Invariant:"):
            in_operations = False
            current["invariants"].append(stripped[len("- Invariant:"):].strip())
            continue

        if stripped.startswith("- examples:"):
            in_operations = False
            continue

        if in_operations and stripped.startswith("- "):
            current["operations"].append(stripped[2:].strip())
            continue

        if not in_operations and stripped.startswith("- ") and not stripped.startswith("- Operations"):
            prop = stripped[2:].strip()
            if prop:
                current["properties"].append(prop)
            continue

    if current:
        concepts.append(current)

    return concepts


def _diff_concept(old, new):
    """Compare two concept dicts. Returns list of diff strings, empty if identical."""
    diffs = []

    if old.get("base") != new.get("base"):
        diffs.append(f"base: {old.get('base') or '(none)'} -> {new.get('base') or '(none)'}")

    added_props = [p for p in new["properties"] if p not in old["properties"]]
    removed_props = [p for p in old["properties"] if p not in new["properties"]]
    for p in added_props:
        diffs.append(f"+ prop: {p}")
    for p in removed_props:
        diffs.append(f"- prop: {p}")

    added_ops = [o for o in new["operations"] if o not in old["operations"]]
    removed_ops = [o for o in old["operations"] if o not in new["operations"]]
    for o in added_ops:
        diffs.append(f"+ op: {o}")
    for o in removed_ops:
        diffs.append(f"- op: {o}")

    added_invs = [v for v in new["invariants"] if v not in old["invariants"]]
    removed_invs = [v for v in old["invariants"] if v not in new["invariants"]]
    for v in added_invs:
        diffs.append(f"+ inv: {v}")
    for v in removed_invs:
        diffs.append(f"- inv: {v}")

    return diffs


def sync_page_to_model(drawio_path, page_name, md_path):
    """Sync classes from a DrawIO page back to domain-model.md.
    Returns a dict describing changes: {added: [], removed: [], updated: []}.
    """
    _, mxfile = load_drawio(drawio_path)
    _, root = get_page(mxfile, page_name)
    if root is None:
        raise ValueError(f"Page '{page_name}' not found in {drawio_path}")

    diagram_concepts = read_classes_from_page(root)
    diagram_by_name = {c["name"]: c for c in diagram_concepts}

    md_text = Path(md_path).read_text(encoding="utf-8")
    sections = parse_model_sections(md_text)

    if page_name not in sections:
        raise ValueError(f"Section '{page_name}' not found in {md_path}")

    section = sections[page_name]
    md_concepts = parse_concepts_from_md(section["concepts_text"])
    md_by_name = {c["name"]: c for c in md_concepts}

    changes = {"added": [], "removed": [], "updated": []}

    for name in diagram_by_name:
        if name not in md_by_name:
            changes["added"].append({"name": name, "concept": diagram_by_name[name]})

    for name in md_by_name:
        if name not in diagram_by_name:
            changes["removed"].append({"name": name, "concept": md_by_name[name]})

    for name in diagram_by_name:
        if name in md_by_name:
            dc = diagram_by_name[name]
            mc = md_by_name[name]
            diffs = _diff_concept(mc, dc)
            if diffs:
                changes["updated"].append({"name": name, "diffs": diffs})

    new_concepts_lines = []
    for dc in diagram_concepts:
        new_concepts_lines.append("")
        new_concepts_lines.append(concept_to_md(dc))

    new_section_body = (
        section["preamble"].rstrip() + "\n\n"
        "### Domain Model\n"
        + "\n".join(new_concepts_lines) + "\n\n"
        "### Extensions\n"
        + section["extensions_text"]
    )

    lines = md_text.split("\n")
    section_start = section["start"]

    next_section_start = len(lines)
    found_current = False
    for i, line in enumerate(lines):
        if line.startswith("## ") and not line.startswith("###"):
            if found_current:
                next_section_start = i
                break
            if line[3:].strip() == page_name:
                found_current = True

    separator_line = None
    for i in range(next_section_start - 1, section_start, -1):
        if lines[i].strip() == "---":
            separator_line = i
            break

    end_line = separator_line if separator_line else next_section_start
    new_lines = lines[:section_start]
    new_lines.append(f"## {page_name}")
    new_lines.append("")
    new_lines.append(new_section_body.rstrip())
    new_lines.append("")
    new_lines.extend(lines[end_line:])

    Path(md_path).write_text("\n".join(new_lines), encoding="utf-8")
    return changes
