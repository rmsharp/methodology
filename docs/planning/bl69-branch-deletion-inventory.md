# BL-69 — the branch deletion inventory, re-derived at S234

**Purpose.** [BL-69](BACKLOG-DETAIL.md#bl-69) was decided by the operator at S189 (picker, 2026-09-18)
and not executed. Its own *How, when it runs* paragraph says **"Re-derive every claim above first;
branches move."** This file is that re-derivation, taken at S234 (2026-09-28) at `main` = `bcd990a`,
`origin/main` = `4c5905b`, `upstream/main` = `6b29d3d`. It exists because the action is **destructive and
partly outward-facing**, and because the S189 list **predates four of the six pull requests now open**.

Fork-only: `docs/planning/` is not in `bin/_manifest.py`, so no adopter receives this file.

## 1. What changed since S189, and what did not

**Nothing moved.** All 21 candidate refs — 10 local, 11 on `origin` — stand at **exactly** the shas
S189 recorded. That is the one claim in BL-69 that could have rotted quietly and did not.

**What did change is the surrounding state, and it is what makes the S189 list unsafe to apply
verbatim: six pull requests are open upstream and FIVE OF THEM HAVE THEIR HEAD ON THIS FORK'S `origin`.**
S189 knew of one (#83, whose head is upstream's own branch) and of #84. The other four — #85, #86, #87,
#88 — were opened after it. None is a deletion candidate, and the mapping below is how that is
established rather than assumed.

| Pull request | State | Head | Disposition |
|---|---|---|---|
| #83 | open | `KJ5HST/docs/parallel-sessions-plan` `219fb9d` | not ours; local `pr83` is a read-only copy at the same sha |
| #84 | open | `rmsharp/bl57/changelog-rules` `77afc12` | **KEEP** — also checked out in the `methodology-bl57` worktree |
| #85 | open | `rmsharp/fix/pre-commit-stale-rebase-marker` `e2501c5` | **KEEP** |
| #86 | open | `rmsharp/fix/context-budget-status` `c1167ae` | **KEEP** — never rebase or force-push |
| #87 | open | `rmsharp/fix/sync-github-history` `67feb9f` | **KEEP** |
| #88 | open | `rmsharp/fix/bootstrap-never-overwrite-rules` `a88fce7` | **KEEP** |

`docs/issue75-plan-surface-upstream` `60246e7` is **KEPT** by the S189 decision itself ([BL-70](BACKLOG-DETAIL.md#bl-70)).

## 2. The 10 local candidates

`anc` = `git merge-base --is-ancestor <ref> upstream/main`. Where `anc` is *no*, the work's survival is
established by a same-subject commit **searched in `upstream/main` alone** — the first measurement of this
was run with `git log --all --grep`, which matched each branch against itself and returned a uniform
*survives*; the tell was `docs/bl-10`, whose pull request closed unmerged, coming back green.

| # | branch | sha | sha == S189 | anc(upstream/main) | survives as | flag |
|---|---|---|---|---|---|---|
| 1 | `fix/bl31-context-budget-dashboard-exclusion` | `9845b4d` | yes | no | `473ec82` | `-D` |
| 2 | `fix/caveman-length-citation-upstream` | `f1dd996` | yes | no | `b4ceb73` | `-D` |
| 3 | `fix/dashboard-r-quarto-rmarkdown-extensions` | `6380139` | yes | no | `736b0a7` | `-D` |
| 4 | `fix/doc-only-thresholds-upstream` | `b52c1a9` | yes | no | `86adc6c`, `9663153` | `-D` |
| 5 | `fix/handoffs-receipt-spec-upstream` | `311c554` | yes | no | `dc3b405`, `33d8c64` | `-D` |
| 6 | `docs/bl-10-dangling-learning-citations` | `268f1e5` | yes | no | `upstream refs/pull/64/head` | `-D` |
| 7 | `port/framework-learnings-extraction` | `7d5b186` | yes | no | see §4 | `-D` |
| 8 | `pr80/f1-learnings-1-13` | `d4e1570` | yes | **yes** | ancestor | `-d` |
| 9 | `pr80/f2-installed-source-guard` | `3774076` | yes | **yes** | ancestor | `-d` |
| 10 | `pr80/f3-read-set-token-ceilings` | `aa36fd8` | yes | **yes** | ancestor, and **is** `upstream/read-set-budgets` | `-d` |

## 3. The 11 `origin` candidates

| # | branch | sha | sha == S189 | anc(upstream/main) | pull request |
|---|---|---|---|---|---|
| 1 | `fix/bl31-context-budget-dashboard-exclusion` | `b2ef20a` | yes | yes | #71 merged |
| 2 | `fix/caveman-length-citation-upstream` | `b4ceb73` | yes | yes | #68 merged |
| 3 | `fix/dashboard-r-quarto-rmarkdown-extensions` | `c4fd879` | yes | yes | #72 merged |
| 4 | `fix/doc-only-thresholds-upstream` | `86adc6c` | yes | yes | #70 merged |
| 5 | `fix/handoffs-receipt-spec-upstream` | `dc75cf6` | yes | **no** | #69 merged — rebased, so not an ancestor; see §3.1 |
| 6 | `pr1/framework-learnings-extraction` | `5b92b2f` | yes | yes | #76 merged |
| 7 | `pr2/ledger-trimmer` | `56997af` | yes | yes | #77 merged |
| 8 | `pr3/apparatus-extraction` | `2c30d0f` | yes | yes | #78 merged |
| 9 | `pr4/context-budget-gate` | `cf15489` | yes | yes | #79 merged |
| 10 | `docs/learning-13-handoff-predictions` | `73b72c0` | yes | yes | #63 merged |
| 11 | `docs/bl-10-dangling-learning-citations` | `268f1e5` | yes | **no** | #64 **closed unmerged** — retained as upstream `refs/pull/64/head` |

### 3.1 The one `origin` sha that no pull ref retains, and why it still loses nothing

**Every affected pull request's head is retained on upstream as `refs/pull/<N>/head`** — checked with
`git ls-remote upstream` for #63, #64, #68–#72 and #76–#79, all eleven present. **Ten of them are the same
sha as our `origin` copy. #69 is not:** upstream retains `dc3b405`, while `origin` carries `dc75cf6`.
So deleting that one branch is the only deletion in this whole item that makes a commit unreachable
everywhere.

It still loses nothing, and this is measured rather than assumed:

- **The tip commits are patch-identical** — `git patch-id --stable` gives `e4d76b99…` for both `dc75cf6`
  and `dc3b405`.
- **Their parents' patch-ids differ** (`6f543e0` `8ccfffbc…` vs `33d8c64` `077fee14…`) **and that
  difference is hunk offsets, not content**: diffing the two commits' added and removed lines in
  `starter-kit/HANDOFFS.md` — the distributed file the pair exists to fix — returns nothing. The
  `CHANGELOG.md` halves differ because the two commits sit on two different ledgers.

This confirms S189's claim for this branch (*"the changed lines were compared: identical"*) and extends it
from the local-vs-`origin` pair to `origin`-vs-upstream's retained head.

Deletion on `origin` runs only at the recorded sha:
`git push --force-with-lease=refs/heads/<b>:<sha> origin :refs/heads/<b>`, then `git fetch --prune origin`.

## 4. The one branch whose tip has no other home — adjudicated, not waved through

`port/framework-learnings-extraction` `7d5b186` is **local only**: no `origin` copy, no pull request, not
an ancestor of either `main`. Its parent `30ddf26` (*extract the Learnings table*) survives upstream as
`5b92b2f` (#76, merged). **Its tip does not.** That tip is a `CHANGELOG.md`-only commit (+11 / −10) that
rewrites one bullet counting backticked referents which resolve to nothing.

The port version reads **eight artifacts across 11 of 46 rows**, with per-row citations; `main`'s copy — in
the frozen shard [`docs/archive/CHANGELOG-through-2026-09-02.md`](../archive/CHANGELOG-through-2026-09-02.md) — reads
**seven across 10 of 46**. **These are not a correction of each other.** The bullet's subject is *"this
tree"*, and the two commits sit on two different trees, so each count is true of the tree it was measured
on. The port tree ceases to exist with the branch, so the measurement is **superseded, not lost** — and
`main`'s shard is not wrong and must not be edited, being frozen under a losslessness proof.

This is also why no note is owed upstream: the byte-identity property the port branch was held to is
adjudicated in [`port-branch-identity-adjudication.md`](port-branch-identity-adjudication.md) §2 — *"no
consumer exists — the identity is asserted, never read."*

## 5. What this does not fix

After the deletions `git branch -a` still reads about 10, so the dashboard's *"Multiple branches"* signal
still fires. That is [BL-71](BACKLOG-DETAIL.md#bl-71) — the signal counts `git branch -a`, including HEAD
aliases and upstream's own refs, so a fork can never clear it — and it is not a failure of this work.
