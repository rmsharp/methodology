#!/usr/bin/env python3
"""Reference inventory for the methodology/ subdirectory move.

For every methodology file name, count the lines (and files) in each consumer class that
mention it, over TRACKED files at HEAD (git grep), so the count is the same on every clone.
Usage (from the repo root, at the commit the plan names):
    python3 -I docs/planning/methodology-subdirectory-evidence/inventory.py            # the table + distinct files per class
    python3 -I docs/planning/methodology-subdirectory-evidence/inventory.py --lines NAME   # also list every file naming NAME
The plan's numbers were taken at c8b9ddd with this script; a later HEAD gives later numbers.
"""
import subprocess, sys, re, collections

# (token, regex that matches the NAME wherever it is written, group)
TOKENS = [
    ("SESSION_RUNNER.md", r"SESSION_RUNNER(\.md)?", "root-tracked"),
    ("FRAMEWORK_LEARNINGS.md", r"FRAMEWORK_LEARNINGS(\.md)?", "root-tracked"),
    ("SAFEGUARDS.md", r"SAFEGUARDS(\.md)?", "root-tracked"),
    ("RECOMMENDED_SKILLS.md", r"RECOMMENDED_SKILLS(\.md)?", "root-tracked"),
    ("CONTEXT_TEMPLATE.md", r"CONTEXT_TEMPLATE(\.md)?", "root-tracked"),
    ("CLAUDE_TEMPLATE.md", r"CLAUDE_TEMPLATE(\.md)?", "root-tracked"),
    ("BOOTSTRAP.md", r"BOOTSTRAP(\.md)?", "root-tracked"),
    ("methodology_dashboard.py", r"methodology_dashboard(\.py)?", "root-tracked"),
    ("methodology_trim.py", r"methodology_trim(\.py)?", "root-tracked"),
    ("context_budget.py", r"context_budget(\.py)?", "root-tracked"),
    ("quality_ratchet.py", r"quality_ratchet(\.py)?", "root-tracked"),
    ("SESSION_NOTES.md", r"SESSION_NOTES(\.md)?", "root-seed"),
    ("CHANGELOG.md", r"CHANGELOG(\.md)?", "root-seed"),
    ("HANDOFFS.md", r"HANDOFFS(\.md)?", "root-seed"),
    ("ROADMAP.md", r"ROADMAP(\.md)?", "root-seed"),
    (".context-budget.json", r"\.context-budget(\.json)?", "root-seed"),
    (".quality-gates.json", r"\.quality-gates(\.json)?", "root-seed"),
    (".gitattributes", r"\.gitattributes", "root-seed"),
    ("ITERATIVE_METHODOLOGY.md", r"ITERATIVE_METHODOLOGY(\.md)?", "docs/methodology"),
    ("HOW_TO_USE.md", r"HOW_TO_USE(\.md)?", "docs/methodology"),
    ("FRAMEWORK_APPARATUS.md", r"FRAMEWORK_APPARATUS(\.md)?", "docs/methodology"),
    ("workstreams/", r"workstreams/|_WORKSTREAM\.md|_CAMPAIGN\.md", "docs/methodology"),
    ("docs/methodology (path)", r"docs/methodology", "layout-path"),
    ("starter-kit/ (path)", r"starter-kit/", "layout-path"),
]

# consumer classes, first match wins (pathspec prefixes / exact names)
def classify(path):
    if path.startswith(("docs/archive/",)) or path in ("CHANGELOG.md", "HANDOFFS.md") \
            or re.match(r"docs/(HANDOFFS_ARCHIVE_INDEX|versioning-archive|RELEASE_HISTORY)\.md$", path) \
            or path.startswith("docs/planning/") or path.startswith("docs/audits/") \
            or path.startswith("docs/tutorials/") or path == "dashboard_history.jsonl" \
            or path == ".context-budget-history.jsonl" or path.endswith(".verify.sh"):
        return "history/planning (frozen or fork-only record)"
    if path.startswith(("bin/", "tools/", ".githooks/")) or path.endswith(".py") \
            or path in (".quality-gates.json", ".context-budget.json", ".gitattributes", ".gitignore") \
            or path.startswith("starter-kit/") and path.rsplit("/", 1)[-1] in (
                "context-budget.json", "quality-gates.json", "gitattributes"):
        return "code+config"
    if path.startswith("starter-kit/") or path.startswith("workstreams/") \
            or path in ("ITERATIVE_METHODOLOGY.md", "HOW_TO_USE.md", "FRAMEWORK_APPARATUS.md"):
        return "distributed docs"
    return "canonical-only docs"  # README.md, CLAUDE.md, docs/*.md other, LICENSE...

CLASSES = ["code+config", "distributed docs", "canonical-only docs",
           "history/planning (frozen or fork-only record)"]

def tracked():
    out = subprocess.run(["git", "ls-files", "-z"], capture_output=True, text=True, check=True).stdout
    return [p for p in out.split("\0") if p]

def main():
    files = tracked()
    # read each text file once
    content = {}
    for p in files:
        try:
            with open(p, "r", encoding="utf-8") as fh:
                content[p] = fh.read().splitlines()
        except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError, OSError):
            continue
    only = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--lines" else None
    print(f"tracked files read: {len(content)} of {len(files)}")
    hdr = f"{'name':28s} {'group':16s} " + " ".join(f"{c.split(' ')[0][:11]:>13s}" for c in CLASSES)
    print(hdr)
    print("(each cell: files/lines mentioning the name)")
    tot_files = collections.Counter(); tot_lines = collections.Counter()
    for token, rx, group in TOKENS:
        cre = re.compile(rx)
        per = {c: [0, 0] for c in CLASSES}
        for p, lines in content.items():
            n = sum(1 for ln in lines if cre.search(ln))
            if n:
                cls = classify(p)
                per[cls][0] += 1; per[cls][1] += n
                if only == token:
                    print(f"   {cls[:10]:10s} {p}: {n}")
        row = " ".join(f"{per[c][0]:>5d}/{per[c][1]:<7d}" for c in CLASSES)
        print(f"{token:28s} {group:16s} {row}")
        for c in CLASSES:
            tot_files[c] += per[c][0]; tot_lines[c] += per[c][1]
    print("(sum of per-name cells; a file naming several names is counted once per name)")
    print(f"{'SUM':28s} {'':16s} " + " ".join(f"{tot_files[c]:>5d}/{tot_lines[c]:<7d}" for c in CLASSES))
    # distinct files per class (the plan's "files to change" lists come from here)
    hits = collections.defaultdict(lambda: collections.defaultdict(int))
    for p, lines in content.items():
        for token, rx, group in TOKENS:
            cre = re.compile(rx)
            n = sum(1 for ln in lines if cre.search(ln))
            if n:
                hits[p][token] = n
    byclass = collections.defaultdict(list)
    for p in hits:
        byclass[classify(p)].append(p)
    print()
    for c in CLASSES:
        ps = sorted(byclass[c])
        print(f"{c}: {len(ps)} distinct files")
    for c in ["code+config", "distributed docs", "canonical-only docs"]:
        print(f"\n== {c}: files (name-mentions, distinct names) ==")
        for p in sorted(byclass[c]):
            print(f"  {sum(hits[p].values()):5d} {len(hits[p]):2d} {p}")

main()
