# Operational Backlog (fork-only)

Operational/coordination backlog for **rmsharp's** methodology work. Fork-only — it lives in
`docs/planning/` and is **not** part of the canonical framework or any upstream PR (same convention
as [`adopter-pr25-27-remediation-plan.md`](adopter-pr25-27-remediation-plan.md)).

This is a backlog, **not** GitHub issues, by operator decision.

**Open: BL-11, BL-12, BL-13, BL-14, BL-16, BL-17, BL-18, BL-19, BL-20 (residual only), BL-21,
BL-22, BL-23, BL-26, BL-30, BL-31, BL-32, BL-36, BL-37 (half (a) done, half (b) open), BL-39,
BL-42, BL-43, BL-44, BL-45, BL-46.**
Re-derive rather than trust that list —
it is hand-maintained, and it has been wrong before:

```
grep -nE '^\*\*BL-[0-9]+ —' docs/planning/BACKLOG-DETAIL.md
```

**That grep now reads the DETAIL file, not this one** — since S99 the item bodies live in
[`BACKLOG-DETAIL.md`](BACKLOG-DETAIL.md) and this file carries a one-row index of them (§Open
items). Run against *this* file it matches nothing, which is a wrong answer rather than an obvious
failure, so the path above is the one that still means what it used to mean.

Two things that grep will *not* tell you, both deliberate: **BL-16 is open but has no heading of
its own**, living inside BL-14's follow-ons paragraph — so it is absent from that grep's output and
present in the index, the one row not derivable from the detail file's headings; and **BL-20's
heading now covers only its open residual**, its closed history having moved to the archive below.

**⚠ Do not trust a number in this file without re-deriving it.** S30 re-measured every open item
and found a wrong number in **six of six**; the corrections are in `CHANGELOG.md` (*"The framework's
context cost — adopter heuristics and a remediation plan"*) and the items themselves are
deliberately NOT edited (FM #17). Known-wrong figures still standing in the item prose (now in
[`BACKLOG-DETAIL.md`](BACKLOG-DETAIL.md), moved verbatim and so still carrying every one of them): the
live-voice *"32 receipts"* (it is 33), BL-18's *"30 anchors"* (28) and its *"cannot be repaired
without fabricating a citation"* (false), BL-12's *"four sites"* (five), and BL-16's
`bin/check-handoff:301-303` (it is `:487`, and was never `:301-303` at any tree that ever existed).

**Closed items are archived, not kept here.** Eleven closed items — BL-8, BL-15, BL-20's closed
half, BL-24, BL-25, BL-27, BL-28, BL-29, BL-33, BL-34, BL-35 — live verbatim in
[`BACKLOG-archive-2026-08-15.md`](BACKLOG-archive-2026-08-15.md), with a one-line pointer row each
in §Completed items below. Losslessness is proved by
[`BACKLOG-archive-2026-08-15.md.verify.sh`](BACKLOG-archive-2026-08-15.md.verify.sh) — run it
rather than trusting this sentence. **Grep the archive too**, not just this file: BL-36 was raised
into this file 471 lines below BL-27, which already contained its answer, and cost a session.
The narrative of *what was done and when* belongs to [`CHANGELOG.md`](../../CHANGELOG.md), which is
the authoritative action ledger; this file holds open work only.

> **BL-10's parked fix — HALF of it is now moot, and the other half found a home. Still do not
> re-propose it, and still do not lose it.** It is **not** on `main`. It exists only on branch
> `docs/bl-10-dangling-learning-citations` (local + `origin`) and on the annotated tag
> **`archive/bl-10-citations`** (pushed to `origin` only — deliberately namespaced under `archive/`
> so it is never mistaken for a release tag and never mirrored as one). Commits: **`1eac7a4`** (the
> five citation rewrites) and **`268f1e5`** (`bin/check-citations` + Test 23), based on `d6dd6c9` =
> `upstream/main` at 2026-08-01. Verified at that SHA: `bin/tests.sh` 91/91, `bin/check-citations`
> OK, `bin/check-links` OK (85 links / 21 files).
> Recover with `git checkout archive/bl-10-citations` even if the branch is deleted on both sides.
>
> **Status as of the S26 resync (2026-08-01):**
> — **`1eac7a4` (the prose) is SUPERSEDED.** Upstream `15ccb38` fixed the same five sites the same
> evening, from the same rad-con root cause, with the same disposition. The two fixes differ only in
> wording and in how hard each re-grounds the claim — see **BL-13**, which is where that difference
> stopped being cosmetic.
> — **`268f1e5` (the checker) is NOT superseded.** Upstream shipped the prose fix with **no**
> mechanization and then filed [issue #65](https://github.com/KJ5HST/methodology/issues/65) asking
> for exactly this class of assertion. The branch's contiguity guard is a *partial* answer to #65's
> Learnings-table half; #65 also wants duplicate-row, malformed-row and one-physical-line detection,
> plus a `--all` mode for `bin/check-handoff`, none of which this branch has.
> **Status of PR #64 is unchanged: opened *without operator authorization* and closed at his
> instruction. An open upstream issue is an invitation to the maintainer's own repo, NOT
> authorization** — no agent may reopen #64, open a replacement, comment upstream, or answer #65
> without an explicit ask.

> **S34 regression note (2026-08-03), recorded not fixed.** The parked `bin/check-citations`
> (branch `docs/bl-10-dangling-learning-citations`, tag `archive/bl-10-citations` → `268f1e5`) is
> hard-anchored on `REGISTRY_FILE = "starter-kit/SESSION_RUNNER.md"` (`:34`) and
> `REGISTRY_HEADING = "## Learnings (added by sessions)"` (`:35`). It exits 0 against `816984b` and
> aborts `GUARD FAIL — the Learnings table parsed to zero rows` (exit 2) against the post-S34 tree,
> because the table now lives in `starter-kit/FRAMEWORK_LEARNINGS.md` under `# Framework Learnings`.
> **Whoever revives it — S43 absorbs it into `bin/check-derived` — must retarget both constants.**
> The guard failing loudly rather than silently passing is the tool behaving correctly.

## Open items

**Routing — what a session can actually run today.** Until 2026-08-03 several items below
carried *"blocked on the paused channel"* as their disposition. **That constraint was never
imposed** (see [`framework-context-cost-plan.md`](framework-context-cost-plan.md) §5): the
operator's rule is *ask before each outward-facing action, batch and vet to protect the maintainer's
review time* — sequence, not suspension. Nothing here is blocked for that reason.

- **Runnable now, nothing outward-facing.** **BL-18** — S30 proved its stated blocker false.
  **BL-22**, **BL-30**, **BL-32** — measurement and decision work, fork-side throughout.
- **Runnable now up to the PR, which needs a go-ahead.** **BL-13**, **BL-12's first bullet**,
  **BL-14's distributed half**, **BL-17's distributed half**, **BL-20's residual option (3)**,
  **BL-21**, **BL-31** (already opened as PR #71), **BL-36's repair**. Each touches a
  `bin/_manifest.py`-**DISTRIBUTED** file, so the *fix* lands upstream — but the preparation and the
  evidence are fork-side and are the part that carries the work. Batch them rather than sending each
  alone; that is what the operator's rule is protecting.
- **Genuinely not advanceable by a session, and the only one.** **BL-11** — its deliverable is *a
  maintainer decision*, not an edit. No amount of fork-side work produces it. This is what a real
  block looks like, and it is worth contrasting with the ones above that were mislabelled as one.
- **Not the fork's to raise.** **BL-12's second bullet** is upstream
  [issue #65](https://github.com/KJ5HST/methodology/issues/65); answering it is an outward-facing
  action and needs an explicit ask.

**Index only — one row per open item. The full text of every item lives in
[`BACKLOG-DETAIL.md`](BACKLOG-DETAIL.md), read on demand.** Nothing was compacted, reworded or
dropped in the split (S99): the bodies are byte-identical to what stood here, which
[`BACKLOG-DETAIL.md.verify.sh`](BACKLOG-DETAIL.md.verify.sh) re-derives from git — run it rather
than trusting this sentence.

Re-derive this table rather than trusting it; the population it indexes is:

```
grep -nE '^\*\*BL-[0-9]+ —' docs/planning/BACKLOG-DETAIL.md
```

| Item | What it is | Full text |
|------|------------|-----------|
| **BL-11** | Unreachable non-`Learning` referents across the distributed corpus | [detail](BACKLOG-DETAIL.md#bl-11) |
| **BL-12** | Two verified corpus defects found during BL-10's sweep, out of its declared scope | [detail](BACKLOG-DETAIL.md#bl-12) |
| **BL-13** | Upstream's citation fix left an unattributed false claim standing in a distributed file | [detail](BACKLOG-DETAIL.md#bl-13) |
| **BL-14** | The `commit:` answer slot — a distributed promise with no owner and no detector | [detail](BACKLOG-DETAIL.md#bl-14) |
| **BL-16** | *(no heading of its own, by design)* — lives inside BL-14's follow-ons paragraph | [detail](BACKLOG-DETAIL.md#bl-14) |
| **BL-17** | The `changelog_ref` referent the seed does not offer, and the one title that is stale | [detail](BACKLOG-DETAIL.md#bl-17) |
| **BL-18** | The same line anchors, in `key_files`, where the checker's schema requires them | [detail](BACKLOG-DETAIL.md#bl-18) |
| **BL-19** | The framework's context cost — adopter heuristics and the design deficiencies behind them | [detail](BACKLOG-DETAIL.md#bl-19) |
| **BL-20** | The seed documents only the `- **Model:**` list form the live ledger does not use — RESIDUAL only, defect FIXED | [detail](BACKLOG-DETAIL.md#bl-20) |
| **BL-21** | When the Phase 1B carve-out goes upstream, two seed sentences must ship with it | [detail](BACKLOG-DETAIL.md#bl-21) |
| **BL-22** | `DOC_ONLY_SOURCE_LOC_MAX = 200` — an unexamined round number, no test, decides a user-visible verdict | [detail](BACKLOG-DETAIL.md#bl-22) |
| **BL-23** | Issue #65's proposed invariants collide with fork state issue #65 doesn't know about | [detail](BACKLOG-DETAIL.md#bl-23) |
| **BL-26** | Issue #67 and PR #66 vs this fork's current state — neither addressed, PR #66 has its own collisions | [detail](BACKLOG-DETAIL.md#bl-26) |
| **BL-30** | Watch item, not a defect: `methodology_trim.py`'s next firing outside `nprcgenekeepr` | [detail](BACKLOG-DETAIL.md#bl-30) |
| **BL-31** | `upstream/main`'s dashboard exclusion list wasn't updated for PR #66's new distributed file | [detail](BACKLOG-DETAIL.md#bl-31) |
| **BL-32** | `methodology_trim.py`'s `LEDGERS` covers only the framework's own two ledgers; an adopter's third has no path | [detail](BACKLOG-DETAIL.md#bl-32) |
| **BL-36** | Four of the six shipped `.verify.sh` losslessness proofs do not hold — found, not fixed | [detail](BACKLOG-DETAIL.md#bl-36) |
| **BL-37** | This repo ships a size-ceiling gate it does not run on itself; the shipped list has no `BACKLOG.md` entry | [detail](BACKLOG-DETAIL.md#bl-37) |
| **BL-39** | Issue #75's two *Related* items — carry the named surface forward into close-out | [detail](BACKLOG-DETAIL.md#bl-39) |
| **BL-42** | `methodology_trim.py` still generates the fat pointer block S109's compaction removed | [detail](BACKLOG-DETAIL.md#bl-42) |
| **BL-43** | Six `bin/tests.sh` assertions flake under `pipefail` — diagnosed, enumerated, not fixed | [detail](BACKLOG-DETAIL.md#bl-43) |
| **BL-44** | `bin/check-learnings` reports `contiguous 1..N` from `len(rows)`, so a reserved gap makes it false | [detail](BACKLOG-DETAIL.md#bl-44) |
| **BL-45** | `FRAMEWORK_LEARNINGS.md` is 16 B from its ceiling — **blocks Phase 3C for the next session** | [detail](BACKLOG-DETAIL.md#bl-45) |
| **BL-46** | An adopter's trimmer inert since bootstrap; the seed's own removal has no detector | [detail](BACKLOG-DETAIL.md#bl-46) |
| **BL-47** | Seed `context-budget.json` omits the two ledgers `methodology_trim.py` exists to bound | [detail](BACKLOG-DETAIL.md#bl-47) |
| **BL-48** | Seed `HANDOFFS.md` lacks the count sentence its own `LedgerSpec` declares | [detail](BACKLOG-DETAIL.md#bl-48) |
| **BL-49** | `content_probe` runs only at zero records, so a partial grammar mismatch freezes into a shard | [detail](BACKLOG-DETAIL.md#bl-49) |

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
| **BL-10** | Five dangling `Learning #N` citations in adopter-distributed files | ✅ CLOSED 2026-08-01 — **the defect is fixed in the corpus, but not by this fork's work.** The corrected record, restated at the S26 resync: the fork's fix was opened as [PR #64](https://github.com/KJ5HST/methodology/pull/64) *without authorization* and **CLOSED, never merged**; the maintainer then fixed the same five sites independently in `15ccb38`. The earlier wording here read "SHIPPED … via PR #64", which was wrong on both counts. The fork's analysis below stands and was reached first; **its predicted failure then came true — see BL-13**, where upstream's fix kept one of the false claims after removing its citation. The parked branch survives for `bin/check-citations` alone (now partial input to [issue #65](https://github.com/KJ5HST/methodology/issues/65)). All five traced to the 2026-05-02 Pocock audit, written in session S438 of a *different* methodology instance whose Learnings table ran into the 30s. **Three were worse than dangling** — they asserted framework rules that do not exist (there is no handoff length discipline; the only `150`-as-handoff-length string in the distributed corpus was the line claiming it), so stripping just the numbers would have left unattributed false claims. Each site re-grounded on a reachable referent; dispositions unchanged; no Learnings row added or edited. Mechanized per Learning #12: canonical-only `bin/check-citations` + Test 23, driven RED first (6 findings), with every guard driven RED too — mutation-testing the fixture caught a real defect in the checker itself (a missing registry file exited 1, indistinguishable from a corpus finding). Suite 84 → 91. Follow-ons raised as BL-11 and BL-12. |
| **BL-8** | Subagent capability-tiering — adopt as an operational default, or decline | ✅ **ADOPTED** 2026-08-11 (S78), operator-directed. Not a methodology change; no distributed document edited. This fork now authors gate-checkable `Workflow` subagent roles on a lighter tier while judgment and review roles stay on the strongest available tier. |
| **BL-15** | `changelog_ref`'s deictic deferral — 13 of 32 receipts defer instead of naming an entry | ✅ **CLOSED** 2026-08-02 (S29). Raised correctly — the "13 of 32" is exact — and **already discharged by BL-14's own repair**, which gave all 13 receipts a real sha in `commit:` to defer to. Do not re-raise. Its one residual (the one-hop resolution is a convention no document states) is live in **BL-17**, not here. |
| **BL-20** | `bin/model-report`'s Source 1 blind to the `**Model:**` form this repo writes | ✅ **FIXED** 2026-08-11 (S79), option (1) — `CHANGELOG_MODEL_RE` widened to accept both dialects, RED-first, Test 30. **Option (3) remains open and is retained live in §Open items above.** |
| **BL-24** | `mts-system` focused UAT re-run | ✅ **CLOSED** 2026-08-08 (S50). F9 confirmed resolved, F10 improved 1 → 0, **F6 and F7 reproduce unchanged and are still open** in [`uat-2026-08-08-followup.md`](uat-2026-08-08-followup.md) §8, F11 not applicable. Zero regressions; read-only throughout. |
| **BL-25** | `vscode_quarto_ext` focused UAT re-run | ✅ **CLOSED** 2026-08-08 (S53). Net 1 of 7 improved (F9); **F2, F3, F6, F8 unchanged and still open** in [`uat-2026-08-08-followup.md`](uat-2026-08-08-followup.md) §9; F10/F11 unchanged-and-clean. Zero regressions; read-only throughout. |
| **BL-27** | `methodology_trim.py`'s generated `.verify.sh` — two false-positive triggers on `HANDOFFS.md` | ✅ **CLOSED** 2026-08-10 (S65), `TRIM_VERSION` 1.1.1 → 1.1.2, 4 tests. **Read this one before concluding an archive lost data:** it states the bundled-commit trigger *"is not evidence of historical data loss"* and predicted the exact re-raise that became BL-36. Its fix 2 deliberately keeps that case a loud FAIL. |
| **BL-28** | The generated `.verify.sh`'s L2 front-matter check was a substring test, not exact-line-set membership | ✅ **CLOSED** 2026-08-10 (S68), `TRIM_VERSION` 1.1.2 → 1.1.3, 2 RED-first tests (97/97). An append-style edit that kept the original text as a substring was invisible to the check. |
| **BL-29** | D4(c)'s directory-exclusion fix missed the self-scan case | ✅ **CLOSED** 2026-08-10 (S72). `resolve_single_project_root()` bridges the canonical repo's two checked-in copies (`tools/`, `starter-kit/`) to their repo root; `DASHBOARD_VERSION` 2.14.0 → 2.15.0, 6 RED-first tests, with a negative control proving the `bin/_manifest.py` marker — not the directory name — gates the behaviour. |
| **BL-33** | `bin/model-report`'s `CHANGELOG_ENTRY_RE` can't parse a multi-tag `### ` header | ✅ **FIXED** 2026-08-11 (S80). Widened to accept adjacent `[TAG]` groups; a non-matching `### ` line is now a loud `WARNING` instead of being silently folded into the preceding entry. Closed BL-20's reported 51-vs-52 population gap (now 55 = 55). |
| **BL-34** | `methodology_dashboard.py`'s `LANG_MAP`/`DOC_EXTS` blind to R, Quarto, R Markdown | ✅ **FIXED** 2026-08-11 (S81), **merged upstream** as [PR #72](https://github.com/KJ5HST/methodology/pull/72) (`5c59f0b`, verified S85) **and synced into local `main`** 2026-08-12 (S86). Found scanning `../nprcgenekeepr`: 603 `.r` files, 77,773 LOC counted as Source but invisible in "Code by Language". |
| **BL-38** | `context_budget.py --calibrate` returned noise on any repo that had merged another lineage of its regressor, with no goodness-of-fit gate | ✅ **FIXED** 2026-08-15 (S91), `VERSION` 1.0.0 → 1.1.0, all five defects in the one DISTRIBUTED file. **D1** `--first-parent` (the ancestry walk made "size at time T" not a function); **D2** tz-aware datetime comparison (ISO stamps were ordered as strings across mixed offsets); together **14.75 B/tok at R² = 0.0503 → 2.81 at R² = 0.8054**, re-derived at n=76 and reproducing S90's n=75 table within rounding. **D3** `calibration_verdict()` refuses below R² 0.50 (configurable via `calibrate_min_r2`), refuses a negative slope however tight the fit, refuses an undefined R² — and **suppresses** the `⇒ bytes/token` line rather than annotating it. **D4** the ledger row now names the ceiling that fired (`HANDOFFS.md` read `417 ln / 1,200 ln — over` for a **byte** breach). **D5** remediation prose no longer names the tool's home-project directories nor states that project's measurement as a claim about the reader's repo. Plus a leaked file descriptor per transcript in the same loop. Evidence: new canonical-only `tools/test_context_budget.py` (41 tests, wired into `bin/tests.sh` — `calibrate()` previously had **no** test of its arithmetic), `--selftest` 13 → 34 gates, **10-mutant round 10/10 killed** with control green and restorations `cmp`-verified, harness 229/1 diffed row-for-row against baseline. **One boundary re-derived the hard way and now pinned:** git's default history simplification already prunes a TREESAME merge, so D1 needs a merge that *changed* the target — the first fixture used `merge -s ours`, did not reproduce the defect, and would have passed against the broken code. **Fork-side only; no PR opened.** |
| **BL-35** | `starter-kit/FRAMEWORK_LEARNINGS.md` rows 18 and 19 were malformed 2-column rows | ✅ **FIXED** 2026-08-11 (S84). Live since S40/S41; found by `bin/check-learnings` arriving via S83's upstream merge; the two missing cells recovered by git archaeology on the rows' authoring commits (`11b843a`, `12463dd`) and approved before writing. Distributed to adopters at their next `bin/sync`. |
| **BL-40** | A `HANDOFFS.md` trim at the trimmer's default cut silently made Test 34's anchor-dependent assertions vacuous | ✅ **FIXED** 2026-08-17 (S96), **option (b) exactly as recorded** — canonical-only, `bin/tests.sh` alone, zero distributed files (verified against `bin/_manifest.py`'s 26 SOURCE rows, none under `bin/`). The indexed reads `ids[1]`/`ids[2]` become a population with a stated floor: `handoff_anchors` returns `<count> <A1> <A2>` and cannot raise, `anchor_disposition` routes that count to MALFORMED / EMPTY / SHORT / ANCHORED, and the SHORT arm emits **six** `SKIP` rows naming each unbuildable assertion and why. A new `skip()` primitive counts separately from `pass()` and the summary line carries the total — routing an unbuildable assertion to `pass()` was the real hazard, and nothing a reader watches would have moved. **RED first, against copied fixtures, never the live ledger:** the pre-change body replayed at 1/2/3/4 receipts gave 2 passed / 5 failed below the floor and 8 / 0 at or above it; after, 11 / 0 / 6 skipped and 17 / 0 / 0. EMPTY (0 receipts) fails rather than skips — corruption is not rotation. **This item's own count was low: SIX assertions stopped running, not five** — the sixth sat in a failed guard's then-branch and emitted no row at all, which is why the pass delta (−6) never matched the failure delta (+5). Recorded as **Learning #33**. **9-mutant round, 9/9 killed**, unmutated control green, including both mutants that would silently reinstate the vacuum: a renamed `SHORT)` arm (reads as 0 skip rows) and a non-numeric count falling through to the permissive default. Option **(a)** — a retained-records floor in the distributed trimmer — stays **declined** for the reason recorded here: the trimmer has no business knowing a test's fixture requirements, and the floor would ship to adopters who never run Test 34. **What this still does not do, unchanged:** it cannot stop a default trim from cutting to 2, only stop that from being silent. `--cut 3` remains the right cut for this ledger. |
| **BL-41** | `methodology_trim.py` could not trim `HANDOFFS.md` at all: shard-naming-by-date and Test 34's retention floor had no common solution | ✅ **FIXED** 2026-08-23 (S100), **option (1) exactly as recorded — collision disambiguation**, operator-chosen from four costed levers at Phase 2. `TRIM_VERSION` 1.2.0 → **1.3.0**. **The defect stated precisely:** the shard name is a function of a RECORD DATE while the cut is POSITIONAL, so the naming function is **not injective** — distinct cuts derive one name whenever two records share a date — yet the name was used as a unique key behind a write-once refusal. The tool's own advice, *"Disambiguate with `--cut`"*, could not work: a date cut key both SELECTS the records and BECOMES the key, so there is no second knob. A taken name is now resolved to `-2`, `-3`, … and **reported** (`SHARD_NAME_DISAMBIGUATED`); write-once is unchanged — nothing is ever overwritten, and past `SHARD_SUFFIX_MAX` the tool still refuses with `SHARD_EXISTS`. **Verified on the live case BL-41 said had none:** `--cut 3` now archives to `docs/archive/HANDOFFS-through-2026-08-17-2.md`, retaining Test 34's floor of three, 82,966 B → **43,928 B** — 21,608 B under the ceiling, more than a full receipt of headroom. Dry run only; **no trim was run** (a second capability, FM #26). **RED first**, against copied fixtures in `tempfile` repos, never the live ledger: 3 failures + 2 errors before the fix, with the fixture control and the free-name negative control green on BOTH sides. **9-mutant round, 9/9 killed**, each verified to APPLY, control green before and after, every restore `cmp`-verified. **Two things the research killed, and they are worth keeping:** option (2) — name the shard by record range — is **unsound for this ledger**, because its own front matter records that two session sequences share it and their `S<N>` numbers collide (upstream S7/S8 vs the fork's S7/S8), so it reintroduces the same non-injectivity on a different axis; and `LedgerSpec` carries only `date_of_record`, so `CHANGELOG.md` records have no identity but their date. Option (3) — dropping Test 34's floor — was **declined** because it does not fix the naming defect at all; it removes the constraint that made *this instance* unsatisfiable while the defect survives and recurs. **The `.verify.sh` half is part of the fix, not decoration:** the shard and its proof are written as a pair, and a check that looked only at the shard would overwrite a frozen proof left by an interrupted run — the same corruption write-once exists to exclude, one file over. That narrowing is the M1/M2 mutant pair and both die. |

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
