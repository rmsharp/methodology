#!/usr/bin/env python3
"""PROTOTYPE Stop / SessionStart hook for docs/planning/close-out-report-actuator-plan.md (S252).
Fail-quiet by construction: any internal error exits 0 with no output, never 2."""
import json, sys, os, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import closeout_proto as C

def decide(payload):
    ev, cwd, sid = payload.get("hook_event_name"), payload["cwd"], payload["session_id"]
    gitdir = C.git("rev-parse", "--absolute-git-dir", cwd=cwd)
    base, stamp = f"{gitdir}/co-baseline-{sid}", f"{gitdir}/co-stamp-{sid}"
    ledger = cwd + "/HANDOFFS.md"
    r = C.receipts(ledger)[0]
    if ev == "SessionStart":                      # first sight of this session_id only; resume/compact never overwrite
        if not os.path.exists(base):
            json.dump({"id": r["session"], "status": r["status"]}, open(base, "w"))
        return None
    b = json.load(open(base)) if os.path.exists(base) else None
    owed = bool(b) and r.get("status") == "complete" and (r["session"] != b["id"] or b["status"] != "complete")
    if not owed:
        return None                               # no baseline, or no close-out happened in this session
    m = C.mech(ledger, cwd)
    state = [m["head"], C.git("rev-list", "--count", "@{upstream}..HEAD", cwd=cwd) or "0",
             hashlib.sha256(json.dumps(r, sort_keys=True).encode()).hexdigest()[:12]]
    errs = C.lint(payload.get("last_assistant_message", ""), m)
    if not errs:
        json.dump(state, open(stamp, "w"))        # a valid report, issued at this state
        return None
    if payload.get("stop_hook_active"):
        return None                               # the harness allows ONE forced retry per Stop chain
    if os.path.exists(stamp) and json.load(open(stamp)) == state:
        return None                               # report already issued and nothing has changed since
    return {"decision": "block", "reason":
        "Close-out is complete but your final message is not the Phase 3G report (" + "; ".join(errs[:3]) + "). "
        "Run: python3 " + HERE + "/closeout_proto.py --ledger HANDOFFS.md --deliverable '...' --outcome done|partial|none "
        "--well '...' --badly '...' --predecessor '...' --next '...' (each text at most 300 characters, no '|') "
        "and print its output verbatim as your entire final message, with nothing before or after it."}

if __name__ == "__main__":
    try:
        out = decide(json.load(sys.stdin))
    except Exception:
        out = None
    if out:
        print(json.dumps(out))
    sys.exit(0)
