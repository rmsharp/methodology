#!/usr/bin/env python3
"""BL-101 F24 (S299): run `tools/test_migrate_layout.py`'s VSCE_ORACLE table through the real minimatch, the call vsce makes
(`minimatch(path, pattern, { dot: true })`, `@vscode/vsce` `out/package.js` `collectFiles`), and print every row where the
table and minimatch differ. Exit 0 when none does.

Usage: f24-oracle.py <directory holding node_modules/minimatch>   (the adopter's own checkout was used: minimatch 10.2.5,
the version `@vscode/vsce` 3.9.2 requires, `"minimatch": "^10.2.2"`). Needs node; reads the table, writes nothing."""
import importlib.util
import json
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = __file__.rsplit("/", 1)[0]
spec = importlib.util.spec_from_file_location("t", HERE + "/../../../tools/test_migrate_layout.py")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
table = t.TestThePureRules.VSCE_ORACLE

js = """
const {minimatch} = require(process.argv[1] + '/node_modules/minimatch');
const rows = JSON.parse(require('fs').readFileSync(0, 'utf8'));
console.log(JSON.stringify(rows.map(([p, f]) => minimatch(f, p, {dot: true}))));
"""
r = subprocess.run(["node", "-e", js, sys.argv[1]], input=json.dumps([[p, f] for p, f, _w in table]), capture_output=True, text=True)
if r.returncode:
    sys.exit("node failed: " + r.stderr)
got = json.loads(r.stdout)
version = json.load(open(sys.argv[1] + "/node_modules/minimatch/package.json"))["version"]
bad = [(row, g) for row, g in zip(table, got) if row[2] is not g]
print("minimatch %s, { dot: true }: %d rows, %d differ" % (version, len(table), len(bad)))
for (p, f, w), g in bad:
    print("  DIFFERS  %r against %r: table %s, minimatch %s" % (p, f, w, g))
sys.exit(1 if bad else 0)
