"""SCRATCH EVIDENCE for docs/planning/issue93-trimmer-proof-false-red-plan.md, not the plan's implementation.
Controlled reproduction of issue #93 cause 2 (the L2 `leaked` substring test), using the
canonical suite's own fixture helpers against the canonical generator. Read-only on the repo:
everything is built in a temp directory.

Variants (each trims HANDOFFS.md at --cut 2, commits, runs the generated .verify.sh):
  A  control        : no archived record quotes a front-matter line          -> expect OK
  B  quote mid-line : an ARCHIVED record quotes a front-matter line in
                      backticks, inside a longer line (the adopter's shape)  -> v1.5.0 FAILs L2 "leaked"
  C  B + exact-line : the same generated script with `leaked` patched to
                      exact whole-line membership                            -> expect OK
  D  true leak      : a front-matter line copied WHOLE into the shard's own
                      front matter inside the trim commit (the defect
                      `leaked` exists to catch), v1.5.0 script               -> FAILs
  E  the same leak with the exact-line patch applied                       -> must still FAIL
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
import test_methodology_trim as T  # noqa: E402

FM_LINE = "Newest on top; prepend-only. Archive when above N receipts."   # > 24 chars
EXACT_OLD = 'leaked = [ln for ln in bfront.splitlines()\n          if ln.strip() and len(ln.strip()) > 24 and (ln in sfront or ln in "".join(sr))]'
EXACT_NEW = ('sr_lines = set("".join(sr).splitlines()); sfront_lines = set(sfront.splitlines())\n'
             'leaked = [ln for ln in bfront.splitlines()\n'
             '          if ln.strip() and len(ln.strip()) > 24 and (ln in sfront_lines or ln in sr_lines)]')


def build(tmp, quote=False, leak=None):
    p = T.make_handoff_repo(tmp)
    hf = p / "HANDOFFS.md"
    t = hf.read_text(encoding="utf-8")
    t = t.replace("This file currently holds **0**.\n",
                  "This file currently holds **0**.\n\n" + FM_LINE + "\n", 1)
    if quote:
        t = t.replace("commentary about session 5.",
                      "commentary about session 5, see `%s` in the front matter." % FM_LINE, 1)
    hf.write_text(t, encoding="utf-8")
    T.sh(p, "git", "commit", "-qa", "--amend", "-m", "seed")
    T.run_trim(p, "--file", "HANDOFFS.md", "--cut", "2", "--write", "--today", "2026-02-01")
    shard = sorted((p / "docs" / "archive").glob("HANDOFFS-through-*.md"))[0]
    if leak == "shard-front-matter":      # the whole line lands in the shard's own front matter
        st = shard.read_text(encoding="utf-8")
        first, rest = st.split("\n", 1)
        shard.write_text(first + "\n\n" + FM_LINE + "\n" + rest, encoding="utf-8")
    T.sh(p, "git", "add", "-A")
    T.sh(p, "git", "commit", "-qm", "trim")
    return p, shard


def verify(p, shard, patch=False, true_leak=False):
    v = Path(str(shard) + ".verify.sh")
    s = v.read_text(encoding="utf-8")
    if patch:
        assert EXACT_OLD in s, "the v1.5.0 leaked line was not found verbatim"
        s = s.replace(EXACT_OLD, EXACT_NEW, 1)
        v = Path(str(v) + ".patched.sh")
        v.write_text(s, encoding="utf-8")
    r = subprocess.run(["bash", str(v)], cwd=str(p), capture_output=True, text=True)
    out = [ln for ln in (r.stdout + r.stderr).splitlines() if ln.startswith(("FAIL", "OK", "NOTE", "records"))]
    return r.returncode, out


def main():
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        p, shard = build(Path(tmp) / "a")
        rows.append(("A control (no quote)", verify(p, shard)))
    with tempfile.TemporaryDirectory() as tmp:
        p, shard = build(Path(tmp) / "b", quote=True)
        rows.append(("B quote mid-line, v1.5.0 script", verify(p, shard)))
        rows.append(("C quote mid-line, exact-line patch", verify(p, shard, patch=True)))
    with tempfile.TemporaryDirectory() as tmp:
        p, shard = build(Path(tmp) / "d", leak="shard-front-matter")
        rows.append(("D true leak (whole line in shard front matter), v1.5.0 script", verify(p, shard)))
        rows.append(("E same true leak, exact-line patch", verify(p, shard, patch=True)))
    for name, (rc, out) in rows:
        print("%-38s exit=%s" % (name, rc))
        for ln in out:
            print("    " + ln[:150])


if __name__ == "__main__":
    main()
