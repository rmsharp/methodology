# Evidence for the PR #94 rewrite and the 8-of-54 gap (S334, 2026-10-16)

These are the scripts and the saved outputs behind the numbers in [`../body.md`](../body.md) and [`../README.md`](../README.md). Everything here was run on 2026-10-16 against the PR branch tip `972eb2c` and the #93 repository (`rmsharp/nprcgenekeepr`) at commit `82433662`. Nothing here changes this repository, the PR, or the #93 repository.

## Scripts

| File | What it does |
|---|---|
| `sweep.sh` | For each shard in a list: runs the shard's frozen proof as written, then `methodology_trim.py --reverify <shard>` with the trimmer file you name; writes `summary.tsv` (shard, as-written exit, `--reverify` exit) and one output file per run. Checks out `82433662` in the clone (sparse: `docs/archive/` and the three ledgers). |
| `sweep_after.sh` | The `--reverify` half alone, for any trimmer file (used for the prototypes). |
| `stub_survival.py` | For the shards that still fail: finds the pre-trim stub (record 0 at the trim commit's parent) and the finished record that replaced it, and lists the stub's lines that are absent from the finished record. Read-only (`git log`, `git show`). |
| `make_prototypes.py` | Builds the two scratch prototypes from the PR's trimmer: A (a stub marker for `SESSION_NOTES.md`) and A+B (also a recognised stub finalize exits 0, which reverses decision D2). Tested: it reproduces the prototypes the sweeps used, byte for byte. |
| `audit_text.py` | Compares a rewrite of the PR body with the body it replaces: sizes, banned tokens, lost or new figures and code names, the word "red", first-use offsets of key terms, ambiguous-pronoun sentences. A prompt for a reader, not a verdict. |

## Saved outputs

| File | What it shows |
|---|---|
| `sweep-before-after.tsv` | All 54 proofs: exit code as written and under `--reverify` (PR branch). 10 rows differ from 0 as written; 8 stay non-zero. |
| `sweepA.tsv` | `--reverify` exit codes with prototype A: 46 at exit 0, 8 at exit 4. |
| `sweepAB.tsv` | With prototype A+B: 54 at exit 0. |
| `reverify-outputs-10-failing.txt` | The full `--reverify` output for the 10 shards that fail as written (banner, substituted values, the proof's own output). |
| `original-proof-outputs-10-failing.txt` | The original proofs' own output for the same 10, run as written. Each prints exactly one of the three distinguishing failure lines. |
| `stub-survival-output.txt` | Output of `stub_survival.py` for the 8 shards that still fail. |
| `protoAB-test-failures.txt` | The PR's 181 trimmer tests on the unmodified branch (OK) and with prototype A+B (4 fail; they are the tests that assert exit 4 or the label). |
| `sync-test-output.txt` | `bin/sync` from the PR branch against a project holding the #93 repository's edited trimmer: exit 2 without `--force`; "would write" with it (dry runs). |

## Reproduce (from the repository root; `$SCRATCH` is any empty scratch directory)

```
git fetch upstream pull/94/head                                   # makes 972eb2c available
git show 972eb2c:starter-kit/methodology_trim.py > $SCRATCH/trim_pr94.py
mkdir -p $SCRATCH/adopter && cd $SCRATCH/adopter
git clone --filter=blob:none --no-checkout https://github.com/rmsharp/nprcgenekeepr.git repo
git -C repo ls-tree -r --name-only 82433662 | grep 'verify\.sh$' | sed 's/\.verify\.sh$//' > shards.txt   # 54 lines
cd -
bash docs/planning/pr94-rewrite/evidence/sweep.sh "$SCRATCH/adopter/repo" "$SCRATCH/trim_pr94.py" "$SCRATCH/out" "$SCRATCH/adopter/shards.txt"
python3 -I docs/planning/pr94-rewrite/evidence/make_prototypes.py "$SCRATCH/trim_pr94.py" "$SCRATCH"
bash docs/planning/pr94-rewrite/evidence/sweep_after.sh "$SCRATCH/adopter/repo" "$SCRATCH/trim_protoAB.py" "$SCRATCH/outAB" "$SCRATCH/adopter/shards.txt"
python3 -I docs/planning/pr94-rewrite/evidence/stub_survival.py "$SCRATCH/adopter/repo" "$SCRATCH/out"
```

The clone is partial, so the first sweep fetches blobs from GitHub on demand (about ten minutes); later sweeps read the cached blobs (under a minute). To run the PR's tests against a prototype, make a throwaway worktree of `972eb2c`, copy the prototype over its `starter-kit/methodology_trim.py`, run `python3 tools/test_methodology_trim.py`, and remove the worktree.

## Added at S335 (2026-10-16): the build of the fourth commit, `2308553`

Everything below was run on 2026-10-16 against the build worktree at `2308553` (the local branch `fix/trim-verify-false-red-issue93-v2`), the #93 repository at `82433662`, this fork's own frozen shards, and the 12 adopters' live notes files under `~/Development/`. Nothing here changes this repository's tracked files, the PR, or the #93 repository.

| File | What it is |
|---|---|
| `0001-trim-1.8.0.patch` | The build commit `2308553` as a patch (`git format-patch -1`), applicable with `git am` onto `972eb2c`. The branch is local only; this file keeps the change if the branch is lost. |
| `marker_measure.py` / `marker-measure-output.tsv` | The two candidate stub markers (the status line alone; the status line plus the `(IN PROGRESS)` tag) on the #93 repository's seven real stubs and the records that replaced them. Both match all 7 stubs and none of the 7 replacements. |
| `adopter_claim_lines.py` / `adopter-claim-lines-output.tsv` | Every record in the 12 adopters' live notes files that still carries the Phase 1B status line, with its position and whether it keeps the tag: 3 finished records in 3 adopters carry the line, 2 of them without the tag; the other hits are live record-0 stubs. |
| `adopter_check.sh` / `adopter-check-output.txt` | `methodology_trim.py --file SESSION_NOTES.md --check` (read-only) with the 1.8.0 tool on each adopter's notes file: 10 parse, 1 `NO_RECORDS`, 1 `GRAMMAR_MISMATCH`. |
| `mutants_s335.py` / `mutants-s335-output.txt` | The mutation round on the new layer: 17 mutants, 17 killed, the intended test among the failures in every case. Takes the worktree root as its argument. |
| `fork_shards_compare.sh` / `fork-shards-old-vs-new.tsv` | `--reverify` exit codes for this fork's 174 frozen shards under the PR tip's tool (1.7.0) and the build's (1.8.0): identical. |
| `sweep-after-1.8.0.tsv` | `--reverify` exit code for each of the #93 repository's 54 shards under 1.8.0 (`sweep_after.sh`): 46 at 0, 8 at 4. |
| `reverify-outputs-8-labelled-1.8.0.txt` | The full `--reverify` output for the 8 shards 1.8.0 labels exit 4, each with its `DIFF:` block. |
| `trimmer-suite-1.8.0.txt` | `python3 tools/test_methodology_trim.py` at `2308553`: 199 tests, OK, 2 skipped. |
| `tests-sh-1.8.0.txt` / `ratchet-run-1.8.0.txt` | `bin/tests.sh` and `quality_ratchet.py --run` in a clean `--no-local` clone of `2308553` with `core.hooksPath .githooks`: the summaries. |
| `sync-test-1.8.0.txt` | `bin/sync --source local` from the build worktree into a fresh project (byte-identical, 1.8.0), against the #93 repository's edited trimmer (exit 2; `--force` would write), and after a forced sync (the canonical entry reads that repository's notes file as its own entry did). |

Reproduce the build's checks (from the repository root; `$SCRATCH` any empty directory; the clone from the recipe above):

```
git worktree add $SCRATCH/pr94wt fix/trim-verify-false-red-issue93-v2          # or: git worktree add $SCRATCH/pr94wt 972eb2c && git -C $SCRATCH/pr94wt am docs/planning/pr94-rewrite/evidence/0001-trim-1.8.0.patch
(cd $SCRATCH/pr94wt && python3 tools/test_methodology_trim.py)                   # 199 tests
python3 -I docs/planning/pr94-rewrite/evidence/mutants_s335.py $SCRATCH/pr94wt    # 17 killed
bash docs/planning/pr94-rewrite/evidence/sweep_after.sh "$SCRATCH/adopter/repo" "$SCRATCH/pr94wt/starter-kit/methodology_trim.py" "$SCRATCH/outNew" "$SCRATCH/adopter/shards.txt"
python3 -I docs/planning/pr94-rewrite/evidence/marker_measure.py "$SCRATCH/adopter/repo"
```

## Added at S337 (2026-10-17): the build of the fifth commit, `1082d3b`

Everything below was run on 2026-10-17 against a scratch `--no-local` clone at `2308553` (then at `1082d3b`), a fresh partial clone of the #93 repository at `82433662` (`--filter=blob:none`, sparse-checked-out as `sweep.sh` does), and a clean `--no-local` clone of `1082d3b` with `core.hooksPath .githooks`. Nothing here changes the PR: the commit is on the local branch `fix/trim-verify-false-red-issue93` and in the patch below.

| File | What it is |
|---|---|
| `0002-trim-1.8.1.patch` | The build commit `1082d3b` as a patch (`git format-patch -1`), applicable with `git am` onto `2308553`. |
| `bl118-build.py` | The builder: refuses unless the four files it edits are the blobs `2308553` holds, applies exact-once text replacements (the version and its history paragraph, `unfinished(why)` in the template, the test class, the gate, the apparatus sentence), refuses a line over 100 characters, and writes nothing on any refusal. Takes the clone root. Its first run refused on a 102-character line of its own. |
| `bl118-mutants.py` / `bl118-mutants-output.txt` | The mutation round on the new layer: 6 mutants, 6 killed, the intended test among the failures in every case. Takes the worktree root. |
| `trimmer-suite-1.8.1.txt` | `python3 tools/test_methodology_trim.py` at `1082d3b`: 203 tests, OK, 2 skipped, 36 s. |
| `field-case-1.8.0-vs-1.8.1.txt` | The field case on the #93 repository's partial clone with the promisor remote pointed at a dead path: the frozen proof and `--reverify` under 1.8.0 exit 1 (`verify: cannot read 7a55e19^:SESSION_NOTES.md`); `--reverify` under 1.8.1 exits 3 with the same reason and no `FAIL:`; the frozen proof's bytes are unchanged and it still exits 1. Four runs with their exit codes. Needs an uncached parent blob: run it before a sweep (a sweep caches the blobs) or on a fresh partial clone. |
| `sweep-after-1.8.1.tsv` | `--reverify` exit code for each of the 54 shards under 1.8.1 (`sweep_after.sh`): 46 at 0, 8 at 4, identical row by row to `sweep-after-1.8.0.tsv`. |
| `tests-sh-1.8.1.txt` / `ratchet-run-1.8.1.txt` | `bin/tests.sh` (261 passed, 0 failed) and `quality_ratchet.py --run` (12/12 pass · 0 fail · 0 unmeasured (results `cb7ffb255deb`, manifest `072b6ca7f1a0`; `trimmer-unit-tests` measured 203 against 203; 3 min 5 s at a load of 7.6 to 8.6)) in a clean `--no-local` clone of `1082d3b` with `core.hooksPath .githooks`: the full outputs. |

Reproduce (from the repository root; `$SCRATCH` any empty directory; the #93 clone from the recipe above):

```
git clone -q --no-local . $SCRATCH/pr94c && git -C $SCRATCH/pr94c checkout -q 2308553 && git -C $SCRATCH/pr94c config core.hooksPath .githooks
python3 -I docs/planning/pr94-rewrite/evidence/bl118-build.py $SCRATCH/pr94c           # 4 files edited, nothing committed
(cd $SCRATCH/pr94c && python3 tools/test_methodology_trim.py)                          # 203 tests
python3 -I docs/planning/pr94-rewrite/evidence/bl118-mutants.py $SCRATCH/pr94c          # 6 killed
(cd $SCRATCH/adopter/repo && git remote set-url origin /nonexistent/promisor && python3 -I $SCRATCH/pr94c/starter-kit/methodology_trim.py --reverify docs/archive/SESSION_NOTES-through-2026-09-26-2.md; echo exit=$?; git remote set-url origin https://github.com/rmsharp/nprcgenekeepr.git)   # exit=3 while the parent blob is uncached
bash docs/planning/pr94-rewrite/evidence/sweep_after.sh "$SCRATCH/adopter/repo" "$SCRATCH/pr94c/starter-kit/methodology_trim.py" "$SCRATCH/out181" "$SCRATCH/adopter/shards.txt"   # 46 at 0, 8 at 4
```

## Added at S338 (2026-10-18): BL-119, the fifth commit's change on fork `main` and on the candidate

The same fix as `1082d3b` (the proof's abort before its checks exits 3, not 1; `TRIM_VERSION` 1.8.1) ported onto the layout trimmer: fork `main` `5f09130` and the candidate `pr2/candidate` `3cba1e5` (its 34th commit). The record is `docs/planning/pr-composition-evidence/bl119-record.md`; the claims run on the candidate and decision 3's figures are `bl119-claims-output.txt`, `bl119-decision3.sh` and `bl119-decision3-output.txt` in that directory. The `main` outputs were saved by the session that claimed BL-119 on 2026-10-17, in a scratch clone that is gone; S338 reproduced them on 2026-10-18 in fresh clones (the mutant output and the sweep byte for byte, the suite but for its timing line).

| File | What it is |
|---|---|
| `bl119-build.py` | The builder for a tree that carries the layout trimmer: refuses unless the four files are the blobs of the pinned commit, copies the new text blocks out of `bl118-build.py` as text, applies exact-once replacements (and the one edit `1082d3b` did not need, the template pin's mapping of the abort block), refuses a line over 100 characters, writes nothing on any refusal. `python3 bl119-build.py <clone-root> <pinned-commit>`. |
| `bl119-mutants.py` | The mutation round: 9 mutants one at a time (the first six are `bl118-mutants.py`'s; then a template byte outside the abort block, one inside it, and one the pin normalises away, which must survive), the trimmer restored byte for byte. `python3 bl119-mutants.py <clone-root>`. |
| `bl119-field-case.sh` | The depth-1 clone procedure as a script: the frozen proof, then `--reverify` under the old and the new trimmer. `bash bl119-field-case.sh <label> <repo> <shard> <old-trimmer> <new-trimmer> <scratch-dir>`. |
| `fork_shards_compare.sh` | (Changed.) An optional 5th argument names the repository to sweep, so the sweep can run in a clean clone while the live tree takes commits. |
| `bl119-main-trimmer-suite-1.8.1.txt`, `bl119-candidate-trimmer-suite-1.8.1.txt` | `python3 tools/test_methodology_trim.py`: 222 tests OK, 2 skipped, on each tree. |
| `bl119-main-mutants-output.txt`, `bl119-candidate-mutants-output.txt` | 8 killed (each by its intended test), 1 survived as meant, 0 invalid, 0 unexpected, of 9; the two files are byte-identical. |
| `bl119-main-field-case-1.8.0-vs-1.8.1.txt`, `bl119-candidate-field-case-1.8.0-vs-1.8.1.txt` | Frozen proof 1; `--reverify` under 1.8.0 1; under 1.8.1 3, the same reason text and no `FAIL:`. |
| `bl119-main-fork-shards-1.8.0-vs-1.8.1.tsv`, `bl119-candidate-archived-piece-1.8.0-vs-1.8.1.tsv` | `--reverify` exit under each version: 177 pieces on `main`, equal in every row (172 at 0, 2 at 1, 2 at 3, 1 at 4); the candidate's one piece 0 and 0. |
| `bl119-main-gate-output.txt` | `layer-verify.sh` on `5f09130` in a clean clone: ratchet 18/18, 0 unmeasured, results `51eb96ff6a98`, manifest `7e1f0d1576e4`; 23 min 1 s. |

Reproduce on `main` (from the repository root; `$SCRATCH` any empty directory):

```
git clone -q --no-local . $SCRATCH/m && git -C $SCRATCH/m checkout -q 6907c53
python3 -I docs/planning/pr94-rewrite/evidence/bl119-build.py $SCRATCH/m 6907c53    # 4 files edited, nothing committed
(cd $SCRATCH/m && python3 tools/test_methodology_trim.py)                            # 222 tests
python3 -I docs/planning/pr94-rewrite/evidence/bl119-mutants.py $SCRATCH/m           # 8 killed, 1 survived as meant
```
