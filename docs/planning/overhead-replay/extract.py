#!/usr/bin/env python3
"""Turn one session transcript into one row: O2-O6 and B1 (plan section 2).

    python3 extract.py TRANSCRIPT.jsonl [--fixture DIR --base SHA --ghost SHA] [--arm A --rep N]

Without --fixture the tree-dependent fields (O4, acceptance, B1) are null: an existing transcript
from any project still yields O2, O3, O5 and O6.
"""
import argparse, json, os, subprocess, sys
import replaylib as L
import scorers, stakeholder, acceptance_test

SOURCE = {"textkit.py", "tests/test_textkit.py"}


def process_bytes(fixture, base):
    """O4: bytes of files that are not source or tests, added or changed since BASE (final size minus base size)."""
    def sh(*a):
        return subprocess.run(["git", "-C", fixture, *a], capture_output=True, text=True).stdout.split("\n")
    changed = set(filter(None, sh("diff", "--name-only", base) + sh("ls-files", "-o", "--exclude-standard")))
    total = 0
    for p in changed:
        if p in SOURCE or not os.path.exists(os.path.join(fixture, p)):
            continue
        old = subprocess.run(["git", "-C", fixture, "cat-file", "-s", f"{base}:{p}"], capture_output=True, text=True)
        total += os.path.getsize(os.path.join(fixture, p)) - (int(old.stdout) if old.returncode == 0 else 0)
    return total


def row(path, fixture=None, base=None, ghost=None, arm=None, rep=None):
    recs = L.load_records(path)
    ev = L.events(recs)
    u = L.usage_total(recs)
    stamps = [e["ts"] for e in ev if e["ts"]]
    first_edit = next((i for i, e in enumerate(ev) if L.is_source_edit(e)), None)
    humans = sum(1 for e in ev if e["kind"] == "human")
    reqs_before_edit = None
    if first_edit is not None:  # O2: tool calls issued before the first source edit (a proxy for turns of process)
        reqs_before_edit = sum(1 for e in ev[:first_edit] if e["kind"] == "tool_use")
    out = {
        "arm": arm, "rep": rep, "model": u["model"], "date": stamps[0].date().isoformat() if stamps else None,
        "O2_tool_calls_before_first_edit": reqs_before_edit,
        "O3_requests": u["requests"], "O3_tool_calls": sum(1 for e in ev if e["kind"] == "tool_use"),
        "O3_input": u["input"], "O3_output": u["output"], "O3_cache_read": u["cache_read"], "O3_cache_write": u["cache_write"],
        "O5_wall_seconds": round((max(stamps) - min(stamps)).total_seconds(), 1) if stamps else None,
        "O6_human_turns_after_opening": max(0, humans - 1),
        "O6_unscripted_stops": stakeholder.unscripted_stops(max(0, humans - 1) + 1) if humans else 0,
        "O4_process_bytes": None, "acceptance_pass": None, "B1": None,
    }
    if fixture:
        out["O4_process_bytes"] = process_bytes(fixture, base)
        out["acceptance_pass"] = acceptance_test.run(fixture)
        out["B1"] = scorers.score(ev, fixture, base, ghost)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("transcript"); ap.add_argument("--fixture"); ap.add_argument("--base"); ap.add_argument("--ghost")
    ap.add_argument("--arm"); ap.add_argument("--rep", type=int)
    a = ap.parse_args()
    print(json.dumps(row(a.transcript, a.fixture, a.base, a.ghost, a.arm, a.rep)))
