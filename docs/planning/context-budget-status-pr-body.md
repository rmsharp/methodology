# Upstream PR — `context_budget.py`: a real `--status`, refused unknown arguments, an advisory that agrees with its table (draft body)

Fork-only working file: the draft title and body for the pull request from `rmsharp:fix/context-budget-status`
into `KJ5HST/methodology:main`. Everything below the rule is the body as it would be posted. Written under
[`context-budget-status-plan.md`](context-budget-status-plan.md) §5 P3 (S212). **Not posted.** Opening the PR,
and pushing the branch to fork `origin` first, is P4's go-ahead on the exact text below. Every figure in it was
measured at S212 on the heads named in its first line; re-measure if either head moves before posting.

> **⚠ SUPERSEDED DRAFT — DO NOT POST THIS TEXT.** The operator reviewed it at S212 and did not approve it: it
> named problems without fixes. The review decided two more changes for the same PR instead: plan §3 **D6** (each
> refused argument's message answers what the user meant, and `--check` becomes a second name for `--status`) and
> **D7** (a byte ceiling's `over` survives a failed structure pattern). This text is kept, frozen, as the record of
> what was reviewed. The plan's **P3′** rewrites the body on P2c's tip. It recomposes, it does not patch, and every
> figure is re-measured.

**Title:** `context_budget.py`: `--status` becomes a real run that writes nothing, unknown arguments are refused, and the growth-run advisory stops contradicting the table

---

**Base `main` (`6b29d3d`), head `rmsharp:fix/context-budget-status` (`d4dbc26`).** Three commits, one per
change, each with its own `CHANGELOG.md` entry: 5 files, +348 / −7, of which `CHANGELOG.md` is +74.
`starter-kit/context_budget.py` +33 / −5, `tools/test_context_budget.py` +216, `bin/tests.sh` +23,
`.quality-gates.json` 2 thresholds. No Learning row, no failure-mode change, no hook change.

## The problem

Two defects in what `starter-kit/context_budget.py` does and what it says.

**1. There is no `--status`, and an argument the tool does not recognise is ignored.** `main()` dispatches
on membership tests, and anything it does not match falls through to the default measurement. That run
appends a row to `.context-budget-history.jsonl` whenever a size changed. So `--status`, `--check`,
`--force` and a typo all ran the real measurement, write included. In a fresh clone of `main`, each of
`--status`, `--check` and `--zzz` exits 0 and leaves `?? .context-budget-history.jsonl` in the tree.

`--status` is nonetheless cited 12 times in this repository's own ledgers as a verification step (5 in
`CHANGELOG.md`, 7 in `HANDOFFS.md`), and once in the body of #84. Each of those readings was sound, since the
default run prints the same ledger. The defect is the write, and the silence. It is also the blocker you
named reviewing #82
([point 6](https://github.com/KJ5HST/methodology/pull/82#issuecomment-5701463025)): *"`--status` writes
`.context-budget-history.jsonl` into the tree on every run … Tracked-or-ignored gets decided first; then the
gate."*

**2. The growth-run advisory contradicts the table.** When the growth run fires, `render()` prints:

```
growth run: 168 consecutive non-shrinking measurements. Nothing is
over a ceiling yet — that is the point. Ceilings fire late.
```

The second sentence was a literal. It printed in every such run, including runs whose headline read
`context budget OVER` above a table with rows marked `over`.

## What this changes

| Arguments | Measures | Writes history | Output | Exit |
|---|---|---|---|---|
| (none) | yes | when a size changed | ledger | 0 / 1 / 2 by verdict |
| `--json` | yes | when a size changed | JSON | same |
| **`--status`** | yes | **never** | ledger | same as (none) on the same tree |
| **`--status --json`** | yes | **never** | JSON | same |
| `--precommit`, `--calibrate`, `--selftest`, `install-hook` | unchanged | unchanged | unchanged | unchanged |
| `-h`, `--help` (with anything) | no | no | usage | 0 |
| **anything else** | **no** | **no** | `unknown argument: …` + usage | **3** |

- **`--status`** is the default run with its one write removed (`e859196`): the same ledger and exit code, and
  no history row. Like `quality_ratchet.py --status`, it changes nothing in the tree. It makes the gate from
  #82 declarable without first settling whether the history file is tracked or ignored.
- **An unknown argument exits 3**, the tool's documented usage code (*"config or usage"*), before the tree is
  read (`e859196`). The accepted list is `ACCEPTED_ARGUMENTS`, declared above the selftest, because the
  selftest's check that the string `--force` appears nowhere above it is the one existing guard that can
  read the list. The two `"--force" in args` greps match only that expression. The usage text's *"There is
  deliberately no --force"* becomes observable: `--force` is refused rather than silently measured.
- **The advisory's second sentence is chosen by `worst`**, the variable the headline prints, so the two
  cannot disagree (`c299c30`). When nothing is over, the sentence is unchanged, word for word. When something
  is, it reads *"A ceiling has fired as well — see the rows marked over."* No other output changes, and
  `test_a_declared_ceiling_still_renders_exactly_as_before` still holds.
- **`VERSION` 1.2.0 → 1.3.0**, for the usage banner only: `bin/status` compares blobs, not versions. The
  usage text gains a `--status` line, and the default's *"append one history line"* now says *"when a size
  changed"*, which is what `append_history` does.
- **Two floors tightened to the values this branch measures** (`d4dbc26`): `tests-sh-passed` 139 → 141 and
  `context-budget-unit-tests` 118 → 129, since the manifest owes a tightening whenever a measured value
  rises. Every other gate measures exactly its threshold.

## How it was tested

- **11 unit tests, each written first and run against the tool as it stood before its change.**
  `TestCommandLine` (8): 6 fail on the old tool, and the other 2 are controls that pass on it by design
  (the default run still writes; `--help` still wins). `TestGrowthRunAdvisory` (3): a matrix over every
  status `render()` ranks, with and without the growth run, calling `render()` in process; a control that every status below `over` still prints the original
  sentence, so deleting the sentence cannot pass; and one run of the real `main()` → `render()` path on a
  project over its budget with a seeded history. 2 fail on the old tool; the control passes on it by design.
- **2 rows in `bin/tests.sh`**, in a `mktemp` project with the seed config: `--status` leaves
  `git status --porcelain --ignored` empty, and `--zzz` exits 3 and changes nothing. The project's default run
  comes last, as a control that it does get written to. Both rows fail on the old tool.
- **Mutants, each run:** the append made unconditional again; the rejection removed; `--force` added to the
  list; a comment above the list naming the selftest's definition, plus `--force`; the advisory's literal
  restored; the sentence deleted; the condition inverted; the condition widened to `instrument-failed`. Every
  one is caught by at least one test. The fourth is worth a word: the selftest's check splits the source on
  the first mention of the selftest's definition, so a comment naming it moves the cut up and `--force` in the
  list passes the selftest. `test_the_selftest_escape_hatch_check_still_reads_the_accepted_list` pins the
  split point.

## Verified

On the branch tip `d4dbc26`, in a fresh `--no-local` clone with `HEAD` asserted:

- `python3 starter-kit/quality_ratchet.py --run`: **10/10 pass**. `bin/tests.sh` 141 passed, 0 failed;
  budget units 129, dashboard units 226, trimmer units 123, ratchet units 45; `check-links`,
  `check-learnings`, `check-handoff --all` and `commit-msg --selftest` all at 0.
- `python3 starter-kit/context_budget.py --selftest`: 52 PASS, exit 0.
- Measured behaviour, each in a clean clone:

| Command | `main` (`6b29d3d`) | this branch |
|---|---|---|
| `--status` | exit 0, leaves `?? .context-budget-history.jsonl` | exit 0, tree unchanged |
| `--status --json` | the `--json` run: valid JSON, leaves the history file | valid JSON, tree unchanged |
| `--check`, `--force`, `--zzz` | exit 0, leave the history file | exit 3, `unknown argument: …` + usage, tree unchanged |
| bare | writes the history file | writes the history file |

## Against the three open PRs

Computed with `git merge-tree --write-tree --name-only` from `d4dbc26`, then merged for real in scratch clones
(any `CHANGELOG.md` conflict resolved by keeping both sides, every entry kept). The quality ratchet then ran on
each merge result:

| PR | Merge | On the merge result |
|---|---|---|
| #84 (`77afc12`) | clean, `CHANGELOG.md` included, though both touch `tools/test_context_budget.py` and `bin/tests.sh` | **10/10 pass**; `bin/tests.sh` 165 passed, 0 failed (141 + #84's 24); budget units 133 (129 + #84's 4) |
| #85 (`e2501c5`) | `CHANGELOG.md` only; `.quality-gates.json` merges cleanly (its new gate sits below the two changed thresholds) | **11/11 pass**, #85's `pre-commit-selftest` included; `bin/tests.sh` 141 passed, 0 failed |
| #83 (`219fb9d`) | `CHANGELOG.md` only | **10/10 pass**; `bin/tests.sh` 141 passed, 0 failed |

Whichever of these you merge first, the next conflicts at the top of `CHANGELOG.md`; I will merge `main` into
the branch after it.

## Who notices

- **A session that types `--status`** gets the same ledger and exit code as before, and no history row. The
  growth series is now fed only by bare and `--json` runs.
- **Anything passing an unrecognised argument** now gets exit 3 and the usage text, not a silent measurement.
  Of seven adopter projects checked, one has a live instruction in its session notes to run
  `context_budget.py --check`; it will now fail loudly, and dropping the flag restores it. No caller passes
  `"$@"`: the installed hook passes only `--precommit`.

## Not changed here

- **Declaring a `context-budget` gate.** This PR makes one declarable; whether to declare it is yours.
- **Combinations of known commands** (`--selftest --calibrate`): their precedence is unchanged.
- **A row can be over a ceiling and still read `instrument-failed`.** `measure_file()` gives a row the status
  of whichever check wrote last, so a structure pattern below its `expect_min` overwrites a byte ceiling's
  `over`. The headline then reads `INSTRUMENT-FAILED`, and the advisory keeps the original sentence above a
  finding that says the ceiling was exceeded. The advisory agrees with the headline, as intended; the question
  is status precedence in `measure_file()`, and `main()`'s comment ranks an instrument failure above `over`
  while `render()` ranks it below. It is a separate question from these two defects, so it is left alone here.
- **No existing ledger entry or receipt that cites `--status` is edited.** Each was a sound reading, and the
  command it names now exists.

## What can be dropped

Each change is its own commit. The likeliest to be unwanted is `d4dbc26`, the two floors, if you would rather
tighten them yourself; without it they stay at 139 and 118, below what the branch measures. A plain
`git revert` of any one conflicts in `CHANGELOG.md`, because later entries sit above its own; say which you
would drop and I will drop it on the branch.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
