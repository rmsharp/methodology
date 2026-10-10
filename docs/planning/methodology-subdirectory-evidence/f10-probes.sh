#!/bin/bash
# BL-101 F10 and F11 (S290): what R and vsce DO with the pattern lists the tool now reads. Nothing here touches an adopter or this
# repository: it builds toy projects in the directory given and runs the real programs on them.
#   usage: bash f10-probes.sh <an empty scratch directory>
# Needs R (R CMD build; the figures in the record are R 4.6.1) and, for the second half, node/npx and the network
# (npx fetches @vscode/vsce 3.6.0, the version whose source was read: `package.js` matches each line with minimatch and
# `{ dot: true }`, no `matchBase`).
set -u
D="${1:?usage: bash f10-probes.sh <an empty scratch directory>}"
mkdir -p "$D" && cd "$D" || exit 2
echo "== R: $(R --version 2>&1 | head -1)"
rm -rf pkgx && mkdir -p pkgx/R pkgx/methodology pkgx/docsdir
cat > pkgx/DESCRIPTION <<'EOF'
Package: pkgx
Type: Package
Title: Probe
Version: 0.0.1
Description: Probe of Rbuildignore semantics.
License: GPL-3
EOF
echo 'f <- function() 1' > pkgx/R/f.R
echo 'export(f)' > pkgx/NAMESPACE
echo a > pkgx/FOO.txt; echo a > pkgx/foo2.txt; echo a > pkgx/methodology/KEEP.txt; echo a > pkgx/docsdir/inner.txt
echo a > pkgx/SESSION_RUNNER.md; echo a > pkgx/ALPHA.md; echo a > pkgx/BETA.md
build() {  # the files of the package that the case is about, as R packaged them
  rm -f pkgx_0.0.1.tar.gz
  R CMD build pkgx --no-build-vignettes > /dev/null 2>&1
  echo "   built (exit $?): $(tar tzf pkgx_0.0.1.tar.gz | grep -E 'FOO|foo2|inner|SESSION|ALPHA|BETA' | sed 's#^pkgx/##' | tr '\n' ' ')"
}
echo "1. matching is case-insensitive: ^foo\\.txt\$ against FOO.txt (FOO.txt absent = excluded)"
printf '^foo\\.txt$\n^foo2\\.txt$\n' > pkgx/.Rbuildignore; build
echo "2. a line that matches a directory covers what is under it: ^docsdir\$ (inner.txt absent = excluded)"
printf '^docsdir$\n' > pkgx/.Rbuildignore; build
echo "3. a line that starts with # is a regular expression, not a comment: '# |ALPHA' (ALPHA.md absent = excluded; BETA.md present)"
printf '# |ALPHA\n' > pkgx/.Rbuildignore; build
echo "4. the framework file where it is now, covered: ^SESSION_RUNNER.*\\.md\$"
printf '^SESSION_RUNNER.*\\.md$\n' > pkgx/.Rbuildignore; build
echo "5. after the move to methodology/ the same line no longer covers it (methodology/SESSION_RUNNER.md is packaged)"
rm -f pkgx/ALPHA.md pkgx/BETA.md; mv pkgx/SESSION_RUNNER.md pkgx/methodology/SESSION_RUNNER.md; build
echo "6. one more line, ^methodology\$, covers the new directory (0 methodology/ entries packaged: the moved file and KEEP.txt are both out)"
echo '^methodology$' >> pkgx/.Rbuildignore
rm -f pkgx_0.0.1.tar.gz; R CMD build pkgx --no-build-vignettes > /dev/null 2>&1
echo "   built (exit $?): methodology/ entries packaged: $(tar tzf pkgx_0.0.1.tar.gz | grep -c methodology)"

echo "== vsce 3.6.0: a bare name in .vscodeignore is the project root's"
rm -rf ext && mkdir -p ext/methodology && cd ext || exit 2
cat > package.json <<'EOF'
{"name":"probe","displayName":"probe","version":"0.0.1","publisher":"probe","engines":{"vscode":"^1.80.0"},"repository":{"type":"git","url":"https://example.invalid/x.git"},"license":"MIT","main":"./extension.js","activationEvents":[]}
EOF
echo "// x" > extension.js; echo "# probe" > README.md; echo "MIT" > LICENSE
echo a > SESSION_RUNNER.md; echo a > CHANGELOG.md; echo a > methodology/SESSION_RUNNER.md
echo "7. .vscodeignore = SESSION_RUNNER.md, with a copy in methodology/ (the moved file is listed = packaged):"
printf 'SESSION_RUNNER.md\n' > .vscodeignore
npx --yes @vscode/vsce@3.6.0 ls --no-dependencies 2>&1 | grep -v 'npm warn' | sed 's/^/   /'
echo "8. .vscodeignore = SESSION_RUNNER.md and methodology/** (the moved file is not listed):"
printf 'SESSION_RUNNER.md\nmethodology/**\n' > .vscodeignore
npx --yes @vscode/vsce@3.6.0 ls --no-dependencies 2>&1 | grep -v 'npm warn' | sed 's/^/   /'
