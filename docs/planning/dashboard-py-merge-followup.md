# Dashboard: Restore Python Coverage Detection and Vitest Fix Lost in v2.2 Merge

**Status:** Open — to be addressed in a follow-up session.
**Created:** 2026-04-25 during the upstream v2.2 merge (commit `af1e062`).

## Context

Merging upstream KJ5HST v2.2 (`af1e062`) into `rmsharp/main` took upstream's rewrite of `tools/methodology_dashboard.py`'s coverage detection logic. The rewrite did not include two improvements that existed only on the fork:

1. **Python coverage detection** — `pytest-cov` and `coverage` package detection in `package.json` devDependencies. Upstream's rewrite is JS-only (`c8`, `@vitest/coverage-v8`, `@vitest/coverage-istanbul`, plus a fallback for unknown `@vitest/coverage-*` variants).

2. **Vitest double-counting fix** — origin commit `711a002` ("fix: vitest double-counting and sync LOC fix to starter-kit"). Upstream merged origin's earlier `fd3f1da` as PR #5 but did not pick up the subsequent double-counting fix.

## Where the pre-merge state lives

Branch [`chore/dashboard-py-merge-followup`](https://github.com/rmsharp/methodology/tree/chore/dashboard-py-merge-followup) points at `b91ac8c` (pre-merge `main`). Origin's full version of `tools/methodology_dashboard.py` is recoverable as:

```
git show chore/dashboard-py-merge-followup:tools/methodology_dashboard.py
```

The conflicted blocks are around lines 323-326 (commented-out leftover, trivially deletable), 635-639 (comment text), and 645-671 (the substantive coverage-detection logic divergence).

## Proposed resolution

A small follow-up PR that:

1. Adds Python coverage detection back as a separate trailing block alongside upstream's JS-side enumeration. *(Caveat: Python coverage tools rarely live in `package.json` — verify the use case is real before re-adding. If pytest is detected separately by the dashboard's other heuristics, this re-addition may be unnecessary.)*
2. Inspects whether upstream's rewrite already addresses the vitest double-counting fix implicitly (the explicit enumeration of `@vitest/coverage-v8` and `@vitest/coverage-istanbul` may have made double-counting impossible by construction). If not, re-apply the specific change from `711a002`.
3. Adds a regression test if one doesn't already exist.

## Acceptance

- `pytest-cov` / `coverage` packages in `devDependencies` are detected (subject to the caveat above)
- No double-counting of vitest coverage entries in dashboard output
- Existing JS detection (c8, vitest-v8, vitest-istanbul, unknown vitest variants) continues to work
- The follow-up PR can close this planning doc and delete the `chore/dashboard-py-merge-followup` branch
