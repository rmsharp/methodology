**Orientation report (Phase 0).** I haven't started any work, because "go" didn't name a task and the protocol says to wait for one.

- **Branch and state:** `master` (the main branch is `main`). The tree is clean apart from an untracked `dashboard_history.jsonl`, which my dashboard run created. S314 left the same file untouched. There is no git remote.
- **Last session (S314, 2026-09-30):** Finished issue #121. `getPedMaxAge()` now returns `NA` instead of `-Inf` plus a warning when no ages exist, which fixed the 5 `test_modPyramid.R` warnings. The 2 `gvaConvergence` warnings are the deliberate >0.5 kinship override, and that test now asserts the warning. The commits are `7aab006c`, `ff261655`, `0d23637e`, `0a121159` and `aeebcdec`.
- **Open issues:** `gh issue list` fails with "no git remotes found", so I'm working from the S314 handoff. I didn't read `BACKLOG.md`.
- **Ghost sessions and ledger:** None found. The `CHANGELOG.md` and `HANDOFFS.md` frontiers are both `aeebcdec` (HEAD), so there are 0 undocumented commits. The newest `HANDOFFS.md` receipt says `status: complete`, so no backfill was needed.
- **Dashboard:** Health 96/100, 0 high-or-above risks, 0 vulnerabilities, 1,805 commits.
- **Build status:** I haven't run a build. S314 reported the full suite at `FAIL 0` and `R CMD check --no-manual --ignore-vignettes --no-tests` at Status OK.
- **Environment:**
  - **`Rscript --vanilla`:** Use it with `NOT_CRAN=true`, because the renv lockfile packages aren't restored here.
  - **`test_getVersion.R`:** It fails under that setup. This is known baseline noise, so don't chase it.
  - **Edit `NEWS.Rmd`, not `NEWS.md`.**

**Candidates for this session's one deliverable** (from S314's SUGGESTED NEXT):
1. **#121 close-out.** It's fixed but still open on GitHub, and I can't close it without a remote. Nothing to do unless you add one.
2. **#120:** Citations audit, starting from the Crow & Kimura 1970 and Lacy 1989 citations in `population_genetics_terms.html`.
3. **#40:** Strengthen the shinytest2 E2E assertions and CI stability.
4. **#103:** roxygen harmonization.
5. **Smaller or deferred:** #37, #36, #28, #12, #11, #10, #5, and the E4 rate-of-coancestry Ne work. #116 is blocked, and the CRAN thread is a hard stop for you to run.

Which one do you want? I'll state the deliverable back and claim the session before touching anything.