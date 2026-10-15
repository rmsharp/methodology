#!/usr/bin/env python3
"""The reduction commit's edits (BL-113 option (a), S325): the runner's layout paragraph loses its duplicate example
command, and the runner's row in the budget config records the re-measured density.

Run in a clone of pr2/candidate checked out at 28f99a7:  python3 -I bl113-build.py REPO

It refuses, writing nothing, if the runner is not the blob the meter measured (3d09a4a8), if an anchor is not found exactly
once, or if the runner it produces is not the blob the meter measured for the cut (07ef7250). It then writes the two files.
It does not commit; the commit message is bl113-message.txt. Generates no bytecode.

The figures in the config sentence are the meter's (bl113-meter-output.txt): the doubled read of each blob, halved.
"""
import json
import subprocess
import sys

sys.dont_write_bytecode = True

REPO = sys.argv[1]
RUNNER, CONFIG = "starter-kit/SESSION_RUNNER.md", ".context-budget.json"
BEFORE_BLOB = "3d09a4a81aa3e95ea20cbfac94c3f7c165c77d94"   # the candidate's runner, 53,184 B
AFTER_BLOB = "07ef7250dca07221bdf52113fbeffd4cd38d13ae"    # the runner with the example dropped, 53,100 B

EXAMPLE = " (`python3 methodology/methodology_trim.py --file methodology/CHANGELOG.md --check`)"
DENSITY_OLD = '"bytes_per_token": 2.8107,\n      "measured_bytes": 52839,'
DENSITY_NEW = '"bytes_per_token": 2.8130,\n      "measured_bytes": 53100,'
NOTE_END = 'so measure, never extrapolate."'
NOTE_ADD = (' RE-MEASURED 2026-10-15 (the layout paragraph\'s duplicate example command dropped, '
            'which FRAMEWORK_APPARATUS.md already carries): the control, blob 71ad950f at 52,839 B, '
            'reproduced 37,599 doubled; the runner before the cut, 53,184 B, read 37,823 doubled, so 18,911.5 tokens '
            '(2.8123 B/token) where the tool at 2.8107 said 18,921; the runner after it, 53,100 B, reads 37,753 doubled, '
            'so 18,876.5 tokens at 2.8130 B/token, 23.5 under the ceiling.')


def git(*a, stdin=None):
    r = subprocess.run(["git", "-C", REPO, *a], input=stdin, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("refused: git %s: %s" % (" ".join(a), r.stderr.strip()))
    return r.stdout.strip()


def once(text, old, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit("refused: %s found %d times (expected 1)" % (label, n))


def blob_of(text):
    return git("hash-object", "--stdin", stdin=text)


def read(rel):
    with open("%s/%s" % (REPO, rel), encoding="utf-8", newline="") as f:
        return f.read()


runner, config = read(RUNNER), read(CONFIG)
if blob_of(runner) != BEFORE_BLOB:
    raise SystemExit("refused: %s is not the blob the meter measured (%s)" % (RUNNER, BEFORE_BLOB[:8]))
once(runner, EXAMPLE, "the example command")
once(config, DENSITY_OLD, "the runner row's density and size")
once(config, NOTE_END, "the end of the runner row's note")

new_runner = runner.replace(EXAMPLE, "")
if blob_of(new_runner) != AFTER_BLOB:
    raise SystemExit("refused: the cut runner is not the blob the meter measured (%s)" % AFTER_BLOB[:8])
new_config = config.replace(DENSITY_OLD, DENSITY_NEW).replace(NOTE_END, NOTE_END[:-1] + NOTE_ADD + '"')
json.loads(new_config)   # still valid JSON

for rel, text in ((RUNNER, new_runner), (CONFIG, new_config)):
    with open("%s/%s" % (REPO, rel), "w", encoding="utf-8", newline="") as f:
        f.write(text)
print("wrote %s (%d B -> %d B) and %s (%d B -> %d B)" % (
    RUNNER, len(runner.encode()), len(new_runner.encode()), CONFIG, len(config.encode()), len(new_config.encode())))
