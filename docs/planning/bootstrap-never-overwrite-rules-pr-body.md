# Pull-request body — the prose update route's ledger-protection rules

**Status:** DRAFTED, NOT SENT. Built at fork session S224 (2026-09-26/27) on branch
`fix/bootstrap-never-overwrite-rules`, tip `a88fce7`, based on `upstream/main` `6b29d3d`. Opening the pull
request is a separate operator go-ahead and is deliberately not part of the session that wrote this. The text
below the rule is the body; everything above it is fork-side scaffolding and must not be sent. An edit to this
file is not an edit to a pull request.

**This closes the upstream half of UAT F2 (CRITICAL)** — the fork-only fix from `12463dd` (2026-08-04),
re-derived against `upstream/main` rather than cherry-picked. It is the fork item BL-85.

**Suggested title:** The prose update route can wipe an adopter's ledgers: give the instruction the three rules
that stop it

**Recognized-terms check** (0 hits required). It reads only the body — everything after the first standalone
rule — because the pattern would otherwise match this very command:

```sh
sed -n '/^---$/,$p' docs/planning/bootstrap-never-overwrite-rules-pr-body.md \
  | grep -nE 'S[0-9]{2,3}\b|BL-[0-9]+|\bD[0-9]\b|UAT|fork Learning|12463dd'
```

**Measured before drafting** (each re-run, not carried):

- `grep -c 'never overwrite' starter-kit/BOOTSTRAP.md` — 0 on `upstream/main` and on all five open pull-request
  heads; 2 on fork `main` and on this branch.
- `bin/_manifest.py`'s `DISTRIBUTION` list is **identical** on the two trees, so rule 1's table ports unchanged.
  The manifests differ only in comments and in `STALE_FORMAT_MARKERS`.
- Rule 2 could **not** port verbatim: the fork's wording cites `ledger-format: 2` and `FRAMEWORK_APPARATUS.md`
  §The Action Ledger, neither of which exists on `upstream/main` (0 occurrences of *Action Ledger* in that file).
  Both arrive with #84. Rule 2 was therefore rewritten to **point at the existing migration paragraph** instead of
  restating it — which is also why it survives #84 unchanged.
- Rule 3's five verdicts read from `upstream/main`'s `bin/status`: `missing` `:95`, `current` `:98`,
  `N versions behind` / `1 version behind` `:102`, `locally modified` `:103`, `STALE_SEED` `:106`.
- The fork's closing *A note on `--source=github`* paragraph is **excluded**: it describes the route #87 changes.

**Merge measurements** (`git merge-tree --write-tree`, then the suite on the merged tree):

| against | result | merged tree |
|---|---|---|
| #84 `77afc12` | **CLEAN**, `BOOTSTRAP.md` included | **163 passed, 0 failed**; gates 10/10, `results 93ea168d093e` |
| #87 `67feb9f` | `CHANGELOG.md` only; `BOOTSTRAP.md` auto-merges | **188 passed, 0 failed**, floor 188 met exactly; gates 10/10, `results 2162213f5332` |
| #83, #85, #86 | `CHANGELOG.md` only | not run — the collision is the prepend-only ledger's, resolved by keeping both entries |

**Observed and deliberately NOT fixed** (failure mode #17), to be raised separately if wanted: the
§Setup with `bin/sync` prose at `:74` lists the installed operating files but omits `methodology_trim.py`,
`context_budget.py` and `quality_ratchet.py`, and its seed list omits `.context-budget.json` and
`.quality-gates.json` — both stale against the manifest this branch's table is derived from. Fixing it here would
put a second, larger edit in a pull request whose point is one section.

---

## The defect

`starter-kit/BOOTSTRAP.md` §Without `bin/sync` is one sentence:

> Tell your agent: *"Update methodology using https://github.com/KJ5HST/methodology"*. It will fetch the latest
> starter-kit files and overlay them.

It names no exception, and six of the files it tells the agent to overlay are seeds: `CHANGELOG.md`,
`HANDOFFS.md`, `SESSION_NOTES.md`, `ROADMAP.md`, `.context-budget.json` and `.quality-gates.json`. An agent that
follows the sentence literally replaces the adopter's action ledger and every close-out receipt with empty
templates.

`bin/sync` has never had this defect. `bin/_manifest.py` classes those six as seeds and installs them once, and
`bin/sync` refuses to overwrite them by construction. **The gap is only in the prose route — which is the route
this very section tells people to use**, and for an adopter with no sibling checkout it is the only route there
is. The fix is delivered by the instruction that is broken: following it to get the corrected text overwrites the
ledgers first.

An acceptance test across six adopter projects rated this critical and measured the exposure. Three of them were
inspected directly and held identical text; their `CHANGELOG.md` / `HANDOFFS.md` pairs were 42 KB / 70 KB,
150 KB / 112 KB and 474 KB / 1.1 MB. The protection had reached **none of the six**.

## What this changes

One section of one file. The instruction stays exactly as it is; three numbered rules follow it.

**1. Overlay the tracked files; never overwrite the adopter-owned ones.** A two-row table splitting the
distribution, with the consequence of getting it wrong in the sentence beneath it rather than left implicit. The
rows are derived from `bin/_manifest.py`'s `DISTRIBUTION` list, not written from memory.

**2. Reconcile the adopter-owned files by hand, because nothing else will.** Never overwriting them means a
project moving up from an earlier version keeps its ledgers in their old *format* — new behaviour, missing
structure. This rule **points at the *Updating an existing project from an earlier methodology version* paragraph
in §Setup with `bin/sync`** rather than restating the migration, so the two cannot drift apart and this section
needs no edit when that paragraph changes.

**3. Verify afterwards, don't assume.** `bin/status` and the five verdicts it prints, with the one that means
rule 2 is still owed called out.

## Why it is prose and not a mechanism

Because the failure is a prose instruction being followed correctly. There is no code path to guard: the agent
never runs `bin/sync`, so no refusal in `bin/sync` can reach it. The only thing standing between the instruction
and an overwritten ledger is what the instruction says, which is what this changes.

## Verification

Measured on the branch, and again on the merged trees:

- `bash bin/tests.sh` — **139 passed, 0 failed**, unchanged from the base commit; **163/0** merged with #84;
  **188/0** merged with #87, where the raised floor of 188 is met exactly.
- `bin/check-links` — OK, 107 relative links across 23 distributed markdown files.
- `python3 starter-kit/context_budget.py --precommit` — exit 0.
- `python3 starter-kit/quality_ratchet.py --run` — **10/10 pass, 0 fail, 0 unmeasured**,
  `results 6542e640a956 · manifest 97a7aab85b9a` on the branch; 10/10 on both merged trees.

No gate moves: the change is prose in one file and adds no tests.

## Deliberately not in this pull request

- **The `--source=github` note.** The fork's version of this section closes with a paragraph about that route.
  It describes behaviour #87 changes, so it belongs with that work, not here.
- **The stale file lists in §Setup with `bin/sync`.** Noted above; a separate, larger edit.
- **Any change to `bin/sync`, `bin/status` or the manifest.** They already behave correctly; only the prose did not.
