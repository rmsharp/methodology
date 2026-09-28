# Which of the fork's dashboard rows go upstream, and in what order

**Status:** PLANNED by the session, **awaiting the operator's ratification** · **S231, 2026-09-27** ·
Fork-side routing document. **Nothing here is implemented, no branch is cut, and every pull request
named below is its own go-ahead.**

Commissioned at S231's Phase 0 picker from S230's next_steps (1), which measured
[the read-cap class plan](dashboard-read-cap-class-adopter-drift-plan.md)'s **P4 to have no target**:
`upstream/main`'s scanner is **2.11.1** and carries none of the code P1 (`cb9b0ed`) and P2 (`161181c`)
change, so the shipped fork-side fix can reach an adopter only inside a pull request that first
upstreams the rows underneath it. **Which rows those are, and in what order they can travel, is this
document.**

Every number below was measured this session by a command named beside it, against
**`upstream/main` = `6b29d3d`** and **fork `main` = `0aeeec1`** (this session's claim commit `8285bdb`
changed no dashboard file; `git diff 0aeeec1 8285bdb -- '*methodology_dashboard.py'` is empty).

---

## 0. The verdict

**The fork's scanner is not a set of separable rows. It is one stack plus four detachable pieces, and
the biggest piece is the one whose route is hardest.**

- **The read-cap work and the trim-trigger row are a single dependency stack, not two features.**
  `collect_trim_metrics` iterates `files["read_cap_watch"]` and calls `read_cap_class()`
  (`tools/methodology_dashboard.py:2319`, `:2320`), while the newest read-cap arm — BL-88's P2 —
  calls `find_trim_tool()`, which the trim work introduced. They interleave in both directions, so
  they cannot be sent as two independent pull requests. Together they are **90 tests and 2,287 lines
  of fork-only test code**, plus **478 lines** of fork-only module definitions and **150 of the 151
  added lines** in `assess_risks`.
- **Four pieces detach cleanly:** the root-commit-date fix (5 tests), the self-scan root (6), the
  scoped `--sync` CLI (16), and the framework-installed content structure (+10 in an existing class).
- **One of those four is a replacement of the maintainer's own design, and part of it exists only
  inside merge commits** — there is no ordinary commit to cherry-pick, so it must be re-derived by
  hand or not sent at all.
- **One is a live defect in the maintainer's shipped tool**, independent of everything else, 13 module
  lines: upstream's `first_commit_date` reads the **newest** commit, so every upstream user's
  *"project age"* and the low-velocity risk that keys on it are wrong. This is the natural first
  pull request.
- **And the timing argument runs the other way from the routing argument.** Six pull requests have sat
  open upstream with **0 reviews** since 2026-09-16 (`gh pr list`, `gh api …/reviews` → `0` on each of
  #83–#88). A seventh of ~2,300 lines does not get reviewed faster because it is well ordered.
  **§5 Option A — send nothing yet — is a live option and is not the coward's one.**

---

## 1. What I measured, and what I did not

**Measured, this session:** the two scanners' top-level definitions (AST, not grep), their risk rows,
their test suites, the upstream suite's green baseline in a clean clone, the collision surface against
all six open pull requests, the provenance of every fork-only symbol group, and which fork content
exists only inside a merge commit.

**Not measured, deliberately — it is the executor's work, not the plan's:** whether any group applies
onto `upstream/main` without conflict (no branch was built), whether upstream's suite stays green with
the fork's rows added (same reason), and the adopter-facing effect of any group other than the read-cap
one, whose fleet diff S229 and S230 already ran (0 of 49 rows changed at P2).

**Out of scope, but divergent and worth its own document later:** `bin/tests.sh` (2,845 added lines),
`bin/model-report` (640, fork-only), `bin/check-handoff` (549). Among the *distributed* files the
scanner is the outlier — `starter-kit/methodology_trim.py` is 16 added / 16 removed, essentially
converged (`git diff --numstat upstream/main main -- starter-kit/ bin/`).

---

## 2. The two trees today

| | `upstream/main` `6b29d3d` | fork `main` `0aeeec1` |
|---|---|---|
| `DASHBOARD_VERSION` | **2.11.1** | **2.19.0** |
| `tools/methodology_dashboard.py` | 3,738 lines | 4,860 lines |
| `starter-kit/` twin | byte-identical (`cmp`) | byte-identical (`cmp`) |
| Top-level definitions (AST) | 128 | 169 |
| `assess_risks` rows | 29 appends | 34 appends |
| `tools/test_methodology_dashboard.py` | 26 classes / **226 tests** | 34 classes / **350 tests** |
| Suite in a `--no-local` clone | **226 tests, OK, exit 0** (14.5 s) | 350, OK (skipped=4) |
| `.quality-gates.json` | 10 gates; `dashboard-unit-tests` ≥ 226 | 11 gates; ≥ 336 |

Divergence, exactly (`git diff --numstat upstream/main main`):

```
1314   192   tools/methodology_dashboard.py        (and the identical starter-kit/ twin)
3180   115   tools/test_methodology_dashboard.py
  34    14   bin/_manifest.py
  15     4   .quality-gates.json
```

**The scanner is distributed** (`bin/_manifest.py`, TRACKED), so every row that lands upstream reaches
every adopter on their next `bin/sync`. The test file is canonical-only — but it exists upstream, so a
pull request must carry its tests there too.

---

## 3. Evidence-based inventory (MANDATORY)

The change list below comes from the searches, not from recollection
(`SESSION_RUNNER.md` §Planning Sessions). Method, re-runnable:

```
git show upstream/main:tools/methodology_dashboard.py > /tmp/up.py     # the comparison tree
python3 - <<'PY'   # AST top-level names: fork-only / upstream-only / both-but-different
import ast
def defs(p):
    s=open(p).read(); out={}
    for n in ast.parse(s).body:
        for nm in ([n.name] if getattr(n,"name",None) else
                   [t.id for t in getattr(n,"targets",[]) if isinstance(t,ast.Name)]):
            out[nm]=ast.get_source_segment(s,n)
    return out
PY
git log --oneline -S'<symbol>' upstream/main..main -- tools/methodology_dashboard.py     # provenance
git log --oneline -S'<symbol>' --diff-merges=first-parent upstream/main..main -- …       # merge-only
```

### 3.1 Fork-only top-level definitions — 42 names, 565 lines, by group

| Group | Names | Lines | Introduced by |
|---|---|---|---|
| **Trim-trigger row** | 17 — `TRIM_TOOL_NAME`, `TRIM_TOOL_FRAMEWORK_REL`, `_TRIM_VERSION_RE`, `_TRIM_BUDGET_RE`, `TRIM_ARCHIVE_DIR`, `_MIDDLE_DOT`, `TRIM_GRAMMARS`, `_TRIM_FENCE_RE`, `git_show`, `find_trim_tool`, `_parse_trim_budget`, `_trim_record_count`, `_newest_archive_sha`, `collect_trim_metrics`, `_GENERATED_PROOF_SUFFIX`, `_GENERATED_PROOF_BANNER`, `is_generated_proof` | **397** | `bcc0d7b`, `316e7ef` |
| **Read-cap class** | 12 — `READ_CAP_TOKENS`, `MIN_BYTES_PER_TOKEN`, `READ_CAP_BYTES`, `READ_REFUSE_BYTES`, `CLASS_A_FIRE_BYTES`, `CLASS_A_STOP_BYTES`, `READ_CAP_CLASS_A`, `READ_CAP_CLASS_B`, `READ_CAP_WATCHED`, `read_cap_class`, `_TRIM_LEDGERS_READ_ONLY`, `_parse_trim_ledgers` | **81** | `9e71f83`, `596a602`, `0afe9d6`, `161181c` |
| **Installed-content structure** | 9 — `_FRAMEWORK_SIGNATURES`, `_FRAMEWORK_SIGNATURE_MIN`, `_CONTEXT_BUDGET_VERSION_RE`, `_CONTEXT_BUDGET_SIGNATURES`, `_CONTEXT_BUDGET_JSON_SIGNATURES`, `_QUALITY_RATCHET_VERSION_RE`, `_QUALITY_RATCHET_SIGNATURES`, `_QUALITY_GATES_JSON_SIGNATURES`, `_FRAMEWORK_INSTALLED_CONTENT` | **45** | `6f10460`, `316e7ef`, **and two merge commits — see F2** |
| **Self-scan root** | 2 — `_CANONICAL_IN_REPO_DIRS`, `resolve_single_project_root` | **28** | `c26358f` |
| **Scoped `--sync`** | 2 — `_KNOWN_FLAGS`, `_extract_sync_target` | **14** | `7d682fa` |

**Upstream-only: one name** — `_FRAMEWORK_FILE_SIGNATURES` (57 lines), the design the fork replaced.

### 3.2 Shared definitions whose body differs — 15

| Definition | upstream → fork | What the delta is |
|---|---|---|
| `assess_risks` | 199 → 350 lines | **+151**: the read-cap block (`:3516-3658`, 143 lines, 4 rows) and the trim re-emit (`:3660-3666`, 7 lines, 1 row) |
| `sync_dashboards` | 54 → 101 | scoped target + the `.gitignore`-aware `--force` gate |
| `collect_file_metrics` | 121 → 151 | the `read_cap_watch` population; `is_generated_proof` at the exclusion call site |
| `collect_git_metrics` | 71 → 84 | **the root-commit-date fix** |
| `is_framework_installed` | 40 → 47 | reads `_FRAMEWORK_INSTALLED_CONTENT`; the `version_re is None` arm |
| `collect_all` | 53 → 57 | wires `metrics["trim"]` |
| `print_usage` / `main` | 16 → 20 / 123 → 124 | `--sync [DIR]`, `--force`, the reworded bare-`--dry-run` refusal, `resolve_single_project_root` |
| `check_stale_version` | 27 → 30 | the stale-copy remedy names `--sync <dir>` instead of `cp` — **see F3** |
| `FRAMEWORK_INSTALLED_SOURCE` | 3 → 1 | derived from the content table instead of hand-listed |
| `EXCLUDE_DIRS` | 1 → 1 | **drops `"methodology"`** — see F4 |
| `LANG_MAP`, `detect_doc_only`, `FRAMEWORK_ITEMS` | — | **comments only.** The `.r` entry, the `.qmd`/`.rmd` handling and the item table are already identical upstream; only the fork's `BL-34` commentary and two counted nouns (*"25"* vs *"24"* distributed sources, *"21"* vs *"22"* doc files) differ |

### 3.3 Risk rows — 5 fork-only, 0 upstream-only

Upstream emits 29 `risks.append(...)`, the fork 34, and the first 29 are the same rows in the same
order. The five are all in the tail block: the `READ_REFUSE_BYTES` hard-limit row (`:3548`), the
`READ_CAP_BYTES` one-read-budget row (`:3577`), the Class B remedy arm (`:3650`, BL-88 P2), the Class B
HIGH arm (`:3658`), and the trim collector's re-emit (`:3666`).

*(First pass of this count said **3**. Two appends normalise to the same leading text as upstream's
generic `risks.append({"severity": sev, "description": desc})` and were silently merged by the
instrument. The number above is from reading all 63 appends, not from the set difference.)*

### 3.4 Tests — 10 fork-only classes, 123 tests

| Class | Tests | Lines | Group |
|---|---|---|---|
| `TestS38TrimTriggerRow` | 39 | 1,043 | trim |
| `TestD4SelfExclusion` | 4 | 69 | trim |
| `TestD4ReadCapTruncation` | 16 | 320 | read-cap |
| `TestPhaseC1ReadCapClasses` | 10 | 355 | read-cap |
| `TestPhaseC2PerClassRiskRows` | 9 | 199 | read-cap |
| `TestBL88P2TrimmerSourceProbe` | 12 | 301 | read-cap |
| `TestIssue67ScopedSync` | 16 | 304 | scoped sync |
| `TestBL29SelfScanRoot` | 6 | 81 | self-scan |
| `TestD4RootCommitDate` | 5 | 108 | root-commit date |
| `TestBL34LanguageAndDocExtensions` | 6 | 88 | **a rename** of upstream's `TestLanguageAndDocExtensionCoverage` (6 tests) |

Plus `TestFrameworkInstalledExclusion`, **33 → 43 tests**, for the installed-content structure.
Upstream-only: the class above and `TestCliRemedyProportionality` (3 tests, issue #67's landed answer).

### 3.5 The collision surface — measured against all six open pull requests

`gh api repos/KJ5HST/methodology/pulls/<N>/files`: **no open pull request touches either scanner copy
or its test file.** Shared paths a dashboard pull request would meet: `CHANGELOG.md` (all six),
`.quality-gates.json` (#85, #86, #87), `bin/tests.sh` (#84, #86, #87), `bin/_manifest.py` (#84).

---

## 4. Findings

**F1 — The read-cap work and the trim row are one stack.** Bidirectional: `collect_trim_metrics` reads
`read_cap_watch` and calls `read_cap_class()`; BL-88's P2 arm calls `find_trim_tool()`. Splitting them
into two pull requests means shipping one half broken. `CLAUDE.md`'s batching rule already forbids it —
*"independent work may go separately, dependent work should not."*

**F2 — Part of the installed-content group exists only inside merge commits, so nothing can cherry-pick
it.** `_CONTEXT_BUDGET_VERSION_RE`, `_CONTEXT_BUDGET_SIGNATURES`, `_CONTEXT_BUDGET_JSON_SIGNATURES` and
the `version_re is None` guard first appear in **`8b87086`** (the 21-commit resync merge);
`_QUALITY_RATCHET_*` and `_QUALITY_GATES_JSON_SIGNATURES` in **`421ebf9`** (resync stage M2). Both were
written as conflict resolutions. `git log -S… upstream/main..main` finds neither without
`--diff-merges=first-parent`, which is exactly how a cherry-pick-shaped plan would miss them.

**F3 — Issue #67 is closed, the maintainer answered it, and the fork's answer is different rather than
missing.** Closed by `KJ5HST` at **2026-08-12T04:43:18Z**; upstream carries
`TestCliRemedyProportionality` and a scoped remedy that says `cp <canonical> <copy>`. The fork replaces
it with `--sync <DIR>`. **Both destroy a local `EXCLUDE_DIRS` edit** — that is BL-90, raised at S230 and
measured on the portfolio copy — so upstreaming the fork's wording neither creates nor cures that
hazard; it swaps an unconditional `cp` for a route that at least skips git-tracked and brand-new
targets unless `--force`. A pull request here re-opens a question the maintainer considers answered,
and should say so in its first paragraph.

**F4 — The self-scan group changes the maintainer's own portfolio scan.** The fork dropped
`"methodology"` from `EXCLUDE_DIRS` so the canonical repo scores itself. Upstreaming that decides, for
the maintainer, that his portfolio run now includes his framework repo. It is one token, and it is a
policy, not a fix.

**F5 — Upstream has a live measurement defect that the fork already fixed, in 13 lines, dependent on
nothing.** `log --reverse --format=%ai -1` applies `-n1` while walking and *then* reverses, so it
returns the **newest** commit: upstream's `first_commit_date` tracks HEAD and its `project_age_days` is
"days since the last commit" under the name "project age". The fork reads root commits
(`--max-parents=0`, `min()` over multiple roots). 5 tests, `TestD4RootCommitDate`.

**F6 — Coined tokens: precedent exists upstream, and nothing resolves there.** Upstream's scanner
already carries `BL-5` ×9 and its tests carry `BL-1`, `BL-2`, `BL-4`, `BL-5`, `BL-31` — arrived through
merged fork pull requests. The fork's scanner adds `BL-88` ×8, `BL-34` ×3, `BL-52` ×2, `BL-29`, and
`S38` ×11, `S39` ×7, `S40` ×2, `S176` ×2; its test file has 55 such tokens against upstream's 12, and
four test *class names* encode them. **Upstream has no `docs/planning/BACKLOG.md`**, so none of it
resolves for a reader there. Precedent is not licence, and this is D3.

**F7 — The queue is the binding constraint, not the routing.** #83–#88 have **0 reviews** and no
comments but our own two (#83, #84), the oldest open since 2026-09-16.

**F8 — Everything here is distributed.** The scanner is TRACKED in `bin/_manifest.py`; each merged row
reaches every adopter root on the next `bin/sync`, and `bin/sync` overwrites a local `EXCLUDE_DIRS`
without a word (BL-90).

---

## 5. Options for the campaign's shape

**Option A — send nothing yet; prepare nothing.** Revisit when any of #83–#88 draws a review.
*Fixes:* protects the maintainer's attention, which F7 says is the scarce resource. *Leaves standing:*
the fork's scanner keeps diverging, and every session's re-derivation cost grows with it.

**Option B — one convergence pull request carrying everything.** *Fixes:* one review event, one merge,
the fork's copy becomes a descendant again. *Leaves standing:* **≈4,500 added lines across three files** (1,314 + 3,180, `git diff --numstat`), including two
policy changes (F3, F4) and a replacement of the maintainer's own design (F2) — a review no one can do
in one sitting, offered to a queue with 0 reviews.

**Option C — one small correctness pull request now, the stack prepared but held. RECOMMENDED.**
Send F5's 13-line fix with its 5 tests: it is a real defect in the maintainer's shipped tool, reviewable
in minutes, and depends on nothing. Build and vet the read-cap/trim stack fork-side meanwhile, and open
it only when the small one merges — its merge is the evidence the channel is alive, which no amount of
planning substitutes for. Leave F2, F3 and F4 out of both; each is a policy question, not a fix.
*Leaves standing:* the fork still carries four detachable pieces indefinitely.

---

## 6. Decisions for the operator

Each is recommended, none is taken. **D1 governs; the rest can be deferred without blocking it.**

- **D1 — campaign shape.** (a) Option C *(recommended)*; (b) Option B; (c) Option A.
- **D2 — the installed-content structure (F2).** (a) Never send it; re-derive future additions onto
  upstream's `_FRAMEWORK_FILE_SIGNATURES` whenever they are needed there *(recommended — it is a
  refactor of the maintainer's own recent work, it is invisible to adopters, and F2 says it cannot be
  cherry-picked anyway)*; (b) send it as a standalone refactor pull request carrying the drift argument
  the fork's own comment already makes; (c) fold it into the convergence pull request.
- **D3 — coined tokens in upstream-bound code (F6).** (a) Scrub them: rename the four test classes and
  rewrite the comments in recognised terms before any pull request *(recommended)*; (b) keep them,
  citing the precedent already upstream; (c) scrub prose, keep class names.
- **D4 — the scoped `--sync` group (F3).** (a) Hold until BL-90 is costed, then send both together
  *(recommended)*; (b) send now with the hazard disclosed in the body; (c) never send — upstream
  considers #67 answered.
- **D5 — the self-scan group (F4).** (a) Hold; it is a policy about the maintainer's own scan
  *(recommended)*; (b) send with the exclusion made configurable rather than removed; (c) send as is.
- **D6 — gate thresholds.** Each pull request tightens `dashboard-unit-tests` and `tests-sh-passed` in
  `.quality-gates.json` by exactly what it adds *(recommended — the ratchet only tightens, and a pull
  request that adds tests without raising the floor lets them be deleted later)*. Note the conflict
  surface: #85, #86 and #87 also touch that file.

---

## 7. Phases

Each phase is **one session**. Close out when its DONE criterion is met; do not start the next.

### The surface, stated once because it governs every phase

Fork-side phases are demonstrated **on this machine**, in a `git clone --no-local` of the branch at the
commit under test — never in a worktree, which shares the object database and can resolve a `git show`
that will not resolve upstream (the measurement that changed S39's picture). Pull-request phases are
demonstrated **on GitHub**. **What neither surface can enforce: the merge.** That is the maintainer's,
and no phase below may record a merge as its own DONE.

### P1 — the correctness pull request (D1(a) or (b); its own go-ahead)

Branch from **`upstream/main`**, re-derive F5's fix there (**a fork-side fix is not an upstream patch**:
the fork's `collect_git_metrics` also carries the read-cap-era comment block, which must not ride
along), port `TestD4RootCommitDate` under a name D3 allows, and raise the two gates by what it adds.

- **DONE looks like:** the pull request open and `MERGEABLE`, body in recognised terms — no session
  numbers, no `BL-`/`D4` codes, no fork-coined names.
- **Verify:** in a `--no-local` clone of the branch — `python3 tools/test_methodology_dashboard.py`
  (expect **226 + 5 = 231**, and read the number rather than predicting it), `bash bin/tests.sh`,
  `python3 starter-kit/quality_ratchet.py --run` exit 0; `cmp` the two scanner twins;
  `git merge-tree --write-tree --name-only upstream/main <branch>` for the conflict list.
- **Surface:** GitHub. **Cannot enforce:** the merge.

### P2 — build and vet the convergence branch, fork-side, NOT opened

Branch from `upstream/main`; re-derive the read-cap + trim stack (F1) as one coherent change; apply D3;
leave F2, F3 and F4 out unless D2/D4/D5 say otherwise.

- **DONE looks like:** the branch exists locally with the suite green in a clone, and a written
  adopter-impact statement — the fleet diff re-run read-only through both module versions, in process,
  writing no `dashboard.html` (the S229/S230 procedure).
- **Verify:** the clone suite (expect 226 + 90 = **316** if D3 is a pure rename and nothing else moves —
  **a prediction, not a measurement; read the runner's number**); `bash bin/tests.sh`; the ratchet;
  twins `cmp`; the trial merge into `upstream/main`, **and the suite run on the merge result, not on the
  branch**.
- **Surface:** this machine, in a clone. **Cannot enforce:** anything about upstream's CI, which this
  repository does not run.

### P3 — the convergence pull request (its own go-ahead; hold per D1)

- **DONE looks like:** the pull request open and `MERGEABLE`, carrying P2's branch unchanged and an
  adopter-impact paragraph.
- **Verify:** re-run the trial merge at the moment of opening — `upstream/main` may have moved.
- **Surface:** GitHub. **Cannot enforce:** the merge, or the review.

### P4 — the deferred policy pieces, one session each, only if D2/D4/D5 are taken that way

F2's structure, F3's scoped `--sync` (with BL-90), F4's self-scan. Each gets its own phase with the same
shape as P1; **none may be bundled into P3**, because each asks the maintainer a question rather than
fixing a defect.

- **Surface:** this machine for the build, GitHub for the pull request. **Cannot enforce:** the answer
  to the question each one asks — a maintainer may decline a policy change and be right to.

### P5 — the fork-side reconcile, after any merge

Re-point the fork's copy at the merged upstream, decide the `DASHBOARD_VERSION` continuation (the fork
is at 2.19.0, upstream at 2.11.1 — the same collision the resync's D3 settled once and will face again),
and update BL-88's record and this document's status.

- **DONE looks like:** fork `main` merged with the new `upstream/main`, twins byte-identical, gates green,
  BL-88's detail row updated to name where its P1 and P2 finally landed.
- **Verify:** `bin/tests.sh` and the ratchet in a `--no-local` clone of the merge result; `cmp` the twins;
  `python3 tools/methodology_dashboard.py --no-open` exit 0.
- **Surface:** this machine, in a clone of the merged tree. **Cannot enforce:** that adopters sync —
  a merged row reaches a project only when someone runs `bin/sync` there.

---

## 8. Here be dragons

1. **The twins must stay byte-identical, and a number recorded before the mirror is false with nothing
   failing.** Mirror `starter-kit/` **last**, then re-measure; `test_twins_byte_identical` and the
   version test both fail until you do, and that failure list is the checklist.
2. **`git log -S` does not see a merge commit.** F2's four constants are invisible to it. Any inventory
   built with `-S` alone under-reports the fork's content; use `--diff-merges=first-parent`.
3. **A `git worktree` shares the object database.** A verification that passes there can fail in a clone
   for a reason that has nothing to do with the change. Use `git clone --no-local`.
4. **The read-cap class sets are declared literals of paths, and one of them is
   `docs/planning/BACKLOG.md`** — a path upstream does not have. That is fine: the list names locations
   in a *scanned* project, not in this repository. Do not "fix" it on the way upstream.
5. **`assess_risks`'s first 29 rows are byte-shared with upstream.** A convergence branch that rewrites
   that function wholesale will look like it changes 350 lines when it changes 151, and the review cost
   is the diff, not the intent.
6. **`--sync` overwrites a local `EXCLUDE_DIRS` with no warning** (BL-90). Any phase that tells a reader
   to run it — including a stale-copy message this plan upstreams — is shipping that hazard further.
7. **The fork's read-cap rows presuppose the fork's ledger discipline.** `READ_CAP_CLASS_A` is
   `CHANGELOG.md` + `HANDOFFS.md`; an adopter without a `HANDOFFS.md` simply never matches, which is
   correct — but the row's prose, written for this repository, should be re-read for a tree that does
   not work this way before it ships to one.

---

## 9. Explicitly not in scope

The other three distributed tools; `bin/tests.sh`'s 2,845-line divergence; `bin/model-report`
(fork-only); the fork's documentation divergence; and **any outward action at all** — this document
opens nothing, comments nowhere, and touches no branch.
