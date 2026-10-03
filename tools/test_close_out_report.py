#!/usr/bin/env python3
"""Tests for starter-kit/close_out_report.py -- the Phase 3G report generator and lint.

CANONICAL-ONLY (not in bin/_manifest.py until the plan's P3). Imports the starter-kit module
directly, so what is tested is what would ship. stdlib unittest.

Every lint rule is observed REFUSING a corrupted report (a rule never seen to fire is a
suggestion), and the property test renders a report for every complete receipt this repository
has ever kept -- the live ledger and every archived shard -- and requires each to lint clean.
"""
import glob
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True  # keep starter-kit/ free of __pycache__

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TOOL = os.path.join(REPO, "starter-kit", "close_out_report.py")
_spec = importlib.util.spec_from_file_location("close_out_report", TOOL)
cor = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cor)

LEDGER = """# Handoffs

```handoff
session: S2
date: 2026-10-03
status: {status}
self_score: 8
predecessor_score: 7
active_task: demo
runtime_smoke: n/a; quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results abc
```

```handoff
session: S1
date: 2026-10-02
status: complete
self_score: 7
predecessor_score: 8
active_task: x
```
"""
TEXTS = dict(deliverable="demo", outcome="done", well="a", badly="b", predecessor="c", nxt="d")


def sh(*a, cwd):
    return subprocess.run(a, cwd=cwd, capture_output=True, text=True, check=True).stdout


def make_repo(status="complete"):
    t = tempfile.mkdtemp()
    sh("git", "init", "-q", ".", cwd=t)
    sh("git", "config", "user.email", "t@e.com", cwd=t)
    sh("git", "config", "user.name", "T", cwd=t)
    sh("git", "config", "commit.gpgsign", "false", cwd=t)
    with open(os.path.join(t, "HANDOFFS.md"), "w", encoding="utf-8") as f:
        f.write(LEDGER.format(status=status))
    sh("git", "add", ".", cwd=t)
    sh("git", "commit", "-qm", "c", cwd=t)
    return t


def run_cli(*args, cwd, stdin=None):
    return subprocess.run([sys.executable, TOOL, *args], cwd=cwd, input=stdin, capture_output=True, text=True)


class Parse(unittest.TestCase):
    def test_receipts_in_order_first_line_value(self):
        r = cor.parse_receipts(LEDGER.format(status="complete"))
        self.assertEqual([x["session"] for x in r], ["S2", "S1"])
        self.assertEqual(r[0]["self_score"], "8")

    def test_prose_mentioning_the_fence_is_not_a_receipt(self):
        s = "run `grep -c '^```handoff' HANDOFFS.md`\n" + LEDGER.format(status="complete")
        self.assertEqual(len(cor.parse_receipts(s)), 2)

    def test_gate_citation_and_default(self):
        r = cor.parse_receipts(LEDGER.format(status="complete"))
        self.assertEqual(cor.facts(r[0], r[1], "h", 0)["gate"], "11/11 pass · 0 fail · 0 unmeasured")
        self.assertEqual(cor.facts(r[1], {}, "h", 0)["gate"], "not cited")


class Render(unittest.TestCase):
    def setUp(self):
        self.repo = make_repo()
        self.addCleanup(lambda: __import__("shutil").rmtree(self.repo))
        self.m = cor.live_facts(os.path.join(self.repo, "HANDOFFS.md"), self.repo)

    def good(self):
        return cor.render(self.m, *TEXTS.values())

    def test_output_lints_clean_and_has_the_shape(self):
        t = self.good()
        self.assertEqual(cor.lint(t, self.m), [])
        self.assertTrue(t.startswith("## Close-out report: S2 · 2026-10-03\n"))
        self.assertTrue(t.endswith("\nSession over.\n"))
        self.assertIn("**Predecessor handoff (S1):** 7/10", t)

    def test_head_is_computed_from_git_not_the_receipt(self):
        self.assertEqual(self.m["head"], sh("git", "rev-parse", "--short", "HEAD", cwd=self.repo).strip())

    def test_refuses_each_empty_text(self):
        for i, k in enumerate(cor.FIELDS):
            v = list(TEXTS.values())
            v[i] = " "
            with self.assertRaises(ValueError, msg=k):
                cor.render(self.m, *v)

    def test_refuses_over_long_text_instead_of_truncating(self):
        v = list(TEXTS.values())
        v[2] = "x" * (cor.FIELD_MAX + 1)
        with self.assertRaisesRegex(ValueError, "301 characters"):
            cor.render(self.m, *v)

    def test_accepts_exactly_the_field_cap(self):
        v = list(TEXTS.values())
        v[2] = "x" * cor.FIELD_MAX
        self.assertEqual(cor.lint(cor.render(self.m, *v), self.m), [])

    def test_refuses_pipe_and_newline(self):
        for bad in ("a | b", "a\nb"):
            v = list(TEXTS.values())
            v[4] = bad
            with self.assertRaises(ValueError):
                cor.render(self.m, *v)

    def test_worst_case_fits_the_total_cap(self):
        m = dict(self.m, gate="x" * 60)
        full = ["y" * cor.FIELD_MAX, "y" * cor.OUTCOME_MAX] + ["y" * cor.FIELD_MAX] * 4
        self.assertLessEqual(len(cor.render(m, *full).encode()), cor.TOTAL_MAX)

    def test_refuses_a_paragraph_as_the_outcome(self):
        v = list(TEXTS.values())
        v[1] = "z" * (cor.OUTCOME_MAX + 1)
        with self.assertRaisesRegex(ValueError, "--outcome"):
            cor.render(self.m, *v)


class LintMutants(unittest.TestCase):
    """Ten corruptions of a good report; each must be refused, and by the rule it targets."""

    def setUp(self):
        self.repo = make_repo()
        self.addCleanup(lambda: __import__("shutil").rmtree(self.repo))
        self.m = cor.live_facts(os.path.join(self.repo, "HANDOFFS.md"), self.repo)
        self.good = cor.render(self.m, *TEXTS.values())

    def refused(self, text, rule):
        errs = cor.lint(text, self.m)
        self.assertTrue(any(e.startswith(rule) for e in errs), f"{rule} not raised: {errs}")

    def test_drop_closing_line(self):
        self.refused(self.good.replace("\nSession over.\n", "\n"), "R3")

    def test_text_after_closing_line(self):
        self.refused(self.good + "\nShall I continue?\n", "R3")

    def test_prefix_before_heading(self):
        self.refused("Here is the summary:\n\n" + self.good, "R1")

    def test_heading_names_another_session(self):
        self.refused(self.good.replace("S2 ·", "S9 ·"), "R1")

    def test_wrong_self_score(self):
        self.refused(self.good.replace("8/10", "9/10"), "R4")

    def test_wrong_predecessor_score(self):
        self.refused(self.good.replace("7/10", "6/10"), "R4")

    def test_stale_head(self):
        self.refused(self.good.replace(self.m["head"], "deadbee"), "R5")

    def test_missing_label(self):
        self.refused(self.good.replace("**Next session:**", "Next:"), "R2")

    def test_labels_out_of_order(self):
        t = self.good.replace("**Record:**", "**Zed:**").replace("**Next session:**", "**Record:**")
        self.refused(t.replace("**Zed:**", "**Next session:**"), "R2")

    def test_table_pipe(self):
        self.refused(self.good.replace("DONE", "DONE | x"), "R6")

    def test_over_total_cap(self):
        self.refused(self.good.replace("demo", "x" * 2100, 1), "R7")

    def test_empty_message_is_refused_not_crashed(self):
        self.assertTrue(cor.lint("", self.m))


class Cli(unittest.TestCase):
    def setUp(self):
        self.repo = make_repo()
        self.addCleanup(lambda: __import__("shutil").rmtree(self.repo))
        self.args = ["--deliverable", "demo", "--outcome", "done", "--well", "a", "--badly", "b",
                     "--predecessor", "c", "--next", "d"]

    def test_print_then_check_round_trip(self):
        p = run_cli(*self.args, cwd=self.repo)
        self.assertEqual(p.returncode, 0, p.stderr)
        c = run_cli("--check", "-", cwd=self.repo, stdin=p.stdout)
        self.assertEqual((c.returncode, c.stdout.strip()), (0, "OK"))

    def test_check_refuses_a_hand_written_report(self):
        c = run_cli("--check", "-", cwd=self.repo, stdin="Done. All shipped.\n")
        self.assertEqual(c.returncode, 1)
        self.assertIn("R1", c.stdout)

    def test_report_goes_stale_after_a_commit(self):
        p = run_cli(*self.args, cwd=self.repo)
        with open(os.path.join(self.repo, "n.txt"), "w") as f:
            f.write("x")
        sh("git", "add", ".", cwd=self.repo)
        sh("git", "commit", "-qm", "later", cwd=self.repo)
        c = run_cli("--check", "-", cwd=self.repo, stdin=p.stdout)
        self.assertEqual(c.returncode, 1)
        self.assertIn("R5", c.stdout)

    def test_missing_text_is_refused_with_exit_2(self):
        p = run_cli("--deliverable", "demo", cwd=self.repo)
        self.assertEqual(p.returncode, 2)
        self.assertIn("--outcome is required", p.stderr)

    def test_pending_receipt_is_refused(self):
        r = make_repo("pending")
        self.addCleanup(lambda: __import__("shutil").rmtree(r))
        p = run_cli(*self.args, cwd=r)
        self.assertEqual(p.returncode, 2)
        self.assertIn("not complete", p.stderr)

    def test_missing_ledger_is_refused(self):
        p = run_cli(*self.args, "--ledger", "nope.md", cwd=self.repo)
        self.assertEqual(p.returncode, 2)

    def test_dirty_count_is_reported(self):
        with open(os.path.join(self.repo, "u.txt"), "w") as f:
            f.write("x")
        self.assertIn("1 uncommitted", run_cli(*self.args, cwd=self.repo).stdout)


class Property(unittest.TestCase):
    """A report for every complete receipt the repository has ever kept lints clean."""

    def receipts(self):
        paths = [os.path.join(REPO, "HANDOFFS.md")]
        paths += sorted(p for p in glob.glob(os.path.join(REPO, "docs", "archive", "HANDOFFS*.md")))
        out = []
        for p in paths:
            with open(p, encoding="utf-8") as f:
                rs = cor.parse_receipts(f.read())
            # within one file, newest first; the predecessor is the next block
            out += [(os.path.basename(p), r, rs[i + 1] if i + 1 < len(rs) else {}) for i, r in enumerate(rs)]
        return [x for x in out if x[1].get("status") == "complete"]

    def test_every_complete_receipt_renders_and_lints_clean(self):
        rs = self.receipts()
        self.assertGreaterEqual(len(rs), 100, "the archive should hold well over a hundred complete receipts")
        bad, unscored = [], []
        for fname, r, prev in rs:
            if not (r.get("self_score", "").isdigit() and r.get("predecessor_score", "").isdigit()):
                unscored.append((fname, r.get("session"), r.get("date")))
                continue
            m = cor.facts(r, prev, "abc1234", 0)
            try:
                text = cor.render(m, "d", "done", "w", "b", "p", "n")
            except ValueError as e:
                bad.append(f"{fname} {r.get('session')} {r.get('date')}: {e}")
                continue
            errs = cor.lint(text, m)
            if errs:
                bad.append(f"{fname} {r.get('session')} {r.get('date')}: {errs}")
        self.assertEqual(bad, [], "\n".join(bad[:10]))
        # The first receipt ever written (S1, 2026-07-08) predates predecessor_score. It is the one
        # pinned exception; a second unscored receipt means the ledger stopped recording scores.
        self.assertEqual(unscored, [("HANDOFFS-archive.md", "S1", "2026-07-08")])


if __name__ == "__main__":
    unittest.main()
