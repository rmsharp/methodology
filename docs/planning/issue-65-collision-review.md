# Issue #65 vs. fork-side upstream-bound work — collision review

**Session:** S47 (2026-08-08) · **Task:** operator-directed — does open upstream
[issue #65](https://github.com/KJ5HST/methodology/issues/65) collide with anything in this fork
that is prepared or planned for an upstream PR? · **Verdict: COLLISION.** Two real, moderate-severity
collisions, both against a single piece of prepared-but-unpushed work; one adjacent-but-not-blocking
finding; everything else checked is clear.

## Method

Four independent read-only investigations (a background `Workflow`, four parallel agents — full
transcripts in this session's `HANDOFFS.md` S47 receipt) plus this session's own direct `git`/`grep`
verification of every load-bearing claim before writing it here. Every fact below is corroborated by
at least two of these five sources; none rests on a single unverified subagent report (this repo's
own [Learning](../../starter-kit/FRAMEWORK_LEARNINGS.md): *a subagent's reported figure is a claim
until you re-run its command*).

## Verdict, in one paragraph

Issue #65 is accurate against `upstream/main` today — nothing there has changed. It is **not**
accurate against this fork's own tree, because session S34 (`ed22ace`, 2026-08-03) already did the
thing #65's own evidence assumes hasn't happened: moved the Learnings table out of the file and
heading #65 names. That PR is built, reviewed, and sitting unopened, waiting on a go-ahead unrelated
to this review. Separately, one of #65's own proposed invariants ("`session:` values are unique") is
already known to be false against this repo's real receipt ledger — recorded once before (BL-14) but
never connected back to #65 itself. Nothing else queued for an upstream PR (BL-12/13/14/17/21, or
either non-`main` local branch) touches #65's territory at all.

---

## Finding 1 (moderate) — Evidence A's anchor has already moved fork-side

Issue #65's Evidence A proposes structural mutation tests (malformed row, duplicate row number,
deleted row) run against `starter-kit/SESSION_RUNNER.md`'s `## Learnings (added by sessions)`
section — that is the literal target named in the issue text.

Session S34 (commit `ed22ace`, claimed at `816984b`, 2026-08-03) already extracted the entire
13-row Learnings table **out of that section** into a new distributed sibling file,
`starter-kit/FRAMEWORK_LEARNINGS.md` (top-level heading `# Framework Learnings`), leaving only a
one-paragraph pointer under the old heading:

- `starter-kit/SESSION_RUNNER.md:362-364` today reads only: *"The framework's accumulated learnings
  live in [`FRAMEWORK_LEARNINGS.md`](FRAMEWORK_LEARNINGS.md) — a sibling of this file, read on
  demand..."* — the heading text (`## Learnings (added by sessions)`) survives verbatim, but there
  is no table beneath it.
- `starter-kit/FRAMEWORK_LEARNINGS.md:22` carries the actual `| # | Learning | Source | When to
  Apply |` table, numbered 1–13 plus a deliberate gap at #14 and a row 15 appended by S35.
- Both files are `TRACKED` in `bin/_manifest.py` (i.e. **distributed** to every adopter via
  `bin/sync`), confirmed directly.

**S34 itself flagged this exact tension as open, at claim time, and it was never closed.** Its own
`active_task` (`HANDOFFS.md:554`) lists as item (d): *"the interaction with open upstream issue #65,
which proposes a structural test for this very table"* — named as one of four things "OPEN AT CLAIM
TIME, to be settled by evidence not preference." S34's `what_was_done`, `next_steps`, and `gotchas`
(`HANDOFFS.md:555-558`) never mention #65 again. A grep of every session's receipt body from S35
through S46 (`HANDOFFS.md`, twelve consecutive sessions) for the string `#65` returns **zero
matches** — nobody revisited it until this session.

**The PR is built and waiting, unrelated to this finding:**
- `ed22ace` is an ancestor of `origin/main` (this fork's own GitHub remote) but **not** of
  `upstream/main` — confirmed by `git merge-base --is-ancestor`.
- `next_steps` (`HANDOFFS.md:556`): *"THE PR IS PREPARED AND VETTED BUT NOT OPENED — it needs the
  operator's explicit go-ahead, and no agent may take that step."*
- `docs/planning/framework-context-cost-plan.md:472` and two independent `CHANGELOG.md` entries both
  confirm the PR "remains prepared and unopened" as of the most recent check.
- `gh pr list --repo KJ5HST/methodology --state all` shows no PR referencing this work; the highest
  PR number there is #64 (opened without authorization, closed same day, never merged).

**Confirmed live against `upstream/main`:** the table is still in its original location and heading
there today (`git show upstream/main:starter-kit/SESSION_RUNNER.md`), so **issue #65 is accurate
against the repo the maintainer sees.** The collision is entirely with this fork's own unshipped
state — invisible from upstream until the PR lands.

## Finding 2 (moderate) — Evidence B's own proposed invariant is false against this repo's real ledger

Issue #65's proposed receipt-ledger invariant: *"`session:` values are unique."*

Directly re-derived this session, independent of the workflow's own count:

```
$ grep -h "^session: " HANDOFFS.md docs/archive/HANDOFFS-archive.md | sort | uniq -c | sort -rn | awk '$1>1'
      2 session: S8
      2 session: S7
      2 session: S5
      2 session: S3
$ grep -ch "^session: " HANDOFFS.md docs/archive/HANDOFFS-archive.md   # 32 + 19 = 51 total
$ grep -h "^session: " HANDOFFS.md docs/archive/HANDOFFS-archive.md | sort -u | wc -l   # 47 distinct
```

**51 receipts, 47 distinct session identifiers — S3, S5, S7, and S8 each name two different,
real sessions.** This is not a defect in the ledger; it is documented, intentional design, stated in
this file's own front matter (`HANDOFFS.md:16-21`): *"This fork and `upstream/main` each run their
own `S<N>` counter, so a receipt is identified by **session + date**, never by number alone."* A
literal implementation of #65's invariant — checking `session:` uniqueness across "every block,"
per the issue's own proposed `--all` mode — would be permanently red against real, correctly-kept
project history.

This is not a new discovery: `BL-14` recorded the identical falsification when the ledger was
smaller (32 receipts, 28 distinct at the time) and explicitly connected it to #65 — *"#65's proposed
`'session: values are unique'` invariant is false at full-ledger scope... and its scope omits the
archive"* (this file, BL-14 entry). What had **not** happened before this session is re-verifying the
figure against the current, larger corpus (it still holds, now at 51/47) and recording it as its own
tracked item rather than a parenthetical inside a different backlog entry about something else.

## Finding 3 (adjacent, not blocking) — a parked partial answer to Evidence A is stale

The local branch `docs/bl-10-dangling-learning-citations` (2 commits ahead of `main`, not merged)
carries `bin/check-citations` — a contiguity-from-1 guard over the Learnings table, built as a
side-effect of BL-10's citation work and explicitly documented as *"a partial answer to #65's
Learnings-table half"* (this file, historical BL-10/BL-12 entries).

It is currently broken against `main`, for exactly the reason Finding 1 describes: it is
hard-anchored to `REGISTRY_FILE = "starter-kit/SESSION_RUNNER.md"` and
`REGISTRY_HEADING = "## Learnings (added by sessions)"` (`bin/check-citations:34-35` on that branch),
so it now aborts `GUARD FAIL — the Learnings table parsed to zero rows` (exit 2) against the
post-S34 tree — already recorded in this file's S34 regression note. Anyone reviving it, or anyone
implementing #65 unaware it exists, should know it is there rather than rebuild the same guard from
scratch — but it needs its two constants retargeted before it does anything.

The other non-`main` branch, `docs/learning-13-handoff-predictions`, is **not** a collision risk: its
diff against `main` is empty (it was PR #63, already merged, squashed to `73b72c0`, which is a direct
ancestor of `main`). A prior session's `next_steps` asked for it to be pruned
(`docs/archive/HANDOFFS-archive.md:53`); nobody has. Housekeeping, not a finding — noted here only so
it isn't mistaken for live work during any future sweep of non-`main` branches.

## Checked and cleared — no collision

- **BACKLOG.md's "runnable now up to the PR" list** (BL-12's first bullet, BL-13, BL-14's
  distributed half, BL-17's distributed half, BL-21): none touch the Learnings table's content,
  `FRAMEWORK_LEARNINGS.md`, or `HANDOFFS.md`'s fence/key structure. BL-14/BL-17 edit adjacent lines
  inside `starter-kit/HANDOFFS.md`'s receipt template (the `commit:` and `changelog_ref` field specs)
  without altering its shape.
- **`bin/check-handoff`'s already-shipped cross-block checks** (`check_answer_slots` for BL-14,
  `check_locator_forms` for BL-17): neither implements any of #65's four Evidence-B asks (fence
  balance, `session:`/`date:` as first two keys, `session:` uniqueness, no body outside a fence). Both
  the module's own docstring (`bin/check-handoff:72-76`) and a pinned regression test
  (`bin/tests.sh` Test 25 N6) explicitly disclaim answering #65 — this is deliberate, documented
  non-overlap, not an accident waiting to be found. `bin/check-handoff` is canonical-only (absent
  from `bin/_manifest.py` `DISTRIBUTION`), matching #65's own stated scope, so no adopter-facing
  surface is at stake either way.
- **BL-20, BL-22** and the rest of the open backlog: unrelated files (`bin/model-report`,
  `tools/methodology_dashboard.py`, `.githooks/pre-commit`'s seed documentation).

## Recommendation

This session takes no outward-facing action — reviewing is the deliverable, not resolving. For the
operator:

1. **Findings 1 and 2 are now tracked as `BL-23`** (`docs/planning/BACKLOG.md`) so they don't fall
   through a second time the way Finding 1 did for twelve sessions.
2. When S34's Learnings-table PR is ready to open (its own separate go-ahead), decide how #65 should
   be handled alongside it — a note in the PR description, a direct comment on #65 once authorized, or
   leaving it for the maintainer to notice at review. **Answering #65 in any form is itself an
   outward-facing action and needs an explicit ask**, same standing rule as BL-12's second bullet.
3. If #65 is ever implemented fork-side (also outward-facing, also needs an ask), its "`session:`
   values are unique" invariant needs a session+date compound key, or an explicit archive/sequence
   exclusion — not a literal per-block uniqueness check — to avoid failing on legitimate history.
