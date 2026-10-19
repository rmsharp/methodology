"""Points 4 to 8 of the maintainer's comment on PR #94, each reproduced on a throwaway repository.

Usage: python3 -I verify_points.py <trimmer.py> <tests-module.py>

The tests module is loaded only for its fixture helpers (`make_handoff_repo`, `make_repo`,
`run_trim`, `sh`); TRIM_PY is overridden so the trimmer given on the command line writes every
proof. Run it against the PR head (1082d3b) for the "before" reading and against a fixed tree for
the "after" reading. Each point prints what was OBSERVED; the maintainer's claim it tests is in the
heading. Points 1 and 2 have their own scripts (point1_removed_ledger.py, point2_planted_module.py).
"""
import importlib.util
import pathlib
import re
import sys
import tempfile

trimmer, tests = sys.argv[1], sys.argv[2]
sys.dont_write_bytecode = True
_spec = importlib.util.spec_from_file_location("t", tests)
t = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(t)
t.TRIM_PY = pathlib.Path(trimmer)


def shard_of(p, ledger_glob="HANDOFFS-through-*.md"):
    return sorted((p / "docs" / "archive").glob(ledger_glob))[0]


def trim(p, ledger="HANDOFFS.md"):
    r = t.run_trim(p, "--file", ledger, "--cut", "2", "--write", "--today", "2026-02-01")
    assert "[WROTE]" in r.stdout, r.stdout
    return r.stdout


def interesting(out, keys=("FAIL:", "NOTE:", "DIFF:", "OK:", "verify:")):
    return [ln[:200] for ln in out.splitlines() if ln.startswith(keys)]


def show(title, rows):
    print("\n== %s" % title)
    for r in rows:
        print("   " + r)


def point4a():
    """4a: 'A trim committed on its own while record 0 is a pending stub passes, but
    FRONTIER_PENDING_STUB warns against it.'"""
    with tempfile.TemporaryDirectory() as tmp:
        p = t.make_handoff_repo(tmp)
        hf = p / "HANDOFFS.md"
        hf.write_text(hf.read_text(encoding="utf-8").replace("status: complete", "status: pending", 1),
                      encoding="utf-8")
        t.sh(p, "git", "commit", "-q", "--amend", "-a", "-m", "seed")  # one commit: no undocumented set
        out = trim(p)
        t.sh(p, "git", "add", "-A")
        t.sh(p, "git", "commit", "-qm", "trim, alone (record 0 untouched)")
        v = t.sh(p, "bash", shard_of(p).relative_to(p).as_posix() + ".verify.sh")
        show("4a  trim committed alone while record 0 is a pending stub",
             ["trimmer printed FRONTIER_PENDING_STUB: %s" % ("FRONTIER_PENDING_STUB" in out),
              "proof exit: %d" % v.returncode] + interesting(v.stdout))


def point4b():
    """4b: 'an ACTIVE TASK edit in the trim commit fails L2 after the trimmer printed L2_OK.'"""
    with tempfile.TemporaryDirectory() as tmp:
        p = t.make_handoff_repo(tmp)
        hf = p / "HANDOFFS.md"
        hf.write_text(hf.read_text(encoding="utf-8").replace(
            "# Handoff Receipts\n\n", "# Handoff Receipts\n\nACTIVE TASK: alpha\n\n", 1), encoding="utf-8")
        t.sh(p, "git", "commit", "-q", "--amend", "-a", "-m", "seed")  # one commit: no undocumented set
        out = trim(p)
        hf.write_text(hf.read_text(encoding="utf-8").replace("ACTIVE TASK: alpha", "ACTIVE TASK: beta"),
                      encoding="utf-8")
        t.sh(p, "git", "add", "-A")
        t.sh(p, "git", "commit", "-qm", "trim AND an ACTIVE TASK edit, one commit")
        v = t.sh(p, "bash", shard_of(p).relative_to(p).as_posix() + ".verify.sh")
        show("4b  an ACTIVE TASK (front matter) edit in the trim commit",
             ["trimmer printed [L2_OK]: %s" % ("[L2_OK]" in out), "proof exit: %d" % v.returncode]
             + interesting(v.stdout))


def point5():
    """5: 'A stray `status: pending` after a complete receipt gives exit 4 on a real loss.'"""
    with tempfile.TemporaryDirectory() as tmp:
        p = t.make_handoff_repo(tmp)
        hf = p / "HANDOFFS.md"
        text = hf.read_text(encoding="utf-8")
        tail = "Self-score **8/10.** commentary about session 0.\n"
        assert text.count(tail) == 1
        hf.write_text(text.replace(tail, tail + "status: pending\n"), encoding="utf-8")
        t.sh(p, "git", "commit", "-q", "--amend", "-a", "-m", "seed")  # one commit: no undocumented set
        trim(p)
        text = hf.read_text(encoding="utf-8")
        text = text.replace("status: pending\n", "", 1)                       # the stray line goes
        text = re.sub(r"what_was_done: x{34000}", "what_was_done: x", text, count=1)   # the LOSS
        hf.write_text(text, encoding="utf-8")
        t.sh(p, "git", "add", "-A")
        t.sh(p, "git", "commit", "-qm", "trim, and record 0 loses 34,000 B of what_was_done")
        v = t.sh(p, "bash", shard_of(p).relative_to(p).as_posix() + ".verify.sh")
        show("5   a complete record 0 that LOST data, with a stray `status: pending` line in the parent",
             ["proof exit: %d (4 = labelled a recognised stub finalize; 1 = a plain FAIL)" % v.returncode]
             + interesting(v.stdout))


def point6():
    """6: '--reverify doesn't lift PREFIX, so a passing proof at nprcgenekeepr's HEAD
    (PREFIX = "../") reads exit 1. It should refuse instead.'"""
    with tempfile.TemporaryDirectory() as tmp:
        p = t.make_repo(tmp)
        r = t.run_trim(p, "--file", "CHANGELOG.md", "--write", "--today", "2026-02-01")
        assert "[WROTE]" in r.stdout, r.stdout
        shard = shard_of(p, "CHANGELOG-through-*.md")
        proof = pathlib.Path(str(shard) + ".verify.sh")
        (p / "archive").mkdir()
        new_shard = p / "archive" / shard.name
        new_proof = p / "archive" / proof.name
        # a shard one directory deep: its links climb one level, not two
        new_shard.write_text(shard.read_text(encoding="utf-8").replace("](../../", "](../"), encoding="utf-8")
        ptxt = proof.read_text(encoding="utf-8")
        ptxt = ptxt.replace("SHARD=docs/archive/", "SHARD=archive/").replace('PREFIX = "../../"', 'PREFIX = "../"')
        new_proof.write_text(ptxt, encoding="utf-8")
        shard.unlink()
        proof.unlink()
        ctext = (p / "CHANGELOG.md").read_text(encoding="utf-8").replace("docs/archive/", "archive/")
        (p / "CHANGELOG.md").write_text(ctext, encoding="utf-8")
        t.sh(p, "git", "add", "-A")
        t.sh(p, "git", "commit", "-qm", "trim, shard one directory deep")
        rel = "archive/" + shard.name
        v = t.sh(p, "bash", rel + ".verify.sh")
        rv = t.run_trim(p, "--reverify", rel)
        show("6   a passing proof whose PREFIX is \"../\"",
             ["frozen proof as written: exit %d" % v.returncode,
              "--reverify: exit %d" % rv.returncode]
             + [ln[:200] for ln in rv.stdout.splitlines() if "REVERIFY" in ln or ln.startswith("FAIL")][:4])


def point7():
    """7: 'A \\r in RECORD_START crashes the proof, which reports exit 1.'"""
    with tempfile.TemporaryDirectory() as tmp:
        p = t.make_handoff_repo(tmp)
        trim(p)
        t.sh(p, "git", "add", "-A")
        t.sh(p, "git", "commit", "-qm", "trim")
        shard = shard_of(p).relative_to(p).as_posix()
        proof = p / (shard + ".verify.sh")
        text = proof.read_text(encoding="utf-8")
        text2 = re.sub(r'(?m)^(RECORD_START = r")([^"\n]*)(")$', lambda m: m.group(1) + m.group(2) + "\r" + m.group(3),
                       text, count=1)
        assert text2 != text
        with open(str(proof), "w", encoding="utf-8", newline="") as fh:
            fh.write(text2)
        rv = t.run_trim(p, "--reverify", shard)
        show("7   a carriage return in the frozen proof's RECORD_START line",
             ["--reverify exit: %d (1 = read as a FAIL; 3 = the proof did not finish)" % rv.returncode]
             + [ln[:160] for ln in rv.stdout.splitlines() if "Error" in ln or "REVERIFY" in ln][:4])


def point8():
    """8: 'The generic note and diff hide a reorder.'"""
    with tempfile.TemporaryDirectory() as tmp:
        p = t.make_handoff_repo(tmp)
        trim(p)
        shard = shard_of(p)
        text = shard.read_text(encoding="utf-8")
        pos = [text.index("```handoff\nsession: S%d\n" % i) for i in (2, 3, 4)]
        a, b = text[pos[0]:pos[1]], text[pos[1]:pos[2]]
        shard.write_text(text[:pos[0]] + b + a + text[pos[2]:], encoding="utf-8")        # S2 and S3 swapped
        hf = p / "HANDOFFS.md"
        old = "commentary about session 0."
        htext = hf.read_text(encoding="utf-8")
        assert htext.count(old) == 1
        hf.write_text(htext.replace(old, old + " (edited)"), encoding="utf-8")            # record 0 edited
        t.sh(p, "git", "add", "-A")
        t.sh(p, "git", "commit", "-qm", "trim, record 0 edited, two archived records swapped")
        v = t.sh(p, "bash", shard.relative_to(p).as_posix() + ".verify.sh")
        lines = interesting(v.stdout)
        show("8   record 0 edited AND two archived records reordered, in one trim commit",
             ["proof exit: %d" % v.returncode] + [ln[:170] for ln in lines]
             + ["names a reorder anywhere in the output: %s" % bool(re.search(r"reorder|out of order", v.stdout, re.I))])


if __name__ == "__main__":
    print("trimmer:", trimmer)
    for fn in (point4a, point4b, point5, point6, point7, point8):
        fn()
