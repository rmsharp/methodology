# Pocock skill enablement gap: decide methodology's strategy before any v2.7 work

**Type:** Strategy / proposal-of-work. No PR attached.
**Investigator:** rmsharp, 2026-05-27, Session 1 of a multi-session investigation.
**Backing material:** [`docs/planning/skill-enablement-gap-investigation.md`](https://github.com/rmsharp/methodology/blob/feature/skill-enablement-investigation/docs/planning/skill-enablement-gap-investigation.md) on branch `feature/skill-enablement-investigation` of `rmsharp/methodology` (full S1–S10 / R1–R10 signal lists, per-skill phase-compression table, provenance, 7 verbatim SKILL.md fetches at pinned SHAs).

---

## 1. The gap, in one sentence

Methodology v2.6 cites seven Pocock skills in `starter-kit/RECOMMENDED_SKILLS.md`. Two of them (`/improve-codebase-architecture`, `/grill-with-docs`) read or modify files (`CONTEXT.md`, `docs/adr/`, `LANGUAGE.md`) that `BOOTSTRAP.md` neither references nor copies; a third (`/diagnose`) consults a domain glossary and ADRs when present; a fourth (`/triage`) recommends running `/setup-matt-pocock-skills`, which methodology's "Skills not recommended" subsection explicitly declines.

An adopter who follows `BOOTSTRAP.md` Steps 1–9 verbatim ends up unable to satisfy three of the seven cited skills, and unable to satisfy the fourth without violating a v2.6 decision.

## 2. How the gap was found

Operator (rmsharp) report, 2026-05-27: invoking `/improve-codebase-architecture` on a methodology-adopting repo flagged missing files the adopter had never been instructed to create.

Verbatim from `/improve-codebase-architecture` SKILL.md (SHA `a36584e09eae`):

> *"Find deepening opportunities in a codebase, informed by the domain language in CONTEXT.md and the decisions in docs/adr/."*

Verbatim from `/grill-with-docs` SKILL.md (SHA `e7df78bb81da`):

> *"Create files lazily — only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed."*

The two skills compose: `/grill-with-docs` lazy-creates the same files `/improve-codebase-architecture` reads.

Verbatim from `/triage` SKILL.md (SHA `179a14e72103`):

> *"These are canonical role names — the actual label strings used in the issue tracker may differ. The mapping should have been provided to you — run `/setup-matt-pocock-skills` if not."*

Methodology's [`starter-kit/RECOMMENDED_SKILLS.md`](../starter-kit/RECOMMENDED_SKILLS.md) §"Skills not recommended (and why)" declines `/setup-matt-pocock-skills`.

## 3. Per-skill dependency catalog (verbatim-verified)

| Skill | Files expected | Self-creates? | Methodology ships template? | `BOOTSTRAP.md` ensures? | Gap? |
|---|---|---|---|---|---|
| `/git-guardrails-claude-code` | `.claude/hooks/`, `.claude/settings.json` | Yes | n/a | Step 10 recommends | No |
| `/grill-me` | None | n/a | n/a | n/a | No |
| `/grill-with-docs` | `CONTEXT.md`, `docs/adr/` | Yes, lazy | `CONTEXT_TEMPLATE.md` ✓; no ADR template | No copy step | **Documentation gap** |
| `/diagnose` | Glossary + ADRs (consultative) | No | `CONTEXT_TEMPLATE.md` ✓; no ADR | No | **Soft gap** |
| `/triage` | `AGENT-BRIEF.md`, `OUT-OF-SCOPE.md`, `.out-of-scope/`, issue-tracker label mapping | Partial; recommends `/setup-matt-pocock-skills` | None | No | **Contradiction** |
| `/improve-codebase-architecture` | `CONTEXT.md`, `docs/adr/`, `LANGUAGE.md` | No | `CONTEXT_TEMPLATE.md` ✓; no ADR; no LANGUAGE | No | **Missing files** |
| `/setup-pre-commit` | `package.json`, lockfile | Creates `.husky/`, `.lintstagedrc` itself | n/a | Implicit | No |

Three out of seven cited skills have no gap. Three have file-shaped gaps. One has the `/triage` contradiction.

## 4. Why this is a decision, not a bug

The natural fix — ship `ADR_TEMPLATE.md` (and maybe `LANGUAGE_TEMPLATE.md`) and have `BOOTSTRAP.md` Step 2 copy them — contradicts the load-bearing v2.6 principle:

> *"methodology recommends; methodology does not reimplement"*
> — `ITERATIVE_METHODOLOGY.md` §Recommended Skills

Shipping templates that duplicate the file-creation behavior already inside Pocock's `/grill-with-docs` is reimplementation.

There is also a second, runtime concern. The two highest-gap skills (`/improve-codebase-architecture`, `/grill-with-docs`) are also the two skills with the highest phase-compression risk — they each span Phase 2 (Research) → Phase 3 (Create) → Phase 5 (Implement) in a single invocation. Methodology's only safeguard today is a textual principle in `ITERATIVE_METHODOLOGY.md` §Recommended Skills (added 2026-05-24, commit `f1d1fbf`):

> *"A skill is not a phase. A recommended skill that pulls a session across a hard gate ... is failure mode #2 (keep-going) wearing a tool costume. Close out first."*

That principle has no mechanical enforcement — and, as of 2026-05-28, its conceptual ground is shifting underneath it. Upstream issues **#20** (redefine "1 and done" to allow a verified *vertical slice* — one capability across all layers in a single session, gated on a pre-declared plan-mode contract and per-layer verification) and **#21** (guardrails for that model, including a new failure mode, *"mega-session masquerading as a vertical slice"*) reframe exactly the territory the bounding axis occupies. A skill that pulls a session across Phase 2→3→5 *is* a tool-driven vertical slice; whether that is legitimate is precisely #20's question, and *"a skill is not a phase"* is the special case of #21's proposed failure mode where the slice arrives wearing a skill costume. **The bounding axis is therefore downstream of #20/#21** — its vocabulary and its enforcement story should inherit whatever those issues settle, not get re-invented here.

So the decision still has two orthogonal axes — each is an independent question, and a chosen strategy answers both:

- **Enablement axis.** How (if at all) does methodology help an adopter satisfy the file prerequisites the skills expect (`CONTEXT.md`, `docs/adr/`, `LANGUAGE.md`)?
- **Bounding axis.** How (if at all) does methodology *bound* — set limits on — a skill's tendency to compress Phase 2 → 3 → 5 into one invocation and cross hard gates, consistent with the vertical-slice model #20/#21 are defining?

Each axis is set independently. Some answers preserve "methodology recommends; methodology does not reimplement"; some erode it.

## 5. Damage axes

Detailed signal lists live in the backing planning doc (§4). The headline:

| Axis | What it measures | Who feels it |
|---|---|---|
| **Static** | Damage to methodology documents at rest | Every adopter — most painfully, those who never use a Pocock skill |
| **Runtime** | Damage to methodology's functional value during a session | Adopters who use a Pocock skill |

Static signals worth highlighting:

- **S4 Agent-independence.** Pocock skills are Claude Code–specific. README line 232 states methodology is "agent-independent." Framework files (`ITERATIVE_METHODOLOGY.md`, workstreams, `SESSION_RUNNER.md`, `SAFEGUARDS.md`) must remain Claude-Code-free for that claim to hold.
- **S5 Principle preservation.** Does the change ship a template that duplicates an external skill's file-creation? If yes, "methodology recommends; does not reimplement" no longer holds.
- **S7 Non-using-adopter friction.** Does an adopter who never invokes a Pocock skill see new required bootstrap reading?

Runtime signals worth highlighting:

- **R1–R5.** Are Phase 0 Orient, Phase 1B Claim, Phase 4 Present gate, "1 and done", and Phase 3D handoff preserved when a skill is invoked?
- **R10.** Does *"a skill is not a phase"* fire when the skill tries to pull across a hard gate?

## 6. Five plausible strategies

The full 28-combination matrix is in the backing doc. The five that pass static damage screening:

| # | Pairing | Static cost | Runtime protection | When this is right |
|---|---|---|---|---|
| **A** | **Never + None.** Methodology does not change; existing principle is the only control. | Zero | Principle-only | Operator believes Pocock-skill compatibility is outside methodology's commitment surface. |
| **B** | **Never + Per-skill phase map.** No bootstrap change; `RECOMMENDED_SKILLS.md` adds a "Phases spanned" column. | Trivial (one column) | Awareness-based | Methodology stays out of bootstrap but publishes structural runtime information. |
| **C** | **Reactive + Per-skill phase map.** Same as B plus per-request bootstrap support via CLAUDE.md adaptations when an adopter asks. | Trivial | Awareness-based | Recommended for adopters who want enablement on request, without baking it into starter-kit. |
| **D** | **Reactive (templated) + Per-skill break-point guidance.** One commented-out paragraph in `CLAUDE_TEMPLATE.md` that adopters uncomment; explicit Phase-gate break-point guidance for the two high-risk skills in `RECOMMENDED_SKILLS.md`. | Small | Explicit | Methodology hints at bootstrap and provides explicit runtime safeguards for the two highest-risk skills. |
| **E** | **Preemptive A + Strengthened "A skill is not a phase".** `BOOTSTRAP.md` names `/grill-with-docs` as the seeding tool; `RECOMMENDED_SKILLS.md` adds a "Prerequisites" column; the existing principle gets concrete per-high-risk-skill examples. | Medium | Explicit | Methodology commits to enablement and reinforces the runtime principle. |

Excluded from this shortlist is the family of strategies in which **methodology itself ships the prerequisite templates** — e.g. an `ADR_TEMPLATE.md` (and perhaps a `LANGUAGE_TEMPLATE.md`) that `BOOTSTRAP.md` copies into the adopter's repo. They fail the **S5 principle-preservation** check (§5): `/grill-with-docs` already creates `CONTEXT.md` and `docs/adr/` itself, so shipping methodology templates for the same files duplicates an external skill's file-creation behavior — exactly the reimplementation that *"methodology recommends; methodology does not reimplement"* forbids. That is why every pairing on the A–E shortlist keeps file-creation on the skill's side (or in the adopter's own CLAUDE.md), never in a methodology-shipped template.

One caveat on the **bounding half** of each pairing (the second term in each *"enablement + bounding"* name — what the pairing does to protect methodology's phases). Every bounding mechanism on this shortlist is framed in today's phase-compression vocabulary: pairings **B/C** propose a *per-skill phase map* (a "Phases spanned" column in `RECOMMENDED_SKILLS.md` recording which phases each skill can cross); **D** proposes *break-point guidance* (prose telling the adopter where to stop a high-compression skill and apply methodology's gates); **E** strengthens the existing *"a skill is not a phase"* principle. If #20/#21 land, that vocabulary becomes "vertical slice" and the stop-point becomes the slice-contract gate. None of A–E is invalidated by that shift, but the bounding half of whichever pairing is chosen should be *expressed* in the model #20/#21 settle on rather than the pre-#20 framing used here (see §4).

## 7. The `/triage` contradiction (separate decision)

`/triage` recommends `/setup-matt-pocock-skills` to establish label mappings; methodology declines that skill. Three resolutions:

| # | Resolution | Effect | Cost |
|---|---|---|---|
| 1 | **Drop.** Remove `/triage` from `RECOMMENDED_SKILLS.md`; move to "Skills not recommended". | Reverses a v2.6 audit decision; minus one cited skill. | Low |
| 2 | **Document.** Add a label-init paragraph to `DEVELOPMENT_WORKSTREAM.md` §Issue Lifecycle, replacing what `/setup-matt-pocock-skills` would do. | Tracks a Pocock convention by hand; the document drifts if Pocock changes the canonical roles. | Medium |
| 3 | **Footnote.** Keep `/triage` cited; add a note in its `RECOMMENDED_SKILLS.md` row acknowledging the prereq contradiction. | Adopter is informed; methodology takes no position. | Low |

Independent of the §6 choice and can be deferred.

## 8. Decisions requested

1. **Enablement-axis choice (and bounding-axis choice).** Among the five pairings A–E in §6, which (if any) does methodology pursue? "None of the above" is a valid answer. Note: the bounding half can reasonably be **deferred until #20/#21 resolve** (§4), since it should inherit their vertical-slice vocabulary; the enablement half is decidable now.
2. **`/triage` resolution.** Drop, Document, or Footnote (§7)? Defer is also acceptable.
3. **Implementation form, if any.** If a pairing is chosen, should the resulting work land as: (a) a single upstream PR; (b) one PR per axis; (c) a Methodology Roadmap entry first, then PR?

A "no change" answer is fully expected and is one of the strategy table's two zero-cost options.

## 9. What this issue is not

- It is not a proposal for a specific change. It is a request for the strategy decision that bounds any S3 implementation.
- It does not subsume #15 (Phase 2.5 naming), #16 (`CONTEXT_TEMPLATE.md` auto-memory generalization), #17 (workstream citation pattern), or #19 (cross-reference completeness as Learning). Those remain orthogonal.
- It is, by contrast, **coupled to** #20 (vertical-slice redefinition of "1 and done") and #21 (its guardrails) — not orthogonal. They redefine the runtime model the bounding axis lives in (§4). This issue does not subsume them and should not be decided ahead of them *on the bounding axis*; the enablement axis is independent of both.

## 10. Provenance

All 7 cited Pocock SKILL.md files were verbatim-fetched at their `RECOMMENDED_SKILLS.md`-pinned SHAs for this investigation:

- `/git-guardrails-claude-code` at `62f43a18177b`
- `/grill-me` at `62f43a18177b`
- `/grill-with-docs` at `e7df78bb81da`
- `/diagnose` at `7afa86d3a5dd`
- `/triage` at `179a14e72103`
- `/improve-codebase-architecture` at `a36584e09eae`
- `/setup-pre-commit` at `62f43a18177b`

The verbatim `/diagnose` fetch surfaced the soft glossary/ADR dependency that initial subagent enumeration had missed. The verbatim `/triage` fetch confirmed the `/setup-matt-pocock-skills` contradiction is in the canonical skill body, not adopter folklore.

Backing doc: [`docs/planning/skill-enablement-gap-investigation.md`](https://github.com/rmsharp/methodology/blob/feature/skill-enablement-investigation/docs/planning/skill-enablement-gap-investigation.md).
