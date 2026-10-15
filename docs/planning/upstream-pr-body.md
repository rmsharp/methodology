# The text of the one upstream pull request (draft)

**Status: DRAFT, not frozen, nothing sent.** Everything below the rule is the text that would be posted: the title on its own line,
then the body. Written for `KJ5HST/methodology` from the local branch `pr2/candidate` at `ced2c82` (31 commits over `upstream/main`
`f34769f`). Every number in it is printed by a command named beside it; the re-runs are in
[`pr-composition-evidence/pr4-claims.sh`](pr-composition-evidence/pr4-claims.sh),
[`pr-composition-evidence/pr4-fixture.sh`](pr-composition-evidence/pr4-fixture.sh) and
[`pr-composition-evidence/pr4-supersede.sh`](pr-composition-evidence/pr4-supersede.sh), the outputs beside them, and the text is checked by
[`pr-composition-evidence/pr4-body-check.py`](pr-composition-evidence/pr4-body-check.py).

---

**Title:** A methodology/ directory for a project's framework files, and bin/migrate-layout to move a project there

@KJ5HST: this changes where a project keeps the framework's files and makes every tool in the repository read either place. It is large, so this description says first what I am asking you to decide, then what in it is not about the layout, how to read it, what I measured, and what I could not.

## What I am asking you to decide

1. **Do you want the layout at all?** Everything else follows from that. If not, close this; nothing in it changes a project that does not ask.
2. **Three choices in the dashboard** (below) are policy, not fixes. Tell me which to drop and I will drop them.
3. **The order with #94.** #94 and this change both rewrite `starter-kit/methodology_trim.py` and its tests (last section). Say whether to wait for #94 and rebase on it, or take this as superseding it.

## What it does

A project that adopts the framework keeps its framework files in two places: 18 at its root, beside its own files (11 that `bin/sync` keeps current and 7 it writes once), and 12 under `docs/methodology/`: the 30 rows of `bin/_manifest.py`. This adds a second layout that holds all 30 under one directory, `methodology/`, with `workstreams/` its one subdirectory, so a project's root shows which files are the framework's.

- **Nothing changes for a project that does not ask.** Every tool reads either layout, and `bin/sync` writes a legacy project the same paths it writes today (measured below).
- **A project moves with `bin/migrate-layout`,** a dry run unless given `--apply`. It refuses, before writing anything, a tree that is dirty, half-migrated, already holds a destination, keeps the files out of git, or is not current with what `bin/sync` would write. An apply is one commit, rolled back if a step or a check fails. Like `bin/sync` and `bin/status` it is not in `bin/_manifest.py`, so a project does not receive it; it runs from a checkout of this repository.
- **No tool guesses where the files are.** `tools/layout_resolver.py` decides from where `SESSION_RUNNER.md` sits: at the root, the legacy layout; under `methodology/`, the new one; in both places, a refusal that names both. The same marked block is copied into each of the 10 tools that need it and into the dashboard's twin under `tools/`, because each is a single stdlib file, and `python3 tools/test_layout_resolver.py` asserts that all 11 copies equal the module.

## What in it is not layout

Two commits are earlier work of mine that you have not seen, and the layout work is built on them:

- `bbe0dc3`: the dashboard 2.11.3 to 2.21.0 and the ledger trimmer 1.5.0 to 1.7.0, with their tests, a `skip` in `bin/tests.sh`, and two checks it gains. Trimmer 1.7.0 carries my fix for #93, which is why it overlaps #94.
- `c8c0b21`: the quality ratchet's 1.4.0 and 1.5.0. A gate whose command outlives its time budget reads `unmeasured` instead of an exit code of 127, and the command's whole process group is stopped.

I sent whole files rather than only the layout hunks because the hunks do not apply to your copies: a three-way merge of your copy, the copy this work started from (`c8b9ddd`, on my fork) and my tip conflicts in 51 places in 8 files, 34 of them the dashboard's two copies (command at the end).

**Three choices in the dashboard** ride along with that lineage. They are policy, so each is yours to refuse:

- The dashboard's `--sync` takes a directory and skips a target that git tracks or that is brand new unless `--force`. You answered #67 with a remedy that says `cp <canonical> <copy>`; this replaces it.
- `"methodology"` is no longer in `EXCLUDE_DIRS`, so a portfolio run scores this repository too.
- How the dashboard recognises a project's installed copy of a framework tool is one table, and the name list (`FRAMEWORK_INSTALLED_SOURCE`) is derived from it. Yours keeps the list and a separate signature table with a test that they agree. After this a name cannot be added without saying how a file of that name identifies itself. The same 7 names are recognised either way; what changes is the design of your code.

It also fixes one defect: `git log --reverse --format=%ai -1` applies `-1` before it reverses, so `first_commit_date` is the newest commit and a project's age is days since its last one. The dashboard now reads the root commits (`--max-parents=0`).

## How to read it

31 commits, 47 files (38 changed, 9 new), +19,821 / -1,150: `git diff --shortstat f34769f HEAD` and `git rev-list --count f34769f..HEAD`. Every commit but the first touches at most 5 files. The numbers below are the head's. While building I ran the suite and the gates in a clean clone at the last commit of each group in this table; I did not re-run every commit alone for this description.

| Commits | What |
|---|---|
| `bbe0dc3` | not layout: dashboard 2.21.0, trimmer 1.7.0, the suite's `skip` (+7,765 / -575, 9 files) |
| `14ef959` | `tools/layout_resolver.py`, `tools/layout_fixtures.py`, `bin/check-layout-literals` (finds a root path written into a tool), and `NEW_LAYOUT`, the manifest's second table, which is data |
| `fd96593`, `c8c0b21` | the ledger pre-commit hook and the quality ratchet read either layout (ratchet 1.3.0); then ratchet 1.4.0 and 1.5.0, not layout |
| `98ca7fc`, `e9c5cb8`, `dd581fe` | the trimmer 1.8.0, `context_budget.py` 1.4.0 and the dashboard 2.22.0 each find a project's files at either place; the trimmer writes its archive shard and proof beside the ledger it trims |
| `4c0bdde`, `261b8d3`, `0aa1897` | `bin/sync` (`--layout auto\|legacy\|new`), `bin/status`, `bin/check-links` (`--layout legacy\|new\|both`) and the manifest reader, which reads `NEW_LAYOUT` as data for `--source=github`; with their 82-test suite |
| `a459b8b`, `505541c` | `bin/check-ledger` and `bin/check-handoff` read either layout (the layout hunks only; the rest of my versions of them stays on my fork) |
| `c8d4375` to `18cda0f` | the documents say where the files sit and their references hold in both layouts; `bin/check-links --layout both` runs in `bin/tests.sh` |
| `2942e46`, `ab35e96` | `bin/migrate-layout` and its 280-test suite |
| `5afc962` | a cited gate run that reads unmeasured gates must be repaired or name them (`starter-kit/HANDOFFS.md`, `HOW_TO_USE.md`; 5 lines) |
| `c933b0f` to `28f99a7` | ten commits that take out references only my fork can resolve, from comments and docstrings (the first seven; no program token changes) and from text a program prints (the last three). Skippable as a run |
| `ced2c82` | `python3 starter-kit/context_budget.py --status` read `SESSION_RUNNER.md` as over its ceiling after the documents commits; this drops one duplicated example command (84 B). It also edits one line of `.context-budget.json` that records the file's new density and **loosens that gate's line by 43 B**; that hunk is separable |

The ten commits did not remove everything. A grep for four kinds of reference of mine still finds 56 added lines, 36 of them comment lines (`git diff f34769f HEAD -- . ':!docs' | grep -E '^\+[^+]' | grep -cE 'BL-[0-9]+|\bS[0-9]{2,3}\b|\bD[0-9]{1,2}\b|Learning #[0-9]+'`). A script on my fork that counts more kinds read 654 added lines in 28 files before the ten commits and 25 in 6 after.

## What a project sees

**A legacy project gets the same paths.** Two throwaway projects, one synced by upstream's `bin/sync` and one by this branch's, then the trees diffed:

```
git init a-up && git -C a-up commit --allow-empty -m init ; cp -R a-up a-pr
python3 <upstream checkout>/bin/sync a-up ; python3 <this branch>/bin/sync a-pr
diff -rq --exclude=.git a-up a-pr
```

Both write the same 30 paths and neither makes a `methodology/` directory. 22 of them differ in bytes, and every one is a file this pull request changes (`git diff --name-only` over `starter-kit/`, `workstreams/` and the three manuals). `pr4-fixture.sh`, in [my fork's evidence directory](https://github.com/rmsharp/methodology/tree/main/docs/planning/pr-composition-evidence), runs this and the next.

**A project's own files are not overwritten.** The same project with its 7 seeds edited and its framework files at upstream's tip: upstream's `bin/sync` writes 0 paths; this branch's writes 19 (every framework file it changes, nothing else), needs no `--force`, and changes 0 of the 7 seeds.

**A project that has moved is synced as the project it is.** Synced by the `bin/sync` on `main` today, a project under `methodology/` gets 23 framework files written at its root beside the moved ones, and two of my projects' own pre-commit hooks refused that commit as half-migrated. That is why the sync tools are in this pull request and not left for later.

**My own 12 projects,** which you cannot reproduce: measured in `--no-local` clones of their committed HEADs by `pr3-adopters.py` in that directory. 7 are under `methodology/` and 5 are not. This branch's `bin/sync` changed none of their seeds and created 13 where a project had none. It refuses a plain run at 10 of the 12, 39 files in all. 38 of those are versions of a file from my fork's history that no commit of this branch carries, so that count is mine and not yours; one `--force`, then a plain run writes nothing at all 12. The 39th is a project's own 49 added lines in its copy of `methodology_trim.py`, which `--force` drops without saying so (below).

## Evidence

Each in a clean `--no-local` clone of the pull request's head (0 dirty paths), serially, exit codes read bare; upstream's tip is the control. `pr4-claims.sh` in the same directory runs them all.

| Claim | Command | upstream `f34769f` | this branch |
|---|---|---|---|
| the suite passes, and holds more | `bash bin/tests.sh` | 261 passed, 0 failed | 302 passed, 0 failed, 0 skipped |
| every declared gate holds | `python3 starter-kit/quality_ratchet.py --run` | 12/12 pass, 0 fail, 0 unmeasured | 18/18 pass, 0 fail, 0 unmeasured |
| both layouts' links resolve | `python3 bin/check-links --layout both` | usage error, takes only `--tree` (exit 2) | OK: 80 links across 23 documents, in each layout |
| no root path is left in a tool | `python3 bin/check-layout-literals` | not present | 15 files, 0 sites |
| one resolver, byte for byte | `python3 tools/test_layout_resolver.py` | not present | 76 tests OK; 11 copies, each equal to the module |
| every frozen proof gives the verdict it gave | `bash <proof>` for each tracked `*.verify.sh` | exit 0 (the one tracked proof) | exit 0 (the same proof) |
| gates tighten and none loosens | `compare()` of the branch's ratchet, each commit against its parent | | 0 refusals over 31 commits; gates 12 to 18, five floors raised, none lowered |

The unit suites behind the gate: dashboard 395 tests (upstream's floor 229), trimmer 218 (124), quality ratchet 120 (45), context budget 163 (148), and four new: layout 76, checkers 11, sync 82, migration 280.

## What this does not show

- **The route a project takes alone from GitHub.** Every sync above used the local source, not `--source=github`.
- **Anything about a project that is not mine.** The 12 are mine, and 10 carry versions of the framework's files that are in no history here. A project on your released files is the fixture above.
- **Windows, your machine, hooks armed in another clone, or a project's own CI.** This repository has no CI, so every check is local.
- **My own suite as a whole.** It has blocks that read this repository's ledgers, backlog and archive as fixtures and cannot run on your tree; they are not carried, so `bin/tests.sh` here is yours plus the changes above.
- **Enforcement of the rule in `5afc962`.** The check lives in my version of `bin/check-handoff`, which is not carried, so the rule is prose; the session runner's own sentence for it is left out because the runner is at its ceiling.

Known gaps from the 12 projects, open:

- Like the `bin/sync` on `main`, a sync refuses a project's edited framework file by name but does not say which published version is nearest or how many lines differ, and `--force` then drops the edit.
- Moving only the framework's files (`--tier 1`) leaves the dashboard writing a second history file under `methodology/` while the root's old one stays, unused.
- On a ledger in the old format (no month headings) the migration's own entry lands at the end, so the ledger has two orders; `bin/check-ledger` fails before and after.
- For the hook that `context_budget.py install-hook` writes, the migration warns that it "will refuse the migration commit". It does not.
- An older copy of the ledger hook that a project armed itself keeps looking for the ledger at the root; once the ledger moves it passes every commit without saying so. The hook in this branch follows the ledger.
- A project's own tests or scripts that read a moved file by name can break. The tool lists the files whose text mentions a moved name; that list is an upper bound, not the set that breaks.

## Order with the open pull requests

- **#94** (`972eb2cd6263`): conflicts in 3 files and 17 regions: the trimmer 10, its tests 6, `.quality-gates.json` 1 (`git merge-tree --write-tree`). Of the 430 lines #94 adds to `starter-kit/methodology_trim.py`, all but 11 are in this branch as exact lines; the 11 are the version string, comment wording and the tool's name in four messages (this branch prints it from a constant). Of the 1,136 lines it adds to the tests, all but 9 are here (comments and docstrings). The floor in `.quality-gates.json` is 181 there and 218 here (`pr4-supersede.sh`, same directory). I have not resolved the conflicts.
- **#92** (`fa2bb5d464f9`): merges clean (`git merge-tree --write-tree`, exit 0). This branch touches neither `CLAUDE.md` nor `README.md`.

I have not bumped the framework's release version. Release notes would be a separate pull request after a merge, in the manner of #92.

Command for the conflict count: for each file the `methodology/` work changed since `c8b9ddd` that upstream also has, `git merge-file -p <your copy> <c8b9ddd's copy> <my tip's copy>`; the exit status is the number of regions (`pr4-mergefile.sh`, same directory).
