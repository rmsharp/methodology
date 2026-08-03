# Dashboard Signal-Integrity Campaign — ratified plan

**Status:** RATIFIED (operator decisions D1–D4 taken 2026-07-25, session S9).
**Deliverable of S9:** this plan. **Implementation begins in S10 at Layer 1.**
**Scope:** `tools/methodology_dashboard.py` + its byte-identical twin `starter-kit/methodology_dashboard.py`.
**Resolves:** upstream issues [#59](https://github.com/KJ5HST/methodology/issues/59),
[#60](https://github.com/KJ5HST/methodology/issues/60), [#61](https://github.com/KJ5HST/methodology/issues/61),
plus five defects found during this planning session that are not yet filed.

---

## 1. Root cause — one sentence

Every defect below is **a proxy presented as a semantic finding**: a 110-point weighted sum presented
as a percentage; `.exists()` at the repo root presented as "adoption"; a checkbox regex presented as
"completed work not migrated"; any file whose name starts with `CHANGELOG` presented as "has an action
ledger"; and a signal that never executes presented as "no finding".

The dashboard is **advisory — never a hard gate** (`starter-kit/SESSION_RUNNER.md` Phase 0 step 5). That
does not make a wrong signal harmless: the motivating case was a **false GREEN on a real adopter**, which
silenced the exact finding the operator needed.

---

## 2. The eight defects — every one reproduced first-hand in S9

Reproduced by loading the scanner via `importlib` and calling `collect_all()` read-only. **Never copy the
scanner into a repo root to test it** — the copy inflates that repo's own source-LOC count (S7 lost a
measurement to this).

| # | Defect | Site | Verified evidence |
|---|--------|------|-------------------|
| 1 | Weights sum **110**, not 100, while `compliance_score` is rendered as a percentage | `:110-119` | `sum(w) == 110` |
| 2 | Methodology dimension is the only one of five with **no clamp** | `:1329` | `compliance=110 → methodology **22/20**, total **102/100**` |
| 3 | **No self-recognition** of the canonical repo | `:110`, `:782` | canonical scan → compliance 5, health **43/100**, false medium risk *"Partial methodology adoption (5%)"* |
| 4 | Backlog signal is **checkbox-only**, blind to table formats | `:131`, `:660` | real 643-line table backlog: counts **0**; true done-rows **256** |
| 5 | A `docs/` **product changelog masks the missing action ledger** | `:644-657`, `:1409` | fixture: *"adopter has no CHANGELOG ledger"* risk **suppressed**, replaced by misdirecting lag advisories |
| 6 | **Signal F is unreachable** when no changelog exists | `:698-701` vs `:772` | identical 60 done-marks: ledger absent → **silent**; ledger present → fires |
| 7 | **Archive shadowing** — `sorted()` returns the first name-prefix match | `:648-654` | `CHANGELOG-archive.md` + `CHANGELOG.md` present → locator returns **the archive** (`-` = 0x2D sorts before `.` = 0x2E) |
| 8 | **`HANDOFFS.md` missing from the checklist** | `:110-119` | shipped to adopters as SEED since v3.3 (`bin/_manifest.py:47`); never added |

Defects 6, 7, 8 and the fenced-code-block false positive (§4.3) are **not filed upstream**. File them, or
let this plan stand as their record — an operator decision at merge.

### 2.1 The live blast radius

`mts-system` currently scores `compliance_score: **110**` → `methodology: **22/20**` → total **90/100**.
Its card renders **"Methodology Compliance (110%)"** *today*. Issue #61 predicted the 110% case would be
the one "someone would probably have noticed"; it is now live, because that adopter completed its v3.5
migration (`28e9bb3`) after #61 was filed.

**Consequence for implementers:** the #60 live reproduction fixture is **gone**. Use synthetic fixtures;
recover the real 643-line backlog from `mts-system` commit `383c1715:BACKLOG.md` when real data is needed.

---

## 3. Evidence inventory (grep-based, MANDATORY per Planning Sessions)

**Every consumer of `compliance_score`** — `grep -n "compliance_score" tools/methodology_dashboard.py`:

| Site | Role | Broken how |
|------|------|-----------|
| `:805` | producer | emits a 0–110 sum |
| `:1329` | health dimension | `int(score * 0.2)`, **unclamped** |
| `:1368-1372` | risk thresholds | `== 0` / `< 50` stated in % against a 110 scale |
| `:1583-1585` | portfolio grid | colour ladder `>=80` / `>=40` **mis-scaled**, renders `{score}%` |
| `:1892` | project card | renders `({score}%)` |

**The three subsystems that answer "does this repo have a changelog"** — and they disagree:

| Subsystem | Searches | Reports on the fixture |
|-----------|----------|------------------------|
| `collect_doc_metrics` `:620-641` | root + `docs/`, name-prefix | `has_changelog: True` |
| `_find_changelog` `:644-657` | root + `docs/`, name-prefix, first sorted | `present: True` |
| `METHODOLOGY_ITEMS` via `:782` | root, exact `CHANGELOG.md` | `missing_files: ['CHANGELOG.md']` |

The risk layer at `:1409` trusts the middle one. It should trust the last one.

**Distribution manifest** (`bin/_manifest.py`) — 22 entries, **0 under `bin/`**. `bin/` is therefore
canonical-only, which makes `bin/_manifest.py` a sound structural marker for §5.4. Adopter-root
destinations: `SESSION_RUNNER.md`, `SAFEGUARDS.md`, `RECOMMENDED_SKILLS.md`, `CONTEXT_TEMPLATE.md`,
`CLAUDE_TEMPLATE.md`, `BOOTSTRAP.md`, `methodology_dashboard.py`, `SESSION_NOTES.md`, `CHANGELOG.md`,
`HANDOFFS.md`, `ROADMAP.md`.

**Baseline:** `bin/tests.sh` = **84 passed / 0 failed**; `tools/test_methodology_dashboard.py` = **29
tests, OK**. Confirmed across four consecutive runs. *(One earlier run reported 83/84 and could not be
reproduced; the failing check was never captured. Treat an isolated 83/84 as unexplained, not as your
change — re-run before diagnosing.)*

---

## 4. Ratified design decisions

### D1 — Normalize to a true 0–100 percentage *(operator-ratified)*

Decided by git history, not preference: commit `46b17e8` (v2.0) created **six** items summing to
**exactly 100** — the `%` label and the bare `* 0.2` were correct **by construction**. Commit `274dcd4`
(v2.1) appended `CHANGELOG.md` (5) and `ROADMAP.md` (5) **without re-cutting the scale**. `README.md:473`
still documents "Methodology compliance scoring (0-100)". Normalization **restores** the original
invariant rather than inventing a new one.

- `METHODOLOGY_MAX = sum(w for _, w, _ in METHODOLOGY_ITEMS)` — **derived, never a literal**. This, not
  the number 110, is the actual fix for defect 1: a hardcoded denominator is what drifted in the first
  place, and a literal `100` would drift again the next time the checklist grows.
- Normalize **once, producer-side**, in `collect_methodology_metrics`. All four downstream consumers then
  become correct with no per-site arithmetic, and double-rounding is avoided.
- Render `"{pct}% ({raw} of {MAX})"` so the raw sum stays inspectable.
- Keep the `meth == 0` HIGH-risk branch reading the **raw** sum — scale-independent, so a small weight in
  a future larger table cannot truncate to 0% and false-fire.

**Accepted cost:** a one-time fleet-wide deflation of the methodology sub-score (~9%). Ratified.

### D2 — `HANDOFFS.md` joins the checklist, weighted 5 *(operator-ratified)*

Matches its structural twin `CHANGELOG.md` exactly (both SEED, both lifetime-stable). `METHODOLOGY_MAX`
becomes **115**, absorbed by the derived denominator.

**Accepted cost:** every pre-v3.3 adopter reads as a one-point health drop through no action of their own,
and `bin/sync` never overwrites an existing SEED, so they must act. The statement is **true** — they *are*
missing a v3.3 operating artifact — and it self-corrects on re-sync. Ratified.

### D3 — Ledger identity: a **dual predicate**, not a narrowed one

This is the subtlest decision in the plan and the one where the obvious fix is wrong.

The tempting fix — point `_find_changelog` at the root only — **silently costs a documentation point**
for exactly the repo class #60b is about. Mechanism, verified by reading: `evaluate_changelog_freshness`
early-returns at `:698-701` leaving `is_fresh: False`, and `score_health:1309` adds `+1` only when
`is_fresh` is true. An adopter with `docs/changelog.md` would lose that point silently while the change
claims "no score moves" — reproducing defect #61's own failure mode (a correct assertion over an
unreachable input) *inside the fix*.

**Therefore:**
- `present` / `is_fresh` / Signals B–D keep computing against the **best-available** changelog. Unchanged.
- A **new** root-anchored `ledger_present` is consumed **only** by the `:1409` risk.
- Lag messages **name the file they were computed against** and drop the word "ledger"
  (`"docs/changelog.md trails HEAD by N commits"`), which attacks the misdirection directly.
- `collect_doc_metrics.has_changelog` is **untouched** — it answers a different question (doc hygiene).

### D4 — Abstention is a first-class result

`_scan_backlog_done` returns `{format, done, recognized}`. A backlog whose format is unrecognized
produces a **visible footnote** ("done-mark format not recognized; this signal is inactive for this
repo"), never a silent `0`. **A silent 0 is defect #4 itself.** This repo's own
`docs/planning/BACKLOG.md` (`| Item | Scope | Outcome |`, no Status column) lands in that branch and will
correctly say so.

> **CORRECTION (Layer 6, S16) — the last sentence above is FALSE at HEAD, and the shipped behaviour
> is correct while the ratified text is not.** Measured against `HEAD` by calling the shipped
> function directly: `_scan_backlog_done(<repo root>)` →
> `{'format': 'unrecognized', 'done': 0, 'recognized': False, 'source': 'docs/planning/BACKLOG.md'}`.
> The *classification* half is right — the format is read as `unrecognized`, exactly as ratified.
> But this repo emits **nothing**, because the abstention has exactly **one** disclosure surface
> (the Signal-F advisory tuple in `evaluate_changelog_freshness`) and that surface is gated on
> `(path / "SESSION_RUNNER.md").is_file()` — the *adopter* test, which this repo fails: its runner
> lives at `starter-kit/SESSION_RUNNER.md`, not the root. So the backlog lands in the abstaining
> branch and stays silent. **Widening that gate was rejected by operator decision in S13, and that
> decision stands** — Signal F's premise (an item is *removed* from `BACKLOG.md` in the commit that
> logs it to `CHANGELOG.md`) is verifiably false for this repo class, whose backlog deliberately
> **keeps** all completed `BL-` rows permanently; widening the counting branch would manufacture a
> false "not migrated" accusation the moment that table gains a Status column. The correct reading
> of D4 is therefore: *abstention is a first-class result **for adopters**, which is the population
> the signal is scoped to.* Two smaller drifts in the same paragraph: the return dict now carries a
> fourth key, `source` (which location the backlog was actually found at), and the shipped advisory
> text is "done-mark format not recognized (no `- [x]` checkboxes and no Status column) — the
> unmigrated-work signal is inactive for this repo", not the shorter string quoted above.

---

## 5. Layer decomposition — one layer per session, do NOT bundle

Each code layer touches exactly **4 files** (both twins + tests + `CHANGELOG.md`), sitting at 4 of the
5-file per-commit cap with no slack — `.githooks/pre-commit` requires `CHANGELOG.md` co-staged.

> **STANDING RULE — RED FIRST, at every layer.** The suite is green against **all eight** defects today
> (84/84, 29/29). "Tests pass" is therefore **not evidence** at any boundary. Add each assertion and
> **watch it fail against unpatched code** before touching the scanner. `base_metrics():55` pins
> `compliance_score: 0`, and the only two `changelog` occurrences in the entire test file are constants
> at `:52` and `:57` — the changelog subsystem has **zero** existing coverage.

### Layer 1 — Scale honesty + checklist currency (defects 1, 2, 8)

**Files:** `tools/methodology_dashboard.py`, `starter-kit/methodology_dashboard.py`,
`tools/test_methodology_dashboard.py`, `CHANGELOG.md`

**Changes:** derived `METHODOLOGY_MAX`; add `("HANDOFFS.md", 5, "file")`; producer-side `compliance_pct`;
`:1329` → `min(20, int(pct * 0.2))`; `:1368-1372` thresholds vs `pct` (keep `== 0` on raw); `:1583-1585`
ladder + render vs `pct`; `:1892` render `"{pct}% ({raw} of {MAX})"`; collapse the three duplicate
`exists()` loops in `collect_methodology_metrics` (`:782-811`) into one; stamp `dashboard_version` into
each `dashboard_history.jsonl` entry. `DASHBOARD_VERSION` → **2.9.0**.

> **Load-bearing, not cleanup:** `render_methodology_grid:1570` hard-codes an **8-string** `headers`
> list while `:1571` derives `item_keys` from `METHODOLOGY_ITEMS`. Adding a 9th item therefore
> **misaligns the grid's columns** — 8 headers over 9 item cells. Deriving `headers` from
> `METHODOLOGY_ITEMS` is required for correctness in this layer, and is why defect 8 cannot be fixed by
> appending to the list alone. Assert `len(headers) == len(METHODOLOGY_ITEMS) + 2`.

**RED-first proof (must fail before the fix):**
1. `score_health` driven at `compliance_score = METHODOLOGY_MAX` asserts `methodology == 20` and
   `total <= 100` — today yields **22** and **102**.
2. The **manifest-vs-checklist structural guard**: every manifest adopter-root destination is either in
   `METHODOLOGY_ITEMS` or in an explicit `CHECKLIST_EXEMPT` dict with a stated reason. *Prototyped in S9
   and confirmed to fail on exactly `HANDOFFS.md` and nothing else.* This converts defect 8 from a
   one-off patch into an invariant — the next distributed artifact cannot repeat it.
3. Assert no literal denominator: `METHODOLOGY_MAX == sum(w for _, w, _ in METHODOLOGY_ITEMS)`.

**Done when:** no rendered percentage can exceed 100, no dimension exceeds its band, and the checklist
matches the distributed corpus.
**Verify:** `python3 tools/test_methodology_dashboard.py` · `bash bin/tests.sh` (expect 84) ·
`diff -q` the twins · re-scan `mts-system` and confirm the card no longer reads 110%.
**Stops coherently:** the one defect visible on 100% of the live adopter fleet is closed.
**This layer is one session. Close out when done.**

### Layer 2 — Ledger identity (defects 5, 6, 7)

**Files:** as Layer 1.

**Changes:** add `_find_action_ledger` (root only, exact `CHANGELOG.md`) alongside an **unchanged**
`_find_changelog`; add `ledger_present`, consumed only at `:1409`; fix archive shadowing by preferring an
exact `CHANGELOG.md` over any name-prefix match; make lag messages name their source file; **move the
Signal F emission above the `changelog is None` early return** so it no longer depends on ledger presence.
`DASHBOARD_VERSION` → **2.9.1**.

**RED-first proof:** (a) adopter + `docs/changelog.md`, no root ledger → the "no CHANGELOG ledger" risk
**fires** (today suppressed); (b) `CHANGELOG.md` + `CHANGELOG-archive.md` → locator returns
`CHANGELOG.md` (today the archive); (c) 60 done-marks, no changelog → Signal F **fires** (today silent);
(d) **regression lock** — an adopter with `docs/changelog.md` **keeps** its `+1` freshness point.

**Done when:** location answers membership, and no signal depends on an unrelated file existing.
**Verify:** as Layer 1, plus the four fixtures above.
**Stops coherently:** the reported adopter learns it has no action ledger instead of being told to update
a product release-notes file.
**This layer is one session. Close out when done.**

### Layer 3 — Backlog shape with abstention (defect 4 + fenced-block false positive)

**Files:** as Layer 1.

**Changes:** `_scan_backlog_done` → `{format, done, recognized}`; **strip fenced code blocks before
scanning**; keep the checkbox predicate; add the table predicate — *a cell that **starts with** a done
token, in a row of >= 3 cells, ignoring the ID column*; abstain visibly on an unrecognized format.
`DASHBOARD_VERSION` → **2.9.2**.

The table predicate is **empirically tuned against the real 643-line backlog** — do not re-derive it:

| Predicate | Count | Verdict |
|-----------|-------|---------|
| current checkbox-only | 0 | blind |
| cell *contains* a done token | 321 | **94 false positives** (NOTES-column prose) |
| cell *equals* a done token | 227 | misses `**DONE (Session 30, …)**`; matches the legend row |
| **starts-with, >=3 cells, ignore ID column** | **256** | rejects all 94 FPs *and* the legend row |

256 lands within 3 of S8's independent hand count of 253.

**RED-first proof:** (a) 4-column Status-table fixture counts its DONE rows (today **0**); (b) a fenced
` ```markdown ` block containing `- [x]` counts **0** (today **1** — a live false positive); (c) the real
recovered backlog counts 256 (today 0); (d) a checkbox backlog still counts exactly as before.

**Done when:** a readable backlog is measured and an unreadable one says so out loud.
**Verify:** as Layer 1, plus the four fixtures.
**Stops coherently:** the format-blindness that produced the false green is closed.
**This layer is one session. Close out when done.**

### Layer 4 — Repo role (defect 3)

**Files:** as Layer 1.

**Changes:** `detect_repo_role` following the BL-5 precedent exactly — marker override
(`.methodology-profile`, new `framework` token, read with `encoding="utf-8-sig"` so the v3.2 BOM fix is
inherited) → structural heuristic (`bin/_manifest.py` **and** `starter-kit/SESSION_RUNNER.md` both
present; sound because `bin/` ships nothing to adopters). When `role == framework`, score a
`FRAMEWORK_ITEMS` checklist and suppress/reframe the adoption risk. **Both marker readers must scan the
full token set**, not `tokens[0]`, so `doc-only` and `framework` compose. `DASHBOARD_VERSION` → **2.10.0**.

> **Do NOT score the framework repo by remapping `METHODOLOGY_ITEMS` onto `starter-kit/` paths.** S9
> tested this and it is wrong: `starter-kit/SESSION_NOTES.md` is a **27-line empty stub**
> (`[None — project just started]`) and `starter-kit/BACKLOG.md` **does not exist**. The remap would
> credit 20 points for a placeholder and render "SESSION_NOTES.md ✓" on a repo with no root session
> notes — **defect 3 inverted**, a false positive replacing a false negative.

**Detection and wiring land in the SAME layer.** Splitting them ships a version bump plus dead code with
every filed defect still live, failing FM #25's test ("if I stop here, is something working?").

**RED-first proof:** scanning this repo yields no "Partial methodology adoption" risk and a
Framework-Integrity score (today: 5% + a false medium risk); an adopter fixture's score is **unchanged**;
a `doc-only framework` marker satisfies both axes.
**Done when:** the repo that publishes the methodology stops being graded for failing to install itself.
**Verify:** as Layer 1, plus a scan of this repo and of an adopter fixture.
**Stops coherently:** all four filed issues are closed.
**This layer is one session. Close out when done.**

### Layer 5 — Completeness-critic sweep (v3.4 Learning #10 / AUDIT anti-pattern #9)

**Files:** `README.md`, `docs/tutorials/T7_portfolio_dashboard.md`, `starter-kit/BOOTSTRAP.md`,
`CHANGELOG.md`

**Mandatory, not optional.** This campaign adds a member to a numbered set (`METHODOLOGY_ITEMS` 8 → 9),
adds a detection axis, and makes a second health dimension context-dependent — and **not one** of these
targets appears in any code diff. v3.4 exists precisely because a clean diff-scoped review missed this.

| Target | Verified state | Action |
|--------|----------------|--------|
| `README.md:128` | "health (0-100) across 5 weighted dimensions" — **currently false** (max 102) | **Verify, don't edit** — L1 makes it true; re-run and confirm |
| `README.md:75` and `:79` | seeded files enumerated as "SESSION_NOTES.md, CHANGELOG.md, ROADMAP.md" — **omits `HANDOFFS.md`** | Add it — pre-existing v3.3 gap this campaign owes |
| `README.md` repo tree (`:182`, `:196`) | `tools/test_methodology_dashboard.py` never listed | Add — shipped in v3.2, never listed |
| `docs/tutorials/T7…:42` | enumerates the checklist files | Add `HANDOFFS.md` |
| `docs/tutorials/T7…:72` and `:85` | **both** say "compliance %" | Reconcile to the new rendering |
| `starter-kit/BOOTSTRAP.md:267` | "5 dimensions (…)" | Note slots 2 and 5 are context-dependent on repo class |

**Explicitly NOT edited** — dated release prose, frozen by the v2.7.1 convention:
`README.md:472-473` (v2.0 §What's New — and the documentary evidence for D1),
`README.md:287` (v3.2 §What's New), and `CLAUDE.md`'s v3.2 entry.

> **Rejected corpus edits.** The S9 design panel proposed "correcting" `CLAUDE.md`'s v3.2 claim of
> "29 stdlib-`unittest` cases" to 30, and its "51 → 54 checks" to 84. **Both rejected.** There are
> genuinely **29** test methods — `grep -c 'def test_'` returns 30 only because line 327 is
> `"test_app.py": "def test_f():…"`, a *string inside a fixture*. And "51 → 54" is a dated statement
> about what v3.2 did, not a claim about today. Applying either "fix" would have **introduced** an
> error — itself a grep signal that does not mean what it appears to mean.

**Verify:** `grep -rn "0-100\|compliance %\|5 weighted dimensions\|SESSION_NOTES.md\`, \`CHANGELOG.md"
README.md docs/tutorials/ starter-kit/ HOW_TO_USE.md` · `bash bin/check-links`
**This layer is one session. Close out when done.**

### Layer 7 — The installer defeats doc-only detection (amendment; executes BEFORE Layer 6)

> **Amendment ratified by operator decision, S14.** This defect was **not** among the eight this plan
> was written against — it was found by Layer 5's late boundary review, and it predates the campaign
> (live since **v3.2**). The number is **appended, never renumbered**, following this repo's own rule
> for numbered sets (`CLAUDE.md`: "FMs 1–26 must not be renumbered; new FMs append at the end"), so
> Layers 1–6 keep their identities. Its **execution slot is before Layer 6**, because Layer 6 closes
> the campaign and settles R1 — a release should not ship with a known live defect in this subsystem.

**The defect — the campaign's own class, from an unexpected direction.** `bin/sync` installs
`methodology_dashboard.py` (**3,070 lines**) to the adopter **root** (`bin/_manifest.py:43`,
disposition `TRACKED`), and `DOC_ONLY_SOURCE_LOC_MAX` is **200** (`:232`). So `detect_doc_only`'s
source-cap short-circuit (`:1841`) fires before the corpus disjunction (`:1855`) is ever consulted:
**installing the methodology destroys the doc-only fair-scoring v3.2 exists to provide.** The signal
"No test infrastructure" does not mean what it appears to mean — it means *we put our own scanner in
your repo and then counted it against you*.

**Measured (S14), on a Quarto-book fixture — 6 `.qmd` chapters + `_quarto.yml`, `git init`:**

| | `doc_only` | `source_loc` | testing dim | risk |
|---|---|---|---|---|
| before `bin/sync` | `True` | 0 | 4 (render proxy) | — |
| after `bin/sync` | `False` | 3,070 | **0** | **HIGH "No test infrastructure"** |

**Files:** `tools/methodology_dashboard.py`, `starter-kit/methodology_dashboard.py` (byte-identical
twins), `tools/test_methodology_dashboard.py`, `CHANGELOG.md`. `DASHBOARD_VERSION` → **2.10.1**.

**Change (operator-chosen fix A of three):** stop counting **framework-installed files** toward the
adopter's source LOC. `bin/sync` installs exactly one non-markdown file, so this is a one-name
exclusion, not a judgment call — confirm with
`[d for _,d,_ in DISTRIBUTION if not d.endswith('.md')]` → `['methodology_dashboard.py']`.

> **Two rejected alternatives, recorded so they are not re-proposed.** **(B) Raise or replace the
> 200-LOC cap** — knowingly surrenders v3.2's written guarantee that a mixed code+docs repo is never
> misclassified; any threshold above 3,070 makes a real 4,070-LOC code repo read as doc-only.
> **(C) No code change, rely on the marker** — converts v3.2's automatic fair-scoring into an opt-in
> feature and leaves a false HIGH risk on every doc-only adopter who never reads `BOOTSTRAP.md`
> §Step 9. Layer 5 already shipped the prose half of C (both `README.md` and `BOOTSTRAP.md` now tell
> a document-only project it **must** declare `doc-only`); that prose stays correct either way and
> is **not** a substitute for this fix.

**The exclusion must not become a laundering hole.** Exclude only by the manifest's own installed
name, at the point of the source-LOC read — never a general "skip large Python files" rule, which
would exempt an adopter's real code. A repo whose *own* source exceeds the cap must still read as
`code` after the exclusion.

**RED-first proof** (drive each against unpatched code and watch it fail — a rename produces
`AttributeError`, which proves absence, not wrongness):
(a) the synced Quarto fixture reports `doc_only=True` (today: `False`);
(b) a synced **real code repo** — 500 own-source functions ≈ 1,000 LOC plus the installed scanner —
still reports `doc_only=False` (**measured today: 4,070 → 1,000 after exclusion, still over the cap**,
so this test must be seen to fail against a *wrong* fix such as B, not merely pass against A);
(c) an **unsynced** doc repo is unchanged (no regression to the v3.2 path);
(d) the HIGH "No test infrastructure" risk is absent from (a) and present in a genuine no-test code repo.

> **CORRECTION (Layer 6, S16) — clauses (b) and (c) above are unsound as written. Both were
> re-measured at HEAD, and Layer 7 shipped replacements for both; the text here is corrected so the
> plan does not teach the two mistakes it caused.**
>
> **(b) is false.** The fixture it prescribes — a synced real code repo whose docs are one `README.md`
> — reports `doc_only=False` at **every** cap: measured 200 / 1,000 / 3,100 / 4,100 / 6,000 / 10,000,
> all `False`, with `source=1,000` own LOC and 21 framework docs discounted. It therefore **cannot**
> "be seen to fail against a wrong fix such as B", because raising the cap only lets control fall
> through to the corpus disjunction, which this fixture fails anyway on a single README. A test that
> passes identically against the fix and against the rejected alternative distinguishes nothing —
> the plan's own §8 #2 ("a test that passes against the bug is not coverage") applied to the plan.
> **What actually refutes fix B is an *unsynced* code repo with a real doc corpus**: measured
> `doc_only=False` at cap 200 and **`True` at cap 3,100** — the false doc-only classification of a
> genuine 1,000-LOC code repo that raising the cap would buy. Shipped as a labelled characterization
> test in `tools/test_methodology_dashboard.py`.
>
> **(c) was verified by a test structurally incapable of failing.** The Quarto fixture reports
> `doc_only=True` with `toolchain_present=True`, and that arm is a **standing-`True` disjunct** of the
> corpus check, so the verdict is invariant to both doc counts. (Stated precisely, because the
> mechanism is easy to get backwards: `render["toolchain_present"]` is the **last** of the three
> `or` operands, *reached only after* both doc-count comparisons evaluate `False` — it does not
> short-circuit ahead of them. What makes the test unfailable is that this final arm is `True`
> regardless, not that it is evaluated first.) Probed by counterfactual: stripping the
> fixture's markdown doc corpus bare leaves the verdict **unchanged at `True`**. No doc-corpus
> regression can ever move this test, so it could not have detected the framework-doc discount it was
> cited to protect. A plain-markdown fixture now carries clause (c). **Ask what a fixture makes
> unreachable, not only what it asserts.**
>
> **Line citations in this section were re-derived at HEAD** after Layer 7's five commits:
> `DOC_ONLY_SOURCE_LOC_MAX` is still `:232`, but the source-cap short-circuit moved `:1678` → **`:1841`**
> and the corpus disjunction `:1686` → **`:1855`**. Prefer the symbol names (`DOC_ONLY_SOURCE_LOC_MAX`,
> `detect_doc_only`) over the line numbers — this is the second time these citations have gone stale.

**Done when:** installing the methodology no longer changes a document-only repo's classification.
**Verify:** as Layer 1, plus the four fixtures above, plus `bin/tests.sh`, `bin/check-links`, twins
byte-identical, and a live read-only fleet re-scan showing no other repo's score moves.
**Stops coherently:** the subsystem is correct before Layer 6 settles the release.
**This layer is one session. Close out when done.**

### Layer 6 — Close-out and release decision

**Files:** `CLAUDE.md` (conditional), `HANDOFFS.md`, `CHANGELOG.md`

Settle **deferred decision R1** (below). If a release: one narrated `CLAUDE.md` §Versioning entry stating
that the FM count **stays 27** and no principle, phase, gate, or workstream changes, naming the one-time
scale step and the `dashboard_version` history stamp. Complete the receipt; `bin/check-handoff` green.

---

## 6. Deferred decision

**R1 — is this a tagged framework release?** *Deliberately deferred to merge by operator decision, the
same way PR #57 / BL-7 handled it.* Inputs when it is time: it changes scoring for every scanned repo,
resolves 3 filed issues + 5 unfiled defects, and every synced adopter copy begins emitting
`check_stale_version` warnings (`:251-264`) the moment canonical bumps.

---

## 7. Residual risks — here be dragons

1. **One-time trend discontinuity, unavoidable for any correct fix.** `dashboard_history.jsonl` persists
   only derived totals with no scale marker, and the trend renderer diffs first-vs-last across a 30-run
   window — so the scale step would render as a red regression arrow indistinguishable from a real one.
   The `dashboard_version` stamp (L1) is what makes it interpretable. **Do not skip it.**
2. **The table parser is the largest new surface and the only change with meaningful false-positive
   risk.** Its root cause is structural: `BACKLOG.md` is the one task-tracking file the framework never
   gave a format. Abstention (D4) is the containment.
3. **The framework heuristic will misfire** on any repo that legitimately ships `starter-kit/` templates
   plus distribution machinery without installing to its own root — a second framework distributor, or a
   monorepo vendoring this one. The `.methodology-profile` marker is the escape hatch; document it.
4. **Three notions of "the canonical repo" will coexist** after L4: `EXCLUDE_DIRS`' literal `"methodology"`
   string (`:74`), `CANONICAL_REL`'s hardcoded path (`:215`), and the new structural role. Not unified
   here — note it, do not silently add a fourth.
5. **Two dict keys now carry context-dependent meanings** — `testing` (Testing | Render/Verify, BL-5) and
   `methodology` (Compliance | Framework Integrity, this change). Both keys stay stable for portfolio
   aggregation by design; document the convention rather than renaming.
6. **Cross-platform divergence, pre-existing and deliberately not fixed here:**
   `collect_methodology_metrics` probes `CHANGELOG.md` exactly while the changelog subsystems upper-case
   the name, so a case-insensitive filesystem can disagree with a case-sensitive one. Out of scope.
7. **The commit budget has no slack** — 4 of 5 files per code layer. Any extra file forces a split.
8. **Presence is not use.** The checklist scores `.exists()`; it cannot tell a maintained
   `SESSION_RUNNER.md` from an empty stub, and this plan does not change that. The card footnote
   ("presence check — the scanner does not verify these files are used") is the honest disclosure.
   `mts-system` scoring 110% while running a v2.0-era runner is this limitation, and it is **not** closed
   by this campaign.

---

## 8. Method learnings from the planning session (S9)

Recorded here so they are durable and greppable. **A `FRAMEWORK_LEARNINGS.md` Learnings-table row is owed at
Layer 6**, once the campaign has actually shipped — editing that distributed file was out of scope for a
session whose ratified deliverable is this plan.

1. **Make the cross-reference machine-checkable, not re-greppable.** Learning #7 and #10 catch stale
   enumerations by *grepping at review time* — a human step that failed twice here (`HANDOFFS.md` missed
   both the compliance checklist and two `README.md` enumerations for two releases). Where an invariant
   is mechanical — "every distributed adopter-root file is on the checklist or explicitly exempt" — encode
   it as a **test**, and the class of defect cannot recur. Prototyped in S9; fails today on exactly
   `HANDOFFS.md`.
2. **A test that passes against the bug is not coverage.** `test_all_dims_bounded_and_total_is_sum`
   asserts the correct property over an input (`compliance_score = 0`) that can never violate it. Before
   trusting any assertion, **drive it against unpatched code and watch it fail.** This is why every layer
   above carries a RED-first clause.
3. **Adversarial design review pays even when the design is evidence-based.** The S9 panel refuted the
   author's own `starter-kit/` path-remap for #59 (it would have credited a 27-line empty stub and
   inverted the defect) and caught a silent `+1` documentation regression hiding inside the obvious #60b
   fix. Neither was visible from the issue text.
4. **…and the reviewer needs reviewing too.** The same panel asserted "30 tests" (a fixture *string*
   miscounted as a test method) and proposed edits to dated release prose the repo's own v2.7.1
   convention freezes. Both were rejected only because each claim was re-executed rather than read.
   Agent output is evidence to verify, not a conclusion to adopt.
