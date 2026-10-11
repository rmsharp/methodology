# F12 — the dirty-tree refusal and generated files: measured over every adopter, then declined (BL-101, plan section 7.6, S295)

Row F12 of [`findings-register.md`](findings-register.md) (raised at P13, S291) left one question to the operator: should `bin/migrate-layout` count the generated files it will move (`dashboard.html`, `dashboard_history.jsonl`, `.context-budget-history.jsonl`, `.quality-gates-results.json`) as not-dirt, or should each adopter ignore them before the move? This record is the measurement that answers it and the decision that followed. **The tool did not change.**

## 1. The question, and the estimate that was wrong

At S295's Phase 0 `P15` was blocked again (four adopters with a live `claude` session, three dirty), and the session offered F12 as the deliverable with this reason: *"my estimate, not measured: it would clear the only dirt in `chat_verification` and `mts-system`."* **That estimate was wrong for the rule the row describes.** The row is about *untracked* generated files (`airqino`'s four); the two adopters' dirt is a *modified, tracked* `dashboard_history.jsonl`, which is a different case with a different cost. The measurement below is what showed it; the operator chose F12 on the estimate, then saw the correction and the options before deciding.

## 2. The instrument

[`f12-measure-dirt.py`](f12-measure-dirt.py), run as `python3 -I -B docs/planning/methodology-subdirectory-evidence/f12-measure-dirt.py`; its output is [`f12-measure-output.txt`](f12-measure-output.txt) (2026-10-11). Read-only in every real tree (`git status` is the only command run there). Three parts:

1. **Each adopter's dirt**, by git status code (untracked, or tracked and changed) and by whether the path is one of the tool's own `GENERATED` names, and how many trees each candidate rule would leave clean: **rule A** (untracked generated files are not dirt: what the row describes) and **rule B** (rule A, and a modified tracked generated file is not dirt either).
2. **The tool's own dry run**, in a `git clone --no-local` of `mts-system` and `chat_verification`, with the real modified `dashboard_history.jsonl` copied over the clone's so the clone carries the real dirt: what the refusal says today.
3. **What git does to a modified tracked file** that `git mv` carries and `reset --hard` rolls back, in a scratch repository: the two paths rule B would have to handle.

## 3. The result

| | |
|---|---|
| Adopters on this machine | 12: 4 already moved (`model_project_constructor`, `feedback-loop-comparison`, `airqino`, `church_growth`), 8 not |
| Of the 8 not yet moved: clean trees | `nprcgenekeepr`, `wsfct` (each has a live session) |
| Dirt that is a generated file | `mts-system` and `chat_verification`: **one modified tracked `dashboard_history.jsonl` each**, nothing else |
| Dirt that is not | `vscode_quarto_ext` (1: an untracked `scratchpad/`), `Philippians` (4), `dalia_martinez_funeral` (6), `claude_work` (16; it has no commit at all) |
| **Trees rule A leaves clean** | **0 of 8** |
| Trees rule B leaves clean | 2 of 8 (`mts-system`, `chat_verification`) |

**Rule B would not have made either adopter movable.** The tool's dry run on each clone shows a second refusal beside the dirt: `[not-current]`, the framework files behind (each lists 11 files: `mts-system`'s are 1 to 9 versions behind; `chat_verification`'s are 1 to 45 behind, `FRAMEWORK_LEARNINGS.md` the 45, and `quality_ratchet.py` is missing), with the tool's own remedy, *run `bin/sync` first* (plan 5A.2). `chat_verification` also has an older ledger hook to replace before any move (register row F2). So for the only two adopters rule B touches, the dirt is the smallest of three preparations still owed.

**What rule B would have to handle** (part 3, scratch repository): after the apply's commit the moved file reads ` M methodology/h.jsonl`, since `git mv` carries the working-tree line but the commit holds the old blob, so the apply's own after-check (`clean`) fails and the tool exits 4; and on a failed apply `rollback()` runs `reset --hard HEAD`, which restores the old content and **deletes the adopter's uncommitted line**. Making the file not-dirt therefore needs new code in both directions: save its bytes and restore them on rollback, and either commit the line inside the migration commit (so one `git revert` also undoes the adopter's data) or leave it modified at its new path and teach the after-check to accept that.

## 4. The decision (his, 2026-10-11)

Four options in one picker: **decline with no tool change** (recommended), decline and name the remedy in the refusal text, fix rule A only, fix rule B. **He chose to decline with no tool change.** The reasons are the numbers above: the rule the row describes clears none of the 8; the rule that clears two adds a data-loss path to a tool whose central guarantee is that a dirty tree is refused so the rollback loses nothing; and one commit in the adopter clears the same dirt. The refusal stays loud and names the file (`[dirty-tree] the working tree is not clean: dashboard_history.jsonl`, part 2).

## 5. What an adopter does instead (the preparation F12 stands for)

- **A modified tracked generated file** (`mts-system`, `chat_verification` today): commit it in the adopter, or `git restore` it (it is regenerated by the next dashboard run), as its own commit there, before the sync.
- **Untracked generated files** (the `airqino` shape, P13): ignore both the old names and the new `methodology/` names, in a local `.git/info/exclude` for the run (as P13 did) or in the adopter's own `.gitignore` as its own commit; with the old names alone excluded the apply exits 4, because the moved files are untracked at their new place (register row F12).
- **A stray file the tool does not move** (`church_growth`'s `__pycache__/`, P14): exclude it locally; it is not F12.

## 6. Limits, stated where the number is

- The adopters are the ones on this machine on 2026-10-11, and two of the eight have live sessions that may write a generated file at any time: this is a measurement of that day.
- Untracked files are read in git's default mode (a whole untracked directory is one entry). That is faithful here because the generated names live at the project root and a root-level file is always listed by itself.
- "Clean under rule A or B" is read as a set of paths; it says what the rule would let the tool proceed on, not that the move would then succeed (part 2 shows two other refusals).
- "The shape arose once" rests on four moves (P11 to P14): the register records it at P13 (`airqino`) only, and P14's dirt was a stray `.pyc` the tool does not move (register, the S292 dated line). I did not re-read P11's and P12's dirt.

## 7. Reopens if, and what was not done

**Reopens if** an adopter turns up whose only dirt is untracked generated files the adopter will not ignore (the `airqino` shape, outside a rehearsal), or if modified generated files become common enough that a commit in each adopter costs more than the carry. **Not done:** any change to `bin/migrate-layout` or its tests (the tool is canonical-only, so no adopter receives anything and nothing is released); `P15`; F6, F8, F13, F14; anything upstream.
