# DDD ⇄ Architecture ⇄ Clean Code — Overlap & Gaps Assessment

**Scope of this note.** A working assessment of where the three engineering-facing skill families overlap uncomfortably, where they hand off cleanly, and where the concepts we actually care about (OOAD, modularization, seams, deep modules, framework mechanisms, domain focus) live — or don't yet live — in the current library.

> **Reading note.** Written in bullet form rather than wide tables so it word-wraps on mobile (GitHub mobile scrolls tables sideways without wrapping). Section §2's concept map is the part that most benefits from this layout.

> **Two-part note.** §1–§8 assess **concept overlap** — where the same ideas live in more than one skill. §9–§16 assess **structural overlap** — the skill vs practice vs stage vs common boundaries, and where reuse leaks through them. Read §1–§8 first if you only want the concept-layer story.

**Skills in scope:**

- **Domain-Driven Design** — `practices/domain-driven-design/`
  - Main pipeline: `abd-domain-glossary`, `abd-domain-language`, `abd-domain-model`, `abd-domain-specification`, `abd-domain-code`.
  - Supporting: `abd-bounded-context-map`, `abd-ddd-design-building-blocks`, `abd-domain-walk`.
  - Shared OO substrate: [`oo-concepts.md`](../../practices/domain-driven-design/reference/oo-concepts.md).
- **Architecture-Centric Engineering** — `practices/architecture-centric-engineering/`
  - Pipeline: `abd-architecture-outline`, `abd-architecture-blueprint`, `abd-architecture-specification`, `abd-architecture-template`, `abd-architecture-code`.
  - Shared model: [`architecture-context-model.md`](../../practices/architecture-centric-engineering/reference/architecture-context-model.md).
  - Mechanism definition: [`architecture-mechanism.md`](../../practices/architecture-centric-engineering/reference/architecture-mechanism.md).
- **Clean Code** — `stages/engineering/abd-clean-code/`
  - Single stage-level skill with 17 rules.
  - Concepts: [`concepts.md`](../../stages/engineering/abd-clean-code/reference/concepts.md).

---

## 1. What each family actually is

**DDD — the domain-perspective pipeline.** Five fidelities (glossary → language → model → specification → code) describing *what the business is*, using OOAD as the notation. `oo-concepts.md` is where "what is a class / when do I use a subtype / how do responsibilities decompose" is authored for the whole library. Business focus is a stated bias, not a hard boundary — the practice keeps saying "domain concepts", but the reference is generic OOAD.

**ACE — the structure-perspective pipeline.** Five fidelities (outline → blueprint → specification → template → code) describing *how the software is organised* into systems, modules, mechanisms, seams. Central abstractions:

- The **architecture mechanism** — a cross-cutting concern with a fixed code shape.
- The per-folder **`architecture-context.md`** — a manual carrying seam, participants, rules, canonical patterns.

**Clean Code — a single-stage rules bundle.** Seventeen rules covering *what good production code looks like line by line* — single-responsibility, small functions, guard clauses, explicit DI, domain-language names, encapsulation, no swallowed exceptions. The concepts page is explicitly OOAD-in-code.

Your summary — *"same rules and truths circling on a big pile of stuff"* — is accurate. The three families are three vantage points on **one underlying OOAD substrate**, with different degrees of business bias and different fidelity structures.

---

## 2. The underlying concept map

For each concept, who currently owns it and how.

### Class — definition, when to introduce one

- **DDD** — authored in [`oo-concepts.md § What is a class`](../../practices/domain-driven-design/reference/oo-concepts.md#what-is-a-class).
- **ACE** — implied via the "Class Specification" section in per-folder context files.
- **Clean Code** — implied via "single-responsibility classes", "class under 200-300 lines".
- **Owner:** DDD's OO substrate; others assume it.

### Responsibilities — property vs operation vs both

- **DDD** — authored in `oo-concepts.md § Decomposing responsibilities`.
- **ACE** — silent.
- **Clean Code** — talks about "one thing" but never distinguishes state from behaviour.
- **Owner:** DDD only.

### Relationships — ownership, collection, independence, direction

- **DDD** — authored in `oo-concepts.md § Relationships`.
- **ACE** — package dependencies covered as "consumers" and "dependencies on other packages".
- **Clean Code** — silent.
- **Owner:** DDD owns the modelling, ACE owns direction between modules. Nothing bridges them.

### Inheritance, subtypes, Liskov, delta rule

- **DDD** — authored in `oo-concepts.md § Inheritance and subtypes`.
- **ACE** — mentioned as one of three "activation paths" for mechanisms (inherited base).
- **Clean Code** — silent.
- **Owner:** DDD.

### Subtype vs type-property vs instance — the "surface the choice" workflow

- **DDD only.** Not obviously exportable to ACE (a module is not a subtype).

### DDD stereotypes (Entity / Value / Aggregate / Repository / Service / Factory / Event)

- **DDD** — supporting skill [`abd-ddd-design-building-blocks`](../../practices/domain-driven-design/skills/supporting/abd-ddd-design-building-blocks/SKILL.md).
- Not integrated into the main model pipeline.

### Bounded context — model boundary, ubiquitous language scope

- **DDD** — supporting skill [`abd-bounded-context-map`](../../practices/domain-driven-design/skills/supporting/abd-bounded-context-map/SKILL.md).
- **ACE** — related but distinct concept: **module** (with a scope).
- **The sharpest overlap in wording ("boundary", "context") without a shared vocabulary.** See §4.2.

### Modularization / module definition

- **DDD** — implicit; bounded context is *organisational*, the code side is left to ACE.
- **ACE** — authored: module catalogue in blueprint; package-tier context file.
- **Clean Code** — implicit ("one module per sub-epic area").
- **Owner:** ACE.

### Seams / public API vs internals

- **DDD** — silent.
- **ACE** — authored in [`package-seam-is-minimal-and-named`](../../practices/architecture-centric-engineering/skills/abd-architecture-specification/rules/package-seam-is-minimal-and-named.md) (Ousterhout cited).
- **Clean Code** — implicit ("expose behavior, not raw data"; `_private` helpers).
- **Owner:** ACE at module level; clean-code covers the class-level analogue; DDD silent.

### Deep modules (Ousterhout — small surface, big function)

- **ACE only.** Not obviously mapped to DDD's aggregate/entity concept, though it should be.

### Encapsulation / hiding state

- **DDD** — implicit in the OO reference.
- **ACE** — implicit in `package-context-file-stays-out-of-domain-details`.
- **Clean Code** — authored in [`enforce-encapsulation`](../../stages/engineering/abd-clean-code/rules/enforce-encapsulation.md).
- **Owner:** clean-code at class level; ACE at module level; DDD assumes it.

### Isolation / decoupling / dependency direction

- **DDD** — silent.
- **ACE** — authored: "one direction of dependency per pair"; blueprint dependency lists.
- **Clean Code** — implicit: "explicit dependencies", constructor DI.
- **Owner:** ACE for modules; clean-code for classes; no bridge.

### Explicit constructor DI

- **DDD** — implicit; model diagrams show collaborators.
- **ACE** — implicit; canonical patterns cover wiring.
- **Clean Code** — authored in [`use-explicit-dependencies`](../../stages/engineering/abd-clean-code/rules/use-explicit-dependencies.md).
- **Owner:** clean-code at class level.

### Domain language in code

- **DDD** — authored: glossary → language → model chain, names inherited.
- **ACE** — vocabulary chain enforced across artefacts, but not to *domain* terms.
- **Clean Code** — authored in [`use-domain-language`](../../stages/engineering/abd-clean-code/rules/use-domain-language.md).
- **Owner:** DDD; clean-code repeats DDD's rule at code level.

### Framework / cross-cutting mechanism — one shape, many instances

- **ACE only** — [`architecture-mechanism.md`](../../practices/architecture-centric-engineering/reference/architecture-mechanism.md); `abd-architecture-template` produces a runnable scaffold.
- Nothing in DDD acknowledges that a business domain can itself supply a framework (e.g. a base Payment).

### Function-level rules — size, params, guards, exceptions, comments

- **Clean-code only** — 17 rules under `rules/`. Clean-code owns line-level discipline.

---

## 3. The core observation

Everything except the top-level *pipeline* is one substrate: **OOAD, applied recursively to units of different sizes.**

- A **domain concept** is a unit that earns identity because of state, behaviour, or interactions (DDD OO reference).
- A **module** is a unit that earns identity because of cohesive scope, deep functionality behind a named seam (ACE).
- A **class** is a unit that earns identity because it has one reason to change and exposes behaviour, not data (clean code).
- A **mechanism** is a *shape* — a unit that other units instantiate — with a fixed extension contract (ACE).

The rules pointing at these units are almost identical:

- *Cohesion, one reason to change* — DDD ("what is a class"), ACE ("package-surface-is-cohesive"), clean-code ("keep-classes-single-responsibility").
- *Minimal named surface, deep inside* — ACE ("package-seam-is-minimal-and-named" citing Ousterhout), clean-code ("enforce-encapsulation", "expose behavior not data"), DDD (implicit in aggregate boundaries).
- *Dependency direction is a first-class decision* — ACE ("one direction per pair"), DDD ("navigating end"), clean-code ("explicit dependencies").
- *Names come from the domain* — DDD (glossary → language → model), clean-code ("use-domain-language"), ACE ("vocabulary-matches-source-of-truth" — but the "source" is the outline/blueprint, not the domain glossary).

**The families are not saying different things. They are saying the same things at different scales and about different subjects.** That is the "uncomfortable overlap".

---

## 4. The specific overlaps — resolved, ambiguous, or in conflict

### 4.1 Clean Code ⇄ Domain Code — resolved (explicit hand-off)

`abd-domain-code` explicitly delegates production-code shape to `abd-clean-code`:

> **Step 3. Write production code — follow abd-clean-code** ... Read and follow `abd-clean-code/SKILL.md` in full.
> — [`abd-domain-code/reference/generate.md`](../../practices/domain-driven-design/skills/abd-domain-code/reference/generate.md)

`abd-architecture-code` does the same:

> **GREEN — production** ... `abd-clean-code` ... **MUST** read and follow that skill's `SKILL.md` and `rules/` when writing production code.
> — [`abd-architecture-code/reference/generate.md`](../../practices/architecture-centric-engineering/skills/abd-architecture-code/reference/generate.md)

**Verdict:** clean-code is the shared engineering-stage terminal skill. Both pipelines converge on it. This part of the design is coherent.

### 4.2 DDD "bounded context" ⇄ ACE "module / package" — ambiguous, no bridge

- **Bounded context** ([bounded-context-map concepts](../../practices/domain-driven-design/skills/supporting/abd-bounded-context-map/reference/concepts.md)) — *"an explicitly set boundary in which a model applies and is managed to be uniform"*. Has an organisational facet AND an implementation facet ("code base, database schema, or deployable unit").
- **Module / package** ([architecture-context-model § 2](../../practices/architecture-centric-engineering/reference/architecture-context-model.md#2-three-tiers-of-context-file)) — a folder tier with "deep functional surface area" and a public seam.

These overlap heavily in the "implementation facet". A bounded context that maps 1:1 to a deployable unit *is* an ACE module (or a group of them). But **there is no explicit bridge**:

- No rule in ACE says "a package's ubiquitous language is authored by a bounded context".
- No rule in DDD says "a bounded context resolves to N modules in the blueprint".

The vocabularies drift silently.

**This is the sharpest structural overlap in the library.** DDD *does* talk about implementation boundaries, but it does so in `abd-bounded-context-map` — a *supporting* skill, not part of the main pipeline — and the resulting artefact never enters ACE's outline/blueprint as an input.

### 4.3 "Domain language" ⇄ "vocabulary matches source of truth" — parallel, unconnected chains

Two vocabulary chains run in parallel:

- **DDD chain** — glossary → language → model → specification → domain code. Source of truth for *business* terms.
- **ACE chain** — [architecture-context-model § 3](../../practices/architecture-centric-engineering/reference/architecture-context-model.md#3-the-vocabulary-chain): outline → blueprint → specification → template → architecture code. Source of truth for *system, mechanism, module, and layer* names.

Clean-code's `use-domain-language` sits at the end of the DDD chain. Clean-code has no equivalent hook that says "architecture mechanism names propagate to code symbols too" — even though ACE's vocabulary chain claims exactly that:

> `abd-architecture-code` — inherits all of the above verbatim; instantiates the template package's patterns for stories.
> — architecture-context-model § 3

**Verdict:** two independently coherent chains, no crossover rule. In practice a code file must satisfy *both* — the class name is a domain entity (DDD) *and* the surrounding module/mechanism scaffolding uses ACE's vocabulary. The current skills never state that jointly.

### 4.4 "Single responsibility" — stated three times with slightly different meanings

- **DDD** — "one class per named domain idea that earns identity" — cohesion around a *domain concept*.
- **ACE** — "package-surface-is-cohesive" — cohesion around a *subject / external system / capability*.
- **Clean Code** — "keep-classes-single-responsibility" — one reason to *change* (SRP).

Not contradictions, but three definitions of the same principle at three scales. A reader hitting all three has to work out that they are consistent. No cross-reference makes that explicit.

### 4.5 Encapsulation ⇄ deep modules ⇄ aggregates — same idea, three names

Your instinct — *"deep modules, public api vs internals, encapsulation"* — is one concept. It shows up as:

- Ousterhout's *deep module* in ACE (small seam, big functionality) — `package-seam-is-minimal-and-named`.
- Aggregate *root and internals* in DDD stereotypes (`abd-ddd-design-building-blocks`) — the aggregate root is the seam; inner entities and value objects are internals.
- Class-level *encapsulation* in clean-code — `enforce-encapsulation`, private members hidden, behaviour exposed.

Nothing in the library says these three are the same idea at three scales.

---

## 5. The specific gaps

### 5.1 ACE has no OOAD reference of its own; it borrows implicitly from DDD

Your phrasing: *"Architecture Eng is really about module definition, and creating some modules that are framework-pattern enabling other modules; it needs better OOAD from the DDD skills."*

Evidence:

- `abd-architecture-specification`'s per-folder templates include a **"Class Specification"** section — but the rules that govern *what a good class looks like* are not in ACE. They are in DDD's `oo-concepts.md` and in clean-code's rule set. ACE is silent on how to author that section.
- `abd-architecture-code`'s Step 2 delegates to `abd-clean-code` for class-level shape, but never to DDD's OO reference for class-level *modelling*.

The consequence: an ACE package-tier context file can name participants and rules without ever asking "which of these participants earns identity, and why?" — the DDD question. Result is often participant lists that read as *file inventories* rather than *class models*.

**Gap:** ACE spec should either (a) import DDD's `oo-concepts.md` as a read-gate for its Class Specification section, or (b) restate the class / responsibility / relationship discipline in its own reference.

### 5.2 DDD has no module concept in the main pipeline

Your phrasing: *"DDD skills language forward are about OOAD, and domain focus is very complementary with the idea of documenting the external facing pieces of a module; and has explicit module language."*

The "explicit module language" you're remembering lives in **two support skills** — `abd-bounded-context-map` and (structurally) the aggregate stereotype in `abd-ddd-design-building-blocks`. Neither is in the shaping → discovery → exploration → specification → engineering main pipeline. In practice a domain model can be authored and coded without either.

**Gap:** if DDD is meant to include module thinking, the bounded-context map (or an equivalent module-boundary artefact) should be a first-class step in the pipeline, not a supporting skill.

### 5.3 No cross-family concept of "the domain provides a framework"

Your phrasing: *"all payments can leverage a base payment framework."*

Today:

- ACE's mechanism concept is defined as **cross-cutting concerns**: security, error handling, logging, validation, configuration, caching, communication, persistence. Its canonical categories are all technical.
- DDD's OO reference has *base class + subtype* — with a payment example — but this is class-level modelling, not a project artefact that other domain modules extend.
- Nothing in the library names the pattern you care about: **a domain-level framework** — one bounded context or module that provides a base shape that other domain modules extend, with the same "code shape constraint" discipline ACE uses for technical mechanisms.

**Gap:** either ACE's mechanism concept broadens to cover domain-level frameworks (Payment base as a mechanism whose instances are ACH / Wire / Card modules) or DDD gains a "domain framework" artefact that consumes both practices. Today it falls between.

### 5.4 No unified place to state "the OOAD unit-at-any-scale" rules

The rules you listed — good class / function / module design, encapsulation, isolation, decoupling, deep modules, seams, public API vs internals — are currently authored in three places at three scales:

- DDD `oo-concepts.md` — class scale, domain-concept flavour.
- ACE `package-seam-is-minimal-and-named` + `architecture-context-model.md` — module scale, structural flavour.
- Clean-code `rules/` — class + function scale, code flavour.

A reader who wants "the abd-skills theory of a good unit" has to synthesise across three families. That is exactly the "same rules and truths circling on a big pile of stuff" symptom.

**Gap:** a shared "unit design" reference (or explicit cross-links between the three current homes) would let each family stop restating and start pointing.

### 5.5 Testing responsibility is split, not framed

- ACE names testing tiers and stub boundaries at the module level (blueprint + `testing-architecture.md`).
- DDD names domain-only test scope in `abd-domain-code` ("in-memory fakes; no infrastructure").
- Clean-code says nothing about testing.

Not your stated question, but adjacent — the same fracture pattern applies: two families make partial statements, no shared framing.

---

## 6. What the current library says the shape *is* (evidence for a redraw)

Sources that already hint at a unified shape, if you want to argue for consolidation:

- **DDD's OO reference is generic OOAD, not business-specific**, despite the practice's name. `oo-concepts.md` never uses the word "business" outside the payment example. It can be lifted to a library-wide reference with no rewrite.
- **ACE explicitly cites Ousterhout's deep modules** in a rule — `package-seam-is-minimal-and-named` — which is the same discipline clean-code applies to classes.
- **Both terminal skills (`abd-domain-code`, `abd-architecture-code`) hand off to `abd-clean-code`.** The library has already conceded that clean-code is the shared engineering-stage skill.
- **`architecture_and_design.json` lists DDD as one option under "architecture and layering"** — somewhere the library already treats DDD as *a way to do architecture*, which is a stronger claim than either practice makes in its main text.

---

## 7. Options for reshaping (choices, not recommendations)

If the aim is to remove the uncomfortable overlap without collapsing distinct value, the choices seem to be:

**Option A — Extract a shared "unit design" reference.**
Move the OOAD-at-any-scale rules (class earns identity, cohesion, deep unit, minimal seam, encapsulation, direction of dependency) to a library-level reference at `practices/reference/unit-design.md`. Each family cites it and adds the *scale-specific* discipline on top:

- DDD adds "the unit is a domain concept; names come from the ubiquitous language".
- ACE adds "the unit is a module or a mechanism; seams participate in cross-cutting concerns".
- Clean-code adds "the unit is a class or a function; here is the line-level discipline".

Cost: a new shared reference; three families updated to cite instead of restate. Payoff: one authoring site for the recurring rules; the three families become genuinely orthogonal (subject, structure, code) instead of overlapping restatements.

**Option B — Rename and re-scope, leave content in place.**
Accept the three families as three subjects (domain, structure, code) and add explicit cross-reference sections. Every place clean-code says "domain language" it links to DDD; every place ACE says "Class Specification" it links to DDD's OO reference; every place DDD's `abd-domain-model` writes classes it links to clean-code's class-level rules.

Cost: cheaper — no new artefact, just cross-links. Payoff: overlap becomes visible and traceable rather than silent. Does not solve the "same rule authored three times" problem.

**Option C — Promote bounded context into DDD's main pipeline and formalise the domain-module bridge to ACE.**
Address §4.2 and §5.2 specifically. Bounded-context map becomes a required step between `abd-domain-language` and `abd-domain-model`, and its output becomes a required input to `abd-architecture-outline` (each module in the blueprint traces to one or more bounded contexts).

Cost: pipeline change, cross-practice dependency. Payoff: closes the sharpest structural gap; makes "domains as frameworks" (§5.3) expressible — a bounded context can produce a base module that others extend.

**Option D — Broaden the mechanism concept to include domain-level frameworks.**
Address §5.3 by editing `architecture-mechanism.md`: mechanisms today are cross-cutting *technical* concerns; broaden to cross-cutting *domain* concerns too. A Payment base with ACH / Wire / Card extensions is a mechanism; every payment module adopts the same code shape.

Cost: small edit to one reference; ripple through blueprint and template skills. Payoff: gives your "base payment framework" example a legitimate home.

The options are additive, not exclusive. A + C + D together produce the tidiest library; B alone is the cheapest improvement.

---

## 8. Summary — what to take from this note

- The three families are three lenses on **one OOAD substrate applied at three scales** (concept, module, class / function).
- The **hand-off from both `*-code` skills to `abd-clean-code` is explicit and works.** That part is fine.
- The **hand-off between DDD and ACE is not made anywhere.** Both practices talk about boundaries; only ACE talks about modules; only DDD talks about concepts; nothing joins them. Two support skills (`abd-bounded-context-map`, `abd-ddd-design-building-blocks`) live outside the main pipeline where the bridge would go.
- The **OO reference in DDD is generic OOAD** and could serve the whole library. ACE currently borrows it implicitly; clean-code re-states pieces of it at code level.
- **"Deep modules / seams / encapsulation" is one concept** authored three times at three scales, with no cross-link.
- **"Domain framework" (base + extenders) has no home.** Mechanism is technical; DDD stops at the class-level inheritance discussion. This is a real gap for your mental model.
- Two vocabulary chains run in parallel with no crossover rule; a good code file must satisfy both.

The document is deliberately assessment-only — no reshaping has been done. The four options in §7 sketch what a reshape could look like if you decide to act on the assessment.

---

# Part II — Structural overlap: skill / practice / stage / common

Concept overlap (§1–§8) is only half the story. Underneath the concept homes there is a structural taxonomy — perspective, fidelity, tier, role — that decides *where each concept can live*. The uncomfortable overlaps in Part I are often really structural mismatches: content authored in one layer but consumed by skills in a different layer, with no formal reuse mechanism between them.

Part II reads the library as an architecture in its own right — perspective × fidelity axes, four structural layers (common / stage / practice / skill), three tiers (practice / foundational / support), and the front-matter fields that place every skill in the taxonomy — and then names the specific boundary ambiguities that make the concept overlaps hard to fix.

---

## 9. The four structural layers the library actually uses

Not two (skill vs practice), but **four**. Each with its own folder, its own contract, and a different role in reuse.

### Common — `common/`

Cross-library machinery. Every skill in every practice reads from here. This is the *procedural* layer — how to run a skill, how to validate, where to write output.

Contents:

- `common/reference/skill-workflow.md` — bootstrap + read-gates + generate + validate contract. Every practice `SKILL.md` mandates reading this before generation.
- `common/reference/rule-checklist.md` — universal per-rule verdict format.
- `common/reference/context-taxonomy.md` — the perspective × fidelity model (see §10).
- `common/reference/skill-package-layout.md` — `SKILL.md`, `rules/`, `reference/`, `templates/`, `scanners/` contract.
- `common/reference/skill-index.md` — auto-generated skill catalogue.
- `common/reference/folder-conventions.md` — canonical output paths for every skill.
- `common/reference/decision-record.md`, `agentic-repair-loop.md`, `manual-repair-loop.md`, `record-all-architecture-violations.md`, `grill-me-with-practice-skill.md` — shared procedures.
- `common/reference/stages/{context,shaping,discovery,exploration,specification,engineering}.md` — the fidelity definitions.
- `common/scripts/`, `common/templates/`, `common/instructions/`, `common/prompts/`, `common/context-scaffold/`.

Consumer contract: every skill's SKILL.md links `common/reference/skill-workflow.md`; every practice's perspective file links `common/reference/context-taxonomy.md`. Reuse is via link, not copy.

### Stage — `stages/<fidelity>/[skills/]<skill>/`

Skills that belong to a fidelity level but aren't owned by a single perspective. `context-perspective: stage` in front matter. Directly under `stages/` (no practice bundle around them).

Current inventory:

- `stages/shaping/skills/` — `abd-cost-of-delay`, `abd-impact-mapping`, `abd-opportunity-generation`, `abd-simple-validated-learning`. All practice-tier, all shaping-fidelity, all cross-perspective.
- `stages/discovery/` — `abd-code-research`, `abd-service-level-objectives`.
- `stages/engineering/` — `abd-clean-code`, `abd-secure-code`.

Consumer contract: any practice can call a stage skill at the matching fidelity. The two `*-code` skills in `abd-domain-code` and `abd-architecture-code` explicitly hand off to `abd-clean-code` here.

### Practice — `practices/<family>/`

A perspective-owning bundle. One perspective, a pipeline of skills across fidelities, shared reference material, optional support skills, sometimes example specs.

Anatomy (using DDD and ACE as examples):

- `reference/` — the practice's shared conceptual substrate. DDD has `oo-concepts.md`, `domain-perspective.md`, `validate-checklist.md`, `source-traceability.md`, `diagram-workflow.md`. ACE has `architecture-context-model.md`, `architecture-mechanism.md`, `architecture-perspective.md`, `validate-checklist.md`, `diagram-workflow.md`, `architecture_and_design.json`, `data.md`.
- `references/` (DDD) — practice-wide artefact schemas (`domain-model-json.md`, template JSON, example JSON).
- `skills/` — the pipeline: one skill per fidelity level in the perspective.
- `skills/supporting/` — support skills (see §14).
- `specs/` (ACE) — worked example specifications (`hero-vtt`, `mern-domain-first-specification`, `domain-driven-vs-code-plugin`).
- `README.md` — one-paragraph package overview.

Consumer contract: a practice's `<perspective>-perspective.md` file lists its skills by fidelity level; the perspective is the practice's spine.

### Skill — `skills/<name>/`

The leaf unit. Contract from `common/reference/skill-package-layout.md`:

- `SKILL.md` — thin router (purpose, bootstrap, read-gates, generate, validate).
- `rules/*.md` — source of truth for rule prose.
- `reference/*.md` — concept teaching, examples, heuristics.
- `templates/*` — layout contracts.
- `scanners/*-scanner.py` — optional, linked from rule frontmatter via `scanner:`.

Consumer contract: `SKILL.md` mandates reading `common/reference/skill-workflow.md`, then the skill's own rules / reference / templates. May also mandate reading practice-level reference and other skills' `SKILL.md` (e.g. `abd-domain-code` mandates `abd-clean-code`).

**The four layers, one line each:**

- **Common** — procedure and taxonomy, cross-library.
- **Stage** — cross-perspective quality gates, one fidelity level each.
- **Practice** — perspective-owning bundle: reference + pipeline + support.
- **Skill** — the leaf artefact producer.

---

## 10. The two-axis taxonomy — perspective × fidelity

Every practice skill declares its position in a matrix via YAML front matter (`context-taxonomy.md`).

**Perspectives** (five): `domain`, `stories`, `ux`, `architecture`, `stage`.

**Fidelities** (six): `context`, `shaping`, `discovery`, `exploration`, `specification`, `engineering`.

The default perspective order is `domain → stories → ux → architecture`; specification is the never-skip fidelity.

### Where the three families sit in the matrix

- **DDD (domain perspective)**
  - Shaping — `abd-domain-glossary` (glossary)
  - Discovery — `abd-domain-language` (language)
  - Exploration — `abd-domain-model` (conceptual-model)
  - Specification — `abd-domain-specification` (typed-model); `abd-domain-walk` (walkthrough)
  - Engineering — `abd-domain-code` (domain-tdd)
- **ACE (architecture perspective)**
  - Shaping — `abd-architecture-outline` (system-context)
  - Discovery — `abd-architecture-blueprint` (blueprint / scaffold)
  - Exploration — `abd-architecture-specification` (document)
  - Specification — `abd-architecture-template` (project / mechanism)
  - Engineering — `abd-architecture-code` (production-code)
- **Clean Code (stage perspective)**
  - Engineering — `abd-clean-code` (quality-gate). One cell only.

### What this reveals

- **DDD and ACE occupy parallel columns of the matrix.** Each fidelity has one domain skill and one architecture skill. They are structurally symmetric — which is why the concept overlap feels uncomfortable: the two columns describe *the same fidelities* through *different lenses*, but nothing bridges the columns row by row.
- **Clean-code occupies a single cell** — engineering × stage. It is by design a *cross-column* skill; both `abd-domain-code` and `abd-architecture-code` route through it.
- **No cross-column skill exists at any other fidelity.** There is no `abd-<...>-glossary` at stage; no cross-perspective specification skill; no cross-perspective exploration skill. Cross-column reuse is *only* granted at engineering.
- **Domain × any fidelity has no analogue to `architecture-mechanism`** — that is, DDD has no artefact that captures "the pattern all payments must follow" at the domain level. This is the same finding as §5.3, now visible as an empty matrix cell rather than just a missing concept.

---

## 11. Skill boundary — what the library treats as one skill vs many

Reverse-engineered from front-matter usage, the library follows roughly these rules for what earns its own skill:

- **One skill per `(perspective, fidelity, mode)` cell.** A cell may have multiple modes (e.g. `abd-architecture-blueprint` has `blueprint` and `scaffold` modes), and those modes live inside one skill package rather than being split. Similarly `abd-architecture-specification` has `document` and `template` modes across two fidelities.
- **A skill in a perspective's pipeline shares that perspective's reference bundle.** DDD's five main skills all point at `oo-concepts.md`; ACE's five all point at `architecture-context-model.md`.
- **Cross-perspective content becomes a stage skill.** Clean-code, secure-code, code-research, SLOs — all live under `stages/` because they serve any perspective.
- **Machinery becomes a foundational tier skill.** `story-graph-ops`, `domain-ops`, `drawio-*-sync`, `track_task`, `abd-skill-catalog`, `abd-kanban-repo` — all carry `catalog_garden_tier: foundational`. They are libraries, not artefact producers.
- **Callable-anywhere-but-off-the-pipeline becomes a support skill.** `context-role: support` in front matter + `supporting/` folder location. Examples: `abd-bounded-context-map`, `abd-ddd-design-building-blocks`, `abd-domain-walk` (also main pipeline at specification), `drawio-*-sync`, `story-graph-ops`, `domain-ops`, `abd-thin-slicing`.

### What this reveals about the DDD ⇄ ACE gap

The rules above **cannot produce a DDD-to-ACE bridge skill**:

- A bridge would need to span two perspectives, so it cannot be a practice skill (single perspective) — it would have to be a stage skill.
- But every stage skill so far is *engineering* fidelity. There is no precedent for a stage skill at exploration or specification fidelity, which is where the bridge would sit.
- The nearest existing analogue — `abd-bounded-context-map` — is placed as a *DDD support skill* instead of a cross-perspective stage skill. That is a boundary choice: the library decided the bridge belongs to DDD, not to a shared stage.

Either the choice is right and DDD must own it end-to-end (in which case the support skill needs to be promoted into the DDD pipeline — §5.2), or the choice is wrong and the bridge should be a new stage-perspective skill at exploration or specification fidelity.

---

## 12. Practice boundary — what makes a practice

A practice today is a folder under `practices/` with **five typical ingredients**:

- **One perspective** (`context-perspective` value shared by its skills). DDD → `domain`. ACE → `architecture`.
- **A perspective reference** — `reference/<perspective>-perspective.md` listing skills by fidelity.
- **A shared concept substrate** — DDD's `oo-concepts.md`, ACE's `architecture-context-model.md` + `architecture-mechanism.md`.
- **A pipeline of skills** covering multiple fidelity levels.
- **Support skills and (optionally) example specs.**

### Which practices actually match this shape

- **Domain-Driven Design** — clean match. One perspective, full pipeline, shared substrate, support skills.
- **Architecture-Centric Engineering** — clean match. Same structure as DDD.
- **User Experience Design** — clean match (perspective = `ux`).
- **Story-Driven Delivery** — mostly clean (perspective = `stories`).

### Which practices break the shape

- **Behavior-Driven Development** — `catalog_garden_family: behavior-driven-development` on `abd-bdd-*` skills, but BDD is not a perspective in `context-taxonomy.md`. Its skills straddle stories (behaviour specs) and architecture (test wiring). The practice folder exists; the perspective doesn't.
- **Context-Driven Delivery** — cross-cutting orchestration; not perspective-owned.
- **Kanban** — flow management, cross-cutting; not perspective-owned.
- **User Experience Design** — folder appears twice: `practices/user-experience-design/skills/*` **and** `practices/kanban/user-experience-design/skills/*`. Two of the UX skills (`abd-ux-mockup`, `abd-interface-design`, `abd-information-architecture`) live in both trees. Migration state or duplication.

### The boundary ambiguity that matters for Part I

- **Clean-code and secure-code both self-declare `catalog_garden_family: architecture-centric-engineering`** in front matter — even though they physically live under `stages/engineering/` and carry `context-perspective: stage`. The catalog rollup groups them under ACE; the perspective taxonomy groups them under `stage`. **Two authoritative answers to "which practice owns clean-code?" — ACE (catalog) and no-one (perspective is stage).**

This mismatch is where the "clean-code as shared terminal skill" story from §4.1 becomes structurally awkward: it is treated as a stage skill by hand-off contracts (`abd-domain-code` → `abd-clean-code`; `abd-architecture-code` → `abd-clean-code`) but as an ACE skill by the catalog. If DDD also depends on it — and it does — the ACE family label is misleading.

---

## 13. Common reuse — what is genuinely shared vs restated

Distinguish three flavours of reuse:

- **Genuinely shared** — content lives in `common/` (or a practice's `reference/`) and every consumer *links* to it, without restating.
- **Practice-shared** — content lives in one practice and multiple skills within that practice link to it.
- **Restated** — the same conceptual content is authored independently in multiple places, with no cross-links.

### Genuinely shared (in `common/`)

- `skill-workflow.md` — every practice `SKILL.md` mandates it in `## Bootstrap` and `## Read`.
- `rule-checklist.md` — every practice `SKILL.md`'s `## Validate` links here.
- `folder-conventions.md` — resolved by every skill for output path.
- `context-taxonomy.md` — perspective × fidelity vocabulary. Referenced by perspective files.
- `skill-package-layout.md`, `skill-index.md`, `decision-record.md`, `grill-me-with-practice-skill.md` — all imported, not restated.
- `record-all-architecture-violations.md` — imported by ACE's perspective file.

Verdict: `common/` is **cleanly reused for procedural machinery**. This part of the library is coherent.

### Practice-shared (in `practices/<family>/reference/`)

- **DDD** — `oo-concepts.md` (imported by domain-language, domain-model, domain-specification), `domain-perspective.md`, `diagram-workflow.md`, `validate-checklist.md`, `source-traceability.md`.
- **ACE** — `architecture-context-model.md` (imported by all five ACE skills), `architecture-mechanism.md`, `architecture-perspective.md`, `diagram-workflow.md`, `validate-checklist.md`.

Verdict: practice-shared reference is **cleanly reused within a practice**. Nothing wrong with either family internally.

### Restated (concept authored more than once, no cross-link)

- **OOAD substrate** — DDD's `oo-concepts.md` is the only authored reference; ACE and clean-code assume it silently.
- **Seam / deep module** — ACE's `package-seam-is-minimal-and-named` + clean-code's `enforce-encapsulation`. Two authored places, no cross-link.
- **Single responsibility** — DDD's "what is a class", ACE's `package-surface-is-cohesive`, clean-code's `keep-classes-single-responsibility`. Three authored places, no cross-link.
- **Constructor DI** — clean-code's `use-explicit-dependencies`. ACE's canonical patterns show it in code but do not name it as a rule. DDD implies it via collaborator diagrams. One authored place; two implicit consumers.
- **Domain language in code** — DDD's glossary→language→model chain + clean-code's `use-domain-language`. Two authored places; the clean-code rule is a copy of the DDD chain's terminal expectation, without linking upstream.
- **Vocabulary chain** — DDD chain (glossary→…→domain-code) + ACE chain (outline→…→arch-code). Two authored places, no crossover rule.

### The pattern

Reuse works well when the content is **procedure** (workflow, gates, folder paths, taxonomy). Reuse fails when the content is **concept** (OOAD units, seams, cohesion, dependency direction). The `common/` layer today has no conceptual substrate — there is no `common/reference/oo-concepts.md` or `common/reference/unit-design.md`. Every practice reinvents its concept layer, which is why the three families' concept homes overlap so uncomfortably.

**This is the deepest structural finding.** Part I's concept-overlap findings all trace back to the same missing thing: a shared conceptual reference in `common/`, with the same linking discipline that the procedural references already enjoy.

---

## 14. Support / foundational / practice — the boundary lines actually used

Front-matter reveals three orthogonal tier markers plus a role marker:

- **`catalog_garden_tier: practice`** — the artefact-producing pipeline skills. Most skills.
- **`catalog_garden_tier: foundational`** — machinery. `story-graph-ops`, `domain-ops`, `drawio-*-sync`, `track_task`, `abd-skill-catalog`, `abd-kanban-repo`. Data ops, diagram sync, tracking, catalog generation.
- **`context-role: support`** — callable but not on the pipeline. `abd-bounded-context-map`, `abd-ddd-design-building-blocks`, `abd-domain-walk`, `abd-thin-slicing`, `drawio-*-sync`, `story-graph-ops`, `domain-ops`, `miro-story-sync`.
- **(implicit fourth) stage skill** — `context-perspective: stage` + lives under `stages/<fidelity>/`.

### The boundary lines currently in force

- **Practice skill** owns a `(perspective, fidelity)` cell and belongs to a family.
- **Support skill** is callable from any pipeline step but not part of the default flow. Concept-central skills can end up here (see below).
- **Foundational skill** is machinery — no artefact fidelity in the human sense.
- **Stage skill** is cross-perspective; fidelity is fixed, perspective is `stage`.

### The boundary line that misfires

The support / practice line is where concept-central material has been misfiled:

- **`abd-bounded-context-map`** — the structural bridge between DDD and ACE (§5.2). Currently `context-role: support`, meaning "not on the default flow". Anyone running the domain pipeline can finish it without ever touching bounded contexts.
- **`abd-ddd-design-building-blocks`** — the DDD stereotypes (Entity, Value Object, Aggregate, Repository, Service, Factory, Event) that are how DDD talks about *seams within the domain*. Same story: `context-role: support`, off the default flow.
- **`abd-domain-walk`** — has both a support tag and a specification-fidelity entry in `domain-perspective.md`. Straddles.

**Consequence:** the "same rules and truths circling on a big pile of stuff" symptom you named is partly the *support-vs-pipeline classification decision*. Bounded contexts and building blocks are structurally central; they have been placed off the default flow; so their content has to be restated (poorly) elsewhere to be heard.

---

## 15. Concrete boundary ambiguities visible in the library today

Ambiguities not to be fixed here — just named, so a future edit knows what to look at:

- **A1 — `abd-clean-code` catalog family vs perspective.** Front matter says `catalog_garden_family: architecture-centric-engineering`; perspective says `stage`. Two answers to "which practice owns this?".
- **A2 — `abd-secure-code`** — same pattern as clean-code.
- **A3 — `abd-bounded-context-map` support-vs-pipeline.** Concept-central; off the pipeline. See §14.
- **A4 — `abd-ddd-design-building-blocks` support-vs-pipeline.** Same as A3.
- **A5 — Duplicated UX skill folders.** `practices/user-experience-design/skills/` and `practices/kanban/user-experience-design/skills/` both contain `abd-ux-mockup`, `abd-interface-design`, `abd-information-architecture`. Migration state or duplication.
- **A6 — BDD family without a perspective.** `catalog_garden_family: behavior-driven-development` exists in front matter but is not a perspective in `context-taxonomy.md`; BDD skills sit ambiguously between stories and architecture.
- **A7 — `story-graph-ops` and `domain-ops`** — both listed as `catalog_garden_tier: foundational` AND `context-role: support`, so tier and role both apply. Not necessarily wrong, but shows the tier and role axes are not orthogonal in practice.
- **A8 — No `common/reference/` conceptual substrate.** `common/` holds only procedural references. Every practice reinvents its concept layer. See §13.
- **A9 — No cross-perspective skills above engineering fidelity.** Stage-perspective skills exist only at shaping, discovery, engineering — no exploration or specification stage skills. A DDD-to-ACE bridge would have nowhere to live under current conventions.

---

## 16. Structural reshape options (extending §7)

Following the same "options, not recommendations" convention. The Part I options (A / B / C / D) address *concept* placement; these address *structural* placement.

- **Option E — Create `common/reference/oo-concepts.md` (or a broader `unit-design.md`).** Extract DDD's OO reference and promote it to the common procedural layer. The current DDD file becomes a thin pass-through that adds domain-specific bias. ACE cites the common file for its Class Specification section. Clean-code cites the common file for its class/function rules. Closes §5.1, §5.4, §13-restated.
- **Option F — Create `common/reference/mechanism.md` covering both technical and domain frameworks.** Lift ACE's `architecture-mechanism.md` into `common/`, generalise "cross-cutting concern" to include cross-cutting *domain* concerns. Add DDD-flavoured examples (Payment base + subtypes). Closes §5.3.
- **Option G — Reconcile `catalog_garden_family` with `context-perspective` for stage skills.** Two paths: (i) fold clean-code and secure-code back into ACE's skills folder — accept they are ACE skills that happen to be reused by DDD; or (ii) keep them under `stages/engineering/` and drop the `catalog_garden_family: architecture-centric-engineering` header (replace with something like `catalog_garden_family: engineering-quality-gates`). Closes A1, A2.
- **Option H — Promote structural support skills into their practice's pipeline.** Bounded-context-map moves from DDD support to DDD exploration (between language and model). DDD building blocks moves to DDD specification. Both are wired into `domain-perspective.md`'s fidelity table. Closes A3, A4, §5.2.
- **Option I — Formalise a cross-perspective stage tier at exploration / specification fidelity.** Add a `stages/exploration/` or `stages/specification/` folder and place a new bridge skill there (e.g. `abd-domain-to-module-map`). Requires accepting stage-perspective skills above engineering, which today the library does not. Closes A9 and gives §5.2 a legitimate home if H is not chosen.
- **Option J — Deduplicate the UX skill trees.** Pick one home for `abd-ux-*`; delete the other. Closes A5.
- **Option K — Add BDD to the perspective taxonomy or fold it into stories / architecture.** Either extend `context-taxonomy.md` with a `behaviour` perspective (with knock-on effects across other practices), or reclassify each BDD skill's perspective to `stories` or `architecture` and remove `catalog_garden_family: behavior-driven-development`. Closes A6.

The Part I options and Part II options are additive:

- Concept-level fix without structural change: A or B from Part I.
- Structural fix without new concept content: G, J, K from Part II.
- Deep fix (recommended reading direction): E + F + H, which together make `common/` the conceptual substrate, promote the structural bridge into DDD's pipeline, and unify the mechanism concept — and Part I's A + C + D drop out for free.

---

## 17. Extended summary — the structural story

Repeating Part I's summary points and adding the structural findings:

- The three families are three lenses on **one OOAD substrate applied at three scales**.
- The `*-code` → `abd-clean-code` hand-off is explicit and works.
- The DDD ⇄ ACE hand-off is not made anywhere.
- The library has an **explicit taxonomy** — perspective × fidelity, with tier (practice / foundational) and role (support) as orthogonal markers. Every skill declares its cell in front matter.
- The library has **four structural layers** — common, stage, practice, skill — with clear procedural contracts.
- **`common/` is well-formed for procedure but empty of concept.** Workflow, gates, folder paths, taxonomy — all shared. OOAD, seams, unit design, cohesion — restated per practice.
- The DDD ⇄ ACE bridge cannot live where it structurally needs to: no stage-perspective skills exist above engineering fidelity, and the current bridge candidates (`abd-bounded-context-map`, `abd-ddd-design-building-blocks`) are filed as *support*, meaning "off the pipeline".
- Clean-code's ownership is contradicted by its own front matter — `catalog_garden_family: architecture-centric-engineering` while `context-perspective: stage`.
- Reuse works at the procedural layer; reuse fails at the conceptual layer. **Every concept overlap in Part I is downstream of the missing conceptual substrate in `common/`.**

The library's structure is more coherent than the concept overlap suggests. The overlap comes from a single missing layer — a shared conceptual reference in `common/` — plus a handful of misplaced classification decisions (bounded-context-map as support, clean-code as ACE family). Fix those and most of Part I's overlaps resolve themselves.

The document remains assessment-only. §7 (concept options) and §16 (structural options) together sketch the full reshape space.
