import re, sys, collections
EARLY = re.compile(r'(?<!\|)\|\s*(?:grep\b[^|]*?-[A-Za-z]*q[A-Za-z]*(?=\s|$)|grep\b[^|]*?-m\s*\d|head\b|sed\b[^|]*\bq\b)')
HEREDOC = re.compile(r"(?<!<)<<(?!<)-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
def outside(s):
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
lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
logical, i = [], 0
while i < len(lines):
    start, buf = i + 1, lines[i]
    while buf.endswith("\\") and i + 1 < len(lines):
        i += 1; buf = buf[:-1] + " " + lines[i].lstrip()
    logical.append((start, buf)); i += 1
    m = HEREDOC.search(buf)
    if m:
        while i < len(lines) and lines[i].strip() != m.group(2): i += 1
        i += 1
rows = []
for n, s in logical:
    st = s.strip()
    if st.startswith("#"): continue
    mask = outside(s)
    ms = [m for m in EARLY.finditer(s) if mask[m.start()]]
    if not ms: continue
    # producer = text of the pipeline segment before the first early consumer's pipe (back to the start of the command)
    m = ms[0]
    head = s[:m.start()]
    # last command separator before the pipe
    seg = re.split(r'(?:&&|\|\||;|\bthen\b|\bdo\b|\{|\()\s*', head)[-1].strip()
    seg = re.sub(r'^(?:if|elif|while|until|!)\s+', '', seg)
    rows.append((n, seg, s.strip()))
c = collections.Counter()
for n, seg, s in rows:
    if re.match(r'echo\s+"\$[A-Za-z_][A-Za-z0-9_]*"$', seg): k = 'echo "$VAR"'
    elif re.match(r'echo\b', seg): k = 'echo other'
    elif re.match(r'printf\b', seg): k = 'printf'
    elif '|' in seg: k = 'chain(' + seg.split()[0] + ')'
    else: k = 'command'
    c[k] += 1
    if len(sys.argv) > 2 and k == sys.argv[2]: print(n, '::', s[:200])
for k, v in c.most_common(): print(v, k)
print("TOTAL", len(rows))
