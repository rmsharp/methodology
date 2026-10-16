#!/usr/bin/env python3
"""Audit a rewrite of a PR body against the body it replaces (S334).

usage: audit_text.py OLD.md NEW.md      (for example original-body.md body.md)

Prints, for the rewrite:
  - byte sizes of both texts;
  - outward-text tokens that must not appear (session numbers, backlog ids, fork-learning references,
    decision ids);
  - numbers and `code spans` in OLD that are missing from NEW (a rewrite must not lose a figure or a
    name) and those only in NEW (check that each is intended);
  - how often the word "red" appears (it was shorthand for "a proof that reports FAIL" and was dropped);
  - the offset of the first use of each key term (a definition must come before its first use);
  - sentences that contain a pronoun or demonstrative that can be ambiguous (read each one).
It reads two files and writes nothing. It is a prompt for a human or a fresh reader, not a verdict.
"""
import re
import sys

old = open(sys.argv[1], encoding="utf-8").read()
new = open(sys.argv[2], encoding="utf-8").read()
print("bytes old", len(old.encode()), "new", len(new.encode()))
print("banned:", re.findall(r"\bS\d{2,3}\b|\bBL-\d+|[Ff]ork [Ll]earning|\bD\d\b|session \d+", new))


def numbers(t):
    return set(re.findall(r"\d[\d,.]*\d|\d", t))


def spans(t):
    return set(re.findall(r"`([^`]+)`", t))


print("numbers in old, missing from new:", sorted(numbers(old) - numbers(new)))
print("numbers only in new:", sorted(numbers(new) - numbers(old)))
print("code spans in old, missing from new:", sorted(spans(old) - spans(new)))
print("code spans only in new:", sorted(spans(new) - spans(old)))
print("'red' occurrences (offsets):", [m.start() for m in re.finditer(r"\bred\b", new)])

print("\nfirst occurrence offset of each term (its definition must come first; -1 = absent):")
for term in ["ledger", "record", "shard", "proof", "L1", "L2", "L3", "adopter", "stub", "claim", "finalize",
             "record 0", "timing rule", "record grammar", "LIVE", "SHARD", "stub_marker", "TRIM_VERSION",
             "receipt", "close-out", "--reverify", "header", "footer", "trim commit", "running trimmer"]:
    print("  %-16s %s" % (term, new.find(term)))

print("\nsentences with ambiguous-pronoun candidates:")
text = re.sub(r"```.*?```", "", new, flags=re.S)
for s in re.split(r"(?<=[.!?:;])\s+|\n+", text):
    if re.search(r"\b(It|it|Its|its|They|they|Their|their|This|this|That|that|Those|those|These|these|which|Which)\b", s):
        print("  -", s.strip()[:230])
