#!/usr/bin/env python3
"""BL-101 P7 evidence: bin/migrate-layout over the 12 adopter repositories, each in a --no-local CLONE.

Plan: docs/planning/methodology-subdirectory-plan.md section 7.3 row P7. For each adopter the script
  1. clones the adopter's committed HEAD (nothing in a real tree is read through the working directory, written, or run),
     sets a throwaway identity and arms the hooks path the real clone has;
  2. reads bin/status; if any TRACKED file is not `current`, runs bin/sync and commits it as its own commit
     (plan 5A.2: sync before migrate), with --force in the clone if the sync alone refuses (and says so);
  3. copies the synced clone (the "before" tree), runs the project's own dashboard and ratchet there;
  4. runs bin/migrate-layout as a dry run, then with --apply (checks on), in the clone;
  5. runs the migrated project's own dashboard and ratchet, and records one row.
The output is a table with one row per adopter and no blank cell (a step that does not apply says why), rows.json (the rows as
data) and reports.json (the raw JSON report of each dry run and apply, by adopter). Run it from the repository root:

    python3 docs/planning/methodology-subdirectory-evidence/migrate-12-adopters.py [--only NAME ...] [--out DIR]

It takes tens of minutes (the proofs of nprcgenekeepr alone are 130 scripts, run twice). Nothing it writes leaves --work.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True

REPO = Path(__file__).resolve().parents[3]
DEV = Path.home() / "Development"
ADOPTERS = ["model_project_constructor", "feedback-loop-comparison", "nprcgenekeepr", "mts-system", "vscode_quarto_ext",
            "Philippians", "airqino", "chat_verification", "church_growth", "dalia_martinez_funeral", "claude_work", "wsfct"]
ANSI = re.compile(r"\x1b\[[0-9;]*m")
TRAILER = "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"


def sh(args, cwd=None, timeout=1800, env=None):
    """(exit code, output) -- an exit code of 'timeout' or 'error' is a cell, not a crash."""
    try:
        r = subprocess.run(args, cwd=str(cwd) if cwd else None, capture_output=True, text=True, timeout=timeout,
                           env=env or os.environ)
        return r.returncode, ANSI.sub("", r.stdout + r.stderr)
    except subprocess.TimeoutExpired:
        return "timeout", ""
    except OSError as e:
        return "error", str(e)


def git(clone, *args, timeout=600):
    return sh(["git", "-C", str(clone), "-c", "commit.gpgsign=false", *args], timeout=timeout)


def status_counts(project):
    """(tracked rows, tracked rows not current, the not-current rows) from bin/status over `project`."""
    code, out = sh([sys.executable, "-B", str(REPO / "bin" / "status"), str(project)])
    lines = out.splitlines()
    head = next((i for i, line in enumerate(lines) if line.startswith("Project ")), None)
    if code != 0 or head is None:
        return None, None, ["bin/status failed: " + out.strip()[-200:]]
    h = lines[head]
    c1, c2, c3 = h.index("File"), h.index("Disposition"), h.index("Status")
    rows = []
    for line in lines[head + 1:]:
        if not line.strip():
            break
        rows.append((line[c1:c2].strip(), line[c2:c3].strip(), line[c3:].strip()))
    tracked = [(f, s) for f, d, s in rows if d == "tracked"]
    bad = ["%s (%s)" % (f, s) for f, s in tracked if s != "current"]
    return len(tracked), len(bad), bad


def project_tool(project, name):
    """The project's own copy of a methodology tool, at the root or under methodology/."""
    for rel in (name, "methodology/" + name):
        if (Path(project) / rel).is_file():
            return rel
    return None


def dashboard_health(project):
    rel = project_tool(project, "methodology_dashboard.py")
    if rel is None:
        return "no dashboard copy"
    code, out = sh([sys.executable, "-B", rel, "--no-open"], cwd=project, timeout=900)
    m = re.search(r"Health:\s*(\d+)/100", out)
    return int(m.group(1)) if m else "exit %s: %s" % (code, out.strip()[-120:])


def ratchet_line(project):
    rel = project_tool(project, "quality_ratchet.py")
    if rel is None:
        return "no ratchet copy"
    code, out = sh([sys.executable, "-B", rel, "--run"], cwd=project, timeout=900)
    lines = [x.strip() for x in out.splitlines() if x.strip()]
    pick = [x for x in lines if "pass" in x and "fail" in x]
    return (pick[-1] if pick else ("exit %s: %s" % (code, lines[-1] if lines else "no output")))[:160]


def run_one(name, work, reports):
    row = {"adopter": name}
    reports[name] = {}
    src = DEV / name
    clone = work / name
    t0 = time.time()
    code, out = sh(["git", "clone", "-q", "--no-local", str(src), str(clone)])
    if code != 0:
        row["clone"] = "failed: " + out.strip()[-160:]
        return row
    git(clone, "config", "user.email", "evidence@example.com")
    git(clone, "config", "user.name", "P7 evidence")
    code, hp = sh(["git", "-C", str(src), "config", "--get", "core.hooksPath"])
    if code == 0 and hp.strip():
        git(clone, "config", "core.hooksPath", hp.strip())
        row["hooks"] = "armed: " + hp.strip()
    else:
        row["hooks"] = "none"
    has_commit = git(clone, "rev-parse", "--verify", "-q", "HEAD")[0] == 0
    row["head"] = git(clone, "rev-parse", "--short", "HEAD")[1].strip() if has_commit else "no commits"
    tracked, bad, bad_rows = status_counts(clone)
    row["status_before_sync"] = "%s tracked, %s not current" % (tracked, bad)
    row["sync"] = "not needed"
    if bad:
        c1, o1 = sh([sys.executable, "-B", str(REPO / "bin" / "sync"), str(clone)])
        forced = False
        if c1 != 0:
            c1, o1 = sh([sys.executable, "-B", str(REPO / "bin" / "sync"), str(clone), "--force"])
            forced = True
        if c1 != 0:
            row["sync"] = "FAILED (exit %s): %s" % (c1, o1.strip()[-160:])
        else:
            git(clone, "add", "-A")
            msg = "sync the methodology files before the layout migration\n\n" + TRAILER
            cc, co = git(clone, "commit", "-q", "-m", msg)
            hook_note = "ok"
            if cc != 0:  # the adopter's own armed hook refused the sync commit (a real session would write the entry it wants)
                hook_note = "its own hook refused (%s); committed with --no-verify" % " ".join(co.split())[-90:]
                cc, co = git(clone, "commit", "-q", "--no-verify", "-m", msg)
            n = git(clone, "diff", "--name-only", "HEAD~1", "HEAD")[1].split() if cc == 0 else []
            row["sync"] = "%s (%d files, %s)" % ("committed with --force" if forced else "committed", len(n), hook_note)
        tracked, bad, bad_rows = status_counts(clone)
    row["status_after_sync"] = "%s tracked, %s not current%s" % (tracked, bad, (": " + ", ".join(bad_rows[:4])) if bad else "")
    # the before tree: a copy, so the dashboard's and the ratchet's writes do not dirty the tree that is migrated
    pre = work / (name + "-before")
    shutil.copytree(clone, pre, symlinks=True)
    row["health_before"] = dashboard_health(pre) if has_commit else "no commits"
    row["ratchet_before"] = ratchet_line(pre) if has_commit else "no commits"
    shutil.rmtree(pre, ignore_errors=True)
    # the dry run, then the apply
    code, out = sh([sys.executable, "-B", str(REPO / "bin" / "migrate-layout"), str(clone), "--json"])
    try:
        dry = json.loads(out)
    except ValueError:
        dry = {"status": "unparseable", "raw": out[-300:]}
    row["dry_exit"] = code
    row["dry_status"] = dry.get("status")
    row["refusals"] = "; ".join("%s: %s" % (r["code"], r["message"][:100]) for r in dry.get("refusals", [])) or "none"
    reports[name]["dry_run"] = dry
    code, out = sh([sys.executable, "-B", str(REPO / "bin" / "migrate-layout"), str(clone), "--apply", "--json", "--trailer", TRAILER], timeout=3600)
    try:
        app = json.loads(out)
    except ValueError:
        app = {"status": "unparseable", "raw": out[-300:]}
    row["apply_exit"] = code
    row["apply_status"] = app.get("status")
    row["hook_rollback"] = "-"
    if app.get("status") == "rolled-back" and row["hooks"] != "none":
        # the adopter's own hook refused the commit: say what it said, then run the rest of the plan with this clone's hooks off
        row["hook_rollback"] = " ".join(((app.get("commit") or {}).get("error") or "").split())[:200]
        reports[name]["apply_with_its_hooks"] = app
        git(clone, "config", "--unset", "core.hooksPath")
        code, out = sh([sys.executable, "-B", str(REPO / "bin" / "migrate-layout"), str(clone), "--apply", "--json", "--trailer", TRAILER], timeout=3600)
        try:
            app = json.loads(out)
        except ValueError:
            app = {"status": "unparseable", "raw": out[-300:]}
        row["apply_exit"] = "%s (hooks on) then %s (hooks off)" % (row["apply_exit"], code)
        row["apply_status"] = "rolled back by its hook; %s with hooks off" % app.get("status")
    reports[name]["apply"] = app
    moves = app.get("moves") or dry.get("moves") or []
    row["moves"] = "%d (%d tracked, %d plain)" % (len(moves), sum(1 for m in moves if m["tracked"]), sum(1 for m in moves if not m["tracked"]))
    scores = [x["score"] for x in (app.get("commit") or {}).get("renames", [])]
    row["min_similarity"] = ("R%d" % min(scores)) if scores else "-"
    rewrites = {x["path"]: x["replacements"] for x in (app.get("rewrites") or dry.get("rewrites") or [])}
    row["rewrites"] = ", ".join("%s %d" % (k, v) for k, v in sorted(rewrites.items())) or "none"
    nr = app.get("not_rewritten") or dry.get("not_rewritten") or {}
    row["hits"] = ", ".join("%s %d" % (k, nr[k]["mentions"]) for k in ("ci", "harness", "hooks", "ledger", "other") if k in nr) or "-"
    le = app.get("ledger_entry") or dry.get("ledger_entry")
    row["ledger_entry"] = le["path"] if le else "no ledger"
    left = app.get("left_in_place") or dry.get("left_in_place") or []
    row["left_in_place"] = str(len(left))
    reh = app.get("rehearsal") or dry.get("rehearsal") or {}
    row["rehearsal"] = ("%d proof(s) run, kept in place: %s" % (reh.get("proofs", 0), ", ".join(reh.get("excluded") or ["none"]))) if reh.get("ran") else "no proofs to rehearse"
    ck = app.get("checks") or {}
    if ck.get("ran"):
        row["checks"] = "ok" if ck["ok"] else "DIFFER: " + ",".join(ck["differences"])
        b, a = ck["before"], ck["after"]
        row["proofs"] = "%s -> %s" % (json.dumps(b["proofs"]["histogram"], sort_keys=True), json.dumps(a["proofs"]["histogram"], sort_keys=True))
        row["history"] = "%d -> %d" % (b["history"]["commits"], a["history"]["commits"])
        row["links"] = "exit %s -> exit %s" % (b["links"]["exit"], a["links"]["exit"])
    else:
        row["checks"] = "not run (%s)" % app.get("status")
        row["proofs"] = row["history"] = row["links"] = "-"
    if app.get("status") in ("applied",):
        row["tree_clean"] = "yes" if git(clone, "status", "--porcelain")[1].strip() == "" else "NO"
        row["health_after"] = dashboard_health(clone)
        git(clone, "checkout", "-q", "--", ".")
        row["ratchet_after"] = ratchet_line(clone)
    else:
        row["tree_clean"] = "yes" if has_commit and git(clone, "status", "--porcelain")[1].strip() == "" else "-"
        row["health_after"] = row["ratchet_after"] = "not migrated"
    row["seconds"] = int(time.time() - t0)
    return row


COLUMNS = [("adopter", "adopter"), ("hooks", "hooks"), ("status_before_sync", "status before sync"), ("sync", "sync"),
           ("dry_status", "dry run"), ("apply_status", "apply"), ("apply_exit", "exit"), ("refusals", "refusals"),
           ("hook_rollback", "its hook refused the commit"), ("rehearsal", "shards kept (rehearsal)"),
           ("moves", "moves"), ("min_similarity", "min rename"), ("rewrites", "rewrites"), ("left_in_place", "left"),
           ("hits", "not rewritten (mentions)"), ("ledger_entry", "ledger entry"), ("checks", "checks"), ("proofs", "proofs"),
           ("history", "history"), ("links", "check-links"), ("tree_clean", "clean"), ("health_before", "health before"),
           ("health_after", "health after"), ("ratchet_before", "ratchet before"), ("ratchet_after", "ratchet after"),
           ("seconds", "s")]


def table(rows):
    out = ["| " + " | ".join(h for _k, h in COLUMNS) + " |", "|" + "---|" * len(COLUMNS)]
    for r in rows:
        out.append("| " + " | ".join(str(r.get(k, "MISSING")).replace("|", "/") for k, _h in COLUMNS) + " |")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--only", nargs="*", help="adopter names (default: all twelve)")
    p.add_argument("--out", default=str(Path(__file__).resolve().parent / "p7-adopter-runs"))
    p.add_argument("--work", help="a directory for the clones (default: a temporary one, removed at the end)")
    p.add_argument("--resume", action="store_true", help="keep the rows already in --out/rows.json and run only the adopters missing from it")
    args = p.parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    names = args.only or ADOPTERS
    work_ctx = tempfile.TemporaryDirectory(prefix="p7-clones-") if not args.work else None
    work = Path(args.work) if args.work else Path(work_ctx.name)
    work.mkdir(parents=True, exist_ok=True)
    rows, reports = [], {}
    if args.resume and (out_dir / "rows.json").is_file():
        rows = json.loads((out_dir / "rows.json").read_text(encoding="utf-8"))
        reports = json.loads((out_dir / "reports.json").read_text(encoding="utf-8")) if (out_dir / "reports.json").is_file() else {}
    done = {r["adopter"] for r in rows}
    for name in names:
        if name in done:
            continue
        print("== %s" % name, flush=True)
        try:
            row = run_one(name, work, reports)
        except Exception as e:  # noqa: BLE001 -- one adopter's failure is a row, not the end of the run
            row = {"adopter": name, "apply_status": "SCRIPT ERROR: %r" % (e,)}
        rows.append(row)
        print(json.dumps(row), flush=True)
        (out_dir / "rows.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
        (out_dir / "reports.json").write_text(json.dumps(reports, indent=1, sort_keys=True), encoding="utf-8")
        shutil.rmtree(work / name, ignore_errors=True)
    order = {n: i for i, n in enumerate(ADOPTERS)}
    rows.sort(key=lambda r: order.get(r["adopter"], 99))
    md = table(rows)
    (out_dir / "summary.md").write_text(md + "\n", encoding="utf-8")
    print(md)
    if work_ctx:
        work_ctx.cleanup()
    return 0


if __name__ == "__main__":
    sys.exit(main())
