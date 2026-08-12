"""Distribution manifest — the single source of truth for what the methodology
ships into an adopter project, where each file lands, and how sync treats it.

Imported by bin/sync, bin/status, and bin/check-links so the mapping is defined
exactly once (B1 plan Decision 5; Ousterhout deepening — the three scripts
previously each carried their own copy of the file list).

Each entry is ``(src, dest, disposition)``:
  * ``src``         path relative to the canonical methodology repo root.
  * ``dest``        path relative to the ADOPTER project root (README Option B
                    layout: starter-kit root-files at the project root, the
                    framework under docs/methodology/). Cross-references inside
                    distributed files are authored for this layout — see
                    bin/check-links and B1 plan section 4 ("link-topology paradox").
  * ``disposition`` how sync reconciles the dest (see below).

Dispositions:
  TRACKED  canonical owns it; sync keeps it current and the existing
           drift / --force / upgrade machinery applies. Overwrites toward
           canonical (never silently clobbering unrecognized local edits).
  SEED     adopter owns it after first creation; sync writes it ONLY when the
           dest is absent and never overwrites it afterward (B1 plan Decision 2a).

Adopter-owned *instances* (CONTEXT.md, CLAUDE.md, BACKLOG.md, …) are deliberately
NOT listed: the template ships under a different name (CONTEXT_TEMPLATE.md →
TRACKED), and the instance simply never appears as a dest, so it can never be a
sync target — no special-case guard needed (B1 plan Decision 2).

Python 3 stdlib only; data-only module (no imports, no side effects).
"""

TRACKED = "tracked"
SEED = "seed"

DISTRIBUTION = [
    # starter-kit root-files -> adopter project root
    ("starter-kit/SESSION_RUNNER.md", "SESSION_RUNNER.md", TRACKED),
    ("starter-kit/FRAMEWORK_LEARNINGS.md", "FRAMEWORK_LEARNINGS.md", TRACKED),
    ("starter-kit/SAFEGUARDS.md", "SAFEGUARDS.md", TRACKED),
    ("starter-kit/RECOMMENDED_SKILLS.md", "RECOMMENDED_SKILLS.md", TRACKED),
    ("starter-kit/CONTEXT_TEMPLATE.md", "CONTEXT_TEMPLATE.md", TRACKED),
    ("starter-kit/CLAUDE_TEMPLATE.md", "CLAUDE_TEMPLATE.md", TRACKED),
    ("starter-kit/BOOTSTRAP.md", "BOOTSTRAP.md", TRACKED),
    ("starter-kit/methodology_dashboard.py", "methodology_dashboard.py", TRACKED),
    # The SECOND executable adopters receive (S39'). Placement is load-bearing, not tidiness:
    # tools/test_methodology_dashboard.py compares the non-markdown dests to the scanner's
    # FRAMEWORK_INSTALLED_SOURCE as an ORDERED tuple (the sibling markdown assertions in the same
    # test are set-compared, and say so), so moving this entry above the dashboard forces that
    # tuple to be rewritten in the same reversed order.
    ("starter-kit/methodology_trim.py", "methodology_trim.py", TRACKED),
    # Arriving via upstream/main's PR #66 (context-budget gate, FM #28) — a third executable,
    # appended after methodology_trim.py so FRAMEWORK_INSTALLED_SOURCE's ordered-tuple comparison
    # (see the comment above) only needs one new tail entry, not a reorder.
    ("starter-kit/context_budget.py", "context_budget.py", TRACKED),
    # seed-once root-files: created if absent, then adopter-owned (never clobbered)
    ("starter-kit/SESSION_NOTES.md", "SESSION_NOTES.md", SEED),
    ("starter-kit/CHANGELOG.md", "CHANGELOG.md", SEED),
    ("starter-kit/HANDOFFS.md", "HANDOFFS.md", SEED),
    ("starter-kit/ROADMAP.md", "ROADMAP.md", SEED),
    ("starter-kit/context-budget.json", ".context-budget.json", SEED),
    # framework docs -> docs/methodology/
    ("ITERATIVE_METHODOLOGY.md", "docs/methodology/ITERATIVE_METHODOLOGY.md", TRACKED),
    ("HOW_TO_USE.md", "docs/methodology/HOW_TO_USE.md", TRACKED),
    # workstreams + campaigns + templates -> docs/methodology/workstreams/
    ("workstreams/DESIGN_WORKSTREAM.md",
     "docs/methodology/workstreams/DESIGN_WORKSTREAM.md", TRACKED),
    ("workstreams/ARCHITECTURE_WORKSTREAM.md",
     "docs/methodology/workstreams/ARCHITECTURE_WORKSTREAM.md", TRACKED),
    ("workstreams/DEVELOPMENT_WORKSTREAM.md",
     "docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md", TRACKED),
    ("workstreams/AUDIT_WORKSTREAM.md",
     "docs/methodology/workstreams/AUDIT_WORKSTREAM.md", TRACKED),
    ("workstreams/RESEARCH_DOCUMENTATION_WORKSTREAM.md",
     "docs/methodology/workstreams/RESEARCH_DOCUMENTATION_WORKSTREAM.md", TRACKED),
    ("workstreams/TEMPLATE_WORKSTREAM.md",
     "docs/methodology/workstreams/TEMPLATE_WORKSTREAM.md", TRACKED),
    ("workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_CAMPAIGN.md",
     "docs/methodology/workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_CAMPAIGN.md", TRACKED),
    ("workstreams/INHERITED_CODEBASE_FAMILIARIZATION_CAMPAIGN.md",
     "docs/methodology/workstreams/INHERITED_CODEBASE_FAMILIARIZATION_CAMPAIGN.md", TRACKED),
    ("workstreams/TEMPLATE_CAMPAIGN.md",
     "docs/methodology/workstreams/TEMPLATE_CAMPAIGN.md", TRACKED),
]

# Optional "current-format" markers for SEED dests, keyed by adopter-relative dest path.
#
# A SEED is adopter-owned and never overwritten (Decision 2a), so an adopter upgrading from a
# pre-v3.1 methodology keeps its OLD-shaped seed: it gains the new behavior (the synced
# SESSION_RUNNER.md's FM #27 + Phase 0 reconcile) but silently misses the new seed FORMAT. When a
# seed listed here is PRESENT but its content lacks the marker string, bin/status reports it
# advisory-only as "present (stale format)" so the migration is DISCOVERABLE. sync still never
# auto-overwrites it — reconcile manually or delete-and-reseed (BOOTSTRAP.md "Updating an existing
# project…"; BL-6 item 2).
#
# A marker must satisfy TWO properties, and the pair is the whole design. Missing either one makes
# the check useless in a different direction:
#   1. LIFETIME-STABLE — surviving everything an adopter legitimately does to the file, or it
#      mis-flags a current-format seed. This rules out the METHODOLOGY-SEED-SENTINEL, which the
#      adopter deletes on its first real entry.
#   2. VERSION-DISCRIMINATING — absent from the formats it must detect as stale, or it can never
#      fire at all.
#
# Both markers keyed on the seeds' H1 TITLES until 2026-08-04, which satisfied (1) and silently
# failed (2): the titles are precisely what did NOT change when the seed format did. S40 added the
# `## Size, and when to archive` doctrine to both ledger seeds; every existing adopter kept a seed
# without it and still reported `present` — "current" — because the title was still there. That
# falsified BOOTSTRAP.md's own written promise that status "flags any seed whose format predates
# the current methodology ... so the format lag is surfaced rather than silent." Measured at the
# time: 11 sibling projects held CHANGELOG.md, 9 held HANDOFFS.md, and none held the doctrine.
#
# The doctrine heading satisfies both. It lives in the front-matter zone, which methodology_trim.py
# PINS and never archives, so it survives every trim, every prepend and every close-out (1); and it
# arrived with a known format version, so its absence dates the file (2).
#
# CONSEQUENCE, stated because it is a real cost: a version-discriminating marker has to MOVE when
# the seed format materially changes again. That is the mechanism working, not drift — a marker that
# never needs updating is a marker that can never fire. Move it, and drive the RED case in
# bin/tests.sh Test 20 (b2) before trusting the green.
#
# SESSION_NOTES.md is deliberately omitted: it is rewritten wholesale every session, so no token is
# stable enough to detect its format without false positives. ROADMAP.md likewise carries no
# format contract worth asserting. Add an entry here only when a seed gains a marker meeting both
# properties above.
SEED_FORMAT_MARKERS = {
    "CHANGELOG.md": "Size, and when to archive",
    "HANDOFFS.md": "Size, and when to archive",
}
