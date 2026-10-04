#!/usr/bin/env python3
"""Tests for probe.py (BL-94 P2a (a)): the cold-start probe driven against a FAKE `claude`, before it is pointed at a real one.

    python3 docs/planning/overhead-replay/tests_probe.py

Synthetic repositories and a stand-in process only: no model, no spend, no run tree, not the project. The plan (section 5 P2a (a)) puts this
in `tests.py`; it is its own file, as `tests_doc_evidence.py` and `tests_p1b.py` are, so it runs in seconds on its own and can be run
against mutants of `probe.py` (`mutants_p2a.py`). The technique is `tests.py`'s `DriverAgainstFakeClaude`. A fake cannot show that a
real model stops where the fake does: that is what the pilot (P2) is for.
"""
import json, os, shutil, subprocess, sys, tempfile, textwrap, unittest
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doc_evidence as D
import driver
import probe as P
from tests_doc_evidence import make_project, run_for
from tests_ratchet import sh, write, commit, ENV

RID = "t/x-r1"
FAKE = textwrap.dedent("""
    import sys, json, os
    seen = os.path.join(%(seen)r, "seen.jsonl")
    mode = %(mode)r
    if mode == "dies":
        sys.exit(3)
    print(json.dumps({"type": "system", "subtype": "init", "session_id": "sidP", "model": "m"}), flush=True)
    for line in sys.stdin:
        text = json.loads(line)["message"]["content"][0]["text"]
        open(seen, "a").write(json.dumps({"cwd": os.getcwd(), "text": text}) + "\\n")
        if mode == "silent":
            sys.exit(0)
        if mode == "budget":
            print(json.dumps({"type": "result", "subtype": "error_max_budget_usd", "is_error": True, "session_id": "sidP", "total_cost_usd": 2.01}), flush=True)
        elif mode == "capped":
            print(json.dumps({"type": "result", "subtype": "success", "session_id": "sidP", "total_cost_usd": 2.0, "result": "a report cut short"}), flush=True)
        elif mode == "budget_text":
            print(json.dumps({"type": "result", "subtype": "error_max_budget_usd", "is_error": True, "session_id": "sidP", "total_cost_usd": 0.8,
                              "result": "I had read the runner and was part way through the report"}), flush=True)
        else:
            print("not json, as a CLI warning line may be", flush=True)
            print(json.dumps({"type": "result", "subtype": "success", "session_id": "sidP", "total_cost_usd": 0.37, "result": "Phase 0 report: S2, #1"}), flush=True)
""")


def fake(mode="ok"):
    d = tempfile.mkdtemp(prefix="fakeclaude-")
    path = os.path.join(d, "fake.py")
    with open(path, "w") as f:
        f.write(FAKE % {"seen": d, "mode": mode})
    return path, d


def seen(d):
    p = os.path.join(d, "seen.jsonl")
    return [json.loads(l) for l in open(p)] if os.path.exists(p) else []


def make_tree(project):
    """A run tree: the project's start commit, the harness install commit (author Fixture), then two session commits that change code
    and test files (not record), a record file (SESSION_NOTES.md) and add a record file (NEWS.md) and a generated file (man/x.Rd)."""
    t = tempfile.mkdtemp(prefix="probetree-")
    shutil.rmtree(t)
    sh(project, "clone", "-q", "--no-local", project, t)
    write(t, "SESSION_NOTES.md", "notes at install\n"); write(t, "R/x.R", "x <- function() 1\n"); write(t, "CLAUDE.md", "rules\n")
    sh(t, "add", "-A")
    subprocess.run(["git", "-C", t, "commit", "-q", "--no-verify", "-m", "Install methodology arm v9"],
                   env=dict(ENV, GIT_AUTHOR_NAME="Fixture", GIT_COMMITTER_NAME="Fixture"), check=True)
    install = sh(t, "rev-parse", "HEAD")
    write(t, "R/x.R", "x <- function() 2\n"); write(t, "tests/test_x.R", "expect_equal(x(), 2)\n")
    s1 = commit(t, "fix: #1 S2 -- x returns 2")
    write(t, "SESSION_NOTES.md", "notes at install\nS2 did #1 in " + s1[:7] + "\n"); write(t, "NEWS.md", "x now returns 2\n"); write(t, "man/x.Rd", "\\name{x}\n")
    s2 = commit(t, "docs: #1 S2 -- close-out")
    return t, install, s1, s2


class Base(unittest.TestCase):
    def setUp(self):
        self.project, self.start = make_project()
        self.tree, self.install, self.s1, self.s2 = make_tree(self.project)
        self.evidence = tempfile.mkdtemp(prefix="probeev-")
        self.out = os.path.join(tempfile.mkdtemp(prefix="probeout-"), "ledger")
        self.work = tempfile.mkdtemp(prefix="probework-")
        for d in (self.project, self.tree, self.evidence, os.path.dirname(self.out), self.work):
            self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        self.build()

    def build(self, tree=None):
        self.manifest = D.build(self.evidence, self.project, [run_for(tree or self.tree, self.start, RID)])

    def go(self, mode="ok", control=None, session_cap=2.0, total_cap=10.0, **kw):
        path, d = fake(mode)
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        kw.setdefault("argv", [sys.executable, path])
        row = P.run_probe(RID, session_cap, total_cap, control, evidence=self.evidence, project=self.project, out=self.out, work=self.work, **kw)
        return row, d

    def refused(self, *a, **kw):
        with self.assertRaises(P.Refused) as c:
            self.go(*a, **kw)
        return str(c.exception)


class OneTurn(Base):
    def test_the_session_opens_with_go_once_in_the_clone_and_the_row_records_it(self):
        row, d = self.go()
        s = seen(d)
        self.assertEqual([x["text"] for x in s], ["go"])                       # one message: the probe stops at its first stop
        self.assertEqual(os.path.realpath(s[0]["cwd"]), os.path.realpath(row["clone_dir"]))
        self.assertEqual((row["stops"], row["probe_ok"], row["launched"]), (1, True, True))
        self.assertTrue(row["end"].startswith("cut off after 1"))
        self.assertEqual(row["cost_usd"], 0.37)

    def test_the_report_is_the_last_result_text_and_is_saved_with_the_stream(self):
        row, _ = self.go()
        base = os.path.join(self.out, P.slug(RID))
        self.assertEqual(open(os.path.join(base, "report.md")).read(), "Phase 0 report: S2, #1")
        self.assertTrue(os.path.getsize(os.path.join(base, "stream.jsonl")) > 0)
        self.assertEqual(row["report"], os.path.join(P.slug(RID), "report.md"))

    def test_one_spend_line_and_one_row_per_probe(self):
        self.go()
        spend = [json.loads(l) for l in open(os.path.join(self.out, "spend.jsonl"))]
        self.assertEqual([(x["cost_usd"], x["run"], x["control"], x["kind"]) for x in spend], [(0.37, RID, None, "probe")])
        rows = [json.loads(l) for l in open(os.path.join(self.out, "rows.jsonl"))]
        self.assertEqual(len(rows), 1)
        self.assertEqual(driver.spent(self.out), 0.37)                         # the driver's own ledger reader sums it

    def test_the_real_command_line_carries_the_session_cap_and_the_isolation_flags(self):
        path, d = fake()
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        got = {}
        def popen(argv, **kw):
            got["argv"] = argv
            return subprocess.Popen([sys.executable, path], **kw)
        P.run_probe(RID, 1.5, 10.0, evidence=self.evidence, project=self.project, out=self.out, work=self.work, popen=popen,
                    help_text=" ".join(P.cli_flags(driver.cmd("sonnet", 1.5))))
        a = got["argv"]
        self.assertEqual(a[a.index("--max-budget-usd") + 1], "1.5")
        self.assertEqual(a[a.index("--setting-sources") + 1], "")
        for flag in ("--strict-mcp-config", "--disable-slash-commands"):
            self.assertIn(flag, a)
        self.assertEqual(a[a.index("--model") + 1], "sonnet")

    def test_a_budget_stop_is_recorded_as_a_failed_probe_and_its_cost_still_counts(self):
        row, _ = self.go("budget")
        self.assertEqual((row["probe_ok"], row["stops"], row["end"]), (False, 0, "result error_max_budget_usd"))
        self.assertEqual(driver.spent(self.out), 2.01)                         # money was spent: the ledger must say so

    def test_an_error_result_that_carries_text_is_still_a_failed_probe(self):
        row, _ = self.go("budget_text")
        self.assertEqual((row["probe_ok"], row["stops"]), (False, 0))            # text exists, but the turn never finished
        self.assertTrue(os.path.exists(os.path.join(self.out, P.slug(RID), "report.md")))      # kept, so a reader can see how far it got

    def test_a_result_that_says_success_at_the_session_cap_is_not_a_good_probe(self):
        row, _ = self.go("capped", session_cap=2.0)
        self.assertEqual((row["stops"], row["cap_hit"], row["probe_ok"]), (1, True, False))      # the CLI's own cap message was never observed
        row2, _ = self.go("capped", control="git-only", session_cap=5.0)
        self.assertEqual((row2["cap_hit"], row2["probe_ok"]), (False, True))                    # the same $2.00 under a $5.00 cap is a finished probe

    def test_a_session_that_exits_without_a_result_is_a_failed_probe_with_no_report(self):
        row, _ = self.go("silent")
        self.assertEqual((row["probe_ok"], row["stops"], row["end"], row["report"], row["cost_usd"]), (False, 0, "process exited", None, 0.0))

    def test_a_process_that_dies_before_reading_is_a_failed_probe_that_cost_nothing(self):
        row, _ = self.go("dies")                    # whether the write hits a closed pipe is a race: either end is a failed probe
        self.assertFalse(row["probe_ok"])
        self.assertTrue(row["end"] == "process exited" or row["end"].startswith("driver error"), row["end"])
        self.assertEqual(driver.spent(self.out), 0.0)

    def test_a_cli_that_cannot_be_started_is_recorded_not_raised(self):
        def popen(argv, **kw):
            raise FileNotFoundError("claude")
        row, _ = self.go(popen=popen)
        self.assertEqual((row["probe_ok"], row["stops"], row["cost_usd"]), (False, 0, 0.0))
        self.assertTrue(row["end"].startswith("driver error FileNotFoundError"), row["end"])
        self.assertEqual(len(open(os.path.join(self.out, "rows.jsonl")).read().splitlines()), 1)     # it is on the record, so a rerun is a decision


class TheClone(Base):
    def test_the_clone_is_the_pinned_commit_with_no_remote_and_a_clean_tree(self):
        row, _ = self.go(launch=False)
        c = row["clone"]
        self.assertEqual(c["head"], self.s2)
        self.assertEqual((c["head_is_pin"], c["install_is_ancestor"], c["remotes"], c["tracked_clean"]), (True, True, [], True))
        self.assertEqual(c["commits"], 4)                                      # start, install and two session commits

    def test_a_pin_before_head_leaves_the_later_commits_out_of_the_clone(self):
        write(self.tree, "late.md", "after the pin\n")
        late = commit(self.tree, "docs: after the close-out")
        D.PIN_OVERRIDES[RID] = self.s2[:8]
        self.addCleanup(D.PIN_OVERRIDES.pop, RID, None)
        self.build()
        self.assertEqual(self.manifest["runs"][0]["head"], late)
        row, _ = self.go(launch=False)
        self.assertEqual(row["clone"]["head"], self.s2)
        self.assertTrue(row["clone"]["later_commits_absent"])
        self.assertEqual(subprocess.run(["git", "-C", row["clone_dir"], "cat-file", "-e", late], capture_output=True).returncode != 0, True)

    def test_a_ref_that_does_not_hold_the_manifest_pin_is_refused_before_checkout(self):
        D.PIN_OVERRIDES[RID] = self.s1[:8]
        self.addCleanup(D.PIN_OVERRIDES.pop, RID, None)
        self.build()
        scratch, manifest = D.rebuild(self.evidence, self.project)
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        run = dict(manifest["runs"][0], pin=self.install)                      # the manifest now claims a pin the pin ref does not hold
        dest = os.path.join(self.work, "x")
        with self.assertRaises(P.Refused) as c:
            P.build_clone(scratch, run, dest)
        self.assertIn("fetched", str(c.exception))
        self.assertFalse(os.path.exists(os.path.join(dest, "R")))              # nothing was checked out

    def test_an_existing_destination_is_never_overwritten(self):
        os.makedirs(os.path.join(self.work, P.slug(RID)))
        self.assertIn("exists", self.refused(launch=False))

    def test_the_scratch_repository_is_removed_after_the_clone_is_built(self):
        made = []
        real = D.rebuild
        def spy(*a, **k):
            r = real(*a, **k)
            made.append(r[0])
            return r
        D.rebuild = spy
        self.addCleanup(setattr, D, "rebuild", real)
        self.go(launch=False)
        self.assertEqual(len(made), 1)
        self.assertFalse(os.path.exists(made[0]))

    def test_each_failing_clone_fact_refuses(self):
        good = {"head_is_pin": True, "install_is_ancestor": True, "later_commits_absent": None, "remotes": [], "tracked_clean": True}
        P.verify_clone(good)
        for k, bad in (("head_is_pin", False), ("install_is_ancestor", False), ("later_commits_absent", False), ("remotes", ["origin"]), ("tracked_clean", False)):
            with self.assertRaises(P.Refused, msg=k):
                P.verify_clone(dict(good, **{k: bad}))


class GitOnlyControl(Base):
    def test_record_files_return_to_the_install_text_and_code_stays_at_the_pin(self):
        row, _ = self.go(control="git-only", launch=False)
        d, c = row["clone_dir"], row["control_detail"]
        self.assertEqual(c["restored"], ["SESSION_NOTES.md"])
        self.assertEqual(c["removed"], ["NEWS.md"])
        self.assertEqual(open(os.path.join(d, "SESSION_NOTES.md")).read(), "notes at install\n")
        self.assertFalse(os.path.exists(os.path.join(d, "NEWS.md")))
        self.assertEqual(open(os.path.join(d, "R/x.R")).read(), "x <- function() 2\n")        # the session's code is still there
        self.assertTrue(os.path.exists(os.path.join(d, "tests/test_x.R")))
        self.assertTrue(os.path.exists(os.path.join(d, "man/x.Rd")))                       # generated output is not the record

    def test_it_is_one_commit_on_the_pin_so_every_session_sha_still_resolves(self):
        row, _ = self.go(control="git-only", launch=False)
        d, c = row["clone_dir"], row["control_detail"]
        self.assertTrue(c["parent_is_pin"])
        self.assertEqual(sh(d, "rev-parse", "HEAD"), c["commit"])
        self.assertEqual(sh(d, "log", "-1", "--format=%s"), P.CONTROL_SUBJECT)
        for s in (self.s1, self.s2):
            self.assertEqual(sh(d, "cat-file", "-t", s), "commit")
        self.assertEqual(sh(d, "status", "--porcelain"), "")

    def test_a_control_and_its_end_state_get_different_directories(self):
        a, _ = self.go(launch=False)
        b, _ = self.go(control="git-only", launch=False)
        self.assertNotEqual(a["clone_dir"], b["clone_dir"])
        self.assertTrue(b["clone_dir"].endswith("+git-only"))

    def test_the_probe_session_runs_in_the_control_clone(self):
        row, d = self.go(control="git-only")
        self.assertEqual(os.path.realpath(seen(d)[0]["cwd"]), os.path.realpath(row["clone_dir"]))
        self.assertEqual(row["control"], "git-only")

    def test_a_session_that_changed_no_record_file_has_no_control(self):
        tree, install, _, s2 = make_tree(self.project)
        sh(tree, "reset", "-q", "--hard", install)
        write(tree, "R/x.R", "x <- function() 3\n")
        commit(tree, "fix: code only")
        self.build(tree)
        self.assertIn("no record file", self.refused(control="git-only", launch=False))


class Refusals(Base):
    def test_spent_plus_the_session_cap_over_the_total_is_refused_before_any_clone_is_built(self):
        os.makedirs(self.out)
        with open(os.path.join(self.out, "spend.jsonl"), "w") as f:
            f.write(json.dumps({"cost_usd": 8.5}) + "\n")
        msg = self.refused(session_cap=2.0, total_cap=10.0)
        self.assertIn("refused: spent $8.50 + session cap $2.00 > total cap $10.00", msg)
        self.assertEqual(os.listdir(self.work), [])

    def test_spent_plus_the_session_cap_equal_to_the_total_is_allowed(self):
        os.makedirs(self.out)
        with open(os.path.join(self.out, "spend.jsonl"), "w") as f:
            f.write(json.dumps({"cost_usd": 8.0}) + "\n")
        row, _ = self.go(session_cap=2.0, total_cap=10.0)
        self.assertTrue(row["probe_ok"])

    def test_the_same_probe_twice_is_refused_unless_asked_for(self):
        self.go()
        self.assertIn("probed already", self.refused())
        shutil.rmtree(os.path.join(self.work, P.slug(RID)))
        row, _ = self.go(again=True)
        self.assertTrue(row["probe_ok"])

    def test_a_control_is_not_the_same_probe_as_its_end_state(self):
        self.go()
        row, _ = self.go(control="git-only")
        self.assertTrue(row["probe_ok"])

    def test_an_unknown_run_is_refused_and_says_where_to_look(self):
        with self.assertRaises(P.Refused) as c:
            P.run_probe("nope/x-r9", 2.0, 10.0, evidence=self.evidence, project=self.project, out=self.out, work=self.work, argv=[sys.executable, "-c", "0"])
        self.assertIn("--list", str(c.exception))

    def test_a_run_with_tracked_edits_never_committed_is_refused(self):
        write(self.tree, "SESSION_NOTES.md", "edited and never committed\n")
        self.build()
        msg = self.refused(launch=False)
        self.assertIn("never committed", msg)
        self.assertIn("SESSION_NOTES.md", msg)

    def test_a_run_with_no_install_commit_is_refused(self):
        run = dict(self.manifest["runs"][0], install=None)
        with self.assertRaises(P.Refused):
            P.refuse_unprobable(run)

    def test_a_control_name_other_than_git_only_is_refused(self):
        self.assertIn("control must be", self.refused(control="nope"))

    def test_a_cli_that_lost_a_flag_is_refused_before_a_clone_is_built(self):
        argv = driver.cmd("sonnet", 2.0)
        flags = P.cli_flags(argv)
        self.assertEqual(P.check_cli_flags(argv, " ".join(flags)), flags)
        with self.assertRaises(P.Refused) as c:
            P.check_cli_flags(argv, " ".join(f for f in flags if f != "--setting-sources"))
        self.assertIn("--setting-sources", str(c.exception))

    def test_the_flag_check_runs_on_the_real_command_before_any_clone_is_built(self):
        path, d = fake()
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        flags = P.cli_flags(driver.cmd("sonnet", 2.0))
        popen = lambda argv, **kw: subprocess.Popen([sys.executable, path], **kw)
        with self.assertRaises(P.Refused) as c:
            P.run_probe(RID, 2.0, 10.0, evidence=self.evidence, project=self.project, out=self.out, work=self.work, popen=popen,
                        help_text=" ".join(f for f in flags if f != "--effort"))
        self.assertIn("--effort", str(c.exception))
        self.assertEqual(os.listdir(self.work), [])
        self.assertEqual(seen(d), [])

    def test_a_clone_that_fails_its_own_checks_is_never_launched_into(self):
        real = P.clone_facts
        P.clone_facts = lambda dest, run: dict(real(dest, run), remotes=["origin"])
        self.addCleanup(setattr, P, "clone_facts", real)
        path, d = fake()
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        with self.assertRaises(P.Refused) as c:
            P.run_probe(RID, 2.0, 10.0, evidence=self.evidence, project=self.project, out=self.out, work=self.work, argv=[sys.executable, path])
        self.assertIn("not the end state", str(c.exception))
        self.assertEqual(seen(d), [])
        self.assertFalse(os.path.exists(os.path.join(self.out, "spend.jsonl")))

    def test_the_real_cli_flags_the_driver_uses_are_all_set_by_the_command(self):
        self.assertEqual(P.cli_flags(driver.cmd("sonnet", 2.0)),
                         sorted(["--max-budget-usd", "--setting-sources", "--strict-mcp-config", "--disable-slash-commands", "--allowedTools",
                                 "--permission-mode", "--input-format", "--output-format", "--verbose", "--model", "--effort"]))

    def test_no_launch_spends_nothing_and_writes_no_ledger(self):
        row, d = self.go(launch=False)
        self.assertFalse(row["launched"])
        self.assertEqual(seen(d), [])
        self.assertFalse(os.path.exists(self.out))


class Pieces(unittest.TestCase):
    def test_report_text_takes_the_last_result_that_has_text_and_skips_noise(self):
        log = ["warning: not json\n", json.dumps({"type": "result", "result": "one"}) + "\n", json.dumps({"type": "assistant"}) + "\n",
               json.dumps({"type": "result", "subtype": "error", "is_error": True}) + "\n", json.dumps({"type": "result", "result": "two"}) + "\n"]
        self.assertEqual(P.report_text(log), "two")
        self.assertIsNone(P.report_text(["x\n", json.dumps({"type": "result"}) + "\n"]))

    def test_phase0_reads_are_the_read_tool_paths_in_order(self):
        ev = [{"kind": "tool_use", "name": "Read", "input": {"file_path": "/a/SAFEGUARDS.md"}},
              {"kind": "text", "text": "hi"},
              {"kind": "tool_use", "name": "Bash", "input": {"command": "cat /a/b"}},
              {"kind": "tool_use", "name": "Read", "input": {"file_path": "/a/SESSION_NOTES.md"}}]
        self.assertEqual(P.phase0_reads(ev), ["/a/SAFEGUARDS.md", "/a/SESSION_NOTES.md"])

    def test_slug_has_no_path_separator_and_separates_the_control(self):
        self.assertEqual(P.slug("real-3.7/v3.0-r3"), "real-3.7--v3.0-r3")
        self.assertEqual(P.slug("real-3.7/v3.0-r3", "git-only"), "real-3.7--v3.0-r3+git-only")

    def test_the_probe_script_is_the_operators_go_and_nothing_else(self):
        self.assertEqual(P.PROBE_SCRIPT, ["go"])


class VerifyAll(Base):
    def test_every_run_rebuilds_as_an_end_state_and_a_control_and_no_clone_is_left_behind(self):
        work = tempfile.mkdtemp(prefix="verifyall-")
        self.addCleanup(shutil.rmtree, work, ignore_errors=True)
        lines = []
        rows = P.verify_all(self.evidence, self.project, work, say=lines.append)
        self.assertEqual([(r["id"], r["end_state"], r["git-only"], r["ok"]) for r in rows], [(RID, "ok", "ok", True)])
        self.assertEqual(len(lines), 1)
        self.assertEqual([n for n in os.listdir(work) if n != "ledger"], [])

    def test_a_run_with_uncommitted_files_is_refused_by_design_and_counts_as_expected(self):
        write(self.tree, "SESSION_NOTES.md", "edited and never committed\n")
        self.build()
        work = tempfile.mkdtemp(prefix="verifyall-")
        self.addCleanup(shutil.rmtree, work, ignore_errors=True)
        rows = P.verify_all(self.evidence, self.project, work, say=lambda s: None)
        self.assertTrue(rows[0]["expected_refusal"] and rows[0]["ok"])
        self.assertTrue(rows[0]["end_state"].startswith("refused"))

    def test_a_bundle_that_cannot_rebuild_a_run_that_should_is_not_ok(self):
        real = P.build_clone
        def broken(scratch, run, dest):
            raise P.Refused("fetched the wrong thing")
        P.build_clone = broken
        self.addCleanup(setattr, P, "build_clone", real)
        work = tempfile.mkdtemp(prefix="verifyall-")
        self.addCleanup(shutil.rmtree, work, ignore_errors=True)
        rows = P.verify_all(self.evidence, self.project, work, say=lambda s: None)
        self.assertFalse(rows[0]["ok"])


class Command(Base):
    def test_both_caps_are_required_to_launch(self):
        with self.assertRaises(SystemExit) as c:
            P.main(["real-3.7/v3.0-r3", "--session-cap", "2"])
        self.assertEqual(c.exception.code, 2)

    def test_list_names_every_run_and_marks_the_ones_a_bundle_cannot_rebuild(self):
        write(self.tree, "SESSION_NOTES.md", "edited and never committed\n")
        self.build()
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            P.main(["--list", "--evidence", self.evidence])
        self.assertIn(RID, buf.getvalue())
        self.assertIn("REFUSED", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
