#!/usr/bin/env python3
"""Tests for p1b_score.py, the glue that ran the frozen scorer once over the saved runs (BL-94 P1b). They test the driver, not the
scorer: the scorer's own tests are tests_doc_score.py, and the scorer is frozen. Run: python3 tests_p1b.py. stdlib only."""
import io, json, os, shutil, sys, tempfile, unittest
from contextlib import redirect_stdout
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import p1b_score as P

SAVED = os.path.join(P.EVIDENCE, "p1b-scores.json")


def fake_run(rid, group, accuracy, coverage, cost, commits=3, flag=False, cost_valid=None, included=True, arm=None, reply=None):
    r = {"id": rid, "group": group, "arm": arm or group, "ratchet": None, "reply": reply, "cli": ["2.1.287"], "included": included,
         "cost_usd": cost, "requests": 50, "tool_calls": 70, "cost_valid": cost_valid, "row_end": "close-out complete", "task_done": not flag}
    if included:
        r["score"] = {"record": {"lines": 100}, "m1": {"accuracy": accuracy, "checkable": 40, "failures": [], **{k: {"checkable": 10, "verified": 10} for k in ("shas", "paths", "anchors", "counts")}},
                      "m2": {"a": {"coverage": coverage, "commits": commits - 1, "missing": []}, "b": None, "b_descriptive": {"receipts": [], "changelog_markers": []},
                             "c": {"flag": flag, "says_done": True, "task_done": not flag}, "says_done": True, "commit_slot": ""}}
        r["key"] = {"git_derivable": {"session": "S1", "deliverable_terms": ["#1"], "deliverable_commit": "abc", "complete": True},
                    "record_only": {"paths": ["a.md"], "shas": []}}
    return r


class Pieces(unittest.TestCase):
    def test_group_of_puts_every_t_control_run_in_v38_text_and_keeps_s237_arms(self):
        self.assertEqual(P.group_of("real-3.7", "v3.0"), "v3.0")
        self.assertEqual(P.group_of("real-3.7", "v3.7"), "v3.7")
        self.assertEqual(P.group_of("t-control", "R0"), "v3.8-text")
        self.assertEqual(P.group_of("t-control-fix", "R1"), "v3.8-text")

    def test_task_check_needs_no_failures_and_no_errors_in_any_held_out_file(self):
        ok = {"a.R": [0, 0, 0, 6], "b.R": [0, 0, 5, 43]}          # warnings do not fail the check, as in S237's own reading
        self.assertTrue(P.task_from_held_out(ok))
        self.assertFalse(P.task_from_held_out({"a.R": [0, 0, 0, 6], "b.R": [4, 0, 0, 6]}))
        self.assertFalse(P.task_from_held_out({"a.R": [0, 1, 0, 6]}))

    def test_measured_counts_come_only_from_a_row_that_has_them(self):
        self.assertIsNone(P.measured_from_row({"cost_usd": 1}))
        self.assertEqual(P.measured_from_row({"final_measure": {"passed": 5, "failed": 1, "warnings": 0, "files": 9}}), {"passed": 5, "failed": 1, "warnings": 0})

    def test_run_inputs_use_the_held_out_file_for_s237_and_the_row_for_t_control(self):
        held = {"v3.0-r1": {"held_out": {"a.R": [0, 0, 0, 6]}}, "v3.0-r4": {"held_out": {"a.R": [4, 0, 0, 6]}}}
        self.assertEqual(P.run_inputs({"set": "real-3.7", "arm": "v3.0", "rep": 1}, {}, held), (True, None))
        self.assertEqual(P.run_inputs({"set": "real-3.7", "arm": "v3.0", "rep": 4}, {}, held), (False, None))
        self.assertEqual(P.run_inputs({"set": "real-3.7", "arm": "v3.0", "rep": 2}, {}, held), (None, None))     # no result: unknown, never "done"
        row = {"ratchet": {"task_done": False}, "final_measure": {"passed": 3, "failed": 1}}
        self.assertEqual(P.run_inputs({"set": "t-control", "arm": "R1", "rep": 1}, row, held), (False, {"passed": 3, "failed": 1}))

    def test_sample_sd_and_spread(self):
        self.assertIsNone(P.sd([1.0]))
        self.assertAlmostEqual(P.sd([1, 2, 3]), 1.0)
        self.assertEqual(P.spread([None, None])["n"], 0)
        s = P.spread([1, 3, None])
        self.assertEqual((s["n"], s["mean"], s["min"], s["max"]), (2, 2, 1, 3))

    def test_permutation_p_is_exact_for_a_small_case_and_one_for_equal_means(self):
        self.assertAlmostEqual(P.perm_p([1, 2, 3], [4, 5, 6]), 2 / 20)      # the observed split and its mirror, of C(6,3) = 20
        self.assertEqual(P.perm_p([1, 2, 3], [1, 2, 3]), 1.0)
        self.assertIsNone(P.perm_p([], [1]))

    def test_the_sample_size_formula_is_the_plans(self):
        self.assertEqual(P.n_per_arm(0.15, 0.20), 9)                          # plan 3.8's own example: sigma 0.15, d 0.20, n about 9
        self.assertEqual(P.n_per_arm(0.20, 0.20), 16)                         # 15.7 exactly; a constant of 15 would say 15
        self.assertIsNone(P.n_per_arm(0.0))
        self.assertIsNone(P.n_per_arm(None))

    def test_commits_are_counted_to_the_pin_not_to_head(self):
        r = fake_run("x", "v3.7", 1.0, 1.0, 3.0, commits=6)
        r["commits_after_start"] = 18
        self.assertEqual(P.process_of(r)["commits"], 6)

    def test_cost_valid_drops_only_a_run_marked_invalid(self):
        runs = [fake_run("a", "v3.7", 1, 1, 1, cost_valid=True), fake_run("b", "v3.7", 1, 1, 1, cost_valid=False), fake_run("c", "v3.8-text", 1, 1, 1, cost_valid=None)]
        self.assertEqual([r["id"] for r in P.cost_valid(runs)], ["a", "c"])


class Refusals(unittest.TestCase):
    def test_a_changed_scorer_is_refused(self):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        copy = os.path.join(d, "doc_score.py")
        shutil.copy(P.SCORER, copy)
        with open(copy, "a") as f:
            f.write("\n")
        old = P.SCORER
        P.SCORER = copy
        self.addCleanup(setattr, P, "SCORER", old)
        with self.assertRaises(SystemExit):
            P.require_frozen()

    def test_the_real_scorer_passes_the_freeze_check(self):
        P.require_frozen()

    def test_a_second_scoring_run_is_refused_unless_asked_for(self):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        out = os.path.join(d, "scores.json")
        with open(out, "w") as f:
            f.write("{}")
        with self.assertRaises(SystemExit) as cm:
            P.collect(None, again=False, out=out)
        self.assertIn("scores once", str(cm.exception))


class Summaries(unittest.TestCase):
    def data(self):
        runs = [fake_run("a1", "v3.0", 1.0, 1.0, 2.0), fake_run("a2", "v3.0", 0.9, 1.0, 3.0, flag=True),
                fake_run("b1", "v3.7", 1.0, 0.8, 3.0, cost_valid=True), fake_run("b2", "v3.7", 1.0, 1.0, 9.0, cost_valid=False),
                fake_run("c1", "v3.8-text", 0.96, 1.0, 4.0, arm="R1", reply="old"), fake_run("c2", "v3.8-text", 0.96, 1.0, 5.0, arm="R1", reply="fixed"),
                fake_run("x", "v3.7", None, None, 1.0, included=False)]
        return {"runs": {r["id"]: r for r in runs}}

    def test_summary_counts_scored_runs_per_group_and_lists_the_excluded(self):
        s = P.summarize(self.data())
        self.assertEqual({g: x["n"] for g, x in s["groups"].items()}, {"v3.0": 2, "v3.7": 2, "v3.8-text": 2})
        self.assertEqual([e["id"] for e in s["excluded"]], ["x"])
        self.assertEqual(s["groups"]["v3.0"]["m2c_flags"], ["a2"])
        self.assertEqual(s["groups"]["v3.7"]["m2a"]["min"], 0.8)

    def test_process_rows_leave_out_the_cost_invalid_run_but_the_documentation_rows_keep_it(self):
        s = P.summarize(self.data())
        self.assertEqual(s["groups"]["v3.7"]["process"]["cost_usd"]["mean"], 3.0)          # b2 (9.0) is cost-invalid
        self.assertEqual(s["groups"]["v3.7"]["m1"]["n"], 2)                                 # and still scored on M1
        self.assertEqual(s["pooling_span"]["cost_usd"]["hi"], 3.0)                          # the span the pooling check reads leaves it out too

    def test_the_ceiling_verdict_follows_the_rule(self):
        d = self.data()
        self.assertFalse(P.summarize(d)["m1_at_ceiling"])                                    # 0.9 is below 0.95
        for r in d["runs"].values():
            if r["included"]:
                r["score"]["m1"]["accuracy"] = 0.97
        self.assertTrue(P.summarize(d)["m1_at_ceiling"])

    def test_the_report_prints_from_the_saved_scores_alone(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            P.report({"scorer_sha256": "0" * 64, "scorer_frozen": {"frozen": "2026-10-03"}, "manifest_sha256": "1" * 64, "again": False, **self.data()})
        out = buf.getvalue()
        self.assertIn("Not scored", out)
        self.assertIn("v3.8-text", out)


@unittest.skipUnless(os.path.exists(SAVED), "the saved scores are not in this tree")
class SavedScores(unittest.TestCase):
    """The committed output of the one scoring run: its shape, not a re-score."""

    @classmethod
    def setUpClass(cls):
        with open(SAVED) as f:
            cls.data = json.load(f)

    def test_it_was_scored_by_the_frozen_scorer_once(self):
        self.assertEqual(self.data["scorer_sha256"], P.frozen_sha())
        self.assertFalse(self.data["again"])

    def test_the_inclusion_rule_left_out_exactly_the_three_runs_p1a_named(self):
        out = sorted(r["id"] for r in self.data["runs"].values() if not r["included"])
        self.assertEqual(out, ["real-3.7/v3.0-r2", "real-3.7/v3.7-r1", "t-control-fix/R1-r1"])

    def test_the_scored_runs_are_five_six_and_twelve(self):
        s = P.summarize(self.data)
        self.assertEqual({g: x["n"] for g, x in s["groups"].items()}, {"v3.0": 5, "v3.7": 6, "v3.8-text": 12})

    def test_every_scored_run_carries_a_final_message_and_a_task_check(self):
        for r in self.data["runs"].values():
            if r["included"]:
                self.assertTrue(r["final_message"].strip(), r["id"])
                self.assertIsNotNone(r["task_done"], r["id"])


if __name__ == "__main__":
    unittest.main()
