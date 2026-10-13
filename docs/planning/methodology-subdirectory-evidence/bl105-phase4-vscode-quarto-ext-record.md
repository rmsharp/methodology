# BL-105 build phase 4 — the companion top-up at `vscode_quarto_ext` (S309, 2026-10-13)

Plan [`methodology-subdirectory-plan.md`](../methodology-subdirectory-plan.md) §7.4 (the per-adopter DONE list) and D10; backlog row BL-105 ([`BACKLOG.md`](../BACKLOG.md), [detail](../BACKLOG-DETAIL.md#bl-105)); the tool is [`bl105-phase2-record.md`](bl105-phase2-record.md), the prose [`bl105-phase3-record.md`](bl105-phase3-record.md); the adopter's first move is [`p17-vscode-quarto-ext-record.md`](p17-vscode-quarto-ext-record.md). **His pick at the S309 Phase 0 picker**, and his two earlier messages ("ready for the methodology file move" and "I will clean up `vscode_quarto_ext` while you work"). Written after the work; every figure was read from a command's output in this session (raw outputs in [`bl105-p4-vscode-runs/`](bl105-p4-vscode-runs/); scripts [`bl105-p4-vscode-rehearsal.sh`](bl105-p4-vscode-rehearsal.sh), [`bl105-p4-vscode-rehearsal-edit.sh`](bl105-p4-vscode-rehearsal-edit.sh), [`bl105-p4-vscode-final-clone.sh`](bl105-p4-vscode-final-clone.sh); clones lived under `~/.cache/s309-rehearsal`, a path without the word `scratchpad`, F23).

## 1. The answer first

**Done at the adopter, three local commits, nothing pushed:** `bin/sync` (`f89ac407`), one phrase of its own `CLAUDE.md` (`741f8aad`), then `bin/migrate-layout --apply` (`2057838c`: `PROJECT_LEARNINGS.md` renamed into `methodology/` at 100%, 6 occurrences of the name rewritten in `CLAUDE.md`, 1 in `methodology/.context-budget.json`, one ledger entry). `master` reads 76 ahead of `origin/master` (73 before). **The move was one file, not three.** The three the S308 handoff counted came from a *refused* dry run (F32): once the sync cleared the refusal, the tool rehearsed the shard's proof, found it exits 2 at the new place, and left `docs/archive/SESSION_NOTES-through-S253.md` and its `.verify.sh` where they are (as P17 had left them).

**The project's own checks read the same before and after**, in a fresh `--no-local` clone of the real HEAD: 70 test files and 5,155 tests pass, `npm run check-package` OK (42 files, 5.68 MB), `vsce ls` 42 paths with **0 lines different** from the base, `vsce package` **1,940,709 B and 44 entries** with the same entry list, the ratchet 2/2 (results `bba236856bad`, manifest `334939914945`), `check-backlog` and `check-types` exit 0, dashboard 76/100 with 1 high risk. **One finding no check of the tool sees was fixed by the adopter's own commit first (F33):** the rewrite left "(project root, committed)" beside `methodology/PROJECT_LEARNINGS.md` in an auto-loaded file.

## 2. What was done in the adopter

| Step | Commit there | Result |
|---|---|---|
| Start | `0c8d9669` | `master`, 73 commits ahead of `origin/master`; **no session in the project** (`pgrep` and `lsof` on every `claude` process's cwd, before each commit); tree clean (his Session 302 left a local `.git/info/exclude` for `scratchpad/`, untouched here); `bin/status` 23 tracked files, 5 not current: the runner, `CLAUDE_TEMPLATE.md`, `BOOTSTRAP.md`, `HOW_TO_USE.md` (1 version each) and `quality_ratchet.py` (3) |
| `bin/sync`, from this checkout at `a9e550f` | `f89ac407` | dry run first: exactly those 5 would write, 7 seeds `present (seed; left as-is)`, nothing refused, **no `--force`** (F7 and F19 did not arise); 6 files in the commit with its ledger entry |
| `CLAUDE.md` one phrase | `741f8aad` | `(project root, committed)` to `(committed)` at `CLAUDE.md:263`, asserted to match once; ledger entry in the same commit |
| `bin/migrate-layout --apply --trailer` | `2057838c` | dry run read first (exit 0, no refusal; 1 move, 2 rewrites, 3 left in place); **4 files in the commit: 1 rename at 100%, `CLAUDE.md` (10 lines), `.context-budget.json` (1), `CHANGELOG.md` (the tool's entry)**; the tool's checks before to after: status 23/23 current to 23/23, ledger exit 1 to 1, handoff exit 1 to 1, links 18 project dangling to 18, proofs 0 to 0, history 505 to 506 commits through `git log --follow`, clean tree |

The trailer is `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>` (`--trailer` on the apply; the same line on the other two). **Live links:** none (no live Markdown document links to the moved file; F30's list is empty). **The tool's `tests:` (2 mentions in 2 files), `scripts:` (41 in 4 files) and `config:` (1) rows were read** and the rehearsal ran every one of the project's checks: the project's own mentions are comments and message strings (`check-backlog.js:133`, `backlog-hygiene-gate.test.ts:95`, `model.ts:3582`), so F25 to F28 did not arise.

## 3. The rehearsal, and what it decided

Three arms, clones of `0c8d9669` in `~/.cache/s309-rehearsal/p4`, each with `node_modules` and `dist/` APFS-cloned in ([`rehearsal-log.txt`](bl105-p4-vscode-runs/rehearsal-log.txt)); a fourth arm, `edit`, carries the phrase ([`rehearsal-edit-log.txt`](bl105-p4-vscode-runs/rehearsal-edit-log.txt)).

| Arm | `npm test` | `check-package` | ratchet | `vsce ls` | `vsce package` |
|---|---|---|---|---|---|
| `base` (now) | 70 files, 5,155 pass | OK, 42 files | 2/2 | 42 | 44 entries, 1,940,709 B |
| `ctrl` (synced) | same | same | 2/2 | 42, 0 lines differ | n/a |
| `topup` (synced + the tool alone) | same | same | 2/2 | 42, 0 lines differ | 44 entries, 1,940,709 B, entry list identical |
| `edit` (synced + the phrase + the tool) | same | same | 2/2 | 42, 0 lines differ | n/a |

`edit` against `topup`: the file lists are equal and `CLAUDE.md` line 263 and the ledger are the only files that differ. `context_budget.py --status` exits 2 in every arm for the project's own reason (`PROJECT_LEARNINGS.md` 1,139,759 B against 65,536 B), unchanged; the resident class reads 22,855 B at base, 22,841 B after the phrase, 22,913 B after the tool's rewrite, against a ceiling of 28,000 B. `check-ledger` reads 84 findings and `check-handoff` 3 issues in the project's own newest receipt, **the same in `base`, `ctrl` and `head`** (its own). The base reads `[not-current]` and exit 1 from `bin/migrate-layout`, as the real tree did.

**The census held:** the sites the tool lists as machine-read read no program (the one real-path line, `.vscodeignore:56 PROJECT_LEARNINGS.md`, is covered by the `methodology/**` block P17 added; `vsce ls` is identical). The rehearsal's one new fact is F33.

## 4. The final check (a fresh `--no-local` clone of `2057838c`, [`final-clone-log.txt`](bl105-p4-vscode-runs/final-clone-log.txt))

`methodology/SESSION_RUNNER.md`, `SAFEGUARDS.md` and `BOOTSTRAP.md` byte-identical to canonical; `methodology/SESSION_NOTES.md` has its `## ACTIVE TASK` (`:10`); `git status` 0 lines; the CHANGELOG frontier is HEAD (0 undocumented commits, 0 merges), the HANDOFFS frontier is `0c8d966` with 3 commits after it (the three of this phase, each with its ledger entry; the receipts are the project's own sessions'); the tool's entry is at `methodology/CHANGELOG.md:20` with 0 code fences before the first dated heading (F21 did not arise); `git log --follow` reaches 308 commits before the move and 309 after. `PROJECT_LEARNINGS.md` is gone from the root, the shard and its proof **stay and the proof exits 0 at its own place**; `bin/status` `layout: new`, 23 tracked current, 0 not. A later commit with no ledger entry reads `ledger-lag` 1 (fail), with an entry 0 (the gate follows the ledger). `check-links` reads 18 dangling project links before and after (20 lines differ: ledger line numbers moved by the 4 lines of the tool's entry, no new target).

## 5. Findings (rows F32 and F33 of the register)

- **F32 — a refused dry run lists moves the run after the refusal drops.** `bin/migrate-layout:1065` runs `rehearse_shards` only `if moves and not refusals`, so a dry run that is REFUSED prints the pre-rehearsal list: 3 moves at the real tree before the sync, 1 after. The S308 handoff and this session's Phase 0 report said "3 moves" from it. Nothing in the report says the list is unrehearsed. Seen by a check of the tool: no. **Open: his call** (label the list, or rehearse before refusing). Not built: this session is the adopter, and the finding is cosmetic to the result (the apply made the right plan).
- **F33 — the text rewrite makes a sentence that states WHERE the file is false.** `CLAUDE.md:263`: `See [PROJECT_LEARNINGS.md](PROJECT_LEARNINGS.md) (project root, committed)`; the tool rewrote the link and left the parenthesis. This is the first adopter where a rewritten line states a location: F16 was declined on the measurement that every one of the 17 Learnings-region lines it read named a file that exists at its new place (S294), and the BL-105 rehearsal read none that stated where the file was (S302). The tool prints the diff, so a person reads it; no check does. **Fixed for this adopter** by its own commit before the move (`741f8aad`). **F16 stays declined (his); this is a data point against its premise**, in the very region F16 named.

**Seen again:** F2 and F18 (no hooks: `core.hooksPath` unset, `.git/hooks` empty); F7 and F19 (no refusal, no `--force`); F12 (the project's own Session 302 prepared the tree: `scratchpad/` trimmed by 63.7 GB and a local exclude; the tool saw 0 dirt); F20 and F24 (the declared gates, `check-package` and the ratchet, green; nothing to adapt); F23 (clones under `~/.cache`); F29 and F30 (the config rewritten where the layout keeps it, 0 live links); F9 and F13 (18 dangling project links, unchanged).

## 6. Not shown

A push or CI (the commits are local; the project has no CI); `test:integration`, `test:lsp` and `observe:posit` (each launches a VS Code window and needs the 21 GB download; its `CLAUDE.md` asks for the operator's go-ahead first); **the real tree's own gates**, which were not run in it (its `scratchpad/` is untracked and `vsce` would walk it; they ran in clones and in a fresh clone of the result); another clone's hook arming (none exists); an adopter session after the move (its next Phase 0 is the first by an agent reading the relocated file); `scratchpad/`'s contents (not read, listed or moved).

## 7. His calls this leaves

- **The adopter's push:** `f89ac407`, `741f8aad`, `2057838c` (3 commits, local; `origin` exists, no CI). It is the project's own go-ahead.
- **The local exclude** at the foot of that clone's `.git/info/exclude` (`scratchpad/`, with the note "remove this line after the layout migration"): **left in place**, because taking it out is a non-commit action that the project's ledger records (his Session 302 recorded the adding), and recording it means another commit in his repository. The migration is done, so the line is his or his next session's to remove.
- **F32:** label the list or rehearse before refusing.
- **F16** (his, declined): whether F33 reopens it.
