# Operational Backlog — item detail (fork-only)

**The read-on-demand half of [`BACKLOG.md`](BACKLOG.md).** That file is read at every Phase 0
(SESSION_RUNNER.md step 3, for current priorities) and carries a 65,536 B FM #28 ceiling; this
one is opened only once a session knows which item it is working on, and carries no ceiling.
Same split, same reason, as `CLAUDE.md` → [`docs/RELEASE_HISTORY.md`](../RELEASE_HISTORY.md).

**Fork-only.** Not part of the canonical framework, not in `bin/_manifest.py`, not in any
upstream PR — same status as its parent.

**Bodies below are VERBATIM as they stood in `BACKLOG.md` at `384b17c`.** They were moved, not
edited: no rewording, no compaction, no dropped items. That is machine-checkable —
[`BACKLOG-DETAIL.md.verify.sh`](BACKLOG-DETAIL.md.verify.sh) re-extracts each item from git by
its own `BL-N` identity and compares bytes. Run it rather than trusting this paragraph.

**Editing rule: this file is the one place an open item's text lives.** Edit the body here and
the one-line summary in `BACKLOG.md`'s index only if the item's *subject* changed. Closing an
item still means removing it from here, adding its pointer row to `BACKLOG.md`'s
§Completed items, and logging the action in [`CHANGELOG.md`](../../CHANGELOG.md).

**The `<a id="bl-N">` anchors are the record separators** the proof splits on, and the targets
`BACKLOG.md`'s index links to. They are scaffolding added by the move; every byte below one,
up to the next, is original.

---

<a id="bl-11"></a>

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

<a id="bl-12"></a>

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

<a id="bl-13"></a>

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

<a id="bl-14"></a>

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

<a id="bl-17"></a>

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

<a id="bl-18"></a>

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

<a id="bl-19"></a>

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

<a id="bl-20"></a>

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

<a id="bl-21"></a>

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

<a id="bl-22"></a>

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

<a id="bl-23"></a>

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

<a id="bl-26"></a>

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

<a id="bl-30"></a>

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

<a id="bl-31"></a>

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

<a id="bl-32"></a>

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
`date_of_record` callable — a REQUIRED positional parameter of `LedgerSpec.__init__`
(`starter-kit/methodology_trim.py:136`, stored at `:144`, and supplied by both shipped specs at
`:168` and `:194`) — and `evaluate()`
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

<a id="bl-36"></a>

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

**REPAIRED 2026-08-16 (S93) — Defect A is fixed in `methodology_trim.py` v1.2.0. THIS ITEM NOW
COVERS ONLY ITS OPEN RESIDUAL: the four frozen `.verify.sh` artifacts already shipped.** The
heading and the diagnosis below are kept verbatim as the record of how it was found (same
convention as BL-20's).

- **What changed.** The generated proof no longer carries `INJECTED` at all. The records a trim
  commit introduced are measured at verification time from record **content** — those present in
  `after + shard` and absent from `before` — and removed occurrence-wise, in order, before L1/L3
  run. L1/L2/L3 keep their names and their exact semantics. This is Defect A's repair stated as
  rec 2 asked ("a measured count"), done **by content rather than by position**: measuring it
  positionally would derive the operand from the very difference L1/L3 assert on, which is an
  identity that cannot fail (Learning #16). `:1736`'s in-memory `injected` is deliberately
  **unchanged** and now carries a comment saying why — there the count is a fact the tool owns,
  not an inference about a commit.
- **Measured against the six real shards, not predicted** (replayed read-only; `docs/archive/`
  untouched): `CHANGELOG-through-2026-08-02` and `-08-09` **go from FAIL to PASS**, naming the 2
  and 3 records their commits added. The two already-passing proofs still pass. The two
  `HANDOFFS` proofs **still FAIL, correctly** — each trim commit finalized its own frontier
  receipt, so that record's pre-trim bytes exist nowhere afterwards. They now report
  `MISSING: session: S61` / `S64` beside the added twin and the BL-27 note, instead of
  `L3 record [0] not byte-identical`.
- **Audit Finding #4 is dissolved rather than extended.** The note that never fired for a bundled
  `CHANGELOG` trim is moot: that shape is no longer a failure at all.
- **Verified on three surfaces**, since the file is DISTRIBUTED: the canonical suite
  (`tools/test_methodology_trim.py` 103/103, six new RED-first tests), the six real shards above,
  and a fresh `bin/sync` adopter tree where a bundled trim proves lossless end to end and a
  pre-commit shard tamper still goes red naming its victim.

**OPEN RESIDUAL — the four frozen proofs, and the operator's recorded decision.** No change to a
generator can reach an artifact that is already frozen, so the four shipped `.verify.sh` files
still say what they said. Operator decision 2026-08-16: **decide now, execute in a separate
session** — regenerating four archive artifacts is a second capability, not a layer of this one.
The disposition now has measured numbers behind it, which it did not when S88 posed it:
regenerating under v1.2.0 takes the four from **4 red to 2 red**, and the 2 that remain are red
for a true reason a reader can act on. Recommended disposition, for that session to confirm:
regenerate all four under v1.2.0 and state in each shard's front matter that the proof was
regenerated on that date and is no longer the artifact originally shipped — this is a deliberate
exception to the archive freeze rule (`starter-kit/HANDOFFS.md` §Size, and when to archive) and
needs its own go-ahead. **The two that stay red want the protocol rule, not more code:** audit
rec 3 — a trim commit touches nothing but the trim — is the only thing that removes their cause,
and it is still untaken (FM #17).

Full audit: [`docs/audits/2026-08-15-bl36-archive-losslessness.md`](../audits/2026-08-15-bl36-archive-losslessness.md).

**ANSWERED 2026-08-15 (S88) — the archives are INTACT; the fault is entirely in the proofs.**

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

<a id="bl-37"></a>

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

> **HALF (a) IS DONE — S90, 2026-08-15.** `.context-budget.json` provisioned at this repo's root
> and calibrated; figures and derivations in `CHANGELOG.md`'s `[BL-37]` entry and in the config's
> own `_` keys. Run it with `python3 starter-kit/context_budget.py` — **there is no root copy of the
> tool here**, which is itself a finding: `install-hook` would write a hook exec'ing a
> `context_budget.py` that does not exist at this root, and this clone's `core.hooksPath=.githooks`
> `pre-commit` is the FM #27 ledger gate, so the budget gate **measures here, it does not block.**
> Wiring it into `.githooks/pre-commit` edits a canonical file that ships upstream — not taken.
>
> **What (a) measured, which is what makes (b) arguable:** `HANDOFFS.md` (72,449 B) and this file
> (91,857 B) both report `over` the 65,536 B ceiling on the first run, exit 2. Both pre-existing;
> `HANDOFFS.md` is independently corroborated by `methodology_trim.py --check` (`trigger FIRES`, same
> byte count), and this file's excess is S89's finding that the *open* items alone are 1.04× the
> ceiling. **Half (b) is still open and still needs a go-ahead** — it edits the distributed seed.
>
> **Two further findings from (a), neither fixed by (a) (FM #17):** the `calibrate()` defects became
> **BL-38**, since **CLOSED** — see §Completed items. And the seed's `synced` block is
> *meaningless in the canonical repo* — it
> drift-checks an adopter's copy against a canonical checkout elsewhere, and this repo **is** that
> canonical, so the naive adaptation (`path` and `canonical` pointing at the same file) would
> `git hash-object` one blob twice and compare it to itself: an identity no change can falsify.
> `synced` is therefore deliberately `[]` here, with the reason recorded in the config's `_synced`
> key. The inversion has a second half worth a decision someday: the seed never size-checks synced
> files *because an adopter may not edit them*, but here they **are** editable, so a size finding
> **would** be actionable — and `starter-kit/SESSION_RUNNER.md` is 52,386 B and
> `starter-kit/SAFEGUARDS.md` 15,386 B, both mandated reads at every adopter's Phase 0. Declaring
> ceilings for them is framework policy that ships upstream, so it was measured and left.

<a id="bl-39"></a>

**BL-39 — issue #75's two *Related* items: carry the named surface forward into close-out.**
Raised 2026-08-15 by S92, deliberately out of that session's scope rather than forgotten.
S92 answered [issue #75](https://github.com/KJ5HST/methodology/issues/75) at **plan time** —
`starter-kit/SESSION_RUNNER.md` §Per-Phase Completion Criteria now requires each phase to name the
surface its DONE criterion is demonstrated on, and the Planning Session Checklist verifies it. The
issue also offered two counterparts as prior art, explicitly *not* as an ask, and both are about
what happens at the **other** end — whether the named surface survives into the record a successor
actually reads:

1. **Phase 3E** (`starter-kit/SESSION_RUNNER.md`) asks *did you runtime-verify?* and never *can this
   surface fail?* Its only surface-shaped clause covers verification being **impossible** ("requires
   hardware, external service, CI — state this explicitly"), which is a different question from a
   verification that ran somewhere it could not fail. Same gap in the flight manual:
   `ITERATIVE_METHODOLOGY.md:287-288` (Phase 6 step 2) and Quality Gate 8 (`:432`, *"Have I run the
   code and verified it works?"*).
2. **`runtime_smoke`** in the receipt (`starter-kit/HANDOFFS.md:62`) is documented as
   `<a run result, or "n/a — docs-only", or "impossible: <reason>">` — no surface slot. Leading with
   `simulator:` / `device:` / `impossible: …` is purely mechanical and makes a claim like #75's
   visibly incomplete beside a gate that says "real hardware."

**Why it was split rather than bundled.** The plan-time line bites without either: the plan names
the surface, the executor inherits it. These touch **two further distributed files** plus the
flight manual, and (2) changes a documented field format that adopters' existing receipts were
written against — a compatibility question S92's change does not have. Not blocked, not deferred
for cause; sequenced.

**Do not re-derive the disposition of `README.md:713`.** It says the Planning Session Checklist is
*"5-item"* and the checklist is now 7. It is **correct as written**: it sits under
**"### What's New in v1.2"**, frozen release notes where 5 was the count as shipped. Editing it
would falsify the history, and it is not a live claim. S92 verified the heading before leaving it.


<a id="bl-42"></a>

**BL-42 — `methodology_trim.py` still generates the fat pointer block the S109 compaction just
removed. Raised 2026-08-25 (S109), found while doing Phase 2, deliberately not fixed.**

`build_pointer_block` (`starter-kit/methodology_trim.py:935`) emits a 3-line ~447 B block and
`insert_pointer` (`:944`) places it at the end of front matter. S109 collapsed the 8 accumulated
blocks into one table (~190 B/row), so **the next trim of `HANDOFFS.md` re-appends a block in the
old format** and the front matter carries two formats at once. An HTML comment in the front matter
tells that session to fold it in by hand, which works but is a human step that silently stops
happening (Learning #12).

**Why it was not fixed here.** The file is **DISTRIBUTED** (`bin/_manifest.py` ships it to adopter
roots), so the fix lands upstream and needs the operator's go-ahead. The ratified plan's §7 put
`methodology_trim.py` and "anything distributed" out of Phase 2's scope while §6 asked for the
compaction — a **scope collision inside the plan itself**, recorded there too.

**Shape of the fix, for whoever takes it:** the pointer region wants to be a `LedgerSpec`-declared
*regenerated* field — the trimmer already regenerates the receipt-count sentence — so the table is
rebuilt from the shard inventory each trim rather than appended to. That also fixes the count
sentence's drift for free. Runnable fork-side up to the PR.

<a id="bl-43"></a>

**BL-43 — six `bin/tests.sh` assertions flake under `pipefail`. Raised 2026-08-25 (S109),
diagnosed, not fixed.**

Two runs of `bin/tests.sh` on an identical clean tree gave **278/2/0** then **279/1/0**. The
non-reproducing failure was Test 38 assertion (5). It is a **race, not a regression**:
`bin/tests.sh:5` is `set -uo pipefail`, and `echo "$(producer)" | grep -q PAT` lets `grep -q` exit
at the first match, so `echo` can take SIGPIPE and the pipeline is scored **failed even though the
pattern matched** (Learning #34).

**Population enumerated, not sampled:** `:2591`, `:2596`, `:2605`, `:2620`, `:2864`, `:2880`.
**All six are on the `&& pass || fail` polarity, so each fails NOISILY** — none is in the
dangerous `&& fail || pass` direction that would assert nothing and read green. That is why this
is a nuisance rather than a hole, and why it was recorded rather than swept into S109's scope.

**The fix is already in this file**: Test 38 section (8) capture output into a variable first and
say why. Apply the same to all six. **Each needs its own proof that it still fails when it should**
— a capture that silently stops asserting is exactly the failure being fixed — which is what makes
this a session rather than a one-line sweep.

<a id="bl-44"></a>

**BL-44 — `bin/check-learnings` reports a range it has not measured. Raised 2026-08-25 (S109).**

`bin/check-learnings:330` prints `"%d Learning row(s), contiguous 1..%d"` with `len(rows)` for
**both** operands. The table reserves `#14`, so the rows are 1..38 with a deliberate gap and the
tool reports **"37 rows, contiguous 1..37"**. The contiguity *check* is correct — it models the
reserved gap — only the success message is wrong.

**It is not cosmetic: it has already contaminated a durable record.** S108's receipt states
`check-learnings OK (36 rows, contiguous 1..36)` **and** "I discharged one of mine (#37)" in the
same block, because the tool's own summary contradicted the file. A reader trusting the summary
concludes the newest Learning is one lower than it is, and cites the wrong number.

**Fix:** report the observed maximum and name the reserved gap, e.g.
`37 row(s), #1..#38, 1 reserved (#14)` — derived from the parsed numbers, never from `len(rows)`.
Canonical-only (`bin/check-learnings` carries no `bin/_manifest.py` row), so no adopter impact and
no upstream action.

<a id="bl-45"></a>

**BL-45 — `starter-kit/FRAMEWORK_LEARNINGS.md` is 16 B from its ceiling. Raised 2026-08-25 (S109).
This blocks Phase 3C for the next session.**

**65,520 B against a 65,536 B ceiling.** The 37 rows are ~97% of the file; prose is under 2 KB, so
there is nothing else to reclaim. `ROW_BUDGET_BYTES` is 1,500 and the median row is ~1,971 B, so
**no budget-conforming row fits** — S109's own was written to 981 B specifically to fit the
remaining 997, and consumed it.

The table is **append-only and `CLAUDE.md` forbids renumbering**, and rows are cited across the
distributed corpus, so the ledger trimmer's shard-and-pointer pattern does not transfer unchanged:
archiving row #7 breaks every `Learning #7` citation unless `check-learnings`' citation sweep
learns to resolve into the shard.

**This is Learning #35's own shape** — two limits set independently on one artifact multiplying
into a constraint nobody checks — arriving in the file that records it.

**Options, none costed yet, and the choice is the operator's:** (a) archive oldest rows into a
shard plus citation-resolution in the checker; (b) raise the ceiling, which is measured and would
need re-deriving; (c) compact frozen rows in place, which edits an append-only record; (d) split
the table by theme. **Decide before the next session's Phase 3C, because that session cannot
discharge it.**

**✅ CLOSED 2026-08-26 (S114) by option (b), the operator's decision from the four costed below.
Ceiling `65,536 → 73,728 B` (72 KiB), and the five-session Phase 3C backlog discharged — rows
#39–#42 written, 968–1,148 B each. The file is 69,683 B against 73,728: `ok`.** The change is
**canonical-only** — the distributed seed declares `CLAUDE.md`, `SESSION_NOTES.md`, `LEARNINGS.md`
and **not** this file, so no adopter is affected.

**⚠ TWO STATEMENTS ABOVE ARE WRONG AND ARE LEFT STANDING (FM #17); the corrections are here.**

**(i) "archiving row #7 breaks every `Learning #7` citation" overstates it by ~59×.**
`bin/check-learnings`' citation sweep covers the **distributed corpus only** — measured, that is
**8 citations to 5 rows across 4 files** (`AUDIT_WORKSTREAM.md` 3, `SESSION_RUNNER.md` 2,
`methodology_dashboard.py` 2, `ITERATIVE_METHODOLOGY.md` 1). The 471 citations that exist overall
live in ledgers, plans and **frozen archives**, which must not be edited anyway. So option (a) needs
**no checker work at small N**: archiving the oldest **5** rows orphans **zero** distributed
citations; the oldest **10** orphans **five, in two files**, fixable by hand.

**(ii) The ceiling was never "measured" — it was borrowed.** 65,536 came from the ledgers'
`DEFAULT_BUDGET_BYTES`, and the note defending it converted to tokens at `bytes_per_token` 2.80
against an **opening-context** floor. Both wrong: that estimator answers a different question
(S112 measured its own `--calibrate` at 2.46, R² 0.59), and the binding limit is the **25,000-token
Read cap**. Its arithmetic gave 23,406 tok where the measured figure is **21,623** — **8% over, in
the direction that made the ceiling look tighter than it was.**

**The four options, costed [M], so the three unused ones need not be re-derived:**

| | option | frees | buys | cost |
|---|---|--:|--:|---|
| **(b) raise** ✅ | to a margin below the measured one-read cliff (75,751 B) | **8,192 B** | ~5 rows | edits no row, breaks no citation. **Taken.** |
| **(a) archive** | oldest 5 / 10 / 15 / 20 rows | 2,580 / **7,589** / 17,063 / 28,812 B | 1 / 5 / 11 / 19 rows | **0 / 5 / 7 / 8** distributed citations orphaned |
| **(c) compact** | the 20 rows over the 1,500 B row budget, to 1,500 each | **17,533 B** | ~11 rows | **edits an append-only record** — a policy change |
| **(d) split by theme** | — | — | `Learning #7` stops being unambiguous. **Advise against.** |

**What none of them fixes, and it is Learning #26's own shape arriving in the file that records it:**
the 37 pre-existing rows are **97% of the file** and may not be edited, so the untouchable remainder
**is** the file and no reduction step can reach it. The real question is policy — *how many learnings
should the framework carry before old ones retire?* — and no ceiling answers it. **Re-open when the
~3 remaining rows are spent**, which is S97's own instruction, now inherited.

<a id="bl-46"></a>

**BL-46 — an adopter's trimmer has been inert since bootstrap, and nothing detected it. Raised
2026-08-25 (S109) from a cross-repo measurement.**

`../vscode_quarto_ext` has `methodology_trim.py` installed and **zero** archive shards. Its
`HANDOFFS.md` is **1,780,187 B — 27x the 65,536 B ceiling** — and `--check` refuses to parse it:

```
[ZONE_UNCLASSIFIED] HANDOFFS.md declares footer_mode='none', but line 3762 is a standalone '---'
```

The line is the **bootstrap seed sentinel** — `<!-- Receipts go below, newest on top. Delete the
seed-sentinel line above when you add the first one. -->` — never deleted at setup. The tool has
been correctly refusing to guess ever since, and nobody was reading its output.

**Two separate items, and only the first is that repo's.** (1) Delete the sentinel there and run
the overdue trims — that repo's work, not this one's. (2) **The framework defect:** the seed
instructs the adopter to delete the line and **nothing checks that they did**. `bin/check-handoff`
validates receipts, not the seed's own removal. A one-line check — a live `HANDOFFS.md` containing
the sentinel text alongside a real receipt is a bootstrap that did not finish — would have caught
this at that repo's first close-out instead of 216 receipts later. That half touches distributed
files and needs a go-ahead.

**Context:** the same sweep found `nprcgenekeepr` (218,298 / 286,154 B) and `wsfct` (74,180 B)
firing their triggers with the tool installed and unrun. This repo is the only one of four under
the ceiling. See `CHANGELOG.md`'s S109 entries for the full four-repo table.

> **HALF (1) IS DONE — `vscode_quarto_ext` S254, 2026-08-26.** The operator directed that repo to
> trim; it deleted the footer and ran both overdue trims. `CHANGELOG.md` **831,830 → 44,190 B**
> (230 records archived), `HANDOFFS.md` **1,801,150 → 52,850 B** (211 receipts). Both triggers now
> stand down. Losslessness was established four ways, one of them a four-lens pass tasked with
> refuting it. **Two findings that repo hit are filed here as BL-48 and BL-49; a third, BL-47, came
> from installing the budget tool afterwards.**
>
> ⚠ **THE DIAGNOSIS IN THIS ITEM IS RIGHT BUT THE REMEDY IS NARROWER THAN THE DEFECT.** This item
> says the adopter *"never deleted"* the sentinel. They **did** delete it — `METHODOLOGY-SEED-SENTINEL`
> was already absent from that repo — and the trimmer still refused, because what actually blocks it
> is the **trailing `---` and the comment beneath it**, which the seed's own instruction never
> mentions. `starter-kit/HANDOFFS.md` carries the sentinel at **line 20** (front matter) and the
> instruction at **line 160** (last line), and the instruction says only *"Delete the seed-sentinel
> line above"*. **An adopter who follows it exactly still ends up with an inert trimmer.** So the
> proposed one-line check — *"a live `HANDOFFS.md` containing the sentinel text alongside a real
> receipt"* — **would not have fired on `vscode_quarto_ext`**, because the sentinel was gone and the
> footer was not. Either the seed must instruct removal of the separator and comment too, or the
> detector must key on the trailing footer rather than the sentinel.


**BL-47 — the seed `context-budget.json` omits the two ledgers `methodology_trim.py` exists to bound.
Raised 2026-08-26 from `vscode_quarto_ext` S255.**

`starter-kit/context-budget.json` governs `CLAUDE.md`, `SESSION_NOTES.md` and `LEARNINGS.md`. It
does **not** list `CHANGELOG.md` or `HANDOFFS.md`. This repo's own `.context-budget.json` does — at
`max_bytes: 65536`, the **same constant** `methodology_trim.py` budgets to.

So an adopter who bootstraps by the book gets no gate on the two files the sibling tool exists to
bound, at a number both tools already agree on. That is the precise gap BL-46 is about, one level
up: BL-46 asks why nobody read the trimmer's output, and the answer is that the thing which would
have made them read it was not in their config. `vscode_quarto_ext` had `methodology_trim.py` since
S188 and `context_budget.py` **not at all** until S255 — 66 sessions, `HANDOFFS.md` at 27x, no
signal anywhere in Phase 0.

**Proposed:** add both to the seed at 65536 with `_` keys explaining that the number is shared with
the trimmer deliberately, so `context_budget.py` REPORTS what `methodology_trim.py` would ACT on.
Distributed file — needs a go-ahead.

**Update, 2026-09-14 (S161 follow-up): the premise has moved twice — re-decide before acting.**
This repo's `.context-budget.json` no longer lists `CHANGELOG.md`: the operator removed it
(`3c8acd5`) because sessions reach the ledger through git and never read it whole (BL-52's fourth
addendum). It still lists `HANDOFFS.md` at 65,536 B. And *"the same constant `methodology_trim.py`
budgets to"* stopped being true at S116, when the trimmer's budget went to 196,608 B, deliberately
decoupled from this config. Shipping both ledgers in the seed at 65,536 B would now give adopters a
`CHANGELOG.md` gate this repo has just decided it does not need.

**Update, S162 (2026-09-14): the `CHANGELOG.md` half is settled by decision.** BL-57's plan
([`changelog-rules-contradictions-plan.md`](changelog-rules-contradictions-plan.md), Q2 A: archiving is
optional, and the ledger is never read whole) makes a `CHANGELOG.md` entry in the seed
`context-budget.json` wrong on its own terms, so none will be added. The `HANDOFFS.md` half stays open
(the plan's D7).

**BL-48 — the seed `HANDOFFS.md` lacks the count sentence its own `LedgerSpec` declares, so every
adopter gets `FRONTMATTER_FIELD_ABSENT` forever. Raised 2026-08-26 from `vscode_quarto_ext` S254.**

`LEDGERS["HANDOFFS.md"].regenerated` declares one field, keyed to
`(This file currently holds \*\*)(\d+)(\*\*)`. **`starter-kit/HANDOFFS.md` contains no such
sentence** (`grep -c "currently holds" starter-kit/HANDOFFS.md` → `0`). This repo's own root
`HANDOFFS.md` does have it, so the mismatch is invisible from here and hits only adopters.

Every trim an adopter runs therefore reports:

```
[FRONTMATTER_FIELD_ABSENT] declared regenerated field 'retained receipt count' not found in front
matter — its value cannot be kept true. Add it, or remove it from the config.
```

A declared-but-absent field is a config that cannot be satisfied by the artifact it describes.
`vscode_quarto_ext` fixed it locally at S254 by adding the sentence (not by editing the synced
tool). **Proposed:** ship the sentence in the seed. Distributed file — needs a go-ahead.

**BL-49 — `content_probe` is consulted only when the record count is ZERO, so a partial grammar
mismatch is invisible and gets frozen into a shard. Raised 2026-08-26 from `vscode_quarto_ext` S254.**

`content_probe` is documented as *"Evidence that entries EXIST in a grammar this config cannot
read."* It is referenced at exactly **one** call site — `classify_empty`, the zero-record path
(v1.1.1:1365, v1.3.0:1559). When a file has records, a **partial** mismatch is never tested.

**Measured consequence, on a shard that is now frozen.** `vscode_quarto_ext`'s `CHANGELOG.md`
holds **236** dated `###` headings but only **230** match `^### \d{4}-\d{2}-\d{2} · \[` — the six
earliest entries predate that project's source-tagging convention. Those six are not record starts,
so they ride inside the oldest tagged record's span. Bytes move intact and **every L1/L2/L3
assertion passes** — but the computed span is wrong, and it is published in four places: the shard
`h1`, the shard's own "Holds N record(s)" sentence, the live pointer block, and the archive index.
The shard is named `through-2026-08-24` and labelled from `2026-06-30`; its true oldest entry is
**`2026-06-27`**.

⚠ **A byte-level losslessness proof cannot see this, because nothing is lost.** Only the
*description* is wrong — and the description is the index people search.

**Proposed:** on every run, compare probe hits against matched records and report the delta as a
finding when they disagree (`GRAMMAR_COVERAGE`), before anything is frozen. The instrument already
exists; it is simply not consulted on the path where records are present.

<a id="bl-50"></a>

**BL-50 — `insert_pointer` injects a byte `L2`'s reversal never removes, so the trimmer refuses a
correct trim. Raised 2026-08-26 (S110), hit while running the close-out trim.**

`insert_pointer` (`starter-kit/methodology_trim.py:940-950`) appends the pointer block like this
when the front matter has no standalone `---`:

```python
return front + ("\n" if front and not front.endswith("\n\n") else "") + block
```

`L2`'s confinement proof (`:582-586`) reverses the declared changes by removing the block —
`residue.replace(block, "", 1)` — and **never removes that injected `"\n"`**. So the reversal
cannot restore the original bytes, and the run dies with:

```
[L2_FRONTMATTER_UNDECLARED] the FRONT MATTER changed outside the declared regenerated fields and
the pointer block ... (first residual difference at char 6126)
```

**Reproduced in isolation** (S110): `front.endswith("\n\n")` is `False`, and simulating the
insert-then-reverse yields `front + "\n"` with the first difference at char 6126 — the tool's own
number. **Nothing is corrupted; the proof is reporting its own insertion as an undeclared change.**

**Why it became reachable only now.** Before S109's compaction the front matter ended with a
generated pointer block, and `build_pointer_block` returns text ending `"\n\n"` — so the guard
never fired. S109 folded those blocks into a table, leaving the front matter ending `-->\n`. **The
very next trim hit the refusal.** This is a fork-side compaction exposing a latent defect in a
**distributed** tool, so every adopter whose front matter ends in a single newline is equally
blocked, and the failure reads as *data loss* when there is none.

**This is Learning #37 one level down** — a losslessness proof that models the population and the
declared growth but not the producer's full transform — and Learning #16's *"wire the assertion to
the artifact"* seen from the other side: here the checker is correct and the **producer** is what
the checker was not told about.

**Worked around at S110, not fixed:** a one-byte fork-side data edit (a blank line at the end of
`HANDOFFS.md`'s front matter) restores the condition the tool was written for. **A standalone `---`
would be the tool's preferred anchor and is the wrong fix** — it trips `[ZONE_UNCLASSIFIED]`, which
is BL-46's exact failure mode.

**Proposed:** make the reversal symmetric with the insertion — have `insert_pointer` return the
separator it injected (or have `L2` strip a single leading `"\n"` from the block's span), and add a
mutant whose front matter ends in one newline. **Distributed file — needs a go-ahead.** Batches
naturally with BL-42, which is about the same function.

<a id="bl-51"></a>

**BL-51 — the `2,000-line agent read cap` premise is false, and it is distributed. Raised
2026-08-26 (S110). PHASE A SHIPPED (S111). PHASE B SHIPPED (S112). PHASE C OPEN — the item stays
open for it.**

Full analysis and phased remedy:
[`read-cap-premise-correction-plan.md`](read-cap-premise-correction-plan.md) — **RATIFIED**, with
**§11 recording Phase A** and **§12 recording Phase B**. This row exists so the work appears in the
open-item index; the plan is the artifact, and §12.4 is what a Phase C session should read first.

**Phase B (S112) moved the numeral and deleted a rule.** `READ_CAP_LINES` is gone from both
distributed tools; the threshold is now `READ_CAP_BYTES = READ_CAP_TOKENS x MIN_BYTES_PER_TOKEN`
= **56,750 B**, derived at import so no opaque boundary is published, plus a second measured
boundary `READ_REFUSE_BYTES = 262,144` past which a default read returns **no content at all**.
`LINE_FIRE_BELOW`/`LINE_STOP_ABOVE` were **removed, not re-tuned** — the rule is unsatisfiable at
every honest cap (a one-read `CHANGELOG.md` holds 20.9 records, a one-read `HANDOFFS.md` 4.3,
against a rule demanding 30 of headroom). J3 keeps 2000 as `SEED_PLAUSIBLE_MAX_LINES`. Fleet
effect, measured read-only against all four adopters: read-cap risk rows **3 -> 14**, spreading
from one repo to all five, **five of them the zero-content refusal**. Details and the eleven
first-hand measurements are in the plan's §12.

**Three figures in the paragraphs below are known-wrong and are deliberately NOT edited (FM #17);
§12.3 carries the corrections.** *"cliffs near line 690"* and *"~2.9x too permissive"* were measured
on `CHANGELOG.md` content only — per ledger it is 2.32x and **8.75x**. And the "do not just fix the
number" paragraph is right but understated: the degeneracy is not specific to a *corrected* cap.

Measured (probes reproduce in that plan's Appendix A): the cap is **~25,000 tokens**, not 2,000
lines; truncation is **announced** with a full banner, not silent; and at this repo's ledger density
a Read cliffs near line **690**, so `READ_CAP_LINES = 2000` is ~**2.9x** too permissive.

Three carriers are `TRACKED` (a fix reaches existing adopters); **two ledger seeds state the claim as
doctrine in a table and are `SEED`**, so a fix there reaches **future adopters only** — the same
defect class as BL-46/47/48, which is why this batches with them.

**Do not "just fix the number":** `LINE_FIRE_BELOW`/`LINE_STOP_ABOVE` are denominated in records of
headroom to the cap, and `choose_cut` falls through to `return 1` when nothing satisfies `stops()` —
so a corrected cap alone would make every adopter's next trim retain **one record**. Every existing
test stays green. See the plan's §3.

<a id="bl-52"></a>

**BL-52 — the line metric measures a condition that trimming may not remedy. Raised 2026-08-26
(S111), from a critique the operator relayed from a `../model_project_constructor` session.**

**The argument, and it follows from S111's own probes rather than from the relay.** Truncation is
**ordered top-down** (probe B delivered lines 1–10 of 101; probe C's prefix was lines 1–700 of
2,000) and both ledgers are **newest-on-top**. So the records a cut removes are precisely the ones a
whole-file read **was not delivering anyway**. The delivered prefix is identical before and after a
trim; the only thing that changes is that the reader stops receiving the `PARTIAL view` banner.
**If that holds, the line metric's remedy is cosmetic — it suppresses the warning rather than
delivering more of the file.**

**This became visible only because BL-51's Phase A corrected the premise.** While truncation was
believed *silent*, trimming was the only way to avoid an undetectable gap, and the rationale held.
Once truncation is known to be **announced**, the gap is detectable without trimming, and the
rationale has to be re-argued rather than inherited. Phase A therefore did not fix this — it
**exposed** it, and stopped both the seeds and the two TRACKED tools from asserting a remedy none of
them had established.

**What is NOT claimed here, and must not be inferred.**
- **The byte metric is a different claim** — *context tax*, not read delivery — and this item does
  not touch it. The relayed critique argued against that half too; **S111 did not measure it**, and
  asserting it either way would repeat the original error one level over.
- **"Stop trimming" is not proposed.** That is an operator decision with fleet-wide blast radius.
- The relayed figures (a 25,578-line ledger, a cut at line 746, front matter at 34% of the cap) are
  **that repo's, not re-run here** — `[C]`, and they should be re-measured before being used.

**Measured here, since the same shape was asserted about this repo.** `CHANGELOG.md` front matter is
**14,295 B / 185 ln = 39% of the file**, and it is read *first*, so the critique's front-matter point
is directionally right here too. `HANDOFFS.md` front matter is **6,362 B / 72 ln = 11%** — because
**S109 already shipped that compaction** (−16.2%), which is the relayed critique's option E, arrived
at independently. Neither file is near 2,000 lines, so `read_cap_watch` does **not** fire here.

**Sequencing.** This sits *after* BL-51's Phase B (re-denominate) and is entangled with **Phase C**
(the dedup between the two dashboard rows): if the line metric's remedy does not survive, the dedup
answers itself. Do not decide C without deciding this.

**⚠ ADDENDUM (same session, S111): the argument is REGIME-DEPENDENT, and this repo is in the other
regime.** The critique's load-bearing premise is *"the tail costs nothing, because nothing reads
it."* That is true **only once a file is already well past the cap**. Below it, the whole file is
delivered and every byte is paid for in context; at the boundary, a trim moves a file from
*truncated* to *fully delivered*, which is not cosmetic.

Measured on this repo's own action ledger, by the free error path (an over-cap `limit` reports the
span's token count and returns no content):

| `CHANGELOG.md` | bytes | tokens | vs the 25,000 cap |
|---|--:|--:|---|
| **before S111's trim** | 65,012 | **26,723** `[M]` | **OVER — a whole-file read truncated** |
| **after** | 45,750 | ~18,800 `[D]` | under, fully delivered |

So this repo's ledgers **hover at the cap boundary**; the relaying repo's is reported at 25,578
lines, roughly **40× the cap** `[C]`. Their conclusion may well be right *for them* and **does not
transfer here** — the same failure shape this repo keeps recording (a figure measured in one regime
carried into another; sibling of *a ratio is a property of its content type*, Learning #38-owed).

**Consequence for BL-52's own scope, stated so a later session does not over-read it.** What is
genuinely in question is the **line metric's remedy**, on the argument in the body above. The
**byte** metric is *not* in question here — for a file at or under the cap it bounds a cost that is
actually paid, and S111's trim halved one. **Do not close BL-52 by retiring both.**

**⚠ SECOND ADDENDUM (S111, after close-out, at the operator's direction): the PRECONDITION is
questionable too, and this is the sharpest evidence in the item.** The body above asks whether
trimming *remedies* an unread tail. This asks something one level further back — whether these two
files are subject to the read cap **at all** in the way the framework asserts.

**Two shipped texts disagree, and both are `TRACKED`.**

- `starter-kit/methodology_dashboard.py:295` justifies the watched population as *"The files a
  session is instructed to read **IN FULL** to establish state — `SESSION_RUNNER.md` Phase 0 step 2
  (`SESSION_NOTES.md`), step 3 (`BACKLOG.md`), **step 6 (reconcile `CHANGELOG.md` and `HANDOFFS.md`
  against `git log`)**"*, and on that basis `READ_CAP_WATCHED` (`:311`) includes both ledgers.
- `starter-kit/SESSION_RUNNER.md:37`, which **is** step 6, says to run
  `git log -1 --format=%H -- CHANGELOG.md` for a frontier and then list commits after it. **That
  reads git history, not the file.** The `HANDOFFS.md` half of the same step is frontier-based in
  exactly the same way, and Phase 3A reads **one receipt**, not the file.

**So the premise is sound for three of the five watched names and fails for precisely the two the
trimmer exists to bound.**

> **⚠ THAT SENTENCE'S POPULATION IS WRONG, corrected by S112 at Phase B and left standing above per
> FM #17.** `READ_CAP_WATCHED` holds **SIX** names, not five — `SESSION_NOTES.md`, `CHANGELOG.md`,
> `HANDOFFS.md` and **three** `BACKLOG.md` locations. And **`SAFEGUARDS.md` is not in the set at
> all**: it is the one file `SESSION_RUNNER.md:13` really does say to read *"in full, not skimmed"*,
> and it is deliberately excluded as a `TRACKED` dest. So the tally is not 3 sound / 2 false but
> **2 instructed-but-not-"in full" (`SESSION_NOTES.md`, `BACKLOG.md`, and step 3 is conditional on
> having no issue tracker) / 2 with no protocol basis at all (`docs/BACKLOG.md`,
> `docs/planning/BACKLOG.md`, named nowhere in the runner or `SAFEGUARDS.md`) / 2 false
> (`CHANGELOG.md`, `HANDOFFS.md`)**. The finding is unchanged and if anything stronger; only its
> arithmetic was wrong. **This is the item's own lesson landing on itself: a count is only as good
> as the net that produced it.**
>
> **The missing measurement is no longer missing.** S112 re-derived it rather than citing it: over
> **85 transcripts** (this session excluded, heredoc bodies stripped, pipeline segments classified,
> `starter-kit/` SEEDS and other repos excluded) each **root** ledger was read WHOLE **once** and in
> PART **1,696 / 1,797** times — **1 in 85**, corroborating S98 independently. The first pass was
> wrong by 9–10x because it counted the seeds, and was caught only by printing the raw matches.
>
> **And one premise BL-52 shares with the plan is now falsified at the top end.** *"Truncation is
> ordered top-down, so the records a cut removes are ones the read was not delivering anyway"* holds
> only **between** 25,000 tokens and **256 KiB**. Past 262,144 B a default read is **refused with
> zero content** — there is no delivered prefix to be ordered, and a cut back under it turns
> nothing into something. **Five of the eighteen watched fleet ledgers are already past it.** So
> BL-52's argument is bounded at both ends: it does not hold near the cap (S111's regime addendum)
> and it does not hold well past it either. Steps 1–3 really do say *read* (`SAFEGUARDS.md` *"in full, not skimmed"*,
`SESSION_NOTES.md`, `BACKLOG.md`). Step 6 does not. **The population-selection logic in that comment
is careful and is not what is wrong** — its SEED-vs-TRACKED reasoning stands. What is wrong is the
sentence that says why the two ledgers are in the set.

**Observed, not only argued:** S111's own Phase 0 followed step 6 exactly and **never read
`CHANGELOG.md` whole**; no later step did either. The one whole-file read of a ledger this session
was a deliberate probe, not the protocol.

**What this does and does not license.**
- It **strengthens** BL-52: if nothing is instructed to read these files whole, the line metric is
  bounding a cost the protocol does not incur, and trimming to protect that read is remedying a
  condition that may never arise.
- It **does not** settle it. The missing measurement is **how often anything reads these files whole
  in practice** — a prior session put it near 1-in-81, **not re-run**, and a log-mining count of
  exactly this kind was once wrong by **13×** because `cat >>` and heredoc filenames scored as reads.
  **Re-derive it before using it.**
- It says nothing about the **byte** metric, which remains a separate claim.

**⚠ THIRD ADDENDUM (S112, Phase B): BL-52 IS NOW ADJUDICATED FOR THIS REPO'S `HANDOFFS.md`, ON
MEASUREMENT, AND THE ANSWER IS THAT THE TRIM BUYS NOTHING.** The occasion was mundane — a trim was
due as close-out housekeeping and `methodology_trim.py` refused it (`[SRF_RED]` 1.1198: *"the last
archive has been entirely given back; archiving again resets the LEVEL and not the RATE"*). The
session was about to `--force` past it. **It had not asked BL-52's own question first.**

Asked, the answer is decisive. A whole-file read of the untrimmed ledger delivers **the front matter
and the four newest receipts** — measured by the free over-cap error path, not modelled:

| prefix | predicted | **measured** | error |
|---|--:|--:|--:|
| front matter + **4** newest receipts (55,342 B) | 23,409 tok | **23,370 tok** | 0.17% |
| front matter + **5** newest receipts (67,630 B) | 28,606 tok | **28,611 tok** | 0.02% |

The proposed `--cut 3` would have archived S108 and S107 — **both already outside the delivered
prefix.** Against what the protocol actually consumes: **Phase 3A reads ONE receipt**, the
predecessor's, at the top; **Phase 0 step 6 takes the frontier from `git log` and greps** for a
pending receipt; whole-file reads run **1 in 85**. So on the read-delivery claim the trim changes
nothing anyone reads.

**And the context-tax claim does not rescue it either.** That cost is paid per read-span — 1,797
partial reads against 1 whole — and is already guarded per record by `RECORD_BUDGET_BYTES = 12,288`,
which every receipt in the file is inside. S98 reached the same conclusion for this file by a
different route and moved the guard accordingly; `.context-budget.json` still says so in its own
words: *"MAX_BYTES 65,536 IS RETAINED BUT NO LONGER THE OPERATIVE GUARD."*

**So the tool's refusal was right, and right for a STRONGER reason than the one it gave.** It
diagnosed a level remedy applied to a rate problem. The measurement adds: the level is not costing
anything yet.

**What this does and does not settle.**
- It settles **this file, at this size, with these record sizes** — the middle regime, between the
  25,000-token cap and the 256 KiB refusal. It does **not** settle the general question, and it
  says nothing about a repo well past the refusal, where a cut back under it turns nothing into
  something.
- **The threshold that will actually bite is `READ_REFUSE_BYTES` = 262,144**, where the front matter
  itself stops being delivered. From 77,265 B at ~12,288 B per close-out that is **~16 sessions**.
  The remedy between here and there is the **record budget**, not archiving.
- **It leaves two signals red that are literally true and, on this measurement, not worth acting
  on** — `context_budget.py` BREACH and one high-severity read-cap row on this repo's own ledger.
  That is deliberate and is itself the finding: **a guard can be correct and not worth acting on**,
  which makes Phase C's question larger than *two rows or one* — it is what population and what
  claim each row should carry. The **prefix guard** (plan §12.4) is the candidate that answers both.

**Precedent set, and it is the transferable part:** *a trim was declined on evidence rather than
performed as routine*. Every prior session here trimmed when a ceiling said to. This one measured
what the trim would deliver first, and the honest answer was nothing.

**And it is a fourth defect in the same neighbourhood as the three Phase A corrected** — a
justification that was written once, plausibly, and never re-checked against the step it cites.
Whoever takes Phase B or BL-52 should decide whether the fix is to correct the comment, to narrow
`READ_CAP_WATCHED`, or to make step 6 actually require the read it is credited with.

**⚠ FOURTH ADDENDUM (2026-09-14, S161 follow-up, operator decision): the byte half is now decided
for this repo's `CHANGELOG.md`.** The operator removed it from `.context-budget.json` (`3c8acd5`): a
session looking for something in the ledger greps it or runs git, so only those results enter its
context. That is the reasoning this item's own measurements supplied — one whole-file read per root
ledger in 85 transcripts (S112), after S98 found the same for `HANDOFFS.md` in 81 — applied to the
byte metric, which the addenda above had deliberately left open. `context_budget.py` no longer
reports the file; nothing else changed.

**What it leaves open, each still true at 203,649 B:**
- **The trimmer's Class A trigger still fires** (196,608 B, `starter-kit/methodology_trim.py:164`).
  It lives in the distributed tool, reads no config file and gates nothing; its only knob is a
  per-run `--budget-bytes` flag. Retargeting it is an upstream change, and its dashboard mirror
  (`starter-kit/methodology_dashboard.py:322`) moves with it.
- **The 262,144 B default-Read refusal** (`:130`) is still the boundary this item says actually
  bites — about 58 KB away. Reads with `offset`/`limit` are unaffected.
- **`HANDOFFS.md` stays in the budget** only because the decision named `CHANGELOG.md`; the S112
  argument covers it equally.
- **This ledger's own archive rule** (`CHANGELOG.md`, *When to archive again*) is still stated
  against the 2,000-line read-cap proxy.
- **`READ_CAP_WATCHED`'s justification** — the dashboard comment quoted in the second addendum —
  still credits step 6 with reading both ledgers in full.

<a id="bl-53"></a>

**BL-53 — how many learnings should the framework carry before old ones retire? `FRAMEWORK_LEARNINGS.md`'s
limit is now only a growth warning, and it will fire again. Raised 2026-09-10 (S159).**

At S157's close-out the file reached 73,920 B against its 73,728 B limit. At S159 the operator raised
the limit to **81,920 B** and had it re-labelled a **growth warning**, not a readability guarantee
(`.context-budget.json`, the file's entry). After Learnings #62 and #63 the file is 76,007 B, so the
room left is **4 rows** at the 1,239 B median of rows #48–#61 — **about 10 sessions** at the 583 B per
session measured from S132 to S157. **This is the second raise in 15 days** (BL-45 was the first,
S114, 2026-08-26), and neither answers the question underneath — Learning #26's: the rows nobody may
drop *are* the file.

**Readability is already gone, and this limit does not guard it.** Metered by the doubled-file method,
the file was **25,445 tokens at 73,920 B** (2.9051 B/token), past the 25,000-token Read cap, and
26,189 tokens at 76,007 B. A whole Read fails — here, and in any adopter that syncs the file. The
tool computes no token verdict for on-demand files by design (`starter-kit/context_budget.py:77-83`),
because sessions read this one in part. Guarding adopter readability anyway would mean a token limit
for on-demand files in the distributed `context_budget.py` — an upstream change and its own session.

**The options, costed at S159 by running each in a `--no-local` clone** with both new rows appended,
against a 304 passed / 1 failed baseline (Test 9, pre-existing), so they need not be re-derived:

| option | file | room left | whole Read | tests | cost |
|---|--:|--:|---|---|---|
| **raise to 81,920 B** ✅ | 76,007 B | 4 rows | fails (26,189 tok) | 304 / 1, no change | canonical-only config. **Taken.** |
| tombstone rows 1–10 | 70,879 B | 2 rows | fits, 222 tok spare | 304 / 1, no change | 10 distributed rows become ~246 B stubs linking to an archive that exists upstream only after a merge |
| archive rows 1–10 | 68,418 B | 4 rows | fits, 1,412 tok spare | 295 / 10 | a checker change for the numbering gap; 7 citations to missing rows in 4 distributed files; 9 tests built on the live file |
| archive rows 1–5 | 73,427 B | 0 rows | fails (25,328 tok) | 295 / 10 | the same checker change, for 301 B |
| compact ~25 rows | ~69,000 B (est.) | ~4 rows (est.) | fits (est.) | not run | a 3-row trial saved 20% (880 B); rows 12–33 were already compacted once (S119), so returns there will be lower |

**S199 (2026-09-20): the rule is COSTED and written, and it is waiting on the operator, not on a session.**
[`fork-learnings-retirement-rule-plan.md`](fork-learnings-retirement-rule-plan.md) re-measures the whole
question against `docs/FORK_LEARNINGS.md`, which is what D1 left BL-53 governing — **83,768 B, 68 rows,
1,848 B over and widening across three receipts.** Four decisions are open (D1 criterion, D2 mechanism,
D3 trigger, D4 what the ceiling then means) and four mechanisms were **run, not reasoned about**, in a
`--no-local` clone at `6a475b6`. Two results change the options this item records: **(1)** `bin/check-learnings`
already tolerates a declared gap (`RESERVED_RE`, `:76`), so retiring a row needs **no checker change** and need
not start at the oldest — the "checker change for the numbering gap" costed above is false today; **(2)** the
whole distributed-corpus exposure is **zero** — the two apparent hits (`README.md:467`,
`docs/RELEASE_HISTORY.md:53`) are rad-con's numbering narrated as a defect, and no assertion anywhere depends
on a row existing. Against that, the plan's central finding is negative and is why it does not simply
proceed: **adjudicating the ten oldest rows yields at most two retirements (~2,900 B), about one session of
headroom** — age is not a proxy for spentness here, the oldest band being the densest. The trade that buys
real headroom retires live advice, and that is the operator's call.

**RATIFIED AND APPLIED, S200 (2026-09-20) — and the catch-up pass retires nothing.** The operator
answered D1–D4 at S200's Phase 0 picker: **option A + C's D3 pairing.** **D1** a row retires only when
**mechanized** (a `.quality-gates.json` gate, a `bin/tests.sh` test or a numbered FM enforces the lesson),
**superseded** (a later row states it at least as generally) or **spent** (its artifact no longer exists),
with the citation in the retiring commit; **D2** reserved-gap retirement — text moved verbatim to
`docs/archive/FORK_LEARNINGS-retired.md`, one reserved-number line in the live file, no renumbering;
**D3** a session that appends a row either retires one or states in its handoff that none qualifies,
naming what it considered; **D4** the 81,920 B ceiling unchanged as a growth warning, so **no P5**.

P3 then adjudicated **all 69 rows** (15–83), each read in full, in
[`fork-learnings-adjudication-2026-09-20.md`](fork-learnings-adjudication-2026-09-20.md). **Yield: 0.**
The *"at most two, ~2,900 B"* above was the optimistic bound of a ten-row sample that marked `#15` and
`#19` **partly** covered; D1 retires a row *"when, and only when, one of these holds"*, and partly is not
holds. Six rows are partly covered in all (`#15`, `#19`, `#24`, `#38`, `#45`, `#82`). **Two limbs are
unsatisfiable across this corpus, measured rather than argued:** (b) 13 rows cite an earlier row and every
citation is a *differentiation* — "sibling of", "distinct from", "the converse of" — never a restatement,
while **eight** rows are cited BY another live row or live config, so retiring one strands an in-table
reference (row `#22`'s lesson, applied to the file `#22` lives in); (c) 38 rows name a file path, **56
mentions, every one resolving to a tracked file.** **The file therefore stands at 85,228 B, 3,308 B over,
and the plan's central finding is stronger than the plan stated it.** The adjudication recommends keeping
D3 and taking **option C** — demote the ceiling to a reported series, keep the per-row budget — with **B**
(oldest-first to an operator-stated depth) still the only option that recovers real bytes, now costed row
by row rather than by age. **That choice is open; P4 (writing D3 into `CLAUDE.md`) is a separate session.**

**THE CHOICE IS MADE AND P4 IS DONE, S201 (2026-09-20).** The operator ratified **option C** at this
session's Phase 0 picker, with **D3 retained**, and **declined B with its cost known** — 14,502 B at ten
rows, the live advice named row by row in the adjudication's §5. So **D4 is now C, not (i)**: the 81,920 B
figure becomes a **reported series** rather than a limit, and the per-row budget (`bin/check-learnings`,
`ROW_BUDGET_BYTES` = 1,500, green at 0 violations) is what still refuses. **That reverses the S200 block's
*"D4 the ceiling unchanged … so no P5"* above** — left standing as written (FM #17) and corrected here:
**P5 is owed**, and it is the one remaining phase. `.context-budget.json` still calls the figure a warning
until it runs.

**P4 shipped at `24fe658`**: D3 written into `CLAUDE.md` §*Where this fork's learnings go* — the obligation,
D1's three limbs in full (a session cannot honestly refuse against a criterion it must open a plan to
read), D2's mechanism in one sentence, and the ceiling's new standing. Fork-only, **not** the distributed
`starter-kit/SESSION_RUNNER.md`. 12,688 B → 14,392 B against an 18,600 B ceiling. **P4's gate half is not
owed:** §8 makes it conditional on D4 choosing a *mechanical* form and C is not one.

**What is left of BL-53 is P5 and nothing else.** The rule is decided, applied to every row, and written
where sessions read it; the file stands at **86,727 B, 4,807 B over** a number that C has just demoted.

**CLOSED 2026-09-20 (S202). P5 SHIPPED AT `9db2c18` AND BL-53 IS DONE.** `.context-budget.json`'s
`docs/FORK_LEARNINGS.md` entry (`files[3]._`) now states option C in the artifact that was still calling the
figure a warning to be answered: **a reported series, not a limit**; `over` on that row is the expected state,
the per-row `ROW_BUDGET_BYTES` = 1,500 is what refuses, and the D3 obligation in `CLAUDE.md` is what holds the
line. `max_bytes` stays **81920** — C demotes the number's meaning, not the number. Exactly one key changed,
proved by walking the re-parsed object against the pre-edit one (`['/files[3]/_']`). Verified with the phase's
own command run **bare**, so the exit code is the tool's and not a pipe's: `python3
starter-kit/context_budget.py` → **exit 2**, the pre-existing OVER state (this file, `SESSION_RUNNER.md`,
`SAFEGUARDS.md`, the read-set total), unchanged by the edit.

**Two claims in the old note failed verification and were corrected rather than carried into the rewrite.**
`bin/_manifest.py` has **no** row for `docs/FORK_LEARNINGS.md` (`grep -c` = 0); its `:38` distributes
`starter-kit/FRAMEWORK_LEARNINGS.md`, upstream's file — so the old note's *"adopters … receive the file itself
(bin/_manifest.py:38)"* was true of the file this entry watched **before** the 2026-09-16 re-point and inverted
silently with it. And *"no `.quality-gates.json` gate reads budget status"* needed narrowing: four `budget` hits
exist there, three prose and one the gate `context-budget-unit-tests`, which runs the tool's **unit suite**, not
this repo's measurement. The claim holds; the loose wording would have read as refuted by the next session that
grepped.

**What this closure does NOT include, stated so it is not read as more than it is.** No row has ever been
retired, so D2's mechanism is still proven by S199's E2 experiment rather than by use; option **B** stays
declined and **not foreclosed**; P4's gate half was never owed (§8 makes it conditional on D4 choosing a
*mechanical* form, and C is not one), so **D3 is held by prose and by close-out discipline, not by a check** —
the first thing to revisit if it is ever skipped.

**What would answer it** is a retirement rule decided once, as policy, instead of a byte negotiation at
every breach. Tombstoning is the mechanism that keeps `Learning #N` citations resolving; what it lacks
is a rule for *which* rows retire (for example, a row whose lesson the runner itself now carries as an
FM or a phase step). **Decide it before the warning fires again.** Anything that changes the
distributed file's shape is an upstream change.

<a id="bl-54"></a>

**BL-54 — `bin/sync` and `bin/status` walk history without `--full-history`, so a version that exists
only on the merged-in side of a merge reads as a local modification. Raised 2026-09-14 (S161).**

`local_history_blobs` (`bin/sync:55-77`) and `local_history` (`bin/status:52-74`) collect the versions a
file has had with `git log --format=%H -- <path>` (`bin/sync:60`, `bin/status:56`). Git's default history
simplification follows only a merge's TREESAME parent, so when a merge keeps one side's content for a
path, the other side's commits for that path are never visited. Fork `main` kept its own content for
several distributed files when it merged `upstream/read-set-budgets` (`213f841`): for
`starter-kit/SESSION_RUNNER.md` the default walk visits 46 commits and never reaches the branch's version
(`c0550acd`); `--full-history` visits 77 and finds it at `46b56fdb`.

**Measured consequence (S161, on scratch copies):** the three projects that sync cleanly from a clone of
the branch (`airqino`, `church_growth`, `dalia_martinez_funeral`), once synced that way and then synced
from fork `main`, are refused (exit 2) on `SESSION_RUNNER.md`, `BOOTSTRAP.md`,
`methodology_dashboard.py` and `HOW_TO_USE.md` — all four in fork `main`'s full history, none in its
default walk. `--force` is safe there, and the tool cannot say so. None of the refusals in the 12
projects' current states is this defect
([`read-set-budgets-local-use-routes.md`](read-set-budgets-local-use-routes.md) §3, §5.1).

**The fix** is `--full-history` on both `git log` calls. Neither file is distributed (`bin/` has no row in
`bin/_manifest.py`), so it lands here and, through a PR, upstream. Two things to settle when it is made:
whether `bin/status`'s *N versions behind* count — an index into that walk — should count the side
branch's versions; and a test that fails on the default walk, built on a merge that does not keep the
merged-in side's change to the path.

**Fixed fork-side at S179 (2026-09-17): `2c4f801`, with `865119f` batching the blob lookups.** Both questions above were
settled. `bin/sync` walks with `--full-history`; it asks only whether a version is known. For `bin/status` three counts
were measured on the six adopters and **the operator chose C (picker)**: N is the distinct versions newer than the
project's along the checkout's **first-parent** line, one per merge however many commits the merged branch had, and a
version that only ever existed on a merged branch is counted along the full walk instead. Rejected: A, the flag alone,
whose raw position read 63 behind for `mts-system`'s learnings file, and B, distinct versions over the full walk, which
counts every commit inside a merged branch. The test is `bin/tests.sh` Test 41: a repository with both hiding shapes
(a merge taking the side branch's content, `22ce71b`'s, and one keeping main's, `213f841`'s) at fixed dates. It failed
4 rows on the old code, passes 11, and eight mutants fail it, A and B among them. On the real adopters, 8 of 174 rows
change state, all *locally modified* → *N versions behind*, including `vscode_quarto_ext`'s `context_budget.py`, already
misread before `22ce71b`. The fork-side commits changed `bin/status`'s run time from 3.0 s to 4.0 s over the six, and
`bin/sync --dry-run`'s on `wsfct` from 2.9 s to 2.3 s. **Still open: the upstream PR, its own go-ahead.**

<a id="bl-55"></a>

**BL-55 — nothing enforces removing a completed `BACKLOG.md` item; the one detector only reports, and
cannot join a backlog item to the ledger entry that closed it. Raised 2026-09-14 (S161, on the
operator's request).**

**The rule exists; the gate does not.** Removing a completed item in the commit that logs it is required
by `starter-kit/SESSION_RUNNER.md:284` (Phase 3F), FM #27's countermeasure (`:335`),
`ITERATIVE_METHODOLOGY.md:294`, the ledger seed `starter-kit/CHANGELOG.md:29` and
`starter-kit/BOOTSTRAP.md:141`. Nothing checks it: `.githooks/pre-commit:49` requires only that
`CHANGELOG.md` be staged; Phase 0 reconcile compares `CHANGELOG.md` with `git log`, never with
`BACKLOG.md`; `bin/check-handoff:453` rejects only *"pick next from backlog"*; `methodology_trim.py` and
`context_budget.py` do not cover `BACKLOG.md`.

**The one detector is the dashboard's Signal F** (`starter-kit/methodology_dashboard.py:1933-1985`). It
reads `BACKLOG.md` alone, counts items still marked done — `[x]`, or a DONE-type Status cell — as a proxy
for *completed, never migrated*, and adds a risk line for adopters (`:2032`). It never blocks, and it
cannot see a completed item left in place without a done-mark.

**The instance that raised it — `nprcgenekeepr`, measured with Signal F both times.** 2026-09-11: 28
done-marks in a 218,350 B, 2,494-line `BACKLOG.md` that the project reads for its priorities
(`CLAUDE.md:133-143`). That day its S686 adopted a project-level removal rule (`CLAUDE.md:269`,
`eac246f1`); on 2026-09-14 its S687 removed all 28 by hand (`9ae0c99c`, `20fd9c08`). Signal F now reads
0, and the file is 102,069 B, 1,226 lines. **A checklist worked once; nothing stops the next
accumulation.**

**Why the obvious gate does not reach adopters.** The rule's own join key is the `[BL-<N>]` source tag
(`starter-kit/CHANGELOG.md:29`): a gate could refuse a commit that adds a `[BL-N]` entry while `BL-N`
still names an open item. But `nprcgenekeepr`'s backlog names **no** `BL-` id, and only **5 of its 322**
tagged ledger entries carry `[BL-N]`; this repo carries **61 of 484** across the live ledger and its
archives. In practice the key is optional, so each design has to answer that first.

**Options to cost, none decided:** (a) a `[BL-N]` join check — in `.githooks/pre-commit`, which is
canonical-only (BL-6 item 3), or in a distributed checker; it covers only adopters that use the key.
(b) Signal F promoted from a report to a close-out gate — covers done-marked items in the two formats
it recognizes (checkbox, Status table), never unmarked ones. (c) A mechanical check named in Phase 3F —
grows `SESSION_RUNNER.md`, whose Phase 0 pair has ~400 tokens of read-cap headroom on fork `main`.
(d) Keep the report and rely on the warning row at `SESSION_RUNNER.md:366` (*the same finding for
several sessions → add a gate*). Anything distributed is an upstream change.

<a id="bl-56"></a>

**BL-56 — rewrite `airqino`'s `CHANGELOG.md` to the current ledger format. Raised 2026-09-14 (S161, on
the operator's request).**

`bin/status` reads `airqino`'s `CHANGELOG.md` as *present (stale format)* under both the branch's and
fork `main`'s markers: the file (1,309 B) carries neither `Authoritative Action Ledger` nor `Size, and
when to archive`, and the current seed (`starter-kit/CHANGELOG.md`, 12,893 B) carries both. It is the
pre-v3.1 Keep-a-Changelog template, and `bin/sync` never rewrites a seed (`bin/_manifest.py`, the `SEED`
disposition), so S161's Route A sync (`dfe26fd17` in `airqino`, branch
`chore/methodology-read-set-budgets`) left it as it was. The `HANDOFFS.md` that sync created from the
current seed already reads `present`.

**Almost nothing to preserve:** the file holds one dated entry — the 2026-09-14 sync entry — and no
earlier history. That makes the second remedy in `starter-kit/BOOTSTRAP.md:86` the cheap one: delete the
file, re-run `bin/sync` to reseed the current shape, carry the one entry across, and delete the seed's
`METHODOLOGY-SEED-SENTINEL` line (`starter-kit/CHANGELOG.md:10-13`), which its own text says to remove at
the first real entry. The by-hand reconcile, the other remedy there, rebuilds the same file in more steps.

**Where it lands:** on `chore/methodology-read-set-budgets`, the branch that holds the entry, as one
commit with its own ledger entry — the work is `airqino`'s. Pushing either `airqino` branch, or opening a
PR, is a separate go-ahead. **Done** when both `bin/status` versions read `present` for `CHANGELOG.md`.

**Out of scope, recorded:** S161's run of fork `main`'s `bin/status` (2026-09-11) found the same *present
(stale format)* verdict on other projects' `CHANGELOG.md` or `HANDOFFS.md`; this item is `airqino` only.

**Folded into BL-57's plan (S162):** the reseed happens in its P6, against the thin seed that plan
introduces, so it is done once rather than twice
([`changelog-rules-contradictions-plan.md`](changelog-rules-contradictions-plan.md) §5, P6).

**Closed at S180 (2026-09-17): done in `airqino`'s own repository, as BL-57's P6** (its Session 6, local branch
`chore/methodology-bl57-p6`, not pushed). Two things above no longer held by then. The file held **two** dated
entries, not one: `airqino`'s Session 5 had added its own. And the landing branch is a new one taken from
`1402ad4`, not `chore/methodology-read-set-budgets`. So the header was migrated by hand rather than reseeded:
`5e4b483` replaces lines 1–11, the Keep-a-Changelog header and its `## [Unreleased]`, with the thin seed's
header less its `METHODOLOGY-SEED-SENTINEL` line, and leaves every entry byte-identical. `28022fe` is the sync
before it, from fork `main` `ff02b5c`. **The done test holds, re-run from here:** `bin/status` reads
`CHANGELOG.md` `present` in `airqino` from three trees, each a `--no-local` clone with HEAD asserted: the
branch `83a12f0`, `upstream/main` `6b29d3d` and fork `main` `ff02b5c`.

<a id="bl-57"></a>

**BL-57 — HIGH PRIORITY: the framework's rules for `CHANGELOG.md` contradict each other; remove the
contradictions here and roll the fix into six adopters, aiming at an upstream PR. Raised 2026-09-14
(S161 follow-up, on the operator's request).**

**Priority and shape, as the operator set them.** High priority. The next step is a **planning
session** — the plan in `docs/planning/` is its deliverable (`starter-kit/SESSION_RUNNER.md` §Planning
Sessions: a grep inventory, per-phase DONE criteria, the surface each is shown on, one session per
phase) — then implementation sessions under it. Scope: this repo plus `airqino`,
`model_project_constructor`, `mts-system`, `nprcgenekeepr`, `vscode_quarto_ext` and `wsfct`. **Intent:
an upstream PR, or commits added to one** — [PR #80](https://github.com/KJ5HST/methodology/pull/80) was
open on 2026-09-14 — and each such action is its own go-ahead (`CLAUDE.md` §Contributing upstream).

**The contradictions, each line re-read 2026-09-14:**

1. **Whether a session reads the file.** The seed says *"Phase 0 reads it every session"* and prices
   its byte cap as *"every session pays for the whole file, every time"*
   (`starter-kit/CHANGELOG.md:96-97`, `:104`). But Phase 0 step 6 reads `git log`, not the file
   (`starter-kit/SESSION_RUNNER.md:37-38`); `starter-kit/BOOTSTRAP.md:420` calls it a reference doc
   *"not required at session start"*; and S112 measured one whole-file read in 85 transcripts (BL-52).
   The dashboard's watched-set rationale (`starter-kit/methodology_dashboard.py:259`) and the trimmer's
   *"per-file context-tax budget"* (`starter-kit/methodology_trim.py:186`) rest on the seed's premise;
   this repo's budget config dropped it (`3c8acd5`).
2. **Three archive triggers for one file.** The seed: a line rate plus a byte level, *"default 65,536
   B"* (`starter-kit/CHANGELOG.md:103-104`). This repo's front matter: the line rate alone
   (`CHANGELOG.md`, *When to archive again*). The tool it ships with: 196,608 B
   (`starter-kit/methodology_trim.py:164`, `:186`) — so the seed's default is stale, and PR #80 ships
   the two disagreeing.
3. **"Append" or "prepend".** *"Append … newest on top"*: `starter-kit/SESSION_RUNNER.md:284`,
   `ITERATIVE_METHODOLOGY.md:294`, `HOW_TO_USE.md:767`. *"Prepend"*: `starter-kit/CHANGELOG.md:17` and
   the runner's own backfill step (`starter-kit/SESSION_RUNNER.md:39`).
4. **When a trim happens.** The seed: a trim *"does not belong in Phase 0"*
   (`starter-kit/CHANGELOG.md:167-169`). This repo's `HANDOFFS.md:15`: count *"at Phase 0"* and *"trim
   to 4"*. The runner names no trimmer at all.
5. **Two definitions of a stale seed.** PR #80's `bin/_manifest.py` keys `SEED_FORMAT_MARKERS` on the
   seeds' titles (`Authoritative Action Ledger`, `Handoff Receipts`); fork `main` keys both on `Size,
   and when to archive`. `bin/status` answers differently depending on which checkout runs it.
6. **The source-tag vocabulary is closed in the seed and open in practice.** The seed allows exactly
   `[issue #<N>]`, `[BL-<N>]` and `[ad hoc]` (`starter-kit/CHANGELOG.md:23-32`); adopters write
   `[BL-OPS-ADMIN-PW-RECOVERY-001]` (`mts-system`), `[BACKLOG: …]` (`vscode_quarto_ext`),
   `[BL-backlogXBlockBackfill]` (`nprcgenekeepr`), or no tag (`model_project_constructor`). The `[BL-N]`
   removal rule that depends on the tag is BL-55.
7. **The Phase 1B marker has no home in this repo.** The runner puts `CHANGELOG: pending` in
   `SESSION_NOTES.md` (`starter-kit/SESSION_RUNNER.md:88`); this repo keeps none, so each claim writes a
   permanent ledger entry carrying the marker. Fork-only, and not written down as an adaptation.
8. **One entry per action** (`starter-kit/SESSION_RUNNER.md:284`) against this repo's habit of
   bundling several actions into one entry.

**What the rollout will meet — measured 2026-09-14, read-only, from raw match positions:**

| repo | `CHANGELOG.md` | seed's rules text carried | tag style | trimmer | notes |
|---|--:|---|---|---|---|
| `methodology` | 206,897 B | its own front matter, no seed copy | closed | 1.5.0 | the canonical source of items 1–5 |
| `airqino` | 1,309 B | none — the pre-v3.1 template | closed | 1.5.0 | BL-56; a branch off open PR #1 |
| `model_project_constructor` | 666,365 B | none — `### date — summary`, untagged | none | none | runner customized (step 5) |
| `mts-system` | 358,377 B | none | its own `[BL-…-001]` ids | 1.1.1 | |
| `nprcgenekeepr` | 413,383 B | yes, `:3946`–`:3983`, an older copy that still calls truncation *silent* | its own `[BL-…]` ids | 1.1.2 plus a local `SESSION_NOTES.md` ledger | its 2026-09 entries sit under `## 2026-08` |
| `vscode_quarto_ext` | 87,837 B | none | `[BACKLOG: …]` | 1.3.0 | its `.context-budget.json` lists `CHANGELOG.md` (BL-47's question) |
| `wsfct` | 162,549 B | yes, the seed's sections at `:13`–`:196`, above its entries — also the older copy (`:101` still says *silent*) | closed | 1.1.2 | |

What that means for a plan:
- **Two delivery routes.** The runner, `BOOTSTRAP.md`, `HOW_TO_USE.md`, `ITERATIVE_METHODOLOGY.md`, the
  dashboard and the trimmer are TRACKED, so `bin/sync` carries the fix (Route A or B per project —
  [`read-set-budgets-local-use-routes.md`](read-set-budgets-local-use-routes.md)). Each adopter's
  `CHANGELOG.md` and `HANDOFFS.md` are SEEDS, never overwritten, so the copies in `nprcgenekeepr` and
  `wsfct` must be migrated by hand, and each `CLAUDE.md`'s own ledger rules reviewed.
- **Three adopter ledgers are already past the 262,144 B default-Read refusal** —
  `model_project_constructor`, `mts-system`, `nprcgenekeepr` — the boundary BL-52 says actually bites.
  The plan must say what the rule is for them.
- **Known blockers from S161:** `nprcgenekeepr`'s local trimmer entry (it re-adds cleanly onto 1.5.0),
  the customized runner in `model_project_constructor`, and `airqino`'s open PR #1.
- **Batch with** BL-47, BL-52's open list, BL-55 and BL-56 where they touch the same files; the
  maintainer's review time favours one substantial, vetted PR.
- **Operator decision, 2026-09-14: do not trim this repo's `CHANGELOG.md`.** Its trimmer trigger keeps
  firing; the plan settles what the archive rule becomes, starting from that decision.

**Planned at S162 (2026-09-14 → 09-15), operator-approved:
[`changelog-rules-contradictions-plan.md`](changelog-rules-contradictions-plan.md) (`9292132e`).** The
operator decided four questions, all A: the rules move to one synced home (`FRAMEWORK_APPARATUS.md`
§The Action Ledger) and the seed becomes a linked pointer with a format marker; archiving is optional;
`[BL-<id>]` takes any backlog id; one entry per commit, never edited. The inventory grew the eight
contradictions above to sixteen findings. Two corrections to this item: `nprcgenekeepr`'s rules block
runs :3946–:4065, between two runs of entries; and contradiction 1's dashboard citation (:259) is
half-stale, because the fork dashboard's own comment (:325–345) already rejects the premise and keeps
the ledgers in its watched set only as a property report. **Next: the plan's P1**, one session, on
branch `bl57/changelog-rules` created from `b82dcff`. BL-56 folds into the plan's P6, and BL-47's
`CHANGELOG.md` half is settled by Q2 A (both noted in those items).

<a id="bl-58"></a>

**BL-60 — every trim writes a ~16 KB proof script that is 97.9% identical to the last one. 31 of them
now hold 453,689 B, 5.4% of the tracked repository. Raised 2026-09-16 (S172, on the operator's
request, after the retention change made trim frequency a live cost).**

**The measurement.** `methodology_trim.py` emits one `<shard>.verify.sh` per trim, re-deriving L1/L2/L3
from git. It is a **fixed cost per trim** — the same harness whatever the shard holds:

| | |
|---|--:|
| proof scripts under `docs/archive/` | **31** |
| their total bytes | **453,689 B** |
| each proof | **16,011 B**, 357 lines |
| two consecutive `HANDOFFS` proofs differ by | **4 lines / 336 B — 2.1%** |
| a `CHANGELOG` proof vs a `HANDOFFS` proof differ by | 16 lines |
| proofs as a share of `docs/archive/` | **12.4%** |
| proofs as a share of the tracked repo | **5.4%** |

All 31 blobs are distinct, so git stores 31 near-copies rather than one. **97.9% of each new proof is
bytes the repository already holds.**

**Why it matters more now than it did.** Until S172 this was a slow accrual at roughly one trim per
4.5 sessions. The N=1 retention decision made it one trim per session until the trigger was moved to
2, and it is still the dominant per-session overhead: ~16 KB of proof against a median receipt of
9,545 B. **The proof costs more than the thing it proves.** It is also why S171 measured small trims
as the expensive ones — a fixed cost amortised over less relief.

**The shape of a fix, not a decision.** The variable part is small and enumerable: the shard path, the
commit sha, the record count, the byte totals. So a generated proof could be **one shared harness
plus a per-shard manifest** — the harness tracked once, each shard carrying a few hundred bytes of
parameters. Alternatives worth costing against it: emit no script and publish the verification
*command* (the harness becomes documentation, and `docs/archive/` stops growing a script per trim);
or keep the script but stop tracking it, regenerating on demand.

**Three constraints any fix has to respect, each of them load-bearing.**

1. **A shipped proof must be runnable from the shard alone.** Its whole purpose is that a reader runs
   it rather than trusting the table — `HANDOFFS.md`'s own archive table says exactly that. A fix
   that makes verification depend on a file the shard does not name trades a real property for bytes.
2. **The generator is DISTRIBUTED.** `bin/_manifest.py:50` installs `starter-kit/methodology_trim.py`
   at every adopter root as a **TRACKED** file, so this is an adopter-facing change and **its own
   go-ahead**, not a fork-local cleanup.
3. **Frozen proofs must keep working.** The 31 existing scripts are frozen artifacts beside frozen
   shards; a new scheme applies to new trims, and migrating the old ones is a separate question with
   its own losslessness burden — rewriting a proof is exactly the kind of edit a proof exists to catch.

**Not decided here:** which of the three shapes; whether existing proofs migrate; whether this is
worth doing before the `HANDOFFS.md` front-matter cut BL-59 leaves owed. **Measured at S172, and the
numbers above are re-derivable** — `git ls-files 'docs/archive/*.verify.sh'` and `diff` on any two.

**BL-59 — `HANDOFFS.md` retains four receipts, and no consumer needs more than one. Decide the
retention number from what reads the file, and settle whether the *proof* half belongs in
`CHANGELOG.md` at all. Raised 2026-09-16 (S172, on the operator's question: "I thought `HANDOFFS.md`
was only used between 2 sessions").**

**The premise is correct, and the file does two jobs with opposite retention needs.** The *handoff*
— session N briefing session N+1 — is done by the **newest receipt only**: Phase 0 reads it, Phase 3A
scores it, and its content has then done its work. The *proof* — the file's own framing,
*"the durable answer to 'was close-out actually performed?'"* — is what makes the file append-only,
because a proof that can be deleted is not one. The first job wants a retention of 1. The second
wants never to delete. They were merged into one artifact and the retention number is the seam.

**What actually reads a receipt below the newest — all five consumers checked, not assumed:**

| consumer | what it does with older receipts |
|---|---|
| Phase 0 reconcile | **nothing** — frontier-based, newest only |
| `bin/check-handoff --all` | traverses all, but checks *integrity*, not content: the answer-slot rule requires every receipt below the newest to name a commit sha, so a session that claimed and never finished stays detectable |
| `bin/model-report` | **the only content consumer** — reads the free-text prose after every block for model mentions |
| `bin/tests.sh` Test 34 | reads the **live** ledger for its anchors (`bin/tests.sh:2089`); below three receipts six assertions become named `SKIP` rows (BL-40's fix), never a failure |
| `bin/tests.sh` Test 38 | **copies the live ledger into a temp fixture and exits if it holds fewer than two records** (`bin/tests.sh:2752`). This is a HARD failure, not a skip, and it was missing from this item's first draft |
| `methodology_dashboard.py` | presence, freshness, size class — never content |

Two facts follow, and together they are the case. **`model-report` discovers archive shards by glob**
(`bin/model-report:158`), so archiving a receipt does not remove it from the one tool that reads
historical content. And **`bin/check-handoff --archived` validates a frozen shard**, so the integrity
scope survives archiving too. **Nothing requires an old receipt to be in the *live* file.**

**So the number is a choice, and the file says so:** *"N=4 is an operator decision, never
re-derivable from the 56,750 B detector floor."* Adopted at S127 (2026-08-30); the warrant
(`docs/archive/CHANGELOG-through-2026-09-02.md`:2070) justifies the *trim*, never the *four*.

**What it costs, measured at S172's close-out (75,185 B, 7 receipts):**

| | bytes | share |
|---|--:|--:|
| front matter | 6,984 | 9.3% |
| newest receipt (the one doing the handoff) | 13,388 | 17.8% |
| **receipts that have already done their job** | **54,813** | **72.9%** |

The file is over its byte ceiling by 9,649 B and **over its 25,000-token ceiling by 6,793**
(≈31,793 tokens at a measured 2.3648 B/token). At S171 the same decision was costed in bytes alone
and read as a preference (*"roughly 1.9× net-additive"*); in tokens it is a red gate.

**DECIDED BY THE OPERATOR, 2026-09-16 (S172): cut retention to 1.** What follows is what the
decision met when it was executed — measured in a throwaway clone at `dd18114`, never predicted.

**N=1 IS NOT REACHABLE TODAY, AND THIS ITEM'S FIRST DRAFT SAID OTHERWISE.** It claimed the only cost
below three receipts was six stated `SKIP` rows, *"never a failure."* That was wrong. Run for real:

| live ledger | `bin/tests.sh` | verdict |
|---|---|---|
| 7 receipts (baseline) | exit 0 — **305 passed, 0 failed, 0 skipped** | — |
| **1 receipt** (`--cut 1`) | exit 1 — **285 passed, 14 failed, 6 skipped** | **not viable** |
| **2 receipts** (`--cut 2`), before the fold | exit 1 — 298 passed, **1 failed**, 6 skipped | the one failure is the fold-pending state below |
| **2 receipts, after the fold** | exit 0 — **299 passed, 0 failed, 6 skipped** | **clean** |

**The floor is 2, and it is Test 38, not Test 34.** Test 38 copies the live ledger into a temp fixture
and exits `FIXTURE SOURCE TOO SHORT: need >= 2 records, found 1`; the fixture is then never built, so
its 13 downstream assertions all error with *"handoff file not found"*. Test 34's six `SKIP` rows are
the tolerable, stated degradation — they appear at both 1 and 2, because Test 34 wants three. **So
N=1 costs a fixture rewrite in Test 38; N=2 costs six stated skips and nothing else.**

**A second constraint applies at ANY cut depth, and it is tighter than the retention question.**
`bin/tests.sh` Test 39's A2 asserts the live front matter fits a 7,168 B header reserve. A trim
appends a ~448 B pointer block, taking it to 7,440 B — **over by 272** — and the fold that the file's
own `NEXT TRIMMING SESSION` comment prescribes replaces that block with one table row, landing at
**7,139 B, under by 29**. Verified by running it, and the fold must be **its own commit** (inside the
trim commit the shipped `.verify.sh` fails L2, Learning #58). **29 B of headroom means the trim after
this one overflows the reserve** — S169 predicted exactly this. That argues for cutting deep once
rather than shallow repeatedly.

**The trim needs `--force`, and the warrant is strong rather than an override.** `--check` reports
**SRF 2.0244 (RED)**. But §11.1 of
[`srf-red-refusal-adjudication.md`](srf-red-refusal-adjudication.md) proves **every on-schedule trim
under any retention policy is refused, for any file and any depth** — the refusal votes with the
*most recent* archive, an unratified policy addition on top of H3. H3 as written votes with the
largest single drop, and the tool prints that number in the same breath: **0.1016**, deep green.
Forcing here is using the rule as written, not overriding it.

**Measured cost of the cut (throwaway clone, `--force --write`):**

| depth | live file | shard | proof | repo net |
|---|--:|--:|--:|--:|
| `--cut 1` | 75,185 → **20,820 B** | 55,368 | 16,011 | **+17,014 B (1.226×)** |
| `--cut 2` | 75,185 → **30,760 B** | — | — | — |

L1/L2/L3 all OK and the emitted `.verify.sh` exits 0. Note the ratio: at 54 KB of relief against a
**fixed** ~16 KB proof, this is far cheaper per byte than S171's trim-to-four estimate of ~1.9× —
S171's own finding that *small trims are the expensive ones*, running in the operator's favour.

**What remains for N=1:** give Test 38 a frozen fixture instead of the live ledger, the same change
Test 34 wants. `bin/check-handoff` already takes `--file PATH` (*"what tests use"*) and `--archived`,
and BL-57's P1 established `tools/fixtures/` as the pattern — but note where it lives:
`tools/fixtures/seed-CHANGELOG-ledger-format-1.md` (blob `47bc8485`) is on branch
`bl57/changelog-rules` **only**, on neither fork `main` nor `upstream/main`, so it arrives wherever
BL-57 lands. **The honest shape is a split, not a move:** whole-ledger invariants go to the fixture,
a thin assertion stays on the live file, because only the live file catches format drift a frozen
fixture cannot see.

**Still unenforced either way:** `methodology_trim.py` fires on bytes (196,608 B), never on a record
count, so any retention policy stays session-applied until the tool learns one. Teaching it a
retention mode is a **distributed** change and its own go-ahead.

**Can `CHANGELOG.md` or `BACKLOG.md` take the proof job instead? — the operator's second question.**

- **`BACKLOG.md`: no, and not close.** It holds open work only, by explicit design (*"this file holds
  open work only"*); the narrative of what was done belongs to `CHANGELOG.md`. It is a queue, not a
  record, and a completed item is *removed* from it — the opposite of a proof.
- **`CHANGELOG.md`: it already carries the *occurrence* proof, and the duplication is real.** Every
  session writes a close-out entry there, and Phase 0 reconciles it against `git log`. What it cannot
  carry is the other three things the receipt does: **(a)** the `pending` → `complete` lifecycle — in a
  repo with no `SESSION_NOTES.md`, and this is one, the committed `status: pending` receipt is the
  **only** crash breadcrumb; **(b)** a checkable schema — the 13 required keys make the six Minimum
  Handoff Requirements structurally enforceable, where a ledger entry's detail bullets are only
  *recommended*, so `CHANGELOG.md` can prove close-out *happened* but not that the handoff was
  *complete*; **(c)** per-session granularity — a session emits N ledger entries and one receipt, so
  *"did session N hand off?"* is one lookup rather than a reconstruction.

So the split to consider is not *"fold the file into `CHANGELOG.md`"* but: **`CHANGELOG.md` already
proves close-out occurred; `HANDOFFS.md`'s distinct value is the newest receipt plus the schema
check.** Which is the same conclusion the consumer table reaches from the other direction, and is why
the retention number, not the file's existence, is what this item asks the operator to decide.

**Open after the decision:** whether to apply N=2 now as the reachable floor and leave N=1 standing
as policy until Test 38 has a fixture, or to do the fixture work first and land N=1 in one step.
**Nothing adopter-facing is involved either way** — `bin/_manifest.py:58` installs
`starter-kit/HANDOFFS.md` as a seed-once file and it names **no retention number at all**, so this
repository's retention policy is fork-local. Teaching the trimmer a retention mode would be the
one distributed piece, and its own go-ahead.

**BL-58 — consider giving adopters instructions on trimming a ledger losslessly. They receive the
tool and almost none of the operating knowledge. Raised 2026-09-16 (S171, on the operator's request,
immediately after this repository trimmed `CHANGELOG.md` and hit four of the hazards below).**

**The gap, measured rather than asserted.** `bin/_manifest.py` installs
`starter-kit/methodology_trim.py` at every adopter root as a **tracked** file, so every adopter has
the tool. Guidance is a different story — `grep -ciE 'trim'` over the adopter-facing set on fork
`main`:

| file | disposition | matches |
|---|---|--:|
| `starter-kit/SESSION_RUNNER.md` | tracked | **0** |
| `FRAMEWORK_APPARATUS.md` | tracked | **0** |
| `starter-kit/SAFEGUARDS.md` | tracked | **0** |
| `starter-kit/BOOTSTRAP.md` | tracked | 6 (a table row and a file-tree caption) |
| `starter-kit/CHANGELOG.md` | **seed** | 4 |
| `starter-kit/HANDOFFS.md` | **seed** | 6 |

So the only real instructions live in the two files `bin/sync` **never overwrites once they exist**.
An adopter who seeded before a rule was written never receives it, and the one file every session
actually reads says nothing at all. (BL-57's P2 adds a *Reading and archiving* section to
`FRAMEWORK_APPARATUS.md`, which is tracked and would reach everyone — but it is on branch
`bl57/changelog-rules`, not on `main` and not upstream, and it documents reading and the trigger
rather than the operating hazards below.)

**What a trimming session has to know, and where each item was learned.** Every one of these is
either a refusal this repository hit or a defect it shipped:

1. **The tool never stages and never commits.** It leaves the live file modified and the shard
   *untracked*; committing with `-a` lands the shortened ledger while the shard never enters history
   at all — the lossless proof would then certify a file no one has. Stage both by hand.
2. **Reconcile before trimming, not after.** The `P1_UNDOCUMENTED` guard refuses while any commit
   sits unrecorded in the ledger, and it is right to: a trim advances
   `git log -1 --format=%H -- CHANGELOG.md`, so `<frontier>..HEAD` would never contain that commit
   again and Phase 0 reconcile could not recover it. **The usual discharge — naming a `--no-verify`
   housekeeping commit in the close-out entry — is unavailable here, because close-out comes after
   the trim.** S171 hit this and had to write a ledger entry mid-session to clear it.
3. **The `SRF_RED` refusal is a property of the rule, not of your file.** `regrowth / relief >= 1.00`
   is 1.0000 by construction at steady state, so it refuses any recurring maintenance policy and is
   satisfiable only by trimming *late*. An adopter meeting it needs to know that before deciding
   whether `--force` is an override or a correction; the adjudication is
   [`srf-red-refusal-adjudication.md`](srf-red-refusal-adjudication.md) §11.1, and it is **fork-only**.
4. **A trim relocates bytes; it does not free them.** Across this repository's **first ten** archive
   events: relief 1,304,337 B against additions 1,448,576 B — **net +144,239 B, every one
   net-additive** ([`srf-red-refusal-adjudication.md`](srf-red-refusal-adjudication.md) §2.3, measured
   at S124). **That figure has not been re-derived since, and there have been many trims after it** —
   re-run its accounting rather than quoting the number. Two current measurements do stand: the last
   `CHANGELOG.md` trim before S171 (`aaa6d30`) relieved 171,230 B and wrote 189,158 B, **net +17,928 B
   (1.10×)**; and the proof script is a near-fixed cost (15,992 B at v1.5.0), which is 9% of a large
   shard and 47% of a small one, so **small trims are the expensive ones.** `docs/archive/` here is
   **40.6% of the tracked repository (3,381,678 of 8,328,854 B at S171) and is inside no ceiling
   anywhere.**
5. **Run the shipped `.verify.sh`, and know it reads differently either side of the commit** — before
   it reports *"HEAD vs the working tree (trim not yet committed)"*, after it names the trim commit.
6. **For a ledger whose front matter carries a shard *table*, folding the tool's pointer block into it
   belongs in its own commit** — inside the trim commit the shipped proof fails L2 (Learning #58).
7. **A retention count is an operator decision and is not re-derivable** from any threshold in the
   tool, which fires on bytes and knows nothing about record counts.
8. **Trimming a receipt ledger moves what the whole-ledger checks see** — re-run the checker against
   each shard, and never trim to zero receipts (an empty ledger is indistinguishable from a broken one).

**The question this item exists to answer, and it is genuinely open:** *should* adopters be told all
of this, or is the honest answer that archiving is optional and most projects should never trim? The
work is a decision first and an edit second. Three shapes, none costed yet:

- **(a) A section in the tracked `FRAMEWORK_APPARATUS.md`,** beside BL-57's *Reading and archiving* —
  reaches every adopter on the next `bin/sync`, costs nothing at Phase 0 because the apparatus is read
  on demand, and is the natural home. Distributed, so it is an upstream change.
- **(b) A short procedure in `SESSION_RUNNER.md`.** Reaches the one file every session reads, and for
  that exact reason is the expensive option — the runner is already **54,363 B against a 41,364 B
  declared ceiling** on fork `main`, and `context_budget.py --status` exits 2 today.
- **(c) Leave the tool to speak for itself** and improve its own output instead. It already prints the
  rollback, the verify command and *"Then commit yourself"*; items 1, 2 and 5 could become lines the
  tool emits, which is guidance that cannot go stale in a seed.

**Related.** BL-53 (retirement policy for a grow-only file) is the same family of question one file
over. The trimmer's own design record is
[`ledger-trimmer-design.md`](ledger-trimmer-design.md). **Any distributed fix is an upstream change
and its own go-ahead.**

<a id="bl-61"></a>

**BL-61 — Lower `HEADER_RESERVE_BYTES` now that `HANDOFFS.md`'s front matter no longer grows per trim.
Raised 2026-09-16 (S174); scheduled by the operator (picker) for a later small session, not done.**

**Why.** S174 moved the shard table out of `HANDOFFS.md` into `docs/HANDOFFS_ARCHIVE_INDEX.md`
(`ad3479a`, `67ac209`). The front matter fell from 7,028 B to **4,019 B** against the 7,168 B reserve
(`bin/check-handoff:663`) — 56% used — and a trim-and-fold no longer grows it. S109 set the reserve above
the measured front matter *"and BELOW the old 8,000 so the saving is BANKED as slack"*
(`bin/check-handoff:618`). The same argument now applies: ~3 KB of reserve guards nothing, and Test 39's
A2 would not notice the front matter creeping back up by that much.

**What the session must measure and decide, not assume:**
- **The value.** Should it hold the front matter plus the trimmer's pointer block *inside* a trim commit
  (S174 measured +456 B there: 3,929 → 4,385 B), or only the size after the fold? The last three trim
  commits (`5049845`, `0ccfce8`, `1ec509d`) exceeded the old reserve before their folds.
- **Test 39's constraints.** M2's planted value (`bin/tests.sh:3164`, 2,048 B) must stay under the live
  front matter, M1's must still break A1, and A1 must still hold: 3 × 12,288 + reserve ≤ 65,536.
- **The record.** `bin/check-handoff:590`–`:631` narrates S109's reasoning and says its figures are *"a
  record of one moment"*; add a dated paragraph rather than rewriting it.
- **Scope.** Canonical-only — neither `bin/check-handoff` nor `bin/tests.sh` has a `bin/_manifest.py`
  row (checked at S174) — so no adopter impact and no upstream action.

<a id="bl-62"></a>

**BL-62 — Upstream's read-set partition test applies the one-Read sum to every whole-read class.
Raised 2026-09-16 (S177). Operator decision, after S177's close-out: carry it in BL-57's P12 pull request,
not as a standalone upstream issue.**

**What.** `test_whole_read_class_token_ceilings_partition_the_read_cap` (`tools/test_context_budget.py:1256`,
upstream `008d656`, PR #82's P0) loops over every class in `WHOLE_READ_CLASSES`
(`starter-kit/context_budget.py:83`: resident, read-mandated, read-set). For each class with two or more
token-ceilinged files, it asserts that their `max_tokens` sum to at most the 25,000-token read cap (`:1260`).
Its docstring states that rule for the Phase 0 read pair, which is read in ONE Read. A read-mandated class
holds files that are each read whole but *separately*, so the sum is not an invariant there.

**Why upstream has not seen it.** Upstream's root `.context-budget.json` declares token ceilings on two
read-set files and one resident file (checked on `upstream/main`), so no other class reaches the loop.

**How it showed here.** At resync stage M2 (`421ebf9`), the fork's root config declared 25,000 on each of
`HANDOFFS.md` and `docs/planning/BACKLOG.md` (read-mandated). That is 50,000 tokens against 25,000: a red row with
nothing wrong. It was worked around at `0e8c6ac` (operator decision) by dropping the two redundant
declarations, since the tool derives the same 25,000 per file by clamping. The fork's copy of the test stays
identical to upstream's.

**Impact: low.** The test file is canonical-only (no `bin/_manifest.py` row), so no adopter runs it. It binds
only a repository whose own config puts token ceilings on two separately-read files, and it discourages that
config.

**The change to propose.** Restrict the sum to the class that is read together (for example
`if cls != "read-set" or len(members) < 2`), or have the tool declare which classes share one Read, and keep
the presence control. Show it RED-first: a fixture config with two read-mandated files at 25,000 each fails
today and passes after, while a read-set pair summing past the cap still fails. The file is upstream-only on
the fork (`upstream-resync-2026-09-plan.md` §2.2), so where the change lands first is P12's call.

**Where it goes.** BL-57's P12 (`docs/planning/changelog-rules-contradictions-plan.md:742`), the fork's next
substantial pull request, per the batching rule in `CLAUDE.md` §Contributing upstream. Opening that PR is
its own go-ahead.

<a id="bl-63"></a>

**BL-63 — A committed-mode `bin/sync` writes more files than one commit may hold, and no distributed document
says how to commit it. Raised 2026-09-17 (S181), from BL-57 plan item (18). Operator decision the same day (picker):
for BL-57's P7–P11, one sync run is one commit; the question for every adopter goes to the upstream PR.**

**What.** `starter-kit/SAFEGUARDS.md:49` caps a commit at five files, per commit (identical on `upstream/main`).
`starter-kit/BOOTSTRAP.md:55` (*Setup with `bin/sync`*) and `:86` (*Updating an existing project*) tell an adopter to
run `bin/sync`, which copies the whole distributed corpus and does not commit. Neither says how the result is
committed, so every committed-mode sync that updates more than five files breaks the cap, or leaves the adopter to
invent a split.

**Measured.** `airqino`'s syncs `28022fe` (15 files: 14 synced plus its ledger entry) and `dfe26fd` (21). Read-only
dry runs from fork `main`: `wsfct` 14 files at `b0bf91f` (S181); `vscode_quarto_ext` 14 and `mts-system` 16 at
`b5a422b` (S180).

**Why one commit is the sound answer for a sync.** Every file is a byte-for-byte copy of a canonical blob, the dry
run lists them before anything is written, and one `git revert` undoes them all: the recoverability the cap exists
for. A split is worse, not safer. The new `SESSION_RUNNER.md` and `SAFEGUARDS.md` cite `quality_ratchet.py` and
`.quality-gates.json`, so a commit holding them without those files leaves the adopter's framework citing tools it
does not have (checked in `wsfct` at S181).

**Decided for BL-57.** `docs/planning/changelog-rules-contradictions-plan.md:198` (the decision) and `:772` (step 2):
the commit holds exactly the files the run wrote, plus its own ledger entry, and nothing else; hand edits stay in
their own commits under the cap.

**Open.** Whether the distributed `SAFEGUARDS.md` names the exception (a tool-generated copy of canonical files,
listed by a dry run, is one commit), or `BOOTSTRAP.md` says how to commit a sync, or both. Either lands at every
adopter, so it rides BL-57's P12 pull request or its own, and opening either is its own go-ahead.

---

**BL-64 — `bin/tests.sh` Test 38's drift guard read the prose between receipts as receipt fields, and the
close-out gate run is measured one commit too early to catch what the close-out writes. Raised 2026-09-17
(S182), at Phase 0, from a red quality gate on `main`. The guard half is FIXED the same session (`4c6da50`);
the timing half is open.**

**What (fixed half).** Test 38's drift guard compares the field names of the newest receipt in `HANDOFFS.md`
against the newest record in `tools/fixtures/handoff-ledger-2-records.md`, so a frozen fixture cannot rot
unnoticed. It took the live receipt's extent as *its opening fence to the NEXT record's opening fence* — the
extent `bin/check-handoff` uses for the per-record BYTE budget, deliberately, because trailing prose costs the
ledger bytes (Test 38 assertion (5)). Field names are not bytes. Between two receipts sits the close-out's
self-assessment prose, and any line of it that wraps onto a word followed by a colon was read as a field.
`HANDOFFS.md:85` wrapped onto `applied: my report named the row.`

**Measured.** In a `--no-local` clone of `29b0feb` with HEAD asserted: `quality_ratchet: 8/10 pass · 2 fail ·
results 9ccbc3cb49b6 · manifest 3a87b16f1b31` — `tests-sh-passed` 304 against the 305 floor, `tests-sh-failed`
1 against 0. The manifest digest is the same as S181's, so no threshold moved. The dashboard reached the same
reading independently: 76/100 with one HIGH flag naming both gates.

**Fixed at `4c6da50`.** The guard now loads `bin/check-handoff` as a module and calls its `scan()` — fence-bounded
and fence-nesting aware. Two assertions keep it fixed, written RED first and run in that state: a phantom field
planted in the prose below the closing fence must not reach the comparison, and the same phantom inside the fence
must still be named. `bin/check-handoff`'s `parse_block` docstring already named this hazard — *"Only recognized
keys (REQUIRED_KEYS) are captured, so free-text prose lines never masquerade as a field."*

**Open — why it shipped, which is the part not fixed.** The guard clears itself. Only a close-out puts prose
between the newest receipt and the one below it, and only some of that prose wraps onto a colon-word: S180's did
not, S181's did. The next session's Phase 1B claim then prepends a receipt with nothing after it, and the guard
reads OK again. Verified on the guard's own logic across four commits: `OK` at `755fe0d` and `b0bf91f`,
`['applied']` at `473c83d` (S181's close-out) and `29b0feb`, `OK` again at `45bf347` (S182's claim).

So the red window runs from a close-out commit to the next claim, and **nothing in the protocol looks inside it.**
`starter-kit/SESSION_RUNNER.md` Phase 3E has every close-out cite a gate run measured *before* the close-out commit
exists — the commit that writes the receipt, the ledger entry and the learnings row is the one commit its own
citation can never cover. Phase 0 of the next session is the only reader positioned to see it, and Phase 1B erases
the evidence minutes later. S181 cited `10/10 pass` in good faith and shipped a red tree.

**Shapes, none costed yet.** (a) Have the close-out re-run the gate *after* the close-out commit and amend or
follow up with the true citation — honest, but it puts a write after the write-gate. (b) Have Phase 0 record its
own gate reading in the ledger before the claim, so the window is always measured by someone — cheap, and this
session did it by hand. (c) Accept the window and make the next Phase 0's comparison mandatory rather than
customary, which is closest to what `SESSION_RUNNER.md` Phase 0 step 6 already asks for. Canonical-only either
way: `bin/tests.sh` is not in `bin/_manifest.py`, so no adopter received the defect, but the Phase 3E timing rule
IS distributed and the same window exists at every adopter that declares gates.

---

**BL-65 — `tools/test_context_budget.py`'s fit-gate end-to-end test assumes the r² floor is `calibrate()`'s only
refusal path, so it fails on a machine whose transcripts fit a negative slope — and it skips in every clone, which
is where the documented build-equivalent runs. Raised 2026-09-17 (S182), found while verifying an unrelated fix.
Not fixed.**

**What.** `TestFitGateEndToEnd.test_an_admitting_floor_prints_the_constant`
(`tools/test_context_budget.py:372`) sets `calibrate_min_r2` to `0.0` and asserts `calibrate()` returns `CLEAN`
and prints a bytes-per-token constant — the presence control for the test above it, which asserts that an
impossible floor suppresses the constant. The premise is that an r² floor of zero admits every fit.

It does not. `calibrate()` has a second, independent refusal: a **negative slope**. On this machine, right now:

```
opening_tokens ≈ 58,435 + -0.1773 × bytes      R² = 0.0004
no constant recommended — the slope is -0.1773 — more bytes fitting FEWER tokens is not a conversion
```

`rc = 1` (WARN), and no floor value can change that, because the refusal does not consult the floor. The test's
`setUp` screens only for the *"not enough"* path (`:355`), so this one reaches the assertion and is scored a
failure.

**Where it is visible, and where it is not.** The test's inputs are this machine's Claude Code transcripts —
`~/.claude/projects/-Users-rmsharp-Development-methodology/*.jsonl`, derived from the repo path at `:340`. A
`--no-local` clone has a different path, so the slug misses, so the test **skips**. The documented build-equivalent
(`quality_ratchet.py --run` in a clone with HEAD asserted, `HANDOFFS.md` §Citing the gate run) therefore never runs
it: the clone of `4c6da50` read `10/10 pass · 0 fail`, while `bash bin/tests.sh` in the working tree read
`312 passed, 1 failed`. Both readings are honest and they disagree, because they exercise different populations.

The test is not un-guarded: `bin/tests.sh` Test 18 checks the suite's exit status, and the failure surfaces through
the `tests-sh-failed` gate. Worth noting separately, though, is that the four unit-test gates in
`.quality-gates.json` — `dashboard-unit-tests`, `context-budget-unit-tests`, `trimmer-unit-tests`,
`ratchet-unit-tests` — all extract `Ran (\d+) tests`, the number of tests **run**, which is blind to whether any
passed. A failing unit test raises no alarm in its own gate; only the suite's colour catches it.

**Also note the test's own docstring is right about intent** (*"Skipped is honest; asserting against whatever
transcripts happen to be present would not be"*) — and this failure is exactly the case it was trying to avoid.
The skip guard was built for absence, not for data that is present and unfittable.

**Shapes, none costed.** (a) Widen the `setUp` probe to skip when `calibrate()` refuses for any reason, not just
*"not enough"* — smallest change, keeps the presence control where the data supports it. (b) Give the presence
control a synthetic fixture with a known positive slope, so it stops depending on whoever's machine it runs on.
(c) Leave it and accept a test that fails on some developer machines — which is what happens today, silently, since
the clone run never sees it. Canonical-only: `tools/test_context_budget.py` is not in `bin/_manifest.py`.

---

**BL-66 — `README.md`'s Quick Start tells every adopter to update from the GitHub URL, a route that cannot update
any file that is behind, and reports the refusal as "local modifications" on projects that have none. Raised
2026-09-17 (S182) from an operator question. Upstream-facing; not fixed.**

**What.** `README.md:61` (Quick Start note): *"To update an existing project to the latest version, use the same
approach: 'Update methodology using https://github.com/KJ5HST/methodology'."* `bin/sync --source=github` fetches
file **contents** only — `gh api repos/KJ5HST/methodology/contents/<path>` at `bin/sync:100` — with no git history.
The acceptance rule is *matches canonical, or any version in that source's history*; a file that is merely behind
matches an older canonical version, and with no history there is nothing for it to match. So it is classified as
locally modified and held back. **The GitHub route cannot update a file that is out of date**, which is the only
reason the route is run.

**This is already documented, in the opposite direction.** `starter-kit/BOOTSTRAP.md:86`: *"Prefer `--source=local`
from a **full** methodology checkout — an unmodified file that matches an older canonical version is recognized as
upgradable and updated cleanly with no `--force`; a shallow clone or a downloaded tarball loses that git history, so
the same files look 'locally modified' and are held back."* `--source=github` is exactly that historyless case. Two
distributed documents give opposite advice for the same operation, and `README.md` is the first one an adopter reads.

**Measured on a clean-room adopter, not inferred.** A scratch `git init` project, installed with
`bin/sync --source=local` from a checkout of `upstream/main` at `008d656`, committed, never edited — an ordinary
adopter, N versions behind, zero local modifications. Both routes then targeted `6b29d3d`:

| Route | Result |
|---|---|
| `--source=github` (what `README.md:61` tells adopters to do) | **exit 2**, nine files reported as *"local modifications"*, nothing updated |
| `--source=local` from a full checkout (`BOOTSTRAP.md:86`) | **exit 0** — 10 would be written, 1 created, 13 unchanged, no errors |

Corroborated on a real project: `wsfct`, synced clean from fork `main` the same morning with a `git status` of zero
and `--source=local` reporting all 23 files `unchanged`, was told by `--source=github` that seven files *"have local
modifications"*. They do not.

**The diagnosis is the second defect.** The message asserts a cause it has not established. `bin/sync` already has
the precedent for fixing exactly this class of misreport: `fetch_all_github`'s docstring (`bin/sync:117`–`130`)
records that a file missing upstream used to be reported as an auth failure, and concludes *"A missing file is a
VERSION statement, not a failure of the caller: this checkout's manifest is ahead of the upstream repository. Say
that, name every file, and point at the source that does work."* The same reasoning was never extended to the
modification check, where the source's lack of history — not the project's contents — is what produced the verdict.

**Shapes, none costed.** (a) Fix the README to name `--source=local` from a full checkout for updates, keeping the
URL for first install where it works correctly. (b) Teach `--source=github` to compare against upstream history
(`gh api .../commits?path=` per file, or a shallow-but-deepened clone), so a behind-but-unmodified file upgrades
cleanly. (c) At minimum, make the refusal say what it actually knows — *this source carries no history, so a file
that is merely behind cannot be recognized; re-run with `--source=local` from a full checkout* — rather than
asserting local modification. (a) and (c) are small and independent; (b) is the real fix.

**Distributed, and upstream's own front page.** Both `README.md` and `bin/sync` live in the canonical repository,
and this affects every adopter following the documented instruction, not only this fork's projects. An upstream pull
request is its own go-ahead. Not recorded anywhere before this: checked `BACKLOG.md`, this file, the archive,
`CHANGELOG.md`, and upstream issues in all states.

---

**BL-67 — `wsfct`'s report that BL-57's P7 is done and merged is owed a recording here, and the recording that was
written for it was reverted because it was written in the wrong place in the sequence. Raised 2026-09-17 (S184'),
operator-directed. Fork-only; not fixed.**

**What.** `wsfct`'s own Session 630 ran BL-57's P7 in that repository and its work was squash-merged there as
`66e14daa` (PR #903, 2026-09-18T00:36Z). The plan
([`changelog-rules-contradictions-plan.md`](changelog-rules-contradictions-plan.md) §P6–P11) expects a session
*here* to record each finished adopter phase, as S180 recorded P6: the status line, a P7 block carrying what the
phase found for the phases after it, and the BL-57 row. That recording is still owed.

**Why it is an item rather than work already done.** It *was* done, at `a6320ae`, and then reverted at `61eb9ab`.
The operator's reason is about sequence, not content: the report arrived after S183's Phase 3G close-out report,
and a close-out report ends the session. New information arriving after it belongs in this file, where the next
Phase 0 will read it and the operator can rank it against everything else open — not in a second session opened and
executed in the same breath.

**The material already exists and is re-appliable.** `git show a6320ae` is the full recording, and `git revert
a6320ae` re-applies it. It was verified read-only before it was written, with `wsfct`'s `git status --porcelain`
empty before and after: `bin/status ../wsfct` reads `CHANGELOG.md` `present`; the migration removed line 8 and lines
10–181, inside the block that session re-derived; `grep -c '^### '` went 75 → 71 (its 1 entry in, the block's 5
`### ` lines out); the source-tag audit went 72 → 70 (3 of the block's examples out, 1 entry in); `bin/sync
../wsfct --source=local --dry-run` exits 0 with 23 files unchanged; and `git diff 3a257097 66e14daa` is empty, so
the squash preserved the branch tree exactly. **Re-verify rather than trust it** — another repository's state is a
reading with a time on it (fork Learning #74), and it has already moved once: S183's handoff recorded the branch as
unmerged, and it was merged hours later.

**Three findings the reverted block carried, worth keeping whatever shape the recording takes.** (a) The P7 row's
block range (`CHANGELOG.md:13`–`196`) was stale before the phase ran and S630 re-derived it as `:8`–`182`; §9.8's
DONE check holds only against the re-derived range, so P8–P11 should re-derive at the claim and record the range in
the migration commit. (b) A pull-request-merging adopter can squash, and then item (18)'s *one sync run, one commit*
shape survives on the branch ref and not on the default branch — cite both. (c) The phase migrates `CHANGELOG.md`
and leaves the `HANDOFFS.md` seed, which `bin/status` then reports as *present (stale format)*. Measured across all
six adopters: `airqino` both `present`; `wsfct` `CHANGELOG.md` `present` and `HANDOFFS.md` stale;
`vscode_quarto_ext` and `mts-system` both stale; `nprcgenekeepr` `CHANGELOG.md` stale, `HANDOFFS.md` `present`;
`model_project_constructor` `CHANGELOG.md` stale, `HANDOFFS.md` absent. BL-56 put the other projects' *(stale
format)* verdicts explicitly outside its scope, and this plan's DONE list checks `CHANGELOG.md` only, so **no item
owns the `HANDOFFS.md` seed today** — whether P8–P11 carry it is the operator's call.

**Fork-only.** The plan, this backlog and `docs/FORK_LEARNINGS.md` are not distributed; no adopter is affected by
the recording either way.

**Closed at S185 (2026-09-17): recorded at `313459c`, by re-verifying rather than re-applying `a6320ae`.** The operator
chose this item after S185's Phase 0 (picker). Every DONE check was re-run from `wsfct`'s git objects, its working tree
clean before and after, and all of them held. One citation did not: `a6320ae` named
`origin/chore/s630-methodology-bl57-p7` as where the six commits survive, and `wsfct` deletes a branch when its PR
merges, so GitHub answers *Branch not found*. The commits are at `refs/pull/903/head` (`3a257097`), and plan item (20)
now says to cite that ref. Findings (a)–(c) above are plan items (19)–(21). Item (19) is stronger than (a) was: by
S630's own receipt, the row's 13–196 would have deleted three archive-pointer blocks. S630 also reported that
`wsfct`'s three shard proofs fail. They were re-run at S185, and all three were generated by trimmer v1.1.2 and fail
identically before and after P7. That is BL-36's class, noted in the P7 block, and it gets no new item. **Still
open, and not closed by this:** item (c)/(21), the `HANDOFFS.md` seed that no item owns, which is the operator's call.

---

<a id="bl-68"></a>

**BL-68 — Investigate the penalty the dashboard imposes for a large file when the large file is one of the
framework's own `methodology_*.py` tools (and their tests). Raised 2026-09-17 (S189) at the operator's request for
`methodology_dashboard.py`, widened the same session to every `methodology_*.py`. Not investigated yet.**

**The check.** `starter-kit/methodology_dashboard.py:3376`–`3389` (fork `main`; `upstream/main` carries the same
*Layer 7* text) raises a **medium** risk, *"Large files detected (<path>: N lines)"*, for the first file in the top-ten
`largest_files` list with more than 2,000 lines, a source extension, and no `vendor` flag. A risk subtracts no
points: the score is `score_health(metrics)` (`:3641`), computed apart from `assess_risks` (`:3642`), and the risks
feed only the project's risk level (`worst_risk`, `:3557`), which the dashboard prints beside the score.

**What is already exempt, and what is not.** *Layer 7* (`:3380`) exempts a copy the framework installed at an
adopter's root, recognized by its version line or signature (`_FRAMEWORK_INSTALLED_CONTENT`, `:764`–`:773`:
`methodology_dashboard.py`, `methodology_trim.py`, `context_budget.py`, `quality_ratchet.py`), because it was firing on 4 of 10 real repositories: *"we put our scanner in their repo, then flagged it
as their problem."* The same comment keeps the penalty in the canonical repository on purpose: it *"still pays for
the copies it authors (`tools/`, `starter-kit/`)"*.

**Measured here at S189 (2026-09-17).** This repository reads 76/100, **medium** risk, and `dashboard.html` flags
*"Large files detected (tools/test_methodology_dashboard.py: 5,867 lines)"*: the dashboard's own test file. The
dashboard itself is 4,729 lines in each of its two copies, so it trips the same check as soon as the test file is not
first in the list. **Every `methodology_*.py` here is over the 2,000-line threshold, and so are both their test
files:** `tools/test_methodology_dashboard.py` 5,867, `starter-kit/methodology_dashboard.py` and
`tools/methodology_dashboard.py` 4,729 each, `tools/test_methodology_trim.py` 2,291, `starter-kit/methodology_trim.py`
2,181 (`wc -l $(git ls-files '*methodology_*.py')`). The trimmer at an adopter's root is 2,181 lines too, so its
exemption matters there as much as the dashboard's. Fork Learning #27 records a *"Large files detected"* risk shown at every Phase 0 and read by no
one for 15+ sessions, which is the Degradation table's *"same finding for several consecutive sessions"* sign.

**To investigate:**
1. **What the penalty is, exactly.** The risk flag and the project's risk level, as above. Does `score_health`
   also count file size or lines of code anywhere in its dimensions? Read it; don't infer it from the flag.
2. **Whether it holds for every adopter copy.** Run the dashboard on the six adopters and check that *Layer 7* exempts
   each installed copy of **both** tools: one that is locally modified (`nprcgenekeepr`'s trimmer carries a 49-line local
   extension), one installed by hand, and one in an ignore-mode install. The trimmer has no fallback signature
   (`:767`–`:769`), so a copy that lost its `TRIM_VERSION` line would be recognized by nothing and penalized.
3. **Whether the canonical repository should pay for its own tools.** Each is one stdlib-only script by design,
   copied whole to adopter roots, so its size is not the smell the check looks for. The same question applies to the
   test files, one of which trips it today.
4. **Remedies, not chosen:** exempt the framework's own tool files and their tests in the canonical repository; keep
   the penalty but label it as the framework's own; split the file; or leave it as is, with the reason recorded. An
   exemption edits a distributed file, so it is upstream-facing and its pull request is its own go-ahead.

---

<a id="bl-69"></a>

**BL-69 — Delete the branches whose work is finished: 10 local and 11 on `origin`. Raised 2026-09-18 (S189), after
close-out, from the operator's question about the dashboard's *"Multiple branches (31)"*. Decided by the operator
(picker); not done.**

**What the 31 are.** `methodology_dashboard.py` counts `git branch -a`: 13 local branches plus 18 remote-tracking refs,
none stale (`git remote prune --dry-run` lists nothing). Five are `main`, `origin/main`, `upstream/main` and the two
`HEAD` aliases; two are the maintainer's (`upstream/read-set-budgets`, #80 merged; `upstream/docs/parallel-sessions-plan`,
#83 open); `bl57/changelog-rules`, local and on `origin`, is PR #84's head.

**Decided (operator, picker, S189):** delete the merged ones locally and on `origin`, and the two settled unmerged ones;
keep `docs/issue75-plan-surface-upstream` (BL-70). Measured at S189, read-only:
- **Merged in substance.** The five `fix/*` (PRs #68–#72): each local copy is a stale pre-rebase draft, and every
  commit it holds beyond its `origin` copy has a same-subject commit on that branch and in `upstream/main` (for
  `fix/handoffs-receipt-spec-upstream`, the changed lines were compared: identical). `origin/pr1`–`pr4` (#76–#79),
  `origin/docs/learning-13-handoff-predictions` (#63) and local `pr80/f1`–`f3` are ancestors of `upstream/main`.
- **Settled, unmerged.** `docs/bl-10-dangling-learning-citations`: PR #64 closed unmerged, BL-10 closed because the
  defect was fixed another way, and its `bin/check-citations` exists on neither `main`; its commits also survive
  upstream as PR #64's head. `port/framework-learnings-extraction` (local): frozen 2026-09-08 as redundant with #76.
- **The refs and shas at S189:** local `fix/bl31-context-budget-dashboard-exclusion` `9845b4d`, `fix/caveman-length-citation-upstream` `f1dd996`, `fix/dashboard-r-quarto-rmarkdown-extensions` `6380139`, `fix/doc-only-thresholds-upstream` `b52c1a9`, `fix/handoffs-receipt-spec-upstream` `311c554`, `pr80/f1-learnings-1-13` `d4e1570`, `pr80/f2-installed-source-guard` `3774076`, `pr80/f3-read-set-token-ceilings` `aa36fd8`, `docs/bl-10-dangling-learning-citations` `268f1e5`, `port/framework-learnings-extraction` `7d5b186`; origin `fix/bl31-context-budget-dashboard-exclusion` `b2ef20a`, `fix/caveman-length-citation-upstream` `b4ceb73`, `fix/dashboard-r-quarto-rmarkdown-extensions` `c4fd879`, `fix/doc-only-thresholds-upstream` `86adc6c`, `fix/handoffs-receipt-spec-upstream` `dc75cf6`, `pr1/framework-learnings-extraction` `5b92b2f`, `pr2/ledger-trimmer` `56997af`, `pr3/apparatus-extraction` `2c30d0f`, `pr4/context-budget-gate` `cf15489`, `docs/learning-13-handoff-predictions` `73b72c0`, `docs/bl-10-dangling-learning-citations` `268f1e5`.

**How, when it runs.** Re-derive every claim above first; branches move. Local `fix/*`, `bl-10` and `port/*` need
`git branch -D` (they are not ancestors of `main`); `pr80/*` take `-d`. Delete on `origin` only at the recorded sha,
`git push --force-with-lease=refs/heads/<b>:<sha> origin :refs/heads/<b>`, then `git fetch --prune origin` and record the
list in the ledger. After it, `git branch -a` still reads about 10, so the signal still fires: that is BL-71.

---

<a id="bl-70"></a>

**BL-70 — Upstream's runner lacks the plan-surface rule from issue #75, which the maintainer closed silently.
Raised 2026-09-18 (S189), after close-out. Operator (picker): a backlog item, keep the unsent branch. Not decided
beyond that.**

The maintainer filed [issue #75](https://github.com/KJ5HST/methodology/issues/75). The fork commented on 2026-08-16,
ending *"I won't send anything unasked"*; prepared the PR on 2026-08-24 (branch `docs/issue75-plan-surface-upstream`,
`60246e7`, local only, never pushed); and verified it ready on 2026-09-01
([`issue75-pr-readiness-2026-09-01.md`](issue75-pr-readiness-2026-09-01.md)). KJ5HST closed the issue on 2026-09-02 with
no comment and no commit. Fork `main`'s runner carries the rule (§Planning Sessions: each phase names its **surface**);
`upstream/main`'s does not, so adopters syncing from upstream never get it. Nothing in this repository records the
closure or a decision about it before now. The branch is based on `512c2ed`, now far behind `upstream/main`.
**Open:** ask the maintainer on #75 whether he wants it (an outward action, its own go-ahead), fold it into a later
PR, or record it as declined and delete the branch.

---

<a id="bl-71"></a>

**BL-71 — The dashboard's *"Multiple branches"* signal counts `git branch -a`, so a fork can never clear it.
Raised 2026-09-18 (S189), after close-out. Operator (picker): add it. Not investigated.**

`starter-kit/methodology_dashboard.py:1522`–`1523` counts every line of `git branch -a`, and `:3396`–`3397` raises a low
risk above 5. That count includes the two `HEAD` aliases, all three `main` refs, the upstream's own branches (which a fork
always carries), and an open PR's head. After BL-69 this repository still reads about 10. A count of local branches not
merged into `main`, or one excluding remote-tracking refs and aliases, would say what the message claims (*"may indicate
incomplete merges"*). A fix edits a distributed file, so its upstream PR is its own go-ahead; same family as BL-68.

<a id="bl-72"></a>

**BL-72 — `bin/check-handoff` skips the newest receipt in any `HANDOFFS.md` that carries the seed's size section, and
still reports OK. Raised 2026-09-18 (S191), from BL-57's P8 report; reproduced here. Operator (picker): fix before P9.**

The seed's `## Size, and when to archive` section (`starter-kit/HANDOFFS.md:89`, on `upstream/main` and fork `main`
alike) holds a ```` ```sh ```` code block. `scan()` (`bin/check-handoff:254`–`:290`) recognises two openers only: a bare
run of backticks (a wrapper) and ```` ```handoff ````. A fence with any other info string is read as prose, so the
block's closing ```` ``` ```` is taken as a bare wrapper *opener*, and the scanner skips to the next bare fence of three or
more backticks: the closing fence of the first receipt. That receipt is never parsed. The checker then validates the
second receipt as the newest and exits 0; `--all` counts one fewer.

**Reproduced at S191.** Two fixtures built from this repository's two receipts: without the section, *"all 1 older
receipt(s)"*; with it above them, *"all 0 older receipt(s)"*, and `--all` reads 1 receipt, both OK. On the real files,
`scan()`'s first block is the second receipt in `vscode_quarto_ext` at `57750bb2` (S264 skipped; line 94 unread, 109
read), `airqino` (S19, 158 unread) and `nprcgenekeepr` (S714, 146 unread), the last two through an older copy of the same
section; `mts-system` reads its newest (line 77) until BL-57's P9 adds the section. **Not affected:** the distributed
`methodology_trim.py`, which counts all 17 records in `vscode_quarto_ext`, S264 among them; and this repository's own
gates, since its `HANDOFFS.md` has no such block. Test 38's drift guard calls this `scan()` (`4c6da50`), so it inherits
the defect on any ledger that has one.

**Fix shape (not built):** CommonMark's rule, which the scanner's docstring already cites for wrappers: an opening fence
is three or more backticks followed by an optional info string, and it closes only on a bare run at least as long. So a
non-`handoff` fence is skipped to its closer, as a wrapper is. RED first on the two fixtures above, plus an
`sh` block *inside* a receipt's prose tail and one inside a four-backtick wrapper. The checker is
canonical-only, so no adopter receives it (adopters may copy it, `starter-kit/SAFEGUARDS.md` §Close-Out Completeness
Hook); the fix still goes upstream, where the seed carries the same block: inside PR #84 (whose route puts the section
into adopters' files) or as its own PR, decided in the fix session, its own go-ahead.

**Closed at S192 (2026-09-18): fixed as shaped above, on `bl57/changelog-rules` (`77afc12`) so it rides PR #84 (the
operator's choice, picker, over its own PR or fork `main` only), and merged into fork `main` as `ea1a057`.** Beyond the
shape: an info string may not contain a backtick, so a prose line that starts with inline code quoting a fence opens
nothing; the skipped block's lines stay visible to the orphan check, so a receipt under a misspelled tag is reported at
its own lines; an unclosed one is a finding, like an unclosed wrapper. A `handoff`-tagged fence takes the old paths
unchanged. Ten assertions in `bin/tests.sh` Test 22 (six failed on the unfixed checker); six mutants of the fix each
fail one or more. Re-read against the three adopters, read-only: the first block `scan()` returns moved from S18 to S19
in `airqino`, S714 to S715 in `nprcgenekeepr` (which has moved on since S191) and S263 to S264 in `vscode_quarto_ext`;
`mts-system` is unchanged. Found while verifying, and filed apart: BL-73.

**BL-73 — `bin/check-handoff` reads a second `handoff` opener inside an open receipt as content, so a receipt begun
twice reads as one block, and `--all` reports it only when the key order breaks. Raised 2026-09-18 (S192), while
verifying BL-72 on `mts-system`. Not fixed.**

**What.** `scan()`'s receipt loop (`bin/check-handoff:289`–`:306` on fork `main` since `ea1a057`) collects every line up
to the first bare fence as the receipt's content, including a line that is itself a `handoff` opener. `mts-system`'s
`HANDOFFS.md` (read at `710a0f7`, the file last changed 2026-09-15) holds three instances of one shape: an opener and a
`session:` line (at `:320` a `date:` line too), a blank line, then a second opener carrying the whole receipt. They are
`:216`/`:219` (`S131`), `:320`/`:323` (`S126`) and `:671`/`:674` (`S106`); each reads as one block. `--all` reports `:216`
and `:671` only through `validate_ledger`'s key-order rule (*"first two keys must be `session` then `date` (got session,
session)"*). `:320` passes, because its `date:` comes before the second opener. BL-57's P9 row named only `:216`.

**Fix shape (not built).** A `handoff` opener inside an open receipt is a structural finding in `scan()` (*"a receipt
opened at line N is opened again at line M before it closes"*), so `--all` reports every instance whatever the key
order. RED first, on the three `mts-system` shapes as fixtures. The checker is canonical-only; its upstream route is its
own go-ahead. `mts-system`'s ledger is that project's: repairing it belongs to P9 or to that project, not to this item.

<a id="bl-74"></a>

**BL-74 — Keep `README.md` from going stale: the canonical one, and the copies adopters carry at
`docs/methodology/README.md`, which `bin/sync` never updates. Raised 2026-09-19 (S195), on the operator's request. Not
investigated past the measurements below.**

**The request.** The operator, at S195: *"add to backlog to ensure methodology/README.md is not stale."* That path fits
two files, so both were measured, read-only, against fork `main` `00893e0`, whose first-parent history holds 63
versions of `README.md` (last changed 2026-09-16, `fd611a65`).

**The adopters' copies.** `bin/_manifest.py` does not distribute `README.md`, so a copy an adopter took at bootstrap is
never refreshed by `bin/sync`, and `bin/status` never lists it. Five directories under `~/Development` carry
`docs/methodology/README.md`: `model_project_constructor` holds the 2026-05-25 version (`d7fcd6ab`), 39 README commits
behind; `airqino` 2026-06-22 (`90bad48e`), 31 behind; `nprcgenekeepr` 2026-07-08 (`d1396420`), 24 behind;
`dalia_martinez_funeral` 2026-07-08 (`c7f10b42`), 23 behind; `feedback-loop-comparison` matches no version of the file on
any ref (edited there, or from history the fork no longer holds: plan item (32)). No other directory there has one.
`model_project_constructor`'s `NOTICE` counts its copy among the methodology material, so the copy is tracked there on
purpose.

**The canonical `README.md`.** Spot-checked, not audited: `:241`'s *"28 known failure modes"* matches the runner, and
`:528`'s *"27"* sits inside the v3.1 entry, true when written. Known stale: the fork-only cost section (`:383`, `:398`)
still describes S42's 2026-08-04 measurements and a 2,000-line cap, recorded as found-not-fixed at
`changelog-rules-contradictions-plan.md` item (15) (`:185`). Fork `main`'s `README.md` differs from `upstream/main`'s by
168 lines added and 5 removed, most of them that section.

**Shapes (none chosen).** (1) Distribute it: add `README.md` → `docs/methodology/README.md` to `bin/_manifest.py`, so
`bin/sync` keeps copies current and `bin/status` reports them. That edits a distributed file, so it is an upstream PR
and its own go-ahead, and the fork-only section would ship unless it moves out first. (2) Stop carrying copies: each
adopter drops its copy for a link to the canonical file; each adopter's call. (3) A check on the canonical file itself:
its counts and file lists against the runner and the manifest. By the runner's Phase 3C rule, a mechanical invariant is
a gate, not a row. (4) Rewrite the stale section, item (15); fork-only. The design session starts by settling which of
the two files the request meant, or both.

<a id="bl-75"></a>

**BL-75 — `context_budget.py` has no `--status` command, and an unknown argument is silently ignored, so every
*"`context_budget.py --status`"* this repository has ever cited ran the default measurement. Raised 2026-09-19 (S195),
from BL-57's P11 report (plan item (35)). Not fixed.**

**What.** `python3 starter-kit/context_budget.py --help` lists the default run, `install-hook`, `--precommit`,
`--calibrate`, `--selftest` and `--json`. There is no `--status`. Measured here: `python3 starter-kit/context_budget.py
--zzz-nonsense` exits 2, performs the default measurement and appends a row to the tracked
`.context-budget-history.jsonl` — so the argument is not rejected, and the writing side effect happens either way.
`model_project_constructor`'s Session 259 found it while following S195's launch prompt, which cited the flag twice.

**Where the string is.** This repo's `CLAUDE.md:81` (*"reported by `--status`"*), scores of `CHANGELOG.md` entries and
archived receipts, both adopter launch prompts, and `docs/planning/pr82-comment.md:131` and `pr82-review.md:155`, which
propose `python3 starter-kit/context_budget.py --status` to the maintainer as a declared gate command. **No declared
gate runs it today:** `.quality-gates.json:37` runs `tools/test_context_budget.py`.

**What is and is not wrong.** The readings those sessions reported are sound — the default run measures and prints the
same ledger — so no number needs revisiting. What is wrong is the citation, the advice in a PR comment, and the premise
that a gate could be declared on that string: declared, it would measure the default run and append a tracked row on
every invocation.

**Shapes (none chosen).** (1) Add `--status` as an explicit alias of the default run — smallest, makes every existing
citation true, distributed, so an upstream PR and its own go-ahead. (2) Reject unknown arguments (exit 3, the tool's own
usage code) and correct the live citations — honest, but a bare `--status` in an adopter's habit then fails. (3) Correct
the citations only. Whichever is chosen, the PR-comment text is outward-facing and already sent; correcting it there is
its own go-ahead.

**Observed a second time, 2026-09-20 (S198), in this repository rather than in an adopter's.** Phase 0 ran
`python3 starter-kit/context_budget.py --status` from this repo's own `CLAUDE.md:81` citation. The argument was
silently ignored, the default measurement ran, and a row was appended to the tracked
`.context-budget-history.jsonl` — during a phase the runner declares read-only apart from the reconcile backfill. The
row was reverted (`git checkout --`) and the reading itself was sound, as this item already says. Recorded as
evidence that the wrong citation keeps being followed by sessions reading the live file; nothing above is edited.

<a id="bl-76"></a>

**BL-76 — `.git/REBASE_HEAD` disarms `.githooks/pre-commit` for the life of a clone, so both gates it
chains stop running. Found 2026-09-19 (S197).**

**✅ CLOSED 2026-09-20 (S198) by shape (1), chosen from the three below on measured grounds rather than on
size.** Everything below is the item as it stood; the closure note is at its end.

The hook skips replayed commits by exiting 0 if any of `MERGE_HEAD`, `REBASE_HEAD`, `CHERRY_PICK_HEAD`,
`rebase-merge` or `rebase-apply` exists under the git dir (`.githooks/pre-commit:24`). Git **removes**
`MERGE_HEAD`, `CHERRY_PICK_HEAD` and the `rebase-merge` / `rebase-apply` directories when the operation
ends — but it **leaves `REBASE_HEAD` behind after a rebase completes.** So a single rebase, ever, disarms
the hook permanently in that clone. The marker loop runs **before** both gates the hook chains, so the
casualty is not only the FM #27 ledger gate but `quality_ratchet.py --precommit`, whose whole job is to
refuse a loosened threshold.

**Measured here, not inferred.** `.git/REBASE_HEAD` was dated **2026-08-11 15:14**, pointing at
`d56b983`, a commit not in this history — a dropped one from that rebase. On this clone's first-parent
line, **69** commits since that timestamp changed tracked content without co-staging `CHANGELOG.md`:
each would have been refused, or needed `--no-verify`. The count is the hook's exposure, **not** a count
of unrecorded actions — that question belongs to Phase 0 reconcile, which has reported clean every
session, and which caught this session's own ungated commit (`9344c3e`, half a fold) one commit later.
**The fast path was off for five weeks and the guarantee held**, which is the division of labour
`SAFEGUARDS.md` claims for the pair; it is the first time this repo has measured it.

**Scope.** `.githooks/pre-commit` is **canonical-only** (BL-6 item 3, deliberately not distributed), so
no adopter is affected — but `upstream/main` carries the same hook text, so a fix is an upstream change
and **its own go-ahead**. The marker was removed in this clone (backed up first), which **re-arms the
gate and is not the fix**; a control commit confirmed the refusal fires again.

**Shapes (none chosen).** (1) Drop `REBASE_HEAD` from the list — the `rebase-merge` / `rebase-apply`
directories are the real in-progress indicators, and `git rebase` creates one of them for every rebase
type. (2) Test only for the directories and `MERGE_HEAD` / `CHERRY_PICK_HEAD`. (3) Keep the list but
require the marker to be *newer than the index*, which is the general form and the most fragile. Any of
them needs a RED-first test; `.githooks/commit-msg --selftest` is the precedent for a hook that tests
itself, and `.quality-gates.json` already runs that selftest as a gate.

**Closure (S198, 2026-09-20).** **Shape (1)**, and the choice was made from a measurement rather than from
which edit looked smallest. Every git operation in the list was run to completion on git 2.50.1 and its
markers observed at each stage:

| operation | markers while in progress | survives completion |
|---|---|---|
| rebase, no conflict | (never stops) | — |
| rebase stopped by a conflict | `REBASE_HEAD` + `rebase-merge` | **`REBASE_HEAD`** |
| `rebase --apply`, conflict | `REBASE_HEAD` + `rebase-apply` | — (abort clears) |
| `rebase -i` parked at `edit` | `REBASE_HEAD` + `rebase-merge` | **`REBASE_HEAD`** |
| merge, conflict | `MERGE_HEAD` | — |
| cherry-pick, conflict | `CHERRY_PICK_HEAD` | — |
| `git am`, conflict | `rebase-apply` | — |

Two facts settle it. `REBASE_HEAD` is the **only** marker that leaks — the other four are removed when
their operation ends or is aborted, so none of them needs the same treatment. And it is **redundant**:
every rebase in-progress state carries a *directory* alongside it, so dropping it costs no in-progress
coverage. That makes shape (3)'s newer-than-the-index comparison unnecessary as well as fragile, and shape
(2) the same marker set as (1) by another description. A third measured fact explains the five weeks: a
**clean** rebase leaks nothing, so only a rebase that *stopped* arms the trap.

**What shipped.** `REBASE_HEAD` dropped from the marker loop, with the measurement in a comment beside it;
a **`--selftest`** on the `.githooks/commit-msg --selftest` precedent (10 checks); the gate
`pre-commit-selftest` in `.quality-gates.json`; and `bin/tests.sh` **Test 43** (10 assertions), which reads
the marker names off the `for marker in` line rather than off the file — the fix's own comment names
`REBASE_HEAD` a dozen times, so a bare grep would report the bug cured while it stood.

**Proof.** RED-first: the selftest was written against the **unfixed** hook and went red on exactly one of
its ten assertions, the other nine green, so it isolates the defect instead of being vacuously red; 0 red
after. Mutation: **10 mutants, 10 killed** — restoring `REBASE_HEAD`; dropping each of the four remaining
markers; `-e` narrowed to `-f`; deleting the loop; short-circuiting each of the two gates; and breaking the
fixture builder, which the selftest's own fixture assertion catches (a probe run against a repo that failed
to build answers about nothing, and would do it in green).
End-to-end against real git, not planted files: a real conflicted rebase was completed, the leaked
`REBASE_HEAD` confirmed, and a real `git commit` without a ledger line **refused** (exit 1); co-staging the
ledger passed (exit 0); and committing *during* a genuine in-progress rebase was still **skipped** (exit 0).

**Not done, deliberately, at S198.** `upstream/main` carries the same hook text and the same defect. The hook is
canonical-only (BL-6 item 3), so **no adopter is affected** and the upstream fix is **its own go-ahead** —
it did not ride that session.

**S199 (2026-09-20): SENT — [PR #85](https://github.com/KJ5HST/methodology/pull/85), OPEN, MERGEABLE, head
`e2501c5`, 3 files, +131/−1.** Operator go-ahead in the Phase 0 picker, over this session's recommendation to
hold it until PR #84 moves. **Re-derived against `upstream/main`, not cherry-picked:** upstream's hook differs
from the fork's pre-fix text in two words of the error message, and upstream has **no Test 43 and no
`bin/tests.sh` coverage of a hook selftest at all** — its precedent is the *gate*, `commit-msg-selftest`, so the
PR adds `pre-commit-selftest` beside it and leaves `bin/tests.sh` untouched. Measured on upstream's tree in a
`--no-local` clone with HEAD asserted by sha: before `6b29d3d` **139 passed / 0 failed**, gates `10/10 · results
6542e640a956` — **the same `results` hash upstream's own newest receipt cites**; after, **139 / 0 unchanged**,
gates `11/11 · results acddacb93988 · manifest ec617cec62ed`. RED-first 1-of-10 red before and 0 after, **10
mutants 10 killed**, and the end-to-end control run on upstream's text: the unfixed hook lets the unledgered
commit through (exit 0) in the identical scenario where the fixed one refuses it. One scope correction the fork
row did not make: `.githooks/` is not in `bin/_manifest.py`, but the **distributed** `SAFEGUARDS.md` calls this
file the canonical reference implementation and tells adopters to enable it, so an adopter who followed that
instruction copied the defect. **Open until the PR is reviewed.**

<a id="bl-77"></a>

**BL-77 — Phase 0 reconciles the ledger but never checks that the gates protecting it are armed in this
clone. Raised 2026-09-20 (S198), from BL-76's closure. Not fixed.**

**What.** Phase 0 step 6 verifies the *record* thoroughly — both frontiers against `git log`, pending stubs,
and the newest receipt's `quality_ratchet` citation. Nothing verifies that the mechanism guarding that
record is switched on. `core.hooksPath` is **per-clone** and opt-in (`BOOTSTRAP.md` Step 10), so a correct
hook in a correct `.githooks/` does nothing at all in a clone where it was never enabled, and every gate
still reads green: the hook fails **open**, so its failure mode is silence.

**Why it is not already covered.** S198's new `pre-commit-selftest` gate tests the hook's *logic*; it says
nothing about whether that hook is *wired in* here. The two are independent, and BL-76 was the second of
the pair: the hook was enabled and correct-looking, and still ran nothing for five weeks. It was found by
luck — S197 went looking only because one of its own commits landed ungated (its self-assessment says so).

**Scope.** Canonical-only in its current form, since `.githooks/` is not distributed. The general shape —
*a project's Phase 0 should confirm its own gates fire* — is not, and BL-58 is the adjacent distributed
question.

**Shapes (none chosen, none measured).** (1) A Phase 0 read-only line reporting `git config core.hooksPath`
— cheapest, but the runner's own Degradation Detection table says a signal nothing gates on is not the
remedy. (2) A `bin/tests.sh` assertion — but the suite runs in clones where an unset `core.hooksPath` is
legitimate, so it would be wrong exactly where it ran. (3) Have the hook record that it fired, and have
Phase 0 read that trace against the commits in the span it is already reconciling. Each needs its own
RED-first proof; none has been costed.

<a id="bl-78"></a>

**BL-78 — `starter-kit/SAFEGUARDS.md` has been over its declared no-growth pin since 2026-09-14, and
nothing in the commit path measures it. Raised 2026-09-20 (S200), at Phase 0. Not fixed.**

**What.** `.context-budget.json` gives `starter-kit/SAFEGUARDS.md` a `max_bytes` of **15,386 B** and says
in its own `_` note that this **is the file's current size** — *"a deliberate no-growth pin rather than a
measurement dressed as a budget"*, with *"at exactly 15,386 B the file is AT its ceiling, not over: `new >
ceil` is strict, so today's content passes and the next byte does not."* The file is **17,129 B — 1,743 B
over.** Measured back through its history, it passed the pin at `ad7bd37` (2026-09-14, 16,353 B) and grew
in three further commits: `628d218` (16,765 B), `df926b6` (17,024 B), `0d63410` (2026-09-17, 17,129 B).

**Why nothing said so.** Two independent reasons, and the second is the substantive one.

1. **No gate measures it.** `python3 starter-kit/context_budget.py` is **not** run by
   `.githooks/pre-commit`, and `.quality-gates.json` declares no budget-status gate — only
   `context-budget-unit-tests`, which tests the tool, not this repository's budget. So the sibling entry's
   claim for the read-set pair — *"every commit that grows it is refused while every commit that shrinks
   it passes: a ratchet, not a wall"* — describes an enforcement that is **not wired in this clone**.
2. **The checker was already red, so the new row carried no news.** The read-set total and
   `SESSION_RUNNER.md` are over by design (*"being over on arrival is the POINT"*), so
   `context_budget.py` exits non-zero every run and the `SAFEGUARDS.md` row's flip from `ok` to `over` sat
   in output nobody diffed. **That is fork Learning `#62` exactly**, in the one file whose entry says a
   size finding here *is* actionable.

**Why it matters more than 1,743 B — measured, not left as a question.** The pin's stated warrant is that
the file is **byte-identical on `upstream/main`** (blob `f0964195`), *"so pinning it here cannot diverge
the two trees"*, and the sibling's whole 12,999 B of headroom debt was parked on `SESSION_RUNNER.md` on
that basis. **Both halves of that warrant are now false.** Ours is `ed49b977` (17,129 B), upstream's is
`933816b4` (17,024 B) — **neither is `f0964195`, so the cited blob is stale on both sides** — and the two
have **diverged**. The divergence is exactly one line: upstream's blob equals the fork's blob at
`df926b6`, and the only content commit the fork carries beyond `upstream/main` for this path is
**`0d63410`** (BL-63, 2026-09-17), `git diff upstream/main HEAD -- starter-kit/SAFEGUARDS.md` reading
**1 insertion, 1 deletion**. So this is a small, well-understood divergence in an **upstream-facing**
file, not a mystery — but it is a divergence the config says cannot happen, in the note that justifies
where a 12,999 B debt was parked.

**Not investigated, and deliberately not fixed here** (FM #17, FM #18): this was a Phase 0 finding in a
session whose deliverable was BL-53 P3. **Shapes, none costed.** (1) Re-pin: if the growth was intended
and upstream carries it too, move the number and say why. (2) Wire the gate: add a budget-status gate to
`.quality-gates.json` so the pin refuses rather than reports — which is BL-77's shape for a different
mechanism, and inherits its objection that a clone is a legitimate place for it to be unset. (3) Leave the
number and treat the row as a reported series, which is the same question BL-53's option C asks about a
different file. **The blob comparison is already done (above), so the open question is not *what
happened* but *which number is right now*: re-pin at 17,129 B, re-pin at upstream's 17,024 B and treat
`0d63410` as the fork's own delta, or stop pinning this file at all.**

**SECOND INSTANCE, AND THE RATCHET IS NOT MERELY UNWIRED — IT DOES NOT EXIST. Measured at S201's Phase 0.**
The sibling this item already quotes has breached the same way: `starter-kit/SESSION_RUNNER.md` is
**55,406 B against the `measured_bytes` 54,363 B its own entry declares**, written at `beffbd0e`
(2026-08-30) — **+1,043 B** — under the note that says *"every commit that grows it is refused while every
commit that shrinks it passes: a ratchet, not a wall."* Both read-set files have now grown past their
declared sizes, so shape (1)'s *"which number is right now"* question is owed twice.

**Verify the size at the blamed commit, not from position in `git log`.** `git log --since=... --
starter-kit/SESSION_RUNNER.md` reports the file at 52,195 B on 2026-08-28 and no change until
2026-09-15, which would make the declared 54,363 B look invented; history simplification had pruned the
resync merge. `git cat-file -s beffbd0e:starter-kit/SESSION_RUNNER.md` reads **54,363 B exactly**. The
config is right and the first instrument was wrong.

**And there is no per-file growth check for the tool to be wired to.** `measured_bytes` appears **exactly
once** in `starter-kit/context_budget.py` (`:398`) and feeds **only a density-drift warning**, itself
gated on `status == "ok"` — so for a file already `over`, which this one is by design, it does not even
emit that. Nothing in the tool compares a file to its own previous size. The one growth signal it does
have, `growth_run` (`:518`), is *"a series over `resident_bytes`"* (`:622`) — **`CLAUDE.md` alone**, which
is why the run counter read 159 while both read-set files were quietly growing. So reason 1 above holds at
two levels: **no gate runs the tool, and for these files the tool has no growth refusal to run.** Shape
(2) is therefore larger than *"add a gate"* — it has to build the check first, which is a point in favour
of shape (3) for exactly the reason BL-53's option C was ratified.
