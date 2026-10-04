#!/usr/bin/env python3
"""Tests for rater.py (BL-94 P2a (d)): the blind rater, the planted-defect set and the operator's packet. No model, no spend: the rating
call is a stand-in function. Synthetic records only, apart from one check that the CLI still lists the rater's flags.

    python3 docs/planning/overhead-replay/tests_rater.py
"""
import csv, json, os, shutil, subprocess, sys, tempfile, unittest
from unittest import mock
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rater as R
import probe

SHA = "a1b2c3d4e5f6"
RECORD = {"docs": [["### S9 close-out", "- Deliverable: fix #7 in `R/x.R:24`. Commits: `%s` and `0f9e8d7c`." % SHA, "- Checked: 3754 expectations pass.",
                    "", "key_files: `R/x.R:24`, tests/test_x.R", "", "next_steps: Run `tests/test_x.R` first; then fix `R/y.R:9`.", "gotchas: the cache is stale"],
                   ["Handoff", "Next session", "1. open R/y.R", "2. add a test", "", "Other paragraph."]],
          "final": ["Fixed #7 in %s. Done." % SHA, "", "## Next steps", "1. Start in R/y.R:9", "", "Thanks."]}


def sample_records():
    mk = lambda g, i: (g, {"docs": [list(d) for d in RECORD["docs"]], "final": list(RECORD["final"])})
    return {f"set/{g}-r{i}": mk(g, i) for g, n in (("v3.0", 5), ("v3.7", 6), ("v3.8-text", 12)) for i in range(1, n + 1)}


def reply(answers=None, arm="3.7", cost=0.1, **env):
    a = dict.fromkeys(R.KEYS, "yes")
    a.update(answers or {})
    result = json.dumps({"answers": a, "arm_guess": arm, "reason": "because"})
    return subprocess.CompletedProcess([], 0, json.dumps({"type": "result", "subtype": "success", "is_error": False, "result": result, "total_cost_usd": cost, **env}), "")


class Rendering(unittest.TestCase):
    def test_no_file_name_run_id_or_arm_reaches_the_rater(self):
        text = R.render(RECORD)
        self.assertIn("=== Document 1 (text added by the session) ===", text)
        self.assertIn("=== Document 2 (text added by the session) ===", text)
        self.assertIn("=== The session's final message ===", text)
        for forbidden in ("SESSION_NOTES", "HANDOFFS", "CHANGELOG", "set/v3"):
            self.assertNotIn(forbidden, text)

    def test_record_docs_drops_file_names_keeps_blank_lines_and_skips_empty_files(self):
        rec = {"raw": {"b.md": ["x", "", "y"], "a.md": ["p"], "c.md": ["", ""]}}
        rd = R.record_docs(rec, "end\n\nmore")
        self.assertEqual(rd["docs"], [["p"], ["x", "", "y"]])                    # path order; the file with only blanks is gone
        self.assertEqual(rd["final"], ["end", "", "more"])


class Defects(unittest.TestCase):
    def test_a_next_step_paragraph_ends_at_a_blank_line_a_heading_a_fence_or_a_receipt_field(self):
        base = ["next_steps: one line", "key_files: keep me"]
        self.assertEqual(R.drop_parts(base)[0], ["key_files: keep me"])
        self.assertEqual(R.drop_parts(["Next session", "1. a", "2. b", "", "keep"])[0], ["", "keep"])
        self.assertEqual(R.drop_parts(["## Next steps", "1. a", "## Other", "keep"])[0], ["## Other", "keep"])
        self.assertEqual(R.drop_parts(["Next up", "x", "```", "keep"])[0], ["```", "keep"])
        self.assertEqual(R.drop_parts(["keep", "no label here"])[0], ["keep", "no label here"])

    def test_the_label_set_covers_the_forms_the_real_records_use_and_not_a_mention(self):
        """S259: all three real records carry a `**=> SUGGESTED NEXT.**` paragraph, which the scorer's label set (and so this builder's) did not
        name, so `missing` left the next step in and the rater's yes was right."""
        for line in ("**=> SUGGESTED NEXT.** Owner's pick. (1) **From a checkout", "**=> SUGGESTED NEXT (recommendations, not predictions).** **#121 is fixed",
                     "next_steps: run the tests", "## Next session", "**Next session** (details in the receipt)", "Next up: the audit", "What's next",
                     "Recommended next step: close it", "natural next task is #120", "Next task: the audit", "Next action: merge", "- **Next steps:** 1. do x"):
            self.assertTrue(R.NEXT_LABEL.match(line), line)
        for line in ("**Gotchas for next session.** (1) the cache", "The next steps were done", "Nextcloud is down", "Key files (this session). `R/x.R`",
                     "so the next session starts", "(see next steps)", "Suggested reading: the plan"):
            self.assertFalse(R.NEXT_LABEL.match(line), line)

    def test_a_suggested_next_paragraph_goes_whole_and_its_neighbours_stay(self):
        lines = ["**Learnings:** one.", "", "**=> SUGGESTED NEXT.** Owner's pick. (1) **Close it:** `gh issue close 121`", "with a pointer. (2) Issue #120 (the audit).",
                 "(3) Decide the ticket.", "", "**Key files.** `R/x.R:26-32`", "", "**Gotchas for next session.** (1) renv is not restored."]
        out, _ = R.drop_parts(lines)
        self.assertEqual(out, ["**Learnings:** one.", "", "", "**Key files.** `R/x.R:26-32`", "", "**Gotchas for next session.** (1) renv is not restored."])

    def test_a_line_that_starts_with_an_issue_number_does_not_end_a_next_step_paragraph(self):
        """S260, found by reading the v3.8 record after the rebuild: `#28/#12/#11/#10/#5; the CRAN thread` is not a heading, and treating it as
        one left the rest of the SUGGESTED NEXT block (its follow-ups) in a record whose next step was supposed to be gone."""
        lines = ["**=> SUGGESTED NEXT.** (1) close it; (2) issue #120 (the audit); #116", "(BLOCKED); #103 roxygen;", "#28/#12/#11/#10/#5; the CRAN thread.",
                 "**3. Small follow-ups I did NOT do:**", "(a) the advisory fires twice", "", "**Key files.** x"]
        self.assertEqual(R.drop_parts(lines)[0], ["", "**Key files.** x"])
        self.assertEqual(R.drop_parts(["Next up", "#1 first", "#### a heading", "keep"])[0], ["#### a heading", "keep"])      # a real heading still ends it
        self.assertEqual(R.drop_parts(["Next up", "x", "#nospace is not one"])[0], [])

    def test_the_line_each_removal_stopped_at_is_reported(self):
        ends = []
        R.drop_parts(["keep", "next_steps: a", "key_files: b", "Next up", "x", "", "keep", "Next session", "y"], ends=ends)
        self.assertEqual(ends, ["key_files: b", "", None])                      # a receipt field, a blank line, the end of the text

    def test_missing_removes_every_next_step_part_and_nothing_else(self):
        out = R.defect_missing(RECORD)
        text = R.render(out)
        self.assertNotIn("next_steps:", text)
        self.assertNotIn("Next session", text)
        self.assertNotIn("Next steps", text)
        self.assertIn("key_files:", text)
        self.assertIn("gotchas: the cache is stale", text)
        self.assertIn("Other paragraph.", text)
        self.assertIn("Thanks.", text)

    def test_wrong_states_the_contradiction_once_where_the_first_next_step_was(self):
        out = R.defect_wrong(RECORD)
        self.assertEqual(R.render(out).count(R.NEW_NEXT), 1)
        self.assertEqual(out["docs"][0].index(R.NEW_NEXT), 6)                    # in place of next_steps:, between the blank line and gotchas:
        self.assertNotIn("Run `tests/test_x.R` first", R.render(out))

    def test_wrong_appends_the_contradiction_to_a_record_that_has_no_next_step(self):
        rd = {"docs": [["just a note"]], "final": ["Done."]}
        self.assertEqual(R.defect_wrong(rd)["final"][-1], R.NEW_NEXT)

    def test_vague_removes_every_way_the_records_name_a_place_in_the_code(self):
        """S259: no path or anchor survived `vague`, but 273 to 338 backticked spans and 19 to 24 function names did per real record, and the
        question asks for a file, a function OR a location, so the rater's yes was right."""
        line = ("Fixed `getPedMaxAge()` in `R/getPedMaxAge.R:26-32` (see `NA_real_`); then qcStudbook() and pkg::fn, via getPyramidPlot and spell_check_package, "
                "at L512/L763-765, line 24 and §11. Run `RENV_CONFIG_AUTOLOADER_ENABLED=FALSE Rscript x`, not `gh issue close 121`.")
        out = R.defect_vague({"docs": [[line, "active_task: kept as a label", "key_files: `R/y.R:9`"]], "final": []})["docs"][0]
        for gone in ("getPedMaxAge", "R/", "NA_real_", "qcStudbook", "pkg::fn", "getPyramidPlot", "spell_check_package", "L512", "line 24", "§11", "RENV_CONFIG", "gh issue close", "`"):
            self.assertNotIn(gone, out[0], gone)
        self.assertEqual(out[1], "active_task: kept as a label")               # a receipt's field name is a label, not a place
        self.assertNotIn("R/y.R", out[2])
        self.assertTrue(out[2].startswith("key_files: "))
        self.assertEqual(R.location_tokens(out), [])
        self.assertIn("Fixed", out[0])                                          # ordinary words stay

    def test_each_character_is_one_token_and_a_name_inside_a_span_is_not_counted_again(self):
        self.assertEqual(R.location_tokens(["Fixed `getPedMaxAge()` here"]), ["`getPedMaxAge()`"])
        self.assertEqual(R.location_tokens(["see R/x.R:24 and qcStudbook() at line 7"]), ["R/x.R:24", "qcStudbook()", "line 7"])
        self.assertEqual(R.location_tokens(["key_files: R/x.R", "active_task: fix it"]), ["R/x.R"])           # a field's name is a label
        self.assertEqual(R.location_tokens(["ordinary words, 3754 and deadbeef"]), [])

    def test_vague_names_anchors_before_paths(self):
        out = R.defect_vague({"docs": [["see R/x.R:24"]], "final": []})["docs"][0][0]
        self.assertEqual(out, "see the relevant place")

    def test_vague_unwraps_a_span_that_was_only_a_path_and_names_the_rest_generically(self):
        out = R.defect_vague({"docs": [["See `R/x.R:24`, `tests/test_x.R` and `foo bar baz`."]], "final": []})["docs"][0][0]
        self.assertEqual(out, "See the relevant place, the relevant file and the relevant code.")

    def test_vague_replaces_paths_anchors_and_shas_and_leaves_ordinary_words_and_numbers(self):
        rd = {"docs": [["See `R/x.R:24` and tests/test_x.R; commit %s. deadbeef is a word, 1790738507 a number, 3754 a count." % SHA]], "final": []}
        line = R.defect_vague(rd)["docs"][0][0]
        self.assertNotIn("R/x.R", line)
        self.assertNotIn("test_x.R", line)
        self.assertNotIn(SHA, line)
        self.assertIn("deadbeef is a word, 1790738507 a number, 3754 a count", line)
        self.assertIn("the relevant place", line)
        self.assertIn("the commit", line)

    def test_fabricated_swaps_each_sha_for_an_invented_one_of_the_same_length_and_is_deterministic(self):
        a, b = R.defect_fabricated(RECORD), R.defect_fabricated(RECORD)
        self.assertEqual(a, b)
        self.assertNotIn(SHA, R.render(a))
        self.assertNotIn("0f9e8d7c", R.render(a))
        import re
        self.assertEqual(len(re.findall(r"`([0-9a-f]{12})`", a["docs"][0][1])), 1)    # the invented sha is the same length as the one it replaced
        self.assertIn("Run `tests/test_x.R` first", R.render(a))                  # nothing else moved

    def test_no_defect_changes_the_honest_record(self):
        before = json.dumps(RECORD, sort_keys=True)
        for fn, _ in R.DEFECTS.values():
            fn(RECORD)
        self.assertEqual(json.dumps(RECORD, sort_keys=True), before)

    def test_every_defect_changes_the_record_it_is_built_from(self):
        for name, (fn, _) in R.DEFECTS.items():
            self.assertTrue(R.changed(RECORD, fn(RECORD)), name)

    def test_the_defect_table_targets_are_real_questions_and_fabricated_is_reported_only(self):
        for name, (_, targets) in R.DEFECTS.items():
            self.assertTrue(set(targets) <= set(R.KEYS), name)
        self.assertEqual(R.DEFECTS["fabricated"][1], [])


class Evidence(unittest.TestCase):
    """S260 (d): a planted defect is only a test of the rater if it provably removed the evidence its question rests on. Each defect that has a
    finder (missing: next-step labels; vague: place-in-the-code tokens) is counted before and after, at $0, before any call is paid for."""
    def test_each_defect_with_a_finder_removes_its_evidence_from_a_record_that_has_some(self):
        c = R.defect_check(RECORD)
        self.assertEqual(sorted(c), ["missing", "vague"])                        # wrong and fabricated remove nothing a finder could count
        self.assertEqual((c["missing"]["targets"], c["vague"]["targets"]), (["next_step"], ["where"]))
        self.assertEqual((c["missing"]["before"], c["missing"]["after"]), (3, 0))          # next_steps:, "Next session", "## Next steps"
        self.assertGreater(c["vague"]["before"], 5)
        self.assertEqual((c["vague"]["after"], c["vague"]["left"]), (0, []))

    def test_the_boundary_each_next_step_removal_stopped_at_is_part_of_the_check(self):
        self.assertEqual(R.defect_check(RECORD)["missing"]["ends"], ["gotchas: the cache is stale", "", ""])     # a receipt field, then a blank line twice
        self.assertEqual(R.defect_check({"docs": [["Next up", "x"]], "final": []})["missing"]["ends"], ["<end of the text>"])
        self.assertEqual(R.defect_check(RECORD)["vague"].get("ends"), [])

    def test_a_surviving_cue_is_reported_beside_the_verdict_and_is_not_a_failure(self):
        rd = {"docs": [["Next steps: do x", "", "The gate stayed put (see next steps).", "**Gotchas for next session.** (1) the cache"]], "final": []}
        c = R.defect_check(rd)["missing"]
        self.assertEqual((c["before"], c["after"]), (1, 0))
        self.assertEqual(c["cue_lines_left"], ["The gate stayed put (see next steps)."])           # "for next session" is an addressee, not a next step
        self.assertEqual(R.problems_from({"r": {"missing": c}}), [])

    def test_a_defect_that_leaves_its_evidence_is_a_problem_naming_the_record_the_defect_and_what_is_left(self):
        broken = {"missing": (lambda rd: rd, ["next_step"]), "vague": (R.defect_vague, ["where"])}
        probs = R.check_defects({"set/v3.0-r1": ("v3.0", RECORD)}, broken)
        self.assertEqual(len(probs), 1)
        for word in ("set/v3.0-r1", "missing", "3 of 3", "next-step labels", "next_steps:"):
            self.assertIn(word, probs[0])
        self.assertEqual(R.check_defects({"set/v3.0-r1": ("v3.0", RECORD)}), [])

    def test_only_the_honest_set_is_checked(self):
        recs = sample_records()
        self.assertEqual(R.check_defects(recs, {"missing": (lambda rd: rd, ["next_step"])}).__len__(), 3)       # one per group, not one per run

    def test_a_record_with_none_of_the_evidence_is_not_a_failure_but_is_reported(self):
        c = R.defect_check({"docs": [["just a note"]], "final": ["Done."]})
        self.assertEqual((c["missing"]["before"], c["missing"]["after"], c["vague"]["before"], c["vague"]["after"]), (0, 0, 0, 0))
        self.assertEqual(R.problems_from({"r": c}), [])

    def test_the_report_lists_each_defect_before_and_after_and_says_which_failed(self):
        lines, problems = R.defects_report({"set/v3.0-r1": ("v3.0", RECORD)})
        self.assertEqual(problems, [])
        joined = "\n".join(lines)
        for word in ("set/v3.0-r1", "missing", "vague", "3 -> 0", "next-step labels", "location tokens", "removal ended at: 'gotchas: the cache is stale'"):
            self.assertIn(word, joined)
        lines, problems = R.defects_report({"set/v3.0-r1": ("v3.0", RECORD)}, {"missing": (lambda rd: rd, ["next_step"])})
        self.assertEqual(len(problems), 1)
        self.assertIn("LEAVES", "\n".join(lines))


class DefectsCommand(unittest.TestCase):
    def run_main(self, defects=None):
        import io
        from contextlib import redirect_stdout
        out = tempfile.mkdtemp(prefix="defects-")
        self.addCleanup(shutil.rmtree, out, ignore_errors=True)
        buf = io.StringIO()
        with mock.patch.object(R, "load_records", return_value=sample_records()), mock.patch.dict(R.DEFECTS, defects or {}):
            with redirect_stdout(buf):
                R.main(["defects", "--out", out])
        return buf.getvalue(), out

    def test_the_defects_command_writes_each_defective_record_and_prints_the_evidence_before_and_after(self):
        text, out = self.run_main()
        self.assertEqual(len([n for n in os.listdir(out) if n.endswith(".txt")]), 3 * len(R.DEFECTS))
        for word in ("missing", "vague", "3 -> 0", "location tokens", "removal ended at"):
            self.assertIn(word, text)

    def test_the_defects_command_fails_when_a_defect_leaves_its_evidence(self):
        with self.assertRaises(SystemExit) as c:
            self.run_main({"missing": (lambda rd: rd, ["next_step"])})
        self.assertIn("leaves the evidence", str(c.exception))
        self.assertIn("missing", str(c.exception))


class Prompt(unittest.TestCase):
    def test_the_record_sits_between_markers_and_both_orders_ask_every_question_once(self):
        a, b = R.prompt("RECORD TEXT\n", "A"), R.prompt("RECORD TEXT\n", "B")
        for p in (a, b):
            self.assertIn("----- BEGIN -----\nRECORD TEXT\n----- END -----", p)
            for k in R.KEYS:
                self.assertEqual(p.count(f"[{k}]"), 1)
        self.assertLess(a.index("[next_step]"), a.index("[loose_ends]"))
        self.assertGreater(b.index("[next_step]"), b.index("[loose_ends]"))     # B is the reverse

    def test_the_question_list_is_the_fixed_eight(self):
        self.assertEqual(R.KEYS, ["next_step", "where", "state", "evidence", "hazard", "commits", "consistent", "loose_ends"])


class Parsing(unittest.TestCase):
    def good(self, **kw):
        d = {"answers": dict.fromkeys(R.KEYS, "no"), "arm_guess": "3.8", "reason": "r"}
        d.update(kw)
        return json.dumps(d)

    def test_a_valid_reply_with_text_around_it_parses(self):
        p = R.parse_reply("Here you go:\n" + self.good() + "\nDone.")
        self.assertEqual((p["arm_guess"], p["answers"]["where"]), ("3.8", "no"))

    def test_each_defect_in_a_reply_is_refused(self):
        for text in ("no json at all", self.good(arm_guess="3.9"), self.good(answers={"next_step": "yes"}),
                     self.good(answers=dict.fromkeys(R.KEYS, "maybe")), self.good(answers={**dict.fromkeys(R.KEYS, "no"), "extra": "yes"}), ""):
            with self.assertRaises(ValueError, msg=text[:30]):
                R.parse_reply(text)

    def test_totals_count_yes_and_cannot_tell(self):
        p = R.parse_reply(self.good(answers={**dict.fromkeys(R.KEYS, "no"), "where": "yes", "state": "cannot_tell"}))
        self.assertEqual(R.total(p), {"yes": 1, "cannot_tell": 1, "of": 8})


class Calling(unittest.TestCase):
    def test_the_command_has_no_tools_no_session_no_settings_and_the_per_call_cap(self):
        a = R.rater_cmd("sonnet", "high", 0.75)
        self.assertEqual(a[a.index("--tools") + 1], "")
        self.assertEqual(a[a.index("--max-budget-usd") + 1], "0.75")
        self.assertEqual(a[a.index("--setting-sources") + 1], "")
        self.assertEqual(a[a.index("--output-format") + 1], "json")
        for f in ("--no-session-persistence", "--strict-mcp-config", "--disable-slash-commands"):
            self.assertIn(f, a)

    def test_the_installed_cli_still_lists_every_flag_the_rater_passes(self):
        self.assertEqual(probe.check_cli_flags(R.rater_cmd("sonnet", "high", 0.5)), probe.cli_flags(R.rater_cmd("sonnet", "high", 0.5)))

    def test_the_prompt_goes_on_stdin_in_an_empty_directory(self):
        seen = {}
        def run(argv, input=None, cwd=None, **kw):
            seen.update(input=input, listing=os.listdir(cwd), argv=argv)
            return reply()
        parsed, cost, err, raw = R.call_rater("THE PROMPT", ["claude"], run)
        self.assertEqual((seen["input"], seen["listing"]), ("THE PROMPT", []))
        self.assertEqual((parsed["arm_guess"], cost, err, raw), ("3.7", 0.1, None, None))               # a usable reply keeps no raw text

    def test_a_cli_error_an_unparseable_envelope_and_a_bad_reply_are_failures_that_still_report_their_cost(self):
        err = subprocess.CompletedProcess([], 1, json.dumps({"type": "result", "subtype": "error_max_budget_usd", "is_error": True, "total_cost_usd": 0.75}), "")
        self.assertEqual(R.call_rater("p", ["c"], lambda *a, **k: err)[1:3], (0.75, "CLI error error_max_budget_usd"))
        junk = subprocess.CompletedProcess([], 2, "not json", "boom")
        p, cost, e, _ = R.call_rater("p", ["c"], lambda *a, **k: junk)
        self.assertEqual((p, cost), (None, 0.0))
        self.assertIn("exit 2", e)
        bad = subprocess.CompletedProcess([], 0, json.dumps({"subtype": "success", "result": "I think so", "total_cost_usd": 0.2}), "")
        p, cost, e, _ = R.call_rater("p", ["c"], lambda *a, **k: bad)
        self.assertEqual((p, cost), (None, 0.2))
        self.assertIn("unusable reply", e)

    def test_a_failed_call_keeps_the_text_that_failed_so_its_cause_can_be_read(self):
        """S259: one of 31 real calls ("Unterminated string starting at ... char 171", $0.0635) left only that message; the reply was gone."""
        cut = '{"answers": {"next_step": "yes", "where": "ye'                       # a reply cut inside a string, as that one was
        unusable = subprocess.CompletedProcess([], 0, json.dumps({"subtype": "success", "result": cut, "total_cost_usd": 0.0635}), "")
        p, cost, e, raw = R.call_rater("p", ["c"], lambda *a, **k: unusable)
        self.assertEqual((p, cost, raw), (None, 0.0635, cut))
        self.assertIn("unusable reply", e)
        envelope = json.dumps({"type": "result", "subtype": "error_max_budget_usd", "is_error": True, "total_cost_usd": 0.75, "errors": ["over"]})
        self.assertEqual(R.call_rater("p", ["c"], lambda *a, **k: subprocess.CompletedProcess([], 1, envelope, ""))[3], envelope)
        out = R.call_rater("p", ["c"], lambda *a, **k: subprocess.CompletedProcess([], 2, "half a line", "boom"))[3]
        self.assertIn("half a line", out)
        self.assertIn("boom", out)
        notext = subprocess.CompletedProcess([], 0, json.dumps({"subtype": "success", "result": None, "total_cost_usd": 0.2}), "")
        self.assertEqual(R.call_rater("p", ["c"], lambda *a, **k: notext)[3], "")             # a reply with no text at all keeps an empty string, not None

    def test_the_text_kept_is_bounded_and_says_how_much_was_cut(self):
        big = "x" * (R.RAW_KEEP + 5000)
        r = subprocess.CompletedProcess([], 0, json.dumps({"subtype": "success", "result": big, "total_cost_usd": 0.1}), "")
        raw = R.call_rater("p", ["c"], lambda *a, **k: r)[3]
        self.assertTrue(raw.startswith("x" * R.RAW_KEEP))
        self.assertIn(str(len(big)), raw[R.RAW_KEEP:])
        self.assertLess(len(raw), R.RAW_KEEP + 100)
        exact = subprocess.CompletedProcess([], 0, json.dumps({"subtype": "success", "result": "y" * R.RAW_KEEP, "total_cost_usd": 0.1}), "")
        self.assertEqual(R.call_rater("p", ["c"], lambda *a, **k: exact)[3], "y" * R.RAW_KEEP)  # exactly at the bound is not cut


class Verdicts(unittest.TestCase):
    H = dict.fromkeys(R.KEYS, "yes")

    def test_a_defect_is_caught_when_a_targeted_yes_drops(self):
        d = {"missing": {**self.H, "next_step": "no"}}
        self.assertEqual(R.planted_check(self.H, d)["missing"]["verdict"], "caught")

    def test_a_defect_is_missed_when_nothing_targeted_drops(self):
        self.assertEqual(R.planted_check(self.H, {"missing": dict(self.H)})["missing"]["verdict"], "MISSED")

    def test_wrong_is_caught_by_either_of_its_two_questions(self):
        self.assertEqual(R.planted_check(self.H, {"wrong": {**self.H, "state": "cannot_tell"}})["wrong"]["verdict"], "caught")
        self.assertEqual(R.planted_check(self.H, {"wrong": {**self.H, "consistent": "no"}})["wrong"]["verdict"], "caught")

    def test_a_question_the_honest_record_already_failed_cannot_show_a_drop(self):
        h = {**self.H, "next_step": "no"}
        self.assertEqual(R.planted_check(h, {"missing": dict(h)})["missing"]["verdict"], "not testable")

    def test_fabricated_is_reported_never_required(self):
        self.assertEqual(R.planted_check(self.H, {"fabricated": dict(self.H)})["fabricated"]["verdict"], "reported only")

    def test_a_defect_caught_in_one_question_order_only_is_order_sensitive(self):
        caught = {"missing": {"verdict": "caught"}}
        missed = {"missing": {"verdict": "MISSED"}}
        self.assertEqual(R.combine_orders(caught, caught), {"missing": "caught"})
        self.assertEqual(R.combine_orders(caught, missed), {"missing": "order-sensitive"})
        self.assertEqual(R.combine_orders(missed, missed), {"missing": "MISSED"})


class DryRun(unittest.TestCase):
    def setUp(self):
        self.out = tempfile.mkdtemp(prefix="raterout-")
        self.addCleanup(shutil.rmtree, self.out, ignore_errors=True)
        self.calls = []

    def run_fn(self, fail_on=None):
        def run(argv, input=None, **kw):
            self.calls.append(input)
            if fail_on and fail_on in input:
                return reply({"next_step": "no"}, cost=0.2)
            return reply(cost=0.2)
        return run

    def test_one_honest_record_per_group_and_the_first_in_sorted_order(self):
        recs = sample_records()
        self.assertEqual(R.honest_set(recs), ["set/v3.0-r1", "set/v3.7-r1", "set/v3.8-text-r1"])

    def test_it_rates_each_honest_record_and_each_defect_in_both_orders_and_writes_every_cost_to_the_ledger(self):
        res = R.dry_run(sample_records(), 0.75, 100.0, self.out, run=self.run_fn())
        self.assertEqual(len(self.calls), 3 * (1 + len(R.DEFECTS)) * 2)             # 3 records x (honest + 4 defects) x 2 orders
        with open(os.path.join(self.out, "spend.jsonl")) as f:
            ledger = [json.loads(l) for l in f]
        self.assertEqual(len(ledger), len(self.calls))
        self.assertAlmostEqual(sum(x["cost_usd"] for x in ledger), 0.2 * len(self.calls))
        self.assertEqual(set(res["set/v3.0-r1"]), {"honest", *R.DEFECTS})
        self.assertEqual(R.__dict__["probe"].driver.spent(self.out), sum(x["cost_usd"] for x in ledger))

    def test_the_total_cap_is_checked_before_every_call_and_ends_the_run(self):
        with open(os.path.join(self.out, "spend.jsonl"), "w") as f:
            f.write(json.dumps({"cost_usd": 99.5}) + "\n")
        res = R.dry_run(sample_records(), 0.75, 100.0, self.out, run=self.run_fn())
        self.assertEqual(self.calls, [])                                              # 99.5 + 0.75 > 100: nothing was sent
        self.assertIn("refused", json.dumps(res))

    def test_a_ledger_that_fills_mid_run_stops_it_with_what_it_has(self):
        with open(os.path.join(self.out, "spend.jsonl"), "w") as f:
            f.write(json.dumps({"cost_usd": 98.9}) + "\n")
        R.dry_run(sample_records(), 0.75, 100.0, self.out, run=self.run_fn())
        self.assertEqual(len(self.calls), 2)                                          # 98.9 and 99.1 leave room for 0.75; 99.3 does not

    def test_the_summary_reports_caught_defects_the_arm_guess_the_cost_and_the_failures(self):
        recs = {k: v for k, v in sample_records().items() if k == "set/v3.0-r1"}
        def run(argv, input=None, **kw):
            self.calls.append(input)
            missing = "next_steps:" not in input and "Next steps" not in input
            return reply({"next_step": "no"} if missing else {}, cost=0.1)
        s = R.summarize_dry_run(R.dry_run(recs, 0.75, 100.0, self.out, run=run))
        r = s["records"]["set/v3.0-r1"]
        self.assertEqual(r["defects"]["missing"], "caught")
        self.assertEqual(r["defects"]["fabricated"], "reported only")
        self.assertEqual(r["honest_total"]["A"]["yes"], 8)
        self.assertEqual(r["order_disagreement"], [])
        self.assertEqual(len(s["arm_guesses"]), 2)
        self.assertAlmostEqual(s["cost_usd"], 0.1 * 10)
        self.assertEqual(s["failed_calls"], [])

    def test_each_result_carries_the_text_of_a_failed_call_and_none_for_a_good_one(self):
        recs = {k: v for k, v in sample_records().items() if k == "set/v3.0-r1"}
        bad = subprocess.CompletedProcess([], 0, json.dumps({"subtype": "success", "result": '{"answers": {"next', "total_cost_usd": 0.3}), "")
        res = R.dry_run(recs, 0.75, 100.0, self.out, run=lambda *a, **k: bad)
        self.assertEqual(res["set/v3.0-r1"]["honest"]["A"]["raw"], '{"answers": {"next')
        good = R.dry_run(recs, 0.75, 100.0, tempfile.mkdtemp(prefix="raterout-"), run=self.run_fn())
        self.assertIsNone(good["set/v3.0-r1"]["honest"]["B"]["raw"])

    def test_a_defect_that_leaves_its_evidence_stops_the_dry_run_before_any_call(self):
        with mock.patch.dict(R.DEFECTS, {"missing": (lambda rd: rd, ["next_step"])}):
            with self.assertRaises(probe.Refused) as c:
                R.dry_run(sample_records(), 0.75, 100.0, self.out, run=self.run_fn())
        self.assertEqual(self.calls, [])                                          # nothing was sent, so nothing was spent
        self.assertFalse(os.path.exists(os.path.join(self.out, "spend.jsonl")))
        self.assertIn("missing", str(c.exception))
        self.assertIn("nothing was sent", str(c.exception))

    def test_each_result_and_the_summary_carry_the_evidence_check_of_the_defect_rated(self):
        recs = {k: v for k, v in sample_records().items() if k == "set/v3.0-r1"}
        res = R.dry_run(recs, 0.75, 100.0, self.out, run=self.run_fn())
        chk = res["set/v3.0-r1"]["missing"]["A"]["check"]
        self.assertEqual((chk["before"] > 0, chk["after"]), (True, 0))
        self.assertEqual(res["set/v3.0-r1"]["missing"]["B"]["check"], chk)
        for kind in ("honest", "wrong", "fabricated"):
            self.assertIsNone(res["set/v3.0-r1"][kind]["A"]["check"], kind)
        ev = R.summarize_dry_run(res)["records"]["set/v3.0-r1"]["planted_evidence"]
        self.assertEqual(sorted(ev), ["missing", "vague"])
        self.assertEqual((ev["vague"]["after"], ev["missing"]["after"]), (0, 0))

    def test_a_failed_call_is_listed_and_costs_what_it_cost(self):
        recs = {k: v for k, v in sample_records().items() if k == "set/v3.0-r1"}
        bad = subprocess.CompletedProcess([], 0, json.dumps({"subtype": "success", "result": "nope", "total_cost_usd": 0.3}), "")
        s = R.summarize_dry_run(R.dry_run(recs, 0.75, 100.0, self.out, run=lambda *a, **k: bad))
        self.assertEqual(s["records"]["set/v3.0-r1"]["honest"], "unrated")
        self.assertEqual(len(s["failed_calls"]), 10)
        self.assertAlmostEqual(s["cost_usd"], 3.0)

    def test_dry_run_from_the_command_line_needs_both_caps(self):
        with self.assertRaises(SystemExit) as c:
            R.main(["dry-run", "--call-cap", "0.5"])
        self.assertEqual(c.exception.code, 2)


class Packet(unittest.TestCase):
    def test_the_sample_is_two_two_two_by_group_fixed_by_the_seed_and_shuffled(self):
        recs = sample_records()
        s = R.draw_sample(recs)
        self.assertEqual(sorted(recs[r][0] for r in s), ["v3.0"] * 2 + ["v3.7"] * 2 + ["v3.8-text"] * 2)
        self.assertEqual(s, R.draw_sample(recs))
        self.assertNotEqual(s, R.draw_sample(recs, seed=1))
        self.assertEqual(len(set(s)), 6)

    def test_the_packet_names_no_run_and_no_arm_and_the_key_is_a_separate_object(self):
        recs = sample_records()
        sample = R.draw_sample(recs)
        md, sheet, key, size = R.build_packet(recs, sample)
        for rid in sample:
            self.assertNotIn(rid, md)
        for word in ("set/", "v3.0-r", "HANDOFFS", "SESSION_NOTES"):
            self.assertNotIn(word, md)
        self.assertEqual(sorted(key), [f"R{i:02d}" for i in range(1, 7)])
        self.assertEqual({v["run"] for v in key.values()}, set(sample))
        self.assertEqual(sheet[0], ["record", *R.KEYS, "arm_guess", "notes"])
        self.assertEqual(len(sheet), 7)
        self.assertEqual(size["records"], 6)
        self.assertGreater(size["words"], 0)
        self.assertEqual(md.count("# Record R"), 6)
        self.assertIn("6 records, each the text", md)
        self.assertIn("**next_step**", md)

    def test_his_sheet_is_scored_against_the_key_by_group_with_the_arm_guess_checked(self):
        key = {"R01": {"run": "a", "group": "v3.0", "arm_label": "3.0"}, "R02": {"run": "b", "group": "v3.7", "arm_label": "3.7"},
               "R03": {"run": "c", "group": "v3.7", "arm_label": "3.7"}}
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        p = os.path.join(d, "sheet.csv")
        with open(p, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["record", *R.KEYS, "arm_guess", "notes"])
            w.writerow(["R01", "y", "n", "y", "", "", "", "", "", "3.0", ""])
            w.writerow(["R02", "yes", "y", "", "", "", "", "", "", "3.8", ""])
            w.writerow(["R03", "n", "y", "", "", "", "", "", "", "", ""])
        s = R.score_human(p, key)
        self.assertEqual(s["yes_share"]["v3.7"]["next_step"], 0.5)
        self.assertEqual(s["yes_share"]["v3.0"]["where"], 0.0)
        self.assertEqual(s["arm_guess"], {"answered": 2, "right": 1, "of": 3, "chance": 0.333})


if __name__ == "__main__":
    unittest.main()
