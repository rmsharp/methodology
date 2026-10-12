# BL-101 P16 — the sixth adopter, `chat_verification` (S297, 2026-10-11)

Plan: [`methodology-subdirectory-plan.md`](../methodology-subdirectory-plan.md) §3 C5 (an older ledger hook), §7.4 (the per-adopter DONE list), §7.6 (the register is read first). **Out of plan order, by his pick at S297's Phase 0 and with two go-aheads (the owed HANDOFFS trim and the preparation of the tree):** `mts-system`, `vscode_quarto_ext` and `wsfct` each had a Claude session running, `Philippians` and `dalia_martinez_funeral` were dirty, `claude_work` has no commit; `chat_verification` had no session and one dirty file, which F12's remedy prepares. He then chose "Apply, correct there, tool later" at the picker that followed the rehearsal (§5).
**Nothing was pushed, tagged or sent upstream, and nothing can be pushed from here:** the adopter has **no remote** (`git remote -v` prints nothing), so its five new commits live only in `~/Development/chat_verification`. Raw outputs: [`p16-adopter-runs/`](p16-adopter-runs/); the two scripts are [`p16-rehearsal.sh`](p16-rehearsal.sh) and [`p16-final-clone.sh`](p16-final-clone.sh) (set `SCRATCH`; the second also `CTRL_SHA`).

## 1. What was done in the adopter

| Step | Commit there | Result |
|---|---|---|
| Start | `107cbed` | `main`, 36 tracked files, **no remote, no CI, no tests, no declared gate**. A doc-only content repository (a dry-run delivery packet and one process definition). Framework files in the legacy layout, the manual and workstreams in `docs/methodology/`. **A tracked `.githooks/pre-commit` (8,915 B, 2026-08-03) with `core.hooksPath=.githooks`.** One modified tracked file, `dashboard_history.jsonl` (one snapshot line, 2026-08-12T23:52, never committed; the project's `.gitignore` says the file is deliberately tracked, append-only history). Ignored and present: `dashboard.html`, `__pycache__/`. Its own S9 claim (2026-08-13) is still `status: pending` in its `HANDOFFS.md` |
| The tree prepared (F12's remedy) | `b41fb8d` | the snapshot line committed, as its own commit with a ledger entry (the old hook refuses a commit without one); sha256 of the file identical before and after |
| `bin/sync`, from this checkout at `59887b4` | `ee28226` | **19 files updated, 4 created** (`quality_ratchet.py`, `.quality-gates.json`, `.gitattributes`, `docs/methodology/FRAMEWORK_APPARATUS.md`), 2 unchanged; the four seeds and `.context-budget.json` left as written; **no file refused, no `--force`** (F7 and F19 did not arise) |
| The ledger hook replaced with this repository's layout-aware one | `a3174b3` | `.githooks/pre-commit` 8,915 B to 26,463 B, byte-identical to `59887b4`; `--selftest` OK, 43 checks (§3) |
| `bin/migrate-layout --tier all --apply --trailer` | `ebbfabd` | 33 files changed: **32 renames** (29 at 100%, 2 at 97%, 1 at 99%) and `dashboard.html` (ignored) moved plainly; `CLAUDE.md` 14 replacements on 8 lines, the two configs' paths rewritten, one ledger entry the tool wrote (§5) |
| The tool's ledger entry moved out of an example block | `0a8ef90` | F21 (§5); accepted by the replaced hook. Made once as `7823e31` and redone before any other step (soft reset, unpushed, no remote) to correct a count in its own entry (14 ledgers to 12, §5) |

The trailer is `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`. No Claude session was running in the adopter at any check (`pgrep` and `lsof` on each `claude` process's cwd: at Phase 0, the claim, the preparation, the sync, the hook, the dry run, the apply, the correction and its redo).

## 2. The rehearsal, and what it decided

[`p16-rehearsal.sh`](p16-rehearsal.sh) ran **six `--no-local` clones with the project's hook armed** (`base`, `ctrl` synced, `t1`, `tall` with the old hook, `tallh` with the replaced hook, `tallx` with the real tree's ignored files copied in), at the adopter's `b41fb8d`. Unlike P14's script it does not force a refused sync: none was refused. Every apply exited 0 at both tiers with either hook. The tool's `checks (before -> after)` read identical in the clones and in the real apply: `bin/status` 23/23 `current`, `check-ledger` exit 1 to 1, `check-handoff` exit 1 to 1, `check-links` 0 framework and 0 project dangling (tier 1: 0 to 4, **F13 again**, tier 1 not applied), history by `git log --follow` 33 to 34, clean tree. [`rehearsal-log.txt`](p16-adopter-runs/rehearsal-log.txt) is the whole run.

## 3. The hook (F2)

Measured in the six clones ([`rehearsal-hook-probes.txt`](p16-adopter-runs/rehearsal-hook-probes.txt)), then on the real result in a fresh clone (§7):

| Clone | Hook | A later commit with tracked content and **no** ledger entry | With an entry |
|---|---|---|---|
| `base`, `ctrl` (not moved) | the project's old copy | **refused, exit 1** | exit 0 |
| `tall` (moved at tier all) | the project's old copy | **passes, exit 0: the gate fails open** | exit 0 |
| `tallh`, `tallx` (moved at tier all) | this repository's layout-aware hook | **refused, exit 1** | exit 0 |

The old hook also demanded a ledger entry for the preparation commit, so the sync, the hook and the correction each carry one in the project's own format.

## 4. The adopter's own checks, and the tool's

The project has no tests, CI or gate; its own mechanical check is `context_budget.py`. **Identical before and after** (the clones and the fresh clone of the result): `context_budget.py --status` exits 2 both times (`SESSION_NOTES.md` is 1,113 lines against a 400-line ceiling, the project's own BL-15; `CLAUDE.md` 20,583 B before the rewrite, 20,734 B after, ceiling 28,000 B, ok); `check-ledger` reads **83 findings** in every arm (the old seed's own header text); `check-handoff` reads 1 issue (the project's pending S9 receipt); `quality_ratchet.py --run` reads `0/0 pass`, results and manifest `4f53cda18c2b`; `bin/status` reads `layout: new`, 23 tracked `current`; `bin/check-links --tree` exits 0 (80 links in 23 files).

- **Left in place by the tool:** nothing (`docs/methodology/` is empty, and git drops an empty directory). **Prose the tool reports and does not rewrite:** `other` 21 mentions in 4 files, `ledger` 329 mentions in 3 files (a committed entry is never edited), `hooks` 15 mentions in the hook itself, `ci`, `tests`, `proofs`, `scripts`, `config` and `harness` all 0.
- **`CLAUDE.md`: 14 replacements on 8 lines, 3 of them inside the project's `### Project-specific Learnings`** (lines 215, 223, 228). Read: each is a pointer rewritten to the file's new path (`methodology/SESSION_RUNNER.md`, `methodology/CHANGELOG.md`, `methodology/FRAMEWORK_LEARNINGS.md`), none states where a file is or was, so **F16 stays declined** (the count there is now 17 + 3).
- **The non-tracked files:** `dashboard.html` (a plain move to `methodology/`) and `__pycache__/methodology_dashboard.cpython-310.pyc` (not moved) have the **same sha256 before and after** ([`before`](p16-adopter-runs/real-nontracked-hashes.before.txt), [`after`](p16-adopter-runs/real-nontracked-hashes.after.txt)); `.git/info/exclude` was not touched; the real tree reads 0 status lines.
- **The dashboard reads 49 before and 45 after** (Documentation 8/20 to 4/20; Risk "High+" 1 both times, from `SESSION_NOTES.md`'s read-cap row, which the older dashboard did not emit: base read 0). The cause is §6.

## 5. The finding the tool's checks did not see: its ledger entry in an example block (F21)

`bin/migrate-layout`'s `insert_entry` (`bin/migrate-layout:362-376`) puts the entry above the first line matching `^## YYYY-MM` or `^### YYYY-MM-DD · ` anywhere in the file. In this ledger the first such line is the **example** `### 2026-01-15 · [ad hoc] Ship the export-retry fix`, inside the code fence of the header's "How to add an entry" section (the v3.7 seed text). **Result in every apply arm: the tool's entry sat at line 48 of the moved ledger, inside that fence** ([`f21-entry-inside-the-fence.txt`](p16-adopter-runs/f21-entry-inside-the-fence.txt)): the example block was corrupted and the migration read as documentation, not as an entry. No check saw it: `check-ledger` reads 83 findings before and after, and `check-handoff`, `bin/status`, `check-links` and the tool's own checks read the same.
**Measured over every committed ledger on this machine** (12: the five adopters already moved read at the commit before their move, the others at HEAD; two directories have none): **only this one has a fence before its first dated heading**; the other 11 read a month heading or a dated entry outside any fence. So the defect touched one of the six adopters moved so far and none of the remaining ones; `bin/migrate-layout` is canonical-only, so no adopter receives it.
**What was done:** he chose "apply, correct there, tool later". A rehearsal clone first showed that moving the entry to just below `<!-- Entries go below, newest on top. -->` passes the layout-aware hook (exit 0) and leaves `check-ledger` at 83; the real correction `0a8ef90` did the same, unedited, with its own ledger entry. The ledger header (everything before the marker) is **identical** to the control's, and the tool's entry is below the marker (fresh-clone check, §7).

## 6. The dashboard's 4 points (F22)

The 49 to 45 is the Documentation dimension: `docs/ (29 files)` counted before, nothing after (`docs/` held only the moved manual, so the directory is gone). **The plan stated this cost at P5** (§7.2d: *"a project with no `docs/` of its own loses the 4-point `has_docs_dir` credit when it migrates (pinned)"*); this is its first measured instance, and P14's `church_growth` (49 and 49) kept other documents under `docs/`. Nothing broke; the diff of the two dashboards is in [`rehearsal-dashboard-ctrl-vs-tall.diff`](p16-adopter-runs/rehearsal-dashboard-ctrl-vs-tall.diff). A stated cost, not a defect.

## 7. Phase 0 in the new layout (a fresh clone of `0a8ef90`)

[`final-clone-log.txt`](p16-adopter-runs/final-clone-log.txt): `methodology/SESSION_RUNNER.md` and `methodology/SAFEGUARDS.md` byte-identical to canonical; `methodology/SESSION_NOTES.md` has its `## ACTIVE TASK` (`:9`); `git status` reads 0 lines; the `CHANGELOG.md` frontier is HEAD (0 undocumented commits) and the `HANDOFFS.md` frontier is `ebbfabd`, one commit behind (the correction), with the project's own S9 receipt still pending, so its next Phase 0 will list both; the committed hook is byte-identical to the canonical one and `--selftest` reads OK, 43 checks; later commits through it: tracked content with no ledger entry **exit 1**, with an entry at `methodology/CHANGELOG.md` **exit 0**, an edit of a committed entry **exit 1** (`removed ### 2026-10-11 · [ad hoc] Sync the methodology files ...`).

## 8. Not shown

- **A push or CI:** there is no remote and no CI.
- **Another clone's hook arming:** none is known to exist (no remote).
- **An adopter session after the move:** its next Phase 0 will be the first by an agent that reads the relocated runner there, and the first to meet its own pending S9 claim.
- **`quality_ratchet.py` or the dashboard in the real tree:** both write there; they ran in clones.
- **The adopter's S9 and BL-15 (`SESSION_NOTES.md` split):** the project's own work; neither was touched.

## 9. The operator's

- **F21's tool fix** (skip fenced blocks in `insert_entry`, or insert after the marker): open, his call; 11 of the other 12 ledgers read are unaffected.
- **The adopter's pending S9 claim** (BL-6, a delivery-packet verdict): its next session reconciles it.
- **Which adopter next:** `mts-system` and `vscode_quarto_ext` (a session each at S297's Phase 0), `Philippians` (his uncommitted `sermons/03-joy-in-knowing-christ.*` edits), `dalia_martinez_funeral` (6 changed files), `claude_work` (no commit), `wsfct` last.
