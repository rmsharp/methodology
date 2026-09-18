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
session: S186
date: 2026-09-17
status: complete
self_score: 7
predecessor_score: 9
active_task: **`HANDOFFS.md` IS TRIMMED (`67c3e10`, pointer moved to the index `fbc1aaf`), AND BL-57 PLAN ITEM (21) IS DECIDED AND RECORDED: P8–P11 ALSO MIGRATE A STALE `HANDOFFS.md` SEED (`6bae791`, route corrected at `102d5ef`), WITH ITEM (22) RAISED FOR P12.** The operator chose it in the picker after Phase 0: carry it in P8–P11. The route is `starter-kit/BOOTSTRAP.md:386`'s: bring the seed's `## Size, and when to archive` section in above the first receipt, and leave the rest in place. `6bae791` first wrote `bin/status`'s *replace the text above the first receipt* instead; `102d5ef` corrected it, and item (22) records that the two fork-side instructions disagree, which P12 would otherwise ship. The same picker gave the go-ahead to push fork `main` to `origin` after this close-out. Nothing upstream. **Next: P8 (`vscode_quarto_ext`), from that project, as its own session.**
what_was_done: **Phase 0:** `CHANGELOG.md` frontier `9ee08a1` = HEAD, no gap. `HANDOFFS.md` frontier `2d226c1` is one commit behind, and that commit is S185's gate record, with no receipt by design. Nothing backfilled. 3 receipts, so the trim was owed. S185's citation re-ran in a `--no-local` clone of `9ee08a1`: `10/10 pass · results 4433567c1f55`, identical. Dashboard 76/100, no high flags. `vscode_quarto_ext` read-only: `master` `58f7bcbd`, only `scratchpad/` untracked, as S185 recorded. **`34434b4`** claim, carrying Phase 0's two tracked rows. **`67c3e10`** trim, `methodology_trim.py --cut 2 --force`: S183 and S182 to `docs/archive/HANDOFFS-through-2026-09-17-3.md` (`-3`: the third shard named for this date), 39,271 → 16,943 B; its `.verify.sh` exit 0 before the commit, and `check-handoff --all --allow-pending` and `--archived --file` on the shard pass. **`fbc1aaf`** pointer block → index row, 16,943 → 16,487 B (`wc -c`). **`6bae791`** item (21) recorded: the plan's status line, item (21), a bullet under step 3 of P6–P11, a DONE item, the P8 and P9 rows, and §9.8's script, which gains an optional file argument defaulting to `CHANGELOG.md`, so the two-argument form P6/P7 ran is unchanged. The BL-57 row in `docs/planning/BACKLOG.md` names the decision. Measured with `bin/status <project> --source=local` from `fbc1aaf`: `HANDOFFS.md` stale in `vscode_quarto_ext` and `mts-system`, `present` in `nprcgenekeepr` and `airqino`, absent in `model_project_constructor`; also stale in `wsfct`, which is outside the decision. **`102d5ef`** correction: step 3's bullet, item (21)'s paragraph, the DONE item and the P8/P9 rows now follow `BOOTSTRAP.md:384`–`386` (add the section) instead of `bin/status:231`–`236`'s *replace* note, which in `vscode_quarto_ext` would delete the trimmer's pointer block and its count sentence (BL-48). That disagreement is item (22). §9.8 tested in a `--no-local` clone: the insertion `34434b4` passes `53 53 HANDOFFS.md`; the removal `fbc1aaf` fails `10 10 HANDOFFS.md`, naming `(53, 4)`. **Found in `mts-system`, recorded in the P9 row:** a `handoff` fence opened at `:216` never closes, and `bin/check-handoff --all --file` reads it and `:219` as one block. **This close-out:** fork Learning #78, this receipt, the ledger entry.
next_steps: **(1) P8 — `vscode_quarto_ext`, from that project, as its own session** (the P6–P11 procedure is at plan `docs/planning/changelog-rules-contradictions-plan.md:825`, step 3's `HANDOFFS.md` bullet at `:837`, the DONE item at `:857`, the P8 row at `:873`, §9.8 at `:1088`). P8 now migrates **both** seeds. `CHANGELOG.md`: replace the Keep-a-Changelog header (`:1–8`), keeping the shard pointer. `HANDOFFS.md`: bring the seed's `## Size, and when to archive` section in above its pointer block (`:29–31`), below which the first receipt sits at `:33`, and keep the count sentence (`:20–22`) and the project's own warning (`:23–27`). Each migration is its own commit, and §9.8 runs on each. These are readings on `58f7bcbd` at S186; re-derive them by content at the claim, and run `git status --porcelain` there first. **(2) ITEM (22), BEFORE P12:** align `bin/status:231`–`236`'s note with `starter-kit/BOOTSTRAP.md:384`–`386` (for `HANDOFFS.md`, bring across the section). It is fork-side and was written by P1 (`2d5dc6e`). No test pins its wording (`grep` of `bin/tests.sh` and `tools/*.py` finds none), so a change needs a new assertion, not an edited one. It is small enough to go into a session here before P12, or into P12 itself. **(3) NO TRIM OWED at the next Phase 0:** this close-out leaves 2 receipts. **(4) OUTWARD, EACH ITS OWN GO-AHEAD:** BL-66's upstream PR; P12 (BL-62, BL-63, #80's F5, and now item (22)). Fork `main` is pushed to `origin` after this commit under this session's go-ahead. **(5) SMALL AND FOUND, NOT FIXED:** the open list at `docs/planning/BACKLOG.md:9`–`11` still omits BL-63, whose row is at `:156`; the six stale line numbers at `bin/tests.sh:2752`; `wsfct`'s `HANDOFFS.md` seed, stale and outside the decision (the operator's to raise). **CARRIED:** BL-61, BL-60 (folds BL-36), BL-65, BL-54's PR, `README.md`'s stale cost section (plan item (15)). The runner and `SAFEGUARDS.md` remain `over` budget.
key_files: `docs/planning/changelog-rules-contradictions-plan.md:9` (status line: item (21) decided), `:239` (item (21)), `:247` (the decision), `:256` (item (22)), `:825` (P6–P11), `:837` (step 3's `HANDOFFS.md` bullet), `:857` (the DONE item), `:873` (P8), `:874` (P9, with `mts-system`'s unclosed fence), `:1088` (§9.8, the optional third argument); `docs/planning/BACKLOG.md:151` (BL-57); `bin/status:231` (the *replace* note); `starter-kit/BOOTSTRAP.md:386` (the *bring across* route); `bin/_manifest.py:117` (the marker); `starter-kit/methodology_trim.py:337` (the regenerated count field); `docs/HANDOFFS_ARCHIVE_INDEX.md:55` (the new row); `docs/archive/HANDOFFS-through-2026-09-17-3.md` and its `.verify.sh`; `docs/FORK_LEARNINGS.md:90` (#78); in `~/Development/vscode_quarto_ext`: `HANDOFFS.md:20`, `:29`, `:33`; in `~/Development/mts-system`: `HANDOFFS.md:32` (the old seed's example), `:77` (first receipt), `:216` (the unclosed fence)
gotchas: **(1) TWO INSTRUCTIONS FOR THE SAME MIGRATION, AND THE ONE ON SCREEN IS THE WRONG ONE FOR `HANDOFFS.md`.** `bin/status` prints *replace the text above the first entry (or receipt)*; follow `BOOTSTRAP.md:386` instead (add the section) until item (22) aligns them. `6bae791`'s ledger entry describes the replace route, and it stands as written: the correction is `102d5ef`. **(2) `grep -n '^```handoff'` FINDS AN EXAMPLE BEFORE A RECEIPT IN `mts-system`** (`:32`, inside a four-backtick wrapper), so the first receipt has to be found fence-aware. `vscode_quarto_ext`'s own front matter warns the same about `grep -c`. **(3) §9.8 ON AN INSERTION:** pass the insertion line as both bounds. An insertion hunk removes nothing and always passes; a removed line outside the bounds fails. **(4) `mts-system`'s `HANDOFFS.md` IS 373,021 B**, past the 262,144 B read refusal, so read it with an offset and a limit. Its unclosed fence at `:216` predates P9; don't attribute it to P9. **(5) `tests-sh-passed` READS 309 AT 2 RECEIPTS** (315 at 3); the floor is 305, and a post-claim run reads higher, so never tighten the floor from one. **(6) PHASE 0 WRITES TWO TRACKED ROWS** (`.context-budget-history.jsonl`, `dashboard_history.jsonl`); they rode `34434b4`. **(7) NEVER PUT `git checkout <sha>` IN A MEASUREMENT COMMAND ON THE LIVE TREE:** it detached HEAD here mid-session. Nothing was lost, because only unmodified files switched, but test in a `--no-local` clone.
runtime_smoke: **NO APPLICATION. THE BUILD-EQUIVALENT IS `quality_ratchet.py --run` (which runs `bash bin/tests.sh`) IN A `--no-local` CLONE WITH HEAD ASSERTED.** **Citation, clone of `102d5ef`: `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results 8e12f40caec1 · manifest 3a87b16f1b31`**, `tests-sh-passed` 309 at 2 receipts. That is S183's digest at 2 receipts; `6bae791` read the same. The close-out commit is not covered by that run (BL-64), so it is re-measured in a clone of itself after it lands and recorded as its own ledger entry. On the live tree: the shard's `.verify.sh` exit 0 before the trim commit and after the fold; `bin/check-handoff --all --allow-pending` 0 on 2 receipts; `bin/check-links` 0 (110 links, 23 files) after each commit; `bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations` 0 with row 78. In the adopters, read-only: `bin/status` on six projects, and `bin/check-handoff --all --file ../mts-system/HANDOFFS.md`. **NOT EXERCISED:** any adopter write; the migration route itself on an adopter's `HANDOFFS.md` (P8's to run); any upstream action; CI (none).
changelog_ref: CHANGELOG.md "2026-09-17 · [BL-57] S186 close-out", plus the claim, trim, fold, item (21) and correction entries
commit: 34434b4 (claim) + 67c3e10 (trim) + fbc1aaf (fold) + 6bae791 (item (21)) + 102d5ef (route corrected, item (22)) + this close-out
```

**Self-assessment: 7/10.** Plus: the trim and the pointer move each ran their proof before and after their commits,
and the pointer move's size is a `wc -c` reading, not a subtraction. I re-read all six adopters' seed verdicts
instead of carrying S185's, and read the two in-scope files by content, so the P8 and P9 rows name real lines and
what to keep. That reading found `mts-system`'s unclosed fence, pinned with `check-handoff`'s own message. The §9.8
change keeps the old call form, and I tested it both ways, on a pass and on a fail. **Minus, three self-inflicted
repairs:** (1) I wrote `bin/status`'s *replace* route into the plan without grepping for the guide's instruction, and
committed it (`6bae791`). My first draft even carried special cases to protect the lines the route would destroy,
which should have been the signal. It was caught before close-out and corrected at `102d5ef`, but that took one extra
commit and ledger entry, and fork Learning #78 records it. (2) A measurement command ended with `git checkout 67c3e10`
on the live tree and detached HEAD. Nothing was lost; I checked before and after returning to `main`. (3) One edit
duplicated the P9 row, and I removed it with a guarded script. **Growth:** six ledger entries plus the gate record,
~30 plan lines, a learnings row (~1.3 KB). **Reduction:** `HANDOFFS.md` 39,271 → 16,487 B.

**Predecessor (S185): 9/10.** Every reading I re-checked held. The count was 3 receipts with the trim owed, and the
`--cut 2 --force` shape and the `-3` shard name came out as its trim-state record predicted. It said `tests-sh-passed`
would read 315 at 3 receipts, and it did. `vscode_quarto_ext` was at `58f7bcbd` with only `scratchpad/` untracked.
The six seed verdicts in item (21) were exactly what `bin/status` printed today. Fork `main` was 15 ahead. `BACKLOG.md`'s
open list does omit BL-63. Framing item (21) as the operator's call, with the measurements attached, let the decision
be made in one picker. **Not 10:** item (21) framed the question as *who owns it*, not *how to migrate it*. No note
said that the migration's two written routes disagree, or that `vscode_quarto_ext`'s front matter holds lines a
trimmer owns. That is hindsight, and it is where my correction came from. **ROI: strongly positive.**

```handoff
session: S185
date: 2026-09-17
status: complete
self_score: 8
predecessor_score: 8
active_task: **BL-57's P7 (`wsfct`) IS RECORDED HERE (`313459c`) AND BL-67 IS CLOSED (`aee4771`). THE RECORDING WAS RE-VERIFIED FROM `wsfct`'s GIT OBJECTS, NOT RE-APPLIED FROM THE REVERTED `a6320ae`, AND ONE OF ITS CITATIONS TURNED OUT TO HAVE BEEN FALSE WHEN IT WAS WRITTEN.** It named `origin/chore/s630-methodology-bl57-p7` as where the six commits survive. GitHub deleted that branch at 00:36:55Z, two seconds after PR #903 merged and eight minutes before `a6320ae` was committed; what resolved was `wsfct`'s local remote-tracking ref. The commits live at `refs/pull/903/head` (`3a257097`), and plan item (20) now says to cite that ref (fork Learning #77). Chosen by the operator after Phase 0 (picker). Nothing sent upstream, nothing written in `wsfct`. **Next: P8 (`vscode_quarto_ext`), run from that project as its own session.**
what_was_done: **Phase 0:** `CHANGELOG.md` frontier `19eb19b` = HEAD, no gap; `HANDOFFS.md` frontier `61eb9ab`, one behind, and that commit (BL-67 raised) carries its own ledger entry and no receipt by design — nothing backfilled. 2 receipts, no trim owed. Gate in a `--no-local` clone of `19eb19b`: `10/10 pass · results 8e12f40caec1`, the digest S183 cited. Dashboard 76/100, no high flags. Numbered S185 because the reverted claim used S184. **`4cb67c6`** claim, carrying Phase 0's two tracked rows. **Re-verification**, `wsfct` `git status --porcelain` empty before and after, reading git objects only: six commits `790c77d1`..`3a257097`; PR #903 `MERGED` 2026-09-18T00:36:53Z as `66e14daa`, parent `55c293f7`; `git diff 3a257097 66e14daa` empty; `8a41741c` holds 15 files, its `CHANGELOG.md` change only its 7-line entry; the plan's own §9.8 script on `12fb758e` prints *only the block changed* for 8–182 and names `(8, 1), (10, 172)` for the row's 13–196; the block holds 5 `### ` lines and 3 audit matches, and the commit adds 1; headings 75 → 71; audit 72 → 70 live and 132 → 130 with the three shards; `bin/status ../wsfct` `present`, every tracked file `current`; `bin/sync --dry-run` exit 0, 23 unchanged; the six adopters' seed verdicts identical to S184's. **Added from S630's receipt and checked here:** the row's 13–196 would have deleted three archive-pointer blocks (item (19)); `wsfct`'s three shard proofs fail — all v1.1.2-generated, L1/L3 record counts 12/8, 37/35, 29/28, identical at `55c293f7` before P7 and `66e14daa` after — BL-36's class, noted in the P7 block, no new item. **`313459c`** the recording: status line, the P7 block, the P7 row with its range struck, the procedure's stale `130 → 127` struck for `132 → 130`, the BL-57 row naming P8. **`aee4771`** BL-67 closed: row to §Completed items, closing note in `BACKLOG-DETAIL.md`. **This close-out:** item (20)'s wording corrected (it said *"by S185 GitHub had deleted it"*, as if it went stale; the PR's event timeline says it was never true), fork Learning #77, this receipt, the ledger entry.
next_steps: **(1) P8 — `vscode_quarto_ext`, from that project, as its own session** (plan `docs/planning/changelog-rules-contradictions-plan.md:843`, procedure `:808`, §9.8 `:1058`). Measured read-only at this close-out, labelled as readings with a time on them (fork Learning #74): on `master` `58f7bcbd`; `git status --porcelain` shows only an untracked `scratchpad/`, no staged claim; it has no merged PRs, so it commits straight to `master` and item (20) does not apply unless that changes; `bin/sync ../vscode_quarto_ext --source=local --dry-run` exits 0 and would write 14 files; `CHANGELOG.md` has the Keep-a-Changelog header at :1–8 (through `## [Unreleased]`), a v1.1.1 trimmer pointer block at :10–12, and 21 `### ` lines; `.context-budget.json:49` lists `CHANGELOG.md` (the row says drop it, Q2 A, the project's call). **Re-derive the block by content at the claim** (item (19)); re-run `git status --porcelain` there first. **(2) THE NEXT PHASE 0 OWES A `HANDOFFS.md` TRIM:** this close-out leaves 3 receipts (S185, S183, S182). **(3) ITEM (21) IS THE OPERATOR'S CALL:** the `HANDOFFS.md` seed that P6/P7 leave *(stale format)* and no item owns — carry it in P8–P11, raise it as its own item, or leave it. **(4) OUTWARD, EACH ITS OWN GO-AHEAD:** fork `main` is 13 commits ahead of `origin` before this close-out — 15 once it and its post-close-out gate record land — unpushed; BL-66's upstream PR; P12 (BL-62, BL-63, #80's F5). **(5) SMALL AND FOUND, NOT FIXED:** `docs/planning/BACKLOG.md:9`–`11`'s hand-maintained open list omits BL-63, whose row is at `:156`; `bin/tests.sh:2752`'s six stale line numbers (carried from S183). **CARRIED:** BL-61 (scheduled small session), BL-60 (folds BL-36), BL-65, BL-54's PR, `README.md`'s stale cost section (plan item (15)); the runner and `SAFEGUARDS.md` stay `over` budget.
key_files: `docs/planning/changelog-rules-contradictions-plan.md:7` (status line), `:212` (the P7 block), `:226` (19), `:231` (20, corrected at this close-out), `:239` (21), `:247` (the BL-36-class note), `:831` (the struck `130 → 127`), `:842` (the P7 row), `:843` (the P8 row), `:808` (the P6–P11 procedure), `:1058` (§9.8); `docs/planning/BACKLOG.md:151` (BL-57), `:166` (BL-67, completed); `docs/planning/BACKLOG-DETAIL.md:2347` (BL-67's closing note); `docs/FORK_LEARNINGS.md:89` (#77); in `~/Development/wsfct`: `66e14daa` (the squash on `master`), `refs/pull/903/head` = `3a257097` (the six commits), `12fb758e` (the header migration)
gotchas: **(1) ASK THE REMOTE, NOT A LOCAL REF.** In `wsfct`, `git branch -a` still lists `remotes/origin/chore/s630-methodology-bl57-p7` and `git rev-parse` resolves it; `git ls-remote origin` and GitHub say the branch does not exist. `wsfct` has `delete_branch_on_merge` on; `vscode_quarto_ext` has it off. **(2) THE PLAN'S LINE NUMBERS MOVED:** +2 above the P7 block (the status line grew; the P6 block `:175` → `:177`) and +43 below it (the P7 row `:799` → `:842`, §9.8 `:1015` → `:1058`); S183's handoff and the pre-S185 receipts cite the old ones. **(3) THE AUDIT HAS TWO FORMS** — the live file alone (72 → 70) and live plus shards (§9.2's form, 132 → 130); the procedure's figure is the second. Name the form beside the number. **(4) 3 RECEIPTS NOW, SO `tests-sh-passed` READS 315, NOT 309** — six stated skips become assertions at three receipts; never tighten the floor (305) from this reading. **(5) `vscode_quarto_ext`'s SHARD PROOF WAS WRITTEN BY TRIMMER v1.1.1**, older than `wsfct`'s — an estimate, not run: expect it to fail as BL-36's class, and check it before P8 rather than attribute it to P8. **(6) PHASE 0 WRITES TWO TRACKED ROWS** (`.context-budget-history.jsonl`, `dashboard_history.jsonl`); they rode `4cb67c6`.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `quality_ratchet.py --run` (which runs `bash bin/tests.sh`) IN A `--no-local` CLONE WITH HEAD ASSERTED.** **Citation, clone of `aee4771`: `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results 4433567c1f55 · manifest 3a87b16f1b31`**, `tests-sh-passed` 315 at 3 receipts. The close-out commit is not covered by that run (BL-64), so it is re-measured in a clone of itself after it lands and recorded as its own ledger entry, as S183 did. On the live tree: `bin/check-links` 0 (110 links, 23 files) after each commit; `BACKLOG-DETAIL.md.verify.sh` 0 after the append; `bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations` 0 with row 77; `bin/check-handoff --allow-pending` 0 on the claim. In `wsfct`, read-only: the §9.8 script, `bin/status`, the sync dry run and the three shard proofs (these in a `--no-local` clone, at two commits). **NOT EXERCISED:** `wsfct`'s own build (the DONE item rests on S630's receipt: no `web/` code touched); any adopter write; any upstream action; CI (none).
changelog_ref: CHANGELOG.md "2026-09-17 · [BL-67] S185 close-out", plus the claim, the P7 recording and the BL-67 closure entries
commit: 4cb67c6 (claim) + 313459c (P7 recorded) + aee4771 (BL-67 closed) + this close-out
```

**Self-assessment: 8/10.** Plus: I treated the reverted recording as a list of claims to re-check rather than a patch
to re-apply, and re-ran every one from `wsfct`'s git objects with its tree clean before and after — including the
plan's own §9.8 script, run verbatim with only the revision pair substituted, on both ranges, so the row's 13–196 is
shown to fail rather than asserted to. The one claim that did not hold was found by asking the remote instead of
re-reading the same local ref, and then pinned with the PR's event timeline, which turned *"stale"* into *"never
true"*. The audit is stated in both of its forms, and the procedure's stale figure is struck beside the measured one.
S630's report of failing shard proofs was re-run at two commits and matched to BL-36 after searching the backlog,
instead of being raised as a new item. **Minus:** I first called the branch citation *stale* — to the operator
mid-session and in `313459c`'s item (20) (*"by S185 GitHub had deleted it"*) — before looking at when the deletion
happened. That is a derived claim about time published as a measured one, in the exact shape Learning #77 now
names; the close-out commit corrects the plan, and the `313459c` ledger entry stands as written. I also found
`BACKLOG.md`'s open list missing BL-63 while editing that very line and left it, correctly for scope, but it is
one more hand-maintained list known to be wrong. **Growth:** four ledger entries plus this one, the P7 block
(~40 lines), a detail note, a learnings row (+1,158 B). **Reduction:** none this session, stated rather than left
unsaid; the trim this close-out makes owed falls to the next Phase 0.

**Predecessor (S183): 8/10.** Its item (1) named exactly this task, with the plan's P6 block (`:175`) and P7 row
(`:799`) and the BL-57 row (`BACKLOG.md:151`) — all three resolved at my Phase 0 tree — and it said the DONE checks
*"still want running from here"*, which is the instruction that caught the one false claim. Its gotchas (3), (6) and
(7) were right: no trim owed, the two tracked Phase 0 rows, suites one at a time. Its gotcha (2) predicted the
`tests-sh-passed` jump to 315 at three receipts exactly. Its six commit hashes and the 15-file count for `8a41741c`
all held. **Not 9:** it described `wsfct` as *"not merged"*, which was already false a few hours later. It did
say that state was a reading from its own Phase 0, and fork Learning #74 anticipates this, so it was not careless.
But its `key_files` for the item were all on this side, with no `wsfct` ref named to re-check.
BL-67's body, written after S183's close-out, added the verification commands with their expected readings and the
instruction to re-verify rather than trust; every reading held except the one inherited from `a6320ae`.
**ROI: strongly positive** — no time spent rediscovering the task's shape.

