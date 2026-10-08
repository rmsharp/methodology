#!/usr/bin/env python3
"""BL-101 P8 driver: run bin/migrate-layout's own main() on a scratch clone of THIS repository.

    python3 p8-apply-tool.py <path to the clone's bin/migrate-layout> [the tool's own arguments]

bin/migrate-layout refuses this repository (exit 1, P8's first finding): it is the canonical source, so
`bin/status` reads its distributed files as "missing" at the adopter locations (a root SESSION_RUNNER.md,
docs/methodology/...), and the `[not-current]` precondition ("sync first", plan 5A.2) can never hold; at
--tier 2 `[tier-order]` also fires, because the framework files are not under methodology/. Both
refusals answer a question about an ADOPTER. This driver changes nothing else: it loads the tool from the
clone, makes `read_status` report no rows (so the precondition finds nothing wrong), and runs the tool's
real main(), which plans, rehearses the shards, rewrites, applies as one commit and runs the
before-and-after checks exactly as it does anywhere else. The suppression is announced on stderr.

--tier all is the default and is what the driver is used with: the tier-1 files this repository does not
hold at its root give no moves (none), so the plan is the instance files plus docs/archive/, which is
the plan's B2. Nothing here is distributed or committed to the real repository.
"""
import importlib.machinery
import importlib.util
import sys


def main():
    if len(sys.argv) < 2:
        print("usage: p8-apply-tool.py <bin/migrate-layout> [tool arguments]", file=sys.stderr)
        return 2
    tool = sys.argv[1]
    loader = importlib.machinery.SourceFileLoader("migrate_layout", tool)
    spec = importlib.util.spec_from_loader("migrate_layout", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    mod.read_status = lambda root: ([], "")
    print("p8-apply-tool: read_status suppressed (the not-current precondition is about an adopter); "
          "everything else is the tool as written", file=sys.stderr)
    sys.argv = ["migrate-layout"] + sys.argv[2:]
    return mod.main()


if __name__ == "__main__":
    sys.exit(main())
