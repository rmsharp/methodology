# PR #82 review — the quality ratchet's file budgets, and what it needs before it binds anything

**Date:** 2026-09-15 (S169). **Status:** a fork-only review. **Nothing here has been posted upstream** —
a comment on #82 is its own go-ahead, each time.
**Subject:** [KJ5HST/methodology#82](https://github.com/KJ5HST/methodology/pull/82), *Quality ratchet —
declared thresholds that bind every actor and only tighten*, head `feat/quality-ratchet` at **`c84e7d96`**,
base `main` at `8b4dc2c3`; 28 files, +1,965 / −34; OPEN, `CLEAN`, 0 comments and 0 reviews when read.
It implements `docs/planning/quality-ratchet-plan.md` on upstream `main` (PR #81; decisions D1–D10).
**Asked by the operator:** *"Look at PR #82 and the way it manages file budgets. Some look to be using
bytes in a way we have recently replaced with better measures of size"* — and any other challenge to what
it proposes.
**Anchors:** a bare `file:line` is on #82's head `c84e7d96`. *Fork* means this fork's `main`; *plan* means
`docs/planning/quality-ratchet-plan.md` on upstream `main`.

---

## 0. The answer

**Two of #82's budgets rest on bytes where tokens at a measured density is the better measure, and the
PR's own numbers show the difference.**

- **`CLAUDE.md`.** #82 paid for its new table rows *"by reduction, not by a raised ceiling"*, against a
  byte pin set at the file's arrival size (59,168 B). It ends 15 B smaller and **62 tokens larger**
  (23,482.5 against 23,420.5, measured). The pin passed a token increase as a decrease. The token figure
  the budget tool prints for this file uses an unmeasured fallback of 2.93 B/token; the file measures
  2.519, so the tool's estimate is 14% low.
- **The runner.** It is budgeted in tokens, which is the right unit, but at a density measured on the
  file *before* #82 edited it. Measured on #82's file, the runner is **18,897.5 of its 18,900 tokens:
  2.5 tokens of room, where the tool reports 22.** The tool would admit about 63 B more growth, which
  measures about 20 tokens over the ceiling the config declares.

And the one size gate that matters, `context_budget.py --status`, is outside the ratchet: it is not a
declared gate, not in the hook, and not run by `bin/tests.sh`.

**Beyond budgets, the ratchet's central claim — thresholds only tighten, for every actor — has three
holes, each demonstrated in a throwaway repository:**

1. **Deleting the manifest passes the hook.** Deleting it and re-adding it with a lower threshold is
   invisible to both the hook and the dashboard.
2. **The manifest this repo declares for itself can report `9/9 pass` over red suites.** Its count gates
   count failing and skipped tests. With `tests-sh-failed` deliberately undeclared, a failing test goes
   unseen once any test is added.
3. **The receipt's gate-run citation is checked for shape only.** `quality_ratchet: 0/9 pass` satisfies
   the lint, and no Phase 0 step performs the comparison the PR describes.

**What holds, verified:** the Phase 0 read-set is budgeted in tokens and a test holds its partition. The
maintainer's figures reproduce exactly. The results hash is deterministic: a clean-clone re-run
reproduced the receipt's `74c773523dab`. And `--precommit` refuses everything it claims to refuse.

**None of this needs a redesign.** Section 6 lists the fixes in rank order; most are a few lines.

---

## 1. Method

| What | Where | Result |
|---|---|---|
| #82's own suites | a `--no-local` clone checked out at `c84e7d96`, verified before running | `bin/tests.sh` **134 passed / 1 failed** (Test 9, *"github source dry-run failed"* — by construction, as the PR says); `quality_ratchet.py --selftest` **17 checks OK**; `--run` **9/9 pass**, `results 74c773523dab · manifest 2424c429b2c6` (the S20 receipt's own figures); `context_budget.py --status` **0**; no tracked file changed by any of them |
| Tokens | the doubled-file Read: double the file, Read it with a spanning `limit`, halve the count the refusal prints | **The instrument was checked first.** Three controls reproduced recorded figures exactly: `main`'s pair **48,555** (recorded 48,555); #82's pair **49,683** (the maintainer's 49,683); `main`'s runner **36,955** (recorded 36,955) |
| Behaviour | seven throwaway repositories under the scratch directory, each holding #82's `quality_ratchet.py` or its whole tree | the results cited in §§3–4; **`docs/planning/pr82-review-repro.sh` re-runs all seven** and prints each result beside this review's |
| Size inventory | every added line of the diff matching a byte, token, ceiling, pin or budget term | the budgets in §2 |

---

## 2. File budgets — the operator's question

| Budget | Unit #82 uses | Basis | Measured at `c84e7d96` | Verdict |
|---|---|---|---|---|
| `CLAUDE.md` — resident, injected every session | **bytes**: `max_bytes` 59,168 (`.context-budget.json:36`) and the resident class total 59,168 (`:23`) | *"PINNED AT ARRIVAL SIZE"* at `cea3068` — no derivation | 59,153 B = **23,482.5 tokens** (`main`: 59,168 B = 23,420.5). Tool: 20,188, at the config's fallback 2.93 (`:9`) | **Wrong unit.** +62 tokens passed as −15 B |
| `starter-kit/SESSION_RUNNER.md` | tokens: `max_tokens` 18,900 (`:46`) at 2.8248 (`:47`), measured on blob `c0550acd` at 52,195 B (`:48`) | read cap minus its sibling | **18,897.5 tokens** (tool: 18,878) | Right unit, stale density: **2.5 tokens of room**, not 22 |
| `starter-kit/SAFEGUARDS.md` | tokens: 6,100 at 2.8191 | read cap minus its sibling | ≈ 5,944 (pair minus runner, derived; tool 5,946) | Holds |
| The Phase 0 pair | per-file token ceilings partitioning 25,000, held by `TestThisRepoReadSetPartition` | the read cap | **24,841.5 tokens, 99.4%** (the #80 merge: 24,277.5) | Holds. #82 spends 564 of the 722.5 tokens that were left |
| `starter-kit/FRAMEWORK_LEARNINGS.md` | **bytes**: `max_bytes` 73,728 (`:62`) | *"the fork's ceiling"* (`:68`), derived for 46 rows at 3.03 B/token | 15,423 B, 14 rows | Stale — carried from #80, not #82's. The fork replaced its own ceiling at S159 |
| Learning rows | bytes: `ROW_BUDGET_BYTES` = 1,500 per row, via the `check-learnings` gate (`.quality-gates.json:56`) | a partial read returns whole rows | Learning #15 is 1,331 B | Pre-existing, and the row is a defensible unit. Low priority |
| `.quality-gates.json` | — | — | **declares no size gate at all** | The budget verdict is outside the ratchet (§2.4) |

### 2.1 `CLAUDE.md` — the pin measured nothing it exists for

`CLAUDE.md` is injected whole into every session, so its cost is tokens per session. The 25,000-token Read
cap does not even apply to it: it is never Read. The pin is 59,168 B because that was the file's size at
`cea3068` (`.context-budget.json:24`, *"a ratchet, not a defended budget"*). #82 added three table rows
and rewrote the tools table; that put the file 984 B over the pin, so it shortened six existing rows and
bullets and closed 15 B under (#82's `CHANGELOG.md`, the S20 entry). The shortened rows lost real
content. The dashboard row lost *"Place in parent directory above project repos. Python 3 stdlib only,
cross-platform."* The test-suite row lost *"so running it generates no `starter-kit/__pycache__`"*.

**Measured in tokens, the trade went the other way: 15 B smaller, 62 tokens larger.** That is not
surprising, because bytes per token is a property of content type. Table rows dense with backticked paths
tokenize at fewer bytes per token than the prose they replaced. A byte pin cannot see that. It is the same
class of error PR #80's review F3 removed from the read-set, when the pair's byte class ceiling became
per-file token ceilings at measured densities.

Two further facts bear on it:

- **The tool judges this file at 2.93 B/token**, the seed's fallback (`--json`: `density_source: config`,
  `ceiling_derived: true`). Measured, it is 2.519. So the tool shows 20,188 tokens where there are 23,482.5,
  and 4,812 tokens of headroom under its derived 25,000 where there are 1,517.
- **87% of the file's bytes are release history**: 51,617 of 59,153 B, from `## Versioning` at `:96` to
  the end. The tokens of that section were not measured separately. The fork moved its narrated history to
  `docs/RELEASE_HISTORY.md` (BL-9 L3, S24: 52,909 → 8,519 B). The fork now budgets `CLAUDE.md` with a
  measured density and a token ceiling: `bytes_per_token` 2.6144, measured 2026-08-29; `max_tokens` 7,114;
  fork `.context-budget.json:26`–`:34`.

**Fix.** Measure `CLAUDE.md`'s density (2.519 at `c84e7d96`) and declare `max_tokens` — a no-growth pin in
tokens, 23,483, if a pin is what is wanted — keeping `max_bytes` only as a coarse backstop. Whether to move
the history out of the always-loaded file is the maintainer's larger decision; the fork's precedent is
there.

### 2.2 The runner — the right unit at the wrong density

The config measured the runner's density on blob `c0550acd` (`.context-budget.json:47`, `:48`). #82 then
edited the file, 52,195 → 53,328 B, and kept that density. Measured on #82's blob, the runner is 37,795 /
2 = **18,897.5 tokens**, a density of 2.8220 against the config's 2.8248. The tool counts
int(bytes / 2.8248) and refuses above 18,900. So it admits growth up to 53,391 B, 63 B more, and at the
measured density that is about 18,920 tokens: **about 20 over the ceiling the config itself declares.**

The safeguard meant for this, `measured_bytes`, warns only when the file drifts 25% from the measured size
(`:49`). Here that is 13,000 B away, against a margin of 2.5 tokens.

**Fix.** Re-measure whenever the file changes near its ceiling, and record 53,328 B at 2.8220. Better,
bind the density to the blob it was measured on, and warn when the blob changes. For anyone editing the
runner after #82 — this fork's BL-57 included (§5) — **every runner edit must now be net-negative in
tokens**.

### 2.3 The Phase 0 pair — 99.4% of the cap, and who pays for it

The pair measures 24,841.5 tokens (#82) against 24,277.5 (`main`). #82 spends 564 of the 722.5 tokens
that were left: 420 in the runner (measured: 18,897.5 − 18,477.5) and about 144 in `SAFEGUARDS.md`
(derived). The runner's new lines — the Phase 3C bullet (`starter-kit/SESSION_RUNNER.md:223`), the Phase 3E
line (`:275`), the FM #17 clause (`:322`) and the new Degradation row (`:365`) — instruct only projects
that declare gates. But the seed ships empty (`starter-kit/quality-gates.json`), so every adopter reads
them every session before declaring anything.

The plan's own argument cuts against placing them there: *"an instruction is paid for on every session; a
gate is paid for only when it fires"* (plan `:139`–`:140`). Keeping the 3E pointer and moving the rest to
the on-demand files would return most of the 420 tokens. The FM #17 clause and the Degradation row are
ratified decisions (plan D8), so that is the maintainer's call. It should at least be a stated cost in the
PR.

### 2.4 The size gate the ratchet does not hold

`python3 starter-kit/context_budget.py --status` is the verdict on every budget above. At `c84e7d96`:

- it is **not** one of the nine gates in `.quality-gates.json`;
- it is **not** chained into `.githooks/pre-commit` — the only new call there is the ratchet, at `:35`;
- `bin/tests.sh` runs its `--selftest` and unit tests (`:607`, `:249`) **but never `--status` on the
  tree**.

So a commit that breaks the read budget passes every gate #82 declares. This fork learned exactly that at
S167: a green suite cannot see a gate it never runs. **Fix — one gate, which passes today (measured, exit
0):**

```json
{ "name": "context-budget", "direction": "max", "threshold": 0,
  "command": "python3 starter-kit/context_budget.py --status",
  "why": "exit code: every declared file and class within its budget" }
```

It is also #82's own rule, from the Phase 3C bullet it adds: *a mechanical invariant is a gate, not a row.*

---

## 3. Defects, demonstrated

Each result below was observed, not predicted. Sections 1–7 of `docs/planning/pr82-review-repro.sh` re-run
them.

### 3.1 Deleting the manifest — the loosest loosening — passes (high)

- **The hook skips.** It runs the ratchet only when the manifest exists in the working tree
  (`.githooks/pre-commit:35`, `[ -f "$top/.quality-gates.json" ]`).
- **The tool also passes it.** It returns clean when the index holds no manifest
  (`starter-kit/quality_ratchet.py:177`).
- **The dashboard is silent.** It returns early when the file is absent
  (`starter-kit/methodology_dashboard.py:1980`). Its history walk (`:1959`) pairs consecutive versions and
  skips any version that fails to parse, and the deletion is exactly such a version.

**Demonstrated (script §1):**

| Step | Exit | |
|---|---|---|
| Control: lower a floor 5 → 4 | 1 | refused |
| The same with `--no-verify` | 0 | |
| Delete the manifest | 0 | passed |
| Re-add it at floor 1 | 0 | *"first manifest commit — nothing to compare against"* |

The dashboard then reports only the 5 → 4 bypass. **The 4 → 1 made by deleting and re-adding is
invisible to every mechanism #82 ships.**

**Fix.**

- In `precommit()`: when `HEAD` carries a manifest with gates and the index carries none, refuse, as
  *"manifest removed"*.
- In the hook: run the ratchet whenever `HEAD` tracks the manifest, not only when the working tree has it.
- In the dashboard: read a deletion as an empty gate set, so every gate reads *removed*.

### 3.2 The hook `install-hook` writes locks an adopter out after a deletion (medium)

The installed hook runs the tool without a guard (`quality_ratchet.py:325`). With no manifest,
`find_root()` fails and the tool exits 3 (`:473`).

**Demonstrated (script §2):** deleting the manifest is refused (exit 1). After the deletion is forced with
`--no-verify`, **every later commit is refused** (exit 1), including an unrelated one. The message, *"no
.quality-gates.json found … refuses to invent thresholds"*, does not name the cause. An adopter who tries
the ratchet and backs out by deleting its manifest can no longer commit without `--no-verify`.

**Fix.** With no manifest in the index: when `HEAD` has none, pass cleanly; when it does, refuse with
§3.1's *"removed"*.

### 3.3 The count gates cannot see failures or skips (high)

**The gates.** Four of the nine gates extract `Ran (\d+) tests`, the number of test methods that exist
(`.quality-gates.json:15`–`:43`). The fifth count gate extracts the passed count of `bin/tests.sh`
(`:12`).

**Demonstrated (script §3): `--run` reports `3/3 pass` and exits 0 over:**

- a suite in which two of three tests fail;
- a suite in which all three tests are skipped;
- a summary reading `134 passed, 1 failed`.

**Why the exception doesn't cover it.** The manifest's own note says green/red is carried by the
passed-count gate (`:21`). That holds only while no test is added: one new passing check offsets one new
failure. The gate that would catch it, `tests-sh-failed ≤ 0`, is deferred until after the merge because
Test 9 fails on the branch (`_first_tightening_owed`, `:3`). That note is an instruction in a JSON comment
— the class of control the plan argues loses to a gate.

**Fix.** Declare `tests-sh-failed` now at `max 1`, the value the branch measures. That is the manifest's
own rule, *"declared at their CURRENT measured values"* (`:2`), and it catches a second failure today.
Tighten it to 0 in the first commit after the merge. Beside each unit-suite count, add an exit-code gate,
so a suite that fails fails its gate.

### 3.4 The gate-run citation is checked for shape, and nothing performs the comparison (high)

**What the lint checks.** `bin/check-handoff` requires a match for `quality_ratchet:\s*\d+/\d+\s+pass`
(`:101`, lint at `:341`).

**Demonstrated (script §6):**

| Newest receipt | Exit |
|---|---|
| As published | 0 |
| Citing `quality_ratchet: 0/9 pass` | **0** |
| Citing nothing | 1 |

**What was promised.** Plan D9 asked for *"a lint that the citation **resolves**"* (plan `:245`). The
comparison #82 describes — *"the next session's Phase 0 reconcile compares the cited `results` hash and
counts against the current `.quality-gates-results.json`"* — is written in the `HANDOFFS.md` seed
(`starter-kit/HANDOFFS.md:165`) and in the PR description. **But the runner's Phase 0, steps 1–8
(`starter-kit/SESSION_RUNNER.md:9`–`:29`), has no such step.** And the results file is gitignored
(`.gitignore:16`), so a fresh clone has nothing to compare against.

**What does work, and it matters.** The results hash leaves out the commit and the timestamp. A re-run on
an unchanged tree reproduces it: the clean clone at `c84e7d96` printed `results 74c773523dab · manifest
2424c429b2c6`, the S20 receipt's own figures. **So the comparison is real whenever someone runs it.**

**Fix.**

- In the lint, which is cheap and local: require `F == 0` and `U == 0`, and `M` equal to the declared gate
  count.
- Put the comparison into Phase 0 as a step; or let `--status --expect <hash>` check a cited hash.
- Otherwise, say in the PR that the citation is checked for shape only.

### 3.5 The dashboard's copy of `compare()` misses two changes the tool catches (medium)

`_gate_loosenings` (`starter-kit/methodology_dashboard.py:1938`) is described as mirroring
`quality_ratchet.compare()` (`quality_ratchet.py:134`), but it reports a changed threshold only when the
direction is unchanged (`:1952`), and it ignores commands.

**Demonstrated (script §4):**

| Change | The tool | The dashboard |
|---|---|---|
| Direction flip, `min 5` → `max 5` | refuses 1 | reports nothing |
| Command swapped for `echo 'Ran 999 tests'` | warns 1 | reports nothing |

Yet the bypass message promises: *"the manifest's git history shows the loosening and the dashboard
reports it as a risk"* (`quality_ratchet.py:171`–`:172`). A `--no-verify` flip, or any command edit,
leaves no advisory.

**Fix.** Report flips as loosenings, and report command or extract changes as *"gate redefined"* (low
severity).

### 3.6 The coverage bonus rewards a gate's name (medium)

**How it works.** The scanner awards +2 testing points when a passing gate's *name* matches `coverage`,
case-insensitively, in a current results file (`:1928`, `:2011`, `:2247`).

**Demonstrated (script §5):** a gate named `coverage` whose command is `echo 100` earns it.

**Why it matters.** Plan D7 lists *"any coverage floor without a faithfulness check beside it"* as not
adopted (plan `:232`–`:234`). The scanner rewards exactly that, and from a locally written, gitignored
file.

**Fix.** Drop the bonus until a faithfulness gate is required beside a coverage gate. Either way, don't
key on names.

### 3.7 `install-hook` in a fresh canonical clone breaks every commit (low)

**Demonstrated (script §7):** `install-hook` exits 0. The next commit fails: *"can't open file
<root>/quality_ratchet.py"*. The canonical repo keeps the tool under `starter-kit/`, and a fresh clone
has no `core.hooksPath`.

`.context-budget.json:2` carries the warning for the identical `context_budget.py` hazard: *"DO NOT RUN
`install-hook` HERE"*. `.quality-gates.json:2` carries none.

**Fix.** Add the same warning. Or have `install-hook` write the path of the file actually running.

---

## 4. Design challenges — argued, not defects

**4.1 "Binds every actor" describes the goal, not the mechanism.**

- **What binds today** is a per-clone, opt-in hook (`core.hooksPath`), bypassable with `--no-verify`.
- **What is missing:** this repository has no CI, as the dashboard's own risk list says.
- **Where the claim is made:** the new section says the mechanical form *"binds every actor: every tier,
  every agent, every human, every session"* (`ITERATIVE_METHODOLOGY.md:405`). The CampusIQ model the plan
  studies enforces its checks before work gets through.
- **The fix:** a CI job running `--run`, plus the ratchet comparison against the base branch. That is
  what binds an actor who never sets a hook. Short of CI, state the enforcement point.

**4.2 Counts as floors are the target the plan warned against.**

- **The plan's own words:** *"'130 checks' is a count, not a target"* (plan `:173`).
- **What the manifest declares:** five of the nine gates are counts. Pruning a dead or duplicated test
  becomes a plan-mode loosening, and skipped tests still count.
- **Suggestion:** prefer exit-code gates for pass/fail, and keep counts advisory — or floor the passed
  count, not the ran count.

**4.3 Nothing tightens the ratchet.**

- **How thresholds move:** only by hand. `--run` shows measured against declared, but never flags slack.
- **The consequence:** a floor of 134 with 150 passing lets 16 tests go without a word.
- **Suggestion:** have `--run` print *"tightening available"* whenever a measurement clears its
  threshold.

**4.4 Where #82 departs from its plan.**

| Plan | #82 |
|---|---|
| §5: the dogfood manifest declares *"`bin/tests.sh` green"* (plan `:272`) | declares a passed count (§3.3) |
| D9: a citation that *resolves* | a citation that is *present* (§3.4) |
| D2: *"≤ ~400 lines"* (plan `:198`) | 495 — trivial |

**4.5 A mislabel.** An exit-code gate that times out or cannot start records exit code 127 as `fail`
(`quality_ratchet.py:57`, `:231`). The module says such a gate *"reports UNMEASURED, never pass"* (`:19`).
Safe, since it never passes, but mislabelled.

---

## 5. What #82 means for this fork

- **BL-57** (`docs/planning/changelog-rules-contradictions-plan.md`):
  - **Conflicts.** P3's `[BL-<N>]` → `[BL-<id>]` and P4's *"prepend"* edit `ITERATIVE_METHODOLOGY.md:294`,
    the same line #82 extends with its clause (c). `CLAUDE.md` already conflicts, since P1's row meets
    #82's rewritten tools table.
  - **Criteria in bytes.** P3's runner criterion (plan `:508`, *"no larger than at P3's start"*) and P4's
    (plan `:538`, *"no larger than at `b82dcff` (52,195 B)"*) are written in bytes. After #82 the runner
    is 53,328 B with 2.5 tokens of real room. **Both criteria should be restated in tokens,** measured by
    the doubled-file Read on the merged tree. The operator's point applies to this fork's own plan.
- **The fork resync.**
  - Once `.quality-gates.json` arrives, `bin/check-handoff` demands a gate citation in this fork's newest
    complete receipt.
  - Upstream's thresholds would be near-meaningless floors here: this fork's suite ran 305 checks at S168,
    against upstream's 134.
  - The two dashboard lineages number their versions independently (the fork 2.17.0, upstream
    2.10.7 → 2.11.0).
- **Learning numbers collide.**
  - Upstream's #15 is the ratchet (`starter-kit/FRAMEWORK_LEARNINGS.md:47`). The fork's #15 is *"Prove
    'nothing lost' over the PARTITION, not the total"* (fork `starter-kit/FRAMEWORK_LEARNINGS.md:47`).
  - Upstream reserves #14 for `docs/operator-gated-review-plan`, an upstream branch (`:20`).
  - So *"Learning #15"* names different rows on the two trees.

---

## 6. If it goes upstream — the asks, ranked

Not posted. Each is small. Every citation is to `c84e7d96`.

1. **Refuse a removed manifest** (§3.1): `precommit()` and the hook's guard; the dashboard reads a deletion
   as *removed*.
2. **Declare `tests-sh-failed` at `max 1` now**, and tighten it to 0 after the merge. Pair each count gate
   with an exit-code gate (§3.3).
3. **Make the citation lint check the counts**, and put the comparison into a Phase 0 step — or say
   "shape only" (§3.4).
4. **Budget `CLAUDE.md` in tokens at its measured density** (2.519) (§2.1).
5. **Re-measure the runner's density** (2.8220 at 53,328 B), and bind densities to blobs (§2.2).
6. **Declare `context_budget.py --status` as a gate** (§2.4).
7. **Mirror direction flips and command edits in the dashboard** (§3.5). **Drop the name-keyed coverage
   bonus** (§3.6).
8. **Warn against `install-hook` in the canonical repo** (§3.7). **Fix the lockout** (§3.2). **Label a
   timeout `unmeasured`** (§4.5).

---

## 7. Not verified

- **CI:** there is none.
- **A real adopter:** `bin/sync` of #82 into a real adopter was not run.
- **The maintainer's fleet delta** — *"27 repos re-scanned under both versions — 0 changed"* — was not
  reproduced.
- **Windows** was not tested.
- **Tokens of `CLAUDE.md`'s history section** were not measured separately from the file.
- **#82 can move.** Every finding is pinned to `c84e7d96`: re-run `docs/planning/pr82-review-repro.sh`
  against the head of the day before relying on one.
