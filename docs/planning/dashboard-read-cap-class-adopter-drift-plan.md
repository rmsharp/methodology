# The dashboard's declared read-cap class versus an adopter's derived one

**Status:** DECIDED by the session, awaiting the operator's ratification · **S227, 2026-09-27** ·
Fork-side decision document; **Part 1 is upstream-facing and its PR is its own go-ahead.**

Raised by the operator relaying a live discrepancy in `nprcgenekeepr`, with the decision explicitly
delegated: *"investigate and decide what, if anything, to change — this is a design decision for you
to make, not a prescribed fix."* Nothing here is implemented. Every number below was measured this
session by a command named beside it.

---

## 0. The verdict

**The reported drift is real, and it is the symptom rather than the disease.** Two shipped tools decide
the same file's read-cap class by **two different mechanisms** — `methodology_trim.py` **derives** it
from its own `LEDGERS` table plus root position, and `methodology_dashboard.py` **declares** it in a
frozen constant — and the only thing holding them together is a **canonical-only test**. In this
repository they agree and a test proves it. In an adopter that widens `LEDGERS`, the trimmer's answer
moves, the dashboard's cannot, and no test in that tree can notice.

**But the clause that is false is not the class — it is one sentence of prose.** The dashboard's Class B
row asserts *"the trimmer answers `NO_CONFIG` for it"*: a claim about another tool's configuration, in a
tree the dashboard never inspects, emitted as fact. **That sentence is wrong in `nprcgenekeepr` today.**

**And a second defect is larger than the one reported, present in every adopter tree, and owes nothing
to any local patch.** The same row asserts the **backlog-specific** justification — *"a backlog's bottom
items are as live as its top ones"* — for **all four** Class B names, `SESSION_NOTES.md` included. The
module comment eleven lines above the constant **already records that exact over-generalisation as a
caught defect** and states the true, weaker form; the emitted row never received the correction. So the
row text contradicts its own module's comment, in the canonical repository, for every adopter.

**Decision — two parts, and Part 1 stands alone if only one is approved:**

- **Part 1 (primary).** Stop the row asserting what it has not checked. Drop the `NO_CONFIG` clause,
  confine the backlog clause to the backlog names, and state the ordering caveat in the weaker form the
  module comment already settled. **No new mechanism, no derivation, no test distribution** — the
  declared/derived split and both pinning tests are untouched.
- **Part 2 (narrow, optional).** Let the row *add* a remedy it can verify: probe each scanned project's
  own trimmer, and where that project has a config for the file, name the remedy and drop the severity.
  **It derives no class membership**, so dragon 6 is not engaged.

**Rejected:** distributing the pinning tests (Option 1) and adopter-side-only documentation (Option 4).
**Superseded:** an adopter-supplied class override (Option 2). Reasons in §6.

---

## 1. What arrived, what I verified, and what I did not

The relay was treated as a **claim to verify**, not a measurement. Every assertion in it was re-derived.

| Relayed claim | Verdict | How |
|---|---|---|
| The adopter's dashboard is byte-identical to canonical, v2.18.0 | **CONFIRMED** | `diff` against both `tools/` and `starter-kit/` copies; `DASHBOARD_VERSION` read from each |
| Its trimmer carries one documented, unsynced `LedgerSpec` for `SESSION_NOTES.md` | **CONFIRMED** | 51-line `diff` vs `starter-kit/methodology_trim.py`; the patch is labelled `LOCAL ADDITION (nprcgenekeepr, S518, 2026-08-11)` and predicts its own loss at the next overlay sync |
| `--check` returns a full Class-A-style reading and *"trigger does not fire"* | **CONFIRMED** | run in that repo: `57,871 B against a 196,608 B Class A archive threshold`, `[CHECK] trigger does not fire` |
| The dashboard emits a HIGH flag asserting `NO_CONFIG` for that file | **CONFIRMED, with a provenance correction** | see below |
| The size is 56,752 B | **STALE, not wrong** | 56,752 B is what the dashboard recorded at 17:25 today; the file measures **57,871 B** now — it is an active project, and the figure moves |

**The provenance correction the operator supplied mid-session matters, and it makes the finding
structural rather than incidental.** The flag was emitted by **`~/Development/methodology_dashboard.py`**
— the **portfolio-level** copy that scans every project in the parent directory — not by
`nprcgenekeepr`'s own root copy. That copy differs from canonical in **exactly one constant**,
`EXCLUDE_DIRS` (a local scan list); `READ_CAP_CLASS_A`, `READ_CAP_CLASS_B`, `_BACKLOG_LOCATIONS` and
`READ_CAP_BYTES` are byte-identical to `tools/methodology_dashboard.py`.

**So one declared partition is applied across N projects, each carrying its own trimmer.** No
per-repository declaration can be correct for a fleet scanner. This is what supersedes Option 2 and what
forces Option 3 / Part 2 to be **per-scanned-project** rather than "ask the trimmer".

**Not verified, and named as such:** my ordering heuristic for the fleet's `SESSION_NOTES.md` files
compared the first and last of six session numbers and is unreliable on files that interleave
evaluation headings — the `wsfct`, `airqino` and `mts-system` `order=` labels below should not be
relied on. The `## ACTIVE TASK` byte offsets in the same table are robust and are what the argument
rests on.

---

## 2. Root cause — two mechanisms, coupled by a canonical-only test

**The trimmer DERIVES the class.** `starter-kit/methodology_trim.py:947` `is_root_class_a()` returns
true when the file has a `LEDGERS` spec **and** sits at the repository root; `:971` assigns it to
`Trigger.class_a`, which selects the relaxed 196,608 B arm. Its own comment at `:956` says it *"mirrors
methodology_dashboard.py's `read_cap_class()`"* — and that is the whole problem, because it does not
mirror it: one is a lookup in a config table, the other a lookup in a frozen literal.

**The dashboard DECLARES it.** `tools/methodology_dashboard.py:423-424` are frozen sets; `:431`
`read_cap_class()` is a pure path lookup; `:428` derives only the **union**. The comment at `:398`
states the reason plainly: *"Deriving the CLASS from the trimmer would make widening `LEDGERS` silently
reassign a file — exactly what `read-cap-phase-c-plan.md` section 10 dragon 6 says must FAIL rather than
follow."*

**Dragon 6** (`docs/planning/read-cap-phase-c-plan.md:381`): *"Widening the trimmer's `LEDGERS` would
silently move a file's class. Whatever asserts class membership must fail on that, not follow it."*

**It is satisfied only where a test runs.** The two pins —
`tools/test_methodology_dashboard.py:5464` (Class A ≡ `sorted(trim.LEDGERS)`) and `:5485` (every Class B
name must have **no** config) — both call `_load_trimmer()` at `:4314`, which loads **this
repository's** trimmer. `tools/test_methodology_dashboard.py` is **absent from `bin/_manifest.py`**, so
no adopter receives it. In `nprcgenekeepr` the widening therefore neither failed nor followed: **it was
invisible.** The Class B pin's own docstring names this case — *"KILLS: a Class B name that also
acquires a `LEDGERS` entry — the case where the trimmer is widened and this file is not"* — and it does
kill it, in the one tree where it runs.

**Both tools are distributed and both are overlays** (`bin/_manifest.py:44`, `:50`, `TRACKED` —
*"replace with the latest"*). That is why the adopter's patch is fragile by its own admission, and why
Option 4 asks adopters to caveat a file they cannot keep edited.

### 2.1 The classes are conjunctions, and the adopter's file now satisfies neither

`read-cap-phase-c-plan.md` §2 is explicit that membership is *"read off two independent facts, each
machine-checkable: is the name in the trimmer's `LEDGERS` table? and does `SESSION_RUNNER.md` instruct a
read of it?"* The module comment states each class as a conjunction:

- **Class A** = has a `LEDGERS` entry **AND** the protocol consumes it by **frontier** or one record at
  a time, never whole.
- **Class B** = the trimmer answers `NO_CONFIG` **AND** the instructed access path **is the file**, with
  **no remedy the reader can reach**.

In `nprcgenekeepr`, `SESSION_NOTES.md` now has a `LEDGERS` entry (so Class B's first conjunct is false)
and a reachable remedy (so its second is false) — **while `SESSION_RUNNER.md` step 2 still instructs a
whole-file read**, so Class A's second conjunct is false too.

**The file belongs to neither declared class.** The partition is total — A, B, or unwatched — over a
warrant that is two independent bits, so the fourth cell (*trimmable, but read whole*) has no class, no
row text, and no name. `read_cap_class()` must return something, and whatever it returns is wrong.

---

## 3. The measured population — one flag, one project

Every fleet project holding a `SESSION_NOTES.md`, with its own trimmer's answer:

| project | `SESSION_NOTES.md` | trimmer's `SESSION_NOTES.md` config | scanned? |
|---|--:|---|---|
| **nprcgenekeepr** | **57,871 B** | **PATCHED — has a `LedgerSpec`** | yes |
| model_project_constructor | 91,593 B | none | yes |
| wsfct | 489,344 B | none | yes |
| airqino | 33,277 B | none | yes |
| vscode_quarto_ext | 18,088 B | none | yes |
| mts-system | 13,987 B | none | yes |
| Philippians | 12,717 B | none | yes |
| chat_verification | 80,574 B | none | `EXCLUDE_DIRS` |
| church_growth / claude_work / dalia_martinez_funeral / feedback-loop-comparison | 141,083 / 1,093 / 72,485 / 42,748 B | no trimmer | `EXCLUDE_DIRS` |

**`nprcgenekeepr` is the only project in the fleet that has ever widened `LEDGERS`** — 1 of 8 projects
carrying a trimmer. Exactly **one** emitted flag is affected, and it is **1,121 B** over a cap it
crossed within days.

**This bounds the urgency honestly** (the phase-C plan's dragon 7: *a guard can be correct and not worth acting on*). The
reported defect alone would not justify a mechanism. **Part 1 is justified by §4's F3 instead**, which is
fleet-wide and independent of it.

### 3.1 The instructed read target is inside the cap in every measured case

| project | bytes | over cap | `## ACTIVE TASK` at | order (heuristic — see §1) |
|---|--:|--:|--:|---|
| nprcgenekeepr | 57,871 | +1,121 | **9,490** | newest-on-top (confirmed: 796, 795, 794 …) |
| model_project_constructor | 91,593 | +34,843 | **7,473** | newest-on-top |
| wsfct | 489,344 | +432,594 | **132** | unreliable |
| airqino | 33,277 | −23,473 | 132 | unreliable |
| vscode_quarto_ext | 18,088 | −38,662 | 523 | newest-on-top |
| Philippians | 12,717 | −44,033 | 505 | newest-on-top |
| mts-system | 13,987 | −42,763 | **ABSENT** | unreliable |

Every file that has the heading has it at **byte 132–9,490**, far inside `READ_CAP_BYTES` (56,750). The
one file without it is `mts-system` — which the module comment at `:388-391` **already names**. So the
row's *"nothing guarantees the part you need is in the delivered prefix"* is, for the two `SESSION_NOTES.md`
files it actually fires on, delivering the needed part in both cases.

---

## 4. Findings

- **F1 — The reported clause is false, and confined.** *"The trimmer answers `NO_CONFIG` for it"* is
  wrong for `nprcgenekeepr`'s `SESSION_NOTES.md`. One clause, one flag, one project (§3).
- **F2 — The observation came from the portfolio copy, which makes the gap structural.** One declared
  partition, N projects, N trimmers (§1). Supersedes Option 2; forces Option 3 to be per-project.
- **F3 — The larger defect is canonical and owes nothing to the patch.** The Class B row imports the
  backlog-specific justification onto `SESSION_NOTES.md`, which the module comment at `:381-396`
  **already corrected in the comment and not in the row**. Present in every adopter tree. **This, not
  F1, is what justifies changing anything.**
- **F4 — Two shipped tools give the adopter opposite advice about one file.** The trimmer:
  *"trigger does not fire … what truncates is the OLDEST records."* The dashboard: **HIGH**, *"nothing
  guarantees the part you need is in the delivered prefix."* This is BL-66's shape — two distributed
  artifacts, opposite advice — one level up, and the trimmer is the one that is right here.
- **F5 — Dragon 6 holds only where a test runs.** Canonical-only pins cannot constrain an adopter's
  tree; the widening was invisible rather than caught (§2).
- **F6 — BL-32's scope paragraph is now falsified, and I can date it.** It records *"No project in the
  local portfolio has ever extended `LEDGERS` — as reported by the adopter session, not independently
  re-verified."* Independently verified across all 8 trimmer-carrying projects this session:
  `nprcgenekeepr` **has**, since **2026-08-11 — the day BL-32 was raised.** The claim was honestly
  labelled as unverified, which is why finding it cost one command.
- **F7 — and the correction could not be written where the false sentence is.** Recording it in BL-32's
  body was **written, run, and reverted**: that body is among `BACKLOG-DETAIL.md.verify.sh` C2's **frozen
  18**, so the edit turned the losslessness proof RED — `FAIL C2 BL-32: body differs — 5820 B at
  384b17c, 6391 B in detail` — and editing the proof to admit it would be a loosening (`SAFEGUARDS.md`).
  The correction therefore lives in **BL-88's** body, which is not frozen. **A frozen body cannot receive
  a factual correction in place; the correction belongs to the item that found it** — BL-83's append-only
  discipline arriving from the proof side rather than the prose side. Found by running the checker, not
  by predicting it.

---

## 5. Evidence-based inventory (MANDATORY)

`git grep -n 'READ_CAP_CLASS_A\|READ_CAP_CLASS_B\|READ_CAP_WATCHED\|read_cap_class'` — every live site
(archive shards and closed-plan prose excluded; they are frozen records):

| file | hits | role | distributed? |
|---|--:|---|---|
| `tools/methodology_dashboard.py` | 12 | the declaration and its one consumer | canonical copy of a distributed file |
| `starter-kit/methodology_dashboard.py` | 12 | **the distributed twin — must stay byte-identical** | **YES** → adopter root |
| `tools/test_methodology_dashboard.py` | 40 | the two pins and the union/row tests | **NO — canonical-only** |
| `starter-kit/methodology_trim.py` | 2 | `is_root_class_a()`'s comment claiming to mirror it | **YES** → adopter root |
| `docs/planning/read-cap-phase-c-plan.md` | 6 | the governing plan; dragon 6 at `:381` | no |
| `docs/planning/BACKLOG-DETAIL.md` | 4 | BL-51's phases | no |

**Exact anchors for Part 1:** `tools/methodology_dashboard.py:3494` (`cls = read_cap_class(...)`),
`:3510` (the `else:` that is the Class B arm), `:3522` (the `NO_CONFIG` clause), `:3523-3527` (the
imported backlog clause); the comment to reconcile with is `:381-396`; the constants are `:423-424`.
Mirrored into `starter-kit/methodology_dashboard.py` **last** (the phase-C plan's dragon 3). Both copies verified
byte-identical at `760f1d0` with `cmp`.

**Tests that must be extended, not replaced** (the phase-C plan's dragon 4): `tools/test_methodology_dashboard.py:5464`
and `:5485` stay exactly as they are — Part 1 changes no membership. The row-text assertions in the same
file are what move; they must be located and re-pinned before any wording changes, or the change is
unverified.

---

## 6. Options — what each fixes, and what it leaves standing

| # | option | fixes F1 | fixes F3 | new mechanism | verdict |
|--:|---|---|---|---|---|
| 1 | Distribute the two pinning tests | yes | **no** | a distributed suite | **REJECTED** |
| 2 | Adopter-supplied class-override config | yes | no | a config format + loader | **SUPERSEDED** |
| 3 | Probe the trimmer live; reword/downgrade | yes | partly | a per-project probe | **ADOPTED as Part 2** |
| 4 | Adopter-side responsibility, documented | no | **no** | none | **REJECTED** |
| 5 | **Assert only what the row has checked** | yes | **yes** | **none** | **ADOPTED as Part 1** |

**Option 1 — rejected, on three independent grounds.** It would turn a **deliberate, documented**
adopter patch into a permanent red test, punishing a decision that project made on purpose and recorded
in its own `CLAUDE.md`. The suite is 5,867 lines and byte-compares the `starter-kit/` twin — an
assertion with no meaning at an adopter root, which has no `starter-kit/`. And it fixes **none** of F3.
**Kept as a note:** if BL-32 ever ships a supported extension mechanism, a distributed pin belongs
*with* that mechanism, where an adopter's widening is expected rather than surprising.

**Option 2 — superseded by F2, not wrong.** It preserves *declared, not derived* honestly. But the
scanner runs **above** N projects, so one override file is the wrong shape, and a per-project override
duplicates by hand what Part 2's probe reads for free. Revisit only if Part 2 is rejected.

**Option 3 — adopted, narrowed, and the dragon-6 tension dissolved by a distinction.** Dragon 6 forbids
deriving **class membership**. It does not forbid **checking a factual clause before asserting it in
prose**. Part 2 changes only the row's wording and severity; `read_cap_class()` and both constants are
untouched, so a widened `LEDGERS` still turns the canonical pin red and still requires a human to move a
name. **Measured feasibility, this session:** a per-project probe that loads each project's trimmer and
reads `LEDGERS.get(basename)` ran across **12 projects in 0.043 s — 3.6 ms each** — and correctly
returned `True` for `nprcgenekeepr` alone, writing no `__pycache__` (`sys.dont_write_bytecode`, the
discipline `tools/test_methodology_dashboard.py:25` already uses).
**One sub-decision remains open and is the operator's:** the probe may **execute** each adopter's module
(faithful — it reads the *evaluated* config, the independent-operands pattern of fork Learning #16) or
**grep** its source for the spec (safer — no adopter code runs in the scanner, but a source sample
rather than a fact, and *a grep is a sample*). A false negative is harmless — the row stays as it is
today; a false positive names a remedy that does not work. That asymmetry favours executing; the blast
radius of running N adopters' modules inside a shipped scanner favours grepping.

**Option 4 — rejected.** It leaves a prose defect in every adopter tree and asks adopters to document a
caveat about a file `bin/sync` overwrites (`bin/_manifest.py:44`, `TRACKED`). It also inverts the
framework's own rule that a guard must name a remedy its reader can reach.

---

## 7. What the decision deliberately does not change

- **`READ_CAP_CLASS_A` and `READ_CAP_CLASS_B` stay declared literals.** Dragon 6 stands; nothing is
  derived from `LEDGERS`.
- **Both pinning tests stay exactly as written.** Part 1 moves no name between classes.
- **No name is added to or removed from the watched population.** `READ_CAP_WATCHED` stays derived.
- **The trimmer is not touched.** Its derivation is right *for its own question* — having a grammar is
  what makes a file trimmable. The mismatch is not a bug in either tool's logic; it is a bug in one
  tool asserting the other's answer.
- **`nprcgenekeepr` is asked for nothing.** Its patch is sound, documented, and correctly predicts its
  own fragility. **No adopter edit is part of this decision.**
- **Nothing outward-facing happens without a separate go-ahead.** Part 1 touches a distributed file, so
  it is upstream-facing and **its PR is its own go-ahead**.

---

## 8. Phases

### The surface, stated once because it governs every phase

Every criterion below is demonstrated on **this machine, in a `--no-local` clone at the phase's own
commit**, which is this repository's documented build-equivalent surface. **What that surface cannot
enforce:** it cannot prove anything about an adopter tree — the whole subject of this document. Adopter
behaviour is established by **running the changed scanner against the live fleet read-only** and diffing
its emitted rows, which P3 requires and which no test suite substitutes for. It also cannot exercise
GitHub: a merge is the maintainer's, never a phase criterion here.

### P1 — Part 1: the row asserts only what it has checked

**One session.** Rewrite the Class B over-cap row (`tools/methodology_dashboard.py:3510-3528`):
drop the `NO_CONFIG` clause; confine *"a backlog's bottom items are as live as its top ones"* to the
three backlog names; state `SESSION_NOTES.md`'s caveat in the comment's own weaker form — nothing
**enforces** that the needed part is at the top — and name `mts-system`'s heading-less shape as the case
where it fails. Reconcile the row with the comment at `:381-396` so the two can no longer disagree.
Mirror into `starter-kit/methodology_dashboard.py` **last** (the phase-C plan's dragon 3).

- **DONE looks like:** the emitted row for a Class B file contains no claim about any trimmer's config,
  and the backlog clause appears only for backlog names. RED-first: a new assertion pinning the absence
  of the `NO_CONFIG` claim fails before the edit.
- **Verify:** `cmp tools/methodology_dashboard.py starter-kit/methodology_dashboard.py` → identical ·
  `python3 tools/test_methodology_dashboard.py` → the two pins at `:5464`/`:5485` still pass, unchanged ·
  `bash bin/tests.sh` → no regression against the `tests-sh-passed` floor ·
  `python3 starter-kit/quality_ratchet.py --run` → 11/11.
- **Surface:** as above. **Session boundary: this phase is one session. Close out when done.**

### P2 — Part 2: the probe, if the sub-decision in §6 is taken

**One session, and only after P1 has merged or been explicitly decoupled.** Add the per-project probe in
the chosen form; the row gains a remedy sentence and drops to the Class A severity **only** where that
project's trimmer has a config for the file.

- **DONE looks like:** with the probe answering `True`, the row names the remedy and is not HIGH; with it
  answering `False` or failing, the row is byte-identical to P1's output. **The failure path is the
  criterion** — a probe that raises must leave the row exactly as P1 wrote it.
- **Verify:** unit tests for all three probe outcomes (config / no config / load failure) · the two pins
  still green · `bin/tests.sh` · the fleet diff of P3 re-run.
- **Surface:** as above; the load-failure arm is exercised with a deliberately broken fixture trimmer,
  never by waiting for a real one.
- **Session boundary: one session. Close out when done.**

### P3 — the fleet diff, read-only

**Folded into P1 and again into P2, not a separate session.** Run the changed scanner against
`~/Development` read-only and diff every emitted risk row against the current output, confirming the
only changes are the intended ones and that no project's row count moves unexpectedly.

- **DONE looks like:** a row-level diff, in the receipt, naming every changed row and every project.
- **Verify:** the scanner writes to a scratch path, never to `~/Development/dashboard.html`.

### P4 — the upstream PR

**One session, and it needs its own go-ahead.** Branch off `upstream/main`, re-derive the change there
(**a fork-side fix is not an upstream patch**), and open one PR carrying P1 and, if taken, P2.

- **DONE looks like:** the PR open and `MERGEABLE`, its body written in recognised terms — no session
  numbers, no `BL-` codes, no fork-coined names.
- **Verify:** trial-merge into `upstream/main`; run the suite on the merge result, not on the branch.
- **Surface:** GitHub. **What it cannot enforce:** the merge, which is the maintainer's.

> **S230, measured: P4 as written has no target.** `upstream/main`'s dashboard is **2.11.1** and carries none of
> the code P1 and P2 change — `READ_CAP_CLASS_A`, `READ_CAP_CLASS_B`, `read_cap_class`, `find_trim_tool` and
> `collect_trim_metrics` each count **0** in `git show upstream/main:tools/methodology_dashboard.py` — so there is
> nothing to re-derive the change *onto*. BL-88 can reach upstream only inside a PR that first upstreams the
> fork's read-cap class rows. P1 (`cb9b0ed`) and P2 (`161181c`) are shipped fork-side; see BL-88's detail.

---

## 9. Here be dragons

1. **The two dashboard twins must stay byte-identical.** Mirror **last**, then re-measure; a number
   recorded before the mirror is false with nothing failing (the phase-C plan's dragon 3, S37).
2. **`starter-kit/methodology_dashboard.py` is an OVERLAY.** Adopters get Part 1 only when they sync,
   and `nprcgenekeepr`'s trimmer patch is **dropped by that same sync** unless re-added — its own
   comment says so. Landing Part 1 does not fix the fleet; it fixes what the fleet receives next.
3. **Do not "fix" the adopter.** Its patch is the deliberate exercise of BL-32's own leading option. The
   defect is in the tool that asserts its absence.
4. **Part 2 must never lower a severity it cannot justify.** A probe that fails, or a project with no
   trimmer, must produce P1's row unchanged — the failure path is the criterion, not an afterthought.
5. **Dragon 6 is not weakened by Part 2, and the distinction is the whole defence.** Membership stays
   declared; only prose consults the probe. If a future edit lets the probe select the *class*, dragon 6
   is engaged and this document no longer authorises it.
6. **A row-count diff is not a row diff.** Two rows can swap wording at a constant count. Diff text.
7. **BL-32 is adjacent and still undecided.** This document decides what the **dashboard** says, never
   whether the trimmer should ship a canonical `SESSION_NOTES.md` spec. Deciding that would answer
   BL-32, which is a different item with a different blast radius.

---

## 10. Explicitly not in scope

BL-32's open question (a canonical `LedgerSpec` for `SESSION_NOTES.md`, or a supported adopter-extension
mechanism with a sync-survival story) · `CLASS_A_FIRE_BYTES` and every threshold · BL-51's Phases B and C
· the `mts-system` file with no `## ACTIVE TASK` heading, which is a finding about that repo, not this
tool · any edit to any adopter repository · **any outward-facing action beyond P4's own go-ahead.**
