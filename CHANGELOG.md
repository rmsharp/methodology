# Changelog — Authoritative Action Ledger

The cumulative, append-only record of **actions taken in this repository** — across backlog
items, repository issues, and ad-hoc work. It is the authoritative answer to *"what was done
here, ever?"*, distinct from the release narrative in [`CLAUDE.md` §Versioning](CLAUDE.md#versioning).

This repository dogfoods its own methodology: every session records its actions here at
close-out (`starter-kit/SESSION_RUNNER.md` Phase 3F), and Phase 0 reconciles the ledger against
`git log` and backfills anything a crashed or out-of-band session missed. Taking an action — any
commit, or any non-commit action (release, tag, PR, upstream issue close, access grant, grooming
decision) — and not recording it is failure mode #27. The full close-out and reconcile rules, plus
the reusable seed, live in [`starter-kit/CHANGELOG.md`](starter-kit/CHANGELOG.md).

**Source tag — exactly one per entry**, so `grep -E '\[(issue #|BL-|ad hoc)' CHANGELOG.md`
enumerates every logged action and proves all three sources landed:

- `[issue #<N>]` — a repository issue. Issues for this repo live in the **upstream** parent
  `KJ5HST/methodology` (this fork has Issues disabled), so entries cite an **absolute URL**, never
  a bare `#<N>`.
- `[BL-<N>]` — a `docs/planning/BACKLOG.md` item, removed from the backlog in the same commit.
- `[ad hoc]` — work with no backlog or issue origin: releases, tag/branch ops, PR opens, upstream
  issue closes, access grants, and decline/wontfix/grooming decisions.

**Boundary vs. `CLAUDE.md` §Versioning — so the two ledgers cannot diverge.** §Versioning owns
*released-version semantics* (one narrated entry per shipped version); `README.md` §What's New is
its public restatement. This ledger is the *per-action operational timeline*, including
non-release work (housekeeping, doc-only PRs, adopter coordination, backlog grooming) that
otherwise has no home but raw `git log`. Where the two overlap — a release — this ledger carries a
**one-line pointer** into §Versioning, never a re-narration (cite, don't restate).

Reverse-chronological, newest on top; prepend-only. Promote to `## YYYY-MM` sections as it grows.

---

### 2026-07-25 · [ad hoc] Dashboard signal-integrity **Layer 5** — completeness-critic doc sweep (no version bump)

- **Change:** the fifth layer of the ratified campaign plan `docs/planning/dashboard-signal-integrity-plan.md`
  (S9, `bc2481d`), and the first that ships **no scanner code** — `DASHBOARD_VERSION` stays **2.10.0**,
  both twins untouched. Layers 1–4 added a member to a numbered set, added a detection axis, and made
  two health dimensions context-dependent; **not one** of those appeared in a prose file, which is the
  blind spot v3.4 Learning #10 / `AUDIT_WORKSTREAM.md` anti-pattern #9 exist to close.
- **The plan's Layer 5 table was re-derived from the shipped diffs, not trusted.** It listed 6 rows; the
  swept corpus yielded **20 sites across 7 files**. Landed in two commits (the 5-file per-commit cap):
  this one covers `README.md`, `CLAUDE.md`, `HOW_TO_USE.md`, `starter-kit/BOOTSTRAP.md`.
- **The plan's headline row was wrong, and was refuted rather than applied.** It directed a fix at
  `README.md`'s `.methodology-profile` line for documenting only one axis. That line sits inside
  `### What's New in v3.2` — dated prose the v2.7.1 convention freezes, which the plan's *own*
  not-edited list names — and it correctly describes what v3.2 shipped. `grep -rn "methodology-profile"`
  returns **three hits, all inside that frozen section**: the real defect is that the marker had **no live
  documentation anywhere**, which is the plan's residual risk #3 (*"the marker is the escape hatch;
  document it"*). Fixed by adding operative documentation of both axes to `README.md` §Methodology
  Dashboard and `BOOTSTRAP.md` Step 9 (distributed), leaving the v3.2 entry untouched.
- **Verify-don't-edit, verified:** `README.md`'s "health (0-100) across 5 weighted dimensions" was
  measured **false before the campaign** (the pre-L1 scanner scores this repo's tutorial fixture at
  health **62** with a methodology dimension of **22**) and **true at HEAD**. No edit — as the plan said.
- **Scope widened by operator decision, on evidence.** (a) The `HANDOFFS.md` enumeration gap the plan
  adopted at 2 sites is systemic at **11**; all 11 are being fixed rather than leaving 9 known-stale
  siblings behind. (b) Two stale count/size claims not caused by this campaign are included:
  `HOW_TO_USE.md` sized `SESSION_RUNNER.md` at "~150 lines" (actual **397**) and
  `ITERATIVE_METHODOLOGY.md` at "~587" (actual **880**).
- **A false claim in this layer's own new prose was caught before commit.** The first draft of the
  marker documentation asserted that the card always names the path that produced the verdict, "so a
  marker override is never silent." Fixture-tested: a structurally-framework repo declaring `adopter`
  renders **no** provenance line at all — only framework-role cards carry it. Corrected in place. The
  contradiction-fallback claim was tested the same way and held (`framework adopter` on a structurally
  framework repo → `role=framework, reason=marker-contradiction`).
- **Recorded, deliberately not fixed here:** `CLAUDE.md`'s starter-kit table still omits three other
  files (`CLAUDE_TEMPLATE.md`, `CONTEXT_TEMPLATE.md`, `RECOMMENDED_SKILLS.md`) — a separate, older gap
  outside the approved scope; `docs/images/*.png` have shown pre-campaign renderings since v2.0
  (`9639ce6`); the scanner's own module docstring documents `METHODOLOGY_ITEMS` but neither
  `FRAMEWORK_ITEMS` nor the marker, and editing it is a code change this layer does not make.
- **Part 2 — the tutorials** (`T1_setup.md`, `T7_portfolio_dashboard.md`, `T8_keeping_current.md`):
  the remaining `HANDOFFS.md` enumeration sites, including **T8's worked `bin/status` transcript**,
  which showed three SEED rows where the tool emits four — a learner compares their own output
  against that block. T8's "all **21** distributed files" corrected to **22**, verified by counting
  `bin/status` rows against a real synced fixture (21 is the *markdown* count `bin/check-links`
  reports; `bin/status` covers the manifest's 22 entries, `methodology_dashboard.py` included).
- **T7 now teaches the Layer 3 abstention, because the campaign made it fire on the tutorials' own
  sample project.** `docs/tutorials/sample-project/BACKLOG.md` is a feature table with no `Status`
  column and no checkboxes, so at HEAD it scans `format: unrecognized` and the sample — the repo T7
  presents as "the methodology working as designed" — now carries a LOW advisory T7 never mentioned.
  Measured on a rebuilt post-T1 fixture (`sample-project` + `git init` + `bin/sync`): pre-campaign
  3 medium + 1 low; at HEAD the same plus that new LOW. The advisory is quoted **verbatim** (asserted
  byte-equal against the live risk string) and taught as the design working: an unjustifiable 0 would
  be indistinguishable from a clean backlog, so abstention says the signal is *off*, not *green*.
  Two adjacent claims corrected because the addition would otherwise contradict them: T7's expected
  result and risk-bucket cell said the sample's only flag was `No CI/CD`, and the fixture carries
  three mediums — that inaccuracy predates this campaign.
- **The deferred boundary review was run after close-out and found FOUR real defects — three in
  this layer's own new prose, one in the scanner.** Two lenses (marker documentation, numbers) ran
  against the frozen tree; every finding was re-verified by hand before acting. Fixed here:
  (a) the marker documentation never said the declaration line is read as **tokens**, so an
  uncommented sentence placed first silently declares any axis word it contains — measured:
  `We follow the framework conventions for this paper.` grades the repo **framework, reason=marker**
  and discards a `doc-only` on the line below. That is the same failure class S13's review caught
  *in the code*, surviving in the prose that documents it. (b) `BOOTSTRAP.md`'s "every line after
  the first is prose" was **false** whenever line 1 is a comment — a leading `#` does not consume
  the declaration slot (`README.md` stated the rule correctly; the distributed file did not).
  (c) "first non-comment line" under-described the parser, which also skips blank lines. Both
  worked examples added here were executed verbatim and assert `tokens=['doc-only']`,
  `doc_only=True`, `reason=marker`.
- **A LIVE SCANNER DEFECT, found by the same review and NOT fixed here — it needs an operator
  decision and a code layer.** `bin/sync` installs `methodology_dashboard.py` (**3,070 lines**) to
  the adopter root, and `DOC_ONLY_SOURCE_LOC_MAX` is **200**, so the source-LOC cap short-circuits
  before the doc-corpus check runs: **installing the methodology destroys the doc-only fair-scoring
  v3.2 exists to provide.** Measured on a Quarto-book fixture — before `bin/sync`: `doc_only=True`,
  testing dimension **4** (render proxy), no test risk; after `bin/sync`: `doc_only=False`,
  `source_loc=3070`, testing dimension **0**, and the HIGH **"No test infrastructure"** risk is
  back. This predates Layer 5 and has been live since v3.2. Layer 5 corrects only the *prose* that
  misdescribed it — `README.md` and `BOOTSTRAP.md` now tell a document-only project it **must**
  declare `doc-only`, rather than framing the marker as a fallback for when the guess is wrong.
- **This layer's deliverable shipped BEFORE that review ran, and that is recorded rather than
  glossed.** A 4-lens review was launched against the frozen tree and all four agents died on a usage
  limit; the harness returned `findings: []`, which means *nothing executed*, not *nothing found*.
  Two lenses were then run by hand (the T7 counterfactual — adding a `Status` column to a rebuilt
  fixture removes the advisory and restoring it brings the advisory back; and a plain code+docs adopter
  fixture confirming it is `doc_only=False` / `role=adopter` and renders the plain five dimension labels
  plus "Methodology Compliance"). What remains unreviewed is an independent pass over the new marker
  documentation's completeness and wording. **Re-running it is Layer 6's first act.**
- **Commit/PR:** `baa1dd1` (part 1, core docs) and `fc65013` (part 2, tutorials); split only by the
  5-file per-commit cap. Close-out receipt in this commit. **Layer 6** — close-out, release decision R1, the owed `SESSION_RUNNER.md`
  Learnings row, and the D4 plan correction — remains a separate session.
- **Session:** S14 · **Verified:** `bin/check-links` OK (82 links / 21 files); `bin/tests.sh` 84 passed
  / 0 failed; `tools/test_methodology_dashboard.py` 168 OK; twins byte-identical; exhaustive grep
  reconciliation of both fixed classes shows every remaining hit is either the tutorials (part 2) or
  frozen dated prose.

### 2026-07-25 · [issue #59] Dashboard signal-integrity **Layer 4** — repo role (`DASHBOARD_VERSION` 2.9.2 → 2.10.0)
- **Change:** the fourth implementation layer of the ratified campaign plan
  `docs/planning/dashboard-signal-integrity-plan.md` (S9, `bc2481d`). Closes
  [#59](https://github.com/KJ5HST/methodology/issues/59) — the scanner graded **every** repo
  against `METHODOLOGY_ITEMS`, a checklist of adopter-**root** operating files. The repo that
  *publishes* the methodology does not install its own corpus into its own root, so scanning this
  one produced **compliance 10 of 115 = 9%**, a methodology dimension of **1/20**, health
  **49/100**, and a false medium risk **"Partial methodology adoption (9%)"** — reproduced at HEAD
  before a line was changed. New `detect_repo_role` + a separate **`FRAMEWORK_ITEMS`** checklist,
  scored and rendered under its own name.
- **Detection is marker-override → structural heuristic**, following the BL-5 precedent. The
  structural test is a **three-way AND**: `bin/_manifest.py` **and** `starter-kit/SESSION_RUNNER.md`
  present, **and no root `SESSION_RUNNER.md`**. The plan names the first two; the third mechanizes
  the plan's own §7.3 description of the one shape this could misfire on — a repo that ships
  starter-kit templates plus distribution machinery *without installing to its own root* — so a
  monorepo that vendors this framework **and** genuinely runs it keeps its adoption grading. It can
  only remove false positives, never create one. Sound because the manifest ships **0 of 22**
  sources from `bin/`: no synced adopter can acquire `bin/_manifest.py`. Verified against all 10
  live siblings — exactly one repo matches, and every adopter comes back `adopter`.
- **The two files that PROVE the role are deliberately NOT scored.** If the evidence for the role
  also earned points, the raw sum would have a nonzero floor on the structural path and the
  "no corpus at all" branch would become a correct assertion over an input that can never occur —
  **defect 6's exact failure class, re-created inside the campaign that closed it**. Excluding them
  keeps `raw == 0` genuinely reachable and stops the checklist scoring its own premise; the role's
  provenance is *displayed* on the card instead.
- **`FRAMEWORK_ITEMS` (sum 105, derived — never a literal, per D1)** asks two questions a publisher
  can actually answer: does it *publish* a complete corpus (`ITERATIVE_METHODOLOGY.md`,
  `starter-kit/SAFEGUARDS.md`, `workstreams/`, `starter-kit/BOOTSTRAP.md`, `HOW_TO_USE.md`, plus the
  machinery that delivers it — `bin/sync`, `bin/status`, `bin/tests.sh`), and does it *operate* the
  methodology it publishes (root `CHANGELOG.md`, root `HANDOFFS.md`)? The second half is why the
  role swap is **not a hiding place**: without it, becoming a "framework" repo would stop the
  scanner asking whether the publisher runs its own rules.
- **Operator decision — the plan's line-255 prohibition.** The plan forbids scoring the framework
  repo by remapping `METHODOLOGY_ITEMS` onto `starter-kit/` paths; its stated harm is crediting
  placeholders, and that harm is real (`starter-kit/SESSION_NOTES.md` is a 27-line stub,
  `starter-kit/BACKLOG.md` does not exist, `starter-kit/ROADMAP.md` is an 18-line skeleton).
  `starter-kit/SAFEGUARDS.md` — a real 242-line published document — is **permitted**, with the
  boundary drawn **mechanically rather than by reading**: a canonical test asserts that no
  `FRAMEWORK_ITEMS` path is a distribution **SEED** source, which excludes all four placeholders by
  construction. Ratified by the operator, not settled by the implementing session.
- **The marker gained a second axis, and that forced a rewrite of shipped BL-5 code.**
  `.methodology-profile` now answers two questions — corpus (`doc-only` | `code`) and role
  (`framework` | `adopter`) — through one shared reader, with the pairs asserted **disjoint** by
  test. Reading only `tokens[0]` made the plan's own Layer 4 proof ("a `doc-only framework` marker
  satisfies both axes") **unsatisfiable**: measured against HEAD, `doc-only framework` was honoured
  but **`framework doc-only` silently discarded the owner's doc-only declaration**, a leading
  comment line discarded it too, and `doc-only code` vs `code doc-only` resolved a contradiction by
  **word order**. So Layer 4 could not be purely additive here.
- **Comment stripping is the load-bearing part of that reader, and it came from real data, not
  design.** The only `.methodology-profile` in the live population (`church_growth`) is **8 lines /
  87 whitespace tokens**: one declaration plus **seven** lines of `#` prose explaining why the owner set it —
  and that prose mentions the opposite token **twice**. It survives being read as a token bag only
  because both mentions carry trailing punctuation (`code,` and `code.`). **Delete one comma and a
  reader that tokenizes comments discards the very override the file exists to assert**, restoring
  the false "No test infrastructure" penalty BL-5 added the marker to prevent. Switching to
  full-token scanning *without* stripping comments would therefore have been strictly **more**
  dangerous than reading the first token — the plan's instruction, taken literally, was a trap.
- **A contradictory marker abstains on that axis only** (decision D4 applied to the marker): it
  falls through to that axis's heuristic for the *value*, keeps `marker-contradiction` as its
  *reason*, and raises one LOW advisory. An unresolvable declaration is disclosed, never resolved by
  guessing — and the uncontradicted axis on the same line still resolves.
- **The risk layer replaces rather than suppresses.** For `role == framework` the two adoption
  branches are gone — the word "adoption" is not merely unflattering there, it is **false** — and in
  their place a **HIGH** "No framework corpus detected" (reachable, per the unscored-inputs rule)
  and a **graded** "Framework integrity incomplete (N%) — missing: …" that **names the members**.
  Naming them is the finding: losing *both* root ledgers still scores 81%, so a percentage-only
  rung would have said nothing about it.
- **The regression this layer would otherwise have inflicted on the campaign itself.** The
  Component-C ledger risk was gated on `items.get("SESSION_RUNNER.md")`. Under `FRAMEWORK_ITEMS`
  that key does not exist, so the gate would have returned False forever and the risk would have
  gone **unreachable for every framework repo — silently, with no test failing**, on the one repo
  that dogfoods the v3.1 ledger rule it publishes. Verified by driving HEAD's `assess_risks` with a
  framework-shaped items dict: the risk vanishes. Fixed by deriving an explicit `owes_ledger`
  predicate instead of probing a checklist key, and by naming a publisher a publisher.
- **The grid does not misalign — it *lies*, and that is why it needed handling.** Rendered before
  the fix: the two checklists overlap at exactly `CHANGELOG.md` and `HANDOFFS.md`, so a
  framework-keyed `items` dict rendered against the nine adopter columns came out **correctly
  aligned** with **two ✓ beside seven ✗** — under headers naming files the repo was never scored
  on — and the existing width assertion passed against it. Aligned *and partly true* is worse than
  either broken or all-red: the two accidental ticks make the row look considered. A framework row now renders one neutral
  `colspan` cell (a **third glyph**, never a ✗), a daggered score, and a legend that appears only
  when a framework row does. Deriving `item_keys` per project — the obvious alternative — was
  rejected: it puts a 10-cell row under an 11-column header, which is **Layer 1's defect
  reintroduced by the campaign that closed it**.
- **The card** swaps its heading to **Framework Integrity**, reads the denominator from the project
  rather than the module global (rendering `METHODOLOGY_MAX` there would print the literal
  arithmetic falsehood *"100% (105 of 115)"*), iterates the items that were actually **scored** so
  every glyph names something the percentage counted, swaps the Health-Breakdown label to
  **Framework**, and prints the role's **provenance** — a one-word marker is a grading opt-out, so
  how a repo came to be graded as a publisher must be visible.
- **Plan residual risk 8 is now disclosed on BOTH cards** (operator decision): *"presence check —
  the scanner does not verify these files are used"*. The plan calls this footnote "the honest
  disclosure" — it had **never been shipped**. It is equally true of both checklists: `mts-system`
  scores 100% compliance while running a v2.0-era runner.
- **Reachability, checked because this campaign's defect 6 was an unreachable signal.**
  `EXCLUDE_DIRS` contains the literal string `"methodology"`, so a sibling directory of that exact
  name is skipped in **portfolio** mode and this repo is not among the 9 discovered siblings. The
  false risk is reached via **single-project mode** — a dashboard copy at the repo root, which is
  exactly how `BOOTSTRAP.md` tells an operator to run it — or by any fork or clone under a different
  directory name. **The release note must not claim the portfolio dashboard stops mis-scoring the
  framework repo.**
- **Verified:** `tools/test_methodology_dashboard.py` **116 → 168** tests OK; `bin/tests.sh` 84
  passed / 0 failed; `bin/check-links` OK (82 links / 21 files); twins byte-identical, both
  declaring `DASHBOARD_VERSION 2.10.0`; `py_compile` clean. **RED-first**, and the reds that matter
  are behavioural rather than `AttributeError`: 5 assertions failed against unpatched code with
  *wrong answers* before any scanner line changed. **Mutation-tested from a green baseline with
  BOTH twins patched** (a harness patching only `tools/` lets the twin byte-compare fake every
  kill): 34 mutants, first run **31 killed / 3 survived**. One survivor was inert (a redundant
  comment-stripping branch, since removed so no later reader mistakes which line does the work);
  **two were real holes** — no test used a **trailing** `#` comment on a declaration line, and the
  Health-Breakdown label could revert to "Methodology" with the whole suite green. After the
  boundary-review fixes the set stands at **38 mutants, 38 killed, 0 survived**.
- **Boundary review before the commit landed, against a frozen tree**: 5 lenses (plan fidelity,
  reachability/regression, comment honesty, fresh-eyes correctness, completeness critic), one
  skeptical refuter per finding defaulting to *refuted* — **28 raw → 8 confirmed**, all 8 fixed.
  **The HIGH finding was a defect this layer would otherwise have shipped, and it inverted the
  defect being fixed.** The first reader mined *every* line of `.methodology-profile` for
  declaration tokens, so an owner's own **uncommented** sentence was read as a deliberate
  override: *"We keep our docs in the framework style"* graded a plain adopter as the **publisher**
  (`reason: marker`, nothing disclosed), and *"This is a code repository with helper scripts"*
  under a `doc-only` declaration fabricated a **contradiction** and destroyed the override. Reading
  `tokens[0]` never had that failure — whole-file scanning was a regression dressed as a fix. Now
  **only the first line that survives comment-stripping is a declaration**; every later line is
  prose. Composing the two axes needs one line, not two. A MEDIUM finding showed `role_reason` was
  wired from `detect_repo_role` to the card with **nothing pinning the wire** — hardcoding it makes
  a *marker*-classified repo's card assert `structural: bin/_manifest.py + …` about a repo that has
  neither file — now covered end to end. The remaining six were **false claims in my own prose**:
  the grid rationale and its test docstring asserted the checklists "share no keys" and rendered
  "eight red crosses" (measured: two shared keys, nine columns, 2 ✓ + 7 ✗); the user-facing legend
  said those columns "do not apply" to a framework repo when two of them do; the live marker was
  described as six comment lines when it has seven; a fixture was called a copy of that file when
  it is a paraphrase; and a test named `test_no_live_sibling_is_misdetected` claimed to be "driven
  against real trees" while driving a tempdir — renamed, and the live sweep is recorded here
  instead of implied by the suite. **In a change about signals that do not mean what they appear to
  mean, prose that misstates its own evidence is the least excusable defect available**, and six of
  eight confirmed findings were exactly that.
- **Live fleet impact: exactly one repo's scoring moves, and it is the target.** Before/after scan
  of all 10 siblings: `methodology` goes compliance 10 → 105, 9% → 100%, methodology dimension
  1 → 20, and loses the false adoption risk. **Every other repo is byte-identical** (`wsfct`'s only
  delta is a branch count 261 → 262, live git drift — this diff touches no branch-counting code).
  A genuine non-adopter is *not* laundered: `claims-model-starter.wiki` stays at 4% / 0-of-20.
  **Honest attribution of this repo's health 49 → 72:** **+19** is the fix; **+4** is the *testing*
  dimension rising because this session added ~430 lines of tests and crossed the 0.3 test:source
  rung — not a scoring change, and not creditable to the fix.
- **Not a whitewash:** the findings that are *true* of this repo survive the reframing — it still
  reports `No CI/CD pipeline` and `Large files detected`.
- **Owed to Layer 6 (plan correction, deliberately not fixed here — operator decision):** ratified
  decision **D4 states this repo's own `docs/planning/BACKLOG.md` "lands in that branch and will
  correctly say so"**, and that is **false at HEAD**. The format *is* read as `unrecognized`, but
  the advisory is suppressed by Signal F's operator gate (root `SESSION_RUNNER.md`), which this repo
  fails. Widening that gate was rejected for this layer because Signal F's premise — an item is
  *removed* from `BACKLOG.md` in the commit that logs it to `CHANGELOG.md` — is verifiably false for
  this repo class, whose retired backlog deliberately **keeps** all seven completed `BL-1`–`BL-7`
  rows permanently; widening the counting branch would manufacture a false "not migrated"
  accusation the moment that table gains a Status column.
- **Owed to Layer 5 (mandatory doc sweep):** the marker is documented in `README.md` as
  `doc-only | code` and now has a second axis; the plan's Layer 5 table predates both the second
  checklist and the new marker axis, so it needs rows this layer added.
- **Commit/PR:** this commit (fork `main`; upstream #59 stays open until this reaches upstream).
- **Session:** S13 · **Verified:** as above.

### 2026-07-25 · [ad hoc] Dashboard signal-integrity **Layer 3** — backlog shape with abstention (`DASHBOARD_VERSION` 2.9.1 → 2.9.2)
- **Change:** the third implementation layer of the ratified campaign plan
  `docs/planning/dashboard-signal-integrity-plan.md` (S9, `bc2481d`). Closes plan **defect 4** and
  the **fenced-code-block false positive**, neither of which is filed upstream — the plan stands as
  their record pending the operator's filing decision at merge. Signal F counted `BACKLOG.md`
  done-marks with a **checkbox-only** regex, so a real 643-line *table* backlog carrying **256**
  done-marks reported **0** — and reported it *silently*, indistinguishable from a clean backlog.
  `_count_backlog_done` becomes **`_scan_backlog_done`**, returning `{format, done, recognized,
  source}`: the count now travels with the convention it was read under.
- **Six formats, in decision order** — `unreadable` (I/O error), `checkbox`, `table`,
  `unrecognized`, `none`, `absent`. **Abstention is a first-class result** (decision D4): a table
  with no Status column, or plain list items with no checkbox, abstains *out loud* rather than
  reporting a 0 it cannot support. **A silent 0 is defect 4 itself.**
- **The abstention is deliberately NARROW, and that is the load-bearing design choice.** An
  *empty* backlog reports a silent, correct 0 (`format: none`) instead of abstaining — two live
  adopters (`airqino`, `model_project_constructor`) keep exactly that file, and telling a project
  that is simply up to date that its "format was not recognized" would be a signal that does not
  mean what it appears to mean: this campaign's own root defect, re-created inside its fix. The
  abstention fires only on **item-bearing content whose convention cannot be read**, which is this
  repo's own `| Item | Scope | Outcome |` backlog — the case the plan names.
- **The table predicate was NOT re-derived** (the plan forbids it): a cell that *starts with* a
  done token, in a row of >= 3 cells, ignoring the ID column. The plan records its three tuning
  counts but not the token list, so the 8-token set was **recovered by search** and reproduces all
  three simultaneously — *contains* 321, *equals* 227, this predicate **256** (hand count 253).
  That is corroboration, **not uniqueness**: any superset adding tokens the corpus never uses
  reproduces the same numbers. Only `DONE`/`FIXED`/`RESOLVED` are exercised by that corpus at all;
  all eight are now pinned by test, because a token no test exercises is one no one can safely
  change. The 256 was re-verified against the clean tree at every step.
- **Known limitation, measured rather than assumed.** The predicate is a *union over every non-ID
  cell*, not a read of the Status column, so a TITLE cell reading "Fixed login redirect" (status
  READY) counts, as does a 3-column legend's "Completed and tested". On the tuning corpus this
  costs nothing — of the 256, **242** are counted via a Status column and **14** sit in tables with
  no Status column, and **none** only via another column. Narrowing to the Status column would drop
  those 14 and move the ratified count to **242**, so it is an **operator decision, not an
  implementer's**. The behaviour is pinned by characterization test rather than silently changed.
- **Adversarially reviewed at the boundary before the commit landed** — 5 diverse lenses against a
  *frozen* tree, then one skeptical verifier per finding: **23 raw → 15 confirmed**, all 15 fixed.
  Two were **regressions in this layer's own new code**, and both are the campaign's thesis defect
  reproduced inside its fix: (1) an **unterminated fence swallowed the rest of the file**, so one
  stray ` ``` ` line turned a backlog full of unmigrated work into `format: none` — *affirmatively
  the healthy state* — where the old scanner had warned; worse, with a Status table above the stray
  fence it returned a **trusted** zero (`recognized: True`). Only *closed* fences are stripped now,
  which is deliberately **not** what a markdown renderer does. (2) A **GFM-escaped pipe** (`\|`)
  split a cell that was never split, shifting NOTES prose into the position the predicate reads and
  fabricating a done-mark on an open row. Also fixed: a table **header** row was scanned as data, so
  a column headed `Completed` counted itself as finished work.
- **Method.** RED-first per the standing rule — every defect-proving assertion was driven against
  the unpatched scanner and watched to fail (table fixture 0, fenced 2, abstention a silent 0), and
  the behavioural REDs were captured against the *old function* rather than resting on the weak
  `AttributeError` that a renamed function produces. Then mutation-tested per S10/S11's learning —
  and the **first mutation run was invalid**: the harness patched only `tools/`, so the
  byte-identical-twin test killed every mutant regardless of behaviour and reported a false 28/28.
  Re-run with both twins patched, it exposed **8 real holes**, one of them *in a test written to
  close a hole* — `test_every_shipped_done_token_is_counted` built its fixture by iterating the very
  constant it tested, so it passed no matter which tokens were removed. A test derived from the
  thing under test cannot falsify it (plan §8 learning 2, caught here for the third time in this
  campaign).
- **Suite:** `tools/test_methodology_dashboard.py` **79 → 116** tests; `bin/tests.sh` **84/84**;
  `python3 bin/check-links` OK (82 links / 21 files); twins byte-identical; `py_compile` clean.
  Runtime smoke ran the **real** render path (`collect_all` → `render_project_card` →
  `render_methodology_grid` → `render_html` → `append_history`) over five real sibling repos,
  writing nothing into any of them; history entries carry `dashboard_version 2.9.2`.
- **Live fleet impact: no new risk fires anywhere, and no health score moves.** `church_growth`
  keeps its existing advisory (now naming its source file and format); `mts-system` and `wsfct` are
  newly *readable* as table backlogs and correctly report **0** — `mts-system` mentions a done token
  on 12 lines and none is a done row, which is the false-positive class rejected on live data;
  `airqino` and `model_project_constructor` stay silent.

### 2026-07-25 · [issue #60] Dashboard signal-integrity **Layer 2** — ledger identity (`DASHBOARD_VERSION` 2.9.0 → 2.9.1)
- **Change:** the second implementation layer of the ratified campaign plan
  `docs/planning/dashboard-signal-integrity-plan.md` (S9, `bc2481d`). Closes
  [#60](https://github.com/KJ5HST/methodology/issues/60) plus two defects found while planning and
  never filed. All three are one error in three places — **file location standing in for a semantic
  finding**. (1) A `docs/` **product changelog masked a missing action ledger**: three subsystems
  answered *"does this repo have a changelog"* three different ways and the risk layer trusted the
  widest, so a methodology adopter whose only changelog was release notes for a shipped artifact
  was never told it kept no ledger — it was advised to go update the release notes instead. (2)
  **Archive shadowing**: the locator returned the first `sorted()` name-prefix match, and
  `CHANGELOG-archive.md` sorts *before* `CHANGELOG.md` (`-` is 0x2D, `.` is 0x2E), so freshness was
  measured against a deliberately frozen file. Reproduced end to end — a fixture whose ledger was
  committed **at HEAD** was reported **13 commits behind**. (3) **Signal F was unreachable**: the
  unmigrated-`BACKLOG.md`-done-marks advisory was emitted *below* the `changelog is None` early
  return, so an adopter with 60 unmigrated done-marks and no ledger at all — strictly the worse
  case — went **silent**, while one with a ledger was warned.
- **How — per ratified D3, a dual predicate rather than a narrowed one.** The plan is explicit that
  the obvious fix is wrong: pointing the single locator at the root would satisfy the membership
  test while silently costing a documentation point for exactly the repo class the defect is about,
  because `is_fresh` is computed *after* the early return. So the two questions became two
  functions. `_find_changelog` still answers **location** — best-available, root or `docs/`,
  case-insensitive prefix — and still feeds `present`, `is_fresh` and Signals B–D. A new
  `_find_action_ledger` answers **membership** — the root `CHANGELOG.md`, the same probe
  `collect_methodology_metrics` already uses for the compliance checklist — and its
  `ledger_present` result is consumed at exactly **one** site, the `assess_risks` ledger risk.
  `collect_doc_metrics.has_changelog` is untouched; it answers a third question (doc hygiene).
  Shadowing is fixed by preferring an exact `CHANGELOG.md` ahead of prefix matches, with the prefix
  search retained as the fallback so a repo whose only changelog is `CHANGELOG.rst` is still
  measured. Signal F moves above the early return, keeping its adopter scope and its
  grace-independence. Every advisory now **names the file it was computed against** and no longer
  calls that file "the ledger" — `docs/changelog.md: 12 commits since it was last updated`.
- **One judgment call, recorded rather than buried.** The exact-name preference is scoped **within
  a base**, preserving the pre-existing root-over-docs precedence exactly. Hoisting it across bases
  would additionally fix a root archive that shadows an exact `docs/CHANGELOG.md` — but the same
  hoist would silently move which file is measured, and with it the ±1 freshness point, for the
  neighbouring shape where a non-`.md` root changelog (`CHANGELOG.rst`) coexists with an exact
  `docs/CHANGELOG.md` and nothing is being shadowed at all — which no defect here asks for, and
  which is the very failure mode D3 exists to prevent. A boundary reviewer argued the wider reading is within
  the plan's literal text ("preferring an exact `CHANGELOG.md` over **any** name-prefix match") and
  a second reviewer argued the opposite; the plan's own defect-7 evidence is a **same-base** pair,
  so the conservative reading shipped. **Residual, stated plainly:** a root holding *only* an
  archive still shadows an exact `docs/CHANGELOG.md`. It is pinned by a characterization test that
  names it a limitation, so revisiting it is a decision, not a discovery.
- **Adopter-visible effect: exactly one new advisory, and no score moves.** A methodology adopter
  with real history and no root `CHANGELOG.md` now raises *"Methodology adopter has commit history
  but no root CHANGELOG.md action ledger"* — the finding #60 is about. Re-scanned read-only against
  five real sibling repos: every one keeps a root ledger, so **none** newly fires. The repo class
  that does fire keeps its `+1` documentation freshness point — the regression the obvious fix
  would have caused.
- **Verified — RED-first, then mutation-tested.** 18 new assertions were driven against
  **unpatched** code and watched to fail (9 `AttributeError` for the absent locator, 9 wrong-answer
  failures) before the scanner was touched. Because the previous layer proved RED-first is
  *necessary but not sufficient*, every assertion was then **mutation-tested**: 22 mutants were
  applied to both twins and re-run. The first pass killed 15 of 17 and exposed a real hole — Signal
  F could be grace-suppressed unnoticed, since every fixture drove real history. Two survivors are
  survivors *by construction* and are recorded as such: `str()` vs `.as_posix()` is unkillable on a
  POSIX filesystem (proven — the two are byte-identical there, differing only on Windows), and
  moving the `ledger_present` assignment below the early return is logically inert, because "no
  changelog located" now implies "no root ledger" except when `iterdir()` itself fails. A
  self-inflicted trap worth recording: an unconditionally-failing new test made the harness report
  *false* kills, so a mutation run is only meaningful from a green baseline.
- **Hardened at the layer boundary by a 4-lens adversarial review before the commit landed** — 8
  raw findings, each reproduced by this session before acting, with every refuter defaulting to
  *refute*. The **adversarial regression lens came back clean**: no input was found on which the
  new code behaves worse than the old. Three were **coverage holes that RED-first and the first
  mutation pass had both missed** — the prefix-fallback lock's fixture had no `docs/` directory, so
  the second base was never iterated and a per-base reset of the fallback survived the whole suite
  while losing a root `CHANGELOG.rst` outright; the membership risk's history gate had no test on
  either side (deleting it *and* an off-by-one both survived); and the "nothing is stranded below
  the early return" test asserted a literal signal name rather than the structural invariant its
  own docstring claimed. All three are closed and the mutants that exposed them now die.
- **Three findings landed on my own prose, and all three were upheld** — in a change whose entire
  subject is signal integrity, a comment that overstates is the same defect class as a signal that
  overstates. (1) The `_find_action_ledger` docstring called itself "deliberately identical" to the
  compliance checklist probe; false — the checklist uses a bare `exists()`, so a `CHANGELOG.md`
  *directory* scores as present for compliance while it is correctly not a ledger. Corrected, and
  the single divergence is now pinned by its own test. (2) A comment claimed the risk was "the ONE
  site that asks about membership"; also false — `collect_methodology_metrics` asks the same
  question and scores it, which is the *point* of aligning them, not a duplication. (3) A test
  docstring claimed that losing the located changelog costs "documentation presence **and**
  freshness"; it costs only freshness, because presence comes from
  `collect_doc_metrics.has_changelog`, an independent scan D3 deliberately leaves untouched —
  I had reproduced, in my own explanatory prose, the exact location-for-membership conflation this
  layer exists to fix. One further docstring went stale *because of* the narrowing decision above
  and was rewritten to describe what it now guards rather than the mechanism it was born against.
- **Two findings were refuted as pre-existing, and coverage was added anyway.** The history gate
  and the `is_file()`/`exists()` split are both byte-unchanged at HEAD, so neither is a defect this
  change introduces — but this layer rewrote the condition they live in, and an untested guard on a
  line you just edited is a hole regardless of who dug it.
- **Suite:** `tools/test_methodology_dashboard.py` **47 → 79** tests; `bin/tests.sh` **84/84**;
  `python3 bin/check-links` OK (82 links / 21 files); twins byte-identical. Runtime smoke ran the
  **real** render path (`collect_all` → `render_project_card` → `render_methodology_grid` →
  `render_html` → `append_history`) over five real sibling repos and three synthetic defect
  fixtures, writing nothing into any scanned repo; the string `CHANGELOG ledger lag` no longer
  appears anywhere in rendered output, and each history entry carries `dashboard_version 2.9.1`.
- **Note for the next layer:** `changelog["present"]` now has **no consumer inside the scanner** —
  its single reader moved to `ledger_present`. It remains in the emitted metrics (JSON, history)
  and in tests, so it is informational rather than dead, but it is no longer load-bearing.

### 2026-07-25 · [issue #61] Dashboard signal-integrity **Layer 1** — scale honesty + checklist currency (`DASHBOARD_VERSION` 2.8.0 → 2.9.0)
- **Change:** the first implementation layer of the ratified campaign plan
  `docs/planning/dashboard-signal-integrity-plan.md` (S9, `bc2481d`). Closes
  [#61](https://github.com/KJ5HST/methodology/issues/61) — `METHODOLOGY_ITEMS` weights summed
  **110** while `compliance_score` was rendered as a percentage, and the methodology health
  dimension was the only one of five with **no clamp**, so a fully-compliant adopter scored
  **22/20** on a 0–20 dimension and **102/100** overall. Also fixes two defects found while
  planning and never filed: **`HANDOFFS.md`** has shipped to adopters as a SEED since v3.3
  (`bin/_manifest.py:47`) but was never a compliance checklist item, and the grid's header row
  was hand-written at **8** columns while its cells derive from `METHODOLOGY_ITEMS` — so since
  v2.1 every project row has rendered **two cells wider than its headers** (8 `<th>` over 10
  `<td>`, reproduced; the plan predicted this as a *future* trap of adding a 9th item, but it
  was already live).
- **How:** per ratified **D1** the denominator is **derived, never a literal**
  (`METHODOLOGY_MAX = sum(...)`, now 115) and normalization happens **once, producer-side**
  (`compliance_pct`); all four consumers — the health dimension (now `min(20, …)`), the risk
  thresholds, the portfolio grid's colour ladder, and the project card — read that percentage,
  while the `== 0` *"no adoption at all"* test deliberately keeps reading the **raw** sum, which
  is scale-independent. The card renders `"{pct}% ({raw} of {MAX})"` so the weighted sum stays
  inspectable. Per **D2** `HANDOFFS.md` joins the checklist weighted **5**, matching its
  structural twin `CHANGELOG.md`. The grid header row is now derived from the checklist. Two
  supporting changes: the three duplicate `exists()` loops in `collect_methodology_metrics`
  collapse to one probe per item, and every `dashboard_history.jsonl` entry is stamped with
  `dashboard_version`, so the one-time re-scaling is *recoverable from the history data* rather
  than reading as an unexplained red regression arrow (plan residual risk 1). Stated precisely:
  the stamp is written but not yet read — `render_trend_section` remains version-unaware, so the
  discontinuity is now diagnosable, not annotated.
- **A second adopter-visible effect, beyond D1's stated ~9% deflation:** because the
  partial-adoption risk threshold is stated in percent, it now reads the percentage — so the two
  reachable checklist sums between the old and new boundary (raw **50** → 43% and **55** → 48%)
  newly raise a medium *"Partial methodology adoption"* row. Those repos genuinely are below
  half; nothing about them changed, only the honesty of the comparison.
- **Verified — RED-first, per the campaign's standing rule:** 13 new assertions were driven
  against **unpatched** code and watched to fail (methodology **22** not 20, total **102**, card
  **"110%"**, 8 headers over 10 cells, `HANDOFFS.md` the *only* unaccounted manifest
  destination) before the scanner was touched — the suite was green against every one of these
  defects beforehand, so "tests pass" was not evidence. A new **manifest-vs-checklist structural
  guard** converts the `HANDOFFS.md` omission into an invariant: every adopter-root destination
  in `bin/_manifest.py` must be a checklist item or carry a stated exemption, so the next
  distributed artifact cannot repeat it. `tools/test_methodology_dashboard.py` **29 → 47** tests;
  `bin/tests.sh` **84/84**; `python3 bin/check-links` OK (82 links / 21 files); twins
  byte-identical. Live effect, re-scanned read-only: the adopter whose card read *"Methodology
  Compliance (110%)"* now reads *"100% (115 of 115)"* with methodology **20/20** and a total of
  **88** (was 90/100 — the accepted one-time deflation).
- **Hardened at the layer boundary by a 5-lens adversarial review before the commit landed:** 23
  raw findings → **2 confirmed**, 19 refuted (chiefly as Layer 5 doc targets the plan already
  owns, or pre-existing conditions this layer neither introduced nor was chartered to fix). The
  confirmed one was a **mutation-proven coverage hole**: the suite pinned the *clamp* but not the
  *normalized read*, so an implementation that clamps while still reading the raw sum passed all
  44 tests — verified first-hand by mutating both twins, and now killed by an intermediate-value
  lock (the endpoints 0% and 100% cannot distinguish the two readings; the whole adopter fleet
  lives between them). Also added: an end-to-end pre-v3.3 adopter fixture, so D2's accepted cost
  has a test; a direct out-of-range clamp test; exact pinning of the derived grid labels; and
  removal of two assertions that would have broken against correct code if the checklist were
  ever re-cut to sum 100. Two review claims about this session's own prose were upheld and
  fixed — the `compliance_pct` docstring's "no value is rounded twice" was **false** (the
  dimension re-scales the rounded percentage, credited one extra point at raw 40 and 80 — kept
  deliberately, now documented), and this entry's trend claim overstated a write-only stamp.
- **Commit/PR:** `6b10f09` — both scanner twins, the tests and this entry; its immediate
  successor reconciles the `HANDOFFS.md` receipt and this line to that sha, so no `pending`
  marker is left for the next session's Phase 0 to repair. **Layer 1 of 6 — Layers 2–6 remain
  separate sessions** (ledger
  identity, backlog-shape predicate, repo role, completeness sweep, release decision). Upstream
  #61 stays **open** until this reaches upstream; the release decision (plan R1) is deferred to
  merge by operator decision.
- **Session:** S10

### 2026-07-25 · [ad hoc] Ratified plan — dashboard signal-integrity campaign (upstream #59/#60/#61 + 5 unfiled defects)
- **Change:** authored and committed `docs/planning/dashboard-signal-integrity-plan.md`, a ratified
  six-layer campaign plan (one layer per session) closing the three filed dashboard issues
  ([#59](https://github.com/KJ5HST/methodology/issues/59),
  [#60](https://github.com/KJ5HST/methodology/issues/60),
  [#61](https://github.com/KJ5HST/methodology/issues/61)) **plus five defects found while planning and
  not yet filed**: (a) `HANDOFFS.md` ships to adopters as a SEED since v3.3 (`bin/_manifest.py:47`) but was
  never added to `METHODOLOGY_ITEMS`; (b) **Signal F is unreachable** when no changelog exists —
  `evaluate_changelog_freshness` early-returns at `:698-701`, *before* the emission at `:772`, so an adopter
  with unmigrated done-marks **and no ledger** gets fewer warnings than one with a ledger; (c) **archive
  shadowing** — `_find_changelog`'s `sorted()` returns `CHANGELOG-archive.md` over `CHANGELOG.md`;
  (d) a `- [x]` inside a fenced ` ```markdown ` block counts as real completed work; (e) `README.md:75`
  and `:79` omit `HANDOFFS.md` from the seeded-files enumeration. All eight reproduced first-hand
  (`importlib` + `collect_all`, read-only). Operator ratified **D1** normalize to a true 0–100 percentage
  with a *derived* denominator — decided by git history, since v2.0 (`46b17e8`) summed to exactly 100 and
  v2.1 (`274dcd4`) appended two 5-point items without re-cutting; **D2** `HANDOFFS.md` joins the checklist
  weighted 5; **D3** plan now, implement next (FM #18 — the plan↔implementation boundary is never
  collapsible into a slice); **D4** release decision deferred to merge. Design was pressure-tested by an
  11-agent panel (4 code maps → 3 competing designs → 3 judge lenses → synthesis) which **refuted this
  session's own #59 design** (remapping the checklist onto `starter-kit/` paths would credit a 27-line
  empty stub — the defect inverted) and caught a silent `+1` documentation regression hiding inside the
  obvious #60b fix; two of the panel's own claims were rejected after re-execution.
- **Commit/PR:** this commit. **No scanner code changed** — the plan is the deliverable; implementation
  starts next session at Layer 1.
- **Session:** S9 · **Verified:** `bin/tests.sh` 84/84, `tools/test_methodology_dashboard.py` 29 OK,
  `python3 bin/check-links` OK (82 links / 21 files); every cited `file:line` re-read before commit.
  Also reconciled S8's receipt `commit: pending` → `4e2901f`.

### 2026-07-13 · [ad hoc] Opened upstream issues #60 and #61 — dashboard false-GREEN on a drifted adopter
- **Change:** audited the `mts-system` adopter (operator question: "BACKLOG.md is large because of
  completed items; it should be on v3.5, which would not allow the backlog to grow"). The premise was
  false — that adopter runs a hand-patched **v2.0-era** runner (FM table stops at #19; zero occurrences of
  "CHANGELOG"), so the FM #27 eviction rule was never installed. The audit surfaced three **framework**
  defects, filed upstream: [#60](https://github.com/KJ5HST/methodology/issues/60) — (a) Signal F's
  `_BACKLOG_DONE_RE` (`tools/methodology_dashboard.py:131`) matches only `- [x]` checkboxes, so a
  table-status backlog with 253 DONE rows counts **0**; (b) `_find_changelog` (`:644-657`) searches `docs/`,
  so a stale *product* `docs/changelog.md` masks the missing action ledger and **suppresses** the
  "adopter has no CHANGELOG ledger" risk at `:1409` — the operator is instead told to update the wrong file.
  [#61](https://github.com/KJ5HST/methodology/issues/61) — `METHODOLOGY_ITEMS` weights sum to **110** and the
  methodology health dimension is the only one with no `min(20, …)` clamp (`:1329`), so the card renders
  "Methodology Compliance (**105%**)" and a 21-of-20 sub-score. Net effect on a real adopter: **88/100 health,
  zero backlog risks** — a green bill of health on a repo 12 releases behind with no ledger. Sibling class to
  [#59](https://github.com/KJ5HST/methodology/issues/59), but sharper: #59 is a false *risk* on the canonical
  repo; these are a false *green* on an adopter. Existing tests do not catch #61 —
  `tools/test_methodology_dashboard.py:210-219` asserts the bound but drives `compliance_score: 0`, never
  exercising the unclamped path.
- **Commit/PR:** this commit (fork `main` ledger record; the issues live upstream). No dashboard code changed
  this session — the fixes are unclaimed.
- **Session:** S8 · **Verified:** reproductions executed read-only against the adopter via `importlib`
  (no files written to either repo); `bin/status` drift table reproduced first-hand.

### 2026-07-13 · [ad hoc] Adopter coordination — ratified methodology v3.5 migration plan for `mts-system`
- **Change:** authored and committed a six-phase, session-sized migration plan to the adopter repo
  (`mts-system` `fbc35cd`, `docs/planning/methodology-v35-migration.md`) taking it from the hand-patched
  v2.0-era corpus to canonical v3.5 and performing the three-file `BACKLOG`/`CHANGELOG`/`ROADMAP` split it
  never did (0/3, not 2/3 — its `ROADMAP.md` is not the seed). Operator ratified D1–D6 (full-corpus sync;
  full 3-source ledger backfill; narrative→CHANGELOG + inventory→ROADMAP; ROADMAP rewrite; keep
  `docs/changelog.md` with a disambiguating header; archive-then-reset `SESSION_NOTES.md`). Key finding for
  **this** repo's tooling: `bin/sync`'s drift gate is whole-corpus and pre-write, so three locally-modified
  tracked files cause it to exit 2 and write **nothing at all** — including seeds. "Sync will at least seed
  the ledger" is false, and no doc says so.
- **Commit/PR:** plan committed in the adopter repo (`fbc35cd`); no canonical file changed.
- **Session:** S8 · **Verified:** grep-based evidence inventory executed first-hand (keep list, section map,
  reference graph, the three sync-blocking diffs); plan then adversarially reviewed (4 lenses) before
  commit — 11 defects found and folded in, incl. a missed fourth regrowth site (`CLAUDE.md:148`) and an
  unfalsifiable verification step.

### 2026-07-09 · [ad hoc] Opened upstream issue #59 — dashboard self-scan blind spot
- **Change:** filed [KJ5HST/methodology#59](https://github.com/KJ5HST/methodology/issues/59) —
  `methodology_dashboard.py`'s methodology-compliance check (`METHODOLOGY_ITEMS`) looks for
  adopter-facing operating files at the scanned repo's own root, which is a category error when the
  scan target is this canonical repo (those files live under `starter-kit/` here as templates).
  Reproduced: `compliance_score: 5`, a misleading "Partial methodology adoption (5%)" medium-severity
  risk on the repo that authors the methodology. Also confirmed `detect_doc_only` is **not** affected
  by this — it correctly classifies this repo as code (5,567 source LOC, past the 200-LOC cap),
  disproving the "judged doc-only since it has no code" premise that prompted the check in the first
  place. No self-recognition logic exists in the file today; two candidate directions (a bidirectional
  marker following the `.methodology-profile` precedent, or a structural heuristic keyed on
  `starter-kit/` presence) are left for the next session to design.
- **Commit/PR:** this commit (fork `main` ledger record; the issue itself lives upstream).
- **Session:** ad hoc · **Verified:** n/a — issue creation + read-only dashboard investigation.

### 2026-07-08 · [ad hoc] Released v3.5 — capability-tiered review
- **Change:** version bumped **v3.4 → v3.5** (`CLAUDE.md` "Current version" line + a new §Versioning
  entry; `README.md` What's New) covering the capability-tiered review elective addition (BL-7, PR #57,
  already merged). Cite-don't-restate: the full narrative lives in
  [`CLAUDE.md` §Versioning "v3.5"](CLAUDE.md#versioning).
- **Commit/PR:** this commit (release narration) → merged; annotated tag `v3.5` + GitHub Release.
- **Session:** release · **Verified:** `bin/tests.sh` 84/84; `bin/check-links` clean.

### 2026-07-08 · [BL-7] Fork close-out — capability-tiered review merged, fork synced, backlog retired
- **Change:** PR #57 merged to `KJ5HST/main` (`d563600`); no version-bump commit was included in the
  merge, so the version-event decision (dot release vs. `CLAUDE.md`-only) remains open — deferred to
  the operator per the established defer-to-merge pattern. Fork `main` merged `upstream/main` —
  resolved a `CHANGELOG.md` union conflict (this session's `[ad hoc]` entry landed above the prior
  session's `v3.4 close-out` entry, by wall-clock order) and a `HANDOFFS.md` union conflict: this
  session's receipt was originally committed as `session: S2` on the feature branch (the only
  predecessor visible there was `S1`, by the branch-from-upstream convention that keeps fork-only
  content out of the PR diff), which collided with the fork's own already-established `S2` (v3.3
  release). Renumbered to **S6** — the next number in the fork's real sequence — without touching or
  renumbering S1–S5; the receipt's `predecessor_score` evaluation of S1 was left exactly as originally
  written (accurate to what the session actually did), not retroactively rescored against S5. `BL-7`
  marked complete and removed from `docs/planning/BACKLOG.md`'s Open items (backlog retired again, all
  of BL-1–BL-7 complete).
- **Commit/PR:** this commit (fork `main` close-out).
- **Session:** capability-tiered review (fork close-out) · **Verified:** `bin/check-handoff` OK on the
  renumbered S6 receipt; `bin/tests.sh` 84/84; `bin/check-links` clean; fork `main` 0 commits behind
  `upstream/main`.

### 2026-07-08 · [ad hoc] Capability-tiered review — elective vertical-slice addition (BL-7)
- **Change:** codifies the operator-observed pattern from the close-out-receipt slice's hybrid model
  split (session S1) as an elective addition to `starter-kit/SESSION_RUNNER.md` §Vertical Slice
  Sessions: **capability-tiered review** — a pre-declared slice's layers may be delegated to a
  lighter/faster capability tier only where an objective gate (test suite, exhaustive grep, mechanical
  spec) proves correctness, with the strongest tier reviewing every delegated layer's output before
  that layer's checkpoint commit lands; explicitly additional evidence for gates (c)/(d), never a
  substitute, and explicitly not a fifth gate — forecloses two FM #26 misreadings (treating review as
  proof on its own, batching review to the end instead of per boundary). Four files: **`starter-kit/SESSION_RUNNER.md`**
  the core paragraph + new **Learning #11**; **`ITERATIVE_METHODOLOGY.md`** a one-sentence routing
  pointer in §Matching Reasoning Effort to Stakes; **`starter-kit/RECOMMENDED_SKILLS.md`** an
  illustrative Claude-Code-specific addendum after §Reasoning Effort (brand names confined to this file
  only); **`docs/tutorials/T5_cautionary.md`** a corollary citing this repo's own close-out-receipt
  slice as the worked "doing it right" counter-example to FM #26. Preceded by an operator-approved
  3-candidate design panel (placement, naming, scope, and all three optional extras decided by the
  operator). **No new phase, gate, principle, workstream, or failure mode; failure-mode count stays 27.**
  All four touched files are `bin/_manifest.py`-distributed except the tutorial (canonical-only), so
  adopters receive the core/recommendation discipline via `bin/sync`.
- **Design verification:** drafted, then adversarially checked by a 4-lens review (guardrail fidelity,
  citation/numbering fact-check, voice & agent-independence, completeness-critic whole-corpus sweep) —
  all four lenses independently confirmed the same real defect (brand names "Sonnet-5/Opus-4.8" leaking
  into the new Learning #11's Source column in the brand-neutral core file) — fixed before commit; no
  other findings across links, anchors, FM/gate byte-stability, or corpus-wide staleness checks.
- **Commit/PR:** this commit — branch `feat/capability-tiered-review` (from `upstream/main`).
- **Session:** capability-tiered review (BL-7 design + implementation) · **Verified:** `bin/tests.sh`
  84/84; `bin/check-links` clean.

### 2026-07-08 · [ad hoc] v3.4 close-out — fork main synced, branch pruned, S5 receipt written
- **Change:** PR #56 merged to `KJ5HST/main` (`4a6c1d2`, auto-closed issue #55); annotated tag `v3.4` +
  GitHub Release (Latest) pushed to both `upstream` and `origin`. Fork `main` merged `upstream/main`
  (`d139642`) — resolved a `CHANGELOG.md` union conflict (both sides had added dated entries
  independently) by wall-clock authorship order rather than a naive union or "ours" pick, and fixed a
  stale "(just above)" positional cross-reference the reorder broke. Fork main pushed; the feature
  branch `feat/completeness-critic-review-lens` pruned on `origin` and locally. This session's
  `HANDOFFS.md` receipt (**S5**) written at close-out rather than deferred to the next Orient's
  reconcile.
- **Commit/PR:** this commit (fork `main` close-out).
- **Session:** completeness-critic lens (close-out) · **Verified:** `bin/check-handoff` OK on the S5
  receipt; `bin/tests.sh` 84/84; `bin/check-links` clean; fork `main` 0 commits behind `upstream/main`.

### 2026-07-08 · [ad hoc] Released v3.4 — completeness-critic review lens
- **Change:** version bumped **v3.3 → v3.4** (`CLAUDE.md` "Current version" line + a new §Versioning
  entry; `README.md` What's New) covering the completeness-critic lens (issue #55). Cite-don't-restate:
  the full narrative lives in [`CLAUDE.md` §Versioning "v3.4"](CLAUDE.md#versioning).
- **Commit/PR:** this commit (release narration) → merged; annotated tag `v3.4` + GitHub Release.
- **Session:** release · **Verified:** `bin/tests.sh` 84/84; `bin/check-links` clean.

### 2026-07-08 · [issue #55] Completeness-critic review lens — new Learning #10 + AUDIT_WORKSTREAM guidance
- **Change:** promotes **Learning #7** (cross-reference completeness at self-review) and **Learning #8**
  (close-out-gate checklist propagation) from authoring-time self-checks to an explicit **review-time
  lens**: when a change adds, renames, or removes a concept, artifact, file, step, or numbered-set
  member, a review/audit pass now owes a whole-corpus sweep (not just the diff) for enumerations,
  worked examples, indexes, and count-claims that now lag. Three files: **`SESSION_RUNNER.md`** new
  **Learning #10** (table was 1-9); **`AUDIT_WORKSTREAM.md`** new anti-pattern **#9** "Diff-scoped blind
  spot" (list was 1-8), a new Verification Checklist bullet, and a note that `/code-review`/`/review`/
  `/security-review` are diff-scoped by design so the sweep stays methodology-owned; **`ITERATIVE_METHODOLOGY.md`**
  one sentence added to §Review/Audit Sessions citing the new Learning + the operative checklist step.
  Motivated by the v3.3 doc-completeness gap (PR #54) that a clean 6-lens adversarial review missed —
  [KJ5HST/methodology#55](https://github.com/KJ5HST/methodology/issues/55). **No new phase, gate,
  principle, or workstream; failure-mode count stays 27.** All three touched files are
  `bin/_manifest.py`-distributed, so adopters receive this via `bin/sync`.
- **Design verification:** drafted, then adversarially checked by a 4-lens review (acceptance-criteria
  coverage, numbering/citation fact-check, a reflexive Learning-#7 self-check for other stale
  cross-references, and placement/precedent judgment) — 2 of 4 lenses clean, 2 raised real findings
  (a mis-anchored insertion point in `AUDIT_WORKSTREAM.md`'s Recommended Skills section; a citation
  missing the `starter-kit/` path prefix used elsewhere in the repo) — both fixed before commit.
- **Commit/PR:** this commit — branch `feat/completeness-critic-review-lens` (from `upstream/main`).
- **Session:** completeness-critic lens · **Verified:** `bin/tests.sh` 84/84; `bin/check-links` clean.

### 2026-07-08 · [ad hoc] Backfilled (reconcile-on-read): HANDOFFS.md was 3 sessions behind
- **Change:** Phase 0 orientation found `HANDOFFS.md`'s frontier (`4b0b1bc`, the S1 receipt) was 3
  sessions stale — the v3.3 release, the doc-completeness follow-up, and the issue #55 filing had all
  landed commits with no receipt written. Reconstructed `status: reconciled` blocks for **S2** (release,
  `dd2c84b`/`4ec1f47`), **S3** (doc-completeness, `67581fd`/`768631e`), and **S4** (issue #55,
  `6591faa`) from `git log` and each session's own CHANGELOG entry, per `SESSION_RUNNER.md` Phase 0
  step 6's "also reconcile `HANDOFFS.md`" mechanic — this ledger (`CHANGELOG.md`) itself needed no
  backfill (its frontier was already current). Also corrected S1's `commit: pending` to the real merge
  sha (`e5638af`) now that PR #52 has landed, per `HANDOFFS.md`'s own documented reconcile note ("the
  next session reconciles them to real shas"). First real exercise of the reconcile mechanic P4 built —
  and a live instance of the completeness-critic gap issue #55 (see the release/lens entries above,
  and the issue-filing entry below) names.
- **Commit/PR:** this commit (fork `main`; `HANDOFFS.md` backfill, one write Phase 0 permits).
- **Session:** Phase 0 reconcile · **Verified:** `bin/check-handoff` OK on the newest receipt;
  `bin/tests.sh` 84/84; `bin/check-links` clean.

### 2026-07-08 · [ad hoc] Opened upstream issue #55 — completeness-critic review pass
- **Change:** filed [KJ5HST/methodology#55](https://github.com/KJ5HST/methodology/issues/55) proposing a
  **completeness-critic** review lens — reviews should sweep the *whole corpus* (not just the diff) for
  enumerations / worked examples / indexes / count-claims a change made stale, promoting Learning #7/#8
  from an authoring self-check to a review lens. Motivated by the v3.3 out-of-diff doc lag (caught by the
  operator, fixed in #54) that a clean 6-lens adversarial review missed.
- **Commit/PR:** this commit (fork `main` ledger record; the issue itself lives upstream).
- **Session:** ad hoc · **Verified:** n/a — issue creation.

### 2026-07-08 · [ad hoc] v3.3 doc-completeness — propagate the receipt into HOW_TO_USE, README tree, tutorials
- **Change:** the v3.3 close-out receipt is now reflected in the *secondary* docs that describe or
  demonstrate close-out, closing the Learning #7 propagation gap the release surfaced (the operator
  asked "has documentation been fully updated?" — it had not). **`HOW_TO_USE.md`** §Phase 3 3D now names
  the durable `HANDOFFS.md` receipt (it is DISTRIBUTED — was inconsistent with the synced
  `SESSION_RUNNER.md`); **`README.md`** Repository-Structure tree lists `HANDOFFS.md` (starter-kit) +
  `check-handoff` (bin/); the **tutorials** `T2_worked_transcript.md` (a full ` ```handoff ` receipt in
  its Phase-3 close-out + the receipt joins the `git add`), `T2_first_session.md` (1B receipt stub + the
  3D/expected-result), and `T3_compounding_loop.md` (the receipt carries `predecessor_score`, making the
  compounding loop machine-checkable). Mirrors the v3.1→BL-6 downstream-completeness pattern; **no version
  event** (docs-lag). No principle/phase/gate/workstream/FM change.
- **Commit/PR:** `67581fd` (distributed: `HOW_TO_USE.md` + `README.md`) · this commit (tutorials:
  `T2_worked_transcript.md`, `T2_first_session.md`, `T3_compounding_loop.md`) — branch
  `docs/v3.3-doc-completeness` (from `upstream/main`).
- **Session:** doc-completeness follow-on · **Verified:** `bin/check-links` clean; a completeness sweep
  found no other tutorial demonstrating close-out without the receipt (T5 only references a prior handoff).

### 2026-07-08 · [ad hoc] Released v3.3 — durable close-out receipt
- **Change:** version bumped **v3.2 → v3.3** (`CLAUDE.md` "Current version" line + a new §Versioning
  entry; `README.md` What's New) and shipped as an **annotated tag `v3.3` + GitHub Release (Latest)**,
  covering the close-out-receipt slice (PR #52, merge `e5638af`). Cite-don't-restate: the full narrative
  lives in [`CLAUDE.md` §Versioning "v3.3"](CLAUDE.md#versioning).
- **Commit/PR:** this commit (release narration) → merged; annotated tag `v3.3` + GitHub Release.
- **Session:** release · **Verified:** post-merge `bin/tests.sh` green — Test 9's github-source 404
  clears now that `HANDOFFS.md` is on the default branch.

### 2026-07-08 · [ad hoc] Close-out receipt — durable machine-checkable handoff artifact (shipped in v3.3, PR #52)
- **Change:** implemented the ratified plan (fork `main`:
  `docs/planning/close-out-receipt-durable-artifact-plan.md`) as a pre-declared **vertical slice** —
  one capability, checkpoint commit + verification at each layer boundary. Fixes "agent had to be
  prompted for the close-out report." **P1:** new `starter-kit/HANDOFFS.md` SEED — a
  per-session `handoff`-block receipt ledger (twin of this action ledger) — added to `bin/_manifest.py`
  `DISTRIBUTION` (SEED) + `SEED_FORMAT_MARKERS` (`"Handoff Receipts"`); `sync` seeds it, `status`
  reports `present` / `present (stale format)`, `sync` never clobbers it. **P2:** `bin/check-handoff`
  (canonical-only, python3 stdlib) + `bin/tests.sh` Tests 21–22 — asserts a receipt's presence +
  structural completeness (fence-isolated block, integer scores, `path:line` in `key_files`, sha-or-
  `pending` in `what_was_done`) plus anti-pattern lints (rejects "pick next from backlog", "need to
  verify", bare placeholders), never semantic quality. **P3a:** protocol wiring — `SESSION_RUNNER.md`
  (1B receipt stub, 3D "write the six as a durable receipt", Planning checklist, slice-revert) +
  `ITERATIVE_METHODOLOGY.md` (Phase 1B, Phase 6 step 7, the Review/Planning/Debugging session types).
  **P3b:** the receipt item added to all three campaign checklists (per-session + consolidation) —
  Learning #8 fully discharged. **P4:** Phase 0 reconcile-on-read extended to backstop the receipt — a
  missing or still-`pending` receipt for a session that left commits is reconstructed `status:
  reconciled` at the next Orient, folded into the one write Phase 0 already permits (`SESSION_RUNNER.md`
  step 6 + mechanics note, `ITERATIVE_METHODOLOGY.md` Pre-Flight). **P5:** framing — strengthened
  **FM #6** to name the durable receipt (count stays 27, no new FM), a degradation-detection row
  (commits landed but receipt never completed → FM #6), **Learning #9** (a handoff is dependable only
  as a durable machine-checkable artifact: gate-on-write AND reconcile-on-read), and the
  SAFEGUARDS/BOOTSTRAP harness stop-hook **recommendation** (agent-specific, soft-remind, never shipped;
  `bin/check-handoff` noted canonical-only/copyable). **P6:** dogfood close-out — the canonical repo's
  own root `HANDOFFS.md` receives its first receipt (S1) for this very slice, and `bin/check-handoff`
  validates it green (first non-fixture run). Merged to `KJ5HST/main` as **PR #52** (merge `e5638af`);
  the version event (D4) resolved to a **v3.3** minor — see the release entry above.
- **Commit/PR:** `4f0bea7` (P1: artifact + manifest) · `1646773` (P2: checker + tests, built by
  Sonnet 5; Opus review accepted `status: reconciled` for P4's backfill and made the `HANDOFFS.md`
  template checker-safe — no inline `#` comments, since `#` is a literal value char as in `PR #52`) ·
  `f722a84` (P3a: SESSION_RUNNER + IM protocol wiring, Opus) · `afbbe7d` (P3b: 3 campaign
  checklists, Opus) · `5f13c99` (P4: Phase 0 receipt reconcile, built by Sonnet 5; Opus review
  verified the false-positive scoping — one receipt per session, not per commit — and documented the
  `reconciled` status in the seed) · `719a41d` (P5: framing — FM #6 + degradation row + Learning #9 +
  stop-hook recommendation, Opus) · this commit (P6: dogfood root receipt + final verification, Opus —
  P6's deliverable is the session's own handoff, so authored, not delegated) — branch
  `feat/close-out-receipt` (from `upstream/main`); model
  split hybrid — **P2 + P4 Sonnet 5; P1/P3/P5/P6 Opus 4.8**, Opus reviewing every Sonnet phase (P6
  moved to Opus because its deliverable is the session's own close-out handoff, not a delegable task).
- **Final review & fixes:** a 6-lens adversarial review (`wf_91880f5f-35c`, default-to-refute verify) —
  **12 raised → 7 confirmed → all fixed** across 3 checkpoint commits. **Fix A (checker, this commit):**
  `key_files`'s `path:line` regex now requires a **path-like** pre-colon token (`/` or `.`), so an
  incidental colon-digit in prose (`John 3:16`, `10:30`, `3:1`) no longer passes (C1); `what_was_done`'s
  sha-shape now requires a **hex letter**, so a bare 7+ digit decimal/timestamp no longer counts as a sha
  (C2); + a docstring caveat that an unwrapped example fence shadows the real receipt (C7). Regression
  tests added (**81 → 83**). **Fix B (synced docs):** the mandatory-procedure references to
  `bin/check-handoff` in `SESSION_RUNNER.md` §3D, `ITERATIVE_METHODOLOGY.md` Phase 6, and the
  `HANDOFFS.md` seed now carry the "canonical-only — copy it in; the dependable backstop is Phase 0
  reconcile" caveat the optional-hook subsections already had (C4/C5), and the receipt-to-requirements
  wording no longer double-counts `self_score` (C6: "the six requirements, the sixth being `self_score`,
  plus `predecessor_score`"). **Fix C (this commit):** `HANDOFFS.md` added to BOOTSTRAP's seed
  enumerations (repo tree, root-files table, both "seeded"/"seeded-once" sentences) — deliberately NOT
  the named three-file `BACKLOG`/`CHANGELOG`/`ROADMAP` task-tracking split (HANDOFFS is a close-out
  record, not part of that concept; "three" stays accurate); the campaign per-session checklists drop
  the bare `bin/check-handoff` mention (its caveated form stays in §3D). **All 7 confirmed findings fixed**
  (`28cecc8` A · `ac97722` B · this commit C). 5 findings were refuted (e.g. the missing `--range`
  mode — plan-optional; the last-wins duplicate-key parse — benign).
- **Session:** close-out-receipt slice · **Verified:** `bin/tests.sh` **83/84** (the 1 = github-source
  404 on the not-yet-pushed `HANDOFFS.md`, clears on merge); `bin/check-links` clean; block-isolation +
  per-field-defect + C1/C2-regression fixtures green; **`bin/check-handoff` green on the first real
  receipt** (root `HANDOFFS.md`, S1 — dogfood, first non-fixture run).

### 2026-07-08 · [ad hoc] Reopen backlog — BL-7 (consider: model-tiering as an elective feature)
- **Change:** `docs/planning/BACKLOG.md` reopened with **BL-7** (a *consider* item): whether matching
  model capability to task complexity — cheaper tier for spec-driven/test-graded work, strongest tier for
  high-blast-radius doc surgery + reviewing all cheaper-tier output — should become an **elective**
  methodology feature (recommendation layer; capability-tier framing for agent-independence; same risk
  lens as §Matching Reasoning Effort to Stakes). Surfaced by the operator while watching this repo's own
  close-out-receipt slice run on a hybrid Sonnet-5 / Opus-4.8 split. No phase/gate/FM change; planning-only.
- **Commit/PR:** this commit (fork `main`, `docs/planning/` is fork-only).
- **Session:** ad hoc grooming · **Verified:** n/a — backlog/docs only.

### 2026-07-08 · [ad hoc] Close-out receipt plan ratified — durable `HANDOFFS.md` artifact + reconcile, no CI
- **Change:** new fork-only ratified plan `docs/planning/close-out-receipt-durable-artifact-plan.md`.
  Fixes the failure "agent had to be prompted for the mandatory close-out report" by making the handoff a
  durable, machine-checkable `HANDOFFS.md` receipt (SEED twin of this action ledger, one `handoff` block
  per session) + a canonical-only `bin/check-handoff` + a Phase 0 reconcile backstop + strengthened
  **FM #6** (count stays 27) + a *recommended* (never shipped) harness stop-hook. Scope ratified as
  **durable-receipt-+-reconcile, NO server-side CI**; decisions D1–D5 settled. Design workflow
  `wf_4793d8f5-b5b` (6 readers → 5 lens proposals → synthesis + adversarial critique).
- **Commit/PR:** this commit (fork-only planning deliverable; implementation P1–P6 pending, to branch off `upstream/main`).
- **Session:** planning · **Verified:** n/a — docs-only (plan document).

### 2026-07-08 · [BL-6] BL-6 fully closed — item 2 shipped (PR #51), item 3 decided (hook canonical-only)
- **Change:** with the seed-format advisory merged (the `[ad hoc]` entry below / PR #51), the fork
  backlog's last item is complete and **removed from `docs/planning/BACKLOG.md` "Open items"** (moved to
  the Completed table). **Item 2** (seed-format migration discoverability) shipped in PR #51 — advisory,
  no version event. **Item 3** (hook distribution) is **decided: keep `.githooks/pre-commit`
  canonical-only** — adopters run the Phase 3F ledger gate via their root `SESSION_RUNNER.md`, so
  distributing the hook would add a per-clone `git config core.hooksPath` enable step + a maintenance
  surface for a mechanism they already have (the hook exists only because *this* repo has no root runner
  to run the gate on itself). The hook is **not** added to `bin/_manifest.py`. With BL-6 done, BL-1 –
  BL-6 are all complete and the fork backlog is retired again.
- **Commit/PR:** this commit (fork `main` — `BACKLOG.md` close-out + this ledger entry). Item-2 code
  shipped in [PR #51](https://github.com/KJ5HST/methodology/pull/51) (merge `48c253f`); fork-sync merge
  `9a84b8e`.
- **Session:** BL-6 close-out · **Verified:** `docs/planning/BACKLOG.md` "## Open items" now shows none;
  the BL-6 Completed-table row records item 3's decision + rationale; ledger source-tag census intact
  (`[issue #]` / `[BL-]` / `[ad hoc]` all present).

### 2026-07-08 · [ad hoc] bin/status flags stale-format adopter seeds (BL-6 item 2)
- **Change:** `bin/status` now surfaces a SEED file whose *format* predates the current methodology —
  advisory-only — as `present (stale format)`, with a one-line migration note beneath the table, so an
  adopter upgrading from a pre-v3.1 methodology can **discover** that its seeded `CHANGELOG.md` still
  carries the old (pre-action-ledger) shape instead of the lag being silent. Mechanism: a new generic
  `_manifest.SEED_FORMAT_MARKERS` dict (dest → marker), with `CHANGELOG.md` keyed on the ledger
  **title** `"Authoritative Action Ledger"` — a lifetime-stable token that append-only entries never
  remove — deliberately **not** the `METHODOLOGY-SEED-SENTINEL` (which the adopter deletes on its first
  real entry, so keying on it would mis-flag an *in-use* current-format ledger). `SESSION_NOTES.md` /
  `ROADMAP.md` are intentionally omitted (rewritten wholesale each session → no stable marker; add an
  entry only when a seed gains a lifetime-stable one). Detection is **advisory only**: `bin/sync` still
  never auto-overwrites an adopter-owned seed, the status string is never reclassified as drift, and the
  exit code is unchanged. Docs updated in lockstep: `starter-kit/BOOTSTRAP.md`'s update-existing-project
  note and the `docs/tutorials/T8_keeping_current.md` SEED-state model now name the third state.
- **Commit/PR:** `346ac01` (feature + Test 20: `bin/_manifest.py` + `bin/status` + `bin/tests.sh`) ·
  `fe3e10a` (docs: `starter-kit/BOOTSTRAP.md` note + `docs/tutorials/T8_keeping_current.md` third
  state) — branch `feat/status-stale-seed-advisory` (from `upstream/main`) → [PR #51](https://github.com/KJ5HST/methodology/pull/51),
  merge `48c253f`. Design + fixes hardened by a 6-lens adversarial review + default-to-refuted verify
  (`wf_52a1df0d-068`): **5 findings confirmed → all fixed** (an in-use-ledger test-coverage gap that let
  a sentinel-keyed regression pass, a vacuous disposition assertion masked by the note line, a
  multi-project note undercount, and a `T8` doc-code mismatch).
- **Session:** BL-6 item 2 · **Verified:** `bin/tests.sh` **68/68** (new **Test 20**, 14 assertions;
  54 → 68); manual stale / current / absent cases; the marker survives an in-use ledger (root
  `CHANGELOG.md` carries the title, no sentinel); a sentinel-keyed regression now makes Test 20 **fail**
  — proving constraint #2 (no false positive on a current-format seed) is locked in by a test.

### 2026-07-08 · [ad hoc] v3.2 shipped — PR #50 merged, tag + GitHub Release cut, fork synced
- **Change:** the BL-5 dashboard doc-only scoring change was designated **v3.2** (minor) and shipped.
  [PR #50](https://github.com/KJ5HST/methodology/pull/50) merged to `KJ5HST/main` (merge `9bda167`);
  the annotated tag `v3.2` was cut at that commit and its **GitHub Release published + marked Latest**;
  fork `main` synced via `git merge upstream/main` (fork-sync merge `df2cac9`, resolving one
  `CHANGELOG.md` union conflict, reconciled newest-on-top) and the tag mirrored to `origin`.
  `DASHBOARD_VERSION` is now 2.8.0; the failure-mode count stays 27.
- **Commit/PR:** [PR #50](https://github.com/KJ5HST/methodology/pull/50) → merge `9bda167`; fork-sync
  merge `df2cac9`; this commit (fork `main` — BL-5 backlog close-out + these ledger entries). Release:
  <https://github.com/KJ5HST/methodology/releases/tag/v3.2>. → full narrative:
  [`CLAUDE.md` §Versioning "v3.2"](CLAUDE.md#versioning).
- **Session:** BL-5 deploy · **Verified:** v3.2 GitHub Release is Latest (`releases/latest` = v3.2);
  distributed files byte-identical to `upstream/main` post-merge; fork `main` 0 behind upstream.

### 2026-07-08 · [BL-5] Dashboard doc-only scoring closed — removed from fork backlog
- **Change:** with v3.2 shipped, **BL-5** ("adapt dashboard scoring to document-only repositories",
  including the Signal-F adopter-gate + `starter-kit/__pycache__` polish notes) is complete and
  **removed from `docs/planning/BACKLOG.md` "Open items"** (moved to the Completed table). The fork
  backlog now has one open item — **BL-6 items 2–3** (seed-format migration affordance;
  hook-distribution decision).
- **Commit/PR:** this commit (fork `main`). The dashboard change itself shipped in
  [PR #50](https://github.com/KJ5HST/methodology/pull/50) / v3.2 (see the entry above and the branch entry below).
- **Session:** BL-5 close-out · **Verified:** BL-5 no longer under "## Open items"; ledger source-tag census intact (`[issue #]` / `[BL-]` / `[ad hoc]` all present).

### 2026-07-08 · [ad hoc] Dashboard: fair scoring for document-only / research repos (DASHBOARD_VERSION 2.8.0)
- **Change:** `methodology_dashboard.py` (both byte-identical twins, `tools/` + `starter-kit/`) now
  detects a **document-only / research** repo and reshapes scoring so it is no longer falsely
  penalized for having nothing to unit-test. Detection is marker-override → source-loc cap (200) →
  corpus-disjunction: an explicit bidirectional **`.methodology-profile`** marker (`doc-only` |
  `code`) wins; otherwise a repo with negligible source but a real doc corpus **or** a render
  toolchain (the latter catches pure-LaTeX/Quarto repos whose `.tex`/`.qmd` aren't counted as docs)
  is doc-only. When doc-only, the 2nd health slot (dict key `testing`, stable for JSON/portfolio)
  is filled by a new **Render/Verification** score — an *honest static proxy* (the scanner cannot
  execute a render; it scores render/verification *configuration*: toolchain configs, the v2.5
  `pdffonts`/`fc-list`/`kpsewhich` render-dependency check, docs-render/link-check CI, and
  Research-Documentation verification artifacts). The code-centric **No test infrastructure** /
  thin-coverage risks are suppressed for doc-only repos and replaced with render/verification
  advisories; the **Large files** risk is fixed (unconditionally) to fire only on a *source* file,
  so a 2500-line `.md`/`.tex` chapter no longer trips it; the doc-to-source ratio display shows
  `n/a (doc-only)` / Doc LOC instead of a misleading `0.000`. Two BL-5 polish items ride along:
  `.gitignore` now covers `starter-kit/__pycache__/`, and **Signal F** (unmigrated `- [x]` BACKLOG
  done-marks) is gated on methodology adoption so it can't fire on a non-adopter sibling. Adds
  `tools/test_methodology_dashboard.py` — the **first functional scoring tests** (29 cases, stdlib
  `unittest`, canonical-only) — wired into `bin/tests.sh` (51 → 54 suite checks). Advisory tool,
  **no hard gate**. Resolves fork backlog **BL-5** (the `[BL-5]` BACKLOG removal lands on fork
  `main` at merge, since this upstream-based branch carries no `docs/planning/`). Designated
  framework **v3.2** (minor) — annotated tag + GitHub Release at the PR #50 merge commit;
  `DASHBOARD_VERSION` bumps **2.7.0 → 2.8.0**. → full narrative:
  [`CLAUDE.md` §Versioning "v3.2"](CLAUDE.md#versioning).
- **Commit/PR:** `b2efd76` (dashboard logic, both twins) · `536837f` (tests + `.gitignore` +
  `bin/tests.sh` wiring + ledger) · `bad258c` (review-hardening fixes) · this commit (v3.2 release
  narration — `CLAUDE.md` §Versioning + `README.md` What's New) — branch
  `feat/dashboard-doc-only-scoring` (from `upstream/main`) → [PR #50](https://github.com/KJ5HST/methodology/pull/50).
  Design pressure-tested by a judge panel + adversarial synthesis (`wf_7174281b-754`); the
  implementation was then hardened by a 4-dimension adversarial review + default-to-refuted verify (`wf_7c95bb29-131`).
- **Session:** BL-5 dashboard doc-only scoring · **Verified:** 29/29 dashboard unit tests + 54/54
  `bin/tests.sh`; twins byte-identical + both `DASHBOARD_VERSION` 2.8.0; real runs — this mixed
  repo stays code-scored (Testing kept; Large-files still trips on the 2465-line `.py`), a
  synthetic doc-only tree detects doc-only, fills the slot with Render/Verify, and drops the false
  no-test-infra + big-`.md` risks; no `starter-kit/__pycache__` generated. The review found **6
  real defects** — a BOM-prefixed `.methodology-profile` override silently dropped; the large-file
  check inspecting only `largest[0]` (a non-source #1 masking a real large source file below it);
  `fmt_ratio` mislabeling a zero-source *code* repo `(doc-only)`; the footnote printing a false
  `source_loc ≤ 200` on a marker-forced repo; a tautological cap test; an untested render-dependency
  advisory — **all fixed and regression-tested**.

### 2026-07-08 · [ad hoc] PR #49 merged to KJ5HST/main; fork synced; BL-6 follow-up 1c closed
- **Change:** [PR #49](https://github.com/KJ5HST/methodology/pull/49) (BL-6 follow-up 1c —
  `sample-project/.gitignore` ignores the tutorial smoke-test store `demo.json`) merged to `KJ5HST/main`
  (merge `ca7c063`); fork `main` synced via `git merge upstream/main` (fork-sync merge `68488e1`, resolving
  one `CHANGELOG.md` union conflict, reconciled newest-on-top); the head branch
  `docs/sample-gitignore-demo-json` pruned (origin + local); `docs/planning/BACKLOG.md` marks 1c merged.
  With this, **all BL-6 follow-ups 1a/1b/1c are shipped**; BL-6 items 2–3 and BL-5 remain. Canonical-only
  tutorial asset — **no version event**.
- **Commit/PR:** [PR #49](https://github.com/KJ5HST/methodology/pull/49) → merge `ca7c063`; fork-sync merge `68488e1`; this commit (fork `main` — BACKLOG close-out + this ledger entry).
- **Session:** BL-6 1c merge/close-out · **Verified:** `sample-project/.gitignore` byte-identical to `upstream/main` post-merge; 51/51 `bin/tests.sh`; ledger source-tag census intact.

### 2026-07-08 · [ad hoc] sample-project/.gitignore ignores demo.json (Tutorial 2/3 smoke-test store)
- **Change:** `docs/tutorials/sample-project/.gitignore` now ignores **`demo.json`** — the `--file demo.json`
  store that the Tutorial 2 (and Tutorial 3) Phase 3E runtime smoke test writes. The ignore list previously
  covered only `todos.json`/`__pycache__/`/`.pytest_cache/`, and T2's 3F stages four named files, so a
  learner replaying T2 was left with `demo.json` **untracked** after close-out — undercutting the clean-tree
  discipline the tutorial teaches. `demo.json` is the only non-ignored artifact the tutorials generate
  (verified: sole `--file` store; the default `todos.json` is already ignored). Resolves fork backlog BL-6
  follow-up 1c. Canonical-only tutorial asset — **no version event**.
- **Commit/PR:** `f84a440` (branch `docs/sample-gitignore-demo-json`) → [PR #49](https://github.com/KJ5HST/methodology/pull/49), merged `ca7c063` (canonical-only tutorial asset, no version event).
- **Session:** BL-6 follow-up 1c · **Verified:** 51/51 `bin/tests.sh`; grep-confirmed `demo.json` is the complete untracked-artifact set (T2/T3 `--file` sweep); co-staged through `.githooks/pre-commit`.

### 2026-07-08 · [ad hoc] PR #48 merged to KJ5HST/main; fork synced; BL-6 follow-ups 1a/1b closed, 1c filed
- **Change:** [PR #48](https://github.com/KJ5HST/methodology/pull/48) (BL-6 follow-ups 1a/1b — the
  `HOW_TO_USE.md` Phase 3E smoke-test re-letter + `T1_setup.md` setup commit) merged to `KJ5HST/main`
  (merge `be0a523`); fork `main` synced via `git merge upstream/main` (fork-sync merge `cc6023a`, resolving
  one `CHANGELOG.md` union conflict, reconciled newest-on-top); the head branch
  `docs/closeout-3e-smoke-and-t1-commit` pruned (origin + local); `docs/planning/BACKLOG.md` marks 1a/1b
  merged and files a new follow-up **1c** (`sample-project/.gitignore` misses `demo.json`, surfaced by the
  PR #48 re-verify). Docs-lag correction — **no version event**. BL-6 items 2–3 and follow-up 1c remain open.
- **Commit/PR:** [PR #48](https://github.com/KJ5HST/methodology/pull/48) → merge `be0a523`; fork-sync merge `cc6023a`; this commit (fork `main` — BACKLOG close-out + this ledger entry).
- **Session:** BL-6 1a/1b merge/close-out · **Verified:** distributed `HOW_TO_USE.md` + `docs/tutorials/{T1_setup,T2_worked_transcript}.md` byte-identical to `upstream/main` post-merge; 51/51 `bin/tests.sh`; ledger source-tag census intact.

### 2026-07-08 · [ad hoc] HOW_TO_USE close-out gains Phase 3E smoke test (re-lettered 3E→3F, 3F→3G); T1 commits the seeded ledger
- **Change:** two v3.1 close-out fidelity fixes to the teaching docs (fork backlog BL-6 follow-ups 1a + 1b).
  **1a** — `HOW_TO_USE.md` §Phase 3 Close Out gained the missing **3E: Runtime smoke test** step and
  re-lettered the trailing two to match canonical `SESSION_RUNNER.md` (Commit **3E→3F**, Report and STOP
  **3F→3G**); the FM #27 ledger recording stays in the re-lettered **3F Commit**, and the failure-mode
  table now cites the close-out letters (FM #24 → Phase 3E, FM #27 → Phase 3F). **1b** —
  `docs/tutorials/T1_setup.md` Step 6 now explicitly commits the setup (`git add -A && git commit`) so the
  Step-1-seeded `CHANGELOG.md`/`ROADMAP.md` are tracked before the first session; Step 5 now gitignores the
  generated `dashboard.html` (so `git add -A` stays clean and Tutorial 2's clean-tree premise holds), and
  `T2_worked_transcript.md`'s seed citation is reconciled to **[T1 Step 1]**. Docs-lag correction — **no version event**.
- **Commit/PR:** `85aca72` (branch `docs/closeout-3e-smoke-and-t1-commit`) → [PR #48](https://github.com/KJ5HST/methodology/pull/48), merged `be0a523` (docs-lag correction, no version event).
- **Session:** BL-6 follow-ups 1a/1b · **Verified:** 6-lens adversarial review → 6 findings fixed (2 majors: the T1↔T2 `git commit -am` contradiction and `git add -A` sweeping in `dashboard.html`); 2 focused re-verifies returned CONSISTENT + CLEAN; 51/51 `bin/tests.sh`; co-staged through `.githooks/pre-commit`.

### 2026-07-08 · [ad hoc] PR #47 merged to KJ5HST/main; fork synced; BL-6 item 1 fully closed
- **Change:** [PR #47](https://github.com/KJ5HST/methodology/pull/47) (the BL-6 item-1 `HOW_TO_USE.md` +
  `T2_*` FM #27 pedagogical refresh) merged to `KJ5HST/main` (merge `3bb7825`); fork `main` synced via
  `git merge upstream/main` (fork-sync merge `6db6a03`, resolving one `CHANGELOG.md` union conflict — the
  fork's `[BL-6]` / v3.1 entries vs. the branch's own `[ad hoc]` entry, reconciled newest-on-top); the head
  branch `docs/how-to-use-fm27-ledger` pruned (origin + local); `docs/planning/BACKLOG.md` BL-6 item 1
  marked merged. Docs-lag correction — **no version event** (FM #27 already shipped in v3.1). BL-6 items
  2–3 and follow-ups 1a/1b remain open.
- **Commit/PR:** [PR #47](https://github.com/KJ5HST/methodology/pull/47) → merge `3bb7825`; fork-sync merge `6db6a03`; this commit (fork `main` — BACKLOG close-out + this ledger entry).
- **Session:** BL-6 item-1 merge/close-out · **Verified:** distributed files (`HOW_TO_USE.md`, `T2_first_session.md`, `T2_worked_transcript.md`) byte-identical to `upstream/main` post-merge; 51/51 `bin/tests.sh`; ledger source-tag census intact (issue / BL / ad-hoc all present).

### 2026-07-08 · [BL-6] Groom BL-6 — item 1 (pedagogical refresh) shipped via PR #47; file follow-ups 1a/1b
- **Change:** `docs/planning/BACKLOG.md` BL-6 updated — item 1 (HOW_TO_USE + T2-tutorial FM #27 / count
  refresh) marked ✅ shipped via upstream [PR #47](https://github.com/KJ5HST/methodology/pull/47) (pending
  merge). Two follow-ups discovered during the refresh filed under BL-6: **1a** — `HOW_TO_USE.md`'s
  close-out enumeration still lacks canonical's Phase 3E runtime smoke-test step and its 3E/3F lettering
  lags canonical (its own future upstream PR); **1b** — `T1_setup.md` never explicitly commits the seeded
  `CHANGELOG.md`, so a learner can reach Tutorial 2 with it untracked. Items 2–3 (seed-format migration
  affordance, hook-distribution decision) remain open. Fork-only; not part of any upstream PR.
- **Commit/PR:** this commit (fork `main`); the refresh itself is [PR #47](https://github.com/KJ5HST/methodology/pull/47) (see the `[ad hoc]` entry on that branch).
- **Session:** BL-6 item 1 · **Verified:** n/a — `docs/planning` grooming only.

### 2026-07-08 · [ad hoc] HOW_TO_USE + T2 tutorials: sync close-out docs to the v3.1 FM #27 ledger
- **Change:** `HOW_TO_USE.md` (a distributed file) and the `docs/tutorials/T2_*` pair predated failure
  mode #27 and still taught a pre-ledger close-out. Now current: `HOW_TO_USE.md` FM count **23 → 27**
  (two sites) with compressed rows **24–27** added, and the `CHANGELOG.md` action-ledger recording folded
  into the 3E close-out step (cited as Failure Mode #27); `T2_first_session.md` + `T2_worked_transcript.md`
  show the Phase 3F ledger entry, the paired `BACKLOG.md` removal for a `[BL-N]` item, and explicit
  `git add` staging (so a freshly-seeded, still-untracked ledger is not silently dropped by `git commit -am`).
  Resolves the pedagogical-refresh half of fork backlog BL-6. Deliberately out of scope, tracked as a
  BL-6 follow-up: `HOW_TO_USE.md`'s close-out enumeration still lacks the Phase 3E runtime smoke-test step
  and its 3E/3F lettering lags canonical.
- **Commit/PR:** `1f436f4` (branch `docs/how-to-use-fm27-ledger`) → [PR #47](https://github.com/KJ5HST/methodology/pull/47), merged `3bb7825` (docs-lag correction, no version event).
- **Session:** BL-6 item 1 · **Verified:** 6-lens adversarial review (4 fidelity findings fixed); 51/51 `bin/tests.sh`; co-staged through `.githooks/pre-commit`.

### 2026-07-07 · [ad hoc] v3.1 shipped — PR #46 merged, tag + GitHub Release cut, fork synced
- **Change:** the held v3.1 deployment gate cleared after the v3.0→v3.1 adopter-migration trial passed
  (operator post-trial confirm). PR #46 merged to `KJ5HST/main` (merge `75a6853`); the annotated tag
  `v3.1` was cut at that commit and its **GitHub Release published + marked Latest**; fork `main` synced
  (`1adf6b3`, 0 behind upstream) and the tag mirrored to `origin` (identical tag object `202669a` on both
  remotes); the merged feature branch `feat/changelog-authoritative-ledger` was pruned (local + origin).
  Failure-mode count is now **27**.
- **Commit/PR:** [PR #46](https://github.com/KJ5HST/methodology/pull/46) → merge `75a6853`; fork-sync
  merge `1adf6b3` (this entry). Release: <https://github.com/KJ5HST/methodology/releases/tag/v3.1>.
  → full narrative: [`CLAUDE.md` §Versioning "v3.1"](CLAUDE.md#versioning).
- **Session:** v3.1 deploy · **Verified:** 6-dimension adversarial release-readiness pass (version strings,
  FM #27 count, README↔§Versioning parity, ledger integrity, `.githooks/pre-commit`, close-out
  propagation) — clean; 51/51 `bin/tests.sh`; tag object byte-identical on `upstream` + `origin`.

### 2026-07-07 · [ad hoc] BOOTSTRAP: add earlier-version→v3.1 adopter migration note (seed CHANGELOG not auto-updated)
- **Change:** a local v3.0→v3.1 adopter-migration trial (real `bin/sync` against a pristine v3.0 tree)
  confirmed the update path is sound — **8 tracked files upgrade with no `--force`**, drift guard intact —
  but surfaced that the recomposed action-ledger seed (`CHANGELOG.md`, `SESSION_NOTES.md`) does **not**
  reach existing adopters (seed = write-if-absent, never clobbered). `starter-kit/BOOTSTRAP.md` gains an
  "Updating an existing project from an earlier methodology version" note: prefer `--source=local` from a
  full checkout, and manually reconcile (or delete-and-reseed) an older `CHANGELOG.md` to pick up the
  action-ledger format. Remaining loose ends (HOW_TO_USE / tutorial refresh, optional adopter re-seed
  tooling, hook-distribution decision) tracked in fork backlog BL-6.
- **Commit/PR:** this commit — branch `feat/changelog-authoritative-ledger` (held; pre-`v3.1`).
- **Session:** adopter-migration trial · **Verified:** live migration (dry-run + real sync + byte-compare) + 51/51 `bin/tests.sh`; this commit co-staged the ledger through the shipped `.githooks/pre-commit` gate.

### 2026-07-07 · [ad hoc] v3.1 release narration — §Versioning + What's New; tag + Release at PR #46 merge
- **Change:** the CHANGELOG-ledger campaign (S2–S7) is designated **v3.1** — a minor bump (first new
  failure mode since v2.7). `CLAUDE.md` §Versioning gains the narrated v3.1 entry, `README.md` §What's
  New its public restatement; the annotated tag `v3.1` + GitHub Release are cut at the PR #46 merge commit.
- **Commit/PR:** this commit (release narration) · [PR #46](https://github.com/KJ5HST/methodology/pull/46). → full narrative: [`CLAUDE.md` §Versioning "v3.1"](CLAUDE.md#versioning).
- **Session:** S7 · **Verified:** 51/51 `bin/tests.sh`.

### 2026-07-07 · [ad hoc] Authoritative CHANGELOG ledger campaign — gate + reconcile + dashboard + hook (S2–S7 complete)
- **Change:** `CHANGELOG.md` is now a dependable cross-source action ledger, closed on two
  mechanisms rather than one: a write-time gate (FM #27, Phase 3F), a reconcile-on-read backstop
  (Phase 0), a recomposed seed template, a dashboard freshness monitor, this dogfooded root ledger,
  a `.githooks/pre-commit` co-staging gate (decision D1 — the mechanical enforcement where a repo
  has no root runner), and the ledger close-out step propagated into every session-type and campaign
  checklist (escape #8). The whole campaign S2–S7 is complete.
- **Commit/PR:** `2227aab` (S2, FM #27) · `4828929` (S3, Phase 0 reconcile) · `f25e0c4` (S4, seed) ·
  `89b8f60` (S5, dashboard) · `339dfb2` (S6, root ledger) · `d2184cc` (S7, checklists) · this commit
  (S7, hook + docs) — branch `feat/changelog-authoritative-ledger`.
  Ratified plan: [`docs/planning/changelog-authoritative-ledger-gate-plan.md`](https://github.com/rmsharp/methodology/blob/main/docs/planning/changelog-authoritative-ledger-gate-plan.md) (`1710e90`, fork `main` only).
- **Session:** S7 · **Verified:** 9/9 hook behavior tests (block / pass / absent-ledger / mid-merge / `--no-verify`) + 51/51 `bin/tests.sh`.

<!-- Entries below were backfilled at ledger creation (S6), covering everything v3.0-forward per decision D5.
     They were reconstructed from git history at ledger birth, not logged live at the time of the action. -->

### 2026-07-07 · [ad hoc] Operational backlog reopened with BL-5 after full retirement
- **Change:** `docs/planning/BACKLOG.md` was retired 2026-07-06 once BL-1/2/3/4 all closed, then
  reopened 2026-07-07 with BL-5 (make `methodology_dashboard.py` adapt scoring to document-only repos).
- **Commit/PR:** `ff5cee9` (retire) · `72dc914` (reopen with BL-5). *(fork `main`)*
- **Session:** S6 (backfill) · **Verified:** n/a — docs-only (planning).

### 2026-07-06 · [BL-4] Backlog item BL-4 closed — methodology housekeeping
- **Change:** planning docs archived and stale branches pruned; BL-4 removed from `docs/planning/BACKLOG.md`.
- **Commit/PR:** `69dad12`. *(fork `main`)*
- **Session:** S6 (backfill) · **Verified:** n/a — docs-only (planning).

### 2026-07-06 · [ad hoc] PR #45 merged — v3.0.1 added to the §Versioning ledger
- **Change:** `CLAUDE.md` §Versioning gained its v3.0.1 entry (the release itself had already shipped at the PR #44 merge).
- **Commit/PR:** PR #45 (content `3fee545`, merged `4df8ee6`).
- **Session:** S6 (backfill) · **Verified:** n/a — docs-only.

### 2026-07-06 · [ad hoc] Released v3.0.1 — REUSE-compliance metadata + README badges
- **Change:** the repo's already-MIT licensing was made machine-readable (REUSE Spec 3.3); a patch
  release was cut on top of v3.0 (not a re-point — v3.0 left untouched).
- **Commit/PR:** annotated tag `v3.0.1` at `aa822f6` (the PR #44 merge). → full narrative: [`CLAUDE.md` §Versioning "v3.0.1"](CLAUDE.md#versioning).
- **Session:** S6 (backfill) · **Verified:** `reuse lint` 53/53; live REUSE badge scanned compliant.

### 2026-07-06 · [ad hoc] PR #44 merged — REUSE.toml + LICENSES/MIT.txt + README badges
- **Change:** added `REUSE.toml` (single bulk `path = "**"` MIT annotation), `LICENSES/MIT.txt`, and
  two README badges (static `License: MIT` + live REUSE-compliance); no existing framework file gained an inline SPDX header.
- **Commit/PR:** PR #44 (content `7b5238a`, merged `aa822f6`).
- **Session:** S6 (backfill) · **Verified:** `reuse lint` 53/53 files, 0 problems.

### 2026-06-25 · [issue #43] Released v3.0 — relicensed under the MIT License
- **Change:** the bespoke source-available `LICENSE` was replaced with verbatim standard MIT text;
  use/copy/modify/distribute/**sell** with attribution retained is now permitted (the prior no-resale restriction dropped).
- **Commit/PR:** relicense `49a103a`, release `5525f30`, annotated tag `v3.0`. Issue: <https://github.com/KJ5HST/methodology/issues/43>. → full narrative: [`CLAUDE.md` §Versioning "v3.0"](CLAUDE.md#versioning).
- **Session:** S6 (backfill) · **Verified:** n/a — relicense + lockstep README/CLAUDE.md updates.

---

**Release history before v3.0 (v1.0 – v2.9):** not re-narrated here — see [`CLAUDE.md` §Versioning](CLAUDE.md#versioning)
for the per-version narrative and `README.md` §What's New for the public restatement. This ledger is
prepend-only from v3.0 forward (decision D5: an authoritative ledger needs no hole at its recent edge,
and duplicating §Versioning would violate cite-don't-restate).
