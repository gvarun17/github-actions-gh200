# GitHub Actions (GH-200) — 7-Day Course

Goal: pass GH-200 in one week, ~2–3 hours per day, with runnable labs and practice issues each day.

| Day | Topic | Lesson | Labs | Examples |
|---|---|---|---|---|
| 1 | Fundamentals, workflow syntax, triggers, YAML anchors | [day-1](lessons/day-1-fundamentals-and-triggers.md) | [lab-1](.github/workflows/lab-1-hello.yml), [lab-1b](.github/workflows/lab-1b-triggers-anchors.yml) | [examples/day-1](examples/day-1/) |
| 2 | Contexts, expressions, variables, secrets, `GITHUB_TOKEN` | [day-2](lessons/day-2-contexts-variables-secrets.md) | [lab-2](.github/workflows/lab-2-contexts.yml), [lab-2b](.github/workflows/lab-2b-expressions-injection.yml) | [examples/day-2](examples/day-2/) |
| 3 | Jobs: matrix, needs, outputs, artifacts, caching, services | [day-3](lessons/day-3-jobs-matrix-artifacts-cache.md) | [lab-3](.github/workflows/lab-3-matrix-artifacts.yml), [lab-3b](.github/workflows/lab-3b-dynamic-matrix-services.yml) | [examples/day-3](examples/day-3/) |
| 4 | Reuse, templates, environments, concurrency, debugging | [day-4](lessons/day-4-reuse-environments-debugging.md) | [lab-4](.github/workflows/lab-4-reusable-caller.yml), [lab-4b](.github/workflows/lab-4b-environment-concurrency.yml) | [examples/day-4](examples/day-4/) |
| 5 | Authoring custom actions (composite, JavaScript, Docker) | [day-5](lessons/day-5-authoring-actions.md) | [lab-5](.github/workflows/lab-5-custom-actions.yml), [actions/](actions/) | [actions/](actions/) |
| 6 | Enterprise: runners, policies, security, OIDC, attestations | [day-6](lessons/day-6-enterprise-runners-security.md) | [lab-6](.github/workflows/lab-6-oidc-permissions.yml), [lab-6b](.github/workflows/lab-6b-attest-and-pin.yml) | [examples/day-6](examples/day-6/) |
| 7 | Review, cheat sheet, 35 practice questions | [day-7](lessons/day-7-review-and-practice.md) | — | — |

Every lesson has: overview, Mermaid diagrams, how it works, real-world example, hands-on steps, common mistakes, troubleshooting table, exam notes, official references, and "Check yourself" questions.

Prefer working from your Mac? See [LOCAL-SETUP.md](LOCAL-SETUP.md) for Homebrew, `gh`, `act`, and per-day local lab steps.
Content audit and corrections: [AUDIT.md](AUDIT.md).

## Exam facts (skills measured as of January 2026 — verify on the official page)

- GH-200 via Microsoft Learn (Pearson VUE). 100 minutes. Passing score 700. Valid 2 years. Price depends on country (about USD 99).
- Five domains:

| Domain | Weight |
|---|---|
| Author and manage workflows | 20–25% |
| Consume and troubleshoot workflows | 15–20% |
| Author and maintain actions | 15–20% |
| Manage GitHub Actions for the enterprise | 20–25% |
| Secure and optimize automation | 10–15% |

Official: [GH-200 study guide](https://learn.microsoft.com/credentials/certifications/resources/study-guides/gh-200).

## How to use practice issues

Each topic has 3–5 GitHub issues labelled `practice`. Each issue is a hands-on task with a scenario, steps, acceptance criteria, hidden hints and a stretch goal.

1. Open the issues for the day (links in the progress table below). Start with `difficulty:beginner`.
2. Assign the issue to yourself and create a branch: `practice/<issue-number>-<short-name>`.
3. Do the task. Put your work in `solutions/<topic-slug>/<issue-number>/` (workflows that must run go in `.github/workflows/` with a `practice-` prefix).
4. Tick the acceptance criteria in the issue. Link the run URL in a comment.
5. Close the issue with your PR (`Closes #<n>`).

Labels: `practice`, `topic:day-N`, `difficulty:beginner|intermediate|advanced`, `type:lab|build|debug|design|quiz`. Milestones: one per day.
Issue source of truth: [practice-issues.yaml](practice-issues.yaml). Regenerate with `python3 scripts/create_issues.py --dry-run` and then without `--dry-run`.

## Progress

| Day | Topic | Practice issues | Lesson read | Labs run | Issues closed |
|---|---|---|---|---|---|
| 1 | Fundamentals, triggers, anchors | [topic:day-1](https://github.com/gvarun17/github-actions-gh200/issues?q=is%3Aissue+label%3Atopic%3Aday-1) | ☐ | ☐ | 0 / 4 |
| 2 | Contexts, variables, secrets | [topic:day-2](https://github.com/gvarun17/github-actions-gh200/issues?q=is%3Aissue+label%3Atopic%3Aday-2) | ☐ | ☐ | 0 / 4 |
| 3 | Jobs, matrix, artifacts, cache | [topic:day-3](https://github.com/gvarun17/github-actions-gh200/issues?q=is%3Aissue+label%3Atopic%3Aday-3) | ☐ | ☐ | 0 / 4 |
| 4 | Reuse, environments, concurrency | [topic:day-4](https://github.com/gvarun17/github-actions-gh200/issues?q=is%3Aissue+label%3Atopic%3Aday-4) | ☐ | ☐ | 0 / 4 |
| 5 | Custom actions | [topic:day-5](https://github.com/gvarun17/github-actions-gh200/issues?q=is%3Aissue+label%3Atopic%3Aday-5) | ☐ | ☐ | 0 / 4 |
| 6 | Enterprise, security, OIDC | [topic:day-6](https://github.com/gvarun17/github-actions-gh200/issues?q=is%3Aissue+label%3Atopic%3Aday-6) | ☐ | ☐ | 0 / 5 |
| 7 | Review and mock exam | [topic:day-7](https://github.com/gvarun17/github-actions-gh200/issues?q=is%3Aissue+label%3Atopic%3Aday-7) | ☐ | — | 0 / 3 |

See also [PROGRESS.md](PROGRESS.md).

## Using this repo

This repo is public, so labs run on standard GitHub-hosted runners for free. The `.github/workflows/lab-*.yml` files are manually triggerable (`workflow_dispatch`), so they do not run until you start them from the Actions tab or with `gh workflow run "<name>"`. Read each lesson, run its labs, inspect the logs, then work through the practice issues.

Daily routine: read the lesson (60–90 min), run the labs (30 min), close the day's practice issues (45–60 min), answer "Check yourself", commit your notes.

Lint before you push: `actionlint` (config in `.github/actionlint.yaml`).
