# Protocols: A Structural Addition to the Iterative Session Methodology

**Date:** 2026-04-25
**Status:** Proposal for review by the methodology lead

---

## Summary

The methodology currently recognizes three structural layers: principles (universal), phases (per-session), and workstreams (per-domain). It has no first-class concept for **multi-session campaigns** — work whose deliverable cannot be produced by a single session even when every session in the series is run cleanly. This proposal argues that this layer exists in practice, deserves a name (**protocols**), and benefits from being promoted to first-class status alongside workstreams. The change is structural but small: new vocabulary, a new section in `ITERATIVE_METHODOLOGY.md`, an orientation step in `SESSION_RUNNER.md`, and a documented place in the file hierarchy. No principle changes; no phase changes.

---

## The gap

The methodology's session-scope rules ([Principle 9](../../ITERATIVE_METHODOLOGY.md#9-session-scope-bounding)) are explicit: "Every session has exactly ONE deliverable." This is correct and load-bearing — it prevents the quality degradation that follows from cramming multiple deliverables into one session. The principle handles the in-session scope problem definitively.

What it doesn't handle is the **between-session** scope problem. Some deliverables cannot be produced in one session even when the work is decomposed correctly. Examples:

- Verifying every claim in a 5-paper research repository against its primary sources (~500 verification events; one session degrades long before it finishes)
- Familiarizing a new owner with a 40-module codebase inherited from a departing engineer (one session per module, plus planning, plus consolidation)
- Conducting a security-hardening pass across a system with 80+ endpoints (one session per cluster of related endpoints)

In each case, the methodology's per-session machinery applies cleanly. What's missing is a name and a structure for the campaign that *contains* those sessions. Without that name, multi-session work is either:

1. Compressed into one session (violating "1 and done" and producing the quality degradation that "1 and done" exists to prevent), or
2. Fragmented into ad-hoc sessions with no shared deliverable contract, no campaign-level checkpoints, and no resumability if one session crashes mid-campaign.

Both are failure modes the methodology already cares about. Both go unaddressed because the campaign layer isn't named.

---

## What a protocol is

A **protocol** is a multi-session campaign template. It prescribes a session sequence, deliverable contracts at each session boundary, and exit criteria for the campaign as a whole. Each session within a protocol still runs the methodology's 6 phases; the protocol coordinates *across* sessions toward a deliverable that no single session could produce.

| Layer | What it defines | Lifespan | Authored where |
|-------|-----------------|----------|----------------|
| **Methodology** | Universal principles, phases, gates | Always | `ITERATIVE_METHODOLOGY.md` |
| **Session Runner** | Per-session operating procedure | Per session | `SESSION_RUNNER.md` |
| **Workstream** | Domain-specific phase content | Per project / domain | `workstreams/*_WORKSTREAM.md` |
| **Protocol** *(proposed)* | Multi-session campaign template | Per campaign | `workstreams/*_PROTOCOL.md` |
| **Session** | Single bounded unit of work | Hours to a day | (instance, not template) |

A protocol is **not a workstream**. Workstreams adapt the 6 phases to a domain — they answer *"what does Phase 2 look like for UI design / for research papers / for audits?"* Protocols structure session sequences for one specific deliverable type within a workstream — they answer *"what is the N-session sequence to produce X?"*

A protocol is **not a planning-session output**. A planning session produces a bespoke plan for one campaign. A protocol is a reusable template — once written, it applies to every campaign of its type. The planning session for an exhaustive-verification campaign uses the protocol as its template, not its alternative.

---

## Why protocols need to be first-class

Three reasons, all grounded in the methodology's existing values.

### 1. Discoverability

Today, an agent or human starting multi-session work has no entry point. They can find a workstream that tells them how a single session in their domain should run, but nothing tells them *the campaign-level shape* their work should follow. They invent it ad-hoc, and the invention quality varies wildly across attempts.

A documented protocol library gives the same lift that the workstream library gave for single-session work: a known, validated starting point that prevents re-derivation.

### 2. Compounding (the methodology's primary value lever)

The methodology's [self-correcting loop (Principle 2)](../../ITERATIVE_METHODOLOGY.md#2-self-correcting-loop) makes individual sessions get better over time: failures become numbered anti-patterns; successes become named patterns; the methodology evolves. This loop currently operates at two scales — within a session and within the methodology itself — but not at the campaign scale.

When a multi-session campaign reveals a failure mode (e.g., "verdict drift across sub-agents in audit campaigns"), there is no document that anti-pattern can be added to. It either gets folded into the workstream (where it doesn't quite fit, since it's about cross-session coordination, not single-session work) or it gets lost.

A protocol document is the natural home. The protocol gets sharper every time it runs — the same compounding mechanism, applied at one layer up.

### 3. Audit and quality assurance

A campaign that follows a documented protocol can be audited against it. An ad-hoc campaign cannot — there's nothing to compare against. Given the methodology's emphasis on [honest accounting](../../ITERATIVE_METHODOLOGY.md#honest-accounting-framework) and bidirectional handoff scoring, this asymmetry matters: it leaves the largest, most expensive work in the least observable state.

---

## Two examples

### 1. The Research Exhaustive Verification Protocol (just written)

[`workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md`](../../workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md). A campaign template for guaranteeing every claim in a paper or repository has primary-source support. Decomposes into one planning session, N execution sessions (per paper or per section), and one consolidation session. Supports both creation mode (writing) and audit mode (reviewing).

This protocol exists because the Research Documentation workstream's Phase 6 Claim-Source Audit can't scale beyond a single paper section in one session. The campaign structure is what makes the discipline actually achievable on real-world deliverables.

### 2. Hypothetical: Inherited-Codebase Familiarization Protocol

A campaign template for taking over an unfamiliar codebase from a departing owner. One planning session (module map, scope boundaries, "ask the previous owner" question list); N execution sessions, one per major module (architecture diagram, dependency analysis, gotcha catalog); one consolidation session (portfolio-level architecture write-up, risk map, prioritized backlog).

Without a protocol, familiarization expands to fill all available time and produces inconsistent depth across modules. With a protocol, each module gets equal treatment, deliverable contracts force consistency, and the consolidation surfaces cross-module patterns the per-module work couldn't see. This is exactly the kind of high-stakes, error-prone, multi-session work the methodology was built to discipline — and it is exactly the work the methodology currently has nothing structured to say about.

Other protocols that would naturally fit: Performance Investigation, Dependency Modernization, Security Hardening, Post-Incident Review, Multi-Repo Refactor.

---

## What changes if protocols become first-class

A specific, scoped set of changes:

1. **`ITERATIVE_METHODOLOGY.md`** — add a new section after `## Session Types`, parallel to it, named `## Protocols and Multi-Session Campaigns`. ~200 words. Defines the layer, gives the criteria for when a protocol is appropriate vs. when a planning-session-and-go is appropriate.
2. **`SESSION_RUNNER.md`** — add one orientation step in Phase 0/1: *"Check whether this work has a documented protocol. If yes, follow its session sequence; if no, evaluate whether it should."*
3. **`CLAUDE.md` (this repo's)** — already done as part of the exhaustive-verification rollout. The Protocols subsection in the document hierarchy table now exists.
4. **`workstreams/TEMPLATE_PROTOCOL.md`** *(new)* — a blank template, parallel to `TEMPLATE_WORKSTREAM.md`, to make new protocols easy to create.
5. **README.md** — one bullet under "What's New" for the version that includes this; one row in the document hierarchy table.

That is the entire scope. No principle is added or removed. No phase is changed. No workstream is rewritten.

---

## What does not change

- The 9 principles remain load-bearing and unchanged.
- The 6 phases still apply per session. Every session in a protocol still runs them.
- Workstreams remain the right home for domain-specific phase content.
- Session-level discipline (handoff accountability, "1 and done", phase gates) is unchanged. Protocols *strengthen* "1 and done" by making decomposition into bounded sessions easier.
- The Session Runner remains the cockpit checklist. It gains one orientation step, not a redesign.

---

## Anticipated objections

**"Isn't this just a workstream?"** No. A workstream defines what the 6 phases look like in a domain. A protocol defines the sequence and deliverable contracts across multiple sessions for one specific deliverable type. A workstream may host many protocols (the Research Documentation workstream could host an Exhaustive Verification Protocol, a Multi-Paper Synthesis Protocol, and a Source Migration Protocol — each is a distinct campaign template).

**"Isn't this just what a planning session produces?"** A planning session produces a bespoke plan for one campaign. A protocol is reusable across campaigns of the same type. The planning session for a campaign uses the protocol as its template, not its alternative — same way a single session uses a workstream.

**"Doesn't this violate '1 and done'?"** It strengthens it. Without a protocol concept, multi-session work either gets crammed into one session (violating "1 and done") or fragments without structure. Protocols make decomposition into "1 and done" sessions easier, not harder, by providing the shape that decomposition should take.

**"Isn't this scope creep on the methodology itself?"** It would be, if the addition were principle-level or phase-level. It's not — it's a new vocabulary item and a small addition to the existing document hierarchy. The methodology already has a layer for "domain adaptation" (workstreams); this adds a layer for "campaign template" (protocols), which is a smaller and more bounded concept than workstreams.

**"Why now?"** The Research Exhaustive Verification work surfaced the gap. Without a name for the campaign layer, the protocol document had to be written as if it were a workstream, which it isn't. Naming the layer now makes the next protocol cheaper to write and clearer to invoke. (The same argument that justified naming workstreams in v1.0 instead of leaving them as ad-hoc per-domain documents.)

---

## Recommended next step

A planning session produces a transformation plan for promoting protocols to first-class. The plan would specify: exact text for the new `ITERATIVE_METHODOLOGY.md` section, exact text for the new `SESSION_RUNNER.md` step, the `TEMPLATE_PROTOCOL.md` skeleton, and the README/CLAUDE.md updates. That plan goes to the methodology lead for approval; an implementation session executes once approved.

The current state — one protocol exists in the workstreams directory but the concept of "protocol" is not named in the methodology — is the worst-of-both: a structural addition is implicit in the file tree without being named in the documentation. Either retract the protocol document and inline its content into the Research Documentation workstream (cheaper but loses the mechanism that makes the next protocol cheap), or promote the layer to first-class (small addition, repeatable benefit).

The proposal is the latter.
