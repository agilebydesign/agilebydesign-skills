"""Scanner for verb-noun-format rule. Uses NLTK when available; falls back to regex (nerfed mode)."""
import re
from pathlib import Path

from .base import BaseScanner, Violation

try:
    from .grammar import has_grammar_support, get_pos_tags, is_verb, is_noun
except ImportError:
    has_grammar_support = lambda: False
    get_pos_tags = lambda t: []
    is_verb = lambda t: False
    is_noun = lambda t: False


# Common base verbs (regex-safe) - used to allow verb-noun patterns
COMMON_VERBS = {
    "add", "apply", "assign", "build", "cancel", "change", "check", "choose",
    "clear", "close", "confirm", "create", "delete", "display", "edit",
    "enter", "execute", "export", "filter", "find", "generate", "get",
    "group", "load", "make", "move", "open", "parse", "place", "process",
    "remove", "render", "save", "select", "send", "set", "show", "submit",
    "update", "validate", "view",
}

# Gerund endings
GERUND_PATTERN = re.compile(r"^\s*(\w+ing)\s+", re.IGNORECASE)

# Third-person singular (simple -s form)
THIRD_PERSON_PATTERN = re.compile(r"^\s*(\w+s)\s+", re.IGNORECASE)

# Technical terms to flag
TECHNICAL_TERMS = re.compile(
    r"\b(config|json|api|sql|xml|class|method|function|endpoint)\b",
    re.IGNORECASE,
)


class VerbNounScanner(BaseScanner):
    """Flags noun-only, gerund, third-person, and technical terms. Uses NLTK when available; regex fallback."""

    rule_id = "verb-noun-format"

    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        violations: list[Violation] = []
        source = str(source_path) if source_path else "content"
        lines = content.split("\n")
        use_grammar = has_grammar_support()

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith("|"):
                continue

            # Grammar mode: use NLTK POS for verb-noun, noun-verb, gerund, third-person
            if use_grammar:
                v = self._check_with_grammar(stripped, source, i)
                if v:
                    violations.extend(v)
            else:
                # Nerfed mode: regex-only checks
                v = self._check_with_regex(stripped, source, i)
                if v:
                    violations.extend(v)

            # Technical terms (always checked)
            if TECHNICAL_TERMS.search(stripped):
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message="Technical term in interaction text - use behavioral language",
                        location=f"{source}:{i}",
                        severity="warning",
                        snippet=stripped[:80],
                    )
                )

        return violations

    def _check_with_grammar(self, line: str, source: str, line_no: int) -> list[Violation]:
        """Use NLTK POS tagging for verb-noun, noun-verb, gerund, third-person."""
        violations: list[Violation] = []
        tags = get_pos_tags(line)
        if not tags:
            return violations

        first_tag = tags[0][1]
        first_word = tags[0][0]

        # Gerund (VBG)
        if first_tag == "VBG":
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Gerund form '{first_word}' - use base verb (e.g. Submit, Place)",
                    location=f"{source}:{line_no}",
                    severity="warning",
                    snippet=line[:80],
                )
            )

        # Third-person singular (VBZ)
        elif first_tag == "VBZ":
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Third-person singular '{first_word}' - use base verb form",
                    location=f"{source}:{line_no}",
                    severity="warning",
                    snippet=line[:80],
                )
            )

        # Noun-verb pattern (should be verb-noun)
        elif len(tags) >= 2 and is_noun(first_tag) and is_verb(tags[1][1]):
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Noun-verb pattern - use verb-noun format (e.g. 'Places Order' not 'Order places')",
                    location=f"{source}:{line_no}",
                    severity="warning",
                    snippet=line[:80],
                )
            )

        # Noun-only (no verb)
        elif len(tags) >= 1 and not any(is_verb(t[1]) for t in tags):
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message="Noun-only - use verb-noun format (e.g. 'Submit order' not 'Order submission')",
                    location=f"{source}:{line_no}",
                    severity="warning",
                    snippet=line[:80],
                )
            )

        return violations

    def _check_with_regex(self, line: str, source: str, line_no: int) -> list[Violation]:
        """Regex-only fallback (nerfed mode)."""
        violations: list[Violation] = []
        m = GERUND_PATTERN.match(line)
        if m:
            word = m.group(1).lower()
            if len(word) > 4 and word.endswith("ing"):
                base = word[:-3]
                if base + "e" in COMMON_VERBS or base in COMMON_VERBS:
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            message=f"Gerund form '{m.group(1)}' - use base verb (e.g. Submit, Place)",
                            location=f"{source}:{line_no}",
                            severity="warning",
                            snippet=line[:80],
                        )
                    )
        return violations
