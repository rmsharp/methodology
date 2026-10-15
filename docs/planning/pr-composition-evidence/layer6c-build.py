#!/usr/bin/env python3
"""Build PR2 Part 2's prose layer (the framework documents say where the methodology files sit, and every reference in
them resolves in both layouts) in a candidate clone, as checkpoint commits' worth of edits.

    python3 layer6c-build.py <source-repo> <source-rev> <candidate-clone> --report
    python3 layer6c-build.py <source-repo> <source-rev> <candidate-clone> --stage docs1|docs2|docs3|docs4|tests
                             [--passed N]                                  (tests stage, second run)

Reads each file from <source-rev> of <source-repo> (git show, never the working tree) and writes the stage into
<candidate-clone>, which must hold the previous stage's commit (the first stage: the checkers' layer, `505541c`).
It does NOT commit. Every edit is computed before the first write, so a refusal leaves the clone untouched.
`--report` writes nothing and needs no stage: it prints, for the 23 framework documents, what differs between the
candidate's copy and the tip's and which hunks this layer carries.

Why this layer exists (plan section 3 and section 7 D5, amended 2026-10-14): `bin/migrate-layout`'s own suite needs the
framework documents to resolve in both layouts (the 10 failures `layer7-record.md` measured all need the prose), and the
distributed documents are what an adopter reads about where the files sit.

What it carries, and what it does not. The candidate's copy of each document is upstream's text plus the earlier
layers. The tip's copy differs from it by layout text AND by text that is not layout at all (a session number, the
unmeasured-gate clause, issue #75's plan-surface rule, a model-tag sentence). The probe of `layer7-record.md` put the
tip's 23 documents in whole and so could not tell the two apart. This builder takes the candidate's copy and applies
ONLY the hunks that are layout, taken from the tip's text, and refuses unless what is left of the difference to the
tip's copy is exactly the hunks it names as not layout (NOT_LAYOUT, below). A hunk is a git zero-context hunk.

  A layout hunk is one of two classes, found by rule (and read, every one of the 169 changed lines, in the record):
    reference    a relative markdown link or a `docs/methodology/` path the hunk removes and does not put back: the
                 reference becomes a bare name in a code span, or a path that holds in both layouts
    layout text  added prose that names the `methodology/` layout (Where the files are, Two layouts, the runner's
                 location, the migration command)
  A hunk that is neither, and not named in NOT_LAYOUT, is refused: it is a third kind of change and needs a decision.

Five checkpoint commits of at most five files (the cap is per commit; SAFEGUARDS.md):

  docs1  the operating files     starter-kit/SESSION_RUNNER.md, BOOTSTRAP.md, CLAUDE_TEMPLATE.md, SAFEGUARDS.md, HANDOFFS.md
  docs2  the framework           FRAMEWORK_APPARATUS.md, HOW_TO_USE.md, ITERATIVE_METHODOLOGY.md, starter-kit/CHANGELOG.md,
                                 starter-kit/RECOMMENDED_SKILLS.md
  docs3  the workstreams (1/2)   ARCHITECTURE, AUDIT, DEVELOPMENT, INHERITED_CODEBASE_FAMILIARIZATION_CAMPAIGN,
                                 RESEARCH_EXHAUSTIVE_VERIFICATION_CAMPAIGN
  docs4  the workstreams (2/2)   TEMPLATE_CAMPAIGN, TEMPLATE_WORKSTREAM
  tests  bin/tests.sh            Test 10's second block, cut from the tip: `check-links --layout both` (it reads red until
                                 every reference above is fixed, which is why it comes last)
         .quality-gates.json     tests-sh-passed: the new `pass` line raises the count by one (second run: --passed N)
"""
import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

FRAMEWORK = ("ITERATIVE_METHODOLOGY.md", "FRAMEWORK_APPARATUS.md", "HOW_TO_USE.md")
STAGES = {
    "docs1": ["starter-kit/SESSION_RUNNER.md", "starter-kit/BOOTSTRAP.md", "starter-kit/CLAUDE_TEMPLATE.md",
              "starter-kit/SAFEGUARDS.md", "starter-kit/HANDOFFS.md"],
    "docs2": ["FRAMEWORK_APPARATUS.md", "HOW_TO_USE.md", "ITERATIVE_METHODOLOGY.md", "starter-kit/CHANGELOG.md",
              "starter-kit/RECOMMENDED_SKILLS.md"],
    "docs3": ["workstreams/ARCHITECTURE_WORKSTREAM.md", "workstreams/AUDIT_WORKSTREAM.md",
              "workstreams/DEVELOPMENT_WORKSTREAM.md", "workstreams/INHERITED_CODEBASE_FAMILIARIZATION_CAMPAIGN.md",
              "workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_CAMPAIGN.md"],
    "docs4": ["workstreams/TEMPLATE_CAMPAIGN.md", "workstreams/TEMPLATE_WORKSTREAM.md"],
}
BLOBS = {  # file -> (candidate's blob = upstream's text plus the earlier layers, tip's blob): the premises, asserted first
    "FRAMEWORK_APPARATUS.md": ("33d85df", "7288b95"),
    "HOW_TO_USE.md": ("403dc51", "6e7fdd2"),
    "ITERATIVE_METHODOLOGY.md": ("25bf556", "b993bd5"),
    "starter-kit/BOOTSTRAP.md": ("ecec973", "4bb3b89"),
    "starter-kit/CHANGELOG.md": ("1851833", "1ecf399"),
    "starter-kit/CLAUDE_TEMPLATE.md": ("d9a111d", "e0c35a8"),
    "starter-kit/HANDOFFS.md": ("a0ceafd", "394a52a"),
    "starter-kit/RECOMMENDED_SKILLS.md": ("309722e", "9428257"),
    "starter-kit/SAFEGUARDS.md": ("3ec5a0f", "74bdb17"),
    "starter-kit/SESSION_RUNNER.md": ("71ad950", "dc2d0fb"),
    "workstreams/ARCHITECTURE_WORKSTREAM.md": ("33a86bf", "5fdea95"),
    "workstreams/AUDIT_WORKSTREAM.md": ("a7a247c", "5f4fd1e"),
    "workstreams/DEVELOPMENT_WORKSTREAM.md": ("2dec23d", "ef4e989"),
    "workstreams/INHERITED_CODEBASE_FAMILIARIZATION_CAMPAIGN.md": ("47750b5", "69bcd29"),
    "workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_CAMPAIGN.md": ("c3680a1", "be5ead1"),
    "workstreams/TEMPLATE_CAMPAIGN.md": ("6ad3dc6", "8468d2a"),
    "workstreams/TEMPLATE_WORKSTREAM.md": ("88e6712", "f998e3f"),
}
SESSION_NUMBER = "a session number in prose: fork text, and the scrub would remove it"
UNMEASURED = "the unmeasured-gate clause: the plan's section 4 seam (prose upstream's checker does not enforce)"
SURFACE = "issue #75's plan-surface rule: upstream's runner lacks it and the plan's section 8 leaves it out"
MODEL_TAG = "a model-tag sentence: the fork's own, for a convention upstream's FRAMEWORK_APPARATUS already documents"
NOT_LAYOUT = {  # file -> [(a text in exactly one hunk's added lines, why that hunk is not layout)]
    "HOW_TO_USE.md": [("plus, since S130,", SESSION_NUMBER),
                      ("If it reads unmeasured gates, repair", UNMEASURED)],
    "starter-kit/SESSION_RUNNER.md": [("**The surface** — *where*", SURFACE),
                                      ("Without the **surface** named", SURFACE),
                                      ("Each phase names the SURFACE", SURFACE),
                                      ("A run that reads unmeasured gates is not a clean one", UNMEASURED),
                                      ("Optionally tag the acting model", MODEL_TAG)],
    "starter-kit/HANDOFFS.md": [("A run that reads `U unmeasured`", UNMEASURED)],
}
REL_LINK = re.compile(r"\]\((?!https?://|#)[^)\s]+\)")

TESTS_SH = "bin/tests.sh"
GATES = ".quality-gates.json"
TEST10_FI = '    fail "check-links: dangling link(s) in adopter layout (see above)"\nfi\n'
TEST11 = '\necho "== Test 11: '
BLOCK_FROM = "# BL-101 P9: the documents resolve in BOTH layouts."
BLOCK_TO = '    fail "check-links --layout both: dangling link(s) in one of the layouts (see above)"\nfi\n'
# The block's two comment lines carry a fork token ("BL-101 P9") and a figure that is false on the candidate ("36
# dangling, before P9": the candidate's parent reads 35). They are reworded; every other line is the tip's own.
COMMENT_OLD = (
    "# BL-101 P9: the documents resolve in BOTH layouts. A reference that cannot be a relative link in both is a bare\n"
    "# name in a code span, so one new docs/methodology/ link turns this red (it read exit 1, 36 dangling, before P9).\n")
COMMENT_NEW = (
    "# The documents resolve in BOTH layouts. A reference that cannot be a relative link in both is a bare name in a\n"
    "# code span, so one new docs/methodology/ link turns this red.\n")


def git(src, *args):
    return subprocess.run(["git", "-C", str(src), *args], check=True, capture_output=True).stdout.decode("utf-8")


def show(src, rev, path):
    return git(src, "show", "%s:%s" % (rev, path))


def blob(src, rev, path):
    return git(src, "rev-parse", "--short", "%s:%s" % (rev, path)).strip()


def lines_of(text):
    return re.findall(r"[^\n]*\n|[^\n]+", text)


def once(text, old, new, what):
    if text.count(old) != 1:
        raise SystemExit("refused: %s: expected exactly 1 match, found %d" % (what, text.count(old)))
    return text.replace(old, new)


class Hunk:
    def __init__(self, old_start, old_count, removed, added):
        self.old_start, self.old_count, self.removed, self.added = old_start, old_count, removed, added

    @property
    def plus(self):
        return len(self.added)

    @property
    def minus(self):
        return len(self.removed)

    def added_text(self):
        return "".join(self.added)

    def removed_text(self):
        return "".join(self.removed)


def hunks(old, new):
    """git's zero-context hunks from `old` to `new`."""
    for t in (old, new):
        if not t.endswith("\n"):
            raise SystemExit("refused: a document does not end with a newline")
    with tempfile.TemporaryDirectory() as d:
        a, b = Path(d, "a"), Path(d, "b")
        a.write_bytes(old.encode("utf-8"))
        b.write_bytes(new.encode("utf-8"))
        out = subprocess.run(["git", "diff", "--no-index", "--no-color", "-U0", "--", str(a), str(b)],
                             capture_output=True).stdout.decode("utf-8")
    result, cur = [], None
    for ln in lines_of(out):
        m = re.match(r"@@ -(\d+)(?:,(\d+))? \+\d+(?:,\d+)? @@", ln)
        if m:
            cur = Hunk(int(m.group(1)), int(m.group(2)) if m.group(2) is not None else 1, [], [])
            result.append(cur)
        elif cur is not None and ln.startswith("-"):
            cur.removed.append(ln[1:])
        elif cur is not None and ln.startswith("+"):
            cur.added.append(ln[1:])
        elif cur is not None and ln.startswith("\\"):
            raise SystemExit("refused: a hunk touches a file's last line without a newline")
    return result


def apply(old, hs):
    lines, out, pos = lines_of(old), [], 0
    for h in hs:
        start = h.old_start - 1 if h.old_count else h.old_start
        if lines[start:start + h.old_count] != h.removed:
            raise SystemExit("refused: a hunk's removed lines are not the candidate's lines at %d" % h.old_start)
        out += lines[pos:start] + h.added
        pos = start + h.old_count
    return "".join(out + lines[pos:])


def layout_class(h):
    removed, added = h.removed_text(), h.added_text()
    if (len(REL_LINK.findall(removed)) > len(REL_LINK.findall(added))
            or removed.count("docs/methodology/") > added.count("docs/methodology/")):
        return "reference"
    if "methodology/" in added or "layout" in added.lower():
        return "layout text"
    return None


def partition(rel, old, new):
    """(layout hunks as (hunk, class), not-layout hunks as (hunk, why)); refuses a hunk that is neither."""
    marks = NOT_LAYOUT.get(rel, [])
    layout, other, used = [], [], {}
    for h in hunks(old, new):
        hit = [m for m in marks if m[0] in h.added_text()]
        if len(hit) > 1:
            raise SystemExit("refused: %s: one hunk matches %d not-layout markers" % (rel, len(hit)))
        if hit:
            used[hit[0][0]] = used.get(hit[0][0], 0) + 1
            other.append((h, hit[0][1]))
            continue
        cls = layout_class(h)
        if cls is None:
            raise SystemExit("refused: %s: a hunk at line %d is neither a layout hunk nor named in NOT_LAYOUT: %r"
                             % (rel, h.old_start, h.added_text()[:120]))
        layout.append((h, cls))
    for text, _ in marks:
        if used.get(text, 0) != 1:
            raise SystemExit("refused: %s: the not-layout marker %r matched %d hunks, expected 1" % (rel, text, used.get(text, 0)))
    return layout, other


def built(rel, old, new):
    layout, other = partition(rel, old, new)
    text = apply(old, [h for h, _ in layout])
    # what is left of the difference to the tip must be exactly the named not-layout hunks, nothing more, nothing less
    left = hunks(text, new)
    want = sorted((h.removed_text(), h.added_text()) for h, _ in other)
    got = sorted((h.removed_text(), h.added_text()) for h in left)
    if want != got:
        raise SystemExit("refused: %s: what is left of the difference to the tip is not exactly the named hunks" % rel)
    return text


def check_premises(src, rev, dst, files):
    for rel in files:
        cand, tip = BLOBS[rel]
        got = blob(src, rev, rel)
        if got != tip:
            raise SystemExit("refused: %s at %s is blob %s, this builder was written against %s" % (rel, rev, got, tip))
        have = subprocess.run(["git", "-C", str(dst), "rev-parse", "--short", "HEAD:" + rel], capture_output=True,
                              text=True).stdout.strip()
        if have != cand:
            raise SystemExit("refused: %s in the candidate is blob %s, not %s; the premise (the layer is the candidate's "
                             "copy plus the tip's layout hunks) does not hold" % (rel, have, cand))


def documents(src, rev):
    names = git(src, "ls-tree", "-r", "--name-only", rev, "--", "starter-kit", "workstreams", *FRAMEWORK).split("\n")
    return sorted(n for n in names if n.endswith(".md"))


def report(src, rev, dst, cand_rev):
    docs = documents(src, rev)
    print("layer6c-build --report: tip %s, candidate %s" % (git(src, "rev-parse", "--short", rev).strip(),
                                                           git(dst, "rev-parse", "--short", cand_rev).strip()))
    print("%d framework documents (every Markdown file under starter-kit/ and workstreams/, plus %s)" % (len(docs), ", ".join(FRAMEWORK)))
    rows, other_all, same = [], [], []
    for rel in docs:
        old = show(dst, cand_rev, rel)
        new = show(src, rev, rel)
        if old == new:
            same.append(rel)
            continue
        if rel not in BLOBS:
            raise SystemExit("refused: %s differs and this builder does not know it" % rel)
        layout, other = partition(rel, old, new)
        agg = {}
        for h, cls in layout:
            a = agg.setdefault(cls, [0, 0, 0])
            a[0] += 1; a[1] += h.plus; a[2] += h.minus
        o = [len(other), sum(h.plus for h, _ in other), sum(h.minus for h, _ in other)]
        rows.append((rel, agg.get("reference", [0, 0, 0]), agg.get("layout text", [0, 0, 0]), o))
        other_all += [(rel, h, why) for h, why in other]
    print("\n%d differ from the candidate's copy, %d are equal (carried: nothing): %s\n" % (len(rows), len(same), ", ".join(same)))
    fmt = "%-58s %14s %14s %14s"
    cell = lambda a: "%d (+%d -%d)" % tuple(a)
    print(fmt % ("file", "reference", "layout text", "NOT layout"))
    tot = [[0, 0, 0] for _ in range(3)]
    for rel, r, t, o in rows:
        print(fmt % (rel, cell(r), cell(t), cell(o)))
        for k, c in enumerate((r, t, o)):
            tot[k] = [x + y for x, y in zip(tot[k], c)]
    print(fmt % ("total (hunks, lines added, lines removed)", cell(tot[0]), cell(tot[1]), cell(tot[2])))
    print("\nall: +%d -%d over %d hunks; carried by this layer: +%d -%d over %d hunks"
          % (tot[0][1] + tot[1][1] + tot[2][1], tot[0][2] + tot[1][2] + tot[2][2], tot[0][0] + tot[1][0] + tot[2][0],
             tot[0][1] + tot[1][1], tot[0][2] + tot[1][2], tot[0][0] + tot[1][0]))
    print("\nthe hunks NOT carried (candidate line, lines, why, the first words added):")
    for rel, h, why in other_all:
        print("  %s @%d +%d -%d  %s\n      %r" % (rel, h.old_start, h.plus, h.minus, why, h.added_text().strip()[:110]))
    print("\nthe stages (files per commit, cap 5): " + ", ".join("%s %d" % (k, len(v)) for k, v in STAGES.items()) + ", tests 2")
    staged = [f for v in STAGES.values() for f in v]
    if sorted(staged) != sorted(r[0] for r in rows):
        raise SystemExit("refused: the stages do not name exactly the documents that differ")
    print("the stages name exactly the %d documents that differ" % len(staged))


def stage_docs(src, rev, dst, name):
    files = STAGES[name]
    dirty = git(dst, "status", "--porcelain", "--", *files).strip()
    if dirty:
        raise SystemExit("refused: the clone has uncommitted changes in this stage's files:\n" + dirty)
    check_premises(src, rev, dst, files)
    return [(rel, built(rel, show(dst, "HEAD", rel), show(src, rev, rel))) for rel in files]


def stage_tests(src, rev, dst, passed):
    out = []
    if passed is None:
        tip = show(src, rev, TESTS_SH)
        a = tip.index(BLOCK_FROM)
        b = tip.index(BLOCK_TO, a) + len(BLOCK_TO)
        block = tip[a:b]
        if tip.count(block) != 1 or tip.index(TEST10_FI) + len(TEST10_FI) != a:
            raise SystemExit("refused: the tip's second Test 10 block does not follow the first")
        block = once(block, COMMENT_OLD, COMMENT_NEW, "the block's comment")
        sh = (Path(dst) / TESTS_SH).read_text(encoding="utf-8")
        out.append((TESTS_SH, once(sh, TEST10_FI + TEST11, TEST10_FI + block + TEST11, "Test 10's place")))
    else:
        gates = (Path(dst) / GATES).read_text(encoding="utf-8")
        pat = re.compile(r'("name": "tests-sh-passed",\n\s+"direction": "min",\n\s+"threshold": )(\d+),')
        if len(pat.findall(gates)) != 1:
            raise SystemExit("refused: gate tests-sh-passed: expected exactly 1 match")
        out.append((GATES, pat.sub(lambda m: m.group(1) + "%d," % passed, gates)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("rev")
    ap.add_argument("dst")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--stage", choices=tuple(STAGES) + ("tests",))
    ap.add_argument("--passed", type=int)
    ap.add_argument("--candidate-rev", default="HEAD", help="--report only: the candidate's revision in <candidate-clone>")
    args = ap.parse_args()
    if args.report == bool(args.stage):
        raise SystemExit("refused: give exactly one of --report and --stage")
    if args.report:
        report(args.src, args.rev, Path(args.dst), args.candidate_rev)
        return 0
    if args.passed is not None and args.stage != "tests":
        raise SystemExit("refused: --passed belongs to the tests stage")
    dst = Path(args.dst)
    edits = stage_tests(args.src, args.rev, dst, args.passed) if args.stage == "tests" else stage_docs(args.src, args.rev, dst, args.stage)
    for rel, text in edits:
        p = dst / rel
        p.write_text(text, encoding="utf-8")
    print("stage %s written: %s" % (args.stage, ", ".join(rel for rel, _ in edits)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
