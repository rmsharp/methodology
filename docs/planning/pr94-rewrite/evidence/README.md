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
