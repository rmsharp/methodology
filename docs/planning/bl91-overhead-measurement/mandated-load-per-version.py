#!/usr/bin/env python3
"""BL-91 evidence: the per-session MANDATED READ at every released version.

Run from the repository root. Reads only git; writes nothing.

    python3 docs/planning/bl91-overhead-measurement/mandated-load-per-version.py

What it measures, and why this and not something else: Phase 0 requires reading
SESSION_RUNNER.md and SAFEGUARDS.md IN FULL every session, so their combined size at a
release tag is what that version costs every adopter, every session, before any work.
It is the one overhead component recoverable at every version back to v1.0.0 -- observed
per-session dollars are not, because the transcripts that carry usage begin 2026-08-16,
four days before v3.7, and cover one model and one version.
"""
import re, subprocess

def sh(*a):
    r = subprocess.run(["git"] + list(a), capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None

CAND = {"runner":     ["starter-kit/SESSION_RUNNER.md", "SESSION_RUNNER.md"],
        "safeguards": ["starter-kit/SAFEGUARDS.md", "SAFEGUARDS.md"]}

def size(ref, paths):
    for p in paths:
        out = sh("cat-file", "-s", f"{ref}:{p}")
        if out:
            return int(out.strip())
    return 0

tags = sorted((t for t in sh("tag").split() if re.match(r"^v\d", t)),
              key=lambda t: [int(x) for x in re.findall(r"\d+", t)])
print(f"{'version':>10} {'date':>12} {'runner B':>10} {'safeguards B':>13} {'per-session read B':>19}")
first = last = None
for ref in tags + ["HEAD"]:
    body = sh("show", f"{ref}:{CAND['runner'][0]}") or sh("show", f"{ref}:SESSION_RUNNER.md")
    if not body:
        continue
    r, s = size(ref, CAND["runner"]), size(ref, CAND["safeguards"])
    date = (sh("log", "-1", "--format=%ad", "--date=short", ref) or "?").strip()
    print(f"{ref:>10} {date:>12} {r:>10,} {s:>13,} {r + s:>19,}")
    first = first or (ref, r + s)
    if ref != "HEAD":
        last = (ref, r + s)
print(f"\n{first[0]} -> {last[0]}: {first[1]:,} B -> {last[1]:,} B  ({last[1] / first[1]:.1f}x)")
print("Monotone check across releases is the point: re-derive it, do not trust this line.")
