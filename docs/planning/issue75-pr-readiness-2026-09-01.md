# Issue #75 PR — readiness verification (S135, 2026-09-01)

**Payload:** candidate D, branch `docs/issue75-plan-surface-upstream` (`60246e7`).
**Scope chosen by the operator** at the Phase 1 gate; **stop point: everything up to push.**
**Nothing left this machine** — no push, no PR, no comment, no upstream write of any kind.

---

## Branch position

| Property | Value |
|---|---|
| Base | `upstream/main` = `512c2ed` (2026-08-11) — the current tip |
| Ahead / behind | **1 / 0** |
| Merges into `upstream/main` | **clean** — `git merge-tree --write-tree` exit 0 |
| Diff | 3 files, **+172 / −1** |
| Files | `starter-kit/SESSION_RUNNER.md` (distributed), `bin/tests.sh` (canonical-only), `CHANGELOG.md` (upstream's, +35) |
| Pushed anywhere | **no** — `git ls-remote --heads origin` carries no `docs/issue75*` |

It carries **upstream's** `CHANGELOG.md`, not the fork's. No fork-local path appears in the diff.

## Verification — every figure in the drafted PR body, re-run today

The body at [`issue75-upstream-pr-body.md`](issue75-upstream-pr-body.md) publishes seven measurements to
the maintainer. All seven were re-derived in **fresh `--no-local` clones** — control at `512c2ed`, branch
at `60246e7` — never in the live repo, because Tests 32/34/37 mutate live ledgers.

| Body claim | Re-derived | Verdict |
|---|---|---|
| Pre-change control, pristine tree — 114 passed / 0 failed | `114 passed, 0 failed`, exit **0** | ✅ |
| GREEN final state — 120 passed / 0 failed | `120 passed, 0 failed`, exit **0** | ✅ |
| Row-for-row vs control — exactly 6 rows added, zero lost | 114 → 120 rows; **0 lost, 6 added**, all six Test 26's | ✅ |
| RED — 5 of Test 26's 6 rows fail | reconstructed RED: **5 FAIL / 1 PASS** in Test 26 | ✅ |
| RED populations non-empty — `crit=390 items=6 slice=5469` | identical, to the digit | ✅ |
| `bin/check-links` — 83 links / 21 distributed files | exit **0**, same string | ✅ |
| `bin/check-learnings` — 13 rows, contiguous 1..13 | exit **0**, same string | ✅ |
| Adopter smoke — byte-identical, 7 checklist items, **both** phrase occurrences | sha256 match; **7**; **2** | ✅ |

Every exit code read **bare on the next line**, never through a pipe.

**One artifact of my own reconstruction, recorded so nobody re-finds it as a defect.** The RED tree
(branch `bin/tests.sh` + control `SESSION_RUNNER.md`) also fails `Test 6: status: N-behind not detected`,
giving a 6-failure summary. That is caused by hand-copying a file into the tree, which confuses
`bin/status`'s version comparison. Test 6 passes in both real trees. The body's claim is scoped to Test
26's rows and is exactly right; **my first count of "4 of 6" was a `grep -A12` truncation, not an error in
the body.**

## Commit-message claims, measured against the pre-change tree

`60246e7`'s message publishes three grep counts as evidence that gate (d) was an orphan. Measured at
`512c2ed`, not at HEAD:

| Claim | Measured |
|---|---|
| `grep -c "Faithful verification, per surface"` → 1 | **1** ✅ |
| `grep -n "gate (d)"` → 0 | **0** ✅ |
| `grep -n "gate d"` → 1 | **1** ✅ |
| Checklist 6 → 7 items | control **6**, branch **7** ✅ |
| The new quotation's referent resolves on the branch | **2** occurrences ✅ |

## Status of the drafted PR body

**Send-ready as written; no edits needed.** It opens `Closes #75`, matches the branch exactly, discloses
its AI authorship, states its own honest caveat (*"this is a requirement, not a gate"*), and names two
deliberate omissions (the Learnings row; the issue's two *Related* items).

## ⚠ The one thing that is not a technical question

Issue #75 was filed by **KJ5HST (the maintainer)**. On **2026-08-16** this fork commented a full analysis
and closed it with:

> *"Entirely your call whether you'd like it offered as a PR or would rather write the checklist line
> yourself as you suggested — happy either way, and **I won't send anything unasked.**"*

**The maintainer has not replied.** The issue's last activity is that comment — ~16 days.

So opening this PR now would contradict a commitment this side made in public, on the maintainer's own
issue. That is an operator decision, not a session's, and it is **not** a technical blocker: the payload
is verified and ready either way. The options, stated without a recommendation being acted on:

1. **Wait** for a reply — honours the commitment literally; the PR keeps indefinitely, nothing rots
   (the branch is 0 behind and merges clean; re-check both before opening).
2. **Ask on the issue** — a short comment asking whether he'd like the PR now. This is itself an
   outward-facing action and needs its own go-ahead.
3. **Open it anyway**, with the body acknowledging the earlier commitment. Defensible — the issue's own
   text says *"Happy to open a PR for the checklist line if the direction is right"* — but it is a
   reversal of an explicit undertaking and should be a deliberate one.

Precedent that makes this worth pausing on rather than assuming: **PR #64 was opened without
authorisation and closed at the operator's instruction.**

## What is NOT in this package, deliberately

No fork cleanup of any kind. S134 established — and three independent adjudicators confirmed — that the
fork's retention breach, its 148,602 B `CHANGELOG.md`, its five red `docs/archive/*.verify.sh` proofs and
its three unproven archives all sit on paths absent from this diff and absent from `bin/_manifest.py`'s
SOURCE column. **They cannot travel upstream and were never prerequisites.**
