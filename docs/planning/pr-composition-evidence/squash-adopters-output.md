# PR3, the adopters: what the candidate's `bin/status` and `bin/sync` do, against upstream's (S396, the rebuilt candidate)

`pr3b-adopters.py` (`docs/planning/pr-composition-evidence/`), run once from this repository's root, 266 s. The candidate is the local ref `pr2b/candidate` at `ea256ad`, upstream's tool is `upstream/main` at `d50ce29`, the fork's `main` was `9232eae`. Each of the 12 adopters is a `--no-local` clone of its committed HEAD; each tool runs from its own clean clone; nothing in a real tree is read through the working directory, written or run. The write set of a real sync is `git status --porcelain` in the clone, never the tool's own report.

## 1. The candidate's tool over each adopter

| adopter | HEAD | layout | tracked files: current / behind / locally modified / missing | seeds present | `--dry-run` exit | files refused | refused: a fork version / in no history (a local edit) | `--dry-run --force` would write | real sync (forced?) wrote | dry run equals the real write set | seeds changed / created | a second plain sync after the commit: exit, paths written | its own hook on the commit |
|---|---|---|---|---|---|---:|---|---:|---:|---|---|---|---|
| model_project_constructor | 24629e6 | new | 14 / 0 / 9 / 0 | 7 | 2 | 9 | 9: 0 | 9 | 9 (forced) | yes | 0 / 0 | 0, 0 | armed: model_project_constructor/.githooks: ok |
| feedback-loop-comparison | 2e77a73 | new | 14 / 0 / 9 / 0 | 6 | 2 | 9 | 9: 0 | 9 | 9 (forced) | yes | 0 / 0 | 0, 0 | none: ok |
| nprcgenekeepr | 0890874d | new | 16 / 0 / 7 / 0 | 7 | 2 | 7 | 6: 1 | 7 | 7 (forced) | yes | 0 / 0 | 0, 0 | none: ok |
| mts-system | 512b3f7 | legacy | 2 / 17 / 4 / 0 | 6 | 2 | 4 | 4: 0 | 22 | 22 (forced) | yes | 0 / 1 | 0, 0 | armed: .githooks: ok |
| vscode_quarto_ext | 89c9f6b4 | new | 16 / 0 / 7 / 0 | 7 | 2 | 7 | 7: 0 | 7 | 7 (forced) | yes | 0 / 0 | 0, 0 | none: ok |
| Philippians | 427e634 | legacy | 2 / 17 / 4 / 0 | 6 | 2 | 4 | 4: 0 | 22 | 22 (forced) | yes | 0 / 1 | 0, 0 | none: ok |
| airqino | f7a0194 | new | 14 / 0 / 9 / 0 | 6 | 2 | 9 | 9: 0 | 9 | 9 (forced) | yes | 0 / 0 | 0, 0 | none: ok |
| chat_verification | 0a8ef90 | new | 14 / 0 / 9 / 0 | 5 | 2 | 9 | 9: 0 | 9 | 9 (forced) | yes | 0 / 0 | 0, 0 | armed: .githooks: its own hook refused: est on top, then stage it and re-commit. * Bypass this once: git commit --no-verify Phase 0 reconcil |
| church_growth | 62f7d8a | new | 14 / 0 / 9 / 0 | 5 | 2 | 9 | 9: 0 | 9 | 9 (forced) | yes | 0 / 0 | 0, 0 | armed: .githooks: its own hook refused: est on top, then stage it and re-commit. * Bypass this once: git commit --no-verify Phase 0 reconcil |
| dalia_martinez_funeral | 5cd7b91 | legacy | 1 / 14 / 0 / 8 | 2 | 0 | 0 | 0: 0 | 25 | 25 (plain) | yes | 0 / 3 | 0, 0 | none: ok |
| claude_work | no commits | none | 0 / 0 / 0 / 23 | 0 | 0 | 0 | 0: 0 | 30 | 30 (plain) | yes | 0 / 7 | 0, 0 | none: ok |
| wsfct | 2823664d | legacy | 2 / 17 / 4 / 0 | 5 | 2 | 4 | 4: 0 | 22 | 22 (forced) | yes | 0 / 1 | 0, 0 | armed: wsfct/.git/hooks: ok |

## 2. Upstream's tool over the same clones

| adopter | candidate's layout | status rows: missing / locally modified / current / behind | `--dry-run` exit | would write | real sync (forced?) wrote | framework files it wrote outside `methodology/` of a migrated project (a second copy) | seeds changed / created (a seed it created beside the adopter's own) | a second plain sync after the commit: exit, paths written |
|---|---|---|---:|---:|---|---:|---|---|
| model_project_constructor | new | 23 / 0 / 0 / 0 | 0 | 23 | 23 (plain) | 23 | 0 / 0 | 0, 0 |
| feedback-loop-comparison | new | 23 / 0 / 0 / 0 | 0 | 23 | 30 (plain) | 23 | 0 / 7 | 0, 0 |
| nprcgenekeepr | new | 23 / 0 / 0 / 0 | 0 | 23 | 29 (plain) | 23 | 0 / 6 | 0, 0 |
| mts-system | legacy | 0 / 4 / 8 / 11 | 2 | 0 | 16 (forced) | 0 | 0 / 1 | 0, 0 |
| vscode_quarto_ext | new | 23 / 0 / 0 / 0 | 0 | 23 | 30 (plain) | 23 | 0 / 7 | 0, 0 |
| Philippians | legacy | 0 / 4 / 8 / 11 | 2 | 0 | 16 (forced) | 0 | 0 / 1 | 0, 0 |
| airqino | new | 23 / 0 / 0 / 0 | 0 | 23 | 30 (plain) | 23 | 0 / 7 | 0, 0 |
| chat_verification | new | 23 / 0 / 0 / 0 | 0 | 23 | 30 (plain) | 23 | 0 / 7 | 0, 0 |
| church_growth | new | 23 / 0 / 0 / 0 | 0 | 23 | 30 (plain) | 23 | 0 / 7 | 0, 0 |
| dalia_martinez_funeral | legacy | 8 / 0 / 3 / 12 | 0 | 20 | 23 (plain) | 0 | 0 / 3 | 0, 0 |
| claude_work | none | 23 / 0 / 0 / 0 | 0 | 23 | 30 (plain) | 0 | 0 / 7 | 0, 0 |
| wsfct | legacy | 0 / 4 / 8 / 11 | 2 | 0 | 16 (forced) | 0 | 0 / 1 | 0, 0 |

## 2b. The fork's own tip over the same clones (dry runs only)

The fork's `bin/sync` is not the candidate's bytes (`df1b7ea` against `8471117`), so this is the operator's own tool, not a control for the candidate's. The point is the exit code: the same clones, a tool whose source history holds the fork's versions.

| adopter | the fork tip's `--dry-run` exit | files it refuses | the candidate's refusals (for comparison) |
|---|---:|---|---:|
| model_project_constructor | 0 | none | 9 |
| feedback-loop-comparison | 0 | none | 9 |
| nprcgenekeepr | 2 | methodology/methodology_trim.py | 7 |
| mts-system | 0 | none | 4 |
| vscode_quarto_ext | 0 | none | 7 |
| Philippians | 0 | none | 4 |
| airqino | 0 | none | 9 |
| chat_verification | 0 | none | 9 |
| church_growth | 0 | none | 9 |
| dalia_martinez_funeral | 0 | none | 0 |
| claude_work | 0 | none | 0 |
| wsfct | 0 | none | 4 |

## 3. Legacy adopters: the candidate's write set against upstream's

| adopter | candidate wrote | upstream wrote | same paths | only the candidate | only upstream | same path, different bytes | paths in either column not explained by a changed source file |
|---|---:|---:|---|---|---|---:|---|
| mts-system | 22 | 16 | NO | 6 | 0 | 13 | none |
| Philippians | 22 | 16 | NO | 6 | 0 | 13 | none |
| dalia_martinez_funeral | 25 | 23 | NO | 2 | 0 | 18 | none |
| claude_work | 30 | 30 | yes | 0 | 0 | 22 | none |
| wsfct | 22 | 16 | NO | 6 | 0 | 13 | none |

## 4. The refused files, one row each: where the adopter's blob is found

| adopter | file | in upstream's history | in the candidate's | in the fork's | the candidate's current blob |
|---|---|---|---|---|---|
| model_project_constructor | `methodology/SESSION_RUNNER.md` | NO | NO | yes | NO |
| model_project_constructor | `methodology/CLAUDE_TEMPLATE.md` | NO | NO | yes | NO |
| model_project_constructor | `methodology/BOOTSTRAP.md` | NO | NO | yes | NO |
| model_project_constructor | `methodology/methodology_dashboard.py` | NO | NO | yes | NO |
| model_project_constructor | `methodology/methodology_trim.py` | NO | NO | yes | NO |
| model_project_constructor | `methodology/context_budget.py` | NO | NO | yes | NO |
| model_project_constructor | `methodology/quality_ratchet.py` | NO | NO | yes | NO |
| model_project_constructor | `methodology/HOW_TO_USE.md` | NO | NO | yes | NO |
| model_project_constructor | `methodology/FRAMEWORK_APPARATUS.md` | NO | NO | yes | NO |
| feedback-loop-comparison | `methodology/SESSION_RUNNER.md` | NO | NO | yes | NO |
| feedback-loop-comparison | `methodology/CLAUDE_TEMPLATE.md` | NO | NO | yes | NO |
| feedback-loop-comparison | `methodology/BOOTSTRAP.md` | NO | NO | yes | NO |
| feedback-loop-comparison | `methodology/methodology_dashboard.py` | NO | NO | yes | NO |
| feedback-loop-comparison | `methodology/methodology_trim.py` | NO | NO | yes | NO |
| feedback-loop-comparison | `methodology/context_budget.py` | NO | NO | yes | NO |
| feedback-loop-comparison | `methodology/quality_ratchet.py` | NO | NO | yes | NO |
| feedback-loop-comparison | `methodology/HOW_TO_USE.md` | NO | NO | yes | NO |
| feedback-loop-comparison | `methodology/FRAMEWORK_APPARATUS.md` | NO | NO | yes | NO |
| nprcgenekeepr | `methodology/SESSION_RUNNER.md` | NO | NO | yes | NO |
| nprcgenekeepr | `methodology/methodology_dashboard.py` | NO | NO | yes | NO |
| nprcgenekeepr | `methodology/methodology_trim.py` | NO | NO | NO | NO |
| nprcgenekeepr | `methodology/context_budget.py` | NO | NO | yes | NO |
| nprcgenekeepr | `methodology/quality_ratchet.py` | NO | NO | yes | NO |
| nprcgenekeepr | `methodology/HOW_TO_USE.md` | NO | NO | yes | NO |
| nprcgenekeepr | `methodology/FRAMEWORK_APPARATUS.md` | NO | NO | yes | NO |
| mts-system | `SESSION_RUNNER.md` | NO | NO | yes | NO |
| mts-system | `BOOTSTRAP.md` | NO | NO | yes | NO |
| mts-system | `methodology_dashboard.py` | NO | NO | yes | NO |
| mts-system | `docs/methodology/HOW_TO_USE.md` | NO | NO | yes | NO |
| vscode_quarto_ext | `methodology/SESSION_RUNNER.md` | NO | NO | yes | NO |
| vscode_quarto_ext | `methodology/methodology_dashboard.py` | NO | NO | yes | NO |
| vscode_quarto_ext | `methodology/methodology_trim.py` | NO | NO | yes | NO |
| vscode_quarto_ext | `methodology/context_budget.py` | NO | NO | yes | NO |
| vscode_quarto_ext | `methodology/quality_ratchet.py` | NO | NO | yes | NO |
| vscode_quarto_ext | `methodology/HOW_TO_USE.md` | NO | NO | yes | NO |
| vscode_quarto_ext | `methodology/FRAMEWORK_APPARATUS.md` | NO | NO | yes | NO |
| Philippians | `SESSION_RUNNER.md` | NO | NO | yes | NO |
| Philippians | `BOOTSTRAP.md` | NO | NO | yes | NO |
| Philippians | `methodology_dashboard.py` | NO | NO | yes | NO |
| Philippians | `docs/methodology/HOW_TO_USE.md` | NO | NO | yes | NO |
| airqino | `methodology/SESSION_RUNNER.md` | NO | NO | yes | NO |
| airqino | `methodology/CLAUDE_TEMPLATE.md` | NO | NO | yes | NO |
| airqino | `methodology/BOOTSTRAP.md` | NO | NO | yes | NO |
| airqino | `methodology/methodology_dashboard.py` | NO | NO | yes | NO |
| airqino | `methodology/methodology_trim.py` | NO | NO | yes | NO |
| airqino | `methodology/context_budget.py` | NO | NO | yes | NO |
| airqino | `methodology/quality_ratchet.py` | NO | NO | yes | NO |
| airqino | `methodology/HOW_TO_USE.md` | NO | NO | yes | NO |
| airqino | `methodology/FRAMEWORK_APPARATUS.md` | NO | NO | yes | NO |
| chat_verification | `methodology/SESSION_RUNNER.md` | NO | NO | yes | NO |
| chat_verification | `methodology/CLAUDE_TEMPLATE.md` | NO | NO | yes | NO |
| chat_verification | `methodology/BOOTSTRAP.md` | NO | NO | yes | NO |
| chat_verification | `methodology/methodology_dashboard.py` | NO | NO | yes | NO |
| chat_verification | `methodology/methodology_trim.py` | NO | NO | yes | NO |
| chat_verification | `methodology/context_budget.py` | NO | NO | yes | NO |
| chat_verification | `methodology/quality_ratchet.py` | NO | NO | yes | NO |
| chat_verification | `methodology/HOW_TO_USE.md` | NO | NO | yes | NO |
| chat_verification | `methodology/FRAMEWORK_APPARATUS.md` | NO | NO | yes | NO |
| church_growth | `methodology/SESSION_RUNNER.md` | NO | NO | yes | NO |
| church_growth | `methodology/CLAUDE_TEMPLATE.md` | NO | NO | yes | NO |
| church_growth | `methodology/BOOTSTRAP.md` | NO | NO | yes | NO |
| church_growth | `methodology/methodology_dashboard.py` | NO | NO | yes | NO |
| church_growth | `methodology/methodology_trim.py` | NO | NO | yes | NO |
| church_growth | `methodology/context_budget.py` | NO | NO | yes | NO |
| church_growth | `methodology/quality_ratchet.py` | NO | NO | yes | NO |
| church_growth | `methodology/HOW_TO_USE.md` | NO | NO | yes | NO |
| church_growth | `methodology/FRAMEWORK_APPARATUS.md` | NO | NO | yes | NO |
| wsfct | `SESSION_RUNNER.md` | NO | NO | yes | NO |
| wsfct | `BOOTSTRAP.md` | NO | NO | yes | NO |
| wsfct | `methodology_dashboard.py` | NO | NO | yes | NO |
| wsfct | `docs/methodology/HOW_TO_USE.md` | NO | NO | yes | NO |

In no history at all (a local edit of the adopter's):

- nprcgenekeepr `methodology/methodology_trim.py`: 49 changed lines against the fork tip's copy, 298 against the candidate's; the adopter's last commits on it: `e90a9b99 2026-10-22 chore(methodology): S1032 -- put the project's SESSION_NOTES.md ledger spec back into methodology/methodology_trim.py (v1.8.1)`; `3bc8a1e8 2026-10-22 chore(methodology): S1032 sync -- bin/sync --force from the methodology checkout 515b3a7e (v4.2-2285): 7 files updated`

## 4b. Hooks: which adopters' own hook refused the sync commit, and what it said

| adopter | the candidate's sync commit | upstream's sync commit |
|---|---|---|
| chat_verification | its own hook refused: est on top, then stage it and re-commit. * Bypass this once: git commit --no-verify Phase 0 reconcile-on-read backfills anything bypassed, so the ledger is true again on the next session's Orient. The hook is the fast path, not the guarantee. * Opt out for good: delete methodology/CHANGELOG.md and record the decision in CLAUDE.md. "Too small to log" is the failure mode, not an exception (the session runner's FM #27). | its own hook refused: quality-ratchet: REFUSED — half-migrated: this commit's index holds the manifest at .quality-gates.json AND at methodology/.quality-gates.json ✗ the ratchet will not guess which one is the manifest — finish or revert the move · Bypass once: git commit --no-verify — recorded, not exempt: the manifest's git history shows the commit and the dashboard reports it. |
| church_growth | its own hook refused: est on top, then stage it and re-commit. * Bypass this once: git commit --no-verify Phase 0 reconcile-on-read backfills anything bypassed, so the ledger is true again on the next session's Orient. The hook is the fast path, not the guarantee. * Opt out for good: delete methodology/CHANGELOG.md and record the decision in CLAUDE.md. "Too small to log" is the failure mode, not an exception (the session runner's FM #27). | its own hook refused: quality-ratchet: REFUSED — half-migrated: this commit's index holds the manifest at .quality-gates.json AND at methodology/.quality-gates.json ✗ the ratchet will not guess which one is the manifest — finish or revert the move · Bypass once: git commit --no-verify — recorded, not exempt: the manifest's git history shows the commit and the dashboard reports it. |

## 5. Instrument audits

| adopter | dry runs left the clone clean (4 runs) | the tool's refusals equal the history rule (a blob in neither the candidate's history nor its current one) | the plain real run's refusal equals the dry run's |
|---|---|---|---|
| model_project_constructor | yes | yes | yes |
| feedback-loop-comparison | yes | yes | yes |
| nprcgenekeepr | yes | yes | yes |
| mts-system | yes | yes | yes |
| vscode_quarto_ext | yes | yes | yes |
| Philippians | yes | yes | yes |
| airqino | yes | yes | yes |
| chat_verification | yes | yes | yes |
| church_growth | yes | yes | yes |
| dalia_martinez_funeral | yes | yes | n/a (no refusal) |
| claude_work | yes | yes | n/a (no refusal) |
| wsfct | yes | yes | yes |

## 6. Two legacy fixtures, each synced by both tools, trees diffed

Source files that differ between upstream's tip and the candidate (basenames, distributed set): 22: ARCHITECTURE_WORKSTREAM.md, AUDIT_WORKSTREAM.md, BOOTSTRAP.md, CHANGELOG.md, CLAUDE_TEMPLATE.md, DEVELOPMENT_WORKSTREAM.md, FRAMEWORK_APPARATUS.md, HANDOFFS.md, HOW_TO_USE.md, INHERITED_CODEBASE_FAMILIARIZATION_CAMPAIGN.md, ITERATIVE_METHODOLOGY.md, RECOMMENDED_SKILLS.md, RESEARCH_EXHAUSTIVE_VERIFICATION_CAMPAIGN.md, SAFEGUARDS.md, SESSION_RUNNER.md, TEMPLATE_CAMPAIGN.md, TEMPLATE_WORKSTREAM.md, context_budget.py, methodology_dashboard.py, methodology_trim.py, quality-gates.json, quality_ratchet.py.

**(a) an empty project** (`git init` and one commit).

| | upstream's tool | the candidate's tool |
|---|---:|---:|
| exit of the plain sync | 0 | 0 |
| paths written | 30 | 30 |
| layout the tool reports | - | legacy (default: the project has no methodology files yet) |
| seeds created | 7 | 7 |

Same list of paths: **yes**; only upstream's: none; only the candidate's: none; a `methodology/` directory in the candidate's tree: no.
Paths whose bytes differ: 22; of those, not explained by a changed source file: **none**; changed source files whose installed copy does not differ: none.

`diff -rq` of the two trees (22 lines):

```
Files A/.quality-gates.json and B/.quality-gates.json differ
Files A/BOOTSTRAP.md and B/BOOTSTRAP.md differ
Files A/CHANGELOG.md and B/CHANGELOG.md differ
Files A/CLAUDE_TEMPLATE.md and B/CLAUDE_TEMPLATE.md differ
Files A/HANDOFFS.md and B/HANDOFFS.md differ
Files A/RECOMMENDED_SKILLS.md and B/RECOMMENDED_SKILLS.md differ
Files A/SAFEGUARDS.md and B/SAFEGUARDS.md differ
Files A/SESSION_RUNNER.md and B/SESSION_RUNNER.md differ
Files A/context_budget.py and B/context_budget.py differ
Files A/docs/methodology/FRAMEWORK_APPARATUS.md and B/docs/methodology/FRAMEWORK_APPARATUS.md differ
Files A/docs/methodology/HOW_TO_USE.md and B/docs/methodology/HOW_TO_USE.md differ
Files A/docs/methodology/ITERATIVE_METHODOLOGY.md and B/docs/methodology/ITERATIVE_METHODOLOGY.md differ
Files A/docs/methodology/workstreams/ARCHITECTURE_WORKSTREAM.md and B/docs/methodology/workstreams/ARCHITECTURE_WORKSTREAM.md differ
Files A/docs/methodology/workstreams/AUDIT_WORKSTREAM.md and B/docs/methodology/workstreams/AUDIT_WORKSTREAM.md differ
Files A/docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md and B/docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md differ
Files A/docs/methodology/workstreams/INHERITED_CODEBASE_FAMILIARIZATION_CAMPAIGN.md and B/docs/methodology/workstreams/INHERITED_CODEBASE_FAMILIARIZATION_CAMPAIGN.md differ
Files A/docs/methodology/workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_CAMPAIGN.md and B/docs/methodology/workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_CAMPAIGN.md differ
Files A/docs/methodology/workstreams/TEMPLATE_CAMPAIGN.md and B/docs/methodology/workstreams/TEMPLATE_CAMPAIGN.md differ
Files A/docs/methodology/workstreams/TEMPLATE_WORKSTREAM.md and B/docs/methodology/workstreams/TEMPLATE_WORKSTREAM.md differ
Files A/methodology_dashboard.py and B/methodology_dashboard.py differ
Files A/methodology_trim.py and B/methodology_trim.py differ
Files A/quality_ratchet.py and B/quality_ratchet.py differ
```

**(b) a project holding upstream's current files, its 7 seeds edited by the adopter** (SESSION_NOTES.md, CHANGELOG.md, HANDOFFS.md, ROADMAP.md, .context-budget.json, .quality-gates.json, .gitattributes).

| | upstream's tool | the candidate's tool |
|---|---:|---:|
| exit of the plain sync | 0 | 0 |
| paths written | 0 | 19 |
| seeds changed / created | 0 / 0 | 0 / 0 |
| needed `--force` | NO | NO |

The candidate wrote: `BOOTSTRAP.md`, `CLAUDE_TEMPLATE.md`, `RECOMMENDED_SKILLS.md`, `SAFEGUARDS.md`, `SESSION_RUNNER.md`, `context_budget.py`, `docs/methodology/FRAMEWORK_APPARATUS.md`, `docs/methodology/HOW_TO_USE.md`, `docs/methodology/ITERATIVE_METHODOLOGY.md`, `docs/methodology/workstreams/ARCHITECTURE_WORKSTREAM.md`, `docs/methodology/workstreams/AUDIT_WORKSTREAM.md`, `docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md`, `docs/methodology/workstreams/INHERITED_CODEBASE_FAMILIARIZATION_CAMPAIGN.md`, `docs/methodology/workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_CAMPAIGN.md`, `docs/methodology/workstreams/TEMPLATE_CAMPAIGN.md`, `docs/methodology/workstreams/TEMPLATE_WORKSTREAM.md`, `methodology_dashboard.py`, `methodology_trim.py`, `quality_ratchet.py`.
Paths written that are not a changed tracked source file: **none**; changed tracked source files not written: **none**; changed seed sources left as the adopter's own: ['CHANGELOG.md', 'HANDOFFS.md', 'quality-gates.json']; a `methodology/` directory in the candidate's tree: no.

`diff -rq` of the two trees (19 lines):

```
Files A/BOOTSTRAP.md and B/BOOTSTRAP.md differ
Files A/CLAUDE_TEMPLATE.md and B/CLAUDE_TEMPLATE.md differ
Files A/RECOMMENDED_SKILLS.md and B/RECOMMENDED_SKILLS.md differ
Files A/SAFEGUARDS.md and B/SAFEGUARDS.md differ
Files A/SESSION_RUNNER.md and B/SESSION_RUNNER.md differ
Files A/context_budget.py and B/context_budget.py differ
Files A/docs/methodology/FRAMEWORK_APPARATUS.md and B/docs/methodology/FRAMEWORK_APPARATUS.md differ
Files A/docs/methodology/HOW_TO_USE.md and B/docs/methodology/HOW_TO_USE.md differ
Files A/docs/methodology/ITERATIVE_METHODOLOGY.md and B/docs/methodology/ITERATIVE_METHODOLOGY.md differ
Files A/docs/methodology/workstreams/ARCHITECTURE_WORKSTREAM.md and B/docs/methodology/workstreams/ARCHITECTURE_WORKSTREAM.md differ
Files A/docs/methodology/workstreams/AUDIT_WORKSTREAM.md and B/docs/methodology/workstreams/AUDIT_WORKSTREAM.md differ
Files A/docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md and B/docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md differ
Files A/docs/methodology/workstreams/INHERITED_CODEBASE_FAMILIARIZATION_CAMPAIGN.md and B/docs/methodology/workstreams/INHERITED_CODEBASE_FAMILIARIZATION_CAMPAIGN.md differ
Files A/docs/methodology/workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_CAMPAIGN.md and B/docs/methodology/workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_CAMPAIGN.md differ
Files A/docs/methodology/workstreams/TEMPLATE_CAMPAIGN.md and B/docs/methodology/workstreams/TEMPLATE_CAMPAIGN.md differ
Files A/docs/methodology/workstreams/TEMPLATE_WORKSTREAM.md and B/docs/methodology/workstreams/TEMPLATE_WORKSTREAM.md differ
Files A/methodology_dashboard.py and B/methodology_dashboard.py differ
Files A/methodology_trim.py and B/methodology_trim.py differ
Files A/quality_ratchet.py and B/quality_ratchet.py differ
```

