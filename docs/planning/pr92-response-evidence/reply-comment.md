Thanks. All three changes are right, and so is the answer on the tag. I checked each point against `v4.1`, `v4.2` and the branch before editing anything:

- `9b69070` is an ancestor of `v4.2` but not of `v4.1`. `v4.1:bin/sync:15`/`:297` and `bin/status:28`/`:254` use the checkout's own manifest, and `v4.1` has no `bin/_manifest_reader.py`. So the two defects existed only on the PR #91 branch.
- None of the 30 `DISTRIBUTION` sources is under `bin/`. The only distributed file that changed between `v4.1` and `v4.2` is `starter-kit/methodology_dashboard.py` (2.11.2 → 2.11.3).
- `v3.8`, `v4.0` and `v4.1` each have a "tagged and released" entry. `v4.2` is lightweight and the older tags are annotated. `v3.8`'s tag stayed at `6b29d3d` while its notes landed in `2f911c9`.

I pushed `8a232bb` to the branch (`CHANGELOG.md`, `CLAUDE.md`, `README.md`; +14 −5):

1. **Defects.** The two README bullets and `CLAUDE.md` now use your wording. They no longer say v4.2 fixed a defect or that code "no longer runs".
2. **Ledger entry.** `### 2026-10-03 · [ad hoc] Recorded: v4.2 tagged and released by rmsharp`, placed after the documentation entry. I kept your date; the PR #91 comment entry, posted at 01:37Z, carries it too. The documentation entry is already committed and the ledger hook refuses an edit to a committed entry, so it keeps its release clause as the pointer you mentioned.
3. **Adopters.** README and `CLAUDE.md` now say "Update your methodology checkout, then re-run `bin/sync`; sync itself delivers only the 2.11.3 dashboard."

The three small things are in too: "is or lies inside `.git`" and "names no file (`.`)"; the merge date is 2026-10-02; "three non-blocking points" now says it is the approval's.

**Tag.** Left at `f34769f`, lightweight. The PR description still said I would move it; it now says the tag stays.

**Release.** I edited the published Release body the same way: the three sentences, the path-check line and the Updating line. The tag is untouched.

On `8a232bb` in a clean clone: `bash bin/tests.sh` gives 261 passed / 0 failed and `quality_ratchet.py --run` reads 12/12 (`results 10df8059439f · manifest 5986cf638fb1`, the same pair as in your runs at `fa2bb5d` and the tag). `check-links` and `check-ledger` are OK, and `CLAUDE.md` is 51,487 B of its 59,168 B ceiling.
