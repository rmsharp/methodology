"""Scratch: re-derive every frozen docs/archive/*.verify.sh in <repo> under the CURRENT template
(with P2's STUB_PATTERN) and tabulate frozen vs re-derived verdict. Writes nothing under <repo>.

The stub marker is chosen per LEDGER the way the trimmer's own table does: the LIVE basename is
looked up in <trimmer.py>'s LEDGERS; a ledger with no entry, or an entry with no marker, gets ''.
(The adopter's local SESSION_NOTES.md spec is NOT in canonical LEDGERS, so it reads as no marker --
which is what the overlay leaves it with.)

usage: reverify_p2.py <repo> <trimmer.py> <out.tsv>
TSV: shard, frozen-version, frozen-exit, rederived-exit, first FAIL/OK line, NOTE-first-80
"""
import importlib.util
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
repo, trimmer, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])

spec = importlib.util.spec_from_file_location("mtrim_scratch", str(trimmer))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def run(path):
    r = subprocess.run(["bash", str(path)], cwd=str(repo), capture_output=True, text=True)
    lines = (r.stdout + r.stderr).splitlines()
    first = next((l for l in lines if l.startswith("FAIL:")), None) or \
        next((l for l in lines if l.startswith("OK:")), "(no FAIL/OK line)")
    note = next((l for l in lines if l.startswith("NOTE:")), "")
    return r.returncode, first[:150], note[:100]


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
        rows.append((old.name, ver, frc, "-", "grammar lines not found", ""))
        continue
    led = m.LEDGERS.get(Path(live).name)
    stub = repr(led.stub_marker.pattern) if led is not None and led.stub_marker else repr("")
    gen = m.VERIFY_TEMPLATE
    for k, v in (("@@SHARD@@", shard), ("@@LIVE@@", live), ("@@VER@@", m.TRIM_VERSION),
                 ("@@KIND@@", g["KIND"]), ("@@START@@", g["START"]), ("@@INFO@@", g["INFO"]),
                 ("@@FOOTER@@", g["FOOTER"]), ("@@REGEN@@", g["REGEN"]), ("@@STUB@@", stub)):
        gen = gen.replace(k, v)
    assert "@@" not in gen, "an unfilled placeholder is left in the generated proof"
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "reverify.sh"
        p.write_text(gen, encoding="utf-8")
        rrc, first, note = run(p)
    rows.append((old.name, ver, frc, rrc, first, note))

with open(str(out), "w", encoding="utf-8") as fh:
    for r in rows:
        fh.write("\t".join(str(x) for x in r) + "\n")

from collections import Counter
print("proofs=%d  frozen-red=%d  re-derived exit codes: %s" % (
    len(rows), sum(1 for r in rows if r[2] != 0), dict(Counter(r[3] for r in rows))))
newly_red = [r[0] for r in rows if r[2] == 0 and r[3] not in (0, "-")]
print("newly red (frozen exit 0, re-derived nonzero): %d %s" % (len(newly_red), newly_red[:5]))
