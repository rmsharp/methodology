"""Re-derive the 54 proofs of the #93 repository with a given trimmer and compare each exit code to the
reference column of the saved sweep. Usage: python3 -I sweep54.py <clone at 82433662> <trimmer> <tsv> <column>"""
import csv, subprocess, sys
clone, trimmer, tsv, col = sys.argv[1:5]
rows = list(csv.DictReader(open(tsv), delimiter="\t"))
same = diff = 0; counts = {}
for r in rows:
    p = subprocess.run([sys.executable, "-I", trimmer, "--reverify", r["shard"]], cwd=clone,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    counts[p.returncode] = counts.get(p.returncode, 0) + 1
    if str(p.returncode) == r[col]:
        same += 1
    else:
        diff += 1; print("DIFFERS", r["shard"], "now", p.returncode, "saved", r[col])
print("shards: %d | same as saved column '%s': %d | differ: %d | exit counts now: %s"
      % (len(rows), col, same, diff, dict(sorted(counts.items()))))
