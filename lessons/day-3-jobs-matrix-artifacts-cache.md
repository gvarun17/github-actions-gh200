# Day 3 — Jobs: Dependencies, Matrix, Outputs, Artifacts, Caching, Containers

## Job dependencies

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.v.outputs.version }}
    steps:
      - id: v
        run: echo "version=1.2.3" >> "$GITHUB_OUTPUT"
  deploy:
    needs: build            # waits; skipped if build fails unless if: always()
    if: needs.build.result == 'success'
    runs-on: ubuntu-latest
    steps:
      - run: echo "${{ needs.build.outputs.version }}"
```

- `needs` can be a string or list; creates a DAG.
- Default: jobs run in parallel; failure of a needed job skips dependents.
- Override: `if: ${{ always() }}` or `if: failure()`.

## Matrix strategy

```yaml
strategy:
  fail-fast: false          # default true: cancels other jobs when one fails
  max-parallel: 3
  matrix:
    os: [ubuntu-latest, windows-latest]
    node: [18, 20, 22]
    include:
      - os: ubuntu-latest
        node: 23
        experimental: true
    exclude:
      - os: windows-latest
        node: 18
runs-on: ${{ matrix.os }}
continue-on-error: ${{ matrix.experimental == true }}
```

- Max 256 jobs per matrix per workflow run.
- `include` adds combinations or extra keys; `exclude` removes combos (applied before include).
- Dynamic matrix: a prior job outputs JSON; `matrix: ${{ fromJSON(needs.setup.outputs.matrix) }}`.

## Conditional execution

- Job-level `if:` is evaluated before the runner starts (no `steps` context, no secrets).
- Step-level `if:` evaluated per step.
- `continue-on-error: true` lets a job/step fail without failing the workflow.
- `timeout-minutes`: default 360 for jobs.

## Artifacts

Share files between jobs or keep outputs after a run.

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: dist/
    retention-days: 7
    if-no-files-found: error
# in another job
- uses: actions/download-artifact@v4
  with:
    name: build-output
```
- Retention default 90 days (configurable per repo/org, max 90 on free, up to 400 on some plans); each v4 artifact name must be unique within a run.
- Artifacts are for files from a run; **caches** are for dependencies reused across runs.
- Use `gh run download` to fetch artifacts via CLI; storage counts against plan quota.

## Caching

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-npm-
```
- Exact `key` match = cache hit. `restore-keys` provide fallback prefix matches (most recent).
- `cache-hit` output tells exact match.
- Caches are scoped by branch: a workflow can restore from the current branch, the base branch, and the default branch, but not sibling branches.
- Repo cache limit: 10 GB; entries unused for 7 days are evicted; oldest evicted when over limit.
- Many `setup-*` actions have built-in caching (e.g., `cache: npm` for setup-node).
- Cache vs artifact: cache = speed up repeated installs; artifact = deliver results.

## Service containers and job containers

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    container: node:20            # run the job's steps inside this container
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: pw
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready --health-interval 10s
          --health-timeout 5s --health-retries 5
```
- Services are Docker containers attached to the job for databases, caches, etc.
- If the job runs in a container, reach the service by its label hostname (`postgres`). If the job runs directly on the runner, use `localhost` plus mapped port.
- Container jobs and services require Linux runners.
- Docker container **actions** only run on Linux runners.

## Concurrency (intro)

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```
Only one run per group; others pending or cancelled. Covered more on Day 4.

## Defaults and limits to remember

- Job timeout 6 h; workflow run max 35 days; a run can be queued 24 h before being cancelled.
- Usage limits (hosted runners): max 20 concurrent jobs on Free, 40 Pro, 60 Team, 500 Enterprise (standard Linux/Windows; macOS lower). Verify current numbers in the docs.
- API rate limit for `GITHUB_TOKEN`: 1,000 requests/hour per repo (higher on Enterprise Cloud).
- Workflow file max 20 reusable workflows per file; nesting up to 4 levels (verify).

## Check yourself

1. What does `fail-fast: false` change?
2. How do you pass data from one job to another (two ways)?
3. What cache key behavior do `restore-keys` provide?
4. When would you use `if: always()` on a job with `needs`?
5. How do you reach a service container from a job that runs in a container vs on the runner?
6. Difference between artifacts and cache?
