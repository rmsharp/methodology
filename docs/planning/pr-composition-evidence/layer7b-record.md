# PR2, Part 2, the last layer: `bin/migrate-layout` and its suite, built and verified

**Status: BUILT, local, un-pushed, nothing sent.** Session S322, 2026-10-15. The tenth and last Part 2 layer (`../upstream-pr-composition-plan.md` §3 and §5; the
prose layer's record, [`layer6c-record.md`](layer6c-record.md) §5, named it). The local ref `pr2/candidate` moved **`18cda0f` to `ab35e96`**, two commits on it
(`2942e46`, `ab35e96`), built in a scratch clone, verified in a clean `--no-local` clone, fetched back with the `+` refspec and read back equal (`git rev-parse` of the ref,
the scratch clone's HEAD and the verified commit: one sha). The candidate is now **19 commits, 46 files, +19,854 / -1,145 against `upstream/main` (`f34769f`)**
(`layer7b-measure-output.txt` §8). Every figure below is printed by a script in this directory or a command named beside it; the saved outputs are `layer7b-*`.

## 1. The answer first

1. **Two commits, three files each, six files, +4,483 / -2** (`layer7b-measure-output.txt` §1). Commit 1 `2942e46`, the tool: `bin/migrate-layout` (new, mode 755, 1,458 lines),
   `tools/test_layout_resolver.py` (`COPIES` gains the tool: +2 / -1), `tools/test_sync_layouts.py` (the one assertion layer 6 had to leave out, that the tool is a file: +1).
   Commit 2 `ab35e96`, the suite: `tools/test_migrate_layout.py` (new, 2,993 lines), `bin/tests.sh` (+11: a block that runs only the suite's two fast classes), `.quality-gates.json`
   (+18 / -1: two gates, and `tests-sh-passed` 301 to 302). **Three files are the fork tip's bytes whole** (`bin/migrate-layout` `06afa06b2`, `tools/test_migrate_layout.py`
   `da7177abe`, `tools/test_sync_layouts.py` `34712638e`: blob ids equal at `91fdf8c`, §1 of the measure output); the other three differ by the layer's own hunks only.
2. **Green at each boundary** (gate (c)): the shell suite on commit 1 alone **301 passed, 0 failed, 0 skipped** (305 s, load 6.7: `layer7b-commit1-suite-output.txt`); on the suite stage
   **302 / 0 / 0** (341 s) and the whole migration suite **280 tests OK in 364.5 s** (`layer7b-suite-output.txt`; its load average read **85** at launch from another project's tests);
   the layer's last commit in a clean clone: **`quality_ratchet.py --run` 18/18 pass, 0 fail, 0 unmeasured, results `23481eb88ba1`, manifest `66cce597ef4a`**, the scanner
   **15 files, 0 sites** (14 on the parent), the one shipped `.verify.sh` exit 0 (`layer7b-verify-output.txt`, about 14.5 minutes at load 15 to 24). The layout suite reads 76 on both
   (`layout-unit-tests` stays 76); `bin/check-links --layout both` reads OK in both layouts on both (80 links, 23 documents).
3. **The suite's colour had no gate, so the layer carries two** over one command string (BL-109's shape, the draft's): `migrate-layout-unit-tests` (min 280, the count) and
   `migrate-layout-unit-tests-failed` (max 0, no `extract`: the exit code), both `timeout_seconds` 3600. **Shown on the real gates** (`layer7b-mutate-output.txt`, G1): with the tool's exit
   code changed so command-level tests fail, `run_gates()` reads the count gate **280, pass**, the failed gate **1.0, fail**, and the suite ran **once** for five gates (a counter line at import).
4. **The tool run as a command** in a project the layer's own `bin/sync` wrote (`layer7b-measure-output.txt` §4): the dry run exits 0 and writes nothing; an apply on a dirty tree exits 1, refused;
   an apply over the seed's few-line ledger exits 3, **rolled back** (HEAD unchanged, 0 dirty paths, the tool's own 90%-similarity rule); with an 80-entry ledger it exits 0, one commit,
   **30 of 30 paths renamed, lowest similarity 96%**, `bin/status` reads `layout: new`, and a second run exits 0 with nothing to do.
5. **The 12 real adopters, the candidate's tree against the fork tip's** (`migrate-12-adopters.py` from a clean clone of each, the same twelve committed HEADs in `--no-local` clones,
   223 s and 270 s; `layer7b-adopters-output.md` §3): **24 of the 27 columns are equal in all twelve** (the apply's status and exit, the checks, history, proofs, moves, links, similarity, rewrites, clean tree, health).
   The three that differ are all before the migration: `sync` (9 of 12), and `status_before_sync` and `ratchet_before` (`vscode_quarto_ext`, the same cause). Section 3 says what that is.
6. **The prose layer's open claim is answered:** its three added lines that name the tool, and the two flags they use (`--apply`, `--tier`), were "read against the tip's tool, not run"
   (`layer6c-record.md` §4). Both flags now exist in the candidate's own tool, and the commands run as written in item 4 (`layer7b-measure-output.txt` §5).
7. **Against the two open pull requests:** #94 conflicts in the same 3 files and 15 regions as the parent did (`.quality-gates.json` 1, `starter-kit/methodology_trim.py` 9, `tools/test_methodology_trim.py` 5);
   #92 merges clean, at the parent and at the layer (§6). Derived, not resolved.

## 2. Mutants (`layer7b-mutate.py`, `layer7b-mutate-output.txt`)

The tool and its suite are the fork's bytes, which the fork mutated in its own evidence (`methodology-subdirectory-evidence/p7-mutants.py`, `f10-mutation-round-1.txt`), so none of the tool's logic is re-mutated here. The layer's own lines
are three hunks, and each mutant prints the one line it changed so a mutant that lands in a comment is visible:

| | Mutant | Result |
|---|---|---|
| L1 | the layout suite's `COPIES` loses the tool | killed (layout suite fails, 1 failure) |
| L2 | one line of the resolver block inside the tool changed (`return "half", None, found` to `()`) | killed |
| L3 | the tool is not a file | killed, by the assertion the sync suite regained (4 tests, 1 failure) |
| L4 | the wiring block names a class that does not exist (the command alone) | killed (1 error) |
| W1 | the same wiring mutant through the **whole shell suite** | killed: `FAIL: migration tool ... failed`, **301 passed, 1 failed**, exit 1 (330 s) |
| G1 | the real two gates over a command-level red suite | count gate pass at 280, failed gate **fail at 1.0**, one suite run |
| V2 | G1's variant: the failed gate's threshold 5 (a loosening) | **reads pass over the red suite**: the mutant the gate must not become; `quality_ratchet.py --precommit` refuses a loosening, this one is not run here |
| V3 | G1's variant: the failed gate without its `timeout_seconds` | **survives**: reads fail like the real gate; nothing but a loaded machine reads a timeout |
| V1 | G1's variant: the failed gate with an `extract` | reads fail **for the wrong reason** (its extract measures the count, 280 > 0): **my expectation was wrong** (I wrote it would pass); the hole is a `min` count gate, which the first gate already shows. The script's docstring says so |

Round 2, behaviours no test names: V3 survives, and the gates' `why` text and the wiring comment's numbers (365 s, 95 tests, "about a second": measured 0.52 s) are read by no test. The wiring comment first said 329 s, the probe's figure at load 3.6;
this build's own run took 364.5 s, so the stage was rebuilt with 365 (a comment line; the saved suite output ran on the first form: its heading says so).

## 3. What the real adopters show, and one thing they do not (PR3's input, not this layer's defect)

- **The migration is the same in both trees.** In all twelve, `apply_status`, `apply_exit`, `checks`, `history`, `proofs`, `moves`, `links` and `min_similarity` are equal between the candidate's run and the fork's. Five apply, five have nothing to do, one rolls back (`claude_work`, exit 3), one rolls back
  on its own hook and applies with hooks off (`wsfct`): the same as the fork's run (`layer7b-adopters-output.md` §1 and §2). The checks that matter for this layer are the tool's before-and-after comparison of `bin/check-ledger` and `bin/check-handoff`, which are the candidate's own (upstream's blob plus the layout hunks): **they agree with themselves across the move in every adopter that applied.**
- **The candidate's `bin/sync` refuses 9 of the 12 without `--force`, where the fork's refuses none of those.** The two `bin/sync` files are the same bytes (`df1b7ea6c`); what differs is the history and the documents they compare against. `model_project_constructor` is the example kept
  (`layer7b-adopters-output.md` §4): its `SESSION_RUNNER.md`, `CLAUDE_TEMPLATE.md`, `BOOTSTRAP.md` and `HOW_TO_USE.md` are "local modifications that don't match any canonical or historical version" of the candidate. Each of the four is an EARLIER version of the fork's own file (the blob is in the fork's history, not at its tip, and in no commit of the candidate's), so the fork's `bin/sync` reads it as merely behind and the candidate's cannot. That is what an adopter that took the fork's files will meet the first time it syncs from the merged tree, and it is plan §5's PR3 row ("files written, files refused") to measure and the pull request's text to say. **Not measured here:** that every one of the 9 is this cause; the four files of one adopter were checked against both histories.
- **A seed-size ledger blocks an apply** (item 4): the tool says "migrate after it has more entries" (`bin/migrate-layout:1283`). A first-time reader of the prose who migrates a freshly bootstrapped project meets exit 3, rolled back, with the tree untouched.

## 4. Decisions I took that the plan did not

1. **No edit to the tool or its suites.** Three files are the tip's bytes whole, so what the fork tested over twelve adopters is what the candidate ships. One thing the tool says that its code does not: **its docstring's exit list stops at 3 (`bin/migrate-layout:26`) and `main` returns 4 when the checks differ (`:1311`)**; the commit message for the tool says exit 4, from the code. A correction is the scrub's or the fork's, not this layer's.
2. **The paired gate** is a divergence from the tip (which has one gate over the same command, the hole BL-109 describes). It tightens, loosens nothing and is in the candidate only; the fork's gate is unchanged and BL-109 stays open.
3. **`--slow-seconds 365`**, this build's own measurement, over the probe's 329: the number a gate has to survive, in a comment that says what it is.
4. **The adopters' script was run with `--out` and `--work` in a scratch directory.** Its default `--out` is the committed output of its first run (`p7-adopter-runs/`), which a run from the fork's tree would have overwritten.
5. **My measurement script's first §4 was wrong, twice, and the tool was right both times:** a project with no first commit (the tool refused, "no commits yet": exit 1) and then a seed ledger (rolled back, exit 3, the rule above). Both are now in the saved output as what they are; the run before them was not kept.

## 5. What this does not show

The surface is this machine: clean clones, serial runs, `nohup` and done-files, load average 8 to 85 over the session (another project's tests, the highest reading at the migration suite's launch). **Not shown:**
- a maintainer's machine, Windows, upstream CI (there is none), hooks armed in another clone other than the adopters' own (the adopters script arms the real clone's hooks path; `wsfct`'s hook did refuse);
- that all 9 `--force` syncs are the one cause (§3); an adopter's own CI;
- the candidate merged with #94 (derived, the same 15 regions, not resolved);
- the tool's logic under new mutants (the fork's rounds stand for the same bytes).

**Scrub input** (`layer7b-measure-output.txt` §7, a coarse regular expression over the added lines): `bin/migrate-layout` 1,458 lines: 19 with a backlog code, 3 a phase, 2 a session number, 14 a plan reference, 1 a `docs/planning/` path;
`tools/test_migrate_layout.py` 2,993 lines: 13, 7, 8, 19 and 1, one a learning number; the two commit messages 0. The tool's own first docstring line names "BL-101, phase P7". The scrub is its own commit after D6's.

## 6. Next

1. **D6's small commit** (plan §7, answered (a)): the 3 unmeasured-gate hunks (+7 / -4: the runner's 3E sentence, `starter-kit/HANDOFFS.md`'s paragraph, `HOW_TO_USE.md`'s 3E bullet) as one commit on `pr2/candidate`, the pull request's text saying the lint that enforces the clause stays on the fork (`layer6c-record.md` §3 names the 8 not-layout hunks and where they sit).
2. **Then the scrub** (its own commit, so a reviewer can skip it), **then PR3** (adopter impact, with §3's 9 refusals as its first row).
3. Re-run: rebuild `python3 layer7b-build.py <fork> 91fdf8c <clone-at-18cda0f> --stage tool`, commit, `--stage suite --slow-seconds 365`, `--stage suite --migrate-count 280 --passed 302 --layout-count 76`, commit; verify `bash layer-verify.sh <candidate> ab35e96 <dst>`;
   measure `bash layer7b-measure.sh <fork> ab35e96... 18cda0f 91fdf8c <scratch>`; mutate `python3 layer7b-mutate.py <candidate> ab35e96 <work> --fast --e2e-wiring --e2e-gates`; adopters: copy `migrate-12-adopters.py` into a clean clone of each tree and run it with `--out` and `--work`, then `layer7b-adopters-compare.py <rows A> <rows B>`.
