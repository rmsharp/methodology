The v4.2 tag and GitHub Release exist, but the repo's own version documentation still says v4.1. This does what the v4.1 release commit (`1e018d1`) did for v4.1:

- `CLAUDE.md`: *Current version* v4.1 → v4.2, plus the v4.2 entry under §Versioning (51,487 B, under its 59,168 B ceiling).
- `README.md`: "What's New in v4.2" above v4.1's, covering #91 (`--source=github` uses the source's own manifest), which the v4.1 entry named as not yet released.
- `CHANGELOG.md`: two ledger entries, one for the documentation and one recording that v4.2 was tagged and released.

Docs only. No script, gate, or manifest change. In a clean clone of this branch, `bash bin/tests.sh` gives 261 passed / 0 failed and `quality_ratchet.py --run` reads 12/12. `check-links` is OK, `check-ledger` is OK, and the context budget reports nothing over.

**Tag:** the `v4.2` tag and release stay at `f34769f`. A moved tag does not reach clones that already hold it, and v3.8's tag also stayed at its commit when its notes landed later.

**Review changes (`8a232bb`):** the notes no longer present two defects that existed only on the PR #91 branch as fixed by this release; the adopter line says to update the methodology checkout first, since sync itself delivers only the 2.11.3 dashboard; the release has its own ledger entry; three wording fixes.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
