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
lf = _load("layout_fixtures", HERE / "layout_fixtures.py")


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


# The plan's section 4.1, typed out: the one place the target layout is written as literals, so a change to
# the manifest cannot quietly reshape what "the new layout" means. 34 files, none of them at the root.
S41_FRAMEWORK = ["SESSION_RUNNER.md", "SAFEGUARDS.md", "FRAMEWORK_LEARNINGS.md", "RECOMMENDED_SKILLS.md",
                 "BOOTSTRAP.md", "CONTEXT_TEMPLATE.md", "CLAUDE_TEMPLATE.md",
                 "ITERATIVE_METHODOLOGY.md", "FRAMEWORK_APPARATUS.md", "HOW_TO_USE.md",
                 "methodology_dashboard.py", "methodology_trim.py", "context_budget.py", "quality_ratchet.py"]
S41_WORKSTREAMS = ["DESIGN_WORKSTREAM.md", "ARCHITECTURE_WORKSTREAM.md", "DEVELOPMENT_WORKSTREAM.md",
                   "AUDIT_WORKSTREAM.md", "RESEARCH_DOCUMENTATION_WORKSTREAM.md", "TEMPLATE_WORKSTREAM.md",
                   "RESEARCH_EXHAUSTIVE_VERIFICATION_CAMPAIGN.md",
                   "INHERITED_CODEBASE_FAMILIARIZATION_CAMPAIGN.md", "TEMPLATE_CAMPAIGN.md"]
S41_STATE = ["SESSION_NOTES.md", "CHANGELOG.md", "HANDOFFS.md", "ROADMAP.md",
             ".context-budget.json", ".quality-gates.json", ".gitattributes"]
S41_GENERATED = ["dashboard.html", "dashboard_history.jsonl", ".context-budget-history.jsonl",
                 ".quality-gates-results.json"]


class TestFixtureTrees(Scratch):
    """Trees in both layouts, built from the manifest, for every later phase to reuse."""

    def build(self, layout, **kw):
        return set(lf.build_tree(self.root, layout, **kw))

    def test_the_new_tree_is_exactly_section_4_1(self):
        want = {"methodology/" + n for n in S41_FRAMEWORK + S41_STATE + S41_GENERATED}
        want |= {"methodology/workstreams/" + n for n in S41_WORKSTREAMS}
        self.assertEqual(self.build("new"), want)
        self.assertEqual(len(want), 34)

    def test_the_legacy_tree_is_the_manifest_plus_the_generated_files(self):
        manifest = _load("_manifest", REPO / "bin" / "_manifest.py")
        want = {dest for _, dest, _ in manifest.DISTRIBUTION} | set(S41_GENERATED)
        self.assertEqual(self.build("legacy"), want)

    def test_the_legacy_tree_is_what_bin_sync_writes_into_a_project(self):
        # Faithfulness (gate d): a fixture that no real adopter looks like proves nothing about adopters.
        import subprocess
        project = self.root / "real"
        project.mkdir()
        subprocess.run(["git", "init", "-q", str(project)], check=True)
        r = subprocess.run([sys.executable, "-B", str(REPO / "bin" / "sync"), "--source=local", str(project)],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        synced = {p.relative_to(project).as_posix() for p in project.rglob("*")
                  if p.is_file() and ".git" not in p.relative_to(project).parts}
        fixture_root = self.root / "fixture"
        fixture_root.mkdir()
        built = set(lf.build_tree(fixture_root, "legacy", generated=False))
        self.assertEqual(built, synced)

    def test_the_tier_1_tree_moves_only_what_the_manifest_tracks(self):
        built = self.build("tier1")
        want = {"methodology/" + n for n in S41_FRAMEWORK} | \
               {"methodology/workstreams/" + n for n in S41_WORKSTREAMS} | set(S41_STATE) | set(S41_GENERATED)
        self.assertEqual(built, want)
        self.assertEqual(lr.resolve_layout(self.root)[0], "new")
        self.assertEqual(lr.resolve_layout(self.root, "CHANGELOG.md")[:2], ("legacy", self.root))

    def test_the_half_tree_has_the_runner_in_both_places(self):
        built = self.build("half")
        self.assertIn("SESSION_RUNNER.md", built)
        self.assertIn("methodology/SESSION_RUNNER.md", built)
        self.assertEqual(lr.resolve_layout(self.root)[0], "half")

    def test_the_empty_tree_has_no_files(self):
        self.assertEqual(self.build("empty"), set())
        self.assertEqual(lr.resolve_layout(self.root)[0], "none")

    def test_both_anchors_agree_on_the_two_pure_layouts(self):
        for layout, kind in (("legacy", "legacy"), ("new", "new")):
            with tempfile.TemporaryDirectory() as td:
                lf.build_tree(td, layout)
                for anchor in ("SESSION_RUNNER.md", "CHANGELOG.md", ".quality-gates.json"):
                    self.assertEqual(lr.resolve_layout(td, anchor)[0], kind, (layout, anchor))

    def test_the_archive_follows_its_tier(self):
        self.assertTrue(any(p.startswith("docs/archive/") for p in self.build("legacy", archive=True)))
        with tempfile.TemporaryDirectory() as td:
            self.assertTrue(any(p.startswith("methodology/archive/") for p in lf.build_tree(td, "new", archive=True)))
        with tempfile.TemporaryDirectory() as td:
            # tier 2 moves the archive, so a tier-1 tree keeps it where it was
            self.assertTrue(any(p.startswith("docs/archive/") for p in lf.build_tree(td, "tier1", archive=True)))

    def test_new_path_maps_the_three_kinds_of_destination(self):
        self.assertEqual(lf.new_path("CHANGELOG.md"), "methodology/CHANGELOG.md")
        self.assertEqual(lf.new_path("docs/methodology/HOW_TO_USE.md"), "methodology/HOW_TO_USE.md")
        self.assertEqual(lf.new_path("docs/methodology/workstreams/DESIGN_WORKSTREAM.md"),
                         "methodology/workstreams/DESIGN_WORKSTREAM.md")

    def test_contents_override_by_file_name(self):
        lf.build_tree(self.root, "new", contents={"CHANGELOG.md": "# my ledger\n"})
        self.assertEqual((self.root / "methodology" / "CHANGELOG.md").read_text(encoding="utf-8"), "# my ledger\n")
        self.assertNotEqual((self.root / "methodology" / "HANDOFFS.md").read_text(encoding="utf-8"), "# my ledger\n")

    def test_it_refuses_to_build_into_a_non_empty_directory_or_an_unknown_layout(self):
        touch(self.root, "keep.txt")
        with self.assertRaises(ValueError):
            lf.build_tree(self.root, "new")
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):
                lf.build_tree(td, "sideways")

    def test_every_path_stays_inside_the_root(self):
        for layout in lf.LAYOUTS:
            with tempfile.TemporaryDirectory() as td:
                for rel in lf.build_tree(td, layout, archive=True):
                    self.assertFalse(rel.startswith(("/", "..")) or ".." in Path(rel).parts, rel)
                    self.assertTrue((Path(td) / rel).is_file(), rel)


class TestCanonicalOnly(unittest.TestCase):
    def test_the_resolver_is_not_distributed(self):
        manifest = _load("_manifest", REPO / "bin" / "_manifest.py")
        names = {Path(p).name for row in manifest.DISTRIBUTION for p in row[:2]}
        self.assertNotIn("layout_resolver.py", names)
        self.assertNotIn("test_layout_resolver.py", names)


if __name__ == "__main__":
    unittest.main()
