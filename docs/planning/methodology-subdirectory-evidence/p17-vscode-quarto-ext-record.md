# BL-101 P17 — the seventh adopter, `vscode_quarto_ext` (S298, 2026-10-11)

Plan: [`methodology-subdirectory-plan.md`](../methodology-subdirectory-plan.md) §7.4 (the per-adopter DONE list), §7.6 (the register is read first). **His picks:** at S298's Phase 0 "P17 on vscode_quarto_ext" (the only adopter with no live session and a clean tracked tree) with two go-aheads, both done before the claim (a push of `0a2921d` to the fork, the owed HANDOFFS trim); after the rehearsal, three more at one picker: **tier all**, **a local exclude for the 66 GB untracked `scratchpad/`, removed after**, and **run it, three local commits, no push**.
**Nothing was pushed, tagged or sent upstream.** The adopter's three new commits are local (`master` is 3 ahead of `origin/master`); its push is its own go-ahead. Raw outputs: [`p17-adopter-runs/`](p17-adopter-runs/); the scripts are [`p17-rehearsal.sh`](p17-rehearsal.sh) and [`p17-final-clone.sh`](p17-final-clone.sh) (set `SCRATCH` to a path **without** the word `scratchpad`, F23).

## 1. What was done in the adopter

| Step | Commit there | Result |
|---|---|---|
| Start | `507b9348` | `master`, 430 tracked files, 1,729 commits, level with `origin/master`, legacy layout. A VS Code extension (TypeScript, vitest, esbuild). **No hook** (`core.hooksPath` unset, `.git/hooks` empty), **no CI**; two declared gates (`ledger-lag`, and `release-gate` = `npm run check-package`, a deny-by-default list of what the `.vsix` may contain). One untracked path: `scratchpad/`, **66 GB**, deliberately not in its `.gitignore` (its Session 174 decision: the `?? scratchpad/` line is its only signal) |
| Tree prepared | none (`.git/info/exclude`) | `/scratchpad/` appended for the run, the file restored from a copy afterwards: sha256 `321dffcb…` before and after; `git status` read 0 lines during, `?? scratchpad/` again after |
| `.vscodeignore` | `9a53b909` | the one block that denies `methodology/**` (§3), with a ledger entry in its own format; 2 files |
| `bin/sync`, from this checkout at `8df554b` | `a5b0ed9d` | **21 files updated, `.gitattributes` created**, 2 unchanged, 6 seeds left as written; **no file refused, no `--force`** (F7 and F19 did not arise); 23 files in the commit |
| `bin/migrate-layout --tier all --apply --trailer` | `e35d1657` | the dry run read first (exit 0, no refusal, no warning, the rehearsal's 36 moves plus the 2 ignored files only the real tree has); the commit has **36 renames (33 at 100%, `.context-budget.json` 92%, `.quality-gates.json` 96%, `CHANGELOG.md` 99%) and `CLAUDE.md`** (21 lines); `dashboard.html` and `.quality-gates-results.json` (ignored) moved plainly |

The trailer is `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`. No Claude session was running in the adopter at any check (`pgrep` and `lsof` on each `claude` process's cwd: Phase 0, the claim, before each of the three commits and the dry run).

## 2. The rehearsal, and what it decided

[`p17-rehearsal.sh`](p17-rehearsal.sh) ran six `--no-local` clones at `507b9348`, serially, with `node_modules` and `dist/` APFS-cloned in (`/bin/cp -Rc`). Run 2 is the record; run 1 ([`rehearsal-run1-log.txt`](p17-adopter-runs/rehearsal-run1-log.txt)) carried a needless `.gitattributes` line in `.vscodeignore` (the sync alone leaves `check-package` at 42 files) and is kept.

| Arm | `npm test` | `check-package` | ratchet | `vsce ls` |
|---|---|---|---|---|
| `base` (now) | 68 files, 4,583 pass | OK | 2/2 | 42 paths |
| `ctrl` (synced) | same | OK | 2/2 | 42 |
| `t1` (tier 1, as the tool leaves it) | same | **FAIL**: 65 files, 6.67 MB, `methodology` unexpected (23) | 1/2 | 65 |
| `tall` (tier all, as the tool leaves it) | same | **FAIL**: 78 files, 9.90 MB, `methodology` unexpected (36) | 1/2 | 78 |
| `t1A`, `tallA` (+ `methodology/**` first) | same | OK, 42 files, 5.66 MB | 2/2 | 42, identical to `base` |

A real `vsce package` in `base` and `tallA` gives **44 entries and 1,935,373 B each, entry lists identical**; the fresh clone of the real result gives the same (§6). Not run: `test:integration` and `test:lsp` (each needs a downloaded VS Code; `.vscode-test/` is 21 GB).

## 3. The finding the tool's checks did not see (F20 again, and F24)

Every check the tool prints reads the same in all six arms (§4), and **the project's own `release-gate` goes red at both tiers**: vsce matches `.vscodeignore` without `matchBase` (F11), so the bare names it lists (`SESSION_RUNNER.md`, `CHANGELOG.md`, ...) cover the root and `methodology/` is packaged whole. **No test saw it** (4,583 pass in every arm); the declared gate did, as `nprcgenekeepr`'s tarball gate did at P15 (F20). The tool lists the file under `config` (`.vscodeignore:43`, 26 to 27 mentions, F11's fix) and cannot say what the move does to it: it evaluates `.Rbuildignore` as R reads it (F10) and `.vscodeignore` not at all (**F24**). The adaptation is one block, committed before the move (`9a53b909`):

```
# Methodology files live under methodology/ after the layout move (methodology repo BL-101, P17). vsce matches
# these patterns without matchBase, so the bare names above cover the project root only: without this line
# `npm run check-package` reads 78 files against 42 and the release-gate fails (measured in clones, 2026-10-11).
methodology/**
```

## 4. The tool's checks, and the adopter's own, before and after

Identical in `base`, `ctrl` and every moved arm: `bin/status` 23/23 `current`; `check-ledger` exit 1, **78 findings** (the adopter's own heading forms, none the tool's); `check-handoff` exit 1 (3 issues in its newest receipt and 45 unreconciled `commit:` slots, its own); proofs 2 and 2 at tier all; `git log --follow` 483 to 484; clean tree; **dashboard 76/100, High+ risk 1 in every arm**. `links`: **tier 1 0 to 4** (the four seeds the tier does not move, F13) and **tier all 0 to 18 project links** dangling, none in a framework document (F9, by design; **6 of the 18 sit in a ledger header** (the trimmer's pointer blocks and one link to the moved manual), 12 in the body of a ledger). `CLAUDE.md`: 29 replacements on 21 lines, **none in its `### Project-specific Learnings`** (a 10-line pointer to `PROJECT_LEARNINGS.md`), so F16 stays declined; 22,524 B to 22,855 B against its 28,000 B ceiling.
**Already red at the start and unchanged** (the adopter's own): `context_budget.py --status` exit 2, `HANDOFFS.md` 304,808 B, `BACKLOG.md` 384,251 B and `PROJECT_LEARNINGS.md` 1,108,514 B against 65,536 B each. **The `ledger-lag` gate follows the ledger:** the tool rewrote its command to `methodology/CHANGELOG.md` (2 replacements in `.quality-gates.json`); in a fresh clone a later commit with no ledger entry reads 1 (fail) and one with an entry reads 0, before the move (root ledger) and after it (no fail-open, unlike F2's hooks).

## 5. The scratchpad (F12)

The tool counts every untracked file as dirt (`dirty_paths`, `bin/migrate-layout:117`, `--untracked-files=all`), and the project leaves `scratchpad/` unignored on purpose, so its `.gitignore` was the wrong place. A **local exclude** is the remedy F12's record names; with it `git status --untracked-files=all` took 0.014 s. **Not measured:** the tool's behaviour without it (avoided: S295 measured a 64 MB listing for a smaller instance of this shape). **Not run in the real tree:** `check-package` and the ratchet (vsce would walk the 66 GB; the project's own S297 commit message mentions a "timeout disclosure" for its ratchet run, which I did not read): the gates ran in clones and in a fresh clone of the result. **The non-tracked files** (`dashboard.html`, `.quality-gates-results.json`, `__pycache__/quality_ratchet.cpython-310.pyc`) have the **same sha256 before and after** ([`before`](p17-adopter-runs/real-nontracked-hashes.before.txt), [`after`](p17-adopter-runs/real-nontracked-hashes.after.txt)).

## 6. Phase 0 and the gates in the new layout (a fresh clone of `e35d1657`)

[`final-clone-log.txt`](p17-adopter-runs/final-clone-log.txt): `methodology/SESSION_RUNNER.md` and `methodology/SAFEGUARDS.md` byte-identical to canonical; `methodology/SESSION_NOTES.md` has its `## ACTIVE TASK` (`:10`); `git status` 0 lines; both ledger frontiers are HEAD (0 undocumented commits, 0 merges); the tool's entry is at `methodology/CHANGELOG.md:20` with 0 code fences before the first dated heading (F21 did not arise); `npm test` 68 files and 4,583 pass; `check-package` OK, 42 files; `check-backlog` and `check-types` exit 0; **ratchet 2/2**; `vsce ls` 42 paths in both, 0 lines differ; `vsce package` **44 entries, 1,935,373 B**; `bin/status` `layout: new`, 23 current; later commits through `ledger-lag`: 1 (no entry), 0 (entry). The `HANDOFFS.md` receipts, the `SESSION_NOTES.md` shard (`docs/archive/SESSION_NOTES-through-S253.md`, whose proof exits 2 at the new place) and the project's `docs/archive/README.md` stay where they were.

## 7. Not shown

- **A push or CI:** the commits are local and the project has no CI; **another clone's hook arming:** none exists.
- **`test:integration`, `test:lsp`, `observe:posit`:** each launches a VS Code window and needs the 21 GB download; the project's CLAUDE.md asks for the operator's go-ahead before either.
- **An adopter session after the move:** its next Phase 0 will be the first by an agent that reads the relocated runner there.
- **`scratchpad/`'s contents:** not read, listed or moved.

## 8. The operator's

- **F24:** whether the tool evaluates `.vscodeignore` as vsce does (F10's `.Rbuildignore` rule is the precedent: it was chosen, built and held by tests) or this stays an adopter's own commit, as here; plan §7.6 says a finding the tool's checks did not see goes before the next adopter unless he chooses otherwise.
- **The adopter's push** (its three commits, `origin` exists, no CI) and **its own mandatory reads** (`HANDOFFS.md`, `BACKLOG.md`, `PROJECT_LEARNINGS.md` far over their ceilings, the S297 timeout disclosure): the project's own work.
- **Which adopter next:** `mts-system` (a session running at S298), `Philippians` (dirty), `dalia_martinez_funeral` (dirty), `claude_work` (no commit), `wsfct` last.
