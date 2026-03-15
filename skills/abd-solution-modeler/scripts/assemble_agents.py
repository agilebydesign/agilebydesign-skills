#!/usr/bin/env python3
"""Build AGENTS.md from pieces. Assembles pieces/*.md in order."""
import json
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent
_PIECES_DIR = _SKILL_DIR / "pieces"
_CONTENT_ORDER = [
    "introduction.md",
    "process.md",
    "output_formats.md",
    "context_prep.md",
    "scripts.md",
]


def build_agents(skill_path: Path | None = None) -> Path:
    """Assemble pieces into AGENTS.md. Returns output path."""
    skill_path = skill_path or _SKILL_DIR
    skill_path = skill_path.resolve()
    content_dir = skill_path / "pieces"
    output_path = skill_path / "AGENTS.md"

    content_order = _CONTENT_ORDER
    config_path = skill_path / "conf" / "abd-config.json"
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
            if "content_order" in data:
                content_order = data["content_order"]
        except (json.JSONDecodeError, KeyError):
            pass

    parts: list[str] = []
    for fname in content_order:
        p = content_dir / fname
        if p.exists():
            parts.append(p.read_text(encoding="utf-8").strip())
            parts.append("\n\n---\n\n")

    text = "".join(parts).rstrip()
    if text.endswith("\n\n---"):
        text = text[:-4]
    output_path.write_text(text + "\n", encoding="utf-8")
    return output_path


if __name__ == "__main__":
    out = build_agents()
    print(f"Wrote {out}")
