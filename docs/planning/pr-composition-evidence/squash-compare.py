#!/usr/bin/env python3
"""Squash-merge check (S400): compare two runs of pr3b-adopters.py, one against `pr2b/candidate` (the control) and one
against `pr2b/squash-check` (upstream/main plus ONE commit holding the candidate's tree, what GitHub's squash button would
make of the 33 commits).

Reads, read-only: squash-control-rows.json, squash-rows.json and S396's pr3b-rows.json (all beside this script); asks git
(read-only, run from the repository root) about the two refs and about which commits of upstream/main..pr2b/candidate carry
each blob the squash newly refuses. Prints the comparison; writes nothing. Python 3 standard library.

    python3 docs/planning/pr-composition-evidence/squash-compare.py > docs/planning/pr-composition-evidence/squash-compare-output.txt

Exit 0 when every expectation that is a hard property (E1, E4, E6 to E10, E12) holds, 1 otherwise. The counts (E3, E5) and the
timing (E13) are printed and judged in the record, not here.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CAND, SQUASH, UP = "pr2b/candidate", "pr2b/squash-check", "upstream/main"


def git(*args):
    r = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


def blobs_at(commits, path):
    """{commit: blob sha of `path` there} for the commits that hold the path."""
    if not commits:
        return {}
    spec = "\n".join("%s:%s" % (c, path) for c in commits) + "\n"
    r = subprocess.run(["git", "-C", str(REPO), "cat-file", "--batch-check"], input=spec, capture_output=True, text=True)
    out = {}
    for c, line in zip(commits, r.stdout.splitlines()):
        p = line.split()
        if len(p) == 3 and p[1] == "blob":
            out[c] = p[0]
    return out


def history(ref, path):
    code, o = git("log", "--format=%H", ref, "--", path)
    return blobs_at(o.split() if code == 0 else [], path)


def load(name):
    return json.loads((HERE / name).read_text())


def rows(data):
    return {r["adopter"]: r for r in data["adopters"]}


failed = []


def check(tag, ok, text):
    print("  %-4s %s  %s" % (tag, "ok  " if ok else "FAIL", text))
    if not ok:
        failed.append(tag)


ctl, sq, base = load("squash-control-rows.json"), load("squash-rows.json"), load("pr3b-rows.json")
C, Q, B = rows(ctl), rows(sq), rows(base)
names = list(C)

print("== 1. the refs (E1)")
ct, st = git("rev-parse", CAND + "^{tree}")[1], git("rev-parse", SQUASH + "^{tree}")[1]
above = git("rev-list", "--count", UP + ".." + SQUASH)[1]
parents = git("rev-list", "--parents", "-n1", SQUASH)[1].split()[1:]
f_sq = set(git("diff", "--name-only", UP, SQUASH)[1].split())
f_c = set(git("diff", "--name-only", UP, CAND)[1].split())
print("  %s %s tree %s" % (CAND, git("rev-parse", CAND)[1][:12], ct[:12]))
print("  %s %s tree %s, parent %s" % (SQUASH, git("rev-parse", SQUASH)[1][:12], st[:12], [p[:12] for p in parents]))
check("E1", ct == st and above == "1" and parents == [git("rev-parse", UP)[1]] and f_sq == f_c and len(f_c) == 47,
      "one commit above %s, same tree as the candidate, %d files each" % (UP, len(f_c)))
print("  rows.json: control candidate %s, squash candidate %s, upstream %s / %s" % (
    ctl["candidate"][:12], sq["candidate"][:12], ctl["upstream"][:12], sq["upstream"][:12]))
print()

print("== 2. per adopter: plain sync exit, files refused, forced sync wrote, seeds changed / created, the sync after it")
print("  %-26s %-9s %-9s %-4s %-4s | %-8s %-8s %-7s | %-6s %-6s | %-9s | %s" % (
    "adopter", "head ctl", "head sq", "ex c", "ex s", "refused c", "refused s", "new", "wrote c", "wrote s", "seeds", "again c/s"))
tot_c = tot_q = 0
new = []  # (adopter, dest, src, blob)
for a in names:
    rc, rq = C[a]["real_C"], Q[a]["real_C"]
    pc, pq = rc.get("plain_refused", []), rq.get("plain_refused", [])
    tot_c += len(pc)
    tot_q += len(pq)
    only_q = [d for d in pq if d not in pc]
    cl = {x["dest"]: x for x in Q[a]["refused_classified"]}
    for d in only_q:
        new.append((a, d, cl[d]["src"], cl[d]["blob"]))
    print("  %-26s %-9s %-9s %-4s %-4s | %-9d %-9d %-7d | %-7d %-7d | %d/%d %d/%d | %s,%s / %s,%s" % (
        a, C[a]["head"][:8], Q[a]["head"][:8], rc.get("plain_exit"), rq.get("plain_exit"), len(pc), len(pq), len(only_q),
        len(rc.get("written", [])), len(rq.get("written", [])),
        len(rc.get("seeds_changed", [])), len(rc.get("seeds_created", [])), len(rq.get("seeds_changed", [])), len(rq.get("seeds_created", [])),
        rc.get("again_exit"), len(rc.get("again_written", [])), rq.get("again_exit"), len(rq.get("again_written", []))))
print("  TOTAL refused: control %d, squash %d, difference %+d" % (tot_c, tot_q, tot_q - tot_c))
print()

print("== 3. the expectations that are properties")
refusing_c = sum(1 for a in names if C[a]["real_C"].get("plain_exit") == 2)
refusing_q = sum(1 for a in names if Q[a]["real_C"].get("plain_exit") == 2)
check("E2", refusing_c == 10, "control: %d of 12 refuse a plain sync (exit 2)" % refusing_c)
base_tot = sum(len(B[a]["real_C"].get("plain_refused", [])) for a in names)
print("  E3   (count) control total %d, S396's total %d; per-adopter refused sets equal S396's at %d of 12" % (
    tot_c, base_tot, sum(1 for a in names if set(C[a]["real_C"].get("plain_refused", [])) == set(B[a]["real_C"].get("plain_refused", [])))))
check("E4", all(set(C[a]["real_C"].get("plain_refused", [])) <= set(Q[a]["real_C"].get("plain_refused", [])) for a in names),
      "the squash's refused set contains the control's at every adopter")
print("  E5   (count) refused: control %d, squash %d" % (tot_c, tot_q))
check("E6", refusing_q == 10 and all((C[a]["real_C"].get("plain_exit") == 2) == (Q[a]["real_C"].get("plain_exit") == 2) for a in names),
      "the same 10 adopters refuse under both runs (%d under squash)" % refusing_q)
check("E7", all(len(C[a]["real_C"].get("written", [])) == len(Q[a]["real_C"].get("written", [])) for a in names),
      "the forced sync writes the same number of files at every adopter")
check("E8", all(not C[a]["real_C"].get("seeds_changed") and not Q[a]["real_C"].get("seeds_changed") for a in names),
      "seeds changed: 0 at 12 of 12, both runs")
check("E9", all(C[a]["real_C"].get("again_exit") == 0 and not C[a]["real_C"].get("again_written")
                and Q[a]["real_C"].get("again_exit") == 0 and not Q[a]["real_C"].get("again_written") for a in names),
      "the plain sync after the forced one exits 0 and writes 0 at 12 of 12, both runs")
check("E10", all(C[a]["audit_refusal_equals_rule"] and Q[a]["audit_refusal_equals_rule"] for a in names),
      "the refusal list equals the history rule at 12 of 12, both runs")


def u_key(r):
    u = r["real_U"]
    return (u.get("exit"), u.get("written"), u.get("seeds_created"), u.get("seeds_changed"), u.get("again_exit"), u.get("again_written"))


moved = [a for a in names if C[a]["head"] != Q[a]["head"]]
same_u = [a for a in names if u_key(C[a]) == u_key(Q[a])]
print("  E11  upstream's tool: identical result in the two runs at %d of 12 adopters; HEAD moved between the runs at: %s" % (
    len(same_u), ", ".join(moved) or "none"))
print("       (E11 is a count of agreement, judged in the record; the HEAD moves above are checked in section 5)")
fa, fb = ctl["fixtures"], sq["fixtures"]
check("E12", all(fa[k].get("same_paths") == fb[k].get("same_paths") and fa[k].get("only_C") == fb[k].get("only_C")
                 and fa[k].get("only_U") == fb[k].get("only_U") and fa[k].get("unexplained") == fb[k].get("unexplained")
                 and fa[k].get("content_differs") == fb[k].get("content_differs") for k in ("a", "b")),
      "fixtures (a) and (b): same paths, same only-candidate / only-upstream sets, same unexplained, same content_differs")
print()

print("== 4. the files the squash refuses and the merge does not: where each blob lives in the 33 commits")
groups = {}
for a, dest, src, blob in new:
    groups.setdefault((dest, src, blob), []).append(a)
inter = git("rev-list", "--reverse", UP + ".." + CAND)[1].split()
print("  %d newly refused file(s), %d distinct (file, blob) pair(s)" % (len(new), len(groups)))
for (dest, src, blob), ads in sorted(groups.items()):
    cand_blobs = history(CAND, src)
    sq_blobs = history(SQUASH, src)
    up_blobs = history(UP, src)
    carried = [c for c in inter if cand_blobs.get(c) == blob]
    final = git("rev-parse", CAND + ":" + src)[1]
    print("  %s  blob %s  at %d adopter(s): %s" % (dest, blob[:10], len(ads), ", ".join(ads)))
    print("      in %s history of %s: %s; in %s: %s; the candidate's final blob: %s" % (
        UP, src, blob in up_blobs.values(), SQUASH, blob in sq_blobs.values(), "yes" if blob == final else "no"))
    print("      carried by %d of the 33 commits: %s" % (len(carried), " ".join(c[:9] for c in carried[:6]) + (" ..." if len(carried) > 6 else "")))
    for c in carried[:1]:
        print("      first: %s" % git("log", "-1", "--format=%h %s", c)[1][:150])
    if not (blob not in up_blobs.values() and blob not in sq_blobs.values() and carried):
        check("E4x", False, "%s: the blob is not an intermediate-only blob of the 33 commits" % dest)
print()

print("== 5. a HEAD that moved between the runs: the framework files it holds are the same at both heads")
for a in moved:
    repo = str(Path.home() / "Development" / a)
    r = subprocess.run(["git", "-C", repo, "diff", "--stat", C[a]["head"], Q[a]["head"], "--", "methodology", ".githooks", "bin"],
                       capture_output=True, text=True)
    n = subprocess.run(["git", "-C", repo, "rev-list", "--count", "%s..%s" % (C[a]["head"], Q[a]["head"])], capture_output=True, text=True)
    print("  %s: %s commit(s) between %s and %s; changed paths under methodology/, .githooks/, bin/: %s" % (
        a, n.stdout.strip(), C[a]["head"][:8], Q[a]["head"][:8], "none" if not r.stdout.strip() else r.stdout.strip().splitlines()[-1]))
    check("E11x", not r.stdout.strip(), "%s: no framework file differs between its two cloned heads" % a)
print()
print("RESULT: %s" % ("every property holds" if not failed else "FAILED: " + ", ".join(failed)))
sys.exit(1 if failed else 0)
