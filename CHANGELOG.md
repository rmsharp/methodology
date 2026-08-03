# Changelog — Authoritative Action Ledger

The cumulative, append-only record of **actions taken in this repository** — across backlog
items, repository issues, and ad-hoc work. It is the authoritative answer to *"what was done
here, ever?"*, distinct from the release narrative in [`CLAUDE.md` §Versioning](CLAUDE.md#versioning).

This repository dogfoods its own methodology: every session records its actions here at
close-out (`starter-kit/SESSION_RUNNER.md` Phase 3F), and Phase 0 reconciles the ledger against
`git log` and backfills anything a crashed or out-of-band session missed. Taking an action — any
commit, or any non-commit action (release, tag, PR, upstream issue close, access grant, grooming
decision) — and not recording it is failure mode #27. The full close-out and reconcile rules, plus
the reusable seed, live in [`starter-kit/CHANGELOG.md`](starter-kit/CHANGELOG.md).

**Source tag — exactly one per entry.** This enumerates every logged action across the live file
and its archives, and proves all three sources landed:

```
grep -hE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[(issue #[0-9]+|BL-[0-9]+|ad hoc)\]' \
  CHANGELOG.md docs/archive/CHANGELOG-*.md | wc -l
```

It is anchored to the entry heading, and it reads the archives, for two separate reasons. The
unanchored single-file form published here before the v3.6 split returned **78** against 64 actions —
it also matched the three tag definitions just below and eleven in-prose mentions of a tag — and after
the split it would have stopped counting the archived entries at all.

- `[issue #<N>]` — a repository issue. Issues for this repo live in the **upstream** parent
  `KJ5HST/methodology` (this fork has Issues disabled), so entries cite an **absolute URL**, never
  a bare `#<N>`.
- `[BL-<N>]` — a `docs/planning/BACKLOG.md` item, removed from the backlog in the same commit.
- `[ad hoc]` — work with no backlog or issue origin: releases, tag/branch ops, PR opens, upstream
  issue closes, access grants, and decline/wontfix/grooming decisions.

**Boundary vs. `CLAUDE.md` §Versioning — so the two ledgers cannot diverge.** §Versioning owns
*released-version semantics* (one narrated entry per shipped version); `README.md` §What's New is
its public restatement. This ledger is the *per-action operational timeline*, including
non-release work (housekeeping, doc-only PRs, adopter coordination, backlog grooming) that
otherwise has no home but raw `git log`. Where the two overlap — a release — this ledger carries a
**one-line pointer** into §Versioning, never a re-narration (cite, don't restate). §Versioning still
owns that semantics and still answers at the `CLAUDE.md#versioning` anchor every entry below cites;
as of BL-9 L3 its **narrated per-version list** lives one hop further on, in
[`docs/RELEASE_HISTORY.md`](docs/RELEASE_HISTORY.md), so the always-loaded `CLAUDE.md` stays lean.
The boundary itself is unchanged — the pointer moved, not the ownership.

Reverse-chronological, newest on top; prepend-only; grouped into `## YYYY-MM` sections. Prepend
under the topmost `## YYYY-MM`, and when the month changes open a new one above it. Entries stay at
`###`: never demote them beneath the month headings, because `_DATED_ENTRY_RE`
(`starter-kit/methodology_dashboard.py`) and `CHANGELOG_ENTRY_RE` (`bin/model-report`) both key on
exactly that level.

**Everything older than 2026-08-02 is archived, across two shards.** This file holds that day forward;
the preceding spans live in
[`docs/archive/CHANGELOG-through-2026-08-01.md`](docs/archive/CHANGELOG-through-2026-08-01.md)
(2026-07-27 → 2026-08-01) and
[`docs/archive/CHANGELOG-through-v3.6.md`](docs/archive/CHANGELOG-through-v3.6.md)
(2026-06-25 → 2026-07-26) — same format, same `## YYYY-MM` grouping, same newest-on-top order, frozen
at write. **The sections are the calendar; the file boundary is not.** The v3.6 shard was cut at a
release frontier, a cut nothing can ever be written back into. The 2026-08-01 shard was cut at a
**day**, because no release had shipped since v3.6 and the next calendar seam was measured and bought
5 entries; that shard's own front matter labels the departure and says when to prefer a release
again. Archiving is safe by construction: the FM #27 pre-commit gate matches the literal staged path
`CHANGELOG.md`, Phase 0 reconcile is frontier-based (`git log -1 --format=%H -- CHANGELOG.md`), the
dashboard's `_find_action_ledger` resolves the root file only, and `_find_changelog` scans only
`(<root>, <root>/docs)` — so no shard in `docs/archive/` can shadow this file by sort order.

**`bin/model-report` is the one consumer that loses coverage, and it loses more than it looks.** Its
Source 1 matches only the seed's list form `- **Model:**` (`bin/model-report:51`). This file's bullets
are all written in a bare `**Model:**` form it cannot parse, so **every bullet Source 1 could actually
see moved into the 2026-08-01 shard at this split** — run with no arguments it now reports an empty
Source 1 against a ledger whose entries visibly carry the bullet. Reach a span with
`bin/model-report --changelog <shard>`. The parser blindness is **not a consequence of this split**:
the form drifted at `1298af7` (2026-08-02) and has held unbroken since — *every* live entry, this
file's own newest included. Raised as **BL-20**, deliberately not fixed here (FM #17). The count that
stood here ("nine entries since") was falsified by the very next entry written above it, which is the
plan's own **DELETE** sink applied on the spot: the reader can count the list, and the command below
does it. Count both dialects,
never one — a single literal is a sample, not a population:

```sh
grep -cE '^-?[[:space:]]*\*\*Model:\*\*' CHANGELOG.md docs/archive/CHANGELOG-*.md
```

**When to archive again — a rate, not a level.** Archive when the headroom to the 2,000-line agent
`Read` cap, divided by the observed growth per ledger *entry*, falls below **15 entries**; then cut
oldest-first until that ratio is back above **30**. Both are denominated in entries — the framework's
own unit — deliberately: commits-per-session is the most adopter-variable quantity in the system, so a
team committing 10× per session reads a 10× lower slope for identical growth, and the same file
crosses or clears the threshold depending only on which denominator you picked. Compute it; never
recall it:

```sh
split=$(git log --diff-filter=A -1 --format=%H -- 'docs/archive/CHANGELOG-*.md')
live=$(wc -l < CHANGELOG.md)
dl=$(( live - $(git show $split:CHANGELOG.md | wc -l) ))
de=$(( $(grep -c '^### ' CHANGELOG.md) - $(git show $split:CHANGELOG.md | grep -c '^### ') ))
if [ "$de" -gt 0 ] && [ "$dl" -gt 0 ]; then
  echo "$(( (2000 - live) * de / dl )) entries of headroom"
else
  echo "no slope yet — fewer than one entry written since the last split ($de entries, $dl lines)"
fi
```

It **abstains out loud** rather than printing a confident number it cannot support: immediately after
a split both deltas are zero, and against a superseded baseline they go negative. Either way you get
a sentence saying so, never a figure. That is the same discipline the numbers above are asking for.

A **level** was the previous rule, and it failed in the file next door: `HANDOFFS.md` states its
trigger as "approaches ~1,200 lines" and the archive actually fired at 997 — 203 lines early, with
nothing watching. A level is a hand-written derived value that decays silently; a rate re-derives
itself from the file every time it is read. This file crossed the cap once already, at 2,090 lines,
and was silently dropping its ten oldest entries when a `Read` truncated it.

---

## 2026-08

### 2026-08-03 · [ad hoc] Reconcile-on-read: S31's `commit:` field → `020ba3f` — fourth consecutive discharge

**Model:** Claude Opus 5 (1M context).
**Record repair, committed on its own** per `starter-kit/SESSION_RUNNER.md:39` and `:42`. Precedents:
`0a1a0d5`, `d9bedb0`, `9267500`, `7752114`, `728f39a`. Not S32's deliverable and no license for work
beyond it (FM #17). **Deliberately short** — four prior entries carry the mechanics; cite, don't
re-narrate.

- **What was reconciled.** S31's receipt closed out `commit: pending`, legitimately: it shipped inside
  the commit whose sha it names. That sha is **`020ba3f`**, derived by the method
  `bin/check-handoff`'s own failure note prescribes — walk `git log --all --full-history` over
  `HANDOFFS.md` (**85** commits, all refs) with the checker's `extract_blocks`/`parse_block`, take the
  first commit whose `S31` block reads `status: complete`. The claim stub `74479df` holds the same
  block at `status: pending` — distinct commits, S29's gotcha (3), now four receipts running.
- **RED observed, not inherited.** A synthetic `S32` stub prepended to a **scratch copy** made the
  checker emit *"receipt S31 (2026-08-02) names no commit sha in its `commit:` answer slot"*, exit 1.
  The working tree never went red (`starter-kit/SAFEGUARDS.md:34`).
- **Still a practice, not a procedure.** BL-14's DISTRIBUTED half — the seed promises a reconcile no
  checklist assigns — is untouched and blocked on the paused channel.
- **One front-matter number, falsified by this very entry, deleted rather than incremented.** The
  BL-20 paragraph above said the bare `**Model:**` form "has held unbroken for nine entries since" —
  a level, in a sentence that any new entry written above it invalidates. Prepending this entry made
  it wrong within the same commit, so it was **deleted, not bumped** (sink 1 of
  [`framework-context-cost-plan.md`](docs/planning/framework-context-cost-plan.md) §3.5): the list is
  in view and the command two lines below counts it. No other front-matter figure moved.

### 2026-08-02 · [ad hoc] The action ledger split at a day seam, and the archive trigger restated as a rate

**Model:** Claude Opus 5 (1M context).
**S31 of [`framework-context-cost-plan.md`](docs/planning/framework-context-cost-plan.md) §5** — its
only time-critical item. Fork-side, canonical-only: the root ledger is not in `bin/_manifest.py`'s
DISTRIBUTION, so no adopter file was touched and no channel was needed. Three operator decisions were
taken before any technical work.

- **The split.** 18 entries (2026-07-27 → 2026-08-01, 726 lines) moved to
  [`docs/archive/CHANGELOG-through-2026-08-01.md`](docs/archive/CHANGELOG-through-2026-08-01.md);
  9 kept live. **Proven lossless rather than asserted**: reversing the one mechanical edit and
  concatenating shard onto live reproduces the pre-split file **byte-for-byte**, md5
  `f5af5eb58b647d1bba5b4c5d9375a38c`, 101,608 B. The source-tag audit across live + archives reads
  **77** before and after. One mechanical edit only — 7 root-relative links across 5 distinct targets
  given a uniform `../../` prefix, uniform *because* that makes it invertible and therefore provable.
- **The trigger is now a rate, not a level.** Archive when headroom to the 2,000-line `Read` cap
  divided by observed growth *per ledger entry* falls below 15 entries; cut back above 30. Denominated
  in entries, the framework's own unit, because commits-per-session is the most adopter-variable
  quantity in the system. The runnable derivation sits beside it and takes its own baseline from
  `git log --diff-filter=A`, so no session hand-writes a split sha. **The level form failed next
  door:** `HANDOFFS.md` says "approaches ~1,200 lines" and its archive fired at 997.
- **The day seam is a labelled departure, not a new default.** BL-9 L2 settled the file axis as the
  release frontier. That reasoning stands; **the axis was unavailable, not rejected** — v3.6 is the
  previous shard's own boundary and no release has shipped since. The month seam was *measured before
  being chosen* and bought 5 entries (994 lines, re-firing inside 2–3 sessions), reproducing exactly
  what BL-9 L2 predicted of calendar cuts. The day seam lands at 30.5 entries of headroom and agreed
  to within one entry with the new trigger's own reset arithmetic, derived independently. Both shards
  now say to prefer a release frontier when one is available.
- **Two record repairs, each on its own commit** per `starter-kit/SESSION_RUNNER.md:39`/`:42`.
  `0a1a0d5` reconciled S30's `commit:` field to `326094d` (third consecutive discharge). `7f3b7d1`
  fixed **my own** error from the first of those: the entry was *inserted* beside its topical sibling
  instead of *prepended*. Every entry that day carries the same date, so position is the file's only
  ordering signal and adjacency-by-topic destroys it silently. Proven content-preserving by comparing
  the sorted line multiset before and after.
- **The v3.6 shard's front matter was corrected** — its only change since `3aee4e3` created it, and no
  dated entry was touched. It restated the archive rule, and **both halves were wrong one day later**
  (the level became a rate; the release axis was unavailable). A frozen file cannot keep a
  forward-looking rule true, so the restatement was replaced by a pointer. Cite, don't restate.
- **BL-20 raised, not fixed** (FM #17). Verifying a claim this session was about to publish about its
  own split turned up a live defect: `bin/model-report`'s Source 1 regex (`bin/model-report:51`)
  matches only the seed's `- **Model:**` list form, while this repo writes a bare `**Model:**`. The
  tool reports "no entries carry a **Model:** bullet" against a ledger full of them. Population at
  `74479df` (frozen to that tree so it cannot decay): 14 corpus-wide — 9 bare (live) + 5 list (this
  split's shard) + 0 (v3.6 shard). Drift derived, not guessed: last list-only commit `54426cb`, first
  bare `1298af7`, unbroken since. **This entry keeps the bare form deliberately**, so the population
  stays uniform for whoever normalizes it — which also means this entry made it 10 bare / 15 total the
  moment it was written, and the front matter above therefore states no count at all, only the command.
- **My first count of that population was wrong, and it is recorded because it is this plan's own
  thesis.** I wrote "9 live, 0 in shards" into two front matters from `grep -c '^\*\*Model:\*\*'` — one
  literal, one dialect — and only caught it because `bin/model-report` disagreed with my grep in *both
  directions* at once. A count is only as good as its net; state the population beside the number.
- **Verified:** `bin/tests.sh` **142 passed / 0 failed** (unchanged — a split adds no assertion);
  `bin/check-handoff` OK; `bin/check-links` OK 83/21; all relative links in all three ledger files
  resolve under a code-span-aware scan (0 broken); no entry demoted below `###`; dashboard 72/100.
  Zero DISTRIBUTION members in the diff.

### 2026-08-02 · [ad hoc] Reconcile-on-read: S30's `commit:` field → `326094d` — third consecutive discharge

**Model:** Claude Opus 5 (1M context).
**Record repair, committed on its own** per `starter-kit/SESSION_RUNNER.md:39` and `:42`. Precedents:
`d9bedb0`, `9267500`, `7752114`, `728f39a`. Not S31's deliverable and no license for work beyond it
(FM #17). **Deliberately short**: this session's own deliverable is that this file is 15.8 ledger
entries from the `Read` cap, and a reconcile entry is the cheapest place to stop restating what four
prior entries already say — cite, don't re-narrate.

- **What was reconciled.** S30's receipt closed out `commit: pending`, legitimately — it shipped
  inside the commit whose sha it names. That sha is **`326094d`**, derived by the method
  `bin/check-handoff`'s own failure note prescribes: walk `git log --all --full-history` over
  `HANDOFFS.md` (**82** commits, all refs) with the checker's `extract_blocks`/`parse_block`, take the
  first commit whose `S30` block reads `status: complete`. The claim stub `0485d4a` holds the same
  block at `status: pending` — distinct commits, S29's gotcha (3).
- **RED observed, not inherited.** A synthetic `S31` stub prepended to a **scratch copy** made the
  checker emit *"receipt S30 (2026-08-02) names no commit sha in its `commit:` answer slot"*, exit 1.
  The working tree never went red (`starter-kit/SAFEGUARDS.md:34`).
- **Three in a row is a practice with a widening gap behind it.** The DISTRIBUTED half of BL-14 is
  still untouched: the seed promises a reconcile no procedure assigns. Each clean discharge makes the
  fork look healthier while the adopter-facing hole stays exactly where it was — blocked on the
  paused channel, and a choice (schedule it into Phase 0, or delete the promise), not an edit.

### 2026-08-02 · [ad hoc] The framework's context cost — adopter heuristics and a remediation plan

**Model:** Claude Opus 5 (1M context).
**A PLANNING session (S30): the plan is the deliverable and nothing was implemented**
(`starter-kit/SESSION_RUNNER.md` §Planning Sessions). Operator-assigned, not a backlog item. Written
to [`docs/planning/framework-context-cost-plan.md`](docs/planning/framework-context-cost-plan.md),
which is fork-only — absent from `bin/_manifest.py`'s DISTRIBUTION, so no adopter file was touched
and no channel was needed.

- **The question it answers.** Whether a framework's accumulated learnings are actually resident in
  an agent's context or are read-and-discarded. **Nothing is ever discarded.** `CLAUDE.md` is
  resident every turn (8,519 B); everything else enters on Read and is carried until compaction
  replaces it with a *lossy summary*, degrading line numbers and which-of-two-similar-counts first.
  Prompt caching cuts the price of re-sending that prefix (~10%, measured at 91.7% of input in S14)
  but not its occupancy — **so the budget signal that would warn you is the one caching suppresses.**
- **The monitoring verdict — one of the three expenses is DECLINED as framed.** "Coordination
  residue from outward-facing upstream actions" is a *maintainer* cost; an adopter has no PRs, tags
  or releases, so a gauge for it would read zero forever and look like coverage. Its true adopter
  analogue is **record growth**, and there the finding is a missing *doctrine*, not a missing gauge:
  **zero of the 21 distributed `.md` files state any ledger size/archive/split policy**, while
  `starter-kit/BOOTSTRAP.md:195`/`:360` and `starter-kit/CLAUDE_TEMPLATE.md:82` ship exactly that
  policy for `CLAUDE.md`. Every adopter reproduces this repo's sawtooth from scratch. Expense 1 is
  MONITORED but reframed from bytes-shipped to bytes-Phase-0-obliges-opening; expense 3 is monitored
  only in its new-instance half — a resolution check and a numbered-set growth gauge are both
  declined, with reasons.
- **The decisive finding, and it forecloses "add a sentence" as a remedy.**
  `starter-kit/SESSION_RUNNER.md:280` **already** instructs every session to "grep nearby prose for
  set-size claims that may have drifted." That rule is distributed, sits in the 62,410 B file Phase 0
  reads in full every session — and six of six open backlog items still carried a wrong number. It is
  the closest thing this corpus can produce to a controlled comparison of MECHANIZED versus
  DOCUMENTED, and Learning #12 already names the failure: a review-time grep is "a human step that
  silently stops happening."
- **The sawtooth, measured.** `HANDOFFS.md` was archived from **224,368 B** to **52,927 B**
  (`7a71df0`, BL-9 L1) and stood at **164,611 B** one day later — SRF **0.651**, 65% of a whole
  session's deliverable given back. `CHANGELOG.md` split from **186,704 B** to **53,512 B**
  (`3aee4e3`) and is **92,950 B**, SRF **0.296**. **Every accumulation control the framework has is a
  LEVEL control; nothing anywhere is a rate control.** The stated archive trigger is itself a wrong
  derived value — `HANDOFFS.md` says "approaches ~1,200 lines" and the archive fired at **997**.
- **The denominator matters more than the rate.** Measured in the framework's own unit — ledger
  entries, not commits — `CHANGELOG.md` has **18.9 entries** of headroom to the 2,000-line agent
  `Read` cap, not 36 commits. It crossed that cap once before at **2,090 lines** and was *silently
  dropping its ten oldest entries*, found incidentally. This is the only one of the three expenses
  that produces silently wrong answers rather than merely expensive ones.
- **Three verified defects in the only executable adopters receive**, all byte-identical in the
  distributed twin: `tools/methodology_dashboard.py:699` runs `git log --reverse --format=%ai -1`,
  and git applies `-n1` *before* `--reverse`, so it returns the **newest** commit — measured
  `2026-08-02` against a true root of `2026-03-09`, making `project_age_days ≈ 0` and one risk
  permanently dead; `:2122` gates the large-file risk on `SOURCE_EXTS`, and `.md` is in `DOC_EXTS`,
  so the file that actually breached the `Read` cap could never trip it at any size; `:88` excludes
  `"methodology"`, so the instrument is blind to its own home.
- **Corrections to the record, measured so the next session inherits them right** (the items
  themselves are NOT edited — that is a separate deliverable, FM #17): the receipt corpus is **33**,
  not the backlog's nine live-voice "32"s. **BL-18**'s "30 anchors, 20 in `key_files`, 1 in
  `next_steps`" is **28** across 14 receipts (`key_files` 24, `active_task` 1, `gotchas` 1,
  `next_steps` 1, `changelog_ref` **0** — S29's repair held), and its published breakdown was a
  `CHANGELOG.md`-only slice that missed six bare `HANDOFFS.md:<N>` anchors and two whole keys.
  **BL-18's stated blocker is false**: archive-S4's referent is recoverable with zero invention
  (`git show 6591faa:CHANGELOG.md` line 35 → the `Opened upstream issue #55` heading, surviving in
  the archive shard), and a prefixed replacement satisfies `KEY_FILES_RE` while producing no finding.
  **BL-12**'s "four sites" is **five**. **BL-16**'s docstring is at `bin/check-handoff:487`, never at
  the cited `:301-303` at any tree that ever existed. The Learnings table is **13** rows / 12,937 B.
- **A fourth expense the brief did not name: gate erosion.** `.githooks/pre-commit` carves out five
  *git* states and not one *methodology* state, so the Phase 1B claim commit the framework mandates —
  which by construction has no action to log yet — is a gate violation. **25 of 25 claim commits
  stage `HANDOFFS.md` alone and every one bypassed.** Artifact damage nil (reconcile-on-read
  backfills); the damage is that `--no-verify` is trained reflex, and every future check on that hook
  inherits the bypass silently.
- **A third failure class, named here for the first time: *denominator-wrong*** — a number freshly
  and honestly computed over the wrong population, invisible to any derived-value detector because
  the digit is present, recent, and genuinely derived. **This session produced one:** it reported the
  bypass population as "20 of 20" because it passed `-20` to `git log` and read a capped sample as a
  population. Recorded rather than quietly fixed, because it is the strongest available evidence that
  discipline-by-attention fails even for someone actively looking for it.
- **Method.** Two workflows, 22 agents, ~2.29M subagent tokens: a 13-agent re-measurement of every
  open backlog item (measure → adversarially refute) at Phase 0, then a 9-agent design panel (four
  forced-different stances → three judging lenses → synthesis → completeness critic). Every
  load-bearing number in the plan was **re-derived by the session lead** rather than relayed; doing so
  corrected the panel twice (it restated a wrong denominator — "22 distributed `.md` files" for 21
  `.md` + 1 `.py` — inside the document arguing never to restate) and corrected the session lead
  twice (the Learnings table row count, and the bypass population above).
- **The plan dogfoods its own rule.** Its thesis is that derived values must not be stored as
  hand-written prose, so every derived number in it carries the command that computes it — the
  **CITE** sink, added as a fourth sink precisely because a measurement report can neither delete,
  generate, nor freeze its own findings. All embedded commands were executed and reproduce their
  stated values.

### 2026-08-02 · [ad hoc] Reconcile-on-read: S29's `commit:` field → `4669fb6` — and the first time the tripwire was *observed* firing

**Model:** Claude Opus 5 (1M context).
**Record repair, committed on its own** per `starter-kit/SESSION_RUNNER.md:39` and `:42`. Precedents:
`9267500` (the same duty, one session earlier), `7752114`, `728f39a`. It is not S30's deliverable and
does not license work beyond it (FM #17).

- **What was reconciled.** S29's receipt (`HANDOFFS.md`, session `S29`, 2026-08-02) closed out with
  `commit: pending`, legitimately — it shipped inside the very commit whose sha it names. That sha is
  **`4669fb6`**, derived and not assumed: the receipt's first appearance with `status: complete`,
  found by walking `git log --all --full-history` over `HANDOFFS.md` (79 commits, all refs) with the
  checker's own `extract_blocks`/`parse_block`, then re-verified as an ancestor of `HEAD`. The stub's
  own first appearance is `7df3c4b`, and the two are distinct — which is exactly the trap S29's own
  gotcha (3) recorded. Leading token replaced; existing prose kept, `status` untouched.
- **The claim S29 could only make forward, this session tested.** S29 wrote that `bash bin/tests.sh`
  "goes RED (Test 25 L1) the moment that session prepends its own receipt", and recorded honestly that
  the mechanism had been *observable* and never *observed* — both prior discharges happened before any
  successor receipt existed. Rather than inherit that sentence a third time, a synthetic `S30`
  Phase 1B stub was prepended to a **scratch copy** of the ledger and `bin/check-handoff` run against
  it. It named this exact field: *"receipt S29 (2026-08-02) names no commit sha in its `commit:`
  answer slot"*, exit 1. **First observed firing on a real receipt** — and the working tree never went
  red, so nothing was started from a red suite (`starter-kit/SAFEGUARDS.md:34`). A prediction verified
  against a copy costs one file write; repeating it costs the record its meaning
  ([Learning #13](starter-kit/SESSION_RUNNER.md)).
- **Two consecutive discharges make a practice, not a procedure.** BL-14's measured base rate was six
  firings, only four deliberate, all inside one 8-hour window on 2026-07-25, by hand. This is the
  second in a row found at Phase 0 by the mechanism BL-14 shipped. The DISTRIBUTED half is untouched:
  the seed still promises a reconcile that no procedure assigns, and that choice — schedule it into
  `starter-kit/SESSION_RUNNER.md` Phase 0, or delete the promise — remains blocked on the paused
  channel.

### 2026-08-02 · [BL-15] The `changelog_ref` locator-form rule — BL-15 was right, and settling it found a different defect

**Model:** Claude Opus 5 (1M context) — implementation, the 11-agent refute/design/judge workflow,
and this entry.
**Fork-local and canonical-only.** `bin/check-handoff` and `bin/tests.sh` are both absent from
`bin/_manifest.py`'s 22-entry DISTRIBUTION; zero DISTRIBUTION members appear in the diff, verified
by importing the manifest. **No upstream action taken and none authorized** — `gh` read-only,
[issue #65](https://github.com/KJ5HST/methodology/issues/65) untouched.

- **BL-15 was raised correctly and this session's own claim stub was wrong about it.** The stub
  asserted that BL-15's *"identical escape in 13 of 32 receipts"* reproduced under no predicate. It
  reproduces exactly: **13 values defer deictically — 12 × `this commit` plus archive-S1's
  `this branch`.** The stub grepped one literal phrasing, reached 12, and stopped one variant short,
  which is the sampling error this repo has already recorded twice. `bin/check-handoff:69-70` names
  that dialect in writing; the key was documented and was not used. **Three adversarial verifiers
  refuted two of the session's three central claims, and every correction was re-derived here
  first-hand rather than relayed.**
- **It is closed anyway, and for a better reason than "wrong".** All 13 name their entry by a quoted
  `### ` title *before* the deferral, and all 13 now carry a real sha as their own `commit:` first
  token because of `7752114`/`6d47624`. Each deferral is a one-hop back-reference to a field the
  checker already guarantees. **BL-14 discharged BL-15 as a side effect** — one field to the left,
  the same week.
- **What settling it found: 9 positional line anchors, and the arithmetic is the argument.**
  **8 of 9 were correct the day they were written; 0 of 9 resolve to their stated referent now.**
  Four land in `CHANGELOG.md`'s front matter above every entry; four land inside an entry written
  the same day this was measured. **The cause is not "the ledger is prepend-only"** — under strict
  prepending an anchor at `:35` lands on the newest heading forever. The front matter is edited in
  place: the first `### ` moved **35 → 39 → 68**. Published entries are also rewritten mid-file, and
  the v3.6 split moved 50 entries out of the file.
- **The rule is a PROHIBITION, and that choice is the design.** `changelog_ref` may not carry a
  root-relative positional address into a live ledger. Its truth value depends only on the receipt's
  own bytes, so **no later prepend, retitle, front-matter edit or archive split can turn a passing
  receipt red.** The rejected alternative — assert every reference *resolves* to a real `### `
  heading — goes red whenever someone legitimately retitles an entry, and **this repo retitles
  entries precisely to correct false claims** (`de46858`). A guard that punishes correcting a false
  claim gets narrowed, not obeyed (FM #17). Three judges scored four candidate designs on separate
  lenses; the prohibition won 7/9/9 against 2–6 for the resolution rules.
- **No `blocks[0]` exemption, unlike the answer-slot rule — and that asymmetry is load-bearing.**
  BL-14's exemption exists to solve a chicken-egg; a prohibition has none, being satisfiable the
  instant the receipt is written. The corpus agrees: S28's second anchor was wrong the day it was
  written, so write-time values are not self-validating.
- **Prefix-aware, because three populations look alike and only one is the defect.**
  `starter-kit/CHANGELOG.md:92` cites a distributed template and
  `docs/archive/CHANGELOG-through-v3.6.md:46` cites a shard frozen at write; both stay legal, both
  are pinned by controls. Reusing the existing `KEY_FILES_RE` here would have been unsound — it
  matches all three, verified directly.
- **RED-FIRST AGAINST THE REAL CORPUS, and the archive measured rather than assumed.** Run against
  the unrepaired ledger the new pass returned **exactly 9** findings — the same 9 derived
  independently by walking git history — and **0** against the archive shard. **8 mutants, 8 killed,
  zero survivors**, six of them by NARROWING rather than deletion: drop prefix-awareness, copy the
  answer-slot exemption, narrow to a leading-token match, make `:<N>` optional, report per receipt
  instead of per anchor, and rename the finding prefix so `nslot()` would silently absorb it.
- **One line was deleted for being untestable.** An empty-value skip could not be killed by any
  mutant — an empty string contains no anchor, so the pass was already silent on it. A guard no
  mutant can falsify is a comment that looks like a guard; it is now a comment that says so.
- **Suite 127 → 142.** It also exposed and fixed a real coupling defect in the *previous* session's
  work: Test 25's live assertions keyed on the checker's **exit code**, which is a union over all
  three passes, so adding this one turned them red against a ledger whose `commit:` fields were all
  correct — reporting an answer-slot failure for a defect in a different field. Both now count their
  own rows.
- **Raised, deliberately not bundled (FM #17):** **BL-17** — the seed offers no locator a fork-local
  session can write (`PR #N`: often none; a short-sha: unknowable at write time), which is *why*
  eight authors invented a line number; plus the stale-title class the prohibition cannot see.
  **BL-18** — the same anchors in `key_files`, 20 of them, where `KEY_FILES_RE` *requires* a
  `path:line` token, and where one archived receipt cannot be repaired without fabricating a
  citation.

### 2026-08-02 · [ad hoc] Record repair: nine `changelog_ref` line anchors, and one quoted title that had been stale since the day it was written

**Model:** Claude Opus 5 (1M context).
**Record repair, committed on its own** per `starter-kit/SESSION_RUNNER.md:39`/`:42`; precedent
`7752114`, the nine-`commit:`-field repair the same week. It is not S29's deliverable and
licenses nothing further (FM #17). Fork-local, canonical-only: zero `bin/_manifest.py`
DISTRIBUTION members in the diff.

- **The nine anchors.** Every `changelog_ref` carrying a root-relative `CHANGELOG.md:<N>`:
  S28 (`:70`, `:118`), S27 (`:68`), S26 (`:68`), S25 (`:68`), S24 (`:39`), S22 (`:35`),
  S5-2026-08-01 (`:35`), S21 (`:35`) — 9 tokens across 8 receipts, all in the live
  `HANDOFFS.md`; the archive shard was **measured** clean, not assumed. Seven were deletions
  only: each already carried a quoted `### ` heading beside the number, so removing it lost
  nothing.
- **Why they had to go, in one measurement.** **8 of the 9 were correct the day they were
  written. 0 of 9 resolved to their stated referent afterwards.** Four now land in
  `CHANGELOG.md`'s front matter, above every entry; four land inside an entry written *today*.
  The cause is not "the ledger is prepend-only" — under strict prepending an anchor at `:35`
  lands on the newest heading forever. The **front matter itself** is edited in place: this
  file's first `### ` moved **35 → 39 → 68** across two such edits, and the v3.6 split moved 50
  entries out of the file entirely.
- **Two needed more than deletion, and both are disclosed rather than bundled quietly.**
  S28's `:118` is the corpus's **only** anchor-only referent — no title, no sha beside it — and
  it never worked: at `6d47624` line 118 sat inside the BL-14 entry while the repair entry it
  names began at 122. It now names that entry by heading, plus `7752114`. And **S5's `:35` was
  correct at birth**, pointing at PR #63's entry — PR #63 *is* the Learning #13 PR (`f9561a4`),
  confirmed against `d6dd6c9`, the tree where that value first appeared. Its referent is now
  named by title.
- **One repair the shipped rule does not cover, called out for that reason.** S22's quoted
  title had been stale since **23 minutes** after it was written: `de46858` retitled the entry
  from *"fixed upstream (PR #64)"* to *"fixed on a fork branch"* — correcting a false claim —
  and rewrote four other fields of that same receipt while leaving `changelog_ref` alone. It is
  re-quoted here as a judgement call **outside** the invariant; a prohibition on line numbers
  cannot see a stale title, and pretending otherwise would be the more comfortable sentence.
  The general case is BL-17.
- **Derivation, not assumption.** Each anchor's write-time correctness was judged at the tree
  where that value **first appeared**, found by walking `git log --all --full-history` over both
  ledger files with the checker's own `extract_blocks`/`parse_block`. That matters: for 2 of the
  8 receipts the `commit:` field names the **wrong** tree — S24's value first appears in
  `62f191e`, and S5's in `d6dd6c9` while its `commit:` leads with `c3157e8`, that session's
  Phase 1B *claim stub*.

### 2026-08-02 · [ad hoc] Reconcile-on-read: S28's `commit:` field → `6d47624` — the first time the duty was discharged as a duty

**Model:** Claude Opus 5 (1M context).
**Record repair, committed on its own** per `starter-kit/SESSION_RUNNER.md:39` and `:42`. Precedents:
`7752114` (the nine-receipt repair the day before), `728f39a`. It is not S29's deliverable and does
not license work beyond it (FM #17).

- **What was reconciled.** S28's receipt (`HANDOFFS.md:32`, 2026-08-02) closed out with
  `commit: pending`, legitimately — it shipped inside the very commit whose sha it names. That sha
  is **`6d47624`**, derived and not assumed: the receipt's first appearance with `status: complete`,
  found by walking `git log --all --full-history` over `HANDOFFS.md` with the checker's own
  `extract_blocks`/`parse_block`, then re-verified as an ancestor of `HEAD`. Leading token replaced;
  every word of existing prose kept, `status` untouched — the shape `7752114` established.
- **This is the first discharge that was owed rather than remembered.** The base rate BL-14 measured
  is six firings, only four deliberate, all inside one 8-hour window on 2026-07-25 — one operator, by
  hand. This one was found at Phase 0 by the mechanism BL-14 shipped, in the session immediately
  after it shipped.
- **Discharged BEFORE the Phase 1B claim, deliberately.** Test 25 L1 exempts the newest receipt
  positionally, so it was green while S28 was still newest and would have gone RED the instant S29
  prepended its own. Repairing first means S29 never started from a red suite
  (`starter-kit/SAFEGUARDS.md:34`) — and it is the honest record: the mechanism was *observable*
  here, not *observed*. The distinction matters, because a session that claims first and repairs
  second is the one that actually proves the tripwire fires.
- **BL-14's open half is untouched by this.** The DISTRIBUTED spec still promises a reconcile that no
  procedure assigns; one hand-discharge does not make it a procedure. That choice — schedule it into
  `starter-kit/SESSION_RUNNER.md` Phase 0, or delete the promise from the seed — remains blocked on
  the paused channel.

### 2026-08-02 · [BL-14] The `commit:` answer-slot rule — a distributed promise that had no owner and no detector

**Model:** Claude Opus 5 (1M context) — implementation, the design panel, and this entry.
**Fork-local and canonical-only.** `bin/check-handoff` and `bin/tests.sh` are both absent from
`bin/_manifest.py`'s 22-entry DISTRIBUTION; zero DISTRIBUTION members appear in the diff. **No
upstream action taken and none authorized** — `gh` was read-only, and upstream
[issue #65](https://github.com/KJ5HST/methodology/issues/65) stays open and unanswered.

- **The defect S27 nominated and declined to bundle.** `commit:` may legitimately read `pending`
  when written — the receipt ships inside the very commit whose sha it would name. The distributed
  spec then promises a collector (`starter-kit/HANDOFFS.md:64`, `:78-79`; ratified at
  `docs/planning/close-out-receipt-durable-artifact-plan.md:87`). **No procedure ever assigned it:**
  `starter-kit/SESSION_RUNNER.md` Phase 0 step 6 covers undocumented commits, a `CHANGELOG: pending`
  marker, and a missing-or-`status: pending` receipt — never a *complete* receipt whose `commit:` is
  still `pending`. And nothing detected it: the checker read only `blocks[0]`, and `pending` is not
  a `BARE_PLACEHOLDER`. **This is [Learning #9](starter-kit/SESSION_RUNNER.md)'s own remedy —
  gate-on-write AND reconcile-on-read — unapplied to the one sentinel-bearing key that needed both.**
- **Measured, and it corrected the record three times.** 9 of 32 receipts named no sha in the answer
  slot, not the 7 the literal word `pending` would find — S26 and S25 read `this commit — …`, and
  **S25 contained no sha anywhere**. The corpus is **32, not 31**: the claim stub measured the corpus
  pre-claim and the classification post-claim, mixing two trees in one paragraph. And the
  successor-reconcile has fired **6 times, only 4 deliberately**, all in one 8-hour window on
  2026-07-25 — `7817989` is S3 completing its **own** receipt 2m26s later, not a successor. The
  practice was never a procedure; it was one operator, by hand, for one afternoon.
- **The rule, and why it cannot re-create the chicken-egg.** The answer slot is the value's **first
  token**, and on every receipt *except the newest* it must be a sha. The newest is exempt
  **positionally, without its value ever being inspected** — so no close-out receipt can be failed
  for the deferral the plan explicitly permits. Test 25 N3 is that assertion; `bin/tests.sh:366`'s
  long-standing "`commit: pending` is accepted" now holds at ledger scope, not just single-block.
  Leading-token on purpose: it tolerates trailing prose and catches the `this commit` dialect.
- **RED-FIRST WAS RUN AGAINST THE REAL CORPUS, and it earned its keep.** Executed against the
  pre-repair ledger at `fd5d2d8`, the new pass returned **exactly 9** — matching the 9 derived
  independently by walking git history. That run also exposed a hole no fixture would have:
  **"newest" is a property of the LEDGER, not of a file.** In a sharded ledger the archive's
  `blocks[0]` is merely the newest *in that shard*, so S18 was silently exempt. Hence `--archived`,
  and Test 25 N5/N5b.
- **8 mutants, 8 killed — and two of them bought real tests rather than an annotation.** `M3`
  (`fullmatch`→`search`) **survived the first round**, because N7's first token is plain `pending`,
  which contains no sha, so both predicates agree on it; **N9** is the fixture that separates them.
  `M8` (drop the stub skip) drove **N10**. Also killed by narrowing, not only by deletion: `M1`
  (`blocks[1:]`→`blocks[2:]`), `M7` (narrow to the literal `pending`), `M4`/`M5` (both directions of
  the exemption), `M6` (absence-as-pass), `M2`.
- **Suite 112 → 127**, including a **live-corpus assertion** (L1/L1b) that runs the checker against
  the real ledger and archive. Every other `check-handoff` assertion in the suite uses a `mktemp`
  fixture, so nothing observed the real file; precedent is Test 10, which runs `check-links` bare
  against the real tree.
- **What did NOT ship, and it is the half that matters.** The spec still promises a reconcile no
  procedure assigns. Closing that means either **scheduling** the duty into `SESSION_RUNNER.md`
  Phase 0 or **deleting** the promise from the seed — a DISTRIBUTED change, blocked on the paused
  channel, and the choice between the two *is* the deliverable. The shipped detector is agnostic
  between them, which is why it could ship first. Recorded in BL-14 with the 7 affected distributed
  sites. **BL-15** (`changelog_ref`, same escape, 13 of 32) and **BL-16** (the checker's own docstring
  claims this repo has no root ledger) raised, not bundled (FM #17).

### 2026-08-02 · [ad hoc] Reconcile-on-read repair: nine `commit:` fields that named no sha

**Model:** Claude Opus 5 (1M context).
**Record repair, committed on its own** per `starter-kit/SESSION_RUNNER.md:39` ("committed on its
own, separate from this session's later deliverable") and `:42` ("does not become this session's
deliverable"). Precedent: `728f39a`. The analysis this repair came out of ships separately as
**BL-14**.

- **The nine, and what each now names.** Seven carried the literal `pending`: S27 → `1298af7`,
  S22 → `6f994ae`, S21 → `36e9195`, S20 → `596ff18`, S19 → `3737acd`, S18 → `8e6f292`
  (`docs/archive/HANDOFFS-archive.md`), S6 → `21fb521` (same archive). Two more named no sha in the
  answer slot at all: S26 → `54426cb` and S25 → `3aee4e3`, both reading `this commit — …`.
  **S25 contained no sha anywhere in the field** — the most unresolvable value in the corpus, and
  the one that keying on the literal word `pending` would have missed.
- **Every target derived, not assumed.** Each is the commit in which that receipt's block first
  appeared with `status: complete`, computed by walking `git log --all --full-history` over both
  ledger files with the checker's own `extract_blocks`/`parse_block` — never grep, per the
  fence-nesting rule at `bin/check-handoff:83`. All nine re-verified as ancestors of `HEAD`.
- **S6 is dual-homed and is the one case that is not a one-token edit.** It was authored at
  `21fb521` as `session: S2` on `feat/capability-tiered-review`, then renumbered S2 → S6 and given
  its fork-side close-out narrative in the merge `ab5b2d6`. `21fb521` is an ancestor of **both**
  `upstream/main` and this fork's `main`; **`ab5b2d6` is fork-only.** `upstream/main` still carries
  the identical receipt as `session: S2, commit: pending`. Naming `ab5b2d6` alone would have written
  a value unresolvable in the canonical copy of the same receipt — the unreachable-reference trap
  [Learning #13](starter-kit/SESSION_RUNNER.md) was added to prevent. That copy is upstream's to
  fix, not the fork's, and no upstream action was taken.
- **Shape of the edit: replace the leading token, keep every word of existing prose.** `status` is
  untouched on all nine — the historical reconciles (`e5638af`, `4e2901f`, `bc2481d`) all left it
  `complete`, and `reconciled` is reserved for a receipt a later session *reconstructed*, which
  none of these are.
- **Verified after.** 31 of 32 receipts now lead their `commit:` with a sha; the sole exception is
  this session's own open S28 Phase 1B stub, which carries no `commit:` key at all and is exempt by
  construction.
- **The archive was edited, and that rewrites no history** — `docs/archive/HANDOFFS-archive.md` is
  frozen *content*, not a frozen file, and two of the nine live there.

### 2026-08-02 · [ad hoc] `bin/check-handoff` learned the Phase 1B stub schema — the flag advertised a capability the tool never had

**Model:** Claude Opus 5 (1M context) — implementation, both workflows, and this entry.
**Fork-local, canonical-only; no upstream action taken and none is authorized.** Session claimed
`2026-08-01` (`8bd750c`, 23:42 CDT) and closed out after midnight; the receipt keeps `date:
2026-08-01` because session+date is the ledger's identity key and must not shift between Phase 1B
and Phase 3D, while this entry is dated when the work actually shipped.

- **The defect.** `bin/check-handoff --allow-pending` promised, in its docstring and its `--help`,
  to accept "a just-written Phase 1B stub." It relaxed exactly one assertion — the `status` finding
  — while every other assertion ran at full strength against a document both distributed specs
  describe as deliberately partial (`starter-kit/SESSION_RUNNER.md:91`, "the fields you can fill
  now"; `starter-kit/HANDOFFS.md:26`, "filling what you can").
- **Measured over git history, not the working tree: 21 distinct Phase 1B stubs, 0 passing.**
  Enumerated with the checker's own parser across 63 ledger-touching commits on `--all` refs, keyed
  by session+date because two sequences share this file and both have an S7 and an S8. **THREE
  dialects, and the checker rejected all three:** FLOOR-4 (4 stubs — `da46b19` S8, `65b1e8e` S15,
  `71ae4a1` S16, `9e93588` S3 — carrying exactly the `(session, date, active_task)` triple the spec
  names, 9 findings each); FORK-11 (14 — S9–S14, S18–S20, S22–S26 — both score keys omitted, 2
  findings each); and **SENTINEL-13 (3 — `c3157e8` S5, `a4e2b30` S7, `9c9c39c` S8, all authored by
  the framework's own maintainer — writing `self_score: pending`, 2 findings each).** That third
  dialect decided the design: the author of the checker, working in its home repo, independently
  reached for the value his own tool rejects, which is what rules out "the convention is wrong, just
  fill the scores in." S26's entry below says "17 distinct sessions"; that figure counts the fork's
  own *prior* sessions and is correct on its own terms — 21 is the whole population, both sequences,
  measured at `8bd750c`.
- **The root cause was a fixture, not a missing test.** `bin/tests.sh` has exercised
  `--allow-pending` since `1646773` and has been green the whole time, because its fixture is
  `good_handoff | sed 's/^status:.*/status: pending/'` — a fully-populated close-out receipt with one
  word changed, which is not a stub. **The guard was proved; the fixture under it never was.** That
  is why 21 real stubs failed unnoticed for a month, and it is the same lesson this repo already
  carries in its own receipts.
- **Known since 2026-07-25, recorded four times, fixed now.** `9ebedda` (S12) first wrote *"`bin/check-handoff`
  STILL cannot validate a 1B stub even with `--allow-pending` … do not 'fix' it by inventing
  scores"*; S13, S17/S19 and S26 each recorded it again under FM #17. The standing instruction not to
  invent scores is honoured — no session is asked to fabricate a self-score.
- **The design, ratified by the operator before implementation.** A three-candidate panel scored on
  two lenses picked **status-dispatched schema selection** (16.5/20, zero fatal flaws): a block is a
  stub **iff its own `status` is `pending`** — never because of the flag. Stubs require four keys
  (`session`, `date`, `status`, `active_task`); the other nine are optional-if-absent but **validated
  at full strength when present**, and a present-but-blank one is its own finding so blanking never
  becomes an escape. `self_score`/`predecessor_score` may carry `pending` inside a stub (extending
  the sentinel `starter-kit/HANDOFFS.md:77-79` already blesses for `commit`/`what_was_done`); the
  three other floor keys may not, since they are knowable at claim time. **The flag's job is
  unchanged** — it still gates exactly one finding, so an unflagged stub still exits 1 and no
  relaxation can produce a false green. **Labelled as ADDED POLICY in the code**, because no ratified
  text enumerates a stub's keys.
- **Why status-dispatch and not the one-line version.** The obvious patch —
  `required = STUB if allow_pending else REQUIRED_KEYS` — is a hole: a `status: complete` receipt
  missing `gotchas`, checked with the flag, returns clean. That receipt is now Test 24's N1.
- **Verified.** `bin/tests.sh` **92 → 112**, new Test 24 written and run **RED first** (its three
  unmutated stub fixtures failed with exactly 9 / 2 / 2 findings, matching the three dialects).
  **11 mutants, 10 killed** — including the naive flag-dispatch, dropping either new guard, letting
  the sentinel escape stub scope, and making the stub branch skip the sha-shape check or the
  placeholder lint. The one survivor is annotated in-code as uncoverable by construction rather than
  claimed as coverage. **All 21 historical stubs now pass (22 with this session's own).** An
  exhaustive **312-case** old-vs-new differential (4 statuses × 13 keys × 3 mutations × 2 flag
  states) shows **zero** behavioural change on the close-out path — nothing that fails today passes
  after. `bin/check-links` OK 83/21 unchanged; **zero `bin/_manifest.py` DISTRIBUTION members
  touched**, verified by importing the manifest.
- **A four-lens adversarial review before commit produced 14 findings; 3 survived refutation and all
  3 were fixed.** The sharpest was this session's own thesis recurring one level down: `N2` and `N7`
  each made a *plural* claim ("blank optional key", "floor keys") while sampling exactly **one** key,
  so narrowing either loop to that key passed the whole suite. Two `for` loops and four assertions
  closed it, each then mutation-proved.
- **Commits:** `8bd750c` (claim) · this commit (implementation + close-out). **Session:** S27 ·
  **Not done, deliberately:** no Learnings row (that table lives in a DISTRIBUTED file and the
  upstream channel is paused); no distributed-seed documentation of the stub schema (operator
  decision — the residual is recorded in the receipt); no version event (canonical-only, adopters
  receive nothing).
