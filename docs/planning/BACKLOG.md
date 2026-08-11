# Operational Backlog (fork-only)

> **STATUS: REOPENED 2026-07-25 — BL-8, BL-11, BL-12, BL-13, BL-14, BL-16, BL-17, BL-18, BL-19,
> BL-20, BL-21, BL-22, BL-23, BL-26 and BL-30 are open** (**BL-29 and BL-30 raised 2026-08-10
> (S70)**, operator-directed, out of a cross-repo investigation into whether adopting the methodology
> produced measurable effects in local adopter repos — **BL-29** a still-reproducible self-scan gap in
> `tools/methodology_dashboard.py`, **BL-30** a deliberately lightweight watch item on the ledger
> trimmer's adoption outside `nprcgenekeepr`; see their own entries. **BL-29 raised 2026-08-10 (S70),
> CLOSED 2026-08-10 (S72)** — `ROOT = Path(__file__).parent` is the script's own directory, correct
> for every adopter-installed and portfolio-root copy, but the canonical repo's own two checked-in
> copies (`tools/`, `starter-kit/`) file the script one level BELOW the repo they belong to, so
> `(ROOT / ".git").exists()` read false there; a new `resolve_single_project_root()` bridges exactly
> those two known, marker-verified nestings to their repo root, `DASHBOARD_VERSION` 2.14.0 → 2.15.0,
> 6 new RED-first tests (290/290 in the dashboard suite), full `bin/tests.sh` 185/186 (Test 9's
> pre-existing baseline) unaffected; see its own entry. **BL-28 raised 2026-08-10 (S65), CLOSED 2026-08-10
> (S68)** — the generated `.verify.sh`'s "missing front-matter line" check was a substring test, not
> exact-line-set membership, so an append-style edit that kept the original text as a literal
> substring of the new line was invisible to it; fixed by comparing against the exact set of new
> front-matter lines, `TRIM_VERSION` 1.1.2 → 1.1.3, 2 new RED-first tests (97/97); see its own entry.
> **BL-27 raised 2026-08-10 (S64), CLOSED 2026-08-10 (S65)** — the
> ledger trimmer's generated `.verify.sh` had two known false-positive triggers on `HANDOFFS.md`
> (front-matter field regeneration; a same-commit close-out bundled with the archive write reading as
> record alteration); both fixed in `VERIFY_TEMPLATE`/`build_verify` (`starter-kit/methodology_trim.py`
> v1.1.2), RED-first, 4 new tests (95/95), full suite unaffected; see its own entry for the fix shape.
> **BL-26 raised 2026-08-09 (S56)** — issue #67
> describes a live, unfixed defect already shipped in this fork's own `methodology_dashboard.py`;
> PR #66 has two concrete, reproduced collisions of its own (a hook-install path that silently
> no-ops under this fork's `core.hooksPath` convention, and a duplicate-session check with the exact
> flaw BL-23 already found in issue #65); see its own entry and
> [`issue67-pr66-review.md`](issue67-pr66-review.md). **BL-25 raised and CLOSED same session (S53)** — the
> `vscode_quarto_ext` counterpart to BL-24: F9 confirmed resolved, F2/F3/F6/F8 unchanged/open,
> F10/F11 unchanged-and-clean, both bonus checks (F1, F4) clean; see its own entry and
> [`uat-2026-08-08-followup.md`](uat-2026-08-08-followup.md) §9. **BL-24 raised 2026-08-08 (S49), CLOSED same day (S50)**
> — the focused `mts-system` re-run it queued ran: F9 confirmed resolved, F10 improved to zero, F6/F7
> unchanged/open, F11 not applicable; see its own entry and
> [`uat-2026-08-08-followup.md`](uat-2026-08-08-followup.md) §8. **BL-23 raised 2026-08-08 (S47)** — issue #65 collides
> with S34's unopened Learnings-table PR; see its own entry and
> [`issue-65-collision-review.md`](issue-65-collision-review.md). **BL-22 raised 2026-08-03 (S36)**,
> and this enumeration WAS updated with it — the omission called out below for BL-20 is the reason it
> was checked;
> **BL-21 raised 2026-08-03 (S32)**; **BL-20 was raised 2026-08-02
> (S31) and this enumeration was not updated with it**, which is why it is being said out loud: this
> list is a hand-maintained derived value in the file whose own header tells you not to trust those.
> It cannot be derived by counting headings either — the 16 `**BL-N —**` headings in §Open items
> (re-derived 2026-08-09, S56, via `grep -cE '^\*\*BL-[0-9]+ —' docs/planning/BACKLOG.md`; **15** at
> S53's count, itself already stale by then — this line is exactly the kind of drift the
> paragraph warns about, caught only because S56 added a sixteenth heading, BL-26, and re-ran the
> grep rather than incrementing by hand) are a *different* set: **BL-15** keeps its
> heading though it is CLOSED, and **BL-16** is open but has no heading of its own, living inside
> BL-14's follow-ons paragraph. Read each item's own status line.) (**BL-19 raised 2026-08-02 (S30)** — the operator-assigned context-cost plan; it is an
> index entry for [`framework-context-cost-plan.md`](framework-context-cost-plan.md), not a restatement
> of it. **S30 also re-measured every open item above and found a wrong number in six of six**; the
> corrections are recorded in the `CHANGELOG.md` entry *"The framework's context cost — adopter
> heuristics and a remediation plan"* and the items themselves are deliberately NOT edited (FM #17).
> Do not trust a number in this file without re-deriving it — in particular the live-voice "32
> receipts" (it is 33), BL-18's "30 anchors" (28) and its "cannot be repaired without fabricating a
> citation" (false), BL-12's "four sites" (five), and BL-16's `bin/check-handoff:301-303` (it is
> `:487`, and was never `:301-303` at any tree that ever existed).) (BL-14 raised 2026-08-02 (S28) and **partially closed the same session**: the fork-side
> detector and the 9-receipt repair shipped; its distributed half — the spec still promises a
> reconcile no procedure assigns — is prepared, unshipped, and needs a go-ahead (see the routing
> paragraph; it was recorded as "blocked on the channel" until 2026-08-03, on a constraint nobody
> imposed). **BL-15 is CLOSED 2026-08-02 (S29):
> raised correctly — its "13 of 32" is exact — and already discharged by BL-14's own repair, which
> gave all 13 receipts a real sha in `commit:` to defer to. S29's claim stub said the population
> did not reproduce; that was wrong, and the correction is recorded in BL-15 itself. Settling it
> uncovered a different defect, and the fork-side prohibition for that shipped the same session.
> BL-17 and BL-18 were raised out of the settlement and are open.**) BL-8 was deliberately
> sequenced *after* the dashboard signal-integrity campaign closed (Layer 7, then Layer 6), which it
> now has (v3.6 shipped 2026-07-27), so it is unblocked. BL-11 and BL-12 were both raised 2026-08-01
> at BL-10's close-out. BL-1 – BL-7, BL-9 and BL-10 are complete; the retirement note below is
> preserved as the record of that cycle. **BL-9 closed 2026-08-01 (S25)** — all three layers
> delivered across S23/S24/S25.
>
> **RECONCILED 2026-08-01 (S26) against `upstream/main` `e02538b`, and three items moved.** The
> maintainer ran their own S7/S8 the same evening, and the fork resynced (`d6dd6c9` → `e02538b`):
> — **BL-10's prose fix was superseded upstream.** `15ccb38` re-grounded the identical five
> `Learning #N` citations in the identical two distributed files, from the identical rad-con root
> cause. The fork's parked branch is now of historical interest only; see the parked block below,
> which has been rewritten rather than deleted.
> — **BL-12's second bullet became upstream [issue #65](https://github.com/KJ5HST/methodology/issues/65)**,
> filed by the maintainer (`f85a324`), open, and scoped almost exactly as BL-12 framed it —
> mutation-proved, with Learning #12's RED-first precondition carried over verbatim.
> — **BL-13 is new**, and it exists *because* of `15ccb38`: that fix stripped the dangling numbers
> but left one of the claims they were attributing standing on its own. BL-10's own session predicted
> this failure in writing.

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

## Open items

**BL-8** was sequenced AFTER the dashboard signal-integrity campaign closed — i.e. after **Layer 7**
(the installer/doc-only fix, ratified S14) and then **Layer 6** (close-out + release decision R1).
That campaign shipped as **v3.6** on 2026-07-27, so it is not blocked any longer. It is not a change
to the methodology. It was raised and measured in **S14** (as was BL-9, now complete); see the action
ledger for those entries. **BL-11** and **BL-12** are unrelated to the campaign; both were raised
2026-08-01 at BL-10's close-out. **BL-13** was raised 2026-08-01 at the S26 resync.

**RE-TRIAGED 2026-08-03 (S33) — the routing that decides what a session can run today, corrected.**
Until this date several items below carried *"blocked on the paused channel"* as their **disposition**.
**That constraint was never imposed** (see `framework-context-cost-plan.md` §5): the operator's rule
is *ask before each outward-facing action, batch and vet to protect the maintainer's review time* —
sequence, not suspension. Nothing here is blocked for that reason. The honest routing:

- **Runnable now, nothing outward-facing.** **BL-8** — a fork-side operational decision where
  *"decline"* is an explicitly correct outcome. **BL-18** — S30 proved its stated blocker false.
  **BL-20** — two of its three fixes are fork-side.
- **Runnable now up to the PR, which needs a go-ahead.** **BL-13**, **BL-12's first bullet**,
  **BL-14's distributed half**, **BL-17's distributed half**, **BL-21**. Each touches a
  `bin/_manifest.py`-**DISTRIBUTED** file, so the *fix* lands upstream — but the preparation and the
  evidence are fork-side and are the part that carries the work. Batch them rather than sending each
  alone; that is what the operator's rule is protecting.
- **Genuinely not advanceable by a session, and the only one.** **BL-11** — its deliverable is *a
  maintainer decision*, not an edit. No amount of fork-side work produces it. This is what a real
  block looks like, and it is worth contrasting with the five above that were mislabelled as one.
- **Not the fork's to raise.** **BL-12's second bullet** is upstream [issue #65](https://github.com/KJ5HST/methodology/issues/65);
  answering it is an outward-facing action and needs an explicit ask.

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

> **S34 regression note (2026-08-03), recorded not fixed.** The parked `bin/check-citations`
> (branch `docs/bl-10-dangling-learning-citations`, tag `archive/bl-10-citations` → `268f1e5`) is
> hard-anchored on `REGISTRY_FILE = "starter-kit/SESSION_RUNNER.md"` (`:34`) and
> `REGISTRY_HEADING = "## Learnings (added by sessions)"` (`:35`). It exits 0 against `816984b` and
> aborts `GUARD FAIL — the Learnings table parsed to zero rows` (exit 2) against the post-S34 tree,
> because the table now lives in `starter-kit/FRAMEWORK_LEARNINGS.md` under `# Framework Learnings`.
> **Whoever revives it — S43 absorbs it into `bin/check-derived` — must retarget both constants.**
> The guard failing loudly rather than silently passing is the tool behaving correctly.

**BL-11 — Unreachable non-`Learning` referents across the distributed corpus.**
*Raised 2026-08-01 at BL-10's close-out; deliberately not bundled into it (FM #17/#18).*
**Re-verified line-by-line at the S26 resync against `e02538b`: every site below still stands.**
Upstream `15ccb38` fixed the `Learning #N` class only, and none of these are that class, so the item
is untouched by it — the row numbers below are the post-resync ones.
BL-10 closed the `Learning #N` case (upstream `15ccb38`; the fork's parked `bin/check-citations`
would have mechanized it). The same class survives in referents that no such checker can model,
because they are prose provenance rather than a relation between two enumerable sets:
- `starter-kit/FRAMEWORK_LEARNINGS.md` Learnings **Source** column, four rows — #8 (`:25`, `escape #8` /
  `S7`), #9 (`:26`, the deictic "this session"), #11 (`:28`, `HANDOFFS.md` session `S1`, `BL-7`),
  #12 (`:29`, `S9–S16`, `Layer 1`/`Layer 7`). *(Line anchors re-derived by S34 on 2026-08-03, when
  the table moved out of `starter-kit/SESSION_RUNNER.md`, where they read `:375`/`:376`/`:378`/`:379`.)* All fork-only vocabulary with no referent in
  `upstream/main`. **Note the S7 collision this backlog itself can now cause:** upstream has since
  run its own S7 and S8, so "S7" in that Source column resolves to *neither* session unambiguously —
  the token got worse without anyone editing it.
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
*The maintainer's own stated value now supports this item:* `f85a324` deliberately cited **no SHA**
for a real incident because both SHAs lived on an unpushed branch, reasoning that *"an unreachable
reference is precisely the trap Learning #13 was just added to prevent."* BL-11 is that same
principle applied to references already shipped to adopters. Worth quoting when the decision is put.

**BL-12 — Two verified corpus defects found during BL-10's sweep, out of its declared scope.**
*Raised 2026-08-01; both measured, neither fixed (FM #17). Both re-measured at the S26 resync, and
the first one grew.*
- **The `"19 anti-patterns"` count claim — FOUR live sites.** The list enumerates **20** (#20
  appended in v2.5; the size claim was never recounted), and the workstream file self-contradicts at
  `:306` — *"Anti-patterns #9, #10, #11 … The remaining 17"* = 20. The sites, with their
  dispositions, because they differ:
  - `workstreams/RESEARCH_DOCUMENTATION_WORKSTREAM.md:55` — *"The 19 anti-patterns"*.
    `bin/_manifest.py`-**DISTRIBUTED**: adopters have the false claim. Fix needs the channel.
  - `README.md:475` — *"**19 documented anti-patterns**"*. Canonical-only.
  - `README.md:477` — *"the 19 anti-patterns as finding categories"*. Canonical-only.
  - `docs/RELEASE_HISTORY.md:34` — the v2.3 entry, *"19 documented anti-patterns"*. Canonical-only.
  **Treat all four as one fix, on this repo's own precedent:** `ac770fe`
  (*"update v2.3 anti-pattern count 13→19 to match workstream file"*) changed the workstream count,
  **both** README bullets and the `CLAUDE.md` v2.3 entry in a single commit, saying so outright —
  *"Also fixes the README Audit Mode bullet … same drift, same fix."* BL-9 L3 later moved that
  `CLAUDE.md` entry to `docs/RELEASE_HISTORY.md:34`, so the fourth site is the same site `ac770fe`
  already maintained once; the frozen-dated-entry convention does not shield it, because `ac770fe`
  established it is maintained prose that tracks the workstream file.
  *This bullet has now been miscounted twice — "one site" when raised, "two" at the S26 resync — both
  times by grepping the literal string `"19 anti-patterns"` and missing `"19 documented
  anti-patterns"`. Whoever fixes it: enumerate the list in the file and grep BOTH phrasings
  case-insensitively. Do not trust the 20 or the four above; that is the exact error being fixed.*
- ~~The Learnings table has no shape coverage~~ → **MOVED UPSTREAM. This is now
  [issue #65](https://github.com/KJ5HST/methodology/issues/65)**, filed by the maintainer on
  2026-08-01 (`f85a324`) and OPEN. It supersedes this bullet and is strictly broader: it covers the
  `HANDOFFS.md` receipt ledger as well as the Learnings table, proposes a `--all` mode for
  `bin/check-handoff`, and carries Learning #12's RED-first precondition verbatim. Its evidence is
  mutation-proved at `a4e2b30`, matching what this bullet asserted from upstream's S5 receipt.
  **Answering it is an outward-facing action and needs an explicit ask** — see the PR #64 block
  above. The fork's parked `bin/check-citations` (`268f1e5`) is a partial head start on the
  Learnings-table half only.

**BL-13 — Upstream's own citation fix left an unattributed false claim standing in a distributed
file.** *Raised 2026-08-01 (S26), found while reconciling the resync; measured, not fixed (FM #17).*
`starter-kit/RECOMMENDED_SKILLS.md:94` now reads: *"`/caveman` … Stylistic compression; **the
methodology's own handoff length discipline** addresses token reduction without changing voice."*
`15ccb38` removed the dangling `Learning #34` citation and kept the assertion it was attributing.
*Measured at `e02538b`, not inferred:* `"length discipline"` occurs **once** in the entire
distributed corpus — that line — and twice in `docs/audits/2026-05-02-mattpocock-skills-evaluation.md`,
which is canonical-only and correctly attributes the rule to **rad-con**. So the claim survives with
no referent anywhere an adopter can reach.
*It is not merely unsupported; the corpus says the opposite.* Failure mode **#15** is *"Minimal
handoff"* (`starter-kit/SESSION_RUNNER.md:317`), the Phase 3D tripwire table flags *"Handoff is
<5 lines"* (`:339`), and `ITERATIVE_METHODOLOGY.md:509` lists *"the handoff gets a little shorter"*
as **erosion**. A reader told to compress handoffs is being pointed across a gate.
*Why this is BL-10's lesson and not a new one:* that session wrote, before any of this happened, that
three of the five citations were **worse than dangling** — they asserted framework rules that do not
exist — and that stripping just the numbers *"would have left unattributed false claims."* This is
that prediction landing. The fork's parked `1eac7a4` re-grounded this same row on FM #15 and the six
Minimum Handoff Requirements, and stated outright that there is no length rule to trade against.
*Scope:* one distributed file, one table cell. **DISTRIBUTED**, so the fix lands upstream and the PR
needs a go-ahead — but the evidence package is fork-side work and is the part that matters. `/zoom-out` on the same line
is a weaker sibling: upstream's replacement is *true but unlocated* (it describes a structured
architecture survey and points at nothing), where `1eac7a4` cited
`INHERITED_CODEBASE_FAMILIARIZATION_CAMPAIGN.md` §Sub-Agent Dispatch Pattern. Not false; note it,
do not bundle it.

**BL-14 — The `commit:` answer slot: a distributed promise with no owner and no detector.**
*Raised and PARTIALLY CLOSED 2026-08-02 (S28). The fork-side half shipped; the distributed half is
prepared and awaiting a go-ahead — recorded as "blocked on the channel" until the 2026-08-03
re-triage.* Nominated by S27's `next_steps` as a pre-existing escape it
declined to bundle (FM #17).
**The defect.** `commit:` may legitimately read `pending` when written — a close-out receipt ships
inside the very commit whose sha it would name, the chicken-egg the ratified plan solved by
deferring. The distributed spec then promises a collector: `starter-kit/HANDOFFS.md:64`
(*"`pending` until the next session reconciles it"*) and `:78-79` (*"the next session reconciles
them to real shas"*), ratified at
[`close-out-receipt-durable-artifact-plan.md:87`](close-out-receipt-durable-artifact-plan.md).
**No procedure ever assigned it.** `starter-kit/SESSION_RUNNER.md` Phase 0 step 6 reconciles
undocumented commits, a `CHANGELOG: pending` marker, and a missing-or-`status: pending` receipt —
and says nothing about a `status: complete` receipt whose `commit:` is still `pending`. Nothing
detected it either: `bin/check-handoff` read only `blocks[0]`, and `pending` is not in
`BARE_PLACEHOLDERS`.
*Measured over both ledger files with the checker's own parser, never grep:* **9 of 32 receipts
named no sha in the answer slot** — 7 literal `pending` (S27, S22, S21, S20, S19, S18, S6) plus
S26 and S25 reading `this commit — …`, **S25 containing no sha anywhere**. The oldest, S6, had
stood **25 days**.
*The base rate corrects the folk history:* the successor-reconcile has fired **6 times, only 4 of
them deliberately**, all inside one 8-hour window on 2026-07-25 — one operator, by hand. (`7817989`
is not a seventh: it is S3 completing its **own** receipt 2m26s later.) It was never a procedure.
*This is [Learning #9](../../starter-kit/FRAMEWORK_LEARNINGS.md)'s own remedy — gate-on-write AND
reconcile-on-read, neither dependable alone — unapplied to the one sentinel-bearing key that needed
both.* Two archived receipts had already **docked their successors points** for exactly this
(`docs/archive/HANDOFFS-archive.md:569`, `:632`) without anyone fixing it.
**SHIPPED (fork-local, canonical-only, no channel):** the ledger repair of all 9 (`7752114`), plus
the **answer-slot rule** in `bin/check-handoff` — every receipt *except the newest* must have a sha
as its `commit:` value's **first token**. The newest is exempt **positionally, not by value**, so
the chicken-egg cannot return. Test 25 (13 assertions incl. a live-corpus assertion against the real
ledger) + `--archived`. **8 mutants, 8 killed.**
**STILL OPEN, and it is the half that matters — DISTRIBUTED, needs the channel.** The spec still
promises a reconcile that no procedure assigns. The fix is one of two forks, and *choosing between
them is the deliverable*, not the edit: **(A) schedule it** — add the `commit:` case to
`SESSION_RUNNER.md` Phase 0 step 6; or **(B) delete the promise** — drop "the next session
reconciles it" from `starter-kit/HANDOFFS.md:64`/`:78-79` and let the state predicate stand alone.
The shipped detector is **agnostic between them** and correct under either, which is why it could
ship first. Seven distributed sites currently scope "reconcile" to `status: pending` only:
`starter-kit/SESSION_RUNNER.md:18`, `:44`, `:343`; `starter-kit/FRAMEWORK_LEARNINGS.md:26`;
`ITERATIVE_METHODOLOGY.md:148`; `starter-kit/SAFEGUARDS.md:179`; `starter-kit/BOOTSTRAP.md:324`.
*(Re-derived by S34 on 2026-08-03 — `git grep -n 'status: pending' -- <the DISTRIBUTION sources>`.
The seventh site was `SESSION_RUNNER.md:376`, which is now Learning #9 in the extracted
`FRAMEWORK_LEARNINGS.md`; `BOOTSTRAP.md` shifted `:322`→`:324`. The count stays **seven** only
because `FRAMEWORK_LEARNINGS.md` is itself distributed.)* Per **Learning #8**, a fix must
reach every checklist that restates close-out, not just the canonical phase text.
**Upstream note, disclosed not absorbed.** `bin/check-handoff` is canonical-only but **not
fork-only**; it now diverges from `upstream/main` by S27's stub schema *and* this. Upstream
[issue #65](https://github.com/KJ5HST/methodology/issues/65) separately asks for an `--all` mode
over *different* ground. This is not that, is named nothing like it, leaves `validate()` on
`blocks[0]` (pinned by Test 25 N6), and **does not answer #65** — answering it remains an
outward-facing action needing an explicit ask. Two facts to hold before anyone does: #65's proposed
*"`session:` values are unique"* invariant is **false at full-ledger scope** (32 receipts, 28
distinct numbers — S3/S5/S7/S8 each collide across the two sequences), and its scope omits the
archive.
**Upstream's copy of S6 is upstream's to fix.** `upstream/main` still carries that receipt as
`session: S2, commit: pending`; the fork reconciled its own renumbered copy to `21fb521`, the only
sha that is an ancestor of *both* repos. No upstream action taken.
*Follow-ons raised, deliberately not bundled (FM #17):* **BL-15** — `changelog_ref` carries the
identical escape in 13 of 32 receipts, but its false-positive surface is wider (a legitimately
pending PR number is plausible). **BL-16** — `bin/check-handoff:301-303`'s docstring claims the
canonical repo "has no root-level receipt ledger of its own," which is false here (13 receipts + a
19-receipt archive it knows nothing about).

**BL-15 — `changelog_ref`'s deictic deferral: RAISED CORRECTLY, AND ALREADY DISCHARGED.**
*Settled 2026-08-02 (S29). Do not re-raise; the count below is the third time this population has
been measured and the first time it was measured right.*
**BL-15's "13 of 32" is exact.** 13 `changelog_ref` values defer deictically instead of naming an
identifier — **12 × `this commit` plus archive-S1's `this branch`**. S29's claim stub asserted the
population did not reproduce under any predicate; that assertion was **wrong**, and wrong the way
[`feedback_a_grep_count_is_a_sample`] describes: it grepped one literal phrasing, reached 12, and
stopped one variant short. `bin/check-handoff:69-70` names the dialect in writing —
*"it catches the `this commit — ...` dialect that names no sha at all"* — so the key was documented
and was not used. The provenance settles the "identical" wording too, and it is textual rather than
analogy: `starter-kit/HANDOFFS.md:63` specifies `changelog_ref: <PR #N or a short-sha into
CHANGELOG.md>` and `:88` says outright *"the shared key across all three is the commit sha
(`changelog_ref` / `commit` here)"*; the ratified plan agrees at
[`close-out-receipt-durable-artifact-plan.md:105`](close-out-receipt-durable-artifact-plan.md).
**Why it is nonetheless closed rather than open.** Two measured facts, neither of which was
available when BL-15 was raised one session earlier:
- **All 13 name their entry by a quoted `### ` title BEFORE the deferral** — "…entry, this commit".
  The deferral is a trailing modifier, never the answer slot. BL-14's escape was categorical: S25
  and S26's `commit:` read `this commit` **and nothing else, with no sha anywhere in the receipt**.
- **All 13 now carry a real sha as their own `commit:` first token**, because `7752114` and
  `6d47624` forced it. Each deictic reference is therefore a one-hop back-reference to a field the
  checker already guarantees. **BL-14 discharged BL-15 as a side effect** — which is the honest
  finding, and better than either "wrong" or "open".
*What no longer stands:* the parenthetical about a *"legitimately pending PR number"*. Zero of the
32 values contain the literal `pending`, and the seed's `PR #N` form appears in **no** receipt —
only in `bin/tests.sh` fixtures. Nothing in the corpus can produce that false positive.
*Residual, deliberately not mechanized:* the one-hop resolution is a convention no document states.
Writing it down means editing `starter-kit/HANDOFFS.md`, which is **DISTRIBUTED** — see BL-17.

**BL-17 — The `changelog_ref` referent the seed does not offer, and the one title that is stale.**
*Raised 2026-08-02 (S29) out of BL-15's settlement; measured, not fixed (FM #17).*
Two halves that share one root cause: **the distributed spec offers no locator a fork-local session
can actually write.** `starter-kit/HANDOFFS.md:63` gives `PR #N` (there is often no PR) and a
short-sha (unknowable while the receipt is being written). **0 of 32 receipts use either.** All 32
invented the same third form — `CHANGELOG.md "<its ### heading>"` — and eight then reached for a
line number on top. *That vacuum is why the anchors existed*, so the shipped prohibition treats the
symptom and this item is the cause.
- **The DISTRIBUTED half — prepared here, shipped upstream, needs a go-ahead.** Bless the quoted `### ` heading as a
  third locator form at `starter-kit/HANDOFFS.md:63`, and state that a line number is not a locator
  into a ledger. Per **Learning #8** a fix must reach every checklist restating close-out.
- **The fork-side half, unblocked but deliberately deferred.** Stale quoted titles are the failure
  mode the shipped rule cannot see. Measured over 32 receipts: **22 resolve byte-exact, 9 more after
  folding markup only (backticks, `**bold**`, `--`/`—`, and — declare it, S29 did not at first — an
  ASCII `->` against a `→`), and 1 resolved nowhere**: root-S22, whose entry `de46858` retitled **23
  minutes** after the receipt was written, to correct a false claim, while rewriting four other
  fields of that same receipt and leaving `changelog_ref` alone. S22 is repaired in `7c8284e` as a
  disclosed judgement call; the *class* is untouched. **Do not mechanize this as a resolution check
  without reading why it was rejected** (`bin/check-handoff`, THE LOCATOR-FORM RULE): a checker that
  asserts every title resolves goes red whenever someone legitimately retitles an entry — and this
  repo retitles entries *to correct false claims*. Four retitle events already exist; of the two
  receipts ever exposed to one, **one broke**. That is a 50% conditional rate on a 25-day-old corpus,
  not a 1-in-32 rate.

**BL-18 — The same line anchors, in `key_files`, where the checker's own schema requires them.**
*Raised 2026-08-02 (S29); measured, not fixed (FM #17). This is the larger half of the defect
BL-15's settlement uncovered, and it was scoped out by operator decision, not by oversight.*
Root-relative live-ledger anchors across **all** receipt keys: **30 in 14 receipts** — **20 in
`key_files`**, 9 in `changelog_ref` (repaired), 1 in `next_steps`. They decay identically; the
`changelog_ref` nine were merely the ones inside the settled question.
*Why it is a genuinely harder item, and not just a bigger one:* `bin/check-handoff`'s
`KEY_FILES_RE` **requires** `key_files` to carry a `path:line` token, so a prohibition and a
requirement meet head-on in one field. Worse, archive-S4's entire `key_files` value is
`CHANGELOG.md:35 (issue #55 ledger entry)` — repairing it means **fabricating a source citation
into a frozen 2026-07-08 archived receipt**, which no measurement can supply. Verified: after
stripping ledger anchors, 13 of the 14 receipts still satisfy `KEY_FILES_RE`; **archive-S4 does
not.**
*Method note for whoever takes it:* judge each anchor at the tree where its value **first appeared**
(walk `git log --all --full-history` with the checker's own parser), never at the tree its `commit:`
names — that field named the wrong tree for 2 of the 8 `changelog_ref` receipts, once because it
leads with a Phase 1B *claim stub*.

**BL-19 — The framework's context cost: adopter heuristics and the design deficiencies behind them.**
*Raised 2026-08-02 (S30). Operator-assigned planning session; the plan shipped, nothing was
implemented.* **The deliverable is [`framework-context-cost-plan.md`](framework-context-cost-plan.md)
— read it rather than this entry, which is an index and deliberately carries no numbers.**
*What it settles:* one of the three expenses is **declined as framed** (coordination residue is a
maintainer cost with no adopter analogue; its true analogue is record growth); a resolution check and
a numbered-set growth gauge are both declined with reasons; five heuristics are specified, two
load-bearing.
*Why it is not just a monitoring proposal:* `starter-kit/SESSION_RUNNER.md:280` already mandates the
countermeasure in prose — *"grep nearby prose for set-size claims that may have drifted"* — and six
of six backlog items still carried a wrong number. That is this corpus's controlled comparison of
MECHANIZED versus DOCUMENTED, and it forecloses "add a sentence" before anyone proposes one.
*The plan's §5 was RE-QUEUED 2026-08-03 (S33) against the operator's three stated goals* — context
tax, **automated** trimming, and user instructions — after its original sequence was found to be
ordered by *what needed no permission*. The two items that serve those goals most directly (extracting
the Learnings table, and the doctrine into the two seeds) had been marked BLOCKED on a constraint
nobody imposed; the extraction is now **first in the queue**. S31 (ledger split) and S32 (the Phase 1B
carve-out in `.githooks/pre-commit`, the hard precondition for the diff-scoped prohibition) are
shipped. **An outward-facing step is not a block — but it is still not authorization:** every PR,
issue, comment, tag or release needs an explicit ask, each time.
*Five open decisions belong to the operator, not to an agent* — plan §7. **Three were taken at S31**
(run S31; state the trigger as a rate; cut at a day seam); §7's own five — the S39 parked branch, the
`CLAUDE.md` version-pointer sink, DVX's `docs/planning/` scope, whether S40 is worth it, and the
archive-trigger form — **remain open except the last, which S31 settled as a rate.**

**BL-20 — `bin/model-report`'s Source 1 is blind to the `**Model:**` form this repo actually writes.**
*Raised 2026-08-02 (S31), found while verifying a claim S31 was about to publish about its own split.
Not fixed in that session (FM #17): the split was the deliverable, and this is a tool/convention
mismatch with at least three defensible fixes.*
**The defect.** `CHANGELOG_MODEL_RE` (`bin/model-report:51`) is `^-\s*\*\*Model:\*\*\s*(.+)$` — the
list form the distributed seed documents (`starter-kit/CHANGELOG.md:42`, `:57`, `:69`). This repo's
live ledger writes the bullet as a bare `**Model:**` at line start, which that regex cannot match. So
`python3 bin/model-report` prints *"(no CHANGELOG.md entries carry a **Model:** bullet)"* against a
file containing nine of them. Source 1 is the **primary, structured** source; it fails silently and
reads as "no data recorded" rather than "not parsed."
**Population, both dialects, frozen at the tree it was measured against** (`74479df`, S31's claim, so
the figure cannot decay): 14 bullets corpus-wide — **9** bare, all in the live `CHANGELOG.md`, and
**5** list-form, all in `docs/archive/CHANGELOG-through-2026-08-01.md`; 0 in the v3.6 shard. It is
already stale at HEAD — S31's own close-out entry made it 10 bare / 15 total, which is the point.
Re-measure, never recall:
`grep -cE '^-?[[:space:]]*\*\*Model:\*\*' CHANGELOG.md docs/archive/CHANGELOG-*.md`
**Drift point, derived not guessed:** `54426cb` (2026-08-01) is the last commit with list-form only;
`1298af7` (2026-08-02) is the first bare-form entry, and every one of the nine entries since has
followed it — a same-day convention change that no check noticed because the only reader is
non-gating and its empty output is indistinguishable from an unrecorded field.
**Consequence of S31's split, recorded because it is counterintuitive:** the split moved 100% of what
Source 1 can parse into the archive. The tool's default invocation is now empty, and its front-matter
note in both ledgers says so.
**Three fixes, and the choice is the deliverable:** (1) widen the regex to accept both dialects —
smallest, but blesses a form the seed does not document; (2) normalize the nine live entries to the
seed's list form — restores the documented convention, but rewrites dated entries, which the v2.7.1
convention forbids; (3) change the seed to document the bare form — **DISTRIBUTED, so it ships
upstream and needs a go-ahead.** Note (1) and (2) are fork-side, so this can advance today either
way.
**Related:** this is the same shape as BL-14/BL-15 — a promise in the seed with no detector — except
here the detector exists and reads the wrong dialect.

**BL-21 — When the Phase 1B carve-out is contributed upstream, two seed sentences must ship with it.**
*Raised 2026-08-03 (S32) by the change that will eventually create the drift. Scoped DOWN from how it
was first written, by an adversarial review that refuted the stronger claim — recorded here because
the refutation is the useful part.*
**Not a live defect, and the distinction is the item.** S32 gave `.githooks/pre-commit` one exemption
(the Phase 1B claim; see that date's ledger entry). Two distributed files state the hook's contract
without it — `starter-kit/SAFEGUARDS.md:167` and `starter-kit/BOOTSTRAP.md:320`, the latter as an
explicit list (*"It never blocks a repo that has no ledger yet, and it skips merges/rebases"*). But
both seeds designate the **canonical reference implementation** by URL
(`SAFEGUARDS.md:171` → `KJ5HST/methodology/blob/main/.githooks/pre-commit`), that file is
byte-identical to `upstream/main`, and `grep -c githooks bin/_manifest.py` is **0** — no adopter
receives the hook through `bin/sync`. The carve-out exists only in this fork, in a canonical-only
file. **So no adopter-reachable sentence is false today**; it becomes false at the moment the hook
is contributed upstream, and not before.
**Two facts that keep this item small.** (1) The exemption list was *already* incomplete at the
hook's birth (`dc8aa76`): neither seed mentions the empty-index exit (`git commit --allow-empty`
passes) or `rebase-apply`/`git am`. These are summary-level docs that point at the implementation,
by design. (2) The divergence direction is **fail-safe** — the seeds describe a *stricter* gate than
the hook enforces, so no adopter instruction breaks; the failure mode is a reader who expects a
refusal and gets a pass.
**Proposed wording, written here so the upstream PR carries it without re-deriving it.** One clause
in each, no restructuring:
- `SAFEGUARDS.md`, appended to the bullet list — *"**One exemption: the Phase 1B claim.** A commit
  staging only `HANDOFFS.md` (`SESSION_NOTES.md` may ride along) whose diff adds a receipt block and
  whose every added `status:` line reads `pending` passes: it is written before any technical work,
  so it has no action to record yet, and Phase 3F records it with the rest of the session. Note the
  width — any other edit inside `HANDOFFS.md` in that same commit rides through with it, and Phase 0
  reconcile-on-read is what reads those."*
- `BOOTSTRAP.md`, extending the existing list — *"…and it skips merges/rebases, and the Phase 1B
  claim commit."*
**Verification when it ships:** `python3 bin/check-links` green; `bin/status` will show both files as
drift for every adopter, so the `bin/status`→`bin/sync` pass is the second half of the work.
**Blocked on the same thing everything distributed is blocked on** — the paused upstream channel —
but note it is blocked *behind* a decision nobody has made yet: whether this hook is contributed at
all. `.githooks/pre-commit` being canonical-only was itself a ratified decision (BL-6 item 3).

**BL-22 — `DOC_ONLY_SOURCE_LOC_MAX = 200`: an unexamined round number, protected by no test, that
decides a user-visible risk verdict in a DISTRIBUTED file.**
Raised 2026-08-03 (S36) while checking whether the new trimmer could ship without perturbing adopter
scoring. Not a defect this session introduced, and deliberately not folded into it (FM #17).

**What it does.** `tools/methodology_dashboard.py:248` (and its byte-identical `starter-kit/` twin).
`detect_doc_only` runs marker-override → **source-LOC cap** → corpus-disjunction; the cap is the
short-circuit at `:1918` — above 200 lines of source, a repo is **not** doc-only, so it keeps the
code-centric `Testing` dimension and can earn a HIGH **"No test infrastructure"** risk. Below it, and
with a doc corpus, the repo is exempted and scored on a render/verification proxy instead. The
constant therefore decides, for every adopter, which of two scoring regimes applies.

**Provenance, traced not assumed.** Introduced by `b2efd76` (2026-07-08, *"feat(dashboard): score
document-only repos fairly (BL-5)"*). The commit message, the `[BL-5]` ledger entry
(`docs/archive/CHANGELOG-through-v3.6.md:1375`) and `dashboard-signal-integrity-plan.md` all state
the cap's **purpose** — *"keeps a mixed tooling repo … from being silently exempted"* — and **none
states where 200 came from.** Two tells that it was chosen rather than measured:

- its sibling `DOC_ONLY_DOC_LOC_MIN` is **also 200**, for an unrelated quantity (doc lines, not
  source lines);
- **no test asserts the value.** The only test that touches it *overrides* it to `4100`
  (`tools/test_methodology_dashboard.py:2252-2255`). Change 200 to anything and the suite stays green.

```sh
git log --oneline -S DOC_ONLY_SOURCE_LOC_MAX -- tools/methodology_dashboard.py   # -> b2efd76 only
grep -rn 'DOC_ONLY_SOURCE_LOC_MAX' tools/test_methodology_dashboard.py           # override, never an assertion
```

**It is already on record as having been wrong once.** The comment above `FRAMEWORK_INSTALLED_SOURCE`
(`tools/methodology_dashboard.py:~450`) documents a real **148-LOC** utility repo that correctly read
`code` and, after `bin/sync`, flipped to `doc-only` and **lost a TRUE "No test infrastructure" risk** —
*"The old source cap had been masking that."* 148 < 200, so the cap alone misclassifies that repo.

**Why it is worth an item rather than a shrug.** This is the class of value the operator's
derived-value work exists to catch — a number that reads as calibrated, is not, sits in an
adopter-distributed file, and drives a risk verdict adopters act on.

**It is NOT load-bearing for queue item S39′, and this paragraph used to say it was.** The original
claim — *"shipping `methodology_trim.py` (1,632 LOC, 8.2× the cap) requires adding it to
`FRAMEWORK_INSTALLED_SOURCE`, and the softness of the threshold is exactly why that exclusion cannot
be skipped in favour of re-tuning the number"* — was right that re-tuning is the wrong move and wrong
about the dependency, in two ways S39′ measured:

- **The tuple entry accomplishes nothing on its own.** With `methodology_trim.py` on the exclusion
  list and no content rule for it, a synced doc fixture still read `doc_only` False, `source_loc`
  1,632 and a HIGH "No test infrastructure" — identical to having never touched the tuple. What does
  the work is `is_framework_installed`'s per-name **content** gate; the membership list is now derived
  from it, so the two cannot be separated again.
- **Once recognition lands, this constant never sees the file.** A recognized install is categorized
  `vendor` before the source cap is consulted, so `DOC_ONLY_SOURCE_LOC_MAX` is not on S39′'s path at
  all. Verified on two real `bin/sync` runs: `source_loc` is **0** both before and after, and the
  trimmer's lines appear in `vendor` instead — 1 file before, **2 after**. No absolute LOC is quoted
  on purpose; the figure this paragraph first carried was stale within the hour, because both
  executables grew under the same session's edits. Re-derive it if you need it.

**BL-22 therefore stands entirely on its own merits, unblocked and unblocking**, and the merits are
unchanged: 200 has no derivation, no test asserts it, and the comment above `FRAMEWORK_INSTALLED_SOURCE`
still records a real **148-LOC** repo the cap alone misclassifies. The deliverable is still a decision.

**The deliverable is a decision, and "leave it at 200, with the reasoning written down" is a fully
correct outcome.** Options: (a) derive a value from real adopter repos and record the derivation;
(b) keep 200 and document it as a deliberate, stated heuristic; (c) pin whatever value survives with
a test so it cannot drift unnoticed. (c) is worth doing under any of the three. **Runnable fork-side;
the fix lands in a DISTRIBUTED file, so the PR needs the operator's go-ahead** — batch it with the
other distributed work rather than sending it alone.

**BL-23 — Issue #65's proposed invariants collide with fork state issue #65 doesn't know about.**
*Raised 2026-08-08 (S47), operator-directed review of #65 against work planned for an upstream PR.
Measured, not fixed (FM #17); answering #65 in any form remains an outward-facing action needing an
explicit go-ahead. Full evidence trail: [`issue-65-collision-review.md`](issue-65-collision-review.md).*

Two real collisions, both re-derived independently — this session's own greps plus a 4-agent
read-only investigation, agreeing on every cited fact:

1. **Evidence A's anchor has already moved.** #65 tests mutations against
   `starter-kit/SESSION_RUNNER.md`'s `## Learnings (added by sessions)` section. S34 (`ed22ace`,
   2026-08-03) already extracted the entire 13-row table out of that section into a new distributed
   file, `starter-kit/FRAMEWORK_LEARNINGS.md` (`# Framework Learnings`), leaving only a pointer
   paragraph under the old heading (`starter-kit/SESSION_RUNNER.md:362-364`). A
   `SESSION_RUNNER.md`-anchored implementation of Evidence A would find zero rows to mutate. S34's own
   claim flagged this exact tension as open (*"(d) the interaction with open upstream issue #65"*,
   `HANDOFFS.md:554`) and never resolved it — no session between S34 and S46 (twelve sessions)
   mentioned #65 again. S34's PR is prepared, vetted, and **not opened**, waiting on a go-ahead
   unrelated to this item (`framework-context-cost-plan.md:472`; `CHANGELOG.md` "S34's PR remains
   prepared and unopened"). Confirmed live against `upstream/main`: the table is still in the old
   location there today, so #65 is accurate *against upstream* — the collision is with the fork's
   unshipped state, not with reality as the maintainer currently sees it.
2. **Evidence B's own proposed invariant is false on this repo's real ledger.** *"`session:` values
   are unique"* does not hold: 51 combined receipts across `HANDOFFS.md` +
   `docs/archive/HANDOFFS-archive.md`, 47 distinct — S3/S5/S7/S8 each appear twice, because the fork
   and `upstream/main` run independent `S<N>` counters that this ledger's own header documents as
   colliding by design (`HANDOFFS.md:16-21`: *"a receipt is identified by session + date, never by
   number alone"*). Not a new discovery — BL-14 recorded the same falsification at 32/28 receipts —
   but it was never connected back to #65 itself as its own tracked item.

**Not a collision, checked and cleared:** none of BACKLOG.md's "runnable now up to the PR" items
(BL-12's first bullet, BL-13, BL-14's distributed half, BL-17's distributed half, BL-21) touch the
Learnings table, `FRAMEWORK_LEARNINGS.md`, or `bin/check-handoff`'s fence/key structure.
`bin/check-handoff`'s already-shipped BL-14/BL-17 cross-block checks (`check_answer_slots`,
`check_locator_forms`) do not implement any of #65's four Evidence-B asks and explicitly disclaim
answering it, in both the module docstring (`bin/check-handoff:72-76`) and a pinned test
(`bin/tests.sh` Test 25 N6) — no duplication risk.

**Adjacent, not blocking:** the parked `bin/check-citations` (branch
`docs/bl-10-dangling-learning-citations`, not on `main`) is a partial, already-broken answer to
Evidence A's contiguity check — hard-anchored to the pre-S34 file/heading, it now exits
`GUARD FAIL` against the current tree (this file's own S34 regression note, above). Whoever revives
it must retarget both constants first. The sibling branch `docs/learning-13-handoff-predictions` has
zero delta from `main` (already merged as PR #63) and should simply be pruned — no collision, just
stale housekeeping a prior session's `next_steps` asked for and nobody did.

**The deliverable is a decision, not an edit — same shape as BL-8/BL-22.** When S34's Learnings-table
PR is ready to open (its own go-ahead, separate from this item's), the operator should decide
whether/how to also flag #65 — e.g. a PR-description note to the maintainer, a direct comment on #65
once authorized, or leaving it for the maintainer to discover at review time. **Answering #65 in any
form is an outward-facing action and needs an explicit ask**, same rule as BL-12's second bullet.

**BL-24 — `mts-system` cleared both UAT blocking conditions; focused re-run CLOSED (S50).**
*Raised 2026-08-08 (S49), from a live conversational spot-check triggered by the operator, not a
scheduled sweep. Closed the same day (S50). Full evidence:
[`uat-2026-08-08-followup.md`](uat-2026-08-08-followup.md) §7 (raised) and §8 (closed).*

`mts-system` was one of three repos the S48 UAT follow-up recorded as carrying uncommitted work
(§6 there). Re-checked live at ~15:30 today: `git status --porcelain` reads **0** dirty paths (was
**2** at S48's 14:00 snapshot), and `bin/sync --dry-run ../mts-system` remains unblocked (exit 0 —
it was never F4-blocked, only the "carries uncommitted work" condition applied). The change is real,
independent adopter-side activity, not anything this fork did: `mts-system`'s own commit log shows an
internal session (its own "S95") closed out and left the tree clean about 1.5 hours after S48's
snapshot. Two things also worth noting, found in the same spot-check but out of this item's own
scope: `mts-system`'s `dashboard_history.jsonl` (F9) now looks independently tracked/resolved there
too; F2's dangerous `BOOTSTRAP.md:330` text is unchanged, byte-identical (closes only upstream, §6).

**CLOSED 2026-08-08 (S50):** ran the focused UAT pass this item queued — re-derived F6, F7, F9, F10,
F11 against `mts-system`'s current state (F1/F3/F4/F8/F12 correctly scoped out, per this item's own
framing). **F9 confirmed resolved** (tracked, deliberately unignored, documented in `.gitignore`) —
S49's "looks independently resolved" hedge is now a verified fact. **F10 improved, 1 → 0** reconcile
debt — new information this item's own scope didn't originally ask for but the re-run surfaced.
**F6 and F7 reproduce unchanged, still open** — the dashboard's presence-only compliance blind spot
and `check-handoff`'s all-numeric-sha false positive on receipt S74 both still stand exactly as S43
found them. **F11 not applicable** — `mts-system` was never one of the three repos missing
`HANDOFFS.md`. Zero regressions. Read-only throughout; `git status --porcelain` inside `mts-system`
confirmed 0 dirty paths both before and after. No sync or write action was taken or authorized.

**BL-25 — Focused `vscode_quarto_ext` UAT re-run, raised and CLOSED same session (S53).**
*Operator-directed 2026-08-08 (S53), choosing `vscode_quarto_ext` from three offered alternatives
(issue #67/PR #66, this fork's own F9 instance, F3). The `mts-system` counterpart to BL-24, run
against the other repo §7 flagged as "closer, not identical." Full evidence:
[`uat-2026-08-08-followup.md`](uat-2026-08-08-followup.md) §9.*

Pre-condition re-verified at claim: `git status --porcelain` **1** dirty path (`?? scratchpad/`, an
untracked non-methodology scratch directory, not a modified-tracked-file conflict — unchanged from
§7's S49 snapshot); `bin/sync --dry-run ../vscode_quarto_ext` exit 0, unblocked (never F4-blocked).
Re-derived **F2, F3, F6, F8, F9, F10, F11**, plus two bonus checks never run against this repo before
(**F1**, **F4**). **F9 confirmed resolved** — tracked, not ignored, not dirty; last touched by
`fe1e05b` with two further unrelated session commits landing since and leaving it untouched, which
upgrades §7's (S49) "committed cleanly today" hedge to a verified fact, the same upgrade BL-24 gave
`mts-system`'s F9. **F2, F3, F6, F8 reproduce unchanged, still open** — `BOOTSTRAP.md:330`'s
"overlay them" text is byte-identical; `SESSION_NOTES.md` grew to 7,549 lines/506 headings (+81/+6
since S43); the dashboard's 100%-compliance/11-drifting-files blind spot reproduces exactly, `bin/status`
now naming `SESSION_RUNNER.md`/`BOOTSTRAP.md` 8 versions behind; `ZONE_UNCLASSIFIED` still fires on
`HANDOFFS.md`, now at line 2807 (was 2771 — the shift is the file growing, not a new defect). **F10
unchanged at 0; F11 not applicable** (has `HANDOFFS.md`). **Both bonus checks came back clean**: F1's
original grammar-mismatch bug was never present in this repo's `CHANGELOG.md` (the trimmer's
`TRIGGER_BYTES` check fires correctly, no `NO_RECORDS`/`GRAMMAR_MISMATCH`); F4 confirms this repo was
correctly excluded from the "2 of 6 blocked" set. Adjacent, not a numbered finding:
`bin/check-handoff` now counts 96 unreconciled `commit:` answer slots (S38–S186), up from §4's 93
(S38–S184) — ordinary adopter ledger-hygiene drift, not a new tool defect. **Net: 1 of 7 improved
(F9), 4 unchanged/open (F2, F3, F6, F8), 2 unchanged-and-clean (F10, F11), zero regressions.**
Read-only throughout; `git status --porcelain` inside `vscode_quarto_ext` confirmed identical (1
dirty path) both before and after. No sync or write action was taken or authorized.

**BL-26 — Issue #67 and PR #66 checked against this fork's current state: neither is addressed, and
PR #66 has its own unfixed collisions.** *Raised 2026-08-09 (S56), operator-directed — offered and
declined as an alternative at BL-25's claim (S53) and left un-investigated across five prior sessions'
`next_steps`. Measured, not fixed (FM #17). Full evidence:
[`issue67-pr66-review.md`](issue67-pr66-review.md).*

**Issue #67** (`check_stale_version()` advertises `--sync`, a 26-file/25-repo portfolio write, as the
remedy for one stale copy) **reproduces verbatim in this fork's own `tools/methodology_dashboard.py`
and its `starter-kit/` twin** (`DASHBOARD_VERSION` 2.13.0, already past the `v2.10.2` the issue's own
example cites) — a live, currently-**shipped** defect, not merely an upstream gap this fork hasn't
pulled a fix for. All three parts reproduce: the warning still prints only the portfolio remedy
(`:774-777`), bare `--dry-run` still falls through to a full write (`:3923-3928`, reproduced live this
session), and none of the issue's four suggested fixes exist in `print_usage()`. Fork-side-fixable
today, independent of upstream — same class as BL-20/BL-22.

**PR #66** (Failure Mode #28 + `context_budget.py`, still `OPEN`/`MERGEABLE`) is **not safely
mergeable as-is**, two concrete collisions, both reproduced rather than inferred:
1. `install_hook()` targets `.git/hooks/pre-commit` unconditionally, with no `core.hooksPath`
   awareness — silently a no-op against this fork's own `.githooks/pre-commit` convention
   (`core.hooksPath = .githooks`, BL-6 item 3), printing a false "installed" success message. The
   PR's own dev-session note records `core.hooksPath` as unset in its author's test environment, so
   this path was never exercised there either.
2. `bin/check-handoff --all`'s new duplicate-`session:` check (built to answer issue #65) keys on the
   bare session id with no date component — **the exact invariant BL-23 already found false against
   this repo's real ledger** (S3/S5/S7/S8 each name two different real sessions, by this repo's own
   documented fork/upstream dual-sequence design). Re-verified live this session: still 4 duplicates.
   This fork's own `bin/check-handoff:74` already disclaims answering #65 for precisely this reason;
   PR #66 answers it anyway and inherits the flaw as shipped code.

**Adjacent, not a collision:** PR #66 overlaps ground this fork's own `framework-context-cost-plan.md`
(BL-19) already planned as **S45** (`bin/check-context-budget`, still unshipped) but goes further —
an actual commit-refusing size gate, where BL-19's five heuristics are all read-only/dashboard-only.
Whether this repo wants a size-enforcing gate at all is an undecided, operator-level design question,
parallel to BL-19 §7's existing decision items — not resolved here.

**Issue #67 thread: a full fork-side fix plan, PROPOSED 2026-08-09 (S57), RATIFIED as written
2026-08-09 (S58), operator-directed both times.** Not implemented — ratification approves the design,
it is not a go-ahead to implement (a future session's own deliverable) and not a go-ahead for any
upstream-facing action (the plan's own §9 restates this repo's ask-before-outward-facing-action rule
as a binding gate on itself). Covers all four of the issue's suggested fixes (scoped remedy message, a
generalized `--sync [TARGET_DIR]` in place of a second flag, a `.gitignore`-aware `--force` gate, and a
hard error on bare `--dry-run`), reached via a 3-candidate design panel (scored by 6 independent
judges, none scored above 7/10) synthesized into one design, then itself put through a second,
independent four-lens adversarial review that found and fixed one high-severity defect (the
create-gate silently blanket-gates any target directory that isn't a git repo yet — reachable through
the plan's own new capability) plus several medium/low citation and test-soundness defects. Full plan:
[`issue67-fork-side-fix-plan.md`](issue67-fork-side-fix-plan.md). **PR #66 thread unchanged, still
open** — neither session touched it.

No outward-facing action taken; PR #66 remains exactly as found. Issue #67 now has a ratified,
implementation-ready plan but is still functionally unaddressed — the live defect this plan describes
is still shipped; nothing changes there until a future session implements it.

**PR #66 thread: proposed fix drafted and posted as review comments, 2026-08-10 (S67),
operator-directed.** Both collisions above re-verified live against `df6a9918` (PR head, unchanged
since 2026-08-08) before drafting — `install_hook()` still targets `<git-dir>/hooks/pre-commit`
unconditionally (`starter-kit/context_budget.py:472-490`), and `validate_ledger()`'s duplicate check
still keys on bare `session:` (`bin/check-handoff:204-212`); the real ledger still reproduces the
second collision exactly (`S3`/`S5`/`S7`/`S8` each appear twice across `HANDOFFS.md` + both archives).
**Proposed fix, not implemented:** (1) `install_hook()` should check `git config --get
core.hooksPath` first and target that directory when set, falling back to `<git-dir>/hooks` only
when it's unset — a general correctness fix, not a fork-specific carve-out, since any repo using that
convention hits the same silent no-op. (2) `validate_ledger()`'s duplicate check should key on
`(session, date)` instead of `session` alone, matching the invariant `HANDOFFS.md` itself documents
(*"a receipt is identified by session + date, never by number alone"*) rather than the module
docstring's stronger, locally-false claim that session ids are unique. **Posted to PR #66 as three
review comments** — one general summary plus two inline `suggestion` blocks, each anchored to the
exact file/line/commit the defect reproduces at:
[general](https://github.com/KJ5HST/methodology/pull/66#issuecomment-5246274123),
[hook-install suggestion](https://github.com/KJ5HST/methodology/pull/66#discussion_r3753541194),
[duplicate-check suggestion](https://github.com/KJ5HST/methodology/pull/66#discussion_r3753543217).
**This is a comment, not a commit** — no code changed, nothing pushed to the PR branch, and the
suggestions are the PR author's to accept, reject, or ignore. Whether this fork's own copies of
`bin/check-handoff`/`context_budget.py`-equivalents ever need the same fix independently of what
happens to PR #66 is a separate, not-yet-raised question — this repo does not carry
`context_budget.py`, and its own `bin/check-handoff` has no `--all` mode to share the defect with
(disclaims answering issue #65 outright, per BL-23).

**Issue #67 thread: IMPLEMENTED fork-side, 2026-08-10 (S62), operator-directed.** All four fixes from
the ratified plan landed in both `tools/methodology_dashboard.py` and its `starter-kit/` twin
(byte-identical), `DASHBOARD_VERSION` 2.13.0 → 2.14.0, 17 RED-first tests
(`TestIssue67ScopedSync` in `tools/test_methodology_dashboard.py`), `bin/tests.sh` 185/186 (Test 9's
pre-existing expected failure, unrelated). Commit `7d682fa`. **Not the same as closed**: this is the
fork-side half only — the live defect no longer ships in this fork's own copies, but the upstream
issue itself is still open, and no PR has been opened against `KJ5HST/methodology` (the plan's own §9
gate — needs a separate, explicit go-ahead, asked for again at that time). **PR #66 thread still
untouched and still open** — this item did not touch it.

**BL-27 — `methodology_trim.py`'s generated `.verify.sh` has two known false-positive triggers on
`HANDOFFS.md`, distinct from the internal `--check`/`--write` assertions, which do not share them.
CLOSED (S65).**
*Raised 2026-08-10 (S64), found while independently re-running the tool's own generated proof for a
routine `HANDOFFS.md` archive-cut — the practice this repo's own precedent (S61, S63) established
specifically to avoid trusting the tool's write-time summary.* Both are reproduced, not inferred:

1. **Front-matter field regeneration reads as data loss.** `HANDOFFS.md`'s front matter carries a
   `This file currently holds **N**` receipt count that the tool mechanically regenerates on every
   archive (`[FRONTMATTER_FIELD_REGENERATED]`, e.g. `30 → 3` this session). The internal `assert_L2`
   check correctly excuses this — it reverses every *declared* regeneration and requires the original
   bytes back (`starter-kit/methodology_trim.py:523-563`) — but the simpler, self-contained check
   embedded in the generated `.verify.sh` only asserts "every non-blank line of the original front
   matter survives verbatim," with no concept of a declared exception. Any archive that changes this
   line — every one, since the count always changes — makes the standalone proof report
   `FAIL: L2 FRONT MATTER lost 1 line(s)` even though nothing was lost. Reproduced live this session:
   `docs/archive/HANDOFFS-through-2026-08-09.md.verify.sh` fails this way; manually diffing
   `HEAD:HANDOFFS.md` against the pre-commit working tree confirmed the *only* front-matter changes
   were the declared count regeneration and the declared pointer-block insertion — genuinely lossless,
   just not provable by the generated script as currently written.
2. **A same-commit close-out bundling reads as record alteration.** This repo's own established
   practice (S61, S63, and this session) commits an archive's `--write` output together with
   finalizing the session's *own* close-out receipt (`status: pending` → `complete`) in one commit.
   The frontier record (the newest, never archived) therefore legitimately differs between that
   commit's parent and itself — a fact the internal test suite already names and accepts
   (`tools/test_methodology_trim.py`'s `test_L3_fixture_is_the_event_that_bundled_an_edit_with_the_move`,
   fixture `7a71df0`, S23's original archive). But `.verify.sh`, re-run in commit-comparison mode
   after the fact, has no such exception and reports `FAIL: L3 record(s) not byte-identical … [0]` /
   an `L1` mismatch. Reproduced live this session against `docs/archive/HANDOFFS-through-2026-08-02.md.verify.sh`
   (S61's shard, untouched since `c0e6944`, same tool version `v1.1.1` throughout) — its record-0
   "alteration" is exactly S61's own receipt going from its pending stub to its finished self-score-7
   form, all within `c0e6944`. **This is not evidence of historical data loss** — S61's actual archive
   move is intact — but it does mean a past session's disclosed "independently re-ran `.verify.sh` —
   OK" can go stale the moment the receipt is later finalized into the same commit, and a *future*
   re-run of that same frozen script, done for due diligence, will misread as a fresh finding of loss
   unless the reader already knows this pattern.

**Practical mitigation already used this session, not a fix:** run `.verify.sh`'s underlying check
in the working-tree window *before* finalizing the session's own receipt (which is when `L1`/`L3`
are still meaningful), and rely on a manual front-matter diff — not the generated script's verdict —
for `L2`. **Not fixed here (FM #17):** the two real fixes are (a) teach the `.verify.sh` generator
the same declared-field-reversal exception `assert_L2` already has, and (b) either exempt the
frontier record from the generated script's `L1`/`L3` comparison when it's the only one to change, or
document the bundled-commit pattern in the script's own output so a `FAIL` doesn't read as an
unqualified loss. Both are changes to a canonical, adopter-distributed tool (`bin/_manifest.py`) and
need their own RED-first tests against `tools/test_methodology_trim.py`'s existing 91-test suite —
scoped as a session of its own, not folded into a trim.

**CLOSED 2026-08-10 (S65):** fixed both, in `VERIFY_TEMPLATE`/`build_verify`
(`starter-kit/methodology_trim.py`, the sole canonical copy — no `tools/` twin to mirror). (1) A new
`@@REGEN@@` template variable carries `spec.regenerated`'s declared field patterns into the
generated script (`repr()`'d, since it is 0-or-more patterns, not the single-pattern case
`@@START@@`'s r-string wrapper already handled); a `field_reversible()` helper excuses a "missing"
line only when it has a same-shaped partner elsewhere in the new front matter, identical everywhere
outside the declared field's own span. (2) L1/L3 now share one `rebuilt`/`bad`-index computation;
when the only altered record is position 0 (the frontier) the script still FAILs — a real loss can
have this exact shape — but also prints a `NOTE:` naming the known bundled-commit pattern, so a
`FAIL` here no longer reads as unqualified. RED-first: 4 new tests in a new
`TestVerifyShHandoffFalsePositives` class (`tools/test_methodology_trim.py`), a new
`make_handoff_repo` fixture (the suite's first end-to-end `HANDOFFS.md` trim through the actual
subprocess, not just `assert_L2` in isolation); both fix-tests confirmed RED against unpatched code
for the exact defects above, both narrowed controls confirmed already-green unpatched (proving the
fix doesn't become a blanket permit). Suite 91 → 95, all green; full `bin/tests.sh` unaffected.
`TRIM_VERSION` 1.1.1 → 1.1.2 (patch — no new finding code or exit status on the tool's own CLI, a
correctness fix to generated output). One real finding surfaced while building the first control
test, not fixed here: **BL-28**, its own entry below.

**BL-28 — the generated `.verify.sh`'s L2 "missing front-matter line" check is a substring test,
not an exact-line-set membership test, so an APPEND-style edit that keeps the original text as a
literal substring of the new line is invisible to it.** *Raised 2026-08-10 (S65), found while
building BL-27's own narrowed control test.* The check is `ln not in afront` — `afront` is the
whole front-matter TEXT, not a list of lines, so `in` is substring containment. A tamper of
`"# Handoff Receipts"` → `"# Handoff Receipts EDITED"` (append, not replace) left the original 19
characters intact as a literal prefix of the new line, and the check reported no loss — reproduced
live via the actual generated script, not inferred. **Pre-existing, not introduced by BL-27's fix**:
the same substring check was there before this session touched the file; BL-27's own fix (the
declared-field-reversal exemption) only *exposed* it, by removing a co-occurring, unrelated false
positive (the regen-field "loss") that had been accidentally covering for it in BL-27's own first
draft of that control test — the tamper appeared caught, but for the wrong reason. **The INTERNAL
`assert_L2` (used by `--check`/`--write`) does not share this defect** — it compares the whole
front-matter TEXT for exact equality after reversing declared changes (`residue != before_zones.front`),
which an append-style edit still fails correctly; the bug is specific to the standalone script's
separately-written, weaker line-based reimplementation. **Not fixed here (FM #17):** the fix is to
compare an exact set/sequence of lines (or reuse the internal residue-equality approach) instead of
substring containment — a change to the same canonical, adopter-distributed tool, needing its own
RED-first test. Low severity in practice (an append that happens to preserve the exact original
text as a contiguous substring is a narrow tamper shape), but real, and this file's own precedent
(BL-27) is to record what is found even when it is not what was being looked for.

**CLOSED 2026-08-10 (S68):** fixed in the same `starter-kit/methodology_trim.py` template (the sole
canonical copy — no `tools/` twin to mirror). The "missing" check now builds `afront_lines =
set(afront.splitlines())` once and tests `ln not in afront_lines` — exact membership in the new
front matter's line set — instead of `ln not in afront` (substring containment on the whole text).
`field_reversible()`'s own separate, correct line-by-line carve-out for the declared regenerated
fields is untouched. RED-first: a new `TestVerifyShAppendTamperEvadesSubstringCheck` class
(`tools/test_methodology_trim.py`) with the exact reproduction from this entry (`"# Handoff
Receipts"` → `"# Handoff Receipts EDITED"`, append not replace) — confirmed FAILing (no `FAIL:` in
the script's output) against unpatched code before the fix, `FAIL: L2 FRONT MATTER` after; a
narrowed control re-confirms the regenerated-count field still passes unpatched-and-patched, so the
fix doesn't turn the exact-line-set comparison into a blanket new false positive. Trimmer suite 95 →
97, all green; full `bin/tests.sh` unaffected. `TRIM_VERSION` 1.1.2 → 1.1.3 (patch — no new finding
code or exit status on the tool's own CLI, a correctness fix to generated output, same class as
1.1.2). The sibling BL-27 control test's own comment about needing a full-line replacement (not an
append) for its tamper — because an append would have been invisible to *this* defect — is now
historical: an append-shaped tamper is caught too, verified by the new test above it in the same
file.

**BL-29 — D4(c)'s "methodology" directory-exclusion fix does not cover the self-scan case it was
meant to close.** *Raised 2026-08-10 (S70), found while investigating cross-repo methodology-adoption
effects for the operator; reproduced live, not inferred.*

D4(c) (`0e188f5`, 2026-08-03, `DASHBOARD_VERSION` 2.10.3 → 2.11.0) removed `"methodology"` from
`EXCLUDE_DIRS` — but its own commit message discloses the naive form couldn't ship as worded, because
`discover_projects()` has two consumers and `sync_dashboards()` is a write path, so the naive removal
"would have made `--sync` install a third copy into this repo's own root." A different fix landed
instead ("Fixed and mutation-proved"), and S69's own `HANDOFFS.md` receipt separately flagged, but did
not chase, that `python3 tools/methodology_dashboard.py` run in-place from this repo's own root still
reports "No projects found" rather than scanning this repo as a single project. Reproduced live this
session, against current `HEAD` (`DASHBOARD_VERSION` 2.14.0):

```sh
$ python3 tools/methodology_dashboard.py --no-open
Methodology Dashboard: No projects found.
```

The portfolio-root copy (`/Users/rmsharp/Development/methodology_dashboard.py`) scans this repo
correctly as part of the 13-project portfolio — the defect is specific to running the in-repo copy
from its own root in single-project mode, the same `single_project = (root / ".git").exists()` branch
`main()` already special-cases for its title text but apparently not for discovery. **Not fixed here
(FM #17):** whoever revives it should first re-read the D4(c) commit's own account of why the naive
fix was rejected, so a second attempt doesn't reintroduce the write-path collision it already found
and avoided once.

**CLOSED 2026-08-10 (S72).** Re-read D4(c)'s own account first, as this entry asked: its collision
was in `sync_dashboards()` (a WRITE path taking `discover_projects()`'s exclusion set with it), a
different function from the one `main()`'s plain scan calls `discover_projects()` through — so this
fix never touches `EXCLUDE_DIRS`, `discover_projects()`, or `sync_dashboards()` at all, and cannot
reintroduce that collision. The actual defect was `ROOT = Path(__file__).parent`: correct for every
adopter-installed and portfolio-root copy (all sit exactly where `bin/_manifest.py` /
`sync_dashboards()` place them), wrong for the methodology repo's own two checked-in copies
(`tools/`, `starter-kit/`), which file the script one level BELOW the repo they belong to. Fixed with
a new `resolve_single_project_root()` (both twins) that bridges `ROOT` to its parent only when
`ROOT.name` is `tools` or `starter-kit` AND the parent both is a git repo and carries
`bin/_manifest.py` — the same structural marker `detect_repo_role()` already trusts to prove "this
is the framework's own publishing repo", which no adopter can acquire via `bin/sync`. Deliberately
narrow: not a generic upward walk, which could let an accidental copy anywhere in an unrelated
subdirectory tree claim its ancestor as "the project". `main()`'s single call site
(`root = resolve_single_project_root(ROOT)`) is the only line changed in `main()` itself.
Verified live, both copies, from this repo's own root:
```sh
$ python3 tools/methodology_dashboard.py --no-open
  METHODOLOGY — METHODOLOGY DASHBOARD  │  1 projects  │  v2.15.0
  Health: 76/100    High+ Risk: 0    Commits: 491
```
— matching the portfolio scan's own row for this repo exactly. `DASHBOARD_VERSION` 2.14.0 → 2.15.0.
6 new RED-first tests (`TestBL29SelfScanRoot`, `tools/test_methodology_dashboard.py`): each failed
with `AttributeError` pre-fix except the end-to-end reproduction, which failed by actually printing
"No projects found" — confirmed the exact reported symptom before patching it. Coverage includes a
negative control (`test_a_tools_dir_with_no_manifest_marker_is_not_bridged`): an adopter repo with
its own unrelated `tools/` directory and no `bin/_manifest.py` is NOT bridged, proving the marker
check — not just the directory name — gates the new behavior. Dashboard suite 284 → 290, all green;
full `bin/tests.sh` 185/186 unaffected (Test 9's pre-existing upstream-404 baseline). Twins verified
byte-identical after the mirror. `dashboard_history.jsonl` gained two real entries from the live
verification runs above — first time this repo's own root copy could write its own history.

**BL-30 — Watch item, not a defect: `methodology_trim.py`'s next firing outside `nprcgenekeepr`.**
*Raised 2026-08-10 (S70), operator-directed, while examining cross-repo adoption effects. Deliberately
lightweight — a tracking note, not a defect write-up like this file's other entries.*

`methodology_trim.py` (shipped at `DASHBOARD_VERSION`/`TRIM_VERSION` 2.13.0-era, S39) is installed in
four local adopter repos — `mts-system`, `nprcgenekeepr`, `vscode_quarto_ext`, `wsfct` — but has
actually **fired** (archived real ledger records, not merely been present) in exactly **one**:
`nprcgenekeepr`, 2026-08-10 (session S509, commits `0929172a`/`d07814a7`, 288 + 181 records archived,
verified by its own generated `.verify.sh`). The other three haven't crossed their trim trigger yet.
One clean run in one repo is evidence the tool *can* work, not that it generalizes across different
ledger shapes, sizes, and histories. **Check on later:** the next time any of the other three crosses
its trigger, confirm the run is verified by its own `.verify.sh` (not just "ran without error") before
treating the tool as proven rather than promising.

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
