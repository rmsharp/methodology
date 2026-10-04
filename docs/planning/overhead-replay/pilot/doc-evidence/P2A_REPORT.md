# P2a report: the cold-start probe is built (BL-94, S258, 2026-10-04)

**Cost: $0. No model session was launched, no rating call was made, nothing outside `docs/planning/` changed, nothing was sent upstream.**
The plan is [`documentation-quality-experiment-plan.md`](../../../documentation-quality-experiment-plan.md) §5 P2a; the harness is in
[`overhead-replay/`](../..). P2a ends in a stop for the operator, because the P2 spend is his (D4); §7 below lists what he is asked.

## The answer

1. **The probe works against a fake `claude` and rebuilds every saved end state from the real bundle.** `probe.py` rebuilds a run's end
   state from the evidence bundle into a fresh repository (the pinned commit and its ancestors only), optionally applies the
   **git-only control**, runs one `claude -p` turn with the operator's own `go`, and records one spend line and one row.
   `tests_probe.py`: 43 tests; `mutants_p2a.py probe`: 35 of 35 mutants killed. **Pre-flight on the real bundle** (`p2a-preflight.txt`):
   all 41 runs behave as expected: 38 rebuild as end state and as control with HEAD equal to the pinned sha, 3 are refused by design
   because they ended with tracked edits the bundle cannot carry.
2. **A probe should cost about a third of what the plan assumed.** The saved runs also opened `go`, so their first stop is the same turn
   on the start state: **$0.24 (v3.0), $0.38 (v3.7), $0.38 (v3.8-text); mean $0.35, highest $0.51**, against the plan's guess of $1.
   That is the original sessions' first turn, not a probe (§3).
3. **The R suite takes 2 minutes** (120.8 s at `879503cce`), so M1 (d) can re-run it on every scored end state (about 46 minutes for 23)
   with no sample.
4. **There is no M3 task in the project's history.** 56 commits remove a function; none makes two parsed-or-agent live documents false
   in a way the commit also fixed. **One constructed task exists on the start state the study already uses** (rename `getEmptyErrorLst`),
   which is a design and a cost, not a search result.
5. **The operator's blind packet is large: 33,592 words in ten records, about 2.8 hours of reading at 200 words a minute.** The plan said
   this was untimed. He chose at the Phase 1 picker to have the model rater built as well as his own rating.

## 1. Item (a): the driver mode, tested before any real launch

`probe.py RUN_ID --session-cap S --total-cap T [--control git-only]`. In order, and a refusal at any step stops the run before the next:
the spend check (`spent + session cap > total cap` refuses, as the driver does; **both caps are required**, so a total is never read
without its per-session cap); the CLI check (every long flag the driver passes must still be in `claude --help`: a dropped flag would
otherwise cost a launch to find out); the bundle rebuild (`doc_evidence.rebuild` checks the bundle against the project and every run's
head and pin against the manifest); the clone (the pin is fetched by ref and compared with the manifest's sha before checkout; no
remote; install commit an ancestor; a later commit of the original session absent; tracked tree clean); the control, if asked; the
one-turn session through `driver.drive` with `max_stops=1`; the ledger line, the stream log, the report text and the row.
`--no-launch` stops before the session and spends nothing. `--verify-all` is the $0 pre-flight over the whole bundle.

* **Tests:** `tests_probe.py`, 43 tests, synthetic repositories and a stand-in process. They cover the one-turn contract (one message,
  `go`, in the clone), the saved report being the *last* result's text, a budget stop, an error that carries text, a process that exits
  silently, one that dies, a CLI that cannot start, a success at the cap, the command line (`--max-budget-usd`, isolation flags), the
  pin-before-head case, a manifest sha the pin ref does not hold, every refusal, the control (record files back to the install text, code
  untouched, one commit on the pin, a record file the session added removed) and `--verify-all`. The plan puts them in `tests.py`; they are
  their own file, as `tests_doc_evidence.py` and `tests_p1b.py` are, so they run alone in under 30 seconds and can be run against mutants.
* **Mutants:** `mutants_p2a.py probe` applies 35 one-line mutations to a copy; its first run left three alive (the CLI check, the clone
  check and the stop count in `run_probe`), each answered with a test, and a later run left one alive because a new guard masked it,
  answered with a cheaper fake. **The final run killed all 35** (before a comment-only edit to `probe.py`).
* **Real data:** `python3 probe.py --verify-all` (about 14 minutes, $0). Table in `p2a-preflight.txt`.
* **A bug the tests found in my own draft:** a process that died before reading could raise `BrokenPipeError` out of `driver.drive`
  after the clone was built; `run_probe` now records it as a failed probe with cost 0. Whether the write hits a closed pipe is a race, so
  the test accepts either ending and a second test injects the `OSError`.
* **The git-only control is one commit on the pin** (subject `Restore tracked documentation to its text at the install commit`), so
  every session sha still resolves and the key's deliverable sha still names a commit. The commit is visible in `git log`: a named
  confound, equal in every arm. Record files are those `doc_score.is_record_path` says (`.md` and the like, not code, tests, `man/`, JSON).

**What a probe cannot carry** (named in every row): uncommitted and untracked files (the 3 runs with tracked edits are refused),
the arm's git hook (R1 end states lose it), and the original `.git/config`.
**STOP conditions the plan names, checked:** a bundle that cannot rebuild its sha: none (41 of 41 as expected). A driver behaviour the
fake cannot reproduce: **none found, one guarded.** Of the 56 saved rows, 47 end at a close-out, 8 are cut off at the stop limit and
**one hit the cap**: S237's `xhigh-go` pilot, HEAD rep 1, ended `result error_max_budget_usd` at **$2.0389 on a $2.00 cap**. So the
fake's budget stop has the real shape, and the CLI overshoots a cap by a little: a cap is approximate, and `spent + cap <= total`
bounds the ledger only to within that overshoot. Should a cap stop ever come back as an ordinary success the report would be cut short
and look whole, so a cost at 98% of the session cap is a failed probe whatever the result says (`cap_hit`).

## 2. Item (b): the R suite, timed once

120.8 s wall at `879503cce`, a plain clone, 12 CPUs, load average 8.0 falling to 5.6 (a busy machine, so a quiet one may be faster). `passed=3734 failed=1 warnings=7 files=252`: the ratchet study's figures for this commit, reproduced. An end
state has more test files, so expect a little more. `p2a-suite-time.json`.

## 3. Item (c): the probe's cost, from the saved runs

`probe_budget.py` reads each scored run's first `result` message in its stream log (cost and turns at the Phase 0 stop) and its
transcript's first turn (tool calls, files read, characters returned). 22 of 23 scored runs have both; `v3.7-r2` has no stream log.

| Arm | n | First-stop cost (mean, range) | Turns | Shell commands | Framework KB read | Record KB read |
|---|--:|---|--:|--:|--:|--:|
| v3.0 | 5 | $0.240 (0.222-0.264) | 12.2 | 5.2 | 62.5 | 11.1 |
| v3.7 | 5 | $0.377 (0.308-0.511) | 17.4 | 6.7 | 69.8 | 18.3 |
| v3.8-text | 12 | $0.384 (0.265-0.509) | 16.6 | 7.1 | 79.1 | 16.7 |

* **What this is not:** a probe's cost. It is the same first turn on the *start* state. An end state has more commits and a longer
  record, and with the git-only control's record reverted the cold session will find a ledger gap and may backfill it, which is a write
  and more turns. Read it as a floor and a reason to ask for a smaller cap than the plan did, not as a forecast.
* **Pilot, four probes** (one per arm and a control on a v3.8-text end state): $1.38 at these means, $1.73 with the plan's 25% margin,
  against the plan's $4. **Main, 27 probes** (21 + 6 controls): $9.44, $11.80 with margin, against the plan's $27 + margin. P3 is re-stated
  from P2's measured cost before anything is authorised (D4), so these are not a proposal for P3.

## 4. Item (d): the rater protocol, the planted-defect set and the packet

`rater.py`. The operator's reading of D5 (**he rates himself, and the model rater is built as well**) is his answer at the Phase 1 picker.

* **What the rater sees:** one record as neutral "Document n" blocks (no file name, run id or arm) plus the final message. No tools,
  an empty working directory, JSON out, its own `--max-budget-usd`. **Eight fixed questions**, each yes / no / cannot_tell
  (`next_step`, `where`, `state`, `evidence`, `hazard`, `commits`, `consistent`, `loose_ends`), then a three-way arm guess. Each record
  is rated in both question orders; disagreement shows as an order effect. Same model family as the writers; stated beside every M5 figure.
* **Planted defects, mechanical, no model:** `missing` (drop the next-step parts), `wrong` (replace them with a sentence that
  contradicts the record), `vague` (paths, anchors, shas become generic words), `fabricated` (shas swapped for invented ones). A required
  defect is *caught* when a question it targets goes from yes to not yes in **both** orders. `fabricated` is reported, not required: a
  sha cannot be checked from the text, and M1 does that against git. All four change each honest record (`rater.py defects`).
* **Not run:** the paid dry run (`dry-run`, 30 calls on three honest records: one per arm, first in sorted order, so the choice is made
  before any rating) and the call itself. The command line is checked against `claude --help`; whether the model answers in the JSON form
  asked for is first seen in P2, and the parser refuses anything else and lists the failed calls.
* **The packet:** `pilot/doc-probe/rating/packet.md`, `sheet.csv` and, apart, `KEY-do-not-open-before-rating.json`. Ten records, seed
  20261004, 3 / 3 / 4 by arm. **33,592 words, 2,832 to 3,600 per record (19-25 KB), about 168 minutes at 200 words a minute: reading
  only, an estimate.** `rater.py score-human sheet.csv KEY.json` scores his sheet and checks his arm guesses.

## 5. Item (e): the M3 task search

`m3_search.py`, results in `p2a-m3-search.json`. Searched: every deleted top-level R function in the project's history, against the live
documents (plan §3.4's classification) at the commit's parent, counting only mentions a tool must parse (a run vignette or README chunk,
the pkgdown config) or an agent reads (`CLAUDE.md`), and whether the commit itself changed them. `NEWS` is counted apart: an old entry
naming a later-removed function is history and stays true.

* **History: none.** 56 commits, 101 names, 13 named in a live document, **0** in two or more parsed-or-agent documents the commit also
  changed. The first run showed two 2020 candidates; I read them: one was a commented-out call (`#runManager()`), the others
  `eval = FALSE` chunks. The two 2026 removals (`3db018d1d`) are named only in `NEWS`.
* **Constructed, on the study's start state:** of 182 exports at `879503cce`, `getEmptyErrorLst` is named in two vignettes, each in an
  evaluated chunk, and used in 7 `R/` files and 10 test files; `kinship` is the prose word in `CLAUDE.md` (noise). A rename of `getEmptyErrorLst` would
  honestly make the vignettes fail to build until updated. Using it means designing the task (a reply that names no document, a held-out
  check, an answer key) and running it per arm: new sessions at the measured task cost (about $2.5-3.5 each), the operator's to ask for.
* **Blind spots:** removed arguments, renamed files, options and config keys are not searched; a chunk's `eval` is read from its header only.

## 6. Item (f): the caps, stated

| What | Cap | Basis |
|---|---|---|
| The study | **$100**, its own ledger from $0 (`pilot/doc-probe/spend.jsonl`) | the operator, 2026-10-03; no spend yet |
| One probe | **proposed $1.00** (`--session-cap`) | about twice the highest measured first stop ($0.51); at 98% of it a probe is recorded as failed |
| One rater call | **proposed $0.50** (`--call-cap`) | unmeasured; bounds a call, and the total cap ends the dry run |
| The P2 pilot | **plan's proposal $10 stands** (`--total-cap`) | expected: probes about $1.4-1.7; the 30-call rater dry run is the unmeasured part |

Every launch passes both caps; the driver and the rater refuse before a call when `spent + cap > total`, read from the study's own
ledger. The figures are proposals; the P2 cap is his (D4).

## 7. Where this differs from the plan, and what is asked

* Tests in `tests_probe.py`, not `tests.py` (reason in §1). A `cap_hit` rule and `--verify-all` were added; neither is in the plan.
* A probe is cheaper than the plan's guess by about a factor of three; the packet is far heavier than "about ten records" implied.
* All probes run on one CLI, as §3.7 requires: the CLI is now 2.1.289, the saved runs used 2.1.285-2.1.287.
* **Asked of the operator at this stop (S258 close-out picker):** the P2 spend and go; how many records he will read; whether M3 is
  dropped or run as the constructed rename task.
