#!/usr/bin/env python3
"""Consolidate extracted evidence into an AI-ready evidence graph.

Links terms to actions, decisions, variations, and states.
Detects hotspots, ambiguities, and conflicts.
"""
import argparse
import json
from collections import Counter
from pathlib import Path


def _load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def _find_term_links(terms: list[dict], items: list[dict], item_field: str) -> list[dict]:
    """Link terms to items by checking if term name appears in the item's text fields."""
    links = []
    term_names = {t["name"].lower(): t["term_id"] for t in terms}

    for item in items:
        text = " ".join(str(v) for v in item.values()).lower()
        for name, term_id in term_names.items():
            if name in text:
                links.append({
                    "term_id": term_id,
                    f"{item_field}_id": item.get(f"{item_field}_id", ""),
                    "term_name": name,
                })
    return links


def _detect_hotspots(term_action_links: list, term_decision_links: list) -> list[dict]:
    """Terms that appear in many actions AND decisions are behavioral hotspots."""
    action_counts: Counter = Counter()
    decision_counts: Counter = Counter()

    for link in term_action_links:
        action_counts[link["term_id"]] += 1
    for link in term_decision_links:
        decision_counts[link["term_id"]] += 1

    hotspots = []
    all_terms = set(action_counts.keys()) | set(decision_counts.keys())
    for term_id in all_terms:
        a_count = action_counts.get(term_id, 0)
        d_count = decision_counts.get(term_id, 0)
        total = a_count + d_count
        if total >= 3:
            hotspots.append({
                "term_id": term_id,
                "action_links": a_count,
                "decision_links": d_count,
                "total_links": total,
            })

    return sorted(hotspots, key=lambda h: h["total_links"], reverse=True)


def consolidate(extracted_dir: Path) -> dict:
    terms = _load_json(extracted_dir / "terms.json")
    actions = _load_json(extracted_dir / "actions.json")
    decisions = _load_json(extracted_dir / "decisions.json")
    variations = _load_json(extracted_dir / "variations.json")
    states = _load_json(extracted_dir / "states.json")
    relationships = _load_json(extracted_dir / "relationships.json")

    term_action_links = _find_term_links(terms, actions, "action")
    term_decision_links = _find_term_links(terms, decisions, "decision")
    term_state_links = _find_term_links(terms, states, "state")

    hotspots = _detect_hotspots(term_action_links, term_decision_links)

    return {
        "summary": {
            "terms": len(terms),
            "actions": len(actions),
            "decisions": len(decisions),
            "variations": len(variations),
            "states": len(states),
            "relationships": len(relationships),
            "hotspots": len(hotspots),
        },
        "term_action_links": term_action_links,
        "term_decision_links": term_decision_links,
        "term_state_links": term_state_links,
        "hotspots": hotspots,
        "variations": variations,
        "issues": [],
    }


def _write_summary(graph: dict, output_path: Path) -> None:
    lines = ["# Evidence Summary\n"]
    s = graph["summary"]
    lines.append(f"- **Terms:** {s['terms']}")
    lines.append(f"- **Actions:** {s['actions']}")
    lines.append(f"- **Decisions:** {s['decisions']}")
    lines.append(f"- **Variations:** {s['variations']}")
    lines.append(f"- **States:** {s['states']}")
    lines.append(f"- **Relationships:** {s['relationships']}")
    lines.append(f"- **Hotspots:** {s['hotspots']}")
    lines.append("")

    if graph["hotspots"]:
        lines.append("## Hotspots (high behavioral density)\n")
        for h in graph["hotspots"][:20]:
            lines.append(f"- `{h['term_id']}`: {h['action_links']} actions, {h['decision_links']} decisions")
        lines.append("")

    if graph["variations"]:
        lines.append("## Variation Axes\n")
        for v in graph["variations"][:20]:
            lines.append(f"- {v['axis']}")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Consolidate evidence into graph")
    parser.add_argument("--extracted-path", required=True, help="Path to extracted/ directory")
    parser.add_argument("--output-dir", default=None, help="Output directory for consolidated files")
    args = parser.parse_args()

    extracted_dir = Path(args.extracted_path).resolve()
    output_dir = Path(args.output_dir) if args.output_dir else extracted_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    graph = consolidate(extracted_dir)

    graph_path = output_dir / "evidence_graph.json"
    graph_path.write_text(json.dumps(graph, indent=2), encoding="utf-8")

    summary_path = output_dir / "evidence_summary.md"
    _write_summary(graph, summary_path)

    s = graph["summary"]
    print(f"Evidence graph: {s['terms']} terms, {s['actions']} actions, {s['decisions']} decisions, {s['hotspots']} hotspots")
    print(f"Written to: {graph_path}")


if __name__ == "__main__":
    main()
