# The port-branch byte-identity — adjudicated, and the options costed

**Status: ADJUDICATION. Awaiting the operator's ratification. No remedy is applied by this document.**
S123's deliverable, against the decision S121 recorded as `§6(4)` and S122 carried forward as
`next_steps (a)`, both explicitly marking the options **uncosted**. The Present→Implement gate holds:
nothing is appended, rebuilt, refreshed or frozen until the operator chooses.

> **Declared budget: 35,000 B.** File 35 in `docs/planning/`, which has no ceiling — the same
> instance-of-the-problem this directory always is. Stated rather than discovered.

**Method note.** Five independent read-only probes, four option-costings and three adversarial lenses
were run, then a completeness critic. **All three lenses refuted the ranking as first stated**, and the
critic found both the origin of the confusion and a fifth option nobody had posed. Every load-bearing
number below was re-derived by the author against the working tree after the agents reported it —
**a subagent's figure is a claim until you re-run its command.** Two of their numbers were wrong and
are corrected in place, marked ⚠.

---

## 1. The finding under adjudication

> *"I did not append a row — it would breach the cap **and** break the byte-identity that lets
> `bin/sync` agree from either source."* — S120, `HANDOFFS.md` `next_steps`

S121 refuted the first ground (the cap) and **upheld the second**, recording it at `CHANGELOG.md:261` as
*"correct, load-bearing, and unrefuted … Six refutation lenses missed it; a critic found it. That, not
the cap, is why this session appended no Learning row."*

**Verdict: the second ground is false as well. There is no blocker, and there never was one.**
Three independent measurements refute it, any one of which is sufficient.

---

## 2. Why the blocker is not real

### 2.1 No consumer exists — the identity is asserted, never read

| probe | command | result |
|---|---|---|
| Anything mechanical naming the branch or blob | `grep -rn 'port/framework-learnings-extraction\|b21854cc' bin/ tools/ .githooks/ starter-kit/ workstreams/` | **exit 1 — no matches** |
| Where the name *does* appear | `grep -rl … . --exclude-dir=.git` | 4 files, **all prose**: `CHANGELOG.md`, `HANDOFFS.md`, and two `docs/planning/` |
| CI | `ls .github` | **does not exist** |
| Cross-ref content comparison in the suite | `grep -c 'git show' bin/tests.sh` | **0** |
| Is the port commit reachable from `main`? | `git merge-base --is-ancestor 30ddf26 main` | **not an ancestor** |

Every byte-comparison in the repo is *within the checked-out tree* (`diff -q` in Tests 6/11/19, the
starter-kit↔tools dashboard twins) or against **HEAD's own history** (`local_history_blobs` →
`git log -- <path>`). `git log -- starter-kit/FRAMEWORK_LEARNINGS.md` from `main` returns **35 commits**
and `30ddf26` is **not among them**. No classifier in this repository can see the port branch.

### 2.2 The named mechanism does not exist

`bin/sync`'s *"either source"* is not *"either branch"*:

```
bin/sync:17    REPO = "KJ5HST/methodology"
bin/sync:245   p.add_argument("--source", choices=("local", "github"), …)
bin/sync:51    def read_local(...):  return (methodology_root / src).read_bytes()   # the WORKING TREE
bin/sync:93    ["gh", "api", f"repos/{REPO}/contents/{src}"]                        # GitHub, upstream
```

Neither source is a local git ref, and **the port branch is on neither remote** — it is unpushed. A file's
byte-identity between `main` and an unpushed local branch cannot participate in a comparison `bin/sync`
is not able to make.

Worse for the sentence: **the file is absent from `upstream/main` altogether** —
`git cat-file -e upstream/main:starter-kit/FRAMEWORK_LEARNINGS.md` → *"exists on disk, but not in
'upstream/main'"*. The port *adds* it. So `--source=github` already `sys.exit`s on this path today,
which is the standing Test 9 failure every recent receipt names.

### 2.3 The property the sentence claims is already false — and not because of this file

The strongest refutation is the one nobody looked for. Classifying five real adopters exactly as
`bin/sync` does (`git hash-object` per installed file; `history=set()` on the github path, `bin/sync:283`):

| adopter | `--source=local` | `--source=github` |
|---|---|---|
| wsfct | upgradable | **7 tracked MODIFIED → exit 2** |
| chat_verification | upgradable | **7 → exit 2** |
| nprcgenekeepr | upgradable | **7 → exit 2** |
| mts-system | upgradable | **8 → exit 2** |
| vscode_quarto_ext | upgradable | **8 → exit 2** |

> **Author's re-derivation, wsfct:** `current=12, MODIFIED=7, absent-upstream=2` — `SESSION_RUNNER.md`,
> `CLAUDE_TEMPLATE.md`, `BOOTSTRAP.md`, `methodology_dashboard.py`, `ITERATIVE_METHODOLOGY.md`,
> `HOW_TO_USE.md`, `AUDIT_WORKSTREAM.md`. One `modified` TRACKED file aborts the **entire** sync — all
> 26 files, exit 2 (`bin/sync:290-306`).

**The two sources do not agree for any adopter, on seven-to-eight tracked files, today** — before this
decision and after it, whichever option is chosen. *"What lets `bin/sync` agree from either source"*
describes a property this repository does not have.

⚠ **One agent number corrected.** A lens reported *"11 of 24 shared distributed sources differ."* The
count is right; the population is wrong for the use it was put to. **3 of the 11 are `seed`**, which
`bin/sync:287-288` exempts by construction (*"Only TRACKED files can block: SEED files are never
overwritten, so they cannot be 'modified' in the drift sense"*). The blocking-relevant figure is
**8 tracked**. The conclusion survives because 8 > 0.

---

## 3. Where the confusion came from — a real rule about a different pair of trees

This is the most useful finding in the adjudication, and it explains how five sessions reasoned about
"the byte-identity" without anyone tracing it to a consumer.

**Phase 3C does carry a byte-identity requirement.** `starter-kit/SESSION_RUNNER.md:227`, mirrored in
the disputed file's own front matter at `starter-kit/FRAMEWORK_LEARNINGS.md:27`:

> *"Do NOT edit the framework's own learnings table in `FRAMEWORK_LEARNINGS.md` — like this file it is
> synced from canonical and **must stay byte-identical**, or local edits will block future syncs."*

That rule is **correct, mechanically enforced, and about `adopter ↔ canonical`** — an adopter who edits
their installed copy gets `classify_target → "modified"`, and their next `bin/sync` aborts with exit 2.
It has nothing to do with `fork ↔ port`. The instruction it gives is *"don't edit your synced copy"*,
addressed to adopters; it is not *"don't append to canonical"*, and canonical appending is the very
thing the same step orders two lines earlier.

**Five sessions inherited the phrase "the byte-identity" and none opened either copy of the sentence.**

### 3.1 How the blocker got its warrant

`CHANGELOG.md:261` promotes it on this basis: *"Six refutation lenses missed it; a critic found it."*
That is **evidence about six lenses**, recorded as a positive finding about the world. *"Unrefuted"*
became *"correct and load-bearing"* with **no consumer ever named**. `CLAUDE.md` states the governing
rule: *"an unattributed blocker is a defect, not a constraint."* This one is worse than unattributed —
it is attributed, and its whole warrant is that nobody had yet disagreed.

---

## 4. What the hold has actually cost

**Four sessions, not two.** `git log --oneline 364b410..main -- starter-kit/FRAMEWORK_LEARNINGS.md` is
**empty**; the last genuine append is `364b410` (2026-08-27, S119). S120 abstained on both grounds, S121
and S122 on this one, and **S123 as scoped is the fourth**.

**A held row is downgraded, not deferred.** This repo has run the play once already: `b26bb63`
(*"write the five owed sessions' learnings"*) produced **4 rows for 5 owed sessions**, reconstructed
from receipts rather than written in the originating session's live context.

**The blocked thing is worth having — I attacked this hardest and it survived.** A first cut looked
devastating: over the 22 distributed `.md` files, only 8 of 46 rows have an inbound `Learning #N`
citation. That is *denominator-wrong* — rows are cited overwhelmingly from fork-only documents the
distributed net excludes. Over the whole working tree, excluding the table itself and the announcing
ledgers: **29 of 46 rows have a genuine non-ledger citer, and 12 of 46 fire from CODE, TESTS or
CONFIG** — `bin/check-learnings`, `bin/tests.sh`, both dashboard twins, three `tools/test_*.py`,
`starter-kit/context_budget.py`, `.context-budget.json`. **Row #43 is two days old and already fires in
two test files.** S121's *"#46 has zero inbound citations and fired on nobody"* is a true statement
about **one** row that does not generalise; the mature base rate (rows #15–#35) is 12 of 21.

And the file has room: **73,728 − 56,673 = 17,055 B ≈ 14 rows** at the measured 1,182.6 B mean.
It is class `on-demand` in `.context-budget.json` with `max_tokens: null` — read *in part*, never
whole — so under S122's own class gate it takes no token verdict at all. **Nothing about size binds.**

---

## 5. The five options, costed

Costs are **per future session**, for as long as the option stands.

### (i) Append on both branches, keeping them byte-identical — **WEAK**

- **Per session: ~10–12 commands.** The branch is checked out in a dead session's scratchpad worktree,
  so every session first pays `git worktree prune` / `remove --force` before `git worktree add`. Then
  copy, commit, and run the checkers in the second tree.
- **Plus 7 derived numbers per append**, on the port side, by hand. `30ddf26`'s shipped `CHANGELOG.md`
  entry states *"`bin/check-learnings` 0 (46 rows, contiguous 1..46)"*, *"10 of the 46 rows"*,
  *"32 of 46 rows"*, *"the sibling is 56,673 B"*. None is checked by anything.
- **The manifests differ** (main 26 dests, port 25 — `methodology_trim.py` is main-only), so a row
  whose citation resolves on `main` may dangle on the port branch.
- **Silent failure:** a session copies the file, confirms the blobs match, records *"branches in sync"*,
  and ships upstream a verification line reading *"46 rows, contiguous 1..46"* above a 47-row table.
  `bin/check-learnings` validates the **table**, never the ledger prose about the table.
- **It protects nothing.** Its one credited asset — keeping `30ddf26:CHANGELOG.md:93` true — fails,
  because that sentence is false whether or not the blobs match (§2.2).

### (ii) Hold Phase 3C until Phase 5 ships or is abandoned — **REFUTED**

- **Per session: near-zero commands, which is exactly why it keeps winning by default.** It is scored on
  a denominator that hands it the win automatically: the other options cost commands, and what this one
  spends is counted by **no instrument in the repo**. There is no rows-per-session check anywhere.
- **It makes a mandatory *inward* protocol step hostage to an *outward* action no session may trigger.**
  Phase 5 needs the operator's explicit go-ahead, each time. That is the exact shape of the documented
  failure `CLAUDE.md` warns about — a blocker nobody imposed, re-ranking sessions away from the work.
- **Refuted on its premise, its cost, and its value** — §2 kills the premise, §4 prices the cost, and
  the citation measurement kills the "the rows are worthless anyway" defence.

### (iii) Accept divergence and re-run the port's end-to-end `bin/sync` check — **STRONG, with its remedy clause struck**

- **Per session: zero commands, zero commits, zero judgement calls.** Nothing in a session's loop
  touches the port branch. It also *removes* a recurring cost already being paid: S121 and S122 each
  spent a re-litigation of this question and a paragraph of `next_steps` on it.
- **⚠ The named re-run is a ritual with zero discriminating power, and must be struck from the option.**
  `bin/tests.sh` Test 11 diffs `$P/$dest` against `$METHODOLOGY/$src` **in the same tree** — both
  operands move together, so the assertion is content-agnostic by construction. `30ddf26` is untouched
  by an append on `main`, so S120's 113/1 result still describes the branch bit-for-bit. Running it
  costs ~7 minutes and buys assurance the check cannot supply. **A future session must not be able to
  read this option's label and believe the divergence has been checked.**

### (iv) Treat the port branch as derived and rebuild it from `main` at Phase 5 — **STRONG**

- **Per session: zero.** The single recurring obligation is negative and costs no commands — no session
  hand-edits the branch.
- **The rebuild is provably a no-op today:** `30ddf26^` = `upstream/main` = `512c2ed` (unmoved since
  2026-08-11), and the file diff is currently zero bytes.
- **Its real cost is what a refresh imports:** **9 of 46 rows name an artifact absent from
  `upstream/main`**, and 33 of 46 cite a fork session number. A refresh ships those upstream.

### (v) Ship the extraction, not the fork's table — **NOT PREVIOUSLY POSED; belongs to the operator**

Replace the port's copy with the blob `ed22ace` itself created — **13,894 B, 13 rows (#1–#13)** —
verified by the author: `git show ed22ace:starter-kit/FRAMEWORK_LEARNINGS.md | wc -c` → `13894`.

- **It restores the port to its own method.** The other 17 files came from replaying `ed22ace`'s
  per-file patch. **This one file was hand-copied from `main`'s tip** — option (v) removes the sole
  exception; (i)/(iii)/(iv) all preserve it and argue about how to maintain it.
- **A PR titled *"extract the Learnings table"* currently carries 42,779 B — 75.5% of the file — that
  is not the extraction.**
- **It deletes the plan's own headline objection** (§3.1: *"porting alone hands upstream a new over-cap
  file"*). At 13,894 B nothing is over any cap.
- **The divergence question stops existing**: the port's copy is frozen by construction and `main`
  appends freely forever.
- **Cost, honestly:** re-authoring the port's ~5,716 B shipped ledger entry, which is written about a
  46-row table. Paid once, now, against a smaller and stabler set of numbers.
- **It poses a question no option on record asks:** *does upstream receive the fork's 46 accumulated
  learnings, or the extraction mechanism plus the 13 rows that predate the fork's divergence?*
  **That is a PR-content question and it is the operator's.**

---

## 6. Recommendation — two tiers, two different owners

The three lenses converged on one structural correction: **this was never a four-way technical tie.**
It is one session-reachable fact plus one operator-owned PR-content commitment, and publishing two
co-equal "strong" verdicts hides that.

### Tier 1 — the fact, settled by measurement; nothing here is a preference

**The byte-identity is incidental, not a constraint. Phase 3C is not blocked and never was.**
Append on `main`; leave `30ddf26` byte-frozen; do not maintain the identity per session.
This is **common ground between (iii), (iv) and (v)** — every option except (i) and (ii) agrees on it,
so ratifying it does not pre-commit the Phase 5 question.

Mechanics, each with a measured silent-failure mode:

- **The next row is `#48`, not `#47`.** Verified: 46 rows, numbered 1..47, **#14 reserved**, no
  duplicates. A row written `#47` is a duplicate-number failure.
- **It must land inside the table region.** A row after a trailing blank line is invisible to
  `bin/check-learnings`, **which still exits 0**. Acceptance is the checker's printed row count, not
  its exit code.
- **The row budget is 1,500 B** and the file has 17,055 B of headroom.

### Tier 2 — the PR's content, which is the operator's and is NOT ranked here

At Phase 5, what does the port branch carry? Three live answers, with the consequence attached:

| | what upstream receives | what it costs |
|---|---|---|
| **freeze (iii)** | the 46-row table as of 2026-08-27 | `30ddf26`'s three derived counts stay true; upstream's table is N rows behind the fork |
| **refresh (iv)** | the fork's current table | all three counts become false and need hand re-derivation, with no checker; 9 rows name artifacts absent upstream |
| **extraction only (v)** | 13 rows — the blob the ported commit created | re-author the port's ledger entry once; the PR then matches its own title |

**I am not ranking these, deliberately.** They differ only in a decision no session may take, and
§7 of S121's adjudication is the precedent for not dressing an operator choice as a measurement.

### A governance inheritance this document declines to make silently

S121's `§6(4)` wrote: *"(1)–(3) need the operator's choice; **(4) is a precondition**"* — an **agent**
classifying this question as agent-decidable, inside a document whose own line 3 says *"Awaiting the
operator's ratification"*, and `git log` shows **one commit, no ratification recorded since**.
Tier 1 is settled by measurement and I believe it is the session's to act on; **that belief is inherited
from an unratified agent sentence, and it is named here rather than assumed.**

---

## 7. The record to repair

Applying S121's own test — *does the sentence tell a future session what to DO, or record what a past
session FOUND?*

**Live instructions — repair:**

| site | what is wrong |
|---|---|
| `30ddf26:CHANGELOG.md:92-93` | **Ships upstream in the PR.** Declines a ~400 B note because it *"would break the file's byte-identity with the fork, which is what lets `bin/sync` agree from either source"* — false in both halves, and it carries a stale 56,750 B / 77 B derivation. **A standing defect, not a per-option cost.** |
| `docs/planning/phase3c-deadlock-adjudication.md:236` | §6(4) states the options; add the verdict and strike "precondition" |
| `docs/planning/upstream-read-set-pr-plan.md:221` (§5) | Phase 5 needs the two Tier-2 line items named, not an option label |
| the published **229 B** smallest-row floor | ⚠ **It is 228 B.** `check-learnings` budgets `len(raw.encode())` on the raw line; 229 counts the trailing newline. Off by one against the gate that enforces it, and already propagated into three documents. |

**Frozen records — do not rewrite; cite:** `CHANGELOG.md:261`, the S120/S121/S122 receipts.

**One correction owed to S121 in the other direction.** It self-accused of *"a fabricated quotation in a
commit message."* `SESSION_RUNNER.md:228` reads *"record framework-level learnings by appending a new row
to the table"*; the paraphrase was faithful. **A false self-accusation is still a false claim in the
record**, and it should not stand uncorrected.

---

## 8. Reproduction

```sh
# 1. No consumer — exit 1 means no matches
grep -rn 'port/framework-learnings-extraction\|b21854cc' bin/ tools/ .githooks/ starter-kit/ workstreams/

# 2. The mechanism does not exist
sed -n '17p;51,52p;245p' bin/sync                    # REPO, read_local, --source choices
git cat-file -e upstream/main:starter-kit/FRAMEWORK_LEARNINGS.md   # absent upstream
git merge-base --is-ancestor 30ddf26 main            # not an ancestor
git log --format=%H -- starter-kit/FRAMEWORK_LEARNINGS.md | wc -l  # 35, none of them 30ddf26

# 3. The property is already false, for every adopter (read-only)
#    classify each installed TRACKED file against upstream/main with history=set()
#    wsfct: current=12 MODIFIED=7 absent=2  -> bin/sync --source=github exits 2

# 4. The rule that was actually being remembered — a different pair of trees
grep -n 'byte-identical' starter-kit/SESSION_RUNNER.md starter-kit/FRAMEWORK_LEARNINGS.md

# 5. The next row number, and the fifth option's blob
git show HEAD:starter-kit/FRAMEWORK_LEARNINGS.md | grep -oE '^\|\s*[0-9]+\s*\|'   # 46 rows, 1..47, #14 reserved
git show ed22ace:starter-kit/FRAMEWORK_LEARNINGS.md | wc -c                        # 13894
```

---

## 9. What this document does not establish

- **No test was run.** `bin/tests.sh` was not executed; §5(iii)'s claim that it *cannot* fail from
  divergence is read from Test 11's source, not demonstrated by running it.
- **The adopter classification is a simulation of `bin/sync`'s logic, not a `bin/sync` run.** Nothing in
  any adopter repo was touched — `SAFEGUARDS.md:38` governs.
- **No option's Phase-5 cost is verified**, because Phase 5 has not happened and needs a go-ahead.
- **Nothing here licenses an outward-facing action.** No push, no PR, no comment, no tag.
