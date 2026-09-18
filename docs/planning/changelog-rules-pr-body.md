# Upstream PR — `CHANGELOG.md` rules in one synced home (draft body)

Fork-only working file: the draft title and body for the pull request from `rmsharp:bl57/changelog-rules`
into `KJ5HST/methodology:main`. Everything below the rule is the body as it would be posted. Written under
plan [`changelog-rules-contradictions-plan.md`](changelog-rules-contradictions-plan.md) §P12, step 5.

**Title:** Put the CHANGELOG.md rules in one synced home: the seed becomes a pointer, and the rules stop contradicting each other

---

**Base `main` (`6b29d3d`), head `rmsharp:bl57/changelog-rules` (`036d840`).** 20 commits, plus three merges
of `main` into the branch (the last at `f572068`, after your first tightening), so `git merge-tree` against
`main` reports no conflicts. 19 files, +657 / −293, and 408 lines of `CHANGELOG.md` entries (one per commit,
as #76–#79 did). No Learning row, no failure-mode change, no hook behaviour change.

## The problem

The rules for a project's `CHANGELOG.md` live **inside the seed**: 11,804 of `starter-kit/CHANGELOG.md`'s
12,893 bytes are rules — how to add an entry, the source tags, when to archive. `bin/sync` writes a seed
once and never again, because after that it holds the project's history. So every correction to those rules
strands the copies already in adopters. When this work was planned, two of six adopter ledgers still
carried an older copy of those rules, one that called read truncation *silent* after the framework had
corrected it.

Spread across fourteen files, the rules have also come to disagree with each other — fifteen ways in this
repository's text, listed below. Most of the disagreement has the same cause: the rules were stated in the
seed and then restated, differently, wherever a session needed them.

## What this changes

- **One home, kept current by sync.** A new section, **§The Action Ledger** in `FRAMEWORK_APPARATUS.md`
  (distributed, so it lands in adopters at `docs/methodology/FRAMEWORK_APPARATUS.md`), holds the rules. The
  seed's three rule sections moved there verbatim first, one heading level down, and every later change
  was made in the home.
- **The seed becomes a pointer** — 12,893 → 1,335 B: title, purpose line, a link to the home, and a format
  marker, `ledger-format: 2`, on the line the seed tells adopters to keep.
- **The stale-seed check can fire.** On `main`, `bin/_manifest.py` keys each seed on its title
  (`Authoritative Action Ledger`, `Handoff Receipts`), which never changes, so an old seed always reads
  current. It now keys `CHANGELOG.md` on the versioned marker and `HANDOFFS.md` on its `## Size, and when to
  archive` heading. `bin/status` then gives each flagged seed its own migration route, and **no longer tells
  adopters to "reconcile its header and per-entry format"** — which meant rewriting committed entries.
- **The rules themselves**, decided as below: the ledger is never read whole, so archiving is optional;
  `[BL-<id>]` takes whatever id a backlog uses; one entry per commit, never edited; month headings start at
  a ledger's next new month.
- **Wording everywhere else follows** — *prepend*, not *append*, for a newest-on-top file; *action ledger*,
  not *completed work history*; the runner cites the audit instead of restating an older form of it. The
  hook's refusal text changes the same two words; its behaviour does not.
- **Your root `CHANGELOG.md` front matter** points to the home for its rules, audit and month headings — its
  own commit, `83a12f0`, because it is your file (see *What can be dropped*).
- **Three smaller fixes ride along:** your review's F5 on #80 (`methodology_trim.py` links its design document
  at a pinned public commit, and stops citing a `--no-renames` flag no hook has); the read-cap partition test
  sums only the two files read together, not every whole-read class (a config declaring two ledgers at 25,000
  tokens each, read separately, used to fail it); and `BOOTSTRAP.md` says how to commit a `bin/sync` run.

## The four decisions

These were taken by the contributor's operator before any edit, each against named alternatives. The fourth
changes your current practice, so the evidence is given with it.

| Question | Chosen | Not chosen |
|---|---|---|
| Where the rules live | One synced home; the seed keeps a pointer and a format marker | Keep them in the seed and flag stale copies; move only the size rules |
| Archiving | **Optional.** Nothing reads the ledger whole (Phase 0 takes a frontier from `git log`; close-out reads the top; a lookup is a `grep`), so no size is stated. `methodology_trim.py --check` is the only statement of *when* | Mandatory at the trimmer's trigger; each project records its own choice |
| Source tags | `[BL-<id>]` takes any backlog id; the audit is anchored to the entry heading and reads the archived shards | Numeric ids only; an open vocabulary |
| Entries | **One per commit, never edited.** A claim commit carries an *(in progress)* entry and close-out adds its own. A correction is a new entry; the one exception is removing content that must not be published | One entry per session, edited until close-out |

On the fourth: the co-staging hook's unit is the commit, so an entry per commit is the one rule the hook
already enforces. Of the contributor fork's last 60 commits that touched its ledger when the decision was
taken, 56 only inserted. Your
sessions S13–S17 each rewrote their claim entry at close-out, and S16's rewrite, done by a script that
searched for the wrong boundary, deleted ten other entries (`356556f`, 40 → 30 headings; restored in
`ed98444`). Never editing a committed entry removes that class of accident. It is your call; if you prefer
the per-session form, *Lifecycle* in §The Action Ledger is the one place to change.

## The fifteen disagreements, before and after

Line numbers are `main`'s (`6b29d3d`).

| # | The disagreement | On `main` | With this PR |
|---|---|---|---|
| 1 | Whether a session reads the ledger at all | The seed prices it as a *context tax* — *"every session pays for the whole file"* (`starter-kit/CHANGELOG.md:104`), *"split into shards once it outgrows a session's read"* (`:180`); the `HANDOFFS.md` seed repeats it (`:98`, `:150`), and the trimmer calls its budget *"the per-file context-tax budget"* (`methodology_trim.py:186`). The runner's Phase 0 never reads it: it takes a frontier from `git log` | *Reading and archiving* names the three partial reads and says the file is never read whole. The five sites are gone |
| 2 | Which size triggers an archive | The seed: a ~2,000-line proxy and a 65,536 B default (`:103`–`104`); the trimmer fires at 196,608 B | No size in the rules; the trimmer's `--check` is the only trigger |
| 3 | *Append* or *prepend* | *"Append … newest on top"*: runner `:281`, `ITERATIVE_METHODOLOGY.md:294`, `HOW_TO_USE.md:767`, `:804`, the hook's message `:70`; the seed says *prepend* | *Prepend* at every site |
| 4 | Whether a trim may run in Phase 0 | Only the seed says *never* (`:168`), and adopters stop receiving the seed | Stated once in the home: a trim is its own action with its own entry, never in Phase 0 |
| 5 | Detecting an old seed | `bin/_manifest.py:97`–`99` keys both seeds on titles that never change, so the check cannot fire | A versioned marker, and a heading that older `HANDOFFS.md` seeds lack |
| 6 | A closed tag vocabulary against an open practice | `[BL-<N>]` in the hook `:71`, the runner and the flight manual; but hundreds of adopter entries use ids like `BL-OPS-ADMIN-PW-RECOVERY-001`, and your own tutorial writes `[BL-F1]` (`docs/tutorials/T2_worked_transcript.md:257`) | `[BL-<id>]`; the audit pattern is `BL-[^]]+`. The tutorial now conforms unchanged |
| 7 | Where the Phase 1B marker lives, and whether a claim commit has an entry | Runner `:88` and `ITERATIVE_METHODOLOGY.md:169` put `CHANGELOG: pending` in `SESSION_NOTES.md` and record actions only at Phase 3F; this repository keeps no `SESSION_NOTES.md`, and its claims write an entry | A claim commit carries an *(in progress)* entry; a project with no `SESSION_NOTES.md` relies on its `status: pending` receipt |
| 8 | One entry per action, or per session | The runner says per commit and per non-commit action; practice here is one per session, rewritten at close-out | One per commit, never edited (decision four) |
| 9 | A proposed guard that would refuse every trim | Your S16 receipt's next step (e): refuse a commit whose staged ledger has fewer `### ` headings than `HEAD`'s. Every trim lowers that count by design | *Conservation*, below. The guard itself is not built here; it stays yours |
| 10 | An audit that miscounts, or fails | The published audit, `grep -E '\[(issue #\|BL-\|ad hoc)' CHANGELOG.md` (root `:14`, seed `:24`, runner `:39`), is unanchored and reads one file: **on `main` today it counts 69 actions in a ledger of 55 entries**. The shard-spanning glob form reads 0 in zsh wherever no shard exists (*"no matches found"*) | One audit, in the home: anchored, reading the shards through `git ls-files`. It counts 55 on `main`'s ledger and 74 on this branch's, the same in bash and zsh |
| 11 | What the file is | *"Completed work history"*: `CLAUDE.md:51`, `README.md:96`, `:114`, `:200`, `BOOTSTRAP.md:23`, `:107`, `:131`, `:139`, `:145` — against an action ledger that also records releases, PR opens and declines | *Action ledger* at every site. `README.md`'s release history is left as written |
| 12 | Distributed seeds citing material that is not in this repository | Both seeds' size tables (`CHANGELOG.md:103`, `HANDOFFS.md:97`) cite a backlog item and a planning document in the contributor's fork | Gone from both seeds |
| 13 | Where a month section starts | Seed `:92`: *"promote … as the list grows"*; your root ledger `:34` promises sections and has none | *Placement*: prepend under the topmost `## YYYY-MM`; a ledger without month headings starts them at its next new month, and nothing is retrofitted |
| 14 | The `HANDOFFS.md` seed repeats 1 and 2 | `starter-kit/HANDOFFS.md:89`–`125`: the same premise, the same 65,536 B, and a cross-reference (`:123`) to the seed section this PR moves | Premise and byte row gone; the cross-reference points at the home; the heading stays, as the marker |
| 15 | Stale-seed advice that rewrites history | `BOOTSTRAP.md:85` and `bin/status` tell an adopter to *"reconcile its header and per-entry format"* by hand | Each seed's own route; every entry and receipt stays as written |

A sixteenth concerned a proposal in the contributor's own backlog, withdrawn; nothing here changes for it.

## Conservation, for the heading-count guard

The home states it (*The shard convention*): **the live file and its shards together never lose an entry.**
A trim moves entries and deletes none, so anything that counts the ledger reads both —
`cat CHANGELOG.md $(git ls-files 'docs/archive/CHANGELOG-*.md')`, which runs the same in bash and zsh with or
without a shard. A guard built that way lets every trim through and still catches the S16 accident. One that
compares the live file's `### ` count across commits refuses every trim, because the live count falls at
each one by design.

## Size: the Phase 0 pair still fits

Measured by the doubled-file method, each run reproducing the previous recorded figure as a control
(`2a3e410d` 37,731, `1244e95b` 46,965, `933816b4` 42,208 over seven copies):

| File | `main` | this branch | ceiling |
|---|---:|---:|---:|
| `starter-kit/SESSION_RUNNER.md` | 53,252 B · 18,865.5 tok | 53,229 B · **18,858.5 tok** | 18,900 |
| `starter-kit/SAFEGUARDS.md` | 17,024 B · 6,029.7 tok | 17,129 B · **6,083.7 tok** | 6,100 |
| the pair | 24,895.2 tok | **24,942.2 tok** (99.77% of 25,000) | 25,000 |
| `CLAUDE.md` | 59,153 B · 23,482.5 tok | 59,119 B · **23,476.5 tok** | 23,483 |

No ceiling changed. The runner and `CLAUDE.md` shrink. `SAFEGUARDS.md` grows by one sentence (+105 B), the
`bin/sync` commit rule, and that commit can be dropped on its own. The root `.context-budget.json` records
the new densities with the blobs they were measured on (`adaa4a3`), as its own rule asks when a blob changes.
`FRAMEWORK_APPARATUS.md` grows 15,493 → 28,245 B; it is read on demand and has no budget entry.

## Verified

On the branch tip, in a fresh `--no-local` clone with `HEAD` asserted:

- `python3 starter-kit/quality_ratchet.py --run` — **10/10 pass**: `bin/tests.sh` 149 passed / 0 failed,
  dashboard units 226, budget units 122, trimmer units 124, ratchet units 45, `check-links`, `check-learnings`,
  `check-handoff --all`, `commit-msg --selftest` all 0.
- `python3 starter-kit/context_budget.py --status` — nothing over budget.
- `bin/check-links` — 111 links across 23 distributed files (107 on `main`).
- `methodology_trim.py`'s syntax tree is identical to `main`'s once docstrings are blanked: its change is
  comments and docstrings only.

Three floors in `.quality-gates.json` now sit below what the branch measures (`tests-sh-passed` 139 against
149, `context-budget-unit-tests` 118 against 122, `trimmer-unit-tests` 123 against 124). The manifest is
yours, so this PR does not raise them.

## Adopters: `bin/sync` dry runs

Six real adopter projects, copied into a scratch directory as exactly what `bin/sync` reads (`.gitignore`
plus whichever distributed paths exist), dry-run from `main` and from this branch. Every refusal was checked
against the source's full history:

| Project | From `main` | From this branch |
|---|---|---|
| A | refuses 7 | refuses 4 |
| B | refuses 2 | refuses 2 |
| C | refuses 5 | refuses 5 |
| D | refuses 5 | refuses 5 |
| E | refuses 6 | refuses 6 |
| F | refuses 7 | refuses 4 |

**This PR adds no refusal**; it removes three in each of two projects. Every remaining refusal is either a
version these projects took from the contributor's fork, which `main`'s history has never held, or a genuine
local edit (three files across two projects) — the same from `main` today.

After merge, `bin/status` flags the `CHANGELOG.md` seed as *present (stale format)* in four of the six and the
`HANDOFFS.md` seed in three, each with its migration route. Two of the projects have already migrated their
`CHANGELOG.md` seed by hand, from the contributor's fork; theirs read *present*. Sync never rewrites a seed, so each migration is a hand edit in
that project, with every existing entry left byte-identical.

## What can be dropped

- **`83a12f0` — your root `CHANGELOG.md` front matter.** Dropping it leaves `:12` saying the rules *"live in
  `starter-kit/CHANGELOG.md`"*, which no longer holds them, and `:14`'s unanchored audit in place.
- **`0d63410` — how to commit a `bin/sync` run.** `BOOTSTRAP.md` gains the paragraph and `SAFEGUARDS.md` the
  one sentence that keeps its five-file cap from contradicting it. Dropping it also means restoring
  `SAFEGUARDS.md`'s density entry in `.context-budget.json` to `main`'s (2.8234 at 17,024 B, blob `933816b4`).

## Not in this PR

- No Learning row and no failure-mode change: the count stays 28, and FM #27's requirement is unchanged.
- No existing ledger entry is retagged or rewritten, here or in any adopter.
- `HANDOFFS.md`'s own archive rule, apart from its seed's copy of the size premise.
- The history-walk fix for `bin/sync` and `bin/status` (git's default walk can hide a published version behind
  a merge, so an unmodified file reads *locally modified*) — a separate, small PR to follow.
- Found, not fixed: four comments in two distributed tools still cite planning documents in the contributor's
  fork (`methodology_trim.py:200`, `:818`, `:821`; `context_budget.py:683`); they arrived with #77 and #79.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
