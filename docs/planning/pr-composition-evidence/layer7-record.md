# PR2, Part 2, layer 7: `bin/migrate-layout`: NOT BUILT. Its own suite needs two things the candidate does not have

**Status: a FINDING, no layer built, nothing sent. D5 amended at his word.** Session S319, 2026-10-14. This is the ninth PR2 session
(`../upstream-pr-composition-plan.md` §3 and §5; layer 6's record, [`layer6-record.md`](layer6-record.md), §7 named this layer and left
"what else its suite needs" NOT CHECKED: this record is that check). `pr2/candidate` is unchanged, `0aa1897`.
Every figure below is printed by a script in this directory or by a command named beside it; the saved outputs are `layer7-*-output.txt`
and `layer7-probe-failure-lines.txt`.

## 1. The answer first

1. **Taken whole into the candidate, the tool and its suite fail 10 of 280 tests** (`layer7-probe-output.txt`, state `base`: 363 s, exit 1).
   `bin/migrate-layout` and `tools/test_migrate_layout.py` are the fork tip's bytes (`d68207f`; equal at `7ac733d`, the tip when this ran), put into a
   clean `--no-local` clone of `0aa1897` with nothing else changed. The other 270 pass, so the tool's own logic is not the problem.
2. **Two things are missing, and each was measured by adding it alone** (the two classes that hold the 10, `TestTheChecks` and `TestTheShardRehearsal`,
   23 tests, about a minute each state):

   | State of the candidate + the tool and its suite | Fails of the 23 | Whole suite |
   |---|---|---|
   | as it is (`base`) | 10 | 10 of 280 fail, 363 s |
   | + the tip's `bin/check-ledger` and `bin/check-handoff` (`checkers`) | **10** | |
   | + the tip's 23 framework documents (`docs`: the prose layer) | **9** | |
   | + both (`both`) | | **280 run, OK, 361 s** |

   **All 10 need the prose; 9 of them also need the two checkers; the tenth needs only the prose.** The prose layer alone leaves 9 red.
3. **The checkers (D5), the cause the prose cannot fix.** `bin/migrate-layout` runs `HERE/check-ledger` and `HERE/check-handoff` over the project before
   and after the move and compares their exit codes (`bin/migrate-layout:1201` `run_checks`, `:1227` `check_differences`). The candidate's two are
   **upstream's own blobs** (`a96b641`, `d314c4d`), which read the legacy layout only: D5 left them out on 2026-10-14. On a migrated tree they exit
   differently, the tool reports `CHECKS DIFFER`, and an apply exits 4 (`layer7-probe-failure-lines.txt`, `docs`: `Lists differ: ['ledger', 'handoff'] != []`). A tool
   shipped in that state fails its own after-check on every migration it does.
4. **The prose, the cause the plan already placed after this layer.** The candidate's framework documents carry 34 dangling links once under `methodology/` (S318 read 35 in
   `check-links --layout new`), and the tool's links check judges them: `Tuples differ: (34, 3) != (1, 1)` (`base` and `checkers`, not `docs`).
   The one test the prose alone repairs is `test_a_framework_document_that_dangles_after_the_move_is_a_difference_exits_4_and_the_commit_stands`.
5. **The tip's count gate would have read this green.** `migrate-layout-unit-tests` (min 280, `extract` `Ran (\d+) tests`) is measured by `measure_gate()` from the output
   alone, and a gate with an `extract` ignores the command's exit code: a suite that prints `Ran 280 tests` and `FAILED` reads 280 and passes. The tip's `why` says
   *"green/red is carried by tests-sh-failed"*; that holds for every other suite (`bin/tests.sh` runs them whole) and **not for this one, whose command-level classes
   `bin/tests.sh` does not run** (the tip's own comment at `bin/tests.sh:327`). `layer7-pair-proof.py` shows the repair on the candidate's own `run_gates()`: a count gate and a
   second gate over the **same command string** with no `extract`: `suite-count measured=5.0 status=pass`, `suite-failed measured=1.0 status=fail`, **command executions: 1**
   (`layer7-pair-proof-output.txt`; the memo is keyed by the command, the design of the `tests-sh-passed` / `tests-sh-failed` pair).
6. **His answer** (the S319 picker, the recommended option): **amend D5 from (a) to (b)** (carry the layout hunks of the two checkers, hand-built as upstream's blob plus those
   hunks) **and reorder: the checkers' layout reading, then the prose, then `bin/migrate-layout` last.** Plan §3, §4 row F, §7 and the status line say so.
7. **Against the two open pull requests:** not recomputed; no tree changed. #94 and #92 had no comment or review at Phase 0 (`gh api`, 2026-10-14).

## 2. What the probe is, and what it cannot show

`layer7-probe.sh <fork> 0aa1897 d68207f` clones the candidate four times (under `~/.cache/layer7-probe-<state>`), drops in the tip's tool, its suite and the tip's sync suite (whole: layer 6
had left one assertion out because the tool did not exist), adds what the state says, and runs the suite serially. **The surface is this machine**: load average 6 to 15 during the run, a clean
clone per state, no hooks armed. **It cannot show:** the suite on a maintainer's machine; a real adopter's tree (the 280 tests build scratch projects, as the fork's did); that the
hand-built hunks of D5 (b) pass the 280 (`checkers` and `both` use the tip's WHOLE files, +610 / -57 for `bin/check-handoff` and +72 / -5 for `bin/check-ledger` against the candidate's,
which include fork-only lints §4 row F keeps off the pull request: how much of that is the layout reading is NOT CHECKED); that the 23 documents the `docs` state drops in are the prose layer's
exact set (every Markdown file under `starter-kit/` and `workstreams/` plus the three root framework documents, from the tip: 23 files, of which 17 differ from the candidate's, +102 / -67). The probe script's `sed` that shortens test names is a no-op under BSD sed
(`\S`), so its failure lines print as unittest prints them; the script is left as it ran.

## 3. The builder: a draft whose mechanics were run, not its result

`layer7-build.py` is written on layer 6's pattern (every precondition asserted before the first write: the tool's inputs equal the tip's, `bin/_manifest.py` equal in code, the candidate's sync
suite equal to the tip's less the one assertion). **Run on `0aa1897` in a scratch clone: stage `tool` writes 3 files, stage `suite` 2 and then the gates file; the gates file parses.** **Not run:** the
suite stage's result through the suite and the ratchet (no layer was committed), and the floors it writes (280, 300, 76) are placeholders for the mechanics test, not measurements. **It must be re-based
before it is used:** after the checkers' layer the `COPIES` anchor it edits (`COPIES_OLD`), the tests.sh insertion point and the gates' place will have moved, and the prose layer changes what its `docs`
assertions read. It writes two gates over one command (§1.5) where the tip has one: the layer that carries `bin/migrate-layout` should carry the pair.

## 4. Decisions I took that the plan did not

1. **I stopped at the finding rather than ship the layer around it.** Three ways round were possible and none is mine to choose: skip the 10 tests until the prose layer (the tool would still fail its own
   after-check for the 9 that need the checkers, after the prose too), edit the tool so its after-check skips the two checkers (1,458 lines that differ from the bytes the fork tested over 12 adopters),
   or build the prose layer in its place (a different deliverable). The picker asked; he chose the recommended one.
2. **The paired exit gate** (§1.5) is a divergence from the tip, written into the draft builder only; it tightens and loosens nothing.
3. **The draft builder and the probe are committed** so the next session starts from measurements, with §3 saying exactly what they have and have not shown.

## 5. Not done, and not known

Not done: any layer; the checkers' layer (§6); the prose; the scrub. **The fork tip carries the same hole** (its `migrate-layout-unit-tests` gate counts a suite `bin/tests.sh` does not run): not changed here,
a fork-only gate repair that is his call. Not known: which of the checkers' 10 scanner sites (6 in `bin/check-handoff`, 4 in `bin/check-ledger`) the hand-built hunks must carry to make the 280 pass; whether
`tools/test_checker_layouts.py` (the tip's 281 lines) can be cut to the two checkers the candidate has (it also drives `bin/check-overhead` and `bin/model-report`, which the candidate lacks:
`git cat-file -e pr2/candidate:bin/model-report` fails).

## 6. Next: the checkers' layout reading, as one layer

Plan §3 (amended), §7 D5 (b). Derive first (`git`, read-only): the layout hunks in the tip's two checkers against upstream's blobs; each tool's embedded resolver block (the layout suite's `COPIES` must list both,
and the candidate's two `NOT_SCANNED_ALWAYS` entries (`bin/check-layout-literals:60-61`) and the layout suite's `test_the_two_checkers_that_do_not_read_the_layout_are_not_scanned_and_say_why`
(`tools/test_layout_resolver.py:635`) are deleted by this layer, since the scanner then reads them); a suite for the two checkers cut from the tip's `tools/test_checker_layouts.py` with its count measured; the wiring block and the gate (`checker-layout-unit-tests`, the tip's 15, re-measured). Verify
as every layer: a clean `--no-local` clone, `layer-verify.sh <candidate> <commit>`, the contrast against the parent's tools, mutants aimed at code. **Then the prose; then this layer**, re-running
`layer7-probe.sh` with `checkers` and `docs` replaced by the candidate's own commits as the first check.
