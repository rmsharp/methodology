#!/usr/bin/env python3
"""Cumulative proof over the whole scrub range, written apart from the builders so it does not share their bugs (S324).

    python3 -I docs/planning/pr-composition-evidence/scrub-proof.py REPO FROM TO

For every file that differs between FROM and TO in REPO: a Python file's token stream with every string literal and comment
masked is equal (so over both phases no code token changed anywhere, only text inside literals and comments); a shell file
still parses; a JSON file is equal with every `why` masked. Also: the set of files is the same in both (no file added,
removed or renamed), the two dashboard copies are byte-identical in TO, and the executable bits are unchanged. Exit 0 only if
all of it holds. READ-ONLY.
"""
import ast
import io
import json
import subprocess
import sys
import tokenize

sys.dont_write_bytecode = True
repo, a, b = sys.argv[1:4]


def git(*args, check=True):
    r = subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit("git %s: %s" % (" ".join(args), r.stderr.strip()))
    return r.stdout


def stream(text):
    toks = list(tokenize.generate_tokens(io.StringIO(text).readline))
    return [("S",) if t.type == tokenize.STRING else (t.type, t.string)
            for t in toks if t.type not in (tokenize.COMMENT, tokenize.NL)]


def mask(o):
    if isinstance(o, dict):
        return {k: "<why>" if k == "why" else mask(v) for k, v in o.items()}
    if isinstance(o, list):
        return [mask(v) for v in o]
    return o


tree_a = set(git("ls-tree", "-r", "--name-only", a).split())
tree_b = set(git("ls-tree", "-r", "--name-only", b).split())
ok = tree_a == tree_b
print("files in both trees: %d; the sets are %s" % (len(tree_a), "equal" if ok else "DIFFERENT: %s" % sorted(tree_a ^ tree_b)))
modes_a = dict((l.split("\t")[1], l.split()[0]) for l in git("ls-tree", "-r", a).splitlines())
modes_b = dict((l.split("\t")[1], l.split()[0]) for l in git("ls-tree", "-r", b).splitlines())
badmode = sorted(f for f in modes_a if modes_a[f] != modes_b.get(f))
print("executable bits / modes unchanged: %s" % ("yes" if not badmode else "NO: %s" % badmode))
ok = ok and not badmode
changed = git("diff", "--name-only", a, b).split()
print("%d file(s) differ" % len(changed))
for f in changed:
    old, new = git("show", "%s:%s" % (a, f)), git("show", "%s:%s" % (b, f))
    if f.endswith(".json"):
        good, kind = mask(json.loads(old)) == mask(json.loads(new)), "JSON, `why` masked"
    elif f.endswith(".py") or (old.startswith("#!") and "python" in old.split("\n", 1)[0]):
        good, kind = stream(old) == stream(new), "Python tokens, strings and comments masked"
    else:
        sh = "bash" if old.startswith("#!/usr/bin/env bash") else "sh"
        good = subprocess.run([sh, "-n"], input=new, capture_output=True, text=True).returncode == 0
        kind = "%s -n parses" % sh
    ok = ok and good
    print("  %-46s %-44s %s" % (f, kind, "ok" if good else "FAILED"))
da, db = git("show", "%s:starter-kit/methodology_dashboard.py" % b), git("show", "%s:tools/methodology_dashboard.py" % b)
print("the two dashboard copies byte-identical in %s: %s" % (b[:7], "yes" if da == db else "NO"))
ok = ok and da == db
numstat = git("diff", "--numstat", a, b).splitlines()
add = sum(int(l.split("\t")[0]) for l in numstat)
dele = sum(int(l.split("\t")[1]) for l in numstat)
print("diff against FROM: +%d / -%d over %d files (git diff --numstat)" % (add, dele, len(numstat)))
print("CUMULATIVE PROOF:", "HOLDS" if ok else "FAILS")
sys.exit(0 if ok else 1)
