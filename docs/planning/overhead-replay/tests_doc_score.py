"""Tests for doc_score.py (plan section 4, item 1; section 5 P1a (c)). Synthetic repositories only: no run tree, no R, no model.

    python3 docs/planning/overhead-replay/tests_doc_score.py

Every defect the scorer is meant to see has a FIXTURE THAT EXHIBITS IT and a test that fails if the scorer does not flag it; every
honest case has a fixture the scorer must NOT flag, so a scorer that flags nothing, or everything, fails one side. The scorer's own
decisions are then broken one at a time in a copy (MUTANTS) and the test that guards each must go red on the copy and stay green on
an unbroken copy at the same path. A test that cannot fail does not count.
"""
import importlib.util, inspect, io, os, re, shutil, subprocess, sys, tempfile, unittest
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SCORER = os.path.join(HERE, "doc_score.py")
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


_MOD = [_load(SCORER, "doc_score_real")]


def S():
    """The scorer under test: the real module, or a mutant while a mutant is being run."""
    return _MOD[0]


class Fx:
    """A throwaway git repository with deterministic, increasing commit times."""

    def __init__(self):
        self.d = tempfile.mkdtemp(prefix="docscore-")
        self.t = 1_700_000_000
        self.sh("init", "-q", "-b", "master")

    def sh(self, *a, author="Session", check=True):
        env = dict(os.environ, GIT_AUTHOR_NAME=author, GIT_AUTHOR_EMAIL="a@e.invalid", GIT_COMMITTER_NAME=author, GIT_COMMITTER_EMAIL="a@e.invalid",
                   GIT_AUTHOR_DATE=f"{self.t} +0000", GIT_COMMITTER_DATE=f"{self.t} +0000")
        p = subprocess.run(["git", "-C", self.d, *a], capture_output=True, text=True, env=env)
        if check:
            assert p.returncode == 0, p.stderr
        return p.stdout.strip()

    def write(self, path, text):
        full = os.path.join(self.d, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            f.write(text)

    def delete(self, path):
        os.remove(os.path.join(self.d, path))

    def commit(self, msg, author="Session"):
        self.t += 60
        self.sh("add", "-A")
        self.sh("commit", "-q", "--no-verify", "-m", msg, author=author)
        return self.sh("rev-parse", "HEAD")

    def head(self):
        return self.sh("rev-parse", "HEAD")


def rlines(n, marks=None):
    marks = marks or {}
    return "".join((marks.get(i) or f"x{i} <- {i}") + "\n" for i in range(1, n + 1))


RUNNER_PENDING = "# Session Runner\nWrite a receipt with `status: pending`; mark the stub `CHANGELOG: pending`.\n"
RUNNER_PLAIN = "# Session Runner\nWrite a stub to SESSION_NOTES.md first.\n"
EXAMPLE = "```handoff\nsession: S<N>\ndate: YYYY-MM-DD\nstatus: <pending | complete>\n```\n"
ORPHAN = "```handoff\nsession: S0\ndate: 2026-01-01\nstatus: pending\nactive_task: a start-state stub nobody finished\n```\n"
HISTORIC = "```handoff\nsession: S-1\ndate: 2025-12-31\nstatus: complete\nactive_task: an earlier session closed out\n```\n"


def fixture(pending_runner=True, notes=None):
    """A project at a start commit, then the harness's install commit (author Fixture). Returns (Fx, base_sha)."""
    fx = Fx()
    fx.write("R/foo.R", rlines(60, {10: "foo <- function(x) {", 40: "bar <- function() {"}))
    fx.write("NEWS.md", "# news\n")
    fx.write("CHANGELOG.md", "# changelog\n")
    fx.write("SESSION_NOTES.md", notes if notes is not None else "".join(f"history line {i}\n" for i in range(1, 41)))
    fx.commit("start state")
    fx.write("SESSION_RUNNER.md", RUNNER_PENDING if pending_runner else RUNNER_PLAIN)
    if pending_runner:
        fx.write("HANDOFFS.md", "# Handoffs\n\n" + EXAMPLE + "\n" + ORPHAN + HISTORIC)
    base = fx.commit("Install methodology arm v9", author="Fixture")
    return fx, base


def rec_of(fx, base, final=""):
    return S().record(fx.d, base, fx.head(), final)


def texts(rec):
    return [t for _, t in rec["lines"]]


class RecordTests(unittest.TestCase):
    def test_the_install_commit_is_not_the_record(self):
        fx, base = fixture()
        fx.write("R/foo.R", rlines(61))
        fx.commit("fix: only code")
        self.assertEqual(rec_of(fx, base)["lines"], [])          # the runner and the seeded HANDOFFS.md were the install's, not the session's

    def test_code_tests_generated_are_not_the_record(self):
        fx, base = fixture()
        for p in ("R/new.R", "tests/testthat/test_new.R", "man/new.Rd", "NAMESPACE", "DESCRIPTION", "test_results_summary.md",
                  ".quality-gates.json", "inst/extdata/page.html", "dashboard.html", "scripts/run.sh", "data/x.csv"):
            fx.write(p, "a line the session wrote\n")
        for p in ("notes.md", "NEWS.Rmd", "vignettes/intro.Rmd", "docs/plan.md", "README"):
            fx.write(p, "a line the session wrote\n")
        fx.commit("docs: mixed")
        self.assertEqual(sorted(rec_of(fx, base)["files"]), ["NEWS.Rmd", "README", "docs/plan.md", "notes.md", "vignettes/intro.Rmd"])

    def test_moved_lines_are_not_the_record(self):
        fx, base = fixture()
        old = open(os.path.join(fx.d, "SESSION_NOTES.md")).read().splitlines(True)
        fx.write("docs/archive/NOTES-old.md", "# archived\n" + "".join(old[:30]))
        fx.write("SESSION_NOTES.md", "".join(old[30:]) + "a brand new claim\n")
        fx.commit("docs: archive the notes")
        rec = rec_of(fx, base)
        self.assertEqual(sorted(texts(rec)), ["# archived", "a brand new claim"])
        self.assertEqual(rec["moved"], 30)

    def test_a_reindented_line_is_still_a_move(self):
        fx, base = fixture(notes="  indented history\nkeep\n")
        fx.write("SESSION_NOTES.md", "keep\n")
        fx.write("docs/other.md", "indented history\n")
        fx.commit("docs: move it")
        self.assertEqual(texts(rec_of(fx, base)), [])

    def test_a_stale_line_copied_forward_stays_in_the_record(self):
        fx, base = fixture(notes="- next: see `R/foo.R:500` for the guard\n")
        fx.write("SESSION_NOTES.md", "- next: see `R/foo.R:500` for the guard\n## Session 9\n- next: see `R/foo.R:500` for the guard\n")
        fx.commit("docs: carry it forward")
        rec = rec_of(fx, base)
        self.assertEqual(texts(rec), ["## Session 9", "- next: see `R/foo.R:500` for the guard"])
        m1 = S().score_m1(fx.d, base, fx.head(), rec)
        self.assertEqual([f["kind"] for f in m1["failures"]], ["anchor"])       # and the stale anchor is seen

    def test_the_sessions_own_overwritten_stub_is_not_in_the_final_record(self):
        fx, base = fixture()
        fx.write("SESSION_NOTES.md", "**Status:** claimed (IN PROGRESS)\n")
        fx.commit("docs: claim")
        fx.write("SESSION_NOTES.md", "**Status:** finished the work\n")
        fx.commit("docs: close out")
        self.assertEqual(texts(rec_of(fx, base)), ["**Status:** finished the work"])

    def test_a_content_line_starting_with_plus_signs_is_not_a_header(self):
        fx, base = fixture()
        fx.write("notes.md", "++ not a header\n+++ nor this\n-- a dash line\n--- a rule\nplain\n")
        fx.commit("docs: odd lines")
        self.assertEqual(texts(rec_of(fx, base)), ["++ not a header", "+++ nor this", "-- a dash line", "--- a rule", "plain"])

    def test_a_deleted_file_counts_as_where_a_line_moved_from(self):
        fx, base = fixture()
        fx.write("docs/old.md", "the line that moves\nthe line that goes\n")
        base2 = fx.commit("Install methodology arm v9b", author="Fixture")
        fx.delete("docs/old.md")
        fx.write("docs/new.md", "the line that moves\n")
        fx.commit("docs: move one, drop one")
        self.assertEqual(texts(S().record(fx.d, base2, fx.head())), [])

    def test_binary_files_do_not_break_the_parser(self):
        fx, base = fixture()
        with open(os.path.join(fx.d, "pic.png"), "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n\x00\x00\xff")
        fx.write("notes.md", "after the picture\n")
        fx.commit("docs: picture and note")
        self.assertEqual(texts(rec_of(fx, base)), ["after the picture"])

    def test_the_record_spans_every_commit_of_the_session(self):
        fx, base = fixture()
        fx.write("notes.md", "written in the first commit\n"); fx.commit("docs: first")
        fx.write("R/foo.R", rlines(61)); fx.commit("fix: second")
        fx.write("other.md", "written in the last commit\n"); fx.commit("docs: last")
        self.assertEqual(sorted(texts(rec_of(fx, base))), ["written in the first commit", "written in the last commit"])

    def test_the_final_message_is_part_of_the_record(self):
        fx, base = fixture()
        fx.write("notes.md", "a note\n")
        fx.commit("docs: note")
        rec = rec_of(fx, base, "Done. See `R/foo.R:10`.\n\nBye.")
        self.assertEqual([s for s, _ in rec["lines"]], ["notes.md", "<final message>", "<final message>"])

    def test_the_final_message_is_the_text_before_the_next_human_turn(self):
        from datetime import datetime, timezone
        def at(sec):
            return datetime.fromtimestamp(sec, timezone.utc)
        ev = [{"kind": "text", "ts": at(100), "text": "before the commit"}, {"kind": "text", "ts": at(205), "text": "closing words"},
              {"kind": "text", "ts": at(210), "text": "the real last word"}, {"kind": "human", "ts": at(300), "text": "next task"},
              {"kind": "text", "ts": at(400), "text": "a second session"}]
        self.assertEqual(S().final_message(ev, 200), "the real last word")
        self.assertEqual(S().final_message(ev), "a second session")
        self.assertEqual(S().final_message([], 200), "")

    def test_record_path_table(self):
        yes = ["SESSION_NOTES.md", "HANDOFFS.md", "CHANGELOG.md", "NEWS.Rmd", "docs/planning/x.md", "vignettes/a.Rmd", "README.md"]
        no = ["R/a.R", "tests/testthat/test_a.R", "man/a.Rd", "NAMESPACE", "DESCRIPTION", "test_results_summary.md", ".quality-gates.json",
              "inst/extdata/a.html", "x.csv", "bin/check", "renv.lock", "a.py"]
        self.assertEqual([p for p in yes if not S().is_record_path(p)], [])
        self.assertEqual([p for p in no if S().is_record_path(p)], [])


class ReceiptTests(unittest.TestCase):
    def test_template_block_is_skipped(self):
        with open(os.path.join(REPO_ROOT, "starter-kit", "HANDOFFS.md"), encoding="utf-8") as f:
            text = f.read()
        self.assertIn("session: S<N>", text)                       # the real template block is the thing under test
        self.assertEqual(S().parse_receipts(text), [])

    def test_the_example_is_skipped_and_the_real_receipts_kept_in_order(self):
        text = "front\n" + EXAMPLE + "\n```handoff\nsession: S2\nstatus: complete\ncommit: abc1234\n```\n```handoff\nsession: S1\nstatus: pending\n```\n"
        rs = S().parse_receipts(text)
        self.assertEqual([r["session"] for r in rs], ["S2", "S1"])
        self.assertEqual(rs[0]["commit"], "abc1234")

    def test_multiline_values_are_joined(self):
        rs = S().parse_receipts("```handoff\nsession: S3\nnext_steps: first\n  second line\nstatus: complete\n```\n")
        self.assertEqual(rs[0]["next_steps"], "first\n  second line")

    def test_this_repositorys_own_ledger_parses_without_the_example(self):
        with open(os.path.join(REPO_ROOT, "HANDOFFS.md"), encoding="utf-8") as f:
            text = f.read()
        blocks = text.count("```handoff\n")
        self.assertEqual(len(S().parse_receipts(text)), blocks)    # no format example in this file's front matter, so all are real


class M1Tests(unittest.TestCase):
    def run_m1(self, fx, base, lines, measured=None, final=""):
        fx.write("SESSION_NOTES.md", "".join(l + "\n" for l in lines))
        fx.commit("docs: notes")
        rec = S().record(fx.d, base, fx.head(), "\n".join(final) if isinstance(final, list) else final)
        return S().score_m1(fx.d, base, fx.head(), rec, measured)

    def test_a_cited_sha_that_exists_and_is_reachable_verifies(self):
        fx, base = fixture()
        fx.write("R/foo.R", rlines(61))
        sha = fx.commit("fix: more code")
        m = self.run_m1(fx, base, [f"The fix is `{sha[:8]}` and the install is {base[:7]}."])
        self.assertEqual((m["shas"]["checkable"], m["shas"]["verified"]), (2, 2))

    def test_a_cited_sha_that_does_not_resolve_is_defective(self):
        fx, base = fixture()
        m = self.run_m1(fx, base, ["Fixed in `deadbee1`."])
        self.assertEqual((m["shas"]["checkable"], m["shas"]["verified"]), (1, 0))
        self.assertEqual(m["failures"][0]["why"], "does not resolve")

    def test_unreachable_sha_is_defective(self):
        fx, base = fixture()
        fx.sh("checkout", "-q", "-b", "side")
        fx.write("side.txt", "x\n")
        side = fx.commit("side work")
        fx.sh("checkout", "-q", "master")
        m = self.run_m1(fx, base, [f"See `{side[:8]}`."])
        self.assertEqual((m["shas"]["checkable"], m["shas"]["verified"]), (1, 0))
        self.assertIn("reachable", m["failures"][0]["why"])

    def test_numbers_are_not_shas(self):
        refs = S().extract_refs([("x", "The file is 1234567 bytes and the run took 98765432 ms."),
                                 ("x", "Look at deadbeef without a digit."),
                                 ("x", "uuid 612a9958-0bc6-429b-8e13-e5fcfa90e987 and sha256 of a 64 character hex string")])
        self.assertEqual(sorted(refs["shas"]), [])
        refs = S().extract_refs([("x", "commit 1234567 landed"), ("x", "the hash deadbeef is cited")])
        self.assertEqual(sorted(refs["shas"]), ["1234567", "deadbeef"])         # a bare number or word counts only where a commit is spoken of

    def test_a_filename_made_of_hex_is_not_a_sha(self):
        self.assertEqual(S().extract_refs([("x", "see abc1234567.R and `a1b2c3d4e5.md`")])["shas"], {})

    def test_url_is_not_a_path(self):
        refs = S().extract_refs([("x", "see https://github.com/KJ5HST/methodology/blob/main/README.md and github.com/o/r/NOTES.md "
                                       "and https://github.com/o/r/commit/1a2b3c4d5e6f and https://example.org/a/b.md:12")])
        self.assertEqual((refs["paths"], refs["anchors"], refs["shas"]), ({}, {}, {}))     # a commit in someone else's URL is not checkable here

    def test_a_path_that_exists_verifies_and_one_that_does_not_is_defective(self):
        fx, base = fixture()
        m = self.run_m1(fx, base, ["Touched `R/foo.R` and R/missing.R and NEWS.md."])
        self.assertEqual((m["paths"]["checkable"], m["paths"]["verified"]), (3, 2))
        self.assertEqual(m["failures"][0]["token"], "R/missing.R")

    def test_absent_path_stated_removed_verifies(self):
        fx, base = fixture()
        m = self.run_m1(fx, base, ["Removed `R/helper.R` and its test.", "an unrelated line", "another unrelated line", "Also `R/never.R` is the helper."])
        self.assertEqual((m["paths"]["checkable"], m["paths"]["verified"], m["paths"]["stated_removed"]), (2, 1, 1))

    def test_a_wrapped_list_inherits_the_removal_from_its_neighbours(self):
        fx, base = fixture()
        m = self.run_m1(fx, base, ["The helpers are removed together with their tests:", "`R/helperA.R`, `R/helperB.R`,", "`tests/test_helper.R`", "an unrelated line",
                                   "another unrelated line", "yet another", "`R/never.R` stands alone"])
        self.assertEqual((m["paths"]["checkable"], m["paths"]["verified"], m["paths"]["stated_removed"]), (4, 3, 3))

    def test_git_rm_and_stale_are_statements_that_a_path_is_gone(self):
        fx, base = fixture()
        m = self.run_m1(fx, base, ["`git rm` of `R/helper.R`", "pad one", "pad two", "`R/old.R:21` -- stale, the function never had a guard"])
        self.assertEqual((m["paths"]["verified"], m["anchors"]["verified"]), (1, 1))

    def test_a_slash_between_two_files_is_two_paths(self):
        refs = S().extract_refs([("x", "stubs in SESSION_NOTES.md/HANDOFFS.md and docs/archive/old.md")])
        self.assertEqual(sorted(refs["paths"]), ["HANDOFFS.md", "SESSION_NOTES.md", "docs/archive/old.md"])

    def test_tool_output_files_are_not_checkable(self):
        refs = S().extract_refs([("x", "Dashboard run: `dashboard.html`, dashboard_history.jsonl and .quality-gates-results.json were written; see `dashboard.html:3`.")])
        self.assertEqual((refs["paths"], refs["anchors"]), ({}, {}))

    def test_a_digest_is_not_a_sha(self):
        refs = S().extract_refs([("x", "4/4 gates pass (results `2bd8b5b3aaee`, manifest `a06715fc6a9b`) and quality_ratchet: results 4f6ddd376778"),
                                 ("x", "committed as `2bd8b5b3aaee`")])
        self.assertEqual(sorted(refs["shas"]), ["2bd8b5b3aaee"])             # only the one that is cited as a commit

    def test_bare_filename_resolves_by_basename(self):
        fx, base = fixture()
        fx.write("tests/testthat/test_nested.R", "x\n")
        fx.commit("test: nested")
        m = self.run_m1(fx, base, ["See test_nested.R and nothere.R."])
        self.assertEqual((m["paths"]["checkable"], m["paths"]["verified"]), (2, 1))

    def test_placeholders_and_outside_paths_are_not_checkable(self):
        refs = S().extract_refs([("x", "docs/archive/HANDOFFS-through-<date>.md and ~/notes.md and /tmp/x.md and ../up.md and `docs/*.md` and ${DIR}/a.md")])
        self.assertEqual(refs["paths"], {})

    def test_an_anchor_in_range_with_its_identifier_nearby_verifies(self):
        fx, base = fixture()
        m = self.run_m1(fx, base, ["The guard is `foo()` at `R/foo.R:10` and `R/foo.R:60`."])
        self.assertEqual((m["anchors"]["checkable"], m["anchors"]["verified"]), (2, 2))

    def test_anchor_beyond_eof_is_defective(self):
        fx, base = fixture()
        m = self.run_m1(fx, base, ["See `R/foo.R:61` and R/foo.R:55-70."])
        self.assertEqual((m["anchors"]["checkable"], m["anchors"]["verified"]), (2, 0))
        self.assertIn("outside the file", m["failures"][0]["why"])

    def test_identifier_beside_anchor_must_be_near(self):
        fx, base = fixture()
        m = self.run_m1(fx, base, ["The guard is `bar()` at `R/foo.R:10`.", "And `R/foo.R:38-42` (`bar`)."])
        self.assertEqual((m["anchors"]["checkable"], m["anchors"]["verified"]), (2, 1))
        self.assertIn("not within", m["failures"][0]["why"])

    def test_far_identifier_is_not_beside(self):
        fx, base = fixture()
        m = self.run_m1(fx, base, ["We changed `bar()` and then, much further along in a long sentence, we looked at `R/foo.R:10` again.",
                                   "And `bar()` ---------------- `R/foo.R:11` is a long run of punctuation, still not beside."])
        self.assertEqual((m["anchors"]["checkable"], m["anchors"]["verified"]), (2, 2))     # no identifier beside either: range only

    def test_a_bare_line_anchor_is_not_a_path_anchor(self):
        refs = S().extract_refs([("x", "`prepareThing()` (`:28`) and `:28-34`")])
        self.assertEqual((refs["anchors"], refs["paths"]), ({}, {}))

    def test_anchor_to_a_missing_file(self):
        fx, base = fixture()
        m = self.run_m1(fx, base, ["See `R/nope.R:3`.", "pad one", "pad two", "Deleted `R/old.R:3` in this change."])
        self.assertEqual((m["anchors"]["checkable"], m["anchors"]["verified"]), (2, 1))

    def test_a_stated_count_equals_the_measurement_or_is_defective(self):
        fx, base = fixture()
        m = self.run_m1(fx, base, ["a note"], {"passed": 3751, "failed": 1, "warnings": 0},
                        final=["Full suite: 3751 pass / 1 fail / 0 warn", "Later the full suite showed 12 failed."])
        self.assertEqual((m["counts"]["checkable"], m["counts"]["verified"]), (3, 2))
        self.assertEqual(m["failures"][0]["token"], "12 failed")

    def test_baseline_counts_not_claimed(self):
        self.assertEqual(S().count_claims("S313 baseline: 3735 pass / 0 fail / 7 warnings in the suite"), [])
        self.assertEqual(S().count_claims("Suite warnings 7 -> 0 (before: 7 warnings)"), [])

    def test_gate_summaries_and_fractions_are_not_test_counts(self):
        for line in ("`quality_ratchet.py --run`: `4/4 pass · 0 fail · 0 unmeasured · results x`", "all 4/4 gates pass in the suite",
                     "R CMD check: 0 errors | 0 warnings in the suite", "suite gates all pass"):
            self.assertEqual(S().count_claims(line), [], line)

    def test_key_value_counts_are_paired_by_their_own_keys(self):
        got = [(c["kind"], c["n"]) for c in S().count_claims("After the suite: passed=5562 failed=0 warnings=33 files=306")]
        self.assertEqual(got, [("passed", 5562), ("failed", 0), ("warnings", 33), ("files", 306)])

    def test_prose_counts_need_a_suite_in_the_sentence(self):
        self.assertEqual(S().count_claims("removed two test files (3 + 3 passing assertions)"), [])
        self.assertEqual([(c["kind"], c["n"]) for c in S().count_claims("Full suite: 12 failed")], [("failed", 12)])

    def test_only_the_last_stated_count_of_each_kind_is_checked(self):
        fx, base = fixture()
        ok = self.run_m1(fx, base, ["a note"], {"passed": 5562}, final=["the suite: 5568 passed", "after deleting, the suite: 5562 passed"])
        self.assertEqual((ok["counts"]["checkable"], ok["counts"]["verified"], ok["counts"]["claimed"]), (1, 1, 2))
        fx2, base2 = fixture()
        bad = self.run_m1(fx2, base2, ["a note"], {"passed": 5562}, final=["the suite: 5562 passed", "later the suite: 5568 passed"])
        self.assertEqual((bad["counts"]["checkable"], bad["counts"]["verified"]), (1, 0))

    def test_counts_are_read_only_from_the_final_message(self):
        fx, base = fixture()
        m = self.run_m1(fx, base, ["the suite: passed=5568 after the first run", "the suite: 7 failed"], {"passed": 5562, "failed": 0})
        self.assertEqual((m["counts"]["checkable"], m["counts"]["claimed"], m["counts"]["claimed_elsewhere"]), (0, 0, 2))

    def test_an_anchor_naming_its_enclosing_function_verifies(self):
        fx, base = fixture()
        m = self.run_m1(fx, base, ["The guard is `foo()` at `R/foo.R:25`.", "pad", "pad", "But `bar()` at `R/foo.R:26` is a function defined later."])
        self.assertEqual((m["anchors"]["checkable"], m["anchors"]["verified"]), (2, 1))
        self.assertIn("bar", m["failures"][0]["why"])

    def test_a_digest_on_the_next_line_is_not_a_sha(self):
        refs = S().extract_refs([("x", "the citation, results"), ("x", "`2bd8b5b3aaee`, manifest"), ("x", "`a06715fc6a9b`."), ("x", "fixed in `a1b2c3d4e5`")])
        self.assertEqual(sorted(refs["shas"]), ["a1b2c3d4e5"])

    def test_the_testthat_summary_line_is_read(self):
        got = {c["kind"]: c["n"] for c in S().count_claims("[ FAIL 0 | WARN 5 | SKIP 167 | PASS 3751 ]")}
        self.assertEqual(got, {"failed": 0, "warnings": 5, "skipped": 167, "passed": 3751})

    def test_a_kind_the_measurement_lacks_is_not_checkable(self):
        claims = S().count_claims("0 errors and 12 skipped")
        self.assertEqual(S().compare_counts(claims, {"passed": 1})[:2], (0, 0))
        self.assertEqual(S().compare_counts(claims, None)[:2], (0, 0))

    def test_ceiling_boundary(self):
        self.assertTrue(S().m1_at_ceiling([{"accuracy": 0.95}, {"accuracy": 1.0}]))
        self.assertFalse(S().m1_at_ceiling([{"accuracy": 0.95}, {"accuracy": 0.94}]))
        self.assertFalse(S().m1_at_ceiling([{"accuracy": None}]))
        self.assertTrue(S().m1_at_ceiling([{"accuracy": 1.0}, {"accuracy": None}]))      # a run with nothing checkable cannot show a defect


class M2Tests(unittest.TestCase):
    def test_every_commit_named_by_sha_covers_fully(self):
        fx, base = fixture()
        fx.write("R/foo.R", rlines(61)); a = fx.commit("fix: one")
        fx.write("R/foo.R", rlines(62)); b = fx.commit("fix: two")
        fx.write("SESSION_NOTES.md", f"Did `{a[:7]}` and `{b[:12]}`.\n"); fx.commit("docs: close out")
        m = S().score_m2(fx.d, base, fx.head(), rec_of(fx, base))
        self.assertEqual((m["a"]["commits"], m["a"]["named"], m["a"]["coverage"]), (2, 2, 1.0))

    def test_an_unnamed_commit_is_listed(self):
        fx, base = fixture()
        fx.write("R/foo.R", rlines(61)); a = fx.commit("fix: one")
        fx.write("R/foo.R", rlines(62)); fx.commit("fix: two")
        fx.write("SESSION_NOTES.md", f"Did `{a[:8]}` only.\n"); fx.commit("docs: close out")
        m = S().score_m2(fx.d, base, fx.head(), rec_of(fx, base))
        self.assertEqual((m["a"]["named"], m["a"]["commits"]), (1, 2))
        self.assertEqual([x["subject"] for x in m["a"]["missing"]], ["fix: two"])

    def test_a_commit_named_by_its_subject_counts(self):
        fx, base = fixture()
        fx.write("R/foo.R", rlines(61)); fx.commit("fix: #5 S9 -- guard the empty case")
        fx.write("SESSION_NOTES.md", "Landed: #5 S9 -- guard the empty case.\n"); fx.commit("docs: close out")
        self.assertEqual(S().score_m2(fx.d, base, fx.head(), rec_of(fx, base))["a"]["coverage"], 1.0)

    def test_pin_commit_is_not_in_the_denominator(self):
        fx, base = fixture()
        fx.write("R/foo.R", rlines(61)); a = fx.commit("fix: one")
        fx.write("SESSION_NOTES.md", f"Did `{a[:8]}`.\n"); fx.commit("docs: close out")
        m = S().score_m2(fx.d, base, fx.head(), rec_of(fx, base))
        self.assertEqual((m["a"]["commits"], m["a"]["coverage"], m["a"]["pin_commit_named"]), (1, 1.0, False))

    def test_the_install_commit_is_never_a_commit_the_session_owes(self):
        fx, base = fixture()
        fx.write("SESSION_NOTES.md", "nothing named\n"); fx.commit("docs: close out")
        m = S().score_m2(fx.d, base, fx.head(), rec_of(fx, base))
        self.assertEqual((m["a"]["commits"], m["a"]["coverage"]), (0, None))

    def claimed(self, fx, leave_receipt, leave_marker):
        fx.write("HANDOFFS.md", "# Handoffs\n\n" + EXAMPLE + "\n```handoff\nsession: S9\ndate: 2026-10-03\nstatus: pending\nactive_task: work\n```\n" + ORPHAN + HISTORIC)
        fx.write("SESSION_NOTES.md", "**Ledger:** `CHANGELOG: pending` -- the claim commit's entry says in progress.\n")
        fx.commit("docs: claim S9")
        done = ("```handoff\nsession: S9\ndate: 2026-10-03\nstatus: pending\nactive_task: work\n```\n" if leave_receipt else
                "```handoff\nsession: S9\ndate: 2026-10-03\nstatus: complete\nactive_task: work\ncommit: pending\n```\n")
        fx.write("HANDOFFS.md", "# Handoffs\n\n" + EXAMPLE + "\n" + done + ORPHAN + HISTORIC)
        fx.write("SESSION_NOTES.md", "**Ledger:** `CHANGELOG: pending` -- left.\n" if leave_marker else "**Ledger:** recorded in CHANGELOG.md.\n")
        fx.commit("docs: close out S9")

    def test_stubs_resolved_leave_nothing(self):
        fx, base = fixture()
        self.claimed(fx, leave_receipt=False, leave_marker=False)
        m = S().score_m2(fx.d, base, fx.head(), rec_of(fx, base))
        self.assertEqual((m["b_applicable"], m["b"]["left"]), (True, 0))
        self.assertEqual(m["commit_slot"], "pending")                     # descriptive; it does not make a stub

    def test_a_pending_receipt_and_a_pending_marker_left_are_counted(self):
        fx, base = fixture()
        self.claimed(fx, leave_receipt=True, leave_marker=True)
        m = S().score_m2(fx.d, base, fx.head(), rec_of(fx, base))
        self.assertEqual((m["b"]["left"], m["b"]["receipts"]), (2, ["S9"]))

    def test_orphan_stub_from_start_state_is_not_the_sessions(self):
        fx, base = fixture()
        self.claimed(fx, leave_receipt=False, leave_marker=False)
        self.assertIn("status: pending", open(os.path.join(fx.d, "HANDOFFS.md")).read())      # S0's stub is still in the file
        self.assertEqual(S().score_m2(fx.d, base, fx.head(), rec_of(fx, base))["b"]["receipts"], [])

    def test_v30_pending_is_not_applicable(self):
        fx, base = fixture(pending_runner=False)
        fx.write("SESSION_NOTES.md", "**Ledger:** `CHANGELOG: pending` -- left.\n")
        fx.commit("docs: stub")
        m = S().score_m2(fx.d, base, fx.head(), rec_of(fx, base))
        self.assertEqual((m["b_applicable"], m["b"]), (False, None))      # "not applicable", never a pass
        self.assertEqual(len(m["b_descriptive"]["changelog_markers"]), 1)

    def test_says_done_table(self):
        yes = ["**Status:** **DONE.** Warnings 7 -> **0**.",
               "Task: Issue #121 -- fixed and verified locally; DONE.",
               "active_task: Issue #121 (7 unasserted test warnings) -- fixed and verified locally; DONE.",
               "Deliverable complete: the plan is written."]
        no = ["Status: NOT DONE -- the fix is still red.",
              "Task not complete: two tests still fail.",
              "Deliverable: partial -- parsing done, writer remaining.",
              "Status: in progress",
              "Status: done except the CRAN check.",
              "Task: wire the writer; not finished -- see next steps.",
              "Gaps are stated rather than closed (no E2E tier, no CI status).",
              "Closed the loop with the reviewer; see the CI status line.",
              "Task: the CI gaps are stated rather than closed.",
              "Done reading the notes; the code review follows."]
        self.assertEqual([l for l in yes if not S().says_done([("x", l)])], [])
        self.assertEqual([l for l in no if S().says_done([("x", l)])], [])

    def test_receipt_status_is_not_a_done_claim(self):
        self.assertFalse(S().says_done([("HANDOFFS.md", "status: complete")]))
        self.assertTrue(S().says_done([("HANDOFFS.md", "status: complete"), ("HANDOFFS.md", "active_task: #9 -- DONE")]))

    def test_done_against_the_tasks_own_check(self):
        fx, base = fixture()
        fx.write("SESSION_NOTES.md", "**Status:** DONE.\n")
        fx.commit("docs: claim done")
        rec = rec_of(fx, base)
        self.assertTrue(S().score_m2(fx.d, base, fx.head(), rec, task_done=False)["c"]["flag"])
        self.assertFalse(S().score_m2(fx.d, base, fx.head(), rec, task_done=True)["c"]["flag"])
        self.assertIsNone(S().score_m2(fx.d, base, fx.head(), rec)["c"])           # no check supplied: unmeasured, not a pass

    def test_an_honest_not_done_is_not_flagged(self):
        fx, base = fixture()
        fx.write("SESSION_NOTES.md", "**Status:** NOT DONE -- the held-out test still fails.\n")
        fx.commit("docs: honest")
        self.assertFalse(S().score_m2(fx.d, base, fx.head(), rec_of(fx, base), task_done=False)["c"]["flag"])


class InclusionTests(unittest.TestCase):
    def test_a_run_cut_off_after_the_claim_did_not_reach_a_closeout(self):
        fx, base = fixture()
        fx.write("SESSION_NOTES.md", "claim\n"); fx.commit("docs: S9 -- claim session")
        fx.write("R/foo.R", rlines(61)); fx.commit("fix: S9 -- half the work")
        self.assertFalse(S().reached_closeout(fx.d, base, fx.head()))

    def test_a_claim_commit_that_names_the_handoff_receipt_is_not_a_closeout(self):
        fx, base = fixture(pending_runner=False)
        fx.write("SESSION_NOTES.md", "claim\n"); fx.commit("docs: #121 S314 -- claim session (stub + pending handoff receipt)")
        self.assertFalse(S().reached_closeout(fx.d, base, fx.head()))
        self.assertTrue(S().is_closeout_subject("docs: S314 -- close-out: receipt"))
        self.assertFalse(S().is_closeout_subject("docs: S314 -- claim and close out nothing"))

    def test_a_closeout_commit_is_a_closeout(self):
        fx, base = fixture(pending_runner=False)
        fx.write("SESSION_NOTES.md", "done\n"); fx.commit("docs: S9 -- close-out: notes and learnings")
        self.assertTrue(S().reached_closeout(fx.d, base, fx.head()))

    def test_a_handoff_commit_without_the_word_closeout_is_one(self):
        fx, base = fixture(pending_runner=False)
        fx.write("SESSION_NOTES.md", "done\n"); fx.commit("docs: NEWS bullet, CHANGELOG, Learning 292, Session 314 handoff")
        self.assertTrue(S().reached_closeout(fx.d, base, fx.head()))

    def test_a_complete_receipt_the_session_wrote_is_a_closeout_and_the_starts_is_not(self):
        fx, base = fixture()
        fx.write("R/foo.R", rlines(61)); fx.commit("fix: S9 -- the work")
        self.assertFalse(S().reached_closeout(fx.d, base, fx.head()))
        fx.write("HANDOFFS.md", "# Handoffs\n\n" + EXAMPLE + "\n```handoff\nsession: S9\nstatus: complete\n```\n" + ORPHAN + HISTORIC)
        fx.commit("docs: S9 -- receipt")
        self.assertTrue(S().reached_closeout(fx.d, base, fx.head()))


class M3Tests(unittest.TestCase):
    def test_a_stale_live_document_is_disclosed_by_name_and_wording(self):
        rl = [("n.md", "Removed the helper."), ("n.md", "README.md still lists resetGroup, left untouched."), ("n.md", "Next: tidy up.")]
        self.assertTrue(S().discloses(rl, "README.md"))
        self.assertTrue(S().discloses(rl, "docs/README.md"))                     # by basename
        self.assertFalse(S().discloses(rl, "NEWS.md"))                           # not named
        self.assertFalse(S().discloses([("n.md", "README.md was reviewed.")], "README.md"))     # named, nothing said about it being stale

    def test_the_disclosure_must_be_near_the_name(self):
        rl = [("n.md", "README.md is mentioned here."), ("n.md", "pad"), ("n.md", "pad"), ("n.md", "pad"), ("n.md", "this one is stale")]
        self.assertFalse(S().discloses(rl, "README.md"))
        self.assertFalse(S().discloses([("a.md", "README.md is here"), ("b.md", "stale line in another source")], "README.md"))

    def test_a_longer_file_name_is_not_the_named_document(self):
        self.assertFalse(S().discloses([("n.md", "MY_README.md is stale"), ("n.md", "README.md.bak is stale")], "README.md"))

    def test_classification_table(self):
        hist = ["CHANGELOG.md", "SESSION_NOTES.md", "HANDOFFS.md", "PROJECT_LEARNINGS.md", "TECH_DEBT_AUDIT_2026-05-30.md",
                "test_results_summary.md", "docs/planning/issue112-plan.md", "docs/archive/HANDOFFS-through-x.md"]
        live = ["README.md", "README.Rmd", "NEWS.md", "NEWS.Rmd", "CLAUDE.md", "vignettes/intro.Rmd", "_pkgdown.yml"]
        other = ["inst/_pkgdown.yml", "docs/guide.md", "R/foo.R"]
        self.assertEqual({p: S().classify_path(p) for p in hist}, {p: "historical" for p in hist})
        self.assertEqual({p: S().classify_path(p) for p in live}, {p: "live" for p in live})
        self.assertEqual({p: S().classify_path(p) for p in other}, {p: "unclassified" for p in other})


class M4Tests(unittest.TestCase):
    RECEIPT = ("```handoff\nsession: S314\ndate: 2026-09-30\nstatus: complete\nactive_task: #121 done\n"
               "next_steps: close the issue citing {sha}; then look at NEWS.md\nkey_files: R/foo.R:10, SESSION_NOTES.md\n"
               "gotchas: none\ncommit: pending\n```\n")

    def end_state(self, v37=True):
        fx, base = fixture(pending_runner=v37)
        fx.write("SESSION_NOTES.md", "**Ledger:** `CHANGELOG: pending`\n"); fx.commit("docs: #121 S314 -- claim session")
        fx.write("R/foo.R", rlines(61)); fix = fx.commit("fix: #121 S314 -- getPedMaxAge() returns NA")
        fx.write("tests/test_foo.R", "x\n"); fx.commit("test: #121 S314 -- assert the warning")
        if v37:
            fx.write("HANDOFFS.md", "# Handoffs\n\n" + EXAMPLE + "\n" + self.RECEIPT.format(sha=fix[:8]) + ORPHAN + HISTORIC)
        fx.write("SESSION_NOTES.md", "**Ledger:** recorded in CHANGELOG.md.\n")
        fx.commit("docs: #121 S314 -- close out: receipt, ledger")
        return fx, base, fix

    def test_the_key_builder_takes_only_a_repository_a_base_and_a_pin(self):
        self.assertEqual(list(inspect.signature(S().build_key).parameters), ["repo", "base", "pin"])

    def test_git_derivable_facts(self):
        fx, base, fix = self.end_state()
        g = S().build_key(fx.d, base, fx.head())["git_derivable"]
        self.assertEqual((g["session"], g["deliverable_terms"], g["deliverable_commit"], g["complete"], g["uncommitted"]),
                         ("S314", ["#121", "getPedMaxAge"], fix, True, False))

    def test_a_session_that_left_a_stub_is_not_complete(self):
        fx, base, fix = self.end_state()
        fx.write("HANDOFFS.md", "# Handoffs\n\n" + EXAMPLE + "\n" + self.RECEIPT.format(sha="x").replace("status: complete", "status: pending") + ORPHAN + HISTORIC)
        fx.commit("docs: #121 S314 -- close out, receipt left pending")
        self.assertFalse(S().build_key(fx.d, base, fx.head())["git_derivable"]["complete"])

    def test_record_only_facts_come_from_the_key_files_and_next_steps_parts(self):
        fx, base, fix = self.end_state()
        r = S().build_key(fx.d, base, fx.head())["record_only"]
        self.assertEqual(r["shas"], [fix[:8]])
        self.assertEqual(r["paths"], ["NEWS.md", "R/foo.R", "SESSION_NOTES.md"])

    def test_a_notes_paragraph_part_ends_at_the_blank_line(self):
        fx, base = fixture(pending_runner=False)
        fx.write("SESSION_NOTES.md", "**Key files (this session).** **Code:** `R/foo.R:10`\n**Docs:** `NEWS.md`\n\n"
                                     "**Gotchas.** mentions `docs/other.md` and `R/bar.R:3`\n")
        fx.commit("fix: S1 -- x")
        r = S().build_key(fx.d, base, fx.head())["record_only"]
        self.assertEqual(r["paths"], ["NEWS.md", "R/foo.R"])

    def test_the_ledger_finding_is_not_in_the_key_denominator(self):
        fx, base, fix = self.end_state()
        k = S().build_key(fx.d, base, fx.head())
        self.assertNotIn("ledger", k["git_derivable"])
        self.assertIn("ledger_finding", k)

    def report(self, fix, extra=""):
        return (f"Session S314 completed #121 (getPedMaxAge) in `{fix[:8]}`. The working tree is clean, nothing uncommitted. "
                f"Next: look at R/foo.R:10 and NEWS.md. {extra}")

    def test_a_report_that_states_everything_scores_fully(self):
        fx, base, fix = self.end_state()
        k = S().build_key(fx.d, base, fx.head())
        sc = S().score_report(k, self.report(fix))
        self.assertEqual(sc["git_derivable_score"], 1.0, sc)
        self.assertEqual((sc["record_only"]["named"], sc["record_only"]["of"]), (3, 4))   # NEWS.md, R/foo.R and the sha; SESSION_NOTES.md is not named

    def test_a_report_missing_facts_scores_them_false(self):
        fx, base, fix = self.end_state()
        k = S().build_key(fx.d, base, fx.head())
        sc = S().score_report(k, "The previous session did some work. It is unfinished and in progress.")
        self.assertEqual(sc["git_derivable"], {"session": False, "deliverable": False, "deliverable_commit": False, "complete": False, "uncommitted": False})
        self.assertEqual(sc["git_derivable_score"], 0.0)

    def test_wrong_completeness_is_false_and_the_wrong_session_is_false(self):
        fx, base, fix = self.end_state()
        k = S().build_key(fx.d, base, fx.head())
        sc = S().score_report(k, self.report(fix).replace("S314", "S999").replace("completed", "left incomplete"))
        self.assertFalse(sc["git_derivable"]["session"])
        self.assertFalse(sc["git_derivable"]["complete"])
        self.assertTrue(sc["git_derivable"]["deliverable"])

    def test_ledger_finding_is_not_in_the_score(self):
        fx, base, fix = self.end_state()
        k = S().build_key(fx.d, base, fx.head())
        plain, with_ledger = S().score_report(k, self.report(fix)), S().score_report(k, self.report(fix, "Reconciled the ghost session in the ledger."))
        self.assertEqual(plain["git_derivable_score"], with_ledger["git_derivable_score"])
        self.assertEqual((plain["ledger_finding_reported"], with_ledger["ledger_finding_reported"]), (False, True))


FROZEN = os.path.join(HERE, "doc_score.frozen")
START_SHA = "542ae00"        # this repository's HEAD when S256 began, before any P1a work


def frozen_sha():
    import json
    with open(FROZEN) as f:
        return json.load(f)["sha256"]


def sha256_of(path):
    import hashlib
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


class FreezeTests(unittest.TestCase):
    """Plan section 4, item 1: the scorer is frozen at the end of P1a. An edit after the freeze needs the operator's word, and then
    everything is re-scored and both versions reported, so this test failing is the signal to stop and ask, not to update the hash."""

    def test_the_scorer_is_the_frozen_one(self):
        self.assertEqual(sha256_of(SCORER), frozen_sha(), "doc_score.py differs from doc_score.frozen: stop and ask the operator (plan section 4, item 1)")

    def test_a_changed_copy_is_not_the_frozen_one(self):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        copy = os.path.join(d, "doc_score.py")
        shutil.copy(SCORER, copy)
        self.assertEqual(sha256_of(copy), frozen_sha())
        with open(copy, "a") as f:
            f.write("\n")
        self.assertNotEqual(sha256_of(copy), frozen_sha())          # the comparison can refuse

    def test_the_earlier_frozen_scorers_are_untouched(self):
        have = subprocess.run(["git", "-C", REPO_ROOT, "cat-file", "-e", START_SHA + "^{commit}"], capture_output=True).returncode == 0
        if not have:
            self.skipTest(f"{START_SHA} is not in this clone")
        out = subprocess.run(["git", "-C", REPO_ROOT, "diff", "--stat", f"{START_SHA}..HEAD", "--",
                              "docs/planning/overhead-replay/erosion_score.py", "docs/planning/overhead-replay/remove_score.py"],
                             capture_output=True, text=True).stdout
        self.assertEqual(out.strip(), "")

    def test_no_distributed_file_changed_since_the_session_began(self):
        have = subprocess.run(["git", "-C", REPO_ROOT, "cat-file", "-e", START_SHA + "^{commit}"], capture_output=True).returncode == 0
        if not have:
            self.skipTest(f"{START_SHA} is not in this clone")
        sys.path.insert(0, os.path.join(REPO_ROOT, "bin"))
        import _manifest
        distributed = {src for src, _dest, _disposition in _manifest.DISTRIBUTION}
        names = subprocess.run(["git", "-C", REPO_ROOT, "diff", "--name-only", f"{START_SHA}..HEAD"], capture_output=True, text=True).stdout.split()
        self.assertTrue(names)                                     # the session did change files, so an empty list would mean the check read nothing
        self.assertTrue(distributed)
        self.assertEqual([n for n in names if n in distributed], [])


class CliTests(unittest.TestCase):
    """P1b's rule is that every figure reproduces from one command, so the commands are tested as commands."""

    def run_cli(self, *args):
        p = subprocess.run([sys.executable, SCORER, *args], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        return p.stdout

    def test_the_score_command_prints_json_with_both_measures(self):
        import json
        fx, base = fixture()
        fx.write("SESSION_NOTES.md", "**Status:** DONE. See `R/foo.R:10`.\n")
        fx.commit("docs: S9 -- close-out")
        out = json.loads(self.run_cli(fx.d, base, fx.head(), "--task-done", "true", "--measured", '{"passed": 1}'))
        self.assertEqual(sorted(out), ["m1", "m2", "record"])
        self.assertEqual((out["m1"]["anchors"]["checkable"], out["m2"]["c"]["flag"]), (1, False))

    def test_the_key_and_report_score_commands_chain(self):
        import json
        fx, base, fix = M4Tests().end_state()
        key = self.run_cli("key", fx.d, base, fx.head())
        kp = tempfile.mktemp(suffix=".json")
        rp = tempfile.mktemp(suffix=".txt")
        with open(kp, "w") as f:
            f.write(key)
        with open(rp, "w") as f:
            f.write(f"Session S314 completed #121 (getPedMaxAge) in `{fix[:8]}`. The working tree is clean, nothing uncommitted.")
        sc = json.loads(self.run_cli("report-score", kp, rp))
        self.assertEqual(sc["git_derivable_score"], 1.0)

    def test_the_smoke_command_prints_parse_facts_and_no_score(self):
        out = self.run_cli("smoke", os.path.join(HERE, "pilot", "doc-evidence"))
        self.assertIn("t-remove/R0-r5", out)
        self.assertNotIn("accuracy", out)
        self.assertEqual(len([l for l in out.splitlines() if "/" in l.split()[0]]), 41)


# ---- mutants: one decision broken at a time in a copy of the scorer --------------------------------------------------------------
MUTANTS = [
    ("the moved-line rule is dropped", [("            if t in removed:\n                moved += 1", "            if False:\n                moved += 1")],
     "test_moved_lines_are_not_the_record"),
    ("code, tests and generated files count as the record", [("    if path.startswith(NOT_RECORD_DIRS) or name in NOT_RECORD_NAMES:\n        return False", "    if False:\n        return False")],
     "test_code_tests_generated_are_not_the_record"),
    ("reachability from the pin is not required of a sha", [("if p.returncode == 0 and full in reach:", "if p.returncode == 0:")],
     "test_unreachable_sha_is_defective"),
    ("the receipt format example is read as a receipt", [('if "<" in sess or ">" in sess or not sess:', "if not sess:")],
     "test_template_block_is_skipped"),
    ("the anchor window is 50 lines, not 5", [("ANCHOR_WINDOW = 5 ", "ANCHOR_WINDOW = 50 ")],
     "test_identifier_beside_anchor_must_be_near"),
    ("the line-in-range test is dropped", [("        if a < 1 or hi < a or hi > len(flines):", "        if False:")],
     "test_anchor_beyond_eof_is_defective"),
    ("a path stated removed is held against the record", [('        elif STATED_REMOVED.search(info["ctx"]):\n            out["paths"]["verified"] += 1', '        elif False:\n            out["paths"]["verified"] += 1')],
     "test_absent_path_stated_removed_verifies"),
    ("a bare file name is not resolved by basename", [('if path in nameset or ("/" not in path and any(os.path.basename(n) == path for n in names)):', "if path in nameset:")],
     "test_bare_filename_resolves_by_basename"),
    ("any identifier on the line is beside the anchor", [("        if gap is None or len(gap) > BESIDE_GAP:", "        if gap is None:")],
     "test_far_identifier_is_not_beside"),
    ("a bare number is a sha", [("            if mixed or SHA_CONTEXT_RE.search(line):", "            if True:")],
     "test_numbers_are_not_shas"),
    ("urls are not blanked before paths are read", [("        work = _blanked(line, url_spans)", "        work = line")],
     "test_url_is_not_a_path"),
    ("baseline counts are claims about the end state", [("    if BASELINE_RE.search(line) or NOT_TEST_COUNT.search(line):", "    if NOT_TEST_COUNT.search(line):")],
     "test_baseline_counts_not_claimed"),
    ("a gate summary is read as a test count", [("    if BASELINE_RE.search(line) or NOT_TEST_COUNT.search(line):", "    if BASELINE_RE.search(line):")],
     "test_gate_summaries_and_fractions_are_not_test_counts"),
    ("key=value counts are re-read as prose", [("    rest = _blanked(line, [(m.start(), m.end()) for m in kv])", "    rest = line")],
     "test_key_value_counts_are_paired_by_their_own_keys"),
    ("prose counts need no suite", [("    if SUITE_RE.search(rest):", "    if True:")],
     "test_prose_counts_need_a_suite_in_the_sentence"),
    ("every stated count is checked, not the last of each kind", [("compare_counts(last_claims(refs[\"counts\"]), measured)", "compare_counts(refs[\"counts\"], measured)")],
     "test_only_the_last_stated_count_of_each_kind_is_checked"),
    ("a removal is looked for on the path's own line only", [('        elif STATED_REMOVED.search(info["ctx"]):', '        elif STATED_REMOVED.search(info["line"]):')],
     "test_a_wrapped_list_inherits_the_removal_from_its_neighbours"),
    ("git rm and stale are not statements of absence", [("|git rm|rm|stale|never (?:had|existed)|", "|never (?:had|existed)|")],
     "test_git_rm_and_stale_are_statements_that_a_path_is_gone"),
    ("a slash between two files is one path", [('            for p in _split_joined(m.group(1).removeprefix("./")):', '            for p in [m.group(1).removeprefix("./")]:')],
     "test_a_slash_between_two_files_is_two_paths"),
    ("tool output files are checked against the tree", [("                if os.path.basename(p) in TOOL_OUTPUT_FILES:\n                    continue", "                pass")],
     "test_tool_output_files_are_not_checkable"),
    ("counts are read from every line, not the final message", [("        if source == FINAL_SOURCE:\n            counts.extend(count_claims(line))", "        if True:\n            counts.extend(count_claims(line))")],
     "test_counts_are_read_only_from_the_final_message"),
    ("an anchor's identifier must be within the window even when it names the enclosing function", [("any(i in window or i == enclosing for i in idents)", "any(i in window for i in idents)")],
     "test_an_anchor_naming_its_enclosing_function_verifies"),
    ("a digest is looked for on its own line only", [('DIGEST_BEFORE.search(prev1[-40:] + " " + work[:s])', 'DIGEST_BEFORE.search(work[:s])')],
     "test_a_digest_on_the_next_line_is_not_a_sha"),
    ("a digest after `results` or `manifest` is a sha", [('            if DIGEST_BEFORE.search(prev1[-40:] + " " + work[:s]):\n                continue', "            if False:\n                continue")],
     "test_a_digest_is_not_a_sha"),
    ("the ceiling is strict", [("all(a >= CEILING for a in scored)", "all(a > CEILING for a in scored)")],
     "test_ceiling_boundary"),
    ("the pin commit is owed a name in its own record", [("    own = [c for c in commits if c[0] != pin_full]", "    own = commits")],
     "test_pin_commit_is_not_in_the_denominator"),
    ("pending stubs are always applicable", [("    return any(m in runner for m in RUNNER_PENDING_MARKERS)", "    return True")],
     "test_v30_pending_is_not_applicable"),
    ("the start state's orphan stub is counted as the session's", [('and r["_block"] not in base_blocks]', "]")],
     "test_orphan_stub_from_start_state_is_not_the_sessions"),
    ("a task word after the done word makes it a claim", [("            if not TASK_WORD.search(before[-100:]):\n                continue", "            if not (TASK_WORD.search(before[-100:]) or TASK_WORD.search(after[:100])):\n                continue")],
     "test_says_done_table"),
    ("rather than is not a negator", [("|\\brather than\\b", "")],
     "test_says_done_table"),
    ("a close-out commit is not looked for", [("    if any(is_closeout_subject(subj) for _, subj, _ in session_commits(repo, base, pin)):\n        return True", "    if False:\n        return True")],
     "test_a_closeout_commit_is_a_closeout"),
    ("a claim commit can be a close-out", [("    return bool(CLOSEOUT_SUBJECT.search(subject)) and not CLAIM_SUBJECT.search(subject)", "    return bool(CLOSEOUT_SUBJECT.search(subject))")],
     "test_a_claim_commit_that_names_the_handoff_receipt_is_not_a_closeout"),
    ("the start state's complete receipts count as the session's", [('r["_block"] not in base_blocks\n               for r in parse_receipts(blob(repo, pin, "HANDOFFS.md") or ""))', 'True\n               for r in parse_receipts(blob(repo, pin, "HANDOFFS.md") or ""))')],
     "test_a_complete_receipt_the_session_wrote_is_a_closeout_and_the_starts_is_not"),
    ("a disclosure anywhere in the record counts for any document", [("            if DISCLOSES.search(\" \".join(near)):", "            if DISCLOSES.search(\" \".join(r[1] for r in rec_lines)):")],
     "test_the_disclosure_must_be_near_the_name"),
    ("a longer file name is the named document", [('re.search(r"(?<![\\w/.-])(?:%s|%s)(?![\\w-]|\\.\\w)" % (re.escape(doc_path), re.escape(base)), line)', 're.search(re.escape(base), line)')],
     "test_a_longer_file_name_is_not_the_named_document"),
    ("negation is ignored when reading done", [("            if NEG_BEFORE.search(before) or NEG_AFTER.search(after):\n                continue", "            if False:\n                continue")],
     "test_says_done_table"),
    ("the receipt's own status field is read as a done claim", [("        if STATUS_FIELD.match(line):\n            continue", "        if False:\n            continue")],
     "test_receipt_status_is_not_a_done_claim"),
    ("a part does not end at a blank line", [("            if not line:\n                cur = None\n            elif PART_LABEL", "            if False:\n                cur = None\n            elif PART_LABEL")],
     "test_a_notes_paragraph_part_ends_at_the_blank_line"),
    ("completeness is not checked against the report", [('        facts["complete"] = says_complete == bool(g["complete"])', '        facts["complete"] = True')],
     "test_wrong_completeness_is_false_and_the_wrong_session_is_false"),
    ("the ledger finding is summed into the score", [("    return {\"git_derivable\": facts, \"git_derivable_score\"", "    facts[\"ledger\"] = bool(LEDGER_FINDING.search(text))\n    return {\"git_derivable\": facts, \"git_derivable_score\"")],
     "test_ledger_finding_is_not_in_the_score"),
    ("the record is only the last commit's diff", [('    text = git(repo, "diff", "--no-renames", "--no-color", "-U0", base, pin)', '    text = git(repo, "diff", "--no-renames", "--no-color", "-U0", f"{pin}~1", pin)')],
     "test_the_record_spans_every_commit_of_the_session"),
]


def _find_test(name):
    for cls in (RecordTests, ReceiptTests, M1Tests, M2Tests, InclusionTests, M3Tests, M4Tests):
        if hasattr(cls, name):
            return cls(name)
    raise KeyError(name)


def _run(path, name, test):
    old = _MOD[0]
    _MOD[0] = _load(path, name)
    try:
        return unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(unittest.TestSuite([test]))
    finally:
        _MOD[0] = old


class Mutants(unittest.TestCase):
    """One decision broken at a time in a copy of the scorer; the named test must go red, and must be green on an unbroken copy at
    the same path, so a red test is the mutation's doing and not the copy's."""

    @staticmethod
    def make(name, edits, test_name):
        def test(self):
            with open(SCORER, encoding="utf-8") as f:
                src = f.read()
            d = tempfile.mkdtemp()
            self.addCleanup(shutil.rmtree, d, ignore_errors=True)
            control, mutant = os.path.join(d, "control_doc_score.py"), os.path.join(d, "mutant_doc_score.py")
            with open(control, "w", encoding="utf-8") as f:
                f.write(src)
            for old, new in edits:
                self.assertEqual(src.count(old), 1, f"mutation anchor must occur exactly once: {old!r}")
                src = src.replace(old, new)
            with open(mutant, "w", encoding="utf-8") as f:
                f.write(src)
            _load(mutant, "mutant_probe")                      # a file that no longer imports is a typo, not a mutant
            self.assertTrue(_run(control, "control_probe", _find_test(test_name)).wasSuccessful(), f"{test_name} is red on an UNBROKEN copy")
            self.assertFalse(_run(mutant, "mutant_run", _find_test(test_name)).wasSuccessful(), f"{test_name} stayed green with: {name}")
        return test


for _i, (_n, _e, _t) in enumerate(MUTANTS, 1):
    setattr(Mutants, f"test_mutant{_i:02d}_{re.sub(r'[^a-z0-9]+', '_', _n.lower())[:52]}", Mutants.make(_n, _e, _t))


if __name__ == "__main__":
    unittest.main()
