# PR #14 Review — v2.6 Skill-Recommendation Convention

**PR:** [KJ5HST/methodology#14](https://github.com/KJ5HST/methodology/pull/14) — `feature/skill-recommendation-release`
**Reviewer:** rmsharp
**Review date:** 2026-05-25
**Author:** KJ5HST (Terrell Deppe)
**Status at review time:** open, no prior reviews, mergeable, +694/-16 across 12 files

---

## Verdict (TL;DR)

**Approve direction.** The convention — *methodology recommends; methodology does not reimplement* — is sound, the audit-doc provenance is exemplary, and the keep/drop/distill discipline against the 16-skill Pocock catalog is more rigorous than I would have applied if I'd built this myself.

**Ask for two changes before merge** (both low cost):

1. **CLAUDE.md "24 failure modes" line is stale-by-one** after FM #25 lands. Two-character fix.
2. **`RECOMMENDED_SKILLS.md` lists `/init` and `/fewer-permission-prompts` as cited in `BOOTSTRAP.md`, but neither is actually cited there.** Either add the citations or remove the entries.

**Three follow-on suggestions** worth considering before merge or in a v2.6.1, your call:

3. **Add an explicit FM-#2-via-skill-misuse paragraph** (the highest-value lift from PR #6 — content KJ5HST's silent-omission defense doesn't cover).
4. **Add a "Skills not recommended and why" subsection** to RECOMMENDED_SKILLS.md naming `/loop`, `/schedule`, `/to-issues`, `/tdd`, `/to-prd`, `/handoff`, `/zoom-out`, `/caveman` with one-line rationale (closes the door on future re-litigation).
5. **Phase 2.5 numbering** — half-phase notation breaks the "9 principles, 6 phases" framing the methodology has used since v1.0. Consider re-framing as a Phase 2 sub-step or naming it without a phase number.

**Karpathy-skills:** Evaluated separately at [`docs/planning/karpathy-skills-evaluation.md`](karpathy-skills-evaluation.md). Conclusion: out of scope for v2.6 — different category (behavioral overlay vs task workflow), no merge dependency. A possible follow-on PR if/when the methodology decides to address behavioral overlays as a category.

---

## 1. Context

### What PR #14 is

PR #14 introduces a new content layer (skill recommendations) alongside the existing layers (principles, phases, gates, workstreams, campaigns), under the principle: *if a discipline can be expressed as a Claude Code skill, methodology cites the skill at the relevant phase or workstream rather than re-documenting the discipline in its own voice.*

It also lands **six pieces of conceptual content distilled from a 16-skill audit** of Matt Pocock's repo (`docs/audits/2026-05-02-mattpocock-skills-evaluation.md`, 339 LOC, ships with the PR as provenance):

- FM #25 horizontal-slicing (appended; FMs 1–24 unchanged)
- Phase 3F commit-cleanup gate citing `/diagnose`
- New `starter-kit/CONTEXT_TEMPLATE.md` + Phase 2 read-step citing `/grill-with-docs`
- New Issue Lifecycle 5-state machine in DEVELOPMENT_WORKSTREAM citing `/triage`
- New Refactor Heuristics section in ARCHITECTURE_WORKSTREAM citing `/improve-codebase-architecture`
- New optional Phase 2.5 (Pre-Create Grill) citing `/grill-me`
- New Debugging Sessions as 4th session type citing `/diagnose`
- New BOOTSTRAP Step 10 pre-commit + git-guardrails paragraphs

Plus two refactors of existing content under the principle: Phase 3E body shortened to cite `/verify` and `/run`; AUDIT_WORKSTREAM gains a Light "Recommended Skills" callout.

### What's been considered already

The audit doc's "Implementation Status (re-framed 2026-05-25)" section is the most important context for any reviewer. It documents:

- 10 follow-up sessions (F1–F10) implemented on `experimental/pocock-audit` between 2026-05-02 and 2026-05-22
- An operator review on 2026-05-22 that paused the rollout when several F-commits were found to violate an emerging principle the methodology had not yet articulated
- A 2026-05-25 planning session that formalized the principle and produced PR #14's drop/keep/refactor framing

The drop list is substantial — 8 items including F1 (`block-dangerous-git.sh`), F5 body (full debug-loop section), F10 design (574 LOC), F10.A/B/C (three methodology-authored SKILL.md files), F10.0 + F10.0+ (bin/sync skill-directory support). **These are the right drops.** Each was a methodology-reimplementing a skill that exists upstream; the convention catches them.

### What hasn't been considered

PR #14 was built by drop/keep/refactoring KJ5HST's own F1–F10 branch. **The rmsharp fork PR #6 (opened 2026-05-02, never reviewed) was not in the visible decision set.** PR #6's premise was nearly identical (Pocock skills mapped onto methodology) but its execution emphasized FM-erosion defense in a way PR #14 doesn't. Mining #6 surfaces three things worth lifting (§4).

The audit also predates Pocock's repo evolution. Current Pocock catalog includes `/prototype` (engineering) and `/handoff` (productivity), neither of which appear in PR #14. Worth a separate audit-currency conversation (§3.7).

---

## 2. Standalone findings — must-fix

These are independent of PR #6 and karpathy. Both are low-cost.

### 2.1 CLAUDE.md FM-count stale-by-one

**File:** `CLAUDE.md` line 77
**Current:**

> SESSION_RUNNER.md documents **24 failure modes** with specific countermeasures. These are empirically derived from 60+ sessions — do not remove or weaken them without strong justification. FMs 1–23 must not be renumbered; new FMs append at the end (e.g., FM #24 was appended in v2.3, not inserted).

**Should be (after FM #25 lands):**

> SESSION_RUNNER.md documents **25 failure modes** with specific countermeasures. These are empirically derived from 60+ sessions — do not remove or weaken them without strong justification. FMs 1–24 must not be renumbered; new FMs append at the end (e.g., FM #25 was appended in v2.6, not inserted).

**Why this matters:** CLAUDE.md is the project-level orientation file every agent reads first. A stale count there will mislead future agents about the FM-count invariant the same sentence guards. Worth catching at PR-review time; same checklist applies for any future PR that appends an FM.

### 2.2 Aspirational citations in RECOMMENDED_SKILLS.md

**File:** `starter-kit/RECOMMENDED_SKILLS.md` (built-ins table)
**Issue:** Two entries claim citations that don't exist in the PR:

| Entry | Claimed citation | Actual state |
|---|---|---|
| `/init` | "`BOOTSTRAP.md` Step 4 — initializing `CLAUDE.md`" | `BOOTSTRAP.md` does not grep for `init`-as-skill anywhere |
| `/fewer-permission-prompts` | "`BOOTSTRAP.md` — permission setup" | Same — no grep hit in BOOTSTRAP.md |

Verified via `git show upstream/feature/skill-recommendation-release:starter-kit/BOOTSTRAP.md | grep -i "init\|fewer-permission"` — the only hit is the word "init" inside "initial setup" prose, not a skill citation.

**Two ways to fix:**
- **(a)** Add the citations to BOOTSTRAP.md (one paragraph each, parallel to the `/setup-pre-commit` and `/git-guardrails-claude-code` paragraphs Step 10 just gained).
- **(b)** Remove the two table entries until they have real citation sites.

I'd prefer (a) — both skills are genuinely useful at bootstrap, and removing them weakens the built-ins coverage. But (b) is fine if (a) is more work than the v2.6 release wants.

---

## 3. Standalone findings — should-consider

These are framing concerns, not blockers. Each can be deferred to v2.6.1 or a follow-on PR.

### 3.1 PR-body claim vs. actual scope

PR body says: *"No principle, phase, gate, or workstream changes."*

PR actually adds:
- **One new (optional) phase** — Phase 2.5 Pre-Create Grill, with its own "When this applies / When to skip / Why this phase exists" body
- **One new session type** — Debugging, taking the taxonomy from 3 → 4
- **One new content layer** — recommended skills, parallel to phases / principles / workstreams / campaigns
- **Phase 2 step renumber** 1→2..7→8

The claim is **technically defensible** (no *existing* phases or session types changed; the new ones are additive; the renumber is mechanical and the one cross-reference is by name) — but reviewers reading the headline framing will under-weight the additions. Worth tightening to something like:

> *No removal or modification of existing principles, gates, workstreams, or failure modes. Additions: one optional phase (2.5), one session type (Debugging, 4th), one content layer (recommended skills), one FM (#25, appended), Phase 2 step renumber 1→2..7→8.*

This is honest about scope while still signaling backward compatibility.

### 3.2 Phase 2.5 numbering breaks the "6 phases" framing

The methodology has been **"9 principles, 6 phases, 12 quality gates"** since v1.0 — that count appears in CLAUDE.md's introduction and README's "What This Is" framing. Adding "Phase 2.5" makes the count ambiguous: is it 6 phases or 6.5? 7? Even calling it "optional" doesn't remove the ambiguity — the section header is *literally* `### Phase 2.5: Pre-Create Grill (Optional)`.

Note: the methodology already has a precedent for **letter-suffixed sub-phases** — `Phase 1B (Claim the Session)` exists between Phase 1 and Phase 2. That precedent makes Phase 2.5's decimal notation the *outlier* in the existing naming scheme, and points at a hybrid option (Phase 2B) that better fits the established style.

**Five options worth considering:**

| Option | What it looks like | Pros | Cons |
|---|---|---|---|
| **(a) Keep as-is** | `### Phase 2.5: Pre-Create Grill (Optional)` | Minimum diff; preserves PR #14's framing as written | Breaks "6 phases" count ambiguously; decimal notation has no precedent in methodology |
| **(b) Phase 2 sub-step** | `### Phase 2 Step 9: Pre-Create Grill (Optional)` | Preserves "6 phases" exactly | Conceptually awkward — the grill is *pre*-Create, not part of Research |
| **(c) Drop the phase number** | `### Pre-Create Grill (Optional, between Research and Create)` | Preserves "6 phases"; makes optionality salient; fits actual position | Section loses phase-level structural identity; harder to cross-reference ("see Phase ??") |
| **(d) Phase 2B hybrid** | `### Phase 2B: Pre-Create Grill (Optional)` (existing Research steps stay as Phase 2 or recast as Phase 2A) | Preserves "6 phases"; uses established Phase 1B precedent; gives phase-shaped identity without integer renumber; letter suffix carries less ordinality than a decimal | Mild Phase 2A/2B ambiguity (does Phase 2A include all 8 Research steps?); needs one clarifying sentence |
| **(e) Renumber 2.5→3, cascade 3→4 ... 6→7** | `### Phase 3: Pre-Create Grill (Optional)`; old Phase 3 Create → Phase 4 Create; … old Phase 6 Verify & Close → Phase 7 Verify & Close | Most honest about adding a phase; clean integer numbering; one-time accounting cost | Largest cross-reference blast radius (every numbered phase reference everywhere — `SAFEGUARDS.md`, every workstream, every campaign, CLAUDE.md, HOW_TO_USE, all FM countermeasure cells); breaks PR #14's "no phase change" claim explicitly; gives an optional grill the same visual weight as the gated phases; **downstream adopters' existing SESSION_NOTES, planning docs, CHANGELOG entries, and commit history reference the old numbers** — a handoff note saying "complete Phase 5 before proceeding" now means a different phase pre- and post-v2.6 |

**Recommended order:**

1. **(d) Phase 2B** — strongest on most axes. The Phase 1B precedent makes it consistent with existing methodology naming; the letter suffix communicates "inserted activity" without carrying integer-phase weight; "6 phases" count survives. Probably the option PR #14 *should* have used — it has precedent, preserves count, and gives the optional grill exactly the right weight (phase-shaped but not gated).
2. **(c) Drop the phase number** — most explicit about optionality. Best if (d) is rejected for the Phase 2A/2B ambiguity.
3. **(e) Renumber** — most honest, but expensive. Justified if the methodology is willing to accept that v2.6 *did* add a phase and is willing to pay the cross-reference cost. The downstream-adopter citation drift is the strongest argument against — adopters' existing references to "Phase 5" or "Phase 6" stop meaning the same thing across the v2.5/v2.6 boundary. That's a coordination tax v2.5's render-discipline addition explicitly avoided by not renumbering anti-patterns; consistency argues against renumbering phases either.
4. **(a) Keep as-is** — works, but the decimal notation is the outlier vs. the existing Phase 1B precedent.
5. **(b) Phase 2 Step 9** — awkward conceptual fit; not recommended.

The single most useful question for KJ5HST: *given that Phase 1B is already in the framework, why didn't Phase 2B get the same treatment?* The answer probably surfaces the right choice between (d) and (e).

### 3.3 `CONTEXT_TEMPLATE.md` couples to a Claude Code-specific feature

`starter-kit/CONTEXT_TEMPLATE.md` includes a section "CONTEXT.md vs auto-memory: when to use which" with a side-by-side table. **Auto-memory is a specific Claude Code feature**, not a general agent capability. The methodology has historically positioned itself as **agent-independent** — `README.md` line 232 explicitly says:

> The framework is agent-independent — it works with any AI coding agent that supports persistent files and session-based interaction.

Naming "auto-memory" specifically introduces a Claude-Code-shaped contract that other agents may not honor. Two fixes:

- **(a)** Generalize: "agent-level memory or cross-project preferences" instead of "auto-memory" — preserves the conceptual distinction without naming a specific implementation
- **(b)** Add a footnote: "Auto-memory is a Claude Code-specific feature; equivalent capabilities in other agents (Cursor memories, Cody preferences, etc.) are the analog" — preserves the example but acknowledges the genre

Either is fine; (a) is cleaner. This is the kind of coupling that's hard to walk back later, so worth catching now.

### 3.4 `CONTEXT_TEMPLATE.md` uses rad-con as a concrete example

The template includes:

> *Example: "rad-con is a desktop ham-radio control suite (Java 17 + Vue 3 + optional Tauri shell) that pairs a hardware-CAT layer with a digital-modes pipeline. Three coexisting decoder strategies (in-process Java, JNI, jt9 subprocess) trade off licensing and performance differently."*

Plus a domain-vocabulary example (`nzhsym`, FT8 decoder) and a load-bearing-constraint example (jt9 GPLv3 boundary).

These are **excellent grounding** for someone reading the template who wants to see what a real CONTEXT.md looks like — but they leak portfolio-specific context (rad-con is KJ5HST's project) into the public methodology starter-kit. The other starter-kit templates (SESSION_NOTES.md, CHANGELOG.md, ROADMAP.md) use generic placeholders, not specific project names.

**Two readings:**
- *Intentional* — grounding the abstract in real examples is pedagogically valuable, and the rad-con project is open-source so this isn't private context
- *Leak* — coupling a public methodology artifact to a specific portfolio project hardens an example that future projects may diverge from

If intentional, the template should say so: "The examples below are from KJ5HST's `rad-con` project (a worked instance); replace with your project's specifics." If unintentional, generalize the examples to fictional but plausible projects (e.g., a calculator service, a payment processor — the same pattern starter-kit/SESSION_NOTES.md uses).

### 3.5 Workstream citation patterns are inconsistent

Across the three workstreams PR #14 touches, the citation pattern differs:

| Workstream | Citation style |
|---|---|
| `AUDIT_WORKSTREAM.md` | Dedicated `## Recommended Skills` section near top, table-format |
| `DEVELOPMENT_WORKSTREAM.md` | No dedicated section; citation embedded inside the Issue Lifecycle subsection's last paragraph |
| `ARCHITECTURE_WORKSTREAM.md` | No dedicated section; citation embedded inline at end of Refactor Heuristics |

Future contributors adding new workstream skills will not know which pattern to follow. Two ways to converge:

- **(a)** Promote the AUDIT_WORKSTREAM pattern to convention: every workstream gets a `## Recommended Skills` section near the top, in table format. DEV and ARCH grow one each in this PR.
- **(b)** Document the existing variety: a short note in `RECOMMENDED_SKILLS.md` or `HOW_TO_USE.md` saying "skills cited at the point of recommendation; a dedicated Recommended Skills section is appropriate when ≥2 skills apply" and leaving the choice to the contributor.

I lean (a) for symmetry. The AUDIT_WORKSTREAM table is the cleanest pattern — three rows for `/code-review`, `/review`, `/security-review` — and that shape generalizes.

### 3.6 Pocock's `/handoff` skill is unaddressed

Pocock has shipped `productivity/handoff` since the 2026-05-02 audit. The skill:

> *Compact the current conversation into a handoff document for another agent to pick up. Save to the temporary directory of the user's OS — not the current workspace.*

This is **directly adjacent** to methodology's core mechanism — Phase 3D's minimum-handoff requirements and the bidirectional scoring loop that makes session N+1 better than N. **It's also conceptually opposite:**

| | Pocock `/handoff` | Methodology handoff |
|---|---|---|
| Storage | OS temp directory | Repo-versioned `SESSION_NOTES.md` |
| Scope | Single-user, single-arc | Cross-session, score-driven |
| Lifecycle | Ephemeral; lost on reboot | Permanent; informs the next session's audit |
| Audience | A fresh agent in the same conversation | A future session's agent (and an auditor) |

This is **the most important Pocock-skill non-citation** in PR #14, because it's the one most likely to be misused as a substitute for methodology's discipline. Suggested addition to `RECOMMENDED_SKILLS.md` (or a new "Skills not recommended and why" subsection, §3.4 of this review):

> **`/handoff` (Pocock)** is not recommended as a substitute for methodology's handoff discipline. The skill writes ephemeral compaction to OS temp; methodology requires repo-versioned handoff notes scored by the next session. The two target different scopes — `/handoff` is useful for context-window pressure within one session arc, but Phase 3D's minimum handoff requirements apply at session close regardless.

### 3.7 Audit currency

The audit is dated 2026-05-02; the PR is dated 2026-05-25 (23 days later). In that window Pocock has shipped at minimum `/prototype` and `/handoff`. There's no documented stance on what triggers a re-audit. **Worth a brief note in `RECOMMENDED_SKILLS.md` or as a follow-on principle:** does methodology re-audit Pocock's repo on a calendar (quarterly?), on a trigger (when a new skill ships?), or trust adopters to track changes themselves?

My read: methodology should claim a **pin-not-track** posture — the SHA pinning already does most of this work — and explicitly disclaim a commitment to continuous re-audit. Adopters who want cutting-edge Pocock skills should track upstream themselves; methodology's index is a *vetted snapshot*, not a *live feed*. A sentence on this would prevent the index from looking stale by drift.

---

## 4. Lifts from PR #6 worth incorporating

PR #6 (rmsharp fork, opened 2026-05-02, never reviewed, conflicting) has been functionally superseded by PR #14. Three pieces of its content **uniquely** address gaps in PR #14.

### 4.1 FM-#2-via-skill-misuse paragraph — highest-value lift

**The single most valuable lift from PR #6.** PR #14 defends against skill-induced FM erosion **silently** — by omitting gate-crossing skills (`/to-issues`, `/tdd`, `/to-prd`, `/simplify`) from RECOMMENDED_SKILLS.md. The audit doc explicitly justifies this for `/to-issues` (rejected as covered by Learning #30), `/to-prd` (rejected as covered by Planning Sessions), and `/tdd` (kept naming only).

**The problem:** silent omission doesn't reach adopters who install the full Pocock skill set independently (e.g., from `/plugin marketplace`). Those adopters have access to `/to-issues` and `/tdd` and may use them without the FM #2 caveat. The skill citation discipline assumes adopters only know about skills the methodology recommends — but in practice they will encounter skills the methodology *deliberately omitted* and may not know why.

**PR #6's framing addresses this directly:**

> A skill that pulls you across a hard gate — e.g., `/to-issues` immediately followed by `/tdd` — is failure mode #2 (Keep going) wearing a tool costume. Close out first.

This sentence belongs in PR #14. Two reasonable homes:

- **(a)** `ITERATIVE_METHODOLOGY.md` §Recommended Skills, appended as a final paragraph
- **(b)** `RECOMMENDED_SKILLS.md`, in a new "When a recommended skill bypasses methodology" subsection paired with the existing "When a recommended skill is unavailable" subsection

I'd lean (a) — it puts the FM defense at the same level as the recommend-don't-reimplement principle. Both are about the same concern: skills as tools, not phase-replacements.

**Suggested wording** (light edit of PR #6's):

> **A skill is not a phase.** A recommended skill that pulls a session across a hard gate — e.g., `/to-issues` followed immediately by `/tdd`, or any skill that produces an artifact and continues to the next artifact in the same session — is failure mode #2 (keep-going) wearing a tool costume. Close out first. The methodology recommends skills as sharper instruments for specific phases; it does not authorize them to compress two sessions into one.

### 4.2 Explicit "Skills not recommended and why" subsection

PR #6 explicitly excludes `/loop` and `/schedule` with a one-line rationale ("orchestration, not engineering, and would muddy the discipline message"). PR #14 silently doesn't cite them.

**Generalize PR #6's pattern** into a subsection that names the skills the methodology *intentionally* doesn't cite, with one-line rationale each. This closes the door on future re-litigation and makes the audit-doc decisions discoverable from `RECOMMENDED_SKILLS.md` itself rather than only from the 339-LOC audit.

Suggested entries (synthesized from PR #6 + audit doc + my own §3.6):

| Skill | Why not cited |
|---|---|
| `/loop`, `/schedule` (Claude Code built-ins) | Orchestration, not engineering. Methodology phases are sequential and gated; loop/schedule belong above the session, not inside it. |
| `/to-issues` (Pocock) | Covered by Learning #30 (table-first, decisions batch, parallel creation). Methodology version is materially more rigorous. |
| `/to-prd` (Pocock) | Covered by Planning Sessions discipline. `/to-prd` is "synthesize what's been discussed"; methodology's planning discipline requires grep-verified evidence inventories (per FM #19). |
| `/tdd` (Pocock) | TDD's vertical-slicing framing is incorporated as FM #25; the red-green-refactor workflow is left to adopter preference. |
| `/handoff` (Pocock) | Targets ephemeral single-arc compaction; methodology requires repo-versioned cross-session handoffs (Phase 3D). Different scope, not a substitute. See §3.6 of this review. |
| `/caveman` (Pocock) | Stylistic compression; methodology's length discipline (Learning #34: ≤150 lines for handoffs) addresses token reduction without changing voice. |
| `/zoom-out` (Pocock) | Covered better by Learnings #28/#29 (Plan-subagent architecture surveys with file:line citations). |
| `/write-a-skill` (Pocock) | Methodology doesn't ship its own skills (per the v2.6 principle). Becomes relevant only if that posture changes. |

This subsection serves two audiences: (a) reviewers who want to know "why isn't X here?", (b) future contributors who might re-propose a citation that's already been considered.

### 4.3 Per-skill setup-prerequisites note

PR #6 surfaced a concept PR #14 partially adopts but doesn't fully address: **some recommended skills need per-repo config to run.** PR #6 proposed `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, `docs/agents/domain.md` as a scaffold pattern.

PR #14 introduces `starter-kit/CONTEXT_TEMPLATE.md` which covers the `domain` slot, but `/triage` needs label vocabulary and `/diagnose` may need a feedback-loop template that aren't covered.

**Suggested addition** to each RECOMMENDED_SKILLS.md entry that has prerequisites: a single "Setup:" line. Example:

| Skill | Recommended at | Setup |
|---|---|---|
| `/triage` | `DEVELOPMENT_WORKSTREAM.md` §Issue Lifecycle | Requires per-repo label vocabulary; see `docs/agents/triage-labels.md` (template forthcoming) |
| `/grill-with-docs` | `ITERATIVE_METHODOLOGY.md` §Phase 2 | Requires `CONTEXT.md`; see `starter-kit/CONTEXT_TEMPLATE.md` |

This is a smaller lift than (4.1) and (4.2). Worth doing but not blocking.

### 4.4 Other PR #6 content not worth lifting

For completeness:

- **PR #6's `docs/skills.md` cites `/simplify`** which does not exist in Pocock's repo (verified against current `mattpocock/skills` catalog). This is a bug in PR #6, not material to lift.
- **PR #6's `/setup-matt-pocock-skills` recommendation** was explicitly rejected by the audit; don't relitigate.
- **PR #6's workstream-level 3-line citation blocks** are superseded by PR #14's more thorough workstream-by-workstream treatment.
- **PR #6's HOW_TO_USE.md addition** is superseded by PR #14's HOW_TO_USE Phase 2 read-step illustration (Example 2).

After PR #14 merges and these lifts (or whichever the author accepts) land, PR #6 should be **closed** with a comment pointing at PR #14 as the upstream successor.

---

## 5. Suggested verdict on GitHub

**COMMENT** (not APPROVE or REQUEST CHANGES) — the convention is sound and the implementation is rigorous, but the two must-fix items (§2.1, §2.2) deserve at least a "noted, fix in v2.6.1" acknowledgment before merge.

If KJ5HST wants to land §4.1 (the FM-#2 paragraph) in this PR, that pushes the verdict closer to "REQUEST CHANGES with one-paragraph addition pending"; if they prefer it as a follow-on, COMMENT is the right shape.

The other items (§3, §4.2, §4.3) can all be follow-on PRs. They're not blockers; they're improvements I'd rather see filed than forgotten.

---

## 6. Items explicitly out of scope for this review

- **Audit currency posture** (§3.7) — a substantive forward question but not a PR #14 blocker.
- **Phase 2.5 numbering** (§3.2) — framing, not content; merge-then-fix is fine.
- **Karpathy-skills inclusion** — evaluated separately at [`karpathy-skills-evaluation.md`](karpathy-skills-evaluation.md). Different category, no merge dependency.
- **PR #6 closure mechanics** — separate task (close with pointer to PR #14 + this review).
- **`CONTEXT_TEMPLATE.md` adoption tracking** — when adopters start writing CONTEXT.md files, are there dashboard metrics? Out of scope here; raised once for awareness.

---

*Generated 2026-05-25 in support of reviewing [KJ5HST/methodology#14](https://github.com/KJ5HST/methodology/pull/14). This is a fork-local planning artifact; not intended for upstream.*
