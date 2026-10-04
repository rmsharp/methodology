#!/usr/bin/env python3
"""Keep the saved runs of the documentation study (plan docs/planning/documentation-quality-experiment-plan.md, section 5 P1a (a)).

    python3 doc_evidence.py build  OUTDIR [--project PATH]   # needs the run trees; they are in /tmp and die at reboot
    python3 doc_evidence.py verify OUTDIR [--project PATH]   # needs only OUTDIR and the project repository

`build` fetches every saved run's HEAD from its tree into a scratch repository, adds a pin ref where the run went on past its
first close-out, and writes ONE git bundle (`runs.bundle`: refs/runs/<id> and refs/pins/<id>) plus `manifest.json`. The bundle's
prerequisites are the project's own start commits (`879503cce`, `402a6b5b7`), which are in the project repository, so every sha a
run's record cites survives; the install commit the harness makes is NOT in the project repository, which is why the range cannot
begin there. `verify` proves the bundle against the project repository, rebuilds every run's head and pin from it, and checks them
against the manifest. Nothing here reads a score. Python 3 stdlib only.
"""
import argparse, hashlib, json, os, re, subprocess, sys, tempfile
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
PILOT = os.path.join(HERE, "pilot")
DEFAULT_PROJECT = os.path.expanduser("~/Development/nprcgenekeepr")
START_BASE = "879503cce"      # the S237 and T-control start state (plan 3.2)
START_REMOVE = "402a6b5b7"    # the ratchet study's T-remove start state
# (set name, rows file under pilot/, project start commit)
SETS = [
    ("real-3.7", "real-3.7/rows.jsonl", START_BASE),
    ("t-control", "ratchet-control-t-control/rows.jsonl", START_BASE),
    ("t-control-fix", "ratchet-control-t-control-reply-fix/rows.jsonl", START_BASE),
    ("t-remove", "ratchet-main-t-remove/rows.jsonl", START_REMOVE),
]
# Plan 2.5: the pin is the first close-out commit. Every run ends at it except these three, which went on past it. The first two
# are named in held_out.RUNS; the third is S555's close-out in R0 rep 5, which also holds S556 (plan section 10 row 5).
PIN_OVERRIDES = {
    "real-3.7/v3.7-r2": "7b9bd618",
    "real-3.7/v3.0-r3": "b15ae1c5",
    "t-remove/R0-r5": "3aa6c2b9",
}
INSTALL_AUTHOR, INSTALL_SUBJECT = "Fixture", "Install methodology arm"


def git(repo, *a, check=True):
    p = subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True)
    if check and p.returncode != 0:
        raise SystemExit(f"git {' '.join(a)} failed in {repo}: {p.stderr.strip()}")
    return p.stdout.strip()


def is_ancestor(repo, a, b):
    return subprocess.run(["git", "-C", repo, "merge-base", "--is-ancestor", a, b]).returncode == 0


def run_id(set_name, arm, rep):
    return f"{set_name}/{arm}-r{rep}"


def tree_for(set_name, row):
    ratchet = row.get("ratchet")
    if isinstance(ratchet, dict) and ratchet.get("tree"):
        return ratchet["tree"]
    return f"/tmp/overhead-real/{row['arm']}-r{row['rep']}"       # S237's rows carry no tree path


def transcript_for(row):
    t = row.get("transcript") or ""
    return t if os.path.isabs(t) else os.path.join(HERE, t) if t else ""


def cli_versions(path):
    """Every distinct Claude Code version a transcript records, in order of first appearance."""
    seen = []
    if path and os.path.isfile(path):
        for line in open(path, errors="replace"):
            m = re.search(r'"version"\s*:\s*"(\d+\.\d+\.\d+)"', line)
            if m and m.group(1) not in seen:
                seen.append(m.group(1))
    return seen


def install_commit(tree, start):
    """The harness's own commit: first by author `Fixture` with the install subject, after the project's start commit."""
    for line in git(tree, "log", "--reverse", "--format=%H%x1f%an%x1f%s", f"{start}..HEAD").splitlines():
        h, author, subject = line.split("\x1f", 2)
        if author == INSTALL_AUTHOR and subject.startswith(INSTALL_SUBJECT):
            return h
    return None


def runs():
    out = []
    for set_name, rel, start in SETS:
        for row in map(json.loads, open(os.path.join(PILOT, rel))):
            out.append({"id": run_id(set_name, row["arm"], row["rep"]), "set": set_name, "arm": row["arm"], "rep": str(row["rep"]),
                        "start": start, "tree": tree_for(set_name, row), "transcript": transcript_for(row),
                        "row_end": row.get("end"), "row_complete": row.get("complete")})
    return out


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def describe(r, project):
    tree = r["tree"]
    if not os.path.isdir(tree):
        raise SystemExit(f"tree missing for {r['id']}: {tree} (the run trees are in /tmp; a reboot deletes them)")
    start = git(project, "rev-parse", r["start"])
    head = git(tree, "rev-parse", "HEAD")
    if not is_ancestor(tree, start, head):
        raise SystemExit(f"{r['id']}: project start {start} is not an ancestor of the tree's HEAD")
    pin = git(tree, "rev-parse", PIN_OVERRIDES[r["id"]]) if r["id"] in PIN_OVERRIDES else head
    if not is_ancestor(tree, pin, head):
        raise SystemExit(f"{r['id']}: pin {pin} is not an ancestor of HEAD")
    return {**r, "start": start, "head": head, "pin": pin, "pin_rule": "override" if r["id"] in PIN_OVERRIDES else "head",
            "install": install_commit(tree, start),
            "commits_after_start": int(git(tree, "rev-list", "--count", f"{start}..{head}")),
            "cli": cli_versions(r["transcript"])}


def build(outdir, project, run_list=None):
    os.makedirs(outdir, exist_ok=True)
    described = [describe(r, project) for r in (runs() if run_list is None else run_list)]
    scratch = tempfile.mkdtemp(prefix="doc-evidence-")
    git(scratch, "init", "-q")
    alt = os.path.join(scratch, ".git", "objects", "info", "alternates")
    with open(alt, "w") as f:
        f.write(os.path.join(git(project, "rev-parse", "--absolute-git-dir"), "objects") + "\n")
    for d in described:
        git(scratch, "fetch", "-q", "--no-tags", d["tree"], f"HEAD:refs/runs/{d['id']}")
        if d["pin"] != d["head"]:
            git(scratch, "update-ref", f"refs/pins/{d['id']}", d["pin"])
    starts = sorted({d["start"] for d in described})
    bundle = os.path.join(outdir, "runs.bundle")
    if os.path.exists(bundle):
        os.remove(bundle)
    git(scratch, "bundle", "create", bundle, "--all", *[f"^{s}" for s in starts])
    manifest = {"about": "BL-94 P1a (a): the saved runs of the documentation study. Rebuild with `doc_evidence.py verify`.",
                "bundle": {"file": "runs.bundle", "bytes": os.path.getsize(bundle), "sha256": sha256(bundle),
                           "prerequisites": starts, "refs": "refs/runs/<id> (HEAD of the run), refs/pins/<id> (only where the pin is not HEAD)"},
                "project": "nprcgenekeepr", "runs": [{k: v for k, v in d.items() if k != "tree"} | {"tree_was": d["tree"]} for d in described]}
    with open(os.path.join(outdir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1, sort_keys=True)
        f.write("\n")
    return manifest


def verify(outdir, project):
    """Exit non-zero (raise SystemExit) on any mismatch; return the list of run ids rebuilt."""
    manifest = json.load(open(os.path.join(outdir, "manifest.json")))
    bundle = os.path.join(outdir, manifest["bundle"]["file"])
    if sha256(bundle) != manifest["bundle"]["sha256"]:
        raise SystemExit("bundle sha256 differs from the manifest")
    p = subprocess.run(["git", "-C", project, "bundle", "verify", bundle], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"git bundle verify failed: {p.stderr.strip()}")
    scratch = tempfile.mkdtemp(prefix="doc-evidence-verify-")
    git(scratch, "init", "-q")
    with open(os.path.join(scratch, ".git", "objects", "info", "alternates"), "w") as f:
        f.write(os.path.join(git(project, "rev-parse", "--absolute-git-dir"), "objects") + "\n")
    git(scratch, "fetch", "-q", "--no-tags", bundle, "refs/runs/*:refs/runs/*", "refs/pins/*:refs/pins/*")
    rebuilt = []
    for r in manifest["runs"]:
        head = git(scratch, "rev-parse", f"refs/runs/{r['id']}")
        if head != r["head"]:
            raise SystemExit(f"{r['id']}: rebuilt head {head} != manifest {r['head']}")
        if git(scratch, "cat-file", "-t", r["pin"]) != "commit":
            raise SystemExit(f"{r['id']}: pin {r['pin']} was not rebuilt")
        if not is_ancestor(scratch, r["pin"], head):
            raise SystemExit(f"{r['id']}: pin is not an ancestor of the rebuilt head")
        rebuilt.append(r["id"])
    return rebuilt


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("mode", choices=["build", "verify"])
    ap.add_argument("outdir")
    ap.add_argument("--project", default=DEFAULT_PROJECT)
    a = ap.parse_args(argv)
    if a.mode == "build":
        m = build(a.outdir, a.project)
        print(f"built {len(m['runs'])} runs; bundle {m['bundle']['bytes']:,} B; sha256 {m['bundle']['sha256']}")
    else:
        ids = verify(a.outdir, a.project)
        print(f"verified: bundle verifies against the project and rebuilds {len(ids)} runs (head and pin each)")


if __name__ == "__main__":
    main()
