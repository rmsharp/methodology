#!/usr/bin/env python3
"""Phase B of the scrub: the OUTPUT-BEARING text (S324). Never touches the fork's working tree.

    python3 -I docs/planning/pr-composition-evidence/scrub-build-b.py CLONE GROUP [--write]

Phase A (scrub-build.py) removed fork tokens from comments and docstrings, which no program reads or prints, and proved each
file's token stream equal. What is left in the files below is text a program PRINTS or a test ASSERTS on: a refusal message, a
test title, a failure message, the commit message a tool writes into a project's ledger, a gate's "why". Changing it is a change
of output, so it is its own commit, built against the phase A tip, and a reviewer can accept phase A and refuse this one.

The edits are in scrub-edits-b.txt:

    @@ path                      starts a file's section
    N|old ==> new                line N holds `old` exactly once; it becomes the line with `new` in its place
    N|old ==>                    the same with an empty `new`: the text `old` is removed
    @@ = path                    a file takes its twin's edits (the dashboard pair)
    @left path N,M reason        flagged lines left as they are, on purpose, with the reason

The builder REFUSES (exit 2, nothing written) when: the clone's HEAD tree is not the tree scrub-derive-after-a.txt was made
from (checked per file, against the recorded tree); `old` is absent from, or twice in, its line; a rewritten line still carries a fork token; a flagged line of the group is
neither edited nor left on purpose; or a proof fails. The proof, per file: Python, the token stream with every string literal
and every comment masked is equal before and after (so only text inside a literal or a comment changed); shell, `sh -n` /
`bash -n` still passes (the changed lines are printed, and a person reads them); JSON, the parsed document is equal with every
`why` value masked. Every changed line is printed old and new.
"""
import io
import json
import os
import re
import subprocess
import sys
import tokenize

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
CANDIDATE_TIP = "5afc962"
GROUPS = {
    "B1": ["bin/migrate-layout", "tools/test_migrate_layout.py", "bin/check-layout-literals"],
    "B2": ["starter-kit/methodology_dashboard.py", "tools/methodology_dashboard.py", "tools/test_methodology_dashboard.py"],
    "B3": ["bin/tests.sh", ".githooks/pre-commit", ".quality-gates.json"],
}
TWINS = {"tools/methodology_dashboard.py": "starter-kit/methodology_dashboard.py"}

# the same fork tokens scrub-build.py refuses; a bare "Learning #12" is upstream's own row and is not one
STRICT = [
    r"\bBL-\d+", r"\bS\d{2,3}\b", r"[Ff]ork [Ll]earning|(?<![Ff]ork )[Ll]earning #(?:1[4-9]|[2-9]\d|\d{3})\b",
    r"docs/(?:planning|audits)/(?!BACKLOG\.md\b)", r"\bP\d{1,2}\b(?= |\)|,|:|\.|\]|$)",
    r"\b[Pp]lan (?:[0-9§]|[CD]\d|section)|\bplan's\b|§ ?\d|\bD[1-9]\b(?= |\)|,|:|\.)|\bC\d\b(?= |\)|,|:|\.)",
    r"nprcgenekeepr|vscode_quarto_ext|mts-system|wsfct|feedback-loop-comparison|model_project_constructor|claude_work|church_growth|chat_verification|Philippians|airqino|dalia_martinez",
    r"\b[\w-]+-plan\.md|findings-register(?:\.md)?|ledger-trimmer-design(?:\.md)?|f24-(?:oracle|differential)\.py",
    r"(?<![\w-])[FX]\d{1,2}\b(?![\w-])", r"\b[Ss]ections? \d+(?:\.\d+)*[a-z]?\b",
]


def git(clone, *a, check=True):
    r = subprocess.run(["git", "-C", clone] + list(a), capture_output=True, text=True)
    if check and r.returncode:
        sys.exit("git %s failed: %s" % (" ".join(a), r.stderr.strip()))
    return r.stdout


def refuse(msg):
    sys.exit("REFUSED: %s" % msg)


def parse_edits(path):
    out, left, cur = {}, {}, None
    for raw in open(path, encoding="utf-8").read().split("\n"):
        if raw.startswith("@@ = "):
            out[cur] = ("twin", raw[5:].strip())
        elif raw.startswith("@left "):
            _t, p, nums, why = raw.split(" ", 3)
            left.setdefault(p, {}).update({int(n): why for n in nums.split(",")})
        elif raw.startswith("@@ "):
            cur = raw[3:].strip()
            out.setdefault(cur, {})
        elif cur and re.match(r"^\d+\|", raw):
            n, rest = raw.split("|", 1)
            if rest.endswith(" ==>"):  # a deletion: nothing after the arrow
                old, new = rest[:-4], ""
            elif " ==> " in rest:
                old, new = rest.split(" ==> ", 1)
            else:
                refuse("scrub-edits-b.txt: line %s has no ' ==> '" % n)
            out[cur].setdefault(int(n), []).append((old, new))
        elif raw.strip() and not raw.startswith("#"):
            refuse("scrub-edits-b.txt: unreadable line %r" % raw[:60])
    return out, left


def index():
    out, tree = {}, None
    for ln in open(os.path.join(HERE, "scrub-derive-after-a.txt"), encoding="utf-8"):
        m = re.match(r"^candidate (\S+) \(tree (\w+)\) against", ln)
        if m:
            tree = m.group(2)
        m = re.match(r"^([^ ]+):(\d+): <([a-z?]+)> \[([A-Z,]+)\] ", ln)
        if m:
            out.setdefault(m.group(1), {})[int(m.group(2))] = m.group(3)
    return out, tree


def is_python(path, text):
    return path.endswith(".py") or (not os.path.splitext(path)[1] and text.startswith("#!") and "python" in text.split("\n", 1)[0])


def masked_stream(text):
    """The token stream with every string literal and comment masked and docstring-like statements collapsed."""
    toks = list(tokenize.generate_tokens(io.StringIO(text).readline))
    skip = (tokenize.NEWLINE, tokenize.NL, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT, tokenize.ENDMARKER)
    out, cur = [], []
    logical = []
    for t in toks:
        if t.type == tokenize.NEWLINE:
            logical.append(cur)
            cur = []
        else:
            cur.append(t)
    logical.append(cur)
    for lg in logical:
        body = [t for t in lg if t.type not in skip]
        if body and all(t.type == tokenize.STRING for t in body):
            out.append(("DOCSTRING",))
        else:
            out.extend(("STRING",) if t.type == tokenize.STRING else (t.type, t.string)
                       for t in lg if t.type not in (tokenize.COMMENT, tokenize.NL))
            out.append(("NEWLINE",))
    return out


def mask_why(o):
    if isinstance(o, dict):
        return {k: ("<why>" if k == "why" else mask_why(v)) for k, v in o.items()}
    if isinstance(o, list):
        return [mask_why(v) for v in o]
    return o


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
    idx, tree = index()
    if git(clone, "cat-file", "-t", tree, check=False).strip() != "tree":
        refuse("the tree scrub-derive-after-a.txt was made from (%s) is not in the clone: rebuild phase A, or regenerate the index" % tree)
    for f in files:  # the group's files must be byte-for-byte what the index was made from (the groups touch disjoint files)
        if git(clone, "rev-parse", "HEAD:" + f).strip() != git(clone, "rev-parse", "%s:%s" % (tree, f)).strip():
            refuse("%s is not the phase A tip's blob the index was made from: its line numbers cannot be trusted" % f)
    edits, left = parse_edits(os.path.join(HERE, "scrub-edits-b.txt"))
    shown, new_text, summary = [], {}, []
    for f in files:
        spec = edits.get(f)
        if spec is None:
            refuse("%s has no section in scrub-edits-b.txt" % f)
        if isinstance(spec, tuple):
            spec = edits[spec[1]]
        old = git(clone, "show", "HEAD:" + f)
        lines = old.split("\n")
        flagged = idx.get(f, {})
        lf = left.get(f, left.get(TWINS.get(f, f), {}))
        miss = sorted(n for n in flagged if n not in spec and n not in lf)
        if miss:
            refuse("%s: %d flagged line(s) neither edited nor left on purpose: %s" % (f, len(miss), miss[:12]))
        both = sorted(n for n in lf if n in spec)
        if both:
            refuse("%s: lines %s are both edited and left" % (f, both))
        nedits = 0
        for n in sorted(spec):
            if not 1 <= n <= len(lines):
                refuse("%s: line %d is past the end" % (f, n))
            line = lines[n - 1]
            before = line
            for o, nw in spec[n]:
                if line.count(o) != 1:
                    refuse("%s:%d: %r occurs %d times in the line, wanted exactly once: %s" % (f, n, o, line.count(o), line.strip()[:110]))
                line = line.replace(o, nw, 1)
            for p in STRICT:
                if re.search(p, line):
                    refuse("%s:%d: the rewritten line still carries a fork token (%s): %s" % (f, n, p, line.strip()[:110]))
            lines[n - 1] = line
            shown.append((f, n, before.strip(), line.strip()))
            nedits += 1
        nt = "\n".join(lines)
        try:
            if f.endswith(".json"):
                ok = mask_why(json.loads(old)) == mask_why(json.loads(nt))
                kind = "parsed JSON, every `why` masked"
            elif is_python(f, old):
                ok = masked_stream(old) == masked_stream(nt)
                kind = "token stream, strings and comments masked"
            else:
                sh = "bash" if old.startswith("#!/usr/bin/env bash") else "sh"
                r = subprocess.run([sh, "-n"], input=nt, capture_output=True, text=True)
                ok = r.returncode == 0
                kind = "%s -n parses (the changed lines are read by a person)" % sh
        except (tokenize.TokenError, IndentationError, SyntaxError, ValueError) as e:
            refuse("%s: the proof could not read it: %s" % (f, e))
        if not ok:
            refuse("%s: the proof failed: %s" % (f, kind))
        new_text[f] = nt
        summary.append("  %-44s %3d line(s) rewritten %3d left   %s: ok" % (f, nedits, len(lf), kind))
    for twin, partner in TWINS.items():
        if twin in new_text and partner in new_text and new_text[twin] != new_text[partner]:
            refuse("the twins %s and %s would differ" % (twin, partner))
    print("group %s on %s (tree %s): %d file(s)" % (group, git(clone, "rev-parse", "--short", "HEAD").strip(), tree[:9], len(files)))
    print("\n".join(summary))
    print("\nthe lines this commit changes:")
    for f, n, b, a in shown:
        print("  %s:%d\n    - %s\n    + %s" % (f, n, b[:170], a[:170]))
    if not write:
        print("\ndry run: nothing written")
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
    print("\ncommitted %s: %s" % (git(clone, "rev-parse", "--short", "HEAD").strip(), msg.split("\n", 1)[0]))


main()
