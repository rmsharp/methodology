#!/usr/bin/env python3
"""The canonical checkers find their ledger (or config) at the project root or under methodology/ (BL-101 P4).

CANONICAL-ONLY, like the checkers it drives (bin/check-handoff, bin/check-ledger, bin/check-overhead,
bin/model-report): none is in bin/_manifest.py. bin/check-learnings is not driven here: it reads the
framework's own learnings table under starter-kit/ and no ledger, and the scanner reads zero root
literals in it.

Plan section 4.3 and 7.2b. Each tool is run as a command, in a scratch project, in four shapes:

    legacy   its file at the root
    new      its file under methodology/, nothing at the root
    tie      the file at BOTH places and the runner tracked under methodology/ and not at the root:
             the methodology copy is the framework's and the root copy is the project's own, which
             the tool must not read (the root copy here is deliberately unreadable as a ledger)
    half     the file at both places and no runner under methodology/ (or a runner at both): refused,
             naming both, never guessed

Every assertion is on a value (which path was read, what was counted), never on an exit code alone: an
exit code is a union over every check a tool runs.
"""
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
BIN = REPO / "bin"

ENTRY = "### 2026-01-01 · [ad hoc] an entry\n\n- body\n- **Model:** Claude Sonnet 5.5\n"
LEDGER = "# Changelog\n\n## 2026-01\n\n" + ENTRY
JUNK_LEDGER = "# Changelog\n\n## 2026-01\n\n<<<<<<< ours\n### no heading shape\nstray text\n"   # a conflict marker
HANDOFFS_EMPTY = "# Handoff Receipts\n\nno receipts yet\n"
HANDOFFS_JUNK = "# Handoff Receipts\n\n```handoff\nsession: S1\n"        # an unclosed fence
HANDOFFS_MODEL = ("# Handoff Receipts\n\n```handoff\nsession: S1\ndate: 2026-01-01\nstatus: complete\n```\n\n"
                  "The model wrote it.\n")   # free text AFTER the block is what the secondary source reads
CONFIG = '{"classes": {"read-set": {"total_bytes": 1000}}, "files": [{"path": "%s", "class": "read-set"}]}'
SHARD = "# Changelog shard\n\n### 2025-12-01 · [ad hoc] an archived entry\n\n- body\n- **Model:** Claude Fixture Shard 7\n"


def touch(root, rel, text="x\n"):
    p = Path(root, *rel.split("/"))
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


class Project(unittest.TestCase):
    """A scratch git repository; the tools find their project from the current directory."""

    def setUp(self):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        self.root = os.path.realpath(td.name)
        subprocess.run(["git", "init", "-q", self.root], check=True)

    def run_tool(self, tool, *args):
        p = subprocess.run([sys.executable, "-B", str(BIN / tool), *args], cwd=self.root,
                           capture_output=True, text=True)
        return p.returncode, re.sub(r"\x1b\[[0-9;]*m", "", p.stdout), p.stderr

    def shape(self, name, rel, good, junk):
        """Write `rel` (a root-relative name) in one of the four shapes."""
        new = "methodology/" + rel
        if name == "legacy":
            touch(self.root, rel, good)
        elif name == "new":
            touch(self.root, new, good)
        elif name == "tie":
            touch(self.root, new, good)
            touch(self.root, rel, junk)
            touch(self.root, "methodology/SESSION_RUNNER.md", "runner\n")
        elif name == "half":
            touch(self.root, new, good)
            touch(self.root, rel, good)
        elif name == "half-two-runners":
            touch(self.root, new, good)
            touch(self.root, rel, good)
            touch(self.root, "methodology/SESSION_RUNNER.md", "runner\n")
            touch(self.root, "SESSION_RUNNER.md", "runner\n")
        else:
            raise ValueError(name)
        subprocess.run(["git", "-C", self.root, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.root, "-c", "user.name=t", "-c", "user.email=t@t",
                        "commit", "-q", "-m", "fixture"], check=True, capture_output=True)

    def assertNamesBoth(self, out, rel):
        self.assertIn(rel, out)
        self.assertIn("methodology/" + rel, out)


class TestCheckLedger(Project):
    def test_each_layout_reads_its_own_ledger(self):
        for name, ledger in (("legacy", "CHANGELOG.md"), ("new", "methodology/CHANGELOG.md"),
                             ("tie", "methodology/CHANGELOG.md")):
            with self.subTest(layout=name):
                self.setUp()
                self.shape(name, "CHANGELOG.md", LEDGER, JUNK_LEDGER)
                rc, out, err = self.run_tool("check-ledger")
                self.assertEqual((rc, "OK" in out), (0, True), out + err)
                self.assertIn("1 file(s)", out)

    def test_a_tree_the_runner_does_not_decide_is_refused_naming_both(self):
        for name in ("half", "half-two-runners"):
            with self.subTest(layout=name):
                self.setUp()
                self.shape(name, "CHANGELOG.md", LEDGER, LEDGER)
                rc, out, err = self.run_tool("check-ledger")
                self.assertEqual(rc, 2, out + err)
                self.assertNamesBoth(err, "CHANGELOG.md")

    def test_all_reads_the_shards_beside_the_ledger_in_either_layout(self):
        for name, shard in (("legacy", "docs/archive/CHANGELOG-through-2025-12-01.md"),
                            ("new", "methodology/archive/CHANGELOG-through-2025-12-01.md"),
                            ("new", "docs/archive/CHANGELOG-through-2025-12-01.md")):   # the archive moves last (D5)
            with self.subTest(layout=name, shard=shard):
                self.setUp()
                self.shape(name, "CHANGELOG.md", LEDGER, JUNK_LEDGER)
                touch(self.root, shard, SHARD)
                rc, out, err = self.run_tool("check-ledger", "--all")
                self.assertEqual(rc, 0, out + err)
                self.assertIn("2 file(s)", out, "the ledger and its shard")


class TestARepositoryCalledMethodology(unittest.TestCase):
    """The authoring repository is a directory NAMED methodology with its ledger and docs/archive/ at its root.
    A tool that takes a directory so named for a project's methodology/ subdirectory looks one level up and
    finds nothing: check-ledger --all reported `OK -- 1 file(s)` over a repository holding 20 shards, which no
    fixture named anything else could show. A repository root is told by its .git."""

    def test_check_ledger_all_reads_the_shards_of_a_repository_that_is_itself_called_methodology(self):
        with tempfile.TemporaryDirectory() as td:
            proj = os.path.join(os.path.realpath(td), "methodology")
            os.makedirs(proj)
            subprocess.run(["git", "init", "-q", proj], check=True)
            touch(proj, "CHANGELOG.md", LEDGER)
            touch(proj, "docs/archive/CHANGELOG-through-2025-12-01.md", SHARD)
            p = subprocess.run([sys.executable, "-B", str(BIN / "check-ledger"), "--all"], cwd=proj,
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertIn("2 file(s)", p.stdout, "the ledger and its shard")

    def test_the_same_directory_holding_a_projects_methodology_subdirectory_still_looks_there(self):
        with tempfile.TemporaryDirectory() as td:
            outer = os.path.realpath(td)
            subprocess.run(["git", "init", "-q", outer], check=True)
            touch(outer, "methodology/CHANGELOG.md", LEDGER)
            touch(outer, "methodology/archive/CHANGELOG-through-2025-12-01.md", SHARD)
            touch(outer, "docs/archive/CHANGELOG-through-2025-11-01.md", SHARD)
            p = subprocess.run([sys.executable, "-B", str(BIN / "check-ledger"), "--file",
                                os.path.join(outer, "methodology", "CHANGELOG.md"), "--all"], cwd=outer,
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertIn("3 file(s)", p.stdout, "the ledger and a shard in each archive directory")


class TestCheckHandoff(Project):
    def test_each_layout_reads_its_own_ledger(self):
        for name, ledger in (("legacy", "HANDOFFS.md"), ("new", "methodology/HANDOFFS.md"),
                             ("tie", "methodology/HANDOFFS.md")):
            with self.subTest(layout=name):
                self.setUp()
                self.shape(name, "HANDOFFS.md", HANDOFFS_EMPTY, HANDOFFS_JUNK)
                rc, out, err = self.run_tool("check-handoff", "--allow-none")
                self.assertEqual(rc, 0, out + err)
                self.assertIn(os.path.join(self.root, ledger), out, "the note names the file it read")

    def test_a_tree_the_runner_does_not_decide_is_refused_naming_both(self):
        for name in ("half", "half-two-runners"):
            with self.subTest(layout=name):
                self.setUp()
                self.shape(name, "HANDOFFS.md", HANDOFFS_EMPTY, HANDOFFS_EMPTY)
                rc, out, err = self.run_tool("check-handoff", "--allow-none")
                self.assertEqual(rc, 1, out + err)
                self.assertNamesBoth(out, "HANDOFFS.md")

    def test_the_canonical_seed_is_still_the_fallback_for_a_tree_with_no_ledger(self):
        touch(self.root, "starter-kit/HANDOFFS.md", HANDOFFS_EMPTY)
        rc, out, err = self.run_tool("check-handoff", "--allow-none")
        self.assertEqual(rc, 0, out + err)
        self.assertIn(os.path.join(self.root, "starter-kit", "HANDOFFS.md"), out)


class TestCheckOverhead(Project):
    """The class total is the sum of the declared files' sizes, so the value that proves WHICH config was
    read is the byte count. The tool used to look for the config at the root only, and from a project
    whose config sat under methodology/ it fell through to ITS OWN directory and measured the tree it
    shipped in: a wrong number, printed as a measurement."""

    def project(self, name):
        self.shape(name, ".context-budget.json", CONFIG % "doc.md", CONFIG % "other.md")
        touch(self.root, "doc.md", "12345\n")            # 6 B
        touch(self.root, "other.md", "123456789012\n")   # 13 B

    def test_each_layout_measures_the_project_whose_config_it_found(self):
        for name in ("legacy", "new", "tie"):
            with self.subTest(layout=name):
                self.setUp()
                self.project(name)
                rc, out, err = self.run_tool("check-overhead")
                self.assertEqual(rc, 0, out + err)
                self.assertIn("read-set: 6 B ", out)

    def test_run_from_inside_methodology_it_names_the_project_not_that_directory(self):
        self.project("new")
        p = subprocess.run([sys.executable, "-B", str(BIN / "check-overhead")],
                           cwd=os.path.join(self.root, "methodology"), capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("read-set: 6 B ", p.stdout)

    def test_a_repository_that_is_itself_called_methodology_stays_its_own_project(self):
        """The authoring repository is a directory named methodology with its config at its root: taken for the
        methodology/ directory of a project, it would send the walk one level up. Test 44 of bin/tests.sh found
        this on the real repository; no fixture named methodology could."""
        with tempfile.TemporaryDirectory() as td:
            proj = os.path.join(os.path.realpath(td), "methodology")
            os.makedirs(proj)
            subprocess.run(["git", "init", "-q", proj], check=True)
            touch(proj, ".context-budget.json", CONFIG % "doc.md")
            touch(proj, "doc.md", "12345\n")
            p = subprocess.run([sys.executable, "-B", str(BIN / "check-overhead")], cwd=proj,
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertIn("read-set: 6 B ", p.stdout)

    def test_a_tree_the_runner_does_not_decide_is_refused_naming_both(self):
        for name in ("half", "half-two-runners"):
            with self.subTest(layout=name):
                self.setUp()
                self.project(name)
                rc, out, err = self.run_tool("check-overhead")
                self.assertEqual(rc, 2, out + err)
                self.assertNamesBoth(err, ".context-budget.json")


class TestModelReport(Project):
    def test_each_layout_reads_its_own_ledgers(self):
        for name, pre in (("legacy", ""), ("new", "methodology/"), ("tie", "methodology/")):
            with self.subTest(layout=name):
                self.setUp()
                self.shape(name, "CHANGELOG.md", LEDGER, JUNK_LEDGER)
                self.shape(name, "HANDOFFS.md", HANDOFFS_MODEL, HANDOFFS_JUNK)
                rc, out, err = self.run_tool("model-report", "--no-git")
                self.assertEqual(rc, 0, out + err)
                self.assertIn("-- %sCHANGELOG.md (live)" % pre, out, "the header names the file it read")
                self.assertIn("Claude Sonnet 5.5", out, "the entry was read")
                self.assertIn("The model wrote it.", out, "the receipt was read")
                if pre:
                    self.assertNotIn("<<<<<<<", out)

    def test_a_tree_the_runner_does_not_decide_is_refused_naming_both(self):
        for name in ("half", "half-two-runners"):
            with self.subTest(layout=name):
                self.setUp()
                self.shape(name, "CHANGELOG.md", LEDGER, LEDGER)
                touch(self.root, "HANDOFFS.md", HANDOFFS_MODEL)
                rc, out, err = self.run_tool("model-report", "--no-git")
                self.assertEqual(rc, 1, out + err)
                self.assertNamesBoth(out, "CHANGELOG.md")

    def test_the_shards_are_found_beside_the_ledger_in_either_layout(self):
        for name, shard in (("legacy", "docs/archive/CHANGELOG-through-2025-12-01.md"),
                            ("new", "methodology/archive/CHANGELOG-through-2025-12-01.md"),
                            ("new", "docs/archive/CHANGELOG-through-2025-12-01.md")):
            with self.subTest(layout=name, shard=shard):
                self.setUp()
                self.shape(name, "CHANGELOG.md", LEDGER, JUNK_LEDGER)
                self.shape(name, "HANDOFFS.md", HANDOFFS_MODEL, HANDOFFS_JUNK)
                touch(self.root, shard, SHARD)
                rc, out, err = self.run_tool("model-report", "--no-git")
                self.assertEqual(rc, 0, out + err)
                self.assertIn("Claude Fixture Shard 7", out, "the shard's entry was read")


if __name__ == "__main__":
    unittest.main(verbosity=1)
