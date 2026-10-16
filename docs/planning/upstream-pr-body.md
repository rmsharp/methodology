# The text of the one upstream pull request (draft 8)

**Status: DRAFT 8, not frozen, nothing sent.** Draft 8 is draft 7 (`93245dc`) cut to a byte budget at his direction ("Cut it, then one more read"): from 25,959 B to 20,000 B or less, by the readers' cut list (the commit table, the
12-projects paragraph, the conflict paragraph) and by tightening, with nothing added except what keeps a disclosure the cut text alone carried. His answer at the same picker also takes out draft 7's offer in decision 1 to rebuild any
commit separately. The history: draft 1 is `ef98e78`, draft 2 `a6ad168`, draft 3 `025afed` (and `ab4f563` with its figures); draft 4 `d5bb53b`, draft 5 `9becf89` and draft 6 `dfc31ab` were each read by a fresh agent (5, 5 and 6 of 10);
draft 7 (`93245dc`) had no read. Each reader's findings and what became of them are in [`pr-composition-evidence/draft4-record.md`](pr-composition-evidence/draft4-record.md); the read of draft 8 is added there.
**Draft 8 has had no read of its own until that record says so.** Everything below the rule is the text that would be posted: the title on its own line, then the body. Written for `KJ5HST/methodology` from the local branch
`pr2/candidate` at `a62bfec` (32 commits over `upstream/main` `f34769f`). Every number in it is printed by a command named beside it, and the text is read by `pr4-body-check.py`.

---

**Title:** A methodology/ directory for a project's framework files, and bin/migrate-layout to move a project there

@KJ5HST:

This pull request lets a project keep all of the framework's files in one directory, `methodology/`. Today they sit in two places: 18 at the project root, among the project's own files, and 12 under `docs/methodology/`. Every tool in the repository learns to find the files in either place. A project that changes nothing keeps its current locations, and a new command, `bin/migrate-layout`, moves a project when its owner chooses.

The numbered items I mention: #93 is my issue about the proof scripts that the ledger trimmer (`methodology_trim.py`) generates, and #94 is my pull request that fixes it; #92 is my pull request with the release notes for v4.2; #67 was your issue about the dashboard's stale-copy warning, and #73 your pull request that fixed it. Every number below comes from a command, or is rounded from one; the scripts and their saved output are in [my fork's evidence directory](https://github.com/rmsharp/methodology/tree/main/docs/planning/pr-composition-evidence).

## What I am asking you to decide

1. **Do you want the single directory?** I asked for it for my own 12 projects, to clear the project root and show which files belong to the framework; I found no issue on your repository that asks for it. The 30 rows of `bin/_manifest.py` are 18 files at a project's root (11 that `bin/sync` keeps current, and 7 "seeds", which it writes once, when the project lacks them, and the project owns afterwards) and 12 documents under `docs/methodology/`. With the directory, all 30 sit in one place. That is the only benefit. It costs this repository: the code that decides a project's layout is copied into 11 files; 138 lines name a file by its root path on purpose and carry a same-line comment, `# layout: ok -- <reason>`; 36 relative links became plain names in code spans (a relative link that is right in one layout is dead in the other); and `bin/migrate-layout` (1,457 lines) and its 280 tests are new. It costs projects: even a project that never moves receives 19 changed files at its next `bin/sync`, reads two framework files that are 244 bytes larger, and finds the first paragraph of `SESSION_RUNNER.md` changed (it says where to look for the other framework files). One known gap bears on this decision: a ledger hook that a project installed itself keeps looking for the ledger at the root, so once the ledger has moved it passes a commit that has no ledger entry, without saying so. The branch is 32 commits and adds 19,826 lines.
   - If you do not want the directory, the first commit, `bbe0dc3`, can be taken alone on your current code (271 passed, 0 failed, 0 skipped and 12/12 gates, in a clean clone). The other commits sit on top of the directory work, and I have not tested them without it.
2. **Which of the dashboard changes do you want?** These come with the earlier work in `bbe0dc3`, and they are policy, not fixes. Please tell me which to remove and I will remove them. The other dashboard changes in `bbe0dc3` (2.11.3 to 2.21.0) are not itemised here; I will itemise them on request.
   - (a) The dashboard's `--sync` takes an optional directory: with one, it writes only that project; without one, every project it finds. It skips a target that git tracks, or a brand-new file the project's `.gitignore` does not cover, unless `--force` is given. Your pull request #73 made the stale-copy warning say `cp <canonical> <copy>`; this branch's warning says `--sync <directory>` instead. Both answer #67 (a remedy that rewrote 26 files in 25 repositories).
   - (b) `"methodology"` is no longer in `EXCLUDE_DIRS`, so a run of the dashboard over a directory of projects scores this repository too.
   - (c) How the dashboard recognises a project's installed copy of a framework tool is now one table, and the list of names (`FRAMEWORK_INSTALLED_SOURCE`) is derived from it; yours keeps the list and a separate signature table, with a test that they agree. The same 7 names are recognised either way, but the trimmer loses its signature fallback: a copy with no `TRIM_VERSION` line is no longer recognised. All 4 versions of the trimmer in your history have that line.
   - Five new risk rows: two for a file past the limits of an agent's file read (256 KiB, past which the read is refused, and a budget of 25,000 tokens, past which it is cut short with a banner; counted at 2.27 bytes per token, the densest content measured, so 56,750 B); two for a file a session is told to read whole, such as a backlog, when it is past that budget (lower severity if the project's own trimmer can archive it, higher if not); and one that repeats the trimmer's own size trigger (192 KiB). The thresholds are my choices.
   - Four of your tests are removed: the three in `TestCliRemedyProportionality`, because (a) replaces the remedy they assert, and `test_every_framework_installed_source_name_has_a_signature`, because (c) derives the list of names from the signature table, so the two cannot disagree.
3. **In what order should this and #94 go?** This branch and #94 both rewrite `starter-kit/methodology_trim.py` and its tests. `git merge-tree` reports conflicts in 3 files and 17 regions (the trimmer 10, its tests 6, `.quality-gates.json` 1); #92 merges cleanly. Taking only `bbe0dc3` would still conflict with #94, in 6 regions in 2 files. This branch contains my fix for #93 inside `bbe0dc3`. #94 adds 430 lines to the trimmer and 1,136 to its tests; this branch contains all but 11 of the trimmer lines and all but 9 of the test lines as identical lines (`pr4-supersede.sh` prints the 20). The minimum for the `trimmer-unit-tests` gate is 181 in #94 and 218 here (`pr4-supersede.sh`). Please say whether I should wait for #94 and rebase on it, or whether this pull request should supersede it. I have not resolved the conflicts.
4. **Three smaller choices.**
   - `ced2c82` drops a duplicated example command (84 B) from the runner (`SESSION_RUNNER.md`) so that it reads under its token ceiling. The same commit also re-records the runner's bytes-per-token ratio in `.context-budget.json`, as that file's own rule asks, which lets the runner grow 43 B more before the budget tool (`context_budget.py`) reports it over. That second change can be dropped on its own; the cut alone is enough to pass.
   - Ten commits remove references that only my fork can resolve, such as backlog and session codes in comments and messages. Please tell me whether to keep them or drop them. If you keep them, a merge commit or a rebase leaves them as a separable run; a squash folds them in. A search for such codes still matches 56 added lines (some may be legitimate): `git diff f34769f HEAD -- . ':!docs' | grep -E '^\+[^+]' | grep -cE 'BL-[0-9]+|\bS[0-9]{2,3}\b|\bD[0-9]{1,2}\b|Learning #[0-9]+'`.
   - No `CHANGELOG.md` entry and no change to `README.md` or `CLAUDE.md` (which list the files) is included; the 32 commits were made without your pre-commit hook, which would require a ledger entry in each. Please say if you want one entry for the whole pull request. Whether it needs a new release version is yours to say; I have not made one, and release notes would be a separate pull request after a merge, as with #92.

These four items are complete in themselves. The sections below give the detail behind them and the evidence.

## Size, what reaches a project, and what it costs

**Size.** The branch adds 19,826 lines and removes 1,152 (`git diff --shortstat f34769f HEAD`). Most of that never reaches a project. `bin/sync` writes 19 of the changed files into a project, with 2,959 lines added and 530 removed in all; 3 more changed files are templates that only a new project receives. The other 25 files, with 16,860 of the added lines (85%), stay in this repository: tests, tools that only this repository runs, and its gate configuration. The dashboard is counted twice in that total (as `starter-kit/methodology_dashboard.py` and as an identical copy in `tools/`). About 43% of the added lines (8,461, in `bbe0dc3` and `c8c0b21`) are earlier work of mine that is not about the directory (`pr4-distribution.py`).

**What it costs to use.** A session must read two of the framework's files in full, `SESSION_RUNNER.md` and `SAFEGUARDS.md`. Together they are 244 bytes (0.35%) larger on this branch, about 90 tokens at 2.81 bytes per token. The programs a session runs (the dashboard, the trimmer's check, the budget tool) took the same time as upstream's versions, within 0.1 s on two test projects; the dashboard took 0.59 to 0.63 s here against 0.66 to 0.68 s for upstream's on a project of 488 commits (`pr4-cost.sh`).

## What the change does

- **Paths.** `bin/sync` writes a project that keeps the current layout (called `legacy` in the tools' `--layout` options) the same paths it writes today (measured below). `bin/sync` and `bin/check-links` take `--layout`; `bin/status` and every other tool read either layout. The manifest has a second table, `NEW_LAYOUT`, giving each file's place under `methodology/`; it is plain data, so `bin/sync --source github` (which clones the framework repository) can read it without running it.
- **No tool guesses where the files are.** `tools/layout_resolver.py` is a short block of code that decides a project's layout from where an anchor file sits. The default anchor is `SESSION_RUNNER.md`: at the root, the current layout; under `methodology/`, the new one; in both places, the tool refuses and names both. A tool that reads a ledger anchors on that ledger instead, and the ratchet and the budget tool on their configuration file, so a project that moved only the framework's files (`--tier 1`) is read correctly. For a file other than the anchor that exists in both places (for example a project's own product `CHANGELOG.md`), the tool reads the copy under `methodology/` as the framework's and leaves the other alone, but only when the runner is under `methodology/` and not at the root; otherwise it refuses. The block is copied into 10 tools and into the dashboard's identical copy, because the four tools a project receives (`methodology_dashboard.py`, `methodology_trim.py`, `context_budget.py`, `quality_ratchet.py`) are single files that import only the standard library. `python3 tools/test_layout_resolver.py` fails until all 11 copies are equal.
- **Moving a project.** `bin/migrate-layout` makes no change unless given `--apply`. `--tier 1` moves the framework's files, `--tier 2` the project's own state (its seed files, the files the tools generate, the archive shards the trimmer wrote, and the project-owned PROJECT_LEARNINGS.md that `BOOTSTRAP.md` names), `all` (the default) both.
  - *It refuses, before writing anything,* a tree that is not a git repository with a commit; has uncommitted changes; is half-migrated (a runner at the root and another under `methodology/`); already holds a destination file; keeps its framework files out of git (its `.gitignore` lists them); is not current with what `bin/sync` would write; or has a file to rewrite that it cannot rewrite safely (for example, a ledger with a code fence that never closes).
  - *An apply is one commit.* It moves the files, rewrites the moved paths in `CLAUDE.md`, in anchored `.gitignore` entries and in `.context-budget.json` and `.quality-gates.json`, and adds a ledger entry. Every move must remain a rename at 90% similarity or better, so that `git log --follow` still reaches the history; a ledger too small for that fails, and the apply is rolled back (exit 3), as is any step that fails before the commit. The report names `git revert <commit>` as the way back.
  - *It checks itself.* Before and after the commit it runs read-only checks (`bin/status`, the two ledger checkers, `bin/check-links`, every archive shard's proof, and how far `git log --follow` reaches). If a result differs afterwards, it exits 4 and keeps the commit (`--skip-checks` turns the checks off).
  - Like `bin/sync` and `bin/status`, it is not in `bin/_manifest.py`; a project runs it from a checkout of this repository. Its 280 tests take about 6 minutes, so the two gates that run them each set `timeout_seconds` to 3600.

## What the commits contain

Each commit's message describes it. A suggested order for reading: `bbe0dc3`, then `14ef959` (the foundation: the layout code, test projects in both layouts, `bin/check-layout-literals`, which finds a tool that names a file by its root path, and `NEW_LAYOUT`), then the rest in order. The last commit, `a62bfec`, corrects four stale statements in comments and gate reasons and changes no code path or threshold.

- **`bbe0dc3` (9 files, +7,765 / -575), earlier work.** The dashboard 2.11.3 to 2.21.0 and the ledger trimmer 1.5.0 to 1.7.0, with their tests. The trimmer change is my fix for #93, which is why it overlaps #94. In `bin/tests.sh`: three blocks changed so that `cmd | grep -q` under `pipefail` cannot report a match as a failure, a lint for that pattern, a `skip` helper (a test reported as skipped, not passed) and an executable-bit check derived from the manifest. It also adds to `BOOTSTRAP.md` a row, in its table of files `bin/sync` never overwrites, that names every seed; adds 11 lines to `FRAMEWORK_APPARATUS.md`; and raises three thresholds in `.quality-gates.json`. It fixes one defect: `git log --reverse --format=%ai -1` applies `-1` before it reverses, so `first_commit_date` was the newest commit and a project's age was the days since its last commit; the dashboard now reads the root commits (`--max-parents=0`).
- **`c8c0b21` (4 files), earlier work.** The quality ratchet's 1.4.0 and 1.5.0. A gate may set `timeout_seconds`; a command that outlives it is reported `unmeasured` (its result could not be determined), not as exit code 127, and its whole process group is stopped. Two gates that read the same command's output share one run of it. Changing `timeout_seconds` is a warning, not a refusal. It does not depend on the layout, but it is built on the ratchet's layout commit `fd96593`.
- **`5afc962` (5 lines), a small change elsewhere.** A rule in `starter-kit/HANDOFFS.md` and `HOW_TO_USE.md` for a close-out receipt that cites a gate run: a gate that read `unmeasured` must be repaired, or named in the receipt. Its check is in my version of `bin/check-handoff`, which is not carried, so the rule is prose only.
- **One of your tests is rewritten** (`4c0bdde`): Test 15 now counts the status table's rows, because `bin/status` prints a `layout:` line that names the project and the old assertion counted lines naming the project (31 for 30 files).
- **Whole files, not hunks.** For the dashboard and the trimmer this pull request contains whole files, because my versions had diverged from yours: a three-way merge of your copy with mine, from the copy my work began with (`c8b9ddd`), conflicts in 51 places in 8 files (`pr4-mergefile.sh`, with my fork's `main` as of `e7b389f`). For `bin/check-ledger` and `bin/check-handoff` it contains the layout hunks only.

## What a project sees

**A project that keeps the current layout gets the same paths.** Sync two temporary test projects, one with upstream's `bin/sync` and one with this branch's, and compare:

```
git init a-up && git -C a-up commit --allow-empty -m init ; cp -R a-up a-pr
python3 <upstream checkout>/bin/sync a-up ; python3 <this branch>/bin/sync a-pr
diff -rq --exclude=.git a-up a-pr
```

Both write the same 30 paths and neither makes a `methodology/` directory. 22 of the 30 differ in bytes, and every one is a file this pull request changes: the cost of the next sync to a project that did not ask for the change. With its 7 seeds edited and its framework files at upstream's tip, upstream's `bin/sync` writes 0 paths; this branch's writes 19, needs no `--force`, and changes 0 of the 7 seeds (`pr4-fixture.sh`).

**A project that has moved is synced where its files are.** Take a project whose 30 files are already under `methodology/`. The `bin/sync` on `main` today writes 30 paths outside `methodology/`, a second copy of every framework file and seed; this branch's writes none (`pr4-moved.sh`). So once a project can move, the sync tools have to change with it. On my 7 projects that had moved, the `bin/sync` on `main` created 41 seed files at the root across six of them, and two projects' own pre-commit hooks refused the resulting commit as half-migrated.

**My own 12 projects** (7 under `methodology/`, 5 not; `pr3-adopters.py` is the method) are mine, so you cannot run this on them. Without `--force`, this branch's `bin/sync` refuses 10 of them, over 39 files: 38 are versions from my fork's history that no commit of this branch carries, and one is a project's own 49 added lines in `methodology_trim.py`, which `--force` drops without saying so. After one `--force`, a plain run writes nothing at any of the 12; it changed none of their seeds.

## Evidence

Each check ran in a fresh `--no-local` clone of the head with no modified files, serially; upstream's tip is the control. `pr4-claims.sh` runs them all (about 35 minutes).

| Check | Command | upstream `f34769f` | this branch |
|---|---|---|---|
| The suite passes and has more tests | `bash bin/tests.sh` | 261 passed, 0 failed | 302 passed, 0 failed, 0 skipped |
| Every declared gate holds | `python3 starter-kit/quality_ratchet.py --run` | 12/12 pass, 0 fail, 0 unmeasured | 18/18 pass, 0 fail, 0 unmeasured |
| Links resolve in both layouts | `python3 bin/check-links --layout both` | usage error: it takes only `--tree` (exit 2) | OK: 80 links across 23 documents, in each layout (116 at your tip) |
| No tool names a file by a root path without saying why | `python3 bin/check-layout-literals` | not present | 15 files scanned, 0 unacknowledged sites |
| One copy of the layout-deciding code | `python3 tools/test_layout_resolver.py` | not present | 76 tests OK; 11 copies, each equal to the master |
| No gate threshold in `.quality-gates.json` is lowered | `quality_ratchet.compare`, each commit against its parent | | 0 refusals over 32 commits; gates 12 to 18; five thresholds raised |

I ran the suite and the gates at the last commit of each group of commits, not at every commit.

## What this does not show, and what is missing

- **The route a project takes alone from GitHub:** every sync above used the local source, not `bin/sync --source github`.
- **Any project that is not mine:** the 12 are mine, and 10 carry versions of the framework's files that are in no history here.
- **Windows, your machine, a project's own CI:** this repository has no CI, so every check is local.
- **My fork's own suite:** some of its test blocks read my fork's ledgers as test data and are not carried.

## Known gaps

These came from the 12 projects and are open:

- A sync refuses a project's edited framework file by name but does not say which published version is nearest or how many lines differ, and `--force` then drops the edit (the `bin/sync` on `main` does the same).
- With only the framework's files moved (`--tier 1`), the dashboard writes a second history file, `dashboard_history.jsonl`, under `methodology/` while the one at the root stays, unused.
- On a ledger in the old format (no month headings), the migration appends its entry at the end, so the entries are no longer in one order; `bin/check-ledger` already fails on such a ledger and still fails after.
- For the hook that `context_budget.py install-hook` writes, the migration warns that it "will refuse the migration commit". In fact the hook does not refuse it.
- A ledger hook that a project installed itself keeps looking for the ledger at the root, so once the ledger moves it passes a commit with no ledger entry, without saying so. The hook in this branch follows the ledger.
- A project's own tests or scripts that read a moved file by name can break. The migration lists the other files whose text mentions a moved name; the list is an upper bound, not the set that breaks.
