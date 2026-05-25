# Karpathy-Skills Evaluation — Possible Follow-On to v2.6

**Date:** 2026-05-25
**Author:** rmsharp
**Status:** Evaluation only — no PR proposed. Surfaced during review of [KJ5HST/methodology#14](https://github.com/KJ5HST/methodology/pull/14) (v2.6 skill-recommendation convention). Split out from `pr14-review.md` to keep that review focused on PR #14's actual scope.

---

## Why this came up

PR #14 introduces the convention *methodology recommends; methodology does not reimplement* and ships a `starter-kit/RECOMMENDED_SKILLS.md` index of Pocock community skills + Claude Code built-ins. A reasonable follow-on question, once that convention is live: does the methodology's recommendation pattern extend to *behavioral overlays* like [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)?

The short answer: probably not, but not for the reason it sounds. Karpathy-guidelines isn't a worse-quality skill; it's a different *category* of artifact than PR #14's convention was built to handle. Treating that distinction as a content question would be wrong; it's a vocabulary question — what does "recommended skill" mean in the methodology, and what's the next category-up if behavioral overlays don't fit?

## What karpathy-skills is

`multica-ai/andrej-karpathy-skills` is a single-skill repository at `forrestchang/andrej-karpathy-skills` (also distributed via the Multica plugin marketplace).

- **One skill:** `karpathy-guidelines`. Distributed as both `SKILL.md` (Claude Code plugin) and `CLAUDE.md` (per-project drop-in)
- **License:** MIT
- **Provenance:** Distilled from [Andrej Karpathy's 2026-04 X post](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls
- **Content:** Four behavioral principles —
  1. **Think Before Coding** — surface assumptions, present interpretations, push back when warranted
  2. **Simplicity First** — minimum code, no speculative features, no abstractions for single-use, no error handling for impossible scenarios
  3. **Surgical Changes** — touch only what you must, don't improve adjacent code, don't refactor what isn't broken, match existing style
  4. **Goal-Driven Execution** — transform tasks into verifiable goals, loop until verified

## Category assessment

Karpathy-guidelines is **a behavioral overlay**, not a task workflow. This makes it a different category from Pocock's skills:

| | Pocock skills | Karpathy-guidelines |
|---|---|---|
| Genre | Task workflow (do TDD, do triage, do diagnosis) | Behavioral overlay (don't overengineer, don't refactor adjacent code) |
| Invocation | Slash command at a specific moment | Always active, applies to every edit |
| Granularity | Single session task | Sub-edit behavior |
| Citation site | A specific phase or workstream | Everywhere, all the time |

PR #14's convention — *cite skills at the relevant phase or workstream* — assumes the skill has a *relevant phase or workstream*. Karpathy-guidelines doesn't; it applies everywhere. Trying to cite it under that convention would either weaken the convention (every skill is "always-on" if karpathy is) or list karpathy in every phase (which defeats the indexing purpose).

## Overlap with methodology

Each karpathy principle has a partial-overlap home in methodology, but the overlap is *architectural enforcement* vs *behavioral exhortation* — same content, different mechanism:

| Karpathy principle | Methodology architectural analog | Coverage |
|---|---|---|
| Think Before Coding | Phase 0 Orient + Plan/Present/Implement gates | Full at session granularity; gaps at sub-edit decisions |
| Simplicity First | SAFEGUARDS blast-radius limits + "1 and done" rule | Full at session granularity; gaps at code-level overengineering |
| Surgical Changes | Mode-Switch Problem + Artifact Integrity (v2.1) | Partial — methodology addresses scope creep across sessions; karpathy addresses scope creep *within an edit* |
| Goal-Driven Execution | Phase 3E Runtime Smoke Test + Verify discipline (now citing `/verify`) | Full at session granularity; partially redundant with `/verify` recommendation |

The **one genuine gap** karpathy addresses is **Surgical Changes** — *"don't 'improve' adjacent code, don't refactor things that aren't broken, match existing style, every changed line should trace directly to the user's request."* This is **sub-edit-granularity scope discipline** that methodology's session-level "1 and done" and SAFEGUARDS blast-radius don't directly enforce. It's the kind of small mid-implementation behavior that doesn't trip a phase gate but produces a worse PR.

## Recommendation

**Do not** add karpathy-guidelines to `RECOMMENDED_SKILLS.md` alongside Pocock skills.

- It's a different category. Citing it next to `/diagnose` or `/triage` would dilute what "recommended skill" means in v2.6 — task workflows the methodology cites at specific phases. Karpathy applies everywhere, all the time.
- It would couple methodology more tightly to Claude Code / Cursor than the agent-independent stance allows. Karpathy-guidelines ships specifically as `CLAUDE.md` and `.cursor/rules/`; the methodology's other recommendations (verify, run, code-review, security-review) are agent-features, not agent-config.

**Two paths forward, both legitimate:**

**Path A — Brief mention as a future category.** If/when the methodology decides to address behavioral overlays as a distinct category (vs task workflows), karpathy-guidelines is a reasonable first example. A new subsection in `RECOMMENDED_SKILLS.md` titled **"Complementary behavioral guidelines (not skills)"** could host this:

> Some methodology adopters augment their `CLAUDE.md` (or equivalent agent-config) with behavioral guidelines that operate at edit granularity — below the level the methodology's session-level phases address. One example is [`karpathy-guidelines`](https://github.com/multica-ai/andrej-karpathy-skills) (MIT licensed), which addresses sub-edit scope discipline ("don't refactor adjacent code", "don't add abstractions for single-use code"). The methodology does not require any such overlay — Phase 0 Orient, the Plan/Present/Implement gates, and SAFEGUARDS blast-radius limits enforce equivalent discipline at session granularity. Adopters who want finer-grain enforcement may install karpathy-guidelines or an equivalent behavioral overlay; the choice is intentionally tool-agnostic, analogous to the pre-commit hook recommendation in `BOOTSTRAP.md` Step 10.

This is parallel to the v2.6 BOOTSTRAP.md treatment of pre-commit hooks: the methodology names one option, acknowledges the gap, but stays tool-agnostic.

**Path B — Leave it out entirely.** The methodology survives without it. Phase 0 Orient and the gates address most of what karpathy targets. The only genuine gap is sub-edit Surgical Changes discipline, and adopters who care can install karpathy-guidelines independently. No methodology change required.

**My lean:** Path B for now, Path A if/when a second behavioral-overlay candidate appears. A category with one member doesn't need a category yet. If a second behavioral overlay enters the conversation (Anthropic ships something equivalent? a defensive-coding skill emerges?), Path A becomes more compelling because then the category genuinely exists.

## Status

No PR proposed. If/when the methodology decides to address behavioral overlays as a category, this evaluation is the starting point. Until then, adopters can install karpathy-guidelines independently — the methodology survives without it.

If you (KJ5HST or rmsharp) want to act on Path A, the change is:
- One new subsection in `starter-kit/RECOMMENDED_SKILLS.md`
- Optional one-line mention in `ITERATIVE_METHODOLOGY.md` §Recommended Skills pointing at the subsection

That's a ~40-line PR. Trivial to land if/when the timing is right; equally trivial to leave indefinitely.
