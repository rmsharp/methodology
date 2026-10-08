#!/usr/bin/env python3
"""BL-101 P10 evidence: what the expand stage does to an adopter that only SYNCS, over the 12 adopters in --no-local CLONES.

Plan: docs/planning/methodology-subdirectory-plan.md section 7 row P10 and section 5A.2. The plan's claim (section 8) is that "the
expand release changes no adopter that does not run the tool". This script measures it as a differential. For each adopter it makes
two clones of the adopter's committed HEAD and syncs one from the BASE (the commit before the first BL-101 commit) and the other from
the CANDIDATE (the sha adopters may sync from), each with the `bin/sync` of its own commit and the flags an adopter would type
(`bin/sync <project>`, then --force only if that refuses, and says so). It then compares the two synced trees, so what differs is
exactly what the expand stage changes for an adopter and nothing older (every adopter is behind on something):

  * the PATH set: no file added, removed or renamed, nothing under methodology/ (layout unchanged);
  * the candidate-synced tree: bin/status reads layout `legacy` and every TRACKED file `current`; bin/check-links --tree exit code
    in both trees; the project's own dashboard health and ratchet line in both (run in a COPY, so their writes dirty nothing).

Nothing in a real adopter is read through its working directory, written or run: only clones are touched. Run it from the repository
root (a temporary directory holds the clones and is removed at the end):

    python3 docs/planning/methodology-subdirectory-evidence/p10-sync-12-adopters.py --base <sha> --cand <sha> [--only NAME ...] [--out DIR]
"""
import argparse
import importlib.util
import json
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("p7", HERE / "migrate-12-adopters.py")
p7 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p7)
sh, git, ADOPTERS, DEV, REPO, TRAILER = p7.sh, p7.git, p7.ADOPTERS, p7.DEV, p7.REPO, p7.TRAILER
NO_HOOKS = ["-c", "core.hooksPath=/dev/null"]


def make_source(sha, dest):
    """A clone of THIS repository checked out at `sha`: the tool and the files an adopter at that sha would sync from."""
    code, out = sh(["git", "clone", "-q", "--no-local", str(REPO), str(dest)])
    if code != 0:
        raise SystemExit("clone failed: " + out[-200:])
    code, out = git(dest, "checkout", "-q", "--detach", sha)
    if code != 0:
        raise SystemExit("checkout %s failed: %s" % (sha, out[-200:]))
    return dest


def sync_clone(name, tag, source, work):
    """Clone adopter `name`, sync it from `source` and commit. Returns (clone path, info dict)."""
    clone = work / ("%s-%s" % (name, tag))
    code, out = sh(["git", "clone", "-q", "--no-local", str(DEV / name), str(clone)])
    if code != 0:
        return None, {"error": "clone failed: " + out.strip()[-160:]}
    git(clone, "config", "user.email", "evidence@example.com")
    git(clone, "config", "user.name", "P10 evidence")
    info = {"forced": False}
    c1, o1 = sh([sys.executable, "-B", str(source / "bin" / "sync"), str(clone)])
    if c1 != 0:
        c1, o1 = sh([sys.executable, "-B", str(source / "bin" / "sync"), str(clone), "--force"])
        info["forced"] = True
    info["sync_exit"] = c1
    if c1 != 0:
        info["error"] = "sync failed: " + " ".join(o1.split())[-200:]
        return clone, info
    git(clone, "add", "-A")
    cc, co = git(clone, *NO_HOOKS, "commit", "-q", "-m", "sync from %s\n\n%s" % (tag, TRAILER))
    info["committed"] = cc == 0
    info["files"] = len(git(clone, "diff", "--name-only", "HEAD~1", "HEAD")[1].split()) if cc == 0 else 0
    return clone, info


def layout_of(clone, status_tool):
    code, out = sh([sys.executable, "-B", str(status_tool), str(clone)])
    m = re.search(r"^layout:\s+\S+\s+(\S+)", out, re.M)
    return m.group(1) if m else "unreadable (exit %s)" % code


def links_exit(clone, tool):
    code, out = sh([sys.executable, "-B", str(tool), "--tree", str(clone)])
    return code


def own_tools(clone, work, tag):
    """The project's own dashboard health and ratchet line, in a COPY of the tree."""
    cp = work / ("copy-%s-%s" % (clone.name, tag))
    shutil.copytree(clone, cp, symlinks=True)
    health = p7.dashboard_health(cp)
    ratchet = p7.ratchet_line(cp)
    shutil.rmtree(cp, ignore_errors=True)
    return health, ratchet


def run_one(name, work, base_src, cand_src, tamper=False):
    row = {"adopter": name}
    t0 = time.time()
    a, ia = sync_clone(name, "base", base_src, work)
    b, ib = sync_clone(name, "cand", cand_src, work)
    if tamper and b is not None and "error" not in ib:  # the negative control: the verdict must be able to fail
        (b / "methodology").mkdir(exist_ok=True)
        git(b, "mv", "SAFEGUARDS.md", "methodology/SAFEGUARDS.md")
        git(b, *NO_HOOKS, "commit", "-q", "-m", "negative control: one file moved under methodology/")
    row["base_sync"] = ia.get("error") or "exit %s%s, %s files" % (ia["sync_exit"], " with --force" if ia["forced"] else "", ia.get("files"))
    row["cand_sync"] = ib.get("error") or "exit %s%s, %s files" % (ib["sync_exit"], " with --force" if ib["forced"] else "", ib.get("files"))
    if a is None or b is None or "error" in ia or "error" in ib:
        row["verdict"] = "NOT MEASURED (a sync did not complete)"
        return row
    # the differential: fetch the base-synced commit into the candidate-synced clone and diff the two trees
    git(b, "fetch", "-q", str(a), "HEAD")
    code, ns = git(b, "diff", "--name-status", "FETCH_HEAD", "HEAD")
    changes = [x.split("\t") for x in ns.strip().splitlines() if x.strip()]
    kinds = {}
    for c in changes:
        kinds[c[0][0]] = kinds.get(c[0][0], 0) + 1
    row["files_differing"] = len(changes)
    row["added_removed_renamed"] = "%d / %d / %d" % (kinds.get("A", 0), kinds.get("D", 0), kinds.get("R", 0))
    tree_b = set(git(b, "ls-files")[1].split("\n")) - {""}
    tree_a = set(git(a, "ls-files")[1].split("\n")) - {""}
    row["under_methodology"] = sum(1 for p in tree_b if p.startswith("methodology/"))
    row["path_sets"] = "identical" if tree_a == tree_b else "DIFFER: +%s -%s" % (sorted(tree_b - tree_a)[:3], sorted(tree_a - tree_b)[:3])
    row["lines"] = " ".join(git(b, "diff", "--shortstat", "FETCH_HEAD", "HEAD")[1].split()) or "no difference"
    row["changed"] = ", ".join(sorted(c[-1] for c in changes))
    # the candidate-synced tree, read with the candidate's tools
    status_tool = cand_src / "bin" / "status"
    row["layout_after"] = layout_of(b, status_tool)
    p7.REPO = cand_src
    tracked, bad, bad_rows = p7.status_counts(b)
    row["status_after"] = "%s tracked, %s not current%s" % (tracked, bad, (": " + ", ".join(bad_rows[:3])) if bad else "")
    row["links_base_cand"] = "exit %s / exit %s" % (links_exit(a, cand_src / "bin" / "check-links"), links_exit(b, cand_src / "bin" / "check-links"))
    row["health_base_cand"] = "%s / %s" % (own_tools(a, work, "base")[0], own_tools(b, work, "cand")[0])
    ra, rb = own_tools(a, work, "base2")[1], own_tools(b, work, "cand2")[1]
    row["ratchet_base"], row["ratchet_cand"] = ra, rb
    ok = (row["path_sets"] == "identical" and row["under_methodology"] == 0 and row["layout_after"] == "legacy" and bad == 0)
    row["verdict"] = "layout unchanged, paths identical, all current" if ok else "CHECK ROW"
    row["seconds"] = int(time.time() - t0)
    return row


COLUMNS = ["adopter", "base_sync", "cand_sync", "files_differing", "added_removed_renamed", "path_sets", "under_methodology",
           "lines", "layout_after", "status_after", "links_base_cand", "health_base_cand", "ratchet_base", "ratchet_cand",
           "verdict", "seconds"]


def table(rows):
    out = ["| " + " | ".join(COLUMNS) + " |", "|" + "---|" * len(COLUMNS)]
    for r in rows:
        out.append("| " + " | ".join(str(r.get(k, "MISSING")).replace("|", "/") for k in COLUMNS) + " |")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--base", required=True, help="the commit before the first BL-101 commit (a sha)")
    ap.add_argument("--cand", required=True, help="the sha adopters may sync from")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--out", default=str(HERE / "p10-adopter-runs"))
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--tamper", action="store_true", help="negative control: move one file under methodology/ in the candidate-synced clone, "
                                                          "so the verdict must read CHECK ROW")
    args = ap.parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    if args.resume and (out_dir / "rows.json").is_file():
        rows = json.loads((out_dir / "rows.json").read_text(encoding="utf-8"))
    done = {r["adopter"] for r in rows}
    with tempfile.TemporaryDirectory(prefix="p10-clones-") as tmp:
        work = Path(tmp)
        base_src = make_source(args.base, work / "src-base")
        cand_src = make_source(args.cand, work / "src-cand")
        shas = {"base": git(base_src, "rev-parse", "HEAD")[1].strip(), "cand": git(cand_src, "rev-parse", "HEAD")[1].strip()}
        print("base", shas["base"], "cand", shas["cand"], flush=True)
        for name in args.only or ADOPTERS:
            if name in done:
                continue
            print("== %s" % name, flush=True)
            try:
                row = run_one(name, work, base_src, cand_src, args.tamper)
            except Exception as e:  # noqa: BLE001 -- one adopter's failure is a row, not the end of the run
                row = {"adopter": name, "verdict": "SCRIPT ERROR: %r" % (e,)}
            rows.append(row)
            print(json.dumps(row), flush=True)
            (out_dir / "rows.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
            for tag in ("base", "cand"):
                shutil.rmtree(work / ("%s-%s" % (name, tag)), ignore_errors=True)
        order = {n: i for i, n in enumerate(ADOPTERS)}
        rows.sort(key=lambda r: order.get(r["adopter"], 99))
        md = "base `%s`, candidate `%s`\n\n%s\n" % (shas["base"], shas["cand"], table(rows))
        (out_dir / "summary.md").write_text(md, encoding="utf-8")
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
