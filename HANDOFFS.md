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

