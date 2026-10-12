#!/usr/bin/env python3
"""BL-105 rehearsal driver (S302): what a COMPANION RULE would do, simulated with the tool's own functions.

Plan D10: `PROJECT_LEARNINGS.md` joins the `methodology/` set as a companion of the move, with no manifest entry. Nothing
is built. This script imports bin/migrate-layout as a module and applies ONE extra mapping to its existing rewrite
functions, in a clone it is given; it never edits the module, never commits, never touches a path outside the clone.

  bl105-companion.py scan <clone> <out.json>     the tool's own list (`scan_hits`) for the move, and the before-checks
  bl105-companion.py move <clone> <out.json>     git mv + the rewrites + the after-checks (the caller commits)
  bl105-companion.py checks <clone> <out.json> <before.json>
                                                 the tool's checks on the COMMITTED result, against a `move` run's before-checks

Where the tool would look for a config in a tree it calls migrated, `plan_rewrites` looks at the ROOT only (`add(...)`
tests `root / path`), so this driver reads each config at the root and under methodology/ and says which it found: that
is one of the things the rehearsal reports.
"""
import difflib
import importlib.machinery
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
CANONICAL = Path(__file__).resolve().parents[3]
SRC, DEST = "PROJECT_LEARNINGS.md", "methodology/PROJECT_LEARNINGS.md"


def load_tool():
    loader = importlib.machinery.SourceFileLoader("migrate_layout", str(CANONICAL / "bin" / "migrate-layout"))
    spec = importlib.util.spec_from_loader("migrate_layout", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


def rewrites_for(ml, root, mapping):
    """(path, new text, replacements, diff) for each file the tool's rewrite functions edit, found where it is."""
    tokens = ml.token_rewriter(mapping)
    out, found = [], {}
    plan = [(".gitignore", lambda s: ml.rewrite_gitignore(s, mapping)),
            ("CLAUDE.md", tokens),
            (".context-budget.json", lambda s: ml.rewrite_json(s, mapping)),
            (".quality-gates.json", lambda s: ml.rewrite_json(s, mapping))]
    for name, fn in plan:
        places = [name] if name in (".gitignore", "CLAUDE.md") else [name, "methodology/" + name]
        found[name] = [p for p in places if (root / p).is_file()]
        for p in found[name]:
            old = (root / p).read_text(encoding="utf-8")
            try:
                new, n = fn(old)
            except ValueError:
                continue
            if n:
                diff = "".join(difflib.unified_diff(old.splitlines(keepends=True), new.splitlines(keepends=True),
                                                    fromfile=p, tofile=p))
                out.append({"path": p, "new": new, "replacements": n, "diff": diff})
    return out, found


def checks(ml, root, ledger):
    return ml.run_checks(root, [], ledger)


def main(argv):
    if argv[1:2] == ["checks"] and len(argv) == 5:
        ml = load_tool()
        before = json.loads(Path(argv[4]).read_text())["checks_before"]
        after = checks(ml, Path(argv[2]).resolve(), DEST)
        Path(argv[3]).write_text(json.dumps({"checks_before": before, "checks_after": after,
                                             "differences": ml.check_differences(before, after)}, indent=1))
        print("checks", argv[2], "differences:", ml.check_differences(before, after))
        return 0
    if len(argv) != 4 or argv[1] not in ("scan", "move"):
        print(__doc__)
        return 2
    mode, root, outp = argv[1], Path(argv[2]).resolve(), Path(argv[3])
    ml = load_tool()
    kind, directory, _found = ml.resolve_layout(root)
    report = {"mode": mode, "project": str(root), "layout": kind, "file_bytes": (root / SRC).stat().st_size if (root / SRC).is_file() else None,
              "tracked": SRC in ml.tracked_files(root)}
    moves = [{"src": SRC, "dest": DEST, "kind": "manifest", "tracked": report["tracked"]}]
    mapping = ml.logical_map(moves, "1")
    report["mapping"] = mapping
    dirty = ml.dirty_paths(root)
    report["dirty_before"] = dirty
    rewrites, found = rewrites_for(ml, root, mapping)
    report["configs_found"] = found
    report["rewrites"] = [{k: v for k, v in r.items() if k != "new"} for r in rewrites]
    if mode == "scan":
        class R:  # the shape scan_hits reads: .path, .new
            def __init__(self, d):
                self.path, self.new = d["path"], d["new"]
        report["scan_hits"] = ml.scan_hits(root, moves, [R(r) for r in rewrites], "1")
        report["checks_before"] = checks(ml, root, SRC)
    else:
        if dirty:
            report["refused"] = "dirty tree: " + " ".join(dirty)
            outp.write_text(json.dumps(report, indent=1))
            return 1
        report["checks_before"] = checks(ml, root, SRC)
        (root / "methodology").mkdir(exist_ok=True)
        r = ml.run(root, "mv", SRC, DEST)
        report["git_mv"] = {"exit": r.returncode, "err": r.stderr.strip()}
        if r.returncode != 0:
            outp.write_text(json.dumps(report, indent=1))
            return 1
        for rw in rewrites:
            (root / rw["path"]).write_text(rw["new"], encoding="utf-8")
        report["checks_after"] = checks(ml, root, DEST)
        report["differences"] = ml.check_differences(report["checks_before"], report["checks_after"])
    outp.write_text(json.dumps(report, indent=1))
    print("%s %s: layout %s, %s B, %d rewrite(s), configs %s" % (
        mode, root.name, kind, report["file_bytes"], len(rewrites), found))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
