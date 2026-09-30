#!/usr/bin/env python3
"""Run ONE replay session: build the arm, drive `claude -p` with the scripted stakeholder, extract a row.

    python3 driver.py ARM REP [--model sonnet] [--session-cap 2.0] [--total-cap 10.0] [--out DIR] [--max-stops N]

What it does, in order:
  1. refuses to start if (dollars already recorded in OUT/spend.jsonl) + session cap would pass the total cap;
  2. installs the arm (install_arm.install) into OUT/<arm>-r<REP>/ ;
  3. runs claude in that directory, stream-json both ways, isolated as probed in P1
     (--setting-sources "" --strict-mcp-config --disable-slash-commands), session persistence ON so the
     on-disk transcript exists for extract.py (README: "How a session is driven");
  4. at every `result` message answers with stakeholder.next_reply(n, script); stops after MAX_STOPS stops, or
     when the process ends on its own (--max-budget-usd reached counts as an end, recorded as such);
  5. appends one line to OUT/spend.jsonl and one row to OUT/rows.jsonl (extract.row on the on-disk transcript).

Permissions: headless has no one to approve a tool call, so the standard file and shell tools are pre-allowed.
That is the same tool set for every arm; the fixture has no remote, so nothing here reaches outside OUT/.
Dollar figures are the CLI's own `total_cost_usd`, i.e. list price for this session, not a bill.
"""
import argparse, glob, json, os, re, subprocess, sys, time
import extract, install_arm, real_project, real_score, replaylib, stakeholder

TOOLS = "Bash,Read,Edit,Write,Glob,Grep"


def cmd(model, session_cap, effort="xhigh"):
    return ["claude", "-p", "--model", model, "--effort", effort, "--max-budget-usd", str(session_cap),
            "--setting-sources", "", "--strict-mcp-config", "--disable-slash-commands",
            "--allowedTools", TOOLS, "--permission-mode", "acceptEdits",
            "--input-format", "stream-json", "--output-format", "stream-json", "--verbose"]


def user_msg(text):
    return json.dumps({"type": "user", "message": {"role": "user", "content": [{"type": "text", "text": text}]}}) + "\n"


def spent(out):
    p = os.path.join(out, "spend.jsonl")
    if not os.path.exists(p):
        return 0.0
    return sum(json.loads(l)["cost_usd"] for l in open(p) if l.strip())


def transcript_path(session_id):
    hits = glob.glob(os.path.expanduser(f"~/.claude/projects/*/{session_id}.jsonl"))
    return hits[0] if hits else None


def closeout_done(cwd):
    """True when the newest receipt in HANDOFFS.md reads `status: complete` and no tracked file is uncommitted."""
    try:
        text = open(os.path.join(cwd, "HANDOFFS.md")).read()
    except OSError:
        return False
    blocks = re.findall(r"```handoff\n(.*?)```", text, re.S)
    if not blocks or not re.search(r"^status:\s*complete\s*$", blocks[0], re.M):
        return False
    dirty = subprocess.run(["git", "-C", cwd, "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True).stdout
    return dirty.strip() == ""


def drive(argv, cwd, max_stops, popen=subprocess.Popen, timeout=3600, script=None, done=None):
    """Run the process; return dict(session_id, cost_usd, stops, replies, end, init, log). Testable with a fake argv."""
    p = popen(argv, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    log, replies, stops, cost, sid, init, end = [], [], 0, 0.0, None, None, "process exited"
    t0 = time.time()

    def send(n):
        msg, scripted = stakeholder.next_reply(n, script)
        replies.append({"n": n, "scripted": scripted, "text": msg})
        p.stdin.write(user_msg(msg))
        p.stdin.flush()

    send(0)
    for line in p.stdout:
        log.append(line)
        try:
            m = json.loads(line)
        except ValueError:
            continue
        if m.get("type") == "system" and m.get("subtype") == "init":
            sid, init = m.get("session_id"), {k: m.get(k) for k in ("model", "mcp_servers", "skills", "slash_commands", "tools")}
        if m.get("type") == "result":
            cost = m.get("total_cost_usd", cost)
            sid = m.get("session_id", sid)
            if m.get("is_error") or str(m.get("subtype", "")).startswith("error"):
                end = f"result {m.get('subtype')}"
                break
            stops += 1
            if stops >= max_stops:
                end = f"cut off after {max_stops} stops"
                break
            if done and stops >= len(script or stakeholder.SCRIPT) and done(cwd):
                end = "close-out complete"
                break
            send(stops)
        if time.time() - t0 > timeout:
            end = f"timeout {timeout}s"
            break
    try:
        p.stdin.close()
    except OSError:
        pass
    try:
        p.wait(timeout=30)
    except subprocess.TimeoutExpired:
        p.kill()
    return {"session_id": sid, "cost_usd": cost, "stops": stops, "replies": replies, "end": end, "init": init, "log": log}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("arm"); ap.add_argument("rep", type=int)
    ap.add_argument("--model", default="sonnet"); ap.add_argument("--effort", default="xhigh"); ap.add_argument("--session-cap", type=float, default=2.0)
    ap.add_argument("--total-cap", type=float, default=10.0); ap.add_argument("--out", default="/tmp/overhead-pilot")
    ap.add_argument("--project", default="fixture", choices=["fixture", "real"]); ap.add_argument("--max-stops", type=int, default=stakeholder.MAX_STOPS)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    before = spent(a.out)
    if before + a.session_cap > a.total_cap:
        raise SystemExit(f"refused: spent ${before:.2f} + session cap ${a.session_cap:.2f} > total cap ${a.total_cap:.2f}")
    dest = os.path.join(a.out, f"{a.arm}-r{a.rep}")
    info = real_project.install(a.arm, dest) if a.project == "real" else install_arm.install(a.arm, dest)
    res = drive(cmd(a.model, a.session_cap, a.effort), dest, a.max_stops,
                script=stakeholder.REAL_SCRIPT if a.project == "real" else None,
                done=closeout_done if a.project == "real" else None)
    with open(os.path.join(a.out, "spend.jsonl"), "a") as f:
        f.write(json.dumps({"arm": a.arm, "rep": a.rep, "cost_usd": res["cost_usd"]}) + "\n")
    with open(dest + ".stream.jsonl", "w") as f:
        f.writelines(res["log"])
    tp = transcript_path(res["session_id"]) if res["session_id"] else None
    if tp and a.project == "real":
        r = extract.row(tp, arm=a.arm, rep=a.rep)
        r["real"] = real_score.score(replaylib.events(replaylib.load_records(tp)), dest, info["base"])
        r["project"] = "nprcgenekeepr@" + info["start_commit"][:9]
    else:
        r = extract.row(tp, dest, info["base"], info["ghost"], a.arm, a.rep) if tp else None
    if r is not None:
        r.update({"cost_usd": res["cost_usd"], "stops": res["stops"], "end": res["end"], "transcript": tp,
                  "model_requested": a.model, "effort": a.effort, "init": res["init"],
                  "unscripted_replies": sum(1 for x in res["replies"] if not x["scripted"])})
        with open(os.path.join(a.out, "rows.jsonl"), "a") as f:
            f.write(json.dumps(r) + "\n")
    print(json.dumps(r or {"error": "no transcript on disk", "session_id": res["session_id"], "end": res["end"],
                           "cost_usd": res["cost_usd"]}, indent=1))


if __name__ == "__main__":
    main()
