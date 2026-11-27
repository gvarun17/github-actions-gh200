#!/usr/bin/env bash
# Trigger workflows from the CLI. Usage: ./dispatch.sh OWNER/REPO
set -euo pipefail
REPO="${1:?usage: dispatch.sh OWNER/REPO}"

# workflow_dispatch with typed inputs
gh workflow run "Lab 1b - Triggers, Inputs, Anchors" --repo "$REPO" \
  -f target=staging -f dry-run=false -f replicas=3

# repository_dispatch with a custom event type and payload
gh api "repos/$REPO/dispatches" \
  -f event_type=deploy \
  -F 'client_payload[env]=staging'

gh run list --repo "$REPO" --limit 5
