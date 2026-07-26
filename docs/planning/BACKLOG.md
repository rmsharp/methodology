# Operational Backlog (fork-only)

> **STATUS: REOPENED 2026-07-25 — BL-8 and BL-9 are open, both deliberately sequenced *after*
> the dashboard signal-integrity campaign closes (Layer 7, then Layer 6).** BL-1 – BL-7 remain
> complete; the retirement note below is preserved as the record of that cycle.

> **(prior status) RETIRED (again) — BL-1 – BL-7 all complete, 2026-07-08.**
> BL-7 (capability-tiered review, an elective vertical-slice addition) shipped via
> [PR #57](https://github.com/KJ5HST/methodology/pull/57) (merge `d563600`) — see the Completed table
> + `CHANGELOG.md`. Verbose task bodies are removed at close-out; git history preserves them
> (`b091fba` … `69dad12`; BL-5 `b2efd76` … the v3.2 merge; the BL-6 item-1/1a/1b/1c detail up to the
> `9a84b8e` fork-sync merge; BL-7 design panel + implementation up to the `d563600` merge).

Operational/coordination backlog for **rmsharp's** methodology work. Fork-only — it lives in
`docs/planning/` and is **not** part of the canonical framework or any upstream PR (same convention
as [`adopter-pr25-27-remediation-plan.md`](adopter-pr25-27-remediation-plan.md)).

This is a backlog, **not** GitHub issues, by operator decision.

## Open items

**Both are sequenced AFTER the dashboard signal-integrity campaign closes** — i.e. after **Layer 7**
(the installer/doc-only fix, ratified S14) and then **Layer 6** (close-out + release decision R1).
Neither blocks that campaign, and neither is a change to the methodology. Raised and measured in
**S14**; see `CHANGELOG.md` for that session's entries.

**BL-8 — Subagent capability-tiering: adopt as an operational default, or decline.**
*Not a methodology change, and no document needs editing.* `SESSION_RUNNER.md` §Vertical Slice
Sessions already carries the decision rule (v3.5, BL-7) — explicitly **elective**, scoped to
pre-declared vertical slices — and `RECOMMENDED_SKILLS.md` states the default outright:
*"Elective; single-tier-throughout remains the default."* The open question is narrower and purely
operational: when a session authors a **workflow** whose subagent roles rest on an objective,
checkable gate (extraction re-verified by executing the module; corpus sweeps re-verified downstream),
should those roles be authored onto a lighter tier while judgment roles and review stay on the
strongest? Note the current campaign is **horizontal** (one layer per session), not a slice, so the
v3.5 mechanism does not formally govern it — this would be applying its *principle* to a context the
document does not cover.
*Measured in S14, against its own 48 subagents:* all-Opus **$132**; all-Sonnet **$79** standard /
**$53** intro; **hybrid ~13–19% saving** — much less than the headline, because the judgment-heavy
verifier role is **61% of input tokens**. Cache reads are **91.7%** of all input. Sonnet intro
pricing ends **2026-08-31**.
*The larger lever measured alongside it, and the better first move:* **8 of 36 verifier agents
re-verified a site another slice had already surfaced** (dedupe findings before spawning verifiers),
and the review budget should be reserved *before* the discovery sweep — S14's sweep consumed the
budget and its review then died on a usage limit, which is why Layer 5 shipped unreviewed and later
needed three prose fixes. Both are free of any quality tradeoff.
**"Decline and keep single-tier" is a correct outcome** and matches the documented default; the only
cost is the saving above.

**BL-9 — This repo has drifted from two size disciplines it publishes, and a third has no rule at all.**
*Also not a new proposal — two of the three are rules this repo already states and does not follow.*
- `CHANGELOG.md` is **103 KB**, and its own line 31 says *"Promote to `## YYYY-MM` sections as it
  grows."* Never done.
- `CLAUDE.md` is **43 KB** and **85%** of it is `§Versioning`, against `starter-kit/BOOTSTRAP.md:195`,
  which sets a *"practical size budget (…roughly 200 lines…)"* and warns that an oversized memory file
  *"measurably degrades how reliably the agent follows it."* That file is auto-loaded every session.
- `HANDOFFS.md` is **110 KB** with **no archival rule anywhere in the corpus** — the genuine gap.
  Per-session receipts grew **10 → 13 → 13 → 15 KB** across S10–S13.
*Scope note:* this is a **canonical-repo** problem. Adopters pay almost none of it — their
per-session floor is `SESSION_RUNNER.md` + `SAFEGUARDS.md`, and the signal-integrity campaign added
~0 to it.
*Constraints any fix must respect:* Phase 0 reconcile is **frontier-based** (`git log -1 --format=%H
-- <file>`), so sharding either ledger is safe by construction; `bin/check-handoff` validates only
the **newest** receipt, so archiving older ones does not break it; and the `§Versioning` ↔
`CHANGELOG.md` cite-don't-restate boundary (v3.1) must survive whatever `CLAUDE.md` extraction is
chosen.

## Completed items (BL-1 – BL-7)

| Item | Scope | Outcome |
|------|-------|---------|
| **BL-1** | wsfct → v2.9 (supersede #520) | ✅ Complete in `rmsharp/wsfct` (operator). Legacy PR #520 closed. |
| **BL-2** | mts #1 — adopt PR #25/#27, refresh → v2.9 | ✅ Complete in `rmsharp/mts` (operator). |
| **BL-3** | airqino #1 — remediation + full re-vendor → v2.9 | ✅ Complete in `rmsharp/airqinodashboard` (operator). |
| **BL-4** | Housekeeping: methodology repo | ✅ DONE 2026-07-06 — plans archived to `docs/planning/`, 3 stale branches pruned, fork/upstream/tags in sync. |
| **BL-5** | Dashboard: fair scoring for document-only / research repos | ✅ SHIPPED 2026-07-08 in **v3.2** ([PR #50](https://github.com/KJ5HST/methodology/pull/50), merge `9bda167`). `detect_doc_only` + Render/Verification proxy; code-centric risks suppressed; Large-files ext-filter; both polish items (Signal-F adopter-gate + `starter-kit/__pycache__` gitignore) done; `DASHBOARD_VERSION` 2.8.0; first functional scoring tests (29). |
| **BL-6** | v3.1 adopter-migration completeness (pedagogical + seed-format + hook distribution) | ✅ CLOSED 2026-07-08. **Item 1** (pedagogical refresh) + follow-ups **1a/1b/1c** shipped via [PR #47](https://github.com/KJ5HST/methodology/pull/47) / [#48](https://github.com/KJ5HST/methodology/pull/48) / [#49](https://github.com/KJ5HST/methodology/pull/49) (docs/tutorial lag; no version event). **Item 2** (seed-format migration discoverability) shipped via [PR #51](https://github.com/KJ5HST/methodology/pull/51) (merge `48c253f`, no version event) — `bin/status` flags a pre-v3.1-shaped seed `present (stale format)` with a migration note, advisory-only (generic `_manifest.SEED_FORMAT_MARKERS`; `sync` never auto-overwrites). **Item 3** (hook distribution) **DECIDED: keep `.githooks/pre-commit` canonical-only** — adopters run the Phase 3F ledger gate via their root `SESSION_RUNNER.md`, so distributing the hook would add a per-clone `core.hooksPath` enable step + a maintenance surface for a mechanism they already have; the hook exists only because *this* repo has no root runner. Not added to `bin/_manifest.py`. |
| **BL-7** | Capability-tiered review — model-tiering as an elective vertical-slice addition | ✅ SHIPPED 2026-07-08 via [PR #57](https://github.com/KJ5HST/methodology/pull/57) (merge `d563600`). A 3-candidate design panel (extend-in-place / full-parallel-treatment / anchor-to-vertical-slice) scored on 4 lenses, synthesized, then every open decision (placement, naming, scope, all three extras) put to the operator before implementation. Landed as an elective paragraph in `SESSION_RUNNER.md` §Vertical Slice Sessions + new Learning #11, a routing pointer in `ITERATIVE_METHODOLOGY.md`, an illustrative addendum in `RECOMMENDED_SKILLS.md`, and a corollary in `docs/tutorials/T5_cautionary.md`. A 4-lens adversarial review unanimously caught and fixed one defect (brand names leaking into the brand-neutral core file). No new phase, gate, principle, workstream, or FM; FM count stays 27. Version-event decision still open (deferred past merge — no version-bump commit landed with PR #57). |

**Not in this backlog:** upstream **PR #44** (REUSE compliance + license/REUSE README badges) is being
handled directly with the maintainer (Terrell) and was never a backlog item.

## Historical context (for the record)

The backlog existed to bring three v2.7-era adopter PRs (all authored 2026-06-12) current to canonical
**v2.9** before merging, and to run one methodology-repo housekeeping session. Two conventions governed it:

- **Mechanism = the documented update workflow, not PR-resurrection.** Bring an adopter current with
  `bin/status` → `bin/sync` from a canonical `methodology/` checkout (`--source=local` preferred), or the
  *"Update methodology using https://github.com/KJ5HST/methodology"* agent prompt — then supersede the
  stale PR rather than conflict-resolving it. This is exactly what v2.8's full-corpus `bin/sync`
  (`bin/_manifest.py`, issue #32) was built for.
- **Merge only when the target repo is between sessions**, since each adopter PR rewrites live operating
  files (`SESSION_RUNNER.md`, `CLAUDE.md`, `SAFEGUARDS.md`, `SESSION_NOTES.md`). One repo = one session.

Two adopters from the original PR #25/#27 rollout were always out of this backlog's scope:
**nprcgenekeepr** (the clean reference end-state) and **model_project_constructor** (tracked separately).
