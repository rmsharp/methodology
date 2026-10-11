# BL-101 P15 — the fifth adopter, `nprcgenekeepr` (S296, 2026-10-11)

Plan: [`methodology-subdirectory-plan.md`](../methodology-subdirectory-plan.md) §3 C5 and C11, §4.6 (two tiers), §7.4 (the per-adopter DONE list), §7.6 (the register is read first). **His pick at S296's Phase 0**, after he asked whether it could run once the adopter was clean and out of a session: "P15 on nprcgenekeepr at tier all". At the check before the claim (`pgrep -x claude` and `lsof -a -p <pid> -d cwd`, and again before the sync and before the apply) no `claude` process had that directory as its cwd; the tree was clean at `3004914aa`.
**Nothing was pushed, tagged or sent upstream.** The adopter has a GitHub remote (`origin`, `rmsharp/nprcgenekeepr`); its `master` was one commit ahead of `origin/master` at the start and is five ahead now, four of them this session's. Raw outputs: [`p15-adopter-runs/`](p15-adopter-runs/); the scripts are [`p15-rehearsal.sh`](p15-rehearsal.sh) (set `SCRATCH`), [`p15-f7-match.py`](p15-f7-match.py) and the R runners [`p15-r-full.R`](p15-r-full.R), [`p15-r-one.R`](p15-r-one.R), [`p15-r-run.sh`](p15-r-run.sh).

## 1. What was done in the adopter

| Step | Commit there | Result |
|---|---|---|
| Start | `3004914aa` | `master`, 1,547 tracked files, an R package (`nprcgenekeepr` 2.0.0.9000): 7 workflows, 391 test files under `tests/testthat` (11,017 tests), `renv`, one declared gate (`tarball_size_clean_export`, at most 5,000,000 B), 57 archived-ledger proofs (47 exit 0, 10 exit 1: the population of upstream issue #93). Framework files in the legacy layout, the manual and workstreams in `docs/methodology/`. **No tracked hook and `core.hooksPath` unset; an untracked `.git/hooks/pre-commit` (238 B, 2026-09-19) runs `context_budget.py` at the root** (§3). Ignored and present at the root: `dashboard.html`, `dashboard_history.jsonl`, `.context-budget-history.jsonl`, `.quality-gates-results.json`; five `git worktree`s under `.claude/worktrees` (older commits, left alone) |
| `bin/sync --force`, from this checkout at `19b9882` | `4f67cb927` | **21 files updated** (10 at the root, 11 under `docs/methodology/`), 2 unchanged, the seeds left as written; its own ledger entry. **`--force` for one file, `methodology_trim.py`** (§2) |
| The per-clone hook rewritten | none (untracked) | `python3 context_budget.py install-hook`: 238 B to 785 B; the old file kept in [`p15-adopter-runs/real-old-hook.sh`](p15-adopter-runs/real-old-hook.sh) (§3) |
| **Nine of the project's own files edited, before the move** | `74804498a` | `.Rbuildignore`, the four push workflows, three tests and one script, +27 −5, valid in both layouts; [`adapter.patch`](p15-adopter-runs/adapter.patch); with its own ledger entry (§4) |
| `bin/migrate-layout --tier all --apply --trailer` | `0e2663642` | 144 files changed: **143 renames** (140 at 100%, `.context-budget.json` 97%, `.quality-gates.json` 98%, `CHANGELOG.md` 98%) and `CLAUDE.md` edited in place (27 replacements, 19,700 B to 20,024 B, ceiling 28,000 B); the two configs' paths rewritten; **4 ignored generated files moved plainly**; the tool's ledger entry; 3 files left in place (`.gitattributes`, `docs/archive/CHANGELOG-legacy-pre-S325.md`, `docs/methodology/README.md`: the project's own or an older copy) |
| The project's own trimmer addition put back | `5a41dbbdd` | the 49 lines the sync's overlay dropped, applied at `methodology/methodology_trim.py` (§2) |

The checkout synced from is `19b9882`; its distributed files are those of `add55f1` (`git diff --stat add55f1 19b9882 -- bin tools starter-kit .githooks ITERATIVE_METHODOLOGY.md FRAMEWORK_APPARATUS.md HOW_TO_USE.md workstreams` lists only `bin/migrate-layout` and `tools/test_migrate_layout.py`, both canonical-only). The trailer is `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`. Ledger entries in the adopter are written in its own format; two of my counts in them were wrong when first written (the sync's file split, the tarball's 146 tar entries against 143 files) and were corrected by amending the same unpushed commits before any later commit.

## 2. What the sync refused, and what the overlay would have dropped (F7, F19)

`bin/sync` refused `methodology_trim.py` ("local modifications that don't match any canonical or historical version") and nothing else ([`ctrl-sync-dry-refusal.txt`](p15-adopter-runs/ctrl-sync-dry-refusal.txt)). Matched by hand against every revision of the file in this repository, both git walks, under `starter-kit/`, the root and `methodology/` ([`p15-f7-match.py`](p15-f7-match.py), [`f7-match-output.txt`](p15-adopter-runs/f7-match-output.txt)): **26 distinct blobs; the nearest is `d7768cbeb`, and the adopter's file is that plus 49 lines and nothing removed** (the next nearest is `22ce71b47`). The 49 lines are the project's own: a `_session_notes_date` helper and a `SESSION_NOTES.md` entry in `LEDGERS`, "LOCAL ADDITION (nprcgenekeepr, S518, 2026-08-11)", whose comment says the next sync overlay will drop it. Its `CLAUDE.md` ("Additional close-out checks") carries the standing instruction to re-apply it after any sync.

**What the overlay does, measured** (the project's trimmer on its own `SESSION_NOTES.md`, 55,096 B, dry run, `--budget-bytes 30000`): with the addition, `would archive 38 of 39 record(s)`; after the forced sync, `[NO_CONFIG] SESSION_NOTES.md has no entry in the config table`, exit 3. So the sync would have silently ended the project's ability to trim that ledger.

**Why it comes back only after the move:** `bin/migrate-layout` refuses a tree where `bin/status` does not read every tracked file `current`, and a file with the addition reads `locally modified`. The order is therefore sync (overlay) → move → re-apply. Re-applied at `methodology/methodology_trim.py` with `patch` (no fuzz): the file differs from canonical `19b9882` by 49 lines added and none removed, the same as before; the dry run plans the same 38 of 39 records, now into `methodology/archive/SESSION_NOTES-through-2026-10-05.md` (L1, L2 and L3 hold), and at the project's own `--budget-bytes 65536` answers `NOTHING_TO_DO`. **The file is `locally modified` again** (`bin/status`: 22 of 23 tracked `current`, this one not), as it was before the session, so the next `bin/sync` refuses it again. Not run: an actual trim (`--write`).

## 3. The hook (F17, F18)

The hook is `.git/hooks/pre-commit`, untracked, `core.hooksPath` unset: `exec python3 "$(git rev-parse --show-toplevel)/context_budget.py" --precommit`. A clone does not inherit it, so each rehearsal arm had it copied in (the real tree's own file, sha256 `209e617bfeed`).

| Arm | Hook | `migrate-layout --apply` | After |
|---|---|---|---|
| `t1`, `tall` | the old one | **exit 3, `ROLLED BACK: git commit was refused: python3: can't open file '.../context_budget.py'`** | HEAD stays at the sync commit, "the project is as it was before the run" ([`old-hook-apply-rolled-back.txt`](p15-adopter-runs/old-hook-apply-rolled-back.txt)) |
| `t1h`, `tallh`, `tallx`, `tallA`, **the real tree** | rewritten by `context_budget.py install-hook` | exit 0 | applied |

- **F18 (the old hook):** the dry run named the file (`.git/hooks/pre-commit:4 ... [not tracked: per clone]`) with a warning that was true, and the apply refused loudly and rolled back. The tool did its job; the rehearsal is what showed the case.
- **F17 (the rewritten hook):** the dry run warns again, on the new hook, `WARNING: 2 hook line(s) run a moved tool: that hook will refuse the migration commit and the run will roll back`, and the apply exits 0 (in four clones and on the real tree). The installer's text loops over `"context_budget.py" "methodology/context_budget.py"` and carries no `# layout: ok -- <reason>` marker, the one F15 made the tool honour.
- **After the move, the rewritten hook still binds** (a fresh clone of the real result with the real hook copied in): a small tracked commit exits 0; a commit that grows `CLAUDE.md` from 20,024 B to 28,502 B (ceiling 28,000 B) is refused (`context-budget: REFUSED`, exit 1, HEAD unmoved), the same as in the unmoved control. **Another clone's hook arming is not shown**, as at P13 and P14: a second clone of this project that pulls the move and still has the old hook will have every commit refused until it runs `python3 methodology/context_budget.py install-hook`.

## 4. What tier all does to an R package, measured (F20)

The adopter's own clean regression read (its `CLAUDE.md`: `Sys.setenv(NOT_CRAN = "true"); pkgload::load_all(); testthat::test_dir(..., reporter = "silent")`) in `--no-local` clones, one at a time, against the project's own `renv` library (a clone is at another path, so `RENV_PATHS_LIBRARY` names the real library's root; nothing installed). Per-file CSVs: [`r-*.csv`](p15-adopter-runs/).

| Arm | Tests | Passed | **Failed** | Error | **Skipped** | Tarball (the project's gate command) |
|---|---:|---:|---:|---:|---:|---:|
| `base`, unsynced | 11,017 | 10,824 | 0 | 0 | 187 | 3,775,455 B |
| `ctrl`, synced | 11,017 | 10,824 | 0 | 0 | 187 | |
| `t1h`, tier 1 | 11,017 | 10,824 | 0 | 0 | 187 | |
| **`tallh`, tier all, as the tool leaves it** | 11,016 | 10,821 | **0** | 0 | **189** | **8,494,054 B** (146 tar entries under `methodology/`) |
| `tallA`, tier all after the nine edits | 11,040 | 10,847 | 0 | 0 | 187 | 3,775,642 B |
| **a fresh clone of the real result `5a41dbbdd`** | 11,040 | 10,847 | 0 | 0 | 187 | 3,775,628 B |

- **Three effects, caught by three different things.** (1) `test_handoffsReceiptPlacement.R` reads `HANDOFFS.md` at the root and skips when it is absent: 10 expectations became 7 passed and 2 skipped (the only per-file difference from `base`). **A rise in skips, the S285 rule, caught this one.** (2) `.Rbuildignore` lists the moved files by name (22 lines, per the tool's pattern rule) and no line covers `methodology/`, so `R CMD build` ships all 143 moved files: **3,775,455 B to 8,494,054 B, past the project's own gate (5,000,000 B)**; no test fails on it; the declared gate does. (3) The four push workflows' identical `paths-ignore` list names the moved files at their old places, so a push that changes only `methodology/` files would start a full CI run; `test_workflowPathsIgnore.R` (218 expectations) and `test_rbuildignore.R` stay green because they pin names, not places. **Nothing run here shows (3);** it is read from the list and the tool's own `ci` row.
- **The nine edits** ([`adapter.patch`](p15-adopter-runs/adapter.patch)), each valid in both layouts: `.Rbuildignore` gains `^methodology$`; `methodology/**` is added to the four workflows' list (each file still parses as YAML, 22 entries, `pull_request` unfiltered); `test_handoffsReceiptPlacement.R` reads `methodology/HANDOFFS.md` when it exists and the root file otherwise; `test_workflowPathsIgnore.R` and `test_rbuildignore.R` pin the new entries (218 to 240 and 3 to 4 expectations); `vignettes/articles/data-raw/build-document1-evidence.R` reads its three ledgers through a one-line `ledger_path()` (a script that fails when run at tier all; **not run**, before or after). The three test files read 4, 10 and 240 passed, 0 skipped, in the real tree before the move and in the clone after it.
- **Tier 1** left every count identical (`t1h`); its tarball and CI filters were not measured.
- **The project's own gate**, run by `quality_ratchet.py --run` in a clone of the result: `1/1 pass · 0 fail · 0 unmeasured`, measured 3.77563e+06 against `<= 5e+06`; results `9493226ce61d`, manifest `aa983075d6a2`. **The dashboard** reads 96/100 and risk 0 before and after.

## 5. The tool's checks, before and after

| Check | Tier 1 (clone `t1h`) | Tier all (real apply) |
|---|---|---|
| `bin/status` tracked `current` | 23/23 → 23/23 | 23/23 → 23/23 |
| `check-ledger` | exit 1 → 1 | exit 1 → 1 (31 findings, the same lines: orphaned trim-pointer text) |
| `check-handoff` | exit 1 → 1 | exit 1 → 1 (14 unreconciled `commit:` slots, the same) |
| `check-links`, framework documents | 0 → 0 | 0 → 0 |
| `check-links`, the project's own files | 0 → **4** | 0 → **110** |
| proofs | 0 → 0 (none moved) | 57, exit histogram `{0: 47, 1: 10}` → the same |
| history by `git log --follow` | 1,850 → 1,851 | 1,851 → 1,852 |
| clean tree after | yes | yes |

- **110 links dangle at tier all** in the project's own ledgers, against 23 at P12, 1 at P13 and 0 at P14; reported, never edited (C6; F9). 108 are the trimmer's pointer blocks naming `docs/archive/` shards (`SESSION_NOTES.md` 46, `HANDOFFS.md` 34, `CHANGELOG.md` 28), links written relative to where the ledger sat; the shards themselves moved with their proofs to `methodology/archive/` (34 + 34 + 46 files, the project's 23 `SESSION_NOTES` shards among them); 2 are the ledger headers' link to `docs/methodology/FRAMEWORK_APPARATUS.md`. The 4 at tier 1 are F13 again, not links (tier 1 was applied in a clone this time).
- **The 10 red proofs are the same 10 before and after:** moving does not change a shard proof's exit code (issue #93's false reds are a separate defect, not this move's).
- **The tool's list read against what broke.** It listed `ci` 4 files (68 mentions), `tests` 10 files (33 mentions; 3 on code lines), `scripts` 2 files (1 on code lines), `config` `.Rbuildignore` (22 lines, none covering the directory) and, in the dry run, the per-clone hook. Every file that broke or would break was on the list; the list does not say which effect each has (F4's limit: an upper bound).
- **The ledger entry the tool wrote** made a second `## 2026-10` heading above `## 2026-09`, because the project's ledger carries September above October (F8's shape); `check-ledger` does not count it.

## 6. The real tree's non-tracked files

The tool refuses a dirty tree; the four ignored generated files at the root are not dirt (F12 did not arise). Hashed before the move ([`real-nontracked-before.sha`](p15-adopter-runs/real-nontracked-before.sha)) and after: `.context-budget-history.jsonl`, `.quality-gates-results.json`, `dashboard.html` and `dashboard_history.jsonl` are **identical under `methodology/`** and gone from the root; `.claude/settings.local.json` is identical in place (the tool's `harness` row read 0 in every arm, including `tallx`, which carried a copy, and the file names none of the moved files). The real tree reads clean, and `git status` read 0 lines after each of the four commits.

## 7. Phase 0 in the new layout (a fresh clone of `5a41dbbdd`)

`methodology/SESSION_RUNNER.md` and `methodology/SAFEGUARDS.md` are byte-identical to canonical; `methodology/SESSION_NOTES.md` has its `## ACTIVE TASK` (`:99`); `git status` reads 0 lines; `bin/status` reads `layout: new`, 22 of 23 tracked `current` and `methodology/methodology_trim.py` `locally modified` (§2); `check-links --tree` exits 1 for the 110 project links only. **The `CHANGELOG.md` frontier is HEAD (`5a41dbbdd`); the `HANDOFFS.md` frontier is the move commit (`0e2663642`), one commit behind**: the trimmer restore touches the ledger but not the receipts, so the adopter's next Phase 0 will list `5a41dbbdd` as past its `HANDOFFS.md` frontier. It is recorded in `methodology/CHANGELOG.md` and needs no receipt of the adopter's own.

## 8. Not shown

- **A push or CI.** The five commits are local; a push starts the four push workflows (the nine edits are not in their ignore list). `R CMD check` was not run, only the tarball build; **a live GitHub run of the four filters** is not possible from a clone.
- **`build-document1-evidence.R`** was not run, before or after.
- **Another clone's hook arming** (§3) and the five `git worktree`s under `.claude/worktrees`, which sit on older commits and do not see the move.
- **The full suite in the real tree.** It ran in a fresh clone of the result; the three affected files ran in the real tree before the move. `quality_ratchet.py` and the dashboard ran in a clone (they write where they live).
- **Tier 1's tarball and filters**, and whether `quality_ratchet.py install-hook` has F17's shape.

## 9. The operator's

- **The push of the five commits** (`origin/master..HEAD`; mine are `4f67cb927`, `74804498a`, `0e2663642`, `5a41dbbdd`): its own go-ahead, naming the commit. Expect CI on the four workflows.
- **Rows F17 and F19** (§2, §3): open, untracked, his triage. F19's fix would be a place for a project-local ledger entry that survives an overlay; today the project carries the reminder in its `CLAUDE.md`, which still reads true (the path is now `methodology/methodology_trim.py`).
- **Which adopter next:** `mts-system`, `vscode_quarto_ext` and `wsfct` had a live `claude` session at S296's Phase 0 (the same three), `Philippians`, `dalia_martinez_funeral` and `chat_verification` were dirty, `claude_work` has no commit; `wsfct` stays last and only on a clean default branch.
