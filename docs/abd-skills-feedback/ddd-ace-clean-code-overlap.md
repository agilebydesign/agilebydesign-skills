# DDD ⇄ Architecture ⇄ Clean Code — Overlap & Gaps Assessment

**Scope of this note.** A working assessment of where the three engineering-facing skill families overlap uncomfortably, where they hand off cleanly, and where the concepts we actually care about (OOAD, modularization, seams, deep modules, framework mechanisms, domain focus) live — or don't yet live — in the current library.

> **Reading note.** Written in bullet form rather than wide tables so it word-wraps on mobile (GitHub mobile scrolls tables sideways without wrapping). Section §2's concept map is the part that most benefits from this layout.

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
