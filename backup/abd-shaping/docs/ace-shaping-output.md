# Interaction Tree and State Model — Agile Bots 

**Source:** `agile_bots` — bots/, src/, docs/story/story-graph.json; `abd-shaping` skill (currently `solution-shaping`) — AGENTS.md, content/*.md  
**Methodology:** abd-shaping skill (`skills/abd-shaping/` or `skills/solution-shaping/`)  
**Strategy:** `skills/abd-shaping/docs/abd-shaping-strategy.md`  
**Assumption:** Developer initiates; Agile Context Engine responds. AI Agent may invoke via MCP tools.

---

## Interaction Tree

- Epic: **Create Ace-Skill**
     Actor: Developer
     Supporting: AI Agent, Build-ACE skill
     Required State: User has one or more markdown files (or prompts, text) describing how the skill will work
     State Concepts: AceSkill, AssembledAgent, BuildScript, BuildAceSkill
     Initiation: User initiates build abd-skill through AI
     Response: AI uses Build-ACE skill; skill invokes script with params to create scaffolding; AI follows skill guidance to fill content pieces from markdown/prompts/text; if pieces missing/incomplete, AI tells user and user completes; AI reruns build script when all pieces done
     Resulting State: Ace-skill created; ready to register
     
     - Story: **Create scaffolding via script**
          Required State: Build-ACE skill available; user has provided skill name and params
          State Concepts: AceSkill, BuildScript, BuildAceSkill
          Initiation: AI invokes Build-ACE skill with params (skill name, etc.)
          Response: Skill runs script with params; creates abd-skill directory; content/ with core-definitions, intro, output-structure, shaping-process, validation; scripts/ folder; build script
          Resulting State: Ace-skill scaffold created; ready for content fill
          Failure Modes: Template missing; path conflict; invalid abd-skill name; script fails
     - Story: **AI fills content pieces from input**
          Required State: Scaffold created
          State Concepts: AceSkill
          Initiation: AI follows Build-ACE skill guidance
          Response: AI takes markdown file(s), prompts, text passed in; fills core_definition, intro, output_structure, shape, validation per skill guidance
          Resulting State: Content pieces filled (or gaps identified)
          Failure Modes: Input insufficient; skill guidance unclear

     - Story: **User completes missing pieces**
          Required State: AI has identified missing/incomplete pieces
          State Concepts: AceSkill
          Initiation: AI tells user which pieces are missing or incomplete
          Response: User completes those pieces; repeats until all pieces done
          Resulting State: All content pieces complete
          Failure Modes: User does not complete; invalid content format

     - Story: **AI reruns build script**
          Required State: All content pieces complete
          State Concepts: AceSkill, AssembledAgent
          Initiation: AI reruns build script (when necessary)
          Response: Build script assembles core_definition, intro, output_structure, shape, validation into single agent file; produces rules, readme, metadata, skills file
          Resulting State: Assembled agent file ready; abd-skill usable
          Failure Modes: Build script fails; content merge conflict

- Epic: **Initialize Agile Context Engine**
     Actor: Developer
     Supporting: Agile Context Engine
     Required State: Shaping skill installed (abd-shaping)
     State Concepts: AgileContextEngine
     Initiation: Developer chats to AI guided by skill, AI calls skill code
     Response: Engine loads registered skills from JSON; sets workspace when specified; rule sets available
     Resulting State: Engine initialized; skills loaded; rule sets available

     - Story: **Load registered skills and rule sets**
          Required State: —
          State Concepts: AceSkill, RuleSet
          Initiation: —
          Response: Engine loads skills list from JSON; for each skill path, loads rule set (markdown from content/, JSON for scanners); merges into unified rule set per skill
          Resulting State: Available for instruction assembly
          Failure Modes: Malformed JSON config; missing skill path; invalid rule path

- Epic: **Add Context to Memory**
     Actor: Developer
     Supporting: abd-context-to-memory
     Required State: Workspace with content sources
     State Concepts: ContentSource, Markdown, Chunk, Memory, Memories, Workspace
     Initiation: Developer requests add to memory (convert and chunk, ingest, refresh)
     Response: Skill converts each original artifact in full to markdown (alongside original, within workspace); chunks markdown into memory; each file → one memory; memories nested; each memory points to original artifact and markdown converted artifact
     Resulting State: Memories available for future reference

     - Story: **Convert content sources to markdown**
          Required State: Content in supported formats (PDF, PPTX, DOCX, etc.)
          State Concepts: ContentSource, Markdown
          Initiation: Developer requests conversion (or step 1 of pipeline)
          Response: Skill converts original artifact in its entirety to markdown; markdown stored alongside original (same folder)
          Resulting State: Markdown converted artifact available alongside original artifact
          Failure Modes: Unsupported format; conversion fails; path invalid

     - Story: **Chunk markdown**
          Required State: Markdown available
          State Concepts: Markdown, Chunk
          Initiation: Developer requests chunking (or step 2 of pipeline)
          Response: Skill splits markdown by slide, heading, or whole file; writes chunks with source attribution
          Resulting State: Chunks produced; available for reference
          Failure Modes: No markdown found; chunk strategy fails

     - Story: **Sync workspace to memory (convert + copy + chunk)**
          Required State: —
          State Concepts: ContentSource, Markdown, Chunk, Memory, Memories, Workspace
          Initiation: Developer requests sync workspace to memory
          Response: Skill converts each original to markdown in full (alongside original); copies chunks to <workspace>/context-to-memory/memory/; each file → one memory; memories nested; each memory points to original artifact and markdown converted artifact
          Resulting State: Memories populated
          Failure Modes: Workspace missing; copy fails; chunk fails

- Epic: **Use Shape Skill**
     Actor: Developer
     Supporting: Agile Context Engine
     Required State: Engine initialized; context gathered
     State Concepts: Strategy, Slice
     Initiation: Developer invokes shaping (create strategy, generate slice, improve strategy, improve skill)
     Response: Engine loads shaping instructions (from assembled skill content); assembles with context; produces or updates strategy/slice output; or applies strategy corrections to base skill
     Resulting State: Strategy created or updated; slice output produced; strategy improved; or skill improved

     - Story: **Create Shaping Strategy**
          Required State: —
          State Concepts: SourceAnalysis
          Initiation: Developer requests strategy creation
          Response: Engine assembles instructions for create_strategy; caller injects into prompt; AI reads context from paths; produces strategy doc (complexity analysis, epic breakdown, slice order, assumptions); AI validates sections; caller persists to output path in real time during iterations (steps 6–9)
          Resulting State: Ready for approval
          Failure Modes: Memories empty; strategy validation fails; save path invalid
          Steps:
          1. User → AI: Requests strategy creation
          2. AI → Engine: Requests context source paths and instructions for create_strategy
          3. Engine → AI: Returns (1) context source paths, (2) assembled instructions (injected into prompt)
          4. AI: Reads context from returned paths; instructions already in prompt (shaping.process.intro, shaping.strategy.phase, shaping.strategy.criteria, shaping.core.*)
          5. AI: Analyzes source; determines complexity areas in order to determine splitting criteria, slice ordering criteria, depth criteria
          6. AI: Generates initial strategy criteria, scaffold (epic breakdown, assumptions); and slicing order, and validates all sections
          7. AI → User: Presents strategy (content in output path)
          8. User → AI: Reviews and refines
          9. AI: Iterates (5–8 until user satisfied); each iteration validated and persisted to output path
          10. AI → calls engine to persist skill operation "strategy" completed

     - Story: **Generate Slices**
     │    Required State: Strategy approved; slice order defined
     │    State Concepts: InteractionTree, StateModel
     │    Initiation: Developer requests slice (e.g. Slice 1 or "next slice")
     │    Response: Caller injects instructions for generate_slice; AI reads strategy and context; produces 4–7 stories; derives concepts; builds Interaction Tree + State Model; validates; caller persists to output path in real time during iterations; when user feedback implies reusable correction, AI adds DO/DO NOT to strategy (no separate improve_strategy call)
     │    Resulting State: Slice available for review; corrections in strategy when applicable
     │    Failure Modes: Strategy not approved; slice index invalid; output validation fails
     │    Steps:
     │    1. User → AI: generate next slice (e.g. "Slice 1", "next slice")
     │    2. Caller: Injects context paths and instructions for generate_slice into prompt (shaping.process.intro, shaping.strategy.slices.running, shaping.strategy.corrections, shaping.output.*, shaping.validation.*, shaping.core.*, strategy doc path)
     │    3. AI: Reads context from paths; loads strategy doc; instructions already in prompt
     │    4. AI: Determines current slice from strategy order; produces 4–7 stories; derives concepts; builds Interaction Tree + State Model
     │    5. AI: Generates slice output; validates against checklist; caller persists to output path
     │    6. AI → User: Presents slice (content in output path)
     │    7. User → AI: Reviews and refines
     │    8. AI: Iterates (4–7 until user satisfied); each iteration validated and persisted
     │        When user feedback implies reusable correction → AI adds DO/DO NOT to strategy doc (corrections format in prompt; no "go improve strategy" needed)
     │        User may instead: edit strategy markdown directly, or say "rethink slicing/criteria" → Create Strategy flow (new context)
     │    9. User satisfied → next slice (or done)
     │
     ├─ Story: Improve Strategy
     │    Required State: Slice produced; user has corrections
     │    State Concepts: —
     │    Initiation: Developer provides corrections (DO/DO NOT rules)
     │    Response: Caller injects instructions for improve_strategy; AI adds DO/DO NOT to strategy doc per corrections format; caller persists; user may re-run slice (Generate Slices) until approved
     │    Resulting State: Strategy doc updated; slice ready for approval or next slice
     │    Failure Modes: Correction format invalid; rule conflicts with existing
     │    Steps:
     │    1. User → AI: Provides corrections (DO/DO NOT rules) — explicit or implied from slice feedback
     │    2. Caller: Injects instructions for improve_strategy into prompt (shaping.strategy.corrections, correction format)
     │    3. AI: Reads strategy doc; applies correction format (DO/DO NOT, example wrong, example correct)
     │    4. AI: Produces updated strategy doc with new DO/DO NOT block(s)
     │    5. Caller: Persists strategy to output path
     │    6. User: Reviews; decides to re-run slice or proceed to next slice
     │    7. If re-run: Generate Slices flow (with updated strategy in context) — iterate until approved
     │    8. Result: Strategy doc updated; slice ready for approval or next slice
     │
     └─ Story: **Improve Skill**
          Required State: All slices done; strategy doc has accumulated corrections
          State Concepts: —
          Initiation: Developer requests post-shaping review
          Response: AI reviews all corrections in strategy; determines what to change in skill content/rules; promotes rules that apply across domains; updates base skill
          Resulting State: Base skill (content, rules) updated; skill improved
          Failure Modes: Promotion conflicts; invalid content format
```

---
## State Model

Concepts scoped to the smallest subtree where they are used. Each section lists the tree nodes it applies to.

**Concept → Tree mapping**

| Tree node | State concepts |
|-----------|----------------|
| Epic: Create Ace-Skill | AceSkill, AssembledAgent, BuildScript, BuildAceSkill |
| Epic: Initialize Agile Context Engine | AgileContextEngine, AceSkill, RuleSet, Workspace |
| Epic: Add Context to Memory | ContentSource, Markdown, Chunk, Memory, Memories, Workspace |
| Epic: Use Shape Skill | ContextSources, Strategy, Slice, InteractionTree, StateModel |

### Path (Cross-cutting)

**Applies to:** All epics (file paths used throughout). *See `docs/ace-architecture-pattern.md` §1.1.5 for full Path convention.*

| Concept | Properties | Operations |
|---------|------------|------------|
| **Path** | — | Represents file/dir; all path properties return Path, not String. Reuse agile_bots bot_path. |

### AgileContextEngine, AceSkill, RuleSet, Workspace, ArchitectureConstraint

**Applies to:** Epic: Initialize Agile Context Engine (all stories); Epic: Create Ace-Skill (AceSkill shared).

**Object model principle:** Inject dependencies (e.g. Engine) so components can refer to context without passing parameters. Favor properties over getters. Encapsulate over passing parameters.

```
AgileContextEngine
- Path engine_path
     Path to the engine itself
     invariant: agile-context-engine/
- Path config_path
     Path to engine config
     invariant: e.g. conf/abd-config.json; config lives outside any workspace
- AceSkill[] skills
     List of registered abd-skills; each skill gets Engine injected at construction
- Workspace workspace
     Skill space — derived from skill path (parent of .agents/skills or parent of skills)
     invariant: not configurable; always derived from where the skill is deployed
- Path strategy_path
     Path to strategy doc (when exists)
     invariant: from workspace; used by skills for instruction assembly
- Path[] context_paths
     Context source paths for operations
     invariant: from workspace, memories, etc.
- Context context
     Reference to context object below

- AgileContextEngine load(): AgileContextEngine
     Loads JSON config; loads skills; injects self into each skill; each skill loads rule set

Workspace
- Path path
     Folder path (root of project/IDE or subfolder)
     invariant: outputs of engine for skill work here; returns Path, not String
- String name
     Workspace identifier (for output paths)
     invariant: derived from path
```

| Concept | Properties | Operations |
|---------|------------|------------|
| **Workspace** | path (Path), name | — |

```
AceSkill
- Engine engine
     Injected at construction. AceSkill uses it for context (workspace, strategy_path, slice_index, etc.).
- Path path
     Path to skill directory
     invariant: skills/ace-<skill_name>/
- RuleSet rule_set
     RuleSet (markdown + JSON)
     invariant: skills/ace-<skill_name>/rules
- Script[] scripts
     Scripts collection
     invariant: skills/ace-<skill_name>/scripts/
- String core, process, strategy, output, validation
     Content from content/*.md
     invariant: from skills/ace-<skill_name>/content/
- AssembledAgent assembled_agent
     All pieces assembled into single agent file
     invariant: output of build()
- Map<Operation, SectionIds> operation_sections
     operation → section IDs to inject. Keys: create_strategy, generate_slice, improve_strategy, improve_skill.
     invariant: from skill config
- Instructions instructions
     Property. References operation_sections. When assembled for an operation, grabs context from engine (workspace, strategy_path, slice_index) and returns markdown. No context parameter — pulls from engine.
- AceSkill build(path_to_markdown): AceSkill
     Assembles pieces; produces assembled agent file; creates JSON config scaffold
- Map<Operation, SectionIds> operation_sections
     From AceSkill.operation_sections
- String display_content(operation)
     Assembles sections for operation; injects context from engine; returns markdown. No context parameter.
- String[] sections_included
     Section IDs assembled (for debugging)


RuleSet
- Path[] markdown_paths
     Path to each content file
     invariant: Path objects for shaping-core.md, shaping-process.md, shaping-strategy.md, shaping-output.md, shaping-validation.md
     Specific markdown file eg
     - Object scanner_rules
          JSON for scanners
          invariant: from skills/ace-<skill_name>/rules
- String merged_content
     Unified content for instruction assembly
     invariant: markdown from all markdown_paths concatenated with scanner_rules
- RuleSet load(path): RuleSet
     AceSkill path
     Reads markdown from content/; loads JSON from rules

ArchitectureConstraint
- String pattern
     e.g. "must use X", "must run in Y time"
- String scope
     Scope of constraint
     invariant: Epic, Story, or global
```

### AssembledAgent, BuildScript

**Applies to:** Epic: Create Ace-Skill — Story: Create scaffolding via script, Story: AI reruns build script.

*AceSkill is defined above (Initialize). Create Skill adds:*

```
AssembledAgent
- Path path
     Path to assembled output
     invariant: skills/ace-<skill_name>/AGENTS.md (or assembled agent file under skill); returns Path, not String
- String content
     Merged content for agent consumption
     invariant: shaping-core + shaping-process + shaping-strategy + shaping-output + shaping-validation assembled in order

BuildScript
- Path path
     Path to build script
     invariant: skills/ace-<skill_name>/scripts/build.py; returns Path, not String
- BuildScript run(): AssembledAgent
     AceSkill path
     Assembles content files; writes assembled agent file
```

### Add Context to Memory — ContentSource, Markdown, Chunk, Memory, Memories, Workspace

**Applies to:** Epic: Add Context to Memory (all stories: Convert content sources to markdown, Chunk markdown, Sync workspace to memory).

**abd-context-to-memory skill** defines what our context sources are, converts them to markdown, chunks them, and puts them in memories so we can refer to them later.

```
ContentSource
- Path path
     Path to source file or folder
     invariant: supported format (PDF, PPTX, DOCX, XLSX, HTML, etc.)
- String format
     File extension / type
- Markdown convert(): Markdown
     Converts to markdown in place

Markdown
- Path path
     Path to .md file
     invariant: alongside original artifact (same folder as source)
- String content
     Full content converted to markdown
     invariant: includes <!-- Source: path | file://url --> when converted
- String artifact_ref
     Original artifact this markdown was converted from
     invariant: path to PDF, PPTX, DOCX, etc.
- Chunk[] chunk(): Chunk[]
     Splits by slide, heading, or whole file

Chunk
- Path path
     Path to chunk file
     invariant: <workspace>/context-to-memory/memory/<folder>/<stem>__<label>.md
- String content
     Chunk content
     invariant: includes <!-- Source: path | file://url --> for attribution
- String source_ref
     Original source path and location (slide/section)
     invariant: <!-- Source: path, location | url -->

Memory
- Path path
     Folder in <workspace>/context-to-memory/memory/
     invariant: each folder = one memory
- Chunk[] chunks
     Chunked markdown for one specific file
     invariant: all chunks from same original artifact
- String artifact_ref
     Original artifact (source file: PDF, PPTX, DOCX, etc.)
     invariant: path or file://url to the file that was added
- String markdown_ref
     Markdown converted artifact (full file, alongside original)
     invariant: same folder as original; entire content converted to markdown
- Memory[] children
     Nested memories
     invariant: memories are nested (folder hierarchy)

Memories
- Path root_path
     <workspace>/context-to-memory/memory/ subfolder
     invariant: under workspace
- Memory[] memories
     All memory folders (nested)
- Chunk[] refer(): Chunk[]
     Chunks available for agents/context to find

Workspace
- Path path
     Folder path (root of project/IDE or subfolder)
     invariant: everything gets packed into this workspace; returns Path, not String
- String name
     Workspace identifier (for output paths)
     invariant: derived from path
```

| Concept | Properties | Operations |
|---------|------------|------------|
| **ContentSource** | path (Path), format | convert(): Markdown |
| **Markdown** | path (Path), content, artifact_ref | chunk(): Chunk[] |
| **Chunk** | path (Path), content, source_ref | — |
| **Memory** | path (Path), chunks, artifact_ref, markdown_ref, children | — |
| **Memories** | root_path (Path), memories | refer(): Chunk[] |
| **Workspace** | path (Path), name | — |

### Use Shape Skill — ContextSources, Strategy, Slice

**Applies to:** Epic: Use Shape Skill (all stories: Create Shaping Strategy, Generate Slices, Improve Strategy, Improve Skill). Shaping gets context from Memories — not from raw paths.

```
ContextSources
- Memories memories
     Populated by abd-context-to-memory (defines context sources → convert → markdown → chunk → memories)
     invariant: each folder in memory/ = one Memory; each Memory = chunked markdown for one file; points to original artifact and markdown converted artifact (alongside original); memories nested
- Workspace workspace
     Folder containing project; all skill operations happen in this context
     invariant: likely at root of project/IDE; can be subfolder; everything packed into workspace
- Strategy strategy
     When we have one (for slice runs)
     invariant: required for Generate Slice; optional for Create Strategy
- RuleSet rule_set
     From abd-skill (shaping instructions)
- ContextSources gather(content_sources, workspace, strategy): ContextSources
     ContentSources, Workspace, Strategy
     Populates memory (convert, chunk, sync via abd-context-to-memory); refers to memories for chunks; assembles with workspace, strategy, rule_set per shaping phase (strategy vs slice)

Strategy (Markdown Document)
     
- Path path
     Path to strategy document
     invariant: <workspace>/shaping/strategy.md; returns Path, not String
- SourceAnalysis source_analysis
     Semantic structure within the markdown
- InteractionTree
- StateModel
- Slice[] slices
     Semantic structure within the markdown

Slice
- Number index
     Slice order (1, 2, 3, …)
     invariant: positive integer
- String theme
     Slice theme (e.g. de-risk foundation, structure decision)
- Story[] stories
     Story
     invariant: 4–7 stories per slice
- Slice produce(strategy): InteractionTree, StateModel
     Strategy
     Produces 4–7 stories; derives concepts; outputs tree + model
```

**Instruction injection (what to inject, when):** See `docs/ace-instruction-injection-analysis.md`. Summary:

| Operation | Inject |
|-----------|--------|
| create_strategy | intro.process, shaping.strategy_phase, shaping.strategy_criteria, core.interaction, core.state_concept |
| generate_slice | intro.process, shaping.running_slices, output.interaction_tree, output.state_model, validation.checklist, core.*, strategy doc |
| improve_skill | shaping.corrections, validation.checklist (correction format) |

| Concept | Properties | Operations |
|---------|------------|------------|
| **Strategy** | path (Path), source_analysis, epic_breakdown, slice_order, assumptions | — (represented as markdown; AI reads/writes) |
| **Slice** | index, theme, stories | produce(Strategy): InteractionTree, StateModel |
| **InteractionTree** | Epic[] hierarchy | validate(): boolean |
| **StateModel** | Concept[] concepts | validate(): boolean |

---

## D) abd-context-to-memory (Embedded)

**Source:** `abd-context-to-memory` skill — SKILL.md, scripts  
**Methodology:** abd-shaping skill  
**Domain:** abd-context-to-memory — content sources → markdown → chunks → refer for future use  
**Assumption:** Developer initiates; abd-context-to-memory responds. Integration (e.g. Vesta 7) is separate.

### D.1) Interaction Tree (abd-context-to-memory)

*(See Epic: Add Context to Memory in main Interaction Tree above.)*

### D.2) State Model (abd-context-to-memory)

*(See main State Model — "Add Context to Memory — ContentSource, Markdown, Chunk, Memory, Memories, Workspace" section above; inline concepts table follows that section.)*

### D.3) Notes (abd-context-to-memory)

- **Very specific skill:** abd-context-to-memory does one thing: take content → convert → chunk → memories. Does not need to change as we create new skills.
- **Memories structure:** Each folder in the memory subfolder = one Memory. A Memory = chunked markdown for one specific file. Memories are nested. Each memory points to (1) original artifact and (2) markdown converted artifact.
- **Conversion in place:** The original artifact is converted in its entirety to markdown; the markdown file is stored alongside the original (same folder). Chunks are derived from that markdown and stored in memory.
- **Triad:** Memory ↔ Original Artifact ↔ Markdown Converted Artifact. Each memory links to both: the source file (artifact_ref) and the full markdown version (markdown_ref, alongside original).
- **Chunking strategy:** Slide decks → one chunk per slide; docs >200 lines → split at # or ##; small files → single chunk.
- **Source attribution:** Each chunk includes `<!-- Source: path | file://url -->` for traceability.
- **Integration:** How chunks are added to context (e.g. Vesta 7) is separate; this skill produces referable chunks.
- **Workspace:** All skill operations happen in the context of a workspace — a folder (likely at root of project/IDE, or a subfolder). Everything gets packed into this workspace. Workspace path in engine config (engine knows where to find it).
- **Skill outputs:** Always at <workspace>/<output-folder>/ where output-folder = skill name with `ace-` stripped (e.g. shaping, context-to-memory).

---

## Notes (Slice 1)

**Note → Tree mapping:** Each note applies to the listed tree nodes.

| Note | Applies to |
|------|------------|
| Object-oriented model, Ace-skill, Rule dual representation, Create Skill | Epic: Create Ace-Skill; Epic: Initialize Agile Context Engine |
| Python/JSON hybrid, Architecture-pattern constraints | Epic: Initialize Agile Context Engine |
| Workspace, Skill outputs | All epics (Initialize sets workspace; Add Context and Use Shape run in workspace) |
| Context from memories, not raw paths | Epic: Add Context to Memory; Epic: Use Shape Skill |
| Path concept | All epics (cross-cutting) |
| Subsequent slices | Future slices |

- **Object-oriented model:** AgileContextEngine → AceSkill[] (not EngineConfig). Each abd-skill has path, RuleSet (markdown + JSON), hard-coded properties (core_definition, intro, output_structure, shape, validation), assembled agent file, build method.
- **Ace-skill:** Shaping skill is `abd-shaping` (currently `solution-shaping`). Every abd-skill has the same five content pieces: core-definitions, intro, output-structure, shaping-process, validation.
- **Rule dual representation:** Ace-skill–rule relationship lives in (1) markdown (content files) and (2) JSON (for scanners).
- **Create Skill:** User creates markdown(s) describing intent; initiates build abd-skill through AI. AI uses Build-ACE skill; skill runs script with params to create scaffolding; AI fills content pieces from markdown/prompts/text; if incomplete, user completes; AI reruns build script when done.
- **Python/JSON hybrid:** Config lists skill paths in JSON; Python (or CLI) loads skills and assembles; instruction injection uses merged content.
- **Architecture-pattern constraints:** Constraints (must use X, must run in Y time) are stored in config and applied when validating shaping output.
- **Workspace:** Skill space is wherever you deploy the skill — parent of `.agents/skills`. Engine derives it from the skill path; no config needed. All outputs go under that path (e.g. `shaping/`, `context-to-memory/`).
- **Skill outputs:** Always at <workspace>/<output-folder>/ where output-folder = skill name with `ace-` stripped. Fixed convention; never changes.
- **Context from memories, not raw paths:** Add Context to Memory populates memory (convert, chunk, sync via abd-context-to-memory). Use Shape Skill gets context from those memories — not from raw file paths. Context comes from Memories (memory/ subfolder under workspace). Each folder = one Memory = chunked markdown for one file. Each memory points to (1) original artifact and (2) markdown converted artifact (full conversion, alongside original). Memories are nested.
- **Subsequent slices:** Slice 2+ will add one-skill-vs-many, slice-as-run semantics, instruction injection, CLI, hierarchy scoping, panel, impacts.
- **Path concept:** All file-returning properties return Path objects (not strings). Path handles OS separators and centralizes path logic. Reuse `agile_bots/src/bot_path` (BotPath, StoryGraphPaths) in its entirety — do not reimplement.
