# The upstream read-set PR — what it carries, and what it must not claim

**Status: PHASES 1, 2 AND 3 SHIPPED (fork-side, unpushed); 4–5 open.** This plan was S118's
deliverable. **Phase 2** shipped at S119 (`364b410`). **Phase 1** shipped at S120 on branch
`port/framework-learnings-extraction`, cut from `upstream/main` (`512c2ed`) — one commit,
local only, **no PR opened**. **Phase 3** shipped at S129 (`9999410` + `beffbd0`) on `main`,
all four DONE criteria demonstrated. Four of this plan's own numbers were superseded in the
doing, and **§3.4(d) and §3.4(e) each carry a claim S129 refuted**; see §8.
It is scoped by an operator re-aim recorded at `CHANGELOG.md` 2026-08-27 · *"S118 RE-AIM"*.

> **Declared budget: 45,000 B**, so this file is deliverable in one agent `Read` at the settled
> denominator (`READ_CAP_BYTES = 56,750`). It is file 33 in `docs/planning/`, which has no ceiling —
> the same instance-of-the-problem this directory always is. Stated rather than discovered.

---

## 1. The target, in the operator's words

> *"Our goal is to create a PR for upstream that addresses the file management problem we are
> working on."*

and the scoping that produced it:

> *"you are solving two problems and, presently, I am only concerned with one … 1) fixing the
> `methodology` repository's customized files. 2) fixing the files and code that goes to adopters.
> The problem that is most important is to fix the files and code that goes to adopters via
> `https://github.com/KJ5HST/methodology.git`."*

**The product is exactly `bin/_manifest.py`'s `DISTRIBUTION` list and nothing else.** Parse it on the
**SOURCE** column — a bare-filename grep matches the DEST column and returns the opposite answer.
Upstream: **24 rows (19 TRACKED + 5 SEED), 658,788 B.** This fork: **26 rows, 936,867 B.**
Everything else here — the root `.context-budget.json`, `docs/planning/`, `docs/archive/`, `bin/*`,
the root ledgers — reaches no adopter by any route and is out of scope.

**No outward-facing action is authorised by this plan.** `git fetch upstream` was run with explicit
permission and is a read. The PR itself needs the operator's go-ahead, separately, each time.

---

## 2. The baseline, verified 2026-08-27

`git fetch upstream` confirmed `upstream/main` is still **`512c2ed`** (2026-08-11) — unmoved.
`main` is **439 ahead, 1 behind**.

### 2.1 The Phase 0 mandatory read — the number the PR is about

| | upstream | this fork |
|---|---:|---:|
| `starter-kit/SESSION_RUNNER.md` | **65,140 B** | 54,363 B |
| `starter-kit/SAFEGUARDS.md` | 15,386 B | 15,386 B |
| **pair** | **80,526 B** | 69,749 B |
| metered tokens | **28,234 = 112.9% of one read** | 24,597 = 98.4% |
| at the floor (56,750 B) | **over by 23,776 B** | over by 12,999 B |

**Upstream's read set is over on *both* denominators, so no choice of density rescues it.** That is
the strongest sentence available for the PR body, and it is true only of the product — metered, the
*fork's* pair fits with 403 tokens to spare. A design measured against this fork is measured against
the wrong tree.

The adopter's `CLAUDE.md` is added on top and the framework does not own it (no manifest row has
`CLAUDE.md` as a dest; only `CLAUDE_TEMPLATE.md`). Across 11 measured adopters it runs
**2,725 – 43,956 B**, median 20,583.

### 2.2 Nothing is lost by porting — the fork is a strict superset

- `SAFEGUARDS.md` is **byte-identical** on both sides (blob `f0964195…`).
- `SESSION_RUNNER.md` has **identical heading structure** — the symmetric difference of all headings
  is empty in both directions.
- **Exactly three sections differ**, accounting for the −10,777 B to the byte:

| section | upstream | fork | delta |
|---|---:|---:|---:|
| `## Learnings (added by sessions)` | 13,422 | 442 | **−12,980** |
| `## Phase 2: Execute` | 8,923 | 10,900 | +1,977 |
| `## Phase 3: Close Out` | 10,303 | 10,529 | +226 |

- Upstream's **13 inline learnings are byte-for-byte the fork's rows #1–#13** (478/545/418/712/422/
  485/1067/942/1164/1346/1356/2400/1572 on both sides).

So the fork **moved** 12,980 B out of the every-session read into a file that is a superset of what
was moved (44 rows vs 13), and **added** 2,203 B of procedure. Upstream has no content the fork lacks.

**Upstream lacks two whole product files:** `starter-kit/FRAMEWORK_LEARNINGS.md` and
`starter-kit/methodology_trim.py`.

---

## 3. What the PR carries

### 3.1 Port the extraction — the largest win, already built

`ed22ace` (S34) moved the learnings table out of the mandatory read. **It has never shipped.**
Porting it takes upstream **80,526 → 69,749 B**, overage **23,776 → 12,999 B — a 45.3% cut with zero
new authoring.**

**But porting alone hands upstream a new over-cap file**: it creates `FRAMEWORK_LEARNINGS.md`
upstream at 73,483 B, itself 16,733 B past the cap. The trade is still right (bytes move from
read-every-session to read-on-demand), but shipping a file that is over on arrival is the pattern
this PR exists to end. Hence 3.2.

### 3.2 Compact the 20 over-budget rows — the remedy that actually closes the gap

`starter-kit/FRAMEWORK_LEARNINGS.md` is 73,483 B; **44 data rows are 97.3% of it** (1,934 B of
non-row prose is the only part no row-level remedy can reach). **20 of the 44 exceed the 1,500 B row
budget the file's own preamble publishes, by 17,553 B.**

**73,483 − 17,553 = 55,930 B — 820 B UNDER the 56,750 B cap.** Compliance with the framework's own
already-published budget is the only measured remedy that closes the gap. No deletions, no merges,
no abbreviations are required to reach it.

**Two facts make this far cheaper than it looks.**

1. **Of the 20 rows, upstream has only two** — #12 and #13, together **972 B** of the excess. The
   other **18 rows (16,561 B) upstream has never seen**, so they arrive already compliant rather
   than being edited in place. The file's *"append only; do not edit existing rows"* rule is
   genuinely engaged by two rows, not twenty.
2. **The checker cannot currently see any of it.** `bin/check-learnings` scopes `ROW_BUDGET_BYTES`
   to rows **not yet frozen in git HEAD**, so all 44 frozen rows are permanently exempt: it prints
   `0 unfrozen row(s), 0 over 1,500 B` against a table with 20 violators. A guard that cannot fire
   on the population it was written for is the *"unkillable guard"* shape this repo has deleted
   before. **Repairing that scope is part of this PR**, or the compaction has nothing holding it.

**820 B is thin.** The file gains roughly a row per session against a median row of ~1,626 B, so it
re-crosses within a session or two. That is the argument for §3.4 covering this file too.

### 3.3 `ITERATIVE_METHODOLOGY.md` — 68,240 B, needs to shed 11,490 B

Essentially identical upstream (68,247 B), so this is entirely new work. `## The 6 Phases` alone is
**20,796 B = 30%** of the file. Measured proposals total **12,358 B**, which reaches the target —
but three of them do not survive review as written and the PR must not carry them unfixed:

- **`MERGE-EROSION` would lose content.** Prevention #1 (*"Treat the methodology as if you've never
  read it. Every session."*) has **no counterpart** in `SESSION_RUNNER.md` or `SAFEGUARDS.md`; the
  runner's only *"2 minutes"* sentence is **conditional**, this one is unconditional.
- **`EXTRACT-EV-DUPLICATE-PERFTABLE` deletes a unique column.** *"Gaps identified"* exists **exactly
  once in the entire distributed markdown corpus** — inside the block proposed for deletion.
- **Any extraction creates dangling links for hand-installing adopters.** `starter-kit/BOOTSTRAP.md`
  names the manual copy set as exactly *"ITERATIVE_METHODOLOGY.md, HOW_TO_USE.md, workstreams/"* —
  and that file **ships**. A new sibling needs a manifest row *and* that sentence updated, in the
  same commit.

### 3.4 The gate

**Design: per-file ceilings first, then a generalised class total whose ceiling is a partition.**

**(a) The part that needs no Python and is live the moment the config lands.** `precommit()` already
iterates `cfg["files"]`, reads `ceil = spec.get("max_bytes")`, and refuses on
`if ceil and new > ceil and new > old`. Declaring the two files with `max_bytes` makes the gate live
with **zero lines changed**. Its **relative rule is what makes this a ratchet rather than a wall**:
measured over 32 points and 31 steps on the two files, it refuses **29 of 31 growth steps and 0 of 2
reductions** — a commit that shrinks an over-budget pair always passes, so the tool never prevents
its own remedy.

**(b) The aggregate arm, because two per-file ceilings do not sum.** With per-file ceilings alone,
bytes can move from `SAFEGUARDS.md` into `SESSION_RUNNER.md` with both rows green and the Phase 0
read unchanged. This is the plan's Phase 1 — and **it must extend `precommit()` as well as `main()`**,
or it ships an aggregate that reports and cannot gate.

**(c) The ceiling is derived, not picked.** `framework_share := READ_CAP_BYTES − adopter_reserve_bytes`,
asserted at run time. Recommended first ship: `total_bytes = 56,750`, `adopter_reserve_bytes = 0`,
with 28,000 B carried in the config as a documented candidate. **Reserve zero still leaves upstream
23,776 B over** — which proves the reserve is not what causes the shortfall — and raising the reserve
later is a raise in *strictness*, the one direction that never needs an excuse.

**(d) Two shipped defects the gate depends on, both verified by running the code.**

- **`precommit()` measures one byte short.** `run()` returns `p.stdout.strip()`, so
  `len(staged.encode())` gives **54,362** for a file that is **54,363 B**. Fix: size the index and
  HEAD blobs with `git cat-file -s`. *A size gate that miscounts bytes is the wrong thing to build on.*
- **`cfg["classes"]["resident"]` is a direct key access at `:339` and `:892`.** A config without a
  `classes` key raises `KeyError`. Both sites must move together.

**(e) D7(b) is honoured by non-participation.** No change to `READ_CAP_WATCHED`, `read_cap_class()`,
or either dashboard twin. The ceilings live in the canonical root `.context-budget.json`, which is
**not a manifest SOURCE**, so `bin/sync` has nothing to copy; the SEED carries schema documentation
only and declares no total; and at an adopter these two files are `synced[]` entries, which
`check_synced()` never size-checks by its own docstring. **Four independent locks, none of them a
rule someone must remember.**

**Do not port this fork's `.context-budget.json` wholesale.** Its `CLAUDE.md` ceiling of 18,600 B is
calibrated on this fork's 11,064 B file; **upstream's `CLAUDE.md` is 58,652 B**, so importing it
turns the bare run red on day one for an unrelated reason.

---

## 4. What was refuted — three avenues that do not pay

Recorded so no successor re-runs them.

**Removal of rarely-used learnings yields ZERO.** Every candidate died in verification. Deleting
rows #39–#42 makes `bin/check-learnings` exit 1 (*"not contiguous from 1 — missing #39, #40, #41"*),
and **`bin/tests.sh` Test 32 goes red too** — it runs two presence controls asserting
`^check-learnings: OK` and carries **four hardcoded content anchors into the live distributed file**
(rows #11, #12, #13 twice). The census ranked 44 rows for removal without enumerating the file's
non-human readers.

**Abbreviation / tokenisation does not pay, and the measurement is the interesting part.** At the
settled 2.27 floor, the proposed abbreviation's 1,593 B would be *credited* as 702 tokens; metered,
it delivers **170**. **The floor overstates abbreviation by 4.13× while overstating plain deletion by
only 1.23×** — because abbreviation is precisely the operation that lowers B/token. *A floor that is
conservative for prose is anti-conservative for this remedy.* The generous whole-corpus upper bound
is **1,203 B = 0.849%** of the two files. Second, independent kill: fixed-length truncation is **not
injective** over this corpus and silently merges distinct technical terms.

**Example-list truncation is correct in kind and cannot be the mechanism.** The operator's hypothesis
is real — `EX-7`, `EX-5`, `EX-3`, `IM-2` are genuine, ~1,258 B in total. But truncating **every**
comma series of 3+ members in both files — an absurd edit that would gut both — recovers **10,484 B,
7.4% of the two files and 37% of the gap.** The defensible portion falls **22× short**. Any plan
budgeting example truncation as the route to the cap is budgeting against a number nobody measured.

**Merging is real but small, and needs a scheme decided first.** The operator's #7/#8 pair is a
genuine specialisation (row 8 says so verbatim) and one row can carry both countermeasures — but
both rows are already under budget, so the merge nets **303 B**. Total across all clusters: 6,782 B.
**The enabling decision is disposal of the vacated number, and the two schemes are not equivalent** —
proven by running the checker on scratchpad copies. **Reservation** keeps contiguity green but makes
surviving citations dangle: `main()` builds `valid` from existing row numbers only and never adds the
reserved set, so retiring #8 fails on 4 checker-gating citations. **A tombstone row** (~250 B, keeps
the number, redirects to the survivor) keeps contiguity **and** citations green. Use tombstones.

---

## 5. Phases — each one session, each closing at its own STOP

**Phase 1 — Port the extraction. ✅ SHIPPED S120** (`port/framework-learnings-extraction`, 18 files,
1 commit). Its first DONE criterion was **wrong as written** — *"upstream's `SESSION_RUNNER.md`
matches this fork's"* would have carried issue #75's additions and the `Model:` bullet, neither of
which belongs to this port. What was delivered instead: upstream's runner matches this fork's **in
the Learnings region only**, and is 2,168 B smaller overall. Everything else was met — the manifest
row and the file exist, `bin/tests.sh` ran row-for-row against a pristine control (114/0 vs 113/1,
**zero status flips across 111 shared assertions**), and the §7 meter was re-run. **STOP.**

**Phase 2 — Repair the row-budget scope, then compact.** Fix `ROW_BUDGET_BYTES`'s frozen-row exemption
first — driven **RED** against today's 20 violators — then compact. **DONE:** the checker reports 20
violators before and 0 after; the file is ≤ 55,930 B; every `Learning #N` and `[[N]]` citation still
resolves; Test 32's four anchors updated in the same commit. **STOP.**

**Phase 3 — The gate. ✅ SHIPPED S129** (`9999410` step 1, `beffbd0` steps 2–4). In order: the
`blob_bytes` fix and the `KeyError`, then per-file ceilings, then the class total in `main()` **and**
`precommit()`, then the reserve identity. **DONE:** a bare run prints the aggregate row and exits
BREACH; `--precommit` refuses a growth commit and passes a shrink commit; a synthetic third class
totals correctly; `(resident total)` stays byte-identical for the three instrumented adopters.
**Ships to every adopter who syncs.** **All four met — see §8's S129 rows for what the phase found
that this section had wrong, including that "the three instrumented adopters" is named nowhere in
this plan.** **STOP.**

**Phase 4 — `ITERATIVE_METHODOLOGY.md`,** with the three §3.3 defects fixed and `BOOTSTRAP.md`
updated in the same commit as any extraction. **STOP.**

**Phase 5 — Assemble and open the PR.** **REQUIRES THE OPERATOR'S EXPLICIT GO-AHEAD, and approving
this plan is not it.**

> **Two line items Phase 5 must settle, added at S123 (2026-08-29). Neither is session-reachable and
> neither is ranked here** — see [`port-branch-identity-adjudication.md`](port-branch-identity-adjudication.md) §6 Tier 2.
>
> **(a) What table does the port carry?** `main` now diverges from `30ddf26` (Learning #48 landed at
> `dd6ee0f`), and that divergence is **accepted, not a defect** — the byte-identity is incidental and
> nothing reads it (§2 of that document). Three live answers: **freeze** the 46-row table (`30ddf26`'s
> three derived counts stay true; upstream lands N rows behind); **refresh** from `main` (all three
> counts become false and need hand re-derivation with no checker, and 9 of 46 rows name artifacts
> absent upstream); or ship **the extraction only** — the 13,894 B / 13-row blob `ed22ace` itself
> created, after which the PR matches its own title, since it currently carries 42,779 B (75.5%) that
> is not the extraction.
>
> **(b) Rewrite `30ddf26:CHANGELOG.md:92-93` — a standing defect that ships upstream in the PR.** It
> declines a ~400 B note because that *"would break the file's byte-identity with the fork, which is
> what lets `bin/sync` agree from either source."* **False in both halves:** `bin/sync --source` reads
> a working tree or `KJ5HST/methodology`, never a local ref, and the two sources already disagree on
> 7–8 tracked files for every measured adopter. It also carries a stale 56,750 B / 77 B derivation.
> This needs rewriting under **every** option, including freeze.

---

## 6. Here be dragons

1. **The gate binds only someone who chooses to be bound, and the PR must not claim otherwise.**
   `core.hooksPath` is **local git config, never in the repo**. There is **no CI**. `.githooks/` is
   in neither manifest. A framework author on a fresh clone of `KJ5HST/methodology` has *no* gate —
   not a weakened one, none — and nothing in the clone tells them to set one.
2. **The bypass is already a trained reflex, and `.githooks/pre-commit` says so about itself:**
   *"32 of 32 commits in this repo's history whose entire diff is `HANDOFFS.md` alone were refused …
   and every claim among them shipped with `--no-verify`. A gate bypassed 100% of the time at a
   known, mandatory point is not a gate — it is a trained reflex — **and the derived-value checks
   planned for this same hook inherit that reflex unless it is removed first.**"* That is a direct
   warning against the design in §3.4, written before it, and it must be answered in the PR.
3. **The residual hole: bytes moved into a fourth mandatory file.** Split `SESSION_RUNNER.md`, add a
   manifest row, have Phase 0 read both — the aggregate *falls* and nothing fires. Partial
   mitigation: a `bin/tests.sh` case asserting that the adopter-root filenames Phase 0 names as
   read-in-full equal the declared membership. It catches the honest split, not the determined one.
4. **The framework ships a size gate its own procedure never mentions.**
   `grep -n context_budget starter-kit/SESSION_RUNNER.md starter-kit/SAFEGUARDS.md` returns nothing;
   Phase 0 step 5 runs the dashboard. Closing that gap means editing Phase 0, which **grows the very
   file being capped** by ~300 B. An operator decision, made visibly.
5. **`bin/tests.sh` takes ~7 min and EXITS 1 EVEN WHEN GREEN.** Background it, read `$?` bare, never
   through a pipe. Tests 32/34/37 **mutate the live `HANDOFFS.md` and `FRAMEWORK_LEARNINGS.md`** — do
   not measure those files while it runs.
6. **`bin/check-*` are Python with no extension; the two `*.jsonl` go dirty from Phase 0 alone —
   do not `git reset --hard`.** A bare `context_budget.py` run **appends** to a tracked `.jsonl`;
   `--precommit` writes nothing.
7. **Exit codes are tiered `CLEAN/WARN/BREACH = 0/1/2`.** Never assert on a bare run's exit code as a
   success criterion, and never read one through a pipe.
8. **439 commits ahead of upstream.** The PR must be *scoped*, never "merge the fork."

---

## 7. Reproduction

```sh
# the product, from the manifest's SOURCE column — never a bare-filename grep
python3 -c "import sys;sys.path.insert(0,'bin');import _manifest as m;print(len(m.DISTRIBUTION))"

# the Phase 0 pair, both trees
git cat-file -s upstream/main:starter-kit/SESSION_RUNNER.md   # 65,140
wc -c starter-kit/SESSION_RUNNER.md starter-kit/SAFEGUARDS.md # 54,363 + 15,386

# the token meter: doubled file, spanning limit, halve. Returns NO content, costs nothing.
cat A B A B > /tmp/x.txt && wc -l /tmp/x.txt   # then Read /tmp/x.txt offset=1 limit=<lines>

# the 20 over-budget rows and what compliance would buy
python3 -c "import re;rows=[l for l in open('starter-kit/FRAMEWORK_LEARNINGS.md','rb').read().split(b'\n') if re.match(rb'^\s*\|\s*\d+\s*\|',l)];sz=[len(r)+1 for r in rows];o=[s for s in sz if s>1500];print(len(sz),len(o),sum(s-1500 for s in o))"

# the precommit byte defect
python3 -c "import subprocess;raw=subprocess.run(['git','show','HEAD:starter-kit/SESSION_RUNNER.md'],capture_output=True).stdout;print(len(raw), len(raw.decode().strip().encode()))"
```

**Every checker is run bare with `$?` read on the next line.** `producer | grep -q` under
`set -o pipefail` reports a *failed* pipeline even when the pattern matched, because grep
short-circuits and the producer takes SIGPIPE.

---

## 8. What S120 superseded — read this before quoting §2 or §3

Four figures in this plan are now wrong, all in the **favourable** direction. Re-derive, don't quote.

| § | The plan said | Measured at S120 | Why it moved |
|---|---|---|---|
| 2.1 / 3.1 | port takes upstream to **69,749 B**, overage **12,999** | **67,581 B**, overage **10,831** | The plan equated "ported runner" with "the fork's runner". The fork's also carries issue #75's additions (+1,977 B) and the Phase 3F `Model:` bullet (+191 B) — **2,168 B this port does not take**. |
| 3.1 | a **45.3%** cut in the overage | **54.4%** | Follows from the row above. |
| 2.2 | upstream's 13 inline learnings are **byte-for-byte** the fork's rows #1–#13 | **11 of 13** | S119 compacted #12 (2,401 → 1,451 B) and #13 (1,573 → 1,447 B). The port therefore **replaces 1,076 B of text upstream can see today** — disclosed in the commit body rather than presented as purely additive. |
| 3.2 | compaction lands the file at **55,930 B** | **56,673 B** | Superseded at S119 by its own mandatory Learning row; already recorded in that receipt. |

**And three scope facts this plan did not have.**

1. **Upstream already ships `bin/check-learnings`** (247 lines, pointed at `SESSION_RUNNER.md`).
   The plan never mentions it. The port had to carry the fork's version, because the shipped
   `FRAMEWORK_LEARNINGS.md` front matter publishes *"1,500 B, checked by `bin/check-learnings`"* and
   declares the `#14` reservation — shipping the file without the budget arm and the reserved-number
   handling would ship two false claims and flag the deliberate gap as a missing row.
2. **`git diff upstream/main HEAD -- starter-kit/SESSION_RUNNER.md` is not the patch.** The
   originating commit `ed22ace` touched **18 files**; 12 of its per-file patches `git apply --check`
   clean onto `upstream/main`, four are fork-only ledgers/plans that must not port (their failure is
   *correct*), and three — both dashboard twins and the dashboard test — needed hand-porting.
3. **The metered figure and the byte figure disagree, and both belong in the PR.** On the settled
   56,750 B floor the ported pair is still over by 10,831 B. **Metered** by §7's own doubled-file
   method it is **23,902 tok = 95.6% of one read — it fits**, down from 28,234 tok = 112.9%
   (which reproduces §2.1's figure exactly). The floor's 2.27 B/token is ~26% conservative for this
   content. Claim the metered result *and* the floor, never only the flattering one.

---

## 9. What S129 superseded — read this before quoting §3.4

Phase 3's own execution refuted three claims in §3.4 and left one term undefined. Same discipline as
§8: **re-derive, do not quote.**

| § | The plan said | Measured at S129 | Why it moved |
|---|---|---|---|
| 3.4(e) | *"the SEED carries schema documentation only and **declares no total**"* | **FALSE.** `starter-kit/context-budget.json` declares `classes.resident = {total_bytes: 34000, warn_bytes: 30000}`, and `git show upstream/main:starter-kit/context-budget.json` carries the byte-identical block | The claim was never checked against the file. **It matters:** it is offered as one of *"four independent locks"* on D7(b), and that lock does not exist. The other three were re-verified and **do** hold — `.context-budget.json` appears only in the manifest's DEST column, `check_synced()` genuinely never size-checks, and no dashboard twin is touched. |
| 3.4(d) | `precommit()` *"measures **one byte** short"* | **One byte is the FLOOR of the error, not its size.** CRLF content loses **3 B**; content that is not valid UTF-8 does not miscount at all — it raises `UnicodeDecodeError` **out of `run()`**, which does not catch it, taking the pre-commit hook and the commit down | Two independent loss paths, not one. `run()` passes `text=True`, so subprocess applies universal-newline translation **before** `.strip()` takes the trailing byte. Deleting `.strip()` would have fixed only the smaller half. `git cat-file -s` fixes both by never decoding. |
| 3.4(d) | the `KeyError` sites are at `:339` and `:892` | Stale. They were `:450`/`:1025` when S129 opened and are **gone** now, replaced by `class_spec()` | The plan's numbers belong to blob `9e71f83` (919 lines). **Navigate by symbol** (`grep 'def <name>'`), never by this plan's line numbers. |
| 5, Phase 3 | *"the three instrumented adopters"* | **Named nowhere in this repository.** The phrase occurs exactly once — in that DONE line | S129 identified them as `chat_verification`, `vscode_quarto_ext` and `wsfct`: the only siblings carrying `.context-budget.json` **and** `context_budget.py` **and** a history file, corroborated by `file-management-system-plan.md`'s fleet table (`guard=budget`, *"3 of 11 have any size instrument"*). That is an **inference**, not a quotation. **A future phase that re-uses this population should say so explicitly rather than inheriting it.** |

**And three facts Phase 3 had that this plan did not.**

1. **The literal DONE criterion was VACUOUS as written, and the stronger reading was used instead.**
   `(resident total)` — with parentheses — is a pseudo-row emitted **only when the class exceeds its
   ceiling**. None of the three adopters is over (20,583/34,000; 16,607/34,000; 43,956/44,000), so an
   assertion over that string runs on an empty population and passes whatever the code does. S129
   compared the **unconditional summary line**, found the **entire stdout** byte-identical for all
   three, and separately built a deliberately-over fixture so the parenthesised row has a
   non-vacuous witness. **State which output a byte-identity criterion is about.**
2. **Both sides of such a comparison must be run with the CANONICAL tool, on FROZEN inputs.** All
   three adopters run stale copies (29,549 / 41,986 / 29,549 B against 68,081 B canonical), so
   comparing against output they produced would compare two different programs. And the rendered line
   ends in `growth run R/L`, where `R` is a function of the history file **the run itself appends
   to** — a bare run and a `--json` run both append, since `append_history()` precedes the `--json`
   branch. Only `--precommit`, `--selftest` and `--help` are write-free.
3. **`config_defects()` had zero call sites.** It was defined and unit-tested and never run, while
   the distributed seed tells every adopter that a `max_tokens` above the cap *"is rejected as a
   config defect"*. §3.4(c)'s *"asserted at run time"* could not have been satisfied inside it. S129
   wired it into `main()` and `precommit()` after checking that no adopter reddens.

> **Left for a successor, deliberately not done here (FM #17).** The growth-run advisory prints
> *"Nothing is over a ceiling yet — that is the point"* whenever the run fires, including when files
> **are** over — visibly false on this repo's own output today, and **pre-existing**, not a Phase 3
> regression. And `append_history()`'s change test compares `snapshot["files"]` alone, so the new
> `class_bytes` key lands on disk only when a file size also moved. Neither is Phase 3's scope; both
> are one-line decisions someone should take on purpose.
