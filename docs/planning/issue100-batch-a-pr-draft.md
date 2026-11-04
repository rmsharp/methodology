# Draft pull request: Batch A of the #100 fixes (DRAFT, S416; nothing sent)

**Status: a fork-only DRAFT. Nothing was sent to `KJ5HST/methodology`; opening the pull request, commenting on it or on #100, and pushing the branch each need the operator's go-ahead, each time.** This file is the text of the pull request that composing Batch A (piece 6 of [`issue100-fixes-plan.md`](issue100-fixes-plan.md)) would open, with the composition's facts beside it. The text between the two `PR TEXT` markers is the only part meant for the maintainer; it is written in the repository's own terms and was scanned for the fork's codes (the scan is in §"Facts beside the text").

## What this is

- **The branch** is `issue100-batch-a` in this clone (not pushed): four commits on `upstream/main` `d50ce290`, tip `c93f1feb` (`64e1ce00`, `a6935e63`, `12431de1`, `c93f1feb`). `issue100-batch-a-before-s416` (tip `7adb0bd9`) is the stack as S412 to S415 left it; the two differ by the changes S416 made after a cold review (plan §6).
- **Not in it:** piece 3 (finding 2's Phase 0 step), which waits on #95 (D8 (a), the plan's recommendation); and everything in Batch B.
- **Decisions this composition took, each measured** (they are the operator's to overrule): no gate-floor raise (every variant adds a conflict region against #99; `piece6-floor-trial-output.txt`); no `CHANGELOG.md` entry (#98 prepends one at the same place, and #99 adds none); no `TRIM_VERSION` bump (#98 and #99 both edit it); the four commits carry the `Co-Authored-By` trailer the fork's hook requires, although the maintainer's open issue #101 asks to remove that hook, so the trailers stay unless the operator says otherwise.

<!-- BEGIN PR TEXT -->
**Title:** Refs #100: the trimmer keeps file modes and names a ledger kept out of git; bin/status warns when the checkout is behind its remote; the runner says a new task after STOP is a new session

Refs #100, not "Fixes": findings 2, 3 and 4, the hook recipe in finding 5 and the `bin/sync` / `bin/status` seed warnings in finding 6 are not here.

Four commits, one per item of the issue:

| Commit | Item in #100 | What changes | New tests |
|---|---|---|---|
| `fix(trim): a rewritten file keeps its mode and group…` | smaller point: mode 0600 | `atomic_write` in `starter-kit/methodology_trim.py` no longer uses `tempfile.mkstemp`, which is always 0600. A rewritten file keeps its permission bits and, best effort, its group; a new file's mode follows the umask; the verify script stays 0755. The temp file is never readable by more than could read the file it replaces. | 17 |
| `fix(trim): name a ledger kept out of git…` | finding 6, "the trimmer's refusal names this case" | A new finding `LEDGER_NOT_IN_GIT` names the cause (listed in `.gitignore`, never committed, or no longer tracked), in `--check` as well as in the write path. It has no exit status of its own; `P1_NO_LEDGER` keeps its id and exit 2. | 12 |
| `docs(runner): a new task after STOP is a new session…` | finding 5, the sentence | One sentence after 3G's STOP, paid for by a cut in 1B: the runner goes from 52,839 B to 52,828 B, and its headroom under its ceiling from 283 B to 294 B. | none |
| `feat(status): warn when the methodology checkout is behind…` | finding 1 | `release_lag()` in `starter-kit/context_budget.py` compares the newest release tag the checkout contains with the newest the remote lists. `bin/status` asks by default; `context_budget.py` asks with `--remote`. | 29 |

Commit 2's tests sit next to commit 1's in `tools/test_methodology_trim.py`, so commit 2 does not apply without commit 1. The other commits apply on their own.

The four commits carry the `Co-Authored-By` trailer that the Disclosure Hook (`.githooks/commit-msg`) requires when an agent harness is detected; they can be dropped before merging if you would rather not have them, as #101 proposes for the hook itself.

**Where it differs from the issue's proposals**
- Finding 1 proposed the line "in `bin/status` and in the `synced` check". `bin/status` asks by default, after its table. `context_budget.py` asks only with `--remote`, so the run a session starts with (`--status`) makes no network call, and never in `--precommit`. A stale checkout is a `warn` row (exit 1), never a breach.
- Finding 6: warning only. The trimmer does not prove a trim lossless on an untracked ledger by content.
- Finding 5: the sentence only, no hook recipe.

**What `bin/status` now does.** In local mode it asks the checkout's `origin` for its release tags (`git ls-remote --tags --refs`, usually a few seconds, and it gives up after 10) and prints `warning: checkout at v3.5, newest release v4.2 (behind: git pull)`. When it cannot ask (offline, no `origin`, no release tag, timed out) it prints one `remote not checked: <why>` line; the exit code is the run's own. `METHODOLOGY_REMOTE_CHECK=0` switches the check off, and `bin/tests.sh` sets it: the suite calls `bin/status` 18 times from its own checkout. The checkout's release is the highest tag of `git tag --merged HEAD`, not `git describe`'s nearest tag, which after a merged hotfix line can be older than a release HEAD also holds. A directory that is not the root of a git repository is not taken for a checkout. The call runs in its own process group, which is killed on a timeout and on Ctrl-C; it sets `GIT_TERMINAL_PROMPT=0` and adds `-o BatchMode=yes` to the ssh command in force.

**Adopter impact**
- Reaches adopters on their next `bin/sync` (distributed): the runner sentence, the trimmer changes, and `context_budget.py --remote`.
- Reaches only people with a checkout (canonical-only): the `bin/status` line.
- Files already at 0600 stay at 0600; `chmod` them once. A new file follows the umask, as for any file the user's own tools create, so a shard cut from a 0600 ledger is 0644 under umask 022.
- A checkout that never syncs again never gets this check. It shortens the time to notice for projects that do bring the checkout current, which is the issue's scenario once someone does.

**Left alone on purpose**, because other open pull requests edit those lines: the `TRIM_VERSION` bump, the `.quality-gates.json` floors (the suites now count 177 for `context-budget-unit-tests` and 256 for `trimmer-unit-tests`) and a `CHANGELOG.md` entry. Raising either floor here adds a conflict region against #99, and the trimmer's also against #98.

**Checks**
- The repository's own gates on a clean clone of the tip (`python3 starter-kit/quality_ratchet.py --run`): 12/12 pass, 0 fail, 0 unmeasured. `bash bin/tests.sh` passes 261 and fails 0; the four unit suites count 229, 177, 256 and 45.
- Merged with each open pull request head (`git merge-tree --write-tree`, attributes off, which is GitHub's view) the branch adds no conflict region that head did not already have: #99 and #98 merge cleanly with and without it; #96 conflicts only in `CHANGELOG.md`, with or without it.
- `python3 starter-kit/context_budget.py --status` reads the runner and `SAFEGUARDS.md` as `ok`.
- A read-only run against this repository from a checkout at v4.1: `bin/status` printed the warning line (whole runs of 2.5 to 3.0 s, against 1.7 to 2.2 s with the check off); `context_budget.py --status --remote` printed a `warn` row for the checkout.
- Cost: the budget suite goes from 12 s to 56 s; 13 s of that is the one test that waits out the 10 s limit.

**Not shown:** Windows (the group kill falls back to killing the child alone, and the repository-root comparison is untested there), HTTPS credential prompts, proxies, rate limits. The latency figures in the code comment are from one machine on two afternoons that disagreed, which is why the limit is a bound.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
<!-- END PR TEXT -->

## Facts beside the text (fork-only)

**Where each statement in the PR text comes from** (re-derived this session from the code, the PR heads or a command, not from earlier drafts):

| Statement | Source |
|---|---|
| 17, 12 and 29 new tests; the suites count 177 and 256 | the three classes in the diff; `python3 tools/test_context_budget.py` and `tools/test_methodology_trim.py` (`piece6-upstream-gates-output.txt`) |
| runner 52,839 B to 52,828 B; headroom 283 B to 294 B | `wc -c` on the two trees; the ceiling is 53,122 B (plan §0 item 4); `context_budget.py --status` reads it `ok` |
| `bin/tests.sh` calls `bin/status` 18 times | `grep -o '"$BIN/status" "$P[0-9]*"' bin/tests.sh | wc -l` on the tip |
| a shard cut from a 0600 ledger is 0644 under umask 022, the ledger stays 0600 | `atomic_write` run from the tip's file under umask 022 (S416) |
| #98 and #99 both edit `TRIM_VERSION`; #98 and #96 edit `CHANGELOG.md` | `git diff <merge-base> <head> -- <file>` for each head (S416) |
| raising either floor adds a region against #99; the trimmer's also against #98 | `piece6-floor-trial-output.txt` |
| 0 regions added against #99, #98, #96; #96's `CHANGELOG.md` region is its own | `piece6-merge-trials-output.txt` |
| commit 2 does not apply alone; 1, 3 and 4 do | `piece6-solo-apply-output.txt`; the conflict is in `tools/test_methodology_trim.py` |
| 12/12 gates, 261 passed, 0 failed | `piece6-upstream-gates-output.txt` |
| the `bin/status` run times and the `warn` row | `piece6-smoke-and-latency-output.txt` |
| 12 s to 56 s, 13 s in one test | the same file (148 tests 12.2 s; 177 tests 55.8 s; the hanging-remote test 12.6 s) |
| the highest tag of `git tag --merged HEAD`, not `git describe`'s | `release_lag()` on the tip; `piece6-red-first-output.txt` shows the old code naming `v1.0.1` where `v1.1` was reachable |
| the trailer sentence (S417): the four commits carry `Co-Authored-By`; the hook is `.githooks/commit-msg` and fires when an agent harness is set; #101 proposes removing it | `git log -1 --format=%B <sha> \| grep -c '^Co-Authored-By:'` is 1 for each of `64e1ce00`, `a6935e63`, `12431de1`, `c93f1feb`; `git show upstream/main:.githooks/commit-msg` (lines 12 to 15 and 34: `AI_AGENT`, `CLAUDECODE`, `CLAUDE_CODE_SESSION_ID`, `METHODOLOGY_REQUIRE_COAUTHOR`); `gh issue view 101 -R KJ5HST/methodology` (title and body) |

**Scan for the fork's codes.** The added lines of the diff and the four commit messages were searched for `BL-<n>`, session numbers, `upstream`, `fork`, `the operator`, `Learning #`, `docs/planning`, `issue100`, the plan's labels (`F1` to `F6`, `piece N`, `Batch A`), `scratch clone`, `the plan`, `we chose`, `I measured` and `my`: no hit on the tip. The first scan missed `upstream` (the maintainer's own repository is not "upstream" to him): seven added lines said "upstream issue #100" and one "upstream already has v2.6.1", and are fixed. The S417 re-scan did not include `upstream` either and the word survived in the PR text, in "Upstream's own gates on a clean clone of the tip" (Checks, first bullet), until a second scan with it found it; it now reads "The repository's own gates". The scan now has `upstream` in its pattern, and a scan is run on the PR TEXT block, the added diff lines and the commit messages separately.

**What the cold review changed** (plan §6 has the row): the reviewer's findings and what each came to are in the register. Fixed on the branch: a network call on every test-suite run (now switched off by `METHODOLOGY_REMOTE_CHECK=0`, which `bin/tests.sh` sets), a temp file briefly wider than the file it replaces, the checkout's release read from `git describe`, a directory inside another repository taken for a checkout, a Ctrl-C leaving git and ssh running, a test that depended on the user's git configuration, a zombie read as running, and some wording. Not changed: `LEDGER_NOT_IN_GIT`'s advice to track an ignored ledger (it is the issue's own cause, a note with no exit status); `TRIM_VERSION` (other pull requests edit it); "Phase 0, then 1B" in the runner sentence (the issue's own wording).

**Decided at the S417 Phase 0 picker** (the operator took the option marked Recommended on each of four questions; nothing was sent): (1) **when:** open it in the next session, not after #99 gets a reply (D1 was already taken as (Y), Batch A now, because the trials were clean); (2) **trailers:** the four commits keep the `Co-Authored-By` trailer and the PR text gained the one sentence under its commit table (the maintainer's issue #101, filed 2026-11-01, asks to remove the hook; the hook is still upstream's rule); (3) **the suite's +44 s:** open as stated, it is in the Checks list and is not reduced first; (4) **piece 3:** stays out (D8 (a)), the text says "Refs #100, not Fixes".

**Still the operator's** (nothing here has been sent): the go-ahead for the act itself, in the session that does it: pushing the branch to the fork and opening the pull request, shown to him first with the then-current heads of #99, #98 and #96 and `upstream/main` (a head that moved means `piece-merge-trials.sh` and `plan-evidence.py` re-run first); the three left-alone items above; piece 3 (D8).
