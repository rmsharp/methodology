"""The three things the maintainer's comment on PR #94 says it did not test: symlinks, regex
backtracking, repo-local git config. What this probe saw, without changing any code.

Usage: python3 -I probe_untested.py <trimmer.py> <tests-module.py>

(1) Regex backtracking. Every stub marker in the ledger table is searched over a record of 400,000
    lines (about 16 MB for the lines alone) that does NOT contain the marker, the worst case for a
    scan; the elapsed time is printed. HANDOFFS.md's marker is the one this review changed.
(2) Symlinks. A trimmed repository in which the SHARD, then the LIVE ledger, is a symlink: what the
    proof says. Printed, not judged.
(3) Repo-local git config. A repository whose .git/config sets `diff.external`, `core.pager`,
    `core.fsmonitor` and `core.hooksPath` to a script that writes a marker file: does the proof's
    git use run it? (The proof calls `git rev-parse`, `git log`, `git ls-tree` and `git show`.)
"""
import importlib.util
import os
import pathlib
import sys
import tempfile
import time

trimmer, tests = sys.argv[1], sys.argv[2]
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("t", tests)
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
t.TRIM_PY = pathlib.Path(trimmer)
tspec = importlib.util.spec_from_file_location("trim", trimmer)
trim = importlib.util.module_from_spec(tspec)
tspec.loader.exec_module(trim)

print("trimmer:", trimmer)

# (1) backtracking
print("\n== 1. each stub marker searched over a 400,000-line record with no marker in it")
body = ("x" * 40 + "\n") * 400000
for name, spec_ in sorted(trim.LEDGERS.items()):
    m = spec_.stub_marker
    if m is None:
        print("   %-16s declares no marker" % name)
        continue
    if name == "HANDOFFS.md":
        rec = "```handoff\nsession: S1\nstatus: complete\n" + body + "```\n"
    else:
        rec = "### What Session 1 Did\n**Deliverable:** x\n" + body
    t0 = time.monotonic()
    hit = m.search(rec)
    print("   %-16s %.3f s, matched: %s" % (name, time.monotonic() - t0, bool(hit)))

# (2) symlinks
print("\n== 2. a symlink where the proof reads a file")


def symlinked(what, committed):
    """Trim; then make `what` ("shard" or "live") a symlink to a copy of its content; prove."""
    with tempfile.TemporaryDirectory() as tmp:
        p = t.make_handoff_repo(tmp)
        r = t.run_trim(p, "--file", "HANDOFFS.md", "--cut", "2", "--write", "--today", "2026-02-01")
        assert "[WROTE]" in r.stdout, r.stdout
        shard = sorted((p / "docs" / "archive").glob("HANDOFFS-through-*.md"))[0]
        rel = shard.relative_to(p).as_posix()
        target = shard if what == "shard" else p / "HANDOFFS.md"
        side = p / ("real-" + what + ".md")
        side.write_bytes(target.read_bytes())
        target.unlink()
        os.symlink(os.path.relpath(str(side), str(target.parent)), str(target))
        if committed:
            t.sh(p, "git", "add", "-A")
            t.sh(p, "git", "commit", "-qm", "trim, with the %s a symlink" % what)
        v = t.sh(p, "bash", rel + ".verify.sh")
        last = [ln for ln in v.stdout.splitlines() if ln.strip()][-1][:130]
        return v.returncode, last


for what in ("shard", "live"):
    for committed in (False, True):
        rc, last = symlinked(what, committed)
        print("   %-5s is a symlink, trim %-11s: proof exit %d; last line: %s"
              % (what, "committed" if committed else "uncommitted", rc, last))

# (3) repo-local git config
print("\n== 3. repo-local git config that would run a program")
with tempfile.TemporaryDirectory() as tmp:
    p = t.make_handoff_repo(tmp)
    r = t.run_trim(p, "--file", "HANDOFFS.md", "--cut", "2", "--write", "--today", "2026-02-01")
    assert "[WROTE]" in r.stdout, r.stdout
    shard = sorted((p / "docs" / "archive").glob("HANDOFFS-through-*.md"))[0].relative_to(p).as_posix()
    t.sh(p, "git", "add", "-A")
    t.sh(p, "git", "commit", "-qm", "trim")
    prog = p / "evil.sh"
    prog.write_text("#!/bin/sh\necho ran >> %s/git-config-ran.txt\nexit 0\n" % tmp, encoding="utf-8")
    prog.chmod(0o755)
    for k, v_ in (("diff.external", str(prog)), ("core.pager", str(prog)), ("core.fsmonitor", str(prog)),
                  ("core.sshCommand", str(prog)), ("core.editor", str(prog))):
        t.sh(p, "git", "config", k, v_)
    marker = pathlib.Path(tmp) / "git-config-ran.txt"
    v = t.sh(p, "bash", shard + ".verify.sh")
    print("   proof exit %d; a configured program ran: %s" % (v.returncode, marker.exists()))
    if marker.exists():
        print("   it ran %d time(s)" % len(marker.read_text().splitlines()))
