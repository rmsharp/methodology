# Handoff Receipts — durable close-out proof

This repository dogfoods its own methodology: every session records a durable, machine-checkable
`handoff` receipt here at close-out (Phase 3D), and Phase 0 reconciles it against `git log`. See
[`starter-kit/HANDOFFS.md`](starter-kit/HANDOFFS.md) for the block format and the write points, and
`bin/check-handoff` for the checker. Newest on top; prepend-only.

---

```handoff
session: S15
date: 2026-07-25
status: pending
active_task: Layer 7 of docs/planning/dashboard-signal-integrity-plan.md (:305-364) — the ratified amendment that executes BEFORE Layer 6. The installer defeats doc-only detection: bin/sync installs methodology_dashboard.py (3,070 lines) to the adopter ROOT (bin/_manifest.py:43, TRACKED) while DOC_ONLY_SOURCE_LOC_MAX is 200, so detect_doc_only's source-cap short-circuit (:1678) fires before the corpus disjunction (:1686) is ever consulted — installing the methodology destroys the doc-only fair-scoring v3.2 exists to provide. Operator chose fix A of three (S14): stop counting framework-installed files toward the adopter's source LOC. B (raise the cap) and C (rely on the marker) are REJECTED ON THE RECORD at plan :337 — do not re-propose. The exclusion must not become a laundering hole: exclude only by the manifest's own installed name at the point of the source-LOC read, never a general "skip large Python files" rule, and a repo whose OWN source exceeds the cap must still read as `code`. RED-first proof is four fixtures (plan :351): (a) synced Quarto fixture -> doc_only=True; (b) synced real code repo -> still doc_only=False, and this one must be SEEN TO FAIL against a wrong fix such as B, not merely pass against A; (c) unsynced doc repo unchanged; (d) the HIGH "No test infrastructure" risk absent from (a), present in a genuine no-test code repo. DASHBOARD_VERSION -> 2.10.1; both byte-identical twins + tests. ONE LAYER ONLY — Layer 6 (close-out, release decision R1, the owed SESSION_RUNNER.md Learnings row, the D4 plan correction) is a separate session, and BL-8/BL-9 are sequenced after it.
```

```handoff
session: S14
date: 2026-07-25
status: complete
self_score: 7
predecessor_score: 9
active_task: Layer 5 of docs/planning/dashboard-signal-integrity-plan.md (:272-303) — the MANDATORY completeness-critic doc sweep (v3.4 Learning #10 / AUDIT_WORKSTREAM.md anti-pattern #9). Reconcile the prose corpus to what Layers 1-4 actually SHIPPED. THE PLAN'S OWN TABLE IS INCOMPLETE AND MUST NOT BE TRUSTED AS THE SCOPE: it was written at S9 and predates Layer 3's abstention and Layer 4's repo role, so its six rows cover only the HANDOFFS.md / compliance-% / 5-dimensions items. Re-derive the target list from the four shipped diffs (6b10f09, 3838a13, 9ebedda, abb3b29), not from the table. Known-stale before the sweep even starts: README.md:285 documents .methodology-profile as "doc-only | code" and it now has a SECOND axis (framework | adopter), and nothing in the corpus mentions the second checklist, the "Framework Integrity" dimension label, or the role-provenance line. THE FROZEN-PROSE RULE BINDS (v2.7.1): dated release prose in README §What's New and CLAUDE.md §Versioning entries is NOT edited, and the plan at :294 records two "corrections" it explicitly REJECTED because applying them would have INTRODUCED errors ("29 tests" is right; "51 -> 54" is a dated statement). NO SCANNER CODE CHANGES — this is a prose layer; DASHBOARD_VERSION stays 2.10.0. ONE LAYER ONLY: Layer 6 (close-out, release decision R1, the owed SESSION_RUNNER.md Learnings row, and the D4 plan correction) is a separate session.
what_was_done: Executed Layer 5 in two checkpoint commits (baa1dd1 core docs, fc65013 tutorials; split only by the 5-file cap, full verification at each boundary). NO scanner code: DASHBOARD_VERSION stays 2.10.0, twins byte-identical. THE PLAN'S TABLE WAS RE-DERIVED, NOT TRUSTED, AND ITS HEADLINE ROW WAS REFUTED: the row directing a fix at README's `.methodology-profile` line is wrong, because that line sits inside `### What's New in v3.2` — dated prose the v2.7.1 convention freezes and which the plan's OWN not-edited list names at :290 — and it correctly describes what v3.2 shipped. All three corpus mentions of the marker are inside that frozen section, so the real defect was that the marker had NO LIVE DOCUMENTATION ANYWHERE, which is the plan's residual risk #3 ("the marker is the escape hatch; document it"). Fixed by adding operative documentation of both axes to README §Methodology Dashboard and BOOTSTRAP Step 9 (distributed to adopters), leaving the v3.2 entry untouched. Applying the plan as written would have been the THIRD instance of the error class the plan itself records at :294. The plan listed 6 rows; the swept corpus yielded 20 sites across 7 files. The HANDOFFS.md enumeration gap the plan adopted at 2 sites is systemic at 11; the operator approved fixing all 11 rather than leaving 9 known-stale siblings. README's "0-100 across 5 weighted dimensions" was verify-don't-edit and is VERIFIED, not assumed: the pre-L1 scanner scores the tutorial fixture at health 62 with a methodology dimension of 22, and HEAD scores 60/20 — so the claim was false before the campaign and is true now. Not edited. T7 now teaches the L3 abstention because the campaign made it fire on the tutorials' own sample project, whose BACKLOG.md is a feature table with no Status column; the advisory is quoted byte-identical to the live risk string (asserted programmatically) and the causal claim was proved by COUNTERFACTUAL — adding a Status column to a rebuilt fixture makes the advisory disappear and restoring the file brings it back. ONE FALSE CLAIM IN MY OWN NEW PROSE WAS CAUGHT BEFORE COMMIT: the first draft of the marker documentation asserted "a marker override is never silent", and a fixture showed a structurally-framework repo declaring `adopter` renders NO provenance line at all — only framework-role cards carry it. Corrected in place. Every other marker claim was fixture-tested and held (contradiction on one axis falls back to structural with reason=marker-contradiction; token order is irrelevant; only the first non-comment line is read; unknown tokens ignored).
next_steps: **NEW AND HIGHEST-PRIORITY — A LIVE SCANNER DEFECT, found by Layer 5's late boundary review, awaiting an operator decision. It is NOT a Layer 5 item and NOT in the ratified plan: installing the methodology destroys the doc-only fair-scoring that v3.2 exists to provide.** bin/sync installs methodology_dashboard.py (3,070 lines) to the adopter ROOT (bin/_manifest.py:43, disposition TRACKED) while DOC_ONLY_SOURCE_LOC_MAX is 200 (tools/methodology_dashboard.py), so detect_doc_only's source-LOC cap short-circuits before the doc-corpus/render-toolchain disjunction is ever consulted. MEASURED on a Quarto-book fixture (6 .qmd chapters + _quarto.yml, git init): BEFORE bin/sync doc_only=True / testing dimension 4 / no test risk; AFTER bin/sync doc_only=False / source_loc=3070 / testing dimension 0 / HIGH "No test infrastructure" risk restored — the exact false penalty v3.2 shipped to remove, re-inflicted on every doc-only adopter that follows BOOTSTRAP. LIVE SINCE v3.2; predates this campaign. **DECIDED BY THE OPERATOR (S14) AND ALREADY WRITTEN INTO THE PLAN — execute it, do not re-open it: fix A (stop counting framework-installed files toward adopter source LOC), as the new LAYER 7, whose execution slot is BEFORE Layer 6.** The full contract — defect, measured before/after table, the two rejected alternatives with reasons, the one-name exclusion, the anti-laundering constraint, and a four-fixture RED-first proof — is at docs/planning/dashboard-signal-integrity-plan.md (search "Layer 7"). It was written in S14 while the measurements were first-hand, deliberately, because Layer 5's own table went stale by being written without them. DASHBOARD_VERSION -> 2.10.1; both twins + tests. NOTE THE NUMBERING: 7 is appended, never renumbering 1-6 (this repo's rule for numbered sets), so "Layer 7 runs before Layer 6" is correct and intentional, not a typo. Then execute Layer 6 (close-out + release decision R1) of docs/planning/dashboard-signal-integrity-plan.md — the LAST layer. It owes four things, not one: (1) settle deferred decision R1 (is this a tagged framework release? inputs at plan :317 — it changes scoring for every scanned repo and every synced adopter copy starts emitting check_stale_version warnings the moment canonical bumps); (2) a SESSION_RUNNER.md Learnings-table row, owed since S9 and explicitly deferred to Layer 6 by plan §8 (that file is DISTRIBUTED — the table is 1-11 today, append #12, do not renumber); (3) THE D4 PLAN CORRECTION — ratified decision D4 asserts this repo's own docs/planning/BACKLOG.md "lands in that branch and will correctly say so", which is FALSE at HEAD: the format reads `unrecognized` but the advisory is suppressed by Signal F's root-SESSION_RUNNER.md gate, and the operator decided in S13 NOT to widen that gate because Signal F's premise (an item is removed when logged) is verifiably false for this repo class; (4) close the campaign in CLAUDE.md §Versioning IF R1 says release. ALSO CARRY FORWARD, ALL RECORDED AND NONE ASSIGNED: the boundary review for THIS layer never ran (see gotchas) — re-run it as Layer 6's first act before anything else; the operator raised a COST concern that is measured and unanswered (this repo's per-session floor is now ~304 KB / ~76k tokens, of which CHANGELOG.md 93 KB + HANDOFFS.md 95 KB, and the per-session receipt is growing 10 -> 13 -> 13 -> 15 KB across S10-S13 — proposed fixes are ledger sharding per CHANGELOG.md's own "Promote to ## YYYY-MM sections as it grows" header, applying this repo's own CLAUDE.md size budget from BOOTSTRAP.md:195 to its 43 KB CLAUDE.md whose §Versioning is 86% of the file, and a receipt length target; none of it started); CLAUDE.md's starter-kit table still omits CLAUDE_TEMPLATE.md / CONTEXT_TEMPLATE.md / RECOMMENDED_SKILLS.md (older gap, outside approved scope); docs/images/*.png have shown pre-campaign renderings since v2.0 (9639ce6); the scanner's module docstring CUSTOMIZATION section documents METHODOLOGY_ITEMS but neither FRAMEWORK_ITEMS nor the marker, and fixing it is a code change to BOTH twins whose own rule says bump the version.
key_files: README.md:130 (the new "Adapts" bullet — the first live statement that two dimensions are context-dependent), README.md:136 (the new `.methodology-profile` two-axis table — the plan's residual risk #3 discharged; the sentence about provenance is deliberately scoped to framework verdicts because an adopter-role override renders NOTHING), starter-kit/BOOTSTRAP.md:267 (same two facts, DISTRIBUTED — an error here propagates to every adopter), docs/tutorials/T7_portfolio_dashboard.md:72 (the abstention lesson + the byte-exact advisory quote), docs/tutorials/T8_keeping_current.md:57 (the bin/status transcript row that was missing), docs/tutorials/T8_keeping_current.md:183 (21 -> 22, and the two counts are BOTH right for different questions), bin/_manifest.py:47 (HANDOFFS.md as SEED — the authority for 9 of the 11 enumeration fixes), tools/methodology_dashboard.py:1604 (the first-non-comment-line rule the new marker docs describe), docs/planning/dashboard-signal-integrity-plan.md:305 (Layer 6, next), docs/planning/dashboard-signal-integrity-plan.md:317 (deferred decision R1)
gotchas: (1) **THE BOUNDARY REVIEW RAN LATE, AFTER CLOSE-OUT, AND IT FOUND FOUR REAL DEFECTS — three in my own new prose (fixed in f16523e) and one LIVE SCANNER DEFECT still open.** The first attempt died: all four lenses hit a usage limit and the harness returned `{"findings":[],"notes":[]}`, which means NOTHING EXECUTED, not "nothing found" — reporting that as a clean review would have been the S13 "unapplied mutant reported as killed" error exactly. On the operator's instruction I re-ran the two lenses I had NOT already hand-checked (marker documentation, numbers) and hand-verified every finding before acting. THE LESSON, and it is the whole point of the layer: my marker documentation never said the declaration line is read as TOKENS, so an uncommented sentence placed first silently declares any axis word it contains — "We follow the framework conventions for this paper." grades a doc repo as framework/reason=marker and discards its `doc-only` on the next line. That is the SAME failure class S13's review caught in the CODE, reproduced by me in the PROSE THAT DOCUMENTS THAT VERY CODE, one layer later. My hand-run lenses (3 and 4) were both clean; the two I could not get to were the two carrying every defect — a coverage gap, not a quality result. DO NOT treat "I hand-checked the important ones" as equivalent to a review again. (2) A PARALLEL WORKFLOW IS NOT FREE AND CAN EXHAUST THE SESSION: the Layer 5 sweep spent ~3.05M subagent tokens over 40 agents / 796 tool calls, and the review that followed hit the ceiling. Budget the review BEFORE the sweep, or run the sweep with fewer verifiers — a layer that ships unreviewed because the discovery pass ate the budget is a bad trade. (3) MY OWN VERIFICATION SCRIPT WAS WRONG ONCE: the smoke test's `1[0-9][0-9]%` regex matches "100%" and reported a nonexistent violation. A check that can fire on correct output is not a check — extract values and compare numerically. (4) THE PLAN CAN BE WRONG ABOUT ITS OWN FROZEN LIST: Layer 5's table directed an edit at README.md:285, which the SAME plan freezes at :290. Read the not-edited list before applying any row, and confirm each target's enclosing heading with awk rather than trusting a line number. (5) Line numbers in a doc corpus MOVE as you edit it — every plan row cited a pre-edit line; re-grep before each edit, never batch by line number. (6) Two counts that are both correct and look contradictory: bin/check-links says 21 (markdown only), bin/status says 22 (all manifest entries, incl. methodology_dashboard.py). Do not "fix" either. (7) Still-unrepaired record defect, found at Phase 0 and never assigned: HANDOFFS.md carries a leftover stub `status: pending` above S12's `status: complete` — a duplicate key bin/check-handoff cannot see because it validates only the NEWEST block, and which false-positives the portable `grep 'status: pending'` stop-hook SAFEGUARDS.md recommends. Also an untracked empty scratch_test/ at root.
runtime_smoke: Ran the real render path against live collected metrics (collect_all -> render_project_card -> render_methodology_grid -> aggregate_portfolio -> render_html), writing nothing into any scanned repo and generating no dashboard.html. 23,451 chars; distinct percentages rendered are exactly {0, 80, 100} — none over 100. MY FIRST BOUND CHECK WAS ITSELF WRONG and I caught it: the regex `1[0-9][0-9]%` matches "100%", so it reported a violation that did not exist; re-done by extracting every percentage and comparing numerically. This repo still reads role=framework, "Framework Integrity (100% (105 of 105))", health 72, with the presence-check disclosure and the structural provenance line. Prose-claim verification beyond the suites, all by execution: a rebuilt post-T1 fixture (sample-project + git init + bin/sync) reproduces the T7 advisory byte-identically and loses it when a Status column is added; an ordinary code+docs adopter fixture is doc_only=False/role=adopter and renders the plain five labels plus "Methodology Compliance", so BOOTSTRAP's "most projects see the plain five" holds; bin/status emits exactly 22 rows against that fixture (the 21 in bin/check-links is the MARKDOWN subset — both numbers are right for different questions); HANDOFFS.md is genuinely a member of BOTH the SEED set and METHODOLOGY_ITEMS, so the two kinds of list I edited are not conflated; test_methodology_dashboard.py is absent from the manifest, so "canonical-only" is accurate. Suites at both boundaries: bin/tests.sh 84 passed / 0 failed; tools/test_methodology_dashboard.py 168 OK; python3 bin/check-links OK (82 links / 21 files); diff -q twins identical; both declare DASHBOARD_VERSION 2.10.0 (unchanged by design).
changelog_ref: CHANGELOG.md entry "Dashboard signal-integrity Layer 5 — completeness-critic doc sweep (no version bump)", commits baa1dd1 + fc65013
commit: fc65013
```
Self-score **7/10 — revised down from 8 after the deferred boundary review ran and found three
defects in my own new prose.** The revision is the honest one: I closed out claiming the layer was
sound on the strength of two lenses I had hand-run myself, and the two lenses I could not get to
were the two that carried every defect. **+** Refused the ratified plan's headline row on evidence rather than executing it:
the marker line it told me to fix is frozen by the plan's own not-edited list six lines further down,
and applying it would have been the third instance of the error class the plan itself documents.
Finding the *real* gap behind it — the marker had no live documentation anywhere, which is the plan's
own residual risk #3 — came from grepping the corpus, not from reading the row. **+** Re-derived the
target list instead of trusting the table, which is what my predecessor told me to do: 6 planned rows
→ 20 real sites, and the `HANDOFFS.md` gap the plan adopted at 2 sites was systemic at 11. **+** Took
the three genuine scope questions to the operator before editing anything, with the evidence for each,
rather than deciding them myself. **+** Verified the verify-don't-edit row by *executing the
pre-campaign scanner* (health 62, dimension 22) instead of asserting that Layer 1 had fixed it.
**+** Proved T7's causal claim by counterfactual — added a `Status` column to a rebuilt fixture, watched
the advisory vanish, restored it — rather than reasoning from the predicate. **+** Caught a false claim
in my own new prose before it was committed, by fixture rather than by re-reading it.
**−** I shipped the deliverable before the review ran, and the review then found **three defects in
my own new prose** — including one that reproduces, in the documentation, the exact failure class
S13's review had just caught in the code it documents (an uncommented sentence read as a
declaration). I recorded the missing review rather than letting an empty `findings: []` pass for a
clean bill, and that recording is what let the operator call for the re-run — but the correct move
was to budget the review *before* spending ~3M subagent tokens on discovery, not to close out and
hope. **−** I also treated "I hand-checked the two highest-value lenses" as near-equivalent to a
review. It was not: my two hand-run lenses were clean and the two I skipped held every defect. **−** My own smoke-test regex (`1[0-9][0-9]%`)
matched `100%` and reported a violation that did not exist; a check that fires on correct output is not
a check, and I wrote it in a session whose entire subject is signals that don't mean what they appear
to mean. **−** I answered the operator's cost question with real measurements but left the resulting
work unstarted and unscheduled, so a 93 KB ledger and a 95 KB receipt file keep growing meanwhile —
and this receipt is itself part of that trend. **−** `CLAUDE.md`'s starter-kit table is left knowingly
incomplete (three other files) because the approved scope named only the `HANDOFFS.md` class; defensible,
but a reader of that table is still misinformed today.

Predecessor (S13) evaluation: 9/10. Its handoff was the most operationally load-bearing of the campaign.
The single most valuable line was its instruction to **re-derive Layer 5's table from the shipped diffs
rather than trust the plan** — the plan's table was not merely incomplete but actively wrong in its
headline row, and a session that executed it faithfully would have edited frozen release prose. Its
warning that "six of eight confirmed findings were false claims in my own prose" is why I fixture-tested
my own marker documentation and found the "never silent" error before committing it. Its gotcha that the
scanner cannot scan its own repo in place, with the exact `importlib` + `collect_all` recipe, worked
first try and saved the whole verification approach. Its `--no-verify` note explained the receipt-commit
bypass before I hit it. Every `file:line` in its `key_files` resolved to the code it named. One
deduction, and it is real: its `next_steps` and the memory both asserted that `README.md:285` "is stale
TODAY" and needed fixing, stated flatly and without the qualifier that the line sits inside a frozen
`§What's New` section — the very convention the same handoff was careful about elsewhere. I checked the
enclosing heading and refuted it, but a session that trusted a confident predecessor would have shipped
the error the plan explicitly warns about two paragraphs above.

---

```handoff
session: S13
date: 2026-07-25
status: complete
self_score: 8
predecessor_score: 9
active_task: Layer 4 of docs/planning/dashboard-signal-integrity-plan.md — repo role (defect 3 / upstream issue #59). Add detect_repo_role following the BL-5 precedent: bidirectional .methodology-profile marker (new `framework` token, read with encoding="utf-8-sig") then the structural heuristic (bin/_manifest.py AND starter-kit/SESSION_RUNNER.md both present); score a SEPARATE FRAMEWORK_ITEMS checklist when role == framework; suppress/reframe the adoption risk. DASHBOARD_VERSION -> 2.10.0. THE OBVIOUS FIX IS WRONG AND THE PLAN SAYS SO AT :255 — do NOT remap METHODOLOGY_ITEMS onto starter-kit/ paths (starter-kit/SESSION_NOTES.md is a 27-line empty stub; starter-kit/BACKLOG.md does not exist), which would credit 20 points for a placeholder and INVERT defect 3. Detection and wiring land in the SAME layer (plan :261). Both marker readers must scan the full token set, not tokens[0], so `doc-only` and `framework` compose. ONE LAYER ONLY — Layers 5 (mandatory doc sweep) and 6 (close-out + release decision R1) are separate sessions.
what_was_done: Implemented Layer 4 of the plan ratified in bc2481d. New detect_repo_role (marker override -> a THREE-way structural AND: bin/_manifest.py AND starter-kit/SESSION_RUNNER.md AND no root SESSION_RUNNER.md) plus a separate FRAMEWORK_ITEMS checklist (sum 105, derived per D1) scored, risk-reframed and rendered under its own name. The third conjunct is mine, not the plan's: it mechanizes the plan's own §7.3 description of the one misfire shape ("ships starter-kit/ templates plus distribution machinery WITHOUT installing to its own root"), so a monorepo that vendors this framework and also runs it keeps its adoption grading — it can only remove false positives. THE DESIGN CHOICE THAT MATTERS: the two files that PROVE the role are deliberately UNSCORED. If the evidence for the role also earned points, the raw sum would have a nonzero floor on the structural path and the "no corpus at all" HIGH branch would become a correct assertion over an input that can never occur — defect 6's exact failure class, re-created inside the campaign that closed it. THE MARKER FORCED A REWRITE OF SHIPPED BL-5 CODE, which the plan did not anticipate: reading tokens[0] made the plan's own Layer 4 proof ("a doc-only framework marker satisfies both axes") UNSATISFIABLE — measured against HEAD, "doc-only framework" was honoured but "framework doc-only" silently discarded the owner's declaration, a leading comment discarded it too, and "doc-only code" vs "code doc-only" resolved a contradiction by WORD ORDER. And the plan's instruction, taken literally, was a TRAP: the only .methodology-profile in the live population is 8 lines / 87 tokens whose "#" prose mentions the opposite token twice, surviving a token-bag read only on trailing punctuation ("code," / "code."), so full-token scanning WITHOUT comment stripping is strictly more dangerous than tokens[0]. I also fixed a regression this layer would otherwise have inflicted on the campaign itself: the Component-C ledger risk was gated on items.get("SESSION_RUNNER.md"), a key FRAMEWORK_ITEMS does not have, so it would have gone unreachable for every framework repo silently, with no test failing — now an explicit owes_ledger predicate. RED-first with FIVE BEHAVIOURAL failures against unpatched code (not AttributeError). Mutation-tested with BOTH twins patched: 34 mutants, 31 killed / 3 survived — one inert (a redundant comment-stripping branch, removed rather than tested so no later reader mistakes which line does the work) and TWO REAL HOLES (no test used a TRAILING "#" comment; the Health-Breakdown label could revert with the suite green). Then a 5-lens boundary review over a FROZEN tree with one skeptical refuter per finding: 28 raw -> 8 confirmed, all fixed. THE HIGH FINDING WAS A DEFECT I WOULD HAVE SHIPPED, AND IT INVERTED THE DEFECT BEING FIXED: my first reader mined EVERY line for declaration tokens, so an owner's own uncommented sentence became an override — "We keep our docs in the framework style" graded a plain adopter as the PUBLISHER with reason=marker and nothing disclosed, and "This is a code repository with helper scripts" under a doc-only declaration fabricated a contradiction and destroyed the override. Six of the eight confirmed findings were FALSE CLAIMS IN MY OWN PROSE, including a comment and legend asserting the two checklists "share no keys" when they share CHANGELOG.md and HANDOFFS.md. Tests 116 -> 168; final mutation set 38/38 killed.
next_steps: Execute Layer 5 (completeness-critic doc sweep — MANDATORY, plan :272-303) of docs/planning/dashboard-signal-integrity-plan.md. IT NEEDS MORE ROWS THAN THE PLAN'S TABLE LISTS, because the table predates what Layers 3 and 4 actually shipped: (a) README.md:285 documents the marker as ".methodology-profile (doc-only | code)" and it now has a SECOND axis (framework | adopter) — that line is stale TODAY; (b) nothing in the corpus mentions a second checklist, the Framework Integrity dimension label, or the role provenance line; (c) the plan's own Layer 5 table still lists only the HANDOFFS.md / compliance-% / 5-dimensions rows. Re-derive the table from the shipped diffs rather than trusting it. Then Layer 6 (close-out + release decision R1), which also owes: a SESSION_RUNNER.md Learnings row (plan §8 says one is owed once the campaign ships), and a PLAN CORRECTION — ratified decision D4 asserts this repo's own docs/planning/BACKLOG.md "lands in that branch and will correctly say so", which is FALSE at HEAD (format reads "unrecognized" but the advisory is suppressed by Signal F's root-SESSION_RUNNER.md gate). The operator decided NOT to widen that gate in Layer 4: Signal F's premise (an item is REMOVED from BACKLOG.md when logged to CHANGELOG) is verifiably false for this repo class, whose retired backlog deliberately keeps all seven BL-1..BL-7 rows, so widening the counting branch would manufacture a false "not migrated" accusation the moment that table gains a Status column.
key_files: tools/methodology_dashboard.py:159 (FRAMEWORK_ITEMS + the two "not scored, and why" rules), tools/methodology_dashboard.py:176 (FRAMEWORK_MAX — derived, and deliberately not 100 so value-sweep tests cannot go inert), tools/methodology_dashboard.py:245 (PROFILE_MARKER + the two disjoint axis token pairs), tools/methodology_dashboard.py:1568 (_profile_tokens — FIRST declaration line only; the review finding is written into the comment), tools/methodology_dashboard.py:1611 (_resolve_marker_axis — per-axis contradiction abstention), tools/methodology_dashboard.py:1631 (detect_repo_role), tools/methodology_dashboard.py:1828 (the framework risk branch — replaces, never merely suppresses), tools/methodology_dashboard.py:1908 (owes_ledger — the unreachable-signal fix), tools/methodology_dashboard.py:2118 (the grid's neutral framework cell + legend), tools/methodology_dashboard.py:2223 (card heading/denominator/provenance/presence-check note), tools/test_methodology_dashboard.py:1562 (test_only_the_first_declaration_line_is_read — the review's HIGH finding, locked), tools/test_methodology_dashboard.py:1686 (the operator-ratified no-SEED-source guard), docs/planning/dashboard-signal-integrity-plan.md:272 (Layer 5, next — and incomplete as written)
gotchas: (1) DEFECT 3 WAS REPRODUCED AT HEAD BEFORE ANY EDIT (compliance 10/115 = 9%, methodology 1/20, health 49/100, false medium risk) — do the same before Layer 5 rather than trusting this receipt. (2) REACHABILITY MATTERS HERE AND IS EASY TO OVERSTATE: EXCLUDE_DIRS contains the literal string "methodology" (:74), so discover_projects returns 9 siblings NOT including this repo. The false risk is reached via SINGLE-PROJECT mode (a dashboard copy at the repo root — exactly how BOOTSTRAP tells an operator to run it) or a fork under another directory name. DO NOT write a release note claiming the portfolio dashboard stops mis-scoring the framework repo. (3) THE HEALTH MOVE IS NOT ALL THE FIX: this repo goes 49 -> 72, but only +19 is Layer 4; +4 is the TESTING dimension rising because this session added ~430 lines of tests and crossed the 0.3 test:source rung. Attribute it honestly in any release prose. (4) A MUTATION HARNESS MUST PATCH BOTH TWINS or test_twins_byte_identical fakes every kill; run with a raised timeout (a timed-out harness leaves a LIVE MUTANT in the tree, and its .mutbak is the recovery path); DELETE the .mutbak files afterwards — they land in the repo root of tools/ and starter-kit/ and are untracked. (5) A PATTERN THAT NO LONGER MATCHES REPORTS AS "unapplied", NOT as killed — my final run had one, and reporting 37/37 would have been a false all-killed; apply it by hand before believing the number. (6) The dashboard still cannot scan its own repo in place (ROOT = Path(__file__).parent resolves to tools/). Load via importlib and call collect_all(Path(target)); never main(). render_html takes (portfolio, projects) built with aggregate_portfolio(projects). (7) A receipt-only or claim-only commit needs --no-verify; backstopped by Phase 0 reconcile. (8) bin/check-handoff STILL cannot validate a 1B stub even with --allow-pending (self_score/predecessor_score are required and unknowable at claim time) — do not "fix" it by inventing scores. (9) Freeze the tree before the boundary review, and tell reviewers it is frozen — mine reported zero stale line numbers.
runtime_smoke: Ran the REAL render path against live collected metrics (collect_all -> render_project_card -> render_methodology_grid -> aggregate_portfolio -> render_html), writing nothing into any scanned repo; 126,411 chars over 10 projects. Framework card reads "Framework Integrity (100% (105 of 105))", carries the presence-check disclosure, the role provenance line ("structural: ... no root SESSION_RUNNER.md"), names bin/sync, and contains neither "Methodology Compliance" nor "SESSION_NOTES.md". Grid row is one colspan=9 neutral cell + a daggered 100%, with the legend naming the two shared items. Adopter card (mts-system) still reads "Methodology Compliance (100% (115 of 115))" with the dim label "Methodology" and gains only the disclosure. BEFORE/AFTER SNAPSHOT OF ALL 10 LIVE SIBLINGS: exactly ONE repo's scoring moves and it is the target (methodology: compliance 10 -> 105, 9% -> 100%, methodology dimension 1 -> 20, false adoption risk gone). Every other repo is byte-identical except wsfct's branch count 261 -> 262, which is live git drift — verified my diff touches no branch-counting code. A genuine non-adopter is NOT laundered: claims-model-starter.wiki stays 5/115 = 4%, 0/20. church_growth (the only live marker) still classifies doc_only via marker, role adopter/default. Not a whitewash: this repo still reports "No CI/CD pipeline" and "Large files detected". Suites: tools/test_methodology_dashboard.py 116 -> 168 OK; bin/tests.sh 84 passed / 0 failed; python3 bin/check-links OK (82 links / 21 files); diff -q twins identical; both declare DASHBOARD_VERSION 2.10.0; py_compile clean.
changelog_ref: CHANGELOG.md entry "Dashboard signal-integrity Layer 4 — repo role", commit abb3b29
commit: abb3b29
```
Self-score 8/10. **+** Claimed at Phase 1B *before* any technical work, unlike S12, and captured a
green baseline plus a first-hand reproduction of the defect before editing a line. **+** Refused the
plan's own instruction where real data contradicted it: "scan the full token set" would have been
strictly *more* dangerous than the `tokens[0]` read it replaces, and I found that by looking at the
only marker file that actually exists in the wild rather than by reasoning about the rule. **+**
Caught the campaign-shaped regression *inside my own change* — the ledger risk would have gone
silently unreachable for every framework repo under a checklist that lacks its gating key — and
proved it by driving HEAD's `assess_risks` rather than arguing it. **+** Kept the two detection
inputs unscored so the `raw == 0` branch stays reachable, which is the same defect class this
campaign exists to close, applied reflexively. **+** Decomposed the health move instead of banking
it: of 49 → 72, only +19 is the fix and +4 is my own test code crossing a ratio rung, and the ledger
says so. **+** Took the three genuinely open decisions to the operator rather than settling a
ratified prohibition myself.
**−** The boundary review found a HIGH defect I would otherwise have shipped, and it **inverted the
defect I was fixing**: my reader mined every line of the marker for declarations, so an owner's own
uncommented sentence could grade a plain adopter as the publisher, or destroy a `doc-only`
declaration outright. `tokens[0]` never had that failure. I introduced a regression while fixing a
regression, and a reviewer caught it, not me. **−** Six of the eight confirmed findings were **false
claims in my own prose** — the grid comment, its test docstring and the user-facing legend all
asserted the two checklists "share no keys" when they share `CHANGELOG.md` and `HANDOFFS.md`; I had
measured that counterfactual on a two-key toy dict and never re-ran it against the real checklist.
In a layer about signals that do not mean what they appear to mean, that is the least excusable
class of error available, and it is the *second* consecutive session to make it. **−** I reported
"8 red crosses" to the operator mid-session from that same unverified toy measurement. **−** My
mutation set had no mutant for the `role_reason` wire at all, so an end-to-end path that prints a
*false provenance claim* on the card was unpinned until review found it; I mutated the code I had
thought hardest about and left the plumbing alone.

Predecessor (S12) evaluation: 9/10. Its handoff was the most operationally useful of the campaign so
far, and three of its gotchas paid out directly in this session rather than merely reading well. The
warning that **a mutation harness must patch both twins** was load-bearing twice: I built the
harness that way from the start, and my first run's 3 survivors were real information instead of a
false 28/28. The **raised-timeout** warning and the `.mutbak` recovery note meant I ran two full
rounds without ever leaving a live mutant in the tree. Its **weak-RED** distinction — that a rename
produces `AttributeError`, which proves absence rather than wrongness — is why I drove five
behavioural reds against unpatched code instead of shipping 38 errors and calling it red-first. Its
`bin/check-handoff` note again saved me from inventing scores at claim time. Every line number in
its `key_files` resolved to the code it named. Its generalized lesson — *ask what a fix makes the
dashboard SAY, not just what number it produces* — is exactly the lens that made me check the grid
rendering rather than the grid arithmetic, which is where the real defect was. One deduction, and it
is small: it recorded the plan's Layer 4 trap (the `starter-kit/` remap) faithfully but did not flag
that the plan's marker instruction was itself unsafe, and it had the evidence to — it had just
finished working with `_strip_fenced_blocks`, the same class of "content that looks like markup".
That is a high bar, which is why the score is 9 and not lower.

```handoff
session: S12
date: 2026-07-25
status: pending
active_task: Layer 3 of docs/planning/dashboard-signal-integrity-plan.md — backlog shape with abstention (defect 4 + the fenced-code-block false positive). _scan_backlog_done returns {format, done, recognized, source}; strip fenced code blocks BEFORE scanning; keep the checkbox predicate byte-unchanged in behaviour; add the table predicate (a cell that STARTS WITH a done token, in a row of >=3 cells, ignoring the ID column) WITHOUT re-deriving it — the plan tuned it empirically against the real 643-line backlog; abstain visibly on an unrecognized format per decision D4. DASHBOARD_VERSION -> 2.9.2. ONE LAYER ONLY — Layers 4-6 are separate sessions, and release decision R1 is settled at merge, not by an implementing session.
status: complete
self_score: 8
predecessor_score: 9
what_was_done: Implemented Layer 3 of the plan ratified in bc2481d. _count_backlog_done -> _scan_backlog_done returning {format, done, recognized, source} across six formats in decision order (unreadable, checkbox, table, unrecognized, none, absent); fenced code blocks stripped before scanning; the checkbox predicate's regex left byte-unchanged; the plan's tuned table predicate added WITHOUT re-derivation. The plan records its three tuning counts but not the token list, so I recovered the 8-token set by search and it reproduces all three simultaneously (contains 321, equals 227, predicate 256 vs hand count 253) — corroboration, NOT uniqueness, and the comment says so rather than overclaiming. THE DESIGN DECISION THAT MATTERS: I made the abstention NARROW. An empty backlog reports a silent, correct 0 (format "none") instead of abstaining, because airqino and model_project_constructor keep exactly that file and telling an up-to-date adopter its "format was not recognized" would be a signal that does not mean what it appears to mean — this campaign's own root defect re-created inside its fix. Abstention fires only on item-bearing content whose convention cannot be read. RED-first per the standing rule, and I drove the behavioural REDs against the OLD FUNCTION rather than resting on the AttributeError a rename produces (that is a weak RED: it proves absence, not wrongness). MY FIRST MUTATION RUN WAS INVALID AND I CAUGHT IT: the harness patched only tools/, so test_twins_byte_identical killed every mutant regardless of behaviour and reported a false 28/28 — any mutant whose kill cited exactly ONE assertion was a false kill. Re-run with both twins patched it exposed 8 real holes, INCLUDING ONE IN A TEST I HAD JUST WRITTEN TO CLOSE A HOLE (test_every_shipped_done_token_is_counted built its fixture by iterating the constant under test, so it passed no matter which tokens were deleted). Then a 5-lens adversarial boundary review against a FROZEN tree with one skeptical verifier per finding: 23 raw -> 15 confirmed, all 15 fixed. Two were REGRESSIONS in this layer's own new code — an unterminated fence swallowed the file (one stray ``` turned a backlog full of unmigrated work into "healthy empty", and with a Status table above it into a TRUSTED zero), and a GFM-escaped pipe fabricated a done-mark on an open row. Also fixed a header row being scanned as data. Quantified the predicate's known false-positive mode instead of asserting it away: of the 256, 242 come via a Status column and 14 from tables with no Status column, NONE only via another column — so narrowing to the Status column would move the ratified count to 242 and is an operator decision, pinned by characterization test.
next_steps: Execute Layer 4 (repo role, defect 3 / upstream issue #59) of docs/planning/dashboard-signal-integrity-plan.md — detect_repo_role following the BL-5 precedent (marker override `.methodology-profile` with a new `framework` token read with encoding="utf-8-sig", then the structural heuristic: bin/_manifest.py AND starter-kit/SESSION_RUNNER.md both present), score a SEPARATE FRAMEWORK_ITEMS checklist when role == framework, suppress/reframe the adoption risk. DASHBOARD_VERSION -> 2.10.0. THE OBVIOUS FIX IS WRONG AND THE PLAN SAYS SO AT :255 — do NOT remap METHODOLOGY_ITEMS onto starter-kit/ paths: starter-kit/SESSION_NOTES.md is a 27-line empty stub and starter-kit/BACKLOG.md does not exist, so the remap credits 20 points for a placeholder and inverts defect 3. Detection and wiring MUST land in the same layer (plan :261). Both marker readers must scan the full token set, not tokens[0], so `doc-only` and `framework` compose. RED-first AND mutation-test from a green baseline with BOTH twins patched. Then Layers 5 (doc sweep — mandatory, and Layer 3 added nothing to its table: I grepped the corpus and every hit is frozen historical prose) and 6 (close-out + release decision R1).
key_files: tools/methodology_dashboard.py:151 (_BACKLOG_DONE_TOKENS — the tuned set + the honest corroboration-not-uniqueness note), tools/methodology_dashboard.py:740 (_strip_fenced_blocks — only CLOSED fences are stripped; deliberately not renderer behaviour), tools/methodology_dashboard.py:772 (_split_row — splits on UNESCAPED pipes only), tools/methodology_dashboard.py:786 (_header_line_indices), tools/methodology_dashboard.py:806 (_table_data_rows — skips header rows), tools/methodology_dashboard.py:836 (_count_table_done + the measured known-limitation note), tools/methodology_dashboard.py:855 (_scan_backlog_done — the six formats), tools/methodology_dashboard.py:944 (the advisory + abstention branch, adopter-gated), tools/test_methodology_dashboard.py:963 (TestBacklogFormatAndAbstention), tools/test_methodology_dashboard.py:1043 (mutation-driven coverage + the two documented inert survivors), tools/test_methodology_dashboard.py:1120 (review-driven coverage), docs/planning/dashboard-signal-integrity-plan.md:244 (Layer 4, next)
gotchas: (1) PROCESS DEVIATION, recorded rather than backdated — the Phase 1B stub was written AFTER the technical work began. Everything up to the boundary review ran unclaimed. (2) A MUTATION HARNESS THAT PATCHES ONLY tools/ IS WORTHLESS HERE: test_twins_byte_identical kills every mutant and reports a false all-killed. Patch BOTH twins (or drop the twin test from your copy). Tell-tale: a "kill" citing exactly ONE assertion. (3) A TIMED-OUT MUTATION HARNESS LEAVES A LIVE MUTANT IN BOTH TWINS. Mine was killed by the 2-minute Bash timeout mid-round-3 and left `stripped[:2]` in the working tree; bin/tests.sh then read 83/84 — the plan's §3 warning that an isolated 83/84 is "unexplained" had a concrete cause. The harness's own .mutbak file is the recovery path; check for one before diagnosing anything. A test I had written minutes earlier is what caught it. (4) The real 643-line fixture is NOT in this repo and must not be vendored into it — recover it from mts-system commit 383c1715:BACKLOG.md. The plan's RED-first proof (c) asks for it as a test; I verified 256 as runtime smoke instead and encoded each property it depends on as a named test, rather than committing 51 KB of an adopter's data. (5) The dashboard still cannot scan its own repo in place (ROOT = Path(__file__).parent resolves to tools/). Load it via importlib and call collect_all(Path(target)); never call main() against a real repo. render_html takes (portfolio, projects) — build portfolio with aggregate_portfolio(projects) first. (6) A receipt-only or claim-only commit needs --no-verify; backstopped by Phase 0 reconcile. (7) bin/check-handoff STILL cannot validate a 1B stub even with --allow-pending (self_score/predecessor_score are required and unknowable at claim time) — do not "fix" it by inventing scores. (8) Freeze the tree before a boundary review; I did, and it meant zero stale-line-number churn, unlike S11.
runtime_smoke: Ran the REAL render path against live collected metrics (collect_all -> render_project_card -> render_methodology_grid -> aggregate_portfolio -> render_html -> append_history), writing nothing into any scanned repo (verified by mtime: the only dashboard.html files under Development/ are 70-1030 hours old). The real 643-line mts-system backlog scans as format "table", done 256 — the plan's tuned number, re-verified against the clean tree after every change, and still 256 with a stray unterminated fence prepended. Five real sibling repos: NO new risk fires anywhere and NO health score moves. church_growth keeps its advisory, now "BACKLOG.md: 15 done-marked item(s) not migrated to CHANGELOG (checkbox format)"; mts-system and wsfct are newly readable as table backlogs and correctly report 0 (mts-system mentions a done token on 12 lines, none of them a done row — the false-positive class rejected on live data); airqino and model_project_constructor stay silent as format "none". Rendered HTML 68,578 chars; history entries carry dashboard_version 2.9.2. Suites: tools/test_methodology_dashboard.py 79 -> 116 OK; bin/tests.sh 84 passed / 0 failed; python3 bin/check-links OK (82 links / 21 files); diff -q twins identical; both declare DASHBOARD_VERSION 2.9.2; py_compile clean.
changelog_ref: CHANGELOG.md entry "Dashboard signal-integrity Layer 3 — backlog shape with abstention", commit 9ebedda
commit: 9ebedda
```
Self-score 8/10. **+** Caught that my own mutation run was invalid before trusting it — the twin
byte-compare was killing every mutant, and a "kill" citing exactly one assertion was the tell. The
corrected run found 8 real holes, so the false 28/28 would have shipped a suite that could not tell
this code from broken code. **+** Drove the behavioural REDs against the *old function* instead of
accepting the `AttributeError` a rename produces; that distinction is the difference between
proving a defect and proving a spelling. **+** Made the abstention narrow on evidence — I checked
what the five live adopters actually keep before choosing the boundary, so the disclosure fires on
zero of them. A wider rule would have been defensible from the plan's text and wrong in practice.
**+** Quantified the predicate's false-positive mode (242 via Status / 14 no-Status / **0** via
another column) rather than either dismissing the reviewers or re-deriving a predicate the plan
forbids me to touch, and left the residual as an operator decision pinned by test. **+** Froze the
tree before the boundary review, so unlike S11 no reviewer reasoned about a moving target.
**−** I shipped two regressions in my own new code and a reviewer found both, not me: the
unterminated-fence swallow and the escaped-pipe split. The fence one is the worse failure — I wrote
a docstring *defending* the swallow as "conservative, it can only ever under-count" while it was
silently converting a backlog full of unmigrated work into the affirmatively healthy state. I
reasoned about the count and never about the classification, in a layer whose entire subject is
that a count means nothing without the convention it was read under. **−** I wrote a test that
iterated the constant it was testing, so it could not fail; that is plan §8 learning 2, and this
campaign has now hit it three times. **−** I let a mutation harness run under a 2-minute timeout,
which killed it mid-round and left a live mutant in both twins; I only noticed because a test I
had written minutes earlier failed. Had that test not existed I would have committed a mutated
scanner. **−** I started technical work before writing the Phase 1B stub.

Predecessor (S11) evaluation: 9/10. Its handoff was the most operationally useful I have been
given in this campaign: the `next_steps` field told me not to re-derive the table predicate and
*why* (the plan has it empirically tuned), named the exact recovery path for the fixture
(`mts-system` `383c1715:BACKLOG.md`), and predicted the abstention case — all three held exactly.
Its gotchas were load-bearing and every one paid: the `--no-verify` note applied verbatim at my
claim; the `check-handoff`-cannot-validate-a-stub warning saved me from either inventing scores or
debugging a checker working as designed; the importlib/`main()` warning was the difference between
a clean smoke run and corrupting a scanned repo; and its gotcha (1) — *check that each fixture
actually reaches the branch it names* — is the discipline that made my mutation kills double as
branch-reachability proofs. Its `key_files` line numbers all resolved. Most valuable of all was its
carried-forward method rule, *RED-first is necessary but not sufficient — mutation-test each
assertion from a green baseline*; I followed it and it earned its cost immediately. Two small
deductions. First, it flagged the boundary-review freezing gotcha but stated it as advice rather
than as a step, and I nearly re-ran the review live before re-reading it. Second, its own mutation
discipline had the twin-masking hole in it — S11 reported 26 mutants across the session against a
suite containing `test_twins_byte_identical`, so some fraction of those kills were false by the
same mechanism I hit; the learning it handed me was right, but the harness it validated it with
was not, and it did not notice. That is not a correctness failure in what it shipped — I re-ran
its layer's tests and they hold — but it is the one place its evidence was weaker than it read.

```handoff
session: S11
date: 2026-07-25
status: complete
self_score: 8
predecessor_score: 9
active_task: Layer 2 of docs/planning/dashboard-signal-integrity-plan.md — ledger identity (defects 5, 6, 7; upstream issue #60). COMPLETE. DASHBOARD_VERSION 2.9.0 -> 2.9.1. Layers 3-6 remain unclaimed, one per session.
what_was_done: Implemented Layer 2 of the plan ratified in bc2481d, per decision D3 — the dual predicate, not a narrowed locator. _find_changelog still answers LOCATION (best-available, root or docs/, case-insensitive prefix) and still feeds present/is_fresh/Signals B-D; a new _find_action_ledger answers MEMBERSHIP (root CHANGELOG.md, the same probe the compliance checklist uses) and its ledger_present is consumed at exactly one site, the assess_risks ledger risk. Archive shadowing fixed by preferring an exact CHANGELOG.md ahead of prefix matches, prefix search retained as fallback. Signal F moved above the `changelog is None` early return, keeping its adopter gate AND its grace-independence. Every advisory now names the file it was computed against (rel via as_posix) and no longer calls that file "the ledger". RED-first per the standing rule: 18 assertions driven against unpatched code and watched to fail (9 AttributeError for the absent locator, 9 wrong-answer) before the scanner was touched. Then MUTATION-tested per S10's learning — 26 mutants across the session; the first pass killed 15 of 17 and exposed a real hole (Signal F could be grace-suppressed unnoticed, because every fixture drove real history). Ran a 4-lens adversarial review at the boundary BEFORE committing: 8 findings, and the ADVERSARIAL REGRESSION LENS CAME BACK CLEAN (no input found where the new code is worse than the old). Three findings were coverage holes RED-first and mutation had both missed; three landed on my own prose and all three were upheld; two were refuted as pre-existing but got coverage anyway, since this layer rewrote the condition they live in. ONE SCOPE DECISION I MADE AGAINST A REFUTER, flagged for the operator: I first hoisted the exact-CHANGELOG.md preference ACROSS both bases; a reviewer called it scope creep, a refuter called it within the plan's literal text ("over ANY name-prefix match"). I narrowed it to per-base, because the hoist silently moves which file is measured — and the +1 freshness point — for a repo keeping CHANGELOG.rst at root alongside an exact docs/CHANGELOG.md, where nothing is shadowed; that is precisely the failure mode D3 exists to prevent, and the plan's own defect-7 evidence is a same-base pair. Residual pinned by a characterization test: a root holding ONLY an archive still shadows an exact docs/CHANGELOG.md. Ledger entry + this receipt in the same commit.
next_steps: Execute Layer 3 (backlog shape with abstention, defect 4 + the fenced-code-block false positive) of docs/planning/dashboard-signal-integrity-plan.md — _scan_backlog_done returns {format, done, recognized}, strip fenced code blocks BEFORE scanning, keep the checkbox predicate, add the table predicate (a cell that STARTS WITH a done token, in a row of >=3 cells, ignoring the ID column), and abstain visibly on an unrecognized format. DASHBOARD_VERSION -> 2.9.2. Do NOT re-derive the table predicate: plan §Layer 3 has it empirically tuned against the real 643-line backlog (contains-token 321 = 94 false positives; equals-token 227 misses bolded forms; starts-with/>=3-cells/ignore-ID 256, within 3 of S8's hand count) — recover that backlog from mts-system commit 383c1715:BACKLOG.md. RED-first AND mutation-test again, and this time also check each new fixture actually REACHES the branch it names (see gotcha 1). This repo's own docs/planning/BACKLOG.md is the abstention case (| Item | Scope | Outcome |, no Status column) and must say so out loud rather than report 0. OPERATOR DECISION OWED, do not decide it in an implementing session: whether to keep the per-base exact-match scoping shipped here or hoist it across bases (see what_was_done; both sides are argued in the CHANGELOG entry and pinned by tests).
key_files: tools/methodology_dashboard.py:658 (_find_changelog — LOCATION, per-base exact preference + prefix fallback), tools/methodology_dashboard.py:702 (_find_action_ledger — MEMBERSHIP, root-exact, is_file), tools/methodology_dashboard.py:748 (the ledger_present key), tools/methodology_dashboard.py:763 (ledger_present computed above the early return), tools/methodology_dashboard.py:793 (rel via as_posix — display AND git pathspec), tools/methodology_dashboard.py:1503 (the one risk that reads ledger_present), tools/test_methodology_dashboard.py:571 (guard-the-guard: calls the real checklist rather than re-implementing it), tools/test_methodology_dashboard.py:612 (characterization test pinning the residual archive/docs limitation), tools/test_methodology_dashboard.py:817 (TestMembershipRiskGating — the history gate, previously untested on both sides), docs/planning/dashboard-signal-integrity-plan.md:215 (Layer 3, next)
gotchas: (1) A fixture can fail to reach the branch it is named for. My new-adopter-grace test asserted result["new_adopter_grace"] on a repo with NO changelog — but grace is only computed AFTER the early return, so the key was always False and the test failed against correct code. Worse, while it was failing it made the mutation harness report FALSE KILLS for every mutant: a mutation run is only meaningful from a green baseline. Re-run the suite clean before trusting any mutation verdict. (2) macOS is case-INSENSITIVE, so (p/"CHANGELOG.md").is_file() is True for a file named changelog.md and a test asserting otherwise passes on Linux and fails here. That is plan §7 residual risk 6, live. Assert the INVARIANT (the ledger locator and the checklist probe answer alike) rather than a platform-dependent value. (3) Two mutants survive by construction and are not holes: str() vs as_posix() is byte-identical on POSIX (proven — it differs only on Windows), and moving the ledger_present assignment below the early return is logically inert, because "no changelog located" now implies "no root ledger" EXCEPT when iterdir() itself raises OSError. Do not "fix" either by inventing a test. (4) changelog["present"] now has NO consumer inside the scanner — its one reader moved to ledger_present. It is still emitted in the metrics/JSON and read by tests, so it is informational, not dead; do not delete it without checking the JSON contract. (5) The dashboard still cannot scan its own repo in place (ROOT = Path(__file__).parent resolves to tools/). Load it via importlib and call collect_all(Path(target)); never call main() against a real repo (it writes dashboard.html + dashboard_history.jsonl into the scan root). (6) A receipt-only or claim-only commit needs --no-verify (the pre-commit hook wants CHANGELOG.md co-staged); backstopped by Phase 0 reconcile. (7) bin/check-links is PYTHON — run python3 bin/check-links. (8) Boundary-review agents read the working tree WHILE I was editing it; two refuters explicitly noted the tree moved under them and had to freeze copies in /tmp. Their line numbers may be stale by the time you read their findings — re-locate before acting, and prefer landing review-driven edits after the lens returns, not during. (9) Layer 5 still owes the doc sweep, and this layer added nothing to its table: I grepped the corpus for the advisory strings this layer changed and every hit is frozen historical prose (the plan's own defect table, the Layer 1 ledger entry) that correctly describes the pre-fix state.
runtime_smoke: Ran the REAL render path against live collected metrics (collect_all -> render_project_card -> render_methodology_grid -> render_html -> append_history), writing nothing into any scanned repo. Five real sibling repos: all keep a root CHANGELOG.md, so ledger_present is True for every one and NO new risk fires anywhere on the live fleet. airqino shows the new advisory format live: "CHANGELOG.md: 10 commits since it was last updated (Component C)" and "CHANGELOG.md trails HEAD by 71 days" (was "CHANGELOG ledger lag: ..." / "CHANGELOG frontier trails ..."). Three synthetic fixtures drove the defects end to end: D5 (adopter, only docs/changelog.md) now raises "no root CHANGELOG.md action ledger" AND keeps is_fresh True with documentation 10/20 — the regression the obvious fix would have caused; D6 (60 done-marks, no changelog at all) now emits Signal F, previously silent; D7 (root CHANGELOG-archive.md + CHANGELOG.md committed at HEAD) locates CHANGELOG.md with 0 unlogged commits, where the verbatim pre-Layer-2 locator picked the archive and reported the repo 13 commits behind. Rendered HTML 42,282 chars with no "CHANGELOG ledger lag" string anywhere; history entries carry dashboard_version 2.9.1. Suites: tools/test_methodology_dashboard.py 47 -> 79 tests OK; bin/tests.sh 84 passed / 0 failed; python3 bin/check-links OK (82 links / 21 files); diff -q twins identical; both twins declare DASHBOARD_VERSION 2.9.1; py_compile clean.
changelog_ref: CHANGELOG.md entry "Dashboard signal-integrity Layer 2 — ledger identity", commit 3838a13
commit: 3838a13
```
Self-score 8/10. **+** Held RED-first *and* added the mutation discipline S10 paid for — which
immediately earned its cost by exposing a hole (grace-suppressible Signal F) that RED-first alone
could never surface, because every fixture I had written drove real history. **+** Reviewed at the
boundary before the commit landed, and reproduced **every** finding myself rather than adopting
it: that is how I caught that one reviewer's mutant was a semantic no-op, and how I confirmed the
three that were real. **+** Refused a refuter's verdict where I had better evidence — narrowing the
exact-match preference to per-base — and then wrote the counter-argument into the ledger and pinned
the residual with a characterization test, so the decision is reversible by whoever disagrees.
**+** Proved defect 7 by running the verbatim pre-Layer-2 locator against the same fixture instead
of reasoning about what it would have done. **+** Grepped the corpus for the advisory strings this
layer changed rather than assuming Layer 5 owns every doc consequence. **−** Three of my own
comments overstated what the code does, and all three were caught by a reviewer rather than by me —
including one that reproduced, in prose, the exact location-for-membership conflation this layer
exists to fix. In a change about signal integrity that is the least excusable class of defect I
could ship. **−** My first-cut fixtures twice asserted a property over an input that could not
violate it (the fallback lock with no `docs/` base; the grace test on a repo where grace is never
computed) — the campaign's own §8 learning 2, third occurrence. **−** I let the boundary review
run against a working tree I was still editing, so two refuters had to freeze copies and reason
about a moving target; their findings arrived partly stale through my own doing. **−** I hoisted
the exact-match preference across bases on first pass without noticing it changed an unrelated
repo shape — the narrowing was a reviewer's catch, not mine.

Predecessor (S10) evaluation: 9/10. The single most valuable thing it handed me was not code but a
correction to method: *RED-first is necessary but not sufficient — mutation-test each assertion.*
I followed it, and it paid immediately — the grace-suppression hole was invisible to a green
RED-first suite and would have shipped. Its gotchas were load-bearing and accurate: the warning
that `bin/check-handoff` cannot validate a 1B stub saved me from either fabricating scores or
debugging a checker that was working as designed; the importlib/`main()` warnings held; the
`--no-verify` note applied verbatim at my claim commit. Its `key_files` line numbers all resolved
to the code they claimed (`:133`, `:796`, `:1348`, `:1391`, `:1612`, `:1707`, `:2313`), and its
correction of the ratified plan — that the grid misalignment was *live*, not prospective, verified
by rendering HEAD's scanner rather than by reading the plan — is exactly the standard this campaign
needs. Two deductions, both small and both about scope calibration rather than correctness. First,
its own retrospective called the 5-lens sweep wasteful and said "one lens would have done"; that
advice was too strong, and I nearly under-reviewed on the strength of it. My 4-lens run produced
findings from *three* different lenses that no single lens would have covered — the regression lens
came back clean, which is itself information, while test-quality and prose-accuracy each found real
defects the other could not have. The correct lesson was narrower: drop the lens whose findings a
*later layer* already owns, not "use one lens". Second, it left `changelog["present"]`'s
consumer-count unexamined while touching the neighbouring risk site; noticing that the key was one
edit away from having no reader would have cost nothing and belonged in the handoff I received.
Neither touches the layer it shipped, which held up under a 4-lens adversarial review.

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
