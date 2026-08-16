#!/usr/bin/env python3
"""Behaviour tests for starter-kit/context_budget.py — the FM #28 size-budget gate.

CANONICAL-ONLY. Not in bin/_manifest.py, so adopters do not receive it. The tool's own
`--selftest` ships to them and covers every pure gate; what cannot ship is this file's
git fixtures, which need a scratch repository with a real merge in it.

WHY THIS FILE EXISTS AT ALL. Until BL-38 the tool's `calibrate()` had no test asserting
its arithmetic — Test 35 in bin/tests.sh covered install-hook, sync distribution and the
selftest gates, all of which stayed green while the fit itself returned noise on any repo
that had merged another lineage of its regressor. A shipped executable can be arbitrarily
wrong in a dimension nothing asserts. That is the same argument the harness already makes
for the ledger trimmer at bin/tests.sh:248-251.

DISCIPLINE THIS FILE IS WRITTEN UNDER (inherited from tools/test_methodology_trim.py):

  * PROVE THE FIXTURE FIRST. Every fixture asserts what it IS before anything is asserted
    about what the code does to it. A merge fixture that failed to create a merge would
    make the D1 tests pass for the wrong reason, forever.
  * DRIVE EACH GUARD RED. Green is not evidence until red has been observed. Each defect
    below is exhibited as well as fixed: D1 through `first_parent=False`, which is the
    real pre-change behaviour preserved as a parameter for exactly this purpose, and D2
    through `_string_size_at`, a verbatim re-implementation of the shipped comparison.
  * NARROW THE GUARD, DO NOT ONLY DELETE IT. The plausible weaker implementation is shown
    to give the WRONG answer on the same fixture, which is what makes the strong version
    load-bearing rather than merely present.
  * ASSERT ON VALUES, NEVER ON A TOOL'S EXIT CODE. An exit code is a union over every
    check the tool runs, so adding a check silently re-labels unrelated assertions.

THE PRE-CHANGE TOOL is blob be2721a5fa12df027636d1451d84301293467fae — `git cat-file blob
be2721a` — should anyone need to re-run the four-way fit that motivated this.
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True          # no starter-kit/__pycache__ from this import

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
CB_PY = REPO / "starter-kit" / "context_budget.py"

_spec = importlib.util.spec_from_file_location("context_budget", str(CB_PY))
cb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cb)


def git(repo, *args, when=None, check=True):
    """Run git in `repo`. `when` pins BOTH author and committer date, which is what makes
    the ordering fixtures reproducible — %cI reads the committer date, not the author's.
    `check=False` is for the deliberate conflict in the merge fixture."""
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    if when:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = when
    p = subprocess.run(["git", "-C", str(repo), *args], env=env,
                       capture_output=True, text=True)
    if check and p.returncode:
        raise AssertionError(f"git {' '.join(args)} failed: {p.stderr.strip()}")
    return p.stdout.strip()


def write_commit(repo, name, size, when, msg=None):
    (Path(repo) / name).write_text("x" * size)
    git(repo, "add", name)
    git(repo, "commit", "-m", msg or f"{name} -> {size}", when=when)


def new_repo(d):
    git(d, "init", "-q", "-b", "main")
    return d


# ---------------------------------------------------------------------------------
# D1 — lineage. `git log -- <path>` walks ALL merged ancestry, so on a repository that
# has merged another lineage of the same file, two size series interleave by commit
# date and "the size of X at time T" stops being a function.
# ---------------------------------------------------------------------------------

class TestLineage(unittest.TestCase):

    def _forked_repo(self, d):
        """main: 100 B at t0, 200 B at t2. A side branch carries 50,000 B at t1 — a size
        that NEVER existed on main — and is merged at t3, the merge RESOLVING the file to
        300 B.

        The resolution matters, and the first draft of this fixture got it wrong. A merge
        taken with `-s ours` leaves the tree TREESAME to the first parent, and git's
        DEFAULT history simplification then prunes the side branch from `git log -- <path>`
        on its own — so the defect does not reproduce and every assertion below would have
        passed against the broken code. D1 requires a merge that genuinely changed the
        target, which is exactly the case this framework's own workflow produces: a fork
        syncing an upstream that has edited the same file.
        """
        new_repo(d)
        write_commit(d, "CLAUDE.md", 100, "2026-01-01T00:00:00+00:00")
        git(d, "checkout", "-q", "-b", "side")
        write_commit(d, "CLAUDE.md", 50000, "2026-01-02T00:00:00+00:00")
        git(d, "checkout", "-q", "main")
        write_commit(d, "CLAUDE.md", 200, "2026-01-03T00:00:00+00:00")
        git(d, "merge", "--no-commit", "--no-ff", "side", check=False)   # conflicts, by design
        (Path(d) / "CLAUDE.md").write_text("x" * 300)                    # the resolution
        git(d, "add", "CLAUDE.md")
        git(d, "commit", "-m", "merge side", when="2026-01-04T00:00:00+00:00")
        return d

    def test_fixture_really_has_a_merge_and_a_foreign_size(self):
        """PROVE THE FIXTURE. Without a real two-parent merge, without the side branch's
        size being reachable through the ancestry walk, and without the merge having
        actually changed the file, every assertion below would pass vacuously. This test
        failed first on the original fixture and is the only reason that was caught."""
        with tempfile.TemporaryDirectory() as d:
            self._forked_repo(d)
            parents = git(d, "rev-list", "--parents", "-n", "1", "HEAD").split()
            self.assertEqual(len(parents), 3, "HEAD is not a two-parent merge")
            allsizes = {s for _, s in cb.size_history(d, "CLAUDE.md", first_parent=False)[0]}
            self.assertIn(50000, allsizes, "the foreign lineage is not reachable at all")
            self.assertEqual((Path(d) / "CLAUDE.md").stat().st_size, 300,
                             "the merge did not change the file, so it is TREESAME-pruned")

    def test_first_parent_excludes_the_foreign_lineage(self):
        with tempfile.TemporaryDirectory() as d:
            self._forked_repo(d)
            hist, skipped, err = cb.size_history(d, "CLAUDE.md")
            self.assertIsNone(err)
            self.assertEqual(skipped, 0)
            self.assertEqual([s for _, s in hist], [100, 200, 300])

    def test_the_defect_it_replaces_admits_a_size_that_never_existed_here(self):
        """DRIVE IT RED. first_parent=False is the shipped pre-change behaviour."""
        with tempfile.TemporaryDirectory() as d:
            self._forked_repo(d)
            defective, _, _ = cb.size_history(d, "CLAUDE.md", first_parent=False)
            self.assertIn(50000, [s for _, s in defective])

    def test_size_at_disagrees_between_the_two_views_on_the_same_instant(self):
        """The consequence, stated as the quantity that actually feeds the regression:
        at 2026-01-02T12:00Z main's CLAUDE.md was 100 B. The ancestry-walking view says
        50,000 B — a 500x error in the regressor, silently."""
        with tempfile.TemporaryDirectory() as d:
            self._forked_repo(d)
            when = cb.parse_iso("2026-01-02T12:00:00Z")
            good = cb.size_at(cb.size_history(d, "CLAUDE.md")[0], when)
            bad = cb.size_at(cb.size_history(d, "CLAUDE.md", first_parent=False)[0], when)
            self.assertEqual(good, 100)
            self.assertEqual(bad, 50000)

    def test_a_treesame_merge_is_pruned_even_without_first_parent(self):
        """The boundary of D1, pinned so nobody re-derives it the hard way (this session
        did): git's default history simplification already drops a side branch whose merge
        did not change the target. The defect needs a merge that DID."""
        with tempfile.TemporaryDirectory() as d:
            new_repo(d)
            write_commit(d, "CLAUDE.md", 100, "2026-01-01T00:00:00+00:00")
            git(d, "checkout", "-q", "-b", "side")
            write_commit(d, "CLAUDE.md", 50000, "2026-01-02T00:00:00+00:00")
            git(d, "checkout", "-q", "main")
            write_commit(d, "CLAUDE.md", 200, "2026-01-03T00:00:00+00:00")
            git(d, "merge", "-q", "-s", "ours", "side", "-m", "merge",
                when="2026-01-04T00:00:00+00:00")
            self.assertNotIn(50000, [s for _, s in
                                     cb.size_history(d, "CLAUDE.md", first_parent=False)[0]])

    def test_presence_control_no_merge_means_the_two_views_agree(self):
        """Without this the D1 tests could be passing because --first-parent drops
        something unconditionally, rather than because it drops the foreign lineage."""
        with tempfile.TemporaryDirectory() as d:
            new_repo(d)
            write_commit(d, "CLAUDE.md", 100, "2026-01-01T00:00:00+00:00")
            write_commit(d, "CLAUDE.md", 200, "2026-01-03T00:00:00+00:00")
            self.assertEqual(cb.size_history(d, "CLAUDE.md")[0],
                             cb.size_history(d, "CLAUDE.md", first_parent=False)[0])

    def test_a_missing_target_is_an_empty_history_not_an_error(self):
        with tempfile.TemporaryDirectory() as d:
            new_repo(d)
            write_commit(d, "other.md", 10, "2026-01-01T00:00:00+00:00")
            hist, skipped, err = cb.size_history(d, "CLAUDE.md")
            self.assertEqual((hist, skipped, err), ([], 0, None))

    def test_a_non_repository_surfaces_the_error_never_an_empty_history(self):
        """'no history' and 'git could not run' must not be the same value — that
        conflation is the defect run() was written to avoid (tool docstring :54)."""
        with tempfile.TemporaryDirectory() as d:
            hist, _, err = cb.size_history(d, "CLAUDE.md")
            self.assertIsNone(hist)
            self.assertTrue(err)


# ---------------------------------------------------------------------------------
# D2 — timezone. git %cI emits a numeric offset that moves with the season; transcripts
# end in Z. Ordered as STRINGS that is not chronological.
# ---------------------------------------------------------------------------------

def _string_size_at(hist_iso, iso):
    """The shipped pre-change comparison, verbatim (context_budget.py:402/:410 at blob
    be2721a): sort ISO strings, take the last one <= the target string."""
    best = None
    for when, size in sorted(hist_iso):
        if when <= iso:
            best = size
    return best


class TestTimezone(unittest.TestCase):

    # The real pair from this framework's own repository: commit 7603f10 shrank CLAUDE.md
    # 52,909 -> 8,519 B at 19:42:50-05:00, which is 2026-08-02T00:42:50Z — AFTER a session
    # that opened at 2026-08-01T21:25:28Z. String order says the opposite.
    COMMIT = "2026-08-01T19:42:50-05:00"
    SESSION = "2026-08-01T21:25:28Z"

    def test_fixture_the_string_comparison_really_is_wrong_here(self):
        """PROVE THE FIXTURE. If these strings did not mis-order, the pair would be a
        decoration rather than a regression test."""
        self.assertLess(self.COMMIT, self.SESSION, "chosen pair does not mis-order as strings")
        self.assertGreater(cb.parse_iso(self.COMMIT), cb.parse_iso(self.SESSION),
                           "chosen pair is not actually inverted in real time")

    def test_size_at_scores_the_session_against_the_size_that_was_live(self):
        hist = [(cb.parse_iso("2026-07-20T12:00:00-04:00"), 52909),
                (cb.parse_iso(self.COMMIT), 8519)]
        self.assertEqual(cb.size_at(hist, cb.parse_iso(self.SESSION)), 52909)

    def test_the_defect_it_replaces_scores_it_against_the_wrong_size(self):
        """DRIVE IT RED against the narrowed implementation."""
        hist_iso = [("2026-07-20T12:00:00-04:00", 52909), (self.COMMIT, 8519)]
        self.assertEqual(_string_size_at(hist_iso, self.SESSION), 8519)

    # A DST-straddling pair whose lexical order is the REVERSE of its real order. Not
    # every mixed-offset pair inverts — the first pair tried here did not, which is why
    # the fixture is asserted below before it is relied on.
    EARLIER = "2026-08-01T20:00:00-04:00"     # = 2026-08-02T00:00:00Z, first in real time
    LATER = "2026-08-01T19:30:00-05:00"       # = 2026-08-02T00:30:00Z, second in real time

    def test_fixture_the_dst_pair_really_inverts(self):
        """PROVE THE FIXTURE, again: lexically LATER sorts before EARLIER."""
        self.assertLess(self.LATER, self.EARLIER, "pair does not invert lexically")
        self.assertLess(cb.parse_iso(self.EARLIER), cb.parse_iso(self.LATER),
                        "pair is not in the claimed real-time order")

    def test_history_is_ordered_chronologically_not_lexically(self):
        """A repository whose commits straddle a DST boundary — every long-lived one."""
        with tempfile.TemporaryDirectory() as d:
            new_repo(d)
            write_commit(d, "CLAUDE.md", 100, self.EARLIER)
            write_commit(d, "CLAUDE.md", 200, self.LATER)
            hist, _, _ = cb.size_history(d, "CLAUDE.md")
            self.assertEqual([s for _, s in hist], [100, 200])
            # The narrowed implementation orders the same two records the other way.
            self.assertEqual([s for _, s in sorted([(self.EARLIER, 100), (self.LATER, 200)])],
                             [200, 100])

    def test_offsets_and_z_agree_on_the_instant(self):
        self.assertEqual(cb.parse_iso("2026-08-02T00:42:50Z"), cb.parse_iso(self.COMMIT))
        self.assertEqual(cb.parse_iso("2026-08-02T02:42:50+02:00"), cb.parse_iso(self.COMMIT))

    def test_unparseable_stamps_are_counted_not_silently_dropped(self):
        self.assertIsNone(cb.parse_iso("yesterday"))
        self.assertIsNone(cb.parse_iso(""))
        self.assertIsNone(cb.parse_iso("2026-02-30T00:00:00Z"))     # shape ok, date not

    def test_a_naive_stamp_is_read_as_utc(self):
        """Documented assumption, pinned so it is a decision rather than an accident."""
        self.assertEqual(cb.parse_iso("2026-08-02T00:42:50"), cb.parse_iso("2026-08-02T00:42:50Z"))


# ---------------------------------------------------------------------------------
# D3 — goodness of fit. The tool must not hand back a constant it cannot support.
# ---------------------------------------------------------------------------------

class TestFitGate(unittest.TestCase):

    def test_a_known_line_is_recovered_exactly(self):
        slope, inter, r2 = cb.linfit([(x, 3*x + 7) for x in range(1, 12)])
        self.assertAlmostEqual(slope, 3.0, places=9)
        self.assertAlmostEqual(inter, 7.0, places=9)
        self.assertAlmostEqual(r2, 1.0, places=9)

    def test_this_repos_own_four_way_fit_is_reproduced_from_its_recorded_points(self):
        """The BL-38 table is a claim about arithmetic; this pins the arithmetic itself.
        Points chosen so the corrected fit is strong and the scrambled one is not."""
        good = [(8519, 45000), (11064, 46000), (20000, 49000), (52909, 61000)]
        _, _, r2_good = cb.linfit(good)
        self.assertGreater(r2_good, 0.9)
        scrambled = [(8519, 61000), (11064, 45000), (20000, 46000), (52909, 49000)]
        _, _, r2_bad = cb.linfit(scrambled)
        self.assertLess(r2_bad, cb.MIN_R2)

    def test_no_regressor_variance_is_None_not_a_fabricated_line(self):
        self.assertIsNone(cb.linfit([(5, 1), (5, 2), (5, 3)]))

    def test_no_response_variance_leaves_r2_undefined_never_perfect(self):
        self.assertIsNone(cb.linfit([(1, 9), (2, 9), (3, 9)])[2])

    def test_the_floor_admits_and_refuses(self):
        self.assertIsNone(cb.calibration_verdict(0.3557, 0.8054, cb.MIN_R2))
        self.assertIsNotNone(cb.calibration_verdict(0.0678, 0.0503, cb.MIN_R2))

    def test_the_boundary_is_inclusive(self):
        """A floor that refused its own boundary value would be a different floor."""
        self.assertIsNone(cb.calibration_verdict(0.3557, cb.MIN_R2, cb.MIN_R2))
        self.assertIsNotNone(cb.calibration_verdict(0.3557, cb.MIN_R2 - 1e-9, cb.MIN_R2))

    def test_a_negative_slope_is_refused_however_tight_the_fit(self):
        """NARROWED-GUARD CHECK. An R²-only gate — the obvious weaker implementation —
        would accept this and print a NEGATIVE bytes-per-token."""
        self.assertIsNotNone(cb.calibration_verdict(-0.3557, 0.999, cb.MIN_R2))

    def test_an_undefined_r2_is_refused(self):
        self.assertIsNotNone(cb.calibration_verdict(0.3557, None, cb.MIN_R2))

    def test_the_refusal_says_which_test_failed(self):
        """A refusal that does not name its cause sends the reader back to the source."""
        self.assertIn("R²", cb.calibration_verdict(0.0678, 0.0503, cb.MIN_R2))
        self.assertIn("slope", cb.calibration_verdict(-0.3557, 0.999, cb.MIN_R2))

    def test_the_floor_is_configurable_per_project(self):
        self.assertIsNone(cb.calibration_verdict(0.3557, 0.30, 0.25))
        self.assertIsNotNone(cb.calibration_verdict(0.3557, 0.30, 0.75))


class TestFitGateEndToEnd(unittest.TestCase):
    """The unit gate above proves the verdict; this proves calibrate() ACTS on it — that
    a refused fit suppresses the number rather than printing it with a caveat beside it.

    It can only run where transcripts for this repository exist, which is a developer
    machine and not CI, so it skips rather than failing. Skipped is honest; asserting
    against whatever transcripts happen to be present would not be.
    """

    def setUp(self):
        slug = "-" + str(REPO).strip("/").replace("/", "-")
        self.tdir = Path.home() / ".claude" / "projects" / slug
        if not self.tdir.exists() or not any(self.tdir.glob("*.jsonl")):
            self.skipTest(f"no transcripts at {self.tdir}")
        cfgp = REPO / ".context-budget.json"
        if not cfgp.exists():
            self.skipTest("this repo has no .context-budget.json")
        self.cfg = json.loads(cfgp.read_text())

    def _run(self, floor):
        import contextlib, io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = cb.calibrate(str(REPO), {**self.cfg, "calibrate_min_r2": floor})
        return rc, buf.getvalue()

    def test_an_impossible_floor_suppresses_the_constant_entirely(self):
        rc, out = self._run(1.01)
        self.assertEqual(rc, cb.WARN)
        self.assertIn("no constant recommended", out)
        self.assertNotIn("bytes/token", out)

    def test_an_admitting_floor_prints_the_constant(self):
        """Presence control: without it, a calibrate() that never printed anything would
        pass the test above."""
        rc, out = self._run(0.0)
        self.assertEqual(rc, cb.CLEAN)
        self.assertIn("bytes/token", out)
        self.assertNotIn("no constant recommended", out)


# ---------------------------------------------------------------------------------
# D4 / D5 — what the ledger row and the remediation text say.
# ---------------------------------------------------------------------------------

class TestLedgerRow(unittest.TestCase):

    OVER_BYTES = {"class": "read-mandated", "lines": 359, "max_lines": 1200,
                  "bytes": 72449, "max_bytes": 65536, "status": "over",
                  "findings": [{"kind": "bytes", "msg": "x"}]}

    def test_a_read_mandated_file_over_BYTES_reports_bytes(self):
        self.assertEqual(cb.ledger_dimension(self.OVER_BYTES), ("72,449 B", "65,536 B"))

    def test_the_defect_it_replaces_named_the_ceiling_that_did_not_fire(self):
        """DRIVE IT RED against the narrowed implementation: class-only selection, which
        is what the tool did, reports lines for this row — the ceiling that passed."""
        r = self.OVER_BYTES
        by_class = (f"{r['lines']:,} ln" if r["class"] == "read-mandated"
                    else f"{r['bytes']:,} B")
        self.assertEqual(by_class, "359 ln")
        self.assertNotEqual(by_class, cb.ledger_dimension(r)[0])

    def test_a_read_mandated_file_over_LINES_still_reports_lines(self):
        r = {**self.OVER_BYTES, "lines": 1500,
             "findings": [{"kind": "lines", "msg": "x"}]}
        self.assertEqual(cb.ledger_dimension(r), ("1,500 ln", "1,200 ln"))

    def test_over_both_reports_bytes_deterministically(self):
        r = {**self.OVER_BYTES, "lines": 1500,
             "findings": [{"kind": "bytes", "msg": "x"}, {"kind": "lines", "msg": "y"}]}
        self.assertEqual(cb.ledger_dimension(r)[0], "72,449 B")

    def test_nothing_fired_falls_back_to_the_class(self):
        self.assertEqual(cb.ledger_dimension({**self.OVER_BYTES, "findings": [],
                                              "status": "ok"}), ("359 ln", "1,200 ln"))
        self.assertEqual(cb.ledger_dimension({"class": "resident", "bytes": 900,
                                              "lines": 9, "max_bytes": 1000,
                                              "findings": []}), ("900 B", "1,000 B"))

    def test_a_non_size_finding_does_not_hijack_the_dimension(self):
        r = {**self.OVER_BYTES, "findings": [{"kind": "protected", "msg": "x"}]}
        self.assertEqual(cb.ledger_dimension(r)[0], "359 ln")

    def test_an_undeclared_ceiling_renders_rather_than_crashing(self):
        """The pre-change expression formatted max_bytes unconditionally, so a resident
        file declaring only max_lines raised TypeError inside the renderer."""
        self.assertEqual(cb.ledger_dimension({"class": "resident", "bytes": 10,
                                              "lines": 1, "findings": []}), ("10 B", "—"))

    def test_the_resident_total_pseudo_row_renders(self):
        """main() appends a synthetic row that has no line count at all."""
        self.assertEqual(cb.ledger_dimension(
            {"path": "(resident total)", "class": "resident", "status": "over",
             "bytes": 20000, "max_bytes": 18600,
             "findings": [{"kind": "bytes", "msg": "x"}]}), ("20,000 B", "18,600 B"))


class TestRemediationText(unittest.TestCase):

    def test_no_remedy_names_a_directory_from_the_tools_home_project(self):
        """server/, mobile/*/ and database/ exist in no repository but the one the tool
        was written in, and were printed verbatim to every adopter."""
        for kind, remedies in cb.REMEDIES.items():
            for name, how in remedies:
                for token in ("server/", "mobile/", "database/"):
                    self.assertNotIn(token, how, f"{kind}/{name} names {token}")

    def test_measured_claims_are_attributed_not_deictic(self):
        """'10 of 11 rows of one table HERE were wrong' reads, in an adopter's terminal,
        as a claim about the adopter's own repository. It was never measured there."""
        compute = dict((n, h) for n, h in cb.REMEDIES["bytes"])["Compute"]
        self.assertIn("10 of 11", compute)
        self.assertNotIn("table here", compute)

    def test_raising_the_ceiling_is_still_offered_last(self):
        """Ordering is the message: it is the only remedy that removes the signal."""
        self.assertEqual(cb.REMEDIES["bytes"][-1][0], "Raise the ceiling")


class TestToolInvariants(unittest.TestCase):

    def test_the_tool_and_its_selftest_agree_the_gates_all_fire(self):
        p = subprocess.run([sys.executable, str(CB_PY), "--selftest"],
                           capture_output=True, text=True, cwd=str(REPO))
        rows = [l for l in p.stdout.splitlines() if l.strip().startswith(("PASS", "FAIL"))]
        self.assertGreater(len(rows), 30, "selftest row population collapsed")
        self.assertEqual([l for l in rows if l.strip().startswith("FAIL")], [])

    def test_there_is_still_no_force_escape_hatch(self):
        src = CB_PY.read_text().split("def selftest")[0]
        self.assertNotIn('"--force" in args', src)


if __name__ == "__main__":
    unittest.main(verbosity=1)
