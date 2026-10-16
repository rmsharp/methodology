# The text of the one upstream pull request (draft 5)

**Status: DRAFT 5, not frozen, nothing sent.** Draft 5 follows a fresh reader's report on draft 4 (`d5bb53b`); draft 4 was a recomposition of draft 3 (`ab4f563`) in plainer,
formal language at his direction. Draft 1 is `ef98e78`, draft 2 `a6ad168` and draft 3 `025afed`; a fresh reviewer read each of the first two
([`pr-composition-evidence/pr4-record.md`](pr-composition-evidence/pr4-record.md)), and the reader's findings on draft 4, each checked before it was acted on, and the read of
draft 5 are in [`pr-composition-evidence/draft4-record.md`](pr-composition-evidence/draft4-record.md). Everything below the rule is the text that would be posted: the title on
its own line, then the body. Written for `KJ5HST/methodology` from the local branch `pr2/candidate` at `a62bfec` (32 commits over `upstream/main` `f34769f`). Every number in
it is printed by a command named beside it, and the text is read by `pr4-body-check.py`.

---

**Title:** A methodology/ directory for a project's framework files, and bin/migrate-layout to move a project there

@KJ5HST:

This pull request lets a project keep all of the framework's files in one directory, `methodology/`. Today they sit in two places: 18 at the project root, among the project's own files, and 12 under `docs/methodology/`. Every tool in the repository learns to find the files in either place. A project that changes nothing keeps its current locations, and a new command, `bin/migrate-layout`, moves a project when its owner chooses.

The numbered items I mention: #93 is my issue about the proof scripts the ledger trimmer generates, and #94 is my pull request that fixes it; #92 is my pull request with the release notes for v4.2; #67 was your issue about the dashboard's stale-copy warning, and #73 your pull request that fixed it. Every number below comes from a command. The scripts that run them, and their saved output, are in [my fork's evidence directory](https://github.com/rmsharp/methodology/tree/main/docs/planning/pr-composition-evidence); the `pr3-` and `pr4-` in their names are my own numbering and mean nothing for this review.

## What I am asking you to decide

1. **Do you want the single directory?** The 30 rows of `bin/_manifest.py` are 18 files at a project's root (11 that `bin/sync` keeps current, and 7 "seeds", which it writes once, when the project lacks them, and the project owns afterwards) and 12 documents under `docs/methodology/` (also kept current). With the directory, all 30 sit in one place and the root shows which files are the framework's. That is the whole benefit. It costs the repository this: the code that decides a project's layout is copied into 11 files; 138 lines name a file by its root path on purpose and carry a marker saying why; 36 relative links became plain names in code spans; and `bin/migrate-layout` (1,457 lines) and its 280 tests are new. If you do not want the directory, the first commit, `bbe0dc3`, can be taken alone on your current code (271 passed, 0 failed, 0 skipped and 12/12 gates, in a clean clone of it). The other commits cannot be taken without the directory work; that includes `c8c0b21`, whose ratchet changes are not about layout but are built on a layout commit.
2. **Which of the dashboard changes do you want?** Three design choices, five new risk rows and the removal of four of your tests are policy, not fixes. They are described under "What the commits contain". Please tell me which to remove and I will remove them.
3. **In what order should this and #94 go?** This branch and #94 both rewrite `starter-kit/methodology_trim.py` and its tests. `git merge-tree` reports conflicts in 3 files and 17 regions (the trimmer 10, its tests 6, `.quality-gates.json` 1); #92 merges cleanly. This branch contains my fix for #93 inside `bbe0dc3`, together with other dashboard work. Of the 430 lines #94 adds to the trimmer, all but 11 are present here as identical lines (the version string, comment wording, and the tool's name in four messages); of the 1,136 lines it adds to the tests, all but 9 (comments and docstrings). The minimum for the `trimmer-unit-tests` gate in `.quality-gates.json` is 181 in #94 and 218 here (`pr4-supersede.sh`). Please say whether I should wait for #94 and rebase on it, or whether this pull request should supersede it. I have not resolved the conflicts.
4. **Four smaller choices.**
   - `ced2c82` changes `.context-budget.json` in a way that loosens the budget tool's line for the runner by 43 B; the change can be dropped on its own (the other change in that commit is enough to make the check pass).
   - Ten commits remove references that only my fork can resolve, such as backlog and session codes in comments and messages. They can be skipped as a group, in which case those references stay. A merge commit or a rebase keeps them skippable; a squash does not.
   - A `CHANGELOG.md` entry, and any change to `README.md` or `CLAUDE.md` (which list the files), are not included. The 32 commits were made without your pre-commit hook, which would require a ledger entry in each. Please say if you want one entry for the whole pull request, and I will add it.
   - I have not changed the framework's release version. Release notes would be a separate pull request after a merge, as with #92.

## Size, what reaches a project, and what it costs

**Size.** The branch has 32 commits and adds 19,826 lines (it removes 1,152): `git diff --shortstat f34769f HEAD`. Most of that never reaches a project. `bin/sync` copies 19 of the changed files into a project, with 2,959 lines added and 530 removed in all; 3 more changed files are templates that only a new project receives (7 added, 4 removed). The other 25 files, with 16,860 of the added lines (85%), stay in this repository: tests, tools that only this repository runs, and its gate configuration. The dashboard is counted twice in the total, as `starter-kit/methodology_dashboard.py` and as an identical copy in `tools/`. `pr4-distribution.py` derives these figures from the manifest, `bin/_manifest.py`.

**Earlier work that is not about the directory.** About two fifths of the added lines (8,461, in `bbe0dc3` and `c8c0b21`) are earlier work of mine on the dashboard, the ledger trimmer and the quality ratchet, on which the directory work is built. 1,566 of those lines are the same work as my pull request #94. `bbe0dc3` can be taken alone; `c8c0b21` depends on a layout commit (decision 1).

**What it costs to use.** A session must read two of the framework's files in full, `SESSION_RUNNER.md` and `SAFEGUARDS.md`. Together they are 244 bytes (0.35%) larger on this branch, which is about 90 tokens at the budget tool's rate of 2.81 bytes per token. The programs a session runs took the same time as upstream's versions: the dashboard, the trimmer's check and the budget tool each finished within 0.1 s of upstream's on two test projects (`pr4-cost.sh`).

That is everything you need to decide. The rest is the detail behind it: what the change does, what each commit contains, what a project sees, the evidence, and the gaps.

## What the change does

- **Paths.** `bin/sync` writes a project that keeps the current layout (called `legacy` in the tools' `--layout` options) the same paths it writes today (measured below). Every tool reads either layout.
- **Moving a project.** `bin/migrate-layout` makes no change unless given `--apply`. `--tier 1` moves the framework's files; `--tier 2` moves the project's own state (its seed files, the files the tools generate, the archive shards the trimmer wrote, and a project-learnings file); `all`, the default, moves both. Before writing anything, it refuses a tree that: is not a git repository with a commit; has uncommitted changes; is half-moved (a runner at the root and another under `methodology/`); already holds a destination file; keeps its methodology files out of git (listed in `.gitignore`); is not current with what `bin/sync` would write; or names a moved path in a file that the tool cannot safely rewrite. An apply is one commit. It moves the files; rewrites the moved paths in `CLAUDE.md`, in anchored `.gitignore` entries and in `.context-budget.json` and `.quality-gates.json`; and adds a ledger entry. Every move must remain a rename at 90% similarity or better, so that `git log --follow` still reaches the history; a ledger too small to take its entry fails that test, and the apply is rolled back (exit 3). A step that fails before the commit is also rolled back. After the commit the tool repeats read-only checks that it ran before: `bin/status`, `bin/check-ledger`, `bin/check-handoff`, `bin/check-links`, the proof of every archive shard, and how far `git log --follow` reaches from the ledger. If any result differs, it exits 4, keeps the commit and prints the `git revert` command (`--skip-checks` turns the checks off). Like `bin/sync` and `bin/status`, it is not in `bin/_manifest.py`; a project runs it from a checkout of this repository.
- **No tool guesses where the files are.** `tools/layout_resolver.py` is a short block of code that decides a project's layout from where an anchor file sits. The default anchor is `SESSION_RUNNER.md`: at the root, the project has the current layout; under `methodology/`, the new one; in both places, the tool refuses and names both. A tool that reads a ledger anchors on that ledger instead (`CHANGELOG.md` or `HANDOFFS.md`), and the ratchet and the budget tool anchor on their configuration file, so a project that moved only the framework's files (`--tier 1`) is read correctly. One exception to the refusal: when `SESSION_RUNNER.md` is under `methodology/` and not at the root, a file found in both places is read as the framework's copy under `methodology/`, and the copy at the root is left alone as the project's own. The block is copied into 10 tools and into the dashboard's identical copy. The four tools that a project receives, `methodology_dashboard.py`, `methodology_trim.py`, `context_budget.py` and `quality_ratchet.py`, are single files that import nothing outside the standard library, so each carries its own copy. `python3 tools/test_layout_resolver.py` asserts that all 11 copies equal the master.

## What the commits contain

**Earlier work that is not about the directory.**

- **`bbe0dc3` (9 files, +7,765 / -575).** The dashboard 2.11.3 to 2.21.0 and the ledger trimmer 1.5.0 to 1.7.0, with their tests. The trimmer change is my fix for #93, which is why it overlaps #94: its 430 trimmer lines and 1,136 test lines are #94's counts. In `bin/tests.sh`, three blocks changed so that a pipeline of the form `cmd | grep -q` under `pipefail` cannot report a match as a failure; a lint for that pattern; a `skip` helper, which reports a test as skipped, not passed; and an executable-bit check derived from the manifest. The commit also adds to `BOOTSTRAP.md` a row, in its table of files that `bin/sync` never overwrites, that names every seed; 11 lines in `FRAMEWORK_APPARATUS.md` for the trimmer's new warning; and raises three thresholds in `.quality-gates.json`. The layout commits for the dashboard and the trimmer build on it.
- **`c8c0b21` (4 files).** The quality ratchet's 1.4.0 and 1.5.0. A gate may set `timeout_seconds`; a command that outlives it is reported `unmeasured` (its result could not be determined), not as exit code 127, and its whole process group is stopped. Two gates that read the same command's output share one run of it. Changing `timeout_seconds` is a warning, not a refusal. The `_gate_schema` entry in `starter-kit/quality-gates.json`, which lists a gate's keys, now names `timeout_seconds`. This does not depend on the layout, but it is built on the ratchet's layout commit `fd96593` and cannot be taken without it.
- **Four of your tests are removed.** The three in `TestCliRemedyProportionality` (the stale-copy warning's `cp` remedy, from #67 and #73), because dashboard choice (a) below replaces that remedy and this branch's tests assert the new one; and `test_every_framework_installed_source_name_has_a_signature`, because dashboard choice (c) derives the list of names from the signature table, so the two cannot disagree.
- **Three design choices in the dashboard** come with that work:
  - (a) The dashboard's `--sync` takes an optional directory, and skips a target that git tracks, or a brand-new file the project's `.gitignore` does not cover, unless `--force` is given. Your pull request #73 made the stale-copy warning say `cp <canonical> <copy>`; this branch's warning says `--sync <directory>` instead.
  - (b) `"methodology"` is no longer in `EXCLUDE_DIRS`, so a portfolio run scores this repository too.
  - (c) How the dashboard recognises a project's installed copy of a framework tool is now one table, and the list of names (`FRAMEWORK_INSTALLED_SOURCE`) is derived from it. Yours keeps the list and a separate signature table, with a test that they agree. The same 7 names are recognised either way, but the trimmer loses its signature fallback: a copy with no `TRIM_VERSION` line is no longer recognised (the code's own note says every release has one).
- **Five new risk rows** in the dashboard (its `risks.append` sites go from 29 to 34 in `bbe0dc3`, and to 35 at the head with the half-moved row of the layout work): two for a file too large for an agent to read in one read (a hard limit of 256 KiB, and a budget of 25,000 tokens, counted at no fewer than 2.27 bytes per token), two for an oversized backlog (with and without a remedy available in the project), and one that re-reports the trimmer's trigger (192 KiB). The constants are mine and are policy too.
- **One defect fixed.** `git log --reverse --format=%ai -1` applies `-1` before it reverses, so `first_commit_date` is the newest commit and a project's age is the days since its last commit. The dashboard now reads the root commits (`--max-parents=0`).

This pull request contains whole files, not the layout hunks, because my copies of those tools had diverged from yours and the hunks do not apply: a three-way merge of your copy, the copy this work started from (`c8b9ddd`) and my fork's `main` at `e7b389f` conflicts in 51 places in 8 files (`pr4-mergefile.sh`; fetch my fork's `main` to get both commits).

**All 32 commits, by group.** The branch changes 47 files (38 changed, 9 new). I ran the suite and the gates in a clean clone at the last commit of each group below, and I did not re-run every commit alone.

| Commits | What |
|---|---|
| `bbe0dc3` | Earlier work, not the directory (above) |
| `14ef959` | The foundation of the directory work: `tools/layout_resolver.py`, `tools/layout_fixtures.py` (test projects in both layouts), `bin/check-layout-literals` (finds a tool that names a file by its root path), and `NEW_LAYOUT`, a second table in `bin/_manifest.py` that gives each file's place under `methodology/`; it is plain data, so `--source=github` can read it without running it |
| `fd96593`, `c8c0b21` | The ledger pre-commit hook and the quality ratchet read either layout (ratchet 1.3.0); then ratchet 1.4.0 and 1.5.0, which are not about layout |
| `98ca7fc`, `e9c5cb8`, `dd581fe` | The trimmer 1.8.0, `context_budget.py` 1.4.0 and the dashboard 2.22.0 each find a project's files in either place; the trimmer writes its archive shard and proof beside its ledger. `98ca7fc` also adds `tools/fixtures/trim-verify-template-1.7.0.sh` (406 lines: the 1.7.0 proof script, frozen so that a test can compare against it) |
| `4c0bdde`, `261b8d3`, `0aa1897` | `bin/sync` (`--layout auto\|legacy\|new`), `bin/status`, `bin/check-links` (`--layout legacy\|new\|both`) and the manifest reader, which reads `NEW_LAYOUT` as data for `--source=github`, with an 82-test suite. `4c0bdde` rewrites your Test 15 assertion to count the status table's rows, not every line that names the project |
| `a459b8b`, `505541c` | `bin/check-ledger` and `bin/check-handoff` read either layout (the layout hunks only; the rest of my versions of them stays on my fork) |
| `c8d4375` to `18cda0f` | The documents say where the files sit, and their references hold in both layouts: 36 relative links became plain names in code spans (`python3 bin/check-links` counts 116 links across the 23 distributed documents at your tip and 80 at the head), and the first paragraph of `SESSION_RUNNER.md` tells every project, including one that keeps the current layout, to look beside the runner, and says where such a project keeps the other files. `bin/check-links --layout both` runs in `bin/tests.sh` |
| `2942e46`, `ab35e96` | `bin/migrate-layout` and its 280-test suite. `bin/tests.sh` runs two fast classes of it; all 280 run through two gates that each set `timeout_seconds` to 3600, because they take about 6 minutes |
| `5afc962` | A rule for a receipt that cites a gate run: a gate that read `unmeasured` (its command did not finish) must be repaired, or named in the receipt (`starter-kit/HANDOFFS.md`, `HOW_TO_USE.md`; 5 lines) |
| `c933b0f` to `28f99a7` | The ten commits that remove references only my fork can resolve (decision 4): seven in comments and docstrings (no program token changes) and three in text a program prints. At least 56 added lines of that kind remain (the pattern does not look for the codes of my own planning documents), 36 of them starting with `#` or `//` (`git diff f34769f HEAD -- . ':!docs' \| grep -E '^\+[^+]' \| grep -cE 'BL-[0-9]+\|\bS[0-9]{2,3}\b\|\bD[0-9]{1,2}\b\|Learning #[0-9]+'`) |
| `ced2c82` | `python3 starter-kit/context_budget.py --status` read `SESSION_RUNNER.md` as over its token ceiling after the documents commits; this drops one duplicated example command (84 B). It also changes three lines of `.context-budget.json` (the runner's recorded bytes-per-token ratio, its measured size and a note), which loosens the budget tool's line for the runner by 43 B; that tool is not one of the 18 gates (decision 4) |
| `a62bfec` | Four statements the series left stale, corrected in text only: the `layout-literals` gate's reason said two checkers are not scanned (they are), the `layout-unit-tests` reason said 74 tests against a minimum of 76 (it runs 76), a dashboard comment named `cp` where the warning prints a `--sync` scoped to the project, and `bin/migrate-layout`'s header omitted its exit 4. No code path or threshold changes |

## What a project sees

**A project that keeps the current layout gets the same paths.** Take two temporary test projects, one synced by upstream's `bin/sync` and one by this branch's, and compare the trees:

```
git init a-up && git -C a-up commit --allow-empty -m init ; cp -R a-up a-pr
python3 <upstream checkout>/bin/sync a-up ; python3 <this branch>/bin/sync a-pr
diff -rq --exclude=.git a-up a-pr
```

Both write the same 30 paths and neither makes a `methodology/` directory. 22 of the 30 differ in bytes, and every one is a file this pull request changes (`git diff --name-only` over `starter-kit/`, `workstreams/`, `ITERATIVE_METHODOLOGY.md`, `HOW_TO_USE.md` and `FRAMEWORK_APPARATUS.md`). That is the cost of the next sync to a project that did not ask for the change: 19 files that `bin/sync` keeps current, and the sources of 3 seeds. `pr4-fixture.sh` runs this and the next check.

**A project's own files are not overwritten.** Take the same project with its 7 seeds edited and its framework files at upstream's tip. Upstream's `bin/sync` writes 0 paths; this branch's writes 19 (every framework file it changes, and nothing else), needs no `--force`, and changes 0 of the 7 seeds.

**A project that has moved is handled correctly.** Synced by the `bin/sync` on `main` today, each of my 7 projects that had moved gets 23 framework files written at the old places (the root and `docs/methodology/`) beside the moved ones, and six of them get seed files created at the root beside the project's own (41 in all). When the result was committed, two projects' own pre-commit hooks refused the commit as half-moved. That is why the sync tools are in this pull request and not left for later.

**My own 12 projects** (7 under `methodology/`, 5 not) cannot be run by you; `pr3-adopters.py` is the method. This branch's `bin/sync` changed none of their seeds, and without `--force` it refuses 10 of them, 39 files in all. 38 of those are versions from my fork's history that no commit of this branch carries, so that count is specific to my projects. After one `--force`, a plain run writes nothing at all 12. The 39th is one project's own 49 added lines in `methodology_trim.py`, which `--force` drops without saying so (see "Known gaps").

## Evidence

Each check ran in a fresh `--no-local` clone of the pull request's head with no modified files, serially, with exit codes read directly; upstream's tip is the control. `pr4-claims.sh` runs them all; it took about 35 minutes on my last run, while the machine was also running other work.

| Check | Command | upstream `f34769f` | this branch |
|---|---|---|---|
| The suite passes and has more tests | `bash bin/tests.sh` | 261 passed, 0 failed | 302 passed, 0 failed, 0 skipped |
| Every declared gate holds | `python3 starter-kit/quality_ratchet.py --run` | 12/12 pass, 0 fail, 0 unmeasured | 18/18 pass, 0 fail, 0 unmeasured |
| Links resolve in both layouts | `python3 bin/check-links --layout both` | usage error: it takes only `--tree` (exit 2) | OK: 80 links across 23 documents, in each layout |
| No tool names a file by a root path without saying why | `python3 bin/check-layout-literals` | not present | 15 files scanned, 0 unacknowledged sites; 138 lines name a file on purpose and carry a same-line marker `# layout: ok -- <reason>`; `bin/_manifest.py` and `bin/tests.sh` are exempt by name |
| One copy of the layout-deciding code, byte for byte | `python3 tools/test_layout_resolver.py` | not present | 76 tests OK; 11 copies, each equal to the master |
| Frozen proofs still give the verdict they gave (the `.verify.sh` that the trimmer writes beside an archived shard) | `bash <proof>` for each tracked `*.verify.sh` | exit 0 (the one tracked proof) | exit 0 (the same proof) |
| No gate threshold in `.quality-gates.json` is lowered | the ratchet's own comparison, `quality_ratchet.compare`, each commit against its parent | | 0 refusals over 32 commits; gates 12 to 18; five thresholds raised |

## What this does not show, and what is missing

- **The route a project takes alone from GitHub.** Every sync above used the local source, not `--source=github`.
- **Any project that is not mine.** The 12 are mine, and 10 carry versions of the framework's files that are in no history here; a project on your released files is the fixture above.
- **Windows, your machine, pre-commit hooks installed in another clone, a project's own CI.** This repository has no CI, so every check is local.
- **My fork's own suite as a whole.** Some of its test blocks read my fork's ledgers, backlog and archive as test data and cannot run on your tree. They are not carried, so `bin/tests.sh` here is yours plus the changes above.
- **Enforcement of the rule in `5afc962`.** Its check is in my version of `bin/check-handoff`, which is not carried, so the rule is prose only; the runner's own sentence for it is left out because the runner is at its token ceiling.

## Known gaps

These came from the 12 projects and are open:

- Like the `bin/sync` on `main`, a sync refuses a project's edited framework file by name but does not say which published version is nearest or how many lines differ, and `--force` then drops the edit.
- Moving only the framework's files (`--tier 1`) leaves the dashboard writing a second history file, `dashboard_history.jsonl`, under `methodology/` while the one at the root stays, unused.
- On a ledger in the old format (with no month headings), the migration appends its entry at the end, so the ledger's entries are no longer in one order; `bin/check-ledger` already fails on such a ledger before the migration and still fails after it.
- For the hook that `context_budget.py install-hook` writes, the migration warns that it "will refuse the migration commit". It does not.
- An older copy of the ledger hook that a project installed itself keeps looking for the ledger at the root. Once the ledger moves, that hook passes a commit that has no ledger entry, without saying so. The hook in this branch follows the ledger.
- A project's own tests or scripts that read a moved file by name can break. The tool lists the files whose text mentions a moved name; that list is an upper bound, not the set that breaks.
