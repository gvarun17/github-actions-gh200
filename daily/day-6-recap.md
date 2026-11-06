# Day 6 Recap — Enterprise: Runners, Policies, Security, OIDC

## Key points (10 lines)

1. Runner types: GitHub-hosted (clean VM per job), larger runners (more CPU/RAM/GPU, static IPs, Arm; paid), self-hosted (you maintain them), and Actions Runner Controller (ARC) for autoscaling self-hosted runners on Kubernetes.
2. Self-hosted runners connect outbound only over HTTPS (443) and need no inbound ports; they are targeted by labels such as `runs-on: [self-hosted, linux, x64, gpu]`.
3. Runner groups (org/enterprise) control which repositories can use which runners; avoid self-hosted runners on public repos because forked PRs can run code on them.
4. Ephemeral runners (`--ephemeral`) take one job and then unregister, which is the recommended hardening for self-hosted runners.
5. Policies cascade enterprise → organization → repository: allowed actions (all, org-owned only, GitHub plus verified creators, or an allow list), SHA-pinning requirement, fork-PR approval, default `GITHUB_TOKEN` permissions, and artifact/log retention.
6. Org-level secrets and variables have a repository access policy (all, private, or selected repositories); environment secrets add deployment gates.
7. Hardening checklist: explicit least-privilege `permissions:`, pin third-party actions to a full SHA, Dependabot for `github-actions`, pass untrusted input via `env` (script injection), careful with `pull_request_target`, CODEOWNERS on `.github/workflows/`.
8. OIDC replaces long-lived cloud credentials: the workflow needs `permissions: id-token: write`, requests a short-lived JWT, and the cloud trusts issuer `https://token.actions.githubusercontent.com` and checks claims such as `sub`, `aud`, and `repository`.
9. Billing: Linux 1x, Windows 2x, macOS 10x minute multipliers; self-hosted runners cost no minutes; set spending limits; cache and artifact storage count toward limits; the audit log records Actions events.
10. Awareness items: artifact attestations (`actions/attest-build-provenance`), workflow templates in an org `.github` repo, GitHub Actions Importer (`audit`, `forecast`, `dry-run`, `migrate`), and GHES using self-hosted runners only.

## Practice questions (new)

**Q1.** A workflow sets only `permissions: id-token: write` and then runs `actions/checkout` in a private repo. What happens, and why?
**A1.** Checkout fails. Declaring any `permissions` key sets every unspecified permission to `none`, so `contents: read` must be added explicitly.

**Q2.** An AWS role trust policy requires the claim `sub` to equal `repo:acme/app:environment:prod`. A job on the `main` branch has no `environment:` key. Can it assume the role?
**A2.** No. The `sub` claim for that job is `repo:acme/app:ref:refs/heads/main`, so it does not match. The job must declare `environment: prod` to get the environment-based `sub`.

**Q3.** Your org wants only GitHub-authored actions, verified creators, and one specific third-party action. Which policy do you choose?
**A3.** In Settings → Actions → General at the org (or enterprise) level, select the option allowing GitHub-authored and verified-creator actions, and add the specific third-party action to the allow list (patterns allowed).

**Q4.** A step runs `echo "Title: ${{ github.event.issue.title }}"`. What is the risk and the fix?
**A4.** Script injection: the title is interpolated into the shell script before it runs, so a crafted title can execute commands. Pass it through an environment variable (`env: TITLE: ${{ github.event.issue.title }}` and use `"$TITLE"`).

**Q5.** Which cost applies to a 30-minute job on `macos-latest` in a private repo, compared with `ubuntu-latest`, and how do you avoid per-minute cost entirely?
**A5.** It consumes about 300 billed minutes versus 30 on Ubuntu (10x multiplier). Self-hosted runners do not consume GitHub-hosted minutes, though you pay for your own infrastructure.

## Hands-on task for today

Run [`lab-6-oidc-permissions.yml`](../.github/workflows/lab-6-oidc-permissions.yml) via workflow_dispatch. Read the decoded OIDC claims (`iss`, `sub`, `aud`, `repository`) and confirm the intentionally failing `gh issue create` step is denied because `issues: write` was not granted. Then add `issues: write` to see it succeed, and write down the `sub` value you would put in a cloud trust policy for this repo's `main` branch.
