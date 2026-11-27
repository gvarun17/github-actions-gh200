#!/bin/sh
set -eu
WHO="${1:-World}"
NOW="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "${GREETING_PREFIX:-Hello}, ${WHO} (from a container)"
echo "pwd=$(pwd)  (GitHub mounts the workspace at /github/workspace)"
echo "time=${NOW}" >> "$GITHUB_OUTPUT"
echo "### Docker action greeted ${WHO}" >> "$GITHUB_STEP_SUMMARY"
