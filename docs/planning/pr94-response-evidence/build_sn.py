"""Build the second change (SESSION_NOTES.md joins the ledger table) on top of the fixed PR branch.

Run inside the second worktree. Everything is taken from the ORIGINAL commits of the pull request
(2308553 and 1082d3b) by extraction, then adapted: the timing rule's new wording, the version
(1.9.0), the `--cut DATE` comment, the README line. Every insertion asserts its anchor occurs once.
"""
import pathlib
import re
import subprocess


def git_show(rev, path):
    return subprocess.run(["git", "show", "%s:%s" % (rev, path)], stdout=subprocess.PIPE, text=True,
                          check=True).stdout


def once(text, old, new, what):
    assert text.count(old) == 1, "%s: expected exactly one match, found %d" % (what, text.count(old))
    return text.replace(old, new)


ORIG = "1082d3b"

# ---- the trimmer ----------------------------------------------------------------------------
orig = git_show(ORIG, "starter-kit/methodology_trim.py")
fn = re.search(r"def _session_notes_date\(text\):.*?\n\n\n(?=LEDGERS = \{)", orig, re.S).group(0)
entry = re.search(r"    # The session-notes file: the runner's Phase 1B claim stub.*?    \),\n(?=\}\n)", orig, re.S).group(0)

# the one comment that was wrong: the date is NOT label-only
old_c = ("    # bare YYYY-MM-DD anywhere in the record, else None. Used only to LABEL a shard's span in its\n"
         "    # header and pointer text -- never compared against anything L1/L2/L3 assert.\n")
new_c = ("    # bare YYYY-MM-DD anywhere in the record, else None. It LABELS a shard's span in its header and\n"
         "    # pointer text, and it DECIDES where `--cut DATE` falls (`resolve_cut` compares it with the date\n"
         "    # given), so a record whose only date is the fallback -- the first bare date in its text, which\n"
         "    # need not be its own -- can be cut by a date that is not its. The cut is lossless either way: it\n"
         "    # moves records, it does not judge them. Never compared against anything L1/L2/L3 assert.\n")
fn = once(fn, old_c, new_c, "date comment")

tp = pathlib.Path("starter-kit/methodology_trim.py")
s = tp.read_text(encoding="utf-8")
s = once(s, "\n\nLEDGERS = {", "\n\n" + fn.rstrip("\n") + "\n\n\nLEDGERS = {", "insert _session_notes_date")
s = once(s, "    ),\n}\n\n\n# ====", "    ),\n" + entry + "}\n\n\n# ====", "insert LEDGERS entry")
s = once(s, "(true of both entries in LEDGERS today)", "(true of every entry in LEDGERS today)", "both entries")
s = once(s, 'TRIM_VERSION = "1.8.2"   # 1.8.2:',
         'TRIM_VERSION = "1.9.0"   # 1.9.0: issue #93, SESSION_NOTES.md joins LEDGERS -- seven of the adopter\'s ten failing\n'
         '                         # proofs are SESSION_NOTES.md shards, a ledger the table did not list, so no stub\n'
         '                         # marker reached them and `--reverify` could print only the generic failures. The\n'
         '                         # entry: the runner\'s two record shapes (`### What Session N Did`, `### Session N-1\n'
         '                         # Handoff Evaluation (by Session N)`), no footer, a best-effort record date, and a stub\n'
         '                         # marker that needs BOTH Phase 1B lines -- the `**Status:** Session claimed` line and\n'
         '                         # the `(IN PROGRESS)` tag -- because a finished record in 3 of 12 measured adopters\n'
         '                         # still carries the first. Minor, not patch: a third ledger the tool can trim. The two\n'
         '                         # existing ledgers\' verdicts are unchanged.\n'
         '                         #\n'
         '                         # 1.8.2:', "version")
tp.write_text(s, encoding="utf-8")

# ---- the tests ------------------------------------------------------------------------------
orig_t = git_show(ORIG, "tools/test_methodology_trim.py")
b0 = orig_t.index("# Issue #93, the gap the first three commits left -- SESSION_NOTES.md joins the ledger table.")
b0 = orig_t.rindex("# =====", 0, b0)
b1 = orig_t.index("class TestAnAbortBeforeTheChecksIsNotAVerdict")
block = orig_t[b0:b1].rstrip("\n") + "\n"
# the HANDOFFS half of this test now lives in TestTheProofPrintsTheRecord0Diff
h0 = block.index("        with tempfile.TemporaryDirectory() as tmp:\n            helper = TestVerifyShNamesAStubFinalize()\n            p = helper._stub_repo(tmp)\n            shard = helper._trim(p)\n            helper._edit_live(p, \"status: pending\\n\", \"status: complete\\n\", \"record 0 must be finalized\")")
h1 = block.index("    def test_no_diff_prints_when_a_record_other_than_the_frontier_is_edited")
block = block[:h0].rstrip("\n") + "\n\n" + block[h1:]
block = once(block, "def test_the_diff_also_prints_for_the_generic_frontier_edit_and_for_a_HANDOFFS_stub(self):",
             "def test_the_diff_also_prints_for_the_generic_frontier_edit(self):", "test rename")
xp = pathlib.Path("tools/test_methodology_trim.py")
t = xp.read_text(encoding="utf-8")
tail = '\n\nif __name__ == "__main__":\n    unittest.main(verbosity=2)\n'
assert t.endswith(tail)
t = t[:-len(tail)].rstrip("\n") + "\n\n\n" + block + tail
t = once(t,
         '        self.assertEqual(records_of(hf_seed, HF), [], "a freshly seeded ledger has no records")\n',
         '        self.assertEqual(records_of(hf_seed, HF), [], "a freshly seeded ledger has no records")\n'
         '        sn_seed = (REPO / "starter-kit" / "SESSION_NOTES.md").read_text(encoding="utf-8")\n'
         '        self.assertEqual(records_of(sn_seed, mod.LEDGERS["SESSION_NOTES.md"]), [],\n'
         '                         "a freshly seeded notes file has no records")\n', "TestFixtureControls")
t = once(t,
         '        self.assertEqual(mod.stub_pattern_for("SESSION_NOTES.md"), "",\n',
         '        self.assertEqual(mod.stub_pattern_for("SESSION_NOTES.md"),\n'
         '                         mod.LEDGERS["SESSION_NOTES.md"].stub_marker.pattern,\n'
         '                         "SESSION_NOTES.md has an entry since 1.9.0, and it declares a marker")\n'
         '        self.assertEqual(mod.stub_pattern_for("PROJECT_LEARNINGS.md"), "",\n', "TestReverify")
xp.write_text(t, encoding="utf-8")

# ---- the docs -------------------------------------------------------------------------------
fp = pathlib.Path("FRAMEWORK_APPARATUS.md")
f = fp.read_text(encoding="utf-8")
f = once(f,
 "claim leaves record 0 of `HANDOFFS.md` as a `status: pending` stub that close-out overwrites in\n"
 "place. A trim that lands in that same commit",
 "claim leaves record 0 of `HANDOFFS.md` as a `status: pending` stub, and record 0 of `SESSION_NOTES.md`\n"
 "as the Phase 1B stub (a `**Deliverable:** … (IN PROGRESS)` line and a `**Status:** Session claimed`\n"
 "line); close-out overwrites both in place. A trim that lands in that same commit", "APPARATUS paragraph")
fp.write_text(f, encoding="utf-8")

rp = pathlib.Path("README.md")
r = rp.read_text(encoding="utf-8")
r = once(r, "Ledger trimmer (archives cold CHANGELOG/HANDOFFS entries losslessly)",
         "Ledger trimmer (archives cold CHANGELOG, HANDOFFS and SESSION_NOTES entries losslessly)", "README line 204")
rp.write_text(r, encoding="utf-8")
print("built")
