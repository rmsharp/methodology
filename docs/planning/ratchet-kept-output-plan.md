# Plan: the quality ratchet keeps the output of a gate that did not pass

**Status: DRAFT for the operator's decision (2026-11-13, S445). Nothing is built, no ref moved, nothing sent to `KJ5HST/methodology`.** A planning session's deliverable is the plan; each *piece* in section 6 is a later session. The decisions the operator owes are in section 8. Backlog row: BL-92 (its shape (c)); BL-103's option (c) is a neighbour (section 2, decision D3).

**Origin.** BL-92 (raised S233) listed three shapes for a flaky red inside a gate run; shape (c) is "teach the ratchet to keep a failing gate's output", marked a distributed-tool change and the operator's call (`BACKLOG-DETAIL.md:3982`). `docs/planning/backlog-interaction-review-2026-10-18.md:112` and `:279` pair it with BL-103's option (c), which is a *different* feature, "make `--run` print the unmeasured gate names", and say both want a new ratchet, "one version, 1.6.0". No session priced shape (c). This one does.

## Words used here

- **S233**, **S384** and so on are numbers of past working sessions of this repository; **BL-92**, **BL-103** are items of its backlog (`docs/planning/BACKLOG.md`). **The operator** is the repository's owner, who decides. A **receipt** is the record a session writes in `HANDOFFS.md` when it closes.
- A **gate** is one entry of `.quality-gates.json`: a name, a direction, a threshold and, usually, a shell command whose number is read. A **run** is `python3 starter-kit/quality_ratchet.py --run`: it runs every gate's command, reads the numbers, writes the **results file** (`.quality-gates-results.json`, overwritten by every run, ignored by git here), prints a table, and prints a **summary line** that a receipt cites (`25/25 pass · results 638dfc5a4d33 · manifest 36d7ab25ab98`).
- A gate **did not pass** when it read `fail`, or read `unmeasured` although its command ran to the end (for example `extract matched nothing (exit 127)`). Not in that set: a gate with no command, and a gate whose command outlived its time budget (the tool stops it and, by design, treats nothing it printed as a measurement).
- **Kept output** is what this plan adds: the text a not-passing gate's command printed, saved where a person can read it after the run.
- **A shared command** is one command two gates use: `tests-sh-passed` and `tests-sh-failed` both run `bash bin/tests.sh`, and the tool runs it once for both (`starter-kit/quality_ratchet.py:495`).
- **The surface** of a piece is where its DONE criterion is shown, with what that surface cannot enforce (the session runner's Planning Sessions rule; its "gate (d)", *faithful verification, per surface*, says a green test that ran somewhere the real thing cannot fail is not evidence about the real thing). A **layer** is one commit of a build session. A **mutation round** changes the new code in small ways (a mutant) to see whether any test notices; a **survivor** is a mutant no test noticed.
- **[E1]** to **[E3]** are files in [`ratchet-kept-output-evidence/`](ratchet-kept-output-evidence/): [E1] `occurrences.sh` with its output, [E2] `suite-output-measure.txt` (a measurement of one real suite run, method in section 9), [E3] `self-ignore-check.sh` with its output. The two scripts read this repository and write only to a throwaway directory.

## 1. Context: what is wrong, measured

**What the tool does with a gate's output today.** `run_gate_command` returns the command's stdout and stderr (`starter-kit/quality_ratchet.py:157`). `measure_gate` joins them, reads one number with the gate's regex, and drops the text (`:505-517`). `do_run` then overwrites the one results file (`:586-590`). After any run, the only trace of what a gate printed is a number, and the next run erases even that.

**Five reds nobody can explain** [E1]. Each is a full gate run that read a suite gate red and whose failing assertion was never named; later runs read green (on the very same commit in S233, S384 and S430, on a later commit in S192 and S257):

| When | Commit | The red run read | What else read | What was lost |
|---|---|---|---|---|
| S192, 2026-09-18 | `4c96234` | 9/10, `tests-sh-failed` 1 | the re-run read green | "one unnamed failure" |
| S233, 2026-09-28 | `5d6fbe4` | 10/11, `tests-sh-passed` 360 and `tests-sh-failed` 1 | four more runs of the same commit read 361 / 0 | the failing assertion, "unrecoverable" (BL-92 was raised for it) |
| S257, 2026-10-04 | `f5d6d4f` | 10/12, one red explained, the other `tests-sh-failed` 1 | it did not recur | "not attributed to a named test (the suite output of a gate run is not kept)" |
| S384, 2026-10-27 | `9507e0f6` | 22/24, `tests-sh-passed` 691 against a floor of 692, `tests-sh-failed` 1 | a direct `bash bin/tests.sh` read 692 / 0; a second full run read 24/24 | the failing assertion; the machine was heavily loaded by other work |
| S430, 2026-11-07 | `52adbb9f` | 23/25, `tests-sh-passed` 701 against 702, `tests-sh-failed` 1 | the suite alone with its output captured read 702 / 0; a second full run read 25/25 | "which test failed is unknown, because the ratchet keeps no output" |

All five are the two gates over `bash bin/tests.sh`. None repeated on demand. That is five reds in the seven weeks from S192 to S430. (At S233 one red in five runs of one commit was measured; no other session recorded how many green runs lay between its reds, so that figure is one measurement and not a rate.)

**Why capturing the suite's output by hand does not close it.** The practice, as S430's and S444's receipts record it, is to run `bash bin/tests.sh > file` in the same clone, detached, with its output kept. It fails exactly where it is needed: the red run is an ordinary gate run nobody thought to capture, and a capture taken *after* a red is green (S384, S430). A red cannot be asked for again, and trying costs 25 to 41 minutes per attempt (S440 took 25 min 4 s, S434 took 41 min 24 s).

**What is not claimed.** That the output would name the cause: unknown until one is kept. That the cause is the suite and not the machine: S384's run was heavily loaded. This plan keeps the evidence; it does not diagnose. BL-92's shapes (a) and (b), done at S357, already dealt with the one suspect it named (Test 44's whole-tree comparison); the S384 and S430 reds came after that repair, so it is not the suspect any more.

**One kind of red left out on purpose.** S280's run (2026-10-07) read the two suite gates `unmeasured (exit 127)`. That one was explained, not a flake: a command that outlived 600 s was reported as exit 127 (`docs/archive/CHANGELOG-through-2026-10-08.md:306`, BL-103), and 1.4.0 reports a timeout as a timeout. A timed-out command keeps nothing here either (section 2).

**How big the suite's output is** [E2]: `bash bin/tests.sh` printed 770 lines and 59,382 bytes to stdout and 0 bytes to stderr, 702 passed, in 615 seconds on a clean clone at a load average of 3 to 7 (the whole 25-gate run is about 34 minutes: S444 measured 34 min 33 s; the suite is the first gate). Each assertion prints one line, `  PASS: …` or `  FAIL: …` (`bin/tests.sh:14-15`), so a failed assertion's whole identity is one greppable line, and the last line is `== Summary: P passed, F failed, S skipped ==` (`:5505`).

## 2. Scope boundary

**In scope.** `starter-kit/quality_ratchet.py`, 1.5.1 to 1.6.0: save the output of every not-passing gate that ran to the end, bounded in size and number, outside git's sight, and tell the person where it is. Its unit tests, its `--selftest` and its `--help`. One sentence in the seed manifest's note about the results file.

**Not in scope, and why.**
- **Diagnosing or fixing the flake.** Different work, and unknowable until an output exists.
- **Output of passing gates.** Alternative D below.
- **Output of a timed-out command.** The tool stops the command and discards what it printed (`run_gate_command`, `:157-203`), by decision: nothing a timed-out command printed is a measurement. None of the five reds was a timeout: each read a number (`tests-sh-failed` 1), and a timeout reads none. Keeping partial output would mean streaming to files instead of reading a pipe: a larger change for no recorded case.
- **`--run` printing the unmeasured gates' names** (BL-103's option (c), the neighbour above): decision D3.
- **The runner, the dashboard, `bin/check-handoff`, `bin/sync`, `bin/migrate-layout`.** None changes (section 7). No sentence is added to `SESSION_RUNNER.md`, so no cut is owed (the rule that a runner addition is paired with a cut: `issue100-fixes-plan.md:122`).
- **Any outward act.** Reaching an adopter, or `KJ5HST/methodology`, is a separate go-ahead each time (section 6, P4).

## 3. Decision: the design

**3.1 When.** Right after each gate is measured, and never while a gate's command runs: for a gate that did not pass and whose command ran to the end, the tool saves that command's output at that moment. Gates that share a command share one saved file. **A run in which every gate passes writes nothing and deletes nothing.** That sentence is the point of the design: in S384 and S430 the red run was followed by green ones, and a design that cleaned up on green would erase the evidence the way the results file does today. Saving per gate, not at the end, also means a run that is cut short (Ctrl-C, a signal, a crash in a later gate: `_stop_on_signals` raises `SystemExit`, `:140-141`) keeps what its finished gates had saved; the suite is the first gate and is 10 of the run's 34 minutes.

**3.2 Where.** A directory `.quality-gates-output/` **beside the results file**: in the project root for a legacy project, under `methodology/` for a new-layout one, wherever an explicit `results_file` puts the results. Every write first writes `.quality-gates-output/.gitignore` containing `*`, so the directory is invisible to `git status` and the project's own `.gitignore` is not edited [E3]. Inside it, **one folder per gate** (the first gate that uses a shared command names the folder), and in it **one file per run**: `<UTC start>-<short commit>.txt`, for example `tests-sh-passed/20261113T231118Z-a8f84d5a.txt`. The start time is taken by `do_run` before the first gate (`ran_at`, `:539`, is stamped at the end, about 34 minutes later). The commit is `head_sha` (`:362`), or `nohead` when git gives none. A name already taken gets `-2`, `-3`, … and is created exclusively (`open(path, "x")`), so two runs in one second cannot overwrite each other. The folder is made with `os.mkdir`, never `os.makedirs`: it must not create a missing parent that the results write would have failed on (an existing test pins that the tool "does not make the directory", `tools/test_quality_ratchet.py:964`).

**A gate's folder name** is its name when that is already lowercase `[a-z0-9._-]` and does not begin with `.`. Any other name is lowercased, every other character becomes `_`, and `-` plus the first six hex digits of the sha256 of the exact name is appended. `config_defects` accepts any non-empty string as a gate name (`:272-274`), so `a/b`, `..` and two names that differ only in case (one folder on APFS) must not escape the directory or collide.

**3.3 What a file holds.** Exactly this form, so a reader and a test agree:

```
quality-ratchet kept output
gates: tests-sh-passed, tests-sh-failed
command: bash bin/tests.sh
exit: 0   budget: 3600 s
commit: a8f84d5a   started: 2026-11-13T23:11:18Z
stdout: 59382 bytes, kept 59382
stderr: 0 bytes, kept 0
=== stdout ===
<stdout text>
=== stderr ===
<stderr text>
```

The tool holds decoded text (`text=True`), so each stream is encoded to UTF-8 and counted in bytes. A stream over the cap is cut in the middle (its start shows how a command began and its end shows how it ended, where a summary or a crash prints): the first H bytes, then the line `... [N bytes omitted] ...`, then the last T bytes, each cut dropping a character that the cut split. The whole suite (59,382 bytes) is far under the proposed cap and is never cut. Proposed H and T: D2.

**3.4 How long.** Per gate folder, the newest K files are kept; older ones are removed after a write. Only names of the form in 3.2 are removed, never a link, never anything in another folder, and never the file just written (a clock set backwards would otherwise sort the new file oldest). Because the count is per gate, a gate that is `unmeasured` on every run (a missing tool) fills only its own folder and cannot push the suite's red out. Proposed K: D2.

**3.5 What the person sees.** The results file gains one top-level key, `kept`, mapping each gate kept *in that run* to its file, as a path relative to the results file's directory (never absolute: the seed allows a project to commit the results file, and an absolute path would carry a home directory into it). `gates`, `summary`, `manifest` and `results` are unchanged, so the citation `results <hash>` that receipts quote is unchanged: the hash is taken over the `gates` list alone (`:538`), and `kept` is added to the snapshot after it is taken.

**But the next run replaces the results file**, and a green run's snapshot has no `kept`. So the pointer cannot live only there: that would hide the red run's output behind the very green run 3.1 protects. Both `--run` and `--status` therefore scan the directory itself and print, after the table, `kept output on disk: N file(s) in M gate folder(s) under <absolute path>; newest <file name> (<gate>)`, and print nothing when the directory does not exist or holds no file. `--run` adds one line per gate kept in this run, with its absolute path; `--status` adds one per gate in the stored `kept` whose file still exists (a committed results file can carry a `kept` into a clone where the folder was never made). Under `--json` nothing is added to stdout beyond the snapshot, which carries `kept`, so a caller that parses stdout still can (the tool's own self-test does, `:765-767`). Exit codes are unchanged (0 clean, 1 unmeasured, 2 failed, 3 usage). The absolute path is printed because the real suite's gate run happens in a scratch clone that is later deleted: the person copies the directory out first, as the results file is copied today.

**3.6 Best effort.** Everything the tool does to keep output is inside `try … except Exception` (not only `OSError`: an encoding error would otherwise escape as a traceback with exit 1 where exit 2 was owed). A failure prints one yellow warning to **stderr** and carries on: every status, the results file and the exit code are what they would have been, and a keeping step never runs ahead of the results write in a way that could stop it. Keeping output must never be able to turn a pass into anything else.

**3.7 How the output reaches the writer.** `run_gates(root, cfg, timeout=DEFAULT_TIMEOUT)` gains one keyword, `keep=None`. When given, it is called as `keep(result, raw)` right after each gate is measured, where `raw` is that command's `(rc, out, err, timed_out, budget)` from the run's memo, or `None` for a gate with no command. Its return value and its behaviour without `keep` are unchanged, so every existing test, which calls it without `keep`, writes nothing (one calls it with `os.getcwd()` as the root, `tools/test_quality_ratchet.py:335`). Only `do_run` passes a keeper. The keeper decides what to save (status `fail` or `unmeasured`, a command that ran, `timed_out` false), remembers which command it has already saved so a shared command is written once, and collects the `kept` map that `do_run` attaches to the snapshot.

**Interface catalog** (the Architecture workstream's table; the tool's command line gains nothing):

| Interface | Input | Output | Error | Versioned? | Consumers |
|---|---|---|---|---|---|
| `--run` | the manifest | as today, plus a file per not-passing gate, the `kept` key, and the "kept output" lines | a failed keep: one stderr warning, same exit code | 1.6.0 | a person; receipts cite the summary line |
| `--status` | the stored results and the directory | as today, plus the "kept output" lines | none new | 1.6.0 | a person at Phase 0 |
| `run_gates(..., keep=None)` | as today | unchanged return value | `keep`'s own failures are the keeper's | 1.6.0 | `do_run`; the unit tests (without `keep`) |
| results file | n/a | one new top-level key, `kept`; no key inside `gates` changes | a reader that ignores unknown keys is unaffected | the tool stamps `version` (`:540`); the file has no schema version | both dashboards read `gates`, `ran_at`, `manifest` only (`tools/methodology_dashboard.py:3315-3332`) |

## 4. Alternatives considered

| | Alternative | For | Against |
|---|---|---|---|
| A | **Do nothing; capture the suite by hand** (today's practice) | no shipped change | five reds in seven weeks; it fails by construction, because a capture after the red reads green |
| B | **A wrapper file named in the gate's `command`** that records the output (BL-92's note says this works without changing a shipped file) | no tool change; per gate | each project writes its own; the gate's command line changes, which the ratchet reports as a changed command and which breaks the shared-command memo; and **measured at S233: a wrapper placed over `bin/tests.sh` contaminated the suite's own self-referential tests and produced three spurious failures** (`BACKLOG-DETAIL.md:3982-3985`), on the one gate that matters |
| C | **Keep the output inside the results file** | no new artifact | the seed says a project may commit that file (`starter-kit/quality-gates.json:5`), so output would be committed; the file is overwritten by the next run, so the red run's output goes with it unless carried forward (more code); `--json` and `--status` load it every time |
| D | **Keep every gate's output, passing or not** | the simplest rule | a passing gate's output explains nothing; it multiplies the size by the 25 gates every run; and it hides the one run that matters among the green ones |
| E | **Make `bin/tests.sh` write its own log and keep the failing ones** | fork-local, no distributed change | only this suite (adopters' suites stay blind); the retention rule needs the exit status from inside the thing under test; any change to `bin/tests.sh` runs inside the same self-referential tests B contaminated |

**Recommendation: the design in section 3.** It looks at a gate's output from outside, so it cannot disturb the suite (nothing is written while a command runs, 3.1), and it covers every gate in every project that runs the ratchet. Its honest weakness is reach: adopters hold ratchet versions from 1.1.0 to 1.5.1 today, and upstream's own copy is 1.1.0, so the change reaches them only when the operator syncs a project from this fork, or when a pull request carrying it is merged (section 7).

## 5. Failure modes of the new step

"A test" below means a unit test written in P2; "P3" means the proof on the real suite.

| Failure | What happens | Guard |
|---|---|---|
| A write fails (read-only tree, full disk, permissions, an encoding error) | one stderr warning; statuses, results file and exit code unchanged (3.6) | a test with an unwritable folder (skipped when run as root and on Windows) and a test whose keeper raises a non-`OSError` |
| The next green run hides the red run's output | the files stay; the results file loses `kept`, so both modes scan the directory (3.5) | a test: failing run, then passing run, then `--status` prints the on-disk line and the first file is byte-identical; P3 repeats it on the real suite |
| A gate that is never measured evicts the suite's file | retention is per gate folder (3.4) | a test: seven runs of an unmeasured gate beside one run of a failing gate; the failing gate's file survives |
| A run is cut short | each not-passing gate is saved right after it is measured (3.1) | a test: gate 1 fails and is saved, gate 2 raises; gate 1's file exists |
| `--json` output stops parsing | no extra stdout lines under `--json`; warnings go to stderr | a test that runs `--run --json` after a failing gate and loads stdout |
| `results` hash drifts, so every receipt's citation stops matching | `kept` is outside `gates`; the hash is taken before `kept` is added | a test with a literal hash: the unmodified 1.5.1 tool is run once over a throwaway manifest holding a passing, a failing, an unmeasured-with-exit and a no-command gate, its `results` is written into the test as a literal, and 1.6.0 must equal it (the existing pinned hash, `tools/test_quality_ratchet.py:608`, covers a passing manifest only) |
| A gate name escapes or collides (`a/b`, `..`, `Tests` and `tests`, a leading dot) | the folder name is sanitised and carries a hash of the exact name (3.2) | a test per hazard |
| Two runs at once, or two in one second, or a clock set backwards | exclusive creation with a numeric suffix; the file just written is never pruned | a test that forces two runs onto one start time and commit; a test with a future-dated stray file |
| A symlink or a stray file in the directory | pruning never follows a link and never removes a name that does not match 3.2's form | a test with a planted link and a planted stray file |
| `.gitignore` inside the directory is deleted or edited | rewritten on every write | a test that deletes it between two runs |
| Unbounded growth | per gate folder at most K files, each at most 2 × (H + T) bytes plus a header | a test that runs K + 2 failing runs and counts files; a test that writes more than H + T bytes and reads the marker line |
| An explicit `results_file` in a folder that does not exist | the run fails as it does today (`os.mkdir`, not `makedirs`) | the existing test at `:964`, unchanged |
| Several projects share one absolute `results_file` | they share one directory and, if their gates have the same names, prune each other's files | stated, not guarded: it is the operator's setup |
| A layout move (`bin/migrate-layout`) | the old directory stays behind in an ignored place; the next run creates the new one beside the moved results; harmless | stated in P2's record; the migration's own tests are unaffected because the directory is never tracked |
| A kept directory is present while later gates run | no suite assertion reads the live tree's status now (Test 44 moved to a fixture at S357, `bin/tests.sh:3969`; the other `git status --porcelain` reads, `:2205-2209`, `:2467`, `:3939-3943`, are of fixtures), and an ignored directory is not in porcelain output anyway; a `find` or a directory count over the tree would see it | P3: the 23 gates that run after the suite read as in an unmodified run, and a second run with the first run's directory present reads 25/25 |
| An old tool reads a results file with `kept`, or the new one reads a file without it | both ignore what they do not know | a test per direction |
| A scratch clone is deleted with the output in it | the absolute path is printed; the seed note says to copy the directory out | the seed note (P2); P3 does the copy |
| Windows | the tool already runs there without process groups (`HAS_PROCESS_GROUPS`) | the new tests that need POSIX are guarded the way the existing ones are; not run on Windows (section 9) |

## 6. Pieces, each one session, each with its own STOP

### P1: this plan (done at the close-out of the session that wrote it)

DONE: this file, [`ratchet-kept-output-evidence/`](ratchet-kept-output-evidence/), BL-92's row pointing here, the receipt. No code.

### P2: build 1.6.0 on fork `main` only

**DONE when:**
1. New tests are written first and fail on 1.5.1 for the right reasons: the red list is recorded, and the tests that hold on both (exit codes; a timeout keeps nothing; a passing run keeps nothing) are named as expected to pass. The literal-hash test is written first against the **unmodified** tool and is the one test that must pass on both.
2. `starter-kit/quality_ratchet.py` is 1.6.0 with the behaviour of sections 3.1 to 3.7 in the forms of 3.2 and 3.3; its `--help` text and module docstring say what is kept, where, and that it is local and must not be committed; `--selftest` gains one check that a failing gate keeps its output and one that a later passing run leaves it.
3. `tools/test_quality_ratchet.py` holds a test for every row of section 5 whose Guard names a test; the `ratchet-unit-tests` floor in `.quality-gates.json` moves from 123 to the measured count, with a `_s…_tightening_bl92c` note (tightening needs no approval).
4. A mutation round on the new code, survivors each given a test (this tool's practice: BL-103's repairs 1 and 2 ran one, 23 mutants, and 6 survived round one, each a behaviour no test named).
5. The seed's `_results_file` note names the directory, the do-not-commit warning and the copy-out advice for scratch clones.

**Verification commands, repository root, serially:** `python3 tools/test_quality_ratchet.py`; `python3 starter-kit/quality_ratchet.py --selftest`; `python3 bin/check-layout-literals` (0 sites; the new directory name may need a `# layout: ok` marker); `bash bin/tests.sh` after the tool layer, because it runs the ratchet's unit tests (`:288`) and its self-test (`:3439-3440`, both with their output discarded, so a failure shows only as a failed assertion) and a changed output is a changed input; then the 25 gates on a scratch clone of the last work commit (about 34 minutes, detached, with a done-file).

**Files.** At most five per commit (`SAFEGUARDS.md`): layer 1 the tool, its tests and the ledger; layer 2 the floor, the seed note and the ledger; the backlog row rides the close-out.

**Surface:** this repository on `main`, scratch clones for the gates, one writer per tree. **Cannot enforce:** that the behaviour holds on a 34-minute run with the real suite's output (P3), on Windows, or in an adopter. A unit test over a two-second `python -c` command is not evidence about `bin/tests.sh` (gate (d), applied at plan time).

**Session boundary.** One session. Close out when DONE holds. Do not start P3.

### P3: show it on the real suite

**DONE when**, in a scratch clone of P2's last commit, and recorded in `ratchet-kept-output-evidence/`:
1. The failure is injected by adding one line to the clone's `bin/tests.sh`, `fail "kept-output proof: deliberate failure"`, right after Test 1's header (it prints `  FAIL: …` and counts one failure, and nothing else moves). A full `--run` reads `tests-sh-failed` red and `tests-sh-passed` at its floor (702); the kept `tests-sh-passed/…txt` contains the injected `  FAIL:` line and `== Summary: 702 passed, 1 failed, 0 skipped ==`; `kept` names it; `--status` prints the "kept output on disk" line; the only line of `git status --porcelain` is the injected edit; the 23 gates that ran after the suite, with the directory already present, read as in an unmodified run (24 pass, 1 fail). If the dirty `bin/tests.sh` makes any assertion other than the injected one change, P3 records which: that is a finding about the injection, not a failure of the proof.
2. The injection is removed (`git checkout -- bin/tests.sh`) and a second `--run` reads 25/25: it keeps nothing, the results file has no `kept`, `--status` still prints the "kept output on disk" line, and the first run's file is byte-identical. This is the S384 shape end to end, with the real suite's output present in the tree for the second run.
3. The kept stdout section is within 5% of 59,382 bytes ([E2]'s green run), so the caps keep the suite whole.
4. The directory is copied out of the clone with `cp -R` before the clone is deleted, and the copy reads the same.

**Surface:** a scratch clone of this repository running its own real suite twice (about 70 minutes; detached with done-files). **Cannot enforce:** that a *real* flake becomes diagnosable; that shows only when one happens, which is the point of keeping output.

**Closes** BL-92 (shapes (a) and (b) are done; this is (c)). **Session boundary:** one session; do not start P4.

### P4: not a piece of this repository's work

How 1.6.0 reaches anyone: (a) the operator's own projects that declare gates (section 7) by `bin/status` then `bin/sync` from this fork, each his go-ahead; (b) upstream, stacked on the pull request that carries the ratchet (#99, which holds 1.5.0 at its head) or after it, his go-ahead each time, with a merge trial first (section 9).

## 7. Impact

| System | Impact | Action |
|---|---|---|
| `starter-kit/quality_ratchet.py` (distributed) | the one shipped file that changes; `run_gates` gains an optional keyword | P2 |
| `.quality-gates-results.json` | one new top-level key, `kept`; no field of any gate changes | none |
| both dashboards (byte-identical twins) | read `gates`, `ran_at`, `manifest`; ignore the rest | none |
| `bin/check-handoff`, the Phase 0 citation check | read the receipt's summary line and the results' counts and `results` hash | none: the hash is unchanged by design |
| `bin/migrate-layout`, `bin/sync`, `bin/_seed_paths.py` | the directory is derived from the results path, so no new methodology file name is added to any table | none; a legacy to new move strands the old directory (5) |
| `SESSION_RUNNER.md`, `SAFEGUARDS.md` | untouched | none |
| adopters that declare gates | 8 of the projects under `~/Development` declare 1 to 12 gates (`airqino` 2, `claude_work` 2, `colossians_1_15_20` 1, `gaius` 4, `nprcgenekeepr` 12, `pedkindraw` 4, `Philippians` 2, `vscode_quarto_ext` 2) and hold the tool at 1.1.0 to 1.5.1 | nothing changes in any until it is synced (P4) |
| the 25 gates here | `ratchet-unit-tests` rises; `tests-sh-passed` does not (P2 adds no test to `bin/tests.sh`) | P2 |
| the working tree during a run | an ignored directory appears after a failing run | P3 shows the later gates and a second run are unaffected |

## 8. Decisions for the operator

- **D1. Build it as designed** (a tool change, 1.6.0, fork `main`), rather than A, B, C, D or E? *Recommended: yes.* Choosing A or E is a legitimate no: E would give this repository its own answer sooner and leave every other project blind, and it edits the suite that B showed is fragile to wrappers.
- **D2. The numbers.** Per stream: up to 256 KiB, and when longer the first 64 KiB and the last 192 KiB; the newest **5** files per gate folder. *Recommended:* the cap is above the suite's whole output (59,382 bytes, [E2]) so the suite is kept whole, and K = 5 is as many failing runs as were recorded in the whole seven weeks, all of them the same gate, so a session that comes back after a bad stretch still finds them. Both are constants in the tool; changing one is a version bump, not a decision about design.
- **D3. BL-103's option (c), `--run` printing the unmeasured gates' names in `check-handoff`'s form**, which the 2026-10-18 interaction review paired with this change as "one version, 1.6.0": the same build, or separate? *Recommended: separate.* It is a different capability with its own red-first tests, the two share only the print path, and a version number is cheap; if it is built first it takes 1.6.0 and this takes 1.7.0.
- **D4. P3 as its own session?** *Recommended: yes.* Two real-suite runs are about 70 minutes, and P2's unit tests cannot stand in for them (section 6, P2 surface).
- **D5. The route.** *Recommended: nothing outward now.* Decide P4 after P3.

## 9. What was checked, and what was not

**Checked this session, with the place:**
- `starter-kit/quality_ratchet.py` read in full (932 lines, 1.5.1). Every line number into it in this plan was read at that version.
- The five reds read at their sources [E1], which the script finds by phrase; the sixth, excluded (section 1), at `docs/archive/CHANGELOG-through-2026-10-08.md:306`.
- A directory holding its own `.gitignore` of `*` is invisible to `git status` and `git add -A` and does not hide a real change beside it, with git 2.56.0 on this machine [E3].
- The suite's output [E2]: one run of `bash bin/tests.sh` in a clean `--no-hardlinks` clone of `a8f84d5a`, stdout and stderr kept separately, at a load average of 3 to 7, with `suite-output-measure.sh` run over the five files the detached run left.
- The tool versions: upstream `main` 1.1.0, #99's head `47637be2` 1.5.0, #98, #102 and #96 heads 1.1.0, fork `main` 1.5.1, read with `git show`; #99's head differs from fork `main` in this file in 11 hunks (17 insertions, 12 deletions): the version line, ten others of which `install_hook` holds the largest (the 1.5.1 commit `0df0bae8`: `install-hook` resolves a symlinked tool path) and one is in `selftest`, which this change also edits.
- The adopters' gate counts and tool versions (section 7), by reading each project's manifest and tool, read-only.
- **A cold read.** A fresh agent with read-only tools, given the first draft of this plan and the code and told none of its conclusions, read it once. Each of its findings was checked against the files before use: all seven of its fact findings held (one showed a claim of mine wrong: BL-103's option (c) does resolve, to the neighbouring feature), and its blocking design finding (a green run erases the results file's pointer to the red run's output) is why 3.5 scans the directory. Its other design findings became 3.1 (per-gate saving), 3.2 (per-gate folders, safe names, exclusive creation, `os.mkdir`), 3.4 (per-gate retention), 3.6 (`Exception`) and 3.7 (the `keep` keyword); its executability findings became the exact forms in 3.2 and 3.3 and the rewritten P2 and P3. The reworked design has **not** been read cold a second time.

**Not checked:**
- That the output would name a real flake's cause (nothing can show that until one is kept).
- Windows. The tool's own tests that need process groups are skipped there; this plan's tests are written to the same rule and are not run.
- Whether the change applies to #99's 1.5.0 source cleanly: it will be built on fork `main` (1.5.1), and the two differ in 11 hunks, one in `selftest` which this change edits too. A merge trial belongs to P4 (`git merge-tree`, as the other pull requests' trials were done).
- Git versions older than 2.56 for the `*` in a directory's own `.gitignore`. The behaviour is long-standing and the same trick many tools use for a cache directory, but this plan measured one version only.
- The cost of the per-gate write on a run with many failing gates: at most one small file each, but not measured.
