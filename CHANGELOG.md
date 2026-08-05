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

### 2026-08-04 · [ad hoc] S44 — UAT F1: a grammar the trimmer cannot read is no longer reported as an empty file

**Model:** Claude Opus 5 (1M context).
Operator-chosen from a four-option menu at Phase 0 close; also S43's own ranked #1 in
[`docs/planning/uat-2026-08-04-six-adopters.md`](docs/planning/uat-2026-08-04-six-adopters.md) §6.
**Fork session `S44` is NOT plan §5 queue item `S44`** — queue S44 is the diff-scoped prohibition
plus pre-commit/CI wiring. The two axes coincided four sessions running (S38, S40, S42, S43) and
**diverge here**, which is why the axis is named at every claim.

- **The defect.** `starter-kit/methodology_trim.py` printed `[NO_RECORDS] … nothing to archive. (A
  freshly seeded ledger looks exactly like this, and must not be trimmed.)` **and exited 0** on
  `../model_project_constructor/CHANGELOG.md` (**597,717 B**, 130 dated entries) and
  `../wsfct/CHANGELOG.md` (**1,239,085 B**, entries as table rows under 8 month groupers). Neither
  matches the declared `^### \d{4}-\d{2}-\d{2} · \[`. A 1.2 MB ledger and a 324 B fresh seed
  produced **byte-identical output and the same exit status**, and the message actively reassured.
- **The fix.** A new `classify_empty()`. Three signals, any of which refuses: over
  `SEED_PLAUSIBLE_MAX_BYTES`; over `READ_CAP_LINES`; or evidence of records the grammar cannot see
  — a fence-aware **anchored** content probe plus **the seed's own freshness test**. The sentinel
  exemption covers only that fuzzy evidence, **never size**. Refusal is `GRAMMAR_MISMATCH` at
  **exit 3**, naming size, line count, both hit counts, the first unparsed line (bounded at 200
  chars; `ZONE_UNCLASSIFIED` bounds at 400) and the declared grammar. `ZONE_UNCLASSIFIED` was the
  model to copy, exactly as the UAT recommended.
- **Exit 3 is a return to the ratified table, not a new opinion.** `ledger-trimmer-design.md` §6.3
  already said `3 | usage error: … no records`; the branch shipped with **no exit code at all**.
  **Keeping 0 for the genuinely-empty half is ADDED POLICY** and is labelled as such in the code: a
  day-one adopter running `--check` from a hook must not be handed a usage error.
- **`SEED_PLAUSIBLE_MAX_BYTES` is deliberately its own literal**, not `DEFAULT_BUDGET_BYTES` and not
  `opts.budget_bytes`. `--budget-bytes` tunes when a trim *fires* and the seeds invite adopters to
  lower it; wiring it in would let a calibration choice decide whether the tool calls your ledger
  unreadable, and a budget under 12,124 B would condemn the seed we ship.
- **Three defects in this session's own design were found by producer mutation and by the diff
  review, not by reasoning.** (1) A mutant *deleting* the sentinel exemption **survived** — with the
  probe anchored, no fixture existed in which that guard could fire; a guard nothing can falsify is
  a comment shaped like a guard. (2) A mutant *adding* a probe to `HANDOFFS.md` survived, exposing
  `content_probe=None` there as an **undefended asymmetry** — strictness that depended on which of
  two filenames you were holding. Both ledgers now carry the same probe. (3) `negations` were
  computed as evidence and then **discarded**, so a receipt ledger written as bare `session:` blocks
  — no fences, no dated headings — still answered `NO_RECORDS` at exit 0: **F1 intact in the very
  file the probe had just been widened to cover.** Final harness **24 mutants, 24 killed, 0
  survived, 0 did-not-apply**, control green.
- **Two figures quoted from the UAT report did not reproduce and were replaced with ones that carry
  a command.** *"wsfct 508 table rows"* — actual **531** pipe-leading lines, **489** date-shaped;
  and `church_growth`'s receipt count is **19** fence-aware, **20** by a fence-blind grep. Both had
  been republished here from S43 without re-running their commands.
- **Verified on real files, not fixtures alone.** Four adopter ledgers now refuse: the two above
  plus **`../claims-model-starter.wiki`** (28,300 B) and **`../feedback-loop-comparison`**
  (7,067 B) — **both under both size limits, caught by the probe alone, and neither examined by the
  UAT**. That is what makes the probe load-bearing rather than decorative. `../airqino`'s genuine
  324 B seed and both shipped seeds still answer `NO_RECORDS` at exit 0; every parsing ledger is
  unchanged. **No file outside this repository was written.**
- **Adopter-visible surface.** `TRIM_VERSION` **1.0.0 → 1.1.0** (new finding code, new exit status,
  on a distributed tool). `README.md`'s install-size table re-derived by running the command the
  README itself publishes: executables **278,042 → 279,552 B**, total **765,311 → 766,821 B** —
  measured *after* the last edit, because the first pair was already stale by the time the comments
  were finished.
- **Not taken (FM #17):** F3, F6, F7, F8, F9 stay open; no `FRAMEWORK_LEARNINGS.md` row (it changes
  what adopters receive and is the operator's call); no ledger archiving; no `.gitignore` fix for
  `dashboard_history.jsonl`; no outward-facing action. **S34's PR remains prepared and unopened.**
- **A follow-up commit removed the seed-sentinel exemption entirely, because it reopened F1.** The
  first draft let a ledger still carrying `METHODOLOGY-SEED-SENTINEL` suppress the probe. Table rows
  do not match the `^###` negation, so the seal held while 121 probe hits were discarded, and a
  **6,150 B ledger holding 120 real table-row entries — `wsfct`'s exact shape, under both size
  limits — answered `[NO_RECORDS]` at exit 0.** F1 reopened by its own fix, found by the diff review
  and reproduced before being believed. **A seal you can hold open by choosing a record shape is
  worse than no seal.** The seeds are protected instead by the probe being *anchored* — both ship
  with zero hits, pinned by a fixture control, so a seed edit that would flag every adopter fails in
  our suite rather than at their root. The accepted cost is stated in the code: an adopter with a
  dated `##` heading in their own front matter and no records gets a loud false refusal. Loud and
  wrong is recoverable; quiet and wrong is the finding. `CHANGELOG.md`'s `seed_negation` went to
  `None` in the same pass — for a heading-keyed ledger the probe strictly subsumes it, so it could
  never be the only signal firing, and an unfalsifiable clause is a comment shaped like a guard.
  `TRIM_VERSION` **1.1.0 → 1.1.1**; final harness **20 mutants, 20 killed, 0 survived, 0 skipped**.
- **A third pass cleared the rest of the diff review** (31 findings filed, 17 survived refutation;
  most were the two above, caught mid-flight). Four were real and outstanding. The one that mattered
  is a **factual error in a distributed file**: the `content_probe` comment credited *"the four
  mismatched adopter ledgers found by the UAT"* — the UAT examined six repositories and found **two**
  (`model_project_constructor`, `wsfct`); the other two were found while building this fix and are
  not part of that audit. Corrected, with a sentence telling the next reader not to re-merge them.
  Also: the refusal message printed *"0 line(s) matching this ledger's own freshness test"* for a
  ledger that declares none — now omitted unless one is declared; a behavioural test for the
  `HANDOFFS.md` probe had been lost in an edit, leaving that mutant killable only by another test's
  fixture control (coverage by accident) and is restored with its own negation-is-silent control; and
  a citation to a test name wrapped across two comment lines, so grepping for it found nothing.
- **Incident, disclosed:** a design-review subagent wrote a probe sentence into the **distributed**
  seed `starter-kit/CHANGELOG.md` and left it uncommitted. Caught at the next `git status`, reverted
  (`git checkout --`), and the tree re-verified clean before any commit. The second review workflow
  was launched with an explicit read-only constraint and a self-check on `git status --porcelain`.

### 2026-08-04 · [ad hoc] Reconcile-on-read: S43's `commit:` field → `f7637b3` — sixteenth discharge, and the first receipt that closed out twice

**Model:** Claude Opus 5 (1M context).
**Record repair, committed on its own** per `starter-kit/SESSION_RUNNER.md:39` and `:42`. Precedents:
`75bc44b`, `e23d595`, `ab94743`, `5e9ea52`, `1b3f808`, `763e8c7`, `eb6fbe4`, `408136c`, `0a1f19b`,
`40a1554`, `caf1612`, `c000a90`, `0a1a0d5`, `d9bedb0`, `9267500`, `7752114`, `728f39a`.

- **What was reconciled.** S43 closed out `commit: pending`, legitimately — its receipt shipped inside
  the commit whose sha it names. That sha is **`f7637b3`**. Derived, not assumed: walking
  `git log --all --full-history` over `HANDOFFS.md` (**123** commits, all refs) and reading each
  blob's S43 block with `bin/check-handoff`'s own `extract_blocks`/`parse_block`.
- **The derivation returned two answers this time, and that is new.** Every prior discharge found
  exactly **one** commit carrying the session's block at `status: complete`. S43 has **two** —
  `f7637b3` and `b215c0a` — because the operator corrected the session's `nprcgenekeepr` disclosure
  after close-out and the receipt was amended in place to carry finding **F12**. The claim stub
  `4dea909` still reads `status: pending`, so the stub/close-out split holds for a **sixteenth**
  consecutive receipt (S29's gotcha 3). **The field names `f7637b3`, the earlier of the two** — the
  commit where the close-out actually happened; `b215c0a` is a correction *to* the receipt, not a
  second close-out of it. Naming the later sha would have silently redefined "the commit this receipt
  shipped in" to mean "the last commit that touched it", which is a different question with the same
  answer on all fifteen previous receipts and a different one here. Both shas are recorded in the
  field so the amendment is not lost.
- **The ordinal is derived, not incremented on faith.**
  `grep -cE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[ad hoc\] Reconcile-on-read' CHANGELOG.md docs/archive/CHANGELOG-*.md`
  returned **16** in the live file and **0** in both archive shards immediately before this entry was
  prepended — and one of those sixteen is the `nine commit: fields that named no sha` **repair**, not
  a discharge. Fifteen numbered discharges precede this one, so this is the **sixteenth**.
- **Taken BEFORE the claim.** Nothing else was staged when this was committed. Both ledger frontiers
  agreed at `b215c0a` at Orient and `git rev-list --count --no-merges b215c0a..HEAD` was **0** — no
  ghost session, no backfill owed. The working tree was clean apart from the untracked
  `dashboard_history.jsonl` that S43's own Phase 0 step-5 dashboard run left behind and reported as
  **F9**; it is still uncommitted, still not covered by `.gitignore`, and still not fixed here
  (FM #17). This session's own mandated dashboard run was taken through the scratchpad symlink
  harness (S43's gotcha 4) precisely so it would not write a second one.

### 2026-08-04 · [ad hoc] S43 — UAT: the framework against six real adopter repositories, read-only

**Model:** Claude Opus 5 (1M context).
Operator-assigned (*"begin UAT with ../airqino, ../church_growth, ../model_project_constructor,
../mts-system, ../vscode_quarto_ext, and ../wsfct"*), scoped in the same exchange to a **read-only**
assessment across **all four** adopter-facing surfaces. **Fork session `S43` is not plan §5 queue item
`S43`** (`bin/check-derived`) — the axes coincide for the fourth time and it remains a coincidence.
Deliverable: **one report, [`docs/planning/uat-2026-08-04-six-adopters.md`](docs/planning/uat-2026-08-04-six-adopters.md)**, fork-only. **12 findings — 5 critical, 5 moderate, 2 minor; 10 of 12 are defects in
what we ship.** No adopter repository was written to, and the claim is proven rather than asserted:
`git status --porcelain` across all six is byte-identical to the pre-audit snapshot.

- **The result that reframes the rest: a fresh adopter installs cleanly.** `bin/sync --dry-run` into
  an empty git repo writes all **24** destinations, `FRAMEWORK_LEARNINGS.md` and
  `methodology_trim.py` included. **Every defect found is an *update-path* defect** — the fleet is
  un-updated, not broken. The report says so before its findings so they are not misread.
- **The trimmer declares multi-hundred-KB ledgers empty, in the words reserved for a fresh seed.**
  `model_project_constructor/CHANGELOG.md` (**597,717 B**, 130 dated entries) and
  `wsfct/CHANGELOG.md` (**1,239,085 B**, 508 table rows) both print *"holds zero records under its
  declared grammar … A freshly seeded ledger looks exactly like this"* and exit **0** — the same
  status as "trigger does not fire". The grammar wants a U+00B7 middle dot and a source tag; they use
  an em dash and `## YYYY-MM`. A grammar mismatch is indistinguishable from an empty file.
- **Every adopter holding `BOOTSTRAP.md` holds the history-destroying instruction S41 fixed, and the
  only documented route to the fix is that instruction.** `:330` in all three still reads *"It will
  fetch the latest starter-kit files and overlay them"* with no exception. S41's rewrite has reached
  **0 of 6**. `bin/` ships nothing, so an adopter without a sibling clone has only the prose route.
- **`SESSION_NOTES.md` is documented as transient, accumulates in 6 of 6, and no tool covers it.**
  The seed contradicts itself — `:5` *"transient — it is overwritten every session"* against `:27`
  *"Session history accumulates below this line"* — and `SESSION_RUNNER.md:260` publishes the false
  half. `model_project_constructor` is at **25,346 lines, 12.7× the 2,000-line `Read` cap**, on a file
  Phase 0 step 2 mandates reading; the trimmer knows only `CHANGELOG.md` and `HANDOFFS.md`.
- **2 of 6 cannot be updated at all, and the file explaining the way out is among the files withheld.**
  `bin/sync` exits 2 on `model_project_constructor` and `wsfct`; the guard is *correct* (three of the
  four blocked files carry genuine project content). But the reconciliation procedure lives in
  `BOOTSTRAP.md:341`/`:452`, and **`BOOTSTRAP.md` is absent from both repos.**
- **Two live instances of the same checker false positive, found the same day.** `bin/check-handoff`'s
  `SHA_RE` (`:198`) requires a hex *letter*, so an all-numeric short sha is rejected: `mts-system`
  receipt S74's `commit: 4966443` (a real commit, `49664433f…`, failing since 2026-07-14) and **this
  repository's own S42 receipt**, which reconciled to `8804635` at this session's Phase 0 and had to
  be written `8804635e` to pass. The comment at `:197` claims a mitigation that `:373-374` removes.
- **Also:** the dashboard credits `airqino`'s 17-versions-behind `SESSION_RUNNER.md` in full (96–100%
  methodology compliance for all six, against **11–20** drifting files each, **82** portfolio-wide);
  the URL update path installs nothing for 6 of 6 until upstream merges (S41's pre-flight working as
  designed); `ZONE_UNCLASSIFIED` reproduced on a 1.1 MB `HANDOFFS.md` from our own seed's trailing
  comment; `dashboard_history.jsonl` is ignored in 1 of 6 and tracked-and-dirty in one.
- **Verified rather than assumed, on the pass side:** S41's stale-format detection was correct on
  **9 of 9** ledgers; the trimmer's fence-awareness correctly excluded the seed's own template line
  from `church_growth`'s 26 records; `bin/sync`'s local-modification guard protected real content.
- **A 13-agent adversarial workflow refuted or materially overstated 4 of my 6 headline claims**, and
  the corrections are in the report rather than its findings. The worst was mine: I reported "6 to 9"
  drifting files per repo when the true range is **11 to 20** — a figure matching no slice of output I
  had already collected — and asserted a dangling `FRAMEWORK_LEARNINGS.md` reference in all six when
  **0 of 6** runners reference it at all. Every number published was re-run by me at `4dea909`;
  figures I could not personally reproduce were dropped.
- **F12 was produced by this audit committing the defect it describes, and it is the sharpest finding
  in the set.** I reported reading `nprcgenekeepr` as a breach of a standing off-limits instruction.
  **It was not one.** The operator lifted that constraint in the final prompt of the preceding session
  — *"nprcgenekeepr now idle"* — and **the lift was never written down**: `grep -rn "idle"` over both
  ledgers and both archive shards returns only S41/S42 stating the trigger *condition*, never the
  trigger firing, while `CHANGELOG.md:244` records the imposition in full. **Phase 0 reconcile cannot
  catch this** — it is keyed to `<frontier>..HEAD`, and an operator lifting a scope constraint leaves
  no commit — so the write-gate is the only mechanism that covers it, and it did not fire. This is the
  mirror image of the failure `CLAUDE.md` already records (a session that *invented* a constraint
  nobody imposed): **a constraint has two edges, and only one of them is being logged.** The rule this
  repo already carries — *check who imposed a blocker and when* — needs its other half: check whether
  it still holds. Corrected in the report, the receipt and this entry; the operator caught it.
- **Two scope disclosures, both in the report's §7.** Repositories outside the assigned six were read
  read-only during verification (`chat_verification`, `claude_work`, `dalia_martinez_funeral`,
  `feedback-loop-comparison`, `nprcgenekeepr`) — none of them off-limits, per F12, but none of them
  assigned either: the six-repo scope was named in the subagents' prose while the commands were given
  the whole tree. And this session's own mandated Phase 0 dashboard run left an untracked
  `dashboard_history.jsonl` at this repo's root, which `.gitignore` does not cover — an instance of
  finding F9 in the canonical repo.
- **Not done, deliberately:** no adopter repository touched (three carry uncommitted work, two are on
  feature branches); no defect fixed — findings are recorded, not remediated; **no `FRAMEWORK_LEARNINGS.md`
  row**, because this session's claim scoped out every distributed file and a row changes what adopters
  receive (owed, and named in the receipt as a residual); no outward-facing action.
- **Commits:** `75bc44b` (Phase 0 reconcile) · `4dea909` (claim) · this commit. **Session:** S43.

### 2026-08-04 · [ad hoc] Reconcile-on-read: S42's `commit:` field → `8804635` — fifteenth discharge, taken before the claim

**Model:** Claude Opus 5 (1M context).
**Record repair, committed on its own** per `starter-kit/SESSION_RUNNER.md:39` and `:42`. Precedents:
`e23d595`, `ab94743`, `5e9ea52`, `1b3f808`, `763e8c7`, `eb6fbe4`, `408136c`, `0a1f19b`, `40a1554`,
`caf1612`, `c000a90`, `0a1a0d5`, `d9bedb0`, `9267500`, `7752114`, `728f39a`.

- **What was reconciled.** S42 closed out `commit: pending`, legitimately — its receipt shipped inside
  the commit whose sha it names. That sha is **`8804635`**. Derived, not assumed: walking
  `git log --all --full-history` over `HANDOFFS.md` (**119** commits, all refs) and reading each
  blob's S42 block with `bin/check-handoff`'s own `extract_blocks`/`parse_block`, `8804635` is the
  **only** commit where it reads `status: complete`; the claim stub `cc593e0` carries the same block
  at `status: pending`, so the stub and the close-out are distinct commits — S29's gotcha (3), now
  **fifteen receipts running**.
- **The ordinal is derived, not incremented on faith.**
  `grep -cE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[ad hoc\] Reconcile-on-read' CHANGELOG.md docs/archive/CHANGELOG-*.md`
  returned **15** in the live file and **0** in both archive shards immediately before this entry was
  prepended — and one of those fifteen is the `nine commit: fields that named no sha` **repair**, not
  a discharge. Fourteen numbered discharges precede this one, so this is the **fifteenth**.
- **Taken BEFORE the claim.** Nothing else was staged when this was committed. The working tree was
  clean at Orient apart from an untracked `dashboard_history.jsonl`, written by the Phase 0 step-5
  dashboard run itself and **not** covered by `.gitignore` — reported, not committed, and not fixed
  here (FM #17).
- **The two frontiers disagree for the first time in this run, and the gap is benign.**
  `git log -1 --format=%H -- CHANGELOG.md` returns `db8f061`; `git log -1 --format=%H -- HANDOFFS.md`
  returns `8804635`. The one commit between them is `db8f061` itself — the ledger-only record of the
  operator-authorized push, taken *after* S42's close-out. `git rev-list --count --no-merges db8f061..HEAD`
  is **0**, so no backfill is owed on the ledger side; and a commit that exists solely to record a
  non-commit action is not a session that left work unreceipted, so no reconstructed `status: reconciled`
  block is owed on the receipt side either. No ghost session.

### 2026-08-04 · [ad hoc] Pushed 42 commits to `origin/main` — the fork is published, and the README's pinned SHAs now resolve

**Model:** Claude Opus 5 (1M context).
**A push is a non-commit action, so it is recorded here rather than left to `git log`** (failure
mode #27; the same reason releases, tags and PR opens get entries). **Authorized by the operator in
the same breath as the UAT go-ahead** — *"push to origin prior to starting UAT"* — and taken after
S42's close-out, which is why it is its own entry and not a correction to S42's receipt. That receipt
says "no outward-facing action was taken" and remains true of the session it describes.

- **What moved.** `d9bedb0..8804635`, **42 commits**, `origin/main` only. Nothing was pushed to
  `upstream/main`, no branch was created, no PR opened. `main` is now **0 ahead / 0 behind**
  `origin/main` and **165 ahead / 0 behind** `upstream/main`. The two other local branches
  (`docs/bl-10-dangling-learning-citations`, `docs/learning-13-handoff-predictions`) were already in
  sync with origin and were not touched.
- **It discharges half of S42's own finding, and the measurement is the proof.** The `## What It
  Costs` section pins four SHAs — `cc593e0`, `020ba3f`, `7a71df0`, `3aee4e3` — and before this push
  **none of them resolved in any published clone**; two were on no remote at all. All four now return
  `YES` to `git merge-base --is-ancestor <sha> origin/main`. **All four still return `no` against
  `upstream/main`**, and no push can change that: the figures they pin are measurements of this
  fork's own ledger history, which is not upstream's. That remains a stated precondition for any
  upstream PR carrying the section, not a defect this action closed.
- **What is still unselected.** Ten paths in those 42 commits do not exist upstream. Three
  (`starter-kit/FRAMEWORK_LEARNINGS.md`, `starter-kit/methodology_trim.py`,
  `tools/test_methodology_trim.py`) **must** go — their absence is what makes Test 9 fail and what
  makes a URL-sourced adopter update install nothing. Three are fork-only by convention
  (`docs/planning/BACKLOG.md`, `framework-context-cost-plan.md`, `ledger-trimmer-design.md`). **Four
  are undecided** — `docs/planning/dashboard-signal-integrity-plan.md`,
  `model-use-provenance-plan.md`, and both `docs/archive/CHANGELOG-*` shards — because "planning is
  fork-only" is *not* a blanket rule: `upstream/main` carries four planning documents of its own.
  That selection is an open decision, recorded here so the next session does not have to rediscover
  that it was never made.
- **UAT scope set at the same time.** The operator named
  **`/Users/rmsharp/Development/nprcgenekeepr` as busy and off-limits** until they say otherwise —
  no read-for-write, no `bin/status`, no `bin/sync` against it. The other three S41 candidates
  remain candidates, and their live state was re-measured at this point rather than inherited from
  S41: `mts-system` 2 uncommitted / 1 undocumented commit since `42aae69`; `vscode_quarto_ext`
  3 uncommitted / 0 undocumented; `wsfct` 0 uncommitted / 1 undocumented. **S41's recorded frontier
  for `nprcgenekeepr` (`5c9ee6c`) is already stale — it now reads `7739e425`** — which is the
  standing reason to re-derive an adopter's frontier at the moment of use.

### 2026-08-04 · [ad hoc] S42 — what the framework costs an adopter, and the numbers a reader cannot reach

**Model:** Claude Opus 5 (1M context).
Operator-assigned; sequenced by S41 as residual (i). **Fork session `S42` is not plan §5 queue item
`S42`** (purge derived values from `CLAUDE.md`) — the axes coincide for the third time and it remains
a coincidence. `README.md` gains one section, **`## What It Costs`**, 160 lines, 70,502 → 83,896 B.
No distributed file was touched: `README.md` is absent from `bin/_manifest.py`, so no adopter
receives a byte of this.

- **Why it was owed.** [`framework-context-cost-plan.md`](docs/planning/framework-context-cost-plan.md)
  exists because the operator raised the cost, and it measured that cost in detail — but
  `docs/planning/` reaches no adopter and no reader of the landing page. A prospective adopter could
  read the entire public corpus and find no statement of what a session costs them. Four costs are
  now stated: **disk 757,941 B / 24 files**, an unavoidable **per-session floor of 64,851 B**, two
  ledgers growing at **43.9 lines per entry** and **44.8 lines per receipt**, and a cadence of one
  deliverable and two-to-three mandatory stops per session.
- **Every figure carries the command that prints it — DVX sink 4, applied to a page that adds ~30
  derived values to a live file.** Without it the section would be the exact defect the plan was
  written about. Two figures cannot carry one and say so in place: the 91.7% cache-read telemetry and
  the private-portfolio comparison.
- **A 5-lens adversarial review with a refute pass filed 29 findings; 15 survived, all fixed.** Two
  were serious and both were mine. **(1) The section promised that every figure carried its command
  and its own tables broke the promise** — the two headline byte slopes, the `2.09 entries per
  session` that converts bytes into a deadline, the seed row and the whole "Files" column were
  produced by nothing on the page. Worse, the printed numbers supported a *different* answer: a
  reader combining the two visible deltas gets 1.10 entries/session and ~7.9 sessions of headroom,
  nearly double the true four. Fixed by publishing the missing commands, not by softening the
  promise. **(2) None of the four pinned SHAs is reachable from any published clone** — `cc593e0` and
  `020ba3f` are on no remote at all (local `main` is **41 ahead of `origin/main`**), and `7a71df0` /
  `3aee4e3` are fork-only, so a reader who clones `KJ5HST/methodology` gets `fatal: invalid object
  name` from the very commands the section tells them to trust over its prose. The section now states
  which figures depend on this repository's history; **making them reachable is a push, and pushes
  are the operator's call.**
- **Three claims the review falsified and I had asserted.** *"The heaviest possible user of its own
  framework … an upper bound"* — false: this repository writes the largest receipts by bytes
  (**12,764 B** each against **3,517–7,404** across seven adopters) but has neither the largest
  ledger (another is **10.3×**) nor the fastest line growth (an adopter's 20 receipts average **47.9**
  lines against **44.6** here). *"Nothing here is installed into your project"* — true of what the
  manifest installs, false on disk: **6 of 11** adopter repositories hold a hand-copied
  `docs/methodology/README.md`. *"`methodology_dashboard.py` reports headroom … so growth is watched
  rather than discovered"* — it is a **tripwire, not a gauge**: it reports headroom only for a ledger
  already archived once, and below the trigger it emits nothing.
- **Two more corrections, one of them a number I nearly republished from the plan.** The
  commit-denominated headroom is **13.3 commits**, not the plan's `36.0` — that figure was true at the
  tree it was measured on and is not true now, which is the plan's own thesis landing on the plan.
  And the Present → Implement gate is not design-only: `ITERATIVE_METHODOLOGY.md` calls it the most
  valuable gate in the model and the Development and Research-Documentation workstreams each carry
  their own `Phase 4: Present`, so it binds any session that will build something. Two skeptics
  refuted that finding and one confirmed it; it was settled from the sources, not from the vote.
- **Verification.** `bash bin/tests.sh` **182 passed / 1 failed** — Test 9's expected upstream 404,
  unchanged from the claim baseline and **not to be weakened**. `python3 -m unittest discover -s tools`
  **334 OK**. `python3 bin/check-links` OK **88 links / 22 files**. Dashboard twins byte-identical.
  Every one of the section's **nine** command blocks was executed verbatim after the last edit and
  matched its published output; the 18 fence delimiters balance and no table's column count drifts.

### 2026-08-04 · [ad hoc] Reconcile-on-read: S41's `commit:` field → `12463dd` — fourteenth discharge, taken before the claim

**Model:** Claude Opus 5 (1M context).
**Record repair, committed on its own** per `starter-kit/SESSION_RUNNER.md:39` and `:42`. Precedents:
`ab94743`, `5e9ea52`, `1b3f808`, `763e8c7`, `eb6fbe4`, `408136c`, `0a1f19b`, `40a1554`, `caf1612`,
`c000a90`, `0a1a0d5`, `d9bedb0`, `9267500`, `7752114`, `728f39a`.

- **What was reconciled.** S41 closed out `commit: pending`, legitimately — its receipt shipped inside
  the commit whose sha it names. That sha is **`12463dd`**. Derived, not assumed: walking
  `git log --all --full-history` over `HANDOFFS.md` (**116** commits, all refs) and reading each
  blob's S41 block with `bin/check-handoff`'s own `extract_blocks`/`parse_block`, `12463dd` is the
  first commit where it reads `status: complete`; the claim stub `c44037c` carries the same block at
  `status: pending`, so the stub and the close-out are distinct commits — S29's gotcha (3), now
  **fourteen receipts running**.
- **The ordinal is derived, not incremented on faith.**
  `grep -cE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[ad hoc\] Reconcile-on-read' CHANGELOG.md docs/archive/CHANGELOG-*.md`
  returned **14** in the live file and **0** in both archive shards immediately before this entry was
  prepended — and one of those fourteen is the `nine commit: fields that named no sha` **repair**, not
  a discharge. Thirteen numbered discharges precede this one, so this is the **fourteenth**.
- **Taken BEFORE the claim**, unlike S33 (the only session that took it late) and unlike S40/S41,
  which had to *recover* the order after drafting a claim stub first. Nothing else was staged when
  this was committed.
- **Nothing else needed reconciling, and both frontiers agree on it.**
  `git log -1 --format=%H -- CHANGELOG.md` and `git log -1 --format=%H -- HANDOFFS.md` both return
  `12463dd`, and `git rev-list --count --no-merges 12463dd..HEAD` is **0** — no ghost session, no
  backfill owed. The working tree was clean at Orient.

### 2026-08-04 · [ad hoc] S41 — the update path for older adopters, and a documented instruction that destroys history

**Model:** Claude Opus 5 (1M context).
Operator-assigned: *"the equivalent of 'Update methodology using
https://github.com/KJ5HST/methodology' should work for repositories using earlier versions of
methodology."* **Fork session `S41` is not plan §5 queue item `S41`** (the floor audit, still
undecided). Three independent defects; two fixed here, one is upstream's.

- **The most serious is the one nobody had to run to hit.** `starter-kit/BOOTSTRAP.md`'s agent-facing
  update path — the operator's exact phrase, already documented there — read in full: *"It will fetch
  the latest starter-kit files and overlay them."* It named **no exception**. Four distributed files
  are adopter-owned (`CHANGELOG.md`, `HANDOFFS.md`, `SESSION_NOTES.md`, `ROADMAP.md`), and an agent
  following that sentence literally **overwrites the action ledger and the receipt ledger with empty
  templates** — destroying precisely the history `SEED` disposition exists to protect. `bin/sync`
  refuses structurally; prose had nothing. Rewritten as three numbered rules with a tracked
  vs adopter-owned table, the by-hand reconcile step, and a verification step. **Pinned by new
  Test 28**, because a list in prose drifts: both directions are asserted against `_manifest`
  (every SEED named; no TRACKED mislabelled) and **both were driven RED on separate mutations**.
- **The stale-format detector could not fire, and reported *current* instead.** `BOOTSTRAP.md:85`
  promises `bin/status` *"flags any seed whose format predates the current methodology ... so the
  format lag is surfaced rather than silent."* S40 falsified it: `SEED_FORMAT_MARKERS` keyed on the
  seeds' **H1 titles**, and titles are exactly what did not change. Measured across the operator's
  portfolio — **11 sibling projects hold `CHANGELOG.md`, 9 hold `HANDOFFS.md`, 0 held the doctrine**,
  and every one reported `present`. Markers now key on the `## Size, and when to archive` heading,
  which lives in the front-matter zone the trimmer pins and therefore survives every trim and
  prepend. Recorded as **Learning #19**: a version tripwire keyed to something that never changes
  across versions cannot fire, and it fails by returning a confident *current*.
- **A URL-sourced update installed nothing and blamed the operator's credentials.** `read_github`
  exited on the **first** failing file with `hint: run gh auth login`. Auth was fine; two files in
  this manifest simply are not upstream yet, and the first sits at manifest index **1**, so the run
  died before writing anything. New `fetch_all_github` reads the whole distribution before writing,
  separates *absent upstream* from *actual error*, and now says: `2 of 24 distributed file(s) do not
  exist in KJ5HST/methodology yet` — naming both, stating **"This is NOT an authentication
  problem — the other 22 file(s) read fine"**, explaining that the repository is behind this
  manifest, and pointing at `--source=local`.
- **The third defect is not fixable here and needs the operator.** Those two files reach upstream
  only through a merged PR. Until then `--source=github` cannot deliver a complete update, which is
  what `bin/tests.sh` Test 9 has been reporting all along — **that failure is evidence for this
  finding, not noise, and must not be weakened.**
- **Verified end-to-end on real syncs, not reasoned about.** A fresh adopter reads `present`; an
  adopter with pre-doctrine ledgers carrying real history reads `present (stale format)` on **both**,
  with the migration note; and a re-sync leaves that history intact. `bash bin/tests.sh`
  **182 passed / 1 failed** (178 baseline + 4 new; the 1 is Test 9's expected 404),
  `python3 -m unittest discover -s tools` **334 OK**, `python3 bin/check-links` OK **88 links /
  22 files**, dashboard twins identical.
- **A test that never ran is worse than no test, and this session shipped one for an hour.**
  Test 28 first used an undefined `$KIT`; with `set -u` active the script aborted mid-test, and the
  tell was the missing `== Summary ==` line rather than any failure message. The earlier RED proofs
  had been run standalone, so they proved the *logic* and not the *harness*. Both assertions were
  re-proved RED **inside the suite** afterwards (181/2, naming exactly the two removed files).
- **The four-repo rollout is deferred, not abandoned**, on the operator's instruction not to modify
  repositories in active use. Nothing outside this repo was touched: the four target working trees
  were re-checked after the stand-down and are as found.

### 2026-08-04 · [ad hoc] Reconcile-on-read: S40's `commit:` field → `11b843a` — thirteenth discharge, taken before the claim

**Model:** Claude Opus 5 (1M context).
**Record repair, committed on its own** per `starter-kit/SESSION_RUNNER.md:39` and `:42`. Precedents:
`5e9ea52`, `1b3f808`, `763e8c7`, `eb6fbe4`, `408136c`, `0a1f19b`, `40a1554`, `caf1612`, `c000a90`,
`0a1a0d5`, `d9bedb0`, `9267500`, `7752114`, `728f39a`.

- **What was reconciled.** S40 closed out `commit: pending`, legitimately — its receipt shipped inside
  the commit whose sha it names. That sha is **`11b843a`**. Derived, not assumed: walking
  `git log --all --full-history` over `HANDOFFS.md` (**113** commits, all refs) and reading each
  blob's S40 block with `bin/check-handoff`'s own `extract_blocks`/`parse_block`, `11b843a` is the
  first commit where it reads `status: complete`; the claim stub `65cdc19` carries the same block at
  `status: pending`, so the stub and the close-out are distinct commits — S29's gotcha (3), now
  **thirteen receipts running**.
- **The ordinal is derived too, not incremented on faith.** `grep -cE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[ad hoc\] Reconcile-on-read' CHANGELOG.md docs/archive/CHANGELOG-*.md`
  returned **13** in the live file and **0** in either archive shard, immediately before this one was
  prepended — one of the thirteen is the `nine commit: fields that named no sha` **repair**, not a
  discharge. Twelve numbered discharges precede this one, so this is the **thirteenth**.
- **Taken BEFORE the claim, and it had to be recovered to stay that way.** This session drafted its
  Phase 1B stub first, noticed the outstanding answer slot only when `bin/check-handoff` failed, and
  **reverted the stub to HEAD rather than collapse the two commits** — the working copy was set aside,
  the reconcile taken alone, and the claim re-applied on top. S33 remains the only session that took
  the reconcile late.
- **Nothing else needed reconciling, and both frontiers agree on it.**
  `git log -1 --format=%H -- CHANGELOG.md` and `git log -1 --format=%H -- HANDOFFS.md` both return
  `11b843a`, and `git rev-list --count --no-merges 11b843a..HEAD` is **0** — no ghost, no backfill.

### 2026-08-04 · [ad hoc] S40 — the ledger doctrine, and an instruction that would have deleted an adopter's records

**Model:** Claude Opus 5 (1M context).
Plan §5 queue item **S40** (fork session **S40** — the axes agree this session). Spec:
[`ledger-trimmer-design.md`](docs/planning/ledger-trimmer-design.md) §11 Phase 5. **G3** of the
operator's three goals: the instructions for the cases automation cannot reach.

- **What is now true.** `starter-kit/CHANGELOG.md` and `starter-kit/HANDOFFS.md` each carry a
  **Size, and when to archive** section stating a size norm, the archive trigger, the shard
  convention and the commands to run. Before this, **no distributed file stated any archive, split,
  size or truncation policy**, and the receipt seed described itself as *kept forever* — the single
  hard contradiction, now gone. Both seeds state all three of Phase 5's items **independently**;
  neither depends on the other having been installed.
- **The check that proves it is new, because the published one had stopped working.** §11 Phase 5
  shipped `grep -l archiv starter-kit/*.md   # currently empty`. It was not empty at S39' and is not
  empty now — **a word is not a policy.** Replaced with one that asserts what the file *says*:
  ```sh
  python3 -c "import sys;sys.path.insert(0,'bin');import _manifest as m;\
    print('\n'.join(sorted(e[0] for e in m.DISTRIBUTION if e[0].endswith('.md'))))" \
    | xargs grep -l '^## Size, and when to archive'
  ```
  → exactly the two ledger seeds.
- **THE WORST DEFECT WAS MINE, IT WAS A DISTRIBUTED INSTRUCTION, AND IT INVITED THE EXACT LOSS THE
  TOOL EXISTS TO PREVENT.** The seed told adopters `--write` *"leaves the change staged for you."*
  The trimmer contains **no `git add` anywhere**, prints `WRITTEN (uncommitted — this tool never
  commits)`, and leaves the new shard **untracked**. An adopter who believed the sentence and ran
  `git commit -a` would have committed the *shortened* ledger while the shard holding the removed
  records never entered history — and the rollback promised in the same clause
  (`git checkout -- <file>`) only works *because* nothing is staged. I did not invent it: it is
  copied faithfully from this design's own `:722`, *"staged-but-uncommitted"*, which its own rollback
  table two lines below already contradicts. **The spec was stale and I cited it instead of running
  the tool.** Recorded as **Learning #18**; the design's stale sentence is raised, not fixed (FM #17).
- **The worked anecdote was chronologically backwards.** I published that the receipt ledger
  *"carried ~1,200 lines while its archive actually fired at 997, and nothing noticed."* The archive
  (`7a71df0`, 19:15) **predates** the level (`3aee4e3`, 21:35) by 2h20m the same day —
  `git merge-base --is-ancestor` settles it in one command — and six lines of this repo's own
  `HANDOFFS.md` noticed, one of them the stub that created this session. Rewritten to the claim that
  is both true and stronger: the level **has never once fired**; the file sits under it while running
  multiples over its byte budget; a level in the wrong unit says *fine* indefinitely.
- **Phase 5's "the archive trigger as a *rate*" is half the rule, and shipping only that half would
  have been silent on the file this campaign exists for.** §5.2 says the byte metric is a **level
  with hysteresis, not a rate**, and measured at this session's claim the *line* rate does **not**
  fire on `HANDOFFS.md` — only the byte level does. Both seeds state both conditions with the correct
  form for each; **the departure is labelled** at §11 Phase 5 and in the queue row.
- **G3 is delivered for new adopters only, and the mechanism that would tell the rest is deliberately
  untouched.** Both seeds are **SEED** disposition — written only when the destination is absent —
  and `bin/_manifest.py`'s `SEED_FORMAT_MARKERS` key on their H1 titles, which this change leaves
  intact, so `bin/status` reports every existing adopter's ledger as `present`, not
  `present (stale format)`. Changing that marker flags every adopter at once: an operator decision,
  not taken here. **This also settles the item S39' handed forward with a *no*:** the dashboard's
  absent-branch remedy must not point at these sections, because the trimmer is `TRACKED` and the
  seeds are `SEED`, so "tool absent" implies "seed predates S40" — the two are anti-correlated and
  the pointer would name a section that reader is guaranteed not to have.
- **Cost, stated rather than buried — this is the first change in the context-cost campaign that
  *increases* per-session cost.** The two seeds grow **+8,252 B**, and every byte lands in the
  **pinned front-matter zone the trimmer never touches**. Re-derive:
  `for f in starter-kit/CHANGELOG.md starter-kit/HANDOFFS.md; do git show <sha>:$f | wc -c; wc -c < $f; done`.
  Judged worth it against a measured **13,639 B per receipt** on this repo's own ledger.
- **Verification.** `bash bin/tests.sh` **178 passed / 1 failed** — `FAIL: github source dry-run
  failed`, Test 9's expected 404 on files not yet upstream, named not counted, and identical to the
  claim baseline. `python3 -m unittest discover -s tools` **334 OK**. `python3 bin/check-links` OK
  **88 links / 22 files**. The seed fixture invariant holds under **both** implementations (the
  dashboard's counter and the trimmer's `classify_zones` each read **0** records in each seed while
  the naive regex reads 3 and 1) — the property that stops a freshly seeded adopter ledger being
  trimmed on day one. All **13** line-anchored citation instances into the seeds are **byte-identical
  to HEAD**, achieved by inserting only below the highest cited line. Two real `bin/sync` runs into
  throwaway repos: the doctrine lands at the adopter root, both published commands are accepted
  verbatim (exit 0), and a controlled pre/post pair scores identical health with identical risks.
- **A 5-lens adversarial review over the uncommitted diff, each finding then attacked by a refuter
  that defaults to refuted: 4 survived, all fixed, 2 of them serious and both mine.** The refutations
  were not rubber stamps — one lens's "the pointer carries no recompute command" was refuted by a
  refuter that actually *ran* the verify script it dismissed.

### 2026-08-04 · [ad hoc] Reconcile-on-read: S39's `commit:` field → `316e7ef` — twelfth discharge, taken before the claim

**Model:** Claude Opus 5 (1M context).
**Record repair, committed on its own** per `starter-kit/SESSION_RUNNER.md:39` and `:42`. Precedents:
`1b3f808`, `763e8c7`, `eb6fbe4`, `408136c`, `0a1f19b`, `40a1554`, `caf1612`, `c000a90`, `0a1a0d5`,
`d9bedb0`, `9267500`, `7752114`, `728f39a`.

- **What was reconciled.** S39 closed out `commit: pending`, legitimately — its receipt shipped inside
  the commit whose sha it names. That sha is **`316e7ef`**. Derived, not assumed: walking
  `git log --all --full-history` over `HANDOFFS.md` (**110** commits, all refs) and reading each blob's
  S39 block with `bin/check-handoff`'s own `extract_blocks`/`parse_block`, `316e7ef` is the first
  commit where it reads `status: complete`; the claim stub `5b0dd23` carries the same block at
  `status: pending`, so the stub and the close-out are distinct commits — S29's gotcha (3), now
  **twelve receipts running**.
- **The ordinal is derived too, not incremented on faith.** `grep -cE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[ad hoc\] Reconcile-on-read' CHANGELOG.md docs/archive/CHANGELOG-*.md`
  returned **12** in the live file and **0** in either archive shard, immediately before this one was
  prepended — one of the twelve is the `nine commit: fields that named no sha` **repair**, not a
  discharge. Eleven numbered discharges precede this one, so this is the **twelfth**.
- **Taken BEFORE this session's Phase 1B claim**, holding the order for the twelfth consecutive time
  (S33 is still the only session that took it late). **BL-14's distributed half remains open**, so the
  practice is still inherited from the predecessor's receipt rather than assigned by any checklist:
  `starter-kit/SESSION_RUNNER.md` Phase 0 step 6 still scopes reconcile to `status: pending` receipts
  and undocumented commits — never to a *complete* receipt whose `commit:` is `pending`.
- **Nothing else needed reconciling, and both frontiers agree on it.**
  `git log -1 --format=%H -- CHANGELOG.md` and `git log -1 --format=%H -- HANDOFFS.md` both return
  `316e7ef`, and `git rev-list --count --no-merges 316e7ef..HEAD` is **0** — no ghost, no backfill.
  `python3 bin/check-handoff` was **OK** before this edit (newest receipt structurally complete, all
  23 older receipts naming a sha) and is re-run after it. The live file still holds **24** receipts;
  this repair adds none, so the header count is unchanged and was re-counted rather than assumed
  (`grep -c '^\`\`\`handoff' HANDOFFS.md` → 24).
- **The G2 trend line, re-measured rather than quoted forward — and BOTH files have now been past RED
  for two consecutive readings.** `python3 starter-kit/methodology_trim.py --file HANDOFFS.md --check`
  reads **SRF 1.4911** against archive `7a71df0` (both the most-recent and H3's largest-drop boundary
  resolve to the same archive, so nothing has to be chosen), **308,563 B** against a 65,536 B budget,
  line headroom **20**, trigger **FIRES**. That is the **fifth consecutive reading past RED** — 1.0820
  at S36, 1.1709 at S37, 1.2832 at S38, 1.4028 at S39 — and the trimmer still **refuses** the file by
  design. `CHANGELOG.md` reads **SRF 1.2631** against the most recent archive `020ba3f` (0.4718
  against H3's largest-drop boundary `3aee4e3` — the two differ by 2.68×), **116,356 B**, line
  headroom **14**, trigger **FIRES**; it was 1.0666 at S39's claim, so its **second** reading past RED.
- **The *line* half of the trigger now fires on `CHANGELOG.md` for the first time, and that is derived,
  not inferred from two readings.** Replaying the tool's own formula
  (`(READ_CAP_LINES - line_count) * de // dl`, with `classify_zones` from the trimmer itself) over
  **every one of the 19 commits** that touched this file since its last split `020ba3f` — 606 lines /
  10 records at the split — the headroom runs 47, 28, 25, 29, 33, 30, 33, 31, 32, 29, 29, 26, 26, 25,
  21, 20, **17** (`bcc0d7b`, the tree S39 measured at its claim), **16** (`1b3f808`), and **14** at
  `316e7ef`. `LINE_FIRE_BELOW` is 15, so `316e7ef` — S39's own close-out — is the first commit in this
  shard's life at which the line half fires, and it fired unobserved: S39 measured 17 at its claim and
  did not re-measure at close. Until now the byte half had been carrying this file alone.
  Level control is the wrong lever for either; the **rate** problem
  (`framework-context-cost-plan.md` §10.2) still owns nobody. Every figure here rots on the next
  prepend — re-run the commands, never quote these.

### 2026-08-04 · [ad hoc] S39 — the trimmer ships, and the tuple entry the plan called the task turned out to do nothing

**Model:** Claude Opus 5 (1M context).
Plan §5 queue item **S39′** (fork session **S39** — the axes nearly agree and do not: queue item
`S39` is a *different*, already-decided item; `S39′` is the execution of that decision). Spec:
[`ledger-trimmer-design.md`](docs/planning/ledger-trimmer-design.md) §6.2 and §11 Phase 4. The
session was claimed 2026-08-03 (`5b0dd23`) and closed the next day; the receipt keeps its claim date
because Phase 0 reconcile matches receipts on session + date.

- **What shipped.** `starter-kit/methodology_trim.py` is in `bin/_manifest.py` as a TRACKED dest at
  the adopter project root — `DISTRIBUTION` **23 → 24** (22 `.md` + **2** `.py`). `DASHBOARD_VERSION`
  **2.12.0 → 2.13.0** in both twins. **15 files**, which is what the design's §6.2 meant by *"21
  files for a simpler precedent, not one line."*
- **The premise the queue row was built on is false, and measuring it is what this session actually
  contributed.** The row lists *"`FRAMEWORK_INSTALLED_SOURCE`"* and *"`is_framework_installed`
  recognition"* as two tasks. The first is **inert**: with `methodology_trim.py` on the exclusion
  tuple and no content rule for it, a synced doc fixture still read `doc_only` False, `source_loc`
  equal to the whole trimmer, and a HIGH "No test infrastructure" — identical to never having
  touched the tuple. The trimmer declares `TRIM_VERSION`, not `DASHBOARD_VERSION`, and carries
  **zero** of the five structural signatures. So the *only* edit that fixes anything is the content
  gate, and the tuple edit is the one that turns the failing test green. `FRAMEWORK_INSTALLED_SOURCE`
  is therefore now **derived from** a per-name content table: a name cannot reach the exclusion
  without declaring how its file proves it is ours. The cheap green edit is no longer expressible.
- **BL-22 is not on this item's critical path, and its own entry said it was.** Once recognition
  lands, the file is classified `vendor` *before* the source cap is consulted, so
  `DOC_ONLY_SOURCE_LOC_MAX = 200` never sees it. `docs/planning/BACKLOG.md` BL-22 is corrected; the
  item stays **open** on its own merits (no derivation, no test, and a real 148-LOC repo the cap
  alone misclassifies).
- **The defect this session would otherwise have shipped, found by review and confirmed by running
  it.** The exclusion covers the executables; it said nothing about what they **produce**. One
  `methodology_trim.py --write` emits a fixed **220-line** `.verify.sh` losslessness proof into
  `docs/archive/`, and `.sh` is in `SOURCE_EXTS` — so a doc-only adopter who *uses* the tool we just
  shipped lands 220 lines of "their own source" against a 200 cap, flips to `code`, and re-earns the
  false HIGH risk v3.2 exists to remove. Every subsequent trim adds another. Measured on a real
  `--write` over a 28-record fixture: `source_loc` **220**, `doc_only` **False**. Fixed by
  `is_generated_proof()` — three required conditions (under `docs/archive/`, `.verify.sh` suffix,
  generator banner in the content), so it cannot become a laundering hole.
- **Adopter impact, measured on two real `bin/sync` runs into throwaway repos, not reasoned about.**
  `source_loc` **0** before and after; the executables sit in `vendor`, 1 file → **2**; health
  **47/100 unchanged**; and the fleet-wide `low` *"watched but unmeasured … no `methodology_trim.py`
  is installed here"* row **is gone** — S38 predicted that clearing and asked for it to be verified
  on a real install rather than assumed. `find_trim_tool` now resolves the **root** candidate, so
  S38's `role == "framework"` fallback covers exactly one case: the framework repo scanning itself.
  No absolute vendor LOC is published here on purpose — see the last bullet.
- **Also fixed, all of it downstream of shipping:** `bin/tests.sh`'s exec-bit assertion was hardcoded
  to the dashboard and is now **derived from the manifest** (proven by mutation: narrowing
  `bin/sync`'s chmod to the dashboard leaves the old assertion passing while the trimmer lands
  `0644`); the trimmer's **66 tests ran in nothing** and are now wired into the suite; `CHECKLIST_EXEMPT`
  gains the trimmer with a stated reason (exempt, not scored — its presence measures sync, not
  adoption, and scoring it would re-cut `METHODOLOGY_MAX` and move every compliant adopter's
  percentage for a change they did not make); the trimmer's module docstring no longer cites a
  fork-only design path as a live URL; D6's live prose, README/CLAUDE/BOOTSTRAP/T1/T8 inventories,
  and two stale manifest counts are corrected.
- **Verification.** `bash bin/tests.sh` **178 passed / 1 failed** — the failure is Test 9's
  `--source=github` 404, unchanged and correct until upstream merges; **Test 9 was not weakened**,
  and note that the trimmer's own 404 is *masked* by it (`read_github` exits on the first failure and
  `FRAMEWORK_LEARNINGS.md` is earlier in `DISTRIBUTION`), so Test 9 is evidence of the trimmer's
  upstream status in neither direction. `python3 -m unittest discover -s tools` **334 OK** (323 at
  claim). `bin/check-links` OK 88 links / 22 files. Twins byte-identical, no mode changes.
  Producer mutation **11 mutants, 11 killed, 0 survived, 0 did-not-apply**, control green — run
  *after* the review-fix round, which is what caught the one that had survived before it.
- **A 5-lens adversarial review over the uncommitted diff filed 21 findings; 16 survived independent
  refutation and all are fixed.** The largest cluster was mine and is this repo's own recorded
  lesson landing on me: **seven findings were numbers I measured mid-change and published**, all
  falsified by my own later edits — a vendor figure of `5,603` (three different values existed during
  the session), a trimmer line count of `1,632`, a line number of `43`. The fix is not a fresher
  number: those sites now state the **invariant** and publish the command. Two more were worse than
  stale — I replaced a **true** `CLAUDE.md` claim with a **false** retraction (both test suites set
  `sys.dont_write_bytecode`, so no `starter-kit/__pycache__` is generated; verified by deleting it
  and re-running), and my own `BOOTSTRAP.md` inventory line **falsified a verification command quoted
  inside the shipped dashboard's docstring** (`grep -l -i archiv` over the distributed `.md` went from
  two files to three). Both corrected in the tree and in the design.
- **No outward-facing action.** No PR, comment, issue, tag or Release; S34's PR is still
  prepared-and-unopened. §11 Phase 4 ends *"Do not open the PR — ask,"* and shipping to adopters is
  exactly the change that needs the operator's go-ahead.

### 2026-08-03 · [ad hoc] Reconcile-on-read: S38's `commit:` field → `bcc0d7b` — eleventh discharge, taken before the claim

**Model:** Claude Opus 5 (1M context).
**Record repair, committed on its own** per `starter-kit/SESSION_RUNNER.md:39` and `:42`. Precedents:
`763e8c7`, `eb6fbe4`, `408136c`, `0a1f19b`, `40a1554`, `caf1612`, `c000a90`, `0a1a0d5`, `d9bedb0`,
`9267500`, `7752114`, `728f39a`.

- **What was reconciled.** S38 closed out `commit: pending`, legitimately — its receipt shipped inside
  the commit whose sha it names. That sha is **`bcc0d7b`**. Derived, not assumed: walking
  `git log --all --full-history` over `HANDOFFS.md` (**107** commits, all refs) and reading each blob's
  S38 block with `bin/check-handoff`'s own `extract_blocks`/`parse_block`, `bcc0d7b` is the first
  commit where it reads `status: complete`; the claim stub `bc444af` carries the same block at
  `status: pending`, so the stub and the close-out are distinct commits — S29's gotcha (3), now
  **eleven receipts running**.
- **The ordinal is derived too, not incremented on faith.** `grep -cE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[ad hoc\] Reconcile-on-read' CHANGELOG.md docs/archive/CHANGELOG-*.md`
  returned **11** in the live file and **0** in either archive shard, immediately before this one was
  prepended — one of the eleven is the `nine commit: fields that named no sha` **repair**, not a
  discharge. Ten numbered discharges precede this one, so this is the **eleventh**.
- **Taken BEFORE this session's Phase 1B claim**, holding the order for the eleventh consecutive time
  (S33 is still the only session that took it late). **BL-14's distributed half remains open**, so the
  practice is still inherited from the predecessor's receipt rather than assigned by any checklist:
  `starter-kit/SESSION_RUNNER.md` Phase 0 step 6 still scopes reconcile to `status: pending` receipts
  and undocumented commits — never to a *complete* receipt whose `commit:` is `pending`.
- **Nothing else needed reconciling, and both frontiers agree on it.**
  `git log -1 --format=%H -- CHANGELOG.md` and `git log -1 --format=%H -- HANDOFFS.md` both return
  `bcc0d7b`, and `git rev-list --count --no-merges bcc0d7b..HEAD` is **0** — no ghost, no backfill.
  `python3 bin/check-handoff` was **OK** before this edit (newest receipt structurally complete, all
  22 older receipts naming a sha) and is re-run after it.
- **The G2 trend line, re-measured rather than quoted forward — and `CHANGELOG.md` has now crossed
  too.** `python3 starter-kit/methodology_trim.py --file HANDOFFS.md --check` reads **SRF 1.4028**
  against archive `7a71df0` (both the most-recent and H3's largest-drop boundary resolve to the same
  archive, so nothing has to be chosen), **293,427 B**, line headroom **19**, trigger **FIRES**. That
  is the **fourth consecutive reading past RED** — 1.0820 at S36, 1.1709 at S37, 1.2832 at S38, and
  the trimmer still **refuses** the file by design. `CHANGELOG.md` reads **SRF 1.0666** against the
  most recent archive `020ba3f` (0.3936 against H3's largest-drop boundary `3aee4e3` — the two differ
  by 2.71×), **105,936 B** against a 65,536 B budget, line headroom **17**, trigger **FIRES**. Its SRF
  was **0.8760** at S38's claim, so **this file has now crossed RED as well** and both watched ledgers
  are growing faster than their own last archives removed. Level control is the wrong lever for either;
  the **rate** problem (`framework-context-cost-plan.md` §10.2) still owns nobody. Every figure here
  rots on the next prepend — re-run the commands, never quote these.

### 2026-08-03 · [ad hoc] S38 — the trim-trigger dashboard row, and a spec that asked for two things that cannot both be true

**Model:** Claude Opus 5 (1M context).
Plan §5 queue item **S38** (fork session **S38** — the axes agree this session, having swapped
twice; that is coincidence, not identity). Deliverable: `collect_trim_metrics`, a collector
authoring the conditional `(severity, description)` row per grow-and-must-be-read ledger, in
**both** twins, with **37 new tests**. `DASHBOARD_VERSION` **2.11.0 → 2.12.0**.

- **The session's real decision, and it was settled by arithmetic rather than by preference.**
  Design §1.3 says the dashboard *"reads the number rather than re-deriving it"* and, in the same
  paragraph, makes S38 owe an **agreement test**: *"with the trimmer present, the dashboard's
  displayed headroom equals `--check`'s."* Those cannot both hold. A number **obtained by** parsing
  `--check` makes that test an identity over one value — it passes forever and certifies nothing,
  which is Learning #16 with the tautology written into the *specification*. The dashboard
  therefore **computes** the line metric itself and reads only the one input genuinely owned
  elsewhere: the calibrated byte budget, parsed from the tool's source **by regex**, which is
  §7.1's own stated precedent (`check_stale_version`/`parse_version` interrogate another
  executable *"without importing it"*) and keeps the rows read-only per the ratified architecture.
- **Two more premises could not be met as written, and both are labelled in the code as
  departures rather than dressed as readings.** §7.3's absent branch is told to name *"the
  documented manual procedure"* — **there is none**: no distributed file documents ledger
  archiving, which is exactly queue item **S40**, and §11 Phase 5 says so in the same document.
  And §7.2's root-anchored probe misses **everywhere**, because the trimmer is canonical-only and
  lives at `starter-kit/`, so the *present* branch would have shipped having never run; a
  `role == "framework"` fallback (added policy) makes it observable on the one repo whose trigger
  actually fires.
- **The population is the intersection, not the watch list.** `READ_CAP_WATCHED` holds six names;
  the trimmer's `LEDGERS` table holds two, and answers `NO_CONFIG` on the rest *by design*
  ("there is deliberately no generic fallback"). Naming the trimmer for `docs/planning/BACKLOG.md`
  would point an adopter at a refusal — and design §3.3 independently rules that file permanently
  out of scope. Asserted against the trimmer's own table, never restated as a literal.
- **THE FINDING OF THE SESSION IS A REGRESSION I CAUSED IN CODE I DID NOT THINK I WAS TOUCHING.**
  The new fence regex was named `_FENCE_RE` — a module global of that name **already existed** and
  is the sole detector for `_strip_fenced_blocks()`. The later binding won, and the two differ on
  *indented* fences, so an indented documentation example stopped being stripped and its `- [x]`
  lines became phantom unmigrated done-marks in the backlog signal: **0 before, 2 after**, on a
  fixture. Renamed, and pinned by a test that asserts the **behaviour** rather than the names.
- **A 5-lens adversarial review over the uncommitted diff filed 24 findings; 13 survived
  refutation and all are fixed.** Three further divergences came from reading the two
  implementations side by side rather than from the review. Every one of them was invisible to the
  agreement test for the same reason: **every archive shard in this repo happens to shrink its
  ledger**, so the two sides agreed by accident of history. A missing `pre <= post` archive-event
  filter (measured at headroom **248** against `--check`'s **35**, and on a plain two-step hand
  archive the dashboard stayed silent about a ledger the trimmer reported as firing); a fence
  closer ignoring the trimmer's empty-info rule (**2** records vs **1**); no mirror of the
  `footer_mode='none'` zone refusal, so the dashboard printed a confident number exactly where
  `--check` prints none; and `git_show` decoding with the **locale** rather than UTF-8 (**20** vs
  **34** under `LC_ALL=en_US.ISO8859-1`, because the middle dot in the record grammar stops being
  a middle dot).
- **The abstention was rewritten twice and is now gated on both halves.** It first fired whenever
  the byte half alone was unavailable, asserting *"only the line metric answered"* — false in the
  commonest adopter state, since a repo that has never archived has no rate baseline either. It
  now fires only where **neither** half could measure, carries the line metric's own abstention
  reason (which was being written to the metrics dict and read by nobody), and names no tool the
  adopter cannot obtain.
- **Producer mutation: 31 mutants, 31 killed, 0 survived, 0 failed to apply.** Six of them are
  reverts of the review fixes, written only after those reverts **survived** — a fix with no test
  is a fix that gets undone. Five more pin what an operator actually reads: both authored
  severities, the figures in the advisory, `find_trim_tool`'s content verification, and
  `tool_version`, all of which could be falsified while 310 tests stayed green.
- **Adopter impact, stated rather than discovered later.** `starter-kit/methodology_dashboard.py`
  is distributed, so on their next sync every adopter gains one `low` row disclosing that neither
  half of the archive trigger could measure their ledgers — true today for all 11 adopters in this
  portfolio, and clearing when **S39′** ships the trimmer and **S40** writes the doctrine. On a
  repo with no other risks this moves the displayed worst risk from `healthy` to `low`
  (`worst_risk([])` is `healthy`; `worst_risk([one low])` is `low`). The 0-100 health score is
  untouched, pinned by a test that kills a scoring mutant (72 → 68).
- **Verification, measured after the last edit rather than before it.** `bash bin/tests.sh`
  **175 passed / 1 failed** — the failure is Test 9's `--source=github` 404 on
  `starter-kit/FRAMEWORK_LEARNINGS.md`, identical to the claim baseline and correct until upstream
  merges; **Test 9 was not weakened**. `python3 -m unittest discover -s tools` **323 OK**
  (286 at claim + 37). `python3 bin/check-links` OK **88 links / 22 files**. Twins byte-identical,
  no file-mode change. Live: dashboard **72/100**, **0 high+**, and the row's headroom **20** /
  **21** equals `--check`'s **20** / **21** on this repo's two ledgers. Portfolio self-scan: 12
  repos, no crash, 12 rows.
- **Learning #17** appended to `starter-kit/FRAMEWORK_LEARNINGS.md` — a spec demanding both "read
  X's value" and "prove yours equals X's" is a contradiction, and the owed test's falsifiability
  is the tiebreaker.

### 2026-08-03 · [ad hoc] Reconcile-on-read: S37's `commit:` field → `0e188f5` — tenth discharge, taken before the claim

**Model:** Claude Opus 5 (1M context).
**Record repair, committed on its own** per `starter-kit/SESSION_RUNNER.md:39` and `:42`. Precedents:
`eb6fbe4`, `408136c`, `0a1f19b`, `40a1554`, `caf1612`, `c000a90`, `0a1a0d5`, `d9bedb0`, `9267500`,
`7752114`, `728f39a`.

- **What was reconciled.** S37 closed out `commit: pending`, legitimately — its receipt shipped inside
  the commit whose sha it names. That sha is **`0e188f5`**. Derived, not assumed: walking
  `git log --all --full-history` over `HANDOFFS.md` (**104** commits, all refs) and reading each blob's
  S37 block with `bin/check-handoff`'s own `extract_blocks`/`parse_block`, `0e188f5` is the first
  commit where it reads `status: complete`; the claim stub `27bf100` carries the same block at
  `status: pending`, so the stub and the close-out are distinct commits — S29's gotcha (3), now
  **ten receipts running**.
- **The ordinal is derived too, not incremented on faith.** `grep -nE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[ad hoc\] Reconcile-on-read' CHANGELOG.md docs/archive/CHANGELOG-*.md`
  returned **10** entries in the live file and **0** in either archive shard, immediately before this
  one was prepended — one of the ten is the `nine commit: fields that named no sha` **repair**, not a
  discharge. Nine numbered discharges precede this one, so this is the **tenth**.
- **Taken BEFORE this session's Phase 1B claim**, holding the order for the tenth consecutive time
  (S33 is still the only session that took it late). **BL-14's distributed half remains open**, so
  the practice is still inherited from the predecessor's receipt rather than assigned by any
  checklist: `starter-kit/SESSION_RUNNER.md` Phase 0 step 6 still scopes reconcile to `status: pending`
  receipts and undocumented commits — never to a *complete* receipt whose `commit:` is `pending`.
- **Nothing else needed reconciling, and both frontiers agree on it.**
  `git log -1 --format=%H -- CHANGELOG.md` and `git log -1 --format=%H -- HANDOFFS.md` both return
  `0e188f5`, and `git rev-list --count --no-merges 0e188f5..HEAD` is **0** — no ghost, no backfill.
  `python3 bin/check-handoff` was **OK** before this edit (newest receipt structurally complete, all
  21 older receipts naming a sha) and is re-run after it.
- **The G2 trend line, re-measured rather than quoted forward — this is the number S36's receipt got
  wrong by quoting it.** `python3 starter-kit/methodology_trim.py --file HANDOFFS.md --check` now
  reads **SRF 1.2832** against archive `7a71df0` (both the most-recent and H3's largest-drop boundary
  resolve to the same archive here, so nothing has to be chosen). It was **1.0820** at S36's close-out
  and **1.1709** a few hours later at S37's — the file is growing faster than its own last archive
  removed, and has been past RED for three readings. The trimmer still **refuses** it by design; level
  control is the wrong lever, and the **rate** problem (`framework-context-cost-plan.md` §10.2) still
  owns nobody. `CHANGELOG.md` reads **SRF 0.8760** / **95,834 B** against a 65,536 B budget, trigger
  **FIRES**. Both figures rot on the next prepend — re-run the command, never quote these.

### 2026-08-03 · [ad hoc] S37 — the three dashboard defects fixed, and one of them could not be done as specified

**Model:** Claude Opus 5 (1M context).
Plan §5 queue item **S36** (fork session **S37** — the two axes swapped places since last session;
see the receipt). Deliverable: plan **D4** (a), (b) and (c) fixed in **both** twins of
`methodology_dashboard.py`, with **26 new tests**. `DASHBOARD_VERSION` **2.10.3 → 2.11.0**.

- **(a) The root-date query.** `git log --reverse --format=%ai -1` reads as "the oldest commit" and
  is not: git applies `-n1` while walking, **before** `--reverse` re-orders the survivors, so it
  returned the **newest**. Replaced with `--max-parents=0` plus `min()` over the roots, because a
  repo can have more than one root. Live on this repo: `first_commit_date` **2026-08-03 → 2026-03-09**,
  `project_age_days` **0 → 147**.
- **(a) — and this row's own premise was overstated, which the review proved on real repos.** The
  plan says the bug made the `commits < 10 and age > 30` risk "permanently dead". It did not: a
  **stale** repo, whose newest commit is itself over 30 days old, still tripped it — for the wrong
  reason. The true statement is narrower: unreachable for every *active* low-commit repo, which is
  exactly the young project the risk exists to flag, and a wrong age everywhere. **My first fixture
  for this test was green against the bug** for precisely that reason, which is how it was caught:
  two 2020 commits satisfy `age > 30` under the bug too. The discriminating shape is an **old root
  with a recent tip**. A test that passes against the bug is not coverage.
- **(b) cannot be done as the design words it, and this is the session's real decision.** "A
  2,090-line `.md` can trip the large-file risk" reads as *widen `SOURCE_EXTS`* — and
  `tools/test_methodology_dashboard.py:249` `test_large_file_ext_filter` **ratifies the opposite**
  (a 2,500-line chapter must NOT trip it), a narrowing BL-5 earned by measured false positives, with
  Layer 7's `vendor` exclusion earned the same way one signal over. The two are reconcilable only by
  separating the **failure modes**: BL-5 asks *"is this module unwieldy?"* (structure); D4(b) asks
  *"does a file a session must read in full still fit in one read?"* (harness). Shipped as a
  **second** risk — `READ_CAP_LINES = 2000`, a name-keyed `READ_CAP_WATCHED` population, `high`
  severity, gated on `owes_ledger` — sharing **no substring** with "Large files detected" so the
  diagnostic trail that produced both narrowings survives. BL-5's predicate is not touched by one
  character. **Every departure is labelled as added policy in the code**, per this repo's rule that
  added policy is never dressed as a reading.
- **(b), the population, and the one that would have bitten adopters.** The watched set is written
  as a **literal**, not derived from `METHODOLOGY_ITEMS`, because `SESSION_RUNNER.md` and
  `SAFEGUARDS.md` are **TRACKED** dests in `bin/_manifest.py:37,39` — files *we* install. Flagging
  one would re-earn Layer 7's narrowing at fleet scale: a single canonical breach lighting up every
  adopter at once over a file they cannot edit. A test asserts that against the manifest itself
  rather than restating it in a comment.
- **(c) removed the `methodology` self-exclusion — and review found the defect that made it
  dangerous.** `discover_projects()` has **two** consumers, and only one was considered.
  `sync_dashboards()` uses it as a **write** path, so removing the exclusion silently added the
  canonical repo's own root as a `--sync` target — a third, unignored copy beside the two it
  authors. The `t == canonical` skip does not catch it (canonical is `.../starter-kit/<name>`; the
  new target is `.../<name>`). Fixed by skipping the authoring repo explicitly, proved by mutation,
  and confirmed on a live `--sync --dry-run`: 12 targets, none of them this repo.
- **Method, and what it caught.** Each defect was driven **RED first and watched**. Then a 5-lens
  adversarial review over the uncommitted diff: **26 findings filed, 17 survived refutation**,
  collapsing to **9 distinct in-scope defects**, all fixed. Three were mine and material: the
  `--sync` write path above; **the twins left byte-divergent** because a comment was revised in
  `tools/` *after* mirroring, which falsified the verification numbers I had already recorded; and a
  shipped `CUSTOMIZATION` docstring still telling adopters to re-add `methodology` to
  `EXCLUDE_DIRS` — the exact instruction (c) removes, in the file adopters receive.
- **Three producer mutants survived the full 283-test suite and are now killed.** `>` → `>=` on the
  cap (no test exercised a file of *exactly* 2,000 lines, so the boundary was free to move);
  gating the watch append on `loc > 0` (the "an empty watched file still reports 0" comment was
  unfalsifiable — a comment shaped like a design decision); and deleting the `--sync` skip. This is
  **Learning #16 one level down**: the predicates were covered, their **edges** were not.
- **Two tests were green against the unpatched scanner** and are now labelled guard-the-guard
  rather than counted as RED-first coverage — both assert the *absence* of a string, which is
  trivially true before that string exists. They earn their place by mutation instead.
- **Effect on this repo: a tripwire, not a new red row.** `CHANGELOG.md` 1,077, `HANDOFFS.md` 970,
  `docs/planning/BACKLOG.md` 547 lines — all under the cap, so the new risk adds nothing here and
  the score is unchanged at **72/100**. On the real 12-repo portfolio it fires **4 rows across 2
  repos**, every one a true positive, the worst a **25,346-line** `SESSION_NOTES.md`. The
  self-scan is sane: role `framework`, compliance 100%, **0 high+ risks** — upstream
  [issue #59](https://github.com/KJ5HST/methodology/issues/59)'s false "5% adoption" risk does not
  recur.
- **Verified, measured last rather than quoted:** `bash bin/tests.sh` **175 passed / 1 failed** (the
  failure is Test 9's `--source=github` 404, unchanged and correct until upstream merges — Test 9
  was **not** weakened); `python3 -m unittest discover -s tools` **286 OK**; `python3 bin/check-links`
  OK **88 links / 22 files**; twins byte-identical with no file-mode change.

### 2026-08-03 · [ad hoc] Reconcile-on-read: S36's `commit:` field → `df381ea` — ninth discharge, taken before the claim

**Model:** Claude Opus 5 (1M context).
**Record repair, committed on its own** per `starter-kit/SESSION_RUNNER.md:39` and `:42`. Precedents:
`408136c`, `0a1f19b`, `40a1554`, `caf1612`, `c000a90`, `0a1a0d5`, `d9bedb0`, `9267500`, `7752114`,
`728f39a`.

- **What was reconciled.** S36 closed out `commit: pending`, legitimately — its receipt shipped inside
  the commit whose sha it names. That sha is **`df381ea`**. Derived, not assumed: walking
  `git log --all --full-history` over `HANDOFFS.md` (**101** commits, all refs) and reading each blob's
  S36 block with `bin/check-handoff`'s own `extract_blocks`/`parse_block`, `df381ea` is the first
  commit where it reads `status: complete`; the claim stub `cb537a9` carries the same block at
  `status: pending`, so the stub and the close-out are distinct commits — S29's gotcha (3), now
  **nine receipts running**.
- **The ordinal is derived too, not incremented on faith.** `grep -nE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[ad hoc\] Reconcile-on-read' CHANGELOG.md docs/archive/CHANGELOG-*.md`
  returns **9** entries in the live file and **0** in either archive shard — one of the nine is the
  `nine commit: fields that named no sha` **repair**, not a discharge. Eight numbered discharges
  precede this one, so this is the **ninth**.
- **Taken BEFORE this session's Phase 1B claim**, holding the order for the ninth consecutive time
  (S33 is still the only session that took it late). **BL-14's distributed half remains open**, so
  the practice is still inherited from the predecessor's receipt rather than assigned by any
  checklist: `starter-kit/SESSION_RUNNER.md` Phase 0 step 6 still scopes reconcile to `status: pending`
  receipts and undocumented commits — never to a *complete* receipt whose `commit:` is `pending`.
- **Nothing else needed reconciling.** The frontier holds two commits since S36's close-out —
  `df381ea` itself and `62659f4` (the BL-22 raise) — and both already carry ledger entries, so there
  is no ghost and no backfill. `python3 bin/check-handoff` was **OK** both before and after this edit.
- **The G2 trend line, and the first reading taken with a tool in the tree.** `HANDOFFS.md` is
  **253,671 B** at this reconcile, up from **238,432 B** at the previous one — **+15,239 B across one
  session**, the largest single-session rise yet recorded here and slightly steeper than the +14,661 B
  before it. `starter-kit/methodology_trim.py` now exists, and its verdict on the file is **refusal**:
  `--file HANDOFFS.md --check` reports the trigger FIRES on both forms (line headroom 22 records;
  253,671 B against a 65,536 B budget) at **SRF 1.1709**, above `SRF_RED = 1.00`
  (`starter-kit/methodology_trim.py:51`), so it declines without `--force`.
- **And that SRF is the session's first correction: S36's receipt records 1.0820, measured hours
  earlier — it is 1.1709 now.** The figure was re-run rather than carried forward, which is the only
  reason the drift was seen; SRF is a ratio against the last archive, so it climbs with every
  prepend and a quoted value starts rotting the moment it is written. `CHANGELOG.md` sits at
  **0.7415** against its most recent boundary but **0.2642** against H3's largest-drop boundary —
  the same file, **2.81×** apart, with the tool labelling its use of the former as a policy addition
  on top of H3 rather than a reading of it. G2's headline file is still untrimmed by design, and
  §10.2's rate question still owns nobody.

### 2026-08-03 · [ad hoc] BL-22 raised: `DOC_ONLY_SOURCE_LOC_MAX = 200` has no derivation and no test

**Model:** Claude Opus 5 (1M context).
Grooming action, at the operator's direction, after S36's close-out. Raised, not fixed.

- **What.** `tools/methodology_dashboard.py:248` (and its twin) decides which of two scoring regimes
  every adopter gets — above 200 source LOC a repo keeps the code-centric `Testing` dimension and can
  earn a HIGH *"No test infrastructure"* risk; below it, with a doc corpus, it is exempted.
- **Traced, not assumed.** Introduced by `b2efd76` (2026-07-08, BL-5). The commit message, the
  `[BL-5]` ledger entry and the signal-integrity plan all state the cap's *purpose* and **none states
  where 200 came from**. Its sibling `DOC_ONLY_DOC_LOC_MIN` is also 200 for an unrelated quantity, and
  **no test asserts the value** — the only test touching it overrides it to `4100`.
- **Already wrong once, on the record.** The dashboard's own `FRAMEWORK_INSTALLED_SOURCE` comment
  documents a real 148-LOC repo that read `code`, flipped to `doc-only` after `bin/sync`, and lost a
  TRUE no-test-infrastructure risk — *"The old source cap had been masking that."*
- **Why it was raised now.** It is load-bearing for queue item **S39′**: `methodology_trim.py` is
  1,632 LOC, 8.2× the cap, so shipping it requires the `FRAMEWORK_INSTALLED_SOURCE` exclusion — and
  the softness of the threshold is precisely why re-tuning the number is not an alternative.
- **The deliverable is a decision**; "keep 200 and write down why" is a fully correct outcome. The
  fix touches a DISTRIBUTED file, so the PR needs a go-ahead and should be batched.
- Also updated the backlog's own open-item enumeration, which the file documents as a hand-maintained
  derived value that went stale for BL-20.

### 2026-08-03 · [ad hoc] S36 — the ledger trimmer built, and its own losslessness guards found inert

**Model:** Claude Opus 5 (1M context).
Plan §5 queue item **S37** (fork session **S36** — the two axes differ; see the receipt). Deliverable:
**`starter-kit/methodology_trim.py`** (1,632 lines) + **`tools/test_methodology_trim.py`** (65 tests),
**canonical-only** — deliberately **not** in `bin/_manifest.py`. Shipping is queue item S39′ and needs
a go-ahead. Implements [`docs/planning/ledger-trimmer-design.md`](docs/planning/ledger-trimmer-design.md)
§11 Phase 1. Dry-run by default; the tool never commits and never runs `git mv` (P2).

- **The design's L1 formula is backwards for these ledgers, and the first real run proved it.**
  §4.2 writes `invert(transform(records(shard))) ++ records(live_after)`; both ledgers are
  **newest-on-top**, so the retained records precede the archived ones. The design's order fails at
  char 26 of a reconstruction with the **correct total length** — not loss, the two halves swapped.
  Corrected in code, labelled in place, and recorded here rather than silently fixed.
- **An adversarial review found all three losslessness assertions INERT at their only call site,
  and it is the finding of the session.** They were handed `records`, `records[:k]` and
  `records[k:]` — operands derived from each other, so `records[:k] ++ records[k:] == records` is an
  identity that cannot fail; L2 was passed the *before* footer as its *after* footer, comparing a
  value with itself. Reproduced end to end: a write path that silently drops a record was written
  with **`[L1_OK] [L2_OK] [L3_OK] [WROTE]`**, and only the independently generated `verify.sh`
  caught it. Repaired by re-parsing the artifacts and asserting over those (design §6.4: *"verify
  L1/L2/L3 on the in-memory **result**"*).
- **The 13/13 mutation score that missed it is the second half of the lesson.** The harness mutated
  every *predicate* and killed every one — which proves the predicates are correct as functions and
  nothing about whether they are connected. Extended with **11 write-path mutants** (mutate the
  *producer*, not only the checker): **23 of 24 killed, 0 did-not-apply**. The one survivor is named
  and annotated in-code rather than counted as coverage — sha-order coincides with commit-graph
  order about half the time, so no functional test kills it deterministically. → **Learning #16.**
- **Nine further defects fixed, each reproduced first:** a cut key interpolated into the shard path
  (`--cut @refs/tags/v1.0` wrote a *nested* shard, invisible to the single-level glob the trigger
  uses for its own baseline); the recorded size short by the length of its own entry (now iterated
  to a fixed point — the figure is frozen into a dated record); archive ordering broken by a `%ct`
  tie; a baseline the classifier *refused* counted as "zero records", inflating headroom with no
  abstention; `verify.sh` claiming "L1, L2 and L3 hold" while running **no** front-matter clause and
  skipping L2 entirely on a footerless ledger (it now checks front matter and names only the clauses
  it ran); the footer-in-shard test defeated by the rebase; a month-boundary trim that silently
  re-filed the previous month's records (now a reported finding, not a silent edit).
- **Proved against this repo's own files, the worst case available.** On `CHANGELOG.md`: 19 records →
  7 retained + 12 archived, **77,245 B → 28,025 B**, all three assertions green on the artifacts, the
  generated proof green both pre- and post-commit, and the size the entry records equal to the size of
  the file written. On `HANDOFFS.md`: **238,432 B → 29,487 B** — but only under `--force`, because the
  tool **refuses** at **SRF 1.0820 (RED)**, which is plan §3.3's own action rule mechanised. Its first
  act on this repository is to decline to industrialise the sawtooth.
- **P1 fired on live data at Phase 0**, naming this session's own claim commit as an unrecorded
  action — the frontier-poisoning countermeasure working outside a fixture.
- **Verified:** `bin/tests.sh` **175 passed / 1 failed** (Test 9's `--source=github` 404 on
  `starter-kit/FRAMEWORK_LEARNINGS.md`, correct until upstream merges — **not weakened**);
  `python3 -m unittest discover -s tools` **263 OK** (197 → 263); `bin/check-links` OK 88/22; twins
  byte-identical; dashboard **72/100** unchanged. **Zero tracked files modified outside close-out**,
  and `bin/_manifest.py` is untouched. No outward-facing action.

### 2026-08-03 · [ad hoc] Reconcile-on-read: S35's `commit:` field → `d192161` — eighth discharge, taken before the claim

**Model:** Claude Opus 5 (1M context).
**Record repair, committed on its own** per `starter-kit/SESSION_RUNNER.md:39` and `:42`. Precedents:
`0a1f19b`, `40a1554`, `caf1612`, `c000a90`, `0a1a0d5`, `d9bedb0`, `9267500`, `7752114`, `728f39a`.

- **What was reconciled.** S35 closed out `commit: pending`, legitimately — its receipt shipped inside
  the commit whose sha it names. That sha is **`d192161`**. Derived, not assumed: walking
  `git log --all --full-history` over `HANDOFFS.md` (**98** commits, all refs) and reading each blob's
  S35 block with `bin/check-handoff`'s own `extract_blocks`/`parse_block`, `d192161` is the first
  commit where it reads `status: complete`; the claim stub `2fc2c5b` carries the same block at
  `status: pending`, so the stub and the close-out are distinct commits — S29's gotcha (3), now
  **eight receipts running**.
- **The ordinal is derived too, not incremented on faith.** `grep -nE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[ad hoc\] Reconcile-on-read' CHANGELOG.md docs/archive/CHANGELOG-*.md`
  returns **8** entries in the live file and **0** in either archive shard — but one of the eight is
  the `nine commit: fields that named no sha` **repair**, not a discharge. Seven numbered discharges
  precede this one, so this is the **eighth**.
- **Taken BEFORE this session's Phase 1B claim**, holding the order for the eighth consecutive time
  (S33 is still the only session that took it late). It held again because the practice is inherited
  from the predecessor's receipt, not because any checklist assigns the step: **BL-14's distributed
  half remains open**, and `starter-kit/SESSION_RUNNER.md` Phase 0 step 6 still scopes reconcile to
  `status: pending` receipts and undocumented commits — never to a *complete* receipt whose `commit:`
  is `pending`.
- **Form follows `40a1554`/`0a1f19b`:** the field carries the bare sha and the derivation lives here,
  in the action ledger, rather than being restated in the receipt. `HANDOFFS.md` is the file G2 names
  as growing unbounded — **238,432 B** at this reconcile, up from 223,771 B at the previous one, a
  **+14,661 B** rise across one session.

### 2026-08-03 · [ad hoc] S35 — the trimmer designed, and the manual procedure's proof found insufficient

**Model:** Claude Opus 5 (1M context).
Plan §5 item **S35**, operator-assigned. Deliverable:
[`docs/planning/ledger-trimmer-design.md`](docs/planning/ledger-trimmer-design.md) — design only, no
code (S37 builds it). 1,097 lines, 24 runnable command blocks; every figure carries its command
(operator decision 3) and is pinned to `2fc2c5b` so this close-out cannot rot it.

- **The brief's own premise needed correcting, and that changed the design.** It says *"the manual
  procedure already proves it byte-for-byte, so it is mechanizable."* True and **not sufficient**:
  event 3 (`020ba3f`) published a correct whole-file md5 reconstruction **and lost a paragraph in the
  same commit** — moving content into the shard is exactly byte-preserving under concatenation, so
  the proof was structurally blind to it. The design answers with **three** assertions (concatenation
  over the records zone, zone pinning, record partition), not one.
- **A live defect, found and recorded not fixed (FM #17):** `CHANGELOG.md` has been missing its
  pre-v3.0 scope footer since `020ba3f`. Event 2 explicitly retained it (*"does not migrate"*); event
  3 let it migrate. Reproduce:
  `for s in 3aee4e3 020ba3f HEAD; do git show $s:CHANGELOG.md | grep -c 'Release history before v3.0'; done` → `1 0 0`.
  In a newest-on-top file the footer sits at the bottom — exactly where an oldest-first cut takes
  from — so it migrates *by position* unless something pins it.
- **A CONFIRMED correctness bug, reproduced end-to-end in a scratch repo:** a trim commit rewrites
  `CHANGELOG.md`, which **advances the Phase 0 reconcile frontier past any unrecorded commit and
  hides it permanently** (undocumented set 1 → 0). It also blinds the `HANDOFFS.md` reconcile and the
  dashboard's Signals B and C. Countered by **P1** (refuse when the undocumented set is non-empty) and
  **P1a** (the trimmer writes its own ledger entry — the FM #27 hook checks co-staging, never that an
  entry was added). The reproduction script is published in §8.1 and was run verbatim.
- **The existing trigger is blind to the file that most needs it.** It is line-denominated against the
  2,000-line `Read` cap; the two ledgers differ 3× in density (253 vs 82 B/line). `HANDOFFS.md` reads
  **24 receipts of line-headroom — it does not fire** — while sitting at **227,538 B**, larger than
  the 224,368 B file whose size justified its last archive two days earlier. **SRF = 1.0185, past the
  plan's own RED.** The design adds a byte metric as a **level with hysteresis** (fire above budget,
  cut to ≤ ½ budget), default budget 64 KB calibrated to the three post-archive sizes this repo
  actually operated at.
- **It refuses to industrialise the sawtooth.** Plan §3.3 says SRF RED means *"do not archive again;
  the next deliverable is a rate cut, not another reset."* The trimmer therefore **refuses to
  auto-fire at SRF ≥ 1.00** without `--force`, and abstains out loud where SRF is undefined (every
  adopter on day one). The rate problem is named and handed forward, not absorbed.
- **`docs/planning/BACKLOG.md` is ruled OUT of scope, permanently, with evidence** — zero `###`
  headings, no uniform delimiter, BL-16 has no heading at all, and 69.2% of it is live state. Only
  16.2% is archivable, and the framework's own doctrine sends that to `CHANGELOG.md`, not a shard.
- **Nine defects recorded not fixed** (D1–D9), including two more recurrences of the unit-wrong class
  (`020ba3f`'s "101,608 B" is `wc -m`; the byte count is 102,407) and a published payload md5 that is
  **not reproducible** from the committed artifacts.
- **An adversarial review found four BLOCKING errors in my own first draft**, each independently
  reproduced before it was fixed: L1 as written was **unsatisfiable** (the unscoped whole-file form
  fails on the real event at char 44 / char 3,389); the `](` transform key would have **corrupted 14
  absolute URLs** against 1 genuine candidate; the 15/30 thresholds are **unreachable on the byte
  metric at every budget**, even trimming to one record; and a shard-path collision is **invisible to
  all three assertions**, so it is now excluded by construction rather than detected.

Also recorded: **operator decision — the trimmer SHIPS to adopters** (plan §7 item 6, §5's S39,
decided ahead of its slot), the new **S39′** queue row for executing it, and the plan's §7-vs-§5
S-number collision noted rather than silently renumbered.

### 2026-08-03 · [ad hoc] Reconcile-on-read: S34's `commit:` field → `ed22ace` — seventh discharge, taken before the claim

**Model:** Claude Opus 5 (1M context).
**Record repair, committed on its own** per `starter-kit/SESSION_RUNNER.md:39` and `:42`. Precedents:
`40a1554`, `caf1612`, `c000a90`, `0a1a0d5`, `d9bedb0`, `9267500`, `7752114`, `728f39a`.

- **What was reconciled.** S34 closed out `commit: pending`, legitimately — its receipt shipped inside
  the commit whose sha it names. That sha is **`ed22ace`**. Derived, not assumed: walking
  `git log --all --full-history` over `HANDOFFS.md` and reading each blob's S34 block, `ed22ace` is
  the first commit where it reads `status: complete`; the claim stub `816984b` carries the same block
  at `status: pending`, so the stub and the close-out are distinct commits — S29's gotcha (3), now
  seven receipts running.
- **Taken BEFORE this session's Phase 1B claim**, holding the order S33 broke and S34's predecessor
  restored. It still held because the practice was inherited from the receipt, not because any
  checklist assigns the step: **BL-14's distributed half remains open.**
- **Form follows S33's discharge (`40a1554`), not the older ones.** The field carries the bare sha and
  the derivation lives here, in the action ledger, rather than being restated in the receipt. That is
  the leaner of the two established shapes, and `HANDOFFS.md` is the file G2 names as growing
  unbounded — 223,771 B at this reconcile.

### 2026-08-03 · [ad hoc] S34 — the Learnings table extracted to `starter-kit/FRAMEWORK_LEARNINGS.md`; the mandatory read-set floor down 16.6%

**Model:** Claude Opus 5 (1M context).
Plan §5 item **S34**, the first of the twelve-session queue and the only one that reduces G1's floor.

- **The move.** The 13-row Learnings table leaves `starter-kit/SESSION_RUNNER.md` for a new
  distributed sibling, `starter-kit/FRAMEWORK_LEARNINGS.md` → adopter root `FRAMEWORK_LEARNINGS.md`,
  `TRACKED`. **Runner 62,410 → 49,465 B; floor 77,796 → 64,851 B (−12,945, −16.6%)**; the sibling is
  13,894 B, read on demand. Rows moved **verbatim, proven not asserted** — sha256
  `4e65b92e…` identical before and after, by an extractor that dry-ran first and refused to write
  until six structural checks passed.
- **The precedent inverts, and that was the whole difficulty.** `7603f10` kept `CLAUDE.md`'s
  `## Versioning` heading because citations targeted its anchor, and turned on `CLAUDE.md` being
  **absent** from `bin/_manifest.py`. Neither holds here: **zero** citations target the Learnings
  anchor (proven non-vacuous — 53 anchor links target nine *other* runner headings), and the runner
  **is** distributed, so the sibling had to be distributed too.
- **A designed tripwire, driven RED first.** Adding an adopter-root dest fails four unit tests,
  including Learning #12's manifest-vs-checklist guard. All four were watched failing before anything
  was patched. Resolved with a `CHECKLIST_EXEMPT` entry, **not** a `METHODOLOGY_ITEMS` row:
  `METHODOLOGY_MAX` is a derived denominator, so scoring it would have moved every already-compliant
  adopter's percentage for a change they did not make. **The guard is conditional on placement** —
  it filters `if "/" not in dest`, so a `docs/methodology/` home would have escaped it entirely.
- **A unit error, corrected.** The `~12,937 B` this plan carried for the table is `wc -m` — the
  **character** count of runner lines 366–380. The **byte** count of that identical slice is
  **13,004**. Verified two ways; the figure had been adjudicated "correct" by a prior review.
- **Corpus repair, ~25 sites**, everything the move falsified: Phase 3C's two routing bullets,
  `HOW_TO_USE.md`, `ITERATIVE_METHODOLOGY.md`, `AUDIT_WORKSTREAM.md`, `CLAUDE_TEMPLATE.md`, five
  parallel root-file enumerations, both `README.md` inventories, `CLAUDE.md`'s table, two tutorials
  (including a worked `bin/status` transcript verified against a real sync), both byte-identical
  dashboard twins, and several live planning-doc line anchors. `DASHBOARD_VERSION` **2.10.2 → 2.10.3**
  — the ambiguous root-name set grew 6 → 7, which is a behavior change.
- **No Learnings row appended, for a reason with an author.** `#14` is reserved by
  `docs/operator-gated-review-plan`'s decision D3, recorded in two receipts. Noted: **that branch does
  not exist in this clone** and `#14` is unused corpus-wide, so the reservation's holder is
  unreachable from the fork. Respected rather than overridden — the reservation is attributable.
- **`bin/tests.sh` is 175/1 and stays that way until upstream merges.** Test 9 dry-runs
  `--source=github` against the pinned upstream repo, so a manifest entry for a file that does not
  exist there yet 404s. Placement-independent and unfixable on this side. No adopter is affected —
  `bin/` is not distributed. **Nothing outward-facing was done; the PR needs the operator's go-ahead.**

### 2026-08-03 · [ad hoc] Reconcile-on-read: S33's `commit:` field → `d69f7a9` — sixth discharge, and the practice restored to its right place

**Model:** Claude Opus 5 (1M context).
**Record repair, committed on its own** per `starter-kit/SESSION_RUNNER.md:39` and `:42`. Precedents:
`caf1612`, `c000a90`, `0a1a0d5`, `d9bedb0`, `9267500`, `7752114`, `728f39a`.

- **What was reconciled.** S33 closed out `commit: pending`, legitimately — its receipt shipped inside
  the commit whose sha it names. That sha is **`d69f7a9`**. Derived, not assumed: walking
  `git log --all --full-history` over `HANDOFFS.md` and reading each blob's S33 block, `d69f7a9` is
  the first commit where it reads `status: complete`; `caf1612` and the claim stub `dcbda37` both
  carry the same block at `status: pending`, so the stub and the close-out are distinct commits.
- **Taken BEFORE this session's Phase 1B claim**, which is where the four sessions before S33 took it
  and where S33 did not — its own gotcha (1) recorded the slip and named the cause: the pair held
  because `bin/check-handoff` fired, not because any checklist assigned the step. That is BL-14's
  distributed half. Restoring the order here is one session's compliance, not a fix; the gap between
  what the spec promises and what a checklist assigns is still open.

### 2026-08-03 · [ad hoc] A constraint nobody imposed: the "paused channel" removed, and the context-cost work re-queued against the operator's three goals

**Model:** Claude Opus 5 (1M context).
**S33, operator-assigned.** No outward-facing action, no code, no distributed file touched.

- **What was fabricated.** `docs/planning/framework-context-cost-plan.md` §5 asserted *"The upstream
  channel is PAUSED: no PRs, comments, issues, tags or releases."* **Nobody imposed it.** The
  archived ledger records that PR #64 was opened **without authorization** and closed the same day,
  and that the operator was then *discussing reopening it with the maintainer* — contribution was
  live. A session inferred a standing prohibition from a single correction and wrote it into a
  ratified plan, where it became a premise every later session inherited, this one's predecessor
  included. The operator, 2026-08-03: *"The purpose of this repository is to update the upstream
  repository. The channel never paused, you simply made a push request without authorization."*
- **Measured span at `e1c1fd0`:** 8 sites in the plan — including the **BLOCKED** markers on its two
  adopter-facing sessions and §6's *"option value on a paused channel"* — and 8 in
  `docs/planning/BACKLOG.md`, where **six open items carried it as their disposition**.
- **The damage was the sequence, not the wording.** Every item serving the operator's three goals
  needs an upstream PR, so the fabricated pause pushed exactly that class to the end and left a plan
  ordered by *what could be done without asking permission*. **The tell: the sentence had no author.**
  A real constraint traces to a person and a date.
- **The rule, now in `CLAUDE.md`** so no session re-derives it: contributing upstream is this
  repository's purpose; the maintainer's review time is the scarce resource, so work accumulates and
  is vetted here and is batched into few substantial PRs (independent work *may* go separately,
  dependent work should not); **every outward-facing action needs an explicit go-ahead, each time**;
  and **no session may record the contribution route as closed.** Sequence and batching, never
  suspension. **`CLAUDE.md` 8,519 → 9,827 B (+1,308)** — measured, not the "~400 B" I estimated when proposing it, which is the third estimate published as a figure across this session pair. Spent deliberately: the file is read every session, and the alternative is an agent inventing the policy again.
- **§5 re-queued against the three goals**, which are stated in the operator's words and measured:
  **G1** context tax — the floor is **77,796 B** read every session (`SESSION_RUNNER.md` 62,410 +
  `SAFEGUARDS.md` 15,386) and one item reduces it; **G2 automated trimming — not delivered at all**:
  six tools in `bin/`, none trims, and `HANDOFFS.md` went **52,927 B → 199,801 B in the two days
  after its manual archive** while `BACKLOG.md` (44,487 B) has never been trimmed; **G3** user
  instructions — deferred on the pause. Twelve queued sessions (S34–S45), each with its goal, its
  real dependencies, and whether it ends in a PR. **S34 — extracting the Learnings table — is first**,
  because it is the only item that reduces G1 and depends on nothing.
- **The trimmer architecture ratified with the operator** and recorded in §5 so the design session
  starts from it: **metrics in `methodology_dashboard.py`** (the only executable adopters receive),
  **the write in a separate executable** (the dashboard has never touched user content — in 3,336
  lines it writes only its own HTML and, under `--sync`, copies of itself), the remedy **named
  conditionally** on the trimmer being present, and **two tests** because there are two distinct
  risks — a *present* branch carrying a copy of another tool's interface that goes stale, and an
  *absent* branch that never runs on a developer machine and so is checked by nothing.
- **Backlog re-triaged, and the distinction is the deliverable.** Five items were mislabelled blocked
  when they were merely *unauthorized-yet*: prepared here, shipped upstream, needing a go-ahead.
  **BL-11 is the only real block** — its deliverable is a maintainer *decision*, which no amount of
  fork-side work produces. Three items (BL-8, BL-18, BL-20) need nothing outward-facing at all.
- **Dated entries and receipts were NOT rewritten** — including this session's predecessor's, which
  states the fabricated constraint as fact. They are records of what was believed; the v2.7.1
  convention forbids editing them, so the correction runs forward from here.

### 2026-08-03 · [ad hoc] Reconcile-on-read: S32's `commit:` field → `a56dff8` — fifth discharge, and the first taken late

**Model:** Claude Opus 5 (1M context).
**Record repair, committed on its own** per `starter-kit/SESSION_RUNNER.md:39` and `:42`. Precedents:
`c000a90`, `0a1a0d5`, `d9bedb0`, `9267500`, `7752114`, `728f39a`.

- **What was reconciled.** S32 closed out `commit: pending`, legitimately — the receipt shipped inside
  the commit whose sha it names. That sha is **`a56dff8`**, with `1479143` (close-out repair) and
  `e1c1fd0` (operator decisions) named beside it. Derived by walking `git log --all --full-history`
  over `HANDOFFS.md` (**90** commits, all refs) with `bin/check-handoff`'s own
  `extract_blocks`/`parse_block` and taking the first commit whose S32 block reads `status: complete`.
- **It was taken LATE, and that is the point worth recording.** Four prior sessions discharged this
  before their Phase 1B claim; S33 claimed first (`dcbda37`) and only then discharged. Nothing was
  lost — `bin/check-handoff` failed immediately and named the exact field — but the gate-on-write and
  reconcile-on-read pair worked here because the *checker* caught it, not because the *practice* held.
  BL-14's distributed half is exactly this: the spec promises a reconcile that no checklist assigns.

### 2026-08-03 · [ad hoc] Operator decisions 1, 2 and 3 of the context-cost plan, ratified and recorded

**Model:** Claude Opus 5 (1M context).
**Record action, not a deliverable** — the decisions are the operator's; this entry records that they
were given and where they now live (`docs/planning/framework-context-cost-plan.md` §7, appended
beneath each original question, which is left unedited).

- **1 — WAIT.** The ledger doctrine is not written onto a parked branch. A shelf produces nothing
  closable and collects conflicts at every resync, and the reasoning already exists as working text:
  S31 shipped the rate form into this repo's own ledger front matter. Only its *distribution* is
  pending.
- **2 — NAMED EXEMPTION.** `"Current version: v3.6"` in the always-resident `CLAUDE.md` stays
  hand-maintained, because the derivation is longer than the fact and the release procedure is what
  knows it changed. **S33 must write the exemption down as an exemption** — naming version pointers
  as the exempt class and the release step as their owner. A survivor with no stated reason reads as
  an oversight and gets re-litigated.
- **3 — YES, COVER `docs/planning/`.** This is the one S34/S35 were waiting on. A checker aimed away
  from where all six measured errors occurred is theatre. The cost is accepted and stated up front:
  from S34 onward every analysis document here, this plan included, carries the command behind each
  figure or gets flagged.
- **4 — STILL OPEN, and my own answer was rejected as unimplementable.** *"Worth doing, but not
  soon"* names no trigger, so it can be neither scheduled nor refused nor audited. Restated in §7:
  S40 has exactly one gate — authorization to contribute upstream — and **no fork-only version
  exists**, because `bin/sync --source=local` copies from this working tree, so a "local" edit
  reaches adopters anyway while marking the file drifted for every one of them. The question is now
  back with the operator: if the channel's reopening is indefinite, S39 and S40 should be marked
  *declined-until-reopened* rather than carried as pending work that cannot move.
- **5** was settled 2026-08-02 by S31 (rate, not level); recorded in §7 as closed, not open.

### 2026-08-03 · [ad hoc] The Phase 1B carve-out — the ledger gate stops refusing the one commit the methodology requires

**Model:** Claude Opus 5 (1M context).
**S32 of [`framework-context-cost-plan.md`](docs/planning/framework-context-cost-plan.md) §5**, the
plan's stated hard precondition for S34/S35: a new refusal reason on a hook with a measured 100%
bypass is worse than no refusal. Fork-side, canonical-only — `.githooks/pre-commit` is not in
`bin/_manifest.py`'s DISTRIBUTION, so no adopter file was touched and no channel was needed.

- **The RED was this session's own claim commit.** Phase 1B stages `HANDOFFS.md` alone, so the FM #27
  gate refused it — *"CHANGELOG.md not staged"*, exit 1 — before `d582e5b` went in with
  `--no-verify`. The framework's own mandatory step could not satisfy the gate the framework ships.
- **The population was re-measured message-independently, and the correction decided the design.**
  At `c000a90`: **32** commits stage `HANDOFFS.md` and nothing else — not the 26 that
  `git log --grep="claim S"` reports, which counts *claims*, not *commits this hook refuses*. The 6
  the grep misses are the whole problem: `f2d013b` and `21fb521` are **close-out receipts committed
  alone** — precisely what FM #27 exists to catch — and `f9ea5d7`, `faf2c42`, `a7c814d`, `1626e09`
  are later repairs of an older receipt. **A path-only carve-out would have exempted the two
  close-outs.**
- **So the predicate reads the staged diff, not the staged path.** It fires only when the staged set
  is `HANDOFFS.md` (`SESSION_NOTES.md` may ride along) **and** the diff adds a ` ```handoff ` fence
  **and** adds no stronger (4-backtick / tilde) wrapper **and** every added `status:` line reads
  `pending`. Committed alone, a close-out, a bundled claim-plus-close-out, an in-place status flip
  and a prose edit are each still refused.
- **One deliberate widening beyond the plan's sketch, labelled as added policy.** The plan says *"a
  claim commit staging only `HANDOFFS.md`"*; the carve-out also admits `SESSION_NOTES.md`, because
  distributed Phase 1B (`starter-kit/SESSION_RUNNER.md` §1B) tells every adopter to write that stub
  and *"commit it with this claim"*, and `SESSION_NOTES.md` is a DISTRIBUTION `seed`. A
  `HANDOFFS.md`-only carve-out would fix this repo and leave every adopter's prescribed shape refused.
- **Test 27 — 34 assertions, RED-first.** Against the pre-change hook it failed 10 and enumerated
  every historical claim as refused, while the negative controls stayed green. It replays the real
  corpus: each single-file `HANDOFFS.md` commit is reconstructed in a scratch repo and run through
  the hook — 27 claims pass, 6 non-claims refuse — with **both** populations derived from `git`
  (the non-claims as the complement, plus a coverage check that the 6 known shas are still in it) and
  a vacuity guard that fails if the query collapses. Nine guards were mutation-tested by **narrowing**,
  each killed by one named test.
- **An adversarial review of the finished diff found three defects, and all three are closed.** (1)
  `git diff --cached --name-only` collapses a rename to its **destination**, so `git mv <tracked
  source> SESSION_NOTES.md` beside a real claim read as the two exempt paths and deleted a tracked
  file with no ledger line — fixed with `--no-renames`, pinned by `27.N13`/`27.M8`. (2) A ` ```handoff `
  shown as **documentation** inside a 4-backtick wrapper satisfied the fence test while filing no
  receipt at all — fixed by refusing a stronger wrapper, the line-oriented analogue of the rule
  `bin/check-handoff`'s own `extract_blocks` already applies, pinned by `27.N14`/`27.M9`. (3) The
  content query inherited the committer's diff **presentation** config, so `diff.external`
  (difftastic's documented global setup) or `color.ui = always` made `grep '^+'` match nothing and
  every claim was refused — fail-closed, invisible, and only for people whose tooling is configured;
  fixed with `--no-ext-diff --no-textconv --no-color`, pinned by `27.N15`/`27.N16`/`27.M10`. The
  adversarial pass then re-ran each repro against the fixed hook and returned **0 of 11 findings
  surviving**, having refuted the rest — including its own over-broad claim that `--no-renames` can
  only tighten the gate.
- **Three prose defects in the change's own comments were corrected, which is the more useful half.**
  The hook claimed a prose edit was refused (true only when committed alone), claimed Phase 0
  reconcile-on-read reads HANDOFFS.md content (it is frontier-based; it reads the *ledger*), and
  reported the exemption's width from **two commits noticed rather than a population counted**. The
  measured width: **all 27** claims add lines outside the new block, and **5** also delete one — four
  bump the front matter's receipt count, one reconciles a predecessor's `commit:` field. So "only the
  receipt block" would refuse 27 of 27 and "deletes nothing" 5 of 27; the width stays, stated.
- **The test harness was hardened by its own misfire.** A mutant literal (`' --no-renames'`) also
  matched the *comment* explaining it, so the patch landed in prose and the guard "survived" a
  removal that never happened. `apply_mutant` now exits distinctly on an **ambiguous** literal, and
  the mutation harness runs against a scratch **copy** of the hook — two suite runs overlapped during
  development and one mutant leaked into the other — with the no-write-to-the-tracked-file invariant
  asserted per mutant, since an end-of-run check passes even when the harness edits the real file.
- **This entry was itself repaired minutes after it was written** (`a56dff8` → the following commit):
  it said the review found *two* escapes when three shipped, and the receipt carried no self-score
  narrative, which every other receipt in `HANDOFFS.md` has. Recorded here rather than in a second
  entry, because the action is the same action.
- **New: BL-21**, scoped *down* by that review from how it was first written. `starter-kit/SAFEGUARDS.md`
  and `starter-kit/BOOTSTRAP.md` describe the hook without this exemption, but both point adopters at
  the **upstream** file, which is byte-identical and has no carve-out, and no adopter receives the
  hook via `bin/sync` — so nothing adopter-reachable is false today. It becomes false the moment the
  hook is contributed upstream, and the wording to ship with it is written into the item.

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
