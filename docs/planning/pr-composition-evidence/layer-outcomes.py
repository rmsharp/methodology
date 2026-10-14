#!/usr/bin/env python3
"""Per-test outcomes of one unittest file, one line per test: `<Class.method> <ok|bad|skip>`, sorted.

    python3 layer-outcomes.py <test-file>            (run it from the checkout whose tool the test file should exercise)

A plain `addFailure` hook misses a test that fails only inside a subtest (layer 3's contrast found one: it reports
`FAILED (errors=2)` run alone and has no outcome of its own), so this runner also records `addSubTest`: a test
with a failing or erroring subtest is `bad`. It loads the file as a module under a fixed name, so two files'
outcomes are comparable by name. It writes no bytecode. Used by `layer4-contrast.sh`.
"""
import contextlib
import importlib.util
import io
import sys
import unittest

sys.dont_write_bytecode = True


class Recorder(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.outcome = {}

    @staticmethod
    def _name(test):
        test = getattr(test, "test_case", test)     # a subtest reports as its parent test, never as a test of its own
        return "%s.%s" % (type(test).__name__, getattr(test, "_testMethodName", str(test)))

    def _mark(self, test, value):
        name = self._name(test)
        if self.outcome.get(name) != "bad":     # bad is sticky: one bad subtest makes the test bad
            self.outcome[name] = value

    def addSuccess(self, test):
        super().addSuccess(test)
        self._mark(test, "ok")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._mark(test, "bad")

    def addError(self, test, err):
        super().addError(test, err)
        self._mark(test, "bad")

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self._mark(test, "skip")

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err is not None:
            self._mark(test, "bad")


def main(path):
    spec = importlib.util.spec_from_file_location("layer_outcomes_target", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    rec = Recorder()
    sink = io.StringIO()    # the tools under test print to stdout in-process; the outcome lines must be the only output
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        unittest.defaultTestLoader.loadTestsFromModule(mod).run(rec)
    for name in sorted(rec.outcome):
        print("%s %s" % (name, rec.outcome[name]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
