# Claude Code Skills

Maps Claude Code skills (Matt Pocock's engineering skill set + built-ins) onto
this methodology. Skills are **tools, not phases** — `starter-kit/SESSION_RUNNER.md`
and the per-workstream procedures still drive every session. Use a skill at the
step where it fits; don't reorganize a session around it.

## One-time setup (per adopting project)

Several skills (`triage`, `to-issues`, `to-prd`, `diagnose`,
`improve-codebase-architecture`, `tdd`) read per-repo config from `docs/agents/`:

- `docs/agents/issue-tracker.md` — where issues live (GitHub / GitLab / local markdown)
- `docs/agents/triage-labels.md` — label vocabulary for the triage state machine
- `docs/agents/domain.md` — pointer to `CONTEXT.md` and ADRs

Run `/setup-matt-pocock-skills` once on a new project to scaffold these. The
methodology does not require them; they unlock the skills that need them.

## Skill ↔ phase / workstream map

| Skill | Phase | Workstream(s) | When to use |
|---|---|---|---|
| `/grill-me` | Pre-Flight, Research | All | Stress-test a plan or design before committing |
| `/grill-with-docs` | Pre-Flight, Research | All — esp. RESEARCH_DOCUMENTATION | Same, anchored to CONTEXT.md and ADRs |
| `/to-prd` | Create | ARCHITECTURE, RESEARCH_DOCUMENTATION | Turn current conversation into a PRD |
| `/to-issues` | Create → Implement boundary | ARCHITECTURE, DEVELOPMENT | Decompose a plan into tracer-bullet issues |
| `/triage` | Pre-Flight | DEVELOPMENT, AUDIT | Move incoming issues through the triage state machine |
| `/tdd` | Implement | DEVELOPMENT | Red-green-refactor on a feature or bug fix |
| `/diagnose` | Research, Implement | DEVELOPMENT, AUDIT | Disciplined loop for hard bugs / perf regressions |
| `/improve-codebase-architecture` | Research, Verify & Close | AUDIT, DEVELOPMENT | Find refactor opportunities, informed by CONTEXT.md and ADRs |
| `/simplify` | Verify & Close | All | Review changed code for reuse, quality, efficiency |
| `/review` | Verify & Close | AUDIT, DEVELOPMENT | Review a pull request |
| `/security-review` | Verify & Close | AUDIT, DEVELOPMENT | Security review of pending changes |

## What skills don't replace

- **Phase 0 (Orient).** No skill substitutes for reading `SAFEGUARDS.md`,
  `SESSION_NOTES.md`, and running `git status`.
- **Phase 1B (Claim the Session).** Write the stub before invoking any skill.
- **Phase 3 (Close Out).** `/simplify` and `/review` produce inputs to close-out,
  not the close-out itself.
- **The "1 and done" rule.** A skill producing an artifact (e.g., `/to-issues`)
  does not authorize starting another deliverable in the same session.

A skill that pulls you across a hard gate — e.g., `/to-issues` immediately
followed by `/tdd` — is failure mode #2 (Keep going) wearing a tool costume.
Close out first.
