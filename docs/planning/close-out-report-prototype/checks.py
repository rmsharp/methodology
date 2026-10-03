#!/usr/bin/env python3
"""All the runnable checks for the S252 plan. Run: python3 checks.py   (exit 0 = every row passes and every mutant is caught)
  1. hook decision table, driven with the payload shape measured from the real harness (claude 2.1.288)
  2. lint mutants: 10 corruptions of a good report, each must be refused
  3. hook mutants: 6 single-defect copies of hook_proto.py, each must turn the table red"""
import json, os, subprocess, sys, tempfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import closeout_proto as C

def sh(*a, cwd): return subprocess.run(a, cwd=cwd, capture_output=True, text=True, check=True).stdout
LEDGER = lambda s2: f"""# Handoffs

```handoff
session: S2
date: 2026-10-03
status: {s2}
{"self_score: 8" if s2 == "complete" else ""}
{"predecessor_score: 7" if s2 == "complete" else ""}
active_task: demo
```

```handoff
session: S1
date: 2026-10-02
status: complete
self_score: 7
predecessor_score: 8
active_task: x
what_was_done: x
next_steps: x
key_files: x:1
gotchas: x
runtime_smoke: n/a; quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured
changelog_ref: x
commit: abc1234
```
"""
def fire(repo, sid, ev, msg="", active=False):
    p = {"session_id": sid, "transcript_path": "/x", "cwd": repo, "hook_event_name": ev}
    if ev == "SessionStart": p["source"] = "startup"
    else: p.update({"prompt_id": "p", "permission_mode": "default", "stop_hook_active": active,
                    "last_assistant_message": msg, "background_tasks": [], "session_crons": []})
    r = subprocess.run([sys.executable, os.path.join(HERE, "hook_proto.py")], input=json.dumps(p), capture_output=True, text=True)
    return r.returncode, ("BLOCK" if '"block"' in r.stdout else "allow")

def report(repo):
    m = C.mech(repo + "/HANDOFFS.md", repo)
    class A: deliverable="demo"; outcome="done"; well="a"; badly="b"; predecessor="c"; next="d"
    return C.render(m, A)

rows, bad = [], 0
def case(name, got, want):
    global bad; ok = got == want; bad += 0 if ok else 1
    rows.append(f"{'PASS' if ok else 'FAIL'}  {name:70s} exit={got[0]} {got[1]:5s} (want {want[1]})")

t = tempfile.mkdtemp(); repo = t + "/r"; os.mkdir(repo)
try:
    sh("git", "init", "-q", ".", cwd=repo); sh("git", "config", "user.email", "t@e.com", cwd=repo); sh("git", "config", "user.name", "T", cwd=repo)
    open(repo + "/HANDOFFS.md", "w").write(LEDGER("pending"))
    sh("git", "add", ".", cwd=repo); sh("git", "commit", "-q", "-m", "claim", cwd=repo)
    S = "sess-1"
    fire(repo, S, "SessionStart")
    case("1  newest receipt pending (no close-out yet), prose message", fire(repo, S, "Stop", "hello"), (0, "allow"))
    open(repo + "/HANDOFFS.md", "w").write(LEDGER("complete")); sh("git", "commit", "-qam", "close-out", cwd=repo)
    case("2  close-out done, final message 'Done.'", fire(repo, S, "Stop", "Done."), (0, "BLOCK"))
    case("3  same, but stop_hook_active (harness guard: one retry only)", fire(repo, S, "Stop", "Done.", True), (0, "allow"))
    good = report(repo)
    case("4  close-out done, message IS a lint-clean report", fire(repo, S, "Stop", good), (0, "allow"))
    case("5  later chat, nothing changed since the report", fire(repo, S, "Stop", "Sure, anything else?"), (0, "allow"))
    open(repo + "/note.txt", "w").write("x"); sh("git", "add", ".", cwd=repo); sh("git", "commit", "-qm", "post-report action", cwd=repo)
    case("6  a commit landed AFTER the report; message 'Pushed.' (S230 case)", fire(repo, S, "Stop", "Pushed."), (0, "BLOCK"))
    p = {"session_id": S, "cwd": repo, "hook_event_name": "SessionStart", "source": "resume"}
    subprocess.run([sys.executable, os.path.join(HERE, "hook_proto.py")], input=json.dumps(p), capture_output=True, text=True)
    case("7  SessionStart(resume) must not reset the baseline; still BLOCK", fire(repo, S, "Stop", "x"), (0, "BLOCK"))
    case("8  stale report (HEAD moved after it was printed) is not accepted", fire(repo, S, "Stop", good), (0, "BLOCK"))
    case("9  new session_id, no baseline recorded (fail-quiet)", fire(repo, "sess-2", "Stop", "Done."), (0, "allow"))
    open(repo + "/HANDOFFS.md", "w").write("not a ledger\n")
    case("10 internal error (ledger unparseable) exits 0, never 2", fire(repo, S, "Stop", "Done."), (0, "allow"))
finally:
    shutil.rmtree(t)
print("== 1. hook decision table"); print("\n".join(rows)); print(f"rows failed: {bad} of {len(rows)}")

def lint_mutants():
    t = tempfile.mkdtemp(); repo = t + "/r"; os.mkdir(repo)
    try:
        sh("git", "init", "-q", ".", cwd=repo); sh("git", "config", "user.email", "t@e.com", cwd=repo); sh("git", "config", "user.name", "T", cwd=repo)
        open(repo + "/HANDOFFS.md", "w").write(LEDGER("complete")); sh("git", "add", ".", cwd=repo); sh("git", "commit", "-qm", "c", cwd=repo)
        m = C.mech(repo + "/HANDOFFS.md", repo); good = report(repo); head = m["head"]
        assert C.lint(good, m) == [], "the generator's own output must lint clean"
        muts = {"drop closing line": good.replace("\nSession over.\n", "\n"), "text after closing line": good + "\nShall I continue?\n",
                "prefix before heading": "Here is the summary:\n\n" + good, "wrong self score": good.replace("8/10", "9/10"),
                "stale HEAD sha": good.replace(head, "deadbee"), "missing Next session label": good.replace("**Next session:**", "Next:"),
                "table pipe": good.replace("DONE", "DONE | x"), "over 2000 B": good.replace("demo", "x" * 2100, 1),
                "heading names other session": good.replace("S2 ·", "S9 ·"), "labels out of order": good.replace("**Record:**", "**Zed:**").replace("**Next session:**", "**Record:**").replace("**Zed:**", "**Next session:**")}
        out, miss = [], 0
        for n, t_ in muts.items():
            caught = bool(C.lint(t_, m)); miss += 0 if caught else 1; out.append(f"{'CAUGHT' if caught else 'MISSED'}  {n}")
        return out, miss
    finally:
        shutil.rmtree(t)

def hook_mutants():
    muts = {"drop the stop_hook_active guard": ('    if payload.get("stop_hook_active"):\n        return None', '    if False:\n        return None'),
            "drop the already-reported stamp check": ('    if os.path.exists(stamp) and json.load(open(stamp)) == state:\n        return None', '    if False:\n        return None'),
            "SessionStart overwrites the baseline": ('        if not os.path.exists(base):\n            json.dump', '        if True:\n            json.dump'),
            "no baseline counts as owed": ('owed = bool(b) and r.get("status") == "complete" and (r["session"] != b["id"] or b["status"] != "complete")',
                                           'owed = r.get("status") == "complete" and (b is None or r["session"] != b["id"] or b["status"] != "complete")'),
            "internal error exits 2": ('    except Exception:\n        out = None', '    except Exception:\n        sys.exit(2)'),
            "stamp ignores HEAD": ('state = [m["head"], ', 'state = ["x", ')}
    out, miss = [], 0
    for n, (a, b) in muts.items():
        t = tempfile.mkdtemp()
        try:
            shutil.copytree(HERE, t + "/m", ignore=shutil.ignore_patterns("__pycache__"))
            h = open(t + "/m/hook_proto.py").read(); assert a in h, n
            open(t + "/m/hook_proto.py", "w").write(h.replace(a, b, 1))
            r = subprocess.run([sys.executable, t + "/m/checks.py", "--table-only"], capture_output=True, text=True)
            fails = [l.split()[1] for l in r.stdout.splitlines() if l.startswith("FAIL")]
            caught = r.returncode != 0; miss += 0 if caught else 1
            out.append(f"{'CAUGHT' if caught else 'MISSED'}  {n:40s} failing rows: {','.join(fails) or '-'}")
        finally:
            shutil.rmtree(t)
    return out, miss

if "--table-only" in sys.argv:
    sys.exit(1 if bad else 0)
lo, lm = lint_mutants(); print("\n== 2. lint mutants"); print("\n".join(lo)); print(f"missed: {lm} of {len(lo)}")
ho, hm = hook_mutants(); print("\n== 3. hook mutants"); print("\n".join(ho)); print(f"missed: {hm} of {len(ho)}")
sys.exit(1 if (bad or lm or hm) else 0)
