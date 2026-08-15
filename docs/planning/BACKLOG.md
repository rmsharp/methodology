# Operational Backlog (fork-only)

Operational/coordination backlog for **rmsharp's** methodology work. Fork-only — it lives in
`docs/planning/` and is **not** part of the canonical framework or any upstream PR (same convention
as [`adopter-pr25-27-remediation-plan.md`](adopter-pr25-27-remediation-plan.md)).

This is a backlog, **not** GitHub issues, by operator decision.

**Open: BL-11, BL-12, BL-13, BL-14, BL-16, BL-17, BL-18, BL-19, BL-20 (residual only), BL-21,
BL-22, BL-23, BL-26, BL-30, BL-31, BL-32, BL-36, BL-37.** Re-derive rather than trust that list —
it is hand-maintained, and it has been wrong before:

```
grep -nE '^\*\*BL-[0-9]+ —' docs/planning/BACKLOG.md
```

Two things that grep will *not* tell you, both deliberate: **BL-16 is open but has no heading of
its own**, living inside BL-14's follow-ons paragraph; and **BL-20's heading now covers only its
open residual**, its closed history having moved to the archive below.

**⚠ Do not trust a number in this file without re-deriving it.** S30 re-measured every open item
and found a wrong number in **six of six**; the corrections are in `CHANGELOG.md` (*"The framework's
context cost — adopter heuristics and a remediation plan"*) and the items themselves are
deliberately NOT edited (FM #17). Known-wrong figures still standing in the prose below: the
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
**PR OPENED 2026-08-10 (S73):** [upstream PR #68](https://github.com/KJ5HST/methodology/pull/68),
re-verified against `upstream/main` fresh (no drift since this item was raised — `upstream/main` had
not advanced past the `e02538b` resync at all), re-grounded the row on FM #15 + the Minimum Handoff
Requirements rather than reusing `1eac7a4`'s wording verbatim (that text answered a since-superseded
corpus state — a dangling `Learning #34` citation that no longer exists to remove). `bin/tests.sh`
84/84 and `bin/check-links` OK on the PR branch. Awaiting maintainer review; not yet merged.
**Turned `CONFLICTING` 2026-08-11, diagnosed same day (S76).** Root cause, confirmed with
`git merge-tree --write-tree --name-only upstream/main <branch>` (not inferred): **`CHANGELOG.md` is
the only conflicting path** in all of #68/#69/#70 — every other touched file, including
`starter-kit/HANDOFFS.md` in #69, auto-merges clean despite PR #66 also touching it. This PR (and
#69/#70) branched from the shared base `e02538b` at 05:00 UTC 2026-08-11; PR #66 merged into
`upstream/main` (`a2a7275`) at 15:15 UTC the same day, landing a 9-commit batch
(`e02538b..a2a7275`: two upstream sessions, S9 and S10) that rewrote `CHANGELOG.md`'s header
source-tag prose (lines 17-20 at the base) and prepended several new dated entries — the identical
top-of-ledger insertion point every session's own new entry also targets. Git's three-way merge
cannot reconcile two independent prepends at the same location plus a genuine content edit on the
same lines, so it conflicts by construction, not because of any defect in this PR's own change.
[PR #71](https://github.com/KJ5HST/methodology/pull/71) does **not** conflict because it was branched
at 16:36 UTC, after #66 had already merged — its base `CHANGELOG.md` already includes the batch.
**Fix is mechanical: rebase onto current `upstream/main` and re-resolve the `CHANGELOG.md` prepend
(keep both sides' entries, reorder by date), not a content change** — not yet done; needs a
go-ahead, since it touches an open upstream PR branch. Same root cause and same fix shape apply to
#69 and #70 below; see this note rather than repeating it.
**REBASED AND FORCE-PUSHED 2026-08-11 (S76, operator-directed).** All three rebased onto
`upstream/main` (`a2a7275`, unchanged since diagnosis), `CHANGELOG.md` resolved by keeping both
sides' entries with the rebased PR's own new entry placed above the already-merged PR #66 entries
(newest-on-top, matching the ledger's own convention) — `f1dd996` → `b4ceb73`. Confirmed clean with
`git merge-tree --write-tree --name-only upstream/main <branch>` (no `CONFLICT` output) before
pushing, not assumed from a successful `rebase --continue` alone. `bin/check-links` OK on the
rebased tree. `gh pr view 68 --json mergeable` → `MERGEABLE` after GitHub recomputed (took under a
minute; read `UNKNOWN` immediately after push, which is normal async lag, not a second problem).
**Found, not fixed, while verifying: a latent version collision with PR #71, unrelated to the
conflict just fixed.** Both #70 (this item's fix, unchanged by the rebase) and the already-open
#71 bump `DASHBOARD_VERSION` `"2.10.2"` → `"2.10.3"` for unrelated changes — #70 branched before
#71 existed, so no git conflict today, but whichever of the two merges *second* will re-diff
against a tree where the string already reads `2.10.3`, which is either a silent no-op (if by then
identical) or a fresh conflict on that exact line. Neither PR's own content is wrong; this is
sequencing, decided by merge order the fork does not control. Not raised as its own BL item —
small enough to note here and revisit once the maintainer merges either one.

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
**DISTRIBUTED half — PR OPENED 2026-08-10 (S73):**
[upstream PR #69](https://github.com/KJ5HST/methodology/pull/69), choosing fork **(B) delete the
promise** over (A) schedule it — re-verified live: upstream's Phase 0 step 6 is byte-identical to
the fork's (confirmed by diff), never mentions `commit:` at all, and (A)'s real footprint turned
out larger than "add a case" (Phase 0's write permission is explicitly *append-only*; reconciling
an existing receipt's `commit:` field in place is a mutation, not an append — a doctrinal conflict
(A) would have to resolve first). Re-derived the "seven distributed `status: pending` sites" this
item cites: the same grep now returns **11**, not 7, on the current tree — none of the 11 mention
`commit:`, so (B)'s edit stays confined to `HANDOFFS.md` alone regardless. **Bundled with BL-17 in
the same PR** (same file, adjacent lines, one review pass). `bin/tests.sh` 84/84 and
`bin/check-links`/`bin/check-handoff` OK on the PR branch. Awaiting maintainer review; not yet
merged. **Turned `CONFLICTING` 2026-08-11, diagnosed same day (S76) — same root cause as BL-13's
#68 note above (`CHANGELOG.md` prepend-point collision with PR #66's merged batch, confirmed via
`git merge-tree` as the only conflicting path); needs the same rebase, not a content fix.**
**REBASED AND FORCE-PUSHED 2026-08-11 (S76, operator-directed), same run as BL-13's #68 — see that
entry for the shared method. `d47d4ee` → `e74de65`; the `starter-kit/HANDOFFS.md` auto-merge was
diffed against `upstream/main` (not trusted from a clean `rebase --continue` alone) and confirmed
to carry only this PR's own two intended edits, nothing lost or duplicated from PR #66's separate
edits to the same file. `gh pr view 69 --json mergeable` → `MERGEABLE`.** **A
third instance of the same promise, fork-only, still open:** the investigating agent
found a `starter-kit/HANDOFFS.md` "Size, and when to archive" section (fork-only — upstream has no
equivalent, since upstream has no archiving) that restates the identical unkept promise at its own
`:134-136`. Not part of the PR (nothing to fix upstream, since the section doesn't exist there);
needs its own small fork-local fix in a future session so the fork's own copy doesn't cite a
promise its own PR just deleted upstream.
*Follow-ons raised, deliberately not bundled (FM #17):* **BL-15** — `changelog_ref` carries the
identical escape in 13 of 32 receipts, but its false-positive surface is wider (a legitimately
pending PR number is plausible). **BL-16** — `bin/check-handoff:301-303`'s docstring claims the
canonical repo "has no root-level receipt ledger of its own," which is false here (13 receipts + a
19-receipt archive it knows nothing about).

**BL-17 — The `changelog_ref` referent the seed does not offer, and the one title that is stale.**
*Raised 2026-08-02 (S29) out of BL-15's settlement; measured, not fixed (FM #17).*
Two halves that share one root cause: **the distributed spec offers no locator a fork-local session
can actually write.** `starter-kit/HANDOFFS.md:63` gives `PR #N` (there is often no PR) and a
short-sha (unknowable while the receipt is being written). **0 of 32 receipts use either.** All 32
invented the same third form — `CHANGELOG.md "<its ### heading>"` — and eight then reached for a
line number on top. *That vacuum is why the anchors existed*, so the shipped prohibition treats the
symptom and this item is the cause.
- **The DISTRIBUTED half — PR OPENED 2026-08-10 (S73).** Bless the quoted `### ` heading as a
  third locator form at `starter-kit/HANDOFFS.md:63`, and state that a line number is not a locator
  into a ledger. Per **Learning #8** a fix must reach every checklist restating close-out.
  [upstream PR #69](https://github.com/KJ5HST/methodology/pull/69) (bundled with BL-14's
  distributed half — same file, adjacent lines). Confirmed byte-identical against `upstream/main`
  before editing; also found `bin/check-handoff`'s own remediation-hint text already teaches the
  `CHANGELOG.md "<its ### heading>"` convention the spec never blessed, so the wording matches what
  the checker already prints. `bin/tests.sh` 84/84 OK on the PR branch. Awaiting maintainer review;
  not yet merged.
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

**BL-20 — the seed still documents only the `- **Model:**` list form the live ledger does not
use. RESIDUAL ONLY; the defect itself is FIXED.**
*Raised 2026-08-02 (S31); fixed 2026-08-11 (S79) as option (1) of three — `CHANGELOG_MODEL_RE`
widened so `bin/model-report`'s Source 1 reads both dialects. Closed history archived verbatim to
[`BACKLOG-archive-2026-08-15.md`](BACKLOG-archive-2026-08-15.md).*
**What is still open, and only this.** Option (3): change the distributed seed
(`starter-kit/CHANGELOG.md:42`, `:57`, `:69`) to document the bare `**Model:**` form this repo
actually writes. It would close the last gap — the seed and the live convention still disagree, and
the widened regex tolerates that disagreement rather than settling it. It is a **DISTRIBUTED**
change that ships upstream and **needs its own go-ahead**. Option (2) (normalise the live entries to
list form) is not merely untaken but ruled out: it rewrites dated `CHANGELOG.md` entries, which the
v2.7.1 convention forbids outright.

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
**Blocked *behind* a decision nobody has made yet: whether this hook is contributed at all** —
not on any general channel state (`.githooks/pre-commit` being canonical-only was itself a ratified
decision, BL-6 item 3). **Re-verified 2026-08-10 (S73), NOT bundled into the PR batch opened this
session** — the precondition is still unmet: `git grep -c githooks bin/_manifest.py` is still 0
(never distributed to adopters), and `.githooks/pre-commit`'s Phase 1B exemption logic (`a56dff8`)
is fork-only — confirmed `upstream/main`'s own canonical copy at the URL this item's own proposed
sentences would cite has zero exemption logic (still the pre-exemption `dc8aa76` shape; the two
files have also further diverged, not converged, since this item was raised — `.githooks/pre-commit`
was BYTE-IDENTICAL to upstream when written, it is not now). Landing the two sentences now would
describe a hook neither the cited canonical URL nor any adopter's copy actually has — the same
false-on-arrival shape BL-21 itself was written to avoid. Leave exactly as scoped.

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

**DECIDED (b)+(c), PR OPENED 2026-08-10 (S73):**
[upstream PR #70](https://github.com/KJ5HST/methodology/pull/70). Re-verified first that no prior
session had actually made this decision despite being carried as "prepared" through seven handoffs
(S66–S73) — `git log --all --grep="BL-22"` turns up only this item's own raise and this session's
own claim, never a decision commit. (a) declined as disproportionate to a bundle-PR session (needs
a defined measurement corpus this session doesn't have). Shipped: a comment above the three
constants recording them as deliberate, unmeasured heuristics, plus a direct regression test
(`test_doc_only_thresholds_are_pinned_not_left_to_drift`) pinning all three current values —
`test_source_cap_boundary` already pinned `DOC_ONLY_SOURCE_LOC_MAX` *indirectly* via hardcoded
200/201 literals, but that coverage would silently vanish if that fixture were ever rewritten to
derive its boundary from the constant instead. `DASHBOARD_VERSION` 2.10.2 → 2.10.3 in both
`tools/` and `starter-kit/` twins. `python3 tools/test_methodology_dashboard.py` 198/198 and
`bin/tests.sh` 84/84 on the PR branch. Awaiting maintainer review; not yet merged.
**Turned `CONFLICTING` 2026-08-11, diagnosed same day (S76) — same root cause as BL-13's #68 note
above (`CHANGELOG.md` prepend-point collision with PR #66's merged batch, confirmed via
`git merge-tree` as the only conflicting path, despite this PR's own substantive files —
`tools/methodology_dashboard.py` / `starter-kit/methodology_dashboard.py` /
`tools/test_methodology_dashboard.py` — never being touched by #66 at all); needs the same rebase,
not a content fix.**
**REBASED AND FORCE-PUSHED 2026-08-11 (S76, operator-directed), same run as BL-13's #68 — see that
entry for the shared method and for a latent `DASHBOARD_VERSION` collision with PR #71 found while
verifying this one (both bump `2.10.2` → `2.10.3` independently; not a conflict today, sequencing
risk at whichever merges second). `d56b983` → `13796c4`. `python3 -m unittest
tools/test_methodology_dashboard.py` on the rebased branch: 198/198 minus the same 2 pre-existing
`FRAMEWORK_INSTALLED_SOURCE`/`CHECKLIST_EXEMPT` failures BL-31 already found and fixed in the
still-unmerged PR #71 — confirmed present on unmodified `upstream/main` itself via a throwaway
worktree before trusting that they weren't introduced by this rebase. `gh pr view 70 --json
mergeable` → `MERGEABLE`.**

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

**PR #66 thread: MERGED 2026-08-11, both review findings confirmed genuinely implemented (S74).**
`gh pr view 66` shows `state: MERGED`, `mergedBy: rmsharp`, merge commit `a2a7275` — both S67 review
comments were fixed by the maintainer **before** merge, not left as unresolved suggestions: `14bd88a`
(*"fix(context-budget): install-hook must honor core.hooksPath"*) and `63e1dcf` (*"fix(check-handoff):
receipt identity is session + date, not session alone"*), each crediting *"Reported by rmsharp in
review of PR #66"* in its commit message, each with new RED-first `bin/tests.sh` assertions (107→111,
then →112). `starter-kit/HANDOFFS.md` also gained 7 lines stating the session+date identity rule this
item's own proposed wording asked for. **Re-verified independently, not by reading commit messages
alone:** checked out `a2a7275` in an isolated `git worktree`, ran `bash bin/tests.sh` three times —
113–114/114 passed each run, the one intermittent failure being this fork's already-known
`gh api`/github-source-dry-run network flake (Test 9's baseline), not a regression. **This closes the
PR #66 thread of BL-26.** The issue #67 thread (fork-side fix shipped S62, not yet contributed
upstream) remains open on its own — a separate go-ahead question, unaffected by this merge.

**New, out-of-scope finding surfaced while re-verifying (S74), disclosed not fixed (FM #17): see
BL-31.** `python3 -m unittest tools/test_methodology_dashboard.py` against `a2a7275` — 2 failures,
reproduced consistently (not a flake): PR #66 added `context_budget.py`/`.context-budget.json` to
`bin/_manifest.py` as newly distributed files, but `tools/methodology_dashboard.py`'s
`FRAMEWORK_INSTALLED_SOURCE` exclusion tuple was never updated to include the new TRACKED file. This
is `upstream/main`'s own state post-merge, not anything this fork introduced.

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

**BL-31 — `upstream/main`'s dashboard exclusion list wasn't updated for PR #66's new distributed
file; reproduces on `a2a7275` today.** *Raised 2026-08-11 (S74), found while re-verifying BL-26's PR
#66 review-comment fixes — out of that item's scope, so recorded separately rather than folded in
(FM #17). Measured, not fixed.*

**The defect.** `bin/_manifest.py:44` (as of `a2a7275`, upstream `main` post-merge) adds
`("starter-kit/context_budget.py", "context_budget.py", TRACKED)` — a new framework-owned file
`bin/sync` now installs into every adopter root, same class as `methodology_dashboard.py` itself.
`tools/methodology_dashboard.py:344`'s `FRAMEWORK_INSTALLED_SOURCE = ("methodology_dashboard.py",)`
was never extended to match, so the dashboard's own LOC-counting will attribute `context_budget.py`'s
source to the *adopter's* code rather than excluding it as framework tooling — the same class of
scoring distortion `FRAMEWORK_INSTALLED_SOURCE`'s own neighboring comment (`:346-350`) describes for
the markdown half of this exact problem.

**Reproduced, not inferred.** `git worktree add <tmp> a2a7275 && python3 -m unittest
tools/test_methodology_dashboard.py`: 2 failures, both in `TestFrameworkInstalledExclusion` —
`test_no_manifest_file_is_unaccounted_for` (`context_budget.py`/`.context-budget.json` show up as
"distributed adopter-root file(s) neither on METHODOLOGY_ITEMS nor in CHECKLIST_EXEMPT") and
`test_exclusion_list_matches_the_manifest` (the tuple comparison fails outright:
`('methodology_dashboard.py', 'context_budget.py', '.context-budget.json') !=
('methodology_dashboard.py',)`). Reproduced consistently across 3 runs — not the known `gh api`
network flake (`bin/tests.sh` Test 9), a separate, deterministic failure.

**Scope note.** This is `upstream/main`'s own state, introduced by PR #66, not anything this fork's
own tree carries — this fork does not distribute `context_budget.py` (BL-26's own note: "this repo
does not carry `context_budget.py`"). It is upstream's defect to fix, in upstream's own
`tools/methodology_dashboard.py` (this fork's canonical-only twin has no `context_budget.py` entry to
add either, so nothing here is fork-side-fixable the way BL-20/BL-22 were). **Whether/how to flag
this to the maintainer is an outward-facing decision needing an explicit go-ahead**, same rule as
BL-23/BL-26's issue-#67 thread.

**PR OPENED upstream 2026-08-11 (S75), operator-directed** (chose "open an issue/small PR
describing/fixing it" over fork-side-only continuation, offered as one of two options): re-verified
`upstream/main` first — unchanged since S74's `a2a7275` measurement, no drift. **Correcting S74's own
test attribution while re-deriving it (this file's own header warns not to trust a number without
re-checking):** S74 named both failures as inside `TestFrameworkInstalledExclusion`
(`test_no_manifest_file_is_unaccounted_for` + `test_exclusion_list_matches_the_manifest`). Re-running
`python3 -m unittest tools/test_methodology_dashboard.py` against a fresh worktree at `a2a7275` found
the first failure is actually `test_every_distributed_adopter_root_file_is_scored_or_exempt` in a
*different* class, `TestChecklistCurrency` — a real second defect (the compliance-checklist
`CHECKLIST_EXEMPT` map, not just `FRAMEWORK_INSTALLED_SOURCE`) that S74's prose collapsed into one.
No `test_no_manifest_file_is_unaccounted_for` exists in the test file at all. Both are pre-existing
tests (last touched `bec4095`, before PR #66), not newly authored. Fix: extended
`FRAMEWORK_INSTALLED_SOURCE` to `("methodology_dashboard.py", "context_budget.py",
".context-budget.json")` (mirrored `tools/`+`starter-kit/`) and `CHECKLIST_EXEMPT` (in
`tools/test_methodology_dashboard.py`) with both new dests, same reasoning already on record for
`methodology_dashboard.py`'s own exemption; `DASHBOARD_VERSION` 2.10.2 → 2.10.3. Built and verified in
an isolated `git worktree` branched from `a2a7275` (not this repo's own tree, which carries neither
file): `python3 -m unittest tools/test_methodology_dashboard.py` 197/197 (was 195/197), `bash
bin/tests.sh` 114/114, `python3 bin/check-links` OK (83/21), twins byte-identical. **One recovered
mistake, not shipped:** the comment first drafted for `FRAMEWORK_INSTALLED_SOURCE` cited this fork's
own `BL-31` id directly inside upstream/adopter-installed source — caught before committing and
reworded to describe the defect in neutral terms with no fork-only vocabulary, the exact class BL-11
already flagged (fork ID shipped inside adopter-installed code). **Also caught and recovered before
pushing:** the first commit attempt was blocked by upstream's own pre-commit `CHANGELOG.md`-ledger
hook; running `git commit --amend --no-edit` immediately after landed the fix as an amend of the PR
#66 *merge commit itself* (`a2a7275` → `142e807`) rather than a new commit on top of it — caught by
reading `git log` right after, not assumed clean. Recovered with `git diff a2a7275 142e807 -- <4
files> > patch`, `git reset --hard a2a7275`, `git apply patch`, then a fresh, correctly-parented
commit — verified via `git log -1 --format="%H parent=%P"` before pushing. Nothing was pushed during
the bad state. PR: [KJ5HST/methodology#71](https://github.com/KJ5HST/methodology/pull/71), open,
`MERGEABLE`. Not yet reviewed/merged — nothing further owed here unless the maintainer asks for
changes.

**BL-32 — `methodology_trim.py`'s `LEDGERS` config table covers only the two ledgers the framework
itself owns; an adopter with a third grow-and-must-be-read file has no supported path to trim it.**
*Raised 2026-08-11, reported by an operator conversation relaying a live `nprcgenekeepr` Claude Code
session's own investigation into a "ledger-size trim" deliverable there — not a session claimed in
this repo. Independently verified against this repo's own canonical source before being recorded
here. Measured, not fixed (FM #17).*

**The defect, verified here.** `starter-kit/methodology_trim.py:161` — `LEDGERS = {` — has exactly
two keys, `"CHANGELOG.md"` and `"HANDOFFS.md"`; there is no `tools/` twin (this file has always had a
sole canonical copy, per BL-27/BL-28's own fix notes). A ledger-shaped file with no entry hits
`NO_CONFIG` in `evaluate()` (`:1508-1513`) and exits 3. `nprcgenekeepr` (a portfolio adopter, distinct
from this fork) has two more grow-and-must-be-read files needing the same treatment as
CHANGELOG.md/HANDOFFS.md: `SESSION_NOTES.md` (a canonical starter-kit template — reported at 40,252
lines, ~20× the 2,000-line agent `Read` cap) and `BACKLOG.md` (project-bespoke, no starter-kit
template — reported at ~2,181 lines, ~1× over). Neither can be trimmed by the shipped tool as it
stands. The two file sizes above are as reported by the adopter session, not independently
re-measured in that repo by this one.

**Reported extensibility claim, checked here and found NOT to hold.** The reporting session
characterized the tool's own design comment as inviting adopters to add their own `LEDGERS` entries.
Re-read directly (`:131-132`, restated at `:1511-1512`): *"It does NOT fall back to a generic rule,
because a generic rule is exactly what would mis-zone an adopter's differently-shaped ledger (design
§6.3)."* That is the tool's stated reason for having **no** generic/auto-detected fallback at all —
every `LedgerSpec` is deliberately hand-authored (content probe, footer mode, seed negation,
regenerated-field handling, each individually reasoned through — see the two existing entries,
`:162-212`) precisely because guessing a ledger's shape risks silently corrupting it. Read plainly,
the comment argues **against** ad hoc adopter-authored specs, not for them.

**Why that correction matters, not just its accuracy.** It weakens the reporting session's own
leading option — hand-add `SESSION_NOTES.md`/`BACKLOG.md` entries locally, flag the risk — on two
independent grounds, not one: (1) `methodology_trim.py` is classified **Tracked** in
`starter-kit/BOOTSTRAP.md:354` — *"overlay — replace with the latest"*, the same bucket as
`SESSION_RUNNER.md`/`SAFEGUARDS.md` — so `bin/sync` silently discards any local edit to it, and no
existing survive-the-sync mechanism covers this shape of edit (the closest precedent, the
never-overwrite list for adopter-*owned* whole files, was built for a different problem — a whole
file an adopter owns outright, not a partial hand-edit inside a canonical overlay file); (2) a
hand-written spec assembled without the same design rigor the two shipped ones required is exactly
the "mis-zone a differently-shaped ledger" failure the tool's own comment exists to prevent.

**Scope, not yet decided.** No project in the local portfolio (`mts-system`, `nprcgenekeepr`,
`vscode_quarto_ext`, `wsfct`) has ever extended `LEDGERS` — as reported by the adopter session, not
independently re-verified across those other three repos here. Adjacent to **BL-30** (the watch item
on where `methodology_trim.py` has/hasn't fired outside `nprcgenekeepr`) — the other three repos will
hit this same wall the moment any of them grows a third ledger-shaped file past its own trim trigger.
Whether the right fix is (a) a canonical `LedgerSpec` for `SESSION_NOTES.md` shipped in this repo (it
is, after all, a framework-standard filename every adopter gets), with `BACKLOG.md` left as
project-bespoke and out of scope; (b) a documented, supported adopter-extension mechanism with its
own sync-survival story; or (c) something else — **is a decision, not yet made, and not this entry's
to make.** Nothing here was implemented, and no upstream/outward-facing action was taken.

**One of the three options is now measurably ruled out for `BACKLOG.md` specifically (S89,
2026-08-15).** A `LedgerSpec` for a backlog file cannot work, and this is a property of the tool's
model rather than of any particular spec anyone might write. Every `LedgerSpec` requires a
`date_of_record` callable (`starter-kit/methodology_trim.py:145`, `:150`, `:158`) and `evaluate()`
freezes the **oldest by date**; a backlog's reduction axis is **status, not age**. Measured on this
repo's own file at the moment of reduction: BL-11 (raised 2026-08-01) is open and had to be
retained, while BL-35 (raised 2026-08-11) was fixed and was exactly what had to go. A date-keyed
trim would have archived the open items and kept the closed ones — the *"mis-zone an adopter's
differently-shaped ledger"* failure the tool's own comment (`:131-132`) exists to prevent, arriving
through the front door as a hand-authored spec rather than through the generic fallback it refuses
to have. Backlog reduction was therefore done **by hand** here, with its own identity-keyed proof
([`BACKLOG-archive-2026-08-15.md.verify.sh`](BACKLOG-archive-2026-08-15.md.verify.sh)). This
narrows the open question rather than answering it: it says nothing about option (a)'s
`SESSION_NOTES.md` spec, which is a different file with a different shape, and it leaves (b) — a
supported adopter-extension mechanism — untouched. **The decision is still not made.**

**BL-36 — Four of the six shipped `.verify.sh` losslessness proofs do not hold. Raised 2026-08-15
(S87), found, not fixed.**

The archive front matter tells every reader *"run it rather than trusting this sentence"*, and for
four of six shards that instruction currently returns FAIL. Observed at HEAD:

| Shard's proof | Generated by | Result |
|---|---|---|
| `CHANGELOG-through-2026-08-02.md.verify.sh` | v1.1.1 | **FAIL** — L1 not byte-identical; L3 record count 73 != 72 |
| `CHANGELOG-through-2026-08-09.md.verify.sh` | v1.1.1 | **FAIL** — L1 not byte-identical; L3 record count 77 != 75 |
| `HANDOFFS-through-2026-08-02.md.verify.sh` | v1.1.1 | **FAIL** — L1 not byte-identical; L3 record `[0]` not byte-identical |
| `HANDOFFS-through-2026-08-09.md.verify.sh` | v1.1.1 | **FAIL** — L2 front matter lost 1 line; L3 record `[0]` not byte-identical |
| `CHANGELOG-through-2026-08-11.md.verify.sh` | v1.1.3 | OK |
| `HANDOFFS-through-2026-08-11.md.verify.sh` | v1.1.3 | OK |

**Not caused by S87's trims, and that is measured rather than assumed.** All four fail identically
in a detached worktree at `8a22608` (S86's tip, before this session's first commit) — run
`git worktree add --detach <dir> 8a22608` and execute them there to reproduce. S87's own two proofs,
written by v1.1.3, pass.

**What is known, and where the diagnosis deliberately stopped.** The generator version correlates
perfectly (all four v1.1.1 fail; both v1.1.3 pass), which points at the defect class BL-27 and BL-28
already fixed in v1.1.2/v1.1.3 — but correlation is not the cause and this item does not assert one.
The obvious competing explanation — *"a later trim moved records out from under an older proof"* —
is **unlikely on inspection**: each script resolves `TRIM_SHA` via `git log --diff-filter=A -1` and
then reads `show(TRIM^, LIVE)`, `show(TRIM, LIVE)`, `show(TRIM, SHARD)`
(`docs/archive/CHANGELOG-through-2026-08-02.md.verify.sh:156-158`), so its whole derivation is frozen
at its own trim commit and is not a function of HEAD. Excluded, not disproved.

**Why it matters more than a red script.** These are the artifacts that discharge Learning #15 — the
reason the trimmer is trusted to move records at all. A proof that fails is indistinguishable, to a
reader, from records that were actually lost; the archives may well be perfectly intact, and nobody
can currently demonstrate it from the shipped artifact. Note also that the two *newest* proofs pass,
so a session that checks only what it just wrote — as S87 did first — sees green and moves on.

**Next session:** determine whether the four shards' content is genuinely intact (re-derive
independently) and whether the fault is in the v1.1.1-generated scripts or in the archives
themselves. Those are different repairs: regenerating a stale proof is cheap, and actual record loss
is not. Do not regenerate the scripts before answering that question — a regenerated proof over lost
content would pass, and would destroy the only evidence that anything is wrong.

**ANSWERED 2026-08-15 (S88) — the archives are INTACT; the fault is entirely in the proofs. Still
open as a repair decision.** Full audit: [`docs/audits/2026-08-15-bl36-archive-losslessness.md`](../audits/2026-08-15-bl36-archive-losslessness.md).

- **No loss, measured independently.** A re-derivation keyed on record *identity* rather than
  position finds **0 records missing** across all six trims, and **0 of 228** historical record
  identities unreachable at HEAD (live + all 9 archives). All six trimmer-declared counts (10, 70,
  68, 16, 30, 25) reproduce exactly. The detector was mutation-proved able to fail first (deleted /
  altered / truncated shard records all detected; silent on the real artifact).
- **Root cause — `injected = 1 if trims_the_ledger else 0`** (`starter-kit/methodology_trim.py:1715`,
  `:1736`). It is a **0/1 flag**, not a count of records the trim commit adds, so the generated
  proof's positional identity breaks *by construction* on any trim commit bundled with other edits
  to the same ledger. All four failures are that shape: two extra records (`73!=72`), three
  (`77!=75`), and a frontier receipt finalized `pending → complete` in the trim commit (`record [0]`).
- **The version correlation in the table above is a CONFOUND, and the repair depended on catching
  it.** Every failing shard came from a *bundled* trim and every passing one from a *standalone*
  trim, so version and commit-shape are collinear across the six shipped artifacts. Running the
  off-diagonal cells settles it: **v1.1.3 logic fails all four bundled trims with identical text**,
  and v1.1.1 logic *passes* the standalone `CHANGELOG` trim. There are two independent defects —
  **A: bundling** (present in every version, causal, and deliberately kept a loud FAIL by BL-27's own
  fix 2) and **B: the regenerated front-matter count line** (genuinely fixed v1.1.1 → v1.1.3).
- **Regenerating the four proofs is NOT the repair** — measured, not predicted: the current
  generator's logic still fails all four. The repair is Defect A (make `injected` a measured count),
  or a protocol rule that a trim commit touches nothing but the trim. Both need their own
  operator-gated session against a distributed tool; neither was taken here (FM #17).
- **This was already answered once.** BL-27 — now archived to
  [`BACKLOG-archive-2026-08-15.md`](BACKLOG-archive-2026-08-15.md), and in this file at `:975` when
  S87 raised BL-36 past it — documents this exact trigger, states *"This is not evidence of
  historical data loss"*, and predicted this re-raise verbatim. It was not found because this file
  was **1,518 lines / 134,759 B** — 2.06× the ledgers' own 65,536 B budget — and no reduction step
  reached it, which is **BL-32**, still open. That link now has a cost attached. **S89 ran the
  reduction** (a third of the file; exact before/after figures are in `CHANGELOG.md`'s `[BL-32]`
  entry — this file deliberately does not state its own byte size, because writing that number in
  changes it) and it did not close the gap: with every closed item archived, and measured before
  that session added anything of its own, the 16 inherited *open* items already totalled **68,195 B,
  1.04× the 65,536 B budget**. So the remaining excess is not deferred housekeeping — it is the open
  work itself, and reaching a ceiling here means compacting live items, which is a separate
  decision. Re-derive rather than trust any of it: `wc -c docs/planning/BACKLOG.md`.

**BL-37 — this repo ships a size-ceiling gate to every adopter and does not run it on itself; and
the ceiling list it ships has no `BACKLOG.md` entry.** *Raised 2026-08-15 (S89), found while
reducing `BACKLOG.md` and looking for that file's DECLARED ceiling. Measured, not fixed (FM #17):
both halves change distributed artifacts or this repo's own root config, and neither is a
reduction.*

**Half one — the gate does not run here.** `bin/_manifest.py:54` and `:60` distribute
`starter-kit/context_budget.py` → adopter `context_budget.py` (TRACKED) and
`starter-kit/context-budget.json` → adopter `.context-budget.json` (SEED). This repo has **no
`.context-budget.json` at its own root** (`find . -name '.context-budget.json' -not -path
'./.git/*'` → nothing), so the FM #28 gate authored here has never been run against the repo that
authors it. That is the same shape as **BL-29** and upstream
[issue #59](https://github.com/KJ5HST/methodology/issues/59) — a tool correct for every installed
copy and blind at home — arriving through configuration rather than through path resolution.
Note the asymmetry that makes it easy to miss: `bin/tests.sh` proves the gate *installs* correctly
(13 passing rows: hook honouring `core.hooksPath`, seed parses, over-ceiling exits 2, re-sync does
not clobber). Nothing asserts it is *configured here*, and an unconfigured gate is silent, not red.

**Half two — the shipped ceiling list has no backlog entry.** The seed's `files` array covers
`CLAUDE.md` (resident), `SESSION_NOTES.md` (read-mandated) and an optional `LEARNINGS.md`
(on-demand). `BACKLOG.md` is absent, in a framework whose `SESSION_RUNNER.md` Phase 0 step 3 names
it as the documented fallback for current priorities — *"Fall back to `BACKLOG.md` if no repo
exists"* — which makes it the mandated Phase 0 read for any adopter without a repo, and states in
the same breath that it *"should contain only open work items."* It is the file class that just
cost a session (BL-36 raised past its own answer), and this session's own measurement says its
excess cannot be archived
away — after moving every closed item out, the open items alone are 68,195 B. A ceiling for it is
therefore a *policy* question about how much open work a backlog may hold, not a housekeeping one,
which is exactly why it wants an entry with a defended number rather than a default.

**Not decided here:** whether the right move is (a) provision `.context-budget.json` in this repo
from the seed and calibrate it (fork-side, no distributed file, runnable today); (b) add a
`BACKLOG.md` entry to the distributed seed (DISTRIBUTED — ships upstream, needs a go-ahead); or
both, in that order. (a) is a precondition for arguing (b) from a measurement rather than a guess.

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
| **BL-35** | `starter-kit/FRAMEWORK_LEARNINGS.md` rows 18 and 19 were malformed 2-column rows | ✅ **FIXED** 2026-08-11 (S84). Live since S40/S41; found by `bin/check-learnings` arriving via S83's upstream merge; the two missing cells recovered by git archaeology on the rows' authoring commits (`11b843a`, `12463dd`) and approved before writing. Distributed to adopters at their next `bin/sync`. |

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
