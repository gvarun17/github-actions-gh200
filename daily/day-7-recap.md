# Day 7 Recap — Final Readiness Checklist

## Key points (10 lines)

1. Triggers: `workflow_dispatch` (UI/API, typed inputs), `workflow_call` (reusable), `workflow_run`, `repository_dispatch`, and `schedule` (UTC, default branch only).
2. Data flow: step output via `$GITHUB_OUTPUT`, env persistence via `$GITHUB_ENV`, job output exposed under `jobs.<id>.outputs` and read with `needs.<id>.outputs.<key>`.
3. Control flow: `needs`, `if: always()/failure()/cancelled()`, matrix with `include`/`exclude`/`fail-fast`/`max-parallel`, dynamic matrix with `fromJSON()`.
4. Sharing and speed: artifacts move files between jobs; `actions/cache` (`key`, `restore-keys`) speeds dependencies; `services:` provides databases for tests.
5. Reuse: reusable workflows are called at job level (`uses:` plus `secrets: inherit`); composite actions are called as steps and every `run` needs `shell:`.
6. Action types: JavaScript, Docker (Linux runners only), and composite; metadata always lives in `action.yml`.
7. Deployment safety: `concurrency` groups serialize deploys; environments add required reviewers, wait timers, and environment-scoped secrets.
8. Security: explicit least-privilege `permissions:` (any key zeros the rest), pin actions to a full SHA, avoid script injection by passing untrusted input via `env`, be careful with `pull_request_target`.
9. Enterprise: runner groups, ephemeral self-hosted runners, allowed-actions policies, org secrets with repo access policy, OIDC (`id-token: write`) instead of long-lived cloud keys.
10. Debugging and migration: `ACTIONS_STEP_DEBUG` and `ACTIONS_RUNNER_DEBUG`, `outcome` vs `conclusion` with `continue-on-error`, and GitHub Actions Importer for migrating Jenkins/other CI.

## Final-readiness checklist

Tick these yourself; they are for your own self-assessment.

- [ ] I can write a workflow from scratch (trigger, jobs, steps, `runs-on`) without notes.
- [ ] I can explain the difference between `env`, `vars`, `secrets`, and `github` contexts and where each is available.
- [ ] I can pass data step → step, and job → job, and know the file commands used.
- [ ] I can build a matrix with `include`/`exclude` and explain `fail-fast`.
- [ ] I know when to use artifacts versus cache.
- [ ] I can choose between a reusable workflow and a composite action and state how each is called.
- [ ] I can describe the three action types and their runner limitations.
- [ ] I can configure an environment with required reviewers and environment secrets.
- [ ] I can set minimal `permissions:` and explain the "any key zeros the rest" rule.
- [ ] I can explain how OIDC works and which claims a cloud trust policy checks.
- [ ] I can list the script-injection risk and the `env` mitigation.
- [ ] I know runner types, labels, runner groups, and ephemeral runners.
- [ ] I know the policy hierarchy (enterprise → org → repo) and allowed-actions options.
- [ ] I know the debug variables and how to re-run with debug logging.
- [ ] I scored at least 85% on the Day 7 practice exam (untimed), and reviewed every miss.
- [ ] I re-ran each lab workflow (labs 1-4 and 6, plus the Day 5 action exercises).
- [ ] I skimmed GitHub's official skills-measured document for gaps.
- [ ] Exam booked, ID ready, test environment checked, sleep planned.

## Last-minute reminders

- Read each question twice for qualifiers: "most secure", "least effort", "without storing credentials".
- Eliminate invented keys and options first, then read YAML literally for subtle bugs (indentation, missing `needs`, missing `shell`, wrong context).
- Flag and return; do not burn time on one question.

## Hands-on task for today

Do a final lap of the lab workflows: run [`lab-1-hello.yml`](../.github/workflows/lab-1-hello.yml), [`lab-3-matrix-artifacts.yml`](../.github/workflows/lab-3-matrix-artifacts.yml), [`lab-4-reusable-caller.yml`](../.github/workflows/lab-4-reusable-caller.yml), and [`lab-6-oidc-permissions.yml`](../.github/workflows/lab-6-oidc-permissions.yml) via workflow_dispatch (or push). For each, predict the result before opening the run, then check the logs and note any prediction you got wrong, and review those topics once more.
