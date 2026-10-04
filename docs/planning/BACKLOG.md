# Operational Backlog (fork-only)

Operational/coordination backlog for **rmsharp's** methodology work. Fork-only — it lives in
`docs/planning/` and is **not** part of the canonical framework or any upstream PR (same convention
as [`adopter-pr25-27-remediation-plan.md`](adopter-pr25-27-remediation-plan.md)).

This is a backlog, **not** GitHub issues, by operator decision.

**Open: BL-11, BL-12, BL-13, BL-14, BL-16, BL-17, BL-18, BL-19, BL-20 (residual only), BL-21,
BL-22, BL-23, BL-26, BL-30, BL-31, BL-32, BL-36, BL-37 (half (a) done, half (b) open), BL-39,
BL-42, BL-44, BL-46, BL-47, BL-48, BL-49, BL-50, BL-51, BL-52, BL-54, BL-55, BL-57, BL-58, BL-60, BL-61, BL-62, BL-64 (residual only), BL-65, BL-66, BL-68, BL-70, BL-71, BL-73, BL-74, BL-75, BL-77, BL-79, BL-80, BL-81, BL-84, BL-85, BL-87, BL-92.**
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
in [`BACKLOG-COMPLETED.md`](BACKLOG-COMPLETED.md) — which is where every closed item's pointer row
now lives, since S223; §Completed items below keeps the ids and the path to it. Losslessness is
proved by
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
| **BL-36** | Four of the six shipped `.verify.sh` losslessness proofs do not hold — found, not fixed. **Operator, S173 (2026-09-16, picker):** **folded into BL-60's design session**; the four frozen proofs are decided inside the new scheme, not regenerated first | [detail](BACKLOG-DETAIL.md#bl-36) |
| **BL-37** | This repo ships a size-ceiling gate it does not run on itself; the shipped list has no `BACKLOG.md` entry | [detail](BACKLOG-DETAIL.md#bl-37) |
| **BL-39** | Issue #75's two *Related* items — carry the named surface forward into close-out | [detail](BACKLOG-DETAIL.md#bl-39) |
| **BL-42** | `methodology_trim.py` still generates the fat pointer block S109's compaction removed | [detail](BACKLOG-DETAIL.md#bl-42) |
| **BL-44** | `bin/check-learnings` reports `contiguous 1..N` from `len(rows)`, so a reserved gap makes it false. **S176: half fixed, without knowing this item existed** — `8cfaf0d` reads the span off the parsed rows (`min..max`), but the message does not yet name the reserved gap as the detail's fix proposes. **Operator, after S176 (2026-09-16, picker): keep open** for that half | [detail](BACKLOG-DETAIL.md#bl-44) |
| **BL-46** | An adopter's trimmer inert since bootstrap; the seed's own removal has no detector | [detail](BACKLOG-DETAIL.md#bl-46) |
| **BL-47** | Seed `context-budget.json` omits the two ledgers `methodology_trim.py` exists to bound | [detail](BACKLOG-DETAIL.md#bl-47) |
| **BL-48** | Seed `HANDOFFS.md` lacks the count sentence its own `LedgerSpec` declares | [detail](BACKLOG-DETAIL.md#bl-48) |
| **BL-49** | `content_probe` runs only at zero records, so a partial grammar mismatch freezes into a shard | [detail](BACKLOG-DETAIL.md#bl-49) |
| **BL-50** | `insert_pointer` injects a byte `L2`'s reversal never removes — the trimmer refuses a correct trim | [detail](BACKLOG-DETAIL.md#bl-50) |
| **BL-51** | The distributed `2,000-line read cap` premise is false — plan RATIFIED at S111; **Phase A shipped**, Phases B and C open | [detail](BACKLOG-DETAIL.md#bl-51) |
| **BL-52** | The line metric measures a condition trimming may not remedy — ordered truncation of a newest-on-top file | [detail](BACKLOG-DETAIL.md#bl-52) |
| **BL-54** | `bin/sync` and `bin/status` walked history without `--full-history`, so a version from a merge's other side read as locally modified. **FIXED FORK-SIDE AT S179** (`2c4f801`; `865119f` batches the blob lookups): sync walks the full history, and status counts the versions that landed on the first-parent line, falling back to the full walk (**operator, S179: option C**). On the six adopters, 8 rows read *N versions behind* again and the 3 genuine edits stay *locally modified*; RED-first Test 41. **Open only for its upstream PR, its own go-ahead** — proposed as one PR with BL-66's fix, [`sync-github-route-plan.md`](sync-github-route-plan.md) D3 (S217; taken, S218) | [detail](BACKLOG-DETAIL.md#bl-54) |
| **BL-55** | Nothing enforces removing a completed `BACKLOG.md` item — Signal F only reports, and adopters rarely carry the `[BL-N]` join key | [detail](BACKLOG-DETAIL.md#bl-55) |
| **BL-57** | **HIGH PRIORITY** — the `CHANGELOG.md` rules contradict each other across the framework; fix here and in six adopters, aiming at an upstream PR. [`changelog-rules-contradictions-plan.md`](changelog-rules-contradictions-plan.md), approved at S162 (Q1–Q4 all A). **P1–P4 done** on branch `bl57/changelog-rules` (`83a12f0`, on `origin`). Fork `main` was resynced with `upstream/main` `6b29d3d` first (S176–S177). **P5 done at S178, by merge** (`22ce71b`, operator): fork `main` carries the rules; D10 removed the hook's claim carve-out and Test 27, and `tests-sh-passed` went 327 → 294 (operator-approved). **BL-54 fixed fork-side at S179. P6 (`airqino`) done in that repository, recorded at S180; P7 (`wsfct`) done there and MERGED to its `master` (PR #903, squash `66e14daa`), recorded at S185 with items (19)–(21); next P8–P11** (one adopter per session, P8 `vscode_quarto_ext`; item (18) decided at S181 by the operator: one `bin/sync` run is one commit, and item (20) records that a squash-merging adopter keeps that shape only on the PR's head ref; item (21) decided at S186 by the operator: P8–P11 also migrate a stale `HANDOFFS.md` seed, which is P8 and P9 today; item (22) done at S187: `bin/status`'s note gives each stale seed its own route, on the branch `100f09b`, merged into fork `main` `2d5ce70`), then P12's PR, which also carries BL-62 and #80's F5. **S188: F5, BL-62 and BL-63 are on the branch** (`657acb7`, `5223afb`, `0d63410`) and merged into fork `main` (`5f5a400`); plan item (23). **P12 done at S189: [PR #84](https://github.com/KJ5HST/methodology/pull/84) OPEN** (head `20db3f0`; plan item (24)), after an independent review's five fixes. **S190: the branch merged into fork `main`** (`2410657`, item (24) (a)). **P8 (`vscode_quarto_ext`) done in that repository, recorded at S191** (items (25)–(27)); the operator kept the plan and put BL-72 before P9 (S191). **BL-72 done at S192** (`77afc12` on the branch, riding PR #84; `ea1a057` in fork `main`). **P9 (`mts-system`) done in that repository, recorded at S193** (items (28)–(29)), with one remainder there, a superseded rules block (item (28), its CLEANUP-006). **P10 (`nprcgenekeepr`) decided at S194 (`--force`, then re-apply its trimmer extension; launch prompt [`bl57-p10-nprcgenekeepr-launch-prompt.md`](bl57-p10-nprcgenekeepr-launch-prompt.md)), done in that repository (its S719) and recorded at S194** (items (30)–(31)). **`nprcgenekeepr` pushed `4cfe2dad..4565c39d` after S194's close-out, and every per-push workflow passed on it, R-CMD-check included; the plan's P10 block and row say so since S195. **P11 (`model_project_constructor`) decided at S195** (operator, picker: (a) the runner's rows and *Wiki sync* paragraph into `CLAUDE.md`, step 5 retired; (b) the ledger adopts the rules going forward, cadence included, superseding that project's `PROJECT_CONVENTIONS.md` §2), **done there the same day (its Session 259, `bb91fda`..`159e739`, not pushed) and recorded here at S195**, re-verified from a clone; plan items (32)–(37), item (34) corrected by the run. **Every adopter phase P6–P11 is now done; what remains is PR #84's review**; **next: watch #84**. **Operator:** no `CHANGELOG.md` trim at its trigger (2026-09-14, reaffirmed S177) | [detail](BACKLOG-DETAIL.md#bl-57) |
| **BL-60** | Every trim writes a ~16 KB proof script **97.9% identical** to the last; 31 of them hold **453,689 B, 5.4% of the tracked repo**, and the proof costs more than the median receipt it proves. Shapes: shared harness + per-shard manifest, publish the command instead, or stop tracking it. **Distributed — `methodology_trim.py` lands at every adopter root, so its own go-ahead.** **Operator, S173 (2026-09-16, picker):** **one planning session costs the three shapes and folds BL-36 in** | [detail](BACKLOG-DETAIL.md#bl-60) |
| **BL-58** | Consider instructing adopters on lossless ledger trimming — they receive `methodology_trim.py` at their root but the runner, the apparatus and `SAFEGUARDS.md` say nothing about it; the only guidance sits in two never-overwritten seeds. Decision first: (a) the tracked apparatus, (b) the runner, (c) better tool output | [detail](BACKLOG-DETAIL.md#bl-58) |
| **BL-61** | Lower `HEADER_RESERVE_BYTES` (`bin/check-handoff:663`, 7,168 B) now that `HANDOFFS.md`'s front matter is 4,019 B and no longer grows per trim — bank the freed ~3 KB as S109 did. **Operator, S174 (2026-09-16, picker): scheduled for a later small session.** Canonical-only | [detail](BACKLOG-DETAIL.md#bl-61) |
| **BL-62** | Upstream's `TestThisRepoReadSetPartition` (`tools/test_context_budget.py:1256`) sums the token ceilings of **every** whole-read class against one 25,000-token Read, but only the read-set pair is read together; a read-mandated class's files are read separately. Hit at resync M2 by the fork's two ledgers (25,000 tokens declared on each, 50,000 in sum), worked around at `0e8c6ac`. Test is canonical-only: no adopter impact. **Operator, after S177: carry it in BL-57's P12 PR**, not a standalone issue. **S188: fixed on the branch** (`5223afb`, test-first; the sum covers only `READ_TOGETHER_CLASSES`, the read-set pair), merged into fork `main` (`5f5a400`). Open until P12's PR merges | [detail](BACKLOG-DETAIL.md#bl-62) |
| **BL-63** | A committed-mode `bin/sync` writes more files in one run than the distributed `SAFEGUARDS.md` lets one commit hold (15 and 21 in `airqino`'s two syncs; 14–16 in the S180 and S181 dry runs, against a cap of 5), and no distributed document says how to commit a sync. **Operator, S181 (picker):** for BL-57's P7–P11, one run is one commit (plan item (18)). Whether `SAFEGUARDS.md` or `BOOTSTRAP.md` should say so for every adopter rides the upstream PR. **Distributed, so its own go-ahead.** **S188 (operator, pickers): `BOOTSTRAP.md` says how, and `SAFEGUARDS.md`'s cap row names the case in one sentence**, so the two agree (`SAFEGUARDS.md` wins conflicts); on the branch `0d63410`, merged into fork `main` `5f5a400`; its own commit, droppable from P12's PR. Open until that PR merges | [detail](BACKLOG-DETAIL.md#bl-63) |
| **BL-64** | Test 38's drift guard measured a receipt from its opening fence to the NEXT receipt's, so the close-out prose between them read as receipt fields and `applied: ` turned the quality gate red on `main`. **Guard FIXED 2026-09-17 (S182)** (`4c6da50`, RED-first, two new assertions). **Open:** the close-out cites a gate run measured before the close-out commit exists, so the commit that writes the receipt is the one its own citation can never cover — S181 cited `10/10 pass` and shipped a red tree. Guard canonical-only; the Phase 3E timing rule is distributed | [detail](BACKLOG-DETAIL.md#bl-64) |
| **BL-65** | `tools/test_context_budget.py:372` assumes the r² floor is `calibrate()`'s only refusal, but a **negative slope** refuses independently of it — so the presence control fails on this machine's transcripts (slope −0.1773, R² 0.0004) while skipping in every clone, where the documented build-equivalent runs. The clone read `10/10 pass`; the working tree read `312 passed, 1 failed`. Note also that all four `*-unit-tests` gates extract `Ran (\d+) tests`, blind to failures. Canonical-only | [detail](BACKLOG-DETAIL.md#bl-65) |
| **BL-66** | **UPSTREAM-FACING** — `README.md:61` tells every adopter to update with the GitHub URL, but `bin/sync --source=github` fetches contents without history (`bin/sync:100`), so a file that is merely *behind* cannot be recognized and is refused as a *"local modification"*. Measured clean-room: an unedited adopter at upstream `008d656` got **exit 2 / nine files** from the URL route and **exit 0 / 10 written** from `--source=local`. `starter-kit/BOOTSTRAP.md:86` already says to prefer the local route, for this exact reason — two distributed documents, opposite advice. Its PR is its own go-ahead. **Plan: [`sync-github-route-plan.md`](sync-github-route-plan.md) (S217; ratified S218, D1–D8 all (a)). P1–P5 DONE** (S218–S222) on `fix/sync-github-history`, tip `67feb9f`: the route clones, the refusal names a source without its history, the documents match, P4 vetted it — trial merge into `upstream/main` a fast-forward, both cross-PR conflicts built and run (#84 212/0 with its phrase pins passing, #86 191/0), six adopters measured — and **P5 opened the pull request: [KJ5HST/methodology#87](https://github.com/KJ5HST/methodology/pull/87), `MERGEABLE` / `CLEAN`**, carrying [`sync-github-route-pr-body.md`](sync-github-route-pr-body.md) unchanged. **Next: P6, fork-side adoption — it waits on the merge; nothing further is owed upstream** | [detail](BACKLOG-DETAIL.md#bl-66) |
| **BL-68** | Investigate the dashboard's *"Large files detected"* penalty when the large files are the framework's own `methodology_*.py` tools and their tests: here all five are over 2,000 lines (the dashboard 4,729 per copy, the trimmer 2,181, the tests 5,867 and 2,291). *Layer 7* exempts an adopter's installed copies by version signature; the canonical repo pays for its own on purpose, and today's flag names `tools/test_methodology_dashboard.py`. Raised at S189 on the operator's request, widened the same session from the dashboard to every `methodology_*.py`; not investigated | [detail](BACKLOG-DETAIL.md#bl-68) |
| **BL-70** | Upstream's runner lacks issue #75's plan-surface rule: the maintainer closed #75 silently the day after the fork's PR was verified ready, and the PR (`docs/issue75-plan-surface-upstream`, `60246e7`, local only) was never sent. Branch kept (operator, S189); what to do upstream is open | [detail](BACKLOG-DETAIL.md#bl-70) |
| **BL-71** | The dashboard's *"Multiple branches"* signal counts `git branch -a` (HEAD aliases, upstream's branches), so a fork can never clear it; count unmerged local branches instead. Raised at S189 (operator); not investigated | [detail](BACKLOG-DETAIL.md#bl-71) |
| **BL-73** | `bin/check-handoff` reads a second `handoff` opener inside an open receipt as content, so a receipt begun twice reads as one block, and `--all` reports it only when the key order breaks. `mts-system`'s `HANDOFFS.md` has three (`:216`, `:320`, `:671` at `710a0f7`); `--all` reports two. Raised at S192, found while verifying BL-72; not fixed. Canonical-only; its upstream route is its own go-ahead | [detail](BACKLOG-DETAIL.md#bl-73) |
| **BL-74** | Keep `README.md` current: the canonical file (plan item (15)'s stale cost section) and the copies five adopters carry at `docs/methodology/README.md`, which `bin/sync` never updates (23–39 README commits behind; one matches no version). Raised at S195 on the operator's request; not investigated | [detail](BACKLOG-DETAIL.md#bl-74) |
| **BL-75** | `context_budget.py` has no `--status` command and ignores unknown arguments, so every cited *"`--status`"* run (including a gate command proposed to the maintainer in a PR comment) was the default measurement, which also appends a tracked history row. Raised at S195 from BL-57 P11. **S209: planned with BL-80 as ONE upstream PR, all decisions taken** — a write-free `--status`, unknown arguments refused with exit 3 ([`context-budget-status-plan.md`](context-budget-status-plan.md)). **S210: P1 built, `e859196` on the local branch `fix/context-budget-status`, not pushed. S211: P2 built, `c299c30`, same branch. S212: P3 done on `d4dbc26` and amended by the operator's review — D6: refused arguments' messages answer the intent, `--check` = `--status`. S213: P2b (D6) built, `612570b`, same branch. S214: P2c (D7) built, `2f73733`; P3′ on `c1167ae` (floors, trial merges green, the body rewritten and APPROVED by the operator). S215: P4 done — the branch pushed and the PR opened as [#86](https://github.com/KJ5HST/methodology/pull/86), the approved text unchanged; next: the maintainer's review, then P5** | [detail](BACKLOG-DETAIL.md#bl-75) |
| **BL-77** | Phase 0 reconciles the ledger thoroughly but never checks that the gates protecting it are ARMED in this clone: `core.hooksPath` is per-clone and opt-in, so a correct hook that was never enabled runs nothing while every gate reads green — the hook fails open, and its failure mode is silence. S198's `pre-commit-selftest` tests the hook's logic, not whether it is wired in. Raised at S198 from BL-76's closure; three shapes, none costed | [detail](BACKLOG-DETAIL.md#bl-77) |
| **BL-79** | `SESSION_RUNNER.md` §3G specifies the close-out report's **content** — four items and *"Then STOP"* — but not its **shape**: no header, no labels, no required identifiers, no closing line. A report can satisfy every word of it and still not read as a close-out report, which is what happened at S202 and prompted the operator to ask whether a format was specified. It is not: `Close-Out Report` and `Session over` return **0 grep hits** here and **0** in `nprcgenekeepr`, whose §3G is **byte-identical** to this one — the legibility difference comes from a project convention, not the framework. The 3G report is the only close-out artifact addressed to a human in real time, and the only place the *"1 and done"* boundary is announced, yet `HANDOFFS.md` has a 13-key schema and a checker while the report that announces it has neither. Distributed (`starter-kit/`), so the fix is an upstream PR and its own go-ahead. Raised at S202 on the operator's request; **costed at S252:** [plan](close-out-report-actuator-plan.md) — one tool that renders and lints the report, plus a Stop hook; phases P1-P3, decisions D1-D3 ratified 2026-10-03; **S253: P1 built** (`starter-kit/close_out_report.py`, `tools/test_close_out_report.py`, a ratchet gate); **S254: P2 built** (`--hook`, 68 tests, four scenarios run on the real harness; the operator's install of the snippet and one watched close-out are outstanding); P3, the distributed change, is its own go-ahead | [detail](BACKLOG-DETAIL.md#bl-79) |
| **BL-80** | `context_budget.py` prints *"Nothing is over a ceiling yet"* in the same run whose table shows **four** rows `over` — the sentence is a literal at `starter-kit/context_budget.py:652-653`, inside `if run_hit:`, reading no row's status. The growth run itself is right and right-scoped (a series over `resident_bytes`, printed only on the resident row precisely so a true number is not put where it becomes false); the defect is the advisory beside it, which breaks the rule the same file states one screen above. It is also BL-78 shape (3)'s prerequisite: a *reported series* is worth what its report is worth. Distributed (`bin/_manifest.py:54`), so the fix is an upstream PR and its own go-ahead. Raised while costing BL-78. **S209: planned with BL-75 as ONE upstream PR, decided** — the second sentence chosen by the headline's own `worst` ([`context-budget-status-plan.md`](context-budget-status-plan.md) §3 D3); **S211: P2 built, `c299c30` on the local branch `fix/context-budget-status`, not pushed; a status-precedence edge found and not fixed.** **S212: the edge goes in this PR (plan D7). S213: P2b done (`612570b`). S214: P2c built (`2f73733`, a check may raise a row's status, never lower it), and the body carrying it approved. S215: in [#86](https://github.com/KJ5HST/methodology/pull/86) (BL-75's P4); next: the maintainer's review, then P5** | [detail](BACKLOG-DETAIL.md#bl-80) |
| **BL-81** | `.context-budget.json` records the same two read-set file sizes in **three** places, and BL-78 P1's declared scope reached only one: `files[]` now says 55,406/17,129 while `_synced` and `_deliberate_exclusions` still say 54,363/15,386 *(wc -c, 2026-08-30)* fifteen lines below. The second of those notes exists *because* a prose size went stale, closes with *"never derive a ceiling from a size written in prose"*, and the size in that sentence is now 1,043 B stale by the identical mechanism in the identical file. **No behaviour depends on it** — both are `_` comment keys, `check_synced()` is drift-only and the other is inert — but `grep 54,363` is how three successive sessions reached *"over its declared size"*, and after P1 that grep still hits in a key nothing re-measures. Fork-only (this repo's config, not the distributed seed). Raised while doing BL-78 P1; **uncosted, nothing measured for it beyond what P1 already ran** | [detail](BACKLOG-DETAIL.md#bl-81) |
| **BL-84** | **UPSTREAM-FACING** — the distributed seed `starter-kit/context-budget.json` (installed once at every adopter root as `.context-budget.json`, `bin/_manifest.py:61` on fork `main`, `:53` on `upstream/main`) gives `CLAUDE.md` one fixed 24,000 B warn line **and** a mandatory `budget:protected` purpose fence whose body must be at least 800 characters; a missing fence is `over`, exit 2 (`starter-kit/context_budget.py:422-438`). The warn line is not set against the adopter's file, so a `CLAUDE.md` within about 850 B of it cannot comply without warning, and complying invites cutting rules text to get back to green: `mts-system` S143 went 23,557 B → 24,603 B adding the fence and was offered a 495 B deletion that would have left it at 24,108 B, still `warn`. Relayed by the operator at S217; four shapes, none costed | [detail](BACKLOG-DETAIL.md#bl-84) |
| **BL-85** | **UPSTREAM-FACING** — the fix for UAT F2 (CRITICAL) is fork-only: the three rules in `starter-kit/BOOTSTRAP.md` §Without `bin/sync` (`:362-400`, S41's `12463dd`) that stop an agent's prose update from overwriting an adopter's `CHANGELOG.md` and `HANDOFFS.md` are on no upstream tree — *never overwrite* has 0 hits on `upstream/main` and on all four open PR heads. Raised S218; four shapes, none costed. **S224: DISCHARGED — delivery route (a) chosen by the operator and [PR #88](https://github.com/KJ5HST/methodology/pull/88) opened from `fix/bootstrap-never-overwrite-rules` (`a88fce7`); the merge is the maintainer's** | [detail](BACKLOG-DETAIL.md#bl-85) |
| **BL-87** | Nine of the 63 `[detail]` links in this file and [`BACKLOG-COMPLETED.md`](BACKLOG-COMPLETED.md) resolve to nothing: nine item bodies in [`BACKLOG-DETAIL.md`](BACKLOG-DETAIL.md) were appended without their `<a id>` separator line — **BL-47, BL-48, BL-49, BL-59, BL-60, BL-64, BL-65, BL-67, BL-73**, seven open and two closed, measured at `HEAD` (63 bodies, 54 anchors). Every body is present; only the separator is missing, so the body reads as part of the record above it — and that file's front matter says those anchors **are** the record separators its proof splits on, so C2's spans depend on them. Green today only because all nine sit after bodies outside its frozen 18. **Recorded, not fixed (FM #17):** found while fixing BL-86, and the obvious check is RED on arrival. Three shapes, none costed | [detail](BACKLOG-DETAIL.md#bl-87) |
| **BL-88** | Two shipped tools decide a file's read-cap class by two different mechanisms — the trimmer DERIVES it from `LEDGERS`, the dashboard DECLARES it — and the only coupling is a canonical-only test, so an adopter's widened `LEDGERS` is invisible. **DECIDED at S227**; **P1 SHIPPED at S229** (`cb9b0ed`) and **P2 at S230** (`161181c`, `DASHBOARD_VERSION` 2.19.0), both fork-side, no PR granted ([plan](dashboard-read-cap-class-adopter-drift-plan.md)); **P4, the upstream PR, has no target** — `upstream/main`'s dashboard (2.11.1) has none of the read-cap class rows either part changes; **S231 planned the route** ([`dashboard-upstream-routing-plan.md`](dashboard-upstream-routing-plan.md), awaiting ratification): BL-88 rides the read-cap/trim stack's PR, which is that plan's P2/P3 | [detail](BACKLOG-DETAIL.md#bl-88) |
| **BL-89** | `bin/check-handoff` validates the newest receipt's SCHEMA, not the ledger's RECORD STRUCTURE: it passed three differently-broken `HANDOFFS.md` trees in three consecutive sessions — a receipt spliced into the front matter's own code example, and a duplicated `session:` number twice. Adjacent to **BL-73**; canonical-only. Raised S229 at the operator's request; nothing costed | [detail](BACKLOG-DETAIL.md#bl-89) |
| **BL-90** | `methodology_dashboard.py --sync` **overwrites a copy's local `EXCLUDE_DIRS`** — the edit point its own CUSTOMIZATION section invites — with no warning, and 2.19.0's stale-copy warning now prints that `--sync` to every older copy. The portfolio copy carries 13 names, seven of them local additions (synced by hand at S230 with them re-applied). Raised S230 after close-out; nothing costed | [detail](BACKLOG-DETAIL.md#bl-90) |
| **BL-91** | **PLANNED at S232 — [`overhead-ratchet-plan.md`](overhead-ratchet-plan.md); D1 RATIFIED at S233 as (a), shape A: *report better, gate nothing*.** The plan's recommended (b) — one canonical-only `max` gate on the read-set class total — was **declined**, so §7's P2 is out of scope and **nothing here refuses a growth**; (c) distributed enforcement was declined a second time and standing decision S3 stays closed. **What survives is P1, the printer** (S233's deliverable): canonical-only `bin/check-overhead`, read-set total in bytes and tokens, write-free. The instrument was never missing: `context_budget.py --precommit` exists, works, and is unwired, and hook enforcement was DECLINED by the operator at S206 (BL-78 P3) — read §1 before re-proposing anything. The per-session mandated read has risen **4.6x across 27 releases** (17,615 B at v1.0.0 -> 80,526 B at v3.7, never once falling; HEAD 72,535 B after the apparatus extraction), and no gate watches it: the quality ratchet only tightens, and the context budget's ceiling is a reported series by the S202 decision. A planning session decides whether overhead becomes a gated metric, what a release that raises it must state, and how BL-60 folds in | [detail](BACKLOG-DETAIL.md#bl-91) |
| **BL-92** | `bin/tests.sh` read **360 passed / 1 failed** inside one `quality_ratchet.py --run` at `5d6fbe4` while four other runs at the same commit read **361 / 0** — and **the failing assertion is unrecoverable**, because the ratchet keeps only each gate's extracted number, not its output. The suspect is Test 44's whole-tree `git status --porcelain` comparison (`bin/tests.sh:3595`), the suite's only assertion over the live repository's entire state and therefore the only one unrelated churn can red; it is a suspect, not a diagnosis — the four re-runs include the exact invocation that failed. Raised S233 from its own close-out; three shapes, none costed | [detail](BACKLOG-DETAIL.md#bl-92) |
| **BL-93** | The hand-maintained **Open:** list at the top of this file (`:8`) omits **five** open items — **BL-63, BL-88, BL-89, BL-90, BL-91** — while the index table below it carries 57 rows to the list's 52. This is [fork Learning #81](../FORK_LEARNINGS.md) (*a population recorded as a LIST decays*) occurring in the file whose own next sentence says *"Re-derive rather than trust that list — it is hand-maintained, and it has been wrong before"* and prints the grep to do it. Found at S234 while removing BL-69 from that list; the derivation is `re.findall(r'^\| \*\*(BL-\d+)\*\* \|')` over the index table minus the prose list. **Not fixed — the decision is whether to repair the list or replace it with the derivation**, which is #81's own remedy and would end the class rather than the instance. BL-20 appearing in both the index and `BACKLOG-COMPLETED.md` is its documented *residual only* split, not a defect | [detail](BACKLOG-DETAIL.md#bl-93) |
| **BL-94** | **A planning session is owed for an experiment on documentation quality and management, v3.8 against v3.0.** Asked for by the operator on 2026-10-01 (S244): *"Let's plan an additional experiment to look at documentation quality and management in another session."* Nothing is built or run. Known so far: the existing studies cannot answer it (S237's process-presence score was at ceiling for both versions), and a free tally of the 15 T-remove trees at S244 found the same footprint in every arm. **S255 wrote the plan:** [`documentation-quality-experiment-plan.md`](documentation-quality-experiment-plan.md) (DRAFT, two independent reviews recorded in its §11; **D1-D5 ratified by the operator 2026-10-03**: Q2, start state `879503cce`, arms v3.0 + v3.7 + v3.8-text, **a $100 cap for this study with the earlier caps ignored**, and he does the blind rating himself; D6 and D7 stay open; **P1a ($0) starts when he says go in a session**). **S256 did P1a** (the 41 saved runs kept as one verified bundle; `doc_score.py` built, calibrated on T-remove and frozen; $0). **S257 did P1b** (the frozen scorer run once over the saved v3.0, v3.7 and v3.8-text runs, $0; a null at the ceiling on M1 and M2(a), report [`P1B_REPORT.md`](overhead-replay/pilot/doc-evidence/P1B_REPORT.md)): **S258 did P2a** ($0, builds the probe: `probe.py` tested against a fake `claude` and run `--no-launch` over all 41 saved runs, a probe measured at about $0.35 not $1, the blind rater and a six-record packet for him; report [`P2A_REPORT.md`](overhead-replay/pilot/doc-evidence/P2A_REPORT.md)): **S259 did P2** ($2.4781 of the $10 cap: a probe about $0.19, a rating call about $0.055; 36 claims checked in the four cold reports, none wrong; the model rater scored every honest record 8 of 8 and missed the `vague` defect; report [`P2_REPORT.md`](overhead-replay/pilot/doc-evidence/P2_REPORT.md)): the next phase is **P3**, its own go (about $9 to $11 restated, against $38), and the report says cost is not the open question: D6/D7 come first (**S260 fixed the four harness defects at $0**: probe reads and leftover clone, the rater's raw text, and the `missing` and `vague` planted defects with a $0 evidence check; the rater has not been re-run on them). Detail in [`BACKLOG-DETAIL.md`](BACKLOG-DETAIL.md) §BL-94. |
| **BL-95** | **Upstream moved while this fork was away: #83-#88 MERGED 2026-10-01 20:19 UTC, tags v4.0 and v4.1, `upstream/main` `16805399` (re-verified S246 Phase 0).** Fork `main` is 89 commits behind and 1,263 ahead of it; #91 (`feat/sync-manifest-at-ref`) is open with 0 reviews. Memory and CLAUDE.md still say v3.7 and "#83-#88 open". **A resync needs its own plan, commissioned by the operator** (the S177 resync is the precedent: read `project_upstream_resync_2026_09_plan`); the two session sequences collide (see `HANDOFFS.md` front matter). Operator deferred it at the S246 Phase 0 picker; recorded, not started. Outward-facing steps need a go-ahead each time. |
| **BL-96** | **`bin/tests.sh` Test 9's skip is not counted: with no `gh` the suite prints `0 skipped` and a green summary although the GitHub-source route never ran.** Its `else` is a bare `echo "  SKIP: gh unauthenticated"` (`bin/tests.sh:141`), not `skip()` (`:20`), the helper that feeds the count the Summary prints and that the other 17 skips use. Upstream (`1680539`) has the same bare echo and no counter at all; its `--source=github` clones with git and its Test 9 guards on `git ls-remote`, where this checkout's `bin/sync` and `bin/status` call `gh api` and stop with `gh CLI not found` without it. Raised S248 from the operator's question what happens with no `gh`; **recorded, not fixed.** The decision is count it, gate it, or leave it, made with the BL-95 resync in view because that replaces the guard. Detail in [`BACKLOG-DETAIL.md`](BACKLOG-DETAIL.md) §BL-96. |
| **BL-97** | **`echo "$(…)" \| grep -q` under `bin/tests.sh`'s `pipefail` fails about 0.3% of runs at a 1.5 KB output, far below the 65,536 B pipe capacity that BL-43's criterion rests on; one such assertion (Test 38, `bin/tests.sh:2573`) read FAIL in S254's full suite with the matching text in its own re-run.** Measured on a synthetic 1,540 B string with the match on line 2: 10 failures in 3,000 runs of the `echo` form, 0 in 3,000 of the here-string form (bash 5.2.37, macOS). 82 lines of `bin/tests.sh` have the form; BL-43 / Test 42 gate only the producers that read the real repository, and Test 38's producer reads a fixture. **Recorded, not fixed;** the mechanism is not established. Detail in [`BACKLOG-DETAIL.md`](BACKLOG-DETAIL.md) §BL-97. |

## Completed items — moved to [`BACKLOG-COMPLETED.md`](BACKLOG-COMPLETED.md)

**Every closed item's pointer row lives in [`BACKLOG-COMPLETED.md`](BACKLOG-COMPLETED.md)** — the 33 that
moved out of this file at `a32f520`, plus every item closed since, one row each. It is the read-on-demand
sibling this file gained at S223, for the reason §Open items' bodies moved to
[`BACKLOG-DETAIL.md`](BACKLOG-DETAIL.md) at S99: the closed rows were **25,276 B, 43% of a file Phase 0 reads
at every session**, and they are the half no session needs to run. Losslessness is proved by
[`BACKLOG-COMPLETED.md.verify.sh`](BACKLOG-COMPLETED.md.verify.sh) — run it rather than trusting this sentence.
**Since S226 that proof pins the 33 that moved and REPORTS the later closures** rather than refusing them, which
is what a destination needs and a move proof alone would not give (BL-86); its C6 asserts every later closure's
id is still in the block below.

**The ids stay here on purpose, so a closed item is still findable from the file Phase 0 reads.**
That is what [`BACKLOG-archive-2026-08-15.md.verify.sh`](BACKLOG-archive-2026-08-15.md.verify.sh)'s
C4 asserts, and its comment names the case it was written for: *"BL-27 is the named case: S88 needed
it and could not find it even while it was in the live file."* Re-derive the list rather than trust
it — `grep -cE '^\| \*\*BL-[0-9]+\*\* \|' docs/planning/BACKLOG-COMPLETED.md`:

**BL-1**, **BL-2**, **BL-3**, **BL-4**, **BL-5**, **BL-6**, **BL-7**, **BL-8**, **BL-9**, **BL-10**, **BL-15**, **BL-20**, **BL-24**, **BL-25**, **BL-27**, **BL-28**, **BL-29**, **BL-33**, **BL-34**, **BL-35**, **BL-38**, **BL-40**, **BL-41**, **BL-43**, **BL-45**, **BL-53**, **BL-56**, **BL-59**, **BL-67**, **BL-69**, **BL-72**, **BL-76**, **BL-78**, **BL-82**, **BL-83**, **BL-86**

**The heading this block replaces named 19 of the 33.** BL-8, BL-15, BL-20, BL-24, BL-25, BL-27,
BL-28, BL-29, BL-33, BL-34, BL-35, BL-38, BL-40 and BL-41 were in the table and missing from its
own id list — this file's *"do not trust a number in this file"* warning applying to its own
section headings. The count and list above are derived, not transcribed.

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
