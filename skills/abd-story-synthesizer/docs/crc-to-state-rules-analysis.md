# CRC Domain Rules → State Domain Rules Analysis

**Purpose:** Identify which CRC bot domain rules should become state domain rules in the story synthesizer, check overlap with existing OOAD rules, and recommend merges. All rules must be adapted to **State Model format** (Properties, Operations, Module) — not CRC (responsibilities, collaborators) or JSON.

---

## CRC Rules Inventory

| CRC Rule | Priority | Core idea |
|----------|----------|-----------|
| use_resource_oriented_design | 7 | Concepts = resources with properties/behaviors; nouns not verbs; encapsulation |
| favor_atomic_responsibilities | 6 | One responsibility = one behavior; noun phrases for properties, verb phrases for behaviors |
| map_bidirectional_collaborators | 4 | When A references B, B should reference A (unless primitive) |
| use_domain_language | 2 | Domain language from stories; avoid Hold/Get/Has; no primitive soup |
| use_natural_english | 6 | Natural English for names; no abbreviations |
| integrate_and_organize_concepts | 1 | Nest related capabilities under parent; avoid noun redundancy |
| favor_code_representation | 3 | Class names, typed collaborators; no prose |
| scope_concepts_correctly | 3 | Local vs global; complete functional units |
| use_module_for_folder_structure | 1 | Module = folder path (dot notation) |
| shape_relationships_from_story_map | 11 | Derive collaborators from stories; don't invent |

---

## Existing Synthesizer State/OOAD Rules

| Rule | Covers |
|------|--------|
| state-ooa-caller-receiver-state | Caller/receiver mapping; state before/after |
| state-ooa-concept-roles | Wirfs-Brock roles (optional) |
| state-ooa-property-types | String, Number, Boolean, List, Dictionary, UniqueID, Instant |
| state-ooa-composition-structure | Composition vs aggregation |
| state-ooa-interaction-patterns | Producer-Consumer, Client-Server, Coordinator |
| interactions-inheritance-domain-concepts | Scope; State Model format; placement |
| state-synchronize-concepts | Keep tree and model in sync |
| state-logical-domain-level | Logical/domain level; no implementation details |

---

## Overlap and Merge Analysis

### 1. scope_concepts_correctly — **ALREADY COVERED**

**Overlap:** `interactions-inheritance-domain-concepts.md` already states:
- Place at most specific level; local vs shared
- Elevate to parent when shared; keep local when single sub-epic
- Complete functional units, not fragments

**Action:** No new rule. Optionally strengthen the existing rule with CRC examples (e.g. don't fragment TradeData + TradeCalculator).

---

### 2. shape_relationships_from_story_map — **STRENGTHEN EXISTING**

**Overlap:** `state-synchronize-concepts.md` says derive concepts from interactions. Strategy and core.md emphasize grounding in domain.

**Action:** Add one DO to `state-synchronize-concepts.md` or `interactions-inheritance-domain-concepts.md`:
- **DO** derive Properties and Operations from interactions/stories; do not invent collaborators or relationships not present in source material.

---

### 3. use_module_for_folder_structure — **OPTIONAL ADD-ON**

**Overlap:** None. Module exists in State Model (core.md) but no rule governs it.

**Action:** Add short rule `state-ooa-module-folder-mapping.md` (optional, when mapping to code):
- **DO** when mapping to code, use Module = folder path in dot notation (e.g. `actions.render`).
- **DO NOT** use `src/` prefix or slashes.

**Note:** Synthesizer may run before code exists — rule is "when applicable."

---

### 4. use_resource_oriented_design — **ADAPT → NEW RULE**

**Overlap:** Partially with state-ooa-concept-roles (nouns). No direct overlap with property-types or composition.

**Adapt to State Model:**
- Concepts = resources with Properties and Operations (not "responsibilities")
- Concept names = nouns (Order, Portfolio), not verbs (OrderManager, InstructionPreparer)
- Properties hold state; Operations perform behaviors
- Encapsulation: don't pass another concept's data to it as parameters
- No Manager/Service/Handler suffixes
- No anemic concepts (only Properties, no Operations)

**Action:** Create `state-ooa-resource-concept-naming.md`:
- **DO** name concepts as nouns (resources).
- **DO** give concepts both Properties and Operations where behavior exists.
- **DO NOT** use Manager/Service/Handler/Preparer/Builder suffixes.
- **DO NOT** create concepts that are only data carriers with no Operations.
- **DO NOT** pass another concept's data to it — concepts own their data.

---

### 5. favor_atomic_responsibilities → **state-ooa-atomic-operations**

**Overlap:** None. State rules don't address atomicity.

**Adapt to State Model:**
- One Operation = one behavior (not "one responsibility")
- Describe what the concept does (verbs), not outcomes (Prevents, Issues)
- Properties = state access; Operations = behaviors

**Action:** Create `state-ooa-atomic-operations.md`:
- **DO** keep Operations atomic: one Operation = one behavior.
- **DO** describe behavior (Acquires, Releases, Calculates), not outcome (Prevents, Issues).
- **DO NOT** pack multiple conditions into one Operation (e.g. "Releases on unlock, redemption complete, or timeout" → split).

---

### 6. map_bidirectional_collaborators — **NEW RULE**

**Overlap:** None. Composition-structure covers has-a; not bidirectional references.

**Adapt to State Model:**
- When Concept A has a Property or Operation that references B (non-primitive), B should have a corresponding reference to A
- Primitives (String, Number, Boolean, etc.) excepted

**Action:** Create `state-ooa-bidirectional-relationships.md`:
- **DO** when A references B (Property or Operation collaborator), B should reference A — same relationship, both perspectives.
- **DO NOT** require bidirectional mapping for primitives (String, Number, Boolean, etc.).

---

### 7. use_domain_language + use_natural_english — **MERGE → state-ooa-domain-language**

**Overlap:** state-logical-domain-level (domain level); state-ooa-property-types (avoid primitive soup).

**Adapt to State Model:**
- Use domain language mined from stories
- Avoid Hold, Get, Has as defaults — find domain verbs
- Use standard types for Properties; prefer domain concepts over primitive soup
- Natural English for Operation names; no abbreviations

**Action:** Create `state-ooa-domain-language.md`:
- **DO** use domain language from stories and acceptance criteria.
- **DO** use standard types (String, Number, Boolean, etc.) for Properties; prefer domain concepts over scattering primitives.
- **DO** write Operation names in natural English (Calculates total, Validates inventory).
- **DO NOT** use Hold, Get, Has as defaults — find domain-specific verbs.
- **DO NOT** use Manager, Service, Handler, Factory suffixes.
- **DO NOT** use abbreviations or technical jargon when simple English works.

---

### 8. integrate_and_organize_concepts — **NEW RULE**

**Overlap:** Partially with scope (complete units). Different focus: integration vs placement.

**Adapt to State Model:**
- Nest related capabilities under a single concept instead of fragmenting (Walk Animation, Run Animation → Character Animation)
- Group by business domain, not technical layers (Data Layer, Business Logic)
- Avoid noun redundancy

**Action:** Create `state-ooa-integrate-concepts.md`:
- **DO** integrate related capabilities under a parent concept (e.g. Character Animation with multiple Operations).
- **DO** group concepts by business domain.
- **DO NOT** create separate concepts with the same noun when they should be one (PortfolioValue, PortfolioRisk, PortfolioAllocation → Portfolio).
- **DO NOT** group by technical layers (Data Layer, Business Logic Layer).

---

### 9. favor_code_representation — **SEPARATE RULE** (do not merge with resource-concept-naming)

**Overlap:** Related to use_resource_oriented_design (both touch naming) but distinct concern: code alignment vs domain modeling.

**Adapt to State Model:**
- Use concise concept names (class-like)
- Use typed Properties and Operations
- No long prose for concept names or types

**Action:** Create `state-ooa-code-representation.md`:
- **DO** use concise concept names that could exist as types.
- **DO** use typed Properties and Operations (actual type names, not prose descriptions).
- **DO NOT** use long prose sentences as concept names.
- **DO NOT** use prose descriptions for Property/Operation types — use actual type names.

---

## Summary: New Rules to Create

| New Rule | Source CRC | Content |
|----------|------------|---------|
| **state-ooa-resource-concept-naming.md** | use_resource_oriented_design | Nouns; no Manager/Service; no anemic; encapsulation |
| **state-ooa-code-representation.md** | favor_code_representation | Concise names; typed Properties/Operations; no prose |
| **state-ooa-atomic-operations.md** | favor_atomic_responsibilities | One op = one behavior; describe behavior not outcome |
| **state-ooa-bidirectional-relationships.md** | map_bidirectional_collaborators | A↔B when non-primitive |
| **state-ooa-domain-language.md** | use_domain_language, use_natural_english | Domain language; no Hold/Get/Has; natural English |
| **state-ooa-integrate-concepts.md** | integrate_and_organize_concepts | Nest related; avoid noun redundancy; business domain |
| **state-ooa-module-folder-mapping.md** | use_module_for_folder_structure | Optional: Module = folder (dot notation) when mapping to code |

## Summary: Strengthen Existing

| Existing Rule | Change |
|---------------|--------|
| state-synchronize-concepts or interactions-inheritance-domain-concepts | Add: derive from stories; don't invent collaborators |
| interactions-inheritance-domain-concepts | Optionally add: don't fragment (TradeData + TradeCalculator → Trade) |

## Summary: Skip (Already Covered)

| CRC Rule | Reason |
|----------|--------|
| scope_concepts_correctly | In interactions-inheritance-domain-concepts |
| shape_relationships_from_story_map | Strengthen sync rule instead |
