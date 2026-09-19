# BL-57 — one set of `CHANGELOG.md` rules, kept in one place

**Status:** APPROVED by the operator at S162 and committed (`9292132e`, 2026-09-15); amended at S163,
S167 and S168 (see **Trees**). **P1–P4 are done** on branch `bl57/changelog-rules` (S167, S168, S172, S173; all four
backed up to `origin` at `83a12f0`). **P5 is done at S178, by merge (see the S178 block)**, and BL-54, which came
before P6, was fixed fork-side at S179 (`2c4f801`). **P6 (`airqino`) is done in that repository, recorded here at S180
(see the P6 block), and P7 (`wsfct`) is done in that repository and MERGED to its default branch, recorded here at
S185 (see the P7 block), and P8 (`vscode_quarto_ext`) is done in that repository, recorded here at S191 (see the P8
block)**, and P9 (`mts-system`) is done there, recorded here at S193 (see the P9 block), and P10 (`nprcgenekeepr`) is
done there, recorded here at S194 (see the P10 block); P11 is not. **Item (18) was decided by the operator at S181: one `bin/sync` run is one
commit. Item (21) was decided by the operator at S186: P8–P11 also migrate a stale `HANDOFFS.md` seed. Item (22) was
done at S187, on the branch (`100f09b`) and merged into fork `main` (`2d5ce70`). At S188 the operator put the
three fixes P12 carries (F5, BL-62, BL-63) on the branch before P12, and chose P12's merge (item (23)); all three are
on the branch (`657acb7`, `5223afb`, `0d63410`) and merged into fork `main` (`5f5a400`). **P12 is done at S189: [PR #84](https://github.com/KJ5HST/methodology/pull/84) is OPEN, head `20db3f0` (item (24)). At S190 the branch's last eight commits were merged into fork `main` (`2410657`). P8 is done (S191). BL-72, the
`bin/check-handoff` fence fix the operator put before P9 (S191), is done at S192: on the branch (`77afc12`, riding PR #84,
the operator's choice) and merged into fork `main` (`ea1a057`). P9 (`mts-system`) is done in that repository, recorded
here at S193 (the P9 block), with one remainder there (item (28)). PR #84's description names the fix since S193. P10
(`nprcgenekeepr`) was decided by the operator at S194 (force the sync, then re-apply its trimmer extension), done in that
repository from S194's launch prompt, and recorded here at S194 (the P10 block). P11 is next.**
**Workstream:** [`ARCHITECTURE_WORKSTREAM.md`](../../workstreams/ARCHITECTURE_WORKSTREAM.md) (a migration
plan), under [`SESSION_RUNNER.md` §Planning Sessions](../../starter-kit/SESSION_RUNNER.md).
**Source:** [BL-57](BACKLOG-DETAIL.md#bl-57), raised 2026-09-14 on the operator's request, high priority.
**Decided:** Q1–Q4, by the operator at S162 (§2.1). **Recommended, approved with the plan:** D5–D10 (§2.2).
**Reviewed:** an independent read-only review at S162 found four errors, nine risks and six nits in the
first draft. Each was reproduced before it was fixed here; about 90 citations and 30 numbers were
confirmed.
**Trees:** the upstream work targets `KJ5HST/methodology:read-set-budgets` at **`b82dcff`** (PR #80's
head); fork `main` at **`7ea7346b`**; six adopters under `~/Development/`. Every line number is
`b82dcff`'s unless marked *fork*.
**Amended at S163 (2026-09-15):** the maintainer's #80 review (F1, option (a)) cuts the branch's
`starter-kit/FRAMEWORK_LEARNINGS.md` to rows 1–13 plus the reserved `#14` — local branch
`pr80/f1-learnings-1-13`, commits `5c9f0f3` and `d4e15706`, not pushed when this was written. Once
pushed, #80's head moves past `b82dcff`, so P1 starts from the new head (hazard 1), and **no row past
#13 exists upstream**: a fork learning reaches an upstream file only as its rule, stated inline, never
as a number (P1 step 5). §1.1's C5 and §7's *Keep keying on the titles* row describe `b82dcff` itself.
**Amended at S167 (2026-09-15):** P1 ran from #80's head `aa36fd8b` — `eb06625b`, `b0634606`, `2d5dc6e9`,
`77b21a20` on `bl57/changelog-rules`, worktree `../methodology-bl57`, not pushed. **#80 merged the same
day** (`4d9e2715`; `upstream/main` `8b4dc2c3`), so D5's route is open and `aa36fd8b` is an ancestor of
`upstream/main`: P2 starts by merging `upstream/main` into the branch (`git merge-tree` clean at S167),
which also brings upstream's new `.githooks/commit-msg`. What P1 found, for P2–P4:
(1) `.context-budget.json` pins upstream `CLAUDE.md`'s ceiling at its size, 59,168 B, so K2 covers
`CLAUDE.md` too — every edit to it is net ≤ 0. P1's step-4 row first went 116 B over while all four suites
stayed green: none runs `context_budget.py --status` on the tree, so §9.7 is the only check that sees it.
Run it at every boundary, on the branch and on its merge. (2) §9.4's command as first published printed
nothing in zsh — `"$c:starter-kit/…"` is a history modifier (hazard 13); corrected below. (3) The frozen
pre-P1 seed is one file, `tools/fixtures/seed-CHANGELOG-ledger-format-1.md`, read by the trimmer's
controls and by Test 20 (b2), with its blob id `47bc8485` asserted — not two literals. (4) A third index of
the apparatus, `ITERATIVE_METHODOLOGY.md` §Reference Apparatus, listed six sections; step 4 updated it with
the plan's two. (5) The marker line reads `ledger-format: 2 — keep this marker; bin/status reads it.`
**Amended at S168 (2026-09-15):** P2 ran after `upstream/main` was merged into the branch (`9e1dfeb`,
clean; `bin/tests.sh` 118/0 before and after, 0 flips): `f2bcc22` (the home, step 1) and `775ba238` (the
`HANDOFFS.md` seed and the trimmer's comment, steps 2–3), not pushed. **Step 4 needed no commit:** #80's
F3 had already moved both ledgers out of upstream's root `.context-budget.json` into
`_deliberate_exclusions` (checked on `upstream/main`), so D8 is now (i) alone, in P4. What P2 found, for
P3–P5: (1) The home's shard enumeration now reads `cat CHANGELOG.md $(git ls-files
'docs/archive/CHANGELOG-*.md')`, equal in bash, zsh and a Python count with no shard (55) and eleven
(526). **The `HANDOFFS.md` seed's matching bullet still publishes the bare glob** `HANDOFFS.md
docs/archive/HANDOFFS-*.md`, which zsh refuses where no shard exists — C10's class, outside P2's lines;
P3 takes it with the audit. (2) After the merge, `upstream/main`'s own entries sit at the top of the
branch's ledger, then BL-57's, then #80's; a new branch entry goes above BL-57's block, below `main`'s.
(3) Upstream's `.githooks/commit-msg` refuses an agent-driven commit that lacks a `Co-Authored-By`
trailer, a merge commit included. (4) `HOW_TO_USE.md:748` gives the apparatus as *"~515 lines"*; it is
501 after P2. P4 edits that file and re-measures. (5) §9.1 still reproduces 1,577 lines on `b82dcff`; the
branch reads 1,616 after the merge and 1,611 after P2.

**Amended at S172 (2026-09-16):** P3 ran on the branch as it stood — upstream PR #82 was re-checked at
Phase 0 and is still OPEN at `c84e7d96`, so S169's merge-first amendment did not trigger. Commits
`d771439` (the home), `e47ca14` (the runner, the flight manual, the hook) and `cf20a3b` (the
`HANDOFFS.md` seed's bare glob, carried from P2), not pushed. **S169's amendment is discharged above:**
P3's and P4's runner criteria are now in tokens, against a measurement taken this session in which both
published controls reproduced exactly (the runner doubled to 36,955, the pair to 48,555). What P3 found,
for P4–P5:
(1) **The two units disagree about a cross-reference.** Replacing the runner's inline audit grep with a
link, plus the two id changes, measured **+36 B but only +9 tokens** — about 4 B/token for a path against
the file's 2.8248 average. Cutting two duplicate clauses on the same step then took the file to
**52,163 B / 18,463.5 tokens**, under its start in both units. A byte rule overstates what a
cross-reference costs and understates what cut prose saves.
(2) **§4.4's adopter figures re-derived: four of six reproduce exactly** (`model_project_constructor`
0→0, `nprcgenekeepr` 599→784, `vscode_quarto_ext` 236→247, `wsfct` 130→130). Two moved by exactly +1,
each explained by one entry dated 2026-09-15: `airqino` 1→2 and `mts-system` 96→262. The widened id
pattern recovers **362 logged actions** across three adopters that `BL-[0-9]+` could not see; one of them
tags with `BL-OPS-ADMIN-PW-RECOVERY-001`, which is the case Q3 A exists for.
(3) **This repo's audit reads 556, not §4.4's 494 — and 494 is exactly the count of entries dated on or
before 2026-09-14**, §4.4's measurement date. The difference is 55 entries logged on 2026-09-15 and 7 on
2026-09-16. S171's trim wrote a 12th shard and moved no entry out of the audit's reach, because the audit
sums the live file and its shards: conservation holds, measured rather than assumed.
(4) **P4 inherits a vocabulary item its scope does not name.** The last live `[BL-<N>]` outside frozen
history is in the branch's root `CHANGELOG.md` front matter, in its own tag-definition list — upstream's
front matter has grown past `b82dcff`, where P4 step 5's `:14` was the inline audit grep, not a
definition list. Treat the tag definitions there as their own item.
(5) **`python3 starter-kit/context_budget.py --status` leaves an untracked `.context-budget-history.jsonl`
in an upstream tree** — upstream neither tracks nor ignores it, where fork `main` tracks it. Delete it
after measuring, or the next Phase 0 finds a dirty worktree.
(6) `bin/check-links` moved 107 → 108, the one link P3 added; `bin/tests.sh` is 118 passed / 0 failed
before and after, in a clone whose HEAD sha was asserted equal to the worktree's.

**Amended at S173 (2026-09-16), before any P4 edit:** **upstream PR #82 merged** (`64f23bf`, 18:05:47 UTC),
so S169's merge-first amendment triggered and P4 began by merging `upstream/main` into the branch —
`52ad407`, two one-line conflicts, both predicted by `git merge-tree` (`CLAUDE.md`'s *Reference apparatus*
row; `ITERATIVE_METHODOLOGY.md` Phase 6 step 8, upstream's new step (c) kept with P3's `[BL-<id>]`).
**P4's size criterion is restated below on the new base,** because `c0550acd` is no longer upstream's
runner and #82 gave upstream's root `.context-budget.json` token ceilings of its own. What the restatement
rests on:
(1) **Every figure is a doubled-file read, and the instrument was checked first.** Two recorded controls
reproduced exactly — 36,955 on `c0550acd`, and 37,731 on `64f23bf`'s runner blob `2a3e410d`, which is the
figure upstream's config records for that blob. `CLAUDE.md`'s blob `1244e95b` reproduced upstream's
recorded 46,965. **The instrument's behaviour changed:** the Read no longer refuses a file over 25,000
tokens; it returns a 25,000-token first page and prints the whole-file count in its truncation notice. A
spanning `limit` prints no count. So each reading costs a full page of context — take them in a subagent
that reproduces a control in the same run, and copy the notice verbatim.
(2) **P3's saving survived the merge exactly.** The merged runner reads 37,703 (18,851.5 tokens), 14 under
`upstream/main`'s 18,865.5 — the same 14 P3 measured against `c0550acd`.
(3) **The merge is 4 tokens OVER `CLAUDE.md`'s token ceiling.** It reads 46,973 (23,486.5 tokens) against
upstream's 46,965 (23,482.5) and a `max_tokens` of 23,483. The only difference is the one row carrying
P1's wording — *"and the `CHANGELOG.md` rules"* for *"extracted so the manual fits one read"*: **9 B
shorter and 4 tokens longer.** `context_budget.py` cannot see it, because it prices the file at upstream's
measured 2.519 B/token and so counts 59,144 B as 23,479. P4 edits `CLAUDE.md` anyway (step 4) and pays
the 4 back there.
(4) **`starter-kit/SAFEGUARDS.md` is blob `933816b4` on the merge and on `upstream/main`** — unchanged by
identity, so no reading is owed.
(5) **Both trees' gates, in `--no-local` clones with HEAD asserted.** `upstream/main`: `bin/tests.sh` 139
passed / 0 failed; `quality_ratchet.py --run` 10/10, results `15c73dda424f`; `bin/check-links` 107;
`context_budget.py --status` exit 0. The merge `52ad407`: 141 / 0; 10/10, results `c5fca86e4674`; 110 links
(the 3 P1–P3 added); exit 0, and a row-by-row diff against upstream's output shows only sizes — no status
flips, read-set total 70,244 B against 70,276 B.

**P4 done at S173:** `0c20022` (§The Action Ledger's *Lifecycle* and *Placement*), `f235db3` (*prepend* at
seven sites; the claim commit's *(in progress)* entry), `836e0d2` (*action ledger* for *completed work
history*; `CLAUDE.md` back under its ceiling), `83a12f0` (upstream's root `CHANGELOG.md` front matter, D8 i).
Not pushed. What P4 found, for P5–P12:
(6) **Against the restated criterion:** the runner reads **37,717** doubled (18,858.5 tokens; ≤ 37,731, 7
over P4's start); `CLAUDE.md` **46,953** (23,476.5; ≤ 46,965, 6 under upstream); `SAFEGUARDS.md` is
`933816b4`. Each file was `cmp`-verified against the committed blob doubled, and each reading ran beside a
reproduced control. `ITERATIVE_METHODOLOGY.md` grew 45 B against the plan's *"byte-neutral wording"*; the
file has no budget row on this tree.
(7) **The plan's P4 line numbers were `b82dcff`'s and three had moved:** runner :278/:329/:357 are
:281/:332/:360, and the hook's refusal text is `.githooks/pre-commit:70` (#82 added lines above it). The
rest held. P5 re-locates every site on fork `main` by grep.
(8) **`README.md:96` carried the same completed-work instruction as `starter-kit/BOOTSTRAP.md:139`**
(*"When you complete work, remove it from `BACKLOG.md` and add an entry"*), inside a line the plan names
for its phrase only. P4 changed both. Grep for the sentence, not only the phrase, in P5 and the adopters.
(9) **P5'S PORT, AS WRITTEN, IS NOW A FORK RESYNC.** `git diff b82dcff bl57/changelog-rules` (ledgers and
budget excluded) is **34 files, +3,015/−358**: it carries #80's review fixes and #82's quality ratchet as
well as BL-57. BL-57's own net change on current upstream, `git diff 64f23bf bl57/changelog-rules` with the
same exclusions, is **16 files, +532/−252**. Fork `main` is **53 commits behind `upstream/main`**, and
`git merge-tree` of the two conflicts in 12 files. So P5 starts with a choice that is the operator's: port
from `64f23bf` (BL-57 only, onto a `main` that lacks #82), or resync fork `main` with `upstream/main` first
(its own go-ahead) and then port. P5's *"494"* audit figure is also stale: the audit read 556 at S172.
**DECIDED by the operator after S173's close-out (picker, 2026-09-16): resync fork `main` with
`upstream/main` first, then port BL-57's own change from `64f23bf`** — and S174 takes the `HANDOFFS.md`
header cut before either, because the trim S175's Phase 0 calls needs it.
(10) **For P12: the branch's `.context-budget.json` density notes name blobs the branch no longer has.**
Upstream's own rule is to re-measure when `HEAD:starter-kit/SESSION_RUNNER.md` stops reading `2a3e410d`
(it now reads `4811f02f`) and `CLAUDE.md` stops reading `1244e95b`. The PR re-measures both on its final
blobs and updates `bytes_per_token`/`measured_bytes`. `context_budget.py` prices a file at its recorded
density, so a wording change can pass it while crossing the real ceiling: P1's row did, by 4 tokens.
(11) **P12 also carries #80's review item F5, by operator decision (S173, picker):** correct
`starter-kit/methodology_trim.py`'s false claims — `:33` says the ledger hook runs `--no-renames` (upstream's
hook has 0), and `:9`/`:155` cite `docs/planning/ledger-trimmer-design.md`, which upstream lacks — on the
branch before P12, since BL-57 already edits that file. Detail: `docs/planning/pr80-review-response.md` §6.

**P5 done at S178 (2026-09-16), by merge. The operator chose a merge over §P5's port, so the branch's
commits are in fork history, and chose D10 as written.** Commits: `22ce71b` (the merge: 5 conflicts, 9 hunks;
`CHANGELOG.md` ours, `bin/_manifest.py` and `bin/tests.sh` theirs, `CLAUDE.md` and the runner combined),
`6774627` (a fork-only test), `1664860` (D10), `dee680c` (this repo's two ledgers), `fd611a6` (two fork-only
sentences), `368b29c` (`tests-sh-passed` 327 → 294, operator-approved) and `d10f9af` (a tightening). What P5
found, for BL-54 and P6–P12:
(12) **THE MERGE MAKES BL-54 BITE.** Git's default history walk follows a merge's same-content parent. After
`22ce71b`, `git log -- starter-kit/methodology_trim.py` visits 3 commits where it visited 14, so `bin/status`
reads the trimmer as *locally modified* in the `mts-system`, `vscode_quarto_ext` and `wsfct` copies (each
read *N versions behind* before). Adding `--full-history` at `bin/status:56` restored every row on the same
copies. It also cleared the 4 `FRAMEWORK_LEARNINGS.md` rows the resync merges had already turned; the
genuine local changes in `model_project_constructor` and `nprcgenekeepr` stay. **So P5's DONE item
*"tracked files read as before, or upgradable"* is not met for those 3 rows. BL-54 is next, before P6
(operator, S178).** `bin/sync` refuses a locally modified file, so no adopter syncs from fork `main` until
then. The other DONE items hold. The five distributed files that were identical between `main` and `64f23bf`
equal the branch's blobs. The audit reads the same in zsh and bash, and its old form matched the new (635 at
Phase 0, not the 494 written above). A claim-only commit is refused in a scratch repository. All six adopter
copies read `CHANGELOG.md` *present (stale format)*. The suite reads 294 passed / 0 failed at two receipts.
(13) **A fork-only test pinned the old seed** (hazard 6, in a test the branch never had): `tools/test_methodology_dashboard.py`
`test_fenced_records_are_not_counted` now reads the frozen format-1 seed. It is fork-only; P12 carries nothing for it.
(14) **D10 makes item (11)'s F5 claim false on fork `main` too.** Neither hook has `--no-renames` now, and
`starter-kit/methodology_trim.py:33` still says it does. F5's fix on the branch reaches fork `main` by the next merge.
(15) **Found, not fixed:** `README.md`'s fork-only cost section (`:374`–`:404`, S42's 2026-08-04 measurements)
still describes a 2,000-line cap and the old seed sizes. It needs its own rewrite, which no phase here covers.

**P6 done (2026-09-17) in `airqino`'s own repository, its Session 6; recorded here at S180.** Local branch
`chore/methodology-bl57-p6`, taken from `1402ad4`, not pushed: `2b0230a` (claim), `28022fe` (the sync from fork `main`
`ff02b5c`: 14 files plus its entry), `5e4b483` (the header), `9f150a5` (`CLAUDE.md`'s ledger wording), `e947798`
(close-out). DONE, as that session reported and as re-run from here: `bin/status` reads `CHANGELOG.md` `present` from
the branch `83a12f0`, from `upstream/main` `6b29d3d` and from fork `main` `ff02b5c`; `5e4b483` removes only lines 1–11
(§9.8); the heading count and the audit each went 4 → 5, the block holding neither. BL-56 is closed. What P6 found,
for P7–P11:
(16) **P6's row gave a reason S179 had already made false.** It chose Route A because BL-54 refused four files from
fork `main`. After `2c4f801` the dry run from fork `main` exited 0 with no refusals, so P6 took Route B. P7–P9 already
name Route B. Re-run at S180 from fork `main` (`b5a422b`), read-only: `wsfct`, `vscode_quarto_ext` and `mts-system`
exit 0 with no refusals; `nprcgenekeepr` (P10) and `model_project_constructor` (P11) exit 2, refusing only the genuine
local edits (the first's `methodology_trim.py`, the second's `SESSION_RUNNER.md` and `SAFEGUARDS.md`).
(17) **A row's fixed figures go stale before its phase runs.** The row said *one entry*; there were two, because
`airqino`'s own Session 5 had added one. The DONE counts are deltas across the migration commit, so they held, but
§4.4's figures for P7–P11 (measured 2026-09-14) need re-deriving at each claim. `airqino` dropped `## [Unreleased]`
rather than converting it, and opens its first `## YYYY-MM` at its next new month: a precedent for P8's
Keep-a-Changelog header.
(18) **A sync is one tool run that writes more than five files.** `28022fe` holds 15. `SAFEGUARDS.md` caps a commit
at five; that session disclosed the breach without asking first, and `airqino`'s previous sync, `dfe26fd`, held 21.
P7–P11 each meet the same cap (the S180 dry runs would write 14 files in `wsfct`, 14 in `vscode_quarto_ext`, 16 in
`mts-system`), so it is one decision for the operator, best taken before P7: split a sync's files
across commits of five, or treat one `bin/sync` run as one commit.

**Item (18) decided at S181 (2026-09-17), by the operator (picker): one `bin/sync` run is one commit.** It binds
P7–P11 and is written into step 2 below. That commit holds exactly the files the run wrote, as its dry run listed
them, plus the commit's own `CHANGELOG.md` entry, and nothing else. The header migration and the `CLAUDE.md` wording
stay in their own commits under the cap, as P6 kept them (`airqino` `5e4b483`, `9f150a5`). The entry states the file
count and cites this item. **Why the exception holds here:** every file is a byte-for-byte copy of a fork `main`
blob, the dry run lists them before anything is written, and one `git revert` undoes them all, which is the
recoverability the cap exists for. Splitting would leave commits where the new `SESSION_RUNNER.md` and
`SAFEGUARDS.md` cite `quality_ratchet.py` and `.quality-gates.json` before the commit that adds them (checked in
`wsfct` at S181: its copies mention neither, and neither file exists). `airqino`'s `28022fe` already fits: the 14
synced files and its entry. **Not decided here:** whether the distributed `SAFEGUARDS.md` (the same on
`upstream/main`) or `BOOTSTRAP.md` should say so for every adopter. That is BL-63, for the upstream PR.

**P7 done (2026-09-17) in `wsfct`'s own repository, its Session 630, and MERGED there; recorded here at S185.** Six
commits on `chore/s630-methodology-bl57-p7`: `790c77d1` (claim), `8a41741c` (the sync from fork `main` `29b0feb`: 14
files plus its entry, 15 in all — item (18) applied), `12fb758e` (the header), `8d0e696a` (`CLAUDE.md`'s ledger
wording), `6891645c` (its own learnings row and pointer), `3a257097` (close-out). **PR #903 squash-merged them to
`master` as `66e14daa` at 2026-09-18T00:36Z.** `wsfct` deletes a branch when its PR merges, so the branch is gone from
GitHub; the six commits survive at **`refs/pull/903/head`** (`3a257097`). DONE, re-run read-only from here at S185 from
git objects alone, with `wsfct`'s `git status --porcelain` empty before and after: `bin/status ../wsfct` reads
`CHANGELOG.md` `present`; §9.8 on `12fb758e` prints *only the block changed* for 8–182 — line 8 modified, lines 10–181
replaced by the thin header, and one pure insertion after old line 198, its own entry; `grep -c '^### '` went 75 → 71,
the migration's 1 entry minus the block's 5 `### ` lines; the audit went 72 → 70 over the live file and 132 → 130 over
the live file and its three shards (§9.2's form), the block's 3 matching examples out and that 1 entry in;
`bin/sync ../wsfct --source=local --dry-run` exits 0 with 23 files unchanged; and `git diff 3a257097 66e14daa` is
empty, so the squash preserved the branch tree exactly. The build item rests on S630's receipt (no `web/` code
touched) and was not re-run from here. What P7 found, for P8–P11:
(19) **The row's block range was stale before the phase ran, and following it would have lost records.** This row
said `CHANGELOG.md:13`–`196`; S630 re-measured the block by content at its claim and migrated 8–182. By its own
receipt, 13–196 would have deleted the three archive-pointer blocks below the header, and §9.8 fails against it,
naming `(8, 1), (10, 172)`. So **re-derive the block at the claim, by content, and record the range in the migration
commit** — item (17) generalized from a count to the block boundary itself.
(20) **An adopter that merges through pull requests can squash, and then item (18)'s shape survives only on the PR's
head ref.** `wsfct`'s `master` carries the whole phase as the one commit `66e14daa`; the one-run-one-commit history is
at `refs/pull/903/head`. A branch name is not a durable citation there: the recording first written for this block
(`a6320ae`, reverted at `61eb9ab`) cited `origin/chore/s630-methodology-bl57-p7` as still carrying the six, and it was
already gone — GitHub deleted it at 00:36:55Z, two seconds after the merge, eight minutes before that text was
committed. What resolved was `wsfct`'s local remote-tracking ref, which git keeps until a pruning fetch (fork
Learning #77). P8–P11 in PR-merging projects should cite the merge commit and `refs/pull/<N>/head`, and ask the
remote (`git ls-remote`) rather than `git branch -a`.
(21) **The phase migrates one seed and leaves its neighbour, and `bin/status` keeps saying so.** After P7, `wsfct`
reads `CHANGELOG.md` `present` and `HANDOFFS.md` *present (stale format)*. Measured across all six adopters, the same
at S184 and at S185: `airqino` both `present`; `wsfct` `CHANGELOG.md` `present`, `HANDOFFS.md` stale; `vscode_quarto_ext`
and `mts-system` both stale; `nprcgenekeepr` `CHANGELOG.md` stale, `HANDOFFS.md` `present`; `model_project_constructor`
`CHANGELOG.md` stale, `HANDOFFS.md` absent. BL-56 explicitly put the other projects' *(stale format)* verdicts —
`CHANGELOG.md` and `HANDOFFS.md` alike — outside its scope ([`BACKLOG-DETAIL.md`](BACKLOG-DETAIL.md) §BL-56), and
this plan's DONE list checks `CHANGELOG.md` only, so **no item owns the `HANDOFFS.md` seed today**. Whether P8–P11
should carry it, or it becomes its own item, is the operator's call — it is not silently in scope.
**Decided by the operator at S186 (picker): P8–P11 carry it.** Where step 1's `bin/status` reads `HANDOFFS.md`
*present (stale format)*, the phase migrates that seed too, the way `starter-kit/BOOTSTRAP.md:386` says: bring the
current seed's `## Size, and when to archive` section in above the first receipt, and leave every receipt
byte-identical (step 3's bullet, and a DONE item). Not the *replace* route `bin/status`'s note gives — item (22). Re-read at S186 with `bin/status <project> --source=local` from fork `main` `fbc1aaf` — readings with a
time on them (fork Learning #74), the same as S184's and S185's: **P8 `vscode_quarto_ext` and P9 `mts-system` are
stale, so in scope; P10 `nprcgenekeepr` reads `present`, nothing to do; P11 `model_project_constructor` has no
`HANDOFFS.md`, so nothing to migrate** — `bin/sync` writes a seed only when it is absent (`bin/sync:235`), so P11's
step-2 sync creates the current one if its dry run lists it. **Outside the decision:** `wsfct`'s `HANDOFFS.md`, still
stale; P7 is done and the answer named P8–P11.
(22) **Found at S186, for P12: two fork-side instructions disagree on how to migrate a stale `HANDOFFS.md` seed.**
`bin/status:231`–`236`'s note, written by P1 (`2d5dc6e`), tells an adopter holding either stale seed to *replace the
text above the first entry (or receipt) with the current starter-kit seed's*; `starter-kit/BOOTSTRAP.md:384`–`386` says
that for `CHANGELOG.md` only, and for `HANDOFFS.md` *bring across the `## Size, and when to archive` section* — the
heading `bin/status` keys on (`bin/_manifest.py:117`). Neither text is on `upstream/main`; both would ship in P12's
PR. Followed literally in `vscode_quarto_ext`, the note would delete the trimmer's pointer block and its *"currently
holds"* count sentence, the regenerated field the seed lacks (BL-48). S186 wrote the replace route into step 3
first, and corrected it before close-out. **P8–P11 follow `BOOTSTRAP.md`; align the note before P12.**
**DONE at S187, by the plan's route for a fix P12 ships (items (11), (14); operator, picker): a commit on the
branch, merged into fork `main`.** `100f09b` on `bl57/changelog-rules`: the note gives each flagged seed its own
route (`bin/status` `MIGRATION_ROUTES`) — for `CHANGELOG.md` replace the header, for `HANDOFFS.md` bring across
the section above the first receipt and keep the rest of the front matter — and the paragraph it cites
(`starter-kit/BOOTSTRAP.md:85` on the branch, `:86` here) now names a stale `HANDOFFS.md` and its route.
`bin/tests.sh` Test 20 (g) pins both with eight assertions: run alone, 5 failures before the fix and 24/0 after;
two mutants fail it. Branch gate on that tree: `10/10 pass`, `results dd16434fe5f5`, `tests-sh-passed` 149.
Merged as `2d5ce70`, `CHANGELOG.md` the one conflict, resolved ours; the three files' changed lines are identical
to the tested patch. Each of the five adopters' present `BOOTSTRAP.md` copies reads one version further behind
than before the merge, none *locally modified*; `model_project_constructor` has none. **One premise above did not hold:** `BOOTSTRAP.md:384`–`386` is fork-only. It sits in
the *Without `bin/sync`* rules the fork added at S41 (`12463dd`, made per-file at `fd611a6`), which the branch
never had, so it does not ship in P12. On the branch the paragraph the note cites is the only statement of the
migration, which is why that paragraph carries the `HANDOFFS.md` route now.
**Not a P7 effect, recorded so it is not rediscovered:** S630 reported that `wsfct`'s three
`docs/archive/CHANGELOG-*.md.verify.sh` proofs fail. Re-run at S185 in a `--no-local` clone: all three were generated
by `methodology_trim.py` v1.1.2 and fail L1 and L3 (record counts 12/8, 37/35, 29/28), identically at `55c293f7`
before the phase and at `66e14daa` after it. That is BL-36's class — proofs frozen before v1.2.0 fixed Defect A — in
an adopter; BL-36 rides BL-60's design session.

**Decided by the operator at S188 (2026-09-17, picker), before P12.**
(23) **P12's three carried fixes were not on the branch, so they land first, in their own session.** S188 was claimed
for P12 and found only item (22) on `bl57/changelog-rules`: F5 (item (11)), BL-62 and BL-63 were not there. The operator
chose to put all three on the branch in S188, each its own branch commit with its own entry, the branch then merged
into fork `main` as at items (11), (14) and (22), and to leave P12 itself (steps 1–6) to the next session. Three routes
were decided with it. **F5:** `starter-kit/methodology_trim.py` links the design doc's public copy on
`rmsharp/methodology`, pinned to a commit, in place of *"not published to a public remote … no URL on purpose"*
(`:9`–`16`), which stopped being true when fork `main` reached `origin`; and `:33` drops the `--no-renames` claim,
which no hook on either tree makes (the fork's went with D10, `1664860`). Not chosen: publishing the 74 KB design doc
upstream, or removing the file's design citations. **BL-63:** `starter-kit/BOOTSTRAP.md` only says how to commit a
sync run, one run one commit (item (18)'s rule, stated for every adopter); `SAFEGUARDS.md` stays untouched (K2), not
both. **P12 step 2: merge** `upstream/main` into the branch, as `9e1dfeb` and `52ad407` did, so the commits already on
`origin` keep their hashes; not a rebase.
**BL-63's route amended the same session (operator, third picker):** `SAFEGUARDS.md` opens *"When this file and other
guidance conflict, this file wins"* and lists the cap under *Hard Rules (No Exceptions)*, so a `BOOTSTRAP.md`-only
exception would have shipped a new contradiction; the recommendation that led to *BOOTSTRAP only* had missed that. The
cap's row now names the case in one sentence linking `BOOTSTRAP.md`, and the how-to stays in `BOOTSTRAP.md`. **K2 is
amended for this one sentence:** `SAFEGUARDS.md` 17,024 → 17,129 B, about 6,067 tokens at its recorded 2.8234 B/token
against upstream's 6,100 `max_tokens` (the read-set partition 18,900 + 6,100 unchanged). On fork `main` it adds 105 B to a
file already over the fork's own 15,386 B ceiling. It is its own commit, so the PR can drop it.
**DONE at S188.** On `bl57/changelog-rules`, each with its own branch entry: `657acb7` (F5; comments only, the link
pinned to `979dc73`, which resolves on GitHub at the blob fork `main` holds; `git log -S` finds `--no-renames` in no
hook on the branch or `upstream/main`), `5223afb` (BL-62; test-first, two of four new fixture tests red under the old
every-class rule, then 122 tests / 0 failures, 118 before; five mutants each fail it; the branch's
`.context-budget.json` note now says *"in the read-set class"*) and `0d63410` (BL-63). Branch gate on `0d63410`:
`10/10 pass · results 1a14fa9610cb`, `tests-sh-passed` 149, `context_budget.py --status` nothing over budget,
`bin/check-links` 111. Merged into fork `main` as `5f5a400`: `CHANGELOG.md` and `.context-budget.json` conflicted and
resolve ours, and the four merged files' 109 changed lines equal the branch patch. `bin/status` on the six adopters,
from `53733f3` and from `5f5a400`: every present copy of the three distributed files reads one version further behind,
and none newly *locally modified*. Fork `main`'s own config note on the test (the `HANDOFFS.md` row) is updated to
match.


**P12 done at S189 (2026-09-18): [PR #84](https://github.com/KJ5HST/methodology/pull/84), OPEN and MERGEABLE, head
`20db3f0`, opened on the operator's go-ahead.** Step 1: PR #80 and #82 are ancestors of the branch; `upstream/main`'s three
new commits touch no rule file. Step 2: the merge `f572068`, then `adaa4a3` (item (10): the three read-set densities
re-measured on the branch's blobs, each run reproducing the previous figure as a control) and `036d840` (two code comments
stop citing *"BL-57 item (22)"*). Step 3: dry runs from `upstream/main`, the branch and fork `main` into scratch copies of
the six adopters: the PR adds no refusal and removes three in `airqino` and `wsfct`; every refusal is a fork-only version
or a genuine local edit. Step 4: gates 10/10 in `--no-local` clones. Step 5: the body, frozen at `72450d8` for review.
(24) **An independent review of the frozen branch and body found five defects in the diff; the operator chose to fix them
before opening (picker).** `f4e974c`: `HANDOFFS.md` keys on `handoffs-format: 2`, the first line of the seed's size
section. **This revises D9:** the heading had been in upstream's seed since `56997af`, over the size premise this plan
removes, so it failed its own property 2, and `airqino` and `nprcgenekeepr` read current while carrying that text.
`7813652`: the `CHANGELOG.md` route keeps the trimmer's archive-pointer block and month heading (item (19)'s hazard, now in
the note itself). `f7d3b8c`, `91f7646`, `20db3f0`: wording. Gate on `20db3f0`: `10/10 pass · results f6b5a63009e8`,
`tests-sh-passed` 153. Also decided in that picker: F5 keeps the pinned link, and the body says it departs from the
maintainer's *"publish the design doc"*; the fork codes in commit subjects are explained in the body, not rewritten.
Decided earlier the same session: the history-walk fix (BL-54) goes upstream as its own PR.
**What (24) means for P8–P11.** (a) **Fork `main` lacks `f572068`..`20db3f0`**: its `bin/status` still keys `HANDOFFS.md`
on the heading, and its `CHANGELOG.md` route still deletes the trimmer's lines. Merge the branch into fork `main` before
P8 syncs from it (Route B), as items (11), (14), (22) and (23) did. Expect `CHANGELOG.md` and `.context-budget.json` to
conflict (resolve ours, as at `5f5a400`). (b) Step 3's `HANDOFFS.md` bullet now keys on the marker line. (c) `airqino` (P6,
done) and `nprcgenekeepr` (P10) now read `HANDOFFS.md` stale: P10 carries it, and `airqino` needs a follow-up in its own
repository.
**(a) DONE at S190: merged into fork `main` as `2410657`** (parents `1f5dcae`, `20db3f0`; two merge bases, `0d63410` and
`6b29d3d`, since `upstream/main`'s side of `f572068` was already in fork `main`). `CHANGELOG.md` and `.context-budget.json`
conflicted, as `git merge-tree` predicted, and resolve ours: `adaa4a3`'s densities are for upstream's `CLAUDE.md` and runner
blobs, and this repo's config budgets neither by measured density, so no note needed a hand fix. The other eight files'
66 changed lines equal the branch patch `f572068..20db3f0`; four are blob-identical to the branch. `bin/status` on the six
adopters from a `--no-local` clone of `1f5dcae` and from `2410657`, the adopters unchanged between the two readings: 15
rows move, all the merge's. (c) is now observed: `airqino` and `nprcgenekeepr` `HANDOFFS.md` read `present (stale format)`
(7 → 9 stale seeds). Every present copy of `BOOTSTRAP.md`, `ITERATIVE_METHODOLOGY.md` and `FRAMEWORK_APPARATUS.md` reads one
version further behind, and none is newly *locally modified*. Gate in a `--no-local` clone of `2410657`: `10/10 pass ·
results 91c29bff06ce`, `tests-sh-passed` 321 at 2 receipts (the diff adds 6 assertions and removes 2, all in Test 20; its marker and route rows pass).

**P8 done (2026-09-18) in `vscode_quarto_ext`'s own repository, its Session 264; recorded here at S191.** Eleven commits
on `master`, not pushed: `48d1790c` (claim), `e8c395b3` (the package allowlist, ahead of the sync: item (25)),
`b8a503e7` (the sync from fork `main` `0ab3881`: 14 files plus its entry, 15 in all, item (18) applied), `acb43e0b` (the
`CHANGELOG.md` header, block old :1–8), `69f0dd43` (the `HANDOFFS.md` section, inserted at :29 above the pointer block),
`4b727a9d` (`CLAUDE.md`'s tag rule; `CHANGELOG.md` out of `.context-budget.json`, Q2 A), `e2ad2dbb` (two finished
`BACKLOG.md` items removed: item (26)), `6d66070a` (a budget comment's figures), `3fa063aa` (its learnings), `a8e56e54`,
`57750bb2` (close-out). The row's line numbers, read at `58f7bcbd`, still held at the claim. DONE, re-run read-only from
here at S191 in a `--no-local` clone of `vscode_quarto_ext` at `57750bb2`, with `bin/status` and `bin/sync` from a clone of
fork `main` `0ab3881`: `bin/status` reads `CHANGELOG.md` and `HANDOFFS.md` `present` and every tracked file current;
`bin/sync --dry-run` exits 0, 23 files unchanged; §9.8 on `acb43e0b` with 1–8 prints *only the block changed*, and 1–7 as
a control names `(6, 3)`; `grep -c '^### '` went 25 → 26 and the audit 20 → 21 (250 → 251 with the shards), the
migration's 1 entry and none of the block's; §9.8 on `69f0dd43` with 29–29 and `HANDOFFS.md` prints *only the block
changed*, the diff a pure 61-line insertion; the trimmer's dry run prints `L1_OK`, `L2_OK` and `L3_OK` on both ledgers.
The build item (compile, `npm test` 2912/2912, the package check) rests on S264's receipt and was not re-run from here.
What P8 found, for P9–P11:
(25) **The sync can break a project's own release gate.** `vscode_quarto_ext`'s package check refuses any top-level file
it does not list. The sync adds `quality_ratchet.py` and `.quality-gates.json` at the root, and the first
`quality_ratchet.py --run` writes `.quality-gates-results.json`. S264 excluded all three one commit before the sync
(`e8c395b3`), so no commit on `master` fails and the sync commit still holds only what `bin/sync` wrote. **For P10 the
same gap is already visible:** `nprcgenekeepr` is an R package, and none of `quality_ratchet.py`, `.quality-gates.json`,
`.quality-gates-results.json`, `context_budget.py` or `.context-budget.json` matches a pattern in its `.Rbuildignore`
(checked at S191 with Python's `re` against its patterns, not by `R CMD build`; its dry run is refused today, so the full
list of new files is unmeasured). `model_project_constructor` has a `pyproject.toml`, not checked; `mts-system` has no
packaging file at its root. At each claim, read the dry run's new root files against the project's build ignores.
(26) **The phase can finish the project's own backlog items, and the rules it syncs require removing them in the same
commit.** P8's header migration and a stale-dashboard item were open in `vscode_quarto_ext`'s `BACKLOG.md`; S264 first
tagged those commits `[ad hoc]` and left both open, and its own verification caught it (`e2ad2dbb`). The ledger rules
arrive with the sync, so the claim (`48d1790c`) and the package commit predate them; `e8c395b3`'s entry records the
claim's, one commit late. At P9–P11's claim, grep the project's backlog for migration and methodology-update items and tag
those commits with the item.
(27) **`bin/check-handoff` skips the newest receipt in any `HANDOFFS.md` that carries the seed's size section: BL-72.** The
section holds a ```` ```sh ```` block. The scanner (`bin/check-handoff:254`–`:290`) knows only bare fences and the
`handoff` opener, so it reads that block's closing ```` ``` ```` as an opener and skips to the first receipt's close,
then reports OK with one receipt fewer. Measured at S191 on the files as they stand: `vscode_quarto_ext` (S264 skipped),
`airqino` (S19) and `nprcgenekeepr` (S714), the last two through an older copy of the section; `mts-system` reads its
newest correctly until P9 adds the section. `methodology_trim.py` is unaffected (17 records in `vscode_quarto_ext`, S264
among them). The checker is canonical-only, and this repo's own `HANDOFFS.md` has no such block, so its gates are
unaffected; the ```` ```sh ```` block is in `upstream/main`'s seed too.
**Decided by the operator at S191 (picker), after P8's report.** (a) **D7, for `vscode_quarto_ext`: `HANDOFFS.md` stays in
its budget** (65,536 B; the file is 146,916 B, so it reads `over`). The remedy is a trim in that project, its own action,
not dropping the warning: unlike `CHANGELOG.md` (Q2 A), that project's `.context-budget.json` classes `HANDOFFS.md`
`read-mandated`. §8's D7 row stays open for
the other adopters, with this as its precedent. (b) **BL-72 is fixed before P9**, in its own session; whether the fix goes
upstream inside PR #84 or on its own is decided then, as its own go-ahead. (c) **P9–P11 keep this plan** rather than a
generic `bin/status` → `bin/sync` route. Measured first, read-only, against the eleven local projects that have a
`SESSION_RUNNER.md`: from fork `main` `0ab3881`, eight sync cleanly and three are refused only for genuine local edits
(`model_project_constructor`, `feedback-loop-comparison`, `nprcgenekeepr`); from a simulated `upstream/main` with PR #84
merged (a `--no-ff` merge, as the maintainer merged #80 and #82), nine are refused, six of them only because they hold
versions from this fork's history that upstream's never had. So after PR #84 merges, these projects keep syncing from fork
`main`, or each takes one `--force` after checking what it would overwrite.

**P9 done (2026-09-18) in `mts-system`'s own repository, its Session 139; recorded here at S193.** Nine commits on
`master`, ~~not pushed (the operator there declined a push; `origin/master` is still `710a0f7`)~~ **pushed 2026-09-19
after S193's close-out, a fast-forward `710a0f7..b8a20ce` (recorded there at `27c77ec`, which is local; recorded here at
S194).** On `b8a20ce` Lint passed and Drift Sentinel failed, as its scheduled runs at `710a0f7` already had: production's
`/health` reports `e2041b0` (the failed run's annotation), and `e2041b0..b8a20ce` changes no application code: 19
root files (methodology tools and their configs, `.gitignore`, the ledgers and session documents) and five under `docs/`. It stays red
until the next `scripts/deploy_vps.sh`, which refuses unless HEAD equals `origin/master` (:94), so `27c77ec` goes up
first; both are that project's go-ahead. The nine: `a48f543` (claim),
`76c7f38` (`.gitignore` gains `.quality-gates-results.json`, one commit ahead of the sync: item (25) applied, and item
(29)), `adb2c9b` (the sync from fork `main` `v3.7-956-g99fb6bf`: 16 files plus its entry, 17 in all, item (18) applied),
`f70358c` (the `CHANGELOG.md` pointer and marker, a pure 10-line insertion after old :9), `24c590f` (the `HANDOFFS.md`
section, a pure 61-line insertion above the first receipt), `e4b36f1` (`CLAUDE.md`'s ledger wording at three sites and a
legacy-layout adaptation), `97f8aa7` (item (28), filed there as CLEANUP-006), `6b9cbb4` (its learnings), `b8a20ce`
(close-out). The row's line numbers, read at `710a0f7`, still held. DONE, re-run read-only from here at S193 in a
`--no-local` clone of `mts-system` at `b8a20ce`, with `bin/status` and `bin/sync` from a clone of fork `main` `99fb6bf`:
`bin/status` reads `CHANGELOG.md` and `HANDOFFS.md` `present` and every tracked file current; `bin/sync --dry-run` exits 0
with nothing to write; neither ledger lost a line across the phase (`git diff --numstat 710a0f7 b8a20ce`: `CHANGELOG.md`
+61/−0, `HANDOFFS.md` +78/−0), and every old line survives in order; at `f70358c` `grep -c '^### '` went 266 → 267 and
the anchored audit 265 → 266, the migration's 1 entry (no shards); the trimmer's dry run prints `L1_OK`, `L2_OK` and
`L3_OK` on both ledgers. **§9.8 cannot fail on either commit:** both are pure insertions, and a control range prints the
same (S139 found this; confirmed here), so the zero-deletion count and the order check carry that item. The build item
(backend 664, admin 1336 and web 105 tests passed) rests on S139's receipt and was not re-run from here.
**BL-72's fix, on a real ledger for the first time.** Asked which receipt is the newest (`scan()`'s first block): at
`710a0f7` every checker reads S138. At `b8a20ce`, with the seed's section and its `sh` block above the receipts, the
unfixed checker (`20db3f0`, identical to `upstream/main`'s) still reads S138, 70 blocks, skipping S139; the fixed one
(`77afc12`, and fork `main` `99fb6bf`) reads S139, 71 blocks. From fork `main`, `check-handoff --all` reports the same 33
issues before and after, all in older receipts, only their line numbers moved: P9 added none. BL-73's three twice-opened
receipts now open at :294, :397 and :749 (:216, :319 and :671 at `710a0f7`).
What P9 found, for P10–P11:
(28) **A ledger can hold a second, superseded rules block below its header, and the phase row did not name it.**
`mts-system`'s `CHANGELOG.md` keeps the pre-v3.5 seed's rules text, from `## How to add an entry` to the seed's
`<!-- Entries go below … -->` comment: 48 lines at :782 on `b8a20ce`, first added by `28e9bb3` (its v3.5 sync), now
between two runs of entries. Its fenced format example holds one `### ` line, and its tag list matches the old-form
audit four times; the anchored audit matches none of it. S139 found it by scanning the whole file's headings and filed
it there as CLEANUP-006 rather than widen the phase. By step 3's own rule (replace *the rules text … the block*) it is
part of the migration, as the P10 row already treats `nprcgenekeepr`'s block between two runs of entries, so it is
**P9's remainder**: one commit in `mts-system`, on which §9.8 with the block's bounds can fail, since the commit removes
lines. Predicted for that commit: `grep -c '^### '` +0 (−1 for the block, +1 for its entry), the anchored audit +1, the
old-form audit −3 (−4, and +1 only if the entry's own text matches once: the unanchored form also counts prose). **S139 asked whether P9's recorded counts should be restated: no.** Each count is recorded
against the commit it was measured on, and the remainder records its own. **At P10 and P11's claim, list the whole
ledger's `## ` headings (`grep -n '^## ' CHANGELOG.md`), not only the header.**
(29) **A strict deploy gate refuses what the synced tools write, not only what the sync adds.** `mts-system`'s
`scripts/deploy_vps.sh` refuses to deploy while any file is untracked (:82) and rsyncs with `--exclude-from=.gitignore`
(:111–112), so every file a synced tool writes must be tracked or ignored. `76c7f38` covers
`.quality-gates-results.json`. Not covered there: `context_budget.py` appends `.context-budget-history.jsonl` when a
measurement changes (S139's receipt, gotcha (b)), and `mts-system`'s `.gitignore` does not list it. At P10 and P11's
claim, check what the synced tools write when they run, beside item (25)'s new root files.

**P10 done (2026-09-19) in `nprcgenekeepr`'s own repository, its Session 719; recorded here at S194.** Decided first by
the operator at S194 (picker), from four options each run in a scratch clone at `312996b0`: `--force` the sync, then
re-apply the project's 49-line `SESSION_NOTES.md` extension to `methodology_trim.py`. Run from S194's launch prompt,
[`bl57-p10-nprcgenekeepr-launch-prompt.md`](bl57-p10-nprcgenekeepr-launch-prompt.md). Eleven commits on `master`, not
pushed (16 ahead of `origin/master` `4cfe2dad` in all, with S717's backfill and S718's four): `74243f04` (Phase 0 backfill of `312996b0`), `d064993a` (claim),
`00b8a4ca` (six `.Rbuildignore` patterns and two `.gitignore` entries, ahead of the sync: items (25) and (29) applied),
`b773ddb6` (the forced sync from fork `main` `v3.7-964-gce14b3f`: 15 files plus its entry, 16 in all, item (18)
applied), `63b3286f` (the extension re-applied), `ba1f0135` (the `CHANGELOG.md` pointer and marker, a pure insertion),
`47364f51` (the `HANDOFFS.md` `## Size, and when to archive` section replaced), `2f451d1d` (`CLAUDE.md`: the trimmer
checklist corrected, the bare `[BL]` tag and the empty `## 2026-08` recorded as legacy forms, and the trim-budget choice),
`f88afcb2` (its backlog), `a095f4be` (close-out), `4565c39d` (receipt sha). DONE, re-run read-only from here at S194 in a
`--no-local` clone of `nprcgenekeepr` at `4565c39d`, with `bin/status` and `bin/sync` from fork `main` `ce14b3f`:
`bin/status` reads `CHANGELOG.md` and `HANDOFFS.md` `present`, 22 tracked files current and `methodology_trim.py`
*locally modified*, by design; the dry run exits 2 on that file alone, and with `--force` would write only it. The
trimmer at `b773ddb6` is byte-identical to fork `main`'s, and `63b3286f` adds exactly the original 49 lines (the same
added lines as `git diff 18d8e3c7 312996b0`), nothing removed. §9.8 with bounds `62 117 HANDOFFS.md` on `47364f51`
prints *only the block changed*, and the new section (`:62`–`:121`) equals the seed's `:89`–`:148`. `ba1f0135` is 13/0
in `CHANGELOG.md`, and all 540 old lines survive in order. From the claim `d064993a` to `4565c39d`, `grep -c '^### '`
went 37 → 46 and the anchored audit 24 → 33: nine entries, all `[ad hoc]`. The trimmer's dry run prints `L1_OK`–`L3_OK`
on all three ledgers (46, 11 and 21 records at `4565c39d`; the report's 43, 11 and 20 are the counts at `2f451d1d`).
All six files from item (25) match an `.Rbuildignore` pattern, and `git check-ignore` confirms both tool outputs are
ignored. The build item (the R CMD build tarball ships none of the tooling or ledger files; the test suite 2,437 blocks,
0 failed, equal to S718's baseline) rests on S719's report and was not re-run from here; a full `R CMD check` was not run
there. The report's *"`bin/_manifest.py` lists the trimmer at `:50`, not `:45`"* reads fork `main`, where it is `:50`;
the prompt named `upstream/main`, where it is `:45`. Both are right. **Open there, that project's go-ahead:** the push,
the trim-budget cadence (it took 1.5.0's 196,608 B default; `--budget-bytes 65536` restores the old 65,536 B), and
whether to adopt `context_budget.py`.
What P10 found, for P11 and the upstream route:
(30) **The block a phase row names can leave the live file before the phase runs.** Measured on 2026-09-14 at
`:3946`–`:4065`, `nprcgenekeepr`'s rules block was gone by P10: its own S702 trim (`6bac092f`, 2026-09-17) had moved it into the frozen
shard `docs/archive/CHANGELOG-through-2026-09-17.md` (`:4171`). A shard is not edited, so the ledger step became a pure
insertion, like P9's. At P11's claim, re-derive the row's line ranges against the live file, and search the shards too.
(31) **A locally extended synced tool can be kept, at a price every later sync pays.** Force, then re-apply, works: the
patch applies onto trimmer 1.5.0, and the extended copy's dry run matched the old one's. The file then reads *locally
modified*, so every later `bin/sync` refuses the whole run (exit 2) until BL-32 gives adopters a supported way to add a
ledger. BL-32's detail says `bin/sync` *"silently discards"* such an edit; today it refuses. The same sync also moved
the trimmer 1.1.2 → 1.5.0, which raises the byte trigger from 65,536 to 196,608 B and drops the line trigger: an adopter
on an old trimmer gets a new trim cadence from a sync, and only `--budget-bytes` keeps the old one.

---

## 0. The answer

The framework states its rules for `CHANGELOG.md` across fourteen files (§4.2), and they disagree in
sixteen ways (§1.1). Most of the disagreement has one cause: the bulk of the rules live **inside the
seed** `starter-kit/CHANGELOG.md` — 11,804 of its 12,893 bytes — and `bin/sync` writes a seed once and
never again, so every correction strands the copies already in adopters. `wsfct/CHANGELOG.md:101` and
`nprcgenekeepr/CHANGELOG.md:3982` still call truncation *silent*, although the framework corrected that
at BL-51's Phase A.

The plan moves the rules to **one synced home**, a new §The Action Ledger in `FRAMEWORK_APPARATUS.md`.
It shrinks the seed to a linked pointer carrying a format marker that `bin/status` keys on. Then it fixes
each contradiction once, in that home, as the operator decided: **archiving is optional**, because
nothing reads the ledger whole; **`[BL-<id>]` accepts any backlog id**; **one entry per commit, never
edited**.

Four sessions build it on a branch from PR #80's head (P1–P4). One brings it to fork `main` and this
repo's own ledgers (P5). Six migrate the adopters, each in its own repository (P6–P11). The last opens a
**new** upstream PR once #80 has merged, which is its own go-ahead (P12). PR #80 itself is not touched.

---

## 1. Context

### 1.1 The sixteen findings

C1–C8 are BL-57's own, each re-read on `b82dcff`. C9–C16 were found while taking this plan's inventory;
C16 follows from Q4 A.

| # | The disagreement | Where it is stated | Phase |
|---|---|---|---|
| C1 | Whether a session reads the file at all | *It does:* seed :96–97, :104 (*"every session pays for the whole file"*), :180–181 (*"split into shards once it outgrows a session's read"*); `HANDOFFS.md` seed :91, :98, :150; `methodology_trim.py:186` (*"the per-file context-tax budget"*); upstream's root `.context-budget.json` (`CHANGELOG.md` read-mandated at 65,536 B). *It does not:* runner :37–38 (Phase 0 takes a frontier from `git log`); `BOOTSTRAP.md` :136, :383. *Measured:* one whole read per root ledger in 85 transcripts (BL-52, S112) | P2 |
| C2 | Which size triggers an archive | seed :103–104 (a 2,000-line rate plus a byte level, *"default 65,536 B"*); `methodology_trim.py` :164, :186 (196,608 B); *fork* root front matter (*When to archive again*, the line rate alone); upstream's root (none); this repo: do not trim (operator, 2026-09-14) | P2 |
| C3 | "Append" or "prepend" | *Append … newest on top:* runner :278, :329, :357; `ITERATIVE_METHODOLOGY.md:294`; `HOW_TO_USE.md` :767, :804; `.githooks/pre-commit:56`. *Prepend:* seed :17, :91; runner :39 | P4 |
| C4 | Whether a trim may happen in Phase 0 | seed :167–169 (never); *fork* root `HANDOFFS.md:15` (count at Phase 0, trim to 4) | P2, P5 |
| C5 | Two definitions of a stale seed | `bin/_manifest.py:95–98` keys on the seeds' titles, which never change, so the check cannot fire — and `b82dcff` ships Learning #19 saying exactly that. *Fork* `bin/_manifest.py:125–128` keys both on `Size, and when to archive` (`12463dd`, S41, never upstreamed) | P1 |
| C6 | A closed tag vocabulary, an open practice | seed :23–32; runner :278, :329; `ITERATIVE_METHODOLOGY.md:294`; `.githooks/pre-commit:57` — against 361 adopter entries carrying a non-numeric `[BL-…]` id (§4.4) and the canonical tutorial's own `[BL-F1]` (`docs/tutorials/T2_worked_transcript.md:257`) | P3 |
| C7 | Where the Phase 1B marker lives, and whether a claim commit has an entry | runner :88 and `ITERATIVE_METHODOLOGY.md:169` put `CHANGELOG: pending` in `SESSION_NOTES.md` and say the actions are recorded at Phase 3F. Neither this repo nor upstream keeps a `SESSION_NOTES.md`: both write an entry at the claim — the fork a new one per commit, upstream one it edits at close-out — and the *fork* hook exempts a claim commit from having any entry (`.githooks/pre-commit:53–120`) | P4, P5 |
| C8 | One entry per action, or per session | runner :278 (*"one per commit and per non-commit action"*) — against upstream's practice: each of S13–S17 wrote one entry at its claim and rewrote 1–2 lines of it at close-out | P4 |
| C9 | A proposed guard that would refuse every trim | upstream's S16 receipt, next step (e): refuse a commit whose staged `CHANGELOG.md` has fewer `### ` headings than `HEAD`'s. Every trim lowers that count by design (`aaa6d30`: 80 → 27) | P2, P12 |
| C10 | An audit that miscounts, or fails | seed :24, runner :39 and upstream's root `CHANGELOG.md:14` publish the unanchored, one-file form. The seed's own shard rule (:160–162) says an enumeration must span the shards, and *fork* root :22–25 records the unanchored form counting 78 against 64. The shard-spanning glob form in turn fails under zsh wherever no shard exists: *"no matches found"*, then 0 (bash: 43, on `b82dcff`) | P3 |
| C11 | What the file is | *"Completed work history":* `BOOTSTRAP.md` :23, :107, :131; `README.md` :96, :114, :200; `CLAUDE.md:51`. *Completed-work framing:* `BOOTSTRAP.md` :139, :145 — against the seed's action ledger, which also records non-commit actions and declines (:3–8, :30–32) | P4 |
| C12 | Distributed seeds cite fork-only material | Both seeds' *Lines* rows (seed :103, `HANDOFFS.md` seed :97) cite `BL-52` and `docs/planning/read-cap-premise-correction-plan.md`; neither exists on `b82dcff` | P2 |
| C13 | Where a month section starts | seed :92 (*"promote … as the list grows"*); *fork* root :48–52 (prepend under the topmost `## YYYY-MM`, open a new one when the month changes); upstream's root :34 promises sections and has none; `nprcgenekeepr` files September's entries under `## 2026-08` | P4 |
| C14 | The `HANDOFFS.md` seed repeats C1 and C2 | `starter-kit/HANDOFFS.md:89–125` — the same premise, the same 65,536 B, and a cross-reference (:123) to the `CHANGELOG.md` seed section this plan moves | P1, P2 |
| C15 | BL-47's proposal went stale | BL-47 proposes adding both ledgers to the seed `context-budget.json` at 65,536 B. Under Q2 A the ledger is not a read-budget file, and this repo already dropped it (`3c8acd5`) | S162 records it |
| C16 | The stale-seed advice rewrites entries | `BOOTSTRAP.md:85` and `bin/status:188–192` tell an adopter with a stale seed to *"reconcile its header and per-entry format"* by hand — rewriting committed entries, which Q4 A forbids. P1's marker makes every adopter read stale, so the advice meets all six at once | P1 |

### 1.2 Why they keep coming back

`bin/_manifest.py` ships two kinds of file. **Tracked** files belong to the framework, and `bin/sync`
keeps them current. **Seeds** — `CHANGELOG.md`, `HANDOFFS.md`, `SESSION_NOTES.md`, `ROADMAP.md`,
`.context-budget.json` — are written once and then belong to the adopter, because they hold its history;
sync never touches them again.

The seed `CHANGELOG.md` is a 970 B header, **11,804 B of rules** and a 119 B footer. The rules are *How
to add an entry* (4,517 B), *Size, and when to archive* (6,621 B) and *CHANGELOG.md vs SESSION_NOTES.md*
(666 B). Each adopter holds a snapshot of them from the day it was seeded. The framework has corrected
them since — the *silent truncation* row became *announced* at BL-51's Phase A — and the copies did not
move. Fixing the words without moving them would restart the same drift at the next correction.

A second cost shows in §4.4: the seed's fenced example entries are line-shaped like real ones, so in an
adopter that carries the rules text, a line-based audit counts the examples as entries (`wsfct`: three).

### 1.3 Constraints

- **K1 — PR #80 is under private review.** Its head is `b82dcff`; the maintainer's queue (the S17
  receipt on `upstream/main`) begins *"#80 decision F1 + fixes F2/F3 → merge"*, and F1–F3 are not
  public. This plan adds nothing to #80. It builds on a branch from `b82dcff`, because the seed text it
  changes arrived with #80 (PR #77, `56997af`) and does not exist on `upstream/main`.
- **K2 — The Phase 0 read has no spare bytes.** On `b82dcff`, `context_budget.py` exits 2: runner
  52,195 B against its 41,364 B ceiling, the read-set 67,581 B against 56,750 B. On the simulated
  post-merge tree (`upstream/main` ⊕ `b82dcff`, tree `e48a828e`), upstream's S16 paragraph also takes
  `SAFEGUARDS.md` to 16,353 B against 15,386 B. **This plan never grows the runner, and never touches
  `SAFEGUARDS.md`.**
- **K3 — The maintainer's queue shares two files.** After #80: v3.8; the S16 follow-ups
  (`commit-msg --selftest` in `bin/tests.sh`, `BOOTSTRAP.md` Step 10); quality-ratchet Phase 1
  (`SESSION_RUNNER.md`'s FM #17 row, Degradation table and Phase 3C routing, plus `SAFEGUARDS.md`,
  `ITERATIVE_METHODOLOGY.md` and a Learning row); then the ledger-count ratchet.
- **K4 — Learning numbers diverge between the trees.** `b82dcff`'s table stops at #47 and fork `main`'s
  at #64; upstream's `docs/operator-gated-review-plan` reserves #14. **The PR adds no Learning row.**
- **K5 — Operator decisions in force.** Do not trim this repo's `CHANGELOG.md` (2026-09-14).
  `CHANGELOG.md` is out of this repo's read budget (`3c8acd5`). `HANDOFFS.md` keeps four receipts (S127).
- **K6 — Every outward action is its own go-ahead** — pushing the branch, opening the PR, any comment on
  #80 (`CLAUDE.md` §Contributing upstream).
- **K7 — Seeds are migrated by hand, in each adopter's own session** (the runner's session-notes
  boundary). Sync never rewrites one.
- **K8 — Every command the rules publish must run in zsh and in bash.** zsh is the macOS default shell,
  and it aborts a command whose glob matches nothing (C10).

---

## 2. Decisions

### 2.1 Answered by the operator at S162 (2026-09-14)

| # | Question | Chosen | Not chosen |
|---|---|---|---|
| Q1 | Where the rules live | **A — one synced home**, `FRAMEWORK_APPARATUS.md` §The Action Ledger; the seed keeps a pointer and a format marker | B: keep the rules in the seed and flag stale copies. C: move only the size rules |
| Q2 | The archive rule | **A — optional.** Nothing reads the ledger whole, so no size is stated and the trimmer stays available; past the default-read refusal, read with offset/limit | B: mandatory at the trimmer's trigger. C: each project records its choice |
| Q3 | Source tags | **A — `[BL-<id>]` takes any backlog id.** Three families, one per entry; the audit is anchored and spans shards | B: numeric ids only. C: an open vocabulary |
| Q4 | Entries | **A — one per commit, never edited.** A claim's entry says *(in progress)* and close-out adds its own. A correction is a new entry; the one exception is removing content that must not be published, recorded by an entry of its own | B: one per session, edited until close-out (the maintainer's practice). C: fix only the wording |

Q4 was chosen after comparing A and B on measurement. Of this fork's last 60 commits that touched the
ledger, 56 only inserted, three edited a committed entry (`7a6ea4b`, `7b30980`, `e48ffa9`) and one
trimmed (`aaa6d30`). Upstream's S13–S17 each rewrote their own entry at close-out. S16's rewrite, done
by a script that searched for the wrong boundary, deleted ten other entries (`356556f`: 40 → 30
headings; restored in `ed98444`).

### 2.2 Recommended — approved with this plan unless the operator says otherwise

- **D5 — Route.** A **new** upstream PR, opened after #80 merges, from branch `bl57/changelog-rules`
  (created from `b82dcff`) brought onto `upstream/main` at P12. Not commits on #80 (K1). A stacked PR
  against `read-set-budgets` only if #80 is still open when P12 is ready, and only on the operator's
  choice then.
- **D6 — Rollout.** Adopters migrate after P5, before the PR merges: from fork `main` (Route B), or from
  the branch for `airqino` (Route A). Thin seeds make that safe: if review changes the text, the change
  reaches adopters by sync and the hand migration is not repeated. The PR does not wait for them.
- **D7 — `HANDOFFS.md`'s own archive rule stays as it is**, apart from C1, C2 and C12's defects in its
  seed. Extending Q2 A to it is left to the operator (§8).
- **D8 — Two upstream-root changes, each its own commit.** (i) Upstream's root `CHANGELOG.md` front
  matter, the maintainer's own file: its pointer to the seed's rules (:11–12), which P1 makes false; its
  audit (:14); and its month sentence (:34). (ii) `CHANGELOG.md` leaves upstream's root
  `.context-budget.json` (this fork's `3c8acd5`, same reasoning). The PR body says either can be dropped,
  and that dropping (i) leaves :11–12 pointing at a seed that no longer holds the rules.
- **D9 — Markers.** `CHANGELOG.md` keys on a new versioned token on the seed's pointer line (§3.2).
  `HANDOFFS.md` keys on the heading `Size, and when to archive` on both trees — fork `main`'s S41 choice,
  brought upstream — so its seed keeps that heading.
- **D10 — The fork hook's claim carve-out goes.** *Fork* `.githooks/pre-commit:16–17`, `:53–120` and
  `:144` let a claim commit carry no entry, and *fork* Test 27 (`bin/tests.sh:1195–1700`) pins that.
  Under Q4 A a claim commit carries an *(in progress)* entry. Both upstream's claims (S13–S17) and this
  fork's recent ones (`7ea7346b`) already do, and `b82dcff`'s hook has no carve-out. P5 removes it and
  its test; the operator can keep it instead, in which case §The Action Ledger must state the exception.

---

## 3. Target state

### 3.1 The one home: `FRAMEWORK_APPARATUS.md` §The Action Ledger

A seventh top-level section, beside the six the file already holds (it lands in adopters at
`docs/methodology/FRAMEWORK_APPARATUS.md`). In order:

1. **What counts as an action** — any commit, and every non-commit action (release, tag or branch
   operation, PR open, upstream issue close, access grant, decline or grooming decision). Re-expressed
   from the seed (:3–8, :30–32).
2. **The entry format** — `### YYYY-MM-DD · [SOURCE] outcome`, the detail bullets, the optional
   **Model:** bullet and the capability-tiered examples. Moved from the seed (:34–87).
3. **Source tags** — `[issue #<N>]`, `[BL-<id>]` (whatever id the project's backlog uses) and
   `[ad hoc]`; exactly one per entry. The audit, which runs in zsh and bash alike (K8) and reads the
   committed shards:

   ```
   cat CHANGELOG.md $(git ls-files 'docs/archive/CHANGELOG-*.md') \
     | grep -cE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[(issue #[0-9]+|BL-[^]]+|ad hoc)\]'
   ```

   Entries written before a project adopted the vocabulary stay as written; the audit does not count
   them.
4. **Lifecycle** — one entry per commit (the co-staging hook's unit) and one per non-commit action.
   - A claim commit carries an *(in progress)* entry; close-out adds its own entry.
   - A committed entry is never edited. A correction is a new entry naming what was wrong. The one
     exception is removing content that must not be published, recorded by an entry of its own.
   - A Phase 0 backfill is the one entry that may span several commits.
   - The Phase 1B `CHANGELOG: pending` marker lives in `SESSION_NOTES.md`; a project that keeps none
     relies on its pending `HANDOFFS.md` receipt.
5. **Placement** — prepend under the topmost `## YYYY-MM`, and open a new month heading above it when
   the month changes. A ledger that has no month headings starts them at its next new month; nothing is
   retrofitted. Entries stay at `###`, the level the tools key on.
6. **Reading the ledger** — never whole. Phase 0 takes a frontier from `git log`, close-out reads the
   top, and a lookup uses `grep` or `git log`. Past the harness's default-read refusal
   (`READ_REFUSE_BYTES`, `methodology_trim.py:130`), read with offset/limit.
7. **Archiving** — optional. `methodology_trim.py` does it losslessly for a project that wants it, and
   its `--check` is the only statement of a trigger; the rules name no size. The shard convention moves
   from the seed (:145–165). A trim is its own action with its own entry, never in Phase 0.
   **Conservation:** the live file and its shards together never lose an entry, so a count check counts
   both, as the audit in item 3 does — never the live file alone.
8. **Three files, three questions** — `SESSION_NOTES.md`, `HANDOFFS.md`, `CHANGELOG.md`. Moved from the
   seed (:176–183), with its read premise (:180–181) corrected in P2.

Expected size: 9–11 KB. P1 moves 11,804 B verbatim; P2 condenses the two-cap table and its
rate-versus-level argument, which Q2 A no longer needs.

### 3.2 The thin seed, `starter-kit/CHANGELOG.md` (about 1.5 KB)

It keeps the title (`bin/tests.sh:276` and the dashboard's fixtures use it). Then comes a purpose line,
still naming FM #27, the Phase 3F write and the Phase 0 reconcile as :5–8 did. Then **the pointer, as a
relative Markdown link carrying the marker**, so `bin/check-links` can prove it resolves — for example:

```
Entry format, source tags and archiving:
[§The Action Ledger](docs/methodology/FRAMEWORK_APPARATUS.md#the-action-ledger)
(ledger-format: 2 — keep this line; bin/status reads it)
```

— then the sentinel, `---` and the entries comment. P1 settles the wording. The marker must meet four
tests: it is absent from **every** earlier version of the seed; it sits in the front matter the trimmer
pins; it is on a line the seed tells adopters to keep; and it carries a version number the next format
change bumps.

### 3.3 The `HANDOFFS.md` seed

The heading at :89 stays (it is the marker, D9). P1 turns its cross-reference (:123–125) into a pointer to
§The Action Ledger. P2 corrects its read premise (:91, :150–151) and removes its 65,536 B row (:98) in
favour of the tool's trigger. The receipt-specific rules (:127–144) do not change.

### 3.4 Everywhere else: wording only

The runner, `ITERATIVE_METHODOLOGY.md`, `HOW_TO_USE.md`, `BOOTSTRAP.md`, `README.md`, `CLAUDE.md`, the
stale-seed advice in `bin/status`, the hook's refusal text and two trimmer comments (§4.2).

### 3.5 What does not change

- The failure-mode count (28), and FM #27's requirement that every action be recorded.
- The upstream hook's behaviour, and Phase 0 reconcile.
- The trimmer's behaviour and grammar: `methodology_trim.py:307` already accepts any bracket.
- The dashboard. Upstream has no read-cap code, and the fork's comments were already corrected (*fork*
  `starter-kit/methodology_dashboard.py:325–345`).
- `bin/model-report`: *fork* `:72` already accepts any bracket.
- **Any existing ledger entry anywhere** — nothing is retagged or rewritten (Q4 A).

---

## 4. Evidence inventory

### 4.1 How it was produced

The inventory is `git grep -n -I -i -E` over three refs — `b82dcff`, `upstream/main` and fork `main` —
with twelve patterns:
- `changelog`, `ledger`, `prepend`, `newest[- ]on[- ]top`, `append`;
- the byte constants with their derived neighbours (`65,?53[56]|196,?60[78]|262,?14[34]|98,?30[34]|56,?750`);
- `CLASS_A|READ_REFUSE|DEFAULT_BUDGET`;
- `source[- ]tag|ad hoc\]|\[BL-`;
- `SEED_FORMAT|Authoritative Action Ledger|when to archive`;
- `context-tax|watched`, `reconcile`, `\btrim`.

It excluded the ledgers themselves, `docs/archive/`, `docs/planning/`, `docs/RELEASE_HISTORY.md`,
`dashboard.html`, `*.jsonl` and `LICENSES`. It returned **1,577 lines in 45 files on `b82dcff`**, 905 in
39 on `upstream/main` and 2,679 in 48 on fork `main`, each read and classified below. The independent
review reproduced all three counts. The command is §9.1; re-run it at the start of every phase.

### 4.2 Sites that change

**D** = distributed, tracked; **S** = distributed seed; **C** = canonical-only. The fourteen
rule-bearing files are marked ●.

| File | Kind | Lines (`b82dcff`) | *Fork* `main` | Phase |
|---|---|---|---|---|
| ● `starter-kit/CHANGELOG.md` | S | :15–92, :94–174, :176–183 moved verbatim; :3–8 re-expressed in the purpose line; the thin seed | identical | P1 |
| `FRAMEWORK_APPARATUS.md` | D | new §The Action Ledger; intro :9–11 (*"The six sections below were moved here verbatim"*) | identical | P1–P4 |
| ● `starter-kit/HANDOFFS.md` | S | :123–125 (P1); :91, :97–98, :150–151 (P2) | identical | P1, P2 |
| ● `bin/_manifest.py` | C | :78–98 (comment and `SEED_FORMAT_MARKERS`) | :125–128 | P1 |
| ● `bin/status` | C | :188–192 (the stale-seed advice) | identical | P1 |
| `bin/tests.sh` | C | :266–303 (seed-marker fixtures; the title-only fixture is :276) | :290–305 | P1 |
| `tools/test_methodology_trim.py` | C | :238–253, :1824–1829, :2003–2007 and :2027–2035 change; :1692–1693, :1749, :1757, :1792, :1797, :1918, :2169–2175 must stay green | identical | P1 |
| ● `starter-kit/methodology_trim.py` | D | :358–363 (comment: *"the seed files are the proof"*) in P1; :186 (comment) in P2 | identical | P1, P2 |
| ● `HOW_TO_USE.md` | D | :748 (apparatus row, *"~330 lines"*), :767, :804 | differs by 2 lines | P1, P4 |
| ● `CLAUDE.md` (upstream's) | C | the Document Hierarchy row for `FRAMEWORK_APPARATUS.md`; :51 | :69 | P1, P4 |
| ● `.context-budget.json` (upstream root) | C | the `CHANGELOG.md` entry | already removed (`3c8acd5`) | P2 (D8 ii) |
| ● `starter-kit/SESSION_RUNNER.md` | D | :39, :88, :278, :329, :357 | :39, :88, :284, :335, :363 | P3, P4 |
| ● `ITERATIVE_METHODOLOGY.md` | D | :169, :294 | identical | P3, P4 |
| ● `.githooks/pre-commit` | C | :56–57 | differs (and has the carve-out, D10) | P3, P4 |
| ● `starter-kit/BOOTSTRAP.md` | D | :85 (C16) in P1; :23, :107, :131, :139, :145 in P4 | :23, :108, :133, … | P1, P4 |
| ● `README.md` | C | :96, :114, :200 | :114, :201, … | P4 |
| ● `CHANGELOG.md` (upstream root) | C | :11–12, :14, :34 — one commit (D8 i) | the fork's own — P5 | P4 |

**Fork-only (P5):**
- Root `CHANGELOG.md` front matter: the pointer (:11–12); the audit (:17–20), which takes `BL-[^]]+` and
  the cross-shell form; *When to archive again* (:105–141); and a new paragraph on this repo's claim
  practice.
- Root `HANDOFFS.md:15` (C4).
- The hook's carve-out and Test 27 (D10).
- The port of every file above.

### 4.3 Checked and unchanged

- **Consistent already:** runner :11, :24, :35–44 (reconcile mechanics), :91, :146, :159;
  `ITERATIVE_METHODOLOGY.md` :142, :148, :153, :160, :325, :425; `SAFEGUARDS.md` :117, :165–173 (the hook
  section, also left alone because of K2); `BOOTSTRAP.md` :136, :383 (already say the ledger is not read
  at session start — the statement C1 converges on), :323–325; `FRAMEWORK_APPARATUS.md:207`; every
  campaign checklist line *"recorded in `CHANGELOG.md` (Phase 3F ledger entry, failure mode #27)"*
  (`workstreams/*_CAMPAIGN.md`).
- **Tutorials:** T1 :86–92, :125–131; T2 :54, :89, :98–99; the T2 worked transcript :251–262 (prepend;
  *one action, one commit*; `[BL-F1]`, which conforms under Q3 A); T8 :57, :75–105, :179 (the
  `bin/status` output is still accurate).
- **No code change for Q3 A:** `methodology_trim.py:307` (`^### \d{4}-\d{2}-\d{2} · \[`), the dashboard's
  `_DATED_ENTRY_RE` (:210) and *fork* `bin/model-report:72` (`\[[^\]]+\]`) all accept any bracket.
- **History, never edited:** `README.md`'s *What's New*; `CLAUDE.md`'s version lines;
  `docs/RELEASE_HISTORY.md`; the `FRAMEWORK_LEARNINGS.md` rows that mention ledgers (append-only; on
  `b82dcff`, `grep -i ledger` finds rows 8, 9, 13, 15, 16, 17, 18, 22, 24, 26, 28, 31, 32, 35, 36, 39 and
  41); `docs/archive/`; `docs/audits/`; `docs/planning/`.

### 4.4 The adopters (measured 2026-09-14, read-only)

*Conform* counts headings in the live ledger plus its shards that match the audit, under the current rule
and then under Q3 A (§9.2). `/usr/bin/grep` and Python agree on the pattern.

| Adopter | State | `CHANGELOG.md` | Rules text it carries | Conform: now → Q3 A | Route (S161; re-derive) | Blockers and notes |
|---|---|---|---|---|---|---|
| `airqino` | branch `chore/methodology-read-set-budgets`, off open PR #1; 2 untracked | 1,309 B, pre-v3.1 template | none | 1 → 1 of 1 | runner is `b82dcff`'s; A | BL-56 (reseed); BL-54 if synced from fork `main` |
| `model_project_constructor` | `master`, clean | 666,365 B; Keep-a-Changelog layout, `### date — summary` | none | 0 → 0 of 155 | runner customized; refuses both | runner step 5 is a real customization; a format decision; no `HANDOFFS.md`, no trimmer. BL-57 names the `~/Development` checkout; the second, under `mpc_tests/`, is not included |
| `mts-system` | `master`, clean | 358,377 B; title and v3.1 intro, entries from :10 | none | 96 → 261 of 262 | B clean | hook enabled; `HANDOFFS.md` is 372,830 B (out of scope) |
| `nprcgenekeepr` | `master`; 9 untracked | 413,383 B; custom intro, a legacy block | an older seed copy at :3946–:4065, between two runs of entries (the first at :19, the next at :4070); *silent* :3982, 65,536 :3983 | 599 → 784 of 1,090 (live + 6 shards; 2 of the headings are the block's own) | refuses both | a 49-line local extension of `methodology_trim.py` blocks every sync; September's entries under `## 2026-08`; `CLAUDE.md:271` (S325, *"freeze legacy, go forward"*) |
| `vscode_quarto_ext` | `master`; 1 untracked | 87,837 B; Keep-a-Changelog header, `## [Unreleased]` | none | 236 → 247 of 257 (live + 1 shard) | runner is fork `main`'s; B clean | `[BACKLOG: …]` tags; its `.context-budget.json` lists `CHANGELOG.md` |
| `wsfct` | `master`, clean | 162,549 B | the full older seed copy, :13–196 (*silent* :101, 65,536 :102) | 130 → 130 of 133 (live + 3 shards) — **both include 3 fenced examples** in the block, which holds 5 `### ` lines; real entries: 127 of 128 | runner is fork `main`'s; B clean | `CLAUDE.md` :43, :218, :695 call it *"Completed work history"*; :162, :206 frame it as completed work |

This repo: 494 → 494 of 494 (live + 11 shards). `b82dcff`'s root ledger: 43 of 43.

---

## 5. Phases

### 5.0 How every phase works

- **Records go on fork `main`.** Each phase runs Phase 0, the claim and the close-out there (receipt
  and fork ledger).
- **The canonical work goes on a branch.** P1–P4 work on `bl57/changelog-rules`, created at P1 from
  `b82dcff` and checked out in its own worktree (`git worktree add ../methodology-bl57
  bl57/changelog-rules`), so `main` and the branch never share a working directory.
- **Each branch commit carries its own entry in the branch's `CHANGELOG.md`** — upstream's ledger — as
  #76–#79's did. The hook requires it and Q4 A defines it. Upstream's front matter (`upstream/main`
  :20–23) already accepts `[BL-<N>]` entries for work that originates in the fork.
- **Five files per commit at most**, the ledger included (`SAFEGUARDS.md` §Blast Radius Limits).
- **Suites run only in a `git clone --no-local`**, because `bin/tests.sh` rewrites both live ledgers.
  Such a clone copies only this repo's branches: fetch the ref first (hazard 12).
- **Commit before running the trimmer suite:** its seed fixtures read `HEAD:starter-kit/CHANGELOG.md`
  (`tools/test_methodology_trim.py:1692–1693`), not the working tree.
- **Every command a phase publishes runs in zsh and in bash** (K8).
- **Baseline at `b82dcff`**, taken at plan time in a `--no-local` clone that fetched the ref:
  - `bin/tests.sh`: 115 passed / 1 failed, exit 1. The failure is Test 9, `github source dry-run
    failed`, which reads GitHub's upstream `main` and fails on every tree until #80 merges.
  - Unit suites: 450 tests, OK (4 skipped).
  - `bin/check-links`: OK, 105 links across 23 distributed files.
- **Baseline at fork `main` `7ea7346b`:** `bin/tests.sh` 304 passed / 1 failed / 0 skipped, exit 1 (the
  same Test 9).

### P1 — One home, thin seeds, one stale-seed rule (structure only; no rule changes)

**Scope.**
1. `FRAMEWORK_APPARATUS.md`: add `## The Action Ledger` holding the seed's three rule sections
   **verbatim**, one heading level down — outside fences only, since the seed's fenced example entries
   (:37–43, :52–58, :64–76) are text, not headings. Update the intro (:9–11), which says the file holds
   six sections moved from `ITERATIVE_METHODOLOGY.md`.
2. `starter-kit/CHANGELOG.md`: the thin seed (§3.2).
3. `starter-kit/HANDOFFS.md:123–125`: point at the new home instead of the seed's section.
4. `starter-kit/methodology_trim.py:358–363`: the comment says the seeds' fenced examples *"are the
   proof"* of fence-awareness; after the move they live in the home and the tests' fixture. Comment only.
5. `bin/_manifest.py:78–98`: `CHANGELOG.md` keys on the new marker; `HANDOFFS.md` keys on
   `Size, and when to archive` (D9). Rewrite the comment, stating *fork* Learning #19's rule inline — a
   marker keyed to something that never changes across versions cannot fire — rather than citing its
   number: after #80's F1 (a), no row past #13 exists upstream (amended at S163).
6. **The stale-seed advice (C16).** `BOOTSTRAP.md:85` and `bin/status:188–192` describe the thin-seed
   migration: replace the rules text above the first entry with the current seed's header; leave every
   entry as written; reseed only a file that holds no history. The marker makes every adopter read stale
   in this same phase.
7. Tests:
   - `bin/tests.sh:266–303` — the in-use fixture at :276 is title-only and would read stale under the
     new marker, so give it the marker line. Add a fixture holding the pre-P1 seed (a frozen literal)
     that must read *present (stale format)*.
   - `tools/test_methodology_trim.py:238–253` and `:2027–2035` — three fence-awareness controls assert
     that *the live seed* holds probe-shaped example lines inside fences, and those lines leave. Move
     them onto one frozen literal fixture in the test file, not onto a pinned sha, which a fork clone may
     not hold.
   - `:1824–1829` — the `.replace()` anchor `## How to add an entry` leaves the seed. Choose an anchor
     the thin seed has and assert it occurs exactly once before replacing, or the test passes without
     testing anything.
   - `:2003–2007` — a docstring cites `starter-kit/CHANGELOG.md:10`; re-cite it.
8. `HOW_TO_USE.md:748` (the apparatus row's use column and *"~330 lines"*) and upstream `CLAUDE.md`'s
   Document Hierarchy row for `FRAMEWORK_APPARATUS.md`.

Suggested commits, each green:
1. the test refactor (green with either seed);
2. the move — `FRAMEWORK_APPARATUS.md`, both seeds and the trimmer comment;
3. the marker and its advice — `bin/_manifest.py`, `bin/tests.sh`, `bin/status` and `BOOTSTRAP.md`;
4. `HOW_TO_USE.md` and `CLAUDE.md`.

**DONE — all of these hold.**
- **The move is verbatim.** Each of the seed's three sections at `b82dcff`, with its headings demoted
  one level outside fences, occurs byte for byte in `FRAMEWORK_APPARATUS.md` (§9.3; the check caught all
  four mutants it was tried on at S162).
- **The thin seed is still a fresh seed.** `starter-kit/CHANGELOG.md` is ≤ 1,600 B with no `## `
  section. It keeps its title, sentinel and footer, and its purpose line names FM #27, Phase 3F and the
  Phase 0 reconcile. The trimmer reports `NO_RECORDS` (exit 0) on it, and `bin/sync` into an empty
  scratch directory seeds it.
- **The marker discriminates.** It occurs in the new seed and in no earlier version of it on any ref
  (§9.4).
- **The pointer resolves.** It is a Markdown link, and `bin/check-links` resolves it in the simulated
  adopter tree. `grep -c '^## The Action Ledger$' FRAMEWORK_APPARATUS.md` is 1.
- **The advice no longer rewrites entries.**
  `grep -n 'per-entry format' starter-kit/BOOTSTRAP.md bin/status` prints nothing.
- **`bin/status` from the branch gives the expected verdicts:**
  - `present` on the fresh scratch target;
  - *present (stale format)* for `CHANGELOG.md` on scratch copies of all six adopters, none of which is
    migrated yet, with the new advice beneath;
  - `HANDOFFS.md` verdicts equal to fork `main`'s `bin/status` on the same copies.
- **All three suites are green against the baseline**, every changed row named.

**Surface.** The branch worktree; suites in a `--no-local` clone of the branch; scratch copies of the six
adopters holding exactly what `bin/status` reads — never an empty target (*fork* Learning #64). **Cannot
enforce:** that a reader follows the pointer rather than guessing, or the anchor as GitHub renders it
(`check-links` resolves the file, and the grep checks the heading).
**One session. STOP.** Reasoning: the deepest available — a distributed seed and the tests that guard it.

### P2 — Reading and archiving (C1, C2, C4, C9, C12, C14)

**Scope.**
1. §The Action Ledger: rewrite the moved *Size, and when to archive* text to Q2 A (§3.1 items 6 and 7):
   - the three reads the protocol actually makes, and never a whole read;
   - offset/limit past `READ_REFUSE_BYTES`;
   - archiving optional, with the tool's `--check` as the only trigger statement;
   - the shard convention;
   - a trim is its own action, never in Phase 0;
   - conservation across the live file and its shards (C9).
   Also correct the read premise in the moved *three files* text (from seed :180–181).
2. `starter-kit/HANDOFFS.md`: keep the heading (:89). Replace the premise (:91, :150–151) and the
   65,536 B row (:98) with a pointer to the shared reasoning and to the tool's trigger. The file's own
   rule otherwise stands (D7).
3. `starter-kit/methodology_trim.py:186`: correct the comment. Nothing else in the tool changes.
4. Upstream's root `.context-budget.json`: remove the `CHANGELOG.md` entry, in **its own commit** (D8 ii).

**DONE.**
- **The false statements are gone.** Each of these prints nothing:
  - `grep -nE "reads it every session|every session pays|outgrows a session's read" starter-kit/CHANGELOG.md starter-kit/HANDOFFS.md FRAMEWORK_APPARATUS.md`
  - `grep -nE '65,536|BL-52|read-cap-premise-correction-plan' starter-kit/CHANGELOG.md starter-kit/HANDOFFS.md FRAMEWORK_APPARATUS.md`
  - `grep -n 'context-tax budget' starter-kit/methodology_trim.py`
- **The trimmer only changed comments.** `git diff b82dcff -- starter-kit/methodology_trim.py` changes
  comment lines only (P1's and this one), and the trimmer suite is green.
- **§The Action Ledger states each rule:** the three reads, *optional*, the tool as the only trigger,
  *never in Phase 0*, and conservation. The session's ledger entry quotes each rule's sentence with its
  line number in `FRAMEWORK_APPARATUS.md`, so the claim can be checked by reading.
- **Suites and `bin/check-links` are green.**

**Surface.** As P1. **Cannot enforce:** what *optional* does to ledger growth, which shows only across
later sessions; or the 256 KiB refusal itself, which no test here can exercise (*fork*
`starter-kit/methodology_dashboard.py:284–287` says the same).
**One session. STOP.** Reasoning: the deepest available — this is the rule adopters will run on.

### P3 — Source tags and the audit (C6, C10)

**Scope.**
1. §The Action Ledger's tag text and audit (§3.1 item 3). Pre-vocabulary entries stay as written and are
   not counted.
2. `starter-kit/SESSION_RUNNER.md`:
   - `:39` drops its inline grep for a pointer to the home (net bytes ≤ 0);
   - `:278` and `:329` change `[BL-<N>]` to `[BL-<id>]`.
3. `ITERATIVE_METHODOLOGY.md:294` and `.githooks/pre-commit:57`: the same change.

**DONE.**
- `grep -nF '[BL-<N>]'` over the runner, `ITERATIVE_METHODOLOGY.md`, `HOW_TO_USE.md`, the hook, the home
  and both seeds prints nothing.
- **The audit gives the same count in zsh and bash** (§9.2b):
  - on the branch's root ledger, which has no shards, it equals the heading count;
  - on this repo's 11 shards it gives 494;
  - on each adopter copy it gives the §4.4 figures. A changed figure is a finding: explain it before
    closing.
- **`starter-kit/SESSION_RUNNER.md` is no larger in TOKENS than at P3's start — 18,477.5 tokens**,
  measured on blob `c0550acd` (52,195 B). The instrument is the Read tool's refusal: concatenate the
  file with itself, Read the doubled file with a spanning `limit`, and halve the count the refusal
  prints — so the check is **doubled read ≤ 36,955**. Reproduce a recorded figure before trusting a
  new one; on the same tree the Phase 0 pair doubles to 48,555 (24,277.5 tokens). Bytes are a proxy,
  not the rule: the file's own ceiling (`.context-budget.json`, `max_tokens` 19,200) and the 25,000
  read cap are both written in tokens, and a byte count misprices an edit that trades prose for a path.
- Suites are green.

**Surface.** As P1. **Cannot enforce:** that adopters' future entries use `[BL-<id>]`.
**One session. STOP.** Reasoning: high.

### P4 — Entry lifecycle and the words (C3, C7, C8, C11, C13)

**Scope.**
1. §The Action Ledger items 4 and 5 (§3.1).
2. "Append … newest on top" becomes "prepend … newest on top" at:
   - runner :278, :329, :357;
   - `ITERATIVE_METHODOLOGY.md:294`;
   - `HOW_TO_USE.md` :767, :804;
   - `.githooks/pre-commit:56`.
3. Runner :88 and `ITERATIVE_METHODOLOGY.md:169`: the claim commit carries an *(in progress)* entry, and
   Phase 3F records the rest. Byte-neutral wording.
4. "Completed work history" and its framing become the action ledger at `BOOTSTRAP.md` :23, :107, :131,
   :139, :145, `README.md` :96, :114, :200, and `CLAUDE.md:51`.
5. Upstream's root `CHANGELOG.md` front matter — :11–12, :14 and :34 — in **one commit** (D8 i).

At least three commits.

**DONE.**
- `grep -nE '[Aa]ppends? (a|one) dated|Append the owed entry'` over the runner,
  `ITERATIVE_METHODOLOGY.md`, `HOW_TO_USE.md` and the hook prints nothing.
- `grep -ni 'completed work history'` over `BOOTSTRAP.md`, `README.md` and `CLAUDE.md` finds only history
  (`README.md`'s *What's New*). List what remains, and why.
- §The Action Ledger states every rule in §3.1 items 4 and 5. The ledger entry quotes each with its line
  number, as in P2.
- **Restated at S173, after #82's merge, before any P4 edit — the base is now `upstream/main` `64f23bf`:**
  - **`starter-kit/SESSION_RUNNER.md` is no larger in TOKENS than `upstream/main`'s — 18,865.5 tokens,
    doubled read ≤ 37,731** (blob `2a3e410d`; upstream's recorded figure, reproduced). P4 starts at
    37,703, 14 under.
  - **`CLAUDE.md` is no larger in TOKENS than `upstream/main`'s — 23,482.5 tokens, doubled read ≤ 46,965**
    (blob `1244e95b`, `max_tokens` 23,483). **P4 starts 4 tokens over, at 46,973** — the merge carries P1's
    row — so this criterion fails until P4 pays them back.
  - **`starter-kit/SAFEGUARDS.md` is blob `933816b4`**, `upstream/main`'s.
  - `python3 starter-kit/context_budget.py --status` on the branch tree flips no row against
    `upstream/main`'s, and the read-set total it reports is no larger (§9.7).
  - *Superseded:* the `b82dcff` criterion (doubled read ≤ 36,955 on `c0550acd`), which P3 met at 18,463.5.
- Suites and `bin/check-links` are green, and `python3 starter-kit/quality_ratchet.py --run` passes
  every gate the branch declares (#82's `.quality-gates.json`, merged at S173).

**Surface.** As P1, plus `context_budget.py` on the branch tree. **Cannot enforce:** that the
maintainer's practice changes. Q4 A asks it to; the PR presents the evidence, not a verdict.
**One session. STOP.** Reasoning: high.

### P5 — Fork `main` adopts it

**Scope.**
1. **The port.**
   ```
   git diff b82dcff bl57/changelog-rules -- . ':!CHANGELOG.md' ':!HANDOFFS.md' ':!.context-budget.json'
   ```
   Apply it to `main` with `git apply -3` in commits of at most five files, each with its fork ledger
   entry. `.context-budget.json` is excluded because fork `main` already removed the entry (`3c8acd5`) and
   its blob differs.
   - Resolve the hunks in files where `main` differs from `b82dcff`: `SESSION_RUNNER.md`,
     `BOOTSTRAP.md`, `HOW_TO_USE.md`, `README.md`, `CLAUDE.md`, `bin/_manifest.py`, `bin/tests.sh` and
     `.githooks/pre-commit` (`git diff --stat b82dcff main`).
   - Fork `main` already keys `HANDOFFS.md` on the S41 marker, so only the `CHANGELOG.md` row changes
     there.
2. **This repo's own ledgers.**
   - Root `CHANGELOG.md` front matter: the pointer at :11–12 goes to the home.
   - The audit at :17–20 takes `BL-[^]]+` and the cross-shell form.
   - *When to archive again* (:105–141) becomes the operator's 2026-09-14 decision plus a pointer.
   - A new paragraph records this repo's claim practice (C7): the claim commit carries an *(in
     progress)* entry, and the crash breadcrumb is the pending receipt, because this repo keeps no
     `SESSION_NOTES.md`.
   - Root `HANDOFFS.md:15`: Phase 0 **counts and reports**; the trim is its own action after the report
     (C4).
3. **The hook's claim carve-out (D10).** Remove it (*fork* `.githooks/pre-commit:16–17`, `:53–120`,
   `:144`) and its Test 27 (`bin/tests.sh:1195–1700`), unless the operator keeps it. In that case
   §The Action Ledger must state the exception, and that change travels upstream too.

**DONE.**
- **Identical files stay identical.** Every distributed file that was byte-identical between `main` and
  `b82dcff` when P5 began is byte-identical to the branch's version afterwards (blob equality, §9.6 —
  list them). A project synced from fork `main` then gets exactly the bytes the PR proposes for those
  files.
- **The audit count is unchanged:** 494 in zsh and bash alike, because this repo uses numeric ids only.
- **The carve-out decision is recorded.** If it was removed, a claim commit staging only `HANDOFFS.md`
  is refused. Show it with a real `git commit` in a scratch clone.
- **Fork suites are green** against the fork's baseline (§5.0), less Test 27 if it was removed.
- **`bin/status` from fork `main`** on the six scratch copies reads `CHANGELOG.md` *present (stale
  format)* until each adopter migrates; tracked files read as before, or upgradable.

**Surface.** Fork `main`; suites in a `--no-local` clone; scratch adopter copies. **Cannot enforce:** that
the later resync with upstream is clean. That is a separate task, and fork `main` already conflicts with
`upstream/main` in both ledgers.
**One session. STOP.** Reasoning: high.

### P6–P11 — The adopters (one session each, in that adopter's repository)

Each session is that project's own work, with its own Phase 0, claim, ledger entry and receipt (the
runner's session-notes boundary rule).

1. Run `bin/status` from the source checkout: fork `main` for Route B, the branch for Route A. Decide the
   route from its output; §4.4 is only where to start (S161 §3).
2. Sync the tracked files: a dry run, then for real. Commit the run as one commit, past `SAFEGUARDS.md`'s
   five-file cap: exactly the files the dry run listed, plus that commit's ledger entry, and nothing else
   (item (18), decided at S181).
3. Migrate the `CHANGELOG.md` seed by hand. Replace the rules text or old header — the *block*, with its
   line range recorded before editing — with the thin header, and leave **every entry byte-identical**.
   - **And the `HANDOFFS.md` seed, where step 1 read it *present (stale format)*** (item (21), decided at S186).
     Bring the current `starter-kit/HANDOFFS.md`'s **`## Size, and when to archive`** section in above the first
     real receipt, as `starter-kit/BOOTSTRAP.md:386` says. Since item (24), `bin/status` keys on that section's first
     line, `handoffs-format: 2`; where an older copy of the section is present, replace that section. Otherwise add, don't
     replace: every receipt stays byte-identical, and so do the trimmer's archive-pointer blocks and the *"This
     file currently holds **N**"* sentence where present — the trimmer's regenerated field
     (`starter-kit/methodology_trim.py:337`), which the seed lacks (BL-48), and which `bin/status`'s note told
     adopters to replace until S187 (item (22)). Find the first real receipt fence-aware: an older seed's worked example is a
     `^```handoff` line inside a four-backtick wrapper. Its own commit, so §9.8 checks it.
4. Bring the project's `CLAUDE.md` ledger wording into line, and record any legacy tag format or layout as
   an adaptation.
5. Verify, as below.

**DONE, for each adopter.**
- `bin/status` reads `present` for `CHANGELOG.md`.
- **Only the block changed.** Every line the migration commit removed from `CHANGELOG.md` lies inside
  the recorded block (§9.8).
- **The heading count moved as predicted:** `grep -c '^### ' CHANGELOG.md` changed by (the migration's
  own entries) minus (the block's own `### ` lines): 5 in `wsfct`, 2 in `nprcgenekeepr`, 0 elsewhere.
- **The audit count moved as predicted:** it fell by the block's examples that matched it (`wsfct`: 3,
  so ~~130 → 127~~ 132 → 130 with its 1 entry, re-measured at P7) and rose by the migration's own entries.
- **Where `HANDOFFS.md` was stale:** `bin/status` reads `present` for it; §9.8 on that commit, with the insertion
  line as both bounds and `HANDOFFS.md` as its third argument, prints *only the block changed* (an insertion
  removes nothing, so a removed line is what it catches); and the trimmer's dry run
  (`python3 methodology_trim.py --file HANDOFFS.md --cut 1 --force`, no `--write`) prints `L1_OK`, `L2_OK` and
  `L3_OK`, so the new front matter still classifies.
- The project's own build or test command still passes; the change touches documents only.

**Surface.** The adopter's repository, in its own session. **Cannot enforce:** that its later sessions
follow the rules. Pushing, or opening a PR there, is that project's own go-ahead.
**One session each. STOP after each.** Reasoning: high for P10 and P11, each of which starts with a
decision; medium otherwise.

| Phase | Adopter | Specifics |
|---|---|---|
| P6 | `airqino` | **DONE 2026-09-17, recorded at S180 (the P6 block, items (16)–(18)).** BL-56 folds in: reseed from the thin seed and carry its ~~one entry~~ entries (two by then; the header was migrated by hand) across, unchanged. ~~Route A from the branch, because its files are the branch's versions; from fork `main`, BL-54 refuses four files.~~ Route B, since S179 fixed BL-54. ~~It is on `chore/methodology-read-set-budgets`, off open PR #1~~ Landed on `chore/methodology-bl57-p6`, taken from that branch's `1402ad4` |
| P7 | `wsfct` | **DONE 2026-09-17 in that repository and MERGED there (PR #903, squash `66e14daa`); recorded here at S185 (the P7 block, items (19)–(21)).** At the claim, check first that `wsfct` is clean, with no other session's claim staged or uncommitted (at S181 its own S629 had one staged). At fork `main` `b0bf91f` the dry run exits 0 and would write 14 files; it ran from `29b0feb`, 14 files, `8a41741c`. Replace the older full seed copy (block ~~:13–196~~ **:8–182**, re-derived at the claim; 5 `### ` lines) with the thin header, `12fb758e`. Route B. `CLAUDE.md` :43, :218, :695 (*"Completed work history"*) and :162, :206 (completed-work framing), `8d0e696a` |
| P8 | `vscode_quarto_ext` | **DONE 2026-09-18 in that repository (Session 264, `48d1790c`..`57750bb2`, not pushed); recorded here at S191 (the P8 block, items (25)–(27)).** Replace the Keep-a-Changelog header (:1–8) with the thin header, keeping the shard pointer. Record the `[BACKLOG: …]` entries as legacy in `CLAUDE.md`. Drop `CHANGELOG.md` from its `.context-budget.json` (Q2 A; the project's call). Route B. `CLAUDE.md` :102, :146. **`HANDOFFS.md` is stale too (item (21)).** Read at S186 on `58f7bcbd`, to re-derive at the claim: the first receipt is at :33, below the pointer block (:29–31); the section goes in above that block. The count sentence (:20–22), the pointer block and the project's own *fence-aware* warning (:23–27) all stay |
| P9 | `mts-system` | **DONE 2026-09-18 in that repository (Session 139, `a48f543`..`b8a20ce`, ~~not pushed~~ pushed 2026-09-19, the P9 block); recorded here at S193 (the P9 block, items (28)–(29)). One remainder: the superseded rules block at :782, item (28), filed there as CLEANUP-006.** Add the pointer and marker under its title and intro (:1–8); its 165 non-numeric `[BL-…]` entries now conform. Route B. Its hook is on, so every commit carries an entry. `CLAUDE.md` :152, :182, :189. **`HANDOFFS.md` is stale too (item (21)).** Read at S186 on `710a0f7`: the first receipt is :77, and the section goes in above it. The first `^```handoff` match (:32) is the old seed's worked example inside a four-backtick wrapper (:31–55), not a receipt. No count sentence, no pointer block. The file is 373,021 B, past the 262,144 B read refusal. **Found, not a P9 effect:** the fence opened at :216 (`session: S131`) never closes before the next at :219, and `bin/check-handoff --all --file ../mts-system/HANDOFFS.md` reads them as one block (*"first two keys must be `session` then `date` (got session, session)"*). Check it before P9, and don't attribute it to P9 **S192, at `710a0f7`: the same shape recurs at `:320` (`S126`) and `:671` (`S106`), three in all; `--all` reports `:216` and `:671` only, since `:320`'s `date:` precedes its second opener (BL-73).** |
| P10 | `nprcgenekeepr` | **DONE 2026-09-19 in that repository (Session 719, `74243f04`..`4565c39d`, not pushed); recorded here at S194 (the P10 block, items (30)–(31)).** **DECIDED at S194 (operator, picker): `--force` the sync, then re-apply the extension in its own commit** (measured in a scratch clone: the patch applies onto trimmer 1.5.0 and its `SESSION_NOTES.md` dry run matches the old copy's). **Launch prompt, with the facts measured at `312996b0`: [`bl57-p10-nprcgenekeepr-launch-prompt.md`](bl57-p10-nprcgenekeepr-launch-prompt.md).** ~~**Decide first.**~~ Its 49-line local extension of `methodology_trim.py` blocks every sync, because one modified file refuses the whole run. Three options: send the extension upstream; migrate the seed only and leave the pointer dangling until it can sync; or `--force`, which discards the extension. ~~Then replace the rules block (:3946–:4065, 2 `### ` lines, between two runs of entries)~~ **The block has left the live file** (its S702 trim, `6bac092f`, moved it into the frozen `docs/archive/CHANGELOG-through-2026-09-17.md`, `:4171`), so the `CHANGELOG.md` step is a pure insertion of the pointer and marker. Then record the S325 legacy block and September's `## 2026-08` placement in `CLAUDE.md` (:271) |
| P11 | `model_project_constructor` | **Decide first.** (a) Its runner customization (step 5) moves into `CLAUDE.md` Adaptations before any `--force` sync (*fork* `BOOTSTRAP.md:75`). (b) Its ledger is a release-grouped work log of 143 untagged `### date — …` entries, which the trimmer refuses by design: either adopt the action-ledger format going forward (the S325 *"freeze legacy, go forward"* precedent) or record an adaptation. It has no `HANDOFFS.md` and no trimmer today. **S192, after close-out (the operator asked why it has no `HANDOFFS.md`), read-only at `a18706f`: `bin/sync --dry-run` exits 2 before writing anything, refusing `SESSION_RUNNER.md` and `SAFEGUARDS.md`, so no seed has reached it since the receipt shipped (`4f0bea7`, 2026-07-08); its runner never mentions `HANDOFFS.md`. The runner's local edits are three, not one:** step 5, the task-to-workstream table (seven project rows in place of four canonical ones) and a *Wiki sync* paragraph (which `CLAUDE.md:75` already corrects). They are 10 lines of the 29 that differ from the closest canonical version (`7073dec`, 2026-04-07); the other 19 are later canonical text grafted in. `SAFEGUARDS.md` differs from `3d648ab` by one line. (a) must move all three before any `--force` |

### P12 — The upstream PR (after #80 merges; outward, its own go-ahead)

**Preconditions.** #80 is `MERGED` — if it is still open when the branch is ready, ask the operator:
wait, or a stacked PR against `read-set-budgets`. P1–P5 are done. Adopter migrations are not a
precondition.

**Steps.**
1. Fetch, and compare #80's merged content with `b82dcff`. Re-derive anything it changed in a file this
   plan touches.
2. Run `git merge-tree --write-tree --name-only upstream/main bl57/changelog-rules`, then bring the branch
   onto `upstream/main` (merge or rebase — the operator's choice then). **Merge, decided at S188 (item (23)).**
3. Dry-run `bin/sync` from the branch into scratch copies of all six adopters. Record, per adopter, the
   files it would change and the refusals that already existed (S161 §3).
4. Run the suites in a `--no-local` clone. Re-run §9.1: no contradiction sites should remain.
   `SESSION_RUNNER.md` must be no larger than on `upstream/main`.
5. Draft the PR body:
   - the sixteen findings, before and after;
   - the four decisions;
   - the adopter results;
   - the conservation definition for the proposed count ratchet;
   - D8's two commits and what dropping each would cost;
   - *no Learning row, no failure-mode change*.
6. Ask the operator for the go-ahead to push the branch to `origin` and open the PR.

**DONE.** `gh pr view <N> --repo KJ5HST/methodology --json state,url` reads `OPEN` and the URL is
recorded; a ledger entry records the PR open (a non-commit action); this fork has merged nothing.
**Surface.** GitHub. **Cannot enforce:** the maintainer's decision, or what the merge method does to fork
`main` (S161's unanswered part (b)).
**One session. STOP.** Reasoning: the deepest available.
**Done at S189:** [PR #84](https://github.com/KJ5HST/methodology/pull/84) is OPEN; see item (24).

---

## 6. Hazards

1. **Upstream moves while this runs.** Re-fetch at every Phase 0. If #80's head moves past `b82dcff`
   before P1, start the branch from the new head; after P1, merge the new head into the branch and re-run
   the suites. Re-derive any self-referential number at publish time (*fork* Learning #61).
2. **The maintainer's queue shares two files (K3).** In `SESSION_RUNNER.md`, quality-ratchet Phase 1
   edits the FM #17 row, the Degradation table and Phase 3C routing, while this plan edits :39, :88, :278,
   :329 and :357 — and :357 sits inside that Degradation table. In `BOOTSTRAP.md`, the S16 follow-up edits
   Step 10, while this plan edits :23–:145. Compute the conflicts with `git merge-tree` at P12; do not
   predict them.
3. **The Phase 0 read has no spare bytes (K2).** Every runner edit is net ≤ 0; the rules' detail goes to
   the home, not the runner.
4. **The seed fixtures read `HEAD:`** (`tools/test_methodology_trim.py:1692–1693`), not the working tree.
   Commit inside the clone before running them.
5. **A `.replace()` whose anchor is gone passes silently** (`:1824`). Assert the anchor's count first.
6. **A control that asserts the live seed has a property breaks when the seed changes** (`:238–253`,
   `:2027–2035`). Move such controls onto frozen fixtures before changing the seed.
7. **`bin/tests.sh` rewrites both live ledgers.** Run it only in a `--no-local` clone, never the live tree.
8. **zsh aborts on an unmatched glob** (K8). A shard glob with no shards prints *"no matches found"* and
   runs nothing, so a count reads 0. Use `$(git ls-files '<pattern>')`.
9. **A proposed count ratchet (C9).** If upstream ships one before P12, check that it counts across the
   shards, or every trim fails. Say so in the PR body either way.
10. **Adopter ledgers past 256 KiB** (`model_project_constructor`, `mts-system`, `nprcgenekeepr`). Read
    them with offset/limit; a default read returns nothing.
11. **BL-54.** From fork `main`, `bin/sync` cannot see versions that exist only on a merge's other side.
    That is why `airqino` syncs from the branch.
12. **A `--no-local` clone copies only this repo's branches.** To test `b82dcff` in one, fetch the ref
    first (`git fetch <repo> refs/remotes/upstream/read-set-budgets`). This plan's first baseline attempt
    failed on exactly this, and its `&&` chain then skipped the suite silently.
13. **zsh history modifiers.** `$R:path` is one; it cost a call while taking this inventory. Run loops over
    refs and paths in `bash` or Python.
14. **Learning numbers diverge (K4).** The PR adds no Learning row; this fork's own learnings go to fork
    `main` only.

---

## 7. Alternatives considered, beyond §2.1

| Alternative | Why not |
|---|---|
| Add BL-57's commits to PR #80 | #80 is under private review with a decision (F1) and fixes (F2, F3) pending. Moving its head mid-review costs the maintainer a re-review, and K6 makes it its own go-ahead anyway |
| A stacked PR against `read-set-budgets` now | Reviewable sooner, but it asks for review of a branch whose base is itself unmerged. Kept as an option at P12, only if #80 is still open |
| Migrate adopters only after the upstream merge (D6) | Clean provenance, but it leaves six projects on contradictory rules for as long as review takes. With thin seeds, a change made in review reaches them by sync, so migrating early costs nothing twice |
| Key `CHANGELOG.md` on an HTML comment (D9) | Easy to delete along with the sentinel comment beside it. A token on the pointer line survives, because the line is the pointer |
| Keep keying on the titles (D9) | They never change, so the check cannot fire — Learning #19, which `b82dcff` itself ships |
| Build the heading-count ratchet in this PR (C9) | It is the maintainer's own queued item (S17 receipt). This plan supplies the definition it needs and does not pre-empt it |
| Extend Q2 A to `HANDOFFS.md` (D7) | The operator has not decided it, and `HANDOFFS.md` carries a retention policy here and more tooling than `CHANGELOG.md`. Left open (§8). **Decided for `vscode_quarto_ext` at S191: keep it budgeted** (the P8 block, decision (a)); open for the other adopters |
| Keep the fork hook's claim carve-out (D10) | It exempts exactly the commit Q4 A gives an entry, and neither current practice uses it. Kept as the operator's option at P5 |
| Also fix the four code comments that cite fork-only material | They are in #80's own content (§8), not BL-57's rules; P2's check is scoped to the files BL-57 rewrites |

---

## 8. Out of scope, and follow-ons

- **Trimming this repo's `CHANGELOG.md`** — the operator decided not to (2026-09-14).
- **`HANDOFFS.md`'s own archive rule** (D7), and every adopter's `HANDOFFS.md` copy of the shared size
  section. They carry the same premise error, left for a follow-on the operator may raise.
- **A project whose `CHANGELOG.md` is a product changelog** (`model_project_constructor`, and
  `vscode_quarto_ext`'s header). The framework has no documented path for one. P11 decides locally; the
  framework-level question is a follow-on.
- **A permanently red `--check`.** Under Q2 A, `methodology_trim.py --check` keeps exiting 1 on a large,
  deliberately unarchived ledger, and an always-red check cannot report a new problem. A follow-on could
  let a project declare a ledger unarchived.
- **Retagging old entries anywhere** — never (Q4 A).
- **Separate items:** BL-54; BL-55's gate (its join key gains from Q3 A); the fork dashboard's read-cap
  row for `CHANGELOG.md` (BL-52); the fork's resync with upstream.
- **Found and not fixed:**
  - Four comments in two distributed tools cite fork-only material: `methodology_trim.py:201`, `:818`,
    `:821` and `context_budget.py:683`. They arrived with #77 and #79.
  - `docs/tutorials/T2_worked_transcript.md:228` writes `changelog_ref: CHANGELOG.md [BL-F1] entry`,
    not the quoted-heading form the `HANDOFFS.md` seed asks for (:63).

---

## 9. Commands

### 9.1 The inventory (run from the repo root)

```python
import subprocess
refs = {'main': 'main', 'up': 'upstream/main', 'pr80': 'b82dcff'}
pats = [r'changelog', r'ledger', r'prepend', r'newest[- ]on[- ]top', r'append',
        r'65,?53[56]|196,?60[78]|262,?14[34]|98,?30[34]|56,?750', r'CLASS_A|READ_REFUSE|DEFAULT_BUDGET',
        r'source[- ]tag|ad hoc\]|\[BL-', r'SEED_FORMAT|Authoritative Action Ledger|when to archive',
        r'context-tax|watched', r'reconcile', r'\btrim']
excl = [':!CHANGELOG.md', ':!HANDOFFS.md', ':!docs/archive', ':!docs/planning',
        ':!docs/RELEASE_HISTORY.md', ':!dashboard.html', ':!*.jsonl', ':!LICENSES']
for k, r in refs.items():
    args = ['git', 'grep', '-n', '-I', '-i', '-E'] + sum([['-e', p] for p in pats], []) + [r, '--', '.'] + excl
    out = subprocess.run(args, capture_output=True, text=True).stdout
    print(k, len(out.splitlines()), 'lines in', len({l.split(':')[1] for l in out.splitlines()}), 'files')
```

### 9.2 Conformance under the current rule and under Q3 A

(a) The §4.4 figures, over the live ledger and its shard files:

```bash
bash <<'EOF'
NEW='^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[(issue #[0-9]+|BL-[^]]+|ad hoc)\]'
OLD='^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[(issue #[0-9]+|BL-[0-9]+|ad hoc)\]'
for d in methodology airqino model_project_constructor mts-system nprcgenekeepr vscode_quarto_ext wsfct; do
  p=$HOME/Development/$d; files="$p/CHANGELOG.md $(ls $p/docs/archive/CHANGELOG-*.md 2>/dev/null | grep -v verify)"
  echo "$d $(cat $files | /usr/bin/grep -c '^### ') $(cat $files | /usr/bin/grep -cE "$OLD") $(cat $files | /usr/bin/grep -cE "$NEW")"
done
EOF
```

(b) The published form, in each shell. The two outputs must agree; they did at S162, 43 on `b82dcff`,
which has no shards, and 494 on this repo.

```bash
P='^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[(issue #[0-9]+|BL-[^]]+|ad hoc)\]'
zsh  -c "cat CHANGELOG.md \$(git ls-files 'docs/archive/CHANGELOG-*.md') | grep -cE '$P'"
bash -c "cat CHANGELOG.md \$(git ls-files 'docs/archive/CHANGELOG-*.md') | grep -cE '$P'"
```

### 9.3 P1 — the move is verbatim

```python
import re, subprocess
seed = subprocess.run(['git', 'show', 'b82dcff:starter-kit/CHANGELOG.md'], capture_output=True, text=True).stdout
home = open('FRAMEWORK_APPARATUS.md', encoding='utf-8').read()
def demote(text):                       # one level down, outside fences only
    out, fence = [], None
    for line in text.split('\n'):
        m = re.match(r'^(`{3,}|~{3,})', line)
        if m and fence is None: fence = m.group(1)
        elif m and line.startswith(fence): fence = None
        elif fence is None and re.match(r'^#{2,5} ', line): line = '#' + line
        out.append(line)
    return '\n'.join(out)
starts = [m.start() for m in re.finditer(r'(?m)^## ', seed)] + [seed.index('\n---\n', seed.rindex('## '))]
for a, b in zip(starts, starts[1:]):
    sec = demote(seed[a:b].rstrip('\n'))
    print(sec.split('\n')[0], 'VERBATIM' if sec in home else 'MISSING')
```

At S162 it printed MISSING for all three on today's file, VERBATIM on a correct home, and MISSING for
each of four mutants: a one-character change inside each section, and one heading left undemoted.

### 9.4 P1 — the marker discriminates

```bash
M='ledger-format: 2'     # whatever token P1 settles on
git log --all --format=%H -- starter-kit/CHANGELOG.md | while read c; do
  git show "${c}:starter-kit/CHANGELOG.md" 2>/dev/null | grep -qF "$M" && echo "$c"
done                     # must print only P1's commit and later ones
```

*(S167: the braces are load-bearing. The first published form, `"$c:starter-kit/…"`, printed nothing in
zsh; at S167 the braced form printed only `b0634606` of nine versions.)*

### 9.5 The distributed files

```bash
python3 -c "import sys; sys.path.insert(0,'bin'); import _manifest as m; print('\n'.join(s for s,_,_ in m.DISTRIBUTION))"
```

### 9.6 P5 — the files identical at the start (run before porting)

```bash
bash <<'EOF'
python3 -c "import sys; sys.path.insert(0,'bin'); import _manifest as m; print('\n'.join(s for s,_,_ in m.DISTRIBUTION))" |
while read f; do
  [ "$(git rev-parse "main:$f" 2>/dev/null)" = "$(git rev-parse "b82dcff:$f" 2>/dev/null)" ] && echo "$f"
done
EOF
```

### 9.7 The budget on any tree

```bash
S=$(mktemp -d)
T=$(git merge-tree --write-tree upstream/main bl57/changelog-rules | head -1)   # or a ref
git archive "$T" | tar -x -C "$S" && (cd "$S" && git init -q && python3 starter-kit/context_budget.py)
```

### 9.8 P6–P11 — only the recorded block changed

```python
# usage: python3 check_block.py <first_line> <last_line> [<file>]   (the block, as recorded before editing;
#        <file> defaults to CHANGELOG.md — pass HANDOFFS.md for item (21)'s migration, added at S186)
import re, subprocess, sys
lo, hi = int(sys.argv[1]), int(sys.argv[2])
path = sys.argv[3] if len(sys.argv) > 3 else 'CHANGELOG.md'
diff = subprocess.run(['git', 'diff', '-U0', 'HEAD~1', 'HEAD', '--', path],
                      capture_output=True, text=True, check=True).stdout
bad = []
for m in re.finditer(r'^@@ -(\d+)(?:,(\d+))? ', diff, re.M):
    start, count = int(m.group(1)), int(m.group(2) or 1)
    if count and not (lo <= start and start + count - 1 <= hi):
        bad.append((start, count))
print('only the block changed' if not bad else f'lines removed outside the block: {bad}')
```
