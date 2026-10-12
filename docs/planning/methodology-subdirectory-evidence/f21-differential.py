#!/usr/bin/env python3
"""BL-101 F21 (S300): where `bin/migrate-layout` puts its ledger entry, against a real CommonMark parser, in two parts. Writes
nothing into the repository; exit 0 when no row differs.

  A. the real population: every distinct committed version of `CHANGELOG.md` / `methodology/CHANGELOG.md` in every git repository
     under ~/Development, and every committed version of the ledger seed. For each, `first_heading` (the new rule) against
     markdown-it: the first line that reads as a month heading or a dated entry heading and is not inside a fenced block, an
     indented code block or an HTML block. The OLD rule (the first such line anywhere) is run beside them, so the table
     says how many real ledgers the defect touched and how many the fix changed.
  B. random ledger-shaped texts (every one ends with a newline) built from lines of the kinds below, seeded. Every
     disagreement with markdown-it is classified; one in a text WITHOUT an out-of-scope construct (an indented fence, a fence
     inside a quote or a list, an HTML comment holding a heading) is a FAIL. The in-scope kinds: month and entry headings,
     prose, blanks, backtick fences of 3, 4 and 5, tilde fences of 3 and 4, closing lines of each length, a closing line with an
     info string. A text with no fence line at all must give the OLD rule's answer (the fix changes nothing there).

Usage: f21-differential.py <directory with node_modules/markdown-it> [seed] [count] [parts]
(the adopter checkout `vscode_quarto_ext` was used: markdown-it from its node_modules; the fourth argument is `A`, `B` or `AB`).
Needs node. The tool is read-only here: the texts are strings, no project is touched."""
import importlib.machinery
import importlib.util
import json
import os
import random
import re
import subprocess
import sys
import threading

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ORACLE = sys.argv[1]
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 21
COUNT = int(sys.argv[3]) if len(sys.argv) > 3 else 20000
PARTS = sys.argv[4] if len(sys.argv) > 4 else "AB"
DEV = os.path.expanduser("~/Development")


def load(path):
    loader = importlib.machinery.SourceFileLoader("migrate_layout", path)
    spec = importlib.util.spec_from_loader("migrate_layout", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


m = load(os.path.join(REPO, "bin", "migrate-layout"))
HEADING = re.compile(r"^(## \d{4}-\d{2})[ \t]*$|^### \d{4}-\d{2}-\d{2} · ")
OLD = re.compile(r"^(## \d{4}-\d{2})[ \t]*$|^### \d{4}-\d{2}-\d{2} · ", re.M)

NODE = r"""
const MarkdownIt = require(process.argv[1] + '/node_modules/markdown-it');
const md = new MarkdownIt();
let buf = '';
process.stdin.on('data', d => buf += d);
process.stdin.on('end', () => {
  const out = JSON.parse(buf).map(text => {
    const blocked = [];
    let unterminated = false;
    for (const t of md.parse(text, {})) {
      if (!t.map) continue;
      if (t.type === 'fence') {
        blocked.push([t.map[0], t.map[1], 'fence']);
        const lines = t.content === '' ? 0 : t.content.split('\n').length - 1;
        if (t.map[1] - t.map[0] - 1 === lines) unterminated = true;
      } else if (t.type === 'code_block') blocked.push([t.map[0], t.map[1], 'code_block']);
      else if (t.type === 'html_block') blocked.push([t.map[0], t.map[1], 'html_block']);
    }
    return {blocked, unterminated};
  });
  process.stdout.write(JSON.stringify(out));
});
"""


def oracle(texts):
    r = subprocess.run(["node", "-e", NODE, ORACLE], input=json.dumps(texts), capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("node failed: " + r.stderr[:500])
    return json.loads(r.stdout)


def first_outside(text, spans):
    for i, line in enumerate(text.split("\n")):
        if HEADING.match(line) and not any(a <= i < b for a, b, _k in spans):
            return i + 1
    return None


def tool(text):
    try:
        f = m.first_heading(text)
    except m.Unsafe:
        return "unsafe"
    return None if f is None else text.count("\n", 0, f[0]) + 1


def old_rule(text):
    o = OLD.search(text)
    return None if o is None else text.count("\n", 0, o.start()) + 1


def sh(args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, errors="replace").stdout


SHAPES = [("a tilde fence", re.compile(r"^~{3,}", re.M)), ("a fence of four or more backticks", re.compile(r"^`{4,}", re.M)),
          ("an indented fence (1 to 3 spaces)", re.compile(r"^ {1,3}(`{3,}|~{3,})", re.M)),
          ("a heading inside an HTML comment", re.compile(r"<!--(?:(?!-->).)*?^#{2,3} \d{4}-\d{2}", re.M | re.S)),
          ("a fence inside a quote or a list", re.compile(r"^(>|[-*+]) +(`{3,}|~{3,})", re.M))]


def blob_texts(repo, queries):
    """(query, object id, text) for each query that names an object, from ONE `git cat-file --batch` process per repository."""
    p = subprocess.Popen(["git", "cat-file", "--batch"], cwd=repo, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def feed():
        for q in queries:
            p.stdin.write((q + "\n").encode())
        p.stdin.close()
    t = threading.Thread(target=feed)
    t.start()
    for q in queries:
        head = p.stdout.readline().split()
        if len(head) < 3:
            continue                       # "<query> missing"
        data = p.stdout.read(int(head[2]))
        p.stdout.read(1)
        yield q, head[0].decode(), data.decode("utf-8", "replace")
    t.join()
    p.wait()


print("tool under test: %s (%s)" % (sh(["git", "rev-parse", "--short", "HEAD"], REPO).strip(), os.path.join(REPO, "bin", "migrate-layout")))
fails = 0

# ------------------------------------------------------------------------------------------------------ part A
if "A" in PARTS:
    rows, regions, seen, per_repo, n_seed, shapes = [], {}, set(), {}, 0, {}

    def take(label, oid, text):
        if oid in seen:
            return False
        seen.add(oid)
        got, old = tool(text), old_rule(text)
        region = "\n".join(text.split("\n")[:got + 3]) + "\n" if isinstance(got, int) else text
        regions.setdefault(region, len(regions))
        rows.append((label, got, old, region))
        for tag, rx in SHAPES:
            if rx.search(region):
                shapes[tag] = shapes.get(tag, 0) + 1
        return True

    # What the first heading rule reads is the text up to that heading, so the oracle gets that region (and 3 lines after, for
    # the parser's lookahead) once per distinct region; a text the tool reads no heading in goes whole.
    seed_shas = sh(["git", "log", "--all", "--format=%h", "--", "starter-kit/CHANGELOG.md"], REPO).split()
    for q, oid, text in blob_texts(REPO, [s_ + ":starter-kit/CHANGELOG.md" for s_ in seed_shas]):
        n_seed += take("seed@" + q.split(":")[0], oid, text)
    repos = sorted(os.path.join(DEV, d) for d in os.listdir(DEV) if os.path.isdir(os.path.join(DEV, d, ".git")))
    for repo in repos:
        name = os.path.basename(repo)
        shas = sh(["git", "log", "--all", "--format=%H", "--", "CHANGELOG.md", "methodology/CHANGELOG.md"], repo).split()
        n = 0
        for q, oid, text in blob_texts(repo, [s_ + ":" + path for s_ in shas for path in ("CHANGELOG.md", "methodology/CHANGELOG.md")]):
            n += take("%s@%s" % (name, q[:7]), oid, text)
        per_repo[name] = n
    order = sorted(regions, key=regions.get)
    res = dict(zip(order, oracle(order)))
    touched, changed, disagree, kinds = {}, {}, [], {}
    for label, got, old, region in rows:
        o = res[region]
        spans = o["blocked"]
        expect = first_outside(region, spans)
        repo = label.split("@")[0]
        if old != got:
            changed[repo] = changed.get(repo, 0) + 1
        if old is not None and any(a <= old - 1 < b for a, b, _k in spans):
            touched[repo] = touched.get(repo, 0) + 1
        if got == "unsafe":
            if not o["unterminated"] or expect is not None:
                disagree.append((label, "unsafe", expect))
        elif got != expect:
            disagree.append((label, got, expect))
            for a, b, k in spans:
                if got is not None and a <= got - 1 < b:
                    kinds[k] = kinds.get(k, 0) + 1
    print("== A. every distinct committed version of the ledger: %d versions in %d repositories (+ %d versions of the seed), %d distinct header regions" % (
        len(rows) - n_seed, len(repos), n_seed, len(order)))
    for name in sorted(per_repo):
        print("   %-28s versions %5d   old rule inside a block: %4d   new rule moves it: %4d" % (name, per_repo[name], touched.get(name, 0), changed.get(name, 0)))
    print("   seed versions: %d   old rule inside a block: %d   new rule moves it: %d" % (n_seed, touched.get("seed", 0), changed.get("seed", 0)))
    print("   what the new rule reads: a heading in %d, no heading outside a block in %d (the entry goes at the end), a fence that never closes in %d (refused)" % (
        sum(1 for r in rows if isinstance(r[1], int)), sum(1 for r in rows if r[1] is None), sum(1 for r in rows if r[1] == "unsafe")))
    print("   distinct versions whose header region (up to the first heading, or the whole text) holds: " +
          ", ".join("%s %d" % (tag, shapes.get(tag, 0)) for tag, _rx in SHAPES))
    print("   disagreements with markdown-it (new rule): %d" % len(disagree))
    for row in disagree[:20]:
        print("     ", row)
    if kinds:
        print("   of those, the tool's line is inside a block of kind:", kinds)
    fails += len(disagree)

# ------------------------------------------------------------------------------------------------------ part B
if "B" in PARTS:
    rng = random.Random(SEED)
    IN_SCOPE = [
        ("month", lambda: "## 2026-%02d" % rng.randint(1, 12)), ("entry", lambda: "### 2026-%02d-%02d · [ad hoc] e" % (rng.randint(1, 12), rng.randint(1, 28))),
        ("prose", lambda: "some prose"), ("blank", lambda: ""),
        ("open3", lambda: "```"), ("open4", lambda: "````"), ("open5", lambda: "`````"), ("openinfo", lambda: "```" + rng.choice(["python", "handoff", "text"])),
        ("tilde3", lambda: "~~~"), ("tilde4", lambda: "~~~~"), ("close3", lambda: "```"), ("close4", lambda: "````"), ("close5", lambda: "`````"),
        ("closeinfo", lambda: "```python"), ("tilde3b", lambda: "~~~"),
    ]
    OUT_OF_SCOPE = [
        ("indented-fence", lambda: " ```"), ("indented-fence2", lambda: "   ~~~"), ("quote-fence", lambda: "> ```"), ("list-fence", lambda: "- ```"),
        ("comment-open", lambda: "<!-- note"), ("comment-close", lambda: "-->"), ("comment-heading", lambda: "<!-- ### 2026-01-01 · x -->"),
        ("indented-heading", lambda: "    ### 2026-01-01 · indented code"),
    ]
    texts, metas = [], []
    for _ in range(COUNT):
        n = rng.randint(1, 16)
        pool = IN_SCOPE + (OUT_OF_SCOPE if rng.random() < 0.3 else [])
        kinds = [rng.choice(pool) for _ in range(n)]
        text = "\n".join(k[1]() for k in kinds) + "\n"
        texts.append(text)
        metas.append(sorted(set(k[0] for k in kinds)))
    res = oracle(texts)
    agree = nofence_same = nofence = out_of_scope = 0
    classes, fails_b = {}, []
    for text, meta, o in zip(texts, metas, res):
        expect = first_outside(text, o["blocked"])
        got = tool(text)
        has_fence = any(k.startswith(("open", "tilde", "close", "indented-fence", "quote-fence", "list-fence")) for k in meta)
        if not has_fence:
            nofence += 1
            if got == old_rule(text):
                nofence_same += 1
            else:
                fails_b.append(("no fence, but not the old answer", text, got, old_rule(text)))
        same = (got == expect) or (got == "unsafe" and o["unterminated"] and expect is None)
        if same:
            agree += 1
            continue
        oos = [k for k in meta if k in dict(OUT_OF_SCOPE)]
        if oos:
            out_of_scope += 1
            for k in oos:
                classes[k] = classes.get(k, 0) + 1
        else:
            fails_b.append(("in-scope disagreement", text, got, expect))
    print("== B. %d random ledger-shaped texts (seed %d)" % (COUNT, SEED))
    print("   agree with markdown-it: %d   disagree, text holds an out-of-scope construct: %d   disagree, in scope: %d" % (agree, out_of_scope, len(fails_b)))
    print("   out-of-scope constructs present in those disagreeing texts (a text can hold several):", dict(sorted(classes.items())))
    print("   texts with no fence line: %d, giving the old rule's answer: %d" % (nofence, nofence_same))
    for row in fails_b[:5]:
        print("   FAIL", row[0], repr(row[1])[:200], "got", row[2], "expect", row[3])
    fails += len(fails_b)

print("RESULT:", "no row differs" if fails == 0 else "%d row(s) differ" % fails)
sys.exit(1 if fails else 0)
