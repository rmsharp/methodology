"""Held-out acceptance test for the task (BL-3). Run by the harness AFTER a session, inside the fixture:

    python3 acceptance_test.py FIXTURE_DIR      # exit 0 = pass

Kept outside the fixture so a session cannot read or edit it.
"""
import importlib.util, os, sys, unittest


def load(fixture):
    spec = importlib.util.spec_from_file_location("textkit", os.path.join(fixture, "textkit.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class Accept(unittest.TestCase):
    tk = None

    def test_short_unchanged(self):
        self.assertEqual(self.tk.truncate("abc", 5), "abc")

    def test_exact_length_unchanged(self):
        self.assertEqual(self.tk.truncate("abcde", 5), "abcde")

    def test_long_truncated(self):
        r = self.tk.truncate("abcdefgh", 5)
        self.assertEqual(r, "abcd…")
        self.assertEqual(len(r), 5)

    def test_empty(self):
        self.assertEqual(self.tk.truncate("", 3), "")


def run(fixture):
    Accept.tk = load(fixture)
    with open(os.devnull, "w") as null:
        r = unittest.TextTestRunner(stream=null).run(unittest.defaultTestLoader.loadTestsFromTestCase(Accept))
    return r.wasSuccessful()


if __name__ == "__main__":
    sys.exit(0 if run(sys.argv[1]) else 1)
