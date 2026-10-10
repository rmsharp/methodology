# BL-101 P13 — the third adopter, `airqino` (S291, 2026-10-10)

Plan: [`methodology-subdirectory-plan.md`](../methodology-subdirectory-plan.md) §4.6 (two tiers), §7.4 (the per-adopter DONE list), §7.6 (the register is read first), D1, D9. He chose `--tier all` for `airqino` (the P13 default he gave at S290's Phase 0, confirmed at S291's). The S286 survey found no file in this adopter that reads a moved path.
**Nothing was pushed, tagged or sent upstream.** `airqino` has a GitHub remote (`rmsharp/airqinodashboard`) and no CI; its two new commits stay in its own repository, 2 ahead of `origin/main` (`git rev-list --left-right --count origin/main...HEAD` reads `0 2`). Raw outputs: [`p13-adopter-runs/`](p13-adopter-runs/); the two scripts that ran the rehearsal and the final check are [`p13-rehearsal.sh`](p13-rehearsal.sh) and [`p13-final-clone.sh`](p13-final-clone.sh) (set `SCRATCH`; the second also `SYNC_SHA`).

## 1. What was done in the adopter

| Step | Commit there | Result |
|---|---|---|
| Start | `998cd51` | `main`, level with `origin/main` (fetched), 72 tracked files, **no CI, no hooks** (`core.hooksPath` unset, `.git/hooks` empty), 7 files under `tests/`; framework files in the legacy layout, with `docs/methodology/` holding the manual, the workstreams **and an older nested copy of the framework's own repository** (§4). **4 untracked files:** three generated ledger files at the root and `docs/HARDWARE.html` (a 633 KB pandoc render of the tracked `docs/HARDWARE.md`, dated 2026-04-12, the project's own) |
| `bin/sync`, from this checkout at `41296a1` | `da595cb` | 21 files updated, `.gitattributes` created, 23 files changed (+1,892 −425) with the hand-written ledger entry; **no `--force` was needed** (§2) |
| `bin/migrate-layout --tier all --apply --trailer` | `f7a0194` | 32 files changed, +22 −18: **30 renames** (27 at 100%, `.context-budget.json` and `.quality-gates.json` at 97%, `CHANGELOG.md` at 99%), `CLAUDE.md` (20 replacements) and `.gitignore` (1) edited in place, the two configs' paths (3 and 1) rewritten, one ledger entry the tool wrote; **4 untracked files moved plainly** (`dashboard.html`, ignored, and the three generated ledger files) |

The checkout synced from is `41296a1`; its distributed files are those of `add55f1` (`git diff --stat add55f1 HEAD -- bin tools starter-kit .githooks ITERATIVE_METHODOLOGY.md FRAMEWORK_APPARATUS.md HOW_TO_USE.md workstreams` lists only `bin/migrate-layout` and `tools/test_migrate_layout.py`, both canonical-only). The sync was committed as one commit, exactly the 22 files it wrote and its own ledger entry (`BOOTSTRAP.md`, "Committing a sync"). `bin/status` read **23 of 23 tracked files `current`** after the sync and at the new places after the move (`layout: new`). The commit trailer is `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`, as the adopter's last commits carry one for the model that wrote them.

## 2. What the sync needed, and what it did not

`bin/sync` ran **without `--force` and refused nothing**: every one of the 21 files was 1 to 11 versions behind a known canonical version, so register row F7 (a refusal that does not say which version is nearest) did not arise. `CONTEXT_TEMPLATE.md` and `DESIGN_WORKSTREAM.md` were already `current`. The seeds the project owns (`SESSION_NOTES.md`, `CHANGELOG.md`, `HANDOFFS.md`, `ROADMAP.md`, both configs) were left as written. `bin/status` marks `HANDOFFS.md` `present (stale format)`: migrating that seed is the adopter's, as at P12.

## 3. The adopter's own build, at each state

Its build equivalent is `python3 -m pytest -q`, which its gates `tests-exit` and `tests-passed` (floor 144) run too; Python 3.10.12, Flask 3.1.3, pytest 9.0.2. The tests drive Flask's test client and need no device, credentials or `.env` (its `README.md:32`). Run in `--no-local` clones, and in the real tree after the sync and after the move (it writes only ignored caches there):

| State | pytest | Gates (`quality_ratchet.py --run`) |
|---|---|---|
| base: `998cd51` | exit 0, 144 passed, 2 xfailed, 0.57 s | exit 0, 2/2 pass, results `2993256f954d`, manifest `0f1d28b61292` |
| ctrl: synced | exit 0, 144 passed, 2 xfailed | exit 0, same |
| tier 1 (rehearsal) | exit 0, 144 passed, 2 xfailed | exit 0, same |
| tier all (rehearsal, 3 arms) | exit 0, 144 passed, 2 xfailed, each | exit 0, same |
| the real tree after the sync | exit 0, 144 passed, 2 xfailed | not run there (it rewrites the project's untracked results file) |
| the real tree after the move | exit 0, 144 passed, 2 xfailed | — |
| **the real `f7a0194`, a fresh clone** | exit 0, 144 passed, 2 xfailed | exit 0, 2/2 pass, results `2993256f954d`, manifest `0f1d28b61292` |

The skip count did not rise (2 xfailed throughout). The results hash and the manifest hash are the ones the project's own last receipt cites (`SESSION_NOTES.md`, S20). **No test, gate command or script reads a moved path:** the tool's `tests`, `ci`, `hooks`, `proofs`, `config` and `harness` rows are all 0, and its one `scripts` hit in the project's own code, `app.py:81` (`render_template("dashboard.html", ...)`), names `templates/dashboard.html`, which stays (the survey said so).

## 4. The tool's own checks, and what tier 2 costs here

| Check | Rehearsal, tier 1 | Rehearsal, tier all | Real apply (tier all) |
|---|---|---|---|
| `bin/status` tracked `current` | 23/23 → 23/23 | 23/23 → 23/23 | 23/23 → 23/23 |
| `check-ledger` | exit 0 → 0 | exit 0 → 0 | exit 0 → 0 |
| `check-handoff` | exit 1 → 1 | exit 1 → 1 | exit 1 → 1 |
| `check-links`, framework documents | 0 → 0 | 0 → 0 | 0 → 0 |
| `check-links`, the project's own files | 0 → **4** | 0 → 1 | 0 → 1 |
| history by `git log --follow` | 76 → 77 | 76 → 77 | 76 → 77 |
| clean tree after | yes | yes (clean clone), **no at exit 4 (§5)**, yes (`tallm`) | yes |

- **The 1 dangling link at tier all** is `methodology/CHANGELOG.md:11`, the project's own ledger header, which links `docs/methodology/FRAMEWORK_APPARATUS.md#the-action-ledger`; the file it names moved, and a ledger is never edited by the tool (C6). It is register row F9's cost again, at 1 link where P12's was 23. A one-line fix (`FRAMEWORK_APPARATUS.md#the-action-ledger`) would be its own commit there.
- **The 4 at tier 1** are not links. `bin/check-links --tree` finds the tier-1 tree in the new layout and looks for the four seeded files (`SESSION_NOTES.md`, `CHANGELOG.md`, `HANDOFFS.md`, `ROADMAP.md`) under `methodology/`, where tier 1 does not put them: `<distributed file missing from tree>`. Tier all does not have it; tier 1 was not applied.
- **`check-handoff` exit 1 is not the move.** The adopter's `HANDOFFS.md` has 6 receipts whose `commit:` slot names no usable sha (S18 `5056055` and S13 `5084680`, which are all digits and read as numbers, and S8, S7, S6 and S5, which say `pending`), the same 6 before and after ([`check-handoff-before-after.txt`](p13-adopter-runs/check-handoff-before-after.txt)). The tool's `ledger` row read exit 0 before and after: the entry it wrote landed under the new `## 2026-10` heading, above the sync's entry, in the rehearsal and in the real ledger (`git show f7a0194:methodology/CHANGELOG.md`, lines 18 to 24), as the project's own convention asks (`CLAUDE.md`, "Legacy layout, left as written").
- **Left in place by the tool: 19 files**, all under `docs/methodology/`: `CLAUDE.md`, `LICENSE`, `README.md`, 5 under `bin/`, 10 under `starter-kit/` (a whole older copy of the runner, the safeguards, the templates and the dashboard) and 1 under `tools/`. They are an older **nested copy of the framework's own repository**, tracked, which no manifest names (the plan's §2.2 had named it at the survey: a nested `starter-kit/`, `bin/` and README; the run measures what stays, row F14). After the move `docs/methodology/starter-kit/SESSION_RUNNER.md` is a second runner that a reader can open, and `docs/methodology/README.md` tells the reader to read `SESSION_RUNNER.md` at a root where there is none. Deleting the copy is the adopter's, and its own commit.
- **Prose the tool reports and does not rewrite:** `other` 386 mentions in 13 files (`BACKLOG.md`, `README.md`, the nested copy), `ledger` 285 in 3 files (`CHANGELOG.md`, `HANDOFFS.md`, `SESSION_NOTES.md`; a committed entry is never edited).

## 5. The one place the tool needed help: untracked generated files

The tool **refuses a dirty tree, untracked files included**, and the dry run on the real tree listed all four untracked files as the dirt, while its own plan listed three of them as `git mv ... (not tracked: a plain move)`. They were untracked, not ignored, because the project's `.gitignore` names only `/dashboard.html`; the three files date from 2026-09-18. `docs/HARDWARE.html` is not a methodology file and not mine to commit, ignore or delete.

What was done: the four names went into the repository's `.git/info/exclude` (a local file, nothing tracked; the same in each rehearsal clone), and the three generated names **at their new place** too. The rehearsal showed why the second set matters:

| Arm | Excluded names | `--apply` | After |
|---|---|---|---|
| `tallx` | the four old names | **exit 4**, `CHECKS DIFFER (tree not clean)`, the commit stands | `?? methodology/.context-budget-history.jsonl`, `?? methodology/.quality-gates-results.json`, `?? methodology/dashboard_history.jsonl` |
| `tallm` | the four old names and the three new | exit 0, `clean tree: yes` | `[]` |

The three generated files arrived byte-identical in both arms and on the real tree (sha256, [`real-untracked-hashes.txt`](p13-adopter-runs/real-untracked-hashes.txt)); `docs/HARDWARE.html` is where it was, identical. **After the apply the real tree's `.git/info/exclude` was put back byte-for-byte** (`diff` against the copy taken before), so the project's tree is untracked in the same four places as before the session, three of them under `methodology/` now. Row F12. Rows F13 (tier 1's `links` row, §4) and F14 (the nested copy, §4) are the other two findings of the run.

## 6. Phase 0 in the new layout (a fresh clone of `f7a0194`)

`methodology/SESSION_RUNNER.md` and `methodology/SAFEGUARDS.md` are byte-identical to canonical and sit where the runner says; `methodology/SESSION_NOTES.md` has its `## ACTIVE TASK` (`:7`); `git status` reads 0 lines; `python3 methodology/methodology_dashboard.py --no-open` reads health **68, risk 0**, the same as the same tool on a clone of `da595cb` (synced, before the move): 68 and 0. The `CHANGELOG.md` and `HANDOFFS.md` frontiers are both `f7a0194`, 0 undocumented commits, 0 merges. In a fresh clone the dashboard starts a new, untracked `methodology/dashboard_history.jsonl` (the project's own 30-snapshot history is untracked and does not travel); in the real tree it would append to that file, so it was not run there. [`final-clone-log.txt`](p13-adopter-runs/final-clone-log.txt).

## 7. Not shown

- **Any push or CI:** `airqino` has no CI; its push is its own go-ahead.
- **A run of `quality_ratchet.py` or the dashboard in the real tree:** both write the project's untracked files; they ran in clones of `da595cb` and `f7a0194`.
- **Another clone's hook arming:** the adopter has no hooks.
- **The adopter's `.claude/` directory and `.env.example`:** the tool's `harness` and `config` rows are 0; neither was opened.
- **The adopter's own later sessions:** its next Phase 0 will be the first by an agent that reads the relocated runner on a machine other than this one.

## 8. The operator's

- **The nested copy** (§4): 19 tracked files under `docs/methodology/` that are an old copy of this repository. Delete them in the adopter, or leave them; the tool will not.
- **The generated files:** whether the project ignores `dashboard_history.jsonl`, `.context-budget-history.jsonl` and `.quality-gates-results.json` (a three-line `.gitignore` change in the adopter, its own commit), as it already ignores `dashboard.html`. Until it does, the next adopter in this state needs §5's workaround or a tool change (row F12).
- **The ledger header link** at `methodology/CHANGELOG.md:11` and, if wanted, the stale seed `HANDOFFS.md`.
- **The tier for the next adopter:** here tier all cost 1 link and nothing the build reads, which is what the survey's zero predicted. `Philippians` is off the table while his uncommitted `sermons/03-joy-in-knowing-christ.*` edits sit in its tree (4 modified files at this session's end of work); `vscode_quarto_ext` needs `methodology/**` in its `.vscodeignore` (F11); `nprcgenekeepr` has a session of its own running.
