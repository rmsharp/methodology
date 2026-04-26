#!/usr/bin/env python3
"""Regression tests for tools/methodology_dashboard.py.

Currently exercises collect_coverage_config(). The function detects coverage
configuration in a project. Two prior bugs motivate these tests:

  1. Vitest double-counting (origin commit 711a002): the `@vitest/coverage-*`
     catch-all and the explicit `@vitest/coverage-v8` / `@vitest/coverage-istanbul`
     checks could both fire for the same package.json, producing duplicate tags.
     The fix gates the catch-all on "no known @vitest/coverage-* matched".
     Upstream's c624eeb rewrite converged on the same shape.

  2. pytest-cov / coverage in package.json (intentionally dropped by upstream
     in c624eeb): scanning package.json devDependencies for Python coverage
     tools is a category error. Python coverage is detected via requirements.txt,
     pyproject.toml, .coveragerc, setup.cfg, and pytest.ini -- those paths are
     covered here.

Run: python3 bin/test_dashboard.py  (from the methodology repo root)
"""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
TOOLS_DIR = THIS_DIR.parent / "tools"
sys.path.insert(0, str(TOOLS_DIR))

import methodology_dashboard as md  # noqa: E402


def pkg_label(configs):
    for c in configs:
        if "package.json" in c:
            return c
    return None


def pkg_tags(configs):
    label = pkg_label(configs)
    if label is None or "(" not in label:
        return None
    inside = label.split("(", 1)[1].rstrip(")")
    return sorted(t.strip() for t in inside.split(","))


class CoverageConfigTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.path = Path(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write_pkg(self, contents):
        (self.path / "package.json").write_text(json.dumps(contents))

    # --- Vitest no-double-counting (711a002 regression) ---

    def test_vitest_v8_single_tag(self):
        self.write_pkg({"devDependencies": {"@vitest/coverage-v8": "^1.0.0"}})
        self.assertEqual(pkg_tags(md.collect_coverage_config(self.path)),
                         ["@vitest/coverage-v8"])

    def test_vitest_istanbul_single_tag(self):
        self.write_pkg({"devDependencies": {"@vitest/coverage-istanbul": "^1.0.0"}})
        self.assertEqual(pkg_tags(md.collect_coverage_config(self.path)),
                         ["@vitest/coverage-istanbul"])

    def test_vitest_unknown_variant_uses_catchall(self):
        self.write_pkg({"devDependencies": {"@vitest/coverage-future": "^1.0.0"}})
        self.assertEqual(pkg_tags(md.collect_coverage_config(self.path)),
                         ["vitest-coverage"])

    def test_vitest_known_plus_unknown_no_double(self):
        # A known and unknown @vitest/coverage-* together: catch-all is gated off
        # because a known one matched. The unknown is intentionally silenced.
        self.write_pkg({"devDependencies": {
            "@vitest/coverage-v8": "^1.0.0",
            "@vitest/coverage-future": "^1.0.0",
        }})
        tags = pkg_tags(md.collect_coverage_config(self.path))
        self.assertEqual(tags, ["@vitest/coverage-v8"])
        self.assertNotIn("vitest-coverage", tags)

    def test_vitest_v8_and_istanbul_both_listed(self):
        self.write_pkg({"devDependencies": {
            "@vitest/coverage-v8": "^1.0.0",
            "@vitest/coverage-istanbul": "^1.0.0",
        }})
        tags = pkg_tags(md.collect_coverage_config(self.path))
        self.assertEqual(tags, ["@vitest/coverage-istanbul", "@vitest/coverage-v8"])
        self.assertNotIn("vitest-coverage", tags)

    # --- Other package.json detection paths ---

    def test_c8_detected(self):
        self.write_pkg({"devDependencies": {"c8": "^9.0.0"}})
        self.assertEqual(pkg_tags(md.collect_coverage_config(self.path)), ["c8"])

    def test_jest_top_level(self):
        self.write_pkg({"jest": {"coverageThreshold": {}}})
        self.assertEqual(pkg_tags(md.collect_coverage_config(self.path)), ["jest"])

    def test_nyc_top_level(self):
        self.write_pkg({"nyc": {}})
        self.assertEqual(pkg_tags(md.collect_coverage_config(self.path)), ["nyc"])

    def test_jest_top_level_and_c8_dep_combine(self):
        self.write_pkg({"jest": {}, "devDependencies": {"c8": "^9.0.0"}})
        self.assertEqual(pkg_tags(md.collect_coverage_config(self.path)),
                         ["c8", "jest"])

    def test_no_coverage_no_pkg_entry(self):
        self.write_pkg({"name": "x", "version": "1.0.0"})
        self.assertIsNone(pkg_label(md.collect_coverage_config(self.path)))

    def test_pytest_cov_in_devdeps_not_detected(self):
        # Documents upstream's intentional removal: pytest-cov in package.json
        # devDependencies is a category error and produces no package.json tag.
        self.write_pkg({"devDependencies": {"pytest-cov": "^4.0.0"}})
        self.assertIsNone(pkg_label(md.collect_coverage_config(self.path)))

    # --- Python coverage detection (non-package.json paths) ---

    def test_pytest_cov_in_requirements_txt(self):
        (self.path / "requirements.txt").write_text("pytest==7.0.0\npytest-cov==4.0.0\n")
        configs = md.collect_coverage_config(self.path)
        self.assertIn("requirements.txt (pytest-cov)", configs)

    def test_requirements_txt_without_pytest_cov(self):
        (self.path / "requirements.txt").write_text("flask==2.0.0\n")
        configs = md.collect_coverage_config(self.path)
        self.assertNotIn("requirements.txt (pytest-cov)", configs)

    def test_python_config_files_detected(self):
        for name in (".coveragerc", "setup.cfg", "pyproject.toml", "pytest.ini"):
            with self.subTest(name=name):
                sub = Path(tempfile.mkdtemp())
                try:
                    (sub / name).write_text("# fixture\n")
                    self.assertIn(name, md.collect_coverage_config(sub))
                finally:
                    shutil.rmtree(sub, ignore_errors=True)

    # --- vite.config.* content sniffing ---

    def test_vite_config_with_coverage_detected(self):
        (self.path / "vite.config.js").write_text(
            "export default { test: { coverage: { provider: 'v8' } } }"
        )
        self.assertIn("vite.config.js", md.collect_coverage_config(self.path))

    def test_vite_config_without_coverage_skipped(self):
        (self.path / "vite.config.js").write_text("export default { plugins: [] }")
        self.assertNotIn("vite.config.js", md.collect_coverage_config(self.path))

    # --- Recursive scanning ---

    def test_recursive_scan_finds_nested_package_json(self):
        nested = self.path / "packages" / "ui"
        nested.mkdir(parents=True)
        (nested / "package.json").write_text(json.dumps(
            {"devDependencies": {"@vitest/coverage-v8": "^1.0.0"}}
        ))
        configs = md.collect_coverage_config(self.path)
        labels = [c for c in configs if "package.json" in c]
        self.assertEqual(len(labels), 1)
        self.assertTrue(labels[0].startswith("packages/ui/package.json"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
