# BL-105 — does `PROJECT_LEARNINGS.md` join the `methodology/` set? (S301, 2026-10-12)

Plan: [`methodology-subdirectory-plan.md`](../methodology-subdirectory-plan.md) §1 and D1 (§9). Backlog row BL-105. **Read-only session:**
no tool, distributed document or adopter was changed. Canonical repository at `92a76b6`; the adopters at their working trees on 2026-10-12
(`wsfct`, `mts-system` and `nprcgenekeepr` have a live session, so only `git grep` and `git ls-files` ran there). **His questions (S298):**
why is `nprcgenekeepr`'s `PROJECT_LEARNINGS.md` not in `methodology/`; give an argument other than "it is not in the manifest"; is it a file
that would typically exist in non-methodology use of Claude Code.

## 1. His two questions, answered

**Is it a file Claude Code users typically have? No.** (a) The name's first appearance in this repository's whole history, all branches
(`git log --all -S`), is `1999f4a` (2026-06-06, "extract Learnings to PROJECT_LEARNINGS.md when it grows", upstream issue #26): no earlier use here,
which fits the framework having coined it. (b) `starter-kit/BOOTSTRAP.md:218-222` defines it as where the Phase 3C Learnings table goes when it outgrows `CLAUDE.md`, the
project-side twin of `FRAMEWORK_LEARNINGS.md` (which moves). (c) All five adopters' files open with that provenance: "Migrated verbatim from
`SESSION_RUNNER.md`'s Learnings table" (`model_project_constructor`, `mts-system`, `wsfct`), "Extracted verbatim from `CLAUDE.md` to keep it
within its size budget" (`nprcgenekeepr`), "the append-only table of project-specific learnings accumulated at each session's Phase 3C
close-out" (`vscode_quarto_ext`). That Claude Code itself names only `CLAUDE.md` is my knowledge of the product, not something measured here.

**An argument other than the manifest.** The test: *would this file exist, under this name, if the project had never adopted the framework?*
`CLAUDE.md`: yes (Claude Code loads it from the root), so it stays. `CONTEXT.md`: yes (the third-party `/grill-with-docs` skill maintains
it; the skill's own expected location was not read), so it stays. `BACKLOG.md`: a backlog exists anyway, and the shipped dashboard reads it
(§2). `PROJECT_LEARNINGS.md`: no. **The counter-argument, in full:** `CHANGELOG.md`, `HANDOFFS.md`, `SESSION_NOTES.md` and `ROADMAP.md` are
also project-written content and they moved, so "project-owned" does not separate this file from them. What separates it is only that the
framework seeds them; for a leave-at-the-root answer the non-circular support is **cost** (§3), not principle.

## 2. The census (what the backlog row listed as not measured)

| Adopter (layout) | Bytes | Tracked files naming it, apart from itself | Of those, ledger- or archive-shaped | Path literals a program reads (outside `.md`, `.jsonl`) |
|---|---|---|---|---|
| `model_project_constructor` (new, tier 1) | 411,884 | 38 | 17 | 1: `tests/test_read_budget.py:64` |
| `mts-system` (legacy) | 265,780 | 34 | 7 | 3: `.context-budget.json:54`, `scripts/learnings_archive.py:30`, `scripts/test_learnings_archive.py:23` |
| `nprcgenekeepr` (new) | 3,230,644 | 143 | 60 | 7: `.Rbuildignore:70`, 4 workflows' `paths-ignore`, `tests/testthat/test_workflowPathsIgnore.R:39`, `vignettes/articles/data-raw/build-document1-evidence.R:186` |
| `vscode_quarto_ext` (new) | 1,108,514 | 33 | 5 | 2: `methodology/.context-budget.json:61`, `.vscodeignore:56` |
| `wsfct` (legacy) | 1,123,065 | 107 | 20 | 1: `.context-budget.json:51` |

- **The other seven of the 12 adopters carry none.** `BACKLOG.md` is tracked in 11 of 12 and `CONTEXT.md` in 5.
- **Most mentions are citations by name** (`PROJECT_LEARNINGS #109`), which a move leaves true. The 14 path literals sort three ways: **3 are
  `.context-budget.json` paths** the migration tool rewrites for a file in its move set; **6 already hold when the file moves** (`nprcgenekeepr`'s
  `.Rbuildignore` has `^methodology$` and all four workflows ignore `methodology/**`, so its tarball and CI do not change; `vscode_quarto_ext`'s
  `.vscodeignore` has `methodology/**` since P17); **5 need a hand edit**: `model_project_constructor`'s test (1, likely; not run),
  `mts-system`'s own archiver and its test (2: the archiver matches the config path by equality, which the config rewrite would change),
  `nprcgenekeepr`'s R script and its test list (2).
- **Markdown links to it:** 124 in 22 files, 14 of them live and 8 ledger-shaped (`model_project_constructor` 111 in 11 files, 6
  ledger-shaped; the rest 1 to 5 each). A committed ledger entry is never edited (plan C6), so those dangle after a move, as F9 did at tier 2.
- **No shipped tool reads it.** `git grep` over `starter-kit/*.py`, `tools/methodology_dashboard.py` and `bin/*` finds one hit,
  `bin/check-links:84` (its list of project-owned files); the distributed prose is `BOOTSTRAP.md:218,220,222,439` and `CLAUDE_TEMPLATE.md:83`.
- **`BACKLOG.md` is read by a shipped tool:** `starter-kit/methodology_dashboard.py:304` looks in `BACKLOG.md`, `docs/BACKLOG.md` and
  `docs/planning/BACKLOG.md` and scores it 15 points (`:202`), in two byte-identical copies. **`CONTEXT.md`** is read by no tool
  (`bin/check-links:81` only).
- **The manifest has two dispositions only, `TRACKED` and `SEED`** (`bin/_manifest.py:44-45`), and a seed is "created if absent": an entry for
  this optional file would put an empty one in every adopter. An optional entry needs a third disposition, a schema change to a file upstream
  merged under a constraint (PR #91: literal data, one plain assignment per name) and read by `bin/_manifest_reader.py`.
- **On an already-migrated tree the tool stops:** `bin/migrate-layout` on a `--no-local` clone of `vscode_quarto_ext` at `e35d165` prints
  "nothing to migrate: no methodology file is left to move". Three of the five adopters that carry the file are in that state, so a move needs a new top-up mode or three hand moves.

## 3. The options and what each costs

| | What it is | Canonical-side cost | Adopter-side cost (measured sites) | Reverses |
|---|---|---|---|---|
| **A** | Keep D1; state the boundary in plan §1 as "the framework seeds it, a project's own optional file stays at its root" | one plan edit | none | any later move costs the same as B |
| **B** | Move it as a **companion of the move**, not a manifest entry: `bin/migrate-layout` moves a project-owned `PROJECT_LEARNINGS.md` when present and rewrites the `CLAUDE.md` pointer; the distributed prose says "beside `FRAMEWORK_LEARNINGS.md`" (layout-neutral, as P9's bare-name rule) | `BOOTSTRAP.md` (4 lines), `CLAUDE_TEMPLATE.md` (1), `bin/check-links` (1), `bin/migrate-layout` (a companion rule, a top-up mode), tests and gate floor; no manifest change; an upstream pull request carries the doc and tool edits (D8) | 5 hand-edit sites in 3 adopters, 3 config rewrites by the tool, 6 sites already hold; one move per adopter, 3 as top-ups | a move back is the same cost |
| **B-manifest** | B, but as an optional manifest entry | B plus a third disposition across `_manifest.py`, its reader, `bin/sync`, `bin/status`, the dashboard's installed-source tuple and their tests | as B | not recommended: the schema change buys nothing B does not |
| **C** | B plus `BACKLOG.md` (and `CONTEXT.md`) | B plus the dashboard's three backlog locations, its scoring and tests, and a second copy | `BACKLOG.md` is in 11 of 12 adopters, 3 of them over 100 KB; not counted | not recommended: a different plan, and `CONTEXT.md` has an outside reader |

**Recommendation: B**, because it is the only option whose boundary rests on a reason other than the manifest and it needs no schema change;
**its first build phase is a rehearsal on a `--no-local` clone of `nprcgenekeepr`** (the worst case: 3.2 MB, 143 names), and the decision can
still be withdrawn at that result. The cost figures above are a census of references, **not a rehearsal**.

## 4. Not measured, not run

No move was rehearsed on any adopter. Not run: `model_project_constructor`'s `tests/test_read_budget.py` against a moved file; how many of its
111 links sit in live files; the skill `/grill-with-docs`'s own expected location of `CONTEXT.md`; adopters outside the 12.

## 5. His answer

*(Recorded after the S301 picker.)*
