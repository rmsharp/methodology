"""Take the SESSION_NOTES.md ledger entry out of a tree of the PR, leaving the record-0 diff.

Usage: python3 -I excise_sn.py <tree-root> <stage>
  stage "4": the tree of commit 2308553 (header, entry, tests, docs, ledger entry all present)
  stage "5": the tree of commit 1082d3b (the same, plus commit 5's changes on top)

Every removal asserts that its target is present exactly once, so a tree that is not the one this
script was written for fails loudly instead of being half-edited.
"""
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
stage = sys.argv[2]


def once(text, old, new, what):
    assert text.count(old) == 1, "%s: expected exactly one match, found %d" % (what, text.count(old))
    return text.replace(old, new)


def sub_once(pattern, repl, text, what, flags=0):
    new, n = re.subn(pattern, repl, text, flags=flags)
    assert n == 1, "%s: expected exactly one match, found %d" % (what, n)
    return new


# ---- the trimmer ----------------------------------------------------------------------------
tp = root / "starter-kit" / "methodology_trim.py"
s = tp.read_text(encoding="utf-8")

old_head = s[s.index('TRIM_VERSION = "1.8.'):s.index("                         # 1.7.0: issue #93, cause 3")]
new_head = (
    'TRIM_VERSION = "%s"   # %s: issue #93, the proof prints the record-0 diff -- whenever the frontier was\n'
    '                         # edited in the trim commit (exit 4 or exit 1) the generated proof, and so\n'
    '                         # `--reverify`, prints a unified diff of record 0 against the record that\n'
    '                         # replaced it, so a reader can judge in seconds what the proof cannot. Minor,\n'
    '                         # not patch: new proof output. No verdict and no exit status changes.\n'
    '                         #\n'
)
# the version string differs between the stages; the header text of 1.8.1 is edited by the caller
m = re.match(r'TRIM_VERSION = "(1\.8\.\d)"', old_head)
assert m, old_head[:60]
if stage == "4":
    s = s.replace(old_head, new_head % ("1.8.0", "1.8.0"), 1)
else:
    # stage 5: the header carries the 1.8.1 block on top of the 1.8.0 block; replace only the 1.8.0 block
    i0 = s.index("                         # 1.8.0: issue #93, the gap the first three left")
    i1 = s.index("                         # 1.7.0: issue #93, cause 3")
    block = s[i0:i1]
    s = s.replace(block,
                  "                         # 1.8.0: issue #93, the proof prints the record-0 diff -- whenever the\n"
                  "                         # frontier was edited in the trim commit (exit 4 or exit 1) the generated\n"
                  "                         # proof, and so `--reverify`, prints a unified diff of record 0 against\n"
                  "                         # the record that replaced it, so a reader can judge in seconds what the\n"
                  "                         # proof cannot. Minor, not patch: new proof output. No verdict and no exit\n"
                  "                         # status changes.\n"
                  "                         #\n", 1)

s = sub_once(r"def _session_notes_date\(text\):.*?\n\n\n(?=LEDGERS = \{)", "", s, "_session_notes_date",
             flags=re.S)
s = sub_once(r"    # The session-notes file: the runner's Phase 1B claim stub.*?    \),\n(?=\}\n)", "", s,
             "the SESSION_NOTES.md LEDGERS entry", flags=re.S)
s = once(s, "(true of every entry in LEDGERS today)", "(true of both entries in LEDGERS today)", "both entries")
left = [ln.strip()[:110] for ln in s.splitlines() if "SESSION_NOTES" in ln]
print("trimmer lines still naming SESSION_NOTES:", len(left)); [print("   ", x) for x in left]
tp.write_text(s, encoding="utf-8")

# ---- the tests ------------------------------------------------------------------------------
xp = root / "tools" / "test_methodology_trim.py"
t = xp.read_text(encoding="utf-8")
t = once(t,
         '        sn_seed = (REPO / "starter-kit" / "SESSION_NOTES.md").read_text(encoding="utf-8")\n'
         '        self.assertEqual(records_of(sn_seed, mod.LEDGERS["SESSION_NOTES.md"]), [],\n'
         '                         "a freshly seeded notes file has no records")\n',
         "", "TestFixtureControls hunk")
t = once(t,
         '        self.assertEqual(mod.stub_pattern_for("SESSION_NOTES.md"),\n'
         '                         mod.LEDGERS["SESSION_NOTES.md"].stub_marker.pattern,\n'
         '                         "SESSION_NOTES.md has an entry since 1.8.0, and it declares a marker")\n'
         '        self.assertEqual(mod.stub_pattern_for("PROJECT_LEARNINGS.md"), "",\n',
         '        self.assertEqual(mod.stub_pattern_for("SESSION_NOTES.md"), "",\n', "TestReverify hunk")
# the banner, the fixtures and the whole class
b0 = t.index("# Issue #93, the gap the first three commits left -- SESSION_NOTES.md joins the ledger table.")
b0 = t.rindex("# =====", 0, b0)
if stage == "4":
    end = t.index('if __name__ == "__main__":')
else:
    end = t.index("class TestAnAbortBeforeTheChecksIsNotAVerdict")
t = t[:b0].rstrip("\n") + "\n\n\n" + t[end:]
assert "SessionNotes" not in t and "make_session_notes_repo" not in t and "sn_spec" not in t
xp.write_text(t, encoding="utf-8")
print("excised stage", stage)
