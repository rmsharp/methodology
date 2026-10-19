The v4.2 tag and GitHub Release exist, but the repo's own version documentation still says v4.1. This does what the v4.1 release commit (`1e018d1`) did for v4.1:

- `CLAUDE.md`: *Current version* v4.1 → v4.2, plus the v4.2 entry under §Versioning (51,405 B, under its 59,168 B ceiling).
- `README.md`: "What's New in v4.2" above v4.1's, covering #91 (`--source=github` uses the source's own manifest), which the v4.1 entry named as not yet released.
- `CHANGELOG.md`: one ledger entry.

Docs only. No script, gate, or manifest change. In a scratch clone of this branch, `bash bin/tests.sh` gives 261 passed / 0 failed, `check-links` is OK, `check-ledger` is OK, and the context budget reports nothing over.

**Tag:** once this merges, the `v4.2` tag and release currently at `f34769f` should move to the merge commit, so the tagged tree carries its own version notes. I'll do that on your say-so after the merge, since moving a published tag is something you'll want to decide. The release body's "Tagged at" line will be updated with it.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

