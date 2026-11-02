#!/usr/bin/env python3
"""triage-evidence.py -- re-derive, from git objects, every line citation in upstream issues #100 and #101.

READ-ONLY. Reads blobs with `git show <ref>:<path>` and `git grep`; writes nothing; stdlib only.
Run from the repository root:  python3 docs/planning/issue100-101-evidence/triage-evidence.py

Three refs are read, because the issues cite v4.2 and say `main` moved:
  V42   f34769f3  the tag v4.2 (the issues say every citation is against it)
  MAIN  d50ce290  upstream/main when S410 read it
  FORK  HEAD      this fork's committed tree (blobs, not the working tree)

For each citation the line is one of:
  HOLDS   the expected text is on the cited line(s)
  MOVED   the text is in the file, not on the cited lines (the lines it IS on are printed)
  ABSENT  the text is nowhere in the file (or the file is not at that ref)
A check of the form NONE asserts a population of ZERO (a claim of the shape "no X names Y"); it passes
only when the search ran over a non-empty set of files, so an empty search is never read as a pass.

Exit 0 always: this prints a table for a human to read, it is not a gate.
"""
import re
import subprocess
import sys

REFS = {"V42": "f34769f3", "MAIN": "d50ce290", "FORK": "HEAD"}


def git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    return r.returncode, r.stdout


def blob(ref, path):
    rc, out = git("show", f"{ref}:{path}")
    return out.splitlines() if rc == 0 else None


def parse_span(span):
    a, _, b = span.partition("-")
    return int(a), int(b or a)


def at(ref, path, span, rx):
    """HOLDS / MOVED / ABSENT for `rx` on lines `span` of path at ref."""
    lines = blob(ref, path)
    if lines is None:
        return "ABSENT", "no such file at this ref"
    a, b = parse_span(span)
    window = "\n".join(lines[a - 1:b])
    if re.search(rx, window):
        return "HOLDS", f"{path}:{span}"
    hits = [str(i) for i, ln in enumerate(lines, 1) if re.search(rx, ln)]
    if hits:
        return "MOVED", f"{path} now at {','.join(hits[:5])}"
    return "ABSENT", path


def none(ref, rx, paths, flags="-i"):
    """Population-of-zero claim: how many matching lines over `paths` (a non-empty set of files)."""
    rc, files = git("ls-tree", "-r", "--name-only", ref, "--", *paths)
    files = [f for f in files.splitlines() if f]
    if not files:
        return "EMPTY-SET", "the search covered no files, so it asserts nothing"
    rc, out = git("grep", "-n", flags, "-E", rx, ref, "--", *files)
    n = len([ln for ln in out.splitlines() if ln])
    return ("ZERO" if n == 0 else f"{n} HITS"), f"{len(files)} files searched"


def row(tag, label, ref, res):
    print(f"[{tag}] {ref:<4} {res[0]:<9} {label} -- {res[1]}")


def span_check(tag, label, path, span, rx, refs=("V42", "MAIN", "FORK")):
    for r in refs:
        row(tag, label, r, at(REFS[r], path, span, rx))


def none_check(tag, label, rx, paths, refs=("V42", "MAIN", "FORK")):
    for r in refs:
        row(tag, label, r, none(REFS[r], rx, paths))


print("== refs ==")
for k, v in REFS.items():
    rc, out = git("rev-parse", "--short=8", v)
    print(f"{k} {v} -> {out.strip()}")

print("\n== #101 -- remove the Disclosure Hook ==")
span_check("101-a", "'this file wins' (SAFEGUARDS)", "starter-kit/SAFEGUARDS.md", "3", r"this file wins")
span_check("101-b", "Disclosure Hook section + trailer rule", "starter-kit/SAFEGUARDS.md", "184-187", r"Disclosure Hook[\s\S]*Co-Authored-By")
span_check("101-c", "commit-msg-selftest gate block", ".quality-gates.json", "80-86", r"commit-msg-selftest")
for r in ("V42", "MAIN", "FORK"):
    ls = blob(REFS[r], ".githooks/commit-msg")
    row("101-d", ".githooks/commit-msg is 78 lines", r, ("HOLDS" if ls is not None and len(ls) == 78 else "ABSENT", f"{None if ls is None else len(ls)} lines"))
span_check("101-e", "hook header says 'honesty counterpart of failure mode #16'", ".githooks/commit-msg", "1-4", r"honesty counterpart of failure mode #16")
span_check("101-f", "FM #16 row exists", "starter-kit/SESSION_RUNNER.md", "322", r"False credit / fabrication", refs=("V42", "MAIN"))
span_check("101-f", "FM #16 row exists", "starter-kit/SESSION_RUNNER.md", "325", r"False credit / fabrication", refs=("FORK",))
for r, ln in (("V42", 322), ("MAIN", 322), ("FORK", 325)):
    lines = blob(REFS[r], "starter-kit/SESSION_RUNNER.md") or []
    fm = lines[ln - 1] if len(lines) >= ln else ""
    row("101-g", "FM #16 row does NOT ask for a trailer", r, ("HOLDS" if fm and not re.search(r"co-authored|trailer", fm, re.I) else "ABSENT", "row read"))
span_check("101-h", "CLAUDE_TEMPLATE 'base files govern unless explicitly overridden'", "starter-kit/CLAUDE_TEMPLATE.md", "51", r"base files govern unless explicitly overridden")
span_check("101-i", "BOOTSTRAP names 'a gate removed' as refused", "starter-kit/BOOTSTRAP.md", "327", r"gate removed|removed")
for r in ("V42", "MAIN", "FORK"):
    rc, out = git("grep", "-n", "-E", r"gate .*removed", REFS[r], "--", "starter-kit/quality_ratchet.py")
    row("101-j", "quality_ratchet.py refuses a removed gate", r, ("HOLDS" if out.strip() else "ABSENT", out.splitlines()[0].split(":", 2)[1] if out.strip() else "no match"))
span_check("101-k", "FRAMEWORK_APPARATUS mentions trailers / model-report", "FRAMEWORK_APPARATUS.md", "433-436", r"Co-Authored-By|model-report")
span_check("101-l", "HANDOFFS seed mentions trailers / model-report", "starter-kit/HANDOFFS.md", "44-46", r"Co-Authored-By|model-report")
for r in ("V42", "MAIN", "FORK"):
    present = blob(REFS[r], "bin/model-report") is not None
    row("101-m", "bin/model-report is in the tree", r, ("HOLDS" if present else "ABSENT", "present" if present else "not in the tree"))
none_check("101-n", "'nothing in tests.sh, _manifest.py or other hooks names the hook'", r"commit-msg|Disclosure Hook|REQUIRE_COAUTHOR", ["bin/tests.sh", "bin/_manifest.py", ".githooks/pre-commit"])

print("\n== #101 -- what ELSE names the hook or the trailer on the FORK (files, hits; evidence/archives excluded) ==")
for label, rx in (("hook / section / env switch", r"commit-msg|Disclosure Hook|disclosure gate|REQUIRE_COAUTHOR"), ("the Co-Authored-By trailer", r"co-authored-by")):
    rc, out = git("grep", "-c", "-i", "-E", rx, "HEAD", "--", ".", ":!docs/archive", ":!CHANGELOG.md", ":!HANDOFFS.md", ":!dashboard_history.jsonl",
                  ":!docs/planning/overhead-replay", ":!docs/planning/*evidence*", ":!docs/planning/pr94-rewrite", ":!docs/planning/bl91-overhead-measurement")
    rows = sorted((ln[5:].rsplit(":", 1) for ln in out.splitlines()), key=lambda p: -int(p[1]))
    print(f"-- {label}: {len(rows)} files")
    for p, n in rows:
        print(f"   {n:>3}  {p}")

print("\n== #100 -- finding 1: bin/status trusts an unfetched checkout ==")
none_check("100-1a", "bin/status never asks the remote (ls-remote)", r"ls-remote", ["bin/status"])
span_check("100-1b", "seed budget's synced check reads a sibling checkout", "starter-kit/context-budget.json", "61-70", r"\.\./methodology/starter-kit/SESSION_RUNNER\.md")

print("\n== #100 -- finding 2: no protocol step runs context_budget.py ==")
span_check("100-2a", "context_budget.py header: measurement alone did not work", "starter-kit/context_budget.py", "17", r"MEASUREMENT ALONE WAS ALREADY PRESENT AND DID NOT WORK")
span_check("100-2b", "install-hook is opt-in", "starter-kit/context_budget.py", "1378", r"Opt-in")
span_check("100-2c", "FM #28 row", "starter-kit/SESSION_RUNNER.md", "334", r"Unbounded mandatory read", refs=("V42", "MAIN"))
span_check("100-2c", "FM #28 row", "starter-kit/SESSION_RUNNER.md", "337", r"Unbounded mandatory read", refs=("FORK",))
none_check("100-2d", "no session-read doc names the tool in any spelling",
           r"context[-_ ]budget", ["starter-kit/SESSION_RUNNER.md", "starter-kit/SAFEGUARDS.md", "ITERATIVE_METHODOLOGY.md", "HOW_TO_USE.md", "FRAMEWORK_APPARATUS.md", "workstreams"])
span_check("100-2e", "BOOTSTRAP names it only in update tables (:352 merge=union, :381-382 tables)", "starter-kit/BOOTSTRAP.md", "352-382", r"context-budget", refs=("V42", "MAIN"))

print("\n== #100 -- finding 3: the extraction instruction is an HTML comment ==")
for r in ("V42", "MAIN", "FORK"):
    lines = blob(REFS[r], "starter-kit/CLAUDE_TEMPLATE.md") or []
    i = next((n for n, ln in enumerate(lines) if "PROJECT_LEARNINGS" in ln), None)
    if i is None:
        row("100-3a", "PROJECT_LEARNINGS instruction sits inside <!-- -->", r, ("ABSENT", "not in the file")); continue
    j = i
    while j >= 0 and "<!--" not in lines[j]:
        j -= 1
    k = i
    while k < len(lines) and "-->" not in lines[k]:
        k += 1
    row("100-3a", "PROJECT_LEARNINGS instruction sits inside <!-- -->", r, ("HOLDS" if j >= 0 and k < len(lines) and i - j <= 3 else "ABSENT", f"comment opens line {j + 1}, closes line {k + 1}"))
span_check("100-3b", "BOOTSTRAP 'Keep CLAUDE.md lean'", "starter-kit/BOOTSTRAP.md", "200", r"Keep CLAUDE\.md lean", refs=("V42", "MAIN"))
span_check("100-3b", "BOOTSTRAP 'Keep CLAUDE.md lean'", "starter-kit/BOOTSTRAP.md", "218", r"Keep CLAUDE\.md lean", refs=("FORK",))
span_check("100-3c", "BOOTSTRAP customization table: 'nears CLAUDE.md's size budget'", "starter-kit/BOOTSTRAP.md", "421", r"nears CLAUDE\.md's size budget", refs=("V42", "MAIN"))
span_check("100-3c", "BOOTSTRAP customization table: 'nears CLAUDE.md's size budget'", "starter-kit/BOOTSTRAP.md", "439", r"nears CLAUDE\.md's size budget", refs=("FORK",))
span_check("100-3d", "seed budget names the file LEARNINGS.md (BOOTSTRAP: PROJECT_LEARNINGS.md)", "starter-kit/context-budget.json", "53", r'"path": "LEARNINGS\.md"', refs=("V42", "MAIN"))
span_check("100-3d", "seed budget names the file LEARNINGS.md (BOOTSTRAP: PROJECT_LEARNINGS.md)", "starter-kit/context-budget.json", "55", r'"path": "LEARNINGS\.md"', refs=("FORK",))
span_check("100-3e", "3C sends adopter learnings into CLAUDE.md", "starter-kit/SESSION_RUNNER.md", "222", r"Adopter project", refs=("V42", "MAIN"))
span_check("100-3e", "3C sends adopter learnings into CLAUDE.md", "starter-kit/SESSION_RUNNER.md", "230", r"Adopter project", refs=("FORK",))

print("\n== #100 -- finding 4: SESSION_NOTES.md transient or accumulating ==")
span_check("100-4a", "seed header: transient, overwritten", "starter-kit/SESSION_NOTES.md", "5", r"transient")
span_check("100-4b", "seed footer: history accumulates below this line", "starter-kit/SESSION_NOTES.md", "27", r"accumulates below this line", refs=("V42", "MAIN"))
span_check("100-4b", "seed footer: history accumulates below this line", "starter-kit/SESSION_NOTES.md", "31", r"accumulates below this line", refs=("FORK",))
span_check("100-4c", "runner 3D: 'Update SESSION_NOTES.md'", "starter-kit/SESSION_RUNNER.md", "239", r"Update `SESSION_NOTES\.md`", refs=("V42", "MAIN"))
span_check("100-4c", "runner 3D: 'Update SESSION_NOTES.md'", "starter-kit/SESSION_RUNNER.md", "247", r"Update `SESSION_NOTES\.md`", refs=("FORK",))
span_check("100-4d", "ITERATIVE_METHODOLOGY: rewritten, not merged", "ITERATIVE_METHODOLOGY.md", "400", r"rewritten, not merged")
span_check("100-4e", "FRAMEWORK_APPARATUS: transient handoff", "FRAMEWORK_APPARATUS.md", "535", r"transient handoff", refs=("V42", "MAIN"))
span_check("100-4f", "HANDOFFS seed: transient", "starter-kit/HANDOFFS.md", "6", r"transient", refs=("V42", "MAIN"))
span_check("100-4g", "budget config records UPDATE read as ADD", "starter-kit/context-budget.json", "46", r"UPDATE", refs=("V42", "MAIN"))
span_check("100-4g", "budget config records UPDATE read as ADD", "starter-kit/context-budget.json", "48", r"UPDATE", refs=("FORK",))

print("\n== #100 -- finding 5: no rule for work after the 3G STOP ==")
span_check("100-5a", "runner has the 3G heading", "starter-kit/SESSION_RUNNER.md", "288", r"3G: Report and STOP", refs=("V42", "MAIN"))
span_check("100-5a", "runner has the 3G heading", "starter-kit/SESSION_RUNNER.md", "296", r"3G: Report and STOP", refs=("FORK",))
none_check("100-5b", "runner names no rule for a new task after the STOP", r"new task after|after the STOP|is a new session|phase 0 again|re-run phase 0|follow-on session", ["starter-kit/SESSION_RUNNER.md"])
span_check("100-5c", "SAFEGUARDS: Close-Out Completeness Hook is the recommended Stop hook", "starter-kit/SAFEGUARDS.md", "175", r"Close-Out Completeness Hook")

print("\n== #100 -- finding 6 and the smaller points: the trimmer ==")
for r in ("V42", "MAIN", "FORK"):
    lines = blob(REFS[r], "starter-kit/methodology_trim.py") or []
    def find(rx):
        return [str(i) for i, ln in enumerate(lines, 1) if re.search(rx, ln)]
    row("100-6a", "P1_NO_LEDGER refusal", r, ("HOLDS" if find(r'result\.add\("P1_NO_LEDGER"') else "ABSENT", f"line {','.join(find(r'result.add.*P1_NO_LEDGER')[:2])}"))
    row("100-6b", "SRF_UNDEFINED reported", r, ("HOLDS" if find(r'SRF_UNDEFINED') else "ABSENT", f"line {','.join(find(r'result.add.*SRF_UNDEFINED')[:2])}"))
    row("100-s1", "mkstemp then os.replace (no chmod of the ledger)", r, ("HOLDS" if find(r"tempfile\.mkstemp") and find(r"os\.replace\(tmp, path\)") else "ABSENT", f"mkstemp {','.join(find('tempfile.mkstemp')[:1])}, replace {','.join(find(r'os.replace.tmp, path')[:1])}"))
    row("100-s2", "front-matter field 'This file currently holds **N**' expected", r, ("HOLDS" if find(r"This file currently holds") else "ABSENT", f"line {','.join(find('This file currently holds')[:1])}"))
span_check("100-6c", "BOOTSTRAP: seeds committed under --mode=ignore", "starter-kit/BOOTSTRAP.md", "72", r"not the seeded ones", refs=("V42", "MAIN"))

print("\n== #100 -- smaller point 3: the dashboard's size risks (the fork carries the rows #99 (d) adds) ==")
none_check("100-s3a", "size-risk rows reading 'past the read limits' ('lines) — past')", r"lines\) — past", ["starter-kit/methodology_dashboard.py"])
none_check("100-s3b", "the older 'Large files detected' row", r"Large files detected \(", ["starter-kit/methodology_dashboard.py"])

print("\n== #100 -- finding 3: which tools already know the name PROJECT_LEARNINGS.md (the budget seed says LEARNINGS.md) ==")
for r in ("MAIN", "FORK"):
    rc, out = git("grep", "-c", "PROJECT_LEARNINGS", REFS[r], "--", "bin", "tools", "starter-kit")
    print(f"   {r}: " + ", ".join(ln.split(":", 1)[1] if ln.count(":") == 1 else ln.split(":", 1)[1] for ln in out.splitlines()))

print("\n== #100 -- smaller point 1 re-run on the FORK's own tree: modes of files the trimmer wrote ==")
import os, stat, glob
modes = {}
for p in glob.glob("docs/archive/*"):
    if os.path.isfile(p):
        m = stat.S_IMODE(os.stat(p).st_mode)
        modes[oct(m)] = modes.get(oct(m), 0) + 1
for m, n in sorted(modes.items()):
    print(f"   {n:>4} files in docs/archive with mode {m}")
print("   (git records only the executable bit, so a 0600 file is invisible in a commit and gone in a fresh clone;")
print("    it is a property of the working tree the trimmer ran in.)")
