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

**Archived 2 record(s), 2026-09-17 → 2026-09-17** into [`docs/archive/HANDOFFS-through-2026-09-17-4.md`](docs/archive/HANDOFFS-through-2026-09-17-4.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/HANDOFFS-through-2026-09-17-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-17-4.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

```handoff
session: S188
date: 2026-09-17
status: pending
self_score: pending
predecessor_score: pending
active_task: **BL-57 PLAN P12: PREPARE THE UPSTREAM PULL REQUEST.** Plan `docs/planning/changelog-rules-contradictions-plan.md` §P12 (`:892`): re-derive what PR #80's merge changed in the files this plan touches, bring `bl57/changelog-rules` onto `upstream/main` (`git merge-tree` at Phase 0 lists no conflicting paths; the branch is 17 ahead and 3 behind), dry-run `bin/sync` from the branch into scratch copies of all six adopters, run the suites in a `--no-local` clone, re-run §9.1, and draft the PR body. Pushing the branch and opening the PR (step 6) each wait for the operator's go-ahead. Chosen by the operator after Phase 0 (picker), over the trim alone with P8 next, BL-53, and two small backlog fixes. The `HANDOFFS.md` trim this session owes runs first, as its own commits.
what_was_done: pending
next_steps: pending
key_files: `docs/planning/changelog-rules-contradictions-plan.md:892` (§P12), `:9` (status line), `:50` (the branch-ledger placement rule); `docs/planning/BACKLOG.md:151` (BL-57); branch `bl57/changelog-rules` (tip `100f09b`, worktree `../methodology-bl57`)
gotchas: pending
runtime_smoke: pending
changelog_ref: CHANGELOG.md "2026-09-17 · [BL-57] S188 claim"
commit: pending
```

```handoff
session: S187
date: 2026-09-17
status: complete
self_score: 7
predecessor_score: 8
active_task: **BL-57 PLAN ITEM (22) IS DONE: `bin/status`'s STALE-SEED NOTE GIVES EACH SEED ITS OWN MIGRATION ROUTE, ON THE BRANCH P12 SHIPS (`100f09b`) AND MERGED INTO FORK `main` (`2d5ce70`), RECORDED AT `5b9a3e3`.** For `CHANGELOG.md` the note says replace the header; for `HANDOFFS.md`, bring across the seed's `## Size, and when to archive` section above the first receipt and keep the rest of the front matter. The `BOOTSTRAP.md` paragraph the note cites now says the same. The operator chose item (22) after Phase 0 (picker), then chose the route (second picker): commit on `bl57/changelog-rules`, merge into fork `main`, the plan's convention (items (11), (14)). **Item (22)'s premise was half wrong:** `BOOTSTRAP.md:384`–`386` is fork-only, not on the branch, so the paragraph the note cites (`:86` here, `:85` on the branch) had to carry the route. Nothing pushed, nothing upstream. **Next: P8 (`vscode_quarto_ext`), from that project, as its own session.**
what_was_done: **Phase 0:** `CHANGELOG.md` frontier `ae406d2` = HEAD, no gap; `HANDOFFS.md` frontier `1707051`, two behind, both `CHANGELOG.md`-only records with no receipt by design. Nothing backfilled. 2 receipts, no trim owed; `methodology_trim.py --check` fires on neither ledger. S186's gate citation re-run in a `--no-local` clone of `ae406d2`: `results 8e12f40caec1`, identical. Dashboard 76/100, no high flags. **`6fb428f`** claim, carrying Phase 0's two tracked rows. **Research:** the note's current text came from P1 (`2d5dc6e`); `BOOTSTRAP.md:383`–`386` was made per-file later by S178 (`fd611a6`), inside S41's fork-only *Without `bin/sync`* rules (`12463dd`), which the branch never had. The note and its cited paragraph are byte-identical on fork `main` and the branch, and so is Test 20, so one patch fits both trees; Test 20 never exercised a stale `HANDOFFS.md`. **The patch, test-first, in a `--no-local` clone of the branch:** Test 20 (g), eight assertions, run alone: 5 failures on the old code, among them *"the note tells a stale HANDOFFS.md to replace its front matter"*; `bin/status` gains `MIGRATION_ROUTES` beside `STALE_SEED` (the `HANDOFFS.md` route reads its section name from `bin/_manifest.py`'s marker; a file with no route gets a general rule) and prints a route per flagged file; the cited paragraph names a stale `HANDOFFS.md` and its route; 24/0 after. Two mutants fail it. `git merge-tree` measured before the route picker: with the branch's ledger entry, `CHANGELOG.md` is the only conflict. **`100f09b`** on the branch (in the `methodology-bl57` worktree): the four files are blob-identical to the tested tree, whose gate read `10/10 pass · results dd16434fe5f5`, `tests-sh-passed` 149. **`2d5ce70`** the merge: `CHANGELOG.md` ours, as at P5; the three files' changed lines identical to the patch; Test 20 24/0 on `main`. `bin/status` on the six adopters, read-only, before and after: each of the five present `BOOTSTRAP.md` copies one version further behind, none *locally modified*; `model_project_constructor` has none, before and after. (`mts-system`'s and `nprcgenekeepr`'s pre-merge readings, 8 → 9, were taken only at close-out, after `5b9a3e3` had already said *every*.) **`5b9a3e3`** recorded it: the plan's status line, item (22)'s DONE block with the premise correction, step 3's bullet, the BL-57 row, one ledger entry. **This close-out:** fork Learning #79, this receipt, the ledger entry.
next_steps: **(1) P8 — `vscode_quarto_ext`, from that project, as its own session.** Plan `docs/planning/changelog-rules-contradictions-plan.md`: procedure `:839`, step 3's `HANDOFFS.md` bullet `:851`, the DONE item `:871`, the P8 row `:887`, §9.8 `:1102` (all +14 since S186). `bin/status` now prints the right route for both seeds, so S186's gotcha (1) is retired; read-only at S187, the note for `vscode_quarto_ext` names both files, each with its own route. Its `BOOTSTRAP.md` reads 7 versions behind (6 before `2d5ce70`), and P8's sync brings it. At S187's Phase 0 it was on `master` `58f7bcbd` with only `scratchpad/` untracked. That is a reading, so re-run `git status --porcelain` there at the claim. **(2) THE NEXT PHASE 0 RUN HERE OWES A `HANDOFFS.md` TRIM:** this close-out leaves 3 receipts (S187, S186, S185). The claim makes 4, then `--cut 2 --force`, then the pointer fold in its own commit (S186's `67c3e10` + `fbc1aaf`). **(3) OUTWARD, EACH ITS OWN GO-AHEAD:** fork `main` is 6 commits ahead of `origin` once the post-close-out gate record lands (`6fb428f`, `100f09b`, `2d5ce70`, `5b9a3e3`, the close-out, the record). `bl57/changelog-rules` is 1 ahead of `origin/bl57/changelog-rules` (`100f09b`). Also BL-54's PR, and P12 (BL-62, BL-63, #80's F5; item (22) now rides the branch). **(4) `docs/FORK_LEARNINGS.md` IS 80,916 B AGAINST AN 81,920 B CEILING**, less than one median row of headroom. When the next row crosses it, answer BL-53 (how many learnings before old ones retire), as the `.context-budget.json` note says; don't raise the ceiling by reflex. **(5) SMALL AND FOUND, NOT FIXED (carried):** `docs/planning/BACKLOG.md:9`–`11`'s open list omits BL-63 (row `:156`); the six stale line numbers are now at `bin/tests.sh:2775` (were `:2752`; this session's 23 lines moved them); `wsfct`'s stale `HANDOFFS.md` seed, outside item (21). **CARRIED:** BL-61, BL-60 (folds BL-36), BL-65, `README.md`'s stale cost section (plan item (15)). The runner, `SAFEGUARDS.md` and the read-set total remain `over` budget.
key_files: `bin/status:149` (`STALE_SEED`), `:156` (`MIGRATION_ROUTES`), `:163` (`GENERAL_ROUTE`), `:244` (the per-file route join); `starter-kit/BOOTSTRAP.md:86` (the paragraph the note cites, now with the `HANDOFFS.md` route), `:379`–`386` (the fork-only per-file rule 2); `bin/tests.sh:341` (Test 20 (g)), `:363` (the assertion reading the cited paragraph); `bin/_manifest.py:117` (the `HANDOFFS.md` marker the route reads); `docs/planning/changelog-rules-contradictions-plan.md:9` (status line), `:50` (the branch-ledger placement rule), `:257` (item (22)), `:265` (its DONE block), `:851`, `:887`, `:892` (§P12); `docs/planning/BACKLOG.md:151` (BL-57); `docs/FORK_LEARNINGS.md:91` (#79); on the branch `100f09b`: `bin/status:113`, `starter-kit/BOOTSTRAP.md:85`, `CHANGELOG.md:395` (its entry)
gotchas: **(1) THE BRANCH'S LEDGER IS NOT DATE-ORDERED AT ITS TOP, BY RULE.** A new branch entry goes above the `[BL-57]` block and below `upstream/main`'s entries (plan `:50`), so `100f09b`'s 2026-09-17 entry (branch `CHANGELOG.md:395`) sits below upstream's 2026-09-16 ones. Don't "fix" it. **(2) EVERY MERGE OF THE BRANCH INTO `main` CONFLICTS IN `CHANGELOG.md`:** resolve ours, record in `main`'s own entry. The pre-commit hook skips merges, but `commit-msg` still wants the `Co-Authored-By` trailer. **(3) THE BRANCH IS CHECKED OUT IN THE `methodology-bl57` WORKTREE:** commit there (hooks apply), and measure in a `--no-local` clone. **(4) IN A SCRATCH CLONE, `git reset --hard HEAD~1` AFTER `commit -am` DISCARDS THE UNCOMMITTED WORK THE COMMIT SWEPT UP.** It happened here: the patch came back from the reflog, and nothing on a live tree was touched. Save a patch file first. **(5) `BOOTSTRAP.md:379`–`386` EXISTS ON FORK `main` ONLY.** P12 ships the branch's `:85` paragraph and no rule 2. **(6) `tests-sh-passed` READS 323 AT 3 RECEIPTS on `main`** (315 + the 8 new assertions), so expect 317 at 2. The floor is 305; don't tighten it from a post-claim reading. On the branch it reads 149, floor 138. **(7) zsh TRAPS RECURRED:** `$r:starter-kit/…` is a history modifier (write `${r}:…`), and an unquoted `echo ====` aborts the command. **(8) PHASE 0 WRITES TWO TRACKED ROWS**; they rode `6fb428f`.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `quality_ratchet.py --run` (which runs `bash bin/tests.sh`) IN A `--no-local` CLONE WITH HEAD ASSERTED.** **Citation, fork `main`, clone of `5b9a3e3` (the merge plus its record): `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results e7deb63146bb · manifest 3a87b16f1b31`**, `tests-sh-passed` 323 at 3 receipts. Branch, on the tree committed as `100f09b` (blobs checked): `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results dd16434fe5f5 · manifest 08423c179055`, `tests-sh-passed` 149. The close-out commit is not covered by that run (BL-64), so it is re-measured in a clone of itself after it lands and recorded as its own ledger entry. The tool's runtime behaviour was exercised directly: `bin/status` run read-only on `vscode_quarto_ext` from the patched tree printed both routes, and on all six adopters from `ae406d2` and from `2d5ce70`. Also: `bin/check-links` 0 after `5b9a3e3`; `bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations` 0 with row 79; `bin/check-handoff --allow-pending` 0 on the claim. **NOT EXERCISED:** an adopter actually following the new route (P8's to run); any push or upstream action; CI (none).
changelog_ref: CHANGELOG.md "2026-09-17 · [BL-57] S187 close-out", plus the claim and the item (22) entries; the branch's own entry is in `100f09b`
commit: 6fb428f (claim) + 100f09b (fix, on bl57/changelog-rules) + 2d5ce70 (merge) + 5b9a3e3 (recorded) + this close-out
```

**Self-assessment: 7/10.** Plus: the fix went in test-first, 5 red to 24 green, and two mutants fail it. I committed the
tested tree and checked it blob for blob. The merge's changed lines match the patch exactly, and every adopter's
`bin/status` reading was compared before and after the merge, BL-54's class. Reading the note's pointer, and the
branch P12 actually ships, turned up the item's false premise before it could ship a note whose cited paragraph never
mentions `HANDOFFS.md`. **Minus:** (1) my first picker described a change to fork `main` alone before I had checked
which tree P12 ships from, so the route needed a second picker. That is the order fork Learning #79 now names,
applied one step too late. (2) `5b9a3e3` said *every adopter's `BOOTSTRAP.md`* moved one version when I had
measured four of six. Measured at close-out, it held for all five present copies, and the plan's wording is
corrected. (3) A measurement in the scratch clone ran `git reset --hard` after a `commit -am` and
discarded the uncommitted patch. The reflog returned it, and nothing live was touched. (4) Two zsh traps my memory
names recurred, each costing one failed command. **Growth:** four ledger entries on `main`, one on the branch, 14 plan
lines, a learnings row (864 B). **Reduction:** none this session, which I'm stating here rather than leaving unsaid;
the trim this close-out makes owed falls to the next Phase 0 here.

**Predecessor (S186): 8/10.** Its item (2) named this task exactly and said *"no test pins its wording (grep of
`bin/tests.sh` and `tools/*.py` finds none), so a change needs a new assertion"*. That was true, and it shaped the
work. Its line numbers for the note (`:231`–`236`) held. Its gotcha (7), measure in a `--no-local` clone and never
`git checkout` on the live tree, was followed throughout. Gotcha (5)'s 309 at 2 receipts and item (3)'s *no trim
owed* both held at Phase 0, and S186's gate citation reproduced exactly. **Not 9:** item (22)'s *"both would ship in
P12's PR"* was half false, because `BOOTSTRAP.md:384`–`386` is fork-only. The handoff did not say that P12 ships
from the branch, so which tree the fix belongs on was left for me to discover. Nor did it note that the paragraph the
note itself cites gave only the `CHANGELOG.md` route. **ROI: strongly positive:** the task's shape and its test
requirement came straight from the handoff.

