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
session: S194
date: 2026-09-19
status: pending
self_score: pending
predecessor_score: pending
active_task: **BL-57 P10 (`nprcgenekeepr`): WRITE ITS LAUNCH PROMPT FROM FACTS MEASURED READ-ONLY IN THAT PROJECT, AND RECORD P10 HERE WHEN THE OPERATOR RELAYS ITS REPORT, AS S193 DID FOR P9.** Chosen by the operator after Phase 0 (picker), over P9's remainder, BL-53 and BL-73. P10 runs in `nprcgenekeepr`'s own session and starts with a decision about its 49-line local extension of `methodology_trim.py`. That project's own S718 was claimed at 02:03 today, so the launch waits for it to close. The same picker approved one side action: correct this repo's P9 records, which still say `mts-system` is not pushed (`b8a20ce` is on its `origin/master`, verified).
what_was_done: pending
next_steps: pending
key_files: `docs/planning/changelog-rules-contradictions-plan.md:1056` (the P10 row), `:372` and `:377` (item (25)), `:431` (item (28)), `:443` (item (29)), `:408`–`:409` (the P9 block), `:1055` (the P9 row), `:1270` (§9.8); `../nprcgenekeepr/CLAUDE.md:271`
gotchas: pending
runtime_smoke: pending
changelog_ref: CHANGELOG.md "2026-09-19 · [BL-57] S194 claim"
commit: pending
```

```handoff
session: S193
date: 2026-09-18
status: complete
self_score: 8
predecessor_score: 9
active_task: **BL-57 P9 (`mts-system`) IS DONE IN THAT REPOSITORY (its Session 139, `a48f543`..`b8a20ce`, not pushed there) AND RECORDED HERE (`676ca33`), RE-VERIFIED READ-ONLY FROM HERE. ONE REMAINDER STAYS THERE: A SUPERSEDED RULES BLOCK PARTWAY DOWN ITS `CHANGELOG.md` (item (28), its CLEANUP-006). P10 (`nprcgenekeepr`) IS NEXT.** Chosen by the operator after Phase 0 (picker), over BL-73, BL-53 and BL-54's PR, as S192 ranked it. The operator launched P9 from a prompt this session wrote, then said *continue*; the report was read from S139's receipt. The same picker approved three side actions, all done: `037335d` pushed to `origin`; the `tests-sh-passed` floor 305 → 331 (`e9b7962`); PR #84's description drafted (`8db82c2`) and, on a second go-ahead, posted (`99fb6bf`). Fork `main` is 6 commits ahead of `origin` after this close-out, not pushed: no go-ahead yet.
what_was_done: **Phase 0:** `CHANGELOG.md` frontier `037335d` = HEAD; `HANDOFFS.md` frontier `f6d1c0b`, three post-close-out records behind, no receipt owed; nothing backfilled. Gate on `037335d`: `results d56e26f10caf`, S192's citation. **Push:** `037335d` to `origin` (guarded, read back; entry in the claim). **`94c3fd5`** claim (Phase 0's two rows). **`e9b7962`** floor 305 → 331, measured at two receipts on `037335d`; gate on it 337 passed at three. **P9 launch prompt** written after running `bin/status` and `bin/sync --dry-run` on `mts-system` read-only; S139 reported its line numbers held. **`8db82c2`** PR #84 description draft: the fence-fix bullet, plus head, commit, diff and suite figures re-measured on `77afc12` (the old ones reproduced on `20db3f0` first; they exclude `CHANGELOG.md`), gate on a clone of `77afc12` `results 93ea168d093e`, 163 passed. **Posted** on the operator's second go-ahead (`gh api -X PATCH`, the live body re-fetched first, read back identical); recorded at **`99fb6bf`**. **`676ca33`** P9 recorded: plan status line, P9 block, items (28)–(29), P9 row; the BL-57 backlog row (also brought past BL-72, which S192 left stale). Re-verified from `--no-local` clones of `mts-system` `b8a20ce` and fork `main` `99fb6bf`: both ledgers `present`, every tracked file current, the dry run has nothing to write, both ledgers only gained lines (+61/−0, +78/−0) with every old line in order, `### ` 266 → 267 and the anchored audit 265 → 266 at `f70358c`, trimmer `L1_OK`–`L3_OK` on both. BL-72 on a real ledger: the unfixed checker (`20db3f0`) reads S138 as newest after P9 and skips S139; the fixed one reads S139. `--all`: the same 33 issues before and after.
next_steps: **(1) P10, `nprcgenekeepr`, ITS OWN SESSION, FROM THAT PROJECT; IT STARTS WITH A DECISION** (plan row `docs/planning/changelog-rules-contradictions-plan.md:1056`, reasoning high). Its 49-line local extension of `methodology_trim.py` blocks every sync, so the choice among the row's three options comes first. Then apply items (25) `:370` (its `.Rbuildignore` matches none of the new root files; `:377`), (28) `:431` (list the whole ledger's `## ` headings at the claim) and (29) `:443` (check what the synced tools write, e.g. `.context-budget-history.jsonl`, against its ignores). `nprcgenekeepr` was clean at `047d7f74` at this close-out. Write its launch prompt the way this session did: run `bin/status` and the dry run read-only first, and put the measured facts in the prompt. **(2) P9'S REMAINDER, IN `mts-system`, ITS OWN SESSION THERE, INDEPENDENT OF (1):** remove the 48-line block (`../mts-system/CHANGELOG.md:782`–`:829` at `b8a20ce`; re-derive it with `grep -n '^## How to add an entry' CHANGELOG.md`, since every prepended entry moves it) in one commit, then run §9.8 (`:1270`) with the block's bounds; this time it can fail. Predicted counts are in item (28). Whether to ignore `.context-budget-history.jsonl` (item (29)) is that project's call. Pushing there is that project's go-ahead. **(3) PUSH FORK `main` TO `origin`** when the operator says so: 6 commits (`94c3fd5`, `e9b7962`, `8db82c2`, `99fb6bf`, `676ca33`, this close-out). **(4) WATCH PR #84:** `gh pr view 84 -R KJ5HST/methodology --json state,headRefOid,reviews,comments`; OPEN at `77afc12`, no reviews, description current. **(5) BL-73, ITS OWN SESSION** (`docs/planning/BACKLOG-DETAIL.md:2501`); its three shapes are now at `../mts-system/HANDOFFS.md:294`, `:397`, `:749`. **(6) ANSWER BL-53 BEFORE ANY LEARNINGS ROW:** `docs/FORK_LEARNINGS.md` 81,721 of 81,920 B; five sessions' candidates are withheld. **(7) A `HANDOFFS.md` TRIM IS OWED AT THE NEXT PHASE 0:** this close-out leaves 3 receipts (S193, S192, S191); after the next claim, `--cut 2 --force --write`, then the fold in its own commit (S192's `b27236e` + `1c7e3c2`). **(8) `CHANGELOG.md` is 230,089 B**, past its trigger under the operator's standing no-trim decision; raise a trim at 262,144 B. **CARRIED:** BL-54's own PR, the `vscode_quarto_ext` relay (S191 (3)), BL-43, BL-68, BL-61, BL-60, BL-65, BL-66, `airqino`'s `HANDOFFS.md` migration in its own repository.
key_files: `docs/planning/changelog-rules-contradictions-plan.md:7`–`:17` (status line), `:408` (the P9 block), `:431` (item (28)), `:443` (item (29)), `:1005` (P6–P11 steps and DONE), `:1055`–`:1057` (the P9, P10, P11 rows), `:1270` (§9.8); `docs/planning/BACKLOG.md:151` (BL-57); `docs/planning/changelog-rules-pr-body.md:8` (posted note), `:60` (the fence-fix bullet); `.quality-gates.json:12` (floor 331), `:4` (why it is measured at two receipts); `../mts-system/CHANGELOG.md:782` (the remainder at `b8a20ce`), `../mts-system/BACKLOG.md:28` (CLEANUP-006), `../mts-system/scripts/deploy_vps.sh:82`, `:111`–`:112` (its deploy gate)
gotchas: **(1) §9.8 CANNOT FAIL ON A PURE INSERTION:** a control range prints the same. For an insertion, the evidence is `git diff --numstat` showing no deletions plus a check that every old line survives, in order, in the new file (the P9 block records both); the remainder in (2) is the first adopter commit where §9.8 can fail. **(2) A CONTROL MUST DIFFER BY THE CHANGE ALONE:** fork `main`'s checker against `upstream/main`'s disagrees for other reasons (fork `main` alone fails `mts-system` on 12 unreconciled `commit:` slots). Compare the branch before and after the fix (`20db3f0` vs `77afc12`) and ask `scan()` which block is first. **(3) THE TWO-RECEIPT FLOOR:** `tests-sh-passed` 331 is measured with `HANDOFFS.md` at two receipts; at three, Test 34 adds six and it reads 337. A trim back to two lands exactly on the floor, so a single lost test there fails the gate: that is the ratchet working, not a flaky test. **(4) PR #84'S DESCRIPTION IS A FORK FILE, POSTED BY HAND:** edit `docs/planning/changelog-rules-pr-body.md`, build the body from below its rule, re-fetch the live body and compare before a PATCH, and read it back (`jq` adds one trailing newline). **(5) ADOPTER LINE CITATIONS DRIFT BY ONE:** S192 wrote `:320` for an opener at `:319`, and S139 wrote `:293`/`:396`/`:748` for `:294`/`:397`/`:749`. Give every adopter line citation with its commit, re-derived from that commit.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `quality_ratchet.py --run` IN A `--no-local` CLONE WITH HEAD ASSERTED, SUITE OUTPUT SAVED.** **Citation, fork `main`, clone of the recording `676ca33`: `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results 6d2ca2197aa7 · manifest 61cd292c36bd`**, `bin/tests.sh` 337 passed / 0 failed / 0 skipped at 3 receipts; the same digest on the floor commit `e9b7962`. Branch, clone of `77afc12` (for PR #84's figures): `10/10 pass · results 93ea168d093e`, 163 passed. Phase 0 on `037335d`: `results d56e26f10caf`. The P9 migration was exercised directly: `bin/status`, `bin/sync --dry-run`, both trimmer dry runs, and three checker versions on `mts-system`'s ledgers at `710a0f7` and `b8a20ce`. This close-out commit is docs-only and not covered (BL-64). **NOT EXERCISED:** `mts-system`'s own tests (backend 664, admin 1336, web 105), which rest on S139's receipt; CI (none); the maintainer's review.
changelog_ref: CHANGELOG.md "2026-09-19 · [BL-57] S193 close-out", plus the claim, push, floor, PR-draft, PR-post and P9-recording entries
commit: 94c3fd5 (claim) + e9b7962 (floor) + 8db82c2 (PR draft) + 99fb6bf (PR post record) + 676ca33 (P9 recording) + this close-out
```

**Self-assessment: 8/10.** Plus: every option was run before it was offered. The P9 launch prompt carried `bin/status`
and dry-run figures measured that minute, and S139 found its line numbers held. Every outward action was guarded before it
ran and read back after, one at a time. The PR #84 figures were re-measured, and the old ones reproduced first as a
control. Every gate captured the suite's output, so no failure could go unnamed. P9 was re-verified rather than
transcribed, with a check that can fail where §9.8 cannot, and a clean before/after control for the BL-72 fix. S139's
question about restating counts was answered in the record. **Minus:** (1) The picker's P9 option said this session
would claim nothing until the relay, yet two go-aheads in the same picker committed; I claimed at once, so the option
text was wrong. (2) My first checker comparison set fork `main` against `upstream/main`, which differ by far more than the
fix; I caught it from the output, not before running it. (3) The launch prompt repeated S192's `:320` without re-deriving
it. (4) The first go-ahead approved *one paragraph*; the draft also changed four figures. Disclosed and shown before
posting, but wider than the option described. (5) `mts-system`'s tests were not re-run from here.
**Growth:** seven ledger entries, a 40-line plan block, an 11-line PR-body bullet plus its note.
**Reduction:** none, stated here rather than left unsaid.

**Learnings withheld from `docs/FORK_LEARNINGS.md`:** it is 81,721 of 81,920 B and BL-53 is unanswered. Candidates:
(a) a control must differ from its subject by the change under test alone; two versions that differ by more give a
verdict that cannot be attributed. (b) A check that cannot fail on the commit it is run on is not evidence: a deletion
check on a pure insertion passes vacuously, so run it on a control first and substitute one that can fail. (c) An
option's description is a commitment: check it against every other option in the same picker before offering it.

**Predecessor (S192): 9/10.** Next step (1) held throughout: plan row `:1011`, items `:370` and `:379`, *`--all` reports
only `:216` and `:671`*, and the prediction that the fixed checker would read `mts-system`'s newest receipt once P9 added
the section, which is exactly what happened. Item (7)'s 331 re-measured exactly. Gotcha (1) (the ratchet keeps no output)
is why every gate here saved the suite's output, and (5) kept zsh from aborting. Item (2), the PR #84 offer, went
straight into the picker. **Not 10:** it scoped PR #84's staleness as one missing paragraph, when the header's head,
commit and diff figures and the suite count were stale too. It left the BL-57 backlog row at *"next: BL-72, then
P9–P11"* after closing BL-72. Its `:320` was `:319`. **ROI: strongly positive.**

