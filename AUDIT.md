# Content Audit — GH-200 Course

Audit date: 2026-11-27. Baseline commit: `6481e40`.
Reference: GH-200 study guide, skills measured as of **January 2026** (Microsoft Learn), and GitHub Docs.

## 1. Summary

| Item | Before audit | After audit |
|---|---|---|
| Lessons | 7 | 7 (deepened) |
| Exam domains covered | 4 (old outline) | 5 (January 2026 outline) |
| Runnable labs | 5 workflows + 1 reusable + 1 composite action | 11 workflows + 1 reusable + 3 actions (composite, JS, Docker) |
| Mermaid diagrams | 0 | 1+ per lesson |
| Troubleshooting tables | 0 | 1 per lesson |
| Practice issues | 0 | 28 (see [practice-issues.yaml](practice-issues.yaml)) |
| Factual errors found | — | 9 (see section 3) |
| Outdated items found | — | 8 (see section 4) |

## 2. Topic inventory

| # | Path | Title | Depth before | Main gaps before audit | Exercises before |
|---|---|---|---|---|---|
| 1 | `lessons/day-1-fundamentals-and-triggers.md` | Fundamentals, syntax, triggers | Adequate | No diagram; no event-payload walkthrough; no `workflow_run`/`repository_dispatch` example; no YAML anchors (new in Jan 2026 outline); no troubleshooting | Lab 1, 6 check questions |
| 2 | `lessons/day-2-contexts-variables-secrets.md` | Contexts, expressions, variables, secrets | Adequate | Error on `secrets` in `if:`; no static vs runtime evaluation; no context-availability table; no REST API for secrets/variables (new in outline) | Lab 2, 6 check questions |
| 3 | `lessons/day-3-jobs-matrix-artifacts-cache.md` | Jobs, matrix, artifacts, cache, services | Adequate | Outdated reusable-workflow limits; outdated cache limit text; artifact retention rule incomplete; no matrix-output behaviour; no retention REST API | Lab 3, 6 check questions |
| 4 | `lessons/day-4-reuse-environments-debugging.md` | Reuse, environments, concurrency, debugging | Adequate | Error on `always()` with cancel; outdated nesting limits; plan rule for environments incomplete; no `queue: max`; no templates vs reusable vs composite matrix; no disable vs delete | Lab 4, 6 check questions |
| 5 | `lessons/day-5-authoring-actions.md` | Authoring custom actions | Adequate | `node20` is removed; no `node24`; no Docker action lab; no immutable actions/lockfile; Marketplace rules incomplete | `actions/README.md` exercises only |
| 6 | `lessons/day-6-enterprise-runners-security.md` | Enterprise, runners, security, OIDC | Adequate | Outdated billing model; no IP allow lists; no runner-image/preinstalled software topic; no attestation verify step; no `ubuntu-slim`; no SHA-pinning policy detail | Lab 6, 7 check questions |
| 7 | `lessons/day-7-review-and-practice.md` | Review and practice | Adequate | Cheat sheet uses old 4-domain outline; no anchors/immutable/attestation questions | 20 practice questions |
| — | `LOCAL-SETUP.md` | macOS setup | Deep | Node example uses `node20` | — |
| — | `actions/README.md` | Action exercises | Shallow | `node20`; no solution scaffold | 5 exercises |
| — | `daily/*.md` | Daily recaps | Adequate | No change needed except outdated facts carried from lessons | 5 Q&A each |

## 3. Factual errors corrected

| # | Location | Old statement | Correct statement | Source |
|---|---|---|---|---|
| 1 | Day 4 → Manage runs | "`if: always()` steps are skipped on cancel but `if: cancelled()` runs" | `always()` returns true even when the run is cancelled. Both `always()` and `cancelled()` steps run after a cancel. Use `!cancelled()` to run on success or failure but not on cancel. | [Expressions — status check functions](https://docs.github.com/en/actions/reference/workflows-and-actions/expressions#status-check-functions) |
| 2 | Day 2 → Contexts | "`secrets` cannot be used in `if:` at job level directly" | Secrets cannot be referenced directly in **any** `if:` condition (job or step). Map the secret to `env` and test the env var in a step `if:`. | [Using secrets in a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets) |
| 3 | Day 3 + Day 4 | Reusable workflows: "nesting up to 4 levels, max 20 per file" | github.com: up to **10 levels** (caller + 9 reusable) and **50** unique reusable workflows per run tree. GHES keeps 4 and 20. | [Changelog Nov 2025](https://github.blog/changelog/2025-11-06-new-releases-for-github-actions-november-2025), [Reusable workflows reference](https://docs.github.com/actions/reference/reusable-workflows-reference) |
| 4 | Day 3 → Artifacts | "max 90 on free, up to 400 on some plans" | Public repos: 1–90 days. Private/internal repos: 1–400 days. Default 90. | [Artifact and log retention](https://docs.github.com/en/organizations/managing-organization-settings/configuring-the-retention-period-for-github-actions-artifacts-and-logs-in-your-organization) |
| 5 | Day 3 → Caching | "Repo cache limit: 10 GB" (hard) | 10 GB is the included default. Since Nov 2025 admins can raise the limit (Pro/Team/Enterprise, billed). Eviction now runs hourly. | [Changelog Nov 2025](https://github.blog/changelog/2025-11-20-github-actions-cache-size-can-now-exceed-10-gb-per-repository/) |
| 6 | Day 4 → Environments | "Available on public repos for all plans; on private repos need Pro/Team/Enterprise" | Private/internal: environments, environment secrets and deployment branches need Pro/Team/Enterprise. On Free, Pro and Team, required reviewers and wait timers work **only in public repos** (private/internal needs Enterprise). Max 6 required reviewers. | [Managing environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments) |
| 7 | Day 4 → Concurrency | "At most one running and one pending" (only behaviour) | Still the default. Since May 2026, `queue: max` lets up to 100 runs wait in a group (only with `cancel-in-progress: false`). | [Changelog May 2026](https://github.blog/changelog/2026-05-07-github-actions-concurrency-groups-now-allow-larger-queues) |
| 8 | Day 6 → Billing | "Self-hosted runners are free" (unqualified) | Free today, but GitHub announced a $0.002/min platform charge (Dec 2025) and then postponed it. Watch the billing docs. | [Changelog Dec 2025](https://github.blog/changelog/2025-12-16-coming-soon-simpler-pricing-and-a-better-experience-for-github-actions/) |
| 9 | README → Exam facts | 4 domains | January 2026 outline has **5 domains** (adds "Secure and optimize automation", 10–15%). | [GH-200 study guide](https://learn.microsoft.com/credentials/certifications/resources/study-guides/gh-200) |

## 4. Outdated items updated

| # | Item | Old | New |
|---|---|---|---|
| 1 | JavaScript action runtime | `using: node20` | `using: node24` (Node 20 removed from runners on 2026-09-23) |
| 2 | `actions/checkout` | `@v4` | `@v7` (v7, Jun 2026, refuses fork PR head checkout in `pull_request_target` by default) |
| 3 | `actions/setup-python` | `@v5` | `@v6` |
| 4 | `actions/upload-artifact` / `download-artifact` | `@v4` / `@v4` | `@v7` / `@v8` |
| 5 | `actions/cache` | `@v4` | `@v5` |
| 6 | `workflow_dispatch` inputs | limit not stated | up to 25 inputs |
| 7 | Exam outline | not in course | YAML anchors, immutable actions, lockfiles, editor tooling, REST retention APIs, runner images |
| 9 | `pull_request_target` | "dangerous" only | Blocked by default in public repos from 2026-12-02 unless an Actions event policy allows it |
| 10 | Concurrency | 1 running + 1 pending only | `queue: max` (May 2026) |
| 11 | Supply chain | SHA pin advice | Require SHA pinning policy (Aug 2025), immutable releases (Oct 2025), lockfiles (Oct 2026) |
| 8 | Included usage | minutes only | Docs now show included compute as a dollar allowance on the limits page; minute table still in billing docs — verify before exam |

## 5. Study-guide vs docs conflict

The January 2026 study guide lists "YAML anchors and aliases (`&`, `*`, and merge `<<`)". GitHub's implementation supports anchors and aliases but **not** merge keys (YAML 1.2). The course teaches the docs behaviour and flags it as a likely exam distractor.

## 6. Items not verified

| Item | Reason |
|---|---|
| Exact exam price in INR | Price depends on the country. Check the Microsoft Learn exam page before you book. |
| Latest patch tags and commit SHAs of `actions/*` | This session could not query those repos. Examples use major tags. Practice issue "Pin every action to a SHA" asks you to resolve them. |
| Self-hosted runner platform charge final date | Postponed; no new date published at audit time. |
| Latest majors of `actions/attest-build-provenance` (v3) and `aws-actions/configure-aws-credentials` (v5) | Could not query the repos; confirm on their release pages. |
| `examples/day-6/terraform-oidc/main.tf` | `terraform validate` not run (Terraform binary not available in the build session). Run `terraform init -backend=false && terraform validate`. |
| Docker action image build | Docker daemon not available in the build session; `entrypoint.sh` was tested directly with `sh`. Lab 5 builds it on GitHub. |
