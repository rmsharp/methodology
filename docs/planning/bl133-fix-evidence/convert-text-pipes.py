#!/usr/bin/env python3
"""BL-133: move every `echo`/`printf` producer of an early-exiting `grep` into a here-string.

    python3 convert-text-pipes.py bin/tests.sh            # dry run: prints each line before and after
    python3 convert-text-pipes.py bin/tests.sh --write    # rewrites the file in place

WHAT IT CONVERTS. The lines come from the suite's OWN scanner (Test 45, Rule C), extracted from the
file it is about to change, so the converter and the test that holds the result cannot disagree
about which lines are sites. On each flagged line, every top-level pipe into an early-exiting
`grep` whose immediate producer is exactly `echo "ARG"` or `printf '%s\\n' "ARG"` becomes the
consumer followed by `<<< "ARG"`:

    echo "$OUT" | grep -q 'x' && pass ...     ->  grep -q 'x' <<< "$OUT" && pass ...
    if echo "$OUT" | grep -q 'x'; then        ->  if grep -q 'x' <<< "$OUT"; then
    && ! printf '%s\\n' "$OUT" | grep -q 'x'  ->  && ! grep -q 'x' <<< "$OUT"

The shell writes a here-string's text before `grep` starts, so there is no pipe for `grep -q` to
close early and nothing to kill (BL-133). `echo ARG` and `printf '%s\\n' ARG` both write ARG and one
newline, as `<<<` does.

A flagged line may be the first physical line of a backslash-continued command (the pipeline is on
that first line, the `&& pass` and `|| fail` arms on the next); the trailing backslash is kept.

WHAT IT REFUSES, and reports instead of guessing: a producer that is not exactly one of the two
forms above (`echo -n`, two arguments, another format), a consumer that is not `grep`. Exit status
0 only if every flagged line was converted and both self-checks passed.

THE SELF-CHECKS. (1) The scanner, run on the result, flags 0 lines. (2) Every changed line is read
as shell words (`shlex`, with `&&`, `||`, `;`, `|` and `<<<` as words of their own); after the moved
words are taken out of both versions (`echo ARG |` from the old line, `<<< ARG` from the new), the
two word sequences must be identical, so an edit outside the moved text is caught.
"""
import re, shlex, subprocess, sys, tempfile, os


def extract_scanner(text):
    m = re.search(r"cat > \"\$SCAN45\" <<'PY45'\n(.*?)\nPY45\n", text, re.S)
    if not m:
        sys.exit("convert-text-pipes: Test 45's scanner (heredoc PY45) was not found in the file")
    return m.group(1)


def run_scanner(scanner_src, path):
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(scanner_src)
        sp = f.name
    try:
        out = subprocess.run([sys.executable, sp, path], capture_output=True, text=True, check=True).stdout
    finally:
        os.unlink(sp)
    sites = [int(m.group(1)) for m in re.finditer(r"^FLAKE-SITE (\d+) ", out, re.M)]
    total = int(re.search(r"^FLAKE-TOTAL (\d+)", out, re.M).group(1))
    assert total == len(sites)
    return sites


def outside(s):
    """The scanner's own mask: True where a character is not inside quotes or `$( )`."""
    mask, stack, i, n = [False] * len(s), ['top'], 0, len(s)
    while i < n:
        c, ctx = s[i], stack[-1]
        if ctx == 'sq':
            if c == "'": stack.pop()
        elif c == '\\' and i + 1 < n:
            i += 2; continue
        elif c == "'" and ctx != 'dq': stack.append('sq')
        elif c == '"':
            if ctx == 'dq': stack.pop()
            else: stack.append('dq')
        elif c == '$' and s.startswith('$(', i):
            stack.append('subst'); i += 2; continue
        elif c == ')' and ctx == 'subst': stack.pop()
        elif ctx == 'top': mask[i] = True
        i += 1
    return mask


EARLY = re.compile(r'(?<!\|)\|\s*(?:grep\b[^|]*?-[A-Za-z]*q[A-Za-z]*(?=\s|$)|grep\b[^|]*?-m\s*\d|head\b|sed\b[^|]*\bq\b)')
ARG = r'"(?:[^"\\]|\\.)*"'
KW = r'(?:(?:then|do|else|if|elif|while|until|!)\s+)*'
STAGE = re.compile(r'^(?P<kw>' + KW + r')(?P<prod>(?:echo\s+(?P<a1>' + ARG + r')|printf\s+\'%s\\n\'\s+(?P<a2>' + ARG + r')))\s*$')


def convert_line(line):
    """Return (new_line, refusals). Edits run right to left, so offsets to their left stay valid."""
    tail = ""
    m = re.search(r'\s*\\$', line)
    if m:
        line, tail = line[:m.start()], line[m.start():]
    refused = []
    mask = outside(line)
    for m in reversed([m for m in EARLY.finditer(line) if mask[m.start()]]):
        i = m.start() - 1
        while i >= 0 and not (mask[i] and line[i] in '|;&({'):
            i -= 1
        stage_text = line[i + 1:m.start()]
        if not re.match(r'\s*' + KW + r'(?:echo|printf)\b', stage_text):
            continue  # this early consumer's producer is not echo/printf: not this converter's
        st = STAGE.match(stage_text.strip())
        if not st:
            refused.append("producer is not exactly echo \"ARG\" or printf '%s\\n' \"ARG\": " + stage_text.strip())
            continue
        cstart = m.start() + 1
        while line[cstart] in ' \t':
            cstart += 1
        if not line.startswith('grep', cstart):
            refused.append("consumer is not grep: " + line[cstart:cstart + 30])
            continue
        # the consumer runs to the first top-level control operator, a comment, or the end
        j = cstart
        while j < len(line):
            if mask[j] and (line.startswith('&&', j) or line.startswith('||', j) or line[j] in ';|)'
                            or (line[j] == '#' and line[j - 1] in ' \t')):
                break
            j += 1
        consumer = line[cstart:j]
        trailing = consumer[len(consumer.rstrip()):]
        arg = st.group('a1') or st.group('a2')
        prod_start = i + 1 + stage_text.index(st.group('prod'))
        line = line[:prod_start] + consumer.rstrip() + ' <<< ' + arg + trailing + line[j:]
        mask = outside(line)
    return line + tail, refused


def words(s):
    s = re.sub(r'\s*\\$', '', s)
    lex = shlex.shlex(s, posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    lex.commenters = ''
    return list(lex)


def drop(ws, pattern_of):
    """Remove each run of words that pattern_of(ws, k) says starts at k; returns the rest."""
    out, k = [], 0
    while k < len(ws):
        n = pattern_of(ws, k)
        if n:
            k += n
        else:
            out.append(ws[k]); k += 1
    return out


def old_run(ws, k):  # `echo ARG |` or `printf %s\n ARG |`
    if ws[k] == 'echo' and k + 2 < len(ws) and ws[k + 2] == '|': return 3
    if ws[k] == 'printf' and k + 3 < len(ws) and ws[k + 1] == '%s\\n' and ws[k + 3] == '|': return 4
    return 0


def new_run(ws, k):  # `<<< ARG`
    return 2 if ws[k] == '<<<' and k + 1 < len(ws) else 0


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    write = "--write" in sys.argv[2:]
    text = open(path, encoding="utf-8").read()
    scanner = extract_scanner(text)
    sites = run_scanner(scanner, path)
    lines = text.split("\n")
    changed, refusals = [], []
    for n in sites:
        old = lines[n - 1]
        new, refused = convert_line(old)
        if refused or new == old:
            refusals.append((n, "; ".join(refused) or "nothing converted", old))
            continue
        lines[n - 1] = new
        changed.append((n, old, new))
    for n, old, new in changed:
        print("%5d  - %s" % (n, old.strip()))
        print("       + %s" % new.strip())
    for n, why, old in refusals:
        print("REFUSED %d: %s\n        %s" % (n, why, old.strip()))
    print("converted %d of %d flagged lines; refused %d" % (len(changed), len(sites), len(refusals)))
    if refusals:
        sys.exit(2)
    # self-check 1: the scanner, run on the result, flags nothing
    with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False, encoding="utf-8") as f:
        f.write("\n".join(lines))
        tmp = f.name
    try:
        left = run_scanner(scanner, tmp)
    finally:
        os.unlink(tmp)
    print("self-check 1, the scanner on the result: %d flagged line(s)%s" % (len(left), " " + str(left) if left else ""))
    # self-check 2: only the moved words differ
    bad = 0
    for n, old, new in changed:
        a, b = drop(words(old), old_run), drop(words(new), new_run)
        if a != b:
            bad += 1
            print("SELF-CHECK 2 MISMATCH at line %d:\n  old without the moved words: %s\n  new without them:            %s" % (n, a, b))
    print("self-check 2, moved words only: %d mismatch(es) in %d changed line(s)" % (bad, len(changed)))
    if left or bad:
        sys.exit(3)
    if write:
        open(path, "w", encoding="utf-8").write("\n".join(lines))
        print("wrote %s" % path)
    else:
        print("dry run: nothing written (pass --write)")


if __name__ == "__main__":
    main()
