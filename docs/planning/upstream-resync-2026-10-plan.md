# Resync plan 2 — merge `upstream/main` `f34769f` into fork `main` (BL-95)

**Status: DECISIONS TAKEN — D1–D7 were answered by the operator at S269's close-out picker (2026-10-06), every one as recommended (§3); R1 is DONE (S270, 2026-10-06: merge `2ed9262`, fix-ups `b7ded00`, `c333475`, `3b67019`, `d7c44ea`; local, nothing pushed) and R2 is not started and needs his commission.** Written at S269, a planning session: nothing is merged or rebased by it. Evidence
taken at fork `main` `f203159` and `upstream/main` `f34769f` (tag `v4.2`; fetched 2026-10-06, unchanged since
S268). §3's decisions were the operator's; each carries the recommendation he accepted, and §5's phases assume
those answers. Precedent: [`upstream-resync-2026-09-plan.md`](upstream-resync-2026-09-plan.md) (S175,
carried out S176–S177). S269 ran in two conversations: the first claimed the session and stopped after the
claim (`f203159`), leaving no plan; the second resumed that claim on the operator's choice at the Phase 0
picker (2026-10-06) and wrote this document.

## 0. The answer, in one paragraph

Fork `main` is **102 commits behind** `upstream/main` (69 first-parent, 11 merges) and 1,433 ahead, from merge
base **`77afc12`** (2026-09-18) — not S177's target `6b29d3d`: upstream's history now contains the fork's
merged PR branches (#84–#89, #91), so the base moved. Upstream changed **46 paths** since the base and the fork
also changed 24 of them. `git merge-tree` lists **17 conflicting files** (§2.3); 6 more auto-merge and need a
check; 22 arrive untouched; and `starter-kit/methodology_trim.py` is not among upstream's changes, so the
fork's P1–P3 trimmer work (offered upstream as PR #94) merges clean. A **trial merge in a scratch clone**
(§6: crude resolutions plus the fixes below, and once more with both ledgers folded) reached **451 passed / 1 failed / 0 skipped** on `bin/tests.sh`
(fork `main` today: 365 / 0 / 0, measured at this session's Phase 0 by a lone suite run and again inside the gate run), five unit suites green after one deliberate guard change, and **11 of 13
gates**; the one failing suite row and both failing gates are the same single finding (D3). The trial also
found four things the diff does not show (§2.3 rows 12–13, §2.4, §2.5): the fork's Tests 42–45 sit inside the
same conflict hunk as the tail of the test being replaced, so *order* decides whether the suite passes;
upstream's trimmed shard cannot be carried under its own name; the arriving shard entries carry links the
fork's trimmer refuses; and one hook now refuses a practice the fork's sessions have used. Seven decisions
are his; the two that cost something are how upstream's 118 unseen ledger entries reach the fork's ledger
(D2) and what to do with a finding in a frozen shard (D3). The plan recommends **one merge** (not S175's four
stages) and **two executor sessions**.

## 1. Target, and what is already decided

| | |
|---|---|
| **Target** | `upstream/main` `f34769f` (tag `v4.2`; the documented version is v4.1 — the v4.2 release docs are PR #92, open). Merge base `77afc12`. |
| **Order** | Operator, S269 Phase 0 picker (2026-10-06): this plan first (BL-95, `docs/planning/BACKLOG.md:180`); an executor session follows, as S176–S177 followed S175. |
| **Outward** | None. No push (each push of fork `main` is his go-ahead, every time), no PR, no comment on `KJ5HST/methodology`. |
| **Retention** | `HANDOFFS.md` keeps two receipts, trims above two (operator, S232; `HANDOFFS.md:8`). |
| **Root budget config** | The fork keeps its own `.context-budget.json` (D11, S146; restated S177). |
| **Learnings** | The distributed `starter-kit/FRAMEWORK_LEARNINGS.md` is upstream's; fork rows live in `docs/FORK_LEARNINGS.md` (D1, S175, ratified). Not reopened here. |
| **BL-96** | Its premise changes with this merge (§2.3 row 12): the guard it names is replaced; the uncounted skip is not. Its decision is D7. |

**The target moves.** Two of the fork's own pull requests are open upstream and touch files in this merge.
Measured with `git merge-tree` against a commit built from each branch's tip (`origin/docs/release-v4.2`
`fa2bb5d`, `origin/fix/trim-verify-false-red-issue93` `972eb2c`, both based on `upstream/main`):

| If, before the executor starts… | Then | Measured |
|---|---|---|
| neither has merged (today) | §2.3 as written | 17 conflicting files |
| **#92** merges | v4.2's `CLAUDE.md` §Versioning and README text arrive; D6's lift also takes v4.2 | merges cleanly onto upstream; the conflict set stays the same 17 files |
| **#94** merges | **+2 conflicting files**: `starter-kit/methodology_trim.py` and `tools/test_methodology_trim.py`, because the branch reworded lines the fork still carries (the S267 receipt counts six, `HANDOFFS.md:86`; `git diff --numstat main origin/fix/trim-verify-false-red-issue93` over the two files reads 1 line and 6 lines, in 6 hunks). Rule: **take upstream's text**; afterwards `git diff upstream/main main -- starter-kit/methodology_trim.py tools/test_methodology_trim.py` is empty. `.quality-gates.json` then conflicts in **4** hunks, not 5 (the trimmer floor is 181 on both sides: `ooto`). Its 3 `CHANGELOG.md` entries are folded by §2.4 | 19 files in the hypothetical (#92 and #94 both merged); #94 onto #92 conflicts in `CHANGELOG.md` alone (measured; both prepend) — the maintainer's to resolve, and the `merge=union` driver in `.gitattributes` handles it from v4.1 |

**Rule for the executor: re-derive §2.1 and §2.3 at pre-flight; if upstream moved, add rows; do not wait for it.**
Never rebase or force-push `origin/fix/trim-verify-false-red-issue93` or `origin/docs/release-v4.2`: they are
published pull-request heads.

## 2. Evidence-based inventory

### 2.1 Topology — and where the conflicts enter

`git merge-base main upstream/main` = `77afc12` ("fix(check-handoff): skip a fenced block with an info string…",
2026-09-18). `git rev-list --count 77afc12..upstream/main` = 102 (69 with `--first-parent`; 11 are merge commits, 10 of them on the first-parent line);
`77afc12..main` = 1,433, all first-parent. Upstream tags since the base: `v4.0` (`2f911c9`), `v4.1` (`1e018d1`),
`v4.2` (`f34769f`, lightweight); `v3.8` is `6b29d3d`, which fork `main` already contains.

Path sets (`git diff --name-status 77afc12 <side>`): upstream **46**, fork **467**, both **24**, upstream-only
**22**. The 24 are the 17 conflicting paths, the shard's `.verify.sh` (byte-identical on both sides, blob
`7ea4541`) and **6 auto-merged paths** that still need a look (§2.2).

Where the conflict set grows, from `git merge-tree --write-tree --name-only main <c>` for each first-parent
commit `c` of `77afc12..upstream/main` (69 runs, all against `main`; every row is in `upstream-resync-2026-10-evidence/stages.tsv`):

| First-parent commit | What it is | Newly conflicting | Cumulative |
|---|---|---|---|
| `1befe64` | S26 claim | `CHANGELOG.md`, `HANDOFFS.md` | 2 |
| `19f8d4f` | PR #89 merge | `.quality-gates.json` | 3 |
| `19566b6` | PR #88 merge | `starter-kit/BOOTSTRAP.md` | 4 |
| `af8a693` | PR #87 merge | `bin/status`, `bin/sync`, `bin/tests.sh` | 7 |
| `a9946c6` | PR #85 merge | `.githooks/pre-commit` | 8 |
| `d1c1154` | `CLAUDE.md` §Versioning archived | `CLAUDE.md` | 9 |
| `e010fdf` | upstream's `CHANGELOG.md` trim | `docs/archive/CHANGELOG-through-2026-09-30.md` (add/add) | 10 |
| `3e857aa` | budget re-measure | `.context-budget.json`, `.context-budget-history.jsonl` (add/add) | 12 |
| `3d1b25c` | dashboard 2.11.2 | both dashboard twins, `tools/test_methodology_dashboard.py` | 15 |
| `428c452` | `check-learnings` OK line | `bin/check-learnings` | 16 |
| `5158d39` | Phase 4 README tree | `README.md` | 17 |

**S175's caveat stands and was not re-measured here:** each set is computed against `main`, not against a
previous stage's resolved result, so a staged merge would conflict again wherever upstream re-edited a file.
That is the reason D1 recommends one merge: it resolves each file once, against the final text.

### 2.2 The 29 changed paths that do not conflict (6 auto-merged, 22 upstream-only, and the byte-identical shard proof)

**Auto-merged, changed on both sides — check the result** (`git merge-tree` said "Auto-merging", no hunk):

| Path | Fork's change since base | Upstream's | Check after the merge |
|---|---|---|---|
| `FRAMEWORK_APPARATUS.md` | +11 lines (the trimmer's timing-rule paragraph) | +5/−1 | both present; size 29,683 B (trial) |
| `HOW_TO_USE.md` | +1/−1 | +8/−2 (Multi-Agent Teams: two shapes, one-writer rule) | `bin/check-links` exit 0 |
| `docs/tutorials/T8_keeping_current.md` | +1/−1 | +1/−1 | `bin/check-links` |
| `starter-kit/SESSION_RUNNER.md` | +8/−2 | +10/−7 (FM #29, one-writer rule) | 55,406 → 55,016 B (trial); the table ends at `\| 29 \|` |
| `bin/_manifest.py` | +8 lines | +7 (the `.gitattributes` seed row; the literal-data constraint) | `len(DISTRIBUTION)` 30 (fork 29, upstream 30); upstream's Tests 32 and 34 (51 and 53 after renumbering) pass |
| `bin/check-handoff` | +528/−39 (the fork's block) | +39/−5 (fused-receipt check, one live pending per line of sessions) | `bin/check-handoff --all --allow-pending` exit 0 on the merged ledger |

**Upstream-only (22; the fork never touched them since the base) — arrive as written:** `.gitattributes`,
`bin/_manifest_reader.py`, `bin/check-ledger`, `docs/planning/parallel-sessions-plan.md`,
`docs/tutorials/{README,T1_setup,T2_first_session,T5_cautionary,TUTORIAL_TEMPLATE}.md`,
`docs/versioning-archive.md` (19,363 B; duplicates `docs/RELEASE_HISTORY.md`'s v1.0–v2.9 — keep, arriving files
are not edited), `ITERATIVE_METHODOLOGY.md` (+6,807 B: §Parallel Actors), `starter-kit/{context_budget.py,
FRAMEWORK_LEARNINGS.md,gitattributes,HANDOFFS.md,RECOMMENDED_SKILLS.md,SAFEGUARDS.md}`,
`tools/test_context_budget.py` and four `workstreams/*` files. After the merge `git diff upstream/main main`
over these 22 must be empty.

### 2.3 The 17 conflicting paths — resolution and verification

Hunk counts are `git merge-tree`'s (ort); hunk letters are in the order git prints them at these two
commits (`o` fork, `t` upstream, `b` fork then upstream) and **must be re-derived at pre-flight**. "Trial"
means the scratch merge of §6.

| # | Path | What each side did | Resolution | Verify |
|---|---|---|---|---|
| 1 | `.context-budget-history.jsonl` (add/add, 1) | both created it; the fork's holds its own measurements (growth run 177); upstream tracks its own since `3e857aa` | **ours** | `git diff HEAD -- .context-budget-history.jsonl` empty |
| 2 | `.context-budget.json` (2) | the fork's calibrated root config (D11); upstream's re-measure | **ours** | `git diff HEAD -- .context-budget.json` empty; `context_budget.py --status` rows diffed against pre-merge. Trial: runner 55,406 → 55,016 B, `SAFEGUARDS.md` 17,129 → 16,965, read-set total 72,535 → 71,981, **every status unchanged** (the same four `over` rows, exit unchanged) |
| 3 | `.githooks/pre-commit` (3) | the fork's 10-check selftest with BL-76 labels; upstream's 17-check selftest (7 added "lifecycle" checks for the never-edit gate, `106f22b`) and the same `REBASE_HEAD` comment reworded | hunks **`oto`**: fork's label wording, upstream's extra checks, fork's comment | `.githooks/pre-commit --selftest` prints `OK (17 checks)`; suite Test 43 (reads the marker list and the BL-76 label) passes. Behaviour change: §2.5 |
| 4 | `.quality-gates.json` (5) | four thresholds plus `pre-commit-selftest` added on both sides with different `why` text | hunks **`ootoo`**: each threshold the **higher** of the two (the ratchet only tightens): `tests-sh-passed` 343 (upstream 261), `dashboard-unit-tests` 336 (229), **`context-budget-unit-tests` 148 (upstream's; the fork's is 122)**, `trimmer-unit-tests` 181 (124); the fork's `pre-commit-selftest` | `quality_ratchet.py --precommit` accepts the commit. Upstream's `check-ledger` gate arrives un-conflicted (13 gates): D3 |
| 5 | `CHANGELOG.md` (1) | both prepend at one point | §2.4 | §2.4 |
| 6 | `CLAUDE.md` (4) | the fork's 14,392 B file against upstream's 49,722 B: upstream keeps v3.0–v4.1 narration in §Versioning (`upstream/main:CLAUDE.md:118,120,122` for v3.8, v4.0, v4.1), the fork moved it to `docs/RELEASE_HISTORY.md` | hunks **`oooo`**, then three edits: (a) one row in the starter-kit table for `starter-kit/gitattributes` (seed → `.gitattributes`), and the checker row of `upstream/main:CLAUDE.md:67` (`bin/check-handoff`, `bin/check-ledger`, `bin/check-learnings`) added to the Tools table, since the fork's file has no `bin/` rows and names `bin/check-learnings` only in prose (`:56`); `bin/_manifest_reader.py` is named in neither tree, so leave it out; (b) `documents 28 failure modes` → **29** (`CLAUDE.md:135`); (c) the version line (`:145`) and `docs/RELEASE_HISTORY.md` per D6 | `bin/check-links` exit 0; size under the resident ceiling (14,392 B against 18,600 B today); the failure-mode count agrees with the runner's table |
| 7 | `HANDOFFS.md` (1) | the fork's three receipts (S269 pending, S268, S267); upstream's 38 | §2.4 | §2.4 |
| 8 | `README.md` (1) | one tree line: the fork's `model-report`, upstream's `check-ledger` | hunk **`b`** (both lines) | both names present; `bin/check-links` |
| 9 | `bin/check-learnings` (1) | the same fix both sides (the OK line must name the highest number, not the row count): the fork's prints `min..max`, upstream's `1..max` | **ours** (a superset) | `bin/check-learnings` exit 0, trial: "16 rows, contiguous 1..17, 0 over 1,500 B" (upstream's row #17 is 1,060 B and the largest row in the table is #12 at 1,451 B; both are under the 1,500 B row budget) |
| 10 | `bin/status` (4) and 11 `bin/sync` (4) | the fork's BL-54 re-implementation of what upstream took under #87 (fork `865119f`, `2c4f801`; upstream `5f4c3f9`, `0277396`), then upstream moved `--source=github` from `gh api` to a git clone (`252a4b6`) and to the source's own manifest (`9b69070`, `fa44be6`, PR #91) | **theirs**, both files. Measured loss: of the lines the fork added since the base, **4 of 57 in `bin/status`** (BL-54 labels, one `history[src] = {}`) and **48 of 74 in `bin/sync`** (the `gh api` fetch: `GitHubFetchError`, `fetch_all_github`) are absent from upstream's version (non-blank added lines, by exact stripped-line membership in upstream's file; 67 and 85 counting blanks; a moved line counts as present) | the suite's Tests 9, 41 (as relabelled below) and 46–53 (upstream's 27–34 after renumbering); `bin/sync --source=local` into a scratch project exits 0 (trial: created all files) |
| 12 | `bin/tests.sh` (4, one region: on main, Test 41 at `:3371` through Test 45 at `:3703`) | **the same test written twice**: the fork's Test 41 (`bl54_*` helpers) and upstream's Test 26 (`mh_*`); hunk 4's fork side is the *tail* of Test 41 (three `bl54_sync` lines and its closing `rm -rf "$M" "$P"`) **followed by the fork's Tests 42–45**; upstream's side is the tail of its Test 26 **followed by its Tests 27–34**. Seven of upstream's numbers collide with different fork tests (28–34); the fork has **no Test 27** (it was removed at S178 with the hook's claim carve-out, `bin/tests.sh:1313`–`:1315`) | hunks 1–3 **theirs**, header relabelled **Test 41** (the fork's number, which fork learning #72 cites; the two bodies differ only in fixture construction — upstream wraps it in `mh_fixture()` and copies `bin/_manifest_reader.py` — and in helper names; the four assertion rows are the same, and the fork's "(BL-54…)" label and three provenance comments are lost). Hunk 4, **in this order**: upstream's tail (three `mh_sync` lines and its `rm`), then the fork's Tests 42–45, then upstream's Tests 27–34 **renumbered 46–53** (one offset, +19; Test 27's slot stays vacant). **Drop the fork's three `bl54_sync` lines and its `rm`.** Put one comment above the renumbered block: `# upstream's Tests 27-34 = Tests 46-53 here; its Test 26 = Test 41`. **Four textual references go with the renumbering** (inventory: `git grep -nE 'Tests? (26|27|28|29|3[0-4])([^0-9]|$)' upstream/main` outside ledgers, plans and archives): Test 27's header and its comment ("Test 26" → "Test 41", `upstream/main:bin/tests.sh:1041`, `:1045`), `mh_fixture`'s comment ("Test 27" → "Test 46", `:983`), and `bin/_manifest.py:35` ("Test 34" → "Test 53") | the suite (§5 R1 DONE). **Measured, three runs** (only the third is saved): bl54 lines kept, wrong order → 5 red (3 rows at exit 127); bl54 lines removed but the fork's closing `rm -rf "$M" "$P"` kept ahead of upstream's tail → 4 red (the same 3 rows: that `rm` had removed `$M` and `$P` before the `mh_sync` calls ran); right order, fork `rm` dropped → 1 red. **The trial did not renumber** (its log has headers 26 and 28–34 twice), so every suite-row name the trial reports is upstream's number. Test 9 arrives as upstream's: its guard is `git ls-remote` reachability, not `gh` auth, and its skip stays a bare `echo "  SKIP: …"` (D7) |
| 13 | `docs/archive/CHANGELOG-through-2026-09-30.md` (add/add, 3) | both sides trimmed to the same name: the fork's `07af992` (89 records, 154,936 B) and upstream's `e010fdf` (96 records, 213,940 B); **zero headings in common** | **ours, byte-identical** | §2.4 — the proof depends on it |
| 14 | `starter-kit/BOOTSTRAP.md` (1) | both carry the three-rules update section; upstream's is newer and drops the `gh` note | **theirs** (this also drops the fork's rule-2 sentences on `ledger-format: 2` and the `## Size, and when to archive` section, lines 385–388 on main; the migration route survives in upstream's §Setup paragraph and in `bin/status`'s note), then **add `.gitattributes` to the never-overwrite row** (`Adopter-owned`: `.context-budget.json`, `.quality-gates.json`, **`.gitattributes`**) and "those six" → "seven" | suite Test 28 (pins that row to the manifest): **trial red until this edit** — upstream's own text omits its own seed |
| 15–16 | `starter-kit/methodology_dashboard.py`, `tools/methodology_dashboard.py` (3 each; twins byte-identical on both sides) | `DASHBOARD_VERSION` 2.19.0 against 2.11.3; the fork's `_FRAMEWORK_INSTALLED_CONTENT` table (`:771`) against upstream's tuple extended by `.gitattributes` and a 111-line per-file signature dict (`_FRAMEWORK_FILE_SIGNATURES`, which the fork's file does not contain — S175's row 11) | hunks **`ooo`**, then a port into the fork's structure: `_GITATTRIBUTES_SIGNATURES = ("Methodology ledgers", "CHANGELOG.md merge=union", "HANDOFFS.md is deliberately NOT listed")` and the row `".gitattributes": (None, _GITATTRIBUTES_SIGNATURES)` after the `.quality-gates.json` row (the manifest lists the seed after `quality-gates.json`); version per D5. The dotfile entries in `CONFIG_FILES` and the `name.lower() in CONFIG_EXTS` match auto-merged | `cmp` the twins; `python3 starter-kit/methodology_dashboard.py` exit 0 |
| 17 | `tools/test_methodology_dashboard.py` (1) | the two version pins (`:2396`, `:2398` on main) | **ours**, pins follow D5; then the population guard `assertEqual(len(md.FRAMEWORK_INSTALLED_SOURCE), 6` (`:2787` on main) → **7**, deliberately, as S177 raised 4 → 6 | dashboard suite: trial 353 tests, **1 red before the raise, 0 after** |

### 2.4 The two ledgers

**The rule** is `HANDOFFS.md:24`–`:29`: two sequences, never renumbered, a receipt identified by session **and
date**, each incoming one checked against ours, and within a shared date the fork's first.

**`CHANGELOG.md`.** Fork live ledger: 275,433 B as a file, 268 entries (2026-09-27…10-05), plus 19 shards
holding 1,067 entries. Upstream: a live ledger of 56,126 B holding 72 entries, and one shard of 213,940 B holding
96. (Entry byte counts below, 139,967 B for the 118 absent entries and the like, are sums of entry text, not
file sizes.) **All 87 entries upstream added
since the base are absent from the fork's corpus by exact heading**; of upstream's 168 entries in all, **118
(139,967 B) are absent** (72 live, 46 from the shard) and 50 are already held — 43 byte-identical, 7 with a
different body (the fork's copy is kept; `fold-ledger.py` names them).

- **Fold, don't carry (D2 A).** `python3 docs/planning/upstream-resync-2026-10-evidence/fold-ledger.py
  changelog` inserts the 118 entries into the live ledger by date (the fork's entries first within a day) and
  prints whether its figures match this plan's (**386 entries, 415,398 B**; `bin/check-ledger` on the result: OK,
  no findings). **It reads the fork's side from git (`--fork-ref`, default `HEAD`), never from the working tree**,
  so it is correct in the middle of a plain `git merge --no-commit` with conflict markers and upstream's shard in
  the tree — the reviewer of this plan showed that the first version, which read the working tree, folded nothing
  there and printed a plausible result. Verified byte-for-byte against the trial's folded ledger in a real
  conflicted merge, for both modes.
- **Why upstream's shard is not carried under any name.** Both trims are named `…-2026-09-30.md`. A shard's
  generated proof finds its trim commit with `git log --diff-filter=A -1 -- "$SHARD"`
  (`docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh:17`), a lookup by **path**. With the fork's file kept
  byte-identical, the merge is TREESAME to its first parent for that path and git's default walk prunes
  `e010fdf` (fork learning #103's mechanism, relied on here; a `--full-history` walk shows it): **measured, the
  fork's proof exits 0 in the trial and in a scratch merge commit** (L1, L2/front-matter, L3, trim commit
  `07af992`). A content merge of the two shards would defeat that pruning and point the proof at the wrong
  commit; a renamed shard needs a proof the trimmer cannot generate (`--reverify` is read-only).
- **Shard-sourced entries carry archive-relative links.** The trimmer rebases `](x)` to `](../../x)` when it
  archives, so upstream's shard holds the `../../` form. Folded back into a root ledger the form points outside
  the repository, and the fork's trimmer refuses the range: **`TRANSFORM_NOT_INVERTIBLE … record(s) 93`**,
  measured on the folded ledger (one entry, `### 2026-09-16 · [BL-57] The runner cites the ledger rules…`, one
  link). `fold-ledger.py` applies the inverse (`](../../` → `](`) to shard-sourced entries only; with it the dry
  run is clean: **L1, L2, L3 OK; `--cut 280 --force` would archive 106 of 386 records (2026-08-10 → 2026-09-29)
  to `docs/archive/CHANGELOG-through-2026-09-29.md` — a fresh name, so no collision — and take the live ledger
  415,398 → 255,204 B.**
- **Order.** The trimmer refuses while the undocumented set is non-empty (`P1_UNDOCUMENTED`: 93 commits past the
  ledger frontier in the trial). The merge commit changes `CHANGELOG.md`, so it becomes the frontier and the set
  empties; **the trim is its own commit after the merge**, never inside it.

**`HANDOFFS.md`.** Upstream holds 38 receipts (221,642 B); the fork's checker passes all 38 as they stand
(`bin/check-handoff --file <upstream's> --all`: OK). Of them, **21 are already in a fork shard** by session and date (S1, S2, S3, S5, S7–S23;
18 byte-identical, 3 differ: S1, S2 and S5) and **17 are not** — S39…S24, including `S35-alpha` and
`S35-beta` — 87,461 B in all, 3,001 to 8,785 B each, all under the fork's 12,288 B record budget.
`python3 …/fold-ledger.py handoffs` builds the merged ledger (the fork's front matter and receipts, then the 17 in
upstream's order) and prints whether its figures match. The merged ledger: the fork's front matter and three receipts, then the 17 below them
(dated 2026-09-16…10-02 against the fork's 2026-10-05): 20 receipts, 114,995 B, `check-handoff --all
--allow-pending` OK. The retention trim (`--cut 2 --force`) dry-runs clean: **archives 18 of 20 to
`docs/archive/HANDOFFS-through-2026-10-05-5.md`; L1, L2, L3 OK; live 114,995 → 16,628 B.** It reports
`FRONTIER_PENDING_STUB` while a claim is open (advisory: keep the trim and the finalize in separate commits) and
`FRONTMATTER_FIELD_ABSENT` (expected, `HANDOFFS.md:31`). **A merge commit has no ledger entry of its own**: the
hook skips merges, so the next ordinary commit's entry records it (S176 precedent). **One sentence goes stale
between R1 and R2:** the front matter says "Every upstream receipt is now archived; every receipt retained here is
the fork's" (`HANDOFFS.md:26`–`:27`); with 17 upstream receipts live it is false until R2's trim, and nothing
checks it — R2's DONE does.

### 2.5 What arrives that changes how the fork works

None of these is a conflict; all are behaviour.

- **The never-edit gate (`106f22b`).** The *rule* is already the fork's: `FRAMEWORK_APPARATUS.md:445`, "A
  committed entry is never edited. A correction is a new entry that names what was wrong." What arrives is the
  hook that **refuses** a staged ledger that changes or drops a committed entry (17-check selftest, pass). Fork
  sessions have broken the rule on paper — S268's receipt records correcting its own earlier ledger entry in
  the close-out commit, and S267's records that upstream's hook refused an `--amend` of an entry already in HEAD
  (`HANDOFFS.md`, gotcha 4) — and from the merge on this fork's hook refuses both; the remedy is a "Correction"
  entry, and for an `--amend` of a ledger line in HEAD S267's remedy: soft-reset the unpushed commit and
  recommit, never `--no-verify` (a recorded bypass). The gate exempts any commit that stages a file under
  `docs/archive/` (`upstream/main:.githooks/pre-commit:198`), which is how a trim passes. D4.
- **`.gitattributes`** (seed `starter-kit/gitattributes`): `CHANGELOG.md` and the two `.jsonl` histories merge
  by `union`, `HANDOFFS.md` deliberately not. It binds from the merge on, so the *next* resync's ledger hunks
  resolve silently by concatenation; `bin/check-ledger` reads the result. A line-level driver keeps lines, not
  records (fork learning #90), which is why `HANDOFFS.md` is excluded and why `check-ledger` exists.
- **`bin/check-ledger` and its gate**, `check-ledger --all`, max 0: D3.
- **FM #29** ("Shared-state interference"), §Parallel Actors in `ITERATIVE_METHODOLOGY.md`, Learning #17 in the
  distributed learnings, sequence tags (`S35-alpha`) in the `HANDOFFS.md` seed, and `check-handoff`'s one live
  pending receipt per line of sessions. The fork's `CLAUDE.md` and tutorials say 28 failure modes; the
  tutorials arrive saying 29.
- **`bin/sync`/`bin/status --source=github`** clone the repository; `gh` is no longer required.
  `bin/_manifest_reader.py` reads `bin/_manifest.py` as data (`dd1bba2`): every name it binds takes one plain
  assignment, no `+=` or `.append`. The fork's manifest passes (upstream's Tests 32 and 34, which are Tests 51 and 53 after renumbering; in the trial they ran under their own numbers).
- **`context_budget.py` 1.3.1** (worktree-aware `--calibrate`) and its 148-test suite (fork 122).

### 2.6 The gates, against measured values

Declared on each side: 12; the fork's set has `close-out-report-unit-tests`, upstream's has `check-ledger`;
the merge has **13**. Measured in the trial (`docs/planning/upstream-resync-2026-10-evidence/trial-gates.log`):

| Gate | Merged floor | Trial measured | Status |
|---|---|---|---|
| `tests-sh-passed` | 343 | 451 | pass (floors are set at the two-receipt state, fork learning #70) |
| `tests-sh-failed` | 0 | **1** | **fail** — the real-ledger row of upstream's Test 31 (Test 50 after renumbering; D3) |
| `dashboard-unit-tests` | 336 | 353 | pass |
| `context-budget-unit-tests` | 148 | 148 | pass (2 skipped, as upstream) |
| `trimmer-unit-tests` | 181 | 181 | pass |
| `close-out-report-unit-tests` | 68 | 68 | pass |
| `ratchet-unit-tests` | 45 | 45 | pass |
| `check-links` / `check-learnings` / `check-handoff-all` | 0 | 0 / 0 / 0 | pass (116 links; 16 rows, contiguous 1..17) |
| `check-ledger` | 0 | **1** | **fail** — one finding in a frozen shard (D3) |
| `commit-msg-selftest` / `pre-commit-selftest` | 0 | 0 / 0 | pass (7 and 17 checks) |

Summary line: `quality_ratchet: 11/13 pass · 2 fail · 0 unmeasured · results 07deaefe7f86 · manifest 7a4a86985f5c`.

### 2.7 Adopter impact

The six adopters sync from fork `main` (`bin/status` → `bin/sync`). Comparing each `bin/_manifest.py`
`DISTRIBUTION` source in the trial against fork `main`: **16 of 30 change** — `SESSION_RUNNER.md` 55,406 →
55,016 B, `FRAMEWORK_LEARNINGS.md` 16,560 → 17,621 (#17), `SAFEGUARDS.md` 17,129 → 16,965,
`RECOMMENDED_SKILLS.md` 17,453 → 18,501, `BOOTSTRAP.md` 36,297 → 36,737, `methodology_dashboard.py` 255,019 →
255,770 (**so the version must bump**, D5), `context_budget.py` 73,009 → 78,172, the `HANDOFFS.md` seed 12,109 →
13,523, **a new seed `starter-kit/gitattributes`** (1,339 B, installed once, never overwritten),
`ITERATIVE_METHODOLOGY.md` 59,770 → 66,577, `HOW_TO_USE.md` 55,892 → 56,850, `FRAMEWORK_APPARATUS.md` 29,348 →
29,683, and four workstream or campaign documents (+74 to +331 B). The 14 others are unchanged. R2 re-measures
this against the real merge result.

## 3. Decisions for the operator

**Decided (operator, picker at S269's close-out, 2026-10-06) — every recommendation:** D1 (A) one merge, R1 + R2; D2 (A) fold the
118 entries into the live ledger and keep the fork's shard byte-identical; D3 (A) scope the gate and the one real-ledger
assertion to the live ledger; D4 (A) adopt the never-edit gate; D5 (A) `DASHBOARD_VERSION` 2.20.0; D6 (A) state v4.1 and
lift v3.8, v4.0 and v4.1 into `docs/RELEASE_HISTORY.md`; D7 (A) count BL-96's skip. He also approved the push of fork `main`
(six commits, done: `ab171c3..5f302c0`, then the CHANGELOG-only push record `a4c5587`). The options below stay as the
record of what was weighed.

### D1 — Merge shape, and the session split

| Option | What it does | Cost |
|---|---|---|
| **(A) Recommended — one merge, then fix-up commits; R1 + R2** | One `git merge --no-ff upstream/main`, 17 files resolved once against final text; fix-ups in ≤5-file commits | The trial did exactly this and reached 451/1. The blast-radius cap is per commit, a merge is one commit, and `SAFEGUARDS.md` already treats a committed-mode `bin/sync` as one commit whatever its file count; S151's merge `213f841` is the precedent |
| (B) Four stages, as S175 | Merge `19566b6` (4 files), `d1c1154` (+5), `3e857aa` (+3), then `f34769f` (+5): none resolves more than five new files; the suite runs between | Ledgers, `bin/tests.sh` and the dashboards are resolved up to four times, each against text the next stage rewrites (§2.1 caveat); four suite runs of about 8 minutes |
| (C) One stage per upstream boundary (11) | Smallest steps | Not recommended: eleven merge commits and eleven suite runs for 17 files |

### D2 — How upstream's unseen `CHANGELOG.md` entries reach the fork (118 entries, 139,967 B)

| Option | What it does | Cost |
|---|---|---|
| **(A) Recommended — fold into the live ledger; keep the fork's shard byte-identical** | `fold-ledger.py` (§2.4); upstream's shard is not carried; its 46 unseen entries become live entries and the next trim archives them under a fresh name | Live ledger 275,433 → 415,398 B in the merge commit, then 255,204 B after the trim (its own commit and proof, §5 R2). Lossless in-tree; no proof touched |
| (B) Carry upstream's shard under `…-2.md` | Keeps upstream's records in their shard | The proof is keyed on the path and cannot be generated for a renamed shard by this trimmer; a hand-edited proof is not lossless by construction |
| (C) Leave upstream's entries in git history only | Cheapest | 118 entries stop being greppable in the tree; not the S175 rule ("interleave") |

### D3 — `check-ledger --all` finds one thing in the fork's frozen shards

Upstream's new gate runs `bin/check-ledger --all` (max 0). On the fork's tree it reports **1 finding**:
`docs/archive/CHANGELOG-through-2026-08-11.md:609`, "2 source tags (want exactly one of …)" — a historical
entry whose heading carries two tags. The shard is proof-locked: editing the line breaks its `.verify.sh`
(L3). Both a suite row (the last assertion of upstream's Test 31, `check-ledger --all` over this repository's own ledger; **Test 50 after renumbering**: the fork's own Test 31 is a `model-report` test) and two gates (`check-ledger`, `tests-sh-failed`)
read it, so the merge cannot be green without a decision. The live ledger and the folded one pass.

| Option | What it does | Cost |
|---|---|---|
| **(A) Recommended — scope to the live ledger** | The gate command becomes `bin/check-ledger` (no `--all`) and that assertion in upstream's Test 31 (Test 50) follows; a `_fork_*` note in `.quality-gates.json` says why | One command and one assertion differ from upstream's; later shards are not shape-checked by this gate (the trimmer's proof covers their losslessness, and their entries were checked while live) |
| (B) Patch the fork's `bin/check-ledger` to skip a finding inside a shard that has a `.verify.sh` | Keeps `--all` | A fork-side change to a tool upstream ships; a standing divergence |
| (C) Do not adopt the gate | | The Test 50 assertion stays red unless it is changed anyway; the arriving gate is dropped |
| (D) Edit the shard | | Voids its proof; rejected |

### D4 — Adopt the never-edit hook gate

**(A) Recommended — adopt as shipped.** It enforces a rule the fork already has (`FRAMEWORK_APPARATUS.md:445`);
sessions append a "Correction" entry instead of editing a committed one. (B) Strip the lifecycle block from the
merged hook: a permanent fork-only divergence in a file upstream ships, and the rule goes unenforced.

### D5 — The dashboard's version

**(A) Recommended — 2.20.0**, the next MINOR above the fork's 2.19.0: the distributed file changes
(255,019 → 255,770 B; dotfiles categorized as config, `.gitattributes` recognized), and a changed output on a
distributed tool is MINOR (the 2.19.0 comment, `starter-kit/methodology_dashboard.py:92`, S230). Both pins in the test file follow. Upstream's own line continues from 2.11.3,
so the two stay apart until a dashboard PR reconciles them — recorded, not solved (as S175's D3). (B) 2.19.1.

### D6 — The version the fork's text states

**(A) Recommended.** `CLAUDE.md:145` says v3.7 although fork `main` has contained v3.8 since S177 and will contain
v4.1's text after this merge. State **v4.1** (upstream's documented version; v4.2 is tagged but its docs are #92)
and append **v3.8, v4.0 and v4.1** to `docs/RELEASE_HISTORY.md` verbatim from `upstream/main:CLAUDE.md:118,120,122`
(and v4.2 if #92 has merged). This is a documentation correction, **not a fork release or tag** ("not every
merge is a release"). (B) Leave the line at v3.7 and the history unextended: the fork's text then misstates its
own content.

### D7 — BL-96's uncounted skip

Test 9's guard is replaced by this merge (`git ls-remote` reachability); its else-arm stays a bare
`echo "  SKIP: …"` that the summary's skip count never sees (`bin/tests.sh:141` on main). **(A) Recommended — count
it:** use the `skip` helper at the merged line, one line, and close BL-96. (B) Leave it.

## 4. What this plan deliberately does not do

- **Nothing outward.** No push, PR, comment, tag or release; no action on #92, #93 or #94 (D6 and §1 describe
  their effect, they do not act on them).
- **No adopter sync.** R2 measures the impact (§2.7) into a scratch project and stops.
- **No change to `.context-budget.json`'s ceilings** (D11), to `starter-kit/methodology_trim.py` (clean) or to
  the learnings split (D1 of S175).
- **No BL-94, BL-91, BL-79 or BL-90 work.**
- **No edit to a frozen shard** and no renaming of one.

## 5. Phases — each one session, each closing at its own STOP

### R1 — the merge, the resolutions and the fix-ups

1. **Pre-flight.** Clean tree; `ls .git/REBASE_HEAD` absent; `git fetch upstream`; re-derive §2.1 and §2.3
   (`git merge-base main upstream/main`, `git merge-tree --write-tree --name-only main upstream/main`); read
   `gh pr view 92` and `gh pr view 94` (`--repo KJ5HST/methodology --json state,mergedAt`) and apply §1's table;
   if the conflict set differs from §2.3's 17, add or change rows **before** merging. `HANDOFFS.md`'s owed trim
   and the claim run first, as in any session. Create a local backup ref (`git branch pre-resync-2026-10 main`);
   it is not pushed.
2. **Merge.** `git merge --no-ff --no-commit upstream/main`. Resolve the 17 files per §2.3 — the mechanical ones
   with `git checkout --ours|--theirs` and §2.3's hunk letters, re-reading each file before editing it. **The
   ledgers come from the fold script, which reads the fork's side from git and so needs no restore-ours step and is
   correct amid the conflict markers:** `python3 docs/planning/upstream-resync-2026-10-evidence/fold-ledger.py
   changelog` and `… handoffs` (each prints whether its figures match §2.4's — 118 folded, 386 entries, 415,398 B;
   17 arriving, 20 receipts, 114,995 B — and says plainly if they differ), then `git checkout --ours --
   docs/archive/CHANGELOG-through-2026-09-30.md` (the fork's shard, byte-identical; upstream's is dropped).
   Renumber upstream's Tests 27–34 and fix the four textual references (§2.3 row 12). `git ls-files -u` empty;
   `git add`; `git commit`. The message names the 17 files, the 7 headings whose fork copy was kept, and D1–D7's
   outcomes. **Check at once:** `git diff HEAD^1 HEAD -- docs/archive/CHANGELOG-through-2026-09-30.md` is empty and
   `bash docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh` exits 0 (the shard proof, in the merged history).
3. **Fix-ups**, each commit ≤5 files with its own ledger entry (hooks live, so the never-edit gate binds from the
   first one): **F1** `tools/test_methodology_dashboard.py` population guard 6 → 7 and the version pins,
   both dashboard twins' `.gitattributes` row and version bump (D5), `starter-kit/BOOTSTRAP.md`'s row — four
   files; **F2** the gates per D3 (`.quality-gates.json`, and `bin/tests.sh`'s Test 50 real-ledger assertion if (A));
   **F3** `CLAUDE.md` (the two rows of §2.3 row 6, 29, the version line), `docs/RELEASE_HISTORY.md` (D6: the v3.8, v4.0 and
   v4.1 bullets lifted verbatim from `upstream/main:CLAUDE.md:118,120,122`), the ledger entry that records the
   merge; **F4** BL-96's count (D7) and its closure in the backlog files.
4. **Verify in a `--no-local` clone of the tip** (a clone sees only committed history).

**DONE:** `git merge-base --is-ancestor <target> main` exits 0 and `git rev-list --count main..<target>` = 0;
`git ls-files -u` empty; `bash bin/tests.sh` in the clone exits 0 with `0 failed` — **trial: 451 passed at
three receipts, 1 failed before D3**; `python3 starter-kit/quality_ratchet.py --run` in the clone passes all 13
gates and its summary line is in the receipt (the D9 lint); `bin/check-links`, `bin/check-learnings`,
`bin/check-ledger [--all per D3]`, `bin/check-handoff --all --allow-pending`, `.githooks/pre-commit --selftest`
and `.githooks/commit-msg --selftest` each exit 0; the dashboard twins `cmp` equal; `git diff upstream/main main`
over §2.2's 22 upstream-only paths is empty; `context_budget.py --status` rows diffed against Phase 0, every
flip explained (the trial changed none); `grep -c '^| 29 |' starter-kit/SESSION_RUNNER.md` = 1 and `CLAUDE.md`
says 29; `git grep -nE '(^|[^0-9])28 (known )?failure modes' -- . ':!CHANGELOG.md' ':!HANDOFFS.md' ':!docs/archive' ':!docs/planning' ':!docs/RELEASE_HISTORY.md' ':!README.md'` returns only `starter-kit/FRAMEWORK_LEARNINGS.md:47` (a historical row; trial);
`grep -o '^echo "== Test [0-9]*' bin/tests.sh | sort | uniq -d` is empty (no number twice) and Tests 46–53 exist; the merge commit's shard proof and its empty shard diff (step 2).

**Surface:** this machine, the suite and the gate run in a `--no-local` clone whose path has no session
transcripts. **What it cannot show:** the adopters' view (R2 measures the file set, not an adopter's project),
CI (none), upstream's acceptance. **What the trial did not exercise:** commits with hooks live (the scratch
clone ran with `core.hooksPath` off; only the hook's selftests ran), so the never-edit gate's effect on the
real fix-up commits is first seen here.

**Boundary:** one session. STOP.

### R2 — the ledger trims, the floors and the adopter measurement

1. **Trim `CHANGELOG.md`** (its own commit): dry run `python3 starter-kit/methodology_trim.py --file CHANGELOG.md
   --cut <K> --force` — the trial's `K = 280` archived 106 records to `CHANGELOG-through-2026-09-29.md`; re-derive
   `K` at the real merge result — then `--write`, commit, and run **the new shard's proof by name from a
   `--no-local` clone** (exit 0, L1/L2/L3).
2. **Trim `HANDOFFS.md`**: `--cut 2 --force`, dry run first (trial: 18 of 20 to
   `HANDOFFS-through-2026-10-05-5.md`), `--write`, commit, proof by name from a clone, then the pointer block
   folded into `docs/HANDOFFS_ARCHIVE_INDEX.md` in its **own** commit (fork learning #58).
3. **Re-measure the floors at the state every close-out leaves** (two receipts) and tighten
   `tests-sh-passed` and `dashboard-unit-tests` to the measured values in their own commit (never loosen; fork
   learning #70). `bash bin/tests.sh > file` first: the ratchet keeps no output.
4. **Adopter measurement:** `bin/sync --source=local` into a scratch project; compare the tree to §2.7's list
   (16 of 30 changed, one new seed). Nothing is synced to a real adopter.
5. The report asks for the push go-ahead: `git rev-list --left-right --count origin/main...main` read back
   after a push, each push his go-ahead.

**DONE:** both new shards' `.verify.sh` exit 0 by name from a `--no-local` clone; `methodology_trim.py --file
CHANGELOG.md --check` and `HANDOFFS.md --check` reported (the first may still fire; it is a reported series);
`bin/tests.sh` and `quality_ratchet.py --run` green in a clone at the final tip; the measured adopter set equals
§2.7 or the difference is explained; the `HANDOFFS.md` front-matter sentence (`:26`–`:27`) is true again — no upstream receipt is live; **BL-95 is closed** in the backlog files (its index row out of `BACKLOG.md`, its id on the closed-ids list, a `BACKLOG-COMPLETED.md` row: two edits, or the C6 check goes red) and BL-96 with it if D7 is (A). **Surface and limits:** as R1. **Boundary:** one session. STOP.

## 6. The trial — what was run, and how it differs from a resolved merge

A scratch clone (`git clone --no-local`, `core.hooksPath` off) of `f203159`, `git merge --no-ff --no-commit`
of `upstream/main`, with these crude resolutions: ours for `.context-budget*`, `CHANGELOG.md`, `HANDOFFS.md`,
`bin/check-learnings`, and the shard; theirs for `bin/status`, `bin/sync`, `BOOTSTRAP.md`; hunk letters as in
§2.3 for the hook, the gates, `README.md`, `bin/tests.sh` and the dashboards; `CLAUDE.md` ours with "29"; the
`.gitattributes` row ported into both twins; then three corrections the suite itself demanded (the population
guard, the BOOTSTRAP row, Test 26's tail moved ahead of Tests 42–45). **The trial did not renumber** upstream's tests:
its log has headers 26 and 28–34 twice, so every suite-row name the trial reports is upstream's number. The ledgers were then folded in a second
clone (the script, in its first, working-tree-reading form, whose output the final form reproduces byte for byte), the
suite was run on that tree (suite 4), and the two trims were dry-run.

| Run | Result | What it showed |
|---|---|---|
| suite 1 | 447 / 5 | the BOOTSTRAP row (real); the real-ledger row (real, D3); three `sync:` rows at exit 127 (the `bl54_sync` lines kept) |
| suite 2 | 448 / 4 | the same three rows after the `bl54_sync` lines were removed: **the order** — the fork's closing `rm -rf "$M" "$P"` still stood ahead of upstream's `mh_sync` calls |
| suite 3 | **451 / 1** | the one real-ledger row (the fork's own ledgers) |
| suite 4 | **451 / 1** | the same row, **with both ledgers folded** (20 receipts live, so Test 34's six rows are assertions, not skips); saved as `…-evidence/trial-suite.log` |
| gates | **11 / 13** | `tests-sh-failed` and `check-ledger`, the same finding; saved as `…-evidence/trial-gates.log` |
| units | dashboard 353 (1 red before the guard), trimmer 181, context budget 148, ratchet 45, close-out report 68 | |

**Not the plan's resolutions:** `CLAUDE.md`, the dashboard version, the renumbering and the RELEASE_HISTORY lifts were not
done; both trims ran only as dry runs; no commit in the trial ran with hooks live.

## 7. Self-review — measured, predicted, not run

**Measured at S269:** the merge base and every count in §2.1; the path sets; all 69 stage sets; the 17-file
conflict set and its hunk counts; the three suite runs, the gate run, and the five unit suites in the trial;
every checker named in §2.3; the 118 absent entries and their bytes, the 7 differing duplicates, the one
shard-sourced link, the fold script's byte-for-byte reproduction of the trial ledgers, in both modes, inside a real
conflicted merge; the suite on the tree with both ledgers folded; both ledger dry runs; the proof
of the fork's shard in the merged history; the 17 arriving receipts through the fork's checker and the merged
20-receipt ledger through it; the adopter set (16 of 30); the loss in `bin/status` and `bin/sync` by line
comparison; the #92 and #94 conflict sets.

**Predicted, to re-derive:** every conflict set against a *staged* result (§2.1's caveat); K for the CHANGELOG
trim at the real merge result; the exact suite count at two receipts (the trial ran at three, so the six
Test 34 rows were not skips); the effect of the never-edit gate on R1's own commits; whether #92 or #94 will
have merged by then.

**Not run:** the real resolutions of `CLAUDE.md`, the dashboards' version bump and the RELEASE_HISTORY lifts; the
renumbering and its four reference fixes; D7's `skip` edit; either trim with `--write`; the ratchet at two
receipts; any commit with hooks live in the trial.

**Process note (honest):** the Planning Sessions checklist's first box — the deepest available reasoning mode
set at session start — was **not** satisfied: this session ran at the default effort, and no command to raise it
was available from inside the session. The plan compensates with measurement rather than argument; an
independent read-only review of this text against the repository was run before the close-out (§8).

## 8. The independent review, and what it changed

A read-only subagent re-derived about 215 claims of the frozen draft against the repository (174 tool calls, about
25 minutes; told not to run the suite or touch the tree). It reported **14 wrong, 10 imprecise and 6 omissions**.
Its report is a work product, so each substantive finding was re-run before any edit; every one below was
confirmed. The topology, the 17-file conflict set and its hunk counts, the stage table, the line citations, the
ledger and receipt counts, the shard and proof facts, both dry runs, the gate tables, the adopter set and the
#92 and #94 conflict sets all verified exactly.

| Finding | Severity | What changed |
|---|---|---|
| The first `fold-ledger.py` read the working tree: in a plain `git merge`, with conflict markers in `CHANGELOG.md` and upstream's shard in the tree, it **folded nothing and printed a plausible result**; run after only `CHANGELOG.md` was restored it folded 72, not 118 | **high** | the script reads the fork's side from git (`--fork-ref`), covers `HANDOFFS.md` too, and prints whether its figures match the plan's; re-verified byte for byte in a real conflicted merge (§2.4, §5 R1 step 2) |
| the trial did not renumber upstream's tests, so "Test 31" and "Tests 32, 34" were upstream's numbers; after the plan's renumbering they are 50, 51 and 53 (Test 28, the BOOTSTRAP pin, is the fork's own and keeps its number) | substantive | §2.2, §2.5, §2.6, D3 and R1 F2 name both numbers; §6 says the trial did not renumber |
| four textual references to renumbered tests (`bin/_manifest.py:35`, `bin/tests.sh` comments) | substantive | listed in §2.3 row 12 with the inventory command |
| the fork's retained closing `rm -rf "$M" "$P"`, not Test 45, cleared `$P` before upstream's tail ran | substantive (cause only) | §2.3 row 12, §6 |
| the never-edit gate's remedy for an `--amend` is soft-reset and recommit (S267), not `--no-verify` | substantive | §2.5 |
| the fork has no Test 27 (removed at S178); seven numbers collide, not eight | imprecise | §2.3 row 12 |
| entry-text sums quoted beside file sizes; the receipt sizes in KB; the "S13–S23 archived" count (21 are held, S1–S23 less S4 and S6; 3 differ) | imprecise | §2.4 |
| "six lines" the #94 branch rewords is seven lines in six hunks; `.quality-gates.json` conflicts in 4 hunks if #94 merges first | imprecise | §1 |
| `CLAUDE.md` row 6(a) named sibling rows the fork's file does not have | unsupported | §2.3 row 6 |
| line-loss figures counted blank lines (57 and 74 non-blank) | imprecise | §2.3 rows 10–11 |
| the MINOR rule's source, the 29-paths heading, the first-parent merge count, a `Test 41` provenance loss, BOOTSTRAP's dropped migration sentences, the stale front-matter sentence | minor | §3 D5, §2.2, §2.1, §2.3 rows 12 and 14, §2.4 |
| no step closes BL-95; the stage table and runs 1–2 were not in the evidence directory | omission | R2's DONE; `stages.tsv` added; runs 1–2 are described, run 4 is saved |

**One finding was the reviewer's mistake of fact, not the plan's:** it called the 365 / 0 / 0 figure unverified;
it was measured at this session's Phase 0 (a lone suite run, and again inside the gate run), which §0 now says.
**The review did not cover** anything it was told not to run: the suite, the gates, a trim with `--write`.
