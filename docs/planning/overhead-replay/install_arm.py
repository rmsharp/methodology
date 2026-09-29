#!/usr/bin/env python3
"""Build one arm's working directory: the fixture plus THAT VERSION's own framework files.

    python3 install_arm.py ARM DEST            # one arm
    python3 install_arm.py --all OUTDIR        # all eight, OUTDIR/<arm>
    ARM is one of: v1.0.0 v2.0 v2.7 v3.0 v3.3 v3.7 HEAD none

The framework files come from `git archive <tag>` -- the tag's own layout, never today's.
What is installed follows the tag's BOOTSTRAP.md as the tag's own `bin/sync` (v3.x) and its
Steps 1-4 (v1.x) describe it, applied mechanically:
  * every file in starter-kit/ goes to the project root; the SEEDED files (SESSION_NOTES.md,
    CHANGELOG.md, HANDOFFS.md, ROADMAP.md) only when absent, so the fixture's prior-session
    record survives (BOOTSTRAP: "seeded only when absent, never overwritten");
  * ITERATIVE_METHODOLOGY.md, HOW_TO_USE.md, FRAMEWORK_APPARATUS.md (where the tag has it) and
    workstreams/ go under docs/methodology/;
  * CLAUDE.md = a one-paragraph project header + the tag's SESSION PROTOCOL block (its
    CLAUDE_TEMPLATE.md where present, otherwise the fenced block in BOOTSTRAP.md Step 4).
Known simplifications, stated so nobody reads them as fidelity: README.md is not installed (no version
mandates reading it); customisation steps (Task Mapping table, hooks, dashboard setup) are not applied;
the install is committed on its own so the fixture's uncommitted stub stays uncommitted.
`none` gets the project header only: the zero-overhead baseline.
"""
import io, json, os, re, shutil, subprocess, sys, tarfile, tempfile
import fixture

ARMS = ["v1.0.0", "v2.0", "v2.7", "v3.0", "v3.3", "v3.7", "HEAD", "none"]
SEEDED = {"SESSION_NOTES.md", "CHANGELOG.md", "HANDOFFS.md", "ROADMAP.md"}
REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                      cwd=os.path.dirname(os.path.abspath(__file__))).stdout.strip()
HEADER = ("# textkit\n\nSmall text helpers. Run the tests with `python3 -m unittest discover -s tests`.\n\n")


def archive(ref):
    tar = subprocess.run(["git", "-C", REPO, "archive", ref], capture_output=True, check=True).stdout
    tmp = tempfile.mkdtemp(prefix="arm-")
    tarfile.open(fileobj=io.BytesIO(tar)).extractall(tmp)
    return tmp


def protocol_block(src):
    tpl = os.path.join(src, "starter-kit", "CLAUDE_TEMPLATE.md")
    if os.path.exists(tpl):
        return open(tpl).read()
    boot = open(os.path.join(src, "starter-kit", "BOOTSTRAP.md")).read()
    step4 = boot[boot.index("## Step 4"):]
    m = re.search(r"```markdown\n(.*?)\n```", step4, re.S)
    if not m:
        raise SystemExit("no protocol block found in BOOTSTRAP.md Step 4")
    return m.group(1) + "\n"


def install(arm, dest):
    if arm not in ARMS:
        raise SystemExit(f"unknown arm {arm}; one of {ARMS}")
    fixture.build(dest)
    ref_sha, touched = None, []
    if arm == "none":
        body = HEADER
    else:
        ref_sha = subprocess.run(["git", "-C", REPO, "rev-parse", "--short", arm], capture_output=True, text=True,
                                 check=True).stdout.strip()
        src = archive(arm)
        try:
            kit = os.path.join(src, "starter-kit")
            for name in sorted(os.listdir(kit)):
                p = os.path.join(kit, name)
                target = os.path.join(dest, name)
                if os.path.isfile(p) and not (name in SEEDED and os.path.exists(target)):
                    shutil.copyfile(p, target)
                    touched.append(name)
            for name in ("ITERATIVE_METHODOLOGY.md", "HOW_TO_USE.md", "FRAMEWORK_APPARATUS.md"):
                if os.path.exists(os.path.join(src, name)):
                    os.makedirs(os.path.join(dest, "docs", "methodology"), exist_ok=True)
                    shutil.copyfile(os.path.join(src, name), os.path.join(dest, "docs", "methodology", name))
                    touched.append(f"docs/methodology/{name}")
            ws = os.path.join(src, "workstreams")
            if os.path.isdir(ws):
                shutil.copytree(ws, os.path.join(dest, "docs", "methodology", "workstreams"))
                touched.append("docs/methodology/workstreams")
            body = HEADER + protocol_block(src)
        finally:
            shutil.rmtree(src, ignore_errors=True)
    with open(os.path.join(dest, "CLAUDE.md"), "w") as f:
        f.write(body)
    touched.append("CLAUDE.md")
    env = dict(os.environ, GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
               GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid")
    subprocess.run(["git", "-C", dest, "add", "--", *touched], check=True, capture_output=True)
    subprocess.run(["git", "-C", dest, "commit", "-q", "-m", f"Install methodology arm {arm}"], check=True,
                   capture_output=True, env=env)
    return {"arm": arm, "ref_sha": ref_sha, "dest": dest, "base": fixture.base_sha(dest), "ghost": fixture.ghost_sha(dest)}


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 2 and a[0] == "--all":
        for arm in ARMS:
            print(json.dumps(install(arm, os.path.join(a[1], arm))))
    elif len(a) == 2:
        print(json.dumps(install(*a)))
    else:
        raise SystemExit(__doc__)
