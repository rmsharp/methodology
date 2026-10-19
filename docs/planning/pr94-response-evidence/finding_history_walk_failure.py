"""A finding beyond the maintainer's nine points, made while testing point 1.

Usage: python3 -I finding_history_walk_failure.py <trimmer.py> <tests-module.py>

The generated proof starts with `TRIM_SHA="$(git log --diff-filter=A -1 --format=%H -- "$SHARD" 2>/dev/null)"`.
If that command FAILS (here: the parent commit's root tree is not in the object store, as in a
treeless partial clone whose remote is gone), the error is discarded, TRIM_SHA is empty, and the
proof runs in its "trim not yet committed" mode: it compares HEAD's copy of the live ledger with
the working tree's, which are the same file, and prints OK. The trim IS committed; nothing was
compared. Prints the proof's exit code and its last line.
"""
import importlib.util
import pathlib
import sys
import tempfile

trimmer, tests = sys.argv[1], sys.argv[2]
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("t", tests)
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
t.TRIM_PY = pathlib.Path(trimmer)

with tempfile.TemporaryDirectory() as tmp:
    p = t.make_handoff_repo(tmp)
    r = t.run_trim(p, "--file", "HANDOFFS.md", "--cut", "2", "--write", "--today", "2026-02-01")
    assert "[WROTE]" in r.stdout, r.stdout
    shard = sorted((p / "docs" / "archive").glob("HANDOFFS-through-*.md"))[0].relative_to(p).as_posix()
    t.sh(p, "git", "add", "-A")
    t.sh(p, "git", "commit", "-qm", "trim")
    ok = t.sh(p, "bash", shard + ".verify.sh")
    sha = t.sh(p, "git", "rev-parse", "HEAD^^{tree}").stdout.strip()      # the parent's root tree
    obj = p / ".git" / "objects" / sha[:2] / sha[2:]
    obj.chmod(0o644)
    obj.unlink()
    v = t.sh(p, "bash", shard + ".verify.sh")
    print("trimmer:", trimmer)
    print("control (store intact)           : exit %d, %s" % (ok.returncode, ok.stdout.strip().splitlines()[-1][:110]))
    print("parent's root tree missing       : exit %d, %s" % (v.returncode, v.stdout.strip().splitlines()[-1][:110]))
    print("   the proof says it compared: %s" % ("trim not yet committed" in v.stdout))
