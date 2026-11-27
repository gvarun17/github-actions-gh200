#!/usr/bin/env bash
# Debugging commands for workflow runs. Usage: ./debug-cheatsheet.sh OWNER/REPO
set -euo pipefail
REPO="${1:?usage: debug-cheatsheet.sh OWNER/REPO}"

gh run list --repo "$REPO" --limit 10                 # recent runs
RUN_ID=$(gh run list --repo "$REPO" --limit 1 --json databaseId --jq '.[0].databaseId')
gh run view "$RUN_ID" --repo "$REPO"                  # jobs and status
gh run view "$RUN_ID" --repo "$REPO" --log-failed     # only failed step logs
gh run rerun "$RUN_ID" --repo "$REPO" --failed --debug  # re-run failed jobs with debug logging

# Turn on debug logging for every run (remove when done)
# gh variable set ACTIONS_STEP_DEBUG --body true --repo "$REPO"
# gh variable set ACTIONS_RUNNER_DEBUG --body true --repo "$REPO"

# Pause vs remove a workflow
# gh workflow disable "Lab 1 - Hello Actions" --repo "$REPO"
# gh workflow enable  "Lab 1 - Hello Actions" --repo "$REPO"
