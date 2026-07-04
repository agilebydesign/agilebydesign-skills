# DDD / Architecture / Clean Code — What's Actually Broken and What to Do

An evidence-first read of the three engineering-facing skill families — rules, templates, references, concepts — with the specific files and lines that prove each finding. Then one recommendation with a concrete execution plan.

Everything below is checkable with `grep` and `diff` against the current repo.

**Scope of the read**

- Every `rules/*.md` in `abd-clean-code`, all five ACE skills, and all five DDD skills.
- Every `templates/*` in the same skills.
- The concept references: `stages/engineering/abd-clean-code/reference/concepts.md`, `practices/domain-driven-design/reference/oo-concepts.md`, `practices/domain-driven-design/skills/abd-domain-model/reference/concepts.md`, `practices/architecture-centric-engineering/reference/architecture-context-model.md`, `practices/architecture-centric-engineering/reference/architecture-mechanism.md`, `practices/architecture-centric-engineering/skills/abd-architecture-specification/reference/concepts.md`.

---

## Six concrete findings

### F1 — Nine rule filenames are duplicated between `abd-domain-model` and `abd-domain-specification`, and every one of them has drifted

Filenames present in **both** `practices/domain-driven-design/skills/abd-domain-model/rules/` and `practices/domain-driven-design/skills/abd-domain-specification/rules/`:

- `all-collaborators-accounted-for.md`
- `dependency-magnet-split-concerns.md`
- `explicit-chain-of-responsibility.md`
- `extract-complex-logic-to-named-operation.md`
- `invariants-from-business-logic.md`
- `name-from-invariant.md`
- `receiver-not-responsible-for-receiving.md`
- `state-marker-correct.md`
- `subtype-uses-child-parent.md`

Running `diff -q` on each pair shows **all nine files differ**. Not one is a shared file linked from both skills; each skill maintains its own copy.

Concrete example — `dependency-magnet-split-concerns.md`:

- **In `abd-domain-model`**: the rule threshold is *"no more than 5–7 distinct collaborator types across its methods"* and the anti-example is a class called **`BoardManager`** with eight collaborators.
- **In `abd-domain-specification`**: the rule threshold is gone — the criterion is *"properties, operations, and typed relationships span multiple unrelated business concerns"* and the anti-example is a class exposing *"tax calculation, email dispatch, inventory validation, and PDF generation"*.

Same rule name, same intent (split god classes), different criterion, different example. Two separate copies drifting.

**Consequence.** A scanner or reviewer using domain-model's file will accept a 5-collaborator class; the same class run through domain-specification's file will be judged by an entirely different criterion ("business concerns", no count). The nine drifted files quietly encode different definitions of the same nine rules.

### F2 — The single-responsibility rule is authored four times across the three families

Same rule, four homes, no cross-link:

- `practices/domain-driven-design/skills/abd-domain-model/rules/dependency-magnet-split-concerns.md` — counts collaborators (≤ 5–7); example: `BoardManager`.
- `practices/domain-driven-design/skills/abd-domain-specification/rules/dependency-magnet-split-concerns.md` — checks "unrelated business concerns"; example: tax + email + inventory + PDF.
- `practices/architecture-centric-engineering/skills/abd-architecture-specification/rules/package-surface-is-cohesive.md` — checks "operations share one subject"; example: a `Utils` package with `formatDate`, `validateEmail`, `parseJWT`, `retryWithBackoff`, `escapeHtml`.
- `stages/engineering/abd-clean-code/rules/keep-classes-single-responsibility.md` — checks "one reason to change"; example: an `Invoice` class that calculates, persists, notifies, and formats PDF.

Four rule files. Four different check criteria. Four different examples. Zero cross-references between them.

**Consequence.** A code file has to satisfy all four independently. Nothing tells the reader they are the same principle at three scales. Nothing tells the author which of the four to update when the shared idea evolves.

### F3 — DDD says "no stereotypes"; ACE's mechanism template requires them

Direct contradiction, in the same repo, both files owned by the library:

- `practices/domain-driven-design/skills/abd-domain-model/reference/concepts.md` § *What this format omits*, line 84:

  > **No `<< stereotypes >>`** — no Entity, ValueObject, Service markers.

- `practices/architecture-centric-engineering/skills/abd-architecture-specification/templates/mechanism-context.md`, § *Class Specification*, line 108:

  ```
  ## {{Class1Name}}  << {{Stereotype}} >>
  ```

DDD's own concept file forbids the exact notation ACE's own template demands. A `Class Specification` block in an ACE mechanism-context file will fail DDD's rule, and vice versa. Neither file acknowledges the other exists.

**Consequence.** A class documented in an ACE mechanism-tier context file cannot be lifted into DDD's domain model without stripping stereotypes; a class authored in DDD's domain model cannot be pasted into an ACE class-spec block without adding stereotypes. Every crossover requires manual reformatting.

### F4 — Three different class-notation formats for the same modelling task

Same task (spec-fidelity typed class), three notations:

- **DDD `abd-domain-model`** — `practices/domain-driven-design/skills/abd-domain-model/reference/concepts.md` — `### **ClassName**` heading, `ClassName(Type, Type)` constructor line, `------` (six dashes) property separator, `propertyName: Type` properties, `----` (four dashes) method separator, `methodName(Type): ReturnType` methods, `-` prefix for private.
- **DDD `abd-domain-specification`** — `templates/domain-specification-scaffold.md` and the `.py` / `.ts` / `.java` templates — adds `@stereotype`, `@initialisation`, `@invariant`, `@interaction` markers **on top of** the model format.
- **ACE `abd-architecture-specification`** — `templates/mechanism-context.md` § Class Specification — `## ClassName << Stereotype >>`, `Initialisation: {when and how}`, `------`, `+` public / `-` private visibility, `Interaction:` blocks inside operations.

Compare visibility markers alone: DDD says "`-` for private only, no prefix for public"; ACE says "`+` public, `-` private". Two different visibility conventions for the same concept.

**Consequence.** A domain concept modelled once for the business (DDD spec) has to be re-modelled in a different notation for its architectural placement (ACE mechanism context). Two independently authored representations of the same class, kept in sync manually.

### F5 — `clean-code.py` and `domain-model.py` templates overlap in scope, with no compositional contract

Both templates ship at `templates/*.py` and produce Python domain modules:

- `stages/engineering/abd-clean-code/templates/clean-code.py` — 250 lines. Contains **concrete** `Product`, `LineItem`, `Cart`, `Order`, `User` classes with `__init__`, `@property`, methods, `_private` helpers, `EmptyCartError` / `OrderAlreadyConfirmedError` domain exceptions, `TAX_RATE` / `MAX_LOYALTY_DISCOUNT` / `LOYALTY_THRESHOLD` constants. Fully worked commerce example.
- `practices/domain-driven-design/skills/abd-domain-model/templates/domain-model.py` — 81 lines. Contains **abstract** `KaName(ABC)` with `@abstractmethod` operations, typed properties, one subtype `EnterpriseKaName`. Placeholder file for one Key Abstraction.

The DDD skill (`abd-domain-code`) says it delegates production code to `abd-clean-code`. But the two templates authored under those skills are **not composed** — clean-code.py invents its own commerce entities (Cart, Order) rather than showing how to fill an abstract KaName from domain-model.py with concrete methods. A user reading both templates has no contract for how one becomes the other.

**Consequence.** Clean-code's template restates domain-modelling decisions (what classes exist, what they own, what exceptions they raise) that DDD's `abd-domain-model` is the source of truth for. The hand-off promised in prose is not embodied in the template.

### F6 — DDD's own anti-example violates clean-code's own rule

- `stages/engineering/abd-clean-code/rules/use-domain-language.md`, line 40:

  > Use generic class names: Manager, Handler, Helper, Processor, Util.

  Anti-example: `class Manager:` and `class Handler`.

- `practices/domain-driven-design/skills/abd-domain-model/rules/dependency-magnet-split-concerns.md`, lines 38–55:

  > `### **BoardManager** ...` — the anti-example class name is literally **`BoardManager`**.

DDD's authors reached for the exact class name pattern that clean-code's rule forbids, in a rule about splitting classes. Both files are correct on their own terms. Together they demonstrate that the two skills are not aware of each other's rule content.

**Consequence.** More striking as evidence than as a bug — but the two rule files are shipped in the same skill package tree and never see each other, which is why the drift happens.

---

## The single root cause

Every finding above is the same problem in a different guise: **there is no library-level authoring of OOAD**. Class-scale design rules (SRP, cohesion, encapsulation, DI, no-generic-names, no-god-class), class-scale notation (properties, methods, visibility, stereotypes, invariants), and class-scale templates are authored **per skill**, not per library. Each skill drifts because there is no shared source.

- DDD authored an OO reference (`oo-concepts.md`) but only wired it into its own skills.
- ACE authored its own class-spec notation in a template and forgot the OO reference existed.
- Clean-code authored its own class-level rules with its own examples and its own vocabulary.
- Within DDD, `abd-domain-model` and `abd-domain-specification` authored parallel copies of the same nine rules and let them drift.

Everything in F1–F6 dissolves the moment class-scale content has one authoring site the four skills all read from.

---

## Recommendation — one move, three commits

Extract the class-scale substrate to a shared home. Delete or link the duplicates. Fix the notation contradiction in the same pass. That's it.

### Commit 1 — Create the shared substrate

Create `common/reference/class-design.md`. Populate it with the material that is currently authored four times:

- **Naming** — no `Manager` / `Handler` / `Helper` / `Processor` / `Util`. Names come from the domain. (Lifted from clean-code `use-domain-language.md`.)
- **Cohesion / SRP** — one reason to change; operations share one subject; collaborators bounded. Merge the four F2 files into one rule with three-scale examples (class / package / mechanism).
- **Encapsulation** — private state; expose behaviour. (Lifted from clean-code `enforce-encapsulation.md`.)
- **Explicit DI** — constructor injection, no hidden globals. (Lifted from clean-code `use-explicit-dependencies.md`.)
- **Class notation** — one canonical block format for typed classes. Decide the visibility convention (`+`/`-` or `-` only) and the stereotype convention (permitted or forbidden) once. Every downstream template inherits.

Create `common/reference/class-block-format.md` as the single canonical notation reference. Reconcile the DDD/ACE contradiction here — pick one visibility convention, pick one stereotype rule.

### Commit 2 — Rewire the four skills to cite it

- `stages/engineering/abd-clean-code/rules/keep-classes-single-responsibility.md` — replace body with a one-paragraph class-scale specialisation, cite `common/reference/class-design.md`.
- `stages/engineering/abd-clean-code/rules/use-domain-language.md` — same treatment.
- `stages/engineering/abd-clean-code/rules/enforce-encapsulation.md` — same.
- `stages/engineering/abd-clean-code/rules/use-explicit-dependencies.md` — same.
- `practices/architecture-centric-engineering/skills/abd-architecture-specification/rules/package-surface-is-cohesive.md` — replace body with a one-paragraph package-scale specialisation of the shared cohesion rule; cite.
- `practices/architecture-centric-engineering/skills/abd-architecture-specification/templates/mechanism-context.md` § Class Specification — replace the inline notation with a link to `common/reference/class-block-format.md`.
- `practices/domain-driven-design/skills/abd-domain-model/rules/dependency-magnet-split-concerns.md` and `practices/domain-driven-design/skills/abd-domain-specification/rules/dependency-magnet-split-concerns.md` — collapse to one file (in the shared home) with two thin domain-scale specialisations; the model skill and spec skill both cite it.
- `practices/domain-driven-design/skills/abd-domain-model/reference/concepts.md` — update § *What this format omits* to cite `common/reference/class-block-format.md` for the visibility and stereotype conventions instead of restating them.

### Commit 3 — Collapse the intra-DDD duplicated rules

For each of the nine F1 filenames present in both `abd-domain-model/rules/` and `abd-domain-specification/rules/`:

1. Pick one canonical text (the stronger / more current of the two — or the merged synthesis).
2. Delete the copy from `abd-domain-specification/rules/`.
3. In `abd-domain-specification/SKILL.md` § Read, link to the domain-model copy explicitly, or promote the rule to `practices/domain-driven-design/reference/` if it applies to both fidelities.

The nine files affected are listed in F1. Two touches per file (delete + add link) = eighteen mechanical edits.

---

## What this recommendation does NOT do

- It does not touch the perspective × fidelity taxonomy. The library's structural model is fine.
- It does not merge DDD and ACE. They stay as separate perspective-owning practices.
- It does not touch clean-code's placement under `stages/engineering/`. Clean-code stays a stage skill.
- It does not resolve the `abd-bounded-context-map` support-vs-pipeline question or the "domain framework" gap. Those are real issues but they are not the source of the concrete duplication problem — they are separate calls.

The move fixes the six findings above, all of which come from the same missing shared substrate. It does not attempt a wider reshape.

---

## What the finished state looks like

- **One rule file per class-scale rule**, in `common/reference/` or as a shared file cited by every consuming skill.
- **One class-block notation**, in `common/reference/class-block-format.md`, used by DDD model, DDD spec, and ACE mechanism-context alike.
- **Nine deleted DDD rule copies**; the spec skill inherits from the model skill via link, not copy.
- **The DDD-vs-ACE stereotype contradiction resolved** — one convention wins.
- Clean-code's rule files shrink to short specialisations that cite the shared substrate. Its concepts page and templates stay as the how-to-write-code teaching layer, which is genuinely clean-code's own scope.

Estimated size of the change: one new folder (`common/reference/class-design.md` + `class-block-format.md`), ~25 file edits, ~9 file deletes.

---

## What was cut

Earlier revisions of this doc contained (a) a concept-map tour of every concept in the three families and (b) a taxonomy tour of the perspective × fidelity model, the four structural layers, and eleven reshape options. Both restated things you had already sketched in the original prompt. They are removed. Git history has them if referenced.
