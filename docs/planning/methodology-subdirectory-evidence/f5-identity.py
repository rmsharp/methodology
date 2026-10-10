#!/usr/bin/env python3
"""BL-101 F5 verification (S289): the scan did not change, only its sorting. For each clone that f5-population.py left, run the
tool as it was before F5 (a revision, default fb71d55~1) and as it is now, and compare: `ledger`, `harness`, `ci` and `hooks`
must be identical, and the old `other` must equal `tests + proofs + scripts + config + other` in mentions and in files.
Read-only on the clones (a dry run writes nothing). Usage: python3 -I f5-identity.py <the directory f5-population.py wrote> [REV]
Exit 0 when every clone is identical, 1 when one differs."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
pop = Path(sys.argv[1]) / "clones"
rev = sys.argv[2] if len(sys.argv) > 2 else "fb71d55~1"
SPLIT = ("tests", "proofs", "scripts", "config", "other")

old_home = Path(tempfile.mkdtemp(prefix="f5-oldtool-"))
(old_home / "bin").mkdir()
old = subprocess.run(["git", "-C", str(REPO), "show", rev + ":bin/migrate-layout"], capture_output=True, text=True, check=True).stdout
(old_home / "bin" / "migrate-layout").write_text(old, encoding="utf-8")
for name in ("_manifest.py", "_manifest_reader.py", "status", "sync", "check-links", "check-ledger", "check-handoff"):
    if (REPO / "bin" / name).exists():
        (old_home / "bin" / name).symlink_to(REPO / "bin" / name)
for name in ("starter-kit", "tools", "docs"):
    (old_home / name).symlink_to(REPO / name)


def report(tool, clone):
    r = subprocess.run([sys.executable, "-B", str(tool), str(clone), "--json"], capture_output=True, text=True)
    return json.loads(r.stdout)


bad = 0
for clone in sorted(pop.iterdir()):
    o, n = report(old_home / "bin" / "migrate-layout", clone), report(REPO / "bin" / "migrate-layout", clone)
    if o["status"] == "refused" or n["status"] == "refused":
        print("%-26s refused (old %s, new %s)" % (clone.name, o["status"], n["status"]))
        continue
    o, n = o["not_rewritten"], n["not_rewritten"]
    same = all((o[c]["mentions"], o[c]["files"]) == (n[c]["mentions"], n[c]["files"]) for c in ("ledger", "harness", "ci", "hooks"))
    split = (sum(n[k]["mentions"] for k in SPLIT), sum(n[k]["files"] for k in SPLIT))
    ok = same and split == (o["other"]["mentions"], o["other"]["files"])
    bad += not ok
    print("%-26s old other=%s  new %s=%s  ledger/harness/ci/hooks same=%s  %s" % (
        clone.name, (o["other"]["mentions"], o["other"]["files"]), "+".join(SPLIT), split, same, "IDENTICAL" if ok else "DIFFERENT"))
print("clones that differ: %d" % bad)
sys.exit(1 if bad else 0)
