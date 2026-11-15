# P4 merge trial record (S453, 2026-11-15): the ratchet's 1.5.1, 1.6.0 and 1.7.0 changes on pull request #99's source

Fork only: nothing was sent to `KJ5HST/methodology`, and nothing in this repository's tool or its tests changed. The operator picked
this as the session's deliverable at the S453 Phase 0 picker ('P4 merge trial'). It is the "merge trial first" that section 6, P4 of
[`../ratchet-kept-output-plan.md`](../ratchet-kept-output-plan.md) asks for before route (b), upstream. Route (a), the operator's own projects
by `bin/status` and `bin/sync`, is **not** tried here (section 4).

## Words used here

- **#99** is the open pull request on `KJ5HST/methodology` that carries the quality ratchet at 1.5.0; its head is `47637be2`, written **ours** below.
- **The change** is the net difference, in the three shipped files (`starter-kit/quality_ratchet.py`, `tools/test_quality_ratchet.py`,
  `starter-kit/quality-gates.json`), between this fork's last 1.5.0 text (`0df0bae8^`, `b01f0fe9`) and `b32fda08` (1.7.0; equal to fork `main` in these
  three files). It is 1.5.1, 1.6.0 and 1.7.0 together: 19 hunks, 81,435 B as a patch (+1,226 and -7 lines). **The 1.6.0-only change** stops at
  `f1020217`: 17 hunks, 68,999 B (+1,048 and -6).
- **A composed tree** is a scratch clone of this repository at ours with the three files replaced by the result of the merge; **the control tree** is the
  same clone untouched. A **three-way merge** applies what changed between a base and a wanted state to a third copy that moved on its own.

## 1. Why a three-way merge, and which base

#99's head is not a descendant of the fork's ratchet commits: it was rebuilt on `upstream/main` (`d50ce290`), so its three ratchet commits
(`7d87cb2b`, `1d93579a`, `911c82fe`) are a rebuilt and reworded series, not the fork's, and the fork's merge base with it is the old `f34769f3`. I did not
cherry-pick the fork's commits one by one (each carries its own surrounding text and fork-only files); the question is asked of the three shipped files
directly: a merge with base `0df0bae8^` (the last fork text that says 1.5.0), ours `47637be2`, theirs `b32fda08`. The fork's eight commits since 1.5.0
(`0df0bae8`, `2f84a756`, `52fdb97a`, `f1ea7034`, `f1020217`, `e33ebeba`, `1e84df48`, `dcc5129b`) touch nothing shipped except those three files; everything else
in them is the fork's own ledger, evidence and root manifest. #98, #102 and #96 touch none of the three files, so no other open pull request can collide with them.

## 2. What was found

| Question | Answer | Where |
|---|---|---|
| Does the change apply to #99's text? | **Yes, with one conflict, one line wide.** Tests and seed: no conflict. Tool: one block at the top (`HAS_PROCESS_GROUPS`, `quality_ratchet.py:87` of the merged file): #99's rewording dropped a `(BL-107)` suffix from a comment, and 1.6.0 adds four constants on the next lines. | `p4-trial-state.txt`, 'merge' |
| Is that result the instrument's, or an accident of it? | Two mechanisms agree: `git merge-file` on blobs and `git apply --3way` of the net patch in a clone. A **positive control** (one `VERSION` line changed in ours) reads 2 conflicts, so the zero elsewhere is believed; a **negative control** (nothing changes) is clean and equal to ours. After one rule for the one block (keep ours' line, add the lines the change adds), both outputs are **byte-identical** for all three files. | 'merge', 'patch', 'resolve' |
| Does the composed tool work on #99's tree? | Unit file: control **120 tests OK**; composed **207 tests, 1 error** (92 s); 1.6.0-only **190 tests OK**. `--selftest`: control 30 checks OK, composed 33, 1.6.0-only 32. | 'units' |
| What is the one error? | `test_the_lint_accepts_the_pasted_pair_and_refuses_the_citation_without_the_clause` (1.7.0's, `test_quality_ratchet.py:2181`): it loads `bin/check-handoff` and expects its `validate_gate_citation` to refuse a citation that does not name the unmeasured gates. #99's lint (`bin/check-handoff:430`) has no such rule; it was added on the fork by `5cb11a6c` (23 lines added, 6 removed; **the fork's file had 1,026 lines then, #99's has 537**). Cause shown, not assumed: with that one commit merged into #99's lint on blobs (no conflict), or with the fork's whole lint, the test and the whole 1.7.0 class (17 tests) pass. | 'lint' |
| Does #99's own gate set stay green? | Composed tree, `quality_ratchet.py --run` over #99's 18 gates, about 20 min at load 10.8: **16/18 pass, 2 fail**, results `e349b0deaf1a`, manifest `72583325c300`. The two are the suite gates: 301 passed against a floor of 302, and 1 failed. The kept output (the 1.6.0 keeper, working on #99's tree) holds exactly one `FAIL:` line, `quality ratchet unit tests failed` (`bin/tests.sh:287`): the same error, seen from the suite. 301 + 1 = 302, #99's declared floor. The other 16 gates, including every layout, migrate and checker suite, pass. | 'run, composed' |
| And with 1.6.0 alone? | **Yes.** The same one-line conflict and the same byte-identical resolution; 190 unit tests OK; `--selftest` 32 checks OK; `--run` over #99's 18 gates: **18/18 pass, 0 fail, 0 unmeasured**, results `e2f466fc1cf6`, manifest `72583325c300`, `tests-sh-passed` 302 (equal to #99's floor). It took 31 min 37 s while other work on the machine held the load average at 250 to 317 (against about 10 for the first run); nothing was re-run and nothing read red. | 'units', 'run, 1.6.0-only' |
| What would the pull request carry that is the fork's own? | Five comment lines with project-internal codes in the added text (line numbers at `b32fda08`), none in #99's own text: 1.6.0 two (`test_quality_ratchet.py:1337` a plan path, `:1517` two session numbers), 1.7.0 three (`quality_ratchet.py:761` a backlog id; the tests `:2065` a backlog id, `:2066` a session number and 'the operator'). Counted by regex, so a wording read is still owed. | 'census' |

**The floor.** #99's `.quality-gates.json` declares `ratchet-unit-tests` at 120. The composed tree measures 207 (1.7.0) or 190 (1.6.0 only), so a pull request
would tighten that floor to the measured count (a tightening needs no approval; section 6 of the plan). #99's tree has no `.github` workflows: the surface for
its gates is the maintainer's own machine.

**A side result for the plan's P3.** The keeper's DONE criteria were shown on the fork's tree. Here it ran unchanged on #99's tree (18 gates, a different
suite) and kept the failing run's whole output in the first gate's folder, as designed; the unmeasured-names clause correctly printed nothing (0 unmeasured).

## 3. What the one dependency means

1.7.0 prints `unmeasured: <gate>, <gate>` "in the form `bin/check-handoff` reads". On #99's tree nothing reads it: its lint requires that a citation exist and
checks nothing about names. The clause is harmless there, but its stated purpose and its one test both rest on a file that is **canonical-only** (not
distributed) and on a separate fork capability (BL-103's repair 3, `5cb11a6c`), which neither `upstream/main` nor any open pull request head has (checked: 0 hits for the rule's message in `bin/check-handoff` at each). So 1.7.0 does not travel alone as it
stands: either its one test is changed, or the lint's rule travels with it, or 1.7.0 waits.

## 4. What this trial cannot say

- **#99 moves.** This is its head `47637be2` at S453. If its head changes, `p4-trial.sh merge` and `patch` re-answer in seconds; the unit and gate runs in about 20 minutes.
- **Only macOS (arm64), Python 3.10.12, git 2.56.0.** Not Linux, not Windows.
- **Route (a) is not tried.** A sync copies whole files and has its own dry run (`bin/status`, `bin/sync`); each adopter is a separate go-ahead and was not touched.
- **The census is a regex count**, not a read of the wording; a pull request needs its own cold read of the composed diff (the plan's section 9 says the same of its design).
- **Not run:** a `--run` of #99's untouched head (the 1.6.0-only run's 302 passed and 0 failed, and #99's own floor of 302, stand in for it; the change adds no
  assertion to `bin/tests.sh`); `bin/check-handoff`'s own tests with the merged lint (only the 1.7.0 class was run against it); anything about whether the maintainer
  wants the change.
- **No outward act was made or prepared.** Nothing was pushed, opened or commented.

## 5. Decisions the trial leaves to the operator

- **D-A. The route, now?** *Recommended: nothing outward now.* The trial removes "does it land" as an unknown; whether and when to send is his, with his go-ahead each time.
- **D-B. If it is sent: what travels.** (1) 1.5.1 and 1.6.0 together: lands with the one-line conflict, 190 unit tests and #99's whole gate set green (see the 1.6.0 row), two
  comment lines to reword. (2) 1.7.0 later or with the lint's rule from `5cb11a6c`, which is a `bin/check-handoff` change of its own with its own review. (3) 1.7.0 now with
  its one lint test guarded to skip when the lint lacks the rule (a change to the test, not the tool). *Recommended if sent: (1), then (2).*
- **D-C. Stacked on #99 or after it.** The files are the same either way; "after" lets #99's own review changes land first and the trial re-run once.

## 6. Reproduce

From the repository root, with `<W>` a scratch directory outside it (the six phases are in [`p4-trial.sh`](p4-trial.sh)'s header):
`bash p4-trial.sh merge <W> "$PWD" 0df0bae8^ 47637be2 b32fda08`, then `patch` (same arguments), `resolve <W>`, `compose <W> "$PWD" 47637be2`,
`lint <W> "$PWD" 47637be2 5cb11a6c main`, `census "$PWD" 0df0bae8^ 47637be2 b32fda08`. The long runs are
`bash p3-prove.sh launch <W>/composed <tag>` (the clone is named `methodology`, which the gates' paths need). The verbatim outputs are in
[`p4-trial-state.txt`](p4-trial-state.txt).
