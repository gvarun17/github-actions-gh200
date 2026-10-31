# Day 7 — Review, Cheat Sheet, and Practice Exam

## Cheat sheet

| Need | Answer |
|---|---|
| Workflow location | `.github/workflows/*.yml` |
| Manual trigger | `workflow_dispatch` |
| Call another workflow | `on: workflow_call` + job-level `uses:` |
| Run after another workflow | `workflow_run` |
| External trigger via API | `repository_dispatch` |
| Cron | `schedule` (UTC, default branch) |
| Persist env to later steps | `echo "A=b" >> $GITHUB_ENV` |
| Step output | `echo "k=v" >> $GITHUB_OUTPUT` |
| Job output | `jobs.<id>.outputs` → `needs.<id>.outputs.k` |
| Job dependency | `needs` |
| Always run | `if: always()` |
| Matrix | `strategy.matrix`; `include`/`exclude`; `fail-fast`; `max-parallel` |
| Dynamic matrix | `fromJSON()` |
| Share files between jobs | upload/download-artifact |
| Speed up dependencies | `actions/cache` (`key`, `restore-keys`) |
| Databases for tests | `services:` |
| Serialize deploys | `concurrency` |
| Approval before deploy | environment required reviewers |
| Cloud auth without secrets | OIDC, `id-token: write` |
| Least privilege token | `permissions:` |
| Docker action runs on | Linux only |
| Composite `run` requires | `shell:` |
| Action metadata file | `action.yml` |
| Version pinning (most secure) | full commit SHA |
| Debug logs | `ACTIONS_STEP_DEBUG`, `ACTIONS_RUNNER_DEBUG` |
| Self-hosted label targeting | `runs-on: [self-hosted, linux, x64]` |
| Limit allowed actions | Org/enterprise Actions policy |
| Migrate CI | GitHub Actions Importer |

## Common traps

1. `GITHUB_TOKEN`-triggered events don't start new runs (except `workflow_dispatch`, `repository_dispatch`).
2. Secrets aren't available to fork PRs; `pull_request_target` is risky.
3. `schedule` and `workflow_dispatch` need the file on the default branch.
4. `branches` + `branches-ignore` conflict; use `!` patterns.
5. Reusable workflows are called at job level; composite actions are called as steps.
6. Setting any `permissions` key zeros the rest.
7. Composite action `run` without `shell` is an error.
8. Cache is branch-scoped (can read from current, base, default).
9. Environment secrets require the job to reference the environment.
10. `outcome` vs `conclusion` differ when `continue-on-error: true`.

## Practice questions

1. Which event lets you start a workflow from the UI with typed inputs?
   A) `repository_dispatch` B) `workflow_dispatch` C) `workflow_call` D) `schedule`
2. A job should run even when a previous job failed. What do you add?
   A) `continue-on-error: false` B) `if: always()` C) `needs: none` D) `retry: true`
3. You need job B to use a value produced by job A. What is needed?
   A) `env` at workflow level B) job output in A and `needs` in B C) cache D) secret
4. Which allows a workflow to authenticate to AWS without storing long-lived keys?
   A) PAT B) OIDC with `id-token: write` C) Deploy key D) Dependabot secret
5. How do you run one workflow from another workflow file as a reusable unit?
   A) `uses:` at step level with a workflow path B) `uses:` at job level with `workflow_call` target C) `include:` D) `needs:`
6. Which runner type can run Docker container actions?
   A) Windows B) macOS C) Linux D) all
7. Which is the most secure way to reference a marketplace action?
   A) `@main` B) `@v1` C) `@<full-sha>` D) no ref
8. What stops two deploys of the same app from running at once?
   A) `max-parallel` B) `concurrency` group C) matrix D) `timeout-minutes`
9. Which file declares inputs/outputs for a custom action?
   A) `workflow.yml` B) `action.yml` C) `package.json` D) `.actionrc`
10. Production deploy must wait for manual approval. Use:
    A) Wait timer in workflow B) Environment with required reviewers C) CODEOWNERS D) `if: manual`
11. Which `GITHUB_TOKEN` permissions config removes all permissions?
    A) `permissions: read-all` B) `permissions: {}` C) `permissions: none-all` D) omit key
12. Where do you add a secret that should be available to many repos in an org?
    A) Repository secret B) Organization secret with repo access policy C) Environment secret D) Codespaces secret
13. Which is a risk of `run: echo "${{ github.event.issue.title }}"`?
    A) Cache miss B) Script injection C) Rate limit D) Timeout
14. A matrix should not cancel other jobs when one fails. Which setting?
    A) `fail-fast: false` B) `max-parallel: 1` C) `continue-on-error` at workflow D) `cancel-in-progress: false`
15. What makes a self-hosted runner execute exactly one job then deregister?
    A) `--once` B) `--ephemeral` C) `--single` D) runner group
16. Which tool helps convert existing Jenkins pipelines?
    A) Actions Importer B) Dependabot C) CodeQL D) Copilot
17. In a composite action, a step with `run:` must include:
    A) `if:` B) `shell:` C) `id:` D) `name:`
18. How do you pass all caller secrets to a reusable workflow?
    A) `secrets: all` B) `secrets: inherit` C) `env: inherit` D) not possible
19. A cache restore falls back to an older cache whose key starts with the same prefix. Which setting?
    A) `fallback-keys` B) `restore-keys` C) `path` D) `retention-days`
20. Which variable enables step debug logs?
    A) `ACTIONS_STEP_DEBUG=true` B) `RUNNER_DEBUG=1` C) `DEBUG=true` D) `ACTIONS_LOG=verbose`

### Answers

1 B · 2 B · 3 B · 4 B · 5 B · 6 C · 7 C · 8 B · 9 B · 10 B · 11 B · 12 B · 13 B · 14 A · 15 B · 16 A · 17 B · 18 B · 19 B · 20 A

## Final-day plan

1. Retake every "Check yourself" list from Days 1–6 aloud (45 min).
2. Take the practice questions untimed, then review misses (45 min).
3. Re-run any lab you found confusing (30 min).
4. Skim GitHub's official skills-measured document and docs pages for any topic you haven't touched.
5. Book the exam; sleep.

## Exam day tips

- Read each question twice: look for words like "most secure," "least effort," "without storing credentials."
- Eliminate options that don't exist (invented keys) first.
- Many questions show YAML with a subtle bug (indentation, missing `needs`, missing `shell`, wrong context). Read the YAML literally.
- Flag and return; don't burn time on one question.
