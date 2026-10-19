"""Point 2 of the maintainer's comment on PR #94: does a planted `difflib.py` run under the proof?

Usage: python3 -I point2_planted_module.py <trimmer.py> <tests-module.py>

Builds the PR's `make_handoff_repo` fixture, trims it with the given trimmer, plants `difflib.py` and
`subprocess.py` at the repo root, each writing a marker file and then handing over to the real
standard-library module (so the proof still works), and runs the shard's proof twice: as the frozen script (`bash
<shard>.verify.sh`, which carries the generating trimmer's template) and through `--reverify`
(which re-renders today's template). Prints, for each, the exit code and whether the marker exists.
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

PLANTED = '''import importlib.util, sysconfig, os, sys
open("planted-ran-" + __name__, "w").write("the planted module ran\\n")
_real = os.path.join(sysconfig.get_paths()["stdlib"], __name__ + ".py")
_spec = importlib.util.spec_from_file_location(__name__, _real)
_mod = importlib.util.module_from_spec(_spec)
sys.modules[__name__] = _mod
_spec.loader.exec_module(_mod)
'''

with tempfile.TemporaryDirectory() as tmp:
    p = t.make_handoff_repo(tmp)
    r = t.run_trim(p, "--file", "HANDOFFS.md", "--cut", "2", "--write", "--today", "2026-02-01")
    assert "[WROTE]" in r.stdout, r.stdout
    shard = sorted((p / "docs" / "archive").glob("HANDOFFS-through-*.md"))[0]
    rel = shard.relative_to(p).as_posix()
    t.sh(p, "git", "add", "-A")
    t.sh(p, "git", "commit", "-qm", "trim")
    for name in ("difflib", "subprocess"):                              # untracked, at the repo root
        (p / (name + ".py")).write_text(PLANTED, encoding="utf-8")

    def ran():
        found = sorted(f.name[len("planted-ran-"):] for f in p.glob("planted-ran-*"))
        for f in p.glob("planted-ran-*"):
            f.unlink()
        return found

    print("trimmer:", trimmer)
    v = t.sh(p, "bash", rel + ".verify.sh")
    print("frozen proof   : exit %d, planted modules that ran: %s" % (v.returncode, ran() or "none"))
    rv = t.run_trim(p, "--reverify", rel)
    print("--reverify     : exit %d, planted modules that ran: %s" % (rv.returncode, ran() or "none"))
