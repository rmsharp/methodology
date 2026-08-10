#!/usr/bin/env python3
"""Functional tests for starter-kit/methodology_trim.py — the ledger trimmer.

CANONICAL-ONLY. Not in bin/_manifest.py, so adopters do not receive it.

DISCIPLINE THIS FILE IS WRITTEN UNDER (design §11 Phase 1, and this repo's own learnings):

  * PROVE THE FIXTURE FIRST. A test green for a year can assert nothing about its stated case if
    its fixture was never that artifact. Every fixture here has an unmutated control that asserts
    what the fixture IS before anything is asserted about what the code does to it.
  * DRIVE EACH GUARD RED AND WATCH IT FAIL. Green is not evidence until red has been observed.
  * NARROW THE GUARD, DO NOT ONLY DELETE IT. Deleting a guard proves only that it runs. Each
    assertion below also has a NARROWED variant — the plausible weaker implementation — shown to
    PASS the case the full-strength guard catches. That is what makes the strong clause load-bearing.
  * ASSERT ON NAMED FINDINGS, NEVER ON THE EXIT CODE. The exit code is a union over every check
    the tool runs, so adding a check silently re-labels unrelated assertions (design §6.3).

TWO FIXTURES ARE REAL HISTORY, NOT INVENTED — both events happened in this repository:
  L2  `020ba3f^:CHANGELOG.md` — the last tree in which the root ledger still had its pre-v3.0
      scope footer. The commit that archived from it lost that footer, and it is still missing.
  L3  `7a71df0` — the archive that moved 19 receipts AND rewrote the RETAINED S22 receipt in the
      same commit, making "the move was verbatim" unfalsifiable.
"""

import importlib.util
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True          # no starter-kit/__pycache__ from this import

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
TRIM_PY = REPO / "starter-kit" / "methodology_trim.py"

_spec = importlib.util.spec_from_file_location("methodology_trim", str(TRIM_PY))
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)


def show(ref):
    p = subprocess.run(["git", "-C", str(REPO), "show", ref], stdout=subprocess.PIPE,
                       stderr=subprocess.DEVNULL)
    return None if p.returncode else p.stdout.decode("utf-8")


def records_of(text, spec):
    z = mod.classify_zones(text, spec, mod.Result("x"))
    return z.records() if z else []


# The token the two shipped seeds carry until first real use. The TOOL no longer reads it — an
# exemption keyed on it left one shape of F1 uncovered — see the 120-entry sealed-table-row test
# below — so this is
# purely a fixture token here, used to build files that DO carry the marker and must be judged on
# their contents anyway.
SEED_SENTINEL_TOKEN = "METHODOLOGY-SEED-SENTINEL"


def mod_seed_sentinel():
    return SEED_SENTINEL_TOKEN


def negations_of(text, spec):
    """Fence-aware count for the spec's seed negation. 0 when none is declared."""
    if spec.seed_negation is None:
        return 0
    return sum(1 for i, s, inside, _ in mod.fence_scan(text.splitlines())
               if not inside and spec.seed_negation.match(s))


def probe_hits_of(text, spec):
    """[(1-based line, line)] for the spec's content probe, fence-aware. [] when none declared.

    Reimplemented here rather than called through the module: an assertion computed by the same
    code it is testing cannot fail. This walks the module's fence_scan — the shared primitive the
    production path also uses — but applies the predicate itself.
    """
    if spec.content_probe is None:
        return []
    out = []
    for i, s, inside, _info in mod.fence_scan(text.splitlines()):
        if not inside and spec.content_probe.search(s):
            out.append((i + 1, s))
    return out


CL = mod.LEDGERS["CHANGELOG.md"]
HF = mod.LEDGERS["HANDOFFS.md"]


# =============================================================================================
# Controls — prove the fixtures before asserting anything about the code.
# =============================================================================================

class TestFixtureControls(unittest.TestCase):

    def test_L2_fixture_is_the_tree_that_still_had_the_footer(self):
        text = show("020ba3f^:CHANGELOG.md")
        self.assertIsNotNone(text, "fixture commit 020ba3f^ is unreachable — history changed")
        z = mod.classify_zones(text, CL, mod.Result("x"))
        self.assertEqual(len(z.starts), 27, "fixture must hold 27 records")
        self.assertIn("Release history before v3.0", z.footer,
                      "the L2 fixture is only a fixture if the footer is actually IN it")
        self.assertGreater(len(z.footer.encode("utf-8")), 300)

    def test_L2_fixture_loss_actually_happened_and_is_still_unrepaired(self):
        """The defect this assertion exists to prevent is live, not historical.

        Asserted over the FOOTER ZONE, not over the whole file — deliberately. The design's own D1
        command is `grep -rn 'Release history before v3.0' CHANGELOG.md docs/archive/`, and that
        command now returns a FALSE POSITIVE: S35's close-out entry quotes the phrase inside a dated
        record while the footer itself is still gone. A whole-file grep can no longer tell "the
        footer is present" from "something talks about the footer". Zones can.
        """
        after = show("020ba3f:CHANGELOG.md")
        head = show("HEAD:CHANGELOG.md")
        shard = show("020ba3f:docs/archive/CHANGELOG-through-2026-08-01.md")
        za = mod.classify_zones(after, CL, mod.Result("x"))
        zh = mod.classify_zones(head, CL, mod.Result("x"))
        zs = mod.classify_zones(shard, CL, mod.Result("x"))
        self.assertNotIn("Release history before v3.0", za.footer, "the footer left the live file")
        self.assertNotIn("Release history before v3.0", zh.footer, "and it has never come back")
        self.assertIn("Release history before v3.0", zs.footer, "it is now the SHARD's footer")
        # The control matches the design's own D1 scope (`CHANGELOG.md docs/archive/`), not the
        # live file alone: S35's quoting entry migrates by position on every later trim just like
        # any other record (Learning #15), and did — a S63 archive moved it out of the live file
        # into docs/archive/CHANGELOG-through-2026-08-09.md. The whole-CORPUS grep stays ambiguous
        # even after it moves; only the live file's grep would stop being.
        archive_dir = REPO / "docs" / "archive"
        corpus = head + "".join(
            show(f"HEAD:{p.relative_to(REPO).as_posix()}") or ""
            for p in sorted(archive_dir.glob("CHANGELOG-*.md"))
        )
        self.assertIn("Release history before v3.0", corpus,
                      "control: the phrase IS in the live corpus (live file or an archive "
                      "shard), just not as any shard's footer")

    def test_L3_fixture_is_the_event_that_bundled_an_edit_with_the_move(self):
        before = show("7a71df0^:HANDOFFS.md")
        after = show("7a71df0:HANDOFFS.md")
        shard = show("7a71df0:docs/archive/HANDOFFS-archive.md")
        self.assertIsNotNone(before, "fixture commit 7a71df0 is unreachable — history changed")
        b, a, s = (records_of(t, HF) for t in (before, after, shard))
        self.assertEqual((len(b), len(a), len(s)), (25, 6, 19),
                         "fixture must be the 25 = 6 + 19 partition the design describes")
        # The control that makes this a fixture: the counts DO partition, so any failure below is
        # about record BYTES, not about a miscount.
        self.assertEqual(len(a) + len(s), len(b))

    def test_seed_files_hold_zero_records_under_the_declared_grammar(self):
        """Fence-awareness control. Both seeds contain record-shaped lines that are NOT records."""
        cl_seed = (REPO / "starter-kit" / "CHANGELOG.md").read_text(encoding="utf-8")
        hf_seed = (REPO / "starter-kit" / "HANDOFFS.md").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"(?m)^### 20", cl_seed)), 3,
                         "the seed must still contain the fenced examples this guards against")
        self.assertEqual(len(re.findall(r"(?m)^```handoff", hf_seed)), 1)
        self.assertEqual(records_of(cl_seed, CL), [], "a freshly seeded ledger has no records")
        self.assertEqual(records_of(hf_seed, HF), [], "a freshly seeded ledger has no records")

    def test_a_fence_blind_scan_would_have_trimmed_the_seed(self):
        """NARROWED: drop fence-awareness and the day-one hazard reappears."""
        cl_seed = (REPO / "starter-kit" / "CHANGELOG.md").read_text(encoding="utf-8")
        naive = [ln for ln in cl_seed.splitlines() if CL.record_start.match(ln)]
        self.assertEqual(len(naive), 3,
                         "a fence-blind scanner finds 3 'records' in a file that has none")


# =============================================================================================
# L1 — records-zone concatenation identity
# =============================================================================================

class TestL1(unittest.TestCase):

    def setUp(self):
        self.before = [ "### 2026-01-0%d · [ad hoc] r%d\n\nbody %d\n\n" % (i, i, i)
                        for i in range(1, 6) ]

    def test_green_on_a_clean_partition(self):
        r = mod.Result("x")
        ok = mod.assert_L1(self.before, self.before[:2],
                           [mod.transform_record(x) for x in self.before[2:]], r)
        self.assertTrue(ok)
        self.assertNotIn("L1_MISMATCH", r.codes)

    def test_red_when_a_record_is_dropped(self):
        r = mod.Result("x")
        ok = mod.assert_L1(self.before, self.before[:2],
                           [mod.transform_record(x) for x in self.before[3:]], r)
        self.assertFalse(ok)
        self.assertIn("L1_MISMATCH", r.codes)

    def test_red_when_a_record_is_duplicated(self):
        r = mod.Result("x")
        dup = self.before[2:] + [self.before[4]]
        ok = mod.assert_L1(self.before, self.before[:2], [mod.transform_record(x) for x in dup], r)
        self.assertFalse(ok)
        self.assertIn("L1_MISMATCH", r.codes)

    def test_red_on_the_operand_order_the_design_specifies(self):
        """The ratified §4.2 formula puts the shard FIRST. These ledgers are newest-on-top, so that
        order is wrong — and it fails with the CORRECT TOTAL LENGTH, which is why the mutation below
        matters. This is the defect the first build of this tool shipped and L1 caught."""
        swapped = "".join(mod.invert_record(mod.transform_record(x)) for x in self.before[2:]) \
                  + "".join(self.before[:2])
        original = "".join(self.before)
        self.assertEqual(len(swapped), len(original), "the swap conserves length — that is the trap")
        self.assertNotEqual(swapped, original)

    def test_NARROWED_length_only_L1_passes_the_operand_swap(self):
        """A plausible weaker L1 — compare byte LENGTH — is green on the real defect above."""
        swapped = "".join(self.before[2:]) + "".join(self.before[:2])
        original = "".join(self.before)
        self.assertEqual(len(swapped), len(original))      # narrowed guard: PASSES
        r = mod.Result("x")                                # full-strength guard: REFUSES
        mod.assert_L1(self.before, self.before[2:], [mod.transform_record(x) for x in self.before[:2]], r)
        self.assertIn("L1_MISMATCH", r.codes)

    def test_red_on_the_real_7a71df0_event(self):
        b = records_of(show("7a71df0^:HANDOFFS.md"), HF)
        a = records_of(show("7a71df0:HANDOFFS.md"), HF)
        s = records_of(show("7a71df0:docs/archive/HANDOFFS-archive.md"), HF)
        r = mod.Result("x")
        self.assertFalse(mod.assert_L1(b, a, [mod.transform_record(x) for x in s], r))
        self.assertIn("L1_MISMATCH", r.codes)


# =============================================================================================
# L2 — zone pinning. The assertion whose absence cost a paragraph.
# =============================================================================================

class TestL2(unittest.TestCase):

    def setUp(self):
        self.text = show("020ba3f^:CHANGELOG.md")
        self.z = mod.classify_zones(self.text, CL, mod.Result("x"))

    def test_green_when_the_footer_stays_live_and_out_of_the_shard(self):
        r = mod.Result("x")
        ok = mod.assert_L2(self.z, self.z.front + "PTR\n", self.z.footer,
                           "shard body with no footer", ["PTR\n"], [], r)
        self.assertTrue(ok, [f.message for f in r.findings])

    def test_red_when_the_footer_migrates_into_the_shard(self):
        """The `020ba3f` loss, reproduced: footer gone from live, present in the shard."""
        r = mod.Result("x")
        ok = mod.assert_L2(self.z, self.z.front + "PTR\n", "",
                           "shard body\n" + self.z.footer, ["PTR\n"], [], r)
        self.assertFalse(ok)
        self.assertIn("L2_FOOTER_ALTERED", r.codes)
        self.assertIn("L2_FOOTER_MOVED", r.codes)

    def test_red_when_the_footer_is_DUPLICATED_into_the_shard(self):
        """Isolates the 'absent from the shard' clause: live keeps it, the shard also gets it. The
        footer-identical clause alone is green here."""
        r = mod.Result("x")
        ok = mod.assert_L2(self.z, self.z.front + "PTR\n", self.z.footer,
                           "shard body\n" + self.z.footer, ["PTR\n"], [], r)
        self.assertFalse(ok)
        self.assertIn("L2_FOOTER_MOVED", r.codes)
        self.assertNotIn("L2_FOOTER_ALTERED", r.codes)

    def test_NARROWED_footer_identical_only_passes_the_duplication(self):
        """The plausible weaker L2 — 'is the footer still in the live file?' — is green while the
        same bytes have ALSO been frozen into a shard that must never carry them."""
        self.assertEqual(self.z.footer, self.z.footer)            # narrowed guard: PASSES
        r = mod.Result("x")                                       # full-strength guard: REFUSES
        mod.assert_L2(self.z, self.z.front + "PTR\n", self.z.footer,
                      "shard\n" + self.z.footer, ["PTR\n"], [], r)
        self.assertIn("L2_FOOTER_MOVED", r.codes)

    def test_red_when_front_matter_changes_outside_the_declared_spans(self):
        tampered = self.z.front.replace("Changelog", "Chnagelog", 1) + "PTR\n"
        r = mod.Result("x")
        ok = mod.assert_L2(self.z, tampered, self.z.footer, "shard", ["PTR\n"], [], r)
        self.assertFalse(ok)
        self.assertIn("L2_FRONTMATTER_UNDECLARED", r.codes)

    def test_a_declared_regenerated_field_is_permitted_and_confined(self):
        """Uses the REAL declared field on the REAL front matter — not a synthetic anchor, because
        a synthetic one tests the test. HANDOFFS.md declares its retained-receipt count regenerated,
        and that count has already drifted by hand, which is why it is declared at all.

        The probe value must differ from whatever the live count currently reads, computed rather
        than hardcoded: a hardcoded literal (this test's own prior form used `3`) is exactly the
        kind of coupling to real, mutable ledger content this repo's own precedent warns about
        (S63's `test_L2_fixture_loss_actually_happened_and_is_still_unrepaired`) — and it went
        live here, not hypothetically: S64's own HANDOFFS.md archive set the real count to 3, the
        very literal this test had hardcoded, making `old == new` and silencing the assertion this
        test exists to make."""
        hf_text = (REPO / "HANDOFFS.md").read_text(encoding="utf-8")
        zh = mod.classify_zones(hf_text, HF, mod.Result("x"))
        name, rx, _fn = HF.regenerated[0]
        m = rx.search(zh.front)
        self.assertIsNotNone(m, "control: the declared field must exist in the live front matter")
        old = m.group(2)
        probe = int(old) + 1  # guaranteed to differ from `old`, whatever `old` currently is

        r = mod.Result("x")
        new_front, reversals = mod.apply_regenerated(zh.front, HF, {"retained": probe}, r)
        self.assertIn("FRONTMATTER_FIELD_REGENERATED", r.codes)
        self.assertNotEqual(new_front, zh.front, "control: the field really changed")
        self.assertEqual(reversals[0][1], old)

        r2 = mod.Result("x")
        ok = mod.assert_L2(zh, new_front + "PTR\n", zh.footer, "shard", ["PTR\n"], reversals, r2)
        self.assertTrue(ok, [f.message for f in r2.findings])

    def test_a_regenerated_field_does_not_license_an_edit_elsewhere(self):
        """NARROWED: the carve-out must not become a blanket permit for front-matter edits."""
        hf_text = (REPO / "HANDOFFS.md").read_text(encoding="utf-8")
        zh = mod.classify_zones(hf_text, HF, mod.Result("x"))
        name, rx, _fn = HF.regenerated[0]
        old = rx.search(zh.front).group(2)
        r = mod.Result("x")
        new_front, reversals = mod.apply_regenerated(zh.front, HF, {"retained": int(old) + 1}, r)
        tampered = new_front.replace("prepend-only", "prepend-onlyX", 1) + "PTR\n"
        self.assertNotEqual(tampered, new_front + "PTR\n", "control: the tamper must apply")
        r2 = mod.Result("x")
        ok = mod.assert_L2(zh, tampered, zh.footer, "shard", ["PTR\n"], reversals, r2)
        self.assertFalse(ok)
        self.assertIn("L2_FRONTMATTER_UNDECLARED", r2.codes)

    def test_red_when_the_pointer_block_is_missing(self):
        r = mod.Result("x")
        ok = mod.assert_L2(self.z, self.z.front, self.z.footer, "shard", ["PTR\n"], [], r)
        self.assertFalse(ok)
        self.assertIn("L2_POINTER_MISSING", r.codes)


# =============================================================================================
# L3 — record partition by identity, order and bytes.
# =============================================================================================

class TestL3(unittest.TestCase):

    def setUp(self):
        self.before = records_of(show("7a71df0^:HANDOFFS.md"), HF)
        self.after = records_of(show("7a71df0:HANDOFFS.md"), HF)
        self.shard = records_of(show("7a71df0:docs/archive/HANDOFFS-archive.md"), HF)

    def test_green_on_a_pure_partition_of_the_same_fixture(self):
        r = mod.Result("x")
        ok = mod.assert_L3(self.before, self.before[:6], self.before[6:], r)
        self.assertTrue(ok, [f.message for f in r.findings])

    def test_red_on_the_real_event_that_edited_a_retained_record(self):
        r = mod.Result("x")
        ok = mod.assert_L3(self.before, self.after, self.shard, r)
        self.assertFalse(ok, "the real 7a71df0 archive was not a pure move; L3 must refuse it")
        self.assertIn("L3_RECORD_ALTERED", r.codes)

    def test_NARROWED_count_only_L3_passes_the_real_event(self):
        """The plausible weaker L3 — 'do the counts partition?' — is green on the event that
        actually shipped a co-mingled edit. Counts are exactly what that event preserved."""
        self.assertEqual(len(self.after) + len(self.shard), len(self.before))   # narrowed: PASSES
        r = mod.Result("x")                                                     # full: REFUSES
        mod.assert_L3(self.before, self.after, self.shard, r)
        self.assertIn("L3_RECORD_ALTERED", r.codes)

    def test_red_on_a_boundary_shift_that_L1_cannot_see(self):
        """L3's independent value: move a line from the end of one record to the start of the next.
        The concatenation is unchanged, so L1 is green; the partition is not, so L3 refuses."""
        recs = ["### 2026-01-01 · [ad hoc] a\n\nalpha\n", "### 2026-01-02 · [ad hoc] b\n\nbeta\n"]
        shifted = [recs[0][:-len("alpha\n")], "alpha\n" + recs[1]]
        self.assertEqual("".join(shifted), "".join(recs), "control: bytes are conserved")
        r1 = mod.Result("x")
        self.assertTrue(mod.assert_L1(recs, shifted[:1],
                                      [mod.transform_record(shifted[1])], r1), "L1 is blind here")
        r3 = mod.Result("x")
        self.assertFalse(mod.assert_L3(recs, shifted[:1], shifted[1:], r3))
        self.assertIn("L3_RECORD_ALTERED", r3.codes)

    def test_red_when_order_is_reversed(self):
        r = mod.Result("x")
        ok = mod.assert_L3(self.before, self.before[:6][::-1], self.before[6:], r)
        self.assertFalse(ok)
        self.assertIn("L3_RECORD_ALTERED", r.codes)


# =============================================================================================
# The transform — the domain predicate IS the contract.
# =============================================================================================

class TestTransform(unittest.TestCase):

    def test_only_root_relative_targets_are_rebased(self):
        src = ("see [a](CLAUDE.md) and [b](https://example.com/x) and [c](#frag) and\n"
               "[d](../up.md) and [e](/abs.md) and [f](docs/x.md#y)\n")
        out = mod.transform_record(src)
        self.assertIn("](../../CLAUDE.md)", out)
        self.assertIn("](../../docs/x.md#y)", out)
        self.assertIn("](https://example.com/x)", out, "absolute URLs must never be prefixed")
        self.assertIn("](#frag)", out)
        self.assertIn("](../up.md)", out)
        self.assertIn("](/abs.md)", out)

    def test_the_naive_key_would_corrupt_absolute_urls(self):
        """NARROWED: key on `](` alone, which is what the design measured as corrupting 14 URLs."""
        src = "[b](https://example.com/x)\n"
        naive = re.sub(r"\]\(([^)\s]*)\)", lambda m: "](../../%s)" % m.group(1), src)
        self.assertIn("](../../https://example.com/x)", naive)          # narrowed: CORRUPTS
        self.assertIn("](https://example.com/x)", mod.transform_record(src))   # full: leaves it

    def test_links_inside_fences_and_code_spans_are_untouched(self):
        """The code-span target must be ROOT-RELATIVE, or the assertion is inert.

        The first version of this test used `](../../x.md)` inside the span — but `_in_domain`
        already refuses any `../`-prefixed target, so `code_span_ranges` did no work and the whole
        span mechanism could be deleted with the suite still green. `](CONTEXT.md)` is in-domain,
        so only the span exclusion can save it.
        """
        src = ("prose [a](CLAUDE.md)\n"
               "a code span `](CONTEXT.md)` explaining the rebase\n"
               "```sh\n[b](CLAUDE.md)\n```\n")
        self.assertTrue(mod._in_domain("CONTEXT.md"),
                        "control: the span's target must be one the transform WOULD rewrite")
        out = mod.transform_record(src)
        self.assertIn("](../../CLAUDE.md)", out, "control: the prose link IS rewritten")
        self.assertIn("`](CONTEXT.md)`", out, "an inline code span must not be rewritten")
        self.assertIn("```sh\n[b](CLAUDE.md)\n```", out, "a fenced block must not be rewritten")

    def test_round_trip_is_the_identity_on_the_real_shard_corpus(self):
        recs = records_of(show("HEAD:docs/archive/HANDOFFS-archive.md"), HF)
        self.assertGreater(len(recs), 10, "control: the corpus must be non-trivial")
        for rec in recs:
            self.assertEqual(mod.invert_record(mod.transform_record(rec)), rec)

    def test_a_record_carrying_an_already_relative_target_is_refused(self):
        r = mod.Result("x")
        ok = mod.check_invertible(["### 2026-01-01 · [ad hoc] x\n\n[a](../../already.md)\n"], r)
        self.assertFalse(ok)
        self.assertIn("TRANSFORM_NOT_INVERTIBLE", r.codes)


# =============================================================================================
# Zones
# =============================================================================================

class TestZones(unittest.TestCase):

    def test_unclassified_trailing_content_aborts_a_footer_none_family(self):
        text = ("# H\n\n---\n\n```handoff\nsession: S1\ndate: 2026-01-01\n```\n\n"
                "prose belonging to S1\n\n---\n\n**A trailing paragraph nobody declared.**\n")
        r = mod.Result("x")
        z = mod.classify_zones(text, HF, r)
        self.assertIsNone(z)
        self.assertIn("ZONE_UNCLASSIFIED", r.codes)
        self.assertEqual(r.exit, 2)

    def test_handoff_trailing_prose_belongs_to_its_record(self):
        text = ("# H\n\n```handoff\nsession: S1\ndate: 2026-01-01\n```\n\nSelf-score 8/10.\n")
        recs = records_of(text, HF)
        self.assertEqual(len(recs), 1)
        self.assertIn("Self-score 8/10.", recs[0],
                      "23% of the HANDOFFS payload lives outside the fences")

    def test_a_four_backtick_wrapper_hides_its_inner_handoff_fence(self):
        text = "# H\n\n````\n```handoff\nsession: S1\n```\n````\n"
        self.assertEqual(records_of(text, HF), [])


# =============================================================================================
# The trigger — the two metrics take different FORMS.
# =============================================================================================

class TestTrigger(unittest.TestCase):

    def test_the_line_form_transplanted_onto_bytes_is_unreachable(self):
        """Design §5.2, mechanised: 'cut until back above 30' cannot be satisfied on the byte
        metric at ANY budget, even trimming to a single record. A trimmer using it would trim to
        empty and still report the trigger unsatisfied."""
        slope, floor = 12472, 2025 + 3767
        for budget in (52927, 65536, 131072, 262144):
            self.assertLess((budget - floor) / float(slope), 30,
                            "budget %d must NOT reach 30 units of byte-headroom" % budget)

    def test_the_byte_form_is_a_level_with_hysteresis_and_terminates(self):
        t = mod.Trigger()
        t.budget = 65536
        t.size_bytes = 200000
        self.assertTrue(t.byte_fires)
        self.assertFalse(t.stops(40000, 100, None, None), "above half budget must not stop")
        self.assertTrue(t.stops(32000, 100, None, None), "at or below half budget must stop")

    def test_the_line_metric_cannot_veto_a_stop_it_cannot_compute(self):
        t = mod.Trigger()
        t.budget = 65536
        self.assertTrue(t.stops(1000, 50, None, None))
        self.assertTrue(t.stops(1000, 50, 0, 0))

    def test_fires_if_either_metric_fires(self):
        t = mod.Trigger()
        t.budget = 65536
        t.size_bytes = 10
        t.line_headroom = 3
        self.assertTrue(t.fires, "the line metric alone must be able to fire")
        t2 = mod.Trigger()
        t2.budget = 100
        t2.size_bytes = 500
        t2.line_headroom = 999
        self.assertTrue(t2.fires, "the byte metric alone must be able to fire")


# =============================================================================================
# End to end, in a scratch repo.
# =============================================================================================

def sh(cwd, *args):
    return subprocess.run(list(args), cwd=str(cwd), stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True)


FOOTER = ("\n---\n\n**Release history before v3.0:** not re-narrated here — see\n"
          "[`CLAUDE.md` §Versioning](CLAUDE.md#versioning). This ledger is prepend-only.\n")


def make_repo(tmp, n_records=30, body=3500, footer=False):
    p = Path(tmp)
    (p / "docs" / "archive").mkdir(parents=True)
    entries = "".join(
        "### 2026-01-%02d · [ad hoc] entry %d\n\n"
        "see [the runner](SESSION_RUNNER.md), [abs](https://example.com/a) and [frag](#f)\n"
        "%s\n\n" % (i % 28 + 1, i, "x" * body)
        for i in range(n_records))
    (p / "CHANGELOG.md").write_text(
        "# Changelog\n\nFront matter prose about [the runner](SESSION_RUNNER.md).\n"
        "Retained entries: **0**.\n\n---\n\n"
        "## 2026-01\n\n" + entries + (FOOTER if footer else ""), encoding="utf-8")
    sh(p, "git", "init", "-q", ".")
    sh(p, "git", "config", "user.email", "t@t")
    sh(p, "git", "config", "user.name", "T")
    sh(p, "git", "add", "-A")
    sh(p, "git", "commit", "-qm", "seed")
    return p


def make_handoff_repo(tmp, n_hf_records=6, hf_body=1200, n_cl_records=3, cl_body=50):
    """A repo holding BOTH ledgers, seeded in ONE commit — HANDOFFS.md fence-kind records with the
    real declared regen field (`This file currently holds **N**`), plus a minimal CHANGELOG.md
    (check_P1's ledger_rel_for() is hardcoded to CHANGELOG.md regardless of which file is trimmed,
    and insert_ledger_entry() writes into it even when trimming HANDOFFS.md — both need it to
    exist and parse). One commit, not two, so the P1 undocumented-set is empty at trim time: a
    second commit adding HANDOFFS.md after CHANGELOG.md's own commit would itself be undocumented.
    """
    p = Path(tmp)
    (p / "docs" / "archive").mkdir(parents=True)
    cl_entries = "".join(
        "### 2026-01-%02d · [ad hoc] entry %d\n\nbody %s\n\n" % (i % 28 + 1, i, "x" * cl_body)
        for i in range(n_cl_records))
    (p / "CHANGELOG.md").write_text(
        "# Changelog\n\nFront matter.\nRetained entries: **0**.\n\n---\n\n"
        "## 2026-01\n\n" + cl_entries, encoding="utf-8")

    def hf_rec(i):
        return (
            "```handoff\n"
            "session: S%d\n"
            "date: 2026-01-%02d\n"
            "status: complete\n"
            "active_task: x\n"
            "what_was_done: %s\n"
            "next_steps: n\n"
            "key_files: k\n"
            "gotchas: g\n"
            "runtime_smoke: r\n"
            "changelog_ref: c\n"
            "commit: %040x\n"
            "```\n"
            "Self-score **8/10.** commentary about session %d.\n\n"
            % (i, n_hf_records - i, "x" * hf_body, i, i)
        )

    hf_entries = "---\n\n".join(hf_rec(i) for i in range(n_hf_records))
    (p / "HANDOFFS.md").write_text(
        "# Handoff Receipts\n\nThis file currently holds **0**.\n\n---\n\n" + hf_entries,
        encoding="utf-8")
    sh(p, "git", "init", "-q", ".")
    sh(p, "git", "config", "user.email", "t@t")
    sh(p, "git", "config", "user.name", "T")
    sh(p, "git", "add", "-A")
    sh(p, "git", "commit", "-qm", "seed")
    return p


def run_trim(repo, *args):
    return subprocess.run([sys.executable, str(TRIM_PY)] + list(args), cwd=str(repo),
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)


class TestEndToEnd(unittest.TestCase):

    def test_dry_run_is_the_default_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            r = run_trim(p, "--file", "CHANGELOG.md", "--today", "2026-02-01")
            self.assertIn("[DRY_RUN]", r.stdout)
            self.assertEqual(sh(p, "git", "status", "--porcelain").stdout.strip(), "",
                             "a dry run must leave the tree untouched")

    def test_write_produces_a_shard_a_proof_and_an_uncommitted_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            r = run_trim(p, "--file", "CHANGELOG.md", "--write", "--today", "2026-02-01")
            for code in ("[L1_OK]", "[L2_OK]", "[L3_OK]", "[P1A_OK]", "[WROTE]"):
                self.assertIn(code, r.stdout, r.stdout)
            shards = sorted((p / "docs" / "archive").glob("CHANGELOG-through-*.md"))
            self.assertEqual(len(shards), 1)
            self.assertTrue((p / (str(shards[0].relative_to(p)) + ".verify.sh")).is_file())
            self.assertEqual(sh(p, "git", "log", "--oneline").stdout.count("\n"), 1,
                             "the trimmer must never commit")

    def test_the_generated_proof_passes_before_and_after_the_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            run_trim(p, "--file", "CHANGELOG.md", "--write", "--today", "2026-02-01")
            v = sorted((p / "docs" / "archive").glob("*.verify.sh"))[0]
            pre = sh(p, "bash", str(v))
            self.assertIn("OK: L1, L2/front-matter, L3 hold", pre.stdout, pre.stdout)
            sh(p, "git", "add", "-A")
            sh(p, "git", "commit", "-qm", "trim")
            post = sh(p, "bash", str(v))
            self.assertIn("OK: L1, L2/front-matter, L3 hold", post.stdout, post.stdout)
            self.assertIn("the trim commit", post.stdout)

    def test_the_proof_goes_RED_when_the_shard_is_tampered_with(self):
        """The tamper must land on a record that is ACTUALLY IN THE SHARD. The first draft of this
        test edited 'entry 0' — which is newest-on-top and therefore RETAINED, so the edit was a
        no-op and the proof passed for the right reason on the wrong file. Hence the control."""
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            run_trim(p, "--file", "CHANGELOG.md", "--write", "--today", "2026-02-01")
            shard = sorted((p / "docs" / "archive").glob("CHANGELOG-through-*.md"))[0]
            before = shard.read_text(encoding="utf-8")
            victim = re.search(r"(?m)^### .*\[ad hoc\] (entry \d+)$", before)
            self.assertIsNotNone(victim, "control: the shard must contain a real record heading")
            after = before.replace(victim.group(1), victim.group(1) + " TAMPERED", 1)
            self.assertNotEqual(after, before, "control: the tamper must actually change the shard")
            shard.write_text(after, encoding="utf-8")
            v = sh(p, "bash", str(shard) + ".verify.sh")
            self.assertIn("FAIL:", v.stdout, v.stdout)
            self.assertNotEqual(v.returncode, 0)

    def test_the_proof_goes_RED_when_the_live_file_loses_a_retained_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            run_trim(p, "--file", "CHANGELOG.md", "--write", "--today", "2026-02-01")
            live = p / "CHANGELOG.md"
            text = live.read_text(encoding="utf-8")
            heads = re.findall(r"(?m)^### .*$", text)
            self.assertGreater(len(heads), 2, "control: there must be a retained record to drop")
            start = text.index(heads[-1])
            live.write_text(text[:start], encoding="utf-8")
            v = sh(p, "bash", str(sorted((p / "docs" / "archive").glob("*.verify.sh"))[0]))
            self.assertIn("FAIL:", v.stdout, v.stdout)

    def test_P1_refuses_when_the_undocumented_set_is_non_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            (p / "src.txt").write_text("unrecorded action\n", encoding="utf-8")
            sh(p, "git", "add", "-A")
            sh(p, "git", "commit", "-qm", "an action with no ledger entry")
            r = run_trim(p, "--file", "CHANGELOG.md", "--write", "--today", "2026-02-01")
            self.assertIn("[P1_UNDOCUMENTED]", r.stdout)
            self.assertNotIn("[WROTE]", r.stdout)
            self.assertEqual(sh(p, "git", "status", "--porcelain").stdout.strip(), "")

    def test_P1a_keeps_the_trim_from_hiding_itself(self):
        """After a trim commit the ledger frontier IS that commit, so the undocumented set is
        empty ONLY because the trim recorded itself. Without the entry the trim's first act would
        be to advance the frontier past unrecorded history."""
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            run_trim(p, "--file", "CHANGELOG.md", "--write", "--today", "2026-02-01")
            text = (p / "CHANGELOG.md").read_text(encoding="utf-8")
            self.assertIn("[ad hoc] Ledger trim:", text)
            self.assertEqual(len(re.findall(r"(?m)^### .*Ledger trim:", text)), 1)

    def test_P1a_fires_when_the_ledger_did_NOT_gain_exactly_one_entry(self):
        """Drives the post-condition RED directly. Without this the whole check can be deleted and
        the suite stays green — which is exactly what the mutation harness found."""
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp, n_records=3, body=10)
            ledger = p / "CHANGELOG.md"
            actual = len(records_of(ledger.read_text(encoding="utf-8"), CL))
            self.assertEqual(actual, 3, "control: the fixture ledger must hold 3 records")

            ok_r = mod.Result("x")
            self.assertTrue(mod.check_P1a(ledger, CL, actual - 1, ok_r),
                            "expected == actual-1 means exactly one entry was gained")
            self.assertIn("P1A_OK", ok_r.codes)

            bad_r = mod.Result("x")
            self.assertFalse(mod.check_P1a(ledger, CL, actual, bad_r),
                             "no entry gained must be caught")
            self.assertIn("P1A_LEDGER_ENTRY", bad_r.codes)
            self.assertEqual(bad_r.exit, 2)

            two_r = mod.Result("x")
            self.assertFalse(mod.check_P1a(ledger, CL, actual - 2, two_r),
                             "TWO entries gained must also be caught, not just zero")
            self.assertIn("P1A_LEDGER_ENTRY", two_r.codes)

    def test_shard_collision_is_a_refusal_never_an_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            run_trim(p, "--file", "CHANGELOG.md", "--write", "--today", "2026-02-01")
            sh(p, "git", "add", "-A")
            sh(p, "git", "commit", "-qm", "trim")
            shard = sorted((p / "docs" / "archive").glob("CHANGELOG-through-*.md"))[0]
            key = shard.name[len("CHANGELOG-through-"):-3]
            before = shard.read_bytes()
            r = run_trim(p, "--file", "CHANGELOG.md", "--cut", key, "--write", "--today", "2026-02-02")
            self.assertIn("[SHARD_EXISTS]", r.stdout, r.stdout)
            self.assertEqual(shard.read_bytes(), before, "the earlier shard must be untouched")

    def test_srf_abstains_out_loud_before_a_first_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            r = run_trim(p, "--file", "CHANGELOG.md", "--check")
            self.assertIn("[SRF_UNDEFINED]", r.stdout)
            self.assertNotIn("[SRF_RED]", r.stdout, "abstention must not block")

    def test_check_never_writes_even_with_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            r = run_trim(p, "--file", "CHANGELOG.md", "--check", "--write")
            self.assertIn("[CHECK]", r.stdout)
            self.assertNotIn("[WROTE]", r.stdout)
            self.assertEqual(sh(p, "git", "status", "--porcelain").stdout.strip(), "")

    def test_batched_write_is_a_usage_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            r = run_trim(p, "--file", "CHANGELOG.md", "--file", "HANDOFFS.md", "--write")
            self.assertEqual(r.returncode, 3)
            self.assertIn("one --file per --write", r.stdout)

    def test_an_unconfigured_file_gets_no_generic_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            (p / "NOTES.md").write_text("### 2026-01-01 · [ad hoc] x\n\nbody\n", encoding="utf-8")
            r = run_trim(p, "--file", "NOTES.md")
            self.assertIn("[NO_CONFIG]", r.stdout)
            self.assertEqual(r.returncode, 3)

    def test_srf_red_refuses_and_force_overrides(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            run_trim(p, "--file", "CHANGELOG.md", "--write", "--today", "2026-02-01")
            sh(p, "git", "add", "-A")
            sh(p, "git", "commit", "-qm", "trim")
            # Grow the file back past its pre-archive size -> SRF >= 1.00.
            pre = int(sh(p, "git", "cat-file", "-s",
                         sh(p, "git", "rev-parse", "HEAD^:CHANGELOG.md").stdout.strip()).stdout)
            text = (p / "CHANGELOG.md").read_text(encoding="utf-8")
            grow = "".join("### 2026-03-%02d · [ad hoc] new %d\n\n%s\n\n" % (i % 28 + 1, i, "y" * 3000)
                           for i in range(40))
            idx = text.index("### ")
            (p / "CHANGELOG.md").write_text(text[:idx] + grow + text[idx:], encoding="utf-8")
            sh(p, "git", "add", "-A")
            sh(p, "git", "commit", "-qm", "growth recorded")
            self.assertGreater((p / "CHANGELOG.md").stat().st_size, pre,
                               "control: the file must really be back past its pre-archive size")
            r = run_trim(p, "--file", "CHANGELOG.md", "--write", "--today", "2026-04-01")
            self.assertIn("[SRF_RED]", r.stdout, r.stdout)
            self.assertNotIn("[WROTE]", r.stdout)
            r2 = run_trim(p, "--file", "CHANGELOG.md", "--write", "--force", "--today", "2026-04-01")
            self.assertIn("[WROTE]", r2.stdout, r2.stdout)


# =============================================================================================
# BL-27 — the GENERATED .verify.sh has two false-positive triggers on HANDOFFS.md that the
# internal --check/--write assertions do not share (they have assert_L2's declared-field-reversal
# exception; the standalone script did not). Reproduced against a real end-to-end HANDOFFS.md trim
# through the actual subprocess, not just the internal assert_L2 unit — the defect lives entirely
# in the generated shell/python text, not in the tool's own in-memory checks.
# =============================================================================================

class TestVerifyShHandoffFalsePositives(unittest.TestCase):

    def test_regenerated_front_matter_field_no_longer_false_fails_verify_sh(self):
        """Fix 1. The trim's own regenerated receipt-count line changes on every archive by
        construction — the standalone proof must not read that as data loss."""
        with tempfile.TemporaryDirectory() as tmp:
            p = make_handoff_repo(tmp)
            r = run_trim(p, "--file", "HANDOFFS.md", "--cut", "2", "--write", "--today", "2026-02-01")
            self.assertIn("[WROTE]", r.stdout, r.stdout)
            live = (p / "HANDOFFS.md").read_text(encoding="utf-8")
            self.assertIn("This file currently holds **2**", live,
                         "control: the regenerated field must actually have changed")
            shard = sorted((p / "docs" / "archive").glob("HANDOFFS-through-*.md"))[0]
            v = sh(p, "bash", str(shard) + ".verify.sh")
            self.assertIn("OK: L1, L2/front-matter, L3 hold", v.stdout, v.stdout)
            self.assertEqual(v.returncode, 0)

    def test_an_undeclared_front_matter_edit_still_fails_L2_even_with_the_field_regenerated(self):
        """NARROWED control for fix 1 — the exemption must not become a blanket permit. An edit
        OUTSIDE the declared field's own parens, alongside a real regenerated-field change, must
        still be caught: the same shape as `test_a_regenerated_field_does_not_license_an_edit_elsewhere`,
        but through the actual generated script rather than the internal assert_L2 unit.

        The tamper must be a full-line REPLACEMENT, not an append — the "missing" check compares
        by substring (`ln not in afront`), so a tamper that merely appends to a line leaves the
        original text intact as a substring of the edited one and is invisible to it. That gap is
        real and pre-existing (open as its own finding, not this session's to fix), but a control
        built on it would pass for the wrong reason — masked by the very regen-field false-positive
        this test exists to prove is no longer masking anything.
        """
        with tempfile.TemporaryDirectory() as tmp:
            p = make_handoff_repo(tmp)
            run_trim(p, "--file", "HANDOFFS.md", "--cut", "2", "--write", "--today", "2026-02-01")
            live = p / "HANDOFFS.md"
            text = live.read_text(encoding="utf-8")
            before = text
            text = text.replace("# Handoff Receipts", "# TAMPERED", 1)
            self.assertNotEqual(text, before, "control: the tamper must actually change the file")
            self.assertNotIn("# Handoff Receipts", text,
                             "control: the tamper must be a full replacement, not an append -- the "
                             "old text surviving as a substring of the new line would defeat the "
                             "'missing' check's own (pre-existing, unrelated) substring comparison")
            live.write_text(text, encoding="utf-8")
            shard = sorted((p / "docs" / "archive").glob("HANDOFFS-through-*.md"))[0]
            v = sh(p, "bash", str(shard) + ".verify.sh")
            self.assertIn("FAIL:", v.stdout, v.stdout)
            self.assertIn("L2 FRONT MATTER", v.stdout, v.stdout)
            self.assertNotEqual(v.returncode, 0)

    def test_frontier_record_edit_bundled_into_trim_commit_still_fails_but_is_labelled(self):
        """Fix 2. This repo's own established practice (S61/S63/S64): a session's frontier receipt
        is finalized (status: pending -> complete) in the SAME commit as the archive write. The
        standalone script re-run later must still FAIL (a real loss can have this exact shape) —
        but must now also print a NOTE naming the known pattern, so a reader does not mistake a
        legitimate bundled edit for an unqualified loss."""
        with tempfile.TemporaryDirectory() as tmp:
            p = make_handoff_repo(tmp)
            run_trim(p, "--file", "HANDOFFS.md", "--cut", "2", "--write", "--today", "2026-02-01")
            live = p / "HANDOFFS.md"
            text = live.read_text(encoding="utf-8")
            before = text
            # Record 0 (S0, the newest/frontier — file position 0 is topmost/newest, though dates
            # descend with i) — simulate its own close-out finalize, bundled into the trim commit.
            self.assertIn("session: S0", text, "control: the frontier record must be S0")
            text = text.replace("status: complete\nactive_task: x",
                                "status: complete\nactive_task: x (finalized)", 1)
            self.assertNotEqual(text, before, "control: the tamper must actually change record 0")
            live.write_text(text, encoding="utf-8")
            sh(p, "git", "add", "-A")
            sh(p, "git", "commit", "-qm", "trim + frontier finalize, bundled")
            shard = sorted((p / "docs" / "archive").glob("HANDOFFS-through-*.md"))[0]
            v = sh(p, "bash", str(shard) + ".verify.sh")
            self.assertIn("FAIL:", v.stdout, v.stdout)
            self.assertIn("NOTE:", v.stdout, v.stdout)
            self.assertIn("BL-27", v.stdout, v.stdout)
            self.assertNotEqual(v.returncode, 0, "a bundled edit must still FAIL, never pass silently")

    def test_a_non_frontier_record_edit_bundled_into_trim_commit_gets_no_such_label(self):
        """NARROWED control for fix 2 — the label must not spread to a record that is not the
        frontier. Editing the OTHER retained record (position 1, not 0) is real, uncovered data
        alteration and must fail with no reassuring NOTE."""
        with tempfile.TemporaryDirectory() as tmp:
            p = make_handoff_repo(tmp)
            run_trim(p, "--file", "HANDOFFS.md", "--cut", "2", "--write", "--today", "2026-02-01")
            live = p / "HANDOFFS.md"
            text = live.read_text(encoding="utf-8")
            before = text
            self.assertIn("session: S1", text, "control: the second retained record must be S1")
            text = text.replace("session: S1\n", "session: S1-TAMPERED\n", 1)
            self.assertNotEqual(text, before, "control: the tamper must actually change record 1")
            live.write_text(text, encoding="utf-8")
            sh(p, "git", "add", "-A")
            sh(p, "git", "commit", "-qm", "trim + an edit to the wrong record, bundled")
            shard = sorted((p / "docs" / "archive").glob("HANDOFFS-through-*.md"))[0]
            v = sh(p, "bash", str(shard) + ".verify.sh")
            self.assertIn("FAIL:", v.stdout, v.stdout)
            self.assertNotIn("NOTE:", v.stdout, v.stdout)
            self.assertNotEqual(v.returncode, 0)


# =============================================================================================
# Regression tests for the defects an adversarial review found in the first build of this tool.
# Each one existed BECAUSE the corresponding guard was wired to the wrong operand and no test
# noticed. They mutate the WRITE PATH — not the predicate — because mutating the predicate is
# exactly what the first mutation harness did, and it scored 13/13 while all three assertions
# were tautologies at their only production call site.
# =============================================================================================

class TestWritePathIsActuallyGated(unittest.TestCase):

    def _run_in_proc(self, repo, **patches):
        """Run evaluate() in-process with parts of the write path mutated."""
        saved = {k: getattr(mod, k) for k in patches}
        for k, v in patches.items():
            setattr(mod, k, v)
        cwd = os.getcwd()
        try:
            os.chdir(str(repo))
            opts = type("O", (), dict(write=True, check=False, cut=None, budget_bytes=40000,
                                      force=False, today="2026-02-01"))()
            r = mod.Result(Path("CHANGELOG.md"))
            mod.evaluate(Path("CHANGELOG.md"), opts, r)
            return r
        finally:
            os.chdir(cwd)
            for k, v in saved.items():
                setattr(mod, k, v)

    def test_control_the_unmutated_write_path_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            r = self._run_in_proc(p)
            self.assertIn("L1_OK", r.codes, [f.message for f in r.findings])
            self.assertIn("L3_OK", r.codes)
            self.assertIn("WROTE", r.codes)

    def test_a_shard_that_silently_drops_a_record_is_REFUSED_before_the_write(self):
        """The defect: assertions were wired to records[:k] + records[k:] == records, an identity.
        A shard body missing its oldest record was written with [L1_OK] [L2_OK] [L3_OK] [WROTE]."""
        real = mod.build_shard
        drop = lambda spec, live, shard, recs, span, key: real(spec, live, shard, recs[:-1], span, key)
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            r = self._run_in_proc(p, build_shard=drop)
            self.assertNotIn("WROTE", r.codes, "a record-losing trim must never be written")
            self.assertIn("L1_MISMATCH", r.codes)
            self.assertIn("L3_RECORD_COUNT", r.codes)
            self.assertEqual(sh(p, "git", "status", "--porcelain").stdout.strip(), "",
                             "nothing may reach the working tree")

    def test_a_trim_that_drops_the_footer_is_REFUSED(self):
        """Proves L2 is wired to the ARTIFACT, not to the input. With `assert_L2` handed the
        before-footer as its after-footer, this passes with [L2_OK] and the footer is destroyed."""
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp, footer=True)
            z = mod.classify_zones((p / "CHANGELOG.md").read_text(encoding="utf-8"),
                                   CL, mod.Result("x"))
            self.assertTrue(z.footer.strip(), "control: the fixture must have a footer to drop")
            r = self._run_in_proc(p, assemble_live=lambda f, ret, foot: f + "".join(ret))
            self.assertNotIn("WROTE", r.codes, "a footer-dropping trim must never be written")
            self.assertIn("L2_FOOTER_ALTERED", r.codes, [f.message for f in r.findings])
            self.assertEqual(sh(p, "git", "status", "--porcelain").stdout.strip(), "")

    def test_control_a_footered_ledger_trims_cleanly(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp, footer=True)
            r = self._run_in_proc(p)
            self.assertIn("WROTE", r.codes, [f.message for f in r.findings])
            self.assertIn("L2_OK", r.codes)

    def test_the_recorded_size_is_the_size_of_the_file_actually_written(self):
        """The entry states the live file's post-trim size, and the entry is IN that file."""
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            run_trim(p, "--file", "CHANGELOG.md", "--write", "--budget-bytes", "40000",
                     "--today", "2026-02-01")
            text = (p / "CHANGELOG.md").read_text(encoding="utf-8")
            m = re.search(r"Live file [\d,]+ B → ([\d,]+) B", text)
            self.assertIsNotNone(m, "control: the entry must state a post-trim size")
            claimed = int(m.group(1).replace(",", ""))
            actual = len(text.encode("utf-8"))
            self.assertEqual(claimed, actual,
                             "the frozen record must not be short by the length of its own entry")


class TestReviewRegressions(unittest.TestCase):

    def test_a_cut_key_that_would_nest_the_shard_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            sh(p, "git", "tag", "rel/v1.0")
            self.assertEqual(sh(p, "git", "rev-parse", "--verify", "rel/v1.0").returncode, 0,
                             "control: the ref must exist, or CUT_UNKNOWN_REF fires first")
            r = run_trim(p, "--file", "CHANGELOG.md", "--cut", "@rel/v1.0",
                         "--budget-bytes", "40000", "--write", "--today", "2026-02-01")
            self.assertIn("[CUT_KEY_UNSAFE]", r.stdout, r.stdout)
            self.assertFalse(list((p / "docs" / "archive").rglob("*.md")),
                             "no shard may be created outside the flat namespace")

    def test_a_same_month_trim_works(self):
        """Every synthetic fixture crosses a month boundary (2026-01 records, --today 2026-02-01),
        so `month_heading` was never empty and the empty declared-insertion path was unreachable.
        The real CHANGELOG.md is same-month, and it broke there. Cover both."""
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            r = run_trim(p, "--file", "CHANGELOG.md", "--write", "--budget-bytes", "40000",
                         "--today", "2026-01-31")
            self.assertNotIn("[LEDGER_MONTH_BOUNDARY]", r.stdout,
                             "control: this run must NOT cross a month boundary")
            self.assertNotIn("[L2_DECLARED_INSERT_MISSING]", r.stdout, r.stdout)
            self.assertIn("[L2_OK]", r.stdout, r.stdout)
            self.assertIn("[WROTE]", r.stdout, r.stdout)
            v = sh(p, "bash", str(sorted((p / "docs" / "archive").glob("*.verify.sh"))[0]))
            self.assertIn("OK:", v.stdout, v.stdout)

    def test_the_month_boundary_is_reported_not_silently_misfiled(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            r = run_trim(p, "--file", "CHANGELOG.md", "--write", "--budget-bytes", "40000",
                         "--today", "2026-02-01")
            self.assertIn("[LEDGER_MONTH_BOUNDARY]", r.stdout,
                          "a trim in a new month must say so; the fixture is all 2026-01")
            self.assertIn("[L2_OK]", r.stdout, "and the new heading must not trip L2")

    def test_the_proof_catches_a_front_matter_line_deleted_after_the_trim(self):
        """Design §4.2's L2 has a front-matter half; the first proof script had none, and printed
        'L1, L2 and L3 hold' after running zero L2 assertions on both real ledgers."""
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            run_trim(p, "--file", "CHANGELOG.md", "--write", "--budget-bytes", "40000",
                     "--today", "2026-02-01")
            live = p / "CHANGELOG.md"
            text = live.read_text(encoding="utf-8")
            self.assertIn("Front matter prose", text, "control: the line must be there to delete")
            live.write_text(text.replace("Front matter prose about [the runner](SESSION_RUNNER.md).",
                                         "", 1), encoding="utf-8")
            v = sh(p, "bash", str(sorted((p / "docs" / "archive").glob("*.verify.sh"))[0]))
            self.assertIn("L2 FRONT MATTER lost", v.stdout, v.stdout)
            self.assertNotEqual(v.returncode, 0)

    def test_the_proof_names_the_clauses_it_actually_ran(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            run_trim(p, "--file", "CHANGELOG.md", "--write", "--budget-bytes", "40000",
                     "--today", "2026-02-01")
            v = sh(p, "bash", str(sorted((p / "docs" / "archive").glob("*.verify.sh"))[0]))
            self.assertIn("checked: L1, L2/front-matter, L3", v.stdout)
            self.assertNotIn("L2/footer", v.stdout,
                             "this fixture has no footer, so the footer clause must NOT be claimed")


    def test_a_footered_ledger_keeps_its_footer_live_and_out_of_the_shard(self):
        """W7: with no footer in any end-to-end fixture, L2's footer clauses were unreachable from
        integration — the tool could be handed the BEFORE footer as its AFTER footer and no test
        would notice. This fixture has one, shaped like the real pre-v3.0 scope footer that the
        `020ba3f` archive actually lost."""
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp, footer=True)
            z = mod.classify_zones((p / "CHANGELOG.md").read_text(encoding="utf-8"),
                                   CL, mod.Result("x"))
            self.assertIn("Release history before v3.0", z.footer,
                          "control: the fixture must actually HAVE a footer zone")
            r = run_trim(p, "--file", "CHANGELOG.md", "--write", "--budget-bytes", "40000",
                         "--today", "2026-02-01")
            self.assertIn("[L2_OK]", r.stdout, r.stdout)
            live = (p / "CHANGELOG.md").read_text(encoding="utf-8")
            shard = sorted((p / "docs" / "archive").glob("CHANGELOG-through-*.md"))[0]
            body = shard.read_text(encoding="utf-8")
            self.assertIn("Release history before v3.0", live, "the footer is pinned to live")
            self.assertNotIn("Release history before v3.0", body, "and must not reach the shard")
            after = mod.classify_zones(live, CL, mod.Result("x"))
            self.assertEqual(after.footer, z.footer, "byte-identical, not merely present")
            v = sh(p, "bash", str(shard) + ".verify.sh")
            self.assertIn("L2/footer", v.stdout, "the proof must now RUN the footer clause")
            self.assertIn("OK:", v.stdout, v.stdout)

    def test_a_footered_ledger_refuses_when_the_footer_would_migrate(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp, footer=True)
            z = mod.classify_zones((p / "CHANGELOG.md").read_text(encoding="utf-8"),
                                   CL, mod.Result("x"))
            r = mod.Result("x")
            ok = mod.assert_L2(z, z.front + "PTR\n", "", "shard\n" + z.footer, ["PTR\n"], [], r)
            self.assertFalse(ok)
            self.assertIn("L2_FOOTER_ALTERED", r.codes)
            self.assertIn("L2_FOOTER_MOVED", r.codes)

    def test_the_transform_is_exercised_end_to_end(self):
        """The e2e fixtures previously had zero links inside records, so `transform_record` was the
        identity in every integration test and the proof's inverse could be deleted unnoticed."""
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp)
            run_trim(p, "--file", "CHANGELOG.md", "--write", "--budget-bytes", "40000",
                     "--today", "2026-02-01")
            shard = sorted((p / "docs" / "archive").glob("CHANGELOG-through-*.md"))[0]
            body = shard.read_text(encoding="utf-8")
            self.assertIn("](../../SESSION_RUNNER.md)", body, "root-relative targets must rebase")
            self.assertIn("](https://example.com/a)", body, "absolute URLs must not")
            self.assertIn("](#f)", body, "fragments must not")

    def test_the_footer_moved_clause_sees_through_the_rebase(self):
        """A footer swept into the records zone is transformed on its way into the shard, so a
        verbatim substring test misses it. The real 020ba3f footer contains exactly such a link."""
        z = mod.classify_zones(show("020ba3f^:CHANGELOG.md"), CL, mod.Result("x"))
        self.assertIn("](", z.footer, "control: the fixture footer must contain a rebasable link")
        rebased = mod.transform_record(z.footer)
        self.assertNotEqual(rebased, z.footer, "control: the rebase must actually change it")
        self.assertNotIn(z.footer.strip(), rebased, "control: verbatim substring no longer matches")
        r = mod.Result("x")
        ok = mod.assert_L2(z, z.front + "PTR\n", z.footer, "shard\n" + rebased, ["PTR\n"], [], r)
        self.assertFalse(ok, "the transformed footer must still be detected in the shard")
        self.assertIn("L2_FOOTER_MOVED", r.codes)

    def test_an_unclassifiable_baseline_makes_the_line_metric_abstain(self):
        t = mod.Trigger()
        self.assertIsNone(t.line_headroom)
        self.assertTrue(t.stops(10, 10, None, None),
                        "an abstaining rate must not veto a stop it cannot compute")

    def test_srf_reports_both_boundaries_and_the_refusal_uses_the_most_recent(self):
        """The design's one explicitly-labelled departure from H3. Every other fixture creates a
        single archive event, so most-recent and largest-drop coincide and the choice is untested.
        Here the two events are built directly, with deliberately different drops."""
        with tempfile.TemporaryDirectory() as tmp:
            p = make_repo(tmp, n_records=40, body=3000)
            arch = p / "docs" / "archive"

            def event(name, keep):
                """Shrink the live file to `keep` records and add a shard in the same commit."""
                z = mod.classify_zones(read_live(p), CL, mod.Result("x"))
                recs = z.records()
                (arch / name).write_text("# shard\n\n" + "".join(recs[keep:]), encoding="utf-8")
                (p / "CHANGELOG.md").write_text(z.front + "".join(recs[:keep]) + z.footer,
                                                encoding="utf-8")
                sh(p, "git", "add", "-A")
                sh(p, "git", "commit", "-qm", "archive " + name)

            def read_live(repo):
                return (repo / "CHANGELOG.md").read_text(encoding="utf-8")

            event("CHANGELOG-through-2026-01-10.md", 8)     # event 1: the LARGE drop
            # regrow a little, then a second, SMALLER drop
            z = mod.classify_zones(read_live(p), CL, mod.Result("x"))
            grow = "".join("### 2026-03-%02d · [ad hoc] g%d\n\n%s\n\n" % (i % 28 + 1, i, "y" * 800)
                           for i in range(6))
            (p / "CHANGELOG.md").write_text(z.front + grow + "".join(z.records()) + z.footer,
                                            encoding="utf-8")
            sh(p, "git", "add", "-A")
            sh(p, "git", "commit", "-qm", "growth")
            event("CHANGELOG-through-2026-03-06.md", 10)    # event 2: the SMALLER drop

            events = mod.archive_events(p, CL)
            self.assertEqual(len(events), 2, "control: the fixture must create TWO archive events")
            # Ordering must follow the COMMIT GRAPH, not %ct (ties) and not sha (arbitrary).
            newer = sh(p, "git", "rev-list", "--topo-order", "HEAD").stdout.split()
            self.assertLess(newer.index(events[1][0]), newer.index(events[0][0]),
                            "archive_events must return oldest-first by commit-graph position")
            drops = [pre - post for _sha, pre, post, _rel in events]
            self.assertNotEqual(drops[0], drops[1],
                                "control: the drops must differ, or nothing is being chosen between")
            self.assertGreater(drops[0], drops[1],
                               "control: the LARGEST drop must be the OLDER event, so the two "
                               "boundary policies genuinely disagree")

            # Regrow past both boundaries so BOTH SRFs are positive — otherwise the ratio is
            # meaningless and the tool correctly declines to print one, and the test would be
            # asserting on a branch it never reaches.
            z = mod.classify_zones(read_live(p), CL, mod.Result("x"))
            regrow = "".join("### 2026-05-%02d · [ad hoc] r%d\n\n%s\n\n" % (i % 28 + 1, i, "z" * 2500)
                             for i in range(45))
            (p / "CHANGELOG.md").write_text(z.front + regrow + "".join(z.records()) + z.footer,
                                            encoding="utf-8")
            out = run_trim(p, "--file", "CHANGELOG.md", "--check").stdout
            self.assertNotIn("non-positive", out,
                             "control: both SRFs must be positive, or no ratio is printed")
            self.assertIn("vs the most recent archive", out, out)
            self.assertIn("H3's largest-drop boundary", out, out)
            self.assertIn("policy addition on top of H3", out,
                          "the departure must be labelled as a departure, per design §5.3")
            # And the two reported values must actually differ — otherwise the label is decoration.
            m = re.search(r"SRF ([\d.]+) vs the most recent archive \w+; ([\d.-]+) vs H3", out)
            self.assertIsNotNone(m, out)
            self.assertNotEqual(m.group(1), m.group(2),
                                "the two boundaries must yield different SRFs in this fixture")


# =============================================================================================
# GRAMMAR_MISMATCH — a file the grammar cannot read must not be reported as a file with nothing
# in it. UAT finding F1 (docs/planning/uat-2026-08-04-six-adopters.md §4).
#
# The defect these pin: evaluate() answered `[NO_RECORDS] ... nothing to archive. (A freshly
# seeded ledger looks exactly like this, and must not be trimmed.)` AT EXIT 0 for a 597,717 B
# ledger holding 130 dated entries and a 1,239,085 B ledger keying entries on table rows, because
# neither
# uses the declared `### YYYY-MM-DD · [tag]` heading. A 1.2 MB ledger and a 324 B fresh seed
# produced byte-identical output and the same exit status, and the message actively reassured.
#
# EVERY FIXTURE HERE IS A LITERAL, ON PURPOSE. The shapes are copied from real adopter ledgers
# and each one's real-world source and measurements are named in its docstring, but no test reads
# a sibling repository: a suite that does is green or red depending on which checkouts happen to
# sit beside this one, which is not a property of this code. The two seed fixtures come from
# `show("HEAD:...")`, not from the working tree — a working-tree read measures a file nobody
# shipped, and during the design review for this very change an agent left an uncommitted edit in
# `starter-kit/CHANGELOG.md` that would have silently redefined the control.
#
# ON ASSERTING `Result.exit` HERE. This file's own rule is "assert on named findings, never on
# the exit code," and design §6.3 states its reason: the exit code "is a union over every check
# the tool runs." That union is `main()`'s `worst = max(...)` across `--file` arguments
# (methodology_trim.py:1629-1635). `Result.exit` is per-evaluation, and in this branch evaluate()
# returns immediately, so the union is over exactly one check — which each test asserts by
# checking `len(r.codes) == 1` beside it. The exit status is pinned because it is half of what
# F1 reports: a mutant that keeps the code and drops `exit_code=3` produces identical `codes`,
# and asserting codes alone lets exactly the reported defect back in.
# =============================================================================================

SEED_CL = "HEAD:starter-kit/CHANGELOG.md"
SEED_HF = "HEAD:starter-kit/HANDOFFS.md"


def one_file_repo(tmp, name, data):
    """A scratch git repo holding exactly one ledger. Bytes in, never a template."""
    p = Path(tmp)
    (p / name).write_bytes(data.encode("utf-8") if isinstance(data, str) else data)
    sh(p, "git", "init", "-q", ".")
    sh(p, "git", "config", "user.email", "t@t")
    sh(p, "git", "config", "user.name", "T")
    sh(p, "git", "add", "-A")
    sh(p, "git", "commit", "-qm", "seed")
    return p


def ev(repo, name, **optkw):
    """evaluate() in-process against `repo`. Mirrors TestWritePathIsActuallyGated._run_in_proc."""
    kw = dict(write=False, check=False, cut=None, budget_bytes=None, force=False,
              today="2026-08-04")
    kw.update(optkw)
    cwd = os.getcwd()
    try:
        os.chdir(str(repo))
        r = mod.Result(Path(name))
        mod.evaluate(Path(name), type("O", (), kw)(), r)
        return r
    finally:
        os.chdir(cwd)


def evaluate_text(case, name, data, **optkw):
    with tempfile.TemporaryDirectory() as tmp:
        return ev(one_file_repo(tmp, name, data), name, **optkw)


# The two shapes F1 found in the wild, reduced to literals. Neither matches
# `^### \d{4}-\d{2}-\d{2} · \[` — the first uses a U+2014 em dash where the grammar wants a
# U+00B7 middle dot plus a bracketed source tag; the second keys entries on table rows under
# `## YYYY-MM` group headings and has no dated `###` heading at all.
MISMATCH_EMDASH = "# Changelog\n\nThe action ledger.\n\n" + "".join(
    "### 2026-07-%02d — did a thing (Session %d)\n\n- Change: something real.\n\n" % (i % 28 + 1, i)
    for i in range(12))

MISMATCH_TABLE = "# Changelog\n\n## 2026-08\n\n| Item | Date | Notes |\n|------|------|-------|\n" + \
    "".join("| **Did a thing %d** | 2026-08-%02d | Session %d. Notes. |\n" % (i, i % 28 + 1, i)
            for i in range(12))


class TestGrammarMismatchFixtureControls(unittest.TestCase):
    """Prove each fixture IS what the tests below assume, before anything is asserted about code.

    Without these, every assertion downstream can pass for the wrong reason — a fixture that
    quietly stopped being a mismatch would make the mismatch tests green by accident.
    """

    def test_the_seed_fixtures_are_reachable_and_are_the_shipped_seeds(self):
        for ref in (SEED_CL, SEED_HF):
            text = show(ref)
            self.assertIsNotNone(text, "%s is unreachable — history changed" % ref)
            self.assertIn(mod_seed_sentinel(), text,
                          "%s must still carry the seed sentinel — the fixtures below build on it" % ref)

    def test_the_seed_fixtures_hold_zero_records_AND_zero_probe_hits(self):
        """The seed is only a control if BOTH halves hold: no records, and nothing that looks like one."""
        cl = show(SEED_CL)
        self.assertEqual(records_of(cl, CL), [], "a freshly seeded ledger has no records")
        self.assertEqual(probe_hits_of(cl, CL), [],
                         "the shipped CHANGELOG seed must produce zero content-probe hits — if a "
                         "future edit adds a dated heading to its prose, fix the seed, not the probe")

    def test_the_mismatch_fixtures_really_do_fail_the_declared_grammar(self):
        """Both fixtures must hold zero records under the grammar AND real content under the probe."""
        for label, data, want_hits in (("em dash", MISMATCH_EMDASH, 12),
                                       ("table rows", MISMATCH_TABLE, 12)):
            self.assertEqual(records_of(data, CL), [], "%s fixture must parse to zero records" % label)
            self.assertEqual(len(probe_hits_of(data, CL)), want_hits,
                             "%s fixture must carry %d probe-visible lines" % (label, want_hits))

    def test_the_mismatch_fixtures_are_UNDER_both_size_signals(self):
        """This is what makes them tests of the PROBE rather than tests of the size rule.

        Both real files F1 names are over the byte ceiling, so a probe-free implementation would
        catch them and ship the probe decorative. Two real adopter ledgers are not:
        `claims-model-starter.wiki/CHANGELOG.md` (28,300 B / 269 lines / 11 probe hits) and
        `feedback-loop-comparison/CHANGELOG.md` (7,067 B / 41 lines / 4 hits), both under both
        limits and both misreported as empty by the shipped tool. These literals stand in for them.
        """
        for label, data in (("em dash", MISMATCH_EMDASH), ("table rows", MISMATCH_TABLE)):
            self.assertLess(len(data.encode("utf-8")), mod.SEED_PLAUSIBLE_MAX_BYTES,
                            "%s fixture must be under the byte ceiling" % label)
            self.assertLess(len(data.splitlines()), mod.READ_CAP_LINES,
                            "%s fixture must be under the line ceiling" % label)


class TestGrammarMismatch(unittest.TestCase):

    # --- the genuine-seed half: must stay exit 0 -------------------------------------------

    def test_the_shipped_CHANGELOG_seed_is_still_reported_as_a_fresh_seed(self):
        r = evaluate_text(self, "CHANGELOG.md", show(SEED_CL))
        self.assertEqual(r.codes, ["NO_RECORDS"], [f.message for f in r.findings])
        self.assertEqual(r.exit, 0, "a day-one adopter must not be told their ledger is broken")

    def test_the_shipped_HANDOFFS_seed_is_still_reported_as_a_fresh_seed(self):
        r = evaluate_text(self, "HANDOFFS.md", show(SEED_HF))
        self.assertEqual(r.codes, ["NO_RECORDS"], [f.message for f in r.findings])
        self.assertEqual(r.exit, 0)

    def test_a_hand_rolled_empty_ledger_with_no_sentinel_is_still_exit_0(self):
        """Copied from ../airqino/CHANGELOG.md, a real 324 B seed that is NOT ours.

        It carries no sentinel, so the exemption cannot save it — only the absence of every
        signal does. This is the case that fails first if a size floor is tightened carelessly.
        """
        data = ("# Changelog\n\nAll notable changes to this project are documented here.\n"
                "Format loosely follows [Keep a Changelog](https://keepachangelog.com/).\n\n"
                "When completing work, remove the item from `BACKLOG.md` and add an entry here.\n\n"
                "## [Unreleased]\n\n"
                "<!-- Add entries here as work is completed. Group by month when the list grows. -->\n")
        self.assertNotIn(mod_seed_sentinel(), data, "control: this fixture has no sentinel")
        r = evaluate_text(self, "CHANGELOG.md", data)
        self.assertEqual(r.codes, ["NO_RECORDS"], [f.message for f in r.findings])
        self.assertEqual(r.exit, 0)

    def test_dated_PROSE_in_a_sealed_seed_does_not_trip_the_probe(self):
        """Two independent guards, and this asserts BOTH are needed.

        A design-review agent added exactly this sentence to the shipped seed while probing this
        change. The anchored probe ignores it (it is not heading- or row-shaped) AND the sentinel
        exemption would cover it anyway. Belt and braces, because the seed is a file adopters get.
        """
        data = show(SEED_CL).replace(
            "## How to add an entry",
            "For instance an entry dated 2026-01-15 sits above one dated 2026-01-14.\n\n"
            "## How to add an entry", 1)
        r = evaluate_text(self, "CHANGELOG.md", data)
        self.assertEqual(r.codes, ["NO_RECORDS"], [f.message for f in r.findings])

    # --- the mismatch half: must refuse, loudly ---------------------------------------------

    def test_an_em_dash_ledger_under_both_size_limits_is_refused_by_the_probe_alone(self):
        """RED against the shipped tool, which answers [NO_RECORDS] at exit 0.

        Shape of ../model_project_constructor/CHANGELOG.md (597,717 B, 130 entries), reduced to a
        size where ONLY the probe can fire.
        """
        r = evaluate_text(self, "CHANGELOG.md", MISMATCH_EMDASH)
        self.assertEqual(r.codes, ["GRAMMAR_MISMATCH"], [f.message for f in r.findings])
        self.assertEqual(len(r.codes), 1)
        self.assertEqual(r.exit, 3, "a file the grammar cannot read is not a file with nothing in it")

    def test_a_table_row_ledger_under_both_size_limits_is_refused_by_the_probe_alone(self):
        """Shape of ../wsfct/CHANGELOG.md — 1,239,085 B, entries as table rows under 8 `## YYYY-MM`
        group headings (`grep -cE '^## [0-9]{4}-[0-9]{2}$'` = 8), 87 probe-visible lines."""
        r = evaluate_text(self, "CHANGELOG.md", MISMATCH_TABLE)
        self.assertEqual(r.codes, ["GRAMMAR_MISMATCH"], [f.message for f in r.findings])
        self.assertEqual(r.exit, 3)

    def test_the_refusal_names_the_evidence_instead_of_reassuring(self):
        """F1's core complaint was the WORDING, not only the code: the message reassured.

        The refusal has to carry what a reader needs to act — how big the file is, how many lines
        the probe saw, where the first one is, and what the grammar actually wants — and must not
        repeat the fresh-seed reassurance.
        """
        r = evaluate_text(self, "CHANGELOG.md", MISMATCH_EMDASH)
        msg = r.findings[0].message
        self.assertNotIn("freshly seeded", msg, "the mismatch must not reuse the seed reassurance")
        self.assertNotIn("nothing to archive", msg)
        # Anchored to the label, not a bare "12": the byte and line counts also contain "12", so a
        # substring check passed a mutant that deleted the count entirely.
        self.assertIn("content probe: 12", msg, "the probe hit count must be stated")
        self.assertRegex(msg, r"\b5\b|\bline 5\b|:5\b", "the first unparsed line must be located")
        self.assertIn("2026-07-01 — did a thing", msg, "the first unparsed line must be quoted")
        self.assertIn(CL.record_start.pattern, msg, "the declared grammar must be shown")

    def test_the_quoted_line_is_bounded(self):
        """A real table-row ledger stores 900+ character rows; ZONE_UNCLASSIFIED bounds at 400."""
        long_row = "| **x** | 2026-08-01 | " + ("y" * 4000) + " |\n"
        r = evaluate_text(self, "CHANGELOG.md", "# Changelog\n\n" + long_row)
        self.assertIn("GRAMMAR_MISMATCH", r.codes)
        self.assertLess(len(r.findings[0].message), 1200,
                        "an unbounded quote turns one finding into a screenful")

    # --- the size signals, each isolated ----------------------------------------------------

    def test_a_file_over_the_byte_ceiling_is_refused_with_zero_probe_hits(self):
        """Isolates the byte signal: no dates anywhere, so only size can fire."""
        data = "# Changelog\n\n" + ("z" * (mod.SEED_PLAUSIBLE_MAX_BYTES + 1)) + "\n"
        r = evaluate_text(self, "CHANGELOG.md", data)
        self.assertEqual(r.codes, ["GRAMMAR_MISMATCH"], [f.message for f in r.findings])
        self.assertEqual(r.exit, 3)

    def test_a_file_of_exactly_the_byte_ceiling_is_NOT_refused(self):
        """The `>` edge. Without this, `>` and `>=` are indistinguishable."""
        head = "# Changelog\n\n"
        data = head + ("z" * (mod.SEED_PLAUSIBLE_MAX_BYTES - len(head)))
        self.assertEqual(len(data.encode("utf-8")), mod.SEED_PLAUSIBLE_MAX_BYTES,
                         "control: the fixture must be EXACTLY the ceiling, not near it")
        r = evaluate_text(self, "CHANGELOG.md", data)
        self.assertEqual(r.codes, ["NO_RECORDS"], [f.message for f in r.findings])

    def test_a_file_over_the_read_cap_is_refused_even_though_it_is_under_budget(self):
        """Isolates the line signal: 2,402 short lines, 33 KB, no dates.

        No file in the audited portfolio has this shape — zero records AND over 2,000 lines — so
        this signal has no real-world fixture and is pinned synthetically. It exists because the
        `Read` truncation it guards is the whole reason the trimmer exists.
        """
        data = "# Changelog\n\n" + "".join("- bullet %04d\n" % i for i in range(2400))
        self.assertLess(len(data.encode("utf-8")), mod.SEED_PLAUSIBLE_MAX_BYTES,
                        "control: must be UNDER the byte ceiling, or this tests the wrong signal")
        r = evaluate_text(self, "CHANGELOG.md", data)
        self.assertEqual(r.codes, ["GRAMMAR_MISMATCH"], [f.message for f in r.findings])

    def test_a_file_of_exactly_the_read_cap_is_NOT_refused(self):
        data = "".join("line %04d\n" % i for i in range(mod.READ_CAP_LINES))
        self.assertEqual(len(data.splitlines()), mod.READ_CAP_LINES, "control: exactly the cap")
        r = evaluate_text(self, "CHANGELOG.md", data)
        self.assertEqual(r.codes, ["NO_RECORDS"], [f.message for f in r.findings])

    # --- the sentinel exemption, and its limits ---------------------------------------------

    def test_a_sealed_seed_that_grew_past_the_byte_ceiling_is_refused(self):
        """Size was never exemptible, and still is not now that nothing is."""
        data = show(SEED_CL) + ("\nz" * mod.SEED_PLAUSIBLE_MAX_BYTES)
        self.assertIn(mod_seed_sentinel(), data, "control: the fixture still carries the marker")
        r = evaluate_text(self, "CHANGELOG.md", data)
        self.assertEqual(r.codes, ["GRAMMAR_MISMATCH"], [f.message for f in r.findings])

    def test_a_receipt_ledger_that_kept_its_sentinel_while_filling_up_is_still_refused(self):
        """The receipt ledger's half of the conjunction, and it is not hypothetical.

        ../church_growth/HANDOFFS.md carries METHODOLOGY-SEED-SENTINEL today alongside 19 real
        receipts — an adopter who simply never deleted the comment. That file happens to parse, so
        it never reaches this branch; one that did NOT parse would be handed a permanent silent
        exit 0 by a sentinel nobody removed. The seed's own rule is the fix: fresh means the token
        AND no `session:` blocks below. Two producer mutants (dropping this negation, and keying it
        on ```handoff instead) survived until this test existed.
        """
        data = ("# Handoff Receipts\n\n<!-- " + mod_seed_sentinel() + ": fresh receipt ledger -->\n\n" +
                "".join("## Session %d — 2026-08-%02d\n\nsession: S%d\ndate: 2026-08-%02d\nDid a thing.\n\n"
                        % (i, i % 28 + 1, i, i % 28 + 1) for i in range(8)))
        self.assertIn(mod_seed_sentinel(), data, "control: the sentinel really is present")
        self.assertEqual(records_of(data, HF), [], "control: zero records under the fence grammar")
        self.assertGreater(len(probe_hits_of(data, HF)), 0, "control: the probe must fire")
        r = evaluate_text(self, "HANDOFFS.md", data)
        self.assertEqual(r.codes, ["GRAMMAR_MISMATCH"], [f.message for f in r.findings])
        self.assertEqual(r.exit, 3)

    def test_a_receipt_ledger_in_the_wrong_shape_is_refused_by_the_probe(self):
        """The receipt ledger's PROBE, exercised behaviourally rather than by a fixture control.

        An earlier revision of this class lost this test in an edit, leaving `drop HANDOFFS probe`
        killable only by another test's control assertion — coverage by accident. Shape: receipts as
        dated headings instead of ```handoff fences, with NO out-of-fence `session:` lines, so the
        negation is silent and only the probe can fire. No sentinel, so nothing else is in play.
        """
        data = ("# Handoff Receipts\n\nReceipts below.\n\n" +
                "".join("## Session %d — 2026-08-%02d\n\nDid a thing.\n\n" % (i, i % 28 + 1)
                        for i in range(8)))
        self.assertEqual(records_of(data, HF), [], "control: zero records under the fence grammar")
        self.assertEqual(negations_of(data, HF), 0,
                         "control: the NEGATION must be silent, or this tests the wrong signal")
        self.assertGreater(len(probe_hits_of(data, HF)), 0, "control: the probe is the live signal")
        self.assertLess(len(data.encode("utf-8")), mod.SEED_PLAUSIBLE_MAX_BYTES)
        self.assertLess(len(data.splitlines()), mod.READ_CAP_LINES)
        r = evaluate_text(self, "HANDOFFS.md", data)
        self.assertEqual(r.codes, ["GRAMMAR_MISMATCH"], [f.message for f in r.findings])
        self.assertEqual(r.exit, 3)

    def test_bare_session_blocks_with_no_headings_are_refused_by_the_negation_alone(self):
        """The gap that existed while `negations` was computed and then thrown away.

        A receipt ledger written as bare `session:` blocks — no fences for the grammar, and no
        dated headings for the content probe — sat under both size limits and reported NO_RECORDS
        at exit 0, which is F1 intact in the very file the probe had just been extended to cover.
        The seed's own freshness test already knew better: it asks whether any `session:` block has
        been recorded below, and here the answer is yes.
        """
        data = ("# Handoff Receipts\n\nReceipts below.\n\n" +
                "".join("session: S%d\ndate: 2026-08-%02d\nstatus: complete\nDid a thing.\n\n"
                        % (i, i % 28 + 1) for i in range(8)))
        self.assertEqual(records_of(data, HF), [], "control: zero records under the fence grammar")
        self.assertEqual(probe_hits_of(data, HF), [],
                         "control: the PROBE must find nothing, or this tests the wrong signal")
        self.assertLess(len(data.encode("utf-8")), mod.SEED_PLAUSIBLE_MAX_BYTES)
        self.assertLess(len(data.splitlines()), mod.READ_CAP_LINES)
        r = evaluate_text(self, "HANDOFFS.md", data)
        self.assertEqual(r.codes, ["GRAMMAR_MISMATCH"], [f.message for f in r.findings])
        self.assertEqual(r.exit, 3)

    def test_a_documentation_example_quoting_the_sentinel_cannot_seal_a_real_ledger(self):
        """The sentinel check is fence-aware, like both signals beside it.

        A ledger that merely QUOTES the token inside a fenced example — documenting the seed
        format, say — would otherwise be sealed by its own documentation and silenced forever.
        """
        data = ("# Changelog\n\nHow a fresh ledger is marked:\n\n```\n<!-- "
                + mod_seed_sentinel() + ": fresh ledger -->\n```\n\n"
                + "".join("## Release %d — 2026-06-%02d\n\n- did a thing\n\n" % (i, i % 28 + 1)
                          for i in range(6)))
        self.assertIn(mod_seed_sentinel(), data, "control: the token IS in the file")
        self.assertGreater(len(probe_hits_of(data, CL)), 0, "control: the probe fires")
        r = evaluate_text(self, "CHANGELOG.md", data)
        self.assertEqual(r.codes, ["GRAMMAR_MISMATCH"], [f.message for f in r.findings])

    def test_a_seed_that_gained_a_real_entry_in_the_wrong_grammar_is_refused(self):
        """The sentinel is a conjunction, exactly as the seed's own comment states it.

        `starter-kit/CHANGELOG.md:10` says the file is fresh "While this line is present AND there
        are no dated (### YYYY-MM-DD) entries below." An adopter who starts writing entries in
        their own grammar without deleting the comment has a mismatch, not a fresh ledger.
        """
        data = show(SEED_CL) + "\n### 2026-07-27 — did a thing\n\n- Change: x\n"
        self.assertIn(mod_seed_sentinel(), data, "control: the sentinel is still present")
        r = evaluate_text(self, "CHANGELOG.md", data)
        self.assertEqual(r.codes, ["GRAMMAR_MISMATCH"], [f.message for f in r.findings])

    # --- narrowed variants: what makes each clause load-bearing ------------------------------

    def test_NARROWED_a_size_only_implementation_misses_both_real_shapes(self):
        """Delete the probe and the two shapes F1 found survive at adopter-plausible sizes.

        This is the test that makes `content_probe` load-bearing rather than decorative: both
        files F1 actually names are over the byte ceiling, so size alone would have "fixed" F1
        while leaving ../claims-model-starter.wiki (28,300 B) and ../feedback-loop-comparison
        (7,067 B) — both real, both misreported today — exactly as broken.
        """
        for data in (MISMATCH_EMDASH, MISMATCH_TABLE):
            size_only = (len(data.encode("utf-8")) > mod.SEED_PLAUSIBLE_MAX_BYTES
                         or len(data.splitlines()) > mod.READ_CAP_LINES)
            self.assertFalse(size_only, "a size-only rule would report this mismatch as empty")

    def test_NARROWED_a_fence_blind_probe_would_refuse_our_own_shipped_seed(self):
        """Drop fence-awareness from the probe and day one breaks for every adopter."""
        cl = show(SEED_CL)
        blind = [ln for ln in cl.splitlines() if mod.LEDGERS["CHANGELOG.md"].content_probe
                 and mod.LEDGERS["CHANGELOG.md"].content_probe.search(ln)]
        self.assertGreater(len(blind), 0,
                           "control: the seed DOES contain probe-shaped lines inside its fences")
        self.assertEqual(probe_hits_of(cl, CL), [],
                         "fence-aware, those same lines must be invisible")

    def test_NARROWED_an_unanchored_probe_would_flag_dated_prose(self):
        """`search(r'\\d{4}-\\d{2}-\\d{2}')` anywhere on the line is too loose.

        Measured on the real population: the anchored form loses no detection (147/87/11/4 hits on
        the four mismatched adopter ledgers) while dropping to 0 on ordinary dated prose.
        """
        prose = "For instance an entry dated 2026-01-15 sits above one dated 2026-01-14.\n"
        self.assertRegex(prose, r"\d{4}-\d{2}-\d{2}", "control: the line does carry a date")
        self.assertIsNone(mod.LEDGERS["CHANGELOG.md"].content_probe.search(prose),
                          "an anchored probe must ignore prose that merely mentions a date")


if __name__ == "__main__":
    unittest.main(verbosity=2)
