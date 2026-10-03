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
`grep -c '^```handoff' HANDOFFS.md` and reports the count; **above 2**, the trim is its own action after
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
session: S254
date: 2026-10-03
status: pending
active_task: IMPLEMENT BL-79 P2: the --hook mode of starter-kit/close_out_report.py (Stop and SessionStart decisions, state under .git/ keyed by session_id, fail-quiet), its unit tests from the prototype's ten-row table and six hook mutants, a tightened .quality-gates.json gate, CHANGELOG entry. The operator installs the hook snippet in his own gitignored settings; no .claude file is edited by a session; nothing sent upstream.
```

```handoff
session: S253
date: 2026-10-03
status: complete
self_score: 8
predecessor_score: 9
active_task: **DONE (P1 of BL-79): `starter-kit/close_out_report.py` renders the Phase 3G close-out report from the newest receipt and git and lints any message against the same constants; `tools/test_close_out_report.py` (31 tests) is wired into `bin/tests.sh` and gated in `.quality-gates.json`.** Not done, by design: the hook (P2), the distributed change (P3). Nothing installed, nothing sent upstream.
what_was_done: Phase 0 complete and reported (0 undocumented commits; ratchet 11/11; `check-handoff --all` OK; #91 merged, #92 open with no reply; dashboard 72/100). The operator said go and chose P1 from the picker. Claim `ea9ea6d`. Ported the prototype (`closeout_proto.py`) into the tool with R1-R7 unchanged, a 20-character cap on the outcome word, and refusals that exit 2 (missing, over-long, pipe or newline in a text; newest receipt not complete or unscored). Tests: each rule refused by a corruption (12 mutant tests), render, CLI round trip, a report gone stale after a commit, and a property test over 249 scored complete receipts in the ledger and the shards. Reconciled S252's `commit:` slot to `f6085ab`. All in the close-out commit.
next_steps: **(1) P2, the hook, if he says go**, per plan section 4: add `--hook` mode to `starter-kit/close_out_report.py` (state under `.git/`, keyed by `session_id`, fail-quiet, exit 0 always); turn `docs/planning/close-out-report-prototype/checks.py`'s ten decision-table rows and six hook mutants into unit tests using its `fire()` payload shape; he puts the snippet at plan section 4 P2 in his own gitignored `.claude/settings.local.json`; then four `claude -p` scenarios (rows 1, 2, 5, 6) in a scratch clone, about $0.2-0.3 on haiku; name the model and estimate and ask before a higher rate. **(2) DOGFOOD NOW:** this session's own 3G report should be the tool's output; run `python3 starter-kit/close_out_report.py --check -` on it. **(3) CHECK #92:** `gh pr view 92 --repo KJ5HST/methodology --json state,mergeCommit,comments,reviews`; a maintainer reply outranks everything; ASK before moving tag `v4.2` after it merges. **(4) STILL OPEN:** BL-95 (the resync needs a plan he commissions), BL-91 D3, BL-94, BL-96, the P4 chain. **(5) TRIM:** HANDOFFS.md holds 4 receipts after this one; the policy trims above 2, as its own action after the Phase 0 report (`--cut 2 --force`, then fold the pointer in its own commit). **(6) PUSH:** local `main` is 12 commits ahead of `origin/main`; he declined at S252, so ask only when it matters.
key_files: `starter-kit/close_out_report.py:16` (constants), `:44` (`facts`, pure), `:56` (`live_facts`, the refusals), `:81` (`render`), `:104` (`lint`, R1-R7), `:132` (`main`); `tools/test_close_out_report.py` (`Property` class, the 249-receipt test and the pinned S1 exception; `LintMutants`); `bin/tests.sh` (after the ratchet unit-test row); `.quality-gates.json` (`close-out-report-unit-tests`); the P2 source to port: `docs/planning/close-out-report-prototype/hook_proto.py:8` (`decide`) and `checks.py` (`fire`, the table, the mutants).
gotchas: **(1) 249, NOT 250:** the plan says every complete receipt has numeric scores; the first receipt ever (`docs/archive/HANDOFFS-archive.md`, S1, 2026-07-08) has no `predecessor_score`. The tool refuses to render for it (R4 needs both) and the property test pins it as the one exception. **(2) THE OUTCOME WORD HAS ITS OWN CAP (20):** with six texts at 300 characters the report is 2,111 B against the 2,000 B cap, so an over-long outcome would have passed the per-text check and failed the total. **(3) A COMPLETE RECEIPT IS REQUIRED TO RENDER:** the tool refuses while the newest receipt is `pending`, so the report is printed after the receipt is completed and committed, which is also when its HEAD is right; any later commit makes it stale (R5). **(4) `commit:` SLOT OF THE PREVIOUS RECEIPT:** S252 left it as prose and Test 39 (L1) went red at 361/1; reconcile it at Phase 0 next time the predecessor leaves one. **(5) THE SUITE TAKES ABOUT 10 MINUTES:** run it to a file in the background and wait; `quality_ratchet.py --run` runs it again. **(6)** `dashboard_history.jsonl` and `.context-budget-history.jsonl` are modified by tool runs and left alone.
runtime_smoke: The deliverable is a CLI plus tests, not a harness behavior: `python3 tools/test_close_out_report.py` Ran 31 tests, OK; `python3 starter-kit/close_out_report.py` exercised by the CLI tests (print, check, stale, refusals). Full suite before the slot reconcile: 361 passed / 1 failed (Test 39 L1, S252's slot), output in the session scratch; after it, quality_ratchet: 12/12 pass · 0 fail · 0 unmeasured · results 472fdef97623 · manifest c45a2115d478
changelog_ref: CHANGELOG.md "S253 close-out", "S253 — P1: the close-out report generator and lint", "S253 claim"
commit: 62005872ea5c (close-out, reconciled by S254: S253 wrote the 7-character form, all decimal digits, which check-handoff does not accept as a sha; P1 is b34a841); Phase 3C appended no fork learning, so no retirement is owed (none considered: no row appended); nothing git-pushed; nothing sent to KJ5HST/methodology
```

**3A, S252's handoff: 9/10.** What helped: it named P1 as the next deliverable with the five files, the prototype functions to port with line numbers, the exact `gh pr view 92` command, and the unreconciled `commit:` slot as item (0). Missing: nothing that cost time except that its `commit:` slot stayed prose, which turned `bin/tests.sh` red (361/1) until I reconciled it; and "all 250 receipts have numeric scores" was 249 (the first receipt ever has no predecessor score). Nothing else was wrong.

**3B, self: 8/10.** Right: the tool's rules are the plan's R1-R7 unchanged; every rule is seen refusing a corruption; the property test over the real archive found the 249-not-250 error and the outcome-word overflow before they could bite. Weak: I ran the 10-minute suite twice more than needed (the chicken-and-egg of citing the gate run in the receipt is known and I still paid for it); a P1 commit that is only the five plan files plus a separate close-out would have been cleaner; the tool has not yet printed a real close-out, which is the dogfood in the next step.

```handoff
session: S252
date: 2026-10-03
status: complete
self_score: 8
predecessor_score: 8
active_task: **DONE (a plan only): `docs/planning/close-out-report-actuator-plan.md` costs BL-79, the Phase 3G close-out report: one tool, `close_out_report.py`, that renders and lints the report, plus a Stop and a SessionStart hook; phases P1-P3; decisions D1-D3 were RATIFIED by the operator after the close-out, all as recommended.** Nothing is implemented, installed or sent upstream. The operator asked for "a way to ensure that the Phase 3 close-out report is run and formatted cleanly for display" and chose *generated report + Stop hook* from a picker.
what_was_done: Phase 0 complete and reported (runner and SAFEGUARDS read; 0 undocumented commits at both frontiers; dashboard 72/100). The owed policy trim ran first as its own action: `4cdade2` (3 receipts to `HANDOFFS-through-2026-10-02-2`, shard proof exit 0 from a clone of that commit) and its fold `4d98ccb`; suite 355 passed / 0 failed / 6 skipped. Claim `7ed0ee0`. Prototype and evidence `c7e42ff`: `checks.py` passes 10/10 decision-table rows, 10/10 lint mutants, 6/6 hook mutants. Measured on the real harness (claude 2.1.288, haiku, about nine `claude -p` calls in scratch directories, about $0.25 in all): project hooks run under `-p`; a `{"decision":"block"}` makes the model continue; the harness allows ONE forced retry per Stop chain (`stop_hook_active`); `--continue` keeps the `session_id`; a three-turn session was blocked on turn 1, allowed on turn 2, and re-issued the report after a commit on turn 3. The plan, the BL-79 row and detail, and this receipt are in the close-out commit. Two of my own instruments were wrong and were fixed before the plan relied on them (`close-out-report-prototype/EVIDENCE.md`).
next_steps: **(1) D1-D3 ARE RATIFIED (2026-10-03, all as recommended):** the tool is `starter-kit/close_out_report.py`; the hook goes in the operator's gitignored `.claude/settings.local.json` (he installs it; a session does not edit it); the shape is required and checkable. **(2) P1 is the next deliverable if he says go**, per plan section 4: five files (`starter-kit/close_out_report.py`, `tools/test_close_out_report.py`, `bin/tests.sh`, `.quality-gates.json`, `CHANGELOG.md`); port `closeout_proto.py` (render and lint) and add the property test over all 250 complete receipts. **(3) CHECK #92:** `gh pr view 92 --repo KJ5HST/methodology --json state,mergeCommit,comments,reviews`; a maintainer reply ranks above everything; ASK before moving the `v4.2` tag after it merges. **(4) STILL OPEN:** BL-95 (the resync needs a plan he commissions), BL-91 D3, BL-94, BL-96, the P4 chain. **(0) RECONCILE S252's `commit:` SLOT** to its close-out sha (`git log --format=%h -S'session: S252' -- HANDOFFS.md` finds the first commit where it reads complete); `bin/check-handoff --all` fails L1 until it is done. **(5) PUSH:** local `main` was 8 commits ahead of `origin/main` before this close-out commit (`git rev-list --count origin/main..main`); he answered "not now" to a push at S252, so ask again only when it matters.
key_files: `docs/planning/close-out-report-actuator-plan.md:47` (the shape and its rules), `:89` (when the hook fires, 10-row table), `:118` (what it cannot do), `:160` (phases P1-P3), `:222` (D1-D3); `docs/planning/close-out-report-prototype/hook_proto.py:8` (`decide`), `closeout_proto.py:37` (`render`) and `:46` (`lint`), `checks.py:83` and `:102` (the mutants), `EVIDENCE.md:1` (measured vs documented); the sites P3 would edit: `starter-kit/SESSION_RUNNER.md:293` (3G, 252 B), `starter-kit/SAFEGUARDS.md:176` (the hook section), `bin/_manifest.py:55`; BL-79 at `docs/planning/BACKLOG.md:167` and `BACKLOG-DETAIL.md:3151`.
gotchas: **(1) THE HOOK FORCES ONE RETRY, NOT A LOOP:** the second Stop carries `stop_hook_active: true` and the design honours it, so a model that reprints an unclean report ends the session with only a log line as evidence; measured on haiku, never on Sonnet or Opus. **(2) THE HOOK CONFIG IS THE OPERATOR'S:** do not edit `.claude/settings.local.json` or create `.claude/settings.json` without his go-ahead; no `.claude` file is tracked, and `settings.local.json` is ignored by his GLOBAL git ignore, not this repo's. **(3) TWO DISTRIBUTED FILES ARE ALREADY OVER THEIR CEILINGS:** `SESSION_RUNNER.md` 55,406 B vs 41,364 B, `SAFEGUARDS.md` 17,129 B vs 15,386 B, so any P3 edit is net <= 0 B (the 3G candidate is 239 B against 252 B). **(4) PHASE 0 STEP 5 NAMES A FILE THAT IS NOT HERE:** root `methodology_dashboard.py` does not exist in this repo; run `python3 tools/methodology_dashboard.py`. **(5) A LIVE FIXTURE MUST COME FROM `git show HEAD:<file>`, NOT A WORKING TREE:** my first three-turn run copied a ledger an earlier run had already completed, so the hook correctly stayed silent and the run proved nothing. **(6) A FAIL-QUIET WRAPPER HIDES A CRASHING MUTANT:** one mutant "failed" by raising inside the wrapper and so passed for the wrong reason; build mutants that change the decision, not ones that crash. **(7) MY CLAIM STUB WAS INSERTED INTO THE FRONT-MATTER PROSE:** I located the insertion point with `s.index('```handoff')`, whose first hit is the sentence `grep -c '^```handoff'`, so claim commit `7ed0ee0` split it; only the 3E suite run caught it (`check-handoff --all`, Test 39 A2); insert at a LINE-ANCHORED fence, and run the suite once after the claim. **(8)** `dashboard_history.jsonl` and `.context-budget-history.jsonl` are modified by tool runs and left alone.
runtime_smoke: No runtime behavior of the framework changed (a plan and a labelled prototype under docs/planning/; no hook, setting, manifest row or distributed file was touched). Prototype: `python3 docs/planning/close-out-report-prototype/checks.py` exit 0. Full suite with this receipt in place (3 receipts, so Test 34 runs): 361 passed / 0 failed / 0 skipped, measured by the ratchet's tests-sh gates; the earlier red runs on the way (358/3, then 360/1) were my split front-matter sentence and S251's unreconciled `commit:` slot, both fixed here; `bin/check-handoff --all` OK; quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 95b5ea74bd7c · manifest 01a4ae7aa511
changelog_ref: CHANGELOG.md "S252 close-out — plan for a generated 3G close-out report plus a Stop hook"
commit: f6085ab (close-out, reconciled by S253); Phase 3C appended no fork learning, so no retirement is owed (rows considered: #16, #33 and #41, which already hold the mutant-blind-spot and live-fixture lessons); nothing git-pushed; nothing sent to KJ5HST/methodology
```

**3A, S251's handoff: 8/10.** What helped: the ordered next steps with the exact `--cut 2 --force` command, the `gh pr view` command for #92, and the 3-commits-ahead figure, which I re-measured as 4 with its close-out. Nothing in it was wrong. Missing: item 3's picker text was "drafted in an earlier turn" and exists in no file, so I rebuilt the candidate list; it did not note that Phase 0's dashboard command needs `tools/`; and it did not say its own `commit:` slot (prose, not a sha) would fail `check-handoff --all` until I reconciled it, which I learned from the suite rather than the handoff.

**3B, self: 8/10.** Right: the deliverable was confirmed with the operator before work; every plan number was run, not reasoned (a spike, a three-turn live session, 26 mutants); two instrument errors were found and fixed before the plan used them; a check of the plan against the repo corrected a wrong line anchor and a memory-only reference. Wrong or weak: I spent about $0.25 of the operator's tokens on nested `claude -p` runs and stated the figure only after the fact; the first live three-turn run was vacuous from a bad fixture; the prototype code is committed under docs/planning/, which is borderline for a session whose rule is "the plan is the deliverable", defensible only because it is labelled evidence and nothing ships.

