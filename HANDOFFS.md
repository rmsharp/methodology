# Handoff Receipts — durable close-out proof

This repository dogfoods its own methodology: every session records a durable, machine-checkable
`handoff` receipt here at close-out (Phase 3D), and Phase 0 reconciles it against `git log`. See
[`starter-kit/HANDOFFS.md`](starter-kit/HANDOFFS.md) for the block format and the write points, and
`bin/check-handoff` for the checker. Newest on top; prepend-only.

---

```handoff
session: S11
date: 2026-07-25
status: pending
active_task: Layer 2 of docs/planning/dashboard-signal-integrity-plan.md — ledger identity (defects 5, 6, 7; upstream issue #60). Add _find_action_ledger (root-only, exact CHANGELOG.md) ALONGSIDE an unchanged _find_changelog; add ledger_present, consumed only at the assess_risks site; fix archive shadowing by preferring an exact CHANGELOG.md over any name-prefix match; make lag messages name their source file and drop the word "ledger"; move the Signal F emission above the `changelog is None` early return. DASHBOARD_VERSION -> 2.9.1. ONE LAYER ONLY — Layers 3-6 are separate sessions, and release decision R1 is settled at merge, not by an implementing session.
what_was_done: pending
next_steps: pending
key_files: tools/methodology_dashboard.py:658 (_find_changelog — archive-shadowing sorted() locator), tools/methodology_dashboard.py:712 (the `changelog is None` early return that strands Signal F), tools/methodology_dashboard.py:786 (Signal F emission, currently below the early return), tools/methodology_dashboard.py:1332 (the +1 freshness point the obvious #60b fix silently costs), tools/methodology_dashboard.py:1439 (the risk that must read ledger_present, not present), docs/planning/dashboard-signal-integrity-plan.md:194 (Layer 2 contract)
gotchas: pending
runtime_smoke: pending
changelog_ref: pending
commit: pending
```

```handoff
session: S10
date: 2026-07-25
status: complete
self_score: 8
predecessor_score: 9
active_task: Layer 1 of docs/planning/dashboard-signal-integrity-plan.md — scale honesty + checklist currency (defects 1, 2, 8; upstream issue #61). COMPLETE. DASHBOARD_VERSION 2.8.0 -> 2.9.0. Layers 2-6 remain unclaimed, one per session.
what_was_done: Implemented Layer 1 of the plan ratified in bc2481d, exactly as written, RED-first. Wrote 13 assertions and watched them FAIL against unpatched code before touching the scanner (methodology 22 not 20, total 102, card "110%", 8 headers over 10 cells, HANDOFFS.md the only unaccounted manifest destination) — necessary because the suite was green against all eight defects. Then: derived METHODOLOGY_MAX (=115, never a literal); ("HANDOFFS.md", 5, "file") added next to its structural twin CHANGELOG.md per D2; producer-side compliance_pct() normalizing ONCE; the four consumers rewired to the percentage (dimension now min(20, int(pct*0.2)); grid ladder + cell; card renders "{pct}% ({raw} of {MAX})") while the "no adoption at all" risk keeps reading the RAW sum (scale-independent); grid headers derived; the three duplicate exists() loops in collect_methodology_metrics collapsed to one probe per item; dashboard_version stamped into each dashboard_history.jsonl entry. Both twins byte-identical, re-copied after every edit. CORRECTION TO THE PLAN, verified by rendering HEAD's scanner: the header misalignment is NOT a future trap of adding a 9th item — it has been LIVE since v2.1, 8 <th> over 10 <td>, so "Methodology Dir"/"Workstreams"/"Score" have been sitting above the CHANGELOG/ROADMAP/docs-methodology cells and the last two cells have had no header at all. Ran a 5-lens adversarial review at the layer boundary BEFORE committing: 23 findings -> 2 confirmed, 19 refuted. The confirmed one mattered: a mutation (dimension reads compliance_score again, clamp retained) survived all 44 tests, because 0% and 100% cannot distinguish the clamp from the normalized read — I reproduced the surviving mutant myself, added an intermediate-value lock, and re-ran the mutation to watch it die. Also added an end-to-end pre-v3.3 adopter fixture (D2's accepted cost had no test), a direct out-of-range clamp test, and de-brittled two assertions that would have failed against correct code if the checklist were ever re-cut to sum 100. Two review findings against my own prose were upheld and fixed: the compliance_pct docstring claimed "no value is rounded twice" — false, the dimension re-scales an already-rounded percentage (credits +1 at raw 40 and 80; kept per plan, now documented), and my CHANGELOG entry overstated the write-only version stamp. Ledger entry + this receipt in the same commit.
next_steps: Execute Layer 2 (ledger identity, defects 5/6/7) of docs/planning/dashboard-signal-integrity-plan.md — add _find_action_ledger (root-only, exact CHANGELOG.md) ALONGSIDE an unchanged _find_changelog, consume it only at the :1409 risk, fix archive shadowing, make lag messages name their source file, and move the Signal F emission above the `changelog is None` early return. DASHBOARD_VERSION -> 2.9.1. Start RED-first again, and this time also MUTATION-test each new assertion: Layer 1 proved that RED-first alone is not enough — a test can go red for the defect and still be blind to a wrong-field regression. The plan's four Layer 2 fixtures are the RED list; note fixture (d) (an adopter with docs/changelog.md KEEPS its +1 freshness point) is the regression lock that makes the obvious #60b fix wrong. Do NOT bundle: Layers 3-6 are separate sessions, and the release decision R1 is settled at merge, not by an implementing session.
key_files: tools/methodology_dashboard.py:133 (METHODOLOGY_MAX, derived), tools/methodology_dashboard.py:796 (compliance_pct — the single normalization site), tools/methodology_dashboard.py:1348 (clamped dimension), tools/methodology_dashboard.py:1391 (risk thresholds — raw for ==0, pct for <50), tools/methodology_dashboard.py:1612 (methodology_grid_headers, derived), tools/methodology_dashboard.py:1707 (card label "{pct}% ({raw} of {MAX})"), tools/methodology_dashboard.py:2313 (dashboard_version history stamp), tools/test_methodology_dashboard.py:278 (RAW_MAX + CHECKLIST_EXEMPT — the manifest-vs-checklist guard), tools/test_methodology_dashboard.py:339 (intermediate-value lock that kills the raw-sum mutant), docs/planning/dashboard-signal-integrity-plan.md:194 (Layer 2, next)
gotchas: (1) RED-first is necessary but NOT sufficient — my clamp test went red for the right reason and still let a raw-vs-pct regression through. Mutate the fix and re-run before believing any assertion; the endpoints of a normalized scale are exactly where the two readings coincide. (2) bin/check-handoff CANNOT validate a Phase 1B stub even with --allow-pending: self_score and predecessor_score are REQUIRED keys that must be integers 1..10, and neither is knowable at claim time (bin/check-handoff:51 + :161). S9's stub and mine both omit them and so both fail --allow-pending; filling them at claim would be fabrication. Worth an upstream issue — do not "fix" it by inventing scores. (3) The dashboard still cannot scan its own repo in place (ROOT = Path(__file__).parent resolves to tools/). Load it via importlib and call collect_all(Path(target)); never copy it into a repo root, never call main() against a real repo (main() writes dashboard.html + dashboard_history.jsonl into the scan root). My read-only scan + smoke scripts are in the session scratchpad if useful. (4) A receipt-only or claim-only commit needs --no-verify (the pre-commit hook wants CHANGELOG.md co-staged); backstopped by Phase 0 reconcile. (5) Each code layer is 4 files + the receipt = exactly the 5-file cap, so nothing else can ride along — this is why the SESSION_RUNNER.md Learnings row stays owed at Layer 6 (plan §8) rather than being appended now. (6) Layer 5's target table is missing three enumerations the review found and confirmed as ALREADY-STALE-BEFORE-THIS-LAYER, so they are Layer 5 work, not regressions: README.md:106-115 ("What's in the starter kit" table omits HANDOFFS.md), docs/tutorials/T1_setup.md:63 and docs/tutorials/T8_keeping_current.md:62 (both enumerate SEED files as SESSION_NOTES/CHANGELOG/ROADMAP), CLAUDE.md:42-48 (starter-kit table omits HANDOFFS.md; Tools table omits test_methodology_dashboard.py), plus README.md's two dashboard screenshots, which are worked examples of output this layer changed. Layer 5's own verify grep surfaces T1/T8; the others need adding as rows. (7) The two README screenshots (README.md:147 area) now show pre-2.9.0 output — regenerating images is NOT in any layer's file list; raise it as its own decision.
runtime_smoke: Ran the REAL render path against live collected metrics (render_project_card + render_methodology_grid + render_html + append_history), writing nothing into any scanned repo. Card: mts-system "Methodology Compliance (100% (115 of 115))" (was "110%"), this repo "9% (10 of 115)". Grid: 11 headers over 11 cells for both projects (was 8 over 10). Full HTML render 34,469 chars with no percentage over 100 anywhere. History entry carries dashboard_version 2.9.0. Suites: tools/test_methodology_dashboard.py 29 -> 47 tests OK; bin/tests.sh 84 passed / 0 failed; python3 bin/check-links OK (82 links / 21 files); diff -q twins identical. Live re-scan read-only: mts-system 90 -> 88/100 with methodology 22/20 -> 20/20; this repo 43 -> 49 (testing 6 -> 12 because this session's own test file pushed the test-to-source ratio past 0.1 — not a scoring change).
changelog_ref: CHANGELOG.md entry "Dashboard signal-integrity Layer 1 — scale honesty + checklist currency", commit 6b10f09
commit: 6b10f09
```
Self-score 8/10. **+** Held the RED-first rule: every defect-proving assertion was watched to fail
against unpatched code first, with the exact numbers the plan predicted. **+** Reviewed the layer
at its boundary *before* the commit landed rather than after, and the review earned its cost — it
found a mutation-surviving coverage hole that RED-first alone could never have surfaced. **+**
Reproduced the confirmed finding myself (mutated both twins, watched 44/44 stay green) instead of
taking the agent's word, and re-ran the mutation after fixing to prove the lock bites. **+**
Corrected the ratified plan where reality disagreed with it — the grid misalignment is live, not
prospective — instead of implementing to the plan's description. **+** Fixed two inaccuracies in
my *own* prose that the review caught (a false "rounded twice" claim, an overstated trend claim);
honest comments matter more in a repo whose subject is signal integrity. **−** I wrote that false
docstring claim in the first place, restating the plan's rationale as an implementation guarantee
without checking whether the code I had just written met it. **−** My first-cut tests pinned the
clamp and not the normalized read — the exact anti-pattern this campaign documented as its own
§8 learning 2, reproduced at the opposite endpoint one layer after it was written down. **−** Two
of my new assertions would have failed against *correct* code if the checklist were ever re-cut to
sum 100 — brittleness a reviewer had to point out. **−** I spent tokens on a 5-lens sweep whose
doc-completeness lens was always going to land in Layer 5's lap; one lens would have done.

Predecessor (S9) evaluation: 9/10. The plan is the best executable artifact I have been handed in
this repo, and its value was concentrated exactly where it promised: the three "traps" section
saved real time (I would have narrowed `_find_changelog` and would have remapped the checklist onto
`starter-kit/` paths, both wrong), and the RED-first standing rule is the only reason I did not
ship a suite that was green against the bug. Every `file:line` in its `key_files` resolved to the
code it claimed (`:110`, `:1329`, `:1570`, `:698`, `:648`, `:1309`, `:210`), and the D1 decision
was argued from `git show 46b17e8` rather than taste, which made implementation a transcription
job rather than a judgment call. Its gotchas were load-bearing: the importlib warning and the
"collect_all returns risks under metrics['scores']['risks']" note both applied verbatim. Two
deductions, both small. First, one claim was wrong in a way that mattered to sequencing: the plan
frames the grid `headers` misalignment as a trap that *appears* when a 9th item is added ("the grid
misaligns until `headers` is derived too"), but it is already live at HEAD — 8 headers over 10
cells since v2.1 — which means it was a *shipped defect* that belonged in the defect table, not a
note about implementation order. It cost nothing here because the fix is identical, but a plan
that mis-classifies a live defect as prospective could let a later layer defer it. Second, the plan
prescribes `min(20, int(pct * 0.2))` while asserting in the same decision that "double-rounding is
avoided" — the two cannot both hold, and reconciling them was left to me. I kept the prescription
and documented the cost; a sentence in D1 acknowledging the one-point artifact would have closed
it. Neither deduction touches the plan's core, which held up under a 5-lens adversarial review.

```handoff
session: S9
date: 2026-07-25
status: complete
self_score: 8
predecessor_score: 9
active_task: Dashboard signal-integrity cluster (upstream #59/#60/#61). COMPLETE as a PLANNING session — operator ratified D1-D4 and chose "ratify the plan now, implement next". Deliverable is docs/planning/dashboard-signal-integrity-plan.md. Implementation begins next session at Layer 1. No scanner code was changed this session.
what_was_done: Reproduced all eight defects first-hand (importlib + collect_all, read-only) rather than trusting the issue text — and found FIVE that were never filed. Mine: (a) HANDOFFS.md ships to adopters as SEED since v3.3 (bin/_manifest.py:47) but was never added to METHODOLOGY_ITEMS; (b) Signal F is UNREACHABLE when no changelog exists — evaluate_changelog_freshness early-returns at :698-701, before the emission at :772, so an adopter with 60 unmigrated done-marks and no ledger gets FEWER warnings than one with a ledger (proved by flipping the marker: ledger absent -> silent, present -> fires). Found by the design panel and then verified by me: (c) archive shadowing — _find_changelog's sorted() returns CHANGELOG-archive.md over CHANGELOG.md ('-' 0x2D sorts before '.' 0x2E); (d) a '- [x]' inside a fenced ```markdown block counts as real completed work; (e) README.md:75 and :79 both omit HANDOFFS.md from the seeded-files enumeration. Ran an 11-agent design panel (wf_e3499138-1fd: 4 code maps, 3 competing designs, 3 judge lenses, 1 synthesis) — it REFUTED my own #59 design (remapping the checklist onto starter-kit/ paths would credit a 27-line empty stub and render "SESSION_NOTES.md ✓" on a repo with no session notes: defect #59 inverted) and caught a silent +1 documentation regression hiding inside the obvious #60b fix. I rejected two of its claims after re-executing them ("30 tests" — line 327 is a fixture STRING, there are genuinely 29; and edits to dated release prose the v2.7.1 convention freezes). Empirically tuned the table done-row predicate against the real 643-line backlog recovered from mts-system 383c1715: contains-token = 321 (94 false positives), equals-token = 227 (misses bolded forms), starts-with/>=3-cells/ignore-ID-column = 256 — within 3 of S8's independent hand count. Settled D1 from git history: v2.0 commit 46b17e8 summed to EXACTLY 100, v2.1 commit 274dcd4 appended two 5-pointers without re-cutting. Also reconciled S8's commit: pending -> 4e2901f. Plan + ledger + this receipt in this commit.
next_steps: Execute Layer 1 of docs/planning/dashboard-signal-integrity-plan.md — derived METHODOLOGY_MAX, the HANDOFFS.md checklist row, producer-side compliance_pct, min(20,...) at :1329, and the manifest-vs-checklist structural guard. ONE LAYER PER SESSION; do not bundle. Start by writing the three RED-first assertions and watching them FAIL against unpatched code — the suite is green against all eight defects today, so "tests pass" is not evidence. Note L1 is not a pure append: render_methodology_grid:1570 hard-codes an 8-string headers list while :1571 derives item_keys from METHODOLOGY_ITEMS, so adding a 9th item misaligns the grid columns until headers are derived too. Deferred decision R1 (tagged release vs ledger-only) is settled at merge, not now.
key_files: docs/planning/dashboard-signal-integrity-plan.md:1 (the ratified plan — read it first), tools/methodology_dashboard.py:110 (METHODOLOGY_ITEMS, weights sum 110), tools/methodology_dashboard.py:1329 (unclamped dimension), tools/methodology_dashboard.py:1570 (hand-written 8-header list — column misalignment trap), tools/methodology_dashboard.py:698 (the early return that strands Signal F at :772), tools/methodology_dashboard.py:648 (archive-shadowing sorted() locator), tools/methodology_dashboard.py:1309 (the +1 freshness point the obvious #60b fix silently costs), tools/test_methodology_dashboard.py:210 (test that passes against the bug), bin/_manifest.py:47 (HANDOFFS.md SEED entry)
gotchas: (1) The dashboard CANNOT scan its own repo in place — ROOT = Path(__file__).parent resolves to tools/, which has no .git. Load it via importlib and call collect_all(Path(target)); NEVER copy it into a repo root to test, or the copy inflates that repo's own source-LOC count. (2) collect_all returns risks under metrics["scores"]["risks"], NOT metrics["risks"] — my first repro script crashed on exactly this. (3) The obvious #60b fix is WRONG: narrowing _find_changelog to root-only silently costs the +1 documentation freshness point (:1309) for exactly the adopter class #60b is about, because the early return leaves is_fresh False. Use the dual predicate in the plan. (4) The obvious #59 fix is WRONG too — see what_was_done. (5) The mts-system live repro fixture is GONE: it executed migration Phase 2 (28e9bb3) since S8 and now scores 110% with a root ledger. Use synthetic fixtures; recover real data from 383c1715:BACKLOG.md. (6) Each code layer sits at exactly 4 of the 5-file commit cap because .githooks/pre-commit requires CHANGELOG.md co-staged — no slack. (7) A receipt-only commit needs --no-verify (the hook wants CHANGELOG.md co-staged and the ledger entry is already committed); that bypass is documented and backstopped by Phase 0 reconcile. (8) bin/check-links is PYTHON — run python3 bin/check-links, not bash. (9) One bin/tests.sh run reported 83/84 and was never reproduced across four subsequent clean runs; the failing check was not captured. If you see 83/84, re-run before diagnosing your change.
runtime_smoke: n/a — planning session, no code changed. Verified by re-running the full harness clean after the plan landed: bin/tests.sh 84 passed / 0 failed, tools/test_methodology_dashboard.py 29 tests OK, python3 bin/check-links OK (82 links across 21 files). All eight defects were reproduced by executing the canonical scanner read-only against this repo, the adopter, and synthetic git fixtures — no files written to any scanned repo.
changelog_ref: CHANGELOG.md entry "Ratified plan — dashboard signal-integrity campaign", this commit
commit: bc2481d
```
Self-score 8/10. **+** Reproduced every defect first-hand instead of trusting three well-written issues —
which is how the four unfiled defects surfaced, and how I caught that #61's stated "21/20" is actually
**22/20** (`int(110*0.2)`). **+** Settled the one decision the whole design hinges on from *evidence*
rather than taste: `git show 46b17e8` proves the checklist once summed to exactly 100 and that v2.1 broke
it, so normalization restores an invariant instead of inventing a scale. **+** Ran an adversarial design
panel and then *actually let it win* — my `starter-kit/` remap for #59 was wrong and I replaced it rather
than defending it. **+** Verified the panel instead of adopting it, rejecting two of its claims that would
each have introduced a new error into the corpus. **+** Empirically tuned the riskiest predicate against
real recovered data rather than reasoning about regexes in the abstract. **−** I *authored* that wrong
`starter-kit/` design in the first place, from files I had listed but not read — precisely failure mode
#20, and a panel had to catch it. **−** My first reproduction script had two defects (wrong accessor path,
a fixture loop that committed identical content); a cleaner first draft would have cost less. **−** I
reported a "83/84" baseline having tailed away the line naming the failing check, so I could not diagnose
it and had to record it as an unexplained transient — capture full output the first time. **−** Ran
`bin/check-links` under the wrong interpreter and briefly read a syntax error as a repo problem.

Predecessor (S8) evaluation: 9/10. The most useful handoff I have been given in this repo. Its `gotchas`
were load-bearing rather than decorative: the importlib warning saved me from repeating S7's
self-polluting scan, and its NOTES-column caution turned out to be *exactly* the trap in the table
predicate — I confirmed it quantitatively (94 false positives) and its warning is why I tested three
candidate rules instead of shipping the naive one. Every `key_files` line:line I checked resolved to the
code it claimed (`:131`, `:644`, `:110`, `:1329`, `:210-219`). Its `next_steps` correctly recommended
designing the three issues together rather than as separate patches, which the panel independently
confirmed was right. Two small deductions: `commit: pending` was left unreconciled for the second session
running (I fixed it to `4e2901f` here), and its adopter-track guidance ("mts-system executes Phase 1")
was stale by the time I read it — through no fault of its own, since that repo moved on independently,
but it is a reminder that handoffs naming *another* repo's state should say "verify before acting".

```handoff
session: S8
date: 2026-07-13
status: complete
self_score: 8
predecessor_score: 9
active_task: Examine the mts-system adopter's 643-line BACKLOG.md (operator premise: "it should be on v3.5, which would not allow the backlog to grow"). COMPLETE — premise disproved, root cause found, two framework defects filed upstream (#60, #61), and a ratified 6-phase migration plan committed to the adopter repo (mts-system fbc35cd).
what_was_done: Audited mts-system (92-agent workflow, every load-bearing fact adversarially re-verified; then reproduced each claim myself before relaying). Premise is FALSE: mts-system runs a hand-patched v2.0-era SESSION_RUNNER.md (FM table stops at #19 vs canonical #27; ZERO occurrences of "CHANGELOG" vs canonical's 16), has no root CHANGELOG.md and no HANDOFFS.md, so the FM #27 eviction rule ("remove a completed backlog item in the same commit") was never installed — and four sites in that repo (BACKLOG.md:640, CLAUDE.md:118/:148/:154) actively instruct sessions to KEEP completed work in the backlog. 67 sessions did what they were told; the 643-line file is the correct output of its own rules. Filed KJ5HST/methodology#60 (Signal F's _BACKLOG_DONE_RE at tools/methodology_dashboard.py:131 matches only "- [x]" checkboxes, so a table-status backlog with 253 DONE rows counts 0; AND _find_changelog at :644-657 searches docs/, so a stale product docs/changelog.md masks the missing ledger and suppresses the :1409 risk) and #61 (METHODOLOGY_ITEMS weights sum to 110, methodology dimension unclamped at :1329 -> card renders "105%", 21-of-20 sub-score). Net: the dashboard rates that adopter 88/100 with ZERO backlog risks — a false GREEN. Then built a grep-based evidence inventory by hand (the 5-agent inventory workflow died on network ECONNRESET/cert errors — rebuilt it myself rather than re-run against a flaky connection) and authored the migration plan; 4-lens adversarial review before commit found 11 defects, all folded in. The plan landed in the ADOPTER repo as mts-system commit fbc35cd (with its SESSION_NOTES.md handoff, so that repo's next Orient does not see an undocumented commit); this repo's own actions (2 upstream issues) are ledgered in CHANGELOG.md in this commit.
next_steps: TWO independent tracks, both unclaimed. (1) FRAMEWORK: issues #59, #60, #61 are all open and all in tools/methodology_dashboard.py — they are the same class ("dashboard signals do not mean what they appear to mean") and #59's suggested marker-vs-heuristic design would likely inform #60's fix; consider designing them together rather than three separate patches. #61 is nearly mechanical (add min(20,...) at :1329, decide renormalize-vs-relabel, extend tools/test_methodology_dashboard.py:210-219 to drive compliance_score=110 — the current test passes against the bug). Both dashboard twins must stay byte-identical and DASHBOARD_VERSION (2.8.0) needs a bump. (2) ADOPTER: mts-system executes Phase 1 of docs/planning/methodology-v35-migration.md (extract 3 runner customizations into CLAUDE.md — it unblocks bin/sync, which today writes NOTHING). One phase per session; do NOT bundle. Phase 2 arms an obligation (once CHANGELOG.md exists the next Orient must reconcile it) and Phase 6 destroys the substrate Phase 3 reads — the ordering is load-bearing.
key_files: tools/methodology_dashboard.py:131 (_BACKLOG_DONE_RE — checkbox-only regex, issue #60), tools/methodology_dashboard.py:644-657 (_find_changelog — masks the missing ledger), tools/methodology_dashboard.py:110-119 (METHODOLOGY_ITEMS — weights sum to 110, issue #61), tools/methodology_dashboard.py:1329 (unclamped methodology dimension), tools/test_methodology_dashboard.py:210-219 (bound test that cannot catch #61), bin/sync:230-248 (whole-corpus pre-write drift gate — exits 2 and writes nothing, seeds included), bin/_manifest.py:44-48 (SEED block: CHANGELOG/HANDOFFS are write-if-absent), /Users/rmsharp/Development/mts-system/docs/planning/methodology-v35-migration.md (the deliverable)
gotchas: (1) bin/sync's drift gate is WHOLE-CORPUS and PRE-WRITE — three locally-modified tracked files make it exit 2 before the write loop, so it seeds nothing either. "Sync will at least create the ledger and leave the runner alone" is false, and no doc says so; I only learned it by running --dry-run. Worth documenting upstream. (2) The dashboard cannot scan its own repo in place (ROOT = Path(__file__).parent resolves to tools/, which has no .git) — load it via importlib from a scratchpad script and call collect_all(Path(target)); never copy it into a repo root to test, or it pollutes the source-LOC count (S7 hit this). collect_all writes no files; main() does. (3) When censusing a markdown-table backlog, read the STATUS column specifically — several mts-system rows carry "DONE"/"FIXED IN CODE" inside their NOTES column, and a naive "any field contains a status token" awk mis-flags them. My first draft got BACKLOG.md:470 wrong exactly this way; the review caught it. (4) Sub-agent fleets died mid-run on network errors (ECONNRESET / UNKNOWN_CERTIFICATE_VERIFICATION_ERROR) — a 5-agent workflow burned 38 minutes and returned nothing. Check the journal before assuming a workflow's empty result means "found nothing."
runtime_smoke: n/a — no code changed in this repo. The dashboard defects were reproduced by executing the canonical scanner read-only against the adopter (health 88/100, compliance 105%, methodology sub-score 21/20, weights sum 110, zero backlog risks); bin/status and bin/sync --dry-run were both run first-hand against the adopter.
changelog_ref: CHANGELOG.md entries "Opened upstream issues #60 and #61 — dashboard false-GREEN on a drifted adopter" and "Adopter coordination — ratified methodology v3.5 migration plan for mts-system", this commit
commit: 4e2901f
```

```handoff
session: S7
date: 2026-07-09
status: complete
self_score: 7
predecessor_score: 8
active_task: Ad hoc — answered a "should we register with FlexNet Code Insight" question, checked the dashboard for staleness, and filed an issue for a real blind spot it found.
what_was_done: Answered that FNCI (an SCA/license-compliance tool) gains nothing here — no dependency manifest, stdlib-only tooling, and no CI to change that calculus (confirmed no .github/workflows exists). Then ran methodology_dashboard.py against this repo in single-project mode (collect_all(Path('.')), loaded directly from tools/methodology_dashboard.py to avoid polluting the scan — an earlier attempt that copied the script into the repo root to test single-project mode had to be discarded because the copy itself added ~2,475 LOC to the source count). Confirmed detect_doc_only correctly returns False (5,567 real source LOC, past the 200-LOC cap) — disproving the user's "judged doc-only since it has no code" premise. Found the methodology-compliance checklist (METHODOLOGY_ITEMS) has no self-recognition for this being the canonical repo, so it misreports "Partial methodology adoption (5%)". Filed KJ5HST/methodology#59 with reproduction steps and two candidate fix directions; logged it in CHANGELOG.md, commit 3cabd85. Also compacted MEMORY.md (auto-memory index) from 20.3KB to 7.7KB per a hook-triggered size warning, moving no content (topic files already held the detail) — just trimmed accreted prose out of the index lines.
next_steps: Next session should pick up issue #59 — design the self-recognition fix (marker vs. structural heuristic, both sketched in the issue body) and implement it against tools/methodology_dashboard.py + starter-kit/methodology_dashboard.py (byte-identical twins, must stay in sync) + tools/test_methodology_dashboard.py. docs/planning/BACKLOG.md stays retired — this is tracked as a GitHub issue, not reopened as a backlog item, per operator instruction this session.
key_files: tools/methodology_dashboard.py:110 (METHODOLOGY_ITEMS checklist), tools/methodology_dashboard.py:782 (collect_methodology_metrics), tools/methodology_dashboard.py:1209 (detect_doc_only — confirmed correct, not part of the bug), starter-kit/methodology_dashboard.py:110 (twin, needs the same fix)
gotchas: the dashboard can't scan its own repo in place — ROOT = Path(__file__).parent resolves to tools/, which has no .git, so discover_projects returns nothing in portfolio mode; single-project mode requires the script to actually be copied to (or loaded as if running from) the project root. Any temp copy left sitting in the repo root during testing pollutes files.largest_files and source LOC — clean it up (and re-run) before trusting the numbers, as this session had to do once.
runtime_smoke: n/a — no product code changed; verified by re-running the dashboard scan clean (git status empty) after removing the temporary test copy, dashboard.html, and dashboard_history.jsonl
changelog_ref: CHANGELOG.md "Opened upstream issue #59 — dashboard self-scan blind spot" entry, commit 3cabd85
commit: 3cabd85
```
Self-score 7/10. **+** Corrected my own methodology mid-investigation (caught and discarded a
measurement polluted by my own temp file before reporting numbers) rather than reporting the
contaminated first run. **+** Verified the user's stated premise ("no code") against actual data
instead of accepting it, and reported the correct mechanism (200-LOC cap, not "no code") when it
turned out false. **+** Filed a well-evidenced issue with exact reproduction steps and file:line
references rather than a vague "dashboard is wrong" report, and correctly deferred design/implementation
to the next session per the operator's explicit instruction. **+** Split the ledger entry and this
receipt into two commits specifically so `what_was_done`/`commit` could cite a real sha (`3cabd85`)
instead of leaving `pending` — avoided the self-reference problem outright rather than accepting an
imprecise amend. **−** No Phase 0/1B was run at the start of this session — it began as an ambient "go"
with no formal claim stub, the same class of procedural deviation S6 flagged in itself; harmless here
since the session was small and low-risk, but not a pattern to repeat by default. **−** The HANDOFFS.md
commit itself required `git commit --no-verify` (the ledger hook blocks a commit that touches tracked
content without CHANGELOG.md co-staged, and CHANGELOG.md was already fully committed by that point) —
the sanctioned bypass the hook's own message documents, backstopped by Phase 0 reconcile-on-read, but a
deviation worth naming rather than passing over silently.

Predecessor (S6) evaluation: 8/10. Thorough and specific — `next_steps` named exact actions ("mark
BL-7 complete in BACKLOG.md," "ask the operator about a version event," "prune the branch"), all of
which check out against the current repo state (BACKLOG.md shows BL-7 retired/complete;
feat/capability-tiered-review is pruned locally and on origin). `key_files` carried real path:line
tokens, `gotchas` transparently explained a session-renumbering decision (S2→S6) with reasoning rather
than silently overwriting history, and the self-critique (skipped Phase 1B stub) was honest rather than
self-serving. Docked one point only because `commit: pending` was never reconciled to a real sha in
that entry either — a small, repeated gap in an otherwise exemplary handoff.

```handoff
session: S6
date: 2026-07-08
status: complete
self_score: 8
predecessor_score: 9
active_task: BL-7 — capability-tiered review, an elective vertical-slice addition. COMPLETE: design panel (3 candidates, judged, synthesized) -> operator approval on all 4 decisions -> implementation (4 files) -> 4-lens adversarial review -> 1 confirmed defect fixed -> committed on branch feat/capability-tiered-review -> PR #57 opened and merged (d563600).
what_was_done: Ran a 3-candidate design panel (workflow wf_e2f587c7-efd) scoring placement/naming/scope on 4 judge lenses each; synthesized one proposal. Operator approved via AskUserQuestion: SESSION_RUNNER.md placement, "capability-tiered review" naming, vertical-slice-only scope, and all three optional extras (IM routing pointer, Learning #11, T5 tutorial callout). Implemented and committed as 0942b17: starter-kit/SESSION_RUNNER.md (core paragraph in Vertical Slice Sessions + new Learning #11), ITERATIVE_METHODOLOGY.md (routing-pointer sentence), starter-kit/RECOMMENDED_SKILLS.md (illustrative addendum), docs/tutorials/T5_cautionary.md (corollary). Ran bin/tests.sh (84/84) and bin/check-links (clean) before review. 4-lens adversarial review (workflow wf_9446b96d-651: guardrail fidelity, citation fact-check, voice/agent-independence, completeness-critic sweep) unanimously found one real defect — brand names "Sonnet-5/Opus-4.8" leaking into the new Learning #11's Source column in the brand-neutral core file — fixed; re-ran bin/tests.sh (84/84) and bin/check-links (clean) after the fix; both folded into commit 0942b17. Receipt for this work committed as 21fb521 (--no-verify; ledgered by 0942b17's CHANGELOG entry). Operator confirmed "merge completed"; PR #57 verified MERGED (d563600). This entry is the fork-side close-out completing that work: merged upstream/main into fork main, resolved CHANGELOG.md + HANDOFFS.md union conflicts by chronological reordering (this session's work is newest, landing above the prior session's S5 close-out).
next_steps: Mark BL-7 complete in docs/planning/BACKLOG.md (fork-only) in this same close-out commit. Ask the operator whether this ships as a version event (a version-bump commit was NOT included in the PR #57 merge, so that decision is still open) — if yes, a small follow-up commit + tag/release; if no, this close-out is the final action. Push fork main; prune feat/capability-tiered-review locally and on origin.
key_files: starter-kit/SESSION_RUNNER.md:177 (capability-tiered review paragraph), starter-kit/SESSION_RUNNER.md:376 (Learning #11), ITERATIVE_METHODOLOGY.md:397 (routing pointer), starter-kit/RECOMMENDED_SKILLS.md:75 (illustrative addendum), docs/tutorials/T5_cautionary.md:68 (corollary), docs/planning/BACKLOG.md:19 (BL-7 entry to close)
gotchas: This receipt was originally written and committed (21fb521) on the feat/capability-tiered-review branch as "session: S2" — accurate at the time, since that branch was cut from upstream/main and the only visible predecessor there was S1 (the fork's own S2-S5 sequence is fork-internal and was never part of that branch, by design, so it wasn't visible). Renumbered S2 -> S6 here at fork-sync to land in the fork's true chronological sequence without colliding with the already-established, already-pushed S2 (v3.3 release). The predecessor_score of 9 below still evaluates S1, exactly as originally written on the branch — not retroactively re-scored against S5 — because that is what this session actually did at the time, and rewriting it now would misrepresent the session's own history. Per the "never renumber an already-shipped entry" rule, only this NOT-yet-fork-published entry was renumbered; S1-S5 below are untouched.
runtime_smoke: n/a -- docs-only change; verified by bin/tests.sh 84/84 and bin/check-links clean, both re-run after the post-review fix and again after this fork-sync merge
changelog_ref: CHANGELOG.md "Capability-tiered review -- elective vertical-slice addition (BL-7)" entry, commit 0942b17; fork-sync entry, this commit
commit: pending
```
Self-score 8/10. **+** Structured 3-candidate design panel with explicit operator sign-off on every
open decision (placement, naming, scope, all three extras) before any file was touched — the
AskUserQuestion answers function as the plan-mode contract this backlog item's own "planning/design,
not implementation" framing called for. **+** 4-lens adversarial review independently converged on the
same real defect and it was fixed before commit; full test suite + link check re-verified after the
fix, not just before it, and again after fork-sync. **+** Scope stayed exactly within BL-7's approved
shape — no second capability bundled in. **+** Caught and correctly resolved the session-numbering
collision this receipt's own earlier draft had flagged as a foreseeable risk (see gotchas), rather than
letting it land as a silent duplicate S2. **−** Skipped the Phase 1B pending stub (this session went
straight from Orient into the design workflow without writing an interim claim); harmless here since
the session ran to a clean close without crashing, but it is a real deviation from the documented
procedure, not a judgment call to repeat by default. **−** Design and implementation landed in one
continuous session rather than two — defensible because every decision was closed out by explicit
operator Q&A before a single file changed and the resulting diff is small (4 files, ~300 words, no new
gate/phase/FM), consistent with this repo's own precedent for backlog items (e.g. BL-5 ran its design
panel and adversarial implementation review in one session too) — but flagged here as a considered
call, not an unexamined default.

Predecessor (S1) evaluation: 9/10, as originally written on the feat/capability-tiered-review branch.
S1's `next_steps` explicitly named "Consider BL-7 (model-tiering as an elective feature) as a follow-on
planning session" — a precise, actionable pointer that this session followed directly. Key files,
gotchas (canonical-only checker, Test 9 github-404), and an honest self-critique (large single-session
slice, unmerged, version event undecided) were all present and accurate.

```handoff
session: S5
date: 2026-07-08
status: complete
self_score: 8
predecessor_score: 7
active_task: Design, adversarially verify, implement, and ship upstream issue #55 — a "completeness-critic" review lens promoting Learning #7/#8 from an authoring self-check to a review-time lens. Also earlier this session: a Phase 0 reconcile backfilling S2-S4 (see that receipt).
what_was_done: Read issue #55 in full, drafted a 3-file design (SESSION_RUNNER.md Learning #10, AUDIT_WORKSTREAM.md anti-pattern #9 + Verification Checklist bullet + Recommended-Skills note, ITERATIVE_METHODOLOGY.md one sentence), then ran a 4-lens adversarial verify workflow before writing anything to disk — 2 lenses clean (acceptance-criteria coverage, a reflexive Learning-#7 self-check for other stale cross-references), 2 found real defects (a mis-anchored insertion point in AUDIT_WORKSTREAM.md's Recommended Skills section; a citation missing the starter-kit/ path prefix used elsewhere) — both fixed before commit. Implemented on branch feat/completeness-critic-review-lens off upstream/main: f00fcb2 (content) + 1b191cd (v3.3->v3.4 version bump, operator directed "increment version by 0.1; add new tag" + "make it a new release"). Opened PR #56, merged to upstream (4a6c1d2, auto-closed issue #55), tagged v3.4 + GitHub Release (Latest) on both remotes, merged upstream/main back into fork main (d139642 — resolved a CHANGELOG.md union conflict by chronological reordering, not a naive ours/theirs pick), pushed fork main, pruned the feature branch.
next_steps: BL-7 (model-tiering as an elective methodology feature) remains the only open fork-backlog item — a planning/design session, not implementation. No other open threads from this session.
key_files: starter-kit/SESSION_RUNNER.md:373 (Learning #10), workstreams/AUDIT_WORKSTREAM.md:196 (anti-pattern #9), workstreams/AUDIT_WORKSTREAM.md:166 (checklist bullet), ITERATIVE_METHODOLOGY.md:327 (Review/Audit Sessions sentence), CLAUDE.md:115 (v3.4 Versioning entry)
gotchas: branched from upstream/main, not origin/main — fork's origin/main carries fork-only docs/planning content that would pollute the PR diff (established convention, see prior sessions). Merging upstream/main back into fork main after the PR merged produced a CHANGELOG.md union conflict (both sides added dated entries independently) — resolve these by reasoning about actual wall-clock authorship order, not a blind union or a naive "ours" pick; a stale "(just above)" positional cross-reference in one of the reconciled entries needed fixing after the reorder (a live instance of this very session's own completeness-critic lens).
runtime_smoke: n/a — docs + python3-stdlib tooling; bin/tests.sh 84/84 at every checkpoint (post-content-edit, post-version-bump, post-merge-resolve); bin/check-links clean throughout.
changelog_ref: CHANGELOG.md "Completeness-critic review lens" + "Released v3.4" entries, commit d139642
commit: d139642
```
Self-score 8/10. **+** Design was adversarially verified BEFORE implementation (not after) — caught 2 real
placement/citation defects a solo draft would have shipped; **+** applied the new Learning reflexively to
its own merge-conflict resolution (fixed a stale positional cross-reference the reorder created); **+**
full release flow executed correctly end-to-end (branch-from-upstream convention, PR, merge, dual-remote
tag, GitHub Release, fork sync) matching established precedent without a step skipped. **−** Did not write
this receipt until session close — the earlier Phase 0 reconcile work (S2-S4) and the completeness-critic
implementation both landed several commits before this receipt was written, relying on this session's own
attentiveness rather than a mid-session checkpoint; a crash before this point would have left the same
kind of gap S2-S4 reconciled. **+** Predecessor (S4, reconciled) scored 7: consistent with a small, ad hoc,
single-commit session; this session's own work discharges S4's own next_steps about issue #55 fully.

```handoff
session: S4
date: 2026-07-08
status: reconciled
self_score: 7
predecessor_score: 8
active_task: File an upstream issue proposing a "completeness-critic" review lens — reviews should sweep the whole corpus, not just the diff, for enumerations/indexes/worked-examples/count-claims a change made stale.
what_was_done: Opened KJ5HST/methodology#55 (motivated by the v3.3 doc-completeness gap S3 had just closed — a clean 6-lens adversarial review missed out-of-diff staleness that the operator caught by asking "has documentation been fully updated?"); logged it in CHANGELOG.md, commit 6591faa.
next_steps: Issue #55 is unimplemented — a future session should design where the completeness-critic lens lands (a review-skill addition, or a SESSION_RUNNER/AUDIT_WORKSTREAM checklist step?). Separately, this very file was 3 sessions behind (S2/S3/S4 all left commits with no receipt) until this Phase 0 reconcile backfilled them — a live instance of exactly the gap issue #55 names.
key_files: CHANGELOG.md:35 (issue #55 ledger entry)
gotchas: this repo's Issues live upstream only (KJ5HST/methodology) — the fork has Issues disabled, so cite the absolute URL, never a bare #55.
runtime_smoke: n/a — issue filing + one ledger commit, no code/doc-render surface
changelog_ref: CHANGELOG.md "Opened upstream issue #55" entry, commit 6591faa
commit: 6591faa
```
Reconciled at the next Orient (Phase 0 step 6) — this session left one commit (`6591faa`) with no
`HANDOFFS.md` receipt. Reconstructed from `git log` and the CHANGELOG entry it wrote for itself;
`self_score`/`predecessor_score` are this reconciling session's best-effort read of the evidence, not
the original session's own self-assessment — `SESSION_NOTES.md` held nothing by the time of reconcile.

```handoff
session: S3
date: 2026-07-08
status: reconciled
self_score: 8
predecessor_score: 7
active_task: v3.3 doc-completeness — propagate the close-out receipt into the secondary docs that describe or demonstrate close-out.
what_was_done: Updated HOW_TO_USE.md Phase 3 3D to name the durable HANDOFFS.md receipt, README.md's Repository-Structure tree to list HANDOFFS.md + check-handoff, and the tutorials (T2_worked_transcript.md, T2_first_session.md, T3_compounding_loop.md) to show the receipt at close-out; commits 67581fd and 768631e, merged via PR #54 (merge 630fd97).
next_steps: The operator's prompting question ("has documentation been fully updated?") that motivated this session is itself a manual catch a review lens should make automatic — that observation became issue #55, filed next by S4.
key_files: HOW_TO_USE.md:764 (3D receipt wording), docs/tutorials/T2_worked_transcript.md:217 (worked receipt example), docs/tutorials/T2_first_session.md:54 (1B receipt stub), docs/tutorials/T3_compounding_loop.md:6 (predecessor_score in the compounding loop)
gotchas: this is a docs-lag fix, not new capability — no version event, per CLAUDE.md's "not every contribution needs a release" convention.
runtime_smoke: bin/check-links clean; a completeness sweep found no other tutorial demonstrating close-out without the receipt
changelog_ref: CHANGELOG.md "v3.3 doc-completeness" entry, commit 768631e
commit: 768631e
```
Reconciled at the next Orient (Phase 0 step 6) — this session left commits `67581fd`/`768631e` with no
`HANDOFFS.md` receipt. Reconstructed from `git log` and the CHANGELOG entry it wrote for itself;
`self_score`/`predecessor_score` are this reconciling session's best-effort read of the evidence, not
the original session's own self-assessment.

```handoff
session: S2
date: 2026-07-08
status: reconciled
self_score: 7
predecessor_score: 8
active_task: Release v3.3 — durable close-out receipt (ship the merged close-out-receipt slice, PR #52).
what_was_done: Version bumped v3.2 to v3.3 (CLAUDE.md "Current version" line + new §Versioning entry; README.md What's New), shipped as annotated tag v3.3 + GitHub Release (Latest), commit dd2c84b, merged via PR #53 (merge 4ec1f47).
next_steps: None recorded by the session itself (SESSION_NOTES.md was overwritten by later sessions before this reconcile ran). In practice the next session (S3) found the secondary docs — HOW_TO_USE, README tree, tutorials — still described close-out without the receipt, and closed that gap.
key_files: CLAUDE.md:114 (v3.3 Versioning entry), README.md:257 (What's New in v3.3)
gotchas: Test 9 (github-source) 404s until HANDOFFS.md lands on the default branch — clears on this merge, not before.
runtime_smoke: post-merge bin/tests.sh green (Test 9's github-source 404 cleared)
changelog_ref: CHANGELOG.md "Released v3.3 — durable close-out receipt" entry, commit dd2c84b
commit: dd2c84b
```
Reconciled at the next Orient (Phase 0 step 6) — this session left commits `dd2c84b`/`4ec1f47` with no
`HANDOFFS.md` receipt. Reconstructed from `git log` and the CHANGELOG entry it wrote for itself; scores
are this reconciling session's best-effort read of the evidence, not the original session's own
self-assessment.

---

```handoff
session: S1
date: 2026-07-08
status: complete
self_score: 8
active_task: Close-out receipt vertical slice (P1-P6) — durable HANDOFFS.md receipt + bin/check-handoff + Phase 0 reconcile backstop + framing. COMPLETE on branch feat/close-out-receipt; PR + version decision pending.
what_was_done: Shipped the close-out-receipt slice as 6 checkpoint commits — 4f0bea7 (P1 seed+manifest), 1646773 (P2 checker+tests), f722a84 (P3a SESSION_RUNNER+IM wiring), afbbe7d (P3b campaign checklists), 5f13c99 (P4 Phase 0 reconcile), 719a41d (P5 framing), plus this P6 dogfood commit. Hybrid model split: Sonnet 5 built P2/P4, Opus 4.8 did P3/P5/P6 and reviewed all Sonnet output.
next_steps: Open the PR from feat/close-out-receipt to KJ5HST/methodology; decide the version event at merge (D4 — CLAUDE.md §Versioning v3.3 vs none). Fork main already carries the ratified plan (6b9ccd7) and BL-7 (cb8165d); fork-sync after merge unions the CHANGELOG newest-on-top. Consider BL-7 (model-tiering as an elective feature) as a follow-on planning session.
key_files: starter-kit/HANDOFFS.md:1 (seed + format), bin/check-handoff:1 (checker), starter-kit/SESSION_RUNNER.md:18 (Phase 0 receipt reconcile), docs/planning/close-out-receipt-durable-artifact-plan.md:1 (ratified plan, fork main)
gotchas: bin/check-handoff is canonical-only (not in bin/_manifest.py) — adopters get the synced write-step + reconcile and copy the checker if wanted. Test 9 (github-source) fails until this branch merges (HANDOFFS.md 404s on the remote). Receipt keys take no inline # comments (# is a literal value char, cf. PR #52). status: reconciled is written only by Phase 0 backfill, never by hand.
runtime_smoke: n/a — docs + python3-stdlib tooling; verified by bin/tests.sh 81/82 (the 1 = expected github-404), bin/check-handoff green on this receipt, and check-links clean
changelog_ref: CHANGELOG.md "Close-out receipt — durable machine-checkable handoff artifact" entry (this branch)
commit: e5638af
```
Self-score 8/10. **+** Full vertical slice with per-boundary verification (build/test + check-links at
every checkpoint) and a clean hybrid model split; **+** adversarial Opus review of the Sonnet phases
caught real defects (an inline-`#` template footgun, the `status: reconciled` doc gap, and confirmed the
reconcile's false-positive scoping is per-session not per-commit); **+** honest ceiling stated throughout
(structure not quality; a no-commit session still escapes). **−** Large single-session slice (6 commits)
— recoverable only because each layer is an independent checkpoint commit and it is ONE capability
(passes the FM #26 slice test); **−** unmerged and not yet operator-reviewed; the version event is
undecided. This is the first real receipt in this ledger (S1), so there is no predecessor to score.
