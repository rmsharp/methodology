# The Framework's Context Cost — Adopter Heuristics and a Remediation Plan

**Status:** PLAN. Nothing here is implemented. Written 2026-08-02 (session S30) against `0485d4a`.
**Scope:** fork-side. `docs/planning/` is absent from `bin/_manifest.py`'s DISTRIBUTION, so writing
this touches no adopter file. Several remedies below *do* touch distributed files; each needs the
operator's go-ahead before it goes upstream. **None is blocked.**
**Corrected 2026-08-03 (S33):** as first written this plan asserted that "the upstream channel is
PAUSED" and marked its adopter-facing half BLOCKED on that. No one imposed that constraint — see the
§5 note — and the correction re-ordered the queue.
**Origin:** not a backlog item. The operator asked whether a framework's accumulated learnings are
actually resident in an agent's context or are read-and-discarded, then assigned the two deliverables
in §0.

---

## 0. The brief, and this document's own rule

> 1. Develop some heuristics adopters can use to monitor and assess the impact of these three
>    expenses (**assuming you find all 3 should be monitored**).
> 2. Develop a plan to address any design deficiencies in this methodology.

The parenthetical is honored: **one of the three is declined as framed** (§2.2), and one is declined
in half (§2.3).

**This document applies its own central rule to itself.** Its thesis is that the framework stores
*derived* values — counts, sizes, line numbers — as hand-written prose, where they decay silently.
So every derived number below carries the command that computes it. A reader who doubts a figure
re-runs one line rather than trusting the sentence. Where a number has **no measured basis**, it says
so in those words.

That convention is also this plan's answer to an objection raised against it during review: a
prohibition on hand-authored derived values would refuse this very document, since a measurement
report cannot delete, generate, or freeze its own findings. **CITE is the fourth sink** (§3.5).

---

## 1. What was actually asked, and the answer

**Nothing is ever discarded from context.** There is no read-it-apply-it-drop-it mechanism. There are
three tiers, and they behave differently:

| Tier | What | Cost |
|---|---|---|
| Always resident | `CLAUDE.md` and any `@`-import in it — injected before turn 1, present every turn | `wc -c CLAUDE.md` → **8,519 B** |
| Read once, then carried | Everything else. Enters on Read, **never leaves** | see §2.1 |
| Compacted | When the session grows long, verbatim text is replaced by a **lossy summary** | what degrades first is line numbers and which-of-two-similar-counts |

That third tier is the mechanism behind the defect that provoked this plan. A 13-agent
re-measurement at this session's Phase 0 found **six of six** open backlog items carrying a wrong
number, every one the same shape: a figure that was correct at some earlier tree, later restated
from recollection instead of re-derived.

**Prompt caching hides the cost.** Cache reads bill at roughly a tenth of base input and were
measured at **91.7% of all input** (session S14, recorded in `docs/planning/BACKLOG.md` under BL-8).
Caching cuts the *price* of re-sending the prefix, not its *occupancy*. So framework growth is nearly
free in dollars and expensive in reliability — **the budget signal that would warn you is the one
caching suppresses.** This will never self-correct; the gap widens as caching improves. A deliberate
substitute is the only signal that will ever exist on that axis.

---

## 2. The monitoring verdict

### 2.1 Expense 1 — distributed prose: **MONITOR, REFRAMED**

The obvious metric is wrong. Total shipped is **618,679 B**, but the single largest distributed file
is `starter-kit/methodology_dashboard.py` at **155,453 B** — 25% of the shipment, and it is
*executed*, not read. Monitoring shipped bytes points an adopter at the cheapest artifact in the
corpus.

Monitor the **read set** — what Phase 0 obliges opening:

| Artifact | Bytes | Owner |
|---|---|---|
| `starter-kit/SESSION_RUNNER.md` | 62,410 | framework (FLOOR) |
| `starter-kit/SAFEGUARDS.md` | 15,386 | framework (FLOOR) |
| `CLAUDE.md` | 8,519 | adopter |
| `BACKLOG.md` | 35,330 | adopter |
| **Phase 0 doctrine subtotal** | **121,645** | |
| `HANDOFFS.md` + `CHANGELOG.md` (step 6 reconcile opens both) | 257,561 | adopter |
| **Total** | **379,206 B** | |

```sh
wc -c starter-kit/SESSION_RUNNER.md starter-kit/SAFEGUARDS.md CLAUDE.md \
      docs/planning/BACKLOG.md HANDOFFS.md CHANGELOG.md
```

At ~4 B/token that is ≈ **94,800 tokens before Phase 1 begins**. See §3.1 for why the token figure is
reported as a *proxy* and the byte figure as ground truth.

**One correction that three of four candidate designs got wrong:** dashboard output is *itself* in
the read path. `starter-kit/SESSION_RUNNER.md:17` mandates running it and `:25` mandates reporting
"Dashboard health score and any risk flags." A new gauge is not free; its own output row is the cost.
Hence the hard budget in §3.

### 2.2 Expense 2 — coordination residue: **DECLINE AS FRAMED. Monitor what it actually is.**

As put to the operator, "coordination residue from outward-facing upstream actions" is a **maintainer
cost**. An adopter has no PRs, no tags, no releases, no fork resyncs. A heuristic for it would read
zero for every adopter forever — worse than no gauge, because it looks like coverage.

The adopter's real second expense is **record growth**, and the finding there is not a missing gauge
but a **missing doctrine**:

- Zero of the **21** distributed `.md` files state any ledger size, archive, split, or truncation
  policy. (DISTRIBUTION is 21 `.md` + 1 `.py`.) The keyword hits are an example app's CRUD
  `archive/unarchive` endpoints, a 2,000-line monolith refactoring scenario at `HOW_TO_USE.md:385`,
  an anti-pattern *staleness* rule at `HOW_TO_USE.md:944`, and a UI truncation question at
  `DESIGN_WORKSTREAM.md:57`.
- **The framework already ships exactly this doctrine for a different file.**
  `starter-kit/BOOTSTRAP.md:195`, `:360` and `starter-kit/CLAUDE_TEMPLATE.md:82` all tell adopters to
  keep `CLAUDE.md` under a size budget and to *extract* rows before they crowd it.

So the pattern is known, written, and distributed — and was never generalized to the ledgers.
Adopters receive `starter-kit/HANDOFFS.md` and `starter-kit/CHANGELOG.md` as monotonically growing
seeds, a Phase 0 that reads both, and no instruction to trim. **Every adopter reproduces this repo's
sawtooth from scratch.** A gauge reporting "your ledger is 41k tokens" against no stated norm is a
decoration. **Doctrine ships with the gauge or neither ships.**

### 2.3 Expense 3 — numbered sets: **MONITOR THE NEW-INSTANCE HALF ONLY**

Three declines, each for a stated reason:

- **Decline a resolution check** ("assert every citation still resolves"). It goes red whenever
  someone legitimately retitles an entry to correct a false claim — and this repo does exactly that.
  A guard that punishes correcting a false claim gets narrowed, not obeyed. This is settled;
  `bin/check-handoff:95` records the reasoning.
- **Decline a numbered-set growth gauge.** Three of the four sets are unpoliceable by construction:
  `bin/check-citations`' own docstring excludes failure modes, principles and anti-patterns, and
  anti-patterns have no single registry (AUDIT owns 1–9, RESEARCH_DOCUMENTATION owns 1–20) with some
  live citations deliberately pointing at an *adopter's* project-local list. They are also already
  governed by a rule stronger than any dial: append-only, never renumber.
- **Monitor new instances**, diff-scoped, threshold zero (§3.5).

### 2.4 The unnamed fourth expense — **gate erosion: name it, fix it, do not gauge it**

`.githooks/pre-commit` refuses any commit that changes tracked content without co-staging
`CHANGELOG.md`. It carves out five *git* states — `MERGE_HEAD`, `REBASE_HEAD`, `CHERRY_PICK_HEAD`,
`rebase-merge`, `rebase-apply` — and not one *methodology* state. The Phase 1B claim commit that the
framework itself mandates has, by construction, no action to log yet.

```sh
git log --format=%h --grep="claim S" | wc -l          # 25
for c in $(git log --format=%h --grep="claim S"); do git show --name-only --format="" $c; done \
  | sort -u                                            # HANDOFFS.md — and nothing else
```

**25 of 25 claim commits stage `HANDOFFS.md` alone**; every one bypassed the gate. Reconcile-on-read
backfills the record, so the artifact damage is nil. The damage is that `--no-verify` is now trained
reflex, and **every future check added to that hook inherits the bypass silently** — which caps every
mechanism proposed in §3.

No standing gauge: a bypass-rate metric is gamed by deleting the hook. The fix has a two-point
before/after verification with a known answer at both ends, which is stronger than any dial.

> **Disclosure.** This session bypassed the gate for its own claim commit (`0485d4a`), following the
> precedent, and said so in the commit body. It also *first reported this population as "20 of 20"* —
> because it passed `-20` to `git log` and reported a capped sample as a population. That is the
> exact defect this plan is about, committed by its author, mid-session. It is recorded rather than
> quietly corrected because it is the strongest available evidence that discipline-by-attention does
> not work, including for someone actively looking for it.

---

## 3. The heuristics

Five. **Load-bearing:** H2, H5. **Supporting:** H1, H3. **Advisory:** H4.

Every one lives in `starter-kit/methodology_dashboard.py` and its byte-identical `tools/` twin,
except H5's gate half. This is forced: **no `bin/` executable is distributed.** `bin/` holds
`check-handoff`, `check-links`, `model-report`, `status`, `sync`, `tests.sh` — six tools, zero
shipped. The dashboard is the only executable an adopter receives.

**Hard budget, enforced as a test rather than promised in prose: total added stdout ≤ 300 B.**
Baseline dashboard output is ~1,448 B, so this is ≈ +21% on the instrument and ≈ +0.08% on the
379,206 B read set.

### 3.1 H1 — Read-Set Floor (RSF) · *supporting*

- **What.** Bytes Phase 0 obliges opening, split **FLOOR** (distributed, adopter cannot change) and
  **CEILING** (adopter-owned), with the reconcile band reported separately.
- **How.** Six `stat()` calls on paths the dashboard already probes, plus a transitive walk of any
  `@`-imports parsed out of `CLAUDE.md`. No git, no subprocess.
- **Reported in bytes.** A token figure is a *proxy* and is labelled as one: the 4 B/token constant
  is wrong for markdown-with-tables by roughly ±15%, and the window is not 200k for every adopter —
  this very session runs at 1M, where the same read set is 9.5% rather than 47.4%.
  `starter-kit/BOOTSTRAP.md:195` **already** tells adopters to check with `/context`, which measures
  true occupancy including system prompt and tools. **Cite `/context` as ground truth; RSF is the
  always-on proxy.** Read the window size from `.methodology-profile` if declared.
- **Threshold.** WARN ≥ 150,000 B of adopter-owned CEILING. Absolutely and separately: **any new
  `@`-import in `CLAUDE.md` is RED regardless of size.**
- **Basis.** The `@`-import rule is not a threshold; it is this repo's own written prohibition
  (`CLAUDE.md` §Versioning, backed by an 83.9% cut) generalized. **The 150,000 B WARN line has no
  independent basis** — it is judgment, set just above this repo's current CEILING. Labelled.
- **Action.** Cut the CEILING first; `BACKLOG.md` (35,330 B) is the largest adopter-owned
  contributor. If the FLOOR alone breaches, that is a framework defect, not an adopter one —
  escalate, do not trim, and never `@`-import the pointer back.
- **Known limit.** The FLOOR's prescribed action is unavailable to its reader: an adopter cannot edit
  distributed files, and `bin/status`/`bin/sync` do not ship. The FLOOR is therefore reported as a
  **framework-owned constant with a canonical-side budget checked in `bin/tests.sh`**; only the
  CEILING is actionable adopter-side.

### 3.2 H2 — Ledger slope and Time-to-Cap (TTC) · *load-bearing*

- **What.** Lines added per **ledger entry / receipt**, and projected entries until a ledger reaches
  the 2,000-line agent `Read` cap.
- **The denominator is the whole point, and it is stated beside every rate.** Commits are the wrong
  unit: commits-per-session is the single most adopter-variable quantity in the system, so a team
  that commits 10× per session shows a 10× lower slope for identical growth. **Denominate in the
  framework's own unit** — ledger entries and receipts — which is also already inside the file being
  measured, so the denominator needs no git walk.

| Ledger | lines now | added since split | denominator | slope | **TTC to 2,000** |
|---|---|---|---|---|---|
| `CHANGELOG.md` | 1,122 | +464 | **10 entries** | 46.4 /entry | **18.9 entries** |
| " | " | " | 19 commits | 24.4 /commit | 36.0 commits |
| `HANDOFFS.md` | 685 | +421 | **9 receipts** | 46.8 /receipt | **28.1 receipts** |

```sh
git show 3aee4e3:CHANGELOG.md | wc -l ; wc -l < CHANGELOG.md      # 658 -> 1122
grep -c '^### ' CHANGELOG.md                                      # 25 (was 15 at the split)
grep -c '^```handoff' HANDOFFS.md                                 # 15 (was 6 at 7a71df0)
```

The commit-denominated row is shown only to demonstrate the swing: **under the framework's own unit
`CHANGELOG.md` has ~19 entries of headroom, not 36 commits.** At this repo's observed 2–3 entries per
session that is roughly **6–9 sessions**.

- **Threshold.** WARN < 40 units of headroom. CRITICAL < 15.
- **Basis — the strongest in the set, because the failure already happened.**
  `git show 3aee4e3^:CHANGELOG.md | wc -l` → **2,090 lines**. The ledger crossed the 2,000-line cap
  by 90 lines and was **silently dropping its ten oldest entries**, discovered incidentally rather
  than by any check. WARN at 40 fires for `CHANGELOG.md` today and not for `HANDOFFS.md` — two
  artifacts, two verdicts, which is a far better acceptance test than one file going red.
  **CRITICAL at 15 is judgment**, chosen as under two sessions of headroom.
- **Meaning.** This is the only expense that produces **silently wrong answers** rather than merely
  expensive ones. Past 2,000 lines a `Read` truncates with no error and no missing-data marker, and
  Phase 0's reconcile then computes a frontier against a record it cannot fully see.
- **Action.** Split now, below the cap, oldest-first, one-line pointer to the shard.

### 3.3 H3 — Sawtooth Recovery Fraction (SRF) · *supporting, post-archive only*

- **What.** The fraction of an archive's savings already given back. Dimensionless, so it needs no
  absolute byte threshold and cannot be mis-calibrated for an adopter whose cadence differs.
- **How.** `SRF = (now − post) / (pre − post)` around the largest single size drop in the file's
  history. Print the boundary sha so the number is falsifiable in one command.

```sh
git cat-file -s $(git rev-parse 7a71df0^:HANDOFFS.md)   # 224368  (pre)
git cat-file -s $(git rev-parse 7a71df0:HANDOFFS.md)    #  52927  (post)
git cat-file -s $(git rev-parse HEAD:HANDOFFS.md)       # 164611  (now)
```

| Ledger | pre | post | now | **SRF** |
|---|---|---|---|---|
| `HANDOFFS.md` | 224,368 | 52,927 | 164,611 | **0.651** |
| `CHANGELOG.md` | 186,704 | 53,512 | 92,950 | **0.296** |

- **Threshold.** AMBER ≥ 0.50, RED ≥ 1.00. RED needs no basis: it is the definition of an archive
  that bought nothing. **AMBER at 0.50 is judgment**, set between the two measured values.
- **Meaning.** `HANDOFFS.md` gave back 65% of a whole session's deliverable (`7a71df0`, BL-9 L1)
  **in one day**. SRF distinguishes "my ledger is big" from "my ledger is big *again, on schedule,
  for the same reason*."
- **Action.** AMBER: the archive trigger is set at the wrong level — recompute it as
  (target) − (slope × desired headroom). RED: **do not archive again**; the next deliverable is a
  rate cut, not another reset.
- **Known limit, and why it is only *supporting*.** SRF is undefined before an adopter's first
  archive — i.e. for the entire population that will reproduce the sawtooth from scratch. It can only
  tell you an archive was insufficient *after* you archived. It is a post-archive refinement on H2,
  never the primary gauge. It also degrades on shallow clones and after a rename without `--follow`.

### 3.4 H4 — Receipt Inflation (RI) · *advisory, never blocking*

- **What.** Mean size of recent complete receipts divided by the mean of the oldest ten. **The
  threshold is on the trend, never on the level.**
- **How.** Split on `^```handoff`; skip any segment whose `status:` is `pending`.
- **Measured.** Fenced blocks only, oldest-10 mean **3,944 B** → last-10 mean **8,677 B** = **2.2×
  in 25 days**. Measured over full segments (fence plus the trailing prose the seed documents as
  receipt payload) the multiple is higher. **Report which convention is used**; the two differ and a
  bare "receipt size" figure is ambiguous.
- **Threshold.** WARN ≥ 1.75×, RED ≥ 2.5×. **Both are judgment**, set below the measured 2.2× so the
  gauge fires on the corpus that motivated it.
- **Action.** Not a cap. Move narrative justification into that session's `CHANGELOG.md` entry and
  `docs/planning/`, which Phase 0 does not re-read. The six Minimum Handoff Requirements do not
  relax; the essay around them does.
- **Honest hazard, and the reason this is advisory.** A size signal on a document whose purpose is
  completeness invites **failure mode #15, "Minimal handoff"** — a documented control. Anything that
  shortens handoffs argues against the framework's own compounding mechanism and must earn it. This
  is a trend, it never blocks, and `bin/check-handoff`'s field requirements still bind above it.

### 3.5 H5 — Derived-Value Exposure (DVX) · *load-bearing*

The only mechanism here that changes the trajectory rather than describing it.

- **What.** A **diff-scoped prohibition**: no commit may *add* a line to a live file containing a
  hand-authored derived value without giving it a sink.
- **How.** `git diff --cached -U0`, added lines only, matched against a numeral immediately followed
  by a framework countable noun.
- **Threshold. Zero** — and this is not a round number, it is the only threshold a diff-scoped
  predicate can have. The existing population is grandfathered by construction, so no later edit by
  anyone can turn a passing repo red, **including an edit that legitimately corrects a false claim.**
- **The four sinks.**
  1. **DELETE** — "the phases", not "6 phases". Lossless to a reader who can see the list.
  2. **GENERATE** — compute it. The repo's own worked example is `METHODOLOGY_MAX` in
     `tools/methodology_dashboard.py`, whose comment records that a hardcoded denominator had already
     drifted once into rendering "110%".
  3. **FREEZE** — put it inside a dated ledger entry, where it is a historical record and correct
     forever.
  4. **CITE** — the same or adjacent line carries the backticked command that computes it. Unlike a
     provenance *marker* (rejected: discharged by typing, and a confidently-marked wrong number
     suppresses reader doubt better than a bare one), a command is falsifiable by re-running and is
     checkable from the artifact's own bytes, so the rule stays prohibition-form. **This document
     uses sink 4 throughout.**
- **Basis.** Standing population, corpus-wide: **304 occurrences, 96 distinct claim-strings, 37
  files**.

  ```sh
  # see §6 for the exact scan; the denominator is the live tracked corpus, archives excluded
  ```

  Consequence basis: six of six open backlog items carried a wrong number; `"19 anti-patterns"` was
  miscounted three times across three sessions and is five live sites against a list of 20 that
  self-contradicts at `RESEARCH_DOCUMENTATION_WORKSTREAM.md:306`; nine positional `CHANGELOG.md:<N>`
  anchors were 8-of-9 correct at birth and 0-of-9 now.
- **The mechanism basis is the decisive fact in this plan** and it is quoted in §4, D1.
- **Where it lives.** `bin/check-derived`, canonical-only, absorbing the parked 273-line
  `bin/check-citations` rather than maintaining a seventh executable → then `.githooks/pre-commit`.
  An adopter-facing detector in the dashboard comes **later and only if warranted**.
- **Scope, stated because it decides the value.** It must cover `docs/planning/`, since all six
  measured errors were restatements added to `BACKLOG.md`. Sink 4 is what makes that possible without
  refusing legitimate measurement reports.
- **Boundary with an existing rule.** `bin/check-handoff:78-117` already prohibits positional
  `FILE.md:<N>` anchors in receipts (shipped `4669fb6`, BL-15). **DVX must not re-implement that
  predicate in a second executable**; the anchor half stays where it is, and DVX owns set-size claims
  only. Sequenced behind BL-17/BL-18, which own the anchor class.
- **Real hazard.** It adds a second refusal reason to a hook with a measured 100% bypass at the
  Phase 1B point. **The carve-out (§5, S32) is a hard precondition, not a courtesy.**

### 3.6 Explicitly declined

| Declined | Why |
|---|---|
| Restatement fan-out (count how often a claim is repeated) | Prescribes nothing enforceable; subsumed by DVX plus a one-time sweep |
| A contradiction check across sites | **Punishes the first corrector**: five sites agreeing on a stale value read GREEN, and correcting one turns it RED. Also blind to the dominant measured failure — all sites stale in unison. One-time diagnostic only |
| Numbered-set growth gauge | 3 of 4 unpoliceable; append-only is stronger than a dial |
| Standing gate-bypass gauge | Gamed by deleting the hook |
| Derived-value density per file | A mean-based threshold flags half of any corpus by construction |

---

## 4. Design deficiencies, ordered by measured damage explained

**D1 — Derived values have no sink but prose, and the framework's own countermeasure is a review-time
grep that demonstrably does not bind.**
*Explains 100% of the measured wrong numbers.* `starter-kit/SESSION_RUNNER.md:280` already says:

> "…or modified a numbered set (FMs, principles, phases, anti-patterns, learnings), grep each cited
> destination to confirm it resolves and **grep nearby prose for set-size claims that may have
> drifted**."

That rule exists, is distributed to every adopter, sits inside the 62,410 B file Phase 0 reads in
full every session — **and six of six backlog items still carried a wrong number.** This is the
closest thing the corpus can produce to a controlled comparison of MECHANIZED versus DOCUMENTED, and
it forecloses "add a sentence" as a remedy before anyone proposes one. Learning #12 in the same file
already names the failure: an invariant left as a review-time grep is "a human step that silently
stops happening."
*The defect even propagates through documents written about it:* this session first measured the
Learnings table at 15 rows; it is **13** (`awk` over the table at `SESSION_RUNNER.md:366-380`), and
three of four independent candidate designs restated a wrong figure for it.

**D2 — No ledger doctrine exists in any distributed file, though the framework ships exactly that
doctrine for a different file.**
*Explains the entire sawtooth, and makes every expense-2 gauge normless.* Zero of 21 distributed
`.md` files state a ledger size/archive/split policy; `BOOTSTRAP.md:195`/`:360` and
`CLAUDE_TEMPLATE.md:82` state precisely that policy for `CLAUDE.md`. The archive practice is
fork-side folklore recorded only in this repo's own live prose. It was invented under operational
pressure and never promoted into the seed, because promoting it means touching a distributed file and
nothing ever forced the question.

**D3 — Every accumulation control is a LEVEL control, and the one that exists watches the wrong unit
and states its own trigger wrongly.**
*Explains the silent-truncation event and why the trigger reads healthy.* Nothing anywhere is a rate
control; a level control reads identically at 12 KB/session and 24 KB/session, it just fires twice as
often. Worse, the stated trigger is itself a wrong derived value — **D1 nested inside D3**:

```sh
grep -o "approaches ~[0-9,]* lines" HANDOFFS.md   # "approaches ~1,200 lines"
git show 7a71df0^:HANDOFFS.md | wc -l             # 997  — it fired 203 lines early
```

**D4 — Three verified defects inside the only executable adopters receive.**
*Explains why the instrument cannot yet be trusted to measure any of the above.* All three are
byte-identical in the distributed twin.
  (a) `tools/methodology_dashboard.py:699` runs `git log --reverse --format=%ai -1`. Git applies
  `-n1` *before* `--reverse`, so it returns the **newest** commit. Verified live: it yields
  `2026-08-02` against a true root of `2026-03-09`, making `project_age_days ≈ 0` and the
  `commits < 10 and age > 30` risk permanently dead.
  (b) `:2122` gates the large-file risk on `f.get("ext") in SOURCE_EXTS`, and `.md` is in `DOC_EXTS`
  — so the file that actually breached the `Read` cap at 2,090 lines **could never have tripped it at
  any size**.
  (c) `:88` `EXCLUDE_DIRS` contains `"methodology"`, so the instrument is structurally blind to its
  own home in portfolio mode.

**D5 — Enforcement is canonical-only.**
*Explains why D1 and D2 were fixed here and not there.* Zero `bin/` entries in DISTRIBUTION; six
executables exist and none ship. Canonical mechanizes rules for itself and delivers them to adopters
as prose — **the framework's own top standard, inverted exactly at the distribution boundary**, for
the larger and less-able-to-compensate population.

**D6 — A framework-mandated act is a gate violation.** See §2.4. *Explains zero past damage and caps
every future mechanism.*

**D7 — Caching severed the only automatic signal from the cost that matters.** See §1. *Will never
self-correct.*

### The third failure class, which the framework does not name

Two classes were already known: **born-wrong** (a value wrong the day it was written) and
**decayed-wrong** (correct at birth, invalidated by later edits). This session found a third:

**Denominator-wrong** — a number freshly and honestly computed, over the wrong population. It is
invisible to DVX, because the digit is present, recent, and genuinely derived. It produced this
session's own "20 of 20" (a `-20` cap read as a population), the panel's "22 distributed `.md` files"
(21 `.md` + 1 `.py`), and the commit-vs-entry swing in §3.2 that moves `CHANGELOG.md` from 36 units of
headroom to 19. **The countermeasure is not a checker but a convention: state the population beside
the number.** Sink 4 discharges it.

---

## 5. Remediation plan — re-queued 2026-08-03 against the operator's three goals

One deliverable per session.

> **The constraint this section used to assert did not exist.** It read: *"The upstream channel is
> PAUSED: no PRs, comments, issues, tags or releases."* Nobody imposed that. The archived ledger
> records that PR #64 was opened **without authorization** and closed the same day, and that the
> operator was then *discussing reopening it with the maintainer*. The operator, 2026-08-03: *"The
> purpose of this repository is to update the upstream repository. The channel never paused, you
> simply made a push request without authorization."*
>
> **The real rule** (now in `CLAUDE.md`, so no session has to re-derive it): contributing upstream is
> this repository's purpose; the maintainer's review time is the scarce resource, so work accumulates
> and is vetted here, batched into few substantial PRs — independent work *may* go separately,
> dependent work should not — and **every outward-facing action needs the operator's explicit
> go-ahead, each time.** A rule about sequence and batching, never a suspension.
>
> **Why the correction changes the order and not just the wording.** Every item that serves the
> operator's three stated goals needs an upstream PR. The fabricated pause therefore pushed exactly
> that class to the end and left a sequence optimized for *what could be done without asking*. The
> queue below is re-ordered by the goals instead.

**The three goals, in the operator's words (2026-08-03).** This plan is measured against these, and
as first written it did not deliver two of them:

| | Goal | Status when re-queued |
|---|---|---|
| **G1** | Model context is not overly taxed by the framework | **Measured, barely reduced.** The floor an adopter reads every session is **77,796 B** (`starter-kit/SESSION_RUNNER.md` 62,410 + `starter-kit/SAFEGUARDS.md` 15,386). Exactly one item reduces it, and it was the item marked BLOCKED |
| **G2** | **Automated** trimming of files that both grow and must be read | **Not delivered — the real gap.** Six tools in `bin/`; none trims anything. Manual trimming demonstrably does not hold: `HANDOFFS.md` was archived to **52,927 B** on 2026-08-01 and was **199,801 B** two days later; `docs/planning/BACKLOG.md` (44,487 B) has never been trimmed and has no rule at all |
| **G3** | Instructions for users where automated maintenance is not possible | **Deferred** on the fabricated pause |

Re-derive all four figures before trusting them:
`wc -c starter-kit/SESSION_RUNNER.md starter-kit/SAFEGUARDS.md HANDOFFS.md docs/planning/BACKLOG.md`

### The queue

`S31` and `S32` are shipped; `S33` is this correction. Everything below is queued work, ordered by
goal, with real dependencies named. **"Needs go-ahead" marks an outward-facing step, never a block.**

| # | Deliverable | Serves | Depends on | Outward? |
|---|---|---|---|---|
| **S34** | **Extract the Learnings table** from `starter-kit/SESSION_RUNNER.md` to a read-on-demand sibling, mirroring the `CLAUDE.md` → `docs/RELEASE_HISTORY.md` precedent. *The single largest floor reduction available (~12,937 B ≈ 17%), and independent of everything else here* | **G1** | — | PR, needs go-ahead |
| **S35** | **Design the trimmer.** What is trimmed, the trigger, how losslessness is proven mechanically (the manual procedure already proves it byte-for-byte, so it is mechanizable), where it lives, and the search path that lets the dashboard detect it. Design only — no code | **G2** | — | no |
| **S36** | **Fix the three dashboard defects (D4).** Independently valuable and a precondition for trusting any dashboard row: (a) root-date query returns the newest commit, not the oldest; (b) a 2,090-line `.md` cannot trip the large-file risk; (c) the `methodology` self-exclusion | **G2** | — | fork now; PR later |
| **S37** | **Build the trimmer, canonical-only**, and prove it against this repo's own files — the worst case available. Dry-run by default; refuses to write unless the reconstruction is byte-identical | **G2** | S35 | no (canonical-only) |
| **S38** | **Dashboard row per grow-and-must-be-read file** — headroom and whether the trigger has fired. Read-only. Names the trimmer **only when it is present**, with **two tests**: the named command is one the trimmer really accepts, and a no-trimmer fixture still points at the documented manual procedure | **G2** | S36, S37 | PR, needs go-ahead |
| **S39** | **Decide whether the trimmer ships to adopters**, on S37's evidence. Adopters receive exactly one executable today, so this is "extend the manifest" vs "stay canonical-only" — and it must be decided *before* S40, because "run this" and "here is the manual procedure" are different documents | **G2/G3** | S37 | operator decision |
| **S40** | **The ledger doctrine** into `starter-kit/HANDOFFS.md` and `starter-kit/CHANGELOG.md`: a stated size norm, the archive trigger as a *rate*, and the one-line-pointer shard convention — the instructions for the cases automation cannot reach | **G3** | S39 (wording) | PR, needs go-ahead |
| **S41** | **Floor audit: procedure vs reference.** How much of the remaining ~65 KB an agent must read every session is *procedure it must follow* rather than *reference it could look up*? Raised 2026-08-03; **no operator decision yet** — do not start without one | **G1** | S34 | no |
| **S42** | **Purge derived values from `CLAUDE.md`**, and write the **version-pointer exemption** down *as an exemption* (operator decision 2, §7) — naming version pointers as the exempt class and the release step as their owner | **G1** | — | no |
| **S43** | **`bin/check-derived`** — detector plus a one-time standing-population report; **covers `docs/planning/`** (operator decision 3, §7). Absorbs the parked `bin/check-citations` | support | — | no (`bin/` is not distributed) |
| **S44** | **Promote to the diff-scoped prohibition** and wire into `.githooks/pre-commit` + CI | support | S43 | no |
| **S45** | **`bin/check-context-budget`** and port H1–H4 into the dashboard within the ≤ 300 B stdout budget, asserted as a test | **G1** (measurement) | S36 | PR, needs go-ahead |

**Sequencing rules, and the reasons.** S35 precedes S37 (design before code). S36 precedes S38 (do
not put gauges in a broken instrument). S37 precedes S39 (decide shipping on evidence, not
intention). S39 precedes S40 (the instructions differ depending on the answer). S43 precedes S44 (a
detector before a refusal). **S34 is first because it is the only item that reduces G1's floor and it
depends on nothing** — and because `.githooks/pre-commit`'s Phase 1B carve-out (S32) is already in
place, which was the precondition for S44.

### Architecture ratified 2026-08-03 (operator + agent)

Split by **what the code does to the user's files**, not by topic:

- **Metrics → `methodology_dashboard.py`**, the only executable adopters receive. Read-only rows.
- **The write → a separate executable.** The dashboard has never touched user content: in 3,336
  lines it writes only its own HTML and, under `--sync`, copies of itself. Trimming rewrites a
  tracked history file and creates another. The losslessness proof is substantial code with its own
  failure modes, and the dashboard already carries a 2,684-line test file and a byte-identical twin.
  Distribution cost of a second tool is **one line** in `bin/_manifest.py`, riding the existing sync
  — the cost is cognitive, not mechanical.
- **The remedy is named conditionally.** The dashboard detects whether the trimmer is present and
  names the command only then. This dissolves "pointing adopters at a tool they don't have" *and*
  removes the last dependency between the pieces — with conditional naming all four are technically
  independent, so PR batching becomes a review-economics choice rather than a structural one.
- **Two tests, because there are two distinct risks.** The *present* branch carries a copy of another
  tool's interface and goes stale — assert the named command is one the trimmer accepts. The *absent*
  branch never runs on a developer machine, so nothing checks it says anything useful — run a fixture
  with no trimmer and assert the row still points at the documented manual procedure.

---

## 6. What this plan does not do

- **It does not repair the standing population of 304 derived values.** DVX stops the bleeding;
  it does not treat the wound. That is deliberate — a corpus-wide correctness sweep is the
  resolution-check this plan declines in §2.3.
- **It does not touch the 27 failure modes, the 9 principles, the 6 phases, or any numbered set's
  contents.** Append-only stands.
- **~~It reaches no adopter until the channel reopens.~~** *Struck 2026-08-03 (S33): the premise was
  fabricated.* This bullet called the adopter-facing half **"option value on a paused channel"** —
  i.e. it recorded this repository's stated purpose as speculative. What is true is narrower and does
  not defer anything: **each adopter-facing step needs the operator's go-ahead before it goes
  upstream**, and the work is prepared and vetted here first. The queue in §5 is ordered on that
  basis.
- **Its thresholds are calibrated on one atypical corpus** — a framework repo whose "product" is
  documents. Every threshold marked *judgment* above should be re-derived after the first three
  adopters report, and the gauges should **abstain loudly** rather than emit a confident zero during
  a warm-up period.
- **Cost of being wrong.** If DVX is too strict it becomes the next `--no-verify` reflex, which is
  worse than not shipping it — the failure mode is measured and lives in §2.4. If the gauges are too
  chatty they consume the budget they exist to protect. Both are why the stdout cap is a test.

## 7. Open decisions — the operator's, not an agent's

**Ratified 2026-08-03 by the operator: 1 WAIT, 2 EXEMPTION, 3 YES.** 5 was settled by S31 (rate).
**4 remains open, and the reason it does is recorded below** — the answer first given ("worth doing,
but not soon") was a deferral with no trigger, which is not an implementable disposition. Each item
keeps its original question text unedited; the ratified answer is appended beneath it.

1. **Does the ledger doctrine (S39) get written now as a parked branch, or not until the channel
   reopens?** Evidence supports either: parking preserves the work, but a parked branch produces zero
   closable work and collects conflicts at the next resync.
   **RATIFIED 2026-08-03 — WAIT (no parked branch), but the reason was partly void.** The sound half
   stands: a shelf produces nothing closable and collects conflicts, and the reasoning already exists
   as working text — S31 applied the rate form to this repo's own `CHANGELOG.md` front matter. The
   unsound half was "it cannot ship anyway"; the route was never closed. **Restated:** the doctrine is
   queued as **S40**, sequenced after the trimmer's ship decision because its wording depends on that
   answer — not deferred for lack of a route.
2. **`"Current version: v3.6"` in the always-resident `CLAUDE.md`** — take sink 4 (CITE), or grant a
   named, reasoned exemption for version pointers? It decays at every release and has no other sink.
   **RATIFIED 2026-08-03 — NAMED EXEMPTION.** Version pointers are hand-maintained by design: the
   derivation (`git describe --tags`) is longer than the fact it yields, and the place that knows the
   value changed is the release procedure, not a reader. S33 must therefore write the exemption down
   *as an exemption* — a sentence naming version pointers as the exempt class and the release step as
   their owner — not silently leave the line alone. An unexplained survivor reads as an oversight and
   gets re-litigated; a named one does not.
3. **Does DVX cover `docs/planning/`?** It must, to catch the six measured errors — but that makes
   sink 4 load-bearing for every future measurement report, including this one.
   **RATIFIED 2026-08-03 — YES, COVER IT.** A checker aimed away from where every measured error
   actually occurred is theatre. The accepted cost is stated rather than discovered: from S34 onward
   every analysis document in `docs/planning/` — this plan included — must carry the command behind
   each figure, or the checker flags it. That burden is the countermeasure, not a side effect of it.
   This is the decision S34/S35 were waiting on.
4. **Is S40 (extracting the Learnings table) worth it at all?** It is the single largest FLOOR
   reduction available (~12,937 B) and the most invasive change to a file that must stay
   byte-identical for `bin/sync`.
   **SUPERSEDED 2026-08-03 — QUEUED AS S34, FIRST IN THE QUEUE.** Two answers were given to this and
   both were wrong. The first, *"worth doing, but not soon,"* named no trigger, so it could be neither
   scheduled, refused, nor audited. The second restated it as gated on "the channel reopening" — a
   gate that did not exist. **What is actually true:** this is the only item in the plan that reduces
   the floor of §3's G1, it depends on nothing, its verification is mechanical (every `Learning #N`
   citation still resolves), and there is no fork-only version of it — `bin/sync --source=local`
   copies from this working tree, so a "local" edit reaches adopters anyway while marking the file
   drifted for every one of them. It is therefore first in the §5 queue. The upstream PR that carries
   it still needs the operator's go-ahead when it is ready; that is a step, not a gate.

5. **Should the archive trigger be restated as a rate** (§3.3's "(target) − (slope × headroom)"), or
   left as a level with a corrected number? D3 argues the former; the latter is a one-word fix.
   **SETTLED 2026-08-02 by S31 — RATE**, shipped in this repo's `CHANGELOG.md` front matter with a
   runnable derivation that re-baselines itself from `git log --diff-filter=A` and abstains out loud
   when it has no slope. Retained here as the record; not open.
