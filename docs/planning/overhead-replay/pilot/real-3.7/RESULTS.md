# Real-project runs: v3.7 against v3.0 (S237)

Start state: `nprcgenekeepr` at `879503cce` (the parent of the real fix `54b87c1da`), one methodology version laid over the project's own files, no remote, nothing after that commit reachable. Task: issue #121 (7 unasserted test warnings), named at the go-ahead. Model `claude-sonnet-5-5`, effort xhigh, opening message "go". Five valid runs per version; every figure below is re-derivable from `rows.jsonl` and the transcripts beside it.

| | v3.7 (n=5) | v3.0 (n=5) | gap |
|---|---|---|---|
| Cost (list price) | $3.20 ($3.00-3.41) | $2.69 ($2.27-3.01) | +19%, p about 0.02 |
| Requests | 70 | 60 | +17% |
| Tool calls | 96 | 85 | +13% |
| Output tokens | 75k | 67k | +11% |
| Process bytes added | 21.4 KB | 17.7 KB | +21% |
| Commits | 5.6 | 3.4 | +65% |
| Wall time | 12.9 min | 10.4 min | not distinguishable |

(p-values: Welch t, small n, uncorrected.) **Correctness** (`held_out.py`, the real fix's tests, never visible to a session): 9 of 9 source-fixing valid runs pass with 0 failures and 0 warnings; 3.0 rep 4 repaired test fixtures only and leaves the `-Inf` behaviour (4 real-test failures, 5 pyramid warnings). Excluded from cost statistics: v3.7 rep 5 closed out as partial at the RED gate. Each run's own tests fail on the original source (3-8 failures), so they can see the bug. **Process-rigor indicators** (`rigor_score.py`) are at ceiling in both versions and do not separate them.

## What this does not show
- **The quality ratchet.** `quality_ratchet.py` was merged upstream on 2026-09-16 (PR #82) and is in no release tag; v3.0 and v3.7 do not contain it, and no transcript mentions a gate. The arm called HEAD does ship it, with an empty manifest and no hook set-up applied by `real_project.py`. **Correction, S238:** upstream tagged v3.8 on 2026-09-30 and that tag contains the ratchet (`git ls-tree -r --name-only v3.8`), so "in no release tag" holds for v3.0 and v3.7 only; the arm to test is v3.8, not main (see [`../../../ratchet-mechanism-test-plan.md`](../../../ratchet-mechanism-test-plan.md)).
- **Benefits that accumulate over sessions** (handoff loop, ledger, drift): one session per run cannot show them.
- **Other tasks, other projects, other models.** One task at one commit.

## Losses and the decisions behind them
About $10.70 of the $44.55 spent was wasted on driver defects, each recorded in `CHANGELOG.md`: a close-out check that read the format template as a receipt ($6.45 of unrequested work), a stop limit that ended a run mid-verification ($1.94), and a close-out commit whose subject the check did not recognise ($2.30). Neutral replies are paced 90 s; a run ends at a structural close-out or 14 stops.
