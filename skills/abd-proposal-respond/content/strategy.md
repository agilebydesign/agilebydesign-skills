# Strategy Phase

<!-- section: proposal.strategy.starting -->
## Common Response Instructions (Starting Template)

Include in `response/strategy.md` as baseline. Adapt per RFP.

**Structure:** Lead paragraph → bulleted list with **Bold labels** → source references.

**Lead paragraph — DO:** Articulate outcomes in the client's language. "Our firm would aim to accomplish [concrete outcomes]." "We will achieve these outcomes through:"

**Lead paragraph — DON'T:** Do not restate the question generically.

**Bullet prose — DO:** Explain method and mechanism. 2–3 substantive sentences per bullet.

**Bullet prose — DON'T:** Do not use "We will [verb]... to achieve [outcome]" for every bullet. Explain *how*.

**Bullet labels — DO:** Use approach/method names. Name what we do, not the output.

**Tailoring — DO:** Connect each bullet to the specific question. Use the question's language.

See `rules/response-format.md` for full DO/DO NOT. Add project-specific corrections as you iterate.

<!-- section: proposal.strategy.phase -->
1. **Analyze** the proposal sources — question coverage, priorities, assumptions.
2. **Present** the strategy — which questions, in what order, format guidance.
3. **Validate** — User reviews; refine until approved.
4. **Save** to `response/strategy.md`.

<!-- section: proposal.strategy.criteria -->
## Strategy Criteria

**Tone** — Voice, formality, perspective (e.g. aspirational, direct, collaborative).

**Level of detail** — How deep per question (full answer, draft, placeholder; technical vs executive).

**Audience** — Who reads this (evaluators, technical reviewers, executives); tailor accordingly.

**References or examples to speak to** — Which sources, case studies, or prior work to cite; what evidence to invoke.

<!-- section: proposal.strategy.slices.running -->
## Running Batches

1. **Answer 3–5 questions** — User reviews and corrects.
2. **Corrections → strategy** — Add DO/DO NOT with wrong/correct examples. Re-run until approved.
3. **Proceed** — Next batch or expand scope.
4. **Correct** — "Correct" means correct the strategy; do not just fix the answer in place.

<!-- section: proposal.strategy.corrections -->
## Corrections Format

Each **DO** or **DO NOT** must include:
- The rule
- **Example (wrong):** What was done incorrectly
- **Example (correct):** What it should be

Re-run until the user approves.

**Use memory RAG** — Run `search_memory "<query>"` and cite retrieved chunks when answering.

**Optional: index our work** — After each batch (or when strategy changes), run `index_memory --path response/` so subsequent answers can reference prior work and corrections.

<!-- section: proposal.strategy.accelerators -->
## Accelerators (Lettered Appendix)

Answers may refer to accelerators — typically `*See Appendix X (Full Name)*` at the end of bullets. The author (or AI) may suggest an accelerator when a framework, method, or approach warrants a slide appendix.

**Define and accumulate in real time** — When writing or revising answers, define each referenced accelerator (appendix letter, framework name) and accumulate it in the **Accelerator Table** (e.g. `Accelerator Table.md`). Add or update a row with slide file, slide numbers, and URL. The table grows as answers are written. Keep URLs in the table for now.

**Table format:**
| Appendix | Framework Name | Slide File | Slide Numbers | Url |
|----------|----------------|------------|---------------|-----|
| **A** | Lean Change | Lean Change Approach Slides.pptx | **1, 2** | [Link](url) |

**When done** — Run `build_appendix_deck.py` (or project-specific script) to assemble the appendix deck from the table. Default output: derived from the table md name (e.g. `Accelerator Table.md` → `Appendix_Accelerators.pptx`). Override with `--output <path>`.
