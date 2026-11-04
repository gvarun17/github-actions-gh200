# Day 4 Recap — Reuse, Environments, Concurrency, Debugging

## Key points (10 lines)

1. Reusable workflows use `on: workflow_call` with typed `inputs`, `secrets`, and `outputs`; they are called with `uses:` at the **job** level, never as a step.
2. A calling job cannot also define `runs-on` or `steps`; pass data with `with:` and secrets with `secrets:` (explicit map) or `secrets: inherit`.
3. Reference reusable workflows as `./.github/workflows/x.yml` (same repo) or `org/repo/.github/workflows/x.yml@ref`; a full SHA is safest. The caller's `env` is not passed.
4. The called workflow's `GITHUB_TOKEN` permissions can only be downgraded by the caller, never elevated. Nesting is limited to 4 levels; matrix works on reusable calls.
5. Reusable workflow = whole jobs with its own runner; composite action = steps inside the caller's job on the caller's runner (defined in `action.yml`).
6. Starter workflows live in an org's `.github` repo under `workflow-templates/` with a `.properties.json` metadata file.
7. Environments provide required reviewers (up to 6), wait timers, deployment branch/tag rules, and environment-scoped secrets/variables released only after approval.
8. `concurrency.group` allows one running + one pending run; a newer pending run replaces the older one. `cancel-in-progress: true` cancels the running one (good for PR CI); `false` serializes (good for deploys).
9. Run management: re-run all/failed/single job (optionally with debug logging), cancel (`cancelled()` steps still run, `always()`... see docs), `$GITHUB_STEP_SUMMARY`, annotations, badges; logs kept 90 days by default.
10. Debugging: `ACTIONS_STEP_DEBUG=true` (step debug) and `ACTIONS_RUNNER_DEBUG=true` (runner diagnostics); `::debug::` shows only with debug on. `uses:` pinning: tag < branch risk-wise; full commit SHA is immutable and recommended.

## Practice questions (new)

**Q1.** A caller job has `uses: ./.github/workflows/build.yml` and also `runs-on: ubuntu-latest`. What happens?
**A1.** The workflow is invalid. A job that calls a reusable workflow cannot define `runs-on` (or `steps`); the called workflow's own jobs choose their runners.

**Q2.** The reusable workflow's job needs `contents: write`, but the caller sets `permissions: contents: read`. What permission does the called job get?
**A2.** `contents: read`. The caller can only keep or reduce the token permissions passed to the called workflow, not elevate them.

**Q3.** Two pushes to `main` trigger a deploy workflow with `concurrency: {group: deploy, cancel-in-progress: false}`, and a third push arrives while the first is still running and the second is pending. What happens to the second run?
**A3.** The second (pending) run is cancelled and replaced by the third. At most one run is running and one pending per group; the first run continues untouched.

**Q4.** A job references `environment: production` that has two required reviewers and a secret `DB_PASS` scoped to that environment. When can the job read `DB_PASS`?
**A4.** Only after the required reviewer approval is granted (and the branch passes any deployment-branch rule). Until then the job waits and the environment secret is not available.

**Q5.** You need to see `::debug::` output for a single failed run without changing repo settings permanently. What do you do?
**A5.** Use "Re-run jobs" and tick "Enable debug logging" (this sets step and runner debug for that run only); alternatively set `ACTIONS_STEP_DEBUG` / `ACTIONS_RUNNER_DEBUG` as secrets or variables.

## Hands-on task for today

Run the **Lab 4** workflow: [`.github/workflows/lab-4-reusable-caller.yml`](../.github/workflows/lab-4-reusable-caller.yml), which calls [`reusable-greet.yml`](../.github/workflows/reusable-greet.yml).
Trigger it, then try: adding a new `input` and an `output` to the reusable workflow and reading the output in a dependent caller job, switching between explicit `secrets:` and `secrets: inherit`, adding a `concurrency` group and starting two runs to watch pending replacement, and re-running with debug logging enabled.
