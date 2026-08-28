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

---

## 2026-08

### 2026-08-27 · [ad hoc] S118 RE-AIM — the deliverable becomes a product-scoped shrink plan plus a size gate, aimed at one upstream PR

- **Model:** Claude Opus 5 (1M context).
- **The operator re-scoped the session mid-flight, and the re-scoping is the substance, not a detail.**
  In their words: *"much of my problem in understanding you is that you are solving two problems and,
  presently, I am only concerned with one … 1) fixing the `methodology` repository's customized files.
  2) fixing the files and code that goes to adopters. The problem that is most important is to fix the
  files and code that goes to adopters via https://github.com/KJ5HST/methodology.git"* — and then:
  *"Our goal is to create a PR for upstream that addresses the file management problem we are working on."*
- **The re-scoping was earned by a defect in how S118 was presenting the decisions.** Every option in §6
  had been costed without sorting Problem 1 from Problem 2, so fork-only work (`.context-budget.json`,
  `docs/planning/`, `docs/archive/`, the root ledgers) was priced beside product work as though both
  reached adopters. **The product is exactly `bin/_manifest.py`'s DISTRIBUTION list: 26 rows / 936,867 B**
  — 21 TRACKED (906,419 B) + 5 SEED (30,448 B). Nothing else reaches an adopter by any route.
- **THE THREE ASSIGNED DELIVERABLES**, all planning-mode (FM #18: nothing implemented this session):
  **(1)** analyse `starter-kit/FRAMEWORK_LEARNINGS.md` and `ITERATIVE_METHODOLOGY.md` for shortening —
  duplication removal, merging near-identical learnings (the operator named **#7/#8** as a candidate pair,
  and row 8 says of itself *"This is Learning #7 applied to procedure summaries rather than citations"*),
  abbreviations for frequent phrases, removal of rarely-used learnings, and truncation of example lists
  that enumerate every instance from the original finding. **(2)** design a gate preventing
  `SESSION_RUNNER.md` + `SAFEGUARDS.md` from becoming undeliverable. **(3)** aim both at one upstream PR.
- **The premise was checked before the work started, and it is conditionally true — the condition matters.**
  At the 2.27 floor (decision D5 below) one read is 56,750 B, so `FRAMEWORK_LEARNINGS.md` (73,483 B) is over
  by **16,733 B** and `ITERATIVE_METHODOLOGY.md` (68,240 B) by **11,490 B**. **Metered directly, both still
  fit** — 24,110 and 23,432 tokens against the 25,000 cap. `FRAMEWORK_LEARNINGS.md`'s true runway is
  **2,714 B ≈ one to two rows**, so the shortening buys headroom that is nearly gone rather than recovering
  headroom already lost. Recorded this way so no successor inherits the stronger claim.
- **The load-bearing number for the whole effort:** the framework's *own* shipped Phase 0 read —
  `starter-kit/SESSION_RUNNER.md` (54,363 B) + `starter-kit/SAFEGUARDS.md` (15,386 B) = **69,749 B =
  24,597 metered tokens = 98.4% of one 25,000-token read**, before the adopter's `CLAUDE.md` — which the
  framework does **not** own (`CLAUDE_TEMPLATE.md` is the manifest dest, never `CLAUDE.md`) — contributes a
  byte. Across 11 real adopters that file runs 2,725–43,956 B.
- **Superseded, not abandoned:** the claim entry above stands. D1/D2/D3/D4 and D6 remain unanswered and are
  now re-posed against the product rather than against this fork.
- **No outward-facing action taken.** No fetch, no push, no PR, no issue, no comment. `main` is 97 ahead of
  `origin/main` and **438 ahead of `upstream/main`** (1 behind, `512c2ed`), measured against refs last fetched
  2026-08-15 / 2026-08-11 and therefore **stale**; the operator asked about resyncing as a *question* and it
  was answered, not executed (FM #23).

### 2026-08-27 · [ad hoc] S118 DECISIONS (3 of 7) — the density floor, the fork-local ceiling, and the fleet instrument

- **Model:** Claude Opus 5 (1M context).
- Three **operator decisions** from §6, recorded per FM #27 before any carrier is edited. Four remain open
  (D1, D2, D3, D4, D6 — re-posed against the product after the re-aim above).
- **(1) D5 — CEILINGS ARE DENOMINATED IN THE CONSERVATIVE `MIN_BYTES_PER_TOKEN = 2.27` FLOOR**, giving
  `READ_CAP_BYTES = 56,750`. Chosen over per-file measured density, a per-class denominator, and two
  labelled denominators. **This ratifies what already ships** — the floor is already the constant in
  `starter-kit/methodology_trim.py:120` and both dashboard twins, all TRACKED. Two consequences were put to
  the operator before the choice was recorded: it leaves `SESSION_RUNNER.md` **2,387 B** of headroom against
  a floor-denominated ceiling, when that file's four largest single commits are **+8,084 / +5,325 / +5,101 /
  +4,436 B**; and it disagrees with the 73,728 B ceiling S114 derived for `FRAMEWORK_LEARNINGS.md` at that
  file's *measured* 3.03 density. **Both collisions are Problem 1** — they live in the fork-only
  `.context-budget.json` — so neither blocks the product work. **The in-scope residue is a product defect:**
  the SEED `starter-kit/context-budget.json` declares `bytes_per_token: 2.93`, a *fourth* denominator that
  contradicts the floor and ships to every future adopter.
- **(2) D7(a) — YES, the canonical repo may hold itself to a ceiling on `SESSION_RUNNER.md` and
  `SAFEGUARDS.md`.** **Problem 1**, and the plan's stated ground for fencing it was measured and **refuted**:
  §6's *"Adding them … ships upstream"* and dragon 3 are false for the edit the decision actually requires.
  `.context-budget.json` is **never a manifest SOURCE** (only ever a DEST, from the SEED
  `starter-kit/context-budget.json`) and **does not exist in `upstream/main`** — `git cat-file -e
  upstream/main:.context-budget.json` exits 128 while `origin/main` exits 0. The *other* half of the ground
  stands: a ceiling constrains what future canonical sessions may write into a TRACKED file.
- **(3) D7(b) — NO, the fleet-wide instrument must not flag those two files.** **This ratifies shipped
  behaviour**: `starter-kit/methodology_dashboard.py:420-425` already excludes them from `READ_CAP_WATCHED`,
  and `:350-356` states the reason — *"one canonical breach would light up every adopter at once over a file
  they cannot edit."* **No product change; the value is that the exclusion is now a decision on record with
  a reason, so no future session re-opens it as an oversight.** The two declines rest on *different* grounds
  and only the first was affected by the refutation above.
- **The distinction the decision turns on, from the manifest's own header:** `SAFEGUARDS.md` is protected at
  an adopter (TRACKED — `bin/sync`'s `classify_target()` marks a locally edited copy `modified` and declines
  to overwrite) and **editable here**, where it is the original — 8 commits, 7,850 → 15,386 B. So a ceiling
  here is actionable and a fleet flag is not, which is exactly what `.context-budget.json`'s `_synced` key
  already argues.

### 2026-08-27 · [ad hoc] S118 claim — answer the six operator decisions gating Phase 1 of the file-management plan

- **Model:** Claude Opus 5 (1M context).
- Phase 1B claim. **Deliverable: the six operator decisions in
  [`docs/planning/file-management-system-plan.md`](docs/planning/file-management-system-plan.md) §6,
  asked and RECORDED** — each as its own entry in this ledger, the way S116 recorded its three.
  Assigned by the operator at this claim from a Phase 0 report that put it beside BL-51 Phase C3,
  issue #75's unsent PR, and the 1-commit `upstream/main` resync. **None of those is authorized.**
- **Why this is a session and not a preamble.** §6 states the gate in its own words — *"Phase 1 does
  not start until these are answered"* — and states why the gate cannot be dissolved by working
  harder: *"None is derivable from measurement — that is why they are here and not in §4."* The plan
  is **DRAFT** until they are answered; six of its seven phases depend on the vocabulary D1–D6 fix.
- **THE ANSWERS ARE THE OPERATOR'S. A RECOMMENDATION IS NOT AN ANSWER.** This session's work is to
  re-verify each decision's load-bearing evidence **against today's tree**, put concrete costed
  options with their consequences, and record what is chosen — attributed, so a successor cannot
  read a recommendation as a ratification.
- **The six, in §6's order:** **D1** target cost per session · **D2** how many of each thing the
  framework carries · **D3** the semantic event on which an artifact retires · **D4** whether
  *undeliverable in one `Read`* is a fault or an accepted operating state · **D5** whether ceilings
  are denominated in the conservative floor or measured density · **D6** whether the framework has
  jurisdiction over adopter-owned files, and by what delivery mechanism. **A seventh rides with
  Phase 1** — whether `SESSION_RUNNER.md` and `SAFEGUARDS.md` get ceilings at all; it is recorded
  with the six because `.context-budget.json`'s `_deliberate_exclusions` declined it once already.
- **RE-MEASUREMENT IS PART OF THE WORK, NOT A COURTESY.** Every figure in §6 was measured during
  S117 and some were stale before that session closed: `FRAMEWORK_LEARNINGS.md`'s 73,483 B is the
  size *after* S117's own Learning #45, and both root ledgers grew again at its close-out. Figures
  quoted to the operator are re-derived here and the command is shown beside each.
- **Not in scope, explicitly:** Phase 1 itself (teaching `context_budget.py` to total any declared
  class), any edit to `.context-budget.json`, BL-45's remedy, BL-51 Phase C3,
  BL-42/43/44/46/47/48/49/50/52, issue #75's unsent PR, trimming `CHANGELOG.md` or `HANDOFFS.md`,
  the `upstream/main` resync, **and any outward-facing action whatsoever.**
- **State at claim, measured:** `main` clean but for the two telemetry `.jsonl`; **96 ahead of
  `origin/main`, 437 ahead / 1 behind `upstream/main`**. `check-handoff` **0**, `check-learnings`
  **0** (44 rows), `check-links` **0**, each run bare. `context_budget.py` exits **2** — the
  adjudicated BL-52 ledger breach, unchanged, **not** a regression; `methodology_trim.py --check`
  fires on **neither** ledger (run per file — bare it exits **3** on a *usage* error, which is not a
  signal about either ledger). Dashboard **76/100**, medium risk, 694 commits.

### 2026-08-27 · [ad hoc] S117 close-out — full-scope file-management plan shipped, self-score 8/10

- **Model:** Claude Opus 5 (1M context).
- Close-out receipt written to [`HANDOFFS.md`](HANDOFFS.md); **predecessor S116 scored 8/10**.
- **Build-equivalent RUN:** `bin/tests.sh` **287 rows — 286 passed / 1 failed / 0 skipped, exit 1**,
  identical row-for-row to S116's control; sole failure by name `github source dry-run failed`
  (Test 9's standing 404). **Zero skips**, so Test 34 stayed in its anchored arm. Tests 34/37 mutate
  the live `HANDOFFS.md` and `FRAMEWORK_LEARNINGS.md` and **the tree restored cleanly.**
  `check-links` 0, `check-learnings` 0, `check-handoff` 0, all run bare. `context_budget.py` exits
  **2** — the adjudicated BL-52 ledger breach, unchanged, not a regression.
- **Phase 3C discharged: Learning #45 appended** (836 B) — *a budget made of per-file ceilings
  cannot see the cost that is actually paid, the aggregate.* `starter-kit/FRAMEWORK_LEARNINGS.md`
  72,646 → **73,483 B against 73,728: `ok`, 245 B headroom.** **This corrects a claim this session
  itself repeated from S116:** the file did **not** block a learning row. A *median* row (1,464 B)
  does not fit; a terse one does. Measure the row you intend to write.
- **`starter-kit/FRAMEWORK_LEARNINGS.md` is a TRACKED manifest source, so Learning #45 reaches every
  adopter at their next `bin/sync`.** Re-derived on the manifest's source column at close-out. The
  plan itself (`docs/planning/`) and the two root ledgers are **not** distributed.
- **FIVE DEFECTS FOUND AND DELIBERATELY NOT FIXED**, recorded here so they are not lost and each
  needing a backlog item a future session raises: (1) a **new current-generation v1.3.0 losslessness
  proof failure** — `docs/archive/HANDOFFS-through-2026-08-25.md.verify.sh` exits 1 with
  `L2 FRONT MATTER lost 1 line(s)`, caused by the hand-maintained *"Archived shards — N trims, M
  receipts"* sentence that is not in `spec.regenerated` and that the next trim edited — making
  **5 of 16** shipped proofs red, not BL-36's four; (2) **`bin/check-learnings` is silently disarmed
  by a single blank line** inside the table — it prints `OK — 21 Learning row(s), contiguous 1..21;
  all citations resolve` at **exit 0** with 43 rows present, and on today's file only an *incidental*
  citation catches it; (3) its **"out of ascending order" guard is dead code**, nested inside the
  contiguity-failure branch — reversing all 43 rows returns exit 0; (4) **four `[[N]]`
  cross-references** in rows #32/#33/#36/#38 are invisible to `CITATION_RE`; (5) the seed
  `starter-kit/context-budget.json` declares **`LEARNINGS.md`**, a filename no manifest dest installs.
- **Two self-corrections on the record, both of which reached the operator before they were
  measured:** `ITERATIVE_METHODOLOGY.md` was asserted past its one-read limit from an *estimated*
  density and in fact reads whole with **1,568 tokens spare**; and this session's own claim commit
  `fd44454` said *"every figure in [BL-45] is stale"* when **both its byte columns reproduce
  byte-exactly** — only its baseline, row count, median and citation figure are wrong.
- **No outward-facing action taken, and none authorized.** `main` is **95 ahead of `origin/main`**;
  nothing pushed. Issue #75's PR remains local-only and unsent.

### 2026-08-27 · [ad hoc] S117 — a full-scope file-management plan for the framework (DRAFT)

- **Model:** Claude Opus 5 (1M context).
- **Deliverable:** [`docs/planning/file-management-system-plan.md`](docs/planning/file-management-system-plan.md)
  (31,643 B, against a **declared 65,000 B budget** stated in its own header — the plan is file 32
  in an ungoverned directory and says so). **Planning session: nothing is implemented.**
- **Evidence base:** a 6-census / 12-verifier / 1-critic read-only workflow, plus direct measurement
  with the no-content token meter. Every figure was reproduced by a command; §10 carries the
  reproductions. Tree asserted clean throughout — no agent wrote to this repo or to any adopter.
- **THE CENTRAL FINDING, metered rather than estimated:** the mandatory Phase 0 read set —
  `CLAUDE.md` + `starter-kit/SESSION_RUNNER.md` + `starter-kit/SAFEGUARDS.md` — is **80,813 B =
  28,832 tokens = 115.3% of the 25,000-token single-read limit.** It cannot be delivered in one
  read and would have to shed 10,741 B to fit. **No per-file ceiling can catch it: the failure is a
  sum nothing sums.** `starter-kit/context_budget.py:888-898` totals exactly one class and hardcodes
  which (`cfg["classes"]["resident"]`), and that class has one member.
- **Six more structural findings, each reproduced:** (F2) the ceilings sit on the files that can
  afford to grow — `CHANGELOG.md`/`HANDOFFS.md` are frontier-read and newest-first, so truncation
  costs them their *oldest* records, while the unwatched oldest-first files lose their *newest*;
  (F3) **the only automated decay mechanism is net-additive by 1.79×** — trim `9038e40` relieved
  22,146 B and added 39,672 B for a **net +17,526 B**, the proof script being 70% of the shard it
  certifies, and `docs/archive/` is now 35.0% of the tracked repo with no ceiling and no deletion
  ever; (F4) **in 693 commits exactly one tracked file has ever been deleted** (`LICENSE`, `d207d1c`,
  re-added as a mistake) — the framework has a create verb and no retire verb; (F5) nothing
  mechanically enforces any ceiling, and the one hook that *is* installed forces growth; (F6)
  `docs/planning/` and the archive tier are ungoverned, and `git log --oneline` is **56,856 B**, a
  read artifact with zero possible decay; (F7) three live ceilings, two densities differing by 25%,
  and **20 copies of the literal `65536` across 8 files** with nothing keeping them consistent.
- **Fleet evidence, measured read-only across 11 real adopters:** **8 of 11 exceed the single-read
  limit** on mandatory Phase 0 reading — robust at both the measured mix density and the most
  token-sparse density in the repo — while only **3 of 11** hold any size instrument, and 10 files
  across 5 adopters are already past the 262,144 B hard refusal.
- **SIX OPERATOR DECISIONS (§6) GATE PHASE 1 and are not derivable from measurement:** the target
  cost per session; how many of each thing the framework should carry; the semantic retirement
  event; whether "undeliverable in one read" is a fault or an accepted state; conservative floor vs
  measured density; and whether the framework has jurisdiction over adopter-owned files.
- **BL-45 is absorbed, not closed.** Its remedy becomes Phase 4's first instance. Its byte columns
  were re-derived and **still reproduce exactly**; its citation figure does not — *"five, in two
  files"* at N=10 is **9, in 4 files**, measured by running the checker. **This session's own claim
  commit (`fd44454`) was wrong to say every figure in it is stale, and that is corrected here.**
- **Defects found and deliberately NOT fixed** (handed forward, out of a planning session's scope):
  a **new current-generation `.verify.sh` failure** (`HANDOFFS-through-2026-08-25`, `L2 FRONT MATTER
  lost 1 line(s)`) making **5 of 16** shipped proofs red; `bin/check-learnings` **silently disarmed
  by a single blank line** (prints `OK — 21 rows` at exit 0 with 43 present); its dead
  ascending-order guard; four `[[N]]` citations invisible to its sweep; and the seed budget
  declaring `LEARNINGS.md`, a filename no manifest dest installs.
- **Not in scope / not taken:** implementing any phase, BL-51 Phase C3, `RECORD_BUDGET_BYTES`,
  trimming either ledger, and **any outward-facing action whatsoever.** Phase 6 (upstream PR)
  explicitly requires the operator's go-ahead and is **not** implied by approving this plan.

### 2026-08-27 · [ad hoc] S117 RE-AIM — the deliverable becomes a full-scope file-management plan

- **Model:** Claude Opus 5 (1M context).
- **Operator decision, taken mid-session, and it supersedes this session's own claim entry below
  rather than abandoning it.** The session was claimed for BL-45's `FRAMEWORK_LEARNINGS.md` remedy;
  the BL-45 research ran to completion and its findings stand (recorded in the two entries below).
  Presented with the re-costed options, the operator asked instead for
  *"a full scope plan … because we have been solving localized problems and not solving for making
  methodology as efficient and effective as possible from the standpoint of file management."*
- **THE RECORD SUPPORTS THAT CHARACTERISATION, which is why the re-aim is recorded as a decision
  and not as scope drift.** Every prior effort in this space is a point fix on one artifact:
  BL-19, BL-22, BL-37, BL-42, BL-43, BL-44, BL-45, BL-46, BL-47, BL-48, BL-49, BL-50, BL-51, BL-52,
  [`read-cap-phase-c-plan.md`](docs/planning/read-cap-phase-c-plan.md) Phases A–C,
  [`record-budget-reduction-plan.md`](docs/planning/record-budget-reduction-plan.md),
  [`ledger-trimmer-design.md`](docs/planning/ledger-trimmer-design.md) and
  [`framework-context-cost-plan.md`](docs/planning/framework-context-cost-plan.md).
  **No document in this repository has ever asked what the whole file-management system should be**,
  which is why the two largest per-session reads have no ceiling and nobody noticed (see below).
- **THE DELIVERABLE IS A PLAN AND NOTHING IS IMPLEMENTED THIS SESSION** — Planning-session rules,
  `SESSION_RUNNER.md` §Planning Sessions and failure modes #18/#19. The plan is written to
  `docs/planning/`, with the mandatory grep-based evidence inventory, per-phase DONE criteria,
  verification commands, and the **surface** each criterion is demonstrated on. Implementation is
  a separate session per phase.
- **BL-45's own remedy is deliberately NOT taken here.** Its four options are re-costed inside the
  plan and put to the operator there. Closing it by a point fix is precisely the pattern the re-aim
  rejects.
- **THE FINDING THAT MOTIVATED THE RE-AIM, measured this session:** `.context-budget.json` declares
  ceilings for five paths, and **neither of the two files every session must read in full is among
  them** — `starter-kit/SESSION_RUNNER.md` (54,363 B, ~18,100 tok, the largest recurring context
  cost in the repository) and `starter-kit/SAFEGUARDS.md` (15,386 B, which Phase 0 step 1 requires
  *"in full, not skimmed"*). Meanwhile the two files that **are** red — `CHANGELOG.md` and
  `HANDOFFS.md` — are read only at a frontier, are newest-first, and so lose their **oldest**
  records to truncation, which is the harmless end. **The guards are on the files that can afford
  to grow, and absent from the files that cannot.**
- **Not in scope:** implementing any phase of the plan, BL-51 Phase C3, `RECORD_BUDGET_BYTES`,
  issue #75's unsent PR, and **any outward-facing action whatsoever.**

### 2026-08-27 · [BL-45] S117 claim — BL-45 re-opened: the `FRAMEWORK_LEARNINGS.md` size remedy

- **Model:** Claude Opus 5 (1M context).
- Phase 1B claim. Deliverable: **BL-45's remedy**, re-opened on BL-45's own closing instruction —
  *"Re-open when the ~3 remaining rows are spent."* They are spent. `starter-kit/FRAMEWORK_LEARNINGS.md`
  is **72,646 B against a 73,728 B ceiling — 1,082 B free**, and `ROW_BUDGET_BYTES` is **1,500**, so
  **no conforming Phase 3C learning row fits.** S116's close-out named this the binding constraint on
  its successor rather than a note, and it binds this session too.
- Authorized by the operator at this claim, from a Phase 0 report that put it beside BL-51 Phase C3
  and issue #75's unsent PR. **Phase C3 stays unstarted. No outward-facing action is approved,
  implied, or taken.**
- **THE OPTION CHOICE IS THE OPERATOR'S.** BL-45's own table says so outright (*"the choice is the
  operator's"*). Its four options — (a) archive oldest rows, (b) raise the ceiling **[taken at S114,
  now spent]**, (c) compact the over-budget frozen rows, (d) split by theme **[BL-45 advises
  against]** — are put to them **re-derived against today's tree**, not quoted: the costed table was
  measured at **65,520 B / 37 rows** and the file is now **72,646 B / 43 rows**, so every figure in
  it is stale. Whichever way it falls is recorded here as its own ledger entry before any row moves.
- **TWO FACTS FOUND AT ORIENT ALREADY FALSIFY THAT TABLE, and both are recorded now rather than at
  close-out, because a successor who reads BL-45 without them will act on a wrong premise:**
  1. **The carrier is a DISTRIBUTED manifest source.** `bin/_manifest.py:38` is
     `("starter-kit/FRAMEWORK_LEARNINGS.md", "FRAMEWORK_LEARNINGS.md", TRACKED)` — read on the
     **source** column, not by grepping the bare filename — so any change reaches **every adopter at
     their next `bin/sync`**. BL-45's closure note says *"The change is canonical-only … so no
     adopter is affected"*; that is true of the **ceiling in `.context-budget.json`**, which is what
     S114 actually moved, and **not** of the file. Left standing in BL-45 per FM #17; corrected here.
  2. **Option (a) needs checker work at EVERY N, not only at large N.** BL-45's correction (i)
     retired the *citation* objection on measurement — archiving the oldest 5 orphans **zero**
     distributed citations. It never reached `bin/check-learnings:197`,
     `expected = list(range(1, len(numbers) + len(reserved) + 1))`: the numbered set is asserted
     contiguous **from 1**. Archiving the oldest row fails the checker at **N = 1** with
     *"not contiguous from 1 — missing #1"*. The table's *"needs no checker work at small N"* is a
     claim about citations that reads as a claim about the checker.
- **Not in scope:** BL-51 Phase C3 (A3/B1/B2), `RECORD_BUDGET_BYTES` and the record-budget campaign,
  BL-42/43/44/46/47/48/49/50/52, issue #75's unsent PR, and **any outward-facing action whatsoever.**
- **State at claim, recorded because a successor will misread it:** `CHANGELOG.md` (92,346 B) and
  `HANDOFFS.md` (123,667 B) are over their fork-local ceilings **by adjudication, not neglect**
  (BL-52) — `context_budget.py` exits **2**, while `methodology_trim.py --check` fires on
  **neither**, which is the intended post-Phase-C2 state. **This session does not trim them.**

### 2026-08-26 · [BL-51] S116 — Phase C2: the Class A archive threshold, bundled with `DEFAULT_BUDGET_BYTES`

- **Model:** Claude Opus 5 (1M context).
- **Phase C2 of [`read-cap-phase-c-plan.md`](docs/planning/read-cap-phase-c-plan.md) §9, complete**
  — option **A2** and option **C1** in one commit (`0afe9d6`), as §8 requires and §10 dragon 1
  explains. New `CLASS_A_FIRE_BYTES = 192*1024` / `CLASS_A_STOP_BYTES = 96*1024`;
  `DEFAULT_BUDGET_BYTES` **65,536 → 196,608**; `Trigger.read_fire_at` / `read_stop_at` per class;
  new `is_root_class_a()`. `methodology_trim.py` **1.4.0 → 1.5.0**, `methodology_dashboard.py`
  **2.16.1 → 2.17.0** with its twin.
- **THE FINDING THAT CHANGED THE PHASE'S SHAPE: §7's *"replace the read arm's threshold"* is TWO
  SITES.** `Trigger.stops()` compares each candidate cut to its own constant, and before C2 the
  fire and the stop were both `READ_CAP_BYTES`. **Moving only the fire leaves `choose_cut` cutting
  to 56,750 B — three times deeper than intended — with the whole suite green**, because every
  assertion was about what *fires* and none about what a remedy *converges to*. Found by reading
  `stops()` before writing anything, and pinned by an end-to-end test on the resting size: a real
  `--write` on a 213,704 B fixture lands at **93,909 B**, inside
  `(READ_CAP_BYTES, CLASS_A_STOP_BYTES]`. Recorded as **Learning #44**.
- **§9's DONE criterion, each half demonstrated:** `--check` **fires on neither ledger** at today's
  sizes (exit 0, was 1); **fires** on a synthetic 256,037 B root ledger; `choose_cut` returns a
  **real cut at both densities** (`CHANGELOG.md` 26 of 27 → 85,052 B; `HANDOFFS.md` 8 of 10 →
  91,906 B), not the `return 1` fall-through; **no ledger can stop above `READ_REFUSE_BYTES` at any
  budget**, asserted to 4 MiB — the read arm caps the byte arm, which is the `--budget-bytes` guard
  restated at the new value.
- **The widened half — the dashboard — was TWO unowned sites, not the one §6 names**, and that
  section's `:3045-3072` citation is pre-C1 (true range `:3135-3169`). The second is
  `collect_trim_metrics:2197`, which **re-implements** the trimmer's read arm; left behind it would
  have emitted *"the archive trigger fires; … run `--check`"* beside a `--check` reporting that it
  does not. **A1's deferred *buys* are now delivered:** the two rows are *different* rather than
  deduplicated (§7's own wording), and the effect is fleet-visible — a Class A ledger over the
  one-read cap drops **`high` → `low`**, worst risk `high` → `medium`.
- **`READ_CAP_BYTES` did not move and must not** — it is a measured harness fact, not a policy
  knob. It still reports, and it is still Class B's threshold.
- **VERIFIED, NOT ARGUED.** `bin/tests.sh` row-for-row against a worktree control at `b80f1a8`,
  run **twice** (after the deliverable, and again after the prose repairs rather than assumed),
  both populations asserted non-empty: **287/287, zero lost, zero gained, zero status flips, zero
  skipped**; sole failure both sides by name, Test 9's standing `--source=github` 404. Python
  suites **111/313/42 → 123/321/42**. **Mutation: 12 mutants, 12 killed, 0 survived, 0 failed to
  apply** — and the half-application mutant was re-run alone to list **all four** objecting tests,
  three of them this session's, because the harness reports only the first.
- **A guard written to gate this phase stayed green through it.** S115's
  `test_phase_c1_moved_no_threshold` promised a namespace check *"which no per-class threshold can
  slip past whatever it is called"*; it greps one prefix, and `CLASS_A_FIRE_BYTES` is not that
  prefix. Its successor sweeps by **substring** and asserts the exact expected set.
- **Not done, each deliberately:** all of **Phase C3** (A3, B1, B2), `RECORD_BUDGET_BYTES`,
  BL-42/43/44/46/47/48/49, issue #75's unsent PR, and **any outward-facing action whatsoever.**

### 2026-08-26 · [BL-51] Phase C2 DECISIONS — `DEFAULT_BUDGET_BYTES` raised, C2 widened to the dashboard, the Class A threshold scoped to root

- **Model:** Claude Opus 5 (1M context).
- Three non-commit **operator decisions**, recorded per FM #27 before any carrier is edited. The
  plan states of the first *"This plan does not decide it"*; S115 fenced the second as needing the
  operator; the third neither the plan nor S115 anticipated and it was found by measurement this
  session.
- **(1) OPTION C1 — `DEFAULT_BUDGET_BYTES`: RAISE to `192 * 1024` (196,608).** Chosen over retiring
  it and over keeping it.
  - Keeping it is not viable *if C2 is to close*: both ledgers `byte_fire` at today's sizes
    (81,070 B and 111,388 B against 65,536), so §9's C2 criterion — *"`--check` fires on neither
    ledger at today's sizes"* — is **unsatisfiable** with the constant where it is.
  - Retiring it is a `NameError` at import from the `LedgerSpec` default parameter
    (`starter-kit/methodology_trim.py:218`) unless the whole per-file budget machinery goes with
    it, which would delete the `--budget-bytes` knob §8 gives a reason to keep. It also removes the
    **only** byte guard adopters have on these two files: the seed
    `starter-kit/context-budget.json` governs `CLAUDE.md`, `SESSION_NOTES.md` and `LEARNINGS.md`
    and **not** the two ledgers (BL-47, re-verified this session by parsing the seed).
  - Raising costs nothing extra in machinery: `BYTE_STOP_FRACTION` is already 0.5, so
    `int(196,608 × 0.5)` is **98,304 = 96 KiB exactly**, which is option A2's stated stop.
- **(2) THE C2 HOLE — WIDEN C2 rather than raise a fourth phase.** C2's DONE criterion now also
  covers the dashboard. **The hole is TWO sites, not the one §6 names**, and the plan's
  `:3045-3072` citation is pre-C1 — the true D4(b) range on this tree is
  `starter-kit/methodology_dashboard.py:3135-3169`. The second site is the sharp one:
  `collect_trim_metrics:2197` **re-implements** `read_fires = size_bytes > READ_CAP_BYTES` and
  emits *"the archive trigger fires; … run `--check` for the full report"*. Moving the trimmer's
  trigger without it would have the dashboard name a command whose output contradicts the row —
  the exact misdirection the comment at `:2240` says that wording exists to avoid.
- **(3) THE CLASS A THRESHOLD IS SCOPED TO THE REPO ROOT.** Found by measurement, not anticipated:
  the trimmer resolves its config by **basename at any depth** (`methodology_trim.py:1674`,
  `LEDGERS.get(path.name)`), while the dashboard's class is a **repo-relative path** lookup
  (`methodology_dashboard.py:407`). Unscoped, the relaxed threshold would apply to any
  `*/CHANGELOG.md` or `*/HANDOFFS.md` — **3.38× today's 56,750 B** — for a file that was never
  classified. Harmless today (the only non-root instances in 13 portfolio repos are this repo's own
  two ~12 KB seeds) and a trap tomorrow. The relaxed pair applies only where the file sits at the
  repo root; a nested one keeps the tighter one-read threshold.
- **Two costs of (1) are accepted with eyes open, and neither goes red on its own.** Moving the
  constant silently falsifies three `.context-budget.json` `_` keys that name it as their ceiling's
  source (*"max_bytes 65,536 is NOT chosen here — it is starter-kit/methodology_trim.py:69
  `DEFAULT_BUDGET_BYTES`"*) and the comment at `bin/check-handoff:596` (*"still the trigger
  `methodology_trim.py` keys on"*). That is Learning #28's shape — repairing a defect falsifies the
  records that described it — so the repair is part of this session's scope, not left to be found.
- **One argument in the plan's §5 does not survive re-derivation, and it argued against the option
  chosen.** *"the number BL-9/BL-32/BL-36/S87/S89 have all measured against"* is **impossible for
  BL-9**: BL-9 closed **2026-08-01** and `DEFAULT_BUDGET_BYTES` was first written **2026-08-03**
  (`df381ea`, S36). The relation is the reverse — design §5.4 calibrates the constant on three
  sizes, and 52,927 B is BL-9's own L1 output commit `7a71df0`, so **BL-9 is the constant's input,
  not a measurement against it.** Only BL-9 was re-derived; the other four names are **not**
  re-checked and are not claimed either way. The sentence originates in `.context-budget.json`'s
  `_` key and the plan inherited it.

### 2026-08-26 · [BL-51] S116 claim — Phase C2: the Class A trigger, bundled with `DEFAULT_BUDGET_BYTES`

- **Model:** Claude Opus 5 (1M context).
- Phase 1B claim. Deliverable: **Phase C2** of [`read-cap-phase-c-plan.md`](docs/planning/read-cap-phase-c-plan.md)
  §9 — option **A2** (the Class A fire/stop pair) shipped in **one commit** with option **C1**
  (`DEFAULT_BUDGET_BYTES`), which §8 requires be bundled and §10 dragon 1 explains: `Trigger.fires`
  is `read_fires or byte_fires`, and the 65,536 B byte arm fires first, so **A2 alone ships a
  trigger that can never fire.**
- Authorized by the operator at this claim. The plan itself was **RATIFIED 2026-08-26** at S115's
  claim; that ratification approved §8's sequence but authorized **only Phase C1**, so C2 needed
  its own go-ahead and now has it. **Phase C3 stays unstarted.**
- **TWO DECISIONS BELONG TO THE OPERATOR AND ARE NOT DERIVABLE FROM THE PLAN.** Both are put to
  them with measured evidence **before any carrier is edited**, and whichever way each falls is
  recorded here as its own ledger entry:
  1. **Option C1's disposition** — retire `DEFAULT_BUDGET_BYTES`, raise it, or keep it and accept
     A2 is inert. §5 states the evidence on both sides and §7's C1 row says plainly
     *"Judgment, not derivation"*; the plan closes the point with *"This plan does not decide it."*
     Retiring it orphans the baseline BL-9/BL-32/BL-36/S87/S89 all measured against.
  2. **The C2 hole**, fenced at the plan's top by S115 and not resolved there. §6's inventory puts
     option A1's **per-class dashboard thresholds** at `starter-kit/methodology_dashboard.py:3045-3072`,
     but §9's Phase C2 DONE criterion names only `--check`, `choose_cut` and `READ_REFUSE_BYTES` —
     all **trimmer**-side. Those risk rows fall between C2's and C3's criteria and are owned by
     **neither phase**. The operator either widens C2's criterion or raises a fourth phase.
- **Carriers are DISTRIBUTED** — `starter-kit/methodology_trim.py` and
  `starter-kit/methodology_dashboard.py` are both TRACKED manifest SOURCEs (the dashboard with a
  byte-identical `tools/` twin), so this reaches every adopter at their next `bin/sync`. To be
  re-derived off the manifest's **SOURCE** column at close-out, never by grepping a bare filename.
- **State at claim, recorded because §10 dragon 8 says a successor will misread it:** `CHANGELOG.md`
  (81,070 B) and `HANDOFFS.md` (111,388 B) are over both ceilings **by adjudication, not neglect**;
  `context_budget.py` exits **2** and `methodology_trim.py --check` **FIRES** on both. That is the
  expected state. **This session does not trim them.**
- **Not in scope:** the prefix invariant (A3), the Class B remedy and `BOOTSTRAP.md` (B1/B2),
  `RECORD_BUDGET_BYTES` and the record-budget campaign, `HEADER_RESERVE_BYTES`, Test 34's retention
  floor, BL-42/43/44/46/47/48/49, issue #75's unsent PR, and **any outward-facing action whatsoever.**

### 2026-08-26 · [BL-51] S115 — Phase C1: the read-cap population split into two classes, pinned to the trimmer

- **Model:** Claude Opus 5 (1M context).
- **Phase C1 of [`read-cap-phase-c-plan.md`](docs/planning/read-cap-phase-c-plan.md) §9, complete.**
  `READ_CAP_WATCHED`'s six names become **Class A** (`CHANGELOG.md`, `HANDOFFS.md` — the trimmer has
  a `LEDGERS` entry) and **Class B** (`SESSION_NOTES.md` + three `BACKLOG.md` locations — the trimmer
  answers `NO_CONFIG`). Both classes are **declared literals**; `READ_CAP_WATCHED` is **derived** from
  their union, so *"the population did not change"* is provable rather than asserted. New public
  `read_cap_class(rel_posix)` → `"A"` / `"B"` / `None`.
- **It changes no behaviour, and that is measured, not argued.** The pre-change module (`git show
  HEAD:tools/methodology_dashboard.py`) and the post-change module were both run against the same
  live tree: watched rows, trim ledger rows, trim signals, **all** risk rows and the health total are
  **identical**, with a control confirming the two modules really differ. Phase C1 is deliberately
  fleet-invisible; §7's A1 row promises otherwise and §§8–9 do not — see the plan's new note.
- **Dragon 6 is satisfied by DECLARING the class, not deriving it.** Deriving class from `LEDGERS`
  would let a widened trimmer silently reassign a file. `test_class_a_is_pinned_to_the_trimmers_ledgers_table`
  fails instead — that is §9's second DONE criterion.
- **The two `docs/**` backlog locations: KEPT, decided on evidence** (§9's third criterion).
  Neither is named as a file to read in `SESSION_RUNNER.md` or `SAFEGUARDS.md`; across the whole
  22-file distributed `.md` corpus `docs/BACKLOG.md` appears **0** times and `docs/planning/BACKLOG.md`
  **once**, in Learning #26 as a worked example. Kept for §7's reason for rejecting option D — the row
  reports a real property — and because keeping costs nothing measurable: `docs/BACKLOG.md` matches no
  file in the fleet, `docs/planning/BACKLOG.md` matches only this repo's, at 0.54× the cap. A canonical
  test pins the "no protocol basis" half so the reasoning cannot quietly go stale.
- **`DASHBOARD_VERSION` 2.16.0 → 2.16.1.** Not cosmetic: `check_stale_version()` (`:928`) compares an
  adopter copy's constant against the canonical's and warns only when the canonical is **newer**, so
  without a bump every synced adopter would run diverged content and be told nothing. (`bin/status`
  is unaffected either way — it keys on a content blob SHA, `bin/status:95-98`. A review finding and
  its refutation both named that tool; the real consequence runs through the other one.)
- **10 new canonical tests, 12-mutant round, 12/12 killed**, each verified to APPLY, both twins mutated
  together, control green before and after, every restore `cmp`-verified.
- **A review found a defect in text this session shipped into a DISTRIBUTED file, and it is fixed.**
  The Class B warrant said flatly *"there is no record ordering that puts the needed part at the top"*
  — false of `SESSION_NOTES.md`, whose `ACTIVE TASK` the runner puts at the top. The plan's own wording
  is *"no record ordering that **guarantees** that"*; the qualifier had been dropped. Restored, with the
  fleet measured **first-hand** (11 repos: offsets 132–23,013, inside the cap in all 10 that have the
  heading; `mts-system` has **no** such heading at all — a fact the review's 6-repo sample missed).
- **Learning #43** appended (1,498 B): *deriving a set from its own parts is usually right, and it
  disarms the assertion that those parts still cover it.* Earned in-session — the first mutation round
  scored 8/10 and both survivors traced to one tautological line.
- **Carve-out, re-derived off `bin/_manifest.py`'s SOURCE column:** `starter-kit/methodology_dashboard.py`
  is **TRACKED/distributed** → reaches every adopter at their next `bin/sync`;
  `starter-kit/FRAMEWORK_LEARNINGS.md` is a **SOURCE** too → Learning #43 ships with it.
  `tools/methodology_dashboard.py` and `tools/test_methodology_dashboard.py` are **canonical-only**.
- **Verification:** `bin/tests.sh` **287 rows, 286 passed / 1 failed / 0 skipped**, row-for-row against
  a worktree control at `757fed2` — **0 status flips**, exactly one row differs and it is a derived
  count this session's own Learning #43 moved (`#43`→`#44`). Sole failure both sides by name:
  `github source dry-run failed` (Test 9's standing `--source=github` 404). Python suites **111 / 313 /
  42 OK** from a foreign CWD. `check-links` OK (88/22) · `check-learnings` OK (42 rows, 1..42, 0 over
  budget). Twins byte-identical, **mirrored last**. `context_budget.py` exit **2** — `CHANGELOG.md` and
  `HANDOFFS.md` only, both adjudicated (BL-52), expected.
- **Commits:** `757fed2` (1B claim + the ratification) + **`596a602`** (the deliverable) + this close-out.
- **NOT DONE, each deliberately:** every threshold (Phase C2 / option C1 `DEFAULT_BUDGET_BYTES`), the
  prefix invariant (A3), the Class B remedy and `BOOTSTRAP.md` (B1/B2), `RECORD_BUDGET_BYTES`,
  BL-42/43/44/46/47/48/49, issue #75's unsent PR, **any outward-facing action**. Nothing pushed.

### 2026-08-26 · [BL-51] S115 claim — Phase C1 of the read-cap correction: split the watched population by class

- **Model:** Claude Opus 5 (1M context).
- Phase 1B claim. Deliverable: **Phase C1** of [`read-cap-phase-c-plan.md`](docs/planning/read-cap-phase-c-plan.md)
  §9 — `READ_CAP_WATCHED` becomes class-aware, with membership **declared** in
  `starter-kit/methodology_dashboard.py` and **pinned by a canonical test** against
  `starter-kit/methodology_trim.py`'s `LEDGERS` table.
- **THIS PHASE CHANGES NO THRESHOLD.** §8 states A1 *"changes no threshold and cannot degenerate
  anything"* and §9's Phase C1 criterion names none; §7's A1 mechanism cell, which reads as if two
  thresholds move, is the summary that drifted. The threshold move is **Phase C2** (option A2),
  which §8 requires be bundled with option C1 (`DEFAULT_BUDGET_BYTES`) or it is inert.
- **The class must be DECLARED, not derived from the trimmer.** §10 dragon 6 requires that widening
  `LEDGERS` **fail** rather than silently reassign a file's class, and §9's DONE criterion asks for
  a test that fails when a name is added to `LEDGERS` without moving class. Deriving the class
  would satisfy neither. The model is the existing `test_grammars_agree_with_the_trimmer_config_table`.
- **Carriers are DISTRIBUTED** — `starter-kit/methodology_dashboard.py` is a TRACKED manifest
  SOURCE, with a byte-identical `tools/` twin — so this reaches every adopter at their next
  `bin/sync`. To be re-derived off the manifest's SOURCE column at close-out.
- **Not in scope:** every threshold, the Class A fire/stop pair, the prefix invariant (A3), the
  Class B remedy and `BOOTSTRAP.md` (B1/B2), `RECORD_BUDGET_BYTES`, BL-42/43/44/46/47/48/49,
  issue #75's unsent PR, and **any outward-facing action**.

### 2026-08-26 · [BL-51] Phase C plan RATIFIED — §8's three-session sequence approved, Phase C1 authorized

- **Model:** Claude Opus 5 (1M context).
- Non-commit **operator decision**, recorded per FM #27. S113 wrote
  [`read-cap-phase-c-plan.md`](docs/planning/read-cap-phase-c-plan.md) as a DRAFT awaiting
  ratification (`9a71c8e`); the operator ratified it at S115's Orient, selecting it over the
  record-budget campaign and over issue #75's unsent PR.
- **What was approved:** §8's recommendation `A1 → (A2 + C1 together) → A3 → (B1 + B2)`, as **three
  sessions**. **Phase C1 alone is authorized as S115's deliverable.** Phases C2 and C3 stay
  unstarted and are **not** authorized by this ratification.
- **What was NOT approved, and is not implied:** any outward-facing action. The plan's own Scope
  line already says so; the ratification does not relax it. The carriers are distributed, so the
  eventual upstream landing batches with BL-46(2)/47/48/49 — and still needs an explicit go-ahead,
  each time.
- The plan's Status line was rewritten in place from DRAFT to RATIFIED, and **two ambiguities a
  successor would otherwise have hit were fenced in the same edit**: `C1` names both an option
  (§7, `DEFAULT_BUDGET_BYTES`) and a phase (§9, the class split, which is option A1), so §9's
  *"Do: A2 and C1 in one commit"* means the **option**; and §7's A1 row reads as if Phase C1 moves
  two thresholds when §8 and §9 both say it moves none.

### 2026-08-26 · [BL-45] S114 — the learnings ceiling re-derived, and five sessions of owed learnings written

**BL-45 CLOSED** by the operator's choice of option (b) from four costed alternatives.
`starter-kit/FRAMEWORK_LEARNINGS.md`'s ceiling **65,536 → 73,728 B (72 KiB)**, and the backlog it had
been blocking is discharged: **rows #39–#42**, 968–1,148 B each, all inside the 1,500 B row budget.
The file is **69,683 B against 73,728 — `ok`**, and `context_budget.py` no longer reports it over.
**Canonical-only:** the distributed seed declares `CLAUDE.md`, `SESSION_NOTES.md`, `LEARNINGS.md` and
**not** this file. *(The rows themselves are a different matter — `FRAMEWORK_LEARNINGS.md` **is** a
manifest source, so #39–#42 reach every adopter at their next `bin/sync`.)*

**The number was re-derived, and the old one's justification was wrong twice.** 65,536 was borrowed
from the ledgers' `DEFAULT_BUDGET_BYTES`; the note defending it converted bytes to tokens at
`bytes_per_token` 2.80 and compared the result to an **opening-context** floor. That estimator
answers a different question, and the limit that bites a read is the **25,000-token Read cap**. Its
arithmetic gave 23,406 tok for a 65,536 B file where the measured figure is **21,623** — 8% over, in
the direction that made the ceiling look tighter than it was.

**Measured three times, including after the write** — x2 = 43,247 tok, x3 = 64,868 against 64,870
predicted (**linear to 0.004%**), giving **3.0300 B/token** and a cliff at **75,751 B**; re-measured
after appending the four rows, **3.0396**, so the margin held. **73,728 is deliberately 2,023 B under
that cliff**: a ceiling must sit below where the file stops fitting, not on it, and this is the value
at which the file stays inside one read even if every future byte is 20% denser. The margin is
judgment and is labelled as such in the config note.

**What it buys, and what it does not.** 8,192 B gained, 4,159 B spent on the owed rows, **~3 rows
left**. The 37 pre-existing rows are 97% of the file and may not be edited, so the untouchable
remainder **is** the file — **Learning #26's own shape, arriving in the file that records it**. The
question underneath is policy, not arithmetic. BL-45's other three options stay open and are now
**costed in the item** so nobody re-derives them.

**A correction to BL-45's own text, left standing per FM #17.** It warns that archiving breaks every
citation to a row. The checker's sweep covers the **distributed corpus only** — **8 citations to 5
rows across 4 files**, not the 471 overall — so archiving the oldest **5** rows would orphan
**none**, and the oldest **10** just **five, in two files**.

**Verification.** `bin/tests.sh` **287 rows, 286 / 1 / 0**, zero status flips, zero skips, sole
failure by name Test 9's standing `--source=github` 404. **Test 37 was watched specifically** — it
copies the live learnings file as its fixture, so four new rows enter its population; 9 assertions,
4 mutants, green. Python suites **111 / 303 / 42 OK**. `check-learnings` OK — **41 rows, contiguous
1..41** (`#14` remains deliberately reserved), 4 unfrozen, 0 over budget. `check-links` OK (88/22),
`check-handoff` + `--all` OK, `BACKLOG-DETAIL` verify OK, twins byte-identical and untouched.
`context_budget.py` exits **2**, and the composition is the point: the learnings file is now `ok`;
the two remaining breaches are `CHANGELOG.md` and `HANDOFFS.md`, **both adjudicated** (BL-52 third
addendum) — do not trim either on sight.

**Model:** Claude Opus 5 (1M context).


### 2026-08-26 · [BL-45] S114 claim — raise the learnings ceiling to the file's real one-read limit

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](HANDOFFS.md). **Operator's decision**, taken from four costed options: raise the
ceiling rather than archive, compact or split. **One deliverable in two halves** — the raise is only
worth making because Phase 3C has been blocked for five sessions, so the owed learnings are written
in the same session or the defect survives the fix.

**Canonical-only, checked rather than assumed:** `.context-budget.json` governs this file; the
distributed seed declares only `CLAUDE.md`, `SESSION_NOTES.md` and `LEARNINGS.md`. **No adopter is
affected.**

**The number will be re-derived, not carried.** 65,536 was borrowed from the ledgers'
`DEFAULT_BUDGET_BYTES`, and the note defending it converts bytes to tokens at `bytes_per_token`
2.80 — an estimator S112 measured as wrong for this purpose. S97's own note invited the re-opening:
*"Re-open that choice when the four rows are spent, not before."* They are spent.

**Model:** Claude Opus 5 (1M context).


### 2026-08-26 · [BL-51] S113 — Phase C planned: what each guard watches, and what it claims; self-score 8/10

Commits `f06b6f7` (claim) and **`9a71c8e`** (the deliverable),
[`docs/planning/read-cap-phase-c-plan.md`](docs/planning/read-cap-phase-c-plan.md), **DRAFT awaiting
ratification**. A planning session: **nothing implemented, no numeral moved** (FM #18/#19). The
predecessor plan's Phase C stub is **annotated in place** to point here.

**The operator's proposal, answered.** *"Only worry about the 256 KB limit for trimming"* is **right
for the two ledgers the trimmer can act on and wrong as a blanket rule.** The six watched names are
**two classes**, evidenced per name off two independent facts — membership of the trimmer's `LEDGERS`
table, and what `SESSION_RUNNER.md` actually instructs. **Class A** (`CHANGELOG.md`, `HANDOFFS.md`):
records, newest-on-top, read by frontier and one record; 9 files, 8 over the cap. **Class B**
(`SESSION_NOTES.md`, three `BACKLOG.md` locations): prose, no delimiter, **read in full**; the
trimmer refuses them by design; **9 files, seven over the cap**. Truncation is only harmless when the
part you need is at the top, and a backlog's bottom items are as live as its top ones.

**The finding the plan did not go looking for and could not avoid: Class B has no reachable remedy.**
`SESSION_NOTES.md` has **none documented anywhere in the distributed corpus**. `BACKLOG.md` has one —
`BOOTSTRAP.md:144-151` — and **Learning #26, earned on this repo's own backlog at S89, proves it
insufficient in general**: archiving everything finished recovered 33% and still left the file at
1.40× its yardstick, because the **open** items alone exceeded it. The remedy that actually worked
here (index + detail split with a runnable losslessness proof) is **fork-only**. **A guard whose
remedy cannot reach is the misdirection [`ledger-trimmer-design.md`](docs/planning/ledger-trimmer-design.md)
§7.3 exists to prevent, and it is shipping.**

**And the proposal is inert without a second decision.** `Trigger.fires` is `read_fires or
byte_fires`, so a 256 KB read trigger changes nothing while `DEFAULT_BUDGET_BYTES` = 65,536 fires
first — **Phase B's §3 coupling recurring one level over.** The plan requires the two ship in the same
session and **deliberately does not decide the second**, laying out the evidence both ways and marking
it a decision rather than a derivation.

**A correction the plan makes to its own first draft, recorded because it is this campaign's lesson
landing on the plan that states it.** Class B's *"× the cap"* column was drafted by carrying a
**Class A** ratio (2.4 B/token, measured on ledger content) onto Class B files. Measured directly,
Class B is **less** dense — 2.5472–2.9096 against Class A's 2.2705–2.5150 — so the draft
**overstated every multiple by 6–20%**, in the direction that flattered the argument. The finding is
unchanged; the numbers were wrong. Corrected before ratification.

**Verification.** No code changed, and the suites were run to prove exactly that: `bin/tests.sh`
**287 rows, 286 / 1 / 0**, sole failure by name Test 9's standing `--source=github` 404 — identical in
shape to S112's control. Python suites **111 / 303 / 42 OK** from a foreign CWD. `check-links` OK
(88/22), `check-learnings` OK (37), `check-handoff` + `--all` OK, `BACKLOG-DETAIL` verify OK (C1–C5),
twins byte-identical and untouched. **20 of 20 load-bearing citations machine-verified** by re-reading
the cited line. `context_budget.py` exits **2**, expected — `HANDOFFS.md` is over its ceiling **by
adjudication, not neglect** (BL-52 third addendum); do not trim it on sight.

**BL-45 now blocks Phase 3C for a fifth consecutive session** — `starter-kit/FRAMEWORK_LEARNINGS.md`
is 16 B from its ceiling and four learnings are earned and unwritten across S112–S113. It is the
longest-standing unaddressed blocker here and needs an operator decision.

**Model:** Claude Opus 5 (1M context).


### 2026-08-26 · [ad hoc] S113 claim — plan Phase C of the read-cap correction

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](HANDOFFS.md). **A planning session: the plan is the deliverable, nothing is
implemented** (FM #18/#19). Origin: the operator's proposal at S112's close-out — *only worry about
the 256 KB limit for trimming*. That is right for the two ledgers the trimmer can act on and wrong as
a blanket rule, because the six watched names are **two classes**, and the four the trimmer refuses
are the ones the protocol genuinely reads in full. Phase C therefore grows from *"two rows or one"*
into **what population and what claim each guard carries** — and must decide `DEFAULT_BUDGET_BYTES`,
which fires first and would render a 256 KB trigger inert.

**Not in scope:** implementing any of it, `RECORD_BUDGET_BYTES`, BL-45, issue #75's unsent PR, the
§11.2 adopter remediation, **and any outward-facing action**.

**Model:** Claude Opus 5 (1M context).


### 2026-08-26 · [BL-52] S112 close-out — the trim was DECLINED on evidence; self-score 7/10, predecessor S111 scored 8/10

Phase 3D receipt in [`HANDOFFS.md`](HANDOFFS.md), **12,288 B inside the 12,288 B per-record budget**
— four trim passes, and `bin/check-handoff` was **run** rather than predicted each time (it counts
the opening fence through the **next** opening fence, trailing prose included).

**A trim was due as close-out housekeeping and was not performed, and that is the entry.**
`methodology_trim.py` refused it (`[SRF_RED]` 1.1198). This session was about to `--force` past the
refusal, **not having asked BL-52's own question** — whether the trim remedies anything. Asked, and
measured by the free over-cap error path: a whole-file read of the untrimmed ledger delivers the
front matter and the **four newest receipts** (55,342 B = **23,370 tok measured**, against 23,409
predicted; the five-receipt prefix is **28,611 tok**, over). The cut on offer would have archived
**S108 and S107 — both already outside the delivered prefix.** Phase 3A reads **one** receipt;
Phase 0 step 6 takes the frontier from `git log` and **greps**; whole-file reads run **1 in 85**.
The context-tax claim does not rescue it either: that cost is per read-span and is already guarded
per record by `RECORD_BUDGET_BYTES`. **The tool's refusal was right for a stronger reason than it
gave** — it diagnosed a level remedy on a rate problem; the measurement adds that the level is not
costing anything yet.

**Deliberately left red, and it is a finding rather than an oversight:** `context_budget.py` exits
**2 (BREACH)** and this repo's own dashboard carries **one high-severity read-cap row**, both on
`HANDOFFS.md`. Both are literally true and, on this measurement, not worth acting on — **a guard can
be correct and not worth acting on**, which enlarges Phase C's question from *two rows or one* to
*what population and what claim each row carries*. The threshold that will actually bite is
`READ_REFUSE_BYTES` = **262,144 B**, roughly **16 sessions** out, where the front matter itself stops
being delivered; the remedy between here and there is
[`record-budget-reduction-plan.md`](docs/planning/record-budget-reduction-plan.md) Phase 2/3.

**Sizes, measured last — and this entry moved one of them, which is worth recording rather than
hiding.** `HANDOFFS.md` **77,238 B / 305 ln**, over its 65,536 B ceiling, declined above.
`CHANGELOG.md` was **58,843 B / 807 ln** before this entry; adding it takes the file to **61,574 B**,
which crosses the new **56,750 B** one-read cap, so **its read arm now fires too.** Measured before
asserting anything about it: at this file's own density it is **24,530 tokens — still inside the
25,000 cap by 470.** So the firing is **early, not wrong**: `MIN_BYTES_PER_TOKEN` is deliberately the
measured *floor* (2.27) rather than this content's 2.51, because a guard that must not stay silent
on a truncating file has to assume the densest content it will meet. The cost of that choice, now
quantified on a real file: it fires about **9.6% early** here (56,750 B against a true cliff near
62,754 B). **That is the designed trade, stated with its price rather than discovered later.**
**And the margin is closing, so do not inherit the word "early":** this file is now within a few
hundred bytes of its own measured cliff, and the next close-out will take it past. Re-run the
doubling probe (concatenate the file with itself, `Read` it with a spanning `limit`, halve the
reported token count) rather than trusting either figure here — the *threshold vs cliff* ratio is a
property of the content type and holds; the file's position against it does not.
`starter-kit/FRAMEWORK_LEARNINGS.md` **65,520 B, 16 B free** — **BL-45 blocked Phase 3C for a fourth
consecutive session**; three learnings are earned and unwritten. `main` is **77 ahead of
`origin/main`**; nothing pushed, no outward-facing action taken.

**Model:** Claude Opus 5 (1M context).


### 2026-08-26 · [BL-51] S112 — Phase B shipped: the read cap is re-denominated onto bytes, and the line rate is deleted

Commits `9e71f83` (the deliverable) and `b5c1357` (the record). Scope was the operator's **"B-min"**
at Phase 1: re-denominate, delete the line rate, rename J3, correct the false justification — and
present the design before any distributed constant moved.

**`READ_CAP_LINES = 2000` is gone from both distributed tools.** In its place, derived at import so
that no opaque boundary is published: `READ_CAP_TOKENS = 25_000` (stated verbatim by the tool's own
error) × `MIN_BYTES_PER_TOKEN = 2.27` (the measured **floor** of 2.2705–3.0300 over nine real
markdown files in five repos) = **`READ_CAP_BYTES` 56,750 B**. Plus a second measured boundary,
`READ_REFUSE_BYTES = 262,144`.

**The axis change is a dominance result, not a calibration argument.** Over 18 watched ledgers in 5
repos the 2,000-line threshold fires on **3** and stays silent on **8** that a byte threshold at
*any* point in the measured band catches — and it catches **nothing** a byte threshold misses.
B/line spread over that population is **8.6×**; B/token is **1.33×**. Measured on the file that
motivated it: this repo's own `HANDOFFS.md` is **29,300 tokens, 1.17× the cap, truncating today**,
and the shipped guard reported no risk because it is 268 lines.

**A third delivery mode nobody had costed.** Past **262,144 B** a default `Read` is **refused
outright with zero content** — `File content (256.1KB) exceeds maximum allowed size (256KB)` — not
truncated. So *"truncation is ordered top-down, so the front matter still arrives"* holds only
**between** the two boundaries. **Five of the eighteen** fleet ledgers are already past it. It gets
its own risk row and its own edge test: a different failure, not a worse degree of one.

**`LINE_FIRE_BELOW`/`LINE_STOP_ABOVE` were removed, not re-tuned.** The plan's §3 said a *corrected*
cap degenerates the rule; measured, it is degenerate at **every** honest cap. A one-read
`CHANGELOG.md` holds **20.9** records and a one-read `HANDOFFS.md` **4.3**, against a rule demanding
**30** of headroom — satisfiable only because 2,000 lines granted them 2.32× and 8.75× more capacity
than a real read. [`ledger-trimmer-design.md`](docs/planning/ledger-trimmer-design.md) §5.2 already
held the reason: units-of-headroom is well-formed only while the cap *"sits far above normal
operating size"*, and at operating size it prescribes *"a level with hysteresis, not a rate — the
form that terminates"*. Removal was the design's own prescription. Recomputed through the shipped
code, `stops()` is satisfiable at **k ∈ [8..1]** for `CHANGELOG.md` and **[2,1]** for `HANDOFFS.md`
— a real cut exists for both, where every corrected *line* cap gave nothing for either.

**A second distributed copy of the rate rule was found and removed** — `TRIM_LINE_FIRE_BELOW` in
`methodology_dashboard.py`, absent from every plan, backlog and ledger text — along with its
reimplementation `trim_line_headroom()`. **J3 keeps its value under its own name**
(`SEED_PLAUSIBLE_MAX_LINES = 2000`): it asks whether a file is plausibly a fresh seed, which has
nothing to do with truncation, and sharing the name meant a correction made for the reporter's
reasons would silently widen a **refusal** population.

**`READ_CAP_WATCHED`'s justification is corrected; the set is unchanged.** It claimed the two
ledgers are read *in full* at Phase 0 step 6. `SESSION_RUNNER.md:37` **is** step 6 and is
frontier-based on `git log`. Re-derived over **85 transcripts**, each root ledger is read whole
**once** and in part **1,696 / 1,797** times. Narrowing the population is fleet-visible and is
sequenced after this (Phase C / BL-52).

**Fleet effect, measured read-only against all four adopters plus this repo:** read-cap risk rows
**3 → 14**, spreading from one repo to five, five of them the zero-content refusal. No adopter file
was written; `collect_all` reaches no writer, verified by call-graph.

Versions, both **minor**: trim `1.3.0 → 1.4.0` (CLI finding codes change), dashboard
`2.15.2 → 2.16.0`.

**The surface cannot enforce the property under test, and that is stated rather than implied.**
`bin/tests.sh` 287 rows both sides, **286 passed / 1 failed / 0 skipped, zero rows lost, gained or
flipped**; sole failure by name on both sides is Test 9's standing `--source=github` 404. Python
suites **111 / 302 / 42** OK (was 110 / 300 / 41). Twins byte-identical, mirrored last. **No test in
this repository can falsify a read-cap claim** — nothing here invokes the agent's `Read` tool — so a
green suite is evidence that nothing *else* broke. Appendix A was re-run first-hand this session.

**Not done, each deliberately:** Phase C, option D, narrowing `READ_CAP_WATCHED`,
`DEFAULT_BUDGET_BYTES`, the prefix guard (measured this session and handed to Phase C in plan
§12.4), `RECORD_BUDGET_BYTES`, BL-45, issue #75's unsent PR, and **any outward-facing action**.

**Model:** Claude Opus 5 (1M context).


### 2026-08-26 · [ad hoc] S112 claim — Phase B of the read-cap premise correction

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](HANDOFFS.md). **Operator's decision at Phase 1: take Phase B as ratified, but settle
BL-52's precondition question inside it, as act 1.** The two are one question — `methodology_dashboard.py:295`
justifies watching the two ledgers by crediting Phase 0 step 6 with a whole-file read, and
`starter-kit/SESSION_RUNNER.md:37`, which *is* step 6, reads `git log`. Whether the guard should be
**re-denominated**, **narrowed**, or **removed** for those two files cannot be answered without it,
and this session's own Phase 0 read neither ledger whole.

**The design is presented for approval before any distributed constant moves** — the operator's gate,
recorded at claim. `LINE_FIRE_BELOW`/`LINE_STOP_ABOVE` must be re-derived in the **same commit** as
any cap change ([plan §3](docs/planning/read-cap-premise-correction-plan.md)): `choose_cut` falls
through to `return 1`, so a corrected cap alone ships a trim that retains **one** record to every
adopter, with every test green.

**Not in scope, each deliberately:** Phase C, option D as a decision, the 65,536 B ceiling,
`RECORD_BUDGET_BYTES`, BL-42/43/44, **BL-45**, BL-46(2)/47/48/49, BL-50, issue #75's unsent PR, the
cross-repo §11.2 adopter remediation, **and any outward-facing action**.

**Known at claim, measured:** `HANDOFFS.md` 64,977 B against 65,536 B — **559 B clear**, both trim
triggers silent. The trim this session is close-out housekeeping (FM #26), due because this
session's own receipt breaches, not because the trigger fired.

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [BL-52] Post-close-out addendum: the read-cap premise's PRECONDITION fails for the two ledgers

**Recorded after S111's close-out, at the operator's direction, and logged here so Phase 0's
reconcile finds a ledger entry rather than a gap.** The S111 receipt in `HANDOFFS.md` names its own
commits and is left as written; this is a separate action.

**The finding.** `starter-kit/methodology_dashboard.py:295` justifies `READ_CAP_WATCHED` (`:311`) as
*"the files a session is instructed to read **IN FULL** to establish state"*, citing
`SESSION_RUNNER.md` Phase 0 **step 6** for `CHANGELOG.md` and `HANDOFFS.md`. But step 6
(`SESSION_RUNNER.md:37`) is **frontier-based** — `git log -1 --format=%H -- CHANGELOG.md`, then the
commits after it. **It reads git history, not the file.** Phase 3A reads **one receipt**, not the
ledger.

**The premise holds for three of the five watched names and fails for exactly the two the trimmer
exists to bound.** Steps 1–3 genuinely do say *read*. Step 6 does not. The comment's
SEED-vs-TRACKED population logic is careful and is **not** what is wrong; the sentence saying why the
two ledgers are in the set is.

**Observed:** S111's own Phase 0 followed step 6 exactly and never read `CHANGELOG.md` whole.

**It strengthens BL-52 without settling it.** The missing measurement is how often anything reads
these files whole — put near 1-in-81 by an earlier session, **not re-run**, and a count of exactly
this kind was once wrong by **13×**. Re-derive before using. Says nothing about the byte metric.

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] S111 close-out — Phase A shipped; self-score 8/10, predecessor S110 scored 8/10

Phase 3D receipt in [`HANDOFFS.md`](HANDOFFS.md), **inside the 12,288 B per-record budget** — over by
546 B on the first pass and cut from the **trailing prose**, which is where `bin/check-handoff` says
to cut, because a record is the opening fence through the **next** opening fence. Commits: `d5a4fb4`
(claim) · `730a309` (trim) · **`84abc60` / `86037bd` / `85a2158`** (Phase A) · `b8ecccf` · `979dc73` ·
`90d9b76` · this close-out.

**Phase A is complete and the plan is RATIFIED.** Six distributed carriers corrected — **3 `TRACKED`**
(reach every existing adopter at their next `bin/sync`) and **2 `SEED`** (future adopters only).
**No numeral moved.** Phases B and C are not started.

**Three findings, each from running rather than reading.**

**Dragon 8 settled, and the plan's own test could not have settled it.** An explicit `limit` spanning
an over-cap region **neither bypasses the cap nor truncates — it errors and returns no content at
all.** Three delivery modes, not two. Probe D's "returned whole" is therefore not an artifact.

**Phase A's DONE criterion was unsatisfiable as written** — it matches a live, distributed, *correct*
sentence about `$(...)`. The corrected command returns **0** (§11.3).

**I shipped a benefit claim I had not established, and an operator relay caught it.** Replacing
*"protects against silent truncation"* with *"protects against an unread tail"* substituted one
unverified benefit for another — the exact move Phase A exists to stop. Corrected in the seeds **and**
in the two TRACKED tools; **BL-52** raised, then narrowed by measuring that the argument is
**regime-dependent** and does not reach this repo.

**Verification.** Control 287 rows **286 / 1 / 0**; after **286 / 1 / 0**; row-for-row, both
populations asserted non-empty: **zero status flips, zero skipped**, one pair differing only in a
derived count this session's trim moved. Sole failure both sides by name: `github source dry-run
failed`. Python suites **300 / 110 / 41 OK**, re-run **after** the mirror. Twins `diff -q`
byte-identical. Trim losslessness three ways including an independent inverter: **12/12
byte-identical, 0 lost, 0 unexplained.** `check-links` OK (88/22) · `check-learnings` OK (37) ·
`check-handoff` + `--all` OK · `trim --check` silent on both · `BACKLOG-DETAIL.md.verify.sh` OK.

**The surface cannot enforce the property under test, and that is stated rather than glossed:** no
test here can invoke the agent's `Read` tool. A green suite proves nothing *else* broke — Appendix A
is the only instrument, and it must be re-run every phase.

**FM #28 gate, measured after the last write.** `HANDOFFS.md` **64,977 B** / 225 ln;
`CHANGELOG.md` **47,207 B** *before this entry*; `starter-kit/FRAMEWORK_LEARNINGS.md`
65,520 B (**16 B free — BL-45 still blocks Phase 3C, third session running**);
`docs/planning/BACKLOG.md` 30,915 B. **`main` 69 ahead of `origin/main`, nothing pushed.**

**Carve-out re-derived by importing `DISTRIBUTION` and reading the SOURCE column:** 3 TRACKED,
2 SEED, 10 canonical. **No outward-facing action.**

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [BL-52] S111 — the relayed critique measured: it is regime-dependent, and this repo is in the other regime

**BL-52 addendum.** The critique's load-bearing premise — *"the tail costs nothing, because nothing
reads it"* — is true **only once a file is already well past the cap**. Below it the whole file is
delivered and every byte is paid for; **at** the boundary, a trim moves a file from *truncated* to
*fully delivered*, which is not cosmetic.

Measured by the free error path (an over-cap `limit` reports the span's token count and returns no
content): this file was **26,723 tokens before this session's trim — OVER the 25,000 cap** `[M]`, and
is ~18,800 after `[D]`. **This repo's ledgers hover at the cap boundary**; the relaying repo's is
reported at 25,578 lines, ~**40×** the cap `[C]`. Their conclusion may be right for them and **does
not transfer here** — the same failure shape this repo keeps recording, a figure measured in one
regime carried into another.

**So the trim run earlier in this session did real work on both axes**, which I could not have
asserted when I ran it: I ran it because the ceiling forced it, and only measured afterwards that the
file had actually been over the read cap too.

**BL-52's scope narrowed accordingly:** what is in question is the **line metric's remedy**. The byte
metric is **not**, and BL-52 must not be closed by retiring both.

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [BL-52] S111 — BL-52 raised; the design record annotated; the plan RATIFIED and Phase A closed

**The plan's status moves `DRAFT` → `RATIFIED`** (operator, this session's Phase 1: A → B → C as
three separate sessions; the one-pass fix stays declined, option D stays deferred-on-evidence).
**Phase A is shipped; B and C are not started.** A new **§11** records what shipped, what existing
adopters still need by hand, and two findings Phase A produced that the plan did not anticipate.

**§5.4 settled and executed:** *leave the design and audit records, annotate
[`ledger-trimmer-design.md`](docs/planning/ledger-trimmer-design.md) only* — it is the document a
future session reads to re-derive the rate rule, which is what earns it the annotation the others do
not get. Its false table cell is struck through in place, not rewritten (FM #22), with a block note
carrying the measurement, the reproduction, and both consequences.

**BL-52 raised** — *the line metric measures a condition trimming may not remedy.* From the critique
the operator relayed mid-session, but **argued from this session's own probes**: truncation is
ordered top-down, these ledgers are newest-on-top, so a cut removes records a whole-file read was not
delivering anyway. **Phase A did not fix this — it exposed it.** While truncation was believed
*silent*, trimming was the only way to avoid an undetectable gap and the rationale held; once it is
known to be **announced**, the rationale has to be re-argued rather than inherited.

**What BL-52 deliberately does NOT claim**, because S111 did not measure it: anything about the
**byte** metric (a different claim — context tax), and anything resembling *"stop trimming"*, which
is an operator decision with fleet-wide blast radius. The relayed figures are marked `[C]` — that
repo's, not re-run here.

**Measured here, since the same shape was asserted about this repo:** `CHANGELOG.md` front matter is
**14,295 B / 185 ln = 39% of the file** and is read first, so the front-matter point is directionally
right here too; `HANDOFFS.md` front matter is **6,362 B / 72 ln = 11%**, because **S109 already
shipped that compaction** — the relayed critique's option E, arrived at independently.

**Dragon 8 settled, and Appendix A's probe D found unsound as specified** — it names a file that
returns whole either way, so it cannot discriminate. §11.3 records the corrected form.
**Phase A's §8 DONE criterion found unsatisfiable as written** — one live, distributed, *correct*
sentence about `$(...)` matches it. §11.3 records the corrected command, which returns **0**.

**Verification.** `BACKLOG-DETAIL.md.verify.sh` **OK** — C1–C5 green, 18 items byte-identical,
BL-52 correctly reported as raised-since and **not** a finding.

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] S111 — the detector reworded rather than exempted, so it stays a zero-hit tripwire

Phase A's verify grep still returned one row after the corrections, and the row was **`README.md`
quoting the false phrase in order to disclose that it was false**. Quoting-to-correct is not
asserting — but a detector that returns a permanent row is a detector nobody will ever read again.

**S106's precedent applies and was followed** (§5.5): *rewrite the live sentence rather than exempt
it, keeping the zero-hit grep a live detector without falsifying history.* The disclosure stays and
now names the old claim without reproducing its exact words. **An exemption list would have retired
the detector instead** — which is the failure mode, not the fix.

`git grep -nE 'no (error|missing-data) marker|silently truncat' -- starter-kit bin tools README.md`
now returns **0 rows** across every live path, with one documented carve-out: eleven shipped
`.verify.sh` files and `starter-kit/methodology_trim.py` carry *"command substitution strips trailing
newlines, which silently truncates the LAST record"* — a **correct** sentence about `$(...)`, with no
connection to the read cap. **Repairing it would be a defect.**

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] S111 — Phase A (3 of 3): the same unearned-remedy caveat pushed into the two TRACKED tools

The correction made to the SEED tables in the entry below, carried into the two files that are
**`TRACKED`** — so unlike the seeds, **this half does reach every existing adopter** at their next
`bin/sync`. `starter-kit/methodology_trim.py`'s two-metric header and
`starter-kit/methodology_dashboard.py`'s shipped **`high`**-severity risk text both told the reader
what the line metric *protects against*; neither had ever established that archiving *remedies* it.

Both now state the measured mechanism, then the caveat, then the boundary: **the byte metric is a
separate claim — context tax, not read delivery — and is explicitly excluded**, so the caveat cannot
be read as retiring both metrics at once. The dashboard's risk row previously ended with the bare
imperative *"Archive it"*; it now says archiving's effect here is open, because the row fires on a
file whose unreachable records a cut would not make reachable.

**The mirror was re-taken and re-verified after this edit** (dragon 2): `diff -q` byte-identical,
suites re-run **after** the mirror rather than before — S37's failure was recording numbers taken
before a mirror that then moved.

**Verification.** `tools.test_methodology_dashboard` **300 OK** (4 skipped, pre-existing) ·
`tools.test_methodology_trim` **110 OK** · both re-run against the final tree. The seven suite
assertions that string-match `"read cap"` inside the risk description still pass — the replacement
text was written to keep satisfying them.

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] S111 — Phase A (2 of 3): the two SEED doctrine tables, `README.md`, and this file's own front matter

**The `SEED` half of Phase A, and the half that cannot be delivered by syncing.**
`bin/_manifest.py` marks `starter-kit/CHANGELOG.md` and `starter-kit/HANDOFFS.md` as **SEED**, and
`bin/sync:225-230` writes a SEED **only when the destination is absent and never overwrites it
afterward**. So this correction reaches **future adopters only**; every already-bootstrapped project
keeps the false doctrine table until someone edits it **by hand, per repo**. Same defect class as
BL-46/47/48. The remediation note that has to accompany it is a separate commit.

**A mid-session critique from the operator changed this text after it was first written, and the
change is the substantive part of this entry.** Relayed from a `../model_project_constructor`
session: *if the ledgers are newest-on-top and reads are ordered top-down, what is the rationale for
trimming?* The first draft of these rows had replaced *"protects against **silent truncation**"*
with *"protects against **an unread tail**"* — **which is substituting one unverified benefit claim
for another, the exact move Phase A exists to stop.**

**The deduction follows from this session's own measurements, not from the relay.** Probe B
delivered lines 1–10 of 101; probe C's prefix was lines 1–700 of 2,000 — truncation is **ordered
top-down**. These ledgers are **newest-on-top**. Therefore the records a cut removes are ones a
whole-file read **was not delivering anyway**: the delivered prefix is the same before and after the
trim, and what changes is that the reader stops being **warned**. The rows now say the metric
**measures** an unread tail and **does not, on its own, establish a remedy**, and point at **BL-52**.

**What was NOT decided here, deliberately.** Whether to stop trimming, whether the byte metric
survives the same argument, and the dedup between the two dashboard rows — that last is **Phase C**,
and the seeds' *"neither subsumes the other"* sentence is therefore **left standing untouched**.

**`README.md:390`** republished the false rationale as the framework's own; rewritten to state
measured behaviour, to name what it cannot prove, and to say plainly that the earlier claim was
false. **This file's front matter** carried the same claim twice — the rate rule's *"2,000-line agent
`Read` cap"* and the incident line's *"silently dropping its ten oldest entries"*. The second is
corrected with its own diagnosis: truncation was announced; **what was silent was that nothing in the
repo was checking**, which is why the overrun was found by accident.

**No numeral moved.** **Frozen records untouched** — `docs/archive/**`, and every historical
statement inside this file's own records (FM #22, §5.5).

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] S111 — Phase A (1 of 3): the false read-cap premise corrected in the three TRACKED tools

**Phase A of [`read-cap-premise-correction-plan.md`](docs/planning/read-cap-premise-correction-plan.md),
ratified by the operator at this session's Phase 1.** The claim is corrected; **no numeral moved** —
`READ_CAP_LINES` is still `2000`, `LINE_FIRE_BELOW` still `15`, `LINE_STOP_ABOVE` still `30`. Phases
B and C are explicitly not started.

**These three are `TRACKED` in `bin/_manifest.py`, so this correction reaches every existing adopter
at their next `bin/sync`** — read off the SOURCE column by importing `DISTRIBUTION`, never by
grepping the bare filename, which matches the DEST half and inverts the answer.

| file | what was false |
|---|---|
| `starter-kit/methodology_dashboard.py` | the `UNIT`/`VALUE` block, and the shipped **`high`**-severity adopter-facing risk text |
| `starter-kit/methodology_trim.py` | `READ_CAP_LINES`' own comment, and the line metric's stated raison d'être |
| `starter-kit/context_budget.py` | the docstring justifying the LINES axis *"because that is the unit an agent's read cap comes in"* |

**What replaced it — measured this session, not relayed.** Truncation is **announced, not silent**:
an over-cap read returns a `PARTIAL view` banner naming the delivered span, the true length, the
token count and the cap. It does **not** return 2,000 lines. And the cap is **token-denominated**.

**A fourth behaviour, which the plan did not know about and which settles its dragon 8.** An
explicit `limit` spanning an over-cap region **neither bypasses the cap nor truncates — it returns
an error with no content at all** (`File content (199405 tokens) exceeds maximum allowed tokens
(25000)`). The plan's stated controlled pair could not have discriminated this: it reads a file that
comes back whole either way. Run instead on a file that *does* truncate, `limit` is proved not to
bypass — so probe D's "returned whole" is **not** an artifact and §1.4's ratio range stands.

**Every corrected site names the reproduction rather than a replacement number.** §7's least
confident point is whether 25,000 tokens is stable across harness versions; a numeral would rot, the
command does not. Each site now points at Appendix A and says what it cannot prove.

**The unit argument was inverted, not deleted.** The old comment's own evidence — a ~3× B/line
spread, re-measured at **74.7** here against **227.4** next door — argues the *opposite* of what it
was written to argue, because tokens track bytes: it is a single **line** threshold that is wrong for
one ledger by 3×. Bytes are only a proxy too (2.42–2.66 B/token), so no conversion is published.

**Each site also now carries the coupling that makes the cheap fix dangerous** (BL-51): the two
thresholds are denominated in *records of headroom to this number*, so correcting it alone drives
`choose_cut` to `return 1` — one record retained at every adopter, with every test green.

**Verification.** Three Python suites **300 / 110 / 41, all OK** (4 skipped, pre-existing). Twins
**byte-identical** (`diff -q`), mirrored **last** per the plan's dragon 2. `check-links` OK (88/22).
**Seven suite assertions string-match `"read cap"` inside the risk description** and one matches
`"CHANGELOG.md is 2,090 lines"` — found *before* editing, and the replacement text was written to
keep satisfying them rather than discovered by a red suite.

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-08-25.md` (12 record(s), 65,012 B → 32,900 B)

**Written by:** `methodology_trim.py` v1.3.0 — a tool action, not a session's judgment.
Moved the oldest **12** record(s) (2026-08-25 → 2026-08-25) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-08-25.md`](docs/archive/CHANGELOG-through-2026-08-25.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-08-25.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-25.md.verify.sh)
rather than trusting a digest printed here. Live file 65,012 B → 32,900 B (−49.4%).

### 2026-08-26 · [ad hoc] S111 claim — Phase A of the read-cap premise correction

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](HANDOFFS.md). **The operator ratified `A → B → C` at Phase 1** and directed Phase A
this session; §5.4's open question is settled — *leave the design/audit records, annotate
`ledger-trimmer-design.md` only*. Deliverable: the live behaviour-claim sites in
[`read-cap-premise-correction-plan.md`](docs/planning/read-cap-premise-correction-plan.md)
§5.2/§5.3/§5.4 rewritten to state **measured behaviour and its reproduction method**, **no numeral
moved**, plus the existing-adopter remediation note §5.1 requires.

**Not in scope, each deliberately:** Phase B, Phase C, `READ_CAP_LINES`' value,
`LINE_FIRE_BELOW`/`LINE_STOP_ABOVE`, option D, the 65,536 B ceiling, `docs/archive/**` and every
frozen record (§5.5), BL-45, BL-50, issue #75's unsent PR, **and any outward-facing action**.

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] S110 close-out — read-cap plan delivered; self-score 8/10, predecessor S109 scored 8/10

Phase 3D receipt in [`HANDOFFS.md`](HANDOFFS.md), **12,237 B inside the 12,288 B per-record budget** —
reached in seven passes, each one run against `bin/check-handoff` rather than estimated, every cut
taken from the trailing prose where the checker says to cut. Commits: `8decf71` (1B claim) +
**`c2bc56f`** (the deliverable) + `9038e40` (the trim) + this close-out.

**Two findings this session did not set out to make, both from checking rather than reasoning.**

**BL-50 — the trimmer refuses a correct trim, and it is a distributed defect.** `insert_pointer`
(`starter-kit/methodology_trim.py:940-950`) appends `"\n" + block` when the front matter does not
already end `"\n\n"`; `L2`'s confinement proof (`:582-586`) removes only `block` and never that
injected newline, so the reversal cannot restore the original bytes and the run dies reporting a
losslessness failure **that is an artifact of its own insertion**. Reproduced in isolation — first
difference at char 6126, the tool's own number — rather than forced past. It became reachable
because S109's compaction removed the trailing pointer blocks that used to end `"\n\n"`. Worked
around with a one-byte fork-side data edit; **not** with a standalone `---`, which would trip
`[ZONE_UNCLASSIFIED]` (BL-46's failure). Learning #37 one level down.

**BL-51 — `choose_cut` makes the read-cap correction dangerous.** `stops()` has exactly one caller,
and `choose_cut` (`:876-881`) falls through to **`return 1`** when nothing satisfies it. So
correcting `READ_CAP_LINES` alone would make every adopter's next `--write` retain **one record**.
S94 measured a cut to *two* taking the suite 235/1 → 229/6 (Learning #31). Every existing test stays
green, because nothing evaluates the rate rule at a corrected cap.

**Method notes worth more than either finding.** A ratio measured on one content type does not
transfer to another — 2.419 B/token from ledger content against ≥2.62 from prose — and probe D
killed a self-consistent table this session had already drafted. **A `--check` is not a dry run:** it
returns at `:1698`, before the L1/L2/L3 machinery, so it reports a green trigger for a trim that will
refuse. And a subagent's citation is a claim: **301 reported sites, every one re-read and verified
against the file before use.**

**Phase 3C NOT discharged, and it is structural, not skipped.** `starter-kit/FRAMEWORK_LEARNINGS.md`
is **16 B** from its ceiling (BL-45) and no budget-conforming row fits. **Two learnings are earned
and owed**, both recorded in the receipt's gotchas: *a ratio is a property of its content type, not
of the corpus*, and *`--check` is not a dry run*.

**Verification.** Suite control 287 rows **286 passed / 1 failed / 0 skipped**; after the trim
287 rows, **286 / 1 / 0**; row-for-row, both populations asserted non-empty: **zero status flips,
zero skipped**, five rows differing only in a derived count the trim moved. Sole failure both sides
by name: `github source dry-run failed` (Test 9's standing 404). Trim losslessness three ways
including an independent inverter modelling the declared link-rebase transform: **6 records,
6 byte-identical, 0 unexplained**. `check-handoff` OK · `--all` OK (4) · `check-links` OK (88/22) ·
`check-learnings` OK (37) · `trim --check` silent · `context_budget.py` no file over a ceiling
(bare exit **1 = WARN**, growth run 64/10, ceiling-independent) · `BACKLOG-DETAIL.md.verify.sh` OK.

**FM #28 gate, measured after the last write.** `HANDOFFS.md` **52,808 B** (12,728 B clear), front
matter **6,362 / 7,168 B**; `CHANGELOG.md` 59,542 B *before this entry*;
`starter-kit/FRAMEWORK_LEARNINGS.md` 65,520 B (**16 B free**); `docs/planning/BACKLOG.md` 30,458 B.
`main` **61 ahead of `origin/main`**, nothing pushed.

**Carve-out re-derived by importing `DISTRIBUTION` and reading the SOURCE column** — after a first
attempt grepped the bare filename and hit the DEST half of
`("starter-kit/HANDOFFS.md", "HANDOFFS.md", SEED)`. **Nothing this session touched is a manifest
source. No adopter receives anything. No outward-facing action.**

**Open for the operator:** ratify or reject the plan's A → B → C (§7), and answer §5.4 (annotate the
design records, or leave them?). **BL-45 still blocks Phase 3C for the next session too.**

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-08-25.md` (2 record(s), 66,615 B → 44,725 B)

**Written by:** `methodology_trim.py` v1.3.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-08-25 → 2026-08-25) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-08-25.md`](docs/archive/HANDOFFS-through-2026-08-25.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-08-25.md.verify.sh`](docs/archive/HANDOFFS-through-2026-08-25.md.verify.sh)
rather than trusting a digest printed here. Live file 66,615 B → 44,725 B (−32.9%).

### 2026-08-26 · [ad hoc] S110 — plan delivered: correcting the read-cap premise

**The deliverable:** [`docs/planning/read-cap-premise-correction-plan.md`](docs/planning/read-cap-premise-correction-plan.md),
**DRAFT awaiting ratification.** A planning session — nothing implemented, no numeral changed, no
distributed file touched (FM #18/#19). Carve-out re-derived off `bin/_manifest.py`'s **SOURCE**
column, after a first attempt hit the DEST column and read the root ledgers as distributed: all
three files this session touched are **canonical-only**.

**Recommends A → B → C as three separate sessions, and declines the one-pass fix.**

**Three defects in one distributed constant,** separated because they have different remedies:
`READ_CAP_LINES = 2000`'s stated behaviour is false, its unit is wrong (the cap is ~25,000 **tokens**),
and its value is ~**2.9×** too permissive at this repo's ledger density.

**The finding that decided the plan's shape — no grep for `2000` reaches it.** `LINE_FIRE_BELOW = 15`
and `LINE_STOP_ABOVE = 30` are denominated in *records of headroom to the cap*. Run through the
trimmer's own `evaluate_trigger` arithmetic at both ledgers' real baselines: at a corrected cap the
rate rule **degenerates on both** — max possible headroom falls to **12** and **22** records against
a `>30` stop, so `stops()` (`byte_ok and line_ok`) can never return true. **And `stops()` has exactly
one caller.** `choose_cut` (`methodology_trim.py:876-881`) loops the retention count down and
**`return 1`** when nothing satisfies it — so the next `--write` at every adopter would retain **one
record** and archive the rest. S94 measured a cut to *two* taking `bin/tests.sh` from 235/1 to 229/6
(Learning #31); S96 corrected that to six assertions (Learning #33). **Every existing test stays
green**, because nothing evaluates the rate rule at a corrected cap.

**The structural result.** `DEFAULT_BUDGET_BYTES = 64 * 1024 = 65,536 B` sits *inside* the measured
one-read band of **60,475–66,425 B**. The framework already ships a guard on the right axis at very
nearly the right value; the line cap is a redundant second guard on the wrong axis firing ~3× late.
This answers S38's residual 1, which `methodology_dashboard.py:3001-3003` records as undecided.

**The comment's own cited basis refutes it.** `git show 3aee4e3^:CHANGELOG.md` → **2,090 lines /
186,704 B**, which is 2.8–3.1× the token cap: it had been truncating since roughly line **676–743**.
The constant records where the problem was *noticed*, not where it *starts*.

**Four probes [M], reproduction in Appendix A.** 3,000 lines returned whole; 101 lines / 199,700 B
cut at line 10 with a loud `PARTIAL view … cap 25000` banner; **2,000 lines of this repo's own
ledger content cut at line 687 of 2,001**. The fourth **falsified this session's own first draft** —
`FRAMEWORK_LEARNINGS.md` (65,520 B) returned **whole**, so the 2.419 B/token ratio does not transfer
across content types (measured range 2.42–2.66). The plan therefore prescribes the **method**, not a
new numeral.

**The inventory caught the plan itself.** Six blind search angles plus two adversarial critics;
**255 of 255 reported citations re-read and machine-verified** before use. A first draft written from
one reader's grep named 19 sites; the completed sweep found live sites in **ten further files** —
three of them **distributed seeds**, including the two that state the false claim as doctrine in a
table (`starter-kit/CHANGELOG.md:103`, `starter-kit/HANDOFFS.md:97`).

**And those two cannot be repaired by syncing.** Both are `SEED` in `bin/_manifest.py`, and
`bin/sync:225-230` writes a SEED only when the destination is absent, **never overwriting it after**.
A correction reaches **future adopters only**; every already-bootstrapped project keeps the false
doctrine permanently. That is the same defect class as BL-46/47/48 and is the substantive reason
this work batches with them.

**The surface, named per `SESSION_RUNNER.md` §Planning Sessions:** every DONE criterion is
demonstrated on the local suites — **and that surface cannot enforce the property under test.** The
three carriers are Python and cannot invoke the agent's `Read` tool; `bin/tests.sh` has **zero**
`READ_CAP` references. **No test in this repository can falsify a read-cap claim**, so each phase
requires Appendix A re-run in the implementing session, with its output in the receipt.

**Fork-side only. Nothing outward-facing.** Two open questions are left for the operator rather than
decided: whether to annotate the design records (§5.4), and ratification of A → B → C (§7).

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] S110 claim — plan the read-cap premise correction

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](HANDOFFS.md). **A planning session: the plan is the deliverable and nothing is
implemented** (FM #18, FM #19).

**Why now.** The operator handed over `../model_project_constructor/docs/planning/ledger-budgets-review.md`
(that repo's S248, 2026-08-26). It finds its own trim trigger's stated rationale — *"1,500 lines
(75% of the 2,000-line agent read cap)"* — false by measurement, and recommends replacing a
file-length target with a front-matter budget. **That premise is not only theirs: this repository
authors and distributes it.**

**Three probes, run here rather than relayed.** Their two reproduced exactly; the third is this
session's, and it is the one that decides whether this is a documentation defect or a real one:

| probe | file | result |
|---|---|---|
| A | 3,000 ln / 21,000 B | **returned whole** — the documented "up to 2000 lines" did not bind |
| B | 101 ln / 199,700 B | **cut at line 10**, with a `PARTIAL view … (199405 tokens, cap 25000)` banner naming the exact next call and warning not to answer from the page alone |
| C | **2,000 ln of real `CHANGELOG.md` content at this repo's own 74.8 B/line density** | **61,844 tokens against the 25,000 cap — truncated at line 687 of 2,001, 34% delivered** |

**The cap is token-denominated at 25,000, and truncation is announced, not silent.**

**The exposure is distributed, and read off `bin/_manifest.py`'s SOURCE column rather than the bare
filename.** `READ_CAP_LINES = 2000` ships to every adopter root through three TRACKED tools:
`starter-kit/methodology_trim.py:92` (headroom arithmetic at `:729`/`:809`, a refusal signal at
`:1589`), `starter-kit/methodology_dashboard.py:269` (a **high**-severity adopter-facing risk at
`:3006-3010`, the headroom metric at `:1046`), and `starter-kit/context_budget.py`'s `max_lines`
axis. Its stated justification at `starter-kit/methodology_dashboard.py:264`, republished at
`README.md:390` — *"a Read past it returns the first 2,000 lines with no error and no missing-data
marker"* — is **false in both halves**, and probe C says the number is also wrong in the unsafe
direction: at this repo's density the cliff is near line **690**, so the guard is ~**2.9×** too
permissive and a ledger at 1,999 lines passes every check while delivering a third of itself.
`tools/test_methodology_dashboard.py:3191-3193` **pins the trimmer's and the dashboard's literals to
each other**, so the two agree and are wrong together.

**Two qualifications recorded at claim so the plan cannot overstate.** (1) The practical consequence
here is **small**: truncation is *ordered* top-down and these ledgers are newest-on-top, so Phase 0's
frontier and Phase 3A's single-receipt read land inside the delivered prefix — this repo measured
whole-file reads at 1-in-81. What is wrong is the published claim and the constant's unit more than
the outcome. (2) **This repo has already arrived at the sibling document's recommendation by another
route** — S105/S109's per-record budget and `HEADER_RESERVE_BYTES` are its Options D and E, shipped.
The convergence is corroboration, not a new finding.

**Also standing at claim, neither of them this session's deliverable.** `HANDOFFS.md` is 62,717 B
with **2,819 B clear**, so this session's close-out receipt breaches the ceiling while `--check`
still reports *trigger does not fire* — confirmed silent at this Orient, exactly as S109 predicted.
The trim is **close-out housekeeping**, not a second capability. And `starter-kit/FRAMEWORK_LEARNINGS.md`
is **16 B** from its ceiling, so **Phase 3C cannot be discharged without the operator's BL-45 decision.**

**What does NOT change:** anything implemented, `RECORD_BUDGET_BYTES`, the 65,536 B ceiling, Test
34's floor of 3, and every historical statement of the 2,000-line cap in this ledger and in the
frozen shards, which are records of what was believed when written (FM #22).
**Fork-side only. Nothing outward-facing** — the fix batches with BL-46(2)/47/48/49 for one later PR.

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [BL-46] Cross-repo: BL-46's half (1) closed by the adopter, and its remedy shown too narrow — BL-47/48/49 raised

**Written by:** a session running in `../vscode_quarto_ext` (its S254/S255), acting on that repo's
operator directive. **No distributed file in this repository was touched** — this is a backlog
filing plus this ledger entry. Nothing outward-facing; nothing pushed.

**BL-46 half (1) is DONE.** That repo deleted the blocking footer and ran both overdue trims:
`CHANGELOG.md` **831,830 → 44,190 B** (230 records archived), `HANDOFFS.md` **1,801,150 → 52,850 B**
(211 receipts). Both triggers now stand down. Losslessness established four ways — the tool's
in-process L1/L2/L3+P1A, its emitted `verify.sh`, an independent verifier sharing no code with it,
and a four-lens adversarial pass tasked with *refuting* the claim, which found none.

⚠ **BL-46's DIAGNOSIS IS RIGHT AND ITS PROPOSED DETECTOR WOULD NOT HAVE FIRED.** BL-46 says the
adopter *"never deleted"* the seed sentinel. They **had** deleted it — `METHODOLOGY-SEED-SENTINEL`
was already absent — and the trimmer refused anyway, because what blocks it is the **trailing `---`
and the comment below it**, which the seed's instruction never mentions. `starter-kit/HANDOFFS.md`
carries the sentinel at line 20 and, at line 160, an instruction reading only *"Delete the
seed-sentinel line above"*. **An adopter who follows it exactly still ends up with an inert
trimmer** — which is what happened, for 216 receipts. BL-46's proposed check keys on the sentinel;
it must key on the footer, or the seed must instruct removing both. Annotated in place.

**Three items raised, none duplicating anything here (checked before filing):**
- **BL-47** — the seed `context-budget.json` omits `CHANGELOG.md`/`HANDOFFS.md`, the two files
  `methodology_trim.py` exists to bound, at the 65,536 B constant both tools already share. This is
  BL-46 one level up: BL-46 asks why nobody read the trimmer's output; this is why. That adopter had
  the trimmer since S188 and `context_budget.py` **not at all** until S255.
- **BL-48** — the seed `HANDOFFS.md` lacks the `This file currently holds **N**` sentence its own
  `LedgerSpec.regenerated` declares, so every adopter gets `FRONTMATTER_FIELD_ABSENT` on every trim,
  forever. This repo's root copy *has* the sentence, so the mismatch is invisible from here.
- **BL-49** — `content_probe` is consulted at exactly one call site, `classify_empty`, so a
  **partial** grammar mismatch is never tested. Measured consequence: that repo's `CHANGELOG.md`
  holds 236 dated `###` headings and 230 matched records (six predate its source-tagging
  convention), so a **frozen** shard is published in four places as spanning from `2026-06-30` when
  its true oldest entry is `2026-06-27`. Every L1/L2/L3 assertion passes — nothing is lost, only the
  *description* is wrong, and the description is the index people search.

**Also confirmed from the adopter side:** **BL-27's fix works.** Syncing that repo `v1.1.1 → v1.3.0`
and regenerating its `HANDOFFS` shard proof turned `FAIL: L2 FRONT MATTER lost 1 line(s)` into `OK`.

**Verification:** `docs/planning/BACKLOG-DETAIL.md.verify.sh` **OK** — C1–C5 green, 18 split items
still byte-identical, new items correctly reported as raised-since and not a finding.

