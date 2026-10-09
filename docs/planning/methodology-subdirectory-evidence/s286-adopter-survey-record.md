# S286 — the adopter survey (BL-101, plan section 7.4: "tier 1 until it is surveyed")

Read-only. Nothing was written in any adopter and nothing went upstream. Instrument:
`s286-adopter-survey.py`; its output `s286-adopter-survey-output.txt`; every matching line of every machine-read candidate
`s286-adopter-lines.txt` (prose is counted, not quoted: some adopters are private); the control `s286-control-output.txt`; the shell
suite after the trim `s286-suite-after-trim.txt`. **Every revision is pinned** (section 7): the adopters are live repositories.

## 1. The result

Of the 11 adopters other than `model_project_constructor`, **10 have commits and were surveyed; `claude_work` has none**
(0 tracked files, its methodology files untracked, so `bin/migrate-layout` refuses it and there is nothing to survey).
The instrument names **25 machine-read files** (a test, script, proof, CI, hook or config that is not a comment and
carries a moved file's exact name). I read every one of the 25 and the three `.qmd`/`.Rmd` files it classes as prose.
**15 read a moved path by name; 10 are text** (a message, a docstring, a URL, a fixture, an unrelated file of the same name).

| Adopter (surveyed rev) | tracked | named | reads a moved path | tier 1 touches it? | what tier 2 does to it |
|---|---|---|---|---|---|
| `feedback-loop-comparison` (`cda76db`) | 33 | 0 | 0 | no | nothing found |
| `airqino` (`998cd51`) | 72 | 1 | 0 | no | `app.py` renders its own `templates/dashboard.html`, not the generated root file |
| `Philippians` (`427e634`) | 123 | 1 (+1 weak) | 0 | no | both are docstrings |
| `vscode_quarto_ext` (`507b934`) | 430 | 2 (+15 weak) | 0 | no | message text; the 15 weak are `CHANGELOG: <entry title>` citations in test names |
| `chat_verification` (`107cbed`) | 36 | 1 | 1 | no | `.githooks/pre-commit` **fails open** (plan C5, already measured) |
| `church_growth` (`3035560`) | 42 | 1 | 1 | no | same hook, same failure (C5) |
| `dalia_martinez_funeral` (`5cd7b91`) | 32 | 1 | 1 | no | `bin/check-handoff` (an older copy): no root `HANDOFFS.md`, so `error: handoff file not found`, exit 1 (**loud**) |
| `mts-system` (`d1cf54f`) | 738 | 3 | 1 | no | `scripts/learnings_archive.py` reads `.context-budget.json` from `--root`, default the repo root; its own docstring says exit 2, "the root cannot be read" (**loud**). Its test builds temporary roots; `deploy_vps.sh` only lists `--exclude` names |
| `wsfct` at `master` (`adba306`) | 2,711 | 6 | 2 | no | `web/scripts/archive-session-notes.ts` and `fold-stale-pr.ts` default to `../../SESSION_NOTES.md` (**loud**). `docs/archive/session-notes/` is the project's own and stays |
| `nprcgenekeepr` (`6302757`) | 1,534 | 9 (+1 weak) | 9 | **yes** | see section 3 |
| `claude_work` | 0 | n/a | n/a | n/a | the tool refuses: no commit |

`wsfct` is checked out on `docs/s698-storage-write-design`, not its default `master`; the survey read `master`
(`--rev wsfct=master`), and the feature branch names the same 6 files. The dirty and upstream figures in the output describe the checked-out tree when the survey ran, not the pinned revision. Working trees
are not all clean (the tool refuses a dirty one): `airqino` 4 untracked (three are generated ledger files), `dalia_martinez_funeral` 6, `Philippians` 4 modified
sermon files, `chat_verification` and `mts-system` a modified `dashboard_history.jsonl`, `church_growth` a `__pycache__/`,
`vscode_quarto_ext` a `scratchpad/`; `feedback-loop-comparison`, `nprcgenekeepr` and `wsfct` are clean.

## 2. The instrument, and what its control showed

It lists the tracked files at one revision that name a file `bin/migrate-layout` moves (read from the tool's own
tables), classifies each by path, and ignores comment-only lines. **Control:** `model_project_constructor` at `0dc3051`,
its tree before the move, where S285's CI measured what breaks (`tests/test_read_budget.py`,
`tests/test_session_notes_census.py` and two proofs). **Pass criterion, fixed before the run: all four found with their tiers.**
Result: **4 of 4** (`s286-control-output.txt`).

**The control also bounds what a hit means.** It named 25 machine-read files; 4 broke. The other 21 include 11 shard
proofs carrying the same `LIVE = "SESSION_NOTES.md"` line as the 2 that broke, because those 11 read the ledger at an old
commit through git, which a move cannot touch. **A name on a code line is necessary, not sufficient**, and no static search
separates a reader of the live file from a reader of history. So the 15 above are files that read a moved path by name,
an upper bound on the breaks that come from a literal name (a path built in pieces, or an untracked file, is not seen). A zero is the strong result. The instrument was changed after the first control run, so those
changes are not tested out of sample: the bare word `dashboard` and the token `-through-` were dropped as names, comment-only
matches are ignored, `.gitignore` is counted as tool-handled, and names are split into exact file names (strong) and stems
(weak). They cut the control's further machine-read files from 29 to 21, and none can remove one of the four (each has a
code line carrying a strong name).

Audit of the zeros: `feedback-loop-comparison`'s `index.qmd` has no executable chunk, and the `.qmd`/`.Rmd` token lines in
`nprcgenekeepr` are captions and labels (`#| fig-cap`), not reads. No adopter has a proof naming a ledger (proof kind: 0
candidates in all 10), so the control's main false-positive family does not recur here; the shard proofs under
`docs/archive/` are excluded because `bin/migrate-layout` already rehearses them (`rehearse_shards`).

## 3. `nprcgenekeepr`, the one with many

All 9 named files read a moved path by name. **Tier 1** (the framework files move): the four push workflows' `paths-ignore`
lists (identical, md5-checked; 21 entries: 17 moved files' names, 3 that stay, `docs/**`) stop matching the moved framework
files (the plan's C11 knew); **`.Rbuildignore`** ignores them by per-file regex and `^docs$`
(`^SESSION_RUNNER.*\.md$`, `^methodology_trim\.py$`, ...), so files under `methodology/` match none of it and no pattern
would ignore that directory (the plan text does not name `.Rbuildignore`; the tool's P7 report
`p7-adopter-runs/reports.json` lists it); `test_rbuildignore.R` asserts that a pattern matches the bare name
`methodology_trim.py`, so it stays true while the real file is unprotected. **Tier 2** (the ledgers move):
`test_handoffsReceiptPlacement.R` does `skip_if_not(file.exists(HANDOFFS.md))`, so it **skips** (a rise in skips is a
failure by S285's rule); `vignettes/articles/data-raw/build-document1-evidence.R` reads `CHANGELOG.md`, `HANDOFFS.md` and
`SESSION_NOTES.md` by bare name and fails when run; `test_workflowPathsIgnore.R` hard-codes the names at `:38-44`.
**Not shown:** whether a package-build NOTE fails its `R-CMD-check` (the workflow sets no `error-on` in the lines read), and
what any of this does when run. One weak hit, `renv/activate.R`, is the English word "bootstrap".

## 4. What was already known, and what is new

**Confirms the plan:** C5 (the two adopters' older ledger hooks fail open once the ledger leaves the root: both are armed,
`core.hooksPath=.githooks`, and each ends `if ! git ls-files --error-unmatch CHANGELOG.md ...; then exit 0`), and C11
(`nprcgenekeepr`'s CI filter). **Not in the plan text:** the count for the other adopters (S285 said "unknown"); a copy of the canonical `bin/check-handoff` in
`dalia_martinez_funeral`, `scripts/learnings_archive.py` in `mts-system`, the two TypeScript scripts in `wsfct`, and
`nprcgenekeepr`'s `.Rbuildignore` and `data-raw` script. **The tool saw only two of them:** its P7 dry-run reports
(`p7-adopter-runs/reports.json`) list `bin/check-handoff` and `.Rbuildignore` among the `other` sites they show, and not the
other three files, because `scan_hits` (categories `ci`, `harness`, `hooks`, `ledger`, `other`) lumps tests, scripts and proofs
with prose in `other` and shows 25 sites a category (`other` held 33 files for `mts-system`, 59 for `wsfct`, 119 for
`nprcgenekeepr`), and it does not say which names are read as paths. That is S285's follow-up (4), now with a measured sort to build from: this script's `kind_of`.

## 5. What this leaves to him (not decided here)

1. **Tier for P12 and after.** The condition he set at S285 (tier 1 until each adopter is surveyed) is now met for 10 of
   11. By this survey, tier 1 touches only `nprcgenekeepr`; `feedback-loop-comparison`, `airqino`, `Philippians` and
   `vscode_quarto_ext` have no file that reads a moved path, so tier `all` there depends on the adopter's own CI in a clone,
   not on a repair; `chat_verification` and `church_growth` need their hook replaced by the layout-aware one before tier 2;
   `dalia_martinez_funeral`, `mts-system` and `wsfct` need one or two script paths changed.
2. **The order in plan 7.4.** It lists `nprcgenekeepr` third "by risk" (after `model_project_constructor`, done, and
   `feedback-loop-comparison`); by this count it is the riskiest of the 11.
3. **Whether to build the tool follow-up** (separate tests, scripts, proofs, CI and hooks from prose in the dry run).

## 6. Not shown

The committed trees only (untracked and ignored files are not seen); no adopter's test, proof or CI was run, so no name here
is shown to break, and "fails open", "loud" and "skips" above are my reading of the code, except C5, which the plan measured; the control is one adopter; `claude_work`'s untracked `analyze_repo.py` is outside the surface;
unpushed commits exist in `mts-system` (43), `nprcgenekeepr` (49) and `vscode_quarto_ext` (249), and the survey read local
commits, not `origin`. **`nprcgenekeepr` has a session of its own running** (its `44d5786`, "S947 claim", landed during this one and
touches only its three ledgers, so no result here changes): P-step work there needs that session's owner.

## 7. Reproduce

    python3 -I docs/planning/methodology-subdirectory-evidence/s286-adopter-survey.py --control
    bash -c 'python3 -I docs/planning/methodology-subdirectory-evidence/s286-adopter-survey.py --lines /tmp/lines \
      --rev airqino=998cd51 --rev chat_verification=107cbed --rev church_growth=3035560 --rev dalia_martinez_funeral=5cd7b91 \
      --rev feedback-loop-comparison=cda76db --rev mts-system=d1cf54f --rev nprcgenekeepr=6302757 --rev Philippians=427e634 \
      --rev vscode_quarto_ext=507b934 --rev wsfct=master'

`wsfct=master` is `adba306` today; use that sha to pin it. The control is pinned in the script (`0dc3051`).
