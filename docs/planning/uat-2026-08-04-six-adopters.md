# UAT — the framework against six real adopter repositories

**Date:** 2026-08-04 · **Session:** fork S43 · **Mode:** read-only · **Tree:** `4dea909`
**Assigned by the operator:** *"begin UAT with ../airqino, ../church_growth,
../model_project_constructor, ../mts-system, ../vscode_quarto_ext, and ../wsfct"*, scoped in the same
exchange to a **read-only assessment** covering **all four** adopter-facing surfaces.

This is fork-only. It lives in `docs/planning/` and reaches no adopter.

> **Why this is the first real acceptance test.** S41 fixed three defects in the update path and
> verified them on **throwaway** repositories it had created itself. The trimmer ships to adopters as
> of S39′ and had **never been run against a real adopter ledger**. S40's ledger doctrine was measured
> as reaching **0 of 11** sibling repos. Six real adopters is the first time any of it met a
> repository the framework did not create.

---

## 1. Audit summary

| | |
|---|---|
| **Scope** | 6 repositories × 4 surfaces (update path, ledger trimmer, dashboard, installed state) |
| **Coverage** | 6 of 6 repositories examined; 9 of 9 existing adopter ledgers exercised; 24 of 24 manifest destinations checked per repo |
| **Criteria** | §2 below |
| **Findings** | **4 critical · 5 moderate · 2 minor** — 9 of 11 are defects in what we ship |
| **Writes outside this repository** | **zero**, proven in §7 |

**The single most important result is a reframing, not a defect.** A fresh adopter installs cleanly:

```sh
mkdir fresh && cd fresh && git init -q && git commit -q --allow-empty -m init
python3 bin/sync --dry-run fresh | grep -cE "would write|would create"   # → 24
```

All 24 destinations land, including `FRAMEWORK_LEARNINGS.md` and `methodology_trim.py`. **Every
defect below is an *update-path* defect.** The fleet is not broken; it is un-updated, and the
machinery that would update it is what fails. Read the findings in that light.

---

## 2. Criteria

| # | Dimension | Pass | Fail |
|---|---|---|---|
| D1 | Update path delivers | An adopter can reach the current framework by a documented route | Any route installs nothing, installs partially, or destroys adopter data |
| D2 | Trimmer acts correctly | Trims what should be trimmed; refuses what it must; **never mistakes a full ledger for an empty one** | Silent no-op on a real ledger, or a wrong write |
| D3 | Dashboard reports truthfully | Its methodology signal tracks real methodology health | The number contradicts `bin/status` on the same tree |
| D4 | Installed state is coherent | Distributed files are current, mutually consistent, and their cross-references resolve | Stale instructions, dangling references, mandated reads that silently truncate |

---

## 3. Inventory

`bin/status` across all six, counting `tracked` rows only
(`python3 bin/status ../<repo>`, all six in `scratchpad/uat/status-all.txt`):

| Repo | missing | locally modified | versions behind | **drifting** | current | Ledgers |
|---|---:|---:|---:|---:|---:|---|
| `airqino` | 6 | 0 | 10 | **16** | 4 | CHANGELOG (seed) |
| `church_growth` | 2 | 0 | 9 | **11** | 9 | CHANGELOG + HANDOFFS |
| `model_project_constructor` | 7 | 2 | 11 | **20** | 0 | CHANGELOG |
| `mts-system` | 2 | 0 | 9 | **11** | 9 | CHANGELOG + HANDOFFS |
| `vscode_quarto_ext` | 2 | 0 | 9 | **11** | 9 | CHANGELOG + HANDOFFS |
| `wsfct` | 7 | 2 | 4 | **13** | 7 | CHANGELOG |
| **Total** | **26** | **4** | **52** | **82** | | |

`FRAMEWORK_LEARNINGS.md` and `methodology_trim.py` are **absent in 6 of 6**.

**Do not read the rows as six independent observations.** `SESSION_RUNNER.md` is byte-identical
(`c892376fb198`) in `church_growth`, `mts-system` and `vscode_quarto_ext` — one vendoring event, three
repos. `SAFEGUARDS.md` is byte-identical to canonical in those same three. The "9 versions behind"
tier is **one** data point, not three.

```sh
for r in airqino church_growth model_project_constructor mts-system vscode_quarto_ext wsfct; do
  shasum -a 1 $r/SESSION_RUNNER.md; done
```

---

## 4. Findings

### F1 — CRITICAL · D2 · The trimmer declares multi-hundred-kilobyte ledgers empty, in the words reserved for a fresh seed

**Location:** `starter-kit/methodology_trim.py:140` (`record_start`), `:1322` (the `NO_RECORDS`
finding, whose `return result` at `:1326` precedes the `evaluate_trigger()` call at `:1342`).

**Evidence.**

```sh
python3 starter-kit/methodology_trim.py --file ../model_project_constructor/CHANGELOG.md --check
python3 starter-kit/methodology_trim.py --file ../wsfct/CHANGELOG.md --check
```

Both print, byte-for-byte the same sentence the tool prints for a 324 B freshly-seeded file:

> `[NO_RECORDS] CHANGELOG.md holds zero records under its declared grammar — nothing to archive.`
> `(A freshly seeded ledger looks exactly like this, and must not be trimmed.)`

| File | Size | Real records | Grammar matches |
|---|---:|---:|---:|
| `model_project_constructor/CHANGELOG.md` | 597,717 B | **130** dated entries | **0** |
| `wsfct/CHANGELOG.md` | 1,239,085 B | **508** table rows under 8 month groupers | **0** |
| `airqino/CHANGELOG.md` | 324 B | 0 (a genuine seed) | 0 ✅ correct |

```sh
grep -cE '^### [0-9]{4}-[0-9]{2}-[0-9]{2}' ../model_project_constructor/CHANGELOG.md   # → 130
grep -cE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[' ../model_project_constructor/CHANGELOG.md  # → 0
```

The grammar demands `^### \d{4}-\d{2}-\d{2} · \[` — a **U+00B7 MIDDLE DOT** and a bracketed source
tag. `model_project_constructor` uses a U+2014 em dash; `wsfct` uses `## YYYY-MM` groupers with
table-row entries.

**Impact.** The trimmer is blind to the two largest ledgers in the audited set and **reports its
blindness as health**. It exits **0** — the same status as "trigger does not fire" — so a wrapper
reading the exit code is told everything is fine. A grammar mismatch is indistinguishable from an
empty file, and the message actively reassures. This is the worst possible failure shape for a tool
whose entire justification is that manual trimming does not happen.

**Recommendation.** Separate "no records" from "no records **matching the declared grammar** in a file
of N bytes with M candidate headings". Refuse loudly, name the mismatch, and print the first
non-matching heading. Zero records in a 1.2 MB file is never a reassurance.

---

### F2 — CRITICAL · D1 · Every adopter holding `BOOTSTRAP.md` holds an instruction that destroys their history, and the only documented route to the fix is that instruction

**Location:** `church_growth/BOOTSTRAP.md:330`, `mts-system/BOOTSTRAP.md:330`,
`vscode_quarto_ext/BOOTSTRAP.md:330` — identical text in all three.

**Evidence.**

```sh
grep -n "overlay them" ../{church_growth,mts-system,vscode_quarto_ext}/BOOTSTRAP.md
```

> `Tell your agent: *"Update methodology using https://github.com/KJ5HST/methodology"*.`
> `It will fetch the latest starter-kit files and overlay them.`

No exception is named. An agent obeying it literally overlays `CHANGELOG.md` and `HANDOFFS.md` —
42 KB/70 KB (`church_growth`), 150 KB/112 KB (`mts-system`), 474 KB/1.1 MB (`vscode_quarto_ext`) — with
empty seed templates.

S41 identified exactly this on 2026-08-04 and rewrote it into three numbered rules with a
tracked-vs-adopter-owned table (`starter-kit/BOOTSTRAP.md:343`). **That fix has reached 0 of 6.**

**Impact.** The operator's own phrase — *"Update methodology using …"* — is the documented trigger for
this path, and `bin/` ships nothing (0 of 24 destinations), so an adopter without a sibling clone has
**only** the prose route. The fix is delivered by the very instruction that is broken: following it to
get the corrected text destroys the ledgers first.

**Recommendation.** This is the strongest argument in the audit for merging upstream promptly. Until
then, any adopter told to "update methodology" should be given the never-overwrite rule inline, in the
instruction itself, rather than being pointed at their installed `BOOTSTRAP.md`.

---

### F3 — CRITICAL · D4 · `SESSION_NOTES.md` is documented as transient, accumulates in 6 of 6, is mandated reading, and no tool covers it

**Location:** `starter-kit/SESSION_NOTES.md:5` vs `:27` (the seed contradicts itself);
`starter-kit/SESSION_RUNNER.md:260`; `starter-kit/methodology_trim.py:135`.

`SESSION_RUNNER.md:260` — a file every adopter reads every session — states:

> `SESSION_NOTES.md` is the transient scratchpad (**overwritten next session**)

**Evidence.**

```sh
wc -l ../*/SESSION_NOTES.md
grep -cE '^#{2,3} .*[Ss]ession' ../model_project_constructor/SESSION_NOTES.md   # → 1058
python3 -c "...; print(list(mt.LEDGERS.keys()))"   # → ['CHANGELOG.md', 'HANDOFFS.md']
```

| Repo | lines | vs the 2,000-line `Read` cap | session headings |
|---|---:|---|---:|
| `model_project_constructor` | **25,346** | **12.7× over** | 1,058 |
| `vscode_quarto_ext` | **7,468** | **3.7× over** | 500 |
| `church_growth` | 1,777 | approaching | 29 |

It is not overwritten anywhere. Phase 0 step 2 **mandates** reading it. The trimmer knows only
`CHANGELOG.md` and `HANDOFFS.md`.

**Impact.** In `model_project_constructor`, every session reads roughly the first 8% of its own
session notes and **cannot tell that it did**. This is the framework's largest silent-truncation
exposure and it sits in the one file the doctrine excluded *because* it was believed transient. The
premise is load-bearing: it is also why `bin/_manifest.py` omits the file from `SEED_FORMAT_MARKERS`.

**Recommendation.** Correct the premise first — the seed contradicts itself in two lines, and one of
them is wrong. Then decide whether `SESSION_NOTES.md` joins the trimmer's `LEDGERS` or the runner
gains an explicit truncate-on-close-out step. Do not ship a doctrine that omits the largest instance
of the problem it describes.

---

### F4 — CRITICAL · D1 · 2 of 6 cannot be updated at all, and the file explaining the way out is among the files being withheld

**Location:** `bin/sync:307` (`return 2`, before the write loop at `:309`).

**Evidence.**

```sh
python3 bin/sync --dry-run ../model_project_constructor   # exit 2
python3 bin/sync --dry-run ../wsfct                       # exit 2
```

Both abort on `SESSION_RUNNER.md` and `SAFEGUARDS.md` being *locally modified*. The abort is
all-or-nothing: **19 of 22** remaining destinations are prevented for `model_project_constructor`,
**12 of 22** for `wsfct` (the rest are already current or are seeds left as-is).

**The guard is correct.** Three of the four blocked files carry genuine project content — `wsfct`'s
appended `## Integration with TDD and Development Workstream`, its `### Push Discipline` section, and
`model_project_constructor`'s wiki-sync/`.githooks/post-commit` paragraph. `--force` would destroy
them. (The fourth, `model_project_constructor/SAFEGUARDS.md`, differs from canonical by exactly one
superseded line — staleness, not customization.)

**The defect is the escape hatch.** The documented reconciliation path lives in `BOOTSTRAP.md:341`
and `:452` — and:

```sh
ls ../model_project_constructor/BOOTSTRAP.md ../wsfct/BOOTSTRAP.md   # both: No such file
```

**`BOOTSTRAP.md` is absent from both repos.** The guidance for resolving the block is one of the files
the block withholds. Neither repo can read its way out.

**Recommendation.** Two options, both cheap: make `bin/sync` deliver the files that are *not* in
conflict and report the ones that are (partial success beats total refusal when the refusal is
protecting two files out of 24); and/or print the reconciliation procedure inline in the abort message
rather than citing a file the aborting repo may not have. The abort message also cites "plan §3.2" —
a fork-only planning document no adopter has.

---

### F5 — MODERATE · D1 · The URL update path installs nothing, for all six

**Evidence.**

```sh
python3 bin/sync --source=github --dry-run ../church_growth
```

> `error: 2 of 24 distributed file(s) do not exist in KJ5HST/methodology yet:`
> `    starter-kit/FRAMEWORK_LEARNINGS.md`
> `    starter-kit/methodology_trim.py`
> `       This is NOT an authentication problem — the other 22 file(s) read fine.`

**This is S41's fix working exactly as designed** — it reads the whole distribution before writing,
separates *absent upstream* from *error*, and refuses a partial update. Verified against a real
adopter for the first time: **PASS.**

**Impact is a delivery gap, not a defect.** 6 of 6 are frozen out of the URL path until the upstream
PR merges. `bin/tests.sh` Test 9's standing 404 is the same fact from the other side.

---

### F6 — MODERATE · D3 · The dashboard's methodology dimension credits stale files in full

**Location:** `tools/methodology_dashboard.py:2007` (`collect_methodology_metrics`), `:2674`.

**Evidence.**

```sh
python3 -c "...; m = md.collect_methodology_metrics(Path(r)); print(m['compliance_pct'])"
```

| Repo | compliance | health bar | drifting files (`bin/status`) |
|---|---:|---:|---:|
| `airqino` | 96% | 19/20 | 16 |
| `church_growth` | 100% | 20/20 | 11 |
| `model_project_constructor` | 96% | 19/20 | **20** |
| `mts-system` | 100% | 20/20 | 11 |
| `vscode_quarto_ext` | 100% | 20/20 | 11 |
| `wsfct` | 96% | 19/20 | 13 |

The checklist does one `.exists()` probe per item and is blind to version. **`airqino`'s
`SESSION_RUNNER.md` is 17 versions behind and earns its full 25 points.**

Stated precisely, because the loose version is wrong: 7 of the 9 adopter-root files `bin/status`
flags are *deliberately* unscored (`CHECKLIST_EXEMPT`, each with a written rationale). Of the four
distributed files the checklist **does** score, `SESSION_RUNNER.md` and `SAFEGUARDS.md` are credited
in full at 9–17 versions behind or locally modified. The only item docking anyone is `HANDOFFS.md` —
a **seed**, which `bin/status` by design never calls drift. **The two instruments disagree about
which files matter, and the one adopters see is the lenient one.**

**Recommendation.** The dimension does not need to become `bin/status`. It needs one honest
disclosure: the card says "presence check — the scanner does not verify these files are used" and
should also say it does not verify they are *current*.

---

### F7 — MODERATE · D4 · `bin/check-handoff` rejects all-numeric short shas, and the code comment claims a mitigation the code removes

**Location:** `bin/check-handoff:198` (`SHA_RE`), `:196-197` (the comment), `:373-379`
(`leads_with_sha`, which reuses `SHA_RE`).

`SHA_RE` requires at least one hex **letter**. Two live instances surfaced the same day:

```sh
python3 bin/check-handoff --file ../mts-system/HANDOFFS.md
# error: receipt S74 (2026-07-14) names no commit sha in its `commit:` answer slot: '4966443'
git -C ../mts-system cat-file -t 4966443     # → commit   (49664433f931723957a33bb26b450f255314030e)
```

- **`mts-system` S74** carries `commit: 4966443` — a real commit, all-numeric, rejected since
  2026-07-14.
- **This repository's own S42 receipt** reconciled to `8804635`, also all-numeric, also rejected —
  found by this session's Phase 0 and worked around by naming the 8-character prefix `8804635e`.

The comment at `:197` says *"A rare all-numeric short sha is still carried in the separate `commit:`
field"* — but `:373-374` reuses `SHA_RE` for that field, so it is not.

**Impact.** A correct receipt is reported as defective, and the repository that publishes the checker
hit it on itself. Low blast radius, but it is a false positive in the one tool that certifies
close-out.

**Recommendation.** In the answer slot the false-positive risk that motivated the letter rule does not
apply (a date carries hyphens and cannot `fullmatch`). Accept `[0-9a-f]{7,40}` there, or verify the
token with `git cat-file -t`.

---

### F8 — MODERATE · D2 · `ZONE_UNCLASSIFIED` on a 1.1 MB ledger, caused by our own seed

**Location:** `starter-kit/HANDOFFS.md` (trailing `<!-- Receipts go below … -->` after a standalone
`---`) vs `methodology_trim.py` `footer_mode='none'`.

```sh
python3 starter-kit/methodology_trim.py --file ../vscode_quarto_ext/HANDOFFS.md --check
# [ZONE_UNCLASSIFIED] … line 2771 is a standalone '---' with 108 B of content after it
```

The refusal is *correct behaviour* — it declines to guess. But the unclassifiable content is the seed
comment we ship, so **any adopter who follows the seed literally inherits this**. Predicted by S41;
now reproduced on the largest `HANDOFFS.md` in the set.

---

### F9 — MODERATE · D4 · `dashboard_history.jsonl` is unmanaged, and the framework tripped over it here

```sh
for r in ...; do git -C $r check-ignore -q dashboard_history.jsonl; done
```

| Artifact | documented? | ignored | tracked |
|---|---|---:|---|
| `dashboard.html` | yes — `BOOTSTRAP.md:121`, `:296` | **5 of 6** | — |
| `dashboard_history.jsonl` | **nowhere** | **1 of 6** | **`vscode_quarto_ext`** (81,865 B, permanently dirty) |

The two artifacts are not symmetric, and the asymmetry tracks the documentation exactly. Note the
cause is *not* the manifest: all six adopters sync in `commit` mode, and `ensure_gitignore_entries()`
is gated behind `if mode == "ignore":` (`bin/sync:321`), so that branch never runs for any real
adopter. Widening `IGNORE_ENTRIES` would change nothing.

**This session reproduced it in the canonical repo.** Phase 0 step 5 mandates running the dashboard;
doing so created an untracked `dashboard_history.jsonl` at this repo's root, which `.gitignore` does
not cover. Disclosed in `CHANGELOG.md`; left in place.

---

### F10 — MINOR · D4 · Phase 0 reconcile debt

```sh
git -C $r rev-list --count --no-merges $(git -C $r log -1 --format=%h -- CHANGELOG.md)..HEAD
```

`airqino` **10** undocumented commits · `model_project_constructor` **5** · `mts-system` 1 ·
`wsfct` 1 · `church_growth` 0 · `vscode_quarto_ext` 0.

### F11 — MINOR · D4 · 3 of 6 have no `HANDOFFS.md`

`airqino`, `model_project_constructor`, `wsfct`. For `airqino` a sync would seed it
(`HANDOFFS.md: would create`); the other two cannot receive it while F4 stands.

---

## 5. Coverage and structural observations

**Audited:** 6 of 6 repositories · 4 of 4 surfaces · 9 of 9 existing ledgers · 24 of 24 destinations
per repo.

**Three patterns explain nine of the eleven findings.**

1. **A rule stated inside the artifact it protects is invisible to the reader who breaks it.**
   `SESSION_RUNNER.md` tells you not to edit `SESSION_RUNNER.md`; two repos edited it anyway — and
   the text they would lose *contains that instruction*. `BOOTSTRAP.md` carries the way out of F4
   and is absent from both repos that need it. F2, F4.
2. **A tool that cannot parse an input reports it as an absence.** F1's `NO_RECORDS`, F6's
   presence-only checklist, F7's `SHA_RE` — each answers "I found nothing" where the truth is "I
   could not read this", and only F8 refuses loudly. **`ZONE_UNCLASSIFIED` is the model the others
   should copy.**
3. **Everything is an update-path defect.** A fresh install is clean (24/24). The fleet's problem is
   that nothing has reached it — and the two files blocking the URL path (`FRAMEWORK_LEARNINGS.md`,
   `methodology_trim.py`) are absent upstream, which only a merge fixes.

**What the framework got right, verified rather than assumed:** S41's stale-format detection flagged
`present (stale format)` correctly on **9 of 9** ledgers; S41's GitHub pre-flight refused a partial
install with an accurate diagnosis; the trimmer's fence-awareness correctly excluded the seed's own
template line from `church_growth`'s 26 records; `bin/sync`'s local-modification guard correctly
protected three files of genuine project content.

---

## 6. Recommendations, in priority order

1. **F1** — make a grammar mismatch loud. Highest severity, cheapest fix, and it silently misreports
   the largest files in the portfolio today.
2. **F3** — correct the `SESSION_NOTES.md` premise in the seed, then decide the tool question. The
   false premise is load-bearing in three places.
3. **F2/F5** — these close only by merging upstream. Everything else is mitigation.
4. **F4** — partial sync, or the procedure inline in the abort message.
5. **F6, F7, F8, F9** — bounded, independent, each a small change.

**Not recommended:** touching any adopter repository. Three carry uncommitted work and two sit on
feature branches; `SAFEGUARDS.md:38` governs.

---

## 7. Read-only proof, and two scope disclosures

**No file outside this repository was written.** Every tool was proven non-writing *before* being
pointed at a target: `bin/status` performs only `read_bytes`/`read_text` and read-only git/`gh`
queries; all three of `bin/sync`'s write sites (`:179`, `:217-218`, `:233-234`) sit inside
`dry_run` guards; the trimmer's four `atomic_write` calls all sit below the `if not opts.write:`
return. The dashboard **does** write (`dashboard.html`, `dashboard_history.jsonl`, both to the
script's own parent directory), so it was never run from inside an adopter repo — it was run from a
scratchpad directory holding a copy of the script and symlinks to the six repos, sending both
artifacts to the scratchpad.

Verified after the fact: `git status --porcelain` in all six repos matches the pre-audit snapshot
(`scratchpad/uat/before-git.txt`), and the pre-existing dirty paths in `airqino` (2), `mts-system` (2)
and `vscode_quarto_ext` (3) are untouched.

**Disclosure 1 — repositories outside the assigned six were read.** During verification, subagents and
one of my own `*/`-globbed commands read files in `chat_verification`, `claude_work`,
`dalia_martinez_funeral`, `feedback-loop-comparison` and **`nprcgenekeepr`** — which the operator had
declared busy and off-limits. All access was read-only (`wc`, `shasum`, `grep`, `check-handoff`,
`check-links`); nothing was written and no `bin/sync` or `bin/status` was run against
`nprcgenekeepr`. It should not have been read at all, and the six-repo scope should have been
enforced in the subagent instructions rather than assumed.

That reading did produce one result worth recording, because it changes how §5's third pattern should
be read: **`chat_verification` is a clean control** — its `SESSION_RUNNER.md` is byte-identical to
canonical and it is the one repo in the portfolio that holds `FRAMEWORK_LEARNINGS.md`. The same design
that produces six drifted installs produces a clean one where a sync has actually run.

**Disclosure 2 — four of my own six working claims were wrong or overstated**, caught by adversarial
verification and corrected above rather than published. The worst: I reported adopters as carrying
"6 to 9" drifting files when the true range is **11 to 20** (82 portfolio-wide) — a figure matching no
slice of the output I had already collected; and I asserted a dangling `FRAMEWORK_LEARNINGS.md`
reference in all six when **0 of 6** runners reference it at all. Numbers in this report were re-run
by me against the tree at `4dea909`; figures I could not personally reproduce were dropped.
