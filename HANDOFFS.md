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
never on a record count**, so the policy is applied by the session that notices: at Phase 0 run
`grep -c '^```handoff' HANDOFFS.md`; **above 2**, trim with `--cut 1 --force`. The force is
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
     trim commit the shipped .verify.sh fails L2 (Learning #58). -->

```handoff
session: S175
date: 2026-09-16
status: pending
self_score: pending
predecessor_score: pending
active_task: **TRIM `HANDOFFS.md` AND FOLD THE POINTER INTO THE INDEX, THEN RESYNC FORK `main` WITH `upstream/main` `6b29d3d`, CHOSEN BY THE OPERATOR AFTER PHASE 0 (picker).** Fork `main` is 56 commits behind (25 first-parent, merge base `598c459`); `git merge-tree --write-tree --name-only main upstream/main` lists 13 conflicting files. BL-53's retirement rule is decided inside the resync. Upstream PR #83 (planning only) conflicts in the same 13 files and is not acted on. Fork-local; nothing pushed, nothing sent upstream.
what_was_done: pending
next_steps: pending
key_files: `HANDOFFS.md:8` (retention policy), `:46` (the fold comment); `docs/HANDOFFS_ARCHIVE_INDEX.md:50` (the fold rule); `starter-kit/methodology_trim.py:1093` (`build_pointer_block`); `docs/planning/BACKLOG.md:148` (BL-53), `:152` (BL-57); the 13 conflicting files, re-listed by the command above
gotchas: The trim runs with `--cut 2`, not S174's `--cut 1`: this stub is an extra record, and `--cut 2` archives the same S173 and S172. Fold the pointer block in its own commit (Learning #58). Upstream's `.githooks/commit-msg` (`ad7bd37`) and the ratchet chained into `.githooks/pre-commit` arrive with the merge, and `core.hooksPath` is `.githooks` here, so every commit after the merge passes through them.
runtime_smoke: pending
changelog_ref: CHANGELOG.md "2026-09-16 · [BL-57] S175 claim"
commit: pending
```

```handoff
session: S174
date: 2026-09-16
status: complete
self_score: 7
predecessor_score: 8
active_task: **THE `HANDOFFS.md` HEADER CUT (BL-59) IS DONE, CHOSEN BY THE OPERATOR AT PHASE 0 (picker): THE SHARD TABLE MOVED OUT OF THE FRONT MATTER INTO `docs/HANDOFFS_ARCHIVE_INDEX.md`, SO A TRIM-AND-FOLD NO LONGER GROWS IT.** Front matter 7,028 B -> 4,019 B against the 7,168 B reserve (Test 39 A2). Three commits on fork `main`, local only, nothing pushed, nothing sent upstream.
what_was_done: **`e8bd62d`** -- `bin/tests.sh` Test 39's M2 mutant literal 4096 -> 2048 (`:3164`). Running the cut first in a throwaway clone took the suite from 306/0 to 305/1 on exactly that row: M2 is scored killed only while the LIVE front matter exceeds its literal, so the live file was its unstated fixture. Landed first so every commit stays green. **`ad3479a`** -- the 21-row shard table, its intro and the fold rule move to the new `docs/HANDOFFS_ARCHIVE_INDEX.md`. It sits outside `docs/archive/` on purpose: `bin/model-report:158`, `starter-kit/methodology_trim.py:921` and `starter-kit/methodology_dashboard.py:1135` find shards by `docs/archive/HANDOFFS-*.md`. Stale facts found in the move are corrected: *"20 trims, 154 receipts"* was 21 and 160, and the pre-trimmer `HANDOFFS-archive.md` (19 receipts) was never listed. The index prints derive commands instead of totals (22 files, 179 receipts). The spent-reserve callout goes. BL-59's backlog row records the cut. **`67ac209`** -- corrections from a read-only claims review (an opus subagent, ~45 claims checked): **the ~147 B per fold row I carried from the file's own callout was wrong** -- rows are 125-129 B, and the last fold added 123 B -- so S175's trim would have folded back under the reserve with ~11 B to spare. The cut was due one trim later than `ad3479a` says. Also fixed: the index's fold rule (insert position, bare-name cell, dropped proof link), *"rows unchanged"*, shard names with `-2`, the M2 comment's tense, and BL-59's row, which called N=1 unreachable beside `d13a165`, the commit that made it reachable. **Measured, not predicted:** a `--cut 1 --force` trim plus its fold on `ad3479a`, in a clone -- front matter 4,385 B inside the trim commit, back to the pre-trim size after the fold, and the new shard's `.verify.sh` exit 0 after both commits; suite **300 passed / 0 failed / 6 stated skips**. **N=1 is now reachable.**
next_steps: **(1) S175's PHASE 0 TRIMS, AND THE FOLD NOW GOES INTO THE INDEX.** This close-out leaves 3 receipts (`grep -c '^```handoff' HANDOFFS.md`), above 2, so run `python3 starter-kit/methodology_trim.py --file HANDOFFS.md --cut 1 --force --write` and commit the trim alone. Run the new shard's `.verify.sh`, then fold the pointer block into `docs/HANDOFFS_ARCHIVE_INDEX.md` by its rule (`:50`), in its own commit, and re-run `bash bin/tests.sh`. Expect 300 / 0 / 6 stated skips (Test 34 wants 3 receipts; BL-40); any FAIL is news. **(2) THEN THE FORK RESYNC**, the operator's order from S173: merge `upstream/main` into fork `main`. **Upstream moved at S174's Phase 0, `64f23bf` -> `6b29d3d`**: three KJ5HST commits, including `fb81c4b`, the first ratchet tightening after #82 (`.quality-gates.json`: tests-sh-failed max 0, tests-sh-passed min 139). Fork `main` is 56 behind. `git merge-tree --write-tree --name-only main upstream/main` lists **13** conflicting files, not S173's 12 -- the same 13 at S174's Phase 0 `f2c49f7`, so S174 added none. Three bear on this session's work: `HANDOFFS.md` (upstream's front matter must fit the same A2 reserve after the merge), `bin/tests.sh` (M2's literal), `bin/check-handoff`. BL-53's retirement rule is decided inside the resync (`FRAMEWORK_LEARNINGS.md` conflicts). **(3) THEN BL-57's P5** (`docs/planning/changelog-rules-contradictions-plan.md:655`, finding (9) at `:129`), ported from `64f23bf` as S173 decided. **DECIDED BY THE OPERATOR AFTER THIS CLOSE-OUT (picker):** fork `main` pushed to `origin`; **BL-59 CLOSED**; lowering `HEADER_RESERVE_BYTES` (`bin/check-handoff:663`) becomes **BL-61**, scheduled for a later small session, not ranked above (1)-(3) -- M2's 2,048 B literal must stay under whatever value it picks. **CARRIED:** BL-60 (folds BL-36); BL-54 after P5; `choose_cut`.
key_files: `docs/HANDOFFS_ARCHIVE_INDEX.md:3` (why it exists), `:19` (the pre-trimmer shard), `:23` (the glob warning), `:26` (the table), `:50` (the fold rule); `HANDOFFS.md:8` (retention policy), `:41` (why the index is not here), `:46` (the fold comment); `bin/tests.sh:3157`-`:3164` (Test 39 M2), `:3083` (how A2 measures), `:3133` (A2); `bin/check-handoff:663` (`HEADER_RESERVE_BYTES`); `starter-kit/methodology_trim.py:1093` (`build_pointer_block`), `:1103` (`insert_pointer`), `:921` (the shard glob); `docs/planning/BACKLOG.md:154` (BL-59's row)
gotchas: **(1) A NUMBER IN A FILE'S OWN CALLOUT IS A CLAIM.** The *"~147 B"* per row came from `HANDOFFS.md`'s own warning. I repeated it into a commit message and two ledger entries without measuring it, and a review found rows are 125-129 B. Count bytes with Python `.encode()` or `wc -c`. **(2) ANCHOR THE FENCE SEARCH** -- `(?m)^```handoff$`. An unanchored find matches the inline code span on `HANDOFFS.md:14` and reported 1,034 B for a 7,028 B front matter. I did it again at S174. **(3) NEVER PUT A `HANDOFFS-*.md` FILE IN `docs/archive/`** unless it is a shard: three tools glob it, and `tools/test_methodology_dashboard.py:4426` reads every `docs/archive/*.md` as a ledger. **(4) A GREP HIT THAT MEASURES A FILE'S SIZE NEEDS ITS OTHER OPERAND READ.** My grep listed Test 39 M2's live-file read, and I classed it as harmless; its fixed literal broke. Only the throwaway-clone suite run caught it. **(5) THE HANDOFF PROOFS WERE ALREADY 18 PASS / 3 FAIL** (`HANDOFFS-through-2026-08-02`, `-08-09`, `-08-25`), the same before and after this change -- BL-36, pre-existing. Each proof compares its trim commit with that commit's parent, so front-matter edits cannot move them. **(6) BL-59's AND BL-60's DETAIL BODIES STILL DESCRIBE THE TABLE AS LIVING IN `HANDOFFS.md`** (`docs/planning/BACKLOG-DETAIL.md:1824`, `:1903`, `:1928`) -- left as written by the file's rule, and proved byte-identical by its `.verify.sh`.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`**, run in `--no-local` clones whose HEAD sha was asserted equal to the source commit before anything ran, exit codes read bare, assertion sets diffed against the baseline with digits masked. **Baseline `be405b3`:** exit 0, **306 passed / 0 failed / 0 skipped**, A2 7,028 B (98%). **`e8bd62d`:** 306/0/0, identical set. **`ad3479a`:** 306/0/0, identical set, A2 3,929 B. **`67ac209` (HEAD):** exit 0, **306/0/0**, identical set, A2 **4,019 B (56%)**, M2 killed at 2,048 B. **The same cut before the M2 fix:** 305/1 -- the finding. **After a simulated S175 trim and fold on `ad3479a`:** 300/0/6, with only Test 34's six stated skips added. **The reviewer independently re-ran** `be405b3`, `e8bd62d`, `ad3479a` (306/0/0 each) and `ad3479a` with M2 reverted (305/1, the same row). **Other gates on fork `main`:** `bin/check-handoff --all --allow-pending` exit 0 (3 receipts); `bin/check-learnings` 0; `bin/check-links` 0 (105 links, unchanged); `docs/planning/BACKLOG-DETAIL.md.verify.sh` 0; `context_budget.py --status` exit 2 as at Phase 0, diffed row by row: **no status flips** (`HANDOFFS.md` 32,426 -> 30,791 B, `BACKLOG.md` +251 B). All 21 handoff-shard `.verify.sh` scripts gave identical exit codes before and after. Every relative link resolves: 3 in the front matter, 24 in the index, 51 in `BACKLOG.md`. **NOT EXERCISED:** a real trim on fork `main` (S175's), the resync, any push or other outward action, CI (none).
changelog_ref: CHANGELOG.md "2026-09-16 · [BL-59] S174 close-out", plus the claim entry and one entry per commit (`e8bd62d`, `ad3479a`, `67ac209`)
commit: be405b3 (claim) + e8bd62d + ad3479a + 67ac209 + this close-out
```

**Self-assessment: 7/10.** Plus: the first measurement corrected the file's own figure (140 B left, not
~60). I found the three-tool glob hazard before naming the new file. And I ran the change in a throwaway
clone before committing it, which is the only reason Test 39's M2 break was caught before it reached
`main`: 305/1, fixed first in its own commit. I also simulated the exact trim and fold S175 will run and
measured N=1 as reachable (300/0/6), and handed every claim to an independent reviewer. **Minus, and it
cost a correction commit:** I carried *"~147 B"* from the callout I was removing, without measuring it, into a
commit message and two ledger entries as the reason the cut was urgent. Rows are 125–129 B. That is the
error this repo keeps teaching: a number in a file is a claim. I measured the front matter unanchored
first (1,034 B), a hazard already in memory. My dependency grep showed M2's line and I classed it as
harmless. I read one exit code through a pipe before re-reading it bare. **Reduction:** the front matter is
3,009 B smaller, but `HANDOFFS.md` grew 32,426 -> 39,364 B with this receipt (3 receipts, where Phase 0
found 2), and a 5,096 B index file and five ledger entries were added. S175's trim takes the growth back.

**Predecessor (S173): 8/10.** Its item (1) was this deliverable, stated exactly: the deadline logic
(S174's claim makes 3 receipts, S175's Phase 0 trims) held, its *"140 B"* was correct where the file's
own callout said ~60, and its identified cut — the table into its own index — is what shipped. Its
gotcha about `git rev-parse --short` taking one ref saved a failed command at Phase 0. **Not 9:** it
passed *"one archive-table row"* along as the thing 140 B could not hold without measuring a row (125–129
B), which made the cut look one trim more urgent than it was. It also recorded 12 resync conflicts, where
`git merge-tree` lists 13 for its own close-out commit `dd1beeb` against `64f23bf`.

