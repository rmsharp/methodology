# PR2b layer 1: Part 1 rebuilt on `upstream/main` (S377, 2026-10-26)

**Status: BUILT and verified, local, un-pushed, nothing sent to `KJ5HST/methodology`.** This is the first checkpoint of PR2b
(`../upstream-pr-composition-plan.md` section 5, the PR2b row). Every figure is printed by a script here or by a command named beside it; the
saved outputs are `pr2b-layer1-*-output.txt`. What I read from files and what a command measured are labelled.

## 1. The answer first

1. **The layer exists.** Branch `pr2b/candidate` (a local ref with no upstream, so a bare `git push` cannot send it) is one commit, `fbcef390`
   (tree `aafbe533`), on `upstream/main` `d50ce290`: **6 files, +6,187 / -552**. It was built in a scratch clone and fetched here.
   `pr2/candidate` (`3cba1e50`) is kept as it was.
2. **It is the first build minus what upstream already has.** The first build of Part 1 (`bbe0dc35`, S311) was 9 files, +7,765 / -575. The
   difference is exactly the ledger trimmer (+430 / -22), its unit tests (+1,136), `FRAMEWORK_APPARATUS.md` (+11) and one gate-threshold line
   (+1 / -1). Those three files now equal upstream's, which `pr2b-layer1-resolve.py` shows (section 3).
3. **It is green in a clean clone** (section 4): the shell suite **271 passed, 0 failed, 0 skipped**; the quality ratchet **12/12 pass, 0 fail,
   0 unmeasured**; the one shipped `.verify.sh` exits 0, as it does on the base.
4. **No region needed his judgment.** All 28 conflict regions of commit 1 resolve to upstream's side (section 3); the layout hunks, the one
   place the sizing record called new judgment, are commit 5 and not in this layer.

## 2. What it carries

| File | Change | Why it is in the layer |
|---|---|---|
| `starter-kit/methodology_dashboard.py`, `tools/methodology_dashboard.py` (twins) | 2.11.3 to 2.21.0, +1,353 / -210 each | theme D, whole lineage; 2.21.0, not the tip's 2.22.0 (that step is a later layer) |
| `tools/test_methodology_dashboard.py` | +3,245 / -115 | its unit suite, 354 tests |
| `bin/tests.sh` | +232 / -13 | the `skip()` primitive, the exec-bit check from the manifest, three pipelines as here-strings, Tests 35 and 36 |
| `starter-kit/BOOTSTRAP.md` | +2 / -2 | the never-overwrite row names `.gitattributes` |
| `.quality-gates.json` | +2 / -2 | `tests-sh-passed` 261 to 271, `dashboard-unit-tests` 229 to 354. `trimmer-unit-tests` stays at upstream's 227 |

The two decisions of the first build stand unchanged: two dashboard tests that assert facts about this repository's own `docs/planning/BACKLOG.md` are
not carried, and the ledger-count test's floor is `min(6, ledgers present)`. The commit carries no `CHANGELOG.md` entry (the scratch clone runs no hooks, and
the ledger upstream is the maintainer's).

## 3. The 28 regions (`pr2b-layer1-resolve.py`, saved output `pr2b-layer1-resolve-output.txt`)

The script applies `bbe0dc35` to `d50ce290` with `git cherry-pick -n` in a throwaway clone, counts each conflicted file's regions in the default marker
style (the unit of the plan's 46 and of the sizing record's 28), resolves every region to upstream's side, and compares the result with upstream's file byte for byte.

| File | Regions | Resolved to upstream's side equals upstream's file? |
|---|---|---|
| `starter-kit/methodology_trim.py` | 13 | **equal**: the commit's cleanly merged hunks add nothing beyond upstream's 1.8.2 |
| `tools/test_methodology_trim.py` | 13 | **equal** |
| `FRAMEWORK_APPARATUS.md` | 1 | **equal** |
| `.quality-gates.json` | 1 | differs by two cleanly merged thresholds (261 to 271, 229 to 354), which section 4 re-derives |

Total 28 regions in 4 files, equal to the sizing record's figure for commit 1. The five other files merged with no conflict.

**Read from the files (not measured):** what the candidate's copy has that upstream's lacks is the maintainer's review edits' other side. In the trimmer, 30
lines (`git diff --numstat`), among them the 1.7.0 version string, the proof template's `python3 -` heredoc where 1.8.2 has `python3 -I`, and the 1.7.0 wording of the timing rule; in the tests,
20 lines and **one test name**, `test_a_pending_stub_at_record_0_fires_the_guard_and_names_both_ways_out`, which upstream's 227 do not have. Upstream states the same rule in
`FRAMEWORK_APPARATUS.md` (the paragraph beginning "Give the trim a commit of its own, never in the same commit that edits record 0") in other words than the candidate's
("Trim while record 0 is complete"). I took upstream's wording because it is the maintainer's accepted text; whether the fork's own prose should follow it is a question for the
layers that touch the trimmer (commits 5, 26 and 34), not this one.

## 4. The checks of the PR2 row, and which of them apply here

Clean `--no-local` clones, serial, `layer-verify.sh`; the verified commit was `5f202458`, then only its message was amended to `fbcef390` (tree `aafbe533` before and after).

| Check (plan section 5, PR2 row) | Result |
|---|---|
| `bash bin/tests.sh` (run directly; the last section of `pr2b-layer1-verify-output.txt`) | **271 passed, 0 failed, 0 skipped**, exit 0 |
| `quality_ratchet.py --run` (`pr2b-layer1-verify-output.txt`) | **12/12 pass, 0 fail, 0 unmeasured**; results `e658e1a02647`, manifest `84815aa7e6e5`. Measured 271, 354 and 227 against floors 271, 354 and 227. The base reads 12/12 at 261, 229 and 227 (results `b49e29a9e5ea`) |
| every shipped `.verify.sh` exit histogram equal to upstream's | one tracked proof (`docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh`): exit 0 on the layer, exit 0 on the base |
| `bin/check-links --layout both` | **not applicable at this layer**: the flag arrives with the sync layer (commit 9); here it exits 2 as an unknown option. Plain `bin/check-links` exits 0 and is a passing gate |
| `bin/check-layout-literals` 0 sites | **not applicable**: the scanner arrives with commit 2 and does not exist yet |
| the changed-file list equal to section 4 | **by reading, not by a script this time**: the six files are themes B and D, the portable blocks of `bin/tests.sh` and the tightened gates, all in section 4's "Carried" column; nothing from its "Not carried" column is touched |
| PR2b row: `conflicts-after-merge` reads 0 | `git merge-tree --write-tree upstream/main pr2b/candidate` exits 0; `upstream/main` is an ancestor; the branch is 1 commit ahead |
| the read-set budget (`context_budget.py --status`) | nothing over budget, exit 0 |

No threshold was loosened: 261 to 271 and 229 to 354 tighten, 227 is upstream's.

## 5. What this does not show

1. **The surface** is this machine: clean clones, serial runs, hooks **not armed** (`layer-verify.sh` unsets `core.hooksPath`), so the ratchet's pre-commit refusal was not exercised on this commit.
   It cannot show Windows, the maintainer's machine or upstream's CI (there is none).
2. **Two checks of the row wait for a later layer** (the `--layout` flag and the scanner), as above. They are not passed; they do not exist yet.
3. **PR3's table and PR4's text** are not re-run (the plan's PR2b row says they are, after all layers); their figures remain the old base's.
4. **The gate floors will move again.** `tests-sh-passed` and the dashboard floor are exact for this layer; every later layer re-derives them (tighten only).
5. **"Two to three sessions" is still a guess.** One layer cost one session, and it was the one with the most regions (28) but the least judgment (none). Commit 5 is the opposite.

## 6. Next

Re-run the instrument: `python3 -I docs/planning/pr-composition-evidence/pr2b-layer1-resolve.py` (about 10 s). The next layer, from the sizing record's order, is **commit 2**
(`14ef9597`, the layout resolver, the fixture trees and the literal scanner) cherry-picked onto `pr2b/candidate`: the sizing found it applies with no conflict, so its session
is the verification (it adds the scanner, so the row's literal check becomes applicable), then commits 3 and 4 (the ledger hook and the ratchet), then 5 by
reading. One layer per session, a claim first.
