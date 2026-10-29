#!/usr/bin/env python3
"""PR3 evidence, re-run on the rebuilt candidate (S396): what the pull request candidate's bin/status and bin/sync do to the 12 adopters, against upstream's.

This is S326's `pr3-adopters.py`, unchanged in logic: only the default candidate ref, the output names and the report's
heading and header sentence differ (`diff pr3-adopters.py pr3b-adopters.py` shows all of it).

Plan: docs/planning/upstream-pr-composition-plan.md section 5, row PR3. Every adopter is a --no-local CLONE of its
committed HEAD (nothing in a real tree is read through the working directory, written or run). Two tools are run
over the same clones, each from its own clean clone:
  C  the candidate: the local ref `pr2b/candidate` (default), and
  U  upstream's tool: the tip of `upstream/main`.
Per adopter, in this order:
  1. bin/status, then `bin/sync --dry-run`, then `bin/sync --dry-run --force`, each tool, on the pristine clone (a dry run
     must write nothing: the clone is checked clean after each);
  2. a REAL sync, each tool, in its own copy of the clone: plain first, and with --force only if the plain run refused;
     the write set is read from `git status --porcelain`, never from the tool's own report; every seed's blob is hashed
     before and after; the result is committed under the adopter's own hooks (armed as in the real clone) and a refusal
     is recorded, then the commit is redone with --no-verify;
  3. the refused files are classified by where the adopter's blob is found: upstream's history, the candidate's
     history, the fork's history (a blob only the fork has is a fork version, not an edit of the adopter's);
  4. the tool's decision is audited against that classification (a refusal must be exactly a blob in neither
     history of the source and not the current canonical one).
Then two legacy FIXTURES (an empty project; a project holding upstream's current files with seeds the adopter owns),
synced by each tool, trees diffed. Run from the repository root, serially:

    python3 docs/planning/pr-composition-evidence/pr3b-adopters.py [--only NAME ...] [--work DIR] [--out DIR]

Nothing it writes leaves --work except --out (a markdown report and rows.json).
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True

REPO = Path(__file__).resolve().parents[3]
DEV = Path.home() / "Development"
ADOPTERS = ["model_project_constructor", "feedback-loop-comparison", "nprcgenekeepr", "mts-system", "vscode_quarto_ext",
            "Philippians", "airqino", "chat_verification", "church_growth", "dalia_martinez_funeral", "claude_work", "wsfct"]
ANSI = re.compile(r"\x1b\[[0-9;]*m")
TRAILER = "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
SEEDS_LEGACY = ["SESSION_NOTES.md", "CHANGELOG.md", "HANDOFFS.md", "ROADMAP.md", ".context-budget.json", ".quality-gates.json",
                ".gitattributes"]


def sh(args, cwd=None, timeout=900):
    """(exit code, output); 'timeout' or 'error' is a cell, not a crash."""
    try:
        r = subprocess.run(args, cwd=str(cwd) if cwd else None, capture_output=True, text=True, timeout=timeout)
        return r.returncode, ANSI.sub("", r.stdout + r.stderr)
    except subprocess.TimeoutExpired:
        return "timeout", ""
    except OSError as e:
        return "error", str(e)


def git(repo, *args, timeout=600):
    return sh(["git", "-C", str(repo), "-c", "commit.gpgsign=false", *args], timeout=timeout)


def blob_of(path):
    """git blob sha of a file's bytes, or None where there is no file."""
    p = Path(path)
    if not p.is_file():
        return None
    data = p.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def history_blobs(repo, ref_args, path):
    """The set of blob shas `path` has had at any commit reachable from ref_args (the default walk; a file
    deleted and re-added counts at each commit that holds it)."""
    code, out = git(repo, "log", "--format=%H", *ref_args, "--", path)
    shas = out.split() if code == 0 else []
    if not shas:
        return set()
    spec = "\n".join("%s:%s" % (s, path) for s in shas) + "\n"
    r = subprocess.run(["git", "-C", str(repo), "cat-file", "--batch-check"], input=spec, capture_output=True, text=True)
    return {line.split()[0] for line in r.stdout.splitlines() if len(line.split()) == 3 and line.split()[1] == "blob"}


def parse_status(out):
    """(layout kind or None, rows [(file, disposition, status)])."""
    lines = out.splitlines()
    layout = None
    for line in lines:
        m = re.match(r"^layout:\s+\S+\s+(\w+)", line)
        if m:
            layout = m.group(1)
    head = next((i for i, line in enumerate(lines) if line.startswith("Project ")), None)
    if head is None:
        return layout, []
    h = lines[head]
    c1, c2, c3 = h.index("File"), h.index("Disposition"), h.index("Status")
    rows = []
    for line in lines[head + 1:]:
        if not line.strip():
            break
        rows.append((line[c1:c2].strip(), line[c2:c3].strip(), line[c3:].strip()))
    return layout, rows


def status_counts(rows):
    c = {"current": 0, "behind": 0, "modified": 0, "missing": 0, "other": 0, "seed_present": 0, "seed_absent": 0}
    for _f, disp, st in rows:
        if disp == "seed":
            c["seed_present" if st == "present" else "seed_absent"] += 1
        elif st == "current":
            c["current"] += 1
        elif re.match(r"\d+ versions? behind", st):
            c["behind"] += 1
        elif st == "locally modified":
            c["modified"] += 1
        elif st == "missing":
            c["missing"] += 1
        else:
            c["other"] += 1
    return c


def parse_sync(out):
    """The sync report: layout line, per-file (dest, phrase) rows, the refused list and the diff pairs."""
    res = {"layout": None, "files": [], "refused": [], "diffs": [], "version": None}
    lines = out.splitlines()
    in_files = False
    in_refused = False
    for line in lines:
        m = re.match(r"^\s+layout:\s+(.*)$", line)
        if m:
            res["layout"] = m.group(1).strip()
        m = re.match(r"^\s+version:\s+(.*)$", line)
        if m:
            res["version"] = m.group(1).strip()
        if line.strip() == "files:":
            in_files, in_refused = True, False
            continue
        if "would be overwritten:" in line:
            in_refused, in_files = True, False
            continue
        if in_refused:
            if not line.strip():
                in_refused = False
            else:
                res["refused"].append(line.strip())
            continue
        m = re.match(r"^\s+diff (\S+) (\S+)$", line)
        if m:
            res["diffs"].append((m.group(1), m.group(2)))
            continue
        if in_files:
            m = re.match(r"^\s{4}(\S.*?): (.+)$", line)
            if m:
                res["files"].append((m.group(1), m.group(2).strip()))
    return res


def phrase_class(p):
    if p.startswith("would write") or p.startswith("wrote") or p.startswith("written") or p.startswith("created"):
        return "write"
    if p.startswith("would create"):
        return "create"
    if p.startswith("unchanged") or p.startswith("up to date") or p.startswith("current"):
        return "unchanged"
    if p.startswith("present (seed"):
        return "seed-left"
    if p.startswith("not created"):
        return "seed-not-created"
    return "other: " + p


def clean(repo):
    r = subprocess.run(["git", "-C", str(repo), "status", "--porcelain", "--untracked-files=all"], capture_output=True, text=True)
    return r.returncode == 0 and not r.stdout.strip()


def porcelain_paths(repo):
    """Every path git sees as changed or new (untracked files listed one by one)."""
    r = subprocess.run(["git", "-C", str(repo), "status", "--porcelain", "--untracked-files=all"], capture_output=True, text=True)
    paths = []
    for line in r.stdout.splitlines():
        if len(line) > 3:
            paths.append(line[3:].strip().strip('"'))
    return sorted(paths)


def arm_hooks(src, clone):
    code, hp = sh(["git", "-C", str(src), "config", "--get", "core.hooksPath"])
    if code == 0 and hp.strip():
        git(clone, "config", "core.hooksPath", hp.strip())
        return "armed: " + hp.strip()
    return "none"


def set_identity(clone):
    git(clone, "config", "user.email", "evidence@example.com")
    git(clone, "config", "user.name", "PR3 evidence")


def tool(root, name):
    return [sys.executable, "-B", str(Path(root) / "bin" / name)]


def run_tool_views(root, project):
    """status, dry run, dry run --force of one tool over a pristine clone; the clone is checked clean after each."""
    r = {}
    code, out = sh(tool(root, "status") + [str(project)])
    layout, rows = parse_status(out)
    r["status_exit"] = code
    r["layout"] = layout
    r["status_rows"] = rows
    r["status_counts"] = status_counts(rows)
    for key, extra in (("dry", ["--dry-run"]), ("dry_force", ["--dry-run", "--force"])):
        code, out = sh(tool(root, "sync") + [str(project)] + extra)
        p = parse_sync(out)
        p["exit"] = code
        p["tail"] = out.strip()[-400:] if code != 0 and not p["refused"] else ""
        p["raw"] = out
        p["clean_after"] = clean(project)
        p["phrases"] = {}
        for _d, ph in p["files"]:
            k = phrase_class(ph)
            p["phrases"][k] = p["phrases"].get(k, 0) + 1
        r[key] = p
    return r


def sync_in_place(root, dst):
    """One tool's real sync of `dst`: plain first, --force only if the plain run refused. The write set is
    `git status --porcelain`, never the tool's own report; every seed's blob is hashed before and after."""
    _l, rows = parse_status(sh(tool(root, "status") + [str(dst)])[1])
    seeds = [f for f, disp, _ in rows if disp == "seed"]
    before = {sd: blob_of(dst / sd) for sd in seeds}
    res = {"forced": False}
    code, out = sh(tool(root, "sync") + [str(dst)])
    if code != 0:
        res["plain_exit"] = code
        res["plain_refused"] = parse_sync(out)["refused"]
        res["plain_tail"] = out.strip()[-300:]
        code, out = sh(tool(root, "sync") + [str(dst), "--force"])
        res["forced"] = True
    res["exit"] = code
    res["layout"] = parse_sync(out)["layout"]
    res["written"] = porcelain_paths(dst)
    after = {sd: blob_of(dst / sd) for sd in seeds}
    res["seeds_before_present"] = sorted(sd for sd in seeds if before[sd])
    res["seeds_changed"] = sorted(sd for sd in seeds if before[sd] and after[sd] != before[sd])
    res["seeds_created"] = sorted(sd for sd in seeds if not before[sd] and after[sd])
    res["blobs"] = {q: blob_of(dst / q) for q in res["written"] if (dst / q).is_file()}
    return res


def commit_all(dst, trailer=True):
    """Commit what the sync wrote under the project's own hooks; a refusal is recorded and the commit redone with
    --no-verify. Returns the note."""
    if not porcelain_paths(dst):
        return "nothing to commit"
    git(dst, "add", "-A")
    msg = "sync the methodology files (PR3 evidence)\n\n" + TRAILER
    cc, co = git(dst, "commit", "-q", "-m", msg)
    if cc == 0:
        return "ok"
    note = "its own hook refused: " + " ".join(co.split())[-420:]
    cc, co = git(dst, "commit", "-q", "--no-verify", "-m", msg)
    if cc != 0:
        note += " | --no-verify also failed: " + " ".join(co.split())[-80:]
    return note


def real_sync(tag, root, base, work, src_real, name):
    """A real sync of one tool in its own copy of the pristine clone."""
    dst = work / (name + "-real-" + tag)
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(base, dst, symlinks=True)
    set_identity(dst)
    hooks = arm_hooks(src_real, dst) if src_real else "none"
    res = sync_in_place(root, dst)
    res["hooks"] = hooks
    res["commit"] = commit_all(dst)
    if res["written"]:
        code, out = sh(tool(root, "sync") + [str(dst)])
        res["again_exit"] = code
        res["again_written"] = porcelain_paths(dst)
    res["tree"] = str(dst)
    return res


def classify_refused(refused_diffs, project, cand, up, fork_heads):
    """For each (adopter file, canonical file in the candidate clone) the adopter's blob and where it is found."""
    out = []
    for adopter_path, canon_path in refused_diffs:
        ap, cp = Path(adopter_path), Path(canon_path)
        try:
            rel_src = str(cp.relative_to(cand["dir"]))
        except ValueError:
            rel_src = None
        b = blob_of(ap)
        row = {"dest": str(ap.relative_to(project)) if str(ap).startswith(str(project)) else str(ap), "src": rel_src, "blob": b}
        row["adopter_commits"] = [x for x in git(project, "log", "-2", "--format=%h %ad %s", "--date=short", "--", row["dest"])[1].splitlines() if x]
        if rel_src:
            row["in_candidate"] = b in cand["hist"](rel_src)
            row["in_upstream"] = b in up["hist"](rel_src)
            row["in_fork"] = b in fork_heads(rel_src)
            row["is_candidate_current"] = b == blob_of(cp)
            if not (row["in_fork"] or row["in_candidate"] or row["in_upstream"]):
                import difflib
                tip = git(REPO, "show", "main:" + rel_src)[1].splitlines()
                mine = ap.read_text(errors="replace").splitlines()
                row["diff_lines_vs_fork_tip"] = sum(1 for l in difflib.unified_diff(tip, mine, lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---"))
                row["diff_lines_vs_candidate"] = sum(1 for l in difflib.unified_diff(cp.read_text(errors="replace").splitlines(), mine, lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---"))
        out.append(row)
    return out


def md_escape(s):
    return str(s).replace("|", "\\|")


def slim(r):
    """A row without the raw outputs and the clone paths: rows.json keeps the facts, not the transcripts."""
    if "C" not in r:
        return r
    out = {k: v for k, v in r.items() if k not in ("C", "U", "F", "real_C", "real_U")}
    for t in ("C", "U", "F"):
        v = r[t]
        out[t] = {"layout": v["layout"], "status_counts": v["status_counts"], "status_exit": v["status_exit"]}
        for k in ("dry", "dry_force"):
            d = v[k]
            out[t][k] = {kk: vv for kk, vv in d.items() if kk not in ("raw", "files", "diffs")}
            out[t][k]["would_write"] = sorted(f for f, ph in d["files"] if phrase_class(ph) == "write")
            out[t][k]["would_create"] = sorted(f for f, ph in d["files"] if phrase_class(ph) == "create")
    for t in ("real_C", "real_U"):
        out[t] = {kk: vv for kk, vv in r[t].items() if kk != "tree"}
    return out


def init_project(path):
    path.mkdir(parents=True)
    sh(["git", "init", "-q", str(path)])
    set_identity(path)
    (path / "README.md").write_text("a fixture project\n")
    git(path, "add", "-A")
    git(path, "commit", "-q", "-m", "init")


def tree_diff(a, b):
    c, o = sh(["diff", "-rq", "--exclude=.git", str(a), str(b)])
    return [line.replace(str(a), "A").replace(str(b), "B") for line in o.splitlines()]


def changed_sources(up_sha, cand_sha):
    """Basenames of the distributed source files that differ between upstream's tip and the candidate."""
    c, o = git(REPO, "diff", "--name-only", up_sha, cand_sha, "--", "starter-kit", "workstreams", "HOW_TO_USE.md",
               "ITERATIVE_METHODOLOGY.md", "FRAMEWORK_APPARATUS.md")
    return sorted({Path(x).name for x in o.split()})


def run_fixtures(work, cand_dir, up_dir, cand_sha, up_sha):
    """Two legacy fixtures, each synced by upstream's tool and by the candidate's, trees diffed."""
    fx = {"changed_sources": changed_sources(up_sha, cand_sha)}
    cs = {norm(x) for x in fx["changed_sources"]}
    # (a) an empty project: both tools install everything
    a_u, a_c = work / "fixture-a-upstream", work / "fixture-a-candidate"
    init_project(a_u)
    init_project(a_c)
    ra_u, ra_c = sync_in_place(up_dir, a_u), sync_in_place(cand_dir, a_c)
    for d in (a_u, a_c):
        commit_all(d)
    both = sorted(set(ra_u["written"]) & set(ra_c["written"]))
    fx["a"] = {
        "U": {k: v for k, v in ra_u.items() if k not in ("blobs",)},
        "C": {k: v for k, v in ra_c.items() if k not in ("blobs",)},
        "same_paths": sorted(ra_u["written"]) == sorted(ra_c["written"]),
        "only_U": sorted(set(ra_u["written"]) - set(ra_c["written"])),
        "only_C": sorted(set(ra_c["written"]) - set(ra_u["written"])),
        "content_differs": [q for q in both if ra_u["blobs"].get(q) != ra_c["blobs"].get(q)],
        "tree_diff": tree_diff(a_u, a_c),
        "methodology_dir_in_C": (a_c / "methodology").exists(),
    }
    fx["a"]["unexplained"] = [q for q in fx["a"]["content_differs"] if norm(Path(q).name) not in cs]
    fx["a"]["changed_sources_not_differing"] = sorted(cs - {norm(Path(q).name) for q in fx["a"]["content_differs"]})
    # (b) a project that holds upstream's current files, its seeds edited by the adopter
    b_base = work / "fixture-b-base"
    shutil.copytree(a_u, b_base, symlinks=True)
    set_identity(b_base)
    _l, rows = parse_status(sh(tool(up_dir, "status") + [str(b_base)])[1])
    seeds = [f for f, disp, _ in rows if disp == "seed" and (b_base / f).is_file()]
    for sd in seeds:
        edit_seed(b_base / sd)
    git(b_base, "add", "-A")
    git(b_base, "commit", "-q", "-m", "the adopter edits its seeds")
    b_u, b_c = work / "fixture-b-upstream", work / "fixture-b-candidate"
    for d in (b_u, b_c):
        shutil.copytree(b_base, d, symlinks=True)
        set_identity(d)
    seed_norm = {norm(Path(x).name) for x in seeds}
    cs_tracked, cs_seed = cs - seed_norm, cs & seed_norm
    rb_u, rb_c = sync_in_place(up_dir, b_u), sync_in_place(cand_dir, b_c)
    fx["b"] = {
        "seeds_edited": seeds,
        "U": {k: v for k, v in rb_u.items() if k not in ("blobs",)},
        "C": {k: v for k, v in rb_c.items() if k not in ("blobs",)},
        "C_written_not_a_changed_tracked_source": sorted(q for q in rb_c["written"] if norm(Path(q).name) not in cs_tracked),
        "changed_tracked_sources_not_written": sorted(cs_tracked - {norm(Path(q).name) for q in rb_c["written"]}),
        "changed_seed_sources_left_as_is": sorted(cs_seed - {norm(Path(q).name) for q in rb_c["written"]}),
        "tree_diff": tree_diff(b_u, b_c),
        "methodology_dir_in_C": (b_c / "methodology").exists(),
    }
    return fx


def norm(name):
    """A seed's installed name keeps a dot its source lacks (.quality-gates.json from quality-gates.json)."""
    return name.lstrip(".")


def edit_seed(path):
    """An adopter's own edit, valid in the seed's own syntax."""
    if path.name.endswith(".json"):
        d = json.loads(path.read_text() or "{}")
        d["_adopter_owned"] = "a sync must leave this key"
        path.write_text(json.dumps(d, indent=2) + "\n")
    elif path.name == ".gitattributes":
        with open(path, "a") as fh:
            fh.write("\n# adopter-owned edit: a sync must leave this line\n")
    else:
        with open(path, "a") as fh:
            fh.write("\n<!-- adopter-owned edit: a sync must leave this line -->\n")


def mark(b):
    return "yes" if b else "NO"


def build_report(data, seconds):
    L = []
    w = L.append
    w("# PR3, the adopters: what the candidate's `bin/status` and `bin/sync` do, against upstream's (S396, the rebuilt candidate)")
    w("")
    w("`pr3b-adopters.py` (`docs/planning/pr-composition-evidence/`), run once from this repository's root, %.0f s. The candidate is the local ref `pr2b/candidate` at `%s`, upstream's tool is `upstream/main` at `%s`, the fork's `main` was `%s`. Each of the 12 adopters is a `--no-local` clone of its committed HEAD; each tool runs from its own clean clone; nothing in a real tree is read through the working directory, written or run. The write set of a real sync is `git status --porcelain` in the clone, never the tool's own report." % (
        seconds, data["candidate"][:7], data["upstream"][:7], data["fork"][:7]))
    w("")
    ad = [r for r in data["adopters"] if "C" in r]
    w("## 1. The candidate's tool over each adopter")
    w("")
    w("| adopter | HEAD | layout | tracked files: current / behind / locally modified / missing | seeds present | `--dry-run` exit | files refused | refused: a fork version / in no history (a local edit) | `--dry-run --force` would write | real sync (forced?) wrote | dry run equals the real write set | seeds changed / created | a second plain sync after the commit: exit, paths written | its own hook on the commit |")
    w("|---|---|---|---|---|---|---:|---|---:|---:|---|---|---|---|")
    for r in ad:
        c, rc = r["C"], r["real_C"]
        sc = c["status_counts"]
        cl = r["refused_classified"]
        fork_only = sum(1 for x in cl if x.get("in_fork") and not x.get("in_candidate") and not x.get("in_upstream"))
        nowhere = sum(1 for x in cl if not x.get("in_fork") and not x.get("in_candidate") and not x.get("in_upstream"))
        dw = c["dry_force"]["would_write"] + c["dry_force"]["would_create"]
        eq = sorted(dw) == sorted(rc["written"])
        w("| %s | %s | %s | %d / %d / %d / %d | %d | %s | %d | %d: %s | %d | %d (%s) | %s | %d / %d | %s | %s |" % (
            r["adopter"], r["head"], c["layout"] or "legacy", sc["current"], sc["behind"], sc["modified"], sc["missing"], sc["seed_present"],
            c["dry"]["exit"], len(c["dry"]["refused"]), fork_only, nowhere, len(dw), len(rc["written"]),
            "forced" if rc["forced"] else "plain", "yes" if eq else "NO: " + md_escape(", ".join(sorted(set(dw) ^ set(rc["written"])))[:120]),
            len(rc["seeds_changed"]), len(rc["seeds_created"]), ("%s, %d" % (rc["again_exit"], len(rc["again_written"]))) if "again_exit" in rc else "n/a (nothing was written)",
            md_escape(rc["hooks"].replace(str(DEV) + "/", "") + ": " + rc["commit"])[:140]))
    w("")
    w("## 2. Upstream's tool over the same clones")
    w("")
    w("| adopter | candidate's layout | status rows: missing / locally modified / current / behind | `--dry-run` exit | would write | real sync (forced?) wrote | framework files it wrote outside `methodology/` of a migrated project (a second copy) | seeds changed / created (a seed it created beside the adopter's own) | a second plain sync after the commit: exit, paths written |")
    w("|---|---|---|---:|---:|---|---:|---|---|")
    for r in ad:
        u, ru, c = r["U"], r["real_U"], r["C"]
        sc = u["status_counts"]
        created = set(ru["seeds_created"])
        second = [q for q in ru["written"] if c["layout"] == "new" and not q.startswith("methodology/") and q not in created]
        w("| %s | %s | %d / %d / %d / %d | %s | %d | %d (%s) | %d | %d / %d | %s |" % (
            r["adopter"], c["layout"] or "legacy", sc["missing"], sc["modified"], sc["current"], sc["behind"], u["dry"]["exit"],
            len(u["dry"]["would_write"]), len(ru["written"]), "forced" if ru["forced"] else "plain", len(second),
            len(ru["seeds_changed"]), len(ru["seeds_created"]), ("%s, %d" % (ru["again_exit"], len(ru["again_written"]))) if "again_exit" in ru else "n/a"))
    w("")
    w("## 2b. The fork's own tip over the same clones (dry runs only)")
    w("")
    w("The fork's `bin/sync` is not the candidate's bytes (`%s` against `%s`), so this is the operator's own tool, not a control for the candidate's. The point is the exit code: the same clones, a tool whose source history holds the fork's versions." % (data["fork_sync_blob"][:7], data["candidate_sync_blob"][:7]))
    w("")
    w("| adopter | the fork tip's `--dry-run` exit | files it refuses | the candidate's refusals (for comparison) |")
    w("|---|---:|---|---:|")
    for r in ad:
        f = r["F"]["dry"]
        w("| %s | %s | %s | %d |" % (r["adopter"], f["exit"], md_escape(", ".join(f["refused"])) or "none", len(r["C"]["dry"]["refused"])))
    w("")
    w("## 3. Legacy adopters: the candidate's write set against upstream's")
    w("")
    w("| adopter | candidate wrote | upstream wrote | same paths | only the candidate | only upstream | same path, different bytes | paths in either column not explained by a changed source file |")
    w("|---|---:|---:|---|---|---|---:|---|")
    cs_norm = {norm(x) for x in data["fixtures"]["changed_sources"]}
    for r in ad:
        if r["C"]["layout"] == "new":
            continue
        wc, wu = set(r["real_C"]["written"]), set(r["real_U"]["written"])
        diff_bytes = [q for q in wc & wu if r["real_C"]["blobs"].get(q) != r["real_U"]["blobs"].get(q)]
        unexplained = sorted(q for q in (wc ^ wu) | set(diff_bytes) if norm(Path(q).name) not in cs_norm)
        w("| %s | %d | %d | %s | %d | %d | %d | %s |" % (r["adopter"], len(wc), len(wu), mark(wc == wu),
            len(wc - wu), len(wu - wc), len(diff_bytes), md_escape(", ".join(unexplained)) or "none"))
    w("")
    w("## 4. The refused files, one row each: where the adopter's blob is found")
    w("")
    w("| adopter | file | in upstream's history | in the candidate's | in the fork's | the candidate's current blob |")
    w("|---|---|---|---|---|---|")
    for r in ad:
        for x in r["refused_classified"]:
            w("| %s | `%s` | %s | %s | %s | %s |" % (r["adopter"], x["dest"], mark(x.get("in_upstream")), mark(x.get("in_candidate")), mark(x.get("in_fork")), mark(x.get("is_candidate_current"))))
    w("")
    w("In no history at all (a local edit of the adopter's):")
    w("")
    n_edit = 0
    for r in ad:
        for x in r["refused_classified"]:
            if not (x.get("in_fork") or x.get("in_candidate") or x.get("in_upstream")):
                n_edit += 1
                w("- %s `%s`: %s changed lines against the fork tip's copy, %s against the candidate's; the adopter's last commits on it: %s" % (
                    r["adopter"], x["dest"], x.get("diff_lines_vs_fork_tip"), x.get("diff_lines_vs_candidate"), "; ".join("`%s`" % c for c in x["adopter_commits"]) or "none"))
    if not n_edit:
        w("- none")
    w("")
    w("## 4b. Hooks: which adopters' own hook refused the sync commit, and what it said")
    w("")
    w("| adopter | the candidate's sync commit | upstream's sync commit |")
    w("|---|---|---|")
    for r in ad:
        if r["real_C"]["commit"] != "ok" or r["real_U"]["commit"] != "ok":
            w("| %s | %s | %s |" % (r["adopter"], md_escape(r["real_C"]["commit"]), md_escape(r["real_U"]["commit"])))
    w("")
    w("## 5. Instrument audits")
    w("")
    w("| adopter | dry runs left the clone clean (4 runs) | the tool's refusals equal the history rule (a blob in neither the candidate's history nor its current one) | the plain real run's refusal equals the dry run's |")
    w("|---|---|---|---|")
    for r in ad:
        clean4 = all(r[t][k]["clean_after"] for t in ("C", "U") for k in ("dry", "dry_force"))
        pr = r["real_C"].get("plain_refused")
        w("| %s | %s | %s | %s |" % (r["adopter"], mark(clean4), mark(r.get("audit_refusal_equals_rule")),
            "n/a (no refusal)" if pr is None else mark(sorted(pr) == sorted(r["C"]["dry"]["refused"]))))
    w("")
    fx = data["fixtures"]
    w("## 6. Two legacy fixtures, each synced by both tools, trees diffed")
    w("")
    w("Source files that differ between upstream's tip and the candidate (basenames, distributed set): %d: %s." % (len(fx["changed_sources"]), ", ".join(fx["changed_sources"])))
    w("")
    a = fx["a"]
    w("**(a) an empty project** (`git init` and one commit).")
    w("")
    w("| | upstream's tool | the candidate's tool |")
    w("|---|---:|---:|")
    w("| exit of the plain sync | %s | %s |" % (a["U"]["exit"], a["C"]["exit"]))
    w("| paths written | %d | %d |" % (len(a["U"]["written"]), len(a["C"]["written"])))
    w("| layout the tool reports | - | %s |" % (a["C"]["layout"],))
    w("| seeds created | %d | %d |" % (len(a["U"]["seeds_created"]), len(a["C"]["seeds_created"])))
    w("")
    w("Same list of paths: **%s**; only upstream's: %s; only the candidate's: %s; a `methodology/` directory in the candidate's tree: %s." % (mark(a["same_paths"]), a["only_U"] or "none", a["only_C"] or "none", "yes" if a["methodology_dir_in_C"] else "no"))
    w("Paths whose bytes differ: %d; of those, not explained by a changed source file: **%s**; changed source files whose installed copy does not differ: %s." % (len(a["content_differs"]), a["unexplained"] or "none", a["changed_sources_not_differing"] or "none"))
    w("")
    w("`diff -rq` of the two trees (%d lines):" % len(a["tree_diff"]))
    w("")
    w("```")
    for line in a["tree_diff"]:
        w(line)
    w("```")
    w("")
    b = fx["b"]
    w("**(b) a project holding upstream's current files, its %d seeds edited by the adopter** (%s)." % (len(b["seeds_edited"]), ", ".join(b["seeds_edited"])))
    w("")
    w("| | upstream's tool | the candidate's tool |")
    w("|---|---:|---:|")
    w("| exit of the plain sync | %s | %s |" % (b["U"]["exit"], b["C"]["exit"]))
    w("| paths written | %d | %d |" % (len(b["U"]["written"]), len(b["C"]["written"])))
    w("| seeds changed / created | %d / %d | %d / %d |" % (len(b["U"]["seeds_changed"]), len(b["U"]["seeds_created"]), len(b["C"]["seeds_changed"]), len(b["C"]["seeds_created"])))
    w("| needed `--force` | %s | %s |" % (mark(b["U"]["forced"]), mark(b["C"]["forced"])))
    w("")
    w("The candidate wrote: %s." % (", ".join("`%s`" % q for q in b["C"]["written"]) or "nothing"))
    w("Paths written that are not a changed tracked source file: **%s**; changed tracked source files not written: **%s**; changed seed sources left as the adopter's own: %s; a `methodology/` directory in the candidate's tree: %s." % (
        b["C_written_not_a_changed_tracked_source"] or "none", b["changed_tracked_sources_not_written"] or "none", b["changed_seed_sources_left_as_is"] or "none", "yes" if b["methodology_dir_in_C"] else "no"))
    w("")
    w("`diff -rq` of the two trees (%d lines):" % len(b["tree_diff"]))
    w("")
    w("```")
    for line in b["tree_diff"]:
        w(line)
    w("```")
    w("")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--work", default=str(Path.home() / "pr3b-work"))
    ap.add_argument("--out", default=str(REPO / "docs" / "planning" / "pr-composition-evidence"))
    ap.add_argument("--candidate-ref", default="pr2b/candidate")
    ap.add_argument("--upstream-ref", default="upstream/main")
    args = ap.parse_args()
    work, out_dir = Path(args.work), Path(args.out)
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    t_start = time.time()

    cand_sha = git(REPO, "rev-parse", args.candidate_ref)[1].strip()
    up_sha = git(REPO, "rev-parse", args.upstream_ref)[1].strip()
    cand_dir, up_dir = work / "tool-candidate", work / "tool-upstream"
    for d, sha in ((cand_dir, cand_sha), (up_dir, up_sha)):
        c, o = sh(["git", "clone", "-q", "--no-local", str(REPO), str(d)])
        assert c == 0, o
        c, o = git(d, "checkout", "-q", sha)
        assert c == 0, o
    fork_sha = git(REPO, "rev-parse", "main")[1].strip()
    fork_dir = work / "tool-fork"
    c, o = sh(["git", "clone", "-q", "--no-local", str(REPO), str(fork_dir)])
    assert c == 0, o
    c, o = git(fork_dir, "checkout", "-q", fork_sha)
    assert c == 0, o
    cand = {"dir": cand_dir, "hist": lambda p, _c={}: _c.setdefault(p, history_blobs(cand_dir, ["HEAD"], p))}
    up = {"dir": up_dir, "hist": lambda p, _c={}: _c.setdefault(p, history_blobs(up_dir, ["HEAD"], p))}
    fork_cache = {}

    def fork_heads(p):
        if p not in fork_cache:
            fork_cache[p] = history_blobs(REPO, ["--all"], p)
        return fork_cache[p]

    rows = []
    for name in (args.only or ADOPTERS):
        t0 = time.time()
        row = {"adopter": name}
        src = DEV / name
        base = work / (name + "-base")
        c, o = sh(["git", "clone", "-q", "--no-local", str(src), str(base)])
        if c != 0:
            row["clone"] = "failed: " + o.strip()[-160:]
            rows.append(row)
            continue
        set_identity(base)
        has_commit = git(base, "rev-parse", "--verify", "-q", "HEAD")[0] == 0
        row["head"] = git(base, "rev-parse", "--short", "HEAD")[1].strip() if has_commit else "no commits"
        row["tracked_files"] = len(git(base, "ls-files")[1].split())
        row["C"] = run_tool_views(cand_dir, base)
        row["U"] = run_tool_views(up_dir, base)
        row["F"] = run_tool_views(fork_dir, base)
        row["real_C"] = real_sync("C", cand_dir, base, work, src, name)
        row["real_U"] = real_sync("U", up_dir, base, work, src, name)
        diffs = row["C"]["dry"]["diffs"]
        row["refused_classified"] = classify_refused(diffs, base, cand, up, fork_heads)
        row["seconds"] = round(time.time() - t0, 1)
        rows.append(row)
        print("%-28s %5.1fs  layout=%s  C: dry exit %s, refused %d  U: dry exit %s" % (
            name, row["seconds"], row["C"]["layout"], row["C"]["dry"]["exit"], len(row["C"]["dry"]["refused"]),
            row["U"]["dry"]["exit"]), flush=True)

    # the audit: the tool's refusal against the blob classification, per adopter
    for row in rows:
        if "C" not in row:
            continue
        refused = {Path(p).as_posix() for p in row["C"]["dry"]["refused"]}
        classified = row["refused_classified"]
        by_rule = {c["dest"] for c in classified if not c.get("in_candidate") and not c.get("is_candidate_current")}
        row["audit_refusal_equals_rule"] = (by_rule == refused) if classified or refused else True

    fixtures = run_fixtures(work, cand_dir, up_dir, cand_sha, up_sha)
    data = {"candidate": cand_sha, "upstream": up_sha, "fork": fork_sha, "fork_sync_blob": git(REPO, "rev-parse", fork_sha + ":bin/sync")[1].strip(), "candidate_sync_blob": git(REPO, "rev-parse", cand_sha + ":bin/sync")[1].strip(),
            "adopters": [slim(r) for r in rows], "fixtures": fixtures}
    (out_dir / "pr3b-rows.json").write_text(json.dumps(data, indent=1, default=str, sort_keys=True))
    (out_dir / "pr3b-adopters-output.md").write_text(build_report(data, time.time() - t_start))
    print("wrote", out_dir, "in %.0f s" % (time.time() - t_start))
    return 0


if __name__ == "__main__":
    sys.exit(main())
