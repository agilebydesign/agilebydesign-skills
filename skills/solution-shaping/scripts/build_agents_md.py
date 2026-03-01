#!/usr/bin/env python3
"""
Build AGENTS.md from rules and content.
Run from the solution-shaping skill directory or its parent.
"""
from pathlib import Path
import re


def find_skill_dir() -> Path:
    """Find the solution-shaping skill directory."""
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    if (skill_dir / "rules").exists() and (skill_dir / "content").exists():
        return skill_dir
    raise RuntimeError(f"Cannot find skill dir; script at {script_dir}")


def parse_sections(sections_path: Path) -> list[tuple[str, str]]:
    """Parse _sections.md for (prefix, title) in order."""
    text = sections_path.read_text(encoding="utf-8")
    pattern = r"## \d+\. .+? \((.+?)\)"
    matches = re.findall(pattern, text)
    return [(m, m) for m in matches]


def collect_rules(skill_dir: Path, sections: list[tuple[str, str]]) -> list[Path]:
    """Collect rule files in section order, excluding _template and _sections."""
    rules_dir = skill_dir / "rules"
    if not rules_dir.exists():
        return []

    exclude = {"_template.md", "_sections.md"}
    rule_files: list[Path] = []

    for prefix, _ in sections:
        for f in sorted(rules_dir.glob(f"{prefix}-*.md")):
            if f.name not in exclude:
                rule_files.append(f)

    # Include any rule not matched by sections (e.g. orphaned)
    for f in sorted(rules_dir.glob("*.md")):
        if f.name not in exclude and f not in rule_files:
            rule_files.append(f)

    return rule_files


def strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter from markdown."""
    if content.strip().startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip()
    return content


def main() -> None:
    skill_dir = find_skill_dir()
    content_dir = skill_dir / "content"
    output_path = skill_dir / "AGENTS.md"

    parts: list[str] = []

    # 1. Intro and core definitions
    for name in ["intro.md", "core-definitions.md"]:
        path = content_dir / name
        if path.exists():
            parts.append(path.read_text(encoding="utf-8").strip())
            parts.append("\n\n---\n\n")

    # 2. Rules section header + rules
    parts.append("# Rules\n\n")
    parts.append("Each rule has a DO with example and a DO NOT with example.\n\n---\n\n")
    sections_path = skill_dir / "rules" / "_sections.md"
    sections = parse_sections(sections_path) if sections_path.exists() else []
    rule_files = collect_rules(skill_dir, sections)

    for rule_path in rule_files:
        content = rule_path.read_text(encoding="utf-8")
        content = strip_frontmatter(content)
        parts.append(content.strip())
        parts.append("\n\n---\n\n")

    # 3. Output structure, validation, shaping process
    for name in ["output-structure.md", "validation.md", "shaping-process.md"]:
        path = content_dir / name
        if path.exists():
            parts.append(path.read_text(encoding="utf-8").strip())
            parts.append("\n\n---\n\n")

    output_path.write_text("".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
