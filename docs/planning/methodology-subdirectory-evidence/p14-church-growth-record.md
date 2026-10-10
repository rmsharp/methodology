# BL-101 P14 — the fourth adopter, `church_growth` (S292, 2026-10-10)

Plan: [`methodology-subdirectory-plan.md`](../methodology-subdirectory-plan.md) §3 C5 (the adopters' older ledger hooks), §4.6 (two tiers), §7.4 (the per-adopter DONE list), §7.6 (the register is read first). **Out of plan order, by his pick at S292's Phase 0:** `nprcgenekeepr` and `mts-system`, the two ahead of it, each had a Claude session running that morning; `church_growth` had none. He chose it with the move at tier all in the option text.
**Nothing was pushed, tagged or sent upstream, and nothing can be pushed from here:** the adopter has **no remote at all** (`git remote -v` prints nothing), so its three new commits live only in `~/Development/church_growth`. Raw outputs: [`p14-adopter-runs/`](p14-adopter-runs/); the two scripts that ran the rehearsal and the final check are [`p14-rehearsal.sh`](p14-rehearsal.sh) and [`p14-final-clone.sh`](p14-final-clone.sh) (set `SCRATCH`; the second also `CTRL_SHA`).

## 1. What was done in the adopter

| Step | Commit there | Result |
|---|---|---|
| Start | `3035560` | `main`, 42 tracked files, last commit 2026-08-10, **no remote, no CI, no tests, no gates** (the tool's `ci`, `tests`, `proofs`, `scripts`, `config` and `harness` rows are 0; `.claude/settings.json` holds only `"model"`). A doc-only content repository: its `.methodology-profile` says `doc-only`. Framework files in the legacy layout, the manual and workstreams in `docs/methodology/`. **A tracked `.githooks/pre-commit` (2,807 B, 2026-07-11) with `core.hooksPath=.githooks` set in this clone.** One untracked file: `__pycache__/methodology_dashboard.cpython-310.pyc` (2026-08-10). Ignored and present: `dashboard.html`, `dashboard_history.jsonl`, `docs/**/exports/` |
| `bin/sync`, from this checkout at `9ccf08c` | `2f1389c` | **16 files updated, 8 created** (`FRAMEWORK_LEARNINGS.md`, `methodology_trim.py`, `context_budget.py`, `quality_ratchet.py`, both configs, `.gitattributes`, `docs/methodology/FRAMEWORK_APPARATUS.md`), 2 unchanged; 25 files changed with the hand-written ledger entry; **no `--force` was needed** (§2) |
| The ledger hook replaced with this repository's layout-aware one | `4cdf70a` | `.githooks/pre-commit` 2,807 B → 470 lines, its own commit with a ledger entry, before the move (§3) |
| `bin/migrate-layout --tier all --apply --trailer` | `62f7d8a` | 31 files changed, +24 −20: **30 renames** (27 at 100%, `.context-budget.json` and `.quality-gates.json` at 97%, `CHANGELOG.md` at 99%), `CLAUDE.md` edited in place (21 replacements on 16 lines), the two configs' paths rewritten, one ledger entry the tool wrote; **2 ignored generated files moved plainly** (`dashboard.html`, `dashboard_history.jsonl`); `docs/methodology/sessions/.gitkeep` left in place, the project's own |

The checkout synced from is `9ccf08c`; its distributed files are those of `add55f1` (`git diff --stat add55f1 HEAD -- bin tools starter-kit .githooks ITERATIVE_METHODOLOGY.md FRAMEWORK_APPARATUS.md HOW_TO_USE.md workstreams` lists only `bin/migrate-layout` and `tools/test_migrate_layout.py`, both canonical-only). The tracked file count is 42, then 50 after the sync (8 created) and 50 after the hook and the move. The trailer is `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`. No Claude session was running in the adopter at either of two checks (`pgrep` and `lsof` on each `claude` process's cwd, before the sync and before the apply).

## 2. What the sync needed, and what it did not

`bin/sync` ran **without `--force` and refused nothing**: every file it touched was either missing or 1 to 39 versions behind a known canonical version (`methodology_dashboard.py` 39, `BOOTSTRAP.md` 22, `SESSION_RUNNER.md` 12), so row F7 did not arise ([`real-sync-output.txt`](p14-adopter-runs/real-sync-output.txt)). The seeds the project owns (`SESSION_NOTES.md`, `CHANGELOG.md`, `HANDOFFS.md`, `ROADMAP.md`) were left as written; `bin/status` still marks `CHANGELOG.md` and `HANDOFFS.md` `present (stale format)`, and migrating those two is the adopter's. `bin/status` read **23 of 23 tracked files `current`** after the sync and at the new places after the move (`layout: new`).

## 3. The hook: why this adopter needed one more commit than the last three

Register row F2 and plan C5 said it in advance: an adopter's ledger hook is an older copy that names `CHANGELOG.md` at the root, and once the ledger leaves the root it finds no tracked ledger and passes every commit, silently. **Measured here, in six `--no-local` clones with the project's `core.hooksPath` set in each** ([`rehearsal-hook-probes.txt`](p14-adopter-runs/rehearsal-hook-probes.txt), [`rehearsal-log.txt`](p14-adopter-runs/rehearsal-log.txt)):

| Clone | Hook | A later commit with tracked content and **no** ledger entry | With an entry |
|---|---|---|---|
| `ctrl` (synced, not moved) | the project's old copy | **refused, exit 1** | exit 0 |
| `tall` (moved at tier all) | the project's old copy | **passes, exit 0: the gate fails open** | exit 0 |
| `tallh`, `tallx` (moved at tier all) | this repository's layout-aware hook, replaced in its own commit | **refused, exit 1** | exit 0 |

The move commit itself passed under both hooks, as C5 measured; only the **later** commit tells them apart. The same three probes ran against the real committed result, in a fresh clone of `62f7d8a` ([`final-clone-log.txt`](p14-adopter-runs/final-clone-log.txt)): no entry, exit 1; an entry at `methodology/CHANGELOG.md`, exit 0; an edit of a committed entry (the sync entry's heading), exit 1, `removed ### 2026-10-10 · [ad hoc] Synced the methodology files ...`. The hook's own `--selftest` read OK, 43 checks, in a rehearsal clone and in the final one. The replaced hook is the file at `9ccf08c` byte for byte; `core.hooksPath` is untouched (a per-clone setting: with no remote, no other clone is known to exist, and **another clone's arming remains not shown**, as at P13).

## 4. The adopter's own build, and the tool's checks

The project has no tests, CI or gates; its `CLAUDE.md` names its build equivalent as "re-checking the deliverable against its source", which no command runs. What the clones do show, before and after: the dashboard, the gates run, `bin/status`, `bin/check-links`, the two checkers, and the later-commit probes (§3).

| Check | Rehearsal, tier 1 | Rehearsal, tier all (3 arms) | Real apply (tier all) |
|---|---|---|---|
| `bin/status` tracked `current` | 23/23 → 23/23 | 23/23 → 23/23 | 23/23 → 23/23 |
| `check-ledger` | exit 1 → 1 | exit 1 → 1 | exit 1 → 1 |
| `check-handoff` | exit 1 → 1 | exit 1 → 1 | exit 1 → 1 |
| `check-links`, framework documents | 0 → 0 | 0 → 0 | 0 → 0 |
| `check-links`, the project's own files | 0 → **4** | 0 → 0 | 0 → 0 |
| history by `git log --follow` | 35 → 36 | 35 → 36 (`tall`), 36 → 37 (`tallh`, `tallx`) | 36 → 37 |
| clean tree after | yes | yes | yes |

- **`check-ledger` and `check-handoff` exit 1 are not the move.** The adopter's `CHANGELOG.md` is a stale-format seed: 29 findings, every one "orphaned text outside any entry" (the old header), the same 29 before and after; its `HANDOFFS.md` has 2 findings in the newest receipt and 5 `commit:` slots that name no sha (S14, S9, S7, S6, S5), the same before and after ([`check-ledger-handoff-before-after.txt`](p14-adopter-runs/check-ledger-handoff-before-after.txt)).
- **0 links dangle at tier all**, against 23 at P12 and 1 at P13: this ledger carries no relative link to a moved file. The 4 at tier 1 are register row F13 again, not links (tier 1 was rehearsed, not applied).
- **The dashboard reads 49/100 and risk high before and after the move**, in the clone of `4cdf70a` and of `62f7d8a` (`Commits` 59 and 60), with the same line in both: *doc-only repo detected (marker override)*. So the `.methodology-profile` the project keeps at its root is still read by the dashboard under `methodology/`. Before the sync the project's own 39-versions-behind dashboard read 34 ([`rehearsal-dashboards.txt`](p14-adopter-runs/rehearsal-dashboards.txt)). `quality_ratchet.py --run` reads `0/0 pass` (no gate is declared), results and manifest `4f53cda18c2b`, before and after.
- **Left in place by the tool: 1 file**, `docs/methodology/sessions/.gitkeep`, which is the project's own. `docs/methodology/` now holds nothing else.
- **Prose the tool reports and does not rewrite:** `other` 54 mentions in 6 files (`BACKLOG.md`, `.gitignore`, `.methodology-profile`, two planning documents and `CLAUDE.md:28`), `ledger` 306 mentions in 3 files (a committed entry is never edited).
- **`CLAUDE.md`: 21 replacements on 16 lines, 9 of those lines inside the project's own `### Project-specific Learnings`** (line 68 on; the changed lines are 84, 87, 151, 154, 169, 170, 205, 206 and 216). The learnings describe events at the old paths (Learning 11: a grep in July found ~80 hits "inside `CHANGELOG.md`", now reading `methodology/CHANGELOG.md`). The tool printed this diff before the apply and cannot tell a live pointer from a past-tense account. Row F16.

## 5. The one warning the tool got wrong

After the hook is replaced, the tool's `hooks` row prints, in the dry run and in the apply: `WARNING: 1 hook line(s) run a moved tool: that hook will refuse the migration commit and the run will roll back; update the hook first`. **It did not**: the apply exited 0 in both arms that carry the replaced hook (`tallh`, `tallx`) and on the real tree. The tool's own JSON names the line: `.githooks/pre-commit:303`, `rtool=quality_ratchet.py    # layout: ok -- the tool's name; the three places are tried below`, the only `runs_tool: true` site of 15 ([`hook-warning-sites.json`](p14-adopter-runs/hook-warning-sites.json)). It is a variable assignment, not a run, and the hook tries three places for the tool. The warning fires on the very hook that row F2 tells an adopter to install first. Row F15.

## 6. The real tree's non-tracked files

The tool refuses a dirty tree, and the dry run on the real tree listed the stray `__pycache__/methodology_dashboard.cpython-310.pyc` as the only dirt (`REFUSED: [dirty-tree]`, with `[not-current]`). It is not a methodology file, the tool does not move it, and it is not in the project's `.gitignore`. What was done, as at P13: `/__pycache__/` went into the repository's `.git/info/exclude` (a local file, nothing tracked), the sync and the apply ran, and **after the apply the exclude file was put back and `cmp` read it identical** to the copy taken before. The pyc and the two ignored generated files were hashed before and after ([`real-untracked-hashes.txt`](p14-adopter-runs/real-untracked-hashes.txt)): **all three sha256 identical** (`19c1958c078e`, `2ccd4ed32685`, `5050cbab6324`), the pyc where it was, the other two under `methodology/`, still ignored by the project's unanchored `dashboard.html` and `dashboard_history.jsonl` lines (`git check-ignore -v methodology/dashboard.html` names `.gitignore:2`). The real tree reads `?? __pycache__/`, as before the session. Unlike `airqino` (F12), the moved files here were already ignored, so the second exclude set P13 needed was not needed; the first still was. A `__pycache__/` line in the project's `.gitignore` would end it (its own commit).

## 7. Phase 0 in the new layout (a fresh clone of `62f7d8a`)

`methodology/SESSION_RUNNER.md` and `methodology/SAFEGUARDS.md` are byte-identical to canonical; `methodology/SESSION_NOTES.md` has its `## ACTIVE TASK` (`:9`); `git status` reads 0 lines; the `CHANGELOG.md` and `HANDOFFS.md` frontiers are both `62f7d8a`, 0 undocumented commits, 0 merges; `bin/status` reads `layout: new`, 23 tracked `current`; `bin/check-links --tree` exits 0; the dashboard reads 49 and risk high, the same as on the clone before the move ([`final-clone-log.txt`](p14-adopter-runs/final-clone-log.txt)).

## 8. Not shown

- **A push or CI:** there is no remote and no CI.
- **Another clone's hook arming:** none is known to exist (no remote).
- **An adopter session after the move:** its next Phase 0 will be the first by an agent that reads the relocated runner there; its `CLAUDE.md` now says `methodology/SESSION_RUNNER.md`.
- **The adopter's `.claude/settings.json`:** it holds a model name and no path; the tool's `harness` row is 0.
- **`quality_ratchet.py` or the dashboard in the real tree:** both write there (the dashboard appends to the project's ignored 23-snapshot history); they ran in clones.

## 9. The operator's

- **The two stale seeds** (§4): `CHANGELOG.md` and `HANDOFFS.md` carry the pre-v3 header; `bin/status` gives the migration steps. That is what keeps `check-ledger` and `check-handoff` at exit 1 here.
- **`__pycache__/`** in the project's `.gitignore` (one line, its own commit), so the next dry run is not refused for a stray pyc.
- **The next adopter with a hook:** `chat_verification` carries an older ledger hook too (the plan's survey table: `.githooks` 26 lines, `core.hooksPath` set); its session replaces the hook the same way, as its own commit before the move. `wsfct`'s is untracked and names `context_budget.py` at the old root (F2).
- **Rows F15 and F16** (§4, §5): open, untracked, his triage.
- **Which adopter next:** `nprcgenekeepr` and `mts-system` each had a session running at S292's Phase 0; `Philippians` is off the table while his `sermons/03-joy-in-knowing-christ.*` edits sit uncommitted.
