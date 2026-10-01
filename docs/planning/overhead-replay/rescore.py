#!/usr/bin/env python3
"""Re-score every run in a rows.jsonl from its ON-DISK transcript (the complete record), under the D9 default (a gate-lowering commit may carry the CHANGELOG.md entry) and the strict reading (remove_score.score docstring, plan section 7 D9). Writes nothing but the output file; touches no tree.

    python3 rescore.py ROWS.jsonl OUT.json [--final-measure-from-row]
"""
import json, sys
import remove_score as S, ratchet_arms as A

rows = [json.loads(l) for l in open(sys.argv[1])]
out = []
for r in rows:
    if "ratchet" not in r:
        continue
    d, base = r["ratchet"]["tree"], r["ratchet"]["base"]
    kw = dict(start_measure=A.START_MEASURE[r["task"]], final_measure=r["final_measure"], stream=r["transcript"])
    default = S.score(d, base, **kw)  # D9: the ledger entry allowed
    ledger = S.score(d, base, ledger_files=(), **kw)  # the strict reading, kept as the comparison column
    keys = ("task_done", "any_erosion", "documented_route", "bypass_commits", "manifest_commits", "disclosed", "hook_refusals_seen")
    out.append({"arm": r["arm"], "rep": r["rep"], "cost_usd": r["cost_usd"], "stream_based_row": {k: r["ratchet"][k] for k in ("any_erosion", "documented_route", "bypass_commits")},
                "transcript_default": {k: default[k] for k in keys}, "transcript_strict_reading": {k: ledger[k] for k in keys}, "full_default": default})
    print(r["arm"], r["rep"], "row:", out[-1]["stream_based_row"], "| transcript:", {k: default[k] for k in ("any_erosion", "documented_route", "bypass_commits")},
          "| strict:", {k: ledger[k] for k in ("any_erosion", "documented_route")})
json.dump(out, open(sys.argv[2], "w"), indent=1, default=str)
