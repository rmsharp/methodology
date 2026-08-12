# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

A standalone methodology framework for structured, self-correcting AI agent sessions. It is **not a software project** — it contains no code to build, test, or run. The deliverables are markdown documents.

**Repository:** `git@github.com:KJ5HST/methodology.git`
**Author:** Terrell Deppe (KJ5HST)
**License:** MIT — see `LICENSE`. Free to use, copy, modify, distribute, and sell, provided the copyright notice and permission notice are retained.

### Contributing upstream — the purpose, and the one rule

**This clone is a fork whose purpose is to update the upstream repository** `KJ5HST/methodology`
(remote `upstream`; `origin` is the fork). Work that reaches adopters only reaches them through a
merged upstream pull request, so getting work *there* is the point, not an afterthought.

What is scarce is the maintainer's review time. So: let work accumulate here until it is worth his
attention; prefer **one substantial, fully vetted pull request** over several small ones (independent
work *may* go separately, dependent work should not); do the vetting on this side first — tests
green, claims re-verified, adopter impact stated. **Every outward-facing action — pull request,
issue, comment, tag, release — needs the operator's explicit go-ahead, each time.**

This is a rule about **sequence and batching, never a suspension.** No session may record the
contribution route as closed, paused, or unavailable. One did — inferring a standing prohibition from
a single correction and writing it into a ratified plan — and it re-ranked ten sessions away from
this repository's stated purpose before anyone noticed. If you find a blocker in a document, check
who imposed it and when; an unattributed blocker is a defect, not a constraint.

## Document Hierarchy

Three layers, each serving a distinct purpose:

| Layer | File | Role |
|-------|------|------|
| Cockpit checklist | `starter-kit/SESSION_RUNNER.md` | Step-by-step operating procedure for every session |
| Flight manual | `ITERATIVE_METHODOLOGY.md` | Theory: 9 principles, 6 phases, 12 quality gates |
| Mission procedures | `workstreams/*_WORKSTREAM.md` | Domain-specific adaptations (design, architecture, development, audit, research documentation) |
| Campaign templates | `workstreams/*_CAMPAIGN.md` | Multi-session campaigns extending a workstream |

`SESSION_RUNNER.md` is the entry point — it tells agents what to read, when to stop, and how to close out. Everything cascades from that single file.

## Architecture

The framework's core loop:

```
Pre-Flight → Research → Create → Present → Implement → Verify & Close
```

Each phase is hard-gated — you cannot skip ahead. The most critical gate is between Present and Implement (no implementation without stakeholder approval).

**The compounding mechanism** is the handoff accountability loop: each session evaluates its predecessor's handoff (scored 1-10) and writes its own knowing it will be scored. This bidirectional accountability is what makes session N+1 better than session N.

### Starter Kit Files (templates for adopting projects)

| File | Purpose |
|------|---------|
| `starter-kit/SESSION_RUNNER.md` | Operational checklist — users copy this to their project root |
| `starter-kit/FRAMEWORK_LEARNINGS.md` | The framework's own accumulated learnings — the runner's read-on-demand sibling, synced read-only (adopters never edit it; they record project learnings in their `CLAUDE.md`) |
| `starter-kit/SAFEGUARDS.md` | Commit discipline, blast radius limits, mode-switching rules |
| `starter-kit/SESSION_NOTES.md` | Empty template for session continuity between sessions |
| `starter-kit/BOOTSTRAP.md` | Step-by-step setup guide for new projects |
| `starter-kit/CLAUDE_TEMPLATE.md` | Template for a project `CLAUDE.md` — SESSION PROTOCOL block and Adaptations section |
| `starter-kit/CONTEXT_TEMPLATE.md` | Project domain-glossary / `CONTEXT.md` template |
| `starter-kit/RECOMMENDED_SKILLS.md` | Index of recommended skills, cited at the relevant phase/workstream |
| `starter-kit/CHANGELOG.md` | Completed work history template — keeps BACKLOG.md lean |
| `starter-kit/HANDOFFS.md` | Durable close-out receipt template — one machine-checkable block per session |
| `starter-kit/ROADMAP.md` | Feature inventory and future plans template |
| `starter-kit/methodology_dashboard.py` | Health scanner — copy to project root for per-project dashboard |
| `starter-kit/methodology_trim.py` | Ledger trimmer — archives the oldest records of a grow-and-must-be-read ledger (`CHANGELOG.md`, `HANDOFFS.md`) into a frozen shard, and refuses to write unless the reconstruction is provably lossless. Dry-run by default; `--check` reports the trigger without writing. **Distributed since S39'** (`bin/_manifest.py`), so it lands at every adopter root beside the dashboard |

### Tools

| File | Purpose |
|------|---------|
| `tools/methodology_dashboard.py` | Portfolio health scanner — scores projects on activity, testing, docs, CI/CD, and methodology, where the 2nd and 5th dimensions adapt to the repo class (testing → render/verification for a doc-only repo; compliance → framework integrity for a repo that publishes the framework, overridable via `.methodology-profile`); generates HTML dashboard. Place in parent directory above project repos. Python 3 stdlib only, cross-platform. |
| `tools/test_methodology_dashboard.py` | Functional scoring tests for the health scanner (stdlib `unittest`). **Canonical-only** — not in `bin/_manifest.py`, so adopters do not receive it. Wired into `bin/tests.sh`; it imports only the `tools/` module and byte-compares the `starter-kit/` twin. Since S38 it also *loads* `starter-kit/methodology_trim.py` for the trim-row couplings, and still generates no `starter-kit/__pycache__` — `sys.dont_write_bytecode = True` is set before the imports (`:25`), which is what keeps that true rather than the import list. |
| `tools/test_methodology_trim.py` | Behaviour tests for the ledger trimmer (stdlib `unittest`, 66 tests). **Canonical-only.** Wired into `bin/tests.sh` as of S39' — before that the trimmer's own tests ran in nothing, which stopped being tolerable once `bin/sync` began installing the tool at adopter roots. Sets `sys.dont_write_bytecode` (`:34`) for the same reason its sibling does. |

### Workstreams (domain-specific adaptations)

| File | Domain |
|------|--------|
| `workstreams/DESIGN_WORKSTREAM.md` | UI/UX, visual design, layout |
| `workstreams/ARCHITECTURE_WORKSTREAM.md` | Systems, APIs, data models |
| `workstreams/DEVELOPMENT_WORKSTREAM.md` | Feature implementation, bug fixes |
| `workstreams/AUDIT_WORKSTREAM.md` | Code audits, security reviews |
| `workstreams/RESEARCH_DOCUMENTATION_WORKSTREAM.md` | Research papers, technical reports, dissertations, regulatory analyses |
| `workstreams/TEMPLATE_WORKSTREAM.md` | Blank template for creating new workstreams |

### Campaigns (multi-session work patterns within a workstream)

| File | Purpose |
|------|---------|
| `workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_CAMPAIGN.md` | Multi-session campaign template for exhaustive primary-source verification. Extends the Research Documentation workstream when per-session Phase 6 audit cannot complete the work. Supports both creation mode (writing) and audit mode (reviewing). |
| `workstreams/INHERITED_CODEBASE_FAMILIARIZATION_CAMPAIGN.md` | Multi-session campaign template for taking over an unfamiliar codebase. Extends the Audit workstream; feeds the Development workstream via a prioritized backlog. Supports interview mode (departing owner available) and archaeology mode (owner gone). |
| `workstreams/TEMPLATE_CAMPAIGN.md` | Blank template for creating new campaigns (parallel to `TEMPLATE_WORKSTREAM.md`). |

## Key Concepts to Preserve When Editing

- **SESSION_RUNNER.md documents 28 failure modes** with specific countermeasures. These are empirically derived from 1100+ sessions — do not remove or weaken them without strong justification. FMs 1–26 must not be renumbered; new FMs append at the end (e.g., FM #24 was appended in v2.3, FM #25 in v2.6, and FM #26 in v2.7; FM #27 was appended after these, not inserted).
- **Phase 0 (Orient) must remain mandatory and blocking** — the most common failure mode is agents skipping orientation and starting work immediately.
- **"1 and done" rule** — one deliverable per session, then close out. This is structural, not advisory. Since v2.7 the one deliverable MAY be a pre-declared verified vertical slice (issues #20/#21; `SESSION_RUNNER.md` §Vertical Slice Sessions) — the allowance adds a gate and removes no step; one capability never means a second capability.
- **Ghost session detection and ledger reconciliation** (Phase 0, step 6) exist because crashed sessions that leave no trace — or commits that never reached the `CHANGELOG.md` ledger — cause the next session to work from stale state.
- **Phase 1B (Claim the Session)** exists for the same reason — writing a stub before technical work ensures even crashed sessions leave evidence.
- **Minimum handoff requirements** (Phase 3D) are non-negotiable: key files with line numbers, gotchas, specific next steps. "Pick next from backlog" is explicitly insufficient.
- **Plan Mode exit trap** — Plan Mode auto-generates "Implement the following plan" as a preamble. The SESSION_RUNNER explicitly warns this does NOT mean "start coding."

## Versioning

Changes are tracked via git commits and the README's "What's New" section. Current version: v3.7.

This section owns **released-version semantics** — one narrated entry per shipped version. The repo's **per-action operational timeline** (including non-release work: housekeeping, doc-only PRs, adopter coordination, backlog grooming) lives in the root [`CHANGELOG.md`](CHANGELOG.md) action ledger; where the two overlap — a release — `CHANGELOG.md` carries a one-line pointer here rather than re-narrating, so the two ledgers cannot diverge.

The **narrated per-version history** — one entry for every release from v1.0 to v3.7 — lives in [`docs/RELEASE_HISTORY.md`](docs/RELEASE_HISTORY.md). **Read it when you need the semantics of a specific version**: what changed, why, and what it deliberately did not change. New releases append their entry there; this section keeps only the current-version line and the boundary rule above.

That pointer is a plain Markdown link and **must never become an `@`-import**, which is expanded into context every session (`starter-kit/BOOTSTRAP.md` Step 5) and would restore exactly the recurring cost the extraction removed — this file is auto-loaded, and the history was 86% of it. This is that step's own rule applied here: the always-loaded file stays scannable, the accumulated record moves to a sibling read on demand. The `## Versioning` heading stays put, so existing `CLAUDE.md#versioning` links still resolve.
