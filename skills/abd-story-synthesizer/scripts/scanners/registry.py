"""Scanner registry — maps rules to scanners; runs validation on markdown content."""
import re
from pathlib import Path
from .base import BaseScanner, Violation


def scanner_mode() -> str:
    """Return 'full' when grammar/AST available; 'nerfed' when regex-only."""
    grammar_ok = False
    ast_ok = False
    try:
        from .grammar import has_grammar_support
        grammar_ok = has_grammar_support()
    except ImportError:
        pass
    try:
        from .interaction_tree_parser import has_ast_support
        ast_ok = has_ast_support()
    except ImportError:
        pass
    if grammar_ok or ast_ok:
        return "full"
    return "nerfed"
from .logical_domain_scanner import LogicalDomainScanner
from .failure_modes_scanner import FailureModesScanner
from .verb_noun_scanner import VerbNounScanner
from .example_domain_match_scanner import ExampleDomainMatchScanner
from .given_state_scanner import GivenStateScanner
from .atomic_steps_scanner import AtomicStepsScanner
from .step_permutations_scanner import StepPermutationsScanner
from .consistent_steps_scanner import ConsistentStepsScanner


SCANNER_BY_NAME: dict[str, type[BaseScanner]] = {
    "logical_domain": LogicalDomainScanner,
    "failure_modes": FailureModesScanner,
    "verb_noun": VerbNounScanner,
    "example_domain_match": ExampleDomainMatchScanner,
    "given_state": GivenStateScanner,
    "atomic_steps": AtomicStepsScanner,
    "step_permutations": StepPermutationsScanner,
    "consistent_steps": ConsistentStepsScanner,
}

RULE_TO_SCANNER: dict[str, str] = {
    "domain-logical-domain-level": "logical_domain",
    "interaction-failure-modes": "failure_modes",
    "verb-noun-format": "verb_noun",
    "interaction-examples-match-domain-model": "example_domain_match",
    "interaction-given-state-not-actions": "given_state",
    "interaction-atomic-steps": "atomic_steps",
    "interaction-enumerate-step-permutations": "step_permutations",
    "interaction-consistent-steps-across-domains": "consistent_steps",
}


def _parse_rule_frontmatter(content: str) -> dict[str, str]:
    """Extract YAML frontmatter from rule markdown."""
    match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    front = match.group(1)
    result: dict[str, str] = {}
    for line in front.split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            result[k.strip().lower()] = v.strip()
    return result


def get_scanners_for_rules(rules_dir: Path) -> list[BaseScanner]:
    """Load rules from rules_dir; return scanners for rules that have a scanner."""
    scanners: list[BaseScanner] = []
    if not rules_dir.exists():
        return scanners

    for md in sorted(rules_dir.glob("*.md")):
        content = md.read_text(encoding="utf-8")
        meta = _parse_rule_frontmatter(content)
        scanner_name = meta.get("scanner", "").strip()
        rule_stem = md.stem.replace("_", "-")
        if scanner_name and scanner_name in SCANNER_BY_NAME:
            cls = SCANNER_BY_NAME[scanner_name]
            scanners.append(cls(rule_id=rule_stem))
        elif rule_stem in RULE_TO_SCANNER:
            name = RULE_TO_SCANNER[rule_stem]
            cls = SCANNER_BY_NAME[name]
            scanners.append(cls(rule_id=rule_stem))

    return scanners


def get_all_scanners() -> list[BaseScanner]:
    """Return all registered scanners (for validate command)."""
    return [cls(rule_id=rule_stem) for rule_stem, name in RULE_TO_SCANNER.items() for cls in [SCANNER_BY_NAME[name]]]


def run_scanners(
    content: str,
    source_path: str | Path | None = None,
    scanners: list[BaseScanner] | None = None,
) -> list[Violation]:
    """Run scanners on content; return all violations."""
    if scanners is None:
        scanners = get_all_scanners()
    violations: list[Violation] = []
    for s in scanners:
        violations.extend(s.scan(content, source_path))
    return violations
