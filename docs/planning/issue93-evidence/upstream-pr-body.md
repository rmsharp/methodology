<!-- DRAFT of the upstream pull request body for branch fix/trim-verify-false-red-issue93 (3 commits on upstream/main f34769f, tip 972eb2c; the HTML comment is stripped before sending).
     NOT SENT. Sending the branch, opening the PR and every comment on it are the operator's go-ahead, each time.
     Title: fix(trim): generated proofs stop reading red on lossless trims, and --reverify re-derives a frozen one (refs #93) -->

## What this changes

Issue #93 reports that 10 of 54 generated `.verify.sh` proofs in one adopter repository read FAIL on trims that lost nothing, from three causes in the generated script. This PR addresses each, as one commit per cause. They are one change set because they share the proof template and its tests.

| commit (in order) | cause in #93 | change | `TRIM_VERSION` |
|---|---|---|---|
| 1 | 2: L2 `leaked` is a substring test | tests membership in the sets of whole lines, the `> 24` length filter kept | 1.5.1 |
| 2 | 1: a close-out commit that also trims | the ledger spec gains an optional `stub_marker`; the proof names the stub-finalize shape (one labelled `FAIL:`, exit 4) instead of the generic L1/L3 pair; the writer warns before it happens (`FRONTIER_PENDING_STUB`, `FRONTIER_FINALIZE_UNCOMMITTED`, advisory); the timing rule is stated once in `FRAMEWORK_APPARATUS.md`, the proof's note and the writer | 1.6.0 |
| 3 | 3: frozen proofs | `--reverify <shard>` lifts `LIVE`, `SHARD` and the record grammar from the frozen proof, runs today's template and prints the verdict under a banner saying it is a claim about today's logic; it writes nothing | 1.7.0 |

Each commit carries its tests and its `CHANGELOG.md` entry and raises the `trimmer-unit-tests` floor (124, 129, 154, 181).

## What this does not change

- **A proof already written stays frozen.** A red proof stays a red artifact; `--reverify` gives a second verdict next to it.
- **A stub finalize is still a FAIL.** It gets its own label and exit status, but the existing note's reason stands: a real loss can have this exact shape, so the proof certifies that nothing but record 0 changed and that record 0 was a stub, not that the finalized text is right.
- **The write-time warnings are advisory.** They refuse nothing.
- **A ledger the canonical table has no entry for** (for example an adopter's local `SESSION_NOTES.md` spec) gets no stub marker from `--reverify`, so such a proof re-derives at exit 1, not 4. In the adopter run below that is 7 of the 10 red proofs.

So this fixes the two L2 false reds outright, names the stub-finalize shape and warns before it happens, and gives adopters a way to ask what today's template says. It does not turn the other red proofs green, which is why it says `refs`, not `closes`.

## Measured

- **Tests:** `tools/test_methodology_trim.py` 124 → 181 (57 new). `quality_ratchet.py --run` on this branch: 12/12 pass, 0 fail, 0 unmeasured. `bin/tests.sh` 261 passed, 0 failed (the trimmer suite is one assertion there, so that count is unchanged).
- **Mutation testing:** in my fork each phase's new code was mutated (9, 37 and 54 mutants); every non-equivalent mutant is killed by the test written for it. I did not re-run them on this branch: its trimmer and test files differ from the fork's by six comment or message lines, none of which changes behaviour.
- **The adopter** (`rmsharp/nprcgenekeepr`, a fresh clone at `82433662`: 54 proofs, 10 red): `--reverify` over every shard through the shipped CLI gives 46 at exit 0, 7 at exit 1 and 1 at exit 4. No proof newly red; 2 newly green, the two L2 shards in the issue. The tree (every file by size and mtime, HEAD, refs, stash) is identical after the sweep.
- **This repository:** its one frozen proof stays at exit 0 under `--reverify`. In a throwaway clone, a forced `--cut 2` trim of this repository's own `HANDOFFS.md` (38 receipts, 221,642 B, above the 196,608 B trigger) wrote a shard whose proof exits 0.
- **End to end, same throwaway clone:** with a claim stub committed the writer prints `FRONTIER_PENDING_STUB`; finalizing it and trimming in one commit gives a proof that exits 4 with the named FAIL line and the timing-rule note.
- **`bin/sync --source=local` into a throwaway adopter:** `methodology_trim.py` and `FRAMEWORK_APPARATUS.md` arrive byte-identical to this branch's; the adopter's copy then reports v1.7.0.
- **Merge:** `git merge-tree` against #92's branch reports no conflict (both prepend to `CHANGELOG.md`, which is `merge=union`).

## Adopter impact

- `bin/sync` carries `methodology_trim.py` (1.5.0 to 1.7.0) and one new paragraph in `FRAMEWORK_APPARATUS.md`. Commits 1 and 2 change only what a *new* trim writes and warns about; commit 3 adds a flag. Nothing rewrites a proof already in an adopter's archive.
- **Exit status 4 is new** for the generated proof. A caller that tests `== 1` rather than `!= 0` would miss it. Nothing in this repository calls a proof that way (outside the archive, the tests and the trimmer, `verify.sh` appears only in prose and a hook comment); an adopter's own script might.
- The dashboard's read of `TRIM_VERSION` by regex still matches.
- One comment inside `VERIFY_TEMPLATE` changed wording, so newly generated proofs carry the new text.
- Not a framework release; the only version that moves is the tool's own `TRIM_VERSION`.

## Where to read closely

`--reverify` lifts text out of a frozen proof, and that text is later spliced into an unquoted shell assignment and into Python the proof executes. So the lift is strict, not a regex: each required line must match, whole, the form the template writes; `REGEN_PATTERNS` and `STUB_PATTERN` are parsed as literals and never evaluated; paths may not be absolute or contain `..`. The code is `_LIFT_REQUIRED`, `_lift_line`, `_lift_pattern` and `lift_grammar` in `starter-kit/methodology_trim.py`. Four payload tests (a shell payload in `LIVE`, a Python payload in `RECORD_START`, an expression in `REGEN_PATTERNS` or `STUB_PATTERN`, a shard file name carrying a shell payload) each carry a control showing the payload is live when spliced naively, then assert `--reverify` refuses it and nothing runs.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
