# Saved runs of the documentation study: the evidence (BL-94 P1a (a))

Everything the plan's later phases score is in this directory, because the run trees under `/tmp` are deleted at the next reboot.
**`runs.bundle`** is one git bundle holding every saved run as a ref (`refs/runs/<id>`, the run's HEAD, and `refs/pins/<id>` where the
pinned end sha is not HEAD). Its prerequisites are the project's own start commits, which are in the `nprcgenekeepr` repository, so
every sha a run's record cites is preserved. **`manifest.json`** lists each run with its start, install commit, head, pin, commit
count, the CLI version read from its transcript, its uncommitted state, and the tree path it was taken from (perishable, kept only as
provenance).

| Set | What it is | Start | Runs | CLI version (from the transcript) |
|---|---|---|---|---|
| `real-3.7` | S237, issue #121: v3.0 and v3.7 arms | `879503cce` | 13 | 7 on 2.1.285, 6 on 2.1.286 |
| `t-control` | ratchet study T-control, issue #121: R0 and R1 (v3.8 text), old close-out reply | `879503cce` | 8 | 8 on 2.1.287 |
| `t-control-fix` | ratchet study T-control, issue #121: R1 with the fixed close-out reply | `879503cce` | 5 | 5 on 2.1.287 |
| `t-remove` | ratchet study T-remove: v3.0, R0 and R1 | `402a6b5b7` | 15 | 8 on 2.1.286, 7 on 2.1.287 |

**41 runs, 851,479 B** (the plan's limit for keeping them in git is 5 MB). The CLI version is not constant inside a
set: S237's runs straddle 2.1.285 and 2.1.286, the ratchet study's T-remove runs 2.1.286 and 2.1.287. It is a covariate, not a control.

**Pinned end shas** (plan 2.5: the first close-out commit; HEAD for every run except):
- `real-3.7/v3.7-r2`: pin `7b9bd618`, HEAD `b7e1acf4` (18 commits after the start)
- `real-3.7/v3.0-r3`: pin `b15ae1c5`, HEAD `2a6ea695` (5 commits after the start)
- `t-remove/R0-r5`: pin `3aa6c2b9`, HEAD `5ccafa0a` (9 commits after the start)

**What a bundle cannot carry: uncommitted work.** Every tree was checked. 38 of 41 have no tracked file modified and only an untracked
`dashboard_history.jsonl` (a tool's output, not a record). The other 3 have tracked files edited and never committed, and are the
runs cut off before any close-out:
- `real-3.7/v3.7-r1` (cut off after 4 stops): `BACKLOG.md`, `NEWS.Rmd`, `NEWS.md`, `PROJECT_LEARNINGS.md`
- `real-3.7/v3.0-r2` (cut off after 8 stops): `SESSION_NOTES.md`, `tests/testthat/test_gvaConvergence_kinshipOverrides.R`, `tests/testthat/test_modPyramid.R`
- `t-control-fix/R1-r1` (cut off after 10 stops): `CHANGELOG.md`, `PROJECT_LEARNINGS.md`

**Rebuild and check** (needs only this directory and the project repository; `--project` defaults to `~/Development/nprcgenekeepr`):

    python3 docs/planning/overhead-replay/doc_evidence.py verify docs/planning/overhead-replay/pilot/doc-evidence

To read a run: in a clone of the project, `git fetch runs.bundle 'refs/runs/*:refs/runs/*' 'refs/pins/*:refs/pins/*'`, then
`git show refs/runs/<id>:HANDOFFS.md`. The install commit is the one by author `Fixture` with the subject `Install methodology arm ...`;
it is in the bundle, not in the project repository, which is why the bundle's range starts at the project's own commit.

**What is not copied out.** The final documentation files are in the bundle (the notes file alone is 3.85 MB per run and the bundle holds
every version of it in 851,479 B). The harness's `rows.jsonl` and S237's transcripts stay in `pilot/`; the other
transcripts are under `~/.claude/projects/` (`cleanupPeriodDays` 365) and named in each manifest row. Three runs reached no close-out
(`real-3.7/v3.7-r1`, `real-3.7/v3.0-r2`, `t-control-fix/R1-r1`: each ended at the driver's stop limit, the last with a claim commit,
two work commits and a pending receipt); they are kept, and the inclusion rule (plan 2.5) decides what is scored.
