#!/usr/bin/env python3
"""List Actions secret and variable NAMES for a repo and its environments.

Uses the GitHub REST API through the `gh` CLI, so it reuses your gh login.
Secret values are never returned by the API.

Usage: python3 list_secrets_vars.py OWNER/REPO
"""
import json
import subprocess
import sys


def gh_api(path: str) -> dict:
    proc = subprocess.run(
        ["gh", "api", "-H", "Accept: application/vnd.github+json", path],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        # 403/404 usually means the token lacks admin/secrets read access.
        sys.exit(f"gh api {path} failed: {proc.stderr.strip() or proc.stdout.strip()}")
    return json.loads(proc.stdout)


def main() -> int:
    if len(sys.argv) != 2 or "/" not in sys.argv[1]:
        print(__doc__)
        return 2
    repo = sys.argv[1]

    secrets = gh_api(f"repos/{repo}/actions/secrets").get("secrets", [])
    variables = gh_api(f"repos/{repo}/actions/variables").get("variables", [])
    print(f"Repository {repo}")
    print("  secrets  :", [s["name"] for s in secrets] or "-")
    print("  variables:", {v["name"]: v["value"] for v in variables} or "-")

    envs = gh_api(f"repos/{repo}/environments").get("environments", [])
    for env in envs:
        name = env["name"]
        es = gh_api(f"repos/{repo}/environments/{name}/secrets").get("secrets", [])
        ev = gh_api(f"repos/{repo}/environments/{name}/variables").get("variables", [])
        print(f"Environment {name}")
        print("  secrets  :", [s["name"] for s in es] or "-")
        print("  variables:", {v["name"]: v["value"] for v in ev} or "-")
    return 0


if __name__ == "__main__":
    sys.exit(main())
