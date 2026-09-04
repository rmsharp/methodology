# Merge plan — pull `upstream/read-set-budgets` (PR #79 merged) into fork `main`

**Status: DRAFT, self-reviewed, awaiting the operator's go-ahead for Phase B.** Written S150
(2026-09-04), resuming a claim opened and then correctly halted the same day (the operator's *"in
the next session make a plan to complete the merge as you have described"* names this plan, not an
immediate merge). **This plan document is the session's one deliverable** (`SESSION_RUNNER.md`
§Planning Sessions; FM #18) — no merge, no push, no upstream action taken while writing it.

## 0. The answer, in one paragraph

The four PRs of the read-set-budgets series (`#76`–`#79`) are all merged into
`KJ5HST/methodology:read-set-budgets` (tip `598c459`), but that branch has never been merged into
fork `main`, which has spent the whole series building the *same* capabilities independently and
in parallel. Pulling it in is a **real 3-way merge** (`git merge upstream/read-set-budgets
--no-commit`, never a strategy shortcut), resolved **file by file** against the table in §2.2: 13
paths keep fork's own content outright (it is a superset — later, more advanced, or already proven
by fork's own tests), 3 paths take upstream's content outright (deliberately de-fork-ified
modules, or a pointer paragraph that names more than fork's own), 2 are exceptions decided on
their own terms (fork's own root config stays per an existing ratification; one stale count on
both sides gets recomputed, not chosen), and the two ledgers (`CHANGELOG.md`, `HANDOFFS.md`) are
interleaved by date per the convention their own front matter already documents. Verification is
the existing checker suite (`bin/tests.sh`, `check-handoff --all`, `check-links`,
`check-learnings`, the three canonical `unittest` modules) plus a same-blob re-check on the two
files this repo cannot touch without going stale (`context_budget.py`, `methodology_trim.py`).
**Executing this merge is Phase B, a separate session, and needs its own explicit go-ahead** — the
same rule PR 4's own Phase C and Phase D lived under.

## 1. Target, and two corrections to the record

**Target:** `upstream/read-set-budgets` = `598c459` (merge commit, PR #79, merged
`2026-09-04T01:24:30Z` by rmsharp, parents `cea3068` + `cf15489`) — [`KJ5HST/methodology#79`](https://github.com/KJ5HST/methodology/pull/79).
`read-set-budgets` is not on `upstream/main` (`512c2ed`); `upstream/main` **is** an ancestor of
`read-set-budgets` (`git rev-list --count upstream/read-set-budgets..upstream/main` = 0), so this
merge also carries everything on `upstream/main` that fork `main` lacks (one commit,
`512c2ed`, upstream's own S12 receipt — folded into §2.3).

**Correction 1 — the interrupted S150 stub's conflict count was an unverified guess.** Its
`active_task` field said *"20 conflicting paths (5 add/add, 15 content)"*. Measured (below), it is
**20 conflicting paths, 4 add/add + 16 content**. The total was right; the breakdown was not, and
was never run before being written — exactly the failure this repo's own Learning #50 describes.

```
$ git merge-tree --write-tree --name-only main upstream/read-set-budgets
a9b72fee7262430358538babdb096a652dcbe38c        # the virtual merge tree's OID
CONFLICT (add/add): … .context-budget.json
CONFLICT (content): … .gitignore
… [18 more lines, one per path in §2.2] …
$ # exit 1; 20 CONFLICT lines, 4 "add/add", 16 "content"
```

**Correction 2 — the ratified `pr4-read-set-budgets-plan.md` D11 undercounted PR 4's own share by
one.** D11 says merging `cea3068` into fork `main` with no PR 4 at all conflicts on **17** paths
(verified again here, unchanged: `git merge-tree --write-tree --name-only main cea3068` → the same
17, minus `.gitignore`, `.context-budget.json` and `tools/test_context_budget.py` from today's 20)
and that PR 4 adds *"two more, 19 in all"* — `.context-budget.json` and
`tools/test_context_budget.py`. **PR 4 actually adds a third: `.gitignore`**, per that same plan's
own §3.6 (*"seven comment lines, optional but recommended"* — part of what PR 4 carries). `17 + 3 =
20`, exactly today's measured count. This is a correction to a ratified, closed document, so it is
recorded here rather than edited into `pr4-read-set-budgets-plan.md` — this repository's own
convention for a known-wrong figure in closed prose (`docs/planning/BACKLOG.md`'s *"deliberately
NOT edited (FM #17)"* rule for BL-9's own count errors).

## 2. Evidence-based inventory

### 2.1 Auto-merged set — 90 paths, no manual resolution

`git diff --name-only main upstream/read-set-budgets` lists 110 differing paths; 20 conflict (§2.2)
and **90 do not**, because git's 3-way merge finds non-overlapping hunks or one side has no history
of the path at all:

- **86 paths exist only on fork `main`** — every `docs/planning/*.md`, `docs/archive/*`,
  `docs/audits/*`, `docs/RELEASE_HISTORY.md`, `dashboard_history.jsonl`,
  `.context-budget-history.jsonl`, `bin/model-report`, and the `BACKLOG*` files, among others. Pure
  fork-side operational history and tooling upstream's branch has no copy of at all; the merge adds
  nothing to and removes nothing from these, in either direction.
- **4 paths exist on both sides, differ, and still merge cleanly**, because each side's edits land
  in different hunks of the same file: `.githooks/pre-commit`, `bin/check-handoff`, `bin/sync`,
  `starter-kit/SESSION_RUNNER.md`. (First-draft arithmetic here guessed 76/14 without checking which
  side actually has each path — verified by testing `git cat-file -e upstream/read-set-budgets:<path>`
  per path below; the true split is 86/4, not 76/14. Left as a worked example of the same "run it,
  don't predict it" discipline Correction 1 already applies to the conflict-count claim.)

**A clean auto-merge is not proof of correctness — re-verify it, don't just accept it.** Phase B
re-runs the full checker suite (§2.4) after the merge specifically because a non-conflicting hunk
can still combine into something semantically wrong (two independently-true sentences that
contradict once adjacent). Re-derive the auto-merged list:

```sh
comm -23 <(git diff --name-only main upstream/read-set-budgets | sort) \
         <(printf '%s\n' .context-budget.json .gitignore CHANGELOG.md CLAUDE.md HANDOFFS.md \
           HOW_TO_USE.md ITERATIVE_METHODOLOGY.md README.md bin/_manifest.py bin/check-learnings \
           bin/tests.sh docs/tutorials/T1_setup.md docs/tutorials/T8_keeping_current.md \
           starter-kit/BOOTSTRAP.md starter-kit/FRAMEWORK_LEARNINGS.md \
           starter-kit/methodology_dashboard.py tools/methodology_dashboard.py \
           tools/test_context_budget.py tools/test_methodology_dashboard.py \
           tools/test_methodology_trim.py | sort)
```

**Two payload files that merge cleanly *because* fork built them twice, on purpose.**
`starter-kit/context_budget.py` and `starter-kit/methodology_trim.py` do **not** appear as
conflicts, or even in the 110-path diff at all past the tool files already listed — because fork
`main`'s own copy and the copy PR 2/PR 4 shipped upstream are **byte-identical**
(`context_budget.py` blob `d91677b5` both sides; `methodology_trim.py` `diff <(git show
main:…) <(git show upstream/read-set-budgets:…)` is empty). This is deliberate: the S147/S148
build recipe rebuilds each payload tool in a clean upstream-based clone to the *same end-state
blob* fork's own history already reached, rather than replaying fork's commit history verbatim, so
the tool itself never conflicts — only the surrounding docs and tests that reference it by session
number do (§2.2). Worth naming as the pattern, not just the outcome: **build once, port the
end-state blob, and the payload file is immune to this whole class of conflict.**

### 2.2 Conflicting paths — 20, each with a resolution rule and a verification command

| # | Path | Kind | What each side did | Resolution | Verify |
|---|------|------|---------------------|------------|--------|
| 1 | `.context-budget.json` | add/add | Fork: its own root config (29,813 B, this repo's own ceilings). Upstream: PR 4's candidate config for *upstream's* tree. | **Keep ours.** Ratified at S146, `pr4-read-set-budgets-plan.md` §4 D11: *"the fork keeps its own root config… nothing changes for the fork on merge day."* The two configs govern different repos' file trees and are not reconcilable into one. | `git show :1:.context-budget.json \| cmp - .context-budget.json` (stage-2/ours) before commit; `context_budget.py` bare run exits 0 after. |
| 2 | `.gitignore` | content | Both added the same 7-comment block explaining why the two `.jsonl` series are tracked; wording differs only in one clause (fork: *"so it is tracked"*; upstream: *"so it can be tracked… the authoring fork does"*, hedged for a generic reader). | **Keep ours.** Fork's direct wording is accurate for fork's own file; upstream's hedge exists for an audience (adopters) this file isn't distributed to. | `git status --porcelain` shows `.context-budget-history.jsonl` and `dashboard_history.jsonl` still untracked-by-ignore (i.e. still tracked) after merge. |
| 3 | `CHANGELOG.md` | content | Fork: 3,070 fork-only lines since the merge-base. Upstream: 188 lines — its own S9–S12 narration (release, issue #67) plus PR #76–79's own upstream-side entries. | **Interleave by date** — see §2.3. Not a pick-one file. | §2.4's full checker pass; `grep -c '^### [0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}' CHANGELOG.md` before/after accounts for every entry on both sides (no silent drop). |
| 4 | `CLAUDE.md` | content | Fork: the "Contributing upstream" section, the apparatus/learnings/trimmer doc-hierarchy rows, the `docs/RELEASE_HISTORY.md` extraction (BL-9 L3) — 27 ins/31 del since base. Upstream: 3 ins/1 del, exactly the apparatus + learnings doc-hierarchy rows, already a strict subset of fork's. | **Keep ours.** Confirmed by direct grep: every line upstream's diff adds already exists in fork's current `CLAUDE.md`, verbatim or better (fork also names the extraction session, S130). | `grep -c 'FRAMEWORK_APPARATUS.md\|FRAMEWORK_LEARNINGS.md' CLAUDE.md` ≥ 2 after merge. |
| 5 | `HANDOFFS.md` | content | Fork: 529 ins/149 del since base (its own ~20 receipts). Upstream: 14 ins/3 del — one receipt, upstream's own **S12** (its own sequence, not fork's S12) completing a `pending`→`complete` v3.7-release stub, dated 2026-08-12. | **Interleave by date** — see §2.3. Upstream's S12 receipt is real, separate-sequence history and is kept, not dropped; by date it lands far down the file and the retention trim (§2.3) will archive it almost immediately, which is correct, not a loss. | `bin/check-handoff --all` clean; receipt count matches the interleave math exactly (old count + 1). |
| 6 | `HOW_TO_USE.md` | content | One sentence, same fact (apparatus extraction), fork's names the session (*"since S130"*), upstream's doesn't. | **Keep ours** — strictly more informative, same claim. | `grep -n 'FRAMEWORK_APPARATUS' HOW_TO_USE.md` still resolves (already true; unaffected either way). |
| 7 | `ITERATIVE_METHODOLOGY.md` | content | Both independently extracted ~332 lines to `FRAMEWORK_APPARATUS.md` (33 ins/332 del vs. 34 ins/332 del — the *same* extraction, done twice). Surviving inline pointer text differs: fork's is terser (*"Phase 2 step 8, Phase 6 steps 4–6 and its gate"*); upstream's names more (*"Phase 2 steps 6–8… its honest-accounting bullet… the Across the Full Series heading"*). | **Take theirs for this one sentence** — upstream's pointer is more specific about what actually moved, and nothing in fork's terser version is lost by naming more of it. Read the surrounding paragraph before resolving; this is the one prose conflict where "more detail" plausibly wins over "our version" on the merits, not on provenance. | Re-read the resolved paragraph for coherence (this is prose, not a count); confirm `FRAMEWORK_APPARATUS.md` still contains a section matching whichever step range is named. |
| 8 | `README.md` | content | Fork: 174 ins/6 del (a whole new corpus table, tutorials section, `.methodology-profile` documentation). Upstream: 6 ins/3 del, the same apparatus/learnings additions as CLAUDE.md, already present in fork's version (verified: `grep -c` on both target strings ≥ 1 each in fork's current file). | **Keep ours.** | Same grep as row 4, run against `README.md`. |
| 9 | `bin/_manifest.py` | content | Comment-only hunk. Fork's comment explains *why* a derived table replaced a hand-written tuple (S39') and separately flags, as a forward-looking note, that upstream's own PR #66 will add a third executable entry here. Upstream's side of this hunk is empty (just the unchanged `methodology_trim.py` line). | **Keep ours** — a superset comment; the tuple entry itself is identical on both sides in this hunk. | `python3 -c "import sys;sys.path.insert(0,'bin');import _manifest as m;print(len(m.DISTRIBUTION))"` → 27 (unchanged by this merge; PR 4 doesn't touch the manifest — confirmed, `bin/_manifest.py` is not in PR 4's §3 file list). |
| 10 | `bin/check-learnings` | content | Comment-only. Fork: *"`.context-budget.json` carries the full derivation."* Upstream: the same fact restated in three lines because the distributed corpus lacks that canonical-only file. | **Keep ours** — this file *is* canonical-only-adjacent (the comment is in a canonical tool referencing a canonical-only config that exists in this exact repo), so the short form is accurate here. | `bin/check-learnings` still exits 0 after merge (comment-only; behavior unaffected). |
| 11 | `bin/tests.sh` | content, 5 hunks | Fork's test numbering runs far ahead of upstream's (its Test 32 = upstream's Test 23, same test) because fork has many more tests before this point; comments differ in specificity (fork's cites its own test numbers and a named pre-existing caveat; upstream's is generic). One hunk is pure line-wrapping, functionally identical either way. | **Keep ours throughout** — same pattern as the `aa378ab` precedent (§2.3's citation): fork's version is a superset with working self-references; adopting upstream's renumbered comments would break fork's own internal test-number citations elsewhere in this file and in `CLAUDE.md`. | `bash bin/tests.sh` — full suite, see §2.4. Test count must not drop below the 304 baseline (below). |
| 12 | `docs/tutorials/T1_setup.md` | content | One sentence listing what `bin/sync` copies. Fork's list includes `methodology_trim.py`; upstream's omits it even though upstream's own `bin/_manifest.py` already ships that file (confirmed: `methodology_trim.py` is `TRACKED` on both sides, byte-identical). | **Keep ours** — upstream's own tutorial text is stale against upstream's own manifest; fork's is accurate. | `grep -c 'methodology_trim.py' docs/tutorials/T1_setup.md` = 1 after merge. |
| 13 | `docs/tutorials/T8_keeping_current.md` | content | *"24 distributed files"* (ours) vs. *"25 distributed files"* (theirs). | **Neither — recompute.** The real count today is **27** (`len(bin._manifest.DISTRIBUTION)`: 23 markdown + 4 non-markdown), so both stated numbers are already stale relative to fork's current manifest, for the ordinary reason that files keep getting added. Write the resolved sentence with **27**, not by picking a side. | `python3 -c "import sys;sys.path.insert(0,'bin');import _manifest as m;print(len(m.DISTRIBUTION))"` and hand-check the resolved sentence quotes that exact number. |
| 14 | `starter-kit/BOOTSTRAP.md` | content | Same list-omits-`methodology_trim.py` pattern as row 12. | **Keep ours**, same reasoning as row 12. | `grep -c 'methodology_trim.py' starter-kit/BOOTSTRAP.md` = 1 after merge. |
| 15 | `starter-kit/FRAMEWORK_LEARNINGS.md` | add/add | Fork: 86 lines, Learnings 1–54. Upstream (PR 1's ported snapshot): 79 lines — a strict prefix, missing rows 48–54 (fork added these after the PR 1 snapshot was taken; `diff` confirms every upstream line is an unmodified subset of fork's, nothing upstream-only). | **Keep ours** — a strict superset, verified by `diff` (only additions past upstream's tail, zero modifications to shared rows). | `bin/check-learnings` reports contiguous `1..N` with `N` unchanged from pre-merge (currently 53 — recount at merge time, this file grows every few sessions). |
| 16 | `starter-kit/methodology_dashboard.py` | content, 4 hunks | The real conflict in this set. Fork (`DASHBOARD_VERSION` 2.17.0) refactored `FRAMEWORK_INSTALLED_SOURCE` to be *derived* from a single `_FRAMEWORK_INSTALLED_CONTENT` dict (name → (version_re, signatures)), eliminating a drift class where the exclusion list and the content-verification table could disagree. Upstream (2.10.7) still carries the **older**, two-structure design from its own PR #66/#71 (BL-31) — a hand-written `FRAMEWORK_INSTALLED_SOURCE` tuple plus a separate `_FRAMEWORK_FILE_SIGNATURES` dict — which is exactly the drift-prone shape fork's later refactor eliminated. Both cover the identical 4 names (`methodology_dashboard.py`, `methodology_trim.py`, `context_budget.py`, `.context-budget.json`). | **Keep ours** — fork's design is a strict functional superset (same 4 names covered, same signature sets, provably immune to the specific drift bug upstream's own commentary describes) and is at a much later version with its own dedicated test coverage. This is *not* a data-loss risk: nothing upstream's design checks is left unchecked by fork's. | `python3 -m unittest tools.test_methodology_dashboard` (§2.4); confirm `md.DASHBOARD_VERSION` is fork's, unchanged; confirm the two twins (`starter-kit/` and `tools/`) stay byte-identical (`cmp`) as this file's own comments require. |
| 17 | `tools/methodology_dashboard.py` | content, 4 hunks | Byte-identical hunks to row 16 (this is the twin). | **Keep ours**, identical resolution to row 16. | `cmp starter-kit/methodology_dashboard.py tools/methodology_dashboard.py` after resolving both — must be silent (no diff). |
| 18 | `tools/test_context_budget.py` | add/add | Byte-identical except **6** lines: fork's copy still carries fork-relative identifiers (`BL-38`, `Test 35`, `S129`, `S119`, a `bin/tests.sh` line-range) that PR 4's D9 decision scrubbed to dates/generic phrasing for the upstream-facing copy (ratified `pr4-read-set-budgets-plan.md` §4 D9). | **Take theirs.** D11's own fork-side follow-on — *"back-port the four scrubbed lines so the two copies agree"* — is discharged BY taking upstream's module wholesale; there is nothing left to separately back-port once this merge lands. | `diff <(git show upstream/read-set-budgets:tools/test_context_budget.py) tools/test_context_budget.py` empty after merge; `python3 -m unittest tools.test_context_budget` 116 tests, `OK (skipped=2)`. |
| 19 | `tools/test_methodology_dashboard.py` | content | The single `DASHBOARD_VERSION` string-match test, mirroring row 16's version numbers (2.17.0 vs 2.10.7) plus fork's docstring explaining the historical S115 double-pin footgun. | **Keep ours** — consistent with keeping fork's dashboard.py (row 16); taking upstream's version string here while keeping fork's dashboard.py would make this test assert the wrong version and fail immediately. | `python3 -m unittest tools.test_methodology_dashboard` passes (same command as row 16). |
| 20 | `tools/test_methodology_trim.py` | add/add | The larger, previously-unflagged case. Upstream's version (2,259 lines) replaced fork's original real-commit-dependent `L1`/`L2`/`L3` fixtures (`020ba3f`, `7a71df0` — SHAs that exist **only** in this fork's own history) with portable **synthetic** fixtures reproducing the same structural properties, explicitly so the trimmer's own tests "run outside this fork" (PR 2's own title) — in any adopter clone or upstream's CI, where those two SHAs don't exist. Fork's own `main` (2,170 lines) never received this rewrite back. | **Take theirs.** This is the same pattern D9/row 18 already names for `test_context_budget.py` — a fork-authored portability improvement, made only on the PR branch, owed back to fork's own copy — just not previously written down as a named decision. Recorded here as the new instance rather than re-discovering it during Phase B. | `python3 -m unittest tools.test_methodology_trim` run **from the repo root** (not an isolated copy — several assertions read seed files via `git show HEAD:starter-kit/CHANGELOG.md` and need a real checkout); expect the fork's own current pass/skip counts, not upstream's, since upstream's copy predates fixes fork's `methodology_trim.py` has picked up since. |

*(Row 20's synthetic-fixture-adoption verification is genuinely new territory — unlike every other
row, this file has never run against fork's live tree before. Phase B budgets time to fix any
skip/fail this specific combination turns up; it is evidence-gathering the moment it runs, not a
predicted-clean result.)*

### 2.3 The two ledgers — the interleave rule, stated once

`CHANGELOG.md` and `HANDOFFS.md` are **prepend-ordered, newest-on-top** files both fork and
upstream have written to independently since they diverged. A raw 3-way merge cannot interleave two
independent prepend logs correctly — this repo has done this resync five times already
(`aa378ab`, `8b87086`, `232514e`, `fc4d297`, `699046c`, …, `git log --oneline --merges main | grep
-i upstream`), and the rule is already written into `CHANGELOG.md`'s own front matter: **"Two
session sequences share this ledger and their numbers collide… at a resync the two sequences stay
separate and unrenumbered, each incoming receipt is checked against ours before it is kept, and
within a shared date the fork's receipts precede the arriving upstream ones."**

Apply it exactly as the closest precedent (`aa378ab`, 2026-08-12) did:

1. **Never take one side wholesale.** `git merge upstream/read-set-budgets --no-commit`, then edit
   `CHANGELOG.md`/`HANDOFFS.md` by hand in the working tree — this is the one file class in this
   merge that is not "pick ours / pick theirs / recompute."
2. **Order by the entry's own date**, newest first; on a shared date, fork's entries precede
   upstream's (the documented tie-break).
3. **Check each upstream entry for a narrative duplicate** of something fork's own ledger already
   records from its side of the same event (the precedent's own example: upstream's BL-31/PR #71
   narration duplicated what fork's BL-31 entries already covered, and was dropped). This merge's
   own §2.2 rows already establish that PR #76–79's fork-side narration and upstream-side narration
   describe the *same four merges* from two different vantage points ("we opened PR #79" vs.
   "merged PR #79 from rmsharp") — that is **not** a duplicate to drop; keep both, they answer
   different questions, exactly as the precedent kept both perspectives on issue #67.
4. **`HANDOFFS.md`'s one incoming receipt is small and concrete** — upstream's own S12 (§2.2 row
   5), dated 2026-08-12, sits far below fork's live receipts (all 2026-09-02 through -04) once
   interleaved. **Re-apply the retention policy after inserting it**: `grep -c '^```handoff'
   HANDOFFS.md`; if it exceeds the ratified cap of **4** (`HANDOFFS.md`'s own front matter,
   S127), trim to 4 the same way any session would, archiving the oldest — which will include
   upstream's S12 receipt going straight to a shard, correctly, since it is the oldest entry in the
   merged file.
5. **`CHANGELOG.md`'s incoming 188 lines are upstream's own S9–S12 narration plus each PR's
   upstream-side merge entry** — walk it by date the same way; no retention action is owed here
   (this file trims on bytes via `methodology_trim.py --check`, not a fixed entry cap — run
   `--check` after the merge and act on what it reports, don't predict it).
6. **Recompute every derived count in both files' front matter after editing** — receipt counts,
   shard tables, the `grep -c` populations these files' own front matter cites — the same "recount
   before trusting it" discipline `HANDOFFS.md`'s own text already states about itself.

### 2.4 Verification — the surface, and what it does not cover

**Surface: this repository's own working tree and CI-equivalent local run — the same surface every
prior resync merge in this fork's history has used, since this repo ships no application (its own
`SAFEGUARDS.md` §Verify the Build Equivalent names `bash bin/tests.sh` as the build-equivalent for
a doc/tool repo).** This surface *can* prove: every existing test still passes with the merged
tree, the two dashboard twins stay byte-identical, both ledgers' derived counts stay accurate, and
no distributed file silently lost content. It *cannot* prove: that upstream's maintainer would
accept this merge's specific conflict resolutions if this were an outward PR (it isn't — this
merge moves upstream's already-merged content *into* the fork, no PR is opened) — the merge is
purely fork-internal, so this asymmetry doesn't block Phase B the way an upstream-facing PR would.

Full command set, run in this order after resolving all 20 paths and before committing the merge:

```sh
bash bin/tests.sh                                    # baseline today: 304 passed, 1 failed (Test 9)
bin/check-handoff --all                               # 0; receipt count = old + 1 (upstream's S12),
                                                       # then re-checked after any retention trim
bin/check-links                                       # 0; link/file counts may grow (new distributed
                                                       # files this merge lands on this repo's own tree)
bin/check-learnings                                   # 0; contiguous 1..N, N unchanged (this merge adds
                                                       # no learning rows on either side beyond what §2.2
                                                       # row 15 already reconciles)
python3 -m unittest tools.test_methodology_dashboard  # keep ours (row 16) must still pass 100%
python3 -m unittest tools.test_context_budget         # take theirs (row 18) must pass 116/118 (2 skip)
python3 -m unittest tools.test_methodology_trim       # take theirs (row 20) — NEW combination, budget
                                                       # time to fix whatever this surfaces
cmp starter-kit/methodology_dashboard.py tools/methodology_dashboard.py   # silent (twins agree)
```

**Test 9 will NOT flip as a result of this merge, and the plan states that plainly rather than
guessing otherwise.** It fails because `bin/sync`'s `--source=github` path (`bin/sync:93`, `gh api
repos/KJ5HST/methodology/contents/<src>`, no `ref=`) reads whatever is on **`upstream/main`'s
default branch on GitHub** — not this fork's local tree, and not `read-set-budgets`. This merge
changes fork `main` only; it does not touch `KJ5HST/methodology` at all. Test 9 stays red for
exactly its pre-existing reason (3 of 27 manifest sources absent from `upstream/main`) until
`read-set-budgets` itself is merged into `upstream/main` on GitHub — the maintainer's action,
already listed out of scope in §4. A first draft of this row predicted the opposite (that landing
`read-set-budgets` into fork `main` would flip Test 9); reading `bin/sync`'s actual fetch call
before writing it down replaced the guess with this — a second worked example, alongside §2.1's
86/4 correction, of the discipline Correction 1 asks for.

## 3. Phases — each one session, each closing at its own STOP

**Phase A — this plan. DONE when committed to `docs/planning/` with this evidence-based inventory,
matching `SESSION_RUNNER.md` §Planning Sessions' requirement (grep-based inventory, per-item
resolution, verification commands, named surface).** *Verification:* `git log -1 --format=%H --
docs/planning/upstream-read-set-budgets-merge-plan.md` resolves; the file exists and every command
quoted in §2 has actually been run once (already true — every command above was executed producing
the exact output quoted). *Surface: this session's own working tree; read-only except this file and
the session's own ledger/receipt writes.*

**Phase B — perform the merge. One session. NOT authorized by this plan; needs its own explicit
go-ahead, the same gate PR 4's Phase C and Phase D each required.**
- **What DONE looks like:** `git merge upstream/read-set-budgets --no-commit` run for real (no
  `-X ours`/`-X theirs` shortcut), all 20 paths in §2.2 resolved per their stated rule, both
  ledgers interleaved per §2.3, the full §2.4 command set run and its results recorded (not
  predicted) in the merge commit message — following the `aa378ab` precedent's own message shape
  (one paragraph per resolved-file category, plus a **Verified:** paragraph with real numbers) —
  then committed as a real two-parent merge commit (never a squash) and pushed to `origin` (this
  user's own fork; **not** an action on `KJ5HST/methodology` and so not gated by `CLAUDE.md`'s
  outward-facing-action rule).
- **Verification commands:** exactly the §2.4 block, run bare (never through a pipe), each read
  and recorded before commit.
- **Surface:** this repository's own working tree (§2.4); this surface cannot prove upstream CI
  would independently reach the same verdict, since `upstream/read-set-budgets` carries no CI
  workflow of its own to compare against (`git show upstream/read-set-budgets:.github/workflows`
  — confirm empty at Phase B time, don't assume it still is).
- **Session boundary:** one session, closing at its own STOP per the normal Phase 3 close-out —
  claim stub, evaluate this plan's own handoff, self-assess, write the receipt, record the ledger
  entry, commit, report.

## 4. What this plan deliberately does not do

- **Does not perform the merge, push, or touch `origin`/`upstream` in any way.** Zero outward
  action taken while writing this plan, matching the operator's own correction of the interrupted
  S150 attempt.
- **Does not edit `pr4-read-set-budgets-plan.md`.** Correction 2 (§1) is recorded here, not written
  into that ratified, closed document — this repo's own convention for a known-wrong figure in
  closed prose.
- **Does not decide a version bump.** This merge is fork-internal catch-up with content already
  released upstream (v3.7) or never independently versioned (PR 1–4 are all post-v3.7, unreleased
  on either side); `CLAUDE.md`'s `## Versioning` pointer to `docs/RELEASE_HISTORY.md` needs no new
  entry for a merge that ships no new capability to adopters beyond what already exists on fork
  `main` today.
- **Does not clean up now-stale local branches.** `git branch -vv` currently shows
  `pr1/framework-learnings-extraction`, `pr2/ledger-trimmer`, `pr3/apparatus-extraction`, and
  `pr4/context-budget-gate` as fully merged upstream and safe to delete after Phase B confirms the
  merge landed everything they carried — a one-line housekeeping action for a future session, not
  this plan's concern.
- **Does not run `context_budget.py --calibrate`** — the ratified plan (D10) already assigns that
  step to the maintainer, not this fork.
- **Does not answer BL-26** (*"issue #67 and PR #66 vs. this fork's current state — neither
  addressed, PR #66 has its own collisions"*) beyond what §2.2 row 16 resolves mechanically for
  this one file. BL-26's broader scope, if any remains after this merge, is a separate session's
  read of the backlog item, not a byproduct of this plan.

## 5. Self-review

Read back against `SESSION_RUNNER.md` §Planning Sessions' checklist: deepest-reasoning intent
honored (every one of the 20 rows above is backed by a command actually run in this session, not
recalled or assumed); grep-based inventory present (§2.1–§2.2, every path in the true 20-path
conflict set individually diffed, not sampled); per-phase completion criteria, verification
commands, and named surface present for both phases (§3); session boundary stated for Phase B; two
corrections to prior claims recorded rather than silently absorbed (§1). One thing intentionally
left for Phase B rather than resolved here: `tools/test_methodology_trim.py`'s adoption (row 20) is
the one row this session could not fully dry-run in place (an isolated scratch-directory copy
fails on `git show HEAD:...` lookups that require a real checkout, confirmed directly), so its
verification is deferred, honestly, to the session that runs it — the same discipline this plan's
own Correction 1 asks of the file it repairs.
