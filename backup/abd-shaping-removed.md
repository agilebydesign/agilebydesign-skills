# abd-shaping removed

**abd-shaping** was removed in commit `b386b0b` ("removed shaping"). The engine was ported into **abd-story-synthesizer**, which is now self-contained.

## Status

- **Backed up** — copy restored to `backup/abd-shaping/`
- **Not installed** — abd-shaping does not exist in `C:\Users\thoma\.agents\skills` or `agilebydesign-skills/skills`
- **No code references** — build.py and engine use local scripts only
- **Config** — mm3e and other projects reference `abd-story-synthesizer` only

## References updated

- deploy-skills.ps1 — removed from example
- abd-story-synthesizer docs — updated to "self-contained"
