# BL-105 build phase 1 — the rehearsal (S302, 2026-10-12)

Plan: [`methodology-subdirectory-plan.md`](../methodology-subdirectory-plan.md) D10 (§9) and §7.6; decision record [`bl105-record.md`](bl105-record.md) §5 item 1. **His pick at the S302 Phase 0 picker**, which also gave two go-aheads (the owed HANDOFFS trim and the push of `e5d88a5` to the fork), both done before the claim. **Nothing is built:** no tool, distributed document, adopter or upstream repository was changed, and no real adopter tree was written (`nprcgenekeepr`, `mts-system`, `wsfct` and `vscode_quarto_ext` each had a live session; every run below was in a `--no-local` clone). Raw outputs and the scripts are in [`bl105-runs/`](bl105-runs/) and beside this file.

**Method.** Clones were made at the adopters' checked-out commits under `~/.cache/bl105-rehearsal`, a path without the word `scratchpad` (F23): `nprcgenekeepr` at `5cacf616`, `mts-system` at `d1cf54fb`, `model_project_constructor` at `ec23bc7e`. **The companion rule is simulated, not built:** [`bl105-companion.py`](bl105-companion.py) imports `bin/migrate-layout` as a module and gives its existing rewrite functions one extra mapping, `PROJECT_LEARNINGS.md` to `methodology/PROJECT_LEARNINGS.md`: `CLAUDE.md` is rewritten as text (`token_rewriter`), a config's path values by `rewrite_json`, `.gitignore` by `rewrite_gitignore`, then `git mv` and one commit; the tool's own `run_checks` ran before and after. Arms per adopter: **base** (untouched), **move** (the tool's rewrites only) and **edit** (move, then the hand edits in a second commit). `mts-system` is still legacy, so its control is the tree synced and migrated by the tool as it is (`bin/sync`, then `bin/migrate-layout --tier all --apply`, 40 files, one commit), which the other arms start from; the other two adopters are already migrated, so the move is a top-up there.

## 1. The answer first

**B stands: nothing in the rehearsal withdraws it.** Each adopter returned to its base result with a small edit of its own, and the worst case (3.2 MB, 143 names) changed nothing. **The edits touch 6 files in 3 adopters, where the census listed 5** (2 of the 6 only pin the new place or test the edited code), and the sixth is a project document the census could not have found by name; two of the three adopters are red or broken after the move for a reason no check of the tool reports.

| | The tool's rewrite | The project's own checks after the move alone | The edit that restores base |
|---|---|---|---|
| `nprcgenekeepr` | `CLAUDE.md`, 5 lines (7 places) | full suite **identical**: 11,163 tests, 10,970 passed, 0 failed, 187 skipped, 394 per-file results equal; declared tarball gate 3,784,543 B to 3,784,545 B (limit 5,000,000); one script exits 1 (base 0) | 2 files, 1 line each: the script's path, and one name added to a test's list (green either way) |
| `mts-system` (tool's migration first) | `CLAUDE.md` 2 lines (3 places), one config value | its 17 tests green; the real-tree `--check` exits 2 (base 1); the shipped budget gate follows the move | `scripts/learnings_archive.py` and its test: +41 −4, 17 tests to 19 |
| `model_project_constructor` | `CLAUDE.md`, 3 lines (5 places) | **2 tests red and 26 skipped** (suite 3,914 passed against 3,942; the same two tests) | 2 files, 3 lines: a constant in the test, two sentences in a project-owned document |

## 2. `nprcgenekeepr` (a top-up on a migrated tree)

- **The move:** rename at 100% (3,232,615 B), 806 commits reached by `git log --follow` before, 807 after; the commit went through the adopter's own per-clone hook (copied in, F18). `CLAUDE.md` 20,414 B to 20,498 B (ceiling 28,000). `.gitignore` and both configs have no entry for the file, so the tool rewrites nothing else.
- **The tool's checks, before and after:** `bin/status` 22 of 23 `current` in both (the locally modified trimmer, F19), `check-ledger` and `check-handoff` exit 1 in both, `check-links` 0 framework and 110 project in both, `bin/sync --dry-run` refuses the same file in base and move.
- **Tests:** the three files that read paths (`test_rbuildignore.R`, `test_handoffsReceiptPlacement.R`, `test_workflowPathsIgnore.R`) read 4, 10 and 240 expectations in base and move, 244 in edit; the full suite and its per-file CSV are equal in base and move. `test_workflowPathsIgnore.R` **pins names, not places**: it stays green when the file moves, and the new place is pinned nowhere until the one added line (which then passes, so the property holds: `.Rbuildignore`'s `^methodology$` excludes it and the four workflows list `methodology/**`).
- **The script nothing covers:** `vignettes/articles/data-raw/build-document1-evidence.R:186` reads `PROJECT_LEARNINGS.md` from the root. Base exit 0, move exit 1 (`cannot open file`), edit exit 0 (`ledger_path()`, the helper the script already has for its three ledgers); base and edit write the same four data files, hashes equal. P15 left it unrun.
- **Package and CI:** the tarball does not change (+2 B). The four workflows' lists were not run live (GitHub): read, `methodology/**` is there.
- **Links:** 1 markdown link to the file (`CLAUDE.md`, rewritten), 0 dangle.

## 3. `mts-system` (legacy: the tool's migration, then the companion)

- **Control (the tool as it is):** sync read 0 refusals; the migration is one commit of 40 files; its checks equal before and after (15 project links dangle, P18's cost). **Already here, with the file at the root:** the archiver's 17 tests stay green while its real-tree `--check` goes from exit 1 (`265,780 B against the 250,000 B trigger: over`) to exit 2 (`cannot read .context-budget.json`): the config moved and the tests build a fixture root. The tool's list names both files; nothing in the tool shows the effect.
- **The move:** `CLAUDE.md` (3 places), and **`methodology/.context-budget.json` one `path` value**, so the shipped budget gate measures `methodology/PROJECT_LEARNINGS.md` at the same 265,780 B. The tool as written reads the two configs **at the root only** (`plan_rewrites`, `bin/migrate-layout:439-440`); here they are under `methodology/`, and the driver reads both places. History 172 to 173 commits.
- **Move without edits:** 17 tests green; `--check` exit 2 again, now `cannot read PROJECT_LEARNINGS.md`.
- **Edit** (the diff, first section of [`mts-raw.txt`](bl105-runs/mts-raw.txt)): a `_where(root, name)` helper used at the three places that read a path, and `LIVE_REL` for the text the tool writes; two new-layout tests. 19 tests green; `--check` exit 1, the same line as base. **`--write` on a copy of each:** the same rows 84 to 148 move to the same shard, byte-identical to base's; the live file differs in line 9 only, **the lookup command** written for the next reader: `git grep -n "^| 73 |" -- PROJECT_LEARNINGS.md ...` becomes `-- methodology/PROJECT_LEARNINGS.md ...`. Unedited, that command at the new place exits 1 with no output (0 hits, no error); edited, it finds the newest row.
- **Links and hooks:** 2 links to the file, 1 dangles already in the control, none because of the move; the project's tracked hook checks black and isort on `mts-backend` and names nothing moved (not armed in a clone). The live tree has one modified `dashboard_history.jsonl`, absent from a clone (F12 at P18).

## 4. `model_project_constructor` (tier 1, a top-up)

- **The move:** rename at 100% (411,884 B), `CLAUDE.md` 3 lines (5 places), no config entry; the dashboard reads 96/100 and risk 1 before and after; `bin/sync --dry-run` exit 0, nothing refused.
- **Move without edits:** `tests/test_read_budget.py` goes from 47 passed to **2 failed, 19 passed, 26 skipped**, and the whole suite from 3,942 passed and 9 skipped to 3,914 passed and 35 skipped: **no other test reacts**. Two causes. The test reads the file at the root (`known_refused`). And its `declared` check **requires two sentences naming the file exactly once** in `CLAUDE.md` and in `docs/methodology/PROJECT_CONVENTIONS.md`: the tool's text rewrite changed the first, and the second is a project document the tool never edits.
- **Edit** (the diff, first section of [`mpc-raw.txt`](bl105-runs/mpc-raw.txt)): `LEARNINGS = "methodology/PROJECT_LEARNINGS.md"` in the test, then the two sentences in the conventions document. The first edit alone leaves 1 test red (the second file). After both, 47 passed and the whole suite equals base (3,942 and 9).
- **Links, by where each lands:** 115 links to the file; 107 sit in frozen archived shards and dangled already; the file's own 3 self-links resolve; **4 in 2 live documents dangle because of the move** (`BACKLOG.md` 1, `docs/planning/ledger-budgets-review.md` 3). `check-links` read the same project count before and after.
- **Environment:** the system Python lacks `sqlalchemy`; the project's `.venv` has it and **imports the package from the real tree** unless `PYTHONPATH` names the clone's `src` (without it the run would have tested the live project). The first attempts (`mpc-full-*`, `-x`, aborted on the missing module in base and edit alike) are in the raw file, apart from the runs that count.

## 5. The tool's list against what broke

| What broke or would | Listed by the tool's F5 list? | Effect seen by any check of the tool? |
|---|---|---|
| `nprcgenekeepr` script `:186` | yes (a script, code mention) | no: found by running it |
| `nprcgenekeepr` `test_workflowPathsIgnore.R:39` | yes | no: green either way |
| `mts-system` archiver and its test | yes (both, code mentions) | no: tests green while the real-tree call fails (also before the move) |
| `mts-system` the lookup text it writes | the file, not the text | no |
| `mpc` `test_read_budget.py` | yes | the red appears only by running it |
| `mpc` `PROJECT_CONVENTIONS.md` | counted in `other` (709 mentions, 35 files), not among its 25 shown sites | no |
| `mpc` 4 live links | counted in `other`, not shown | `check-links` unchanged |

The list never missed a file that broke: it named every one **or counted it**. What it cannot do is say which of the 10 to 40 candidates per adopter does something, which is F4's limit; only running the project does. **F16 (does the text rewrite make a line false):** 10 `CLAUDE.md` lines changed, 3 in a Learnings region (one live pointer each); none states where the file was, so F16 stays declined.

## 6. Findings, as register rows

F25 to F30 in [`findings-register.md`](findings-register.md): the rewrite of `CLAUDE.md` turning a project's prose-pinning test red (F25); the archiver failing on the real tree while its tests pass (F26, before and after the move); the text the archiver writes (F27); the script no test covers (F28); the configs the tool reads at the root only (F29); live links the move breaks and no check reads (F30).

## 7. What this changes in the build

1. **Phase 2 (the tool, RED first)** gains requirements this run found: the companion's config rewrite and the top-up mode read `.context-budget.json` and `.quality-gates.json` **where the layout puts them** (F29); the mode takes a tree the tool calls migrated (`nothing to migrate` today); one commit, rename at 100%, one ledger entry; and a decision on F30 (list live project links to the moved file, or rewrite them), which is his.
2. **Phase 3 (the distributed prose)** is unchanged: `BOOTSTRAP.md:218,220,222,439`, `CLAUDE_TEMPLATE.md:83`, `bin/check-links:84`.
3. **Phase 4 (the adopters)**: each adopter's hand edits come in **its own commit before the move**, as F20 asked for the others (the three diffs, the first section of each `bl105-runs/*-raw.txt`, are the starting texts); `mts-system` and `wsfct` take them at their own migration; `nprcgenekeepr`'s script and `model_project_constructor`'s two files are the known sites. **A census of names under-counts: it found 5 sites and the run 6 files**, because a test read a prose document as data; every adopter's phase 4 needs its own run.

## 8. Not shown

- **GitHub CI** (the four R workflows' `paths-ignore`, `model_project_constructor`'s workflow): read, never run. `R CMD check`, the vignette and pkgdown builds, and `mts-system`'s backend and iOS suites were not run (nothing in them names the file).
- **`wsfct` and `vscode_quarto_ext`:** carry the file and were not rehearsed (a live session each); the census says `vscode_quarto_ext`'s `.vscodeignore` and config already hold, by reading, not by `vsce`.
- **A built tool.** The driver is the tool's own functions with one more mapping: a built rule may differ (the ledger entry, the commit text, the top-up refusals). One run per arm, under a load average of 18 to 50; times are not a result.
- **Another clone's hook arming**, and `mts-system`'s and `model_project_constructor`'s hooks (not armed in clones; neither names a moved file).

## 9. The operator's

- **Build phase 2 next?** B stands on this evidence; the session did not decide it for him. F30 is his call: whether the companion lists or rewrites live links to the moved file.
- **The three hand-edit diffs are starting texts, not applied anywhere:** each adopter's own session decides its edit.
