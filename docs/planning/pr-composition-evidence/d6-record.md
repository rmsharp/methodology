# PR2, D6's small commit: a cited gate run that reads unmeasured gates is repaired or names them, in two of the three documents

**Status: BUILT, verified in a clean clone, nothing sent.** Session S323, 2026-10-15 (`../upstream-pr-composition-plan.md` §7 D6, answered (a) at the S321 close-out; `layer6c-record.md` §3 and §5 named it). The local ref `pr2/candidate` moved
`ab35e96` to **`5afc962`**, one commit, 2 files, +5 / -2 (`git diff --numstat`); the candidate is now 20 commits, 46 files, +19,859 / -1,147 against `upstream/main` (`f34769f`).
Every figure below is printed by a script in this directory (`d6-*`); the saved outputs are `d6-*-output.txt` (the clean-clone run is `d6-verify-output.txt`, colour stripped).

## 1. The answer first

1. **D6 carried two of its three hunks, and one of them one line short.** The derivation found two things the answer (a) was given without; he decided both at the Phase 0 picker of S323 (each as recommended).

   | File | The fork's hunk | Carried |
   |---|---|---|
   | `starter-kit/HANDOFFS.md` | +5 / -2: the rule (four lines) and the checker sentence changed to "lints the newest receipt for that token **and clause**" | **+4 / -1**: the four rule lines; upstream's checker sentence stays ("for that token"). The candidate's `bin/check-handoff` has 0 mentions of `unmeasured`: the clause lint is fork-only, so the file says the rule and does not say a checker enforces it |
   | `HOW_TO_USE.md` | +1 / -1: the 3E bullet's last sentence | **+1 / -1**, the fork's bytes |
   | `starter-kit/SESSION_RUNNER.md` | +1 / -1: the 3E sentence, +224 B | **not carried** (§1.2) |

2. **The runner already reads OVER its read-set ceiling on the candidate, and has since S321's first prose commit.** `python3 starter-kit/context_budget.py --status` (the candidate carries upstream's `.context-budget.json`: 18,900 tokens for the runner, at 2.8107 B/token):
   `505541c` (upstream's runner, 52,839 B) **ok, exit 0**; `c8d4375` onward (53,184 B, +345 B) **≈18,921 tokens, 21 over, exit 2**, at every later commit including this one (`d6-measure-output.txt` §1). **Nothing refuses it:** the tool is in neither the ratchet's 18 gates nor `.githooks/pre-commit`, and every layer's verification read green. Neither S321's nor S322's record shows a reading of it.
   D6 as first answered would have taken it to **≈19,001 tokens, 101 over** (the fork tip's 3E line, +224 B: `d6-measure-output.txt` §2), with `SAFEGUARDS.md` ≈6,040 beside it against the 25,000-token read cap. So the runner's sentence stays on the fork, D6 moves the reading by **0** (§1 of the output: the same ≈18,921 at `5afc962`), and **the 21 are a defect of S321's layer to repay before PR2 goes out: BL-113.**
3. **Verified, `layer-verify.sh` on `5afc962` in a clean `--no-local` clone (0 dirty paths):** the ratchet **18/18 pass, 0 fail, 0 unmeasured, results `23481eb88ba1`, manifest `66cce597ef4a`** (equal to S322's run on `ab35e96`: the commit changes prose no gate reads);
   `tests-sh-passed` 302 (the floor, 302), `migrate-layout-unit-tests` 280, `layout-unit-tests` 76, `checker-layout-unit-tests` 11, `sync-layout-unit-tests` 82; the scanner 15 files, 0 sites; the one shipped `.verify.sh` proof exit 0. The shell suite ran inside the ratchet, not on the commit alone.

## 2. What was measured, and how

| Check | Result | Output |
|---|---|---|
| The tip's two documents against the candidate's, hunk by hunk (`d6-derive.py`, importing `layer6c-build.py`'s `hunks()` and `NOT_LAYOUT`) | the unmeasured hunks total **+7 / -4** in 3 files (the plan's figure); the fork tip's blobs equal the builder's recorded premises; 0 fork tokens in the added lines | `d6-derive-output.txt` |
| The build (`d6-build.py`): premises asserted, one hunk per file, what is left to the tip is exactly the others | 2 files written, HANDOFFS 13,487 to 13,764 B (+277), HOW_TO_USE 57,070 to 57,188 B (+118); refuses on drift | `d6-build-output.txt` |
| The runner's budget reading at each commit, and the counterfactual (`d6-measure.sh` §1, §2) | §1.2 above | `d6-measure-output.txt` |
| What the commit touches (§3) | 2 files; the runner untouched; 0 gate or budget files | same |
| The claims the added text makes about tools (§4) | the summary line prints `U unmeasured` (1 line in `quality_ratchet.py`); `timeout_seconds` declared (17 mentions); `bin/check-handoff` 0 | same |
| Scrub input (§5) | 5 added lines, **0** fork tokens (backlog code, session number, `docs/planning`, fork, operator, learning, PR or issue number); the commit message **0** | same |
| `bin/check-links --layout both` (§6) | exit 0 | same |
| The two open pull requests, `git merge-tree --write-tree --name-only` of `ab35e96` and `5afc962` with each head | **#94 (`972eb2c`): the same three conflicting files before and after** (`.quality-gates.json`, `starter-kit/methodology_trim.py`, `tools/test_methodology_trim.py`); **#92 (`fa2bb5d`): clean at both** | `d6-conflicts-output.txt` (`d6-conflicts.sh`) |

## 3. Decisions

His, at the Phase 0 picker, 2026-10-15: **the runner's 3E sentence stays on the fork** (the recommended option; the alternatives were to pay 101 tokens out of upstream's runner text in the same commit, or to carry it and let the tool read 101 over), and **the HANDOFFS hunk is carried honest to the candidate** (the alternative was the fork's bytes with only the pull request's text qualifying them).
Mine: the commit message uses recognised terms only (it becomes pull request text); no `CHANGELOG.md` co-stage and no hook, as every earlier commit on the candidate (none touches `CHANGELOG.md`; the trailer is in the message); the builder imports `layer6c-build.py` and sets `sys.dont_write_bytecode` (the first derivation left an untracked `__pycache__` in this directory, removed before any commit).

## 4. What this does not show

- **The OVER is the tool's reading at the config's density, not a meter reading.** The config says a density is tied to the blob it was measured on (2.8107 was measured on upstream's blob) and that new text dense in backticked paths costs more tokens per byte. The true reading of `c8d4375`'s blob may be more than 21 over; the doubled-read method (an opus subagent with a control) was not run.
- **PR2's text must now say two things:** the clause lint stays on the fork, and the runner's 3E sentence stays on the fork. A session reading the candidate's runner meets the 3E mechanical half without the rule about unmeasured gates; the rule is in the receipt seed and the how-to.
- The other non-layout hunks stay on the fork as S321 recorded them (four in the runner: the plan-surface rule's three and the model tag; one in HOW_TO_USE: a session number); with them stay the runner's 3E hunk and the HANDOFFS checker line. Read from `d6-derive-output.txt`, not new.
- The surface is this machine (load average 6.64 at the launch, 11.36 two minutes later): a clean clone, serial runs. Not shown: a maintainer's machine; Windows; upstream CI (there is none); the candidate merged with #94 (the conflicting paths are equal before and after; their regions were not recounted).

## 5. Next, and for him

**The scrub (its own commit) and PR3**, in the plan's order; the scrub's inputs are `layer7b-measure-output.txt` §7 (`bin/migrate-layout`: 19 lines with a backlog code, 14 plan references; its suite 13 and 19), `layer6c-measure-output.txt` §7, and this commit's §5 (none). **Before PR2 goes out: BL-113** (the runner's 21 tokens) and a budget reading per layer: `layer-verify.sh` runs 18 gates and none reads `context_budget.py --status`.
PR3's first row is the 9 `--force` syncs (`layer7b-adopters-output.md` §3 and §4).
Re-run this layer: `bash layer-verify.sh <candidate> 5afc962`; rebuild: `python3 d6-build.py <fork> 2481960 <clone-at-ab35e96> --write`, commit; the rest: `d6-derive.py <fork> <rev> <clone> ab35e96`, `d6-measure.sh <fork> <rev> <candidate> 5afc962 <work-dir>`.
