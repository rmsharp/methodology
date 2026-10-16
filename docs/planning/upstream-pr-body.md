# The text of the one upstream pull request (draft 3)

**Status: DRAFT 3, not frozen, nothing sent.** Draft 1 is `ef98e78` and draft 2 `a6ad168`; a fresh reviewer read each and the revisions follow those reads
([`pr-composition-evidence/pr4-record.md`](pr-composition-evidence/pr4-record.md)). Everything below the rule is the text that would be posted:
the title on its own line, then the body. Written for `KJ5HST/methodology` from the local branch `pr2/candidate` at `a62bfec` (32 commits over
`upstream/main` `f34769f`). Every number in it is printed by a command named beside it; the re-runs are `pr4-claims.sh`, `pr4-fixture.sh`,
`pr4-mergefile.sh`, `pr4-supersede.sh` and `pr4-first-commit.sh` in [`pr-composition-evidence/`](pr-composition-evidence/), each with its output, and
the text is read by `pr4-body-check.py`.

---

**Title:** A methodology/ directory for a project's framework files, and bin/migrate-layout to move a project there

@KJ5HST: this gives a project's framework files one directory, `methodology/`, instead of two places, and makes every tool read either. A project that does nothing keeps its paths, but its next `bin/sync` still brings new versions of 19 files. It is large (32 commits, +19,826 / -1,152) and about two fifths of it (+8,461 of the added lines, in `bbe0dc3` and `c8c0b21`) is earlier work of mine, 1,566 of those lines the same work as #94, so this description starts with what I am asking you to decide.

## What I am asking you to decide

1. **Do you want the layout?** Today a project's root lists 18 framework files among its own and 12 more sit under `docs/methodology/` (the 30 rows of `bin/_manifest.py`: 11 kept current by `bin/sync`, 7 "seeds" it writes once and the project then owns, 12 documents). With the layout one directory holds all 30 and the root shows which files are the framework's. That is the whole benefit. If you do not want it, `bbe0dc3`, the first commit, stands alone on your tip (271 passed, 0 failed, 0 skipped and 12/12 gates, in a clean clone of it); the rest, including the ratchet's 1.4.0 and 1.5.0, does not.
2. **Choices in the dashboard** (below) are policy, not fixes: three design choices, a set of new risk rows, and four of your tests that this removes. Tell me which to drop and I will drop them.
3. **The order with #94.** This branch and #94 both rewrite `starter-kit/methodology_trim.py` and its tests: `git merge-tree` conflicts in 3 files and 17 regions (the trimmer 10, its tests 6, `.quality-gates.json` 1). #92 merges clean. This branch carries my #93 fix as its own commits, and of the 430 lines #94 adds to the trimmer all but 11 are in it as exact lines (the version string, comment wording, and the tool's name in four messages, which this branch prints from a constant); of the 1,136 it adds to the tests all but 9 (comments and docstrings); the floor in `.quality-gates.json` is 181 there and 218 here (`pr4-supersede.sh`). Say whether to wait for #94 and rebase on it, or take this as superseding it. I have not resolved the conflicts.

## What it does

- **Paths.** `bin/sync` writes a legacy project the same paths it writes today (measured below). Every tool reads either layout.
- **Moving.** `bin/migrate-layout` is a dry run unless given `--apply`; `--tier 1` moves the framework's files, `2` the project's state, `all` (the default) both. It refuses, before writing, a tree that is not a git repository with a commit, is dirty, is half-migrated (a runner at the root and under `methodology/`), already holds a destination, keeps the files out of git, is not current with what `bin/sync` would write, or holds a file that cannot be rewritten faithfully. An apply is one commit: it moves the files, rewrites the paths in `CLAUDE.md`, anchored `.gitignore` entries and the two configs, adds a ledger entry, and requires every move to stay a rename at 90% similarity or better so `git log --follow` still reaches the history (a ledger too small to take its entry fails that, rolls back and exits 3). A step that fails before the commit rolls it back; the before-and-after checks run after it, and a difference exits 4, keeps the commit and prints the `git revert` (`--skip-checks` turns them off). Like `bin/sync` and `bin/status` it is not in `bin/_manifest.py`; a project runs it from a checkout of this repository.
- **No tool guesses where the files are.** `tools/layout_resolver.py` decides from where an anchor file sits: at the root, legacy; under `methodology/`, new; in both places, a refusal naming both. One exception: with `SESSION_RUNNER.md` only under `methodology/`, a file found in both places is the framework's under `methodology/`, and the root copy is left alone as the project's own. A tool that reads a ledger anchors on that ledger (`CHANGELOG.md` or `HANDOFFS.md`), and the ratchet and the budget gate on their config, so a project that moved only the framework's files (`--tier 1`) is read right. The block is copied into each of 10 tools and the dashboard's twin, because the four that a project receives are single stdlib files; `python3 tools/test_layout_resolver.py` asserts all 11 copies equal the module.

## What in it is not layout

- **`bbe0dc3` (9 files, +7,765 / -575).** The dashboard 2.11.3 to 2.21.0 and the ledger trimmer 1.5.0 to 1.7.0 (my fix for #93, which is why it overlaps #94: its 430 trimmer lines and 1,136 test lines are #94's counts), with their tests. In `bin/tests.sh`: three blocks changed so that `cmd | grep -q` under `pipefail` cannot read a match as a failure, a lint for that pattern, a `skip` primitive, and the executable-bit check derived from the manifest. Also `BOOTSTRAP.md`'s never-overwrite row naming every seed, 11 lines in `FRAMEWORK_APPARATUS.md` for the trimmer's new warning, and three floors raised in `.quality-gates.json`. The layout commits for the dashboard and the trimmer build on it.
- **It removes four of your tests.** The three of `TestCliRemedyProportionality` (the stale-copy warning's `cp` remedy, #67 and #73), because choice 1 below replaces that remedy and the branch's tests assert the new one; and `test_every_framework_installed_source_name_has_a_signature`, because choice 3 derives the name list from the signature table, so the two cannot disagree.
- **`c8c0b21` (4 files).** The quality ratchet's 1.4.0 and 1.5.0. A gate takes an optional `timeout_seconds`; a command that outlives it reads `unmeasured` instead of exit code 127 and its whole process group is stopped; gates over one command share one run; changing `timeout_seconds` is a warning, not a refusal; the seed's schema line in `starter-kit/quality-gates.json` names the key. It does not depend on the layout, but it is built on the ratchet's layout commit `fd96593` and cannot be taken without it.

I sent whole files rather than the layout hunks because my copies of those tools had already moved on from yours, so the hunks do not apply: a three-way merge of your copy, the copy this work started from (`c8b9ddd`, a commit on my fork, which `git fetch https://github.com/rmsharp/methodology main` brings) and my tip conflicts in 51 places in 8 files, 34 of them the dashboard's two copies (`pr4-mergefile.sh`).

**Three design choices in the dashboard** come with that earlier dashboard work:

- The dashboard's `--sync` takes an optional directory, and skips a target that git tracks, or a brand-new file the project's `.gitignore` does not cover, unless `--force`. You answered #67 with a stale-copy warning that says `cp <canonical> <copy>`; this one says `--sync <directory>` instead.
- `"methodology"` is no longer in `EXCLUDE_DIRS`, so a portfolio run scores this repository too.
- How the dashboard recognises a project's installed copy of a framework tool is one table, and the name list (`FRAMEWORK_INSTALLED_SOURCE`) is derived from it; yours keeps the list and a separate signature table with a test that they agree. The same 7 names are recognised either way, but the trimmer loses its signature fallback: a copy with no `TRIM_VERSION` line is no longer recognised (the code's own note says every release has one).

**Five new risk rows** (the dashboard's `risks.append` sites go from 29 to 34 in `bbe0dc3`, 35 at the head with the layout's half-migrated row): a file too large for an agent to read in one read (a hard limit of 256 KiB, a budget of 25,000 tokens at a floor of 2.27 bytes per token), two for an oversized backlog, and one that re-reports a finding of the trimmer (whose trigger is 192 KiB). The constants are mine and are policy too.

It also fixes one defect: `git log --reverse --format=%ai -1` applies `-1` before it reverses, so `first_commit_date` is the newest commit and a project's age is days since its last one. The dashboard now reads the root commits (`--max-parents=0`).

## How to read it

32 commits, 47 files (38 changed, 9 new): `git diff --shortstat f34769f HEAD`, `git rev-list --count f34769f..HEAD`. Three commits touch more than 5 files: `bbe0dc3` 9, `14ef959` 7, `fd96593` 6. The numbers in this description are the head's; while building I ran the suite and the gates in a clean clone at the last commit of each group below, and I did not re-run every commit alone.

| Commits | What |
|---|---|
| `bbe0dc3` | not layout (above) |
| `14ef959` | `tools/layout_resolver.py`, `tools/layout_fixtures.py`, `bin/check-layout-literals` (finds a root path written into a tool), and `NEW_LAYOUT`, the manifest's second table, which is data |
| `fd96593`, `c8c0b21` | the ledger pre-commit hook and the quality ratchet read either layout (ratchet 1.3.0); then ratchet 1.4.0 and 1.5.0, not layout |
| `98ca7fc`, `e9c5cb8`, `dd581fe` | the trimmer 1.8.0, `context_budget.py` 1.4.0 and the dashboard 2.22.0 each find a project's files at either place; the trimmer writes its archive shard and proof beside its ledger. `98ca7fc` adds `tools/fixtures/trim-verify-template-1.7.0.sh` (406 lines: 1.7.0's proof script, frozen, for a test to compare) |
| `4c0bdde`, `261b8d3`, `0aa1897` | (`4c0bdde` rewrites your Test 15 assertion to count the status table's rows, not every line that names the project) `bin/sync` (`--layout auto\|legacy\|new`), `bin/status`, `bin/check-links` (`--layout legacy\|new\|both`) and the manifest reader, which reads `NEW_LAYOUT` as data for `--source=github`; with their 82-test suite |
| `a459b8b`, `505541c` | `bin/check-ledger` and `bin/check-handoff` read either layout (the layout hunks only; the rest of my versions of them stays on my fork) |
| `c8d4375` to `18cda0f` | the documents say where the files sit and their references hold in both layouts: 36 relative links became bare names in code spans (`python3 bin/check-links` counts 116 across the 23 distributed documents at your tip, 80 at the head), and `SESSION_RUNNER.md`'s first paragraph tells every project, legacy ones too, to look beside the runner and where a legacy project keeps the others. `bin/check-links --layout both` runs in `bin/tests.sh` |
| `2942e46`, `ab35e96` | `bin/migrate-layout` and its 280-test suite: `bin/tests.sh` runs two fast classes of it, and the 280 run through two gates, each with a `timeout_seconds` of 3600 (about 6 minutes) |
| `5afc962` | a cited gate run that reads unmeasured gates must be repaired or name them (`starter-kit/HANDOFFS.md`, `HOW_TO_USE.md`; 5 lines) |
| `c933b0f` to `28f99a7` | ten commits that take out references only my fork can resolve: seven in comments and docstrings (no program token changes), three in text a program prints. Skippable as a run. At least 56 added lines of that kind remain (the pattern does not look for my phase codes), 36 of them starting with `#` or `//`, some naming things your own trimmer already carries (`git diff f34769f HEAD -- . ':!docs' \| grep -E '^\+[^+]' \| grep -cE 'BL-[0-9]+\|\bS[0-9]{2,3}\b\|\bD[0-9]{1,2}\b\|Learning #[0-9]+'`) |
| `ced2c82` | `python3 starter-kit/context_budget.py --status` read `SESSION_RUNNER.md` as over its token ceiling after the documents commits; this drops one duplicated example command (84 B). It also changes three lines of `.context-budget.json` (the file's density, its measured size and a note), which **loosens that gate's line by 43 B**; that hunk is separable |
| `a62bfec` | four statements the series left stale, in text only: the `layout-literals` gate's reason said two checkers are not scanned (they are), the `layout-unit-tests` reason said 74 tests against a floor of 76 (it runs 76), a dashboard comment named `cp` where the warning prints a `--sync` scoped to the project, and `bin/migrate-layout`'s header omitted its exit 4. No code path or threshold changes |

## What a project sees

**A legacy project gets the same paths.** Two throwaway projects, one synced by upstream's `bin/sync` and one by this branch's, then the trees diffed:

```
git init a-up && git -C a-up commit --allow-empty -m init ; cp -R a-up a-pr
python3 <upstream checkout>/bin/sync a-up ; python3 <this branch>/bin/sync a-pr
diff -rq --exclude=.git a-up a-pr
```

Both write the same 30 paths and neither makes a `methodology/` directory. 22 of them differ in bytes, and every one is a file this pull request changes (`git diff --name-only` over `starter-kit/`, `workstreams/`, `ITERATIVE_METHODOLOGY.md`, `HOW_TO_USE.md` and `FRAMEWORK_APPARATUS.md`): that is the next sync's cost to a project that did not ask, 19 tracked files and 3 seeds' sources. `pr4-fixture.sh`, in [my fork's evidence directory](https://github.com/rmsharp/methodology/tree/main/docs/planning/pr-composition-evidence), runs this and the next.

**A project's own files are not overwritten.** The same project with its 7 seeds edited and its framework files at upstream's tip: upstream's `bin/sync` writes 0 paths; this branch's writes 19 (every framework file it changes, nothing else), needs no `--force`, and changes 0 of the 7 seeds.

**A project that has moved is synced as the project it is.** Synced by the `bin/sync` on `main` today, a project under `methodology/` gets 23 framework files written at the legacy places (the root and `docs/methodology/`) beside the moved ones, and seeds created at the root beside the project's own (41 across six projects); two of my projects' own pre-commit hooks refused that commit as half-migrated. That is why the sync tools are in this pull request and not left for later.

**My own 12 projects** (7 under `methodology/`, 5 not; not reproducible by you, `pr3-adopters.py` in that directory): this branch's `bin/sync` changed none of their seeds, and without `--force` refuses 10 of them, 39 files in all. 38 are versions from my fork's history that no commit of this branch carries, so that count is specific to my projects. After one `--force` a plain run writes nothing, at all 12. The 39th is a project's own 49 added lines in its copy of `methodology_trim.py`, which `--force` drops without saying so (below).

## Evidence

Each in a clean `--no-local` clone of the pull request's head (0 dirty paths), serially, exit codes read bare; upstream's tip is the control. `pr4-claims.sh` runs them all: about 5 minutes for the suite and 10 for the gate run, on a machine with other load.

| Claim | Command | upstream `f34769f` | this branch |
|---|---|---|---|
| the suite passes, and holds more | `bash bin/tests.sh` | 261 passed, 0 failed | 302 passed, 0 failed, 0 skipped |
| every declared gate holds | `python3 starter-kit/quality_ratchet.py --run` | 12/12 pass, 0 fail, 0 unmeasured | 18/18 pass, 0 fail, 0 unmeasured |
| both layouts' links resolve | `python3 bin/check-links --layout both` | usage error, takes only `--tree` (exit 2) | OK: 80 links across 23 documents, in each layout |
| no root path is written into a tool | `python3 bin/check-layout-literals` | not present | 15 files, 0 unacknowledged sites; 138 lines carry a same-line `# layout: ok -- <reason>`; the manifest and `bin/tests.sh` are exempt by name |
| one resolver, byte for byte | `python3 tools/test_layout_resolver.py` | not present | 76 tests OK; 11 copies, each equal to the module |
| every frozen proof (the `.verify.sh` the trimmer writes beside an archived shard) gives the verdict it gave | `bash <proof>` for each tracked `*.verify.sh` | exit 0 (the one tracked proof) | exit 0 (the same proof) |
| no gate threshold in `.quality-gates.json` is lowered | the ratchet's own comparison, `quality_ratchet.compare`, each commit against its parent | | 0 refusals over 32 commits; gates 12 to 18, five floors raised (the `ced2c82` density is in `.context-budget.json`, not a gate) |

The unit suites behind the gate (a floor is a gate's minimum): dashboard 395 tests (upstream's floor 229), trimmer 218 (124), quality ratchet 120 (45), context budget 163 (148), and four new: layout 76, checkers 11, sync 82, migration 280.

## What this does not show, and what is missing

- **The route a project takes alone from GitHub.** Every sync above used the local source, not `--source=github`.
- **Any project that is not mine.** The 12 are mine, and 10 carry versions of the framework's files found in no history here; a project on your released files is the fixture above.
- **Windows, your machine, hooks armed in another clone, a project's own CI.** This repository has no CI, so every check is local.
- **My own suite as a whole.** Some of its blocks read this repository's ledgers, backlog and archive as fixtures and cannot run on your tree; they are not carried, so `bin/tests.sh` here is yours plus the changes above.
- **Enforcement of the rule in `5afc962`.** Its check is in my version of `bin/check-handoff`, which is not carried, so the rule is prose; `SESSION_RUNNER.md`'s own sentence for it is left out because that file is at its token ceiling.
- **A `CHANGELOG.md` entry, or a change to `README.md` or `CLAUDE.md`** (which list the files). The 32 commits were made without your pre-commit hook, which would require a ledger entry in each; say if you want one entry and I will add it. I have not bumped the framework's release version; release notes would be a separate pull request after a merge, as with #92.
- **How to merge it.** A merge commit or a rebase keeps the ten reference-removal commits skippable as a run; a squash does not.

Known gaps from the 12 projects, open:

- Like the `bin/sync` on `main`, a sync refuses a project's edited framework file by name but does not say which published version is nearest or how many lines differ, and `--force` then drops the edit.
- Moving only the framework's files (`--tier 1`) leaves the dashboard writing a second history file under `methodology/` while the root's old one stays, unused.
- On a ledger in the old format (no month headings) the migration's own entry lands at the end, so the ledger has two orders; `bin/check-ledger` fails before and after.
- For the hook that `context_budget.py install-hook` writes, the migration warns that it "will refuse the migration commit". It does not.
- An older copy of the ledger hook that a project armed itself keeps looking for the ledger at the root; once the ledger moves it passes a commit that has no ledger entry, without saying so. The hook in this branch follows the ledger.
- A project's own tests or scripts that read a moved file by name can break. The tool lists the files whose text mentions a moved name; that list is an upper bound, not the set that breaks.
