#!/usr/bin/env python3
"""BL-101 F24 (S299): `bin/migrate-layout`'s reading of a `.vscodeignore` against the real thing, in three parts. Writes nothing
into the repository; exit 0 when no row differs.

  A. the glob matcher (`vsce_glob`) against minimatch: a generated corpus of patterns x paths, every pair compared with
     `minimatch(path, pattern, { dot: true })`, the call vsce 3.9.2 makes. Patterns the tool does not read (None) are counted,
     by shape, never compared.
  B. the whole list handling (`vsce_ignore_list`: comments, trimming, line breaks, the `/**` vsce adds to a directory name,
     negations, vsce's default list) against `vsce ls --no-dependencies` run on a project tree, for random `.vscodeignore`
     files: the files vsce lists are the files the tool says are packaged.
  C. vsce's default list and the two negations it appends, the tool's copy against the list in vsce's own source.

Usage: f24-differential.py <directory with node_modules/minimatch and node_modules/.bin/vsce> [seed] [parts]
(the adopter's checkout was used: minimatch 10.2.5, @vscode/vsce 3.9.2; the third argument is any of `A`, `B`, `C`: the default is `ABC`). Needs node."""
import importlib.util
import itertools
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ORACLE = sys.argv[1]
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 24
PARTS = sys.argv[3] if len(sys.argv) > 3 else "ABC"


def load(path):
    import importlib.machinery
    loader = importlib.machinery.SourceFileLoader("migrate_layout", path)
    spec = importlib.util.spec_from_loader("migrate_layout", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


m = load(os.path.join(REPO, "bin", "migrate-layout"))
rng = random.Random(SEED)
failures = 0

# ---------------------------------------------------------------------------------------------------- part A
NAMES = ["a", "b", "ab", "abc", "a.b", "docs", "methodology", "archive", "SESSION_RUNNER.md", "CHANGELOG.md", "x.map",
         ".git", ".hidden", "HOW_TO_USE.md", "src", "out"]
FORMS = ["{n}", "*", "?", "{n}*", "*{n}", "*.md", "*.map", "[ab]", "[!a]", "[^a]", "[a-c]*", "**", "a**", "**a", "{{a,b}}",
         "{{a,docs}}", "a?c", ".*", "*a*", "{{x,y/z}}", "x{{,y}}", "{{a,{{b,c}}}}", "[a-]", "[-a]", "[ab-]c", "a[.]b"]
UNREAD_FORMS = ["+(a|b)", "@(a|b)", "!(a)", "?(a)b", "*(a)", "x{{1..3}}", "x{{a..c}}", "a\\*b", "[[:upper:]]*", "{{a}}", "x{{", "x}}",
                "a//b", "[a", "[]", "[]a]"]
PATH_SEGS = ["a", "b", "ab", "abc", "a.b", "docs", "methodology", "archive", "SESSION_RUNNER.md", "CHANGELOG.md", "x.map",
             ".git", ".hidden", "HOW_TO_USE.md", "src", "out", "c", "a.map", ".md", "x.md", "ac", "a b"]


def segment():
    form = rng.choice(FORMS)
    return form.replace("{n}", rng.choice(NAMES)).replace("{{", "{").replace("}}", "}")


def make_patterns(n):
    out = set(NAMES) | set(f.replace("{n}", "a").replace("{{", "{").replace("}}", "}") for f in FORMS)
    for f in UNREAD_FORMS:
        out.add(f.replace("{{", "{").replace("}}", "}"))
    for a, b in itertools.product(FORMS[:14], FORMS[:14]):
        out.add(a.replace("{n}", "docs").replace("{{", "{").replace("}}", "}") + "/" + b.replace("{n}", "a").replace("{{", "{").replace("}}", "}"))
    while len(out) < n:
        segs = [segment() for _ in range(rng.randint(1, 3))]
        pattern = "/".join(segs)
        pre = rng.choice(["", "", "", "./", "/", "**/"])
        post = rng.choice(["", "", "", "/", "/**", "/**/"])
        out.add(pre + pattern + post)
    return sorted(out)


def make_paths(n):
    out = set(PATH_SEGS)
    tool = importlib_manifest_names()
    out |= tool
    while len(out) < n:
        out.add("/".join(rng.choice(PATH_SEGS) for _ in range(rng.randint(1, 4))))
    return sorted(out)


def importlib_manifest_names():
    names = set()
    for src, dest in m.NEW_LAYOUT.items():
        names.add(os.path.basename(src))
        names.add(dest)
        names.add(dest.rsplit("/", 1)[-1])
    return names | {".gitattributes", "docs/methodology/HOW_TO_USE.md", "docs/archive/CHANGELOG-through-2026-08-01.md",
                    "methodology/archive/CHANGELOG-through-2026-08-01.md"}


NODE_MATRIX = """
const {minimatch} = require(process.argv[1] + '/node_modules/minimatch');
const {patterns, paths} = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const out = patterns.map(p => paths.map(f => minimatch(f, p, {dot: true}) ? '1' : '0').join(''));
console.log(JSON.stringify(out));
"""


def witnesses(pattern):
    """Paths built from the pattern itself (its wildcards filled in, a segment added or dropped), so that the matcher is also
    tried where minimatch says yes: a random path matches a random pattern about once in two hundred pairs."""
    alts = m.expand_braces(pattern)
    out = set()
    for alt in (alts or [])[:3]:
        for _ in range(3):
            segs = []
            for seg in alt.split("/"):
                if seg == "**":
                    segs += [rng.choice(PATH_SEGS) for _ in range(rng.randint(0, 2))]
                    continue
                piece, i = "", 0
                while i < len(seg):
                    c = seg[i]
                    if c == "*":
                        piece += rng.choice(["", "a", "xyz", ".x", "ab"])
                    elif c == "?":
                        piece += rng.choice(["a", ".", "b"])
                    elif c == "[":
                        end = seg.find("]", i + 2)
                        body = seg[i + 1:end] if end > 0 else "a"
                        piece += "z" if body[:1] in "!^" else body[:1]
                        i = end if end > 0 else i
                    else:
                        piece += c
                    i += 1
                segs.append(piece)
            path = "/".join(segs)
            out.add(path)
            out.add(path + "/x")
            out.add("q/" + path)
            if "/" in path:
                out.add(path.rsplit("/", 1)[0])
    # a file vsce lists never has an empty, `.` or `..` segment, and minimatch treats those specially: not paths, not compared
    return sorted(x for x in out if x and not any(seg in ("", ".", "..") for seg in x.split("/")))


NODE_PAIRS = """
const {minimatch} = require(process.argv[1] + '/node_modules/minimatch');
const pairs = JSON.parse(require('fs').readFileSync(0, 'utf8'));
console.log(JSON.stringify(pairs.map(([p, f]) => minimatch(f, p, {dot: true}))));
"""


def part_a():
    global failures
    real = [l.strip() for l in subprocess.run(
        ["git", "-C", ORACLE, "show", "507b9348:.vscodeignore"], capture_output=True, text=True).stdout.splitlines()]
    real = [l for l in real if l and not l.startswith("#")]
    patterns = sorted(set(make_patterns(6000)) | set(real) | {l + "/**" for l in real} | set(m.VSCE_DEFAULT_IGNORE))
    paths = make_paths(260)
    r = subprocess.run(["node", "-e", NODE_MATRIX, ORACLE], input=json.dumps({"patterns": patterns, "paths": paths}), capture_output=True, text=True)
    if r.returncode:
        sys.exit("node failed: " + r.stderr[-400:])
    matrix = json.loads(r.stdout)
    version = json.load(open(ORACLE + "/node_modules/minimatch/package.json"))["version"]
    read = unread = pairs = pairs_true = 0
    bad = []
    unread_shapes = []
    for pattern, row in zip(patterns, matrix):
        g = m.vsce_glob(pattern)
        if g is None:
            unread += 1
            unread_shapes.append(pattern)
            continue
        read += 1
        for path, want in zip(paths, row):
            pairs += 1
            pairs_true += want == "1"
            if g(path) is not (want == "1"):
                bad.append((pattern, path, want == "1"))
    pairs_w = [(pattern, path) for pattern in patterns if m.vsce_glob(pattern) is not None for path in witnesses(pattern)]
    r = subprocess.run(["node", "-e", NODE_PAIRS, ORACLE], input=json.dumps(pairs_w), capture_output=True, text=True)
    if r.returncode:
        sys.exit("node failed: " + r.stderr[-400:])
    answers = json.loads(r.stdout)
    witness_true = sum(answers)
    for (pattern, path), want in zip(pairs_w, answers):
        if m.vsce_glob(pattern)(path) is not want:
            bad.append((pattern, path, want))
    print("A. glob matcher against minimatch %s, { dot: true }, seed %d" % (version, SEED))
    print("   targeted paths: %d more pairs, %d of them matches" % (len(pairs_w), witness_true))
    print("   %d patterns (%d read, %d not read), %d paths; %d pairs compared, %d of them matches; %d differ" %
          (len(patterns), read, unread, len(paths), pairs, pairs_true, len(bad)))
    # a pattern the tool does not read must be one of the shapes it names: nothing else may fall out of the matcher
    stray = [p for p in unread_shapes if not any(k in p for k in ("(", ")", "..", "\\", "[:", "//", "[]", "{", "}")) and not (p.count("[") != p.count("]"))]
    print("   not read: %d; of them outside the named shapes (extended glob, range, backslash, POSIX class, lone brace, `//`, bad class): %d" %
          (unread, len(stray)))
    for pattern, path, want in bad[:40]:
        print("   DIFFERS  %r against %r: minimatch %s, tool %s" % (pattern, path, want, not want))
    for p in stray[:40]:
        print("   STRAY unread  %r" % p)
    failures += len(bad) + len(stray)


# ---------------------------------------------------------------------------------------------------- part B
TREE = ["package.json", "extension.js", "README.md", "LICENSE", "SESSION_RUNNER.md", "CHANGELOG.md", "HANDOFFS.md", ".gitattributes",
        ".quality-gates.json", ".context-budget.json", "dashboard.html", "methodology_trim.py", "CONTRIBUTING.md", ".eslintrc.json",
        "docs/methodology/HOW_TO_USE.md", "docs/archive/CHANGELOG-through-2026-08-01.md", "docs/readme.md", "src/a.ts",
        "src/deep/b.ts", "out/x.js", "x.map", "a/b/c.map", "test/t.ts", ".github/workflows/ci.yml", "sub/.eslintrc.json",
        "sub/CHANGELOG.md", ".hidden/x", "methodology/SESSION_RUNNER.md", "methodology/CHANGELOG.md", "methodology/HANDOFFS.md",
        "methodology/.gitattributes", "methodology/.quality-gates.json", "methodology/.context-budget.json", "methodology/dashboard.html",
        "methodology/methodology_trim.py", "methodology/HOW_TO_USE.md", "methodology/archive/CHANGELOG-through-2026-08-01.md",
        "methodology/workstreams/A.md", "methodology/README.md", "methodology/sub/x.ts", "tools/a.py"]  # no DOCS/: APFS folds its case into docs/
LINES = ["SESSION_RUNNER.md", "CHANGELOG.md", "HANDOFFS.md", "*.md", "**/*.md", "docs", "docs/", "docs/**", "docs/*", "docs/**/*.md",
         "methodology", "methodology/", "methodology/**", "methodology/*", "**/*.py", "*.py", "src/**", "**/*.map", "x.map", "*.json",
         ".*", ".quality-gates.json", ".context-budget.json", "dashboard.html", "{SESSION_RUNNER,CHANGELOG}.md", "[CH]*.md", "?.map",
         "!README.md", "!docs/methodology/HOW_TO_USE.md", "!methodology/HOW_TO_USE.md", "!methodology", "!methodology/**", "!*.md",
         "!CHANGELOG.md", "!docs", "/SESSION_RUNNER.md", "./CHANGELOG.md", "tools", "tools/**", "out/**", "test/**", "a/**/c.map",
         "**", "!**/*.json", "# SESSION_RUNNER.md", "   ", "", "  docs/**  ", "\tCHANGELOG.md", "sub", "sub/**", "**/CHANGELOG.md",
         "*.todo", ".github", "DOCS", "docs/archive", "dashboard*", "*.ts", "!src/a.ts", "!sub/CHANGELOG.md", "methodology_trim.py"]
BREAKS = ["\n", "\n", "\n", "\r\n", "\r"]


def part_b():
    global failures
    n = int(os.environ.get("F24_RUNS", "150"))
    vsce = os.path.join(ORACLE, "node_modules", ".bin", "vsce")
    root = tempfile.mkdtemp(prefix="f24-tree-")
    try:
        for rel in TREE:
            path = os.path.join(root, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write("x\n")
        with open(os.path.join(root, "package.json"), "w") as f:
            json.dump({"name": "toy", "displayName": "toy", "version": "0.0.1", "publisher": "t", "engines": {"vscode": "^1.80.0"}}, f)
        bad, seen, started, unread_total = [], 0, time.time(), 0
        for k in range(n):
            lines = [rng.choice(LINES) for _ in range(rng.randint(1, 9))]
            brk = rng.choice(BREAKS)
            text = ("﻿" if rng.random() < 0.05 else "") + brk.join(lines) + rng.choice(["", brk])
            with open(os.path.join(root, ".vscodeignore"), "w", encoding="utf-8", newline="") as f:
                f.write(text)
            r = subprocess.run(["node", vsce, "ls", "--no-dependencies"], cwd=root, capture_output=True, text=True)
            if r.returncode:
                sys.exit("vsce ls failed: " + (r.stdout + r.stderr)[-400:])
            listed = {l.strip() for l in r.stdout.splitlines() if l.strip()}
            covering, unread = m.vsce_ignore_list(text)
            unread_total += unread
            mine = {p for p in TREE if not covering(p)}
            seen += 1
            if listed != mine:
                bad.append((text, sorted(listed - mine), sorted(mine - listed)))
        print("B. list handling against `vsce ls --no-dependencies` (@vscode/vsce %s), seed %d, %d random .vscodeignore files over a %d-file tree, %.0f s" %
              (json.load(open(ORACLE + "/node_modules/@vscode/vsce/package.json"))["version"], SEED, seen, len(TREE), time.time() - started))
        print("   %d differ (lines the tool does not read in these files: %d)" % (len(bad), unread_total))
        for text, only_vsce, only_tool in bad[:12]:
            print("   DIFFERS  text %r\n            vsce lists and the tool does not: %s\n            the tool says packaged and vsce does not: %s" %
                  (text, only_vsce, only_tool))
        failures += len(bad)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def part_c():
    """The tool's copy of vsce's default list and of its two appended negations, against vsce's own source."""
    global failures
    import re
    source = open(os.path.join(ORACLE, "node_modules", "@vscode", "vsce", "out", "package.js"), encoding="utf-8").read()
    block = re.search(r"const defaultIgnore = \[(.*?)\];", source, re.S).group(1)
    theirs = re.findall(r"'([^']*)'", block)
    notignored = re.search(r"const notIgnored = \[(.*?)\];", source, re.S).group(1)
    negations = [x.replace("${readmePath}", "README.md").lstrip("!") for x in re.findall(r"[`']([^`']*)[`']", notignored)]
    ours, ours_neg = list(m.VSCE_DEFAULT_IGNORE), list(m.VSCE_NOT_IGNORED)
    print("C. vsce's default list against the tool's copy (@vscode/vsce %s): %d entries in vsce, %d in the tool; %d appended negations in vsce, %d in the tool" %
          (json.load(open(ORACLE + "/node_modules/@vscode/vsce/package.json"))["version"], len(theirs), len(ours), len(negations), len(ours_neg)))
    same = theirs == ours and negations == ours_neg
    print("   identical, in order" if same else "   DIFFER: only in vsce %s, only in the tool %s, negations vsce %s tool %s" %
          ([x for x in theirs if x not in ours], [x for x in ours if x not in theirs], negations, ours_neg))
    failures += 0 if same else 1


if "A" in PARTS:
    part_a()
if "B" in PARTS:
    part_b()
if "C" in PARTS:
    part_c()
print("RESULT: %s" % ("no row differs" if not failures else "%d row(s) differ" % failures))
sys.exit(1 if failures else 0)
