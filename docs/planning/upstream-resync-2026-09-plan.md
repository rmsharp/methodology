# Resync plan — merge `upstream/main` `6b29d3d` into fork `main`

**Status: RATIFIED; R1 DONE AT S176 (§7), R2 NEXT — the operator chose every recommendation, D1 (A), D2 (a), D3 (a), D4 (a), by
picker after S175's close-out (2026-09-16).** Written at S175, a planning session: nothing is merged. Evidence taken at fork `main` `1f34e75`, `upstream/main` `6b29d3d`, and PR #83's head
`219fb9d`. Carried out by **R1** and **R2** (§5), one session each. Precedent: the plan
[`upstream-read-set-budgets-merge-plan.md`](upstream-read-set-budgets-merge-plan.md) (S150), carried
out as merge `213f841` (S151).

## 0. The answer, in one paragraph

Fork `main` is 56 commits behind `upstream/main` (25 first-parent) from merge base `598c459`: PR #81 (a
plan document), PR #80 (the read-set budgets series plus the review fixes F1–F3), PR #82 (the quality
ratchet), the `commit-msg` disclosure hook, and the maintainer's receipts S13–S23. `git merge-tree`
lists **13 conflicting files**. Each one has a resolution rule below (§2.3), most of them mechanical. Four decisions need
the operator (§3): **what happens to the fork's Learnings #15–#66, now that upstream has its own
#15 and #16** (BL-53, decided here per S173); whether fork `main` adopts the ratchet and tightens it to
its own measured values; the dashboard's version after merging two numbering lines; and the session split.
The merge runs in **four stages**, cut where upstream's own commits introduce the conflicts, so no
merge commit resolves more than five newly conflicting files, and the suite runs between stages.

## 1. Target, and what is already decided

| | |
|---|---|
| **Target** | `upstream/main` `6b29d3d`. Merge base `598c459` (PR #79's merge, the last resync's target). |
| **Order** | Operator, S173 (picker): the `HANDOFFS.md` header cut (done, S174), **this resync**, then BL-57's P5 (`changelog-rules-contradictions-plan.md:659`). |
| **BL-53** | Operator, S173: the learnings retirement rule is decided **inside** the resync (`BACKLOG.md:148`). |
| **`.context-budget.json`** | The fork keeps its own root config: D11, ratified at S146 (`pr4-read-set-budgets-plan.md` §4), applied at `213f841`. |
| **Retention** | `HANDOFFS.md` keeps one receipt, trims above two (operator, S172; `HANDOFFS.md:8`). |
| **Plan first** | Operator, S175 (picker): this plan, then a separate execution session, as the previous resync ran. |

**The target moves.** PR #83 (the maintainer's parallel-sessions plan) is open; its head conflicts with
fork `main` in **the same 13 files** (computed), so merging it adds a stage but no new conflicts.
Upstream's next step is the v3.8 release PR (`upstream/main:HANDOFFS.md:18`, S23's `next_steps` (a)),
which per that text edits `CLAUDE.md` and `README.md` — both already conflicting here (a prediction from
upstream's description, not measured). **Rule for the executor: re-derive §2.1 at pre-flight; if
upstream moved, append a stage; do not wait for it.**

## 2. Evidence-based inventory

### 2.1 Where the conflicts come from — the stage boundaries

Computed with `git merge-tree --write-tree --name-only main <c>` for each first-parent commit of
`598c459..upstream/main`, and for each commit on PR #82's branch, against fork `main` `1f34e75`:

| Stage | Merge target | Newly conflicting files | What it brings |
|---|---|---|---|
| **M1** | `0fd003a` | `.context-budget.json`, `CHANGELOG.md`, `HANDOFFS.md`, `starter-kit/FRAMEWORK_LEARNINGS.md` | PR #81, receipts S13–S19 and S21, `.githooks/commit-msg` (`ad7bd37`), PR #80 (`4d9e271`) |
| **M2** | `cca7941` | both `methodology_dashboard.py` twins, `bin/tests.sh`, `tools/test_methodology_dashboard.py` | PR #82 through P3: the ratchet, its distribution, the dashboard's gates panel |
| **M3** | `64f23bf` | `bin/check-handoff`, `.githooks/pre-commit`, `CLAUDE.md`, `README.md`, `docs/tutorials/T1_setup.md` | PR #82 P4a–P4c and its review fixes; this repository's own `.quality-gates.json` (P4b, `58babe6`) — absent at `cca7941`, so the D9 receipt lint binds from M3 |
| **M4** | `6b29d3d` | none beyond the 13 | S23: the first tightening (`fb81c4b`) and its receipt |

On `main`, the first 16 upstream commits (`db121ce`…`e5e2661`) conflict only in the two ledgers. PR #82's
conflicts arrive in six steps: `727d9ff` (the dashboard twins), `d433739` (+ `tests.sh`),
`cca7941` (+ the dashboard tests), `bae6b05` (+ `check-handoff`), `58babe6` (+ `pre-commit`),
`04044f1` (+ `CLAUDE.md`, `README.md`, `T1_setup.md`).

**A caveat the executor must re-derive, not trust:** each set above is computed against `main`, not
against the previous stage's merge. A file resolved at one stage conflicts again at a later one if
upstream edited it again:

- **At M2, measured** on the trial M1 result (`e856970`, §3 D1): `git merge-tree --write-tree
  --name-only e856970 cca7941` lists `.context-budget.json` and both ledgers again, plus M2's four new
  files. `FRAMEWORK_LEARNINGS.md` does **not** conflict there under D1 (A); under (B) it would, because
  upstream's #15 (`628d218`) is already in `cca7941`.
- **At M3, predicted from the diffs:** both dashboard twins and `tools/test_methodology_dashboard.py`
  again — `ddcbf29` moves `DASHBOARD_VERSION` 2.11.0 → 2.11.1 and its pins, the line D3 resolves on our
  side (`git diff --stat cca7941 64f23bf`: +140 lines per twin, +81 in the test file);
  `.context-budget.json` again (S22 re-measures upstream's config); the ledgers. Upstream's #16
  (`5c9d3b4`) arrives here.
- **At M4:** `64f23bf..6b29d3d` touches only `.quality-gates.json` (which the fork never edits) and the
  two ledgers.

Before each stage run `git merge-tree --write-tree --name-only HEAD <target>`.

### 2.2 The 20 paths that merge without conflict

Upstream changed 33 paths since `598c459`: the 13 conflicting ones, **6 the fork also changed**, and
**14 the fork never touched**, which arrive as upstream wrote them.

**Changed on both sides, merged cleanly by git — each still needs a check of the result:**

| Path | Upstream's change | Check after merge |
|---|---|---|
| `.gitignore` | ignores `.quality-gates-results.json` | present once |
| `bin/_manifest.py` | +2 rows: `quality_ratchet.py` (TRACKED), `quality-gates.json` → `.quality-gates.json` (SEED) | `len(DISTRIBUTION)` = 29 (fork 27, upstream 29, measured) |
| `bin/check-learnings` | rewords the comment that quotes the `#14` callout (fork `:70`) to upstream's shorter callout | the quoted text matches the callout in the learnings file D1 leaves distributed |
| `starter-kit/SESSION_RUNNER.md` | dashboard step wording, a ratchet sentence, an FM #17 clause, one Degradation row (+7/−3 lines) | merged 55,420 B against the fork's 54,363 B (measured on the `merge-tree` result); BL-57's P5 edits this file next |
| `starter-kit/BOOTSTRAP.md` | +17/−1: the ratchet seed step | read the merged step list once; P5 edits this file too |
| `HOW_TO_USE.md` | +2/−2 | `bin/check-links` |

**Upstream-only (fork untouched since `598c459`):** `.githooks/commit-msg` (new),
`.quality-gates.json` (new), `ITERATIVE_METHODOLOGY.md`, `docs/planning/quality-ratchet-plan.md` (new),
`starter-kit/HANDOFFS.md`, `starter-kit/SAFEGUARDS.md`, `starter-kit/context_budget.py`,
`starter-kit/quality-gates.json` (new), `starter-kit/quality_ratchet.py` (new),
`tools/test_context_budget.py`, `tools/test_methodology_trim.py`, `tools/test_quality_ratchet.py`
(new), `workstreams/AUDIT_WORKSTREAM.md`, `workstreams/DEVELOPMENT_WORKSTREAM.md`. After R2,
`git diff upstream/main main` over the 13 of these other than `.quality-gates.json` must be empty;
`.quality-gates.json` differs only by D2's tightening.

**What the arriving files change about working on fork `main`** — none is a conflict, all are
behaviour:

- **`.githooks/commit-msg`** is live in this clone (`core.hooksPath` is `.githooks`). Under an agent
  harness it refuses a commit whose message has no `Co-Authored-By:` trailer. The fork's commits carry
  one; `--selftest` becomes a gate. **It also refuses a fork test's own fixture commit** (§3 D1's
  trial, failure 3) — measured, and fixed in R1 whatever D1 decides.
- **`.githooks/pre-commit`**, once M3 resolves it, runs `quality_ratchet.py --precommit` first: a
  commit that loosens or removes a declared gate is refused. Merge commits skip the hook, so the ratchet
  first binds on the first ordinary commit after M3.
- **`bin/check-handoff`** gains upstream's D9 lint (`validate_gate_citation`): once `.quality-gates.json`
  declares gates, the newest receipt — `blocks[0]`, and only when it reads `status: complete` — must
  quote a `quality_ratchet: N/M pass` summary line; it never looks past a pending stub
  (`upstream/main:bin/check-handoff:341`, `:411`–`:414`, `:425`–`:426`). **Every fork close-out from R2
  on runs `quality_ratchet.py --run`** (predicted at `pr82-review.md:363`).
- **`starter-kit/SAFEGUARDS.md` becomes 17,024 B** against the fork's no-growth pin of 15,386 B
  (`.context-budget.json:105`): `context_budget.py --status`, already exit 2, gains an `over` row. D11
  keeps the fork's ceilings; this plan records the flip and does not raise anything.

### 2.3 The 13 conflicting paths — resolution and verification

Hunk shapes were measured on the `diff3` merge result: 4 hunks are insertions on both sides at one point; every other
hunk edits the same base lines on both sides.

| # | Path | Stage | What each side did | Resolution | Verify |
|---|---|---|---|---|---|
| 1 | `.context-budget.json` | M1, M2 (measured), M3 (predicted) | 3 hunks. Fork: its own calibrated root config. Upstream: its tree's config — token ceilings for `CLAUDE.md` (23,483 at 2.519 B/tok), the runner (18,900) and `SAFEGUARDS.md` (6,100), measured on upstream's blobs (upstream's `CLAUDE.md` is 59,153 B; the fork's is 11,368 B). | **Keep ours** (D11). | `git diff HEAD -- .context-budget.json` empty; `context_budget.py --status` rows diffed against the pre-merge snapshot, every flip explained. |
| 2 | `.githooks/pre-commit` | M3 | Fork: `--no-renames` on the staged-path listing, with its comment. Upstream: the ratchet block, inserted before the same line. | **Both:** upstream's ratchet block, then the fork's comment and `--no-renames` line. | `grep -c quality_ratchet.py` ≥ 1, and the fork's command line `staged=$(git diff --cached --name-only --no-renames)` present exactly once (the fork's hook has three `--no-renames` lines, `:31`, `:39`, `:83`, and upstream's block adds none); upstream's *"its ledger hook must chain the ratchet"* check and the fork's rename test both pass. |
| 3 | `CHANGELOG.md` | every | Fork: its own ledger. Upstream: 15 entries. | **Interleave** — §2.4. | §2.4. |
| 4 | `CLAUDE.md` | M3 | 3 hunks. Fork: its own file (S130 wording, long tool rows). Upstream: shortened rows written to upstream's token pin, plus rows for the trimmer, `context_budget.py` and `quality_ratchet.py`. | **Keep ours** for both wording hunks. **Add**, in the fork's register, starter-kit rows for `context_budget.py` and `quality_ratchet.py` (the fork's file names neither: `grep -c` = 0) and a Tools row for `tools/test_context_budget.py` and `tools/test_quality_ratchet.py`. Not distributed. | `grep -c quality_ratchet.py CLAUDE.md` ≥ 1; `bin/check-links` exit 0; size against the resident ceiling (18,600 B). |
| 5 | `HANDOFFS.md` | every | Fork: 2 live receipts after S175's trim. Upstream: 11 receipts, S23…S13. | **Interleave, then retention** — §2.4. The front matter stays the fork's. | §2.4. |
| 6 | `README.md` | M3 | 4 hunks, all lists: upstream's name `context_budget.py`, `quality_ratchet.py` and both seeds; the fork's name only the trimmer. | **Take theirs** — a superset. | Every file named as copied is a DEST in the merged `bin/_manifest.py`. |
| 7 | `bin/check-handoff` | M3 | Both inserted at one point. Fork: its block from `:466` (`def leads_with_sha`), 274 lines (answer slots, locator forms, the record budget, the header reserve, `:663`). Upstream: 25 lines (`declared_gate_count`, `validate_gate_citation`). | **Both**, the fork's block first; keep the call sites git merges around them. | `check-handoff --all --allow-pending` exit 0; the suite's check-handoff tests and upstream's D9 test pass. |
| 8 | `bin/tests.sh` | M2, M3 | Both inserted before the summary. Fork: Tests 36–40 (1,018 lines). Upstream: `== Test: quality_ratchet.py ==` (128 lines at M3; its first part at M2). | **Both**, the fork's tests first, then upstream's block at that stage's text. Upstream's gate patterns match the fork's three-count summary — run on this session's output: `== Summary: (\d+) passed` → 300, `== Summary: \d+ passed, (\d+) failed` → 0. | The suite in a clone: exit 0, `0 failed`. |
| 9 | `docs/tutorials/T1_setup.md` | M3 | One sentence listing what `bin/sync` copies; upstream's names the four tools. | **Take theirs.** | As row 6. |
| 10 | `starter-kit/FRAMEWORK_LEARNINGS.md` | M1; under D1 (B) also M2 and M3 | Fork: rows 1–13, reserved `#14`, rows 15–66 (65 rows, `bin/check-learnings`). Upstream: rows 1–13 and `#14` (`d4e1570`), then its own #15 (`628d218`, in `cca7941`) and #16 (`5c9d3b4`, in `64f23bf`). | **Decision D1.** | Per D1. |
| 11 | `starter-kit/methodology_dashboard.py` | M2, M3 (predicted, §2.1) | 3 hunks. (a) `DASHBOARD_VERSION`: 2.17.0 vs 2.11.0 at M2, then vs 2.11.1 at M3 (`ddcbf29`). (b) The fork derives `FRAMEWORK_INSTALLED_SOURCE` from a `_FRAMEWORK_INSTALLED_CONTENT` table; upstream extends the old tuple. (c) The fork removed the 57-line `_FRAMEWORK_FILE_SIGNATURES` dict (`598c459`, lines 468–524) that upstream extends. | (a) **D3.** (b)+(c) **the fork's structure**, adding `quality_ratchet.py` (version pattern `^VERSION = …`, upstream's four signatures) and `.quality-gates.json` (no version pattern, upstream's four signatures) in `bin/_manifest.py` order; drop upstream's dict. Upstream's other +293 lines (`collect_gate_metrics`, `gates_summary_html`, …) do not reference the dict (checked outside the hunks). | The dashboard suite passes, including the manifest-agreement and per-file signature tests; `python3 starter-kit/methodology_dashboard.py` exit 0 and `dashboard.html` shows the gates panel. |
| 12 | `tools/methodology_dashboard.py` | M2, M3 | The twin of row 11. | **Identical to row 11.** | `cmp` the twins. |
| 13 | `tools/test_methodology_dashboard.py` | M2, M3 | 3 hunks: imports (`io` / `hashlib`) and both `DASHBOARD_VERSION` pins. | **Both imports**; pins follow D3. Upstream's per-file signature test does not survive the merge; its dict name remains only in a docstring (`:3117`) and an assertion message (`:3155`) of the merge result — reword both. | As row 11. |

### 2.4 The two ledgers

**The rule** is `HANDOFFS.md:19–24` — separate sequences, never renumbered, each incoming record checked
against ours, and on a shared date the fork's first — applied to `CHANGELOG.md` exactly as
`213f841`'s commit message records, and as the precedent plan's §2.3 steps 1–6 spell out.

- **`CHANGELOG.md`: upstream brings 15 entries, 44,607 B, dated 2026-09-14…16.** None matches a fork
  heading byte for byte (`grep -cxF` per heading: 0 of 15). Four (#80 review F1 step 1, F1 step 2, F2,
  F3) narrate fork-authored commits the fork's ledger records from its own side (S163–S166): **keep
  both**, per precedent step 3. **The merge takes the file over the trimmer's trigger:** 161,989 B live +
  44,607 B ≈ 206,596 B against the 196,608 B Class A threshold, before any resync entry is written. A
  `CHANGELOG.md` trim is owed after the merges — its own commit, and **only after every merge commit is
  recorded in the ledger**, since a trim moves the frontier past anything unrecorded.
- **`HANDOFFS.md`: upstream brings 11 receipts, 63,982 B** (3,693–8,547 B each, all under the
  12,288 B record budget), arriving by stage: **M1** S13–S19 and S21 (8); **M2** S20 as a
  `status: pending` stub; **M3** S20 completed (`e13958d`) and S22; **M4** S23 (read from each target's
  own `HANDOFFS.md`). **They pass the fork's checker:**
  `check-handoff --all` and `--archived` both exit 0 on the 11 alone. All are dated 2026-09-14…16; on
  2026-09-16 the fork's precede them. Then, at each session's end, the retention policy runs: `--cut 2`
  keeps the session's own stub and the newest fork receipt and archives everything below, the arrived
  upstream receipts among them. The pointer block folds into `docs/HANDOFFS_ARCHIVE_INDEX.md` in its own
  commit (the rule at `:51`). The front matter stays the fork's (4,019 B against the 7,168 B reserve).
- **A merge commit has no ledger entry of its own**: the hook skips merges. Record each merge in the
  next ordinary commit's entry (S173's gotcha (3); precedent `9e1dfeb`).

### 2.5 The arriving gates, against the fork's measured values

`upstream/main:.quality-gates.json` declares ten gates. Fork `main` today:

| Gate | Upstream | Fork `main` `1f34e75` | Note |
|---|---|---|---|
| `tests-sh-passed` | min 139 | **300** | a `--no-local` clone, S175 |
| `tests-sh-failed` | max 0 | **0** | the first run gave 1: Test 9 (`bin/sync --source=github`), which passed standalone and on the re-run — it needs GitHub |
| `dashboard-unit-tests` | min 226 | **321** (4 skipped) | live checkout |
| `context-budget-unit-tests` | min 118 | **116**, 1 failure | live checkout: `TestFitGateEndToEnd.test_an_admitting_floor_prints_the_constant` fails; in a clone (no session transcripts for its path) the suite is OK, 2 skipped. Upstream's S24 diagnosed the same test's failure as environmental (a fit on exactly 4 transcripts); the cause here is not measured. The file arrives as upstream's (fork untouched); count after merge not measured |
| `trimmer-unit-tests` | min 123 | **123** (2 skipped) | live checkout |
| `ratchet-unit-tests` | min 45 | absent until M2 | |
| `check-links` | max 0 | exit 0, 105 links | |
| `check-learnings` | max 0 | exit 0, 65 rows | |
| `check-handoff-all` | max 0 | exit 0 | |
| `commit-msg-selftest` | max 0 | absent until M1 | |

**Where to run them:** in a `--no-local` clone. In this checkout's path `bin/tests.sh:267` runs the
context-budget suite, which fails one test here and passes in a clone, so a whole-suite run in this
checkout is expected to read `tests-sh-failed` 1 (not run) and reads 0 in a clone (run).

## 3. Decisions for the operator

**Decided (operator, picker, after S175's close-out):** D1 (A) the fork-only learnings file; D2 (a) tighten
the ratchet to the fork's values; D3 (a) `DASHBOARD_VERSION` 2.18.0; D4 (a) R1 + R2. The options below
stay as the record of what was weighed.

### D1 — The fork's Learnings #15–#66, now that upstream has its own #15 and #16 (BL-53)

**Facts.** Upstream ships rows 1–13 and reserves `#14` — the fork's own answer to #80's review F1
(`d4e1570`; `pr80-reply-f1.md:10`). PR #82 then appended upstream's **#15** (enforce on the artifact,
`628d218`) and **#16** (test a fix in the state the defect leaves, `5c9d3b4`): different lessons under
numbers the fork's rows already hold (`pr82-review.md:369`). Upstream cites its #15 and #16 only in its
ledgers. **After M1**, the fork's live code and config cite fork rows #15+ at 23 sites in 6 files: both
dashboard twins `:452` (#16) and `:2152` (#15); `tools/test_methodology_dashboard.py` (11 sites,
`:3277`–`:5406`); `bin/tests.sh` `:1711`, `:2981`, `:3067`; `.context-budget.json` `:94` (three) and
`:114`; `docs/HANDOFFS_ARCHIVE_INDEX.md:58` (#58). Fork `main` today has eight more, in three files M1
replaces with upstream's versions (`starter-kit/context_budget.py:77`, `:378`, `:409`;
`tools/test_context_budget.py:489`, `:546`, `:563`; `tools/test_methodology_trim.py:1244`, `:2063`;
`git grep` at `0fd003a` finds none). `bin/check-learnings:36` is **not** one: its `Learning
#28/#30/#34` are another project's numbering, quoted as the defect S8 fixed — leave it. Ledgers, plans
and `README.md:461` (a release note) cite more; they are history and stay as written. **The six adopters sync from fork `main`**, so whatever this decides changes what
*"Learning #15"* means in their `FRAMEWORK_LEARNINGS.md` at their next sync — BL-57's P6 sessions.

| Option | What it does | Cost |
|---|---|---|
| **(A) Recommended — the distributed file becomes upstream's; the fork's 52 rows move to a fork-only file** | `starter-kit/FRAMEWORK_LEARNINGS.md` equals upstream's at each stage (rows 1–13 at M1; + upstream's #15 at M2; + #16 at M3). Fork rows 15–66 move **verbatim, numbers kept**, to `docs/FORK_LEARNINGS.md` — not under `docs/archive/`, whose every `*.md` a dashboard test reads as a ledger target (`tools/test_methodology_dashboard.py:4426`). New fork learnings append there. Live code and config citations become *"fork Learning #N"*. | 23 citation sites in 6 live files (two commits by the 5-file cap); **trial below**; `.context-budget.json:81`'s entry re-pointed; a way to keep the fork file's rows checked (`bin/check-learnings` reads a fixed path, `:123`); one line in the fork's `CLAUDE.md` routing its sessions' learnings to the fork file, since the runner's Phase 3C (`starter-kit/SESSION_RUNNER.md:228`) tells a canonical-repo session to append to `FRAMEWORK_LEARNINGS.md`. The fork's distributed corpus then equals upstream's, so the next resync does not collide again. BL-53's question splits: the distributed file's size is upstream's to steward; the fork file is on-demand with its own growth warning. |
| **(B)** Keep the fork's 65 rows distributed; append upstream's #15/#16 as #67/#68 with a provenance note | The fork's adopters keep every row. | The distributed file diverges from upstream permanently; every future upstream learning collides again; reverses `d4e1570` on the fork only; adopters get a table no upstream document describes. |
| **(C)** Take upstream's file; leave the fork's rows in git history only | One pointer line in the fork's `CLAUDE.md`: `git show 1f34e75:starter-kit/FRAMEWORK_LEARNINGS.md`. | Zero live bytes (the budget tool's *Archive* remedy), but the 52 rows are no longer greppable, and new fork learnings still need a home. |

**Trial of (A), run at S175** in a throwaway clone: M1 merged with upstream's learnings file and the
other three conflicts kept ours. `bin/check-learnings`: exit 0, *"13 Learning row(s), contiguous
1..13"*. `bash bin/tests.sh` in that clone: **297 passed / 3 failed / 6 skipped**, against 300 / 0 / 6 at
`1f34e75`. Diffed with digits masked, exactly three rows flipped from pass to fail and nothing else
moved:

1. **Test 18, the dashboard suite — caused by (A), as predicted.**
   `test_the_two_docs_backlog_locations_have_no_protocol_basis` (fork `:5359`) pins Learning #26 as the
   only distributed mention of `docs/planning/BACKLOG.md`; under (A) there is none. Its docstring says
   it is *"SUPPOSED TO GO RED"* when the corpus changes: assert `[]` and reword it.
2. **Test 37's edge row — caused by (A), at M1's state only.** `add_row37` numbers the appended row
   `max + 1` (`bin/tests.sh:2561`) = **14**, the reserved number, so the check reports *"not contiguous
   from 1 — missing #15"* and the exactly-1,500 B row reads as rejected. At M2 upstream's #15 makes it
   16 (predicted from `cca7941`'s rows). Fix the helper to skip reserved numbers rather than wait for M2.
3. **Test 27.N1b — not caused by D1; every option hits it.** M1 brings `.githooks/commit-msg`, and the
   test's real commit `git -C "$P" commit -q -m "claim S2"` (`bin/tests.sh:1281`) carries no
   `Co-Authored-By:` trailer. The suite runs under an agent harness (`CLAUDECODE=1` in this session), so
   the hook refuses it. Fix: the hook's documented override, `METHODOLOGY_REQUIRE_COAUTHOR=0`, on that
   one commit — or a trailer in its message. The exposure is any test that points `core.hooksPath` at
   the live `$METHODOLOGY/.githooks` (`bin/tests.sh:1211`, `:1692`) and makes a real commit without a
   trailer; the mutation harness's copy (`MUTDIR`, `:1530`–`:1538`) holds only `pre-commit`. This run
   found one.

Option (B) needs no trial: at M1 it is `1f34e75`'s own file, which is green today; it then appends
upstream's #15 at M2 and #16 at M3, and conflicts at both. Option (C) removes the same rows (A) removes, so it shares (A)'s failures 1 and 2.

### D2 — Adopt upstream's quality ratchet on fork `main`

- **(a) Recommended:** merge it as upstream ships it, then in R2, after M4, **one commit tightens the
  thresholds to the fork's measured values** (the manifest's own rule: tightening needs no approval;
  loosening is a plan-mode decision in its own commit). From §2.5: `tests-sh-passed` to the fork's count,
  `dashboard-unit-tests` to 321; the others as measured then.
- **(b)** Merge it and keep upstream's thresholds. A floor of 139 on a 300-test suite catches almost
  nothing (`pr82-review.md:365`).
- **(c)** Keep the ratchet off fork `main`. Listed to be rejected: it spans six merged files (the
  manifest, the hook, the suite, the dashboard, `check-handoff`, the runner) and would diverge the fork's
  distributed corpus from upstream's.

### D3 — The dashboard's version after merging two numbering lines

The fork is at 2.17.0; upstream went 2.10.7 → 2.11.0 → 2.11.1 for different changes.

- **(a) Recommended: 2.18.0**, the next MINOR above both, because the merged tool gains upstream's gates
  panel (changed output). Both pins in `tools/test_methodology_dashboard.py` follow.
- **(b) 2.17.1.**

Either way upstream's next dashboard release numbers from 2.11.1, so the two lines stay apart until a
dashboard PR reconciles them upstream. Recorded here, not solved.

### D4 — The session split

- **(a) Recommended:** **R1** = M1 plus D1's follow-through; **R2** = M2–M4 plus D2's tightening.
- **(b)** One session for M1–M4.
- **(c)** One session per stage.

## 4. What this plan deliberately does not do

- **Nothing outward.** No push (each push to `origin` is its own go-ahead), no upstream PR, no comment
  on PR #83, whose proposals are unratified.
- **No adopter sync.** That is BL-57's P6 onward, after P5.
- **BL-57's P5 is not folded in.** Once fork `main` contains `64f23bf`, P5's port may reduce to merging
  `bl57/changelog-rules` directly, since that branch already merged `64f23bf` (`52ad407`) — a prediction
  for P5 to re-derive, not a finding.
- **No ceiling changes** in `.context-budget.json` (D11); the runner's and `SAFEGUARDS.md`'s `over` rows
  are recorded, not remedied.
- **No BL-54, BL-60 or BL-61 work.**

## 5. Phases — each one session, each closing at its own STOP

### R1 — M1: merge `0fd003a`, and carry out D1

1. **Pre-flight:** clean tree; `git fetch upstream`; re-derive §2.1. If `upstream/main` moved or PR #83
   merged, note it and add a final stage to R2.
2. `git merge --no-ff --no-commit 0fd003a`; resolve rows 1, 3, 5, 10; commit the merge.
3. Test 27.N1b's fix (D1's trial, failure 3) — needed under any option, since M1 brings the hook.
   Keep it to the one-line override: BL-57's P5 removes the hook's claim carve-out and Test 27 with it,
   unless the operator keeps them (`changelog-rules-contradictions-plan.md:278`, `:683`).
4. D1's follow-through, each commit at most 5 files with its ledger entry; under (A) that includes the
   two test fixes the trial found (failures 1 and 2).
5. The ledger entry recording the merge; the `HANDOFFS.md` retention trim and fold if above two.

**DONE:** `git merge-base --is-ancestor 0fd003a main` exits 0; `git ls-files -u` is empty; `bash
bin/tests.sh` in a `--no-local` clone at `HEAD` exits 0 with `0 failed`; `bin/check-learnings`,
`bin/check-handoff --all --allow-pending`, `bin/check-links` and `.githooks/commit-msg --selftest` each
exit 0. Under (A): the distributed learnings file is byte-identical to `git show
0fd003a:starter-kit/FRAMEWORK_LEARNINGS.md`, and the fork file's rows are byte-identical to rows 15–66 of
`1f34e75`'s (compared in Python, not by eye).

**Surface:** this machine, the suite in a `--no-local` clone whose path has no session transcripts. Test
9 needs GitHub and failed transiently once at S175: re-run a lone Test 9 failure, never waive it.
**Cannot show:** the adopters' view (P6), CI (none), upstream's.

**Boundary:** one session. STOP.

### R2 — M2–M4: merge `cca7941`, `64f23bf`, `6b29d3d`, and carry out D2 and D3

1. For each stage: re-derive its conflicts against the previous result; resolve per §2.3; commit the
   merge; then run the suite in a `--no-local` clone of that commit (a clone sees only committed
   history, so an uncommitted resolution cannot be tested there). A red result is fixed in its own
   commit before the next stage.
2. D2's tightening commit, carrying the ledger entries for the three merges and for itself, citing
   `quality_ratchet.py --run` from a clone. The first ordinary commit after M3 is the first the ratchet's
   hook checks: its hook run is the proof the ratchet binds in this clone.
3. The `CHANGELOG.md` trim if `methodology_trim.py --file CHANGELOG.md --check` fires (§2.4 predicts
   it will), in its own commit; the `HANDOFFS.md` retention trim and fold.

**DONE:** `git rev-list --count main..upstream/main` = 0 at the re-derived target; the suite in a clone
exits 0 with `0 failed`; `quality_ratchet.py --run` in a clone passes every gate, and its summary line is
in the receipt (the D9 lint demands it); the dashboard twins `cmp` equal; `python3
starter-kit/methodology_dashboard.py` exits 0 and `dashboard.html` shows the gates panel;
`context_budget.py --status` rows diffed against R1's, every flip explained; `git diff upstream/main main`
over §2.2's upstream-only paths is empty except `.quality-gates.json`, whose thresholds differ from
upstream's only in the tightening direction.

**Surface:** as R1. Merge commits skip `.githooks/pre-commit`, so no merge commit is checked by the
ratchet; the first ordinary commit after M3 is. **Cannot show:** as R1.

**Boundary:** one session. STOP. Next: BL-57's P5.

## 6. Self-review — what is measured and what is predicted

**Measured at S175:** every conflict set in §2.1 (against `main`); hunk counts and shapes; the 33-path
split in §2.2; the merged runner and `SAFEGUARDS.md` sizes; manifest rows (27 / 29); the ledger byte
counts and the heading match; the 11 receipts through the fork's checker; the gate values in §2.5; the
regex match on the fork's summary line; the citation sites in D1; the trial of D1 (A); the M2 conflict
set against the trial's M1 result. **A read-only claims review** (an independent subagent, ~150 claims
checked against the repository) found 15 wrong claims in the first draft; each was re-run by the author
and corrected in this text — the M2/M3 re-conflicts, where upstream's #15 and S20 arrive, two DONE
criteria that could not pass as written, the `--no-renames` count, the citation count, and five
citations.

**Predicted, to re-derive:** the M3 and M4 conflict sets against each stage's own result (the §2.1
caveat); the `CHANGELOG.md` trim firing (the arithmetic is measured, the entries the
sessions add are not); the `SAFEGUARDS.md` flip; the context-budget suite's count after the merge; the
v3.8 PR's files; P5's simplification.

**Not run:** any resolution beyond the trial of (A); the suite on a fully merged tree; the ratchet on fork
`main`.

## 7. R1 as carried out (S176, 2026-09-16) — what R2 inherits

**R1 is done:** merge `5c2bd59`, then `8c35872` (Test 27.N1b), `8cfaf0d` (`docs/FORK_LEARNINGS.md`,
`check-learnings --first`), `82f0d3a` (citations, the #26 pin, `add_row37`), `4ef6390` (`CLAUDE.md`
routing), the retention trim `084ba1b` and its fold `28ae585`. Where the result differs from §2–§5, this
section wins:

1. **Suite, each in a `--no-local` clone:** the merge 303 / 3 / 0 (the trial's three failures; 0 skips at
   11 receipts); after D1 (`4ef6390`) 309 / 0 / 0; after the trim and fold (`28ae585`) 303 / 0 / 6, the six being Test 34's stated skips at 2 receipts (a digit-masked row diff against `4ef6390` shows nothing else).
2. **Conflict sets against `28ae585`, computed** with `git merge-tree --write-tree --name-only 28ae585
   <target>`: `cca7941` → 7 files (`.context-budget.json`, `CHANGELOG.md`, `HANDOFFS.md`, `bin/tests.sh`,
   both dashboard twins, `tools/test_methodology_dashboard.py`); `64f23bf` and `6b29d3d` → 12 (those
   plus `.githooks/pre-commit`, `CLAUDE.md`, `README.md`, `bin/check-handoff`,
   `docs/tutorials/T1_setup.md`). `starter-kit/FRAMEWORK_LEARNINGS.md` conflicts at no later stage. Each
   stage still re-derives against the previous stage's committed result (§2.1). **`cca7941` does not contain
   `0fd003a`** (`git merge-base --is-ancestor` exit 1): it is on PR #82's branch, and its `HANDOFFS.md`
   holds S20 as a `pending` stub directly above S19.
3. **`HANDOFFS.md` conflicts at every later stage because R1's retention trim archived S21 and S19–S13**,
   the text upstream's later receipts are inserted against. Against the pre-trim `4ef6390` it merged
   cleanly with `cca7941` and `64f23bf`. The rule is still §2.4, with one addition: keep only the incoming
   receipts that are in neither the live file nor a shard — S20 (a stub at M2, completed at M3), S22 (M3),
   S23 (M4). Never re-add S13–S19 or S21, which are in `docs/archive/HANDOFFS-through-2026-09-16-3.md`.
4. **`CHANGELOG.md` is already over the trimmer's trigger:** `methodology_trim.py --file CHANGELOG.md
   --check` FIRES at 200,985 B on `28ae585`. §2.4's trim (R2 step 3) is owed whatever M2–M4 add, and only
   after every merge commit is recorded.
5. **The citation sites were 26, not D1's 23:** in both twins at `:409` the text `Learning`/`#26` wraps
   across two comment lines, and `HANDOFFS.md`'s fold comment sits in front matter, which is live text,
   not ledger history. All 26 now read *fork Learning #N*. At M1, line numbers in
   `tools/test_methodology_dashboard.py` moved +39 (upstream's F2 test).
6. **`bin/check-learnings` already took `--file`.** What the fork file needed was contiguity from #15:
   `--first N`, wired into Test 32 with a no-flag run and a deleted-row mutant. The change is fork-side, in a file
   upstream ships, but upstream does not touch it after `0fd003a` (`git diff 0fd003a 6b29d3d --
   bin/check-learnings` is empty), so M2–M4 do not conflict there.
7. **`context_budget.py --status`**, rows diffed against Phase 0, exit 2 both times:
   `starter-kit/SAFEGUARDS.md` ok → over, 15,386 → 16,353 B (M1's four upstream lines; §2.2 predicts
   17,024 B at the full merge). The learnings row is re-pointed to `docs/FORK_LEARNINGS.md` (67,177 B, ok,
   under the unchanged 81,920 B warning: 14,743 B of headroom where the table had 2,437 B).
   `HANDOFFS.md` 24,200 → 15,845 B; `CLAUDE.md` 11,368 → 11,808 B.
