# `bin/sync --source=github`: an update route that can update, and a refusal that says what it knows

**Date:** 2026-09-21 (fork session S217)
**Status:** RATIFIED 2026-09-21 — the operator ruled all eight decisions in §3 option (a), as recommended, at fork
session S218's Phase 0 picker; §4 is therefore the design. Implementation is §5, one phase per session; **P1 is done**
(S218, its outcome under §5 P1); P2 is next. Nothing is upstream-facing until P5, its own go-ahead.
**Backlog:** BL-66 ([detail](BACKLOG-DETAIL.md#bl-66)); under D3 (a) the same pull request closes BL-54's
open upstream half ([detail](BACKLOG-DETAIL.md#bl-54)).
**Route:** `bin/sync` and `bin/status` are canonical-only — `bin/` has no row in `bin/_manifest.py` — so the code
reaches adopters when they clone or pull the canonical repository, and only an **upstream pull request** puts it there.
`starter-kit/BOOTSTRAP.md` is distributed (TRACKED); `README.md` and `docs/tutorials/` are not.

**Line citations name their tree.** The two scripts differ between trees: `bin/sync` is blob `c4514983` on
`upstream/main` (`6b29d3d`) and on PR #84's head (`77afc12`), `6fea8d08` on fork `main`; `bin/status` is `076f9f8f`
upstream, `24b3ddc3` on #84, `b12986ae` on fork `main`. A bare `bin/sync:N` below is **fork `main`**; upstream's
number follows as `upstream:N`. `README.md:61` and `:72` are the same text in all three trees (no hunk touches them
in `git diff upstream/main main -- README.md`, and #84's README hunks are at `:93`, `:111`, `:197`).

---

## 0. In one paragraph

`bin/sync --source=github` reads each distributed file's **contents** from GitHub and nothing else
(`bin/sync:100-113`, `upstream:80-90`), then classifies the adopter's copy against an **empty history**
(`bin/sync:293`, `upstream:224`). The classifier's only ways to accept a file that differs from canonical are
*byte-identical* or *matches a version in the source's history* (`:209-218`), so with no history every file that is
merely behind is refused as *"local modifications"* — the one case an update exists for. `bin/status --source=github`
has the same gap (`bin/status:227`, `upstream:165`) and reads the same files as *locally modified*. Both were
**deferred on purpose** by the B1 plan (`b1-sync-coverage-expansion-plan.md:161`, Decision 3: *"Defer + document …
Document the limitation in `--help` / BOOTSTRAP"*); the BOOTSTRAP half was done, the `--help` half was not, and the
front page (`README.md:61`) still tells an adopter to update by pointing an agent at the GitHub URL, whose only
mechanical form is this route. Measured today on an adopter installed from `008d656` and never edited, against
`6b29d3d`: `--source=local` from a full clone updates 10 files, exit 0, 2.2 s; `--source=github` refuses 9, exit 2,
12.3 s, and prints an *"inspect the drift"* header with nothing under it. **The fix that removes the defect rather
than documenting around it is small and measured:** `git clone` of the upstream repository costs **3.8 s and 2.2 MB**,
and the existing local machinery run over that clone updates the same project in **4.9 s end to end, exit 0** — faster
than today's broken route, with the BL-54 merge-side fix inherited for free. The plan makes `--source=github` mean
*"a fresh clone, then exactly what `--source=local` does"*, gives the refusal a diagnosis it can stand behind for the
history-less local sources that remain (a shallow clone, a tarball), and reconciles the four documents that describe
the route.

---

## 1. Context

### 1.1 The defect, reproduced at today's heads

A scratch adopter (`git init`, `bin/sync --source=local` from a checkout at upstream `008d656`, committed, never
edited: zero local modifications, N versions behind) was updated toward `upstream/main` `6b29d3d` by every route the
documents name. Run at S217 from `--no-local` clones; the timings are one run each.

| Route | Command | Result | `version:` line | Time |
|---|---|---|---|---|
| **(i)** full clone, local | `bin/sync <p> --source=local --dry-run` | **exit 0** — 10 would write, 13 unchanged | `v3.7-68-g6b29d3d` | 2.24 s |
| **(ii)** shallow clone (`--depth 1`), local | same, from a depth-1 clone of the same commit | **exit 2** — 9 refused as *local modifications* | `6b29d3d` | — |
| **(ii-b)** tarball (`git archive`, no `.git`), local | same, from the extracted tree | **exit 2** — 9 refused | `local` | — |
| **(iii)** GitHub | `bin/sync <p> --source=github --dry-run` | **exit 2** — 9 refused; *"To inspect the drift first:"* printed with **no lines under it** | `github:6b29d3d` | 12.27 s |
| **(iv)** GitHub, status | `bin/status <p> --source=github` | **9 `locally modified`, 0 behind**, 13 `current`, 6 seeds `present` | — | — |
| **(v)** full clone, status | `bin/status <p> --source=local` | **9 `N versions behind`** | — | — |

Rows (iii) and (iv) are the defect; (ii) and (ii-b) are the cases BOOTSTRAP's *"a shallow clone or a downloaded
tarball loses that git history"* (`starter-kit/BOOTSTRAP.md:88`, `upstream:85`) already describes, and they show the
refusal text is wrong for them too: the files have no local modifications, the source has no history. Row (i) is
what BL-66 measured at S182 (exit 0 / 10 written); row (iii) is its *"exit 2 / nine files"*, unchanged since.

### 1.2 Provenance: a chosen deferral whose second half never landed

- `bin/status`'s *"history-walk not implemented for github source"* (`upstream:165`) was written by the maintainer in
  `22d1da7` (2026-04-20, v2.2 Phase 1). `bin/sync`'s `else set()` (`upstream:224`) came with the fork's B1 expansion,
  `662cdaf` (2026-06-20).
- The B1 plan (2026-06-19) recommended it, the implementation shipped that way in v2.8 (PRs #33–#37), and the maintainer closed
  issue #32 on 2026-06-21 with it in place; the plan's own status line was never updated from *"Not yet ratified"*: **Decision 3, *"`--source=github`
  incremental safety — Defer + document. History walk is unimplemented for github source … so any changed file
  misclassifies as 'locally modified' and blocks → `--force`. Keep local source the supported update path to keep B1
  small. Document the limitation in `--help` / BOOTSTRAP."*** (`b1-sync-coverage-expansion-plan.md:161`).
- The BOOTSTRAP half was done: *"Prefer `--source=local` from a full methodology checkout …"* (`upstream:85`). The
  `--help` half was not: `--source`'s help is still *"local (default if sibling methodology/ exists) or github"*
  (`bin/sync:255`, `upstream:191`; `bin/status:206`, `upstream:144`), and `README.md:72` still lists the route beside
  the other two with nothing to distinguish it.
- `README.md:61` — *"To update an existing project to the latest version, use the same approach: 'Update methodology
  using https://github.com/KJ5HST/methodology'"* — is the maintainer's own line (`ce1ec629`, 2026-03-27; the phrase
  itself first appeared in the operator's `496511b`, 2026-03-13), written before `bin/sync` existed. It is prose to an
  agent, not a command; §1.3 is about what it maps to.
- No upstream issue records the defect: `gh issue list --state all --search` for `source=github`, `"locally modified"`
  and `Update methodology using` returns #32 (the deferral) and three unrelated issues. BL-66 is the only record.

### 1.3 What the README's instruction is, and what it is not

`README.md:61` names no command. The documented mechanical form of *"Update methodology using <url>"* is
`bin/sync --source=github`: fork `main`'s `BOOTSTRAP.md:396` says so in as many words (*"the closest mechanical
equivalent of the instruction above"*), the S41 audit ran that command as *"the URL update path"*
(`uat-2026-08-04-six-adopters.md:247`), and the routes memo treats the two as one route
(`read-set-budgets-local-use-routes.md:25`). An agent that instead clones the repository in full and runs `bin/sync`
gets route (i) and succeeds; one that clones shallow, downloads a tarball, or follows `README.md:72` gets (ii), (ii-b)
or (iii) and is refused. So the plan does not claim the instruction *always* fails; it claims that the only route the
documents give it fails, and that the refusal then blames the adopter's files. **Both halves are what D1 fixes.**

### 1.4 Why this is one pull request

The real fix (§3 D1) makes the GitHub route *reuse* `local_history_blobs()` (`bin/sync:55-87`) and `bin/status`'s
`local_history()` (`bin/status:90-102`). On `upstream/main` those functions still walk without `--full-history`, so a
version hidden behind a merge reads *locally modified* — BL-54, fixed fork-side in `2c4f801` and `865119f` and **still
owed upstream** (its row: *"Open only for its upstream PR, its own go-ahead"*; #84's body, line 196: *"a separate,
small PR to follow"*). A GitHub route built on upstream's walk would ship a known defect into a new path; built on the
fork's, it depends on BL-54's commits. `CLAUDE.md` §Contributing upstream: *"independent work may go separately,
dependent work should not."* D3 asks the operator to confirm the batching; the fallback is a stacked pair.

---

## 2. Evidence-based inventory

### 2.1 Code sites

`bin/sync` (fork `main` / `upstream:`):

| Site | Fork | Upstream | What it is |
|---|---|---|---|
| `REPO = "KJ5HST/methodology"` | `:17` | `:17` | the only statement of where GitHub content comes from |
| `detect_source()` — `github` iff no `starter-kit/` beside `bin/` | `:40-43` | `:40-43` | when the route is chosen by default |
| `local_history_blobs()` — `git log --full-history` + one batched `cat-file --batch-check` | `:55-87` | `:55-…` (no `--full-history`, per-commit lookups: BL-54) | the history walk the fix reuses |
| `read_github()` — `gh api repos/{REPO}/contents/{src}`, no `ref` | `:100-113` | `:80-90` (exits on first failure with *"run `gh auth login`"*: S41's UAT F5) | the content fetch |
| `fetch_all_github()` — reads all sources first, names absent ones | `:116-156` | absent | S41's inventory (`12463dd`), fork-only |
| `methodology_version()` — `git describe` for local, `github:<sha7>` for github | `:159-177` | `:95-…` | the `version:` line |
| `classify_target()` — `current` / `upgradable` / `modified` | `:209-218` | `:145-…` | needs a history set to say `upgradable` |
| `--source` help, `--force` help | `:255`, `:257-258` | `:191`, `:193-194` | the `--help` half of Decision 3 |
| `remote = fetch_all_github(...) if source == "github"` | `:283` | — | pre-flight |
| **`history = … if source == "local" else set()`** | **`:293`** | **`:224`** | **the defect** |
| the refusal: *"local modifications that don't match any canonical or historical version"* | `:301-317` | `:232-248` | asserts a cause it has not established |
| the diff hint printed only `if source == "local"` under an unconditional header | `:313-316` | `:244-247` | the empty *"inspect"* header in row (iii) |

`bin/status`:

| Site | Fork | Upstream | What it is |
|---|---|---|---|
| `local_history()` — two walks, first-parent and full (BL-54, option C) | `:90-102` | `:52-…` (one walk, default) | the walks the fix reuses |
| `github_canonical()` — `gh api …/contents/{src}`, returns blob sha + content | `:116-127` | `:77-…` | the content fetch |
| `file_status()` — `"locally modified"` when no walk carries the blob | `:130-146` | `:91-103` | where a behind file becomes *locally modified* |
| `--source` help | `:206` | `:144` | as above |
| **`history[src] = {}  # history-walk not implemented for github source`** | **`:227`** | **`:165`** (`[]`) | **the defect's twin** |

Callers of the two GitHub fetchers: none outside these scripts (`grep -n -i 'github\|gh api' bin/check-links
bin/check-handoff bin/check-learnings` → nothing; `tools/` mention `bin/sync` only in comments and dashboard heuristics).

### 2.2 Every statement of the route in prose (the docs phase's list)

| Where | Fork line | Upstream line | Says | Under the fix |
|---|---|---|---|---|
| `README.md` Quick Start note | `:61` | `:61` | update by telling an agent *"Update methodology using <url>"* | keep; add where the agent should run `bin/sync` from (D6) |
| `README.md` Option A | `:72` | `:72` | `--source=github  # or: pull from GitHub (needs gh CLI)` | `needs git and network`; no longer needs `gh` (D8) |
| `README.md` What's New in v2.2 | `:684-686` | (same section) | dual-source sync; *"Drift safety"* | historical; unchanged |
| `starter-kit/BOOTSTRAP.md` sync block | `:70` | `:69` | `# Pull from GitHub if you don't have a sibling methodology checkout (requires gh CLI)` | reword (inside #84's hunk context: D7) |
| `BOOTSTRAP.md` *Updating an existing project…* | `:88` | `:85` | *"Prefer `--source=local` from a full methodology checkout — … a shallow clone or a downloaded tarball loses that git history, so the same files look 'locally modified'"* | the preference becomes a statement that either source now carries history; the shallow/tarball sentence stays true (D5) — **#84 rewrites this paragraph** |
| `BOOTSTRAP.md` §With `bin/sync` | `:360` | `:356` | *"If `status` shows `locally modified`, sync will refuse … or pass `--force`"* | unchanged |
| `BOOTSTRAP.md` §Without `bin/sync` | `:364` | `:360` | *"Tell your agent: 'Update methodology using …'"* (upstream adds *"It will fetch the latest starter-kit files and overlay them."*) | unchanged by this plan (§7) |
| `BOOTSTRAP.md` *A note on `--source=github`* | `:396-400` | absent (S41, fork-only) | *"the closest mechanical equivalent of the instruction above"* | fork-side wording only (P6) |
| `BOOTSTRAP.md` troubleshooting | `:471-472` | `:431-432` | *"`bin/sync` refuses with 'locally modified'. A synced file has local edits."* | add the second cause the refusal will now name (D5) |
| `docs/tutorials/T1_setup.md` | `:57-58` | same | `--source=github` *"(needs the gh CLI)"* | `needs git and network` |
| `docs/tutorials/T8_keeping_current.md` | `:163`, `:168` | `:163`, `:168` | `bin/status . --source=github  # compare straight against canonical on GitHub` | **becomes true** — today it reports a behind file as *locally modified* (row iv) |
| `bin/sync --help`, `bin/status --help` | `:255`, `:206` | `:191`, `:144` | *"local … or github"* | say what github does now (clones; needs git and network) |

### 2.3 Tests

- Fork `bin/tests.sh` **Test 8** (`:124-133`; `upstream:107`): a behind `SESSION_RUNNER.md` upgrades without `--force`
  — **local source only**. **Test 9** (`:135-142`; `upstream:118`): `--source=github --dry-run` on a fresh tree
  exits 0; skipped without `gh auth`. A fresh tree has nothing to classify, so Test 9 cannot see the defect, and the
  one `--source=github` in the suite is that line. **Test 41** (`:3364` onward, fork-only): builds a methodology repo with
  fixed dates and both merge-hiding shapes, syncs a project from it, and asserts `status`/`sync` per version — the
  fixture pattern P1's tests copy. `:374-375` (fork-only, #84's) pin two phrases of BOOTSTRAP's *Updating…* paragraph
  (`Size, and when to archive`, `keeping any archive-pointer block`); P3's rewording must keep them.
- Upstream `bin/tests.sh`: 820 lines, 27 `== Test` headers (25 numbered, two named). #84 adds at `upstream:277`,
  `:310`, `:431`; #86 at `:672`. A test appended after `:820` overlaps neither.
- The quality ratchet (`.quality-gates.json`, fork) floors `tests-sh-passed` at 343: every new `pass` line raises
  the floor in the same commit, as the earlier plans did.

### 2.4 The manifest, both trees

29 rows, 23 TRACKED, 6 SEED, identical counts on `upstream/main` and fork `main`
(`python3 -c "import sys;sys.path.insert(0,'bin');import _manifest as m;print(len(m.DISTRIBUTION))"`). Across the 23
tracked sources, `git rev-list --count --full-history upstream/main -- <src>` sums to **450** commits (largest
`starter-kit/SESSION_RUNNER.md`, 68) — the size of the history any GitHub-side walk must cover.

### 2.5 Overlap with the four open PRs (heads: #83 `219fb9d`, #84 `77afc12`, #85 `e2501c5`, #86 `c1167ae`)

| File this plan touches | #83 | #84 | #85 | #86 |
|---|---|---|---|---|
| `bin/sync` | — | — (its copy = upstream's) | — | — |
| `bin/status` | — | **yes**: `MIGRATION_ROUTES` (`upstream:105-125`) and the stale-seed note (`:184-212`); not the history loop at `:157-165` | — | — |
| `bin/tests.sh` | — | **yes** (`:277`, `:310`, `:431`) | — | **yes** (`:672`) |
| `README.md` | — | `:93`, `:111`, `:197` — not `:61`/`:72` | — | — |
| `starter-kit/BOOTSTRAP.md` | — | **yes**: `:20`, `:69-78` (context includes `:69`), **`:82-85` (rewrites the *Updating…* paragraph)**, `:104`, `:128`, `:136` | — | — |
| `docs/tutorials/T1`, `T8` | — | — | — | — |
| `CHANGELOG.md` | all four carry ledger entries; a conflict here is routine and resolved by keeping both | | | |

Fork `main` already holds #84's `bin/status` and `BOOTSTRAP.md` beside BL-54's `bin/status`, so the merged shape of
those two files is known to exist. The two textual collisions are `BOOTSTRAP.md:69` (context) and `:85` (rewritten);
D7 sequences around them, and P4 measures them with `git merge-tree --write-tree --name-only` rather than predicting.

### 2.6 The fork-only delta of the two scripts (what D3 folds in)

`git log upstream/main..main -- bin/sync`: `2c4f801` + `865119f` (BL-54: `--full-history`, batched lookups),
`12463dd` (S41: `fetch_all_github`'s absent-file inventory), and a merge. `-- bin/status`: the same two BL-54 commits,
plus #84's five (`2d5dc6e`, `100f09b`, `f4e974c`, `7813652`, `036d840`) — already upstream-bound. Under D1 the
`gh api` fetchers are removed, so S41's inventory is re-expressed over the clone (a missing source is a `Path.exists()`
check, offline) and BL-54's walks are what the route calls. Nothing else in the delta is touched.

### 2.7 The premise, tested on throwaway clones (S217, one run each)

| Experiment | Result |
|---|---|
| `git clone --bare --filter=blob:none https://github.com/KJ5HST/methodology.git` | 0.74 s, **416 KB**, 730 blobs missing |
| in it, `git log --full-history --format=%H --raw --no-abbrev -- starter-kit/SESSION_RUNNER.md` | 0.01 s, **42** raw lines for **68** commits (merges print none without `-m`), 0 blobs fetched |
| in it, the tool's own `cat-file --batch-check` over the 68 `<commit>:<path>` names | **16.24 s, 43 blobs lazily fetched** — the walk the tool already has is a trap on a blobless clone |
| `git clone --bare` (full) | 1.18 s, **2.0 MB** (`size-pack` 1.89 MiB) |
| `git clone` (full, working tree) | **3.77 s, 2.2 MB** `.git`, HEAD `6b29d3d` |
| the proposed route end to end: that clone + upstream's own `bin/sync <p> --source=local --dry-run` | **4.92 s, exit 0**, 10 would write, `version: v3.7-68-g6b29d3d` |
| today's route on the same project (row iii) | 12.27 s, exit 2 |

So a **full** clone is the mechanism: cheap, and it reuses every line of the local path unchanged. The blobless form
saves 1.8 MB and costs a new tree-level walk that must never touch a blob and must handle merges; it is recorded here
as considered and rejected (D2).

---

## 3. Decisions

### D1: what `--source=github` means

| | Option | Consequence |
|---|---|---|
| **(a) recommended** | **A fresh clone, then the local path.** `--source=github` clones `https://github.com/{REPO}.git` into a temporary directory, sets `methodology_root` to it, and runs exactly the `local` code: `read_local`, `local_history_blobs`, `classify_target`, `git describe`. The temporary directory is removed when the run ends, dry run or not. | Rows (iii) and (iv) become rows (i) and (v). BL-54's walk is inherited. `gh` is no longer needed for a public repository (D8). Faster than today (4.9 s vs 12.3 s). New requirement: `git` and network, both already required by `--source=local` from a fresh checkout. |
| (b) | History through the GitHub API: `commits?path=` per file, then a blob lookup per commit. | 450 commits over 23 files → hundreds of calls (5,000/h authenticated), minutes per run; `commits?path=` is git's *simplified* walk, so BL-54's hidden versions return; `bin/status`'s two walks cannot be expressed. Rejected. |
| (c) | Docs only: keep the route as it is and say everywhere that it cannot update. | Finishes Decision 3's `--help` half and nothing else; `README.md:61` keeps sending adopters to a route that refuses them. Rejected as the whole, kept as the floor (D6 lands under any D1). |

### D2: the clone

**(a) recommended:** a **full, non-bare** clone of the default branch into `tempfile.TemporaryDirectory()`, by plain
`git clone --quiet`; the URL is `https://github.com/{REPO}.git`, overridable by an environment variable
(`METHODOLOGY_SOURCE_URL`, say — D8 names it) so the tests can point the route at a local bare repository and a
private mirror can be named without editing the script. No cache directory: 3.8 s per run is under the route's
current cost, and a cache adds staleness, locking and a second thing to explain. **(b)** blobless clone with a
tree-level walk: rejected in §2.7. **(c)** a cache under `~/.cache` with `git fetch`: deferred; nothing measured today
asks for it.

### D3: scope of the pull request

**(a) recommended:** one pull request carrying **BL-54's two commits, S41's inventory behaviour re-expressed, and this
fix** — the three are one subsystem (how the two scripts learn what versions exist) and dependent (§1.4). The body
says plainly that it supersedes #84's *"separate, small PR to follow"* for BL-54, and why. **(b)** two stacked PRs,
BL-54 first as promised, this on top: two reviews for one review's worth of change, and the second cannot merge
until the first does. **(c)** this fix alone over upstream's default walk: ships BL-54's defect into a new path.
Rejected.

### D4: `bin/status --source=github`

**Yes, same mechanism, same PR.** It has the same line (`bin/status:227`), the same symptom (row iv), and
`T8_keeping_current.md:163` sends learners to it as the way to *"compare straight against canonical."* A sync route
that upgrades a file `status` calls *locally modified* would contradict itself.

### D5: the refusal for history-less **local** sources (rows ii and ii-b)

After D1 the GitHub route has history, but a shallow clone or a tarball still has none, and the refusal still blames
the adopter's files. **(a) recommended:** before printing the refusal, `bin/sync` asks the source what it knows —
`git rev-parse --is-shallow-repository` (true → *"the source checkout is shallow (N commits), so a file that is merely
behind cannot be recognized; run from a full clone, or `git fetch --unshallow`"*), and no `.git` at all (→ *"the source
has no git history, so … clone the repository rather than downloading it"*) — and names that cause **instead of**
*local modifications* when it holds. The *local modifications* sentence stays for a full-history source, where it is
earned. One new test per cause (a depth-1 clone of the Test 41 fixture; `git archive` of it). **(b)** leave it to
BOOTSTRAP's sentence: the sentence is in the one document an adopter at that prompt is not reading. Same PR either way;
it is the second half of BL-66's own statement (*"the diagnosis is the second defect"*).

### D6: the documents

**(a) recommended, minimal:** `README.md:61` gains one clause after the instruction — that the agent should run
`bin/sync` from a full clone of the repository, or `bin/sync --source=github`, and that either recognizes files that are
merely behind — and `:72` loses *"needs gh CLI"* for *"needs git and network"*. `BOOTSTRAP.md:69` likewise; `:85`'s
*"Prefer `--source=local` …"* becomes *"Either source carries the history that recognizes a file as merely behind …"*
with the shallow/tarball sentence kept and pointed at the refusal that now names it; `:431` gains the second cause.
`T1_setup.md:58` drops the `gh` remark; `T8` is unchanged, since its instruction becomes correct. `--help` for both
scripts says what `github` does. **(b)** rewrite `README.md:61` to drop the agent-prompt framing: it is the maintainer's
own line and his product's front door; not this fork's call.

### D7: base branch and sequencing against #84

**(a) recommended:** branch `fix/sync-github-history` from **`upstream/main`** (the branching rule: origin carries
fork-only docs), cherry-pick BL-54's two commits first, build on them. P4 runs `git merge-tree --write-tree
--name-only` against each of the four heads; the expected result is a conflict in `starter-kit/BOOTSTRAP.md` with #84
(`:69` context, `:85` rewritten) and in `CHANGELOG.md` with all four, nothing else. **P5 opens the PR after #84 merges
and the branch is rebased**, so the maintainer never sees the BOOTSTRAP conflict — or, if the operator would rather not
wait, with the one-paragraph conflict resolved toward #84's text and stated in the body. **(b)** stack on
`bl57/changelog-rules` (#84's head): no conflict, but the PR cannot merge before #84 and its diff shows #84's changes
until then. Not recommended while #84 is unreviewed.

### D8: `gh` leaves the route

Under D1 (a) a public repository clones over HTTPS with no credentials. **(a) recommended:** drop the `gh` calls from
both scripts; keep `REPO` as the single statement of the source, derive the URL from it, and read the override from
`METHODOLOGY_SOURCE_URL` (a path or URL; the tests use a local bare repo). A private mirror uses git's credential
helper (`gh auth setup-git` is one). Test 9's guard becomes reachability of the URL (`git ls-remote --exit-code -h`,
with a timeout), not `gh auth status`. **(b)** clone through `gh repo clone`: keeps the `gh` requirement for no gain
on a public repository, and `gh repo clone` adds an `upstream` remote on forks. Not recommended.

---

## 4. The design (the decided options, written as the interface)

| Route | Reads content from | History set | `version:` | Needs |
|---|---|---|---|---|
| `--source=local` (default when `starter-kit/` sits beside `bin/`) | the checkout's working tree | `git log --full-history` of that checkout (BL-54) | `git describe --tags --always` | a full checkout |
| `--source=github` | a fresh clone of `https://github.com/KJ5HST/methodology.git` (or `$METHODOLOGY_SOURCE_URL`) in a temp dir | the clone's full history — the same function | the same command, on the clone (`v3.7-68-g6b29d3d`, not `github:6b29d3d`) | `git`, network |

The refusal, for a tracked file that is neither canonical nor in the history set:

- full-history source → today's text, *local modifications that don't match any canonical or historical version*,
  plus the `diff` hint (for `github`, a hint that names the clone's path is useless after the run; print
  `git show <sha>:<src>` against `REPO` instead, or drop the hint for that source — P2 decides on the text and says so).
- shallow source → the shallow sentence (D5), exit 2, no *local modifications* claim.
- source with no `.git` → the no-history sentence (D5), exit 2.

A manifest source absent from the clone (the manifest is ahead of upstream: S41's UAT F5) is reported as an inventory
before anything is written — the same words as `fetch_all_github` prints today (`bin/sync:144-155`), from a
`Path.exists()` loop over the clone.

`bin/status --source=github`: one clone per run, then `local_canonical_sha` and `local_history` over it for every
TRACKED source; the `history[src] = {}` line goes away.

---

## 5. Phases: one per session

**Common to every phase.** Work on `fix/sync-github-history`, branched from `upstream/main` `6b29d3d` (re-fetch and
re-verify the head at Orient). Each commit co-stages its `CHANGELOG.md` entry on the branch, as `fix/context-budget-status`
did (#86's diff carries the ledger). Run the suite **serially** (parallel runs trip GitHub's limit — Test 9). Every
verification below is run in a `--no-local` clone of the branch, never in the working tree.

### P1: the mechanism (D1, D2, D4, D8), with hermetic RED-first tests. One session.

**DONE looks like:** cherry-picked `2c4f801` and `865119f` on the branch; `bin/sync --source=github` clones and runs
the local path; `bin/status --source=github` does the same; both `gh api` fetchers gone; `METHODOLOGY_SOURCE_URL`
honoured; S41's absent-source inventory re-expressed over the clone; two new tests in `bin/tests.sh`, written **red
first** on the pre-fix code: **(1)** a Test 41-style fixture repository served as a bare clone through
`METHODOLOGY_SOURCE_URL`, a project synced from it and then set to an older version → `bin/sync <p> --source=github`
exits 0 and writes canonical, and `bin/status <p> --source=github` reads `N versions behind`, for each of Test 41's
five versions including the merge-hidden ones; **(2)** a manifest source deleted from the fixture's tree → the inventory
message and exit before any write. Test 9's guard changed per D8.
**Verification:**
```sh
bash bin/tests.sh > /tmp/p1.out 2>&1; grep -E '^(PASS|FAIL)' /tmp/p1.out | sort | uniq -c   # 0 FAIL
git stash -q && bash bin/tests.sh 2>&1 | grep -c 'FAIL'; git stash pop -q                      # the new tests FAIL on the old code
bin/sync <scratch project from 008d656> --source=github --dry-run; echo $?                     # exit 0, 10 would write, version v3.7-…
bin/status <that project> --source=github | grep -c -E 'versions? behind'                       # 9
grep -c 'gh", "api' bin/sync bin/status                                                        # 0 0
```
**Surface:** a `--no-local` clone of the branch on this machine, with network for the live run and none needed for
the tests. What it cannot enforce: the maintainer's environment (his `git` version — partial-clone flags are not used,
so any `git` that clones works), and rate limits on the live route, which the hermetic tests never hit.
**Session boundary:** one session; close out at the checkpoint commit.

**P1 outcome (S218, 2026-09-21): DONE on `fix/sync-github-history`; nothing is upstream.** `0277396` and `5f4c3f9` carry
BL-54's `2c4f801` and `865119f` with their logic unchanged: the ledger entries are rewritten in recognized terms, three
comments lose `BL-54`/`S179`, and Test 41 becomes **Test 26** (the numbered tests end at 25 on `upstream/main` and on all
four PR heads). `252a4b6` is the mechanism (D1, D2, D4, D8) with **Tests 27 and 28** and Test 9's new guard; Test 26's
fixture became the shared function `mh_fixture`. Deliberate departures from this section: **(a)** the tests serve the
fixture as `file://`, not a bare path — git ignores `--depth` when it clones a plain path, so a shallow-clone mutant
survived until the switch; **(b)** the inventory drops *"This is NOT an authentication problem"* (no authentication
remains) and names the URL rather than `REPO`; **(c)** `bin/status` prints an inventory too and exits 1 where upstream's
exited on the first failed `gh api` call; **(d)** the `tests-sh-passed` floor (139; measured 170) is **not** tightened
here, because #86 moves the same line (to 142) and P2/P3 add tests, so it belongs to P4 after the rebase; **(e)** the first
verification command above greps `'^(PASS|FAIL)'`, which matches nothing: the suite prints `  PASS:`, indented.
**Evidence:** suite 170 passed, 0 failed, 0 skipped in a `--no-local` clone of `252a4b6` (1 m 20 s);
`quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results 6d2c2313ab22 · manifest 97a7aab85b9a`; red first, Tests
26–28 on the unfixed scripts 15 passed, 16 failed (the 15 are Test 26 and four controls); nine mutants, all killed
(31 / 0 unmutated); live, one run, from `008d656` against GitHub: sync exit 0, 10 would write, `v3.7-68-g6b29d3d`, 1.6 s;
status 9 behind, 0 locally modified, 1.9 s.

### P2: the refusal (D5) and the hint text. One session, same branch.

**DONE looks like:** the two diagnoses in `bin/sync`'s blocked branch, the header no longer printed over an empty
list, the `github` hint decided and written; two RED-first tests (a `--depth 1` clone of the fixture; a `git archive`
of it) asserting the sentence and exit 2 and the absence of *local modifications* from the output; the full-history
case's text unchanged and still asserted by Test 7.
**Verification:**
```sh
bash bin/tests.sh > /tmp/p2.out 2>&1; grep -c FAIL /tmp/p2.out                                  # 0
git clone -q --depth 1 file://<full clone> shallow; shallow/bin/sync <p> --source=local --dry-run | grep -c 'shallow'   # 1
git -C <full clone> archive HEAD | tar -x -C tarball; tarball/bin/sync <p> --source=local --dry-run | grep -c 'no git history'  # 1
bin/sync <p> --source=github --dry-run 2>&1 | grep -A1 'inspect' | sed -n 2p | grep -c .       # 1 — the header has a line under it, or 0 hits for the header
```
**Surface:** as P1. **Session boundary:** one session.

### P3: the documents (D6). One session, same branch.

**DONE looks like:** every row of §2.2 marked for change is changed on the branch, on **upstream's** text
(`BOOTSTRAP.md:69`, `:85`, `:431`; `README.md:61`, `:72`; `T1_setup.md:58`; both `--help` strings); the two phrases
`:374-375` pin are still present; `./bin/check-links` OK; no other prose touched.
**Verification:**
```sh
grep -n 'gh CLI' README.md starter-kit/BOOTSTRAP.md docs/tutorials/T1_setup.md                 # 0 hits for the route
grep -c 'Size, and when to archive\|keeping any archive-pointer block' starter-kit/BOOTSTRAP.md  # both still present
./bin/check-links; bin/sync --help | grep -c 'clone'; bin/status --help | grep -c 'clone'       # OK, 1, 1
git diff --stat upstream/main -- README.md starter-kit/BOOTSTRAP.md docs/tutorials/T1_setup.md  # exactly the three files
```
**Surface:** the branch's working tree and `check-links`'s simulated adopter tree. What it cannot enforce: that the
maintainer keeps `README.md:61`'s framing; the body flags the clause as his to reword.
**Session boundary:** one session.

### P4: vet and package. One session.

**DONE looks like:** the suite green in a `--no-local` clone of the branch tip and of its trial merge into
`upstream/main`; `git merge-tree --write-tree --name-only <branch> <head>` run against each of the four PR heads with
the conflicting paths recorded in the plan (§2.5 predicts `BOOTSTRAP.md` and `CHANGELOG.md` with #84, `CHANGELOG.md`
with the rest); a dry run of the branch's `bin/sync --source=github` against each of the six adopters
(`airqino`, `church_growth`, `dalia_martinez_funeral`, `mts-system`, `vscode_quarto_ext`, `wsfct`) recorded as
before/after row counts against fork `main`'s `bin/sync`; the PR body drafted in `docs/planning/sync-github-route-pr-body.md`
in recognized terms — no session numbers, no `BL-`/`S`/`D` codes, no fork plan names; it cites issue #32's Decision 3
and #84's promised follow-up by their own words — and shown to the operator inline before the review picker.
**Verification:**
```sh
for h in 219fb9d 77afc12 e2501c5 c1167ae; do git merge-tree --write-tree --name-only fix/sync-github-history $h; done
git -C <clone of the trial merge> checkout -q <merge sha> && bash bin/tests.sh | tail -3
grep -n -E 'S[0-9]{2,3}\b|BL-[0-9]+|\bD[0-9]\b' docs/planning/sync-github-route-pr-body.md        # 0
```
**Surface:** clones on this machine; the trial merge is a local merge commit, never pushed. What it cannot enforce: the
maintainer's merge order, which is why the body states the one expected conflict and its resolution.
**Session boundary:** one session; ends at the operator's review of the body.

### P5: open the pull request. One session, outward — its own go-ahead.

**DONE looks like:** after #84 merges (or with the BOOTSTRAP conflict pre-resolved by the operator's choice, D7), the
branch rebased on the new `upstream/main`, the suite re-run on the tip, the branch pushed to fork `origin`, the PR opened
with the approved body unchanged, read back with `gh pr view --json body,headRefOid` and compared to the file, the
ledger entry for the open written.
**Verification:** the read-back diff is empty; `gh pr view <n> --json mergeable` is `MERGEABLE`.
**Surface:** GitHub. **Session boundary:** one session; nothing else that session.

### P6: fork-side adoption. After the merge, or earlier by the operator's separate decision.

**DONE looks like:** `upstream/main` merged into fork `main` (the resync pattern), the fork-only
*A note on `--source=github`* paragraph (`BOOTSTRAP.md:396-400`) reworded to match what the route now does, BL-66 and
BL-54 moved to Completed items, fork Learning row per Phase 3C with D3's retire-or-refuse.
**Verification:** `bin/status ../<adopter> --source=github` on one adopter reads the same rows as `--source=local`
from the merged checkout. **Session boundary:** one session.

---

## 6. What might break

- **Test 9 under no network** now skips on `git ls-remote` failing rather than `gh auth status`; a machine with `gh`
  but no route to GitHub used to fail the test and now skips it. Stated, not silent, as today.
- **`version:` changes shape** for the GitHub route (`github:6b29d3d` → `v3.7-68-g6b29d3d`). Nothing in `bin/tests.sh`
  pins the old form (`grep -n 'github:' bin/tests.sh` → 0); an adopter script that parsed it would notice.
- **A private mirror** that relied on `gh`'s stored credentials needs a git credential helper or the URL override.
  Named in `--help` and BOOTSTRAP.
- **Temp-dir cleanup on a crash** — `TemporaryDirectory()` removes it on normal exit and on exceptions; a `kill -9`
  leaves a 2 MB directory under the system temp root. Acceptable; noted in the docstring.
- **The maintainer's merge order.** If this PR is reviewed before #84, the BOOTSTRAP paragraph conflicts; D7's fallback
  resolves it toward #84's text in the branch and says so.

## 7. Out of scope, deliberately

- **The prose route's three rules** (fork `BOOTSTRAP.md:364-400`, §Without `bin/sync`, S41's `12463dd`): the never-overwrite table that
  protects adopter-owned ledgers when an *agent* overlays files by hand. UAT F2 found it had reached 0 of 6 adopters
  because it is **not upstream**, and it is in none of #83–#86. Independent of this mechanism, so it does not ride
  here (CLAUDE.md's batching rule cuts both ways); it has **no backlog item** — S217's handoff proposes raising one.
- A `--ref` or `--version` option for the GitHub route: the clone reads the default branch, as `gh api` did.
- A clone cache; rate-limit handling; proxies.
- Rewriting `T8_keeping_current.md` beyond the one remark: its `--source=github` instruction becomes correct.
- Any change to what is distributed: `bin/` stays canonical-only.

## 8. Verification commands (collected)

```sh
# the defect, today (any tree; needs gh for row iii)
git clone -q --no-local . r-old && git -C r-old checkout -q 008d656          # installer
git clone -q --no-local . r-full && git -C r-full checkout -q 6b29d3d        # target
mkdir p && git -C p init -q && r-old/bin/sync p --source=local >/dev/null && git -C p add -A && git -C p commit -qm i
r-full/bin/sync p --source=local  --dry-run | grep -c 'would write'         # 10, exit 0
r-full/bin/sync p --source=github --dry-run; echo $?                        # 9 refused, exit 2, empty "inspect" header
r-full/bin/status p --source=github | grep -c 'locally modified'            # 9
# the premise
/usr/bin/time -p git clone -q https://github.com/KJ5HST/methodology.git up  # ~3.8 s, 2.2 MB
/usr/bin/time -p up/bin/sync p --source=local --dry-run                     # ~2.2 s, exit 0 — the route after D1
# the code sites
grep -n 'else set()' bin/sync; grep -n 'not implemented' bin/status         # :293 / :227 (fork); :224 / :165 (upstream)
# overlap
for h in 219fb9d 77afc12 e2501c5 c1167ae; do gh pr view -R KJ5HST/methodology --json files -q '.files[].path' $h; done 2>/dev/null
```
