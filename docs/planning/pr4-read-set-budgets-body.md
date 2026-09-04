# PR 4 body — the context-budget gate (read-set budgets, 4 of 4)

**Status: REBUILT BY THE FIX-ROUND AND RE-VERIFIED, NOT PUSHED (S148, 2026-09-03).** Branch
`pr4/context-budget-gate` = `cf15489` (tree `c857734`), two commits on `cea3068`, rebuilt in a clean
clone made by the plan's §8 R1 recipe and fetched into this fork as a **local ref only** — it exists on
no remote and no PR is open. The three earlier heads are kept as refs, not branches, under
`refs/archive/pr4-context-budget-gate-<sha>`: S147's `f3a4b6d`, and this session's `46089f1` and `c6577f2`,
the two the review lenses read. Phases C (push + open) and D (merge)
each need the operator's explicit go-ahead; this header is updated from server reads when they happen.
Plan: [`pr4-read-set-budgets-plan.md`](pr4-read-set-budgets-plan.md).

- **Head:** `pr4/context-budget-gate` = `cf15489` — `8df8faa` `feat(starter-kit): ship the
  context-budget gate — token ceilings, class totals, and the repairs beneath them (read-set budgets,
  4 of 4)` then `cf15489` `chore(budget): declare this repository's own context budget`. Each carries a
  `CHANGELOG.md` line, and each was committed **through** upstream's `.githooks/pre-commit` with
  `core.hooksPath` set in the clone.
- **Base:** `read-set-budgets` = `cea3068` (unchanged since PR #78 merged; re-read at rebuild time, the
  three pins re-read: 59,168 / 52,195 / 15,386).
- **Seven files:** `starter-kit/context_budget.py` (blob `d91677b5`, byte-identical to fork `main` after
  `22c6cf0` + `544cfb0`, mode 100755, 73,040 B), `tools/test_context_budget.py` (new; **six** lines
  differ from the fork's copy: the four D9 lines and the two row-1 lines), `bin/tests.sh` (+9),
  `starter-kit/context-budget.json` (+6), `CHANGELOG.md` (+64 lines, +5,892 B), `.context-budget.json`
  (new, `cmp`-identical to the amended `pr4-candidate.context-budget.json`), `.gitignore` (+7 comment
  lines). `git diff --stat cea3068 cf15489` → 7 files, 2,320 insertions, 98 deletions.
- **Not verified here:** the maintainer's machine (the two `TestFitGateEndToEnd` tests skip in the
  clone), the network (Test 9), and `--calibrate`, which Phase B does not run.

## The fix-round (S148, 2026-09-03) — what the six rows became, and what the review lens added

S147's self-review left a six-row decision table here, each row inside something the plan ratified;
the operator chose the fix-round (*"Item (1) of S147's handoff"*). Every row was applied, the fork-side
halves committed to `main` first (`22c6cf0`, then `544cfb0` after the review lens) so the ported tool
blob stays byte-identical to the fork's — the shape row 2 prescribed. Line counts of both Python files
are unchanged, so the plan's §3.1 symbol line numbers still hold.

| # | Where | Done | Note |
|---|---|---|---|
| 1 | `tools/test_context_budget.py:9`, `:13` | `:9` → *"the tool's bin/tests.sh block covered …"*; `:13` → *"bin/tests.sh:237-244"* | branch-side only, as the row said; six lines now differ from the fork's copy |
| 2 | `starter-kit/context_budget.py` | `:289-290` (the 54,363 B file named as the authoring fork's), `:683` (the planning-doc pointer names `rmsharp/methodology`), `:733` (*"the authoring repository's history"*); plus `:675` and `:1204` (*"Phase B"* → the date) and, after the review lens, `:57` and `:1157` (*"the repo that authors this tool"* / *"this framework's own repository"* → *"the authoring fork of this tool"*) | **`:409` was NOT fork residue and is untouched:** *"learning #22 / #26a"* is upstream's own 1.0.0 text — `git blame` → `df6a991` (KJ5HST, 2026-08-08), present in blob `be2721a5`. The review had attributed the maintainer's own citation to the port (Learning #54) |
| 2, fold | `tools/test_context_budget.py:417`, `:424`, `:546`, `:484`; then `:214`, `:404` | *"Phase B"* → the date; *"wsfct"* → *"one adopter"*; *"Measured on this repo"* → *"the authoring fork"*; the fork commit `7603f10` attributed to *"the authoring fork"* rather than *"this framework's own repository"*; *"PHASE B"* in capitals (missed by a case-sensitive grep) → the date | fork side, `22c6cf0` + `544cfb0`; the seed `starter-kit/context-budget.json` `_read_cap_tokens` likewise names the fork instead of *"the project that authors this tool"* |
| 3 | `.context-budget.json` `classes.read-set._`; `files[CLAUDE.md]._` | the sentence now says the seed's own `CLAUDE.md.max_bytes` is the documented candidate and that the authoring fork's design names it; *"Accepted as is (ratified 2026-09-03)"* → *"Left as is, deliberately"* | the candidate file amended first (17,934 → 17,893 B); config `cmp`-identical to it; PROPOSAL count still 8 |
| 4 | `.gitignore:5`, `:7-8` | *"so it can be tracked to survive machine loss and clone (the authoring fork does)"*; *"reads the series, which survives a fresh clone only if tracked"* | neither history file is tracked on `cea3068`; still seven comment lines; the ledger bullet and commit (2)'s message now name both histories the comments cover |
| 5 | `CHANGELOG.md` entry | the two PRs cited by **absolute URL** (`…/pull/76`, `…/pull/78`) — the ledger's own front-matter rule, which the review lens held the first rewrite (*"#76 and #78"*) to; and *"nine fork commits (seven that went through the fork's own review rounds, plus two comment-only rewords made for this port)"* with *"every intermediate state of the tool before its reviewed end state fails them"* — the delta lens caught the count and the *"every intermediate"* the third build still carried | the PR body below keeps *"#76 and #78"*, which GitHub resolves in the upstream repository |
| 6 | commit (1) message; ledger entry | *"every git fixture a scratch repository"*; the seed sentence names the on-demand entry's note; *"six lines … four … two …"* replaces *"four lines"*; the tool's size **73,040 B** (the first rewrite still said 73,014, the pre-fix-round size) | wording only |

**The review lens on `46089f1` returned fourteen items; every one re-derived by hand before it was
acted on.** Repaired (in `544cfb0` and the rebuild): the two HIGH test-module sites (`:214`, `:404`), the
73,014 B size, the tool's `:57` / `:1157` and the seed's *"the project that authors this tool"*, the bare
`#76`/`#78`, `.gitignore:8`, the *"seven reviewed"* wording. **Kept, with the reason:** `:683` names the
fork, so the pointer resolves through that repository (upstream's own `methodology_trim.py:818` cites the
same document unattributed); *"five values are marked PROPOSAL"* is five distinct values at seven label
sites, ratified as D10; the config's *"about 37,000 tokens"* and *"about 20,193 tok"* are scoped to
`cea3068` by the config's own `_` key; `context_budget.py:71`'s `starter-kit/methodology_trim.py:129` is
correct on this tree. **Two follow-ons for the maintainer, disclosed in the PR body rather than built:**
`bin/check-learnings:87-89`'s comment (*"a file this tree lacks"*) becomes stale the moment commit (2)
lands — an eighth file, which the ratified seven-file plan does not include; and
`context_budget.py:341`'s `open(path, "rb").read()` raises a `ResourceWarning` under the new test module,
a line upstream's 1.0.0 already carries.

**Re-measured on the rebuilt tree, every DONE item again (S148, fourth build):** blob `d91677b5`, mode
100755; six-line module diff; unit `Ran 116 … OK (skipped=2)`, exit 0; `--selftest` 52 / 0; bare exit 2,
49 lines, 0 *defect*, six findings, `CHANGELOG.md` **97,257 B** (91,365 + 5,892; ≈39,416 tok at 2.4674);
`--json` `config_defects: []`; the 13-case matrix exits 2 0 2 2 0 2 0 2 0 0 0 0 0 with case 12's bare run
2 and `instrument-failed`; by hand — commit (1) vs `cea3068` with no config → **3**; with the candidate in
the worktree → **2** (`91,365 -> 95,557 B`); commit (2) vs commit (1) → **2** (`95,557 -> 97,257 B`); with
the bullet unstaged → **0**; suites on fresh clones **114/1** (control) vs **115/1** (head) vs **114/2**
(commit (1) alone) — 115 shared rows, one added, zero flips, every failure Test 9; `check-links` /
`check-learnings` / `check-handoff` / `--all` **0/0/0/0**; seven files; the identifier regex over added
lines and over both messages empty; a case-insensitive sweep of the added lines for the residue class
empty; `git status --porcelain` empty after deleting the history file.

**A second, delta lens on the frozen third build `c6577f2` confirmed all fourteen dispositions (nine
FIXED, five KEPT with the reason holding) and returned seven more items, each re-derived by hand.**
Repaired in the fourth build: *"eight fork commits (seven …, plus one comment-only reword)"* — nine and
two once `544cfb0` existed, a count the rebuild had made stale (`git log 14bd88a..main --
starter-kit/context_budget.py` → 9); *"every intermediate fails the tests that travel with it"* — the last
two intermediates (`c9c9b7b`, `22c6cf0`) pass them, so the sentence now reads *"every intermediate state of
the tool before its reviewed end state"*; `.gitignore:7-8`'s subject (the series, not the trigger,
survives a clone); and the ledger bullet and commit (2)'s message now name both histories the comments
cover. Disclosed in the PR body rather than built: the test module's `# D1`–`# D5` labels name two
different fork decision series, so `D3`/`D4`/`D5` each label two things; the banner's `≈ 20,194 tok` beside
the config's *"about 20,193"* (two 1.0.0 rounding paths); and the seed now naming `rmsharp/methodology`.
The lens's verdict was *"not yet — fix F1 and F2 first; everything else is disclosable"*; both are fixed.
**No lens ran on the fourth build itself:** its edits are two sentences in a commit message and the
entry, one `.gitignore` clause and one bullet, each checked by grep against the reviewer's own commands,
and every behavioural figure was re-measured on it.
---

## Title

`Ship the context-budget gate: token ceilings, class totals, and a root config for this repository (read-set budgets, 4 of 4)`

## Body

> **Base: `read-set-budgets`, not `main`.** Fourth and last of the four PRs staged there. Nothing here
> is proposed for `main` yet.
>
> ## What this does
>
> Ships the context-budget gate the first three PRs measured against: `starter-kit/context_budget.py`
> `1.0.0` → `1.2.0` (29,549 → 73,040 B), its 116-test module, and a root `.context-budget.json` for
> this repository. #76 and #78 shed bytes; this one **refuses growth**. On this branch, at its head:
>
> | | bytes | ceiling | |
> |---|---|---|---|
> | `starter-kit/SESSION_RUNNER.md` | 52,195 | 41,364 | over by 10,831 |
> | `starter-kit/SAFEGUARDS.md` | 15,386 | 15,386 | at ceiling |
> | read-set pair | **67,581** | **56,750** | **over by 10,831** — exactly what #76's table left |
> | `CHANGELOG.md` | 97,257 | 65,536 | over by 31,721; ≈39,416 tok at 2.4674 B/tok (91,365 B on the base; this PR's own entry is the difference) |
> | `HANDOFFS.md` | 70,182 | 65,536 | over by 4,646; ≈29,677 tok at 2.3648 B/tok |
>
> The bare run exits 2 with that table: six red findings on day one — five per-file ceilings across
> three files, plus the read-set class total. The two token estimates use densities measured on the
> fork's copies of these same-format ledgers, not on this tree; each ledger's `_` key gives the
> doubled-file method to re-measure them here. `--precommit` refuses any commit that grows either file
> in bytes (or, for a whole-read class, in estimated tokens) and passes any that shrinks one (verified:
> +2 B refused; −5,000 B passed while still over); line-count and structure checks run in the bare and
> `--json` modes only. **Nothing on this branch shrinks the pair; this PR makes it stop growing and say
> why.**
>
> ## The tool refuses to run without a config, so this PR provisions one
>
> Your 1.0.0 already exits 3 — *"refuses to invent budgets for a project that has not declared them"*
> — at any root without `.context-budget.json`; that is unchanged. The seed adopters receive reads red
> here for reasons unrelated to this series (`CLAUDE.md` is 59,168 B against the seed's 28,000). So the
> config in this PR **pins** `CLAUDE.md` at its arrival size, **derives** the read-set ceiling from the
> read cap (25,000 tok × 2.27 B/tok = 56,750, computed at run time — 25,000 is `read_cap_tokens` in the
> config — the number in the Read tool's own refusal, `exceeds maximum allowed tokens (25000)`, Claude
> Code 2.1.259; 2.27 is the tool's `MIN_BYTES_PER_TOKEN` floor at `starter-kit/context_budget.py:68`, a
> constant, not a key, so a different floor is a tool edit), and **declares** the two ledgers
> Phase 0 reads and the Learnings table your `bin/check-learnings` already cites this file for.
>
> ## Every ceiling in that config is yours; five are proposals rather than measurements
>
> 1. **`CLAUDE.md` pinned at 59,168 B** (growth refused, shrink passes). Alternative: the seed's
>    28,000 / 34,000, which reads *over by 31,168* today.
> 2. **`CHANGELOG.md` and `HANDOFFS.md` at 65,536 B** — the fork's ceiling, **not the trimmer's**:
>    #77's `methodology_trim.py` triggers at 196,608 B and reports *trigger does not fire* on both
>    ledgers today (97,257 B and 70,182 B). Bringing either under this ceiling is
>    `python3 starter-kit/methodology_trim.py --file <ledger> --budget-bytes 65536` (dry-run by
>    default; add `--write`), `CHANGELOG.md` first — a `HANDOFFS.md` trim writes its own entry into
>    `CHANGELOG.md`, which the gate refuses while that file is over. The trimmer stops at half the budget
>    (measured on the base: 91,365 → 30,920 B, 30 of 39 records; 70,182 → 26,891 B, 7 of 10), appends
>    one `CHANGELOG.md` entry per trim, and refuses on an unreconciled tree. **At the carried densities
>    the token ceiling binds first** — 25,000 tok is 61,685 B for `CHANGELOG.md` and 59,120 B for
>    `HANDOFFS.md` — so 65,536 B fires first only if a re-measured density comes in above 2.62 B/tok.
>    Alternative: omit the byte ceiling and keep `max_tokens`, or omit both and let the trimmer's number
>    govern.
> 3. **`SAFEGUARDS.md` pinned at 15,386 B**, so the whole 10,831 B of debt sits on `SESSION_RUNNER.md`.
> 4. **`FRAMEWORK_LEARNINGS.md` at 73,728 B**, on-demand, no token ceiling — at its measured 2.8897
>    B/tok that sits 1,486 B above the one-read cliff; the `_` key says so.
> 5. **Two more numbers, neither measured:** `read-set.warn_bytes` 51,000 B is the fork's choice, marked
>    PROPOSAL in its `_` key — ~10% under the derived total so the class warns before it refuses;
>    inert while the class is over, which it is today — and `CLAUDE.md.max_lines` 200 is
>    `starter-kit/BOOTSTRAP.md:198`'s own *"roughly 200 lines"* applied to your `CLAUDE.md` (126 lines
>    today by `wc -l`; bare run only, `--precommit` ignores it). Delete either key if you do not want it.
>
> The calibration constants are the seed's. After merge, run `python3 starter-kit/context_budget.py
> --calibrate`; it writes nothing. If it admits a fit (R² ≥ 0.50, positive slope), set `bytes_per_token`
> to the fitted value. Until then `CLAUDE.md`, `SESSION_RUNNER.md` and `SAFEGUARDS.md` are judged at the
> seed's 2.93 B/tok — `CLAUDE.md` reads ≈20,194 tok in the header, `ok`; at the 2.27 floor the same bytes
> read 26,065, `over` — and `CLAUDE.md`'s derived 26,065-token ceiling is clamped to 25,000 without a
> message, because only a *declared* `max_tokens` is reported when clamped. If your harness's read cap
> differs, set `read_cap_tokens` and every derived ceiling follows.
>
> ## Day one, and what does not change
>
> - **This PR's own two commits fail the gate it ships, run by hand:** exit 3 on the first (no config
>   yet — nothing evaluated), exit 2 on the second (its `CHANGELOG.md` bullet grows a file already over
>   65,536 B: `95,557 -> 97,257 B`). The gate is not wired into `.githooks/pre-commit`; nothing refuses
>   these commits. Both carry a ledger line because your `.githooks/pre-commit` requires one, and both
>   were committed through it. If you chain the budget check in later, every commit that appends to a
>   ledger is refused until **that** ledger is under 65,536 B — and the hook's documented `--no-verify`
>   bypass applies to the budget check too. This PR claims no enforcement.
> - **The first commit alone leaves one `bin/tests.sh` row red** (`114 passed / 2 failed`): the wired
>   unit-test row fails until the second commit's config exists, because the tool exits 3 without one
>   and the module's selftest test needs it. The split is deliberate — the policy file is reviewable
>   apart from the code — and the first commit's message says so.
> - `python3 starter-kit/context_budget.py` exits 2 with the table above and creates
>   `.context-budget-history.jsonl`, untracked (the fork tracks it; your call — the `.gitignore` comment
>   explains). `--precommit`, `--selftest`, `bin/tests.sh` write nothing.
> - **Nothing else in your workflow changes unless you wire the hook — except one added `bin/tests.sh`
>   row**, which fails whenever the unit module fails (including the two machine-dependent tests under
>   Verification). `core.hooksPath` is local config; `.githooks/pre-commit` is the ledger gate and this PR
>   does not chain the budget into it.
> - **Do not run `install-hook` at this root.** On a clone without `core.hooksPath` it installs
>   `.git/hooks/pre-commit` pointing at `<root>/context_budget.py`, which does not exist here, and every
>   commit then fails with `can't open file`; recover with `rm .git/hooks/pre-commit`. With
>   `core.hooksPath=.githooks` it declines.
> - `SESSION_RUNNER.md` Phase 0 still never names the tool. Adding one line grows the capped file
>   ~300 B. Not done here; your decision.
> - The dashboard twins are untouched (`2.17.0` on the fork vs `2.10.7` here; separate series).
>
> ## What changes for adopters who sync
>
> Exit codes are unchanged (`0/1/2/3`). On an unchanged seed config, two things differ:
> (1) when nothing fires, a read-mandated row reports **bytes, not lines** (`305 ln / 400 ln ok` →
> `60,048 B / 120,000 B ok`); (2) a read-mandated file **above 73,252 B** — the first size whose
> truncated estimate `int(bytes / 2.93)` exceeds 25,000 tokens is 73,253 B (≈25,001 tok) — now gets a
> **derived token ceiling** the old tool never had, and goes `ok` → `over`, exit 1 → 2, even under every
> byte and line ceiling the adopter declared — measured at 73,253 B and 73,548 B; 73,252 B still `ok`.
> Also new: ceilings may be declared in tokens (`max_tokens`); a `max_tokens` above the cap is
> **clamped to the cap and reported as a config defect** — the clamp is never silent; the gate sizes
> the **index** with `git cat-file -s` (the old path was 1 B short on LF, more on CRLF, and raised on
> non-UTF-8 content); `precommit` gains a class-total arm; `calibrate` walks first-parent history,
> compares timezone-aware stamps, and refuses a fit below R² 0.50; the ledger row names the ceiling
> that fired in its own unit; remediation text no longer says *here* about a measurement taken on
> another project. The seed gains `read_cap_tokens`, two `max_tokens` keys and a note on its on-demand
> entry saying why that one gets none (+6 lines); it is seed-once, so no existing adopter config changes.
>
> ## Verification
>
> Clean clone of `cea3068`, every figure taken from the tree at the head after the last edit.
>
> | | base `cea3068` | this branch |
> |---|---|---|
> | `bash bin/tests.sh` | **114 passed / 1 failed** | **115 passed / 1 failed** |
> | `python3 tools/test_context_budget.py` | — | **116 run, OK, 2 skipped**, exit 0 |
> | `python3 starter-kit/context_budget.py --selftest` | — | **52 PASS / 0 FAIL**, exit 0 |
> | bare run | exit 3 (no config) | **exit 2**, six findings, `config_defects: []` |
> | `check-links` / `check-learnings` / `check-handoff` / `--all` | — | **0 / 0 / 0 / 0**, each read bare |
>
> Diffed **row for row**: **115 shared labels, zero status flips, exactly one row added**
> (`PASS: context budget gate unit tests green`). The single failure is the same on both sides:
> Test 9 (`bin/sync --source=github` reads `main`, where three manifest sources are absent until this
> branch merges). The 13-case `--precommit` matrix from the plan reproduces on the head: +2 B on any
> budgeted file over or at its ceiling → exit 2 `REFUSED`; a shrink on a file still over → 0; +2 B on
> `FRAMEWORK_LEARNINGS.md` (under) and on `README.md` (unbudgeted) → 0; a `## Versioning` → `## Version`
> edit → `--precommit` 0 and the bare run 2 with `instrument-failed`; nothing staged → 0.
>
> The two skips are `TestFitGateEndToEnd` (`tools/test_context_budget.py:330`), which needs *this
> repository's* session transcripts on the running machine. **On yours they run if
> `~/.claude/projects/<your-checkout-slug>/*.jsonl` exists, and they can fail for reasons that are not
> the tool:** fewer than 3 commits touching `CLAUDE.md`, fewer than 4 transcripts with a usage record
> dated at or after the file's first recorded size, a `CLAUDE.md` that was the same size at every usable
> session, a fitted slope ≤ 0, or opening context that never varied (R² undefined). If the new
> `bin/tests.sh` row is red, run `python3 tools/test_context_budget.py -v 2>&1 | grep -B1 -A1
> AssertionError` — the tests capture `calibrate()`'s stdout, so its own diagnosis (*"only N usable
> sessions — not enough to fit"*, *"no variation in CLAUDE.md size"*) appears only inside the
> `AssertionError:` text; `grep -A2 FitGateEndToEnd` shows a `skipped` suffix naming the missing
> directory.

---

## What a reviewer should look at

1. **`.context-budget.json`** — every `_` key states a derivation and marks what is a PROPOSAL (five
   values, eight label sites). The numbers are the maintainer's to move; the file says which.
2. **The `CHANGELOG.md` entry** — it is the PR's own record on the ledger the gate declares, and the
   second commit's bullet says the gate refuses it.
3. **`tools/test_context_budget.py`** — new upstream, 116 tests; six lines differ from the fork's copy:
   four replaced a fork-relative identifier with the date of the change, two replaced a reference to
   the fork's numbered `bin/tests.sh` block with a description of this tree's.

## What this PR deliberately does not do

- **It does not carry the dashboard twins** (`2.17.0` on the fork, ten labels above this base's
  `2.10.7`) — a separate series. Nor the fork's own root config, its measurement history, its
  `.githooks/pre-commit` additions, or its `bin/_manifest.py` comments.
- **It does not wire the gate.** `.githooks/pre-commit` is untouched; the config's `_` key and the
  ledger bullet both say the gate is measuring-only here.
- **It does not run `--calibrate`** and adopts no fitted density; the constants are the seed's.
- **Two one-line follow-ons it leaves to you, named so they are chosen rather than forgotten:**
  `bin/check-learnings:87-89` says the root config is *"a file this tree lacks"*, which stops being true
  the moment the second commit lands (the checker is canonical-only, so the fix is one comment line);
  and `starter-kit/context_budget.py:341`'s `open(path, "rb").read()` — your 1.0.0 line — surfaces a
  `ResourceWarning` on stderr under the new test module (`bin/tests.sh` redirects it; nothing fails);
  the test module's `# D1`–`# D5` section labels come from two different decision series in the fork's
  planning (the five defects of the 2026-08-15 `calibrate()` repair, `:82`–`:372`, and the 2026-08-30 gate
  decisions from `:666`), so `D3`, `D4` and `D5` each label two things — a two-line legend at the module
  head, or a renumbering, is yours; and the banner's `≈ 20,194 tok` beside the config's *"about 20,193"*
  is one quantity through two 1.0.0 rounding paths (`int()` at `:386`, `:,.0f` at `:599`).
- **One thing adopters receive that they did not before:** the seed's `_read_cap_tokens` note now names
  the fork where 1.2.0 was developed (`rmsharp/methodology`) as the site of the measurement it cites,
  rather than *"the project that authors this tool"*, which on this tree reads as you. Reword it if you
  would rather the seed not name a third repository.
