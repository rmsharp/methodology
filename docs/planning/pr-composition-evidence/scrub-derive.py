#!/usr/bin/env python3
"""The scrub's inventory: what the candidate adds that only this fork can read (S324). READ-ONLY.

Run from anywhere inside the repository:  python3 -I docs/planning/pr-composition-evidence/scrub-derive.py [CANDIDATE] [BASE]

CANDIDATE defaults to refs/pr2/candidate-before-scrub (the candidate's tip, 5afc962, before the scrub; pass refs/scrub/final or a
sha to measure what is left), BASE to upstream/main. For every file the candidate changes against BASE,
reads the ADDED lines (git diff -U0, with their line numbers in the candidate's blob) and sorts each line into the STRICT
classes below, which name something a reader of the upstream repository cannot open or follow, and the SOFT words, which
are ambiguous (a "fork" can be a git fork; an "operator" can be a shell operator) and are listed, never counted as a defect.
It also lists every path the added lines cite that the CANDIDATE's own tree does not hold (a dangling path), which is the
second half of the plan's "tokens and dangling paths". A plain regular-expression sort: eyeball a sample before quoting a
figure, and quote the plain `git diff --numstat` figure for sizes.

Writes nothing, and generates no bytecode.
"""
import collections
import io
import os
import re
import subprocess
import sys
import tokenize

sys.dont_write_bytecode = True

CAND = sys.argv[1] if len(sys.argv) > 1 else "refs/pr2/candidate-before-scrub"
BASE = sys.argv[2] if len(sys.argv) > 2 else "upstream/main"


def sh(*a, check=True):
    r = subprocess.run(a, capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit("git failed: %s\n%s" % (" ".join(a), r.stderr.strip()))
    return r.stdout if r.returncode == 0 else ""


os.chdir(sh("git", "rev-parse", "--show-toplevel").strip())

STRICT = collections.OrderedDict([
    ("BL", r"\bBL-\d+"),
    ("S", r"\bS\d{2,3}\b"),
    ("LEARN", r"[Ff]ork [Ll]earning|(?<![Ff]ork )[Ll]earning #(?:1[4-9]|[2-9]\d|\d{3})\b"),
    ("PLANDOC", r"docs/(?:planning|audits)/(?!BACKLOG\.md\b)"),
    ("PHASE", r"\bP\d{1,2}\b(?= |\)|,|:|\.|\]|$)"),
    ("PLANREF", r"\b[Pp]lan (?:[0-9§]|[CD]\d|section)|\bplan's\b|§ ?\d|\bD[1-9]\b(?= |\)|,|:|\.)|\bC\d\b(?= |\)|,|:|\.)"),
    ("PRPLAN", r"\bPR[1-9]\b(?!#)"),
    ("ADOPTER", r"nprcgenekeepr|vscode_quarto_ext|mts-system|wsfct|feedback-loop-comparison|model_project_constructor|claude_work|church_growth|chat_verification|Philippians|airqino|dalia_martinez"),
    ("PLANFILE", r"\b[\w-]+-plan\.md|findings-register(?:\.md)?|ledger-trimmer-design(?:\.md)?|f24-(?:oracle|differential)\.py"),
    ("FINDING", r"(?<![\w-])[FX]\d{1,2}\b(?![\w-])"),
    ("SECTION", r"\b[Ss]ections? \d+(?:\.\d+)*[a-z]?\b|\b[Ss]ections? \d+ and \d+\b"),
])
SOFT = collections.OrderedDict([
    ("fork", r"\bfork(?:s|ed)?\b"),
    ("operator", r"\boperator\b"),
    ("his", r"\b(?:he|his|him)\b"),
    ("upstream-ref", r"\b(?:PR|[Ii]ssue|issues) #\d+|\bupstream (?:PR|issue)\b"),
])

files = sh("git", "diff", "--name-only", BASE, CAND).split()
tree = set(sh("git", "ls-tree", "-r", "--name-only", CAND).split())


COMMENT_COL = {}


def blob(path):
    return sh("git", "show", "%s:%s" % (CAND, path), check=False)


def is_python(path, text):
    return path.endswith(".py") or (not os.path.splitext(path)[1] and text.startswith("#!") and "python" in text.split("\n", 1)[0])


def lexical_classes(path, text):
    """line number -> 'comment' | 'docstring' | 'string' | 'code' for a Python blob, by tokenize; else by a leading '#'."""
    out = {}
    lines = text.split("\n")
    COMMENT_COL.clear()
    if is_python(path, text):
        try:
            toks = list(tokenize.generate_tokens(io.StringIO(text).readline))
        except (tokenize.TokenError, IndentationError, SyntaxError):
            toks = None
        if toks is not None:
            # logical lines made of strings (and layout tokens) only are docstring-like statements
            skip = (tokenize.NEWLINE, tokenize.NL, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT, tokenize.ENDMARKER)
            logical, cur = [], []
            for t in toks:
                if t.type == tokenize.NEWLINE:
                    logical.append(cur)
                    cur = []
                else:
                    cur.append(t)
            logical.append(cur)
            docstring_toks = set()
            for lg in logical:
                body = [t for t in lg if t.type not in skip]
                if body and all(t.type == tokenize.STRING for t in body):
                    docstring_toks.update(id(t) for t in body)
            for t in toks:
                for i, lineno in enumerate(range(t.start[0], t.end[0] + 1)):
                    if t.type == tokenize.COMMENT:
                        COMMENT_COL[lineno] = t.start[1]
                        out[lineno] = "comment" if out.get(lineno) in (None, "comment") else out[lineno]
                    elif t.type == tokenize.STRING:
                        c = "docstring" if id(t) in docstring_toks else "string"
                        if out.get(lineno) in (None, "comment", "docstring"):
                            out[lineno] = c
                    elif t.type not in skip and out.get(lineno) in (None, "comment"):
                        out[lineno] = "code"
            for n in range(1, len(lines) + 1):
                out.setdefault(n, "blank")
            return out
    for n, ln in enumerate(lines, 1):
        st = ln.strip()
        out[n] = "comment" if st.startswith("#") else ("prose" if path.endswith(".md") else "code")
    return out


rows = []  # (file, lineno, text, strict classes, soft classes)
for f in files:
    new = 0
    lex = lexical_classes(f, blob(f))
    CC = dict(COMMENT_COL)
    hunk = sh("git", "diff", "-U0", BASE, CAND, "--", f).splitlines()
    # tokens the line's own hunk REMOVES are upstream's, inherited, not the fork's: a modified line keeps them
    minus_of, cur_minus, i = {}, [], 0
    for j, ln in enumerate(hunk):
        if ln.startswith("@@"):
            k = j + 1
            cur_minus = []
            while k < len(hunk) and not hunk[k].startswith("@@"):
                if hunk[k].startswith("-") and not hunk[k].startswith("---"):
                    cur_minus.append(hunk[k][1:])
                k += 1
            minus_of[j] = "\n".join(cur_minus)
    cur = ""
    for j, ln in enumerate(hunk):
        if ln.startswith("@@"):
            cur = minus_of[j]
        m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", ln)
        if m:
            new = int(m.group(1))
            continue
        if ln.startswith("+++") or not ln.startswith("+"):
            continue
        text = ln[1:]

        def fresh(p, text=text, cur=cur):
            return any(mm.group(0) not in cur for mm in re.finditer(p, text))

        s = [k for k, p in STRICT.items() if fresh(p)]
        w = [k for k, p in SOFT.items() if re.search(p, text)]
        cls = lex.get(new, "?")
        if s and cls in ("code", "string") and new in COMMENT_COL:
            cc = COMMENT_COL[new]
            if all(m.start() >= cc for p in STRICT.values() for m in re.finditer(p, text) if m.group(0) not in cur):
                cls = "tcomment"
        if s or w:
            rows.append((f, new, text, s, w, cls))
        new += 1

print("candidate %s (tree %s) against %s: %d changed files" % (sh("git", "rev-parse", CAND).strip()[:7], sh("git", "rev-parse", CAND + "^{tree}").strip(), sh("git", "rev-parse", BASE).strip()[:7], len(files)))
tot = collections.Counter()
per = collections.defaultdict(collections.Counter)
strict_lines = collections.defaultdict(set)
soft_only = collections.defaultdict(set)
for f, n, t, s, w, lx in rows:
    for k in s:
        tot[k] += 1
        per[f][k] += 1
    if s:
        strict_lines[f].add(n)
    elif w:
        soft_only[f].add(n)
print("\nSTRICT classes, added lines carrying one (a line with two counts once per class):")
for k in STRICT:
    print("  %-8s %4d" % (k, tot[k]))
print("  lines with at least one strict token: %d in %d files" % (sum(len(v) for v in strict_lines.values()), len(strict_lines)))
print("  lines with only a soft word (not counted):  %d in %d files" % (sum(len(v) for v in soft_only.values()), len(soft_only)))
print("\nper file (strict lines / soft-only lines / classes):")
for f in sorted(set(strict_lines) | set(soft_only), key=lambda x: (-len(strict_lines.get(x, ())), x)):
    print("  %-48s %4d %4d   %s" % (f, len(strict_lines.get(f, ())), len(soft_only.get(f, ())),
                                     " ".join("%s=%d" % (k, v) for k, v in per[f].items())))

lexc = collections.Counter(lx for f, n, t, s, w, lx in rows if s)
print("\nSTRICT lines by where the token sits (comment, tcomment (a trailing comment) and docstring are inert; string and code are behaviour-bearing):")
for k in ("comment", "tcomment", "docstring", "prose", "string", "code", "blank", "?"):
    if lexc[k]:
        print("  %-10s %4d" % (k, lexc[k]))
perlex = collections.defaultdict(collections.Counter)
for f, n, t, s, w, lx in rows:
    if s:
        perlex[f][lx] += 1
print("\nper file, behaviour-bearing strict lines (string + code):")
for f, c in sorted(perlex.items(), key=lambda kv: (-(kv[1]["string"] + kv[1]["code"]), kv[0])):
    if c["string"] + c["code"]:
        print("  %-48s string=%d code=%d (of %d)" % (f, c["string"], c["code"], sum(c.values())))

# dangling paths: every path-shaped token on an added line that the candidate's tree does not hold
PATHRE = re.compile(r"(?<![\w/.-])((?:docs|bin|tools|starter-kit|workstreams|\.githooks)/[A-Za-z0-9_./\-]*[A-Za-z0-9_])")
cites = collections.defaultdict(set)
for f in files:
    for ln in sh("git", "diff", "-U0", BASE, CAND, "--", f).splitlines():
        if ln.startswith("+") and not ln.startswith("+++"):
            for p in PATHRE.findall(ln[1:]):
                cites[p.rstrip(".")].add(f)
dangling = sorted(p for p in cites if p not in tree and not any(t.startswith(p + "/") for t in tree))
print("\n%d distinct repository paths cited on added lines; %d are not in the candidate's tree:" % (len(cites), len(dangling)))
for p in dangling:
    print("  %-70s <- %s" % (p, ", ".join(sorted(cites[p]))[:90]))

BARE = re.compile(r"(?<![\w/.-])([A-Za-z0-9_][\w.-]*\.(?:py|sh|md|txt|json|jsonl|verify\.sh))\b")
basenames = {t.rsplit("/", 1)[-1] for t in tree}
bare = collections.defaultdict(set)
for f in files:
    for ln in sh("git", "diff", "-U0", BASE, CAND, "--", f).splitlines():
        if ln.startswith("+") and not ln.startswith("+++"):
            for b in BARE.findall(ln[1:]):
                if b not in basenames:
                    bare[b].add(f)
print("\n%d bare file names on added lines are not the basename of any file in the candidate's tree (fixture names are expected; read for evidence-script names):" % len(bare))
for b in sorted(bare):
    print("  %-46s <- %s" % (b, ", ".join(sorted(bare[b]))[:80]))

print("\n=== STRICT lines in full (file:line: text) ===")
for f, n, t, s, w, lx in rows:
    if s:
        print("%s:%d: <%s> [%s] %s" % (f, n, lx, ",".join(s), t.strip()[:300]))
print("\n=== SOFT-ONLY lines in full ===")
for f, n, t, s, w, lx in rows:
    if not s and w:
        print("%s:%d: [%s] %s" % (f, n, ",".join(w), t.strip()[:300]))
