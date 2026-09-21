# PR #83's twelve decisions — a collaborator's positions, with the fork's evidence

**Date:** 2026-09-20 (fork session S206)
**Status:** DRAFT, internal. **Nothing here has been posted.** A comment, review or edit on PR #83 is an
outward action and needs its own explicit go-ahead; §6 carries a proposed text so that go-ahead can be
given on exact words.
**Backlog:** BL-82 ([`BACKLOG-DETAIL.md` §BL-82](BACKLOG-DETAIL.md#bl-82)). This document answers BL-82's four
settle-first questions in §1 before taking any position.
**Subject:** upstream PR [#83](https://github.com/KJ5HST/methodology/pull/83), head `219fb9d`, the
maintainer's `docs/planning/parallel-sessions-plan.md` (468 lines, 48,116 B), whose §8 lists *"Open
decisions for the operator (answer before Phase 1)"*. Its base, `6b29d3d`, is still `upstream/main` today.
Read it with `git fetch upstream refs/pull/83/head` and `git show 219fb9d:docs/planning/parallel-sessions-plan.md`.
**Evidence discipline:** every figure below was re-run this session unless marked **TAKEN**. Line numbers are
at `6b29d3d` unless another tree is named beside them.

---

## 0. The answer in one paragraph

**The twelve are the maintainer's decisions, not this fork's** (§1a). What #83 can use from us is a
collaborator's review, which is what its author opened it for. On the substance we agree with **eight** of
the twelve items as recommended, most of them with evidence of our own. We would reword a ninth (the
item-12 scope guard), clarify a tenth (D5), and leave release sequencing to him. One item carried no
recommendation (D11), so we offer ours. **The finding that matters is D4**, which item 3 takes as given.
Measured on upstream's own history, git's built-in `merge=union` does what the plan says for
`CHANGELOG.md`: both entries survive, and only a blank separator line is lost.
It does **not** do it for `HANDOFFS.md`. Two receipts prepended at one anchor **fuse into a single block**
with two `session:` lines, and the merge exits 0. Receipts begin and end with identical fence lines, so this
follows from the format. `bin/check-handoff --all` catches it, so it is not silent. But the plan's own
Phase 1 test (*"git merge → exit 0 … `check-handoff --all` green"*) cannot pass as specified, and the
rejected per-receipt-files alternative was ruled out on the premise this falsifies.

---

## 1. Settle first — BL-82's four questions

### (a) Whose decisions these are: the maintainer's

**The evidence says the §8 "operator" is the person who ran the maintainer's session, not this fork's
operator.**

- The plan's own receipt, S24 at `219fb9d:HANDOFFS.md`, gives next step (a) as *"OPERATOR: answer the twelve §8
  decisions on PR #83 (a comment suffices — that is the plan's Phase 0)"*. It describes its deliverable as
  *"the plan document + a PR for review"*.
- The plan's field evidence, "adopter" S13 and S163, comes from a Rust project (`cargo test --workspace`,
  `mod.rs`/`lib.rs`). S24's `key_files` locates it in *"agent memory `adopter-fanout-evidence` (deliberately
  not in this public repo)"*. None of this operator's local projects has a top-level `Cargo.toml`, and a
  grep for `cargo test --workspace|WorktreeCreate hooks|mod\.rs` across the `*.md` files of eight local
  project directories matches **0** files.
- Upstream S22's receipt (`6b29d3d:HANDOFFS.md:34`) names this operator in the third person beside "the
  operator": *"(a) WAIT FOR rmsharp on the thread … (b) MERGE when the operator says so."*
- **Counter-evidence, stated:** the plan's §2 calls PR #82's merge *"the operator's merge button"*, and #82
  was merged by `rmsharp` (`gh pr view 82`: `mergedBy` rmsharp, 2026-09-16T18:05:47Z). So the word is used
  loosely at least once. That changes nothing above.

**Consequence.** BL-82's headline, *"waiting on TWELVE OPERATOR DECISIONS, not on a review"*, is half right.
The PR does wait on §8. But §8 is the maintainer's to answer, and a review is exactly what a collaborator
can give. This document is therefore **positions offered as input, not rulings**, and BL-82's index row is
corrected in the same commit.

**What the count in §0 means.** Of the twelve items, we agree with eight as recommended (items 1, 2, 3, 5,
6, 7, 9 and 10). We ask for a clarification on one (item 4, D5) and would reword one (item 12). One we leave
to the maintainer outright (item 8, D12's release sequencing). One had no recommendation, so we offer ours
(item 11, D11). **Separately, D4 itself needs a change.** Item 3 asks only about its ordering and takes its
file set for granted.

### (b) One document, then a comment — separately

This document is the deliverable. Posting is a later, separate action. §6 proposes the comment text in the
terms an outside reader recognizes, without fork session numbers or backlog codes. It leads with the one
finding that changes the plan rather than walking all twelve, because the author's recommendations stand
where we agree and a comment restating them would be noise.

### (c) What answering commits this fork to: nothing, but the fork has a stake in D4 and D5

Positions commit no one to executing a phase; every phase runs in the maintainer's sessions. The fork is
nonetheless the plan's **named Shape B case** (*"the fork-and-upstream case (`rmsharp` and this repo)"*,
plan §3A). It is also where D4 would first meet a retention-trimmed ledger. This fork's `HANDOFFS.md` keeps
two receipts and is trimmed almost every session, and the September resync already had to rule by hand:
*"keep only the incoming receipts that are in neither the live file nor a shard … Never re-add S13–S19 or
S21"* ([`upstream-resync-2026-09-plan.md:372-376`](upstream-resync-2026-09-plan.md)). Under `merge=union` that
rule would have been broken silently (§3, case 4). D5's identity rule also decides how the receipts of this
fork's 200-odd bare-`S<N>` sessions read after a resync.

### (d) What each position rests on

| Premise | Re-run or taken | Result |
|---|---|---|
| Runner and `SAFEGUARDS.md` token headroom | **Re-run**, plan §9's own command, `--no-local` clone at `6b29d3d` | runner **18,865 / 18,900** (35 left), `SAFEGUARDS.md` **6,029 / 6,100** (71 left). Exact. |
| The same at our PR #84's head `77afc12` | **Re-run**, same method | runner 18,858 / 18,900 (42 left); **`SAFEGUARDS.md` 6,083 / 6,100 (17 left)** |
| No merge driver today | **Re-run** | `git ls-tree 6b29d3d .gitattributes` empty; `git check-attr merge CHANGELOG.md HANDOFFS.md` → `unspecified` |
| The "11 reconciled receipts" item | **Re-run** | `6b29d3d:CHANGELOG.md:293` |
| Principle 9 and Phase 1 step 4 (item 12) | **Re-run** | `6b29d3d:ITERATIVE_METHODOLOGY.md:122` (heading), `:148` (step 4) |
| Manifest rows | **Re-run** | 29 at `6b29d3d`, fork `main`, and the heads of #83, #84, #85 |
| Ratchet gates | **Re-run** | 10 at `6b29d3d` and #84; **11** at #85 (adds `pre-commit-selftest`) |
| What `merge=union` does to each ledger | **New measurement, not in §9** | §3; [`pr83-union-repro.py`](pr83-union-repro.py), commit `c3a096b` |
| GitHub's merge honoring `merge=union` | **TAKEN** (untested) | Testing it needs a scratch PR, which is outward. The plan already defers it to Phase 1 (§7 item 3). |
| Adopter S13 / S163 | **TAKEN** | The maintainer's private records |
| `methodology_trim.py`'s parser on union's missing blank line | **Not tested** | Stated in §3 |

---

## 2. The twelve at a glance

| §8 | Decision | Author recommends | Our position | Fork evidence |
|---|---|---|---|---|
| 1 | Framing (D1): one closer per tree | ratify | **Agree** | Two more observations of the failure (§4.1) |
| 2 | D2 as a `SAFEGUARDS.md` hard rule | hard rule | **Agree** — budget note | Headroom 71 → 17 tokens if #84 lands first |
| 3 | D4 ordering: leave as merged | leave | **Agree on ordering; change D4's file set** | §3: union fuses receipts |
| 4 | D5 identity: `S<N>-<seq>` | `S<N>-<seq>` | **Agree — say which trunk** | The seed already rules that a fork runs its own bare `S<N>` |
| 5 | D6: a merge is one action; drop the 11 receipts | drop | **Agree, strongly** | The 11 commits are this fork's, already recorded here |
| 6 | D7: workers produce, lead commits | lead commits | **Agree** | A review agent wrote into a distributed seed here |
| 7 | D8: manifest-at-ref | manifest-at-ref | **Agree** — one ceiling to add | Concurrent suites trip a GitHub limit |
| 8 | D12: v3.8 first | v3.8 first | **The maintainer's call** | v3.8 not yet tagged; our open PRs move cited lines |
| 9 | D13: merger scores the merged line | merger scores | **Agree** | None either way |
| 10 | D14: FM #29 | FM #29 | **Agree — widen the wording** | Recurrence already exists, and not only in a tree |
| 11 | D11: dashboard advisory | *no recommendation* | **Not now; revisit after Phase 5** | — |
| 12 | Scope guard | confirm | **Confirm, reworded** | The plan edits Principle 9 and flight-manual Phase 1 |

---

## 3. The finding that changes a recommendation: `merge=union` fuses receipts

**The claim** (plan D4): *"On the S21 shape — two contiguous blocks inserted at one anchor — it keeps both
whole (in practice ours above theirs; git's documentation promises only that both survive …)"*. The plan
applies union to all four files, *"whose every legitimate concurrent edit is an insertion"*.

**The measurement.** [`pr83-union-repro.py`](pr83-union-repro.py) (commit `c3a096b`, git 2.50.1) uses
upstream history only. It rebuilds the plan's Shape B case as though S23 and S24 had both claimed from `64f23bf`:
base `64f23bf`, ours `6b29d3d`, theirs `219fb9d` with S23's block removed. Each side is checked to be a pure
insertion at the same anchor before anything is merged. Each case runs once without and once with the
attribute.

| Case | Without `merge=union` | With `merge=union` |
|---|---|---|
| **1. Receipts** — `HANDOFFS.md`, real S23 and S24 blocks (16 lines each) | exit 1, conflict markers | **exit 0; one block at line 10 holds both, with two `session:` lines.** `check-handoff --all` exit 1: *"first two keys must be `session` then `date` (got session, session)"* |
| **2. Ledger entries** — `CHANGELOG.md`, real S23 (19 lines) and S24 (29 lines) entries | exit 1, conflict markers | **exit 0; both entries whole except one blank separator line** (1,592 of 1,593 lines). S24's `###` heading lands directly under S23's last bullet; ours above theirs, as the plan says |
| **3. Receipts sharing no line but their fences** (synthetic) | — | **exit 0; still fused** — two blocks where three belong |
| **4. A retention trim against a prepend** (synthetic, the resync's shape) | exit 1, conflict markers | **exit 0; the archived S21 is back in the live file**, and the two new receipts are fused |

**Why receipts fuse.** Git's three-way merge factors lines both sides share out of a conflicting region
before the union driver concatenates what is left. Two receipts inserted at one anchor share at least the
opening and closing fence lines, and same-day receipts usually share `date:`, `status:` and often the
scores too. Those lines collapse into one copy and the differing keys are stacked inside one fence pair.
Case 3 shows the fences alone are enough. A `CHANGELOG.md` entry opens with a unique `###` heading, so
only its blank separator is shared, and one blank line is all it loses.

**What it means for the plan.**

- **D4 holds for `CHANGELOG.md`, the file D4b's checker is for.** Whether `methodology_trim.py`'s record parser
  and the proposed `bin/check-ledger` accept a heading with no blank line above it was **not tested**. D4b
  should accept it or name it.
- **D4 does not hold for `HANDOFFS.md`.** The plan's premise *"union covers both files at once"* is what
  retired its *per-session receipt files* alternative (alternatives table, row 2). The Phase 1 DONE
  criterion *"git merge → exit 0 … both receipts present, `check-handoff --all` green"* cannot be met for
  receipts. A test built from two minimal receipts would still go red, because case 3 is minimal.
- **Union trades a marked conflict for an unmarked defect.** Without the attribute the merge stops, and the
  conflict is small. With it the merge exits 0 and the fused block is found only by someone who runs the
  checker. A merge made by GitHub's button runs no checker, if GitHub honors the attribute at all, which is
  still untested.
- **"Every legitimate concurrent edit is an insertion" is false once the distributed trimmer runs.**
  `methodology_trim.py` (a `TRACKED` manifest row at `6b29d3d:bin/_manifest.py:45`) deletes the oldest records.
  Case 4 is the resync's hand-applied *"never re-add"* rule, broken silently.

**Our position: change D4's file set.** Declare `merge=union` for `CHANGELOG.md`, `dashboard_history.jsonl` and
`.context-budget-history.jsonl` (one record per line; the two JSONL files were **not tested** here). Leave
`HANDOFFS.md` unattributed: its conflicts stay small and marked, the plan's own "resolve by hand" fallback
covers them, and `check-handoff --all` checks the result. If Shape B shows receipt conflicts are frequent,
the per-session-files alternative is the one to revisit; its stated reason for rejection no longer holds. A
block-aware custom driver would also work, but it needs per-clone configuration, which the plan chose
`union` to avoid. Whatever is chosen, Phase 1's merge test should use real receipts, and this repro's case 1
is one. It would have failed RED-first against the plan as written.

---

## 4. Positions, one by one

**4.1 — Framing (D1). Agree.** "Many hands, one closer per tree" matches what this fork has learned
independently. **Two observations beyond the plan's S163:** a delegated *review* agent appended a sentence to
the distributed seed `starter-kit/CHANGELOG.md` in the shared tree and never reverted it. That was fork S44,
2026-08-04, and it is recorded only in the operator's agent memory, not in a tracked file. Separately, two
`bin/tests.sh` runs in parallel each failed Test 9 on GitHub's rate limit, and a floor measured then read one
low (fork S178, [`docs/archive/CHANGELOG-through-2026-09-17.md:1098-1109`](../archive/CHANGELOG-through-2026-09-17.md)).
**One gap in §8 itself:** item 1 ratifies D1, but D3 (the three new contract gates (e)–(g), the plan's
core), D9, D10 and D15 are decisions §8 never lists. Item 1 is worth reading as covering D3 explicitly.

**4.2 — D2 as a hard rule. Agree.** `SAFEGUARDS.md` is the file that wins conflicts, so a hard rule belongs
there. **Budget note:** the 71 tokens of headroom reproduce at `6b29d3d`. At our PR #84's head the file has
**17** left (6,083 / 6,100), so if #84 merges first the ~70–90-token row must be paid almost entirely by
reduction. The plan already allows that (*"paid by reduction if it does not fit"*); this sizes it. For the
read-only-lens clause: this fork found that `git status --porcelain` cannot show an ignored path. A
`__pycache__` appeared mid-review and only `--ignored` shows it (fork S115, again recorded only in agent
memory). Police lenses with `git status --porcelain --ignored`.

**4.3 — D4's ordering (item 3). Agree:** leave union-merged order as merged. Case 2 confirms ours lands above
theirs, and identity is date + tag + sha. **D4's file set: change it, per §3.**

**4.4 — D5 identity. Agree, and say which trunk.** The seed already rules on the fork case
(`starter-kit/HANDOFFS.md:82-88`, unchanged by #84): *"a fork and its upstream each running their own, so two
distinct sessions share an `S<N>` by construction … do not treat a repeated id across sequences as
corruption"*. It also forbids renumbering a written receipt. D5's *"Bare `S<N>` is reserved for the trunk
sequence (`main`)"* reads as one trunk. A fork's `main` is a trunk too, and this fork has run bare `S<N>` on
it for 200-odd sessions. Suggested wording: *each repository's `main` carries a bare `S<N>` sequence;
`S<N>-<seq>` is for other branches within one repository; across repositories the (`session`, `date`) pair
already identifies a receipt.*

**4.5 — D6, a merge is one action with one receipt. Agree, strongly, and drop the 11 receipts.** The 11 are
the non-merge commits of PR #80 (`5b92b2f` … `aa36fd8`; `gh pr view 80`: author `rmsharp`, 16 commits), and
they are **this fork's commits**. Every one of the 11 is named in the fork's own ledger: `CHANGELOG.md`
archives and fork receipts including S137, S146, S149 and S165. Writing 11 `status: reconciled` blocks
upstream would reconstruct records of sessions the upstream line never ran, which already exist in the
contributor's ledger. That is D6's *"external contribution"* case exactly. **The `--merges` line has
evidence too:** of the 40 newest merges on fork `main`, 37 are named by sha in the fork's ledgers. Two of the
other three are upstream merge-button merges (#73, #68), recorded only by PR number, and the third
(`c7f10b4`, a 2026-07-08 resync) matched neither probe. That is a grep sample, not a census. **One
addition:** after a merge, check ledger coverage **per merged PR**, not per frontier. A merged commit with no
ledger line becomes invisible once a later commit on the same branch touches the ledger. This fork found
that on upstream PR #77's `56997af`, buried by #78's entry (fork Learning #51). The one-receipt rule should
carry that check.

**4.6 — D7. Agree**, and agree that "a worker context waives the hook" stays not adopted. §4.1's S44 case is
the reason workers should write nothing at all.

**4.7 — D8, manifest-at-ref. Agree**, and agree the `tests-sh-failed max 1` option is a standing loosening,
which `SAFEGUARDS.md`'s ratchet row refuses. **A ceiling to state:** manifest-at-ref makes Test 9 *correct*
on every branch but not *safe under concurrency*. Test 9 makes about 29 `gh api` calls per run, one per
manifest row. In S178 two concurrent runs both failed Test 9 on GitHub's API rate limit; the tracked ledger
records the failure. The details are in agent memory: `gh api rate_limit` read 5000/5000 throughout, and the
limit lasted about 15 minutes. Shape B's Phase 5 runs concurrent sessions by design, so it should run suites
serially or record this.

**4.8 — D12, v3.8 first. The maintainer's call.** For the record: the latest release is still `v3.7`
(2026-08-12), and §5 lists the cited lines our open PRs move.

**4.9 — D13, the merger scores the merged line. Agree.** This fork has no evidence either way.

**4.10 — D14, FM #29. Agree, and widen the wording.** The alternative (*"Degradation row only, promote if
Phase 5 records a recurrence"*) is already answered, because recurrences exist: S44 and S178 above, in two
different forms. S178 involved no shared working tree; the shared thing was an external rate limit, and each
run read the other's side-effect as its own failure. A countermeasure worded only for *one working tree*
would not have named it. Suggested tendency: *concurrent actors that edit, build, test or call a
rate-limited service against shared state read each other's side-effects as defects*. The name
("Shared-tree" or "Shared-state mutation") is the author's to pick.

**4.11 — D11, the dashboard advisory. No recommendation was given; ours is: not now.** A permanent LOW
advisory on every single-sequence adopter is a report that nothing gates on. The runner's own Degradation
table says to add a gate rather than another report in that case. If §3's change is taken, the advisory's
text (*"ledgers have no merge driver"*) also changes. Revisit after Phase 5. If adopted, fire it only where
the history shows concurrent ledger writes, for example a merge whose two parents both touched
`CHANGELOG.md`. That trigger is a suggestion and is **untested**.

**4.12 — Scope guard. Confirm, reworded.** The guard says the plan *"does not touch … the 6 phases … the 9
principles"*. The plan's own D1 gives Principle 9 a paragraph (`6b29d3d:ITERATIVE_METHODOLOGY.md:122`), and
its Phase 2 edits flight-manual Phase 1 step 4 (`:148`, the `--merges` clause). Accurate wording: *adds none,
removes none, renumbers none; amends Principle 9 by one paragraph and Phase 1 step 4 by one clause.*
**A naming collision to expect:** the ratchet declares 10 gates at `6b29d3d`, our #85 adds one, and D4b's
`check-ledger` would make **twelve**. That is the same number as the flight manual's "12 quality gates",
a different set. Phase 2's sweep for *"12 quality gates"* will match both.

---

## 5. Where our open PRs move the plan's citations

Both are ours and open against `6b29d3d`. Whichever lands before #83's Phase 1 shifts lines it cites. The
plan's own rule (cite at the base sha) covers the mechanism; this is the list.

- **#85** (`e2501c5`) rewrites `.githooks/pre-commit` (81 → 176 lines). The marker loop the plan cites at `:21-27`
  moves to `:118` and drops `REBASE_HEAD`; the co-staging test at `:53` moves to `:148`.
- **#84** (`77afc12`) turns the `CHANGELOG.md` seed into a pointer (187 → 21 lines). D4's
  *"prepend-only, so close-out never re-sorts"* (`starter-kit/CHANGELOG.md:91`) moves to
  `FRAMEWORK_APPARATUS.md:454`. The seed sentinel D4b relies on survives (line 10 → 14).
- **#84** also changes files the plan cites by line — `starter-kit/SESSION_RUNNER.md`, `starter-kit/SAFEGUARDS.md`,
  `bin/check-handoff`, `bin/tests.sh`, `ITERATIVE_METHODOLOGY.md` — and moves `SAFEGUARDS.md`'s headroom from
  71 to 17 tokens (§4.2). Individual line shifts there were **not** re-derived, so re-derive them at Phase 1.

---

## 6. Proposed comment for #83 — NOT POSTED

*For the operator's go-ahead, verbatim or edited. Written without fork session numbers or backlog codes.
The repro link is pinned to commit `c3a096b` and resolves once the fork is pushed.*

> Thanks for writing this up. I read §8 as your decisions, so these are a collaborator's notes, not answers.
>
> **One finding changes a recommendation: D4's `merge=union` fuses receipts in `HANDOFFS.md`.** I rebuilt
> your Shape B case from this repository's own history. I took the receipt and ledger entry that
> `64f23bf..6b29d3d` adds and the ones `6b29d3d..219fb9d` adds, as if both sessions had claimed from
> `64f23bf`. Then I merged with and without the attribute, on git 2.50.1. For `CHANGELOG.md` union does what the plan says: exit 0, both
> entries whole, ours above theirs, one blank separator line lost. For `HANDOFFS.md` the merge also exits 0,
> but the two receipts become **one block with two `session:` lines**, and `check-handoff --all` fails on it.
> It happens because receipts open and close with identical fence lines. Git factors shared lines out of a
> conflict before union concatenates the rest, so even two receipts that share nothing but their fences
> fuse. A retention trim merged against a prepend also brings the trimmed receipt back into the live file.
> The script is stdlib Python and runs in this repository: https://github.com/rmsharp/methodology/blob/c3a096bdc8b4eeb4be4539e4ac458c652a26bc03/docs/planning/pr83-union-repro.py.
>
> So I'd suggest `merge=union` for `CHANGELOG.md` and the two `.jsonl` histories, and leaving `HANDOFFS.md`
> unattributed (small, marked conflicts, checked by `check-handoff --all`). Phase 1's merge test as written
> (*exit 0 … `check-handoff --all` green*) would go red with real receipts. If receipt conflicts turn out
> frequent, the per-session-files alternative is the one to revisit.
>
> Smaller notes:
> - **D5:** a fork's `main` is a trunk too. The seed already says a fork and its upstream each run their own
>   bare `S<N>`. I'd word it as "each repository's `main` is bare; `-<seq>` is for other branches".
> - **D6:** agreed, and dropping the 11 receipts is right. Those were my commits, and each is already
>   recorded in my fork's ledger. I'd add a per-merged-PR ledger check, because a merged commit with no
>   ledger line disappears below the frontier once a later commit touches the ledger (it happened to
>   `56997af`).
> - **D8:** agreed. Worth stating that Test 9's ~29 API calls per run trip GitHub's secondary limit when two
>   suites run at once (seen here, while `rate_limit` read 5000/5000). That is relevant to the concurrent run
>   in Phase 5.
> - **D14:** agreed on a new FM. I've seen the tendency twice more here — a review agent that wrote into a
>   distributed seed, and two concurrent suites tripping that limit — so the wording could cover shared
>   state, not only a shared tree.
> - **Item 12:** D1 adds a paragraph to Principle 9, and Phase 2 edits flight-manual Phase 1 step 4. "Adds
>   none, removes none" would be accurate where "does not touch" isn't.
> - **Budget:** my open PR on the changelog rules leaves `SAFEGUARDS.md` 17 tokens of headroom rather than 71,
>   so D2's row would be almost all reduction if that lands first.
>
> I agree with the rest as recommended. D11 I'd leave until Phase 5.

---

## 7. What this document does not do

- It posts nothing and answers nothing on the maintainer's behalf.
- It edits no framework file; the plan is untouched.
- It does not test GitHub's handling of `merge=union` (outward: a scratch PR), the two `.jsonl` files, or
  whether `methodology_trim.py` and a future `check-ledger` accept union's missing blank line.
- It does not re-derive the plan's §9 commands that bear on no position here: the dashboard's ledger-lag
  lines, `context_budget.py:867`, and `quality_ratchet.py`'s `find_root`.
