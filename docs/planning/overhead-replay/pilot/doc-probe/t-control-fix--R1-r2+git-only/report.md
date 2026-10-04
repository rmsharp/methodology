I've oriented but haven't changed anything. "go" doesn't name a deliverable, and this project's protocol is to report and wait for you to pick one.

**State of the repo**
- Branch `master`, clean, no remotes. The only side effect is my dashboard run, which created an untracked `dashboard_history.jsonl`. I left it in place.
- The last session was S314, working on issue #121. Its code and test commits are in history: `getPedMaxAge` returning `NA`, the D6 advisory assertion, the NEWS entry, and the test-warnings gate tightened from 7 to 0.
- HEAD (`602a8b5c`, "Restore tracked documentation to its text at the install commit") reverted the S314 close-out docs. As a result:
  - `SESSION_NOTES.md` is back to S313's notes (3.7 MB, so it can't be read whole).
  - `HANDOFFS.md` has no receipts, only the seed sentinel.
  - The S314 CHANGELOG, NEWS and Learning 292 entries are gone.
  - The close-out docs say #121 is still open and the gate is still at 7, while the code and `.quality-gates.json` say otherwise.
- The dashboard shows health 96/100, 0 issues and 0 vulnerabilities. `gh issue list` can't run because there's no remote, so I fell back on `BACKLOG.md` ("Active: none in progress").

**What S313 left as next steps**
- **#121:** appears done in code, but its ledger entries were reverted.
- **#120:** a citations audit. It can start from the Crow & Kimura 1970 and Lacy 1989 citations already in `population_genetics_terms.html`.
- **E4:** rate-of-coancestry Ne, deferred; it needs its own planning pass.
- Others: #103 roxygen harmonization, #116 (blocked), and the CRAN thread (the package was archived 2025-07-29 and the CRAN work is owner-run, a hard stop for me).

**Which one do you want?** My suggestion is to start with the #121 close-out gap: confirm what the HEAD revert was meant to do, then restore or re-record the S314 ledger and receipt if it wasn't intentional. #120 would be the next real deliverable after that.