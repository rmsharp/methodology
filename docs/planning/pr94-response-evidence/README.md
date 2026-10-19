# Evidence for the response to the maintainer's comment on PR #94 (2026-10-19)

The package that explains these files is [`../pr94-response-2026-10-19.md`](../pr94-response-2026-10-19.md). The scripts take a trimmer file and the PR's test module (for its fixture helpers `make_handoff_repo`, `make_repo`, `run_trim`, `sh`) as arguments, override the module's `TRIM_PY`, and build every repository in a temporary directory, so one script gives a "before" reading against `1082d3b` and an "after" reading against `pr94-r2`:

```
git worktree add --detach /tmp/pr94-head 1082d3b                      # a checkout of the head the maintainer reviewed
git show pr94-r2:starter-kit/methodology_trim.py > /tmp/after.py       # the fixed branch's trimmer
python3 -I point1_removed_ledger.py /tmp/pr94-head/starter-kit/methodology_trim.py /tmp/pr94-head/tools/test_methodology_trim.py   # before
python3 -I point1_removed_ledger.py /tmp/after.py /tmp/pr94-head/tools/test_methodology_trim.py                                    # after
```

The tests module must be loaded from a checkout (its fixture paths resolve against the checkout's `tools/` and `starter-kit/`); only its helpers are used.

Run each with `python3 -I`. The `.py` helpers here (`mutate.py`, `excise_sn.py`, `build_sn.py`, `make_pr94_body.py`) were written to build the two branches and the description; they assert every anchor they edit, and are kept so the build can be audited, not as tools.

## Scripts and their saved outputs

| Script | What it shows | Saved output |
|---|---|---|
| `point1_removed_ledger.py` | Point 1: a trim commit that also `git rm`s the live ledger, proof exit code. | `point1-output-before.txt` (1.8.1 exit 3; 1.5.0 exit 1), `point1-output-after.txt` (exit 1) |
| `point2_planted_module.py` | Point 2: a planted `difflib.py` and `subprocess.py` at the repository root; which ran, in the frozen proof and under `--reverify`. | `point2-output-all.txt` (1.5.0, the PR head, the fixed branch) |
| `verify_points.py` | Points 4a, 4b, 5, 6, 7, 8, each on a throwaway repository. | `verify-points-output-before.txt`, `verify-points-output-after.txt` |
| `point3_session_notes.py` | Point 3: a 123,325 B notes file under `context_budget.py` and `--check`; headings the pattern does not match. | `point3-output-before.txt` (PR head), `point3-output-sn-branch.txt` (with the entry) |
| `finding_history_walk_failure.py` | The extra finding: a failed `git log` walk reads as "not committed yet" and the proof prints `OK`. | `finding-history-walk-output-before.txt` (1.5.0, 1.8.1 and the pre-fix branch all print OK), `finding-history-walk-output-after.txt` (exit 3) |
| `probe_untested.py` | The three things the maintainer did not test: backtracking, symlinks, repo-local git config. | `probe-untested-output.txt` |

## Measurements on real repositories

| File | What it is |
|---|---|
| `adopter-54-sweep-compare.tsv` | The 54 proofs of `rmsharp/nprcgenekeepr` at `82433662`: exit code as written, then `--reverify` under `1082d3b`, under `pr94-r2` and under `pr94-sn`. Columns: shard, exit as written, `--reverify` under `1082d3b`, under `pr94-r2`, under `pr94-sn`. As written 44 pass and 10 fail (the maintainer's figure); `1082d3b` reads 46 at exit 0 and 8 at exit 4 (also the maintainer's); `pr94-r2` reads 46 at exit 0, 1 at exit 4, 7 at exit 1; `pr94-sn` is identical to `1082d3b` row for row. |
| `adopter-head-prefix-shards.txt` | The two proofs with `PREFIX = "../"` at that repository's HEAD: as written, under `1082d3b`, under `pr94-r2`. |
| `fork-179-shards-reverify-1.7.0-vs-1.8.2.tsv` | The 179 of this fork's 181 shards that have a proof (the other 2 are early hand-made shards with none; both trimmers read them at exit 3): as written, `--reverify` under 1.7.0, under `pr94-r2`. No row differs between the last two. |
| `adopter-claim-lines-recheck.tsv` | `adopter_claim_lines.py` re-run over the 12 projects' live notes files; compare with `../pr94-rewrite/evidence/adopter-claim-lines-output.tsv` (only the live projects' newest records moved). |
| `adopter-notes-check-sn-branch.txt` | Read-only `--check` of the `pr94-sn` trimmer over the 12 projects' notes files: 10 parse, 1 fresh seed, 1 refused by name. |

## Gates and mutation rounds

| File | What it is |
|---|---|
| `gate-output-pr94-r2-1670c5d.txt` | `quality_ratchet.py --run` in a clean `--no-local` clone of `pr94-r2`: 12 of 12, results `b49e29a9e5ea`, manifest `06181a10ec42`. |
| `gate-output-pr94-sn-8de50d2.txt` | The same for `pr94-sn`: 12 of 12, results `e56bb08a3c66`, manifest `c9460f6eeb2e`. |
| `mutation-rounds.txt` | Every mutation round run today, mutant by mutant, with the first failing test; the three survivors are the maintainer's M1 before its tests existed and the equivalent M7 (before and after). |

## Texts

| File | What it is |
|---|---|
| `reply-comment.md` | The reply to the maintainer's comment (a draft until sent). |
| `pr94-new-title.txt`, `pr94-new-body.md` | PR #94's title and description after the rebuild; `make_pr94_body.py` derives the body from `../pr94-rewrite/body.md`. |
| `sn-pr-title.txt`, `sn-pr-body.md` | The second pull request (the `SESSION_NOTES.md` entry). |
| `session-notes-entry-original.patch` | `git diff 9a4bf79 1082d3b`: the rebuilt commit 5 against the original head. It is the notes entry **and** the edits to my own rebuilt commits, so it is a record of the split, not a patch to apply; `build_sn.py` extracts the entry from the original commits instead. |
