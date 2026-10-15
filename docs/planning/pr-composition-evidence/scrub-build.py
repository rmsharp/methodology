#!/usr/bin/env python3
"""Build one scrub commit on a scratch clone of pr2/candidate (S324). Never touches the fork's working tree.

    python3 -I docs/planning/pr-composition-evidence/scrub-build.py CLONE GROUP [--write]

CLONE is a `git clone --no-local --branch pr2/candidate <fork> CLONE`; its HEAD is the parent (the candidate's tip, or the
previous scrub commit). GROUP names the files of one commit (at most 5, SAFEGUARDS' per-commit cap). The edits are
EXPLICIT, one per line, in scrub-edits.txt beside this script:

    @@ path/of/the/file          starts a file's section
    123|the new text of line 123  everything after the first bar, verbatim (leading spaces included)
    123|~new text               a leading ~ keeps the original line's indentation (tabs or spaces) and replaces the rest
    124|<<DELETE>>               the line goes
    @@ = path-of-an-identical-twin  the file takes the same bytes as its twin (the dashboard pair)

The builder REFUSES (exit 2, nothing written) when: a file of the group is not byte-identical to the candidate's blob
(drift); an edit names a line past the end of its file; an edit leaves a fork token on the line it rewrites; or a file
is not a plain Python or shell file the inertness proof can read. It then PROVES the edit inert, per file:
  Python: the token stream with comments, blank lines and docstring-like statements removed is equal before and after;
  shell:  the file with its full-line comments removed is equal before and after.
`--write` stages the group and commits it with scrub-msgs/GROUP.txt and the trailer, with no hooks (the candidate's
commits never touch CHANGELOG.md, so the fork's ledger hook would refuse them).
"""
import io
import os
import re
import subprocess
import sys
import tokenize

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
CANDIDATE_TIP = "5afc962"

GROUPS = {
    "C1": ["starter-kit/methodology_dashboard.py", "tools/methodology_dashboard.py", "tools/test_methodology_dashboard.py"],
    "C2": ["starter-kit/methodology_trim.py", "tools/test_methodology_trim.py"],
    "C3": ["bin/migrate-layout", "tools/test_migrate_layout.py"],
    "C4": ["starter-kit/quality_ratchet.py", "tools/test_quality_ratchet.py", "starter-kit/context_budget.py",
           "tools/test_context_budget.py"],
    "C5": ["tools/layout_resolver.py", "tools/test_layout_resolver.py", "tools/layout_fixtures.py",
           "tools/test_sync_layouts.py", "tools/test_checker_layouts.py"],
    "C6": ["bin/sync", "bin/status", "bin/check-links", "bin/_manifest.py", "bin/_manifest_reader.py"],
    "C7": ["bin/tests.sh", ".githooks/pre-commit", "bin/check-layout-literals", "bin/check-ledger", "bin/check-handoff"],
}
TWINS = {"tools/methodology_dashboard.py": "starter-kit/methodology_dashboard.py"}
INERT = ("comment", "tcomment", "docstring", "prose")

STRICT = [
    r"\bBL-\d+", r"\bS\d{2,3}\b", r"[Ff]ork [Ll]earning|(?<![Ff]ork )[Ll]earning #(?:1[4-9]|[2-9]\d|\d{3})\b", r"docs/(?:planning|audits)/(?!BACKLOG\.md\b)",
    r"\bP\d{1,2}\b(?= |\)|,|:|\.|\]|$)",
    r"\b[Pp]lan (?:[0-9§]|[CD]\d|section)|\bplan's\b|§ ?\d|\bD[1-9]\b(?= |\)|,|:|\.)|\bC\d\b(?= |\)|,|:|\.)",
    r"nprcgenekeepr|vscode_quarto_ext|mts-system|wsfct|feedback-loop-comparison|model_project_constructor|claude_work|church_growth|chat_verification|Philippians|airqino|dalia_martinez",
    r"\b[\w-]+-plan\.md|findings-register(?:\.md)?|ledger-trimmer-design(?:\.md)?|f24-(?:oracle|differential)\.py",
    r"(?<![\w-])[FX]\d{1,2}\b(?![\w-])", r"\b[Ss]ections? \d+(?:\.\d+)*[a-z]?\b",
]


def git(clone, *a, check=True, text=True):
    r = subprocess.run(["git", "-C", clone] + list(a), capture_output=True, text=text)
    if check and r.returncode:
        sys.exit("git %s failed: %s" % (" ".join(a), r.stderr.strip()))
    return r.stdout


def refuse(msg):
    sys.exit("REFUSED: %s" % msg)


LEFT = {}  # path -> {line: reason}: flagged lines left as they are, on purpose


def parse_edits(path):
    out, cur = {}, None
    for raw in open(path, encoding="utf-8").read().split("\n"):
        if raw.startswith("@@ = "):
            out[cur] = ("twin", raw[5:].strip())
        elif raw.startswith("@left "):
            _tag, path, nums, reason = raw.split(" ", 3)
            LEFT.setdefault(path, {}).update({int(n): reason for n in nums.split(",")})
        elif raw.startswith("@@ "):
            cur = raw[3:].strip()
            out.setdefault(cur, {})
        elif cur and re.match(r"^\d+\|", raw):
            n, text = raw.split("|", 1)
            out[cur][int(n)] = text
        elif raw.strip() and not raw.startswith("#"):
            refuse("scrub-edits.txt: unreadable line %r" % raw[:60])
    return out


def index(name="scrub-derive-output.txt"):
    """{path: {line: (class, strict classes)}} from the saved derivation."""
    out = {}
    for ln in open(os.path.join(HERE, name), encoding="utf-8"):
        m = re.match(r"^([^ ]+):(\d+): <([a-z?]+)> \[([A-Z,]+)\] ", ln)
        if m:
            out.setdefault(m.group(1), {})[int(m.group(2))] = (m.group(3), m.group(4))
    return out


def is_python(path, text):
    return path.endswith(".py") or (not os.path.splitext(path)[1] and text.startswith("#!") and "python" in text.split("\n", 1)[0])


def py_stream(text):
    """The token stream without comments, blank lines and docstring-like statements."""
    toks = list(tokenize.generate_tokens(io.StringIO(text).readline))
    skip = (tokenize.NEWLINE, tokenize.NL, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT, tokenize.ENDMARKER)
    logical, cur = [], []
    for t in toks:
        if t.type == tokenize.NEWLINE:
            logical.append(cur)
            cur = []
        else:
            cur.append(t)
    logical.append(cur)
    out = []
    for lg in logical:
        body = [t for t in lg if t.type not in skip]
        if body and all(t.type == tokenize.STRING for t in body):
            out.append(("DOCSTRING",))
        else:
            out.extend((t.type, t.string) for t in lg if t.type not in (tokenize.COMMENT, tokenize.NL))
            out.append(("NEWLINE",))
    return out


def sh_stream(text):
    return [ln for ln in text.split("\n") if not re.match(r"^\s*#", ln) or ln.startswith("#!")]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    write = "--write" in sys.argv
    if len(args) != 2 or args[1] not in GROUPS:
        sys.exit(__doc__)
    clone, group = args
    files = GROUPS[group]
    if len(files) > 5:
        refuse("group %s has %d files; the per-commit cap is 5" % (group, len(files)))
    if git(clone, "status", "--porcelain").strip():
        refuse("the clone is not clean")
    edits = parse_edits(os.path.join(HERE, "scrub-edits.txt"))
    report, new_text = [], {}
    idx = index()
    for f in files:
        have = git(clone, "rev-parse", "HEAD:" + f).strip()
        want = git(clone, "rev-parse", "%s:%s" % (CANDIDATE_TIP, f)).strip()
        if have != want:
            refuse("%s is not the candidate's blob (HEAD %s, %s %s): drift" % (f, have[:9], CANDIDATE_TIP, want[:9]))
        old = git(clone, "show", "HEAD:" + f)
        if not (is_python(f, old) or f.endswith(".sh") or old.startswith("#!")):
            refuse("%s: not a file the inertness proof reads" % f)
        spec = edits.get(f)
        if spec is None:
            refuse("%s has no section in scrub-edits.txt" % f)
        if isinstance(spec, tuple):  # a twin: the same edits as its partner
            spec = edits[spec[1]]
        lines = old.split("\n")
        changed = deleted = 0
        for n in sorted(spec, reverse=True):
            if not 1 <= n <= len(lines):
                refuse("%s: line %d is past the end (%d lines)" % (f, n, len(lines)))
            text = spec[n]
            if text == "<<DELETE>>":
                del lines[n - 1]
                deleted += 1
            else:
                if text.startswith("~"):  # keep the original line's indentation
                    orig = lines[n - 1]
                    text = orig[:len(orig) - len(orig.lstrip())] + text[1:]
                orig = lines[n - 1]
                if orig[:len(orig) - len(orig.lstrip())] != text[:len(text) - len(text.lstrip())]:
                    refuse("%s:%d: the edit changes the line's indentation (start the text with ~ to keep it): %s" % (f, n, text[:80]))
                for p in STRICT:
                    if re.search(p, text):
                        refuse("%s:%d: the new text still carries a fork token (%s): %s" % (f, n, p, text[:100]))
                lines[n - 1] = text
                changed += 1
        flagged = idx.get(f, {})
        # phase A (this builder) is the INERT scrub: a flagged line in a string or in code is output-bearing text, decided in
        # its own later commit against the tip this phase leaves, so it is not accounted for here
        unaccounted = sorted(n for n, (cls, _k) in flagged.items()
                             if cls in INERT and n not in spec and n not in LEFT.get(f, {}))
        stale = sorted(n for n in LEFT.get(f, {}) if n in spec)
        if stale:
            refuse("%s: lines %s are both edited and listed as left" % (f, stale))
        if unaccounted:
            refuse("%s: %d flagged line(s) neither edited nor left on purpose: %s" % (f, len(unaccounted), unaccounted[:12]))
        nt = "\n".join(lines)
        # the proof
        try:
            if is_python(f, old):
                ok = py_stream(old) == py_stream(nt)
                kind = "token stream (comments, blanks, docstring-like statements removed)"
            else:
                ok = sh_stream(old) == sh_stream(nt)
                kind = "file minus full-line comments"
        except (tokenize.TokenError, IndentationError, SyntaxError) as e:
            refuse("%s: the proof could not read it: %s" % (f, e))
        if not ok:
            refuse("%s: NOT INERT: the %s differs before and after" % (f, kind))
        new_text[f] = nt
        report.append("  %-44s %3d rewritten %3d deleted %3d left  inert by %s: equal" % (f, changed, deleted, len(LEFT.get(f, {})), kind.split(" (")[0]))
    for twin, partner in TWINS.items():
        if twin in new_text and partner in new_text and new_text[twin] != new_text[partner]:
            refuse("the twins %s and %s would differ" % (twin, partner))
    print("group %s on %s: %d file(s)" % (group, git(clone, "rev-parse", "--short", "HEAD").strip(), len(files)))
    print("\n".join(report))
    if not write:
        print("dry run: nothing written")
        return
    for f, nt in new_text.items():
        with open(os.path.join(clone, f), "w", encoding="utf-8", newline="") as fh:
            fh.write(nt)
    git(clone, "add", "--", *files)
    msg = open(os.path.join(HERE, "scrub-msgs", group + ".txt"), encoding="utf-8").read().rstrip("\n")
    msg += "\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\n"
    r = subprocess.run(["git", "-C", clone, "-c", "core.hooksPath=/dev/null", "commit", "-q", "-F", "-"], input=msg,
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit("commit failed: " + r.stderr.strip())
    print("committed %s: %s" % (git(clone, "rev-parse", "--short", "HEAD").strip(), msg.split("\n", 1)[0]))


main()
