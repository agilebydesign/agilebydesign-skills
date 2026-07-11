# AGENTS.md

## Cursor Cloud specific instructions

`abd-skills` ("The ABD Foundry") is primarily a content/skills library (Markdown skill
definitions) plus scattered Python tooling and one embedded MERN sub-app. It is not a
single deployable service. The VM has Python 3.12 and Node 22. The cloud update script
installs `pytest`/`pyyaml`/`watchdog` (user site) and the kanban app's npm deps.

### Runnable app: ABD Delivery Agent Kanban (read-only board viewer)
Located at `practices/kanban/apps/abd-delivery-agent-kanban`.
- `npm run dev` runs the API (`http://localhost:3001`, health `GET /health`) and the Vite
  client (`http://localhost:3000`, board route `/board`).
- Caveat: the API defaults to port 3001, which COLLIDES with the `abd-answers` app. Run
  only one at a time (or set `PORT` for the API — but the client's Vite proxy is hardcoded
  to `127.0.0.1:3001`).
- Caveat: `config.default.json` and `KanbanBoard.DEFAULT_PLANNING_ROOT` point at a Windows
  path, so the "Use stubs" button fails on Linux. To load a board, paste a planning-root
  path into the "Planning folder" input and click "Connect" (or set `VITE_PLANNING_ROOT`).
  A bundled Linux-valid fixture is:
  `practices/kanban/apps/abd-delivery-agent-kanban/tests/e2e/data/pawplace-stubs/docs/planning`

### Tests / lint
- Python tests run with `python3 -m pytest` (the `pytest` console script is in
  `~/.local/bin`, which may not be on PATH). Target real dirs, e.g.
  `python3 -m pytest practices/story-driven-delivery/skills/supporting/story-graph-ops/tests`.
- Caveats (pre-existing, not env issues): the root `pytest.ini` testpaths are stale (point
  to pre-reorg dirs), and a few suites such as `common/tests/test_scanner_test_helper.py`
  reference old top-level paths and fail. The well-formed suites pass.
- Kanban app: `npm test` (Vitest, in the kanban app dir), typecheck `npm run typecheck`.
- "Lint" = the encoding/mojibake guard: `python3 scripts/scan_encoding.py --check`. It
  currently reports many pre-existing mojibake issues in committed content (not a setup
  problem). The `scripts/hooks/pre-commit` hook runs this on staged `.md`/`.mdc` files; it
  is NOT auto-installed (run `./scripts/install-hooks.sh` if you want it).
