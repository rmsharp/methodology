#!/usr/bin/env python3
"""How a reader sees `echo`'s output: whole, or in pieces. The reader reads as soon as data is there.
Two payload shapes at four sizes: 61-byte lines, and the same bytes on ONE line. A delivery in several pieces means the
writer had bytes left after the reader was first woken; a reader that quits then leaves the writer to SIGPIPE.
Usage: python3 -B write-pieces.py [N per cell]   (default 400)"""
import collections, os, subprocess, sys, tempfile
N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
tmp = tempfile.mkdtemp()
def run(cmd):
    seqs = collections.Counter()
    for _ in range(N):
        p = subprocess.Popen(["bash", "-c", cmd], stdout=subprocess.PIPE)
        sizes = []
        while True:
            b = os.read(p.stdout.fileno(), 65536)
            if not b: break
            sizes.append(len(b))
        p.wait(); seqs[tuple(sizes)] += 1
    return seqs
for shape in ("lines", "one line"):
    for size in (300, 1000, 2150, 5000):
        path = f"{tmp}/pay{size}.txt"
        open(path, "w").write(("a" * 60 + "\n") * (size // 61) if shape == "lines" else "a" * size)
        for label, cmd in (("substitution", f'echo "$(cat {path})"'), ("variable    ", f'OUT=$(cat {path}); echo "$OUT"')):
            s = run(cmd)
            whole = sum(v for k, v in s.items() if len(k) == 1)
            top = ", ".join(f"{list(k)}x{v}" for k, v in s.most_common(3))
            print(f"{shape:8} {size:5d} B {label}: whole {whole}/{N}; most common deliveries: {top}")
