# Day 1 — Fundamentals, Workflow Syntax, and Triggers

## Core components

| Component | Description |
|---|---|
| **Workflow** | YAML automation file in `.github/workflows/` |
| **Event** | Activity that triggers a workflow |
| **Job** | Set of steps run on one runner; jobs run in parallel by default |
| **Step** | A shell command (`run`) or an action (`uses`) |
| **Action** | Reusable unit of work |
| **Runner** | Machine that executes a job |

Each job gets a fresh runner environment. Steps within a job share the filesystem. Jobs do not share a filesystem; pass data with outputs or artifacts.

## Anatomy of a workflow

```yaml
name: CI                      # display name
run-name: CI for ${{ github.actor }}
on:                           # triggers
  push:
    branches: [main]
  pull_request:
permissions:
  contents: read
env:
  NODE_ENV: test
defaults:
  run:
    shell: bash
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - name: Say hi
        run: echo "Hello"
        env:
          GREETING: hi
```

Key job-level keys: `runs-on`, `needs`, `if`, `strategy`, `env`, `permissions`, `outputs`, `environment`, `concurrency`, `container`, `services`, `timeout-minutes`, `continue-on-error`, `defaults`.
Key step-level keys: `name`, `id`, `if`, `uses`, `with`, `run`, `shell`, `env`, `working-directory`, `continue-on-error`, `timeout-minutes`.

## Triggers (events)

### Common events

| Event | Fires when |
|---|---|
| `push` | Commits or tags pushed |
| `pull_request` | PR opened, synchronize, reopened (default activity types) |
| `pull_request_target` | Like PR but runs in the context of the **base** branch with secrets: dangerous with untrusted code |
| `workflow_dispatch` | Manual run (supports `inputs`) |
| `schedule` | Cron (UTC), minimum every 5 minutes; runs on default branch |
| `workflow_call` | Called by another workflow (reusable workflow) |
| `workflow_run` | After another workflow completes/requested |
| `repository_dispatch` | External API call with custom event type |
| `release`, `issues`, `issue_comment`, `create`, `delete`, `fork`, `watch` | Matching repo events |
| `check_run`, `check_suite`, `deployment`, `status` | Check/deployment related |

### Filters

```yaml
on:
  push:
    branches: [main, 'release/**']
    branches-ignore: [...]      # cannot combine with branches
    tags: ['v*']
    paths: ['src/**']
    paths-ignore: ['docs/**']
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
```

- `branches` and `branches-ignore` cannot be used together for the same event; use `!` negation patterns inside `branches` instead. Same for `paths`.
- Glob: `*` (no slash), `**` (any), `?`, `[]`, `!` negate.
- Path filters are ignored for tag pushes; `paths` won't be evaluated for pushes of tags.
- `schedule` uses POSIX cron: `'30 5 * * 1-5'` (5:30 UTC weekdays).

### workflow_dispatch inputs

```yaml
on:
  workflow_dispatch:
    inputs:
      env:
        description: Target
        type: choice
        options: [dev, prod]
        required: true
      debug:
        type: boolean
        default: false
```
Access via `${{ inputs.env }}` or `github.event.inputs.env`.

### Important behaviors

- Workflow files must exist on the **default branch** to run for `schedule`, `workflow_dispatch` in the UI, `issue_comment`, etc.
- Events triggered by `GITHUB_TOKEN` generally **do not trigger new workflow runs** (prevents recursion), with exceptions `workflow_dispatch` and `repository_dispatch`. Use a PAT or GitHub App token to chain.
- Workflows from forks: `pull_request` from forks gets a read-only token and no secrets by default; approvals may be required for first-time contributors.
- Disable/enable workflows from the Actions tab; use `[skip ci]` / `[ci skip]` / `[no ci]` / `[skip actions]` in commit message to skip push/PR runs.

## Runners (intro)

`runs-on: ubuntu-latest | windows-latest | macos-latest` or specific versions (`ubuntu-24.04`). Self-hosted: `runs-on: [self-hosted, linux, x64]`. Larger runners exist on paid plans.

## Shell and run steps

- Default shell: bash on Linux/macOS, pwsh on Windows. Override with `shell:`.
- Multi-line: `run: |`.
- Each `run` step is a new shell process; env vars set with `export` do not persist. Persist with `echo "NAME=value" >> $GITHUB_ENV`. Add to PATH with `$GITHUB_PATH`. Step outputs with `echo "key=value" >> $GITHUB_OUTPUT`. Job summary markdown with `$GITHUB_STEP_SUMMARY`.

## Workflow commands

- `::debug::`, `::notice::`, `::warning::`, `::error::` annotations.
- `::add-mask::value` masks a value in logs.
- `::group::` / `::endgroup::` fold log sections.
- The old `set-output` and `save-state` commands were deprecated; use environment files.

## Check yourself

1. Where must workflow files live? What format?
2. Which event types trigger a workflow from PRs by default?
3. Why won't a push made with `GITHUB_TOKEN` trigger another workflow? Which events are exceptions?
4. Which file do you append to in order to set an env var for later steps?
5. What time zone does `schedule` use?
6. Can you use `branches` and `branches-ignore` together?
