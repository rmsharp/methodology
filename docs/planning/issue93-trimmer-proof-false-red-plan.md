# The trimmer's generated `.verify.sh` ends red on lossless trims — a plan for upstream issue #93

**Status (S265, 2026-10-05): P1 DONE, `5270be8` (`TRIM_VERSION` 1.5.1), and P2 DONE, `45d32d6` `ba8f883`
`1214511` (`TRIM_VERSION` 1.6.0); measured results in §5 P1, §5 P2 and `BACKLOG-DETAIL.md` §BL-98. P3 is NOT
built; P4 is its own go-ahead.** The paragraph below is
the plan as written at S263 and is left as written, so its "nothing is built" and "no line changed" are
true of S263 and no longer of the tree. Approved to implement P1 first (D1–D4 decided by the operator,
2026-10-05, at the S263 plan-review picker; D5 in part; §9 records each). Written at S263
(2026-10-05) as that session's single deliverable. **The plan is the deliverable; nothing here is
applied** (`starter-kit/SESSION_RUNNER.md` §Planning Sessions, failure mode #18): no line of
`starter-kit/methodology_trim.py` changed, nothing was sent to `KJ5HST/methodology`. Every number below
was produced by running a command against two trees, and the commands are in §3 and §10 so a successor
re-derives rather than trusts. The issue: <https://github.com/KJ5HST/methodology/issues/93>
(filed 2026-10-05 02:21Z under the operator's login, from the adopter `nprcgenekeepr`; no comments).

---

## 0. The answer

**#93's count reproduces exactly — 10 of 54 proofs red, 44 green — and none of the ten is a data loss.**
What does not reproduce is its *split* of the ten into three causes. Measured, they are two:

| class | shards | what the proof is reporting |
|---|--:|---|
| **L2 "leaked"** (cause 2) | **2** | a substring test: an archived entry quotes a front-matter line mid-line |
| **a close-out commit that also trims** (cause 1 **and** cause 3) | **8** | record 0 was a Phase 1B claim stub before the trim and the full record after it |

- **Cause 3 is not independent.** The v1.1.2 shard #93 blames on the frozen `INJECTED=0` constant fails
  for the *current* template too, once its script is re-derived: it was also written by a close-out
  commit that trims (`850e367` in the adopter's history, "S594 -- close out (lossless archive trim of SESSION_NOTES.md)"). The
  frozen text names a wrong reason (`record count 79 != 78`); the right reason is cause 1's. Fixing
  cause 3 alone moves that shard from one red to another.
- **7 of the 10 are `SESSION_NOTES.md` shards, a ledger the canonical trimmer has no spec for.**
  `nprcgenekeepr/methodology_trim.py` is canonical v1.5.0 plus a local `SESSION_NOTES.md` ledger spec
  (two hunks, both pure additions; §3.3). The proof *template* is byte-identical, so the defects are the
  template's; but it fixes a design requirement for any re-derive mode (§4.3): the grammar must come
  from the frozen script, never from the canonical ledger table.
- **In the stub shape nothing archived is lost, and that is mechanically stateable.** In all 8, record 0
  before the trim is a 432–1,946 B claim stub, record 0 after is 6,460–14,846 B, and **no other record
  is absent** (§3.5). The proof already establishes "everything else is byte-identical" whenever its
  frontier clause holds; what it cannot say is *what kind of record* record 0 was.

**Proposed shape — three vertical slices, each its own session, each a separate version bump:**

| phase | one capability | version | red of the adopter's 54, measured or predicted |
|---|---|---|---|
| today | — | 1.5.0 | **10** measured |
| re-derive under today's template, no fix | — | — | **10** measured (§3.3): regeneration alone changes nothing |
| P1 | L2 `leaked` tests whole lines | 1.5.1 patch | **8** measured on the prototype, **0** newly red in 157 proofs |
| P2 | a bundled stub-finalize is recognised, labelled with its own exit status, and prevented at write time | 1.6.0 minor | 8 stay red **but named** (prediction; D2 decides whether they stay red) |
| P3 | `--reverify <shard>` re-derives a frozen proof read-only | 1.7.0 minor | what P1+P2 do reaches the 44+10 existing proofs (prediction) |

**What this does not fix, said plainly:** P1 and P2 change only *newly written* proofs. The ten red
scripts in the adopter, and the five in this repo, are frozen artifacts and stay exactly as they are
until P3 lets someone re-derive them; and even then eight of the adopter's ten stay red under D2(i),
by design (BL-27's ruling, §2). Nothing reaches an adopter until an upstream pull request merges and
`bin/sync` runs there — every outward step is its own go-ahead (§9, D5).

---

## 1. What #93 says, and what I checked

| #93's claim | where | what I found |
|---|---|---|
| 54 proofs, 44 pass, 10 fail | `nprcgenekeepr/docs/archive/*.verify.sh` | **reproduced**: 54, 10 red; 18 scripts are v1.1.2 (2 red), 36 are v1.5.0 (8 red) (§3.3) |
| **1.** a close-out commit that trims always fails L1/L3 (7 v1.5.0 scripts) | `starter-kit/methodology_trim.py:1544-1555` | **confirmed, and by design**: BL-27 chose "stays a FAIL, loud" (`:1530-1535`); the 7 v1.5.0 shards re-derive to an L1 failure with the BL-27 note; the 8th is the v1.1.2 shard below |
| 1. "record 0 differs only by the finalize, every other record byte-identical" | the 7 shards | **confirmed for all 8**: each *before* record 0 is a claim stub, `other records absent: 0` (§3.5) |
| **2.** L2 `leaked` is a substring test (2 scripts) | `:1508-1509` | **confirmed**: `ln in "".join(sr)` is containment over the concatenated records; repro §3.4 turns a mid-line backtick quote red |
| 2. exact whole-line test flags 0 | the two shards | **confirmed**: patched, both go green (`CHANGELOG-through-2026-08-10`, `HANDOFFS-through-2026-09-26`) |
| **3.** frozen v1.1.2 scripts bake `INJECTED` and cannot benefit from BL-36 | `INJECTED=0` in the script | **true of the file, wrong as a cause**: v1.2.0 already measures the added set (`:1437-1439`); re-derived under it, the shard still fails — as cause 1 |
| suggestion: print record 0's diff + a distinct exit status | — | **adopted in part** (§4.1): the diffs run 11–164 added lines, so a *stub test* says more than a diff does |
| suggestion: `--reverify <shard>` | — | **adopted, with one requirement #93 does not state** (§4.3) |

Two statements in #93 I did **not** check: that each of the ten was "diffed by hand" (I diffed the eight
frontier shards, §3.5, and the two leaked ones by the exact-line test), and the issue's claim that
`rmsharp/nprcgenekeepr` is public (I read the operator's local checkout).

---

## 2. Prior art that binds this plan (read first, and it changes the plan)

| source | what it settles | consequence here |
|---|---|---|
| **BL-27**, v1.1.2 (`starter-kit/methodology_trim.py:98-104`, `:1530-1535`) | a bundled frontier edit *"is NOT an exemption — this stays a FAIL, loud, because a real loss can have this exact shape"*; the note says "diff record 0 by hand" | P2's default keeps it a FAIL; D2(ii), which would not, **reverses a ratified ruling** and needs its own approval |
| **BL-28**, v1.1.3 (`:92-97`, `:1497-1505`) | L2's *missing*-line test was made exact-line-set membership, patch bump | P1 is the mirror image for `leaked` and takes the same bump class |
| **BL-36**, v1.2.0 (`:81-90`; `docs/audits/2026-08-15-bl36-archive-losslessness.md` Recommendations 1–4) | the injected set is *measured*; **Rec. 3: "make the bundling impossible rather than modelled … a protocol rule"**; Rec. 1: regeneration alone fixes nothing | cause 1 is that rec. 3, still untaken in the *distributed* corpus (§4.1) |
| **Operator decision 2026-08-16** (`BACKLOG-DETAIL.md:887-899`) | regenerating frozen proofs is *"a deliberate exception to the archive freeze rule … needs its own go-ahead"* | P3 re-derives **without writing**, so it needs no such exception |
| **BL-60 constraints 1–3** (`BACKLOG-DETAIL.md:1948-1962`) | a proof runs from its shard alone; the generator is distributed; **"frozen proofs must keep working … migrating the old ones is a separate question"** | same; and BL-60's shared-harness redesign is open and could relocate `VERIFY_TEMPLATE` — D4 |
| **fork Learning #58** (`docs/FORK_LEARNINGS.md:76`) | folding the pointer block *inside* the trim commit turns the proof red; the next commit is green | the same family as cause 1: **what else rides in the trim commit** is what the proof reads |
| **Class B** (`docs/audits/2026-09-01-bl36-classb-adjudication.md`) | the fork's own fifth red proof, `HANDOFFS-through-2026-08-25`, is a front-matter line the trim commit rewrote; regeneration is useless | **a fourth cause outside #93**; it stays red under every phase here (§3.2) |
| `FRAMEWORK_APPARATUS.md:520` (distributed) | *"A trim … earns its own commit"* | **contradicts the verifier**: `methodology_trim.py:1551-1555` tells the reader bundling is "this repository's own established practice" |

The last row is classb-adjudication's structural observation 2 again — *a file's instructions and its
verifier disagree, and only the verifier is mechanical* — now in the distributed tool's own message.

---

## 3. Evidence (commands and results)

**Trees.** This repo at `3d7c5c8` via `git clone --no-local` into the session scratchpad; the adopter
via a hardlinked `git clone` of `~/Development/nprcgenekeepr` at `2563a6ee0` (the operator's checkout).
Neither working tree was written to. `starter-kit/methodology_trim.py` is **byte-identical to upstream's**
(`git rev-parse HEAD:starter-kit/methodology_trim.py` and `upstream/main:` both read `b98ff4b`), and
`tools/test_methodology_trim.py` does not differ from upstream's; `FRAMEWORK_APPARATUS.md` does, by 5
lines (the sentence of §2's last row sits at `:524` upstream, `:520` here).

### 3.1 The tool

`python3 docs/planning/issue93-evidence/reverify_prototype.py <repo> <trimmer.py> <out.tsv> [--exact-leak]`
runs each frozen `docs/archive/*.verify.sh`, then regenerates its proof **in memory** from `<trimmer.py>`'s
current `VERIFY_TEMPLATE` — lifting `RECORD_KIND`, `RECORD_START`, `FENCE_INFO`, `FOOTER_MODE` and
`REGEN_PATTERNS` from the frozen script itself, defaulting the last to `[]` for v1.1.1 which predates it —
runs that from a temp file outside the repo, and tabulates both verdicts. It is the prototype of P3, not
P3. `--exact-leak` applies P1's one-line change to the generated text.

### 3.2 This repo — 103 proofs

```
python3 docs/planning/issue93-evidence/reverify_prototype.py <clone> <clone>/starter-kit/methodology_trim.py out.tsv
```

| version | proofs | frozen red | re-derived red |
|---|--:|--:|--:|
| v1.5.0 | 87 | **0** | 0 |
| v1.3.0 | 7 | 1 (`HANDOFFS-through-2026-08-25`, Class B) | 1 |
| v1.2.0 | 3 | 0 | 0 |
| v1.1.3 | 2 | 0 | 0 |
| v1.1.1 | 4 | 4 | 2 (the two `CHANGELOG`, now green; the two `HANDOFFS` print the frontier note) |
| **all** | **103** | **5** | **3** |

BL-36's audit predicted that regenerating its four v1.1.1 proofs "takes the four from 4 red to 2 red";
**the re-derivation reproduces that number without rewriting a frozen file.** No v1.5.0 proof here is
red: this repo trims in its own commit, at the start of a session when record 0 is the predecessor's
*complete* receipt, so neither cause 1 nor cause 2 has occurred. (For the two v1.1.1 `HANDOFFS` shards I
did not read what record 0 was before the trim.) The same run with `--exact-leak`: **0 proofs newly red,
0 newly green.**

### 3.3 The adopter — 54 proofs

18 v1.1.2, 36 v1.5.0; by ledger 16 `CHANGELOG.md`, 15 `HANDOFFS.md`, **23 `SESSION_NOTES.md`**.

| shard (`docs/archive/…`) | script | frozen first failure | class |
|---|---|---|---|
| `CHANGELOG-through-2026-08-10` | v1.1.2 | L2 leaked 2 lines, first `## Size, and when to archive` | L2 leaked |
| `HANDOFFS-through-2026-09-26` | v1.5.0 | L2 leaked 1 line, first `python3 methodology_trim.py --file HANDOFFS.md …` | L2 leaked |
| `HANDOFFS-through-2026-09-26-3` | v1.5.0 | L1 not byte-identical, BL-27 note | frontier stub |
| `SESSION_NOTES-through-2026-09-20-2`, `-09-21`, `-09-21-2`, `-09-26-4`, `-09-28`, `-09-28-2` | v1.5.0 | L1 not byte-identical, BL-27 note | frontier stub (6) |
| `SESSION_NOTES-through-2026-08-15` | v1.1.2 | L1 + `L3 record count 79 != 78` | frontier stub — **re-derived**; the frozen text is the wrong reason |

Re-derived under today's template: **10 red** (nothing changes). With `--exact-leak`: **8 red**, the
two L2 shards green, **0 newly red**. The adopter's trimmer differs from canonical by `diff` hunks
`300a301,315` (a `_session_notes_date` function) and `351a367,400` (the `"SESSION_NOTES.md"` ledger
spec), both appends; its own comment says the overlay in `bin/sync` will silently drop them.

### 3.4 Cause 2, built in a throwaway repo (`docs/planning/issue93-evidence/repro_cause2.py`)

The canonical suite's own fixtures; each variant trims `HANDOFFS.md`, commits, runs the generated script.

| variant | script | result |
|---|---|---|
| A — no archived record quotes a front-matter line | v1.5.0 | exit 0, OK |
| **B** — an archived record quotes one in backticks, mid-line | v1.5.0 | **exit 1, `L2 FRONT MATTER leaked 1 line(s)`** — the false red |
| C — same, `leaked` tested against whole lines | patched | exit 0, OK |
| **D** — the front-matter line copied whole into the shard's own front matter, inside the trim commit | v1.5.0 | exit 1, `leaked` |
| **E** — same leak | patched | **exit 1, `leaked`** — detection kept |

A first version of D committed the tamper *after* the trim commit and passed, which looked like the fix
losing detection. It did not: the proof reads the shard **as the trim commit wrote it** (`TRIM_SHA` is
`git log --diff-filter=A -1 -- $SHARD`), so a later edit is invisible to it by design (fork Learning #58).
The fixture was wrong, not the patch.

### 3.5 Cause 1, read on all eight shards

The re-derivation, with a scratch patch printing record 0's before and after:

| shard | record 0 before | after | lines removed / added | other records absent |
|---|--:|--:|--:|--:|
| `HANDOFFS-through-2026-09-26-3` | 606 B | 7,827 B | 11 / 11 | 0 |
| `SESSION_NOTES-through-2026-08-15` | 1,946 B | 7,665 B | 23 / 90 | 0 |
| `SESSION_NOTES-through-2026-09-20-2` | 807 B | 7,899 B | 12 / 119 | 0 |
| `SESSION_NOTES-through-2026-09-21-2` | 432 B | 8,915 B | 7 / 137 | 0 |
| `SESSION_NOTES-through-2026-09-21` | 553 B | 6,931 B | 9 / 103 | 0 |
| `SESSION_NOTES-through-2026-09-26-4` | 536 B | 14,846 B | 7 / 164 | 0 |
| `SESSION_NOTES-through-2026-09-28-2` | 565 B | 6,460 B | 4 / 103 | 0 |
| `SESSION_NOTES-through-2026-09-28` | 592 B | 8,074 B | 6 / 92 | 0 |

**Checked mechanically over the whole of record 0 before the trim**, not read: the `HANDOFFS` one matches
`^status: pending$`; each of the seven `SESSION_NOTES` ones matches all of `\(IN PROGRESS\)`,
`Session claimed` and `CHANGELOG: pending` — **8 of 8**. (I read the first lines of each diff and none of
the added blocks.) **That is the runner's own design** — `SESSION_RUNNER.md` Phase 1B: "This stub is
overwritten during Phase 3D" — so the bytes the proof reports as missing are a placeholder meant to be
replaced. One stub (`SESSION_NOTES-through-2026-08-15`, 1,946 B, 24 non-blank lines) carries real prose
written into it, which is the cost of D2(ii) in §9: the discriminator says *a stub was replaced*, not
*nothing worth keeping was in it*.

### 3.6 Grep inventory — what a change to the generator touches

`git grep` at `3d7c5c8`, outside `docs/archive/`, `CHANGELOG.md`, `HANDOFFS.md` and generated `*.verify.sh`:

| symbol or construct | files |
|---|---|
| `VERIFY_TEMPLATE`, `build_verify` | `starter-kit/methodology_trim.py`, `tools/test_methodology_trim.py` (`VERIFY_TEMPLATE` only) |
| `frontier_edit`, `absent_records`, `known, accepted pattern` | `starter-kit/methodology_trim.py` only |
| `leaked = [` (the precise construct; the bare word matches 15 other files, in other senses) | `starter-kit/methodology_trim.py:1508` only |
| a test pinning each behaviour | `tools/test_methodology_trim.py:1103` `TestVerifyShHandoffFalsePositives`, `:1152`/`:1180` the frontier tests (`assertNotEqual(returncode, 0)` and `assertIn("NOTE:")`), `:1215` the BL-28 append-tamper, `:1288` `TestVerifyShBundledAddsAreMeasuredNotAssumed` |
| `TRIM_VERSION` consumers | `starter-kit/methodology_dashboard.py:494,1056` and the `tools/` twin (regex-read to report an adopter's tool version), `tools/test_methodology_dashboard.py` (fixtures; one asserts equality with `trim.TRIM_VERSION`, `:5341`) |
| consumers of a proof's **exit code** | `tools/test_methodology_trim.py` only; `bin/`, the dashboard and `.githooks/` do not run proofs (the dashboard only excludes the `.verify.sh` suffix from reads, `_GENERATED_PROOF_SUFFIX`) |
| exit statuses in use | `2` (18 sites) and `3` (11) in the tool; the proof uses `1` (fail) and `3` (not in a repo); **`4` is free** |
| distributed | `bin/_manifest.py:50` installs the trimmer as a TRACKED file; `FRAMEWORK_APPARATUS.md:520` is distributed prose |
| baseline | `python3 tools/test_methodology_trim.py`: **124 tests, OK (skipped=2)** in 15 s; `bash bin/tests.sh` on the tree before this plan: **356 passed, 0 failed, 6 skipped** |

The only consumer of a proof's exit code is the trimmer's own test file, so a distinct nonzero status
breaks nothing in the repo; an adopter's own loop that treats *any* nonzero as red is unchanged by it.

---

## 4. The design

### 4.1 Cause 1 — a commit that finalizes record 0 and trims

The proof cannot tell an honest finalize from an edit of an archived record **by looking at record 0
alone**, and BL-27 refused to guess. §3.5 supplies what it lacked: a discriminator that is not a guess.
Three layers, in the order they act:

1. **Prevent (protocol + write-time).** Audit Recommendation 3, never taken in the distributed corpus.
   `FRAMEWORK_APPARATUS.md:520` says a trim earns its own commit but not *when*. The rule that makes this
   repo green is a timing one: **trim while record 0 is complete — before the claim, or after the
   finalize — never between.** The writer can see the bad state: at `--write`, record 0 of the live ledger
   still carries the ledger's stub marker (HANDOFFS `status: pending`; CHANGELOG a heading ending
   `(in progress)`; a local spec's own). **[S265: corrected. Only `HANDOFFS.md` declares a marker; the
   `CHANGELOG.md` one is withdrawn, with the evidence, in §5 P2 DONE.]** Add a finding `FRONTIER_PENDING_STUB`, exit 0, stating the
   consequence and the two ways out. It needs one optional `LedgerSpec` field, `stub_marker`; a spec
   without it (the adopter's local `SESSION_NOTES.md`) gets no guard and says so.
   *The guard also has to cover the other order* — finalize, then trim, one commit — where record 0 is
   already complete at write time and the live ledger is merely **dirty against `HEAD`**. §3.5 cannot
   tell me which order the adopter used: git shows only that record 0 *in the parent* was a stub.
2. **Name (proof side).** When the existing frontier clause holds *and* the pre-trim record 0 matches the
   stub marker, the proof prints a distinct result instead of the generic L1/L3 pair: *"record 0 was a
   pending stub and was finalized in the trim commit; every other record is byte-identical"*, with the
   stub's size, and exits **4**. The marker must travel in the proof's grammar block (`STUB_PATTERN =`,
   beside `REGEN_PATTERNS`), because a frozen script cannot consult a ledger table. A record 0 that was
   *complete* before the trim and differs after it still exits 1 with BL-27's note and no relabelling —
   which is the real-loss shape BL-27 protected, and P2's complete-record-0 control must pin it.
3. **Say the same thing everywhere.** The note at `:1551-1555` stops asserting that bundling is "this
   repository's own established practice"; `FRAMEWORK_APPARATUS.md:520` gains the timing sentence; the
   distributed `starter-kit/` runner needs no change (it does not mention trimming).

**What the proof still cannot do** is certify that the finalized record 0 is *right* — only that no other
byte of the pre-trim ledger went missing. That was always the limit; the label now says it.

### 4.2 Cause 2 — one line, one bump class

Replace `ln in sfront or ln in "".join(sr)` with membership in the *sets of whole lines* of the shard's
front matter and of its records, keeping the `> 24` length filter. A migration moves whole lines, so
whole-line membership is the right test for it; §3.4 E shows the detection survives, and the prototype
shows 0 newly red proofs over 157. **Patch, 1.5.1** — a correctness fix to what the tool writes with no
new finding code or exit status, the class of 1.1.2 and 1.1.3 (`:92-104`).

### 4.3 Cause 3 — re-derive, do not rewrite

`--reverify <shard>`: given a shard, take `LIVE`, `SHARD` and the five grammar lines **from its frozen
`.verify.sh`**, build today's `VERIFY_TEMPLATE` from them, run it, print the verdict under a banner naming
the version that re-derived it, and **write nothing** (a test asserts `git status --porcelain` unchanged).

- **Why the frozen script, not the ledger table.** 23 of the adopter's 54 shards are a ledger `LEDGERS` has
  no entry for, and the overlay deletes a local entry. §3.1's prototype lifts the grammar by regex over
  five identically shaped lines and lifted **all 157** scripts in both trees (v1.1.1, 1.1.2, 1.1.3, 1.2.0,
  1.3.0 and 1.5.0: 4, 18, 2, 3, 7 and 123).
- **Why this needs no freeze exception.** The operator's 2026-08-16 ruling (§2) covers *regenerating* a
  frozen artifact. This produces a second verdict and leaves the artifact; BL-60 constraint 3 holds.
- **Its own limit, to be printed in the banner:** the re-derived verdict is a claim about today's logic
  against that shard, **not the artifact that was shipped**; a script too old to carry the five lines is
  refused by name.

### 4.4 Alternatives rejected

| alternative | why not |
|---|---|
| regenerate the red scripts in place | the 2026-08-16 ruling; BL-60 constraint 3; and §3.3 shows it changes nothing for 8 of 10 (audit Rec. 1) |
| delete the `leaked` check | loses detection D/E keeps |
| raise the `> 24` length threshold | a heuristic that moves the false red rather than removing it |
| accept *any* frontier edit as a pass | BL-27's reason stands: a complete record 0 edited in the trim commit is a real loss shape |
| print only a unified diff and leave exit 1 (#93's suggestion) | the eight diffs are 11–164 added lines; a caller still cannot tell them from a loss without reading them |
| document the timing rule only | the rule already exists (`FRAMEWORK_APPARATUS.md:520`); nothing detects its breach until a proof runs — the S88 audit's own finding |

---

## 5. Phases

Every phase is **one session**; close out when it is done. Each is a vertical slice of one capability
(failure mode #25), checkpoint-committed per layer at no more than five files (`SAFEGUARDS.md` §Blast
Radius), and RED first.

### P1 — `leaked` tests whole lines (patch, 1.5.1)

- **Layers:** the template line and the version comment (`starter-kit/methodology_trim.py`); tests
  (`tools/test_methodology_trim.py`, beside `TestVerifyShAppendTamperEvadesSubstringCheck`).
- **Tests, written first and failing for the right reason:** a quote-mid-line fixture must go red on the
  1.5.0 text (§3.4 B); the narrowed controls — whole line in the shard's front matter, whole line inside a
  record — must stay red after.
- **DONE:** the new tests RED before and GREEN after; `python3 tools/test_methodology_trim.py` 124 → 124+k
  OK; `bash bin/tests.sh` 0 failed; with the real trimmer, `reverify_prototype.py` (no `--exact-leak`) over
  both trees reads adopter **8 red**, fork **3 red**, **0 newly red**; `TRIM_VERSION` 1.5.1.
- **Surface.** (a) Temp-repo unit tests: faithful to the template's logic, but their front matter is
  synthetic — they **cannot** show that a real ledger quotes a real line. (b) The adopter clone: the only
  surface holding real false reds. (c) This repo's 103 frozen proofs: the green-must-stay-green surface,
  reached only through the prototype because P1 does not touch a frozen script. **Cannot enforce:** that
  the red scripts in the adopter turn green (that is P3), or that any adopter receives the change.
- **DONE at S264 (`5270be8`), each criterion as measured:** the two quote-mid-line tests RED on 1.5.0
  and the three controls green on both; the unit file 129 OK (skipped=2), k = 5; `bin/tests.sh` 362
  passed, 0 failed, 0 skipped; `reverify_prototype.py` with the patched trimmer and no `--exact-leak`:
  adopter 54 proofs **8 red** (from 10), fork 104 proofs **3 red** (from 5, none newly), **0 newly red**
  in either, the adopter's 2 newly green being exactly §3.3's two L2 shards. Two differences from the
  plan's text: the adopter checkout had moved to `3a59ed844` (the plan read `2563a6ee0`) with the same 54
  proofs and 10 red, and the fork has 104 proofs, not 103, because the S264 trim added shard `-5`. The
  patch is two set definitions and the changed `leaked` list inside `VERIFY_TEMPLATE`; the shard's
  front-matter half and the record half are each pinned by a test that fails without it.

### P2 — a bundled stub-finalize is recognised and prevented (minor, 1.6.0)

- **Layers (three checkpoints):** (1) `LedgerSpec.stub_marker` for `CHANGELOG.md` and `HANDOFFS.md`, the
  `STUB_PATTERN` grammar line, the proof's labelled result and exit 4; (2) the write-time guard, both
  orders (§4.1); (3) `FRAMEWORK_APPARATUS.md:520`, the note's wording, the version comment.
- **Tests first:** the `:1152` frontier test gains the stub variant (exit 4, label); its sibling at `:1180`
  and a *complete-record-0-edited* variant stay exit 1 with no relabel; the guard fires on a stub frontier
  and on a dirty ledger and is silent on a clean one; a spec without `stub_marker` is silent and says so.
- **DONE:** all of that green; `bash bin/tests.sh` 0 failed; **mutation check** — delete the stub test in the
  proof and the complete-record-0 control must go red; the guard run against a throwaway clone of the
  adopter at the commit before one of the eight trims.
- **Surface.** Unit fixtures with a real `git commit`. **Cannot enforce:** that an adopter's *local* spec
  carries a marker; that the guard fires at the moment a session actually runs the trimmer (a session that
  trims by hand-editing never reaches it); which commit order the adopter used (§4.1).
- **DONE at S265 (`45d32d6` the proof's label and exit 4, `ba8f883` the write-time guard, `1214511` the prose;
  `TRIM_VERSION` 1.6.0), each criterion as measured.** Tests first: 8 for the label, 12 for the guard, 5 for the
  shared wording; each class RED for the right reasons before its change (exit 1 with the generic pair, no
  `STUB_PATTERN`, no guard code, the prose and the note lacking the rule) with its controls green. The unit file
  reads 154 tests OK (skipped=2), up from 129, and the `trimmer-unit-tests` floor is 154 (`7a18512`).
  `bin/tests.sh` read 362 passed, 0 failed, 0 skipped at each of the three checkpoints (the first run at the
  first checkpoint read 360 and 2 failed, two `echo | grep -q` assertions, while I was cloning repositories in
  parallel; the quiet re-run read 362 and 0). **Mutation check:** 18 mutants of the label, 14 of the guard and 5
  of the wording, every one killed by its intended test, after the first run left 2, 1 and 0 alive and the tests
  were tightened (a marker not anchored at the line start; the note unasserted; the missing-HEAD branch that the
  stub-at-record-0 test never reached). The plan's "delete the stub test in the proof and the complete-record-0
  control must go red" is covered as two mutants: the label never fires (the stub test goes red) and the label
  ignores the pre-trim marker (the complete-record-0 control goes red).
  **Two real surfaces, and where they differ from the plan's prediction.** Re-deriving every frozen proof under
  the new template, the stub marker supplied from the ledger table by the LIVE basename: the adopter
  (`nprcgenekeepr` at `1cfee7215`, read through a clone) 54 proofs, 46 green, **1 at exit 4**
  (`HANDOFFS-through-2026-09-26-3`, a 606 B stub, 5 other records, the size §3.5 recorded), 7 at exit 1, 0 newly
  red; this repo 105 proofs, 102 green, 1 at exit 4 (`HANDOFFS-through-2026-08-02`, a 750 B stub), 2 at exit 1
  (Class B, and `HANDOFFS-through-2026-08-09`, where an L2 front-matter failure also holds, so the label is
  withheld by design and whether its record 0 was a stub is not read), 0 newly red. §0's "8 stay red but
  named" is therefore 1 of 8 with canonical specs: the 7 `SESSION_NOTES.md` shards go to exit 4 only if the
  adopter's local spec (the one the `bin/sync` overlay drops, D5, not asked) declares a marker. The guard, the
  new trimmer's dry run at real commits with `--force` (the stub trim's parent is `SRF_RED` without it): the
  adopter at the parent of its stub trim fires `FRONTIER_PENDING_STUB`; this repo at `8e3d568` (record 0
  complete) is silent; this repo at `994eee5`, S265's own claim, fires. The adopter's parent of
  `HANDOFFS-through-2026-09-26`, a trim whose proof passes, also fires: the warning is about the wrong time to
  trim, not a certainty of a red proof, and its message is conditional.
  **Deviations from the plan's text, each decided on evidence.** (1) **`CHANGELOG.md` declares no stub marker.**
  §4.1 and §5 P2 named one, "a heading ending `(in progress)`". The heading's shape is NOT the reason: of the 27
  `(in progress)` headings in this ledger at S265, 14 end there and the 13 newer ones carry ` — <description>`
  after it (I first wrote that none ends there, from the first five rows of a truncated listing; the committed
  S265 layer-1 entry says so and the correcting entry is in `CHANGELOG.md`). The reason is the ledger's own
  lifecycle, "a committed entry is never edited", with close-out adding its own entry (`FRAMEWORK_APPARATUS.md`,
  The Action Ledger): a claim entry that still reads `(in progress)` is a FINAL record, so a marker there would
  warn on every mid-session `CHANGELOG.md` trim and label an edit of a committed entry "a stub finalize". A
  ledger with no marker is
  silent in the guard and its proof note says it declares none. (2) **The label has two more conditions than
  §4.1 lists:** the record that replaced the stub no longer matches the marker (an edit made while still pending
  was not a finalize) and the other records are also in order, not only present. (3) **The guard has two codes,
  one per commit order** (`FRONTIER_PENDING_STUB`, `FRONTIER_FINALIZE_UNCOMMITTED`), because §4.1 required both
  orders and tests assert on codes; order B asks whether HEAD's stub is absent from the working ledger, the
  proof's own test, not whether the ledger is dirty, which would warn on a pure addition.
  **What P3 inherits.** A frozen proof written before 1.6.0 carries no `STUB_PATTERN` line, so §4.3's "the grammar
  comes from the frozen script, never from the ledger table" holds for the five lines that exist there and not
  for this one: the re-derive above supplied it from `LEDGERS` by the LIVE basename, and `--reverify` must do
  the same (empty when the ledger has no entry or no marker). §0's and §5 P3's prediction for the adopter, "2
  green + 8 exit-4", is superseded by 2 green + 1 exit-4 + 7 exit-1.

### P3 — `--reverify` (minor, 1.7.0)

- **Layers:** the flag and the lift (`:2144-2158` is the argument table); the banner and the refusal for a
  script with no grammar lines; tests.
- **DONE:** writes nothing (`git status --porcelain` identical before and after); the fork's 103 and the
  adopter's 54 re-derive as **predicted in §0** — adopter 2 green + 8 exit-4, fork 2 green + 2 labelled +
  the Class B shard still red — and every difference from the prediction is explained in the report, not
  edited into it.
- **Surface.** Both real trees, which is the point. **Cannot enforce:** that a re-derived verdict equals
  the one a *new* trim would have produced for an old record grammar.

### P4 — distribution (outward; its own go-ahead, never implied by P1–P3)

`bin/sync --source=local --dry-run` against a throwaway adopter tree shows the tracked trimmer arriving
byte-identical; one upstream pull request carrying P1–P3 (they share a template, so they are dependent
work), vetted on this side first. **Nothing in this plan authorizes it, or a comment on #93.**

---

## 6. Impact analysis

| system | impact | action |
|---|---|---|
| `starter-kit/methodology_trim.py` | template, spec, writer, CLI change | P1–P3 |
| its test file | +tests, none removed; `:1152` gains a variant | P1–P3 |
| adopters | new trims get the fixes; **old proofs unchanged until P3**; version moves 1.5.0 → 1.7.0 | a go-ahead, P4 |
| the adopter's local `SESSION_NOTES.md` spec | overlay still drops it; the guard is silent for it | out of scope; named in D5 |
| dashboards | read `TRIM_VERSION` by regex to report an adopter's tool version; whether a bump reads as "behind" I did not check | none expected; `bin/sync` carries the file |
| the fork's 103 proofs | untouched | — |
| **does not change** | the 5 red proofs here, BL-60's open redesign, the S232 retention depth, any ratified BL-27/BL-36 ruling under D2(i) | — |

**Failure modes.** The proof gains a new passing-adjacent exit (4): a caller that tests `== 1` rather than
`!= 0` misses it — none in this repo does (§3.6). A stub marker too loose would label a real edit "stub":
the complete-record-0 control (P2) exists for that, and an adopter's local marker is theirs to get right.
`--reverify` on a script whose grammar the current template reads differently could print a verdict that
disagrees with the frozen one for a *non-bug* reason; the banner names it. **Rollback** per phase is one
`git revert`, since each phase is a checkpoint-committed commit set.

---

## 7. Cost

$0 throughout; no model calls. Each phase is one session; P2 is the largest (three layer checkpoints).

## 8. Order, and BL-60

P1 first and independent (4 lines, patch). BL-60's shared-harness redesign is **open, has no plan
document in `docs/planning/`, and was set aside for the overhead plan the day its planning session was
chosen** (`CHANGELOG.md`: "It displaces BL-60's planning session"); if it lands, `VERIFY_TEMPLATE` moves and P2/P3's template edits move with it, but the *behaviour*
they specify does not, and nothing here is wasted: the tests carry over. Recommendation: do not wait for it.

## 9. Decisions (the operator's; the S263 plan-review picker, 2026-10-05)

**D1 — cause 2's shape.** Whole-line membership, 1.5.1 patch (§4.2). **DECIDED: yes, P1 now.**
Alternative not taken: do not fix it (the two adopter shards stay red).

**D2 — cause 1's verdict for a recognised stub finalize.** (i) keep it a FAIL with its own label and
exit 4, BL-27 intact; or (ii) exit 0 with the label, which **reverses BL-27 for this one shape** and
means the proof certifies a replaced stub, including the one that carried prose (§3.5).
**DECIDED: (i), FAIL, labelled, exit 4.** Moving to (ii) later costs nothing; the reverse does not.

**D3 — cause 3.** `--reverify`, read-only, grammar from the frozen script (§4.3). **DECIDED: yes.**
Alternative not taken: leave frozen proofs frozen and document it.

**D4 — order against BL-60.** **DECIDED: proceed now, do not wait for BL-60** (§8).

**D5 — what leaves this machine, and what is bookkeeping.** **DECIDED, in part:** (a) a fork-side backlog
row for this plan, **BL-98**, opened the same session (not outward); (b) a comment on #93 correcting its
split (§0): **go-ahead given, but the exact text is shown to the operator first and nothing is posted until
he approves that text**; (c) P1–P3 are to be treated as one future upstream pull request, vetted here first
(P4): **nothing is sent now, and the pull request is its own go-ahead.** *Not asked, still open:* whether the
adopter's local `SESSION_NOTES.md` spec, which the `bin/sync` overlay drops, is its own backlog item.

## 10. Reproduce, and what I did not verify

```
git clone --no-local . /tmp/m && git clone ~/Development/nprcgenekeepr /tmp/nprc
python3 docs/planning/issue93-evidence/reverify_prototype.py /tmp/nprc /tmp/m/starter-kit/methodology_trim.py /tmp/a.tsv
python3 docs/planning/issue93-evidence/reverify_prototype.py /tmp/nprc /tmp/m/starter-kit/methodology_trim.py /tmp/b.tsv --exact-leak
python3 docs/planning/issue93-evidence/reverify_prototype.py /tmp/m   /tmp/m/starter-kit/methodology_trim.py /tmp/c.tsv
python3 docs/planning/issue93-evidence/repro_cause2.py
python3 tools/test_methodology_trim.py
```

**Not verified:** (1) which commit order the adopter used for the eight (§4.1); (2) what record 0 was
before the trim in the fork's two v1.1.1 `HANDOFFS` shards; (3) every P2/P3 outcome in §0 is a
**prediction** from the prototype, which patches one line and prints a diff — the stub test, exit 4, the
guard and `--reverify` do not exist yet; (4) in §3.5 the stub test is mechanical over record 0 *before*,
but I did not read the *added* block of any of the eight, so "the finalize is the only change to record 0"
rests on the proof's own clause (no other record absent) and not on a line-by-line read; (5) the operator's
checkout may be ahead of the public repository; (6) the planning checklist's "deepest available reasoning
mode set at session start" was **not** done — there is no tool to set it from inside a session, and the
operator had not set it.
