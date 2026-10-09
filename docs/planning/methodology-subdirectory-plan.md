# Moving the methodology files into one `methodology/` directory — analysis and plan

**Status: DECIDED (S273). The plan was that session's deliverable; P1 to P12 are done, as §7 records (P11 at tier 1, P12 at tier all).**
**Ratified by the operator on 2026-10-06 at S273's close-out picker, every one as recommended (§9).** **P0 to P12
are done (§7.1 to §7.4b, S274 to S287); P13 is next, and tier 2 is open.**
Base commit `c8b9ddd` (fork `main`; it contains all of `upstream/main`, 0 commits behind). **Declared budget: 60,000 B**, one agent
read at prose density, as [`file-management-system-plan.md`](file-management-system-plan.md) sets the
norm. This file is in the population of that plan's retirement rule like every other planning file.

> **The request** (the operator, 2026-10-06): *"analyze the following and if possible make a detailed
> implementation plan: a movement of methodology files from the repos' root to a 'methodology'
> subdirectory that houses all of the methodology files 1 layer lower in the new directory. It would
> clean up the base directory and would clearly identify which files are part of the methodology
> infrastructure. Perhaps this structure could also be used by methodology's own repository."*

Evidence for every number below is re-runnable from
[`methodology-subdirectory-evidence/`](methodology-subdirectory-evidence/) (§11).

---

## 0. The answer first

1. **Feasible. No showstopper found. Large:** 22 to 29 sessions by §7's count (about 25), nearly all of it in the
   shipped tools and one adopter per session. No paid run is involved.
2. **It is a consolidation, not a rename.** Today an adopter keeps its methodology files in **two**
   places: **18 at the project root** (11 that `bin/sync` keeps current, 7 it seeds once) and **12 under
   `docs/methodology/`** (`bin/_manifest.py:41-93`, 30 entries). The target merges both into
   `methodology/`.
3. **Nobody proposed it before** (§2.3 names what was searched). The B1 plan's Decision 1b deferred a
   canonical-side mirror as *"a possible future campaign"*; this plan is that campaign, aimed at a different layout.
4. **What makes it hard is not the files; it is that the shipped tools, the hooks and every adopter's own files read these paths as literals** (17 couplings, §3).
   In scratch clones of `bin/tests.sh`: baseline **452 / 0 / 0**; moving **only** the two ledgers gives **418 / 12 / 3**, and the
   archive directory too **414 / 11 / 5** (§3.1). Worse than a red: **the ledger co-staging hook silently stops binding**: with the
   ledger at `methodology/CHANGELOG.md` a commit with no ledger entry is **passed**, where the unmoved control is refused (§3, C5).
   A green suite is therefore not evidence about a move; §8 names the criteria that are.
5. **Two feared risks were measured and are not risks.** All **117** frozen `.verify.sh` losslessness
   proofs give the same exit codes before and after moving the ledgers, and after moving the archive
   directory as well (§3, C7). A nested `methodology/.gitattributes` carrying `merge=union` merges two
   ledger edits cleanly, and the same merge without it conflicts (§4.2, E1).
6. **Syncing is half the problem** (the operator's addition, §5A). `bin/sync` would write a blank ledger beside a real one; the dashboard
   is a **second** sync channel that writes at the project root; and **this repository's own resync with `upstream` changes shape once its
   files move**: git pairs none of the moved ledgers or JSON files against the merge base, so one synthetic upstream edit gives 4 modify/delete
   conflicts and a file-location conflict where the unmoved fork gives 3 text conflicts (§5A.4; the maintainer made 142 of 234 root-ledger
   commits). The plan's answers: sync before migrate, `--layout auto` through the window, and **this repository's real files move only after
   the upstream decision (D8)**; P8 is a rehearsal in a scratch clone.
7. **Recommended shape:** *expand → migrate → contract* (§4.5), a layout resolver every shipped tool
   embeds (§4.3), two tiers (the framework's own files first, the project's state files second), the
   adopters one per session, and **a gate before** restructuring this repository's distributed source
   paths (§5).
8. **Decisions** (all ratified, S273, §9): D1 all the files, in two tiers; D2 flat, `workstreams/` the only
   subdirectory; D6 this repository rehearses only; D8 the fork first, then one pull request.

---

## 1. The request, and how it is read

- **"methodology files"** = every file in `bin/_manifest.py`'s `DISTRIBUTION`, plus what the tools
  generate beside them (`dashboard.html`, `dashboard_history.jsonl`, `.context-budget-history.jsonl`,
  `.quality-gates-results.json`) and the ledger shards. Not: the project's own `BACKLOG.md`,
  `CONTEXT.md`, `PROJECT_LEARNINGS.md`, `README.md`, `docs/` — no manifest entry creates them (D1).
- **"1 layer lower"** = directly under the root: `methodology/SESSION_RUNNER.md`, never
  `methodology/docs/...`. `workstreams/` stays the one subdirectory it already is (D2).
- **Two targets:** Part A, the adopters (12 sibling projects here, and every external adopter); Part B,
  this repository (§5). They are separable and Part A does not need Part B.
- **Syncing** (the operator's addition): how adopters are kept current while their layout changes, and how
  this repository stays in sync with `upstream` and `origin` once its own files move (§5A).
- **What cannot move, whatever is decided:** `CLAUDE.md` (the file Claude Code loads from the project
  root), `.git*` infrastructure, `.github/`, the project's own `README.md`, `LICENSE`, `docs/`.

## 2. What exists (evidence)

### 2.1 Where an adopter's methodology files are today

| Group | Count | Files | Disposition |
|---|---:|---|---|
| Project root, tracked | 11 | `SESSION_RUNNER.md` `FRAMEWORK_LEARNINGS.md` `SAFEGUARDS.md` `RECOMMENDED_SKILLS.md` `CONTEXT_TEMPLATE.md` `CLAUDE_TEMPLATE.md` `BOOTSTRAP.md` `methodology_dashboard.py` `methodology_trim.py` `context_budget.py` `quality_ratchet.py` | canonical owns; `bin/sync` overwrites toward canonical |
| Project root, seeds | 7 | `SESSION_NOTES.md` `CHANGELOG.md` `HANDOFFS.md` `ROADMAP.md` `.context-budget.json` `.quality-gates.json` `.gitattributes` | written once if absent, then the project's |
| `docs/methodology/` | 12 | `ITERATIVE_METHODOLOGY.md` `HOW_TO_USE.md` `FRAMEWORK_APPARATUS.md` and `workstreams/` (6 workstreams, 3 campaigns) | canonical owns |
| Generated beside them | 4 | the dashboard page and history, the budget history, the ratchet results | tool output |

Not in the manifest, so not delivered today: `starter-kit/close_out_report.py` (BL-79 P1; its
distribution is P3, its own go-ahead), the git hooks (copied by hand), `bin/*` (canonical-only).

### 2.2 The 12 adopters (read-only survey, `adopter-survey.sh`)

All 12 are in **committed** mode: none gitignores a methodology file. The `ignore` mode exists and is
documented as first-class (`starter-kit/BOOTSTRAP.md:42-50`), and §3 C2 covers it.

| Project | Tree / last commit | CLAUDE.md lines naming a path | `.context-budget.json` / `.quality-gates.json` | Other places that name a path |
|---|---|---:|---|---|
| `airqino` | main, dirty 4, 2026-09-18 | 12 | 6 / 2 | `docs/methodology/` also holds a nested `starter-kit/`, `bin/`, README |
| `chat_verification` | main, dirty 1, 2026-08-13 | 9 | 8 / none | `.githooks` 26 lines, `core.hooksPath` set |
| `church_growth` | main, dirty 1, 2026-08-10 | 17 | none | `.githooks` 10 lines, hooksPath set |
| `claude_work` | **no commits**, 16 untracked | 4 | none | not a repository with history |
| `dalia_martinez_funeral` | master, dirty 6, 2026-07-30 | 9 | none | `bin/` |
| `feedback-loop-comparison` | main, **clean**, 2026-05-08 | 8 | none | 2 files locally modified |
| `model_project_constructor` | master, **clean**, 2026-10-04 | 30 | 6 / 2 | `.claude/` permission rules 14 lines; `core.hooksPath` is an **absolute path** |
| `mts-system` | master, dirty 1, 2026-10-06 | 19 | 16 / 2 | `.claude/` 2 lines |
| `nprcgenekeepr` | master, **clean**, 2026-10-06 | 22 | 10 / 2 | **4 CI workflows** list ~20 methodology filenames in `paths-ignore`; `test_workflowPathsIgnore.R` checks the lists are identical |
| `Philippians` | main, dirty 4, 2026-10-03 | 11 | 6 / 2 | — |
| `vscode_quarto_ext` | master, dirty 2, 2026-10-06 | 24 | 28 / 4 | `.claude/` 1 line |
| `wsfct` | **active feature branch**, clean, 2026-10-06 | 42 | 14 / 2 | `.claude/` 5 lines |

Every adopter was behind on something (`bin/status`: 1 to 45 versions per file); `bin/sync` writes into a clean tree only.

### 2.3 Prior art and searches (absence claims name their reach)

- **No prior proposal.** `git grep` over the live tree and `docs/archive/`, and `gh issue list --state
  all --search 'root OR directory OR layout OR subdirectory'` (upstream), found nothing proposing a
  `methodology/` directory or complaining of root clutter.
- **B1 plan §4 and §4.2** (`b1-sync-coverage-expansion-plan.md:114-152`): the *link-topology paradox*.
  The canonical repo and an adopter use different layouts, so a relative link is right in one and dead
  in the other; distributed files author their links for the adopter layout, `bin/check-links`
  simulates an adopter tree to check them. Decision 1b (restructure the canonical repo to mirror the
  adopter layout) was **recommended against "for now"**.
- **`methodology-as-environment-plan.md` §1A**: the documented Quick Start is root files plus
  `docs/methodology/`; "we do NOT break it". This plan breaks it deliberately, with a transition
  (§4.5).
- **BL-74**: five adopters carry a hand-copied `docs/methodology/README.md` that `bin/sync` never
  updates. It moves with the rest or is retired; D4 (§9) decides.

### 2.4 The reference inventory (`inventory.py`, tracked files at `c8b9ddd`)

Files that name a methodology file, by who reads them:

| Class | Distinct files | What it is |
|---|---:|---|
| code + config | **31** | `bin/*` (10), `starter-kit/*.py` and seeds (8), `tools/*` tests, fixtures and the dashboard twin (8), this repo's `.context-budget.json`, `.quality-gates.json`, `.gitattributes`, `.gitignore` and `.githooks/pre-commit` (5) |
| distributed docs | **23** | the runner, bootstrap, safeguards, learnings, skills, templates, the three framework docs, the nine workstream and campaign files |
| canonical-only docs | **3** | `README.md` (347 lines), `CLAUDE.md` (76), `docs/FORK_LEARNINGS.md` (66) |
| history | 420 | `docs/archive/`, `docs/planning/`, `CHANGELOG.md`, `HANDOFFS.md`, tutorials: **frozen or fork-only record, not rewritten** |

The 57 non-history files are the plan's *files to change*. Two refinements, both measured:

- **Most mentions are bare names, and bare names stay true.** 118 relative markdown links exist in the
  distributed docs; **40 change** under a flat `methodology/` (35 between distributed files, 5 to
  project-owned files), 78 do not (`link-simulation.py`). The 6 tool-invocation lines and 38
  `docs/methodology` path lines in the distributed docs change. The ~2,400 name mentions in code and
  config are the part that is *not* mechanical (§3).
- **Every file the move touches already has a fixed set of references**; the inventory is the starting
  list for the gate §7 P1 builds (a scanner that fails while any shipped tool holds a bare root literal
  of a methodology filename outside the resolver), so it becomes a refusal and not a document.

---

## 3. The couplings that decide the design

Each row: where the tool reads the path as a literal, what a move does to it, the remedy, the phase that
owns it. File:line are at `c8b9ddd`.

| # | Coupling | What breaks | Remedy | Phase |
|---|---|---|---|---|
| C1 | `bin/sync` writes a **blank seed** whenever the destination is absent (`bin/sync:278-291`, loop `:344-352`) and overwrites TRACKED destinations in place | An unmigrated adopter synced with a new-layout manifest gets an **empty `CHANGELOG.md` beside its real ledger** and a second, current `SESSION_RUNNER.md` beside the stale one an agent still reads | Layout guard before any write: legacy tree + new layout = refuse, name `bin/migrate-layout` | P6 |
| C2 | Ignore mode lists TRACKED destinations file by file (`bin/sync:25-26`, `detect_mode :34-41`, `:407-424`) | A new layout makes every entry stale; `detect_mode` reads an ignored adopter as committed | Entries become `/methodology/<file>`; detect either layout; the `git rm --cached` hint follows the layout | P6 |
| C3 | `SEED_FORMAT_MARKERS` (`_manifest.py`) and `MIGRATION_ROUTES` (`bin/status`) are keyed by the seed's bare name; `bin/status` finds a seed at its manifest destination; `bin/check-links` simulates the adopter tree from `DISTRIBUTION` | Status reports a moved seed as absent and its format as unknown; links are checked in a layout nobody has | Both read the layout; `check-links` simulates both | P6 |
| C4 | The **ratchet**: config name fixed at the root (`quality_ratchet.py:51-52`), baseline read by path `git log -- .quality-gates.json` capped at 50 commits, removal refused; the installer writes `exec python3 "$(git rev-parse --show-toplevel)/<tool>" --precommit` with the tool's path **embedded at install time** and no `-f` guard | A move reads as "manifest removed"; the baseline **stops at the move** (E2), so a threshold lowered *inside the move commit* is invisible; every installed ratchet hook then **fails every commit loudly** (`python3` cannot open the moved tool) until `--install` is re-run, and a hook installed under `.git/hooks/` is per clone, so the migration commit cannot repair other clones. This repo's own hook guards with `[ -f "$top/starter-kit/quality_ratchet.py" ]` and would **skip silently** | Walk both paths with `--follow`; a move commit must be a pure rename or be refused; the migration tool re-runs the installer where it can and lists every clone-local hook it cannot reach | P2, P7 |
| C5 | `.githooks/pre-commit` names `CHANGELOG.md` at the root five times. The adopters' ledger hooks are older copies of the same logic (`chat_verification`, `church_growth`) | **Measured** (`hook-after-move.sh`): with hooks on, the unmoved control is refused (exit 1); the move commit **passes** (exit 0); a later commit that changes tracked content with no ledger entry **passes** (exit 0). After the ledger leaves the root, `git ls-files --error-unmatch CHANGELOG.md` fails and the hook takes its *"no ledger exists, never block"* branch (`:265`): **the gate that enforces failure mode #27 fails open, silently**, which is BL-77's failure mode, caused by the move itself. `.githooks/` must also **not** move: `core.hooksPath` is per clone and one adopter's is an absolute path | Layout-aware hook ships **before** any move, with the later-commit case (X2) as a permanent test; `.githooks/` stays at the root (D4) | P2 |
| C6 | The **never-edit gate** (`pre-commit`) refuses a change to any committed ledger entry | Entries hold relative links written when the ledger sat at the root: this repo's `CHANGELOG.md` has 79 (64 root-relative), `nprcgenekeepr`'s `HANDOFFS.md` 33. After a move they are dead **and cannot be rewritten**. No gate or test validates links inside a ledger (searched `check-ledger`, `check-handoff`, `bin/tests.sh`) | Do not rewrite. Convention, stated once in the runner: a ledger link is relative to the ledger's location *when written*. New entries use `../`-relative links | P8 |
| C7 | The **trimmer**: `ARCHIVE_DIR = "docs/archive"`, `REBASE_PREFIX = "../../"` (`methodology_trim.py`), links outside `../` and `/` are rebased by that prefix (`_in_domain`, `build_shard`) | After a move, a shard link written for a root ledger is wrong by one level (`../../methodology/` is the right prefix). **Not** the proofs: each shipped `.verify.sh` pins its own commits (`git show <trim>^:HANDOFFS.md`) and its own `PREFIX`, and **117 of 117 give the same exit code** with the ledgers moved, and with the archive moved too (`frozen-proofs.sh`: 112 exit 0, 5 exit 1 in all three trees; the 5 are the August shards, BL-36's class, not a result of a move) | `ARCHIVE_DIR` and the prefix derived from the ledger's directory; new shards' proofs carry the new paths; old proofs are never touched | P3 |
| C8 | The **dashboard** scores a project by path: the methodology checklist (`tools/methodology_dashboard.py:163-173`: `SESSION_RUNNER.md` 25, `SAFEGUARDS.md` 20, `SESSION_NOTES.md` 20, `BACKLOG.md` 15, three ledgers 5 each, `docs/methodology` 10 and `/workstreams` 10, sum 115), the adoption test `(path / "SESSION_RUNNER.md").is_file()`, the installed-source fingerprint | A migrated adopter scores **0 of 115** on that dimension, reads as "not adopted", and owes no ledger until the scanner learns the layout. 79 string constants in the file name a root path (`bin/check-layout-literals`, S274; this plan's first count, 51, came from one grep that could not be reproduced) | Resolver; the checklist items become names resolved through it; `.methodology-profile` stays the override | P5 |
| C9 | `context_budget.py` (`CONFIG_NAME`, `HISTORY_NAME`, `find_root`) and the ratchet read their config by a fixed name under the root; the config's own `files[]` and `command` strings hold root paths (6-28 lines per adopter in `.context-budget.json`, 2-4 in `.quality-gates.json`) | Seeds are adopter-owned and `bin/sync` never rewrites them, so every adopter's config needs a migration the tool must perform | `bin/migrate-layout` rewrites paths inside the two JSON files, shows the diff first | P4, P7 |
| C10 | `close_out_report.py` defaults `HANDOFFS.md` (`:71`, `:178`, `:224`); its Stop-hook command bakes `os.path.abspath(__file__)` (`:213`) | A move silently stops the hook. **Not installed anywhere today** (searched `~/.claude` and seven adopters' `.claude/`) | Write the install snippet layout-aware before anyone installs it | P3 |
| C11 | Adopter-owned references: `CLAUDE.md` (4-42 lines each, including the SESSION PROTOCOL block that names `SESSION_RUNNER.md`: `CLAUDE_TEMPLATE.md:9`), CI `paths-ignore` (`nprcgenekeepr`), `.claude/` permission rules, `.gitignore` | Agents are pointed at a file that is no longer there; CI starts running on doc-only commits; one R test fails | The migration tool lists every hit, rewrites `CLAUDE.md` paths from a printed diff, reports the rest. A benefit: ~20 `paths-ignore` lines become `methodology/**` | P7, adopters |
| C12 | `bin/sync:68` and `bin/status:82` recognise an older canonical version by `git log --full-history -- <src path>` | **Only if Part B moves the source paths:** a version before the move is not found, so an adopter on it reads *"locally modified"* and `bin/sync` refuses (the BL-54 and BL-66 class) | Manifest aliases (`was:`), unioned in both walks; a test that builds the pre-move case | G-B |
| C13 | The suites encode the layout: `bin/tests.sh` (427 mentions), `tools/test_methodology_dashboard.py` (570), `tools/test_methodology_trim.py` (298) | **Measured, §3.1** | One layout constant; tests parameterised over both layouts | P1-P6 |
| C14 | A name collision: the adopter's new `methodology/` and the canonical checkout the docs call `../methodology` (`bin/sync --help`, `BOOTSTRAP.md:36-72`) | Prose that says "`methodology/bin/sync`" becomes ambiguous | The docs say *canonical checkout* for the one and `methodology/` for the other; one sentence in `BOOTSTRAP.md` | P9 |
| C15 | `methodology_dashboard.py --sync` is a **second sync channel**: it writes `<project>/methodology_dashboard.py` at each project's root by a literal, outside the manifest (`tools/methodology_dashboard.py:1375`, `:1385`, `:1389`), and every older copy's stale-version warning prints that command (`:1026-1053`) | After a migration a portfolio `--sync` would create a second dashboard at the root of every migrated project (gated off without `--force`, written with it) | Resolve each target's layout; the advice prints the resolved directory | P5 |
| C16 | `--source=github` reads the clone's `bin/_manifest.py` **as data** (`bin/_manifest_reader.py`; the rule at `_manifest.py:31-37`; `bin/tests.sh:4205`, Test 53) | A destination computed by a function breaks the route and Test 53 | Layout-dependent destinations are a second literal table | P6 |
| C17 | Fork ↔ `upstream`: upstream keeps root copies of the five instance files and its maintainer edits them (§5A.4) | **Measured:** once this repo's files move, git cannot pair them with upstream's copies and the next resync conflicts as modify/delete on four files, plus a file-location conflict on any new shard | P8 is a rehearsal; the real move waits on D8 | P8, G-B |

### 3.1 What a partial move does to the suite (measured, clone of `c8b9ddd`, `bin/tests.sh`)

| Tree | Passed | Failed | Skipped |
|---|---:|---:|---:|
| baseline, nothing moved | **452** | 0 | 0 |
| **A**: `CHANGELOG.md`, `HANDOFFS.md` moved to `methodology/` | 418 | **12** | 3 |
| **B**: A, and `docs/archive/` moved to `methodology/archive/` | 414 | **11** | 5 |

Serial runs in `--no-local` clones, hooks off, nothing else running; the failing assertions and skips are
in `suite-blast-radius.txt`. Tree A's three skips are the checks that print *"no root `HANDOFFS.md`, so the
reserve was not measured"*: they read as green and measure nothing, which is the failure this repository has already met
(Test 31's vacuous 0 = 0 after a trim). Passes fall by 34 and 38 while only 12 and 11 assertions
fail: the rest are assertions a crashed or skipped section never reached. **So the criterion for every
phase is the unmoved tree's own triple, compared in the same state: failed 0, and passed and skipped
exactly as the unmoved tree reads them**, never "the suite is green". The triple depends on how many
receipts `HANDOFFS.md` holds, because Test 34 prints six stated SKIPs below three (fork Learning #70): the
452 / 0 / 0 above is the **three-receipt** baseline at `c8b9ddd`, and after P1 wired one suite the unmoved
tree reads **453 / 0 / 0 at three receipts and 447 / 0 / 6 at two** (S274, measured). A phase that starts
just after a trim measures its baseline at two and compares its moved tree at two: those six skips are
not a move's silent skips. Re-measure the baseline at each phase's own start.

---

## 4. Design

### 4.1 The target layout (an adopter, final state)

```
project/
  CLAUDE.md                     stays: Claude Code loads it from the root
  .githooks/ .github/ .gitignore .claude/        stay: git, CI and harness infrastructure
  README.md LICENSE docs/ src/ ...               stay: the project's own
  methodology/
    SESSION_RUNNER.md SAFEGUARDS.md FRAMEWORK_LEARNINGS.md RECOMMENDED_SKILLS.md
    BOOTSTRAP.md CONTEXT_TEMPLATE.md CLAUDE_TEMPLATE.md
    ITERATIVE_METHODOLOGY.md FRAMEWORK_APPARATUS.md HOW_TO_USE.md
    methodology_dashboard.py methodology_trim.py context_budget.py quality_ratchet.py
    SESSION_NOTES.md CHANGELOG.md HANDOFFS.md ROADMAP.md          (tier 2: the project's state)
    .context-budget.json .quality-gates.json .gitattributes       (tier 2)
    dashboard.html dashboard_history.jsonl .context-budget-history.jsonl .quality-gates-results.json
    archive/                                                      (tier 2, D5)
    workstreams/   (9 files)
```

The root of a project that keeps its own `README.md`, `docs/` and source then holds `CLAUDE.md` and
infrastructure dotfiles, which is the clean base directory the request asks for. A side benefit,
measured in §2.2: a root `CHANGELOG.md` becomes free for the project's *product* changelog (upstream
issue #60 records a `docs/` product changelog masking a missing action ledger), and the
`nprcgenekeepr` CI filter shrinks to one entry.

### 4.2 Root decisions

| File | Decision | Why | Evidence |
|---|---|---|---|
| `CLAUDE.md` | stays | the file Claude Code loads at session start | `CLAUDE_TEMPLATE.md:3`, BOOTSTRAP Step 5 |
| `.githooks/` | stays | `core.hooksPath` is set **per clone**; moving the directory unarms every other clone silently (BL-77); one adopter's value is an absolute path | survey §2.2 |
| `.gitattributes` | **moves**, as `methodology/.gitattributes` | with a nested file `CHANGELOG.md merge=union` merges two ledger edits cleanly (exit 0); without it the same merge conflicts (exit 1). It also stops the seed's `*.jsonl` and `CHANGELOG.md` rules from reaching a project's own root `CHANGELOG.md` | **E1**, `git-behaviour.sh` |
| `.github/`, `.gitignore`, `.claude/` | stay | the host's and the harness's own locations | — |

### 4.3 The layout resolver

One function, embedded in every shipped tool that finds a methodology file, returns the directory that
holds them:

| `R/methodology/SESSION_RUNNER.md` | `R/SESSION_RUNNER.md` | Result |
|---|---|---|
| exists | absent | **new** layout, directory `R/methodology` |
| absent | exists | **legacy** layout, directory `R` |
| exists | exists | **half-migrated**: stop, name both, never guess |
| absent | absent | the framework repo (`starter-kit/SESSION_RUNNER.md`) or not an adopter |

The shipped tools are single stdlib files that adopters receive one by one, so there is no shared module
to import; each carries the same marked block (`tools/layout_resolver.py`, 15 lines), and a canonical test
asserts the copies are byte-identical (`embedded_block`; the dashboard's twin test is the precedent). The
shell hook cannot call it; it tests the same two paths.

**The table is keyed on an anchor file the caller names (refined at P1, S274).** `SESSION_RUNNER.md` is the
default, for the framework's files; a tool that reads a state file (a ledger, a JSON config) resolves with
`CHANGELOG.md`. One directory is not enough: §4.6 makes a tier-1-only adopter (framework files moved,
ledgers still at the root) a coherent end state, and a tool that found the ledger through the runner's
directory would look for a file that is not there, which is C5's silent fail-open again.
**Every tool resolves once per anchor and derives every other path from the result**, so a path is
written in one place.

### 4.4 One documentation convention, not 2,400 edits

Bare filenames stay true if the runner says, once: *"Names of methodology files in these documents are
relative to the directory that holds this file."* The SESSION PROTOCOL block in `CLAUDE.md` names the
directory once (`Read and follow methodology/SESSION_RUNNER.md`). What is rewritten is only a **path**:
the 38 `docs/methodology` lines, the 6 invocation lines, the 40 links (§2.4).

### 4.5 Expand, migrate, contract

| Stage | What ships | Adopter effect | Reversible by |
|---|---|---|---|
| **Expand** (a minor release) | Tools, hooks, `bin/sync`, `bin/status`, `bin/check-links` and the dashboard understand **both** layouts; `bin/sync --layout auto` (per project: legacy stays legacy, migrated stays migrated, an empty directory gets the default); `bin/migrate-layout` ships, opt-in | none until an adopter runs the migration | not shipping the next stage |
| **Migrate** | One adopter per session, each synced first (§5A.2); this repository's own files only after D8 | that adopter's layout changes in one commit | `git revert` of that one commit |
| **Contract** (a major release, **its own go-ahead**) | New projects and `bin/sync` default to the new layout; a legacy tree is refused with the migration command | a still-legacy adopter must migrate before it can sync | — |

The order is forced by C1 and C5: a tool that writes the new layout before the hooks and the guard
understand it damages the adopters it was meant to tidy.

### 4.6 Two tiers

| Tier | Files | Couplings it brings |
|---|---|---|
| **1: the framework's own files** | the 11 tracked root files, the 12 `docs/methodology/` files | C1, C2, C3, C8 (checklist), C10, C11 |
| **2: the project's state** | the 4 seeded ledgers and notes, the 2 configs and `.gitattributes`, the 4 generated files, the archive | C4, C5, C6, C7, C9 |

Tier 1 alone leaves 7 files at the root (still a clean root), carries the cheap couplings, and is a
coherent end state. Tier 2 carries every coupling that touches history or a gate. The migration tool
takes `--tier 1|2|all`; the default is `all` (D1).

### 4.7 The migration tool (`bin/migrate-layout`, canonical-only like `bin/sync`)

Dry run by default. Refuses a dirty tree, a half-migrated tree, any destination that exists, and a
tree where `bin/status` does not read every TRACKED file `current` (sync first, §5A.2).

1. **Plan.** Print every `git mv` (source → destination), derived from the manifest; every path rewrite
   in `.context-budget.json`, `.quality-gates.json`, `CLAUDE.md`, `.gitignore` (a diff); every hit it
   will **not** rewrite and why (CI workflows, `.claude/` rules, `.githooks/` copies, ledger links).
2. **Apply** as **one commit**: all renames with their rewrites and one new ledger entry. Git must
   detect each file as a rename (`git diff -M --name-status`): the tool asserts every moved file keeps
   ≥ 90% similarity, so `git log --follow` reaches the earlier history (E2).
3. **Never** rewrites a committed ledger entry (C6) or a frozen shard or proof.
4. **Verify**: `bin/status` (all `current`), `check-handoff`, `check-ledger`, `quality_ratchet.py
   --run`, the dashboard, `bin/check-links`, and for a project that has shards, every `.verify.sh`
   (the exit histogram must be unchanged).

### 4.8 Ledger continuity (measured, E2)

After `git mv CHANGELOG.md methodology/CHANGELOG.md`, `git log -- methodology/CHANGELOG.md` stops at the
move; `--follow` reaches every older commit; the old path still answers in full; the frontier
(`git log -1 -- <new path>`) is the newest commit. Phase 0's reconcile therefore keeps working after a
move, **provided** it names the resolved path. Every tool that reads a ledger's *history by path*
(the ratchet, C4; the dashboard's lag signal) must follow the rename.

---

## 5. Part B: this repository

"This structure could also be used by methodology's own repository" has three readings. They differ in
what moves, and in the couplings they carry (C12 only the third, C17 both).

| | What moves | New cost | Gains |
|---|---|---|---|
| **B0** nothing | — | — | — |
| **B2: instance files** | this repo's own *instances*: `CHANGELOG.md`, `HANDOFFS.md`, `.context-budget.json`, `.quality-gates.json`, `.gitattributes`, the two histories, the generated page, `docs/archive/` | no source path moves, so no C12. **But C17 (§5A.4):** git cannot pair the moved ledgers or JSON files with upstream's root copies, so the next resync that carries a maintainer edit conflicts as modify/delete | the root loses ~10 files; as a *rehearsal in a clone* it exercises the resolver, hook, ratchet, trimmer and 117 proofs on the largest real ledgers before any adopter |
| **B1: full mirror** | the distributed sources as well: `starter-kit/*`, the three root framework docs and `workstreams/` become `methodology/` | **C12** (history by source path; 31 source renames, 36 with B2's instance files, plus aliases); rewrites README and every `starter-kit/…` reference (24 code and config files, 3 distributed docs, 3 canonical-only docs); the fork is about 1,470 commits ahead of upstream, so a path move there is a merge cost for the maintainer; a name clash: `starter-kit/CHANGELOG.md` (the seed) and the live `CHANGELOG.md` cannot both be `methodology/CHANGELOG.md` (seeds would move to `methodology/seeds/`) | the link-topology paradox vanishes: a distributed link resolves identically in the repo and in an adopter, and `check-links` stops needing a simulation. This is B1 Decision 1b |

**Recommendation (D6): B0 for this repository's real files until D8 is answered; B2 as a rehearsal in a
scratch clone (P8); B1 only at a gate.** B2 moves files that are not distributed, but they are *synced*,
and §5A.4 measures what that costs. B2 ships if the maintainer adopts the layout (then both sides rename
the same files) or the operator accepts hand-resolved conflicts at each resync. The gate (G-B) for B1
opens when at least three adopters have migrated cleanly **and** the operator wants the paradox gone
enough to pay C12 and C17. B1 is a separate campaign with its own plan.

## 5A. Syncing: the adopters, and this repository

*Added at the operator's instruction, mid-session (2026-10-06): the plan must account for syncing the
adopter repositories as well as this one. It is read two ways and both are covered: how adopters are
kept current while their layout changes (§5A.1-§5A.3), and how this repository stays in sync with
`upstream` and `origin` once its own files move (§5A.4).*

### 5A.1 The channels that write into an adopter, and what each knows about paths

| Channel | What it writes | Path knowledge today | What the change does |
|---|---|---|---|
| `bin/sync <project>` | the 23 TRACKED files in place, the 7 seeds once; in `ignore` mode the `.gitignore` entries | manifest destinations (`bin/_manifest.py:41-93`) | C1, C2 |
| `bin/status <projects>` | nothing; reports drift per file | the same manifest | C3 |
| `methodology_dashboard.py --sync [DIR]` | **only** `<project>/methodology_dashboard.py` at each project's **root**, and a copy at the portfolio root | a literal in the dashboard (`tools/methodology_dashboard.py:1375`, `:1385`, `:1389`), **not** the manifest; every older copy's stale-version warning advertises this command (`:1026-1053`) | **C15** |
| `bin/sync --source=github` | as `bin/sync`, from a fresh clone | reads the clone's `_manifest.py` **as data** (`bin/_manifest_reader.py`; the file's own rule, `_manifest.py:31-37`: literals, one plain assignment per name) | **C16** |
| The manual and prose route (README Quick Start, BOOTSTRAP *Setup by manual copy* and *Without `bin/sync`*) | whatever the adopter or its agent copies | prose paths, and three rules that stop a prose update overwriting a ledger (BOOTSTRAP `:362-400`, PR #88) | P9 |

Adopters sync from **this fork's working tree** (`--source=local`, the sibling checkout), so they receive
the fork's version of every distributed file, ahead of `upstream`.

### 5A.2 Rules for the migration window

1. **Sync before migrate.** An adopter is migrated only when `bin/status` reads every TRACKED file
   `current`; `bin/migrate-layout` refuses otherwise. The 12 adopters are 1 to 45 versions behind on
   something, their old tools do not know the new layout, and §3.1 shows what tools that cannot find the
   ledger do. Each adopter's session is therefore: `bin/status`; `bin/sync` (one commit, BOOTSTRAP's
   rule); `bin/migrate-layout` (one commit); `bin/status` and the checkers again.
2. **`bin/sync --layout auto` from the expand release.** Per project: a legacy tree stays legacy, a
   migrated tree stays migrated, an empty directory gets the default. `bin/sync ../*` over a mixed
   portfolio is then correct at every point of the migration. The default flips only at contract (P23).
3. **One dashboard channel, resolved per target.** `--sync` resolves each project's layout and never
   writes a second copy at the root of a migrated project (the existing gate on new, ungitignored files
   stops that only without `--force`). The portfolio-root copy stays at the portfolio root and the
   stale-copy advice prints the resolved directory. BL-90 (a local `EXCLUDE_DIRS` overwritten by
   `--sync`) is untouched by this plan and is not folded in.
4. **The manifest stays data.** Layout-dependent destinations are a second literal table, not a function,
   so `--source=github` can still read them and Test 53 can still build its source from the file (C16).
5. **Adopters sync only from a recorded state of this repository.** Each adopter receipt names the sha of
   the checkout it synced from; P10 records the first sha adopters may use after the expand stage.
6. **Mixed portfolios are legal until contract.** `bin/status` over `*` names each project's layout, so a
   half-migrated portfolio is visible and a half-migrated *project* is an error.

### 5A.3 What P5, P6 and the adopter phases must show for sync

- A scratch portfolio of three projects (legacy, migrated, empty): `bin/sync --dry-run ../*` and the real
  run write exactly the expected files, none in the wrong layout, no blank seed (C1).
- `methodology_dashboard.py --sync` over the same portfolio touches `methodology/methodology_dashboard.py`
  in the migrated project and the root copy in the legacy one, and nothing else (C15).
- `--source=github` against a local repository whose manifest carries the new table: exit 0 (C16; Test 53
  is the harness).
- Per adopter: `bin/status` all `current` before the migration commit and after it.

### 5A.4 This repository's own sync with `upstream` and `origin` (measured)

Upstream keeps root copies of the files this repository would move, and its maintainer edits them:
`CHANGELOG.md` (242 commits, newest 2026-10-02; 142 of its 234 root-ledger commits are his),
`HANDOFFS.md` (84), `.context-budget.json` (8), `.quality-gates.json` (19), `.gitattributes` (2) and
`.context-budget-history.jsonl`. The fork's copies have diverged from the merge base `f34769f` by hundreds
of lines (`CHANGELOG.md` 573 added / 567 removed, `HANDOFFS.md` 76 / 656, `.context-budget.json` 108 / 71,
`.quality-gates.json` 20 / 5).

`resync-after-move.sh`, on clones: against `f34769f` git pairs **only `.gitattributes`** (R100) with its
moved copy; both ledgers and both JSON files read as a **delete and an add**, even at a 30% threshold. One
synthetic upstream commit (a line into each root file it owns, plus a new shard under `docs/archive/`)
merged into the fork gives:

| Fork | Result |
|---|---|
| unmoved (control) | 3 text conflicts (`.context-budget.json`, `.quality-gates.json`, `HANDOFFS.md`); `CHANGELOG.md` and the new shard merge cleanly |
| instance files and archive moved | **4 modify/delete conflicts** (both ledgers, both JSON files), **1 file-location conflict** (the new shard, inside the moved `docs/archive/`), nothing auto-merged |

Both are resolved by hand, but a modify/delete conflict shows no hunks: the upstream edit must be
re-applied into the moved file. The cost is not confined to those files. The 31 code and config files a
resolver touches are files upstream edits too (56 non-merge commits since 2026-09-01, 24 of them the
maintainer's; 44 of 103 in all history, under his two author names), so each of his edits is a
potential conflict with the fork's resolver edits for as long as upstream does not carry the same change.

**So:**

1. **P8 is a rehearsal in a scratch clone and ships nothing.** This repository's real instance files move
   only if the maintainer adopts the layout (both sides then rename the same files and git sees identical
   renames) or the operator accepts hand-resolved ledger conflicts at every resync.
2. **D8 gains a second reason:** the upstream route is what makes the fork's own layout sustainable, not
   only a courtesy.
3. **A resync goes first in any session that moves a file**, so no upstream edit is pending at the root
   path when the move lands; every move receipt names the `upstream/main` sha it was based on.
4. Nothing in this plan pushes to `origin` or sends anything to `upstream`; each is the operator's
   go-ahead, each time.

## 6. Alternatives considered

| Alternative | Verdict |
|---|---|
| **Status quo** plus a manifest file listing the methodology files | Identifies them without moving them, but the root stays crowded (18 files) and a list is the thing that decays (fork learning #81). The request is for a *directory* |
| **`docs/methodology/` for everything** (extend the half that exists) | Two levels down, contradicts "1 layer lower", and buries the runner behind `docs/` |
| **A hidden `.methodology/`** | Cleans the root but hides the files from the person the request wants to help *see* them |
| **Symlinks from the old root names** | Defeats the point (the root keeps 18 names) and symlinks do not travel through `bin/sync`'s `read_bytes` / `write_bytes` copy |
| **Tier 1 only** (§4.6) | Not rejected: a legitimate end state, and the default first release if the operator wants the cheap half first |

---

## 7. The phases

One phase is one session unless stated. Every phase closes out in full (`SESSION_RUNNER.md` Phase 3).
**Every phase's suite criterion is §3.1's: failed 0, and passed and skipped equal to the unmoved tree's,
measured at the phase's own start in the same receipt state.**

| Phase | Deliverable | Sessions | Needs |
|---|---|---:|---|
| **P0** | D1-D3 answered: **done, 2026-10-06** | 0 | the operator (done) |
| **P1** | The resolver, the layout fixtures, the **literal scanner** (RED, listing every site) | 1 | P0 |
| **P2** | Gate layer: `.githooks/pre-commit` and `quality_ratchet.py` (C4, C5) | 1 | P1 |
| **P3** | `methodology_trim.py` and `close_out_report.py` (C7, C10) | 1 | P1 |
| **P4** | `context_budget.py` and the canonical-only checkers (`check-handoff`, `check-ledger`, `check-learnings`, `check-overhead`, `model-report`) (C9) | 1 | P1 |
| **P5** | The dashboard and its twin, including its `--sync` channel (C8, C15) | 1-2 | P1 |
| **P6** | `bin/_manifest.py`, `bin/sync`, `bin/status`, `bin/check-links` (C1-C3, C16) and the sync proofs of §5A.3 | 1-2 | P2-P5 |
| **P7** | `bin/migrate-layout` and a dry run **over all 12 adopters, in clones** (C9, C11) | 1-2 | P6 |
| **P8** | **Rehearsal in a scratch clone** of this repo's instance files, and of a resync (C17); ships nothing | 1 | P7, D6 |
| **P9** | Documentation: README, BOOTSTRAP, runner convention, CLAUDE_TEMPLATE, HOW_TO_USE, APPARATUS, workstreams; `check-links` green in both layouts (C14) | 1-2 | P8 |
| **P10** | Release the *expand* stage and record the sha adopters may sync from (§5A.2); the upstream route is D8's decision | 0-1 | his go-ahead |
| **P11-P22** | One adopter per session (§7.4) | 12 | P10 |
| **P23** | Contract: flip the default (a major release, its own go-ahead) | 1 | all adopters migrated |
| **G-B** | Decide Part B1, and the real move of this repo's own instance files (C17, D8) | 0-1 | §5's gate, D8 |

22 to 29 sessions by this table (about 25). P11-P22 can batch if the operator chooses; the runner's
one-deliverable rule is the default.

### 7.1 P1 — the resolver, the fixtures, the scanner

- **DONE:** the resolver in one canonical-only module with the four-row table of §4.3 as its unit tests;
  a `tools/test_layout_resolver.py` suite wired into `bin/tests.sh`; **fixture trees in both layouts**
  that every later phase reuses; the **literal scanner**, run RED against `c8b9ddd` and listing every
  line that names a root path of a methodology file in a shipped tool (177 sites over 12 files at S274;
  the plan's first figures came from one grep that could not be reproduced); a ratchet gate for each new
  suite, floor set from its measured count.
- **Verify:** `bash bin/tests.sh > /tmp/o.txt` (capture it; the ratchet keeps none), the §3.1 criterion;
  `python3 starter-kit/quality_ratchet.py --run`; the scanner exits non-zero with the list.
- **Surface:** the canonical suite and scratch trees; not a real adopter's tools or a hook armed in a clone.
- **Boundary:** no tool changes behaviour. The scanner is RED on purpose, **not** a gate until P6.

### 7.2 P2-P6 — one layer each (all RED-first, both layouts green)

| Phase | DONE (each tool) | Verify | Surface, and what it cannot enforce |
|---|---|---|---|
| **P2** | DONE (§7.2a): hook and ratchet accept either layout; **X2, a later commit with no ledger entry, is refused (a permanent test)** | a mutant per behaviour; the two selftest gates | scratch repos with real hooks; not another clone's `core.hooksPath` |
| **P3** | DONE (§7.2b): the trimmer and `close_out_report.py` follow the ledger's directory; **all old proofs: histogram unchanged** | the trimmer's tests and mutants; clones | clones; not a trim at an adopter's history |
| **P4** | DONE (§7.2c): `context_budget.py` and the checkers resolve either place | their suites, both fixtures | fixtures; not an adopter's `files[]` |
| **P5** | DONE (§7.2d): the dashboard scores a new-layout fixture as the legacy one; **`--sync` writes no root copy into a migrated project (C15)** | `tools/test_methodology_dashboard.py`; the old and new dashboards over the real repos | fixtures and the repos here |
| **P6** | DONE (§7.2e): the manifest's second table, read as data (C16); `bin/sync --layout auto` never puts a second copy beside the first (**C1**); the scanner is the gate at **zero** | `tools/test_sync_layouts.py`; the old and new tools over the real adopters; the §5A.3 scratch portfolio | clones. Cannot show a sync from GitHub against a real remote (S218's route) |

### 7.2a P2 — what was built (S275)

**DONE.** The ledger hook and `quality_ratchet.py` 1.2.0 read the ledger and the manifest at either place (from the index, HEAD and history); the never-edit check crosses a move; a trim's shard may sit in either archive directory. **X2 is permanent** (`bin/tests.sh` Test 54, real hook, real git, both layouts): 11 of its 15 assertions were red against the old hook, which failed open four ways. 44 mutants. **Not shown:** a hook armed in another clone.

### 7.2b P3 — what was built (S276)

**DONE.** `methodology_trim.py` 1.8.0 takes its shard directory and link prefix from the ledger's own directory, and `close_out_report.py` 1.2.0 finds its ledger the same way; a half-migrated tree is refused. **Measured:** 119 of 119 shards give the same `--reverify` verdict under both tools; a real ledger, moved in a scratch clone, trims and proves. 44 mutants. **Left:** a root ledger's links are dead after the move (C6). **Not shown:** a trim at a real adopter.

### 7.2c P4 — what was built (S277)

**DONE. The tie rule is unconditional** (his S276 decision): a file at the root AND under `methodology/` is the framework's under `methodology/` when the runner is tracked there and not at the root; the root copy is the project's own; any other tie is `half`. `quality_ratchet.py` 1.3.0, `context_budget.py` 1.4.0, `check-ledger`, `check-handoff`, `check-overhead` and `model-report` resolve either place; `files[]` stay project-root-relative (P7 rewrites them). 43 mutants. **Lesson:** derive a root from git, never a directory name. **Not shown:** another clone's hook.

### 7.2d P5 — what was built (S278)

**DONE** (`DASHBOARD_VERSION` 2.22.0, both copies). The checklist, adoption and role probes, file walk, ledger locator, trim and read-cap rows, generated proofs and quality-gate read follow the layout; a half-migrated tree is a HIGH risk; `--sync` resolves each target (never a second copy at a migrated root). 41 tests. **For him:** a project with no `docs/` of its own loses the 4-point `has_docs_dir` credit when it migrates (pinned). **Not shown:** an adopter's CI.

### 7.2e P6 — what was built (S279)

**DONE.** `bin/_manifest.py` carries `NEW_LAYOUT`, a second literal table read as data (C16); `bin/sync --layout auto` keeps a project's layout and refuses a second copy beside the first, a half-migrated tree and a legacy project asked for the new layout (C1); ignore mode follows the layout (C2); `bin/status` prints `layout:`, `bin/check-links --layout legacy|new|both` simulates either tree (C3). Scanner 4 to **0**, now a gate. 81 tests, 55 mutants; 12 of 12 adopters read and sync as before. **Not shown:** a real remote.

### 7.3a P7 — what was built (S280)

**DONE.** `bin/migrate-layout` (canonical-only; a dry run unless `--apply`) refuses a tree that is not clean, current and unmigrated, naming every reason. Its apply is ONE commit through the project's hooks (every tracked move a rename at 90% or better, rolled back on failure, checked before and after; exit 4 if a check differs). **Measured:** 78 mutants; the 12 adopters in `--no-local` clones (`p7-adopter-runs/summary.md`): **11 migrate**, **`claude_work` is refused** (a seed-only ledger falls to 68%), `wsfct`'s untracked pre-commit hook rolls the commit back. **Corrects §3 C7:** equal proof exit codes held for this repository's proofs, not every adopter's. **Not shown:** an adopter's CI or tests (§7.4a).

### 7.3 P7-P8 — the tool, then the rehearsal

- **P7 DONE (§7.3a).** **Surface:** clones; **not** an adopter's own CI or tests (P11-P22, in the real repository).
- **P8 DONE (§7.3b; a rehearsal, ships nothing).** **Surface:** a clone. It **cannot** show the next session's Phase 0 in the new layout; if D8 allows the real move, that move is a single-commit phase of its own with that Phase 0 as its outstanding check.

### 7.3b P8 — what was measured (S281)

**DONE** (§11; two `--no-local` clones). **The §3.1 criterion FAILS for this repository's own move:** unmoved **482 / 0 / 0**, moved **445 / 11 / 4**, gates 18/18 against **16/18**; the failures are canonical-only tests reading root ledgers by path. **Also:** the tool refuses this repository (`[not-current]`); the dashboard reads the moved changelog as absent (76 to 74); the §5A.4 re-run gives 4 modify/delete conflicts. **Held:** 126 tracked proofs (121 / 5 in both trees), both ledgers trim and prove in `methodology/archive/`, X2 is refused. **Not shown:** Phase 0 in the new layout. B2's blockers are BL-104.

### 7.3c P9 — what was done (S282)

**DONE.** `bin/check-links --layout both` went from exit 1 (36 of 116 links dangling in the new layout) to exit 0 (80 links in 23 files); Test 10 holds it. The 36 that no relative path could serve in both layouts became bare names in code spans. The runner, `BOOTSTRAP.md` §Two layouts (C14's sentence) and the README now name both layouts. **Left (closed S284):** the `bin/migrate-layout` links check. **Not shown:** an adopter reading the new text.

### 7.3d P10 — the sha (S283)

**DONE** (a record; nothing sent). **Adopters may sync from `add55f1`**, the last commit to change a distributed file or anything under `bin/`, `tools/`, `starter-kit/`, `.githooks/`. **Measured on 12 adopters in clones:** the stage changes no path, layout, health or `check-links` exit of one that only syncs (19 to 21 content files). **D8 does not gate P11**; a pull request is a port (34 of 81 commits replay). **Not shown:** an adopter's CI. Detail: `methodology-subdirectory-evidence/p10-expand-release-record.md`.

### 7.4 P11-P22 — an adopter per session (the BL-57 P6-P11 pattern)

Done **in that repository** and recorded here. Order, by risk: `model_project_constructor` (P11, §7.4a),
`feedback-loop-comparison` (P12, §7.4b), `nprcgenekeepr` (the four-workflow CI
filter and its R test), `mts-system`, `vscode_quarto_ext`, `Philippians`, `airqino` (nested copy),
`chat_verification`, `church_growth`, `dalia_martinez_funeral`, `claude_work` (no history to move),
`wsfct` **last and only on a clean default branch** (its branch is active).

- **DONE per adopter:** a clean tree; `bin/status` before; **`bin/sync` first if any TRACKED file is not
  `current`, as its own commit (§5A.2)**; `bin/migrate-layout` dry run read; the apply as one commit;
  `bin/status` after (all `current`, at the new destinations); the adopter's **own** proofs, test suite and CI
  green (named in its receipt), rehearsed at each tier in clones first, a rise in skips a failure; **tier 1 until it is surveyed (his, S285);** one full Phase 0 in the new layout; the sha of the checkout it synced
  from; the project's push is **its own go-ahead**.
- **Surface:** the adopter's repository and CI. **Cannot enforce:** another clone's hook arming; say so.

### 7.4a P11 — `model_project_constructor` (S285)

**DONE at tier 1** (record: `methodology-subdirectory-evidence/p11-model-project-constructor-record.md`). `--tier all` passed every check the tool runs and broke the adopter's own CI (2 of 13 proofs, 41 tests name the moved ledger), so by his choice it was reset and `--tier 1` applied: one test constant repaired, CI back to 3,942 passed, 9 skipped, 5 of 5 jobs green after the push. **Confirms §4.6:** tier 1 alone is coherent; `all` is not safe on the tool's checks alone (its `proofs` cell runs only moved shards' proofs).

### 7.4b P12 — `feedback-loop-comparison` (S287)

**DONE at tier all** (record: `methodology-subdirectory-evidence/p12-feedback-loop-comparison-record.md`). A Quarto paper with no remote, tests or CI; its build is `quarto render`. Synced with `--force` (two older canonical copies, nothing of its own overwritten), then moved: 30 renames; the HTML and PDF text of a fresh clone identical to before; health 59, risk 0 before and after. **The cost of tier 2:** 23 relative links in its own `SESSION_NOTES.md` (reported, never edited).

### 7.5 P23 and G-B

P23 flips the default and makes a legacy tree an error; it is a major release and **needs its own
go-ahead**. G-B is §5's decision and, if taken, its own plan.

---

## 8. Verification, summarised

| Check | Why it can fail the way production fails |
|---|---|
| Suite counts: failed 0; passed and skipped equal to the unmoved tree's in the same receipt state (**skipped 0 at three receipts, 6 at two**), re-measured at each phase's start | A move turns tests into silent skips (§3.1) |
| A later content commit with **no ledger entry is refused** in the new layout (X2) | C5: otherwise the ledger gate fails open, silently |
| A scratch portfolio of a legacy, a migrated and an empty project: `bin/sync` and the dashboard `--sync` write exactly the expected files | C1, C15 |
| The resync simulation (§5A.4) re-run against the then-current `upstream/main` before any real move of this repo's files | C17 |
| The literal scanner at zero | A literal is the one thing a green suite does not see |
| Every tracked proof: exit histogram unchanged (the 5 exit-1 proofs pre-exist) | They are the record that every past trim was lossless |
| `git diff -M` similarity ≥ 90% on every moved file | A move that rewrites a ledger defeats `--follow` and the never-edit gate |
| A move commit that lowers a threshold is refused (mutant) | C4's hidden loosening |
| `bin/sync` over a legacy tree under the new layout writes nothing | C1's blank seed |
| The following session's Phase 0 passes unmodified | The only fully faithful check of a layout change |

## 9. Decisions

**Ratified 2026-10-06 (S273 close-out picker): every recommendation below stands as the decision.** D1 (a) all, tier 1
first; D6 rehearse only; D8 fork first, then one pull request, each outward step his go-ahead at the time; D2, D3,
D4, D5, D7 and D9 as written.

| # | Decision | Options | Recommendation |
|---|---|---|---|
| **D1** | Is "all the methodology files" the framework's files, or also the ledgers and configs a project owns? | (a) all, in two tiers, tier 1 first; (b) the framework's files only | **(a)**: it is the literal request, tier 1 is a complete stopping point, tier 2 is where the risk lives (§4.6) |
| **D2** | Shape | (a) flat `methodology/` with `workstreams/` the only subdirectory; (b) fully flat; (c) categories (`docs/`, `tools/`, `state/`) | **(a)**: (b) puts ~35 names in one directory; (c) is two levels, against the request |
| **D3** | Names | (a) every filename kept, dotfiles included; (b) unhide the two JSON files | **(a)**: renames break the ratchet's history by path and add an axis to every adopter; revisit at contract |
| **D4** | Hooks and attributes | `.githooks/` and `CLAUDE.md` at the root; `.gitattributes` nested | as stated: §4.2 |
| **D5** | The ledger archive | (a) moves to `methodology/archive/` with the ledgers; (b) stays in `docs/archive/` | **(a), last**: proofs are unaffected either way (measured); it keeps `docs/` the project's own. Separable: it can ship a release later |
| **D6** | This repository | B0 / B2 / B1 mirror | **B0 for the real files until D8; B2 as a rehearsal (P8); B1 only through G-B** (§5, §5A.4) |
| **D7** | Versions and sync order | expand minor, contract major; both layouts supported until every portfolio adopter has migrated; `bin/sync --layout auto` through the window; sync before migrate | as stated (§4.5, §5A.2); the number of the release is a later decision |
| **D8** | Upstream | fork-side work and adopters first; then **one** vetted pull request carrying the expand stage and the evidence; or none | **as stated.** It is also what makes this repository's own layout sustainable (§5A.4): without it the fork carries the resolver edits over every maintainer change. Every outward action is his go-ahead each time; no part of this plan sends anything |
| **D9** | Adopter order and batching | §7.4's order, one per session | **as stated** |

## 10. Risks, stop conditions, rollback

- **Stop** if P1's scanner finds a literal the resolver cannot express (a tool that reads a methodology
  file by a path its own caller supplies), or P2's mutants cannot make a loosening-in-a-move refused.
- **Stop** if P2 cannot make the hook refuse a ledger-less commit in the new layout, or P6's
  scratch-portfolio sync writes anything outside the expected set.
- **Stop** if P7's clone run shows any adopter whose ledger loses its rename (similarity < 90%).
- **Rollback:** every stage but the contract is additive; an adopter's migration is one commit and one
  `git revert`; the expand release changes no adopter that does not run the tool.
- **Not established here:** how many *external* adopters exist and what layout they keep (the survey
  covers the 12 sibling projects); whether the maintainer will adopt the layout (D8) and so how often
  the fork's resolver edits will conflict with his; Claude Code behaviour beyond "`CLAUDE.md` is read from the project
  root", which this plan relies on and did not re-test; the real cost of P5, since the dashboard is
  4,900 lines, of which the 79 sites naming a root path (S274's scanner) are only the visible part.

## 11. Evidence, and how to re-run it

All in [`methodology-subdirectory-evidence/`](methodology-subdirectory-evidence/); recorded outputs sit
beside the scripts. Counts are of tracked files at `c8b9ddd`.

| File | Re-run | Shows |
|---|---|---|
| `inventory.py`, `inventory-output.txt` | `python3 -I docs/planning/methodology-subdirectory-evidence/inventory.py` | §2.4: 31 / 23 / 3 / 420 |
| `link-simulation.py` | `python3 -I .../link-simulation.py` | §2.4: 118 links, 40 change |
| `adopter-survey.sh` | `bash .../adopter-survey.sh` | §2.2 |
| `git-behaviour.sh` | `bash .../git-behaviour.sh` | E1 and E2 (§4.2, §4.8) |
| `hook-after-move.sh` | `bash .../hook-after-move.sh` | C5 at `c8b9ddd`: control refused, move commit passes, **later commit passes**; at P2 (`hook-after-move-after-p2-output.txt`) the later commit is **refused** |
| `resync-after-move.sh` | `bash .../resync-after-move.sh` | §5A.4: rename pairing and the two merge-trees |
| `frozen-proofs.sh` | `bash .../frozen-proofs.sh` (minutes) | §3 C7: 117 proofs, 3 trees |
| `p8-rehearsal.sh`, `p8-apply-tool.py`, `p8-rehearsal-output.txt` | `bash .../p8-rehearsal.sh` (about 70 minutes) | §7.3b: the criterion, the proofs, the trim, X2, the resync |
| `suite-blast-radius.txt` | `bash bin/tests.sh` in a `--no-local` clone with the files moved (the outputs are the recorded ones) | §3.1 |
| `adopter-survey-output.txt`, `*-output.txt` | the recorded outputs of the scripts above | §2.2 and the rest |
| `layout-literals-output.txt` | `python3 -B bin/check-layout-literals` (the scanner is the script) | §7.1: the RED list at P1, 177 sites in 12 files, exit 1 |

Greps behind the other claims: `git grep -n 'CHANGELOG.md' .githooks/pre-commit`;
`git grep -n 'ARCHIVE_DIR\|REBASE_PREFIX' starter-kit/methodology_trim.py`;
`git grep -n 'SESSION_RUNNER.md' tools/methodology_dashboard.py`; `sed -n '/^DISTRIBUTION/,/^]/p' bin/_manifest.py`;
`git log --since=2026-09-01 --no-merges --format=%an upstream/main -- <the code and config files of §2.4>
| sort | uniq -c` (§5A.4: 24 by the maintainer and 32 by this fork since 2026-09-01); `git log --no-merges --format=%an upstream/main -- CHANGELOG.md
HANDOFFS.md | sort | uniq -c` (142 and 92).
