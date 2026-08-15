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

---

## 2026-08

### 2026-08-15 · [ad hoc] S90 close-out — receipt written, self-score 8/10, predecessor S89 scored 9/10; see the `[BL-37]` entry below for the substantive work

### 2026-08-15 · [ad hoc] Framework Learning #27 appended — a tool can print its own refutation beside its answer, and the answer still gets believed

A derived number and its goodness-of-fit statistic are two claims, and only the first gets read:
`--calibrate` printed `R² = 0.0513` immediately beside `⇒ 14.45 bytes/token`, with nothing marking
the estimate unusable. Same shape as this tool's own founding evidence — a dashboard printed
`Large files detected` at every Phase 0 and 15+ consecutive sessions read past it. Surfacing a
signal is not gating on it. Row 27 in [`starter-kit/FRAMEWORK_LEARNINGS.md`](starter-kit/FRAMEWORK_LEARNINGS.md)
(DISTRIBUTED, append-only; `#14` stays reserved), so `bin/check-learnings` now reports 26 rows.

### 2026-08-15 · [BL-37] Half (a) done — the FM #28 context-budget gate now runs on the repo that authors it, and calibrating it found two defects in the distributed tool

**`.context-budget.json` provisioned at this repo's root and calibrated.** BL-37's half (a): this
repo distributes the FM #28 size-ceiling gate to every adopter (`bin/_manifest.py:54` ships
`starter-kit/context_budget.py` → adopter `context_budget.py`, `:60` ships the seed → adopter
`.context-budget.json`) and had never configured it for itself — the same blind-at-home shape as
BL-29 and [issue #59](https://github.com/KJ5HST/methodology/issues/59), arriving through
configuration rather than path resolution. Fork-local: **no distributed file was edited.** Run it
with `python3 starter-kit/context_budget.py` — there is no root copy of the tool here.

**First run, and it is honest rather than green.** `CLAUDE.md` 11,064 B / 18,600 B **ok**;
`CHANGELOG.md` 48,469 B **ok**; `starter-kit/FRAMEWORK_LEARNINGS.md` 42,249 B / 60,000 B **ok**;
**`HANDOFFS.md` 72,449 B and `docs/planning/BACKLOG.md` 91,857 B both `over` the 65,536 B ceiling**,
exit 2. Both are pre-existing and independently corroborated — `methodology_trim.py --file
HANDOFFS.md --check` reports `trigger FIRES` on the same 72,449 B, and S89 measured BACKLOG.md's
excess as *live open work* (16 open items = 68,195 B = 1.04× the ceiling on their own). Neither is
fixed here (FM #17) and neither ceiling was raised to silence it, which is the seed's own
instruction.

**Those five figures are the FIRST RUN, measured before this session wrote anything of its own —
say which you mean.** This entry and the `BL-38` item below have since grown `CHANGELOG.md` and
`docs/planning/BACKLOG.md`, and the close-out receipt grows `HANDOFFS.md` again, so the current
numbers are larger and the measurer is inside them. Re-derive rather than trust any of it:
`python3 starter-kit/context_budget.py`. This file deliberately states no self-size for the same
reason S89 recorded — writing the number in changes it.

**Every ceiling is cited, not invented.** `max_bytes: 65536` on all three ledger-class files is
`starter-kit/methodology_trim.py:69` `DEFAULT_BUDGET_BYTES = 64 * 1024`, the number BL-9/BL-32/BL-36
have all measured against. `CLAUDE.md`'s `max_lines: 200` is this framework's own published figure
(`starter-kit/BOOTSTRAP.md:199`, *"Claude Code targets roughly 200 lines"*), converted to
`max_bytes: 18600` at the file's measured density (92.97 B/line × 200 = 18,594). `HANDOFFS.md`'s
`max_lines: 1200` is that file's own front-matter archive trigger. `CHANGELOG.md`/`BACKLOG.md` use
`max_lines: 2000`, the agent `Read` cap BL-9's L2 was already bitten by. Each of the five entries
carries its derivation in a neighbouring `_` key, and the two numbers that are **inherited rather
than derived** (`growth_run: 10`, `FRAMEWORK_LEARNINGS.md`'s 60,000 B) say so in their own text
rather than passing as measured.

**`bytes_per_token` is 2.80, measured here — and the shipped `--calibrate` disagrees for reasons
that are its own defects.** Regressing each session's opening context on `CLAUDE.md`'s size across
n=75 transcripts: `opening_tokens ≈ 42,033.2 + 0.356891 × bytes`, **R² = 0.8083 ⇒ 2.8020 B/tok**,
fixed harness floor **42,033 tok**. Corroborated twice locally: the same fit with only the lineage
defect corrected gives **2.93** (R² = 0.6854), and the natural experiment across `7603f10`
(`CLAUDE.md` 52,909 → 8,519 B) using the two sessions bracketing it within 20 minutes each side
gives 44,390 B / 17,616 tok = **2.52**. Three local estimates spanning 2.52–2.93, against the seed's
2.93 from an unrelated project.

**Two defects in `starter-kit/context_budget.py`'s `calibrate()`, separated by running the fit four
ways rather than asserted.** As shipped it prints **14.45 B/tok at R² = 0.0513** — noise, and
implausible on its face for dense markdown. **D1 (causal):** it derives the size history with
`git log -- <target>`, which walks *all* merged ancestry, so upstream's own `CLAUDE.md` lineage
(52,909 / 53,372 / 58,652 B, author `KJ5HST`, reachable only through the merges `8b87086` and
`aa378ab`) interleaves by commit date with this fork's 8,519 → 11,064 B lineage and *"size at time
T"* stops being a function. **D2:** it sorts and compares ISO timestamps **as strings** while `git`
emits mixed offsets (both `-05:00` and `-04:00` appear in this file's history) and transcripts end
in `Z`. Correcting D1 alone: R² 0.0513 → **0.6854**. D2 alone: → 0.0790. Both: → **0.8083**. The
tool is DISTRIBUTED, so neither is fixed here — raised as **BL-38**.

**Verified, not assumed.** `--selftest` 13/13 PASS. `bin/sync . --dry-run` reports
`.context-budget.json: present (seed; left as-is)` — the calibration is proved safe from re-sync
against *this* repo, not inferred from the general seed rule. `bin/tests.sh` unchanged from the
pre-change baseline. `.context-budget-history.jsonl` is created at root and deliberately tracked
(the growth run must survive a fresh clone); `.gitignore` gains a note saying so, mirroring the one
`dashboard_history.jsonl` already carries.

**Half (b) is deliberately NOT taken** — adding a `BACKLOG.md` entry to the *distributed* seed ships
upstream and needs the operator's go-ahead. It is now arguable from a measurement rather than a
guess, which was the whole point of doing (a) first.

### 2026-08-15 · [ad hoc] BL-38 raised — two defects in the distributed `context_budget.py` make its `--calibrate` produce noise on any repo that has merged another lineage of its target

Found by running BL-37 half (a)'s calibration, above. Measured, not fixed (FM #17): the tool is
DISTRIBUTED, so the repair ships to every adopter and needs a go-ahead. Full statement, evidence and
the four-way fit that separates the two defects: `docs/planning/BACKLOG.md` §BL-38.

### 2026-08-15 · [ad hoc] S89 close-out — receipt written, self-score 8/10; see the `[BL-32]` entry below for the substantive work

**Model:** Claude Opus 5.
Phase 3A/3B/3D. Evaluated S88's handoff (**8/10** — its gotcha attached a *measured cost* to BL-32,
naming the file, the size and the session it had just consumed, which is the only reason the work
was selectable; its 228/1 suite baseline and its derived 1-commit/`HANDOFFS.md`-only merge shape both
reproduced exactly at Phase 0. Docked two for a causal claim in its own voice — *"no reduction step
reaches it, **because** `methodology_trim.py`'s `LEDGERS` table covers only
`CHANGELOG.md`/`HANDOFFS.md`"* — which points a successor at a distributed tool that could not have
done the job, when the reduction step was never missing: it is Phase 3F, skipped eleven times).
Receipt written to [`HANDOFFS.md`](HANDOFFS.md); its `next_steps` names the budget gap as a policy
question about live items rather than housekeeping, BL-37's go-ahead-free half (a) as the cheapest
follow-on, and re-derives the upstream merge shape rather than inheriting it. Every line number cited
in the receipt was re-checked after the last edit, which caught one that had shifted (`:925` → `:927`
for BL-37). Corrected in the same pass: `date_of_record` was cited as
`starter-kit/methodology_trim.py:145`/`:150`/`:158` and is actually `:136` (required positional
parameter), `:144`, `:168`, `:194` — fixed in both the `[BL-32]` entry and BL-32 itself before commit.
`bin/check-handoff --all --allow-pending` OK (6 receipts).

### 2026-08-15 · [ad hoc] Framework Learning #26 appended — archiving everything finished can still leave a file over its ceiling, because the excess may be the live work

**Model:** Claude Opus 5.
Appended to [`starter-kit/FRAMEWORK_LEARNINGS.md`](starter-kit/FRAMEWORK_LEARNINGS.md) at Phase 3C —
**DISTRIBUTED**, append-only, `#14` still reserved; the table is now 25 rows numbered 1–13, 15–26.
Generalised from the `[BL-32]` reduction below, where the diagnosis everyone held was correct and the
target was still unreachable: the protocol's own Phase 3F removal step had been skipped 11 times, and
recovering all of it recovered a third of the file without reaching the ceiling, because the *open*
items alone already exceeded it. The countermeasure costs one measurement and is available before the
work starts — **sum the part you are not permitted to remove and compare that to the ceiling first**;
if the untouchable remainder already exceeds it, say so at claim time and re-scope to "reduction plus
finding" rather than discovering it at close-out. Carries a related sub-trap from the same session: a
file cannot accurately state its own byte size, because writing the number in changes it — put the
figure in a neighbouring file and leave a re-derivation command behind. `bin/check-learnings` OK.

### 2026-08-15 · [ad hoc] BL-37 raised — this repo ships a size-ceiling gate to every adopter and has never configured it for itself

**Model:** Claude Opus 5.
Found while looking for `docs/planning/BACKLOG.md`'s **declared** ceiling during the reduction
above, and there isn't one, because this repo declares none at all. `bin/_manifest.py:54`/`:60`
distribute `starter-kit/context_budget.py` → adopter `context_budget.py` and
`starter-kit/context-budget.json` → adopter `.context-budget.json`; this repo's own root has no
`.context-budget.json`. Same shape as **BL-29** / upstream
[issue #59](https://github.com/KJ5HST/methodology/issues/59) — a tool right for every installed copy
and blind at home — but reached through *configuration* rather than path resolution, which is why
nothing catches it: `bin/tests.sh` has **13** rows proving the gate *installs* correctly and none
asserting it is *configured here*, and an unconfigured gate is silent, not red. Second half: the
shipped seed's `files` list covers `CLAUDE.md`, `SESSION_NOTES.md` and an optional `LEARNINGS.md`,
and has **no `BACKLOG.md` entry** — the file `SESSION_RUNNER.md` Phase 0 step 3 names as the
priorities fallback for any adopter without a repo. **Measured, not fixed (FM #17):** one half is
this repo's own root config, the other is a DISTRIBUTED seed change needing a go-ahead, and neither
is a reduction. Both options costed in the item; (a) is a precondition for arguing (b) from a
measurement instead of a guess.

### 2026-08-15 · [BL-32] `docs/planning/BACKLOG.md` reduced 137,440 → 91,857 B (−33.2%) — 11 closed items archived verbatim with an identity-keyed losslessness proof

**Model:** Claude Opus 5.
The measured local half of BL-32, operator-directed. `SESSION_RUNNER.md` Phase 3F requires removing
a completed item from `BACKLOG.md` in the same commit that closes it; **that step was skipped 11
times**, so a file whose stated job is open work only carried 45,288 B — a third of itself — of
finished work. S85's own self-critique had flagged this and it was never picked up. BL-8, BL-15,
BL-20's closed half, BL-24, BL-25, BL-27, BL-28, BL-29, BL-33, BL-34 and BL-35 moved **verbatim** to
[`docs/planning/BACKLOG-archive-2026-08-15.md`](docs/planning/BACKLOG-archive-2026-08-15.md), each
keeping a one-line pointer row carrying its *conclusion* (not just its title) in §Completed items.
The stacked superseded-STATUS preamble went 16,521 → 6,862 B; every live warning it carried was kept
(the six-of-six wrong-numbers caution and its named figures, BL-16's headingless-inside-BL-14
placement, BL-10's parked-branch block and its PR #64 authorization rule).

**Not a `methodology_trim.py` trim, and could not have been — this is a partial answer to BL-32's
own undecided (a)/(b)/(c).** Every `LedgerSpec` requires a `date_of_record` — a required
positional parameter of `LedgerSpec.__init__` (`starter-kit/methodology_trim.py:136`, stored at
`:144`, supplied by both shipped specs at `:168`/`:194`) — and freezes the oldest **by date**; a
backlog's reduction axis is **status**. Measured on the real file: BL-11 (2026-08-01) is open and
had to stay, BL-35 (2026-08-11) is fixed and had to go — a date-keyed trim inverts the correct
answer. That is the *"mis-zone a differently-shaped ledger"* failure the tool's own comment
(`:131-132`) exists to prevent, arriving as a hand-authored spec rather than a generic fallback.
Recorded in BL-32; it narrows the decision and does not make it.

**Losslessness is proved, and the proof was mutation-tested before its green was believed.**
[`BACKLOG-archive-2026-08-15.md.verify.sh`](docs/planning/BACKLOG-archive-2026-08-15.md.verify.sh)
re-extracts each item from `git show 201e84e:docs/planning/BACKLOG.md` and compares **byte-for-byte,
keyed on the item's identity (`BL-N`), never on its position** — deliberately not the shipped
`.verify.sh` design, whose positional `injected` flag is what makes four intact archives read FAIL
(BL-36). C1 identity set / C2 byte-exact bodies / C3 the move actually happened (no archived body
still in the live file) / C4 every item reachable from it. **7 mutants: 6 killed** (delete an item;
a same-length one-character edit inside a body — 7,417 B on both sides, so the check is comparing
bytes and not lengths; truncate an item; copy-instead-of-move; drop a pointer row; unname the
shard), **1 deliberate survivor** (reordering two items — correct, and it is the positive evidence
that the check is identity-keyed rather than positional). A control ran green unmutated, every
restore was `cmp`-verified, and a mutant that failed to apply reported as **MUTATION DID NOT APPLY**
rather than as a survival — one did, and was re-run against real text.

**The retained half was proved too, not assumed:** 14 of the 15 open items are byte-identical to
`201e84e`; the 15th, BL-36, differs by exactly the deliberate edit below.

**The budget was NOT reached, and the reason is the finding.** 137,440 → 91,857 B (1,548 → 1,004
lines) is −33.2%, still 1.40× the 65,536 B the ledgers are held to. With **every** closed item
archived and **before this session had written a word of its own into the file**, the 16 inherited
*open* items already totalled 68,195 B — 1.04× — so no amount of archiving finished work can reach a
ceiling here. (The final 72,920 B / 17 items includes this session's own BL-37 and its additions to
BL-32/BL-36; the 68,195 B figure is the one measured against the pre-addition state, so the
measurement does not include the measurer.)
The remaining excess **is the open work itself**, and closing the gap means compacting live items:
a separate decision, not deferred housekeeping. Recorded in BL-36, whose stale `BL-27 above (:975)`
cross-reference — false in both halves once BL-27 moved — was repointed at the archive in the same
edit. One boundary was hand-checked rather than sliced: an orphaned S34 regression note about
BL-10's parked branch sat inside BL-8's heading span, belongs to neither, and was retained (moved
beside the BL-10 block it describes); the losslessness proof asserts that boundary marker exists
rather than assuming it.

Verified: `bin/tests.sh` 228 passed / 1 failed (Test 9's pre-existing github-source gap, unchanged
from S87/S88), `tools.test_methodology_dashboard` 300/300 (4 skipped), `tools.test_methodology_trim`
97/97, `bin/check-links` OK (88/22), `bin/check-learnings` OK (24 rows), `bin/check-handoff --all
--allow-pending` OK. No `bin/_manifest.py`-distributed file was touched; no outward-facing action
was taken.

### 2026-08-15 · [ad hoc] S88 close-out — receipt written, self-score 8/10; see the `[BL-36] ANSWERED` entry below for the substantive work

**Model:** Claude Opus 5.
Phase 3A/3B/3D. Evaluated S87's handoff (**7/10** — its per-shard failure text, its detached-worktree
proof that the four failures were pre-existing, and its "do not regenerate before answering" warning
were all load-bearing and correct; docked two points for naming a cause from a correlation without
running the two-command experiment that refutes it, and for a "Next session" framing whose binary —
*fault in the v1.1.1 scripts* or *fault in the archives* — omits the actual answer, and a third for
raising BL-36 into the same file that already contained its answer 471 lines above at BL-27, which
is mitigated but not excused by that file having no reduction step, i.e. BL-32). Self-assessed 8/10:
built an independent identity-keyed re-derivation rather than letting the suspect machinery answer
the question about itself, mutation-proved the detector before believing its zero, and caught that
BL-36's central claim was a confound — then constructed the missing 2×2 cells instead of arguing
them, which inverted the conclusion. Held back for nearly settling that same question by *reading*
v1.1.3's source comment rather than running it (the exact error Learning #25 names, one level up),
for a HEAD reachability sweep that is identity-only rather than content-hashed, and for leaving the
audit's central instrument in a scratchpad instead of shipping it with the claim it supports.

**Front-matter receipt count corrected 4 → 5** in `HANDOFFS.md`, the unguarded count its own front
matter warns drifts on every prepend. Its stale archive-trigger sentence (`:13`, "approaches ~1,200
lines" — a level the live `CHANGELOG.md` front matter already documents as wrong) was left untouched:
out of scope for this deliverable, still one line to fix, still open.

### 2026-08-15 · [ad hoc] Framework Learning #25 appended — a total correlation can still be a confound; run the off-diagonal cell

**Model:** Claude Opus 5.
Phase 3C, from the BL-36 audit below. The transferable half is not "the archives were fine" but the
method that showed it: when a defect report names a cause from a correlation that holds across every
artifact in existence, ask what else is perfectly collinear with it, then *construct* the missing
cell rather than reading the evidence harder. Here that was two `sed` substitutions and two runs, and
it inverted the conclusion — the obvious repair (regenerate under the fixed version) provably would
not have worked. Companion half: a failing proof is evidence about the proof until its claim is
re-derived by machinery it does not share, and that re-derivation must be mutation-proved able to
fail before its zero is believed (Learning #16). Appended at the end of the table, `#14` still
reserved; `bin/check-learnings` OK (24 rows, all citations resolve), `bin/check-links` OK (88/22) —
the row cites artifacts in backticks and adds no repo-relative link, since this file is distributed
and such a link would not resolve in an adopter tree.

### 2026-08-15 · [BL-36] ANSWERED — the four failing archive proofs are not evidence of loss; the archives are intact and the fault is in the proofs

**Model:** Claude Opus 5.
One audit, no repair (FM #17 — the repair touches a distributed tool and is its own session).
Report: `docs/audits/2026-08-15-bl36-archive-losslessness.md`. Coverage 9 of 9 archives, 6 of 6
proofs, 6 of 6 trim commits.

**No records were lost.** Re-derived independently — a parser keyed on record *identity* (heading,
or `session|date`) rather than the shipped proof's *position* — giving **0 records missing** across
all six trims and **0 of 228** historical identities unreachable at HEAD across live + all 9
archives. All six trimmer-declared counts (10, 70, 68, 16, 30, 25) reproduce exactly, which is
corroboration from a different program at a different time. The detector was mutation-proved able to
fail *before* its zero was believed (Learning #16): a deleted shard record → 1 missing, an altered
one → 1 changed, a 5-record truncation → 5 missing, silent on the unmutated artifact, each mutant
asserting that it actually applied.

**Root cause: `injected = 1 if trims_the_ledger else 0`** (`starter-kit/methodology_trim.py:1715`,
`:1736`) is a 0/1 flag meaning *"does the trim write its own ledger entry"*, never a count of what
the trim commit added. The generated proof's positional identity therefore breaks by construction on
any trim bundled with other same-ledger edits — two extra records (`73≠72`), three (`77≠75`), or a
frontier receipt finalized `pending → complete` inside the trim commit (`record [0]`).

**BL-36's version correlation was a confound, and catching it changed the repair.** All four failing
shards came from *bundled* trim commits and both passing ones from *standalone* trims, so generator
version and commit shape are collinear across the shipped six. The off-diagonal cells were executed,
not argued: **v1.1.3 logic fails all four bundled trims with identical text** (plus the BL-27 `NOTE:`
on the two `HANDOFFS` cases), and **v1.1.1 logic passes the standalone `CHANGELOG` trim**. So two
independent defects had been fused into one correlation — **A: bundling**, present in every version,
causal, and deliberately retained as a loud FAIL by BL-27's own fix 2; **B: the regenerated
front-matter count line**, genuinely fixed v1.1.1 → v1.1.3. Consequence: **regenerating the four
proofs would not fix them**, which is measured rather than predicted.

**Four minor findings.** BL-27's explanatory `NOTE` is gated on `bad == [0]`, so it never fires for a
bundled `CHANGELOG` trim — the busier ledger's likeliest bundling still fails mute. 3 of 9 archives
predate the trimmer and ship no proof at all. `CHANGELOG-through-v3.6.md` is the one shard not
byte-frozen since its creating commit (S31 corrected its front matter; all 50 dated records verified
byte-identical). And the answer already existed: **BL-27** (`docs/planning/BACKLOG.md:975`) states
*"This is not evidence of historical data loss"* and predicts this exact re-raise — unfound because
that file is 1,518 lines / 134,759 B, 2.06× the budget its own ledgers are held to, with no
reduction step reaching it (**BL-32**, open). Nothing in `docs/archive/` was modified by this audit.

### 2026-08-15 · [ad hoc] S87 close-out — receipt written, self-score 8/10; see the two `Ledger trim` entries below for the substantive work

**Model:** Claude Opus 5.
Phase 3A/3B/3D. Evaluated S86's handoff (**8/10** — its `runtime_smoke` baseline of 228/229 with
Test 9 as the sole known failure is what let this session read a mid-run 227/2 as one new breakage
rather than noise; docked for closing with both mandated-read ledgers 2–4× over their declared
65,536 B budget without naming it, which is FM #28's own degradation sign, and for the FM #27 gap
backfilled here at Phase 0). Self-assessed 8/10: treated the trimmer's `P1_UNDOCUMENTED` refusal as
information rather than an obstacle, measured three cut options instead of arguing them, established
the `HANDOFFS.md` date-cut hazard by running it, and — after the suite went red immediately
following its own change — ran the pre-change tree in a detached worktree before claiming
responsibility, which is what separated one real self-inflicted breakage from four pre-existing
failures. Held back for nearly shipping a verification pass that checked only the two proofs this
session wrote (broadening it is the sole reason BL-36 exists), and for leaving BL-36's cause
excluded-but-unproven.

**This entry deliberately restores the convention that lapsed after S79.** A close-out receipt commit
is written after the ledger commit that would have to cite it, so it can never record itself; S80,
S81, S83, S84, S85 and S86 each left one unrecorded, and frontier-based reconcile can only ever see
the newest. Writing the close-out entry *with* the ledger commit — the S62–S79 shape — is one of the
two clean options (S82's bundled single commit is the other). The historical gap remains open and is
flagged in this session's `8a22608` backfill entry below.

### 2026-08-15 · [BL-36] Four of the six shipped `.verify.sh` losslessness proofs do not hold — raised, not fixed

**Model:** Claude Opus 5.
Found while re-running *every* archive verifier after this session's two trims, rather than only the
two it had just written. Four fail: both v1.1.1-generated `CHANGELOG` proofs (L1 not byte-identical;
L3 counts 73≠72 and 77≠75) and both v1.1.1-generated `HANDOFFS` proofs (L1/L2 plus record `[0]` not
byte-identical). The two this session generated with v1.1.3 pass.

**Not caused by this session — measured, not assumed.** All four fail identically in a detached
worktree at `8a22608` (S86's tip, before S87's first commit). The generator version correlates
perfectly, which points at the class BL-27/BL-28 fixed in v1.1.2/v1.1.3, but the entry asserts no
cause: the competing *"a later trim invalidated an older proof"* explanation is unlikely on
inspection — each script freezes its derivation at its own trim commit via `TRIM_SHA` and three
`git show` reads, so it is not a function of `HEAD` — and unlikely is not disproved.

**Deliberately not fixed here** (FM #17): the repair depends on an answer this session did not have
budget to establish — whether the four archives' content is genuinely intact and only the proofs are
stale, or whether records were actually lost. Those are different repairs, and regenerating the
scripts first would make a passing proof over lost content, destroying the only evidence. Full item,
reproduction command and next-session instruction: `docs/planning/BACKLOG.md` **BL-36**.

### 2026-08-15 · [ad hoc] Framework Learning #24 appended — a check keyed on the live file has a population the protocol's own reduction step can move

**Model:** Claude Opus 5.
Phase 3C. Appended row **24** to [`starter-kit/FRAMEWORK_LEARNINGS.md`](starter-kit/FRAMEWORK_LEARNINGS.md) (append-only; `#14` stays reserved, so the
table now runs 1–13, 15–24 and `bin/check-learnings` reports 23 rows, contiguous, all citations
resolving). The learning generalizes this session's own Test 29 breakage: FM #28 makes archiving a
*routine, mandated* act, which silently makes every check keyed on a live file conditional on where
its population currently lives — and such a check's empty state surfaces as "failed", not as
"nothing to check". Carries the repair (define the population as the whole ledger, live + archives)
and the constraint on it (prove the widened arm can actually fail, or it is Learning #16's tautology
in a new place). Corpus re-grepped for stale set-size claims per Learning #7: none — no document
hardcodes a learnings count, and `bin/check-learnings` derives contiguity dynamically.

### 2026-08-15 · [ad hoc] `bin/tests.sh` Test 29 now reads the archives, not only the live `CHANGELOG.md`

**Model:** Claude Opus 5.
Fixes a test the same session's own archive turned red — found by running the suite, not predicted.

- **The defect.** Test 29's budget check keyed on `CHANGELOG.md` alone, and its pass condition is
  `RECON_COUNT > 0 && RECON_VIOLATIONS == 0`. The trim above moved all **10** remaining
  `Reconcile-on-read` entries into `docs/archive/CHANGELOG-through-2026-08-11.md`, so the live count
  fell to **0** and the test failed with an *empty* violation list — reporting
  `budget violated -- ` with nothing after the dash. Nothing had eroded; the population had moved.
- **Not a new lesson.** This is the blind spot `CHANGELOG.md`'s own source-tag audit already fixed
  for itself ("after the split it would have stopped counting the archived entries at all"), and the
  same *"found nothing" vs. "could not read this"* conflation `methodology_trim.py`'s
  `classify_empty` was widened for (UAT F1). Test 29 had the identical shape and had simply never
  been trimmed past before.
- **Fix.** The check now reads `CHANGELOG.md` **plus** `docs/archive/CHANGELOG-*.md`; violation
  messages carry the shard basename. The population is the whole ledger — which is where the norm
  has to hold — not whichever shard happens to be live today. **43** entries across 4 files, 0
  violations. The pass message no longer says "live", which had become false.
- **The archive arm is a real guard, proved rather than assumed.** Appending a synthetic 20-line
  discharge entry to an *archive* shard on a scratch copy moves the check `43/0 violations` →
  `44/1 violation`. Without that, the widened arm could have inflated the count while being
  incapable of ever failing. The pre-existing scratch-copy RED proof (`bin/tests.sh:1786`) is
  unchanged and still passes.
- **Verified:** `bash bin/tests.sh` **228 passed, 1 failed** — back to the S86 baseline exactly, the
  sole failure being Test 9's pre-existing, unrelated github-source gap.

### 2026-08-15 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-08-11.md` (25 record(s), 247,188 B → 32,649 B)

**Written by:** `methodology_trim.py` v1.1.3 — a tool action, not a session's judgment.
Moved the oldest **25** record(s) (2026-08-02 → 2026-08-11) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-08-11.md`](docs/archive/HANDOFFS-through-2026-08-11.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-08-11.md.verify.sh`](docs/archive/HANDOFFS-through-2026-08-11.md.verify.sh)
rather than trusting a digest printed here. Live file 247,188 B → 32,649 B (−86.8%).

### 2026-08-15 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-08-11.md` (68 record(s), 122,600 B → 25,165 B)

**Written by:** `methodology_trim.py` v1.1.3 — a tool action, not a session's judgment.
Moved the oldest **68** record(s) (2026-08-02 → 2026-08-11) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-08-11.md`](docs/archive/CHANGELOG-through-2026-08-11.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-08-11.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-11.md.verify.sh)
rather than trusting a digest printed here. Live file 122,600 B → 25,165 B (−79.5%).

### 2026-08-15 · [ad hoc] S87 claim commit `4825586` recorded — the trimmer's P1 guard requires an empty undocumented set

**Model:** Claude Opus 5.
Records this session's own Phase 1B claim (`4825586`, the `status: pending` S87 receipt). Written
**before** Phase 3F rather than at it, because `methodology_trim.py`'s `check_P1` refused both
planned trims while the undocumented set was non-empty:

> `[P1_UNDOCUMENTED]` the undocumented set is non-empty (1 commit(s) since the ledger frontier
> `11b44dc`). A trim commit advances that frontier and would hide them PERMANENTLY. Reconcile
> first, then trim.

The refusal is correct and was **not** worked around: a trim rewrites `CHANGELOG.md`, which advances
the Phase 0 frontier past any commit never recorded, so the claim commit would have become
permanently invisible to reconcile-on-read. `--force` would not have applied anyway — it is scoped
to the SRF-RED refusal, not this one.

**The interaction is worth naming for the next session that trims:** Phase 1B mandates a claim
commit, and that commit is itself an unrecorded action until Phase 3F — so *any* session that claims
correctly and then trims will hit `P1_UNDOCUMENTED`. The order that works is claim → record the
claim → trim, not claim → trim. Recorded as an observation, not a defect: the guard is doing
precisely its job, and the tool writes its own ledger entry per trim (`build_ledger_entry`,
`starter-kit/methodology_trim.py:980`), asserted afterwards by `check_P1a`.

### 2026-08-15 · [ad hoc] Backfilled (reconcile-on-read): undocumented commit `8a22608` — S86's own close-out receipt commit

**Model:** Claude Opus 5.
Phase 0 step 6 of the next session. Frontier `git log -1 --format=%H -- CHANGELOG.md` = `f8f32ea`
(S86's ledger commit); `git rev-list --count --no-merges f8f32ea..HEAD` = **1** — `8a22608`,
`docs(handoffs): S86 close-out`, which wrote S86's `HANDOFFS.md` receipt and nothing else. It is an
action this repository took and never logged (FM #27), so it is recorded here rather than left to
`git log`. `HANDOFFS.md` needed no parallel reconcile: its own frontier **is** `8a22608`, nothing
follows it, and the receipt it carries is `status: complete` with `commit: f8f32ea` already filled —
so the `commit: pending` chicken-egg shape discharged 41 times through S69 does not apply here.

**The gap is structural, and wider than the one commit this frontier can see.** A close-out receipt
commit is written *after* the ledger commit it would have to cite, so it can never record itself;
the only two clean shapes are S82's (`62168e6` — ledger and receipt in one commit) or S62–S79's
(a pre-written `[ad hoc] S<N> close-out — receipt written, self-score …` entry riding the ledger
commit, 15 of them in this file). That convention lapsed after S79: **S80 (`ca1261e`), S81
(`0a5b723`), S83 (`bb2c8af`), S84 (`b4780ec`), S85 (`d36a61e`) and S86 (`8a22608`) each left a
close-out commit with no ledger entry** — measured, not inferred (`grep -cE '^### .*S<N> close-out'`
returns 0 for each). Frontier-based reconcile structurally cannot reach the first five: each
session's own ledger commit moves the frontier past its predecessor's close-out commit, so only the
newest is ever visible. Recorded as a finding for the operator; **not** fixed here — a backfill of
five historical commits, or a change to the close-out convention, is a deliverable that needs its
own session and its own go-ahead (FM #17).

### 2026-08-12 · [BL-34] Local `main` synced with `upstream/main` (v3.7 release + issue #67 fix) — the 4-file conflict resolved

**Model:** Claude Sonnet 5.
Operator-directed: sync local `main` with `upstream/main` now, resolving BL-34's 4-file conflict
(`[BL-34]` entry above, S85). Fetching first showed the conflict had grown past what S85 scoped —
upstream had moved from `5c59f0b` to `dcb6fc6`, three commits further: PR #73 (issue #67's own
independent stale-copy fix) and PR #74 (the v3.7 release itself). Re-derived the real shape rather
than trusting the stale snapshot (Learning #13) and resolved the full scope: `git merge
upstream/main --no-commit --no-ff`, 6 conflicting files, no strategy shortcut, real 3-way merge
`aa378ab`.

- **`CLAUDE.md` + `docs/RELEASE_HISTORY.md`:** kept this fork's own history extraction (BL-9 L3)
  over upstream's reintroduced inline version list; appended upstream's new v3.7 entry to
  `RELEASE_HISTORY.md` with a fork note — every functional item it bundles had already reached
  this fork independently before the tag (issue #65's structural tests + FM #28 via S83's earlier
  merge; BL-34's R/Quarto/RMarkdown fix; this fork's own S62 fix for issue #67), so the entry
  records the upstream release as a fact, not new functional content landing here.
- **`CHANGELOG.md`:** upstream's newer-dated entries (the v3.7 release narration, the issue #67
  fix) placed above this fork's own 2026-08-11 entries. Dropped one orphaned duplicate — upstream's
  own narration of PR #71 (`_FRAMEWORK_FILE_SIGNATURES`), the same event this fork's existing
  `[BL-31]` entries already cover from S83's earlier merge, which kept this fork's own
  `_FRAMEWORK_INSTALLED_CONTENT` design over that same PR's dict-shaped one.
- **`tools/methodology_dashboard.py` + `starter-kit/` twin (7 conflicts):** kept this fork's own
  BL-34 comments and `DASHBOARD_VERSION` (`2.15.2`) throughout — functionally identical to
  upstream's leaner, fork-vocabulary-free wording (written for the upstream-targeted branch, not
  this file). For issue #67's stale-copy remedy, kept this fork's own `--sync [DIR]` single-project
  scoping design over upstream's `cp`-based one: more general (reuses the existing sync mechanism
  rather than bypassing it), and already covered by roughly 15 existing Row 13/14 tests
  (`test_sync_accepts_a_single_target_directory`, `test_bare_dry_run_without_sync_errors_and_writes_
  nothing`, `test_sync_end_to_end_via_main_writes_only_the_target`, etc.) that upstream's simpler
  design has no equivalent for.
- **`tools/test_methodology_dashboard.py` (8 conflicts):** kept BL-34 comment flavor throughout;
  adopted upstream's new `test_rmd_analysis_repo_flips_doc_only_and_softens_the_test_risk` (genuinely
  new — it only ever existed on the separate PR #72 branch, never merged into this fork's own
  `main`). Dropped upstream's whole `TestCliRemedyProportionality` class as redundant with this
  fork's own more thorough `--sync`-target coverage — one of its assertions
  (`self.assertIn("cp ", err, ...)`) would have failed against this fork's correct, already-tested
  `--sync [DIR]` design, catching a difference in implementation shape, not a real defect.
- **`README.md` (auto-merged cleanly, no conflict):** its new "What's New in v3.7" section, inherited
  verbatim from upstream, described the `cp`-based stale-copy remedy — inaccurate against what this
  fork actually ships. Corrected the one bullet to describe the `--sync [DIR]` design instead.
- **`HANDOFFS.md` (3 conflicts):** upstream's **S11** (issue #67's fix) merged in. Dated
  2026-08-12 — later than this session's own 2026-08-11 entries — but placed BELOW this session's
  own **S86** stub rather than above it: `check-handoff --allow-pending` exempts only the file's
  literal newest block, so a later-dated but still-`pending` receipt sitting above an in-flight one
  breaks the exemption (found live — two stacked pending stubs, both flagged red even with
  `--allow-pending`). Upstream's own **S12** (the v3.6→v3.7 release-cutting session, still
  `status: pending` at `upstream/main`'s own tip) is deliberately **not** recorded here — a pending
  stub is a live claim in progress, not settled history, and belongs in this ledger once upstream
  completes or abandons it; a future sync should re-check for that rather than assume this one
  reconciled it. Receipt count corrected 24 → 28 (was already stale before this merge, per the
  section's own "unguarded" warning).

**Verified:** `python3 -m unittest tools.test_methodology_dashboard` 300/300; `bash bin/tests.sh`
228/229 (Test 9's pre-existing, unrelated github-source gap aside); `bin/check-links` OK (88/22);
`bin/check-learnings` OK (22 rows, 0 findings); `bin/check-handoff --all --allow-pending` OK (28
receipts, fences balanced, no duplicate session+date); twins byte-identical throughout.

### 2026-08-12 · [ad hoc] Released v3.7 — the artifacts Phase 0 mandates reading now have ceilings

- **Change:** release narration commit on `release/v3.7` — `README.md` §What's New in v3.7 (folding
  in the stale "Since v3.6 (unreleased)" section), `CLAUDE.md` §Versioning entry, and the
  "Current version" line 3.6 → 3.7. Cite-don't-restate: the full narrative lives in
  [`CLAUDE.md` §Versioning "v3.7"](CLAUDE.md#versioning); this entry is the action record.
- **Scope:** 38 commits and 13 ledger entries since `v3.6` (`d7a482a`). **Minor**, not patch,
  because the framework gained a failure mode (**#28**, count 27 → 28 — the first since v3.1) and a
  new distributed tool (`starter-kit/context_budget.py`, TRACKED, with a SEED config). **Not major**
  because no principle, phase, gate, or workstream changed. Learnings 12 → 13; `DASHBOARD_VERSION`
  2.10.2 → 2.10.6 across four separate fixes; `bin/tests.sh` 84 → 114; unit suite 197 → 211.
- **The "unreleased" README section was stale and is why this was worth catching.** It still ended
  *"the failure-mode count stays 27"* — written before PR #66 appended FM #28, and true when
  written. A section that describes itself as pending release is exactly the text nobody re-reads;
  it is Learning #7's cross-reference problem applied to the release notes themselves.
- **Tag and Release are recorded in a follow-up entry, not predicted here.** A tag SHA that does not
  exist yet is a forward-looking claim, and Learning #13 says to compute those rather than assert
  them — so the tag/Release facts are appended once the action has actually happened.

### 2026-08-12 · [issue #67] The stale-copy warning now names a remedy proportionate to the finding, and bare `--dry-run` no longer writes

- **Change:** `tools/methodology_dashboard.py` (+ `starter-kit/` twin, kept byte-identical) and
  `tools/test_methodology_dashboard.py`. `DASHBOARD_VERSION` 2.10.5 → 2.10.6. Closes
  [issue #67](https://github.com/KJ5HST/methodology/issues/67).
- **Defect 1 — a disproportionate remedy.** `check_stale_version()` answered "this one copy is
  old" with `Re-sync: python3 <canonical> --sync`. But `--sync` is scoped from the **canonical's
  own location**, not the working directory, so it rewrites every discovered sibling — measured at
  26 files across 25 repos, including 7 creates in repos that do not gitignore the path and 1
  where the file is git-tracked. An adopter following a one-line instruction verbatim dirtied
  eight unrelated repositories. The warning now leads with the safe per-project action
  (`cp <canonical> <this copy>`) and offers the portfolio path only as `--sync --dry-run`, with
  its scope stated. **Why it matters beyond tidiness:** a remedy nobody can safely run is one
  mechanism behind an *ignored* warning — in one adopter this line rode ~28 consecutive handoffs
  unacted-on. The measurement was never missing; the actionable remedy was.
- **Defect 2 — a flag named `--dry-run` that writes.** It was consulted only inside the `--sync`
  branch, so bare `--dry-run` fell through to a full scan and wrote `dashboard.html` *and*
  appended to `dashboard_history.jsonl`. It is now an error (exit 2) that writes nothing.
  Refusing rather than silently no-opping is deliberate: a silent no-op leaves the caller unable
  to distinguish "nothing to do" from "flag ignored" — the same unreadable-signal class as
  defect 1.
- **Tests:** new `TestCliRemedyProportionality` (3 cases, unit suite 208 → 211). Both defect
  tests were driven RED against the pre-fix scanner and the failing run read, not assumed;
  the third is a presence control (a plain run must still write `dashboard.html`), without which
  a scanner that refused *every* invocation would pass and look fixed.
- **Scope deliberately not taken:** the issue also suggests `--sync-self` and a `--yes` gate on
  `--sync`. Both change the CLI contract rather than fix a defect, so they are left for a
  separate deliverable; the `cp` line already gives the per-project remedy with no new surface.
- **Distribution:** the scanner is `bin/_manifest.py`-TRACKED, so adopters receive both fixes via
  `bin/sync`.

