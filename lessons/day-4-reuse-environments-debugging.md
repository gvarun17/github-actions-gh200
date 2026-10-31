# Day 4 — Reuse, Environments, Concurrency, and Debugging

## Reusable workflows

Called with `workflow_call`.

**Called workflow** (`.github/workflows/build.yml`):
```yaml
on:
  workflow_call:
    inputs:
      node-version:
        type: string
        required: true
    secrets:
      npm_token:
        required: false
    outputs:
      artifact-name:
        value: ${{ jobs.build.outputs.name }}
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      name: ${{ steps.n.outputs.name }}
    steps:
      - id: n
        run: echo "name=dist" >> "$GITHUB_OUTPUT"
```

**Caller**:
```yaml
jobs:
  call-build:
    uses: ./.github/workflows/build.yml          # same repo
    # uses: org/repo/.github/workflows/build.yml@v1   # another repo
    with:
      node-version: '20'
    secrets: inherit                              # or map explicitly
```

Rules:
- Reusable workflow is called at the **job** level (`uses:` on a job), not as a step.
- Cannot be combined with `runs-on`, `steps` in the calling job.
- Inputs pass via `with`; use `secrets` or `secrets: inherit`.
- Reference by path+ref: `@main`, `@v1`, or a SHA (SHA safest).
- `env` context of caller is not passed; use inputs.
- Caller permissions can only downgrade the `GITHUB_TOKEN` permissions in the called workflow, not elevate.
- Nesting depth up to 4 levels, max 20 unique reusable workflows per file (check docs).
- Private repo reuse requires access to be enabled in repo Settings → Actions → Access.
- Matrix can be used with reusable workflow calls.

### Reusable workflow vs composite action

| | Reusable workflow | Composite action |
|---|---|---|
| Level | Whole job(s) | Steps within a job |
| Runner | Chooses own `runs-on` | Uses caller's runner |
| Secrets | Passed explicitly | Accessed through inputs |
| Visibility in logs | Separate jobs | One step in the job |
| Defined in | `.github/workflows/` | `action.yml` |

## Starter workflows

Templates offered in "New workflow" UI. Organization starter workflows live in the org's `.github` repo under `workflow-templates/` with a `.properties.json` metadata file.

## Environments and deployment protection

```yaml
jobs:
  deploy:
    environment:
      name: production
      url: https://example.com
```
Environments (repo Settings → Environments):
- **Required reviewers** (up to 6) must approve before job runs.
- **Wait timer** delay.
- **Deployment branches/tags** restrict which refs can deploy.
- **Environment secrets and variables** available only to jobs referencing the environment (and released after approval).
- Custom protection rules via GitHub Apps.
- Available on public repos for all plans; on private repos need Pro/Team/Enterprise.

## Concurrency

```yaml
concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: false
```
- Defined at workflow or job level.
- At most one running and one pending per group; a newer pending run replaces the older pending (unless `cancel-in-progress`).
- Common for deployments (serialize) and PR CI (`cancel-in-progress: true`).

## Manage workflow runs

- **Re-run** all jobs, failed jobs only, or a single job; re-run with **debug logging**.
- **Cancel** a run. Run is cancelled via `cancel-workflow` API; `if: always()` steps are skipped on cancel but `if: cancelled()` runs.
- **Delete** runs and logs; logs retained 90 days by default.
- **Disable/enable** workflows.
- **Status badges**: `https://github.com/<owner>/<repo>/actions/workflows/<file>.yml/badge.svg`.
- **Workflow summaries**: write markdown to `$GITHUB_STEP_SUMMARY`.
- **Annotations** surface errors/warnings on PRs.
- **Required status checks**: workflow job names must match required checks in branch protection; skipped path-filtered workflows can leave a required check "pending."

## Debugging

- Enable **step debug logging**: secret/variable `ACTIONS_STEP_DEBUG=true`.
- Enable **runner diagnostic logging**: `ACTIONS_RUNNER_DEBUG=true`.
- "Re-run jobs → Enable debug logging" sets them for that run.
- `::debug::message` only shows with debug on.
- Download log archive from run page; view raw logs.
- Common errors: wrong indentation, undefined contexts, missing `permissions`, workflow not on default branch, secrets unavailable on fork PRs, path filters excluding changes, expired caches.
- Validate with VS Code GitHub Actions extension or `actionlint`.
- `act` runs workflows locally (third-party).

## Using actions from Marketplace and elsewhere

`uses:` formats:
- `actions/checkout@v4` (public repo, tag)
- `owner/repo/path@ref` (subdirectory action)
- `./.github/actions/my-action` (local, requires `checkout` first)
- `docker://alpine:3.19` (Docker Hub image)

Pinning: tag (mutable), branch (least safe), **full commit SHA (immutable, recommended)**. Org/enterprise policy can allow only GitHub-authored, verified creators, or an allow list.

## Check yourself

1. How is a reusable workflow called, and at which level?
2. How do you pass all secrets to a called workflow?
3. What does `cancel-in-progress` do?
4. Which feature requires manual approval before a job gets environment secrets?
5. How do you enable debug logging, and what are the two variables?
6. Why might a required check hang as "Expected — waiting for status"?
