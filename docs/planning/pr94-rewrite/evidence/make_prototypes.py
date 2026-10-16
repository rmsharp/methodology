#!/usr/bin/env python3
"""Make the two scratch prototypes of the PR's trimmer that S334 swept the 54 proofs with.

Nothing in the repository is changed: the prototypes are written to OUT_DIR and are meant to be thrown away.

usage: make_prototypes.py PR_TRIMMER OUT_DIR
  PR_TRIMMER  starter-kit/methodology_trim.py as it is on the PR branch
              (git show 972eb2c:starter-kit/methodology_trim.py > trim_pr94.py)
  OUT_DIR     receives trim_protoA.py and trim_protoAB.py

A   stub_pattern_for() returns a stub marker for SESSION_NOTES.md: the runner's Phase 1B line
    "**Status:** Session claimed", matched as a prefix (four of the seven stubs have text appended
    to that line, so an end-anchored marker caught only three of the seven shards).
B   on top of A: a recognised stub finalize exits 0 instead of 4. This reverses decision D2 of
    docs/planning/issue93-trimmer-proof-false-red-plan.md section 9.

Result on the #93 repository's 54 proofs (sweep_after.sh): A gives 46 at exit 0 and 8 at exit 4;
A+B gives 54 at exit 0.
"""
import sys
from pathlib import Path

A_OLD = '''    spec = LEDGERS.get(Path(live_rel).name)
    return spec.stub_marker.pattern if spec is not None and spec.stub_marker else ""'''
A_NEW = r'''    if Path(live_rel).name == "SESSION_NOTES.md":   # PROTOTYPE A (scratch only)
        return r"^\*\*Status:\*\* Session claimed\b.*$"
    spec = LEDGERS.get(Path(live_rel).name)
    return spec.stub_marker.pattern if spec is not None and spec.stub_marker else ""'''

B_OLD = '''for f in fails:
    print("FAIL:", f)
for n in notes:
    print("NOTE:", n)
if fails:
    sys.exit(4 if stub_finalized else 1)'''
B_NEW = '''if stub_finalized:   # PROTOTYPE B (scratch only): treat a recognised stub finalize as OK
    for f in fails:
        print("STUB-FINALIZE (prototype, treated as OK):", f)
    for n in notes:
        print("NOTE:", n)
    sys.exit(0)
for f in fails:
    print("FAIL:", f)
for n in notes:
    print("NOTE:", n)
if fails:
    sys.exit(1)'''


def main():
    src_path, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    src = src_path.read_text()
    assert src.count(A_OLD) == 1, "prototype A: the stub_pattern_for body is not as expected"
    proto_a = src.replace(A_OLD, A_NEW)
    assert proto_a.count(B_OLD) == 1, "prototype B: the end of the proof template is not as expected"
    proto_ab = proto_a.replace(B_OLD, B_NEW)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "trim_protoA.py").write_text(proto_a)
    (out_dir / "trim_protoAB.py").write_text(proto_ab)
    print("wrote", out_dir / "trim_protoA.py", "and", out_dir / "trim_protoAB.py")


if __name__ == "__main__":
    main()
