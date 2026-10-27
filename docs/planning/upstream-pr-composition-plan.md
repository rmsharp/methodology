# The one upstream pull request: what it carries, what stands in front of it, how to build it

**Status: DECIDED (2026-10-13, his picker: D1 to D4, each as recommended, §7). Refreshed 2026-10-26 (S375) for upstream's move: #92 and #94 merged on 2026-10-24, and the candidate now conflicts with `upstream/main` (§2.2).** Nothing is sent; the fork was pushed to
its own `origin` only. **The candidate (`pr2/candidate`, 34 commits over `f34769f`), PR3 and PR4's approved text (draft 11, S338) are done, and D1 and D4 are answered (§7). PR5 is next, but the candidate is 28 commits behind `upstream/main` and is rebuilt first (§5, PR2b).** Each commit's hash is in its record in [`pr-composition-evidence/`](pr-composition-evidence/) (`part1`, `layer1` to `layer7b`, `d6`, `scrub`, `bl113`, `pr3`, `pr4`, `fix32`, `restore33`, `bl119`). D3 overrides the dashboard hold ratified on 2026-09-27 (`dashboard-upstream-routing-plan.md`, which
carries a pointer back here).
§0, §1, §2.1, §2.3 and §2.4 were measured at fork `ffb0fd1` against `upstream/main` = `f34769f` and **have not been re-run**; §2.2 was re-measured at `d50ce290` (S375). Every figure below is printed by a
script in [`pr-composition-evidence/`](pr-composition-evidence/) (§9) or by a command named beside it.
**Declared budget: 30,000 B**, one read.

**Governing text.** [`CLAUDE.md`](../../CLAUDE.md) §Contributing upstream: one substantial, fully vetted pull request, the
vetting done on this side, every outward step his go-ahead each time. [`methodology-subdirectory-plan.md`](methodology-subdirectory-plan.md)
§9 **D8**: *fork-side work and adopters first; then one vetted pull request carrying the expand stage, the evidence and the
findings register*, and §7.6: the pull request *waits while a finding the tool's checks did not see is open, unless he waives it
and the ledger says so*.

---

## 0. The answer first

1. **Nothing is ready to send, and the work is bigger than D8 pictured.** D8 names "the expand stage" (the `methodology/`
   directory work). The fork's tree differs from `upstream/main` by **56 files, +25,804 / −1,409 lines** outside `docs/` and the
   ledgers, and **about half of that (24 files, +13,254) predates that plan and was never sent**: the dashboard 2.11.3 to 2.22.0, the
   trimmer 1.5.0 to 1.8.0 (it includes the work of open #94), the ratchet 1.1.0 to 1.5.0, three tools upstream does not have
   (`bin/model-report`, `bin/check-overhead`, `starter-kit/close_out_report.py`) and 2,982 lines of shell tests. **20 files carry both
   halves**, the second built on the first (§1).
2. **The cheap route is whole files, not hunks.** Porting only the `methodology/` hunks onto upstream's copies is **52 hand-resolved
   conflict regions in 16 files** (`git merge-file`, base `c8b9ddd`; §9). So a
   pull request carries the earlier work too, and it must say so.
3. **The suite is not portable yet, and the cause is the tests, not the tools.** Upstream's tree with the fork's shipped files laid
   over it runs `bin/tests.sh` to **484 passed, 14 failed, 2 skipped** (upstream's own suite: 261/0/0; the fork's: 503/0/0). All 14
   failures (one per failing check) sit in 9 of 54 test blocks, and every one reads this repository's own ledgers, backlog, archive or
   `docs/FORK_LEARNINGS.md` as a fixture, or applies a stricter checker to upstream's live ledger. **No shipped tool misbehaved:** the
   trimmer, context-budget, ratchet, layout, sync and `migrate-layout` unit suites all passed (§2.3).
4. **D8's two gates are open.** Five of twelve adopters are not migrated (`mts-system`, `Philippians`, `dalia_martinez_funeral`,
   `claude_work`, `wsfct`); 13 of the register's 31 rows are open, and on a first-pass reading 7 of those are findings the tool's own
   checks did not see (§2.1). Neither gate is a reason not to *build*: building sends nothing (§7 D1).
5. **The two pull requests that were in front of it have merged, and upstream moved under the candidate.** #92 and #94 merged on 2026-10-24. `upstream/main`
   is now `d50ce290`, 28 commits past `f34769f`, its trimmer at 1.8.2 (the maintainer's review of #94). The candidate (1.8.1) conflicts with it
   in 4 files, **46 regions**, 43 in the trimmer and its tests. #98 (open) edits the same four files; #96 shares four with the candidate (§2.2).
6. **The added code carries about 700 fork-internal token hits** (lines with a backlog code 282, a session number 199, a
   `docs/planning/` path 63, a fork-learning citation 25, a plan-phase code 130; a line can carry two; upstream's copies already carry 67
   and 51 of the first two). **14 plan documents the added lines cite do not exist upstream** (§2.4).
7. **The maintainer's record says size is not the obstacle; waiting is, and he splits what is separable.** He merged #80 (+7,892 / −580, 28 files) five days after it
   opened and #84 (+1,264 / −303, 21 files) after 13, with 0 reviews and 3 and 1 comments (`gh pr list`, `gh pr view`); #83 to #88,
   opened 16 to 27 September, all merged on 1 October. #92 (+32 / −1) and #94 (+2,806 / −30, 5 files) waited 16 and 14 days for his first reply (2026-10-19, changes
   requested on both) and merged on 2026-10-24, five days after the fork answered. On #94 he asked that one separable piece, the trimmer's `SESSION_NOTES.md`
   ledger-table entry, go in its own pull request; it did, as #98. He merges locally, because GitHub's button ignores `merge=union` (his comment on #94).
   Upstream has no CI (`.github/` is absent), so every check is local.
8. **Recommendation:** one pull request, built as a **two-part series of commits** (the earlier lineage, then the `methodology/`
   layers), carrying the **shipped set and its tests** and leaving the fork's own reporting tools and instance tests for later
   (§3). **Build the candidate now, fork-side; decide the D8 waiver at the final approval, with the then-open rows listed** (§7).

---

## 1. What the fork carries that upstream lacks

By tree difference, not by commit count: upstream squash-merged earlier pull requests, so `git rev-list --count upstream/main..HEAD`
reads about 1,860 and is inflated by content upstream already holds. `docs/` (about 800 paths, nearly all added planning and archive
files) is fork-only and never part of a pull request. Files a theme shares (the runner, the shell suite) are counted once. The dashboard
twin (`starter-kit/` and `tools/`) is counted twice, as two files.

| Theme | Files | Lines | New files | What adopters get |
|---|---:|---:|---:|---|
| **A** the `methodology/` directory: resolver, `bin/migrate-layout`, the sync layers, the hook, the prose | 31 | +8,076 / −248 | 8 | the update route (`bin/sync`, `bin/status`, `bin/migrate-layout`), `context_budget.py` and the prose of 14 distributed files |
| **B** quality ratchet 1.1.0 to 1.5.0, and the `HANDOFFS.md` seed that cites its run | 4 | +1,282 / −64 | 0 | `quality_ratchet.py`, two seeds |
| **C** ledger trimmer 1.5.0 to 1.8.0 | 5 | +2,747 / −106 | 2 | `methodology_trim.py` |
| **D** dashboard 2.11.3 to 2.22.0 (and twin) | 3 | +7,229 / −687 | 0 | `methodology_dashboard.py` |
| **E** the close-out report generator (new) | 2 | +1,115 / −0 | 2 | nothing: not in `bin/_manifest.py` |
| **F** canonical-only checkers and reports | 4 | +1,588 / −72 | 2 | nothing: canonical-only |
| **S** the shell suite and the runner | 2 | +3,347 / −118 | 0 | the runner |
| **G** this repository's own configuration and prose | 5 | +420 / −114 | 0 | nothing: stays |

**Adopter impact, if everything were sent:** 19 of 23 tracked distributed files differ (the runner, `SAFEGUARDS.md`,
`RECOMMENDED_SKILLS.md`, `CLAUDE_TEMPLATE.md`, `BOOTSTRAP.md`, the four tools, the three manuals, seven workstreams) and 3 of 7
seeds (`CHANGELOG.md`, `HANDOFFS.md`, `quality-gates.json`). `bin/sync --layout auto` keeps a project in the layout it has and gives
an empty one the legacy default, so a legacy adopter's file *locations* do not change; its file *contents* do. Versions not in the table (`inventory-output.txt`): `context_budget.py` 1.3.1 → 1.4.0, `close_out_report.py` absent → 1.2.0.

The fork's own plan for the dashboard (`dashboard-upstream-routing-plan.md`, **ratified Option C, 2026-09-27**) says: send a small
correctness fix first, **hold** the read-cap and trim stack, and keep three policy pieces (the installed-content structure, the
scoped `--sync`, the self-scan root) out of every pull request. **A whole-file overlay of theme D overrides that hold** (§7, D3).

---

## 2. What stands in front of it

### 2.1 D8's two gates

- **Adopters.** P11 to P17 are done (7 adopters: tier 1 at one, tier all at six). Five remain. Four are not free now: `mts-system` has
  a live session (`pgrep -x claude`, `lsof -a -p <pid> -d cwd`); `Philippians` (4 dirty lines), `dalia_martinez_funeral` (6) and
  `claude_work` (16, no history to move) are dirty. `wsfct` is clean and idle but 21 tracked files behind, so `bin/migrate-layout`
  refuses it (`[not-current]`) until a `bin/sync` commit, and it sits on a feature branch (`fix/s710-sermon-list-delete`). The
  migrated `nprcgenekeepr` also has a live session; its BL-105 top-up is refused `not-current` (F7, F19), a separate call of his. `bin/migrate-layout` dry runs read all
  12 in clones.
- **The register** ([`findings-register.md`](methodology-subdirectory-evidence/findings-register.md), `register-open-rows-output.txt`): 31
  rows, 6 with a dated change of disposition, **13 open**: F2, F4, F6, F7, F8, F13, F14, F17, F19, F25 to F28. A plain-text first pass
  of the *Seen* column reads **F6, F8, F17, F27 as not seen** and F25, F26, F28 as probably not seen; F13 and F19 are half-seen. What
  resolves each: F6, F8, F13, F14, F17, F19 are **his triage**; F2 (`wsfct`'s untracked hook), F25 to F28 resolve inside an adopter's own
  commit at P18 or at BL-105 phase 4; F4 and F7 are stated limits. This is a reading, not a ruling: each *Seen* cell is for a person to
  judge, and §7 D1 asks him to.

### 2.2 Upstream since the plan was measured (`conflicts-after-merge.sh`, S375; `conflicts.sh` is the 2026-10-13 record)

#92 and #94 merged on 2026-10-24. `upstream/main` is 28 commits past `f34769f`: the trimmer at 1.8.2 with its 227
unit tests (124 before), `FRAMEWORK_APPARATUS.md`, the v4.2 notes and the ledgers (8 files, +3,019 / −31). Conflict regions from `git merge-tree`, attributes off (GitHub's view; fork `main` reads 47, 53 and 21, in the output file):

| Side | against `upstream/main` | against #98's head | against #96's head |
|---|---|---|---|
| the candidate, `pr2/candidate` `3cba1e5` | **46 in 4 files**: trimmer 25, its tests 18, `FRAMEWORK_APPARATUS.md` 2, `.quality-gates.json` 1 | 52 in 4 | 3 in 2 (`.quality-gates.json` 2, `bin/tests.sh` 1) |

The earlier reading, that the fork's side wins in the trimmer's regions, was made at #94's 1.7.0 head and **no longer holds**: upstream's side carries 1.8.2, the maintainer's review fixes, which the candidate (1.8.1)
lacks, so each region is read, not assumed (§8). #98 (open, 6 files) edits the candidate's four files; #96 (open, theme E) shares `.quality-gates.json`, `bin/tests.sh`, `BOOTSTRAP.md` and `SAFEGUARDS.md`.
So the candidate is rebuilt on `d50ce290` (§5, PR2b); how it stands to #98 is §7 D4.

### 2.3 The suite on upstream's tree (`candidate-probe-suite-output.txt`, `candidate-probe.sh`)

Base `f34769f`, overlay of every changed path under `starter-kit/`, `workstreams/`, `bin/`, `tools/`, `.githooks/` and the three
manuals. 484 passed, 14 failed, 2 skipped. The suite counts one failure per failing *check*; a unit suite is one check. The failing
blocks, by cause (the cause of each was read in the output; PR2 confirms it at the test):

| Cause | Blocks | Failed checks |
|---|---|---|
| **A population or file only this repository has** (≥100 receipts, ≥6 real ledgers, a Class B backlog at `docs/planning/BACKLOG.md`, `docs/FORK_LEARNINGS.md`, archived shards, a front matter larger than 414 B) | 18 (the dashboard suite: 3 of 397 tests; the close-out report suite: 1 of 82), 30, 32, 39, 40 | 9 |
| **A stricter checker meets upstream's own live ledger** (`bin/check-handoff`'s `commit:` slot and `changelog_ref` locator rules flag upstream's receipt S5, `CHANGELOG.md:35`; the compact-norm paragraph is absent from upstream's ledger front matter; the newest-only check no longer reads upstream's ledger as green) | 25, 26, 29, 34 | 5 |

The second row is not a test to parametrise: carrying those lints means **editing the maintainer's own ledgers**, which are his.

### 2.4 Tokens and dangling paths (`fork-tokens-output.txt`)

Added lines in 51 changed files carrying a backlog code 282, session number 199, `docs/planning/` path 63, fork-learning citation 25, plan-phase
code 130. Upstream's copies of the same files carry 67, 51, 20 and 9 today, so a token has precedent; **a dangling path does not**: 14
`docs/planning/` documents the added lines cite are not in `upstream/main` (`methodology-subdirectory-plan.md` from 11 files, `BACKLOG.md`,
the read-cap and overhead plans). The 17 `docs/archive/` names are test fixtures.

### 2.5 The evidence

`methodology-subdirectory-evidence/` is 245 files, 3.2 MB: 20 records (196 KB), 56 scripts (358 KB), the register (46 KB), the rest recorded run outputs. The plan is 60 KB. Upstream's `docs/planning/` holds 6 plan files and no run outputs.

---

## 3. Shapes considered

| | Shape | For | Against |
|---|---|---|---|
| **S1** | One pull request, everything (A to F), +25.8k lines | one review event | needs the 9 blocks fixed **and upstream's ledgers edited**; carries the held dashboard stack and two tools upstream never received |
| **S2** **(recommended)** | **One pull request, a two-part series of commits, carrying A to D and their tests; E, F and the instance tests stay on the fork** | D8's "one"; ordered like #80's series, readable in two sittings; nothing in it needs a ledger of his edited | the earlier lineage rides along (§0.1); the dashboard needs D3 |
| **S3** | A pull request per theme | smallest reviews | **dependent work must not go separately** (`CLAUDE.md`): A embeds a resolver in B, C and D; six queue entries for a reviewer with 0 reviews on most |

**S2's commits.** Part 1 is the earlier lineage at the state the fork's plan began from (`c8b9ddd`: 24 files, +13,254 / −847, a tree the
fork's suite passed at 452/0/0, the plan's baseline in its §3.1). Part 2 is the plan's layers in its own order: the resolver and scanner,
the gate layer (hook and ratchet), the trimmer, the context-budget gate, the dashboard, the sync layers, the layout hunks of the two checkers (D5, amended), the
prose, and `migrate-layout` last (its suite needs the checkers and the prose: `layer7-record.md`), with the later ratchet and companion-file changes where they belong. Each layer is a checkpoint commit with the suite run on it
(`SESSION_RUNNER.md` §Vertical Slice Sessions, gates (b) and (c)), so a reviewer can stop at any layer. Part 1 is built from the fork's
tree at `c8b9ddd`, so it was green on the fork; it is green on upstream's tree (`part1-record.md`).

---

## 4. What the pull request carries

| Carried | Not carried |
|---|---|
| Themes **A, B and C** (§1), with their tests | **E** `close_out_report.py` and its tests (its own test reads this repository's 342 receipts) |
| **D** per decision D3; **the layout hunks of `check-handoff` and `check-ledger` (D5, amended at S319)** | **F** `check-handoff`'s new lints, `check-overhead`, `model-report`, `check-learnings`: canonical-only, and §2.3's second row |
| The portable blocks of `bin/tests.sh` (45 of 54 pass on upstream's tree) | The 9 blocks of §2.3, until each is parametrised or kept on the fork |
| Gate thresholds tightened by exactly what the pull request adds (`.quality-gates.json`, S231's D6) | `CLAUDE.md`, `README.md`, `.context-budget.json` (except one row, `ced2c82`), the ledgers, `docs/` except the next row |
| The findings register, the plan, the 20 records (the *evidence* D8 names), about 300 KB | The 3.2 MB of recorded outputs (named by fork commit instead) |
| A release-notes pull request is **separate**, after the merge, in the manner of #92 | A version number: D7 leaves it to a later decision |

One seam to keep: the runner's 3E sentence and the `HANDOFFS.md` seed's paragraph say a cited run that reads unmeasured gates must name
them. They ship as prose (B); the lint that enforces them is `bin/check-handoff`'s (F) and stays on the fork, so upstream would hold a rule
its own checker does not enforce. PR2 states that in the text or carries the one lint, with the ledger edit it needs. **D6 (§7) settled it: a small commit after `bin/migrate-layout` (`5afc962`); the runner's sentence stays on the fork.**

---

## 5. Phases — one session each unless stated; close out in full; nothing outward before PR5

| Phase | DONE looks like | Verify | Surface, and what it cannot show | Stop |
|---|---|---|---|---|
| **PR1** this plan | committed with its evidence; his four answers (§7) recorded in the ledger | `bash bin/tests.sh`; the evidence scripts re-run to the saved outputs | this machine; not upstream's maintainer's | his approval picker |
| **PR2** build the candidate | a branch in a scratch clone of the then-current `upstream/main` (after #94 if merged; built at `f34769f`, before it did): Part 1, then each Part 2 layer as one commit; the 9 blocks parametrised or left out; tokens and dangling paths scrubbed **in their own commit** so a reviewer can skip it; no push | in a clean `--no-local` clone of each layer's commit: `bash bin/tests.sh` failed 0, passed and skipped stated; `python3 starter-kit/quality_ratchet.py --run` all pass; `bin/check-links --layout both`; `bin/check-layout-literals` 0 sites; every shipped `.verify.sh` exit histogram equal to upstream's; the changed-file list equal to §4 (a script compares) | clean clones, serial runs, `nohup` and a done-file for the long ones. **Cannot show:** Windows, a maintainer's machine, hooks armed in another clone, upstream CI (there is none) | the branch exists locally, green, un-pushed |
| **PR2b** (added S375; next, his picker 2026-10-26) rebuild the candidate on `upstream/main` | a second branch from `d50ce290`, the old one kept: §3's layers re-applied, the trimmer layer being upstream's 1.8.2 plus the fork's layout hunks, each §2.2 region resolved by reading; PR3's table re-run and PR4's text re-checked (§6), their figures being the old base's | per layer, in a clean `--no-local` clone: every check of the PR2 row; and `conflicts-after-merge.sh` reads 0 for the new branch | clean clones, serial runs. **Cannot show:** the maintainer's machine, or #98 merged | the branch exists locally, green, un-pushed; a region that needs a judgment goes to him |
| **PR3** adopter impact | a table per adopter | `bin/status` and `bin/sync --dry-run` from the candidate over all 12 adopters in `--no-local` clones, legacy and migrated: files written, files refused, seeds untouched; a legacy fixture synced by **upstream's** tool and by the candidate's, trees diffed | clones. **Cannot show:** an adopter's own CI | the table committed |
| **PR4** the text and its approval | a body in recognised terms, every number tied to a command in the diff; a fresh reviewer's read of a **frozen** draft; shown inline | `grep` the body for session numbers, backlog codes and coined names; each claim of §6 re-run | the draft only | his approval picker lists the then-open register rows (D1) and the state of #94 and #92 (D4) |
| **PR5** outward | each step read back before the next: push the branch to `origin`; open the pull request; answer comments | `gh pr view`; `ls-remote` | upstream | each step is its own go-ahead; none is implied by the one before |

PR2 is two to four sessions (a layer is a checkpoint, the dashboard the largest). Adopter sessions P18 to P22 run whenever an adopter is
free and are not in this table; each leaves register rows that PR4 reads first (§7.6 of the directory plan).

PR2b is two to three sessions, **a guess**: 43 of its 46 regions are the trimmer and its tests.

---

## 6. What the pull request will claim, and how each claim is re-verified

| Claim | Re-run |
|---|---|
| A legacy project is unchanged in where its files sit | `bin/sync --layout auto` over a legacy fixture, upstream's tool and the candidate's: the same list of paths written; contents differ only in the files §1 names |
| No file an adopter owns is overwritten | PR3's dry runs: seeds read `present (seed; left as-is)` |
| The resolver is one block, byte-identical in every tool that embeds it | the layout suite's equality test, on the candidate |
| Every frozen proof gives the verdict it gave | the exit histogram of all shipped `.verify.sh` before and after |
| Both layouts' links resolve; no path literal is left in a shipped tool | `bin/check-links --layout both`; `bin/check-layout-literals` |
| The gates tighten and none loosens | `quality_ratchet.py --precommit` on the diff of `.quality-gates.json`, then `--run` |
| The counts in the prose (tools, files, failure modes) are true | grep each against the tree |

**What a green fork does not show:** the fork's suite is not upstream's; 503 passed on the fork against 484/14 on upstream's tree is the
measured gap. Only a clean clone of the candidate speaks for the pull request.

---

## 7. Decisions for him

**Answered 2026-10-13 at the S308 close-out picker, each as recommended: D1 (a) build now, D2 (a) S2, D3 (a) the whole lineage, D4 the defaults.
D5 (S317 close-out picker, 2026-10-14) was also as recommended, amended at S319 (below). D1's waiver and D4's wait were answered 2026-10-18 (S339): [record](pr-composition-evidence/d1-d4-record.md). Options below as asked.**

1. **D1 — may the candidate be built before the adopters and the open rows are done?** (a) **Yes: build now, fork-side; the §7.6 waiver is
   decided at PR4 with the then-open rows listed** *(recommended: building sends nothing, four of the five remaining adopters are not free,
   and every session the build waits is one more week in a queue that already holds #92 and #94)*; (b) no: finish P18 to P22 and close every
   unseen row first (strict D8); (c) waive both now, ledger says so.
2. **D2 — shape.** (a) **S2** *(recommended)*; (b) S1; (c) S3.
3. **D3 — the dashboard.** (a) **Send the whole lineage, 2.11.3 to 2.22.0, and accept that it overrides the earlier hold** *(recommended:
   the alternative is a hand port of the layout layer onto 2.11.3, 17 conflicts per copy and its tests to re-derive, and the three policy
   pieces are in the lineage already, so PR4's text names them as policy for the maintainer to refuse; the migrated adopters also already
   run the fork's dashboard: `bin/status` reads `vscode_quarto_ext`'s as `current` against the fork)*; (b) hand-port the layout layer
   onto 2.11.3 and keep the lineage held; (c) ship without the dashboard layer and say that the dashboard still writes at the project
   root in a migrated project.
4. **D4 — defaults I will follow unless you change one:** the **wait** ended on 2026-10-25, on the date alone (his S369 answer, [`d1-d4-record.md`](pr-composition-evidence/d1-d4-record.md) §5),
   and #92 and #94 merged on 2026-10-24, so the stack-or-supersede question about them is moot. **Added S375, his picker 2026-10-26:** the same question applies to #98 (open; it edits the
   trimmer, §2.2): at PR5, if #98 is still open, ask whether to stack on its head or state that this pull request supersedes it (closing it is outward); **scrub** tokens and
   dangling paths in one separate commit; **carry** the register, the plan and the records, not the outputs; **tighten** gates by what is added.
   **The scrub was built at S324 as ten commits, not one** (`pr-composition-evidence/scrub-record.md` §1.2): the population is 654 lines in 28 files, and `SAFEGUARDS.md` (which wins) caps a commit at 5 files. The ten sit together at the tip, so a reviewer still skips them as one run; the first seven change comments and docstrings only, the last three the text a program prints.
5. **D5 — does the pull request carry the layout reading of `bin/check-handoff` (6 scanner sites) and `bin/check-ledger` (4)?** §4 was silent, and the
   scanner cannot read 0 without an answer; it binds at the sync layer, where `layout-literals` is first declared at 0. (a) **Leave both out and scope the
   scanner to the tools adopters receive plus the hook** *(recommended and answered: both checkers are canonical-only, adopters never run them, and it matches D2
   and §4's row F; the cost is that those two files read root paths only on the candidate, and the fork's own move of its instance files, BL-104, needs
   the reading later, on the fork)*; (b) carry only the layout hunks of both files (10 sites), hand-built as upstream's blob plus those hunks; (c) decide at the sync layer.
   **Amended 2026-10-14 (S319, his picker, the recommended option): (b), not (a).** The cost (a) named was not the whole cost. `bin/migrate-layout` runs `check-ledger` and `check-handoff` over the project
   before and after the move and compares their exit codes, so with both left legacy-only the tool reports `CHECKS DIFFER` and exits 4 on every apply: of its 280 tests, 10 fail on the candidate, 9 of them still
   with the prose present, and none with the tip's checkers and documents both in (`pr-composition-evidence/layer7-probe-output.txt`, `layer7-record.md` §1). **The order is now: the checkers' layout hunks
   (hand-built as upstream's blob plus those hunks: the tip's files carry fork-only lints beyond them, +610 / -57 and +72 / -5), then the prose, then `bin/migrate-layout` last.** The checkers' layer also deletes the
   two `NOT_SCANNED_ALWAYS` entries layer 6 added.
6. **D6 — where does the unmeasured-gate prose go?** (**answered (a) at the S321 close-out picker, 2026-10-14**, the recommended option, do not re-ask; `pr-composition-evidence/layer6c-record.md` §5) The runner's 3E sentence, the `HANDOFFS.md` seed's paragraph and `HOW_TO_USE.md`'s 3E bullet say that a cited run reading unmeasured gates must be
   repaired or name them (3 hunks, +7 / -4). The candidate carries the ratchet's 1.5.0, which makes "unmeasured" a real reading, and none of these sentences; the prose layer carries layout only, so they are still on the fork. (a) **A small commit after `bin/migrate-layout`, the pull request's text stating that
   the lint that enforces the clause stays on the fork** *(recommended: §4 already says they ship as prose, and a reader of the ratchet's output meets the word without the rule)*; (b) leave them on the fork; (c) decide with the text, at PR4.
   **Built at S323 (`5afc962`, [`d6-record.md`](pr-composition-evidence/d6-record.md)), as two of the three hunks, by his picker answers of that session:** the runner's 3E sentence **stays on the fork** (the candidate's runner already reads over its read-set ceiling, 21 tokens, since the prose layer's first commit; the sentence adds 224 B; BL-113), and the receipt seed's hunk is carried **without its last changed line** (the fork says the checker lints "that token and clause"; the candidate's `bin/check-handoff` has no clause lint, so upstream's sentence stays). PR2's text states both: the clause lint and the runner's 3E sentence stay on the fork.

---

## 8. Not established

- Whether the maintainer wants the `methodology/` layout at all (D8's own unknown), or the dashboard lineage (the S231 plan's premise).
- Whether 9 blocks can all be parametrised without weakening what they pin; PR2 finds out.
- The exact line count of the carried set: §1 counts the whole difference, §4 removes E, F, G and 9 blocks.
- The 7 adopter runs and the dry runs are on this machine, with the fork's tool as the source; the route an adopter takes alone, from
  GitHub, has not been run against a real remote (the earlier plan's own caveat).
- Rows tagged upstream-facing and not part of this plan: BL-66 (the update route's README line), BL-70 (issue #75's plan-surface rule,
  never sent), BL-84 (the context-budget seed). They are separate decisions and were not re-adjudicated here.
- Which side wins in each of §2.2's 46 regions; PR2b reads them.
- §0, §1, §2.1, §2.3 and §2.4 are as of `f34769f`: theme C is smaller now that upstream carries the trimmer's earlier lineage, and 484 / 14 / 2 and the 52 regions are the old base's. PR2b re-measures.

## 9. Evidence, and how to re-run it

All in [`pr-composition-evidence/`](pr-composition-evidence/); each script reads git only and prints what it measured; its saved output is
beside it. Run from inside the repository, serially.

| Script | Output | Answers |
|---|---|---|
| `inventory.py` | `inventory-output.txt` | §1: the difference, its halves, the themes, adopter impact, versions |
| `register-open-rows.py` | `register-open-rows-output.txt` | §2.1: the open rows, with the register's dated lines applied |
| `conflicts.sh` | `conflicts-output.txt` | the 2026-10-13 record of #94 and #92 against the fork tip (both have merged since) |
| `conflicts-after-merge.sh` | `conflicts-after-merge-output.txt` | §2.2: the candidate and the fork tip against `upstream/main` and the heads of #98 and #96 |
| `candidate-probe.sh` | `candidate-probe-suite-output.txt`, `candidate-probe-unit-failures-output.txt` | §2.3: upstream's tree plus the overlay, the suite (reproduced by the script after a first run by hand: 484 / 14 / 2 both times), and the two unit suites that fail inside it |
| `fork-tokens.py` | `fork-tokens-output.txt` | §2.4: tokens and dangling paths |

The port-cost figure (52 regions, §0.2) and the evidence sizes (§2.5) are one-line commands: `git merge-file -p <upstream's copy>
<c8b9ddd's copy> <HEAD's copy>` per file, exit status the count, and `git ls-files docs/planning/methodology-subdirectory-evidence | wc -l`.
