# P15: the three test files that read a moved path, one line each.  Rscript p15-r-one.R   (from a checkout's root)
Sys.setenv(NOT_CRAN = "true")
suppressMessages(pkgload::load_all(".", quiet = TRUE))
for (f in c("test_rbuildignore.R", "test_handoffsReceiptPlacement.R", "test_workflowPathsIgnore.R")) {
  r <- as.data.frame(testthat::test_file(file.path("tests/testthat", f), reporter = "silent", stop_on_failure = FALSE))
  cat(f, "tests", nrow(r), "passed", sum(r$passed), "failed", sum(r$failed), "error", sum(r$error), "skipped", sum(r$skipped), "\n")
}
