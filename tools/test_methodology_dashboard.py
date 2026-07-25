#!/usr/bin/env python3
"""Functional tests for methodology_dashboard.py scoring — the BL-5 doc-only reshape plus the
signal-integrity campaign (docs/planning/dashboard-signal-integrity-plan.md).

Canonical-only (NOT in bin/_manifest.py; adopters never receive it). Run:

    python3 tools/test_methodology_dashboard.py

Design notes:
- Import ONLY the tools/ module (via importlib); byte-compare the starter-kit/ twin with
  filecmp — never import it, so no starter-kit/__pycache__ is generated.
- `sys.dont_write_bytecode = True` is set before the import, so no __pycache__ at all.
- The pure scoring helpers are driven with synthetic metrics/files dicts + tempfile trees; this
  is the first functional coverage of score_health / assess_risks / the doc-only detection.
- Campaign tests are written RED-FIRST: every defect-proving assertion was run against unpatched
  code and watched to FAIL before the scanner was touched, because the suite was green against
  all eight filed and unfiled defects (a test that passes against the bug is not coverage — plan
  §8 learning 2). The remaining campaign tests are regression locks and guard-the-guard checks,
  which are expected to pass both before and after; they are marked as such where it is not
  obvious from the name.
"""

import sys
sys.dont_write_bytecode = True

import filecmp
import importlib.util
import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS_PY = os.path.join(HERE, "methodology_dashboard.py")
STARTER_PY = os.path.join(os.path.dirname(HERE), "starter-kit", "methodology_dashboard.py")

_spec = importlib.util.spec_from_file_location("methodology_dashboard_under_test", TOOLS_PY)
md = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(md)


def files(src=0, docs_loc=0, docs_count=0):
    """A minimal files["by_category"] shape for detect_doc_only."""
    return {"by_category": {"source": {"loc": src, "count": 1 if src else 0},
                            "docs": {"loc": docs_loc, "count": docs_count}}}


def base_metrics(**over):
    """A complete-enough metrics dict for score_health / assess_risks; override nested keys by
    passing a dict (shallow-merged) or replace top-level keys outright."""
    m = {
        "git": {"days_since_last_commit": 1, "total_commits": 50,
                "project_age_days": 100, "branch_count": 1},
        "tests": {"test_file_count": 0, "test_to_source_ratio": 0.0,
                  "source_loc": 0, "test_loc": 0},
        "ci": {"has_ci": False, "workflow_count": 0},
        "docs": {"readme_quality": "good", "has_docs_dir": True, "has_changelog": False,
                 "has_license": True, "has_roadmap": False, "has_todo": False,
                 "has_readme": True, "doc_to_source_ratio": 0.0, "doc_total_loc": 5000},
        "methodology": {"compliance_score": 0, "compliance_pct": 0, "items": {}},
        "coverage_configs": [],
        "changelog": {"present": False, "is_fresh": False, "signals": []},
        "files": {"largest_files": []},
        "vulnerabilities": {},
        "render": {"score": 0, "toolchain_present": False,
                   "render_dep_verified": False, "signals": []},
        "doc_only": {"is_doc_only": False, "reason": ""},
    }
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(m.get(k), dict):
            m[k] = {**m[k], **v}
        else:
            m[k] = v
    return m


def risk_descs(metrics):
    return [r["description"] for r in md.assess_risks(metrics)]


class TestDetection(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.p = Path(self._td.name)

    def tearDown(self):
        self._td.cleanup()

    def test_mixed_repo_not_doc_only(self):
        # The core constraint: a mixed tooling repo (real code that should be tested) stays code.
        r = md.detect_doc_only(self.p, files(src=4500, docs_loc=900, docs_count=40),
                               {"toolchain_present": False})
        self.assertFalse(r["is_doc_only"])
        self.assertEqual(r["reason"], "heuristic")

    def test_markdown_research_is_doc_only(self):
        r = md.detect_doc_only(self.p, files(src=0, docs_loc=800, docs_count=12),
                               {"toolchain_present": False})
        self.assertTrue(r["is_doc_only"])
        self.assertEqual(r["reason"], "heuristic")

    def test_pure_latex_research_via_toolchain(self):
        # .tex/.qmd aren't counted as docs, so doc_loc≈0; only toolchain_present rescues it.
        r = md.detect_doc_only(self.p, files(src=0, docs_loc=0, docs_count=0),
                               {"toolchain_present": True})
        self.assertTrue(r["is_doc_only"])

    def test_empty_repo_not_doc_only(self):
        r = md.detect_doc_only(self.p, files(0, 0, 0), {"toolchain_present": False})
        self.assertFalse(r["is_doc_only"])

    def test_source_cap_boundary(self):
        render = {"toolchain_present": False}
        self.assertTrue(md.detect_doc_only(self.p, files(src=200, docs_count=5), render)["is_doc_only"])
        self.assertFalse(md.detect_doc_only(self.p, files(src=201, docs_count=5), render)["is_doc_only"])

    def test_marker_code_forces_not_doc_only(self):
        (self.p / md.DOC_ONLY_MARKER).write_text("code\n")
        r = md.detect_doc_only(self.p, files(src=0, docs_loc=800, docs_count=12),
                               {"toolchain_present": True})
        self.assertFalse(r["is_doc_only"])
        self.assertEqual(r["reason"], "marker")

    def test_marker_doc_only_forces_doc_only(self):
        (self.p / md.DOC_ONLY_MARKER).write_text("doc-only\n")
        r = md.detect_doc_only(self.p, files(src=4500, docs_loc=0, docs_count=0),
                               {"toolchain_present": False})
        self.assertTrue(r["is_doc_only"])
        self.assertEqual(r["reason"], "marker")

    def test_marker_unknown_token_falls_through(self):
        (self.p / md.DOC_ONLY_MARKER).write_text("banana\n")
        r = md.detect_doc_only(self.p, files(src=4500), {"toolchain_present": False})
        self.assertFalse(r["is_doc_only"])
        self.assertEqual(r["reason"], "heuristic")

    def test_marker_with_utf8_bom_is_honored(self):
        # A BOM-prefixed marker (Notepad-authored) must still be read as the token, not silently
        # dropped to the heuristic (which would flip to the opposite of the owner's request).
        (self.p / md.DOC_ONLY_MARKER).write_bytes(b"\xef\xbb\xbfcode\n")
        r = md.detect_doc_only(self.p, files(src=0, docs_loc=800, docs_count=12),
                               {"toolchain_present": True})
        self.assertFalse(r["is_doc_only"])
        self.assertEqual(r["reason"], "marker")


class TestRenderMetrics(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.p = Path(self._td.name)
        self.files = files(src=0, docs_loc=800, docs_count=12)
        self.ci = {"workflow_files": []}
        self.meth = {"items": {}}

    def tearDown(self):
        self._td.cleanup()

    def _score(self):
        return md.collect_render_metrics(self.p, self.files, self.ci, self.meth)

    def test_none_scores_zero(self):
        r = self._score()
        self.assertEqual(r["score"], 0)
        self.assertFalse(r["toolchain_present"])
        self.assertFalse(r["render_dep_verified"])

    def test_toolchain_only(self):
        (self.p / "_quarto.yml").write_text("project:\n  type: book\n")
        r = self._score()
        self.assertTrue(r["toolchain_present"])
        self.assertEqual(r["score"], 4)  # +4 toolchain, no driver/dep/ci/artifact

    def test_render_dep_check_flag(self):
        (self.p / "Makefile").write_text("render:\n\tpdffonts out.pdf\n")
        r = self._score()
        self.assertTrue(r["render_dep_verified"])   # pdffonts token
        # +2 driver (Makefile) +4 dep check = 6
        self.assertEqual(r["score"], 6)

    def test_all_signals_score_twenty(self):
        (self.p / "_quarto.yml").write_text("format:\n  pdf:\n    mainfont: TeX Gyre\n")
        (self.p / "Makefile").write_text("all:\n\tquarto render\n\tpdffonts out.pdf\n")
        (self.p / ".lycheeignore").write_text("http://x\n")
        (self.p / "CITATION.cff").write_text("cff-version: 1.2.0\n")
        (self.p / "RESEARCH_DOCUMENTATION_WORKSTREAM.md").write_text("# ws\n")
        r = self._score()
        # A: toolchain 4 + driver 2 | B: pdffonts 4 + mainfont 2 | C: render-ci 3 + lychee 2
        # | D: CITATION.cff 2 + workstream 1  => 20
        self.assertEqual(r["score"], 20)

    def test_score_capped_at_twenty(self):
        # Even with redundant signals the score never exceeds 20.
        (self.p / "_quarto.yml").write_text("mainfont: X\n")
        (self.p / "Makefile").write_text("quarto render\npdffonts a\nfc-list\nkpsewhich b\n")
        (self.p / ".lycheeignore").write_text("x\n")
        (self.p / "lychee.toml").write_text("x\n")
        (self.p / "CITATION.cff").write_text("x\n")
        (self.p / "refs.bib").write_text("@book{a}\n")
        (self.p / "RESEARCH_DOCUMENTATION_WORKSTREAM.md").write_text("x\n")
        # Exact-value lock (not the tautological `<= 20`): redundant signals must still land on 20,
        # so a broken bucket weight / regex / double-count moves it off 20 and fails.
        self.assertEqual(self._score()["score"], 20)


class TestScoreHealth(unittest.TestCase):
    def test_doc_only_fills_testing_slot_with_render_score(self):
        m = base_metrics(doc_only={"is_doc_only": True}, render={"score": 14})
        self.assertEqual(md.score_health(m)["testing"], 14)

    def test_code_repo_testing_ladder_regression_lock(self):
        # ratio 0.35 -> 16 on the classic ladder; must be unchanged for a code repo.
        m = base_metrics(tests={"test_to_source_ratio": 0.35, "test_file_count": 5, "source_loc": 1000})
        self.assertEqual(md.score_health(m)["testing"], 16)

    def test_all_dims_bounded_and_total_is_sum(self):
        for m in (base_metrics(doc_only={"is_doc_only": True}, render={"score": 11}),
                  base_metrics(tests={"test_to_source_ratio": 0.6, "test_file_count": 9, "source_loc": 500})):
            s = md.score_health(m)
            dims = ["activity", "testing", "documentation", "ci_cd", "methodology"]
            for d in dims:
                self.assertGreaterEqual(s[d], 0)
                self.assertLessEqual(s[d], 20)
            self.assertEqual(s["total"], sum(s[d] for d in dims))
            self.assertLessEqual(s["total"], 100)


class TestRiskReshaping(unittest.TestCase):
    def test_no_test_infra_suppressed_when_doc_only(self):
        m = base_metrics(doc_only={"is_doc_only": True},
                         render={"score": 0}, tests={"test_file_count": 0, "source_loc": 0})
        descs = risk_descs(m)
        self.assertNotIn("No test infrastructure", descs)
        self.assertTrue(any("no detectable render/verification pipeline" in d for d in descs))

    def test_no_test_infra_kept_for_mixed_repo(self):
        m = base_metrics(tests={"test_file_count": 0, "source_loc": 3000})
        self.assertIn("No test infrastructure", risk_descs(m))

    def test_helper_loc_risk_when_doc_only_has_small_source(self):
        m = base_metrics(doc_only={"is_doc_only": True},
                         render={"score": 8, "toolchain_present": True, "render_dep_verified": True},
                         tests={"test_file_count": 0, "source_loc": 150})
        self.assertTrue(any("150 LOC of helper source" in d for d in risk_descs(m)))

    def test_large_file_ext_filter(self):
        doc_big = base_metrics(files={"largest_files": [{"loc": 2500, "ext": ".md", "path": "chap.md"}]})
        self.assertFalse(any("Large files detected" in d for d in risk_descs(doc_big)))
        src_big = base_metrics(files={"largest_files": [{"loc": 2500, "ext": ".py", "path": "big.py"}]})
        self.assertTrue(any("Large files detected" in d for d in risk_descs(src_big)))

    def test_large_file_source_not_masked_by_nonsource_number_one(self):
        # A big lockfile/JSON at rank #1 must not hide a genuine large source file below it.
        m = base_metrics(files={"largest_files": [
            {"loc": 15000, "ext": ".json", "path": "package-lock.json"},
            {"loc": 3000, "ext": ".py", "path": "app.py"},
        ]})
        descs = risk_descs(m)
        self.assertTrue(any("Large files detected" in d and "app.py" in d for d in descs))

    def test_render_dep_advisory_fires_when_toolchain_unverified(self):
        # anti-pattern #20: toolchain present but no post-render dependency check wired.
        m = base_metrics(doc_only={"is_doc_only": True},
                         render={"score": 6, "toolchain_present": True, "render_dep_verified": False},
                         tests={"test_file_count": 0, "source_loc": 0})
        self.assertTrue(any("no post-render dependency check" in d for d in risk_descs(m)))

    def test_render_dep_advisory_silent_when_verified(self):
        m = base_metrics(doc_only={"is_doc_only": True},
                         render={"score": 12, "toolchain_present": True, "render_dep_verified": True},
                         tests={"test_file_count": 0, "source_loc": 0})
        self.assertFalse(any("no post-render dependency check" in d for d in risk_descs(m)))


# --- Signal-integrity campaign, Layer 1 (defects 1, 2, 8) -------------------------------------

# The raw weighted sum, computed HERE from the checklist rather than read from the module, so
# these assertions can be driven against unpatched code (which has no METHODOLOGY_MAX at all).
RAW_MAX = sum(w for _, w, _ in md.METHODOLOGY_ITEMS)

# Adopter-root files that bin/_manifest.py distributes but that are deliberately NOT compliance
# checklist items. Every exemption states WHY, so the structural guard below fails loudly the
# next time a distributed artifact is added without a decision — which is exactly how HANDOFFS.md
# (SEED since v3.3) went two releases unscored. Kept here rather than in the scanner: the manifest
# is canonical-only, so an adopter's copy of the dashboard has nothing to check it against.
CHECKLIST_EXEMPT = {
    "RECOMMENDED_SKILLS.md": "index of optional skill recommendations; using them is elective, "
                             "so its presence says nothing about methodology adoption",
    "CONTEXT_TEMPLATE.md": "template; the operating artifact is the adopter's CONTEXT.md instance",
    "CLAUDE_TEMPLATE.md": "template; the operating artifact is the adopter's CLAUDE.md instance",
    "BOOTSTRAP.md": "one-time setup guide, not a per-session operating artifact",
    "methodology_dashboard.py": "the scanner itself — scoring its own presence is circular",
}


def manifest_adopter_root_dests():
    """Adopter-ROOT destinations from bin/_manifest.py (dests with no directory component)."""
    manifest_path = os.path.join(os.path.dirname(HERE), "bin", "_manifest.py")
    spec = importlib.util.spec_from_file_location("methodology_manifest_under_test", manifest_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return [dest for _src, dest, _disp in mod.DISTRIBUTION if "/" not in dest]


def full_compliance_tree(p):
    """Create every METHODOLOGY_ITEMS artifact under `p` — a 100%-compliant adopter."""
    for item_path, _w, kind in md.METHODOLOGY_ITEMS:
        target = p / item_path
        if kind == "dir":
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"# {item_path}\n")


class TestComplianceScaleIsHonest(unittest.TestCase):
    """Defects 1 & 2: a 110-point weighted sum was rendered as a percentage and fed an
    UNCLAMPED health dimension, so a fully-compliant adopter's card read 'Methodology
    Compliance (110%)' over a 22/20 sub-score and a 102/100 total."""

    def test_max_is_derived_from_the_checklist_never_a_literal(self):
        # A hardcoded denominator is what drifted in the first place (v2.1 appended two 5-point
        # items to a scale cut for exactly 100), so the constant must be computed, not written.
        self.assertEqual(md.METHODOLOGY_MAX, RAW_MAX)
        self.assertEqual(md.METHODOLOGY_MAX, sum(w for _, w, _ in md.METHODOLOGY_ITEMS))

    def test_full_compliance_is_100_percent_not_the_raw_sum(self):
        self.assertEqual(md.compliance_pct(RAW_MAX), 100)
        self.assertEqual(md.compliance_pct(0), 0)
        self.assertLessEqual(md.compliance_pct(RAW_MAX), 100)

    def test_methodology_dimension_is_clamped_to_its_band(self):
        # Driven at full compliance: today int(110 * 0.2) == 22 in a 0-20 band, and the
        # "0-100" total reaches 102.
        m = base_metrics(methodology={"compliance_score": RAW_MAX, "compliance_pct": 100})
        s = md.score_health(m)
        self.assertEqual(s["methodology"], 20)
        self.assertLessEqual(s["total"], 100)

    def test_dimension_reads_the_normalized_percent_at_intermediate_values(self):
        """The endpoints cannot tell the two readings apart — at 0 both give 0, and at full
        compliance the clamp alone yields 20 either way. So a suite driven only at 0% and 100%
        stays green against a dimension that clamps but never normalizes, which is where every
        partially-compliant repo (i.e. the whole adopter fleet) actually lives. Verified by
        mutation: reading compliance_score instead of compliance_pct at the dimension survived
        all 44 tests before this lock existed."""
        discriminating = 0
        for raw in range(0, md.METHODOLOGY_MAX + 1, 5):
            pct = md.compliance_pct(raw)
            m = base_metrics(methodology={"compliance_score": raw, "compliance_pct": pct})
            got = md.score_health(m)["methodology"]
            self.assertEqual(got, int(pct * 0.2), f"dimension is not the normalized pct at raw={raw}")
            self.assertLessEqual(got, 20, f"dimension escaped its band at raw={raw}")
            if got != min(20, int(raw * 0.2)):
                discriminating += 1
        # Guard the guard: if no sampled value separated the two readings, the loop above would
        # be green against the unnormalized implementation and prove nothing.
        self.assertGreater(discriminating, 0,
                           "no sampled value distinguishes the normalized read from the raw sum")

    def test_clamp_holds_even_if_the_percentage_is_out_of_range(self):
        # Defense in depth: normalization makes >100 unreachable through the producer, so the
        # clamp is only load-bearing if compliance_pct is ever wrong. Drive it directly.
        m = base_metrics(methodology={"compliance_score": 999, "compliance_pct": 150})
        self.assertEqual(md.score_health(m)["methodology"], 20)

    def test_no_dimension_or_total_escapes_its_band_at_full_compliance(self):
        m = base_metrics(methodology={"compliance_score": RAW_MAX, "compliance_pct": 100},
                         tests={"test_to_source_ratio": 0.6, "test_file_count": 9, "source_loc": 500},
                         ci={"has_ci": True, "workflow_count": 3},
                         docs={"readme_quality": "excellent", "has_docs_dir": True,
                               "has_changelog": True, "has_license": True,
                               "has_roadmap": True, "has_todo": True},
                         changelog={"present": True, "is_fresh": True, "signals": []})
        s = md.score_health(m)
        for dim in ("activity", "testing", "documentation", "ci_cd", "methodology"):
            self.assertLessEqual(s[dim], 20, f"{dim} escaped its 0-20 band")
        self.assertEqual(s["total"], 100)

    def test_partial_adoption_risk_states_the_normalized_percent(self):
        raw = 52
        pct = md.compliance_pct(raw)
        m = base_metrics(methodology={"compliance_score": raw, "compliance_pct": pct})
        descs = risk_descs(m)
        self.assertTrue(any(f"Partial methodology adoption ({pct}%)" in d for d in descs),
                        f"expected the normalized percent in the risk text; got {descs}")
        if pct != raw:  # the two coincide only if the checklist is ever re-cut to sum 100
            self.assertFalse(any(f"({raw}%)" in d for d in descs),
                             "the raw weighted sum must not be rendered as a percentage")

    def test_zero_adoption_test_reads_the_raw_sum_not_the_percentage(self):
        # Scale-independence: a single small-weight item in a future larger checklist can round
        # to 0% — it must NOT be reported as "no methodology adoption".
        m = base_metrics(methodology={"compliance_score": 0, "compliance_pct": 0})
        self.assertTrue(any("No methodology adoption" in d for d in risk_descs(m)))
        some = base_metrics(methodology={"compliance_score": 5, "compliance_pct": 0})
        descs = risk_descs(some)
        self.assertFalse(any("No methodology adoption" in d for d in descs))
        self.assertTrue(any("Partial methodology adoption" in d for d in descs))


class TestChecklistCurrency(unittest.TestCase):
    """Defect 8: HANDOFFS.md has shipped to adopters as a SEED since v3.3 (bin/_manifest.py:47)
    and was never added to the compliance checklist. The structural guard turns that one-off
    omission into an invariant, so the next distributed artifact cannot repeat it."""

    def test_handoffs_is_a_checklist_item_weighted_like_its_twin(self):
        by_path = {p: (w, kind) for p, w, kind in md.METHODOLOGY_ITEMS}
        self.assertIn("HANDOFFS.md", by_path)
        self.assertEqual(by_path["HANDOFFS.md"], by_path["CHANGELOG.md"],
                         "HANDOFFS.md and CHANGELOG.md are structural twins (both SEED, both "
                         "lifetime-stable) and must carry the same weight and kind")

    def test_every_distributed_adopter_root_file_is_scored_or_exempt(self):
        checklist = {p for p, _w, _k in md.METHODOLOGY_ITEMS}
        unaccounted = [d for d in manifest_adopter_root_dests()
                       if d not in checklist and d not in CHECKLIST_EXEMPT]
        self.assertEqual(unaccounted, [],
                         "distributed adopter-root file(s) neither on METHODOLOGY_ITEMS nor in "
                         "CHECKLIST_EXEMPT — add the item or record why it is not scored")

    def test_exemptions_are_real_manifest_entries_with_a_reason(self):
        # Guard the guard: a stale exemption would silently weaken the invariant above.
        dests = set(manifest_adopter_root_dests())
        for name, reason in CHECKLIST_EXEMPT.items():
            self.assertIn(name, dests, f"CHECKLIST_EXEMPT lists {name}, which is not distributed")
            self.assertTrue(reason.strip(), f"exemption for {name} states no reason")


class TestMethodologyGridAlignment(unittest.TestCase):
    """Load-bearing, not cosmetic: the header row was hand-written at six item columns while the
    cells derive from METHODOLOGY_ITEMS, so v2.1's two added items have silently run every
    project row wider than its headers ever since."""

    def test_headers_are_derived_from_the_checklist(self):
        headers = md.methodology_grid_headers()
        self.assertEqual(len(headers), len(md.METHODOLOGY_ITEMS) + 2)  # Project + items + Score
        self.assertEqual(headers[0], "Project")
        self.assertEqual(headers[-1], "Score")

    def test_derived_labels_are_pinned_exactly(self):
        # Pinned in full rather than spot-checked, so a wording change is never invisible. Note
        # the one deliberate rename: the hand-written row's "Workstreams" becomes "Workstreams
        # Dir", matching the "Methodology Dir" convention for the two directory items. It cost
        # nothing to change because the hand-written headers were misaligned anyway — with 8
        # headers over 10 cells, "Workstreams" was sitting above the ROADMAP.md column.
        self.assertEqual(md.methodology_grid_headers(), [
            "Project", "Session Runner", "Safeguards", "Session Notes", "Backlog",
            "Changelog", "Handoffs", "Roadmap", "Methodology Dir", "Workstreams Dir", "Score",
        ])

    def test_rendered_grid_has_one_header_per_cell(self):
        p = {"name": "demo",
             "methodology": {"items": {k: True for k, _w, _k in md.METHODOLOGY_ITEMS},
                             "compliance_score": RAW_MAX, "compliance_pct": 100}}
        html = md.render_methodology_grid([p])
        self.assertEqual(html.count("<th>"), len(md.METHODOLOGY_ITEMS) + 2)
        row = html.split("<tbody>")[1]
        self.assertEqual(row.count("<td"), len(md.METHODOLOGY_ITEMS) + 2)
        self.assertEqual(html.count("<th>"), row.count("<td"),
                         "header row and project row must be the same width")

    def test_grid_renders_the_percentage_not_the_raw_sum(self):
        p = {"name": "demo",
             "methodology": {"items": {k: True for k, _w, _k in md.METHODOLOGY_ITEMS},
                             "compliance_score": RAW_MAX, "compliance_pct": 100}}
        html = md.render_methodology_grid([p])
        self.assertIn(">100%<", html)
        if RAW_MAX != 100:  # they coincide only if the checklist is ever re-cut to sum 100
            self.assertNotIn(f">{RAW_MAX}%<", html)


class TestHistoryVersionStamp(unittest.TestCase):
    """Residual risk 1: dashboard_history.jsonl persists only derived totals with no scale
    marker, and the trend renderer diffs first-vs-last — so a one-time scoring change renders
    as a red regression arrow indistinguishable from a real one. The stamp is what makes the
    discontinuity interpretable."""

    def test_history_entry_records_the_dashboard_version(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            portfolio = {"health_score": 70, "project_count": 1, "total_commits": 5,
                         "risk_counts": {}}
            projects = [{"name": "demo",
                         "scores": {"health": {"total": 70}, "risks": [], "activity": "active"},
                         "git": {"total_commits": 5}, "tests": {"test_file_count": 2}}]
            md.append_history(root, portfolio, projects)
            line = (root / md.HISTORY_FILE).read_text().strip()
            entry = json.loads(line)
            self.assertEqual(entry.get("dashboard_version"), md.DASHBOARD_VERSION)


class TestFmtRatioAndTwins(unittest.TestCase):
    def test_fmt_ratio(self):
        self.assertEqual(md.fmt_ratio(0.0, 0, True), "n/a (doc-only)")    # actually doc-only
        self.assertEqual(md.fmt_ratio(0.0, 0, False), "n/a (no source)")  # code repo, no source
        self.assertNotIn("doc-only", md.fmt_ratio(0.0, 0))                # default is NOT doc-only
        self.assertEqual(md.fmt_ratio(0.25, 400, False), "0.250")

    def test_twins_byte_identical(self):
        self.assertTrue(filecmp.cmp(TOOLS_PY, STARTER_PY, shallow=False),
                        "tools/ and starter-kit/ dashboards must be byte-identical")

    def test_dashboard_version(self):
        self.assertEqual(md.DASHBOARD_VERSION, "2.9.0")
        starter_src = Path(STARTER_PY).read_text(encoding="utf-8")
        self.assertTrue(re.search(r'^DASHBOARD_VERSION\s*=\s*"2\.9\.0"', starter_src, re.MULTILINE),
                        "starter-kit twin must also declare DASHBOARD_VERSION 2.9.0")


class TestEndToEnd(unittest.TestCase):
    """Exercise the WIRED path (collect_all -> render/detect/score/risk + render_project_card) so a
    wiring or card-display regression cannot pass while every pure-helper test stays green."""

    def _repo(self, files_map):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        p = Path(td.name)
        subprocess.run(["git", "init", "-q", str(p)], check=True)
        for name, content in files_map.items():
            fp = p / name
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)
        subprocess.run(["git", "-C", str(p), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(p), "-c", "user.email=t@t", "-c", "user.name=t",
                        "commit", "-q", "-m", "init"], check=True)
        return p

    def test_doc_only_tree_end_to_end(self):
        p = self._repo({
            "chapter1.md": "# Ch1\n" + "prose line\n" * 400,
            "chapter2.md": "# Ch2\n" + "prose line\n" * 400,
            "_quarto.yml": "format:\n  pdf:\n    mainfont: TeX Gyre\n",
            "Makefile": "render:\n\tquarto render\n\tpdffonts out.pdf\n",
        })
        m = md.collect_all(p)
        self.assertTrue(m["doc_only"]["is_doc_only"])
        # The Testing slot is filled by the render score end to end.
        self.assertEqual(m["scores"]["health"]["testing"], m["render"]["score"])
        self.assertGreater(m["render"]["score"], 0)
        self.assertFalse(any("No test infrastructure" in r["description"]
                             for r in m["scores"]["risks"]))
        card = md.render_project_card(m)
        self.assertIn("Render / Verification (proxy)", card)
        self.assertIn("infrastructure proxy", card)
        self.assertNotIn("<h4>Testing</h4>", card)

    def test_full_compliance_tree_end_to_end_never_exceeds_100(self):
        """The live blast radius (plan §2.1): an adopter with every checklist artifact scored
        compliance 110 -> methodology 22/20 -> total 90/100, and its card read '110%'."""
        p = self._repo({"README.md": "# demo\n" * 60})
        full_compliance_tree(p)
        subprocess.run(["git", "-C", str(p), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(p), "-c", "user.email=t@t", "-c", "user.name=t",
                        "commit", "-q", "-m", "compliance"], check=True)
        m = md.collect_all(p)

        self.assertEqual(m["methodology"]["missing_files"], [])
        self.assertEqual(m["methodology"]["compliance_score"], md.METHODOLOGY_MAX)
        self.assertEqual(m["methodology"]["compliance_pct"], 100)
        self.assertEqual(m["scores"]["health"]["methodology"], 20)
        self.assertLessEqual(m["scores"]["health"]["total"], 100)

        card = md.render_project_card(m)
        self.assertIn(f"Methodology Compliance (100% ({md.METHODOLOGY_MAX} of "
                      f"{md.METHODOLOGY_MAX}))", card)
        self.assertNotIn(f"Methodology Compliance ({md.METHODOLOGY_MAX}%)", card)
        self.assertIn("HANDOFFS.md", card)
        self.assertFalse(any("methodology adoption" in r["description"]
                             for r in m["scores"]["risks"]))

    def test_pre_v33_adopter_tree_end_to_end(self):
        """Ratified decision D2's accepted cost, driven end to end: an adopter that has every
        checklist artifact EXCEPT HANDOFFS.md (the shape of every project seeded before v3.3)
        scores below 100% until it re-seeds — and the shortfall it is told about is exactly the
        weight of the file it is missing."""
        p = self._repo({"README.md": "# demo\n" * 60})
        full_compliance_tree(p)
        (p / "HANDOFFS.md").unlink()
        subprocess.run(["git", "-C", str(p), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(p), "-c", "user.email=t@t", "-c", "user.name=t",
                        "commit", "-q", "-m", "pre-v3.3"], check=True)
        m = md.collect_all(p)
        handoffs_weight = next(w for path, w, _ in md.METHODOLOGY_ITEMS if path == "HANDOFFS.md")

        self.assertEqual(m["methodology"]["missing_files"], ["HANDOFFS.md"])
        self.assertEqual(m["methodology"]["compliance_score"],
                         md.METHODOLOGY_MAX - handoffs_weight)
        self.assertLess(m["methodology"]["compliance_pct"], 100)
        # Still a healthy repo: the missing seed costs at most one point of the 0-20 dimension.
        self.assertGreaterEqual(m["scores"]["health"]["methodology"], 19)
        self.assertLessEqual(m["scores"]["health"]["total"], 100)
        self.assertFalse(any("methodology adoption" in r["description"]
                             for r in m["scores"]["risks"]))

    def test_code_tree_end_to_end_keeps_testing(self):
        p = self._repo({
            "app.py": "def f():\n    return 1\n" * 150,   # ~300 source LOC -> over the 200 cap
            "test_app.py": "def test_f():\n    assert True\n" * 10,
            "README.md": "# app\n" * 5,
        })
        m = md.collect_all(p)
        self.assertFalse(m["doc_only"]["is_doc_only"])
        card = md.render_project_card(m)
        self.assertIn("<h4>Testing</h4>", card)
        self.assertNotIn("Render / Verification", card)


if __name__ == "__main__":
    unittest.main(verbosity=2)
