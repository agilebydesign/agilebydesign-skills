"""
DrawIO class diagram CLI — composable commands for building UML class diagrams.

Usage:
    python drawio_class_cli.py <command> <file> [options]

Commands:
    init            Create empty drawio file or add a page
    inspect         List classes, edges, and overlaps
    add-class       Add a class box
    update-class    Modify properties/operations/invariants on a class
    delete-class    Remove a class and its edges
    move            Reposition a class
    add-inheritance Add inheritance edge (hollow triangle)
    add-composition Add composition edge (filled diamond)
    add-aggregation Add aggregation edge (hollow diamond)
    add-association Add association edge (open arrow)
    add-dependency  Add dependency edge (dashed arrow)
    delete-edge     Remove edge between two classes
    sync-to-model   Sync DrawIO classes back to domain-model.md
    validate        Run layout validation (overlaps, grid, hierarchy flow)
"""

import argparse
import json
import sys
from pathlib import Path

from drawio_tools import (
    load_drawio, save_drawio, create_empty_mxfile,
    get_page, add_page,
    find_cell_by_name, get_all_classes, get_all_edges, check_overlaps,
    create_class_cell, update_class_cell, parse_class_html,
    create_edge, delete_class_and_edges, delete_edge_between,
    set_geometry, get_geometry, unescape,
    sync_page_to_model,
    validate_layout,
)


def cmd_init(args):
    path = Path(args.file)
    if path.exists():
        _, mxfile = load_drawio(path)
        _, existing_root = get_page(mxfile, args.page)
        if existing_root is not None:
            print(f"Page '{args.page}' already exists in {path}")
            return
        add_page(mxfile, args.page)
        save_drawio(path, mxfile)
        print(f"Added page '{args.page}' to {path}")
    else:
        mxfile = create_empty_mxfile()
        add_page(mxfile, args.page)
        save_drawio(path, mxfile)
        print(f"Created {path} with page '{args.page}'")


def cmd_inspect(args):
    _, mxfile = load_drawio(args.file)

    pages_to_inspect = []
    if args.page:
        diagram, root = get_page(mxfile, args.page)
        if root is None:
            print(f"Page '{args.page}' not found")
            return
        pages_to_inspect.append((args.page, root))
    else:
        for d in mxfile.findall("diagram"):
            name = d.get("name", "(unnamed)")
            model = d.find("mxGraphModel")
            root = model.find("root") if model is not None else None
            if root is not None:
                pages_to_inspect.append((name, root))

    output = {}
    for page_name, root in pages_to_inspect:
        classes = get_all_classes(root)
        edges = get_all_edges(root)
        overlaps = check_overlaps(classes)

        id_to_name = {cid: name for cid, name, *_ in classes}

        page_data = {
            "classes": [
                {"name": name, "id": cid, "x": x, "y": y, "w": w, "h": h}
                for cid, name, x, y, w, h in classes
            ],
            "edges": [
                {
                    "type": etype,
                    "source": id_to_name.get(src, src),
                    "target": id_to_name.get(tgt, tgt),
                }
                for eid, etype, src, tgt in edges
            ],
            "overlaps": [list(pair) for pair in overlaps],
        }
        output[page_name] = page_data

    print(json.dumps(output, indent=2))


def cmd_validate(args):
    """Run layout validation on diagram pages. Exit 1 if any violations."""
    _, mxfile = load_drawio(args.file)

    pages_to_validate = []
    if args.page:
        diagram, root = get_page(mxfile, args.page)
        if root is None:
            print(f"Page '{args.page}' not found")
            sys.exit(1)
        pages_to_validate.append((args.page, root))
    else:
        for d in mxfile.findall("diagram"):
            name = d.get("name", "(unnamed)")
            model = d.find("mxGraphModel")
            root = model.find("root") if model is not None else None
            if root is not None:
                pages_to_validate.append((name, root))

    total_violations = 0
    for page_name, root in pages_to_validate:
        violations = validate_layout(root)
        if violations:
            for rule, msg in violations:
                print(f"[{page_name}] {rule}: {msg}")
                total_violations += 1

    if total_violations > 0:
        print(f"\n{total_violations} layout violation(s)")
        sys.exit(1)
    print("OK: no layout violations")


def _get_root_or_exit(file_path, page_name):
    _, mxfile = load_drawio(file_path)
    _, root = get_page(mxfile, page_name)
    if root is None:
        print(f"Page '{page_name}' not found in {file_path}")
        sys.exit(1)
    return mxfile, root


def cmd_add_class(args):
    mxfile, root = _get_root_or_exit(args.file, args.page)

    if find_cell_by_name(root, args.name):
        print(f"Class '{args.name}' already exists on page '{args.page}'")
        return

    props = args.props.split("|") if args.props else []
    ops = args.ops.split("|") if args.ops else []
    invs = args.invs.split("|") if args.invs else []

    x = args.x if args.x is not None else _find_open_x(root)
    y = args.y if args.y is not None else 40

    cell = create_class_cell(
        root, args.name, base=args.base,
        properties=props, operations=ops, invariants=invs,
        x=x, y=y, imported_from=args.imported_from,
    )
    save_drawio(args.file, mxfile)
    geo = get_geometry(cell)
    print(f"Added '{args.name}' at ({int(geo[0])}, {int(geo[1])}) id={cell.get('id')}")


def _find_open_x(root):
    """Find the next open X position to the right of existing classes."""
    classes = get_all_classes(root)
    if not classes:
        return 40
    max_right = max(x + w for _, _, x, _, w, _ in classes)
    return int(max_right + 60)


def cmd_update_class(args):
    mxfile, root = _get_root_or_exit(args.file, args.page)
    cell = find_cell_by_name(root, args.name)
    if cell is None:
        print(f"Class '{args.name}' not found on page '{args.page}'")
        return

    _, old_base, old_props, old_ops, old_invs = parse_class_html(
        unescape(cell.get("value", ""))
    )

    new_base = args.set_base if args.set_base else old_base
    new_props = list(old_props)
    new_ops = list(old_ops)
    new_invs = list(old_invs)

    if args.add_prop:
        new_props.append(args.add_prop)
    if args.remove_prop:
        new_props = [p for p in new_props if args.remove_prop not in p]
    if args.add_op:
        new_ops.append(args.add_op)
    if args.remove_op:
        new_ops = [o for o in new_ops if args.remove_op not in o]
    if args.add_inv:
        new_invs.append(args.add_inv)
    if args.remove_inv:
        new_invs = [v for v in new_invs if args.remove_inv not in v]

    update_class_cell(cell, base=new_base, properties=new_props,
                      operations=new_ops, invariants=new_invs)
    save_drawio(args.file, mxfile)
    print(f"Updated '{args.name}': {len(new_props)} props, {len(new_ops)} ops, {len(new_invs)} invs")


def cmd_delete_class(args):
    mxfile, root = _get_root_or_exit(args.file, args.page)
    if delete_class_and_edges(root, args.name):
        save_drawio(args.file, mxfile)
        print(f"Deleted '{args.name}' and its edges")
    else:
        print(f"Class '{args.name}' not found on page '{args.page}'")


def cmd_move(args):
    mxfile, root = _get_root_or_exit(args.file, args.page)
    cell = find_cell_by_name(root, args.name)
    if cell is None:
        print(f"Class '{args.name}' not found on page '{args.page}'")
        return
    set_geometry(cell, x=args.x, y=args.y)
    save_drawio(args.file, mxfile)
    print(f"Moved '{args.name}' to ({args.x}, {args.y})")


def _add_edge(args, edge_type):
    mxfile, root = _get_root_or_exit(args.file, args.page)

    straight = getattr(args, "straight", False)

    if edge_type == "inheritance":
        source_name = args.child
        target_name = args.parent
    elif edge_type in ("composition", "aggregation"):
        source_name = args.owner
        target_name = args.part
    else:
        source_name = getattr(args, "from")
        target_name = args.to

    source_cell = find_cell_by_name(root, source_name)
    target_cell = find_cell_by_name(root, target_name)

    if source_cell is None:
        print(f"Class '{source_name}' not found")
        return
    if target_cell is None:
        print(f"Class '{target_name}' not found")
        return

    actual_type = f"{edge_type}-straight" if straight else edge_type
    label = getattr(args, "label", "")
    create_edge(root, source_cell.get("id"), target_cell.get("id"), actual_type, label=label)
    save_drawio(args.file, mxfile)
    style_note = " (straight)" if straight else ""
    label_note = f" [{label}]" if label else ""
    print(f"Added {edge_type}{style_note}: {source_name} -> {target_name}{label_note}")


def cmd_add_inheritance(args):
    _add_edge(args, "inheritance")


def cmd_add_composition(args):
    _add_edge(args, "composition")


def cmd_add_aggregation(args):
    _add_edge(args, "aggregation")


def cmd_add_association(args):
    _add_edge(args, "association")


def cmd_add_dependency(args):
    _add_edge(args, "dependency")


def cmd_delete_edge(args):
    mxfile, root = _get_root_or_exit(args.file, args.page)
    source_name = getattr(args, "from")
    count = delete_edge_between(root, source_name, args.to)
    if count > 0:
        save_drawio(args.file, mxfile)
        print(f"Deleted {count} edge(s) between '{source_name}' and '{args.to}'")
    else:
        print(f"No edges found between '{source_name}' and '{args.to}'")


def cmd_sync_to_model(args):
    md_path = args.model or str(Path(args.file).parent / "domain-model.md")
    pages = []

    _, mxfile = load_drawio(args.file)
    if args.page:
        pages.append(args.page)
    else:
        for d in mxfile.findall("diagram"):
            pages.append(d.get("name", ""))

    for page_name in pages:
        if not page_name:
            continue
        try:
            changes = sync_page_to_model(args.file, page_name, md_path)
            total = len(changes["added"]) + len(changes["removed"]) + len(changes["updated"])
            if total == 0:
                print(f"  {page_name}: no changes")
            else:
                print(f"  {page_name}:")
                for entry in changes["added"]:
                    c = entry["concept"]
                    print(f"    + {entry['name']} (added)")
                    for p in c.get("properties", []):
                        print(f"        prop: {p}")
                    for o in c.get("operations", []):
                        print(f"        op: {o}")
                for entry in changes["removed"]:
                    print(f"    - {entry['name']} (removed)")
                for entry in changes["updated"]:
                    print(f"    ~ {entry['name']}:")
                    for diff in entry["diffs"]:
                        print(f"        {diff}")
        except ValueError as e:
            print(f"  {page_name}: skipped ({e})")


def main():
    parser = argparse.ArgumentParser(description="DrawIO class diagram tools")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="Create empty drawio or add page")
    p.add_argument("file")
    p.add_argument("--page", required=True)
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("inspect", help="List classes, edges, overlaps")
    p.add_argument("file")
    p.add_argument("--page", default=None)
    p.set_defaults(func=cmd_inspect)

    p = sub.add_parser("validate", help="Run layout validation (overlaps, grid, hierarchy)")
    p.add_argument("file")
    p.add_argument("--page", default=None)
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("add-class", help="Add a class box")
    p.add_argument("file")
    p.add_argument("--page", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--base", default=None)
    p.add_argument("--props", default=None, help="Properties separated by |")
    p.add_argument("--ops", default=None, help="Operations separated by |")
    p.add_argument("--invs", default=None, help="Invariants separated by |")
    p.add_argument("--x", type=int, default=None)
    p.add_argument("--y", type=int, default=None)
    p.add_argument("--imported-from", default=None, help="Source module (renders as dashed import)")
    p.set_defaults(func=cmd_add_class)

    p = sub.add_parser("update-class", help="Modify a class")
    p.add_argument("file")
    p.add_argument("--page", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--set-base", default=None)
    p.add_argument("--add-prop", default=None)
    p.add_argument("--remove-prop", default=None)
    p.add_argument("--add-op", default=None)
    p.add_argument("--remove-op", default=None)
    p.add_argument("--add-inv", default=None)
    p.add_argument("--remove-inv", default=None)
    p.set_defaults(func=cmd_update_class)

    p = sub.add_parser("delete-class", help="Remove class and edges")
    p.add_argument("file")
    p.add_argument("--page", required=True)
    p.add_argument("--name", required=True)
    p.set_defaults(func=cmd_delete_class)

    p = sub.add_parser("move", help="Reposition a class")
    p.add_argument("file")
    p.add_argument("--page", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--x", type=int, required=True)
    p.add_argument("--y", type=int, required=True)
    p.set_defaults(func=cmd_move)

    p = sub.add_parser("add-inheritance", help="Add inheritance edge")
    p.add_argument("file")
    p.add_argument("--page", required=True)
    p.add_argument("--child", required=True)
    p.add_argument("--parent", required=True)
    p.set_defaults(func=cmd_add_inheritance)

    p = sub.add_parser("add-composition", help="Add composition edge")
    p.add_argument("file")
    p.add_argument("--page", required=True)
    p.add_argument("--owner", required=True)
    p.add_argument("--part", required=True)
    p.add_argument("--straight", action="store_true", help="Straight line instead of orthogonal")
    p.set_defaults(func=cmd_add_composition)

    p = sub.add_parser("add-aggregation", help="Add aggregation edge")
    p.add_argument("file")
    p.add_argument("--page", required=True)
    p.add_argument("--owner", required=True)
    p.add_argument("--part", required=True)
    p.add_argument("--straight", action="store_true", help="Straight line instead of orthogonal")
    p.set_defaults(func=cmd_add_aggregation)

    p = sub.add_parser("add-association", help="Add association edge")
    p.add_argument("file")
    p.add_argument("--page", required=True)
    p.add_argument("--from", required=True)
    p.add_argument("--to", required=True)
    p.add_argument("--straight", action="store_true", help="Straight line instead of orthogonal")
    p.set_defaults(func=cmd_add_association)

    p = sub.add_parser("add-dependency", help="Add dependency edge (dashed arrow)")
    p.add_argument("file")
    p.add_argument("--page", required=True)
    p.add_argument("--from", required=True)
    p.add_argument("--to", required=True)
    p.add_argument("--label", default="", help="Label on the edge")
    p.set_defaults(func=cmd_add_dependency)

    p = sub.add_parser("delete-edge", help="Remove edge between classes")
    p.add_argument("file")
    p.add_argument("--page", required=True)
    p.add_argument("--from", required=True)
    p.add_argument("--to", required=True)
    p.set_defaults(func=cmd_delete_edge)

    p = sub.add_parser("sync-to-model", help="Sync DrawIO classes back to domain-model.md")
    p.add_argument("file")
    p.add_argument("--page", default=None, help="Sync one page (default: all pages)")
    p.add_argument("--model", default=None, help="Path to domain-model.md")
    p.set_defaults(func=cmd_sync_to_model)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
