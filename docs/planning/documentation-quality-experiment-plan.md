# Plan: does v3.8 leave better documentation than v3.0?

**Status: DRAFT for operator approval (BL-94, S255, 2026-10-03), recomposed twice after two independent read-only reviews the same
session (§11).** Written as the session's one deliverable. Nothing here has been run: no model session was launched, no money was
spent, no distributed file changed, nothing was sent upstream. **After the S255 close-out the operator ratified D1 to D3 as recommended,
set $100 as this study's spend cap and said he will do the blind rating himself (D4, D5; his words in §7).** A phase still starts only
when he says go in a session, one phase per session. **S256 (2026-10-03) did P1a** (evidence kept, scorer built and frozen; status under §5 P1a), **S257 (2026-10-04) did P1b** (the saved runs scored once: a null at the ceiling), and **S258 (2026-10-04) did P2a** (the probe built and tested at $0; status under §5 P2a). The next phase is **P2**, the first spend, which is his decision (D4) and its own session.

## In plain words

**The question.** The operator asked on 2026-10-01 (S244): *is there evidence that self documentation and documentation
management is better in 3.8 than in 3.0?* The answer then was: no direct evidence either way. This plan says how to get some,
what it would cost, and what each outcome would and would not mean.

**What this session found, and why it shapes the design.** Each finding was re-derived from files; the commands and their output
are in §10. The first draft of this plan mislabelled the saved runs; the second still ignored a set of v3.8 runs already on disk;
both were corrected by the reviews in §11.

1. **The ratchet study's 15 T-remove trees cannot separate the arms cleanly.** Every arm, v3.0 included, wrote a complete
   handoff receipt (13 to 16 fields) and added ledger entries, because the project's own `CLAUDE.md` at that start commit
   (33,848 B) carries those rules and the overlay replaces only the framework's files. One v3.0 run wrote into its receipt that the
   v3.0 install had *dropped rules the project's `CLAUDE.md` still cites*. There is still a small gap in the direction the
   framework predicts: v3.8 arms added 4.4 ledger entries per run against 3.0 (n=9 against 5; one R0 run holds two sessions and
   is left out; Welch t = 2.70, unadjusted, reproduced by the reviewer) and 8 of 9 made a reconcile or backfill commit against 2 of
   5 (Fisher p = 0.095). Both are confounded by the project's rules and by the harness's own install commit, which is in every arm.
2. **Three versions have already been run on a start state with no documentation rules, and none was ever scored for
   documentation.** `nprcgenekeepr` at `879503cce` has a 9,172 B `CLAUDE.md` with **zero** mentions of `HANDOFFS`, ledger,
   reconcile, receipt, ghost or `CHANGELOG`, and a 3.85 MB notes file. On it, on the same task (issue #121): **v3.0** (S237: five
   runs reached a close-out, 5 of 6 rows), **v3.7** (S237: six of seven rows), and **v3.8's text** (the ratchet study's T-control
   batches: R0 n=3 and R1 n=5+5, 13 runs, mean $3.45). The v3.0 runner has `CHANGELOG: pending`, `reconcile` and `HANDOFFS.md` 0, 0
   and 0 times; v3.7's has 4, 16 and 11; v3.8's has 4, 14 and 8. **Scoring these costs $0** and is the plan's first step. It is a
   confounded comparison (§3.3: the T-control runs used different scripted replies and R1 carries the ratchet hook), which the plan
   names rather than hides.
3. **v3.7 is a stand-in for v3.8's ledger, receipt and reconcile machinery, not for all of it.** Between them v3.8 adds the
   trimmer `methodology_trim.py` (+2,181 lines, new), the ratchet (+592), changes to `context_budget.py`, moves the learnings out of
   the always-read runner (v3.7's carries all 13 inline, including the one about staleness outside a diff; v3.8's is a pointer to an
   on-demand sibling), and cuts 333 lines from the manual (adding 54). The "32 diff lines" I first quoted for the two runners understates this.
4. **The runner text splits the question.** The sentences about writing accurate claims (re-read before claiming, never write
   "need to verify", verify cross-references, key files, gotchas, evaluate the predecessor's handoff) are present, and read
   identically, in v3.0 and v3.8. What v3.8 adds is on the management side: the ledger, the `CHANGELOG: pending` marker, the durable
   receipt, reconcile-on-read, backfill, a size ceiling. This is from the runner only (§2.1 lists what was not compared).
5. **The start state is an untrimmed record, which is a stress test and a confound.** The notes file is 3,850,762 B at `879503cce`
   (3,938,380 B in 11,738 lines at S323, ten commits later; 15 times the 262,144 B at which this repository's own rule says a
   default read returns nothing). The v3.8 trimmer has a spec for `CHANGELOG.md` and `HANDOFFS.md` only, so the notes file has no
   tool; and the pre-upgrade ledger is in a legacy format. Costs at this record size are already measured, which the first draft
   said they were not.
6. **No living document goes stale at these start states.** I first took `inst/_pkgdown.yml` (which names the two helpers the
   ratchet study's removal task deletes) for a living file. It is dead: the project's own commit `d14cd913d` (S354) says a root
   `_pkgdown.yml` shadows it and it was never read. The other places that name the helpers are historical records, dated plans and
   a generated summary. A staleness measure needs a task that does not exist yet, and that task needs its own start state (§3.4).
7. **Loose counts mislead; the framework's own score is compressed.** BL-94 reports "a `status: pending` receipt stayed pending in
   most trees"; counting fenced receipt blocks in the final `HANDOFFS.md` gives **2 of 15**, both the start-state's orphan stub.
   Of 271 `predecessor_score` values in this repository's receipts, 266 (98%) are 7, 8 or 9; none is 10.

**What the plan proposes, in order of cost.** **P1 ($0, two sessions):** keep the perishable evidence, define the measures, build and
test the scorers, calibrate them on the T-remove trees, freeze them, then score the saved v3.0, v3.7 and v3.8-text runs once. That is
the first answer, and the plan stops there for the operator's decision before any spend. **P2a ($0), P2 and P3 (money, his figure):**
run a **cold-start probe** on saved end states, because only a new session can show whether the record *works for a successor* and
what it adds beyond what git already says, plus a blind model rater for what no script reaches. New *task* runs are needed only if
P1 shows the saved v3.8-text runs cannot be pooled. Estimated model spend: a cap of $10 for the pilot (about $6 expected) and about
$38 for the main probes, plus about $28 only if new v3.8 runs prove necessary (§5): **about $76 at most, against the $100 the
operator set for this study on 2026-10-03** (§7, D4; he said to ignore the earlier caps, so the $20.94 and $15.39 headroom figures
of the earlier drafts no longer apply to it).

**What it will not tell us** (§2.4): anything about long-run growth of the record (that needs the session chain, §3.6), another
model, another project, which v3.8 feature produced a difference, or anything about live-document staleness until a task for it
exists.

**BL-94 listed five things a plan must decide; where each is answered:** what the measures are, §2; who or what scores, §4; which
design, §3 (its option (a), the session chain, is §3.6 and is deferred; option (b), the cold-start resume test, is §3.5 and is the
core; option (c), blind rating of existing trees, is P1, because the saved runs are a usable contrast); what the arms must differ
in, §3.2 and §3.3; spend, §7 D4, which is the operator's.

---

## §1 What exists, and what it cannot answer

**Known before this session** (BL-94 in [`BACKLOG-DETAIL.md`](BACKLOG-DETAIL.md), re-derived here):

- S237's process-rigor indicators (`overhead-replay/rigor_score.py`) test whether a step *appeared*; they were at ceiling for both
  versions ([`real-3.7/RESULTS.md`](overhead-replay/pilot/real-3.7/RESULTS.md)). They say nothing about quality.
- The ratchet study ([`ratchet-mechanism-test-report.md`](ratchet-mechanism-test-report.md)) scored what sessions leave true about
  *quality gates*. It did not score documentation.

**Three sets of saved runs hold documentation outputs, and they are different instruments:**

| Set | Start state | Arms | Runs | Project's own documentation rules at the start | Use |
|---|---|---|---|---|---|
| ratchet study, T-remove | `402a6b5b` | v3.0, R0 (v3.8 without ratchet), R1 (v3.8 with) | 5 each (R0 rep 5 holds two sessions) | **present** (`CLAUDE.md` 33,848 B with ledger, reconcile and ghost rules) | negative control and noise floor (P1) |
| S237 real project, issue #121 | `879503cce` | v3.0, v3.7 | 13 rows: v3.0 5 reached a close-out, v3.7 6 (`complete` flag) | **absent** (`CLAUDE.md` 9,172 B, nine terms all 0) | contrast (P1) |
| ratchet study, T-control, issue #121 | `879503cce` | R0 (v3.8 text, no ratchet), R1 (v3.8 text, ratchet hook) | 13: R0 n=3 and R1 n=5 with the old close-out reply, R1 n=5 with the fixed reply | **absent** (same start commit) | v3.8 text on the same task (P1), with caveats in §3.3 |

**Reusable harness** (`overhead-replay/`; the ten files `driver.py`, `stakeholder.py`, `extract.py`, `replaylib.py`,
`install_arm.py`, `real_project.py`, `ratchet_arms.py`, `fixture.py`, `scorers.py`, `held_out.py` total 1,109 lines; file map in its
`README.md`): `real_project.py` builds an arm from a real project at a fixed commit with only that commit and its ancestors
reachable; `install_arm.py` lays a tag's files over it; `driver.py` drives `claude -p` with a scripted stakeholder;
`stakeholder.py` holds the scripts; `extract.py` and `replaylib.py` turn a transcript into a row of cost and behaviour. `held_out.py`
is hard-wired to S237's trees (`RUNS`, `/tmp/overhead-real/...`); the reusable entry for held-out tests is
`ratchet_arms.held_out_task(tree, task)` (`:122`), which has a `t-control` entry for issue #121. **`erosion_score.py` and
`remove_score.py` are frozen (BL-94's instruction) and stay untouched.**

**Not built, each is work in P1, P2a or P4:** a documentation scorer; a cold-start probe, its answer-key builder, and a driver mode
that runs a fresh session in a clone of an *existing* end state at a pinned sha (the driver always builds its arm first; its
`--max-stops` option already exists, so a one-turn probe needs no new stop logic); a chain driver.

**Perishable evidence.** The run trees live in `/tmp` and are deleted at the next reboot (the machine had been up 11 days):
`/tmp/ratchet-main` 2.5 GB, `/tmp/ratchet-control` 1.1 GB, `/tmp/ratchet-control-v2` 665 MB, `/tmp/overhead-real` 1.8 GB. The
transcripts are not at risk: 51 run directories, 72 MB, across `~/.claude/projects/-private-tmp-ratchet-*` and
`…-overhead-real-*`, with `cleanupPeriodDays` 365. P1's first step keeps the evidence of the trees.

---

## §2 Constructs and measures, defined before any scorer exists

### 2.1 The two constructs

| Construct | Meaning here | Where v3.0 and v3.8 differ |
|---|---|---|
| **Self-documentation** | what one session writes about its own work and what comes next: accurate, specific, checkable | **In the runner, almost nowhere.** The accuracy sentences are in both, and the text of the seven phrases counted in §10 row 4 is identical in the two runners (confirmed by the first reviewer). **Not compared:** v3.8's sibling `FRAMEWORK_LEARNINGS.md` (on demand; v3.7 had the same learnings inline in the always-read runner, so the *placement* differs), the workstream documents, `ITERATIVE_METHODOLOGY.md` (333 lines cut and 54 added at v3.8) |
| **Documentation management** | whether the record stays true to git and stays bounded: every action recorded, no stub left behind, a crashed session found by the next, growth controlled | **Throughout.** The durable receipt, ledger entries, `CHANGELOG: pending`, reconcile-on-read, backfill, the unrecorded-action and unbounded-read failure modes, the size ceiling, and (v3.8 only) the trimmer |

### 2.2 The unit: a session's *record*

The record is the set of lines the session **added** to tracked files that are neither code nor tests nor generated (R sources,
`man/`, `NAMESPACE`, test files and `test_results_summary.md` excluded), across the commits from the install base to the **pinned end
sha** (§2.5), plus the session's final message. **Moved lines are excluded:** an added line is dropped from the record when the same
line (whitespace-stripped) is *deleted* from some file in the session's own commits, because a session that archives or splits an
oversized file, as the v3.7 and v3.8 runners tell it to, moves history and a moved line is not a new claim. A line copied
verbatim from the base *without* being deleted elsewhere stays in the record: that is a claim the session chose to carry forward,
and counting it is how a stale next step copied forward gets seen. It is defined by the diff, not by file name, because v3.0 puts
the handoff in `SESSION_NOTES.md` and v3.8 puts it in `HANDOFFS.md`. **Commits at or before the install base are out of scope for
every measure.**

### 2.3 The measures

| # | Measure | Definition | Tier |
|---|---|---|---|
| **M1** | Checkable-reference accuracy | In the record, extract (a) commit shas, (b) file paths, (c) `path:line` anchors, (d) test-count statements. Score each: sha resolves and is reachable from the pinned end sha; path exists there (or is stated as removed); anchor line is within the file **and, when a backticked identifier sits beside the anchor, that identifier occurs within five lines of it** (a bare line-in-range test is nearly vacuous); a stated count equals a re-run. **(d) is new work:** the frozen scorer's R-d (`erosion_score.claim_mismatches`) only tests an unqualified "all tests pass" against net failures; it is reused read-only, not extended. (d) is the only part that needs the R suite, so if one run is long (P2a times it) it is applied to a sample and the report says so. Report accuracy = verified / checkable **and** the checkable count. **Ceiling rule:** if M1 sits at or above 0.95 in every saved run, it is reported as uninformative and is not a headline. (A crude regex of mine over 26 saved trees found 134 of 152 distinct cited shas resolving and 545 of 560 backticked paths existing, §10 row 33; the unresolved shas may be regex noise, unread. The reviewer's smaller look found none unresolved.) | mechanical |
| **M2** | Action coverage and stub resolution | Reported as **separate parts, never summed**, because the arms do not have the same things to score: (a) every commit the session authored (install base excluded) is named in the record by sha or by its subject; (b) no receipt with `status: pending` and no `CHANGELOG: pending` marker the session itself wrote is left. **(b) is defined only where the version has such an artifact; v3.0 has neither, so for it (b) is "not applicable", not a pass.** The `commit:` slot is not scored: `bin/check-handoff:54` says it "may legitimately read `pending`" (7 of the 15 newest T-remove receipts do), and it is reported as a descriptive count; (c) the record says the deliverable is done only when the task's own check says so (for issue #121, `ratchet_arms.held_out_task`) | mechanical, except that "says done" is a keyword rule fixed in P1a |
| **M3** | Staleness handled | **Not run until a task exists** (§3.4). Count live documents still naming the removed thing, and whether the record discloses them (a keyword rule fixed beforehand, hand-read). **History rewritten** = a line present in a historical file at the base that the session removes or changes, **except** the session's own pending stub being overwritten and lines moved (§2.2). Both runners tell a session to add to and update `SESSION_NOTES.md`, `HANDOFFS.md` and `CHANGELOG.md`, so additions and the stub overwrite are never "rewriting" | mechanical, except "discloses" |
| **M4** | Cold-start reconstruction | A fresh session, in a clone of session 1's end state at the pinned sha, opens with the operator's own "go" and produces the Phase 0 report the runner demands. Facts keyed from the tree and git: the previous session's number, its deliverable, the deliverable's commit sha, whether the work is complete, uncommitted changes. **Those are recoverable from git alone**, so they are scored as the *git-derivable* facts, and a **git-only control** (the same end state with the record files reverted to their base text) is probed on a sample: M4 is the score with the record minus the score without it. A *record-only* fact is scored separately: the fraction of the paths and shas the record names under its key-files and next-steps parts that the cold report names. The v3.7 and v3.8 "ledger or ghost finding" has no v3.0 counterpart, so it is reported on its own line and is in no arm's denominator. Cost is split into reads of the record and reads of framework files | mechanical, plus cost |
| **M5** | Blind usefulness | A model rater, shown only the record, answers a fixed list of yes/no checks (for example: "does it name the next step specifically enough to act without reading code?") and is asked to guess the arm. Reported **last**, never as the headline. Each rater call is capped by its own `--max-budget-usd`, because the driver does not enforce a cap on it | judged |

**"Mechanical" means a script decides it from the tree and git, with the two keyword rules named above as the only places a reading
is built into a rule.** **Not measured, on purpose:** prose quality as such; record length (a covariate on M1 and M5); S237's process
presence (kept for continuity only).

### 2.4 Hypotheses, with the result expected stated now

| # | Hypothesis | Expected, and why |
|---|---|---|
| H1 | v3.7 and v3.8 records are more accurate against the tree (M1) | **No difference.** The same accuracy sentences are in both runners (§10 row 4); only forward-looking claims have a rule that differs, and M1 does not score them. M1 may also sit at ceiling (§2.3). A difference would be a surprise worth a hand-read |
| H2 | those records are more complete against git and leave fewer stubs (M2) | **Higher in v3.7 and v3.8, by design.** They require a ledger entry and a durable receipt; v3.0 requires neither. This is the feature working, not prose quality, and the report says so. The T-remove tally (finding 1) leans this way |
| H3 | those sessions leave fewer stale live documents (M3) | **No difference expected; direction uncertain.** Both runners say to grep for dangling references in execution sessions and to verify cross-references a change adds or touches (§10 rows 4 and 20); I found no rule in either that names updating live documents after a removal. Untested until a task exists |
| H4 | a cold session reconstructs the state better from a v3.7 or v3.8 record than from a v3.0 one (M4) | **Plausible, uncertain.** The receipt's required `key_files` and `gotchas` and the ledger give it more to read; the v3.7 runner is 24,666 B longer than v3.0's (65,140 against 40,474) and v3.8's 12,778 B longer, which costs the cold session reading. I do not predict whether the git-only control closes the gap |
| H5 | a blind rater prefers those records (M5) | **Unknown, and the least trustworthy.** The raters are the writers' model family, and receipt format may reveal the arm |

**What a null means:** that on this project, at this start state and model, the versions did not leave measurably different
records on these measures. It does not say they are alike on a longer run or another model.
**What no outcome can say:** which feature produced a difference (the contrast is everything between the versions; an ablation of
ledger against receipt against reconcile is a later study, worth doing only if M2 or M4 shows a signal), anything about growth of
the record over many sessions, or anything about the trimmer, which v3.7 lacks and the saved v3.8-text runs never needed.

### 2.5 Which runs, and where each stops

**Inclusion rule, written before any scoring:** every saved run that reached a close-out commit or receipt in its final tree is
scored. **No run is dropped for cost or for correctness:** S237's cost-valid set and the held-out result are carried as covariates,
because M2(c) exists for exactly the runs that claim done when they are not. (S237's cost table drops v3.7 rep 5, the one honest
partial that closed out at the RED gate, and keeps v3.0 rep 4, whose real-test failures are `[4,0,0]` in `held_out_results.json`; a
cost-based inclusion would have inverted what this study cares about.) Runs cut off before any close-out (v3.0 rep 2, v3.7 rep 1)
are listed and not scored.
**Pinned end sha, per run:** the first close-out commit. For the runs that continued past it (v3.7 rep 2 holds a second full
session; v3.0 rep 3 ran on; T-remove R0 rep 5 holds S555 and S556) the pin is the first close-out, taken from `held_out.py`'s `RUNS`
where it names one (`7b9bd618`, `b15ae1c5`) and from the first close-out commit otherwise. Every scorer takes the pin explicitly.

---

## §3 Design

### 3.1 Which question (D1)

| | Question | What the evidence says |
|---|---|---|
| **Q1** | *For an adopter whose project already carries the rules (the T-remove start), what does moving to v3.8 change?* | **Partly answered** by the T-remove trees, with a small gap in H2's direction and two confounds (finding 1). Re-running adds little |
| **Q2** | *What does the documentation machinery do that v3.0's does not, for an adopter that does not already carry it?* | **Partly answerable now, at $0**, from v3.0, v3.7 and v3.8-text runs on a rule-free start state (finding 2); **not answerable now** for whether a successor can use the record, which needs new sessions. The operator's question reads as Q2 |

The plan designs for **Q2**.

### 3.2 The start state: `879503cce`, the one S237 and the T-control batches used

`nprcgenekeepr` at `879503cce` (2026-07-08, the parent of the real fix `54b87c1da` for issue #121; the harness default in
`real_project.py`). **Why this and not a start state built for this study:** all three saved sets that matter are on it; the task and
its held-out answer already work; the cost at this record size is measured ($2.56 mean for v3.0 and $2.91 for v3.7 over all rows;
$3.45 for the 13 v3.8-text T-control runs, four of them above $4); and nothing has to be built. Its `CLAUDE.md` has no documentation
rules (§10 row 10).

**The neighbouring start state, S323 (`7e3752397`), is not needed.** It is ten commits later, with the same runner (the identical
blob, 31,785 B), the parent of the project's own upgrade to v3.4 (`0c3af8b9f`, S324; verified), and the same kind of record (notes
3,938,380 B, ledger 932,452 B in a legacy format). Its runner is within 4 diff lines of v2.6.1 and v2.6.2 and within 54 of v3.0's.
It was this plan's first choice; the first review showed `879503cce` does everything it did and is already used.

**What this start state is not:** today's `nprcgenekeepr`, or a project with a trimmed record. Four things about it are named,
because each could carry a result:

1. **A 3.85 MB notes file.** The active task sits at the top (at S323, line 7), so a v3.0 session need not read the whole file; but
   every session must write into it. Costs are already measured here.
2. **No trimmer for the notes.** The v3.8 trimmer (`methodology_trim.py` at the tag: specs at `:303` for `CHANGELOG.md` and `:328`
   for `HANDOFFS.md`) does not cover `SESSION_NOTES.md`; the project's own R0 rep 5 session S556 existed to restore a local notes spec
   "dropped by the v3.8 sync". A session obeying the size rule therefore moves history by hand, which §2.2's moved-line rule absorbs.
   (No saved run actually moved history, by the reviewer's count; the rule is for the new ones.)
3. **A legacy-format ledger.** The project's `CHANGELOG.md` predates the authoritative-ledger format (its own `CLAUDE.md`, S325,
   froze 303 untagged entries); a real sync and `install_arm.py` keep seeds unchanged, so a v3.7 or v3.8 arm gets a stale-format
   ledger. That is what a real adopter at that commit got.
4. **A shared writing style.** The project's own notes history sets the style every arm imitates. M1 to M3 score claims against the
   tree, not style, and the limit is named beside every result.

### 3.3 Arms

| Arm | Contents | What it answers |
|---|---|---|
| **v3.0** | tag v3.0 over `879503cce`; S237, five runs that reached a close-out | an adopter on v3.0 |
| **v3.7** | tag v3.7; S237, six runs that reached a close-out | v3.8's ledger, receipt and reconcile machinery, **without** the trimmer and the ratchet (finding 3 above) |
| **v3.8 text** | the ratchet study's T-control R0 (v3.8 text, ratchet removed, n=3) and R1 (n=5 with the old close-out reply, n=5 with the fixed one) | v3.8 itself, on the same task and start state, **with three confounds:** R1 carries the ratchet hook; the close-out reply differs between batches and from S237's; R0 is n=3 |
| *(only if needed)* **v3.8 new** | new task runs, built by `ratchet_arms.py`, which registers `v3.8` with `install_arm.ARMS` at import (`:30-31`) | a clean v3.8 arm if the saved v3.8-text runs cannot be pooled (§5 P1b) |

The contrast is **everything between the versions**, never one feature. **The arms are built as the harness installs them**, with its
known simplifications (`install_arm.py` docstring: README not installed; hooks, task mapping and dashboard setup not applied). The
first reviewer's scratch build of a v3.8 arm gave the expected 53,252 B runner but landed the seed files without their leading dot,
so `context_budget.py --status` found no `.context-budget.json` (reviewer's observation; I did not re-run it): "v3.8 as released" is
not what the harness builds, and no result may be read as about the context-budget gate. P1a re-runs the §10 phrase counts on each
built or saved tree as a **build sanity check, not a guard against the arms behaving alike** (the counts differ 0 against 14 by
construction).

**The install commit.** `bin/sync` here mentions neither the ledger nor the changelog (`grep -in 'changelog\|ledger' bin/sync`
returned nothing; and a sync leaves its changes for the operator to commit), so a v3.7 or v3.8 session will treat the harness's
install commit as undocumented and spend effort backfilling it. That is realistic, part of what those versions cost, **excluded
from every measure** (§2.2) and reported on its own line. It appears in the saved runs of both versions (v3.0 rep 3's own subject
names "methodology v3.0 install").

### 3.4 The task, and the staleness measure

**Task: issue #121 of `nprcgenekeepr`** (seven unasserted test warnings), the S237 task, with the S237 script (`stakeholder.REAL_SCRIPT`)
and the held-out tests of the real fix. A test fails if any scripted reply names the thing under test: *record, handoff, ledger,
receipt, notes, changelog, document, stale* are forbidden in the script, as the ratchet study forbade *gate, floor, threshold*.

**M3 has no target here.** The removal task of the ratchet study (two helpers, `resetGroup` and `chooseAllelesChar`, which exist at
`879503cce`) names no live document: the only other mentions at S323 are `CHANGELOG.md`, `PROJECT_LEARNINGS.md`,
`SESSION_NOTES.md`, `TECH_DEBT_AUDIT_2026-05-30.md`, two dated planning documents (`docs/planning/issue112-…plan.md`,
`docs/planning/phase8e-…subplan.md`), the generated `test_results_summary.md`, and the **dead** `inst/_pkgdown.yml`. P2a searches
the project's history for a task whose honest completion makes **at least two documents false that are demonstrably read** (for a
config file: by the tool that consumes it, as commit `d14cd913d` did), and either finds one or reports that none exists. **A task
found that way would be a different task on a different start state, so it is a new study unit with its own build, runs and cost, not
priced here.** **Classification written now:** historical (never edited): `CHANGELOG.md`, `SESSION_NOTES.md`, `HANDOFFS.md`,
`PROJECT_LEARNINGS.md`, any dated audit or plan under `docs/planning/`, `TECH_DEBT_AUDIT_2026-05-30.md`, `test_results_summary.md`.
Live: `README*`, `vignettes/`, `NEWS*`, `CLAUDE.md`, the pkgdown config that pkgdown reads. A document that fits neither is classified
when it is found and listed.

### 3.5 The unit of a probe: a cold start in a clone, and a control

For each saved end state, a **cold start in a fresh clone of its pinned sha**, same version, opening "go": the runner's mandatory
Phase 0 report, then it stops (`--max-stops 1`; the driver mode that points it at an existing clone is P2a). The clone is rebuilt
from a `git bundle` kept in P1a (a `git format-patch` text would rebuild commits with different shas from the ones the record cites),
and its shas are checked against the bundle's before use. M1 to M3 and M5 read the original session's record at the pinned sha; M4
reads the probe's report. A **git-only control** probe (§2.3 M4) runs on a sample of end states.

### 3.6 The session chain is deferred, and shared (D6)

What accumulates over many sessions (the record's growth, trimming, repeated reconcile) needs the chain of the ratchet plan
[§4](ratchet-mechanism-test-plan.md): one chain driver, **one chain asking both questions** (erosion and documentation), about $35
as that plan estimated. Building it twice would be waste, so the chain is a decision *after* P3 (D6), and choosing it changes that
plan's open decision D4.

### 3.7 Fixed across arms

Model `claude-sonnet-5-5`, effort `xhigh`, opening "go", the same scripted replies, the same pacing, the same stop rule. **The CLI
changed during the saved studies** (the ratchet plan §3.1 records 2.1.285; it is 2.1.288 now, and the reviewer found other patch
versions in between that I did not re-derive; the rows carry no version field). P1a reads each saved run's version from its
transcript and reports it beside the run; every cold probe runs on one CLI, so that factor does not vary within M4. Every
published table carries: *this is today's model under each arm's own instructions, on one project at one start state.*

### 3.8 Sample size, honestly

S237's spread at n=5 was about ±15% on cost (ratchet plan §3.5); binary outcomes need a near-total difference. For a rate such as M1
the size follows from a measured spread: per arm, `n ≈ 15.7 σ² / d²` for 80% power at 5% (two-sided, equal arms, normal
approximation), where `σ` is the standard deviation of the rate and `d` the difference worth detecting. For example `σ = 0.15`,
`d = 0.20` gives n ≈ 9 by that formula, **but a t-test needs about 10: my simulation gives 76% power at n=9 and 80% at n=10.**
**`σ` comes from P1b's scoring of the saved runs, not from a pilot, which has one run per arm and so no spread.** The saved arms have
n = 5 (v3.0), 6 (v3.7) and up to 13 (v3.8 text); a larger n for v3.0 or v3.7 means new task sessions at about $3 each (measured)
plus probes, a cost line the operator approves (D4). The study ranks nothing finer than its spread.

---

## §4 Who or what scores

1. **Mechanical (M1 to M4):** a new module `overhead-replay/doc_score.py`, separate from the frozen scorers, pure functions over a
   run tree at a pinned sha, its commits and the probe's report. Each measure has a fixture that exhibits each defect and must score
   defective, an honest fixture that must score clean, and mutants of the scorer that must be killed. **Frozen at the end of P1a, after
   the calibration and a parse-only smoke test, and before the v3.0, v3.7 and v3.8-text runs are scored.** **Amendment rule:** if a
   defect surfaces after the freeze, it is fixed only with the operator's word, *everything is re-scored*, and both versions of the
   result are reported, as the ratchet study did for D7.
2. **Hand-read:** every verdict on the pilot, three trees per measure in P1a, and a sample of the main run, as the ratchet study did.
3. **Model rater (M5 only):** blind, a fixed yes/no list, order swapped between two ratings of each record, a planted-defect set (a
   record with a deliberately wrong next step, a missing next step, a fabricated sha) that it must rank below the honest ones, and the
   **arm-guess question** reported: if the rater names the arm correctly most of the time, blinding failed and M5 is reported as
   unblinded. It is the same model family as the writers; that bias is stated beside every M5 figure.
4. **Operator's own rating (D5, decided: he does it himself):** a blind sample of about ten records as a human anchor for the model
   rater. How many records he rates is his call; I have not timed how long one record takes to read. **If he meant this to replace
   the model rater rather than anchor it, the model rater and its $2 dry run drop out and M5 becomes his ratings alone; P2a asks
   before building the rater.** **Decided at the S258 picker: both (the model rater is built, beside his rating), and the sample is SIX records, two per
   arm** (about 102 minutes of reading; ten was 168). Measured: the ten-record packet was 33,592 words, 2,832 to 3,600 per record.

---

## §5 Phases

**Each of P1a, P1b, P2a, P2, P3 is one session; close out after each.** The ratchet study's build phases took S239 (P1), S240 (P1b,
abandoned at the operator's instruction) and S241 (P1b again), and its T-control tooling a further $0 session (S244; `CHANGELOG.md`
lines 462 to 534), so a phase with six deliverables is split here and "expect two to four sessions" is the honest number for P1.

### P1a: Keep, define, build, calibrate, freeze ($0, no model tokens)

**Done when:**
(a) **evidence kept**: for every surviving tree (T-remove 15, T-control 13 and the other ratchet batches, real-3.7 13), `git bundle`
of the run's commits (`base..HEAD`, which preserves the shas the records cite; the base commit is in the project repo) and the final
documentation files, saved under `overhead-replay/pilot/doc-evidence/`, **size measured first**; if over 5 MB they are stored
outside git and §10 says where. Each run's CLI version is read from its transcript and tabulated.
(b) **definitions fixed**: §2.2, §2.3 and §2.5 as written, the M4 key builder reading only the tree, the classification of §3.4, and
the two keyword rules ("says done", "discloses") written out.
(c) **scorers**: `doc_score.py` for M1 and M2 and the M4 key builder and report scorer, each with the failing fixtures, honest
fixtures and mutants of §4; unit tests green; a test that cannot fail does not count. **The parser skips any receipt block whose
`session:` line contains `<` or `>` (the format example), with a test on the real template block.** Fixtures cover a session that
archives a file (moved lines must not count), one that overwrites its own pending stub, one that copies a stale line forward, and a
v3.0-style record with no receipt (M2(b) "not applicable").
(d) **parse-only smoke test**: the scorers run over every saved set with **no scores read**, to show each record format parses
(v3.0 has no `HANDOFFS.md`; the real-3.7 trees are run-on in places; the ledger is legacy-format), so a format defect is found
before the freeze and not after it.
(e) **calibration, then freeze**: the scorers run over the 15 T-remove trees (start `402a6b5b`, rules already in the project),
per-tree outputs hand-read for three trees per measure, harness artifacts (the install commit, the S554 orphan stub, R0 rep 5's
second session) excluded by design and fixed; **the scorers are then frozen.**
**Verification:** the new tests green; `git diff <start sha>..HEAD --stat -- docs/planning/overhead-replay/erosion_score.py
docs/planning/overhead-replay/remove_score.py` is empty and no distributed file appears in `git diff --name-only <start sha>..HEAD`
(`git status` alone is always clean after a commit and proves nothing); each bundle verifies (`git bundle verify`).
**Surface:** the local machine; `overhead-replay/` and the saved evidence; the saved trees. **What it cannot enforce:** that a *live
model's* new record behaves like the saved ones, that blinding holds. **Cost: $0.**
**STOP:** a tree missing or a base sha not found; a bundle that does not rebuild the pinned sha; or a noise floor on M1 and M2 so
wide that no plausible difference could show. Return to the operator.

**Status (S256, 2026-10-03): DONE, $0, no model run, no distributed file touched.** (a) [`pilot/doc-evidence/`](overhead-replay/pilot/doc-evidence/README.md): one
851 KB git bundle holding all 41 saved runs, a manifest, `doc_evidence.py` and 14 tests; `verify` passes against the project repository and from a fresh clone. (b) The definitions are
[`DOC_SCORE.md`](overhead-replay/DOC_SCORE.md). (c) [`doc_score.py`](overhead-replay/doc_score.py) with 130 tests, 41 of them mutants each run first on an unbroken copy. (d) The parse-only smoke test
parsed all 41 runs and printed no score. (e) The scorer was calibrated on the 15 T-remove trees (record in
[`CALIBRATION.md`](overhead-replay/pilot/doc-evidence/CALIBRATION.md)): 622 of 626 checkable references verify, the 4 that do not are real, and M1 (0.939 to 1.000), M2(a) (1.000) and M2(b) (zero left) are at a ceiling there; it
was then **frozen** ([`doc_score.frozen`](overhead-replay/doc_score.frozen)). No STOP condition fired. **Where this differs from the text above, and what P1b should use:**
* **The bundle is one file whose range starts at the project's own commit** (`879503cce` or `402a6b5b7`), not at the install base: the install commit is made by the harness and is not in the project repository, so a bundle starting there could not be verified or unbundled. Final documentation files are not copied out; they are in the bundle.
* **CLI versions are per run and differ inside a set**: 2.1.285 on 7 runs, 2.1.286 on 14, 2.1.287 on 20. S237's 13 straddle 2.1.285 and 2.1.286 (6 on 2.1.286), so §3.7's "S237 on 2.1.285" holds for 7 of them. A covariate.
* **Inclusion (§2.5), applied mechanically** (`reached_closeout`): v3.0 n=5, v3.7 n=6, **v3.8-text n=12, not 13** (`t-control-fix/R1-r1` stopped at a claim and two work commits, with a pending receipt), T-remove n=15; left out are exactly `real-3.7/v3.0-r2`, `real-3.7/v3.7-r1` and that one. 26 of 41 trees have an untracked `dashboard_history.jsonl`; only those three have tracked uncommitted edits.
* **Amendments the calibration made to §2.3**, all before the freeze: test counts (M1 d) are read from the final message only, the last of each kind; an identifier beside an anchor also verifies when it names the function enclosing that line; the pin commit is not owed a name in its own record (M2 a); a path stated removed is looked for in the two lines before and one after; tool output nobody commits (`dashboard.html`...) and the ratchet's `results x · manifest y` digests are not references. Sixteen changes in all, each with a test, in `CALIBRATION.md`.
* **T-remove cannot show that the scorers detect defects at realistic rates** (it is at a ceiling because the project's own rules are in every arm); detection rests on the fixtures, the mutants and the four real failures. Whether M1 and M2(a) have spread on the rule-free start state is P1b's question.

### P1b: Score what exists, once ($0)

**Done when:** the frozen scorers have been run once over the v3.0 (five), v3.7 (six) and v3.8-text (up to 13) runs by the §2.5 rule;
the report gives each measure by arm with its spread (`σ` for §3.8), the covariates (cost-valid, held-out, CLI version, close-out
reply wording, ratchet hook), the M1 ceiling check, the §2.4 expectations marked met or not, and a **pooling check**: whether the T-control
batches' process rows (cost, requests, tool calls, commits) are consistent with S237's v3.0 and v3.7 rows, so the report can say whether
v3.8-text may be compared at all or whether new v3.8 runs are needed.
**Verification:** every figure is reproducible from the bundles and `rows.jsonl` by one command the report names; the scorers' output
is saved beside the evidence.
**Surface:** as P1a. **Cannot enforce:** M3 and M4 (no saved run has a cold probe or a live target). **Cost: $0.**
**STOP:** at the end, return to the operator with the first answer and the decisions it informs (D3, D4); do not start P2a.

**Status (S257, 2026-10-04): DONE, $0, no model run, no distributed file touched, the frozen scorer unchanged.** `doc_score.py` (sha-256 `eaec3a2ec9c6`) was run **once** over the 26 saved runs of the three contrast sets by
[`p1b_score.py`](overhead-replay/p1b_score.py) (20 tests, 10 mutants all killed); 23 were scored (v3.0 n=5, v3.7 n=6, v3.8-text n=12). Scores: [`p1b-scores.json`](overhead-replay/pilot/doc-evidence/p1b-scores.json); the report,
hand-reads and the stop: [`P1B_REPORT.md`](overhead-replay/pilot/doc-evidence/P1B_REPORT.md); every table reproduces from `python3 docs/planning/overhead-replay/p1b_score.py report .../p1b-scores.json`.
**First answer:** M1 0.984 / 0.990 / 0.990 and M2(a) 1.000 / 0.967 / 1.000, no difference and at or near the ceiling (**H1 met; H2 not met on M2(a)**: v3.0 names all its commits); on hand-read 11 of the 13 M1 failures and 2 of the 3 M2(c) flags are scorer false positives, and one run (`v3.0-r4`) truly says done on a task the answer key fails. The versions differ in what the record
holds (51 and 56 checkable references per run against 33) and in commits to the pin (3.4, 5.6, 5.2), not in accuracy. **Where this differs from the text above:**
* **The pooling check can only be a screen.** No arm appears in two batches except R1, so arm and batch are confounded; the one within-arm contrast (R1, old reply against fixed reply) is +44% cost (p = 0.07), larger than any between-arm cost difference. v3.8-text may be compared on M1 and M2 as a screen and **not on process rows**; new v3.8 task runs are not forced.
* **"Commits" in the process rows are commits to the pin, from the scorer's range**, not the manifest's count to HEAD (`v3.7-r2` has 13 commits past its pin); the cost rows use S237's cost-valid set (v3.7 rep 5 out).
* **The two S237 override runs' final messages were read** (S256 gotcha 6): each is the first close-out's own report.
* **No amendment was made.** Five false-positive families are listed in the report for the operator's word; the recommendation is not to amend (the hand-read what-if is 1.000, 1.000, 0.997, so no conclusion moves).

### P2a: Build the probe ($0, no model tokens)

**Done when:** (a) the **driver mode** that rebuilds a clone of an end state from its bundle at the pinned sha, checks the shas, runs
a fresh session for one turn, and a git-only variant, is tested against the fake `claude` in `tests.py` before it is pointed at a real
one (24% of S237's spend was lost to untested driver behaviour); (b) the project's R suite at `879503cce` timed once (M1 (d)); (c)
the probe's token and tool-call budget estimated from a saved transcript's Phase 0 reads; (d) the rater protocol and planted-defect
set built (§4 item 3); (e) the M3 task search of §3.4 run and its result listed; (f) **per-session caps stated**: the driver refuses a
launch when `spent + session cap > total cap` (`driver.py:151`), its default session cap is $2.00 and `run_main.py` defaults to $10,
so a total is only usable beside its per-session caps, and the rater's calls get their own `--max-budget-usd`.
**Verification:** the driver tests green; a rebuilt clone's `git rev-parse HEAD` equals the pinned sha. **Surface:** the local
machine; `overhead-replay/` only. **Cannot enforce:** that a real model behaves like the fake `claude`. **Cost: $0.**
**STOP:** a bundle that cannot rebuild its sha, or a driver behaviour the fake cannot reproduce. Return to the operator.

**Status (S258, 2026-10-04): DONE, $0, no model run, no rating call, no distributed file touched. Report: [`P2A_REPORT.md`](overhead-replay/pilot/doc-evidence/P2A_REPORT.md).**
(a) [`probe.py`](overhead-replay/probe.py) with [`tests_probe.py`](overhead-replay/tests_probe.py) (43 tests, mutants all killed); **a pre-flight on the real bundle rebuilt all 38 rebuildable runs as end state and as git-only control with HEAD equal to the pinned sha** (3 refused by design: uncommitted tracked files), [`p2a-preflight.txt`](overhead-replay/pilot/doc-evidence/p2a-preflight.txt).
(b) the R suite at `879503cce`: **120.8 s**, `passed=3734 failed=1 warnings=7 files=252`, so M1 (d) re-runs on every scored end state (no sample).
(c) **a probe should cost about $0.35, not $1:** the saved runs' first stop (the same `go` turn, on the start state) cost $0.24 (v3.0), $0.38 (v3.7), $0.38 (v3.8-text), highest $0.51. That is the original sessions' first turn, not a probe.
(d) [`rater.py`](overhead-replay/rater.py) (36 tests, mutants all killed): the eight fixed questions, both orders, the four planted defects (`fabricated` reported, not required), the packet builder. Built both (his rating and the model rater), his answer at the S258 picker. **A ten-record packet was 33,592 words, about 168 minutes of reading at 200 words a minute; he chose six, two per arm: 20,410 words, about 102 minutes**, in `pilot/doc-probe/rating/`.
(e) **no M3 task in the project's history** (56 function-removal commits, none leaves two parsed-or-agent live documents false that the commit also fixed); **one constructed task exists on the study's start state**: rename `getEmptyErrorLst`.
(f) caps: study $100; proposed probe session cap **$1.00**, rater call cap **$0.50**, P2 total cap **$10** (the plan's proposal stands); both caps are required arguments, and the CLI overshoots a cap slightly (one saved stop: $2.0389 on a $2.00 cap).
**Where this differs from the text above:** the tests are in `tests_probe.py`, not `tests.py`; a probe that costs at 98% of its session cap is recorded as failed (`cap_hit`); `--verify-all` is the pre-flight. **P2 is its own session and its own go. Decided at the S258 stop (his picker answers): P2 at the $10 cap, a six-record packet, M3 deferred until after P2.**

### P2: Pilot, with a cap

**Done when:** cold probes on **four** saved end states (one v3.0, one v3.7, one v3.8-text, and a git-only control on one of them), and
the rater run once on the planted-defect set and once on the pilot records with its arm-guess accuracy reported; every verdict
hand-read; a short report with the **real cost per probe and per rating** and whether the probe is cheap enough for P3.
**Estimate:** four probes at about $1 each (a guess from Phase 0's share of a session, not a measurement) plus a rater dry run about
$2: **about $6.** **Per-probe cap proposed: $2; the worst case is 4 × $2 + $2 = $10, which is the cap proposed.** The driver's
per-session cap ends a runaway probe and records it as cut off. **A proposal; the figure is his (D4).**
**Verification:** the spend ledger is re-summed from its last cumulative file and equals the cost the report states; every row is
re-scored from the saved evidence; `git diff <start sha>..HEAD --name-only` shows only the pilot's own files. **Surface:** `claude -p`
sessions on this machine, under the operator's login and the CLI as probed in P2a. **Cannot enforce:** that a human stakeholder behaves
like the script; the installer's known simplifications; that four probes predict the main run. **STOP:** any unscripted stop pattern, a
probe that cannot be scored, or the cap.

### P3: Main run

**Done when (3a):** cold probes on every remaining saved end state, and a git-only control on a sample; ratings; rows, scores and the
report committed together; the §2.4 expectations marked met or not. **Estimate:** v3.0 4 more + v3.7 5 more + v3.8-text up to 12 more
end states (the pilot did one of each) = 21 probes at $1, plus about 6 controls at $1 = $27, plus a 25% margin for defects (24% of
S237's spend was lost to them) = about $34, plus about $4 of rating = **about $38**. **(3b) only if P1b rejects pooling the v3.8-text
runs:** about five new v3.8 task sessions at the measured T-control mean of $3.45 (**per-session cap $6**: four of the 13 saved runs cost
more than $4 and one $5.29, so a $4 cap would truncate about 30% of sessions), plus five probes, plus margin = **about $28**. Each
needs the operator's word separately. **Both figures are re-stated from P2's measured cost before anything is authorised (D4).**
**Verification:** as P2, and every number in the report is reproducible by one command it names. **Surface:** as P2. **Cannot
enforce:** anything past one project, one model, one start state. **STOP:** cumulative spend crossing the figure the operator set,
checked by the driver before each launch.

### P4: Chain (optional, D6)

A chain driver built at $0 first (P4a), then one chain per arm asking the erosion and documentation questions together; the ratchet
plan's own estimate is about $35. **Not planned in detail here:** it is shared with that plan and waits for P3's real cost.

### P5: Report

A results document in the fork carrying the §3.7 sentence on every table, with H1 to H5 marked against §2.4. **Publication beyond the
fork is a separate outward action and needs the operator's go-ahead at the time (D7).** **Verification:** every figure in the report
is re-derived by a command it names, as this plan's §10 does. **Surface:** documents in the fork only.

**Budget summary (estimates, not measurements):** P1a, P1b, P2a $0; P2 about $6 expected, cap proposed $10; P3a about $38; P3b about
$28 only if needed. Total through P3a about **$48** (the P2 cap plus P3a), through P3b about $76, against **the $100 cap the operator
set for this study** (§7 D4), which leaves about $24: roughly five more task-plus-probe units at the measured $3.45 plus about $1 each,
before margin. A larger n for v3.0 or v3.7 (§3.8) draws on that $24 and needs his word before it is spent.

---

## §6 Risks, each with its counter

| Risk | Counter |
|---|---|
| The arms look alike again | P1b scores saved runs on a rule-free start state before any spend; the build check in §3.3 is a sanity check and says so |
| M4 rewards what git already says | the git-derivable facts are scored separately and a git-only control gives the record's contribution (§2.3) |
| M1 sits at ceiling and says nothing | the ceiling rule in §2.3; the anchor check needs a nearby identifier to match |
| The install commit confounds M2 and cost | excluded from every measure; its reconcile cost reported on its own line (§3.3) |
| A session that archives a file looks like a huge record | §2.2's moved-line rule; a fixture covers it (P1a (c)); a stale line copied forward still counts |
| Compliant sessions score as "rewriting history" or as leaving stubs | §2.3 M3 defines rewriting by removed base lines with two named exceptions; M2 does not score the `commit:` slot; M2(b) is "not applicable" for v3.0 |
| The saved v3.8-text runs differ from S237's in reply wording, hook and CLI | named as confounds (§3.3); P1b's pooling check; new v3.8 runs only if it fails (P3b) |
| A scorer format defect appears only after the freeze | the parse-only smoke test in P1a (d), and an amendment rule (§4) |
| A measure is fitted to what I expect to find | definitions, classification and keys written before any scorer; scorer frozen after calibration and before the saved runs are scored; hand-read pilot |
| A loose pattern produces a number that is not a measure (the "pending in most trees" count) | every measure has a failing fixture and an honest one; hand-read three trees per measure |
| The parser reads the format example as a real receipt (it did, in this session's first tally: `S<N>`, `<pending`) | the scorer skips any block whose session field contains `<` or `>`; a test with the real template block |
| The project's notes history sets a writing style every arm imitates | named as a limit beside every result; M1 to M3 score claims against the tree, not style |
| The model rater is the writers' family and may recognise receipt format | blind, fixed list, planted-defect check, arm-guess reported; M5 is last and never the headline |
| The cold probe's cost reflects the framework's reading load, not the record | cost split into record reads and framework reads from the transcript; both reported |
| A rebuilt clone has different shas from the ones the record cites | `git bundle`, not `format-patch`; shas checked before use (§3.5) |
| Subset selection hides the honest partials | §2.5 includes every run that reached a close-out; cost-validity is a covariate |
| The run trees disappear at reboot | P1a (a) keeps the evidence before any other work |
| Spend mechanics do not compose (driver default session cap $2.00, total check at launch; the rater is uncapped by the driver) | per-session caps stated beside every total (§5 P2a (f), P2); the rater gets its own cap |
| Whole study is "today's model under old instructions" | the §3.7 sentence on every table |

---

## §7 Decisions the operator owns

| # | Decision | Status and recommendation |
|---|---|---|
| D1 | Which question: Q1 or Q2 (§3.1) | **RATIFIED 2026-10-03, as recommended: Q2.** Q1 is partly answered by the T-remove trees |
| D2 | Start state | **RATIFIED 2026-10-03, as recommended: `879503cce`**, the one S237 and the T-control batches used (§3.2): saved runs, measured cost, a working task and answer key. S323 offers nothing more. Alternatives not taken: strip the methodology from a later start state (heavy surgery, not a real adopter); or the S236 fixture (cheap, seeded ghost commit and stale handoff, a mechanism probe, but the operator redirected the overhead study away from it) |
| D3 | Arms | **RATIFIED 2026-10-03, as recommended: v3.0, v3.7 and v3.8-text, all saved.** New v3.8 task runs only if P1b rejects pooling. P1b ends in a stop at which the case for spending on probes is reconsidered with the free result in hand: if v3.0 against v3.7 and v3.8 shows nothing at all on M1 and M2, that case is weaker. **Reconsidered at the P1b stop (S257, 2026-10-04), his answers from a picker:** take **P2a next** ($0, no model tokens; the next session starts on it), **no scorer amendment**, **BL-97 left as it is** (rerun on a lone red). The P2 spend is not decided by this: it is decided at P2a's end, when the probe's real cost is known |
| D4 | Spend | **DECIDED 2026-10-03: $100 for this study, and the earlier caps are ignored for it.** His words: "D4: spend $100 for this experiment (ignore prior cap)". It is a cap on the study's own ledger, which starts at $0: every launch of this study passes the driver `--total-cap 100`, read from the study's own `spend.jsonl`, not the ratchet study's. The earlier figures no longer constrain it: the $125 ratchet-test cap with $109.51 on its ledger, the $175 total with $44.55 before that study, and the $20.94 and $15.39 headroom the earlier drafts computed (§10 row 18 keeps them as history). **What that sentence does not decide, left as the plan's proposals inside the $100:** the per-phase and per-session caps (P2 $10 with $2 per probe; P3a about $38; P3b about $28 with $6 per session). Each phase still starts only when he says go in a session, and P3 is still authorised only after P2 has named its real cost. **At P2a's end (S258) he chose P2 at the $10 cap** (probe session cap $1.00, rater call cap $0.50, to start when he says go in that session), and **M3 deferred until after P2** |
| D5 | Rater: model only, or also his own blind rating of about ten records | **DECIDED 2026-10-03: he does the blind rating himself.** His words: "D5 I will do blind rating". I read it as the plan's recommended option, his own rating of about ten records as the human anchor beside the model rater; if he meant it *instead of* the model rater, §4 item 4 says what drops out, and P2a asks before building the rater. **P2a asked (S258): both, with six records, two per arm** |
| D6 | The session chain, and building it once for both studies | **OPEN, after P3.** Changes the ratchet plan's D4 |
| D7 | Publication beyond the fork | **OPEN, not needed until P5.** Recommend fork only until the results have been seen. Outward-facing, so asked at the time |

**D1 to D5 are decided; D6 (after P3) and D7 (at P5) stay open.** His message, verbatim, after the S255 close-out: *"D1-D3 accept recommendations; D4: spend $100 for this experiment (ignore prior cap); D5 I will do blind rating"*. P1a can start in any session he says go;
P1b ends in a stop at which D3 and the spend are reconsidered with the free result in hand.

---

## §8 What this plan does not do

It adds no gate and changes no distributed file. It builds nothing outside `overhead-replay/` and the saved evidence directory. It
launches nothing: P1a, P1b and P2a spend no model tokens and are the only phases this document's approval would start. It does not
reopen S3 or D1 of `overhead-ratchet-plan.md`, does not extend the frozen erosion scorers, and does not touch upstream.

## §9 Planning checklist (runner §Planning Sessions)

- **Reasoning depth: not verified.** The runner asks for the deepest available mode at the start of a planning session; this
  session could not set one from inside and the operator was told so at the picker. Recorded, not claimed.
- **Re-derived this session, not quoted:** every figure in §10 was produced by a command run in S255, most also by a reviewer
  independently (§11). Quoted and not re-run: the ratchet study's cost means ($2.03 / $2.49 / $2.87 on T-remove), from its report.
- **Not verified here, flagged:** the project's R suite time at `879503cce`; that the harness builds a plain `v3.8` arm over
  `879503cce` (the reviewer's scratch build succeeded on the T-control configuration; I did not re-run it); **what a v3.0 or v3.8
  Phase 0 and close-out do with the 3.85 MB notes file** (only that the active task sits at the top); the cold-probe and rater costs
  (guesses until P2); what S244 counted as "pending" (its tally says only that it was crude); whether the saved runs from different CLI
  patch versions pool; whether the unresolved shas in §10 row 33 are real; the reviewer's finding that no saved run moved history
  (my own count in row 33 includes the receipt file, whose stub overwrite deletes lines, and so is not comparable).
- **Not independently reviewed:** the revision that followed review 2 (this document as it stands). Review 1 found four errors in
  the first draft and review 2 three more in the second; the third version carries the same risk and the executor of P1a should
  re-run §10's rows before relying on them.
- **Per-phase DONE, verification, surface, cost and STOP:** §5.
- **Grep-based inventory** (§10) covers the claims the design rests on; a plan that lists what to check without having checked it is
  an assumption.

---

## §10 Evidence inventory: the commands, and what they returned (S255, 2026-10-03)

| # | Claim | Command (from the repository root unless stated) | Result |
|---|---|---|---|
| 1 | tags exist; v3.0 is an ancestor of v3.8 | `git tag -l 'v3*'`; `git merge-base --is-ancestor v3.0 v3.8` | v3.0 v3.0.1 v3.1 … v3.8 present; exit 0 |
| 2 | v3.8 adds these starter-kit files over v3.0 | `diff <(git ls-tree -r --name-only v3.0 starter-kit \| sort) <(… v3.8 …)` | `context_budget.py`, `context-budget.json`, `FRAMEWORK_LEARNINGS.md`, `HANDOFFS.md`, `methodology_trim.py`, `quality_ratchet.py`, `quality-gates.json` |
| 3 | runner sizes | `git show "refs/tags/${v}:starter-kit/SESSION_RUNNER.md" \| wc -c` (braces: `$v:` is a zsh history modifier) | v3.0 40,474 B / 371 lines; v3.7 65,140 B; v3.8 53,252 B / 394 lines |
| 4 | runner text bearing on each construct (case-sensitive line counts, v3.0 / v3.8) | `grep -c -- '<phrase>'` on each | *Re-read the actual files before writing claims* 1/1; *Never write "need to verify"* 1/1; *Verify cross-references* 1/1; *Minimum Handoff Requirements* 1/1; *Key files* 1/1; *Gotchas* 1/2; *Evaluate the Previous Session* 1/1; *Claim the Session* 2/2; *derive them or label them a guess* **0/1**; `CHANGELOG: pending` **0/4**; *durable receipt* **0/1**; *reconcile-on-read* **0/1**; *Backfill* **0/2**; *size ceiling* **0/1**; `check-handoff` **0/1**; *Unrecorded action* **0/1**; *Unbounded mandatory read* **0/1**; `HANDOFFS.md` **0/8**; `reconcile` **0/14**. v3.7, where measured: `CHANGELOG: pending` 4, `reconcile` 16, `HANDOFFS.md` 11, *Backfill* 2, *Unbounded mandatory read* 1, *size ceiling* 1. The first reviewer confirmed the seven "1/1" lines read identically in v3.0 and v3.8 |
| 5 | the 15 T-remove trees: every arm wrote a complete receipt and ledger entries | `overhead-replay/pilot/ratchet-main-t-remove/rows.jsonl` for tree paths and base shas; per tree, count fenced `handoff` blocks added and read the newest final block, **skipping any whose `session:` line contains `<`** | newest receipt `status: complete` in 15 of 15, 13 to 16 fields; ledger entries added (`^+###` lines in `CHANGELOG.md`): R0 4,4,4,4,6; R1 6,5,5,5,3; v3.0 2,3,4,2,4; `SESSION_NOTES.md` touched in 15 of 15. **R0 rep 5 holds two sessions (S555 and S556, newest receipt S556, $4.89)**; left out of the comparison: v3.8 arms 4.44 per run (n=9), v3.0 3.00 (n=5), Welch t = 2.70 (the reviewer: 2.699, df 7.5), unadjusted |
| 6 | pending receipts at the end | same, counting `^status: pending` in the final `HANDOFFS.md` (raw `grep -c`, fenced or not, gives the same) | 2 of 15 (R1 rep 5, v3.0 rep 1); the start commit has 1; the newest receipt is complete in both, so the pending one is the start-state S554 stub. `SESSION_NOTES.md` has 5 to 8 lines matching `CHANGELOG: pending\|status: pending\|IN PROGRESS` in every tree and **7 at the start commit**: prose and history, not stubs |
| 7 | reconcile or backfill commits | subjects matching `backfill\|reconcile` after the install base | v3.0 0,1,1,0,0 (2 of 5); R0 1,2,1,1,2; R1 1,1,1,1,0; v3.8 arms with R0 rep 5 left out: 8 of 9 (Fisher two-sided p = 0.095, reproduced by the reviewer, 0.0949, against v3.0's 2 of 5). Read: R0 rep 1 backfilled `402a6b5b..c122b876` = the S554 claim **and the install commit**; R1 rep 1 "backfill S554 claim-only session and v3.8 methodology install"; v3.0 rep 3 "Phase 0 reconcile (S554 abandoned claim, methodology v3.0 install)"; v3.0 rep 2 "reconcile S554 ghost session (claimed, no deliverable)" |
| 8 | the project's rules carry v3.8-era behaviour into the v3.0 arm | `git -C /tmp/ratchet-main/v3.0-r1 show HEAD:HANDOFFS.md` newest block | v3.0 rep 1 wrote a 14-field receipt whose `next_steps` asks whether the v3.0 install "dropped the Phase 0 CHANGELOG/HANDOFFS reconcile, the CHANGELOG: pending claim marker and the HANDOFFS receipt requirement that CLAUDE.md still references" |
| 9 | the project's `CLAUDE.md` at the ratchet start | `git -C ~/Development/nprcgenekeepr show 402a6b5b:CLAUDE.md \| wc -c` | 33,848 B with ledger, reconcile and ghost-session rules in its own adaptations |
| 10 | `879503cce` carries no documentation rules | `git -C ~/Development/nprcgenekeepr show 879503cce:CLAUDE.md \| wc -c`; `grep -c -i` for `HANDOFFS`, `CHANGELOG`, `reconcil`, `ghost`, `ledger`, `Phase 1B`, `receipt`, `check-handoff`, `FRAMEWORK_LEARNINGS`; `show 879503cce:SESSION_NOTES.md \| wc -c`; `git rev-list --count 879503cce..7e3752397` | 9,172 B, all nine counts 0; notes 3,850,762 B; runner 31,785 B (the identical blob at S323, per the reviewer); S323 is 10 commits later and a descendant; date 2026-07-08 |
| 11 | S323 is a pre-upgrade state | the same greps on `7e3752397:CLAUDE.md` (case-insensitive) and on its runner (case-sensitive); `git rev-parse --short 0c3af8b9f^`; `git rev-list --count 7e3752397..0c3af8b9f` | `CLAUDE.md` 9,805 B, all nine counts 0; runner 31,785 B with `HANDOFFS` 0, `reconcile` 0 (**a case-insensitive `HANDOFFS` count on the runner is 1**, the prose "plan-mode handoffs"); the upgrade `0c3af8b9f` (S324, 25 files, +2,143 / -143) has parent `7e3752397`, 1 commit between; `HANDOFFS.md` first added by `0c3af8b9f` (`git log --diff-filter=A`) |
| 12 | the S323 runner is v2.6.x | `diff <(git show 7e3752397:SESSION_RUNNER.md) <(git show "refs/tags/${t}:starter-kit/SESSION_RUNNER.md") \| grep -c '^[<>]'` | v2.6.1: 4; v2.6.2: 4; v3.0: 54 (no `v2.7.0` tag) |
| 13 | the removal task's targets and every other mention at S323 | `git grep -l -E 'resetGroup\|chooseAllelesChar' 7e3752397 -- . ':!R/resetGroup.R' …`; `git ls-tree --name-only 879503cce R/` | both R files and both test files exist at both commits; other files at S323: `CHANGELOG.md`, `PROJECT_LEARNINGS.md`, `SESSION_NOTES.md`, `TECH_DEBT_AUDIT_2026-05-30.md`, `docs/planning/issue112-genetic-diversity-dashboard-plan.md`, `docs/planning/phase8e-assertion-strengthening-subplan.md`, `inst/_pkgdown.yml` (lines 124 and 242), `test_results_summary.md`; at `402a6b5b` the same planning files and summary plus two archives, and no `inst/_pkgdown.yml` hit |
| 14 | `inst/_pkgdown.yml` is dead | `git -C ~/Development/nprcgenekeepr ls-tree --name-only 7e3752397 \| grep -i pkgdown`; `git show d14cd913d` | root `_pkgdown.yml` exists at S323; commit `d14cd913d` (S354, 2026-07-11): root `_pkgdown.yml` "shadows `inst/_pkgdown.yml`", which "was therefore never read" |
| 15 | the project's own adaptations at S323 carry no documentation rule | `git show 7e3752397:CLAUDE.md \| sed -n 153,175p`; `grep -n -i 'pkgdown\|NEWS'` | "Additional Phase 0 steps: (none)"; one close-out check about citations; no pkgdown line |
| 16 | handoff scores are compressed | `cat HANDOFFS.md docs/archive/HANDOFFS-*.md \| grep -E '^(predecessor_score\|self_score):' \| sort \| uniq -c` | `predecessor_score` 5:1, 6:4, 7:37, 8:127, 9:102 (271; 266 are 7 to 9); `self_score` 4:3, 5:1, 6:12, 7:59, 8:182, 9:15 (272) |
| 17 | `bin/sync` and the ledger; the trimmer's scope | `grep -n -i -E 'changelog\|ledger' bin/sync`; `git show refs/tags/v3.8:starter-kit/methodology_trim.py \| grep -n 'LedgerSpec('` | no output from the first; specs at `:303` (`CHANGELOG.md`) and `:328` (`HANDOFFS.md`) only. `git -C /tmp/ratchet-main/R0-r5 log` shows S556's commit `9f45cebf` "restore local SESSION_NOTES.md LedgerSpec in methodology_trim.py (dropped by v3.8 sync)" |
| 18 | spend | `pilot/ratchet-pressure-t-erode/spend.jsonl` summed (39 lines); `/tmp/overhead-real/spend.jsonl`; `pilot/rows.jsonl`; `pilot/xhigh-go/rows.jsonl`; `CHANGELOG.md:254` | $109.51; $44.55; $1.27; $3.92; $0.25 and $0.113. The five ratchet ledgers are cumulative: summing all five gives $324.05 and is wrong. $175 − $109.51 − $44.55 = **$20.94**; less the other $5.55 = **$15.39**; $125 − $109.51 = $15.49 |
| 19 | the driver's cap mechanics | `sed -n 4p`, `:145-152` of `overhead-replay/driver.py`; `run_main.py:25` | default `--session-cap 2.0`, `--total-cap 10.0`; `:151` refuses when `before + a.session_cap > a.total_cap`; `run_main.py` defaults session cap $10, total $100 |
| 20 | rules on stale references, both runners | `git show "refs/tags/${v}:starter-kit/SESSION_RUNNER.md" \| grep -n -i -E 'dangling\|stale'` for v3.0 and v3.8 | v3.0: line 35 (an unrelated "stale, cross-contaminated log"), **108** ("equivalent to 'grep for dangling references' in execution sessions"), **350** (learning 7, "Cross-reference completeness at self-review"); v3.8: line 46 (the same unrelated one) and **122** (the "dangling references" line). *Verify cross-references added or changed* is in both (row 4). `FRAMEWORK_LEARNINGS.md` Learning #10 ("a review pass scoped to the diff has a blind spot: what the change made stale *outside* it") is **inline in the v3.7 runner** (line 382) and in the on-demand sibling at v3.8 |
| 21 | the record's size at the start states | `git -C ~/Development/nprcgenekeepr show <sha>:<file> \| wc -c` and `wc -l` for `SESSION_NOTES.md`, `CHANGELOG.md`, `HANDOFFS.md` at `7e3752397` and `402a6b5b`; `grep -n -E '262,144' CHANGELOG.md` | S323: notes 3,938,380 B / 11,738 lines (15.02 × 262,144), ledger 932,452 B (3.56 ×), no `HANDOFFS.md`; `402a6b5b`: 165,980 B / 1,946 lines, 48,906 B, 74,858 B. The S323 notes open with `## ACTIVE TASK` at line 7. `CHANGELOG.md:121` names `READ_REFUSE_BYTES`, the 262,144 B hard read refusal |
| 22 | perishable data | `du -sh /tmp/ratchet-main /tmp/ratchet-control /tmp/ratchet-control-v2 /tmp/overhead-real`; `uptime`; `ls -d ~/.claude/projects/-private-tmp-ratchet-* ~/.claude/projects/-private-tmp-overhead-real-*`; `grep cleanupPeriodDays ~/.claude/settings.json` | 2.5 GB, 1.1 GB, 665 MB, 1.8 GB; up 11 days; 51 transcript directories in all, 72 MB (the ratchet pattern alone matches 38); `cleanupPeriodDays: 365` |
| 23 | S237's saved runs: cost and completeness | `overhead-replay/pilot/real-3.7/rows.jsonl`: `cost_usd`, `complete`, `incomplete_reason` | all rows: v3.0 6 rows mean $2.56, v3.7 7 rows mean $2.91. `complete` true: v3.0 reps 1,3,4,5,6 (5; rep 2 cut off at the stop limit); v3.7 reps 2,3,4,5,6,7 (6; rep 1 ended at stop limit 4). `RESULTS.md`'s five-per-version cost table drops v3.7 rep 5 (closed out partial at the RED gate): its five v3.7 costs are $3.00 to $3.41 ($3.20 mean), the v3.0 five $2.27 to $3.01 ($2.69). v3.0 rep 4's held-out result is `[4,0,0]` (reviewer, `held_out_results.json`) |
| 24 | `commit: pending` is a legal value | `bin/check-handoff:54`; the newest receipt of each T-remove tree | "It may legitimately read `pending`"; 7 of the 15 newest receipts read `pending` |
| 25 | the CLI | `claude --version` | 2.1.288; the ratchet plan §3.1 records 2.1.285 for S237's runs; the rows carry no version field |
| 26 | the arms registry | `grep -n 'ARMS' overhead-replay/install_arm.py overhead-replay/ratchet_arms.py` | `install_arm.ARMS` = v1.0.0, v2.0, v2.7, v3.0, v3.3, v3.7, HEAD, none; `ratchet_arms.py:30-31` appends `v3.8` at import |
| 27 | the T-control batches: v3.8 text on `879503cce`, issue #121 | `overhead-replay/pilot/ratchet-control-t-control/rows.jsonl` and `…-reply-fix/rows.jsonl`: `project`, `task`, `arm`, `cost_usd`, `end` | 8 + 5 = 13 rows, all `nprcgenekeepr@879503cce`, task `t-control`; R1 $2.34, 2.77, 4.21, 2.40, 2.16; R0 $5.29, 3.27, 3.01; fixed-reply R1 $3.43 (cut off after 10 stops), 4.71, 3.54, 3.09, 4.68; mean **$3.45**, max $5.29, **4 above $4**. The report records that two old-reply R1 runs stopped at the project's RED phase on an ambiguous close-out reply |
| 28 | the T-control held-out entry | `grep -n 'def held_out_task' overhead-replay/ratchet_arms.py`; `held_out.py` lines 1-40 | `ratchet_arms.py:122`; `held_out.py` is hard-wired to `/tmp/overhead-real/<arm>-r<rep>` and a `RUNS` dict of S237's runs, with end shas `7b9bd618` (v3.7 rep 2) and `b15ae1c5` (v3.0 rep 3) |
| 29 | what v3.8 changed from v3.7 | `git diff --numstat refs/tags/v3.7 refs/tags/v3.8` | largest: `tools/test_methodology_trim.py` +2,259, `starter-kit/methodology_trim.py` +2,181 (new), `tools/test_context_budget.py` +1,369, `starter-kit/context_budget.py` +825/−99, `quality_ratchet.py` +592 (new), `ITERATIVE_METHODOLOGY.md` +54/−333. The first reviewer: runner 22 `<` lines (17,018 B) and 10 `>` lines (5,106 B) differ, v3.7's runner 11,888 B larger; v3.0 against v3.7 is 51 lines by the same metric |
| 30 | sample size | a stdlib Monte Carlo of a pooled two-sample t-test at d/σ = 0.2/0.15, 40,000 draws per n | power 0.76 at n=9 per arm, 0.80 at n=10 (the reviewer got the same by a different simulation) |
| 31 | the installer's simplifications | `install_arm.py` docstring | "README.md is not installed; customisation steps (Task Mapping table, hooks, dashboard setup) are not applied" |
| 32 | a v3.8 arm builds | the first reviewer's scratch `ratchet_arms.build('v3.8', …, task='t-control')` | succeeded, 53,252 B runner; seeds land without their leading dot, so `context_budget.py --status` refuses (not re-run by me) |
| 33 | **crude** look at the saved trees (a scratch script, not committed; regex only) | per tree, base = the "Install methodology arm" commit; deleted lines in `SESSION_NOTES.md`, `CHANGELOG.md`, `HANDOFFS.md`; distinct 7 to 40 hex tokens with a letter and backticked paths with a doc or code extension in the added lines, resolved with `git cat-file` and `git ls-files` | 26 trees (real-3.7 13, T-control 13): **92** deleted lines (includes the receipt file, whose stub overwrite deletes lines); cited shas 152 distinct, **134 resolve**; backticked paths 560, **545 exist**. Not a measure: regex noise is unread |

| 34 | **S256 re-run before P1a** (two `bash` scripts in the session scratchpad; the commands are those of the rows named) | **re-run and reproduced:** rows 1-4, 9-15, 17-24, 26-29 (and row 31's docstring read). **Re-run, with drift:** row 16 now reads `predecessor_score` 9:103 and `self_score` 7:60 (S255's own receipt, 272 and 273 values); row 25: `claude --version` is **2.1.289**. **Not re-run:** rows 5-8 (scratch tallies of the T-remove trees, replaced by the tested scorer; its calibration found `status: pending` left by the session in none of the ten R0 and R1 trees, consistent with row 6), row 30 (Monte Carlo), row 32 (the reviewer's scratch build), row 33 (a crude regex, replaced by M1, which P1b measures). **New facts P1a produced:** the 41 trees all still existed (machine up 12 days); CLI per run 2.1.285 x7, 2.1.286 x14, 2.1.287 x20; 38 of 41 reach a close-out; 38 of 41 have no tracked uncommitted file |

**Corrections to BL-94's "what is known" (S244), not edited there:** "a `status: pending` receipt stayed pending in most trees" reads
2 of 15 by row 6, and in both it is the start-state's stub. "The same 3 tracked documents naming the removed functions" is
consistent with the ratchet plan §3.3.2's list at `402a6b5b`; row 13 shows the full list at S323 is longer, and none is a live
document.

The scratch scripts that produced rows 5 to 7 and 33 were written in the session scratchpad and are **not committed**; P1a (c)
rebuilds them as a tested scorer.

---

## §11 Independent reviews (S255): what they found and what was done

A fresh read-only reviewer re-ran every §10 row and attacked the design (review 1); the recomposed plan went to a second reviewer
(review 2). I re-verified each finding before acting on it. **The first draft was wrong in four ways, the second in three more.**

### Review 1

| Finding | Verified how | Disposition |
|---|---|---|
| The saved real-3.7 runs start at a commit with no documentation rules, so v3.0 against v3.7 is already a real contrast; the first draft called them "same project rules" | rows 10, 4, 23 | **Accepted; the design was recomposed around it** |
| The one "living" file for M3, `inst/_pkgdown.yml`, is dead | row 14, `d14cd913d` | **Accepted; M3 has no target and a search is P2a** |
| Row 12 omitted three files that name the helpers | row 13 | **Accepted; corrected** |
| Finding 3 overclaimed that the v3.8 trim tool fits the notes file; sessions following the size rule move history | row 17 | **Accepted; the moved-line rule (§2.2, since revised by review 2)** |
| M4's key is recoverable from git | reasoned | **Accepted; git-derivable facts and a git-only control (§2.3)** |
| M3 "history rewritten" would flag compliant sessions; M2 would flag legal `commit: pending` | row 24 | **Accepted; both redefined (§2.3)** |
| Spend mechanics: driver's default session cap $2.00; the pilot's n=1 gives no spread | row 19 | **Accepted; per-session caps stated; `σ` from P1b** |
| "Same footprint in every arm" contradicts row 5's gap | recomputed | **Accepted (finding 1)** |
| "`git status` shows no change" cannot fail; the arms-differ STOP cannot fire | reasoned | **Accepted; `git diff <start sha>..HEAD`; the build check is a sanity check** |
| Session 2 had no pinned sha | reasoned | **Accepted (§2.5, §3.5)** |
| Rows 10, 20 and the "ten files" were imprecise | recounts | **Accepted; corrected** |
| "$20.94 left" stated as fact; other recorded spend exists | row 18 | **Accepted; both figures** |
| S323's runner is v2.6.x, so an as-was arm is a near-twin of v3.0 | row 12 | **Accepted; the third arm was dropped** |
| 2.1 rests on a runner-only grep | row 20 | **Accepted; scoped** |

### Review 2

| Finding | Verified how | Disposition |
|---|---|---|
| **The T-control batches are 13 v3.8-text runs on the same start state and task, and the plan never scored them; this could replace most new v3.8 runs** | row 27 | **Accepted; a third saved set (§1), arms (§3.3), P1b scores them, new v3.8 runs become P3b and conditional** |
| `complete` gives 5 v3.0 and 6 v3.7 rows, not "five valid" each; the bridge range "$2.02 to $3.41" used the excluded rep 5; selecting by cost-validity drops the honest partial and keeps v3.0 rep 4 | row 23, `held_out_results.json` | **Accepted; §2.5 inclusion rule (every run that reached a close-out; cost and correctness are covariates)** |
| "Saved v3.8-era cost not known" is false: $3.45 over 13, four above $4; a $4 task cap would truncate about 30% | row 27 | **Accepted; the cap is $6 (P3b)** |
| P3's "re-run the saved arms for $27" is an unapproved automatic escalation; a one-run bridge cannot fail | reasoned | **Accepted; the bridge run is removed; pooling is checked on free rows (P1b)** |
| The n=9 / $105 and n=5 / $12 lines mis-add; n=9 at 80% power is about 10 by a t-test | recomputed (rows 30, plan §5) | **Accepted; the sample-size text and the P3 arithmetic were rewritten** |
| "32 diff lines" cannot carry the weight; v3.8 adds the trimmer, ratchet, context-budget changes and an extracted manual | row 29 | **Accepted; finding 3 and §3.3** |
| Learning #10 is inline in the v3.7 runner; "v3.8 adds it" overcredits | row 20 | **Accepted** |
| "v3.8 as released" overstated: the harness lands seeds without the dot | row 32 (reviewer's build) | **Accepted; the arms are "as the harness installs them"; flagged as not re-run by me** |
| The §2.2 base-tree subtraction hides verbatim carry-forward of a stale line | reasoned | **Accepted; replaced by a moved-line rule** |
| M1 may be at ceiling; "line within the file" is nearly vacuous | row 33 (mine: 134 of 152 shas, 545 of 560 paths) | **Accepted in part: ceiling rule and an identifier-near-anchor check added; my crude count shows some spread in shas, so M1 is not assumed uninformative** |
| Freeze-then-score has no parse check and no amendment rule | reasoned | **Accepted; P1a (d) and §4 item 1** |
| `format-patch` rebuilds commits with different shas than the records cite; use `git bundle` | reasoned | **Accepted (§3.5, P1a (a))** |
| "One session" for P1 contradicts its six deliverables; the ratchet study's P1 took four sessions | `CHANGELOG.md` | **Accepted; P1a, P1b and P2a are separate sessions (§5)** |
| M2(b) is vacuous for v3.0; "computed by script, never by reading prose" is false for M2(c) and M3's "discloses" | reasoned | **Accepted; M2 parts reported separately, (b) "not applicable" for v3.0; the two keyword rules are named** |
| A found M3 task needs a second start state and no budget covers it | reasoned | **Accepted; said so (§3.4)** |
| The rater has no driver-enforced cap; CLI versions drifted across batches | reasoned; row 25 | **Accepted; the rater gets its own cap; each run's CLI is read from its transcript (P1a (a))** |

**Not checked by the reviewers, and not by me:** whether the $175 covers the other recorded spend; the project's R suite time; every
model-behaviour prediction (H1 to H5); the CLI versions between 2.1.285 and 2.1.288; the probe and rater costs.
