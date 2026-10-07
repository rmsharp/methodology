#!/usr/bin/env bash
# BL-101 P6 runtime check, on REAL data: bin/sync, bin/status and bin/check-links at this commit (NEW) against the
# same three tools at OLD_REV, the last commit before P6 changed a tool, in three parts. Nothing is written to a real
# repository: every part works in `--no-local` clones, which hold the COMMITTED state only (a live tree is a moving
# target, which S278 measured). Each adopter is cloned ONCE and the moved tree is a clone of that clone.
#
#   A  legacy regression   every adopter under the portfolio root that keeps its methodology files at its root:
#                          status, `sync --dry-run` and `check-links --tree` by the OLD and the NEW tool must print
#                          the same thing (once the lines P6 adds are set aside: `layout:` lines, and the version
#                          and source lines that name the two canonical checkouts), exit alike, and write nothing.
#   B  adopters that moved a few real adopters are cloned and their methodology files `git mv`ed to the places the
#                          manifest's NEW_LAYOUT gives, as bin/migrate-layout (P7) will. The OLD tool on the legacy
#                          clone and the NEW tool on the moved clone must agree row by row on every file's state,
#                          the dry run must agree on every file's action, and a real run on the moved clone must
#                          create nothing at its root: no second runner, no blank seed beside a real ledger (C1).
#   C  the plan's 5A.3     a scratch portfolio of a legacy, a migrated, a half-migrated and an empty project: the dry
#                          runs write nothing, the half-migrated one is refused, the real runs write exactly the
#                          expected files; and --source=github against a local repository whose manifest carries
#                          the new table exits 0 (C16).
#
# Run from the repo root:   bash docs/planning/methodology-subdirectory-evidence/sync-in-both-layouts.sh
set -u
SRC="$(git rev-parse --show-toplevel)" || exit 3
PORT="$(dirname "$SRC")"
OLD_REV="${OLD_REV:-7f7f74f}"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
git clone -q --no-local "$SRC" "$T/new" || exit 3
git clone -q --no-local "$SRC" "$T/old" || exit 3
git -C "$T/old" -c advice.detachedHead=false checkout -q "$OLD_REV" || exit 3
printf 'commit under test: %s   old tools: %s\n\n' "$(git -C "$SRC" rev-parse --short HEAD)" "$OLD_REV"

python3 -B - "$SRC" "$PORT" "$T" <<'PYEOF'
import os, re, subprocess, sys
from pathlib import Path

sys.dont_write_bytecode = True
src, port, t = (Path(a) for a in sys.argv[1:4])
OLD, NEW = t / "old", t / "new"
sys.path.insert(0, str(NEW / "bin"))
import _manifest as manifest   # the table under test, read from the clone of the commit under test
bad = 0


def run(canon, tool, *args, env=None):
    e = dict(os.environ)
    e.pop("METHODOLOGY_SOURCE_URL", None)
    e.update(env or {})
    r = subprocess.run([sys.executable, "-B", str(canon / "bin" / tool), *map(str, args)], capture_output=True, text=True, env=e)
    return r.returncode, r.stdout + r.stderr


def git(path, *a):
    return subprocess.run(["git", "-C", str(path), *a], capture_output=True, text=True, check=True).stdout


def clone(origin, dest):
    subprocess.run(["git", "clone", "-q", "--no-local", str(origin), str(dest)], check=True)
    for k, v in (("user.email", "t@t"), ("user.name", "t"), ("commit.gpgsign", "false")):
        git(dest, "config", k, v)


def tree(p):
    return sorted(str(f.relative_to(p)) for f in Path(p).rglob("*") if f.is_file() and ".git" not in f.relative_to(p).parts)


def norm(text, canon):
    """Set aside what P6 adds (the layout lines) and what names the two canonical checkouts."""
    out = []
    for line in text.replace(str(canon), "<canon>").splitlines():
        if line.startswith(("layout: ", "  layout:  ", "  version: ")):
            continue
        out.append(line)
    return "\n".join(out)


# ---- A ------------------------------------------------------------------------------------------------
print("== A. a project that has not moved is read and synced as it was ==")
adopters = sorted(p for p in port.iterdir() if (p / ".git").exists() and (p / "SESSION_RUNNER.md").is_file())
same = {"status": 0, "sync --dry-run": 0, "check-links --tree": 0}
snaps = {}
for p in adopters:
    snap = t / ("snap-" + p.name)
    clone(p, snap)
    snaps[p.name] = snap
    before = tree(snap)
    row = []
    for label, tool, args in (("status", "status", (snap,)), ("sync --dry-run", "sync", (snap, "--dry-run")),
                              ("check-links --tree", "check-links", ("--tree", snap))):
        (orc, oout), (nrc, nout) = run(OLD, tool, *args), run(NEW, tool, *args)
        ok = orc == nrc and norm(oout, OLD) == norm(nout, NEW)
        same[label] += ok
        bad += not ok
        row.append("%s %s" % (label, "=" if ok else "DIFFERS (exit %d vs %d)" % (orc, nrc)))
        if not ok:
            a, b = norm(oout, OLD).splitlines(), norm(nout, NEW).splitlines()
            for x, y in zip(a, b):
                if x != y:
                    print("        first difference:\n          old: %s\n          new: %s" % (x, y))
                    break
    clean = tree(snap) == before and git(snap, "status", "--porcelain") == ""
    bad += not clean
    print("   %-28s %s   wrote nothing: %s" % (p.name, "; ".join(row), "yes" if clean else "NO"))
print("   identical, of %d adopters: %s\n" % (len(adopters), ", ".join("%s %d" % kv for kv in same.items())))

# ---- B ------------------------------------------------------------------------------------------------
print("== B. the same adopters, cloned and moved to the manifest's new destinations ==")
want = ["model_project_constructor", "nprcgenekeepr", "mts-system", "vscode_quarto_ext", "Philippians"]
for name in want:
    if name not in snaps:
        print("   %-28s not present here, skipped" % name)
        continue
    legacy = snaps[name]
    moved = t / (name + "-moved")
    clone(legacy, moved)
    for src_, dest, _disp in manifest.DISTRIBUTION:
        if (moved / dest).is_file():
            target = moved / manifest.NEW_LAYOUT[src_]
            target.parent.mkdir(parents=True, exist_ok=True)
            git(moved, "mv", dest, manifest.NEW_LAYOUT[src_])
    git(moved, "-c", "core.hooksPath=/dev/null", "commit", "-q", "--allow-empty", "-m", "move the methodology files under methodology/")
    to_new = {dest: manifest.NEW_LAYOUT[s] for s, dest, _d in manifest.DISTRIBUTION}

    def states(out):
        rows = {}
        for line in out.splitlines():
            parts = line.split(None, 3)
            if len(parts) == 4 and parts[2] in ("tracked", "seed"):
                rows[parts[1]] = parts[3].strip()
        return rows
    _, oout = run(OLD, "status", legacy)
    nrc, nout = run(NEW, "status", moved)
    o, n = states(oout), states(nout)
    status_ok = ("layout: %s  new" % moved.name) in nout and {to_new.get(k, k): v for k, v in o.items()} == n
    # the dry run: every file's action, set against the legacy clone's
    def actions(out):
        return {line.split(":")[0].strip(): line.split(":", 1)[1].strip()
                for line in out.split("  files:")[-1].splitlines() if ": " in line and not line.strip().startswith(".gitignore")}
    _, odry = run(OLD, "sync", legacy, "--dry-run")
    drc, ndry = run(NEW, "sync", moved, "--dry-run")
    def blocked(out):   # a refused run (exit 2) has no files section: it lists the files that differ, one per line
        return {l.strip() for l in out.splitlines() if re.fullmatch(r"    \S+", l)}
    orc_, _ = run(OLD, "sync", legacy, "--dry-run")
    oa, na = actions(odry), actions(ndry)
    if drc == 2:   # both tools refuse alike: the same exit, naming the same files at their own places
        dry_ok = orc_ == 2 and {to_new.get(k, k) for k in blocked(odry)} == blocked(ndry) and bool(blocked(ndry))
        na = blocked(ndry)
    else:
        dry_ok = orc_ == drc and "  layout:  new (found " in ndry and {to_new.get(k, k): v for k, v in oa.items()} == na
    # a real run on the moved clone: whatever it creates is under methodology/, never at the root or in docs/methodology
    before_all = set(tree(moved))
    rrc, rout = run(NEW, "sync", moved)
    created = set(tree(moved)) - before_all
    root_ok = all(f.startswith("methodology/") for f in created)
    ok = status_ok and dry_ok and root_ok and rrc in (0, 2)
    bad += not ok
    print("   %-28s status rows equal (%d): %s   dry run %s (%d): %s   real run (exit %d) created %s, none outside methodology/: %s" % (
        name, len(n), "yes" if status_ok else "NO", "refused alike, same files" if drc == 2 else "actions equal", len(na),
        "yes" if dry_ok else "NO", rrc, ", ".join(sorted(created)) or "nothing", "yes" if root_ok else "NO"))
print()

# ---- C ------------------------------------------------------------------------------------------------
print("== C. a scratch portfolio: legacy, migrated, half-migrated, empty (plan 5A.3) ==")
port_dir = t / "portfolio"
port_dir.mkdir()
legacy, migrated, half, empty = (port_dir / n for n in ("legacy", "migrated", "half", "empty"))
for d in (legacy, migrated, half, empty):
    d.mkdir()
    git(d, "init", "-q")
assert run(NEW, "sync", legacy)[0] == 0
assert run(NEW, "sync", migrated, "--layout", "new")[0] == 0
assert run(NEW, "sync", half)[0] == 0
(half / "methodology").mkdir()
(half / "methodology" / "SESSION_RUNNER.md").write_text("x\n", encoding="utf-8")
L, N = {d for _s, d, _x in manifest.DISTRIBUTION}, set(manifest.NEW_LAYOUT.values())
checks = []
rc, out = run(NEW, "status", legacy, migrated, half, empty)
lines = [l for l in out.splitlines() if l.startswith("layout: ")]
checks.append(("status over the portfolio names each layout: " + "; ".join(l[len("layout: "):].split(" (")[0] for l in lines),
               [l.split()[2] for l in lines] == ["legacy", "new", "half-migrated:", "none"]))
for proj, expect_rc, want_layout in ((legacy, 0, "legacy"), (migrated, 0, "new"), (half, 2, None), (empty, 0, "legacy")):
    before = tree(proj)
    rc, out = run(NEW, "sync", proj, "--dry-run")
    ok = rc == expect_rc and tree(proj) == before and (want_layout is None or ("  layout:  %s" % want_layout) in out)
    checks.append(("dry run of %s: exit %d, writes nothing%s" % (proj.name, rc, "" if want_layout else ", refused"), ok))
rc, out = run(NEW, "sync", empty)
checks.append(("real run on the empty project writes the legacy tree and no methodology/ directory", rc == 0 and set(tree(empty)) == L))
checks.append(("the migrated project holds exactly the table's destinations and no root runner",
               set(tree(migrated)) == N and not (migrated / "SESSION_RUNNER.md").exists()))
rc, out = run(NEW, "sync", migrated)
checks.append(("a second run on the migrated project changes nothing and stays new", rc == 0 and set(tree(migrated)) == N and "layout:  new" in out))
rc, out = run(NEW, "sync", half)
checks.append(("the half-migrated project is refused, naming both paths, and nothing is written",
               rc == 2 and str(half / "methodology" / "SESSION_RUNNER.md") in out and str(half / "SESSION_RUNNER.md") in out))
rc, out = run(NEW, "sync", legacy, "--layout", "new")
checks.append(("a legacy project asked for the new layout is refused (no second runner)", rc == 2 and not (legacy / "methodology").exists()))
bare = t / "source.git"
subprocess.run(["git", "clone", "-q", "--bare", str(NEW), str(bare)], check=True)
fresh = port_dir / "from-github"
fresh.mkdir()
git(fresh, "init", "-q")
rc, out = run(NEW, "sync", fresh, "--source=github", "--layout", "new", env={"METHODOLOGY_SOURCE_URL": "file://" + str(bare)})
checks.append(("--source=github against a local repository whose manifest carries the table: exit 0, the new tree", rc == 0 and set(tree(fresh)) == N))
for label, ok in checks:
    bad += not ok
    print("   [%s] %s" % ("ok" if ok else "FAIL", label))

rc, out = run(NEW, "check-links", "--layout", "new")
m = re.search(r"(\d+) dangling link", out)
total = re.search(r"(\d+) relative link", run(NEW, "check-links")[1])
print("\n   for P9: check-links --layout new reports %s dangling link(s) of %s in the simulated new layout (exit %d)" % (
    m.group(1) if m else "?", total.group(1) if total else "?", rc))
print("\n%s" % ("ALL CHECKS HELD" if not bad else "%d CHECK(S) FAILED" % bad))
sys.exit(1 if bad else 0)
PYEOF
