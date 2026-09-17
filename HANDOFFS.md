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

**Archived 2 record(s), 2026-09-17 → 2026-09-17** into [`docs/archive/HANDOFFS-through-2026-09-17-2.md`](docs/archive/HANDOFFS-through-2026-09-17-2.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/HANDOFFS-through-2026-09-17-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-17-2.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

```handoff
session: S183
date: 2026-09-17
status: pending
self_score: pending
predecessor_score: pending
active_task: **REPAIR `bin/tests.sh` TEST 38'S PLANT-LANDING CHECK, WHICH A RECEIPT THAT MERELY QUOTES THE PLANTED NAME FALSIFIES.** The planter asks `"phantom_drift" in reblocks[0]["content"]` (`bin/tests.sh:2548`) to decide which side of the closing fence its plant landed on. S182's own receipt quotes that string inside its `what_was_done` field (`HANDOFFS.md:60`), so the check reports *inside the fence* for a plant made below it and assertion (8b) refuses to run: `PLANT MISSED: aimed at 'prose' but inside-the-fence is True`. Chosen by the operator after Phase 0 (picker), which also authorized the `HANDOFFS.md` retention trim. Fork-local; nothing upstream.
what_was_done: pending
next_steps: pending
key_files: `bin/tests.sh:2548` (the landing check), `:2523`-`:2551` (the planter), `:2553` (`plant38`, which always reads the live ledger), `:2561` ((8b)), `:2572` ((8c)); `bin/check-handoff:227` (`scan`, whose `line` and `content` give the record's extent in lines); `tools/fixtures/handoff-ledger-2-records.md` (the frozen fixture); `HANDOFFS.md:60` (the quote that fires it)
gotchas: **The gate was red BEFORE this session touched anything** - `9/10 pass · 1 fail · 0 unmeasured · results aff8a2e08e15 · manifest 3a87b16f1b31` in a `--no-local` clone of `5ae7902`, against S182's `10/10 · results 83c5e3fed6f3` measured one commit earlier at `b25fc19`. The manifest digest is unchanged, so no threshold moved and none may be moved to clear it. Planting through `bin/check-handoff`'s own `scan()` at `git show <rev>:HANDOFFS.md` pins the flip to `93656a1`, S182's close-out commit: the same BL-64 window, two sessions running. This claim names the marker deliberately, so the live-ledger control stays red until the fix lands rather than being cleared by a quieter claim.
runtime_smoke: pending
changelog_ref: CHANGELOG.md "2026-09-17 · [BL-64] S183 claim"
commit: pending
```

```handoff
session: S182
date: 2026-09-17
status: complete
self_score: 7
predecessor_score: 7
active_task: **`bin/tests.sh` TEST 38'S DRIFT GUARD IS REPAIRED (`4c6da50`); THE QUALITY GATE IS GREEN AGAIN ON `main`. THREE FINDINGS RAISED: BL-64, BL-65, BL-66 — THE LAST IS UPSTREAM-FACING AND SITS IN `README.md`'s QUICK START.** Phase 0 found the gate red at `29b0feb` although S181's receipt cited `10/10 pass`: the guard measured a receipt from its opening fence to the NEXT receipt's, so the close-out prose between them read as receipt fields. Chosen by the operator after Phase 0 (picker), which also authorized the push to `origin` and the raising of backlog items. Nothing sent upstream. **P7 (`wsfct`) was done by `wsfct`'s own S630 while this session ran; recording it here is the next session's item (1).**
what_was_done: **Phase 0:** `CHANGELOG.md` frontier `29b0feb` = HEAD, no gap; `HANDOFFS.md` frontier `473c83d`, one commit behind and that commit is S181's authorized push record, so nothing backfilled. 2 receipts, no trim owed. **S181's gate citation did NOT re-run:** `8/10 pass · 2 fail · results 9ccbc3cb49b6 · manifest 3a87b16f1b31` in a `--no-local` clone of `29b0feb`, against its cited `10/10 pass · results 330ab6a19d4b` at `755fe0d`. Same manifest digest, so no threshold moved. Single failing assertion, Test 38's drift guard, bisected on the guard's own logic: `OK` at `755fe0d`/`b0bf91f`, `['applied']` at `473c83d`/`29b0feb`, `OK` again at `45bf347`. The dashboard read 76/100 with one HIGH flag naming both breached gates — a second instrument, same reading. **`45bf347`** claim. **`4c6da50`** the fix: the guard loads `bin/check-handoff` and calls its `scan()`, fence-bounded and fence-nesting aware; two assertions added, written RED first and RUN red in their final home (`FAIL: drift guard: prose below the closing fence reached the comparison as: phantom_drift`), and the planter re-reads the artifact through `scan()` to refuse a plant that landed on the wrong side of the fence. **`0f03f0e`** BL-64, **`89ef2ab`** BL-65, **`b25fc19`** BL-66, each with its own tagged ledger entry. **BL-66 was measured, not reasoned:** a scratch `git init` adopter installed from upstream `008d656` and never edited got exit 2 and nine false *"local modifications"* from the route `README.md:61` prescribes, and exit 0 with 10 files written from `--source=local`. **This close-out:** fork Learning #75, this receipt, the ledger entry.
next_steps: **(1) RECORD P7 HERE**, as S180 recorded P6 (plan `docs/planning/changelog-rules-contradictions-plan.md:799`). `wsfct`'s S630 did it today on branch `chore/s630-methodology-bl57-p7`, `790c77d1`..`3a257097`, six commits, tree clean, pushed to that project's `origin`, not merged; the sync is ONE commit (`8a41741c`, 14 files from fork `main` `29b0feb`), which is decision (18) applied. Check its claims read-only from here first, then write the plan status line, a P7 block and the BL-57 row. Verified from here at this close-out: `bin/sync ../wsfct --source=local --dry-run` exits 0 with all 23 files `unchanged`. **(2) THEN P8, `vscode_quarto_ext`** (plan `:800`), run from that project as its own session; re-derive its line numbers at the claim, since P6's went stale (item (17)). **(3) BL-66 WANTS AN UPSTREAM PR AND IS THE FIRST THING A NEW ADOPTER READS** — it is also P10's opening decision in disguise: `nprcgenekeepr`'s sync is blocked by one locally modified file, and option (a) there is to send the extension upstream. **(4) Push, authorized:** fork `main` goes to `origin` right after this close-out commit; its record follows under the standing grant. **(5) The next Phase 0 finds 3 receipts, so a retention trim IS owed** after the report — `--cut 2 --force` once this session's claim makes four (gotcha (2) of S181; `HANDOFFS.md`'s header still says `--cut 1`, which fits only a trim before any claim). **CARRIED:** BL-61; BL-60 (folds BL-36); BL-62 and #80's F5 ride P12; BL-54's PR; BL-63; `README.md`'s stale cost section (plan item (15)); the runner and `SAFEGUARDS.md` stay `over` budget.
key_files: `bin/tests.sh:2469` (the guard's comment, rewritten), `:2502` (the fence-bounded parser), `:2523` (the planter), `:2555`/`:2561`/`:2572` ((8a)/(8b)/(8c)); `bin/check-handoff:227` (`scan`, the borrowed parser), `:360` (`parse_block`, whose docstring named this hazard first); `tools/fixtures/handoff-ledger-2-records.md:10`; `docs/planning/BACKLOG.md:157` (BL-64), `:158` (BL-65), `:159` (BL-66); `docs/planning/BACKLOG-DETAIL.md` §BL-64/65/66; `docs/FORK_LEARNINGS.md:87` (#75); `README.md:61` (BL-66's sentence); `bin/sync:100` (the historyless GitHub fetch), `:117`–`:130` (the precedent for fixing this class); `starter-kit/BOOTSTRAP.md:86` (the contradicting advice); `tools/test_context_budget.py:340` (the transcript slug), `:355` (the narrow skip probe), `:372` (the failing test)
gotchas: **(1) `bash bin/tests.sh` IN THIS WORKING TREE READS `312 passed, 1 failed`; A `--no-local` CLONE READS `10/10 pass · 0 fail`. BOTH ARE HONEST.** The failure is `tools/test_context_budget.py`'s fit-gate presence control, which reads this machine's Claude Code transcripts and so SKIPS in every clone (BL-65). Do not read the live-tree red as a regression, and do not chase it while doing something else. **(2) THE CLONE IS THE CITATION, BY `HANDOFFS.md` §Citing the gate run** — and BL-64 records that the clone can never cover the close-out commit itself. **(3) A BARE GREP FOR `tests.sh` IN `bin/_manifest.py` RETURNS A MATCH THAT IS A COMMENT** (`:109`). The distributed set is the tuple list at `:37` onward; `bin/tests.sh` is not in it. **(4) 3 RECEIPTS NOW, SO A TRIM IS OWED NEXT PHASE 0** — and it is `--cut 2 --force` after the claim, not `--cut 1`. **(5) `tests-sh-passed` READS 313 AT 3 RECEIPTS** on the fixed tree (305 floor). Never tighten from a working-tree run. **(6) PHASE 0 WRITES A TRACKED ROW** (`context_budget.py --status` → `.context-budget-history.jsonl`); it rode `45bf347`. **(7) RUN SUITES ONE AT A TIME** (Test 9, GitHub rate limit; `gh api rate_limit` read 5000/5000 before the final run). **(8) `git fetch upstream origin` FETCHES A REF NAMED `origin` FROM `upstream` AND FAILS;** fetch each remote separately. **(9) NO `git add -p` HERE:** the three backlog commits were kept separate by writing one item at a time, not by partial staging.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `quality_ratchet.py --run` (which runs `bash bin/tests.sh`) IN A `--no-local` CLONE WITH HEAD ASSERTED.** **Final, clone of `b25fc19`: `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results 83c5e3fed6f3 · manifest 3a87b16f1b31`**, `tests-sh-passed` 313 at 3 receipts. The Phase 0 run on `29b0feb` was `8/10 pass · 2 fail · results 9ccbc3cb49b6`, which is the defect this session fixed; the clone of `4c6da50` already read `83c5e3fed6f3`. On the live tree after the commits: `bin/check-handoff --all --allow-pending` 0 on 3 receipts; `bin/check-links` 0; `docs/planning/BACKLOG-DETAIL.md.verify.sh` 0; `docs/planning/BACKLOG-archive-2026-08-15.md.verify.sh` 0; `docs/archive/HANDOFFS-through-2026-09-17.md.verify.sh` 0; `bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations` 0 with row 75. **Adopters, read-only, each with `git status --porcelain` identical before and after:** `bin/sync ../wsfct --source=local --dry-run` exit 0, 23 unchanged; `bin/sync ../nprcgenekeepr --source=local --dry-run` exit 2 on `methodology_trim.py` alone; the same two on `--source=github` exit 2 on 7 and 10 files; `bin/status ../nprcgenekeepr`. **A scratch adopter was built and synced in the scratchpad for BL-66** (upstream `008d656` → `6b29d3d`), outside every tracked repository. **NOT EXERCISED:** any real sync, any upstream action, `tools/test_context_budget.py`'s fit-gate test in a clone (it skips there), CI (none).
changelog_ref: CHANGELOG.md "2026-09-17 · [BL-64] S182 close-out", plus the claim, the fix, and the three raising entries
commit: 45bf347 (claim) + 4c6da50 (the fix) + 0f03f0e (BL-64) + 89ef2ab (BL-65) + b25fc19 (BL-66) + this close-out
```

**Self-assessment: 7/10.** Plus: Phase 0 caught a gate the previous close-out had certified green, and pinned it to
one commit and one line before anything was touched, on the guard's own logic rather than by re-running a suite four
times. The new assertions went in with the broken parser still in place and were RUN red in their final home, so the
RED-first claim is a log line, not an argument. The fix borrows `bin/check-handoff`'s `scan()` instead of re-deriving
a third record-extent rule, which is what makes the class fixed rather than the instance, and the mutant assertion
keeps the guard killable. When the operator asked whether the sync routes were broken, I built a clean-room adopter
instead of reasoning from the documents, which turned a plausible "both fail" into a measured upstream defect with a
control. I also caught my own bare-grep false positive on `bin/_manifest.py` before it reached a claim.
**Minus:** my Phase 0 report was written in this repository's private shorthand — *frontier*, *gap 0*, *standing
grant*, *receipt*, *citation*, *manifest digest* — and cost the operator two rounds of decoding before any work
could proceed. One of those sentences was also garbled. The instruction to name files and documented practices
instead is now recorded, but the cost was already paid, and it is the same reader-side reachability failure this
repository files against its own corpus. **Growth:** six ledger entries, three backlog items with detail bodies,
fork Learning #75, this receipt, ~103 net lines in `bin/tests.sh`. **Reduction:** none.

**Predecessor (S181): 7/10.** Its gotchas were the useful part and every one that applied held. Gotcha (4) predicted
that Phase 0 writes a tracked row, and it did — named in the report and ridden by the claim. Gotcha (6) (suites one
at a time) and gotcha (7) (`git fetch upstream origin` fails) were both applied without rediscovery. Item (4), *"the
next Phase 0 here finds 2 receipts: no trim"*, was exactly right. Item (1)'s start check for `wsfct` was the right
instruction for the right reason, and its `git status` discipline is what let this session confirm P7 cleanly.
**Not 8:** its `runtime_smoke` asserted `10/10 pass · 0 fail` for a tree that was already red, and gotcha (3)
predicted *"`tests-sh-passed` READS 305 AT 2 RECEIPTS"* when the tree it shipped read 304. Both were measured before
the close-out commit existed, which is structural and is now BL-64 — but `SESSION_RUNNER.md` 3D already requires a
forward-looking claim to be derived or labelled a guess, and gotcha (3) was stated as fact about a tree that did not
yet exist. Its item (1) also assumed P7 would need a session here to start it; `wsfct` ran it itself the same day,
which S181 could not have known and did not claim. **ROI: strongly positive** — the gotchas alone saved more than
the miss cost, because the miss was the thing this session was assigned to find.


