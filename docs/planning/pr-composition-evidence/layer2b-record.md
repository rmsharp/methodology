# PR2, Part 2, layer 2b: the quality ratchet's 1.4.0 and 1.5.0, a gate's budget and its process group

**Status: BUILT and verified, un-pushed, nothing sent.** Session S314, 2026-10-14. This is PR2's fourth checkpoint (`../upstream-pr-composition-plan.md`
§3 and §5; Part 1 is [`part1-record.md`](part1-record.md), layer 1 [`layer1-record.md`](layer1-record.md), layer 2 [`layer2-record.md`](layer2-record.md), whose §4.1
decided this layer would be a commit of its own). Every figure below is printed by a script in this directory or by a command named beside it; the saved
outputs are `layer2b-*-output.txt`.

## 1. The answer first

1. **The layer exists.** Local branch `pr2/candidate` is now `c8c0b21`, one commit on layer 2's `fd96593`: **4 files, +696 / -20**; the candidate as a whole is
   4 commits and 18 files, +10,714 / -703 (`git diff --stat upstream/main pr2/candidate`). No upstream is configured and nothing named `pr2*` exists on `origin`.
2. **It is green on upstream's tree, in a clean `--no-local` clone** (`layer-verify.sh`, `layer2b-verify-output.txt`): `quality_ratchet.py --run` **13/13 pass,
   0 fail, 0 unmeasured** (results `b62a4535792f`, manifest `116324e9d629`; the manifest differs from layer 2's `f43c41607f11` by the one floor); the shell
   suite **298 passed, 0 failed, 0 skipped in 296 s** (the same count as layer 2: this layer changes no block of `bin/tests.sh`, `layer2b-suite-output.txt`);
   the ratchet's own suite **120 tests, OK**; the layout suite 74; the tool's selftest 30 checks; the one shipped `.verify.sh` exit 0, as at layers 1 and 2.
3. **The new tests exercise the new behaviour** (`layer2b-unit-output.txt`): 39 tests are added (81 to 120), none removed. Run against layer 2's tool (1.3.0), **36
   of the 39 fail by name** (25 failures and 12 errors: one test reports twice) and **none of the 81 old tests fails**. The 3 that pass hold on both tools by
   design: a command that cannot start is not a timeout; a run with no timeout hashes as 1.3.0 did; an undeclared gate keeps the default beside a shorter declared one.
4. **The builder reproduces the commit.** `layer2b-build.py` run on `fd96593` with the fork's `ee48ace` as the source and `--ratchet-count 120` gives tree
   `864c7aaa3bc3`, equal to `c8c0b21`'s. Before it writes anything it asserts that the candidate's three files equal the fork's `26bc97a` blobs byte for byte, which
   is what makes "the tip's file is 1.3.0 plus 1.4.0 and 1.5.0 and nothing else" a checked statement.
5. **The scanner reads 121 sites over 7 of 14 files**, line for line as at layer 2 (the one difference is the uncounted-prose counter, 168 to 169). Still not a gate.
6. **Against the two open pull requests, derived with `git merge-tree`:** #94's head (`972eb2cd6263`) conflicts in the same two files as at every layer
   (`starter-kit/methodology_trim.py`, `tools/test_methodology_trim.py`); #92's head (`fa2bb5d464f9`) not at all. This layer adds no conflict.

## 2. What it carries

| File | Change | Note |
|---|---|---|
| `starter-kit/quality_ratchet.py` | +203 / -17 | 1.3.0 to 1.5.0: `DEFAULT_TIMEOUT` and `HAS_PROCESS_GROUPS`; `run_gate_command` (a timed-out command has no exit code, so it reads `unmeasured`, note `timeout (N s)`, never a number read out of the timeout message); `_stop_group`, `_stop_on_signals` (the command runs in a session of its own and a timeout, Ctrl-C, hangup or SIGTERM stops its whole group; a signal the caller ignores stays ignored); `timeout_seconds` validated in `config_defects` and a change to it a warning in `compare`; gates over one command share one run under the largest budget; two selftest checks |
| `tools/test_quality_ratchet.py` | +491 / -1 | 120 tests (81): the budget in both directions, the group stop, the signals through a real child, the shared run, the seed's text |
| `starter-kit/quality-gates.json` | +1 / -1 | the `_gate_schema` line names `timeout_seconds` and says what becomes of a command that outlives it |
| `.quality-gates.json` | +1 / -1 | `ratchet-unit-tests` 81 to 120: tightened by exactly what this adds |

**What the layer does to a reader of the gate run:** a gate whose command outlives 600 s (or its own `timeout_seconds`) is `unmeasured`, never `pass` or `fail`.
Until this layer the candidate's ratchet read it as exit code 127, as upstream's 1.1.0 does, so a floor at or under 127 passed and a ceiling failed on a timeout.

## 3. What it leaves out, and why

| Not at this layer | Why |
|---|---|
| The runner's 3E sentence and the `HANDOFFS.md` seed's paragraph on a run that reads unmeasured gates; `bin/check-handoff`'s lint that enforces them | prose (theme B) and a canonical-only checker (theme F, plan §4): the prose layer carries the sentences, and plan §4's seam note applies, so PR4 states that the lint stays on the fork or carries the one lint |
| `timeout_seconds` on this candidate's own suite gates | decision 1 below |
| The dashboard's mirror of `timeout_seconds` | not built on the fork either (an open call, BL-103) |
| The trimmer, the budget gate, the dashboard, the checkers, `bin/sync`, `bin/status`, `bin/check-links`, `bin/migrate-layout`, the prose | later layers |

## 4. Decisions I took that the plan did not

1. **No `timeout_seconds` on `tests-sh-passed` and `tests-sh-failed`.** The fork declares 3600 on both (and on one more gate) because its gates read `unmeasured` on a loaded machine: its own note measured 794 to
   1,835 s, and 676 s at a load average of about 180, against the 600 s default. This candidate's suite measured **296 s** (load average about 11), about 2 times under the default, so the layer keeps to exactly 1.4.0 and 1.5.0 and adds no
   budget the measurement does not call for. The cost is the other edge: on a machine more than twice as slow, `--run` reads those two gates `unmeasured`, with
   the note `timeout (600 s)`, which is the truthful answer and the one 1.4.0 exists to give. **Reversible with one flag:** `layer2b-build.py ... --ratchet-count 120
   --suite-budget 3600` adds the field to both gates; I ran it on a scratch copy: the manifest has no `config_defects`, `compare` gives 0 refusals and 2 warnings
   (a changed `timeout_seconds` warns, by design). His to overrule; the fork's own 3600 is a separate open call (BL-103).
2. **The three files come from the fork's tip** (`ee48ace`), not from a replay of eight commits: the builder's base assertion makes the result the same as replaying
   `3017741`, `ac85bb8`, `acfbefb`, `c037b48`, `76f0082`, `bf5d122`, `5a50de9` and `1c78a78` onto `26bc97a`, and the tip has no later change to these files
   (`git log 26bc97a..ee48ace -- <the three files>` names those eight and no more). The test commits that the fork wrote RED first are not replayed: layer 2's contrast
   (section 1, item 3) is the evidence that the tests fail without the code.
3. **The test file is verbatim**, with the `ResourceWarning: unclosed file` lines it prints under unittest's default warnings (83 in a run: `open(...).read()` in the
   test file, lines 281 and 1328 to 1336 at the tip). They change no result. Fixing them is a change to a file the fork has verbatim, so it goes in the scrub commit
   or nowhere; I did not take it here.
4. **Scrub input** (a coarse regular expression over the layer's added lines): 9 lines cite `BL-107`, 3 cite `S306`, 2 cite "failure mode #29" (the row exists
   upstream, `SESSION_RUNNER.md` FM #29, so it resolves; the scrub may still drop the number), 2 cite `ITERATIVE_METHODOLOGY.md`, whose sentence ("Automated checks never
   pass by default or by timeout", `:444`) is upstream's. None cites a `docs/planning/` path or a fork learning. The scrub is its own commit after the layers.

## 5. What this does not show

The surface is this machine, with the load average between 8 and 20 across the session: clean clones, serial runs, `nohup` and a done-file (the signal tests ran inside a
`nohup`-launched `--run` and passed, which the fork's own history says is where they failed before its fixes). **Not shown:** Windows, where `HAS_PROCESS_GROUPS` is false
and a timed-out command may keep running (the tests that need groups are guarded, and none ran there); a maintainer's machine; a hook armed in another clone; upstream CI
(there is none); the scanner at 0 (it is 121); the candidate merged with #94 (the conflict list is derived, not resolved); that the fork's own tip behaves as this tree
does (it differs by the prose layer, the lint and the 3600 s budgets).

## 6. Next

**The trimmer layer** (plan §3, third): `starter-kit/methodology_trim.py` and its tests with the resolver block, at the fork's lineage after Part 1's 1.7.0 (the fork's tip is
1.8.0). It is where #94 conflicts, so the first measurement is what the layer does to those two conflicted files. Re-run this layer: `bash layer-verify.sh <candidate>
c8c0b21322e7`; rebuild: `python3 layer2b-build.py <fork> ee48ace <clone-at-fd96593> --ratchet-count 120`. PR2 is now four checkpoints spent of the plan's "two to four" and
the trimmer, the budget gate with the checkers, the dashboard, the sync layers, `bin/migrate-layout`, the prose and the scrub remain, so that figure wants restating at PR4.
