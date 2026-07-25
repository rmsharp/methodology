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


# --- Signal-integrity campaign, Layer 2 (defects 5, 6, 7) -------------------------------------


def write_tree(p, files_map):
    """Materialize {relative path: content} under `p`, creating parent directories."""
    for name, content in files_map.items():
        fp = p / name
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content)


def git_repo(case, files_map, extra_commits=0, tail_files=None, dates=None):
    """A temp git repo with controllable history DEPTH and DATES.

    `files_map` lands in the first commit, then `extra_commits` empty commits, then `tail_files`
    in a final commit — which is how a test places a file at a chosen distance from HEAD (the
    lag signals are computed from `git log -1 -- <file>` against HEAD). `dates`, when given, is
    an (author_date_for_first, author_date_for_the_rest) pair so day-lag can be exercised
    without waiting three weeks.
    """
    td = tempfile.TemporaryDirectory()
    case.addCleanup(td.cleanup)
    p = Path(td.name)
    subprocess.run(["git", "init", "-q", str(p)], check=True)

    def commit(msg, when=None):
        env = dict(os.environ)
        if when:
            env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = when
        subprocess.run(["git", "-C", str(p), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(p), "-c", "user.email=t@t", "-c", "user.name=t",
                        "commit", "-q", "--allow-empty", "-m", msg], check=True, env=env)

    first_date, rest_date = dates if dates else (None, None)
    write_tree(p, files_map)
    commit("init", first_date)
    for i in range(extra_commits):
        commit(f"filler {i}", rest_date)
    if tail_files:
        write_tree(p, tail_files)
        commit("tail", rest_date)
    return p


class TestLedgerLocators(unittest.TestCase):
    """Defects 5 & 7. One locator was answering two different questions: *is there a changelog to
    measure freshness against* (best-available — root or `docs/`, name-prefix, case-insensitive)
    and *does this repo keep an action ledger* (root `CHANGELOG.md`, exactly — what
    METHODOLOGY_ITEMS already probes). Conflating them let a `docs/` product changelog answer the
    membership question, so the adopter that had no ledger at all was never told so."""

    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.p = Path(self._td.name)

    def tearDown(self):
        self._td.cleanup()

    # -- membership: _find_action_ledger, root-anchored and exact (RED: no such function today)
    def test_the_action_ledger_is_the_root_changelog(self):
        write_tree(self.p, {"CHANGELOG.md": "# ledger\n"})
        self.assertEqual(md._find_action_ledger(self.p), self.p / "CHANGELOG.md")

    def test_a_docs_changelog_is_not_an_action_ledger(self):
        write_tree(self.p, {"docs/changelog.md": "# product release notes\n"})
        self.assertIsNone(md._find_action_ledger(self.p))

    def test_an_archive_is_not_an_action_ledger(self):
        write_tree(self.p, {"CHANGELOG-archive.md": "# frozen history\n"})
        self.assertIsNone(md._find_action_ledger(self.p))

    def test_a_changelog_directory_is_not_an_action_ledger(self):
        # Mirrors _find_changelog's is_file() guard: a CHANGELOG/ directory is not a ledger.
        (self.p / "CHANGELOG.md").mkdir()
        self.assertIsNone(md._find_action_ledger(self.p))

    def test_membership_agrees_with_the_compliance_checklist_probe(self):
        """Guard the guard, by CALLING the checklist rather than re-implementing it — a guard that
        restates the thing it is guarding cannot detect the two drifting apart."""
        for tree, expected in (({"CHANGELOG.md": "x"}, True),
                               ({"docs/changelog.md": "x"}, False),
                               ({"CHANGELOG-archive.md": "x"}, False),
                               # A lowercase root file has no platform-independent answer: a
                               # case-insensitive filesystem satisfies the CHANGELOG.md probe and a
                               # case-sensitive one does not (plan §7 residual risk 6, pre-existing
                               # and out of scope). Whatever the platform answers, the invariant
                               # under test is that BOTH probes answer it the same way.
                               ({"changelog.md": "x"}, None)):
            with tempfile.TemporaryDirectory() as td:
                p = Path(td)
                write_tree(p, tree)
                ledger = md._find_action_ledger(p) is not None
                checklist = md.collect_methodology_metrics(p)["items"]["CHANGELOG.md"]
                self.assertEqual(ledger, checklist,
                                 f"the two probes must answer alike; tree={tree}")
                if expected is not None:
                    self.assertEqual(ledger, expected, tree)

    def test_the_one_documented_divergence_from_the_checklist_probe(self):
        # The checklist probes a bare exists(), so a CHANGELOG.md DIRECTORY scores as present for
        # compliance while it is correctly not a ledger. Pinned so the docstring's claim of "the
        # same question, one deliberate difference" stays true, and so the divergence cannot grow
        # silently.
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p / "CHANGELOG.md").mkdir()
            self.assertTrue(md.collect_methodology_metrics(p)["items"]["CHANGELOG.md"])
            self.assertIsNone(md._find_action_ledger(p))

    # -- location: _find_changelog, defect 7 (archive shadowing)
    def test_an_exact_changelog_wins_over_an_archive_sibling(self):
        # 'CHANGELOG-archive.md' sorts BEFORE 'CHANGELOG.md' ('-' is 0x2D, '.' is 0x2E), so the
        # sorted()-first locator measured freshness against a deliberately frozen file and then
        # reported it as lagging.
        write_tree(self.p, {"CHANGELOG.md": "# ledger\n", "CHANGELOG-archive.md": "# frozen\n"})
        self.assertEqual(md._find_changelog(self.p), self.p / "CHANGELOG.md")

    def test_root_precedence_outranks_the_exact_name_across_bases(self):
        """CHARACTERIZATION — this pins a LIMITATION, not a fix, so it cannot change by accident.
        The exact-name preference is scoped within a base, so a root holding only a frozen archive
        still shadows an exact `docs/CHANGELOG.md`. Hoisting the preference across bases would fix
        this arrangement, but the same hoist would silently move which file is measured — and with
        it the ±1 freshness point — for the neighbouring shape pinned in the test below, where a
        non-`.md` root changelog coexists with an exact `docs/CHANGELOG.md` and nothing is being
        shadowed at all. D3 exists precisely because a fix that quietly moves a score it claimed
        not to touch is how this class of defect propagates, so the narrower reading shipped and
        this arrangement was left as it was."""
        write_tree(self.p, {"CHANGELOG-archive.md": "# frozen\n", "docs/CHANGELOG.md": "# live\n"})
        self.assertEqual(md._find_changelog(self.p), self.p / "CHANGELOG-archive.md")

    def test_a_non_md_root_changelog_still_outranks_docs(self):
        # The behavior a cross-base hoist would have changed, pinned so it cannot: root wins, and
        # nothing about this tree involves an archive or any defect this layer fixes.
        write_tree(self.p, {"CHANGELOG.rst": "# root\n", "docs/CHANGELOG.md": "# docs\n"})
        self.assertEqual(md._find_changelog(self.p), self.p / "CHANGELOG.rst")

    def test_a_lowercase_exact_changelog_is_preferred_over_an_archive(self):
        # _find_changelog is documented as case-insensitive (it mirrors has_changelog), so the
        # exact-match preference must be too, or the shadowing simply persists for changelog.md
        # ('C' 0x43 sorts before 'c' 0x63).
        write_tree(self.p, {"changelog.md": "# live\n", "CHANGELOG-archive.md": "# frozen\n"})
        self.assertEqual(md._find_changelog(self.p), self.p / "changelog.md")

    def test_the_prefix_fallback_survives(self):
        # Regression lock: the prefix search is the FALLBACK, not removed. A repo whose only
        # changelog is CHANGELOG.rst is still located and measured.
        write_tree(self.p, {"CHANGELOG.rst": "# rst\n"})
        self.assertEqual(md._find_changelog(self.p), self.p / "CHANGELOG.rst")

    def test_a_root_prefix_match_is_returned_even_when_a_docs_base_exists(self):
        """The test above gives the repo no `docs/` directory at all, so it exercises only the
        single-base path — a rewrite that mishandled the second base could not fail it. The far
        more common shape is a root changelog plus an ordinary `docs/` tree, and that is what this
        pins: the root prefix match is returned, and the presence of a second base does not cost
        the repo its changelog — which would cost the +1 freshness point and silence every
        Component-C advisory, but NOT the +1 presence point, since that comes from
        `collect_doc_metrics.has_changelog`, an independent scan D3 leaves untouched. (Conflating
        those two is the very thing this layer exists to stop doing.) This began as a
        cross-base-accumulation lock against an implementation that carried
        a `fallback` across bases; the shipped locator resolves per base and returns before `docs/`
        is scanned, so what survives here is the behavior, not the original mechanism."""
        write_tree(self.p, {"CHANGELOG.rst": "# rst\n", "docs/guide.md": "# guide\n"})
        self.assertEqual(md._find_changelog(self.p), self.p / "CHANGELOG.rst")

    def test_root_precedence_is_unchanged_when_both_are_exact(self):
        # Regression lock: preferring an exact match must not reorder the bases.
        write_tree(self.p, {"CHANGELOG.md": "# root\n", "docs/CHANGELOG.md": "# docs\n"})
        self.assertEqual(md._find_changelog(self.p), self.p / "CHANGELOG.md")

    def test_the_two_locators_disagree_on_purpose(self):
        """The dual predicate stated as one assertion: the same tree answers YES to location and
        NO to membership. If these two ever collapse into one answer, defect 5 is back."""
        write_tree(self.p, {"docs/changelog.md": "# product release notes\n"})
        self.assertIsNotNone(md._find_changelog(self.p))
        self.assertIsNone(md._find_action_ledger(self.p))


class TestSignalReachability(unittest.TestCase):
    """Defect 6: Signal F (unmigrated `BACKLOG.md` done-marks) was emitted BELOW the
    `changelog is None` early return, so an adopter with 60 unmigrated done-marks and no ledger
    at all — strictly the worse case — received FEWER warnings than one with a ledger. A correct
    assertion over an input that never executes is issue #61's own failure mode."""

    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.p = Path(self._td.name)

    def tearDown(self):
        self._td.cleanup()

    def _freshness(self, files_map, commits=50):
        write_tree(self.p, files_map)
        return md.evaluate_changelog_freshness(
            self.p, {"total_commits": commits, "days_since_last_commit": 1})

    def test_the_backlog_signal_fires_with_no_changelog_at_all(self):
        r = self._freshness({"SESSION_RUNNER.md": "# runner\n",
                             "BACKLOG.md": "- [x] shipped\n" * 60})
        self.assertFalse(r["present"])
        self.assertEqual(r["backlog_done_unmigrated"], 60)
        self.assertTrue(any("not migrated" in d for _sev, d in r["signals"]),
                        "Signal F must not depend on an unrelated file existing")

    def test_the_backlog_signal_still_fires_with_a_changelog(self):
        # Regression lock for the move: the case that already worked must keep working.
        r = self._freshness({"SESSION_RUNNER.md": "# runner\n",
                             "CHANGELOG.md": "# ledger\n",
                             "BACKLOG.md": "- [x] shipped\n" * 60})
        self.assertTrue(r["present"])
        self.assertTrue(any("not migrated" in d for _sev, d in r["signals"]))

    def test_the_backlog_signal_stays_adopter_scoped_with_no_changelog(self):
        # The v3.2 fold-in gate must survive the move: a non-adopter sibling that keeps a [x]
        # backlog does not follow the migrate-on-log convention, so it is not a defect there.
        r = self._freshness({"BACKLOG.md": "- [x] shipped\n" * 60})
        self.assertEqual(r["backlog_done_unmigrated"], 60)
        self.assertFalse(any("not migrated" in d for _sev, d in r["signals"]))

    def test_the_backlog_signal_is_not_suppressed_by_new_adopter_grace(self):
        """Found by mutation: every other test here drives real history, so grace-suppressing
        Signal F while moving it survived the whole suite. Grace exists because a *fresh seed* has
        not had a chance to go stale — it says nothing about a backlog that arrived carrying 60
        unmigrated done-marks, and this signal never was grace-scoped. Pin that."""
        young = {"SESSION_RUNNER.md": "# runner\n", "BACKLOG.md": "- [x] shipped\n" * 60}
        # `new_adopter_grace` is only computed once a changelog is located, so grace is
        # OBSERVABLE only in the with-ledger case — assert it there...
        with_ledger = self._freshness({**young, "CHANGELOG.md": "# ledger\n"},
                                      commits=md.LEDGER_REAL_HISTORY_MIN - 1)
        self.assertTrue(with_ledger["new_adopter_grace"], "fixture must actually be under grace")
        self.assertTrue(any("not migrated" in d for _sev, d in with_ledger["signals"]),
                        "Signal F is not grace-scoped and must keep firing on a young repo")
        # ...and separately drive the intersection of both defect conditions: young history AND
        # no changelog at all, where the emission's new position is what makes it reachable.
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            write_tree(p, young)
            r = md.evaluate_changelog_freshness(
                p, {"total_commits": md.LEDGER_REAL_HISTORY_MIN - 1, "days_since_last_commit": 1})
            self.assertFalse(r["present"])
            self.assertTrue(any("not migrated" in d for _sev, d in r["signals"]))

    def test_no_signal_is_stranded_below_the_early_return(self):
        """Guard the guard, STRUCTURALLY. Rather than naming Signal F — which the two tests above
        already cover — this derives the invariant: every advisory that does not name the located
        changelog is one that did not need a changelog to be computed, so it must survive the
        changelog's absence. Today Signal F is the only such advisory, so the two formulations
        coincide; the structural one keeps holding when the next file-independent signal is added
        in the wrong place, and the literal one would not."""
        runner_and_backlog = {"SESSION_RUNNER.md": "# runner\n",
                              "BACKLOG.md": "- [x] shipped\n" * 60}
        with_ledger = self._freshness({**runner_and_backlog, "CHANGELOG.md": "# ledger\n"})
        located = md._find_changelog(self.p).name
        file_independent = {d for _sev, d in with_ledger["signals"] if located not in d}
        self.assertTrue(file_independent, "fixture emits no file-independent advisory to check")
        with tempfile.TemporaryDirectory() as td:   # same fixture, minus the changelog
            p = Path(td)
            write_tree(p, runner_and_backlog)
            without = md.evaluate_changelog_freshness(
                p, {"total_commits": 50, "days_since_last_commit": 1})
        self.assertFalse(without["present"])
        self.assertTrue(file_independent <= {d for _sev, d in without["signals"]},
                        "an advisory that never needed a changelog vanished when the changelog did")


STATUS_TABLE_BACKLOG = """\
# Backlog

## Status Legend

| Status | Meaning |
|--------|---------|
| `DONE` | Completed and tested |
| `READY` | Ready to implement (no blockers) |

## Critical Issues

| ID | Issue | Status | Notes |
|----|-------|--------|-------|
| SEC-013 | Refresh tokens stored as plaintext | DONE | hash_token() utility |
| SEC-014 | JWT tokens in localStorage | DONE | httpOnly cookies + CSRF |
| B-001 | Pagination field mismatch | READY | blocked until SEC-013 is DONE |
| B-002 | Duplicate files need cleanup | IN_PROGRESS | will be DONE next session |
| DONE-9 | Misleading ID column | READY | the ID itself starts with a done token |

## Later

| ID | Initiative | Duration | Status |
|----|-----------|----------|--------|
| INIT-1 | Migration | 3 weeks | **DONE (Session 30, 2026-01-01)** |
| INIT-2 | Rollout | 2 weeks | BLOCKED |
"""

FENCED_DOC_BACKLOG = """\
# Backlog

Format reference — mark an item done like this before migrating it to CHANGELOG.md:

```markdown
- [x] a completed item that exists only inside a documentation example
- [x] a second one
```

## Open

- [ ] a genuinely open item
"""

OUTCOME_TABLE_BACKLOG = """\
# Operational Backlog (fork-only)

> **STATUS: RETIRED** — verbose task bodies are removed at close-out.

## Open items

None.

## Completed items

| Item | Scope | Outcome |
|------|-------|---------|
| **BL-1** | wsfct migration | ✅ Complete in `rmsharp/wsfct` (operator). |
| **BL-4** | Housekeeping | ✅ DONE 2026-07-06 — plans archived. |
"""

EMPTY_BACKLOG = """\
# Backlog

## Active
<!-- Current work items -->

## Up Next
<!-- Upcoming tasks -->
"""


class TestBacklogFormatAndAbstention(unittest.TestCase):
    """Defect 4 (`BACKLOG.md` done-marks are counted checkbox-only, so a table backlog reads 0)
    plus the fenced-code-block false positive, under campaign decision D4: ABSTENTION IS A
    FIRST-CLASS RESULT.

    A silent `0` is defect 4 itself — it is indistinguishable from a clean backlog, which is how
    a 643-line table backlog carrying 256 done-marks reported "nothing unmigrated". So the scanner
    now reports WHICH convention it read, and says out loud when it could not read one.

    The table predicate (*a cell that starts with a done token, in a row of >= 3 cells, ignoring
    the ID column*) is empirically tuned in the campaign plan against that real backlog and is NOT
    re-derived here — see `_BACKLOG_DONE_TOKENS`. `STATUS_TABLE_BACKLOG` is a compact fixture that
    exercises each property the tuning depends on by name (prose false positives, the 2-cell
    legend, a done token in the ID column, a decorated cell, a moving Status column), rather than
    vendoring 51 KB of an adopter's real backlog into this repo; the real-corpus count of 256 is
    reproduced as runtime-smoke evidence at close-out instead.

    RED-FIRST: every assertion below that proves a defect was driven against the unpatched
    scanner and watched to fail — `_count_backlog_done` returned 0 for the table fixture, 2 for
    the fenced one, and 0 (silently) for the abstention fixture. The regression locks assert
    BEHAVIOUR that is unchanged (a checkbox backlog still counts 60), but they are still new
    tests: they call `_scan_backlog_done`, which did not exist before this layer, so none of them
    could execute against the old module — the invariant is preserved, the assertion is not.
    """

    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.p = Path(self._td.name)

    def tearDown(self):
        self._td.cleanup()

    def _scan(self, text):
        write_tree(self.p, {"BACKLOG.md": text})
        return md._scan_backlog_done(self.p)

    def _freshness(self, files_map, commits=50):
        write_tree(self.p, files_map)
        return md.evaluate_changelog_freshness(
            self.p, {"total_commits": commits, "days_since_last_commit": 1})

    # --- the table predicate, property by property -------------------------------------------

    def test_a_status_table_backlog_is_counted(self):
        """RED: the checkbox-only scanner returns 0 for every table backlog ever written."""
        r = self._scan(STATUS_TABLE_BACKLOG)
        self.assertEqual(r["format"], "table")
        self.assertTrue(r["recognized"])
        self.assertEqual(r["done"], 3, "SEC-013, SEC-014 and INIT-1 are the only done rows")

    def test_prose_containing_a_done_token_is_not_a_done_row(self):
        """The 94-false-positive class the tuning rejected: a NOTES cell that merely mentions a
        done token ("blocked until SEC-013 is DONE") is not a completed item. A *contains*
        predicate scored 321 on the real corpus against a hand count of 253."""
        r = self._scan(
            "| ID | Issue | Status | Notes |\n"
            "|----|-------|--------|-------|\n"
            "| B-001 | Pagination | READY | blocked until SEC-013 is DONE |\n")
        self.assertEqual(r["done"], 0)

    def test_a_done_token_in_the_id_column_is_ignored(self):
        """Why the predicate skips cell 0: an ID may legitimately start with a done token
        (`DONE-9`) while the row's actual status is READY."""
        r = self._scan(
            "| ID | Issue | Status | Notes |\n"
            "|----|-------|--------|-------|\n"
            "| DONE-9 | Misleading ID | READY | still open |\n")
        self.assertEqual(r["done"], 0)

    def test_the_two_cell_legend_is_not_counted(self):
        """Why the predicate needs >= 3 cells: a Status *legend* defines the vocabulary, it does
        not report work. An *equals* predicate scored 227 and counted this row."""
        r = self._scan(
            "| Status | Meaning |\n"
            "|--------|---------|\n"
            "| `DONE` | Completed and tested |\n")
        self.assertEqual(r["done"], 0)

    def test_a_decorated_done_cell_is_counted(self):
        """Why the predicate is *starts-with* and not *equals*: real backlogs write
        `**DONE (Session 30, ...)**`, which no equality test matches."""
        r = self._scan(
            "| ID | Initiative | Duration | Status |\n"
            "|----|-----------|----------|--------|\n"
            "| INIT-1 | Migration | 3 weeks | **DONE (Session 30, 2026-01-01)** |\n")
        self.assertEqual(r["done"], 1)

    def test_the_status_column_may_sit_anywhere_but_the_id_column(self):
        """Guard the guard: across the real corpus's 27 tables the Status column lands at index
        2 (20 tables), 3, 4 and even 0, and 3 tables carry no Status column at all — which is why
        the predicate scans every non-ID cell rather than a fixed column index."""
        r = self._scan(STATUS_TABLE_BACKLOG)
        self.assertEqual(r["done"], 3, "a fixed Status index would miss the trailing-Status table")

    # --- the fenced-code-block false positive ------------------------------------------------

    def test_a_fenced_example_is_not_a_done_mark(self):
        """RED: today this counts 2. A doc that *documents* the `- [x]` convention inside a fenced
        example is not a repo with unmigrated work — it is a match presented as a finding, the
        campaign's own root defect."""
        r = self._scan(FENCED_DOC_BACKLOG)
        self.assertEqual(r["done"], 0)
        self.assertEqual(r["format"], "checkbox",
                         "the surviving `- [ ]` outside the fence still identifies the convention")
        self.assertTrue(r["recognized"])

    def test_a_fenced_table_is_not_a_done_row(self):
        """The same containment on the new surface: a fenced example of the *table* convention
        must not be counted either."""
        r = self._scan(
            "# Backlog\n\nExample:\n\n```markdown\n"
            "| ID | Issue | Status | Notes |\n"
            "|----|-------|--------|-------|\n"
            "| X-1 | example | DONE | not real |\n"
            "```\n\n- [ ] a real open item\n")
        self.assertEqual(r["done"], 0)

    # --- abstention (decision D4) -------------------------------------------------------------

    def test_an_unreadable_table_abstains_visibly(self):
        """RED: today this reports a silent 0, indistinguishable from a clean backlog. A table
        with no Status column carries item state this scanner cannot interpret, so it must say so
        rather than assert a count it cannot support. This is this repo's own backlog shape
        (`| Item | Scope | Outcome |`) and the plan names it as the abstention case."""
        r = self._scan(OUTCOME_TABLE_BACKLOG)
        self.assertEqual(r["format"], "unrecognized")
        self.assertFalse(r["recognized"])
        self.assertEqual(r["done"], 0)

    def test_the_abstention_is_visible_to_an_adopter(self):
        f = self._freshness({"SESSION_RUNNER.md": "# runner\n",
                             "BACKLOG.md": OUTCOME_TABLE_BACKLOG})
        self.assertFalse(f["backlog_recognized"])
        self.assertTrue(any("not recognized" in d for _sev, d in f["signals"]),
                        "an unreadable format must abstain out loud, never report a silent 0")
        self.assertTrue(any("BACKLOG.md" in d for _sev, d in f["signals"]),
                        "the advisory must name the file it was computed against")

    def test_the_abstention_is_adopter_scoped(self):
        """Same gate as Signal F itself: only an adopter follows the migrate-on-log convention, so
        only an adopter is owed a note about the scanner's inability to check it."""
        f = self._freshness({"BACKLOG.md": OUTCOME_TABLE_BACKLOG})
        self.assertFalse(any("not recognized" in d for _sev, d in f["signals"]))

    def test_an_empty_backlog_is_silent_rather_than_abstaining(self):
        """The abstention must stay NARROW. An empty backlog is the healthy state, not an
        unreadable one: it carries no item rows and no checkboxes, so 0 is a correct measurement
        and there is nothing to disclose. Two live adopters keep exactly this file; advising them
        that a format was 'not recognized' would be a signal that does not mean what it appears
        to mean — the defect class this campaign exists to remove."""
        r = self._scan(EMPTY_BACKLOG)
        self.assertEqual(r["format"], "none")
        self.assertEqual(r["done"], 0)
        f = self._freshness({"SESSION_RUNNER.md": "# runner\n", "BACKLOG.md": EMPTY_BACKLOG})
        self.assertFalse(any("not recognized" in d for _sev, d in f["signals"]))

    def test_a_prose_bullet_backlog_abstains(self):
        """The other side of that boundary: plain list items with no checkbox and no table DO
        carry item state the scanner cannot read, so they abstain rather than report 0."""
        r = self._scan("# Backlog\n\n- Fix the login redirect (done)\n- Add rate limiting\n")
        self.assertEqual(r["format"], "unrecognized")
        self.assertFalse(r["recognized"])

    def test_an_absent_backlog_is_not_an_abstention(self):
        """A repo that keeps no backlog at all has no format to fail to recognize."""
        write_tree(self.p, {"SESSION_RUNNER.md": "# runner\n"})
        r = md._scan_backlog_done(self.p)
        self.assertEqual(r["format"], "absent")
        self.assertIsNone(r["source"])
        f = md.evaluate_changelog_freshness(
            self.p, {"total_commits": 50, "days_since_last_commit": 1})
        self.assertFalse(any("not recognized" in d for _sev, d in f["signals"]))

    # --- regression locks ---------------------------------------------------------------------

    def test_a_checkbox_backlog_counts_exactly_as_before(self):
        """The one behaviour this layer must not move: the checkbox predicate is unchanged."""
        r = self._scan("- [x] shipped\n" * 60)
        self.assertEqual(r["format"], "checkbox")
        self.assertEqual(r["done"], 60)
        f = self._freshness({"SESSION_RUNNER.md": "# runner\n",
                             "BACKLOG.md": "- [x] shipped\n" * 60})
        self.assertEqual(f["backlog_done_unmigrated"], 60)
        self.assertTrue(any("not migrated" in d for _sev, d in f["signals"]))

    def test_an_all_open_checkbox_backlog_is_a_recognized_zero(self):
        """A recognized 0 and an abstained 0 are different findings, which is the whole of D4."""
        r = self._scan("- [ ] still open\n- [ ] also open\n")
        self.assertEqual(r["format"], "checkbox")
        self.assertTrue(r["recognized"])
        self.assertEqual(r["done"], 0)

    def test_the_search_order_over_backlog_locations_is_unchanged(self):
        write_tree(self.p, {"BACKLOG.md": "- [x] root\n",
                            "docs/planning/BACKLOG.md": STATUS_TABLE_BACKLOG})
        r = md._scan_backlog_done(self.p)
        self.assertEqual(r["source"], "BACKLOG.md")
        self.assertEqual(r["done"], 1)

    def test_the_emitted_metrics_key_contract_is_preserved(self):
        """`backlog_done_unmigrated` is in the JSON contract; the new keys are additive."""
        f = self._freshness({"SESSION_RUNNER.md": "# runner\n",
                             "BACKLOG.md": STATUS_TABLE_BACKLOG})
        self.assertEqual(f["backlog_done_unmigrated"], 3)
        self.assertEqual(f["backlog_format"], "table")
        self.assertTrue(f["backlog_recognized"])

    # --- mutation-driven coverage --------------------------------------------------------------
    #
    # Every test below closes a hole found by MUTATION, not by RED-first: each one pins a decision
    # that the suite above could not distinguish from its opposite. Two further mutants survive and
    # are deliberately NOT "fixed", because they are inert by construction rather than untested —
    # inventing a test for either would assert a property over an input that cannot violate it,
    # which is the campaign's own §8 learning 2:
    #
    #   * `elif` -> `if` on the abstention branch. An unrecognized format always reports done == 0,
    #     so the two branches are already mutually exclusive; the `elif` documents that, it does not
    #     enforce it.
    #   * dropping the separator-row skip in `_table_rows`. A separator cell contains only `-` and
    #     `:`, which can never start with a done token, so the skip is clarity rather than behaviour.

    def test_checkbox_format_wins_when_a_backlog_carries_both(self):
        """Precedence is a real decision, and no fixture above forced it. Checkbox wins, because
        that is the reading this layer promised not to move; a backlog carrying both conventions is
        reported under the one whose count is already load-bearing."""
        r = self._scan(
            "| ID | Task | Status | Notes |\n"
            "|----|------|--------|-------|\n"
            "| A-1 | a | DONE | |\n"
            "| A-2 | b | DONE | |\n"
            "| A-3 | c | DONE | |\n"
            "\n## Also\n\n- [x] one checkbox item\n")
        self.assertEqual(r["format"], "checkbox")
        self.assertEqual(r["done"], 1)

    def test_a_status_word_in_a_data_row_is_not_a_header(self):
        """A header is the row directly above a `|---|` separator — not any row that happens to
        say "Status". Otherwise a single NOTES cell reading "Status: DONE" would silently promote
        an unreadable table to a counted one, turning an honest abstention into a fabricated count."""
        r = self._scan(
            "| Item | Scope | Outcome |\n"
            "|------|-------|---------|\n"
            "| BL-1 | migration | Status: DONE |\n"
            "| BL-2 | cleanup | DONE 2026-01-01 |\n")
        self.assertEqual(r["format"], "unrecognized")
        self.assertEqual(r["done"], 0)

    # The token list is written out LITERALLY here on purpose. A first version of this test built
    # its fixture by iterating md._BACKLOG_DONE_TOKENS and asserting done == len(that tuple) —
    # which passes no matter which tokens are removed, because fixture and expectation move
    # together. Mutation caught it: dropping a token survived the "coverage" written to pin it.
    # A test derived from the thing under test cannot falsify it (campaign §8 learning 2).
    EXPECTED_DONE_TOKENS = ("DONE", "COMPLETE", "COMPLETED", "SHIPPED", "FIXED", "RESOLVED",
                            "CLOSED", "✅")

    def test_the_published_done_token_set_is_pinned(self):
        self.assertEqual(md._BACKLOG_DONE_TOKENS, self.EXPECTED_DONE_TOKENS,
                         "the done-token set is a published predicate — changing it changes every "
                         "adopter's Signal F, so it changes here first")

    def test_every_shipped_done_token_is_counted(self):
        """The real 643-line corpus only exercises DONE, FIXED and RESOLVED, so the other five
        tokens shipped untested — dropping any one of them changed nothing the suite could see."""
        rows = "".join(f"| A-{i} | task | {tok} | notes |\n"
                       for i, tok in enumerate(self.EXPECTED_DONE_TOKENS))
        r = self._scan("| ID | Task | Status | Notes |\n|----|------|--------|-------|\n"
                       + rows + "| A-99 | open one | READY | notes |\n")
        self.assertEqual(r["done"], len(self.EXPECTED_DONE_TOKENS),
                         "every documented done token must count, and READY must not")

    def test_a_recognized_zero_is_distinguishable_from_an_abstained_zero(self):
        """The whole of D4, asserted on the emitted metrics: `backlog_recognized` must report the
        CONVENTION, never merely `done > 0`. A backlog with only open checkboxes is a trustworthy
        0; an unreadable table is not — and both report 0."""
        f = self._freshness({"SESSION_RUNNER.md": "# runner\n", "BACKLOG.md": "- [ ] open\n"})
        self.assertEqual(f["backlog_done_unmigrated"], 0)
        self.assertTrue(f["backlog_recognized"], "an all-open checkbox backlog is a KNOWN zero")
        f2 = self._freshness({"SESSION_RUNNER.md": "# runner\n",
                              "BACKLOG.md": OUTCOME_TABLE_BACKLOG})
        self.assertEqual(f2["backlog_done_unmigrated"], 0)
        self.assertFalse(f2["backlog_recognized"], "an unreadable table is an UNKNOWN zero")

    def test_a_horizontal_rule_is_not_an_item(self):
        """Keeps the abstention narrow. `---` is a markdown horizontal rule, not a list item, and
        an otherwise-empty backlog containing one is still the healthy empty state. A bullet
        predicate loose enough to match it would abstain on ordinary formatting."""
        r = self._scan("# Backlog\n\n## Active\n\n---\n\n## Up Next\n")
        self.assertEqual(r["format"], "none")

    def test_a_fence_is_closed_only_by_its_own_marker(self):
        """A ``` block is not closed by a ~~~ line inside it. Otherwise the remainder of the
        example leaks back into the scan and is counted as real work."""
        r = self._scan("# Backlog\n\n```markdown\n~~~\n- [x] leaked example\n```\n\n- [ ] real\n")
        self.assertEqual(r["done"], 0)
        self.assertEqual(r["format"], "checkbox")

    # --- review-driven coverage ----------------------------------------------------------------
    #
    # Everything below closes a hole found by the 5-lens adversarial boundary review, which caught
    # what RED-first and two mutation rounds both missed. The first two are REGRESSIONS the review
    # found in this layer's own new code.

    def test_an_unterminated_fence_does_not_swallow_the_file(self):
        """REGRESSION the review caught. A markdown renderer lets an unclosed ``` run to end of
        file; doing that here let ONE stray fence line hide every done-mark below it and report a
        clean backlog — strictly worse than the checkbox-only scanner this layer replaces, and the
        exact silent-zero this layer exists to remove. Only CLOSED fences are stripped."""
        text = "# Backlog\n\n```\n\n## Notes\n\n- [x] a\n- [x] b\n- [x] c\n"
        r = self._scan(text)
        self.assertEqual(r["done"], 3)
        self.assertEqual(len(md._BACKLOG_DONE_RE.findall(text)), 3,
                         "and it must still agree with the pre-Layer-3 reading on this input")

    def test_a_stray_fence_cannot_manufacture_a_trusted_zero(self):
        """The worst sibling of the unterminated-fence regression, and the reason the fix is "do
        not strip an unclosed fence" rather than "redirect the empty case": with a Status table
        ABOVE the stray fence, swallowing the tail returned format `table`, done 0, recognized
        TRUE — an affirmatively trusted zero, worse than abstaining. Also covers the case where the
        document is genuinely balanced to a renderer (a 4-backtick outer fence) so the author has
        no visual cue anything is wrong."""
        r = self._scan("# Backlog\n\n| ID | Item | Status |\n|----|------|--------|\n"
                       "| A-1 | x | OPEN |\n\n```text\n- [x] BL-1 shipped\n- [x] BL-2 shipped\n")
        self.assertEqual(r["done"], 2)
        outer = self._scan("# Backlog\n\n````markdown\n```\n````\n\n- [x] BL-1\n- [x] BL-2\n")
        self.assertEqual(outer["done"], 2, "a 4-backtick fence renders balanced; do not swallow it")

    def test_a_header_row_is_not_a_finished_item(self):
        """REGRESSION the review caught. A table whose column is headed `Completed` counted its own
        HEADING as one unmigrated item — a label read as work, which is this campaign's root defect
        reproduced inside its own fix."""
        r = self._scan("| ID | Status | Completed | Notes |\n"
                       "|----|--------|-----------|-------|\n"
                       "| A-1 | READY | no | still open |\n")
        self.assertEqual(r["format"], "table")
        self.assertEqual(r["done"], 0)

    def test_an_escaped_pipe_does_not_fabricate_a_done_mark(self):
        """REGRESSION the review caught. `\\|` is the only way GFM lets a literal pipe sit inside a
        cell; splitting on it invents cells that were never in the table and can shift a prose
        fragment into the position the predicate reads — so a NOTES cell mentioning "DONE upstream"
        marked an open row complete. The row below is READY and must count 0."""
        r = self._scan("| ID | Task | Status | Notes |\n|----|------|--------|-------|\n"
                       r"| B-1 | a thing | READY | see `foo \| bar` — DONE upstream |" "\n")
        self.assertEqual(r["format"], "table")
        self.assertEqual(r["done"], 0)

    def test_an_inline_code_span_does_not_close_a_fence(self):
        """The fence marker is three characters, not two: a line opening with a two-backtick inline
        code span sits INSIDE the block and must not close it, or the rest of the example leaks
        back in and is counted as work."""
        r = self._scan("# Backlog\n\n```markdown\n``code`` in an example\n- [x] fenced item\n```\n"
                       "\n- [ ] real open item\n")
        self.assertEqual(r["done"], 0)

    def test_a_tilde_fence_is_stripped_too(self):
        """`_FENCE_RE` accepts ~~~ as well as ```, and nothing exercised it: deleting ~~~ support
        entirely survived the suite and re-created the false positive this layer removes."""
        r = self._scan("# Backlog\n\n~~~markdown\n- [x] fenced example\n~~~\n\n- [ ] real\n")
        self.assertEqual(r["done"], 0)

    def test_a_backlog_below_the_root_is_found_and_named(self):
        """No test ever read a non-root location, so `_BACKLOG_LOCATIONS` was effectively a
        one-element tuple as far as the suite could tell — and the advisory that promises to name
        its source file could not fail against a hardcoded "BACKLOG.md"."""
        write_tree(self.p, {"SESSION_RUNNER.md": "# runner\n",
                            "docs/planning/BACKLOG.md": "- [x] shipped\n" * 3})
        r = md._scan_backlog_done(self.p)
        self.assertEqual(r["source"], "docs/planning/BACKLOG.md")
        self.assertEqual(r["done"], 3)
        f = md.evaluate_changelog_freshness(
            self.p, {"total_commits": 50, "days_since_last_commit": 1})
        self.assertTrue(any("docs/planning/BACKLOG.md" in d for _sev, d in f["signals"]),
                        "the advisory must name the file it actually read")

    def test_a_three_column_table_is_counted(self):
        """The `>= 3` floor was only ever tested from below (2-cell rows excluded). A 3-column
        backlog is the boundary case and had no coverage at all."""
        r = self._scan("| ID | Task | Status |\n|----|------|--------|\n"
                       "| A-1 | a thing | DONE |\n| A-2 | another | READY |\n")
        self.assertEqual(r["done"], 1)

    def test_done_tokens_are_matched_case_insensitively_and_through_decoration(self):
        """`_cell_marks_done` upper-cases and strips backticks/asterisks; neither was exercised, so
        dropping either survived both the suite and the 643-line runtime smoke."""
        r = self._scan("| ID | Task | Status | Notes |\n|----|------|--------|-------|\n"
                       "| A-1 | a | done | lowercase |\n"
                       "| A-2 | b | `DONE` | code-span |\n"
                       "| A-3 | c | Done — 2026-01-01 | mixed case + trailer |\n"
                       "| A-4 | d | READY | still open |\n")
        self.assertEqual(r["done"], 3)

    def test_a_bolded_status_header_still_declares_a_table(self):
        r = self._scan("| ID | Task | **Status** | Notes |\n|:---|:----:|-----------:|------|\n"
                       "| A-1 | a | DONE | x |\n")
        self.assertEqual(r["format"], "table")
        self.assertEqual(r["done"], 1, "alignment-colon separators must parse too")

    @unittest.skipIf(os.geteuid() == 0, "root can read a 000-mode file")
    def test_an_unreadable_backlog_abstains_rather_than_reporting_zero(self):
        """An I/O error is the one case where 0 is guaranteed to mean nothing at all, and it was
        the one branch that still reported a silent 0 — D4's own definition of defect 4."""
        write_tree(self.p, {"SESSION_RUNNER.md": "# runner\n", "BACKLOG.md": "- [x] a\n"})
        bl = self.p / "BACKLOG.md"
        bl.chmod(0o000)
        try:
            r = md._scan_backlog_done(self.p)
            self.assertEqual(r["format"], "unreadable")
            self.assertFalse(r["recognized"])
            f = md.evaluate_changelog_freshness(
                self.p, {"total_commits": 50, "days_since_last_commit": 1})
            self.assertTrue(any("inactive for this repo" in d for _sev, d in f["signals"]),
                            "an unreadable backlog must abstain, not report a clean 0")
        finally:
            bl.chmod(0o644)

    def test_the_union_predicates_known_false_positives_are_pinned(self):
        """CHARACTERIZATION, not endorsement. The tuned predicate is a union over every non-ID
        cell rather than a read of the Status column, so a TITLE cell beginning with a done token
        and a 3-column legend's MEANING cell both count. Measured on the 643-line corpus this was
        tuned against, that costs nothing — all 256 rows are counted via a Status column (242) or
        sit in a table with no Status column (14), and none only via another column. Narrowing is
        an operator decision (it would move the ratified count to 242), so the behaviour is pinned
        here rather than silently changed."""
        title = self._scan("| ID | Task | Status | Notes |\n|----|------|--------|-------|\n"
                           "| B-5 | Fixed login redirect | READY | still open |\n")
        self.assertEqual(title["done"], 1, "known false positive: a done token in the TITLE cell")
        legend = self._scan("| Status | Meaning | Example |\n|--------|---------|--------|\n"
                            "| `DONE` | Completed and tested | A-1 |\n"
                            "| ID | Task | Status |\n|----|------|--------|\n"
                            "| A-9 | real | READY |\n")
        self.assertEqual(legend["done"], 1, "known false positive: a 3-column legend")


class TestAdvisoriesNameTheirSource(unittest.TestCase):
    """Defect 5's misdirecting half. An adopter whose only changelog was a `docs/` product
    release-notes file was told its "CHANGELOG ledger" was lagging — advice to go update a
    release-notes file, while the real finding (no action ledger at all) stayed suppressed. An
    advisory that names the file it was computed against cannot misdirect."""

    def _signals(self, p):
        r = md.evaluate_changelog_freshness(
            p, {"total_commits": 50, "days_since_last_commit": 1})
        return [d for _sev, d in r["signals"]]

    def test_the_commit_lag_advisory_names_the_file(self):
        # docs/changelog.md in the first commit, then 12 commits that never touch it.
        p = git_repo(self, {"docs/changelog.md": "# product release notes\n"}, extra_commits=12)
        descs = self._signals(p)
        lag = [d for d in descs if "commits since it was last updated" in d]
        self.assertEqual(len(lag), 1, f"expected exactly one commit-lag advisory; got {descs}")
        self.assertIn("docs/changelog.md", lag[0])
        self.assertNotIn("ledger", lag[0].lower())

    def test_the_day_lag_advisory_names_the_file(self):
        p = git_repo(self, {"docs/changelog.md": "# product release notes\n"}, extra_commits=1,
                     dates=("2026-01-01T12:00:00", "2026-06-01T12:00:00"))
        descs = self._signals(p)
        day = [d for d in descs if "days" in d]
        self.assertEqual(len(day), 1, f"expected exactly one day-lag advisory; got {descs}")
        self.assertIn("docs/changelog.md", day[0])
        self.assertNotIn("ledger", day[0].lower())

    def test_the_never_used_advisory_names_the_file(self):
        # Same misdirection class as the two lag messages: "CHANGELOG present but never used"
        # reads as a statement about the action ledger even when the file found was docs/.
        p = git_repo(self, {"docs/changelog.md": f"# notes\n{md.SEED_SENTINEL}\n"},
                     extra_commits=1)
        descs = self._signals(p)
        never = [d for d in descs if "never used" in d]
        self.assertEqual(len(never), 1, f"expected exactly one never-used advisory; got {descs}")
        self.assertIn("docs/changelog.md", never[0])

    def test_a_root_ledger_advisory_names_the_root_file(self):
        # The naming is uniform, not a special case for docs/: the same code path names
        # CHANGELOG.md when that is what it measured.
        p = git_repo(self, {"CHANGELOG.md": "# ledger\n"}, extra_commits=12)
        lag = [d for d in self._signals(p) if "commits since it was last updated" in d]
        self.assertEqual(len(lag), 1)
        self.assertIn("CHANGELOG.md", lag[0])

    def test_advisory_paths_are_posix_on_every_platform(self):
        # The displayed path is a rendered string, not a filesystem argument — pin the separator
        # so the message reads the same in a Windows adopter's dashboard. Asserted only over
        # advisories that actually carry a nested path, so this cannot pass vacuously against an
        # implementation that names no file at all.
        p = git_repo(self, {"docs/changelog.md": "# notes\n"}, extra_commits=12)
        descs = self._signals(p)
        naming = [d for d in descs if "changelog.md" in d.lower()]
        self.assertTrue(naming, f"no advisory named its source file; got {descs}")
        for d in naming:
            self.assertIn("docs/changelog.md", d)
            self.assertNotIn("\\", d)


class TestMembershipRiskGating(unittest.TestCase):
    """The membership risk's two guards, driven at the pure layer for precision. Both live on the
    one line this layer rewrote, and both were unpinned: mutation showed that DELETING the
    history gate and an OFF-BY-ONE on it each survived the whole suite."""

    def _flagged(self, commits, adopter=True, ledger=False):
        m = base_metrics(
            git={"total_commits": commits},
            methodology={"compliance_score": 25, "compliance_pct": md.compliance_pct(25),
                         "items": {"SESSION_RUNNER.md": adopter}},
            changelog={"present": False, "ledger_present": ledger, "is_fresh": False,
                       "signals": []})
        return any("no root CHANGELOG.md" in d for d in risk_descs(m))

    def test_a_brand_new_adopter_is_not_scolded_for_a_ledger_it_has_not_owed_yet(self):
        self.assertFalse(self._flagged(md.LEDGER_REAL_HISTORY_MIN - 1))

    def test_the_history_threshold_is_inclusive(self):
        self.assertTrue(self._flagged(md.LEDGER_REAL_HISTORY_MIN))

    def test_a_non_adopter_is_never_flagged_however_long_its_history(self):
        self.assertFalse(self._flagged(10_000, adopter=False))

    def test_a_repo_with_a_ledger_is_never_flagged(self):
        self.assertFalse(self._flagged(10_000, ledger=True))


class TestLedgerIdentityEndToEnd(unittest.TestCase):
    """Ratified decision D3 driven through `collect_all`: LOCATION (which changelog to measure
    freshness against) and MEMBERSHIP (does this repo keep an action ledger) are different
    questions, and fixing the second must not silently cost the first. The obvious fix —
    narrowing the one locator to the root — passes the membership test and quietly drops a
    documentation point for exactly the adopter class the defect is about."""

    def _adopter_with_only_a_docs_changelog(self):
        # 12 commits, so the repo has real history and gets no new-adopter grace, with the
        # changelog committed LAST so it is not also lagging: the finding under test is
        # membership, not freshness.
        return git_repo(self, {"SESSION_RUNNER.md": "# runner\n" * 5,
                               "README.md": "# demo\n" * 60},
                        extra_commits=10,
                        tail_files={"docs/changelog.md": "# Product release notes\n\n## 1.2.0\n"})

    def test_the_adopter_is_told_it_has_no_action_ledger(self):
        m = md.collect_all(self._adopter_with_only_a_docs_changelog())
        self.assertGreaterEqual(m["git"]["total_commits"], md.LEDGER_REAL_HISTORY_MIN)
        self.assertTrue(m["changelog"]["present"], "located for freshness")
        self.assertFalse(m["changelog"]["ledger_present"], "but it is not an action ledger")
        descs = [r["description"] for r in m["scores"]["risks"]]
        self.assertTrue(any("no root CHANGELOG.md" in d for d in descs),
                        f"the adopter must learn it has no action ledger; got {descs}")

    def test_the_same_adopter_keeps_its_documentation_freshness_point(self):
        """D3's regression lock, and the reason the obvious fix is wrong: `is_fresh` is computed
        after the `changelog is None` early return, so a root-only locator leaves it False and
        `score_health` silently withholds its +1 — a scoring change under a no-scoring-change
        claim."""
        m = md.collect_all(self._adopter_with_only_a_docs_changelog())
        self.assertTrue(m["docs"]["has_changelog"])
        self.assertTrue(m["changelog"]["is_fresh"], "freshness still measured against docs/")
        earned = md.score_health(m)["documentation"]
        self.assertLess(earned, 20, "the control below is only meaningful under the 0-20 cap")
        stale = {**m, "changelog": {**m["changelog"], "is_fresh": False}}
        self.assertEqual(earned - md.score_health(stale)["documentation"], 1,
                         "the +1 freshness point must still be earned, not silently dropped")

    def test_an_adopter_with_a_real_ledger_is_not_flagged(self):
        # Regression lock on the other side of the predicate: a root CHANGELOG.md satisfies
        # membership, so the risk must stay silent.
        p = git_repo(self, {"SESSION_RUNNER.md": "# runner\n" * 5, "README.md": "# demo\n" * 60},
                     extra_commits=10, tail_files={"CHANGELOG.md": "# ledger\n\n### 2026-07-25 · x\n"})
        m = md.collect_all(p)
        self.assertTrue(m["changelog"]["ledger_present"])
        self.assertFalse(any("no root CHANGELOG.md" in r["description"]
                             for r in m["scores"]["risks"]))

    def test_a_non_adopter_with_no_ledger_is_not_flagged(self):
        # Regression lock: the risk stays adopter-scoped. A sibling project that keeps no ledger
        # by design is not a methodology defect.
        m = md.collect_all(git_repo(self, {"README.md": "# demo\n" * 60}, extra_commits=10))
        self.assertFalse(m["changelog"]["ledger_present"])
        self.assertFalse(any("no root CHANGELOG.md" in r["description"]
                             for r in m["scores"]["risks"]))


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
        self.assertEqual(md.DASHBOARD_VERSION, "2.9.2")
        starter_src = Path(STARTER_PY).read_text(encoding="utf-8")
        self.assertTrue(re.search(r'^DASHBOARD_VERSION\s*=\s*"2\.9\.2"', starter_src, re.MULTILINE),
                        "starter-kit twin must also declare DASHBOARD_VERSION 2.9.2")


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
