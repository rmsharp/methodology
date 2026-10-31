#!/usr/bin/env python3
"""Evidence for docs/audits/2026-10-31-adopter-ledger-defects.md (S407).  READ-ONLY.

Four parts, all stdlib, all read-only on every adopter (the checker is always given a COPY in a
temporary directory; each original is hashed before and after):

  A. Survey: every HANDOFFS.md under ~/Development (a project's root, or its methodology/ directory),
     with its sha256, its project's git HEAD, whether the file differs from that HEAD, and the fork's
     bin/check-handoff findings sorted into classes.
  B. The version S352 read (2026-10-20): reproduced from each of the three projects' git history, so the
     comparison with that earlier audit rests on files and not on a note.
  C. Repair tests on copies: the smallest edit that clears each project's structure findings, and the
     tempting edits that do not.  Each test asserts the line it edits still reads as audited; if a project
     has moved or repaired it since, the test says SKIPPED and why, and prints nothing misleading.
  D. Exposure: ledgers that carry the text ```handoff in the middle of a line (prose), the way the
     damaged line in vscode_quarto_ext did.

Run from anywhere:  python3 docs/audits/2026-10-31-adopter-ledger-defects-evidence.py
Add -v to print every checker finding (about 200 KB) instead of the class counts.
"""
import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HOME = Path.home()
ROOT = HOME / "Development"
REPO = ROOT / "methodology"
CHECK = REPO / "bin" / "check-handoff"
VERBOSE = "-v" in sys.argv
THREE = ("church_growth", "mts-system", "vscode_quarto_ext")
TICKS = "`" * 3


def sh(*args, cwd=None):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


def check(path, *flags):
    rc, out = sh("python3", str(CHECK), "--file", str(path), "--allow-pending", *flags, cwd=REPO)
    return rc, out.replace(str(Path(path).parent) + "/", "")


def classes(out):
    """Sort a default-mode checker output into the classes the checker reports."""
    c = {"newest": 0, "structure": 0, "slots": 0, "ceiling": 0, "other": 0}
    for m in re.finditer(r"^check-handoff: FAIL — (.*?):$", out, re.M):
        h = m.group(1)
        n = re.match(r"(\d+) ", h)
        n = int(n.group(1)) if n else 1
        if "in the newest receipt" in h:
            c["newest"] = n
        elif "ledger-structure" in h:
            c["structure"] = n
        elif "answer slot" in h:
            c["slots"] = n
        elif "ceiling" in h:
            c["ceiling"] = 1
        else:
            c["other"] += n
    return c


def structure_errors(out):
    m = re.search(r"^check-handoff: FAIL — \d+ ledger-structure issue\(s\).*?:\n((?:  .*\n?)+)", out, re.M)
    return [l.strip() for l in m.group(1).splitlines() if l.strip().startswith("error:")] if m else []


def project_of(f):
    f = Path(f)
    if f.parent.parent == ROOT:
        return f.parent, "HANDOFFS.md"
    return f.parent.parent, "methodology/HANDOFFS.md"


ledgers = sorted(ROOT.glob("*/HANDOFFS.md")) + sorted(ROOT.glob("*/methodology/HANDOFFS.md"))
before = {str(f): sha(f) for f in ledgers}
tmp = Path(tempfile.mkdtemp(prefix="s407-"))

rc, out = sh("git", "log", "-1", "--format=%h", "--", "bin/check-handoff", cwd=REPO)
print("check-handoff: last commit touching it %s; fork HEAD %s" % (out.strip(), sh("git", "log", "-1", "--format=%h", cwd=REPO)[1].strip()))
print("ledgers found: %d" % len(ledgers))

# ---------------------------------------------------------------- A. survey
print("\n== A. SURVEY (default mode: the newest receipt's schema, the ledger's structure, `commit:` slots, size ceiling)")
print("%-26s %-9s %-8s %-9s %-4s %-6s | %6s %9s %5s %7s %5s" % (
    "ledger", "sha256", "bytes", "HEAD", "dirty", "exit", "newest", "structure", "slots", "ceiling", "other"))
for f in ledgers:
    proj, rel = project_of(f)
    rc0, head = sh("git", "-C", str(proj), "log", "-1", "--format=%h", cwd=REPO)
    head = head.strip() if rc0 == 0 else "no git"
    dirty = "yes" if rc0 == 0 and sh("git", "-C", str(proj), "status", "--porcelain", "--", rel)[1].strip() else "no"
    work = tmp / proj.name
    work.mkdir(exist_ok=True)
    (work / "HANDOFFS.md").write_bytes(f.read_bytes())
    rc, out = check(work / "HANDOFFS.md")
    c = classes(out)
    print("%-26s %-9s %-8d %-9s %-4s %-6s | %6d %9d %5d %7d %5d" % (
        proj.name, sha(f)[:8], f.stat().st_size, head, dirty, "exit %d" % rc,
        c["newest"], c["structure"], c["slots"], c["ceiling"], c["other"]))
    for e in structure_errors(out):
        print("      structure | " + e[:300])
    if VERBOSE:
        for l in out.splitlines():
            print("      | " + l[:300])
        rc2, out2 = check(work / "HANDOFFS.md", "--all")
        print("      | --all exit %d" % rc2)
        for l in out2.splitlines():
            print("      | " + l[:300])

# ---------------------------------------------------------------- B. the version S352 read
print("\n== B. THE VERSION S352 READ (the last ledger commit before 2026-10-20 23:00 -0500), the three projects")
for name in THREE:
    proj = ROOT / name
    rel = "methodology/HANDOFFS.md" if (proj / "methodology/HANDOFFS.md").exists() else "HANDOFFS.md"
    c = sh("git", "-C", str(proj), "log", "-1", "--before=2026-10-20 23:00 -0500", "--format=%h", "--", rel)[1].strip()
    when = sh("git", "-C", str(proj), "log", "-1", "--format=%ad", "--date=short", c)[1].strip()
    old = tmp / ("then-" + name + ".md")
    old.write_text(sh("git", "-C", str(proj), "show", "%s:%s" % (c, rel))[1])
    rc, out = check(old)
    since = sh("git", "-C", str(proj), "rev-list", "--count", "%s..HEAD" % c, "--", rel)[1].strip()
    lines_then = len(old.read_text().splitlines())
    lines_now = len((proj / rel).read_text().splitlines())
    errs = structure_errors(out)
    print("%s: version %s (%s); %d structure issue(s) then; ledger commits since: %s; lines then %d, now %d (%+d)" % (
        name, c, when, len(errs), since, lines_then, lines_now, lines_now - lines_then))
    for e in errs[:3]:
        print("      then | " + e[:230])
    if len(errs) > 3:
        print("      then | ... and %d more orphaned-field lines of the same receipt" % (len(errs) - 3))


# ---------------------------------------------------------------- C. repair tests on copies
def lines_of(name):
    proj = ROOT / name
    rel = "methodology/HANDOFFS.md" if (proj / "methodology/HANDOFFS.md").exists() else "HANDOFFS.md"
    return (proj / rel).read_text().split("\n")


def try_variant(name, label, expect, edit):
    """edit(lines) mutates a COPY's lines or raises AssertionError('why'); prints expected vs actual."""
    L = lines_of(name)
    try:
        edit(L)
    except AssertionError as e:
        print("  %-52s SKIPPED: %s" % (label, e))
        return
    p = tmp / ("var-" + name + ".md")
    p.write_text("\n".join(L))
    rc, out = check(p)
    errs = structure_errors(out)
    rc2, out2 = check(p, "--all")
    m = re.search(r"issue\(s\) across (\d+) receipt", out2)
    got = len(errs)
    print("  %-52s structure issues: %d (expected %s) [%s]; --all sees %s receipts" % (
        label, got, expect, "ok" if str(got) == str(expect) else "DIFFERS", m.group(1) if m else "?"))
    for e in errs:
        print("        | " + e[:215])


def need(L, n, startswith):
    assert L[n - 1].startswith(startswith), "line %d no longer starts %r (moved or repaired since the audit)" % (n, startswith)


print("\n== C. REPAIR TESTS ON COPIES (the adopter's own file is never written)")
print("church_growth (line 818 is the `session:` line of the block opened at 817):")


def cg(new):
    def e(L):
        need(L, 818, "session: S4")
        need(L, 796, "session: ad-hoc")
        L[817] = "session: " + new
    return e


try_variant("church_growth", "relabel 817 as `ad-hoc`", 1, cg("ad-hoc"))
try_variant("church_growth", "relabel 817 as `ad-hoc-2`", 0, cg("ad-hoc-2"))

print("mts-system (352 and 384 are the `session:` lines of the two `reconciled` receipts; 396 ends the S194 one):")


def mts(relabel, fence, style="ad-hoc"):
    def e(L):
        need(L, 352, "session: S195")
        need(L, 384, "session: S194")
        need(L, 396, "commit: 831549c")
        need(L, 662, "session: S179 (post-close-out housekeeping")
        if relabel:
            if style == "ad-hoc":
                L[383], L[351] = "session: ad-hoc-1", "session: ad-hoc-2"
            else:  # the project's own precedent at line 662: the owning session's id plus a parenthetical
                L[383] = "session: S194 (post-close-out commit; reconciled)"
                L[351] = "session: S195 (post-close-out commits; reconciled)"
        if fence:
            L.insert(396, TICKS)
    return e


try_variant("mts-system", "closing fence after line 396 only", 2, mts(False, True))
try_variant("mts-system", "relabel the two reconciled receipts only", 1, mts(True, False))
try_variant("mts-system", "both, ids `ad-hoc-1` and `ad-hoc-2`", 0, mts(True, True))
try_variant("mts-system", "both, ids in the project's own line-662 style", 0, mts(True, True, style="own"))

print("vscode_quarto_ext (line 907 is the one-line stub of the front-matter sentence):")


def vq(replace):
    def e(L):
        need(L, 907, "⚠ **The record grammar is FENCE-AWARE")
        if replace:
            L[906] = TICKS + "handoff"
        else:
            del L[906]
    return e


try_variant("vscode_quarto_ext", "delete line 907", 12, vq(False))
try_variant("vscode_quarto_ext", "replace line 907 with an opening fence", 0, vq(True))

# ---------------------------------------------------------------- D. exposure
print("\n== D. EXPOSURE: lines holding the text %shandoff NOT at the start of the line (prose), per ledger" % TICKS)
for f in ledgers + [REPO / "starter-kit" / "HANDOFFS.md"]:
    hits = [i + 1 for i, l in enumerate(f.read_text().split("\n")) if TICKS + "handoff" in l and not re.match(r"`{3,4}handoff", l)]
    if hits:
        print("  %-48s %d line(s): %s" % (str(f.relative_to(ROOT)), len(hits), hits[:6]))
print("  (every ledger not listed holds none, including the distributed seed starter-kit/HANDOFFS.md)")

# ---------------------------------------------------------------- end: nothing changed
after = {str(f): sha(f) for f in ledgers}
changed = [Path(k).parent.name for k in before if before[k] != after[k]]
print("\nadopter originals unchanged while this ran: %s" % ("yes (%d of %d)" % (len(ledgers), len(ledgers)) if not changed else "NO: " + ", ".join(changed)))
