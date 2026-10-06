#!/usr/bin/env python3
"""Unit tests for the methodology/ layout work (BL-101, phase P1).

CANONICAL-ONLY. None of tools/layout_resolver.py, tools/layout_fixtures.py or
bin/check-layout-literals is in bin/_manifest.py, so adopters do not receive them: phases
P2-P6 embed the resolver's marked block in each shipped tool, and assert here that every
copy is byte-identical to this module's (the dashboard twin test is the precedent).

The contract is docs/planning/methodology-subdirectory-plan.md section 4.3 (the four-row
table) and section 7.1 (what P1 is done when). Every rule is observed failing as well as
passing (Learning #12): the scanner section builds trees that must be refused.
"""
import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True  # a test run must not generate tools/__pycache__

HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


lr = _load("layout_resolver", HERE / "layout_resolver.py")


def touch(root, *rel):
    p = Path(root).joinpath(*rel)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("x\n", encoding="utf-8")
    return p


class Scratch(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.addCleanup(self._td.cleanup)
        self.root = Path(self._td.name)


class TestTheFourRows(Scratch):
    """Section 4.3, one test per row of the table."""

    def test_row_1_the_runner_under_methodology_is_the_new_layout(self):
        touch(self.root, "methodology", "SESSION_RUNNER.md")
        kind, directory, found = lr.resolve_layout(self.root)
        self.assertEqual(kind, "new")
        self.assertEqual(directory, self.root / "methodology")
        self.assertEqual(found, (self.root / "methodology" / "SESSION_RUNNER.md",))

    def test_row_2_the_runner_at_the_root_is_the_legacy_layout(self):
        touch(self.root, "SESSION_RUNNER.md")
        kind, directory, found = lr.resolve_layout(self.root)
        self.assertEqual(kind, "legacy")
        self.assertEqual(directory, self.root)
        self.assertEqual(found, (self.root / "SESSION_RUNNER.md",))

    def test_row_3_both_is_half_migrated_and_names_both_never_guesses(self):
        touch(self.root, "SESSION_RUNNER.md")
        touch(self.root, "methodology", "SESSION_RUNNER.md")
        kind, directory, found = lr.resolve_layout(self.root)
        self.assertEqual(kind, "half")
        self.assertIsNone(directory, "a half-migrated tree must not yield a directory to guess with")
        self.assertEqual(set(found), {self.root / "SESSION_RUNNER.md",
                                      self.root / "methodology" / "SESSION_RUNNER.md"})

    def test_row_4_neither_is_none(self):
        kind, directory, found = lr.resolve_layout(self.root)
        self.assertEqual((kind, directory, found), ("none", None, ()))

    def test_the_framework_repo_resolves_to_none(self):
        # Row 4's own example: the canonical repo keeps the runner at starter-kit/, not at its root.
        self.assertTrue((REPO / "starter-kit" / "SESSION_RUNNER.md").is_file())
        self.assertEqual(lr.resolve_layout(REPO)[0], "none")


class TestAnchors(Scratch):
    """The table is keyed on one file. A caller picks the anchor for the class of files it reads,
    which is what lets a tier-1-only adopter (framework files moved, ledgers not) be read correctly."""

    def test_the_state_anchor_resolves_independently_of_the_runner(self):
        touch(self.root, "methodology", "SESSION_RUNNER.md")
        touch(self.root, "CHANGELOG.md")
        self.assertEqual(lr.resolve_layout(self.root)[0], "new")
        kind, directory, _ = lr.resolve_layout(self.root, "CHANGELOG.md")
        self.assertEqual((kind, directory), ("legacy", self.root))

    def test_a_directory_named_like_the_anchor_does_not_count(self):
        (self.root / "SESSION_RUNNER.md").mkdir()
        self.assertEqual(lr.resolve_layout(self.root)[0], "none")

    def test_an_unrelated_methodology_directory_is_not_a_layout(self):
        touch(self.root, "methodology", "notes.txt")
        touch(self.root, "SESSION_RUNNER.md")
        self.assertEqual(lr.resolve_layout(self.root)[:2], ("legacy", self.root))

    def test_a_string_root_is_accepted(self):
        touch(self.root, "SESSION_RUNNER.md")
        self.assertEqual(lr.resolve_layout(str(self.root))[0], "legacy")


class TestTheBlockIsEmbeddable(Scratch):
    """Shipped tools are single stdlib files, so each carries the same marked block (section 4.3)."""

    def setUp(self):
        super().setUp()
        self.source = (HERE / "layout_resolver.py").read_text(encoding="utf-8")
        self.block = lr.embedded_block(self.source)

    def test_the_module_carries_one_marked_block(self):
        self.assertIsNotNone(self.block)
        self.assertTrue(self.block.startswith(lr.BEGIN))
        self.assertTrue(self.block.rstrip("\n").endswith(lr.END))
        self.assertEqual(self.source.count(lr.BEGIN), 1)
        self.assertEqual(self.source.count(lr.END), 1)

    def test_the_block_runs_alone_and_answers_the_four_rows(self):
        ns = {}
        exec(compile(self.block, "<block>", "exec"), ns)
        resolve = ns["resolve_layout"]
        self.assertEqual(resolve(self.root)[0], "none")
        touch(self.root, "SESSION_RUNNER.md")
        self.assertEqual(resolve(self.root)[0], "legacy")
        touch(self.root, "methodology", "SESSION_RUNNER.md")
        self.assertEqual(resolve(self.root)[0], "half")
        (self.root / "SESSION_RUNNER.md").unlink()
        self.assertEqual(resolve(self.root)[0], "new")

    def test_the_block_agrees_with_the_module_on_every_tree_shape(self):
        ns = {}
        exec(compile(self.block, "<block>", "exec"), ns)
        for shapes in ([], [("SESSION_RUNNER.md",)], [("methodology", "SESSION_RUNNER.md")],
                       [("SESSION_RUNNER.md",), ("methodology", "SESSION_RUNNER.md")]):
            with tempfile.TemporaryDirectory() as td:
                for s in shapes:
                    touch(td, *s)
                self.assertEqual(ns["resolve_layout"](td), lr.resolve_layout(td))

    def test_the_block_imports_only_the_standard_library(self):
        import ast
        mods = set()
        for node in ast.walk(ast.parse(self.block)):
            if isinstance(node, ast.Import):
                mods.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                mods.add((node.module or "").split(".")[0])
        self.assertLessEqual(mods, {"os", "pathlib"})

    def test_embedded_block_finds_a_copy_inside_another_file(self):
        host = "import sys\n\n" + self.block + "\n\ndef main():\n    pass\n"
        self.assertEqual(lr.embedded_block(host), self.block)

    def test_embedded_block_is_none_without_markers_and_refuses_unbalanced_ones(self):
        self.assertIsNone(lr.embedded_block("import sys\n"))
        with self.assertRaises(ValueError):
            lr.embedded_block(lr.BEGIN + "\nx = 1\n")
        with self.assertRaises(ValueError):
            lr.embedded_block(self.block + "\n" + self.block)


class TestCanonicalOnly(unittest.TestCase):
    def test_the_resolver_is_not_distributed(self):
        manifest = _load("_manifest", REPO / "bin" / "_manifest.py")
        names = {Path(p).name for row in manifest.DISTRIBUTION for p in row[:2]}
        self.assertNotIn("layout_resolver.py", names)
        self.assertNotIn("test_layout_resolver.py", names)


if __name__ == "__main__":
    unittest.main()
