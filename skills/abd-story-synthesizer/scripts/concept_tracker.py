#!/usr/bin/env python3
"""Pre-scan context at chunk/paragraph granularity, extract terms, build cross-references.

Domain-agnostic: no hardcoded terms. Use `seed` to populate a glossary from a domain
model, wordlist, or any text file. The script extracts capitalized terms automatically
and optionally matches against the glossary for lowercase/domain-specific terms.

Operations:
    scan    Scan context path, extract terms per unit, write terms_report.json
    report  Print markdown summary of cross-cutting candidates from terms_report.json
    seed    Create/update glossary.json from a domain model or wordlist file
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

_STOP_WORDS = frozenset(
    "The This That These Those Which What Where When How Who Why And But Or Nor For Yet So "
    "With From Into Through During Before After Above Below Between Under Over Again Further "
    "Then Once Here There All Each Every Both Few More Most Other Some Such No Not Only Own "
    "Same Than Too Very Can Will Just Don Should Now Also Back Even Still New Old Good Great "
    "High Long Big Small First Last Next Our Its Her His Their Your Our Any Many Much May "
    "Chapter Section Part Table Figure Note See Page Roll Per Must "
    "You Your Yours If It Its In On At By To Of As Is Are Was Were Be Been Being "
    "Do Does Did Have Has Had Having Get Gets Got Would Could Shall "
    "They Them Their Theirs He Him She We Us Me My Mine "
    "An Up Out About No Yes One Two Three Four Five Six Seven Eight Nine Ten "
    "Source File Type Use Used Using Make Makes Made Take Takes Taken Give Given "
    "Like Well Also However Instead Either Neither Nor Whether Because Since While "
    "Before During Without Within Along Across Against Among Between Upon Toward "
    "Some Any Most Several Another Certain Enough Least Less Fewer "
    "Already Always Often Never Sometimes Usually Particularly Especially "
    "Example Examples Include Includes Including Particularly Specific Specifically "
    "Simply Normally Typically Generally Essentially Effectively Primarily "
    "Able Unable Necessary Possible Impossible Available".split()
)

_UNIT_SPLIT_PARAGRAPHS = 3


def _extract_terms_from_text(text: str, glossary: set[str] | None = None) -> list[str]:
    """Extract candidate domain terms from text."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    terms = []

    cap_pattern = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b")
    for m in cap_pattern.finditer(text):
        term = m.group(1)
        words = term.split()
        if len(words) == 1 and words[0] in _STOP_WORDS:
            continue
        if all(w in _STOP_WORDS for w in words):
            continue
        terms.append(term)

    bold_pattern = re.compile(r"\*\*([A-Za-z][A-Za-z ]*?)\*\*")
    for m in bold_pattern.finditer(text):
        term = m.group(1).strip()
        if term and term not in _STOP_WORDS:
            terms.append(term)

    if glossary:
        text_lower = text.lower()
        for g in glossary:
            if g.lower() in text_lower:
                terms.append(g)

    return list(set(terms))


def _load_glossary(glossary_path: Path) -> set[str]:
    if not glossary_path.exists():
        return set()
    data = json.loads(glossary_path.read_text(encoding="utf-8"))
    return set(data.get("terms", []))


def _read_units(context_path: Path) -> list[dict]:
    """Read context into units. Chunked = one file per unit. Large single files = paragraph blocks."""
    units = []
    files = sorted(context_path.rglob("*"))
    md_files = [f for f in files if f.is_file() and f.suffix in (".md", ".txt", ".json")]

    if not md_files:
        return units

    avg_size = sum(f.stat().st_size for f in md_files) / len(md_files)
    is_chunked = len(md_files) > 10 and avg_size < 50_000

    if is_chunked:
        for f in md_files:
            text = f.read_text(encoding="utf-8", errors="replace")
            units.append({
                "id": f.stem,
                "path": str(f.relative_to(context_path)),
                "text": text,
            })
    else:
        for f in md_files:
            text = f.read_text(encoding="utf-8", errors="replace")
            paragraphs = re.split(r"\n\s*\n", text)
            for i in range(0, len(paragraphs), _UNIT_SPLIT_PARAGRAPHS):
                block = paragraphs[i : i + _UNIT_SPLIT_PARAGRAPHS]
                block_text = "\n\n".join(block)
                if len(block_text.strip()) < 20:
                    continue
                unit_id = f"{f.stem}__p{i // _UNIT_SPLIT_PARAGRAPHS}"
                units.append({
                    "id": unit_id,
                    "path": f"{f.relative_to(context_path)}:p{i}-{i + len(block) - 1}",
                    "text": block_text,
                })

    return units


def cmd_scan(args):
    context_path = Path(args.context_path).resolve()
    if not context_path.exists():
        print(f"ERROR: context path does not exist: {context_path}", file=sys.stderr)
        sys.exit(1)

    synth_dir = context_path.parent / "story-synthesizer"
    if synth_dir.exists():
        default_output = synth_dir / "context_analysis.json"
        default_glossary = synth_dir / "glossary.json"
    else:
        default_output = context_path.parent / "context_analysis.json"
        default_glossary = context_path.parent / "glossary.json"
    output_path = Path(args.output) if args.output else default_output
    glossary_path = Path(args.glossary) if args.glossary else default_glossary
    glossary = _load_glossary(glossary_path)

    units = _read_units(context_path)
    if not units:
        print("No context files found.", file=sys.stderr)
        sys.exit(1)

    term_index = defaultdict(list)
    unit_records = []

    for u in units:
        terms = _extract_terms_from_text(u["text"], glossary)
        unit_records.append({"id": u["id"], "path": u["path"], "terms": sorted(set(terms))})
        for t in set(terms):
            term_index[t].append(u["id"])

    global_counts = {t: len(ids) for t, ids in term_index.items()}
    single_word_terms = {t for t in global_counts if " " not in t}
    filtered_singles = {t for t in single_word_terms if global_counts[t] < args.min_frequency}
    for t in filtered_singles:
        del term_index[t]
        del global_counts[t]
    for rec in unit_records:
        rec["terms"] = [t for t in rec["terms"] if t not in filtered_singles]

    cross_refs = sorted(global_counts.items(), key=lambda x: -x[1])

    co_occur = Counter()
    for rec in unit_records:
        terms_in_unit = rec["terms"]
        for a, b in combinations(sorted(set(terms_in_unit)), 2):
            co_occur[(a, b)] += 1
    top_co = [
        {"terms": list(pair), "count": count}
        for pair, count in co_occur.most_common(100)
        if count >= 3
    ]

    report = {
        "context_path": str(context_path),
        "total_units": len(unit_records),
        "total_terms": len(term_index),
        "glossary_terms_used": len(glossary & set(term_index.keys())),
        "units": unit_records,
        "term_index": {t: ids for t, ids in sorted(term_index.items())},
        "cross_references": [{"term": t, "unit_count": c} for t, c in cross_refs],
        "co_occurrence": top_co,
    }

    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Scan complete: {len(unit_records)} units, {len(term_index)} terms")
    print(f"Output: {output_path}")
    print(f"Top cross-cutting terms (10+ units):")
    for t, c in cross_refs[:20]:
        if c >= 10:
            print(f"  {t}: {c} units")


def cmd_report(args):
    report_path = Path(args.report_path).resolve()
    if not report_path.exists():
        print(f"ERROR: report not found: {report_path}", file=sys.stderr)
        sys.exit(1)

    report = json.loads(report_path.read_text(encoding="utf-8"))
    min_units = args.min_units

    print(f"# Concept Tracker Report")
    print(f"\n**Context:** {report['context_path']}")
    print(f"**Units scanned:** {report['total_units']}")
    print(f"**Terms extracted:** {report['total_terms']}")
    print()

    print(f"## Cross-Cutting Terms (appearing in {min_units}+ units)")
    print()
    print("| Term | Units | Distribution |")
    print("|------|-------|-------------|")

    unit_lookup = {u["id"]: u["path"] for u in report["units"]}

    for entry in report["cross_references"]:
        term = entry["term"]
        count = entry["unit_count"]
        if count < min_units:
            break
        unit_ids = report["term_index"].get(term, [])
        prefixes = set()
        for uid in unit_ids[:10]:
            path = unit_lookup.get(uid, uid)
            parts = path.split("__")
            if len(parts) > 1:
                prefixes.add(parts[0])
            else:
                prefixes.add(path.split("/")[0] if "/" in path else path[:20])
        dist = ", ".join(sorted(prefixes)[:5])
        print(f"| {term} | {count} | {dist} |")

    print()
    print("## Co-Occurring Term Clusters")
    print()
    print("Terms that frequently appear together may belong to the same foundational model.")
    print()
    print("| Term A | Term B | Co-occurrences |")
    print("|--------|--------|---------------|")
    for entry in report.get("co_occurrence", [])[:30]:
        a, b = entry["terms"]
        print(f"| {a} | {b} | {entry['count']} |")

    zero_terms = [u for u in report["units"] if len(u["terms"]) == 0]
    if zero_terms:
        print()
        print(f"## Coverage Gaps ({len(zero_terms)} units with zero terms)")
        print()
        for u in zero_terms[:20]:
            print(f"- {u['id']} ({u['path']})")
        if len(zero_terms) > 20:
            print(f"- ... and {len(zero_terms) - 20} more")


def cmd_seed(args):
    source_path = Path(args.source).resolve()
    if not source_path.exists():
        print(f"ERROR: source not found: {source_path}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output) if args.output else source_path.parent / "glossary.json"

    text = source_path.read_text(encoding="utf-8", errors="replace")
    terms = set()

    bold = re.compile(r"\*\*([A-Za-z][A-Za-z ]*?)\*\*")
    for m in bold.finditer(text):
        t = m.group(1).strip()
        if t and len(t) > 1:
            terms.add(t)

    heading_concept = re.compile(r"^#+\s+(?:Module:|Concept:)?\s*(.+)", re.MULTILINE)
    for m in heading_concept.finditer(text):
        t = m.group(1).strip().rstrip(":")
        if t and len(t) > 1 and not t.startswith("#"):
            terms.add(t)

    concept_line = re.compile(r"^([A-Z][A-Za-z]+(?:\s+[A-Z][a-z]+)*)\s*$", re.MULTILINE)
    for m in concept_line.finditer(text):
        t = m.group(1).strip()
        if t and t not in _STOP_WORDS:
            terms.add(t)

    if args.extra_terms:
        for t in args.extra_terms.split(","):
            t = t.strip()
            if t:
                terms.add(t)

    existing = set()
    if output_path.exists():
        try:
            existing = set(json.loads(output_path.read_text(encoding="utf-8")).get("terms", []))
        except (json.JSONDecodeError, KeyError):
            pass

    merged = sorted(existing | terms)
    output_path.write_text(
        json.dumps({"terms": merged, "source": str(source_path)}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    new_count = len(terms - existing)
    print(f"Glossary: {len(merged)} terms ({new_count} new from {source_path.name})")
    print(f"Output: {output_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command")

    p_scan = sub.add_parser("scan", help="Scan context and extract terms")
    p_scan.add_argument("--context-path", required=True, help="Path to context directory")
    p_scan.add_argument("--output", help="Output path for terms_report.json (default: sibling of context)")
    p_scan.add_argument("--glossary", help="Path to glossary.json (default: sibling of context)")
    p_scan.add_argument("--min-frequency", type=int, default=3, help="Min unit count for single-word terms (default: 3)")

    p_report = sub.add_parser("report", help="Print markdown report from terms_report.json")
    p_report.add_argument("report_path", help="Path to terms_report.json")
    p_report.add_argument("--min-units", type=int, default=5, help="Min units for cross-cutting (default: 5)")

    p_seed = sub.add_parser("seed", help="Create/update glossary from a source file")
    p_seed.add_argument("--source", required=True, help="Source file (domain model, wordlist, any text)")
    p_seed.add_argument("--output", help="Output glossary.json path")
    p_seed.add_argument("--extra-terms", help="Comma-separated additional terms to add")

    parsed = parser.parse_args()
    if not parsed.command:
        parser.print_help()
        sys.exit(1)

    if parsed.command == "scan":
        cmd_scan(parsed)
    elif parsed.command == "report":
        cmd_report(parsed)
    elif parsed.command == "seed":
        cmd_seed(parsed)


if __name__ == "__main__":
    main()
