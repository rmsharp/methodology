# Operational Backlog (fork-only)

> **STATUS: REOPENED 2026-07-25 — BL-8, BL-11 and BL-12 are open.** BL-8 was deliberately sequenced
> *after* the dashboard signal-integrity campaign closed (Layer 7, then Layer 6), which it now has
> (v3.6 shipped 2026-07-27), so it is unblocked. BL-11 and BL-12 were both raised 2026-08-01 at
> BL-10's close-out and are independent of that campaign. BL-1 – BL-7, BL-9 and BL-10 are complete;
> the retirement note below is preserved as the record of that cycle. **BL-9 closed 2026-08-01 (S25)
> when its last layer, L2, shipped** — all three layers delivered across S23/S24/S25.

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

> **BL-10's fix is complete, verified, and PARKED — do not lose it, and do not re-propose it.**
> It is **not** on `main`. It exists only on branch `docs/bl-10-dangling-learning-citations`
> (local + `origin`) and on the annotated tag **`archive/bl-10-citations`** (pushed to `origin`
> only — deliberately namespaced under `archive/` so it is never mistaken for a release tag and
> never mirrored as one). Commits: **`268f1e5`** (`bin/check-citations` + Test 23) and **`1eac7a4`**
> (the five citation rewrites), based on `d6dd6c9` = `upstream/main` at 2026-08-01. Verified at that
> SHA: `bin/tests.sh` 91/91, `bin/check-citations` OK, `bin/check-links` OK (85 links / 21 files).
> Recover with `git checkout archive/bl-10-citations` even if the branch is deleted on both sides.
> **Status:** opened as `KJ5HST/methodology` PR #64 *without operator authorization* and closed at
> his instruction; **reopening is under discussion between the operator and the maintainer.** No
> agent may reopen it, open a replacement, or comment upstream without an explicit ask.

## Open items

**BL-8** was sequenced AFTER the dashboard signal-integrity campaign closed — i.e. after **Layer 7**
(the installer/doc-only fix, ratified S14) and then **Layer 6** (close-out + release decision R1).
That campaign shipped as **v3.6** on 2026-07-27, so it is not blocked any longer. It is not a change
to the methodology. It was raised and measured in **S14** (as was BL-9, now complete); see the action
ledger for those entries. **BL-11** and **BL-12** are unrelated to the campaign; both were raised
2026-08-01 at BL-10's close-out.

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

**BL-11 — Unreachable non-`Learning` referents across the distributed corpus.**
*Raised 2026-08-01 at BL-10's close-out; deliberately not bundled into it (FM #17/#18).*
BL-10 closed the `Learning #N` case and mechanized it (`bin/check-citations`, `bin/tests.sh`
Test 23). The same class survives in referents that checker cannot model, because they are prose
provenance rather than a relation between two enumerable sets:
- `starter-kit/SESSION_RUNNER.md` Learnings **Source** column, four rows — #8 (`escape #8`, `S7`),
  #9 (the deictic "this session"), #11 (`HANDOFFS.md` session `S1`, `BL-7`), #12 (`S9–S16`,
  `Layer 1`/`Layer 7`). All fork-only vocabulary with no referent in `upstream/main`.
- `starter-kit/RECOMMENDED_SKILLS.md` — `HANDOFFS.md` session `S1`.
- `starter-kit/HANDOFFS.md` — `(root HANDOFFS.md, session S1)`, in a **SEED** that becomes the
  adopter's own file, where the self-reference is actively misleading.
- `HOW_TO_USE.md:861` — *"anti-pattern #31 in the original methodology"*: a numbered referent in a
  project no reader has. **The closest true analogue to BL-10; arguably fix this one first.**
- `starter-kit/methodology_dashboard.py` — `BL-5` at ~9 sites and bare `Layer 4/7/8` at ~7 more: a
  fork-only backlog ID shipped inside adopter-installed code.
*Severity is lower than BL-10 by a stated test:* these are provenance/attribution tokens, so the
rule they annotate stands without them — the reader loses corroboration, not meaning. BL-10's five
were the argument itself.
*Blocker to decide FIRST:* `starter-kit/SESSION_RUNNER.md` says the Learnings table is append-only,
*"do not edit existing rows"*, and all four rows are merged upstream. Rewriting them needs an
explicit maintainer exception — **that decision, not the edit, is the deliverable.**
*Not mechanizable the same way:* prose provenance is not a two-set relation, so Learning #12's own
rule routes this back to a review-time grep (Learnings #7/#10), not to another assertion.

**BL-12 — Two verified corpus defects found during BL-10's sweep, out of its declared scope.**
*Raised 2026-08-01; both measured, neither fixed (FM #17).*
- `workstreams/RESEARCH_DOCUMENTATION_WORKSTREAM.md:55` says *"The 19 anti-patterns"*; the list has
  **20** (#20 was appended in v2.5 and the size claim was never recounted). Self-contradicted at
  `:306` in the same file — *"Anti-patterns #9, #10, #11 … The remaining 17"* = 20. A one-word fix
  in a distributed file, but a **count claim**, not a citation, so it is a different defect class
  from BL-10 and was deliberately left out of that PR.
- The Learnings table has **no shape coverage**: upstream's own S5 receipt mutation-proved that a
  duplicate row number, a malformed 3-column row, and a deleted row all pass the suite.
  `bin/check-citations`' contiguity guard closes only the **hole** case; duplicates and malformed
  rows still pass. Same Learning #12 shape as BL-10's fix — drive it RED first.

## Completed items (BL-1 – BL-7, BL-9, BL-10)

| Item | Scope | Outcome |
|------|-------|---------|
| **BL-1** | wsfct → v2.9 (supersede #520) | ✅ Complete in `rmsharp/wsfct` (operator). Legacy PR #520 closed. |
| **BL-2** | mts #1 — adopt PR #25/#27, refresh → v2.9 | ✅ Complete in `rmsharp/mts` (operator). |
| **BL-3** | airqino #1 — remediation + full re-vendor → v2.9 | ✅ Complete in `rmsharp/airqinodashboard` (operator). |
| **BL-4** | Housekeeping: methodology repo | ✅ DONE 2026-07-06 — plans archived to `docs/planning/`, 3 stale branches pruned, fork/upstream/tags in sync. |
| **BL-5** | Dashboard: fair scoring for document-only / research repos | ✅ SHIPPED 2026-07-08 in **v3.2** ([PR #50](https://github.com/KJ5HST/methodology/pull/50), merge `9bda167`). `detect_doc_only` + Render/Verification proxy; code-centric risks suppressed; Large-files ext-filter; both polish items (Signal-F adopter-gate + `starter-kit/__pycache__` gitignore) done; `DASHBOARD_VERSION` 2.8.0; first functional scoring tests (29). |
| **BL-6** | v3.1 adopter-migration completeness (pedagogical + seed-format + hook distribution) | ✅ CLOSED 2026-07-08. **Item 1** (pedagogical refresh) + follow-ups **1a/1b/1c** shipped via [PR #47](https://github.com/KJ5HST/methodology/pull/47) / [#48](https://github.com/KJ5HST/methodology/pull/48) / [#49](https://github.com/KJ5HST/methodology/pull/49) (docs/tutorial lag; no version event). **Item 2** (seed-format migration discoverability) shipped via [PR #51](https://github.com/KJ5HST/methodology/pull/51) (merge `48c253f`, no version event) — `bin/status` flags a pre-v3.1-shaped seed `present (stale format)` with a migration note, advisory-only (generic `_manifest.SEED_FORMAT_MARKERS`; `sync` never auto-overwrites). **Item 3** (hook distribution) **DECIDED: keep `.githooks/pre-commit` canonical-only** — adopters run the Phase 3F ledger gate via their root `SESSION_RUNNER.md`, so distributing the hook would add a per-clone `core.hooksPath` enable step + a maintenance surface for a mechanism they already have; the hook exists only because *this* repo has no root runner. Not added to `bin/_manifest.py`. |
| **BL-7** | Capability-tiered review — model-tiering as an elective vertical-slice addition | ✅ SHIPPED 2026-07-08 via [PR #57](https://github.com/KJ5HST/methodology/pull/57) (merge `d563600`). A 3-candidate design panel (extend-in-place / full-parallel-treatment / anchor-to-vertical-slice) scored on 4 lenses, synthesized, then every open decision (placement, naming, scope, all three extras) put to the operator before implementation. Landed as an elective paragraph in `SESSION_RUNNER.md` §Vertical Slice Sessions + new Learning #11, a routing pointer in `ITERATIVE_METHODOLOGY.md`, an illustrative addendum in `RECOMMENDED_SKILLS.md`, and a corollary in `docs/tutorials/T5_cautionary.md`. A 4-lens adversarial review unanimously caught and fixed one defect (brand names leaking into the brand-neutral core file). No new phase, gate, principle, workstream, or FM; FM count stays 27. Version-event decision still open (deferred past merge — no version-bump commit landed with PR #57). |
| **BL-9** | Three size disciplines this repo publishes and had drifted from | ✅ CLOSED 2026-08-01 across three sessions, all fork-local, zero distributed files touched. **L1** (S23, `7a71df0`) — `HANDOFFS.md` 216 KB → 51 KB, 19 older receipts to `docs/archive/HANDOFFS-archive.md`; closed the missing-archival-rule gap *for this repo*. **L3** (S24, `7603f10`) — `CLAUDE.md` 52,909 → 8,519 bytes (−83.9%), the 25 version entries verbatim to `docs/RELEASE_HISTORY.md`, with the `## Versioning` heading kept in place because 15 frozen links cite that anchor. **L2** (S25) — the action ledger split at the **v3.6 release frontier**: 186,704 → 53,512 bytes (−71.3%), 2,090 → 658 lines, 50 entries verbatim to `docs/archive/CHANGELOG-through-v3.6.md`. L2's deliverable was the **decision**, and the evidence settled it: the rule's ratified plan (`changelog-authoritative-ledger-gate-plan.md:128`) and the distributed seed (`starter-kit/CHANGELOG.md:92`) both make `## YYYY-MM` a *grouping-axis* rule, never a size rule — so sections went by month and the *file* boundary by release, two different axes. The one concrete defect fixed: the file had crossed the 2,000-line agent `Read` cap at L1's own commit and was silently dropping its 10 oldest entries. Everything else was anticipatory and is recorded as such — this ledger is not auto-loaded and no size-caused harm was on record. |
| **BL-10** | Five dangling `Learning #N` citations in adopter-distributed files | ✅ SHIPPED 2026-08-01 via [PR #64](https://github.com/KJ5HST/methodology/pull/64). All five traced to the 2026-05-02 Pocock audit, written in session S438 of a *different* methodology instance whose Learnings table ran into the 30s. **Three were worse than dangling** — they asserted framework rules that do not exist (there is no handoff length discipline; the only `150`-as-handoff-length string in the distributed corpus was the line claiming it), so stripping just the numbers would have left unattributed false claims. Each site re-grounded on a reachable referent; dispositions unchanged; no Learnings row added or edited. Mechanized per Learning #12: canonical-only `bin/check-citations` + Test 23, driven RED first (6 findings), with every guard driven RED too — mutation-testing the fixture caught a real defect in the checker itself (a missing registry file exited 1, indistinguishable from a corpus finding). Suite 84 → 91. Follow-ons raised as BL-11 and BL-12. |

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
