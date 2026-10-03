#!/usr/bin/env python3
"""PROTOTYPE for docs/planning/close-out-report-actuator-plan.md (S252). Not a shipped tool.
One definition of the Phase 3G report shape, used both to render it and to lint it.
See EVIDENCE.md for what was run against it."""
import re, sys, json, subprocess, argparse

HEAD_RE   = re.compile(r"^## Close-out report: (S\S+) · (\d{4}-\d{2}-\d{2})$")
LABELS    = ("Deliverable", "Record", "Self-assessment", "Predecessor handoff", "Next session")
CLOSING   = "Session over."
FIELD_MAX = 300          # judgment fields: one short paragraph each
TOTAL_MAX = 2000         # bytes; keeps the report on one screen

def receipts(path):
    s = open(path).read()
    out = []
    for m in re.finditer(r"^```handoff\n(.*?)^```$", s, re.S | re.M):
        d = {}
        for line in m.group(1).splitlines():
            k = re.match(r"^([a-z_]+):\s*(.*)$", line)
            if k: d[k.group(1)] = k.group(2)
        out.append(d)
    return out

def git(*a, cwd=None):
    return subprocess.run(["git", *a], capture_output=True, text=True, cwd=cwd).stdout.strip()

def mech(ledger, cwd):
    r = receipts(ledger)
    new, prev = r[0], (r[1] if len(r) > 1 else {})
    gate = re.search(r"quality_ratchet:\s*([^;\n]*?pass[^;\n]*?unmeasured)", new.get("runtime_smoke", ""))
    return dict(session=new["session"], date=new["date"], status=new.get("status"),
                self=new.get("self_score", ""), pred=new.get("predecessor_score", ""),
                pred_id=prev.get("session", "?"), head=git("rev-parse", "--short", "HEAD", cwd=cwd),
                gate=(gate.group(1) if gate else "not cited"),
                dirty=len([l for l in git("status", "--porcelain", cwd=cwd).splitlines() if l]))

def render(m, a):
    L = [f"## Close-out report: {m['session']} · {m['date']}", "",
         f"**Deliverable:** {a.deliverable} — {a.outcome.upper()}", "",
         f"**Record:** HEAD `{m['head']}` · {m['dirty']} uncommitted · gate run: {m['gate']}", "",
         f"**Self-assessment:** {m['self']}/10 — went well: {a.well}; did not: {a.badly}", "",
         f"**Predecessor handoff ({m['pred_id']}):** {m['pred']}/10 — {a.predecessor}", "",
         f"**Next session:** {a.next}", "", CLOSING]
    return "\n".join(L) + "\n"

def lint(text, m):
    errs, lines = [], text.rstrip("\n").split("\n")
    first = next((l for l in lines if l.strip()), "")
    h = HEAD_RE.match(first)
    if not h: errs.append("R1 first line is not the report heading")
    elif (h.group(1), h.group(2)) != (m["session"], m["date"]): errs.append("R1b heading names a different session/date than the newest receipt")
    pos = -1
    for lab in LABELS:
        i = next((n for n, l in enumerate(lines) if re.match(rf"^\*\*{re.escape(lab)}[^*]*:\*\*", l)), None)
        if i is None: errs.append(f"R2 missing label: {lab}")
        elif i < pos: errs.append(f"R2 label out of order: {lab}")
        else: pos = i
    if [l for l in lines if l.strip()][-1:] != [CLOSING]: errs.append("R3 last non-blank line is not 'Session over.'")
    if f"{m['self']}/10" not in text or f"{m['pred']}/10" not in text: errs.append("R4 scores differ from the receipt")
    if f"`{m['head']}`" not in text: errs.append("R5 HEAD sha is stale or absent")
    if "|" in text: errs.append("R6 table/pipe characters do not wrap in a terminal")
    if len(text.encode()) > TOTAL_MAX: errs.append(f"R7 {len(text.encode())} B exceeds {TOTAL_MAX} B")
    return errs

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", default="HANDOFFS.md"); ap.add_argument("--cwd", default=".")
    ap.add_argument("--check"); 
    for f in ("deliverable", "outcome", "well", "badly", "predecessor", "next"): ap.add_argument("--" + f)
    a = ap.parse_args(); m = mech(a.ledger, a.cwd)
    if a.check:
        e = lint(open(a.check).read(), m); print("\n".join(e) or "OK"); sys.exit(1 if e else 0)
    for f in ("deliverable", "outcome", "well", "badly", "predecessor", "next"):
        v = getattr(a, f)
        if not v: sys.exit(f"refused: --{f} is required")
        if len(v) > FIELD_MAX: sys.exit(f"refused: --{f} is {len(v)} chars; max {FIELD_MAX}")
    sys.stdout.write(render(m, a))
