# Upstream PR — `context_budget.py`: a real `--status`, refused arguments that say what was meant, and a headline and advisory that agree with the table (draft body)

Fork-only working file: the draft title and body for the pull request from `rmsharp:fix/context-budget-status`
into `KJ5HST/methodology:main`. Everything below the rule is the body as it would be posted. **Rewritten** under
[`context-budget-status-plan.md`](context-budget-status-plan.md) §5 P3′ (S214) on the branch tip `c1167ae`,
recomposed rather than patched from the draft the operator reviewed at S212 and did not approve, which it
replaces here; that draft stays readable as `git show e4ad63d:docs/planning/context-budget-status-pr-body.md`.
**APPROVED AS WRITTEN by the operator, 2026-09-21 (S214), at `fb324d6`. POSTED UNCHANGED 2026-09-21 (S215) as
[#86](https://github.com/KJ5HST/methodology/pull/86):** title `:12` without its label, body `:16` onward, both read back equal. Its figures are S214's,
on the heads its first line names, and neither had moved. Change the posted body with `gh api -X PATCH`, never `gh pr edit`.

**Title:** `context_budget.py`: `--status` becomes a real run that writes nothing, a refused argument is told what it most likely meant, and the headline and advisory stop contradicting the table

---

**Base `main` (`6b29d3d`), head `rmsharp:fix/context-budget-status` (`c1167ae`).** Six commits, one per change,
each with its own `CHANGELOG.md` entry: 5 files, +631 / −11, of which `CHANGELOG.md` is +156.
`starter-kit/context_budget.py` +78 / −9, `tools/test_context_budget.py` +365, `bin/tests.sh` +30,
`.quality-gates.json` 2 thresholds. No Learning row, no failure-mode change, no hook change.

## The problem

Three defects in what `starter-kit/context_budget.py` does and what it says.

**1. There is no `--status`, and an argument the tool does not recognise is ignored.** `main()` dispatches on
membership tests, and anything it does not match falls through to the default measurement. That run appends a row
to `.context-budget-history.jsonl` whenever a size changed. In a fresh clone of `main`, `--status`, `--check`,
`--force`, `--dry-run`, the misspelling `--stauts` and `--zzz` each exit 0 and leave
`?? .context-budget-history.jsonl` in the tree.

`--status` is nonetheless cited 12 times in this repository's own ledgers as a verification step (5 in
`CHANGELOG.md`, 7 in `HANDOFFS.md`), and once in the body of #84. Each of those readings was sound, since the
default run prints the same ledger. The defect is the write, and the silence. It is also the blocker you named
reviewing #82 ([point 6](https://github.com/KJ5HST/methodology/pull/82#issuecomment-5701463025)): *"`--status`
writes `.context-budget-history.jsonl` into the tree on every run … Tracked-or-ignored gets decided first; then the
gate."*

**2. The growth-run advisory contradicts the table.** When the growth run fires, `render()` adds *"Nothing is over
a ceiling yet — that is the point. Ceilings fire late."* The sentence was a literal. It printed in every such run,
including runs whose headline read `context budget OVER` above rows marked `over`.

**3. A row over a ceiling could read `instrument-failed`.** `measure_file()` gave a row the status of whichever
check wrote last. A structure pattern that matched fewer records than its `expect_min` overwrote a ceiling's `over`
with `instrument-failed`, which `render()` ranks just below `over`. The headline then read `INSTRUMENT-FAILED`, and
when the growth run fired, the advisory said nothing was over directly above the finding that the ceiling was
exceeded. The comment above `main()`'s exit said the tool's ordering ranks an instrument failure *above* `over`.

## What this changes

| Arguments | Measures | Writes history | Output | Exit |
|---|---|---|---|---|
| (none) | yes | when a size changed | ledger | 0 / 1 / 2 by verdict |
| `--json` | yes | when a size changed | JSON | same |
| **`--status`**, **`--check`** | yes | **never** | ledger | same as (none) on the same tree |
| **`--status --json`**, **`--check --json`** | yes | **never** | JSON | same |
| `--precommit`, `--calibrate`, `--selftest`, `install-hook` | unchanged | unchanged | unchanged | unchanged |
| `-h`, `--help` (with anything) | no | no | usage | 0 |
| **anything else** | **no** | **no** | `unknown argument: …`, a hint where one applies, then usage | **3** |

- **`--status`** is the default run with its one write removed (`e859196`): the same ledger and exit code, and no
  history row. Like `quality_ratchet.py --status`, it changes nothing in the tree. It makes the gate from #82
  declarable without first settling whether the history file is tracked or ignored.
- **`--check` is a second name for `--status`** (`612570b`). It is the ledger trimmer's name for its report-only
  run (`methodology_trim.py --check`: *"evaluate the trigger and report; never writes"*), and the one argument
  outside the tool's list that an adopter project's instructions type.
- **An unknown argument exits 3**, the tool's documented usage code (*"config or usage"*), before the tree is read
  (`e859196`). **Each one gets a line of its own saying what it most likely meant** (`612570b`), from what the
  sibling tools use the same flag for:
  - `--force` (the trimmer's and the dashboard's override): *"there is deliberately no --force: to permit growth,
    raise that file's ceiling in .context-budget.json"*;
  - `--dry-run` (the dashboard's preview): *"did you mean --status? It measures and writes nothing"*;
  - `--run` and `--write` (the ratchet's and the trimmer's real run): *"run with no argument to measure and
    record"*;
  - a misspelling of an accepted argument: *"did you mean <nearest>?"*, from `difflib.get_close_matches` with a
    cutoff of 0.75. At the default 0.6, `--version` is offered `--json`; at 0.75 it is offered nothing;
  - anything else: nothing more.

  The accepted list, `ACCEPTED_ARGUMENTS`, is declared above the selftest, because the selftest's check that the
  string `--force` appears nowhere above it is the one existing guard that can read the list. The hint table
  names `--force`, so it sits below the selftest, and hints are looked up by key, never by the
  `"--force" in args` expression the two source greps match. The usage text's *"There is deliberately no
  --force"* becomes observable.
- **The advisory's second sentence is chosen by `worst`**, the variable the headline prints, so the two cannot
  disagree (`c299c30`). When nothing is over, the sentence is unchanged, word for word. When something is, it
  reads *"A ceiling has fired as well — see the rows marked over."*
- **A check may raise a row's status, never lower it** (`2f73733`). A failed structure pattern now leaves an
  `over` row as it is. Both findings still print, the exit code is 2 either way, and `main()`'s comment now says
  what the code does. No other output changes: `test_a_declared_ceiling_still_renders_exactly_as_before` still
  holds.
- **`VERSION` 1.2.0 → 1.3.0**, for the usage banner only: `bin/status` compares blobs, not versions. The usage
  text gains `--status` and `--check` lines, and the default's *"append one history line"* now says *"when a
  size changed"*, which is what `append_history` does.
- **Two floors tightened to the values this branch measures**, in two commits: `tests-sh-passed` 139 → 141
  (`d4dbc26`) → 142 (`c1167ae`), and `context-budget-unit-tests` 118 → 129 → 140, since the manifest owes a
  tightening whenever a measured value rises. Every other gate measures exactly its threshold.

## How it was tested

- **22 unit tests, each written first and run against the tool as it stood before its change.** 15 fail on the
  old tool; the other 7 are controls that pass on it by design.
  - `--status` and the refusal, in `TestCommandLine` (8): 6 fail; the controls are that the default run still
    writes and that `--help` still wins.
  - The advisory, in `TestGrowthRunAdvisory` (3): a matrix over every status `render()` ranks, with and without
    the growth run, calling `render()` in process; a control that every status below `over` still prints the
    original sentence, so deleting it cannot pass; and one run of the real `main()` → `render()` path. 2 fail.
  - `--check` and the hints, in `TestCommandLine` (7, and `--check` added to its frozen accepted set): 5 fail,
    and so does the frozen set; the controls are that `--zzz` and `--version` are offered nothing.
  - Status precedence, in `TestStatusPrecedence` (4): the end-to-end run and the `--json` row fail; the
    controls are that a row which only fails its pattern still reads `instrument-failed`, and that a row past
    its warn line is still raised to it.
- **3 rows in `bin/tests.sh`**, each in a `mktemp` project with the seed config: `--status` leaves
  `git status --porcelain --ignored` empty; `--zzz` exits 3 and changes nothing; `--check` exits as `--status`
  does and writes nothing. Each fails on the tool as it stood before its change.
- **17 mutants, each run and each caught by at least one test.** For the command line: the append made
  unconditional again; the rejection removed; `--force` added to the list; a comment above the list naming the
  selftest's definition, plus `--force`. For the advisory: the literal restored; the sentence deleted; the
  condition inverted; the condition widened to `instrument-failed`. For the hints: `--check` dropped from the
  write guard; the hint table emptied; the cutoff at 0.6; the suggestion printed unconditionally; the hint table
  moved above the selftest. For status precedence: the guard removed; the guard never setting the status;
  raising from `warn` blocked; raising from `ok` blocked. `--selftest`, the part that ships to adopters, catches
  4 of the 17. One is worth a word: the selftest's check splits the source on the first mention of the
  selftest's definition, so a comment naming it moves the cut up, and `--force` in the list then passes the
  selftest. `test_the_selftest_escape_hatch_check_still_reads_the_accepted_list` pins the split point.

## Verified

On the branch tip `c1167ae`, in a fresh `--no-local` clone with `HEAD` asserted:

- `python3 starter-kit/quality_ratchet.py --run`: **10/10 pass**. `bin/tests.sh` 142 passed, 0 failed; budget
  units 140, dashboard units 226, trimmer units 123, ratchet units 45; `check-links`, `check-learnings`,
  `check-handoff --all` and `commit-msg --selftest` all at 0.
- `python3 starter-kit/context_budget.py --selftest`: 52 PASS, exit 0.
- Each command in a clean clone of `main` and of the tip, the tree restored between runs:

| Command | `main` (`6b29d3d`) | this branch (`c1167ae`) |
|---|---|---|
| `--status`, `--status --json` | exit 0, leaves `?? .context-budget-history.jsonl` | exit 0, tree unchanged |
| `--check`, `--check --json` | exit 0, leaves the history file | exit 0, tree unchanged |
| `--force` | exit 0, leaves the history file | exit 3, `unknown argument: --force — there is deliberately no --force: …`, tree unchanged |
| `--dry-run` | exit 0, leaves the history file | exit 3, `… — did you mean --status? It measures and writes nothing` |
| `--stauts` | exit 0, leaves the history file | exit 3, `… — did you mean --status?` |
| `--zzz` | exit 0, leaves the history file | exit 3, `unknown argument: --zzz`, no hint |
| `--help --zzz` | exit 0, usage | exit 0, usage |
| bare | writes the history file | writes the history file |

- The two contradictions, in a `mktemp` project holding one 1,500 B file, with a growth-run limit of 2 and a
  seeded history that fires it:

| Project | `main` | this branch |
|---|---|---|
| a class total over its ceiling | headline `OVER`; *"Nothing is over a ceiling yet"* | headline `OVER`; *"A ceiling has fired as well — see the rows marked over."* |
| a file over its byte ceiling that also fails a structure pattern | headline `INSTRUMENT-FAILED`, row `instrument-failed`; *"Nothing is over a ceiling yet"* | headline `OVER`, row `over`; *"A ceiling has fired as well …"* |

  Every run in that table exits 2.

## Against the three open PRs

Computed with `git merge-tree --write-tree --name-only` from `c1167ae`, then merged for real in scratch clones
(any `CHANGELOG.md` conflict resolved by keeping both sides; every entry kept, and counted). The quality ratchet
then ran on each merge result:

| PR | Merge | On the merge result |
|---|---|---|
| #84 (`77afc12`) | clean, `CHANGELOG.md` included, though both touch `tools/test_context_budget.py` and `bin/tests.sh` | **10/10 pass**; `bin/tests.sh` 166 passed, 0 failed (142 + #84's 24); budget units 144 (140 + #84's 4) |
| #85 (`e2501c5`) | `CHANGELOG.md` only; `.quality-gates.json` merges cleanly (its new gate sits below the two changed thresholds) | **11/11 pass**, #85's `pre-commit-selftest` included; `bin/tests.sh` 142 passed, 0 failed |
| #83 (`219fb9d`) | `CHANGELOG.md` only | **10/10 pass**; `bin/tests.sh` 142 passed, 0 failed |

Whichever of these you merge first, the next conflicts at the top of `CHANGELOG.md`; I will merge `main` into
the branch after it.

## Who notices

- **A session that types `--status` or `--check`** gets the same ledger and exit code as before, and no history
  row. The growth series is now fed only by bare and `--json` runs.
- **One adopter project** of the seven checked has a live instruction in its session notes: *"Re-measure
  (`python3 context_budget.py --check`) before writing more"*. It now does what its author meant, measuring and
  reporting without appending a history row, where before it ran the default measurement, write included.
- **Anything passing another unrecognised argument** now gets exit 3 and a line saying what it most likely
  meant, not a silent measurement. None of the seven adopters types one after the tool's name. No caller passes
  `"$@"`: the installed hook passes only `--precommit`.
- **A script reading a row's status from `--json`**: a row over a ceiling that also fails a structure pattern
  now reports `over`, not `instrument-failed`. The exit code is 2 either way.

## Not changed here

- **Declaring a `context-budget` gate.** This PR makes one declarable; whether to declare it is yours.
- **Combinations of known commands** (`--selftest --calibrate`): their precedence is unchanged.
- **No existing ledger entry or receipt that cites `--status` or `--check` is edited.** Each was a sound reading
  of the default run, and the command it names now exists.

## What can be dropped

Each change is its own commit. The likeliest to be unwanted are the two floor commits, `d4dbc26` and `c1167ae`,
if you would rather tighten the floors yourself; they go together, and without them the floors stay at 139 and
118, below what the branch measures. A plain `git revert` of any one commit conflicts in `CHANGELOG.md`, because
later entries sit above its own; say which you would drop and I will drop it on the branch.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
