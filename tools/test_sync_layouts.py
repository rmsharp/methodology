#!/usr/bin/env python3
"""Unit tests for the sync layer in both layouts (BL-101, phase P6).

CANONICAL-ONLY, like tools/test_layout_resolver.py and tools/test_checker_layouts.py: bin/sync,
bin/status and bin/check-links are not in bin/_manifest.py, so adopters do not receive them. The
contract is docs/planning/methodology-subdirectory-plan.md section 7.2 row P6 and the couplings it
names (C1 no blank seed beside a real ledger and no second runner, C2 ignore mode, C3 status and
check-links, C16 the manifest stays data so --source=github can read it).

Layer 0 (this file's first classes): the manifest's second literal table, NEW_LAYOUT, and the reader
that reads it as data. Later layers add bin/sync, bin/status and bin/check-links, each driven as a
command in a scratch project. Every rule is observed failing as well as passing (Learning #12).
"""
import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True  # a test run must not generate bin/__pycache__ or tools/__pycache__

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
MANIFEST = REPO / "bin" / "_manifest.py"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


manifest = _load("_manifest", MANIFEST)
reader = _load("_manifest_reader", REPO / "bin" / "_manifest_reader.py")
lf = _load("layout_fixtures", HERE / "layout_fixtures.py")
tlr = _load("test_layout_resolver", HERE / "test_layout_resolver.py")  # section 4.1, typed out as literals

DISPOSITIONS = (manifest.TRACKED, manifest.SEED)


def section_4_1_destinations():
    """The new destination of every distributed file, from the plan's section 4.1 as
    tools/test_layout_resolver.py types it: flat under methodology/, workstreams/ the one subdirectory."""
    return ({"methodology/" + n for n in tlr.S41_FRAMEWORK + tlr.S41_STATE}
            | {"methodology/workstreams/" + n for n in tlr.S41_WORKSTREAMS})


class Scratch(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory(prefix="sync-layouts-")
        self.addCleanup(self._td.cleanup)
        self.root = Path(self._td.name)

    def manifest_with(self, old=None, new=None, *, name="_manifest.py"):
        """A copy of the real manifest with one unique text replaced (old -> new), written under
        a fresh directory; returns its path. The anchor must occur once, or the fixture is wrong."""
        text = MANIFEST.read_text(encoding="utf-8")
        if old is not None:
            self.assertEqual(text.count(old), 1, "fixture anchor not unique in bin/_manifest.py: %r" % old)
            text = text.replace(old, new)
        d = Path(tempfile.mkdtemp(dir=self.root))
        path = d / name
        path.write_text(text, encoding="utf-8")
        return path

    def read(self, path):
        rows, _markers = reader.read_manifest(path, DISPOSITIONS)
        return reader.read_new_layout(path, rows)


class TestTheManifestsSecondTable(unittest.TestCase):
    """C16: the layout-dependent destinations are a second LITERAL table, never a function, so
    --source=github reads them as data and bin/tests.sh Test 53 can still build its source from the file."""

    def test_it_names_a_new_destination_for_every_distributed_file_and_no_other(self):
        srcs = [src for src, _dest, _disp in manifest.DISTRIBUTION]
        self.assertEqual(sorted(manifest.NEW_LAYOUT), sorted(srcs))
        self.assertEqual(len(srcs), 30)

    def test_the_destinations_are_exactly_section_4_1(self):
        self.assertEqual(set(manifest.NEW_LAYOUT.values()), section_4_1_destinations())
        self.assertEqual(len(set(manifest.NEW_LAYOUT.values())), 30, "two files share one new destination")

    def test_the_workstreams_stay_one_level_down_and_everything_else_is_flat(self):
        for src, dest, _disp in manifest.DISTRIBUTION:
            want = ("methodology/workstreams/" if dest.startswith("docs/methodology/workstreams/")
                    else "methodology/") + Path(dest).name
            self.assertEqual(manifest.NEW_LAYOUT[src], want, src)

    def test_the_fixture_trees_are_built_from_the_table_not_from_a_rule_of_their_own(self):
        with tempfile.TemporaryDirectory() as td:
            built = set(lf.build_tree(td, "new", generated=False))
        self.assertEqual(built, set(manifest.NEW_LAYOUT.values()))
        self.assertFalse(hasattr(lf, "new_path"), "layout_fixtures still carries its own mapping rule")

    def test_the_tier_1_tree_moves_only_the_tracked_rows_to_the_tables_destinations(self):
        with tempfile.TemporaryDirectory() as td:
            built = set(lf.build_tree(td, "tier1", generated=False))
        want = {manifest.NEW_LAYOUT[src] if disp == manifest.TRACKED else dest
                for src, dest, disp in manifest.DISTRIBUTION}
        self.assertEqual(built, want)

    def test_the_reader_reads_the_real_table_as_data_and_it_equals_the_modules(self):
        rows, _markers = reader.read_manifest(MANIFEST, DISPOSITIONS)
        self.assertEqual(reader.read_new_layout(MANIFEST, rows), manifest.NEW_LAYOUT)


class TestTheReaderReadsTheTableAsData(Scratch):
    ROADMAP = '    "starter-kit/ROADMAP.md": "methodology/ROADMAP.md",'
    RUNNER = '    "starter-kit/SESSION_RUNNER.md": "methodology/SESSION_RUNNER.md",'

    def test_a_source_that_predates_the_table_has_none_and_is_still_readable(self):
        path = self.manifest_with("NEW_LAYOUT = {", "OTHER_LAYOUT = {")
        rows, _markers = reader.read_manifest(path, DISPOSITIONS)
        self.assertEqual(len(rows), 30)
        self.assertIsNone(reader.read_new_layout(path, rows))

    def test_the_table_is_never_run_only_read(self):
        marker = self.root / "EXECUTED"
        path = self.manifest_with("NEW_LAYOUT = {", "import pathlib; pathlib.Path(%r).touch()\nNEW_LAYOUT = {" % str(marker))
        self.assertEqual(self.read(path), manifest.NEW_LAYOUT)
        self.assertFalse(marker.exists(), "reading the manifest ran its code")

    def test_a_row_with_no_destination_is_refused_and_named(self):
        path = self.manifest_with(self.ROADMAP, "")
        with self.assertRaises(reader.ManifestError) as cm:
            self.read(path)
        self.assertIn("starter-kit/ROADMAP.md", str(cm.exception))

    def test_a_destination_for_a_file_the_manifest_does_not_distribute_is_refused_and_named(self):
        path = self.manifest_with(self.ROADMAP, self.ROADMAP + '\n    "starter-kit/GHOST.md": "methodology/GHOST.md",')
        with self.assertRaises(reader.ManifestError) as cm:
            self.read(path)
        self.assertIn("starter-kit/GHOST.md", str(cm.exception))

    def test_a_key_written_twice_is_refused_because_the_last_would_win_without_a_word(self):
        path = self.manifest_with(self.ROADMAP, self.ROADMAP + '\n    "starter-kit/ROADMAP.md": "methodology/ROADMAP2.md",')
        with self.assertRaises(reader.ManifestError) as cm:
            self.read(path)
        self.assertIn("starter-kit/ROADMAP.md", str(cm.exception))

    def test_two_files_sharing_one_destination_are_refused_naming_both(self):
        path = self.manifest_with(self.ROADMAP, '    "starter-kit/ROADMAP.md": "methodology/SESSION_RUNNER.md",')
        with self.assertRaises(reader.ManifestError) as cm:
            self.read(path)
        msg = str(cm.exception)
        self.assertIn("starter-kit/ROADMAP.md", msg)
        self.assertIn("starter-kit/SESSION_RUNNER.md", msg)

    def test_an_unsafe_destination_is_refused_before_anything_could_be_written(self):
        for why, bad in (("climbs out", "methodology/../ESCAPED.md"), ("absolute", "/etc/ESCAPED.md"),
                         ("inside .git", "methodology/.git/hooks/pre-commit"), ("names no file", "."),
                         ("empty", ""), ("NUL byte", "methodology/RO\\x00ADMAP.md")):
            with self.subTest(why):
                path = self.manifest_with(self.ROADMAP, '    "starter-kit/ROADMAP.md": "%s",' % bad)
                with self.assertRaises(reader.ManifestError) as cm:
                    self.read(path)
                self.assertIn("starter-kit/ROADMAP.md", str(cm.exception))

    def test_a_destination_outside_methodology_is_refused_because_the_resolver_would_not_find_it(self):
        for bad in ("ROADMAP.md", "docs/methodology/ROADMAP.md", "other/ROADMAP.md"):
            with self.subTest(bad):
                path = self.manifest_with(self.ROADMAP, '    "starter-kit/ROADMAP.md": "%s",' % bad)
                with self.assertRaises(reader.ManifestError) as cm:
                    self.read(path)
                self.assertIn(bad, str(cm.exception))

    def test_a_table_that_is_not_a_dict_of_strings_is_refused(self):
        for shape in ('NEW_LAYOUT = ["a", "b"]\nIGNORED = {', 'NEW_LAYOUT = {"starter-kit/ROADMAP.md": 3}\nIGNORED = {'):
            with self.subTest(shape):
                path = self.manifest_with("NEW_LAYOUT = {", shape)
                with self.assertRaises(reader.ManifestError):
                    self.read(path)

    def test_a_table_that_changes_after_its_assignment_is_refused_naming_it(self):
        extra = '{"starter-kit/ROADMAP.md": "methodology/ROADMAP.md"}'
        for how, line in (("update", "NEW_LAYOUT.update(%s)" % extra), ("item", 'NEW_LAYOUT["starter-kit/ROADMAP.md"] = "methodology/X.md"'),
                          ("second assignment", "NEW_LAYOUT = %s" % extra), ("augmented", "NEW_LAYOUT |= %s" % extra),
                          ("del", 'del NEW_LAYOUT["starter-kit/ROADMAP.md"]')):
            with self.subTest(how):
                path = self.manifest_with("SEED_FORMAT_MARKERS = {", line + "\nSEED_FORMAT_MARKERS = {")
                with self.assertRaises(reader.ManifestError) as cm:
                    self.read(path)
                self.assertIn("NEW_LAYOUT", str(cm.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
