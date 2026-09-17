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

**Archived 65 record(s), 2026-09-02 → 2026-09-14** into [`docs/archive/CHANGELOG-through-2026-09-14.md`](docs/archive/CHANGELOG-through-2026-09-14.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-09-14.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-14.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

---

## 2026-09

### 2026-09-16 · [BL-57] S178 — D10: the pre-commit hook's Phase 1B claim carve-out and its Test 27 are removed (operator decision)

- **Decision (operator, S178, picker, after a plain-language explanation):** remove the carve-out. It was
  added at S32 (`a56dff8`, 2026-08-03), when claims wrote no ledger entry and every claim shipped with
  `--no-verify`. 61 claims used it, the last S95 (`a35a14f`, 2026-08-17); all 94 claims since carry an
  *(in progress)* entry, which Q4 A (S162) makes the rule. Upstream's hook never had it.
- **Change:** `.githooks/pre-commit` is now byte-identical to `bl57/changelog-rules`' hook (blob `a2457774`):
  the carve-out, its `--no-renames` (which only guarded the carve-out) and the refusal text's exemption
  paragraph go. `bin/tests.sh` Test 27 (508 lines, 34 rows) is replaced by a three-line comment; nothing
  outside it used its helpers. Canonical-only: no adopter receives the hook.
- **Shown in a scratch repository with a real `git commit`:** a claim commit staging only `HANDOFFS.md` exits 1
  with *"failure mode #27"* under the new hook and 0 under the old one; with a `CHANGELOG.md` entry
  co-staged it exits 0 under both.
- **Owed next, in its own commit:** the suite loses 34 rows, so `tests-sh-passed` (327) must come down to the
  measured count, on the same operator approval.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S178 — a fork-only dashboard test read the live `CHANGELOG.md` seed's fenced examples, which P1 moved; it reads the frozen format-1 seed now

- **Change:** `tools/test_methodology_dashboard.py` `test_fenced_records_are_not_counted` (`TestS38TrimTriggerRow`,
  fork-only). Its fixture control asserted that `starter-kit/CHANGELOG.md` holds fenced dated headings; the
  ledger-format-2 seed holds none, so the merge below failed Test 18 with *"0 not greater than 0"*. This is the
  plan's hazard 6 in a test the branch never had. The control now reads
  `tools/fixtures/seed-CHANGELOG-ledger-format-1.md` with its blob id asserted, as
  `tools/test_methodology_trim.py` does, and the live thin seed is asserted to hold 0 records.
- **Verified:** the dashboard suite runs 336 tests, OK. A fence-blind record-counter mutant fails the test.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S178 — P5: fork `main` merges `bl57/changelog-rules` (`83a12f0`), adopting the one-home `CHANGELOG.md` rules (merge `22ce71b`)

- **Operator decisions (S178, picker):** merge the branch rather than port it (plan §P5 wrote a port), so the
  branch's P1–P4 commits enter fork history and the resync after the upstream PR merges does not re-resolve
  them (#80 and #82 were merged upstream as real merge commits). And D10: remove the hook's claim carve-out,
  including lowering the `tests-sh-passed` floor once Test 27 goes; both come in later commits.
- **The merge** (base `64f23bf`; the branch's net change is 16 files): 5 conflicts, 9 hunks, as
  `git merge-tree` predicted. `CHANGELOG.md` ours (the branch's file is upstream's ledger, and its BL-57
  entries record work this ledger already records); `bin/_manifest.py` and `bin/tests.sh` theirs (the fork's
  S41 marker design, which BL-57 replaces for `CHANGELOG.md`); `CLAUDE.md` the fork's row naming the ledger
  rules; `starter-kit/SESSION_RUNNER.md` the branch's Phase 3F bullet plus the fork's `Model:` sentence,
  re-pointed from the seed's format section to `FRAMEWORK_APPARATUS.md` §The Action Ledger (runner −14 B).
- **Checked on the merge:** the 8 files identical between `main` and the base equal the branch's blobs; in the
  8 files where `main` differs from the base, and in both ledgers and the budget config, the differences
  from the branch are exactly the fork's own changes plus the resolutions above (a line-multiset comparison). Suite in a `--no-local` clone: 332 passed / 2 failed / 0
  skipped against the parent's 332 / 1 / 0. The row diff is Test 20 (b2) swapped for the branch's
  frozen-seed pair (+1) and Test 18 failing (fixed above). Test 9 fails on both from GitHub API rate limiting.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S178 claim — P5 of the `CHANGELOG.md` rules plan: fork `main` adopts the one-home rules (in progress)

**Deliverable:** P5 of [`docs/planning/changelog-rules-contradictions-plan.md`](docs/planning/changelog-rules-contradictions-plan.md)
(§P5, with the S173 block overriding its port command): bring BL-57's own change from branch
`bl57/changelog-rules` (`83a12f0`) onto fork `main`, including this repo's own ledger front matter and the
D10 decision on the pre-commit hook's claim carve-out. Chosen by the operator after Phase 0 (picker).

- **Pre-flight, re-derived at Phase 0:** `upstream/main` is still `6b29d3d`, 0 commits ahead of fork `main`;
  PR #83 is still open at `219fb9d`. `git merge-tree --write-tree --name-only main bl57/changelog-rules`
  lists 5 files (`CHANGELOG.md`, `CLAUDE.md`, `bin/_manifest.py`, `bin/tests.sh`,
  `starter-kit/SESSION_RUNNER.md`), the set S177 computed. Merge vs port is measured before choosing.
- Phase 0 ledger reconcile: `CHANGELOG.md` and `HANDOFFS.md` frontiers both at `HEAD` `fc4fe0c`, no gap,
  nothing backfilled. 2 receipts, so no Phase 0 trim. S177's gate citation re-run in a `--no-local` clone of
  `fc4fe0c`: `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results db4e547cc884 · manifest
  c09d7e7f9109`, identical to the receipt. Dashboard 76/100, medium risk. `context_budget.py --status`
  exit 2 with the rows S177 recorded (runner 55,420 B, `SAFEGUARDS.md` 17,024 B, read-set total 72,444 B).
  `methodology_trim.py --file CHANGELOG.md --check` fires at 251,064 B; not trimmed, by the operator's
  standing decision. The two Phase 0 instrument snapshots ride with this claim.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] S178 — fork `main` pushed to `origin`, `c857e50..fc4fe0c` (non-commit action, operator go-ahead)

- **Action:** `git push origin fc4fe0c:refs/heads/main`, `c857e50..fc4fe0c`, a fast-forward of 1 commit: `fc4fe0c`
  (S177's receipt updated with what followed its close-out). Before the push, a guard confirmed a clean tree, that
  `origin/main` still read `c857e50`, and that exactly that one commit was ahead in a fast-forward. Afterwards
  `git ls-remote origin refs/heads/main` read `fc4fe0c07a0ecdcf4dc691013ba53c100908927e`. The go-ahead was the
  operator's S178 Phase 0 picker answer *"Push it now"*. Fork only; nothing sent upstream.
- **This recording commit is pushed too**, under the standing push-record grant, so it records its own push.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] S177 follow-up — the S177 receipt's next steps updated for what happened after close-out

- `HANDOFFS.md`, S177's receipt only. `next_steps` items (2) and (3) are replaced by their outcomes: fork `main` was
  pushed (`9b96ac1..7b55ee3`, `7b55ee3..70265f3`, then `c857e50` under the push-record grant), and the upstream
  test finding is BL-62, riding BL-57's P12 PR. Gotcha (7) carries the ledger's size at this update and the
  grant is named. Item (1)'s P5 conflict set was recomputed against `c857e50`: still the same 5 files. The same
  edit was made after S175's close-out (its receipt opens `next_steps` with the operator's later decision).
- Prepared for a new session: tree clean, `main` level with `origin`, 0 commits behind `upstream/main`
  (`6b29d3d`), PR #83 still open at `219fb9d`, 2 receipts (the next claim makes 3, no Phase 0 trim).
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] Operator decision: push records are pushed to `origin` without asking (standing grant)

- **Decision (operator, after S177, in their own words):** *"yes, push the push records without asking"*.
- **Scope, and nothing wider:** a commit whose only change is the `CHANGELOG.md` entry recording a push the operator
  already authorized goes to fork `origin` `main` without a separate ask. It must be a guarded fast-forward, read
  back with `git ls-remote`. Such a commit records its own push in that same entry, so no further record is owed
  and the chain ends there. Every other push still needs its own go-ahead, and so does every upstream action.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] S177 follow-up — fork `main` pushed to `origin`, `7b55ee3..70265f3` (non-commit action, operator go-ahead)

- **Action:** `git push origin 70265f3:refs/heads/main`, `7b55ee3..70265f3`, a fast-forward of 2 commits: `80f0eef`
  (the record of the previous push) and `70265f3` (BL-62). Before the push, a guard confirmed a clean tree, that
  `origin/main` still read `7b55ee3`, and that exactly those two commits were ahead in a fast-forward. Afterwards
  `git ls-remote origin refs/heads/main` read `70265f390acfd3c5cdb2c762feb573677fb0fc14`. The go-ahead was the
  operator's *"push the two local commits to origin"*. Fork only; nothing sent upstream.
- **This recording commit is pushed too**, under the standing grant recorded in the entry above.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-62] S177 follow-up — BL-62 raised: upstream's partition test sums every whole-read class as one Read; it rides BL-57's P12 PR (operator decision)

- **Raised on the operator's request** after S177's explanation. **Decision (operator): carry it in BL-57's P12 pull
  request, not as a standalone upstream issue.** `tools/test_context_budget.py:1256`
  (`test_whole_read_class_token_ceilings_partition_the_read_cap`, upstream `008d656`) applies the one-Read token
  sum to every class in `WHOLE_READ_CLASSES`, where only the read-set pair is read together. It fired at resync
  M2 against the fork's two read-mandated ledgers and was worked around at `0e8c6ac`.
- **Checked before writing:** no existing backlog item covers it (the test name and *"whole-read class"* grep
  empty in `BACKLOG.md` and `BACKLOG-DETAIL.md`). Upstream's root config gives token ceilings only to its
  read-set pair and one resident file, so upstream cannot see it. No test file has a `bin/_manifest.py` row,
  so no adopter is affected.
- **Files:** `docs/planning/BACKLOG-DETAIL.md` gains `#bl-62` (the proof `BACKLOG-DETAIL.md.verify.sh` still
  exits 0); `docs/planning/BACKLOG.md` gains its index row, the open list gains BL-62, and the BL-57 row says
  P12 carries it. Nothing outward.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] S177 follow-up — fork `main` pushed to `origin`, `9b96ac1..7b55ee3` (non-commit action, operator go-ahead)

- **Action:** `git push origin 7b55ee3:refs/heads/main`, `9b96ac1..7b55ee3`, a fast-forward of 41 commits: S177's
  claim, the three resync merges `421ebf9`, `7245f79`, `d4ac950` with the upstream commits they bring, the M2
  fixes, the config restatement, D3, the `HANDOFFS.md` trim and fold, D2, plan §8 and the close-out. Before the
  push, a guard confirmed that `origin/main` still read `9b96ac1`, that local `main` read `7b55ee3`, and that the
  push was a fast-forward. Afterwards `git ls-remote origin refs/heads/main` read
  `7b55ee30b5814c04214ada57c8ab722e0832f539`. The go-ahead was the operator's message after S177's close-out
  (*"push fork main (9b96ac1..7b55ee3) to origin"*). Fork only; nothing sent upstream.
- **Not pushed:** this recording commit, which is outside the range the go-ahead named.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S177 close-out — resync R2 done: fork `main` contains `upstream/main`; D2, D3 carried out; BL-57's P5 is next

- **Deliverable:** R2 of [`upstream-resync-2026-09-plan.md`](docs/planning/upstream-resync-2026-09-plan.md), recorded in its
  §8. Merges `421ebf9` (M2), `7245f79` (M3), `d4ac950` (M4); `git rev-list --count main..upstream/main` = 0.
  D3 `e1b6bdf` (2.18.0), D2 `e55f204` (`tests-sh-passed` 327, `dashboard-unit-tests` 336), `HANDOFFS.md` trim
  `75056a9` and fold `f4a8ec6`. Two operator decisions: the config restatement `0e8c6ac`, and no
  `CHANGELOG.md` trim (`d23d1a3`).
- **Final, in a `--no-local` clone of `b4c3a45`:** `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results
  db4e547cc884 · manifest c09d7e7f9109`; `bash bin/tests.sh` exit 0, **327 passed / 0 failed / 6 skipped** (Test 34's
  six rows, stated skips at 2 receipts, the only rows that differ from M4's run); `python3
  starter-kit/methodology_dashboard.py` exit 0, v2.18.0, 76/100, gates panel *"10 declared • 10 pass / 0 fail / 0
  unmeasured"*.
- **This commit:** S177's `HANDOFFS.md` receipt completed with that citation (the D9 lint now binds every
  close-out), the self-assessment (8/10) and S176's evaluation (7/10).
- **Not taken:** pushing fork `main` to `origin` (its own go-ahead); raising upstream's
  `TestThisRepoReadSetPartition` finding (outward, its own go-ahead).
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S177 — resync plan §8 (R2 as carried out), the BL-57 row, and fork Learnings #69–#70

- [`upstream-resync-2026-09-plan.md`](docs/planning/upstream-resync-2026-09-plan.md) §8 records R2 as carried out
  and overrides §2–§5 and §7 where they differ: per-stage suite results, the measured conflict sets (7 / 11 / 1),
  M2's three unpredicted red rows and the operator's config decision, the `HANDOFFS.md` deviation at M2, the
  whole-file `CLAUDE.md` resolution, the operator's no-trim decision, D2's values and why 327, D3, and the
  `context_budget.py --status` diff (exit 2 at both ends, no row changes status). Its status line now reads
  carried out. **Next, computed:** `git merge-tree --write-tree --name-only main bl57/changelog-rules` lists 5
  conflicting files for P5.
- `docs/planning/BACKLOG.md` BL-57 row: R2 done, P5 next.
- `docs/FORK_LEARNINGS.md` gains **#69**: an arriving test that reads the repository's own config binds
  whichever config a merge keeps. It also gains **#70**: a count floor holds only if it is measured at the
  state every close-out leaves. `bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15
  --no-citations` passes: 56 rows, contiguous 15..70, none over 1,500 B.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S177 — D2: this repository's quality gates tightened to the fork's measured values (`tests-sh-passed` 327, `dashboard-unit-tests` 336)

- **Measured:** `python3 starter-kit/quality_ratchet.py --run` in a `--no-local` clone of `f4a8ec6`, after the
  `HANDOFFS.md` trim and fold, gave **`quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results
  508b2b5489f3 · manifest 97a7aab85b9a`**. The measured values: `tests-sh-passed` 327, `tests-sh-failed` 0,
  `dashboard-unit-tests` 336, `context-budget-unit-tests` 118, `trimmer-unit-tests` 123,
  `ratchet-unit-tests` 45, and 0 on each of the four exit-code gates.
- **Change, `.quality-gates.json`:** `tests-sh-passed` 139 → **327** and `dashboard-unit-tests` 226 →
  **336**. The other three count gates already sat at their measured values, and every max-gate sits at 0.
  Both changes tighten, which the manifest's own rule lets through without approval, and the chained
  `--precommit` passed on this commit. A fork-only note key `_fork_tightening` records the values and why.
  Every gate's name, direction, command and extract pattern still equals `upstream/main`'s, and
  `config_defects` is `[]`.
- **Why 327 and not 333:** `bin/tests.sh` Test 34 turns six rows into stated skips when `HANDOFFS.md` holds
  fewer than three receipts. Every close-out leaves two and every claim makes three, so the same tree reads
  333 at M4 (6 receipts) and 327 here. A floor taken at 333 would refuse every close-out's gate run.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] S177 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- The pointer block `75056a9` wrote into `HANDOFFS.md`'s front matter is now one row of
  [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) (4 records, 2026-09-15 → 2026-09-16,
  `HANDOFFS-through-2026-09-16-4.md`, v1.5.0). The block is deleted, taking the file from 16,224 to 15,768 B,
  in its own commit per the index's fold rule. `docs/archive/HANDOFFS-through-2026-09-16-4.md.verify.sh` exits
  0 after the fold, `check-handoff --all --allow-pending` passes on 2 receipts, and `bin/check-links` exits 0.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-16-4.md` (4 record(s), 47,200 B → 16,224 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **4** record(s) (2026-09-15 → 2026-09-16) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-16-4.md`](docs/archive/HANDOFFS-through-2026-09-16-4.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-16-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-16-4.md.verify.sh)
rather than trusting a digest printed here. Live file 47,200 B → 16,224 B (−65.6%).

### 2026-09-16 · [BL-57] S177 — resync stage M4 merged (`d4ac950`), fork `main` now contains `upstream/main`; D3: `DASHBOARD_VERSION` 2.18.0

- **Merge `d4ac950`** (parents `d23d1a3`, `6b29d3d`), the last of the four stages. One file conflicted,
  `CHANGELOG.md`: upstream's one new entry (*"PR #82 merged — post-merge verification on main and the first
  tightening"*) now sits above its upstream neighbour, after the fork's 2026-09-16 entries. `HANDOFFS.md`
  merged cleanly and was rebuilt by the same rule: upstream's S23 sits above S22, after the fork's receipts,
  and `check-handoff --all` passes on 6 receipts. `.quality-gates.json` is upstream's (`fb81c4b`:
  `tests-sh-failed` max 0, `tests-sh-passed` min 139) until D2's commit. `git rev-list --count
  main..upstream/main` is **0**. The plan's M3 and M4 were predicted against a pre-M2 tree and are now
  measured: 11 conflicting files at M3 and 1 at M4, against the 12 and 12 computed at `9b96ac1`.
- **Measured on the merge, in a `--no-local` clone at `d4ac950`:** `bash bin/tests.sh` exit 0, **333 passed / 0 failed / 0
  skipped**, and its digit-masked rows are identical to M3's.
- **D3, this commit:** `DASHBOARD_VERSION` 2.17.0 → **2.18.0** in both twins. It is the next minor version
  above both numbering lines, because the merge brings upstream's 2.11.0 gates panel (changed output) and
  2.11.1 history walk. The comment above the constant now describes 2.18.0 and points to git for 2.17.0,
  following `0afe9d6`'s pattern. Both pins in `tools/test_methodology_dashboard.py` (the module attribute
  and the starter-kit source text) and the test's docstring follow. A whole-file search (fork Learning #68)
  found exactly those sites. The only remaining `2.17.0` text is in the two new comments, which name the
  prior version on purpose. The dashboard suite: 336 tests OK in the live checkout.
  `python3 starter-kit/methodology_dashboard.py` exits 0, reports `v2.18.0` at 76/100, and `dashboard.html`
  shows the gates panel (*"Quality Gates: 10 declared, never run"*).
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S177 — resync stage M3 merged (`7245f79`): PR #82 whole, the repository's own gates, and the ratchet chained into `pre-commit`; `CHANGELOG.md` stays untrimmed (operator decision)

- **Merge `7245f79`** (parents `0e8c6ac`, `64f23bf`). There were 11 conflicting files, not the 12 computed
  against `9b96ac1`: M2 had already taken upstream's `bin/tests.sh` block. **`.context-budget.json`:** ours.
  **`.githooks/pre-commit`:** upstream's ratchet block, then the fork's `--no-renames` comment and
  staged-path line, which appears exactly once. **`CLAUDE.md`:** the fork's whole file, which also refuses
  upstream's shortened rows in hunks git would have merged cleanly. It gains starter-kit rows for
  `context_budget.py` and `quality_ratchet.py` and a Tools row for their test suites, taking it from
  11,808 to 12,667 B. **`README.md`, `docs/tutorials/T1_setup.md`:** upstream's lists; every name on the
  fork's side is on upstream's. **`bin/check-handoff`:** the fork's block, then upstream's
  `declared_gate_count` and `validate_gate_citation`. Every line either side added is present in order
  (528 and 40). **Dashboard twins and their test file:** `DASHBOARD_VERSION` pins stay 2.17.0.
  **`CHANGELOG.md`:** upstream's quality-ratchet entry is replaced in place by its completed text (heading
  *"PR opened, not merged"*), and its one new entry sits above its upstream neighbour. **`HANDOFFS.md`:**
  upstream's S22 and its completed S20 follow the fork's receipts, and S21 stays in its shard.
  `check-handoff --all` passes on 5 receipts. Every upstream-only path equals `64f23bf`'s, and so does
  `starter-kit/FRAMEWORK_LEARNINGS.md` (D1). `SAFEGUARDS.md` is 17,024 B and the runner 55,420 B, both as
  plan §2.2 measured. `DISTRIBUTION` has 29 rows, and `.githooks/commit-msg --selftest` exits 0.
- **Measured on the merge, in a `--no-local` clone at `7245f79`:** `bash bin/tests.sh` exit 0, **333 passed / 0 failed / 0 skipped**.
  The digit-masked row diff against the M2 checkpoint shows upstream's 11 new rows passing (the manifest-removal
  cases, this repository's gates, the hook chain, and `check-handoff`'s D9 lint) and no flips.
- **The M2 checkpoint, in a clone at `0e8c6ac`:** exit 0, **322 passed / 0 failed / 0 skipped**. Its rows are
  identical to the trial that preceded the config commit.
- **This commit is the first the ratchet's `--precommit` checks:** the hook M3 merged runs it before the
  ledger gate, and it passed.
- **Decision (operator, picker, during M3's suite run): no `CHANGELOG.md` trim in R2.** The resync plan's R2
  step 3 and §7 item 4 schedule one at the trimmer's 196,608 B trigger. They do not cite the operator's
  2026-09-14 decision not to trim this file at that trigger (`3745748`; `BACKLOG-DETAIL.md`, BL-57), and that
  decision governs. `--check` keeps firing, and that is stated. As S171 did, a trim is raised with the
  operator only if the file passes the 262,144 B hard read refusal. It is 232,771 B after M3's merge.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S177 — `.context-budget.json` restates its token ceilings so upstream's partition test passes, every verdict unchanged (operator decision, an exception to D11)

- **Decision (operator, picker, after `8c429ed`):** *"Restate the config"*, chosen over patching the fork's copy
  of `tools/test_context_budget.py` and over stopping R2 after M2. It is an exception to D11 and to plan §4's
  *"no ceiling changes"*, taken because both limits in effect stay as they were.
- **Change, `.context-budget.json` only:** `starter-kit/SESSION_RUNNER.md` declares `max_tokens` 18,222 and
  `starter-kit/SAFEGUARDS.md` declares 6,777. These are `int(41,364 / 2.27)` and `int(15,386 / 2.27)`, the
  ceilings the tool already derived from their byte ceilings; they sum to 24,999, inside the 25,000-token
  read cap. `HANDOFFS.md` and `docs/planning/BACKLOG.md` drop the `max_tokens` 25,000 declared at `97c8066`,
  which the tool derives anyway by clamping `max_bytes / 2.27` to the cap. Each of the four entries' notes
  says so in its first sentence. Upstream's test file is untouched.
- **Measured:** `context_budget.py --json` before and after on the live tree: every row keeps its status,
  sizes, class totals and finding text (aside from the *"derived from max_bytes"* suffix), `config_defects`
  stays `[]`, and only `ceiling_derived` flips on the four rows. `tools/test_context_budget.py`: 118 tests
  OK. **The whole suite, in a throwaway `--no-local` clone of `8c429ed` with these values committed: exit 0,
  322 passed / 0 failed / 0 skipped**, and a digit-masked row diff against M2's run shows exactly its three
  FAIL→PASS flips (this change plus `8c429ed`'s two fixes).
- **Left for later, outward:** upstream's `TestThisRepoReadSetPartition` sums *every* whole-read class against
  one Read, but a class of separately-read ledgers is not one Read. Raising that upstream is its own go-ahead.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S177 — resync stage M2 merged (`421ebf9`); two of its three red rows fixed, the third waits on the operator

- **Merge `421ebf9`** (parents `374bd8c`, `cca7941`): stage M2 of
  [`upstream-resync-2026-09-plan.md`](docs/planning/upstream-resync-2026-09-plan.md) §5 R2, PR #82 through
  its P3. The 7 conflicting files were resolved per §2.3. `.context-budget.json` keeps ours (D11).
  **`CHANGELOG.md`:** upstream's one new entry (the quality-ratchet slice, still headed
  `CHANGELOG: pending` here) sits after the fork's entries for 2026-09-15, above upstream's
  "Merged PR #80". Removing it gives back ours byte for byte. **`HANDOFFS.md`: ours, unchanged — a deviation
  from §7 item 3.** Upstream's only new receipt at this stage is S20, a `status: pending` stub. Below the
  fork's receipts it fails `check-handoff --all --allow-pending`, because only the newest receipt may be
  pending. Test 34's presence control runs exactly that check on the live ledger, and upstream completes S20
  at M3, so the completed S20 is kept there instead (§2.4: an incoming receipt is checked against ours
  before it is kept). **`bin/tests.sh`:** the fork's Tests 36–40, then upstream's ratchet block; additions
  only. **Dashboard twins:** `DASHBOARD_VERSION` stays 2.17.0 until D3's own commit. The fork's
  `_FRAMEWORK_INSTALLED_CONTENT` gains `quality_ratchet.py` and `.quality-gates.json` in manifest order,
  with upstream's patterns and signatures, checked equal by evaluating both modules. Upstream's
  `_FRAMEWORK_FILE_SIGNATURES` dict is dropped, and the docstring's *"no tool's constant satisfies
  another's"* now names the one pair that does (both name theirs `VERSION`). **Test file:** both imports,
  2.17.0 pins, and two pre-existing mentions of the dropped dict renamed.
- **Measured on the merge, in a `--no-local` clone at `421ebf9`:** `bash bin/tests.sh` exit 1, **319 passed /
  3 failed / 0 skipped**, against 309 / 0 / 0 at the claim `374bd8c`. A digit-masked row diff shows upstream's
  11 new ratchet rows passing and exactly three pass→fail flips:
  1. **The dashboard suite:** `test_every_shipped_executable_is_recognized_from_its_real_source` pins 4
     installed files and the table now holds 6. **Fixed in this commit** (`tools/test_methodology_dashboard.py`,
     4 → 6). The guard's loop checks each file against its real shipped source, so it is what proves the two
     new table entries. With `quality_ratchet.py`'s rule neutralized the test fails, and the same holds for
     `.quality-gates.json`; with neither neutralized it passes. The suite: 332 tests OK.
  2. **Test 28:** the fork's never-overwrite row in `starter-kit/BOOTSTRAP.md` did not name the arriving
     seed. **Fixed in this commit:** the Adopter-owned row names `.quality-gates.json` and the Tracked row
     names `quality_ratchet.py`. The row is fork-only (upstream's `BOOTSTRAP.md` has no such table), and its
     converse check still finds no tracked file in it.
  3. **The context-budget suite: not fixed, operator decision pending.** Upstream's new
     `TestThisRepoReadSetPartition` (P0, `008d656`) asserts two properties of this repository's root
     `.context-budget.json`, which D11 keeps as the fork's. First, the read-set pair declares `max_tokens`:
     the fork's declares byte ceilings only. Second, every whole-read class's token ceilings sum within one
     25,000-token Read: the fork's `read-mandated` class declares 25,000 on each of `HANDOFFS.md` and
     `docs/planning/BACKLOG.md`, 50,000 in total. Three ratified constraints cannot all hold: D11 with §4
     (no ceiling changes), R2's DONE (`tools/test_context_budget.py` identical to upstream's), and a green
     suite.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S177 claim — R2 of the resync plan: merge stages M2–M4 (`cca7941`, `64f23bf`, `6b29d3d`), D2, D3 and the trims (in progress)

**Deliverable:** R2 of [`docs/planning/upstream-resync-2026-09-plan.md`](docs/planning/upstream-resync-2026-09-plan.md)
(§5, with §7 overriding): merge the three remaining stages into fork `main`, resolving each per §2.3 and
§7 item 3, then D2's tightening commit, D3's 2.18.0, the `CHANGELOG.md` trim and the `HANDOFFS.md`
retention trim and fold. Chosen by the operator after Phase 0 (picker), over a read-only review of
upstream PR #83.

- **Pre-flight, re-derived at Phase 0:** `upstream/main` is still `6b29d3d`, so R2 gains no stage. PR #83
  is still open at `219fb9d`. `git merge-tree --write-tree --name-only HEAD <target>` against `9b96ac1`
  lists 7 files for `cca7941` and 12 for each of `64f23bf` and `6b29d3d`, the same sets as §7 item 2.
- Phase 0 ledger reconcile: `CHANGELOG.md` frontier at `HEAD` `9b96ac1`, no gap; `HANDOFFS.md` frontier
  `4a0a5a7`, and its two later commits are S176's recorded follow-ups. Nothing backfilled. 2 receipts, so
  no Phase 0 trim. `methodology_trim.py --file CHANGELOG.md --check` FIRES at 204,886 B (owed in R2).
  Dashboard 76/100, medium risk. `context_budget.py --status` exit 2; its `over` rows are the runner (54,363 B),
  `SAFEGUARDS.md` (16,353 B, as §7 item 7 recorded) and the read-set total (70,716 B).
  The two Phase 0 instrument snapshots ride with this claim.

### 2026-09-16 · [ad hoc] S176 follow-up — fork `main` pushed to `origin`, `f1ae291..9aa1eb9`; BL-44 kept open (non-commit action and a grooming decision, operator go-ahead)

- **Action:** `git push origin main`, `f1ae291..9aa1eb9`, a fast-forward of 38 commits: S176's claim, the
  stage-M1 merge `5c2bd59` with the 28 upstream commits it brings, D1's four commits, the `HANDOFFS.md` trim
  and fold, the close-out and the BL-44 note. Before the push, a guard confirmed `origin` still read `f1ae291`
  and that it was an ancestor of `main`. Afterwards `git ls-remote` read
  `9aa1eb9304773f3987a2566186420145b2f468e7`, equal to local `main`. The go-ahead was given by picker after
  S176's close-out (*"Push fork main to origin"*), and this recording commit is pushed under it. Fork only;
  nothing sent upstream.
- **Decision (same picker):** **BL-44 stays open.** `8cfaf0d` fixed its span half; naming the reserved gap
  in the message remains. The backlog row records the decision.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-44] S176 follow-up — the check-learnings span fix in `8cfaf0d` was BL-44, not a new finding

- **Correction to the record:** `8cfaf0d`'s commit message, its ledger entry and the S176 receipt describe
  the `contiguous 1..65` message as a defect found this session. It is **BL-44**, raised at S109
  (`docs/planning/BACKLOG-DETAIL.md` §BL-44), and my Phase 0 backlog read did not reach it. The fix reads the span
  off the parsed rows, which is BL-44's core defect. BL-44's proposed fix also names the reserved gap in the
  message (*"#1..#38, 1 reserved (#14)"*), and `8cfaf0d` does not. **BL-44 stays open**; its row now says so, and
  closing it is the operator's decision.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S176 close-out — resync R1 done: stage M1 merged, D1 carried out, suite green; R2 is next

- **Deliverable, done:** R1 of [`upstream-resync-2026-09-plan.md`](docs/planning/upstream-resync-2026-09-plan.md). Merge
  `5c2bd59`, then `8c35872`, `8cfaf0d`, `82f0d3a`, `4ef6390`, the retention trim `084ba1b` and its fold
  `28ae585`, each with its own entry below. R1's DONE criteria, run bare on `28ae585`: `0fd003a` is an
  ancestor of `main`; no unmerged paths; the distributed learnings file equals `0fd003a`'s; the fork file's
  rows equal `1f34e75`'s 15–66; `check-learnings` (both tables), `check-handoff --all --allow-pending`,
  `check-links` and `commit-msg --selftest` all exit 0. **Suite in a `--no-local` clone of `28ae585`: exit 0,
  303 passed / 0 failed / 6 skipped**, the six being Test 34's stated rows at 2 receipts (digit-masked
  row diff against `4ef6390`'s 309 / 0 / 0).
- **This commit:** the `HANDOFFS.md` receipt (`status: complete`, self 8, predecessor S175 8); the plan's
  new **§7, *R1 as carried out — what R2 inherits***, and its status line. §7 holds the conflict sets
  computed against `28ae585` (M2 7 files, M3 and M4 12). It records that R1's trim makes `HANDOFFS.md`
  conflict at every later stage, that `cca7941` does not contain `0fd003a`, that the `CHANGELOG.md`
  trigger already fires (200,985 B), and the 26 citation sites against D1's 23. It also diffs
  `context_budget.py --status`: `SAFEGUARDS.md` ok -> over at 16,353 B, recorded, not remedied. Also here:
  BL-53's and BL-57's backlog rows, and **fork Learnings #67** (S175's deferred learning: an arriving hook
  binds the suite's own fixture commits) and **#68** (a grep inventory is line-scoped; wrapped references
  are invisible to it), 1,175 B and 1,043 B, checked from #15.
- **Not done, and not this session's:** R2; the `CHANGELOG.md` trim (R2 step 3); any push. Fork `main` is
  ahead of `origin/main` by 37 commits with this one: 9 of this session's and the 28 upstream commits the merge brought. Pushing
  needs the operator's go-ahead.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] S176 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- **Fold** of `084ba1b`'s pointer block by the index's rule (`docs/HANDOFFS_ARCHIVE_INDEX.md:51`): one
  124 B row at the bottom of the table, `| 9 | 2026-09-14 → 2026-09-16 | HANDOFFS-through-2026-09-16-3.md |
  v1.5.0 |`, and the block deleted from `HANDOFFS.md`, in its own commit as the rule requires (fork Learning #58).
  The shard holds S174 and upstream's S21, S19–S13, the receipts the M1 merge brought.
- **Also in `HANDOFFS.md`'s front matter:** the fold comment's `Learning #58` now reads *fork Learning #58*.
  Commit `82f0d3a`'s inventory skipped the two ledgers as history, but this comment is a live
  instruction; an anchored-fence search of both ledgers' front matter found no other citation past #13.
- **Front matter:** 4,475 B inside the trim commit, 4,024 B after the fold (4,019 B at S175, plus 5 B
  for *fork* ), against Test 39 A2's 7,168 B reserve. `bin/check-handoff --all --allow-pending` exit 0 on
  2 receipts.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-16-3.md` (9 record(s), 68,571 B → 16,296 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **9** record(s) (2026-09-14 → 2026-09-16) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-16-3.md`](docs/archive/HANDOFFS-through-2026-09-16-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-16-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-16-3.md.verify.sh)
rather than trusting a digest printed here. Live file 68,571 B → 16,296 B (−76.2%).

### 2026-09-16 · [BL-53] S176 — `CLAUDE.md` routes this fork's Phase 3C learnings to `docs/FORK_LEARNINGS.md`

- **`CLAUDE.md`, new subsection *Where this fork's learnings go*** (7 lines, in the fork-only part of
  *What This Repository Is*): the runner's Phase 3C (`starter-kit/SESSION_RUNNER.md:228`) sends a
  canonical-repo session to the distributed file. On this fork that file is upstream's, so fork
  learnings append to `docs/FORK_LEARNINGS.md`, cited as *fork Learning #N*. This is the one line D1 (A)
  owed (plan §3). It sits outside the table row that upstream rewrites at M3, so it adds no conflict hunk
  there. `CLAUDE.md` is 11,808 B against the 18,600 B resident ceiling.
- **`docs/HANDOFFS_ARCHIVE_INDEX.md:58`:** the fold rule's `Learning #58` link now reads
  *fork Learning #58* and points at `FORK_LEARNINGS.md`. That was the last of the plan's 23 live
  citation sites, 25 with the two wrapped ones.
- **Correction to the entry below, made in place:** its test-file breakdown read *#16 ×9, #26, #43*; the
  sites are #16 ×8, #26 ×2 (the pin's docstring and its message) and #43. The 11 and 18 totals were right.
- **Verified:** every relative link in `CLAUDE.md`, the index and `docs/FORK_LEARNINGS.md` resolves
  (Python); `bin/check-links` exit 0 (105 links, the distributed corpus).
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-53] S176 — live code cites *fork* Learnings, and the two suite rows D1 turned red pass again

- **Citations, following D1 (A):** 18 sites in 5 files now read *fork Learning #N*: both dashboard twins
  `:452` (#16) and the `archiv` result line (#15); `tools/test_methodology_dashboard.py`, 11 sites (#16 ×8,
  #26 ×2, #43); `bin/tests.sh:1713`, `:3003`, `:3089` (#16, #34 ×2). **Two more that the plan's count of 23
  missed:** in both twins the text `Learning`/`#26` wraps across two comment lines (`:409`), which a per-line grep cannot
  see (found with a multi-line Python search). The `archiv` result line also says its #15 row has since
  left the distributed corpus. Ledgers, plans, audits and `README.md` stay as written. `docs/audits/`
  cites several numbers past #13, most of them another project's.
- **Test 18's pin, rewritten as its docstring asks:** `docs/planning/BACKLOG.md` now appears in no
  distributed `.md` file, so the assertion is `[]`. Because `[]` is also what a net that reads nothing returns,
  a presence control first asserts that the root basename's hits include `SESSION_RUNNER.md`. A mutant
  whose net reads `""` fails on that control. The dashboard's disposition comment beside
  `READ_CAP_CLASS_A` is rewritten to match: both locations appear ZERO times. Its corpus count is
  corrected from 22 to 23, measured off `bin/_manifest.py`. The KEEP decision and its warrant are unchanged.
- **Test 37's `add_row37`:** skips any number the fixture's prose reserves (check-learnings'
  `RESERVED_RE` form). At M1 max+1 landed on the reserved `#14`. Measured on a copy of the live
  table: the helper now appends #15 and check-learnings reads OK. A mutant without the skip appends #14
  and fails with *"missing #15"*, the trial's failure.
- **Verified:** `TestPhaseC1ReadCapClasses` 10 OK; the twins `cmp` equal; `py_compile` clean; no added
  line over 102 characters.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-53] S176 — the fork's Learnings #15–#66 move verbatim to `docs/FORK_LEARNINGS.md`, checked from #15

- **Decision carried out:** D1 (A) of the resync plan (§3), ratified after S175. The merge `5c2bd59` made
  the distributed `starter-kit/FRAMEWORK_LEARNINGS.md` upstream's copy (rows 1–13 and the reserved `#14`). This commit gives
  the fork's 52 rows a home.
- **`docs/FORK_LEARNINGS.md` (new, 67,177 B):** a front matter (why the file exists, *fork Learning #N*
  as the citation form, append here from #67, the same append-only and 1,500 B rules), then the table
  header and rows #15–#66. **A Python comparison shows every row byte-identical to rows 15–66 of
  `git show b85851f:starter-kit/FRAMEWORK_LEARNINGS.md`**, in order, with the header row and separator
  identical too. It sits in `docs/`, not `docs/archive/`, because a dashboard test reads every
  `docs/archive/*.md` as a ledger. It is not in `bin/_manifest.py`, so it is not distributed.
- **`bin/check-learnings`:** `--first N` (default 1): rows must be contiguous from N. The default path's
  behaviour is unchanged. The OK line now reads its span off the rows (`min..max`). The count-derived form
  printed `1..65` for the old 65-row table ending at #66, because the reserved `#14` sits inside the span.
- **`bin/tests.sh` Test 32, three new rows:** the fork file is clean from #15; without `--first` it
  reports #1 missing, which proves the flag is read; a deleted row #40 is caught. The three use
  here-strings, not `echo | grep -q`, which can score a match as failed under pipefail. Run standalone:
  9/9 pass. A checker mutant that ignores `first` fails two of the three new rows.
- **`.context-budget.json`:** the on-demand entry is re-pointed from `starter-kit/FRAMEWORK_LEARNINGS.md`
  to `docs/FORK_LEARNINGS.md` (measured 67,177 B, 2026-09-16), and its notes cite *fork* Learnings #26,
  #34, #62/#63 and #16. **The 81,920 B ceiling did not move** (the plan's §4), so this file has 14,743 B
  of headroom where the whole table had 2,437 B. The note says so: BL-53's pressure eased because rows moved,
  not because the retirement question was answered. `context_budget.py --status`: the row reads `ok`.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S176 — resync stage M1 merged (`5c2bd59`), and Test 27.N1b passes the arriving `commit-msg` hook

- **Merge `5c2bd59`** (parents `b85851f`, `0fd003a`): the first of the resync plan's four stages
  ([`upstream-resync-2026-09-plan.md`](docs/planning/upstream-resync-2026-09-plan.md) §5 R1). It is a real
  3-way merge, resolved per §2.3. `.context-budget.json` keeps ours, by D11 (`git diff HEAD` empty).
  `starter-kit/FRAMEWORK_LEARNINGS.md` takes upstream's copy, by D1 (A): byte-identical to `0fd003a`'s, rows 1–13
  and the reserved `#14`. **`CHANGELOG.md`:** upstream's 12 new entries are interleaved by date, and on a
  shared date the fork's come first. A Python check shows each upstream entry verbatim in the result, and
  removing them gives back the fork's file byte for byte. **`HANDOFFS.md`:** upstream's S21 and S19–S13
  follow the fork's receipts. There is no session+date collision, and `check-handoff --all` exits 0 on
  11 receipts. The hooks skip merge commits, so the merge is recorded here, in the next ordinary commit.
- **Measured on the merge, in a `--no-local` clone at `5c2bd59`:** `bash bin/tests.sh` gave **303 passed / 3
  failed / 0 skipped**. The three failures are the ones the plan's D1 trial found (§3): Test 18's Learning
  #26 pin, Test 37's `add_row37` numbering onto the reserved `#14`, and Test 27.N1b. Run on their own:
  the dashboard suite, 321 tests with 1 failure (that pin, and nothing else behind the row); the
  context-budget suite 116 OK; the trimmer suite 123 OK; `bin/check-learnings` exit 0 (13 rows);
  `.githooks/commit-msg --selftest` OK (7 checks).
- **This commit, `bin/tests.sh:1283`:** Test 27.N1b's real fixture commit runs with
  `METHODOLOGY_REQUIRE_COAUTHOR=0`, the documented override of the disclosure gate that arrived with M1
  (`ad7bd37`). The test points `core.hooksPath` at the live hooks and makes a real commit with no trailer,
  so the gate refused the commit before the test could observe `pre-commit`'s claim carve-out. It stays a
  one-line change (plus a comment), because BL-57's P5 removes Test 27 with the carve-out.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S176 claim — R1 of the resync plan: merge stage M1 (`0fd003a`) and carry out D1 (in progress)

**Deliverable:** R1 of [`docs/planning/upstream-resync-2026-09-plan.md`](docs/planning/upstream-resync-2026-09-plan.md)
(§5): merge `0fd003a` into fork `main`, resolve its four conflicts per §2.3, apply Test 27.N1b's one-line
override, and carry out D1 (A). Chosen by the operator after Phase 0 (picker), over BL-61 and a comment on
upstream PR #83.

- **Pre-flight, re-derived at Phase 0:** `upstream/main` is still `6b29d3d`, so R2 gains no stage. PR #83
  is still open at `219fb9d`, with no reviews or comments. `git merge-tree --write-tree --name-only main
  0fd003a` lists `.context-budget.json`, `CHANGELOG.md`, `HANDOFFS.md`,
  `starter-kit/FRAMEWORK_LEARNINGS.md`, the same four as §2.1. The full merge still conflicts in 13 files.
- Phase 0 ledger reconcile: `CHANGELOG.md` frontier at `HEAD` `f1ae291`, no gap; `HANDOFFS.md` frontier
  `a614a89`, and the one later commit only records S175's push. Nothing backfilled. 2 receipts, so no
  Phase 0 trim. Dashboard 76/100, medium risk. `context_budget.py --status` exit 2, as at S175. The two
  Phase 0 instrument snapshots ride with this claim.

### 2026-09-16 · [ad hoc] S175 follow-up — fork `main` pushed to `origin`, `4735c6c..a614a89` (non-commit action, operator go-ahead)

- **Action:** `git push origin main`, `4735c6c..a614a89`, a fast-forward of 6 commits: S175's claim, the
  `HANDOFFS.md` trim and fold, the resync plan, the close-out, and the ratification record. Before the
  push, a guard confirmed that `origin` still read `4735c6c` and that it was an ancestor of `main`.
  Afterwards `git ls-remote` read `a614a89358a3dbaa2436eb2a6d1bec5926bfb880`, equal to local `main`. The
  go-ahead was the operator's message *"push fork main to origin"*, and this recording commit is pushed
  under the same go-ahead. Fork only; nothing sent upstream.

### 2026-09-16 · [BL-57] S175 follow-up — the operator ratifies the resync plan: every recommendation (picker)

- **Decisions, taken by picker after S175's close-out:**
  - **D1 (A), BL-53:** the distributed `starter-kit/FRAMEWORK_LEARNINGS.md` becomes upstream's at each
    merge stage, and the fork's rows #15–#66 move verbatim, numbers kept, to `docs/FORK_LEARNINGS.md`,
    where new fork learnings are appended. Carried out in R1.
  - **D2 (a):** adopt upstream's quality ratchet, then tighten its thresholds to the fork's measured
    values in R2, after stage 4.
  - **D3 (a):** `DASHBOARD_VERSION` 2.18.0 for the merged dashboard.
  - **D4 (a):** R1 merges stage 1 (`0fd003a`); R2 merges stages 2–4.
- **Recorded in:** the plan's status line and §3, BL-53's and BL-57's backlog rows, and S175's receipt
  (`next_steps`). Nothing outward; no push.

### 2026-09-16 · [BL-57] S175 close-out — the resync is planned, not merged; D1–D4 wait on the operator

- **Deliverable:** the resync plan (`e3bc12c`), after the operator re-scoped the session from merging to
  planning. Preceded by the retention trim of `HANDOFFS.md` (`4679cca`) and its fold (`1f34e75`).
- **Close-out commit:** S175's receipt (self 7/10, S174 scored 8/10). BL-53's and BL-57's backlog rows
  point to the plan. One sentence is added to R1's step 3: keep Test 27.N1b's fix to one line, because
  BL-57's P5 removes Test 27 with the hook's claim carve-out. The instrument snapshot from the close-out's
  `context_budget.py --status` rides along.
- **No `FRAMEWORK_LEARNINGS.md` row:** the file's fate is decision D1, and it is 2,437 B under its growth
  warning. The session's learning (an arriving enforcement hook binds the test suite's own fixture
  commits) is in the plan's D1 trial and the receipt, to be written into whichever file D1 names.
- **Next:** the operator's D1–D4, then R1. S175's close-out leaves 2 receipts, so R1's Phase 0 does not
  trim. **Nothing outward;** fork `main` is 5 commits ahead of `origin/main` after this close-out (`git rev-list --count origin/main..main`), and
  pushing it is its own go-ahead.

### 2026-09-16 · [BL-57] S175 — the fork resync planned: four merge stages over two sessions, four decisions for the operator

- **Deliverable:** [`docs/planning/upstream-resync-2026-09-plan.md`](docs/planning/upstream-resync-2026-09-plan.md),
  a DRAFT for ratification. It merges `upstream/main` `6b29d3d` into fork `main` in four stages cut where
  upstream's commits introduce the conflicts (`0fd003a`, `cca7941`, `64f23bf`, `6b29d3d`: 4, 4, 5 and 0
  newly conflicting files). Each of the 13 conflicting files gets a resolution and a verification, and the
  execution runs in R1 (stage 1) and R2 (stages 2–4).
- **Decisions put to the operator:** D1, the fork's Learnings #15–#66 now that upstream has its own #15
  and #16 (BL-53; recommended: the distributed file becomes upstream's, the fork's 52 rows move verbatim
  to a fork-only file); D2, adopting upstream's quality ratchet and tightening it to the fork's measured
  values; D3, the dashboard's version across two numbering lines (2.18.0 recommended); D4, the session
  split.
- **Measured, not predicted:** a trial of D1's recommendation, merging stage 1 in a throwaway clone:
  297 passed / 3 failed / 6 skipped against 300 / 0 / 6, exactly three flips. Two are D1's cost (a
  dashboard test pinned to Learning #26; Test 37's helper numbering a row with the reserved #14). **One
  is not D1's:** the `commit-msg` hook stage 1 brings refuses Test 27.N1b's trailer-less fixture commit
  under an agent harness, whatever D1 decides. Also measured: upstream's 11 receipts pass the fork's
  `check-handoff` (`--all`, `--archived`), and the merge takes `CHANGELOG.md` to ~206,596 B, over the
  trimmer's 196,608 B trigger.
- **Reviewed:** a read-only claims review by an independent subagent checked ~150 claims and found 15
  wrong in the draft. The author re-ran each one and corrected them before this commit: the stage 2 and 3
  re-conflicts, where upstream's #15 and S20 arrive, two DONE criteria that could not pass as written,
  and several counts and citations.
- **Session:** S175 · **Model:** Claude Opus 5 (claude-opus-5) · Nothing outward.

### 2026-09-16 · [BL-57] S175 — the operator re-scopes the session: plan the resync first, merge in later sessions (picker)

- **Decision, taken by picker during S175:** *"Write the merge plan"*, chosen over merging in this
  session or merging stage 1 only. The claim entry below named the merge itself as the deliverable;
  the deliverable is now the plan, and the merge runs in the sessions it defines.
- **Why it was put to the operator:** `git merge-tree` on `main` against `upstream/main` gave about two
  dozen conflict hunks in 13 files, only 4 of them insertions on both sides. Several resolutions are the
  operator's to decide: the Learning #15/#16 numbering collision (BL-53), adopting upstream's quality
  ratchet, and the dashboard's two numbering lines. And the previous resync, `213f841`, carried out a
  plan ratified first (`docs/planning/upstream-read-set-budgets-merge-plan.md`).
- **Recorded in:** this entry and S175's receipt. Nothing outward.

### 2026-09-16 · [ad hoc] S175 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- **Change:** the 3-line pointer block `methodology_trim.py` wrote for
  `docs/archive/HANDOFFS-through-2026-09-16-2.md` (trim `4679cca`) becomes one row at the bottom of
  `docs/HANDOFFS_ARCHIVE_INDEX.md` (n = 2, the shard's own fence count; 124 B) and leaves `HANDOFFS.md`.
  The first fold into the index S174 created: the front matter goes 4,475 B inside the trim commit back
  to 4,019 B, S174's size, so the trim-and-fold did not grow it. Its own commit, after the trim
  (Learning #58).
- **Commit/PR:** this commit
- **Session:** S175 · **Verified:** the shard's `.verify.sh` exit 0 at the trim commit `4679cca`
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-16-2.md` (2 record(s), 40,816 B → 15,874 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-09-16 → 2026-09-16) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-16-2.md`](docs/archive/HANDOFFS-through-2026-09-16-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-16-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-16-2.md.verify.sh)
rather than trusting a digest printed here. Live file 40,816 B → 15,874 B (−61.1%).

### 2026-09-16 · [BL-57] S175 claim — trim `HANDOFFS.md`, then resync fork `main` with `upstream/main` (in progress)

**Deliverable:** the fork resync, merging `upstream/main` `6b29d3d` into fork `main`, preceded by the
retention trim `HANDOFFS.md`'s policy calls. Chosen by the operator after Phase 0 (picker, *"Trim, then
resync"*), in the order decided after S173: the header cut (done at S174), this resync, then BL-57's P5.
BL-53's retirement rule is decided inside the resync (operator, S173).

- **Measured at Phase 0:** 3 receipts, above 2. Fork `main` is 56 commits behind `upstream/main` (25
  first-parent) from merge base `598c459`; `git merge-tree --write-tree --name-only main upstream/main`
  lists 13 conflicting files, the same 13 as at S174. `upstream/main` has not moved since S174.
- **The trim runs after this claim with `--cut 2`, not the `--cut 1` S174's receipt names.** That
  `--cut 1` was written for a Phase 0 trim, before a claim exists; this claim's stub is a fourth record,
  so `--cut 2` archives the same two receipts (S173, S172) and keeps S174's beside this stub.
- **Observed, not acted on:** upstream PR #83 opened (the maintainer's parallel-sessions plan, planning
  only: `docs/planning/parallel-sessions-plan.md`, `CHANGELOG.md`, `HANDOFFS.md`). Its head `219fb9d`
  conflicts with fork `main` in the same 13 files, so it adds none to the resync. No open upstream issues.
- Phase 0 ledger reconcile: `CHANGELOG.md` frontier at `HEAD` `4735c6c`, no gap; `HANDOFFS.md` frontier
  `9b8a438`, and the one later commit only records the push S174's follow-up names. Nothing backfilled.
  Dashboard 76/100, medium risk. The two Phase 0 instrument snapshots ride with this claim.

### 2026-09-16 · [ad hoc] S174 follow-up — fork `main` pushed to `origin`, `f2c49f7..9b8a438` (non-commit action, operator go-ahead)

- **Action:** `git push origin main`, `f2c49f7..9b8a438` — 6 commits (S174's claim, `e8bd62d`, `ad3479a`,
  `67ac209`, the close-out `df235dc` and the decisions commit), a fast-forward, run behind a guard that
  confirmed the remote still read `f2c49f7` and was an ancestor of `main`. Read back with
  `git ls-remote`: `9b8a4382455be1769312269406c75d7f10c771f8`, equal to local `main`. The go-ahead was
  the operator's picker answer *"Push fork main now"*. This recording commit follows under the same
  go-ahead. Fork only; nothing sent upstream.

### 2026-09-16 · [BL-59] S174 follow-up — the operator closes BL-59 and schedules BL-61; fork `main` push approved (picker)

- **Decisions, taken by picker after the close-out:**
  - **BL-59 is CLOSED.** The retention it set (N=1, S172) is now measured reachable: Test 38 reads a
    frozen fixture (`d13a165`), and a `--cut 1 --force` trim plus its fold on `ad3479a` ran 300 passed /
    0 failed / 6 stated skips. The front-matter cut it left owed is done. What stays undone is teaching
    `methodology_trim.py` a retention mode, which ships to adopters and needs its own go-ahead. The row
    moves to §Completed items; the detail body stays, as BL-45's did.
  - **BL-61 is raised and scheduled:** lower `HEADER_RESERVE_BYTES` (`bin/check-handoff:663`) now that
    the front matter is 4,019 B and no longer grows per trim, banking the freed ~3 KB as S109 did. It
    runs as a later small session, not ahead of S175's trim, the fork resync or BL-57's P5.
    Canonical-only.
  - **Push fork `main` to `origin`:** approved. Recorded in the next entry once it is done.
- **Recorded in:** `docs/planning/BACKLOG.md` (the open list, the BL-61 row, BL-59's completed row),
  `docs/planning/BACKLOG-DETAIL.md` (BL-61's body), and the S174 receipt's `next_steps`.

### 2026-09-16 · [BL-59] S174 close-out — the header cut is done; S175's Phase 0 trims and folds into the new index

- **Change (this commit):** the S174 receipt in `HANDOFFS.md` goes from `pending` to `complete`
  (self 7, S173 scored 8). The context-budget reading taken at close-out rides with it.
- **Deliverable, on fork `main`, local and not pushed:** `e8bd62d` (Test 39's M2 literal 4096 → 2048),
  `ad3479a` (the shard table moves to `docs/HANDOFFS_ARCHIVE_INDEX.md`; front matter 7,028 → 3,929 B)
  and `67ac209` (corrections from a claims review, front matter 4,019 B). Each has its own entry below.
- **Verified, not predicted:** `bin/tests.sh` in `--no-local` clones, each asserted to be at its commit —
  306 passed / 0 failed at `be405b3`, `e8bd62d`, `ad3479a` and `67ac209`, with the same assertion set;
  305 / 1 for the cut without the M2 fix; 300 / 0 / 6 stated skips after a simulated S175 trim and fold.
  All 21 handoff-shard proofs gave the same exit codes before and after (18 pass, 3 pre-existing BL-36
  failures). `context_budget.py --status` shows no status flips against Phase 0.
- **For S175:** 3 receipts, so its Phase 0 trims with `--cut 1 --force` and then folds the pointer block
  into the index by the rule at `docs/HANDOFFS_ARCHIVE_INDEX.md:50`, in its own commit. Then comes the
  fork resync (`upstream/main` is now `6b29d3d`, 56 commits, 13 conflicting files), then BL-57's P5.
- **Raised for the operator, not acted on:** whether to lower `HEADER_RESERVE_BYTES` to bank the freed
  ~3 KB (the S109 precedent), and whether BL-59 closes now that N=1 is measured reachable.

### 2026-09-16 · [BL-59] S174 — corrections to `e8bd62d` and `ad3479a`, found by a claims review before close-out

- **Wrong number, and the urgency it carried:** both earlier entries and `ad3479a`'s message say a fold
  adds **~147 B** and that the trim S175's Phase 0 calls *"would have failed A2"*. Measured in bytes, the 21
  table rows are **125–129 B**, and the last fold added **123 B** (6,984 → 7,107 B, `1ec509d^` →
  `1266282`). With 140 B left the next fold would have landed at ~7,157 B and passed. Only the trim
  commit itself would have exceeded the reserve before its fold, as `5049845` (7,178 B), `0ccfce8`
  (7,311 B) and `1ec509d` (7,432 B) already did. **The cut was due one trim later than stated.** The
  ~147 B figure came from the spent-reserve callout `ad3479a` removed, which also said ~60 B remained.
- **Also overstated in `ad3479a`'s entry:** *"a file added there"* would not be read as a shard; only
  a `HANDOFFS-*.md` name in `docs/archive/` would, and `tools/test_methodology_dashboard.py:4426` would pick
  up any `*.md` there. The index's own warning already said it precisely.
- **Text corrected in this commit:** the index said its rows were *"unchanged"* (their links changed),
  that *"the next row would have overflowed"*, and that every shard is `HANDOFFS-through-<date>.md` (two
  carry `-2`). Its fold rule now says where the trimmer inserts the block, that the shard cell takes the
  bare name, and that the proof link is dropped. The front matter now says a trim *commit* still carries
  the ~448 B block until the fold. `bin/tests.sh`'s M2 comment no longer says the mutant survived at
  a commit where the move had not happened. BL-59's row no longer says N=1 is unreachable next to the
  commit that made it reachable, and records the measurement: a `--cut 1 --force` trim plus its fold on
  `ad3479a` ran **300 passed / 0 failed / 6 stated skips**.
- **Front matter after this commit: 4,019 B** of 7,168 B.
- **Left as written:** `docs/planning/BACKLOG-DETAIL.md` BL-60 (*"`HANDOFFS.md`'s own archive table says
  exactly that"*) and BL-59's detail (the fold *"replaces that block with one table row"*; *"What remains
  for N=1: give Test 38 a frozen fixture"*). Item bodies are deliberately not edited, and
  `BACKLOG-DETAIL.md.verify.sh` proves them byte-identical.

### 2026-09-16 · [BL-59] S174 — `HANDOFFS.md`'s shard index moves out of its front matter, so a trim no longer grows it

- **Change:** the archive table (21 rows), its intro and the fold rule move from `HANDOFFS.md`'s front
  matter to a new [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md). The rows are unchanged
  except for their links (`docs/archive/…` → `archive/…`). Front matter **7,028 B → 3,929 B** against
  the 7,168 B header reserve (`bin/check-handoff:663`, Test 39 A2): **3,239 B left**, where 140 B
  remained and each trim-and-fold row cost ~147 B. The trimmer's ~448 B pointer block now fits even
  inside the trim commit, before the fold.
- **Why not `docs/archive/`:** `bin/model-report:158`, `starter-kit/methodology_trim.py:921` and
  `starter-kit/methodology_dashboard.py:1135` find shards by the glob `docs/archive/HANDOFFS-*.md`. The
  trimmer would even have read this commit as an archive event (a file added there, `HANDOFFS.md`
  shrinking). `tools/test_methodology_dashboard.py:4426` treats every `docs/archive/*.md` as a ledger.
  Nothing globs `docs/*.md`.
- **Corrected in the move, each checked:** the table intro's *"20 trims, 154 receipts"* was stale
  (21 and 160; every row's `n` equals its shard's fence count). Its *"every shard is
  `HANDOFFS-through-<date>.md`"* skipped `HANDOFFS-archive.md` (19 receipts, 2026-07-08 → 2026-07-30,
  no proof), which the index now names. The index gives commands to derive the totals instead of
  writing them (22 files, 179 receipts). In the front matter, *"indexed in the table below"* and
  *"all four retained here"* (stale since N=1) are rewritten, and the spent-reserve callout goes. It
  also said ~60 B remained, where 140 B did.
- **Not changed:** the trimmer (distributed), `HEADER_RESERVE_BYTES`, and the shipped `.verify.sh`
  proofs, each of which compares its own trim commit with that commit's parent
  (`docs/archive/HANDOFFS-through-2026-09-16.md.verify.sh:163`).
- **Depends on `e8bd62d`,** which moved Test 39's M2 mutant under the smaller front matter first.

### 2026-09-16 · [BL-59] S174 — Test 39's M2 mutant moves below the front matter the header cut leaves

- **Change:** `bin/tests.sh` Test 39's M2 plants `HEADER_RESERVE_BYTES = 2048` instead of `4096`. M2 counts
  as killed only when the planted reserve is under the **live** `HANDOFFS.md` front matter, which it
  measures, so the live file was the mutant's unstated fixture. The header cut, run first in a
  throwaway clone, took the front matter from 7,028 B to 3,929 B, under 4,096 B, and the suite went from
  306 passed / 0 failed to 305 / 1 on exactly this row:
  `MUTANT SURVIVED: reserve 4096 B vs front matter 3929 B (fits ceiling: 1)`.
- **Landed before the cut, so every commit stays green:** 2,048 B is under both 7,028 B and 3,929 B,
  and A1 still fits (3 × 12,288 + 2,048 = 38,912 B ≤ 65,536 B). The block's comment now states the
  constraint and what happens if the front matter is ever cut below it.

### 2026-09-16 · [BL-59] S174 claim — the `HANDOFFS.md` header cut (in progress)

**Deliverable:** shorten `HANDOFFS.md`'s front matter so the retention trim S175's Phase 0 will call
does not break Test 39 A2 (`bin/tests.sh:3047`). Chosen by the operator at Phase 0 (picker), in the
order decided after S173: this cut, then the fork resync, then BL-57's P5.

- **Measured at Phase 0:** front matter 7,028 B against `HEADER_RESERVE_BYTES` 7,168 B
  (`bin/check-handoff:663`) — 140 B left; one trim-and-fold row is ~147 B. The file's own callout says
  ~60 B, which is wrong.
- **Observed, not acted on:** `upstream/main` moved `64f23bf` → `6b29d3d` — three maintainer commits,
  the first ratchet tightening after #82 (`.quality-gates.json`: tests-sh-failed max 0, tests-sh-passed
  min 139) and his receipts. Fork `main` is 56 behind, not 53. No open upstream PRs or issues.
- Phase 0 ledger reconcile: `CHANGELOG.md` frontier at `HEAD` `f2c49f7`, no gap; `HANDOFFS.md` frontier
  `d5ea5c4`, and the one later commit only records a push S173's receipt already names. Nothing
  backfilled. Dashboard 76/100, medium risk. The two Phase 0 instrument snapshots ride with this claim.

### 2026-09-16 · [ad hoc] S173 follow-up — fork `main` pushed to `origin`, `3f9210c..d5ea5c4` (non-commit action, operator go-ahead)

- **Action:** `git push origin main`, `3f9210c..d5ea5c4` — 1 commit, a fast-forward, run behind a guard
  that confirmed the remote still read `3f9210c`. Read back with `git ls-remote`:
  `d5ea5c412e57a26ab3ba7a5ad4afd8045d6ee870`, equal to local `main`. Go-ahead: the operator's picker answer
  *"Push now"*. This recording commit follows under the same go-ahead.

### 2026-09-16 · [ad hoc] S173 follow-up — grooming decisions on F5/F6, BL-53, BL-54, BL-36 and BL-60 (operator, picker)

- **Decisions,** each re-checked against current state before the operator was asked:
  - **F5 rides BL-57's upstream PR (P12); F6 is closed.** On `upstream/main` `64f23bf`,
    `starter-kit/methodology_trim.py:33` still says the ledger hook runs `--no-renames` (upstream's hook
    has 0), and `:9`/`:155` still cite a design doc upstream lacks. BL-57 already edits that file. F6 was
    wording in #80's description, and #80 merged on 2026-09-15.
  - **BL-53: the retirement rule is decided inside the fork resync.** Fork `main`'s file is 79,483 of
    81,920 B (about 2 rows); upstream's is 16,560 B (13 rows); the file is one of the resync's 12 conflicts.
  - **BL-54: fixed after BL-57's P5, before P6** — when the adopters first sync from the resynced fork
    `main`, the merge shape the bug breaks. `bin/sync:60` and `bin/status:56` are unchanged upstream.
  - **BL-60: one planning session costs its three shapes and folds BL-36 in**, so the four frozen
    proofs that report FAIL over intact archives are decided inside the new scheme, not rewritten twice.
    31 proofs, 453,689 B, re-counted.
- **Recorded in:** `docs/planning/BACKLOG.md` (the four index rows);
  `docs/planning/pr80-review-response.md` §6; the BL-57 plan's finding (11); the S173 receipt's
  `next_steps`.

### 2026-09-16 · [ad hoc] S173 follow-up — fork `main` pushed to `origin`, `ef83601..22a78b3` (non-commit action, operator go-ahead)

- **Action:** `git push origin main`, `ef83601..22a78b3` — 8 commits, a fast-forward, run behind a guard
  that confirmed the remote head was an ancestor of `main`. Read back with `git ls-remote`:
  `22a78b3c0d6c64d6310ba9466a89aca2c53caa6f`, equal to local `main`. The go-ahead was the operator's
  picker answer *"Push fork main"*. The commit carrying this entry follows it to `origin` under the
  same go-ahead, as S168's recording commit did.

### 2026-09-16 · [BL-57] S173 follow-up — the operator's two decisions, and the branch pushed to `origin` (non-commit actions)

- **Decisions, taken by picker after the close-out:** (1) P5 starts from a **resync of fork `main` with
  `upstream/main`**, then ports BL-57's own change from `64f23bf`, not the plan's `b82dcff` form.
  (2) **S174 does the `HANDOFFS.md` header cut** first, because the trim S175's Phase 0 calls needs
  it. Recorded in the plan (finding (9), `docs/planning/changelog-rules-contradictions-plan.md:129`),
  BL-57's backlog row, and the S173 receipt's `next_steps`, which is rewritten around them.
- **Action:** `git push origin bl57/changelog-rules`, `775ba23..83a12f0` — a fast-forward, run behind a
  guard that confirmed the remote still read `775ba238` and was an ancestor. Read back with
  `git ls-remote`: `83a12f0380b7d23c9a2e339a38fffc49314c7ad2`. P3, P4 and both upstream merges are now
  backed up; fork only, nothing sent upstream.
- **Also:** the operator asked that requests for input come as a picker, to reduce typing. That is a
  change in how I ask, recorded in agent memory; no repository file changed for it.

### 2026-09-16 · [BL-57] S173 close-out — BL-57's P4 done on the branch, not pushed; P5 opens with an operator decision about its base

- **Change (branch `bl57/changelog-rules`, `83a12f0`, not pushed):** P4's four commits after the merge
  `52ad407`. `0c20022` gives §The Action Ledger its *Lifecycle* and *Placement* rules; `f235db3` turns
  *append* into *prepend* at seven sites and records the claim commit's *(in progress)* entry; `836e0d2`
  replaces *completed work history* with the action ledger and brings `CLAUDE.md` back under its ceiling;
  `83a12f0` rewrites upstream's root `CHANGELOG.md` front matter (D8 i). Each commit has its own branch
  ledger entry.
- **Change (fork `main`, this commit):** the plan records P4 done, with findings (6)–(10) for P5–P12
  (`docs/planning/changelog-rules-contradictions-plan.md:114`) and a status-line warning about P5's port.
  BL-57's backlog row reads *P4 at S173, next P5*. The S173 receipt is completed in `HANDOFFS.md`.
- **Found, for the next session:** P5's port command as the plan writes it is **34 files, +3,015/−358**,
  because the branch now carries #80's fixes and #82's ratchet; BL-57's own net change on `64f23bf` is
  **16 files, +532/−252**. Fork `main` is 53 commits behind `upstream/main`, and merging the two conflicts
  in 12 files. So P5 starts with the operator's choice: port from `64f23bf`, or resync fork `main` first.
- **No learning row:** `starter-kit/FRAMEWORK_LEARNINGS.md` is within about two rows of its ceiling, and
  neither finding is new at the framework level. That a recorded density can hide token growth is already
  stated in upstream's `.context-budget.json`, in the runner's entry: *"A DENSITY IS TIED TO THE BLOB IT
  WAS MEASURED ON"*. The instrument change is a harness behaviour,
  recorded in the plan and in the receipt's gotchas.
- **Session:** S173 · **Verified:** see the receipt's `runtime_smoke` — the branch head `83a12f0`, in a
  `--no-local` clone with HEAD asserted: `bin/tests.sh` 141 / 0; ratchet 10/10 (`c5fca86e4674`);
  `bin/check-links` 110; `context_budget.py --status` exit 0, no status flips against `upstream/main`, read-set
  total 70,253 B against 70,276 B.
- **One status flip on fork `main`, caused by this session and left as it is:** `context_budget.py --status`
  (exit 2 at Phase 0 and now, the runner's standing breach) moves `HANDOFFS.md` from ok to **warn** — not
  a ceiling: its density was measured at 20,310 B and the file is 32,800 B after this session's claim stub
  and receipt, a 61% drift that marks its ≈14,500-token figure provisional. Re-measuring is a budget
  commit of its own, as `24d9645` was. An estimate, not a measurement: the next retention trim should take
  the file back near the measured size.
  Runner doubled 37,717 (≤ 37,731) and `CLAUDE.md` 46,953 (≤ 46,965), each beside a reproduced control.

### 2026-09-16 · [BL-57] S173 — #82 merged into BL-57's branch; P4's size criterion restated on the new base before any P4 edit

- **Change:** `docs/planning/changelog-rules-contradictions-plan.md` gains the S173 amendment (above §0)
  and P4's DONE criterion is restated against `upstream/main` `64f23bf` instead of `b82dcff`: the runner
  no larger than **18,865.5 tokens (doubled ≤ 37,731)**, `CLAUDE.md` no larger than **23,482.5 tokens
  (doubled ≤ 46,965)** — newly a criterion, since #82 gave it a token ceiling — `SAFEGUARDS.md` at blob
  `933816b4`, no `context_budget.py` status flip, and `quality_ratchet.py --run` passing.
- **The branch action it rests on:** `52ad407` on `bl57/changelog-rules` merges `upstream/main`; two
  one-line conflicts, both predicted at Phase 0 (`CLAUDE.md`, `ITERATIVE_METHODOLOGY.md`). A merge skips
  the ledger hook, so the branch carries no entry of its own for it — as `9e1dfeb` did at S168.
- **Found:** the merge is **4 tokens over `CLAUDE.md`'s ceiling** (46,973 doubled) — P1's row wording is
  9 B shorter and 4 tokens longer, and `context_budget.py` prices it at 2.519 B/token and reports it ok.
  P4's `CLAUDE.md` edit pays it back. P3's 14-token runner saving survived the merge exactly (37,703).
- **Found:** the Read tool no longer refuses a file over 25,000 tokens — it returns a 25,000-token page and
  prints the count in the truncation notice — so each doubled-file reading costs a page of context.
  Readings were taken in a subagent that reproduced the 36,955 control in the same run.
- **Session:** S173 · **Verified:** upstream 139/0, ratchet 10/10, links 107, budget exit 0; merge 141/0,
  10/10 (`c5fca86e4674`), 110, exit 0 with no status flips — both in `--no-local` clones, HEAD asserted.

### 2026-09-16 · [BL-57] S173 claim — BL-57's P4: merge #82 into the branch first, then entry lifecycle and the words

**Deliverable:** BL-57's **P4** (`docs/planning/changelog-rules-contradictions-plan.md:551`) on branch
`bl57/changelog-rules` (worktree `../methodology-bl57`, at `18962a9`): the lifecycle and placement rules
in §The Action Ledger, "append" becomes "prepend" where the file is newest-on-top, the claim commit's
*(in progress)* entry, "completed work history" becomes the action ledger, and upstream's root
`CHANGELOG.md` front matter.

- **Observed, not taken by this fork: upstream PR #82 MERGED** at 2026-09-16T18:05:47Z — merge commit
  `64f23bf`, head `5c9d3b40`, merged by `rmsharp` — six minutes after S172's last commit. Before it
  merged, the maintainer answered this fork's comment (`5701463025`) and pushed his fixes F1b–F6.
  Verified at Phase 0 with `gh pr view 82`. No open upstream PRs or issues remain.
- **So S169's merge-first amendment triggers.** P4 starts by merging `upstream/main` `64f23bf` into the
  branch. `git merge-tree` at Phase 0: conflicts in `CLAUDE.md` and `ITERATIVE_METHODOLOGY.md` only.
- **P4's token criterion predates #82** (`:575`, doubled read ≤ 36,955 on blob `c0550acd`): the merged
  runner is 53,220 B against the branch's 52,163 B. It is re-measured on the merge result and restated
  before any P4 edit.
- Phase 0 ledger reconcile: both frontiers at `HEAD` `c509190`, no gap, nothing backfilled. The two Phase 0
  instrument snapshots ride with this claim.

### 2026-09-16 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-16.md` (6 record(s), 75,185 B → 20,820 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **6** record(s) (2026-09-15 → 2026-09-16) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-16.md`](docs/archive/HANDOFFS-through-2026-09-16.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-16.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-16.md.verify.sh)
rather than trusting a digest printed here. Live file 75,185 B → 20,820 B (−72.3%).

### 2026-09-16 · [ad hoc] S172 follow-up — the maintainer replied on #82; the receipt's `next_steps` rewritten around it

- **Found while re-verifying before restating, not by looking for it.** Rewriting `next_steps`
  required restating #82's state, so it was re-fetched rather than relayed from Phase 0 — and **three
  things had changed**: the maintainer replied (comment **`5701463025`**, KJ5HST,
  2026-09-16T17:09:39Z); **#82's head moved `c84e7d96` → `5c9d3b40`**; and `upstream/main` moved to
  `0fd003a`. Our comment `5691623656` remains unedited.
- **What the reply says, in substance.** He re-ran our reproduction and it held in all seven sections,
  all four token figures, and `--run`'s results hash. He takes our §1 rewording as the base for the PR
  description. He then gives **six corrections and two findings of his own**, and closes *"Fixes next,
  in the order above."* **Four corrections say specific claims of ours were wrong** — on the fix order
  for the deletion hole, on the dashboard fix being unreachable while the manifest is absent, on the
  pass-offsets-fail claim, and on whether the gate-run comparison is specified anywhere.
- **Saved verbatim** to `docs/planning/pr82-maintainer-reply.md` (4,582 B). **sha256-identical to the
  API body both with and without `jq`'s trailing newline** — `520a7b60…` and `245d388e…` on each
  side — so the label is a measurement, not a description. Precedent: `docs/planning/pr82-comment.md`.
- **The receipt's `next_steps` rewritten.** Item (1) is now the reply — ranked above BL-57's P4 because
  it is the upstream engagement this repository exists for, and because our pinned findings are stale
  against the moved head until re-run. P4 is (2). The front-matter cut is (3) **with a computed
  deadline**: the next trim lands at S175's Phase 0, so the cut belongs to S173 or S174. The expected
  `FRONTMATTER_FIELD_ABSENT` notice and BL-60 follow.
- **Nothing was posted.** A reply is an outward action and the item says so in capitals. **Also
  confirmed while there:** `origin` holds `bl57/changelog-rules` at `775ba238`, P2's head, so **P3's
  four commits exist only in the local worktree.**
- **Commit/PR:** this commit
- **Session:** S172 · **Verified:** `gh pr view 82` and `gh api .../issues/82/comments` re-run;
  `git ls-remote origin 'refs/heads/bl57*'` returns `775ba238`; `bin/check-handoff --all` exit 0.
- **Model:** Claude Opus 5

### 2026-09-16 · [ad hoc] S172 follow-up — a defect the policy rewrite introduced: the trimmer's regenerated field no longer exists

- **What was wrong, and it was mine.** `methodology_trim.py`'s `HANDOFFS.md` `LedgerSpec` declares one
  regenerated front-matter field, matched by the literal `This file currently holds **<N>**`
  (`starter-kit/methodology_trim.py:336`). **S172's policy rewrite deleted that sentence**, so the
  declaration now matches nothing. Found by reading the spec while answering a question about
  something else — no gate reports it, because `--check` never writes and so never evaluates the
  regenerated fields.
- **The consequence, read from the code rather than guessed:** `apply_regenerated` emits
  **`FRONTMATTER_FIELD_ABSENT`** and continues (`:1131`). Not a crash, not a silent skip — a stated
  diagnostic on every future trim. The same rewrite also left the blockquote below it dangling: it
  opened *"The count above drifts between trims"* with no count above.
- **Disposition: keep the deletion, state it.** The number is the one
  [Learning #12](starter-kit/FRAMEWORK_LEARNINGS.md) and upstream
  [issue #65](https://github.com/KJ5HST/methodology/issues/65) both cite as *always wrong by the next
  close-out*; restoring it would restore a documented defect to buy a quieter tool. The dangling
  blockquote is replaced by one that says the field is gone on purpose and that the trim notice is
  expected. **The real fix — dropping the declaration from the spec — is a change to a tool every
  adopter holds, so it is distributed and its own go-ahead.**
- **A side effect that changes a scheduling fact:** the replacement is 645 B out for 505 B in, so the
  front matter drops **7,107 → 7,028 B** and the header reserve goes from ~60 B of room to **140 B —
  one more trim-and-fold row.** The debt BL-59 records is deferred by one trim, not paid.
- **Third time in this session the front matter refused its own explanation.** The first draft of
  this note ran 833 B against the 645 it replaced and put the file 127 B over the reserve; it fitted
  only after the reasoning moved here. A file that cannot afford to explain its own changes is the
  argument for the structural cut, stated as a measurement rather than an opinion.
- **Commit/PR:** this commit
- **Session:** S172 · **Verified:** front matter 7,028 B against the 7,168 B reserve;
  `bin/check-handoff --all` exit 0; `bin/check-links` exit 0; `grep -c 'This file currently holds'`
  returns 0, and `starter-kit/methodology_trim.py:336`-`:339` re-read for the exact regex.
- **Model:** Claude Opus 5

### 2026-09-16 · [BL-59] S172 follow-up — the retention trigger moves to "above 2", and BL-60 is raised on the proof scripts

- **Change:** `HANDOFFS.md`'s policy separates two numbers it had conflated. **Depth stays 1** — the
  handoff is one receipt — but the **trigger moves to "above 2"**, so a trim runs every second
  session instead of every session. The heading now reads *"keep ONE receipt, trim above TWO."*
- **Why, measured.** Every trim emits a `.verify.sh` of **16,011 B**, a fixed cost independent of what
  it archives. Amortised, that is **16,158 B per session at a trigger of 1 and 8,079 B at 2** — the
  proof alone costing more than the **9,545 B** median receipt it proves. The ceilings do not bind
  here: at the median the live file stays under both `max_bytes` and `max_tokens` up to **five**
  receipts, and 2 is the largest trigger still safe at the **13,276 B** worst-case receipt observed
  (a trigger of 3 peaks at 4 receipts, ~26,576 tokens, over the 25,000 cap).
- **It also works with the SRF rule rather than against it.** The adjudication proves that rule
  *"rewards overshoot and punishes maintenance on time"*; a later, larger trim amortises the fixed
  proof over more relief. It still will not go green — any steady state gives SRF exactly 1.0000 by
  construction — so `--force` remains required, but the warrant is stronger, not weaker.
- **What it does not fix, stated so it is not mistaken for a fix:** the header reserve. ~60 B remain
  against ~147 B per trim, so **the next trim still reddens Test 39 unless this front matter is cut
  first.** The trigger halves the rate, not the debt. Test 34's six `SKIP` rows are likewise
  unaffected — it wants three live receipts, which this policy reaches only momentarily.
- **BL-60 raised:** 31 proof scripts hold **453,689 B**, **12.4% of `docs/archive/` and 5.4% of the
  tracked repo**, and two consecutive ones differ by **4 lines / 336 B — 97.9% of each new proof is
  bytes the repository already holds**. Three shapes costed roughly, none chosen; the item records
  three constraints a fix must respect, the binding one being that **`methodology_trim.py` is
  installed at every adopter root (`bin/_manifest.py:50`, TRACKED), so any fix is a distributed
  change and its own go-ahead.**
- **The policy edit took four passes to fit,** which is the front-matter debt demonstrating itself:
  the first draft ran 184 B over the reserve, and it fitted only once the SRF reasoning and the
  consumer measurement moved out to BL-59, leaving the instruction here.
- **Commit/PR:** this commit
- **Session:** S172 · **Verified:** front matter 7,107 B against the 7,168 B reserve;
  `bin/check-handoff --all` exit 0 (1 receipt); `bin/check-links` exit 0; every figure above
  re-derived from `git ls-files 'docs/archive/*.verify.sh'` and `diff`, and `bin/_manifest.py:50`
  re-read rather than recalled.
- **Model:** Claude Opus 5

### 2026-09-16 · [ad hoc] S172 follow-up — fork `main` pushed to `origin`, `1d88eaa..ef83601` (non-commit action, operator go-ahead)

- **Action:** `git push origin main` on the operator's explicit go-ahead — **27 commits**,
  `1d88eaa..ef83601`, a fast-forward (0 behind before the push). To **`rmsharp/methodology`**, the
  fork. **Nothing went to `KJ5HST/methodology`;** upstream is untouched and still needs its own
  go-ahead for anything.
- **Read back from the remote, not from the push output.** `git ls-remote origin refs/heads/main`
  returns `ef836018398ee59b709a8d164b6cb3c978237d94`, identical to local `main` — the remote's own
  answer rather than a cached tracking ref or the transcript of the push.
- **What became public:** this session's whole arc — BL-57's P3 record and plan amendment, BL-59 and
  its correction, the Test 38 fixture decoupling, the `HANDOFFS.md` trim to one receipt with its
  shard and proof, the density recalibration, and three receipt corrections.
- **Still on no remote:** branch `bl57/changelog-rules` at `18962a9`, which carries P3's four
  commits. Backing it up is its own go-ahead and was not given here.
- **Commit/PR:** the push itself left no commit; this entry is its record
- **Session:** S172 · **Verified:** `git rev-list --count origin/main..main` = 0 after the fetch;
  `ls-remote` sha matches local `main` exactly.
- **Model:** Claude Opus 5

### 2026-09-16 · [ad hoc] S172 follow-up — the receipt's `NOT EXERCISED` list still named the retention trim

- **What was wrong:** S172's `runtime_smoke` listed *"the `HANDOFFS.md` retention trim"* among the
  things the session did not exercise. True when written; false from `1ec509d` onward, and this is
  the one receipt the next session reads in full.
- **Change:** the trim moves out of that list into an `EXERCISED AFTER CLOSE-OUT, NOT AT IT` clause
  naming its commit. The distinction is kept rather than erased: the trim was operator-directed
  follow-up, not part of the close-out the receipt attests to.
- **This is the third stale claim this session's own receipt has needed correcting** — the unpushed
  commit count, `next_steps` item (2), and now this. All three share a shape: a receipt states the
  world as of close-out, and work continued afterwards. The first was fixed by naming a command
  instead of a number; these two could not be, because they are statements about what happened.
- **Commit/PR:** this commit
- **Session:** S172 · **Verified:** `bin/check-handoff --all` exit 0 (1 receipt).
- **Model:** Claude Opus 5

### 2026-09-16 · [BL-59] S172 — `HANDOFFS.md`'s token density re-measured after the trim; the budget row goes green

- **Change:** `.context-budget.json`'s `HANDOFFS.md` entry moves from `bytes_per_token` **2.3648**
  (measured 2026-08-29 at **186,617 B**) to **2.2657** (measured today at **20,310 B**). The tool
  itself asked: after the trim it reported *"density ... was measured at 186,617 B; the file is now
  20,310 B (89% drift). The token figure above is provisional — re-measure before trusting it."*
- **Measured, not derived.** The quadrupled-file Read refused at **35,857 tokens**, so the live file
  is **8,964.25 tokens** at 20,310 B. The stale density would have reported 8,588 — under-reporting by
  376 tokens, about 4.4%. Neither figure changes the verdict against a 25,000-token ceiling, so this
  is precision, not rescue.
- **The row is now `ok`.** At Phase 0 it read **over by 2,446 tokens**; it is green on both arms.
  Learning #60 is why this was worth doing now rather than later: a density is a snapshot of the
  content a file held when measured, and this file's composition changed character completely — one
  receipt plus front matter, where front matter is now 35% of it.
- **Two mistakes on the way in, both caught by asserts rather than by the diff.** A first patch
  assumed six-space JSON indentation and matched nothing (the file uses three); the replacement then
  had to key on line numbers because `"measured_on": "2026-08-29"` appears three times, once per
  budgeted file. A pattern edit would have rewritten the wrong entry silently.
- **Commit/PR:** this commit
- **Session:** S172 · **Verified:** `context_budget.py --status` reports `HANDOFFS.md ... ok`; the
  config re-parses as JSON and the parsed entry is asserted to carry the new values.
- **Model:** Claude Opus 5

### 2026-09-16 · [BL-59] S172 — `HANDOFFS.md` retention is now N=1: the fold, the policy, and a header reserve that is spent

- **Change:** the trim's pointer block is folded into the archive table as one row — in its own
  commit, because inside the trim commit the shipped `.verify.sh` fails L2 (Learning #58). The
  retention paragraph now states **N=1, replacing S127's N=4**, with the measurement it rests on and
  the reason `--force` is warranted rather than an override. The live ledger holds **one receipt**,
  20,820 B against 75,185 B before.
- **The retained receipt was corrected in place.** Its `next_steps` item (2) said this file held
  *"seven receipts against a retention policy of four"* — false the moment the trim landed, and it is
  the one receipt the next session reads. It now records what happened, including the test fix N=1
  required. Precedent for correcting a receipt in a follow-up rather than editing history: `1d88eaa`.
- **A consequence the decision did not anticipate, and it is now the binding constraint.** **N=1
  means a trim EVERY session** — each close-out prepends a receipt, so the steady state is exceeded
  immediately. Each trim-and-fold adds one archive-table row, about **147 B** of the **7,168 B**
  header reserve `bin/tests.sh` Test 39 (A2) asserts on this front matter. After this fold the front
  matter is **7,107 B — 61 B of room, which is room for none.** The next trimming session must
  shorten it first; folding the archive table into a shard index of its own is the obvious cut, and
  it is recorded in BL-59 rather than left to be rediscovered.
- **Three passes were needed to write that warning, which is the finding in miniature:** every
  version long enough to explain the problem was long enough to cause it — the first pushed the front
  matter to 7,718 B (over by 550), the second to 7,220 B (over by 52). The reasoning moved to BL-59
  and the instruction stayed here, which is the same move §The Action Ledger prescribes for a rule
  that outgrows the file it is stated in.
- **Commit/PR:** this commit; the trim is `1ec509d`, the test fix `d13a165`
- **Session:** S172 · **Verified:** `bash bin/tests.sh` exit 0 — **300 passed, 0 failed, 6 skipped**;
  the six are Test 34's stated BL-40 rows, which want three receipts, and Test 38 no longer degrades
  because `d13a165` decoupled it. `bin/check-handoff --all` exit 0 (1 receipt); `bin/check-links`
  exit 0; the shard's `.verify.sh` exit 0 both before and after the trim commit.
- **Model:** Claude Opus 5

### 2026-09-16 · [BL-59] S172 — Test 38 reads a frozen fixture instead of the live ledger, and a drift guard keeps the fixture honest

- **Change:** `bin/tests.sh` Test 38 sourced its fixture from the live root `HANDOFFS.md`, which made
  its inputs a function of a **retention policy**: at one retained receipt the copy exits
  `FIXTURE SOURCE TOO SHORT` and all thirteen assertions error with *"handoff file not found"* — 14
  failures, measured. It now reads **`tools/fixtures/handoff-ledger-2-records.md`** (2,985 B), a
  frozen two-record ledger: one record to pad past the 12,288 B per-record budget so assertion (4)
  is armed, one to be the subject of every other assertion. The three comments that asserted the old
  provenance (*"the fixture is a copy of the live ledger"*) are corrected rather than left standing.
- **The live half was kept, because a frozen fixture cannot notice the format moving.** New
  assertion **(8)**, a drift guard: it reads the **live** ledger's newest receipt and the fixture's,
  and fails if the live one carries a field the fixture lacks. **Mutation-tested in both directions
  before it was trusted** — deleting `gotchas` from the fixture reports `gotchas`; deleting two
  reports both; adding a key to a live receipt reports that key; the unmutated control reports `OK`.
- **Why a split and not a move:** the budget assertions want a population the test controls; the
  format check wants the real artifact. Each now runs against the one it needs.
- **Fork-local, verified rather than assumed.** Test 38 does not exist upstream — `grep -q` on the
  branch's `bin/tests.sh` exits 1 while fork `main` exits 0, read bare — and neither `tools/` nor
  `bin/tests.sh` has a row in `bin/_manifest.py` (both appear there only inside comments, which is
  why a bare `grep -c` on the filename answers the wrong question). No adopter receives either.
- **Commit/PR:** this commit
- **Session:** S172 · **Verified:** `bash bin/tests.sh` exit 0 — **306 passed, 0 failed, 0 skipped**,
  against a 305/0/0 baseline; the one added test is the drift guard. `bin/check-handoff --file
  tools/fixtures/handoff-ledger-2-records.md --allow-pending` reports OK and
  `record budget: 0 unwritten record(s), 0 over 12,288 B` — the two strings Test 38's control greps.
- **Model:** Claude Opus 5

### 2026-09-16 · [BL-59] S172 follow-up — the operator decides N=1; measured, the reachable floor is 2, and BL-59's first draft was wrong about why

- **Decision recorded:** the operator set `HANDOFFS.md` retention to **1**. **Nothing was trimmed** —
  executing it was tried in a throwaway clone first, and the result sends the decision back.
- **What the experiment found, run rather than predicted.** Baseline 7 receipts: `bin/tests.sh`
  exit 0, 305 passed / 0 failed / 0 skipped. At **`--cut 1`: exit 1, 285 passed, 14 failed**, 6
  skipped. At **`--cut 2`: exit 1, 298 passed, 1 failed**, 6 skipped — and **after the fold the
  prescribed next step, exit 0, 299 passed, 0 failed, 6 skipped.**
- **BL-59's first draft was wrong and is corrected.** It said the only cost below three receipts was
  six stated `SKIP` rows, *"never a failure."* **The real floor is Test 38, which this item had not
  mentioned at all:** it copies the live ledger into a temp fixture and exits
  `FIXTURE SOURCE TOO SHORT: need >= 2 records, found 1` (`bin/tests.sh:2752`), after which 13
  assertions error with *"handoff file not found"*. Test 34's six skips are the tolerable part.
- **A second constraint binds at any depth.** Test 39's A2 gives the live front matter a 7,168 B
  reserve; a trim's ~448 B pointer block takes it to 7,440 B (**over by 272**) and the fold replaces
  that block with one table row at **7,139 B (under by 29)** — measured, and the fold must be its own
  commit (Learning #58). **29 B of headroom means the trim after this one overflows the reserve**,
  which S169 predicted and which argues for cutting deep once rather than shallow repeatedly.
- **The `--force` warrant, checked rather than assumed:** `--check` reports SRF 2.0244 (RED), but
  §11.1 of the SRF adjudication proves **every on-schedule retention trim is refused for any file at
  any depth** — the refusal votes with the most recent archive, an unratified addition on top of H3.
  H3 as written votes with the largest single drop, printed in the same report: **0.1016**, deep green.
- **Measured cost:** `--cut 1` takes the live file 75,185 → 20,820 B with the repo net **+17,014 B
  (1.226×)** — far cheaper per byte relieved than S171's trim-to-four estimate, because the ~16 KB
  proof is a fixed cost. `--cut 2` takes it to 30,760 B. L1/L2/L3 OK; the emitted `.verify.sh` exits 0.
- **Also confirmed by running it:** `bin/model-report` opens the live ledger **and every archived
  `HANDOFFS-*` shard**, and today finds **0 matched lines in the live file** against matches in ten
  shards — so the one consumer of historical receipt content already reads the archives, not the
  live file. Archiving costs it nothing, which was the load-bearing claim under the whole decision.
- **Commit/PR:** this commit
- **Session:** S172 · **Verified:** all four suite runs in a `--no-local` clone whose HEAD sha was
  asserted equal to the working tree's (`dd18114`); `bin/check-handoff --all` exit 0 throughout.
- **Model:** Claude Opus 5

### 2026-09-16 · [ad hoc] S172 follow-up — BL-59 raised on the operator's question: does `HANDOFFS.md` need to keep four receipts?

- **Change:** BL-59 raised in `docs/planning/BACKLOG-DETAIL.md` with an index row in
  `docs/planning/BACKLOG.md`. The operator asked why the receipt ledger grows when the handoff is
  only used between two sessions, and whether `CHANGELOG.md` or `BACKLOG.md` could take the proof
  half. **The premise holds:** the file does two jobs with opposite retention needs — the *handoff*,
  done by the newest receipt alone, and the *proof*, which is what makes it append-only.
- **All five consumers were checked rather than assumed.** Only `bin/model-report` reads the content
  of a receipt below the newest, and it discovers archive shards by glob (`bin/model-report:158`), so
  archiving costs it nothing; `bin/check-handoff --archived` validates a frozen shard, so the
  integrity scope survives too. **Nothing requires an old receipt to be in the live file.** The
  number is an operator decision, as the file's own front matter says, and the S127 warrant
  (`docs/archive/CHANGELOG-through-2026-09-02.md:2070`) justifies the trim, never the four.
- **Measured at this session's close-out:** 75,185 B across 7 receipts — front matter 9.3%, the
  newest receipt 17.8%, **spent receipts 72.9%** — and **6,793 tokens over the 25,000-token ceiling**.
  S171 costed the same decision in bytes alone, where it read as a preference; in tokens it is a
  red gate.
- **The second question answered in the item:** `BACKLOG.md` cannot take the proof job at all (it
  holds open work only, and completion *removes* an item). `CHANGELOG.md` already carries the
  *occurrence* proof and the duplication is real — but it cannot carry the `pending`→`complete` crash
  breadcrumb (the only one this repo has, having no `SESSION_NOTES.md`), the 13-key schema that makes
  the six Minimum Handoff Requirements checkable, or per-session granularity. So it proves close-out
  *happened*, never that the handoff was *complete*.
- **One citation in the item was wrong and was corrected before commit.** The fixture precedent
  `tools/fixtures/seed-CHANGELOG-ledger-format-1.md` was cited as present; `git rev-parse` finds it on
  branch `bl57/changelog-rules` only, on neither fork `main` nor `upstream/main`. The item now says so.
- **Nothing was decided and nothing distributed was touched** — the retention number, Test 34's
  fixture split and a retention mode for `methodology_trim.py` are all left to the operator, and the
  last is a distributed change needing its own go-ahead.
- **Commit/PR:** this commit
- **Session:** S172 · **Verified:** every cited destination re-read on the ref the item claims it on;
  `bin/check-handoff --all` exit 0 (7 receipts); fork-only files, no distributed file changed.
- **Model:** Claude Opus 5

### 2026-09-16 · [ad hoc] S172 follow-up — the unpushed-commit count replaced by the command that produces it

- **Why the previous entry did not settle it:** the correction from 17 to 18 was committed, and that
  commit made the answer 19. **A count of unpushed commits cannot be written into a file inside the
  repository it counts** — recording it is itself one of the commits, so every fix falsifies the
  figure it just wrote. Two sessions' worth of this is avoidable in one line.
- **Change:** the receipt's carried item now names the command,
  `git rev-list --count origin/main..main`, instead of a number, and says why. This is
  §The Action Ledger's own advice — *replace a hand-maintained count with the command that produces
  it* — applied to the file that advises it.
- **Commit/PR:** this commit
- **Session:** S172 · **Verified:** `bin/check-handoff --all` exit 0, 7 receipts; the receipt now
  contains no commit-count figure (`grep -c 'commits ahead of' HANDOFFS.md` finds none in S172's block).
- **Model:** Claude Opus 5

### 2026-09-16 · [ad hoc] S172 follow-up — the receipt's unpushed-commit count corrected, 17 to 18

- **What was wrong:** S172's receipt gave fork `main` as *"17 commits ahead of `origin/main`"* under
  its carried go-ahead items. The figure was computed before the close-out commit and stated without
  the qualifier that would have made it true, so as a description of the tree the next session finds
  it is short by one. Measured after the close-out: `git rev-list --count origin/main..main` = **18**.
- **Change:** the receipt now reads 18 and says when it was counted. Nothing else in the receipt
  moved. Precedent for correcting a receipt in a follow-up commit rather than in place: `1d88eaa`.
- **Commit/PR:** this commit
- **Session:** S172 · **Verified:** `git rev-list --count origin/main..main` re-run after this commit
  is staged returns 18; `bin/check-handoff --all` exit 0, 7 receipts.
- **Model:** Claude Opus 5

### 2026-09-16 · [BL-57] S172 close-out — P3 done, the size rule now in tokens, and a measurement three handoffs called outstanding was already taken

- **Change:** S172's receipt is completed in `HANDOFFS.md` (self 8/10, predecessor S171 8/10). The
  deliverable was BL-57's P3 on branch `bl57/changelog-rules` — four commits, not pushed — plus the
  plan amendment on fork `main` that discharges S169's instruction to restate P3's and P4's runner
  criteria in tokens.
- **The restated criterion caught its own session.** The first edit measured **+9 tokens** against a
  rule this session had just rewritten. The fix went into the edit, not the rule: two clauses
  duplicated elsewhere on the same step came out, and the runner ended **32 B and 14 tokens under
  where P3 started**. A session that restates the gate binding it is grading its own paper, and the
  only defence is to take the measurement afterwards and let it fail.
- **`b82dcff`, `upstream/main` and P3's start are one blob (`c0550acd`).** So S169's recorded control
  *"`main`'s runner 36,955"* **was** the baseline the last three handoffs each carried forward as an
  unmeasured item. Two `git rev-parse` calls closed it.
- **Two figures the plan said would be findings if they moved, both explained to the entry that
  caused them.** Four of six adopters reproduce §4.4 exactly; `airqino` 1→2 and `mts-system` 96→262
  each gained one entry dated 2026-09-15. This repo reads **556** against §4.4's 494 — and **494 is
  exactly the count of entries dated on or before 2026-09-14**, §4.4's measurement date, so the
  twelfth shard S171 wrote moved nothing out of the audit's reach. Conservation measured, not assumed.
- **One defect was found in this session's own text, at close-out, and corrected on the branch
  (`18962a9`).** §The Action Ledger attributed the *78 against 64* count to *"this framework's own
  ledger"* — but that comparison was run on the project whose ledger was split at v3.6, and the tree
  the sentence now ships in records none of it. Every gate passed it; a grep for the figure's
  provenance did not. The sentence leads with the mechanism now and names the figure for what it is.
- **No learning row, deliberately.** The candidate rule is already carried by rows #46 and #60, and
  `starter-kit/FRAMEWORK_LEARNINGS.md` is 79,483 of 81,920 B with about two rows left under BL-53's
  unresolved retirement policy.
- **`HANDOFFS.md` now holds seven receipts against a retention policy of four,** and the decision
  S171 deferred is sharper in tokens than in bytes: `context_budget.py --status` reports it
  **≈27,446 tokens against a 25,000-token ceiling, over by 2,446.** Cutting to four removes 26,140 B
  of body, leaving ≈16,393 tokens — red to 8,600 tokens of headroom. Still the operator's call.
- **Commit/PR:** this commit (fork `main`)
- **Session:** S172 · **Verified:** in `--no-local` clones with HEAD shas asserted — branch `cf20a3b`
  and again `18962a9`, `bin/tests.sh` **118/0**, `check-links` 0 (**108** links, 107 at `775ba23`),
  budget 0, `grep -F '[BL-<N>]'` exit 1 over all seven files; fork `main`
  `44a1e20` `bin/tests.sh` **305 passed / 0 failed / 0 skipped**, `check-links` 0, `check-learnings` 0,
  `check-handoff --all` 0, budget exit 2 with **0 status flips** against the Phase 0 reading.
- **Model:** Claude Opus 5

### 2026-09-16 · [BL-57] S172 — BL-57's P3 done on branch `bl57/changelog-rules` (3 commits, not pushed); the plan amended and its size rule restated in tokens

- **Change:** P3 ran on the branch as it stood — upstream PR #82 was re-checked at Phase 0 and is
  still OPEN at `c84e7d96`, so S169's merge-first amendment did not trigger. Branch commits:
  `d771439` rewrites `FRAMEWORK_APPARATUS.md` §The Action Ledger's source-tag vocabulary to
  `[BL-<id>]` and replaces the one-line audit with the anchored, shard-reading, `git ls-files` form;
  `e47ca14` drops the runner's inline audit grep at `:39` for a link to that section and moves
  `:278`, `:329`, `ITERATIVE_METHODOLOGY.md:294` and `.githooks/pre-commit:57` to `[BL-<id>]`;
  `cf20a3b` replaces the `HANDOFFS.md` seed's bare glob with `git ls-files` — the bullet P2 left to
  P3. On fork `main`: this entry, the plan's S172 amendment and BL-57's backlog row.
- **S169's amendment is discharged.** P3's and P4's runner criteria were written in bytes; both are
  now in tokens at `docs/planning/changelog-rules-contradictions-plan.md`. **The measurement came
  first and its instrument was checked first:** both published controls reproduced exactly — the
  runner doubled to **36,955** (18,477.5 tokens) and the Phase 0 pair to **48,555** (24,277.5), the
  figures S169 recorded, on the same blob `c0550acd` that is both P3's start and `b82dcff`'s file.
- **The two units disagreed, which is the point.** The link plus the id changes measured **+36 B but
  only +9 tokens** — a path runs near 4 B/token where the runner averages 2.8248. Two duplicate
  clauses on the same step then came out (the step already showed `[ad hoc]` in its own template;
  the note's closing paragraph already forbids the backfill becoming the deliverable), leaving the
  runner at **52,163 B / 18,463.5 tokens — 32 B and 14 tokens under where P3 started**, and the pair
  at 24,263.5 of the 25,000-token read cap.
- **Every DONE criterion was run, not predicted.** `grep -F '[BL-<N>]'` over the runner, the flight
  manual, `HOW_TO_USE.md`, the hook, §The Action Ledger and both seeds exits 1 (no matches). The
  audit returns the same number in zsh and bash on the branch (57, equal to its heading count), on
  this repo (556) and on all six adopters. In a throwaway repository with one entry and no shard the
  **bare glob makes the two shells disagree — zsh prints 0, bash prints 1** — while the `git ls-files`
  form prints 1 and exits 0 in both; that is the failure the fix removes, and it is a wrong number
  rather than a visible error.
- **Two §4.4 figures moved and both are explained.** Four of six adopters reproduce exactly;
  `airqino` 1→2 and `mts-system` 96→262 each gained one entry dated 2026-09-15. This repo reads 556
  against §4.4's 494 — and **494 is exactly the count of entries dated on or before 2026-09-14**, its
  measurement date, so S171's 12th shard moved nothing out of the audit's reach. Widening
  `BL-[0-9]+` to `BL-[^]]+` recovers **362 logged actions** across three adopters.
- **Commit/PR:** this commit (fork `main`); branch `d771439` + `e47ca14` + `cf20a3b`
- **Session:** S172 · **Verified:** in a `--no-local` clone whose HEAD sha was asserted equal to the
  worktree's (`cf20a3b` both sides), `bin/tests.sh` **118 passed / 0 failed**, `bin/check-links` 0
  (**108** links, 23 files — 107 at `775ba23`, the one link P3 added), `context_budget.py --status` 0.
- **Model:** Claude Opus 5

### 2026-09-16 · [BL-57] S172 claim — BL-57's P3: source tags and the audit, on the branch

**Deliverable:** BL-57's **P3** (`docs/planning/changelog-rules-contradictions-plan.md:490`) on branch
`bl57/changelog-rules` (worktree `../methodology-bl57`, at `775ba238`): `[BL-<N>]` becomes `[BL-<id>]`,
and the source-tag audit becomes the shard-reading form that gives the same count in zsh and bash — in
`FRAMEWORK_APPARATUS.md` §The Action Ledger, `starter-kit/SESSION_RUNNER.md` (`:39`, `:278`, `:329`),
`ITERATIVE_METHODOLOGY.md:294` and `.githooks/pre-commit:57`.

- **Upstream PR #82 is still OPEN at `c84e7d96`**, re-checked at Phase 0 rather than assumed, so S169's
  merge-first amendment does **not** trigger: P3 starts on the branch as it stands.
- **Two carried items ride with P3.** P2 found that the `HANDOFFS.md` seed still publishes a bare glob
  zsh refuses where no shard exists — C10's class, outside P2's lines, assigned to P3. And S169's
  amendment holds: P3's runner criterion (`:508`) and P4's (`:538`) are written in **bytes** and must be
  restated in **tokens**. That measurement has not been taken, so it comes first.
- **Riding with this claim:** the Phase 0 `dashboard_history.jsonl` and `.context-budget-history.jsonl`
  snapshots, both appended by mandatory Phase 0 instrument runs. They are recorded here and committed
  with this entry rather than left for a later `--no-verify` — S171's finding, applied at the one point
  in the session where it costs nothing.

**Ledger:** `CHANGELOG: pending` — the crash breadcrumb until Phase 3F.

### 2026-09-16 · [ad hoc] S171 follow-up — the append-only `.context-budget-history.jsonl`, dirtied by Phase 3E

A bare `context_budget.py --status` appends to its own run history, so Phase 3E left the file modified
after the close-out commit. Recorded here and committed with this entry rather than with `--no-verify`:
this session's one finding was that an unrecorded housekeeping commit is a debt the next frontier-advancing
action makes permanent, and leaving one behind in the close-out would be the same mistake twice.

### 2026-09-16 · [ad hoc] S171 close-out — `CHANGELOG.md` readable again, measured as a transfer and not a saving

- **Change:** S171's receipt is completed in `HANDOFFS.md` (self 7/10, predecessor S170 9/10). The session
  did two things on the operator's instruction: trimmed this file under approved `--force` (the tool's own
  entry below) and raised **BL-58** (the entry below that). **The trim's net was projected before the run
  and measured after: +17,928 B projected, +18,138 B actual (1.102×)** — relief 178,162 B against
  196,300 B written, so the repository grew while the read path shrank, and this ledger says so rather
  than crediting a saving. `docs/archive/` is now **42.8% of the tracked repo**, inside no ceiling.
  **The benefit is exactly one thing and is not the context budget:** `CHANGELOG.md` is a deliberate
  exclusion from the read-set, so `context_budget.py --status` is byte-for-byte unmoved by the trim
  (69,749 B, `over`, exit 2) — what changed is that a default `Read` returned **zero content** before and
  the front matter plus the newest ~51% with an announced `PARTIAL view` banner after. The file's own
  rate rule moved **−67 → +33 entries of headroom**, clearing its published *"back above 30"* stop.
- **Found, and self-inflicted:** the `chore(history)` commit `c01854f` was made `--no-verify` **before**
  the trim and tripped the trimmer's `P1_UNDOCUMENTED` guard. The guard is right — a trim advances
  `git log -1 --format=%H -- CHANGELOG.md`, so the commit would have been unrecoverable by Phase 0
  reconcile — and the usual discharge, naming such a commit in the close-out entry, comes too late.
  `f2840fc` records it instead. **S152's trim put its `chore(history)` after the trim; that precedent had
  been read minutes earlier.**
- **Not done, deliberately and with a number:** `HANDOFFS.md` holds **six** receipts against its retention
  policy of four. Its byte trigger does not fire (54,177 B of 196,608), so a retention trim would relieve
  ~18 KB and write a fixed ~16 KB proof — **roughly 1.9× net-additive**, the expensive end of the curve
  measured today. That is an operator decision, not Phase 0 housekeeping, and S172 should put it as one.
- **No learning row.** `starter-kit/FRAMEWORK_LEARNINGS.md` is 79,483 of 81,920 B with about two rows
  left and **BL-53's retirement policy still open**; the transferable content of this session is recorded
  in BL-58's eight hazards, where it is useful to adopters rather than competing for the last rows.
- **Commit/PR:** this commit (claim `ff29a8d`, history `c01854f`, reconcile `f2840fc`, trim `101fa78`,
  BL-58 `1c4e941`)
- **Session:** S171 · **Verified:** in a `--no-local` clone with HEAD asserted equal (`1c4e941` both
  sides), `bin/tests.sh` **305 passed / 0 failed / 0 skipped**, matching the S168–S170 controls; dashboard
  321 OK, trimmer 123 OK, budget 116 OK; `check-links` 0, `check-learnings` 0, `check-handoff --all` 0
  read bare; `context_budget.py --status` exit 2 with 0 status flips against the Phase 0 reading and
  exactly two rows moved, both by this session's own writes; the shard's `.verify.sh` exit 0 twice, before
  and after the trim commit. **The suite run was reported by the harness as exit 1; the chain's own
  echoed code was `tests.sh exit=0` and the 1 belonged to a trailing `grep -c` matching zero SKIP lines.**
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] S171 — BL-58 raised on the operator's request: should adopters be told how to trim a ledger losslessly?

**Change:** `docs/planning/BACKLOG.md` gains the index row and open-list entry; the body is in
`BACKLOG-DETAIL.md` under `<a id="bl-58"></a>`. **The gap is measured, not asserted:** `bin/_manifest.py`
installs `methodology_trim.py` at every adopter root as a **tracked** file, while `grep -ciE 'trim'`
returns **0** for `starter-kit/SESSION_RUNNER.md`, `FRAMEWORK_APPARATUS.md` and `starter-kit/SAFEGUARDS.md`
— so the only real instructions sit in the two **seeds** `bin/sync` never overwrites once they exist, and
the one file every session reads says nothing. The item lists eight operating hazards, **four of them hit
by this session**: the tool stages nothing (commit with `-a` and the shard never enters history);
`P1_UNDOCUMENTED` demands the reconcile happen *before* the trim, because the usual discharge — naming a
`--no-verify` commit at close-out — comes too late; the proof reads differently either side of the commit;
and `SRF_RED` is a property of the rule, not of the file. It is framed as a **decision first**, with three
uncosted shapes: the tracked apparatus beside BL-57's P2 section, a procedure in the runner (expensive —
the runner is 54,363 B against a 41,364 B declared ceiling), or better output from the tool itself.
**One stale figure was caught before it was published:** the *"net +144,239 B across ten archive events"*
accounting is S124's and covers only the first ten, so the entry attributes it and says to re-derive rather
than quote it.

- **Commit/PR:** this commit
- **Session:** S171 · **Verified:** the disposition and install path read from `bin/_manifest.py`
  directly; each `grep -ciE 'trim'` count run per file; the proof-cost percentages and the 40.6%
  archive share re-measured this session
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-09-14.md` (65 record(s), 276,657 B → 98,495 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **65** record(s) (2026-09-02 → 2026-09-14) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-09-14.md`](docs/archive/CHANGELOG-through-2026-09-14.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-09-14.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-14.md.verify.sh)
rather than trusting a digest printed here. Live file 276,657 B → 98,495 B (−64.4%).

### 2026-09-16 · [ad hoc] S171 — `c01854f` recorded before the trim advances the ledger frontier

A `chore(history)` commit for the two append-only `.jsonl` run series that Phase 0's dashboard and
`context_budget.py` runs appended to. It was committed `--no-verify` and so carried no ledger line of
its own, which past sessions have discharged by naming such commits in the close-out entry instead.
**That is not available here:** `methodology_trim.py`'s `P1_UNDOCUMENTED` guard refused the trim while
it stood unrecorded, and the refusal is right — a trim commit advances `git log -1 -- CHANGELOG.md`,
so `<frontier>..HEAD` would never contain `c01854f` again and Phase 0 reconcile could not recover it.
Recorded here, before the trim, rather than at close-out after it.

### 2026-09-16 · [ad hoc] S171 claim — trim `CHANGELOG.md` back under the hard read refusal, on operator go-ahead

**Deliverable:** one trim of this file, authorized by the operator at Phase 1 after the benefit and the
cost were put to him measured. **The file is 274,805 B against the 262,144 B refusal, confirmed
empirically rather than from the constant** — a default `Read` returns `File content (268.4KB) exceeds
maximum allowed size (256KB)`, zero content, front matter included. `methodology_trim.py --check` reports
the byte trigger FIRES and `SRF_RED 1.0306`, so the trim needs `--force`; the warrant is the governing
adjudication's own self-limitation to *"the middle regime, between the 25,000-token cap and the 256 KiB
refusal"*, the regime this file has now left — the same warrant as S132's and S152's forces, and no
precedent for any other file. **A second, smaller action rides with it:** a backlog item asking whether
adopters should be told how to trim a ledger losslessly. **Ledger:** `CHANGELOG: pending` — the crash
breadcrumb until Phase 3F.

### 2026-09-16 · [ad hoc] PR #82 merged — post-merge verification on main and the first tightening

- **Action:** the operator merged [PR #82](https://github.com/KJ5HST/methodology/pull/82) (quality ratchet,
  plan #81 Phases 1–4 + the review-response fixes) at merge commit `64f23bf` (2026-09-16T18:05:47Z; parents
  `0fd003a` + `5c9d3b4`). Session S23 verifies `main` and takes the tightening the S22 receipt records as
  owed: `tests-sh-failed` 1 → 0 and `tests-sh-passed` 138 → 139, Test 9 turning green on `main`. Local
  `feat/quality-ratchet` deleted (merged; the remote branch was already gone). Results appended at close-out.
- **Verified on `main` at `64f23bf`:** `bin/tests.sh` **139/0** — Test 9 green for the first time since the
  branch was cut; dashboard unit 226 OK, budget 118 OK (2 skipped), trimmer 123 OK (2 skipped), ratchet 45
  OK, `check-links` OK, `check-learnings` OK, `check-handoff --all` OK, twins byte-identical at 2.11.1,
  `context_budget.py --status` exit 0, `quality_ratchet.py --selftest` OK (22), `commit-msg --selftest` OK.
- **The first tightening, discharged:** `tests-sh-failed` `max 1 → 0`, `tests-sh-passed` `min 138 → 139`;
  the hook's verdict on the staged edit exit 0 (two tightenings). `--run` at the tightened manifest:
  **10/10 pass · 0 fail · 0 unmeasured · results `6542e640a956` · manifest `97a7aab85b9a`** (2 m 50 s).
  `_first_tightening_owed` in the manifest now records the discharge and the standing rule: raise floors
  when a measurement rises, never lower them.
- Session S23: claim `b4c04af` + tightening `fb81c4b` + the close-out commit (receipt complete, cites the run).
  The ledger hook refused the first close-out attempt — `CHANGELOG.md` was not co-staged — as designed.

### 2026-09-16 · [ad hoc] PR #82 review-response fixes — the six corrections and the review's accepted findings, one checkpoint per fix

- **Action:** the fix set the maintainer's confirmation comment promised, built on `feat/quality-ratchet`
  after merging `main` (`b2aea23`, ledger union). Operator-directed bundling across subsystems (the S8
  shape), one independently verified checkpoint commit per fix. Session S22: merge `b2aea23`, claim `563a6e2`,
  seven checkpoints `b742344`..`b5dda4e`, the close-out commit. PR head `b5dda4e` + close-out; NOT merged.
- Merge `b2aea23`: `origin/main` (S21) into the branch; `CHANGELOG.md` and `HANDOFFS.md` resolved as a union.
- **F1 — the deletion hole** (review 2a + 4, bullets 1 and 4): `quality_ratchet.py` 1.0.0 → 1.1.0. `find_root`
  falls back to the git toplevel, so `--precommit` can judge a commit that removes the manifest instead of
  exiting 3 "refuses to invent thresholds" (the exit that, in the hook `install-hook` writes, refused every
  later commit). The comparison base is now the **newest parseable committed manifest that declares a
  gate** — not HEAD's copy — so removing the manifest is refused as the loosest loosening, re-adding it
  lower after a bypassed removal is still refused against the removed version, and a corrupted or emptied
  HEAD copy is skipped; a branch that removed its manifest and left it removed is not locked. The
  empty-gates rule was found by the test, not the review: the first cut used "newest parseable" and a
  bypassed `{"gates": []}` became a base that let a lower re-declaration through. `install-hook` writes
  the path of the copy that is running (`starter-kit/quality_ratchet.py` here, root for adopters).
  `.githooks/pre-commit` fires when the worktree OR HEAD has a manifest. Tests: unit 33 → 43 (8 RED
  first, 2 controls), selftest 17 → 22, `bin/tests.sh` +4 through real git (one RED on the old tool: the
  lockout) — and the pre-existing `git checkout -- manifest` in that block restored the worktree from a
  still-staged refused edit; now `checkout HEAD --`.
- **F1b** — the F1 base note fired on every ordinary commit ("HEAD has none") because `git log -- manifest`
  names the newest commit that *touched* the file, not HEAD; seen in the F1 checkpoint's own hook output.
  The note now prints only when HEAD's copy is absent, unparseable, or empty. Unit 43 → 44 (RED first).
- **F2 — the dashboard** (review 2a fix 3 + O1, §4 bullets 2–3): `DASHBOARD_VERSION` 2.11.0 → 2.11.1, both
  twins. The history walk runs whenever the manifest *has* a history, not only when the worktree has the
  file — the early return made the deleted-and-never-re-added state report nothing; it now reports
  `manifest deleted in <sha>` with every gate that went with it. A deleted or unparseable version is
  recorded as an empty gate list (flagged), never skipped. Each version is compared to the nearest OLDER
  version that declared a gate — the base `quality_ratchet.py` now uses — so 80 → (deleted) → 1 reads
  as `floor lowered 80 → 1`, not "added". A direction flip is a loosening in its own right; a changed
  `command`/`extract` is a separate LOW advisory, as the bypass message promised. The +2 for a passing
  gate *named* coverage is dropped (`echo 100` earned it, from a gitignored file). Unit 222 → 226 (6 RED
  first, incl. the version pin); fleet delta 0 by construction — no sibling repo has a manifest history.
- **F3 — `tests-sh-failed` at `max 1`** (review 2b): declared now at the branch's measured value (Test 9 by
  construction), so a second failure is caught today; tightens to 0 in the first commit after merge.
  Manifest 9 → 10 gates (the ratchet's own verdict on the staged edit: "1 gate(s) added"). Because two
  gates now read one `bash bin/tests.sh`, `run_gates` memoizes identical commands within a run — the
  suite runs once, two numbers are read from it; a `--run` that took the suite twice is one nobody
  cites (unit 44 → 45, RED first).
- **F4 — the docs** (review 2c, §5, and the unraised merge/rebase skip): `SESSION_RUNNER.md` Phase 0 step 6
  gains the gate-citation check — the newest complete receipt's `quality_ratchet:` line against the results
  file, or a re-run — **paid for by reduction**: the step's HANDOFFS clause no longer restates the note eight
  lines below it, and step 5 loses an aside; measured by the doubled-file Read **18,897.5 → 18,865.5 tokens**
  (53,328 → 53,252 B), 34.5 under the 18,900 ceiling. `SAFEGUARDS.md` ratchet row: removing the manifest is
  refused; merge/rebase commits skip the hook and the dashboard's history read is the catch (16,765 → 17,024
  B, 6,029.7 tokens, 70 under 6,100; the pair 24,894.5 = 99.58 % of the cap). `ITERATIVE_METHODOLOGY.md`
  §Mechanical Gates states the enforcement point beside the "every actor" claim (opt-in hook, on-record
  bypass, merge skip; CI is what makes "every" literal). `BOOTSTRAP.md` Step 10: the manifest itself is
  ratcheted; the two limits stated plainly.
- **F5 — the budget config** (review §3 + O2): both read-set densities re-measured on the blobs they now
  describe — runner **2.8248 → 2.8227** on `2a3e410d` (53,252 B, 18,865.5 tokens), SAFEGUARDS **2.8191 →
  2.8234** on `933816b4` (17,024 B, 6,029.7) — each entry naming its blob and the rule: re-measure when
  `git rev-parse HEAD:<path>` changes; `measured_bytes` at 25 % drift is not a substitute. `CLAUDE.md`
  gains a **token ceiling, 23,483 at its measured 2.519 B/token** (blob `1244e95b`), the byte pin kept as
  the coarse backstop — the S20 reduction was −15 B and **+62 tokens**, which a byte pin cannot see. The
  tool now reports 23,482 / 18,865 / 6,029 against 23,483 / 18,900 / 6,100, within one token of the
  measurements. Not built: a `measured_blob` key the tool checks itself (follow-up).
- **F6 — tightened to measured** (the ratchet doing its job): `tests-sh-passed` 134 → 138, `dashboard-unit-tests`
  222 → 226, `ratchet-unit-tests` 33 → 45 — three tightenings, no approval needed, the hook's verdict on the
  staged edit exit 0. `--run`: **10/10 pass · 0 fail · 0 unmeasured · results `efccbc7f2195` · manifest
  `08423c179055`**, 2 m 46 s with `bin/tests.sh` executed once for its two gates.
- **Non-commit actions:** branch pushed at `b5dda4e`; PR #82 body replaced — rmsharp's §1 rewording as the
  description (facts updated: base = newest committed manifest with gates, ten gates, 2.11.1, the two
  limits), the decisions in plain words, a "Review findings and what changed" section (read back: 9,876
  chars). **Learning #16** appended (1,137 B; 15 rows, `#14` reserved). `git merge-tree --write-tree
  --name-only origin/main feat/quality-ratchet` **exit 0 at this close-out** — clean, by exit code (S21's
  lesson). Not built, recorded: `measured_blob` self-check in the budget tool; the `context-budget` gate
  (history-file decision first); CI.

### 2026-09-16 · [ad hoc] Posted the maintainer's confirmation of the PR #82 review to the PR (non-commit action)

- **Action:** one maintainer comment on [PR #82](https://github.com/KJ5HST/methodology/pull/82) answering
  rmsharp's review comment of 2026-09-16: the review **reproduces** (its own repro script 7/7 sections, the
  four token figures by the doubled-file Read, the `--run` hash `74c773523dab` on a third tree; the §1
  rewording accurate on every checkable claim) — with six corrections from the internal check (oversight
  venue, 2026-09-16): fix 1 alone *refuses* a `git rm` via `find_root`'s exit 3, so `find_root` is the
  prerequisite; the dashboard fix never runs while the manifest stays deleted; "one new test offsets one
  failure" is false at the unit-suite level (one `tests.sh` check each); the receipt-vs-results comparison is
  specified in `starter-kit/HANDOFFS.md` §Citing the gate run, absent only from the runner's Phase 0
  procedure; the stale-density finding applies to `SAFEGUARDS.md` too; the proposed `context-budget` gate
  writes an un-ignored history file. Two items the review did not raise: merge/rebase commits skip the
  ratchet; an unparseable HEAD manifest is the delete/re-add hole with one `--no-verify`. Fixes are the
  next session's work, in the corrected order. Session S21: claim `07d166e` + the close-out commit.
  Comment: <https://github.com/KJ5HST/methodology/pull/82#issuecomment-5701463025> (read back via the API).
  S21's ledger prepends conflict with the branch's S20 prepends in this file and `HANDOFFS.md` (`git merge-tree`
  exit 1; clean against `8b4dc2c`) — resolve as a union on the PR branch before merge, the S15 precedent.

### 2026-09-15 · [ad hoc] S170 close-out — the learning row, the receipt, and what the post left open

**Deliverable posted and verified; this entry closes the session.** Phase 3C: **Learning #66 appended** —
*a remedy you cannot state in one unambiguous sentence is evidence you have not located the defect* —
`starter-kit/FRAMEWORK_LEARNINGS.md` 78,103 → 79,483 B against its 81,920 B ceiling (about two rows left).
Phase 3E, in a sha-verified `--no-local` clone at `40cf1a4`: `bin/tests.sh` **305 passed / 0 failed / 0
skipped**, matching S169's control; dashboard unit 321 OK, budget 116 OK (2 skipped, honestly), trimmer 123
OK; `check-links`, `check-learnings` and `check-handoff --all --allow-pending` all exit 0 read bare;
`context_budget.py --status` exits 2, fork `main` over its declared byte ceiling — pre-existing and by
design. **One instrument trap hit and recorded:** `check-learnings` reported *"65 rows, contiguous 1..65"*
after row #66 landed, which looked like the row had not registered; the parser was run directly and does
see it (65 rows, numbers ending 64, 65, 66). The summary prints `len(rows)` for BOTH numbers, so the
reserved `#14` makes the printed range understate the true maximum. **That is BL-44, raised at S109, not a
new finding** — found by searching the backlog before calling it one. Not fixed: it is not this session's
deliverable. **`CHANGELOG.md` has now crossed the 262,144 B single-Read refusal** — 271,613 B at this
entry, so it must be read with `offset`/`limit` from here. Not trimmed: the operator's decision.

### 2026-09-15 · [ad hoc] S170 — the comment POSTED to upstream PR #82 (non-commit action, operator go-ahead)

- **Action:** one comment posted to `KJ5HST/methodology` PR #82 on the operator's explicit go-ahead, via
  `gh api repos/KJ5HST/methodology/issues/82/comments -F body=@docs/planning/pr82-comment.md`.
- **Result:** comment id **5691623656**, by `rmsharp`, created `2026-09-16T03:31:57Z`,
  <https://github.com/KJ5HST/methodology/pull/82#issuecomment-5691623656>.
- **Read back before this was recorded, byte for byte:** the posted body was fetched again and compared to
  the local file — **sha256 `9d669dc6ee90ba312937453889cf701b2bbb37d83979dc946b6db96936179b30` on both**,
  `cmp` silent. The one-byte delta in a naive `wc -c` is the newline `jq` appends when printing, and the
  API's `len: 25612` is **characters**, not bytes: the body is 25,611 characters and **25,743 bytes**.
- **Pre-flight:** `upstream` re-fetched immediately before posting; #82 still OPEN at head `c84e7d96`,
  unmoved since the review, with 0 comments and 0 reviews — so every claim in the comment was still pinned
  to the tree it was measured on. Working tree clean at `40cf1a4`.
- **Content:** ten suggested changes, ranked — a proposed rewording of the PR's purpose, approach and
  mechanism; three ways the ratchet can still turn backwards; two file budgets denominated in bytes where
  tokens is the operative unit; four smaller defects; and one note on who the mechanism actually binds.
  4,286 words, every result from a run rather than from reading the code, with a reproduction script
  linked by permalink.

### 2026-09-15 · [ad hoc] S170 — the PR #82 comment states the links its facts rested on implicitly (not posted)

**Operator challenge at the Present gate:** *"How does '`_gate_loosenings` already has a removed branch, it
just never reaches it' relate to the empty gate set?"* — two facts set side by side with the causal link
left out. **The link, verified in the source before writing it:** `_gate_map` returns `{}` for a manifest
whose gate list is empty (`methodology_dashboard.py:1931`), and `_gate_loosenings` walks the OLDER version's
gates asking whether each name still exists in the newer, appending `"removed"` when it does not. So an
empty gate set is simply the input that makes *"every gate is missing"* true — and *"a gate is missing"* is
the one case the function already handles. Representing a deleted manifest as zero gates rather than as
unreadable therefore needs **no new detection logic**, only a different answer to *"what was the manifest at
that commit?"* **Audited the rest for the same fault — asserting two facts without their connective — and
fixed three more.** (1) The `install-hook` bullet asserted that a fresh clone has no `core.hooksPath` without
saying why that matters: `install_hook` (`quality_ratchet.py:333`) uses it to choose the hooks directory, so
with it set it finds `.githooks/pre-commit`, declines and prints a chain line, while unset it writes
`.git/hooks/pre-commit` — and `HOOK` (`:325`) execs `<root>/quality_ratchet.py`, the ADOPTER layout, which
does not exist in a repo that keeps the tool under `starter-kit/`. (2) The `CLAUDE.md` bullet gave "4,800
tokens of headroom" without naming what it is headroom under (the 25,000-token ceiling the tool derives for
that file). (3) The coverage bullet said the results file is gitignored without saying the consequence —
the number earning the points was written by whoever last ran the tool locally and no reviewer saw it.
4,002 → 4,286 words. **Still nothing posted.**

### 2026-09-15 · [ad hoc] S170 — the PR #82 comment's remedies made precise; one had the wrong cause (not posted)

**Operator challenge at the Present gate:** *"'run the hook whenever the manifest is tracked in HEAD, not
only when it is on disk' is not clear. What does 'run the hook' mean in this context?"* — it meant nothing
coherent. **The hook script always runs;** what is conditional is the line INSIDE it that calls the tool.
Re-read on the branch: `.githooks/pre-commit` guards on `[ -f "$top/.quality-gates.json" ]`, the WORKING
TREE file, while `precommit()` reads the INDEX (`blob_text(root, ":.quality-gates.json")` → `git cat-file -p
:<path>`). **Two independent doors, each on its own sufficient to wave a deletion past** — so the remedy is
now three numbered places with that dependency stated, rather than one run-on sentence. **Audited every
other remedy for the same fault, since the operator has now flagged it twice; two more failed.** The
lockout bullet named the WRONG CAUSE: it is not that the tool exits 3 on a missing manifest inside
`precommit()` — `find_root()` (`:61`) locates the project by walking up for `.quality-gates.json` ITSELF, so
with the file gone the tool never reaches `precommit()` at all and exits at `main()` (`:473`). The remedy is
therefore to find the root via `git rev-parse --show-toplevel`, as the chained hook already does. The
dashboard bullet said "report flips as loosenings" without saying where or why they are missed:
`_gate_loosenings` compares thresholds only after confirming both versions share a direction, so a flip
falls through both branches. 3,711 → 4002 words. **Still nothing posted.**

### 2026-09-15 · [ad hoc] S170 — the PR #82 comment drops a false contrast: not file vs judgment, but diffable vs not (not posted)

**Operator challenge at the Present gate, and it was fatal to the phrase:** *"Explain what is meant by 'put
the standard in a file instead of in a judgment.' Standard of what? What is the attribute of a standard
that is captured in a file that is not captured in a judgement? How do you preserve a judgment if not via
something stored in a file?"* — **the contrast was false, and the phrase was mine, not the PR's.** This
repository is judgments stored in files; storage was never the distinction. **Re-grounded in the PR's own
principle section** (`ITERATIVE_METHODOLOGY.md`, read on the branch rather than recalled): the thesis is
*"enforce quality on the artifact, not on the actor"*, and *"a more capable agent or a sharper adversarial
reviewer changes the JUDGE, not the CLASS of gate."* **Rewritten to say what a file actually adds, in two
parts:** (1) who evaluates it — a question the session asks itself is answered by whoever is running, and
the answer moves with care, haste and capability; (2) the part that matters here — **a judgment leaves no
record of how strict it was.** One session requiring 134 passing tests and the next settling for 120
changes no artifact, so there is nothing to compare and nothing to notice. A number in a committed file is
a versioned object with an author, a date and a diff. The distinction is **diffable vs not**, not stored vs
unstored: *"the handoff must be specific and actionable"* is stored in a file and still cannot reveal that
this session's "specific" was laxer than the last one's. Closing line, which is now the hinge of the whole
comment: **you can only refuse to let a standard slip if the standard is a thing that has a former self.**
3,520 → 3,711 words. **Still nothing posted.**

### 2026-09-15 · [ad hoc] S170 — the PR #82 comment states the ratchet's actual mechanism, and the findings reorganize around it (not posted)

**Operator question at the Present gate:** *"What is the mechanism that makes raising or lowering a gate's
number have an effect? What is the relationship to a gate and its number?"* — a gap in the rewording, not
in the code. **Answered from the source, verified before asserting:** a gate's number is a pass/fail
boundary whose meaning depends on its `direction` AND on its `command` (the quantity measured), and **two
parts of the system read it differently.** `--run` executes the command and applies the boundary
(`quality_ratchet.py:232`). `--precommit` — the ratchet — **runs no command at all** (`compare()`, `:134`,
docstring *"Pure; no git"*): it reads the staged manifest and `HEAD`'s and compares them field by field, so
the hook sees the EDIT, not its consequences. That is why it works without measuring anything, and it is
also the boundary of the guarantee, in the code's own warning string: **it holds thresholds, not
measurements** — a changed `command` can only warn, since the tool cannot know whether the new command is
easier without running both. **The comment reorganizes around that sentence:** §1 gains three paragraphs
(what the number does / at run time / at commit time / where the guarantee stops), and §2's three findings
stop being a list and become consequences of the one design choice — (a) a comparison with no second side,
(b) thresholds guarded perfectly over a quantity that cannot see failure, (c) the record of the run checked
only for shape. 3,188 → 3,516 words. **Still nothing posted.**

### 2026-09-15 · [ad hoc] S170 — the PR #82 comment recomposed for a reader who has not read the plan (not posted)

**Operator critique at the Present gate, acted on:** the draft assumed too much knowledge — *"Deleting the
manifest is the loosest possible loosening"* carried no meaning without context, `floor 5->4` was never
defined, and the PR's own gap (no understandable statement of purpose, approach and mechanism) was
described rather than remedied. **Recomposed, not patched:** the comment now opens with a proposed
rewording of the PR's purpose/approach/mechanism, offered as liftable text — it defines a quality gate, the
manifest, a loosening, and *why the thing is called a ratchet* (teeth that let the wheel turn one way and
catch it turning back) — and every later section uses only that vocabulary. The three ratchet findings are
reframed as *ways the pawl lifts off*, each with a step-by-step table in plain language (*"at least 5"* →
*"at least 1"* in two unrefused commits); the byte/token section gains the one-sentence setup a reader
needs for why file size is budgeted at all. 2,310 → 3,188 words, deliberately: the operator asked for
clarity, not brevity. **One mechanism verified before describing it plainly:** the dashboard's history walk
skips a deletion commit *and both pairs it sits between* (`methodology_dashboard.py` `_gate_manifest_history`
returns `None` on a failed parse; the pairing loop `continue`s on either side), and `_gate_loosenings`
already carries the `removed` branch it never reaches — which is what makes the suggested fix a two-line
one. Terminology re-audited: no session, backlog or finding codes; the PR's decision codes survive on one
line only, where the comment quotes them as examples a reader cannot resolve. **Still nothing posted.**

### 2026-09-15 · [ad hoc] S170 — the comment on upstream PR #82 drafted (not posted)

**Deliverable, drafted:** `docs/planning/pr82-comment.md` — one comment on upstream PR #82 carrying ten
suggested changes, ranked: two on file budgets measured in bytes where tokens is the operative unit, three
on what the quality ratchet does not hold, four smaller ones, and one on the readability of the PR
description. **Nothing posted** — the post is its own operator go-ahead, and the text is presented in full
first. **Every claim re-verified this session before drafting, none relayed:** #82 unmoved at head
`c84e7d96` with 0 comments and 0 reviews; `docs/planning/pr82-review-repro.sh` re-run end to end, all seven
sections matching what S169 recorded; all six token figures re-measured, both controls (48,555 and 36,955)
reproducing exactly; `quality_ratchet.py --run` re-run in a **verified** `--no-local` clone at `c84e7d96`
(HEAD sha asserted before use) giving **9/9 pass, results `74c773523dab`** — the receipt's own hash,
reproduced firsthand — plus `--selftest` 17 OK, `bin/tests.sh` `== Summary: 134 passed, 1 failed ==` read
directly, and `context_budget.py --status` exit 0. **Two findings sharpened against the review:** the
runner's density 2.8248 was measured correctly in `008d656` and went stale two commits later (`628d218`
53,301 B, `b4226d3` 53,328 B), which is the fair framing and is what the comment says; and Phase 0 is
byte-unchanged by the PR (its runner diff touches only lines 220+, 271+, 316+, 359+), so the description's
"Phase 0 compares the cited counts" has nothing behind it. **One would-be finding dropped:** an
archive-and-`git init` tree measured 131 passed, not 134 — an artifact of the reproduction method, not a
defect, and it did not reach the draft. Terminology audited against the operator's bar: no session
numbers, no backlog or finding codes, no coined names; the PR's own decision codes appear only where the
comment quotes them as examples of what a reader cannot resolve.

### 2026-09-15 · [ad hoc] S170 claim — a comment on upstream PR #82 with suggested changes

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: one comment on
upstream PR #82 (the maintainer's quality ratchet, plan #81) carrying suggested changes to improve it —
drafted to a file, its full text presented before anything is posted, posted only on the operator's explicit
go-ahead, then read back. Scheduled by the operator at S169's close-out: *"for the next session, plan on
developing and posting a comment for PR #82 with suggested changes to improve the PR."* The substance comes
from S169's fork-only review (`docs/planning/pr82-review.md`, recorded at `4ffcb253`) and is **translated,
not pasted** — the operator's bar for the comment is generally recognized terminology with no jargon or
private descriptors, which is also one of the improvements it suggests. Phase 0: #82 OPEN at head
`c84e7d96`, unmoved since the review, 0 comments and 0 reviews; both ledger frontiers at `1d88eaa` with 0
undocumented commits; `HANDOFFS.md` 4 receipts, no trim owed; `CHANGELOG.md` 259,241 B, 2,903 B under the
262,144 B read refusal, not trimmed (the operator's 2026-09-14 decision). BL-57's P3 waits. Carries the
Phase 0 `dashboard_history.jsonl` snapshot.

### 2026-09-15 · [ad hoc] S169 follow-up — the receipt's "unpushed" statement corrected after the push (nothing posted)

- **Change:** S169's receipt, `next_steps` item (1), said the review and its script *"exist only on this fork's
  unpushed `main`"*. That went false when `main` reached `origin` (`4c07b91..c0d7eee`, then `c0d7eee..31b574b`),
  so the line now records the push, gives the absolute URL a comment would need, and says the comment carries
  its substance in plain terms rather than leaning on a link into this fork. A correction is a new entry here,
  never an edited one.
- **Recorded:** this commit, pushed the same way, so `origin/main` equals `main`. Nothing posted upstream.

### 2026-09-15 · [ad hoc] S169 follow-up — fork `main` pushed to `origin`, `4c07b91..c0d7eee` (non-commit action, operator go-ahead)

- **Action:** `git push origin main`, a fast-forward of S169's seven commits — claim `f89c0faf`, trim
  `0ccfce84`, fold `da8af503`, the review record `4ffcb253`, close-out `4c86987`, and the two follow-ups
  `885fd77` and `c0d7eee` — run only inside a guard that re-fetched `origin` and re-checked, in the same
  command, `origin/main` = `4c07b916`, `main` = `c0d7eee3`, 7 ahead, 0 behind, an ancestor, and a clean tree.
  Read back: `git ls-remote origin refs/heads/main` = `c0d7eee3`, equal to local `main`, 0 ahead. Nothing was
  pushed to `upstream`; no PR, comment or reply was opened. This entry's own commit is pushed the same way, so
  `origin/main` equals `main`.
- **Go-ahead:** the operator's, after S169's close-out (*"push fork main to origin"*).

### 2026-09-15 · [ad hoc] S169 follow-up — the operator adds a requirement for the PR #82 comment: generally recognized terminology (nothing posted)

- **Decision:** the operator added that one improvement to suggest on #82 is the readability of its stated
  purpose and methods: *"Use generally recognized terminology with no jargon or private descriptors."* S169's
  receipt, `next_steps` item (1), now carries it, for the suggestion and for the comment itself —
  `docs/planning/pr82-review.md` is written in this fork's shorthand and is to be translated, not pasted.
- **Recorded:** this commit. Nothing was drafted or posted in S169.

### 2026-09-15 · [ad hoc] S169 follow-up — the operator schedules the next session: a comment on PR #82 with suggested changes (nothing posted)

- **Decision:** after S169's close-out the operator directed: *"for the next session, plan on developing and
  posting a comment for PR #82 with suggested changes to improve the PR."* S169's receipt, `next_steps` item
  (1), now says so, with the recipe: re-fetch #82, re-run `docs/planning/pr82-review-repro.sh` against its head,
  draft from `docs/planning/pr82-review.md` §6, present the final text, post it through
  `gh api repos/KJ5HST/methodology/issues/82/comments`, read it back. BL-57's P3 follows it.
- **Recorded:** this commit. Nothing was drafted or posted in S169; the comment is the next session's action.

### 2026-09-15 · [ad hoc] S169 close-out — a fork-only review of upstream PR #82; nothing posted

- **Change:** S169's receipt is completed in `HANDOFFS.md` (self 8/10, predecessor S168 9/10). On the
  operator's request after Phase 0 the session reviewed upstream PR #82 at `c84e7d96` (the record entry
  below) instead of BL-57's P3, which waits; and it trimmed `HANDOFFS.md` to four receipts under its
  retention rule. Nothing was posted upstream. No learning row (BL-53 leaves about three); the lessons are in
  agent memory.
- **Commit/PR:** this commit (claim `f89c0faf`, trim `0ccfce84`, fold `da8af503`, record `4ffcb253`)
- **Session:** S169 · **Verified:** on the record `4ffcb253` in a `--no-local` clone, `bin/tests.sh` 305 passed / 0 failed / 0 skipped, as at a same-time control at `4c07b91`, with 0 status flips and 10 rows differing only in numbers this session moved; `check-links` 105 links; `check-learnings` OK; `check-handoff --all` 0; the shard's `.verify.sh` exit 0 at the trim and after the fold
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] S169 — a fork-only review of upstream PR #82 (the quality ratchet): its file budgets, and seven demonstrated defects

- **Change:** `docs/planning/pr82-review.md` reviews KJ5HST/methodology#82 at `c84e7d96` on the operator's
  request, and `docs/planning/pr82-review-repro.sh` re-runs its seven demonstrations (its section 8, the
  token measurements, is manual). **Budgets:** `CLAUDE.md` is held by a 59,168 B arrival-size byte pin —
  #82 closed 15 B under it yet measures 62 tokens over `main` (23,482.5 against 23,420.5, by the
  doubled-file Read), and the tool judges it at an unmeasured 2.93 B/token (measured: 2.519); the runner's
  token ceiling is applied at a density measured before #82 edited the file — 18,897.5 of 18,900 tokens
  measured, 2.5 of room where the tool reports 22; `context_budget.py --status` is outside the ratchet.
  **Defects, each run in a throwaway repository:** deleting the manifest passes the hook, and deleting then
  re-adding it lower is invisible to hook and dashboard; the count gates pass over failing and skipped
  tests; the gate-run citation lint accepts `0/9 pass`, and no Phase 0 step performs the comparison; the
  dashboard's mirror of `compare()` misses direction flips and command edits; the coverage bonus keys on a
  gate's name; the installed hook locks an adopter out after a deletion; `install-hook` in a fresh
  canonical clone breaks every commit. **Nothing posted upstream.**
- **Commit/PR:** this commit
- **Session:** S169 · **Verified:** #82's suites in a `--no-local` clone at `c84e7d96` — `bin/tests.sh`
  134 passed / 1 failed (Test 9, by construction), `--selftest` 17 OK, `--run` 9/9 with the S20
  receipt's own results hash `74c773523dab`, `context_budget.py --status` 0, no tracked file changed; the
  token instrument first reproduced three recorded figures exactly (48,555; 49,683; 36,955); the saved
  script re-run end to end, every row as the review records it
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] S169 — `HANDOFFS.md`: the trim's pointer block folded into the archive table (20 trims, 154 receipts)

- **Change:** the 3-line pointer block `methodology_trim.py` appended for
  `docs/archive/HANDOFFS-through-2026-09-15-2.md` (trim `0ccfce84`) becomes one table row (n = 2, the
  shard's own fence count), and the table header moves 19 trims / 152 receipts → 20 / 154. Its own
  commit, after the trim (Learning #58). No `--force` was needed: SRF 0.8644 after the claim.
- **Commit/PR:** this commit
- **Session:** S169 · **Verified:** the shard's `.verify.sh` exit 0 at the trim commit `0ccfce84`
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-15-2.md` (2 record(s), 54,851 B → 35,001 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-09-15 → 2026-09-15) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-15-2.md`](docs/archive/HANDOFFS-through-2026-09-15-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-15-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-15-2.md.verify.sh)
rather than trusting a digest printed here. Live file 54,851 B → 35,001 B (−36.2%).

### 2026-09-15 · [ad hoc] S169 claim — a review of upstream PR #82's file budgets and other challenges

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: one fork-only
review of upstream PR #82 — the maintainer's quality ratchet (plan #81), head `c84e7d96`, OPEN and CLEAN
with 0 comments at Phase 0 — written to `docs/planning/pr82-review.md`. The operator's request after Phase
0: *"Look at PR #82 and the way it manages file budgets. Some look to be using bytes in a way we have
recently replaced with better measures of size"* — and any other challenge to what it proposes. Nothing is
posted upstream; a comment on #82 is its own go-ahead. BL-57's P3 waits. Phase 0: both ledger frontiers at
`4c07b91`, 0 undocumented commits; `HANDOFFS.md` 5 receipts, so this session trims to four after this
claim; `CHANGELOG.md` 250,649 B, 11,495 B under the 262,144 B read refusal, not trimmed (the operator's
2026-09-14 decision). Carries the Phase 0 `dashboard_history.jsonl` snapshot.

### 2026-09-15 · [ad hoc] S168 follow-up — fork `main` pushed to `origin` again, `a6520fe..bc7d1e9` (non-commit action, operator go-ahead)

- **Action:** `git push origin main`, a fast-forward of the one commit that records the branch push
  (`bc7d1e9`), inside a guard that re-fetched `origin` and re-checked, in the same command, `origin/main` =
  `a6520fe9`, `main` = `bc7d1e91`, 1 ahead, an ancestor, a clean tree. Read back: `git ls-remote origin
  refs/heads/main` = `bc7d1e91`. This entry's own commit is pushed the same way, so `origin/main` equals
  `main`; S168's receipt, item (4), says so without naming a final sha.
- **Go-ahead:** the operator's (*"push fork main to origin"*).

### 2026-09-15 · [BL-57] S168 follow-up — branch `bl57/changelog-rules` pushed to `origin` as a backup, at `775ba238` (non-commit action, operator go-ahead)

- **Action:** `git push origin bl57/changelog-rules`, creating the branch on the fork — run only inside a
  guard that re-fetched `origin` and re-checked, in the same command, the local branch at `775ba238`, its
  worktree clean, and no branch of that name on `origin`, so nothing could be overwritten. Read back:
  `git ls-remote origin refs/heads/bl57/changelog-rules` = `775ba238`, equal to local. Nothing upstream,
  and no PR — GitHub's *create a pull request* hint was not followed. Rewriting the branch from here — a
  rebase at P12 — needs a force-push of the backup. The plan's header, BL-57's backlog row and S168's
  receipt (`active_task`, item (4)) now say so. This entry's own commit is not pushed.
- **Go-ahead:** the operator's, after S168's close-out (*"push the branch to origin as a backup"*).

### 2026-09-15 · [ad hoc] S168 follow-up — fork `main` pushed to `origin`, `6142d53..2d1bcc3` (non-commit action, operator go-ahead)

- **Action:** `git push origin main` after the close-out, a fast-forward of 8 commits — S167's five and
  S168's three — run only inside a guard that re-fetched `origin` and re-checked, in the same command,
  `origin/main` = `6142d538`, `main` = `2d1bcc30`, 8 ahead, an ancestor, a clean tree. Read back:
  `git ls-remote origin refs/heads/main` = `2d1bcc30`, equal to local `main`, 0 ahead. This entry's own
  commit is pushed the same way, so `origin/main` equals `main` again; S168's receipt says so at item (4).
- **Go-ahead:** the operator's, after S168's close-out (*"push fork main to origin (8 commits)"*).

### 2026-09-15 · [BL-57] S168 close-out — BL-57's P2 done on a branch, not pushed; P3 next

- **Change:** S168's receipt is completed in `HANDOFFS.md` (self 8/10, predecessor S167 9/10). The session
  did BL-57's P2 on branch `bl57/changelog-rules` — a merge of `upstream/main` and two commits, not pushed
  (the entry below). No trim: `HANDOFFS.md` held four receipts at Phase 0 and holds five now, so S169's
  Phase 0 trims. No learning row (BL-53 leaves about three).
- **Commit/PR:** this commit (claim `5eef31f1`, record `30a96bb9`)
- **Session:** S168 · **Verified:** on the record `30a96bb9` in a `--no-local` clone, `bin/tests.sh` 305 passed / 0 failed / 0 skipped, as at a same-time control at `d2347a16`, with 0 status flips and 8 rows differing only in numbers this session moved; unit suites 321 · 123 · 116 OK; the branch as the entry below records; `check-handoff --all` 0
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [BL-57] S168 — BL-57's P2 done on branch `bl57/changelog-rules` (a merge of `upstream/main` and two commits, not pushed); the plan amended

- **Change:** in the worktree `../methodology-bl57`, the branch merged `upstream/main` `8b4dc2c3`
  (`9e1dfeb`, clean; it brings upstream's `.githooks/commit-msg` and the maintainer's S17–S19 records),
  then took P2 in two commits, each with its own entry in the branch's ledger. `f2bcc22`:
  `FRAMEWORK_APPARATUS.md`'s *Size, and when to archive* becomes *Reading and archiving* — the protocol's
  three reads are each partial; past `READ_REFUSE_BYTES`, read with an offset and a limit; archiving is
  optional and the tool's `--check` the only trigger, no size named; conservation across the live file and
  its shards; a trim never in Phase 0 — and the two-cap table and its rate-versus-level argument go,
  28,022 → 25,983 B. `775ba238`: the `HANDOFFS.md` seed's premise and two-cap table give way to *"Archive
  it when the trimmer's trigger fires … this file names no size of its own"* (heading kept, D9; its rule
  otherwise stands, D7), and the trimmer's `:186` comment drops *"context-tax"* (AST identical to
  `b82dcff`). P2's step 4, D8 (ii), needed no commit: #80's F3 did it. **Not pushed; no PR.** Here: the
  plan's header and S168 amendment (`docs/planning/changelog-rules-contradictions-plan.md:3`, `:36`), and
  BL-57's backlog row.
- **Found:** the `HANDOFFS.md` seed's shard bullet still publishes a bare glob that zsh refuses where no
  shard exists (C10's class, recorded for P3); `HOW_TO_USE.md:748`'s *"~515 lines"* is now 501 (P4).
- **Commit/PR:** this commit; branch `9e1dfeb` (merge), `f2bcc22`, `775ba238`
- **Session:** S168 · **Verified:** in `--no-local` clones, `bin/tests.sh` 118 passed / 0 failed at
  `77b21a20` (the control), `9e1dfeb`, `f2bcc22` and `775ba238`, with 0 status flips and no row added or
  removed; unit suites 211 · 124 · 116 OK at each; `check-links` 107 links in 23 files; `check-learnings`
  13 rows; `context_budget.py --status` 0 at each, and §9.7 on `775ba238` — its merge with `upstream/main`
  is its own tree — *nothing over budget*, `CLAUDE.md` 59,159 of 59,168 B; P2's three DONE greps print
  nothing on `775ba238`
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [BL-57] S168 claim — BL-57's P2: reading and archiving, on the branch after merging `upstream/main`

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: P2 of the
approved BL-57 plan (`docs/planning/changelog-rules-contradictions-plan.md:440`), the operator's *"A"* at
this session's Phase 0. In the worktree `../methodology-bl57`, branch `bl57/changelog-rules` (`77b21a20`,
S167's P1) first merges `upstream/main` `8b4dc2c3` (#80 merged at `4d9e2715`), then takes P2's scope;
nothing is pushed. P2's item 4 — D8 (ii), drop `CHANGELOG.md` from upstream's root `.context-budget.json`
— is already done: #80's F3 moved both ledgers to `_deliberate_exclusions`, verified on `upstream/main` at
Phase 0, so the plan records it rather than redoing it. Phase 0: both ledger frontiers at `d2347a16`, 0
undocumented commits; `HANDOFFS.md` 4 receipts, no trim; `CHANGELOG.md` 243,849 B, 18,295 B under the
262,144 B read refusal, not trimmed (the operator's 2026-09-14 decision); no open upstream issues or PRs.
Carries the Phase 0 `dashboard_history.jsonl` snapshot.

### 2026-09-15 · [BL-57] S167 close-out — BL-57's P1 done on a branch, not pushed; PR #80 merged upstream; P2 next

- **Change:** S167's receipt is completed in `HANDOFFS.md` (self 7/10, predecessor S166 9/10). The session
  did BL-57's P1 on branch `bl57/changelog-rules` (four commits, not pushed; the entry below), trimmed
  `HANDOFFS.md` to four receipts, and recorded #80's merge (`4d9e2715`), which landed mid-session. No
  learning row: the one candidate, *a green suite cannot see a gate it never runs*, is in memory, and BL-53
  leaves about three rows.
- **Commit/PR:** this commit (claim `6f9162f1`, trim `50498451`, fold `943059f5`, record `f63460e5`)
- **Session:** S167 · **Verified:** on this content committed inside a `--no-local` clone, `bin/tests.sh`
  305 passed / 0 failed / 0 skipped, as is a same-time control at `6142d538` — Test 9 passes on fork `main`
  too since #80's merge — with 0 status flips and 11 rows differing only in numbers this session moved;
  unit suites 321 · 123 · 116 OK; `check-handoff --all` 0
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [BL-57] S167 — BL-57's P1 done on branch `bl57/changelog-rules` (4 commits, not pushed); the plan amended; PR #80 merged upstream the same day

- **Change:** branch `bl57/changelog-rules` created from PR #80's head `aa36fd8b` in the worktree
  `../methodology-bl57` (a branch operation), and P1 of the approved plan committed on it — four commits,
  each with its own entry in the branch's own `CHANGELOG.md`: `eb06625b` the trimmer's fence controls read
  a frozen copy of today's seed (`tools/fixtures/seed-CHANGELOG-ledger-format-1.md`); `b0634606` the seed's
  three rule sections move verbatim to `FRAMEWORK_APPARATUS.md` §The Action Ledger, and the seed becomes a
  1,335 B pointer carrying `ledger-format: 2`; `2d5dc6e9` `bin/status` keys on that marker and its advice
  stops rewriting entries; `77b21a20` the three documents that describe the apparatus name its seventh
  section. **Not pushed; no PR** — each is its own go-ahead. In this repo: the plan's header and an S167
  amendment (`docs/planning/changelog-rules-contradictions-plan.md:3`, `:21`), its §9.4 command corrected
  for zsh, and BL-57's backlog row.
- **Found:** (1) step 4 first landed as `d4841721`, 116 B over upstream `CLAUDE.md`'s pinned 59,168 B
  ceiling, with all four suites green — none runs `context_budget.py --status` on the tree. The plan's §9.7
  check caught it, and the commit was amended to `77b21a20` (the row is now 9 B shorter than before;
  unpushed, so nothing published was rewritten). (2) The plan's §9.4 command printed nothing under zsh:
  `"$c:…"` is a history modifier. (3) **PR #80 merged** at 19:59 UTC (`4d9e2715`; `upstream/main`
  `8b4dc2c3`), which is why Test 9 now passes on every tree.
- **Commit/PR:** this commit (the record); branch `eb06625b`, `b0634606`, `2d5dc6e9`, `77b21a20`
- **Session:** S167 · **Verified:** at `77b21a20`, in a `--no-local` clone: `bin/tests.sh` 118 passed / 0
  failed, against 116 / 0 at `aa36fd8b` run at the same time — 1 row renamed, 3 added, 0 status flips; unit
  suites 211 · 124 · 116 OK (4 skipped); `check-links` 107 links (from 105); `check-learnings` 13 rows.
  `context_budget.py --status` exits 0 on the branch and on its merge into `upstream/main`. The plan's P1
  DONE checks: §9.3 VERBATIM ×3; §9.4 prints only `b0634606`; the seed ≤ 1,600 B with no `## `, `NO_RECORDS`
  exit 0, seeded by `bin/sync`; all six adopters' `CHANGELOG.md` copies read stale with the new advice, and
  their `HANDOFFS.md` verdicts equal fork `main`'s.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] S167 — `HANDOFFS.md`: the trim's pointer block folded into the archive table (19 trims, 152 receipts)

- **Change:** the 3-line pointer block `methodology_trim.py` appended for
  `docs/archive/HANDOFFS-through-2026-09-15.md` (trim `50498451`) becomes one table row (n = 2, the
  shard's own fence count), and the table header moves 18 trims / 150 receipts → 19 / 152. Its own
  commit, after the trim (Learning #58). No `--force` was needed: SRF 0.8755 after the claim.
- **Commit/PR:** this commit
- **Session:** S167 · **Verified:** the shard's `.verify.sh` exit 0 at the trim commit `50498451`
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-15.md` (2 record(s), 57,366 B → 38,813 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-09-14 → 2026-09-15) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-15.md`](docs/archive/HANDOFFS-through-2026-09-15.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-15.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-15.md.verify.sh)
rather than trusting a digest printed here. Live file 57,366 B → 38,813 B (−32.3%).

### 2026-09-15 · [BL-57] S167 claim — BL-57's P1: the `CHANGELOG.md` rules to one home, thin seeds, one stale-seed rule (structure only), on a branch from #80's head

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: P1 of the
approved BL-57 plan (`docs/planning/changelog-rules-contradictions-plan.md:359`), the operator's *"A"* at
this session's Phase 0. Branch `bl57/changelog-rules` from PR #80's current head `aa36fd8b` (the plan was
written at `b82dcff`; its hazard 1), in a worktree at `../methodology-bl57`; nothing is pushed. Phase 0:
#80 OPEN at `aa36fd8b`, `MERGEABLE`/`CLEAN`, 3 comments, nothing from the maintainer since S166's reply;
`upstream/main` `9fa3141`; both ledger frontiers current; `bin/tests.sh` 304 / 1 / 0 at `6142d538` (Test
9). `HANDOFFS.md` holds 5 receipts, so this session trims it to 4 after this claim (dry run: S162 to
`docs/archive/HANDOFFS-through-2026-09-14.md`, SRF 0.8013, no `SRF_RED`). `CHANGELOG.md` is 237,544 B,
24,600 B under the 262,144 B read refusal; not trimmed — the operator's 2026-09-14 decision, asked about
at Phase 0 and not changed. Carries the Phase 0 `dashboard_history.jsonl` snapshot.

### 2026-09-15 · [ad hoc] S166 follow-up — fork `main` pushed to `origin`, `755ef09..632f575` (non-commit action, operator go-ahead)

- **Action:** `git push origin main` after the close-out, a fast-forward of 11 commits — S164's three,
  S165's five and S166's three — run only after checking that `origin/main` was an ancestor of `main`, 0
  commits behind, with a clean tree. Read back: `git ls-remote origin refs/heads/main` = `632f5758`, equal
  to local `main`. This entry's own commit is pushed the same way, so `origin/main` equals `main` again.
- **Go-ahead:** the operator's, after S166's close-out (*"push main to origin"*).

### 2026-09-15 · [ad hoc] S166 close-out — PR #80's F2 and F3 published (push, description, reply); the maintainer's move next

- **Change:** S166's receipt is completed in `HANDOFFS.md` (self 8/10, predecessor S165 9/10). The session
  published F2 (`37740763`) and F3 (`aa36fd8b`) of the maintainer's #80 review on the operator's go-ahead
  for all three actions — the push `d4e1570..aa36fd8`, the description, the reply — each read back before
  the next (the three entries below). The response plan's §4 and §5 headings now say published too. No
  trim: `HANDOFFS.md` held 4 receipts at Phase 0, and holds 5 after this commit, so S167's Phase 0 trims.
- **Commit/PR:** this commit (claim `32c90db4`, record `6e109e45`)
- **Session:** S166 · **Verified:** A, B and C each read back through the GitHub API; `check-handoff --all`
  0 (5 receipts); `bin/tests.sh` 304/1/0 at Phase 0 (`5ce7bb2`) and again on this close-out content
  committed inside a clone — 305 rows, 0 status flips (the counter proved on a planted flip), 9 rows
  differing only in numbers this session moved
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] S166 — PR #80: the reply for F2 and F3 posted (non-commit action, operator go-ahead)

- **Action:** one comment on [PR #80](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5685701488),
  author `rmsharp`, 2026-09-15 18:21:28 UTC, body `docs/planning/pr80-reply-f2-f3.md`, posted through the
  REST API (`gh api repos/KJ5HST/methodology/issues/80/comments -F body=@…`): F2's generalized test and its
  six-mutant table; F3 as (i) for the pair with the ledgers dropped, (ii) shown unworkable as written, F4
  answered as framed; the corrected headline (68,548 B / 24,278 tokens on the merge); F5 and F6 after the
  merge. Read back through the API: equal to the file. #80 now has 3 comments.
- **Go-ahead:** the operator's, at S166 (*"A B C"*), gated on B's read-back.

### 2026-09-15 · [ad hoc] S166 — PR #80: the description updated to the F3 head (non-commit action, operator go-ahead)

- **Action:** the PR body replaced with `docs/planning/pr80-body-after-f3.md` through `gh api -X PATCH
  repos/KJ5HST/methodology/pulls/80 -F body=@…` — the head `aa36fd8`, 28 files +7,892 / −580 (re-derived at
  Phase 0, after reproducing +7,795 / −554 at `d4e1570`), the headline table re-measured on the merge
  (68,548 B / 24,278 tokens, 97.1%; `main` 81,493 B / 28,610), the paragraph on the root
  `.context-budget.json`, the corpus 659,755 → 839,383 B, and the F2 and F3 verification rows. Before it,
  the live body was checked equal to `pr80-body-after-f1.md`, so the maintainer had not edited it. Read
  back after: equal to the file, byte for byte.
- **Go-ahead:** the operator's, at S166, gated on A's read-back.

### 2026-09-15 · [ad hoc] S166 — PR #80: F2 + F3 pushed, `read-set-budgets` fast-forwarded `d4e1570..aa36fd8` (non-commit action, operator go-ahead)

- **Action:** `git push upstream pr80/f3-read-set-token-ceilings:read-set-budgets`, run only when the same
  command had re-checked #80's head (`d4e1570`), `upstream/main` (`9fa3141`) and its 2 comments. It carries
  F2 (`37740763`) and F3 (`aa36fd8b`), each with its entry in the branch's own ledger. Read back: the remote
  ref and the API's branch head both `aa36fd8b`; #80's head `aa36fd8b`, 16 commits, `MERGEABLE`/`CLEAN` —
  on the second read: the first, seconds after the push, still showed `d4e1570` and `UNKNOWN`. The three
  local `pr80/*` branches stay until #80 merges.
- **Go-ahead:** the operator's, at S166.

### 2026-09-15 · [ad hoc] S166 claim — PR #80: publish F2 + F3 (push, description, reply) on the operator's go-ahead for all three

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: S165's next
step (1) — publish F2 (`37740763`) and F3 (`aa36fd8b`) of the maintainer's #80 review, by
`docs/planning/pr80-review-response.md` §3. The operator approved all three outward actions at this
session's Phase 0 (*"A B C"*): A, push `pr80/f3-read-set-token-ceilings:read-set-budgets` (a fast-forward
from `d4e1570`); B, the description from `docs/planning/pr80-body-after-f3.md`; C, the reply
`docs/planning/pr80-reply-f2-f3.md`. Each is read back before the next, and any mismatch stops the
sequence. Phase 0: #80 still at `d4e1570`, `upstream/main` at `9fa3141`, 2 comments; `HANDOFFS.md` at 4
receipts, so no trim. Carries the Phase 0 `dashboard_history.jsonl` snapshot.

### 2026-09-15 · [ad hoc] S165 close-out — PR #80's F3 done on a local branch, held with F2 for one publish; three go-aheads next

- **Change:** S165's receipt is completed in `HANDOFFS.md` (self 8/10, predecessor S164 9/10). The session
  answered F3 of the maintainer's #80 review on local branch `pr80/f3-read-set-token-ceilings`
  (`aa36fd8b`, on top of F2's `37740763`) with the operator's R1 L1, and recorded it in
  `docs/planning/pr80-review-response.md` §5, with the description re-derived and one reply drafted. It
  also trimmed `HANDOFFS.md` to four receipts without `--force`. The worktree `../methodology-pr80-f3` was
  removed once clean (local housekeeping); the branch stays. Nothing was pushed.
- **Commit/PR:** this commit (claim `8e0a7a72`, trim `d9ace03`, fold `ef55d77`, record `95a4845`; branch
  `aa36fd8b`, not pushed)
- **Session:** S165 · **Verified:** `check-handoff --all` 0 (4 receipts); branch suites 115/1 at `37740763`
  and `aa36fd8b` with 0 status flips; `--status` exit 0 on both trees; fork `bin/tests.sh` 304/1/0 at
  `ef55d775` with 0 status flips against Phase 0, and 304/1/0 again on this close-out content committed
  inside a clone — 0 status flips, 7 rows differing only in numbers this session moved
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] S165 — PR #80 review F3 done on a local branch, not pushed: the root `.context-budget.json` reports OK on the branch and on its merge into `main`

- **Change:** local branch `pr80/f3-read-set-token-ceilings` (worktree `../methodology-pr80-f3`) from F2's
  `37740763`, one commit, **`aa36fd8b`**: the branch's root `.context-budget.json` gives
  `SESSION_RUNNER.md` and `SAFEGUARDS.md` token ceilings at measured densities (19,200 + 5,800 tokens,
  partitioning the 25,000-token cap), declares no `read-set` class ceiling, and moves `CHANGELOG.md` and
  `HANDOFFS.md` to `_deliberate_exclusions`; its entry sits in the branch's own ledger above F2's.
  Canonical-only. The operator chose **R1 L1** at this session's Present gate, from nine variants measured
  first on the branch and on its merge into `upstream/main` (`docs/planning/pr80-f3-variants.py`). Record:
  `docs/planning/pr80-review-response.md` §5 (header, §1 and §3 updated); drafted for the publish, the
  description with every figure re-derived (`docs/planning/pr80-body-after-f3.md`) and one reply for F2 and
  F3 (`docs/planning/pr80-reply-f2-f3.md`). **Nothing pushed, no description edit, no reply** — three
  go-aheads, in §3's order.
- **Found:** the merge is 967 B larger than the branch (upstream S16's paragraph in `SAFEGUARDS.md`), so
  the description's headline row was stale — the merged pair is 68,548 B / 24,278 tokens, not
  67,581 / 23,902; and the review's answer (ii) cannot work as written, because `token_ceiling()` clamps
  every whole-read file to the 25,000-token cap.
- **Commit/PR:** this commit (branch `aa36fd8b`, not pushed)
- **Session:** S165 · **Verified:** `--status` exit 0 on both trees from the committed config; branch
  `bin/tests.sh` 115/1 at `37740763` and `aa36fd8b` — 116 rows, 0 status flips, 0 rows differing; unit
  suites 211 · 123 · 116 OK; `check-links` and `check-learnings` OK; `merge-tree` against `9fa3141` clean;
  the push is a fast-forward
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] S165 — `HANDOFFS.md`: the trim's pointer block folded into the archive table (18 trims, 150 receipts)

- **Change:** the 3-line pointer block `methodology_trim.py` appended for
  `docs/archive/HANDOFFS-through-2026-09-11.md` (trim `d9ace03`) becomes one table row (n = 2, the
  shard's own fence count), and the table header moves 17 trims / 148 receipts → 18 / 150. Its own
  commit, after the trim (Learning #58). No `--force` was needed: SRF 0.9383 after the claim.
- **Commit/PR:** this commit
- **Session:** S165 · **Verified:** the shard's `.verify.sh` exit 0 at the trim commit `d9ace03`
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-11.md` (2 record(s), 60,236 B → 37,186 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-09-11 → 2026-09-11) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-11.md`](docs/archive/HANDOFFS-through-2026-09-11.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-11.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-11.md.verify.sh)
rather than trusting a digest printed here. Live file 60,236 B → 37,186 B (−38.3%).

### 2026-09-15 · [ad hoc] S165 claim — PR #80 review F3: the root `.context-budget.json` reports the PR's own headline as OVER

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: F3 of the
maintainer's PR #80 review ([comment](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5674670153)),
chosen by the operator at this session's Phase 0 (A). Measure the four answers — (i) the read-set ceiling
in tokens at measured density; (ii) the ledger ceilings set where the ledgers are; (iii) *"over at install,
by design"*, stated; (iv) the ledgers dropped from the read budget, as this fork did at `3c8acd5` — on
branch `pr80/f2-installed-source-guard`, bring them to the operator in prose, and commit the chosen one on
top of `37740763`, tested in a `--no-local` clone. First, `HANDOFFS.md`'s retention trim to four (5
receipts at Phase 0, SRF 0.8687: no `--force` needed if this stub keeps the file under 61,471 B —
re-derived after this commit). **Nothing pushed, no PR edit, no reply** — each is its own go-ahead.
Carries the Phase 0 `dashboard_history.jsonl` snapshot.

### 2026-09-15 · [ad hoc] S164 close-out — PR #80's F2 done on a local branch and held for one push with F3; F3 next

- **Change:** S164's receipt is completed in `HANDOFFS.md` (self 8/10, predecessor S163 9/10). The session
  answered F2 of the maintainer's #80 review on local branch `pr80/f2-installed-source-guard` (`37740763`,
  test-only), RED first on the review's mutant, and recorded it in `docs/planning/pr80-review-response.md`
  §4. Nothing was pushed: F2 is held so F2 and F3 go up in one push and one reply. The worktree
  `../methodology-pr80-f2` was removed once clean (local housekeeping); the branch stays. F3 starts with
  an operator decision (§5).
- **Commit/PR:** this commit (claim `8791a272`, record `95d84cfd`; branch `37740763`, not pushed)
- **Session:** S164 · **Verified:** `check-handoff --all` 0 (5 receipts); branch suites 115/1 at
  `d4e1570` and `37740763` with 0 status flips; fork `bin/tests.sh` on this content in a `--no-local`
  clone 304/1/0, exit 1, 0 status flips against the Phase 0 baseline (the one failure is Test 9,
  pre-existing)
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] S164 — PR #80 review F2 done on a local branch, not pushed: every non-markdown file `bin/sync` installs is now tested, RED first

- **Change:** local branch `pr80/f2-installed-source-guard` (worktree `../methodology-pr80-f2`) from #80's
  head `d4e1570`, one commit, **`37740763`**: `tools/test_methodology_dashboard.py:2666` generalizes
  `test_a_synced_repo_with_context_budget_installed_is_still_doc_only` in place as
  `test_a_synced_repo_with_each_installed_source_file_is_still_doc_only` — every non-markdown dest in
  `bin/_manifest.py`, written from its real `starter-kit/` source into a doc-only fixture, alone and all
  together, plus a direct `is_framework_installed` call per file. Its entry sits in the branch's own ledger
  (`CHANGELOG.md:95` there), above F1's and below `main`'s. Test-only and canonical-only: neither scanner
  twin changes. On fork `main`: `docs/planning/pr80-review-response.md` §4 records the branch and its
  evidence, and its header now says F1 was published at S163 (it still read *"Nothing below has been
  pushed"*); new `docs/planning/pr80-f2-mutants.py` plants the six mutants.
- **RED first:** the review's mutant (M1), `.context-budget.json`'s signatures (M4) and a narrowing of the
  one `collect_all` call site (M6) pass the old suite (211 OK) and fail the new test. The scanner's own
  entry (M3) is not caught by this test — its neutralized strings sit in its own signature table, so the
  real file matches itself — and the docstring says so.
- **Verified**, in `--no-local` clones, every exit code read bare: `bin/tests.sh` 115 / 1, exit 1 at
  `d4e1570` and at `37740763` — 116 rows, 0 status flips, 0 rows differing (Test 9, pre-existing); unit
  suites 211, 123 (2 skipped) and 116 (2 skipped) OK on both; `check-links` OK (105 / 23) and
  `check-learnings` OK (13 rows) on both. `git merge-tree` against `upstream/main` `9fa3141`: no
  conflicts; the push would fast-forward `read-set-budgets`.
- **Not pushed, no description edit, no reply** — held so F2 and F3 go up in one push and one reply;
  each is its own go-ahead.
- **Commit/PR:** this commit; branch `37740763`

### 2026-09-15 · [ad hoc] S164 claim — PR #80 review F2: guard the dashboard's doc-only exclusion for every framework-installed file, RED first

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: F2 of the
maintainer's PR #80 review ([comment](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5674670153)),
chosen by the operator at this session's Phase 0 (A). On a local branch from #80's head `d4e1570`:
generalize `test_a_synced_repo_with_context_budget_installed_is_still_doc_only`
(`tools/test_methodology_dashboard.py:2666`) over every `FRAMEWORK_INSTALLED_SOURCE` name
(`starter-kit/methodology_dashboard.py:360`) using the real `starter-kit/` file, RED first on the
maintainer's mutant — `methodology_trim.py`'s `version_re` and signatures (`:484`–`:496`) neutralized in
both twins — while the current suite stays green. A test change: neither dashboard twin is edited except
to plant the mutant in a clone. Tested in a `--no-local` clone. **Nothing pushed, no PR edit, no reply** —
each is its own go-ahead; Phase 0 suggested holding F2 locally so F2 and F3 go up in one push. Carries
the Phase 0 `dashboard_history.jsonl` snapshot.

### 2026-09-15 · [ad hoc] S163 follow-up — fork `main` pushed to `origin`, `f8531cf..6007db3` (non-commit action, operator go-ahead)

- **Action:** `git push origin main` on the operator's *"push main"*, after S163's close-out: a
  fast-forward of 60 commits (`origin/main` was `f8531cf`; no commit on `origin` was missing from
  `main`; the tree was clean). `origin/main` read back as `6007db3`. This entry's own commit is pushed
  the same way, so the two stay equal. Nothing else was pushed — the local branch
  `pr80/f1-learnings-1-13` already matches upstream's `read-set-budgets`.
- **Go-ahead:** the operator's, after S163's close-out. It discharges the S163 receipt's carried item
  *"pushing fork `main`"*.

### 2026-09-15 · [ad hoc] S163 close-out — PR #80's F1 answered and published; F2 and F3 next

- **Change:** S163's receipt is completed in `HANDOFFS.md` (self 8/10, predecessor S162 7/10). The
  session answered F1 of the maintainer's #80 review with option (a) — two commits on
  `read-set-budgets`, pushed; the description updated; the reply posted — and trimmed `HANDOFFS.md` to
  four receipts, forced past `SRF_RED` on the operator's decision. F2 and F3 are set up in
  `docs/planning/pr80-review-response.md` §4–§5; F3 starts with an operator decision.
- **Commit/PR:** this commit (claim `9f66ebd9`, preparation `42e52f9`, trim `ae44dec9`, outward actions
  `b9091fe`, fold `49685a9`; branch `5c9f0f3`, `d4e15706` on
  [PR #80](https://github.com/KJ5HST/methodology/pull/80))
- **Session:** S163 · **Verified:** `check-handoff --all` 0 (4 receipts); the shard proof 0 after the
  fold; branch suites 115/1 at `b82dcff`, `5c9f0f3` and `d4e15706` with 0 status flips; `bin/tests.sh`
  on this content in a `--no-local` clone 304/1/0, exit 1, 0 status flips against the Phase 0 baseline
  (the one failure is Test 9, pre-existing)
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] S163 — `HANDOFFS.md`: the trim's pointer block folded into the archive table

- **Change:** the three-line pointer block `methodology_trim.py` appended for
  `docs/archive/HANDOFFS-through-2026-09-10.md` becomes one table row (n = 2, the shard's own fence
  count), and the heading now reads 17 trims, 148 receipts. Its own commit, after the trim, because
  folding inside the trim commit fails the shipped proof's L2 (Learning #58).
- **Verified:** the table has 17 rows summing to 148; each edit matched exactly once.
- **Commit/PR:** this commit

### 2026-09-15 · [ad hoc] S163 — PR #80: the reply to the maintainer's review posted (non-commit action, operator go-ahead)

- **Action:** one comment on [PR #80](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5676599724),
  author `rmsharp`, 2026-09-15 07:42:05 UTC, body `docs/planning/pr80-reply-f1.md`: F1 answered with (a)
  and its two commits; F2 and F3 next; F4 left to the BL-57 plan's own PR after #80 merges; F5 and F6 can
  follow. Read back through the API: equal to the file.
- **Go-ahead:** the operator's, at S163 (*"push edit reply"*).

### 2026-09-15 · [ad hoc] S163 — PR #80: the description updated to the F1 head (non-commit action, operator go-ahead)

- **Action:** the PR body replaced with `docs/planning/pr80-body-after-f1.md` — the head and diff size,
  the corpus total (658,788 → 838,416 B), the `FRAMEWORK_LEARNINGS.md` and `context_budget.py` rows, a
  verification row, and one sentence saying the file holds rows 1–13 and the reserved `#14`. **`gh pr
  edit` failed** (exit 1, a GraphQL error about the deprecated Projects (classic) API) and changed nothing
  — the description read back as the original, so the reply was held back. The edit then went through
  the REST API (`gh api -X PATCH repos/KJ5HST/methodology/pulls/80 -F body=@…`) and read back equal to the
  file.
- **Go-ahead:** the operator's, at S163.

### 2026-09-15 · [ad hoc] S163 — PR #80: F1 (a) pushed, `read-set-budgets` fast-forwarded `b82dcff..d4e1570` (non-commit action, operator go-ahead)

- **Action:** `git push upstream pr80/f1-learnings-1-13:read-set-budgets`, after re-checking that #80's
  head was still `b82dcff`, upstream `main` still `9fa3141`, one comment, and `git merge-tree` clean.
  After: head `d4e15706`, `MERGEABLE`, `CLEAN`. The two commits carry their entries in the branch's own
  ledger. The worktree `../methodology-pr80` was removed once clean and pushed; the local branch stays
  until #80 merges.
- **Go-ahead:** the operator's, at S163.

### 2026-09-15 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-10.md` (2 record(s), 61,471 B → 41,455 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-09-10 → 2026-09-10) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-10.md`](docs/archive/HANDOFFS-through-2026-09-10.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-10.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-10.md.verify.sh)
rather than trusting a digest printed here. Live file 61,471 B → 41,455 B (−32.6%).

### 2026-09-15 · [ad hoc] S163 — PR #80 review F1 (a) prepared on a local branch, not pushed; the updated description and the reply drafted; the BL-57 plan amended

- **Change:** local branch `pr80/f1-learnings-1-13` (worktree `../methodology-pr80`) from #80's head
  `b82dcff`, two commits: `5c9f0f3` states the rule where eight citations of Learnings past #13 stood
  (`starter-kit/context_budget.py:77`, `:378`, `:409`, and five in the canonical-only tests), then
  `d4e15706` cuts `starter-kit/FRAMEWORK_LEARNINGS.md` to rows 1–13 plus the reserved `#14` (56,673 →
  13,983 B). Their entries sit in the branch's own ledger, with #80's block, below `main`'s. New
  fork-only files: `docs/planning/pr80-review-response.md` (the review, what was done, the publish
  commands, and F2 and F3 set up for the next session), `docs/planning/pr80-body-after-f1.md` (the PR
  description to publish) and `docs/planning/pr80-reply-f1.md` (the reply). The BL-57 plan's header
  now says it is approved and that no row past #13 will exist upstream; its P1 step 5 states Learning
  #19's rule instead of citing it.
- **Why:** the operator chose F1 option (a) at S163's Phase 0. Pushing, editing the PR description and
  replying are each the operator's go-ahead; none is done.
- **Verified:** in `--no-local` clones, `bin/tests.sh` 115/1 at `b82dcff`, `5c9f0f3` and `d4e15706` —
  116 rows each, 0 status flips (Test 9, pre-existing); unit suites 450 OK (4 skipped) at all three;
  `check-links` OK (105/23); `check-learnings` 13 rows, contiguous, citations resolve, and a planted
  `Learning #20` is caught; `git merge-tree` against upstream `main` `9fa3141`: no conflicts
- **Commit/PR:** this commit (fork `main`); the two branch commits are recorded in the branch's ledger
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] S163 claim — PR #80 review F1 (a): trim the branch's `FRAMEWORK_LEARNINGS.md` to rows 1–13 and repair the citations the cut breaks

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: F1 of the
maintainer's PR #80 review ([comment](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5674670153),
2026-09-15 04:19 UTC), option (a), chosen by the operator at this session's Phase 0. On a local branch
from #80's head `b82dcff`: cut `starter-kit/FRAMEWORK_LEARNINGS.md` to rows 1–13 plus the reserved-`#14`
note; repair every citation the cut leaves dangling — `starter-kit/context_budget.py:77` and `:378` cite
Learning #34, and `bin/check-learnings` scans Markdown only, so it would not see them; draft the
replacement for the PR description; amend the BL-57 plan's P1 step 5
(`docs/planning/changelog-rules-contradictions-plan.md:363`, which cites Learning #19). Tested in a
clone. **Nothing pushed, no PR edit, no reply** — each is its own go-ahead. F2 and F3 are set up for the
next session. `HANDOFFS.md` holds five receipts and its trim refuses with `SRF_RED` (SRF 1.0925 vs
`16ac3fc`); the operator's decision on `--force` is pending. Carries the Phase 0
`dashboard_history.jsonl` snapshot.

### 2026-09-15 · [BL-57] S162 close-out — the BL-57 plan approved and committed; P1 is next

- **Change:** S162's receipt is completed in `HANDOFFS.md` (self 7/10, predecessor S161 8/10). BL-57's
  row and note in `docs/planning/BACKLOG.md` and `BACKLOG-DETAIL.md` point at the plan; BL-47's
  `CHANGELOG.md` half is recorded as settled by Q2 A, and BL-56 as folded into the plan's P6.
  `HANDOFFS.md` now holds five receipts, and its own policy trims to four at the next Phase 0.
- **Commit/PR:** this commit (claim `7ea7346b`, plan `9292132e`, Learning #65 `64f085b2`)
- **Session:** S162 · **Verified:** `check-learnings` 0; `BACKLOG-DETAIL.md.verify.sh` 0;
  `check-handoff --all` 0 (5 receipts); `bin/tests.sh` on this content in a `--no-local` clone 304/1/0,
  exit 1, with 0 status flips against the Phase 0 baseline (the one failure is Test 9, pre-existing)
- **Model:** Claude Opus 5, 1M context (claude-opus-5[1m])

### 2026-09-15 · [BL-57] S162 — Learning #65: procedure written into a seed-once file cannot be corrected by the framework

- **Change:** `starter-kit/FRAMEWORK_LEARNINGS.md` gains row 65, the structural cause the BL-57 plan
  found (§1.2). Rules shipped inside a seed are frozen at each adopter's seeding, so every correction
  strands a copy: the two adopters whose ledgers still carry the rules both teach the pre-correction
  *silent* truncation, and their fenced examples inflate a line-based audit. The row is fork-only; the
  upstream PR adds none (plan K4).
- **Commit/PR:** this commit
- **Session:** S162 · **Verified:** `bin/check-learnings` exit 0 — 64 rows, contiguous, 0 over 1,500 B.
  Row 65 is 1,144 B; the file is 78,103 B, 3,817 B under the 81,920 B growth warning — about three more
  rows of this size
- **Model:** Claude Opus 5, 1M context (claude-opus-5[1m])

### 2026-09-15 · [BL-57] S162 — the BL-57 plan: one set of `CHANGELOG.md` rules, kept in one place (operator-approved)

- **Change:** `docs/planning/changelog-rules-contradictions-plan.md` (812 lines) plans the removal of
  the contradictions in the framework's `CHANGELOG.md` rules, here and in six adopters, through a new
  upstream PR once #80 merges. It inventories sixteen findings across fourteen files on three trees
  (`b82dcff`, `upstream/main`, fork `main`; 1,577 matching lines in 45 files on `b82dcff`) and six
  adopters, and sets twelve one-session phases, each with DONE criteria, verification commands, its
  surface and what that surface cannot enforce. **The operator's decisions (S162):** Q1 A, the rules
  move to one synced home, `FRAMEWORK_APPARATUS.md` §The Action Ledger, and the seed becomes a linked
  pointer with a format marker; Q2 A, archiving is optional; Q3 A, `[BL-<id>]` takes any backlog id;
  Q4 A, one entry per commit, never edited. Recommendations D5–D10 were approved with the plan.
  Planning only: nothing implemented, nothing outward-facing.
- **Commit/PR:** this commit
- **Session:** S162 · **Verified:** an independent read-only review found 4 errors, 9 risks and 6 nits
  in the first draft, each reproduced before it was fixed; §9.1 and §9.2 reproduce; the §9.3 and §9.8
  checkers catch every planted mutant; the links resolve; baselines at `b82dcff` (`bin/tests.sh` 115/1,
  450 unit tests OK, `check-links` OK) and fork `main` (304/1)
- **Model:** Claude Opus 5, 1M context (claude-opus-5[1m])

### 2026-09-15 · [ad hoc] Quality ratchet — the plan's Phases 1–4 built as one pre-declared vertical slice (PR opened, not merged)

- **Action:** implement [`docs/planning/quality-ratchet-plan.md`](docs/planning/quality-ratchet-plan.md)
  (PR #81, the plan; D1–D10) through its four buildable layers on branch `feat/quality-ratchet`, one
  checkpoint commit per layer with the full matrix at each boundary, and open a PR for review. Phases 5
  (adopter dogfood) and 6 (release) are separate sessions by the plan's own text. Session S20. **Checkpoints:**
  claim `5cd300e` · P0 `008d656` · P1 `628d218` · P2a `9d34485` · P2b `727d9ff` · P2c `d433739` · P3 `cca7941` ·
  P4a `bae6b05` · P4b `58babe6` · P4c `04044f1` · self-review `b4226d3` + `d24fb2c` · close-out (this commit).
  **Gate run cited in the receipt:** `quality_ratchet: 9/9 pass · results 74c773523dab · manifest 2424c429b2c6`.
  **§8 decisions** taken at the plan's recommendations (1 yes; 2 gitignored; 3 amend #17; 4 empty seed; 5 separate
  file; 7 separate plan) and listed in the PR body for the operator to reverse. **PR opened:**
  [#82](https://github.com/KJ5HST/methodology/pull/82) (a non-commit action; the branch pushed as `e13958d`).
- **P0 — preconditions (checkpoint 1).** `tools/test_context_budget.py`: `TestFitGateEndToEnd` skipped only
  when NO transcript existed, but `calibrate()` refuses to fit below 4 usable sessions — on this machine (2
  transcripts for the repo path) both tests ran and failed against *"not enough to fit"*, so `bin/tests.sh`
  read 115/1 on `main` (S19 gotcha 1); the class now asks the tool (a probe at an impossible floor) and skips
  on its "not enough". New `TestThisRepoReadSetPartition` (**G1** of the #80 re-review): the repo's own
  `.context-budget.json` per-file token ceilings in a whole-read class must sum to ≤ `read_cap_tokens` —
  RED first at 27,800 with the 22,000 mutant, OK at 25,000. And the read-set partition is **re-split
  19,200 + 5,800 → 18,900 + 6,100**: `SAFEGUARDS.md` was pinned at its exact size (5,800/5,800), which would
  have refused the one Blast Radius row D3 adds; 300 tokens move from the runner's margin. `--status` OK,
  `config_defects []`, budget suite 116 → **118** OK.
- **P1 — prose (checkpoint 2).** **D3** `starter-kit/SAFEGUARDS.md` Blast Radius gains one row: *never loosen a
  declared quality threshold to make a change pass — loosening requires plan mode approval; tightening never
  does*. **D4** `ITERATIVE_METHODOLOGY.md` gains §**Mechanical Gates Bind Every Actor** beside §Matching
  Reasoning Effort to Stakes — enforce on the artifact, not the actor; four consequences (never re-done by
  judgment or waived by tier; judgment reserved for what no gate expresses, before and after implementation;
  checks never pass by default or timeout; thresholds only tighten); cites the capability-tiered paragraph
  rather than duplicating it; states the ceiling (a floor without a faithfulness check measures effort).
  No principle, phase, or gate added — "9 principles / 6 phases / 12 quality gates" claims re-grepped, true.
  **D5** `starter-kit/SESSION_RUNNER.md` Phase 3C gains the mechanical branch: *a mechanical learning is a
  gate, not a row* (Learning #12 generalized from "test" to "gate"; the decay term FM #28 names).
  **D8** FM #17 gains one clause (loosening a threshold is erosion in mechanical form; `--no-verify` is a
  recorded bypass, not an exemption) and Degradation Detection gains one row — **FMs 1–28 byte-unchanged,
  count stays 28** (28 table rows re-counted). **Learning #15** appended to `starter-kit/FRAMEWORK_LEARNINGS.md`
  (1,331 B, under the 1,500 B row budget; `#14` stays reserved, callout reworded to "rows continue from
  #15"). **Cost, measured:** the Phase 0 pair is 70,066 B; doubled-file Read reports 49,643 → **24,822
  tokens, 99.3 % of the read cap** (the tool estimates 18,868 + 5,946 = 24,814 — within 8 tokens of the
  measurement); the runner sits 32 tokens under its 18,900 ceiling, so the next runner growth must be paid
  for by a reduction. `bin/check-links` 105 OK; `bin/check-learnings` OK (14 rows, contiguous with #14
  reserved); `bin/tests.sh` 116/0; dashboard unit 211 OK.
- **P2a — the tool (checkpoint 3).** New `starter-kit/quality_ratchet.py` (**D2**; 494 lines, stdlib only, no
  `--force`): `--precommit` refuses a staged `.quality-gates.json` whose thresholds are looser than `HEAD`'s
  (a `min` lowered, a `max` raised, a gate removed, a direction flipped); tightening and adding always pass;
  a changed `command`/`extract` warns (the ratchet holds thresholds, not commands). `--run` executes each
  declared gate (regex `extract` → the number; no `extract` → the exit code), writes a results file
  (`.quality-gates-results.json`, hash-stamped, time-independent hash) and prints a **citable summary line**
  (`quality_ratchet: N/M pass · F fail · U unmeasured · results <sha12> · manifest <sha12>`); a gate with
  no command is **unmeasured, never pass** (exit 1). `--status`, `--selftest` (17 checks, each observed
  failing and passing, incl. the installed hook refusing a loosening through real `git commit`),
  `install-hook` (honours `core.hooksPath`; prints the chain line for a foreign hook). New
  `starter-kit/quality-gates.json` seed (**§8.4 empty**, with the schema and one valid `_example`). New
  canonical-only `tools/test_quality_ratchet.py` — **33 tests** (pure ratchet arithmetic; config defects;
  measurement incl. the index-not-worktree rule and a 127 exit for a missing command; results/status;
  precommit through git; stdlib/no-force/selftest/seed invariants).
- **P2b — distribution (checkpoint 4).** `bin/_manifest.py` **27 → 29** rows (`quality_ratchet.py` TRACKED,
  `.quality-gates.json` SEED). Adding the rows with nothing else changed turned **6 guard tests RED** — the
  F2-generalized installed-file test (by name, and end to end for both files), the checklist
  scored-or-exempt invariant, and the exclusion-matches-manifest cross-reference — exactly the guards
  v3.6/v3.7/#80 built for this moment. Both scanner twins gain the two names in
  `FRAMEWORK_INSTALLED_SOURCE` (in manifest order — the cross-reference is order-sensitive) with their own
  `_FRAMEWORK_FILE_SIGNATURES` entries (the tool's `VERSION` regex + 4 signatures; the seed's `_example`
  keys), so a 494-LOC install cannot flip a document project to `code` (PR #71's lesson, measured by the
  real-file test); `CHECKLIST_EXEMPT` records why neither is scored. Twins byte-identical; 211 OK;
  `bin/sync` into a scratch tree installs both, `bin/status` reports `tracked current` / `seed present`;
  `bin/tests.sh` 115/1 — **Test 9 by construction** (`--source=github` reads `main`, which lacks the new
  starter-kit file until merge; the #80 shape).
- **P2c — install path and shell checks (checkpoint 5).** `bin/tests.sh` **116 → 128** checks: the unit suite
  wired in beside the budget suite, plus a `quality_ratchet.py` block that syncs a scratch adopter tree,
  declares one gate, installs the hook, and proves through real `git commit` that a loosened threshold is
  refused, `--no-verify` bypasses it, a tightening passes, removing the gate is refused, and a re-sync
  leaves the adopter's manifest alone — **RED first**: with `compare()` neutralized, the loosening
  committed. `starter-kit/BOOTSTRAP.md` Step 10 retitled *(Optional) → (Recommended)* and gains the
  ratchet paragraph (start where you are; chain after the ledger hook with one line; the results file and
  the receipt citation) plus a tool-agnostic per-stack table (Python/Node/Rust/JVM/Docs — the methodology
  ships the ratchet, not the ruler). `.gitignore` gains `.quality-gates-results.json` (**§8.2**: gitignored
  by default, with the reason). `bin/check-links` 105 → **107** (both new adopter-layout links resolve).
- **P3 — dashboard (checkpoint 6), `DASHBOARD_VERSION` 2.10.7 → 2.11.0, both twins byte-identical.** New
  `collect_gate_metrics` (**D6**): reads `.quality-gates.json` (declared count), the results file where it
  exists (pass/fail/unmeasured, a `manifest`-hash staleness check, a passing gate named *coverage*), and a
  **git-only** loosening history (`git log -- .quality-gates.json`, capped at 50, each pair diffed for a
  lowered floor / raised ceiling / removed gate — the scanner never executes a project command, and a test
  proves it with a `touch`-marker gate). Advisory risks: *N declared, never run here* (medium); *results
  predate the manifest* (low); *K of N measured outside their threshold: names* (high); *unmeasured (no
  command)* (low); *threshold `x` floor lowered a → b in `sha` (date) (+k earlier) — thresholds only tighten*
  (medium). `score_health`: a **measured** passing coverage gate earns +2 on top of configured coverage's
  +2, cap unchanged — the first number, not file-existence, the scanner scores; doc-only repos keep their
  render slot. Card: a *Quality Gates* row beside *Coverage Config*. **Silence is deliberate**: no manifest,
  and the **empty seed** every synced adopter receives, produce no risk. 11 new tests
  (`TestQualityGateSignals`), **RED first against the 2.10.7 scanner: 11 ran, 2 failures + 7 errors**; unit
  suite **211 → 222** OK. **Fleet delta: 27 repos re-scanned under 2.10.7 and 2.11.0 — 0 changed class,
  score, or risk set** (none has a manifest). `bin/tests.sh` 127/1 (Test 9 by construction).
- **P4a — workstreams and the honesty citation (checkpoint 7).** `workstreams/DEVELOPMENT_WORKSTREAM.md`: Step 4's
  "what's the current standard?" now has its answer (the declared floors/ceilings in `.quality-gates.json`;
  measure and declare at the current value where none exist) and *Code Health Metrics* is generated by
  `quality_ratchet.py --run`, not hand-filled. `workstreams/AUDIT_WORKSTREAM.md`: anti-pattern **#10 "Findings
  that stay prose"** (list was 1–9) — a mechanical-invariant finding becomes a declared gate. **D9**:
  `starter-kit/HANDOFFS.md` documents the gate-run citation (the `quality_ratchet: N/M pass · …` summary line
  in `runtime_smoke`) and the Phase 0 comparison of the cited counts against the results file, with the
  v3.3-style ceiling (structure at lint, counts at reconcile, truth of nothing a gate does not express);
  `bin/check-handoff` gains the lint — when a manifest beside the ledger declares ≥ 1 gate, the **newest**
  complete receipt must carry the token (newest-only, so receipts written before the manifest are not
  re-judged and `--all` stays green on history). Observed in a scratch ledger: silent with no manifest and
  with the empty seed; FAIL with one gate and no citation (both modes); OK once cited.
- **P4b — this repo dogfoods the ratchet (checkpoint 8).** Root `.quality-gates.json` declares **9 gates at
  their current measured values** — `tests-sh-passed ≥ 134`, the four unit-suite counts (dashboard ≥ 222,
  budget ≥ 118, trimmer ≥ 123, ratchet ≥ 33), and five exit-code gates (`check-links`, `check-learnings`,
  `check-handoff --all --allow-pending`, `commit-msg --selftest`) — with `tests-sh-failed ≤ 0` recorded as the
  **first tightening owed after merge** (Test 9 is red by construction on the branch, and a gate declared
  red teaches bypass). First `--run`: **9/9 pass**. `.githooks/pre-commit` chains `--precommit` before the
  ledger gate — **observed live in this repo**: a staged floor 127 → 100 was refused with the bypass cost
  printed, then reverted. `bin/tests.sh` 128 → **135** checks: the manifest parses with no defects and
  declares gates; the hook chains the ratchet; the D9 lint observed silent (no manifest; empty seed),
  failing (one gate, no citation — both modes) and passing (cited).
- **P4c — completeness sweep (checkpoint 9; Learning #10).** Every site that enumerates the distributed corpus
  now names the ratchet — and, found by the same sweep, the two tools that v3.7/#80 shipped **without ever
  reaching these lists**: `README.md` (§Option A/B copy lists, the repo tree — `starter-kit/` gains
  `methodology_trim.py`, `context_budget.py` + `context-budget.json`, `quality_ratchet.py` +
  `quality-gates.json`; `tools/` gains the three canonical-only unit suites), `CLAUDE.md` (starter-kit and
  tools tables), `docs/tutorials/T1_setup.md` (the expected-result file list and the seeds), and
  `HOW_TO_USE.md`'s Phase 3C line (the mechanical branch). No count claim moved. `bin/check-links` 107 OK.
- **Self-review (checkpoints 10–11), before the PR.** (a) The gate run is now a named close-out step everywhere
  close-out is enumerated (Learning #8): `SESSION_RUNNER.md` 3E (one line — `--run` is the smoke test's
  mechanical half; cite its summary line), `ITERATIVE_METHODOLOGY.md` Phase 6 step 8 (c), `HOW_TO_USE.md` 3E.
  (b) Learning #15's *"26 of 28 failure modes bind by text alone"* put in the past tense — this ratchet is
  what changes it. (c) **Two budget consequences, paid by reduction, not by a raised ceiling** (the rule this
  PR adds): the P4c table rows had pushed `CLAUDE.md` **984 B over its arrival-size pin** (59,168 B — the F3
  class flagged on #80); six existing rows/bullets were tightened and it reads **59,153 B, 15 under**;
  the runner's two new lines were shaved so it sits at 18,878 / 18,900 tokens. Measured pair after the
  trims: doubled Read **49,683 → 24,842 tokens** (99.4 % of the cap; tool estimate 24,824, within 18).
  `context_budget.py --status` OK, exit 0. (The ledger hook refused the CLAUDE.md commit until this line was
  co-staged — the fast path working as designed.)

### 2026-09-15 · [ad hoc] Merged PR #80 — the read-set budgets series (#76–#79)

- **Action:** merge [PR #80](https://github.com/KJ5HST/methodology/pull/80) (rmsharp) at head `aa36fd8` into
  `main` with a merge commit, the repo's convention. Preceded by the internal review of 2026-09-14 (F1–F6,
  posted as one comment by S18) and the internal re-review of 2026-09-15 of the four answering commits
  (`5c9f0f3`/`d4e1570` F1 (a), `3774076` F2, `aa36fd8` F3), which returned **merge** with one new
  non-blocking finding (G1: the read-set token partition is prose-only since the byte class ceiling left).
  Session S19. **Merge commit `4d9e271`** (parents `e5e2661` + `aa36fd8`), read back from the API.
- **Verified on the merged `main`:** `bin/tests.sh` 115 / 1 — Test 9 now **passes** (main has the three new files);
  the one failure is `tools/test_context_budget.py` `TestFitGateEndToEnd`, **environmental** (this machine has exactly
  2 transcripts for the repo path: enough for the test to run, too few for `calibrate()` to fit; the test file and tool
  are identical at `aa36fd8` and here, and a worktree path skips it) — fix queued as the next session's first step.
  Dashboard unit 211 OK; trim unit 123 OK; `check-links` OK; `check-learnings` OK (13 rows); `commit-msg --selftest`
  OK; twins byte-identical at `DASHBOARD_VERSION` 2.10.7; `context_budget.py --status` OK, exit 0. Adopters now
  receive 27 manifest rows on their next `bin/sync` (24 → 27; corpus 659,755 → 839,383 B).
- **Deferred to the next Orient by design:** 11 `status: reconciled` receipts for #80's non-merge commits, the
  one-time ledger reorder S15's below-`main` placement made necessary, and the v3.8 release PR.

### 2026-09-15 · [ad hoc] Posted the PR #80 review findings to the PR (non-commit action)

- **Action:** one maintainer comment on [PR #80](https://github.com/KJ5HST/methodology/pull/80) carrying the
  six findings of the 2026-09-14 review (internal, oversight venue): **F1** the Learnings payload —
  `starter-kit/FRAMEWORK_LEARNINGS.md` ships 46 rows (13 canonical + the fork's #15–#47) while the PR body says
  rows #1–#13; **F2** the `methodology_trim.py` doc-only exclusion is unguarded at the predicate level (RED-shown);
  **F3** the shipped root `.context-budget.json` reports the PR's own headline OVER; **F4–F6** optional
  (two limits on one file; a docstring describing the fork; the `--source=github` wording). Reproduction
  commands included; nothing merged, nothing changed on the branch. Session S18: claim `75405be` + the
  close-out commit. Comment: <https://github.com/KJ5HST/methodology/pull/80#issuecomment-5674670153> (read back via the API).

### 2026-09-15 · [ad hoc] PR #80 review F3: the root `.context-budget.json` holds the Phase 0 pair to the read cap in tokens at its measured density, and drops the two ledgers it could only report as over

- **Change:** `.context-budget.json` only — this repository's own config, which `bin/_manifest.py` does not
  distribute (adopters receive the seed, `starter-kit/context-budget.json`, unchanged).
  `starter-kit/SESSION_RUNNER.md` and `starter-kit/SAFEGUARDS.md` trade their byte ceilings for token
  ceilings at densities measured by the doubled-file method — 19,200 + 5,800 tokens, which partition the
  25,000-token read cap — and the `read-set` class keeps its total as a measurement but declares no byte
  ceiling, because `class_ceiling()` can only take a typed byte total or derive one at the 2.27 B/token
  floor. `CHANGELOG.md` and `HANDOFFS.md` leave `files[]` for `_deliberate_exclusions`, with the reason
  and the command that recovers their entries.
- **Why:** F3 of the review ([comment](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5674670153)):
  `context_budget.py --status` printed OVER at the head — for the pair the headline says fits, and for
  both ledgers — and wired as a gate it would have refused every ledger append. The operator chose the
  review's answer (i) for the pair, and for the ledgers a fourth: a ledger is read in part, and in a
  whole-read class `token_ceiling()` clamps every file to the 25,000-token cap, so answer (ii) left both
  ledgers over and its pin refused the next append (measured).
- **Measured on both trees** — this branch, and its merge into `main` at `9fa3141`: `--status` exits
  **0 (OK)** on each, where it exited 2. `--precommit`: a 300 B append to either ledger passes; the
  runner passes +100 B and is refused at +2,100 B (19,220 tokens against 19,200); `SAFEGUARDS.md` is
  pinned at its size in the merge; a shrink passes. The merged pair is 68,548 B and 24,278 tokens,
  967 B more than this branch's 67,581 B — `main`'s own S16 paragraph in `SAFEGUARDS.md`.
- **Placed** with this PR's own entries, above F2's, below `main`'s.
- **Commit:** this commit, on `read-set-budgets` (PR #80)

### 2026-09-15 · [ad hoc] PR #80 review F2: the doc-only exclusion is tested for every non-markdown file `bin/sync` installs, from its real `starter-kit/` source

- **Change:** `tools/test_methodology_dashboard.py` only — canonical-only, so adopters receive nothing,
  and neither scanner twin changes. `test_a_synced_repo_with_context_budget_installed_is_still_doc_only`
  is generalized in place as `test_a_synced_repo_with_each_installed_source_file_is_still_doc_only`.
  Every non-markdown dest in `bin/_manifest.py`'s `DISTRIBUTION` (today `methodology_dashboard.py`,
  `methodology_trim.py`, `context_budget.py`, `.context-budget.json`) is written from its real
  `starter-kit/` source into the Quarto doc-only fixture, one at a time and then all together, and must
  leave `source_loc` 0, `doc_only` true and no "No test infrastructure" risk; each must also pass
  `is_framework_installed` directly. The names come from the manifest, not `FRAMEWORK_INSTALLED_SOURCE`,
  so a file the manifest installs and the scanner does not list fails here by name; a last assertion
  checks the test covered exactly the scanner's list. Still 211 tests — the names are subtests.
- **Why:** F2 of the review ([comment](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5674670153)):
  with `methodology_trim.py`'s `version_re` and four signatures neutralized in both twins, the suite
  stayed OK (211) while a synced doc-only fixture read `code` with the false HIGH.
- **RED first.** Six mutants, each planted in both twins of a clone, the old and the new suite run
  against each; controls 211 OK on both sides, the clone verified clean after every mutant:
  - M1, the review's mutant: old **OK (211)**; new FAILS — `2181 != 0` source LOC, alone and all together.
  - M2, the same neutralization of `context_budget.py`: old fails 2; new fails 3.
  - M3, the same of `methodology_dashboard.py`: old and new fail the same 12. **Not this test:** the
    neutralized strings sit in the scanner's own signature table, so the real file still matches itself;
    the stand-in fixtures catch it. The docstring says so.
  - M4, `.context-budget.json`'s signatures neutralized: old **OK (211)**; new FAILS on the direct
    predicate call — the file is `config`, so end to end it cannot fail.
  - M5, `methodology_trim.py` dropped from the tuple and the table: old fails 1; new fails 4, this test
    by name.
  - M6, the one `collect_all` call site skipping `methodology_trim.py`, predicate untouched: old **OK
    (211)**; new FAILS end to end.
- **Placed** with this PR's own entries, above F1's, below `main`'s.
- **Commit:** this commit, on `read-set-budgets` (PR #80)

### 2026-09-15 · [ad hoc] PR #80 review F1 (a), step 2: `FRAMEWORK_LEARNINGS.md` ships rows 1–13 and the reserved `#14`, as this PR's description says

- **Change:** rows #15–#47 — 33 learnings from the contributor's fork, 32 of them citing fork sessions —
  leave the distributed `starter-kit/FRAMEWORK_LEARNINGS.md` (56,673 → 13,983 B). Rows 1–13 are
  byte-identical to what this PR carried. The `#14` callout stays, reworded because no row 15 exists now:
  the next row appended is `#15`, and its two sentences about fork sessions S34 and S35 are gone.
  `bin/check-learnings`' comment quoting the old callout follows it. The fork keeps its rows in its own
  copy; any of them can come upstream later, one PR at a time.
- **Why:** F1 of the review ([comment](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5674670153)),
  option (a), the reviewer's default, taken by the contributor: the canonical numbered set grows one row
  at a time, and this PR's description says 13 rows.
- **Placed** above step 1, with this PR's own entries.
- **Verified:** `bin/check-learnings` exit 0 — *"13 Learning row(s), contiguous 1..13; all citations
  resolve"*; a `Learning #20` planted in `starter-kit/SAFEGUARDS.md` is caught (exit 1, *"cites Learning
  #20, which does not exist"*) and the restored tree passes. `bin/check-links` OK (105 links, 23 files);
  `tools/test_methodology_dashboard.py` 211 OK; `context_budget.py --status` reports the file `ok` at
  13,983 of 73,728 B.
- **Commit:** this commit, on `read-set-budgets` (PR #80)

### 2026-09-15 · [ad hoc] PR #80 review F1 (a), step 1: citations of Learnings past #13 now state their rule, before the table keeps only rows 1–13

- **Change:** comments and two docstrings, in three files; no behaviour changes. The review of this PR
  ([comment](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5674670153), F1) asks that
  `starter-kit/FRAMEWORK_LEARNINGS.md` ship rows 1–13 plus the reserved `#14` rather than 46 rows. Before
  that cut, every citation it would leave dangling is rewritten to state the rule instead of a number:
  `starter-kit/context_budget.py:77` and `:378` (Learning #34) and `:409` (*"learning #22 / #26a"* — this
  table has no `#26a`, and its #22 is about backlog deletion, so the pair cites another numbering);
  `tools/test_context_budget.py:489`, `:546`, `:563` (#34); `tools/test_methodology_trim.py:1244` (#16)
  and `:2063` (#43).
- **Why:** `bin/check-learnings` sweeps only the Markdown files of the distributed corpus
  (`distributed_md_files`), so the two `context_budget.py` citations — a file every adopter receives —
  would have dangled with the check green. Repaired first, so no commit carries a dangling citation. The
  `Learning #N` mentions past 13 that remain are history (the #28/#29/#30/#34 that never existed, in
  `CLAUDE.md`, `README.md` and `bin/check-learnings:36`), a planted test value (`bin/tests.sh`, #4242),
  and a dated audit citing another project's numbering (`docs/audits/2026-05-02-mattpocock-skills-evaluation.md`).
- **Placed** with this PR's own entries, below `main`'s, for the reason the conflict-resolution entry at
  the top of this ledger gives: an entry prepended at the top re-conflicts with the next `main` prepend.
- **Verified:** `starter-kit/context_budget.py` and `tools/test_methodology_trim.py` parse to an AST
  identical to `b82dcff`'s; `tools/test_context_budget.py` differs in exactly the two docstrings.
  `tools/test_context_budget.py` 116 tests OK, `tools/test_methodology_trim.py` 123 OK,
  `context_budget.py --selftest` exit 0, `bin/check-learnings` exit 0.
- **Commit:** this commit, on `read-set-budgets` (PR #80)

### 2026-09-14 · [BL-57] S162 claim — plan BL-57: remove the contradictions in the framework's `CHANGELOG.md` rules, here and in six adopters, aiming at an upstream PR

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: a plan in
`docs/planning/` for BL-57 (`docs/planning/BACKLOG-DETAIL.md`, anchor `bl-57`) — a grep inventory taken
on the upstream target tree as well as fork `main`, per-phase DONE criteria naming each phase's surface,
one session per phase — presented to the operator for approval before it is committed. The operator
chose it at this session's Phase 0 (option A of three) and set the deepest reasoning mode. **Nothing is
implemented, and nothing is outward-facing: no push, no PR, no comment.** Upstream moved today and the
plan starts from it: PR #80's head is `b82dcff` (the maintainer merged `main` into it to clear a
`CHANGELOG.md` conflict), its review is private and pending (F1–F3), and upstream's S16 receipt proposes
a `CHANGELOG.md` heading-count ratchet that would refuse every trim (`aaa6d30` took the headings
80 → 27). Fork `main` now conflicts with `upstream/main` in `CHANGELOG.md` and `HANDOFFS.md`. Carries
the Phase 0 `dashboard_history.jsonl` snapshot.

### 2026-09-14 · [ad hoc] Operator decision: do not trim `CHANGELOG.md`

The operator decided not to trim this ledger, although `methodology_trim.py --check` fires — the file
is past the tool's 196,608 B Class A trigger. It follows the same day's decision that sessions reach the
ledger through git and never read it whole (`3c8acd5`), and S112's precedent of declining a trim that
buys nothing (BL-52). **Expected from now on:** `--check` keeps exiting 1 and the dashboard keeps
showing the trigger; past 262,144 B a default `Read` returns nothing, so read the file with
`offset`/`limit` — verified today on `nprcgenekeepr`'s 413,383 B ledger. Recorded in the S161 receipt's
item (1), in BL-57 (whose plan settles the archive rule), and in memory. Nothing was trimmed.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-14 · [ad hoc] S161 follow-up — BL-57 raised as HIGH PRIORITY on the operator's request: the `CHANGELOG.md` rules contradict each other; a planning session comes next, aiming at an upstream PR

The operator asked for the contradictions to be logged, and for a high-priority future session to plan
removing them in this repo and in `airqino`, `model_project_constructor`, `mts-system`,
`nprcgenekeepr`, `vscode_quarto_ext` and `wsfct`, with the intent of an upstream PR or adding to one.
**BL-57** (`docs/planning/BACKLOG-DETAIL.md`, index row in `docs/planning/BACKLOG.md`, marked HIGH
PRIORITY) records eight contradictions with every cited line re-read today, and a per-repo table of what
the rollout will meet, measured read-only: `nprcgenekeepr` and `wsfct` carry copies of the seed's rules
text, which `bin/sync` never rewrites; three adopter ledgers are already past the 262,144 B default-Read
refusal; four adopters use their own tag styles. A first survey counted "65,536" anywhere in each file
and a second stopped at the seed's example headings, so the table was taken from raw match positions.
The S161 receipt's item (1) now names the planning session first. No plan was written and no other
repository changed.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-14 · [ad hoc] S161 follow-up — `HANDOFFS.md` back to four receipts: the pointer block folded into the archive table

On the operator's request (*"trim HANDOFFS"*), under the retention policy at `HANDOFFS.md:8` (5
receipts against 4). The trim itself is the tool's own entry below (`16ac3fc97`: S157 to
`docs/archive/HANDOFFS-through-2026-09-09-2.md`, 58,802 → 50,737 B, SRF 0.9849 vs `cd52df7` — no
`SRF_RED`, no `--force`). Nothing was added to the ledger before trimming: about 308 B more would have
taken SRF past 1.0 and into the refusal. This commit folds the generated pointer block into the archive
table as one row — in its own commit, since inside the trim commit the shard's proof fails L2 (Learning
#58) — so the table reads 16 trims and 146 receipts, each row cross-checked against the fence count of
the shard it names. The S161 receipt's item (1) now says the `HANDOFFS.md` half is done;
`CHANGELOG.md`'s trim remains the operator's decision.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-14 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-09-2.md` (1 record(s), 58,802 B → 50,737 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-09 → 2026-09-09) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-09-2.md`](docs/archive/HANDOFFS-through-2026-09-09-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-09-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-09-2.md.verify.sh)
rather than trusting a digest printed here. Live file 58,802 B → 50,737 B (−13.7%).

### 2026-09-14 · [ad hoc] S161 follow-up — BL-47 and BL-52 updated now that `CHANGELOG.md` has left the read budget; one false clause in the exclusion note corrected

On the operator's request. **BL-52** gains a fourth addendum: the operator has now decided its byte
half for this repo's `CHANGELOG.md` (`3c8acd5`), on the reasoning its own S98/S112 measurements
supplied (one whole-file read per root ledger in 85 transcripts). It records what stays open: the
trimmer's 196,608 B Class A trigger, which lives in the distributed tool and still fires; the
262,144 B default-Read refusal, the boundary BL-52 says actually bites, about 58 KB away;
`HANDOFFS.md`, still in the budget; and this ledger's own archive rule, still stated against the
2,000-line read-cap proxy. **BL-47** gains a note that its premise moved twice: this repo's config no
longer lists `CHANGELOG.md`, and the trimmer has budgeted to 196,608 B since S116, not 65,536 B.
**Corrected:** the exclusion note said `HANDOFFS.md`'s 65,536 B "backs" `bin/check-handoff`'s
`CEILING_BYTES`; that checker has its own constant and never reads the config, so the entry only
mirrors it. `BACKLOG-DETAIL.md.verify.sh` covers only BL-32 and BL-36, so neither backlog edit touches
its proof.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-14 · [ad hoc] S161 follow-up — `CHANGELOG.md` removed from this repo's read budget on the operator's decision: sessions reach it through git, never read it whole

The operator's rationale: a session looking for something in `CHANGELOG.md` greps it or runs git, so
only those results enter its context — the file is never read whole. The runner agrees: Phase 0 step 6
takes the reconcile's frontier and gap from `git log`, and Phase 3F prepends under the topmost month
heading. So `.context-budget.json` no longer declares it `read-mandated`: its entry (65,536 B, 2,000
lines, 25,000 tokens, plus a heading-shape check) is removed, the reason recorded in
`_deliberate_exclusions`, the old entry recoverable with `git show bb6eb72:.context-budget.json`.
Asserted before writing: the file parses, `files[]` went 7 → 6, and nothing else changed.
`context_budget.py` still exits 2 — rows diffed against the run before the edit: only `CHANGELOG.md`'s
row left, findings 24 → 15, and the reds that remain are the known ones (`SESSION_RUNNER.md` and the
Phase 0 read-set total). **Its size is still bounded:** `methodology_trim.py`'s own 196,608 B trigger
still fires, so S162's trim stands. `HANDOFFS.md` keeps its entry. Canonical-only config; no test reads
it. The checker's two runs, before and after, are appended to `.context-budget-history.jsonl`,
committed here as that append-only history always has been.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-14 · [ad hoc] S161 follow-up — BL-56 raised on the operator's request: rewrite `airqino`'s `CHANGELOG.md` to the current ledger format

The operator asked for a backlog item, not the rewrite. **BL-56** (`docs/planning/BACKLOG-DETAIL.md`,
index row in `docs/planning/BACKLOG.md`): `airqino`'s `CHANGELOG.md` (1,309 B) reads *present (stale
format)* under both `bin/status` versions — it lacks both markers the current seed carries — and the
Route A sync (`dfe26fd17` in `airqino`) left it as it was, since `bin/sync` never rewrites a seed. It
holds one dated entry, the sync's own, so reseeding and carrying that entry across is the cheap remedy
(`starter-kit/BOOTSTRAP.md:86`). Nothing in `airqino` was changed.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-14 · [ad hoc] S161 follow-up — `airqino` synced by Route A on the operator's request: every tracked file current, on a new local branch

Using the S161 document's Route A (`docs/planning/read-set-budgets-local-use-routes.md` §6), from a
pristine full clone of `upstream/read-set-budgets` at `598c459`. The operator chose a new branch,
`chore/methodology-read-set-budgets`, off `airqino`'s open PR #1 branch
(`chore/methodology-pr2527-remediation`, `0c59e5e9`) — the only branch whose files sync without
`--force`, since `main`'s `SESSION_RUNNER.md` and `SAFEGUARDS.md` match no published version. A dry
run against the real project first matched the scratch-copy result exactly. The sync updated 10
files, added 8 and created 2 seeds; `bin/status` now reads every tracked file `current`. Committed in
`airqino` as `dfe26fd17` — 21 files, one commit for one tool-generated sync, with an entry in
`airqino`'s own `CHANGELOG.md`; its two pre-existing untracked files were left untouched. **Not
pushed; PR #1 and `main` unchanged.** The S161 receipt's item (3) records it.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-14 · [ad hoc] S161 follow-up — BL-55 raised on the operator's request: nothing enforces removing a completed `BACKLOG.md` item

After S161's close-out (`a5ba9ea`) the operator asked for the backlog item its receipt had offered.
**BL-55** (`docs/planning/BACKLOG-DETAIL.md`, index row in `docs/planning/BACKLOG.md`): the removal
rule is required in five places, `starter-kit/SESSION_RUNNER.md:284` first, and checked by none; the
dashboard's Signal F only reports done-marked items. Measured with Signal F, `nprcgenekeepr` went from
28 done-marks (2026-09-11) to 0 after its S687 removed them by hand on 2026-09-14, and its `BACKLOG.md`
from 218,350 B to 102,069 B. A gate keyed on the `[BL-N]` tag would miss that project: its backlog
names no `BL-` id, and 5 of its 322 tagged ledger entries carry one. Options are costed in the item,
none decided; the S161 receipt's item (6) now points to it. The operator's other question — could
Route A run on six named projects — was answered with no change made: re-checked on fresh copies, it
is clean only for `airqino`, identical to 2026-09-11. **Fork-internal; no project was written to.**

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-14 · [ad hoc] S161 close-out — local use of `read-set-budgets` answered; `CHANGELOG.md` now past its trim trigger, so S162 has both ledgers to trim

**The deliverable is done, approved and committed** (`14ffe204`); Learning #64 and BL-54 followed
(`0c81e399`). The S161 receipt carries the verification record, and this entry closes the claim's
`CHANGELOG: pending`. **This entry keeps `CHANGELOG.md` past its 196,608 B trigger, as the operator
chose at Phase 0** — it was 197,584 B before this entry — and `HANDOFFS.md` now holds five receipts
against its policy of four, so **S162 opens with both ledgers to trim.** **One regression, mine,
caught before this close-out:** the claim stub's `key_files` carried no `path:line` token, so
`bin/tests.sh` Test 34 read three extra failures at `18957077f`, `14ffe204` and `0c81e399` (301/4 at
`0c81e399`, found by an intermediate run; S160's claim-time ledger, as a control, passes). This
close-out's receipt replaces the stub, and the live ledger passes `check-handoff --all`. Claimed 2026-09-11 and closed
2026-09-14; before committing the document the session re-checked that nothing it measured had moved
(PR #80 OPEN, 0 reviews, 0 comments; `upstream/main` `512c2ed`; `origin/main` `f8531cf`). It also
answered the operator's mid-session question, read-only: completed `BACKLOG.md` items must be removed
(`starter-kit/SESSION_RUNNER.md:284`), but nothing enforces it — the dashboard's Signal F only reports,
and on `nprcgenekeepr` it counts 28 done-marked items. **Fork-internal: nothing pushed, no PR, no
comment.**

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-14 · [ad hoc] S161 — Learning #64 (a dry run into an empty target cannot exercise a refusal), and BL-54 raised (`bin/sync`'s history walk misses a merge's other side)

Two records of what the deliverable found. **Learning #64** (`starter-kit/FRAMEWORK_LEARNINGS.md`,
952 B): S160 recorded the branch route as working from a dry run into an empty project; run against
copies of the twelve real projects it synced 3 and refused 9. `bin/check-learnings` exit 0, 0 rows over
1,500 B. The file is 76,959 B against its 81,920 B growth warning — **4 rows of room** at BL-53's
1,239 B median. The row is distributed: it reaches projects that sync from fork `main`. **BL-54, raised
on the operator's go-ahead** (`docs/planning/BACKLOG-DETAIL.md`, index row in
`docs/planning/BACKLOG.md`): `bin/sync:60` and `bin/status:56` walk history without `--full-history`, so
a version that exists only on the merged-in side of `213f841` reads as locally modified — measured on 4
files for each of the 3 projects synced from the branch and then from fork `main`. Recorded, not fixed;
neither file is distributed. `BACKLOG-DETAIL.md.verify.sh` exit 0.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-14 · [ad hoc] Housekeeping — merged branches and stray refs deleted (non-commit actions)

- **Deleted, all verified merged into `main` by `git branch --merged` first:** local `docs/quality-ratchet-plan`,
  `feat/context-budget`, `feature/protocols-as-first-class-upstream`, `fix/issue-32-phase2-link-reconciliation`,
  `fix/issue-32-phase3-sync-coverage`, `fix/issue-32-phase4-status-per-file`, `fix/issue-36-check-links-no-mutate`;
  remote `origin/docs/quality-ratchet-plan` (#81), `origin/fix/issue-67-stale-version-remedy` (#73),
  `origin/release/v3.7` (#74); the stray `refs/remotes/pr/63` (merged long ago). Also the local tracking copy
  of `read-set-budgets` created in S15 — `origin/read-set-budgets` is PR #80's head and is untouched.
- **Kept, deliberately:** `docs/operator-gated-review-plan` (3 unpushed commits; reserves Learning #14) and
  `experimental/pocock-audit` (17 unmerged commits, 2026-05-02) — both are the maintainer's to decide.
- **Not done:** no history rewrite. The S16 truncated commits (`356556f`, `ad7bd37`, `ed9ab7e`) stay in
  `main`'s history with the repair `ed98444` on top; removing them would force-push a public branch with a
  fork downstream and is not a housekeeping call. Session S17: claim `b3c9e9d` + the close-out commit; the
  ref list above is the post-deletion read-back (`git branch -a`: 3 local, 2 remote; #80 OPEN/MERGEABLE).

### 2026-09-14 · [ad hoc] Shipped `.githooks/commit-msg` — the disclosure gate (FM #16's honesty counterpart)

- **Change:** new `.githooks/commit-msg` (canonical-only, like the ledger hook beside it — `.githooks/`
  is in no `bin/_manifest.py` row) + a short "Disclosure Hook" paragraph in `starter-kit/SAFEGUARDS.md`
  (distributed). When `AI_AGENT`, `CLAUDECODE`, or `CLAUDE_CODE_SESSION_ID` is in the environment — or
  `METHODOLOGY_REQUIRE_COAUTHOR=1` — the commit message must carry a well-formed
  `Co-Authored-By: <name> <email>` trailer outside comment lines; otherwise the hook is silent, so a
  human committing by hand is never asked to disclose an agent that was not there. `--no-verify`
  bypasses once; `METHODOLOGY_REQUIRE_COAUTHOR=0` disables. Built-in `--selftest` (7 checks).
  Session S16: claim `356556f`, hook + SAFEGUARDS `ad7bd37`, plus the close-out commit completing this entry.
  SAFEGUARDS.md grows by the one paragraph; the Phase 0 pair PR #80 measures stays under its cap
  (checked at close-out against the branch's own figure).
- **What the trailer is, and is not:** the agent never takes credit. The human is the author of every
  commit and owns it. The trailer is *disclosure* — so that no reader of the history is misled about
  how the work was produced. Disclosure was an instruction every session had to remember on every
  commit — an actor-side rule, the class the quality-ratchet plan (§3) says does not scale; under a
  harness this makes forgetting it impossible. The first draft of this entry framed the trailer as
  the agent's credit; the maintainer corrected it before anything was pushed.
- **Deferred, deliberately:** wiring `--selftest` into `bin/tests.sh` and the `BOOTSTRAP.md` Step 10
  mention wait for PR #80, which edits both files (S15 just un-conflicted it).
- **Incident, same session:** the script that reframed this entry sliced the file to the next `---`
  line — which is not the next entry boundary but a separator 316 lines down — and **deleted the ten
  entries between here and 2026-08-10** (S15, S14, S13, the v3.7 release, issue #67, and five more) in
  the amended claim `356556f`, carried by `ad7bd37` and `ed9ab7e`, all pushed. Found by the S15
  merge-tree check re-conflicting where it should not have; restored from `f8fc3ca` by the commit
  after `ed9ab7e` — `diff` against `f8fc3ca` shows 0 lines removed, 21 added (this entry), 41 headings,
  55 source tags. The co-staging hook cannot see this: it checks that the ledger was *touched*, not
  that it did not shrink. A ledger-count ratchet (staged `### ` headings ≥ HEAD's) is the mechanical
  fix and is proposed, not shipped, in the S16 receipt.

### 2026-09-14 · [ad hoc] Resolved the CHANGELOG.md conflict S13/S14 created for PR #80

- **Change:** `main` merged into the PR #80 head branch `read-set-budgets` (which lives in this repo) with
  the one conflicting file, `CHANGELOG.md`, resolved as a union in ledger order — today's S13–S15 entries
  on top, #80's four entries (2026-09-02..04) below them, everything else common. No other file conflicted
  (`git merge-tree --write-tree --name-only origin/main origin/read-set-budgets` → `CHANGELOG.md` only).
  Session S15: claim `8fdc50f` (main) → resolution merge `b82dcff` (pushed to `origin/read-set-budgets`)
  → close-out commit on main. Union verified: 57 source-tagged entries = the branch's 54 + today's 3.
  `git merge-tree` empty after the push and again after the close-out prepend.
- **Why:** #80 was MERGEABLE/CLEAN at `512c2ed` this morning; S13/S14's ledger and receipt commits
  prepended at the same anchor #80 prepends at, so the first session to record anything on `main` after
  #80 opened made it conflict — S13 should have computed that before merging PR #81 (Learning #13) and did
  not. Ordering #80's entries below today's, rather than above, is what stops the next `main` prepend
  from re-conflicting: the two hunks are no longer adjacent.

### 2026-09-14 · [ad hoc] Redacted the quality-ratchet plan to its published source only

- **Change:** `docs/planning/quality-ratchet-plan.md` — every statement derived from the maintainer's
  private correspondence with the article's author removed (the S13 version had paraphrased it, never
  quoted it). The article <https://campusiq.com/blogs/everybody-ships> is now the plan's only source for
  CampusIQ's practice. 15 edits, 425 → 410 lines; residue grep for correspondence-derived phrasing: 0 hits.
  Session S14, committed directly on `main` (the S12 close-out precedent): `4a5aab0` (claim), `762e7bc`
  (redaction), plus the close-out commit completing this entry and the S14 receipt. PR #81's body was
  edited to match. Hook ran clean on every commit.
- **Why:** the maintainer was no longer sure the exchange was not in confidence. Removing it from the live
  record is cheap and reversible; publishing it is neither. Git history (`993aa89`, PR #81) retains the
  S13 text — stated in the receipt, not hidden.

### 2026-09-14 · [ad hoc] Published the quality-ratchet plan — what the methodology should take from CampusIQ's Forseti layer

- **Change:** new `docs/planning/quality-ratchet-plan.md` (canonical-only planning record; not in
  `bin/_manifest.py`, so adopters receive nothing via `bin/sync`). No framework file changed; nothing
  implemented. Session S13; branch `docs/quality-ratchet-plan` → [PR #81](https://github.com/KJ5HST/methodology/pull/81)
  → merge `db121ce` (2026-09-14). Commits: `f62699a` (claim), `993aa89` (plan), `db121ce` (merge), plus the
  close-out commit completing this entry and the S13 receipt. All three session commits ran the ledger
  co-staging hook clean — no `--no-verify` (the first session since S8 to do so; the entry was written
  at claim and completed here).
- **Source:** Aaron Benz, *"Everybody Ships: How CampusIQ Built an AI-Native Company"*,
  <https://campusiq.com/blogs/everybody-ships> — quoted verbatim; the maintainer's correspondence with
  the author is paraphrased as personal communication, never quoted.
- **The finding the plan records:** CampusIQ enforces quality on the *artifact* — the same 130+ checks
  for every actor, thresholds that only tighten, checks that never pass by default — while this
  methodology enforces it on the *actor*: 10 of its 12 quality gates are self-certifications and 26 of
  28 failure modes bind by text alone (only #27 → `.githooks/pre-commit` and #28 → `context_budget.py`
  have a distributed mechanical gate). Self-certification multiplies under N agents rather than scaling;
  a stronger reviewer changes the judge, not the class of gate. Corpus grep for any code-quality
  threshold: 0 hits; the one ratchet that exists (`starter-kit/context_budget.py:504`) guards document size.
- **What it proposes** (D1–D10, six one-session phases): ship the ratchet, not the ruler —
  `.quality-gates.json` SEED + `quality_ratchet.py` TRACKED (refuses a commit that loosens a declared
  threshold), a `SAFEGUARDS.md` hard rule, a flight-manual section generalizing the capability-tiered
  clause from elective to universal, Phase 3C routing "a mechanical learning is a gate, not a row",
  advisory dashboard scoring of gate outcomes, receipt citation of the gate run. Not adopted: two-day
  default approval, PR-throughput floors, coverage floors without a faithfulness check. No new FM.
- **Blocked on:** PR #80 (relocates the Learnings table every prose phase touches). Nothing executes
  until #80 is decided.
- **Verification:** 425 lines; 26 `file:line` anchors on `main @ 512c2ed` re-checked by script (26/26);
  leak check for private-correspondence phrasing, internal-only paths, project names and brand names: 0 hits;
  `bin/check-links` OK (83/21), `bin/check-handoff --allow-pending` OK.

