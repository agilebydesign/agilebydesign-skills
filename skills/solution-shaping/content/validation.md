# Validation Pass

After generating interactions and concepts, verify:

**Interactions**
- [ ] Each interaction has Actor, Supporting, Initiation, Response, Required State, State Concepts, Resulting State
- [ ] Response = behavior only (no state language); Resulting State = outcome only (no action language); no overlap between them
- [ ] Each interaction touches at least one state concept
- [ ] Hierarchy respected: Epic → Epic → Story → Scenario → Step
- [ ] **Sequential order:** Required state creators appear before consumers; tree follows actual flow of the system

**Required State**
- [ ] Shared required state on parent only; children list only new or specialized state
- [ ] Required state comprehensive — data exists, state has right value, relationships in place, dependent concepts populated
- [ ] No child-level detail leaked into parent nodes

**Resulting State**
- [ ] Same inheritance rules as Required State; common state on parent, child-specific detail on child

**Failure Modes**
- [ ] Max 3 per interaction
- [ ] From domain rules, state conditions, or authorization only (no infrastructure or technical failures)

**Concepts**
- [ ] Each concept scoped to Epic/Story that owns it (lowest common ancestor of all interactions that use it)
- [ ] Invariants under specific property/operation when they apply to that property/operation only

**Content**
- [ ] No implementation details (APIs, services, databases, UI components, code)
- [ ] No speculation beyond the provided material
- [ ] Everything at logical/domain level
- [ ] Assumptions stated when unclear (no invented mechanics)
- [ ] **Granularity:** Sufficient stories to capture rule detail; no collapsing of large sections into single stories
