#!/usr/bin/env python3
"""Cold-start probe (BL-94 P2a, plan docs/planning/documentation-quality-experiment-plan.md section 3.5): rebuild a saved end state
from the evidence bundle and open ONE fresh session in it, which opens with "go", writes the runner's Phase 0 report and stops.

    python3 probe.py RUN_ID --session-cap 2.0 --total-cap 100 [--control git-only] [--no-launch] [--again]
                     [--evidence DIR] [--project PATH] [--out DIR] [--work DIR] [--model sonnet] [--effort xhigh]
    python3 probe.py --list                      # the run ids the bundle holds, with what each probe would need
    python3 probe.py --verify-all                # $0: rebuild every end state and its control from the bundle, check each, delete it

What it does, in order (a refusal at any step ends the run before the next one; nothing is spent before step 4):
  1. refuses when (dollars in OUT/spend.jsonl) + the session cap would pass the total cap, and when the CLI no longer accepts a flag the
     driver passes (a changed flag would otherwise cost a launch to find out); both caps are required, so a total is never read without
     its per-session cap beside it (plan P2a (f));
  2. rebuilds the run's end state from the bundle (doc_evidence.rebuild, which checks the bundle against the project and every run's
     head and pin against the manifest) into WORK/<slug>: a fresh repository holding the PINNED commit and its ancestors only, so no
     later commit of the original session can be found; no remote; the install commit present; the tracked tree clean;
  3. with --control git-only, restores every session-changed RECORD file to its text at the install commit and commits that on top
     (plan 2.3 M4: the same end state with the record reverted), so what remains is what git alone says;
  4. runs `claude -p` in the clone through driver.drive, one stop (--max-stops 1), the same isolation and tool set as every other run;
  5. appends one line to OUT/spend.jsonl, saves the stream log and the report text, and appends one row to OUT/rows.jsonl.

--no-launch stops after step 3 and spends nothing: it is the $0 check that a bundle can rebuild its sha.
What a probe cannot carry (named in every row): uncommitted work and untracked files, the arm's git hook (.git/hooks is not in a bundle),
and the original session's `.git/config`. M1-M3 and M5 read the ORIGINAL record at the pin; M4 reads this report (doc_score.score_report).
"""
import argparse, json, os, shutil, subprocess, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doc_evidence, doc_score, driver, extract, stakeholder

EVIDENCE = os.path.join(doc_evidence.PILOT, "doc-evidence")
OUT = os.path.join(doc_evidence.PILOT, "doc-probe")
WORK = "/tmp/doc-probe"
PROBE_SCRIPT = [stakeholder.OPENING]       # "go", and nothing after it: the probe ends at its first stop
CONTROLS = (None, "git-only")
CONTROL_SUBJECT = "Restore tracked documentation to its text at the install commit"
ENV = dict(os.environ, GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
           GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid")
# A session that reaches --max-budget-usd ends as `result error_max_budget_usd` (seen once, pilot/xhigh-go HEAD rep 1: $2.0389 on a $2.00
# cap, so the CLI overshoots a little and a cap is approximate). Should a cap stop ever come back as an ordinary success, the report would
# be cut short and look whole; a cost at 98% of the session cap is therefore a failed probe whatever the result message says.
CAP_HIT = 0.98
NOT_CARRIED = ["uncommitted work and untracked files", "the arm's git hook (.git/hooks is not in a bundle)", "the original .git/config"]


class Refused(SystemExit):
    """A refusal is a SystemExit with a message, like the driver's, so the command line shows it and a test can catch it."""


def git(repo, *a, check=True, env=None):
    p = subprocess.run(["git", "-c", "core.quotePath=false", "-C", repo, *a], capture_output=True, text=True, env=env or ENV)
    if check and p.returncode != 0:
        raise Refused(f"git {' '.join(a)} failed in {repo}: {p.stderr.strip()}")
    return p.stdout.strip()


def slug(run_id, control=None):
    return run_id.replace("/", "--") + (f"+{control}" if control else "")


def find_run(manifest, run_id):
    for r in manifest["runs"]:
        if r["id"] == run_id:
            return r
    raise Refused(f"unknown run {run_id!r}; `probe.py --list` shows the {len(manifest['runs'])} the bundle holds")


def refuse_unprobable(run):
    """A bundle holds commits only. A run with tracked edits never committed has an end state the bundle cannot rebuild."""
    if run.get("uncommitted_tracked"):
        raise Refused(f"{run['id']}: tracked files were edited and never committed ({', '.join(run['uncommitted_tracked'])}); "
                      "the bundle cannot carry them, so a probe would open on a different state than the session ended in")
    if not run.get("install"):
        raise Refused(f"{run['id']}: no install commit in the manifest, so there is no base to restore for a control or to score against")


def cli_flags(argv):
    return sorted({a for a in argv if a.startswith("--")})


def check_cli_flags(argv, help_text=None):
    """Every long flag the driver passes must appear in `claude --help`. A flag the CLI dropped would fail after the clone is built."""
    if help_text is None:
        p = subprocess.run(["claude", "--help"], capture_output=True, text=True)
        help_text = p.stdout + p.stderr
    missing = [f for f in cli_flags(argv) if f not in help_text]
    if missing:
        raise Refused(f"the CLI no longer lists {', '.join(missing)} in --help; the driver's command line needs a look before any launch")
    return cli_flags(argv)


def refuse_over_cap(out, session_cap, total_cap):
    before = driver.spent(out) if os.path.isdir(out) else 0.0
    if before + session_cap > total_cap:
        raise Refused(f"refused: spent ${before:.2f} + session cap ${session_cap:.2f} > total cap ${total_cap:.2f}")
    return before


def build_clone(scratch, run, dest):
    """A fresh repository at `dest` holding the run's PINNED commit and its ancestors, nothing later. The pin is fetched by ref from the
    rebuilt scratch repository (refs/pins/<id> where the run went on past its pin, refs/runs/<id> where it did not); the sha is checked
    against the manifest before anything is checked out. Returns the facts the row records."""
    if os.path.exists(dest):
        raise Refused(f"{dest} exists; refusing to overwrite")
    ref = f"refs/pins/{run['id']}" if run["pin"] != run["head"] else f"refs/runs/{run['id']}"
    os.makedirs(dest)
    git(dest, "init", "-q", "-b", "master")
    git(dest, "fetch", "-q", "--no-tags", scratch, ref)
    got = git(dest, "rev-parse", "FETCH_HEAD")
    if got != run["pin"]:
        raise Refused(f"{run['id']}: fetched {got} where the manifest pins {run['pin']}")
    git(dest, "checkout", "-q", "-B", "master", "FETCH_HEAD")
    return clone_facts(dest, run)


def clone_facts(dest, run):
    """What makes the clone the end state and nothing else. Any False here is a refusal in `verify_clone`."""
    head = git(dest, "rev-parse", "HEAD")
    later = run["head"] != run["pin"]
    return {"head": head, "pin": run["pin"], "head_is_pin": head == run["pin"],
            "install_is_ancestor": subprocess.run(["git", "-C", dest, "merge-base", "--is-ancestor", run["install"], head]).returncode == 0,
            "later_commits_absent": (subprocess.run(["git", "-C", dest, "cat-file", "-e", run["head"] + "^{commit}"],
                                                    capture_output=True).returncode != 0) if later else None,
            "remotes": git(dest, "remote").split(), "tracked_clean": git(dest, "status", "--porcelain", "--untracked-files=no") == "",
            "commits": int(git(dest, "rev-list", "--count", "HEAD"))}


def verify_clone(facts):
    bad = [k for k, v in (("HEAD is not the pinned sha", facts["head_is_pin"]), ("the install commit is not an ancestor", facts["install_is_ancestor"]),
                          ("a later commit of the original session is present", facts["later_commits_absent"] is not False),
                          ("a remote exists", not facts["remotes"]), ("the tracked tree is not clean", facts["tracked_clean"])) if not v]
    if bad:
        raise Refused("the rebuilt clone is not the end state: " + "; ".join(bad))


def apply_git_only(dest, run):
    """The git-only control: every RECORD file (doc_score.is_record_path) the session changed goes back to its text at the install
    commit, a file the session added is removed, and the result is one commit on top of the pin. Commits keep their shas, so the key's
    deliverable sha still names a commit; the extra commit is a named confound (it is in `git log`)."""
    out = git(dest, "diff", "--name-only", "--no-renames", "-z", run["install"], run["pin"])
    changed = [p for p in out.split("\0") if p]
    restored, removed = [], []
    for p in sorted(changed):
        if not doc_score.is_record_path(p):
            continue
        if subprocess.run(["git", "-C", dest, "cat-file", "-e", f"{run['install']}:{p}"], capture_output=True).returncode == 0:
            git(dest, "checkout", run["install"], "--", p)
            restored.append(p)
        else:
            git(dest, "rm", "-q", "-f", "--", p)
            removed.append(p)
    if not restored and not removed:
        raise Refused(f"{run['id']}: the session changed no record file, so a git-only control would equal the end state")
    git(dest, "commit", "-q", "--no-verify", "-m", CONTROL_SUBJECT)
    after = [p for p in git(dest, "diff", "--name-only", "--no-renames", "-z", run["install"], "HEAD").split("\0") if p and doc_score.is_record_path(p)]
    if after:
        raise Refused(f"{run['id']}: record files still differ from the install commit after the control: {after[:5]}")
    return {"restored": restored, "removed": removed, "commit": git(dest, "rev-parse", "HEAD"), "parent_is_pin": git(dest, "rev-parse", "HEAD^") == run["pin"]}


def report_text(log):
    """The probe's report: the `result` field of the last result message in the stream log (the final assistant text of the turn)."""
    text = None
    for line in log:
        try:
            m = json.loads(line)
        except ValueError:
            continue
        if m.get("type") == "result" and isinstance(m.get("result"), str):
            text = m["result"]
    return text


def phase0_reads(events):
    """Paths the session read with the Read tool before its first stop, in order (a Bash `cat` is not counted: the row says so)."""
    return [e["input"].get("file_path", "") for e in events if e["kind"] == "tool_use" and e["name"] == "Read"]


def run_probe(run_id, session_cap, total_cap, control=None, evidence=EVIDENCE, project=doc_evidence.DEFAULT_PROJECT, out=OUT, work=WORK,
              model="sonnet", effort="xhigh", launch=True, again=False, argv=None, popen=None, help_text=None):
    """One probe. `argv` and `popen` are injection points for a test (a fake `claude`); the real command is driver.cmd(...)."""
    if control not in CONTROLS:
        raise Refused(f"control must be one of {CONTROLS}")
    argv = argv or driver.cmd(model, session_cap, effort)
    key = {"run": run_id, "control": control}
    rows = os.path.join(out, "rows.jsonl")
    if launch:
        refuse_over_cap(out, session_cap, total_cap)
        if argv[0] == "claude":                # a test's fake process is not the CLI and has no --help to check
            check_cli_flags(argv, help_text)
        if not again and os.path.exists(rows) and any({k: json.loads(l).get(k) for k in key} == key for l in open(rows) if l.strip()):
            raise Refused(f"{run_id}{' +' + control if control else ''} was probed already (rows.jsonl); --again if the first launch hit a defect")
    scratch, manifest = doc_evidence.rebuild(evidence, project)
    try:
        run = find_run(manifest, run_id)
        refuse_unprobable(run)
        dest = os.path.join(work, slug(run_id, control))
        facts = build_clone(scratch, run, dest)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)     # holds every run of the bundle; the clone has what it needs
    verify_clone(facts)
    ctl = apply_git_only(dest, run) if control else None
    row = {"kind": "probe", "run": run_id, "control": control, "arm": run["arm"], "rep": run["rep"], "pin": run["pin"], "install": run["install"],
           "start": run["start"], "clone": facts, "control_detail": ctl, "clone_dir": dest, "not_carried": NOT_CARRIED,
           "original_cli": run.get("cli"), "session_cap": session_cap, "total_cap": total_cap, "model_requested": model, "effort": effort}
    if not launch:
        row["launched"] = False
        return row
    os.makedirs(out, exist_ok=True)
    popen = popen or subprocess.Popen
    t0 = time.time()
    try:
        res = driver.drive(argv, dest, max_stops=1, popen=popen, script=PROBE_SCRIPT, done=None, pace=0)
    except OSError as e:     # the CLI is missing or died before reading its first message; nothing ran, so nothing was spent
        res = {"session_id": None, "cost_usd": 0.0, "stops": 0, "replies": [], "end": f"driver error {type(e).__name__}: {e}", "init": None, "log": []}
    with open(os.path.join(out, "spend.jsonl"), "a") as f:
        f.write(json.dumps({"arm": run["arm"], "rep": run["rep"], "cost_usd": res["cost_usd"], "kind": "probe", "run": run_id, "control": control}) + "\n")
    base = os.path.join(out, slug(run_id, control))
    os.makedirs(base, exist_ok=True)
    with open(os.path.join(base, "stream.jsonl"), "w") as f:
        f.writelines(res["log"])
    report = report_text(res["log"])
    if report is not None:
        with open(os.path.join(base, "report.md"), "w") as f:
            f.write(report)
    tp = driver.transcript_path(res["session_id"]) if res["session_id"] else None
    row.update({"launched": True, "session_id": res["session_id"], "cost_usd": res["cost_usd"], "stops": res["stops"], "end": res["end"],
                "cap_hit": res["cost_usd"] >= CAP_HIT * session_cap,
                "probe_ok": res["stops"] == 1 and report is not None and res["cost_usd"] < CAP_HIT * session_cap, "report_chars": len(report) if report is not None else None,
                "report": os.path.relpath(os.path.join(base, "report.md"), out) if report is not None else None,
                "wall_seconds": round(time.time() - t0, 1), "transcript": tp, "init": res["init"], "cli": None, "usage": None, "reads": None})
    if tp:
        import replaylib
        recs = replaylib.load_records(tp)
        row["usage"] = extract.row(tp, arm=run["arm"], rep=run["rep"])
        row["cli"] = doc_evidence.cli_versions(tp)
        row["reads"] = phase0_reads(replaylib.events(recs))
    with open(rows, "a") as f:
        f.write(json.dumps(row) + "\n")
    return row


def verify_all(evidence=EVIDENCE, project=doc_evidence.DEFAULT_PROJECT, work="/tmp/doc-probe-verify", say=print):
    """The $0 pre-flight for the whole bundle: rebuild every run's end state and its git-only control, check each clone, delete it.
    Returns one row per run. A run the manifest marks as having uncommitted tracked files is EXPECTED to be refused; any other refusal
    is a bundle that cannot rebuild its end state (plan P2a STOP)."""
    with open(os.path.join(evidence, "manifest.json")) as f:
        runs = json.load(f)["runs"]
    rows = []
    for r in runs:
        row = {"id": r["id"], "expected_refusal": bool(r.get("uncommitted_tracked"))}
        for control in (None, "git-only"):
            name = control or "end_state"
            try:
                got = run_probe(r["id"], 0.0, 0.0, control, evidence, project, os.path.join(work, "ledger"), work, launch=False)
                row[name] = "ok" if got["clone"]["head_is_pin"] else "WRONG HEAD"
            except Refused as e:
                row[name] = f"refused: {e}"
            shutil.rmtree(os.path.join(work, slug(r["id"], control)), ignore_errors=True)
        row["ok"] = all(row[k] == "ok" for k in ("end_state", "git-only")) if not row["expected_refusal"] else all(str(row[k]).startswith("refused") for k in ("end_state", "git-only"))
        say(f"{r['id']:28} end state: {row['end_state'][:40]:40} control: {row['git-only'][:60]}")
        rows.append(row)
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("run", nargs="?"); ap.add_argument("--list", action="store_true")
    ap.add_argument("--verify-all", action="store_true", help="$0: rebuild every run's end state and its git-only control, check, delete")
    ap.add_argument("--session-cap", type=float); ap.add_argument("--total-cap", type=float)
    ap.add_argument("--control", choices=[c for c in CONTROLS if c]); ap.add_argument("--no-launch", action="store_true"); ap.add_argument("--again", action="store_true")
    ap.add_argument("--evidence", default=EVIDENCE); ap.add_argument("--project", default=doc_evidence.DEFAULT_PROJECT)
    ap.add_argument("--out", default=OUT); ap.add_argument("--work", default=WORK)
    ap.add_argument("--model", default="sonnet"); ap.add_argument("--effort", default="xhigh")
    a = ap.parse_args(argv)
    if a.list:
        for r in json.load(open(os.path.join(a.evidence, "manifest.json")))["runs"]:
            note = "REFUSED: uncommitted tracked files" if r.get("uncommitted_tracked") else ""
            print(f"{r['id']:28} pin {r['pin'][:9]}  {r['commits_after_start']:>3} commits  cli {','.join(r.get('cli') or [])}  {note}")
        return
    if a.verify_all:
        rows = verify_all(a.evidence, a.project, a.work if a.work != WORK else "/tmp/doc-probe-verify")
        bad = [r["id"] for r in rows if not r["ok"]]
        print(f"{len(rows) - len(bad)} of {len(rows)} runs as expected; {sum(r['expected_refusal'] for r in rows)} refused by design (uncommitted tracked files)"
              + (f"; NOT as expected: {bad}" if bad else ""))
        raise SystemExit(1 if bad else 0)
    if not a.run:
        ap.error("RUN_ID is required (or --list, or --verify-all)")
    if not a.no_launch and (a.session_cap is None or a.total_cap is None):
        ap.error("--session-cap and --total-cap are both required to launch: a total is only usable beside its per-session cap")
    row = run_probe(a.run, a.session_cap or 0.0, a.total_cap or 0.0, a.control, a.evidence, a.project, a.out, a.work, a.model, a.effort,
                    launch=not a.no_launch, again=a.again)
    print(json.dumps({k: row[k] for k in row if k not in ("init", "usage", "reads")}, indent=1))


if __name__ == "__main__":
    main()
