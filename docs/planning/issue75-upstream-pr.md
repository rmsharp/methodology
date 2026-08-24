# Prepared upstream PR — issue #75 (plan-time verification SURFACE)

**Status: PREPARED, NOT SENT.** Nothing has been pushed and no pull request exists. Sending is an
outward-facing action and needs the operator's explicit go-ahead, per `CLAUDE.md` §Contributing
upstream. This file is fork-only (`docs/planning/`) and never travels upstream.

Written by S102 (2026-08-24). The branch it describes is real and committed; every number below was
measured on that branch, not on fork `main`.

---

## What exists right now

| | |
|---|---|
| **Branch** | `docs/issue75-plan-surface-upstream` — local only, **not on `origin`** (verified with `git ls-remote --heads origin`) |
| **Base** | `upstream/main` = `512c2ed` (KJ5HST/methodology) |
| **Commit** | `60246e7` — one commit, ahead 1 |
| **Diff** | 3 files, +172 / −1 |
| **Target issue** | [#75](https://github.com/KJ5HST/methodology/issues/75), filed 2026-08-14 by KJ5HST, still open |

Files in the commit:

- `starter-kit/SESSION_RUNNER.md` (+7/−1) — **DISTRIBUTED** (`bin/_manifest.py` TRACKED). The change.
- `bin/tests.sh` (+130) — canonical-only, but **not fork-only**; it exists upstream. Test 26.
- `CHANGELOG.md` (+35) — upstream's own action ledger, per FM #27 and the precedent set by
  `fix/handoffs-receipt-spec-upstream` and `fix/caveman-length-citation-upstream`.

## To send it (operator, after a go-ahead)

```sh
git push origin docs/issue75-plan-surface-upstream
gh pr create --repo KJ5HST/methodology \
  --base main --head rmsharp:docs/issue75-plan-surface-upstream \
  --title "[issue #75] Require each plan phase to name its verification SURFACE" \
  --body-file docs/planning/issue75-upstream-pr-body.md
```

Push to **`origin`** (rmsharp/methodology), never to `upstream` — see
`project_repo_branching_pattern`. The PR body is the sibling file
[`issue75-upstream-pr-body.md`](issue75-upstream-pr-body.md), kept separate so it can be passed to
`--body-file` unedited.

---

## Three decisions taken, each reversible before sending

**(1) Two sites, not the one-line diff the issue drafted.** All six pre-existing checklist items
mirror a requirement stated in a section above them — checked mechanically, not assumed. A checklist
line with nothing behind it would be the list's only orphan. So the requirement is *stated* in
§Per-Phase Completion Criteria and *verified* by the checklist. **This is the most likely point of
maintainer pushback**, and it is already flagged in the 2026-08-16 comment on the issue. Re-run the
six-item check before arguing it.

**(2) The new prose QUOTES gate (d) rather than restating it.** Two copies of one rule drift; a
quotation cannot. It also creates a citation that can dangle, which is what Test 26 exists to catch.

**(3) Learning #29 is NOT in this PR — a deliberate exclusion, not an oversight.** In the fork the
#75 work also appended a framework learning (*a rule is only as reachable as the section it sits
in*) to `starter-kit/FRAMEWORK_LEARNINGS.md`. **That file does not exist upstream** — upstream's
learnings still live as a table inside `SESSION_RUNNER.md`, 13 rows, so the row would be **#14**
there and would edit a numbered set that upstream's own Tests 23/24 pin. Excluded to keep this a
one-issue PR the maintainer can review in one sitting. It is a one-row append if he wants it; raise
it as a follow-up rather than widening this PR.

## What is deliberately NOT in the branch, and why it matters

Fork `main`'s `starter-kit/SESSION_RUNNER.md` differs from `upstream/main` in **FIVE** hunks. Only
**two** are issue #75. The other three are unrelated fork work that has never shipped upstream:

1. Phase 3C rerouted to `FRAMEWORK_LEARNINGS.md`
2. the `**Model:**` ledger bullet in Phase 3F
3. the Learnings table replaced by a pointer to `FRAMEWORK_LEARNINGS.md`

All three depend on `starter-kit/FRAMEWORK_LEARNINGS.md`, **which does not exist upstream** (neither
does `starter-kit/methodology_trim.py`). **A whole-file take would have carried three unshipped
changes into a one-issue PR.** The branch was built by applying `b1b7eaf`'s patch for that file
alone, which applies cleanly to `upstream/main` (`git apply --check` passed).

**Test numbering collides between the two repos and had to be re-derived.** The fork's Tests 32/33/34
*are* upstream's Tests 23/24/25; upstream's highest numbered test is **25** (its `bin/tests.sh` is
650 lines against the fork's 2,981). The fork's Test 36 is therefore **Test 26** upstream. Its
fork-only references were rewritten, not carried: `BL-10` and the fork session ids are gone, and the
citation census is stated as the **commands that reproduce it** rather than as line numbers that will
drift.

## Verification — run on the branch, which is the surface that matters

Running the fork's suite would prove nothing about a tree built from `upstream/main`. This is the
requirement issue #75 itself adds, applied to its own PR.

| Stage | Result |
|---|---|
| Pre-change control, pristine `upstream/main` | **114 passed / 0 failed**, exit 0 |
| RED — test added, runner unpatched | **5 of Test 26's 6 rows FAIL**; populations non-empty (`POP crit=390 items=6 slice=5469`). The 6th row is the population-guard control, which must pass either way. |
| GREEN — final branch state | **120 passed / 0 failed**, exit 0 |
| Row-for-row diff, both populations non-empty | exactly **6 rows added, ZERO lost** |
| `bin/check-links` | OK — 83 relative links / 21 distributed files |
| `bin/check-learnings` | OK — 13 rows, contiguous 1..13, all citations resolve |
| Adopter smoke (`bin/sync` into a fresh `git init`) | delivered `SESSION_RUNNER.md` **byte-identical**; 7 checklist items; **both** occurrences of the quoted phrase, so the citation's referent travels in the same file and cannot dangle at an adopter merely by being synced |

**What none of this exercises:** GitHub delivery, review, or merge. No network path was tested,
because none can be without sending something.

## The census behind the finding, reproducible

Measured on `upstream/main` **before** the change — both spellings, because one spelling is one
sample:

```sh
git grep -c "Faithful verification, per surface" upstream/main   # 1  — its own definition
git grep -n  "gate (d)"                          upstream/main   # 0
git grep -n  "gate d"                            upstream/main   # 1  — INSIDE gate (d)'s own section
```

Nothing outside §Vertical Slice Sessions referred to gate (d) in either spelling. Upstream is a
*cleaner* case than the fork, where one citation existed
(`docs/planning/b1-sync-coverage-expansion-plan.md`, a fork-only file). The 2026-08-16 comment on the
issue stated the fork's count; **this is the count for the tree the PR targets**, and it is the one
the PR body uses.

## Housekeeping

The branch was built in a temporary `git worktree` under the session scratchpad, which was removed
after committing. **The branch itself persists** in `refs/heads/` and is checked out normally:

```sh
git checkout docs/issue75-plan-surface-upstream
```
