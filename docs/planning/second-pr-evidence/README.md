# Evidence for the second upstream pull request (prepared 2026-10-26, not sent)

The branch is the local branch `feat/trim-session-notes-ledger-issue93` (tip `65990cda`), three commits on `upstream/main`
`d50ce290` after `KJ5HST/methodology` merged pull requests #92 and #94 on 2026-10-24. Its copy on the fork's `origin` is
still the old single commit `8de50d23` on `1670c5d4`, which is not an ancestor of the new tip, so putting the new branch there
is a force-push. Nothing in this folder has been sent anywhere.

| Commit | What | `TRIM_VERSION` |
|---|---|---|
| `39825279` | `SESSION_NOTES.md` joins the ledger table: `8de50d23` replayed onto `d50ce290` (clean cherry-pick) | 1.9.0 |
| `3df5b0cd` | the maintainer's three follow-ups from his 2026-10-24 comment on #94: the entry-less message, the `PREFIX` refusal's reason, three exit-3 statements | 1.9.1 |
| `65990cda` | `FRONTIER_FRONT_MATTER_UNCOMMITTED`: his answer (b), the warning for an uncommitted front-matter edit | 1.10.0 |

Texts: `second-pr-title.txt` and `second-pr-body.md` are the drafts, shown to the operator before anything is posted.

## Measurements and how to repeat them

Every script takes the trimmer under test as an argument (`git show 65990cda:starter-kit/methodology_trim.py > trim_final.py`),
builds its repositories in temporary directories, and is run with `python3 -I`.

| File | What it shows |
|---|---|
| `gate-output-final-65990cda.txt` | `quality_ratchet.py --run` in a clean `--no-local` clone of the tip, hooks set: 12 of 12, results `1b096f787d67`, manifest `9f6dc2ebeb91`. |
| `trimmer-suite-baseline-245-on-rebased-1.9.0.txt` | The trimmer's suite on the rebased first commit alone: 245 tests, OK, 2 skipped, before any change. The tip runs 270. |
| `exit_by_version.py`, `exit-by-version-output.txt` | A proof written by the 1.8.0, 1.8.1 and 1.10.0 trimmers, run in a depth-1 clone (the trim commit's parent absent): exits 1, 3, 3. The basis of the `FRAMEWORK_APPARATUS.md` sentence. |
| `sweep54.py`, `sweep54-output.txt` | `--reverify` of the 54 proofs of the #93 repository at `82433662`, compared row for row with the saved column in `../pr94-response-evidence/adopter-54-sweep-compare.tsv`: 54 of 54 the same, 46 exit 0 and 8 exit 4. |
| `adopter_guard.py`, `adopter-guard-output.txt` | The dry run over 33 ledger files of 11 projects (a twelfth repository is empty): clean clones, then a one-line front-matter edit, then the live working trees read-only. 0 of 33 clean fires, 0 crashes, 15 of 15 reachable synthetic fires, 0 live fires. **The `reached` column only watches for a printed `[DRY_RUN]`; the warning runs before later refusals (for example `ARTIFACT_UNPARSEABLE` on `mts-system`'s notes file), so `fire` is the measure and 15, not the 14 `reached` shows, is the count of runs that got to the check.** |
| `mutate_fm.py`, `mutation-front-matter-warning.txt` | 12 one-expression mutants of `check_front_matter_frontier` and `_regenerated_partner`: 11 killed. M5 (ignore the prefix group) survives and is equivalent: group 1 and group 3 are literal text in every declared pattern. M9 (treat a missing HEAD copy as an empty one) was judged equivalent and not run. |
| `mutate_f1.py`, `mutation-follow-ups.txt` | 4 mutants of the follow-up code: 4 killed. F1c survived until the test asserted on the substitution's own line rather than on the whole output (whole-output text also contained `status: pending`). |
| `adopter-claim-lines-recheck-2026-10-26.tsv` | `../pr94-rewrite/evidence/adopter_claim_lines.py` over the 12 projects' live notes files: the same 3 projects have a finished record that still carries the Phase 1B status line (2 of them dropped the `(IN PROGRESS)` tag); only the newest records of the live projects moved since the saved recheck. |

Not re-run here: the read-only `--check` of 12 projects' notes files (`../pr94-response-evidence/adopter-notes-check-sn-branch.txt`),
which is a statement about the first commit's table entry, unchanged.
