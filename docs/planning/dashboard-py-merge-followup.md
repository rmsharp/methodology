# Dashboard: Restore Python Coverage Detection and Vitest Fix Lost in v2.2 Merge

**Status:** **CLOSED 2026-04-25** — investigated and resolved without code changes to the dashboard. Regression test added to pin the post-merge structure.
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

---

## Resolution (2026-04-25)

Investigation found that **upstream's `c624eeb` rewrite already addresses both follow-up items by construction**, so no code change to `tools/methodology_dashboard.py` (or its `starter-kit/` twin) was needed. Resolution was a regression test instead.

### Item 1 — Python coverage in `package.json`: deliberately removed by upstream

`c624eeb`'s commit message: *"drops pytest-cov from JS package.json check, replaces ambiguous 'coverage' with specific packages."* This was an intentional design choice, not an oversight. Putting `pytest-cov` in `package.json` devDependencies is a category error; the npm `coverage` package is obscure enough that detecting it added more noise than signal.

Python coverage is still detected by the function via the non-`package.json` paths that already exist:

- `requirements.txt` (pytest-cov line scan, `tools/methodology_dashboard.py:660-668`)
- `pyproject.toml`, `.coveragerc`, `setup.cfg`, `pytest.ini` (`tools/methodology_dashboard.py:609`)

**Decision: do not re-add the `package.json` Python detection.** The fork's original heuristic (added in `f58f63b`) was upstream's removal target, not an accidental loss.

### Item 2 — Vitest double-counting: present by construction

The current upstream code at `tools/methodology_dashboard.py:639-652` is structurally equivalent to origin's `711a002` fix:

```python
for pkg_name in ("c8", "@vitest/coverage-v8", "@vitest/coverage-istanbul"):
    if pkg_name in dev_deps:
        found.append(pkg_name)
# Fallback: detect unknown @vitest/coverage-* variants
if not any(f.startswith("@vitest/coverage") for f in found):
    if any(k.startswith("@vitest/coverage") for k in dev_deps):
        found.append("vitest-coverage")
```

The fallback's gating condition (`if not any(f.startswith("@vitest/coverage") for f in found)`) makes double-counting impossible. Upstream's `c624eeb` and origin's `711a002` converged on the same shape.

**Decision: no code change.** The regression cannot recur unless the function is rewritten.

### Item 3 — Regression test added

`bin/test_dashboard.py` (new): 17-case Python `unittest` covering `collect_coverage_config()`. Pins the no-double-count invariant (`@vitest/coverage-v8` produces one tag, not two), the unknown-variant fallback, the explicit removal of `pytest-cov` from `package.json` detection, and the other detection paths (jest/nyc top-level, c8, requirements.txt, vite.config.* content sniffing, `.coveragerc`/`setup.cfg`/`pyproject.toml`/`pytest.ini`, recursive scan).

`bin/tests.sh` (modified): two new tests appended — Test 10 enforces lockstep between `tools/methodology_dashboard.py` and `starter-kit/methodology_dashboard.py` (the dashboard pair had no automated drift check), Test 11 invokes the Python regression suite. Total: 30/30 passing.

`.gitignore` (modified): added `__pycache__/` (the new test imports the dashboard module, which produces compiled bytecode).

### Outstanding

The local `chore/dashboard-py-merge-followup` branch and its remote counterpart are no longer needed for re-integration but are preserved for now — deletion is a destructive op left to the user's discretion. The branch points at `b91ac8c` and remains recoverable via reflog if accidentally pruned.
