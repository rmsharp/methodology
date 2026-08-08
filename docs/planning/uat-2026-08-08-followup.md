# UAT follow-up — the same six adopters, four sessions later

**Date:** 2026-08-08 · **Session:** fork S48 · **Mode:** read-only · **Baseline:**
[`uat-2026-08-04-six-adopters.md`](uat-2026-08-04-six-adopters.md) (S43, 2026-08-04, tree `4dea909`)

This is fork-only. It lives in `docs/planning/` and reaches no adopter. Excludes `nprcgenekeepr` —
the operator stated it is busy/currently off-limits (recorded in `CHANGELOG.md`); it was never one
of the original six.

**Method:** seven parallel read-only agents (one per repo, one for the dashboard) reproduced S43's
own commands verbatim against the current state of `airqino`, `church_growth`,
`model_project_constructor`, `mts-system`, `vscode_quarto_ext`, `wsfct`, reporting raw command
output rather than summaries. Every number below was cross-checked against the S43 baseline by the
agent that produced it, and the load-bearing ones (F1, F6) were re-verified directly rather than
taken on trust.

---

## 1. Headline result

**F1 is fixed, and the fix now has real-corpus proof, not just unit-test proof.** S44 (2026-08-04)
patched the trimmer's grammar-mismatch blindness and unit-tested it here; that fix had never been
run against the actual malformed ledgers that exposed the bug. This session ran it:

```sh
python3 starter-kit/methodology_trim.py --file ../model_project_constructor/CHANGELOG.md --check
python3 starter-kit/methodology_trim.py --file ../wsfct/CHANGELOG.md --check
```

| Repo | Before (S43) | Now (S48) |
|---|---|---|
| `model_project_constructor/CHANGELOG.md` (597,717 B, 130 real entries) | `[NO_RECORDS]` — exit 0, identical wording to a fresh empty seed | `[GRAMMAR_MISMATCH]` — exit 3, names line 16 as the first non-conforming line |
| `wsfct/CHANGELOG.md` (1,239,085 B, 508 table rows) | `[NO_RECORDS]` — exit 0 | `[GRAMMAR_MISMATCH]` — exit 3, names line 27 |

Ledger byte sizes are unchanged in both files (confirming this is the *tool's* behavior that
changed, not the data). The fix generalizes from the synthetic fixtures it was proven against to
the two real files that motivated it.

**Everything else is exactly where S43 left it.** Ten findings (F2, F3, F4, F5, F6, F7, F8, F9, F10,
F11) were re-checked and every one reproduced its S43 value with **zero drift** — no regression, no
silent improvement, no adopter self-remediation. Every one of the six repos' `F10` reconcile-debt
counts (undocumented commits since each repo's `CHANGELOG.md` was last touched) matched S43 exactly,
repo for repo — strong evidence none of the six have had any session activity in the four sessions
since S43, consistent with the operator's current focus being elsewhere (this repo, and separately
`nprcgenekeepr`).

---

## 2. Per-finding status

| # | Dimension | S43 severity | Status this session | Evidence |
|---|---|---|---|---|
| F1 | D2 | CRITICAL | **FIXED, verified against real corpus** | §1 above |
| F2 | D1 | CRITICAL | **Unchanged, still open** | `BOOTSTRAP.md:330`'s unqualified "overlay them" instruction is byte-identical in `church_growth`, `mts-system`, `vscode_quarto_ext`; no adjacent never-overwrite rewrite in any of the three |
| F3 | D4 | CRITICAL | **Unchanged, still open** | `SESSION_NOTES.md` line counts reproduced exactly where S43 gave a figure (`model_project_constructor` 25,346; `vscode_quarto_ext` 7,468; `church_growth` 1,777/29 headings); newly measured for the other three (`airqino` 230/9, `mts-system` 542/55, `wsfct` 832/86) — no fix landed to the seed's self-contradiction or the trimmer's blind spot |
| F4 | D1 | CRITICAL | **Unchanged, still open** | `bin/sync --dry-run` still exits 2 on `model_project_constructor` and `wsfct`, same two locally-modified files each time; `BOOTSTRAP.md` still absent from both — neither can read its way out |
| F5 | D1 | MODERATE | **Unchanged** (delivery gap, not a defect) | Still frozen out of the URL path until upstream merges; `bin/tests.sh` Test 9's 404 is the same fact, still failing consistently (185/1 this session) |
| F6 | D3 | MODERATE | **Unchanged, still open — directly re-verified** | `airqino`'s `SESSION_RUNNER.md` is still **17 versions behind** (identical to S43); the dashboard's `collect_methodology_metrics()` still credits it in full — compliance **96% (19/20)**, only `HANDOFFS.md` docked. Confirmed via two independent methods (a direct per-repo Python call, and a full dashboard scan of all six) that agreed exactly |
| F7 | D4 | MODERATE | **Unchanged, still open** | `mts-system` receipt S74's `commit: 4966443` (a real, all-numeric 7-char sha) is still rejected by `check-handoff`'s `SHA_RE` — same repo, same receipt, same false positive as S43 |
| F8 | D2 | MODERATE | **Unchanged, still open** | `vscode_quarto_ext/HANDOFFS.md` still hits `[ZONE_UNCLASSIFIED]` at the same line (2771), same cause (trailing `---` + the seed's own sentinel comment) |
| F9 | D4 | MODERATE | **Unchanged, still open** | `dashboard_history.jsonl` still untracked+unignored in `airqino`, `mts-system`, `wsfct`; absent entirely in `model_project_constructor`; still tracked-and-permanently-dirty (81,865 B) in `vscode_quarto_ext`; still correctly ignored only in `church_growth`. Same open state as this repo's own F9 |
| F10 | D4 | MINOR | **Unchanged, exact match all six** | `airqino` 10, `model_project_constructor` 5, `mts-system` 1, `wsfct` 1, `church_growth` 0, `vscode_quarto_ext` 0 — every figure byte-for-byte identical to S43 |
| F11 | D4 | MINOR | **Unchanged, still open** | `airqino`, `model_project_constructor`, `wsfct` still lack `HANDOFFS.md` |
| F12 | D4 | CRITICAL (process) | N/A this session | The lesson (log a constraint's release, not just its imposition) was applied proactively at this session's own claim for `nprcgenekeepr` — see `CHANGELOG.md`, 2026-08-08 |

**Net: 1 of 11 re-checked findings improved (F1, verified against real data); 10 of 11 unchanged;
zero regressions.**

---

## 3. A discrepancy that dissolved under cross-checking, not a new finding

S43's Inventory table (§3) carries a "drifting" column alongside missing/locally-modified/
versions-behind/current. Several of this session's per-repo agents, working in isolation, flagged
that figure as unreproducible — `bin/status`'s own source (confirmed independently by multiple
agents reading `file_status()`) emits only four literal strings (`missing`, `current`, `N versions
behind`, `locally modified`); no `"drifting"` string exists anywhere in the tool, then or now.

Aggregating all six results resolves it completely: **`drifting` is simply `missing +
locally-modified + versions-behind`** — the non-current tracked rows — and it reconciles exactly,
with zero remainder, in every one of the six repos:

| Repo | missing + locally-mod + versions-behind | = drifting (baseline) | + current | = total tracked |
|---|---:|---:|---:|---:|
| `airqino` | 6+0+10 | **16** ✓ | 4 | 20 |
| `church_growth` | 2+0+9 | **11** ✓ | 9 | 20 |
| `model_project_constructor` | 7+2+11 | **20** ✓ | 0 | 20 |
| `mts-system` | 2+0+9 | **11** ✓ | 9 | 20 |
| `vscode_quarto_ext` | 2+0+9 | **11** ✓ | 9 | 20 |
| `wsfct` | 7+2+4 | **13** ✓ | 7 | 20 |

It is a derived summary column in S43's own report prose, never a `bin/status` output string — the
individual agents' confusion came from checking one repo at a time rather than the whole set. Worth
recording as a process lesson (an isolated per-item check can manufacture a false discrepancy that a
same-shape check across the full population resolves instantly), not as a framework defect.

---

## 4. Observations beyond the original 11 findings

Not new framework defects — adopter-side data points worth noting for anyone deciding whether/when
to push a sync:

- **`vscode_quarto_ext/HANDOFFS.md` carries 93 unreconciled `commit:` answer slots** (receipts S38
  through S184), spanning empty values, literal `pending`, and multi-commit prose lists
  `check-handoff` doesn't parse as a single sha. This is the checker working exactly as designed —
  it is flagging a real, large gap between this repo's own reconcile-on-read discipline and how
  deeply that discipline has actually been followed by this particular adopter.
- `church_growth`'s own `HANDOFFS.md` fails `check-handoff` for reasons distinct from F7 (unreconciled
  `pending` slots, a malformed `key_files` line) — ordinary adopter ledger hygiene gaps, not a new
  tool defect.
- The dashboard scan (six repos via a scratchpad harness, matching S43's own precedent — never run
  from inside an adopter repo): portfolio health 70/100, 3 of 6 at HIGH risk (`airqino`,
  `vscode_quarto_ext`, `model_project_constructor`), `DASHBOARD_VERSION` 2.13.0.

---

## 5. Read-only proof

Every repo's `git status --porcelain` was captured before and after its checks and matched exactly
(pre-existing dirty paths — `airqino` 2, `mts-system` 2, `vscode_quarto_ext` 3 — confirmed by file
timestamp to predate this session in every case, none bearing today's date). The dashboard agent
verified the same across all six adopters plus this repo after its scan. Nothing was written outside
the scratchpad directory used for the dashboard run.

## 6. Recommendation

Unchanged from S43: **do not touch any adopter repository.** Three still carry uncommitted or
locally-modified work (`airqino`, `mts-system`, `vscode_quarto_ext`); `model_project_constructor`
and `wsfct` are structurally blocked from syncing at all (F4) until their local `SESSION_RUNNER.md`/
`SAFEGUARDS.md` customizations are reconciled by hand. F1's verified fix does not change this — it
proves the *tool* is now safe to point at these ledgers in `--check` mode, not that a `--write` or a
`bin/sync` run against any of these six is warranted without the operator's separate go-ahead.

The priority order S43 set (§6 there) is unchanged except F1 moving from "highest severity, cheapest
fix" to done: **F3** (correct the `SESSION_NOTES.md` premise) is now the top open item; **F2/F5**
still close only by merging upstream; **F4, F6, F7, F8, F9** remain bounded, independent, small.
