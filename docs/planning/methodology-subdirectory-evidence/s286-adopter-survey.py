#!/usr/bin/env python3
"""Which tracked files of an adopter NAME a file the methodology/ move relocates, by kind of file?

S286, BL-101 plan section 7.4 ("tier 1 until it is surveyed"). READ-ONLY: every call into an adopter is
`git ... ls-tree`, `grep`, `rev-parse`, `rev-list` or `--no-optional-locks status`; nothing is written there.
The surface is the COMMITTED tree at one revision (`git grep <rev>`), so an untracked or ignored file is not seen.

WHAT IT CAN AND CANNOT SHOW. It finds files that NAME a moved file on a line that is not a comment. It cannot show
that the name breaks at run time: the S286 control (model_project_constructor before its move) found 13 proofs
carrying the same `LIVE = "SESSION_NOTES.md"` line of which 2 broke, because the other 11 read the ledger at an old
commit through git, which a move cannot touch. So a hit is a CANDIDATE and the count is an UPPER BOUND; the answer
for any one adopter is its own rehearsal in a clone (plan 7.4). A ZERO is the useful result: nothing to rehearse.

The moved set is bin/migrate-layout's own (DISTRIBUTION, GENERATED), read from the tool, not retyped.

Usage (run from anywhere; python3 -I keeps the script's directory off sys.path):
    python3 -I s286-adopter-survey.py [--portfolio ~/Development] [--lines FILE] [--only NAME[,NAME]]
    python3 -I s286-adopter-survey.py --control    # model_project_constructor at 0dc3051; exit 1 unless it finds S285's 4
"""
import argparse
import importlib.machinery
import importlib.util
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANON = HERE.parent.parent.parent  # <canonical>/docs/planning/methodology-subdirectory-evidence -> <canonical>
ADOPTERS = ["airqino", "chat_verification", "church_growth", "claude_work", "dalia_martinez_funeral",
            "feedback-loop-comparison", "mts-system", "nprcgenekeepr", "Philippians", "vscode_quarto_ext", "wsfct"]
CONTROL = ("model_project_constructor", "0dc3051")
# S285 (record p11-model-project-constructor-record.md, plan 7.4a): what this adopter's own CI showed to break.
#   tier 1: tests/test_read_budget.py (RUNNER = SESSION_RUNNER.md, repaired in ec23bc7)
#   tier 2: the two proofs (LIVE = the ledger) and the two test files (path constants, heading literals)
CONTROL_KNOWN = {
    "tests/test_read_budget.py": {1, 2},
    "tests/test_session_notes_census.py": {2},
    "docs/architecture-history/SESSION_NOTES-pointer-collapse.verify.sh": {2},
    "docs/architecture-history/SESSION_NOTES-pointer-collapse-S254.verify.sh": {2},
}
COMMENT = ("#", "//", "<!--", "/*", "*", ";", "%")  # a comment-only line cannot change what a machine does
TEST_DIR = re.compile(r"(^|/)(tests?|specs?|testthat|__tests__)(/|$)")
TEST_FILE = re.compile(r"(^|/)(test_[^/]*|[^/]*_test\.[^/]*|[^/]*\.test\.[^/]*|[^/]*_spec\.[^/]*|conftest\.py)$")
SCRIPT_EXT = (".sh", ".bash", ".zsh", ".py", ".r", ".R", ".js", ".mjs", ".cjs", ".ts", ".rb", ".pl", ".ps1", ".bat", ".jl")
PROSE_EXT = (".md", ".qmd", ".rmd", ".Rmd", ".rst", ".txt", ".tex", ".html", ".adoc")
CONFIG_EXT = (".json", ".toml", ".yml", ".yaml", ".cfg", ".ini")
CONFIG_NAME = {".Rbuildignore", ".dockerignore", "Makefile", "DESCRIPTION", "NAMESPACE", "Dockerfile"}
# The tool does not rewrite these, and a machine runs or reads them. Not counted: claude_md, tool_config, gitignore
# (the tool rewrites them as text), claude (.claude/ permission strings: prompts only), prose, other.
RUNNABLE = ("ci", "hook", "proof", "test", "script", "config")


def load_tool():
    loader = importlib.machinery.SourceFileLoader("ml", str(CANON / "bin" / "migrate-layout"))
    sys.path.insert(0, str(CANON / "bin"))
    spec = importlib.util.spec_from_loader("ml", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


def tokens(mod):
    """(strong, weak): name -> tier, from the tool's own tables.
    strong = the file name as written in a path (`SESSION_NOTES.md`, `.context-budget.json`, `docs/methodology/`);
    weak   = its stem (`SESSION_NOTES`), which also hits a prose word, a module name, or a path built in two pieces.
    `dashboard` alone and `-through-` are not names (S286: with these, the comment rule and the strong/weak split, the control's
    further machine-read files fell from 29 to 21; the four known files were found before and after)."""
    strong, weak = {}, {}
    for _src, legacy, disp in mod.DISTRIBUTION:
        tier = 1 if disp == mod.TRACKED else 2
        base = os.path.basename(legacy)
        strong[base] = tier
        if not base.startswith("."):
            weak[re.sub(r"\.(md|py|json)$", "", base)] = tier
    strong["docs/methodology/"] = 1
    strong["docs/archive/"] = 2
    for name in mod.GENERATED:
        strong[name] = 2
    weak["dashboard_history"] = 2
    weak["context-budget"] = 2
    weak["quality-gates"] = 2
    return strong, weak


def git(repo, *args, check=True):
    r = subprocess.run(["git", "--no-optional-locks", "-C", str(repo), *args], capture_output=True, text=True, errors="replace")
    if check and r.returncode not in (0, 1):
        raise RuntimeError("git %s failed in %s: %s" % (" ".join(args), repo, r.stderr.strip()[:200]))
    return r


def kind_of(path, mode):
    base = path.rsplit("/", 1)[-1]
    if path.startswith((".github/workflows/", ".circleci/")) or base in (".gitlab-ci.yml", "Jenkinsfile", "azure-pipelines.yml"):
        return "ci"
    if path.startswith((".githooks/", ".husky/")) or base == ".pre-commit-config.yaml":
        return "hook"
    if path.startswith(".claude/"):
        return "claude"
    if base == "CLAUDE.md":
        return "claude_md"
    if base == ".gitignore":
        return "gitignore"
    if base in (".context-budget.json", ".quality-gates.json"):
        return "tool_config"
    if base.endswith(".verify.sh") or re.match(r"verify[^/]*\.sh$", base):
        return "proof"
    if TEST_DIR.search(path) or TEST_FILE.search(path):
        return "test"
    if base in CONFIG_NAME or base.endswith(CONFIG_EXT):
        return "config"
    if base.endswith(SCRIPT_EXT) or mode == "100755":
        return "script"
    if base.endswith(PROSE_EXT):
        return "prose"
    return "other"


def tiers_of(names, tiers):
    return {tiers[n] for n in names}


def survey(label, repo, rev, mod, strong, weak, fh):
    rows = {"label": label}
    head = git(repo, "rev-parse", rev).stdout.strip()
    rows["rev"] = head[:7]
    rows["branch"] = git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    rows["dirty"] = len([x for x in git(repo, "status", "--porcelain").stdout.splitlines() if x])
    ab = git(repo, "rev-list", "--left-right", "--count", "@{upstream}...HEAD", check=False)
    rows["upstream"] = ab.stdout.strip().replace("\t", " ") if ab.returncode == 0 else "no upstream"
    files = {}
    for ln in git(repo, "ls-tree", "-r", "--full-tree", rev).stdout.splitlines():
        meta, path = ln.split("\t", 1)
        files[path] = meta.split()[0]
    rows["tracked"] = len(files)
    rows["dest_taken"] = sorted(p for p in files if p == "methodology" or p.startswith("methodology/"))
    moved = {legacy for _s, legacy, _d in mod.DISTRIBUTION} | set(mod.GENERATED)
    selfp = {p for p in files if p in moved or p.startswith(mod.OLD_FRAMEWORK_DIR + "/")
             or (p.startswith(mod.ARCHIVE_OLD + "/") and mod.SHARD_RE.match(p[len(mod.ARCHIVE_OLD) + 1:]))}
    rows["self"] = len(selfp)
    rows["layout"] = " ".join(x for x in (
        "docs/methodology/" if any(p.startswith("docs/methodology/") for p in files) else "",
        "root-runner" if "SESSION_RUNNER.md" in files else "",
        "methodology/-tracked" if rows["dest_taken"] else "") if x) or "none"
    union = "|".join(re.escape(x) for x in list(strong) + list(weak))
    g = git(repo, "grep", "-n", "-I", "-E", "-e", union, rev, "--", ".", check=False)
    hits = defaultdict(list)  # path -> [(lineno, text)]
    for ln in g.stdout.splitlines():
        body = ln[len(rev) + 1:] if ln.startswith(rev + ":") else ln.split(":", 1)[1]
        path, lineno, text = body.split(":", 2)
        if path not in selfp:
            hits[path].append((int(lineno), text))
    per = {}
    for path, hl in hits.items():
        s_names, w_names, code = defaultdict(int), defaultdict(int), 0
        for _, text in hl:
            if text.lstrip().startswith(COMMENT):
                continue
            code += 1
            present = [x for x in strong if x in text]
            for x in present:
                s_names[x] += 1
            for x in weak:
                if x in text and not any(y.startswith(x) for y in present):
                    w_names[x] += 1
        per[path] = {"kind": kind_of(path, files.get(path, "")), "strong": dict(s_names), "weak": dict(w_names), "code": code, "hl": hl}
    rows["per"], rows["files"] = per, files
    if fh:
        fh.write("\n#### %s @ %s (checked-out branch %s) -- every matching line of every MACHINE-READ non-moved tracked file, by path\n"
                 "# (prose, CLAUDE.md and ignore files are counted in the report but not quoted: some adopters are private)\n"
                 % (label, rows["rev"], rows["branch"]))
        for path in sorted(per):
            v = per[path]
            if v["kind"] not in RUNNABLE:
                continue
            fh.write("\n## %s  [%s]  strong=%s weak=%s code-lines=%d\n" % (path, v["kind"], v["strong"] or "-", v["weak"] or "-", v["code"]))
            for lineno, text in v["hl"][:60]:
                fh.write("%6d: %s\n" % (lineno, text.strip()[:220]))
            if len(v["hl"]) > 60:
                fh.write("   ... %d more lines\n" % (len(v["hl"]) - 60))
    return rows


def report(rows, strong):
    per = rows["per"]
    out = ["== %s  rev %s  checked-out branch %s  dirty %d  upstream(behind ahead) %s  tracked %d  self(moved or old copies) %d" % (
        rows["label"], rows["rev"], rows["branch"], rows["dirty"], rows["upstream"], rows["tracked"], rows["self"]),
        "   layout: %s   destination methodology/ already tracked: %s" % (rows["layout"], rows["dest_taken"][:3] or "no")]
    by = defaultdict(lambda: [0, 0, 0])  # kind -> files naming anything, with a strong name on a non-comment line, with only a weak name
    for v in per.values():
        by[v["kind"]][0] += 1
        by[v["kind"]][1] += 1 if v["strong"] else 0
        by[v["kind"]][2] += 1 if (v["weak"] and not v["strong"]) else 0
    out.append("   files naming a moved name, by kind (any / strong on a code line / weak only on a code line):")
    for k in sorted(by):
        out.append("     %-11s %3d / %3d / %3d%s" % (k, *by[k], "   <- machine-read" if k in RUNNABLE else ""))
    run = sorted((p for p, v in per.items() if v["kind"] in RUNNABLE and (v["strong"] or v["weak"])),
                 key=lambda p: (RUNNABLE.index(per[p]["kind"]), p))
    strong_run = [p for p in run if per[p]["strong"]]
    out.append("   machine-read files with a strong name on a code line: %d   (weak-only: %d)   <- the candidates" % (
        len(strong_run), len(run) - len(strong_run)))
    for p in run:
        v = per[p]
        out.append("     [%-6s] %s  %s  strong=%s weak=%s  code-lines=%d" % (
            v["kind"], "S" if v["strong"] else "w", p, ",".join(sorted(v["strong"])) or "-", ",".join(sorted(v["weak"])) or "-", v["code"]))
    return out, run


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--portfolio", default=os.path.expanduser("~/Development"))
    ap.add_argument("--lines", help="one file for the raw matching lines of the machine-read candidates, a section per adopter")
    ap.add_argument("--only", help="comma-separated adopter names")
    ap.add_argument("--rev", action="append", default=[], metavar="NAME=REF",
                    help="survey this ref of an adopter instead of its checked-out HEAD (wsfct: its default branch is master)")
    ap.add_argument("--control", action="store_true", help="the instrument check: model_project_constructor before its move")
    a = ap.parse_args()
    mod = load_tool()
    strong, weak = tokens(mod)
    ld = open(a.lines, "w", encoding="utf-8") if a.lines else None
    revs = dict(x.split("=", 1) for x in a.rev)
    print("survey instrument: s286-adopter-survey.py   canonical %s @ %s" % (CANON, git(CANON, "rev-parse", "--short", "HEAD").stdout.strip()))
    print("strong names (%d): %s" % (len(strong), ", ".join(sorted(strong))))
    print("weak names (%d): %s" % (len(weak), ", ".join(sorted(weak))))
    if a.control:
        name, rev = CONTROL
        rows = survey(name + "@" + rev, Path(a.portfolio) / name, rev, mod, strong, weak, ld)
        lines, run = report(rows, strong)
        print("\n".join(lines))
        per, miss = rows["per"], []
        for p, want in CONTROL_KNOWN.items():
            v = per.get(p, {"strong": {}, "weak": {}})
            got = {strong[n] for n in v["strong"]}
            ok = want <= got
            print("   control %-72s expected tiers %s  strong-name tiers found %s %s" % (p, sorted(want), sorted(got), "OK" if ok else "MISS"))
            if not ok:
                miss.append(p)
        extra = [p for p in run if p not in CONTROL_KNOWN and per[p]["strong"]]
        print("   control: %d of %d known files found with their tiers; %d further machine-read files carry a strong name on a code line "
              "(none is among S285's failures)" % (len(CONTROL_KNOWN) - len(miss), len(CONTROL_KNOWN), len(extra)))
        return 1 if miss else 0
    for name in ADOPTERS:
        if a.only and name not in a.only.split(","):
            continue
        repo = Path(a.portfolio) / name
        if not (repo / ".git").exists():
            print("== %s  NOT A GIT REPOSITORY at %s" % (name, repo))
            continue
        if git(repo, "rev-parse", "--verify", "-q", "HEAD", check=False).returncode != 0:
            n = len(git(repo, "ls-files").stdout.splitlines())
            print("== %s  NO COMMITS on the checked-out branch (%d tracked files): the committed-tree surface is empty, and "
                  "bin/migrate-layout refuses a project with no commit" % (name, n))
            continue
        rev = revs.get(name, "HEAD")
        rows = survey(name if rev == "HEAD" else "%s@%s" % (name, rev), repo, rev, mod, strong, weak, ld)
        print("\n".join(report(rows, strong)[0]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
