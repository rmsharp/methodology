#!/usr/bin/env python3
"""P15, register row F7: match an adopter's locally modified synced file against this repository's history.

    python3 -I p15-f7-match.py <canonical checkout> <adopter checkout> <file name>

Reads every revision of <file name> reachable in the canonical checkout (both the default walk and --full-history, under
starter-kit/, the root and methodology/), de-duplicates identical blobs, and prints the five closest by difflib ratio plus the
line diff of the nearest against the adopter's file. Read-only."""
import difflib, subprocess, sys

M, A, rel = sys.argv[1:4]


def git(*a):
    return subprocess.run(["git", *a], cwd=M, capture_output=True, text=True, check=False)


mine = open(f"{A}/{rel}", encoding="utf-8").read().splitlines()
seen = {}
for p in (f"starter-kit/{rel}", rel, f"methodology/{rel}"):
    for walk in (["--full-history"], []):
        for h in git("log", "--all", *walk, "--format=%H", "--", p).stdout.split():
            seen.setdefault((h, p), 1)
blobs = {}
for h, p in seen:
    b = git("show", f"{h}:{p}")
    if b.returncode == 0 and b.stdout not in blobs:
        blobs[b.stdout] = (h, p)
res = sorted(((difflib.SequenceMatcher(None, t.splitlines(), mine, autojunk=False).ratio(), h, p, len(t.splitlines()))
              for t, (h, p) in blobs.items()), reverse=True)
print(f"adopter lines: {len(mine)}  distinct canonical blobs examined: {len(res)}")
for r in res[:5]:
    print(f"ratio={r[0]:.5f} {r[1][:9]} {r[2]} lines={r[3]}")
best = res[0]
bl = [t for t, v in blobs.items() if v[0] == best[1]][0].splitlines()
diff = list(difflib.unified_diff(bl, mine, "canonical@" + best[1][:9], "adopter", lineterm="", n=0))
add = sum(1 for x in diff if x.startswith("+") and not x.startswith("+++"))
rem = sum(1 for x in diff if x.startswith("-") and not x.startswith("---"))
print(f"nearest {best[1][:9]}: +{add} -{rem} against the adopter's file")
print("\n".join(diff))
