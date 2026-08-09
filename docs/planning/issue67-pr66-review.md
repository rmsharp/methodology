# Issue #67 and PR #66 vs. this fork's current state — review

**Session:** S56 (2026-08-09) · **Task:** operator-directed — do this fork's local changes already
address upstream [issue #67](https://github.com/KJ5HST/methodology/issues/67) or
[PR #66](https://github.com/KJ5HST/methodology/pull/66)? · **Verdict: NEITHER, and one is worse than
absent.** Issue #67 describes a live, unfixed, currently-**shipped** defect in this fork's own
`tools/methodology_dashboard.py` / `starter-kit/` twin — not merely an upstream gap. PR #66 is not
safely mergeable as-is: two concrete, reproduced collisions with fork-specific state, one of them a
silent no-op in the exact shape PR #66's own rationale warns against.

## Method

Read both fully — `gh issue view 67 --json body,comments`, `gh pr view 66 --json body,files,...`, and
the complete PR diff (`gh pr diff 66`) — then verified every claim below directly against this fork's
actual tracked files and real git history, never accepted from the issue/PR text alone. No outward
action taken; read-only against `upstream/main` throughout (`gh` reads only).

---

## Issue #67 — reproduced live in this fork's own shipped code, not fixed by anything local

Issue #67's complaint: `check_stale_version()`'s warning recommends `--sync` as the remedy for "your
copy is old," but `--sync` is a **26-file, 25-repo portfolio write**, and bare `--dry-run` (without
`--sync`) is not a no-op.

**All three parts reproduce verbatim in this fork's own `tools/methodology_dashboard.py`
(`DASHBOARD_VERSION = "2.13.0"`, `:87` — already past the `v2.10.2` the issue's own example warning
names, so this is not "haven't pulled a fix yet," it is an unfixed defect this fork independently
carried through several of its own dashboard campaigns, S36/S38/S39′ among them):**

- `check_stale_version()` (`:764-777`) still prints only the portfolio remedy:
  `f"    Re-sync: python3 {canonical} --sync\n"` — no scoped, single-project alternative.
- `main()` (`:3916-3928`) checks `"--sync" in args` **first** (`:3923`); only inside that branch is
  `dry_run` consulted. A bare `python3 methodology_dashboard.py --dry-run` falls through to
  `check_stale_version()` and a full scan that writes `dashboard.html` and appends to
  `dashboard_history.jsonl` — reproduced live this session (Phase 0 orientation ran exactly this
  command from the portfolio root and it wrote both files, matching the issue's "second, smaller
  footgun" exactly).
- `sync_dashboards()` (`:989-1051`) **partially** does better than the issue implies is missing: it
  already prints scope before writing (`"Targets: portfolio root + N project(s)"`,
  `"Would change X of Y target(s)"`) — issue #67 suggestion 3's first half. It does **not** do the
  second half: no `--yes` gate for a git-tracked target or a newly-created file in a repo that does
  not ignore the path — those targets are flagged with an inline note and written anyway (or, under
  `--dry-run`, merely reported).
- None of issue #67's four suggested fixes (scoped remedy in the warning; `--sync-self`/target-dir
  flag; state-scope-and-require-`--yes`; make bare `--dry-run` a no-op or error) exist in
  `print_usage()` (`:1054-1066`) or anywhere else in this file.

**Confirmed distributed:** `bin/_manifest.py:44` lists
`("starter-kit/methodology_dashboard.py", "methodology_dashboard.py", TRACKED)` — every adopter of
this fork (`wsfct`, `mts-system`, `vscode_quarto_ext`, `model_project_constructor`, `nprcgenekeepr`,
…) receives this exact code path via `bin/sync`.

**Not the same tool, and not affected:** this fork's own `bin/sync` (the tool actually used against
`wsfct`/`mts-system`/`vscode_quarto_ext` this campaign) is unrelated code entirely — it always takes
an explicit target-repo argument (`bin/sync ../wsfct`) and never defaults to a portfolio-wide sweep.
Issue #67 is entirely about `methodology_dashboard.py`'s own `--sync`/`sync_dashboards()`, a
self-referential "sync my own file across every sibling project" mechanism with no relationship to
`bin/sync`'s adopter-distribution job beyond sharing a repo.

**Verdict: unaddressed, fork-side-fixable today, independent of anything upstream does.** Fixing it
touches a `TRACKED` distributed file, so — per this repo's established pattern (BL-20, BL-22) — the
fix itself can be written and tested fork-side now; only the eventual upstream PR needs a go-ahead.

---

## PR #66, Finding 1 — `context_budget.py install-hook` silently no-ops against this fork's own hook convention

PR #66 ships `starter-kit/context_budget.py`, whose `install_hook()` (diff lines ~1593-1608) resolves
the hooks directory via `git rev-parse --git-dir` and always targets
`os.path.join(<git-dir>, "hooks", "pre-commit")` — i.e. `.git/hooks/pre-commit`. It has **no
awareness of `core.hooksPath`** anywhere in the function.

This fork already redirects hook lookup: `.githooks/pre-commit` (the FM #27 ledger-co-staging gate,
BL-6 item 3) is enabled via `git config core.hooksPath .githooks`, specifically so hooks live outside
`.git/hooks`. If a session ran `python3 context_budget.py install-hook` on a clone with that config
set:

1. It creates `.git/hooks/pre-commit` — a location git will **never consult**, because
   `core.hooksPath` redirects the lookup to `.githooks/` for every hook, not just the ones already
   defined there.
2. It prints `"installed {p}"` — a **success message for a file that will never run.**

This is not hypothetical for this fork specifically: `git config core.hooksPath` here is set to
`.githooks` (confirmed — that is how the existing FM #27 gate fires at all), so `install_hook()` as
shipped would silently do nothing while reporting success — the exact "measurement/mechanism present,
nothing gates on it" failure PR #66's own FM #28 prose exists to name, reproduced by PR #66's own
installer. (Separately, and consistent with this: the PR's own dev-session note in its `CHANGELOG.md`
diff records `git config core.hooksPath` as **unset** in the environment PR #66 was built and tested
in — so the author's own verification never exercised this path.)

**Fix, if adopted:** `install_hook()` needs to read `core.hooksPath` first and write there when set
(or refuse and print the line to add manually, which is already its fallback behavior for a
foreign existing hook) — or, matching this repo's own sequencing precedent for wiring a detector into
`.githooks/pre-commit` (BL-19 §5, S43-then-S44: detector first, gate-wiring as a separate later step),
add `--precommit` as one more line inside the *existing* `.githooks/pre-commit` rather than installing
a second, competing hook file.

## PR #66, Finding 2 — `bin/check-handoff --all`'s new duplicate-session check reproduces the exact issue #65 flaw this fork already found

PR #66 also extends `bin/check-handoff` with an `--all` mode (diff lines ~275-460) — explicitly framed
in its own comment as answering "issue #65" — including a cross-block invariant that a `session:`
value must be unique across every receipt (`validate_ledger()`, keyed as `seen[sid]` where
`sid = fields.get("session", "").strip()` — a bare session id, no date component).

**This is the identical invariant, and the identical flaw,
[`issue-65-collision-review.md`](issue-65-collision-review.md) (BL-23, S47) already found false
against this repo's real ledger — now shipped as code rather than proposed as an issue.** Re-verified
live this session, not assumed from that prior review:

```
$ grep -h "^session: " HANDOFFS.md docs/archive/HANDOFFS-archive.md | sort | uniq -c | sort -rn | awk '$1>1'
      2 session: S8
      2 session: S7
      2 session: S5
      2 session: S3
```

Four real, intentional, documented duplicates (`HANDOFFS.md:16-21`: *"This fork and `upstream/main`
each run their own `S<N>` counter, so a receipt is identified by session + date, never by number
alone"*). Running PR #66's `bin/check-handoff --all` against this fork's actual `HANDOFFS.md` +
archive would print four false "duplicate session id" findings on receipts that are correct, intended
history. This fork's own `bin/check-handoff` already knows this and says so in writing (`:74`):
*"#65 separately proposes a `--all` mode for this tool covering different ground"* — i.e., this repo
deliberately built the BL-14/BL-17 answer-slot checks without implementing #65's asks, precisely
because #65's asks needed exactly this scrutiny first. PR #66 does not add that scrutiny; it ships
the same invariant BL-23 already flagged as needing "a session+date compound key, or an explicit
archive/sequence exclusion" before it can run safely here.

**Fix, if adopted:** key the duplicate check on `(session, date)`, or explicitly special-case the
fork/upstream dual-sequence pattern this repo's own `HANDOFFS.md` front matter documents.

## Adjacent, not a collision — PR #66 overlaps ground this fork already planned, and exceeds it

This fork's own `docs/planning/framework-context-cost-plan.md` (BL-19, S30-S40, five heuristics
H1-H5) already covers the identical problem PR #66's FM #28 names — monotonically growing
mandatory-read artifacts — and explicitly queues **S45**: *"`bin/check-context-budget` and port
H1-H4 into the dashboard... asserted as a test"* (still unshipped — "PR, needs go-ahead", no
`SHIPPED` note, §5's queue table).

The two designs are not equivalent, though: every one of BL-19's H1-H5 heuristics is **read-only,
reported through `methodology_dashboard.py`** — none blocks a commit. `context_budget.py --precommit`
is an actual commit-**refusing** gate for file size. BL-19's plan never proposed a size-based commit
gate at all (it explicitly declined a *different* thing, a "standing gate-bypass gauge," for a
different reason — gaming by hook deletion, §3.6). Whether this repo wants a size-enforcing precommit
gate (PR #66's model) or wants to stay at pure measurement (BL-19's planned S45) is a real, undecided
design question — an operator decision, not a collision to fix, and not this session's to answer.

**Also noted, not a defect:** FM #28 slots cleanly after this fork's own FM #27 with no renumbering —
but adopting it means mirroring the same "27 → 28" count-assertion edits PR #66 makes upstream
(`CLAUDE.md`, `README.md`) into this fork's own copies of those same two files
(`CLAUDE.md:103`, `README.md:233` both currently assert "27").

## Checked and cleared — no other collision found

- `bin/_manifest.py` has no `context_budget`/`context-budget` entry — this fork has not started any
  parallel implementation that PR #66 would duplicate or conflict with.
- PR #66's other touched files (`bin/tests.sh`, `docs/tutorials/*`, `bin/check-learnings` — a new,
  separate checker) do not reference anything this fork has locally diverged on; not reviewed
  line-by-line since neither collision found required it, and neither is blocking either finding
  above.
- Open BACKLOG.md items (BL-8, BL-11 through BL-25) — none touch `context_budget.py`,
  `.githooks/pre-commit`'s content (only its seed *documentation*, BL-21), or `bin/check-handoff`'s
  `--all`/session-uniqueness surface.

## Recommendation

This session takes no outward-facing action — review is the deliverable. For the operator:

1. **Tracked as `BL-26`** (`docs/planning/BACKLOG.md`) so this doesn't sit unaddressed a further
   handful of sessions the way #65/#66 already have (offered and declined at BL-25's claim, S53).
2. **Issue #67 is fork-side-fixable now**, independent of upstream: fix `check_stale_version()`'s
   message and the bare-`--dry-run` fallthrough in both `tools/`/`starter-kit/` twins. Matches the
   BL-20/BL-22 pattern — measure, fix fork-side, PR needs a go-ahead when ready.
3. **Do not merge PR #66 as-is.** If/when this fork adopts it (or writes its own equivalent), it
   needs the two fixes above (`core.hooksPath` awareness in `install_hook()`; a session+date compound
   key in the duplicate check) — both are concrete, both are cheap, neither has been asked of the
   PR author.
4. **The size-enforcing-gate-vs-dashboard-reporting question is a real open design decision**,
   parallel to BL-19 §7's existing operator-decision items — put it there rather than deciding it
   implicitly by merging or ignoring PR #66.
5. No comment, close, or PR action taken on either #67 or #66 — both remain exactly as found.
