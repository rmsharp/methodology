# BL-101 P10 — the expand stage: the sha adopters may sync from (S283, 2026-10-08)

Plan: [`methodology-subdirectory-plan.md`](../methodology-subdirectory-plan.md) §7 row P10, §5A.2 rule 5, D7, D8.
**Nothing in this record was sent, tagged, pushed or commented upstream.** #94, #92 and #93 are unchanged and without a
maintainer reply. D8, the release number and any tag are the operator's; §5 lists them.

## 1. The sha

**`add55f1`** (2026-10-08, S282, "two BOOTSTRAP statements that read as universal now say they describe the legacy layout")
is the last commit that changed any of the 30 distributed sources, or anything under `bin/`, `tools/`, `starter-kit/` or
`.githooks/`. Every later commit changes ledgers, receipts, gate floors, the plan, the backlog and evidence only:
`git diff --stat add55f1 <any later sha> -- bin tools starter-kit .githooks` is empty (checked at `aa1f1b4`, this session's claim).
So a checkout at `add55f1` **or any later commit for which that command prints nothing** gives an adopter the same files. A
session that syncs an adopter (P11-P22) names the sha it synced from in its receipt (§5A.2 rule 5).

`bin/sync --source=local` copies from the **working tree** of the checkout it lives in, so sync from a clean one
(`git status --short` empty); uncommitted edits to `starter-kit/` would travel.

## 2. What was measured at that sha

| Criterion | Command | Result |
|---|---|---|
| The suite (§3.1) | `bash bin/tests.sh`, clean `--no-local` clone of `05a42a0` (same code as `add55f1`) | **477 passed, 0 failed, 6 skipped** at two receipts (the six are the stated two-receipt skips); Test 40 666 = 666. S282 measured **483 / 0 / 0** at three receipts |
| The gates | `quality_ratchet.py --run` (S282, on `8e214c5`, same code) | 18/18 pass, 0 unmeasured, results `5f5bd400b633`, manifest `a58181b6d58b` |
| Links, C14 | `bin/check-links --layout legacy`, `new`, `both` | exit 0 in each; 80 links in 23 files |
| Sync in both layouts, §5A.3 | `p10-sync-hybrid.sh add55f1` (below) | **ALL CHECKS HELD**: 12 adopters, status, `sync --dry-run` and `check-links --tree` identical to P6's tools in 12/12; five adopters moved to the new destinations agree with the old tools' reading (`nprcgenekeepr` is refused alike by both); the 11 checks of the scratch portfolio (legacy, migrated, half-migrated, empty; `--source=github`) |
| An adopter that only syncs | `p10-sync-12-adopters.py --base 078a6cc --cand add55f1` | §3 |

**`sync-in-both-layouts.sh` run as it stands reads RED at the candidate: "25 CHECK(S) FAILED"** (`p10-sync-in-both-layouts-at-candidate.txt`).
All 25 are parts A and B, and every difference is "N versions behind" or "would write" against the OLD tools. Cause: that script's
two sides each read their own checkout's documents, and P9 changed documents after the script was recorded (P6, `b44b654`). It is a
snapshot, not a gate. To prove the cause, `p10-sync-hybrid.sh` builds the candidate's files with P6's tools (`bin/sync`,
`bin/status`, `bin/check-links`, `bin/_manifest.py` of `7f7f74f`) and runs the same script there: **0 differences, exit 0**
(`p10-sync-in-both-layouts-hybrid-output.txt`). The gate that keeps these tools honest is `sync-layout-unit-tests`
(`tools/test_sync_layouts.py`), not the shell script.

## 3. The expand stage on an adopter that only syncs (12 adopters, in `--no-local` clones)

For each adopter, two clones of its committed HEAD: one synced by `bin/sync` of the **base** `078a6cc` (the commit before the first
BL-101 commit), one by `bin/sync` of `add55f1`, each as an adopter types it (`--force` only if the sync refused). The two trees are then
compared, so what differs is the expand stage and nothing older. Between the base and `add55f1`, **20 commits touched a distributed
source and all 20 are BL-101**: no other change is mixed in. Rows: `p10-adopter-runs/rows.json`, `summary.md`.

- **Paths: identical in 12 of 12.** No file added, removed or renamed; nothing under `methodology/`; `bin/status` reads layout
  `legacy` and 23 of 23 TRACKED files `current` in every candidate-synced tree.
- **Content: 19 files differ** in ten adopters (+1,016 −322 lines): `BOOTSTRAP.md`, `CLAUDE_TEMPLATE.md`, `RECOMMENDED_SKILLS.md`,
  `SAFEGUARDS.md`, `SESSION_RUNNER.md`, `context_budget.py`, `methodology_dashboard.py`, `methodology_trim.py`, `quality_ratchet.py`, and
  ten framework documents under `docs/methodology/`. `feedback-loop-comparison` differs in 20 and `claude_work` in 21: those adopters have no `HANDOFFS.md` (`claude_work` no `CHANGELOG.md`
  either), so each sync writes the seed, and the two seeds differ by one link edit.
- **Health: identical before and after in 12 of 12.** `check-links --tree` exit codes identical in 12 of 12
  (`feedback-loop-comparison` reads exit 1 in both: not from this stage).
- **The adopter's own ratchet line: identical in 12 of 12, but meaningful for four.** Eight declare no gates (`0/0`). Of the four:
  `Philippians` and `airqino` 2/2 pass, `vscode_quarto_ext` 2 fail and `nprcgenekeepr` 1 unmeasured, each the same in both trees.
- **`--force` was needed in two adopters** (`nprcgenekeepr`, `feedback-loop-comparison`), in the base tree and the candidate tree alike. It
  overwrites a tracked file that shows local edits; that is the adopter's own session to read, not this stage's effect.

**Controls (the verdict can fail, and does not on noise).** Candidate = base: 0 files differ and paths identical, but the verdict reads
CHECK ROW, because the base's `bin/status` prints no `layout:` line and the verdict will not call an unreadable layout `legacy`
(`p10-adopter-runs/control-candidate-equals-base.json`). `--tamper` moves one file under `methodology/` in the candidate clone: one rename,
paths DIFFER, CHECK ROW (`control-tamper.json`).

## 4. What a pull request carrying the expand stage would be (D8), measured

The 51 files BL-101 touched that an upstream change could carry: 21 distributed sources, 26 files of canonical tools, tests and the hook,
`starter-kit/close_out_report.py`, `.quality-gates.json`, `CLAUDE.md`, `README.md`. The other 28 files BL-101 touched are this fork's plan and
evidence (23), two other documents, `CHANGELOG.md`, `HANDOFFS.md` and `dashboard_history.jsonl`.

| | Files | Lines |
|---|---:|---|
| BL-101 alone (`078a6cc` → `add55f1`) | 51 | +9,915 −661 |
| Fork work in the same files that is **not** BL-101 (`upstream/main` `f34769f` → `078a6cc`) | 20 | +13,079 −758 |
| Everything in those files (`f34769f` → `add55f1`) | 51 | +22,865 −1,290 |

- **It is a port, not a replay.** Of the 110 BL-101 commits in `078a6cc..add55f1`, 81 touch those files; replayed in order onto
  `upstream/main` with `git apply --3way`, **34 apply and 47 fail**, the first at `2ea5d68` (the wiring into `bin/tests.sh`). They fail
  because they sit on fork work upstream lacks: `bin/tests.sh` (48 other commits), `.quality-gates.json`, the trimmer 1.8.0, both dashboards,
  `close_out_report.py`, `check-overhead`, `model-report`.
- **A tree-level merge** (`git merge-tree --write-tree --merge-base=078a6cc upstream/main add55f1`) has 19 conflicting files: 13 in the set
  above (`.quality-gates.json`, `CLAUDE.md`, `bin/check-handoff`, `bin/check-overhead`, `bin/model-report`, `bin/tests.sh`, `BOOTSTRAP.md`,
  `close_out_report.py`, both `methodology_dashboard.py`, `methodology_trim.py`, `tools/test_close_out_report.py`,
  `tools/test_methodology_dashboard.py`) and 6 fork-only documents.
- **Order against the open pull requests.** #94 (+1,641 −23; the trimmer's proof) touches four of the 51 files (`.quality-gates.json`,
  `FRAMEWORK_APPARATUS.md`, `methodology_trim.py`, `tools/test_methodology_trim.py`); #92 (v4.2 notes) touches two (`CLAUDE.md`, `README.md`). Both read
  CLEAN and unreviewed. #94 carries the #93 fix as three commits on `upstream/main`; this fork carries the same work as its own commits (`5270be8` to `3616b5f`;
  `--reverify` is in its trimmer), so a port is built on whichever of #94 and #92 lands first, or carries #94 itself.
- **What "none" costs** is plan §5A.4's: the fork carries the resolver edits over every maintainer change to the same tools; with the
  instance files unmoved there are no ledger conflicts.

**D8 does not gate P11.** Adopters beside this checkout sync from it (`--source=local`, plan §5A.1), ahead of `upstream`. An adopter that
syncs with `--source=github` gets upstream's files, with no expand stage, until a pull request lands.

## 5. Decided by the operator, not here

1. **P11 may start** (one adopter per session, sync first, §5A.2 rule 1). Before each: read that adopter's hooks
   (`git rev-parse --git-path hooks`), its ledger size and its proofs; for `nprcgenekeepr` and `feedback-loop-comparison`, read what `--force` overwrites.
2. **D8:** one ported pull request, and when (§4 gives the order), or none.
3. **The release number and any tag** (D7 left it open; an expand release is a minor one). A tag, a push to `origin` beyond the CHANGELOG-only
   push record, or anything sent to `upstream` is his go-ahead each time.

## 6. Not shown

An adopter's own CI or test suite; uncommitted edits in a real adopter (a clone holds the committed HEAD); `--mode ignore` adopters (none was
identified among the 12); an adopter's own armed hook (the clones commit with hooks off); the next session's Phase 0 in a migrated tree;
whether any adopter reads the new text.

## 7. Reproduce

```
python3 docs/planning/methodology-subdirectory-evidence/p10-sync-12-adopters.py --base 078a6cc --cand add55f1     # §3, about 4 minutes of run time
bash docs/planning/methodology-subdirectory-evidence/p10-sync-hybrid.sh add55f1                                  # §2, a few minutes
```
§4's figures are the `git diff --numstat`, `git apply --3way` and `git merge-tree` commands named there, run in a scratch clone at `f34769f`.
