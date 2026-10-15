#!/usr/bin/env python3
"""i95-dayzero.py -- upstream issue #95: does a fresh adopter fail its own context budget on day zero?

Usage:  python3 i95-dayzero.py SCRATCH_DIR            (SCRATCH_DIR is created; an existing one is removed)

Reads three pinned trees with `git archive` (the working tree is never touched), runs the tool each
tree ships against the files each tree ships, and prints one table. The instrument is the tool's own
`--status --json`, parsed, never read by eye.

Cases, per tree:
  notes      the issue's repro: seed SESSION_NOTES.md alone, with the tree's seed config
  template   the issue's repro: CLAUDE_TEMPLATE.md as CLAUDE.md alone
  control    the issue's control: seed SESSION_NOTES.md with line 5 wrapped and a `## Session History`
             heading above the italic history marker (it must pass, or the repro measures nothing)
  fenced     CLAUDE_TEMPLATE.md with its `## Purpose` placeholder wrapped in the budget:protected fence,
             which is the issue's suggested fix 3 applied to the template and nothing else
  sync       the real route: `bin/sync` into an empty git project, then the tool; once as synced, once
             with CLAUDE_TEMPLATE.md copied to CLAUDE.md (what BOOTSTRAP tells an adopter to do)
  sync-new   the same under `--layout new` (only for a tree whose bin/sync has the flag)
"""
import json
import os
import re
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(REPO, ".git")):
    REPO = os.path.dirname(REPO)

# Pinned: a bare ref moves. `f34769f` is upstream/main at S328's Phase 0, `981c33a` the fork's main
# before this session's claim, `ced2c82` the pull request candidate (a local ref, pr2/candidate).
TREES = [("upstream", "f34769f31ca351a520c2da4fa5f9e65b5153bffa"),
         ("fork", "981c33a43532dd9e14f3ea95b52d5237b8cf8429"),
         ("candidate", "ced2c82")]
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def sh(cmd, cwd=None, check=True):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and p.returncode != 0:
        sys.exit(f"FAILED {cmd} (cwd {cwd}) exit {p.returncode}\n{p.stdout}\n{p.stderr}")
    return p


def export(rev, dest):
    os.makedirs(dest)
    arch = subprocess.run(["git", "archive", rev], cwd=REPO, capture_output=True)
    if arch.returncode != 0:
        sys.exit(f"git archive {rev} failed: {arch.stderr.decode()}")
    subprocess.run(["tar", "-x", "-C", dest], input=arch.stdout, check=True)


def blob(rev, path):
    return sh(["git", "rev-parse", "--short", f"{rev}:{path}"], cwd=REPO).stdout.strip()


def measure(cwd, tool="context_budget.py"):
    """Run the tool's own --status --json in `cwd`; return (exit, {path: (status, [(kind, msg)])})."""
    p = sh(["python3", tool, "--status", "--json"], cwd=cwd, check=False)
    try:
        d = json.loads(p.stdout)
    except ValueError:
        return p.returncode, {"<unparseable>": ("?", [("raw", p.stdout[:200] + p.stderr[:200])])}
    rows = {}
    for f in d.get("files", []):
        rows[f["path"]] = (f["status"], [(x["kind"], x["msg"]) for x in f.get("findings", [])])
    for x in d.get("config_defects", []) or []:
        rows.setdefault("<config>", ("defect", []))[1].append(("config", str(x)))
    return p.returncode, rows


def report(title, rc, rows, out):
    out.append(f"  {title}: exit {rc}")
    for path, (status, finds) in rows.items():
        if status in ("ok", "unmeasured") and not finds:
            out.append(f"      {path}: {status}")
            continue
        out.append(f"      {path}: {status}")
        for kind, msg in finds:
            out.append(f"          [{kind}] {ANSI.sub('', msg)}")


def seed_project(tree_dir, scratch, name, files):
    """A directory holding the tree's tool and seed config plus `files` {dest: source-path-or-bytes}."""
    d = os.path.join(scratch, name)
    os.makedirs(d)
    sh(["git", "init", "-q"], cwd=d)
    shutil.copy(os.path.join(tree_dir, "starter-kit", "context_budget.py"), d)
    shutil.copy(os.path.join(tree_dir, "starter-kit", "context-budget.json"), os.path.join(d, ".context-budget.json"))
    for dest, src in files.items():
        with open(os.path.join(d, dest), "wb") as fh:
            fh.write(src if isinstance(src, bytes) else open(src, "rb").read())
    return d


def wrapped_notes(seed_bytes):
    lines = seed_bytes.decode("utf-8").split("\n")
    long5 = lines[4]
    assert len(long5.encode()) > 280, "seed line 5 is no longer over the cap: the control is moot"
    cut = long5.rfind(" ", 0, len(long5) // 2)
    lines[4:5] = [long5[:cut], long5[cut + 1:]]
    marker = next(i for i, l in enumerate(lines) if l.startswith("*Session history accumulates below"))
    lines[marker:marker] = ["## Session History", ""]
    return "\n".join(lines).encode("utf-8")


def fenced_template(tpl_bytes):
    t = tpl_bytes.decode("utf-8")
    m = re.search(r"(## Purpose\n\n)(.*?)(\n\n---\n)", t, re.S)
    assert m, "no `## Purpose` block in the template"
    body = m.group(2)
    t = t[:m.start(2)] + "<!-- budget:protected -->\n" + body + "\n<!-- /budget:protected -->" + t[m.end(2):]
    return t.encode("utf-8"), len(body.strip())


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    scratch = os.path.abspath(sys.argv[1])
    if os.path.exists(scratch):
        shutil.rmtree(scratch)
    os.makedirs(scratch)
    out = ["i95-dayzero.py: upstream issue #95 on three pinned trees", ""]
    for name, rev in TREES:
        tdir = os.path.join(scratch, name, "tree")
        export(rev, tdir)
        sk = os.path.join(tdir, "starter-kit")
        out.append(f"=== {name} ({sh(['git', 'rev-parse', '--short', rev], cwd=REPO).stdout.strip()})")
        out.append("  blobs: " + ", ".join(f"{os.path.basename(p)} {blob(rev, 'starter-kit/' + os.path.basename(p))}"
                                           for p in ("SESSION_NOTES.md", "context-budget.json", "CLAUDE_TEMPLATE.md", "context_budget.py")))
        notes = open(os.path.join(sk, "SESSION_NOTES.md"), "rb").read()
        tpl = open(os.path.join(sk, "CLAUDE_TEMPLATE.md"), "rb").read()
        line5 = notes.decode().split("\n")[4]
        out.append(f"  seed SESSION_NOTES.md line 5: {len(line5)} characters, {len(line5.encode())} bytes; "
                   f"`## ` headings: {sum(1 for l in notes.decode().split(chr(10)) if l.startswith('## '))}")
        cases = [("notes", {"SESSION_NOTES.md": notes}),
                 ("template", {"CLAUDE.md": tpl}),
                 ("control", {"SESSION_NOTES.md": wrapped_notes(notes)})]
        fenced, body_chars = fenced_template(tpl)
        cases.append(("fenced", {"CLAUDE.md": fenced}))
        for case, files in cases:
            d = seed_project(tdir, os.path.join(scratch, name), case, files)
            rc, rows = measure(d)
            report(case + (f" (the fenced Purpose body is {body_chars} characters)" if case == "fenced" else ""), rc, rows, out)
        for layout in ("legacy", "new"):
            helptxt = sh(["python3", os.path.join(tdir, "bin", "sync"), "--help"], check=False).stdout
            if layout == "new" and "--layout" not in helptxt:
                out.append("  sync-new: bin/sync has no --layout flag in this tree (not run)")
                continue
            proj = os.path.join(scratch, name, "sync-" + layout)
            os.makedirs(proj)
            sh(["git", "init", "-q"], cwd=proj)
            args = ["python3", os.path.join(tdir, "bin", "sync"), proj, "--source", "local"]
            if layout == "new":
                args += ["--layout", "new"]
            sy = sh(args, check=False)
            out.append(f"  sync{'-new' if layout == 'new' else ''}: bin/sync exit {sy.returncode}")
            home = os.path.join(proj, "methodology") if layout == "new" else proj
            tool = "methodology/context_budget.py" if layout == "new" else "context_budget.py"
            rc, rows = measure(proj, tool)
            report("  as synced (no CLAUDE.md)", rc, rows, out)
            shutil.copy(os.path.join(home, "CLAUDE_TEMPLATE.md"), os.path.join(proj, "CLAUDE.md"))
            rc, rows = measure(proj, tool)
            report("  with CLAUDE.md copied from CLAUDE_TEMPLATE.md", rc, rows, out)
        out.append("")
    print("\n".join(out))


if __name__ == "__main__":
    main()
