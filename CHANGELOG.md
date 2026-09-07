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

- `[issue #<N>]` — a repository issue. Issues live in `KJ5HST/methodology`; the fork
  `rmsharp/methodology` has Issues disabled, so entries — authored from either side — cite an
  **absolute URL**, never a bare `#<N>`, and resolve identically from both.
- `[BL-<N>]` — a backlog item, removed from the backlog in the same commit. That backlog is
  [`docs/planning/BACKLOG.md`](https://github.com/rmsharp/methodology/blob/main/docs/planning/BACKLOG.md)
  on fork `main` only — **this repo has no `docs/planning/BACKLOG.md`** — so a `[BL-<N>]` entry here
  records work whose origin lives in the fork.
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

**Everything below the most recent cut is archived — and that boundary is POSITIONAL, not a
calendar seam.** `2026-08-30` carries records on *both* sides of it, so a shard's dated filename is a
**span label, not a day boundary**; `methodology_trim.py` says so itself (`CUT_STRADDLES_DAY`,
design §2.3). Every shard is listed in a pointer block below, and **no count is written here** —
the one that was (*"across two shards"*, plus *"this file holds that day forward"*) went stale
eight trims and 24 days ago and was still being read as current at S132. The two earliest spans are
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

**`bin/model-report` used to be the one consumer that lost coverage here. Since S133 (2026-08-31)
it does not.** Its Sources 1 and 2 now read the live ledger **plus every `docs/archive/` shard** by
default, so a split no longer shrinks what it sees. `bin/model-report --changelog <shard>` still
narrows to one file — an **explicit path means exactly that file** and discovers nothing.

**No population figure is written here, deliberately.** A first draft of this paragraph published
*"247 entries across 11 files (live 9 + archived 238)"* in the present tense. It was **already
false when committed**: 247/live-9 was the tree *before* the fix, and the fix commit and this one
each add an entry carrying a `**Model:**` bullet, so the tool reported **249/live-11** at the
moment the sentence was written. An always-read file, a number that rots on the next commit —
the exact defect the rest of this paragraph is about, reintroduced by the session fixing it. **Run
the tool, or the command below.**

**Two claims that stood in this paragraph were stale, and both are recorded rather than quietly
deleted.** It said Source 1 *"matches only the seed's list form `- **Model:**`"* and *"cannot parse"*
this file's bare form, and that a bare run *"reports an empty Source 1"*. Both were true when written
(`020ba3f0`, 2026-08-02) and **false from 2026-08-11**, when `b434183` fixed **BL-20** by widening
`CHANGELOG_MODEL_RE` to accept either dialect. It stood false for **20 days**, during which
**61 receipts** were written (`cat HANDOFFS.md docs/archive/HANDOFFS-*.md | grep -cE '^date: 2026-08-(1[1-9]|2[0-9]|3[01])'`).
The 2026-08-31 entry below says *"roughly ten sessions"* — a guess, stated as a fact, wrong by
6x, in the very entry that criticises an unchecked sentence. It stands there (this ledger is
append-only) and is corrected here and in the entry that follows it. Measured, not recalled. Its cited `bin/model-report:51` had drifted too. **BL-20's residual option
(3) remains open**; only the parser defect closed. The form itself did drift at `1298af7`
(2026-08-02) and has held unbroken since. Count both dialects, never one — a single literal is a
sample, not a population, and the command below is the independent check on the tool's own number
(it counts *lines*, where the tool counts *entries carrying* a bullet; `bin/tests.sh` Test 40 votes
the two against each other rather than merely computing them):

```sh
grep -cE '^-?[[:space:]]*\*\*Model:\*\*' CHANGELOG.md docs/archive/CHANGELOG-*.md
```

**When to archive again — a rate, not a level.** Archive when the headroom to the 2,000-line
`READ_CAP_LINES` proxy — the agent `Read` cap is denominated in **tokens**, and 2,000 lines is a
stand-in for it pending Phase B of
[`read-cap-premise-correction-plan.md`](docs/planning/read-cap-premise-correction-plan.md) —
divided by the observed growth per ledger *entry*, falls below **15 entries**; then cut
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
and its ten oldest entries were not reaching a reader who read it whole. **That was recorded here
as *silent* dropping, and that word was wrong** — truncation is announced, with a `PARTIAL view`
banner naming the true length; what was silent was that **nothing in the repo was checking**, so
the overrun was found by accident. Re-measured since, the file was 186,704 B — roughly 2.8–3.1×
the token cap — so it had been truncating well before it reached 2,090 lines: the incident dates
when the problem was *noticed*, not when it began.

**Reconcile-on-read entries below — the compact form, and the method stated once.** Each
`[ad hoc] Reconcile-on-read` entry records one Phase 0 discharge of BL-14's shipped half
(`starter-kit/SESSION_RUNNER.md:39`/`:42`): the predecessor session's `HANDOFFS.md` receipt shipped
with `commit: pending`, and the very next session named the real sha, always before its own Phase 1B
claim unless the entry says otherwise. **The derivation method is identical in every entry below and
is stated here, once, not per entry:** the target sha is the first commit — walking
`git log --all --full-history -- HANDOFFS.md` (all refs), read with `bin/check-handoff`'s own
`extract_blocks`/`parse_block` — whose named session's block reads `status: complete`; the claim stub
is the analogous first commit reading `status: pending`; the two are always distinct commits (S29's
gotcha 3, true in every case below); `git rev-list --count --no-merges <target-sha>..HEAD`, taken at
the time of reconcile, is `0` unless an entry says otherwise (no ghost session, no backfill owed).
**Precedents are not restated per entry** — in this prepend-ordered file, every Reconcile-on-read
heading *below* a given entry already is that entry's precedent list; nothing is lost by not
repeating it. The ordinal is reproducible, not incremented on faith:

```sh
grep -cE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[ad hoc\] Reconcile-on-read' CHANGELOG.md docs/archive/CHANGELOG-*.md
```

counts every discharge below plus the one bulk repair; subtract the repair to get the discharge
ordinal. **Each entry below states only what the method above cannot supply:** the two shas, whether
the order was taken before or after the discharging session's own claim, and any adjudication or
measurement unique to that reconcile (a two-answer derivation, a frontier disagreement, a G2/SRF
reading). Nothing quantitative recurs on purpose — the `HANDOFFS.md` SRF/byte-size series that runs
through several entries is the same kind of point-in-time reading the paragraph above already asks
you to re-run, never recall. **This is the norm new entries must stay inside** — `bin/tests.sh`
Test 29 fails a new discharge entry whose body exceeds a fixed line budget, so this cannot silently
erode back into prose the way it did before this compaction. The before/after figures for that
compaction are recorded in the action ledger entry below that performed it, not restated here.

**Archived 10 record(s), 2026-08-02 → 2026-08-02** into [`docs/archive/CHANGELOG-through-2026-08-02.md`](docs/archive/CHANGELOG-through-2026-08-02.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-08-02.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-02.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.1.1.

**Archived 70 record(s), 2026-08-03 → 2026-08-09** into [`docs/archive/CHANGELOG-through-2026-08-09.md`](docs/archive/CHANGELOG-through-2026-08-09.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-08-09.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-09.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.1.1.

**Archived 68 record(s), 2026-08-02 → 2026-08-11** into [`docs/archive/CHANGELOG-through-2026-08-11.md`](docs/archive/CHANGELOG-through-2026-08-11.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-08-11.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-11.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.1.3.

**Archived 28 record(s), 2026-08-12 → 2026-08-15** into [`docs/archive/CHANGELOG-through-2026-08-15.md`](docs/archive/CHANGELOG-through-2026-08-15.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-08-15.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-15.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.2.0.

**Archived 26 record(s), 2026-08-15 → 2026-08-17** into [`docs/archive/CHANGELOG-through-2026-08-17.md`](docs/archive/CHANGELOG-through-2026-08-17.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-08-17.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-17.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.3.0.

**Archived 23 record(s), 2026-08-18 → 2026-08-24** into [`docs/archive/CHANGELOG-through-2026-08-24.md`](docs/archive/CHANGELOG-through-2026-08-24.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-08-24.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-24.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.3.0.

**Archived 12 record(s), 2026-08-25 → 2026-08-25** into [`docs/archive/CHANGELOG-through-2026-08-25.md`](docs/archive/CHANGELOG-through-2026-08-25.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-08-25.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-25.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.3.0.

**Archived 58 record(s), 2026-08-26 → 2026-08-30** into [`docs/archive/CHANGELOG-through-2026-08-30.md`](docs/archive/CHANGELOG-through-2026-08-30.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-08-30.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-30.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

**Archived 54 record(s), 2026-08-12 → 2026-09-02** into [`docs/archive/CHANGELOG-through-2026-09-02.md`](docs/archive/CHANGELOG-through-2026-09-02.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-09-02.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-02.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

---

## 2026-09

### 2026-09-07 · [ad hoc] S152 — pushed `main` to `origin`, deleted five merged local branches, and rewrote a `next_steps` that stated facts instead of naming actions

**Three actions, all operator-directed.** (1) `git push origin main` — `defefb0..71a8d33`, **verified
by reading the remote back** rather than from the push output: `git ls-remote --heads origin main`
and `git rev-parse origin/main` both `71a8d33`, `git rev-list --count origin/main..main` = **0**.
(2) `git branch -d` on the five branches `git branch --merged main` listed —
`docs/learning-13-handoff-predictions` (`73b72c0`), `pr1/framework-learnings-extraction`
(`5b92b2f`), `pr2/ledger-trimmer` (`56997af`), `pr3/apparatus-extraction` (`2c30d0f`),
`pr4/context-budget-gate` (`cf15489`). Each was confirmed an ancestor of `main` with
`git merge-base --is-ancestor` **before** deletion, and `-d` (never `-D`) would have refused any that
was not. **LOCAL ONLY — one copy of each still exists on `origin`**, and removing those is an
outward action on the fork that was not requested; it is `next_steps` (6). **Nothing on
`KJ5HST/methodology`:** `upstream/main` `512c2ed` and `read-set-budgets` `598c459` unchanged, 0 open
PRs.

**(3) THE `next_steps` FIELD WAS REWRITTEN BECAUSE THE OPERATOR CAUGHT IT STATING STATE INSTEAD OF
PRESCRIBING ACTION** — and that is a **protocol violation**, not a style note.
`starter-kit/SESSION_RUNNER.md` §3D's Minimum Handoff Requirement **3** is *"What's next — specific
and actionable"*, whose own bad example is *"Pick next from backlog"* and whose rule is that a
handoff missing it *"will score ≤4/10 by the next session."* The version shipped at `71a8d33` failed
it three ways: item (1) opened *"DO NOT START …"*, a **prohibition** with no accompanying task;
items (2) and (3) opened *"`HANDOFFS.md` IS NOW THE LOUD ONE"* and *"THE TRIMMER SHIPS A STOP IT DOES
NOT HONOUR"*, both **descriptions of a condition** with no verb; and the two genuinely-next actions —
push, delete the branches — sat **outside the numbered list** as loose trailing prose, so the ranked
list did not contain the ranked work.

**What replaced it.** Six items, each opening with an **imperative** and carrying its first command,
with any gate named **before** the verb: (1) *put Tier-2 (a) to the operator as a three-option
decision, then build the branch* — the upstream plan's next phase, §11.1 read first because it
changes what the options mean; (2) *rewrite `30ddf26:CHANGELOG.md:92-94`*, explicitly **not** blocked
by (1); (3) *ask the operator to release `HANDOFFS.md`, then trim it*, with the three gates that trim
must clear; (4) *change `HOW_TO_USE.md:774` 27 → 28*; (5) *fix `choose_cut`*; (6) *delete the five
branches on `origin`*. **The ranking rule is unchanged and is why (1) is (1):** handoff item 1 is the
upstream plan's next phase, never fork housekeeping.

**The budget forced the trade, and the checker dictated which way it went.** Adding the actions took
the record to **13,132 B** against the 12,288 B per-record budget. `bin/check-handoff`'s refusal text
is prescriptive — *"CUT THE TRAILING PROSE FIRST … the Phase 3A/3B essays below the closing fence are
what it is sized to exclude"* — so the 3A/3B essays were cut across four rounds and **no finding was
removed from `next_steps`**. Final record **12,282 B**, 6 B of margin. `bin/check-handoff` **0** bare
and `--all`.

### 2026-09-07 · [ad hoc] S152 — Phase 3 completed: the 3A/3B evaluations and Learning #56 that the close-out skipped, and a self-score revised 8 → 7

**A correction to this session's own close-out (`00347a7`), recorded rather than quietly patched.**
That commit reported Phase 3 complete. **It was 3 of 7 steps short:** 3A (evaluate the predecessor's
handoff), 3B (self-assess) and 3C (document learnings) were never performed. The operator had to ask
for them. Steps 3D–3G *were* done, which is why nothing caught it — **`bin/check-handoff` returned
exit 0 throughout**, and that is exactly what `starter-kit/SESSION_RUNNER.md` §3D says it means:
the checker *"asserts its presence and completeness, never its quality (a green check is not a good
handoff — that stays the next session's 3A score)."* A mechanical gate passing over a missing
compounding step is the gate behaving correctly and the session behaving badly.

**3C — Learning #56 appended to [`starter-kit/FRAMEWORK_LEARNINGS.md`](starter-kit/FRAMEWORK_LEARNINGS.md):**
*"A convention counted across a corpus can be a sample of the rule's OUTPUT, not the rule — and the
lone exception is often the case the written policy was built around."* Sourced from this session's
8-of-9 shard survey, which argued for a calendar cut and was backwards. `bin/check-learnings` **OK —
55 rows, contiguous 1..55, 0 over 1,500 B**. **The next number was 56, not 55:** `#14` is
deliberately reserved (`bin/check-learnings:74`, `RESERVED_RE`), so the checker's *"contiguous
1..54"* message describes a count while the highest live row number was already **55**. Read the
raw rows, not the summary line.

**3A/3B — written below the receipt's closing fence, and the budget is what constrains them.**
`bin/check-handoff` refused the first draft: *"record S152 is 13,786 B, over the 12,288 B
per-record budget by 1,498 … CUT THE TRAILING PROSE FIRST."* The budget is sized so the six
mandatory fenced requirements fit and the 3A/3B essays are what it excludes; the receipt already
carries their conclusions as `self_score` and `predecessor_score`. Three lower-value lines were cut
rather than any finding. Final record **12,222 B**, 66 B of margin. Worth noting the house
convention is genuinely mixed: S150, S149 and S148 carry **2 B** of trailing prose — none at all —
while S151 carries 3,106 B.

**`self_score` revised 8 → 7 in the receipt, and the reason is the skip, not the deliverable.** The
trim itself is unchanged: complete, and proved twice from independent instruments. But a phase
reported complete while 3 of its 7 steps were missing is not an 8, and the three missing steps are
precisely the ones that exist for someone other than this session. **Predecessor S151 scored 7/10** —
its refusal to trim on unrepealed operator provenance was the single most useful thing it did for
this session, against a `next_steps` (4) that was false and ranked already-finished work.

**A DEFECT FOUND BY THE 3F CROSS-REFERENCE SWEEP, RECORDED NOT FIXED (FM #17).**
[`HOW_TO_USE.md`](HOW_TO_USE.md)`:774` says the failure-mode table is *"A table of **27** documented
agent tendencies"*. **The highest FM row is 28**, and [`CLAUDE.md`](CLAUDE.md)`:104` already says 28.
It is **live prose** under *#### What the Session Runner Contains* — not frozen release notes, so it
is unlike `README.md`'s v3.2–v3.6 sections where *"the count stays 27"* is correct as shipped and
must **not** be "fixed". **`HOW_TO_USE.md` is `TRACKED` in `bin/_manifest.py`, so the stale count
ships to every adopter.** Pre-existing, unrelated to this session's diff, and left for a session that
can own it. ⚠ **Do not count it with `grep -c '^| [0-9]* | \*\*' starter-kit/SESSION_RUNNER.md` —
that returns 34**, because the runner holds more than one numbered table; take the highest FM row
number instead. That is S12's gotcha (2), reproduced exactly here.

**No new verification claim is made for the deliverable.** The trim's evidence stands as recorded at
`00347a7`. This commit re-ran what its own diff can affect: `bin/tests.sh` (a distributed file
changed), `check-learnings`, `check-handoff` bare and `--all`, `check-links` — results in the
receipt's `runtime_smoke`. **Fork-internal: no PR, comment, tag or release.**

### 2026-09-07 · [ad hoc] S152 close-out — `CHANGELOG.md` is readable again: 269,571 B → 98,341 B, 54 records to a frozen shard, self-score 8/10

**Phase 3D/3F. Deliverable complete.** Three commits plus this close-out: `0f3f693` the claim,
**`aaa6d30` the trim**, `f2117bd` the `chore(history)` for the append-only `.jsonl`.
**FORK-INTERNAL ONLY — no PR, comment, tag or release on `KJ5HST/methodology`.** `upstream` refs
re-read at Phase 0 and unchanged: `main` `512c2ed`, `read-set-budgets` `598c459`; `gh pr list` empty
on **both** repos.

**THE FILE PHASE 0 MANDATES READING WAS UNREADABLE, AND THAT IS NOW MEASURED RATHER THAN INFERRED.**
At claim time `CHANGELOG.md` was 263,953 B and by the claim commit 269,571 B, against
`READ_REFUSE_BYTES` = 262,144 B (`starter-kit/methodology_trim.py:130`). I did not read the constant
and predict: a default `Read` returned **no content at all** — *"File content (257.8KB) exceeds
maximum allowed size (256KB)"*. It is now **98,341 B**, with **163,803 B** of headroom to the refusal
and **98,267 B** to the 196,608 B fire trigger. `methodology_trim.py --file CHANGELOG.md --check`
exits **0** — the trigger no longer fires.

**LOSSLESSNESS IS PROVED TWICE, FROM TWO INDEPENDENT INSTRUMENTS.** (1) The tool's own clauses, all
green on the artifacts: `L1_OK` (records-zone concatenation byte-identical), `L2_OK` (zones pinned,
front-matter diff confined to declared changes), `L3_OK` (80 records partitioned, every one
byte-identical across the move), `P1A_OK` (26 → 27 entries). `bash
docs/archive/CHANGELOG-through-2026-09-02.md.verify.sh` re-derives all three **from git** at the trim
commit and exits **0**. (2) **`bin/tests.sh` conserves the population without being asked to** —
live `**Model:**` bullets **41 → 8**, archived **238 → 271**, total **279 → 279**. The two deltas are
exactly ±33. That check exists only because S132 taught `bin/model-report` to glob the shards; before
that fix this trim would have blinded it to 33 of 41 entries with every row still green.

**THE ONE DESIGN CHOICE WAS SETTLED FROM PROVENANCE, AGAINST MY OWN FIRST MEASUREMENT.** The dry run
raises `CUT_STRADDLES_DAY` and offers `--cut <earlier date>`. I surveyed the nine dated shards and
found **8 honour a clean day boundary and 1 does not**, and was ready to recommend a calendar cut on
that 8-of-9 evidence. **It points the wrong way.** The ninth —
`CHANGELOG-through-2026-08-30.md` — is precisely the shard this file's own front matter (`:54`)
cites when it ratifies *"that boundary is POSITIONAL, not a calendar seam … The sections are the
calendar; the file boundary is not."* [`ledger-trimmer-design.md:219`](docs/planning/ledger-trimmer-design.md)
§2.3 says the same at the source — *"cuts are by **position in file order**, never by sorting on a
parsed key"* — and its §3.1 table gives this file's cut key as literally `position`. **A majority
across a corpus is a sample; the outlier was the one carrying the policy.** Default cut taken, no
override.

**A DEFECT IN THE DISTRIBUTED TRIMMER, FOUND BY ASKING WHY A NUMBER WAS 37 B TOO BIG.** The dry run
projected **98,341 B** while `CLASS_A_STOP_BYTES` (`:165`) is **98,304**. `choose_cut` (`:1014`)
selects the largest retained count `k` for which `stops(b)` holds, computing `b` from the
**pre-trim** front matter: `resulting(26)` = **97,108 B**, comfortably under. The write then adds
**1,233 B** of front matter — a 453 B pointer block plus regenerated fields — so the file lands
**37 B above the stop the selection was supposed to guarantee**. Immaterial here (0.04%, against
98,267 B of hysteresis) and **deliberately not worked around with `--cut`**: overriding the ratified
default to hide a tool defect would have made the next session's dry run inconsistent with this one
and left nothing on the record. **The tool is DISTRIBUTED** (`bin/_manifest.py`), so the fix is
adopter-facing and is its own deliverable. **Recorded, not fixed** (FM #17).

**A FALSE PREMISE IN MY PREDECESSOR'S HANDOFF, CAUGHT BEFORE IT COST THE SESSION.** S151
`next_steps` (4) calls the `context_budget.py` exit-2 *"Phase 2 of the older
`upstream-read-set-pr-plan.md`, **never executed**."* **Phase 2 shipped at S119** — `28551a5` (scope
the row budget to every row, driven RED) and `364b410` (compact all 20 over-budget rows, 73,712 →
56,673 B), both verified ancestors of `main`; `bin/check-learnings` reports **0 over 1,500 B**,
exit 0. And the 69,749 B is `starter-kit/SESSION_RUNNER.md` (54,363) + `starter-kit/SAFEGUARDS.md`
(15,386), class `read-set`; `starter-kit/FRAMEWORK_LEARNINGS.md` is class `on-demand` and is **not a
member**, so Phase 2 could never have closed that gap. **§11 of that very plan
(`upstream-read-set-pr-plan.md:483`) had already corrected both errors, naming S130 for making them.
This is the third recurrence, and the mechanism is identical each time: the session took its premise
from the previous receipt rather than from the plan the receipt cites.** Consequence for ranking:
**all four executable phases (1–4) are shipped**; only **Phase 5**, which needs the operator's
explicit go-ahead, remains.

**Verification, every command run bare, compared row-for-row against a Phase 0 baseline.**
`bash bin/tests.sh` **304 passed / 1 failed / 0 skipped, exit 1** — identical summary, identical
**305** rows, and **ZERO status flips**; every differing row is `PASS` on both sides and every changed
value is a count the trim moved. The one failure, `github source dry-run failed`, is pre-existing and
its cause was measured rather than assumed: **3 of 27** `bin/_manifest.py` source paths
(`FRAMEWORK_APPARATUS.md`, `starter-kit/FRAMEWORK_LEARNINGS.md`, `starter-kit/methodology_trim.py`)
are absent from `upstream/main`, and `bin/sync:134` `sys.exit()`s before writing anything.
`check-links` **0**, `check-learnings` **0** (54 rows, contiguous 1..54), `check-handoff
--allow-pending` **0**, `--all --allow-pending` **0**. `unittest`: dashboard **321 OK**,
`methodology_trim` **123 OK**, `context_budget` **116 OK** (result row isolated from the advisory
prose it prints after it). Dashboard twins `cmp` **silent**. `context_budget.py` **exit 2**,
unchanged and pre-existing. Both ledgers verified byte-identical to their commits **after** the suite
run, which mutates and restores them — checked against `git status`, not against a copy of themselves.

**ZERO ADOPTER SURFACE, established by grepping the whole manifest rather than one column.** The only
`CHANGELOG` row in `bin/_manifest.py` is `("starter-kit/CHANGELOG.md", "CHANGELOG.md", SEED)` — the
**seed**. The root ledger trimmed here is this repository's own and is distributed nowhere.

**`HANDOFFS.md` was deliberately left alone.** At 222,968 B it is past its own 196,608 B trigger but
**39,176 B clear of the refusal**, and it holds 25 receipts against the ratified cap of 4. One
deliverable is one deliverable; that trim is a real piece of work with its own losslessness proof and
its own `bin/tests.sh` Test 34 three-receipt floor to respect.

### 2026-09-07 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-09-02.md` (54 record(s), 269,571 B → 98,341 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **54** record(s) (2026-08-12 → 2026-09-02) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-09-02.md`](docs/archive/CHANGELOG-through-2026-09-02.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-09-02.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-02.md.verify.sh)
rather than trusting a digest printed here. Live file 269,571 B → 98,341 B (−63.5%).

### 2026-09-07 · [ad hoc] S152 — claim: trim `CHANGELOG.md`, which is 1,809 B PAST the 262,144 B hard read refusal

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: run
[`starter-kit/methodology_trim.py`](starter-kit/methodology_trim.py) `--file CHANGELOG.md --write`
on **this** file, archiving its oldest records into a frozen shard under `docs/archive/` with the
tool's own losslessness proof and `.verify.sh`. **Fork-internal: `origin` only. No action on
`KJ5HST/methodology` — no PR, no comment, no tag, no release.**

**The warrant is a measurement, and it is new since S151 wrote its handoff.** This file is
**263,953 B**. `starter-kit/methodology_trim.py:130` sets `READ_REFUSE_BYTES = 256 * 1024` =
262,144 B — *"a SECOND and HARDER boundary, and it is NOT truncation"* — so this ledger is **1,809 B
(1.0069×) past it**. Verified by running the tool rather than by reading the constant: a default
`Read` of `CHANGELOG.md` returns **no content at all**, front matter included —
*"File content (257.8KB) exceeds maximum allowed size (256KB)"*. The artifact Phase 0 mandates
reconciling is, today, unreadable by the tool Phase 0 uses. S151 measured **243,957 B** and called it
*"~18 KB from"* the refusal; its own five close-out commits carried it across.

**THE BLOCKER WAS RELEASED BY THE OPERATOR THIS SESSION, AND THAT RELEASE IS ITSELF THE RECORDED
ACTION.** The trim was deprioritised at **S129** — when the file in question was `HANDOFFS.md` at
5 receipts and 7,305 B over a *soft* one-read cap — and no repeal stood on record; S151 declined the
trim on exactly that provenance and was right to. Presented at this session's Phase 0 gate with the
changed fact pattern (a *hard* refusal, on the *other* ledger), the operator chose **"Trim
CHANGELOG.md"**. `HANDOFFS.md` is deliberately **out of scope**: at 221,606 B it is past its own
196,608 B trigger but still **40,538 B clear of the refusal**, and one deliverable is one deliverable.

**The cut is POSITIONAL and this session will not override it.** The dry run flags
`CUT_STRADDLES_DAY` and offers `--cut <earlier date>` for a clean calendar seam. **Refused, on
provenance, not on preference.** Design
[`docs/planning/ledger-trimmer-design.md`](docs/planning/ledger-trimmer-design.md) §2.3 states *"cuts
are by **position in file order**, never by sorting on a parsed key"* and its §3.1 table gives this
file's cut key as literally `position`; this file's own front matter (`:56`) ratifies the same rule —
*"that boundary is POSITIONAL, not a calendar seam … The sections are the calendar; the file boundary
is not."* A survey of the nine dated shards shows **8 honour a clean day boundary and 1 does not** —
and the one that does not, `CHANGELOG-through-2026-08-30.md`, is precisely the shard the front matter
cites as the reason the convention is a span label. **That 8-of-9 count is a sample that points the
wrong way**; the ninth carries the policy.

**Planned cut, from the dry run and to be re-derived before `--write`:** archive **52 of 79** records
(span 2026-08-12 → 2026-09-02) to `docs/archive/CHANGELOG-through-2026-09-02.md`; live
**263,953 B → 98,303 B**, one byte under the 98,304 B `CLASS_A_STOP_BYTES`. Proof clauses all green
on the dry run: `L1_OK` (records-zone concatenation byte-identical), `L2_OK` (zones pinned,
front-matter diff confined to declared changes), `L3_OK` (79 records partitioned, every one
byte-identical across the move).

**Phase 0 baseline, every command run bare before any edit.** `bash bin/tests.sh` **304 passed /
1 failed / 0 skipped, exit 1** — the one failure is `github source dry-run failed`, pre-existing, and
its cause was measured this session rather than assumed: **3 of 27** `bin/_manifest.py` source paths
(`FRAMEWORK_APPARATUS.md`, `starter-kit/FRAMEWORK_LEARNINGS.md`, `starter-kit/methodology_trim.py`)
are absent from `upstream/main`, and `bin/sync:134` `sys.exit()`s before writing anything. Nothing in
a fork-internal trim can flip it. `bin/check-links` **0**, `bin/check-learnings` **0** (54 rows,
contiguous 1..54, 0 over 1,500 B), `bin/check-handoff` **0**, `--all` **0** (24 receipts).
`starter-kit/context_budget.py` **exit 2** (read-set total 69,749 B / 56,750) — pre-existing and
out of scope. Ledger accounting before: **442** source-tagged dated entries across live + archives,
**79** records live, **24** receipts. Both ledgers backed up outside the repo and `shasum -c` clean
after the baseline suite run, which mutates and restores them.

**A correction to S151's handoff, carried here because it misdirects the next session.** Its
`next_steps` (4) calls the `context_budget.py` exit-2 *"Phase 2 of the older
`upstream-read-set-pr-plan.md`, **never executed**."* **Phase 2 shipped at S119** — `28551a5` (scope
the row budget to every row, driven RED) and `364b410` (compact all 20 over-budget rows, 73,712 →
56,673 B), both verified ancestors of `main`; `bin/check-learnings` reports **0 over 1,500 B**,
exit 0. And the 69,749 B is `starter-kit/SESSION_RUNNER.md` (54,363) + `starter-kit/SAFEGUARDS.md`
(15,386) — class `read-set` in `.context-budget.json`; `starter-kit/FRAMEWORK_LEARNINGS.md` is class
`on-demand` and is not a member, so Phase 2 could never have closed that gap. This is the **third**
recurrence of the drift §11 of that plan was written to stop — each session taking its premise from
the previous *receipt* rather than from the plan the receipt cites. **All four executable phases
(1–4) are shipped; only Phase 5, which needs the operator's explicit go-ahead, remains.**

### 2026-09-04 · [ad hoc] S151 close-out — Phase B DONE: `upstream/read-set-budgets` (`598c459`) MERGED into fork `main` as `213f841` and pushed to `origin`

**Phase 3D/3F.** Deliverable: Phase B of
[`docs/planning/upstream-read-set-budgets-merge-plan.md`](docs/planning/upstream-read-set-budgets-merge-plan.md)
§3, under the operator's explicit go-ahead. **A real two-parent merge commit `213f841` (parents
`8bfff1e` + `598c459`), never a squash and never an `-X` strategy shortcut**, pushed to the fork:
`origin/main` = local `main` = `f7c7008`, 0 unpushed. **FORK-INTERNAL — no PR, comment, tag or
release anywhere; `upstream` refs re-read after the push and unchanged from Phase 0** (`main`
`512c2ed`, `read-set-budgets` `598c459`), `gh pr list` empty on both repos. Completeness measured,
not assumed: `git rev-list --count main..upstream/read-set-budgets` = **0** and `main..upstream/main`
= **0**, so upstream's own S12 release commit came in too, and all four `pr1`–`pr4` branches now
report as fully merged.

`git merge --no-commit` produced **exactly the 20 conflicts §2.2 enumerates**, re-derived against
today's tree before starting rather than trusted from the plan's snapshot. **14 keep-ours, each
verified byte-identical to `HEAD` after resolution**; **2 take-theirs verified byte-identical to
upstream's blob** (`tools/test_context_budget.py`, which discharges D11's back-port follow-on by
construction, and `tools/test_methodology_trim.py` 2,170 → 2,259 lines, the portable synthetic
fixtures). **Row 7 was adjudicated on the merits rather than on the plan's authority:** measuring the
file's real link sites showed fork's *"Phase 2 step 8"* named **one of three** (`:189`–`:191` are
steps 6, 7 and 8), while upstream's sentence additionally names `:309`'s honest-accounting bullet and
`:478`'s *Across the Full Series*, both of which genuinely carry links — all seven anchors confirmed
to resolve in `FRAMEWORK_APPARATUS.md`. **Row 13 recomputed to the measured 27** (23 markdown + 4
non-markdown); both sides' *"24"*/*"25"* were stale. Ledgers interleaved by date per §2.3: upstream's
four `CHANGELOG.md` entries placed **after** fork's of the same date (the tie-break this file's own
front matter documents), the two pre-2026-08-30 ones at the bottom, **no frozen archive shard
touched**; upstream's S12 receipt kept, placed last, its `---` separator normalised to
`HANDOFFS.md`'s convention, and the front matter's collision paragraph now names the resulting
**live** S12 collision (fork's own S12 is 2026-07-25, archived). **Beyond what the plan asked:** it
says only to "re-verify" the 90-path auto-merged set, so this session checked whether upstream
content had been *dropped* there — of the four both-sides paths upstream had touched only
`starter-kit/SESSION_RUNNER.md`, and **all 3 of its added lines survive while 0 of its 18 deleted
lines do.**

**Two of the plan's own verify-column expected values were wrong, recorded as measured rather than
smoothed over:** `context_budget.py` was to *"exit 0 after"* — it exits **2**, identically before and
after (the pre-existing read-set overage, Phase 2 of the older plan, never executed); and `grep -c
'methodology_trim.py' starter-kit/BOOTSTRAP.md` was to be **1** — it is **5**, and was 5 pre-merge.
The second invites a destructive repair. Recorded as new **Learning #55** in
`starter-kit/FRAMEWORK_LEARNINGS.md` (54 rows, contiguous, 0 over the 1,500 B row budget).

**The retention trim was deliberately NOT done, on provenance rather than oversight.**
`HANDOFFS.md` holds **24** receipts against the ratified cap of **4**, and both ledgers now fire
`methodology_trim.py --check`. §2.3 step 4 says *"trim to 4"*, but the same plan's `next_steps` (3)
says the overage is *"not this plan's or this close-out's to act on"*, and **the operator
deprioritised this trim at S129 with no repeal on record**. Step 4 assumed a file already near the
cap; a 24 → 4 trim is a deliverable with its own losslessness proof. Raised for the operator, not
absorbed.

**Verified.** `bash bin/tests.sh` **304 passed / 1 failed / 0 skipped, exit 1** — compared **row for
row** against the pre-merge baseline: **zero status flips**. The one failure is Test 9
(`--source=github`), pre-existing, and §2.4 predicted a fork-internal merge could not flip it — it
did not. An intermediate run read **303/2**: this session's own front-matter edit had pushed
`HANDOFFS.md`'s header 205 B over its 7,168 B reserve and turned Test 39's A2 RED. Fixed as this
repo's own notes prescribe — **cut the edit, do not raise the reserve** — now 7,122 B. `check-links`
**0** (105 links / 23 files), `check-learnings` **0**, `check-handoff --all` **0** at close-out.
`unittest`: dashboard **321 OK**, context_budget **116 OK**, methodology_trim **123 OK** — the last
being row 20's never-before-run combination. `cmp` of the two dashboard twins silent. Ledger
accounting: **74 → 78** dated entries and **437 → 441** source-tagged across live + archives;
receipts **23 → 24**. Both ledgers `shasum -c` clean after every suite run. Adopter surface, which
the plan did not ask for: `bin/sync <tmp> --mode=commit` exit **0**, **27 files** installed, the
merged `ITERATIVE_METHODOLOGY.md` sentence and Learning #55 both landing. Not exercised: upstream CI
(neither side has `.github/workflows` — confirmed absent, not assumed), the maintainer's machine,
`--calibrate`.

**Model:** Claude Opus 5 (1M context).

### 2026-09-04 · [ad hoc] S151 — claim: Phase B of the merge plan — merge `upstream/read-set-budgets` (`598c459`) into fork `main`

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: execute
**Phase B** of [`docs/planning/upstream-read-set-budgets-merge-plan.md`](docs/planning/upstream-read-set-budgets-merge-plan.md)
§3 — the real 3-way merge of `upstream/read-set-budgets` (`598c459`, PR #79 merged) into fork `main`
(`94ea01f` at claim), authorized by the operator's explicit go-ahead this session (*"do phase B"*),
the same gate PR 4's own Phases C and D each required. **Fork-internal: `origin` only. No action on
`KJ5HST/methodology` — no PR, no comment, no tag, no release.**

Scope, exactly as §2.2/§2.3/§2.4 state it and no wider: `git merge upstream/read-set-budgets
--no-commit` (never a `-X ours`/`-X theirs` shortcut), all **20** conflicting paths resolved per
their stated rule (13 keep-ours, 3 take-theirs, 2 decided on their own terms, 2 ledgers), both
ledgers interleaved by date per §2.3's rule, the full §2.4 command set run bare and its **measured**
results recorded in the merge commit message, then a real two-parent merge commit (never a squash)
pushed to `origin`. Conflict count re-derived at Phase 0 against today's tree: `git merge-tree
--write-tree --name-only main upstream/read-set-budgets` → **20 CONFLICT lines**, matching §2.2
row-for-row.

Phase 0 baseline, run bare before any edit: `bash bin/tests.sh` **304 passed / 1 failed / 0 skipped,
exit 1** (the one failure `github source dry-run failed` is Test 9, pre-existing, and §2.4 states
plainly it will NOT flip from this merge). `check-handoff` **0**, `--all` **0** (22 receipts),
`check-links` **0**, `check-learnings` **0** (53 rows, contiguous 1..53), `context_budget.py`
**exit 2** (read-set total 69,749 B / 56,750 — pre-existing, the never-executed Phase 2 of the older
read-set PR plan, out of scope here).

**Model:** Claude Opus 5 (1M context).

### 2026-09-04 · [ad hoc] S150 close-out — the upstream/read-set-budgets merge plan DONE: `docs/planning/upstream-read-set-budgets-merge-plan.md` committed, Phase B NOT authorized

**Phase 3D/3F.** Deliverable: the one plan the S150 claim scoped — a real, mechanically-verified
evidence-based inventory of every path `upstream/read-set-budgets` (`598c459`, PR #79 merged) conflicts
on with fork `main`, a resolution rule and verification command per path, and the two-phase structure
`SESSION_RUNNER.md` §Planning Sessions requires. **No merge, no push, no upstream action.**
`git merge-tree --write-tree --name-only main upstream/read-set-budgets` → tree `a9b72fee…`, exit 1,
**20 conflicting paths (4 add/add, 16 content)** — corrects the interrupted S150 stub's unverified guess
of *"5 add/add, 15 content"*. Each of the 20 individually diffed (`git diff --stat <merge-base> main --
<path>` / `… upstream/read-set-budgets -- <path>` / `diff <(git show main:<path>) <(git show
upstream/read-set-budgets:<path>)`), yielding: 13 keep-ours (fork's version is a strict superset — later,
more advanced, or already proven by its own tests), 3 take-theirs (`ITERATIVE_METHODOLOGY.md`'s pointer
sentence, plus two add/add test modules — `tools/test_context_budget.py`'s D9-scrubbed wording and
`tools/test_methodology_trim.py`'s portable synthetic fixtures, a previously-unflagged case of the same
back-port pattern D9 already named for the other module), 2 decided on their own terms (`.context-budget.json`
stays fork's own per the ratified D11; `docs/tutorials/T8_keeping_current.md`'s stale *"24 vs. 25
distributed files"* claim is recomputed to the real, measured **27**, not picked), and the two ledgers
(`CHANGELOG.md`, `HANDOFFS.md`) interleaved by date per the convention their own front matter documents,
the same rule five prior resync merges (`aa378ab` et al.) already established. **A correction to the
ratified `pr4-read-set-budgets-plan.md`'s own D11 arithmetic, recorded rather than edited into that closed
document:** D11 said PR 4 adds *"two more, 19 in all"* beyond a measured 17-path baseline against
`cea3068`; PR 4 actually adds a third — `.gitignore` (its own §3.6) — making the true total 20, exactly
what today's measurement shows.

**TWO OF THE PLAN'S OWN FIRST-DRAFT CLAIMS WERE CAUGHT AND CORRECTED BEFORE COMMIT, BOTH RECORDED IN THE
PLAN RATHER THAN SILENTLY FIXED.** (1) The auto-merged-set breakdown first guessed *"76 paths exist only
on fork `main`, 14 exist on both sides"* without checking which side actually has each path; tested
directly (`git cat-file -e upstream/read-set-budgets:<path>` per path), the true split is **86/4**. (2)
A first draft predicted `bin/tests.sh`'s pre-existing Test 9 failure would flip to passing once this
merge lands, reasoning that the merge supplies the 3 manifest sources Test 9 finds missing; reading
`bin/sync`'s actual `--source=github` fetch call (`gh api repos/KJ5HST/methodology/contents/<src>`, no
`ref=`) shows it queries `upstream/main`'s live GitHub default branch, which this fork-internal merge
never touches — Test 9 stays red for its pre-existing reason until `read-set-budgets` reaches
`upstream/main`, the maintainer's action. Both corrections are the same "run it, don't predict it"
discipline this repo's Learning #50 already names, applied to this session's own drafting rather than to
a predecessor's.

**Commits this session:** `d040bd0` (claim, from the earlier, correctly-halted S150 attempt);
`75f1cf6` `chore(history)` (`--no-verify`, the dashboard series Phase 0 dirtied then); this close-out
(the plan document, this ledger entry, the completed receipt). **Runtime smoke, bare, at close-out
with the plan committed:** `bash bin/tests.sh` → **304 passed, 1 failed, 0 skipped, exit 1** — unchanged
from the Phase 0 baseline taken before writing anything (Test 9, pre-existing, expected until
`read-set-budgets` reaches `upstream/main`). Checkers, each bare: `check-handoff` **0** (22 receipts, the
newest complete), `--all` **0** (22 receipts), `check-links` **0** (105 links / 23 files),
`check-learnings` **0** (53 rows, contiguous 1..53 with `#14` a documented reserved gap, 0 over 1,500 B).
`CHANGELOG.md` is 233,769 B and `methodology_trim.py --check` still `FIRES` (196,608 B Class A threshold)
— pre-existing, flagged by S149, not this session's to act on (a separate deliverable).

### 2026-09-04 · [ad hoc] S150 — claim: plan the merge of `upstream/read-set-budgets` (`598c459`) into fork `main`

**Authorization:** the operator's *"in the next session make a plan to complete the merge as you have
described"* (2026-09-04), after the S149 assessment of GitHub's *Sync fork* dialog (unusable here: it
targets upstream `main`, which lacks the four PRs, and the ledgers conflict on every sync). **The ONE
deliverable is the plan document** — `docs/planning/upstream-read-set-budgets-merge-plan.md`: the
evidence-based inventory of every path the merge touches (20 conflicting, plus the auto-merged set),
a resolution rule per path with its verification command, the DONE criteria, the surface, and the
session boundary — committed and self-reviewed. **The merge itself is NOT this session's work** (Planning
Sessions: the plan is the deliverable, not a preamble). No push, no upstream action.

**Reconciled at claim:** S149's receipt `commit:` slot named its close-out by description; this commit
names it — `10d5268`. Both ledger frontiers stood at `10d5268` at Phase 0 (gap 0); no backfill is owed.
**A non-commit action to record, done by the operator, not a session:** PR #79 was MERGED on
`KJ5HST/methodology` at `2026-09-04T01:24:30Z` by rmsharp — merge commit `598c459` on `read-set-budgets`,
parents `cea3068` + `cf15489`, tree `c857734` = the head's; `read-set-budgets` is still not in upstream
`main` (`512c2ed`). The PR 4 plan's Phase D record and the body file's header are updated from those
server reads in the next commit, before the planning work.

**Ledger:** `CHANGELOG: pending` — set at claim; recorded at Phase 3F.

### 2026-09-03 · [ad hoc] S149 close-out — Phase C DONE: `pr4/context-budget-gate` (`cf15489`) pushed to `origin` and OPEN upstream as PR #79 against `read-set-budgets`, NOT merged

**Phase 3D/3F.** Deliverable: Phase C of
[`docs/planning/pr4-read-set-budgets-plan.md`](docs/planning/pr4-read-set-budgets-plan.md) (`:703`), on the
operator's *"1"* (item 1 of the S148 close-out's list), claimed in this ledger before acting. **Two
outward-facing actions, both authorized, both read back:** (1) `git push origin pr4/context-budget-gate`
— a new branch on `rmsharp/methodology`, read back `cf15489` / tree `c857734` (re-checked against the
local branch before the push); (2) `gh pr create --repo KJ5HST/methodology --base read-set-budgets --head
rmsharp:pr4/context-budget-gate` with the body file's *Title* and its Body plus the two sections after
the divider (14,003 B; grep for fork-internal identifiers empty) →
**[PR #79](https://github.com/KJ5HST/methodology/pull/79)**, created `2026-09-04T00:59:58Z` (a 2026-09-03
local session; dragon 14). Read back from the server: `state OPEN`, base `read-set-budgets`, `headRefOid
cf15489…` = the local branch, `mergeable MERGEABLE`, `mergeStateStatus CLEAN` (UNKNOWN on the first read,
seconds after creation), `changedFiles 7` = the §3 list exactly, `+2,320 / −98`, two commits (`8df8faa`,
`cf15489`), body 14,004 B with the eight headings sent, not a draft, `reviewDecision` empty.
`upstream/main` `512c2ed` and `upstream/read-set-budgets` `cea3068` untouched; `origin/main` untouched
(`143ff2b`, 2026-08-15). **Not done, deliberately:** no merge (Phase D keeps its own go-ahead), no tag, no
release, no comment on the PR, no push of `main`. Records: the body file's status header (`:3`), the plan's
status line and Phase C record.

**Commits this session, all recorded here:** `974db79` (claim; S148's `commit:` slot reconciled to
`9a49f09`); `6e4c56b` `chore(history)` (`--no-verify`, the dashboard series Phase 0 dirtied); this
close-out (the body header, the plan's status line and Phase C record, both ledgers).

**Runtime smoke in this worktree, at close-out with every edit in place:** `bash bin/tests.sh` → **304 passed / 1 failed / 0 skipped, exit 1 — S148's close-out summary, to the row**
(the one failure Test 9, pre-existing — and still expected to stay red until `read-set-budgets` reaches
`main`; the run mutated and restored the ledgers as Test 34 does). Checkers, each bare: `check-handoff` **0** (21 receipts, the newest complete, 0 over 12,288 B), `--all` **0** (21 receipts), `check-links` **0** (105 links / 23 files), `check-learnings` **0** (53 rows, 0 over 1,500 B).

### 2026-09-03 · [ad hoc] S149 — claim: Phase C of the PR 4 plan — push `pr4/context-budget-gate` (`cf15489`) to `origin` and open the PR against `read-set-budgets`

**Authorization:** the operator's *"1"*, answering the S148 close-out report's numbered list, whose item 1
was Phase C — the explicit, per-action go-ahead `CLAUDE.md` requires for an outward-facing action on
`KJ5HST/methodology`. Recorded here **before** acting, because a push and a PR leave no commit in this
fork ([`docs/planning/pr4-read-set-budgets-plan.md`](docs/planning/pr4-read-set-budgets-plan.md) §5 Phase
C, `:703`). **The ONE deliverable: the branch on `origin` and the PR open, read back from the server** —
`git rev-parse pr4/context-budget-gate^{tree}` still `c857734`; push; `origin/pr4/context-budget-gate`'s
tree read back equal; `gh pr create --repo KJ5HST/methodology --base read-set-budgets` with the body
file's *Title* and *Body*; `gh pr view` read back (state OPEN, base `read-set-budgets`, `headRefOid` =
`cf15489`, mergeable, the seven files); `upstream/main` untouched; the body file's status header updated
from those reads. **No merge (Phase D keeps its own go-ahead), no tag, no release, no comment, no push of
`main`.**

**Reconciled at claim:** S148's receipt `commit:` slot named its close-out by description; this commit
names it — `9a49f09`. Both ledger frontiers stood at `9a49f09` at Phase 0 (gap 0); no backfill is owed.

**Ledger:** `CHANGELOG: pending` — set at claim; recorded at Phase 3F.

### 2026-09-03 · [ad hoc] S148 close-out — the PR 4 fix-round DONE: `pr4/context-budget-gate` REBUILT as `cf15489` on `cea3068`, re-verified, NOT pushed

**Phase 3D/3F.** Deliverable: the six-row fix-round from S147's self-review, applied, and the branch
rebuilt and re-measured — item (1) of S147's handoff, the operator's words. Head **`cf15489`** (tree
`c857734`), two commits on `cea3068` — `8df8faa` commit (1), `cf15489` commit (2) — built in a clean
clone by the §8 R1 recipe (fixtures `020ba3f 7a71df0 e02881a e5cdc66` unreachable, no `docs/archive/`),
each committed **through** upstream's `.githooks/pre-commit` with `core.hooksPath` set, and fetched into
this fork as the local ref `pr4/context-budget-gate`. The two earlier heads are kept as refs, not
branches: S147's `f3a4b6d` and this session's `46089f1` and `c6577f2` (the two the review lenses read),
under `refs/archive/pr4-context-budget-gate-<sha>`. **Nothing pushed, nothing opened; Phases C and D
still need their own go-aheads.** Records: the body file's header and its *fix-round* section
([`docs/planning/pr4-read-set-budgets-body.md`](docs/planning/pr4-read-set-budgets-body.md)), the plan's
§5 Phase B record, §3.1 heading and DONE criterion re-stated with the new blob id.

**Commits this session, all recorded here:** `1086f5c` (claim; S147's `commit:` slot reconciled to
`ae5ff8d`); `6887b67` `chore(history)` (`--no-verify`, the dashboard series Phase 0 dirtied); `22c6cf0`
and `544cfb0`, the two fork-side passes (one entry below, extended for the second); this close-out
(Learning #54, the plan and body records, both ledgers).

**WHAT THE SIX ROWS BECAME.** Rows 2 and 3's fork halves first (`22c6cf0`: the tool's five fork-authored
sites plus the test module's four, the candidate config's two sentences), then the branch: row 1
(`tools/test_context_budget.py:9`, `:13` → the unnumbered upstream block and `bin/tests.sh:237-244`),
row 4 (`.gitignore:5`, later `:8`), row 5 (the two PRs by absolute URL, and *"eight fork commits (seven
that went through the fork's own review rounds, plus one comment-only reword made for this port)"*),
row 6 (*"every git fixture"*, the seed's on-demand note named, *"six lines"* for *"four"*, the tool's
size 73,040 B). **The one site left alone, on evidence:** `starter-kit/context_budget.py:409` *"learning
#22 / #26a"* is upstream's own 1.0.0 text — `git blame` → `df6a991` (KJ5HST, 2026-08-08), present in blob
`be2721a5` — so S147's review had attributed the maintainer's own citation to the port; Learning #54.

**THE REVIEW LENS RE-RAN, TWICE.** A maintainer's-eye reviewer read the first rebuild (`46089f1`) in its
own R1 clone and returned **fourteen** items (3 HIGH, 5 MEDIUM, 6 LOW), every one re-derived by hand:
repaired in `544cfb0` and the third build — `tools/test_context_budget.py:214` (a fork commit `7603f10`
attributed to *"this framework's own repository"*), `:404` (*"PHASE B"* in capitals, missed by a
case-sensitive grep), the ledger entry's 73,014 B (stale by this session's own +26 B), the tool's `:57` /
`:1157` and the seed's *"the project that authors this tool"* (a fork measurement stated as the tool's
home's), the bare `#76`/`#78` (the ledger's own front-matter rule wants absolute URLs), `.gitignore:8`
(*"must survive a fresh clone"* — untracked there), the *"seven reviewed"* wording; kept with the reason
recorded in the body file — `:683` names the fork so it resolves, *"five values"* is D10 (five distinct,
seven sites), the config's sizes are scoped to `cea3068`, `:71` is correct on the tree; two follow-ons
disclosed in the PR body rather than built — `bin/check-learnings:87-89`'s comment goes stale when commit
(2) lands (an eighth file, outside the ratified seven) and the pre-existing `:341` `ResourceWarning`.
Then a second, delta lens on the frozen third build `c6577f2`: all fourteen dispositions confirmed, seven more items — two false provenance sentences the rebuild itself had written (*"eight commits … one reword"* where it is nine and two; *"every intermediate fails"* where the last two pass), a `.gitignore` subject and a bullet naming only one of the two histories, all four repaired in the fourth build `cf15489`; the module's colliding `D1`–`D5` labels, the 20,193/20,194 rounding pair and the seed naming the fork disclosed in the PR body. The lens's verdict, *"not yet — fix F1 and F2 first"*, was acted on; no lens ran on the fourth build's four text edits, which were checked by grep against the reviewer's own commands.

**EVERY DONE ITEM RE-MEASURED ON THE FOURTH BUILD AND MATCHED:** blob `d91677b5`, mode 100755, equal to
fork `main`'s; the module differs from `main:tools/test_context_budget.py` in exactly six lines (8, 9,
13, 288, 561, 613); unit → exit 0, `Ran 116 … OK (skipped=2)`; `--selftest` → 0, 52 / 0; bare → exit 2,
49 lines, 0 *defect*, six findings, `CHANGELOG.md` **97,257 B** (91,365 + 5,892; ≈39,416 tok); `--json`
`config_defects: []`; the 13-case matrix (2 0 2 2 0 2 0 2 0 0 0 0 0; case 12's bare run 2 with
`instrument-failed`); by hand — commit (1) vs `cea3068` no config → **3**; with the candidate in the
worktree → **2** (`91,365 -> 95,557 B`); commit (2) vs commit (1) → **2** (`95,557 -> 97,257 B`); bullet
unstaged → **0**; suites on fresh clones **114/1** (control) vs **115/1** (head) vs **114/2** (commit (1))
— 115 shared rows, one added, zero flips, every failure Test 9; checkers 0/0/0/0; seven files, 2,320 /
98; the identifier regex over added lines and both messages empty; a case-insensitive sweep of the added
lines for the residue class empty; PROPOSAL 8; config `cmp`-identical to the amended candidate; `git
status --porcelain` empty after deleting the history file.

**Runtime smoke in this worktree, at close-out with every edit in place:** `bash bin/tests.sh` → **304 passed / 1 failed / 0 skipped, exit 1 — S147's close-out summary, to the row**
(the one failure Test 9, pre-existing; the run mutated and restored the ledgers as Test 34 does).
Checkers, each bare: `check-handoff` **0** (20 receipts, the newest complete, 0 over 12,288 B), `--all` **0** (20 receipts), `check-links` **0** (105 links / 23 files), `check-learnings` **0** (53 rows, 0 over 1,500 B).

**Two harness gotchas, recorded for the next builder:** in `zsh` an unquoted `$CB` holding `python3
starter-kit/context_budget.py` does not word-split, so every by-hand and matrix case came back **127**
(*command not found*) on the first pass — eighteen identical exits no case is specified to produce; use a
shell function. And a residue grep must be case-insensitive: *"PHASE B"* survived a `Phase B` sweep.

### 2026-09-03 · [ad hoc] S148 — reword the fork-relative comments in `context_budget.py`, its test module and the PR 4 candidate config (the fix-round's fork-side half: rows 2 and 3)

**The fork-side prerequisite of the fix-round, committed on `main` BEFORE the branch is rebuilt so the
ported tool blob stays byte-identical to fork `main` (the shape row 2 of the decision table prescribes).**
Comment-only, behaviour unchanged, line counts unchanged in both Python files (so the plan's §3.1 symbol
line numbers still hold), every edited line ≤ 99 columns. `starter-kit/context_budget.py` blob
`c5ff15e5` → **`0b103baf`** (73,014 → 73,040 B): `:289-290` (*"this repository's own
SESSION_RUNNER.md is 54,363 B"* → the authoring fork's, which it was), `:675` and `:1204` (*"Phase B"*
→ the date, 2026-08-26), `:683` (the planning-doc pointer now names `rmsharp/methodology`), `:733`
(*"this repository's own history"* → the authoring repository's). `tools/test_context_budget.py` blob
`a671113` → **`f6c94d85`**: `:417`, `:424` (*"Phase B"* → the date), `:484` (*"Measured on this repo"*
→ the authoring fork), `:546` (*"wsfct"* → one adopter) — the folds the table's *Kept as ratified*
paragraph assigns to row 2, plus `:484`, found by this session's grep for the same class. **One row-2
site is NOT fork residue and is left alone:** `:409` *"learning #22 / #26a"* is upstream's own 1.0.0
text — `git blame` → `df6a991` (KJ5HST, 2026-08-08), present in blob `be2721a5` — so the review had
attributed the maintainer's own citation to the port; scrubbing it would have edited his line under the
name of removing ours. Row 3, fork side: `docs/planning/pr4-candidate.context-budget.json` (17,934 →
17,893 B) — `read-set._` no longer cites `upstream-read-set-pr-plan.md`, a file the maintainer cannot
open (the sentence now says the seed's own `CLAUDE.md.max_bytes` is the candidate and that the
authoring fork's design names it), and the `CLAUDE.md` `_` key's *"Accepted as is (ratified
2026-09-03)"* becomes *"Left as is, deliberately"*. Verified in this worktree after the edits:
`python3 tools/test_context_budget.py` → exit 0, `Ran 116 … OK` (both `TestFitGateEndToEnd` rows run
here); `--selftest` → exit 0, 52 PASS / 0 FAIL, the relabelled check at `:1204` among them; the
candidate parses. The `"Phase B"` vocabulary upstream's trimmer (#77) still carries in nine comment
sites is untouched, as D9 left the trimmer's S-numbers — a consistency choice, made visibly.

**Second pass, after the review lens ran on the rebuilt branch (`46089f1`) and found the same class at
four more sites, each re-derived by hand before it was touched:** `starter-kit/context_budget.py` `:57`
(*"the repo that authors this tool"* → *"the authoring fork of this tool"*) and `:1157` (*"this
framework's own repository"* → the same), blob `0b103baf` → **`d91677b5`** (73,040 B, size and line count
unchanged); `tools/test_context_budget.py` `:214` (*"this framework's own repository: commit 7603f10"* →
*"the authoring fork: its commit 7603f10"* — a fork sha stated as this repository's) and `:404` (*"PHASE
B"* in capitals: the first pass's grep was case-sensitive), blob `f6c94d85` → **`04d6aaf6`**; the seed
`starter-kit/context-budget.json` `_read_cap_tokens` (*"On the project that authors this tool"* → the
fork where 1.2.0 was developed, named), 5,766 B. Same verification in this worktree: unit 116 OK,
`--selftest` 52 / 0, and a case-insensitive sweep of all three files for the class is empty.

### 2026-09-03 · [ad hoc] S148 — claim: the six-row fix-round on `pr4/context-budget-gate` (item (1) of S147's handoff)

**Authorization:** the operator's *"Item (1) of S147's handoff"*, given after the Phase 0 report: the
six-row decision table at [`docs/planning/pr4-read-set-budgets-body.md`](docs/planning/pr4-read-set-budgets-body.md)
`:23`, the fix-round S147's self-review recommended before Phase C. **The rewritten, re-measured, still
unpushed branch is the ONE deliverable:** row 2 first, as a fork commit on `main` (the tool's four
fork-relative comment sites), then the branch rebuilt on `cea3068` by the plan's §8 R1 recipe with rows
1, 3, 4, 5 and 6 applied inside it (row 3 also amends `pr4-candidate.context-budget.json`) and the
fork-vocabulary folds the table's *Kept as ratified* paragraph assigns to rows 2 and 3; every DONE-list
figure re-measured on the fresh tree; one review lens re-run; the plan's `c5ff15e5` criterion re-stated
with the new blob id. **No push, no PR, no `--calibrate`, no `install-hook` at the clone root, no
`bin/tests.sh` in this worktree, nothing outward-facing.** Phases C and D each keep their own go-ahead.

**Reconciled at claim:** S147's receipt `commit:` slot named its close-out by description; this commit
names it — `ae5ff8d`. Both ledger frontiers stood at `ae5ff8d` at Phase 0 (`git rev-list --count
--no-merges ae5ff8d..HEAD` → 0), so no backfill is owed and none is written.

**Ledger:** `CHANGELOG: pending` — set at claim; recorded at Phase 3F.

### 2026-09-03 · [ad hoc] S147 close-out — PR 4 BUILT (Phase B): `pr4/context-budget-gate` = `f3a4b6d` on `cea3068`, verified, NOT pushed

**Phase 3D/3F.** Deliverable: the built, verified, unpushed branch — Phase B of
[`docs/planning/pr4-read-set-budgets-plan.md`](docs/planning/pr4-read-set-budgets-plan.md) §5, executed as
ratified (D1–D11). Head `f3a4b6d` (tree `7541e3ee`), two commits on `cea3068` — `28406ce`
`feat(starter-kit): …` (the tool at blob `c5ff15e5`, the test module scrubbed on exactly four lines, the
9-line `bin/tests.sh` wiring, the seed's +6, the D8 ledger entry) and `f3a4b6d` `chore(budget): …` (the
root config byte-identical to the candidate, the seven `.gitignore` comment lines, one ledger bullet) —
built in a clean clone made only by the §8 R1 recipe (fixtures `020ba3f 7a71df0 e02881a e5cdc66` proved
unreachable, no `docs/archive/`), each commit **through** upstream's `.githooks/pre-commit` with
`core.hooksPath` set in the clone, and fetched into this fork as a **local ref only**.
`upstream/read-set-budgets` re-read at `cea3068` and the three pins re-read before the config was copied.
Body file: [`docs/planning/pr4-read-set-budgets-body.md`](docs/planning/pr4-read-set-budgets-body.md).
**Nothing pushed, nothing opened; Phases C and D still need their own go-aheads.**

**Commits this session, all recorded here:** `bfba325` (claim; also reconciled S146's `commit:` slot to
`a05e23a` + `a5fa2ae`); `8dc31e2` `chore(history)` for the two `.jsonl` series Phase 0 dirtied
(`--no-verify`, recorded by this line, committed *before* this close-out so nothing sits above the
frontier); this close-out (Learning #53, the plan's Phase B record, the body file, both ledgers).

**EVERY DONE-LIST FIGURE, TAKEN FROM THE TREE THAT WOULD BE PUSHED:** blob `c5ff15e5`, mode 100755; the
test module differs from `main:tools/test_context_budget.py` in exactly the four D9 lines (8, 288, 561,
613 — widths 95/97/97/97 under the module's 99-column norm); `python3 tools/test_context_budget.py` →
exit 0, `Ran 116 … OK (skipped=2)`; `--selftest` → 0, 52 PASS / 0 FAIL; the bare run → exit 2, 49 lines,
0 *defect*, six findings, `CHANGELOG.md` **96,750 B** (91,365 + 5,385 for the entry; ≈39,211 tok);
`--json` `config_defects: []`; the 13-case `--precommit` matrix reproduced (exits 2 0 2 2 0 2 0 2 0 0 0 0 0;
case 12's bare run 2 with `instrument-failed`); **by hand, each commit's index against its parent:
commit (1) vs `cea3068` with no config → exit 3; the same index with the candidate in the worktree → 2
(`91,365 -> 95,079 B`); commit (2) vs commit (1) → 2 (`95,079 -> 96,750 B`), and 0 with its bullet
unstaged** — the exits D4 ratified, measured again on the real commits; `bin/tests.sh` on a pristine
control **114 passed / 1 failed** vs **115 / 1** on a fresh clone of the head — 115 shared rows, exactly
one added (`context budget gate unit tests green`), zero flips, both failures Test 9 — and **114 / 2 at
commit (1) alone** (the wired row is red until the config lands; that commit's message says so);
`check-links` / `check-learnings` / `check-handoff` / `--all` 0/0/0/0; `git status --porcelain` empty
after deleting the history file; `git diff --stat cea3068 f3a4b6d` exactly seven files (2,315 / 98); the
identifier regex over the diff's added lines and over both commit messages prints nothing;
`grep -c PROPOSAL .context-budget.json` 8; the config `cmp`-identical to the candidate.

**THE FIX-ROUND DISCIPLINE RAN: two independent read-only reviewers on the frozen branch, each in its
own clone.** The plan-compliance lens re-derived every DONE item — all MET, no departures, three cosmetic
observations. The maintainer's-eye lens returned **twelve** items (3 HIGH, 4 MEDIUM, 5 LOW), and every one
re-derives by hand: the shipped tool blob says *"this repository's own SESSION_RUNNER.md is 54,363 B"*
(52,195 B on `cea3068`) and cites a fork planning file at `:683`; the test module still says *"Test 35"*
and *"bin/tests.sh:248-251"* at `:9`/`:13`, outside D9's four regex hits; the config's `read-set` `_` key
cites `upstream-read-set-pr-plan.md`, absent upstream; the ported `.gitignore` comment says a file *"is
tracked"* that upstream does not track; the ledger entry says *"PRs 1 and 3"* where upstream knows #76
and #78; two overstatements of my own in commit (1)'s message. **None repaired — each sits inside an
artifact the plan ratified (D9's four lines, Appendix A verbatim, the `c5ff15e5` blob, the §3.6 lines) —
so the six-row decision table, with proposed wording per row, is in the body file's header, and the
recommendation is a fix-round before Phase C.** The remaining items stand as ratified for the reasons the
table gives (the two machine-dependent tests, the fork-measured densities, the PROPOSAL count, the
rounding, the trailers).

**Learning #53** appended to `starter-kit/FRAMEWORK_LEARNINGS.md`: a per-clone hook is off in a fresh
clone of the target; enable it before the first commit, and let one refusal prove it binds.

**Adopter impact:** none yet — nothing has left this machine. When PR 4 merges and adopters sync, the two
changes the body discloses apply (bytes-not-lines rows when nothing fires; a derived token ceiling above
73,252 B). **Nothing outward-facing.**

**Model:** Claude Fable 5.1.

### 2026-09-03 · [ad hoc] S147 — claim: Phase B of the PR 4 plan — build `pr4/context-budget-gate` on `cea3068`, verify, do not push

**Authorization:** the operator's *"Item (1) of S146's handoff"*, given after the Phase 0 report:
[`docs/planning/pr4-read-set-budgets-plan.md`](docs/planning/pr4-read-set-budgets-plan.md) §5 Phase B
(`:599`), ratified at S146 (the §4 record, `:414`; D1–D11). **The built, verified, unpushed branch is the
ONE deliverable** — a clean clone made only by the §8 R1 recipe, fixture unreachability proved per clone;
two commits, each co-staging a `CHANGELOG.md` line (D4 as ratified); every DONE-list figure taken from the
tree that would be pushed; `docs/planning/pr4-read-set-budgets-body.md` written in the series' precedent.
**No push, no PR, no `--calibrate`, no `install-hook` at the clone root, no `bin/tests.sh` in this
worktree, nothing outward-facing.** Phases C and D each keep their own go-ahead.

**Reconciled at claim:** S146's receipt `commit:` slot named its last two commits by description; this
commit names them — `a05e23a` (close-out) and `a5fa2ae` (`chore(history)`, `--no-verify`). `a5fa2ae` was
the one commit above both ledger frontiers at Phase 0 (`git rev-list --count --no-merges a05e23a..HEAD`
→ 1); S146's close-out entry already records it, so no backfill entry is owed and none is written.

**Ledger:** `CHANGELOG: pending` — set at claim; recorded at Phase 3F.

### 2026-09-03 · [ad hoc] S146 close-out — the PR 4 plan RATIFIED (D1–D11), after the second review round ran

**Phase 3D/3F.** Deliverable: the ratified plan —
[`docs/planning/pr4-read-set-budgets-plan.md`](docs/planning/pr4-read-set-budgets-plan.md) (third draft,
91,883 B) and [`pr4-candidate.context-budget.json`](docs/planning/pr4-candidate.context-budget.json)
(17,934 B). **Status line and §4 now carry the ratification record: D1–D11 stand — D1–D10 as
recommended, D4 reshaped and D11 added on the second review's findings. Phase B is authorized as the
next session's single deliverable; Phases C and D are not.** Nothing built, pushed, or opened.

**Commits this session, all recorded here:** `a78e404` (claim; also reconciled S145's `commit:` slot);
`98c6e10` `[WIP]` third draft, frozen for self-review, and `c2b3106` `[WIP]` its repairs, frozen again for
one verifier — both committed `--no-verify`, both bypasses recorded by this line; this close-out; and a `chore(history)` for the two `.jsonl` series Phase 0 dirtied (`--no-verify`, recorded here).

**THE RATIFICATION, IN THE ORDER IT HAPPENED.** Item (1) of S145's `next_steps` was the operator's pick
(*"1"*). The ten recommendations and their alternatives were tabled as one question; the answer was *"All
ten as recommended."* Before recording it, the second adversarial review round S145 could not run (usage
limit) was run against the frozen close-out tree `67982cc`: **eight read-only slices, then one independent
skeptic per refutation and per HIGH/MEDIUM finding — 45 agents, 0 failed, 0 empty.** 120 claims
re-derived: **102 confirmed, 17 refuted, 1 unverifiable**; of round 1's 59 items **53 fixed, 5 partial,
1 not**; **19 new findings (1 HIGH, 9 MEDIUM, 9 LOW)**; **36 of 37 adjudications stand, 1 overturned.**
Four facts the repairs rest on were re-derived by hand rather than taken from an agent: upstream's
`.githooks/pre-commit` refuses a content commit without `CHANGELOG.md` co-staged; the fork carries **ten**
dashboard version labels above `2.10.7` (one agent said 9, another 10 — the enumeration settled it);
`claude --version` = 2.1.259; the two machine-dependent tests run and pass here (`Ran 116 … OK`). Four
items reopened a decision and went back to the operator as separate questions, each answered as
recommended: **D4** — the two-commit order's rationale was refuted (HIGH: by hand the gate exits **3** on
commit 1, no config yet, and would refuse commit 2's own ledger line; upstream's hook wants a ledger line
on every commit) → two commits, **each carrying a `CHANGELOG.md` line**; **D11**, new — the fork keeps its
own root config after merge; **D2**'s token arm — `CLAUDE.md` carries a silently clamped derived ceiling
(59,168 / 2.27 = 26,065 → 25,000; judged at 2.93 → 20,193, ok) → accept and document; **D6**'s residue —
the #77 ledger backfill is **not** in PR 4, and no frontier-based reconcile can ever surface it
(`56997af` sits below the frontier `2c30d0f`).

**WHAT THE REPAIRS CHANGED, BESIDES THE DECISIONS.** The zsh dragon said the mangled `$c:path` "silently
emptied" an enumeration — it is loud on stderr and `<sha>/` on stdout; dragon 11 blamed `grep -c` for a
SIGPIPE hazard that belongs to `grep -q`; §2.2's Lines column mixed `wc -l` with the tool's count (which
is one higher on every LF-terminated file); the adopter flip threshold is **73,253 B**, not "≥ 73,250"
(`int()` truncates, the compare is strict); D8's date rule was UTC where the ledger's convention is the
author's local date, its bullet shape was invented, and its identifier grep was unsatisfiable as written
(`CHANGELOG.md` and `bin/tests.sh` already carry 65 and 11 hits on `cea3068` → grep the added lines of the
diff); D9's "35 / 5" were line counts under a narrower regex (50 / 28 matches by D8's); D10's "three plus
a fourth" is four, plus two inherited thresholds now labelled (`warn_bytes` 51,000 is inert while the
class is over; `max_lines` 200); `class_totals()` is not called from `precommit()`; the dashboard cite was
`:508-523`, not `:498-508`; Phase A gained a runnable verification; Phase C regained the post-push
read-back the round-1 repair had dropped; the `calibrate()` failure causes and the FitGate diagnosis
command were wrong in detail; the PR body now says the bare run prints **five** red lines on day one,
that 2.27 is a constant not a key, what the trimmer does on its first `--write`, and that the gate this
PR ships would refuse the PR that ships it. Config: `_calibrate_against` added; `_bytes_per_token` now
names `CLAUDE.md` as the one consumer of the fallback; `_fixed_harness_tokens` says the tool reads it
nowhere; the `## Versioning` `why` no longer attributes a rule to a `CLAUDE.md` that does not state it
upstream (twelve `CHANGELOG.md` links and one fixture do the work).

**FIX-ROUND DISCIPLINE.** The third draft was frozen at `98c6e10` and given a four-lens self-review
(the S146 edits re-derived; a whole-plan contradiction sweep; the config prose run and read; the PR body
as the maintainer) with one skeptic per refutation — 17 agents, 4 lenses + 13 skeptics: 41 claims (36 confirmed, 5 refuted), 20 findings (2 HIGH, 6 MEDIUM, 12 LOW), all 13
adjudications standing — every one a defect in my own S146 edits, repaired in a third pass (`c2b3106`), whose 26 added
claims one more independent verifier then re-derived: 22 confirmed, 2 refuted (both in D11's merge arithmetic: 17
base conflicts, not 18, the draft having counted `merge-tree`'s OID line; PR 4's share two, not one), 2 unverifiable
from the tree — repaired in this close-out commit.

**Learnings #51 and #52** appended to `starter-kit/FRAMEWORK_LEARNINGS.md`: frontier-based reconcile is
blind to an omission a later ledger commit has buried; sequence commits around the check that actually
runs on the target, not the check the PR ships.

**Adopter impact:** none — fork-only planning documents and a canonical-only Learnings table. **Nothing
outward-facing.** The plan is 91,883 B and no longer fits one Read; a build session reads §4's
record, §5 Phase B, §3.3 and §8, not the whole file.

**Model:** Claude Fable 5.1.

### 2026-09-03 · [ad hoc] S146 — claim: ratification of the PR 4 plan's decisions D1–D10

**Authorization:** the operator's *"1"*, given after the Phase 0 report, selecting item (1) of S145's
`next_steps`: *"the operator ratifies or amends D1–D10"* (`docs/planning/pr4-read-set-budgets-plan.md`
§4, `:375-455`). **The ratified plan is the ONE deliverable** — each of the ten decisions answered by
the operator and recorded in the plan's status line and §4, in the shape
`docs/planning/read-cap-phase-c-plan.md:3` set at S115. Verification in service of it: the second
adversarial review round S145 could not run (every agent hit the usage limit) runs first, against the
frozen close-out tree `67982cc`, so the operator ratifies on checked premises. **No Phase B build, no
push, no PR, nothing outward-facing.** Phase B remains its own session; Phases C and D each keep their
own go-ahead.

**Ledger:** `CHANGELOG: pending` — set at claim; recorded at Phase 3F.

### 2026-09-03 · [ad hoc] S145 close-out — the PR 4 plan, delivered and adversarially reviewed

**Phase 3D/3F.** Deliverable: [`docs/planning/pr4-read-set-budgets-plan.md`](docs/planning/pr4-read-set-budgets-plan.md)
(67,657 B) and its companion [`pr4-candidate.context-budget.json`](docs/planning/pr4-candidate.context-budget.json)
(14,200 B) — the plan for the fourth and last read-set-budget PR, porting `starter-kit/context_budget.py`
(fork blob `c5ff15e5`, 73,014 B) and everything coupled to it onto `read-set-budgets` at `cea3068`.
**Planned, not built; nothing pushed, nothing opened.** Session began 2026-09-02 local; this entry is
dated by its commit.

**Commits this session, all recorded here:** `209dd51` (claim); `5394079` `[WIP]` draft 1, frozen for
review, committed `--no-verify`; `29054c7` `[WIP]` draft 2 after the review, `--no-verify`; `e13ceda`
`chore(history)` the two append-only `.jsonl` series dirtied by Phase 0, `--no-verify`; and this
close-out. The three bypasses are each recorded by this line, which is what the bypass rule requires.

**WHAT THE PLAN ESTABLISHED, MEASURED IN CLEAN CLONES OF `cea3068`.** (1) The file port is clean by
construction: upstream's blob `be2721a5` is the exact ancestor of the fork's seven linear commits; the
end-state patch and all seven per-commit patches apply. (2) The hard part is the coupling: the fork
tool **exits 3 without a root `.context-budget.json`**, upstream has none, and the distributed seed
dropped in as that config reads red for reasons unrelated to the series (`CLAUDE.md` 59,168 B vs
28,000). So PR 4 must ship a canonical root config, and the plan ships a candidate that was **run**:
exit 2 with `(read-set total) 67,581 B / 56,750 B over` — the 10,831 B the series exists to make
visible — 0 config defects, `--selftest` 52/0, the 116-test module OK (2 environment skips), a
13-case `--precommit` matrix (every over-or-pinned file refuses +2 B, every shrink passes, `structure`
is not evaluated by `--precommit`), and `bin/tests.sh` **115 passed / 1 failed against a control of
114 / 1** — 115 shared rows, one added, zero flips. (3) Under the unchanged seed an adopter sees two
changes on sync: read-mandated rows report bytes instead of lines when nothing fires, and a compliant
file at ≥ 73,250 B flips `ok` → `over`, exit 1 → 2 (Probe C4). (4) Ten operator decisions D1–D10 with
recommendations; Phases B–D with DONE, surface, and STOP each.

**THE RECORD CORRECTED.** Six receipts (S136, S140–S144) called this payload *"no clean starting
point"*; S144 glossed it *"the two versions diverged rather than one being a prefix of the other"*.
`git rev-parse` on the two blobs refutes the file half. The tree half is true.

**REVIEW.** Draft 1 was frozen at `5394079` and attacked by eight independent read-only agents — five
refuters over disjoint claim slices, three critique lenses: **97 claims confirmed, 28 refuted, 2
unverifiable, 32 findings.** Every refutation was re-derived before adoption. Refuted in my own work:
three per-commit mis-attributions (read from commit messages instead of path-restricted diffs); a
false *"hand-copied intermediate"* verdict on `vscode_quarto_ext`'s blob, caused by zsh parsing
`$c:path` as a history modifier (it is `6a91660`'s blob, six versions behind fork `main`); the trimmer
named as the declared ledgers' remedy when its trigger is 196,608 B, 3× the ceiling, and does not fire
at 91,365 or 70,182 B; a Probe C fixture holding one of the seed's three files, which could not
exhibit the changes it was published as not finding; the PR's own upstream ledger entry being a
commit the shipped gate refuses, which fixes the commit order (D4); the `FRAMEWORK_LEARNINGS.md`
row dropped on a false reason when its density was measured on the very blob upstream carries and
upstream's `bin/check-learnings:87-89` already cites the derivation (D7 reversed). **A second review
round was launched against `29054c7` and FAILED: all five agents hit the account's session usage
limit and returned null.** The repaired draft is therefore self-verified only (the round-2 claims I
had not re-derived were checked by hand: `calibrate()`'s too-few-sessions path, the upstream ledger
anchors at `:36`/`:144`, the dashboard's `:361`/`:498`/`:508` entries, `install_hook()`'s write path).

**Also at close-out:** reconciled S144's `commit:` answer slot to `710390b` (claim) + `8c701b5`
(close-out), each verified by reading that commit's own copy of the S144 block. Appended **Learning
#50** to `starter-kit/FRAMEWORK_LEARNINGS.md` (a true ratio carrying a false inference through six
receipts); `check-learnings` OK, 49 rows, 0 over 1,500 B.

**VERIFICATION AT CLOSE-OUT.** `bash bin/tests.sh` in this worktree, bare, after both ledger edits:
**304 passed / 1 failed / 0 skipped, exit 1** — the recorded baseline to the row. A first run before
the S144 `commit:` reconcile read 302 / 3 / 0; its two extra failures were that unreconciled slot (the
`L1` row and the 12,288 B edge case whose fixture is built from the live ledger) and both pass in the
second run. The one failure is Test 9, pre-existing. `check-handoff` 0, `--all` 0, `check-links` 0, `check-learnings` 0,
each read bare. **NO OUTWARD-FACING ACTION.** Phases C and D of the plan each require their own
go-ahead; approving the plan is not it.

**Model:** Claude Fable 5.1.

### 2026-09-03 · [ad hoc] The context-budget gate ships — ceilings in tokens, class totals, and the repairs beneath them

- **Change:** `starter-kit/context_budget.py` `1.0.0` → `1.2.0` (29,549 → 73,040 B), shipped as the
  end state of nine fork commits (seven that went through the fork's own review rounds, plus two
  comment-only rewords made for this port) rather than a replay — the tests arrive as one file, and
  every intermediate state of the tool before its reviewed end state fails them. Ceilings may now be declared in **tokens** (`max_tokens`, against `read_cap_tokens`
  25,000 — the number in the Read tool's own refusal message); a whole-read file with only `max_bytes`
  gets a ceiling derived at the 2.27 B/token floor and clamped at the cap; **class totals**
  (`resident`, `read-set`) are summed and gated in the bare run and in `--precommit`;
  `config_defects()` reports a declared `max_tokens` above the cap and a typed class total that
  disagrees with its derivation; `calibrate()` walks first-parent history, compares timezone-aware
  stamps and refuses a fit below R² 0.50 instead of printing noise; the index is sized with
  `git cat-file -s` (the old path was 1 B short on LF, more on CRLF, and raised on non-UTF-8 content);
  the ledger row names the ceiling that fired in its own unit and reports bytes, not lines, when
  nothing fired. Exit codes are unchanged (`0/1/2/3`), and so is the refusal to run at a root with no
  `.context-budget.json` (exit 3).
- **What it buys.** [#76](https://github.com/KJ5HST/methodology/pull/76) and
  [#78](https://github.com/KJ5HST/methodology/pull/78) shed bytes; this one **refuses growth**. On this branch the Phase 0
  mandatory pair is 52,195 + 15,386 = **67,581 B against the 56,750 B one-read cap — over by
  10,831 B, exactly what [#76](https://github.com/KJ5HST/methodology/pull/76)'s table left.** Nothing here shrinks it. Once a root config declares
  the pair, `--precommit` refuses any commit that grows either file and passes any that shrinks one.
- **The tests travel with the tool.** `tools/test_context_budget.py` — 116 tests, canonical-only
  (not in `bin/_manifest.py`, like the trimmer's), every git fixture a scratch repository — plus one
  `bin/tests.sh` row wiring it, immediately after the trimmer's. Until that row `calibrate()`'s
  arithmetic had no test anywhere: the existing `== Test: context_budget.py ==` block covers
  install-hook, sync distribution and the selftest gates, all of which stay green while the fit
  returns noise. Two tests fit this repository's own session transcripts against `CLAUDE.md` and
  **skip**, by design, on a machine without them.
- **The seed follows the tool.** `starter-kit/context-budget.json` gains `read_cap_tokens`, a
  `max_tokens` on each of its two whole-read entries and a note on the on-demand entry saying why it
  gets none (+6 lines) — documentation of keys the new tool reads. It is a seed-once file: no
  adopter's existing config changes on sync.
- **Scanner:** untouched. Both dashboard twins already list `context_budget.py` and
  `.context-budget.json` as framework-installed files and score neither.
- **Verification:** clean clone of `cea3068`, measured at the branch head with the root config in
  place. `python3 tools/test_context_budget.py` — 116 run, OK, 2 skipped; `--selftest` 52 PASS /
  0 FAIL; `bin/tests.sh` **115 passed / 1 failed** against **114 / 1** on the untouched base — one
  row added, zero status flips; the failure on both is Test 9 (`bin/sync --source=github` reads
  `main`, where three manifest sources are absent until this branch merges). `bin/check-links`,
  `bin/check-learnings`, `bin/check-handoff` and `bin/check-handoff --all` each 0.
- **Provenance:** ported from `rmsharp/methodology` `main` — the tool byte-identical (blob
  `d91677b5`), the test module differing in six lines: four where a fork-relative identifier became
  the date of the change, two where a reference to the fork's numbered `bin/tests.sh` block became a
  description of this tree's. The fork's own root config, its measurement history, its dashboard
  series and its ledgers are **deliberately excluded**.
- **This repository declares its own budget** — a root `.context-budget.json`, in a second commit so
  the policy file is reviewable apart from the code. It **pins** `CLAUDE.md` at its arrival size
  (59,168 B: growth refused, shrink passes), **derives** the `read-set` total from the read cap at run
  time (25,000 tok × 2.27 B/tok = 56,750 B) and splits it 41,364 / 15,386 across `SESSION_RUNNER.md`
  / `SAFEGUARDS.md`, so all 10,831 B of debt sits on the file the series wants shrunk, and
  **declares** the two ledgers Phase 0 reads at 65,536 B and 25,000 tokens each and
  `FRAMEWORK_LEARNINGS.md` at 73,728 B — the derivation `bin/check-learnings` already cites this
  file for. Every number's `_` key says how it was derived; five values are marked PROPOSAL, and the
  calibration constants are the seed's (`--calibrate` proposes and writes nothing). Day one: the bare
  run exits 2 with six findings — `SESSION_RUNNER.md` and the pair over by 10,831 B, both ledgers over
  in bytes and in tokens — none of them new. This file is also what turns the wired `bin/tests.sh`
  row green: without a root config the tool exits 3 and the unit module's selftest test fails. The
  gate is **not wired** into `.githooks/pre-commit`: run `--precommit` by hand, and never
  `install-hook` at this root (the config's `_` key says why). Run by hand, this PR's own two commits
  fail it — exit 3 on the first (no config yet), exit 2 on this one (this bullet grows a ledger
  already over its ceiling). `.gitignore` gains the comments explaining why neither measurement history
  (the dashboard's, this tool's) is ignored; this tool's appears on the first bare run and is yours to
  track or not.

### 2026-09-02 · [ad hoc] S145 — claim: planning session for PR 4 (`starter-kit/context_budget.py` to `read-set-budgets`)

**Authorization:** the operator's *"PR 4 planning session"*, given after the Phase 0 report. The
predecessor (S144) scoped PR 4 to its own session and named a planning session as the expected first
step for this shape — a divergent file with no single commit to port — and the operator chose exactly
that. **The plan is the ONE deliverable** (`SESSION_RUNNER.md` Phase 2 §Planning Sessions; FM #18): no
port branch is built, no PR is opened, nothing outward-facing happens this session.

**Scope of the plan:** `starter-kit/context_budget.py` (fork `main` **73,014 B / 1,400 lines**;
`upstream/read-set-budgets` **29,549 B / 674 lines**, byte-identical to `upstream/main`), the seven fork
commits on that path since `14bd88a`, and every file coupled to it — `tools/test_context_budget.py`,
`.context-budget.json`, `bin/tests.sh`, `bin/_manifest.py`, and the prose that names it. Base is
**`cea3068`**, the tip of `read-set-budgets` after PR #78; nothing else is in flight, so no stacking.

**Ledger:** `CHANGELOG: pending` — set at claim; recorded at Phase 3F.

### 2026-09-02 · [ad hoc] S144 — OUTWARD-FACING ACTION TAKEN: **PR [#78](https://github.com/KJ5HST/methodology/pull/78) MERGED** into `read-set-budgets`

**Recorded here because a merge on `KJ5HST/methodology` leaves no commit in this repository.** Phase 0
reconcile is structurally blind to it; the failure-mode-#27 write-gate is the only mechanism that
records it.

**Authorization:** the operator's *"merge PR #78"*, scope narrowed by their own follow-up to the merge
alone. **`gh pr merge` printed NOTHING**, which is neither success nor failure — every property below
was read back from the server afterwards.

| Property | Value |
|---|---|
| #78 | **MERGED** 2026-09-03T02:04:28Z, merge commit **`cea3068`** |
| `read-set-budgets` | `907a696` → **`cea3068`**, parents `[907a696, 2c30d0f]` — a merge commit, matching #76 and #77 |
| `upstream/main` | **untouched at `512c2ed`** |
| Open PRs | **none** |

**The merge was checked for what it DELIVERED, not merely that it succeeded.** `tree(cea3068)` is
**identical** to `tree(2c30d0f)` — the merge added nothing and lost nothing. On `read-set-budgets`
now: `FRAMEWORK_APPARATUS.md` **present at 15,493 B**, `ITERATIVE_METHODOLOGY.md` **55,976 B**,
manifest **27 rows**.

**Three of four PRs in the read-set-budget series are now in.** `main` has received none of them and
is not a target yet.

**Also at close-out:** reconciled S143's `commit:` answer slot to `29331e5` (claim) + `601e432`
(close-out), each verified by reading that commit's own copy of the S143 block — `29331e5` holds it
`status: pending`, `601e432` holds it `status: complete`. **`check-handoff` also caught this receipt's
own `key_files` carrying no `path:line` token**, which the spec requires; fixed with three real
anchors rather than by loosening the sentence. Both read **0** bare afterwards.

### 2026-09-02 · [ad hoc] S144 — claim: merge PR [#78](https://github.com/KJ5HST/methodology/pull/78) into `read-set-budgets`

**Authorization:** the operator's *"merge PR #78"*, with the scope narrowed by their follow-up —
*"we will start PR 4 in the next session"* — so this session's ONE deliverable is the merge. PR 4 is
explicitly **not** in scope.

**Recorded before the action, because a merge on `KJ5HST/methodology` leaves no commit in this
repository.** Phase 0 reconcile cannot see it; the failure-mode-#27 write-gate is the only mechanism
that records it.

**Pre-merge state, read from the server:** `gh pr view 78` -> **OPEN**, base **`read-set-budgets`**,
`mergeable` **MERGEABLE**, `mergeStateStatus` **CLEAN**.

**Method: a merge commit, matching this series' precedent** — `46b56fd` (#76) and `907a696` (#77) each
have two parents. Consistency matters here because PR 4 will be built on whatever tree this creates,
and a squash would give that tree a new sha with no ancestry link to `2c30d0f`.

**Ledger:** `CHANGELOG: pending` — set at claim; recorded at Phase 3F.
### 2026-09-02 · [ad hoc] S143 — OUTWARD-FACING ACTIONS TAKEN: branch pushed, **PR [#78](https://github.com/KJ5HST/methodology/pull/78) OPENED**

**Recorded here because neither action leaves a commit in this repository.** A push to `origin` and a
pull request on `KJ5HST/methodology` are both invisible to Phase 0 reconcile; the failure-mode-#27
write-gate is the only mechanism that records them.

**Authorization:** the operator's *"Open it, 3 commits as-is"*, given after reviewing the pre-flight,
together with the decision that the trimmer-documentation gap becomes **a separate small PR later** —
so it was deliberately not folded in.

**Every property verified from the server, never from the command's own output.** `gh pr create`
prints the same URL whatever base it used; `gh pr view --json baseRefName` is what proves the base,
and `git ls-remote` rather than the push transcript is what proves the push.

| Property | Value |
|---|---|
| State | **OPEN**, `MERGEABLE` |
| Base | **`read-set-budgets`** — the operator's standing requirement that this never target `main` |
| Head | `rmsharp:pr3/apparatus-extraction` = `2c30d0f`, confirmed on `origin` by `git ls-remote` |
| Size | **12 files, +426 / −348**, matching the local measurement exactly |
| Commits | **3** — `786aa24`, `2897983`, `2c30d0f`; no squash, per the operator's choice |
| `upstream/main` | **untouched at `512c2ed`** |
| `read-set-budgets` | still `907a696` — **a pull request does not advance its base** |

**No re-measurement was owed and none was invented.** `tree(907a696)` — the base created when #77
merged — is **identical** to `tree(56997af)`, the tree S142 built and measured PR 3 on. The suite was
therefore not re-run: it would have measured the same tree.

### 2026-09-02 · [ad hoc] S143 — claim: push `pr3/apparatus-extraction` and open PR 3 against `read-set-budgets`

**Authorization:** the operator's *"Open it, 3 commits as-is"*, given after being shown the verified
pre-flight — base advanced, no rebase needed, `merge-tree` clean, three commits.

**Recorded before the action, because neither a push nor a pull request leaves a commit in this
repository.** Phase 0 reconcile is structurally blind to both; the failure-mode-#27 write-gate is the
only mechanism that records them.

**Pre-flight, re-run against the ADVANCED base and read from the server, not from a handoff:**
`gh pr view 77` -> **MERGED** 2026-09-03T01:38:22Z, merge commit `907a696`; `read-set-budgets`
`46b56fd` -> **`907a696`**; `upstream/main` **unchanged at `512c2ed`**. **`tree(907a696)` is identical
to `tree(56997af)`** — the new base is byte-for-byte the tree PR 3 was built and measured on, so
S142's verification carries over rather than needing a re-run. **0 conflicts** (`merge-tree` exit 0),
**3 ahead / 1 behind**, the 1 being the merge commit itself, which changes no content.

**Scope of this session: the push and the PR open, nothing else.** The trimmer-documentation gap
merged by #77 is deliberately NOT folded in — operator chose a separate small PR later.

**Ledger:** `CHANGELOG: pending` — set at claim; recorded at Phase 3F.
### 2026-09-02 · [ad hoc] S142 close-out — PR 3 built and verified on a stacked base; 3 self-inflicted defects found by review and fixed

**Deliverable: branch `pr3/apparatus-extraction` = `2c30d0f`, 3 commits, 12 files, +426/−348.**
**NOT PUSHED. PR 3 NOT OPENED.** Body prepared at `docs/planning/pr3-read-set-budgets-body.md`.

**The assigned base did not exist.** S141 assigned PR 3 "on the ADVANCED base once #77 merges";
`gh pr view 77` says **OPEN**, so `read-set-budgets` is still `46b56fd`, which carries no
`starter-kit/methodology_trim.py` — and PR 3 touches the dashboard twins, whose canonical-only tests
abort with 13 errors without it. Stacked on `pr2/ledger-trimmer` (`56997af`) instead: the exact tree
#77 proposes, so the branch retargets on merge with no rebase.

**Two large blocks `git` offered as conflict resolutions were dropped, not force-fitted.**
`collect_trim_metrics()` (11,834 B, both twins) and README's `## What It Costs` (14,429 B) exist in
the fork and not on this base; the originating commits edited text *inside* each, so a 3-way merge
presented the whole block as an addition. Importing either would have smuggled a fork feature in
under the guise of resolving a comment edit.

**Ported counts were re-derived, and the manifest row SET diffed** — 27 rows / 23 markdown / 19
tracked-markdown, and **0 rows differing either way** against `e02881a`, so the agreement is
structural rather than a coincidence of equal totals.

**Two fork-relative session numbers were removed.** The port would have written *"Extracted at S130"*
into `CLAUDE.md` and *"since S130"* into `HOW_TO_USE.md`. `git grep -oE '\bS[0-9]{1,3}\b' -- '*.md'`
returns **nothing** on this base, so these would have been the first two — each naming a session in a
different repository's counter.

**Verified in `git clone --no-local --single-branch`, never a worktree.** Base 114/1, branch 114/1,
diffed **row for row: 113 shared labels, zero status flips**; the only two differing rows are the
manifest counters, passing on both sides. Dashboard suite **211 OK**, trimmer suite **exit 0**, the
three checkers **0/0/0** read bare. End to end: a real `bin/sync` into a scratch repo lands the
sibling, and in that installed layout **14 references resolve, 7 fragments, 0 unresolved**.

**ADVERSARIAL REVIEW OF MY OWN WORK: 6 lenses → 25 findings → 3 skeptics each → 9 confirmed,
collapsing to 3 real defects, all mine, all fixed (`2c30d0f`) and re-verified.**
(1) I updated the `22 → 23` markdown count only where the patch touched it, leaving `README.md:138`
and `tools/test_methodology_dashboard.py:2853` stale — **while my own ledger entry claimed the counts
had been re-derived from the manifest**, a false claim that had already shipped into a commit.
Classified against the **pre-change** tree: both read 22 and were correct on base, so both were mine.
(2) The distributed stub's *"every point of need above links onward"* enumerated 9 of the 13 sites
that actually link, and contradicted this branch's own ledger entry. Settled by measuring the base —
5 sites already pointed in prose, 8 gained a pointer, 1 had a bare parenthetical converted — so
"nine added" was right and the stub's list was wrong. (3) Fixing (2) edited the file whose size I had
published, so **55,895 → 55,976 B** and every derived figure moved.

**Reported, not fixed — two pre-existing defects with no author here.** Both dashboard twins (`:185`)
and `docs/tutorials/T8_keeping_current.md:183` say *"25 distributed sources/files"* where the manifest
holds **26** on the base and **27** here: wrong before this change and after it.

**Also this session:** `ef51dc9` reconciled S141's `commit:` answer slot to `72b9b54` + `4329d33`
(the checker went 0 → 1 the moment a newer receipt was prepended); `e0adcec` repaired that commit's
missing ledger line; `1949a83` committed the two append-only measurement series.

### 2026-09-02 · [ad hoc] S142 — claim: build PR 3 (apparatus extraction) STACKED on `pr2/ledger-trimmer`

**Deliverable:** the PR-3 branch for `docs/planning/upstream-read-set-pr-plan.md` §5 — the port of the
S130 apparatus extraction (`e02881a`) to an upstream-like tree. **No outward-facing action.** The
branch is built and verified locally; opening PR 3 needs its own operator go-ahead.

**Why stacked rather than on `46b56fd`.** S141's handoff assigned PR 3 "on the ADVANCED base once #77
merges". [PR #77](https://github.com/KJ5HST/methodology/pull/77) is **still OPEN** (verified from the
server this session), so `read-set-budgets` is still `46b56fd`, which carries **no**
`starter-kit/methodology_trim.py`. PR 3 touches the dashboard twins, whose canonical-only tests abort
with **13 errors** without the trimmer present. Building on `46b56fd` is therefore not available;
stacking on `pr2/ledger-trimmer` (`56997af`, the exact tree #77 proposes) is the same base #77 will
create on merge, so the branch retargets cleanly.

**Also at claim, and it is a separate action with its own commit `ef51dc9`: reconciled S141's
`commit:` answer slot.** `bin/check-handoff --allow-pending` went **0 -> 1** the moment this session's
receipt was prepended — a slot reading `the S141 claim + this close-out` is legal only while that
receipt is newest, and the spec (`starter-kit/HANDOFFS.md:64`, `:78-79`) makes the next session
resolve it. Set to `72b9b54` (claim) + `4329d33` (close-out), each verified by reading **that commit's
own copy of the S141 block** rather than inferred from subject lines: `72b9b54` holds it
`status: pending`, `4329d33` holds it `status: complete`. Checker back to **0**, read bare.

**`ef51dc9` reached history with no ledger line, and this entry is the repair.** The edit that should
have added it aborted on its own uniqueness assertion — the `**Ledger:** ... set at claim` boilerplate
occurs **3** times in this file, not once — but the `git commit` on the following line was never
chained to it and ran anyway. `.githooks/pre-commit` did not stop it: `git add CHANGELOG.md` on an
**unmodified** file stages nothing, so the co-staging test saw no ledger change to demand. **A
co-staging gate keyed on the path being staged cannot distinguish "ledger updated" from "ledger
mentioned",** which is exactly the reflex §6 dragon 2 of `docs/planning/upstream-read-set-pr-plan.md`
warns the derived-value checks would inherit.

**Ledger:** `CHANGELOG: pending` — set at claim; this session's actions are recorded here at Phase 3F.

### 2026-09-02 · [ad hoc] S141 — OUTWARD-FACING ACTIONS TAKEN: head branch pushed, **PR [#77](https://github.com/KJ5HST/methodology/pull/77) OPENED**

**Recorded here because neither action leaves a commit in this repository.** A push to `origin` and a
pull request on `KJ5HST/methodology` are both invisible to Phase 0 reconcile; failure mode #27's
write-gate is the only mechanism that records them.

**Authorization:** the operator's *"re-run the two HEAD-dependent pre-flight checks, push, and open it
with `--base read-set-budgets`"* — the pre-flight, the push and the base all named explicitly.

**Verified from the server, not from the commands' output** (`gh pr view 77`):

| Property | Value |
|---|---|
| State | **OPEN**, `MERGEABLE` |
| **Base** | **`read-set-budgets`** — never `main` |
| Head | `rmsharp:pr2/ledger-trimmer` (`56997af`, confirmed by `git ls-remote`) |
| Diff | 9 files, **+4,691 / −6**, **1 commit** |

**`main` is untouched at `512c2ed4` and remains the default branch**; `read-set-budgets` is still
`46b56fdb`, since opening a PR does not advance its base. `gh pr list` shows exactly one open PR.

**One step the operator did not name, disclosed in the claim before it was taken.** The branch carried
three WIP commits — two labelled *"WIP"*, one literally *"NOT ready to open"* — which would have
misdescribed the work to its reviewer. They were squashed into a single authored commit, and **the
tree was proved unchanged by comparing `HEAD^{tree}` against `81eedb0^{tree}`** rather than assumed:
a rebase that quietly drops a hunk looks exactly like a tidy history. Pre-flight was then re-run,
because the squash changed the very thing the first run had measured.

**The staging design is holding.** Two PRs have now landed on a branch created for selective developer
testing, and `main` has not moved once: `512c2ed4` before #76, before #77, and now.

**Not authorized, not done:** no merge, no comment on #75, #76 or #77, no tag, no release. **PRs 3–4
(apparatus, gate) stay unopened.** PR 3 is now unblocked — the ordering was measured, not assumed: the
dashboard's canonical-only tests abort with 13 errors without the trimmer present and 0 with it — and
it must be built on the **advanced** base once #77 merges, not on `46b56fd`.

- **Model:** Claude Opus 5 (1M context).

### 2026-09-02 · [ad hoc] S141 — claim: push `pr2/ledger-trimmer` and open PR 2 against `read-set-budgets`

**Ledger:** `CHANGELOG: pending` — set at claim; the actions are recorded here at Phase 3F.

**Operator authorized exactly this**, naming the pre-flight, the push and the base. Pre-flight re-run
at claim because both checks are HEAD-dependent: base `46b56fd`, branch **0 behind / 3 ahead**,
`git merge-tree --write-tree` **exit 0**, 9 files **+4,691 / −6**.

**One preparation step the operator did not name, taken and recorded rather than done silently:** the
branch's three commits are this arc's WIP steps, two labelled *"WIP"* and one literally *"NOT ready
to open"*. Shipping those into a pull request would misdescribe the work to its reviewer. They are
squashed into a single authored commit before the push — **the tree is unchanged**, only the history
is presentable, and that is verified by diffing the squashed tree against `81eedb0`.

**⚠ Crash note: a pull request leaves no commit in this repository.** If this entry is the frontier
with no close-out after it, run `gh pr list --repo KJ5HST/methodology --state all` before concluding
nothing shipped (failure mode #27).

**Not authorized, not done:** no merge, no comment on #75 or #76, no tag, no release; PRs 3–4 stay
unopened.

- **Model:** Claude Opus 5 (1M context).

### 2026-09-02 · [ad hoc] S140 close-out — option (C) delivered: PR 2 is green, 19 failures to zero added

**Deliverable:** `pr2/ledger-trimmer` = **`81eedb0`** plus
[`docs/planning/pr2-read-set-budgets-body.md`](docs/planning/pr2-read-set-budgets-body.md).
**PR 2 is ready to open and was NOT opened** — see the close-out receipt's `next_steps` (1).

**Measured in a clone where `020ba3f` and `7a71df0` are unreachable and `docs/archive/` is absent** —
never a worktree, which is the error that gave S138 and S139 two wrong counts:

| | Result |
|---|---|
| Base (`read-set-budgets` @ `46b56fd`) | 113 passed, 1 failed |
| **PR 2** | **114 passed, 1 failed** |
| **Delta** | **+1 passing row, ZERO added failures** |
| `tools/test_methodology_trim.py` alone | **123 tests, exit 0**, 2 skipped *(was 19 failures)* |
| `tools/test_methodology_dashboard.py` | **211 tests, exit 0** |

The one failure is the Test 9 #76 already declared: `bin/sync` reads `main`, and this branch's newest
manifest rows name files not yet there. It heals on merge to `main`.

**THE FIXTURES REPRODUCE STRUCTURE, NOT BYTES.** `SYNTHETIC_CHANGELOG` — front matter, records, and a
non-empty footer carrying a **rebasable `](link)`**, which is load-bearing: without one the
footer-moved clause is only ever tested verbatim and the `transform_record` path goes uncovered. And
a **25 = 6 + 19** partition with one **retained** record edited — precisely the property that made
`7a71df0` the event worth testing against.

**THE AUTHORS' OBJECTION — *"a synthetic one tests the test"* — IS ANSWERED EMPIRICALLY.** Three
mutants of the code under test were disabled in turn and each was **killed**:

| Mutant | Tests failing |
|---|---|
| `L2_FOOTER_MOVED` never emitted | **6** |
| `L3_RECORD_ALTERED` never emitted | **4** |
| `L1_MISMATCH` never emitted | **5** |

The source was restored byte-identically afterwards (`cmp` clean) and the baseline re-confirmed at
exit 0. **Without that evidence the conversion would be indistinguishable from deleting 19 tests.**

**Nothing was dropped to get green.** The three fixture controls were *rewritten*, keeping the
insight that a whole-file grep cannot distinguish *"the footer is present"* from *"a record merely
quotes it"* — the reason zones exist at all. And the two declared-regenerated-field tests **keep
their real artifacts and skip**: their point is that the live count really drifted by hand, so a
synthetic anchor there would test the test. Their precondition is read from the raw file, never
through `classify_zones`, which is the code under test.

**PR 3 (apparatus extraction) is now unblocked** — the coupling was measured, not assumed: the
dashboard's canonical-only tests abort with 13 errors without the trimmer present and 0 with it.

- **Model:** Claude Opus 5 (1M context).

