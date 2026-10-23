# Backlog interaction review: how the 75 open rows affect each other, and the order to take them in

**Status: written 2026-10-19 (session 340). A read-only review: it proposes and edits no backlog row, and nothing was sent to `KJ5HST/methodology`.** He asked for it on 2026-10-18: *"review the backlog - examining interactions between BL items seeking to improve proposed changes and preferred BL item order."* Evidence was read at fork `main` `cfe6f8d9`, upstream `main` `f34769f`, PR #94 head `1082d3b`, PR #92 head `fa2bb5d` and the local branch `pr2/candidate` `3cba1e5`. [§8](#8-method-and-limits) says what was checked by whom and what was not. **Corrected 2026-10-23 (session 368):** lines 203, 286 and 449 first called decision D4's 2026-10-25 date superseded by the maintainer's replies; he ruled on 2026-10-23 that D4 stands, and those three sentences now say so. Nothing else in the review was changed.

**Words used here.**
- **A row** (written `BL-n`) is one item in [`BACKLOG.md`](BACKLOG.md); its full text is in [`BACKLOG-DETAIL.md`](BACKLOG-DETAIL.md), and closed rows are in [`BACKLOG-COMPLETED.md`](BACKLOG-COMPLETED.md).
- **A session** is one unit of work with one deliverable, then a close-out.
- **A receipt** is a session's close-out record: a fenced block in `HANDOFFS.md`.
- **Decisions D1 to D6** are the six decisions the composition plan ([`upstream-pr-composition-plan.md`](upstream-pr-composition-plan.md) §7) put to him; D4 was "keep waiting for the maintainer, and ask again on or after 2026-10-25".
- **A distributed file** is one that `bin/_manifest.py` lists: every adopter project receives it, so changing it is upstream-facing.
- **Outward** means touching the upstream repository (a pull request, a comment, an issue, a push). Each outward action needs his go-ahead, every time. Everything else is fork-side.
- **The candidate** is the local branch `pr2/candidate` (34 commits over upstream), and **the large pull request** is the single upstream pull request being composed from it; its text, draft 11, is approved. Adding a commit to the candidate re-opens that text.
- **The trimmer** is `starter-kit/methodology_trim.py`: it archives old ledger entries and writes a proof script beside each archive.
- **A gate** is an automated check in `.quality-gates.json` that goes red when a number slips. Raising a gate's threshold (a "tightening") needs no approval; lowering one does.

---

## 1. The answer first

**The backlog is less open than it says.** Of the 75 rows in the open table, the evidence shows 32 open, 20 partly done, 15 delivered but still listed, 4 superseded, 2 blocked and 2 on his hold. **Nineteen rows can close now**: 15 whose fix reached upstream (every pull request they cite is verified merged: #66, #68 to #71, #73, #76 and #84 to #88) and 4 whose reason went away or whose question was answered (BL-20, 21, 23, 30). Closing them is fork-only bookkeeping and needs no go-ahead. Three further defects of the record itself are measured in [§2](#2-making-the-backlog-true): the hand-kept "Open:" list names 52 of the 75 rows, 13 row bodies lack the anchor line their links need (10 links point at nothing), and `BACKLOG.md` reads about 26,793 tokens against its 25,000-token ceiling at every session start.

**The order, in one paragraph.** Read and answer the maintainer's two replies first (he commented on PR #92 and on PR #94 on the evening of 2026-10-18; PR #92's reply is the next session's task by his instruction). Then spend one session making the backlog true. Then prepare the large pull request: a read-ceiling guard first, then a rebuild on whatever the maintainer merges. While that waits on him, take the small fork-only fixes that remove silent failures (a gate that ignores a red suite, a checker that sees only the newest receipt, a retention rule that forces a trim every session). Rows that touch the trimmer wait until PR #94 settles and then go out as one release; rows that touch `README.md` or `CLAUDE.md` wait for PR #92 to merge; every distributed fix not already in the approved text goes out after the large pull request, one delivery per file group. Nine rows wait on his decision. [§5](#5-the-order) has the full order, [§6](#6-the-decisions-that-are-his) the decisions, [Appendix A](#appendix-a-every-row-and-where-it-goes) every row.

**The interactions that most change what a row should do** (each is argued in [§3](#3-the-interactions-that-change-a-fix)):
1. **Several rows edit one file and one version number.** Three want a new `quality_ratchet.py`, five want a new dashboard, four want the receipt seed, nine want text in the session runner, five edit one paragraph of `HANDOFFS.md`'s front matter. Done apart, each is a version bump and a second delivery; done together, one.
2. **The candidate ships a known defect unchanged.** BL-102's faulty line is character for character the same in `quality_ratchet.py` on fork `main` and on the candidate (checked), so the large pull request as built delivers it to every adopter.
3. **The session runner has no room.** The candidate's runner is 53,100 bytes, about 23 tokens under its 18,900-token read ceiling (checked), and nine rows want to add to it. They are one decision, not nine.
4. **Every added commit on the candidate re-opens approved text.** That makes the *timing* of a distributed fix part of its proposal: before the large pull request it costs a re-measure and a re-approval; after it, a second delivery.
5. **Some rows are copies of work the candidate already did.** BL-109, 111 and 112 are fork-side ports of hunks the candidate carries, and BL-109's hole (a gate that stays green over a failing suite) is real on the fork and already closed on the candidate (checked).
6. **Some rows are decisions in disguise.** BL-48 is not a seed edit but a decision inside BL-60; BL-32's "decision not yet made" was partly made on 2026-10-17; BL-108 needs him to say which retention depth he meant.

**What this review does not rest on: the maintainer's two comments.** This session read only who wrote each comment, when and how long it is (PR #92: 4,462 characters at 01:19 UTC on 2026-10-19; PR #94: 2,533 characters at 02:47 UTC), because he scheduled "examine and respond" for the next session. Several of the review's own agents read the comments through read-only `gh` and summarised them to the synthesis; those summaries were not checked, and every order step and proposal below has been rewritten to stand without them. If the replies say something the order does not expect, the replies win.

---

## 2. Making the backlog true

### 2.1 Nineteen rows to close

Each closes by the three edits the repository requires (the row out of the index in `BACKLOG.md`, the id into that file's "Completed items" list, the pointer row into `BACKLOG-COMPLETED.md`), plus a ledger entry, with `BACKLOG-COMPLETED.md.verify.sh` and `BACKLOG-DETAIL.md.verify.sh` read before and after (both exit 0 today).

| Row | What it was | Why it closes | How to close it |
|---|---|---|---|
| BL-13 | The /caveman row's false "handoff length discipline" claim: fixed by merged … | PR #68 merged 2026-08-12 | Its only open step was upstream PR #68 (the corrected /caveman row in RECOMMENDED_SKILLS.md) being merged; it merged. Close by the three-edit close and also strike it from the hand-kept 'Open:' list and the 'Runnable now up to the PR' bullet in BACKLOG.md. |
| BL-14 | The receipt's commit: field promised a reconcile nobody owned; … | PR #69 merged 2026-08-12 | PR #69 deleted the promise this row complained about. One leftover sentence (a shard's commit: slot 'was always going to be filled', starter-kit/HANDOFFS.md:163-165) is upstream's own text too, so it is a seed hunk for BL-46's delivery, not the fork-local fix the body planned. … |
| BL-17 | Receipt changelog_ref locator form: the upstream half merged as PR #69; … | PR #69 merged 2026-08-12 (distributed half) | The distributed half (the quoted-heading locator form, no bare line numbers) merged in PR #69. The fork half was deliberately never to become a resolution check, because it would punish correcting a false title; record it as declined by design. Do not amend BL-15's byte-pinned completed row, which points here. |
| BL-20 | Residual of a fixed parser defect: which Model-line form the seed documents; … | seed became a pointer; rules live in `FRAMEWORK_APPARATUS.md` (merged upstream via PR #84) | Its target text, three Model-line sentences in the receipts seed, no longer exists: the seed became a pointer and the rules moved to FRAMEWORK_APPARATUS.md, already merged upstream. Its id and completed row already exist and that row is byte-pinned, so do not amend BACKLOG-COMPLETED.md:90. |
| BL-21 | Two seed sentences for a hook exemption that was removed on 2026-09-16 … | hook exemption removed 2026-09-16 (commit `16648604`) | The two seed sentences were to describe a hook exemption (the Phase 1B claim carve-out) that his decision of 2026-09-16 removed; writing them now would describe an exemption no hook has. They must never be written. |
| BL-22 | Dashboard's 200-line doc-only threshold: reason and pinning test shipped … | PR #70 merged 2026-08-12 | The written reason and the pinning test for the dashboard's 200-line documentation-only threshold shipped in PR #70. Strike it from three places in BACKLOG.md (the Open list, the routing text at about :93, the index row). |
| BL-23 | Upstream issue #65 vs the fork's unshipped Learnings-table move: issue closed, … | issue #65 closed 2026-08-12; PR #76 merged 2026-09-02 | The decision it waited on (how to tell the maintainer about the Learnings-table collision when that pull request opens) has no moment left: issue #65 closed and the table move merged as PR #76. The parked citation checker survives at a tag, so nothing is lost. |
| BL-26 | Issue #67 (dashboard --sync warning) and PR #66: both resolved upstream; … | PR #66 merged 2026-08-11; issue #67 closed 2026-08-12 by his own PR #73 | Both threads are resolved upstream: PR #66 merged and the maintainer closed issue #67 with his own PR #73. The fork's richer scoped --sync [DIR] and --force gate reaches upstream only as decision 2(a) of draft 11 of the large pull request, so the close note must say 'delivered only if that pull request merges with 2(a) kept', … |
| BL-30 | Watch item: has the ledger trimmer fired outside nprcgenekeepr? It has, in all … | the trimmer has fired in the three adopters it named | Both of its questions are answered: the trimmer fired in mts-system, vscode_quarto_ext and wsfct, and each adopter's proofs were run read-only. Close with those figures and do NOT cite BL-36, BL-60 or BL-98 as owners of the question (they cover this repository's proofs). … |
| BL-31 | Upstream dashboard did not exclude context_budget.py from adopter code counts; … | PR #71 merged 2026-08-12 | PR #71 extended the dashboard's exclusion list for context_budget.py and merged. Also strike 'already opened as PR #71' from the routing text; the body's note that the fork does not distribute context_budget.py is now a historical remark. |
| BL-54 | bin/sync and bin/status missed versions hidden by a merge; … | PR #87 merged 2026-10-01 | Its only open condition was the upstream pull request, and #87 merged. Close it with BL-66 as step P6 of the sync-github plan and correct that plan's status line (docs/planning/sync-github-route-plan.md:4-10), which still says the pull request is open. |
| BL-57 | The CHANGELOG.md rules contradicted each other; … | PR #84 merged 2026-10-01 | All twelve plan phases are done and the one remaining item, the review of PR #84, ended in a merge. Point the plan's section-8 follow-ons at rows that already carry them (the HANDOFFS.md archive-rule decision at BL-47, the fork-only comments in distributed tools at BL-11) so nothing is re-raised, and drop the stale 'PR #84 is … |
| BL-62 | Upstream's read-cap partition test summed every whole-read class as one read; … | PR #84 merged 2026-10-01; fix in upstream `5223afb6` | The read-cap test fix is in upstream and the row's one stated condition, 'open until PR #84 merges', fired on 2026-10-01. The two dropped max_tokens declarations stay dropped. |
| BL-63 | One bin/sync run writes more files than the five-file commit cap allows, and no … | PR #84 merged 2026-10-01; paragraph live on both trees | The 'Committing a sync' paragraph and the five-file-cap sentence are live and PR #84 merged. This row was never in the hand-kept Open list. |
| BL-65 | A context-budget test failed on a machine whose transcripts fit a negative … | fixed upstream by the maintainer, commit `229f08d9` | The maintainer fixed the test himself in the shape its body proposed. Its side note (count gates ignore a failing exit code) survives only as BL-109, the one gate where it bites, so nothing is lost. |
| BL-66 | README told adopters to update from the GitHub URL, a route that could not … | PR #87 merged 2026-10-01 | PR #87 merged. Do not hold the close for the plan's verification clause: run it with the documented METHODOLOGY_SOURCE_URL override pointed at the fork (it cannot pass against the default upstream URL). … |
| BL-75 | context_budget.py's missing --status flag was fixed and merged upstream as PR … | PR #86 merged 2026-10-01 | PR #86 shipped the write-free --status flag. One P5 step is NOT done and rides the same commit: .context-budget.json:92 still says the --status flag 'does not exist and is silently ignored', false since #86 (the card that says otherwise is wrong). … |
| BL-80 | Context-budget tool's growth-run note contradicted its own table; … | PR #86 merged 2026-10-01 | The growth-run note that contradicted its own table was fixed in the same pull request #86; close it with BL-75 in the same commit as the .context-budget.json:92 rewrite. |
| BL-85 | The rules that stop a prose update from wiping an adopter's ledgers reached … | PR #88 merged 2026-10-01 | The three never-overwrite rules for an adopter's ledgers reached upstream in PR #88; its one content difference (.gitattributes in the adopter-owned row) already rides the candidate. The 'Setup with bin/sync names none of the three tools' residual becomes its own small row only if he wants it kept. |

Riders the verifiers found, so the close does not undo itself:
- **BL-20's completed row is byte-pinned** by `BACKLOG-COMPLETED.md.verify.sh`; close it in the index only.
- **BL-63 was never in the hand-kept "Open:" list**, so there is nothing to remove there.
- **BL-75 and BL-80 close together, with one real step left in their plan:** `.context-budget.json:92` still says the `--status` flag "does not exist and is silently ignored", false since PR #86. The row card that says otherwise is wrong.
- **BL-66 closes with BL-54 as the sync-route plan's last step**, but its plan's verification clause cannot pass against the default upstream address; run it with the documented `METHODOLOGY_SOURCE_URL` override, and raise `bin/status`'s missing "shallow source" check as its own small row first so that residual is not lost. That plan's status line still says PR #87 is open.
- **BL-14's one leftover sentence** (`starter-kit/HANDOFFS.md:163-165`) is upstream's own text too, so its reword is a hunk in BL-46's seed delivery, not the fork-local fix its body planned.
- **BL-17's fork half is declined by design** (a check that quoted titles resolve would punish correcting a false title); record it as a decision and confirm it with him in the sweep.
- **BL-30 closes after the three adopters' proofs are re-run read-only**, and one proof (wsfct's, which stays red even under `--reverify`) goes into BL-60's brief rather than being lost. Two verifiers found that citing BL-36, BL-60 and BL-98 as the owners of that question is wrong: they cover this repository's archive, not the three adopters.

### 2.2 Rows to retitle, not close

These are partly done and their index titles, bodies or plan status lines are stale. Each needs a corrected index row (the bodies are frozen by the detail file's proof, so a correction goes in the row or in a later entry):
- **BL-12:** its second bullet is closed upstream (issue #65 closed 2026-08-12); the first still stands (four sites plus a frozen archive copy say "19 anti-patterns"; the list has 20).
- **BL-19:** the plan's queue shows six items shipped (by 2026-08-04) and five never started; the plan's status line says nothing is implemented.
- **BL-36:** "four of the six shipped proofs" now describes a pile of 177 tracked proof scripts.
- **BL-37, BL-47:** the titles assert the half that is done (this repository runs its own budget gate; the `CHANGELOG.md` entry was decided against).
- **BL-44:** the body describes the original defect; the true span is fixed, the reserved number is still not named.
- **BL-51, BL-52:** only Phase C3 of BL-51 has no commit; two of BL-52's five leftovers are fixed.
- **BL-58:** the apparatus now covers about three of the eight trimmer hazards, not zero.
- **BL-79, BL-88, BL-94, BL-101, BL-105, BL-108, BL-112:** the plan or body status line lags the shipped work by weeks (BL-101's row ends at an answer given before 2026-10-13); BL-108's written rule is unchanged while practice differs; BL-112's premise ("the file is byte-identical in the fork and the candidate") stopped being true when the candidate added the exit-4 line.
- **BL-98:** the index row names a fourth commit; PR #94 has carried a fifth since 2026-10-17.

### 2.3 Three defects of the record itself

| Defect | Measured | Consequence |
|---|---|---|
| The hand-kept "Open:" list (`BACKLOG.md:9`) is incomplete | names 52 of the 75 rows; 23 missing (BL-63, 88 to 91, 93, 94, 98, 101 to 106, 108 to 115, 117) | BL-93 recorded five missing; the gap has grown more than fourfold. Delete the list; the file already prints the command that derives it. |
| Row bodies without an anchor line | 13 of 94 (BL-47, 48, 49, 59, 60, 64, 65, 67, 73, 94, 96, 97, 98); 10 `[detail]` links dangle (7 in `BACKLOG.md`, 3 in `BACKLOG-COMPLETED.md`) | BL-87 says nine; it is thirteen. Fix before the mass close, or the closed rows' links dangle from the completed file. |
| `BACKLOG.md` is over its read ceiling | about 26,793 tokens against 25,000 (`context_budget.py --status`, exit 2) | Every session start pays for rows that are done. The sweep shrinks the file; BL-55 then puts the two backlog proofs behind gates so the sweep stays true. |

---

## 3. The interactions that change a fix

How these were found: six independent lenses over cards of all 75 rows produced 163 candidate interactions; three skeptics per finding then tried to refute each one. **96 survived and 67 did not** ([§7](#7-what-failed-verification)). What follows uses only the survivors, and where the skeptics disagreed that is said.

### 3.1 The trimmer and PR #94

Open rows that edit `methodology_trim.py`: BL-32 (a third ledger entry, for `SESSION_NOTES.md`), BL-36 and BL-60 (the proof scripts), BL-42 (the pointer block), BL-49, BL-50, BL-52, BL-58 (the apparatus text beside the trimmer's rules), and BL-117's trimmer-suite part. PR #94 rewrites the same file (+563 lines, five commits), and the candidate rewrites it too (+787 lines against upstream) with a *different* "1.8.0" underneath the same "1.8.1" label; draft 11 puts the difference at 400 trimmer lines, 910 test lines and 58 gate lines, in 22 conflict regions across four files. Anything touched now becomes a third lineage.

- **Wait for #94, then do it once.** BL-42, BL-49 and BL-50 are one trimmer release; BL-50's one-newline case is written first as a test BL-42's design must pass, because BL-42 does not close BL-50 by itself (they share `insert_pointer`).
- **BL-48 is a decision, not a seed edit.** It proposes adding "This file currently holds **N**" to the receipt seed; the fork removed that sentence on purpose on 2026-09-16 (session 172; `HANDOFFS.md:31-36`) and has lived with `FRONTMATTER_FIELD_ABSENT` on every trim since. Whether the field ships or the tool stops declaring it is decided inside BL-60.
- **BL-36 is already folded into BL-60** by his decision of 2026-09-16 (session 173), and `--reverify` (trimmer 1.7.0 onward) removes the pressure to regenerate the four old proofs. BL-60 is costed against the proof template *as it stands after #94 settles* (about 20.5 KB written per trim, 177 tracked scripts, about 3.07 MB).
- **BL-32's "decision not yet made" is stale:** on 2026-10-17 he chose "a canonical SESSION_NOTES.md entry in the trimmer's ledger table", built as PR #94's fourth commit `2308553`. That entry exists only on #94's branch (`grep -c SESSION_NOTES` on fork `main`'s trimmer reads 0), so fork `main` and the candidate disagree with the pull request that is already open. BL-32 shrinks to its option (b), a supported adopter-extension mechanism, and waits for #94's outcome.
- **BL-58's text and #94 edit the same apparatus section** (`FRAMEWORK_APPARATUS.md`, "Reading and archiving"); write BL-58 after #94's timing-rule paragraph settles, scoped to the hazards still uncovered.

### 3.2 The quality ratchet

BL-102 (the hook installer writes a symlink-dependent path), BL-103's option (c) (`--run` prints the names of unmeasured gates) and BL-92's option (c) (keep a failing gate's output) each want a new `quality_ratchet.py`. They are **one version, 1.6.0**, not three bumps. BL-102's body says "1.3.1"; the tool is at 1.5.0. The faulty line (`tool = os.path.relpath(os.path.abspath(__file__), top)`, line 666) is identical on fork `main` and on the candidate, so the large pull request as built ships it. The field risk is small (the documented relative invocation is safe), so declining to fix it before the pull request is also safe. Whether it rides the candidate is his call ([§6](#6-the-decisions-that-are-his), question 1). BL-92's shapes (a) and (b), a better failure message and a fixture tree for Test 44, are fork-only and can go now; shape (c) waits for the ratchet release.

### 3.3 The dashboard

BL-68 (the large-files risk names the framework's own tools), BL-71 (the branch count reads every line of `git branch -a`, so a fork can never clear it), BL-90 (`--sync` overwrites a locally edited copy without a word), BL-103's option (a) and BL-51's Phase C3 row all change `methodology_dashboard.py`: two byte-identical copies and one version constant. His decision to send the whole dashboard lineage (2.11.3 to 2.22.0) in the large pull request means none of these fixes is in it. **One 2.23.0 release after the large pull request**, with BL-68 and BL-71 in the same function nine lines apart. BL-68's first investigation step is already answered (the score has no size term; the flag is a risk row), so its remedy can be chosen inside the release, and "leave as is, with the reason recorded" is an allowed answer.

### 3.4 The receipt checker

BL-73 (a receipt opened twice reads as one block) and BL-89 (the default mode checks only the newest receipt) fix the same part of `bin/check-handoff`: **one change**, running in default mode the ledger checks that only `--all` runs, plus a finding for a doubled opener and a block count that tolerates the format example at `starter-kit/HANDOFFS.md:50-51`. BL-16's false docstring clause ("no root-level receipt ledger") rides along; it is also on the candidate, which carries upstream's checker plus layout hunks only. BL-18 (bare line numbers in `key_files`) follows in the same file. The structural change is canonical-only, so nothing pending can overwrite it.

### 3.5 The session runner's byte budget

Nine rows want text in `starter-kit/SESSION_RUNNER.md`: BL-39, 58 (shape b), 64 (shape c), 70, 77 (shape 1), 79's P3, 113, 115 and 55 (shape c). The candidate's runner is 53,100 bytes at a measured 2.813 bytes per token: about 18,877 of 18,900 tokens, roughly 23 tokens or 66 bytes of room. BL-70's plan-surface rule is 2,535 bytes (fork lines 136 to 153), BL-115's chosen sentence 283 bytes. So: **BL-113's option (e) first** (run `context_budget.py --status` in the candidate's verification script, so any runner edit is measured), then **one decision** on what to cut to pay for whichever additions he picks, using the extraction lever BL-91 describes; BL-79's P3, designed net zero bytes, is the template. BL-77's shape (3) (the hook leaves a trace that Phase 0 reads) costs no runner bytes; BL-58 should prefer shape (a) or (c). BL-70's "fold into a later pull request" is priced out; its choice is ask or decline. BL-39 has no logical dependency on BL-70 but competes for the same bytes, and shrinks to the receipt seed's `runtime_smoke` token and the flight manual if BL-70 is declined.

### 3.6 `CLAUDE.md` and `README.md`

`CLAUDE.md` is 18,737 bytes against 18,600 (137 over; `--status` exit 2), and three rows want to add to it (BL-75/80's reword at line 102, BL-19's queue item 42, BL-91's decision D3). **Any addition must remove bytes first;** only BL-19's queue item 42 (purge derived values) frees any. PR #92 edits both `CLAUDE.md` and `README.md`, so edits to either wait for it to merge and the fork to resync: this holds BL-19's queue item 42, BL-74's shape (4) (the stale cost section, `README.md:389` and `:404` still state the disproved 2,000-line cap) and BL-12's fork-only sites. BL-74's shape (1), a `README.md` row in the manifest, is a change to the directory move's machinery (a new-layout row, two pinned counts of 30) and comes after the large pull request, never before shape (4), or the stale cost section ships to adopters.

### 3.7 The fork's own configuration and `HANDOFFS.md`

- **`.context-budget.json` has five editors** (BL-75/80's line 92, BL-81's stale sizes, BL-62's closure note, BL-106's option (b), BL-47's precedent). Line 92 and BL-81's two stale size notes are the same defect class (a prose note contradicting the tool beside it); fix them in adjacent commits and prefer BL-106's option (a) so the file does not gain a fourth prose-and-number pair.
- **`HANDOFFS.md`'s front matter is edited by four rows and bounded by a fifth:** BL-108 (the retention paragraph), BL-42 (the fold comment), BL-60 and BL-48 (the count paragraph), with BL-61 sizing the reserve they must fit. BL-108 goes first and must say which depth he meant; BL-61's reserve is sized in the same session. The price of depth two at rest is concrete: Test 34 then prints six SKIP rows and `tests-sh-passed` reads 497 under its 503 floor (a loosening, so plan mode).
- **BL-106:** both plans are within a few bytes of their declared budgets (composition plan 29,996 of 30,000; directory plan 59,994 of 60,000; checked) and neither is gated. A gate at the declared figure is green on arrival and refuses the next raise; cover both plans.

### 3.8 Work the candidate already did

BL-109 (the `migrate-layout-unit-tests-failed` gate, so the migration suite's colour no longer depends on a count), BL-111 (three checker tests) and BL-112 (the exit-4 docstring line) are fork-side copies of hunks the candidate carries. Each is a tightening or a documentation line, so no plan mode; they share no lines, so batching is a convenience, not a dependency. BL-112: copy the candidate's two-line wording, since byte equality is already gone. BL-111 raises its gate from 15 to 18 only if all three tests pass on the fork's suite (they do, in a scratch copy). BL-109's hole is real: the fork's `.quality-gates.json` has the count gate and no `-failed` twin, so a red suite can pass; the candidate has the twin. BL-65's side note (count gates ignore a failing exit code) survives only as BL-109, the one gate where it bites.

### 3.9 The seed files: three batches, not one

Two ratified plans said BL-46(2), 47, 48 and 49 go in one pull request. They no longer share a file. (i) **The receipt seed** `starter-kit/HANDOFFS.md`: BL-46(2) (the closing instruction that leaves a stray `---` behind, so an adopter's trimmer refuses with `ZONE_UNCLASSIFIED`), BL-14's leftover sentence, BL-39's `runtime_smoke` slot. BL-48 leaves this batch (it is BL-60's decision) and BL-49 is the trimmer's. (ii) **The context-budget seed** `starter-kit/context-budget.json`: BL-47 (HANDOFFS.md's ceiling), BL-37(b), BL-84 (the 24,000-byte warn line and the 800-character fence) and BL-114 (the maintainer's own open issue #95, on his hold). (iii) **The trimmer**, in the trimmer release. None of the seed hunks overlaps a candidate hunk, so batch (i) is a separate small pull request after the large one, never a 35th commit.

### 3.10 The candidate window

Every distributed fix has a timing: before the large pull request it is one more commit whose added lines must be scanned for fork-only codes, the claims script re-run (about half an hour) and draft 11 re-measured; after it, a second upstream delivery. The verifiers split on this. One side would add BL-12's distributed site, BL-16 and BL-11's mechanical sites now; the other showed each would re-open an approved text "for a one-line gain". **The synthesis sides with the second: only BL-113 (a fork-side script, not a candidate commit) and, if he agrees, BL-102 touch the candidate; everything else goes out after it, one delivery per file group.** If the replies force a rebuild anyway, that is the window for reconsidering.

### 3.11 The directory move and the adopters

BL-104 (move this repository's own ledgers under `methodology/`) is a decision row: its repairs are worth building only if the maintainer adopts the layout or he accepts hand-resolved ledger conflicts at each resync; otherwise close it DECLINED. BL-105's phase 4 is **not** gated by the large pull request: its gates are a free adopter tree (check `pgrep -x claude` and `lsof` first), his go-ahead for the migration tool's second stage (`--tier 2`, which moves a project's own notes and ledgers), his calls on findings F7 and F19 in the directory-move findings register (whether a forced sync may drop nprcgenekeepr's 49-line local trimmer patch), and each adopter's own migration; nprcgenekeepr's step now waits on BL-32's outcome, because #94's entry would become canonical the moment it merges. BL-110's rule (flag a `docs/methodology/` path written as code text in a shipped document; the count step is done: 11 mentions in 3 of 23 documents) goes in `bin/check-links`, both copies, before the large pull request is rebuilt.

---

## 4. The proposals that change most

[Appendix B](#appendix-b-the-forty-six-changed-proposals) lists all 46. The ten with most effect:

1. **BL-109:** from "design a second gate" to "copy the written pair from the candidate" (`pr2/candidate:.quality-gates.json:77-91`).
2. **BL-48:** from a seed edit to a decision inside BL-60.
3. **BL-102:** from "its own session at ratchet 1.3.1" to one 1.6.0 with BL-103(c) and BL-92(c), or a 1.5.1 commit on the rebuilt candidate if he agrees.
4. **BL-71, 68, 90, 103(a):** from four separate dashboard fixes to one 2.23.0 after the large pull request.
5. **BL-89 and BL-73:** one change; BL-16 rides it.
6. **BL-46, 47, 48, 49:** from one batch to three ([§3.9](#39-the-seed-files-three-batches-not-one)).
7. **BL-32:** from "decision not yet made" to option (a) decided on 2026-10-17 and built only on #94, so what remains is option (b).
8. **BL-108:** from "edit the rule to trim above three and cut to two" to "ask which depth he meant", with the cost of depth two stated.
9. **BL-87 and BL-93:** nine bodies to thirteen, and the hand-kept list is deleted, not repaired, inside the sweep.
10. **BL-117:** re-baseline first (the trimmer suite reads 222 tests, not 199), and start with the double-run measurement: the ratchet runs eight unit suites that `bin/tests.sh` already ran whole, so every `--run` pays for each twice (a one-command measurement with a known mechanism).

---

## 5. The order

Five rules drove it:
1. **A reply ranks first** (his own rule for the upstream watch).
2. **Make the record true before ordering real work**: a backlog that lists done work as open misleads every later choice.
3. **The large pull request is the fork's purpose**, so its preparation moves ahead of fork-only polish the day its gate opens; but its gate (the replies' outcome) is outside this repository, so bounded fork-only work fills the wait.
4. **Never change a file a pending pull request rewrites until that pull request settles**: the trimmer waits for #94; `README.md` and `CLAUDE.md` wait for #92.
5. **One delivery per file group after the large pull request**, never a late addition to approved text.

Five orderings were produced from different angles and scored by three judges (out of 150: his-time-and-silent-failure 110.5, dependency-and-rework 109.5, upstream-route 108, backlog-truth-first 106.5, adversary 97), so no angle won clearly; the synthesis (a final agent that reconciled the five) takes their shared skeleton. 31 rows have a position; the rest are in the sweep, folded into a lead row, held on him, or have no work.


**1. Answer the maintainer's replies on PR #92 and PR #94**

| # | Row | The one deliverable | Size | Outward? | Waits on |
|---|---|---|---|---|---|
| 1 | BL-98, and PR #92's reply (which has no row) | Read the maintainer's two replies in full: the one on PR #92 first, as he scheduled for the next session, then the one on PR #94 (the trimmer fix). Check each point against PR #94's head, fork main and `pr2/candidate`; write the fix list and the reply text and show both inline. Any fixes are the next sessions on this same row: fix once on #94's branch, then port to fork main and the candidate. Nothing is pushed or posted without his go-ahead. | multi_session | yes | — |

**2. Make the backlog true**

| # | Row | The one deliverable | Size | Outward? | Waits on |
|---|---|---|---|---|---|
| 2 | BL-93 | The sweep, one session in five commits of at most five files: close the 19 rows listed in §2.1 by the three-edit close (row out of BACKLOG.md, id into the 'Completed items' list, pointer row into BACKLOG-COMPLETED.md, plus a CHANGELOG.md entry each), delete the hand-kept 'Open:' list (his one decision, asked in the session's picker; it omits 23 of 75 rows), add the 13 missing anchor lines in BACKLOG-DETAIL.md and move bl-58's, correct the stale status lines of the sync-github, changelog-rules and context-budget-status plans, rewrite .context-budget.json:92, and relabel the index rows whose meaning does not change with the … | M | no | — |
| 3 | BL-55 | Wire the two backlog proofs (BACKLOG-COMPLETED.md.verify.sh and BACKLOG-DETAIL.md.verify.sh, both exit 0 today and in no gate) into .quality-gates.json as no-extract max-0 gates (for a gate with no extract the ratchet reads the exit code as the measurement, quality_ratchet.py:506-517), and add the 'every [detail] link resolves to an anchor' check beside the detail proof. The adopter-facing half (a shipped [BL-N] join check, or promoting the dashboard's Signal F) stays a separate decision for him. | M | no | BL-93 |

**3. Prepare and send the one large pull request**

| # | Row | The one deliverable | Size | Outward? | Waits on |
|---|---|---|---|---|---|
| 4 | BL-113 | Add 'python3 starter-kit/context_budget.py --status' and its exit code to the candidate's layer-verify.sh (a fork-only script under docs/planning/pr-composition-evidence/) so no candidate commit can cross the runner's 18,900-token read ceiling unseen (about 66 bytes of room today), and settle the density hunk in the candidate's .context-budget.json: keep it and amend the composition plan's 'Not carried' cell, because approved draft 11 already describes the hunk. | S | no | — |
| 5 | BL-102 | Fix the ratchet's hook installer (starter-kit/quality_ratchet.py:666 computes the tool path with os.path.abspath against git's real-path top directory, so a hook installed by an absolute symlinked path breaks after bin/migrate-layout moves files): realpath on both sides, a test that installs from a symlinked temp path, and a version bump to 1.5.1 (the tool is 1.5.0; the row's '1.3.1' is stale). Fork-side now; it reaches upstream only as one added commit on the rebuilt candidate, which is his call because it changes draft 11's commit count and ratchet versions. | S | yes | BL-113 |
| 6 | BL-110 | Teach bin/check-links to flag a 'docs/methodology/' path written as code text in a shipped document outside a short allow-list, in the fork's copy and the candidate's copy of the tool (they differ by 8 comment lines, so one patch fits both). The row's 'count first' step is done: 11 mentions in 3 of the 23 distributed documents (BOOTSTRAP.md 9, SESSION_RUNNER.md 1, HOW_TO_USE.md 1). Optional, his pick; run it once against the final prose before the candidate is re-measured. | M | no | BL-102 |
| 7 | BL-101 | Rebuild and send the one large pull request, in steps that each need his go-ahead: (1) resync fork main to whatever #92 and #94 have merged; (2) rebuild `pr2/candidate` on the merged trimmer, adding BL-102's commit only if he agrees, re-run the conflict and claims scripts (the claims run takes about half an hour), re-measure draft 11 (34 commits, 19,983 lines today) and show the changed text inline; (3) ask the three go-aheads separately: push the branch, open the pull request, answer comments. The 2026-10-25 date in decision D4 still governs: the maintainer's first replies on #92 and #94 (2026-10-19) asked for changes and the fork answered them the same day, neither pull request is merged, and he confirmed on 2026-10-23 that D4 stands; … | multi_session | yes | BL-98, BL-113, BL-102 (if he agrees), the outcome of PRs #92 and #94, then a resync |

**4. Fork-only fixes for failures nobody is told about**

| # | Row | The one deliverable | Size | Outward? | Waits on |
|---|---|---|---|---|---|
| 8 | BL-109 | Port three small guards from pr2/candidate to the fork in up to three commits: the gate migrate-layout-unit-tests-failed (max 0, same command, so the ratchet runs the suite once) and the corrected 'why' on the count gate (today the count gate reads 280 and passes even if the suite prints FAILED); BL-111's three missing checker tests, raising checker-layout-unit-tests from 15 to the measured 18; BL-112's missing exit-4 line in bin/migrate-layout's header. | S | no | — |
| 9 | BL-89 | One change to the receipt checker bin/check-handoff, failing tests first: in default mode surface scan()'s structural findings and run the duplicate (session, date) and one-live-pending-per-line checks that only --all runs today; add a finding for a receipt opened twice (BL-73) and a block count that tolerates the format example at starter-kit/HANDOFFS.md:50-51; reword the false 'no root-level receipt ledger' clause in default_path()'s docstring (BL-16, bin/check-handoff:892-894). Fork-only: the candidate carries none of the new checks. | M | no | — |
| 10 | BL-108 | Ask him which retention depth he meant, then edit HANDOFFS.md's front-matter rule. It still says keep two, trim above two, --cut 2; his pick at session 322 was trim at four with --cut 2 (about half the trims); practice since session 325 cuts four to three, so a trim and its hand-folded pointer block fall due every session. Depth two at rest needs bin/tests.sh Test 34's six checks to stop reading the live ledger (use a fixture), otherwise the tests-sh-passed gate reads 497 against its 503 floor, which would be a loosening and is forbidden; if he finds that rework not worth it, write down depth three. … | M | no | — |
| 11 | BL-92 | Make Test 44 (the bin/check-overhead test in bin/tests.sh) say what failed and stop depending on the live tree: print the difference of its two git-status snapshots in the failure message and run the check in a fixture tree. Keeping a failing gate's output is a ratchet change (shape c) that waits for a later ratchet release. | S | no | — |
| 12 | BL-81 | Delete the two stale prose file sizes (54,363 B and 15,386 B, stale for the third time) from the notes at .context-budget.json:114-115 and cite the structured files[] records, the one copy that cannot go stale; no new guard. | S | no | BL-93 |
| 13 | BL-106 | Add two max-direction gates to .quality-gates.json for the plan files that declare byte budgets nothing checks: the directory-move plan (59,994 of 60,000 B) and the composition plan (29,996 of 30,000 B). Both are green on arrival, so the next edit to either must cut bytes first. Ask him once whether 60,000 B is a hard limit or a price he set himself. | S | no | — |
| 14 | BL-18 | A forward-only rule in bin/check-handoff: a bare CHANGELOG.md:N or HANDOFFS.md:N in a new receipt's key_files is a finding, exempting a receipt whose only path:line token is the ledger anchor. 110 of the 113 offending anchors sit in archive shards this repository treats as unrepairable (.quality-gates.json:8), so nothing in the past is rewritten. | M | no | BL-89 |
| 15 | BL-44 | One format string in bin/check-learnings so its success line names the reserved Learning number it skips (for example '16 row(s), #1..#17, 1 reserved (#14)'), derived from the parsed numbers, never from the row count. Canonical-only. | S | no | — |

**5. Measure before speeding anything up**

| # | Row | The one deliverable | Size | Outward? | Waits on |
|---|---|---|---|---|---|
| 16 | BL-117 | A profile-first session on the fork's test suites and gate run: time bin/tests.sh with and without the eight unit-suite lines it runs whole and the ratchet then runs again as count gates (eight of nine suites run twice per gate run), re-baseline first (the trimmer suite reads 222 tests, not the card's 199, and the gate roster grows with BL-109 and BL-55), then change one thing at a time. A speed-up that changes any verdict or count is a defect. Trimmer-suite targets wait until the trimmer settles; no running suites beside each other until BL-92's fixture-tree Test 44 exists. His pick. | L | no | BL-109, BL-55, BL-92 |

**6. Work that waits only on PR #92 (README.md and CLAUDE.md)**

| # | Row | The one deliverable | Size | Outward? | Waits on |
|---|---|---|---|---|---|
| 17 | BL-19 | Do queue item 42 only: write the version-pointer exemption into CLAUDE.md as a named exemption while purging derived values so the file shrinks (it is 137 B over its 18,600 B ceiling, confirmed). item 41 needs his decision first, items 43 and 44 are not the guards other rows thought, and item 45 is overtaken by context_budget.py and bin/check-overhead. The index row itself is relabelled in the sweep. | S | no | PR #92 merged and the fork resynced |
| 18 | BL-74 | Rewrite the stale fork-only cost section of README.md (README.md:389 and :404 still state the 2,000-line cap that was disproved), shape (4), after PR #92 merges and the fork resyncs. Shape (1), adding README.md to bin/_manifest.py, is a change to the directory move's machinery (a new-layout row, pinned counts of 30 rows in two tests, 14 dangling links per layout) and is a post-large-pull-request decision. | M | no | PR #92 merged and the fork resynced |
| 19 | BL-12 | Fix the fork-only '19 anti-patterns' sites (README.md:709 and :711, docs/RELEASE_HISTORY.md:34; decide whether to touch the frozen copy at docs/versioning-archive.md:21), grepping both phrasings; the list has 20. Strike the stale 'issue #65 is open' bullet (it closed 2026-08-12). The one distributed site, workstreams/RESEARCH_DOCUMENTATION_WORKSTREAM.md:55, goes in the post-large-pull-request prose delivery (BL-11) and the row closes then. | S | no | PR #92 merged and the fork resynced |

**7. The trimmer rows, after the #94 fixes settle**

| # | Row | The one deliverable | Size | Outward? | Waits on |
|---|---|---|---|---|---|
| 20 | BL-32 | Settle SESSION_NOTES.md in the trimmer once #94's outcome is known: build the entry as its own pull-request branch (fork-side, nothing pushed) with a policy for a file that is overwritten every session and must be read whole, or drop it, or design a supported adopter-extension mechanism (the row's option (b)). Do not port commit `2308553` (the entry as it sits on #94) to fork main or the candidate as it stands: neither carries it (`grep -c SESSION_NOTES starter-kit/methodology_trim.py` reads 0 on fork main). | M | yes | BL-98 |
| 21 | BL-58 | Extend FRAMEWORK_APPARATUS.md's 'Reading and archiving' section for the five hazards it still lacks (reconcile before trimming, the regrowth refusal as a property of the rule, net-additive trims, retention depth, never trim to zero), once, after #94's trim-timing paragraph is settled. The section is already upstream through PR #84, so this is an extension; runner text is priced out (about 66 B of room). | M | yes | BL-98 |
| 22 | BL-60 | Hold the planning session for the proof-script pile (177 tracked .verify.sh files, about 3.07 MB, about 20.5 KB added per trim) and cost its three shapes against the proof template as it stands after BL-98's fixes. The same plan decides: whether a trim still writes a pointer block (BL-42's target); whether the 'This file currently holds N' field ships in the seed or the tool stops declaring it (BL-48); the four old failing proofs of BL-36, read with --reverify and never regenerated first; and wsfct's one proof that stays red even under --reverify (BL-30's leftover). | multi_session | yes | BL-98 |
| 23 | BL-42 | One trimmer release (a new methodology_trim.py version): BL-42's decision on the pointer block (a regenerated field, an external index, or nothing; 68 hand-fold commits so far), BL-50's one-newline symmetry fix written first as a test case that design must pass, and BL-49's check that counts date-looking headings against matched records when records are present. Built on the merged tree after BL-60's two decisions; fork-side up to the pull request. | M | yes | BL-60 |
| 24 | BL-52 | Decide what each read-cap dashboard row claims for a ledger that sessions read whole (SESSION_NOTES.md, which a session overwrites each time, is a live case), and annotate the two of the row's five leftovers that are already fixed (the `CHANGELOG.md` archive rule, commit `dee680c0`; the `READ_CAP_WATCHED` justification, commit `9e71f83a`). | M | yes | BL-32 |
| 25 | BL-51 | Phase C3 at its full scope: a check that the front matter plus the K newest records fit one read (with edge tests on both sides), BOOTSTRAP.md's worked example of the Class A (whole-file ledgers) and Class B (index-style files) split, and the Class B dashboard row's wording. It must regenerate the row-text pin that BL-88 froze (tools/test_methodology_dashboard.py:6048-6063). | M | yes | BL-52, BL-32 |

**8. Second deliveries after the large pull request**

| # | Row | The one deliverable | Size | Outward? | Waits on |
|---|---|---|---|---|---|
| 26 | BL-46 | The receipt-seed hunks in starter-kit/HANDOFFS.md: rewrite the closing instruction at :196-198 so an adopter deletes the sentinel, the standalone '---' and the comment (the leftover '---' makes their trimmer refuse with ZONE_UNCLASSIFIED), and carry BL-14's leftover sentence at :163-165 reworded as an allowance; test that a fresh seed trims clean. Not BL-48's sentence (decided inside BL-60). One small delivery. | M | yes | BL-101, BL-60 |
| 27 | BL-84 | One seed-configuration pull request after the maintainer answers his own issue #95: BL-84's smallest shape (raise CLAUDE.md's 24,000 B warn line by the 800-character fence floor and count bytes, not characters, at context_budget.py:546), BL-47's HANDOFFS.md entry at a ceiling derived as peak receipts x 12,288 B plus the reserve (not the fork's 65,536 copied), and BL-37 half (b)'s BACKLOG.md entry with a derived ceiling. Never inside the large pull request. | M | yes | BL-114, BL-32, BL-108 |
| 28 | BL-71 | One dashboard release, 2.23.0, both byte-identical copies and one test update, after the large pull request and after the maintainer answers decisions 2(a) and 2(d) of draft 11: count local unmerged branches without hard-coding 'main' (the current count reads every line of git branch -a, so a fork can never clear the warning), plus BL-68's chosen remedy and BL-90's 'locally edited' note. | M | yes | BL-101 |
| 29 | BL-11 | The post-large-pull-request prose delivery: the mechanical provenance-token edits (HOW_TO_USE.md:863 'anti-pattern #31', RECOMMENDED_SKILLS.md:75 and the receipts seed 'session S1', the dashboard's remaining BL-5 lines) plus BL-12's one distributed site; and the one real question, an exception to the Learnings table's append-only rule for four Source cells, asked once in the large pull request's own thread, where draft 11's decision 4 already raises provenance tokens. | M | yes | BL-101 |

**9. Last: the hook check and the adopter track**

| # | Row | The one deliverable | Size | Outward? | Waits on |
|---|---|---|---|---|---|
| 30 | BL-77 | Phase 0 never checks that this clone's commit hook is switched on (core.hooksPath). Prefer shape (3): the hook records that it fired and a check reads the trace against the commits the session already reconciles, which costs no runner bytes. He must pick the shape first. It edits .githooks/pre-commit, which the candidate carries in scrubbed form, so build it after the candidate's hook is final. | M | no | BL-101 |
| 31 | BL-105 | Phase 4 on the remaining adopters, one adopter per session on a tree with no live Claude session and no uncommitted change (check pgrep -x claude and lsof first): model_project_constructor needs his go-ahead for the second stage (`--tier 2`), mts-system and wsfct need their directory-move migration first, nprcgenekeepr waits on BL-32's outcome (its 49-line local trimmer patch is still dropped by a forced sync unless the SESSION_NOTES.md entry becomes canonical). Not gated by the large pull request: plan D8 puts adopters before it. | multi_session | no | BL-32, a free adopter tree |

**Folded into a lead row** (they get no session of their own): BL-87 into BL-93; BL-111 and BL-112 into BL-109; BL-73 and BL-16 into BL-89; BL-61 into BL-108; BL-88 into BL-101; BL-36 and BL-48 into BL-60; BL-49 and BL-50 into BL-42; BL-37 and BL-47 into BL-84; BL-68 and BL-90 into BL-71. **No work:** BL-91 (gating the growth of the session-reading load was declined by his decision of 2026-09-28 and may not be re-proposed unless he reopens it; its release clause waits on decision D3 of its plan, which he has not ratified).

**What changes the order.** (a) *The replies' content.* If #94 merges unchanged, the resync comes early and the trimmer tier moves ahead of the fork-only fixes; if it asks for changes, the BL-98 sessions dominate; if PR #92's reply asks for edits to `README.md` or `CLAUDE.md`, they are made before the tier-6 rows. (b) *His answers on the held rows.* (c) *A free adopter tree*, which makes BL-105 offerable any day.

---

## 6. The decisions that are his

### 6.1 Rows held on his call

| Row | Why it is held | What he decides |
|---|---|---|
| BL-114 | On his hold since session 329 (restated in the three latest close-out records): the comment on the maintainer's own issue #95 (a fresh install fails its own context budget) is drafted, not posted. It also gates the seed pull request (BL-84 with BL-47 and BL-37). Not proposed. | Edit the drafted comment and say whether to post it; nothing is built, recomposed or posted until he releases the hold. |
| BL-115 | On his hold since session 329: one runner sentence (283 B) about reading a large HANDOFFS.md; the candidate's runner has about 66 B of room, so it needs an equal cut. Not proposed. | Whether to release the hold, and if so the route (its own pull request, a comment, or BOOTSTRAP.md) and what the runner cuts to pay for it. |
| BL-94 | Every next step is his: nothing for a session to do and nothing to spend. The only free chore, the stale 'next phase' line in the plan header, rides the sweep's relabel. | A third paid rater run (about $1.60, an estimate, against the study's own $100 cap), or his own blind rating of the six-record packet, or declare the study finished at its null reading on the mechanical scorers. |
| BL-104 | A decision row, not work: moving this repository's own ledgers under methodology/ (option B2) pays only if the maintainer adopts the layout or he accepts hand-resolved ledger conflicts at each resync. Building the four repairs first is rework, because they rewrite tests that BL-61 and BL-108 edit. | Whether he wants B2. The second branch (accept hand-resolved conflicts) is his alone and can be answered now; the first needs the maintainer's reaction to the directory. If neither, close the row DECLINED. |
| BL-64 | A choice among shapes, not a build: shape (c), already written at SESSION_RUNNER.md:20, needs no edit, but as practised the comparison reads the saved output of the pre-close-out run and cannot see the close-out commit; only a re-run at HEAD can. | Accept the window (closes the row with no edit), or re-run the gate after the close-out commit, or add a Phase 0 reading of the citation. |
| BL-70 | Upstream's runner lacks the plan-surface rule from issue #75, which the maintainer closed NOT_PLANNED on 2026-09-02; his pick at session 189 kept the unsent branch and left the upstream route open. Folding it into a later pull request needs +1,977 B against about 66 B of room. | Ask on #75 (an outward step), fold it into a later runner pull request after a byte-accounting session, or decline and delete the local branch. |
| BL-39 | The close-out half of issue #75; it has no logical dependency on BL-70, only the same vehicle and the same scarce runner bytes. | Follows BL-70's answer: if BL-70 is declined, shrink it to the receipts seed's runtime_smoke leading surface token (starter-kit/HANDOFFS.md:62, which both checker parsers already tolerate) and the flight manual, leaving the runner untouched; if BL-70 goes, it rides with it. |
| BL-79 | The close-out report tool and its Stop hook are built; what is outstanding is his action. Phase P3 (shipping the tool to adopters) is a separate pull request of at least six files (manifest including a new-layout row, both dashboard copies and their test, SAFEGUARDS.md, the runner), so it must be split, and the composition plan … | Install the Stop-hook snippet in .claude/settings.local.json himself (a session must not edit hook settings), watch one close-out, then say go for P3. |
| BL-103 | A gate that outlives its time budget now reads unmeasured; three repairs are done, three small calls remain and each is routed to a different place. | (b) keep or lower the 3,600 s budgets (config only); (a) mirror timeout_seconds in the dashboard (joins BL-71's release); (c) make --run print the unmeasured gate names (a ratchet 1.6.0). |

### 6.2 Questions the orderings could not settle

Each has the synthesis's recommendation; none is a go-ahead for an outward action.

1. **Does BL-102 ride the candidate's rebuild?** *Yes:* the defect is on the candidate, its own layout move makes it reachable, and the rebuild must be re-measured anyway, so it is one small commit (three of five orderings). *No:* ship it after the large pull request with BL-103(c) and BL-92(c), because any added commit re-opens approved text. **Recommendation:** ride it after BL-113's guard and let him decide at the re-approval; declining is also safe.
2. **Does the large pull request wait for #94 to merge, or only for its fixes to be pushed?** Decision D4 says build on #94's merge; a candidate built on an unmerged branch is rebuilt again if review changes it. **Recommendation:** wait for the merge; if #94 is still open when the rebuild is ready, ask him whether to stack on it or supersede it. Decision D4's date of 2026-10-25 still governs: the maintainer's first replies (2026-10-19) asked for changes and the fork answered them the same day, but neither #92 nor #94 is merged, and he confirmed on 2026-10-23 that D4 stands.
3. **Which retention depth does BL-108 deliver?** His pick of 2026-10-15 (as the row records it: trim above three, "about half the trims", cutting to two) or the practice since (cut four to three, so a trim falls due every session). **Recommendation:** do the Test 34 fixture work and deliver depth two, because his decision was made and no gate may be loosened; fall back to writing depth three down only if he judges the rework not worth it.
4. **BL-42: wait for the post-BL-60 release, or write a fork-only "fold the pointer block" helper now?** **Recommendation:** wait; a helper is a different deliverable the release would delete, and a script carrying bare ledger file names trips the layout-literals scanner. Raise it as its own row only if he wants relief before then.
5. **May a session decline BL-18, 39, 64, 68, 70 and 103 inside the sweep?** The adversary ordering said yes; four orderings and both judges said no. **Recommendation:** no unilateral declines. BL-64, 70, 39 and 103 go to his picker; BL-18 stays as work; "leave as is" is an acceptable answer for BL-68. (Issue #75, which BL-70 and BL-39 descend from, was closed "not planned" by its own author on 2026-09-02.)
6. **Where does BL-117 go?** Early (its first measurement has a known cause) or last (its baselines move with every suite change). **Recommendation:** after the fork-only fixes (position 16); trimmer-suite targets wait for the trimmer; no concurrent running before BL-92.
7. **May other batches ride the candidate's rebuild window** (dashboard 2.23.0, ratchet 1.6.0, BL-12's distributed site, BL-110)? **Recommendation:** only BL-113 and BL-102; the prose layer carries layout only, the dashboard fixes exist unchanged upstream, and each added hunk needs a new scan and re-measure.
8. **Is the adopter track gated by the large pull request?** **Recommendation:** no; the real gates are a free tree, his go-ahead for the migration tool's second stage (`--tier 2`, which moves a project's own notes and ledgers), his calls on findings F7 and F19 in the directory-move findings register (whether a forced sync may drop nprcgenekeepr's 49-line local trimmer patch), and each adopter's own migration.
9. **When should BL-77 be built?** **Recommendation:** late, shape (3), after his pick; Phase 0's ledger reconciliation already catches commits that skipped the ledger, and the hook rides the candidate in scrubbed form.

---

## 7. What failed verification

Of 163 candidate interactions, **96 survived and 67 did not**: 36 refuted by all three skeptics and 31 by two. By the kind each finding finally carried (survived out of found): status drift 35 of 35; subsumption 21 of 37; dependency 13 of 37; collision 9 of 20; proposal change 9 of 19; upstream route 9 of 15. The pattern is useful to anyone re-proposing one of these:

- **In nearly every refuted finding the cited lines were real.** What failed was the step from "two rows touch one file or one topic" to "the order or the fix must change". Topic adjacency is not a dependency.
- **Several refuted claims were already recorded inside the row they concerned** (an in-session rule mistaken for a cross-session one; a "collision" between rows that edit different regions).
- **Dependencies were the weakest class:** 24 of 37 failed, most because the second row did not actually need the first, or the first did not change the second's fix.
- **A finding that survived often survived narrowed.** Skeptics attached a correction to half of the survivors (48 of 96), and the narrowed form is what this document uses (for example, "BL-90's local-edit fact is BL-90's own; it is not a BL-32 dependency").

All 163 findings, with their verdicts, are in [`backlog-interaction-review-evidence/findings.md`](backlog-interaction-review-evidence/findings.md).

---

## 8. Method and limits

- **Cards.** 15 agents, five rows each, read every row's index line, its full body, its cited commits, files and pull requests, and wrote a card (status on the evidence, scope, artifacts, proposed fix, blockers, standing decisions). 75 cards.
- **Interactions.** Six agents, one lens each (same-file collisions; dependency and sequence; subsumption and supersession; status drift; the upstream route; improving the proposed fix), each reading all 75 cards and the files: 163 findings.
- **Verification.** Three skeptics per finding (an evidence lens, an "is it really an interaction" lens, a standing-decisions lens), a majority to refute: 489 agents. The first run hit the Fable usage limit with 318 of those 489 failed; the 192 completed results were replayed from the run's journal and the 318 re-run after the session model changed to Sonnet 5.5. I did not record which verdict came from which model.
- **Order.** Five orderers (dependency and rework; his time and silent failure; the upstream route; backlog truth first; an adversary), three judges, one synthesis: 9 agents. In total 519 agents, about 37.6 million subagent tokens and 6,400 tool calls.
- **Checked by me directly,** not taken from an agent: the state of 13 pull requests and 5 issues (#66, #68 to #71, #73, #76, #84, #86 to #88 merged; #94 and #92 open; issues #65, #67, #75 closed; #93, #95 open); `BACKLOG.md`'s token reading and `CLAUDE.md`'s overage (`context_budget.py --status`, which wrote nothing); the 52-of-75 "Open:" list; 13 anchorless bodies and 10 dangling links; `grep -c SESSION_NOTES` on the fork's trimmer (0); `quality_ratchet.py:666` on fork `main` and on the candidate (identical); the candidate runner's 53,100 bytes and its 18,900-token ceiling; the `-failed` migration gate on the candidate and its absence on fork `main`; both plans' sizes (29,996 and 59,994 bytes).
- **Not checked by me:** each card's fields (a card was built by one agent and tested only through the findings that rest on it); line numbers in the skeptics' evidence beyond those above; the adopters' state (BL-30's three adopters, BL-105's remaining four); draft 11's figures (22 conflict regions; 400, 910 and 58 differing lines; 31 of 47 candidate-touched files still differing); anything the maintainer's comments say.
- **The comments.** See [§1](#1-the-answer-first): this session did not read them. The review's agents had read-only `gh` and several read them despite my telling them the text was unread; I did not forbid it. Their summaries were left out of this document.
- **An order is advice.** Nothing here edits a row, approves an outward step or lowers a threshold. Re-derive the population with `grep -nE '^\*\*BL-[0-9]+ —' docs/planning/BACKLOG-DETAIL.md` and the status counts with the commands in [§2.3](#23-three-defects-of-the-record-itself), because this backlog has been wrong before.

---

## Appendix A: every row and where it goes

| Row | What it is | Status on the evidence | Where it goes |
|---|---|---|---|
| BL-11 | Fork-only session, backlog and layer numbers still ship inside five adopter-facing files | open | Position 29 |
| BL-12 | "19 anti-patterns" stands at four sites while the list has 20; … | partly done | Position 19 |
| BL-13 | The /caveman row's false "handoff length discipline" claim: fixed by merged upstream PR #68, row never … | done, still listed | Close in the sweep (position 2) |
| BL-14 | The receipt's commit: field promised a reconcile nobody owned; … | done, still listed | Close in the sweep (position 2) |
| BL-16 | bin/check-handoff's docstring says this repo has no root receipt ledger; … | open | Folded into BL-89 (position 9) |
| BL-17 | Receipt changelog_ref locator form: the upstream half merged as PR #69; … | partly done | Close in the sweep (position 2) |
| BL-18 | Bare line numbers into the live ledgers inside receipts' key_files, where the checker's own rule … | open | Position 14 |
| BL-19 | Index row for the context-cost plan (session 30): queue items 34 to 40 shipped, 41 to 45 never started, body … | partly done | Position 17 |
| BL-20 | Residual of a fixed parser defect: which Model-line form the seed documents; … | superseded | Close in the sweep (position 2) |
| BL-21 | Two seed sentences for a hook exemption that was removed on 2026-09-16; … | superseded | Close in the sweep (position 2) |
| BL-22 | Dashboard's 200-line doc-only threshold: reason and pinning test shipped upstream (PR #70 merged); … | done, still listed | Close in the sweep (position 2) |
| BL-23 | Upstream issue #65 vs the fork's unshipped Learnings-table move: issue closed, both sides merged … | superseded | Close in the sweep (position 2) |
| BL-26 | Issue #67 (dashboard --sync warning) and PR #66: both resolved upstream; the row still reads partly open | done, still listed | Close in the sweep (position 2) |
| BL-30 | Watch item: has the ledger trimmer fired outside nprcgenekeepr? It has, in all three named adopters and … | superseded | Close in the sweep (position 2) |
| BL-31 | Upstream dashboard did not exclude context_budget.py from adopter code counts; … | done, still listed | Close in the sweep (position 2) |
| BL-32 | The ledger trimmer knows only two ledger files; an adopter with a third has no supported way to trim it | open | Position 20 |
| BL-36 | Four of the oldest archive losslessness proofs still fail; the archives are intact; … | blocked | Folded into BL-60 (position 22) |
| BL-37 | Context-budget gate: running it on this repo is done; a BACKLOG.md ceiling in the distributed seed … | partly done | Folded into BL-84 (position 27) |
| BL-39 | Carry the verification surface into close-out: Phase 3E, the runtime_smoke receipt field and the flight … | open | Held on his call |
| BL-42 | The ledger trimmer still writes a 3-line pointer block into HANDOFFS.md that every trim session then … | open | Position 23 |
| BL-44 | check-learnings' success line now prints the true span but still does not name the reserved number it … | partly done | Position 15 |
| BL-46 | The seed receipts file's trailing footer leaves an adopter's trimmer unable to run, and nothing detects … | partly done | Position 26 |
| BL-47 | The seed context-budget config does not list HANDOFFS.md, the file the trimmer bounds; … | partly done | Folded into BL-84 (position 27) |
| BL-48 | The seed receipts file lacks the 'This file currently holds **N**' sentence the trimmer declares it … | open | Folded into BL-60 (position 22) |
| BL-49 | The trimmer looks for unreadable entries only when it finds zero records, so a partial mismatch is … | open | Folded into BL-42 (position 23) |
| BL-50 | Trimmer refuses a correct trim when front matter ends in one newline: insertion adds a byte its proof … | open | Folded into BL-42 (position 23) |
| BL-51 | The distributed '2,000-line read cap' claim is false; Phases A, B, C1 and C2 shipped, Phase C3 still … | partly done | Position 25 |
| BL-52 | Whether trimming a newest-on-top ledger delivers anything a read did not already get: the line metric's … | partly done | Position 24 |
| BL-54 | bin/sync and bin/status missed versions hidden by a merge; fixed, merged upstream in PR #87, but the … | done, still listed | Close in the sweep (position 2) |
| BL-55 | Nothing enforces removing a completed BACKLOG.md item; the only detector reports and cannot tie an item … | open | Position 3 |
| BL-57 | The CHANGELOG.md rules contradicted each other; fixed here, in six adopters, and merged upstream as PR … | done, still listed | Close in the sweep (position 2) |
| BL-58 | Adopters receive the ledger trimmer but almost no instructions on using it without losing entries | partly done | Position 21 |
| BL-60 | Every ledger trim writes a 16-20 KB proof script nearly identical to the last one, and the pile keeps … | open | Position 22 |
| BL-61 | Lower the handoff checker's 7,168-byte header reserve now that HANDOFFS.md's front matter stays near … | open | Folded into BL-108 (position 10) |
| BL-62 | Upstream's read-cap partition test summed every whole-read class as one read; … | done, still listed | Close in the sweep (position 2) |
| BL-63 | One bin/sync run writes more files than the five-file commit cap allows, and no shipped document said … | done, still listed | Close in the sweep (position 2) |
| BL-64 | A close-out cites a gate run taken before the close-out commit exists, so that commit is never covered | partly done | Held on his call |
| BL-65 | A context-budget test failed on a machine whose transcripts fit a negative slope, and skipped in every … | done, still listed | Close in the sweep (position 2) |
| BL-66 | README told adopters to update from the GitHub URL, a route that could not update a file that was … | done, still listed | Close in the sweep (position 2) |
| BL-68 | Investigate the dashboard's 'Large files detected' risk when the large files are the framework's own … | open | Folded into BL-71 (position 28) |
| BL-70 | Upstream's session runner still lacks the plan-surface rule from issue #75; … | open | Held on his call |
| BL-71 | The dashboard's 'Multiple branches' warning counts every line of git branch -a, so a fork can never … | open | Position 28 |
| BL-73 | check-handoff reads a receipt opened twice as one block and reports it only when some other rule … | open | Folded into BL-89 (position 9) |
| BL-74 | Keep README.md current: the canonical file's cost section is stale, and five adopters carry copies that … | open | Position 18 |
| BL-75 | context_budget.py's missing --status flag was fixed and merged upstream as PR #86 on 2026-10-01, but … | done, still listed | Close in the sweep (position 2) |
| BL-77 | Phase 0 never checks that this clone's git commit hook is switched on, so a disabled hook fails silently | open | Position 30 |
| BL-79 | The runner's close-out report (step 3G) has no required shape; … | partly done | Held on his call |
| BL-80 | Context-budget tool's growth-run note contradicted its own table; … | done, still listed | Close in the sweep (position 2) |
| BL-81 | This repo's .context-budget.json states the two read-set file sizes in three places, and two of them … | open | Position 12 |
| BL-84 | The distributed budget seed gives CLAUDE.md a fixed 24,000 B warn line and a mandatory 800-character … | open | Position 27 |
| BL-85 | The rules that stop a prose update from wiping an adopter's ledgers reached upstream in PR #88 … | done, still listed | Close in the sweep (position 2) |
| BL-87 | Nine item bodies in the backlog detail file have no anchor line, so their [detail] links point at … | open | Folded into BL-93 (position 2) |
| BL-88 | The dashboard's read-cap class row: fixed on the fork (2.19.0); … | partly done | Folded into BL-101 (position 7) |
| BL-89 | check-handoff validates the newest receipt's fields, not the ledger's structure, so a duplicated … | open | Position 9 |
| BL-90 | The dashboard's --sync overwrites a copy's locally edited EXCLUDE_DIRS without warning, and the … | open | Folded into BL-71 (position 28) |
| BL-91 | The framework's per-session reading load rose 4.6x over 27 releases; … | partly done | No work: his earlier decision stands |
| BL-92 | The test suite went red once in five runs at one commit, and the ratchet threw away the output that … | open | Position 11 |
| BL-93 | The hand-kept 'Open:' list at the top of the backlog omits open items: 23 of 75 today, up from 5 of 57 … | open | Position 2 |
| BL-94 | Documentation-quality experiment, v3.8 against v3.0: harness built, pilot run for $4.09; … | blocked | Held on his call |
| BL-98 | The trimmer's proof script fails on lossless trims (issue #93): fixed on the fork, sent as PR #94, … | done, still listed | Position 1 |
| BL-101 | Move every adopter's methodology files into one methodology/ directory, then send the one upstream pull … | partly done | Position 7 |
| BL-102 | The ratchet's hook installer writes a symlink-dependent tool path that fails after the directory move | open | Position 5 |
| BL-103 | A gate that outlives its time budget read as pass, fail or a wrong number; … | partly done | Held on his call |
| BL-104 | Moving this repository's own ledgers and configs under methodology/ is blocked by four measured defects | open | Held on his call |
| BL-105 | PROJECT_LEARNINGS.md moves with the methodology files as a companion; … | partly done | Position 31 |
| BL-106 | The directory-move plan declares a 60,000-byte size limit that no automated check enforces | open | Position 13 |
| BL-108 | The HANDOFFS.md keep-two rule makes a receipt trim fall due at every session start | partly done | Position 10 |
| BL-109 | The migration-tool test gate counts tests but ignores a failing exit code, so a red suite can pass | open | Position 8 |
| BL-110 | No check catches a wrong directory path written as code text, or the new layout prose, in a shipped … | open | Position 6 |
| BL-111 | Three checker tests written for the upstream pull request are missing from the fork's own test suite | open | Folded into BL-109 (position 8) |
| BL-112 | The migrate-layout tool's header lists exit codes 0 to 3, but the tool also exits 4; one line is missing | partly done | Folded into BL-109 (position 8) |
| BL-113 | The pull-request candidate's session runner read over its token ceiling; … | partly done | Position 4 |
| BL-114 | Upstream issue #95: a fresh install fails its own context budget; … | on his hold | Held on his call |
| BL-115 | The session runner never says how to read a large HANDOFFS.md; … | on his hold | Held on his call |
| BL-117 | A session to profile and speed up the fork's own test suites and gate run, starting from measured … | open | Position 16 |

## Appendix B: the forty-six changed proposals

| Row | Was | Now |
|---|---|---|
| BL-98 | No further fork work; watch PR #94 by gh and treat any maintainer comment as a go-ahead question; D4 says ask again on or after 2026-10-25. | Active, first in line: read and answer the maintainer's reply on #94 (position 1). Any fixes it asks for are made once on #94's branch and ported to fork main and the candidate. Nothing is pushed or posted without his go-ahead. |
| BL-32 | A decision not yet made, or later 'decided at session 335 and built on #94 as commit 2308553'. | Decide after the #94 reply is read. Do not port #94's commit `2308553` (the SESSION_NOTES.md ledger entry) to fork main or the candidate first; the reply may change what that entry should be. |
| BL-30 | Close it by pointing at BL-36, BL-60 and BL-98, which supposedly own its proof question. | Close it with the measured read-only proof results; wsfct's one proof that stays red under --reverify goes into BL-60's brief. |
| BL-14 | A small fork-local fix to the seed sentence at starter-kit/HANDOFFS.md:163-165. | Closed; the sentence is upstream's own text too (f34769f:164), so its reword is a hunk in BL-46's seed delivery. |
| BL-48 | Ship the 'This file currently holds N' sentence in the receipts seed with N=0. | A decision inside BL-60: ship the field, or stop the tool declaring it. The fork removed that sentence on purpose on 2026-09-16 (session 172). |
| BL-60 | Hold the planning session when picked, independent of #94, against the 16 KB proof of trimmer 1.5.0. | Hold the planning session after #94's outcome settles (any change to the proof template lands first), costed against the 1.8.x template (about 20.5 KB per trim), with a wider brief: the pointer block, the count field, BL-36's four proofs and BL-30's wsfct leftover. |
| BL-42 | Runnable fork-side up to the pull request; make the pointer region a regenerated field. | One trimmer release after BL-60's two decisions, together with BL-49 and BL-50; BL-50's one-newline case is a test the design must pass. |
| BL-102 | Its own session at ratchet version 1.3.1, with its own go-ahead. | Fix on fork main as 1.5.1 and, if he agrees, carry as one commit onto the rebuilt candidate; otherwise a later ratchet release. The body's 1.3.1 is stale (the tool is 1.5.0). |
| BL-103 | Three small calls, all his. | Held on him, with each call routed: (b) keep or lower the 3,600 s budgets is config only; (a) the dashboard's timeout mirror joins BL-71's release; (c) --run printing the unmeasured names is a ratchet 1.6.0, with BL-92's shape (c) if BL-102 did not ride the rebuild. |
| BL-71 | Count 'git branch --no-merged main'. | Count local unmerged branches without hard-coding main (it reads 0 on master-default repos), in one dashboard 2.23.0 with BL-68 and BL-90, after the large pull request. |
| BL-68 | Four investigation steps before choosing among four remedies. | Step 1 is already answered (the score has no size term; the flag is a risk row), so pick a remedy inside the dashboard release; 'leave as is, reason recorded' is allowed. |
| BL-90 | No shape proposed; three starting points. | The warn shape (a 'locally edited' note in --sync's dry-run preview) in the dashboard release; the side-file shape only if he refuses decision 2(a). |
| BL-89 | Three starting points, and unsure whether it differs from BL-73. | Same change as BL-73: default mode shows scan()'s findings and runs the duplicate and pending checks, plus a doubled-opener finding and a block count that tolerates the format example; BL-16 rides. |
| BL-109 | Design a second gate over the same command with no extract (fresh work). | Copy the written pair and the corrected 'why' from pr2/candidate:.quality-gates.json:77-91. |
| BL-111 | Port three tests, or port only if the pull request is sent. | Port them now and raise the gate from 15 to 18 (18 OK measured in a scratch copy). |
| BL-112 | Add a one-line exit-4 clause keeping fork and candidate byte-equal. | Copy the candidate's two-line wording from a62bfecf; byte-equality is already gone (blobs 06afa06b and fa96034c). |
| BL-65 | Three shapes, none costed. | Close, citing 229f08d9; its side note survives only as BL-109. |
| BL-20 | Change the receipts seed to document the bare Model line. | Close as superseded without touching BACKLOG-COMPLETED.md:90, which a byte-exact proof pins. |
| BL-21 | Append two sentences to two seed files when the hook goes upstream. | Never write them: they would describe an exemption no hook has. |
| BL-66 | Run P6 and close both rows once the merge lands. | Close with BL-54; verify with the METHODOLOGY_SOURCE_URL override; raise bin/status's missing shallow-source check as its own row first. |
| BL-75 | Bookkeeping only (the card says the 'flag does not exist' note is already gone). | Close together with BL-80 in the commit that rewrites .context-budget.json:92, which still says the flag does not exist; skip the CLAUDE.md:102 reword. |
| BL-87 | Nine bodies lack an anchor; three shapes uncosted. | Thirteen bodies lack an anchor and ten links dangle (checked: 94 headings, 81 anchors); add them inside the sweep. |
| BL-93 | Repair the hand-kept list, delete it, or gate it; none costed. | Delete it inside the sweep (it names 52 of 75 rows, checked); BL-55 then gates the backlog proofs. |
| BL-55 | Four costed options, none decided. | Fork half: wire the two backlog proofs as no-extract max-0 gates after the sweep; the adopter-facing half is a separate decision. |
| BL-108 | Edit the rule to trim above three and cut to two. | Ask which depth he meant; depth two at rest needs Test 34 off the live ledger or the tests-sh-passed gate reads 497 under its 503 floor; otherwise write down depth three. |
| BL-61 | Must follow BL-108 in one session. | Independent in substance; co-edit with BL-108 to state the fit once and size the reserve for the 5,287 B trim-commit front matter. |
| BL-84 | Four shapes, none costed, its own go-ahead. | Take the smallest shape inside one seed pull request with BL-47 and BL-37(b), after issue #95 is answered and the SESSION_NOTES.md policy is known. |
| BL-47 | Add CHANGELOG.md and HANDOFFS.md to the seed at 65,536. | HANDOFFS.md only, at a ceiling derived as peak receipts x 12,288 B plus the reserve. |
| BL-113 | Option (e) is his call; also whether to strip the density hunk. | Do (e) before any further candidate commit; keep the density hunk and amend the plan's 'Not carried' cell. |
| BL-74 | Four shapes, none chosen. | Shape (4) first (rewrite the stale cost section), after PR #92 merges and the fork resyncs; shape (1) (a README row in the manifest) is a change to the directory move's machinery and comes after the large pull request. |
| BL-58 | Choose among an apparatus section, runner text or tool output, with the apparatus count at zero. | Extend the existing apparatus section for the five uncovered hazards, once, after #94's paragraph settles; no wait for BL-42. |
| BL-12 | One commit changing all four sites, the distributed one riding the large pull request. | Five tracked sites; fork-only sites after the resync; the distributed site goes in the post-pull-request prose delivery. |
| BL-11 | Put one decision to the maintainer through an issue. | Mechanical edits in the post-pull-request prose delivery; the one question asked in the large pull request's own thread. |
| BL-51 | Phase C3 reduced because BL-88 delivered the Class B remedy. | C3 keeps its full scope and must regenerate the row-text pin BL-88 froze. |
| BL-105 | nprcgenekeepr waits on his call about the forced sync. | It waits on BL-32's outcome; the other adopters wait on free trees and their migrations, not on the large pull request. |
| BL-117 | Profile from the session 335 baselines (199 trimmer tests, 18 gates). | Re-baseline first (222 tests; 18 gates today, more after BL-109 and BL-55) and start with the double-run measurement. |
| BL-110 | Count the legitimate mentions, then choose a shape. | The count is done (11 in 3 of 23 documents); write the rule once, pre-send, in both copies of bin/check-links. |
| BL-39 | Wait for BL-70's plan-time half before the close-out half. | No logical dependency; held with BL-70's route, and shrinks to the seed token plus the flight manual if BL-70 is declined. |
| BL-70 | Ask on #75, fold into a later pull request, or decline. | Fold-in is priced out (+1,977 B against about 66 B of room); the choice is ask or decline, his call. |
| BL-64 | Choose among three uncosted shapes. | Shape (c) is already written at SESSION_RUNNER.md:20, so accepting it needs no edit, but the practised comparison cannot see the close-out commit. |
| BL-46 | Batch with BL-47, BL-48 and BL-49 in one pull request. | Its own small seed hunk set with BL-14's sentence; BL-48 and BL-49 are not in it. |
| BL-88 | Awaiting ratification; upstream delivery rides the large pull request. | Fork-side done; closes when the large pull request merges with decisions 2(a) and 2(d) kept. |
| BL-101 | Wait for the maintainer until 2026-10-25, then three go-aheads. | Resync, rebuild on the merged trimmer, re-measure draft 11, then the three go-aheads. The 2026-10-25 wait date still governs (he confirmed D4 on 2026-10-23): the maintainer's replies of 2026-10-19 asked for changes and the fork answered them, so the rebuild waits for their outcome. |
| BL-92 | Three uncosted shapes. | Shapes (a) and (b), fork-only, now; shape (c) waits for a later ratchet release. |
| BL-106 | Gate the directory plan only. | Cover both plans; both gates are green on arrival. |
| BL-19 | A title-only row for a plan whose queue is unstarted. | Re-indexed in the sweep (queue items 34 to 40 shipped, the plan's section 7 ratified); only item 42 is a session, after #92. |
