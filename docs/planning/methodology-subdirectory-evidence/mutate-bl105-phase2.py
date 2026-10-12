#!/usr/bin/env python3
"""S303 mutation round over the BL-105 phase 2 code in bin/migrate-layout (32 distinct mutants; M26 was dropped, a no-op).

Runs ONLY in a --no-local clone it is given (never the working tree it was written in): it copies the two files under test
into the clone, applies one textual mutant at a time (each `old` must occur exactly once, or the mutant is reported as
not applicable), runs the new test classes with failfast, restores the file, and prints one line per mutant.
  mutate-s303.py <clone> <source-repo> [mutant ids...]
"""
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

CLONE, SRC = Path(sys.argv[1]), Path(sys.argv[2])
ONLY = set(sys.argv[3:])

if len(sys.argv) < 3:
    sys.exit(__doc__)
_top = subprocess.run(["git", "-C", str(CLONE), "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
if not _top or Path(_top).resolve() == SRC.resolve() or CLONE.resolve() == SRC.resolve():
    sys.exit("refusing: %s is not a separate clone (this script overwrites bin/migrate-layout there, one mutant at a time)" % CLONE)
TOOL = CLONE / "bin" / "migrate-layout"
TESTS = CLONE / "tools"
CLASSES = ["TestTheLinkRules", "TestTheCompanionOfAProjectThatHasNotAdoptedTheMethodology", "TestTheCompanionRule",
           "TestATopUpOnAMigratedTree", "TestTheLiveLinksAMoveBreaks"]

MUTANTS = [
    ("M01", "tier 1 moves the companion",
     'if tier in ("2", "all") and kind in ("legacy", "new"):\n        for name in COMPANIONS:',
     'if kind in ("legacy", "new"):\n        for name in COMPANIONS:'),
    ("M02", "a project with no runner moves the companion",
     'if tier in ("2", "all") and kind in ("legacy", "new"):\n        for name in COMPANIONS:',
     'if tier in ("2", "all"):\n        for name in COMPANIONS:'),
    ("M03", "an untracked file is planned as a move",
     'elif old_here and name in tracked:\n                add(name, new, "companion")',
     'elif old_here:\n                add(name, new, "companion")'),
    ("M04", "a destination that exists is not a collision",
     'if old_here and new_here:\n                collisions.append(new)\n            elif old_here and name in tracked:',
     'if old_here and new_here:\n                pass\n            elif old_here and name in tracked:'),
    ("M05", "any companion move makes it a top-up",
     'return bool(moves) and all(m["kind"] == "companion" for m in moves)',
     'return bool(moves) and any(m["kind"] == "companion" for m in moves)'),
    ("M06", "a top-up maps the generated names too",
     'if tier in ("2", "all") and not is_top_up(moves):',
     'if tier in ("2", "all"):'),
    ("M07", "the top-up ledger entry is never used",
     'if is_top_up(moves):\n        names = ", ".join("`%s`" % m["src"] for m in moves)',
     'if False:\n        names = ", ".join("`%s`" % m["src"] for m in moves)'),
    ("M08", "the top-up commit subject is never used",
     'if is_top_up(moves):\n        subject = ',
     'if False:\n        subject = '),
    ("M09", "a ledger's links are listed",
     'or hit_category(path) == "ledger":\n            continue\n        try:',
     'or False:\n            continue\n        try:'),
    ("M10", "a file the tool rewrites is listed",
     'skip = set(moved) | {r.path for r in rewrites}',
     'skip = set(moved)'),
    ("M11", "a file the tool moves is listed",
     'skip = set(moved) | {r.path for r in rewrites}',
     'skip = {r.path for r in rewrites}'),
    ("M12", "a fenced block is not skipped",
     '        if fence is not None:\n            if f and f.group(1)[0] == fence[0]',
     '        if False:\n            if f and f.group(1)[0] == fence[0]'),
    ("M13", "a path that climbs out of the root resolves",
     'if path in (".", "..") or path.startswith("../"):',
     'if path in (".", ".."):'),
    ("M14", "26 sites are shown",
     'for s in ll["sites"][:SITES_SHOWN]:',
     'for s in ll["sites"][:SITES_SHOWN + 1]:'),
    ("M15", "exactly 25 says there are more",
     'if ll["count"] > SITES_SHOWN:',
     'if ll["count"] >= SITES_SHOWN:'),
    ("M16", "a link with a space after the parenthesis is not read",
     'INLINE_LINK_RE = re.compile(r"\\]\\(\\s*(?:<',
     'INLINE_LINK_RE = re.compile(r"\\]\\((?:<'),
    ("M17", "a config is never looked for under methodology/",
     '(NEW_DIR + "/" + name, name) if kind == "new" else (name,)',
     '(name,)'),
    ("M18", "an untracked copy is not named",
     'left.append({"path": name, "reason": "not tracked by git: this tool moves files git tracks; it stays"})',
     'pass'),
    ("M19", "a percent-encoded path is not decoded",
     '    t = unquote(t)\n',
     '    t = t\n'),
    ("M20", "a URL is resolved as a path",
     'or re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", t):',
     'or False:'),
    ("M21", "the live links are never computed",
     'report["live_links"] = live_links(root, moves, rewrites)',
     'pass'),
    ("M22", "tier 2 alone does not move the companion",
     'if tier in ("2", "all") and kind in ("legacy", "new"):\n        for name in COMPANIONS:',
     'if tier == "all" and kind in ("legacy", "new"):\n        for name in COMPANIONS:'),
    ("M23", "a reference definition is not read",
     '        ref = REF_DEF_RE.match(line)\n        if ref:',
     '        ref = None\n        if ref:'),
    ("M24", "an angle-bracket target is not read",
     'm.group(1) if m.group(1) is not None else m.group(2)))',
     'm.group(2) or ""))'),
    ("M25", "the live_links key is missing from a refused or empty report",
     '"not_rewritten": {}, "live_links": {"count": 0, "files": 0, "sites": []},',
     '"not_rewritten": {},'),
    ("M27", "the top-up entry plural is flipped",
     'len(moves), "" if len(moves) == 1 else "s", sha, edited))',
     'len(moves), "s" if len(moves) == 1 else "", sha, edited))'),
    ("M28", "the commit subject plural is flipped",
     'report["tier"], len(moves), "" if len(moves) == 1 else "s")\n    else:',
     'report["tier"], len(moves), "s" if len(moves) == 1 else "")\n    else:'),
    ("M29", "a file with no link counts as a file",
     'out["files"] += 1 if found else 0',
     'out["files"] += 1'),
    ("M30", "the site text is the wrong line",
     '"text": lines[number - 1].strip()[:200]',
     '"text": lines[number - 2].strip()[:200]'),
    ("M31", "a root-relative link is joined to the document's directory",
     'posixpath.normpath(t[1:] if t.startswith("/") else posixpath.join(posixpath.dirname(doc), t))',
     'posixpath.normpath(posixpath.join(posixpath.dirname(doc), t))'),
    ("M32", "an anchor is not stripped",
     't = target.strip().split("#", 1)[0].split("?", 1)[0]',
     't = target.strip().split("?", 1)[0]'),
    ("M33", "a query is not stripped",
     't = target.strip().split("#", 1)[0].split("?", 1)[0]',
     't = target.strip().split("#", 1)[0]'),
]


def run_tests():
    names = ["test_migrate_layout." + c for c in CLASSES]
    r = subprocess.run([sys.executable, "-B", "-m", "unittest", "-f", *names], cwd=TESTS, capture_output=True, text=True)
    out = r.stdout + r.stderr
    first = re.search(r"^(?:FAIL|ERROR): (\w+) \(test_migrate_layout\.(\w+)\)", out, re.M)
    return r.returncode, (first.group(2) + "." + first.group(1)) if first else "", re.search(r"^Ran \d+ tests?", out, re.M)


def main():
    clean = (SRC / "bin" / "migrate-layout").read_text(encoding="utf-8")
    shutil.copy2(SRC / "tools" / "test_migrate_layout.py", TESTS / "test_migrate_layout.py")
    for mid, what, old, new in MUTANTS:
        if ONLY and mid not in ONLY:
            continue
        if clean.count(old) != 1:
            print("%s NOT-APPLICABLE (%d matches): %s" % (mid, clean.count(old), what), flush=True)
            continue
        TOOL.write_text(clean.replace(old, new), encoding="utf-8")
        t0 = time.time()
        try:
            code, killer, ran = run_tests()
        finally:
            TOOL.write_text(clean, encoding="utf-8")
        verdict = "SURVIVED" if code == 0 else "killed"
        print("%s %s (%ds) %s%s: %s" % (mid, verdict, time.time() - t0, "by " if killer else "", killer, what), flush=True)


if __name__ == "__main__":
    main()
