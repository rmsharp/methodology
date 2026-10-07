#!/usr/bin/env bash
# BL-101 P5 runtime check, on REAL data: the dashboard (tools/methodology_dashboard.py, DASHBOARD_VERSION 2.22.0)
# against the dashboard this repository carried before P5 (the version at OLD_REV, 2.21.0), in three parts.
# Nothing is written to a real repository: every part works in `--no-local` clones, which hold the COMMITTED state
# only. That is deliberate. A live working tree is a moving target (the first run of this script read an active
# 1.5-million-file repository whose OLD dashboard disagreed with ITSELF by 17 files between two scans, and an
# adopter that took a commit between two clones), so a comparison on a live tree proves nothing either way.
# Every repository is cloned ONCE and the moved tree is a clone of that clone, so the two share a commit.
#
#   A  legacy regression   every repository under the portfolio root that carries the methodology at its root
#                          (the adopters, and this one), as committed, is scanned by the OLD and the NEW
#                          dashboard. The two full metrics dicts must be EQUAL once the one additive key
#                          (`methodology.layout`) is set aside: a project that has not moved must read as it read.
#   B  a project that moved   a few real adopters are cloned and their methodology files `git mv`ed under
#                          methodology/ the way bin/migrate-layout (P7) will move them. The OLD dashboard on
#                          the legacy clone and the NEW dashboard on the moved clone must agree on the
#                          compliance score, the file inventory, the ledger and the trim row. The one
#                          difference allowed is the documentation sub-score's `docs/` point, and only for an
#                          adopter that has no docs/ of its own (`has_docs_dir`: pinned on purpose, plan 7.2d).
#   C  --sync over a scratch portfolio   a legacy project, a migrated one, a half-migrated one and an empty
#                          one: a dry run names each target's resolved path and writes nothing.
#
# GitHub and dependency-audit collectors are stubbed to their no-remote answers in BOTH dashboards (network,
# not layout). Run from the repo root:   bash docs/planning/methodology-subdirectory-evidence/dashboard-in-both-layouts.sh
set -u
SRC="$(git rev-parse --show-toplevel)" || exit 3
PORT="$(dirname "$SRC")"
OLD_REV="${OLD_REV:-4a7ce9f}"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
git -C "$SRC" show "$OLD_REV:tools/methodology_dashboard.py" > "$T/old_dashboard.py" || exit 3
cp "$SRC/tools/methodology_dashboard.py" "$T/new_dashboard.py"
printf 'commit under test: %s   old dashboard: %s (%s)\n' "$(git -C "$SRC" rev-parse --short HEAD)" "$OLD_REV" \
  "$(grep -m1 '^DASHBOARD_VERSION' "$T/old_dashboard.py" | tr -d ' ')"
printf 'new dashboard: %s\n\n' "$(grep -m1 '^DASHBOARD_VERSION' "$T/new_dashboard.py" | tr -d ' ')"

python3 -B - "$SRC" "$PORT" "$T" <<'PYEOF'
import importlib.util, json, os, re, subprocess, sys
from pathlib import Path

sys.dont_write_bytecode = True
src, port, t = (Path(a) for a in sys.argv[1:4])


def load(name, p):
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.collect_github_metrics = lambda path: {"open_issues": None, "open_prs": None, "repo_slug": None}
    m.collect_vulnerability_metrics = lambda path: {"vulnerabilities": [], "total_vulns": 0, "scanned": False}
    return m


old, new = load("old_dashboard", t / "old_dashboard.py"), load("new_dashboard", t / "new_dashboard.py")
spec = importlib.util.spec_from_file_location("lf", src / "tools" / "layout_fixtures.py")
lf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lf)
manifest = lf._manifest()
bad = 0


def git(path, *a):
    return subprocess.run(["git", "-C", str(path), *a], capture_output=True, text=True, check=True).stdout


def scan(mod, path):
    return json.loads(json.dumps(mod.collect_all(Path(path)), default=str, sort_keys=True))


def without_layout(d):
    d = json.loads(json.dumps(d))
    d["methodology"].pop("layout", None)
    return d


# ---- A ------------------------------------------------------------------------------------------------
print("== A. a project that has not moved reads exactly as it read ==")
repos = sorted(p for p in port.iterdir() if (p / ".git").exists() and (p / "SESSION_RUNNER.md").is_file())
repos.append(src)
a_same = 0
snaps = {}
for p in repos:
    snap = t / ("snap-" + p.name)
    subprocess.run(["git", "clone", "-q", "--no-local", str(p), str(snap)], check=True)
    snaps[p.name] = snap
    o, n = scan(old, snap), scan(new, snap)
    same = without_layout(o) == without_layout(n)
    a_same += same
    bad += not same
    lay = n["methodology"]["layout"]
    print("   %-28s health %3d -> %3d  compliance %3d -> %3d  layout %-6s  full metrics equal: %s" % (
        p.name, o["scores"]["health"]["total"], n["scores"]["health"]["total"],
        o["methodology"]["compliance_score"], n["methodology"]["compliance_score"], lay["kind"],
        "yes" if same else "NO"))
    if not same:
        for k in o:
            if k != "methodology" and o[k] != n[k]:
                print("        differs in:", k)
print("   %d of %d identical\n" % (a_same, len(repos)))

# ---- B ------------------------------------------------------------------------------------------------
print("== B. the same adopters, cloned and moved under methodology/ ==")
want = ["model_project_constructor", "nprcgenekeepr", "mts-system", "vscode_quarto_ext", "Philippians"]
moved_dirs = {}
for name in want:
    p = port / name
    if not (p / ".git").exists() or not (p / "SESSION_RUNNER.md").is_file():
        print("   %-28s not present here, skipped" % name)
        continue
    legacy, moved = t / (name + "-legacy"), t / (name + "-moved")
    subprocess.run(["git", "clone", "-q", "--no-local", str(p), str(legacy)], check=True)
    subprocess.run(["git", "clone", "-q", "--no-local", str(legacy), str(moved)], check=True)   # the same commit, by construction
    for d in (legacy, moved):
        git(d, "config", "user.email", "t@t")
        git(d, "config", "user.name", "t")
        git(d, "config", "commit.gpgsign", "false")
    n_moved = 0
    for _src, dest, _disp in manifest.DISTRIBUTION:
        if (moved / dest).is_file():
            target = moved / lf.new_path(dest)
            target.parent.mkdir(parents=True, exist_ok=True)
            git(moved, "mv", dest, lf.new_path(dest))
            n_moved += 1
    git(moved, "-c", "core.hooksPath=/dev/null", "commit", "-q", "--allow-empty", "-m", "move the methodology files under methodology/")
    moved_dirs[name] = moved
    o, n = scan(old, legacy), scan(new, moved)
    # the legacy clone and the moved clone differ by one commit, so compare what a layout can change
    keys = [("compliance", lambda m: (m["methodology"]["compliance_score"], m["methodology"]["missing_files"])),
            ("inventory", lambda m: {k: (v.get("count"), v.get("loc")) for k, v in m["files"]["by_category"].items()}),
            ("framework docs", lambda m: m["files"]["framework_docs"]),
            ("ledger", lambda m: (m["changelog"]["present"], m["changelog"]["ledger_present"], m["changelog"]["is_fresh"])),
            ("trim tool", lambda m: m["trim"]["tool_present"]),
            ("doc-only", lambda m: m["doc_only"]["is_doc_only"]),
            ("source loc", lambda m: m["tests"]["source_loc"])]
    diffs = [label for label, f in keys if f(o) != f(n)]
    lay = n["methodology"]["layout"]
    delta = n["scores"]["health"]["total"] - o["scores"]["health"]["total"]
    docs_point = o["docs"]["has_docs_dir"] and not n["docs"]["has_docs_dir"]
    ok = not diffs and delta == (-4 if docs_point else 0) and lay["kind"] == "new"
    bad += not ok
    print("   %-28s at %s moved %2d files  layout %-6s  compliance %3d -> %3d  health %3d -> %3d (%+d%s)  differs in: %s  %s" % (
        name, git(legacy, "rev-parse", "--short", "HEAD").strip(), n_moved, lay["kind"], o["methodology"]["compliance_score"], n["methodology"]["compliance_score"],
        o["scores"]["health"]["total"], n["scores"]["health"]["total"], delta,
        ", the docs/ point: no docs/ of its own" if docs_point else "", ", ".join(diffs) or "nothing", "OK" if ok else "NOT OK"))
print()

# ---- C ------------------------------------------------------------------------------------------------
print("== C. --sync --dry-run over a scratch portfolio: legacy, migrated, half-migrated, empty ==")
if moved_dirs:
    name = sorted(moved_dirs)[0]
    pf = t / "portfolio"
    (pf / "methodology" / "starter-kit").mkdir(parents=True)
    canon = pf / "methodology" / "starter-kit" / "methodology_dashboard.py"
    canon.write_text((t / "new_dashboard.py").read_text(encoding="utf-8"), encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(pf / "methodology")], check=True)
    for label, how in (("legacy", t / (name + "-legacy")), ("migrated", moved_dirs[name])):
        subprocess.run(["git", "clone", "-q", "--no-local", str(how), str(pf / label)], check=True)
    subprocess.run(["git", "clone", "-q", "--no-local", str(moved_dirs[name]), str(pf / "half")], check=True)
    (pf / "half" / "SESSION_RUNNER.md").write_text("# a second runner at the root\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(pf / "empty")], check=True)
    r = subprocess.run([sys.executable, "-B", str(canon), "--sync", "--dry-run"], capture_output=True, text=True, cwd=str(pf))
    lines = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    for l in lines:
        print("   " + re.sub(r"\x1b\[[0-9;]*m", "", l)[:170])
    text = r.stdout
    checks = [("migrated's copy is methodology/methodology_dashboard.py", "migrated/methodology/methodology_dashboard.py" in text),
              ("migrated gets no root copy", not re.search(r"migrated/methodology_dashboard\.py", text)),
              ("legacy's copy is at its root", re.search(r"legacy/methodology_dashboard\.py", text) is not None),
              ("half is refused by name", re.search(r"refuse\s+half", text) is not None),
              ("the dry run wrote nothing", not any((pf / d / "methodology_dashboard.py").exists() != e for d, e in
                                                       (("legacy", True), ("empty", False), ("half", False))))]
    for label, ok in checks:
        bad += not ok
        print("   %-55s %s" % (label, "yes" if ok else "NO"))
print("\nresult: %s" % ("every comparison held" if not bad else "%d comparison(s) did NOT hold" % bad))
sys.exit(1 if bad else 0)
PYEOF
