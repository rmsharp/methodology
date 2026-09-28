# Handoff Receipts — durable close-out proof

This repository dogfoods its own methodology: every session records a durable, machine-checkable
`handoff` receipt here at close-out (Phase 3D), and Phase 0 reconciles it against `git log`. See
[`starter-kit/HANDOFFS.md`](starter-kit/HANDOFFS.md) for the block format and the write points, and
`bin/check-handoff` for the checker. Newest on top; prepend-only.

**Retention policy — keep ONE receipt, trim above TWO.** Everything older is archived under
`docs/archive/` and indexed in [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md). **N=1 is an operator decision (2026-09-16, S172)
replacing S127's N=4**, taken against BL-59's measurement of what actually reads this file: the
handoff is done by the newest receipt alone. **Depth and trigger are separate on purpose:**
every trim pays a FIXED ~16 KB proof, so the trigger sits one above the depth (BL-60). **`methodology_trim.py` fires on BYTES (196,608 B),
never on a record count**, so the policy is applied by the session that notices: Phase 0 runs
`grep -c '^```handoff' HANDOFFS.md` and reports the count; **above 2**, the trim is its own action after
that report, never inside Phase 0, which is read-only apart from the reconcile backfill
(`starter-kit/SESSION_RUNNER.md` Phase 0): `--cut 1 --force`. The force is
warranted, not an override — `SRF_RED` refuses every on-schedule retention trim by construction
(BL-59). `bin/check-handoff` validates the 13-key schema on the **newest** receipt; `--all` checks
every receipt and `--archived` a frozen shard. Below three receipts Test 34 prints six named `SKIP` rows — stated, never silent.

**Two session sequences share this ledger and their numbers collide.** This fork and
`upstream/main` each run their own `S<N>` counter, so a receipt is identified by **session + date**,
never by number alone. **Every upstream receipt is now archived**; every receipt retained here is
the fork's. At a resync the two sequences stay separate and unrenumbered, each incoming receipt is
checked against ours before it is kept, and within a shared date the fork's precede the arriving
upstream ones (precedent: `fc4d297`).

> **THE HAND-MAINTAINED RECEIPT COUNT IS GONE, DELIBERATELY.** S172's rewrite dropped *"This file
> currently holds **N**"* — the number [Learning #12](starter-kit/FRAMEWORK_LEARNINGS.md) and upstream
> [issue #65](https://github.com/KJ5HST/methodology/issues/65) both cite as always wrong by the next
> close-out. The trimmer still declares it, so **every trim now reports `FRONTMATTER_FIELD_ABSENT`**:
> stated, expected, not a failure. Removing the declaration is distributed — its own go-ahead (BL-60).
> **Count with `grep -c '^```handoff' HANDOFFS.md`.**

> **⚠ THREE is the floor the retention policy sits one above.** `bin/tests.sh` Test 34 mutates *this*
> ledger to check `check-handoff --all`'s whole-ledger invariants, reading two anchors from the live
> file — not hardcoded, so it survives *which* receipts rotate, but it needs three to exist. A short
> ledger is **stated rather than silent** (BL-40 (b)): below the floor those six assertions print as
> `SKIP` rows naming themselves, the summary carries a skip count, and a ledger with *zero* receipts
> still FAILS — corruption is not rotation. **Nothing prevents a cut below three; the policy is what
> makes it not happen.** Re-run `bash bin/tests.sh` after any trim of this file.

**The shard index is not in this front matter, on purpose.** It lived here until S174 and grew a row
with every trim against the fixed 7,168 B header reserve (Test 39 A2), so it moved out rather than the
reserve rising. A trim commit still carries the trimmer's ~448 B pointer block; the fold removes it, so a
trim-and-fold no longer grows this front matter. The fold rule is in the index.

<!-- NEXT TRIMMING SESSION: methodology_trim.py appends a 3-line pointer block here
     (starter-kit/methodology_trim.py:1093 build_pointer_block, :1103 insert_pointer). Fold it into
     docs/HANDOFFS_ARCHIVE_INDEX.md as one row and delete the block, IN ITS OWN COMMIT: inside the
     trim commit the shipped .verify.sh fails L2 (fork Learning #58). -->

**Archived 1 record(s), 2026-09-27 → 2026-09-27** into [`docs/archive/HANDOFFS-through-2026-09-27-4.md`](docs/archive/HANDOFFS-through-2026-09-27-4.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/HANDOFFS-through-2026-09-27-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-27-4.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

```handoff
session: S229
date: 2026-09-27
status: pending
active_task: **P1 of the BL-88 plan: the read-cap row stops asserting what it never checked.** The operator decided both changes at S228's report — **fix the message, fork-side only, NO upstream pull request**, and add the trimmer probe as a **source-text read** rather than an execution. **The probe is P2 and is NOT this session**; it now carries zero open decisions. **This session:** the Class B over-cap row (`tools/methodology_dashboard.py:3511-3528`) drops *"the trimmer answers `NO_CONFIG` for it"* — a claim about another tool's config the dashboard never reads — and confines the backlog-specific *"a backlog's bottom items are as live as its top ones"* to the three backlog names, stating `SESSION_NOTES.md`'s caveat in the weaker form the module comment at `:381-396` already settled. **RED first.** `tools/test_methodology_dashboard.py:5800` asserts `"NO_CONFIG"` is present and **must change deliberately, not be deleted** — its purpose survives, only the *why* changes. **The two class pins at `:5464`/`:5485` are untouched**: no name moves class, nothing becomes derived, dragon 6 is not engaged. `starter-kit/` twin mirrored **LAST**. Fork-only; **nothing on `KJ5HST/methodology`, and no PR was granted.**
```

```handoff
session: S228
date: 2026-09-27
status: complete
self_score: 8
predecessor_score: 8
active_task: **DONE: `CHANGELOG.md` IS ARCHIVED AT THE CLEAN 2026-09-22 CALENDAR SEAM — the operator's choice among three cuts costed at S227's Phase 0.** `d23c811`: **85 of 137 records** (2026-09-21 → 2026-09-22) into [`docs/archive/CHANGELOG-through-2026-09-22.md`](docs/archive/CHANGELOG-through-2026-09-22.md), a name no shard had taken, so **no `-N` disambiguator**; live **249,268 B → 130,729 B**. That moves the headroom against the 262,144 B hard read refusal from about **13,000 B — under one session — to 131,415 B, about eight** at the measured 16,074 B/session. **The live file now holds 2026-09-26 onward** and 54 entries. The figures were **re-derived twice, never quoted**: S227 costed this cut at 236,905 B → 118,366 B over 130 records, the claim re-derived 248,167 B → 129,628 B over 137, and the write landed at 249,268 B → 130,729 B, because every entry between the readings — including the claim's own — sits on the retained side. `SRF_RED` refuses this trim by construction, so `--force` was warranted, not an override; **there is no fold for this file.** Fork-only; **nothing on `KJ5HST/methodology`.**
what_was_done: **Before claiming, a defect in S227's own close-out was repaired** (`3815b83`): Phase 3D OVERWRITES the Phase 1B stub, and that close-out PRECEDED it, so `HANDOFFS.md` carried **two `session: S227` blocks** — cause, a `git checkout -- HANDOFFS.md` undoing an over-budget draft restored the committed stub, and the finished receipt was then prepended rather than substituted. 1,500 B removed, back to 2 receipts. **Caught before the next retention trim could freeze the duplicate into a shard and its proof.** **Orientation was carried, not re-run** — S227's Phase 0 had measured everything minutes earlier and the only tree changes were its own commits plus that repair. **Then, in order:** claim `1230dc0`; the deliverable `d23c811`; the owed `HANDOFFS.md` retention trim `0038441` (**S227's `-3` forecast exact**: S226's receipt, 29,818 → 18,138 B) and its fold `c72ad24` (452 B → a 122 B row, index **64 → 65**, own commit per fork Learning #58); Phase 3C `da2ec5f`. **THE nprcgenekeepr QUESTION WAS ANSWERED FROM THAT PROJECT'S OWN CONTRACT AND IT OVERTURNED MY OWN READING** — see gotcha (2).
next_steps: **(1) `CHANGELOG.md` NO LONGER LEADS THE LIST — it is 130,729 B with ~131,415 B of headroom, about eight sessions.** Re-measure at Phase 0 anyway (fork Learning #61); raise the next trim on the refusal, never on `--check`, which still fires and will keep firing. **(2) BL-88 PART 1 IS THE DECIDED, UPSTREAM-FACING WORK AND IT IS ONE SESSION** — [`dashboard-read-cap-class-adopter-drift-plan.md`](docs/planning/dashboard-read-cap-class-adopter-drift-plan.md) §8 P1 has the row text, the anchors (`tools/methodology_dashboard.py:3510-3528`), the mirror-last rule and RED-first criteria. **Its PR is its own go-ahead.** **THE URGENCY CHANGED AND THE REASONING DID NOT:** the reported flag no longer fires, because `nprcgenekeepr`'s `SESSION_NOTES.md` fell to 19,719 B, well under the 56,750 B cap — but the canonical prose defect it exposed is untouched and fires again the moment that file re-crosses the cap. **(3) PART 2's SUB-DECISION IS STILL THE OPERATOR'S AND IS THE ONLY THING THE PLAN LEAVES OPEN:** the probe may **execute** each adopter's trimmer or **grep** it. **(4) NOTHING IS OWED UPSTREAM; SIX PRs (#83–#88) SIT OPEN WITH 0 REVIEWS** — a review comment on any outranks everything and is its own go-ahead. **(5) CHEAPEST CANDIDATES UNCHANGED:** BL-87 fork-side, BL-84 upstream-facing; **BL-66 P6 waits on #87's merge.** **(6) RECEIPTS ARE BACK TO 2, so the NEXT claim makes three and owes the trim** (`--cut 2 --force`, dry run first, then the fold, after the report). It archives **S227's** receipt dated **2026-09-27**, and `-2026-09-27.md`, `-2` and `-3` all exist, so **expect `-4`** — the dry run is the answer. **(7) RECORDED, NOT FIXED (FM #17):** **`bin/check-handoff` has now passed two differently-broken `HANDOFFS.md` trees in two sessions** — a receipt spliced into the front matter's code span, and a duplicated session number — because it validates the newest record's schema, not the file's record structure; **BL-73's family, still unfiled**. `mts-system`'s `SESSION_NOTES.md` has no `## ACTIVE TASK` heading. S226's three carried unchanged.
key_files: **The deliverable:** [`docs/archive/CHANGELOG-through-2026-09-22.md`](docs/archive/CHANGELOG-through-2026-09-22.md) (120,945 B, 85 records, frozen) and its `.verify.sh` beside it; [`CHANGELOG.md`](CHANGELOG.md) front matter now carries the 17th archive pointer block and the trimmer's own `[ad hoc] Ledger trim` entry. **The repair:** [`HANDOFFS.md`](HANDOFFS.md)`:53` (the one S227 receipt that should always have been there). **The owed trim:** `docs/archive/HANDOFFS-through-2026-09-27-3.md` and `docs/HANDOFFS_ARCHIVE_INDEX.md:92` (the 65th row). **The learning:** `docs/FORK_LEARNINGS.md:118` (row #101, last). **The decision this session did NOT implement:** `docs/planning/dashboard-read-cap-class-adopter-drift-plan.md`. **The adopter, read-only:** `~/Development/nprcgenekeepr/CLAUDE.md:256` — the local-customization checklist that ratifies `--budget-bytes 65536` and names `git show 63b3286f -- methodology_trim.py` as the patch to re-apply after each sync.
gotchas: **(1) A `git checkout --` THAT UNDOES A DRAFT RESTORES THE COMMITTED CLAIM STUB, AND PREPENDING AFTER IT DUPLICATES THE SESSION.** Phase 3D substitutes; it does not prepend. **After writing a close-out receipt, grep `^session: ` and confirm each number appears once** — `bin/check-handoff` will not tell you. **(2) I RAN AN ADOPTER'S TOOL WITH THE TOOL'S DEFAULT INSTEAD OF THE PROJECT'S RATIFIED INVOCATION, AND REPORTED THE WRONG BUDGET.** `nprcgenekeepr/CLAUDE.md:256` requires `--budget-bytes 65536` on **every** run, `--check` included; my bare `--check` read the 196,608 B v1.5.0 default. **Grep the adopter's `CLAUDE.md` for the invocation before quoting its tool.** **(3) A CROSS-REPO MEASUREMENT DECAYS WHILE YOU WRITE IT UP.** That project's `SESSION_NOTES.md` was **57,871 B** when I measured it and **19,719 B** forty minutes later — a live session (its S795) archived it mid-analysis with the very local patch under investigation, which incidentally **proved the patch works in production**. Timestamp cross-repo figures; re-read before concluding. **(4) THE TRIM'S NUMBERS MOVE BETWEEN DRY RUN AND WRITE** because the claim entry lands in between — 248,167 → 249,268 B here. Read the `[WROTE]` line, never the forecast, for what to record. **(5) READ THE SHARD'S PROOF FROM A CLONE OF ITS OWN COMMIT** — both were exit 0 that way (`d23c811`, `0038441`). **(6) CARRIED, RE-CONFIRMED:** `--file` not a positional path; `--force` needed to print a plan past `SRF_RED`; `check-learnings` needs `--file docs/FORK_LEARNINGS.md --first 15`; no fold for `CHANGELOG.md`; `FRONTMATTER_FIELD_ABSENT` and `CUT_STRADDLES_DAY` are stated-and-expected.
runtime_smoke: **TWO TRIMS AND A LEDGER REPAIR, SO THE VERIFICATION IS THAT NOTHING WAS LOST AND THAT THE FILES THE PROTOCOL READS STILL PROVE THEMSELVES — EXIT CODES READ OUTSIDE A PIPE.** **Both shard proofs read from a clone of their OWN trim commit:** `CHANGELOG-through-2026-09-22.md.verify.sh` at `d23c811` **exit 0** — L1, L2/front-matter and L3 all hold, *"138 before = 53 retained + 85 archived; added by the trim commit: 1"*, that one addition being the trimmer's own ledger entry; `HANDOFFS-through-2026-09-27-3.md.verify.sh` at `0038441` **exit 0** — *"3 before = 2 retained + 1 archived"*. **In a `--no-local` clone at `c72ad24`, after both trims and the fold:** `bash bin/tests.sh` **343 passed / 0 failed / 6 skipped**, exit 0 — the `tests-sh-passed >= 343` floor exactly, which matters because Test 34 mutates `HANDOFFS.md` and this session trimmed it; `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`, exit 0 — **hashes identical to S227's and to Phase 0's at `12cc571`**, right for doc-only edits. **At HEAD, by hand:** `check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations` **OK, 86 rows, contiguous 15..101, 0 over 1,500 B**; `bin/check-handoff` **OK**, 2 receipts, 0 over the 12,288 B record budget. **Sizes, all `wc -c`:** `CHANGELOG.md` 249,268 → **130,729 B**; the shard **120,945 B**; `HANDOFFS.md` 29,818 → 18,138 → **17,682 B** after the fold. **THE ADOPTER WAS READ ONLY AND A LIVE SESSION WAS RUNNING THERE** — `git status` showed its `SESSION_NOTES.md` `MM`, so nothing was touched and nothing could have been. **NOT EXERCISED:** this close-out commit and its tree (**BL-64**); BL-88's Part 1 and Part 2, **neither built**; the merged trees with #83–#88; `bin/status` against a history-less source.
changelog_ref: CHANGELOG.md "2026-09-27 · [ad hoc] S227 correction — the close-out left the Phase 1B stub in place beside its own receipt", "[ad hoc] S228 claim", the trimmer's own "[ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-09-22.md`", the `HANDOFFS.md` trim's own entry, "[ad hoc] S228 — `HANDOFFS.md`: the trim's pointer block folded into the shard index", "[ad hoc] S228 — Phase 3C: fork Learning #101, and D3 discharged by an explicit refusal", and this close-out
commit: 3815b83 (S227's duplicate stub repaired) + 1230dc0 (claim) + d23c811 (**the deliverable** — 85 records archived, 249,268 → 130,729 B) + 0038441 (HANDOFFS retention trim) + c72ad24 (fold) + da2ec5f (fork Learning #101, D3 by refusal) + this close-out; no branch touched, nothing pushed, nothing on KJ5HST/methodology
```

