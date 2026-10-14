#!/usr/bin/env python3
"""Does a count gate pass over a failing suite, and does a second gate over the SAME command catch it, running it once?

    python3 layer7-pair-proof.py <path-to-quality_ratchet.py>

Imports the ratchet it is given (the candidate's: `git show pr2/candidate:starter-kit/quality_ratchet.py`) and runs its own
run_gates() over two gates that share one command string: a stand-in for a suite that prints `Ran 5 tests` and exits 1
(a suite with a failing test). Prints each gate's reading and how many times the command ran.

Why it matters (layer 7): `measure_gate()` reads a gate with an `extract` from the output and ignores the exit code, so
`migrate-layout-unit-tests` (min 280, `Ran (\\d+) tests`) reads 280 and passes over a suite that FAILED. bin/tests.sh wires in
only two fast classes of that suite, so nothing else carries its colour; the fork tip's `why` says tests-sh-failed does,
which is true of every other suite and not of this one. A second gate with the same `command` and no `extract` measures the
exit code, and the ratchet's per-run memo (keyed by the command string) runs the command once for both, the design of the
tests-sh-passed / tests-sh-failed pair. Expected output:

    suite-count    measured=5.0 status=pass
    suite-failed   measured=1.0 status=fail
    command executions: 1
"""
import importlib.util
import os
import sys
import tempfile

sys.dont_write_bytecode = True


def main():
    spec = importlib.util.spec_from_file_location("qr", sys.argv[1])
    qr = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(qr)
    d = tempfile.mkdtemp()
    counter = os.path.join(d, "runs")
    cmd = '%s -c "open(%r,\'a\').write(\'x\'); print(\'Ran 5 tests\'); raise SystemExit(1)"' % (sys.executable, counter)
    gates = [
        {"name": "suite-count", "direction": "min", "threshold": 5, "command": cmd, "extract": "Ran (\\d+) tests"},
        {"name": "suite-failed", "direction": "max", "threshold": 0, "command": cmd},
    ]
    res = qr.run_gates(d, {"version": 1, "gates": gates}, 60)
    rows = res if isinstance(res, list) else res.get("gates", res)
    for r in rows:
        print("%-14s measured=%s status=%s" % (r["name"], r["measured"], r["status"]))
    print("command executions:", len(open(counter).read()))


if __name__ == "__main__":
    main()
