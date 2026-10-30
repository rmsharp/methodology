#!/usr/bin/env python3
"""PR4: read-only checks of the pull request's body (the text below the first rule of the draft file).

  python3 docs/planning/pr-composition-evidence/pr4-body-check.py <draft.md> <candidate> <upstream> [<hash> ...]

1. no session number, backlog or plan code, finding label, or coined name (the pattern list is printed, with each hit);
2. no `@@placeholder@@` left;
3. every commit hash the body cites resolves in the repository and is inside <upstream>..<candidate>, unless it is
   <upstream>'s own tip or one of the <hash> arguments (the hashes the text itself names as not the branch's);
4. every path the body cites in backticks exists in the candidate's tree, in upstream's tree, or is one of the two
   fork-side evidence scripts it names;
5. the size, byte and count the body states about the repository, recomputed.
Prints one line per check; exit 0 only when every check is clean."""
import re
import subprocess
import sys

draft, cand, up = sys.argv[1:4]
text = open(draft, encoding="utf-8").read()
body = text.split("\n---\n", 1)[1]
URL = "https://github.com/rmsharp/methodology/tree/main/docs/planning/pr-composition-evidence"
body = body.replace(URL, "<FORK-EVIDENCE-URL>")   # the one link to the fork's evidence directory is allowed to name its path


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True).stdout


bad = 0
BANNED = [
    (r"\bS[0-9]{2,4}\b", "session number"),
    (r"\bBL-[0-9]+", "backlog code"),
    (r"\bF[0-9]{1,2}\b", "finding label"),
    (r"\bD[0-9]{1,2}\b", "decision code"),
    (r"\bP[0-9]{1,2}\b", "plan phase"),
    (r"\bPR[0-9]\b", "plan phase"),
    (r"docs/planning", "fork planning path"),
    (r"(?i)\bcandidate\b", "coined name"),
    (r"(?i)\bscrub", "coined name"),
    (r"(?i)\bregister\b", "coined name"),
    (r"(?i)\boperator\b", "coined name"),
    (r"(?i)fork learning", "coined name"),
    (r"(?i)\bpart [12]\b", "coined name"),
    (r"(?i)\blayer [0-9]", "coined name"),
    (r"@@", "placeholder"),
]
for pat, what in BANNED:
    hits = [m for m in re.finditer(pat, body)]
    if hits:
        bad += 1
        for m in hits:
            line = body[: m.start()].count("\n") + 1
            print(f"BANNED {what}: {m.group(0)!r} at body line {line}: {body.splitlines()[line - 1][:110]}")
if not bad:
    print("no banned token, no placeholder")

# 3: hashes
shas = sorted(set(re.findall(r"`([0-9a-f]{7,12})`", body)))
inrange = set(git("rev-list", f"{up}..{cand}").split())
allowed = {git("rev-parse", "--verify", "-q", up + "^{commit}").strip(): "upstream's tip"}
named = {}
for a in sys.argv[4:]:
    full = git("rev-parse", "--verify", "-q", a + "^{commit}").strip()
    if not full:
        print(f"UNRESOLVED allowed hash {a!r}")
        bad += 1
    else:
        allowed.setdefault(full, "named on the command line")
        named[full] = a
n_bad = 0
cited = set()
for s in shas:
    full = git("rev-parse", "--verify", "-q", s + "^{commit}").strip()
    if not full:
        print(f"UNRESOLVED hash `{s}`")
        n_bad += 1
        continue
    cited.add(full)
    line = f"hash `{s}` resolves; in upstream..candidate: {full in inrange}"
    if full in inrange:
        print(line)
    elif full in allowed:
        print(f"{line}; allowed ({allowed[full]})")
    else:
        print(f"{line}; OUTSIDE and not allowed")
        n_bad += 1
for full, a in named.items():
    if full not in cited:
        print(f"allowed hash {a!r} is not cited in the body")
bad += n_bad

# 4: paths
names = {n.rsplit("/", 1)[-1] for rev in (cand, up) for n in git("ls-tree", "-r", "--name-only", rev).split("\n")}
paths = sorted(set(re.findall(r"`((?:[A-Za-z0-9_.\-]+/)+[A-Za-z0-9_.\-]+|[A-Z_]+\.md|[a-z_]+\.py|pr[0-9]-[a-z\-]+\.(?:sh|py))`", body)))
for p in paths:
    if p == "rmsharp/methodology":
        ok = "the fork's name, not a path"
    elif re.fullmatch(r"pr[0-9]-[a-z\-]+\.(?:sh|py)", p):
        ok = "evidence script (named as in the fork's directory)"
    elif "/" not in p and p in names:
        ok = "a file of that name exists"
    elif git("cat-file", "-t", f"{cand}:{p}").strip() == "blob":
        ok = "in the branch"
    elif git("cat-file", "-t", f"{up}:{p}").strip() == "blob":
        ok = "in upstream only"
    elif p.endswith("/") or git("cat-file", "-t", f"{cand}:{p}").strip() == "tree":
        ok = "a directory"
    else:
        ok = None
    if ok is None:
        print(f"PATH NOT FOUND `{p}`")
        bad += 1
print(f"{len(paths)} paths cited")

# 5: sizes
st = git("diff", "--shortstat", up, cand).strip()
print("git diff --shortstat:", st)
print("commits:", git("rev-list", "--count", f"{up}..{cand}").strip())
sys.exit(1 if bad else 0)
