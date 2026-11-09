# GitHub Actions (GH-200) — 7-Day Course

Goal: pass GH-200 in one week, ~2–3 hours per day, with a runnable lab each day.

| Day | Topic | Lesson | Lab |
|---|---|---|---|
| 1 | Fundamentals, workflow syntax, triggers | [day-1](lessons/day-1-fundamentals-and-triggers.md) | [lab-1](.github/workflows/lab-1-hello.yml) |
| 2 | Contexts, expressions, variables, secrets | [day-2](lessons/day-2-contexts-variables-secrets.md) | [lab-2](.github/workflows/lab-2-contexts.yml) |
| 3 | Jobs: matrix, needs, outputs, artifacts, caching, services, containers | [day-3](lessons/day-3-jobs-matrix-artifacts-cache.md) | [lab-3](.github/workflows/lab-3-matrix-artifacts.yml) |
| 4 | Consuming and managing workflows: reuse, environments, concurrency, debugging | [day-4](lessons/day-4-reuse-environments-debugging.md) | [lab-4](.github/workflows/lab-4-reusable-caller.yml) |
| 5 | Authoring custom actions | [day-5](lessons/day-5-authoring-actions.md) | [actions/](actions/) |
| 6 | Enterprise: runners, policies, security, OIDC | [day-6](lessons/day-6-enterprise-runners-security.md) | [lab-6](.github/workflows/lab-6-oidc-permissions.yml) |
| 7 | Review, practice exam, cheat sheet | [day-7](lessons/day-7-review-and-practice.md) | — |

Prefer working from your Mac? See [LOCAL-SETUP.md](LOCAL-SETUP.md) for Homebrew, `gh`, `act`, and per-day local lab steps.

## Exam facts (verify on the official page)

- GH-200, Pearson VUE via Microsoft Learn, passing score 700, about $99 USD, around 100–120 minutes.
- Approximate domains: author and maintain workflows (~20–25%), consume workflows (~20–25%), author and maintain actions (~15–20%), manage Actions in the enterprise (~20–25%). Confirm against GitHub's official skills-measured document.

## Using this repo

Push it to a repo on GitHub (private repos get a monthly free-minute allowance; public repos run on standard runners free). The `.github/workflows/lab-*.yml` files are manually triggerable (`workflow_dispatch`) so they won't burn minutes until you run them from the Actions tab. Read each lesson, then run its lab and inspect the logs.

Daily routine: read the lesson (60–90 min), run the lab (30 min), answer the "Check yourself" questions, commit your notes.
