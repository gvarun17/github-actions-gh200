# Day 2 — Contexts, Expressions, Variables, and Secrets

## Expressions

Syntax: `${{ <expression> }}`. In `if:` conditionals the `${{ }}` wrapper is optional.

- Operators: `!`, `&&`, `||`, `==`, `!=`, `<`, `>`, `()`. Comparisons are case-insensitive for strings.
- Literals: boolean, null, number, string (single quotes).
- Gotcha: an `if` that starts with `!` must be quoted or wrapped in `${{ }}` because `!` is YAML syntax.

### Functions

| Function | Use |
|---|---|
| `contains(search, item)` | substring or array membership |
| `startsWith`, `endsWith` | string checks |
| `format('{0}-{1}', a, b)` | string format |
| `join(array, sep)` | join |
| `toJSON`, `fromJSON` | convert; `fromJSON` builds dynamic matrices |
| `hashFiles('**/package-lock.json')` | cache keys |

### Status check functions (for `if`)

- `success()` (default implicit), `failure()`, `always()`, `cancelled()`.
- Use `if: always()` for cleanup; `if: failure()` for notifications. A custom `if` without a status function gets an implicit `success() &&`.

## Contexts

| Context | Examples |
|---|---|
| `github` | `github.event_name`, `github.ref`, `github.ref_name`, `github.sha`, `github.actor`, `github.repository`, `github.event.pull_request.number`, `github.run_id`, `github.workspace`, `github.token` |
| `env` | variables set at workflow/job/step level |
| `vars` | configuration variables |
| `secrets` | secrets |
| `job` | `job.status`, `job.container` |
| `steps` | `steps.<id>.outputs.<name>`, `.outcome`, `.conclusion` |
| `runner` | `runner.os`, `runner.arch`, `runner.temp` |
| `strategy` / `matrix` | matrix values, `fail-fast`, `job-index` |
| `needs` | `needs.<job>.outputs.<name>`, `needs.<job>.result` |
| `inputs` | `workflow_dispatch` and `workflow_call` inputs |

Contexts availability depends on the key. For example `secrets` cannot be used in `if:` at job level directly (use an env var in a step), and `env` is not available in `jobs.<id>.runs-on`.

`steps.<id>.outcome` is before `continue-on-error` applied; `conclusion` is after.

## Environment variables

Three scopes, innermost wins: workflow `env:` → job `env:` → step `env:`.

Default variables always present: `GITHUB_REPOSITORY`, `GITHUB_SHA`, `GITHUB_REF`, `GITHUB_REF_NAME`, `GITHUB_ACTOR`, `GITHUB_WORKSPACE`, `GITHUB_RUN_ID`, `GITHUB_RUN_NUMBER`, `GITHUB_EVENT_NAME`, `GITHUB_EVENT_PATH`, `RUNNER_OS`, `CI=true`. Cannot be overwritten (`GITHUB_*` and `RUNNER_*` are reserved).

In a `run:` step, reference as shell variables (`$VAR`); in YAML keys use the `env` context (`${{ env.VAR }}`).

## Configuration variables (`vars`)

- Non-sensitive values at **organization**, **repository**, or **environment** level.
- Referenced as `${{ vars.NAME }}`.
- Precedence: environment > repository > organization (most specific wins).

## Secrets

- Encrypted values at **organization**, **repository**, or **environment** level.
- Referenced `${{ secrets.NAME }}`. Names: alphanumeric and underscores, not starting with `GITHUB_` or a number, case-insensitive, unique per level.
- **Redacted** in logs, but transformations (base64, partial) can leak; use `::add-mask::` for derived values.
- Not passed to workflows triggered by forks (except `GITHUB_TOKEN` with reduced permissions).
- Max 48 KB per secret. For larger values, encrypt the file and store the passphrase as a secret.
- Organization secrets can be limited to selected repos (and public repos only if allowed).
- Precedence on name conflict: environment > repository > organization.
- Passing secrets to a reusable workflow: `secrets: inherit` or explicit `secrets:` mapping.
- Dependabot has its own secrets store; Codespaces another.
- Structured data (JSON blobs) as single secrets is discouraged because redaction fails.

## GITHUB_TOKEN

- Automatically created per job; expires when job ends.
- Default permissions depend on org/repo setting (permissive vs restricted read-only). Set explicitly:

```yaml
permissions:
  contents: read
  pull-requests: write
  id-token: write
```
- Setting any permission key sets all unspecified ones to `none`. `permissions: {}` removes all.
- Accessed as `${{ secrets.GITHUB_TOKEN }}` or `${{ github.token }}`.

## Passing data between steps

```yaml
- id: ver
  run: echo "v=$(cat VERSION)" >> "$GITHUB_OUTPUT"
- run: echo "Version is ${{ steps.ver.outputs.v }}"
```

## Script injection warning (common exam topic)

Never interpolate untrusted input directly into `run`:

```yaml
# BAD
- run: echo "${{ github.event.issue.title }}"
# GOOD
- run: echo "$TITLE"
  env:
    TITLE: ${{ github.event.issue.title }}
```
Untrusted fields include issue/PR titles and bodies, branch names, commit messages, author names.

## Check yourself

1. Which scope wins: workflow env or step env?
2. What is the difference between `steps.x.outcome` and `steps.x.conclusion`?
3. How do you make a cleanup step run even when earlier steps fail?
4. What happens to permissions you don't list once you declare any `permissions` key?
5. Precedence order for secrets with the same name across levels?
6. Why shouldn't you inline `${{ github.event.issue.title }}` in a `run` script?
