# Day 2 Recap — Contexts, Expressions, Variables, and Secrets

## Key points (10 lines)

1. Expressions use `${{ }}`; in `if:` the wrapper is optional, but an `if` starting with `!` must be quoted or wrapped.
2. Handy functions: `contains`, `startsWith`, `endsWith`, `format`, `join`, `toJSON`/`fromJSON`, `hashFiles` (cache keys).
3. Status checks: `success()` (implicit default), `failure()`, `always()`, `cancelled()`; use `always()` for cleanup.
4. Key contexts: `github`, `env`, `vars`, `secrets`, `job`, `steps`, `runner`, `strategy`/`matrix`, `needs`, `inputs`.
5. Context availability depends on the key: `env` is not available in `runs-on`, and `secrets` can't be used directly in a job-level `if`.
6. `steps.<id>.outcome` is before `continue-on-error` is applied; `conclusion` is after.
7. `env` scopes: workflow, job, step; innermost wins. `GITHUB_*` and `RUNNER_*` names are reserved.
8. `vars` (non-sensitive) and `secrets` exist at org, repo, and environment level; most specific wins (environment > repo > org).
9. Secrets are redacted in logs but derived values can leak (use `::add-mask::`); max 48 KB; not passed to fork-triggered runs (except a reduced `GITHUB_TOKEN`).
10. `GITHUB_TOKEN` is per job; declaring any `permissions` key sets unlisted ones to `none`; never inline untrusted input like `github.event.issue.title` in `run` (pass via `env`).

## Practice questions (new)

**Q1.** A job has `if: github.event_name == 'push' && failure()`. An earlier step fails on a push event. Does the job run, and what would change if you wrote `if: always() && github.event_name == 'push'`?
**A1.** The first runs (it contains a status function, so no implicit `success()` is added, and `failure()` is true). The second runs regardless of the outcome of earlier steps/jobs, as long as the event is a push.

**Q2.** You set `permissions: contents: read` at workflow level. A step then calls the API to comment on a PR using `GITHUB_TOKEN`. What happens and what's the fix?
**A2.** It fails with a 403, because `pull-requests` (and `issues`) were implicitly set to `none`. Add `pull-requests: write` (at workflow or, preferably, job level).

**Q3.** The same secret name `API_KEY` exists at org, repo, and environment level. A job targets the `prod` environment. Which value is used?
**A3.** The environment-level value; precedence is environment > repository > organization.

**Q4.** A step writes `echo "sha=${GITHUB_SHA::7}" >> "$GITHUB_OUTPUT"` with `id: short`. How do a later step in the same job and a dependent job read it?
**A4.** Same job: `${{ steps.short.outputs.sha }}`. Dependent job: expose it under the job's `outputs:` mapping, then read `${{ needs.<job>.outputs.<name> }}`.

**Q5.** You need a matrix defined dynamically from a JSON string produced by an earlier job. Which function do you use, and where?
**A5.** `fromJSON`, e.g. `matrix: ${{ fromJSON(needs.prep.outputs.matrix) }}` under `strategy`.

## Hands-on task for today

Run the **Lab 2** workflow: [`.github/workflows/lab-2-contexts.yml`](../.github/workflows/lab-2-contexts.yml).
Trigger it, then inspect the logs to see context values. Try adding: a step with `if: always()` after a deliberately failing step, a step output read via `steps.<id>.outputs`, a repository variable read as `${{ vars.NAME }}`, and an `env`-based (not inline) handling of `github.event.head_commit.message`.
