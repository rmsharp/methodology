"""SCRATCH EVIDENCE for docs/planning/issue93-trimmer-proof-false-red-plan.md: what would `--reverify` say?
Not the plan's implementation; nothing here is wired into the trimmer.

For each frozen docs/archive/*.verify.sh in <repo>, take the LIVE and SHARD it names, regenerate the
proof text IN MEMORY from <trimmer.py>'s CURRENT template (build_verify), write it to a temp file
OUTSIDE the repo, run it with cwd=<repo>, and tabulate its verdict beside the frozen script's own.
Nothing under <repo> is written. With --exact-leak the cause-2 fix is applied to the generated text.

usage: proto_reverify.py <repo> <trimmer.py> <out.tsv> [--exact-leak]
TSV: shard, frozen-version, frozen-exit, reverify-exit, reverify first FAIL/OK line, NOTE?(Y/N)
"""
import importlib.util
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
repo, trimmer, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
exact = "--exact-leak" in sys.argv[4:]

spec = importlib.util.spec_from_file_location("mtrim_scratch", str(trimmer))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

OLD = 'leaked = [ln for ln in bfront.splitlines()\n          if ln.strip() and len(ln.strip()) > 24 and (ln in sfront or ln in "".join(sr))]'
NEW = ('sr_lines = set("".join(sr).splitlines()); sfront_lines = set(sfront.splitlines())\n'
       'leaked = [ln for ln in bfront.splitlines()\n'
       '          if ln.strip() and len(ln.strip()) > 24 and (ln in sfront_lines or ln in sr_lines)]')


def run(script_path):
    r = subprocess.run(["bash", str(script_path)], cwd=str(repo), capture_output=True, text=True)
    lines = (r.stdout + r.stderr).splitlines()
    first = next((l for l in lines if l.startswith("FAIL:")), None) or \
        next((l for l in lines if l.startswith("OK:")), "(no FAIL/OK line)")
    note = "Y" if any(l.startswith("NOTE:") for l in lines) else "N"
    return r.returncode, first[:110], note


rows = []
for old in sorted((repo / "docs" / "archive").glob("*.verify.sh")):
    txt = old.read_text(encoding="utf-8")
    ver = (re.search(r"methodology_trim\.py v([0-9.]*[0-9])", txt) or [None, "?"])[1]
    live = (re.search(r"^LIVE=(\S+)", txt, re.M) or [None, ""])[1]
    shard = (re.search(r"^SHARD=(\S+)", txt, re.M) or [None, ""])[1]
    frc, _f, _n = run(old)
    g = {}
    for key, rx in (("KIND", r'^RECORD_KIND = "(.*)"$'), ("START", r'^RECORD_START = r"(.*)"$'),
                    ("INFO", r'^FENCE_INFO = "(.*)"$'), ("FOOTER", r'^FOOTER_MODE = "(.*)"$'),
                    ("REGEN", r'^REGEN_PATTERNS = (.*)$')):
        mm = re.search(rx, txt, re.M)
        g[key] = mm.group(1) if mm else ("[]" if key == "REGEN" else None)
    if not live or not shard or any(v is None for v in g.values()):
        rows.append((old.name, ver, frc, "-", "grammar lines not found in the frozen script", "-"))
        continue
    gen = m.VERIFY_TEMPLATE
    for k, v in (("@@SHARD@@", shard), ("@@LIVE@@", live), ("@@VER@@", m.TRIM_VERSION),
                 ("@@KIND@@", g["KIND"]), ("@@START@@", g["START"]), ("@@INFO@@", g["INFO"]),
                 ("@@FOOTER@@", g["FOOTER"]), ("@@REGEN@@", g["REGEN"])):
        gen = gen.replace(k, v)
    if exact:
        assert OLD in gen, "leaked line not found in the current template"
        gen = gen.replace(OLD, NEW, 1)
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "reverify.sh"
        p.write_text(gen, encoding="utf-8")
        rrc, first, note = run(p)
    rows.append((old.name, ver, frc, rrc, first, note))

with open(str(out), "w", encoding="utf-8") as fh:
    for r in rows:
        fh.write("\t".join(str(x) for x in r) + "\n")
print("scripts=%d  frozen-red=%d  reverify-red=%d%s" % (
    len(rows), sum(1 for r in rows if r[2] != 0),
    sum(1 for r in rows if r[3] not in (0, "-")), "  (exact-leak patch applied)" if exact else ""))
