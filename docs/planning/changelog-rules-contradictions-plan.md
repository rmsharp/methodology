# BL-57 — one set of `CHANGELOG.md` rules, kept in one place

**Status:** APPROVED by the operator at S162 and committed (`9292132e`, 2026-09-15); amended at S163
(see **Trees**). Nothing in it is implemented.
**Workstream:** [`ARCHITECTURE_WORKSTREAM.md`](../../workstreams/ARCHITECTURE_WORKSTREAM.md) (a migration
plan), under [`SESSION_RUNNER.md` §Planning Sessions](../../starter-kit/SESSION_RUNNER.md).
**Source:** [BL-57](BACKLOG-DETAIL.md#bl-57), raised 2026-09-14 on the operator's request, high priority.
**Decided:** Q1–Q4, by the operator at S162 (§2.1). **Recommended, approved with the plan:** D5–D10 (§2.2).
**Reviewed:** an independent read-only review at S162 found four errors, nine risks and six nits in the
first draft. Each was reproduced before it was fixed here; about 90 citations and 30 numbers were
confirmed.
**Trees:** the upstream work targets `KJ5HST/methodology:read-set-budgets` at **`b82dcff`** (PR #80's
head); fork `main` at **`7ea7346b`**; six adopters under `~/Development/`. Every line number is
`b82dcff`'s unless marked *fork*.
**Amended at S163 (2026-09-15):** the maintainer's #80 review (F1, option (a)) cuts the branch's
`starter-kit/FRAMEWORK_LEARNINGS.md` to rows 1–13 plus the reserved `#14` — local branch
`pr80/f1-learnings-1-13`, commits `5c9f0f3` and `d4e15706`, not pushed when this was written. Once
pushed, #80's head moves past `b82dcff`, so P1 starts from the new head (hazard 1), and **no row past
#13 exists upstream**: a fork learning reaches an upstream file only as its rule, stated inline, never
as a number (P1 step 5). §1.1's C5 and §7's *Keep keying on the titles* row describe `b82dcff` itself.

---

## 0. The answer

The framework states its rules for `CHANGELOG.md` across fourteen files (§4.2), and they disagree in
sixteen ways (§1.1). Most of the disagreement has one cause: the bulk of the rules live **inside the
seed** `starter-kit/CHANGELOG.md` — 11,804 of its 12,893 bytes — and `bin/sync` writes a seed once and
never again, so every correction strands the copies already in adopters. `wsfct/CHANGELOG.md:101` and
`nprcgenekeepr/CHANGELOG.md:3982` still call truncation *silent*, although the framework corrected that
at BL-51's Phase A.

The plan moves the rules to **one synced home**, a new §The Action Ledger in `FRAMEWORK_APPARATUS.md`.
It shrinks the seed to a linked pointer carrying a format marker that `bin/status` keys on. Then it fixes
each contradiction once, in that home, as the operator decided: **archiving is optional**, because
nothing reads the ledger whole; **`[BL-<id>]` accepts any backlog id**; **one entry per commit, never
edited**.

Four sessions build it on a branch from PR #80's head (P1–P4). One brings it to fork `main` and this
repo's own ledgers (P5). Six migrate the adopters, each in its own repository (P6–P11). The last opens a
**new** upstream PR once #80 has merged, which is its own go-ahead (P12). PR #80 itself is not touched.

---

## 1. Context

### 1.1 The sixteen findings

C1–C8 are BL-57's own, each re-read on `b82dcff`. C9–C16 were found while taking this plan's inventory;
C16 follows from Q4 A.

| # | The disagreement | Where it is stated | Phase |
|---|---|---|---|
| C1 | Whether a session reads the file at all | *It does:* seed :96–97, :104 (*"every session pays for the whole file"*), :180–181 (*"split into shards once it outgrows a session's read"*); `HANDOFFS.md` seed :91, :98, :150; `methodology_trim.py:186` (*"the per-file context-tax budget"*); upstream's root `.context-budget.json` (`CHANGELOG.md` read-mandated at 65,536 B). *It does not:* runner :37–38 (Phase 0 takes a frontier from `git log`); `BOOTSTRAP.md` :136, :383. *Measured:* one whole read per root ledger in 85 transcripts (BL-52, S112) | P2 |
| C2 | Which size triggers an archive | seed :103–104 (a 2,000-line rate plus a byte level, *"default 65,536 B"*); `methodology_trim.py` :164, :186 (196,608 B); *fork* root front matter (*When to archive again*, the line rate alone); upstream's root (none); this repo: do not trim (operator, 2026-09-14) | P2 |
| C3 | "Append" or "prepend" | *Append … newest on top:* runner :278, :329, :357; `ITERATIVE_METHODOLOGY.md:294`; `HOW_TO_USE.md` :767, :804; `.githooks/pre-commit:56`. *Prepend:* seed :17, :91; runner :39 | P4 |
| C4 | Whether a trim may happen in Phase 0 | seed :167–169 (never); *fork* root `HANDOFFS.md:15` (count at Phase 0, trim to 4) | P2, P5 |
| C5 | Two definitions of a stale seed | `bin/_manifest.py:95–98` keys on the seeds' titles, which never change, so the check cannot fire — and `b82dcff` ships Learning #19 saying exactly that. *Fork* `bin/_manifest.py:125–128` keys both on `Size, and when to archive` (`12463dd`, S41, never upstreamed) | P1 |
| C6 | A closed tag vocabulary, an open practice | seed :23–32; runner :278, :329; `ITERATIVE_METHODOLOGY.md:294`; `.githooks/pre-commit:57` — against 361 adopter entries carrying a non-numeric `[BL-…]` id (§4.4) and the canonical tutorial's own `[BL-F1]` (`docs/tutorials/T2_worked_transcript.md:257`) | P3 |
| C7 | Where the Phase 1B marker lives, and whether a claim commit has an entry | runner :88 and `ITERATIVE_METHODOLOGY.md:169` put `CHANGELOG: pending` in `SESSION_NOTES.md` and say the actions are recorded at Phase 3F. Neither this repo nor upstream keeps a `SESSION_NOTES.md`: both write an entry at the claim — the fork a new one per commit, upstream one it edits at close-out — and the *fork* hook exempts a claim commit from having any entry (`.githooks/pre-commit:53–120`) | P4, P5 |
| C8 | One entry per action, or per session | runner :278 (*"one per commit and per non-commit action"*) — against upstream's practice: each of S13–S17 wrote one entry at its claim and rewrote 1–2 lines of it at close-out | P4 |
| C9 | A proposed guard that would refuse every trim | upstream's S16 receipt, next step (e): refuse a commit whose staged `CHANGELOG.md` has fewer `### ` headings than `HEAD`'s. Every trim lowers that count by design (`aaa6d30`: 80 → 27) | P2, P12 |
| C10 | An audit that miscounts, or fails | seed :24, runner :39 and upstream's root `CHANGELOG.md:14` publish the unanchored, one-file form. The seed's own shard rule (:160–162) says an enumeration must span the shards, and *fork* root :22–25 records the unanchored form counting 78 against 64. The shard-spanning glob form in turn fails under zsh wherever no shard exists: *"no matches found"*, then 0 (bash: 43, on `b82dcff`) | P3 |
| C11 | What the file is | *"Completed work history":* `BOOTSTRAP.md` :23, :107, :131; `README.md` :96, :114, :200; `CLAUDE.md:51`. *Completed-work framing:* `BOOTSTRAP.md` :139, :145 — against the seed's action ledger, which also records non-commit actions and declines (:3–8, :30–32) | P4 |
| C12 | Distributed seeds cite fork-only material | Both seeds' *Lines* rows (seed :103, `HANDOFFS.md` seed :97) cite `BL-52` and `docs/planning/read-cap-premise-correction-plan.md`; neither exists on `b82dcff` | P2 |
| C13 | Where a month section starts | seed :92 (*"promote … as the list grows"*); *fork* root :48–52 (prepend under the topmost `## YYYY-MM`, open a new one when the month changes); upstream's root :34 promises sections and has none; `nprcgenekeepr` files September's entries under `## 2026-08` | P4 |
| C14 | The `HANDOFFS.md` seed repeats C1 and C2 | `starter-kit/HANDOFFS.md:89–125` — the same premise, the same 65,536 B, and a cross-reference (:123) to the `CHANGELOG.md` seed section this plan moves | P1, P2 |
| C15 | BL-47's proposal went stale | BL-47 proposes adding both ledgers to the seed `context-budget.json` at 65,536 B. Under Q2 A the ledger is not a read-budget file, and this repo already dropped it (`3c8acd5`) | S162 records it |
| C16 | The stale-seed advice rewrites entries | `BOOTSTRAP.md:85` and `bin/status:188–192` tell an adopter with a stale seed to *"reconcile its header and per-entry format"* by hand — rewriting committed entries, which Q4 A forbids. P1's marker makes every adopter read stale, so the advice meets all six at once | P1 |

### 1.2 Why they keep coming back

`bin/_manifest.py` ships two kinds of file. **Tracked** files belong to the framework, and `bin/sync`
keeps them current. **Seeds** — `CHANGELOG.md`, `HANDOFFS.md`, `SESSION_NOTES.md`, `ROADMAP.md`,
`.context-budget.json` — are written once and then belong to the adopter, because they hold its history;
sync never touches them again.

The seed `CHANGELOG.md` is a 970 B header, **11,804 B of rules** and a 119 B footer. The rules are *How
to add an entry* (4,517 B), *Size, and when to archive* (6,621 B) and *CHANGELOG.md vs SESSION_NOTES.md*
(666 B). Each adopter holds a snapshot of them from the day it was seeded. The framework has corrected
them since — the *silent truncation* row became *announced* at BL-51's Phase A — and the copies did not
move. Fixing the words without moving them would restart the same drift at the next correction.

A second cost shows in §4.4: the seed's fenced example entries are line-shaped like real ones, so in an
adopter that carries the rules text, a line-based audit counts the examples as entries (`wsfct`: three).

### 1.3 Constraints

- **K1 — PR #80 is under private review.** Its head is `b82dcff`; the maintainer's queue (the S17
  receipt on `upstream/main`) begins *"#80 decision F1 + fixes F2/F3 → merge"*, and F1–F3 are not
  public. This plan adds nothing to #80. It builds on a branch from `b82dcff`, because the seed text it
  changes arrived with #80 (PR #77, `56997af`) and does not exist on `upstream/main`.
- **K2 — The Phase 0 read has no spare bytes.** On `b82dcff`, `context_budget.py` exits 2: runner
  52,195 B against its 41,364 B ceiling, the read-set 67,581 B against 56,750 B. On the simulated
  post-merge tree (`upstream/main` ⊕ `b82dcff`, tree `e48a828e`), upstream's S16 paragraph also takes
  `SAFEGUARDS.md` to 16,353 B against 15,386 B. **This plan never grows the runner, and never touches
  `SAFEGUARDS.md`.**
- **K3 — The maintainer's queue shares two files.** After #80: v3.8; the S16 follow-ups
  (`commit-msg --selftest` in `bin/tests.sh`, `BOOTSTRAP.md` Step 10); quality-ratchet Phase 1
  (`SESSION_RUNNER.md`'s FM #17 row, Degradation table and Phase 3C routing, plus `SAFEGUARDS.md`,
  `ITERATIVE_METHODOLOGY.md` and a Learning row); then the ledger-count ratchet.
- **K4 — Learning numbers diverge between the trees.** `b82dcff`'s table stops at #47 and fork `main`'s
  at #64; upstream's `docs/operator-gated-review-plan` reserves #14. **The PR adds no Learning row.**
- **K5 — Operator decisions in force.** Do not trim this repo's `CHANGELOG.md` (2026-09-14).
  `CHANGELOG.md` is out of this repo's read budget (`3c8acd5`). `HANDOFFS.md` keeps four receipts (S127).
- **K6 — Every outward action is its own go-ahead** — pushing the branch, opening the PR, any comment on
  #80 (`CLAUDE.md` §Contributing upstream).
- **K7 — Seeds are migrated by hand, in each adopter's own session** (the runner's session-notes
  boundary). Sync never rewrites one.
- **K8 — Every command the rules publish must run in zsh and in bash.** zsh is the macOS default shell,
  and it aborts a command whose glob matches nothing (C10).

---

## 2. Decisions

### 2.1 Answered by the operator at S162 (2026-09-14)

| # | Question | Chosen | Not chosen |
|---|---|---|---|
| Q1 | Where the rules live | **A — one synced home**, `FRAMEWORK_APPARATUS.md` §The Action Ledger; the seed keeps a pointer and a format marker | B: keep the rules in the seed and flag stale copies. C: move only the size rules |
| Q2 | The archive rule | **A — optional.** Nothing reads the ledger whole, so no size is stated and the trimmer stays available; past the default-read refusal, read with offset/limit | B: mandatory at the trimmer's trigger. C: each project records its choice |
| Q3 | Source tags | **A — `[BL-<id>]` takes any backlog id.** Three families, one per entry; the audit is anchored and spans shards | B: numeric ids only. C: an open vocabulary |
| Q4 | Entries | **A — one per commit, never edited.** A claim's entry says *(in progress)* and close-out adds its own. A correction is a new entry; the one exception is removing content that must not be published, recorded by an entry of its own | B: one per session, edited until close-out (the maintainer's practice). C: fix only the wording |

Q4 was chosen after comparing A and B on measurement. Of this fork's last 60 commits that touched the
ledger, 56 only inserted, three edited a committed entry (`7a6ea4b`, `7b30980`, `e48ffa9`) and one
trimmed (`aaa6d30`). Upstream's S13–S17 each rewrote their own entry at close-out. S16's rewrite, done
by a script that searched for the wrong boundary, deleted ten other entries (`356556f`: 40 → 30
headings; restored in `ed98444`).

### 2.2 Recommended — approved with this plan unless the operator says otherwise

- **D5 — Route.** A **new** upstream PR, opened after #80 merges, from branch `bl57/changelog-rules`
  (created from `b82dcff`) brought onto `upstream/main` at P12. Not commits on #80 (K1). A stacked PR
  against `read-set-budgets` only if #80 is still open when P12 is ready, and only on the operator's
  choice then.
- **D6 — Rollout.** Adopters migrate after P5, before the PR merges: from fork `main` (Route B), or from
  the branch for `airqino` (Route A). Thin seeds make that safe: if review changes the text, the change
  reaches adopters by sync and the hand migration is not repeated. The PR does not wait for them.
- **D7 — `HANDOFFS.md`'s own archive rule stays as it is**, apart from C1, C2 and C12's defects in its
  seed. Extending Q2 A to it is left to the operator (§8).
- **D8 — Two upstream-root changes, each its own commit.** (i) Upstream's root `CHANGELOG.md` front
  matter, the maintainer's own file: its pointer to the seed's rules (:11–12), which P1 makes false; its
  audit (:14); and its month sentence (:34). (ii) `CHANGELOG.md` leaves upstream's root
  `.context-budget.json` (this fork's `3c8acd5`, same reasoning). The PR body says either can be dropped,
  and that dropping (i) leaves :11–12 pointing at a seed that no longer holds the rules.
- **D9 — Markers.** `CHANGELOG.md` keys on a new versioned token on the seed's pointer line (§3.2).
  `HANDOFFS.md` keys on the heading `Size, and when to archive` on both trees — fork `main`'s S41 choice,
  brought upstream — so its seed keeps that heading.
- **D10 — The fork hook's claim carve-out goes.** *Fork* `.githooks/pre-commit:16–17`, `:53–120` and
  `:144` let a claim commit carry no entry, and *fork* Test 27 (`bin/tests.sh:1195–1700`) pins that.
  Under Q4 A a claim commit carries an *(in progress)* entry. Both upstream's claims (S13–S17) and this
  fork's recent ones (`7ea7346b`) already do, and `b82dcff`'s hook has no carve-out. P5 removes it and
  its test; the operator can keep it instead, in which case §The Action Ledger must state the exception.

---

## 3. Target state

### 3.1 The one home: `FRAMEWORK_APPARATUS.md` §The Action Ledger

A seventh top-level section, beside the six the file already holds (it lands in adopters at
`docs/methodology/FRAMEWORK_APPARATUS.md`). In order:

1. **What counts as an action** — any commit, and every non-commit action (release, tag or branch
   operation, PR open, upstream issue close, access grant, decline or grooming decision). Re-expressed
   from the seed (:3–8, :30–32).
2. **The entry format** — `### YYYY-MM-DD · [SOURCE] outcome`, the detail bullets, the optional
   **Model:** bullet and the capability-tiered examples. Moved from the seed (:34–87).
3. **Source tags** — `[issue #<N>]`, `[BL-<id>]` (whatever id the project's backlog uses) and
   `[ad hoc]`; exactly one per entry. The audit, which runs in zsh and bash alike (K8) and reads the
   committed shards:

   ```
   cat CHANGELOG.md $(git ls-files 'docs/archive/CHANGELOG-*.md') \
     | grep -cE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[(issue #[0-9]+|BL-[^]]+|ad hoc)\]'
   ```

   Entries written before a project adopted the vocabulary stay as written; the audit does not count
   them.
4. **Lifecycle** — one entry per commit (the co-staging hook's unit) and one per non-commit action.
   - A claim commit carries an *(in progress)* entry; close-out adds its own entry.
   - A committed entry is never edited. A correction is a new entry naming what was wrong. The one
     exception is removing content that must not be published, recorded by an entry of its own.
   - A Phase 0 backfill is the one entry that may span several commits.
   - The Phase 1B `CHANGELOG: pending` marker lives in `SESSION_NOTES.md`; a project that keeps none
     relies on its pending `HANDOFFS.md` receipt.
5. **Placement** — prepend under the topmost `## YYYY-MM`, and open a new month heading above it when
   the month changes. A ledger that has no month headings starts them at its next new month; nothing is
   retrofitted. Entries stay at `###`, the level the tools key on.
6. **Reading the ledger** — never whole. Phase 0 takes a frontier from `git log`, close-out reads the
   top, and a lookup uses `grep` or `git log`. Past the harness's default-read refusal
   (`READ_REFUSE_BYTES`, `methodology_trim.py:130`), read with offset/limit.
7. **Archiving** — optional. `methodology_trim.py` does it losslessly for a project that wants it, and
   its `--check` is the only statement of a trigger; the rules name no size. The shard convention moves
   from the seed (:145–165). A trim is its own action with its own entry, never in Phase 0.
   **Conservation:** the live file and its shards together never lose an entry, so a count check counts
   both, as the audit in item 3 does — never the live file alone.
8. **Three files, three questions** — `SESSION_NOTES.md`, `HANDOFFS.md`, `CHANGELOG.md`. Moved from the
   seed (:176–183), with its read premise (:180–181) corrected in P2.

Expected size: 9–11 KB. P1 moves 11,804 B verbatim; P2 condenses the two-cap table and its
rate-versus-level argument, which Q2 A no longer needs.

### 3.2 The thin seed, `starter-kit/CHANGELOG.md` (about 1.5 KB)

It keeps the title (`bin/tests.sh:276` and the dashboard's fixtures use it). Then comes a purpose line,
still naming FM #27, the Phase 3F write and the Phase 0 reconcile as :5–8 did. Then **the pointer, as a
relative Markdown link carrying the marker**, so `bin/check-links` can prove it resolves — for example:

```
Entry format, source tags and archiving:
[§The Action Ledger](docs/methodology/FRAMEWORK_APPARATUS.md#the-action-ledger)
(ledger-format: 2 — keep this line; bin/status reads it)
```

— then the sentinel, `---` and the entries comment. P1 settles the wording. The marker must meet four
tests: it is absent from **every** earlier version of the seed; it sits in the front matter the trimmer
pins; it is on a line the seed tells adopters to keep; and it carries a version number the next format
change bumps.

### 3.3 The `HANDOFFS.md` seed

The heading at :89 stays (it is the marker, D9). P1 turns its cross-reference (:123–125) into a pointer to
§The Action Ledger. P2 corrects its read premise (:91, :150–151) and removes its 65,536 B row (:98) in
favour of the tool's trigger. The receipt-specific rules (:127–144) do not change.

### 3.4 Everywhere else: wording only

The runner, `ITERATIVE_METHODOLOGY.md`, `HOW_TO_USE.md`, `BOOTSTRAP.md`, `README.md`, `CLAUDE.md`, the
stale-seed advice in `bin/status`, the hook's refusal text and two trimmer comments (§4.2).

### 3.5 What does not change

- The failure-mode count (28), and FM #27's requirement that every action be recorded.
- The upstream hook's behaviour, and Phase 0 reconcile.
- The trimmer's behaviour and grammar: `methodology_trim.py:307` already accepts any bracket.
- The dashboard. Upstream has no read-cap code, and the fork's comments were already corrected (*fork*
  `starter-kit/methodology_dashboard.py:325–345`).
- `bin/model-report`: *fork* `:72` already accepts any bracket.
- **Any existing ledger entry anywhere** — nothing is retagged or rewritten (Q4 A).

---

## 4. Evidence inventory

### 4.1 How it was produced

The inventory is `git grep -n -I -i -E` over three refs — `b82dcff`, `upstream/main` and fork `main` —
with twelve patterns:
- `changelog`, `ledger`, `prepend`, `newest[- ]on[- ]top`, `append`;
- the byte constants with their derived neighbours (`65,?53[56]|196,?60[78]|262,?14[34]|98,?30[34]|56,?750`);
- `CLASS_A|READ_REFUSE|DEFAULT_BUDGET`;
- `source[- ]tag|ad hoc\]|\[BL-`;
- `SEED_FORMAT|Authoritative Action Ledger|when to archive`;
- `context-tax|watched`, `reconcile`, `\btrim`.

It excluded the ledgers themselves, `docs/archive/`, `docs/planning/`, `docs/RELEASE_HISTORY.md`,
`dashboard.html`, `*.jsonl` and `LICENSES`. It returned **1,577 lines in 45 files on `b82dcff`**, 905 in
39 on `upstream/main` and 2,679 in 48 on fork `main`, each read and classified below. The independent
review reproduced all three counts. The command is §9.1; re-run it at the start of every phase.

### 4.2 Sites that change

**D** = distributed, tracked; **S** = distributed seed; **C** = canonical-only. The fourteen
rule-bearing files are marked ●.

| File | Kind | Lines (`b82dcff`) | *Fork* `main` | Phase |
|---|---|---|---|---|
| ● `starter-kit/CHANGELOG.md` | S | :15–92, :94–174, :176–183 moved verbatim; :3–8 re-expressed in the purpose line; the thin seed | identical | P1 |
| `FRAMEWORK_APPARATUS.md` | D | new §The Action Ledger; intro :9–11 (*"The six sections below were moved here verbatim"*) | identical | P1–P4 |
| ● `starter-kit/HANDOFFS.md` | S | :123–125 (P1); :91, :97–98, :150–151 (P2) | identical | P1, P2 |
| ● `bin/_manifest.py` | C | :78–98 (comment and `SEED_FORMAT_MARKERS`) | :125–128 | P1 |
| ● `bin/status` | C | :188–192 (the stale-seed advice) | identical | P1 |
| `bin/tests.sh` | C | :266–303 (seed-marker fixtures; the title-only fixture is :276) | :290–305 | P1 |
| `tools/test_methodology_trim.py` | C | :238–253, :1824–1829, :2003–2007 and :2027–2035 change; :1692–1693, :1749, :1757, :1792, :1797, :1918, :2169–2175 must stay green | identical | P1 |
| ● `starter-kit/methodology_trim.py` | D | :358–363 (comment: *"the seed files are the proof"*) in P1; :186 (comment) in P2 | identical | P1, P2 |
| ● `HOW_TO_USE.md` | D | :748 (apparatus row, *"~330 lines"*), :767, :804 | differs by 2 lines | P1, P4 |
| ● `CLAUDE.md` (upstream's) | C | the Document Hierarchy row for `FRAMEWORK_APPARATUS.md`; :51 | :69 | P1, P4 |
| ● `.context-budget.json` (upstream root) | C | the `CHANGELOG.md` entry | already removed (`3c8acd5`) | P2 (D8 ii) |
| ● `starter-kit/SESSION_RUNNER.md` | D | :39, :88, :278, :329, :357 | :39, :88, :284, :335, :363 | P3, P4 |
| ● `ITERATIVE_METHODOLOGY.md` | D | :169, :294 | identical | P3, P4 |
| ● `.githooks/pre-commit` | C | :56–57 | differs (and has the carve-out, D10) | P3, P4 |
| ● `starter-kit/BOOTSTRAP.md` | D | :85 (C16) in P1; :23, :107, :131, :139, :145 in P4 | :23, :108, :133, … | P1, P4 |
| ● `README.md` | C | :96, :114, :200 | :114, :201, … | P4 |
| ● `CHANGELOG.md` (upstream root) | C | :11–12, :14, :34 — one commit (D8 i) | the fork's own — P5 | P4 |

**Fork-only (P5):**
- Root `CHANGELOG.md` front matter: the pointer (:11–12); the audit (:17–20), which takes `BL-[^]]+` and
  the cross-shell form; *When to archive again* (:105–141); and a new paragraph on this repo's claim
  practice.
- Root `HANDOFFS.md:15` (C4).
- The hook's carve-out and Test 27 (D10).
- The port of every file above.

### 4.3 Checked and unchanged

- **Consistent already:** runner :11, :24, :35–44 (reconcile mechanics), :91, :146, :159;
  `ITERATIVE_METHODOLOGY.md` :142, :148, :153, :160, :325, :425; `SAFEGUARDS.md` :117, :165–173 (the hook
  section, also left alone because of K2); `BOOTSTRAP.md` :136, :383 (already say the ledger is not read
  at session start — the statement C1 converges on), :323–325; `FRAMEWORK_APPARATUS.md:207`; every
  campaign checklist line *"recorded in `CHANGELOG.md` (Phase 3F ledger entry, failure mode #27)"*
  (`workstreams/*_CAMPAIGN.md`).
- **Tutorials:** T1 :86–92, :125–131; T2 :54, :89, :98–99; the T2 worked transcript :251–262 (prepend;
  *one action, one commit*; `[BL-F1]`, which conforms under Q3 A); T8 :57, :75–105, :179 (the
  `bin/status` output is still accurate).
- **No code change for Q3 A:** `methodology_trim.py:307` (`^### \d{4}-\d{2}-\d{2} · \[`), the dashboard's
  `_DATED_ENTRY_RE` (:210) and *fork* `bin/model-report:72` (`\[[^\]]+\]`) all accept any bracket.
- **History, never edited:** `README.md`'s *What's New*; `CLAUDE.md`'s version lines;
  `docs/RELEASE_HISTORY.md`; the `FRAMEWORK_LEARNINGS.md` rows that mention ledgers (append-only; on
  `b82dcff`, `grep -i ledger` finds rows 8, 9, 13, 15, 16, 17, 18, 22, 24, 26, 28, 31, 32, 35, 36, 39 and
  41); `docs/archive/`; `docs/audits/`; `docs/planning/`.

### 4.4 The adopters (measured 2026-09-14, read-only)

*Conform* counts headings in the live ledger plus its shards that match the audit, under the current rule
and then under Q3 A (§9.2). `/usr/bin/grep` and Python agree on the pattern.

| Adopter | State | `CHANGELOG.md` | Rules text it carries | Conform: now → Q3 A | Route (S161; re-derive) | Blockers and notes |
|---|---|---|---|---|---|---|
| `airqino` | branch `chore/methodology-read-set-budgets`, off open PR #1; 2 untracked | 1,309 B, pre-v3.1 template | none | 1 → 1 of 1 | runner is `b82dcff`'s; A | BL-56 (reseed); BL-54 if synced from fork `main` |
| `model_project_constructor` | `master`, clean | 666,365 B; Keep-a-Changelog layout, `### date — summary` | none | 0 → 0 of 155 | runner customized; refuses both | runner step 5 is a real customization; a format decision; no `HANDOFFS.md`, no trimmer. BL-57 names the `~/Development` checkout; the second, under `mpc_tests/`, is not included |
| `mts-system` | `master`, clean | 358,377 B; title and v3.1 intro, entries from :10 | none | 96 → 261 of 262 | B clean | hook enabled; `HANDOFFS.md` is 372,830 B (out of scope) |
| `nprcgenekeepr` | `master`; 9 untracked | 413,383 B; custom intro, a legacy block | an older seed copy at :3946–:4065, between two runs of entries (the first at :19, the next at :4070); *silent* :3982, 65,536 :3983 | 599 → 784 of 1,090 (live + 6 shards; 2 of the headings are the block's own) | refuses both | a 49-line local extension of `methodology_trim.py` blocks every sync; September's entries under `## 2026-08`; `CLAUDE.md:271` (S325, *"freeze legacy, go forward"*) |
| `vscode_quarto_ext` | `master`; 1 untracked | 87,837 B; Keep-a-Changelog header, `## [Unreleased]` | none | 236 → 247 of 257 (live + 1 shard) | runner is fork `main`'s; B clean | `[BACKLOG: …]` tags; its `.context-budget.json` lists `CHANGELOG.md` |
| `wsfct` | `master`, clean | 162,549 B | the full older seed copy, :13–196 (*silent* :101, 65,536 :102) | 130 → 130 of 133 (live + 3 shards) — **both include 3 fenced examples** in the block, which holds 5 `### ` lines; real entries: 127 of 128 | runner is fork `main`'s; B clean | `CLAUDE.md` :43, :218, :695 call it *"Completed work history"*; :162, :206 frame it as completed work |

This repo: 494 → 494 of 494 (live + 11 shards). `b82dcff`'s root ledger: 43 of 43.

---

## 5. Phases

### 5.0 How every phase works

- **Records go on fork `main`.** Each phase runs Phase 0, the claim and the close-out there (receipt
  and fork ledger).
- **The canonical work goes on a branch.** P1–P4 work on `bl57/changelog-rules`, created at P1 from
  `b82dcff` and checked out in its own worktree (`git worktree add ../methodology-bl57
  bl57/changelog-rules`), so `main` and the branch never share a working directory.
- **Each branch commit carries its own entry in the branch's `CHANGELOG.md`** — upstream's ledger — as
  #76–#79's did. The hook requires it and Q4 A defines it. Upstream's front matter (`upstream/main`
  :20–23) already accepts `[BL-<N>]` entries for work that originates in the fork.
- **Five files per commit at most**, the ledger included (`SAFEGUARDS.md` §Blast Radius Limits).
- **Suites run only in a `git clone --no-local`**, because `bin/tests.sh` rewrites both live ledgers.
  Such a clone copies only this repo's branches: fetch the ref first (hazard 12).
- **Commit before running the trimmer suite:** its seed fixtures read `HEAD:starter-kit/CHANGELOG.md`
  (`tools/test_methodology_trim.py:1692–1693`), not the working tree.
- **Every command a phase publishes runs in zsh and in bash** (K8).
- **Baseline at `b82dcff`**, taken at plan time in a `--no-local` clone that fetched the ref:
  - `bin/tests.sh`: 115 passed / 1 failed, exit 1. The failure is Test 9, `github source dry-run
    failed`, which reads GitHub's upstream `main` and fails on every tree until #80 merges.
  - Unit suites: 450 tests, OK (4 skipped).
  - `bin/check-links`: OK, 105 links across 23 distributed files.
- **Baseline at fork `main` `7ea7346b`:** `bin/tests.sh` 304 passed / 1 failed / 0 skipped, exit 1 (the
  same Test 9).

### P1 — One home, thin seeds, one stale-seed rule (structure only; no rule changes)

**Scope.**
1. `FRAMEWORK_APPARATUS.md`: add `## The Action Ledger` holding the seed's three rule sections
   **verbatim**, one heading level down — outside fences only, since the seed's fenced example entries
   (:37–43, :52–58, :64–76) are text, not headings. Update the intro (:9–11), which says the file holds
   six sections moved from `ITERATIVE_METHODOLOGY.md`.
2. `starter-kit/CHANGELOG.md`: the thin seed (§3.2).
3. `starter-kit/HANDOFFS.md:123–125`: point at the new home instead of the seed's section.
4. `starter-kit/methodology_trim.py:358–363`: the comment says the seeds' fenced examples *"are the
   proof"* of fence-awareness; after the move they live in the home and the tests' fixture. Comment only.
5. `bin/_manifest.py:78–98`: `CHANGELOG.md` keys on the new marker; `HANDOFFS.md` keys on
   `Size, and when to archive` (D9). Rewrite the comment, stating *fork* Learning #19's rule inline — a
   marker keyed to something that never changes across versions cannot fire — rather than citing its
   number: after #80's F1 (a), no row past #13 exists upstream (amended at S163).
6. **The stale-seed advice (C16).** `BOOTSTRAP.md:85` and `bin/status:188–192` describe the thin-seed
   migration: replace the rules text above the first entry with the current seed's header; leave every
   entry as written; reseed only a file that holds no history. The marker makes every adopter read stale
   in this same phase.
7. Tests:
   - `bin/tests.sh:266–303` — the in-use fixture at :276 is title-only and would read stale under the
     new marker, so give it the marker line. Add a fixture holding the pre-P1 seed (a frozen literal)
     that must read *present (stale format)*.
   - `tools/test_methodology_trim.py:238–253` and `:2027–2035` — three fence-awareness controls assert
     that *the live seed* holds probe-shaped example lines inside fences, and those lines leave. Move
     them onto one frozen literal fixture in the test file, not onto a pinned sha, which a fork clone may
     not hold.
   - `:1824–1829` — the `.replace()` anchor `## How to add an entry` leaves the seed. Choose an anchor
     the thin seed has and assert it occurs exactly once before replacing, or the test passes without
     testing anything.
   - `:2003–2007` — a docstring cites `starter-kit/CHANGELOG.md:10`; re-cite it.
8. `HOW_TO_USE.md:748` (the apparatus row's use column and *"~330 lines"*) and upstream `CLAUDE.md`'s
   Document Hierarchy row for `FRAMEWORK_APPARATUS.md`.

Suggested commits, each green:
1. the test refactor (green with either seed);
2. the move — `FRAMEWORK_APPARATUS.md`, both seeds and the trimmer comment;
3. the marker and its advice — `bin/_manifest.py`, `bin/tests.sh`, `bin/status` and `BOOTSTRAP.md`;
4. `HOW_TO_USE.md` and `CLAUDE.md`.

**DONE — all of these hold.**
- **The move is verbatim.** Each of the seed's three sections at `b82dcff`, with its headings demoted
  one level outside fences, occurs byte for byte in `FRAMEWORK_APPARATUS.md` (§9.3; the check caught all
  four mutants it was tried on at S162).
- **The thin seed is still a fresh seed.** `starter-kit/CHANGELOG.md` is ≤ 1,600 B with no `## `
  section. It keeps its title, sentinel and footer, and its purpose line names FM #27, Phase 3F and the
  Phase 0 reconcile. The trimmer reports `NO_RECORDS` (exit 0) on it, and `bin/sync` into an empty
  scratch directory seeds it.
- **The marker discriminates.** It occurs in the new seed and in no earlier version of it on any ref
  (§9.4).
- **The pointer resolves.** It is a Markdown link, and `bin/check-links` resolves it in the simulated
  adopter tree. `grep -c '^## The Action Ledger$' FRAMEWORK_APPARATUS.md` is 1.
- **The advice no longer rewrites entries.**
  `grep -n 'per-entry format' starter-kit/BOOTSTRAP.md bin/status` prints nothing.
- **`bin/status` from the branch gives the expected verdicts:**
  - `present` on the fresh scratch target;
  - *present (stale format)* for `CHANGELOG.md` on scratch copies of all six adopters, none of which is
    migrated yet, with the new advice beneath;
  - `HANDOFFS.md` verdicts equal to fork `main`'s `bin/status` on the same copies.
- **All three suites are green against the baseline**, every changed row named.

**Surface.** The branch worktree; suites in a `--no-local` clone of the branch; scratch copies of the six
adopters holding exactly what `bin/status` reads — never an empty target (*fork* Learning #64). **Cannot
enforce:** that a reader follows the pointer rather than guessing, or the anchor as GitHub renders it
(`check-links` resolves the file, and the grep checks the heading).
**One session. STOP.** Reasoning: the deepest available — a distributed seed and the tests that guard it.

### P2 — Reading and archiving (C1, C2, C4, C9, C12, C14)

**Scope.**
1. §The Action Ledger: rewrite the moved *Size, and when to archive* text to Q2 A (§3.1 items 6 and 7):
   - the three reads the protocol actually makes, and never a whole read;
   - offset/limit past `READ_REFUSE_BYTES`;
   - archiving optional, with the tool's `--check` as the only trigger statement;
   - the shard convention;
   - a trim is its own action, never in Phase 0;
   - conservation across the live file and its shards (C9).
   Also correct the read premise in the moved *three files* text (from seed :180–181).
2. `starter-kit/HANDOFFS.md`: keep the heading (:89). Replace the premise (:91, :150–151) and the
   65,536 B row (:98) with a pointer to the shared reasoning and to the tool's trigger. The file's own
   rule otherwise stands (D7).
3. `starter-kit/methodology_trim.py:186`: correct the comment. Nothing else in the tool changes.
4. Upstream's root `.context-budget.json`: remove the `CHANGELOG.md` entry, in **its own commit** (D8 ii).

**DONE.**
- **The false statements are gone.** Each of these prints nothing:
  - `grep -nE "reads it every session|every session pays|outgrows a session's read" starter-kit/CHANGELOG.md starter-kit/HANDOFFS.md FRAMEWORK_APPARATUS.md`
  - `grep -nE '65,536|BL-52|read-cap-premise-correction-plan' starter-kit/CHANGELOG.md starter-kit/HANDOFFS.md FRAMEWORK_APPARATUS.md`
  - `grep -n 'context-tax budget' starter-kit/methodology_trim.py`
- **The trimmer only changed comments.** `git diff b82dcff -- starter-kit/methodology_trim.py` changes
  comment lines only (P1's and this one), and the trimmer suite is green.
- **§The Action Ledger states each rule:** the three reads, *optional*, the tool as the only trigger,
  *never in Phase 0*, and conservation. The session's ledger entry quotes each rule's sentence with its
  line number in `FRAMEWORK_APPARATUS.md`, so the claim can be checked by reading.
- **Suites and `bin/check-links` are green.**

**Surface.** As P1. **Cannot enforce:** what *optional* does to ledger growth, which shows only across
later sessions; or the 256 KiB refusal itself, which no test here can exercise (*fork*
`starter-kit/methodology_dashboard.py:284–287` says the same).
**One session. STOP.** Reasoning: the deepest available — this is the rule adopters will run on.

### P3 — Source tags and the audit (C6, C10)

**Scope.**
1. §The Action Ledger's tag text and audit (§3.1 item 3). Pre-vocabulary entries stay as written and are
   not counted.
2. `starter-kit/SESSION_RUNNER.md`:
   - `:39` drops its inline grep for a pointer to the home (net bytes ≤ 0);
   - `:278` and `:329` change `[BL-<N>]` to `[BL-<id>]`.
3. `ITERATIVE_METHODOLOGY.md:294` and `.githooks/pre-commit:57`: the same change.

**DONE.**
- `grep -nF '[BL-<N>]'` over the runner, `ITERATIVE_METHODOLOGY.md`, `HOW_TO_USE.md`, the hook, the home
  and both seeds prints nothing.
- **The audit gives the same count in zsh and bash** (§9.2b):
  - on the branch's root ledger, which has no shards, it equals the heading count;
  - on this repo's 11 shards it gives 494;
  - on each adopter copy it gives the §4.4 figures. A changed figure is a finding: explain it before
    closing.
- `wc -c starter-kit/SESSION_RUNNER.md` is no larger than at P3's start.
- Suites are green.

**Surface.** As P1. **Cannot enforce:** that adopters' future entries use `[BL-<id>]`.
**One session. STOP.** Reasoning: high.

### P4 — Entry lifecycle and the words (C3, C7, C8, C11, C13)

**Scope.**
1. §The Action Ledger items 4 and 5 (§3.1).
2. "Append … newest on top" becomes "prepend … newest on top" at:
   - runner :278, :329, :357;
   - `ITERATIVE_METHODOLOGY.md:294`;
   - `HOW_TO_USE.md` :767, :804;
   - `.githooks/pre-commit:56`.
3. Runner :88 and `ITERATIVE_METHODOLOGY.md:169`: the claim commit carries an *(in progress)* entry, and
   Phase 3F records the rest. Byte-neutral wording.
4. "Completed work history" and its framing become the action ledger at `BOOTSTRAP.md` :23, :107, :131,
   :139, :145, `README.md` :96, :114, :200, and `CLAUDE.md:51`.
5. Upstream's root `CHANGELOG.md` front matter — :11–12, :14 and :34 — in **one commit** (D8 i).

At least three commits.

**DONE.**
- `grep -nE '[Aa]ppends? (a|one) dated|Append the owed entry'` over the runner,
  `ITERATIVE_METHODOLOGY.md`, `HOW_TO_USE.md` and the hook prints nothing.
- `grep -ni 'completed work history'` over `BOOTSTRAP.md`, `README.md` and `CLAUDE.md` finds only history
  (`README.md`'s *What's New*). List what remains, and why.
- §The Action Ledger states every rule in §3.1 items 4 and 5. The ledger entry quotes each with its line
  number, as in P2.
- **`starter-kit/SESSION_RUNNER.md` is no larger than at `b82dcff` (52,195 B), `starter-kit/SAFEGUARDS.md`
  is unchanged,** and the read-set total `python3 starter-kit/context_budget.py` reports is no larger than
  at the baseline (§9.7).
- Suites and `bin/check-links` are green.

**Surface.** As P1, plus `context_budget.py` on the branch tree. **Cannot enforce:** that the
maintainer's practice changes. Q4 A asks it to; the PR presents the evidence, not a verdict.
**One session. STOP.** Reasoning: high.

### P5 — Fork `main` adopts it

**Scope.**
1. **The port.**
   ```
   git diff b82dcff bl57/changelog-rules -- . ':!CHANGELOG.md' ':!HANDOFFS.md' ':!.context-budget.json'
   ```
   Apply it to `main` with `git apply -3` in commits of at most five files, each with its fork ledger
   entry. `.context-budget.json` is excluded because fork `main` already removed the entry (`3c8acd5`) and
   its blob differs.
   - Resolve the hunks in files where `main` differs from `b82dcff`: `SESSION_RUNNER.md`,
     `BOOTSTRAP.md`, `HOW_TO_USE.md`, `README.md`, `CLAUDE.md`, `bin/_manifest.py`, `bin/tests.sh` and
     `.githooks/pre-commit` (`git diff --stat b82dcff main`).
   - Fork `main` already keys `HANDOFFS.md` on the S41 marker, so only the `CHANGELOG.md` row changes
     there.
2. **This repo's own ledgers.**
   - Root `CHANGELOG.md` front matter: the pointer at :11–12 goes to the home.
   - The audit at :17–20 takes `BL-[^]]+` and the cross-shell form.
   - *When to archive again* (:105–141) becomes the operator's 2026-09-14 decision plus a pointer.
   - A new paragraph records this repo's claim practice (C7): the claim commit carries an *(in
     progress)* entry, and the crash breadcrumb is the pending receipt, because this repo keeps no
     `SESSION_NOTES.md`.
   - Root `HANDOFFS.md:15`: Phase 0 **counts and reports**; the trim is its own action after the report
     (C4).
3. **The hook's claim carve-out (D10).** Remove it (*fork* `.githooks/pre-commit:16–17`, `:53–120`,
   `:144`) and its Test 27 (`bin/tests.sh:1195–1700`), unless the operator keeps it. In that case
   §The Action Ledger must state the exception, and that change travels upstream too.

**DONE.**
- **Identical files stay identical.** Every distributed file that was byte-identical between `main` and
  `b82dcff` when P5 began is byte-identical to the branch's version afterwards (blob equality, §9.6 —
  list them). A project synced from fork `main` then gets exactly the bytes the PR proposes for those
  files.
- **The audit count is unchanged:** 494 in zsh and bash alike, because this repo uses numeric ids only.
- **The carve-out decision is recorded.** If it was removed, a claim commit staging only `HANDOFFS.md`
  is refused. Show it with a real `git commit` in a scratch clone.
- **Fork suites are green** against the fork's baseline (§5.0), less Test 27 if it was removed.
- **`bin/status` from fork `main`** on the six scratch copies reads `CHANGELOG.md` *present (stale
  format)* until each adopter migrates; tracked files read as before, or upgradable.

**Surface.** Fork `main`; suites in a `--no-local` clone; scratch adopter copies. **Cannot enforce:** that
the later resync with upstream is clean. That is a separate task, and fork `main` already conflicts with
`upstream/main` in both ledgers.
**One session. STOP.** Reasoning: high.

### P6–P11 — The adopters (one session each, in that adopter's repository)

Each session is that project's own work, with its own Phase 0, claim, ledger entry and receipt (the
runner's session-notes boundary rule).

1. Run `bin/status` from the source checkout: fork `main` for Route B, the branch for Route A. Decide the
   route from its output; §4.4 is only where to start (S161 §3).
2. Sync the tracked files: a dry run, then for real.
3. Migrate the `CHANGELOG.md` seed by hand. Replace the rules text or old header — the *block*, with its
   line range recorded before editing — with the thin header, and leave **every entry byte-identical**.
4. Bring the project's `CLAUDE.md` ledger wording into line, and record any legacy tag format or layout as
   an adaptation.
5. Verify, as below.

**DONE, for each adopter.**
- `bin/status` reads `present` for `CHANGELOG.md`.
- **Only the block changed.** Every line the migration commit removed from `CHANGELOG.md` lies inside
  the recorded block (§9.8).
- **The heading count moved as predicted:** `grep -c '^### ' CHANGELOG.md` changed by (the migration's
  own entries) minus (the block's own `### ` lines): 5 in `wsfct`, 2 in `nprcgenekeepr`, 0 elsewhere.
- **The audit count moved as predicted:** it fell by the block's examples that matched it (`wsfct`: 3,
  so 130 → 127) and rose by the migration's own entries.
- The project's own build or test command still passes; the change touches documents only.

**Surface.** The adopter's repository, in its own session. **Cannot enforce:** that its later sessions
follow the rules. Pushing, or opening a PR there, is that project's own go-ahead.
**One session each. STOP after each.** Reasoning: high for P10 and P11, each of which starts with a
decision; medium otherwise.

| Phase | Adopter | Specifics |
|---|---|---|
| P6 | `airqino` | BL-56 folds in: reseed from the thin seed and carry its one entry across, unchanged. Route A from the branch, because its files are the branch's versions; from fork `main`, BL-54 refuses four files. It is on `chore/methodology-read-set-budgets`, off open PR #1 |
| P7 | `wsfct` | Replace the older full seed copy (block :13–196, 5 `### ` lines) with the thin header. Route B. `CLAUDE.md` :43, :218, :695 (*"Completed work history"*) and :162, :206 (completed-work framing) |
| P8 | `vscode_quarto_ext` | Replace the Keep-a-Changelog header (:1–8) with the thin header, keeping the shard pointer. Record the `[BACKLOG: …]` entries as legacy in `CLAUDE.md`. Drop `CHANGELOG.md` from its `.context-budget.json` (Q2 A; the project's call). Route B. `CLAUDE.md` :102, :146 |
| P9 | `mts-system` | Add the pointer and marker under its title and intro (:1–8); its 165 non-numeric `[BL-…]` entries now conform. Route B. Its hook is on, so every commit carries an entry. `CLAUDE.md` :152, :182, :189 |
| P10 | `nprcgenekeepr` | **Decide first.** Its 49-line local extension of `methodology_trim.py` blocks every sync, because one modified file refuses the whole run. Three options: send the extension upstream; migrate the seed only and leave the pointer dangling until it can sync; or `--force`, which discards the extension. Then replace the rules block (:3946–:4065, 2 `### ` lines, between two runs of entries) and record the S325 legacy block and September's `## 2026-08` placement in `CLAUDE.md` (:271) |
| P11 | `model_project_constructor` | **Decide first.** (a) Its runner customization (step 5) moves into `CLAUDE.md` Adaptations before any `--force` sync (*fork* `BOOTSTRAP.md:75`). (b) Its ledger is a release-grouped work log of 143 untagged `### date — …` entries, which the trimmer refuses by design: either adopt the action-ledger format going forward (the S325 *"freeze legacy, go forward"* precedent) or record an adaptation. It has no `HANDOFFS.md` and no trimmer today |

### P12 — The upstream PR (after #80 merges; outward, its own go-ahead)

**Preconditions.** #80 is `MERGED` — if it is still open when the branch is ready, ask the operator:
wait, or a stacked PR against `read-set-budgets`. P1–P5 are done. Adopter migrations are not a
precondition.

**Steps.**
1. Fetch, and compare #80's merged content with `b82dcff`. Re-derive anything it changed in a file this
   plan touches.
2. Run `git merge-tree --write-tree --name-only upstream/main bl57/changelog-rules`, then bring the branch
   onto `upstream/main` (merge or rebase — the operator's choice then).
3. Dry-run `bin/sync` from the branch into scratch copies of all six adopters. Record, per adopter, the
   files it would change and the refusals that already existed (S161 §3).
4. Run the suites in a `--no-local` clone. Re-run §9.1: no contradiction sites should remain.
   `SESSION_RUNNER.md` must be no larger than on `upstream/main`.
5. Draft the PR body:
   - the sixteen findings, before and after;
   - the four decisions;
   - the adopter results;
   - the conservation definition for the proposed count ratchet;
   - D8's two commits and what dropping each would cost;
   - *no Learning row, no failure-mode change*.
6. Ask the operator for the go-ahead to push the branch to `origin` and open the PR.

**DONE.** `gh pr view <N> --repo KJ5HST/methodology --json state,url` reads `OPEN` and the URL is
recorded; a ledger entry records the PR open (a non-commit action); this fork has merged nothing.
**Surface.** GitHub. **Cannot enforce:** the maintainer's decision, or what the merge method does to fork
`main` (S161's unanswered part (b)).
**One session. STOP.** Reasoning: the deepest available.

---

## 6. Hazards

1. **Upstream moves while this runs.** Re-fetch at every Phase 0. If #80's head moves past `b82dcff`
   before P1, start the branch from the new head; after P1, merge the new head into the branch and re-run
   the suites. Re-derive any self-referential number at publish time (*fork* Learning #61).
2. **The maintainer's queue shares two files (K3).** In `SESSION_RUNNER.md`, quality-ratchet Phase 1
   edits the FM #17 row, the Degradation table and Phase 3C routing, while this plan edits :39, :88, :278,
   :329 and :357 — and :357 sits inside that Degradation table. In `BOOTSTRAP.md`, the S16 follow-up edits
   Step 10, while this plan edits :23–:145. Compute the conflicts with `git merge-tree` at P12; do not
   predict them.
3. **The Phase 0 read has no spare bytes (K2).** Every runner edit is net ≤ 0; the rules' detail goes to
   the home, not the runner.
4. **The seed fixtures read `HEAD:`** (`tools/test_methodology_trim.py:1692–1693`), not the working tree.
   Commit inside the clone before running them.
5. **A `.replace()` whose anchor is gone passes silently** (`:1824`). Assert the anchor's count first.
6. **A control that asserts the live seed has a property breaks when the seed changes** (`:238–253`,
   `:2027–2035`). Move such controls onto frozen fixtures before changing the seed.
7. **`bin/tests.sh` rewrites both live ledgers.** Run it only in a `--no-local` clone, never the live tree.
8. **zsh aborts on an unmatched glob** (K8). A shard glob with no shards prints *"no matches found"* and
   runs nothing, so a count reads 0. Use `$(git ls-files '<pattern>')`.
9. **A proposed count ratchet (C9).** If upstream ships one before P12, check that it counts across the
   shards, or every trim fails. Say so in the PR body either way.
10. **Adopter ledgers past 256 KiB** (`model_project_constructor`, `mts-system`, `nprcgenekeepr`). Read
    them with offset/limit; a default read returns nothing.
11. **BL-54.** From fork `main`, `bin/sync` cannot see versions that exist only on a merge's other side.
    That is why `airqino` syncs from the branch.
12. **A `--no-local` clone copies only this repo's branches.** To test `b82dcff` in one, fetch the ref
    first (`git fetch <repo> refs/remotes/upstream/read-set-budgets`). This plan's first baseline attempt
    failed on exactly this, and its `&&` chain then skipped the suite silently.
13. **zsh history modifiers.** `$R:path` is one; it cost a call while taking this inventory. Run loops over
    refs and paths in `bash` or Python.
14. **Learning numbers diverge (K4).** The PR adds no Learning row; this fork's own learnings go to fork
    `main` only.

---

## 7. Alternatives considered, beyond §2.1

| Alternative | Why not |
|---|---|
| Add BL-57's commits to PR #80 | #80 is under private review with a decision (F1) and fixes (F2, F3) pending. Moving its head mid-review costs the maintainer a re-review, and K6 makes it its own go-ahead anyway |
| A stacked PR against `read-set-budgets` now | Reviewable sooner, but it asks for review of a branch whose base is itself unmerged. Kept as an option at P12, only if #80 is still open |
| Migrate adopters only after the upstream merge (D6) | Clean provenance, but it leaves six projects on contradictory rules for as long as review takes. With thin seeds, a change made in review reaches them by sync, so migrating early costs nothing twice |
| Key `CHANGELOG.md` on an HTML comment (D9) | Easy to delete along with the sentinel comment beside it. A token on the pointer line survives, because the line is the pointer |
| Keep keying on the titles (D9) | They never change, so the check cannot fire — Learning #19, which `b82dcff` itself ships |
| Build the heading-count ratchet in this PR (C9) | It is the maintainer's own queued item (S17 receipt). This plan supplies the definition it needs and does not pre-empt it |
| Extend Q2 A to `HANDOFFS.md` (D7) | The operator has not decided it, and `HANDOFFS.md` carries a retention policy here and more tooling than `CHANGELOG.md`. Left open (§8) |
| Keep the fork hook's claim carve-out (D10) | It exempts exactly the commit Q4 A gives an entry, and neither current practice uses it. Kept as the operator's option at P5 |
| Also fix the four code comments that cite fork-only material | They are in #80's own content (§8), not BL-57's rules; P2's check is scoped to the files BL-57 rewrites |

---

## 8. Out of scope, and follow-ons

- **Trimming this repo's `CHANGELOG.md`** — the operator decided not to (2026-09-14).
- **`HANDOFFS.md`'s own archive rule** (D7), and every adopter's `HANDOFFS.md` copy of the shared size
  section. They carry the same premise error, left for a follow-on the operator may raise.
- **A project whose `CHANGELOG.md` is a product changelog** (`model_project_constructor`, and
  `vscode_quarto_ext`'s header). The framework has no documented path for one. P11 decides locally; the
  framework-level question is a follow-on.
- **A permanently red `--check`.** Under Q2 A, `methodology_trim.py --check` keeps exiting 1 on a large,
  deliberately unarchived ledger, and an always-red check cannot report a new problem. A follow-on could
  let a project declare a ledger unarchived.
- **Retagging old entries anywhere** — never (Q4 A).
- **Separate items:** BL-54; BL-55's gate (its join key gains from Q3 A); the fork dashboard's read-cap
  row for `CHANGELOG.md` (BL-52); the fork's resync with upstream.
- **Found and not fixed:**
  - Four comments in two distributed tools cite fork-only material: `methodology_trim.py:201`, `:818`,
    `:821` and `context_budget.py:683`. They arrived with #77 and #79.
  - `docs/tutorials/T2_worked_transcript.md:228` writes `changelog_ref: CHANGELOG.md [BL-F1] entry`,
    not the quoted-heading form the `HANDOFFS.md` seed asks for (:63).

---

## 9. Commands

### 9.1 The inventory (run from the repo root)

```python
import subprocess
refs = {'main': 'main', 'up': 'upstream/main', 'pr80': 'b82dcff'}
pats = [r'changelog', r'ledger', r'prepend', r'newest[- ]on[- ]top', r'append',
        r'65,?53[56]|196,?60[78]|262,?14[34]|98,?30[34]|56,?750', r'CLASS_A|READ_REFUSE|DEFAULT_BUDGET',
        r'source[- ]tag|ad hoc\]|\[BL-', r'SEED_FORMAT|Authoritative Action Ledger|when to archive',
        r'context-tax|watched', r'reconcile', r'\btrim']
excl = [':!CHANGELOG.md', ':!HANDOFFS.md', ':!docs/archive', ':!docs/planning',
        ':!docs/RELEASE_HISTORY.md', ':!dashboard.html', ':!*.jsonl', ':!LICENSES']
for k, r in refs.items():
    args = ['git', 'grep', '-n', '-I', '-i', '-E'] + sum([['-e', p] for p in pats], []) + [r, '--', '.'] + excl
    out = subprocess.run(args, capture_output=True, text=True).stdout
    print(k, len(out.splitlines()), 'lines in', len({l.split(':')[1] for l in out.splitlines()}), 'files')
```

### 9.2 Conformance under the current rule and under Q3 A

(a) The §4.4 figures, over the live ledger and its shard files:

```bash
bash <<'EOF'
NEW='^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[(issue #[0-9]+|BL-[^]]+|ad hoc)\]'
OLD='^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[(issue #[0-9]+|BL-[0-9]+|ad hoc)\]'
for d in methodology airqino model_project_constructor mts-system nprcgenekeepr vscode_quarto_ext wsfct; do
  p=$HOME/Development/$d; files="$p/CHANGELOG.md $(ls $p/docs/archive/CHANGELOG-*.md 2>/dev/null | grep -v verify)"
  echo "$d $(cat $files | /usr/bin/grep -c '^### ') $(cat $files | /usr/bin/grep -cE "$OLD") $(cat $files | /usr/bin/grep -cE "$NEW")"
done
EOF
```

(b) The published form, in each shell. The two outputs must agree; they did at S162, 43 on `b82dcff`,
which has no shards, and 494 on this repo.

```bash
P='^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[(issue #[0-9]+|BL-[^]]+|ad hoc)\]'
zsh  -c "cat CHANGELOG.md \$(git ls-files 'docs/archive/CHANGELOG-*.md') | grep -cE '$P'"
bash -c "cat CHANGELOG.md \$(git ls-files 'docs/archive/CHANGELOG-*.md') | grep -cE '$P'"
```

### 9.3 P1 — the move is verbatim

```python
import re, subprocess
seed = subprocess.run(['git', 'show', 'b82dcff:starter-kit/CHANGELOG.md'], capture_output=True, text=True).stdout
home = open('FRAMEWORK_APPARATUS.md', encoding='utf-8').read()
def demote(text):                       # one level down, outside fences only
    out, fence = [], None
    for line in text.split('\n'):
        m = re.match(r'^(`{3,}|~{3,})', line)
        if m and fence is None: fence = m.group(1)
        elif m and line.startswith(fence): fence = None
        elif fence is None and re.match(r'^#{2,5} ', line): line = '#' + line
        out.append(line)
    return '\n'.join(out)
starts = [m.start() for m in re.finditer(r'(?m)^## ', seed)] + [seed.index('\n---\n', seed.rindex('## '))]
for a, b in zip(starts, starts[1:]):
    sec = demote(seed[a:b].rstrip('\n'))
    print(sec.split('\n')[0], 'VERBATIM' if sec in home else 'MISSING')
```

At S162 it printed MISSING for all three on today's file, VERBATIM on a correct home, and MISSING for
each of four mutants: a one-character change inside each section, and one heading left undemoted.

### 9.4 P1 — the marker discriminates

```bash
M='ledger-format: 2'     # whatever token P1 settles on
git log --all --format=%H -- starter-kit/CHANGELOG.md | while read c; do
  git show "$c:starter-kit/CHANGELOG.md" 2>/dev/null | grep -qF "$M" && echo "$c"
done                     # must print only P1's commit and later ones
```

### 9.5 The distributed files

```bash
python3 -c "import sys; sys.path.insert(0,'bin'); import _manifest as m; print('\n'.join(s for s,_,_ in m.DISTRIBUTION))"
```

### 9.6 P5 — the files identical at the start (run before porting)

```bash
bash <<'EOF'
python3 -c "import sys; sys.path.insert(0,'bin'); import _manifest as m; print('\n'.join(s for s,_,_ in m.DISTRIBUTION))" |
while read f; do
  [ "$(git rev-parse "main:$f" 2>/dev/null)" = "$(git rev-parse "b82dcff:$f" 2>/dev/null)" ] && echo "$f"
done
EOF
```

### 9.7 The budget on any tree

```bash
S=$(mktemp -d)
T=$(git merge-tree --write-tree upstream/main bl57/changelog-rules | head -1)   # or a ref
git archive "$T" | tar -x -C "$S" && (cd "$S" && git init -q && python3 starter-kit/context_budget.py)
```

### 9.8 P6–P11 — only the recorded block changed

```python
# usage: python3 check_block.py <first_line> <last_line>   (the block, as recorded before editing)
import re, subprocess, sys
lo, hi = int(sys.argv[1]), int(sys.argv[2])
diff = subprocess.run(['git', 'diff', '-U0', 'HEAD~1', 'HEAD', '--', 'CHANGELOG.md'],
                      capture_output=True, text=True, check=True).stdout
bad = []
for m in re.finditer(r'^@@ -(\d+)(?:,(\d+))? ', diff, re.M):
    start, count = int(m.group(1)), int(m.group(2) or 1)
    if count and not (lo <= start and start + count - 1 <= hi):
        bad.append((start, count))
print('only the block changed' if not bad else f'lines removed outside the block: {bad}')
```
