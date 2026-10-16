# The text of the one upstream pull request (draft 7)

**Status: DRAFT 7, not frozen, nothing sent.** Draft 7 follows three fresh readers' reports, on drafts 4 (`d5bb53b`), 5 (`9becf89`) and 6 (`dfc31ab`); each finding was checked before it was
acted on. The third reader was told that the maintainer knows the framework's own vocabulary, which the first two were not, and rated draft 6 at 6 of 10. Draft 4 was a recomposition of draft 3
(`ab4f563`) in plainer, formal language at his direction. Draft 1 is `ef98e78`, draft 2 `a6ad168` and draft 3 `025afed`; a fresh reviewer read each of the first two
([`pr-composition-evidence/pr4-record.md`](pr-composition-evidence/pr4-record.md)); the findings on drafts 4 to 6 and what became of each are in
[`pr-composition-evidence/draft4-record.md`](pr-composition-evidence/draft4-record.md). **Draft 7 has had no read of its own.** Everything below the rule is the text that would be posted: the title
on its own line, then the body. Written for `KJ5HST/methodology` from the local branch `pr2/candidate` at `a62bfec` (32 commits over `upstream/main` `f34769f`). Every number in it is printed by a
command named beside it, and the text is read by `pr4-body-check.py`.

---

**Title:** A methodology/ directory for a project's framework files, and bin/migrate-layout to move a project there

@KJ5HST:

This pull request lets a project keep all of the framework's files in one directory, `methodology/`. Today they sit in two places: 18 at the project root, among the project's own files, and 12 under `docs/methodology/`. Every tool in the repository learns to find the files in either place. A project that changes nothing keeps its current locations, and a new command, `bin/migrate-layout`, moves a project when its owner chooses.

The numbered items I mention: #93 is my issue about the proof scripts that the ledger trimmer (`methodology_trim.py`) generates, and #94 is my pull request that fixes it; #92 is my pull request with the release notes for v4.2; #67 was your issue about the dashboard's stale-copy warning, and #73 your pull request that fixed it. Every number below comes from a command, or is rounded from one. The scripts that run them, and their saved output, are in [my fork's evidence directory](https://github.com/rmsharp/methodology/tree/main/docs/planning/pr-composition-evidence); the `pr3-` and `pr4-` in their names are my own numbering and carry no meaning here.

## What I am asking you to decide

1. **Do you want the single directory?** I asked for it for my own 12 projects, to clear the project root and show which files belong to the framework; I found no issue on your repository that asks for it. The 30 rows of `bin/_manifest.py` are 18 files at a project's root (11 that `bin/sync` keeps current, and 7 "seeds", which it writes once, when the project lacks them, and the project owns afterwards) and 12 documents under `docs/methodology/` (also kept current). With the directory, all 30 sit in one place. That is the only benefit. It costs this repository: the code that decides a project's layout is copied into 11 files; 138 lines name a file by its root path on purpose and carry a same-line comment, `# layout: ok -- <reason>`, saying why; 36 relative links became plain names in code spans (a relative link that is right in one layout is dead in the other); and `bin/migrate-layout` (1,457 lines) and its 280 tests are new. It costs projects: even a project that never moves receives 19 changed files at its next `bin/sync` and reads two framework files that are 244 bytes larger (see "Size" below). One known gap bears on this decision: a ledger hook that a project installed itself keeps looking for the ledger at the root, so once the ledger has moved it passes a commit that has no ledger entry, without saying so (see "Known gaps"). The branch is 32 commits and adds 19,826 lines.
   - If you do not want the directory, the first commit, `bbe0dc3`, can be taken alone on your current code (271 passed, 0 failed, 0 skipped and 12/12 gates, in a clean clone of it). As built, the other commits sit on top of the directory work, and I have not tested them without it. If you want any of them on their own (the ratchet's timeouts in `c8c0b21` are the likeliest), say so and I will rebuild it as a separate pull request.
2. **Which of the dashboard changes do you want?** These come with the earlier work in `bbe0dc3`, and they are policy, not fixes. Please tell me which to remove and I will remove them. I have not itemised the other changes to the dashboard in `bbe0dc3` (2.11.3 to 2.21.0); I will if you want to review them.
   - (a) The dashboard's `--sync` takes an optional directory: with one, it writes only that project; without one, every project it finds. It skips a target that git tracks, or a brand-new file the project's `.gitignore` does not cover, unless `--force` is given. Your pull request #73 made the stale-copy warning say `cp <canonical> <copy>`; this branch's warning says `--sync <directory>` instead. Both answer #67 (a remedy that rewrote 26 files in 25 repositories); mine keeps the dashboard's own `--sync` and scopes it to one directory.
   - (b) `"methodology"` is no longer in `EXCLUDE_DIRS`, so a run of the dashboard over a directory of projects scores this repository too.
   - (c) How the dashboard recognises a project's installed copy of a framework tool is now one table, and the list of names (`FRAMEWORK_INSTALLED_SOURCE`) is derived from it. Yours keeps the list and a separate signature table, with a test that they agree. The same 7 names are recognised either way, but the trimmer loses its signature fallback: a copy with no `TRIM_VERSION` line is no longer recognised. All 4 versions of the trimmer in your history have that line.
   - Five new risk rows (the dashboard's `risks.append` sites go from 29 to 34 in `bbe0dc3`, and to 35 at the head with a row for a half-migrated project, one with framework files in both layouts). Two are for a file past the limits of an agent's file read: a hard limit of 256 KiB, past which the read is refused outright, and a budget of 25,000 tokens, past which it is cut short with a banner (counted at 2.27 bytes per token, the densest content measured, so 56,750 B). Two are for a file that a session is told to read whole, such as a backlog, when it is past that budget: lower severity if the project's own trimmer lists the file as one it can archive, higher if not. One repeats the trimmer's own size trigger (192 KiB). The thresholds are my choices.
   - Four of your tests are removed: the three in `TestCliRemedyProportionality` (the stale-copy warning's `cp` remedy, from #67 and #73), because (a) replaces that remedy and this branch's tests assert the new one; and `test_every_framework_installed_source_name_has_a_signature`, because (c) derives the list of names from the signature table, so the two cannot disagree.
3. **In what order should this and #94 go?** This branch and #94 both rewrite `starter-kit/methodology_trim.py` and its tests. `git merge-tree` reports conflicts in 3 files and 17 regions (the trimmer 10, its tests 6, `.quality-gates.json` 1); #92 merges cleanly. Taking only `bbe0dc3` would still conflict with #94, in 6 regions in 2 files (the trimmer 1, its tests 5). This branch contains my fix for #93 inside `bbe0dc3`, together with dashboard work and test changes. #94 adds 430 lines to the trimmer and 1,136 to its tests, 1,566 in all; this branch contains all but 11 of the trimmer lines and all but 9 of the test lines as identical lines (the differences are the version string, comment wording, the tool's name in four messages, and comments and docstrings in the tests). The minimum for the `trimmer-unit-tests` gate in `.quality-gates.json` is 181 in #94 and 218 here (`pr4-supersede.sh`). Please say whether I should wait for #94 and rebase on it, or whether this pull request should supersede it. I have not resolved the conflicts.
4. **Three smaller choices.**
   - `ced2c82` drops a duplicated example command (84 B) from the runner (`SESSION_RUNNER.md`) so that it reads under its token ceiling. The same commit also re-records the runner's bytes-per-token ratio in `.context-budget.json`, as that file's own rule asks when a file changes. The budget tool (`context_budget.py`) converts bytes to tokens at the ratio recorded for the file, so the new ratio lets the runner grow 43 B more before the tool reports it over. That second change can be dropped on its own; the cut alone is enough to pass.
   - Ten commits remove references that only my fork can resolve, such as backlog and session codes in comments and messages. They change comments and messages only. Please tell me whether to keep them in this pull request or drop them. If you keep them, a merge commit or a rebase leaves them as a separable run in the history; a squash folds them in.
   - A `CHANGELOG.md` entry, and any change to `README.md` or `CLAUDE.md` (which list the files), are not included. The 32 commits were made without your pre-commit hook, which would require a ledger entry in each. Please say if you want one entry for the whole pull request, and I will add it. Whether the change needs a new release version is yours to say; I have not made one, and release notes would be a separate pull request after a merge, as with #92.

These four items are complete in themselves. The sections below give the detail behind them and the evidence.

## Size, what reaches a project, and what it costs

**Size.** The branch has 32 commits and adds 19,826 lines (it removes 1,152): `git diff --shortstat f34769f HEAD`. Most of that never reaches a project. `bin/sync` writes 19 of the changed files into a project, with 2,959 lines added and 530 removed in all; 3 more changed files are templates that only a new project receives (7 added, 4 removed). The other 25 files, with 16,860 of the added lines (85%), stay in this repository: tests, tools that only this repository runs, and its gate configuration. The dashboard is counted twice in the total, as `starter-kit/methodology_dashboard.py` and as an identical copy in `tools/`. About 43% of the added lines (8,461, in `bbe0dc3` and `c8c0b21`) are earlier work of mine that is not about the directory (see decisions 1 to 3). `pr4-distribution.py` derives these figures from the manifest, `bin/_manifest.py`.

**What it costs to use.** A session must read two of the framework's files in full, `SESSION_RUNNER.md` and `SAFEGUARDS.md`. Together they are 244 bytes (0.35%) larger on this branch, which is about 90 tokens at the budget tool's rate of 2.81 bytes per token. The programs a session runs took the same time as upstream's versions, within 0.1 s on two test projects (`pr4-cost.sh`): the dashboard 0.59 to 0.63 s here against 0.66 to 0.68 s for upstream's on a project of 488 commits, and 0.11 to 0.12 s on both for a project of 3 commits; the trimmer's check 0.07 to 0.08 s on both; the budget tool 0.03 s on both.

## What the change does

- **Paths.** `bin/sync` writes a project that keeps the current layout (called `legacy` in the tools' `--layout` options) the same paths it writes today (measured below). Every tool reads either layout.
- **No tool guesses where the files are.** `tools/layout_resolver.py` is a short block of code that decides a project's layout from where an anchor file sits. The default anchor is `SESSION_RUNNER.md`: at the root, the project has the current layout; under `methodology/`, the new one; in both places, the tool refuses and names both. A tool that reads a ledger anchors on that ledger instead (`CHANGELOG.md` or `HANDOFFS.md`), and the ratchet and the budget tool anchor on their configuration file, so these tools read correctly a project that moved only the framework's files (`--tier 1`, below). One exception applies to files other than the anchor: a file may exist in both places, for example a project's own product `CHANGELOG.md` at the root beside the framework's under `methodology/`. If the runner is under `methodology/` and not at the root, the tool reads the copy under `methodology/` as the framework's and leaves the copy at the root alone as the project's own; in any other case it refuses. The block is copied into 10 tools and into the dashboard's identical copy. The four tools that a project receives, `methodology_dashboard.py`, `methodology_trim.py`, `context_budget.py` and `quality_ratchet.py`, are single files that import nothing outside the standard library, so each carries its own copy. To change the code, edit `tools/layout_resolver.py` and copy the block into the other 10 files; `python3 tools/test_layout_resolver.py` fails until all 11 copies equal the master.
- **Moving a project.** `bin/migrate-layout` makes no change unless given `--apply`. `--tier 1` moves the framework's files; `--tier 2` moves the project's own state (its seed files, the files the tools generate, the archive shards the trimmer wrote, and the project-owned learnings file that `BOOTSTRAP.md` names, PROJECT_LEARNINGS.md); `all`, the default, moves both.
  - *It refuses, before writing anything,* a tree that: is not a git repository with a commit; has uncommitted changes; is half-migrated (a runner at the root and another under `methodology/`); already holds a destination file; keeps its framework files out of git (its `.gitignore` lists them); is not current with what `bin/sync` would write; or has a file it must rewrite that it cannot rewrite safely (for example, a ledger with a code fence that never closes, so that the tool cannot place its entry).
  - *An apply is one commit.* It moves the files; rewrites the moved paths in `CLAUDE.md`, in anchored `.gitignore` entries and in `.context-budget.json` and `.quality-gates.json`; and adds a ledger entry. Every move must remain a rename at 90% similarity or better, so that `git log --follow` still reaches the history. A ledger so small that adding the entry would drop it below 90% fails that test, and the apply is rolled back (exit 3), as is any step that fails before the commit. The tool's report names `git revert <commit>` as the way back.
  - *It checks itself.* Before and after the commit it runs read-only checks: `bin/status`, `bin/check-ledger`, `bin/check-handoff`, `bin/check-links`, the proof of every archive shard, and how far `git log --follow` reaches from the ledger. If any result differs afterwards, it exits 4 and keeps the commit (`--skip-checks` turns the checks off).
  - Like `bin/sync` and `bin/status`, it is not in `bin/_manifest.py`; a project runs it from a checkout of this repository.

## What the commits contain

A suggested order for reading: `bbe0dc3`, then `14ef959`, then the other groups in the order of the table below.

**Earlier work that is not about the directory** (the dashboard choices are in decision 2):

- **`bbe0dc3` (9 files, +7,765 / -575).** The dashboard 2.11.3 to 2.21.0 and the ledger trimmer 1.5.0 to 1.7.0, with their tests. The trimmer change is my fix for #93, which is why it overlaps #94. In `bin/tests.sh`, three blocks changed so that a pipeline of the form `cmd | grep -q` under `pipefail` cannot report a match as a failure; a lint for that pattern; a `skip` helper, which reports a test as skipped, not passed; and an executable-bit check derived from the manifest. The commit also adds to `BOOTSTRAP.md` a row, in its table of files that `bin/sync` never overwrites, that names every seed; 11 lines in `FRAMEWORK_APPARATUS.md` for the trimmer's new warning; and raises three thresholds in `.quality-gates.json`. The dashboard also gets one defect fix: `git log --reverse --format=%ai -1` applies `-1` before it reverses, so `first_commit_date` was the newest commit and a project's age was the days since its last commit; it now reads the root commits (`--max-parents=0`).
- **`c8c0b21` (4 files).** The quality ratchet's 1.4.0 and 1.5.0. A gate may set `timeout_seconds`; a command that outlives it is reported `unmeasured` (its result could not be determined), not as exit code 127, and its whole process group is stopped. Two gates that read the same command's output share one run of it. Changing `timeout_seconds` is a warning, not a refusal. The `_gate_schema` entry in `starter-kit/quality-gates.json`, which lists a gate's keys, now names `timeout_seconds`. This does not depend on the layout, but it is built on the ratchet's layout commit `fd96593`.
- **One small change elsewhere.** `5afc962` adds a rule for a close-out receipt in `HANDOFFS.md` that cites a gate run: a gate that read `unmeasured` must be repaired, or named in the receipt (`starter-kit/HANDOFFS.md` and `HOW_TO_USE.md`; 5 lines).

For the dashboard and the trimmer this pull request contains whole files, not the layout hunks, because my versions had diverged from yours and the hunks do not apply. Merging your copy with mine, starting from the copy my work began with (`c8b9ddd`), conflicts in 51 places in 8 files (`pr4-mergefile.sh`, run with my fork's `main` as of `e7b389f`; both commits are on my fork). For `bin/check-ledger` and `bin/check-handoff` it contains the layout hunks only.

**All 32 commits, by group.** The branch changes 47 files (38 changed, 9 new). I ran the suite and the gates in a clean clone at the last commit of each group below, and I did not re-run every commit alone.

| Commits | What |
|---|---|
| `bbe0dc3` | Earlier work, not the directory (above) |
| `14ef959` | The foundation: `tools/layout_resolver.py`, `tools/layout_fixtures.py` (test projects in both layouts), `bin/check-layout-literals` (finds a tool that names a file by its root path), and `NEW_LAYOUT`, a second table in `bin/_manifest.py` that gives each file's place under `methodology/`; it is plain data, so `bin/sync --source github` (which clones the framework repository for the run) can read it without running it |
| `fd96593`, `c8c0b21` | The ledger pre-commit hook and the quality ratchet read either layout (ratchet 1.3.0); then ratchet 1.4.0 and 1.5.0, which are not about layout |
| `98ca7fc`, `e9c5cb8`, `dd581fe` | The trimmer, `context_budget.py` and the dashboard each find a project's files in either place; the trimmer writes its archive shard and proof beside its ledger. `98ca7fc` also adds `tools/fixtures/trim-verify-template-1.7.0.sh` (406 lines: the 1.7.0 proof script, frozen so that a test can compare against it) |
| `4c0bdde`, `261b8d3`, `0aa1897` | `bin/sync` (`--layout auto\|legacy\|new`), `bin/status`, `bin/check-links` (`--layout legacy\|new\|both`) and the manifest reader, which reads `NEW_LAYOUT` as data, with an 82-test suite. `4c0bdde` rewrites your Test 15 to count the status table's rows: `bin/status` now prints a `layout:` line that names the project, and the old assertion counted lines naming the project (31 for 30 files) |
| `a459b8b`, `505541c` | `bin/check-ledger` and `bin/check-handoff` read either layout (the layout hunks only; the rest of my versions of them stays on my fork) |
| `c8d4375` to `18cda0f` | The documents say where the files sit, and their references hold in both layouts: 36 relative links became plain names in code spans (116 links across the 23 distributed documents at your tip, 80 at the head), and the first paragraph of `SESSION_RUNNER.md` tells every project to look beside the runner for the other framework files, and says where a project that keeps the current layout keeps them |
| `2942e46`, `ab35e96` | `bin/migrate-layout` and its 280-test suite. `bin/tests.sh` runs two fast classes of it; all 280 run through two gates that each set `timeout_seconds` to 3600, because they take about 6 minutes |
| `5afc962` | The receipt rule (above) |
| `c933b0f` to `28f99a7` | The ten commits that remove references only my fork can resolve (decision 4): seven in comments and docstrings (no program token changes) and three in text a program prints |
| `ced2c82` | The runner cut and the re-recorded ratio (decision 4) |
| `a62bfec` | Four statements the series left stale, corrected in text only: the `layout-literals` gate's reason said two checkers are not scanned (they are), the `layout-unit-tests` reason said 74 tests against a minimum of 76 (it runs 76), a dashboard comment named `cp` where the warning prints a `--sync` scoped to the project, and `bin/migrate-layout`'s header omitted its exit 4. No code path or threshold changes |

A search for the codes that the ten commits remove still matches 56 added lines, 36 of them starting with `#` or `//`. Some matches may be legitimate, for example upstream's own `Learning #N` rows, and the search does not look for the codes of my own planning documents:

```
git diff f34769f HEAD -- . ':!docs' | grep -E '^\+[^+]' | grep -cE 'BL-[0-9]+|\bS[0-9]{2,3}\b|\bD[0-9]{1,2}\b|Learning #[0-9]+'
```

## What a project sees

**A project that keeps the current layout gets the same paths.** Take two temporary test projects, one synced by upstream's `bin/sync` and one by this branch's, and compare the trees:

```
git init a-up && git -C a-up commit --allow-empty -m init ; cp -R a-up a-pr
python3 <upstream checkout>/bin/sync a-up ; python3 <this branch>/bin/sync a-pr
diff -rq --exclude=.git a-up a-pr
```

Both write the same 30 paths and neither makes a `methodology/` directory. 22 of the 30 differ in bytes, and every one is a file this pull request changes (`git diff --name-only` over `starter-kit/`, `workstreams/`, `ITERATIVE_METHODOLOGY.md`, `HOW_TO_USE.md` and `FRAMEWORK_APPARATUS.md`). That is the cost of the next sync to a project that did not ask for the change: 19 files that `bin/sync` keeps current, and the sources of 3 seeds. `pr4-fixture.sh` runs this and the next check.

**A project's seed files are not overwritten.** Take the same project with its 7 seeds edited and its framework files at upstream's tip. Upstream's `bin/sync` writes 0 paths; this branch's writes 19 (every framework file it changes, and nothing else), needs no `--force`, and changes 0 of the 7 seeds.

**A project that has moved is synced where its files are.** Take a project whose 30 files are already under `methodology/`. The `bin/sync` on `main` today writes 30 paths outside `methodology/`, a second copy of every framework file and seed; this branch's writes none (`pr4-moved.sh`). So once a project can move, the sync tools have to change with it. On my 7 projects that had moved, the `bin/sync` on `main` wrote 23 framework files at the old places at each, and created 41 seed files at the root across six of them; when the result was committed, two projects' own pre-commit hooks refused the commit as half-migrated.

**My own 12 projects** (7 under `methodology/`, 5 not) cannot be run by you; `pr3-adopters.py` is the method. This branch's `bin/sync` changed none of their seeds, and without `--force` it refuses 10 of them, over 39 files in all. 38 of those files are versions from my fork's history that no commit of this branch carries, so that count is specific to my projects. The 39th is one project's own 49 added lines in `methodology_trim.py`, which `--force` drops without saying so (see "Known gaps"). After one `--force`, a plain run then writes nothing at any of the 12.

## Evidence

Each check ran in a fresh `--no-local` clone of the pull request's head with no modified files, serially, with exit codes read directly; upstream's tip is the control. `pr4-claims.sh` runs them all; it took about 35 minutes on my last run, with other programs running on the machine.

| Check | Command | upstream `f34769f` | this branch |
|---|---|---|---|
| The suite passes and has more tests | `bash bin/tests.sh` | 261 passed, 0 failed | 302 passed, 0 failed, 0 skipped |
| Every declared gate holds | `python3 starter-kit/quality_ratchet.py --run` | 12/12 pass, 0 fail, 0 unmeasured | 18/18 pass, 0 fail, 0 unmeasured |
| Links resolve in both layouts | `python3 bin/check-links --layout both` | usage error: it takes only `--tree` (exit 2) | OK: 80 links across 23 documents, in each layout |
| No tool names a file by a root path without saying why | `python3 bin/check-layout-literals` | not present | 15 files scanned, 0 unacknowledged sites; 138 lines name a file on purpose and carry the `# layout: ok -- <reason>` comment; `bin/_manifest.py` and `bin/tests.sh` are exempt by name |
| One copy of the layout-deciding code, byte for byte | `python3 tools/test_layout_resolver.py` | not present | 76 tests OK; 11 copies, each equal to the master |
| Frozen proofs still give the verdict they gave (the `.verify.sh` that the trimmer writes beside an archived shard) | `bash <proof>` for each tracked `*.verify.sh` | exit 0 (the one tracked proof) | exit 0 (the same proof) |
| No gate threshold in `.quality-gates.json` is lowered | the ratchet's own comparison, `quality_ratchet.compare`, each commit against its parent | | 0 refusals over 32 commits; gates 12 to 18; five thresholds raised |

## What this does not show, and what is missing

- **The route a project takes alone from GitHub.** Every sync above used the local source, not `bin/sync --source github`.
- **Any project that is not mine.** The 12 are mine, and 10 carry versions of the framework's files that are in no history here; a project on your released files is the fixture above.
- **Windows, your machine, pre-commit hooks installed in another clone, a project's own CI.** This repository has no CI, so every check is local.
- **My fork's own suite as a whole.** Some of its test blocks read my fork's ledgers, backlog and archive as test data and cannot run on your tree. They are not carried, so `bin/tests.sh` here is yours plus the changes above.
- **Enforcement of the rule in `5afc962`.** Its check is in my version of `bin/check-handoff`, which is not carried, so the rule is prose only; the runner's own sentence for it is left out because the runner is close to its token ceiling.

## Known gaps

These came from the 12 projects and are open:

- Like the `bin/sync` on `main`, a sync refuses a project's edited framework file by name but does not say which published version is nearest or how many lines differ, and `--force` then drops the edit.
- Moving only the framework's files (`--tier 1`) leaves the dashboard writing a second history file, `dashboard_history.jsonl`, under `methodology/` while the one at the root stays, unused.
- On a ledger in the old format (with no month headings), the migration appends its entry at the end, so the ledger's entries are no longer in one order; `bin/check-ledger` already fails on such a ledger before the migration and still fails after it.
- For the hook that `context_budget.py install-hook` writes, the migration warns that it "will refuse the migration commit". In fact the hook does not refuse it.
- An older copy of the ledger hook that a project installed itself keeps looking for the ledger at the root. Once the ledger moves, that hook passes a commit that has no ledger entry, without saying so. The hook in this branch follows the ledger.
- A project's own tests or scripts that read a moved file by name can break. The migration lists the other files whose text mentions a moved name, besides those it rewrites; that list is an upper bound, not the set that breaks.
