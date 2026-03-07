# Interaction Tree and State Model — Ace Commit Message

**Source:** `abd-commit-msg` skill — AGENTS.md, content/*.md  
**Methodology:** abd-commit-msg skill (`skills/abd-commit-msg/`)  
**Assumption:** No story_graph. Scope derived from conversation, changed files, and persisted state.

---

## Interaction Tree

- Epic: **Generate Commit Message**
     Actor: Developer
     Supporting: AI Agent, abd-commit-msg skill
     Required State: User requests commit (/commit or "commit"); no pending primary instructions
     State Concepts: CommitScope, Behavior, Action, CommitMessage, LastCommitScope
     Initiation: User types /commit or requests a commit
     Response: AI reads context files; infers behavior from changed files; infers scope from conversation or changed files when scope files empty; generates message; executes git commit
     Resulting State: Commit created; scope persisted for future commits
     Failure Modes: User's primary instructions not complete; no changed files; git fails

     - Story: **Read context and update scope**
          Required State: Workspace root has last_commit_scope.json, scope.json, optionally behavior_action_state.json
          State Concepts: LastCommitScope, CommitScope
          Initiation: Commit process starts
          Response: Read last_commit_scope.json (preferred); if scope.json has non-empty value, save to last_commit_scope.json; if user said "scope is X", save immediately
          Resulting State: Scope available for message generation
          Failure Modes: Both files empty → infer scope

     - Story: **Infer behavior from changed files**
          Required State: Git status/diff available
          State Concepts: Behavior
          Initiation: Before generating message
          Response: Check git status and git diff; match changed content to behavior (code, tests, shape, prioritization, exploration, scenarios, domain, design); override behavior_action_state.json when changed files clearly match
          Resulting State: Behavior determined
          Failure Modes: No clear match → use behavior_action_state.json when present

     - Story: **Infer scope when scope files empty**
          Required State: last_commit_scope.json and scope.json both empty or missing
          State Concepts: CommitScope
          Initiation: Scope needed for message
          Response: Infer from conversation first (what did user ask? what was discussed?); then from changed files (paths, directory names, document types); save to last_commit_scope.json; confirm to user
          Resulting State: Scope inferred and persisted
          Failure Modes: Nothing specific found → use generic "Update project artifacts"

     - Story: **Generate and execute commit**
          Required State: Behavior and scope determined
          State Concepts: CommitMessage
          Initiation: Message generation
          Response: Format {behavior}.{action}: {description}; use present tense; reference scope; execute git add -A; git commit -m "message"; never add Co-authored-by
          Resulting State: Commit created
          Failure Modes: Git add/commit fails; message too long

---

## State Model

### CommitScope

- **Sources (priority):** last_commit_scope.json, scope.json, conversation, changed files
- **Granularity:** Feature area, document type, path-derived, generic
- **No story_graph:** Scope is NOT epic/sub-epic/story from story-graph.json

### LastCommitScope

- **Path:** workspace root / last_commit_scope.json
- **Format:** `{"value": ["Scope1", "Scope2"], "timestamp": "..."}`
- **Updated when:** scope.json changes; user override; scope inferred

### Behavior

- **Inferred from:** Changed files (git status, git diff)
- **Values:** code, tests, shape, prioritization, exploration, scenarios, domain, design, walkthrough
- **Override:** behavior_action_state.json when changed files don't clearly match

### CommitMessage

- **Format:** `{behavior}.{action}: {meaningful description based on scope}`
- **Constraints:** Present tense; under 80 chars; no Co-authored-by
