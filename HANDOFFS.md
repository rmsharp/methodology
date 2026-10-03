# Handoff Receipts — durable close-out proof

This repository dogfoods its own methodology: every session records a durable, machine-checkable
`handoff` receipt here at close-out (Phase 3D), and Phase 0 reconciles it against `git log`. See
[`starter-kit/HANDOFFS.md`](starter-kit/HANDOFFS.md) for the block format and the write points, and
`bin/check-handoff` for the checker. Newest on top; prepend-only.

**Retention policy — keep TWO receipts, trim above TWO.** Everything older is archived under
`docs/archive/` and indexed in [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md). **N=2 is an operator decision (2026-09-28, S232)**
replacing **his N=1 of S172 (2026-09-16)**, which had replaced S127's N=4. It settles a
contradiction rather than changing practice: this paragraph said *keep ONE* and printed `--cut 1`
while S229, S230 and S231 each ran `--cut 2` and kept two — flagged in S231's receipt as the
operator's to settle. BL-59's measurement of what actually reads this file still stands — the
handoff is done by the newest receipt alone — so the second receipt is a spare, not a working set. **Depth and trigger are separate on purpose:**
every trim pays a FIXED ~16 KB proof, so the trigger sits one above the depth (BL-60). **`methodology_trim.py` fires on BYTES (196,608 B),
never on a record count**, so the policy is applied by the session that notices: Phase 0 runs
`grep -c '^```handoff
session: S252
date: 2026-10-03
status: pending
active_task: PLAN (BL-79) for making the Phase 3G close-out report always run and always shaped: a generated report script plus a Stop hook. Planning session; the plan in docs/planning/ is the deliverable, nothing is implemented and nothing goes upstream.
```

```handoff' HANDOFFS.md` and reports the count; **above 2**, the trim is its own action after
that report, never inside Phase 0, which is read-only apart from the reconcile backfill
(`starter-kit/SESSION_RUNNER.md` Phase 0): `--cut 2 --force`. The force is
warranted, not an override — `SRF_RED` refuses every on-schedule retention trim by construction
(BL-59). `bin/check-handoff` validates the 13-key schema on the **newest** receipt; `--all` checks
every receipt and `--archived` a frozen shard. Below three receipts Test 34 prints six named `SKIP` rows — stated, never silent. **`RETENTION_FLOOR = 3` in `bin/check-handoff` is that TRIGGER, not this depth**, so N=2 leaves it and its A1 fit (3 x 12 KiB + 7,168 <= 65,536 B) untouched; the steady state is two receipts between claims and three during one, which is why `tests-sh-passed` measures 343 at rest and 349 mid-claim.

**Two session sequences share this ledger and their numbers collide.** This fork and
`upstream/main` each run their own `S<N>` counter, so a receipt is identified by **session + date**,
never by number alone. **Every upstream receipt is now archived**; every receipt retained here is
the fork's. At a resync the two sequences stay separate and unrenumbered, each incoming receipt is
checked against ours before it is kept, and within a shared date the fork's precede the arriving
upstream ones (precedent: `fc4d297`).

> **THE HAND-MAINTAINED RECEIPT COUNT IS GONE, DELIBERATELY.** S172's rewrite dropped *"This file
> currently holds **N**"* — the number [Learning #12](starter-kit/FRAMEWORK_LEARNINGS.md) and upstream
> [issue #65](https://github.com/KJ5HST/methodology/issues/65) both cite as always wrong by the next
> close-out. The trimmer still declares it, so **every trim now reports `FRONTMATTER_FIELD_ABSENT`**:
> stated, expected, not a failure. Removing the declaration is distributed — its own go-ahead (BL-60).
> **Count with `grep -c '^```handoff' HANDOFFS.md`.**

> **⚠ THREE is the floor the retention policy sits one above.** `bin/tests.sh` Test 34 mutates *this*
> ledger to check `check-handoff --all`'s whole-ledger invariants, reading two anchors from the live
> file — not hardcoded, so it survives *which* receipts rotate, but it needs three to exist. A short
> ledger is **stated rather than silent** (BL-40 (b)): below the floor those six assertions print as
> `SKIP` rows naming themselves, the summary carries a skip count, and a ledger with *zero* receipts
> still FAILS — corruption is not rotation. **Nothing prevents a cut below three; the policy is what
> makes it not happen.** Re-run `bash bin/tests.sh` after any trim of this file.

**The shard index is not in this front matter, on purpose.** It lived here until S174 and grew a row
with every trim against the fixed 7,168 B header reserve (Test 39 A2), so it moved out rather than the
reserve rising. A trim commit still carries the trimmer's ~448 B pointer block; the fold removes it, so a
trim-and-fold no longer grows this front matter. The fold rule is in the index.

<!-- NEXT TRIMMING SESSION: methodology_trim.py appends a 3-line pointer block here
     (starter-kit/methodology_trim.py:1093 build_pointer_block, :1103 insert_pointer). Fold it into
     docs/HANDOFFS_ARCHIVE_INDEX.md as one row and delete the block, IN ITS OWN COMMIT: inside the
     trim commit the shipped .verify.sh fails L2 (fork Learning #58). -->

```handoff
session: S251
date: 2026-10-03
status: complete
self_score: 7
predecessor_score: 8
active_task: **DONE: tag `v4.2` and a GitHub Release (Latest) on `KJ5HST/methodology` at `f34769f3`, after upstream PR #91 merged; and upstream PR #92 (docs: `CLAUDE.md` v4.2, README What's New, one ledger entry) opened.** The operator asked for both and approved each exact text. NOT DONE: moving the tag and release to the merge commit of #92, which waits for the maintainer.
what_was_done: Phase 0 PARTIAL and no Phase 1B claim (no pending receipt opened; SAFEGUARDS not read; no dashboard refresh; no trim, so HANDOFFS.md now holds 5 receipts). Found #91's head had moved to `9ac2d4b3` after our Approve on `befa7553`, with a maintainer comment asking for a second look; the operator then said #91 was merged (`e1073568`) and asked for tag 4.2 and a release. Measured in a scratch clone at `f34769f3`: 261 passed / 0 failed, ratchet 12/12. Showed the release text, got `post`, created the release, read it back. Found `docs/RELEASE_HISTORY.md` exists only in the fork and the 4.x version docs live in upstream `CLAUDE.md` and `README.md`; the operator chose a PR. Drafted the edits on `docs/release-v4.2` in a scratch clone (suite 261/0, check-links and check-ledger OK), showed the PR text, got `post`, pushed to the fork and opened #92. At the operator's request wrote the ledger entries and this receipt. NOT DONE: this fork's own README, `CLAUDE.md` and `docs/RELEASE_HISTORY.md` still say v3.7 (right until the resync, BL-95).
next_steps: **(0) TRIM FIRST, after the Phase 0 report:** HANDOFFS.md holds 5 receipts; `--cut 2 --force` as its own action, then fold the pointer and re-run `bash bin/tests.sh` (Test 34). **(1) CHECK #92:** `gh pr view 92 --repo KJ5HST/methodology --json state,mergeCommit,comments,reviews`; a maintainer reply ranks above everything. **(2) AFTER HE MERGES #92, ASK THE OPERATOR to move the tag:** `v4.2` and the release from `f34769f3` to the merge commit (delete and recreate the tag, or `git push -f` of the ref; edit the release target and the body's "Tagged at" line; read both back). Moving a published tag is its own go-ahead. **(3) ASK THE OPERATOR, one picker, text drafted in an earlier turn:** BL-95 the resync against `upstream/main` (now v4.2; needs a plan he commissions; it also brings the 4.x version docs here); D3; BL-94; BL-96; the P4 chain (about $35 against $15.49 left, needs a cap raise). **(4) PUSH:** local `main` is 3 commits ahead of `origin/main` plus this close-out; a push needs his go-ahead. **(5) STILL OPEN:** D3, BL-94, BL-95, BL-96, BL-93, BL-89, BL-87, BL-84, BL-92.
key_files: the release https://github.com/KJ5HST/methodology/releases/tag/v4.2 and PR https://github.com/KJ5HST/methodology/pull/92 (branch `docs/release-v4.2`, commit `fa2bb5d4`); in that branch `CLAUDE.md:100` (*Current version*) and the v4.2 bullet after v4.1's, `README.md` "What's New in v4.2" above v4.1's, `CHANGELOG.md` top entry; precedent `1e018d1` (the v4.1 release docs commit). Scratch clone and outputs `.../scratchpad/v42`, `v42-tests.out`, `v42-ratchet.out`, `v42b-tests.out` (session-scoped, not committed).
gotchas: **(1) THE TAG IS LIGHTWEIGHT AND ALREADY PUBLISHED:** `gh release create --target` made it; moving it affects anyone who fetched `v4.2`; the release body says "Tagged at `f34769f`" and must change with it. **(2) `docs/RELEASE_HISTORY.md` IS FORK-ONLY;** upstream keeps release narration in `CLAUDE.md` §Versioning and the README, so "fix the version docs" meant upstream files, not this checkout's. **(3) THIS FORK IS STILL v3.7;** do not bump its version line before the resync. **(4) A PICKER IN THE SAME TURN AS PROSE WAS REJECTED AGAIN:** show the exact text, end the turn, then act on `post`. **(5) A `gh` READ-BACK BODY GAINS ONE TRAILING BLANK LINE;** compare modulo that. **(6) `dashboard_history.jsonl` AND `.context-budget-history.jsonl` ARE MODIFIED BY TOOL RUNS** and left alone.
runtime_smoke: No runtime behavior changed in this fork (releases and a docs PR upstream). Scratch clone at `f34769f3`: `bash bin/tests.sh` 261 passed / 0 failed, exit 0; `quality_ratchet --run` 12/12 pass · 0 fail · 0 unmeasured · results 10df8059439f · manifest 5986cf638fb1. Scratch clone of `docs/release-v4.2`: 261 / 0, exit 0; `check-links` OK; `check-ledger` OK. Fork `main` with this receipt: quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 95b5ea74bd7c · manifest 01a4ae7aa511 (the first run, before the receipt cited a gate run, read 9/11 with tests-sh-failed and check-handoff-all red, both from the receipt itself).
changelog_ref: CHANGELOG.md "S251 — Phase 0", "S251 — tag v4.2 and GitHub Release", "S251 — upstream PR #92 opened", "S251 close-out"
commit: this close-out; Phase 3C appended no fork learning, so no retirement is owed (none considered: no row appended); nothing git-pushed; on KJ5HST/methodology: tag and release `v4.2` and PR #92, each at the operator's `post`
```

```handoff
session: S250
date: 2026-10-03
status: complete
self_score: 6
predecessor_score: 9
active_task: **DONE: the formal review on upstream PR #91 (`KJ5HST/methodology`, the maintainer's `feat/sync-manifest-at-ref`) posted as APPROVE at head `befa7553`, read back identical (state APPROVED, same commit, same body). It was S249's operator decision; the operator said `post` after seeing the exact text. No merge, no push to his branch, no spend.**
what_was_done: Phase 0 PARTIAL and no Phase 1B claim (no pending receipt opened; SAFEGUARDS not read; no dashboard refresh; no policy trim, so HANDOFFS.md now holds 4 receipts). Confirmed #91 OPEN, head unchanged, no maintainer reply after our last comment. At the operator's request ("you need to address the merge conflict") measured it: GitHub says CONFLICTING/DIRTY, but a scratch-clone merge of `befa7553` into upstream `main` `58458db` is clean and its suite is 254 passed / 0 failed, exit 0. The review text carries that finding. Two approval pickers were rejected because the operator could not see the draft; the third attempt (text in its own turn, no picker) worked.
next_steps: **(0) TRIM FIRST, after the Phase 0 report:** HANDOFFS.md holds 4 receipts; policy is `--cut 2 --force` as its own action. **(1) CHECK #91:** `gh pr view 91 --repo KJ5HST/methodology --json state,headRefOid,mergeable,mergeStateStatus,comments,reviews`; a maintainer reply ranks above everything; re-check whether GitHub's `CONFLICTING` cleared. **(2) ASK THE OPERATOR, one picker, text drafted in an earlier turn:** BL-95 the resync against `upstream/main` (needs a plan he commissions); D3; BL-94 planning; BL-96; the P4 chain (about $35 against $15.49 left, needs a cap raise). **(3) PUSH:** fork `origin` is behind local `main`; a push needs his go-ahead. **(4) STILL OPEN:** D3, BL-94, BL-95, BL-96, BL-93, BL-89, BL-87, BL-84, BL-92.
key_files: the review, https://github.com/KJ5HST/methodology/pull/91 (state APPROVED on `befa7553f262377273b9f4dc5a3408a7d3d05522`); scratch draft `.../scratchpad/pr91-review-body.md` and merged-suite output `.../scratchpad/pr91c-tests.out` (session-scoped, not committed); PR-branch files at `befa7553` (not this checkout): `bin/tests.sh:1281` (Test 32), `bin/sync:116` (`source_distribution`), `bin/status:139` (`use_source_manifest`), `bin/_manifest_reader.py`.
gotchas: **(1) GITHUB'S MERGE FLAG AND A LOCAL MERGE DISAGREED:** `CONFLICTING`/`DIRTY` against a clean `git merge` into `58458db`; GitHub's test-merge ref `refs/pull/91/merge` (`204b091`) is built on the OLD base `16805399`, not on `main` `58458db`, so the flag was never recomputed; `git merge-tree --write-tree origin/main befa7553` exits 0 (clean). Only the maintainer can refresh it (push, or close and reopen). The operator confirmed GitHub still showed the conflict after the review. Re-query before repeating either claim. **(2) PROSE IN THE SAME TURN AS AN `AskUserQuestion` WAS NOT SEEN, EVEN IN `preview`:** end the turn with the draft, ask in the next. **(3) SESSION_NOTES.md DOES NOT EXIST IN THIS REPO;** the receipt in HANDOFFS.md is the handoff. **(4) `dashboard_history.jsonl` AND `.context-budget-history.jsonl` ARE MODIFIED BY TOOL RUNS** and left alone.
runtime_smoke: No runtime behavior changed (a PR review and docs). Scratch clone, #91 head merged into upstream `main`: 254 passed / 0 failed, exit 0. Fork `main` with this receipt: quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 95b5ea74bd7c · manifest 01a4ae7aa511 (the first run, before the receipt cited a gate run, read 9/11 with tests-sh-failed and check-handoff-all red, both from the receipt itself; `bash bin/tests.sh` with the final receipt: 361 passed, 0 failed, exit 0 on the rerun inside the ratchet; `check-handoff --all` OK on 4).
changelog_ref: CHANGELOG.md "S250 close-out", "S250 — merge-state check", "S250 — formal review posted"
commit: bfbe8bc (close-out); Phase 3C appended no fork learning, so no retirement is owed (none considered: no row appended; the picker lesson extends memory `feedback_show_the_artifact_before_asking_for_its_review`); nothing git-pushed; one APPROVE review is on KJ5HST/methodology#91 at the operator's `post`
```

