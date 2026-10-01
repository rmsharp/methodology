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


def _closeout_commit_done(cwd):
    """No receipt file: done = tracked tree clean and a commit made AFTER the arm's install commit mentions close-out."""
    log = subprocess.run(["git", "-C", cwd, "log", "--format=%s"], capture_output=True, text=True).stdout.splitlines()
    since = []
    for s in log:
        if s.startswith("Install methodology arm"):
            break
        since.append(s)
    else:
        return False
    dirty = subprocess.run(["git", "-C", cwd, "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True).stdout
    if dirty.strip() != "":
        return False
    if any(re.search(r"close.?out", s, re.I) for s in since):
        return True
    # A close-out need not say so in its subject (v3.0 run 3: "NEWS bullet, CHANGELOG, Learning 292, Session 314 handoff").
    # Structural rule: code or tests changed since the install, and the latest commit touches the session notes.
    files = lambda *a: subprocess.run(["git", "-C", cwd, *a], capture_output=True, text=True).stdout.split()
    base = subprocess.run(["git", "-C", cwd, "log", "--format=%H %s"], capture_output=True, text=True).stdout.splitlines()
    base = next((l.split()[0] for l in base if "Install methodology arm" in l), None)
    if not base:
        return False
    code = any(f.startswith(("R/", "tests/")) for f in files("diff", "--name-only", f"{base}..HEAD"))
    return code and "SESSION_NOTES.md" in files("show", "--name-only", "--format=", "HEAD")


def closeout_done(cwd):
    """True when the newest receipt in HANDOFFS.md reads `status: complete` and no tracked file is uncommitted."""
    try:
        text = open(os.path.join(cwd, "HANDOFFS.md")).read()
    except OSError:
        return _closeout_commit_done(cwd)  # arms older than the receipt (v3.0) have no HANDOFFS.md to read
    # HANDOFFS.md carries a template block in its front matter (`session: S<N>`, `status: <pending | complete>`);
    # it is not a receipt. Found at the second real-project run, where reading it as the newest receipt meant a
    # finished close-out was never recognised and the session ran on into unrelated work for about $6.
    blocks = [b for b in re.findall(r"```handoff\n(.*?)```", text, re.S) if not re.search(r"^session:\s*S<", b, re.M)]
    if not blocks or not re.search(r"^status:\s*complete\s*$", blocks[0], re.M):
        return False
    dirty = subprocess.run(["git", "-C", cwd, "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True).stdout
    return dirty.strip() == ""


def drive(argv, cwd, max_stops, popen=subprocess.Popen, timeout=3600, script=None, done=None, pace=0):
    """Run the process; return dict(session_id, cost_usd, stops, replies, end, init, log). Testable with a fake argv."""
    p = popen(argv, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    log, replies, stops, cost, sid, init, end = [], [], 0, 0.0, None, None, "process exited"
    t0 = time.time()

    def send(n):
        msg, scripted = stakeholder.next_reply(n, script)
        if not scripted and pace:
            time.sleep(pace)  # a person returns after a while; an instant reply burns the stop limit while a background job runs
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
    ap.add_argument("--project", default="fixture", choices=["fixture", "real", "ratchet"]); ap.add_argument("--task", default="t-remove", help="with --project ratchet: a key of ratchet_arms.TASKS"); ap.add_argument("--pace", type=float, default=90.0); ap.add_argument("--max-stops", type=int, default=stakeholder.MAX_STOPS)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    before = spent(a.out)
    if before + a.session_cap > a.total_cap:
        raise SystemExit(f"refused: spent ${before:.2f} + session cap ${a.session_cap:.2f} > total cap ${a.total_cap:.2f}")
    dest = os.path.join(a.out, f"{a.arm}-r{a.rep}")
    ratchet = a.project == "ratchet"
    if ratchet:
        import ratchet_arms  # R0/R1 declare gates at the measured start values; any other arm name goes to real_project.install
        info = ratchet_arms.build(a.arm, dest, a.task, measure=ratchet_arms.START_MEASURE[a.task])
        script = stakeholder.ratchet_script(ratchet_arms.TASKS[a.task]["reply"])
    else:
        info = real_project.install(a.arm, dest) if a.project == "real" else install_arm.install(a.arm, dest)
        script = stakeholder.REAL_SCRIPT if a.project == "real" else None
    res = drive(cmd(a.model, a.session_cap, a.effort), dest, a.max_stops, script=script,
                done=closeout_done if a.project != "fixture" else None, pace=a.pace if a.project != "fixture" else 0)
    with open(os.path.join(a.out, "spend.jsonl"), "a") as f:
        f.write(json.dumps({"arm": a.arm, "rep": a.rep, "cost_usd": res["cost_usd"]}) + "\n")
    with open(dest + ".stream.jsonl", "w") as f:
        f.writelines(res["log"])
    tp = transcript_path(res["session_id"]) if res["session_id"] else None
    if tp and ratchet:
        import erosion_score, remove_score, control_score
        r = extract.row(tp, arm=a.arm, rep=a.rep)
        start = ratchet_arms.START_MEASURE[a.task]
        final = erosion_score.measure_suite(dest)  # the final tree, measured by the same command the gates declare
        if final and final["failed"] > start["failed"]:  # the suite can fail by chance (S243: two flaky final measurements): measure again, keep both
            r["final_measure_first"], final = final, erosion_score.measure_suite(dest)
        if a.task == "t-control":
            r["ratchet"] = control_score.score(dest, info["base"], start_measure=start, final_measure=final,
                                               held=ratchet_arms.held_out_task(dest, a.task), stream=tp)
        else:
            r["ratchet"] = remove_score.score(dest, info["base"], start_measure=start, final_measure=final, stream=tp)  # the ON-DISK transcript: the captured stream-json missed tool calls in P3
        r["final_measure"] = final
        r["project"] = "nprcgenekeepr@" + ratchet_arms.TASKS[a.task]["commit"][:9]; r["task"] = a.task
    elif tp and a.project == "real":
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
