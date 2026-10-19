## Summary

This adds `SESSION_NOTES.md` to the trimmer's ledger table (`LEDGERS` in `starter-kit/methodology_trim.py`), so `methodology_trim.py` can trim it and so `--reverify` can name a stub finalize in a `SESSION_NOTES.md` shard. It was part of #94's fourth commit until you asked for it to be separate. It is one commit on top of #94's branch, `895c7bd`, so it needs #94 first; terms (trimmer, proof, shard, stub, finalize, record 0, `--reverify`) are as defined there.

## What it adds

- **The table entry.** The runner's Phase 1B writes a stub into `SESSION_NOTES.md` and Phase 3D overwrites it in place, exactly as it does the `status: pending` receipt in `HANDOFFS.md`. The entry's grammar is the runner's own: a record starts at `### What Session N Did` or at `### Session N-1 Handoff Evaluation (by Session N)` and at nothing else, so the seed's `### What You Must Do` stays front matter and a `###` sub-heading inside a write-up stays inside its record. The file has no footer. A record's date is its `**Started:**` line (or `**Started/Completed:**`, `**Completed:**`, `**Date:**`), else the first date in the record.
- **The stub marker needs both Phase 1B lines**: the `**Status:** Session claimed` line (which must start a line) and the `(IN PROGRESS)` tag, anywhere in the record. The status line alone is not enough: re-measured today over the live notes files of 12 projects, a finished record in 3 of them still carries it, and 2 of those 3 dropped the tag.
- **The `--cut DATE` comment** now says what is true: the record date labels a shard's span and also decides where `--cut DATE` falls, and a record whose only date is the fallback (the first bare date in its text) can be cut by a date that is not its own. The cut is lossless either way.
- `FRAMEWORK_APPARATUS.md`'s timing-rule paragraph names the notes stub; `README.md`'s file tree (line 204) lists the third ledger.

## Measured

- **The #93 repository, 54 proofs at `82433662`**, `--reverify` of each shard: with this commit 46 exit 0 and 8 exit 4; without it (#94 alone) 46 exit 0, 1 exit 4 and 7 exit 1. The 7 are the `SESSION_NOTES.md` shards.
- **Read-only `--check` of this branch's trimmer on 12 projects' live notes files**: 10 parse, 1 reads as a fresh seed (`NO_RECORDS`), 1 keys its sessions on another heading shape and is refused by name (`GRAMMAR_MISMATCH`, exit 3) rather than reported empty.
- **Tests**: `TestSessionNotesIsATrimmableLedger`, 18 tests; the trimmer's suite goes from 227 to 245 and its floor in `.quality-gates.json` from 227 to 245. `quality_ratchet.py --run` in a clean clone: 12 of 12 (results `e56bb08a3c66`, manifest `c9460f6eeb2e`).

## Not settled by this pull request

You observed three things about this file. I reproduced each and this commit settles none of them:

1. **The budget and the trigger disagree.** A 123,325 B notes file fails `context_budget.py` (over the seed's 120,000 B ceiling; it is also over the seed's 400-line and 25,000-token ceilings) while `methodology_trim.py --check` says `trigger does not fire`, because a root `SESSION_NOTES.md` takes the Class A arm (196,608 B). Options: give this entry the one-read cap instead of the Class A arm, so the trigger fires where the budget fails; or keep the arm and say in the docs that the two thresholds differ for this file. Which do you prefer?
2. **Headings the pattern does not match are silent.** A file whose newest 135 of 160 records say `### What Session N did` (lowercase `did`) is read as 25 records plus a very large front matter; a dry run reports `would archive 24 of 25 record(s)` and `live 249,840 B -> 213,031 B`, still over the 196,608 B trigger, and says nothing about the 135 sections it left in place. The existing `content_probe` only catches dated, heading-shaped lines. Options: a finding when heading-shaped `Session N` lines sit in the front matter, or a case-insensitive `Did`.
3. **An `ACTIVE TASK` edit in the trim commit fails L2 after `L2_OK`.** The trimmer's L2 compares the working tree before and after the trim; the proof compares the trim commit with its parent, so an uncommitted front-matter edit is invisible at write time and fatal in the proof. This is general (any ledger whose front matter changes in the trim commit) but only `SESSION_NOTES.md` has a front matter that sessions rewrite. Option: an advisory finding at write time when HEAD's front matter differs from the working tree's, like `FRONTIER_FINALIZE_UNCOMMITTED` for record 0.

There is also a question underneath all three: `FRAMEWORK_APPARATUS.md` and the seed's first lines say `SESSION_NOTES.md` is transient and overwritten every session, while the seed's last line says session history accumulates below it, and the #93 repository holds hundreds of records in it. If you would rather the framework settle which it is before the trimmer learns to trim the file, this PR can wait for that.

## Adopter impact

`bin/sync` copies `methodology_trim.py` (1.8.2 to 1.9.0) and one paragraph of `FRAMEWORK_APPARATUS.md`. A project can then run `methodology_trim.py --file SESSION_NOTES.md --check` and trim that file with the canonical tool. A project that carries its own table entry for this file (the #93 repository does) will have `bin/sync` stop on the locally edited `methodology_trim.py` (exit 2, naming the file, `--force` to overwrite), as it does for any local edit (measured with #94's earlier fourth commit, which carried the same entry, in a scratch project holding the #93 repository's copy); after a forced sync the canonical entry read that project's notes file exactly as its own entry did. A notes file whose sessions are not under the runner's two headings is refused by name, never reported empty.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
