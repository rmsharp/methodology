"""Measure the two candidate stub markers for SESSION_NOTES.md on the #93 repository's seven real
stubs (record 0 at each trim commit's parent) and the records that replaced them.

usage: marker_measure.py REPO_DIR            (a clone of rmsharp/nprcgenekeepr holding the trim commits)
Read-only: `git show` only. The seven trim commits are those S334's stub_survival.py found."""
import re, subprocess, sys
repo = sys.argv[1]
def git(*a): return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True).stdout
START = re.compile(r"^### (?:Session \d+ Handoff Evaluation \(by Session \d+\)|What Session \d+ Did\b)")
def records(text):
    lines = text.split("\n"); idx = [i for i, l in enumerate(lines) if START.match(l)]
    return [(lines[a], "\n".join(lines[a:b])) for a, b in zip(idx, idx[1:] + [len(lines)])]
LINE_ONLY = re.compile(r"^\*\*Status:\*\* Session claimed\b.*$", re.M)
BOTH = re.compile(r"(?ms)\A(?=.*^\*\*Status:\*\* Session claimed\b)(?=.*\(IN PROGRESS\))", re.M)
print("trim_commit\tstub_line_only\tstub_both\tsuccessor_line_only\tsuccessor_both\tstub_bytes")
for T in ["850e367", "b528b8b", "55da128", "8b2e3f9", "8c9c5ea", "0fc874f", "618e5c1"]:
    before = records(git("show", T + "^:SESSION_NOTES.md")); after = records(git("show", T + ":SESSION_NOTES.md"))
    head, stub = before[0]
    succ = next((r for h, r in after if h == head), "")
    print("\t".join([T, str(bool(LINE_ONLY.search(stub))), str(bool(BOTH.search(stub))),
                     str(bool(LINE_ONLY.search(succ))), str(bool(BOTH.search(succ))), str(len(stub.encode()))]))
