# Tutorial Series — Plan

**Status:** PLAN (deliverable of a planning session). Decisions ratified with the operator 2026-06-20; not yet implemented.
**Date:** 2026-06-20
**Author:** methodology session (canonical-repo dogfooding)
**Governing discipline:** `starter-kit/SESSION_RUNNER.md` §Planning Sessions (evidence-based inventory). Each tutorial will itself be authored as a methodology session ("1 and done"), so the series dogfoods the framework it teaches.
**Fork-only doc** per the established branching pattern: planning docs live on `origin/main`; the tutorial *content* (when written) is canonical-repo material (see Decision 2).
**Relationship to other work:** Independent of B1 / issue #32 (sync coverage). References its ratified link conventions (absolute-URL-for-non-distributed-targets) but adds no dependency. Candidate to ship as its own minor release once the core trio lands.

---

## 1. Problem statement

The methodology has four documentation layers, none of which is a **hands-on, progressive learning track**:

| Existing doc | Genre | What it does | What it does *not* do |
|---|---|---|---|
| `README.md` | Pitch + index | Sells the idea (`§The Problem`, `§Evidence`), quick start | Walk a newcomer through doing it |
| `ITERATIVE_METHODOLOGY.md` (863 ln) | Flight manual | Defines 9 principles, 6 phases, 12 gates, the loop | Teach by doing; it is reference |
| `starter-kit/SESSION_RUNNER.md` (368 ln) | Cockpit checklist | Step-by-step operating procedure to run *during* a session | Onboard someone who has never run one |
| `starter-kit/BOOTSTRAP.md` (394 ln) | Setup procedure | 10 numbered install steps | Reads as reference, not a guided first-run |
| `HOW_TO_USE.md` (941 ln) | Illustrative narratives | 3 worked examples + "Running Your First Session" | **Shows**, does not make you **do**; read-along, no checkpoints, no real artifact the learner produces |

A learner today must read ~900-line manuals and infer the doing. **The gap: a sequenced set of lessons where the learner performs one thing at a time against a real project, hits a checkpoint, and sees the payoff — the genre `HOW_TO_USE.md` gestures at but does not deliver.**

## 2. Evidence-based inventory (run 2026-06-20)

### 2.1 Benefits / "why bother" material already exists — tutorials cite it, do not restate it
- `README.md:5 §The Problem`, `README.md:20 §Evidence` — the case for the methodology + empirical results.
- `ITERATIVE_METHODOLOGY.md:7 §Origin and Findings`, `:49 §When to Use This Methodology`.
- `HOW_TO_USE.md:79 §The Self-Improvement Loop`, `:88 §Quality Gates` — the *value* framing.
- `ITERATIVE_METHODOLOGY.md:424 §The Self-Improvement Loop` — the compounding payoff.

> **Decision 6 (benefits):** the series **points to** this material (cite-don't-duplicate) and additionally opens with a short "Why bother?" hook in the series index and at the top of T1, so a cold-start learner sees the payoff *before* the setup chores. No new benefits prose is authored that could drift from the canonical case.

### 2.2 Source anchors each tutorial will cite (not duplicate)
| Tutorial | Primary sources |
|---|---|
| T1 Setup | `BOOTSTRAP.md` (10 steps), `README.md:57 §Quick Start`, `bin/sync`, `bin/_manifest.py` |
| T2 First Session | `SESSION_RUNNER.md` (whole), `ITERATIVE_METHODOLOGY.md:134 §The 6 Phases`, `HOW_TO_USE.md:630 §Running Your First Session` |
| T5 Cautionary | `SESSION_RUNNER.md` (26 FMs, Quality Gates, §Vertical Slice Sessions), `ITERATIVE_METHODOLOGY.md:49 §When to Use`, `:481 §Protocol Erosion`, `HOW_TO_USE.md:901 §Troubleshooting` |

### 2.3 What does *not* exist (confirmed by `find`)
No `tutorials/`, `*tutorial*`, `*walkthrough*`, or learner sample project anywhere in the repo. Greenfield.

## 3. Governing design principles
1. **Cite, don't restate** — the same rule the methodology applies to skills ("recommends; does not reimplement"). Tutorials link into BOOTSTRAP/SESSION_RUNNER/ITER at the right beat; one source of truth, no drift.
2. **Dogfood** — each tutorial is authored as its own methodology session. The series demonstrates the methodology by being built with it.
3. **One objective per tutorial** — mirrors "1 deliverable per session."
4. **Progressive + prerequisite-stated** — T1 → T2 → T5 builds; each names its predecessor.
5. **Benefits up front** (Decision 6).
6. **A real produced artifact** — every tutorial ends with the learner having *made* something (an installed framework, a saved session doc, a near-miss they caught), not just read.

## 4. Decisions ratified with the operator (2026-06-20)

| # | Decision | Ratified outcome |
|---|---|---|
| 1 | Practice substrate | **Dual-track, learner picks one per pass** ("1 and 2, not at the same time"): **Track A** apply steps to *your own repo* (transcript = reference); **Track B** clone the *bundled sample project* and follow the transcript step-for-step. Unified by §5. |
| 2 | Home + distribution | **Canonical-only.** Tutorials live in the canonical repo, are reachable on GitHub, and are **never** added to `bin/_manifest.py` → `bin/sync` never copies them into adopter repos. Discoverability mechanism in §6. |
| 3 | First-cut scope | **Core trio: T1 (Setup) · T2 (First Session) · T5 (Cautionary).** Exactly the operator's named set. T3/T4/T6/T7/T8 are a roadmap (§7), not committed now. |
| 6 | Benefits | Cite + short hook (§2.1). |

## 5. The sample project + worked transcript (resolves Decision 1)

The two practice tracks are unified by a single artifact: **the worked transcript is a real, recorded methodology run against a bundled sample project.**

- **Sample project** — a deliberately tiny, throwaway repo bundled in the canonical repo (proposed: a stdlib-only Python **todo CLI** with `pytest` — gives a real *build equivalent* (`pytest`), a believable backlog of features/bugs to drive sessions, and a near-miss to catch in T5; exact app is a P1 decision). It is canonical-only (Decision 2), never synced.
- **Worked transcript** — the verbatim record of running T2's session on the sample project. Track-B learners replay it in the sandbox; Track-A learners read it as "what a good run looks like" while applying the same steps to their own repo.
- **One running example threads the core trio:** T1 installs the framework into the sample project; T2 runs the first session (builds one todo-CLI feature, recorded as the transcript); T5 uses *that same session's* near-misses (e.g., the urge to skip Phase 0, or implement before the Present gate) as its cautionary cases. The learner sees the compounding loop on a single continuous artifact.

> **Dragon (transcript staleness):** the transcript hard-codes tool/agent output that ages. Mitigation: keep the transcript's *methodology* steps load-bearing and its tool output illustrative; mark a "re-record if SESSION_RUNNER phases change" note. Treat the sample project as a maintained deliverable, not fire-and-forget (it is a second tiny codebase — accepted cost of Track B).

## 6. Discoverability mechanism — "on GitHub, not pulled into every repo"

This is a **solved pattern already in the repo** (the B1 Phase 2 audits-link decision): a distributed file that must reference a *non-distributed* target uses an **absolute `github.com` URL**, not a relative path that would dangle in an adopter tree.

1. **Location:** tutorials + sample project live at **`docs/tutorials/`** in the canonical repo. They are **not** listed in `bin/_manifest.py`'s `DISTRIBUTION`, so `bin/sync`/`bin/status` ignore them entirely → **never pulled into adopter repos** (requirement met).
2. **Canonical-repo discovery:** a new `## Tutorials` section in `README.md` links to `docs/tutorials/` (relative — both live in the canonical repo).
3. **Adopter discovery:** one-line pointers added to the **synced** `SESSION_RUNNER.md` and/or `BOOTSTRAP.md` — e.g. *"New to the methodology? Walk the tutorials: https://github.com/KJ5HST/methodology/tree/main/docs/tutorials"*. Because the pointer lives in a *distributed* file but targets *non-distributed* content, it **must be an absolute `github.com` URL** (relative would dangle in adopters). `bin/check-links` already skips `http(s)`, so this stays green and re-triggers none of the link-topology paradox.
   - *Byte-sensitivity caveat:* `SESSION_RUNNER.md` is the most sync-sensitive file; prefer the pointer in `BOOTSTRAP.md` (or `README` only) unless a SESSION_RUNNER pointer is judged worth the diff. Decide at P1.

> Net: tutorials are reachable from GitHub and from every adopter's synced docs **by link**, while zero tutorial bytes land in adopter working trees.

## 7. Curriculum (core trio now; full arc as roadmap)

| # | Tutorial | Objective | In first cut? |
|---|---|---|:--:|
| T1 | Setup & First Bootstrap | Framework installed: root files, CLAUDE.md protocol block, task tracking, dashboard | ✅ |
| T2 | Your First Session, End-to-End | One full 6-phase pass → one deliverable; emphasizes Phase 0 Orient + the Present gate | ✅ |
| T5 | Cautionary Use | Gates, the 26 FMs, "1 and done", vertical-slice gates, Plan-Mode exit trap, FM #26, *when it is too heavy* | ✅ |
| T3 | The Compounding Loop | Handoff + scoring + watching session N+1 improve | roadmap |
| T4 | Choosing & Adapting a Workstream | Pick the right workstream; spin a custom one | roadmap |
| T6 | Multi-Session Campaigns | When one deliverable spans many sessions | roadmap |
| T7 | Portfolio & Dashboard Ops | Run across many projects; read the health dashboard | roadmap |
| T8 | Keeping Adopters Current | `bin/sync`/`bin/status`, TRACKED/SEED taxonomy (B1) | roadmap |

## 8. Tutorial anatomy (one shared template)

New `docs/tutorials/TUTORIAL_TEMPLATE.md` (parallel to `workstreams/TEMPLATE_WORKSTREAM.md`):
- **Front-matter:** Objective · Prerequisites (prior tutorials) · Time · *What you'll produce* · Track A/B note.
- **Body:** numbered **"You do X → Expected result"** steps, each with a **checkpoint** ("you should now see …").
- **Common mistakes** callouts that link the relevant FM by number (cite, don't restate).
- **Why this matters** mini-hook linking the benefits sources (Decision 6).
- **Next:** pointer to the successor tutorial.

## 9. Phased execution (each phase = one session; STOP + close out between)

> Sizing: 1 planning (this) + ~4 implementation. The phases are *distinct capabilities* (scaffolding; one tutorial each) — bundling them would be FM #26.

### P1 — Scaffolding *(1 session)*
Create `docs/tutorials/` with: `TUTORIAL_TEMPLATE.md`, `README.md` (series index + "Why bother?" hook + benefits links), the **sample project** skeleton (+ `pytest` green), and the discoverability wiring (§6: README §Tutorials; absolute-URL pointer site decided here).
- **DONE:** `docs/tutorials/` exists; template + index render; sample project's `pytest` passes; README links resolve; any synced-file pointer is an absolute URL and `bin/check-links` stays green.
- **Verify:** `./bin/tests.sh` green (no regression); `pytest` in sample project green; `bin/sync $(mktemp -d) --dry-run` shows **no** `docs/tutorials/` files (proves non-distribution). STOP.

### P2 — T1 Setup *(1 session)*
Write T1 against the template; learner ends with the framework installed (Track A own repo / Track B sample project).
- **DONE/Verify:** a fresh reader following T1 reaches a bootstrapped project; every cited anchor (BOOTSTRAP steps, `bin/sync`) resolves. STOP.

### P3 — T2 First Session + the worked transcript *(1 session)*
Run a real first session on the sample project (build one todo-CLI feature), **record the transcript**, write T2 around it.
- **DONE/Verify:** transcript is a faithful 6-phase run; T2's checkpoints match the transcript; Present-gate stop is explicit. STOP.

### P4 — T5 Cautionary *(1 session)*
Write T5 using P3's near-misses; cover gates, FMs (cite by number — do **not** renumber/restate), when-not-to-use.
- **DONE/Verify:** every FM/gate reference resolves to `SESSION_RUNNER.md`; "too heavy" guidance cites `HOW_TO_USE.md §Troubleshooting`. STOP. Ship the core trio (candidate release).

## 10. Dragons
- **Benefits duplication drift** — restating the case instead of linking it. Mitigation: Decision 6, link-only.
- **FM/gate restatement drift** — copying the 26 FMs into T5 would fork the canonical list. Cite by number only.
- **Transcript/sample staleness** — §5 dragon; maintained-deliverable posture + "re-record on phase change" note.
- **Synced-file link dangle** — any pointer from a distributed file to `docs/tutorials/` must be an absolute URL (§6).

## 11. Out of scope
T3/T4/T6/T7/T8 (roadmap, not committed); video/interactive formats; distributing tutorials via `bin/sync` (explicitly rejected, Decision 2); any principle/phase/gate/workstream/FM change.

## 12. Planning-session checklist
- [x] Evidence-based inventory with file + line anchors (§2) — searches actually run, not from memory
- [x] Each phase has DONE + verification + a STOP (§9)
- [x] Dragons flagged (§10)
- [x] Decisions surfaced and ratified with the operator (§4, Decision 6)
- [x] Discoverability mechanism specified concretely (§6), reusing an established repo convention
