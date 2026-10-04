"""Tests for doc_evidence.py (plan section 5 P1a (a)). Synthetic repositories only: no run tree, no model. Every check that guards
the evidence is seen failing on a corrupted copy, because a verifier that cannot refuse proves nothing.

    python3 docs/planning/overhead-replay/tests_doc_evidence.py
"""
import json, os, shutil, sys, tempfile, unittest
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doc_evidence as D
from tests_ratchet import sh, write, commit, ENV


def make_project():
    p = tempfile.mkdtemp(prefix="evproj-")
    sh(p, "init", "-q", "-b", "master")
    write(p, "a.txt", "one\n")
    first = commit(p, "start")
    return p, first


def make_tree(project, install_author="Fixture", subjects=("claim", "work", "close-out")):
    t = tempfile.mkdtemp(prefix="evtree-")
    shutil.rmtree(t)
    sh(project, "clone", "-q", "--no-local", project, t)
    env = dict(ENV, GIT_AUTHOR_NAME=install_author, GIT_COMMITTER_NAME=install_author)
    write(t, "framework.md", "x\n")
    sh(t, "add", "-A")
    import subprocess
    subprocess.run(["git", "-C", t, "commit", "-q", "--no-verify", "-m", "Install methodology arm v9"], env=env, check=True)
    shas = []
    for i, s in enumerate(subjects):
        write(t, f"f{i}.txt", s)
        shas.append(commit(t, s))
    return t, shas


def run_for(tree, start, rid="t/x-r1", transcript=""):
    return {"id": rid, "set": "t", "arm": "x", "rep": "1", "start": start, "tree": tree, "transcript": transcript,
            "row_end": None, "row_complete": None}


class RoundTrip(unittest.TestCase):
    def setUp(self):
        self.project, self.start = make_project()
        self.tree, self.shas = make_tree(self.project)
        self.out = tempfile.mkdtemp(prefix="evout-")
        self.m = D.build(self.out, self.project, [run_for(self.tree, self.start)])

    def test_manifest_records_head_pin_install_and_count(self):
        r = self.m["runs"][0]
        self.assertEqual(r["head"], self.shas[-1])
        self.assertEqual((r["pin"], r["pin_rule"]), (self.shas[-1], "head"))
        self.assertEqual(r["commits_after_start"], 4)
        self.assertEqual(D.git(self.tree, "log", "-1", "--format=%s", r["install"]), "Install methodology arm v9")
        self.assertNotIn("tree", r)                      # the perishable path is kept only as tree_was
        self.assertEqual(self.m["bundle"]["prerequisites"], [self.start])

    def test_manifest_names_what_a_bundle_cannot_carry(self):
        self.assertEqual((self.m["runs"][0]["uncommitted_tracked"], self.m["runs"][0]["untracked"]), ([], []))
        write(self.tree, "f0.txt", "edited and not committed")
        write(self.tree, "scratch.log", "untracked")
        m = D.build(self.out, self.project, [run_for(self.tree, self.start)])
        self.assertEqual((m["runs"][0]["uncommitted_tracked"], m["runs"][0]["untracked"]), (["f0.txt"], ["scratch.log"]))

    def test_verify_passes_on_the_untouched_bundle(self):
        self.assertEqual(D.verify(self.out, self.project), ["t/x-r1"])

    def test_a_relative_output_directory_is_resolved_against_the_callers_directory(self):
        here = os.getcwd()
        parent = tempfile.mkdtemp(prefix="evrel-")
        os.chdir(parent)
        try:
            D.build("rel/out", self.project, [run_for(self.tree, self.start)])
            self.assertTrue(os.path.isfile(os.path.join(parent, "rel", "out", "runs.bundle")))
            self.assertEqual(D.verify("rel/out", self.project), ["t/x-r1"])
        finally:
            os.chdir(here)

    def test_verify_refuses_a_changed_bundle(self):
        with open(os.path.join(self.out, "runs.bundle"), "ab") as f:
            f.write(b"x")
        with self.assertRaises(SystemExit) as c:
            D.verify(self.out, self.project)
        self.assertIn("sha256", str(c.exception))

    def test_verify_refuses_a_manifest_naming_another_head(self):
        mp = os.path.join(self.out, "manifest.json")
        m = json.load(open(mp))
        m["runs"][0]["head"] = self.shas[0]
        json.dump(m, open(mp, "w"))
        with self.assertRaises(SystemExit) as c:
            D.verify(self.out, self.project)
        self.assertIn("rebuilt head", str(c.exception))

    def test_verify_refuses_when_the_project_lacks_the_prerequisite(self):
        other = tempfile.mkdtemp(prefix="evother-")        # shas are deterministic here, so the content must differ
        sh(other, "init", "-q", "-b", "master")
        write(other, "b.txt", "two\n")
        commit(other, "different history")
        self.assertNotEqual(D.git(other, "rev-parse", "HEAD"), self.start)
        with self.assertRaises(SystemExit) as c:
            D.verify(self.out, other)
        self.assertIn("bundle verify", str(c.exception))

    def test_a_pin_before_head_is_kept_and_rebuilt(self):
        D.PIN_OVERRIDES["t/x-r1"] = self.shas[0][:8]
        try:
            m = D.build(self.out, self.project, [run_for(self.tree, self.start)])
        finally:
            del D.PIN_OVERRIDES["t/x-r1"]
        r = m["runs"][0]
        self.assertEqual((r["pin"], r["pin_rule"]), (self.shas[0], "override"))
        self.assertEqual(D.verify(self.out, self.project), ["t/x-r1"])

    def test_a_pin_that_is_not_an_ancestor_is_refused(self):
        sh(self.tree, "checkout", "-q", "-b", "side", self.start)        # a commit that exists in the tree but is not under HEAD
        write(self.tree, "side.txt", "side\n")
        side = commit(self.tree, "side")
        sh(self.tree, "checkout", "-q", "master")
        D.PIN_OVERRIDES["t/x-r1"] = side
        try:
            with self.assertRaises(SystemExit) as c:
                D.build(self.out, self.project, [run_for(self.tree, self.start)])
        finally:
            del D.PIN_OVERRIDES["t/x-r1"]
        self.assertIn("not an ancestor of HEAD", str(c.exception))

    def test_a_tree_that_is_gone_is_a_stop_not_a_skip(self):
        shutil.rmtree(self.tree)
        with self.assertRaises(SystemExit) as c:
            D.build(self.out, self.project, [run_for(self.tree, self.start)])
        self.assertIn("tree missing", str(c.exception))


class Helpers(unittest.TestCase):
    def test_install_commit_needs_the_fixture_author(self):
        project, start = make_project()
        tree, shas = make_tree(project, install_author="Someone Else")
        self.assertIsNone(D.install_commit(tree, start))
        tree2, _ = make_tree(project)
        self.assertEqual(D.git(tree2, "log", "-1", "--format=%s", D.install_commit(tree2, start)), "Install methodology arm v9")

    def test_cli_versions_in_order_without_repeats(self):
        f = tempfile.mktemp(suffix=".jsonl")
        with open(f, "w") as h:
            h.write('{"version":"2.1.285","x":1}\n{"version":"2.1.286"}\nnot json at all\n{"version":"2.1.285"}\n{"nothing":1}\n')
        self.assertEqual(D.cli_versions(f), ["2.1.285", "2.1.286"])
        self.assertEqual(D.cli_versions("/no/such/file"), [])

    def test_the_three_pin_overrides_name_real_runs(self):
        ids = {r["id"] for r in D.runs()}
        self.assertEqual(len(ids), 41)
        for rid in D.PIN_OVERRIDES:
            self.assertIn(rid, ids)

    def test_run_ids_are_unique_and_cover_the_four_sets(self):
        rs = D.runs()
        self.assertEqual(len({r["id"] for r in rs}), len(rs))
        self.assertEqual({r["set"] for r in rs}, {"real-3.7", "t-control", "t-control-fix", "t-remove"})
        self.assertEqual([sum(1 for r in rs if r["set"] == s) for s in ("real-3.7", "t-control", "t-control-fix", "t-remove")], [13, 8, 5, 15])


if __name__ == "__main__":
    unittest.main()
