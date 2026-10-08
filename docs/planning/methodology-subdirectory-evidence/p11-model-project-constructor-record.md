# BL-101 P11 — the first adopter, `model_project_constructor` (S285, 2026-10-08)

Plan: [`methodology-subdirectory-plan.md`](../methodology-subdirectory-plan.md) §4.6 (two tiers), §7.4 (the per-adopter DONE list), D1, D9.
**Nothing was pushed, sent, tagged or commented, here or in the adopter.** Its three commits are local on `master` (ahead 3 of `origin/master`);
its push is the operator's go-ahead, each time. Raw outputs: [`p11-adopter-runs/`](p11-adopter-runs/).

## 1. What was done in the adopter

| Step | Commit there | Result |
|---|---|---|
| Start | `0dc3051` | clean, `master`, 0 0 with `origin`; hooks path `.githooks`, which holds only a `post-commit` (publishes the wiki when `docs/wiki/model_project_constructor/` changes; none of these commits touched it) |
| `bin/sync`, from this checkout at `ea82c0c` | `63cedc5` | 21 files rewritten, `.gitattributes` created, no `--force`; **its CI green on the exact tree** (§2, S1) |
| `bin/migrate-layout` at `--tier all` (the tool's default) | `972b84f`, **reset away** | the tool's own checks all passed; the adopter's own CI did not (§2, S2). A patch of it was kept in the session's scratch only (not durable); the commit is reproducible with `bin/migrate-layout <clone of 63cedc5> --apply` |
| `bin/migrate-layout --tier 1` | `4399c60` | 23 renames at 100%, `CLAUDE.md` (37 replacements) and `.context-budget.json` (2) rewritten, one ledger entry the tool wrote |
| The adopter's own test, repaired | `ec23bc7` | one constant, `RUNNER` in `tests/test_read_budget.py:67`, its own ledger entry |

The checkout synced from is `ea82c0c`; its distributed files are those of `add55f1` (`git diff --stat add55f1 ea82c0c -- bin tools starter-kit .githooks` lists only
`bin/migrate-layout` and `tools/test_migrate_layout.py`, both canonical-only). The sync's rule "commit one run as one commit, with its own ledger entry" (`BOOTSTRAP.md`) was followed; the adopter's
own rule "every commit carries its entry, tag `[ad hoc]`" put a hand-written entry in each of `63cedc5` and `ec23bc7`, and the tool wrote the third.

## 2. The adopter's own CI, at each state (ruff, mypy, its 13 proofs plain and `--self-test`, `pytest -q`)

| State | ruff / mypy | Proofs (13) | pytest |
|---|---|---|---|
| Recorded by its last session, before the sync | | | 3,942 passed, 9 skipped, 98.34% |
| **S1** the sync, uncommitted tree | 0 / 0 | 13 hold | **3,942 passed, 9 skipped, 98.34%** |
| **S2** `--tier all` (the adopter's own tree, then an identical scratch clone) | 0 / 0 | **2 red** | **32 failed, 9 errors**, 3,875 passed, 35 skipped |
| Scratch clones of `63cedc5`: control / tier 1 / tier all | | 13 / 13 / **11** | 3,942 + 9 skipped / **1 failed**, 3,915 passed, 35 skipped / 32 failed, 9 errors |
| **S4** `--tier 1` + the one constant, the tree that was committed | 0 / 0 | 13 hold | **3,942 passed, 9 skipped, 98.34%** |

The scratch clones used the adopter's own `.venv` interpreter with `--no-cov`; the control reproduced the real tree's counts, and the tier-all clone reproduced S2's.

**What tier 2 breaks here (41 tests, 2 proofs), every one a root path of a file tier 2 moves:**
- `docs/architecture-history/SESSION_NOTES-pointer-collapse.verify.sh:251` and `SESSION_NOTES-pointer-collapse-S254.verify.sh:174` define `LIVE = "SESSION_NOTES.md"`; their live checks print "is not on disk".
- `tests/test_read_budget.py` (7 of the 41: `SESSION_NOTES = "SESSION_NOTES.md"`, `:61`) and `tests/test_session_notes_census.py` (34: `LEDGER = "SESSION_NOTES.md"`, `:138`, and `CLAUDE.md` heading literals at `:340` and `:410` that the tool's rewrite changed).
- The 26 mutant tests in `test_read_budget.py` **skip, not fail, when `test_live` is red** (9 skipped became 35), so a skipped count is part of the criterion.

**What tier 1 breaks: one test.** `RUNNER = "SESSION_RUNNER.md"` (`tests/test_read_budget.py:67`), repaired in `ec23bc7`; nothing else in the suite or the proofs names a file tier 1 moves.

## 3. Why the tool did not show it

`bin/migrate-layout`'s `proofs` cell reads **0 proofs** for this adopter before and after: it runs only the proofs of the ledger shards it moves (`run_checks`, `bin/migrate-layout:732`), and this adopter moves none: its 13 proofs are its own, in
`docs/architecture-history/`, run by its CI job `proofs`. Its `other` hits (2,647 mentions in 73 files at `--tier all`, 1,008 in 55 at tier 1) do not separate code and proofs that name a moved file from prose.
P7's and S284's 12-adopter runs measured the tool's own checks; this is the first run of an adopter's own CI, which P7 listed as not shown.

## 4. Phase 0 in the new layout (the adopter's own relocated runner, tier 1)

Steps 1 to 5 ran from the project root: `methodology/SAFEGUARDS.md` and `methodology/SESSION_RUNNER.md` read where the runner says; `SESSION_NOTES.md` (root, tier 2) has its `## ACTIVE TASK`;
`gh issue list` printed none; `git status` clean, `master` ahead 3; `python3 methodology/methodology_dashboard.py` health **96, risk high, activity active, 0 vulns**, the same health and risk as its last
pre-move snapshot (2026-10-04), so the high flag pre-exists. **A cost of tier 1 alone:** the dashboard run from `methodology/` writes `methodology/dashboard.html` and starts a new
`methodology/dashboard_history.jsonl` (1 snapshot) while the root's 34-snapshot history and `dashboard.html` stay, unused. Step 6, reconcile: the `CHANGELOG.md` frontier is HEAD (0 undocumented);
the `HANDOFFS.md` frontier is `0dc3051`, three commits back, with no receipt for them. They are not a session of that project and I wrote none; its next Phase 0 will report them, and the three ledger
entries say what they are.

## 5. Not shown

An Actions run (nothing pushed); the adopter's wiki hook on a commit that touches `docs/wiki/` (none did); `.claude/settings.local.json` (untracked, ignored) holds permission entries naming
`methodology_dashboard.py`, `SESSION_RUNNER.md` and `SESSION_NOTES.md` at the old paths, which affects prompts only; tier 2 on this adopter (blocked, §6).

## 6. The operator's, and what the tool could do

- **Tier 2 for this adopter** (and the order for P12 to P22): at `--tier all` its repair is two edits to tracked proof scripts that are part of its record, plus the path constants and heading literals in two test files.
  He chose tier 1 now (S285, mid-session picker); tier 2 waits for his go-ahead.
- **A gap in the tool, recorded not built:** its report could list the project's tests, scripts and proofs that name a moved file, apart from prose. Run against these 41 tests and 2 proofs it would have
  named all four files at the dry run. One adopter in twelve is measured; the other eleven are unread for this.
- **Reproduce:** clone the adopter at `63cedc5`, `bin/migrate-layout <clone> --tier 1|all --apply`, then its `.github/workflows/ci.yml` commands with its `.venv` (`ruff check src/ tests/ packages/ scripts/`,
  `mypy`, each `docs/architecture-history/*.verify.sh` plain and `--self-test`, `pytest -q`).
