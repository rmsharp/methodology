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
status: complete
self_score: 8
predecessor_score: 7
active_task: **THE FORK RESYNC IS DONE: FORK `main` CONTAINS `upstream/main` `6b29d3d`. R2 MERGED STAGES M2 `421ebf9`, M3 `7245f79` AND M4 `d4ac950`, CARRIED OUT D3 (`DASHBOARD_VERSION` 2.18.0, `e1b6bdf`) AND D2 (the ratchet tightened to measured values, `e55f204`), AND TRIMMED `HANDOFFS.md`. BL-57's P5 IS NEXT.** Chosen by the operator after Phase 0 (picker). The operator decided two questions mid-session, both by picker. First, restate `.context-budget.json`'s token ceilings rather than patch upstream's test (`0e8c6ac`). Second, no `CHANGELOG.md` trim: the 2026-09-14 decision governs over the plan's step. Fork-local: nothing pushed, nothing sent upstream.
what_was_done: **`374bd8c`** claim, with the Phase 0 snapshots. **`421ebf9`** M2: `.context-budget.json` kept ours; `bin/tests.sh` got both blocks (additions only); the dashboard table gained `quality_ratchet.py` and `.quality-gates.json` with upstream's signatures (equal on evaluation); upstream's per-file dict was dropped. `HANDOFFS.md` kept ours, because upstream's pending S20 stub fails `--all` below the newest receipt (plan §8 item 4). Measured 319 / 3 / 0 in a clone. **`8c429ed`** fixes two of the three red rows: the population guard 4 → 6 (a mutant check kills each new entry) and the fork's never-overwrite row in `starter-kit/BOOTSTRAP.md`. **`0e8c6ac`** (operator): read-set `max_tokens` 18,222 / 6,777 and the ledgers' redundant 25,000 dropped, with every `--json` verdict identical; the checkpoint measured 322 / 0 / 0. **`7245f79`** M3, 11 files: the hook got upstream's ratchet block then the fork's `--no-renames`; `CLAUDE.md` is the fork's whole file plus 3 rows; `README.md` and `T1_setup.md` took theirs (supersets); `check-handoff` got both blocks; the ledgers were rebuilt by rule (lossless); measured 333 / 0 / 0. **`d23d1a3`** records it and the no-trim decision; it was the first commit the chained ratchet checked. **`d4ac950`** M4, 1 file; measured 333 / 0 / 0, rows identical to M3's. **`e1b6bdf`** D3, 2.18.0 at every pin found by a whole-file search; the dashboard suite has 336 tests. **`75056a9`** trim, `--cut 2 --force`: S175, S23, S22 and S20 went to `docs/archive/HANDOFFS-through-2026-09-16-4.md`, 47,200 → 16,224 B, proof exit 0 before and after the commit. **`f4a8ec6`** fold. **`e55f204`** D2: `tests-sh-passed` 139 → 327 and `dashboard-unit-tests` 226 → 336, from `--run` in a clone of `f4a8ec6`. **`b4c3a45`** plan §8 (`:394`), BL-57 row, fork Learnings #69 and #70. Memory updated.
next_steps: **(1) BL-57's P5** (`docs/planning/changelog-rules-contradictions-plan.md:659`). Its scope is a `git apply -3` port, but re-derive it first: fork `main` now contains `64f23bf`, and **`git merge-tree --write-tree --name-only main bl57/changelog-rules` lists 5 conflicting files** (`CHANGELOG.md`, `CLAUDE.md`, `bin/_manifest.py`, `bin/tests.sh`, `starter-kit/SESSION_RUNNER.md`; computed at `b4c3a45`). The branch (`83a12f0`, 16 commits not on `main`) contains `64f23bf`, not `6b29d3d`, so decide merge vs port by measuring both. Pre-flight: `git fetch upstream`; if `upstream/main` moved past `6b29d3d` or PR #83 merged, a resync stage comes before P5. **(2) DONE AFTER CLOSE-OUT (operator go-aheads):** fork `main` pushed to `origin`: `9b96ac1..7b55ee3`, then `7b55ee3..70265f3`, then `c857e50`. **Standing grant (operator):** a commit that only records an authorized push goes to `origin` without asking, recording its own push; every other push still needs a go-ahead. **(3) DECIDED AFTER CLOSE-OUT (operator):** upstream's `TestThisRepoReadSetPartition` (`tools/test_context_budget.py:1232`) finding is **BL-62**, carried in BL-57's P12 PR, not filed on its own. Item (1)'s 5-file set was recomputed at `c857e50`: unchanged. **CARRIED:** BL-61, BL-60 (folds BL-36), BL-54 after P5; the runner and `SAFEGUARDS.md` stay `over` (recorded, not remedied).
key_files: `docs/planning/upstream-resync-2026-09-plan.md:394` (§8, overrides §2–§7); `docs/planning/changelog-rules-contradictions-plan.md:659` (P5); `.quality-gates.json:4` (`_fork_tightening`), `:11` (327), `:27` (336); `.context-budget.json:59`, `:76` (ledgers, no `max_tokens`), `:97`, `:106` (18,222 / 6,777); `tools/test_context_budget.py:1232` (the test that binds our config); `.githooks/pre-commit:42` (the ratchet); `bin/check-handoff:749`, `:762` (D9 lint); `starter-kit/methodology_dashboard.py:94` (2.18.0), `:748`, `:772` (ratchet entry; twin `tools/methodology_dashboard.py`, same lines); `tools/test_methodology_dashboard.py:2389` (version pins), `:2785` (population guard 6); `starter-kit/BOOTSTRAP.md:372`; `CLAUDE.md:82`; `bin/tests.sh:2117` (Test 34, the 2-receipt skips); `docs/FORK_LEARNINGS.md:81`, `:82` (#69, #70); `docs/HANDOFFS_ARCHIVE_INDEX.md:51`; `docs/planning/BACKLOG.md:152` (BL-57)
gotchas: **(1) EVERY CLOSE-OUT NOW OWES A GATE RUN.** `bin/check-handoff`'s D9 lint refuses a complete newest receipt without `quality_ratchet: N/M pass`. Run `python3 starter-kit/quality_ratchet.py --run` in a `--no-local` clone of the last pre-receipt commit (~17 min; it runs `bin/tests.sh`). The chained `pre-commit` refuses any loosened or removed gate. **(2) `tests-sh-passed` 327 IS THE 2-RECEIPT VALUE** (fork Learning #70): the suite reads 333 once a claim makes 3. A lone Test 9 (GitHub) failure fails both suite gates; re-run it, never loosen the gate. **(3) A `--no-local` CLONE LACKS `refs/remotes/upstream/*`:** a merge of an unreachable sha did nothing there, silently. Fetch the ref into the clone and `git cat-file -e` the sha first. **(4) DON'T RUN AN UNCHAINED `git add` AFTER A RESOLVE SCRIPT:** it staged conflict-marked files twice here. Hunk counts differ between a diff3 trial and the live merge. **(5) A PLAN STEP CAN CONTRADICT A STANDING DECISION IT NEVER CITES** (the `CHANGELOG.md` trim vs `3745748`): grep the ledger for decisions on the artifact before acting. **(6) UPSTREAM TESTS READ OUR ROOT CONFIG** (fork Learning #69): keep read-set `max_tokens` summing within 25,000 and no declared `max_tokens` on the two ledgers. **(7) `CHANGELOG.md` IS 250,241 B** after the follow-ups, 11,903 B under the 262,144 B refusal; `--check` fires by decision, and a trim is raised only past the refusal. **(8) ZSH:** `echo =====` recurred; quote it.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh` AND, SINCE M3, `quality_ratchet.py --run`, both in `--no-local` clones with HEAD asserted equal to the source commit.** **Final, clone of `b4c3a45`: `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results db4e547cc884 · manifest c09d7e7f9109`**; suite exit 0, **327 passed / 0 failed / 6 skipped** (Test 34's stated skips at 2 receipts, the only row change against M4); dashboard exit 0, v2.18.0, 76/100, gates panel *10 pass / 0 fail*. **Per stage:** claim `374bd8c` 309/0/0; M2 `421ebf9` 319/3/0 (the three flips diagnosed); trial of the config restatement 322/0/0; checkpoint `0e8c6ac` 322/0/0 (rows identical to the trial); M3 `7245f79` 333/0/0 (11 new rows, no flips); M4 `d4ac950` 333/0/0 (rows identical); D2's measuring run at `f4a8ec6` 10/10 pass (results 508b2b5489f3). **R2's DONE gates:** `git rev-list --count main..upstream/main` 0; `git ls-files -u` empty; the twins `cmp` equal; every §2.2 upstream-only path equal to `upstream/main`'s, `.quality-gates.json` differing only in two tightened thresholds and a note; `config_defects` `[]`; `bin/check-handoff --all --allow-pending` 0; `bin/check-links` 0; `bin/check-learnings` 0, and `--file docs/FORK_LEARNINGS.md --first 15` 0 (15..70); `.githooks/commit-msg --selftest` 0; the shard `.verify.sh` 0 before commit, after it, and after the fold; `context_budget.py --status` exit 2 at Phase 0 and close-out with no row changing status (plan §8 item 9). **NOT EXERCISED:** any push or outward action, adopter syncs, CI (none).
changelog_ref: CHANGELOG.md "2026-09-16 · [BL-57] S177 close-out", plus the claim, M2 + fixes, config restatement, M3 + no-trim decision, M4 + D3, trim, fold, D2 and plan §8 entries
commit: 374bd8c (claim) + 421ebf9 (M2) + 8c429ed + 0e8c6ac + 7245f79 (M3) + d23d1a3 + d4ac950 (M4) + e1b6bdf (D3) + 75056a9 (trim) + f4a8ec6 (fold) + e55f204 (D2) + b4c3a45 + this close-out
```

**Self-assessment: 8/10.** Plus: every stage was computed rather than predicted. The conflict sets were
re-derived against each committed predecessor, which found M3's 11, not the plan's 12. The suite ran in a
clone at every stage, with digit-masked row diffs, so M2's three red rows were isolated at once and nothing
else flipped anywhere. Two conflicts between the ratified plan and reality went to the operator as measured
options rather than being decided alone: upstream's test binding our config (verdicts diffed, the whole suite
run on the recommendation before offering it) and the no-trim decision the plan never cited. D2's floor was
measured at the state every close-out leaves, which caught the 6-row Test 34 swing before the tightening
could refuse this close-out. The ledger merges were built by one rule, and each was proven lossless.
**Minus:** an unchained `git add` staged conflict-marked files twice (caught before commit). `echo =====`
recurred. Twice I wrote a claim before measuring it (*"rows unchanged from S176's close"*, *"the notes
describe the 25,000 at length"*), and corrected both before they were committed. The S20 deviation at M2 was
my call under §2.4, not asked. **Reduction:** `HANDOFFS.md` 47,200 → 15,768 B. Growth: `CHANGELOG.md` +40,557 B
this session (upstream's three new entries, nine S177 entries and the trimmer's one), plan §8, two learning rows, and three `CLAUDE.md`
rows.

**Predecessor (S176): 7/10.** Its conflict sets (7 / 12 / 12 against `9b96ac1`) were exact, and gotchas (1)
S20/S22/S23, (2) `cca7941` lacks `0fd003a`, (3) the trailer on merges, (4) the whole-file search for D3 and
(6) the history files each shaped this session's work. **Not 8:** its item (1) told R2 to run the
`CHANGELOG.md` trim *"it already FIRES"* without surfacing the operator's standing 2026-09-14 decision not
to trim at the trigger, which would have been reversed silently if followed. It computed M3 and M4 against
the pre-M2 tree and did not flag that as an overestimate. And it could not see upstream's test binding our
config, which only an M2 trial would have shown. **ROI: strongly positive.**

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

