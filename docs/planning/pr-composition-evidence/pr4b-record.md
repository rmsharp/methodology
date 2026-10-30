# PR4, the text of the pull request, re-checked on the rebuilt branch: the record (S397, 2026-10-29)

Row PR4 of `docs/planning/upstream-pr-composition-plan.md` section 5 (line 182), as the PR2b row asks (line 180): a body in recognised terms, every number tied to a command, each claim of section 6 re-run, a fresh reader on a frozen draft, shown inline. Local only; nothing is sent to `KJ5HST/methodology`. The text is [`../upstream-pr-body.md`](../upstream-pr-body.md) (everything below its first rule), now **draft 12**; draft 11 is `git show 7d00d29:docs/planning/upstream-pr-body.md` (approved by him at the S338 picker). The branch is the local ref `pr2b/candidate` at `47637be2` (33 commits on `upstream/main` `d50ce290`); the control is upstream's tip. The baseline is [`pr4-record.md`](pr4-record.md) and [`bl119-record.md`](bl119-record.md) (the old branch `pr2/candidate`, 34 commits on `f34769f`). Every figure is printed by a script here or by a command named beside it; saved outputs sit beside this file as `pr4b-*-output.txt`.

## 1. The answer

1. **Draft 12 exists** and is committed twice: first as `357ae739`, frozen for the cold reader (23 edits, 21,612 B), then revised after the read (section 7). It is draft 11 with **26 exact-once edits** ([`pr4b-draft12-build.py`](pr4b-draft12-build.py), which refuses unless the file is draft 11 as `7d00d29` holds it). The body is **21,802 B** (draft 11: 21,486 B; his budget: 20,000 B, which draft 11 already exceeded at his word).
2. **Draft 11 could not be posted as it stood, and one edit was not a number.** #92 and #94 merged on 2026-10-24, so its decision 3 (the order against #94, with merge counts against #94's old head) described a pull request that no longer exists. The rebuilt branch carries none of #98 (the second pull request, open) and both name the trimmer 1.9.0, so decision 3 is rewritten, not re-measured. #96 (open) also conflicts with the branch (3 regions in 2 files); draft 11 never named it.
3. **Every claim of section 6 holds on the rebuilt branch** (section 2), and 26 edits were made (section 3). Six of the changes are not stale numbers but an obsolete question, a false citation, and four sentences that were false or that the rebuilt series made false (section 4, items 1 to 4, 6 and 7).
4. **The old and the new branch differ in 9 files only** (`pr4b-facts-output.txt` section 4: the ledgers, `README.md`, `CLAUDE.md` and `FRAMEWORK_APPARATUS.md`, which are upstream's own movement; `.quality-gates.json`, the trimmer, its tests and its fixture, which are the rebuilt trimmer layer). So a claim about any other file stands by identity, and only claims that rest on those 9 were re-run. That is why this took one claims run, not a re-derivation of the text.
5. **Not ready to send, and not mine to send:** his approval of draft 12 (section 7), and PR5's three go-aheads.

## 2. Section 6's claims, re-run on `47637be2` (clean `--no-local` clones, serial, exits read bare)

| Claim | Re-run | Result (draft 11 on `3cba1e5`, where it differs) |
|---|---|---|
| a legacy project is unchanged in where its files sit | `pr4-fixture.sh` (a): an empty project synced by each tool | the same 30 paths; no `methodology/`; 22 differ in bytes, 22 of 22 are files the branch changes (same as draft 11) |
| no file an adopter owns is overwritten | `pr4-fixture.sh` (b), and PR3's re-run ([`pr3b-record.md`](pr3b-record.md)) | upstream writes 0, the branch 19, 0 of 7 seeds changed, no `--force`; at the 12 real projects 0 seeds changed |
| the resolver is one block, byte-identical | `tools/test_layout_resolver.py` and the 11 copies | 76 tests OK; 11 of 11 equal |
| every frozen proof gives the verdict it gave | each tracked `*.verify.sh`, both tips | 1 at each (`CHANGELOG-through-2026-09-30`), exit 0 at both |
| both layouts' links resolve; no path literal left | `bin/check-links --layout both`; `bin/check-layout-literals` | 80 links in 23 documents in each layout (upstream: 116, `--layout` refused, exit 2); 15 files, 0 sites, 138 acknowledged |
| the gates tighten and none loosens | `compare()` of the branch's own ratchet, each of 33 commits against its parent | 0 refusals, 0 warnings, 0 manifest defects; 12 to 18 gates; five floors raised (**the trimmer's is now 227 to 265**, draft 11 said 124 to 222) |
| the counts in the prose are true | `pr4-body-check.py`; `pr4-distribution.py` (30 rows = 18 + 12, 11 + 7); `pr4b-facts.sh` | all equal the text (section 3 lists the ones that moved) |
| the first commit stands alone | `pr4-first-commit.sh`: `fbcef390` on `d50ce290` | 271 passed, 0 failed, 0 skipped; gates 12/12, results `e658e1a02647` (draft 11's `bbe0dc3`: the same counts) |

The suite and the gates, the question a reader asks first: `bash bin/tests.sh` **302 passed, 0 failed, 0 skipped** (upstream **261 / 0**); `quality_ratchet.py --run` **18/18, 0 fail, 0 unmeasured**, results `8c7362ca5b27`, manifest `72583325c300` (upstream 12/12, results `b49e29a9e5ea`). One serial run of `pr4b-claims.sh`, about 29 minutes, 0 dirty paths in both clones.

## 3. What changed in the text, and why (26 edits)

- **Heading and status paragraph** (above the rule): draft 12, what changed, the budget figure.
- **The numbered items:** #94 and #92 are merged; #98 and #96 are named; the evidence prefixes `pr3b`, `pr4b` explained; the hash sentence names #98's head `65990cd` where it named #94's.
- **Decision 1:** 34 to 33 commits, 19,983 to 18,367 lines; the first commit alone is `fbcef39` (result unchanged).
- **Decision 2:** `bbe0dc3` to `fbcef39` (twice); `cfcc713` to `9848b62`; "All 4 versions of the trimmer in your history" to 17 commits, 1.5.0 to 1.8.2 (upstream's history grew; every one has a `TRIM_VERSION` line).
- **Decision 3:** rewritten for #98 and #96; the counts are `pr4b-claims-output.txt` section 8 (#98: trimmer 3, its tests 1, gates 1; #96: gates 2, `bin/tests.sh` 1).
- **Decision 4:** `ced2c82` to `6ce88cd`; 34 to 33 commits; the reference-removing commits are "seven commits and a tail of three" and "the seven only with `9848b62` rebased" (section 4, item 3).
- **Size:** 18,367 / 1,098; 19 files reach a project with +2,540 / -526; 3 seed sources; 25 stay with +15,820 (86%); the earlier work is 6,883 lines in `fbcef39` and `1d93579`, **37%**, not 42%.
- **Cost:** the 244 B (+0.35%) stands; the timing sentence is rewritten (section 4, item 4).
- **The commit bullets** (replaced as a block): the old `bbe0dc3`, `c8c0b21`, `5afc962`, `3cba1e5` bullets become `fbcef39`, `1d93579`, `d818ca1`, `62680cd`; Test 15's commit is `07ec025`; the whole-file bullet is about the dashboard alone (17 conflict regions in each copy; the trimmer 1 and its tests 1, against draft 11's 51 regions in 8 files).
- **My 12 projects:** `pr3b-adopters.py`; 52 files refused, 51 fork versions and 1 project edit (49 lines), against 39 and 38.
- **Evidence table:** `pr4b-claims.sh`, about 30 minutes; the control column is `d50ce29`; "0 refusals over 33 commits".

- **After the cold read (3 more edits and 3 changed):** the cost sentence about the runner (item 6 below); the `138` named as the scanner's own "acknowledged" count; the migration suite's two classes that `bin/tests.sh` also runs; decision 4's bullet names the seven and the tail and discloses the cherry-pick lines (item 7); decision 3 loses the `merge=union` sentence and the 1.9.1 / 1.10.0 aside; the size paragraph's citation is reworded.

Left as draft 11 had them, on purpose, because the files they rest on are byte-identical: the dashboard items (a) to (e) and the `NEW_LAYOUT` and resolver paragraphs; `bin/migrate-layout` (1,457 lines, 280 tests, 6 minutes, `timeout_seconds` 3600 at both gates, read from `.quality-gates.json` at `47637be2`); the 138 acknowledged lines; the 36 links that became names (116 at upstream's tip and 80 here, both read today); the 7 + 11 + 12 manifest rows; the fixtures, the moved project, the seven-moved-projects sentence (from `pr3b-adopters-output.md`); the Known gaps, which come from the 12 projects and were not re-tested one by one.

## 4. What draft 11 had wrong, or that went stale in a way a number check does not find

1. **Decision 3 asked about a merged pull request.** (Section 1, item 2.)
2. **A citation that did not print the figure.** Draft 11 credited the "42% earlier work" share (8,461 lines) to `pr4-distribution.py`, which prints no such line. The figure is the sum of added lines in two commits; `pr4b-facts.sh` section 3 now prints it (37.5% for the new pair) and reproduces the old 8,461 / 19,983 = 42.3% with the same sum. The text's rule is that every number is printed by a command named beside it; this one was not.
3. **"A separable run."** Draft 11 said that if he keeps the ten reference-removing commits, a merge or a rebase leaves them as a separable run. True of the old branch, where they sat together at the tip. In the rebuilt series they are commits 22 to 28, then `fd43f70` and `9848b62`, then 31 to 33 (`pr4b-facts-output.txt` sections 1 and 2; the order of the grouping plan, which keeps the printed-text commits last so that they can be refused as a tail). `9848b62` and `8c37c28` (the seventh) both edit `tools/test_methodology_dashboard.py`, so the first seven cannot be dropped without rebasing the restore commit. The sentence now says so.
4. **"Within 0.1 s."** Draft 11 said the dashboard, the trimmer's check and the budget tool took the same time as upstream's, within 0.1 s. On the 517-commit project the dashboard takes 0.66 s against upstream's 0.92 s (three alternating rounds each); it was within 0.1 s at 488 commits (0.59 against 0.68). The candidate is quicker, not equal; the sentence says what was measured. I do not know why, and the text does not say.
5. **The instrument has a hole.** `pr4-body-check.py` prints `in upstream..candidate: False` for a hash that is outside the branch and exits 0: it fails only on a hash that does not resolve. Run on draft 11 against the rebuilt branch it printed `False` for all 14 of that text's hashes and exited 0. I read the flags by hand for draft 12 (the four `False` are #98's head, the two fork-`main` hashes and upstream's tip, each named as such in the text). Not changed here; it is a one-line gate if he wants it (section 7).

6. **"The first paragraph of `SESSION_RUNNER.md` changed."** (Draft 11, in decision 1's list of what it costs a project; found by the cold reader, re-run by me.) The paragraph that changed, "Where the files are", is the third (line 7; the title and two paragraphs precede it), and it is new in the sense that upstream has none. The larger cost was left out: the framework documents now name one another by bare name, and `docs/methodology/` is named on 38 lines at upstream's tip and 10 here (the runner 11 to 1, the skills index 14 to 0, `SAFEGUARDS.md` 1 to 0; `pr4b-facts-output.txt` section 9). A legacy project's documents therefore depend on that one paragraph to say where to look. The sentence now says that.
7. **The cherry-pick lines.** 27 of the 33 commits end with `(cherry picked from commit ...)` naming a commit only the fork has (`git cherry-pick -x`; `pr4b-facts-output.txt` section 10). The text promised that references only my fork can resolve were removed and said "some remain"; it did not say these. It now does.

## 5. Expectations, scored (`pr4b-expectations.txt`: twelve saved before the claims run at 18:25:06, four more at 18:55:28 before the other runs)

Confirmed: E1 (47 files, +18,367 / -1,098, 33 commits), E2 (302/0/0), E3 (261/0), E4 (18/18, both ids equal to layer 23's), E5 (12/12), E7 (15 files, 0 sites), E8 (76 OK, 11 of 11), E9 (one proof, exit 0 at both), E10 (0 refusals, five floors, the trimmer's differing), E12 (29 minutes), E13 (271/0/0, 12/12), E15 (fixtures), E16 (moved project). **Half confirmed: E6** (80 links in 23 documents as expected; upstream's own count did not move, against my 55% that it would: 116 in 23) **and E11** (#98: 5 regions in 3 files as expected; #96: 3 regions in 2, not the 4 in 3 I took from the layer-23 record). The #96 miss has a cause I can name: layer 23's tool counts as GitHub does, with no `merge=union`, which adds a `CHANGELOG.md` region that upstream's tip and #96 produce alone (`pr4b-facts-output.txt` section 8); I took the number without reading how it counted. **E14:** the 244 B held (95%), the timing did not (60%: the dashboard on the larger project is 0.26 s quicker, section 4, item 4). Two premises I tested first (P1: upstream moved 8 files; P2: gates 12 at both tips) held.

## 6. How the instruments were checked, and what went wrong

- **No pilot of `pr4b-claims.sh`:** it is `pr4-claims.sh` with three lines changed (`diff pr4-claims.sh pr4b-claims.sh`: the two heads and the label of section 8), and its sections 1 to 7 ran as they ran for draft 11. A pilot would have shown nothing the diff does not.
- **`pr4b-facts.sh` had two faulty lines when first written** (a redirect that starved a pipe in section 6, and a malformed range in section 7); I read it back and fixed both before its first run. Its first run's output was then read in full, not sampled.
- **Two slips of mine, both cleaned:** an `echo` with `old->new` in it created a stray file named `new` in the evidence directory (found by `git status`, deleted; it was mine, 35 bytes), and importing the builder to measure each edit's byte effect left a `__pycache__`.
- **One mistake of mine in the ledger, caught before the commit:** the first evidence entry said "eleven confirmed or half-confirmed, two misses"; the count is ten and two (section 5).
- **The builder refuses** unless the file is draft 11 and every text occurs exactly once; the first dry run applied all 21 edits, the body then came to 21,856 B and was cut to 21,484 B; the decision-4 and cost corrections raised it to 21,612 B (the frozen draft) and the cold read's fixes to 21,802 B; text was cut only where another sentence states the same thing (the duplicate trimmer sentences in two bullets), except that #96 is now named without a description of it, as one of the maintainer's own open pull requests.

## 7. The cold read, and his calls

**The read.** One fresh agent (the read-only `Plan` agent type, 444 s, 45 tool calls), on the frozen blob `357ae739`, briefed with the maintainer's vocabulary, the cost first, and a ban on reading anything under `docs/planning/`. It scored the text **6 of 10**. Its report is claims, and each factual one below was re-run by me before I acted. **Its discipline slipped twice**, both disclosed by the agent: it ran `git merge-tree --write-tree` twice (my brief listed no merge command; this adds unreferenced objects to `.git/objects` and nothing to the working tree), and one Bash call with a redirect to `/tmp` was denied before it ran. After the read `git status` showed only my own untracked record and `/tmp/__x` did not exist. The read-only agent type has Bash, so a brief is not a barrier.

| Finding (the agent's words, shortened) | I re-ran it | What I did |
|---|---|---|
| "first paragraph ... changed" is wrong and understates the cost | confirmed: third paragraph; 38 to 10 lines naming `docs/methodology/` | sentence rewritten (section 4, item 6) |
| the evidence link's scripts are not on the fork's pushed `main` | confirmed: `pr4b-claims.sh`, `pr4b-facts.sh` and this record are not on `origin/main`; the six older cited scripts are; 7 commits of `main` are unpushed | not a text edit: the push is PR5's first step; his call 3 |
| "138 lines" cannot be reproduced by grep (238, or ~148 once duplicates go) | the scanner prints 138 "acknowledged" (my claims run); the agent's grep counts the dashboard's twin and the tests | wording: the scanner's own count |
| versions: the dashboard's 2.22.0 and the ratchet's 1.3.0 are not named | the dashboard's 2.22.0 is true (the cost run prints it); the ratchet's versions I did not verify | none: no sentence is false; the text names the versions of the commits it describes |
| "Counted in a checkout, where `merge=union` applies" is unexplained | its test used `.quality-gates.json`, which the rule does not cover; its counts equal mine | sentence removed |
| the cherry-pick lines and other leftovers are not mentioned | 27 of 33 confirmed; the leftover names (`BL97-SITE`, `S13`, `BL-27`) I did not check one by one (layer 23's record counts 17 lines in 5 files) | disclosed in decision 4 (item 7); stripping them is his call 2 |
| "280 tests (separate from `bin/tests.sh`)" is slightly off | confirmed: `bin/tests.sh:326` runs two classes, 95 tests | wording |
| undefined words: "tail of three", "them", the cryptic citation | confirmed in the text | decision 4 names the seven and the tail, "these commits"; the citation reworded |
| undefined words: "the foundation", "the densest content measured", "decision 4" cross-references, "my own 12 projects" | they are draft 11's approved words, and each is defined or has a local meaning in the text | none |
| decision 1 bundles the tool and has no "directory without the tool" option | true of the structure | none: it is his call 5 |
| cut: decision 3's mechanics, the 12-projects paragraph, the whole-file paragraph, 2(d)'s thresholds | a judgment | partly (the 1.9.1 / 1.10.0 aside went); the rest is his call 4 |

**What the read does not settle:** it checked 12 or more claims by sampling; the timings, `271 passed`, the 49 lines, the 17 conflict regions and the 80-links figure it could not check cheaply (the first and last two are from my clean-clone runs). It is one agent's read, not the maintainer's.

**His calls, in the order I would ask them:**
1. **Approve draft 12**, change it, or hold it. The approved text was draft 11; this one differs in the places section 3 lists and is shown to him in the close-out report.
2. **The cherry-pick lines:** leave them and say so (draft 12 does), or rewrite the 27 messages (every hash changes and the layers need a fresh verification run). I recommend leaving them.
3. **The fork's `main` must be pushed before the pull request is opened,** or the text's links to `pr4b-claims.sh` and `pr4b-facts.sh` read 404. It is part of PR5's first go-ahead (push to the fork's `origin`), not done here.
4. **Length:** 21,802 B against the 20,000 B he set, 316 B above draft 11. The reader's cut list is above; I cut nothing he approved.
5. **Whether decision 1 should offer the migration tool as its own pull request** (the text offers only the first commit alone).
6. **Still open from S396:** whether the text should say how it expects the 33 commits to be merged (a squash can only raise the 52); the trimmer's version number (1.9.0 here; #98 uses 1.9.0 to 1.10.0), settled at PR5; the wsfct sync; #96's rebase; the three adopter ledgers; BL-92 (c) with BL-103 (c); BL-55's adopter-facing half; BL-110; BL-102; BL-94's third run; BL-127 (b) and (c); BL-114.
7. **`pr4-body-check.py` should fail on a branch hash outside `upstream..candidate`** (section 4, item 5); it needs an allowlist for the four hashes that are not the branch's. Not done; a small change when he wants it.

## 8. Files

Here: `pr4b-expectations.txt`, `pr4b-claims.sh` and `pr4b-claims-output.txt`, `pr4b-facts.sh` and `pr4b-facts-output.txt`, `pr4b-up-links-output.txt`, `pr4b-mergefile-output.txt`, `pr4b-distribution-output.txt`, `pr4b-first-commit-output.txt`, `pr4b-cost-output.txt`, `pr4b-fixture-output.txt`, `pr4b-moved-output.txt`, `pr4b-body-check-output.txt`, `pr4b-draft12-build.py`, this record. Re-run: `bash docs/planning/pr-composition-evidence/pr4b-claims.sh <repo> 47637be21425 d50ce290d921 <work-dir>` (about 30 minutes; `nohup`, wait for `pr4-claims done`); `bash docs/planning/pr-composition-evidence/pr4b-facts.sh d50ce290d921 47637be21425 pr2/candidate 65990cda6afd ad5c980f3457` (seconds); `python3 docs/planning/pr-composition-evidence/pr4-body-check.py docs/planning/upstream-pr-body.md 47637be21425 d50ce290d921`.
