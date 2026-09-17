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
     trim commit the shipped .verify.sh fails L2 (fork Learning #58). -->

```handoff
session: S177
date: 2026-09-16
status: pending
self_score: pending
predecessor_score: pending
active_task: **R2 OF THE RATIFIED RESYNC PLAN (`docs/planning/upstream-resync-2026-09-plan.md` §5 `:310`, with §7 `:355` overriding): MERGE STAGES M2 `cca7941`, M3 `64f23bf` AND M4 `6b29d3d` INTO FORK `main`, THEN D2's RATCHET TIGHTENING, D3's `DASHBOARD_VERSION` 2.18.0, AND THE `CHANGELOG.md` AND `HANDOFFS.md` TRIMS. CHOSEN BY THE OPERATOR AFTER PHASE 0 (picker).** Pre-flight re-derived at Phase 0: `upstream/main` still `6b29d3d`; PR #83 still open at `219fb9d`; `git merge-tree --write-tree --name-only HEAD <target>` lists 7 / 12 / 12 files, the same sets as §7 item 2. Fork-local; nothing pushed.
what_was_done: pending
next_steps: pending
key_files: `docs/planning/upstream-resync-2026-09-plan.md:310` (R2), `:355` (§7), `:120` (§2.3 rows), `:141` (§2.4 ledgers), `:166` (§2.5 gates), `:242` (D2), `:254` (D3); `docs/archive/HANDOFFS-through-2026-09-16-3.md` (S13–S19, S21: never re-add)
gotchas: `.githooks/commit-msg` has no merge skip, so every merge message needs its `Co-Authored-By:` trailer. `HANDOFFS.md` conflicts at every stage: keep only S20 (stub at M2, complete at M3), S22 (M3), S23 (M4). `cca7941` does not contain `0fd003a`. Run the suite in a `--no-local` clone of each committed stage; re-run a lone Test 9 failure, never waive it.
runtime_smoke: pending
changelog_ref: CHANGELOG.md "2026-09-16 · [BL-57] S177 claim"
commit: pending
```

```handoff
session: S176
date: 2026-09-16
status: complete
self_score: 8
predecessor_score: 8
active_task: **R1 OF THE RATIFIED RESYNC PLAN IS DONE: STAGE M1 (`0fd003a`) IS MERGED INTO FORK `main` (`5c2bd59`) AND D1 (A) IS CARRIED OUT. R2 (STAGES M2–M4, D2, D3) IS NEXT.** Chosen by the operator after Phase 0 (picker). The distributed `starter-kit/FRAMEWORK_LEARNINGS.md` is upstream's (rows 1–13, `#14` reserved). The fork's rows #15–#66 are in `docs/FORK_LEARNINGS.md`, verbatim, now with #67–#68. The suite is green in a clone of the last commit. Fork-local: nothing pushed, nothing sent upstream.
what_was_done: **`b85851f`** claim, with the Phase 0 snapshots. **`5c2bd59`** the merge, resolved per plan §2.3. `.context-budget.json` is ours (`git diff HEAD` empty). The learnings file is theirs (byte-identical to `0fd003a`). `CHANGELOG.md` interleaves upstream's 12 entries by date, and `HANDOFFS.md` places upstream's 8 receipts after the fork's. Both were built in Python and proved lossless: each upstream record is verbatim in the result, and removing them gives back the fork's file byte for byte. Suite on the merge: 303 / 3 / 0, the trial's three failures. **`8c35872`** Test 27.N1b runs its fixture commit with `METHODOLOGY_REQUIRE_COAUTHOR=0`, and the merge is recorded in the ledger. **`8cfaf0d`** creates `docs/FORK_LEARNINGS.md`, whose rows are byte-identical to `1f34e75`'s rows 15–66. It adds `bin/check-learnings --first N`, and the OK line now reads its span off the rows: the old form printed `1..65` for a table ending at #66. Test 32 gains a clean run, a no-flag run and a deleted-row mutant; a checker mutant ignoring `first` fails two of the three. `.context-budget.json`'s on-demand entry is re-pointed with the ceiling unchanged. **`82f0d3a`** turns 20 citation sites into *fork Learning #N*, two of which the plan's per-line inventory missed (both twins `:409`, where `Learning`/`#26` wraps). Test 18's #26 pin now asserts `[]` behind a new presence control, killed by a net-reads-nothing mutant. `add_row37` skips reserved numbers; a mutant without the skip reproduces *"missing #15"*. **`4ef6390`** adds the `CLAUDE.md` routing subsection and the index's #58 link. Suite: 309 / 0 / 0. **`084ba1b`** trims `HANDOFFS.md`, `--cut 2 --force`: S174 and upstream's S21, S19–S13 go to `docs/archive/HANDOFFS-through-2026-09-16-3.md`, 68,571 -> 16,296 B, proof exit 0 before and after the commit. **`28ae585`** folds the pointer block, and the front-matter #58 comment gets *fork* too. **Plan §7 written** (what R2 inherits), BL-53 and BL-57 rows updated, and fork Learnings #67 (S175's deferred learning) and #68 (this session's) appended.
next_steps: **(1) R2** (`docs/planning/upstream-resync-2026-09-plan.md:310`, **read §7 at `:355` first: it overrides §2–§5 where they differ**). Pre-flight: `git fetch upstream`; if `upstream/main` moved past `6b29d3d` or PR #83 merged, add a stage. For each of `cca7941`, `64f23bf`, `6b29d3d`: `git merge-tree --write-tree --name-only HEAD <target>` against the previous stage's committed result, `git merge --no-ff --no-commit`, resolve per §2.3 rows 1–13 and §7 item 3 for `HANDOFFS.md`, commit, then run the suite in a `--no-local` clone of that commit. Then D2's tightening commit (cite `quality_ratchet.py --run` from a clone), D3's 2.18.0 in both twins and both test pins, the `CHANGELOG.md` trim (it already FIRES, §7 item 4), and the `HANDOFFS.md` retention trim and fold. **R2's claim makes 3 receipts; this close-out leaves 2**, so R2's Phase 0 does not trim. **(2)** after R2: BL-57's P5 (`docs/planning/changelog-rules-contradictions-plan.md:659`). **Pending operator go-ahead, not taken:** pushing fork `main` (`f1ae291..` this close-out) to `origin`. **CARRIED:** BL-61, BL-60 (folds BL-36), BL-54 after P5; `SAFEGUARDS.md` is now `over` its no-growth pin (§7 item 7), recorded, not remedied.
key_files: `docs/planning/upstream-resync-2026-09-plan.md:355` (§7), `:310` (R2), `:120` (§2.3), `:141` (§2.4); `docs/FORK_LEARNINGS.md:1` (why it exists, citation form), `:25` (table), `:79`–`:80` (#67, #68); `bin/check-learnings:177` (`check_table(..., first)`), `:294` (`--first`), `:324` (span); `bin/tests.sh:1283` (27.N1b), `:2071` (Test 32's fork rows), `:2578`/`:2588` (`add_row37`, the reserved skip); `tools/test_methodology_dashboard.py:5353`, `:5403` (the #26 pin); `starter-kit/methodology_dashboard.py:405` (the disposition comment), `:453`, `:2153` (twin: `tools/methodology_dashboard.py`, same lines); `CLAUDE.md:31` (routing); `.context-budget.json:81`; `docs/HANDOFFS_ARCHIVE_INDEX.md:50` (the new row); `docs/planning/BACKLOG.md:148` (BL-53), `:152` (BL-57)
gotchas: **(1) R1'S TRIM MADE `HANDOFFS.md` CONFLICT AT EVERY LATER STAGE.** Against the pre-trim `4ef6390` it merged cleanly with `cca7941` and `64f23bf`; against `28ae585` it conflicts, because upstream's next receipts insert against S21, which is now in a shard. Add only S20, S22 and S23, and never re-add the archived S13–S19 or S21 (§7 item 3). **(2) `cca7941` DOES NOT CONTAIN `0fd003a`** (PR #82's branch; `git merge-base --is-ancestor` exit 1): its `HANDOFFS.md` has S20 `pending` directly above S19. **(3) THE COMMIT-MSG GATE HAS NO MERGE SKIP.** The ledger `pre-commit` skips merges (`MERGE_HEAD`, `.githooks/pre-commit:25`), and upstream's ratchet block sits after that skip (`64f23bf:.githooks/pre-commit:38`), but `commit-msg` runs on a merge commit too: every merge message needs its `Co-Authored-By:` trailer. **(4) A PER-LINE GREP MISSES WRAPPED REFERENCES** (fork Learning #68): D3's `DASHBOARD_VERSION` pins and any citation sweep need a whole-file `re` search. And a `git grep -E` alternative using `\b` matched nothing here, silently, beside alternatives that did match. **(5) SLICE A LEDGER'S FRONT MATTER AT THE ANCHORED FENCE** `(?m)^```handoff$`: an unanchored `index` stopped at the inline code span on `HANDOFFS.md:14` and hid the #58 citation. **(6) `context_budget.py --status` APPENDS TO `.context-budget-history.jsonl`**; the dashboard appends to `dashboard_history.jsonl`. Revert or commit them deliberately. **(7) ZSH:** `echo ====` and `"$r:path"` hit again; use `echo "===="` and `"${r}:path"`.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh` in `--no-local` clones, HEAD asserted equal to the source commit, exit codes read bare.** **`5c2bd59` (merge):** exit 1, **303 passed / 3 failed / 0 skipped**, exactly the trial's three. Run on their own: the dashboard suite 321 tests with 1 failure (the pin, nothing else behind the row), context-budget 116 OK, trimmer 123 OK. **`4ef6390` (D1 done):** exit 0, **309 / 0 / 0**; a digit-masked row diff against the merge shows the three FAIL->PASS flips and the three new Test 32 rows, nothing else. **`28ae585` (after trim and fold):** exit 0, **303 / 0 / 6**; the diff against `4ef6390` shows only Test 34's six rows becoming stated SKIPs at 2 receipts. **R1's DONE gates, bare, on `28ae585`:** `git merge-base --is-ancestor 0fd003a main` 0; `git ls-files -u` empty; `bin/check-learnings` 0 (13 rows); the fork file with `--first 15` 0; `bin/check-handoff --all --allow-pending` 0; `bin/check-links` 0 (105 links); `.githooks/commit-msg --selftest` 0 (7 checks); the distributed learnings file `cmp` equal to `0fd003a`'s; fork rows equal to `1f34e75`'s 15–66 (Python); the shard `.verify.sh` 0 after the trim and after the fold; the twins `cmp` equal; `python3 starter-kit/methodology_dashboard.py` 0 (76/100, in the clone). `context_budget.py --status` exit 2 before and after, with every row flip explained in plan §7 item 7. `methodology_trim.py --file CHANGELOG.md --check` FIRES (200,985 B), owed in R2. No `.quality-gates.json` on fork `main` yet, so no ratchet citation is owed. **NOT EXERCISED:** stages M2–M4, the ratchet, any push or outward action, CI (none).
changelog_ref: CHANGELOG.md "2026-09-16 · [BL-57] S176 close-out", plus the claim, the merge+27.N1b, the fork learnings file, the citations, the routing, the trim and the fold entries
commit: b85851f (claim) + 5c2bd59 (merge) + 8c35872 + 8cfaf0d + 82f0d3a + 4ef6390 + 084ba1b (trim) + 28ae585 (fold) + this close-out
```

**Self-assessment: 8/10.** Plus: every claim R1 makes was computed rather than predicted. The Phase 0
conflict set was re-derived. The suite ran in clones at three states, with row-level diffs, so a single
red row could not hide a second failure. Both ledger merges and the moved rows were proved lossless in
Python, and each new check was shown able to fail by a mutant. The implementation found three citation
sites the plan's inventory missed. It also computed that the plan's own retention trim turns
`HANDOFFS.md` back into a conflict at every later stage, which R2 would otherwise have met at M2.
**Minus:** two zsh traps already in memory recurred (`echo ====`, `$r:path`). My first `git grep`
inventory returned nothing because of `\b`, and my first front-matter search sliced at an unanchored
fence, the exact hazard S174's gotcha names; the known #58 comment not showing is what caught it. I
wrote a wrong per-number breakdown into a ledger entry and corrected it in the next commit. The stub's
gotcha said *"the merge commit skips the hooks"*; only `pre-commit` does. **Reduction:** `HANDOFFS.md`
68,571 -> 16,296 B at the trim; the distributed learnings file 79,483 -> 13,983 B. Growth: `CHANGELOG.md` is now
over its trigger (owed in R2), plus this receipt, plan §7 and two learning rows.

**Predecessor (S175): 8/10.** Its R1 was exact. The steps, the three trial failures with line numbers,
the one-line fix, D1's cost list, and *"`--cut 2` keeps R1's stub and the newest fork receipt"* all held,
and the 4-file conflict set was unchanged. Its gotchas (3) and (4), commit before cloning and run gates
in clones, shaped every verification here. **Not 9:** D1's inventory counted 23 sites with a per-line
search and missed the wrapped `#26` in the one comment the pin guards, plus a front-matter citation. It
named `bin/check-learnings`' *fixed path* as the gap when the tool already took `--file`; the real gap
was contiguity from 1. And it did not say that R1's trim would re-create the `HANDOFFS.md` conflicts it
had resolved. **ROI: strongly positive.**

