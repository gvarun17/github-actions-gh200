# Day 1 Recap — Fundamentals, Workflow Syntax, and Triggers

## Key points (10 lines)

1. Workflows are YAML files in `.github/workflows/`; they contain events, jobs, steps, actions, and runners.
2. Jobs run in parallel by default, each on a fresh runner; steps in one job share the filesystem.
3. Jobs don't share a filesystem: pass data via job outputs or artifacts.
4. Common triggers: `push`, `pull_request`, `workflow_dispatch`, `schedule`, `workflow_call`, `workflow_run`, `repository_dispatch`.
5. `pull_request_target` runs in the base branch context with secrets, so it is dangerous with untrusted code.
6. `branches`/`branches-ignore` (and `paths`/`paths-ignore`) can't be combined for one event; use `!` patterns instead.
7. `schedule` uses POSIX cron in UTC, runs from the default branch, minimum interval 5 minutes.
8. Events caused by `GITHUB_TOKEN` don't start new runs, except `workflow_dispatch` and `repository_dispatch`.
9. Each `run` step is a new shell; persist with `$GITHUB_ENV`, `$GITHUB_PATH`, `$GITHUB_OUTPUT`, `$GITHUB_STEP_SUMMARY`.
10. Workflow commands: `::debug::`, `::notice::`, `::warning::`, `::error::`, `::add-mask::`, `::group::`/`::endgroup::`; `set-output` is deprecated.

## Practice questions (new)

**Q1.** A workflow has `on: push: tags: ['v*']` and `paths: ['src/**']`. You push tag `v1.0.0` with no `src` changes. Does it run?
**A1.** Yes. Path filters are not evaluated for tag pushes, so the tag filter alone decides.

**Q2.** You want a manual run with a required dropdown input `env` offering `dev` and `prod`. Which input `type` and keys do you use, and how do you read it?
**A2.** Under `workflow_dispatch.inputs.env` use `type: choice`, `options: [dev, prod]`, `required: true`. Read it with `${{ inputs.env }}` or `${{ github.event.inputs.env }}`.

**Q3.** Step 1 runs `export VERSION=2.0` and step 2 prints `$VERSION`. It's empty. Why, and what's the fix?
**A3.** Each `run` step starts a new shell, so exports don't persist. Use `echo "VERSION=2.0" >> $GITHUB_ENV`.

**Q4.** Your scheduled workflow lives only on a feature branch. Will the cron fire?
**A4.** No. `schedule` triggers run only from the workflow file on the default branch.

**Q5.** How do you hide a runtime-generated token value from logs, and how do you collapse a block of log lines?
**A5.** `echo "::add-mask::$TOKEN"` masks it from later output. Wrap lines with `echo "::group::Title"` and `echo "::endgroup::"` to fold them.

## Hands-on task for today

Run the **Lab 1** workflow: [`.github/workflows/lab-1-hello.yml`](../.github/workflows/lab-1-hello.yml).
Trigger it from the Actions tab (`workflow_dispatch`), then inspect the logs. Try adding a step that sets a variable via `$GITHUB_ENV`, reads it in the next step, writes to `$GITHUB_STEP_SUMMARY`, and emits a `::notice::` annotation.
