# PR 4 body — the context-budget gate (read-set budgets, 4 of 4)

**Status: BUILT AND VERIFIED, NOT PUSHED (Phase B, 2026-09-03).** Branch `pr4/context-budget-gate`
= `f3a4b6d` (tree `7541e3ee`), two commits on `cea3068`, built in a clean clone made by the plan's §8
R1 recipe and fetched into this fork as a **local ref only** — it exists on no remote and no PR is
open. Phases C (push + open) and D (merge) each need the operator's explicit go-ahead; this header is
updated from server reads when they happen. Plan: [`pr4-read-set-budgets-plan.md`](pr4-read-set-budgets-plan.md).

- **Head:** `pr4/context-budget-gate` = `f3a4b6d` — `28406ce` `feat(starter-kit): ship the
  context-budget gate — token ceilings, class totals, and the repairs beneath them (read-set budgets,
  4 of 4)` then `f3a4b6d` `chore(budget): declare this repository's own context budget`. Each carries a
  `CHANGELOG.md` line, and each was committed **through** upstream's `.githooks/pre-commit` with
  `core.hooksPath` set in the clone (a first attempt without the ledger line was refused by it).
- **Base:** `read-set-budgets` = `cea3068` (unchanged since PR #78 merged; re-read at build time).
- **Seven files:** `starter-kit/context_budget.py` (blob `c5ff15e5`, byte-identical to fork `main`,
  mode 100755), `tools/test_context_budget.py` (new; four lines differ from the fork's copy),
  `bin/tests.sh` (+9), `starter-kit/context-budget.json` (+6), `CHANGELOG.md` (+59 lines, +5,385 B),
  `.context-budget.json` (new, byte-identical to `pr4-candidate.context-budget.json`), `.gitignore` (+7
  comment lines). `git diff --stat cea3068 f3a4b6d` → 7 files, 2,315 insertions, 98 deletions.
- **Not verified here:** the maintainer's machine (the two `TestFitGateEndToEnd` tests skip in the
  clone), the network (Test 9), and `--calibrate`, which Phase B does not run.

## Adversarial self-review of the frozen branch (Phase B, 2026-09-03) — findings awaiting the operator

Two independent read-only reviewers attacked `f3a4b6d` in their own clones: one against the plan's
Phase B DONE list (every item MET, no departures; three cosmetic observations), one as the upstream
maintainer reading every claim against the tree. The second returned twelve items; each was re-derived
by hand before it was kept, and every one re-derives. **None was repaired, because each sits inside
something the plan ratified** — the four-line D9 scrub, the verbatim candidate config, the
byte-identical tool blob `c5ff15e5`, the ported `.gitignore` lines — so amending it is the operator's
decision, not the build's. The branch is unpushed; a fix-round rewrites two commits and re-measures on
a fresh clone. **Recommendation: run that fix-round before Phase C**, in this order.

| # | Where | What the maintainer sees | Proposed repair | Ratified item touched |
|---|---|---|---|---|
| 1 | `tools/test_context_budget.py:9`, `:13` | *"Test 35 in bin/tests.sh"* — upstream's block is unnumbered (`== Test: context_budget.py ==`); *"bin/tests.sh:248-251"* — the trimmer row is `:240-244` on the branch and `:249` is the new row itself | `:9` → *"the `context_budget.py` block in bin/tests.sh covered …"*; `:13` → *"at bin/tests.sh:237-244"*. Six lines then differ from the fork's copy; D11's back-port carries six | D9 (four lines) |
| 2 | `starter-kit/context_budget.py:289-290`, `:409`, `:683`, `:733` | *"this repository's own starter-kit/SESSION_RUNNER.md is 54,363 B"* (52,195 B on `cea3068` — a fork-era size, false at every adopter root); *"(Reproduction: docs/planning/read-cap-premise-correction-plan.md, Appendix A.)"* (absent upstream); *"learning #22 / #26a"* (no row 26a); *"this repository's own history"* | Fix in the **fork's** tool first — one fork commit on `main` (*"a 54,363 B file measured 54,362"*; drop the planning-doc pointer or name it as the fork's; *"#26"*; *"the authoring repository's history"*) — then re-port, so the blob stays byte-identical to fork `main` and the plan's `c5ff15e5` criterion is re-stated with the new id | §3.1 / the DONE blob id |
| 3 | `.context-budget.json`, `classes.read-set._` | *"The governing design (upstream-read-set-pr-plan.md 3.4(c)) names 28,000 B"* — a fork planning file the maintainer cannot open (the number is also the seed's own `CLAUDE.md.max_bytes`, said in the same sentence) | *"The seed's own `CLAUDE.md.max_bytes`, 28,000 B — the always-read file the framework does not own — is the documented candidate (the fork's governing design names it)"*; amend `pr4-candidate.context-budget.json` to match | Appendix A, copied verbatim |
| 4 | `.gitignore:3-5` | *"it is tracked to survive machine loss"* — neither history file is tracked on `cea3068` (both are, in the fork) | *"so it can be tracked to survive machine loss — the authoring fork tracks it"* | §3.6, ported verbatim |
| 5 | `CHANGELOG.md` entry, *What it buys* | *"PRs 1 and 3 shed bytes"*, *"PR 1's table"* — the upstream ledger never numbers the series; it knows #76 and #78 | *"#76 and #78 shed bytes"*, *"#76's table"* (the PR titles carry *"N of 4"*, so both forms resolve) | D8 prose, not a criterion |
| 6 | commit (1) message; ledger entry | *"every fixture a scratch repository"* — 75 of 116 tests build no fixture (pure arithmetic); *"gains `read_cap_tokens` and a `max_tokens` on each of its two whole-read entries (+6 lines)"* omits the `_max_tokens` note on the on-demand entry | *"every git fixture a scratch repository"*; *"… and a note on the on-demand entry saying why it gets none"* | wording only |

**Kept as ratified, with the reason:** the two `TestFitGateEndToEnd` tests can *fail*, not skip, on a
machine with transcripts (the body's Verification section names the causes and the diagnosis — plan
§3.2); the densities and `FRAMEWORK_LEARNINGS.md`'s 73,728 B are fork measurements the tree cannot
re-derive (labelled PROPOSAL / *measured on the fork*; D1, D7, D10); *"five values are marked
PROPOSAL"* against eight grep hits (five distinct values, seven label sites, one definition — D10);
the bare-run header's 20,194 against the row's 20,193 (round vs `int`, §3.3); *"Phase B"* and
*"wsfct"* in the test module and the *"Accepted as is (ratified 2026-09-03)"* phrase in the config
(fork vocabulary inside ratified blobs — fold into rows 2 and 3 if the fix-round runs); the
commit-message trailers (the series' own upstream precedent carries them).

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
> `1.0.0` → `1.2.0` (29,549 → 73,014 B), its 116-test module, and a root `.context-budget.json` for
> this repository. PRs 1 and 3 shed bytes; this one **refuses growth**. On this branch, at its head:
>
> | | bytes | ceiling | |
> |---|---|---|---|
> | `starter-kit/SESSION_RUNNER.md` | 52,195 | 41,364 | over by 10,831 |
> | `starter-kit/SAFEGUARDS.md` | 15,386 | 15,386 | at ceiling |
> | read-set pair | **67,581** | **56,750** | **over by 10,831** — exactly what PR 1's table left |
> | `CHANGELOG.md` | 96,750 | 65,536 | over by 31,214; ≈39,211 tok at 2.4674 B/tok (91,365 B on the base; this PR's own entry is the difference) |
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
>    ledgers today (96,750 B and 70,182 B). Bringing either under this ceiling is
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
>   65,536 B: `95,079 -> 96,750 B`). The gate is not wired into `.githooks/pre-commit`; nothing refuses
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
> another project. The seed gains `read_cap_tokens` and two `max_tokens` keys (+6 lines); it is
> seed-once, so no existing adopter config changes.
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
3. **`tools/test_context_budget.py`** — new upstream, 116 tests; the four lines that differ from the
   fork's copy each replaced a fork-relative identifier with the date of the change.

## What this PR deliberately does not do

- **It does not carry the dashboard twins** (`2.17.0` on the fork, ten labels above this base's
  `2.10.7`) — a separate series. Nor the fork's own root config, its measurement history, its
  `.githooks/pre-commit` additions, or its `bin/_manifest.py` comments.
- **It does not wire the gate.** `.githooks/pre-commit` is untouched; the config's `_` key and the
  ledger bullet both say the gate is measuring-only here.
- **It does not run `--calibrate`** and adopts no fitted density; the constants are the seed's.
