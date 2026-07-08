# Operational Backlog (fork-only)

> **STATUS: 0 open items — BL-6 fully closed 2026-07-08; BL-1 – BL-6 all complete; backlog RETIRED again.**
> BL-6's last two items closed today: item 2 (seed-format migration discoverability) shipped in
> [PR #51](https://github.com/KJ5HST/methodology/pull/51) (merge `48c253f`, no version event), and item 3
> (hook distribution) was **decided — keep `.githooks/pre-commit` canonical-only** (see the Completed
> table + `CHANGELOG.md`). Verbose task bodies are removed at close-out; git history preserves them
> (`b091fba` … `69dad12`; BL-5 `b2efd76` … the v3.2 merge; the BL-6 item-1/1a/1b/1c detail up to the
> `9a84b8e` fork-sync merge).

Operational/coordination backlog for **rmsharp's** methodology work. Fork-only — it lives in
`docs/planning/` and is **not** part of the canonical framework or any upstream PR (same convention
as [`adopter-pr25-27-remediation-plan.md`](adopter-pr25-27-remediation-plan.md)).

This is a backlog, **not** GitHub issues, by operator decision.

## Open items

*(none — BL-6 fully closed 2026-07-08; see Completed items below. BL-1 – BL-6 are all complete, so this
backlog is retired again. Reopen by adding a new `BL-<N>` here.)*

## Completed items (BL-1 – BL-6)

| Item | Scope | Outcome |
|------|-------|---------|
| **BL-1** | wsfct → v2.9 (supersede #520) | ✅ Complete in `rmsharp/wsfct` (operator). Legacy PR #520 closed. |
| **BL-2** | mts #1 — adopt PR #25/#27, refresh → v2.9 | ✅ Complete in `rmsharp/mts` (operator). |
| **BL-3** | airqino #1 — remediation + full re-vendor → v2.9 | ✅ Complete in `rmsharp/airqinodashboard` (operator). |
| **BL-4** | Housekeeping: methodology repo | ✅ DONE 2026-07-06 — plans archived to `docs/planning/`, 3 stale branches pruned, fork/upstream/tags in sync. |
| **BL-5** | Dashboard: fair scoring for document-only / research repos | ✅ SHIPPED 2026-07-08 in **v3.2** ([PR #50](https://github.com/KJ5HST/methodology/pull/50), merge `9bda167`). `detect_doc_only` + Render/Verification proxy; code-centric risks suppressed; Large-files ext-filter; both polish items (Signal-F adopter-gate + `starter-kit/__pycache__` gitignore) done; `DASHBOARD_VERSION` 2.8.0; first functional scoring tests (29). |
| **BL-6** | v3.1 adopter-migration completeness (pedagogical + seed-format + hook distribution) | ✅ CLOSED 2026-07-08. **Item 1** (pedagogical refresh) + follow-ups **1a/1b/1c** shipped via [PR #47](https://github.com/KJ5HST/methodology/pull/47) / [#48](https://github.com/KJ5HST/methodology/pull/48) / [#49](https://github.com/KJ5HST/methodology/pull/49) (docs/tutorial lag; no version event). **Item 2** (seed-format migration discoverability) shipped via [PR #51](https://github.com/KJ5HST/methodology/pull/51) (merge `48c253f`, no version event) — `bin/status` flags a pre-v3.1-shaped seed `present (stale format)` with a migration note, advisory-only (generic `_manifest.SEED_FORMAT_MARKERS`; `sync` never auto-overwrites). **Item 3** (hook distribution) **DECIDED: keep `.githooks/pre-commit` canonical-only** — adopters run the Phase 3F ledger gate via their root `SESSION_RUNNER.md`, so distributing the hook would add a per-clone `core.hooksPath` enable step + a maintenance surface for a mechanism they already have; the hook exists only because *this* repo has no root runner. Not added to `bin/_manifest.py`. |

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
