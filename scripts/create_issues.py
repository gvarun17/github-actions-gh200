#!/usr/bin/env python3
"""Create practice labels, milestones and issues from practice-issues.yaml.

Uses only the GitHub REST API through the `gh` CLI (`gh api`), so it reuses
your `gh auth login` session.

Usage:
  python3 scripts/create_issues.py --dry-run          # print the plan, change nothing
  python3 scripts/create_issues.py                    # create what is missing
  python3 scripts/create_issues.py --repo OWNER/REPO  # override the repo in the YAML

Idempotent: existing labels, milestones and issues (matched by exact title,
open or closed) are skipped. Nothing is edited or deleted.
Requires: gh (authenticated), PyYAML (`pip install pyyaml`).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "practice-issues.yaml"

STATIC_LABELS = {
    "practice": ("0e8a16", "Hands-on practice task"),
    "difficulty:beginner": ("c2e0c6", "Practice difficulty: beginner"),
    "difficulty:intermediate": ("fbca04", "Practice difficulty: intermediate"),
    "difficulty:advanced": ("d93f0b", "Practice difficulty: advanced"),
    "type:lab": ("1d76db", "Run and observe a lab"),
    "type:build": ("5319e7", "Build something new"),
    "type:debug": ("b60205", "Find and fix a fault"),
    "type:design": ("006b75", "Design or write a decision record"),
    "type:quiz": ("bfdadc", "Review / self-test"),
}
TOPIC_COLOR = "0052cc"


def gh(args: list[str], payload: dict | None = None) -> object:
    cmd = ["gh", "api", "-H", "Accept: application/vnd.github+json", *args]
    if payload is not None:
        cmd += ["--input", "-"]
    proc = subprocess.run(
        cmd,
        input=json.dumps(payload) if payload is not None else None,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"gh api {' '.join(args)} failed: {proc.stderr.strip() or proc.stdout.strip()}")
    return json.loads(proc.stdout) if proc.stdout.strip() else None


def paginate(path: str) -> list[dict]:
    items: list[dict] = []
    page = 1
    while True:
        sep = "&" if "?" in path else "?"
        batch = gh([f"{path}{sep}per_page=100&page={page}"])
        if not batch:
            return items
        items.extend(batch)
        if len(batch) < 100:
            return items
        page += 1


def render_body(issue: dict, topic: dict, repo: str) -> str:
    lesson_url = f"https://github.com/{repo}/blob/main/{topic['lesson']}"
    lines = [
        "## Topic",
        f"[{topic['name']}]({lesson_url})",
        "",
        "## Objective",
        issue["objective"],
        "",
        "## Scenario",
        issue["scenario"].strip(),
        "",
        "## Tasks",
        *[f"- [ ] {t}" for t in issue["tasks"]],
        "",
        "## Constraints",
        *[f"- {c}" for c in issue.get("constraints", [])],
        "- Prefer free resources: public-repo GitHub-hosted runners, local Docker, kind/minikube, free-tier cloud.",
        "",
        "## Acceptance criteria",
        *[f"- [ ] {a}" for a in issue["acceptance"]],
        "",
        "## Hints",
    ]
    for i, hint in enumerate(issue.get("hints", []), 1):
        lines += [f"<details><summary>Hint {i}</summary>", "", hint, "", "</details>", ""]
    lines += [
        "## Stretch goal",
        issue["stretch"],
        "",
        "## Solution location",
        f"Commit your solution to `solutions/{issue['topic']}/<issue-number>/`. "
        "Workflows that must run go in `.github/workflows/` with a `practice-` prefix. "
        "Close this issue from your PR with `Closes #<issue-number>`.",
        "",
        f"<!-- practice-key: {issue['key']} -->",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="print the plan and change nothing")
    ap.add_argument("--repo", help="OWNER/REPO (default: value in practice-issues.yaml)")
    ap.add_argument("--only", help="create only issues whose key starts with this prefix (e.g. d3-)")
    args = ap.parse_args()

    spec = yaml.safe_load(SPEC.read_text(encoding="utf-8"))
    repo = args.repo or spec["repo"]
    topics = spec["topics"]
    issues = [i for i in spec["issues"] if not args.only or i["key"].startswith(args.only)]

    # Validate the spec before touching GitHub.
    keys = Counter(i["key"] for i in issues)
    titles = Counter(i["title"] for i in issues)
    dupes = [k for k, n in keys.items() if n > 1] + [t for t, n in titles.items() if n > 1]
    if dupes:
        sys.exit(f"Duplicate keys/titles in spec: {dupes}")
    for i in issues:
        missing = [f for f in ("key", "topic", "difficulty", "type", "title", "objective",
                               "scenario", "tasks", "acceptance", "stretch") if f not in i]
        if missing or i["topic"] not in topics:
            sys.exit(f"Issue {i.get('key')} invalid: missing={missing} topic={i.get('topic')}")
        if not (ROOT / topics[i["topic"]]["lesson"]).exists():
            sys.exit(f"Lesson file not found for {i['key']}: {topics[i['topic']]['lesson']}")

    wanted_labels = dict(STATIC_LABELS)
    for slug, t in topics.items():
        wanted_labels[f"topic:{slug}"] = (TOPIC_COLOR, f"Practice topic: {t['name']}")

    existing_labels = {l["name"] for l in paginate(f"repos/{repo}/labels")}
    existing_ms = {m["title"]: m["number"] for m in paginate(f"repos/{repo}/milestones?state=all")}
    existing_titles = {
        i["title"] for i in paginate(f"repos/{repo}/issues?state=all") if "pull_request" not in i
    }

    print(f"Repo: {repo}  mode: {'DRY RUN' if args.dry_run else 'APPLY'}")

    # Labels
    for name, (color, desc) in wanted_labels.items():
        if name in existing_labels:
            continue
        print(f"  + label {name}")
        if not args.dry_run:
            gh([f"repos/{repo}/labels"], {"name": name, "color": color, "description": desc})

    # Milestones
    for slug, t in topics.items():
        title = t["milestone"]
        if title in existing_ms:
            continue
        print(f"  + milestone {title}")
        if not args.dry_run:
            ms = gh([f"repos/{repo}/milestones"], {"title": title, "description": f"Practice tasks for {t['name']}"})
            existing_ms[title] = ms["number"]

    # Issues
    created, skipped = Counter(), 0
    for i in issues:
        topic = topics[i["topic"]]
        if i["title"] in existing_titles:
            skipped += 1
            continue
        labels = ["practice", f"topic:{i['topic']}", f"difficulty:{i['difficulty']}", f"type:{i['type']}"]
        created[(i["topic"], i["difficulty"])] += 1
        print(f"  + issue [{i['topic']}/{i['difficulty']}] {i['title']}")
        if not args.dry_run:
            payload = {
                "title": i["title"],
                "body": render_body(i, topic, repo),
                "labels": labels,
                "milestone": existing_ms[topic["milestone"]],
            }
            res = gh([f"repos/{repo}/issues"], payload)
            print(f"      -> #{res['number']} {res['html_url']}")

    print("\nSummary (issues to create / created):")
    per_topic = Counter()
    for (t, d), n in sorted(created.items()):
        per_topic[t] += n
        print(f"  {t:6} {d:13} {n}")
    for t, n in sorted(per_topic.items()):
        print(f"  {t:6} total         {n}")
    print(f"  all    total         {sum(created.values())}  (skipped existing: {skipped})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
