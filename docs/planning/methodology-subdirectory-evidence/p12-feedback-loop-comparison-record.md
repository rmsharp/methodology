# BL-101 P12 — the second adopter, `feedback-loop-comparison` (S287, 2026-10-08)

Plan: [`methodology-subdirectory-plan.md`](../methodology-subdirectory-plan.md) §4.6 (two tiers), §7.4 (the per-adopter DONE list), D1, D9. He chose `--tier all` at the Phase 0 picker; the S286 survey had found no file in this adopter that reads a moved path.
**Nothing was pushed, tagged or sent upstream.** The adopter has no git remote, so there is no push and no CI to run. Its three new commits stay in its own repository. Raw outputs: [`p12-adopter-runs/`](p12-adopter-runs/); the two scripts that ran the rehearsal and the final check are [`p12-rehearsal.sh`](p12-rehearsal.sh) and [`p12-final-clone.sh`](p12-final-clone.sh) (set `SCRATCH`).

## 1. What was done in the adopter

| Step | Commit there | Result |
|---|---|---|
| Start | `cda76db` | clean, `main`, 8 commits, 33 tracked files, **no remote, no `core.hooksPath`, no tests, no CI**; framework files in the legacy layout (`docs/methodology/` holds the manual and workstreams) |
| `bin/sync --force`, from this checkout at `c2cdbfd` | `8ce4ed6` | 11 files updated, 16 created, 28 files changed (the 27 and its ledger entry); `--force` was needed for two files (§2) |
| `bin/migrate-layout --tier all --apply --trailer` | `40d2b74` | 32 files changed, +17 −13: 30 renames (27 at 100%, 94% and 97% for three), `CLAUDE.md` (11 replacements), `.gitignore` (1), `.context-budget.json` (3), `.quality-gates.json` (1), one ledger entry the tool wrote; the untracked, ignored `dashboard.html` moved plainly |
| A ledger correction of mine | `2e77a73` | the sync entry's "9 lines" is 10 by `diff` (§2); a new entry above it, since a committed entry is not edited; four lines, no file moved |

The checkout synced from is `c2cdbfd`; its distributed files are those of `add55f1` (`git diff --stat add55f1 c2cdbfd -- bin tools starter-kit .githooks` lists only `bin/migrate-layout` and `tools/test_migrate_layout.py`, both canonical-only). The sync was committed as one commit with its own hand-written ledger entry (`BOOTSTRAP.md`'s rule); this adopter's `CLAUDE.md` states no commit rule of its own. `bin/status` read **23 of 23 tracked files `current`** after the sync and at the new places after the move (`layout: new`).

## 2. What `--force` overwrote

`bin/sync` refused without it: `SESSION_RUNNER.md` and `docs/methodology/workstreams/RESEARCH_DOCUMENTATION_WORKSTREAM.md` matched no canonical or historical version. Both files have one commit in the adopter (the 2026-05-08 scaffold). Matched against every version this repository holds:
- **`SESSION_RUNNER.md`:** nearest `274dcd4` (2026-04-16), 3 lines differ: a table row mapping "Write/draft/audit [paper...]" to the research workstream, and a paragraph, "Multi-session campaign check", written for `*_PROTOCOL.md`. The current runner carries both (as `*_CAMPAIGN.md`).
- **The research workstream:** nearest `b1ba27e` (2026-04-25), 10 lines differ by `diff`, **all of them lines the adopter's copy lacks** (a "Phases Covered" section, a calibration note and a cross-reference note); it adds nothing of its own. (The matcher script that picked the version counted 9 and I wrote 9 into the adopter's sync entry; it is corrected in `2e77a73`.)
- This project's own adaptations are in its `CLAUDE.md`, which `bin/sync` does not touch. **Not checked:** other canonical history this repository does not hold (the nearest-version search ran over this repository's commits only).

## 3. The adopter's own build, at each state

Its build equivalent (`SAFEGUARDS.md`; there are no tests or proofs) is `quarto render index.qmd`, HTML and PDF, run with Quarto 1.7.33 in `--no-local` clones, never in the real tree.

| State | Render exit | Warnings | HTML sha256 (first 12) | PDF text sha256 (first 12) |
|---|---|---|---|---|
| base: the adopter at `cda76db` | 0 | 0 | `c3844843ba3b` | `0c405cac9438` |
| ctrl: synced | 0 | 0 | `c3844843ba3b` | `0c405cac9438` |
| tier 1 (rehearsal) | 0 | 0 | `c3844843ba3b` | `0c405cac9438` |
| tier all (rehearsal) | 0 | 0 | `c3844843ba3b` | `0c405cac9438` |
| **the real `40d2b74`, a fresh clone** | 0 | 0 | `c3844843ba3b` | `0c405cac9438` |

The PDFs differ in bytes (145,669 for three arms, 145,666 for tier 1) and not in text. The build never reads a path the move changes: `index.qmd` and `references.bib` name other repositories' files, as citations.

## 4. The tool's own checks, and what tier 2 costs here

| Check | Rehearsal, tier 1 | Rehearsal, tier all | Real apply (tier all) |
|---|---|---|---|
| `bin/status` tracked `current` | 23/23 → 23/23 | 23/23 → 23/23 | 23/23 → 23/23 |
| `check-ledger` | exit 1 → 1 | exit 1 → 1 | exit 1 → 1 |
| `check-handoff` | 0 → 0 | 0 → 0 | 0 → 0 |
| `check-links`, framework documents | 0 → 0 | 0 → 0 | 0 → 0 |
| `check-links`, the project's own files | 4 → 4 | 4 → 23 | **0 → 23** |
| history by `git log --follow` | 5 → 6 | 5 → 6 | 6 → 7 |

- **The 23 are in `methodology/SESSION_NOTES.md`:** relative links (`docs/research/...`, `index.qmd`, `references.bib`, `index.html`, `index.pdf`, `_quarto.yml`, one `docs/methodology/workstreams/...PROTOCOL.md`) written when the file sat at the root. The tool reports and never edits a committed entry (S284). They are the cost of moving that file; tier 1 leaves it. The clone's 4 "before" are the two rendered files the clone does not have; the real tree has them untracked, so its "before" is 0.
- **`check-ledger` exit 1 is not the move.** The adopter's `CHANGELOG.md` has 4 findings before and after, from its older format: three headings without the `### YYYY-MM-DD · ` prefix and one paragraph outside any entry. `bin/status` marks the file `present (stale format)`; migrating it is adopter-owned (`BOOTSTRAP.md`).
- **The tool's entry landed at the end of that ledger,** after the oldest entry, because the file has no month heading; the sync's hand-written entry is above the `## [v1.0]` heading. The ledger now has two orders.
- **Left in place by the tool:** `docs/methodology/README.md` and three `*_PROTOCOL.md` files (older copies the manifest no longer names). Prose it reports and does not rewrite: 93 mentions in 9 files (`other`) and 72 in 3 ledger files. The two that now mislead a reader: `README.md:21` ("read `SESSION_RUNNER.md`") and the directory sketch in `PLAN.md:99-107`.

## 5. Phase 0 in the new layout (a fresh clone of `40d2b74`)

`methodology/SESSION_RUNNER.md` and `methodology/SAFEGUARDS.md` are byte-identical to canonical and sit where the runner says; `methodology/SESSION_NOTES.md` has its `## ACTIVE TASK` (`:7`); no remote, so no `gh issue list`; `git status` clean; `python3 methodology/methodology_dashboard.py --no-open` health **59, risk 0**, the same as the same tool on a clone of `8ce4ed6` (synced, before the move): 59 and 0. (The rehearsal clones read 52 and 1 in all three synced arms, run after the render; why was not investigated, and it is the same across arms.) The `CHANGELOG.md` frontier and the `HANDOFFS.md` frontier are both `40d2b74`, 0 undocumented. The dashboard starts a new history under `methodology/` (`dashboard_history.jsonl`, untracked in that clone).

## 6. Not shown

- **Any CI or push:** there is none. Another clone's hook arming: the adopter has no hooks.
- **The adopter's `.claude/settings.local.json`** (untracked): it names no moved path.
- **A render in the real tree:** the renders ran in clones, so the real tree's own `index.html` and `index.pdf` are still the 2026-05-08 ones.
- **The adopter's own later sessions:** its next Phase 0 will be the first by an agent that reads the relocated runner on a machine other than this one.

## 7. The operator's

- **Two lines of prose in the adopter** now point at the root: `README.md:21` and `PLAN.md:99-107` (a locked plan's file sketch). A one-line fix to the first would be its own commit there.
- **The ledger's order and format** (§4): migrating it to the current seed header is the adopter's, not the tool's.
- **Whether tier all is the default for the next adopter.** Here it cost 23 links in the project's own notes and nothing the build reads; at P11 it cost 41 tests and 2 proofs. Three of the four adopters the survey found with no file reading a moved path remain (`airqino`, `Philippians`, `vscode_quarto_ext`); that is where it should cost least, and the survey's own caveat holds (a zero is the strong result, a hit an upper bound).
