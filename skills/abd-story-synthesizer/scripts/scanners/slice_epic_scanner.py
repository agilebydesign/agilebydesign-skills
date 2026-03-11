"""Scanner for slice-epic anti-pattern. Regex-only (nerfed mode).
Detects when slices map 1:1 to epics (horizontal slicing) instead of
cutting across epics vertically (build + use end-to-end).

Operates on session files (*-session.md). Extracts epic names from the
Interactions scaffold (§6) and slice scopes from the Slices table (§8).
Flags when:
  - A slice scope string-matches a single epic name
  - The majority of slices map 1:1 to epics
"""
import re
from pathlib import Path
from .base import BaseScanner, Violation

EPIC_HEADING = re.compile(r"^#{1,6}\s+(?:Sub-)?[Ee]pic:\s*(.+)", re.MULTILINE)
SLICE_TABLE_ROW = re.compile(
    r"^\|\s*\d+\s*\|([^|]+)\|([^|]+)\|", re.MULTILINE
)


def _normalize(text: str) -> str:
    """Lowercase, strip markdown bold, collapse whitespace."""
    text = re.sub(r"\*\*", "", text)
    return " ".join(text.lower().split())


class SliceEpicScanner(BaseScanner):
    """Flags session files where slices map 1:1 to epics."""

    rule_id = "session-slice-not-epic-by-epic"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"

        epic_names_raw = EPIC_HEADING.findall(content)
        epic_names = set()
        for raw in epic_names_raw:
            clean = raw.split("(")[0].strip()
            epic_names.add(_normalize(clean))

        if not epic_names:
            return violations

        slice_rows = SLICE_TABLE_ROW.findall(content)
        if not slice_rows:
            return violations

        matched_count = 0
        for slice_name_raw, slice_scope_raw in slice_rows:
            slice_name = _normalize(slice_name_raw)
            slice_scope = _normalize(slice_scope_raw)
            combined = slice_name + " " + slice_scope

            for epic in epic_names:
                epic_words = set(epic.split()) - {"epic:"}
                if not epic_words:
                    continue

                scope_words = set(combined.split())
                overlap = epic_words & scope_words
                if len(overlap) >= len(epic_words) * 0.7:
                    epic_refs_in_scope = sum(
                        1 for e in epic_names
                        if any(w in combined for w in set(e.split()) - {"epic:"} if len(w) > 3)
                    )
                    if epic_refs_in_scope <= 1:
                        line_num = _find_line(content, slice_name_raw.strip())
                        violations.append(Violation(
                            rule_id=self.rule_id,
                            message=f"Slice '{slice_name_raw.strip()}' maps to single epic '{raw_epic_for(epic, epic_names_raw)}' — slices should cut across epics (build + use end-to-end)",
                            location=f"{source}:{line_num}",
                            severity="warning",
                            snippet=f"Slice: {slice_name_raw.strip()} | Scope: {slice_scope_raw.strip()}"[:100],
                        ))
                        matched_count += 1
                        break

        if matched_count > 0 and len(slice_rows) > 0:
            ratio = matched_count / len(slice_rows)
            if ratio >= 0.5:
                violations.insert(0, Violation(
                    rule_id=self.rule_id,
                    message=f"{matched_count}/{len(slice_rows)} slices map 1:1 to epics — this is horizontal (epic-by-epic) slicing. Restructure to vertical slices that build AND use across epics.",
                    location=source,
                    severity="error",
                    snippet=f"{matched_count} of {len(slice_rows)} slices match a single epic",
                ))

        return violations


def raw_epic_for(normalized: str, raw_list: list[str]) -> str:
    for raw in raw_list:
        if _normalize(raw.split("(")[0].strip()) == normalized:
            return raw.split("(")[0].strip()
    return normalized


def _find_line(content: str, needle: str) -> int:
    for i, line in enumerate(content.split("\n"), 1):
        if needle in line:
            return i
    return 0
