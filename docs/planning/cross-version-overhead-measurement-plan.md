# Plan: measuring methodology overhead across versions

**Status: DRAFT for operator approval.** Written at S235 as the session's one deliverable. Nothing here has
been run; no model session has been launched and no money spent. Approval of this document is not approval
of any phase's spend (§7).

**Asked for by the operator, 2026-09-29:** a session dedicated to planning how overhead is measured across
the versions of the methodology. His direction while it was being written: *"we will have to run multiple
sessions using each of the historic versions since we do not have detailed historic information to pull."*
That is the primary design (§4, arm D).

**Relation to BL-91.** [`overhead-ratchet-plan.md`](overhead-ratchet-plan.md) asks whether to *gate* growth
of the mandated read-set (ratified at S233: report better, gate nothing). This plan asks a different and
prior question: **what does each version cost a session, and what does it buy?** It changes no decision
S1–S4 of that plan records, adds no gate and touches no distributed file. It uses that plan's series as
its static arm and as a cross-check.

---

## §1 What exists, and what it cannot answer

| Evidence | What it measures | Reaches | Cannot say |
|---|---|---|---|
| [`mandated-load-per-version.py`](bl91-overhead-measurement/mandated-load-per-version.py) | bytes of `SESSION_RUNNER.md` + `SAFEGUARDS.md` at each release | v1.0.0 → HEAD, 27 releases (`overhead-ratchet-plan.md` §2.1: 17,615 B → 80,526 B at v3.7) | what a session *does* with them: turns, tool calls, artifacts written |
| [`process-vs-work-per-session.py`](bl91-overhead-measurement/process-vs-work-per-session.py) | added lines, ledger vs other, per session claim | S201 onward only (its own docstring) | anything before S201; lines are crude |
| [`cost-per-project.py`](bl91-overhead-measurement/cost-per-project.py) | list-price dollars from local transcripts | transcripts only | version, and any period before the transcripts begin |
| `starter-kit/context_budget.py` | the same read-set, in bytes and tokens | now | history |
| `self_score` in `HANDOFFS.md` + archives | 252 self-graded scores across 253 receipts (one is this session's pending claim) (`grep -c` over the live file and `docs/archive/HANDOFFS-*.md`) | S1 onward | quality: the scorer is the session being scored |

**The gap is the middle column of nothing.** For every version before the transcripts begin, the only
number that exists is a byte count. Turns, which `overhead-ratchet-plan.md` §2.4 names as *"the larger cost
term"*, are measured for no version.

**A correction to carry into that plan, found while surveying this session.** §2.4 says local transcripts
begin 2026-08-16. Surveying `~/.claude/projects/` (first timestamp per project directory): `vscode-quarto-ext`
begins **2026-07-24**, `mts-system` **2026-08-09**, `chat-verification` 2026-08-13, and `methodology` itself
2026-08-16. The claim is true of this repository only. It does not change the conclusion — 2026-07-24 is
still after v3.3 (2026-07-08) and before v3.7 (2026-08-11), one project, one model — but §2.4 should say
"this repository" and this plan should not inherit the wrong scope. (Whether `vscode-quarto-ext` ran the
methodology at all was not established: 58 of its transcripts contain the word, but its checkout carried no
runner. Treat it as unknown.)

## §2 What "overhead" means here

Overhead is **what a session spends that the deliverable does not need**, measured against a session that
does the same task without the framework. Six components, with the instrument for each:

| # | Component | Instrument | Available per version by |
|---|---|---|---|
| O1 | Mandated read (bytes, tokens) | existing script, `context_budget.py` | static (exists) |
| O2 | Turns / requests until the deliverable's first real work | transcript `usage` records | **replay only** |
| O3 | Tool calls and tokens (input, output, cache read/write) over the whole session | transcript `usage` records | **replay only** |
| O4 | Process artifacts written (bytes of ledger, receipt, notes) | diff of the fixture at session end | replay; commits for S201+ |
| O5 | Wall-clock | transcript timestamps | replay only |
| O6 | Stakeholder interruptions (STOPs that wait for a person) | count of scripted replies consumed | replay only |

The **benefit** side is not optional. A cost curve with no benefit reading invites the wrong conclusion
(*cheaper is better*). Each arm is therefore also scored on **B1: seeded traps caught** — the fixture
contains defects the framework exists to catch (§3), scored pass/fail by a script, not by the session.
`self_score` is recorded but never used as evidence (scorer = scored).

## §3 The controlled replay (arm D) — the primary design

**One fixed fixture, one fixed task, one fixed model; only the framework files vary.**

- **Fixture.** A small synthetic repository with a `BACKLOG.md`, a test suite, a prior-session record, and
  a prepared uncommitted change. Small on purpose: it measures *framework* overhead and would otherwise be
  swamped by codebase size.
- **Seeded traps (B1).** At least: a ghost session (commits with no notes), a stale prior handoff that
  contradicts `git log`, and a task whose obvious first move is to implement before approval. Each has a
  script that says caught / not caught from the final tree and transcript. A version that predates the
  mechanism scores 0 for it *by design*; that is a finding about the version, not a fault of the fixture.
- **The task.** One deliverable, identical for every arm, with an acceptance test that is run by the harness
  after the session ends.
- **The arms.** Each arm installs *that version's own* framework files into a copy of the fixture, exactly
  as that version's `BOOTSTRAP.md` (at its tag) instructs — `git archive <tag>`, not today's layout. Arms:
  `v1.0.0`, `v2.0`, `v2.7`, `v3.0`, `v3.3`, `v3.7`, `HEAD` (the seven anchors of `overhead-ratchet-plan.md`
  §2.1), plus **`none`**: a bare `CLAUDE.md` with the task and no framework. `none` is the zero-overhead
  baseline; overhead for a version is its arm minus `none`.
- **The stakeholder.** The runner stops at Phase 0 and at the Present→Implement gate and waits for a person.
  The harness answers from a fixed script: the same messages, in the same order, for every arm. A version
  that asks a question the script does not cover is recorded as an **unscripted stop** (a finding — O6), and
  gets the neutral reply "proceed as you judge best".
- **Repetitions.** k per arm, chosen after the pilot measures variance (P2), never below 3.
- **Harvest.** Each session's transcript lands under `~/.claude/projects/` for the fixture path. A single
  extraction script produces one row per session: O2–O6, B1, arm, rep, model, date.

**What the replay measures, stated so nobody over-reads it.** It measures *today's model working under each
historic version's instructions*. It does **not** measure what those versions cost when they were current,
under the model then in use. It measures the framework text, not the era. Every table produced must carry
that sentence.

**What it cannot see.** A fixture has no accumulated ledger, so it cannot show the cost of reading a
224 KB `CHANGELOG.md` (the growth component of overhead). O1 covers only the fixed mandated read. Ledger
growth is a separate question with its own instrument (`context_budget.py`, the trim triggers) and is out of
scope here, listed so its absence is not mistaken for a zero.

## §4 The other arms, and what they are for

| Arm | Design | Cost | Role |
|---|---|---|---|
| **S** static | O1 per release, existing script | none | cross-check: an arm's mandated read in the transcript must match the script's bytes/tokens for that tag, or the install is wrong |
| **G** git-derived | process vs work lines per session, S201+ | none | corroborates O4 on real work; cannot reach older versions |
| **C** observational | transcripts of real projects from 2026-07-24 / 08-09, tagged by the framework version installed in that project on that date | none | **confounded** (task mix, session length, model); reported only as a sanity band around D, never as a version comparison |
| **D** replay | §3 | model spend | the only arm that yields O2–O6 for old versions |

A preliminary look at C, to show why it cannot stand alone: per-session medians for `methodology` were
122 requests (2026-08, 37 sessions) and 121 (2026-09, 89 sessions); for `mts-system` 103.5 (18) and 129.5
(38). Those movements are within what task mix alone would produce. This is a feasibility probe, run once
and not preserved as a script; if arm C is built it is rebuilt with a committed script.

## §5 Phases

Every phase is **one session**. Close out when it is done; the next phase does not start in the same
session (failure mode #18). Every phase names its surface, because a phase whose criterion was checked
somewhere it cannot fail is the failure issue #75 recorded.

### P1 — Build the harness without spending a model token

**Do:** the fixture; the seeded-trap scorers; the acceptance test; a per-tag installer that builds each arm's
tree from `git archive <tag>` and that version's `BOOTSTRAP.md`; the scripted-stakeholder driver; the
transcript extractor.
**Driver feasibility comes first and is not assumed.** Whether Claude Code can be driven headlessly through
a multi-turn session with scripted replies, with a fixed model and no ambient hooks, skills or memory leaking
into the arm, is **unverified**. P1's first act is to establish it from the installed CLI's own `--help` and a
zero-cost dry run; if it cannot, the plan returns to the operator with the manual alternative (§6, D5).
**DONE:** (a) the installer builds all eight trees; (b) for the seven versioned arms the mandated-read
bytes in the built tree equal `mandated-load-per-version.py`'s figure for that tag — exact match, printed
per arm; (c) the trap scorers each return *not caught* on an untouched fixture and *caught* on a hand-made
positive; (d) the extractor runs on an existing local transcript and emits a row.
**Verify:** run (b), (c), (d) and paste their output. **Surface:** the local machine, no model. It **cannot**
show that the driver behaves under a real model, which is why P2 exists.
**STOP** after commit.

### P2 — Pilot, with a spend cap

**Do:** one session each of `none`, `v1.0.0`, `HEAD`, then a second of `HEAD`, to estimate cost per session
and run-to-run variance, and to find where the scripted stakeholder is inadequate.
**DONE:** a pilot report giving requests, tokens and list-price dollars per session, the `HEAD`-vs-`HEAD`
spread, the unscripted stops, and a **recommended k and total budget for P3** — a number, from the pilot,
not from this plan.
**Verify:** the extractor's rows are in the report and each figure re-derives from the named transcript.
**Surface:** the real model on the fixture. It **cannot** show behaviour on a large or aged real project.
**Requires the operator's spend go-ahead before it starts (D2).** **STOP** after commit.

### P3 — The full run

**Do:** all arms × the k that P2 recommended, in an order that interleaves arms (so a model or service change
mid-run does not line up with one version). May span sessions; each session harvests what it ran and stops.
**DONE:** every planned (arm, rep) has a row or a recorded, explained absence. **Verify:** row count equals
arms × k; no arm's reps fall outside a re-run window that would confound it. **Surface:** as P2.
**Requires the operator's go-ahead against the budget P2 recommended.**

### P4 — Analysis and publication

**Do:** one table, O1–O6 and B1 by version with the spread, `none` subtracted, the §3 sentence attached, and
the arm-S cross-check shown. **DONE:** the report, and the extraction and analysis scripts committed so the
table re-runs. **Verify:** re-run reproduces every figure from the stored rows. **Surface:** the stored
data; it makes no claim about any real project. Where the report is published is decision D3 below.

## §6 Risks, each with its counter

| Risk | Counter |
|---|---|
| The fixture is too small to show framework cost that scales with the project | stated as a non-coverage (§3); not papered over |
| An old version's install steps no longer work | P1 (b) fails loudly; the arm is dropped and named, not silently substituted |
| Ambient state (the operator's `CLAUDE.md`, memory, hooks, skills) leaks into an arm and cancels the comparison | P1 must isolate each session from user-level configuration and prove it with a marker file each arm should not see; otherwise D5's alternative applies |
| Run-to-run variance exceeds version-to-version differences | P2 measures it first; if it does, the report says the versions are not distinguishable at that k, which is a result |
| A model change mid-study | arms are interleaved; the model id is a column in every row |
| Reading the curve as "cheaper is better" | B1 is reported beside every cost row |

## §7 Decisions the operator owns

| # | Decision | Recommendation | Why it is his |
|---|---|---|---|
| D1 | The arm set: the seven anchors plus `none`, or fewer/more tags (27 exist) | the eight in §3 | sets the size of the study |
| D2 | Spend: authorise P2's pilot now; authorise P3 only after P2 names its cost | pilot cap set by him before P2 starts | model spend, each time |
| D3 | Where the results are published (fork only, or contributed upstream) | fork only until seen | outward-facing; ties to the deferred D3 of `overhead-ratchet-plan.md`, which this does **not** settle |
| D4 | Model for the replay: the current default, or one held fixed for the whole study | one held fixed, named in every row | comparability |
| D5 | If headless driving proves impossible: run the sessions by hand from a script, or drop arm D | by hand for the pilot only | his time |

## §8 What this plan does not do

It does not gate, warn or refuse anything, and does not reopen S3 (hook enforcement, declined at S206) or
D1 of `overhead-ratchet-plan.md` (ratified at S233). It changes no distributed file. It launches nothing:
P1 is the first phase, and it spends no model tokens.

## §9 Planning checklist (runner §Planning Sessions)

- Reasoning depth: **not verified** — the session could not set a maximum-effort mode from inside; recorded
  rather than claimed.
- Grep-based inventory: not applicable (no deletion, migration or rename); the survey in §1 was run against
  `~/.claude/projects/`, `git tag`, `HANDOFFS.md` + archives, and the BL-91 scripts.
- Per-phase DONE, verification, surface and STOP: §5.
- Cited figures re-derived this session, not quoted: tag list and dates (`git tag`), receipt and score counts,
  transcript first-dates, the 17,615 → 80,526 B series (read from `overhead-ratchet-plan.md` §2.1, itself a
  re-run — **not re-run here**; P1 (b) re-runs it).
