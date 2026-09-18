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
session: S190
date: 2026-09-18
status: pending
self_score: pending
predecessor_score: pending
active_task: **BL-57 PLAN ITEM (24): MERGE `bl57/changelog-rules` (`20db3f0`) INTO FORK `main`, BEFORE P8.** Fork `main` lacks the branch's last eight commits (`f572068`..`20db3f0`): its `bin/status` still keys `HANDOFFS.md` on the heading, and its `CHANGELOG.md` route still deletes the trimmer's lines. `git merge-tree` at Phase 0 predicts conflicts in `CHANGELOG.md` and `.context-budget.json` only, resolved ours as at `5f5a400`. Then Test 20 (g) on fork `main`, `bin/status` on the six adopters read-only before and after, the gates in a `--no-local` clone. Chosen by the operator after Phase 0 (picker), over BL-54's PR, BL-53 and P8. The same picker approved pushing fork `main` to `origin` after close-out. It also approved a `CHANGELOG.md` trim at its trigger, but my option had not cited the operator's standing 2026-09-14 decision not to trim there; asked again, the operator kept that decision. No `CHANGELOG.md` trim.
what_was_done: pending
next_steps: pending
key_files: `docs/planning/changelog-rules-contradictions-plan.md:326` (item (24)), `:335` (what it means for P8–P11), `:12` (status); `docs/planning/BACKLOG.md:151` (BL-57); branch `bl57/changelog-rules` (tip `20db3f0`, worktree `../methodology-bl57`)
gotchas: pending
runtime_smoke: pending
changelog_ref: CHANGELOG.md "2026-09-18 · [BL-57] S190 claim"
commit: pending
```

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

