# Handoff Receipts — durable close-out proof

This repository dogfoods its own methodology: every session records a durable, machine-checkable
`handoff` receipt here at close-out (Phase 3D), and Phase 0 reconciles it against `git log`. See
[`starter-kit/HANDOFFS.md`](starter-kit/HANDOFFS.md) for the block format and the write points, and
`bin/check-handoff` for the checker. Newest on top; prepend-only.

**Retention policy — keep ONE receipt, trim above TWO.** Everything older is archived under
`docs/archive/` and indexed in [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md). **N=1 is an operator decision (2026-09-16, S172)
replacing S127's N=4**, taken against BL-59's measurement of what actually reads this file: the
handoff is done by the newest receipt alone. **Depth and trigger are separate on purpose:**
every trim pays a FIXED ~16 KB proof, so the trigger sits one above the depth (BL-60). **`methodology_trim.py` fires on BYTES (196,608 B),
never on a record count**, so the policy is applied by the session that notices: Phase 0 runs
`grep -c '^```handoff' HANDOFFS.md` and reports the count; **above 2**, the trim is its own action after
that report, never inside Phase 0, which is read-only apart from the reconcile backfill
(`starter-kit/SESSION_RUNNER.md` Phase 0): `--cut 1 --force`. The force is
warranted, not an override — `SRF_RED` refuses every on-schedule retention trim by construction
(BL-59). `bin/check-handoff` validates the 13-key schema on the **newest** receipt; `--all` checks
every receipt and `--archived` a frozen shard. Below three receipts Test 34 prints six named `SKIP` rows — stated, never silent.

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
session: S179
date: 2026-09-17
status: pending
self_score: pending
predecessor_score: pending
active_task: **BL-54 (`docs/planning/BACKLOG-DETAIL.md:1602`, row `docs/planning/BACKLOG.md:149`): `bin/status` AND `bin/sync` WALK HISTORY WITH `--full-history`, SO A VERSION FROM A MERGE'S OTHER SIDE NO LONGER READS AS LOCALLY MODIFIED. CHOSEN BY THE OPERATOR AFTER PHASE 0 (picker).** Same picker: trim `CHANGELOG.md` now (past the 262,144 B refusal), and push fork `main` to `origin` at close-out. The retention trim of `HANDOFFS.md` is owed after this claim. Fork-local until the push; the upstream PR is its own go-ahead.
what_was_done: pending
next_steps: pending
key_files: `bin/status:52` (`local_history`, the walk at `:56`); `bin/sync:55` (`local_history_blobs`, the walk at `:60`); `docs/planning/changelog-rules-contradictions-plan.md:149` (S178 block, item (12)); `bin/tests.sh` (where the test lands)
gotchas: The default walk follows a merge's TREESAME parent, so `22ce71b` hides the fork-side trimmer versions (3 commits visited, 14 before the merge, 25 with the flag). *N versions behind* indexes the walk and inflates with the flag (`mts-system`'s `FRAMEWORK_LEARNINGS.md` went to 63 behind on S178's scratch copies). The `CHANGELOG.md` trim adds its own entry, and the receipt count reads 4 until the retention trim. Run suites one at a time (Test 9).
runtime_smoke: pending
changelog_ref: CHANGELOG.md "2026-09-17 · [BL-54] S179 claim"
commit: pending
```

```handoff
session: S178
date: 2026-09-16
status: complete
self_score: 7
predecessor_score: 7
active_task: **BL-57'S P5 IS DONE, BY MERGE: FORK `main` CARRIES THE ONE-HOME `CHANGELOG.md` RULES (MERGE `22ce71b` OF `bl57/changelog-rules` `83a12f0`). BL-54 IS NEXT, BEFORE P6: THE MERGE MAKES `bin/status` READ `methodology_trim.py` AS LOCALLY MODIFIED IN 3 ADOPTER COPIES.** Chosen by the operator after Phase 0 (picker). Operator decisions, each by picker: merge rather than port; D10, remove the hook's claim carve-out (explained in plain prose on request), with the `tests-sh-passed` floor lowered to the measured count; keep the merge and take BL-54 next once its rows appeared. Fork-local: nothing pushed after `29321da`, nothing sent upstream.
what_was_done: **`29321da`** records the push of `fc4fe0c` (operator go-ahead), pushed under the push-record grant. **`cba2166`** claim, with the Phase 0 snapshots. **`22ce71b`** the merge: 5 conflicts, 9 hunks, as `merge-tree` said. `CHANGELOG.md` ours; `bin/_manifest.py` and `bin/tests.sh` theirs; `CLAUDE.md` the fork row naming the ledger rules; the runner the branch's 3F bullet plus the fork's `Model:` sentence re-pointed to §The Action Ledger (−14 B). A line-multiset check found every difference from the branch is a fork change or one of those resolutions. The 8 files identical at the base equal the branch's blobs. **`6774627`** a fork-only dashboard test read the live seed's fenced examples (plan hazard 6); it reads the frozen format-1 seed now, blob asserted, and a fence-blind mutant fails it. **`1664860`** D10: the hook equals the branch's byte for byte, and Test 27 (508 lines, 34 rows) is gone. A real claim-only commit exits 1 under the new hook, 0 under the old. **`dee680c`** root `CHANGELOG.md` front matter: the pointer; the cross-shell audit (638 in zsh and bash, equal to the heading count); `[BL-<id>]`; a Claims paragraph; the no-trim decision in place of the rate rule. Plus `HANDOFFS.md`'s retention line (a trim never runs in Phase 0). **`fd611a6`** `starter-kit/BOOTSTRAP.md:383` and `README.md:413`, two fork-only sentences the rules made false. **`368b29c`** `tests-sh-passed` 327 → 294, committed with `--no-verify` after the ratchet refused it (exit 2). 294 was measured at two receipts with Test 9 green; a 293 reading with Test 9 rate-limited was not used. **`d10f9af`** `trimmer-unit-tests` 123 → 124, measured. **`fbdd47d`** plan S178 block items (12)–(15), the BL-57 and BL-54 rows, fork Learning #71. `22ce71b`–`d10f9af` were built in a scratch clone and fast-forwarded onto `main` after their suites ran. The first two ran there without hooks and were checked afterwards: `commit-msg` 0, ledger co-staged, manifest unchanged.
next_steps: **(1) BL-54** (`docs/planning/BACKLOG-DETAIL.md:1602`; row `docs/planning/BACKLOG.md:149`): add `--full-history` at `bin/status:56` and `bin/sync:60`. RED first: build a test on a merge that keeps the merged-in side's content for a path. That is `22ce71b`'s shape for `starter-kit/methodology_trim.py`: the default walk visits 3 commits, `--full-history` 25, and before the merge it was 14. Settle the detail's open question too: with the flag, *N versions behind* inflates (scratch: `mts-system`'s `FRAMEWORK_LEARNINGS.md` went from locally modified to 63 behind), because the count indexes the walk. Verify with `bin/status --source=local` on scratch copies of the six adopters, before and after. S178's copies show 3 new *locally modified* rows (the trimmer in `mts-system`, `vscode_quarto_ext`, `wsfct`) and 4 older ones (`FRAMEWORK_LEARNINGS.md`), all cleared by the flag; `model_project_constructor`'s 2 rows and `nprcgenekeepr`'s trimmer are real local changes and stay. Its upstream PR is its own go-ahead. **(2) Then P6–P11** (plan `:729`), one adopter per session. **(3) `CHANGELOG.md` passes the 262,144 B hard read refusal with this close-out.** The operator's standing decision is to raise a trim only once it does, so ask at the next Phase 0 whether to trim before BL-54. **(4) Push:** fork `main` is 26 commits ahead of `origin` after this close-out; pushing needs a go-ahead. **CARRIED:** BL-61; BL-60 (folds BL-36); BL-62 and #80's F5 ride P12; `README.md`'s stale cost section (plan item (15)); the runner and `SAFEGUARDS.md` stay `over`.
key_files: `docs/planning/changelog-rules-contradictions-plan.md:149` (S178 block), `:684` (P5), `:729` (P6–P11); `docs/planning/BACKLOG-DETAIL.md:1602` (BL-54); `docs/planning/BACKLOG.md:149`, `:152`; `bin/status:56`, `bin/sync:60` (the walks); `.quality-gates.json:5` (`_fork_loosening_d10`), `:12` (294), `:43` (124); `.githooks/pre-commit` (the branch's hook, no carve-out); `bin/tests.sh:1203` (Test 27's removal note); `tools/test_methodology_dashboard.py:4673`; `CHANGELOG.md:11`, `:19`, `:40`, `:113` (front matter); `HANDOFFS.md:13`; `starter-kit/BOOTSTRAP.md:383`; `README.md:413`; `starter-kit/methodology_trim.py:33` (F5's claim, now false here too); `docs/FORK_LEARNINGS.md:83` (#71)
gotchas: **(1) UNTIL BL-54, A MERGE HIDES HISTORY FROM `bin/status` AND `bin/sync`** (fork Learning #71). Sync no adopter from fork `main` before BL-54 lands; a refused trimmer there is this defect, not an adopter edit. **(2) `tests-sh-passed` 294 IS THE 2-RECEIPT VALUE.** This close-out leaves 3 receipts, so the suite reads 300, and the next Phase 0 trim (`--cut 1 --force`) brings it back to 294. **(3) TEST 9 AND GITHUB'S RATE LIMIT:** two suites in parallel (Test 9 makes ~29 `gh` calls each) tripped a limit that `gh api rate_limit` did not show, and it cleared in about 15 minutes. Run suites one at a time, and never take a floor from a run where Test 9 failed. **(4) A SCRATCH CLONE RUNS NO HOOKS:** run `git config core.hooksPath .githooks` in it before committing anything you will land. **(5) `--no-verify` SKIPS `commit-msg` TOO:** after an approved bypass, run `.githooks/commit-msg <msgfile>` by hand. **(6) THE HOOK NOW EXEMPTS NO CLAIM:** a claim commit must stage its *(in progress)* entry. **(7) ZSH:** an unquoted `$h` does not word-split, so `set -- $h` took one argument; use bash for that.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh` AND `quality_ratchet.py --run`, in `--no-local` clones with HEAD asserted.** **Final, clone of `fbdd47d`: `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results 1552052a766d · manifest 8d8ddc767cdc`**; suite exit 0, **300 passed / 0 failed / 0 skipped** (3 receipts). Against `6774627`, the row diff is Test 27's 34 rows gone and Test 9 FAIL → PASS, nothing else. Dashboard exit 0, v2.18.0, 76/100; gates panel *10 pass / 0 fail*, *1 loosened*. **Per stage:** the Phase 0 re-run on `fc4fe0c` matched S177's citation (`db4e547cc884`); parent `cba2166` 332/1/0; merge `22ce71b` 332/2/0; `6774627` 333/1/0; `1664860` at 2 receipts 293/1/6 with Test 9 rate-limited, then `--run` 294 passed / 0 failed (results `839fb8a9f80a`). **P5's DONE, measured:** the 5 identical distributed files equal the branch's blobs; the audit is equal in zsh and bash (635 at Phase 0, old form equal); a claim-only commit is refused (real commit, scratch repo); `bin/status` on six adopter copies reads `CHANGELOG.md` *present (stale format)* in all six, **but tracked rows are not all as before: 3 new *locally modified* (BL-54)**. `bin/check-links` 0; `bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations` 0; `bin/check-handoff --all --allow-pending` 0. `context_budget.py --status` exit 2 at Phase 0 and close-out, the same three `over` rows, runner −14 B. **NOT EXERCISED:** any push after `29321da`, adopter syncs, upstream actions, CI (none).
changelog_ref: CHANGELOG.md "2026-09-17 · [BL-57] S178 close-out", plus the claim, the push record, the merge record with the test fix, D10, the front matter, the two fork-only sentences, the floor, the tightening and the P5-recorded entries
commit: 29321da + cba2166 (claim) + 22ce71b (merge) + 6774627 + 1664860 + dee680c + fd611a6 + 368b29c + d10f9af + fbdd47d + this close-out
```

**Self-assessment: 7/10.** Plus: nothing reached live `main` until it had been verified in a scratch clone. The
merge resolution was checked by line multiset against both parents. The suite ran at every state, with
digit-masked row diffs, which isolated the fork-only test failure at once; its fix was shown to kill a
fence-blind mutant. D10 was proven with real commits under both hooks. The floor was taken at the state a
trimmed ledger returns to, and a 293 reading with Test 9 failing was refused as a floor. The rules also made
two fork-only sentences false, and the plan's own inventory, re-run on the merge, found them. **Minus:** I
recommended the merge before running P5's own `bin/status` criterion on both routes, and that criterion was
the one that told them apart (BL-54). It cost you a third decision, which should have come with the first.
My first D10 question was too dense to decide from, and you had to ask for an explanation. Two commits were
made in a clone without hooks (checked afterwards). I ran two suites in parallel and tripped GitHub's rate
limit, which cost two measurement runs. One ledger entry's wording was corrected before landing. The zsh
word-split trap recurred. **Reduction:** the root `CHANGELOG.md` front matter −959 B; the runner −14 B;
`bin/tests.sh` −504 lines. **Growth:** eleven ledger entries push `CHANGELOG.md` past 262,144 B; plus this
receipt, plan items (12)–(15) and one learning row.

**Predecessor (S177): 7/10.** Its item (1) was exact and shaped the session. The 5-file conflict set held.
*"Contains `64f23bf`, not `6b29d3d`, so decide merge vs port by measuring both"* was the right instruction,
and the pre-flight held too. Gotcha (2) (327 is the 2-receipt value; never loosen for a lone Test 9 failure)
is why the floor was measured correctly. Gotcha (7) (the ledger's headroom) was accurate. **Not 8:** it
tightened `tests-sh-passed` to 327, a floor that includes Test 27's 34 rows, one session before P5, whose
approved D10 deletes Test 27, and did not flag the collision. It named merge vs port without naming plan
hazard 11 (BL-54), which is what a merge of the branch triggers. Gotcha (1)'s *"~17 min"* gate run takes
about 3. **ROI: positive.**

