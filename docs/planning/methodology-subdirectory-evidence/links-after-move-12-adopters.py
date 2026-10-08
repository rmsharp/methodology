#!/usr/bin/env python3
"""BL-101 S284 evidence: which links dangle after bin/migrate-layout moves a project, over the 12 adopters in --no-local CLONES.

The question (the S282 carry): bin/migrate-layout reports its check-links cell and does not judge it ('informational until
P9'). P9 is done, so should a change in that cell count as a difference? That depends on WHAT dangles after a move: a
distributed framework document (a defect the tool or the documents own) or a link in a file the project owns (its ledger's
old entries, which the tool never edits). This script measures it. For each adopter it
  1. clones the adopter's committed HEAD (nothing in a real tree is read through its working directory, written or run),
  2. syncs the clone from the CANDIDATE sha with that sha's own bin/sync (--force only if that refuses, and says so) and commits,
  3. runs that sha's bin/check-links --tree (BEFORE: legacy layout) and keeps every dangling link,
  4. runs that sha's bin/migrate-layout --apply --skip-checks, then check-links again (AFTER: new layout),
and sorts every dangling link by the manifest's disposition of the file it sits in: `tracked` (a framework document the project
receives byte for byte) or `seed` (a ledger or notes file the project then owns). Hooks are off in the clones (as in the P10
differential): an adopter's own hook is a separate question, answered by P11.

    python3 docs/planning/methodology-subdirectory-evidence/links-after-move-12-adopters.py --cand <sha> [--only NAME ...] [--out DIR]
"""
import argparse
import importlib.util
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("p10", HERE / "p10-sync-12-adopters.py")
p10 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p10)
sh, git, ADOPTERS, TRAILER = p10.sh, p10.git, p10.ADOPTERS, p10.TRAILER
FAIL_LINE = re.compile(r"^\s+(\S+):(\d+)\s+->\s+(.*?)\s*$")


def dispositions(source):
    """{path in either layout: (disposition, source path)} from the manifest of the candidate checkout."""
    spec = importlib.util.spec_from_file_location("_manifest_cand", source / "bin" / "_manifest.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    out = {}
    for src, dest, disp in m.DISTRIBUTION:
        out[dest] = (disp, src)
        out[m.NEW_LAYOUT[src]] = (disp, src)
    return out


def dangling(clone, source, table):
    """(exit code, [(file, line, target, disposition)]) from the candidate's check-links --tree over the clone."""
    code, out = sh([sys.executable, "-B", str(source / "bin" / "check-links"), "--tree", str(clone)])
    rows = []
    for line in out.splitlines():
        m = FAIL_LINE.match(line)
        if m:
            rows.append((m.group(1), int(m.group(2)), m.group(3), table.get(m.group(1), ("unlisted", ""))[0]))
    return code, rows


def tally(rows):
    t = {}
    for _f, _n, _t, disp in rows:
        t[disp] = t.get(disp, 0) + 1
    return t


def run_one(name, work, source, table):
    row = {"adopter": name}
    clone, info = p10.sync_clone(name, "cand", source, work)
    row["sync"] = ("FAILED: " + info.get("error", "?")) if "error" in info else ("committed with --force" if info["forced"] else "committed")
    if clone is None or "error" in info:
        return row
    b_code, b_rows = dangling(clone, source, table)
    code, out = sh([sys.executable, "-B", str(source / "bin" / "migrate-layout"), str(clone), "--apply", "--skip-checks", "--json",
                    "--trailer", TRAILER], timeout=3600)
    try:
        rep = json.loads(out)
    except ValueError:
        rep = {"status": "unparseable", "raw": out[-300:]}
    row["apply"] = "%s (exit %s)" % (rep.get("status"), code)
    row["refusals"] = "; ".join("%s" % r["code"] for r in rep.get("refusals", [])) or "none"
    row["before_exit"] = b_code
    row["before"] = tally(b_rows)
    if rep.get("status") != "applied":
        row["after_exit"], row["after"], row["after_where"] = "-", {}, "not migrated"
        return row
    a_code, a_rows = dangling(clone, source, table)
    row["after_exit"] = a_code
    row["after"] = tally(a_rows)
    per_file = {}
    for f, _n, _t, disp in a_rows:
        per_file.setdefault("%s [%s]" % (f, disp), 0)
        per_file["%s [%s]" % (f, disp)] += 1
    row["after_where"] = ", ".join("%s x%d" % kv for kv in sorted(per_file.items())) or "none"
    row["after_targets"] = sorted({t for _f, _n, t, disp in a_rows if disp == "tracked"})[:6]
    return row


COLUMNS = [("adopter", "adopter"), ("sync", "sync"), ("apply", "apply"), ("refusals", "refusals"),
           ("before_exit", "links before (exit)"), ("before", "dangling before"), ("after_exit", "links after (exit)"),
           ("after", "dangling after, by disposition"), ("after_where", "where"), ("after_targets", "tracked targets")]


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--cand", required=True, help="the sha of this repository whose bin/ tools and files are used")
    p.add_argument("--only", nargs="*", help="adopter names (default: all twelve)")
    p.add_argument("--out", default=str(HERE / "links-after-move-runs"))
    args = p.parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    names = args.only or ADOPTERS
    with tempfile.TemporaryDirectory(prefix="links-after-move-") as td:
        work = Path(td)
        source = p10.make_source(args.cand, work / "cand-source")
        table = dispositions(source)
        rows = []
        for name in names:
            print("== %s" % name, flush=True)
            try:
                row = run_one(name, work, source, table)
            except Exception as e:  # noqa: BLE001 -- one adopter's failure is a row, not the end of the run
                row = {"adopter": name, "apply": "SCRIPT ERROR: %r" % (e,)}
            rows.append(row)
            print(json.dumps(row), flush=True)
            shutil.rmtree(work / (name + "-cand"), ignore_errors=True)
    (out_dir / "rows.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
    md = ["| " + " | ".join(h for _k, h in COLUMNS) + " |", "|" + "---|" * len(COLUMNS)]
    for r in rows:
        md.append("| " + " | ".join(str(r.get(k, "MISSING")).replace("|", "/") for k, _h in COLUMNS) + " |")
    (out_dir / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
