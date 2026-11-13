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
