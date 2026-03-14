#!/usr/bin/env python3
"""List all rules from rules/ with order and title, sorted by order then rule_id.
   Usage: python list_rules_by_order.py [--tag TAG]  # filter to rules with TAG in tags"""
import re
import sys
from pathlib import Path

rules_dir = Path(__file__).resolve().parent.parent / "rules"
DEFAULT_ORDER = 999

def parse_frontmatter(content: str) -> dict:
    match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    result = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            result[k.strip().lower()] = v.strip()
    return result

def tags_contain(tags_val: str, tag: str) -> bool:
    """Check if tag is in tags. Handles 'a, b' or '[a, b]' format."""
    if not tags_val:
        return False
    s = tags_val.strip("[]")
    return tag.lower() in [t.strip().lower() for t in s.split(",")]

filter_tag = None
if "--tag" in sys.argv:
    i = sys.argv.index("--tag")
    if i + 1 < len(sys.argv):
        filter_tag = sys.argv[i + 1]

rows = []
for md in sorted(rules_dir.glob("*.md")):
    if md.name == "README.md":
        continue
    content = md.read_text(encoding="utf-8")
    meta = parse_frontmatter(content)
    if filter_tag and not tags_contain(meta.get("tags", ""), filter_tag):
        continue
    rule_id = md.stem
    order_raw = meta.get("order", "")
    try:
        order = int(order_raw) if order_raw else DEFAULT_ORDER
    except ValueError:
        order = DEFAULT_ORDER
    title = meta.get("title", rule_id)
    rows.append((order, rule_id, title))

rows.sort(key=lambda x: (x[0], x[1]))

print("order | rule_id | title")
print("------|---------|------")
for order, rule_id, title in rows:
    print(f"{order:5} | {rule_id} | {title[:60]}{'...' if len(title) > 60 else ''}")
