**What this is for.** Issue #100 reports an adopter project that ran 93 sessions on v3.5 over three months while v3.6 to v4.2 were released. `bin/status` called every file `current`: it compares a project with the checkout it syncs from (the local clone of this repository), and nobody had fetched that checkout. So the project never received the tools those releases added for a context that grows without limit (failure mode #28, `context_budget.py`, `methodology_trim.py`). This pull request is the part of #100 that can be written on today's `main` without changing a line that the open pull requests #96, #98 or #99 also change. It has four commits, one for each of four points in the issue. It refs #100 and does not fix it: what is left is listed under "Not in this pull request".

**What is asked of you.** Review and merge. Commit 2 does not apply without commit 1 (both add tests at the same place in `tools/test_methodology_trim.py`); commits 3 and 4 apply on their own. One decision is yours on purpose: commit 4 makes `bin/status` call the network by default, one `git ls-remote` against the checkout's `origin`, stopped after 10 seconds, and `METHODOLOGY_REMOTE_CHECK=0` turns it off. If you would rather it were opt-in, say so; nothing else here depends on it.

## The four commits

**1. `fix(trim): a rewritten file keeps its mode and group…`** (the first "smaller point" in #100)
- Problem: every trim wrote the ledger and each new archive file with permission bits 0600 (read and write for the owner only). `atomic_write` in `starter-kit/methodology_trim.py` made its temporary file with `tempfile.mkstemp`, which always creates 0600 files. A project whose files are shared by a group lost the group's read access on its first trim. Git records only the executable bit, so no commit shows the change.
- Change: `atomic_write` now creates the temporary file with `os.open`. A rewritten file ends up with the permission bits and the group it had before; if the process cannot set the group, the write still succeeds and the file gets the group a new file in that directory gets. A new file gets the user's umask default (0666 minus the umask bits, so 0644 under umask 022). The generated `.verify.sh` proof script is still written 0755. While the temporary file exists it is never readable by more users than the file it replaces.
- New tests: 17, in `tools/test_methodology_trim.py`.

**2. `fix(trim): name a ledger kept out of git…`** (finding 6, the sentence "the trimmer's refusal names this case")
- Problem: a ledger that git does not track (listed in `.gitignore`, never committed, or committed once and untracked since) got no message about git. `--check` printed `trigger FIRES`, then the write path refused with `P1_NO_LEDGER` and the advice "self-provision and reconcile", which cannot work for a file git ignores. For a ledger committed once and untracked since, the write succeeded and the proof script it shipped exited 1 with `absent from HEAD`.
- Change: a new finding, `LEDGER_NOT_IN_GIT`, says which of the three cases applies to the ledger being trimmed and to `CHANGELOG.md` (for an untracked ledger, also the last commit that touched it). `--check` prints it as well as the write path, whenever a trim could happen. It has no exit status of its own: `P1_NO_LEDGER` is still reported with exit 2, and when the ledger is listed in `.gitignore` its advice is now to track the file. This only warns; for a ledger outside git the trimmer still does not prove by content alone that a trim lost nothing.
- New tests: 12, in the same file; 4 of them check behaviour that did not change.

**3. `docs(runner): a new task after STOP is a new session…`** (finding 5, the sentence only)
- Problem: the runner ends close-out with "Then STOP. The session is over." and says nothing about a later instruction in the same conversation. #100 found follow-on tasks that ran as a continuation: none re-ran Phase 0, and two wrote no step 1B claim stub, so a hook keyed on a pending receipt had nothing to fire on.
- Change: one sentence after that line: "A new task in this conversation is a new session: start again at Phase 0, then 1B." The runner's limit in `.context-budget.json` is 18,900 tokens, about 53,122 B at the recorded bytes per token, and the runner was 283 B under it. So one sentence is removed from the "Why this exists" paragraph of step 1B: "The next session has no idea what happened, what was attempted, or what state was left behind." It restates the clause before it, and `ITERATIVE_METHODOLOGY.md` §Phase 1B: Claim the Session says the same. The runner goes from 52,839 B to 52,828 B, so it is 294 B under its limit. No step, condition or failure mode changes.
- New tests: none; this is a document edit. `python3 starter-kit/context_budget.py --status` reads the runner as `ok`.

**4. `feat(status): warn when the methodology checkout is behind…`** (finding 1)
- Problem: `bin/status` compares each project with the history of the checkout it syncs from, and the `synced` check in `context_budget.py` compares a project's copy with the checkout next to it, so a checkout nobody has fetched is never reported as behind.
- Change: `release_lag()` in `starter-kit/context_budget.py` compares the newest release the checkout contains with the newest release tag that the checkout's `origin` lists (`git ls-remote --tags --refs origin`). The checkout's release is the highest `v<N>[.<N>…]` tag in `git tag --merged HEAD`; `git describe`'s nearest tag can be older than a release HEAD also contains after a hotfix line is merged back. When the checkout is behind, the tools print `checkout at v3.5, newest release v4.2 (behind: git pull)`.
- `bin/status` makes the call by default, after its table, in local mode only (`--source=github` has just cloned its source). `context_budget.py` makes it only with `--remote`, so `--status`, the run a session starts with, makes no network call, and `--precommit` never does (a test checks this). In `context_budget.py` a stale checkout is a `warn` row (exit 1), never a breach.
- When the call cannot be made (offline, no `origin`, no release tag, a directory that is not the root of a git repository, or the 10-second limit) it prints one line, `remote not checked: <why>`, and the exit status is the run's own. The commit message describes the process-group kill on timeout and Ctrl-C and the ssh options.
- Also described in `bin/status --help` and `docs/tutorials/T8_keeping_current.md`.
- New tests: 29, in `tools/test_context_budget.py`; each uses a local bare repository or a script that never answers, not the network.

## Where this differs from the proposals in #100
- Finding 1 proposed the line "in `bin/status` and in the `synced` check". `bin/status` makes the call by default; the `synced` check in `context_budget.py` makes it only with `--remote`, so that the run a session starts with makes no network call.
- Finding 6: a warning only (see commit 2).
- Finding 5: the sentence only, no hook recipe.

## Not in this pull request
- Findings 2, 3 and 4; finding 5's hook recipe; the `bin/sync` and `bin/status` warnings about untracked seeds in finding 6; and the other two "smaller points" (the trimmer's `FRONTMATTER_FIELD_ABSENT` warning on the `HANDOFFS.md` seed, and the dashboard's size risk).
- Finding 3, the `bin/` warnings of finding 6, the `BOOTSTRAP.md` line of finding 2 and the recipe in finding 5 are on lines that #99 or #96 also change. Finding 2's step for `SESSION_RUNNER.md` depends on #95 being settled: a fresh sync reads over budget today, so a Phase 0 step that ran the budget tool would report a breach on day one. Finding 4 depends on the answer to the question about `SESSION_NOTES.md` in the comment on #100.
- Also left out, because other open pull requests change those lines: the `TRIM_VERSION` bump, the `.quality-gates.json` floors, and a `CHANGELOG.md` entry. The unit suites now count 177 tests for `context-budget-unit-tests` (floor 148) and 256 for `trimmer-unit-tests` (floor 227). Raising a floor here would add a conflict region against #99, and the trimmer's also against #98.

## Who receives what
- On their next `bin/sync` (these files are distributed): the runner sentence, the trimmer changes and `context_budget.py --remote`.
- Only people with a checkout (`bin/status` is not distributed): the `bin/status` line.
- Files already at 0600 stay at 0600; run `chmod` on them once. A new file follows the umask, so a shard cut from a 0600 ledger is 0644 under umask 022.
- A project whose checkout is never brought current receives none of this. The check shortens the time to notice for a project whose checkout is.

## Checks
- On a clean clone of the tip (`python3 starter-kit/quality_ratchet.py --run`): 12 of 12 gates pass, 0 fail, 0 unmeasured. `bash bin/tests.sh` passes 261 checks and fails 0. The four unit suites run 229 (dashboard), 177 (context budget), 256 (trimmer) and 45 (quality ratchet) tests.
- Merged with the head of each open pull request (`git merge-tree --write-tree` with attributes off, which is how GitHub checks), this branch adds no conflict region that the head did not already have: #99 and #98 merge cleanly with and without it; #96 conflicts only in `CHANGELOG.md`, with or without it.
- A read-only run against this repository from a checkout at v4.1: `bin/status` printed the warning line, and whole runs took 2.5 to 3.0 s against 1.7 to 2.2 s with the check off (5 runs each). `context_budget.py --status --remote` printed a `warn` row for the checkout.
- The `git ls-remote` call took 0.3 to 3.7 s against github.com from one machine on two afternoons; the 10-second limit is a bound, not a typical time.
- Cost: `tools/test_context_budget.py` takes 36 s instead of 7 s (one run each, on one machine), and 11 s of that is the one test that runs until the 10-second limit expires.

**Not shown:** Windows (the process-group kill falls back to killing the child alone, and the comparison that decides whether a directory is the root of a git repository is untested there), HTTPS credential prompts, proxies, rate limits.

The four commits end with the `Co-Authored-By` line that the Disclosure Hook (`.githooks/commit-msg`) requires when an agent harness is detected; drop those lines before merging if you prefer, as #101 proposes for the hook itself.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
