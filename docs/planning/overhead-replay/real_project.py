#!/usr/bin/env python3
"""Build one arm from a REAL project at a fixed commit, with one methodology version laid over it.

    python3 real_project.py ARM DEST [--repo PATH] [--commit SHA] [--cache DIR]

The default is nprcgenekeepr at 879503cce, the parent of the commit that fixed issue #121 (S314): the
session's natural task is that issue, and the real fix (54b87c1da) is the answer key.

What keeps the run honest:
  * the copy is built by `git fetch <repo> <commit>` into a fresh repository, so only that commit and its
    ANCESTORS exist: the fix commit and everything after it are not in the object database to be found;
  * `origin` is removed and no remote-tracking refs exist, so nothing can be pushed or commented on;
  * the arm's framework files are laid over the project's own the way `bin/sync` would: starter-kit files to
    the root (seeded files only when absent), the manual and workstreams under docs/methodology/, and the
    project's SESSION PROTOCOL block in CLAUDE.md replaced by that version's, leaving the project's own
    sections alone. The install is committed on its own; its sha is the base for scoring.
`none` removes nothing from the project's files but installs nothing either (the project's own methodology, as
it stood at that commit, stays: it is the project's real starting state, not a framework-free one).
"""
import argparse, os, re, shutil, subprocess, sys
import install_arm

DEFAULT_REPO = os.path.expanduser("~/Development/nprcgenekeepr")
DEFAULT_COMMIT = "879503cce9936704eafc3709c2fc9db8328ccc43"
FIX_COMMIT = "54b87c1da"


def sh(*a, cwd=None, check=True):
    return subprocess.run(list(a), cwd=cwd, check=check, capture_output=True, text=True).stdout.strip()


def template(cache, repo=DEFAULT_REPO, commit=DEFAULT_COMMIT):
    """A repository holding `commit` and its ancestors only, on branch master. Built once, reused per run."""
    if os.path.isdir(os.path.join(cache, ".git")):
        return cache
    os.makedirs(cache, exist_ok=True)
    sh("git", "init", "-q", "-b", "master", cache)
    sh("git", "fetch", "-q", "--no-tags", repo, commit, cwd=cache)
    sh("git", "checkout", "-q", "FETCH_HEAD", cwd=cache)
    sh("git", "checkout", "-q", "-B", "master", cwd=cache)
    return cache


def protocol_section(claude_md):
    """Span of the SESSION PROTOCOL block: from its heading to the line before the next '---' rule or '## '/'# ' heading."""
    m = re.search(r"^## SESSION PROTOCOL.*$", claude_md, re.M)
    if not m:
        raise SystemExit("no SESSION PROTOCOL heading in CLAUDE.md")
    end = re.search(r"^(---\s*$|#{1,2} )", claude_md[m.end():], re.M)
    return m.start(), m.end() + (end.start() if end else len(claude_md) - m.end())


def install(arm, dest, cache="/tmp/overhead-real-template", repo=DEFAULT_REPO, commit=DEFAULT_COMMIT):
    if arm not in install_arm.ARMS:
        raise SystemExit(f"unknown arm {arm}")
    if os.path.exists(dest):
        raise SystemExit(f"{dest} exists; refusing to overwrite")
    tpl = template(cache, repo, commit)
    sh("git", "clone", "-q", "--no-local", "--no-tags", tpl, dest)
    sh("git", "remote", "remove", "origin", cwd=dest)
    env = dict(os.environ, GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
               GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid")
    touched = []
    if arm != "none":
        src = install_arm.archive(arm)
        try:
            kit = os.path.join(src, "starter-kit")
            for name in sorted(os.listdir(kit)):
                p, target = os.path.join(kit, name), os.path.join(dest, name)
                if os.path.isfile(p) and name != "CLAUDE_TEMPLATE.md" and not (name in install_arm.SEEDED and os.path.exists(target)):
                    shutil.copyfile(p, target)
                    touched.append(name)
            for name in ("ITERATIVE_METHODOLOGY.md", "HOW_TO_USE.md", "FRAMEWORK_APPARATUS.md"):
                if os.path.exists(os.path.join(src, name)):
                    os.makedirs(os.path.join(dest, "docs", "methodology"), exist_ok=True)
                    shutil.copyfile(os.path.join(src, name), os.path.join(dest, "docs", "methodology", name))
                    touched.append(f"docs/methodology/{name}")
            ws = os.path.join(src, "workstreams")
            if os.path.isdir(ws):
                target = os.path.join(dest, "docs", "methodology", "workstreams")
                shutil.rmtree(target, ignore_errors=True)
                shutil.copytree(ws, target)
                touched.append("docs/methodology/workstreams")
            block = install_arm.protocol_block(src)
            bs, be = protocol_section(block)
            cm = os.path.join(dest, "CLAUDE.md")
            text = open(cm).read()
            ps, pe = protocol_section(text)
            open(cm, "w").write(text[:ps] + block[bs:be].rstrip("\n") + "\n\n" + text[pe:].lstrip("\n"))
            touched.append("CLAUDE.md")
        finally:
            shutil.rmtree(src, ignore_errors=True)
    subprocess.run(["git", "-C", dest, "add", "-A", "--", *touched] if touched else ["git", "-C", dest, "status"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", dest, "commit", "-q", "--allow-empty", "--no-verify", "-m", f"Install methodology arm {arm}"],
                   check=True, capture_output=True, env=env)
    return {"arm": arm, "dest": dest, "base": sh("git", "rev-parse", "--short", "HEAD", cwd=dest),
            "start_commit": commit, "fix_commit_reachable": FIX_COMMIT in sh("git", "rev-list", "--all", cwd=dest)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("arm"); ap.add_argument("dest")
    ap.add_argument("--repo", default=DEFAULT_REPO); ap.add_argument("--commit", default=DEFAULT_COMMIT)
    ap.add_argument("--cache", default="/tmp/overhead-real-template")
    a = ap.parse_args()
    print(install(a.arm, a.dest, a.cache, a.repo, a.commit))
