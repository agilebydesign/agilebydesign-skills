"""
RuleSet — loads markdown from content/, JSON from rules/.
Per skill: rules/*.md (Markdown), rules/scanners.json (JSON).
"""
from pathlib import Path
import json


class RuleSet:
    """Unified rule set per skill: markdown + scanner config."""

    def __init__(self, skill_path: Path):
        self.skill_path = Path(skill_path).resolve()
        self.markdown_paths: list[Path] = []
        self.scanner_rules: dict = {}
        self.merged_content: str = ""

    def load(self) -> "RuleSet":
        """Load markdown from content/, JSON from rules/."""
        content_dir = self.skill_path / "content"
        rules_dir = self.skill_path / "rules"

        content_order = [
            "shaping-core.md",
            "shaping-process.md",
            "shaping-strategy.md",
            "shaping-output.md",
            "shaping-validation.md",
        ]
        parts: list[str] = []
        for fname in content_order:
            p = content_dir / fname
            if p.exists():
                self.markdown_paths.append(p)
                parts.append(p.read_text(encoding="utf-8").strip())
                parts.append("\n\n---\n\n")

        scanners_path = rules_dir / "scanners.json"
        if scanners_path.exists():
            self.scanner_rules = json.loads(scanners_path.read_text(encoding="utf-8"))

        for md in sorted(rules_dir.glob("*.md")):
            self.markdown_paths.append(md)
            parts.append(md.read_text(encoding="utf-8").strip())
            parts.append("\n\n---\n\n")

        self.merged_content = "".join(parts).rstrip()
        return self
