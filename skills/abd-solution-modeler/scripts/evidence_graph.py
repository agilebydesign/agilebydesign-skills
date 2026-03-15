#!/usr/bin/env python3
"""Phase 4: Build evidence graph from extraction outputs.

Produces evidence_graph.json with Concept→performs→Action, Action→produces→State, etc.
"""
import argparse
import json
import sys
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent


def _load_json(path: Path) -> list | dict:
    if not path.exists():
        return [] if "terms" in str(path) or "actions" in str(path) else {}
    return json.loads(path.read_text(encoding="utf-8"))


def _build_graph(evidence_dir: Path) -> dict:
    terms = _load_json(evidence_dir / "terms.json")
    actions = _load_json(evidence_dir / "actions.json")
    decisions = _load_json(evidence_dir / "decisions.json")
    states = _load_json(evidence_dir / "states.json")
    relationships = _load_json(evidence_dir / "relationships.json")
    modifiers = _load_json(evidence_dir / "modifiers.json")

    if not isinstance(terms, list):
        terms = []
    if not isinstance(actions, list):
        actions = []
    if not isinstance(decisions, list):
        decisions = []
    if not isinstance(states, list):
        states = []
    if not isinstance(relationships, list):
        relationships = []
    if not isinstance(modifiers, list):
        modifiers = []

    # Build graph relations: Concept → performs → Action, Action → produces → State, etc.
    performs = []
    produces = []
    modifies = []

    term_names = {t.get("name", "").lower(): t.get("term_id", "") for t in terms if isinstance(t, dict)}

    for act in actions:
        if not isinstance(act, dict):
            continue
        subj = act.get("subject", "").strip()
        verb = act.get("verb", "").strip()
        obj = act.get("object", "").strip()
        if subj and verb:
            performs.append({
                "from": subj,
                "relation": "performs",
                "to": f"{verb} {obj}"[:80],
                "action_id": act.get("action_id", ""),
            })
        if verb and obj and verb.lower() in ("produces", "creates", "adds", "applies", "modifies"):
            produces.append({
                "from": subj,
                "relation": "produces",
                "to": obj,
                "action_id": act.get("action_id", ""),
            })

    for rel in relationships:
        if not isinstance(rel, dict):
            continue
        from_ent = rel.get("from_entity", "")
        to_ent = rel.get("to_entity", "")
        if from_ent and to_ent:
            modifies.append({
                "from": from_ent,
                "relation": "modifies",
                "to": to_ent,
                "relationship_id": rel.get("relationship_id", ""),
            })

    return {
        "summary": {
            "terms": len(terms),
            "actions": len(actions),
            "decisions": len(decisions),
            "states": len(states),
            "relationships": len(relationships),
            "modifiers": len(modifiers),
        },
        "performs": performs,
        "produces": produces,
        "modifies": modifies,
        "terms": terms,
        "actions": actions,
        "decisions": decisions,
        "states": states,
        "relationships": relationships,
        "modifiers": modifiers,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 4: Build evidence graph")
    parser.add_argument("--input-dir", "-i", help="Directory with extraction outputs")
    parser.add_argument("--output", "-o", help="Output path for evidence_graph.json")
    args = parser.parse_args()

    if str(_SKILL_DIR / "scripts") not in sys.path:
        sys.path.insert(0, str(_SKILL_DIR / "scripts"))
    from _config import output_dir

    out_dir = output_dir()
    evidence_dir = Path(args.input_dir).resolve() if args.input_dir else out_dir
    output_path = Path(args.output).resolve() if args.output else out_dir / "evidence_graph.json"

    graph = _build_graph(evidence_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(graph, indent=2), encoding="utf-8")

    s = graph["summary"]
    print(f"Built evidence graph: {s['terms']} terms, {s['actions']} actions, "
          f"{len(graph['performs'])} performs, {len(graph['produces'])} produces, "
          f"{len(graph['modifies'])} modifies -> {output_path}")


if __name__ == "__main__":
    main()
