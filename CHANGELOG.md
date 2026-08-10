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

---

## 2026-08

### 2026-08-10 · [ad hoc] Fix UAT F9's own instance: `dashboard_history.jsonl` tracked + documented, not left unmanaged

**Model:** Claude Sonnet 5.
Operator-directed. UAT F9 (`docs/planning/uat-2026-08-04-six-adopters.md:346`) found `dashboard_history.jsonl`
undocumented anywhere `dashboard.html` is, and reproduced the resulting inconsistency in this
canonical repo itself: an untracked, unignored file at the repo root, left in place at the time
(disclosed then, not fixed). Two real adopters (`mts-system`, `wsfct`) have since independently
converged on the same resolution and the follow-up UAT audit confirmed both: **track** the file
rather than gitignore it, since — unlike `dashboard.html`, fully regenerated every run —
`dashboard_history.jsonl` only appends, so it is the sole place the health-trend history lives.
Put to the operator via `AskUserQuestion` (track-and-document vs. gitignore, matching `dashboard.html`);
operator chose track-and-document. `git add`ed the file (2 existing snapshots, 2026-08-04/2026-08-09).
Added a `.gitignore` comment explaining the deliberate asymmetry, worded to match `mts-system`'s own
`.gitignore` comment for the identical fix (ecosystem consistency). Documented both artifacts'
opposite treatment in `starter-kit/BOOTSTRAP.md` at both existing `dashboard.html`/`.gitignore`
mentions (Step 2, Step 9 Per-Project Setup) — the "nowhere documented" gap F9 named as root cause.
Full `bin/tests.sh` 185/186 before and after (Test 9's expected upstream-404, unaffected); `bin/check-links`
OK (88/22). No BL-N item existed for this — it was tracked only via UAT-report cross-references and
`HANDOFFS.md` `next_steps` carryover since S63; recorded here as `[ad hoc]` accordingly.

### 2026-08-10 · [ad hoc] Reconcile-on-read: S68's `commit:` field → `8a5d4b0` — 40th discharge, found at Phase 0 orientation

**Model:** Claude Sonnet 5.
Reconciled `8a5d4b0` (S68's own close-out commit) — 40th discharge, same mechanical chicken-egg
shape as the prior 39: S68's receipt was written and committed before its own commit sha could be
known, so its `commit:` field was left `pending` in the tree at the frontier this session's Phase 0
found (`git log -1 --format=%H -- HANDOFFS.md` = `8a5d4b0`, no commits after it). No other
undocumented commits exist between the S68 frontier and `HEAD` — `git log --oneline
8a5d4b0..HEAD` is empty, so this is the only gap. `bin/tests.sh` confirmed 185/186 both before and
after this fix (Test 9's expected upstream-404 baseline, unaffected).

### 2026-08-10 · [ad hoc] Reconcile-on-read: S67's `commit:` field → `fb6e3cd` — 39th discharge, found via `bin/tests.sh` after this session's own substantive work

**Model:** Claude Sonnet 5.
Reconciled `fb6e3cd` (S67's own close-out commit) — 39th discharge, same mechanical shape as the
prior 38: prepending this session's own S68 claim stub moved S67 out of "newest," so its still-
`pending` `commit:` field started failing `bin/check-handoff`'s `L1` check inside `bin/tests.sh`
(184 passed, 2 failed — the other being Test 9's expected upstream-404 baseline). **Departs from the
S62–S66 established order** the same way S66 itself did: claimed S68 before checking S67's field,
and only ran the full suite (surfacing the gap) after the BL-28 fix and its tests were already
written — later in the session than S66's own slip, not earlier. Fixed here rather than left for a
future session; disclosed in this session's own `HANDOFFS.md` gotchas, not hidden.

### 2026-08-10 · [BL-28] `.verify.sh`'s L2 "missing front-matter line" check: substring containment → exact-line-set membership

**Model:** Claude Sonnet 5.
Fixed `starter-kit/methodology_trim.py`'s `VERIFY_TEMPLATE` (the generated `.verify.sh`, sole
canonical copy — no `tools/` twin): the "missing" check tested `ln not in afront`, substring
containment against the whole front-matter TEXT, so an append-style edit that kept the original line
as a literal prefix of a new, longer line evaded detection — a real change to the line read as "no
loss." Now builds `afront_lines = set(afront.splitlines())` once and tests exact membership in that
set; `field_reversible()`'s own separate, correct carve-out for the declared regenerated fields is
untouched. RED-first: reproduced the exact BL-28 tamper (`"# Handoff Receipts"` → `"# Handoff
Receipts EDITED"`) in a new `TestVerifyShAppendTamperEvadesSubstringCheck` class
(`tools/test_methodology_trim.py`) — confirmed no `FAIL:` in the script's output against unpatched
code, `FAIL: L2 FRONT MATTER` after the fix; a narrowed control re-confirms the regenerated-count
field still passes both before and after, so the fix does not turn exact-line-set comparison into a
blanket new false positive. Trimmer suite 95 → 97, all green; full `bin/tests.sh` 184/186 (2
pre-existing/unrelated: Test 9's expected upstream-404, and the S67 reconcile fixed in the entry
immediately above). `TRIM_VERSION` 1.1.2 → 1.1.3 (patch — no new finding code or exit status on the
tool's own CLI, a correctness fix to generated output, same class as 1.1.2/BL-27).
`docs/planning/BACKLOG.md` BL-28 closed in place with a closure paragraph (BL-27 precedent), top
STATUS line updated to drop BL-28 from the open list.

### 2026-08-10 · [ad hoc] S67 close-out — receipt written, self-score 8/10; see the `[BL-26]` entry below for the substantive work

**Model:** Claude Sonnet 5.
`HANDOFFS.md`'s S67 stub overwritten in place to `status: complete` with all six Minimum Handoff
Requirements. No separate substantive action beyond the receipt itself and the reconcile entry
immediately below — the PR #66 work is described in the `[BL-26]` entry two below.

### 2026-08-10 · [ad hoc] Reconcile-on-read: S66's `commit:` field → `971377c` — 38th discharge, found at this session's own close-out, not at Phase 0

**Model:** Claude Sonnet 5.
Reconciled `971377c` (S66's own close-out commit, and the tree's `HEAD` at this session's Phase 0) —
38th discharge, same mechanical shape as the prior 37. **Departs from the S62–S66 established
order**, which reconciles the predecessor's `pending` field *before* claiming: this session claimed
S67 first and only found the gap while finalizing its own receipt. `git rev-list --count --no-merges
971377c..e69a7a5` confirms no ghost session — the sole intervening commit is this session's own S67
claim stub. Disclosed as a process slip in `HANDOFFS.md`'s S67 gotchas, not hidden.

### 2026-08-10 · [BL-26] PR #66: proposed fix for both collisions, posted as three review comments

**Model:** Claude Sonnet 5.
Operator-directed. Re-verified both collisions BL-26 (S56) originally found, live against the PR's
current head (`df6a9918`, unchanged since 2026-08-08) and this fork's current state, before drafting
anything: `install_hook()` still writes unconditionally to `<git-dir>/hooks/pre-commit`
(`starter-kit/context_budget.py:472-490`), ignoring this repo's `core.hooksPath = .githooks`;
`bin/check-handoff`'s new `validate_ledger()` still keys its duplicate-session check on bare
`session:` (`:204-212`), and the real ledger still reproduces the false-positive shape exactly
(`S3`/`S5`/`S7`/`S8` each appear twice across `HANDOFFS.md` + both archives, by this fork's own
documented dual-sequence design). Drafted a concrete fix for each — check `core.hooksPath` first in
`install_hook()`, fall back to `<git-dir>/hooks` only when unset; key the duplicate check on
`(session, date)` instead of `session` alone, matching the invariant `HANDOFFS.md` itself states.
Posted three review comments to upstream PR #66 — one general summary plus two inline `suggestion`
blocks, each anchored to the exact file/line/commit the defect reproduces at — via `gh pr comment`
and `gh api repos/KJ5HST/methodology/pulls/66/comments`:
[general](https://github.com/KJ5HST/methodology/pull/66#issuecomment-5246274123),
[hook-install](https://github.com/KJ5HST/methodology/pull/66#discussion_r3753541194),
[duplicate-check](https://github.com/KJ5HST/methodology/pull/66#discussion_r3753543217). Folded the
same proposal into `docs/planning/BACKLOG.md` BL-26 as a new dated, appended paragraph (original
entry text untouched, matching the BL-24/BL-25/BL-27 precedent). This is a comment, not a commit — no
code changed in this repo or on the PR branch; the suggestions are the PR author's to accept, reject,
or ignore. `bin/check-links` OK (88/22, unaffected). Answered the operator's question of whether a
new session is needed to take PR #66 further: yes, if and when the maintainer responds — this
session's scope was the proposal and the comment, not implementation (FM #17).

### 2026-08-10 · [ad hoc] S66 close-out — receipt written, self-score 8/10; see the Learning #22 entry below for the substantive work

**Model:** Claude Sonnet 5.
`HANDOFFS.md`'s S66 stub overwritten in place to `status: complete` with all six Minimum Handoff
Requirements. No separate substantive action beyond the receipt itself — the Learning addition is
described in the sibling entry immediately below.

### 2026-08-10 · [ad hoc] Add Framework Learning #22 — a completed backlog item's own text can be load-bearing for a sibling item's cross-reference

**Model:** Claude Sonnet 5.
Appended row 22 to `starter-kit/FRAMEWORK_LEARNINGS.md` (append-only, existing rows untouched —
verified single-hunk, 1 insertion). Distills a pattern found this session doing cross-repo adopter
`bin/sync`/ledger-reconcile/`BACKLOG.md`-hygiene maintenance in two sibling repos (wsfct,
nprcgenekeepr, both ad hoc, not sessions in either adopter's own sequence): Phase 3F's "remove a
completed backlog item in the same commit" assumes each item is independently deletable, and both
adopters' `BACKLOG.md` files falsified that — items cross-referenced each other by relative
position ("the item above", "immediately below") or by quoted title, and a naive
marker-grep-and-delete pass would have silently orphaned a still-open item's own reference. wsfct
kept 2 of 15 flagged rows, nprcgenekeepr 5 of 9 (a three-item chain plus one member quoted by name
from outside it), both found only by grepping the whole file before deleting anything. Drafted,
reviewed, and shortened (~330 → ~230 words, no claim dropped) with the operator across three rounds
before being written in. `bin/check-links` OK (88/22, unaffected — no new cross-references added).
No adopter impact — canonical-only until contributed upstream, which stays its own, separately
authorized action per this repo's own standing rule.

### 2026-08-10 · [ad hoc] Reconcile-on-read: S65's `commit:` field → `c43e7ee` — 37th discharge, found at Phase 0 orientation

**Model:** Claude Sonnet 5.
Reconciled `c43e7ee` (claim stub `d244dd0`) — 37th discharge, same mechanical shape as the prior 36:
S65's own close-out receipt necessarily named its `commit:` field `pending` at write time, because it
was written in the same commit whose sha it would name. `c43e7ee` is `HANDOFFS.md`'s current frontier
and `HEAD`, with `git rev-list --count --no-merges c43e7ee..HEAD` = `0` (no ghost session, no backfill
owed). Taken before this session's own Phase 1B claim.

### 2026-08-10 · [ad hoc] S65 close-out — receipt written, self-score 8/10; see the `[BL-27]`/`[ad hoc]` entries below for the substantive work

**Model:** Claude Sonnet 5.
`HANDOFFS.md`'s S65 stub overwritten in place to `status: complete` with all six Minimum Handoff
Requirements. No separate substantive action beyond the receipt itself — the fix and the BL-28
finding are described in the sibling entries immediately below.

### 2026-08-10 · [ad hoc] BL-28 raised: the generated `.verify.sh`'s "missing front-matter line" check is a substring test, not exact-line-set membership

**Model:** Claude Sonnet 5.
Found while building BL-27's own narrowed control test for the front-matter-regen fix: an
append-style edit (`"# Handoff Receipts"` → `"# Handoff Receipts EDITED"`) leaves the original text
intact as a literal substring of the new line, and the check (`ln not in afront`, a substring test
over the whole front-matter TEXT) reports no loss — reproduced live via the actual generated script.
Pre-existing, not introduced by this session's fix; BL-27's fix only exposed it by removing an
unrelated false positive that had been accidentally masking it. The INTERNAL `assert_L2` (used by
`--check`/`--write`) does not share this defect — it compares by exact residue equality, which an
append-style edit still fails correctly. Not fixed here (FM #17) — a change to the same canonical,
adopter-distributed tool, needing its own RED-first test. Full evidence: `docs/planning/BACKLOG.md`
BL-28.

### 2026-08-10 · [BL-27] S65 — fix the ledger trimmer's generated `.verify.sh`'s two false-positive triggers on `HANDOFFS.md`

**Model:** Claude Sonnet 5.
Fixed both findings raised at S64, in `VERIFY_TEMPLATE`/`build_verify`
(`starter-kit/methodology_trim.py` — the sole canonical copy, no `tools/` twin to mirror). (1) A new
`@@REGEN@@` template variable carries `spec.regenerated`'s declared field patterns (`repr()`'d,
since it is 0-or-more patterns) into the generated script; a `field_reversible()` helper excuses a
"missing" front-matter line only when a same-shaped partner line exists elsewhere in the new front
matter, identical everywhere outside the declared field's own span. (2) L1/L3 now share one
`rebuilt`/`bad`-index computation; when the only altered record is position 0 (the frontier), the
script still FAILs — loud, never silently exempted, because a real loss can have this exact shape —
but also prints a `NOTE:` naming the known bundled-commit pattern (this repo's own established
practice of finalizing a session's close-out receipt in the same commit as the archive write), so a
`FAIL` no longer reads as unqualified. RED-first: 4 new tests in a new
`TestVerifyShHandoffFalsePositives` class (`tools/test_methodology_trim.py`), against a new
`make_handoff_repo` fixture — the suite's first end-to-end `HANDOFFS.md` trim through the actual
subprocess and generated script, not just `assert_L2` in isolation. Both fix-tests confirmed RED
against unpatched code for the exact defects BL-27 named; both narrowed controls confirmed
already-green unpatched, proving the fix does not become a blanket permit. Suite 91 → 95, all
green; full `bin/tests.sh` unaffected (185/186, Test 9's expected upstream-404 only — unchanged
baseline). `TRIM_VERSION` 1.1.1 → 1.1.2 (patch — no new finding code or exit status on the tool's
own CLI; a correctness fix to what the tool WRITES). One real finding surfaced while building the
first control test, not fixed here: raised as BL-28 (sibling entry above). Full evidence:
`docs/planning/BACKLOG.md` BL-27 and BL-28.

### 2026-08-10 · [ad hoc] Reconcile-on-read: S64's `commit:` field → `a46f2f9` — 36th discharge, found at Phase 0 orientation

**Model:** Claude Sonnet 5.
Reconciled `a46f2f9` (claim stub `ede7cbb`) — 36th discharge, same mechanical shape as the prior 35:
S64's own close-out receipt necessarily named its `commit:` field `pending` at write time. `a46f2f9`
is the first commit (all refs) whose S64 block reads `status: complete`, confirmed via `git log
--all --full-history -- HANDOFFS.md`; it is also `HANDOFFS.md`'s current frontier and `HEAD`, with
`git rev-list --count --no-merges a46f2f9..HEAD` = `0` (no ghost session, no backfill owed). Taken
before this session's own Phase 1B claim.

### 2026-08-10 · [ad hoc] S64 close-out — receipt written, self-score 8/10; see the BL-27 and regression-fix entries below for the substantive work

**Model:** Claude Sonnet 5.
`HANDOFFS.md`'s S64 stub overwritten in place to `status: complete` with all six Minimum Handoff
Requirements. No separate substantive action beyond the receipt itself — the archive, the BL-27
finding, and the two collateral-regression fixes are described in the sibling entries immediately
below, landed in three separate commits.

### 2026-08-10 · [ad hoc] Fix two collateral regressions this session's own `HANDOFFS.md` archive caused in the test suite

**Model:** Claude Sonnet 5.
Same class as S63's own collateral-regression fix, different couplings. (1)
`tools/test_methodology_trim.py::test_a_declared_regenerated_field_is_permitted_and_confined` read
`HANDOFFS.md` directly off disk and probed with a hardcoded `{"retained": 3}` — this session's own
archive set the real live count to exactly `3`, making `old == new` and silencing the
`FRONTMATTER_FIELD_REGENERATED` assertion it exists to make; fixed by deriving the probe from the
live value (`int(old) + 1`) so it can never coincide again, in both this test and its sibling
`test_a_regenerated_field_does_not_license_an_edit_elsewhere`, which shared the same hardcoded
literal. (2) Four tests in `tools/test_methodology_dashboard.py::TestS38TrimTriggerRow` use this
repo's own live state as a real (non-synthetic) fixture and assert its trim trigger currently
fires; clearing `HANDOFFS.md`'s trigger (this session) made that precondition false — `CHANGELOG.md`'s
was already clear from S63, so neither ledger fires today. Fixed by converting the bare
`AssertionError` each already raised on a clear, self-documented fixture-precondition message into
an explicit `self.skipTest(...)` with the same message — the tests still exist to catch a broken
advisory and will run again once either ledger is genuinely over budget; force-passing them would
have hidden that, not fixed it. `python3 tools/test_methodology_trim.py` 91/91 (was 90/91);
`python3 tools/test_methodology_dashboard.py` 284/284, 4 skipped (was 280/284, 4 failed).

### 2026-08-10 · [ad hoc] BL-27 raised: the ledger trimmer's generated `.verify.sh` has two known false-positive triggers on `HANDOFFS.md`

**Model:** Claude Sonnet 5.
Found while independently re-running `docs/archive/HANDOFFS-through-2026-08-09.md.verify.sh` —
this session's own trim precedent (S61, S63) established that practice specifically to avoid
trusting the tool's write-time summary. (1) `HANDOFFS.md`'s regenerated receipt-count front-matter
field reads as `L2` data loss in the generated script, which has no equivalent to `assert_L2`'s
declared-field-reversal exception. (2) A same-commit close-out bundling (this repo's own
established practice) reads as `L1`/`L3` record alteration; reproduced against S61's own frozen
shard proof (`docs/archive/HANDOFFS-through-2026-08-02.md.verify.sh`, untouched since `c0e6944`) —
**not evidence of historical data loss**, confirmed by manual diff and by this repo's own
`tools/test_methodology_trim.py::test_L3_fixture_is_the_event_that_bundled_an_edit_with_the_move`,
which already names and accepts the same pattern from S23's original archive. Not fixed here
(FM #17) — both are changes to a canonical, adopter-distributed tool needing their own RED-first
tests. Full evidence: `docs/planning/BACKLOG.md` BL-27.

### 2026-08-10 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-08-09.md` (30 record(s), 406,941 B → 25,874 B)

**Written by:** `methodology_trim.py` v1.1.1 — a tool action, not a session's judgment.
Moved the oldest **30** record(s) (2026-08-03 → 2026-08-09) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-08-09.md`](docs/archive/HANDOFFS-through-2026-08-09.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-08-09.md.verify.sh`](docs/archive/HANDOFFS-through-2026-08-09.md.verify.sh)
rather than trusting a digest printed here. Live file 406,941 B → 25,874 B (−93.6%).

### 2026-08-10 · [ad hoc] Claim S64 — lossless trim of `HANDOFFS.md` (operator-directed)

**Model:** Claude Sonnet 5.
`HANDOFFS.md`'s S64 stub prepended (`status: pending`) — Phase 1B claim, no substantive work yet.
Commit `ede7cbb`.

### 2026-08-10 · [ad hoc] Reconcile-on-read: S63's `commit:` field → `072324b` — 35th discharge, found at Phase 0 orientation

**Model:** Claude Sonnet 5.
Reconciled `072324b` (claim stub `efe5ee0`) — 35th discharge, same mechanical shape as the prior 34:
S63's own close-out receipt necessarily named its `commit:` field `pending` at write time (the
standard chicken-egg — a session cannot know its own final commit sha before committing). `072324b`
is cited because that is the commit whose message states it "completes S63's HANDOFFS.md close-out
receipt (status: complete, self_score 8/10)" and whose diff matches the receipt as it currently
reads — the earlier `61b48a6` reached `status: complete` first but with content (`self_score: 7`,
one collateral regression) `072324b` itself revised. Found and fixed at this session's Phase 0
orientation, before any task was assigned, per the established reconcile-on-read convention.

### 2026-08-10 · [ad hoc] Fix `tools/test_methodology_trim.py`'s control assertion after the trim moved its target content

**Model:** Claude Sonnet 5.
`test_L2_fixture_loss_actually_happened_and_is_still_unrepaired`'s control checked only
`HEAD:CHANGELOG.md` for a phrase quoted inside S35's old close-out entry (dated 2026-08-03); the
2026-08-09 archive cut (entry immediately below) moved that entry into
`docs/archive/CHANGELOG-through-2026-08-09.md`, so the assertion started failing —
`bin/tests.sh` 184/186. The test's own docstring already documented the correct scope (the
design's D1 command greps `CHANGELOG.md docs/archive/` together); widened the assertion to match,
searching the live file plus all archive shards rather than the live file alone. `python3
tools/test_methodology_trim.py`: 91/91. `bin/tests.sh`: 185/186 (Test 9's expected upstream-404
only) — true baseline, confirmed a second time. Found on a post-commit-amend diligence re-run of
the full suite, not by a pre-trim sweep — see this session's own `HANDOFFS.md` gotcha (3).

### 2026-08-10 · [ad hoc] S63 close-out — receipt written, self-score 8/10; see the ledger-trim and reconcile entries below for the substantive work

**Model:** Claude Sonnet 5.
`HANDOFFS.md`'s S63 stub overwritten in place to `status: complete` with all six Minimum Handoff
Requirements. No separate substantive action beyond the receipt itself — the trim, the collateral
`commit:` reconcile, and the trimmer-test fix it triggered are described in the sibling entries
immediately below and above, all landed together in this same commit.

### 2026-08-10 · [ad hoc] Reconcile-on-read: S62's `commit:` field → `d7712ca` — 34th discharge, found via `bin/tests.sh`

**Model:** Claude Sonnet 5.
Reconciled `d7712ca` (claim stub `575a9ba`) — 34th discharge. Same mechanical shape as the 33rd:
prepending S63's own pending stub moved S62 out of "newest," so its still-`pending` `commit:` field
(the usual chicken-egg) started failing `bin/tests.sh`'s Test 25 (184/186, not the 185/186 baseline).
Found by running the full suite mid-session rather than immediately at claim — a gap against the
established S58→S59→S60→S61→S62 precedent of checking right after claiming.

### 2026-08-10 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-08-09.md` (70 record(s), 161,878 B → 15,002 B)

**Written by:** `methodology_trim.py` v1.1.1 — a tool action, not a session's judgment.
Moved the oldest **70** record(s) (2026-08-03 → 2026-08-09) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-08-09.md`](docs/archive/CHANGELOG-through-2026-08-09.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-08-09.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-09.md.verify.sh)
rather than trusting a digest printed here. Live file 161,878 B → 15,002 B (−90.7%).

### 2026-08-10 · [ad hoc] Claim S63 — lossless trim of `CHANGELOG.md` (operator-directed)

**Model:** Claude Sonnet 5.
`HANDOFFS.md`'s S63 stub prepended (`status: pending`) — Phase 1B claim, no substantive work yet.
Commit `efe5ee0`.

### 2026-08-10 · [ad hoc] S62 close-out — receipt written, self-score 8/10; see the `[issue #67]`/`[BL-26]` entries below for the substantive work

**Model:** Claude Sonnet 5.
`HANDOFFS.md`'s S62 stub overwritten in place to `status: complete` with all six Minimum Handoff
Requirements. No new substantive action in this commit beyond the receipt itself — the fix, its
ledger entry, and the BACKLOG.md update all landed in prior commits this session (`7d682fa`,
`f53f47c`), cited below.

### 2026-08-10 · [BL-26] S62 — issue #67 thread updated: IMPLEMENTED fork-side, PR #66 thread untouched

**Model:** Claude Sonnet 5.
`docs/planning/BACKLOG.md` BL-26 updated in place (not closed — this is the fork-side half only,
upstream issue #67 stays open and no PR was opened against `KJ5HST/methodology`; PR #66's own
collisions remain unaddressed and its thread is untouched). See the `[issue #67]` entry immediately
below for the implementation itself.

### 2026-08-10 · [issue #67] S62 — fork-side fix: scoped `--sync [DIR]`, `.gitignore`-aware `--force` gate, bare `--dry-run` now errors

**Model:** Claude Sonnet 5.
Implemented the ratified fork-side fix plan (`docs/planning/issue67-fork-side-fix-plan.md`, S57
proposed / S58 ratified) in full — all four fixes issue #67 names, in both
`tools/methodology_dashboard.py` and its `starter-kit/` twin (byte-identical, `diff -q` verified).
`check_stale_version()` now recommends a scoped `--sync <dir>` first; `sync_dashboards()` gained a
`target=` scope via a new order-independent `--sync [DIR]` form; a `.gitignore`-aware `--force` gate
now blocks silent overwrites of git-tracked or brand-new targets (computed before `dry_run`
branches, so `--dry-run` previews it honestly); a bare `--dry-run` is now `sys.exit(2)` instead of
a silent full scan-and-write. `DASHBOARD_VERSION` 2.13.0 → 2.14.0. 17 RED-first tests
(`TestIssue67ScopedSync`, 16 new + `test_dashboard_version` updated) — each confirmed failing
against pre-fix code before the fix landed, all green after; `bin/tests.sh` 185/186 (Test 9's
expected upstream 404, unchanged). Live-portfolio dry-run smoke test against this machine's real
13 targets confirmed the gate would have caught 11 of them previously writing unconditionally.
Fork-side only, per the plan's own §9 — no PR opened against `KJ5HST/methodology`.

### 2026-08-10 · [ad hoc] Reconcile-on-read: S61's `commit:` field → `c0e6944` — 33rd discharge, taken at Phase 0/claim

**Model:** Claude Sonnet 5.
Reconciled `c0e6944` (claim stub `6f62787`) — 33rd discharge. Surfaced by `bin/check-handoff`'s
positional exemption: prepending S62's own pending stub moved S61 out of "newest," so its
still-`pending` `commit:` field (the usual chicken-egg — the receipt ships in the commit whose sha
it would name) started failing `bin/tests.sh`. Reconciled before further work, per this repo's own
established S58→S59→S60→S61 precedent.

