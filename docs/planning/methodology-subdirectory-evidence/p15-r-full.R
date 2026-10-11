# P15: the adopter's own clean regression read (its CLAUDE.md "Clean regression read"), one CSV row per test file.
#   Rscript p15-r-full.R <out.csv>        run from the root of a checkout of the adopter
args <- commandArgs(TRUE)
out <- args[1]
Sys.setenv(NOT_CRAN = "true")
suppressMessages(pkgload::load_all(".", quiet = TRUE))
t0 <- Sys.time()
r <- as.data.frame(testthat::test_dir("tests/testthat", reporter = "silent", stop_on_failure = FALSE))
r$error <- as.integer(r$error)
agg <- aggregate(cbind(nb, passed, failed, skipped, error, warning) ~ file, data = r, FUN = sum)
write.csv(agg, out, row.names = FALSE)
cat("FULL tests", sum(r$nb), "passed", sum(r$passed), "failed", sum(r$failed), "error", sum(r$error),
    "skipped", sum(r$skipped), "warning", sum(r$warning), "files", length(unique(r$file)),
    "secs", round(as.numeric(difftime(Sys.time(), t0, units = "secs"))), "\n")
