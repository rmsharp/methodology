#!/usr/bin/env python3
"""i95-compose.py -- upstream issue #95: what would the issue's own suggested fix touch, does it make a
fresh project green, and does it merge with the pull request candidate?

Usage:  python3 i95-compose.py SCRATCH_DIR

THE PATCH THIS BUILDS IS A MEASURING INSTRUMENT, NOT A PROPOSED FIX. It applies the four changes the
issue suggests, literally, as exact-string edits that refuse when an anchor is absent or not unique, onto
two pinned commits (upstream's `main` and the candidate), in a scratch repository that is deleted on the
next run. Nothing here is written to this repository's history except this script and its saved output.

  A  merge test: instrument on upstream's tip, then `git merge-tree --write-tree` against the candidate
     (symmetric, so it answers both "he fixes it first and we rebase" and "we land first and he rebases"),
     once without and once with the version bump the repository's convention asks for
  B  fold test: the same edits on the candidate itself (do the anchors exist, how many files, how many lines)
  C  does the literal fix make day zero green? the new unit class red on the unfixed tool and green on the
     fixed one; the new shell pass-control run against the original seeds and the fixed ones
  D  the same pass-control with the template's placeholder padded to the fence floor, to show what the
     issue's alternative (a long-enough placeholder) would cost
"""
import importlib.util
import os
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = HERE
while not os.path.isdir(os.path.join(REPO, ".git")):
    REPO = os.path.dirname(REPO)

UP = "f34769f31ca351a520c2da4fa5f9e65b5153bffa"      # upstream/main at S328's Phase 0
CAND = "ced2c82"                                      # refs/heads/pr2/candidate (local ref)

_spec = importlib.util.spec_from_file_location("dz", os.path.join(HERE, "i95-dayzero.py"))
dz = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dz)

SH_BLOCK = '''# Seeds that ship together must pass the seed config together (upstream issue 95): a fresh
# project holding only the untouched seeds must not be over budget on day zero.
P=$(mktemp -d); (cd "$P" && git init -q)
cp "$CB" "$P/context_budget.py"
cp "$STARTER/context-budget.json" "$P/.context-budget.json"
cp "$STARTER/SESSION_NOTES.md" "$P/SESSION_NOTES.md"
cp "$STARTER/CLAUDE_TEMPLATE.md" "$P/CLAUDE.md"
(cd "$P" && python3 context_budget.py --status >/dev/null 2>&1); [ "$?" != "2" ] \\
    && pass "untouched seeds are within the seed context budget" \\
    || fail "untouched seeds are over the seed context budget (exit 2)"
rm -rf "$P"
'''
SH_ANCHOR = '''    && pass "removing the budget:protected block is refused" \\
    || fail "protected-block removal was not caught"
rm -rf "$P"
'''
PY_CLASS = '''class TestLineCapIsMeasuredInBytes(unittest.TestCase):
    """max_line_bytes names bytes and its message says B; it used to count characters, so a line
    of three-byte characters passed a cap it exceeded (upstream issue 95, finding 4)."""

    def test_a_multibyte_line_over_the_cap_in_bytes_is_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, "t.md").write_text("x" * 40 + "\\u2014" * 30 + "\\n", encoding="utf-8")  # 70 characters, 130 bytes
            r = cb.measure_file(d, {"path": "t.md", "max_line_bytes": 100})
            self.assertEqual([f["kind"] for f in r["findings"]], ["line_bytes"])
            self.assertIn("130 B", r["findings"][0]["msg"])

    def test_an_ascii_line_under_the_cap_is_not_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, "t.md").write_text("x" * 100 + "\\n", encoding="utf-8")
            r = cb.measure_file(d, {"path": "t.md", "max_line_bytes": 100})
            self.assertEqual(r["findings"], [])


'''


def git(args, cwd, env=None, check=True, inp=None):
    e = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    e.update(env or {})
    p = subprocess.run(["git", *args], cwd=cwd, env=e, capture_output=True, input=inp)
    if check and p.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed ({p.returncode}): {p.stderr.decode()[:400]}")
    return p


def once(text, old, label):
    n = text.count(old)
    if n != 1:
        sys.exit(f"ANCHOR {label}: expected exactly one occurrence, found {n}")


def edits(r, rev, bump, pad=False, where="end"):
    """The instrument's edits against `rev`: {path: new bytes}. Refuses on any missing or repeated anchor."""
    def at(path):
        return git(["show", f"{rev}:{path}"], r).stdout
    out = {}
    out["starter-kit/SESSION_NOTES.md"] = dz.wrapped_notes(at("starter-kit/SESSION_NOTES.md"))
    tpl, _n = dz.fenced_template(at("starter-kit/CLAUDE_TEMPLATE.md"))
    if pad:
        t = tpl.decode()
        m = re.search(r"(<!-- budget:protected -->\n)(.*?)(\n<!-- /budget:protected -->)", t, re.S)
        need = 800 - len(m.group(2).strip()) + 1
        t = t[:m.end(2)] + "\n" + ("padding " * (need // 8 + 1))[:need] + t[m.end(2):]
        tpl = t.encode()
    out["starter-kit/CLAUDE_TEMPLATE.md"] = tpl
    cb = at("starter-kit/context_budget.py").decode()
    old1 = "        long = [(i + 1, len(l)) for i, l in enumerate(lines) if len(l) > cap]"
    once(cb, old1, "context_budget.py line cap")
    once(cb, 'data = open(path, "rb").read()', "context_budget.py raw read")
    cb = cb.replace(old1, '        long = [(i + 1, len(l)) for i, l in enumerate(data.split(b"\\n")) if len(l) > cap]')
    if cb.count("len(body.strip())") != 2:
        sys.exit(f"ANCHOR context_budget.py fence floor: expected 2 occurrences, found {cb.count('len(body.strip())')}")
    cb = cb.replace("len(body.strip())", "len(body.strip().encode())")
    if bump:
        m = re.search(r'^VERSION = "(\d+)\.(\d+)\.(\d+)"', cb, re.M)
        assert m, "no VERSION line"
        cb = cb[:m.start()] + f'VERSION = "{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 1}"' + cb[m.end():]
    out["starter-kit/context_budget.py"] = cb.encode()
    ut = at("tools/test_context_budget.py").decode()
    if where == "end":
        once(ut, '\n\nif __name__ == "__main__":\n', "tools/test_context_budget.py main guard")
        ut = ut.replace('\n\nif __name__ == "__main__":\n', "\n\n" + PY_CLASS.rstrip("\n") + '\n\n\nif __name__ == "__main__":\n')
    else:
        mid = "class TestPrecommitClassArm(unittest.TestCase):"
        once(ut, mid, "tools/test_context_budget.py mid-file anchor")
        ut = ut.replace(mid, PY_CLASS + mid)
    out["tools/test_context_budget.py"] = ut.encode()
    sh = at("bin/tests.sh").decode()
    once(sh, SH_ANCHOR, "bin/tests.sh anchor")
    once(sh, 'CB="$STARTER/context_budget.py"', "bin/tests.sh $CB")
    out["bin/tests.sh"] = sh.replace(SH_ANCHOR, SH_ANCHOR + "\n" + SH_BLOCK).encode()
    return out


def commit_on(r, rev, files, msg):
    """A commit on top of `rev` with `files` replaced, built with a scratch index (no worktree)."""
    idx = os.path.join(r, ".git", "i95-index")
    env = {"GIT_INDEX_FILE": idx}
    git(["read-tree", rev], r, env)
    for path, data in files.items():
        oid = git(["hash-object", "-w", "--stdin"], r, inp=data).stdout.decode().strip()
        git(["update-index", "--cacheinfo", f"100755,{oid},{path}" if path.endswith((".sh", ".py")) and
             git(["ls-tree", rev, path], r).stdout.decode().startswith("100755") else f"100644,{oid},{path}"], r, env)
    tree = git(["write-tree"], r, env).stdout.decode().strip()
    os.remove(idx)
    return git(["commit-tree", tree, "-p", rev, "-m", msg], r).stdout.decode().strip()


def merge_tree(r, a, b):
    p = git(["merge-tree", "--write-tree", "--name-only", a, b], r, check=False)
    lines = p.stdout.decode().split("\n")
    tree = lines[0]
    names = []
    for l in lines[1:]:
        if not l:
            break
        names.append(l)
    regions, hunks = {}, {}
    for n in names:
        blob = git(["show", f"{tree}:{n}"], r, check=False).stdout.decode("utf-8", "replace")
        regions[n] = len(re.findall(r"^<<<<<<< ", blob, re.M))
        m = re.search(r"^<<<<<<< .*?^>>>>>>> [^\n]*$", blob, re.M | re.S)
        hunks[n] = [l[:110] for l in m.group(0).split("\n")[:16]] if m else []
    return p.returncode, names, regions, hunks


def extract(r, commit, dest):
    os.makedirs(dest)
    a = git(["archive", commit], r).stdout
    subprocess.run(["tar", "-x", "-C", dest], input=a, check=True)


def run(cmd, cwd, env=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=dict(os.environ, **(env or {})))
    return p.returncode, (p.stdout + p.stderr)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    scratch = os.path.abspath(sys.argv[1])
    if os.path.exists(scratch):
        shutil.rmtree(scratch)
    os.makedirs(scratch)
    r = os.path.join(scratch, "r")
    git(["init", "-q", r], scratch)
    git(["fetch", "-q", REPO, "refs/remotes/upstream/main:refs/heads/up", "refs/heads/pr2/candidate:refs/heads/cand"], r)
    up = git(["rev-parse", "up"], r).stdout.decode().strip()
    cand = git(["rev-parse", "cand"], r).stdout.decode().strip()
    if up != UP or not cand.startswith(CAND):
        sys.exit(f"pinned revisions moved: upstream {up} (want {UP}), candidate {cand} (want {CAND}...)")
    out = [f"i95-compose.py: the issue's suggested fix as a measuring instrument (upstream {up[:7]}, candidate {cand[:7]})", ""]

    out.append("A. merge test: instrument on upstream's tip against the candidate (git merge-tree --write-tree, symmetric)")
    out.append("   the new unit class goes at the end of tools/test_context_budget.py ('end') or before an existing class ('mid')")
    shown = {}
    for where in ("end", "mid"):
        for bump in (False, True):
            files = edits(r, up, bump, where=where)
            inst = commit_on(r, up, files, "instrument")
            rc, names, regions, hunks = merge_tree(r, inst, cand)
            label = f"new test class at {where}, " + ("with the version bump   " if bump else "without the version bump")
            if rc == 0:
                out.append(f"   {label}: merges cleanly (exit 0)")
            else:
                out.append(f"   {label}: exit {rc}, {len(names)} conflicted: " +
                           ", ".join(f"{n} ({regions[n]} region{'s' if regions[n] != 1 else ''})" for n in names))
                for n in names:
                    shown.setdefault((n, where, bump), hunks[n])
    out.append(f"   files the instrument edits: {len(files)}: " + ", ".join(sorted(files)))
    out.append("   for the 5-file cap per commit (SAFEGUARDS.md): those files plus the ledger entry the pre-commit hook "
               f"requires = {len(files) + 1}")
    out.append("   the conflicting hunks, first region of each (ours = the instrument on upstream's tip, theirs = the candidate):")
    for (n, where, bump), hunk in shown.items():
        out.append(f"      -- {n} (class at {where}, bump={bump})")
        for l in hunk:
            out.append("         | " + l)
    out.append("")

    out.append("B. fold test: the same edits on the candidate itself")
    files_c = edits(r, cand, True)
    fold = commit_on(r, cand, files_c, "instrument on the candidate")
    ns = git(["diff", "--numstat", cand, fold], r).stdout.decode().strip().split("\n")
    out.append("   every anchor exists exactly once on the candidate; the edits apply (numstat, + / - / path):")
    for l in ns:
        out.append("      " + l.replace("\t", "  "))
    out.append("")

    out.append("C. does the literal fix make day zero green?")
    inst_dir = os.path.join(scratch, "inst")
    extract(r, commit_on(r, up, edits(r, up, False), "instrument"), inst_dir)
    orig_dir = os.path.join(scratch, "orig")
    extract(r, up, orig_dir)
    rc_new, o_new = run(["python3", "tools/test_context_budget.py", "TestLineCapIsMeasuredInBytes"], inst_dir)
    tail = [l for l in o_new.strip().split("\n") if l][-3:]
    out.append(f"   new unit class on the fixed tool: exit {rc_new}  ({tail[-1] if tail else ''})")
    shutil.copy(os.path.join(orig_dir, "starter-kit", "context_budget.py"), os.path.join(inst_dir, "starter-kit", "context_budget.py"))
    rc_red, o_red = run(["python3", "tools/test_context_budget.py", "TestLineCapIsMeasuredInBytes"], inst_dir)
    fails = len(re.findall(r"^FAIL: ", o_red, re.M))
    out.append(f"   the same class on the UNFIXED tool: exit {rc_red}, {fails} failing test(s) (it is red where it should be)")
    # a second, untouched copy of the fixed tree for the shell block (inst_dir now holds the unfixed tool)
    extract(r, commit_on(r, up, edits(r, up, False), "instrument"), os.path.join(scratch, "inst2"))
    harness = 'pass(){ echo "PASS: $*"; }; fail(){ echo "FAIL: $*"; }\nSTARTER="$1/starter-kit"; CB="$STARTER/context_budget.py"\n' + SH_BLOCK
    hp = os.path.join(scratch, "block.sh")
    open(hp, "w").write(harness)
    for title, d in (("original seeds and tool (upstream tip)", orig_dir), ("issue's fix applied literally", os.path.join(scratch, "inst2"))):
        rc, o = run(["bash", hp, d], scratch)
        out.append(f"   new shell pass-control on the {title}: " + [l for l in o.split("\n") if l.startswith(("PASS", "FAIL"))][0])
    # the literal fix, in a project: which finding is left?
    proj = os.path.join(scratch, "proj")
    os.makedirs(proj)
    git(["init", "-q"], proj)
    for src, dst in (("starter-kit/context_budget.py", "context_budget.py"), ("starter-kit/context-budget.json", ".context-budget.json"),
                     ("starter-kit/SESSION_NOTES.md", "SESSION_NOTES.md"), ("starter-kit/CLAUDE_TEMPLATE.md", "CLAUDE.md")):
        shutil.copy(os.path.join(scratch, "inst2", src), os.path.join(proj, dst))
    rc, rows = dz.measure(proj)
    out.append(f"   the literal fix in a fresh project (untouched seeds): exit {rc}")
    for path, (status, finds) in rows.items():
        for kind, msg in finds:
            out.append(f"      {path} [{kind}] {dz.ANSI.sub('', msg)}")
        if not finds:
            out.append(f"      {path}: {status}")
    out.append("")

    out.append("D. the issue's alternative: a placeholder long enough to clear the fence floor")
    pad_dir = os.path.join(scratch, "pad")
    extract(r, commit_on(r, up, edits(r, up, False, pad=True), "instrument padded"), pad_dir)
    rc, o = run(["bash", hp, pad_dir], scratch)
    out.append("   shell pass-control with the placeholder padded to 801 characters: " + [l for l in o.split("\n") if l.startswith(("PASS", "FAIL"))][0])
    grow = len(open(os.path.join(pad_dir, "starter-kit", "CLAUDE_TEMPLATE.md"), "rb").read()) - \
        len(open(os.path.join(scratch, "inst2", "starter-kit", "CLAUDE_TEMPLATE.md"), "rb").read())
    out.append(f"   the template grows by {grow} B over the unpadded fenced one, and a never-customised project then passes the "
               "guard that exists to catch an emptied purpose")
    print("\n".join(out))


if __name__ == "__main__":
    main()
