# CHANGELOG.md — archive: 2026-08-02 → 2026-08-02

Retired records from [`CHANGELOG.md`](../../CHANGELOG.md), moved here so the live ledger stays small enough to read
in one pass. Same format, same newest-on-top order — this is the same ledger, continued.

Holds **10 record(s), 2026-08-02 → 2026-08-02**. Cut key: `2026-08-02`. Counts here are computed from the file
itself, never carried forward. This shard is frozen: it states no forward-looking rule,
because the live file owns those and a copy of one was wrong a day after it was written.

---

### 2026-08-02 · [ad hoc] The action ledger split at a day seam, and the archive trigger restated as a rate

**Model:** Claude Opus 5 (1M context).
**S31 of [`framework-context-cost-plan.md`](../../docs/planning/framework-context-cost-plan.md) §5** — its
only time-critical item. Fork-side, canonical-only: the root ledger is not in `bin/_manifest.py`'s
DISTRIBUTION, so no adopter file was touched and no channel was needed. Three operator decisions were
taken before any technical work.

- **The split.** 18 entries (2026-07-27 → 2026-08-01, 726 lines) moved to
  [`docs/archive/CHANGELOG-through-2026-08-01.md`](../../docs/archive/CHANGELOG-through-2026-08-01.md);
  9 kept live. Proven lossless: reversing the one mechanical edit and concatenating shard onto live
  reproduces the pre-split file byte-for-byte, md5 `f5af5eb58b647d1bba5b4c5d9375a38c`, 101,608 B.
  Source-tag audit across live+archives reads **77** before and after. The one mechanical edit: 7
  root-relative links across 5 distinct targets given a uniform `../../` prefix — uniform so the edit
  is invertible and provable.
- **The trigger is now a rate, not a level.** Archive when headroom to the 2,000-line `Read` cap
  divided by growth per ledger entry falls below 15 entries; cut back above 30. Denominated in
  entries — the framework's own unit — not commits-per-session, the most adopter-variable quantity in
  the system. The runnable derivation sits beside it and baselines from `git log --diff-filter=A`, so
  no session hand-writes a split sha. **The level form failed next door:** `HANDOFFS.md` says
  "approaches ~1,200 lines" and its archive fired at 997.
- **The day seam is a labelled departure, not a new default.** BL-9 L2 settled the file axis as
  release frontier; that reasoning stands — the axis was unavailable, not rejected (v3.6 is the
  previous shard's own boundary, no release since). The month seam, measured before being chosen,
  bought 5 entries (994 lines, re-firing within 2–3 sessions) — exactly what BL-9 L2 predicted of
  calendar cuts. The day seam lands at 30.5 entries of headroom, within one entry of the trigger's
  own (independently derived) reset arithmetic. Both shards now say to prefer a release frontier when
  available.
- **Two record repairs, each its own commit** per `starter-kit/SESSION_RUNNER.md:39`/`:42`. `0a1a0d5`
  reconciled S30's `commit:` field to `326094d` (third consecutive discharge). `7f3b7d1` fixed my own
  error from the first repair: the entry was inserted beside its topical sibling instead of prepended.
  Same-date entries make position the file's only ordering signal, which adjacency-by-topic destroys
  silently. Proven content-preserving by comparing the sorted line multiset before/after.
- **The v3.6 shard's front matter was corrected** — its only change since `3aee4e3` created it, no
  dated entry touched. It restated the archive rule, and both halves were wrong one day later (the
  level became a rate; the release axis was unavailable). A frozen file cannot keep a forward-looking
  rule true, so the restatement was replaced by a pointer. Cite, don't restate.
- **BL-20 raised, not fixed** (FM #17). Verifying this session's own split-claim turned up a live
  defect: `bin/model-report`'s Source 1 regex (`bin/model-report:51`) matches only the seed's
  `- **Model:**` list form; this repo writes bare `**Model:**`, so the tool reports "no entries carry
  a **Model:** bullet" against a ledger full of them. Population at `74479df` (frozen so it cannot
  decay): 14 corpus-wide — 9 bare (live) + 5 list (this split's shard) + 0 (v3.6 shard). Drift
  derived, not guessed: last list-only commit `54426cb`, first bare `1298af7`, unbroken since. This
  entry keeps the bare form deliberately so the population stays uniform for whoever normalizes it —
  which also makes it 10 bare / 15 total the moment it was written, so the front matter above states
  no count, only the command.
- **My first count of that population was wrong**, recorded because it is this plan's own thesis. I
  wrote "9 live, 0 in shards" into two front matters from `grep -c '^\*\*Model:\*\*'` — one literal,
  one dialect — and only caught it because `bin/model-report` disagreed with my grep in both
  directions at once. A count is only as good as its net; state the population beside the number.
- **Verified:** `bin/tests.sh` **142 passed / 0 failed** (unchanged — a split adds no assertion);
  `bin/check-handoff` OK; `bin/check-links` OK 83/21; all relative links in all three ledger files
  resolve under a code-span-aware scan (0 broken); no entry demoted below `###`; dashboard 72/100.
  Zero DISTRIBUTION members in the diff.

### 2026-08-02 · [ad hoc] Reconcile-on-read: S30's `commit:` field → `326094d` — third consecutive discharge

**Model:** Claude Opus 5 (1M context).
Reconciled `326094d` (claim stub `0485d4a`) — third discharge, taken before the claim. RED verified
via a synthetic S31 stub on a **scratch copy**.

### 2026-08-02 · [ad hoc] The framework's context cost — adopter heuristics and a remediation plan

**Model:** Claude Opus 5 (1M context).
**A PLANNING session (S30): the plan is the deliverable and nothing was implemented**
(`starter-kit/SESSION_RUNNER.md` §Planning Sessions). Operator-assigned, not a backlog item. Written
to [`docs/planning/framework-context-cost-plan.md`](../../docs/planning/framework-context-cost-plan.md)
(fork-only — absent from `bin/_manifest.py`'s DISTRIBUTION), so no adopter file was touched and no
channel was needed.

- **The question it answers.** Whether accumulated learnings are resident in context or
  read-and-discarded. **Nothing is ever discarded.** `CLAUDE.md` is resident every turn (8,519 B);
  everything else enters on Read and is carried until compaction replaces it with a *lossy summary*,
  degrading line numbers and which-of-two-similar-counts first. Prompt caching cuts the price of that
  prefix (~10%, measured at 91.7% of input in S14) but not its occupancy — **so the budget signal
  that would warn you is the one caching suppresses.**
- **The monitoring verdict — one of the three expenses is DECLINED as framed.** "Coordination
  residue from outward-facing upstream actions" is a *maintainer* cost; an adopter has no PRs, tags
  or releases, so a gauge for it would read zero forever and look like coverage. Its true adopter
  analogue is **record growth**: the finding is a missing *doctrine*, not a missing gauge —
  **zero of the 21 distributed `.md` files state any ledger size/archive/split policy**, while
  `starter-kit/BOOTSTRAP.md:195`/`:360` and `starter-kit/CLAUDE_TEMPLATE.md:82` ship exactly that
  policy for `CLAUDE.md`, so every adopter reproduces this repo's sawtooth from scratch. Expense 1 is
  MONITORED but reframed from bytes-shipped to bytes-Phase-0-obliges-opening; expense 3 is monitored
  only in its new-instance half — a resolution check and a numbered-set growth gauge are both
  declined, with reasons.
- **The decisive finding, and it forecloses "add a sentence" as a remedy.**
  `starter-kit/SESSION_RUNNER.md:280` **already** instructs every session to "grep nearby prose for
  set-size claims that may have drifted" — distributed, in the 62,410 B file Phase 0 reads in full
  every session — yet six of six open backlog items still carried a wrong number. It is the closest
  thing this corpus can produce to a controlled comparison of MECHANIZED versus DOCUMENTED, and
  Learning #12 already names the failure: a review-time grep is "a human step that silently stops
  happening."
- **The sawtooth, measured.** `HANDOFFS.md` was archived from **224,368 B** to **52,927 B**
  (`7a71df0`, BL-9 L1) and stood at **164,611 B** one day later — SRF **0.651**, 65% of a whole
  session's deliverable given back. `CHANGELOG.md` split from **186,704 B** to **53,512 B**
  (`3aee4e3`) and is **92,950 B**, SRF **0.296**. **Every accumulation control the framework has is a
  LEVEL control; nothing anywhere is a rate control.** The stated archive trigger is itself a wrong
  derived value — `HANDOFFS.md` says "approaches ~1,200 lines" and the archive fired at **997**.
- **The denominator matters more than the rate.** Measured in the framework's own unit — ledger
  entries, not commits — `CHANGELOG.md` has **18.9 entries** of headroom to the 2,000-line agent
  `Read` cap, not 36 commits. It crossed that cap once before at **2,090 lines** and was *silently
  dropping its ten oldest entries*, found incidentally — the only one of the three expenses that
  produces silently wrong answers rather than merely expensive ones.
- **Three verified defects in the only executable adopters receive**, all byte-identical in the
  distributed twin: `tools/methodology_dashboard.py:699` runs `git log --reverse --format=%ai -1`;
  git applies `-n1` *before* `--reverse`, so it returns the **newest** commit — measured `2026-08-02`
  against a true root of `2026-03-09`, making `project_age_days ≈ 0` and one risk permanently dead.
  `:2122` gates the large-file risk on `SOURCE_EXTS`, and `.md` is in `DOC_EXTS`, so the file that
  actually breached the `Read` cap could never trip it at any size. `:88` excludes `"methodology"`,
  so the instrument is blind to its own home.
- **Corrections to the record, measured so the next session inherits them right** (items themselves
  NOT edited — separate deliverable, FM #17): the receipt corpus is **33**, not the backlog's nine
  live-voice "32"s. **BL-18**'s "30 anchors, 20 in `key_files`, 1 in `next_steps`" is **28** across 14
  receipts (`key_files` 24, `active_task` 1, `gotchas` 1, `next_steps` 1, `changelog_ref` **0** —
  S29's repair held); its published breakdown was a `CHANGELOG.md`-only slice that missed six bare
  `HANDOFFS.md:<N>` anchors and two whole keys. **BL-18's stated blocker is false**: archive-S4's
  referent is recoverable with zero invention (`git show 6591faa:CHANGELOG.md` line 35 → the
  `Opened upstream issue #55` heading, surviving in the archive shard), and a prefixed replacement
  satisfies `KEY_FILES_RE` while producing no finding. **BL-12**'s "four sites" is **five**.
  **BL-16**'s docstring is at `bin/check-handoff:487`, never at the cited `:301-303` at any tree that
  ever existed. The Learnings table is **13** rows / 12,937 B.
- **A fourth expense the brief did not name: gate erosion.** `.githooks/pre-commit` carves out five
  *git* states and not one *methodology* state, so the Phase 1B claim commit the framework mandates —
  which by construction has no action to log yet — is a gate violation. **25 of 25 claim commits
  stage `HANDOFFS.md` alone and every one bypassed.** Artifact damage nil (reconcile-on-read
  backfills); the damage is that `--no-verify` is trained reflex, and every future check on that hook
  inherits the bypass silently.
- **A third failure class, named here for the first time: *denominator-wrong*** — a number freshly
  and honestly computed over the wrong population, invisible to any derived-value detector because
  the digit is present, recent, and genuinely derived. **This session produced one:** it reported the
  bypass population as "20 of 20" because it passed `-20` to `git log` and read a capped sample as a
  population — recorded rather than quietly fixed, because it is the strongest available evidence
  that discipline-by-attention fails even for someone actively looking for it.
- **Method.** Two workflows, 22 agents, ~2.29M subagent tokens: a 13-agent re-measurement of every
  open backlog item (measure → adversarially refute) at Phase 0, then a 9-agent design panel (four
  forced-different stances → three judging lenses → synthesis → completeness critic). Every
  load-bearing number in the plan was **re-derived by the session lead** rather than relayed; doing so
  corrected the panel twice (it restated a wrong denominator — "22 distributed `.md` files" for 21
  `.md` + 1 `.py` — inside the document arguing never to restate) and corrected the session lead
  twice (the Learnings table row count, and the bypass population above).
- **The plan dogfoods its own rule.** Its thesis: derived values must not be stored as hand-written
  prose, so every derived number in it carries the command that computes it — the **CITE** sink,
  added as a fourth sink because a measurement report can neither delete, generate, nor freeze its
  own findings. All embedded commands were executed and reproduce their stated values.

### 2026-08-02 · [ad hoc] Reconcile-on-read: S29's `commit:` field → `4669fb6` — and the first time the tripwire was *observed* firing

**Model:** Claude Opus 5 (1M context).
Reconciled `4669fb6` (claim stub `7df3c4b`) — second discharge, taken before the claim. **First time
the tripwire was tested against a real receipt** (via a synthetic S30 stub on a **scratch copy** —
both prior discharges had only argued the mechanism was observable, never run it).

### 2026-08-02 · [BL-15] The `changelog_ref` locator-form rule — BL-15 was right, and settling it found a different defect

**Model:** Claude Opus 5 (1M context) — implementation, the 11-agent refute/design/judge workflow,
and this entry.
**Fork-local and canonical-only.** `bin/check-handoff` and `bin/tests.sh` are both absent from
`bin/_manifest.py`'s 22-entry DISTRIBUTION; zero DISTRIBUTION members appear in the diff, verified
by importing the manifest. **No upstream action taken and none authorized** — `gh` read-only,
[issue #65](https://github.com/KJ5HST/methodology/issues/65) untouched.

- **BL-15 was raised correctly; this session's own claim stub was wrong about it.** The stub
  asserted BL-15's *"identical escape in 13 of 32 receipts"* reproduced under no predicate. It
  reproduces exactly: **13 values defer deictically — 12 × `this commit` plus archive-S1's
  `this branch`.** The stub grepped one literal phrasing, reached 12, and stopped one variant short
  (a sampling error already recorded twice). `bin/check-handoff:69-70` names that dialect in
  writing — documented, unused. Three adversarial verifiers refuted two of the session's three
  central claims; every correction was re-derived here first-hand, not relayed.
- **Closed anyway, for a better reason than "wrong."** All 13 name their entry by a quoted `### `
  title before the deferral, and all 13 now carry a real sha as their own `commit:` first token
  because of `7752114`/`6d47624`. Each deferral is a one-hop back-reference to a field the checker
  already guarantees. **BL-14 discharged BL-15 as a side effect** — one field to the left, the same
  week.
- **What settling it found: 9 positional line anchors, and the arithmetic is the argument.**
  **8 of 9 were correct the day they were written; 0 of 9 resolve to their stated referent now.**
  Four land in `CHANGELOG.md`'s front matter above every entry; four land inside an entry written
  the same day this was measured. The cause is not "the ledger is prepend-only" — under strict
  prepending an anchor at `:35` lands on the newest heading forever. The front matter is edited in
  place: the first `### ` moved **35 → 39 → 68**. Published entries are also rewritten mid-file,
  and the v3.6 split moved 50 entries out of the file.
- **The rule is a PROHIBITION, by design.** `changelog_ref` may not carry a root-relative
  positional address into a live ledger — its truth value depends only on the receipt's own bytes,
  so no later prepend, retitle, front-matter edit, or archive split can turn a passing receipt red.
  The rejected alternative — assert every reference *resolves* to a real `### ` heading — goes red
  whenever someone legitimately retitles an entry, and this repo retitles entries to correct false
  claims (`de46858`). A guard that punishes correcting a false claim gets narrowed,
  not obeyed (FM #17). Three judges scored four candidate designs on separate lenses; the
  prohibition won 7/9/9 against 2–6 for the resolution rules.
- **No `blocks[0]` exemption, unlike the answer-slot rule — a load-bearing asymmetry.** BL-14's
  exemption solves a chicken-egg; a prohibition has none, being satisfiable the instant the receipt
  is written. The corpus agrees: S28's second anchor was wrong the day it was written, so
  write-time values are not self-validating.
- **Prefix-aware: three populations look alike, only one is the defect.**
  `starter-kit/CHANGELOG.md:92` cites a distributed template and
  `docs/archive/CHANGELOG-through-v3.6.md:46` cites a shard frozen at write; both stay legal, both
  pinned by controls. Reusing the existing `KEY_FILES_RE` here would have been unsound — it matches
  all three, verified directly.
- **RED-FIRST AGAINST THE REAL CORPUS — the archive measured rather than assumed.** Against the
  unrepaired ledger the new pass returned exactly **9** findings — the same 9 derived independently
  by walking git history — and **0** against the archive shard. **8 mutants, 8 killed, zero
  survivors**, six by NARROWING rather than deletion: drop prefix-awareness, copy the answer-slot
  exemption, narrow to a leading-token match, make `:<N>` optional, report per receipt not per
  anchor, and rename the finding prefix so `nslot()` would silently absorb it.
- **One line deleted for being untestable.** An empty-value skip could not be killed by any
  mutant — an empty string contains no anchor, so the pass was already silent on it. A guard no
  mutant can falsify is a comment that looks like a guard; it is now a comment that says so.
- **Suite 127 → 142.** It also exposed and fixed a real coupling defect in the *previous* session's
  work: Test 25's live assertions keyed on the checker's **exit code** — a union over all three
  passes — so adding this one turned them red against a ledger whose `commit:` fields were all
  correct, reporting an answer-slot failure for a defect in a different field. Both now count their
  own rows.
- **Raised, deliberately not bundled (FM #17):** **BL-17** — the seed offers no locator a
  fork-local session can write (`PR #N`: often none; a short-sha: unknowable at write time), which
  is *why* eight authors invented a line number; plus the stale-title class the prohibition cannot
  see. **BL-18** — the same anchors in `key_files`, 20 of them, where `KEY_FILES_RE` *requires* a
  `path:line` token, and where one archived receipt cannot be repaired without fabricating a
  citation.
</final_entry_full_text>

### 2026-08-02 · [ad hoc] Record repair: nine `changelog_ref` line anchors, and one quoted title that had been stale since the day it was written

**Model:** Claude Opus 5 (1M context).
**Record repair, committed on its own** per `starter-kit/SESSION_RUNNER.md:39`/`:42`; precedent
`7752114` (the nine-`commit:`-field repair, same week). Not S29's deliverable; licenses nothing
further (FM #17). Fork-local, canonical-only: zero `bin/_manifest.py` DISTRIBUTION members in the
diff.

- **The nine anchors** (`changelog_ref` root-relative `CHANGELOG.md:<N>`): S28 (`:70`, `:118`), S27
  (`:68`), S26 (`:68`), S25 (`:68`), S24 (`:39`), S22 (`:35`), S5-2026-08-01 (`:35`), S21 (`:35`) — 9
  tokens across 8 receipts, all in the live `HANDOFFS.md` (archive shard measured clean, not
  assumed). Seven were plain deletions — each already carried a quoted `### ` heading beside the
  number, so removing it lost nothing.
- **8 of the 9 were correct the day they were written. 0 of 9 resolved to their stated referent
  afterwards.** Four now land in `CHANGELOG.md`'s front matter, four inside an entry written today.
  Cause: not the ledger's prepend-only structure (which would leave an anchor at `:35` fixed on the
  newest heading forever) but the front matter itself being edited in place — this file's first
  `### ` moved **35 → 39 → 68** across two such edits, and the v3.6 split moved 50 entries out of the
  file entirely.
- **Two needed more than deletion, disclosed rather than bundled:** S28's `:118` is the corpus's
  only anchor-only referent (no title, no sha) and never worked — at `6d47624` line 118 sat inside
  the BL-14 entry while the repair entry it names began at 122; now named by heading plus
  `7752114`. S5's `:35` was correct at birth, pointing at PR #63's entry — PR #63 is the Learning
  #13 PR (`f9561a4`), confirmed against `d6dd6c9`, the tree where that value first appeared; now
  named by title.
- **One repair outside the shipped rule:** S22's quoted title had been stale since 23 minutes after
  it was written — `de46858` retitled the entry from *"fixed upstream (PR #64)"* to *"fixed on a
  fork branch"* (correcting a false claim) and rewrote four other fields of that same receipt,
  leaving `changelog_ref` alone. Re-quoted here as a judgement call outside the invariant — a
  prohibition on line numbers cannot see a stale title, and pretending otherwise would be the more
  comfortable sentence. General case: BL-17.
- **Derivation, not assumption.** Each anchor's write-time correctness was judged at the tree where
  that value first appeared, found by walking `git log --all --full-history` over both ledger files
  with the checker's own `extract_blocks`/`parse_block`. For 2 of the 8 receipts the `commit:` field
  names the wrong tree: S24's value first appears in `62f191e`, S5's in `d6dd6c9` while its
  `commit:` leads with `c3157e8`, that session's Phase 1B claim stub.
</final_entry_full_text>
</StructuredOutput>

### 2026-08-02 · [ad hoc] Reconcile-on-read: S28's `commit:` field → `6d47624` — the first time the duty was discharged as a duty

**Model:** Claude Opus 5 (1M context).
Reconciled `6d47624` — first discharge, and **the first time this duty was performed as a duty**
rather than remembered by hand (BL-14's base rate: six prior firings, only four deliberate, all in
one 8-hour window, by hand). Taken before the claim so S29 never started from a red suite.

### 2026-08-02 · [BL-14] The `commit:` answer-slot rule — a distributed promise that had no owner and no detector

**Model:** Claude Opus 5 (1M context) — implementation, the design panel, and this entry.

**Fork-local and canonical-only.** `bin/check-handoff` and `bin/tests.sh` are both absent from
`bin/_manifest.py`'s 22-entry DISTRIBUTION; zero DISTRIBUTION members appear in the diff. **No
upstream action taken and none authorized** — `gh` was read-only, and upstream
[issue #65](https://github.com/KJ5HST/methodology/issues/65) stays open and unanswered.

- **The defect S27 nominated and declined to bundle.** `commit:` may legitimately read `pending`
  when written — the receipt ships inside the commit whose sha it would name. The distributed spec
  promises a collector (`starter-kit/HANDOFFS.md:64`, `:78-79`; ratified at
  `docs/planning/close-out-receipt-durable-artifact-plan.md:87`) but no procedure ever assigned it:
  `starter-kit/SESSION_RUNNER.md` Phase 0 step 6 covers undocumented commits, a `CHANGELOG: pending`
  marker, and a missing-or-`status: pending` receipt — never a *complete* receipt whose `commit:` is
  still `pending`. Nothing detected it either: the checker read only `blocks[0]`, and `pending` is
  not a `BARE_PLACEHOLDER`. **This is [Learning #9](../../starter-kit/SESSION_RUNNER.md)'s own remedy —
  gate-on-write AND reconcile-on-read — unapplied to the one sentinel-bearing key that needed both.**
- **Measured, correcting the record three times.** 9 of 32 receipts named no sha in the answer slot
  (not the 7 the literal word `pending` would find — S26 and S25 read `this commit — …`, and **S25
  contained no sha anywhere**). The corpus is **32, not 31**: the claim stub measured the corpus
  pre-claim and classified it post-claim, mixing two trees in one paragraph. The successor-reconcile
  has fired **6 times, only 4 deliberately**, all in one 8-hour window on 2026-07-25 — `7817989` is
  S3 completing its own receipt 2m26s later, not a successor: the practice was never a procedure,
  just one operator, by hand, for one afternoon.
- **The rule, and why it cannot re-create the chicken-egg.** The answer slot is the value's first
  token, and on every receipt except the newest it must be a sha; the newest is exempt positionally,
  without its value ever being inspected — so no close-out receipt can be failed for the deferral the
  plan explicitly permits. Test 25 N3 is that assertion; `bin/tests.sh:366`'s long-standing "`commit:
  pending` is accepted" now holds at ledger scope, not just single-block. Leading-token on purpose:
  it tolerates trailing prose and catches the `this commit` dialect.
- **Red-first ran against the real corpus.** Executed against the pre-repair
  ledger at `fd5d2d8`, the new pass returned exactly **9** — matching the 9 derived independently by
  walking git history. That run also exposed a hole no fixture would have: **"newest" is a property
  of the LEDGER, not of a file.** In a sharded ledger the archive's `blocks[0]` is merely newest *in
  that shard*, so S18 was silently exempt. Hence `--archived`, and Test 25 N5/N5b.
- **8 mutants, 8 killed** — two bought real tests, not just an annotation. `M3` (`fullmatch`→`search`)
  survived the first round because N7's first token is plain `pending` (no sha, so both predicates
  agree); N9 is the fixture that separates them. `M8` (drop the stub skip) drove N10. Also killed by
  narrowing, not only deletion: `M1` (`blocks[1:]`→`blocks[2:]`), `M7` (narrow to literal `pending`),
  `M4`/`M5` (both directions of the exemption), `M6` (absence-as-pass), `M2`.
- **Suite 112 → 127**, including a live-corpus assertion (L1/L1b) that runs the checker against the
  real ledger and archive — every other `check-handoff` assertion uses a `mktemp` fixture, so nothing
  else observed the real file. Precedent: Test 10, which runs `check-links` bare against the real tree.
- **What did NOT ship.** The spec still promises a reconcile no procedure
  assigns. Closing that means either scheduling the duty into `SESSION_RUNNER.md` Phase 0 or deleting
  the promise from the seed — a DISTRIBUTED change, blocked on the paused channel, and the choice
  between the two *is* the deliverable; the shipped detector is agnostic between them, which is why it
  could ship first. Recorded in BL-14 with 7 affected distributed sites. BL-15 (`changelog_ref`, same
  escape, 13 of 32) and BL-16 (the checker's docstring claims this repo has no root ledger) raised, not
  bundled (FM #17).
</final_entry_full_text>

### 2026-08-02 · [ad hoc] Reconcile-on-read repair: nine `commit:` fields that named no sha

**Model:** Claude Opus 5 (1M context). The bulk repair BL-14 came out of; not a per-session
discharge. Nine receipts reconciled at once, each to the commit where its block first read
`status: complete`. Seven carried the literal `pending`: S27→`1298af7`, S22→`6f994ae`,
S21→`36e9195`, S20→`596ff18`, S19→`3737acd`, S18→`8e6f292` (archive), S6→`21fb521` (archive). Two
read `this commit — …` instead: S26→`54426cb`, S25→`3aee4e3` (S25 had no sha anywhere in the field —
the one `pending`-only keying would have missed). **S6 is dual-homed**: authored `21fb521` as
`session: S2` on the since-renamed branch `feat/capability-tiered-review` (an ancestor of both this
fork and `upstream/main`), then renumbered and given its fork-side close-out narrative in the
fork-only merge `ab5b2d6` — the field names `21fb521`, reachable from *both* repos, because naming
`ab5b2d6` alone would recreate the unreachable-reference trap [Learning #13](../../starter-kit/SESSION_RUNNER.md)
exists to prevent; upstream's own copy still reads `session: S2, commit: pending` and is upstream's
to fix, not this fork's. **Shape of the edit**: `status` left untouched on all nine, matching three
prior historical reconciles (`e5638af`, `4e2901f`, `bc2481d`) — `reconciled` is reserved for a
receipt a *later* session reconstructs, none of these are. Verified after: 31 of 32 receipts led
with a sha; the sole exception was S28's own still-open stub. The two archive-housed receipts were
edited too — the archive is frozen content, not a frozen file.

### 2026-08-02 · [ad hoc] `bin/check-handoff` learned the Phase 1B stub schema — the flag advertised a capability the tool never had

**Model:** Claude Opus 5 (1M context) — implementation, both workflows, and this entry.
**Fork-local, canonical-only; no upstream action taken and none is authorized.** Session claimed
`2026-08-01` (`8bd750c`, 23:42 CDT) and closed out after midnight; the receipt keeps `date:
2026-08-01` because session+date is the ledger's identity key and must not shift between Phase 1B
and Phase 3D, while this entry is dated when the work actually shipped.

- **The defect.** `bin/check-handoff --allow-pending` promised, in its docstring and `--help`, to
  accept "a just-written Phase 1B stub." It relaxed only the `status` finding, while every other
  assertion ran at full strength against a document both distributed specs describe as deliberately
  partial (`starter-kit/SESSION_RUNNER.md:91`, "the fields you can fill now"; `starter-kit/HANDOFFS.md:26`,
  "filling what you can").
- **Measured over git history, not the working tree: 21 distinct Phase 1B stubs, 0 passing.**
  Enumerated with the checker's own parser across 63 ledger-touching commits on `--all` refs, keyed
  by session+date (two sequences share this file and both have an S7 and an S8). **Three dialects,
  all rejected:** FLOOR-4 (4 — `da46b19` S8, `65b1e8e` S15, `71ae4a1` S16, `9e93588` S3 — the
  `(session, date, active_task)` triple the spec names, 9 findings each); FORK-11 (14 — S9–S14,
  S18–S20, S22–S26 — both score keys omitted, 2 findings each); **SENTINEL-13 (3 — `c3157e8` S5,
  `a4e2b30` S7, `9c9c39c` S8, all authored by the framework's own maintainer — writing `self_score:
  pending`, 2 findings each).** That third dialect decided the design: the checker's own author, in
  its own home repo, independently reached for the value his tool rejects — ruling out "the
  convention is wrong, just fill the scores in." S26's entry below says "17 distinct sessions,"
  counting only the fork's own prior sessions and correct on its own terms; 21 is the whole
  population, both sequences, at `8bd750c`.
- **Root cause: a fixture, not a missing test.** `bin/tests.sh` has exercised `--allow-pending` since
  `1646773` and been green throughout, because its fixture is `good_handoff | sed 's/^status:.*/status:
  pending/'` — a fully-populated close-out receipt with one word changed, not a stub. **The guard was
  proved; the fixture under it never was.** 21 real stubs failed unnoticed for a month, and it is the
  same lesson this repo already carries in its own receipts.
- **Known since 2026-07-25, recorded four times, fixed now.** `9ebedda` (S12) first wrote *"`bin/check-handoff`
  STILL cannot validate a 1B stub even with `--allow-pending` … do not 'fix' it by inventing
  scores"*; S13, S17/S19 and S26 each recorded it again under FM #17. The standing instruction not to
  invent scores is honoured — no session is asked to fabricate a self-score.
- **The design, ratified by the operator before implementation.** A three-candidate panel scored on
  two lenses picked **status-dispatched schema selection** (16.5/20, zero fatal flaws): a block is a
  stub **iff its own `status` is `pending`** — never because of the flag. Stubs require four keys
  (`session`, `date`, `status`, `active_task`); the other nine are optional-if-absent but validated at
  full strength when present, and a present-but-blank one is its own finding so blanking never
  becomes an escape. `self_score`/`predecessor_score` may carry `pending` inside a stub (extending the
  sentinel `starter-kit/HANDOFFS.md:77-79` already blesses for `commit`/`what_was_done`); the three
  other floor keys may not, since they're knowable at claim time. **The flag's job is unchanged** — it
  still gates exactly one finding, so an unflagged stub still exits 1 and no relaxation can produce a
  false green. **Labelled as ADDED POLICY in the code** — no ratified text enumerates a stub's keys.
- **Why status-dispatch, not the one-line version.** The obvious patch — `required = STUB if
  allow_pending else REQUIRED_KEYS` — is a hole: a `status: complete` receipt missing `gotchas`,
  checked with the flag, returns clean. That receipt is now Test 24's N1.
- **Verified.** `bin/tests.sh` **92 → 112**; new Test 24 written and run **RED first** (three
  unmutated stub fixtures failed with exactly 9/2/2 findings, matching the three dialects). **11
  mutants, 10 killed** — including the naive flag-dispatch, dropping either new guard, letting the
  sentinel escape stub scope, and making the stub branch skip the sha-shape check or the placeholder
  lint. The one survivor is annotated in-code as uncoverable by construction rather than claimed as
  coverage. **All 21 historical stubs now pass (22 with this session's own).** An exhaustive
  **312-case** old-vs-new differential (4 statuses × 13 keys × 3 mutations × 2 flag states) shows
  **zero** behavioural change on the close-out path — nothing that fails today passes after.
  `bin/check-links` OK 83/21 unchanged; **zero `bin/_manifest.py` DISTRIBUTION members touched**,
  verified by importing the manifest.
- **A four-lens adversarial review before commit: 14 findings, 3 survived refutation, all 3 fixed.**
  The sharpest was this session's own thesis recurring one level down: `N2` and `N7` each made a
  *plural* claim ("blank optional key", "floor keys") while sampling exactly **one** key, so
  narrowing either loop to that key passed the whole suite. Two `for` loops and four assertions
  closed it, each then mutation-proved.
- **Commits:** `8bd750c` (claim) · this commit (implementation + close-out). **Session:** S27 ·
  **Not done, deliberately:** no Learnings row (that table lives in a DISTRIBUTED file and the
  upstream channel is paused); no distributed-seed documentation of the stub schema (operator
  decision — the residual is recorded in the receipt); no version event (canonical-only, adopters
  receive nothing).
