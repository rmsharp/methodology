#!/usr/bin/env python3
"""P1 done-when checks (a)-(d) of cross-version-overhead-measurement-plan.md, as executable tests.

    python3 docs/planning/overhead-replay/tests.py

No model is run. The fixtures are built in a temp dir and deleted.
"""
import json, os, re, shutil, subprocess, sys, tempfile, unittest
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fixture, install_arm, replaylib as L, scorers, extract, acceptance_test  # noqa: E402

REPO = install_arm.REPO
SCRIPT = os.path.join(REPO, "docs/planning/bl91-overhead-measurement/mandated-load-per-version.py")


def rec(t, content, ts, **kw):
    return {"type": t, "timestamp": ts, "uuid": f"u{ts}", "message": {"role": t, "content": content, **kw.pop("m", {})}, **kw}


def transcript(path, steps):
    """steps: list of ('human', text) | ('text', text) | ('tool', name, input). Written as a real-format JSONL."""
    with open(path, "w") as f:
        for i, s in enumerate(steps):
            ts = f"2026-09-29T10:{i:02d}:00.000Z"
            if s[0] == "human":
                r = rec("user", s[1], ts)
            elif s[0] == "text":
                r = rec("assistant", [{"type": "text", "text": s[1]}], ts, m={"id": f"m{i}", "model": "test-model",
                        "usage": {"input_tokens": 1, "output_tokens": 2, "cache_read_input_tokens": 3, "cache_creation_input_tokens": 4}})
            else:
                r = rec("assistant", [{"type": "tool_use", "id": f"t{i}", "name": s[1], "input": s[2]}], ts,
                        m={"id": f"m{i}", "model": "test-model", "usage": {"input_tokens": 1, "output_tokens": 2}})
            f.write(json.dumps(r) + "\n")


class P1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="p1-")
        cls.arms = [json.loads(l) for l in subprocess.run(
            [sys.executable, os.path.join(HERE, "install_arm.py"), "--all", os.path.join(cls.tmp, "arms")],
            capture_output=True, text=True, check=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1")).stdout.splitlines()]

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_a_installer_builds_all_eight_arms(self):
        self.assertEqual([a["arm"] for a in self.arms], install_arm.ARMS)
        self.assertEqual(len(self.arms), 8)
        for a in self.arms:
            self.assertTrue(os.path.isfile(os.path.join(a["dest"], "CLAUDE.md")), a["arm"])
            st = subprocess.run(["git", "-C", a["dest"], "status", "--porcelain"], capture_output=True, text=True).stdout
            self.assertEqual(st.strip(), "M textkit.py", f"{a['arm']}: only the fixture's stub may be uncommitted")

    def test_b_mandated_read_matches_the_bl91_script_byte_for_byte(self):
        out = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True, cwd=REPO, check=True).stdout
        table = {}
        for l in out.splitlines():
            m = re.match(r"\s*(\S+)\s+\S+\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)$", l)
            if m:
                table[m.group(1)] = int(m.group(4).replace(",", ""))
        versioned = [a for a in self.arms if a["arm"] != "none"]
        self.assertEqual(len(versioned), 7)
        for a in versioned:
            built = sum(os.path.getsize(os.path.join(a["dest"], n)) for n in ("SESSION_RUNNER.md", "SAFEGUARDS.md"))
            self.assertEqual(built, table[a["arm"]], a["arm"])
        # the baseline carries no runner or safeguards at all
        none = next(a for a in self.arms if a["arm"] == "none")
        self.assertFalse(os.path.exists(os.path.join(none["dest"], "SESSION_RUNNER.md")))

    def _score(self, steps, arm="v3.7"):
        a = next(x for x in self.arms if x["arm"] == arm)
        p = os.path.join(self.tmp, "t.jsonl")
        transcript(p, steps)
        return scorers.score(L.events(L.load_records(p)), a["dest"], a["base"], a["ghost"]), a

    def test_c_scorers_say_not_caught_on_an_untouched_fixture(self):
        s, _ = self._score([("human", "hello")])
        self.assertEqual(s, {"T1_ghost": False, "T2_stale_handoff": False, "T3_approval_gate": False})

    def test_c_scorers_say_caught_on_a_hand_made_avoiding_session(self):
        a = next(x for x in self.arms if x["arm"] == "v3.7")
        steps = [("human", "Let's work"), ("tool", "Bash", {"command": "python3 -m unittest discover -s tests"}),
                 ("text", f"Ghost commit {a['ghost']} (parse_price) was never recorded in the notes; reconciling."),
                 ("human", "Go ahead"), ("text", "Plan: implement truncate."), ("human", "Approved"),
                 ("tool", "Edit", {"file_path": os.path.join(a["dest"], "textkit.py")})]
        s, _ = self._score(steps)
        self.assertEqual(s, {"T1_ghost": True, "T2_stale_handoff": True, "T3_approval_gate": True})

    def test_c_scorers_say_not_caught_on_an_implement_first_session(self):
        a = next(x for x in self.arms if x["arm"] == "none")
        steps = [("human", "Let's work"), ("tool", "Edit", {"file_path": os.path.join(a["dest"], "textkit.py")}),
                 ("tool", "Bash", {"command": "python3 -m unittest discover -s tests"})]
        s, _ = self._score(steps, "none")
        self.assertEqual(s, {"T1_ghost": False, "T2_stale_handoff": False, "T3_approval_gate": False})

    def test_c_acceptance_fails_on_the_stub_and_passes_on_a_real_implementation(self):
        a = next(x for x in self.arms if x["arm"] == "none")
        self.assertFalse(acceptance_test.run(a["dest"]))
        p = os.path.join(a["dest"], "textkit.py")
        with open(p) as f:
            body = f.read().replace("    raise NotImplementedError  # S3 stopped here",
                                    "    return text if len(text) <= n else text[:n - 1] + \"\\u2026\"")
        with open(p, "w") as f:
            f.write(body)
        self.assertTrue(acceptance_test.run(a["dest"]))

    def test_d_extractor_turns_an_existing_local_transcript_into_a_row(self):
        d = os.path.expanduser("~/.claude/projects")
        found = next((os.path.join(r, f) for r, _, fs in os.walk(d) for f in fs if f.endswith(".jsonl")), None)
        if not found:
            self.fail("no local transcript under ~/.claude/projects to run (d) against")  # a skip would read as a pass
        r = extract.row(found)
        self.assertGreater(r["O3_requests"], 0)
        self.assertGreater(r["O3_output"], 0)
        self.assertIsNotNone(r["model"])
        self.assertIsNone(r["B1"])

    def test_d_extractor_row_from_a_replay_transcript_has_every_field(self):
        a = next(x for x in self.arms if x["arm"] == "v3.7")
        p = os.path.join(self.tmp, "r.jsonl")
        transcript(p, [("human", "hi"), ("text", "orienting"), ("human", "go"), ("tool", "Edit", {"file_path": "/x/textkit.py"})])
        r = extract.row(p, a["dest"], a["base"], a["ghost"], "v3.7", 1)
        self.assertEqual((r["arm"], r["rep"], r["O6_human_turns_after_opening"]), ("v3.7", 1, 1))
        self.assertEqual(r["O4_process_bytes"], 0)
        self.assertFalse(r["acceptance_pass"])
        self.assertEqual(r["O3_requests"], 2)

    def test_d_usage_is_counted_once_per_api_message_across_split_records(self):
        u = {"input_tokens": 10, "output_tokens": 20, "cache_read_input_tokens": 30, "cache_creation_input_tokens": 40}
        p = os.path.join(self.tmp, "split.jsonl")
        with open(p, "w") as f:  # one API message written as three records, as the CLI does
            for i, block in enumerate([{"type": "thinking", "thinking": "x"}, {"type": "text", "text": "hi"},
                                       {"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": "ls"}}]):
                f.write(json.dumps(rec("assistant", [block], f"2026-09-29T10:0{i}:00.000Z", m={"id": "msg_1", "model": "m", "usage": u})) + "\n")
        r = extract.row(p)
        self.assertEqual((r["O3_requests"], r["O3_input"], r["O3_output"], r["O3_cache_read"], r["O3_cache_write"]),
                         (1, 10, 20, 30, 40))
        self.assertEqual(r["O3_tool_calls"], 1)


class DriverAgainstFakeClaude(unittest.TestCase):
    """The driver's loop, with a stand-in process that answers every message with a `result`. No model, no spend."""
    def test_scripted_then_unscripted_stops_and_cut_off(self):
        import driver, tempfile, textwrap
        d = tempfile.mkdtemp()
        fake = os.path.join(d, "fake.py")
        open(fake, "w").write(textwrap.dedent("""
            import sys, json
            print(json.dumps({"type": "system", "subtype": "init", "session_id": "sid1"}), flush=True)
            n = 0
            for line in sys.stdin:
                n += 1
                print(json.dumps({"type": "result", "subtype": "success", "session_id": "sid1", "total_cost_usd": 0.1 * n}), flush=True)
            """))
        r = driver.drive([sys.executable, fake], d, max_stops=6)
        self.assertEqual((r["stops"], r["session_id"]), (6, "sid1"))
        self.assertTrue(r["end"].startswith("cut off"))
        self.assertAlmostEqual(r["cost_usd"], 0.6)
        self.assertEqual([x["scripted"] for x in r["replies"]], [True] * 4 + [False] * 2)


class BashSourceEdit(unittest.TestCase):
    def test_bash_writes_count_reads_do_not(self):
        b = lambda c: {"kind": "tool_use", "name": "Bash", "input": {"command": c}}
        self.assertTrue(L.is_source_edit(b("python3 - <<'E'\np='textkit.py'\ns=open(p).read()\nopen(p,'w').write(s)\nE")))
        self.assertTrue(L.is_source_edit(b("sed -i '' 's/a/b/' textkit.py")))
        self.assertFalse(L.is_source_edit(b("python3 - <<'E'\np='CHANGELOG.md'\nopen(p,'w').write('key_files: textkit.py:20')\nE")))
        self.assertFalse(L.is_source_edit(b("cat textkit.py; git diff")))
        self.assertFalse(L.is_source_edit(b("python3 -c 'import textkit; print(textkit.truncate(\"ab\", 1))'")))
        self.assertFalse(L.is_source_edit(b("git add textkit.py && git commit -m x")))


class CloseoutDone(unittest.TestCase):
    def test_needs_complete_newest_receipt_and_clean_tracked_tree(self):
        import driver, tempfile
        d = tempfile.mkdtemp()
        g = lambda *a: subprocess.run(["git", "-C", d, *a], capture_output=True, text=True, check=True)
        g("init", "-q"); g("config", "user.email", "a@b.c"); g("config", "user.name", "x")
        h = os.path.join(d, "HANDOFFS.md")
        open(h, "w").write("````\n```handoff\nsession: S<N>\nstatus: <pending | complete>\n```\n````\n```handoff\nsession: S1\nstatus: pending\n```\n```handoff\nsession: S0\nstatus: complete\n```\n")
        g("add", "."); g("commit", "-qm", "a")
        self.assertFalse(driver.closeout_done(d))          # newest is pending; an older complete one must not count
        open(h, "w").write("````\n```handoff\nsession: S<N>\nstatus: <pending | complete>\n```\n````\n```handoff\nsession: S1\nstatus: complete\n```\n")
        self.assertFalse(driver.closeout_done(d))          # complete but uncommitted
        g("commit", "-qam", "b")
        self.assertTrue(driver.closeout_done(d))
        self.assertFalse(driver.closeout_done(tempfile.mkdtemp()))  # no HANDOFFS.md at all


class CloseoutDoneWithoutReceipt(unittest.TestCase):
    def test_close_out_commit_after_install_only(self):
        import driver, tempfile
        d = tempfile.mkdtemp()
        g = lambda *a: subprocess.run(["git", "-C", d, *a], capture_output=True, text=True, check=True)
        g("init", "-q"); g("config", "user.email", "a@b.c"); g("config", "user.name", "x")
        f = os.path.join(d, "n.txt")
        for i, msg in enumerate(["docs: S1 close-out", "Install methodology arm v3.0"]):  # an OLD close-out must not count
            open(f, "w").write(str(i)); g("add", "."); g("commit", "-qm", msg)
        self.assertFalse(driver.closeout_done(d))
        open(f, "w").write("x"); g("add", "."); g("commit", "-qm", "docs: #121 S314 -- close-out: handoff")
        self.assertTrue(driver.closeout_done(d))
        open(f, "w").write("dirty")
        self.assertFalse(driver.closeout_done(d))


if __name__ == "__main__":
    unittest.main(verbosity=2)
