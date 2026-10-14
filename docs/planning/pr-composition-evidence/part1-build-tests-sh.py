#!/usr/bin/env python3
"""S311: build Part 1's bin/tests.sh = upstream/main's file, with the fork's (c8b9ddd) version of the blocks
named in TAKE, and two fork-only blocks appended: BOOTSTRAP's never-overwrite row pinned to the manifest
(fork Test 28, here Test 35) and the early-exiting-consumer lint (fork Test 45, here Test 36).
Usage: python3 part1-build-tests-sh.py <upstream-rev> <fork-rev> <out>   (inside a repository holding both). Reads git only."""
import re, subprocess, sys
UP, FORK, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
def show(rev): return subprocess.run(['git','show',f'{rev}:bin/tests.sh'],capture_output=True,text=True,check=True).stdout
def split(text):
    out=[]; cur=None
    for l in text.split('\n'):
        m=re.match(r'echo "== (Test[^"]*?) =="',l)
        if m or l.startswith('echo "== Summary'):
            cur=[m.group(1) if m else 'Summary',[]]; out.append(cur)
        elif cur is None:
            cur=['PREAMBLE',[]]; out.append(cur)
        cur[1].append(l)
    return out
def num(n):
    m=re.match(r'Test (\d+):',n); return int(m.group(1)) if m else None
U=split(show(UP)); F=split(show(FORK))
# by number AND title stem, since the fork renumbered: 1, 9, 15, 16, 20 keep their numbers in both trees.
TAKE={'PREAMBLE','Summary',1,9,15,16,20}
fork_by={ (n if n in('PREAMBLE','Summary') else num(n)):b for n,b in F}
new=[]
for n,b in U:
    key = n if n in ('PREAMBLE','Summary') else num(n)
    if key in TAKE:
        assert key in fork_by, key
        new.append((n,fork_by[key]))
    else:
        new.append((n,b))
# two fork-only blocks go in before the Summary, under the next free numbers after upstream's last (34)
def fork_block(prefix):
    b=[b for n,b in F if n.startswith(prefix)]; assert len(b)==1, prefix
    return list(b[0])
si=next(i for i,(n,b) in enumerate(new) if n=='Summary')
b35=fork_block('Test 28:'); b35[0]=b35[0].replace('Test 28:','Test 35:',1)
b36=fork_block('Test 45:'); b36[0]=b36[0].replace('Test 45:','Test 36:',1)
# fork Test 45 names a sibling lint this candidate does not carry, and ends with a note about the fork's numbering
assert sum(l.startswith('# "pipeline failed, so pass" -- a real defect reads green and nothing anywhere goes red. Test 42') for l in b36)==1
b36=[l.replace('goes red. Test 42','goes red. A sibling lint (not carried here)') if l.startswith('# "pipeline failed, so pass"') else l for l in b36]
nxt=[i for i,l in enumerate(b36) if l.startswith('# (BL-43) derives only the producers')]
assert len(nxt)==1; b36[nxt[0]]=b36[nxt[0]].replace('# (BL-43) derives','# derives',1)
while b36 and b36[-1].startswith("# upstream's Tests 27-34"): b36.pop()
while b36 and b36[-1]=='': b36.pop()
b36.append('')
new[si:si]=[('Test 35: BOOTSTRAP',b35),('Test 36: lint',b36)]
open(OUT,'w',encoding='utf-8').write('\n'.join('\n'.join(b) for n,b in new))
print("blocks:",len(new))
