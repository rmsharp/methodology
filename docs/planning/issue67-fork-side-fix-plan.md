# Issue #67 fork-side fix — proposed plan (full fix, upstream-PR-ready)

**Status:** PROPOSED — awaiting operator ratification (not yet approved for implementation).
**Deliverable of S57:** this plan. **Implementation is a future session's deliverable, not this
one's** — no code in `tools/methodology_dashboard.py` or `starter-kit/methodology_dashboard.py` is
touched by S57.
**Scope:** `tools/methodology_dashboard.py` + its byte-identical twin `starter-kit/methodology_dashboard.py`
(verified byte-identical at S57's HEAD via `diff -q`), plus one existing test
(`tools/test_methodology_dashboard.py`).
**Resolves:** upstream [issue #67](https://github.com/KJ5HST/methodology/issues/67), covering **all
four** fixes the issue names — not the minimal subset. **Does not touch PR #66** — BL-26's other
thread (the `install_hook()`/`core.hooksPath` collision and the `bin/check-handoff --all`
duplicate-session flaw) is untouched and remains separately open.
**Builds on:** `docs/planning/issue67-pr66-review.md` (S56's evidence review — read first) and
`docs/planning/BACKLOG.md` BL-26.

---

## 1. Method — how this design was reached

Three independent candidate designs were generated in parallel by fresh agents (no shared state,
each given the same evidence packet: the issue's four asks, the actual current source of
`check_stale_version()`, `sync_dashboards()`, `main()`, `print_usage()`, `find_canonical()`, this
repo's testing/versioning/twin-file conventions), then each scored by two independent judges on two
lenses (issue-completeness-and-new-footguns; smallest-safe-diff/testability/style/cold-maintainer
defensibility) — six scores total, every judge instructed to verify claims against the real file, not
the candidate's own prose.

| Candidate | Mechanism | Completeness | Diff quality | Avg |
|---|---|---|---|---|
| MINIMAL | `--sync-self` + `--yes`, both threaded as new kwargs on the existing `sync_dashboards()` | 6/10 | 7/10 | 6.5 |
| LITERAL | `--sync-self` + `--yes` as issue's own verbatim names, separate `sync_self()` function | 6/10 | 6/10 | 6.0 |
| GENERAL | `--sync [TARGET_DIR]` — one generalized flag, self-sync falls out of it for free | 7/10 | 5/10 | 6.0 |

No candidate scored above 7/10 — every one had at least one real, judge-verified defect (verified a
second time directly against the source for this document, not taken on the judges' word either; see
§3). **The design below is a synthesis, not a pick**: it takes GENERAL's mechanism (highest
completeness, the only one with no future third-flag need), grafts LITERAL's `.gitignore`-aware
create-gate (the most faithful reading of the issue's own wording), and repairs every concrete flaw
every judge found in every candidate — including two defects **every single candidate missed**
(§3, rows 6–7). Full candidate text, scores, and rationale: workflow run `wf_36c11a44-4ac`
(this session, S57).

**Then, per this repo's own "never self-certify" convention, the synthesized plan itself was put
through a second, independent four-lens adversarial review** (code-correctness hand-trace,
citation-accuracy re-verification, design-panel-completeness re-derivation, test-plan soundness —
workflow run `wf_54b22b55-836`, this session) before being finalized. That pass found and this
document now incorporates fixes for: a real create-gate blanket-degrades-on-non-git-directories bug
(D3, high severity), a canonical-version mislabeling bug when `--sync` is invoked from a stale local
copy (§6 item 4, medium), a wrong denominator in the em-dash style claim (§3 row 7), a wrong test-count
figure for the Layer 4 precedent (52, not 26), an internally-inconsistent test-count summary, two test
rows that would have passed vacuously against unpatched code, a missing genuine end-to-end integration
test, and several citation/terminology corrections. Nothing in this second pass found a defect the
first (design-panel) pass should be faulted for missing — the two passes checked different things
(design tradeoffs vs. this specific document's own execution of the chosen design).

---

## 2. Root cause — one sentence

`check_stale_version()`'s warning has exactly one remedy (`--sync`, a portfolio-wide write — the
issue's own title states "26 files across 25 sibling repos" for the environment it was filed against;
this fork's own portfolio measured 13 targets at S57, a different number because it's a different
machine/checkout, not a correction) for a one-file problem, and neither `--sync` nor bare `--dry-run`
has ever had a way to say "write nothing without an explicit go-ahead" — so the tool's only staleness
fix is disproportionate regardless of the exact count, and its only preview flag doesn't actually
preview the common case.

---

## 3. Evidence inventory (grep-based, MANDATORY per Planning Sessions)

**Current state, re-verified at S57 HEAD** (all four functions, `tools/methodology_dashboard.py`;
`starter-kit/` twin confirmed byte-identical via `diff -q`):

| # | Site | Current behavior | Issue #67 point |
|---|------|-------------------|------------------|
| 1 | `check_stale_version()` `:764-777` | stderr recommends only `python3 {canonical} --sync` | 1 — no scoped remedy |
| 2 | `sync_dashboards()` `:989-1051` | no target scoping; always walks the whole portfolio | 2 — no self/target flag |
| 3 | `sync_dashboards()` write loop `:1037-1042` | `if action != "unchanged": ... if not dry_run: shutil.copyfile(...)` — **no gate**, tracked files get only an informational note and are written anyway; brand-new files are created unconditionally | 3 — no `--yes`/scope-and-confirm |
| 4 | `main()` `:3916-3928` | `if "--sync" in args:` is checked, and only *inside* that branch is `dry_run` ever consulted; a bare `--dry-run` falls through to the full single-project scan-and-write (`output_path.write_text(html)`, `append_history(...)`) with no gate at all | 4 — bare `--dry-run` is not a no-op |
| 5 | `print_usage()` `:1054-1066` | documents none of the above | — |
| 6 | `tools/test_methodology_dashboard.py:2048-2051` | `test_dashboard_version` hard-pins the literal string `"2.13.0"` for **both** twins | not in the issue; **every one of the three candidate designs proposed a version bump and none updated this test** — confirmed independently for this document (`grep -n '2\.13\.0' tools/test_methodology_dashboard.py`) |
| 7 | user-facing strings | scoped correctly to the actual population — the string arguments passed to `print(...)`/`sys.stderr.write(...)` calls (not the whole file, which mixes in docstrings/comments/HTML templates and returns a misleading 139): **3** use the real em-dash `—`, **7** use ASCII `--`, and every one of those 7 is CLI flag *syntax* (`--sync`, `--no-open`, etc.), **zero** stylistic-dash exceptions — verified by an AST parse over `print`/`sys.stderr.write` call arguments, not a whole-file grep | not in the issue; **every candidate's new strings used ASCII `--`** in prose — a real, checkable style regression this plan does not repeat |
| 8 | `bin/sync:247,291,302` (sibling tool, same repo) | already uses `--force` for the identical concept — "confirm overwrite of a target with local/tracked changes" | not in the issue; two of three candidates independently proposed `--yes` for the same concept without checking this precedent |

**Baseline:** `bin/tests.sh` 185 passed / 1 failed (Test 9's expected upstream 404 — pre-existing,
unrelated) at S57 HEAD. `python3 tools/methodology_dashboard.py --help` and the existing
`test_sync_does_not_target_the_authoring_repo` (`tools/test_methodology_dashboard.py:3277`) are the
only two things touching this code path with any live test coverage; `check_stale_version()` has
**zero** existing test coverage (`grep -c check_stale_version tools/test_methodology_dashboard.py` →
0 test references).

---

## 4. Design decisions

### D1 — One generalized `--sync [TARGET_DIR]`, not a second `--sync-self` flag *(proposed)*

`--sync` gains an optional, order-independent positional argument. Given, it scopes the write to
exactly `<TARGET_DIR>/methodology_dashboard.py`. Omitted, it is today's unchanged full-portfolio
sweep. Self-sync is this mechanism invoked with `target = self_path.parent` — no second flag, and no
future "sync one other specific project" request will ever need a third one either. Rejected:
MINIMAL's and LITERAL's separate `--sync-self` flag — both scored lower on completeness (6 vs. 7)
specifically because `--sync-self`'s argument-free shape either overloaded an existing parameter
(MINIMAL: `sync_dashboards()`'s `start` did double duty as both canonical-locator and literal write
target, a contract only two hand-written call sites happened to satisfy) or forced a whole second,
asymmetric write function (`sync_self()`, LITERAL) that then shipped three of its own bugs (§3 is not
where these lived, but the design record does — see workflow output) because the two write paths
diverged. Parsed by a small helper, not `argparse` (this file hand-rolls `sys.argv` scanning
throughout; introducing a second parsing paradigm for one flag is a bigger, less consistent diff than
extending the existing one):

```python
_KNOWN_FLAGS = {"--sync", "--dry-run", "--force", "--no-open", "--with-submodules", "--help", "-h"}

def _extract_sync_target(args):
    """First non-flag token in argv (any position, not only after --sync): the optional
    single-project sync scope. Order-independent -- '--sync /path' and '--sync --force /path'
    both resolve to '/path'. None => sync the whole portfolio (today's unchanged default)."""
    for a in args:
        if a not in _KNOWN_FLAGS and not a.startswith("-"):
            return a
    return None
```

**Disclosed risk, corrected from the design panel's own framing (adversarial review caught this):**
every current member of `_KNOWN_FLAGS` starts with `-`, so `not a.startswith("-")` already excludes
every existing flag regardless of `_KNOWN_FLAGS` membership — `_KNOWN_FLAGS` does no independent
filtering work today. The real, live hazard is a **future flag that itself takes a bare-word value**
(e.g. a hypothetical `--out FILE`): `FILE` would be misread as the sync target no matter how
faithfully `_KNOWN_FLAGS` is maintained, because that set only ever lists flag *names*, never "the
token that follows this flag." `argparse` would catch this structurally; the hand-rolled scanner does
not. Mitigated, not eliminated, by `test_extract_sync_target_is_order_independent` (§7) — any future
value-taking flag needs its own dedicated test at the time it's added, not just an entry in
`_KNOWN_FLAGS`.

### D2 — Rename the issue's suggested `--yes` to `--force`, matching this repo's own established verb *(proposed, a deliberate departure from the issue's literal wording)*

`bin/sync` (evidence row 8) already uses `--force` for exactly this semantic in this same repository.
The issue's own text says "`--yes`," but that is the filer's suggestion, not a requirement — and
shipping a second word for one concept inside one repo is the kind of inconsistency a maintainer
reviewing cold would flag on sight (two of three candidate judges did, independently). Named `--force`
here for internal consistency; call this out explicitly in the eventual PR description since it
diverges from the issue's own vocabulary.

### D3 — The `--force` gate covers exactly two risk classes, one of them `.gitignore`-aware *(proposed)*

A write is gated (skipped without `--force`) when the target is **(a)** already git-tracked, or
**(b)** a `"create"` action landing in a repo whose own `.gitignore` does not already cover the
filename. **(b) is `.gitignore`-aware** — `bool(git_cmd(t.parent, "check-ignore", t.name))` — because
the issue's own wording scopes the new-file risk to "a repo that does not ignore the path," and an
unconditional create-gate (which both MINIMAL and GENERAL's own first drafts had) blocks the tool's
routine new-adopter bootstrap even when the new file is already ignored and would never appear in that
adopter's `git status`. `git_cmd()` already returns exactly what's needed (`check-ignore` prints the
path and exits 0 when ignored, nothing and exits 1 when not — `git_cmd()`'s existing
strip-stdout/swallow-failure behavior turns that into a clean boolean), so no new git helper is
needed. Deliberately **not** gated: an ordinary `"update"` of an already-existing, already-untracked
target — the tool's routine self-heal case, which must keep working without `--force` or the flag
would need to accompany every routine re-sync, defeating the tool's purpose.

**Disclosed risk:** `git_cmd()` swallows all subprocess errors and returns `""` on failure, which both
the tracked-check and the ignore-check read as "false." On a host with no `git` on `PATH`, the
tracked-check fails open (looks untracked, write proceeds — same as today, not a regression) and the
ignore-check fails closed for the create branch (looks not-ignored → gated → skipped even if it really
is ignored). Net effect on a git-less host: the tool becomes more conservative, not less — an
acceptable direction to fail in, but worth naming.

**Second, more consequential disclosed risk, found by adversarial review of this plan (not by the
original design panel):** the same fail-closed behavior is reachable on a host with a perfectly
working `git`, whenever `--sync TARGET_DIR` (D1) points at a directory that **is not yet a git
repository at all** — `git check-ignore` there exits non-zero with empty stdout for the same reason as
the git-less-host case, so `ignored` reads `False` and the create-gate fires unconditionally. This is
not a rare edge case: it is reachable through **this plan's own new capability**, and it fires on
exactly the scenario D3's own rationale names as the thing to protect — a brand-new adopter project's
very first sync, before that project has been `git init`'d. **Residual risk, not fixed here** — see
§10 item 2 for the disclosure; a future iteration could distinguish "not a git repo" from "is a git
repo and genuinely not ignored" (e.g. via `git rev-parse --is-inside-work-tree`) and message the two
differently, but that is out of this plan's scope as currently sized.

### D4 — The gate is computed unconditionally, so `--dry-run` previews it honestly *(proposed — fixes a defect every candidate that combined gating with dry-run actually shipped)*

Both MINIMAL's and GENERAL's own designs computed the `gated` decision *inside* an
`if dry_run: pass / elif gated and not force: ...` branch structure, which meant a `--dry-run` preview
never showed the `[SKIPPED]` annotation — so `--sync --dry-run` would report a "would change" count
that a subsequent real run without `--force` would not actually achieve. Both judges scoring those two
candidates flagged this independently; neither candidate's own `honest_risks` list caught it. Fixed
here by computing `gated` **before** branching on `dry_run` and using the same `gated` value to decide
both the printed row and whether `shutil.copyfile` actually runs — see §5 for the exact loop. This
also means `--sync --dry-run --force` previews what a real `--force` run would do, not what a bare
dry-run would.

### D5 — Bare `--dry-run` (no `--sync`) is a hard, explained error, not a silent no-op *(proposed)*

The issue's complaint is silence — a no-op that exits 0 and prints nothing distinctive gives no
signal the flag did nothing. An explained error costs one branch more than a silent no-op and is
self-documenting. `sys.exit(2)` has no precedent anywhere in this file (`grep -c sys.exit
tools/methodology_dashboard.py` → 0 today) — that is disclosed here explicitly, not glossed over the
way GENERAL's design justified it by citing `argparse`'s convention despite this file never using
argparse. The precedent being borrowed, not native, is a real property of this decision, not a defect
in it; note it in the eventual PR so a reviewer isn't left to find it themselves.

### D6 — `sync_dashboards()`'s non-dry-run return value changes meaning; dry-run now returns `0` *(disclosed, not hidden)*

Today `sync_dashboards()` returns `changed` (files that *differ* from canonical) under both dry-run
and real runs — an honest "would-change"/"changed" count only because no gate exists yet. After this
fix, a real run returns `written` (files actually copied — differs from `changed` whenever anything is
gated), and a dry run returns `0` (nothing was written, stated plainly, rather than the old
`changed`-under-dry-run reading). **No current caller consumes this return value** — `main()` discards
it, and the sole existing test (`tools/test_methodology_dashboard.py:3277`) asserts only on printed
text — so this is safe today. Flagging it because a future or external caller reading the return value
for its old meaning would be silently affected, and this repo's own convention is to disclose exactly
this class of change rather than let it hide in a diff.

---

## 5. Implementation spec

**`check_stale_version()` (`:764-777`) — message only, no logic change:**

```python
def check_stale_version():
    self_path = Path(__file__).resolve()
    canonical = find_canonical(self_path.parent)
    if not canonical or canonical == self_path:
        return
    canon_ver = parse_version(canonical)
    if canon_ver and version_key(canon_ver) > version_key(DASHBOARD_VERSION):
        sys.stderr.write(
            f"  ⚠ methodology_dashboard.py is stale: this copy is v{DASHBOARD_VERSION}, "
            f"canonical is v{canon_ver}.\n"
            f"    Update just this copy:      python3 {canonical} --sync {self_path.parent}\n"
            f"    Update the whole portfolio: python3 {canonical} --sync   "
            f"(writes every discovered project — preview first with --dry-run)\n"
        )
```

Note `self_path.parent`, not `self_path` — `--sync` takes a *directory* target, matching
`sync_dashboards()`'s existing directory-based target resolution, and the printed command is
copy-paste-executable with no path the user has to fill in themselves.

**`sync_dashboards()` (`:989-1051`) — full rewrite of the body, same name, extended signature:**

```python
def sync_dashboards(start, dry_run=False, target=None, force=False):
    """Copy the canonical dashboard to a single TARGET_DIR (if given) or to the portfolio root +
    every discovered project (target=None, today's default). In --dry-run mode nothing is written;
    the planned actions — including which targets --force would be needed for — are printed.
    Returns the count of files ACTUALLY written (0 for a dry run; see plan D6)."""
    canonical = find_canonical(start)
    if not canonical:
        sys.stderr.write("  Cannot locate canonical methodology/starter-kit/"
                          "methodology_dashboard.py — nothing synced.\n")
        return 0
    canon_repo = canonical.parent.parent.resolve()
    portfolio_root = canonical.parent.parent.parent
    canon_text = canonical.read_text()
    canon_ver_display = parse_version(canonical) or DASHBOARD_VERSION   # see §6 item 4

    if target is not None:
        target_dir = Path(target).resolve()
        if not target_dir.is_dir():
            sys.stderr.write(f"  Target directory does not exist: {target_dir} — nothing synced.\n")
            return 0
        if target_dir == canon_repo or (target_dir / "methodology_dashboard.py") == canonical:
            sys.stderr.write("  Refusing to sync the canonical's own authoring repo as a target.\n")
            return 0
        targets = [target_dir / "methodology_dashboard.py"]
        scope_label = f"1 target ({target_dir})"
    else:
        targets = [portfolio_root / "methodology_dashboard.py"]
        for proj in discover_projects(portfolio_root):
            if proj.resolve() == canon_repo:
                continue
            targets.append(proj / "methodology_dashboard.py")
        scope_label = f"portfolio root + {len(targets) - 1} project(s)"

    print(f"Canonical: {canonical} (v{canon_ver_display})")
    print(f"{'DRY RUN — no files written.' if dry_run else 'Syncing.'} Targets: {scope_label}\n")

    written = skipped = inspected = 0
    for t in targets:
        t = t.resolve()
        if t == canonical:
            continue
        inspected += 1
        existing = t.read_text() if t.exists() else None
        if existing == canon_text:
            action = "unchanged"
        elif existing is None:
            action = "create"
        else:
            action = "update"

        tracked = bool(git_cmd(t.parent, "ls-files", "--error-unmatch", t.name))
        ignored = action == "create" and bool(git_cmd(t.parent, "check-ignore", t.name))
        gated = action != "unchanged" and (tracked or (action == "create" and not ignored))  # D3/D4

        note = ""
        if gated and not force:
            skipped += 1
            note = ("  [SKIPPED — git-tracked; pass --force, then Phase 3 untrack]" if tracked else
                    "  [SKIPPED — new, ungitignored file; pass --force to create]")
        elif action != "unchanged":
            if not dry_run:
                shutil.copyfile(canonical, t)
            written += 1
            if tracked:
                note = "  [git-tracked — needs Phase 3 untrack]"

        try:
            label = t.relative_to(portfolio_root)
        except ValueError:
            label = t
        shown = "skip" if (gated and not force) else action
        print(f"  {shown:<9s} {label}{note}")

    verb = "Would change" if dry_run else "Changed"
    tail = f" ({skipped} skipped — rerun with --force to include them)" if skipped else ""
    print(f"\n  {verb} {written} of {inspected} target(s).{tail}")
    return 0 if dry_run else written
```

**`main()` (`:3916-3928`) — dispatch, in this order:**

```python
def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print_usage()
        return

    if "--sync" in args:
        target = _extract_sync_target(args)
        sync_dashboards(Path(__file__).resolve().parent, dry_run="--dry-run" in args,
                         target=target, force="--force" in args)
        return

    if "--dry-run" in args:                                                    # D5
        sys.stderr.write(
            "  --dry-run only means something together with --sync (nothing else in this\n"
            "  tool writes speculatively).\n"
            "  Usage: python3 methodology_dashboard.py --sync [DIR] --dry-run\n"
        )
        sys.exit(2)

    check_stale_version()
    # ... rest of main() entirely unchanged from here down ...
```

Order is the whole fix for D5: `--sync` (with or without a target, with or without `--dry-run`)
returns before the new bare-`--dry-run` guard is ever reached.

**`print_usage()` (`:1054-1066`) — the `--sync`/`--dry-run` block (3 lines today) expands to 7, plus a
new 3-line `--force` block (net +7 lines, not a small edit — sized correctly here so the implementing
session isn't surprised):**

```python
print("  --sync [DIR]       Copy the canonical dashboard to DIR (a single project) if")
print("                     given, or to the portfolio root and every discovered")
print("                     project if omitted. Combine with --dry-run to preview,")
print("                     --force to also write tracked/brand-new targets.")
print("  --dry-run          With --sync, show planned changes without writing.")
print("                     Alone, it is an error (nothing else in this tool writes")
print("                     speculatively).")
print("  --force            With --sync, also write targets that are git-tracked or")
print("                     brand-new (and not already .gitignore'd). Without it,")
print("                     those targets are listed but skipped.")
```

**Mirror byte-for-byte to `starter-kit/methodology_dashboard.py`** — the same four edits, applied
identically, verified by the existing twin-identity checks (`bin/tests.sh:258`'s `diff -q`, and the
more direct Python-level `tools/test_methodology_dashboard.py`'s twin-comparison test at `:2043`).
(`bin/tests.sh:27` is a *different* check — that one verifies `bin/sync` correctly propagates the
starter-kit canonical into an already-synced adopter project, not tools/↔starter-kit twin identity —
cited only for the latter here.)

---

## 6. Required companion edits (every candidate design missed at least one of these)

1. **`tools/test_methodology_dashboard.py:2048-2051`, `test_dashboard_version`** — update both
   hard-pinned `"2.13.0"` assertions (the `tools/` value and the starter-kit-twin regex) to
   `"2.14.0"`. Without this, the version bump breaks an existing green test on the next
   `bin/tests.sh` run. **Not optional; verified present at the cited lines (evidence row 6).**
2. **Every new user-facing string uses the real em-dash `—`**, matching the file's own zero-exception
   convention within `print`/`sys.stderr.write` prose (evidence row 7) — not the ASCII `--` every one
   of the three candidates used in their new prose. Applies to printed/stderr text only, not to
   docstrings or comments (§5's `sync_dashboards()` docstring uses the em-dash too, for full
   consistency, but that's a style choice here, not a hard requirement below the CLI-output layer).
   Flag *syntax* like `--sync`/`--force`/`--dry-run` is unaffected either way — those are literal
   double-hyphens by CLI convention, not stylistic dashes.
3. **No stale "needs --force" note on a target that was just written** — the loop in §5 only attaches
   that note when `gated and not force` is true or on the tracked-but-written informational case, never
   on a successful gated write (a bug one candidate's draft had: it kept printing "needs --yes" after a
   `--force` run had already satisfied that need).
4. **Canonical's version, wherever printed, must come from `parse_version(canonical)`, never from the
   running copy's own `DASHBOARD_VERSION`.** The first draft of this plan got this wrong — its
   `sync_dashboards()` spec printed `f"Canonical: {canonical} (v{DASHBOARD_VERSION})"`, which is only
   correct when `--sync` happens to be invoked by running the canonical file directly; running a
   *local, possibly-stale* copy's `--sync` (an entirely ordinary usage pattern for a
   distributed-per-adopter tool) would label the canonical with the running copy's own, wrong version
   number. Caught by adversarial review, not by the design panel. **Fixed in §5's spec** via
   `canon_ver_display = parse_version(canonical) or DASHBOARD_VERSION`, mirroring
   `check_stale_version()`'s already-correct pattern.

---

## 7. Test plan (RED-first, Learning #12 — write against today's code, confirm failure, then implement)

Fixture idiom for the in-process tests matches the one existing precedent in this file exactly
(`test_sync_does_not_target_the_authoring_repo`, `tools/test_methodology_dashboard.py:3277-3308`):
real `tempfile.TemporaryDirectory()` + real `git init`, `md.sync_dashboards(...)` called in-process,
stdout captured via `contextlib.redirect_stdout`. Tests requiring `Path(__file__)` itself to resolve
inside a fixture (the `check_stale_version()` and bare-`--dry-run` tests, rows 1 and 13) run as a real
subprocess against a **temp-copied** source file — this file already uses subprocess-based testing for
cases `importlib`/monkeypatching can't reach (locale-sensitive decoding, trimmer invocation), but the
copy-the-script-itself step is genuinely new here, not directly precedented; it's necessary because
`check_stale_version()`'s `self_path` and `main()`'s module-level `ROOT` both derive from
`Path(__file__)`, which an in-process call against the already-imported module can't fake.

| # | Test | RED against today because |
|---|------|---------------------------|
| 1 | `test_check_stale_version_recommends_scoped_target` | message contains no scoped remedy at all |
| 2 | `test_extract_sync_target_is_order_independent` | `_extract_sync_target` doesn't exist |
| 3 | `test_sync_accepts_a_single_target_directory` (discovery skipped, only the target touched) | `sync_dashboards()` has no `target` kwarg → `TypeError` |
| 4 | `test_sync_target_writes_only_that_target` | same `TypeError` |
| 5 | `test_sync_target_nonexistent_directory_errors_without_writing` | same `TypeError`; no such guard exists |
| 6 | `test_sync_target_refuses_canonical_authoring_repo` | same `TypeError`; no such guard in scoped mode |
| 7 | `test_sync_skips_git_tracked_target_without_force` | today's code writes it unconditionally (the issue's literal point 3) |
| 8 | `test_sync_writes_git_tracked_target_with_force` — must also assert the printed note reads exactly `[git-tracked — needs Phase 3 untrack]` with **no residual "needs --force" text**, since `--force` was just satisfied | `force` kwarg doesn't exist → `TypeError` (and today there's no note-correctness behavior to even check) |
| 9 | `test_sync_skips_new_ungitignored_target_without_force` | today's code creates it unconditionally |
| 10 | `test_sync_creates_new_gitignored_target_without_force` — **control**, calls `sync_dashboards(..., target=target, force=False)` (the new keyword form, not the old 2-positional-arg style) against an already-`.gitignore`d new file, proves the gate doesn't over-fire | **must use the new `target=`/`force=` kwargs to be genuinely RED** (`TypeError` against pre-fix code) — asserting only "the file gets created" without those kwargs would pass vacuously today, since nothing gates it either way yet; pairs with #9 per this repo's own guard-narrowing-not-just-firing convention |
| 11 | `test_sync_updates_existing_untracked_target_without_force` — **control**, same `target=`/`force=` kwarg requirement as #10, proves the ordinary self-heal case still proceeds | same `TypeError`-against-old-signature reasoning as #10 — guards against an over-broad gate regressing the tool's routine use |
| 12 | `test_sync_dry_run_previews_skips_accurately` — asserts a `--dry-run` on a gated target shows `[SKIPPED]` and excludes it from the "would change" count, and that adding `--force` to the same dry run shows the real action instead | **the D4 fix** — no candidate's own test suite caught this gap; this test exists specifically because it was missing everywhere else |
| 13 | `test_bare_dry_run_without_sync_errors_and_writes_nothing` | direct reproduction of issue #67 point 4 — today's bare `--dry-run` writes `dashboard.html` + appends history, exit 0 |
| 14 | `test_sync_dry_run_with_target_still_works` — **control**, must assert the dry-run preview text is scoped to exactly the given `<dir>` (e.g. `"1 target (<dir>)"`, excluding other portfolio members) | **not "unaffected by the guard" alone — that's already true today and would pass vacuously**, violating this plan's own Learning #12 mandate; today's code also silently ignores any directory token on argv entirely (no `_extract_sync_target()` call exists in `main()`), so the scoping assertion is what's actually RED, and it's also the only assertion that would catch a real future bug where `main()` extracts the target but forgets to pass it to `sync_dashboards()` |
| 15 | `test_usage_documents_sync_target_and_force` | neither string exists in `print_usage()` today |
| 16 | `test_sync_end_to_end_via_main_writes_only_the_target` — genuine CLI-level integration test: run `--sync <dir>` (no `--dry-run`) through the real `main()`/argv path (not a direct `sync_dashboards()` call, unlike rows 3–6) against a temp fixture, assert only `<dir>/methodology_dashboard.py` was written | **closes a real coverage gap the design panel and the first draft of this table both left open**: rows 3–6 call `sync_dashboards()` directly, bypassing `main()`'s own argument threading — a slip where `main()` extracts the target correctly but forgets to pass `target=target` through would pass every other row and still ship broken |
| 17 | `test_dashboard_version` **(existing test, updated)** | asserts `"2.14.0"`; fails against the unbumped source until the bump lands — see §6.1 |

17 tests total: 16 new (13 probing new behavior directly + 3 controls: #10, #11, #14) plus 1 existing
test (#17) updated. Comparable in count to the Layer 4 precedent (`abb3b29`, issue #59's fix — **52**
new test methods, confirmed via `git show abb3b29 -- tools/test_methodology_dashboard.py | grep -c
'^\+    def test_'`, ~619 test lines) scaled down for this fix's narrower surface (four functions, no
new scoring dimension).

---

## 8. Version bump

`DASHBOARD_VERSION`: `"2.13.0"` → `"2.14.0"` (minor — every change is additive: two new flags
[`--force`, the `--sync` target argument], reworded messages, one new hard-error branch, one
return-value semantics change with no known consumer; no existing flag or default-mode behavior is
removed or renamed). Bump identically in both twins; update `test_dashboard_version` in the same
commit (§6.1) or `bin/tests.sh` fails immediately.

---

## 9. Upstream PR readiness — and the gate that still applies

This plan's stated purpose is a fix that **can be** pushed upstream once implemented — that is not the
same as authorization to push it. Per this repository's standing rule (`CLAUDE.md` §"Contributing
upstream"), **every outward-facing action needs the operator's explicit go-ahead, each time** — a
ratified plan is not that go-ahead, and no future session may treat this document as license to skip
asking before opening a PR, even after implementing and testing every item above.

When implementation is complete and the operator gives the go-ahead to proceed toward upstream:

- The PR description should be self-contained for a maintainer who has not read this fork's
  `docs/planning/` — cite issue #67 by number, state the four fixes plainly, and do not assume
  familiarity with this fork's own conventions (em-dash style, `bin/sync --force` precedent) beyond
  what's needed to justify the choices made.
- **D2 (the `--yes`→`--force` rename) is the one deliberate departure from the issue's own literal
  suggestion** and should be named as such in the PR — a maintainer who filed the issue asking for
  `--yes` may push back and prefer their own wording; that is a legitimate maintainer call, not a
  defect in this plan, and this fork should not treat push-back on this specific point as something
  to resist.
- No dependency on PR #66 — this fix is orthogonal (confirmed in `issue67-pr66-review.md`); it can be
  proposed independently regardless of PR #66's own outcome.
- BL-26 should be updated to record this plan's existence once written, and closed on its issue-#67
  thread once the fork-side implementation lands (its PR #66 thread stays open independently).

---

## 10. Residual risks — here be dragons

1. **`_KNOWN_FLAGS` is a hand-maintained set, but not for the reason first stated.** Every current flag
   is dash-prefixed, so `_KNOWN_FLAGS` membership does no independent filtering today — the real
   hazard is a *future value-taking flag* (e.g. `--out FILE`), whose bare-word value would be misread
   as a sync target regardless of `_KNOWN_FLAGS`'s contents. No structural guard against this; any
   future value-taking flag needs its own dedicated test at the time it's added (corrected during
   adversarial review — see D1).
2. **`git_cmd()`'s asymmetric failure modes, TWO distinct triggers, not one:** (a) on a genuinely
   git-less host, the tracked-check fails open (permissive, same as today) while the ignore-check
   fails closed (conservative, new) — both silent, neither raises. (b) **More consequential, found by
   adversarial review**: the ignore-check *also* fails closed whenever `--sync TARGET_DIR` (D1) points
   at a directory that simply isn't a git repository yet — a fully working host, not a git-less one —
   which blanket-gates every brand-new adopter's very first sync, exactly the scenario D3's own
   rationale names as the case to protect. Not fixed here (see D3's second disclosed-risk paragraph);
   worth a follow-up that distinguishes "no repo here" from "repo, and genuinely not ignored."
3. **The gate is scoped to exactly the two risk classes the issue names** — an already-existing,
   already-untracked, already-ignored target with local hand-edits different from canonical is still
   overwritten without `--force`, identical to today. A maintainer could reasonably ask for this to be
   gated too as a follow-up; out of scope for a fix that maps 1:1 onto the issue as filed.
4. **This plan was never executed against the real repo** — no code was written or run for it; every
   RED/pass claim in §7 is derived from reading the current source (re-verified twice: once by the
   design panel, once independently by a four-lens adversarial review of this document, both against
   the live source at S57 HEAD — not merely re-asserted). **The implementing session must still
   confirm every RED claim actually fails before trusting Learning #12 compliance**, not carry these
   citations forward as already-proven by a document, however carefully checked.
5. **Return-value semantics change** (D6) is safe today (no consumer) but silent to any future or
   external caller reading the old meaning — disclosed, not fixed, because there's nothing to fix
   without breaking the one behavior (`written`, not `changed`) that's actually correct going forward.
6. **`"--sync" in args` is exact-token membership** (pre-existing, unchanged by this plan) — an
   equals-sign style invocation (`--sync=/path`, common in other CLIs) is not recognized as `--sync` at
   all, and silently falls through to a full unscoped portfolio write instead of the intended scoped
   one. Pre-existing in today's code, not introduced here, and out of scope for this fix — named
   because it's exactly the class of argv-misparse this plan otherwise hardens against.

---

## 11. Completion criteria (for the implementing session)

- [ ] All four fixes land in both twins, byte-identical (`diff -q` passes)
- [ ] All 17 tests in §7 written RED-first, confirmed failing against pre-fix code, then passing
- [ ] `test_dashboard_version` updated in the same commit as the version bump (§6.1, §8)
- [ ] No new user-facing string uses ASCII `--` in prose (§6.2) — spot-check by re-running the AST-based
      check from evidence row 7 (extract `print`/`sys.stderr.write` call-argument strings, not a raw
      grep — a plain `grep -n '\-\-[a-z]'` false-positives on every `--sync`/`--force`/`--dry-run` flag
      token and is not a usable pass/fail check on its own)
- [ ] `bin/tests.sh` full suite green (185/185 or better; the one pre-existing Test 9 failure is
      unrelated and expected)
- [ ] `python3 tools/methodology_dashboard.py --help` output matches §5's `print_usage()` spec exactly
- [ ] CHANGELOG.md / HANDOFFS.md close-out entries filed per this repo's own protocol
- [ ] BL-26 updated: issue-#67 thread marked addressed fork-side; PR #66 thread left open
- [ ] **No PR opened against `KJ5HST/methodology` without the operator's explicit go-ahead, asked for
      again at that time** (§9)
