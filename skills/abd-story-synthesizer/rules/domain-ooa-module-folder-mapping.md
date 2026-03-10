---
title: State Model — Module Folder Mapping
impact: LOW
tags: []
scanner: domain_module_mapping
---

## When Mapping to Code

**DO** when mapping to code, use Module = folder path in dot notation (e.g. `actions.render`, `repl_cli.cli_bot`).

**DO NOT** use `src/` prefix or slashes — use dots for nesting (e.g. `repl_cli.cli_bot`, not `src/repl_cli` or `repl_cli/cli_bot`).

**Note:** Applies when the synthesizer output is mapped to existing or planned code structure. Synthesizer may run before code exists — rule is optional when applicable.
