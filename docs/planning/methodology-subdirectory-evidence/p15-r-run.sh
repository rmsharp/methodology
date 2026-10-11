#!/bin/bash
# P15: run an R script in a CLONE of the adopter against the real project's renv library (read only: nothing installs).
#   p15-r-run.sh <clone dir> <script.R> <out prefix> [script args...]
# A clone is at another path, so renv would look for another (empty) library; RENV_PATHS_LIBRARY names the real one's root
# (renv appends macos/R-4.6/<arch> itself). Writes <out prefix>.txt and <out prefix>.done (the exit code).
export RENV_PATHS_LIBRARY=$HOME/Library/Caches/org.R-project.R/R/renv/library/nprcgenekeepr-e7e04aee
clone=$1; script=$2; out=$3; shift 3
cd "$clone" || exit 3
Rscript "$script" "$@" > "$out.txt" 2>&1
echo $? > "$out.done"
