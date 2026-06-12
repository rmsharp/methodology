# Adopter Remediation Plan — Methodology PR #25 + PR #27

*Drafted 2026-06-06. Status: **EXECUTED 2026-06-12** — PR #25/#27 merged upstream that morning (verbatim, no rework); all five projects remediated the same day. See §Execution record at the end of this document.*
*Scope: 5 adopter projects — `mts-system`, `wsfct`, `model_project_constructor`, `nprcgenekeepr`, `airqino`.*

## Decisions locked (set by the user, 2026-06-06)

1. **Drift handling → migrate.** Move existing project learnings *out* of the synced `SESSION_RUNNER.md` table: large corpora → a committed, plain-linked `PROJECT_LEARNINGS.md`; small sets → inline in a new `CLAUDE.md` Learnings subsection. Restore each synced table to its canonical seed rows.
2. **Wording timing → apply now from the PR branches (O4).** *Supersedes the original "wait for merge."* Source the new wording directly from the PR-25 branch (`fix/3c-learnings-destination`) and PR-27 branch (`fix/claude-md-learnings-overflow`) — captured verbatim as Assets C/D below — without waiting for KJ5HST to merge and without merging your own fork main. Accept minor rework only if upstream review changes the wording. **This collapses the old Bucket A / Bucket B split: everything is "now."**
3. **O1 → broad slim** of mts-system CLAUDE.md. **O2 → full re-vendor** of airqino off v2.1. **O3 → align nprcgenekeepr's "40k" wording now.** (Details in per-project sections + Open items.)
4. **Execution is still greenlit per-project** — this document is the agreed plan of record; each project is its own session/deliverable.

## What PR #25 / PR #27 are

- **PR #25** (`ed9007c`, OPEN) — routes project learnings to `CLAUDE.md → Project-Specific Methodology Adaptations → Project-specific Learnings`; reserves the **synced** `SESSION_RUNNER.md` "Learnings (added by sessions)" table for canonical framework learnings. Touches synced `SESSION_RUNNER.md` + vendored `HOW_TO_USE.md`.
- **PR #27** (`1999f4a` + `a33b269`, OPEN) — CLAUDE.md size-budget rule: when CLAUDE.md nears ~200 lines, extract Learnings to a committed `PROJECT_LEARNINGS.md` reached by a **plain Markdown link, never an `@`-import** (an `@`-import is expanded into context every session and defeats the extraction). Touches vendored `BOOTSTRAP.md` + `CLAUDE_TEMPLATE.md` only.

**Sync reality:** the sync allowlist is exactly 3 files (`SESSION_RUNNER.md`, `SAFEGUARDS.md`, `methodology_dashboard.py`). `HOW_TO_USE.md` / `BOOTSTRAP.md` / `CLAUDE_TEMPLATE.md` are vendored copies (manual patch). Only **wsfct** has `bin/sync` at all; the other four were vendored by hand, so for them *every* file — including `SESSION_RUNNER.md` — is a manual edit.

---

## The finding (why this is bigger than doc wording)

All 5 projects carry the OLD pre-PR-25 wording in three places. More importantly, **4 of 5 already exhibit the exact drift PR #25 was written to prevent**: project-specific session learnings written into the *synced* `SESSION_RUNNER.md` table.

| Project | CLAUDE.md lines | Drifted rows in synced table | Receptacle? | PR-27 done? | bin/sync? | Extract target |
|---|---|---|---|---|---|---|
| **mts-system** | **908** (~4.5× budget) | **~17** (Sessions 10–36) | no | n/a yet | no | `PROJECT_LEARNINGS.md` (17 rows + general slim) |
| **wsfct** | **673** (~3.4×) | **~113** (Sessions 70–123) | no | no | **yes** (drift-guard will block) | `PROJECT_LEARNINGS.md` |
| **model_project_constructor** | 61 | **~46** (#1–#46, Sessions 92–110) | no | n/a yet | no | `PROJECT_LEARNINGS.md` |
| **nprcgenekeepr** | 175 | **0 (clean)** | **yes** | **yes** (plain link) | no | already extracted |
| **airqino** | 12 | **2** (REV6 board, adapter OOS) | no | n/a yet | no (v2.1-era) | inline in `CLAUDE.md` |

**nprcgenekeepr is the reference end-state** — it already has the receptacle, an extracted `PROJECT_LEARNINGS.md` via a plain link, and a clean synced table. Mirror its shape everywhere else.

---

## Execution model

**O4 collapses the buckets — all work runs now.** Each project gets one pass covering both the owned-file work and the new wording (sourced from the PR branches, Assets C/D).

Per-project pass:
- Add the `## Project-Specific Methodology Adaptations` receptacle to `CLAUDE.md` where missing.
- Migrate drifted rows out of the synced `SESSION_RUNNER.md` table → `PROJECT_LEARNINGS.md` (large) or inline `CLAUDE.md` (small). Restore the synced table to its canonical seed rows.
- Apply the new wording (C1/C2/C3 + Asset D where the file is vendored) **verbatim from the captured PR-branch text**.
- Project-specific extras: mts-system broad slim (O1); airqino full re-vendor (O2); nprcgenekeepr "40k"→budget wording (O3).

### Sourcing the wording (O4 = from PR branches)
- Use the **exact** C1/C2/C3/Asset-D text below — it is copied verbatim from PR #25/#27. Do **not** improvise wording; byte-alignment with the eventual merge is what keeps a future sync a no-op.
- **Recommended source-of-truth for execution:** create a local integration branch in the methodology repo = `origin/main` + PR #25 + PR #27 merged, and pull synced/vendored/re-vendor content from *that* tree. This guarantees every adopter gets identical, internally-consistent text (and is the natural source for airqino's full re-vendor). Targeted per-string edits from the captured text are equivalent for the four non-re-vendor projects.

### Hard rules
- **The synced `SESSION_RUNNER.md` may be edited now, but ONLY to the exact PR-25 branch text** (C1/C2). Improvised wording recreates the drift PR #25 prevents. For **wsfct** (sync-managed), also update its vendored canonical baseline copy (`docs/methodology/starter-kit/SESSION_RUNNER.md`) to the same PR-25 text so `bin/status`/`bin/sync` see root and baseline as aligned, not drifted.
- **Restoring the synced table to seed rows** *removes* drift (returns the file toward canonical) — always safe.
- **Preserve every migrated row verbatim.** The drifted rows are real institutional memory. Move, don't summarize (an information-preserving trim is a separate, later per-project decision).
- **wsfct first** among the drifted set — clearing its drift early keeps its sync coherent.

---

## Reusable assets (apply consistently across projects)

### Asset A — `CLAUDE.md` receptacle (canonical structure)

Add before any trailing index/footer, mirroring `starter-kit/CLAUDE_TEMPLATE.md` and nprcgenekeepr's realized copy. Keep the standard subsections even when "(none)":

```markdown
---

## Project-Specific Methodology Adaptations

*Additions and overrides to the base methodology at `SESSION_RUNNER.md` and `SAFEGUARDS.md` (synced from canonical, not project-owned). The base files govern unless explicitly overridden here. **Do not edit the synced files** — put customizations here so `bin/sync` stays friction-free.*

### Additional Phase 0 steps

(none)

### Additional task-to-workstream mappings

(none)

### Project-specific Learnings

<!-- small N: inline table here. large N: replace with the Asset-B pointer. -->
(none)

### Project-specific Failure Modes

(none — the base failure modes in `SESSION_RUNNER.md` apply.)
```

### Asset B — `PROJECT_LEARNINGS.md` + plain-link pointer (large-corpus projects)

Pointer **in CLAUDE.md** (plain link — NOT `@PROJECT_LEARNINGS.md`):

```markdown
### Project-specific Learnings

Project institutional memory (<N> learnings, Sessions <range>) lives in [`PROJECT_LEARNINGS.md`](PROJECT_LEARNINGS.md) — extracted from the synced `SESSION_RUNNER.md` table to keep `CLAUDE.md` within its size budget (Claude Code targets ~200 lines / ~25 KB). **Read it when a task resembles earlier work; append new learnings there, not here.** Base methodology-level learnings remain in `SESSION_RUNNER.md`.
```

`PROJECT_LEARNINGS.md` header:

```markdown
# <project> — Project-Specific Learnings

> Migrated verbatim from `SESSION_RUNNER.md`'s "Learnings (added by sessions)" table on <date> so the synced runner stays byte-identical to canonical, and to keep `CLAUDE.md` within its size budget. No content changed in the move. **Append new project learnings here, not in `CLAUDE.md`.** Base, methodology-level learnings remain in `SESSION_RUNNER.md`.

<the migrated rows, verbatim>
```

> **Note:** use the "~200 lines / ~25 KB" budget language from PR #27, not the empirical "40k-char limit" phrasing that nprcgenekeepr currently uses (see open item O3).

### Asset C — canonical wording replacements (Bucket B — re-verify against MERGED canonical before applying)

*These are the PR draft texts. Treat as the expected final wording; diff against merged `KJ5HST/main` before pasting.*

**C1 — `SESSION_RUNNER.md` §"3C: Document Learnings" body** replaces `Update the workstream document and/or the Learnings table below:` with:

> Capture what this session learned so the next session inherits it. Always update the relevant workstream document for any workstream-level pattern or anti-pattern. Then record session learnings in the right place for your audience:
>
> - **Adopter project** (you copied this `SESSION_RUNNER.md` from the methodology repo): put project learnings in your `CLAUDE.md` → **Project-Specific Methodology Adaptations** → **Project-specific Learnings** subsection. Do NOT edit the "Learnings (added by sessions)" table further down in this file — `SESSION_RUNNER.md` is synced from canonical and must stay byte-identical, or local edits will block future syncs (see BOOTSTRAP, "Customizations Go in CLAUDE.md, Not in Synced Files"). Agents read `CLAUDE.md` at session start, so a learning recorded there is applied on top of the base protocol.
> - **Canonical methodology repo** (you are dogfooding the framework on itself): record framework-level learnings by appending a new row to the "Learnings (added by sessions)" table further down in this file. ...
>
> Capture, wherever it lands: *(then the existing six bullets, unchanged)*

**C2 — `SESSION_RUNNER.md` Learnings-table caption** replaces `*This table starts empty. Each session adds learnings here...*` with:

> *These rows are the methodology's own framework learnings, recorded as the canonical repo dogfoods itself — canonical sessions append new rows here (append only; do not edit existing rows). Adopter projects do NOT edit this synced table — record project learnings in `CLAUDE.md` → Project-Specific Methodology Adaptations → Project-specific Learnings instead (see 3C).*

**C3 — `HOW_TO_USE.md` Phase 3 "3C: Document learnings" bullet** replaces `Update workstream prompt and SESSION_RUNNER learnings table` with:

> **3C: Document learnings** — Update the workstream document; record project learnings in CLAUDE.md → Adaptations → Project-specific Learnings (adopters), or append to the SESSION_RUNNER learnings table (canonical repo dogfooding)

### Asset D — PR-27 vendored-file text (Bucket B; only where the file is vendored)

- **`BOOTSTRAP.md` Step 5** — add the "Keep CLAUDE.md lean — extract Learnings before they crowd the budget" paragraph (size budget + extract pattern + plain-link-not-`@`-import warning + blockquote example).
- **`BOOTSTRAP.md` "What to Customize Over Time"** — complete the Learnings row: `...the table grows organically; when it nears CLAUDE.md's size budget, extract it to a referenced PROJECT_LEARNINGS.md and leave a pointer (see Step 5)`.
- **`CLAUDE_TEMPLATE.md`** — add the HTML comment in the Learnings subsection (`This table is loaded every session and grows with no cap... See BOOTSTRAP.md Step 5.`).

---

## Per-project execution

*Line anchors are from the 2026-06-06 survey — re-grep before editing; files may have moved.*
*Post-O4 the "AT MERGE" label is retained only to mark which steps are the **wording** edits; they are now done in the same now-pass, sourced verbatim from the PR-25/27 branch text.*

### 1. mts-system  *(worst case: 908-line CLAUDE.md + drift)*
**NOW**
1. Add Asset-A receptacle to `CLAUDE.md`.
2. Migrate the ~17 rows (Sessions 10–36) out of root `SESSION_RUNNER.md` "## Learnings (added by sessions)" → new `PROJECT_LEARNINGS.md` (Asset B); pointer in the receptacle. Restore synced table to 6 canonical seed rows.
3. **Broad slim** of `CLAUDE.md` (decision **O1 = broad**): extract the 17 learnings AND aggressively trim the non-learnings sections (Project Overview, Process Contract, Architecture, AI Context) toward the ~200-line budget — relocate stable reference content to sibling docs (`docs/`) and leave one-line pointers. Information-preserving, not lossy.

**AT MERGE**
4. `SESSION_RUNNER.md` 3C (~L159) + caption (~L266) ← C1/C2 from merged canonical (manual copy, no bin/sync).
5. `docs/methodology/HOW_TO_USE.md` (~L740) ← C3.
6. `docs/methodology/BOOTSTRAP.md` (~L177, "grows organically" line that currently *causes* the drift) ← Asset D.

### 2. wsfct  *(only sync-managed; drift-guard blocks; ~113 rows)*
**NOW**
1. **Reconcile sync drift first:** reword local FM #5 (~L304) and FM #38 (~L350) in root `SESSION_RUNNER.md` so they no longer tell sessions to append to the synced Learnings table.
2. Add Asset-A receptacle to `CLAUDE.md`.
3. Migrate the ~113 rows (Sessions 70–123) → `PROJECT_LEARNINGS.md` (Asset B); pointer in receptacle. Restore synced table to seed rows. *(This single move satisfies both the PR-25 migration and the PR-27 extraction.)*

**AT MERGE**
4. Once PR #25 merges and steps 1–3 are done, run `docs/methodology/bin/sync` to pull canonical `SESSION_RUNNER.md` (3C + caption). If the guard still trips, reconcile further — **do not `--force` over un-migrated rows**.
5. `docs/methodology/HOW_TO_USE.md` (~L763) ← C3.
6. vendored `docs/methodology/starter-kit/BOOTSTRAP.md` (~L325–331) + `CLAUDE_TEMPLATE.md` (~L73) ← Asset D.

### 3. model_project_constructor  *(61-line CLAUDE.md; ~46 rows; no bin/sync)*
**NOW**
1. Migrate the ~46 rows (#1–#46, Sessions 92–110) → `PROJECT_LEARNINGS.md` (Asset B). Corpus already exceeds budget → straight to the extracted file, skip inline. Restore synced table to seed rows.
2. Add Asset-A receptacle to `CLAUDE.md` with the Asset-B plain-link pointer (mirror nprcgenekeepr's 3-line shape).

**AT MERGE**
3. `SESSION_RUNNER.md` 3C (~L160) + caption (~L267–269) ← C1/C2 (manual copy).
4. `docs/methodology/HOW_TO_USE.md` (~L763) ← C3.
5. *No BOOTSTRAP/CLAUDE_TEMPLATE vendored → Asset D N/A* (vendor later only if desired).

### 4. nprcgenekeepr  *(the model; only wording remains)*
**NOW**
1. **Align "40k" wording (decision O3 = now).** Rewrite the "Claude Code's 40k `CLAUDE.md` limit" justification in `CLAUDE.md` (~L171) and the `PROJECT_LEARNINGS.md` header to PR-27's documented "~200 lines / ~25 KB" budget language. Mechanism already matches PR #27; wording-only, no behavior change.

**AT MERGE**
2. `SESSION_RUNNER.md` 3C (~L167) + caption (~L296) ← C1/C2 (manual copy).
3. `docs/methodology/HOW_TO_USE.md` (~L763) ← C3.
4. *No drift, receptacle present, PR-27 done, no BOOTSTRAP/CLAUDE_TEMPLATE → nothing else.*

### 5. airqino  *(12-line CLAUDE.md; v2.1-era; 2 rows — decision O2 = full re-vendor)*
**NOW**
1. Add Asset-A receptacle to `CLAUDE.md`.
2. Migrate the 2 airqino rows (REV6 board; adapter OOS) → **inline** in the receptacle's Learnings table (too small for a separate file). **Do this before any re-vendor** so the rows aren't lost when `SESSION_RUNNER.md` is overwritten. Restore synced table to seed rows.

**AT MERGE — full re-vendor (decision O2 = full)**
3. Replace airqino's entire vendored `docs/methodology/` tree + root synced files with the current framework from `origin/main` (rmsharp fork) **after** it carries merged PR #25/#27. One operation lifts airqino v2.1 → current: brings the new 3C/caption/HOW_TO_USE wording *and* everything added since v2.1 (campaigns, `RECOMMENDED_SKILLS`, `CONTEXT_TEMPLATE`, Research Documentation workstream, `bin/sync` tooling, render-dep discipline, starter-kit/BOOTSTRAP/CLAUDE_TEMPLATE). Targeted C1/C2/C3/Asset-D patches become unnecessary — the re-vendor supersedes them.
   - **Caveat:** a re-vendor overwrites airqino's partial vendored copy wholesale — confirm no intentional local edits exist in its `docs/methodology/` first. Afterward, re-validate root `CLAUDE.md` / synced files against the newer `CLAUDE_TEMPLATE.md` shape, and consider wiring up `bin/sync` so future updates are friction-free.

---

## Sequencing

1. **wsfct reconcile + migrate** (clears the sync block early).
2. **model_project_constructor migrate** (~46 rows; straightforward, no sync).
3. **mts-system migrate + slim** (biggest payoff: 908-line CLAUDE.md degrades adherence every session today).
4. **airqino receptacle + 2-row inline migrate** (quick).
5. **nprcgenekeepr** optional cosmetic now; otherwise wording-only at merge.
6. **At merge:** sweep Bucket B across all five from merged canonical.

Each project = its own session/deliverable per the "1 and done" rule; commit per project.

## Verification (after each project's NOW work)
- `git diff` on `SESSION_RUNNER.md` shows **only** the Learnings table reverting to canonical seed rows (no other drift introduced).
- `CLAUDE.md` has the `## Project-Specific Methodology Adaptations → ### Project-specific Learnings` subsection; pointer is a plain link (`grep -n '@PROJECT_LEARNINGS' CLAUDE.md` returns nothing).
- Migrated row count in `PROJECT_LEARNINGS.md` (or inline) equals the count removed from the synced table — no rows dropped.
- `wc -l CLAUDE.md` moved toward budget where extraction applied.
- *(wsfct)* `bin/status` no longer reports `SESSION_RUNNER.md` as drifted once reconciled.

## Open items
- **O1 — mts-system slim scope → DECIDED: broad.** Extract the 17 learnings AND aggressively trim the non-learnings sections toward the ~200-line budget (see mts-system NOW step 3).
- **O2 — airqino re-vendor → DECIDED: full re-vendor** off v2.1, done at-merge from `origin/main` once it carries PR #25/#27 (see airqino AT-MERGE). Migrate the 2 rows first.
- **O3 — nprcgenekeepr "40k" wording → DECIDED: align now.** Wording-only fix to `CLAUDE.md` (~L171) + `PROJECT_LEARNINGS.md` header (see nprcgenekeepr NOW step 1).
- **O4 — wording trigger → DECIDED: apply from PR branches now.** Source the new wording verbatim from the PR-25/27 branches; do not wait for KJ5HST and do not merge fork main. Collapses the bucket split (see Execution model → Sourcing). Residual risk accepted: if upstream review changes wording, a small re-touch follows; for wsfct keep the vendored baseline copy aligned so `bin/sync` stays coherent.

## Provenance
- Survey: workflow `wf_dc1a6d1f-650` (5 parallel per-project assessments + synthesis), 2026-06-06.
- Memory: `project_adopter_pr2527_gap_survey`, `project_learnings_location_vs_claudemd_limit`.
- PRs: KJ5HST/methodology #25 (`ed9007c`), #27 (`1999f4a`, `a33b269`) — both OPEN as of 2026-06-06; **both MERGED verbatim into KJ5HST/main 2026-06-12** (no upstream rework, so the captured Assets C/D matched merged canonical byte-for-byte).

---

## Execution record (2026-06-12)

Both PRs merged upstream the morning of 2026-06-12; fork `main` was synced from `upstream/main` (v2.7) and used as the wording/re-vendor source. Between 2026-06-07 and 06-12, per-project sessions had already executed much of the NOW work from project-local briefs — each pass below was re-verified against the live repo before editing (premise-per-target).

| Project | What was already done (pre-2026-06-12) | What this execution added | Landed as |
|---|---|---|---|
| **wsfct** | s313 (#502): 113 rows → `PROJECT_LEARNINGS.md`, receptacle, C1/C2/C3 + Asset D in root + baseline | Drift reconcile: customizations (BACKLOG orientation, dashboard path, Mode Declaration, TDD-REFACTOR carve-out, blast-radius, push discipline, TDD phase-mapping) relocated verbatim to CLAUDE.md receptacle; `bin/sync --force`; `bin/status` now `current/current/current` | PR rmsharp/wsfct#520 |
| **model_project_constructor** | Fully done by its own session (58 learnings extracted, receptacle, C1/C2/C3; no vendored starter-kit → Asset D N/A) | Nothing — verified complete | — |
| **mts-system** | Execution brief drafted (uncommitted), nothing executed | Full pass per brief: 19 rows (Sessions 11–38; brief's 17 + 3 appended since, row 1 = canonical seed, stays) → `PROJECT_LEARNINGS.md`; 3C/caption/table byte-identical to canonical; C3 + targeted Asset-D row; **broad slim 908 → 360 lines** (11 sections relocated verbatim to `docs/` + `ROADMAP.md`, collisions with existing `docs/architecture.md`/`API.md` handled); receptacle added; brief committed for provenance | PR rmsharp/mts#1 (2 commits) |
| **airqino** | PART 1 done (Sessions 3–4): receptacle + learnings inline, table de-duplicated; PART 2 (re-vendor) DEFERRED pending upstream merge | PART 2 via the brief's recommended DEFER path: full re-vendor v2.1 → v2.7 from `origin/main`; `bin/sync --force`; CLAUDE_TEMPLATE size-budget comment added; airqino is now the 2nd sync-wired adopter | PR rmsharp/airqinodashboard#1 |
| **nprcgenekeepr** | Reference end-state (migration done Sessions 10/28) | Wording-only: C1/C2 (3C now byte-identical to canonical; seed rows already matched), C3, O3 "40k" → "~200 lines / ~25 KB" budget language in CLAUDE.md + PROJECT_LEARNINGS.md header | local branch `chore/methodology-pr2527-wording` (`ce7d6779`), **not pushed** — local `add-methodology` carries 13 unpushed session commits and Session 63 was in flight; merge after S63 closes |

Isolation: every edited repo had a live or recent in-flight session (wsfct S326, mts S39 burn-in, nprc S63), so all work was done in git worktrees on fresh branches; no working tree, session-notes file, or in-progress branch was touched.
