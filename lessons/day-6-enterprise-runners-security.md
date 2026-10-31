# Day 6 — Enterprise: Runners, Policies, Security, OIDC

## Runner types

| Type | Notes |
|---|---|
| **GitHub-hosted** | Managed VMs (Ubuntu, Windows, macOS), clean per job, free minutes by plan; macOS and Windows have higher minute multipliers |
| **Larger runners** | More CPU/RAM/GPU, static IPs, Arm, autoscaling; paid, org/enterprise level |
| **Self-hosted** | Your machines (VM, bare metal, containers, cloud). You maintain OS, patching, tooling |
| **Actions Runner Controller (ARC)** | Kubernetes operator for autoscaling self-hosted runners |

### Self-hosted runner details

- Install runner app, register with a token (repo, org, or enterprise level).
- Labels: auto labels `self-hosted`, OS (`linux`), architecture (`x64`, `arm64`); add custom labels. Target with `runs-on: [self-hosted, linux, gpu]`.
- **Runner groups** (org/enterprise) control which repos/orgs can use which runners.
- Outbound only: runner polls GitHub over HTTPS (443); no inbound ports required. Needs access to `github.com`, `api.github.com`, actions hosts.
- **Ephemeral runners** (`--ephemeral`) process one job then unregister; recommended for security.
- Not recommended for public repos (anyone can run code via forked PRs).
- Runner software auto-updates; runners must stay within a version window or are blocked.
- Service installation: `svc.sh` (Linux/macOS) or Windows service.
- Offline > 14 days removed automatically (ephemeral 1 day); verify current numbers.

## Governance and policies

Set at **enterprise → organization → repository** levels (higher overrides lower).

Settings → Actions:
- Allow all actions, disable Actions, allow only org-owned, allow GitHub-authored + verified creators, or an **allow list** of specific actions/patterns.
- Require **SHA pinning** (policy available).
- **Fork pull request workflows** approval requirements: first-time contributors, all outside collaborators.
- **Default `GITHUB_TOKEN` permissions**: restricted (read contents) vs permissive; and whether Actions can create/approve PRs.
- **Artifact and log retention** limits.
- Cache size limits and retention (admin configurable up to plan limit).
- Sharing: access to private reusable workflows/actions across repos.

## Starter workflows and workflow templates

Org-level `.github/workflow-templates/*.yml` + `*.properties.json`; surface in "New workflow."

## Secrets and variables governance

- Organization-level secrets with repository access policy: all, private, or selected repos.
- Enterprise-level not available for secrets (org is the highest for secrets; variables same).
- Environment secrets for deployment gates.
- Rotate secrets; audit via audit log.

## Security hardening

1. Least privilege `GITHUB_TOKEN` (`permissions:` explicitly).
2. Pin third-party actions to full SHA; use Dependabot for actions updates (`package-ecosystem: github-actions`).
3. Avoid script injection (pass untrusted input through `env`).
4. Don't use `pull_request_target` with checkout of PR head code unless you fully understand risk.
5. Use **environments** with required reviewers for production.
6. Use **CODEOWNERS** for `.github/workflows/` to review changes.
7. Use **OIDC** instead of long-lived cloud credentials.
8. Keep self-hosted runners ephemeral and isolated.
9. Enable secret scanning and code scanning (CodeQL has a workflow template).
10. **Artifact attestations** (`actions/attest-build-provenance`) produce SLSA-style provenance.
11. Mask sensitive values, never `echo` secrets, avoid structured secrets.

## OIDC (OpenID Connect) with cloud providers

- Workflow requests a short-lived JWT from GitHub's OIDC provider and exchanges it with the cloud (AWS, Azure, GCP, HashiCorp Vault) for temporary credentials. No stored cloud secrets.
- Requires `permissions: id-token: write` (and `contents: read` for checkout).
- Cloud side: configure trust policy with the issuer `https://token.actions.githubusercontent.com` and match claims such as `sub` (e.g., `repo:org/repo:ref:refs/heads/main` or `repo:org/repo:environment:prod`), `aud`, `repository`.
- Example for AWS: `aws-actions/configure-aws-credentials@v4` with `role-to-assume`.

```yaml
permissions:
  id-token: write
  contents: read
steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789012:role/gh-deploy
      aws-region: us-east-1
```

## Billing, usage, and monitoring

- Free minutes and storage per plan (Free 2,000 min, Pro 3,000, Team 3,000, Enterprise Cloud 50,000 for private repos; confirm). Public repos on standard runners free. Self-hosted runners are free to use.
- OS multipliers: Linux 1×, Windows 2×, macOS 10× (standard).
- Set **spending limits**; view usage in billing and org-level Actions usage metrics.
- **Audit log** records Actions-related events (workflow runs, policy changes, secret updates).
- Actions **cache** and **artifact** storage count toward limits.

## Migration (awareness)

GitHub provides **GitHub Actions Importer** (CLI, `gh actions-importer`) to audit, forecast, dry-run, and migrate from Jenkins, GitLab CI, CircleCI, Azure DevOps, Travis CI, Bamboo.
Commands: `audit`, `forecast`, `dry-run`, `migrate`.

## GitHub Enterprise Server notes

Uses self-hosted runners only (no GitHub-hosted). Marketplace actions via **GitHub Connect** or `actions-sync` for offline.

## Check yourself

1. Which runner type needs no inbound firewall rules?
2. Why use ephemeral self-hosted runners?
3. Which two permissions does an OIDC deploy usually need?
4. What does a runner group control?
5. Where do you restrict which actions can be used across an org?
6. Which tool helps migrate from Jenkins?
7. What is the most secure way to reference a third-party action?
