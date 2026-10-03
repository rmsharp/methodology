# Making the Phase 3G close-out report run, and read cleanly — BL-79, costed with a prototype

**Status: DRAFT, with D1–D3 RATIFIED by the operator on 2026-10-03 (all as recommended); P1–P3 are not started.** Written at S252 (2026-10-03) as
that session's single deliverable. **The plan is the deliverable; nothing here is applied** — no tool is
installed, no settings file is edited, nothing goes upstream (`starter-kit/SESSION_RUNNER.md` §Planning
Sessions, failure mode #18). Every number below was produced by running something; the commands and the
prototype that produced them are in [`close-out-report-prototype/`](close-out-report-prototype/), with
[`EVIDENCE.md`](close-out-report-prototype/EVIDENCE.md) separating what was measured from what is only
documented.

**The operator's request:** *"Find a way to ensure that the Phase 3 close-out report is run and formatted
cleanly for display."* Chosen from a picker: **a generated report plus a Stop hook**, costed here first.

---

## 1. Why a better sentence will not do

`starter-kit/SESSION_RUNNER.md:293-302` (§3G) is nine lines: four content items and *"Then STOP."* It says
nothing about shape. [BL-79](BACKLOG.md) (`BACKLOG-DETAIL.md:3151`) has recorded the same lapse three times:

| Session | What happened | What was already in the session's context |
|---|---|---|
| S202 (2026-09-20) | All four items given, no recognisable shape; the operator asked whether a format existed | nothing — the gap was newly seen |
| S218 (2026-09-22) | Closing message carried the four items unlabelled; asked for, then given, and the lapse was not named | **BL-79 itself**, read at its own Phase 0 |
| S230 (2026-09-27) | Same, and the report was displaced by a go-ahead picker whose actions then changed the state it described | the S218 rule, verbatim, in the memory index |

A rule that was in the session's context and still failed is not fixed by a longer rule. The two failures
are different, and the plan answers them separately:

* **Not run** (S218, S230): the report was never the last thing said. Needs something outside the model that
  notices — an *actuator*.
* **Not clean** (S202, and the shape half of S218): no specified shape, so nothing to hold a report to. Needs
  *one definition* of the shape that both produces the report and checks it. `HANDOFFS.md` already has this
  (a 13-key schema and `bin/check-handoff`, `bin/check-handoff:161-166`); the report that announces it has
  neither — the asymmetry BL-79 names.

## 2. The design

**One tool, `close_out_report.py`, three modes sharing one definition of the shape.**

| Mode | Does | Why it is separate |
|---|---|---|
| render | Prints the report from the newest receipt, git, and five short texts the session supplies | the session never hand-formats |
| `--check` | Lints a message against the same constants and the receipt | a hand-written or stale report is caught |
| `--hook` | Reads a harness `Stop` or `SessionStart` payload and decides *allow* or *block* | the actuator |

### 2.1 The shape (a specification, so it can be checked)

Rendered and linted from the same constants. Sample, the prototype's exact output for S251's real receipt
(the five judgment texts are illustrative, not S251's actual report; the HEAD sha is the repo's at render time):

```
## Close-out report: S251 · 2026-10-03

**Deliverable:** Tag v4.2 and a GitHub Release on KJ5HST/methodology; upstream PR #92 opened — DONE

**Record:** HEAD `c7e42ff` · 3 uncommitted · gate run: 11/11 pass · 0 fail · 0 unmeasured

**Self-assessment:** 7/10 — went well: measured 261/0 before releasing; did not: skipped Phase 1B

**Predecessor handoff (S250):** 8/10 — clear next_steps and exact commands; nothing in it was wrong

**Next session:** Trim HANDOFFS.md, check #92, then ask about moving the tag

Session over.
```

| Rule | Checked | Answers |
|---|---|---|
| R1 first line is `## Close-out report: S<N> · <date>` and names the newest receipt's session and date | regex + receipt | *"not recognisable as a close-out report"* (S202) |
| R2 five labels, in order: Deliverable, Record, Self-assessment, Predecessor handoff, Next session | regex | the four §3G items plus the record line |
| R3 the last non-blank line is `Session over.` — nothing after it | last line | the *"1 and done"* boundary is announced; no picker rides along (S230) |
| R4 both scores equal the receipt's `self_score` / `predecessor_score` | receipt | the report cannot disagree with the durable record |
| R5 the HEAD sha is the current HEAD | `git rev-parse` | a report printed before a later commit is **stale** (S230) |
| R6 no `\|` characters | text | pipes make tables, which do not wrap in a terminal |
| R7 at most 2,000 B, each judgment text at most 300 characters | bytes | one screen; the generator **refuses** longer input rather than truncating |

**BL-79's two open design questions, answered by the evidence:**
*Required or recommended?* **Required and checkable** — S218 had the item in its own context. *Is a report
the right place for a commit sha, given `HANDOFFS.md` carries one?* The report's sha is **computed from git
at render time, never copied from the receipt**, so there is no second copy to get wrong; and the same
computation is what makes R5 detect staleness.

**Why the generator does not fill the judgment lines from the receipt.** Across **250** complete receipts
the prose fields have medians of 0.7–1.8 KB and maxima of 3–6 KB (`EVIDENCE.md`). Pasting them recreates the
wall of prose. All 250 have numeric scores, so *scores* are read mechanically; *what went well* is the
session's to say, in 300 characters.

### 2.2 When the hook fires

State kept per clone, under `.git/` (never tracked), keyed by the harness's `session_id`:

* **baseline** — written by the `SessionStart` hook the first time it sees a `session_id`: the newest
  receipt's id and status. `resume` and `compact` never overwrite it.
* **stamp** — written when a *valid* report is seen: `[HEAD, commits ahead of upstream, hash of the newest receipt]`.

A close-out is **owed** when the newest receipt is `complete` *and* it is a different receipt than the
baseline's, or the baseline's was not yet complete — i.e. this session completed one.

| # | Situation | Decision | Run? |
|---|---|---|---|
| 1 | newest receipt still `pending` (no close-out yet) | allow | real harness + table |
| 2 | close-out done, final message "Done." | **block**, with the exact command to run | real harness + table |
| 3 | same, `stop_hook_active: true` | allow — the harness permits one forced retry per Stop chain | spike + table |
| 4 | close-out done, message is a lint-clean report | allow, write the stamp | table |
| 5 | later chat, state unchanged since the report | allow | real harness (turn 2) + table |
| 6 | a commit landed after the report (the S230 case) | **block** — fresh report required | real harness (turn 3) + table |
| 7 | `SessionStart(resume)` for a known session | baseline kept; still blocks | table |
| 8 | a report whose HEAD is no longer HEAD | **block** | table |
| 9 | no baseline (hook installed mid-session) | allow — fail-quiet | table |
| 10 | the hook itself errors | exit 0, never 2 — fail-quiet | table |

*Table* = [`checks.py`](close-out-report-prototype/checks.py), 10 of 10 rows, with 6 of 6 hook mutants and
10 of 10 lint mutants caught. *Real harness* = `claude -p`, claude 2.1.288, haiku. The decision rule is
deliberately **fail-quiet**: every uncertainty resolves to *allow*, so the hook can add a message but can
never trap a session.

### 2.3 What it cannot do — stated, not hidden

1. **One forced retry, by the harness's design** (measured: the second Stop carries `stop_hook_active: true`).
   If the model's reprint is still unclean the session ends, and the only trace is the log line. The retry
   reason names the exact command, which is why it is expected to hold — measured **1 for 1 on haiku, never
   on Sonnet or Opus**.
2. **Silent when the close-out itself is skipped.** The hook keys on a *completed* receipt. A session that
   writes no receipt is FM #14 / #6, caught at the next Phase 0 reconcile — not here. A "work done but receipt
   still pending" nag was considered and rejected: it would fire on every Stop after any mid-session commit.
3. **Blind to outward actions that leave HEAD alone** — a PR, a release, a tag on another repo. A push is
   caught through the *ahead-of-upstream* count in the stamp; the others are not, and stay under the runner's
   own rule that 3G comes **after the last action**.
4. **Shape, not substance.** In the runs the model wrote "did not: None" and the lint passed it. The same
   limit `bin/check-handoff` states of itself: *a green check is not a good report*.
5. **Claude Code only.** `Stop` hooks are harness configuration. The render and check modes work under any
   agent; the actuator does not.
6. **Unmeasured:** `session_id` across compaction (design fails quiet if it changes); `/clear` and `fork`
   sources; how the first reply and the forced report **render in the interactive terminal** (`-p` shows only
   the last) — only the operator watching a real close-out can see that.

## 3. Inventory — what this touches (grep'd, `7ed0ee0`)

| Where | Line(s) | Phase | Note |
|---|---|---|---|
| `starter-kit/close_out_report.py` | new | P1 | beside `context_budget.py`, `quality_ratchet.py` |
| `tools/test_close_out_report.py` | new | P1 | canonical-only, like `tools/test_context_budget.py` |
| `bin/tests.sh` | `:267` is the unit-suite wiring pattern; last numbered test is `:3578` (Test 44) | P1 | |
| `.quality-gates.json` | `:36-39` is the gate pattern | P1, P2 | new gates only **tighten** (`SAFEGUARDS.md` Blast Radius) |
| `.claude/settings.local.json` | ignored by the operator's global `~/.config/git/ignore:1`, not by this repo; **no `.claude` file is tracked** | P2 | operator's file — D2 |
| `starter-kit/SESSION_RUNNER.md` | `:293-302` §3G (252 B); FM #6 row `:317` | P3 | **already 55,406 B vs a 41,364 B ceiling** |
| `starter-kit/SAFEGUARDS.md` | `:176-183` *Close-Out Completeness Hook*, which says *"The methodology ships no such hook"* | P3 | also over its ceiling (17,129 vs 15,386 B) |
| `bin/_manifest.py` | `:50-55`; the ordered-tuple note at `:52` | P3 | append one `TRACKED` row after `quality_ratchet.py` |
| `starter-kit/HANDOFFS.md` | `:37`, `:66` call the prose *"the durable proxy for the Phase 3G spoken report"* | P3 | re-read; probably unchanged |
| `HOW_TO_USE.md` | `:765-768` | P3 | one phrase |
| `docs/tutorials/T2_worked_transcript.md` | `:266-270` (§3G, unshaped) | P3 | the worked example should show the shaped report |
| `README.md` | `:428` ("Phase 3G ends by reporting and stopping") | P3 | re-read |
| `docs/planning/BACKLOG.md:167`, `BACKLOG-DETAIL.md:3151` | BL-79 | P3 | closing = **two** edits: drop the index row, keep the id in the "ids stay here" block (`BACKLOG.md:195`) |

Precedents followed: the env-gated, bypassable, canonical-first hook in `.githooks/commit-msg:12,34`
(`SAFEGUARDS.md:185-187`); a distributed tool plus a canonical-only test file, as `methodology_trim.py` and
`tools/test_methodology_trim.py`.

## 4. Phases — each is one session; close out at the end of each

### P1 — the generator and the lint *(fork-only; ships to no adopter)*

**Done looks like:** `python3 starter-kit/close_out_report.py` renders the §2.1 report from the real newest
receipt, refuses a missing or over-long input, and `--check` refuses each of the ten corruptions in
`checks.py`. A property test renders a report for **every complete receipt in the live ledger and every
archived shard** (250 today) and asserts the output lints clean.
**Verify:** `python3 tools/test_close_out_report.py`; `bash bin/tests.sh > /tmp/out` (capture it; the ratchet
keeps none); `python3 starter-kit/quality_ratchet.py --run` with the new gate at the measured count;
`git status` shows no file outside the five below.
**Files (5, one commit):** `starter-kit/close_out_report.py`, `tools/test_close_out_report.py`,
`bin/tests.sh`, `.quality-gates.json`, `CHANGELOG.md`.
**Surface:** this repository's own ledger and shards, in-process. **Cannot enforce:** anything about the
harness — P1 proves the shape and the lint, not that anything fires.
**Dogfood:** the *next* session's close-out ends with the generated report; its receipt cites the lint result.
**STOP** at the commit.

### P2 — the hook *(fork-local, operator's machine; no adopter impact)*

**Done looks like:** `--hook` mode implements §2.2; the ten-row decision table and the six hook mutants become
unit tests with fixtures copied from the **measured payload shape** (`EVIDENCE.md`); the operator has put the
snippet below in their own `.claude/settings.local.json`; and on the real harness, in a scratch clone, four
`claude -p` scenarios behave as in rows 1, 2, 5 and 6. Then **one real close-out is watched by the operator**
to see how the two messages render.
**Verify:** `python3 tools/test_close_out_report.py` (count rises, gate tightens); a scripted scenario run
whose results are pasted into the receipt; the operator's own observation of one live close-out.
**Cost (measured, haiku):** one block-and-comply loop $0.045; the full three-turn session $0.081; four
scenarios ≈ $0.2–0.3. **Not measured at Sonnet/Opus rates.** Any spend cap is the operator's; I will name the
model and the estimate and ask before running at a higher rate.
**Surface:** the real Claude Code harness (`claude -p` for the loop; the operator's terminal for display).
**Cannot enforce:** other harness versions or agents; compaction's `session_id`; outward actions that leave
HEAD alone (§2.3).
**Files (≤5):** `close_out_report.py`, `tools/test_close_out_report.py`, `.quality-gates.json`,
`CHANGELOG.md`; the settings file is the operator's and is **not** committed.
**STOP** after the live check.

The snippet (the operator's to install — a session must not edit permission or hook settings on its own):

```json
{"hooks": {
  "SessionStart": [{"hooks": [{"type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR\"/starter-kit/close_out_report.py --hook"}]}],
  "Stop":         [{"hooks": [{"type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR\"/starter-kit/close_out_report.py --hook"}]}]
}}
```

### P3 — the distributed change *(upstream pull request; **its own go-ahead**)*

**Done looks like:** §3G tells a session to run the tool and print its output, **net ≤ 0 B** in
`SESSION_RUNNER.md` (a candidate is **239 B against today's 252 B**; the obvious fuller wording is 595 B and
would grow a file already over its ceiling — FM #28); `SAFEGUARDS.md:176-183` ships the tool and the snippet
instead of *"ships no such hook"*, also net ≤ 0 B; `bin/_manifest.py` gains one `TRACKED` row; a scratch
adopter receives the tool at its root through `bin/sync`; the worked transcript and the two doc phrases in §3
agree. Respects FM #17: the change **adds** a step's tooling and removes none.
**Verify:** `bash bin/tests.sh` (the manifest-driven tests at `:41`, `:164`, `:220` read `_manifest.DISTRIBUTION`; the twin test pattern is `:280`); `bin/sync` into a scratch
adopter and run the tool there; `python3 starter-kit/context_budget.py --status` before and after (the bytes
above); the PR text greps clean of session numbers and BL codes (it is outward-facing text).
**Adopter impact, stated:** every adopter's `SESSION_RUNNER.md` and `SAFEGUARDS.md` change and one new file
appears at their root; **no hook is installed for anyone** — that stays their harness configuration.
**Surface:** a scratch adopter project plus the real harness. **Cannot enforce:** an adopter's harness.
**Does not start before** P1 and P2 have each closed and the operator says so. **STOP** at the opened PR.

## 5. What the operator is choosing between

| | Choice | Recommendation and why |
|---|---|---|
| **D1** | Where the tool lives: `starter-kit/close_out_report.py` from P1, or `bin/` (canonical-only, like `check-handoff`) | **`starter-kit/`.** Adopters carry the same §3G (BL-79: `nprcgenekeepr`'s is byte-identical), so it will move there; renaming later touches tests and gates. It reaches no adopter until P3 adds the manifest row. |
| **D2** | How the hook is installed: your gitignored `.claude/settings.local.json`, or a tracked `.claude/settings.json` | **`settings.local.json`.** A tracked file would also apply to anyone else who works in this clone or a fork of it; making it shared is a separate go-ahead. |
| **D3** | Required and checkable, or a recommended template | **Required.** The recommended-template route is the one S218 and S230 failed on with the rule in context. |

**Ratified 2026-10-03, in the S252 picker:** D1 `starter-kit/close_out_report.py`; D2 the operator's gitignored `.claude/settings.local.json`; D3 required and checkable. Asked in the same picker and declined for now: pushing local `main` to the fork `origin`.

Plan parameters adjustable at the P1 review without a decision: the 300-character and 2,000 B caps, the label
wording, and whether the Record line carries the uncommitted count (it is informational and not part of the
staleness key, because tool runs dirty two tracked history files every session).

## 6. What this plan deliberately does not do

* **Does not implement anything**, install a hook, or edit any settings file.
* **Does not open or comment on anything upstream.** P3 is a pull request and needs its own go-ahead.
* **Does not judge report quality** (§2.3 item 4), and does not add a "close-out skipped" nag (§2.3 item 2).
* **Does not shape the Phase 0 orientation report**, which has the same character; the tool could grow a mode
  later, and bundling it now would be the keep-going failure (FM #2).
* **Does not touch `FRAMEWORK_LEARNINGS.md`** or append a fork learning; the lesson (*a rule that was in
  context and failed needs an actuator*) is recorded in BL-79 and the memory index already.
