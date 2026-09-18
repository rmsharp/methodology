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
session: S192
date: 2026-09-18
status: pending
self_score: pending
predecessor_score: pending
active_task: **BL-72 — FIX `bin/check-handoff`'s FENCE SCANNER, ON `bl57/changelog-rules` SO IT RIDES PR #84, THEN MERGE INTO FORK `main`.** `scan()` reads a fenced block with an info string other than `handoff` (the seed's `sh` block) as prose, takes its closing fence for a wrapper opener, and skips the newest receipt while reporting OK. The fix skips such a block to its closer, per CommonMark, as a wrapper already is; failing tests first, on the fixtures in `docs/planning/BACKLOG-DETAIL.md` §BL-72, then re-read `airqino`, `nprcgenekeepr` and `vscode_quarto_ext` `HANDOFFS.md`. Chosen by the operator after Phase 0 (picker), with the route (ride PR #84, over its own PR or fork `main` only) and two close-out go-aheads: push fork `main` to `origin`, and push the fix to PR #84's branch, each after the gate passes and read back. The owed `HANDOFFS.md` trim and its fold follow this claim.
what_was_done: pending
next_steps: pending
key_files: `bin/check-handoff:227` (`scan()` on fork `main`), `:253`–`:292` (its loop; `:104` on `bl57/changelog-rules` and `upstream/main`, byte-identical); `docs/planning/BACKLOG-DETAIL.md:2464` (§BL-72); `starter-kit/HANDOFFS.md:101` (the seed's `sh` fence); `bin/tests.sh:2296` (Test 38 on fork `main`, which calls `scan()`)
gotchas: pending
runtime_smoke: pending
changelog_ref: CHANGELOG.md "2026-09-18 · [BL-72] S192 claim"
commit: pending
```

```handoff
session: S191
date: 2026-09-18
status: complete
self_score: 7
predecessor_score: 9
active_task: **BL-57 P8 (`vscode_quarto_ext`) IS DONE IN THAT REPOSITORY AND RECORDED HERE (`10f931a`), ITS DONE RE-RUN READ-ONLY FROM HERE. NEXT IS BL-72, A `bin/check-handoff` FIX, BEFORE P9 (OPERATOR).** P8 ran in `vscode_quarto_ext`'s own Session 264 (`48d1790c`..`57750bb2` on its `master`, not pushed) while this session waited: after Phase 0 the operator chose to run it there (picker), then relayed its report and chose, in a second picker, to record it in full here, over a lighter recording. Three operator decisions are in the plan's P8 block: `vscode_quarto_ext` keeps `HANDOFFS.md` budgeted (D7, for that project only); BL-72 is fixed before P9; P9–P11 keep the plan rather than a generic `bin/status` → `bin/sync` route. PR #84 unchanged at close-out: OPEN, head `20db3f0`, no reviews or comments. Fork `main` is 4 commits ahead of `origin` after this close-out (this session's), not pushed: no go-ahead was asked.
what_was_done: **Phase 0:** `CHANGELOG.md` frontier `0ab3881` = HEAD; `HANDOFFS.md` frontier `61b2fc2`, two post-close-out records behind, no receipt owed; nothing backfilled. Gate in a `--no-local` clone of `0ab3881`: `results 91c29bff06ce`, S190's citation. **Two operator questions answered by measurement, read-only:** what S180/S185's recordings fed forward (items (16)–(22) of the plan, split into distributed fixes, next-phase instructions and re-verification); and whether all local projects could sync without the plan: `bin/sync --dry-run` against the eleven projects with a `SESSION_RUNNER.md`, from a simulated `upstream/main` + PR #84 (`--no-ff`, the maintainer's style) and from fork `main`, each refusal classified by blob history (script `scratchpad/classify.py`, not kept). **`793fa84`** claim (Phase 0's two rows, regenerated after I discarded the first pair when the operator took P8 elsewhere). **`10f931a`** the recording: plan status line, P8 block with items (25)–(27) and decisions (a)–(c), P8 row DONE, D7 row annotated; BL-57 row; BL-72 row + `BACKLOG-DETAIL.md` §BL-72; two ledger entries. **`0b7e672`** fix: the close-out gate on `10f931a` read `9/10 · tests-sh-failed 3` (Tests 30, 31, 40) because three lines I wrote began with inline backticks quoting a fence, which `bin/model-report` reads as a fence toggle; reworded, gate 10/10. P8's DONE re-run in a `--no-local` clone at `57750bb2` with `bin/status`/`bin/sync` from a clone of `0ab3881`: both ledgers `present`, sync exit 0 / 23 unchanged, §9.8 on `acb43e0b` (1–8; control 1–7 fails) and `69f0dd43` (pure 61-line insertion), `### ` 25 → 26 and audit 20 → 21 (250 → 251 with shards), trimmer `L1_OK`–`L3_OK` on both. BL-72 reproduced on two fixtures and on the real files: `scan()` skips `vscode_quarto_ext`'s S264, `airqino`'s S19 and `nprcgenekeepr`'s S714; the trimmer counts all 17 records.
next_steps: **(1) BL-72, ITS OWN SESSION, BEFORE P9 (operator, S191).** `bin/check-handoff:227` `scan()`, the loop `:253`–`:292`: a fence with an info string other than `handoff` must skip to its bare closer, as a wrapper does (CommonMark, which the docstring already cites). RED first on the fixtures in `docs/planning/BACKLOG-DETAIL.md:2464` §BL-72 (two receipts with and without the seed's section at `starter-kit/HANDOFFS.md:89`–`:148`), plus an `sh` block in a receipt's prose tail and one inside a four-backtick wrapper; then re-run against `../airqino`, `../nprcgenekeepr`, `../vscode_quarto_ext` `HANDOFFS.md` (expect the newest receipt read: S19, S714, S264 or later). Test 38 calls this `scan()`. **Decide with the operator first:** does the fix ride PR #84 (commit on `bl57/changelog-rules`, merged into fork `main` as items (22)–(24) were; pushing to the PR is its own go-ahead) or go up on its own later? **(2) P9, `mts-system`, FROM THAT PROJECT, after (1).** Plan row `docs/planning/changelog-rules-contradictions-plan.md:1010`; items (25)–(26) (`:369`, `:378`) now apply: read the dry run's new root files against any build ignores, and grep its backlog for items the phase finishes. Its row's own warning stands: `mts-system`'s `HANDOFFS.md` has a fence opened at :216 never closed before :219, found before P9, not P9's. **(3) RELAY TO `vscode_quarto_ext` (ITS OWN SESSION):** D7 answered: keep `HANDOFFS.md` budgeted; its 146,916 B file is the project's own trim to make (`methodology_trim.py --file HANDOFFS.md --cut N --force`); its 11 commits are unpushed, its own go-ahead. **(4) WATCH PR #84:** `gh pr view 84 -R KJ5HST/methodology --json state,reviews,comments`. **(5) A `HANDOFFS.md` TRIM IS OWED AT THE NEXT PHASE 0:** this close-out leaves 3 receipts (S191, S190, S189); after the next claim, `--cut 2 --force --write`, then the pointer fold in its own commit, as S190's `69ad9c9` + `1f5dcae`. **(6) PUSH FORK `main` TO `origin`** when the operator says so (3 commits now, more with the gate record). **CARRIED:** BL-54's own PR, BL-53 before ANY learnings row (`docs/FORK_LEARNINGS.md` 81,721 of 81,920 B), `CHANGELOG.md` past its trigger under the standing no-trim decision (207,592 B; raise at 262,144 B), BL-43, BL-68, BL-61, BL-60, BL-65, BL-66, `airqino`'s `HANDOFFS.md` migration in its own repository (still stale), the optional `tests-sh-passed` floor (305 vs 321).
key_files: `docs/planning/changelog-rules-contradictions-plan.md:12` (status line), `:354` (the P8 block), `:369` (item (25)), `:378` (item (26)), `:384` (item (27)), `:392` (S191's decisions), `:1009` (the P8 row), `:1010` (the P9 row), `:1011` (the P10 row), `:1093` (the D7 row), `:1225` (§9.8); `docs/planning/BACKLOG.md:151` (BL-57), `:164` (BL-72); `docs/planning/BACKLOG-DETAIL.md:2464` (§BL-72); `bin/check-handoff:227` (`scan()`), `:253`–`:292` (its loop); `starter-kit/HANDOFFS.md:89` (the seed section), `:101` (its `sh` fence); in `~/Development/vscode_quarto_ext`: `48d1790c`..`57750bb2`, `e8c395b3` (the package allowlist), `.vscodeignore`; `~/Development/nprcgenekeepr/.Rbuildignore` (item (25), P10)
gotchas: **(1) UNTIL BL-72 IS FIXED, `bin/check-handoff` ON AN ADOPTER'S `HANDOFFS.md` READS OK WITH ITS NEWEST RECEIPT UNREAD** wherever the file carries the seed's size section (`airqino`, `nprcgenekeepr`, `vscode_quarto_ext` today). Check its first block's line (`scan()`) or count with the trimmer's dry run instead. **(2) AFTER PR #84 MERGES, DO NOT SYNC THESE PROJECTS FROM `upstream/main`:** measured on a simulated merge, 9 of 11 are refused, 6 only for fork-only versions; keep `--source=local` from fork `main`, or `--force` each once after a diff. **(3) A SYNC ADDS ROOT FILES** (`quality_ratchet.py`, `.quality-gates.json`, then `.quality-gates-results.json` at the first `--run`): a deny-by-default package list or an R `.Rbuildignore` must learn them one commit before the sync, as `vscode_quarto_ext`'s `e8c395b3` did. **(4) ADOPTERS MOVE DURING A SESSION:** `vscode_quarto_ext` went `58f7bcbd` → `fa3696ed` → `57750bb2` today; I re-verified from a `--no-local` clone at the reported sha, not the live tree. **(5) NEVER START A LINE WITH A BACKTICK RUN IN A LEDGER, PLAN OR BACKLOG FILE,** not even inline code quoting a fence: `bin/model-report` (`:287`) toggles its fence state on any stripped line that starts with three backticks, and my reflowed line turned three tests red (`0b7e672`). Grep the added lines for a leading backtick run before committing. **(6) zsh TRAPS RECURRED TWICE:** `echo =====` aborted a command, and `$r:starter-kit/...` became a history modifier; quote the one and brace the other (`${r}:`). **(7) PHASE 0 WRITES TWO TRACKED ROWS;** if the operator sends the task elsewhere, leave them uncommitted rather than discarding them: I discarded mine and had to regenerate them for the claim.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `quality_ratchet.py --run` IN A `--no-local` CLONE WITH HEAD ASSERTED.** **Citation, fork `main`, clone of `0b7e672`: `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results 511119b3196e · manifest 58d766958ae1`**, `tests-sh-passed` 327 at 3 receipts (Test 34's six assertions run, none skipped). On `10f931a` the same gate read `9/10 pass · 1 fail · results 434011731a45` (`tests-sh-failed` 3), fixed at `0b7e672`. Phase 0's gate on `0ab3881`: `results 91c29bff06ce`. This close-out commit is docs-only and not covered (BL-64). **NOT EXERCISED:** P8's build item (`npm test`, the package check), which rests on `vscode_quarto_ext`'s S264 receipt; BL-72's fix (not built); CI (none).
changelog_ref: CHANGELOG.md "2026-09-18 · [BL-57] S191 close-out", plus the claim, the P8 recording and the BL-72 raised entries
commit: 793fa84 (claim) + 10f931a (recording) + 0b7e672 (fix) + this close-out
```

**Self-assessment: 7/10.** Plus: both of the operator's questions were answered by measurement, not assertion. Eleven
projects were dry-run from two sources, and every refusal was classified by blob history. Upstream-after-merge was
simulated the way the maintainer actually merges. The adopter was re-verified from a clone at the reported sha, while it
kept moving. Each §9.8 check had a control that fails. The P10 build-ignore gap was computed, not guessed, and labelled
with its method. BL-72 was reproduced on fixtures and on real files before it was filed, and its blast radius was measured
both ways (three adopters hit, the trimmer not). **Minus:** (1) two zsh traps my memory names recurred (`echo =====`,
`$r:path`). (2) I discarded Phase 0's two rows when the operator sent P8 elsewhere, then regenerated them for the claim.
(3) A first draft of the decision text said *seven* fork-only refusals where the count was six; I caught it before it was
written. (4) The build item for P8 rests on S264's receipt; I did not re-run `npm test` or the package check here. (5) **I committed the defect class I was filing:** three lines of `10f931a` began with inline code quoting a fence, and `bin/model-report` read the rest of `CHANGELOG.md` as a code block. The close-out gate caught it before the receipt (fixed at `0b7e672`), but the check I ran before committing (`bin/check-links`) could not see it, and I did not grep my own added lines for a leading backtick run.
**Growth:** five ledger entries, a 57-line plan block, one backlog row and a detail section.
**Reduction:** none, stated here rather than left unsaid.

**Learnings withheld from `docs/FORK_LEARNINGS.md`:** it is 81,721 of 81,920 B and BL-53 is unanswered. Candidates:
(a) a parser that recognises only its own fence's info string misreads every other fenced block. That is BL-72's fix,
and a test is the better home. (b) A tool update that adds root files breaks any deny-by-default packaging list, so read
a sync's new root files against the project's build ignores at the claim (now plan item (25)). (c) An "is the recording
worth it" question is answerable: split what a recording fed forward into distributed fixes, next-phase instructions and
pure re-verification. (d) Prose that quotes a fence must never start a line: a line-based fence toggle reads it as a fence (gotcha (5)); a grep of the added lines is the cheap gate.

**Predecessor (S190): 9/10.** Every citation in its next step (1) held: plan row `:956`, step 3's bullet `:919`, item (18)
`:197`, and `vscode_quarto_ext` still at `58f7bcbd` at my Phase 0. Gotcha (2), that the plan's `BOOTSTRAP.md:386`
citation had drifted to the `CHANGELOG.md` half, went straight into the launch prompt, and P8's commit cites `:387`–`:388`.
Item (6) stopped me offering a `CHANGELOG.md` trim, and gotcha (6) (Phase 0's two rows) was right. **Not 10:** it said P8
runs from that project but not what that leaves this repository's session to do, so the first picker had to work that
out: P8 elsewhere with no claim here, and a recording session to follow. **ROI: strongly positive.**

```handoff
session: S190
date: 2026-09-18
status: complete
self_score: 8
predecessor_score: 9
active_task: **BL-57 PLAN ITEM (24) (a) IS DONE: `bl57/changelog-rules` (`20db3f0`, PR #84's head) IS MERGED INTO FORK `main` AS `2410657`, RECORDED AT `b7585e6`. P8 (`vscode_quarto_ext`) IS NEXT, FROM THAT PROJECT.** Fork `main`'s `bin/status` now keys `HANDOFFS.md` on `handoffs-format: 2`, and its `CHANGELOG.md` route keeps the trimmer's lines, so P8 syncs the rules PR #84 proposes. Chosen by the operator after Phase 0 (picker), over BL-54's PR, BL-53 and P8. The same picker approved pushing fork `main` to `origin` after close-out. It also approved a `CHANGELOG.md` trim at its trigger, but my option had not cited the operator's standing 2026-09-14 decision not to trim there; asked again, **the operator kept that decision.** No `CHANGELOG.md` trim. PR #84 unchanged at close-out: OPEN, head `20db3f0`, no reviews or comments.
what_was_done: **Phase 0:** `CHANGELOG.md` frontier `bce805c` = HEAD; `HANDOFFS.md` frontier `5217d1d`, four post-close-out records behind, no receipt owed; nothing backfilled. Gate in a `--no-local` clone of `bce805c`: `results 949e9e0b4269`, identical to S189's citation. **`c868134`** claim (Phase 0's two tracked rows). **`69ad9c9`** trim, `methodology_trim.py --file HANDOFFS.md --cut 2 --force --write`: S188 and S187 to `docs/archive/HANDOFFS-through-2026-09-17-5.md`, 40,364 → 17,977 B; `.verify.sh`, `check-handoff --all --allow-pending` and `--archived --file <shard>` exit 0. **`1f5dcae`** fold into `docs/HANDOFFS_ARCHIVE_INDEX.md`, → 17,521 B. **`2410657`** merge: conflicts exactly the two `git merge-tree` predicted, resolved ours; the fork's config budgets neither of `adaa4a3`'s re-measured blobs by density, so no hand fix; the other eight files' 66 changed lines equal the branch patch `f572068..20db3f0` (four blob-identical). `bin/status` on six adopters from a `--no-local` clone of `1f5dcae` and from `2410657`, adopters held still: 15 rows move, all the merge's; `airqino` and `nprcgenekeepr` `HANDOFFS.md` now `present (stale format)` (7 → 9). **`b7585e6`** record: plan item (24) (a) DONE block, status line, BL-57 row, ledger entry.
next_steps: **(1) P8, `vscode_quarto_ext`, ITS OWN SESSION, RUN FROM THAT PROJECT.** Plan row `docs/planning/changelog-rules-contradictions-plan.md:956`, step 3's `HANDOFFS.md` bullet `:919`, item (18) (one `bin/sync` run is one commit) `:197`. Read at this close-out, from `2410657`, read-only: HEAD still `58f7bcbd` (the commit S186 read the plan row's line numbers on), working tree only an untracked `scratchpad/`; `CHANGELOG.md` and `HANDOFFS.md` both `present (stale format)`, `quality_ratchet.py` and `docs/methodology/FRAMEWORK_APPARATUS.md` *missing*, `BOOTSTRAP.md` 9 versions behind, `methodology_trim.py` 6. Re-derive at its claim anyway. **(2) WATCH PR #84:** `gh pr view 84 -R KJ5HST/methodology --json state,reviews,comments`; every reply is its own go-ahead; a review change lands on the branch, then merges into fork `main` as `2410657` did. **(3) BL-54's own upstream PR** (`2c4f801` + `865119f`), its own go-ahead. **(4) ANSWER BL-53 BEFORE ANY LEARNINGS ROW:** `docs/FORK_LEARNINGS.md` is 81,721 of 81,920 B; S189's and this session's candidates are withheld below their receipts. **(5) NO `HANDOFFS.md` TRIM OWED at the next Phase 0:** 2 receipts (S190, S189). **(6) `CHANGELOG.md` IS PAST ITS 196,608 B TRIGGER** (about 202 KB after this close-out; `--check` fires); the operator kept the no-trim decision this session, so report it and raise a trim only at 262,144 B. **(7) OPTIONAL, ITS OWN ACTION:** `tests-sh-passed` floor is 305 against 321 measured at 2 receipts; tightening needs no approval. **CARRIED:** BL-43 (Test 38 (5) recurred here), BL-68, BL-61, BL-60, BL-65, BL-66, `README.md`'s stale cost section, `docs/planning/BACKLOG.md:9`–`11` still omits BL-63, `airqino`'s `HANDOFFS.md` migration in its own repository (now confirmed stale by `bin/status`).
key_files: `docs/planning/changelog-rules-contradictions-plan.md:12` (status), `:326` (item (24)), `:335` (what it means for P8–P11), `:341` (S190's DONE block), `:919` (step 3's `HANDOFFS.md` bullet), `:956` (the P8 row); `docs/planning/BACKLOG.md:151` (BL-57); `docs/planning/BACKLOG-DETAIL.md:1055` (BL-43), `:1059` (Test 38 (5)); on fork `main` since `2410657`: `bin/_manifest.py:119` (`handoffs-format: 2`), `bin/status:157` (`MIGRATION_ROUTES`), `bin/tests.sh:341` (Test 20 (g)), `:364` (the old-section fixture), `starter-kit/HANDOFFS.md:91` (the marker line), `starter-kit/BOOTSTRAP.md:386`–`388` (the update paragraph's two routes); `docs/HANDOFFS_ARCHIVE_INDEX.md:57` (the new shard row)
gotchas: **(1) ADOPTERS MOVE UNDER A BEFORE/AFTER READING:** `airqino` and `nprcgenekeepr` both committed between my two `bin/status` readings. `bin/status` takes its source from its own repository (`bin/status:35`), so a `--no-local` clone at the pre-change commit gives a *before* reading at any moment; run both readings back to back with each adopter's HEAD and porcelain digest recorded on either side. **(2) THE PLAN'S `BOOTSTRAP.md:386` CITATION (`:921`) NOW LANDS ON THE `CHANGELOG.md` HALF OF THE PARAGRAPH;** the `HANDOFFS.md` route is `:388`. **(3) A SECOND `bash bin/tests.sh` IN A CLONE THE RATCHET JUST RAN CAN FLAKE ON TEST 38 (5)** (BL-43's `echo | grep -q` race): cite the ratchet's run and name the flake rather than re-running until green. **(4) `bin/check-handoff --archived` TAKES `--file <shard>`,** not a positional path (exit 2). **(5) BEFORE OFFERING A GO-AHEAD ON AN ARTIFACT, GREP THE BACKLOG AND THE PLAN'S K-CONSTRAINTS FOR A STANDING DECISION ON IT** (`BACKLOG-DETAIL.md:1794`, plan K5 `:434`): I didn't, and the operator had to answer twice. **(6) PHASE 0 WRITES TWO TRACKED ROWS;** they rode `c868134`.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `quality_ratchet.py --run` IN A `--no-local` CLONE WITH HEAD ASSERTED.** **Citation, fork `main`, clone of `2410657` (the merge): `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results 91c29bff06ce · manifest 58d766958ae1`**, 343 s, `tests-sh-passed` 321 at 2 receipts (6 stated Test 34 skips), Test 20's 28 rows pass including the marker and old-section fixture. A second `bash bin/tests.sh` in that clone read 320 / 1, Test 38 (5), BL-43's known race. The runtime behaviour changed (`bin/status`'s marker and routes) was exercised directly on six real adopters, before and after. `b7585e6` and this close-out are docs-only and not covered by that run (BL-64): re-measured in a clone of the close-out after it lands and recorded as its own entry. **NOT EXERCISED:** an adopter following the new routes (P8's to run); the maintainer's review; CI (none).
changelog_ref: CHANGELOG.md "2026-09-18 · [BL-57] S190 close-out", plus the claim, trim, fold and merge-record entries
commit: c868134 (claim) + 69ad9c9 (trim) + 1f5dcae (fold) + 2410657 (merge) + b7585e6 (record) + this close-out
```

**Self-assessment: 8/10.** Plus: the conflicts were computed before the merge, and they held exactly. Every merged file
was checked against the branch patch rather than trusting a clean auto-merge. When the adopters moved under my first
`bin/status` pair, I found why, held them still with a clone of the pre-merge commit, and confirmed the diff row for
row before citing it. The one red suite row was traced to BL-43 before it went into any record, not re-run until green.
The owed trim and fold each ran their proof. **Minus:** (1) I offered the `CHANGELOG.md` trim as a go-ahead without
grepping for a standing decision on that file. My own memory names that exact check, and the operator had to answer a
second picker. I caught it before acting, but only because the BL-57 row surfaced in an unrelated grep. (2) A
redundant second suite run cost about three minutes, though it surfaced the flake. (3) `check-handoff --archived`
took a positional path on the first try. **Growth:** five ledger entries, one plan block (9 lines), one index row.
**Reduction:** the `HANDOFFS.md` trim (40,364 → 17,521 B).

**Learnings withheld from `docs/FORK_LEARNINGS.md`, again:** it is 81,721 of 81,920 B and BL-53 is unanswered. Candidates:
(a) a before/after reading of a tool whose source is its own repository can be taken from a clone at the old commit, at
the same moment as the new one, so the subjects under measurement cannot move between readings (gotcha (1)); (b) a
go-ahead option on an artifact must cite every standing decision on that artifact, or the answer it gets is to a
different question (gotcha (5); a recurrence of S177's lesson, so a gate, not a row, is the better home).

**Predecessor (S189): 9/10.** Next step (1) was exact and every part held: the `git merge-tree` instruction, the
`5f5a400` convention, the hedge on `adaa4a3`'s notes (they did not matter here, which it left open rather than
guessed), and the prediction that `airqino` and `nprcgenekeepr` flip to stale. Step (5)'s trim command held to the
flag. Gotcha (3), the parallel adopter session, recurred in two adopters, and the warning is why I checked heads
beside the readings. **Not 10:** it did not say that `CHANGELOG.md` sat 1,237 B under its trigger with a standing
no-trim decision on it, which the next claim was certain to cross. **ROI: strongly positive:** the merge needed no
discovery at all.

```handoff
session: S189
date: 2026-09-17
status: complete
self_score: 7
predecessor_score: 8
active_task: **BL-57 P12 IS DONE: UPSTREAM [PR #84](https://github.com/KJ5HST/methodology/pull/84) IS OPEN AND MERGEABLE, HEAD `20db3f0`, OPENED ON THE OPERATOR'S GO-AHEAD AND READ BACK.** The branch merged `upstream/main` (`f572068`), re-measured its three read-set densities (`adaa4a3`), dropped two fork-plan citations from code comments (`036d840`), then took five fixes from an independent review of the frozen PR, each chosen by the operator in one picker: a versioned `HANDOFFS.md` marker, `handoffs-format: 2` (`f4e974c`, revising plan decision D9), a `CHANGELOG.md` route that keeps the trimmer's lines (`7813652`), and three wording commits (`f7d3b8c`, `91f7646`, `20db3f0`). The body is `docs/planning/changelog-rules-pr-body.md` (`f452f30`). **NOT DONE, AND NOW OWED: fork `main` lacks the branch's last eight commits (`f572068`..`20db3f0`), so its `bin/status` still keys `HANDOFFS.md` on the heading and its `CHANGELOG.md` route still deletes the trimmer's lines; merge the branch into fork `main` before P8 syncs from it (plan item (24)).** Also this session: BL-68 raised on the operator's request (the dashboard's large-file risk on its own file), and, by operator decision, the history-walk fix (BL-54) goes upstream as its own PR.
what_was_done: **Phase 0:** `CHANGELOG.md` frontier `c5af062` = HEAD; `HANDOFFS.md` frontier `6e94f3b`, two `CHANGELOG.md`-only records behind; nothing backfilled. S188's receipt `commit:` slot reconciled to lead with `6e94f3b` (its leading `0743825` is all digits, which `bin/check-handoff` does not read as a sha). Gate in a `--no-local` clone of `c5af062`: `results 582ea833e011`, identical. **`7df4328`** claim. **Branch (worktree `../methodology-bl57`), each commit with its own branch entry:** `f572068` merge (clean, upstream's entry on top); `adaa4a3` densities (`CLAUDE.md` 23,476.5 tokens, runner 18,858.5, `SAFEGUARDS.md` 6,083.7 of 6,100; two opus meter subagents, each run reproducing 37,731 / 46,965 / 42,208 as controls); `036d840` comments; `f4e974c` marker (test-first: the old-section fixture read `present`, now stale); `7813652` route (two new assertions, absent at `f4e974c`); `f7d3b8c`, `91f7646`, `20db3f0` wording. **Dry runs** from `upstream/main`, the branch and fork `main` into scratch copies of six adopters (`.gitignore` + distributed paths): the PR adds no refusal, removes three in `airqino` and `wsfct`; refusals are fork-only versions or three genuine local edits; unchanged on the final tip; from the tip `HANDOFFS.md` reads stale in all five adopters that have one. **Review:** one opus subagent, read-only, on the frozen `036d840` + `72450d8`; its findings 1, 2 and 4–7 were re-verified here before acting. **Fork `main`:** `72450d8` (draft frozen), `d246aff` (BL-68), `f452f30` (body rewritten), `cb1f7d2` (branch push recorded), `c64cbd8` (PR open recorded; plan item (24); BL-57 row). **Outward:** branch pushed `83a12f0..20db3f0` (read back `20db3f09`); PR #84 opened (read back: OPEN, MERGEABLE, body equal to the file).
next_steps: **(1) MERGE `bl57/changelog-rules` (`20db3f0`) INTO FORK `main`, ITS OWN SESSION, BEFORE P8.** Plan item (24) `docs/planning/changelog-rules-contradictions-plan.md:326`. The convention is `5f5a400`'s: `git merge` in the main worktree, `CHANGELOG.md` and `.context-budget.json` resolved ours (this repo's config is its own; then fix this repo's own notes by hand if the branch's `adaa4a3` notes matter here, as `d9d1424` did). Predict conflicts with `git merge-tree --write-tree --name-only main bl57/changelog-rules` rather than trusting this list. After it: Test 20 (g) on fork `main` must pass with the new marker; `bin/status` on the six adopters, read-only, before and after (expect `airqino` and `nprcgenekeepr` `HANDOFFS.md` to flip to stale). **(2) WATCH PR #84:** `gh pr view 84 -R KJ5HST/methodology --json state,reviews,comments`. Any reply, push or comment is its own go-ahead; review changes land on the branch and are merged into fork `main` the same way. **(3) P8 (`vscode_quarto_ext`), after (1), from that project.** Step 3's `HANDOFFS.md` bullet now keys on the marker line (`:911`). **(4) THE HISTORY-WALK FIX'S OWN UPSTREAM PR** (BL-54, `2c4f801` + `865119f`), decided at S189; its PR is its own go-ahead. **(5) A `HANDOFFS.md` TRIM IS OWED AT THE NEXT PHASE 0:** this close-out leaves 3 receipts (S189, S188, S187); `--cut 2 --force` after the claim, then the pointer fold in its own commit, as S188's `83099b5` + `77fe511`. **(6) `docs/FORK_LEARNINGS.md` IS STILL 81,721 OF 81,920 B:** this session withheld its learnings row (the text is below this receipt); answer BL-53 before the next row, don't raise the ceiling by reflex. **CARRIED:** BL-68 (new), BL-61, BL-60, BL-65, BL-66, `README.md`'s stale cost section, `docs/planning/BACKLOG.md:9`–`11` still omits BL-63, `airqino`'s `HANDOFFS.md` now owes a migration in its own repository.
key_files: `docs/planning/changelog-rules-contradictions-plan.md:12` (status), `:319` (P12 done), `:326` (item (24)), `:911` (step 3's `HANDOFFS.md` bullet), `:951` (§P12); `docs/planning/changelog-rules-pr-body.md:12` (the body, below its rule); on the branch `20db3f0`: `bin/_manifest.py:111` (`handoffs-format: 2`), `bin/status:114` (`MIGRATION_ROUTES`), `bin/tests.sh:323` (Test 20 (g)), `:341` (the old-section fixture), `starter-kit/HANDOFFS.md:91` (the marker line), `starter-kit/BOOTSTRAP.md:87` (the update paragraph), `FRAMEWORK_APPARATUS.md:453` (*Placement*), `.context-budget.json:58` (the `SAFEGUARDS.md` density); `docs/planning/BACKLOG.md:151` (BL-57), `:160` (BL-68); `docs/planning/BACKLOG-DETAIL.md:2360` (§BL-68)
gotchas: **(1) `git log --all` IN THE BRANCH WORKTREE OR A `--no-local` CLONE WALKS FORK `main`'S REFS TOO.** My first dry-run classifier read every refusal as *in the source's history* because of it; classify against `git log --full-history HEAD` only. **(2) zsh TRAPS RECURRED THREE TIMES:** `$B:path` and `$r:path` (brace them: `${B}:path`), and `echo ======` aborting a whole command. **(3) A PARALLEL SESSION WAS COMMITTING IN `nprcgenekeepr` (its S707)** while I dry-ran it; its porcelain digest changed between my before and after readings through no action of mine. Read an adopter's `git log -3` beside any before/after comparison. **(4) THE ADOPTER COPIES ARE SCRATCH COPIES** (`.gitignore` + distributed paths), faithful for `bin/sync` and `bin/status` in commit mode only. **(5) `SAFEGUARDS.md` IS 16.3 TOKENS UNDER ITS 6,100 CEILING ON THE BRANCH** (measured), not the ≈33 estimated at the old density; any review change to it must pay for itself or re-split the partition. **(6) THE PR BODY'S ADOPTER NAMES ARE LETTERS A–F**, in `p12_dryrun.py`'s order (airqino, model_project_constructor, mts-system, nprcgenekeepr, vscode_quarto_ext, wsfct). **(7) PHASE 0 WRITES TWO TRACKED ROWS;** they rode `7df4328`.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `quality_ratchet.py --run` IN A `--no-local` CLONE WITH HEAD ASSERTED.** **Citation, fork `main`, clone of `c64cbd8`: `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results 949e9e0b4269 · manifest 58d766958ae1`**, `tests-sh-passed` 323 at 3 receipts; `context_budget.py --status` shows the runner, `SAFEGUARDS.md` and the read-set total `over` (unchanged since Phase 0). Branch, clone of `20db3f0`: `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results f6b5a63009e8 · manifest 97a7aab85b9a`, `tests-sh-passed` 153, `bin/check-links` 111, budget *nothing over*, `check-handoff --all` 21 receipts; also 10/10 on `f572068`, `adaa4a3`, `036d840` and `f4e974c`. The runtime behaviour changed (`bin/status`'s marker and routes) was exercised directly: RED/GREEN on scratch fixtures, then on six adopter copies. This close-out commit is re-measured in a clone of itself after it lands (BL-64) and recorded as its own entry. **NOT EXERCISED:** an adopter following the new routes (P8's to run); the maintainer's review; CI (none).
changelog_ref: CHANGELOG.md "2026-09-18 · [BL-57] S189 close-out", plus the claim, the P12 steps, BL-68, the review, the push and PR-open entries; the branch's seven entries ride `adaa4a3`..`20db3f0`
commit: 7df4328 (claim) + 72450d8 (draft) + d246aff (BL-68) + f452f30 (body) + cb1f7d2 (push record) + c64cbd8 (PR recorded) + f572068, adaa4a3, 036d840, f4e974c, 7813652, f7d3b8c, 91f7646, 20db3f0 (branch) + this close-out
```

**Self-assessment: 7/10.** Plus: every outward step was guarded and read back (the push's fast-forward, the remote
head before the PR, the PR's state and body after). The frozen draft went to an independent reviewer before the PR
opened, and its five diff defects were re-verified, then fixed test-first where behaviour changed. The largest was a
stale-seed marker that failed its own stated property in two real adopters, and it went to the operator as a decision,
since it revised an approved one. Instruments were audited: the meters ran beside controls that reproduced exactly, and
the dry-run classifier was caught reading the fork's refs and corrected before its numbers were used. The PR adds no
refusal to any adopter. **Minus:** (1) my frozen draft carried five claims the reviewer showed wrong or overstated: a
count taken before my own last commit, the title marker's reach, a *silent* example that exists only in the fork's
history, a private "sixteenth" line, and the F5 framing. I had checked numbers against the plan and the trees, not
claims against upstream's own history. (2) I read `bin/_manifest.py`'s marker comment and did not test the heading
against upstream's seed history; the plan had approved it, and I trusted that. (3) zsh traps my memory names recurred
three times. (4) The first dry-run classifier used `git log --all`. **Growth:** eight fork ledger entries at close-out (two more follow it: the gate re-run and the push), seven on the
branch, one plan item (~25 lines), BL-68 (row + detail), a 17 KB PR body. **Reduction:** none, which I state here
rather than leave unsaid; the `HANDOFFS.md` trim this close-out makes owed falls to the next Phase 0.

**Learnings withheld from `docs/FORK_LEARNINGS.md`, deliberately:** the file is 81,721 of its 81,920 B ceiling, and S188
asked that the next row answer BL-53 first rather than raise the ceiling. The candidates, for that session: (a) a format
marker's *absent from every earlier format* property must be checked on every lineage that ships the seed, not only the
one the plan was written on. That one is now a gate, not a row: Test 20 (g)'s old-section fixture. (b) In a worktree or a
`--no-local` clone of a fork, `git log --all` walks the fork's refs, so a *source history* check must walk `HEAD` only.
(c) After 10/10 gates and my own claim checks, a reviewer of the frozen PR still found ten should-fix issues, because it
checked the claims against upstream's history while I had checked them against the plan's.

**Predecessor (S188): 8/10.** Its next steps held where I could test them. `git merge-tree` listed no conflicts and the
merge was clean. 20 ahead / 3 behind was right. Its floor estimate (149 ≥ 139, labelled an estimate) held. Its item (10)
pointer led directly to the `SAFEGUARDS.md` measurement. Its body requirements (the droppable `0d63410`, the +105 B
amendment) went into the body. *No trim owed* held. Gotcha (4) was the right warning, at an estimate (≈33 tokens)
the meter halved (16.3). **Not 9:** its own receipt's `commit:` slot led with an all-digit sha, so my claim's
`check-handoff` failed until I reconciled it. And it carried forward S187's two fork-plan citations in branch code
comments without noticing they would ship upstream. That one was mine to catch too. **ROI: strongly positive:** step 2,
item (10) and the body's requirements all came straight from it.

