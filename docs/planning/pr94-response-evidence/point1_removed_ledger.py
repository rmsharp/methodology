"""Point 1 of the maintainer's comment on PR #94: a trim commit that also `git rm`s HANDOFFS.md.

Usage: python3 -I point1_removed_ledger.py <trimmer.py> <tests-module.py>

Builds the PR's own `make_handoff_repo` fixture, trims it with the given trimmer (--cut 2), then
commits the trim TOGETHER with `git rm HANDOFFS.md` (a total loss of the live ledger), and runs the
generated proof. Prints the proof's exit code and its last lines. The tests module is only used for
its fixture helpers; TRIM_PY is overridden so the given trimmer generates the proof.
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
    shard = sorted((p / "docs" / "archive").glob("HANDOFFS-through-*.md"))[0]
    rel = shard.relative_to(p).as_posix()
    t.sh(p, "git", "rm", "-q", "-f", "HANDOFFS.md")          # the loss: the live ledger is gone
    t.sh(p, "git", "add", "-A")
    t.sh(p, "git", "commit", "-qm", "trim, and delete the live ledger")
    assert not (p / "HANDOFFS.md").exists()
    v = t.sh(p, "bash", rel + ".verify.sh")
    print("trimmer:", trimmer)
    print("proof exit:", v.returncode)
    print("\n".join(v.stdout.strip().splitlines()[-4:]))
