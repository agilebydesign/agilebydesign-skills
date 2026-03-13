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
from .hierarchy_sizing_scanner import HierarchySizingScanner
from .parent_granularity_scanner import ParentGranularityScanner
from .sequential_order_scanner import SequentialOrderScanner
from .story_granularity_scanner import StoryGranularityScanner
from .vertical_slice_scanner import VerticalSliceScanner
from .small_testable_scanner import SmallTestableScanner
from .actor_response_scanner import ActorResponseScanner
from .domain_structure_scanner import (
    DomainCompositionScanner, DomainConceptRolesScanner,
    DomainIntegrateConceptsScanner, DomainModuleMappingScanner,
)
from .domain_language_scanner import (
    DomainPropertyTypesScanner, DomainNamingScanner, DomainResourceNamingScanner,
)
from .domain_ooa_scanner import (
    DomainAtomicOpsScanner, DomainBidirectionalScanner,
    DomainCallerReceiverScanner, DomainInteractionPatternsScanner,
    DomainCodeRepresentationScanner,
)
from .domain_sync_scanner import DomainSyncScanner
from .inheritance_scanner import (
    InheritanceActorsScanner, InheritancePreConditionScanner,
    InheritanceResultingStateScanner, InheritanceTriggeringStateScanner,
    InheritanceDomainConceptsScanner, InheritanceExamplesScanner,
)
from .steps_language_scanner import (
    AndButConditionsScanner, OutcomeLanguageScanner, BackgroundSetupScanner,
)
from .slice_epic_scanner import SliceEpicScanner
from .thin_orchestration_scanner import ThinOrchestrationScanner
from .generic_resolver_scanner import GenericResolverScanner
from .decision_ownership_scanner import DecisionOwnershipScanner


SCANNER_BY_NAME: dict[str, type[BaseScanner]] = {
    "logical_domain": LogicalDomainScanner,
    "failure_modes": FailureModesScanner,
    "verb_noun": VerbNounScanner,
    "example_domain_match": ExampleDomainMatchScanner,
    "given_state": GivenStateScanner,
    "atomic_steps": AtomicStepsScanner,
    "step_permutations": StepPermutationsScanner,
    "consistent_steps": ConsistentStepsScanner,
    "hierarchy_sizing": HierarchySizingScanner,
    "parent_granularity": ParentGranularityScanner,
    "sequential_order": SequentialOrderScanner,
    "story_granularity": StoryGranularityScanner,
    "vertical_slice": VerticalSliceScanner,
    "small_testable": SmallTestableScanner,
    "actor_response": ActorResponseScanner,
    "domain_composition": DomainCompositionScanner,
    "domain_concept_roles": DomainConceptRolesScanner,
    "domain_integrate": DomainIntegrateConceptsScanner,
    "domain_module_mapping": DomainModuleMappingScanner,
    "domain_property_types": DomainPropertyTypesScanner,
    "domain_naming": DomainNamingScanner,
    "domain_resource_naming": DomainResourceNamingScanner,
    "domain_atomic_ops": DomainAtomicOpsScanner,
    "domain_bidirectional": DomainBidirectionalScanner,
    "domain_caller_receiver": DomainCallerReceiverScanner,
    "domain_interaction_patterns": DomainInteractionPatternsScanner,
    "domain_code_representation": DomainCodeRepresentationScanner,
    "domain_sync": DomainSyncScanner,
    "inheritance_actors": InheritanceActorsScanner,
    "inheritance_precondition": InheritancePreConditionScanner,
    "inheritance_resulting_state": InheritanceResultingStateScanner,
    "inheritance_triggering_state": InheritanceTriggeringStateScanner,
    "inheritance_domain_concepts": InheritanceDomainConceptsScanner,
    "inheritance_examples": InheritanceExamplesScanner,
    "and_but_conditions": AndButConditionsScanner,
    "outcome_language": OutcomeLanguageScanner,
    "background_setup": BackgroundSetupScanner,
    "slice_epic": SliceEpicScanner,
    "thin_orchestration": ThinOrchestrationScanner,
    "generic_resolver": GenericResolverScanner,
    "decision_ownership": DecisionOwnershipScanner,
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
    "interaction-approximately-4-to-9-children": "hierarchy_sizing",
    "interaction-parent-granularity": "parent_granularity",
    "interaction-sequential-order": "sequential_order",
    "interaction-story-granularity": "story_granularity",
    "interaction-ensure-vertical-slices": "vertical_slice",
    "interaction-story-small-and-testable": "small_testable",
    "interaction-supporting-actor-response": "actor_response",
    "domain-ooa-composition-structure": "domain_composition",
    "domain-ooa-concept-roles": "domain_concept_roles",
    "domain-ooa-integrate-concepts": "domain_integrate",
    "domain-ooa-module-folder-mapping": "domain_module_mapping",
    "domain-ooa-property-types": "domain_property_types",
    "domain-ooa-domain-language": "domain_naming",
    "domain-ooa-resource-concept-naming": "domain_resource_naming",
    "domain-ooa-atomic-operations": "domain_atomic_ops",
    "domain-ooa-bidirectional-relationships": "domain_bidirectional",
    "domain-ooa-caller-receiver-state": "domain_caller_receiver",
    "domain-ooa-interaction-patterns": "domain_interaction_patterns",
    "domain-ooa-code-representation": "domain_code_representation",
    "domain-synchronize-concepts": "domain_sync",
    "interaction-inheritance-actors": "inheritance_actors",
    "interaction-inheritance-pre-condition": "inheritance_precondition",
    "interaction-inheritance-resulting-state": "inheritance_resulting_state",
    "interaction-inheritance-triggering-state": "inheritance_triggering_state",
    "interaction-inheritance-domain-concepts": "inheritance_domain_concepts",
    "interaction-inheritance-examples": "inheritance_examples",
    "interaction-steps-use-and-and-but-for-conditions": "and_but_conditions",
    "interaction-outcome-oriented-language": "outcome_language",
    "interaction-examples-background-vs-scenario-setup": "background_setup",
    "session-slice-not-epic-by-epic": "slice_epic",
    "domain-ooa-thin-orchestration": "thin_orchestration",
    "domain-ooa-no-generic-resolvers": "generic_resolver",
    "domain-ooa-behavior-owns-decision": "decision_ownership",
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
