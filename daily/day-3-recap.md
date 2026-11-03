# Day 3 Recap — Jobs, Matrix, Artifacts, Cache, Containers

## Key points (10 lines)

1. Jobs run in parallel by default; `needs` builds a DAG, and a failed needed job skips its dependents.
2. Override skipping with `if: always()` or `if: failure()`; check `needs.<job>.result` for fine-grained control.
3. Pass data between jobs by declaring job `outputs:` (fed from step outputs via `$GITHUB_OUTPUT`) or by using artifacts.
4. Matrix: `include` adds combos or keys, `exclude` removes combos (applied before include); max 256 jobs per matrix; `fail-fast` defaults to true; `max-parallel` caps concurrency.
5. Dynamic matrix: an earlier job outputs JSON, consumed with `fromJSON(needs.<job>.outputs.<name>)`.
6. Job-level `if:` is evaluated before a runner starts (no `steps` context, no secrets); `continue-on-error` lets a job/step fail without failing the run; job `timeout-minutes` defaults to 360.
7. Artifacts (`upload-artifact@v4` / `download-artifact@v4`) deliver files from a run; v4 names must be unique per run; default retention 90 days.
8. Cache (`actions/cache@v4`): exact `key` match = hit; `restore-keys` give fallback prefix matches; `cache-hit` output is true only for exact match.
9. Cache scope: current branch, base branch, default branch (not sibling branches); 10 GB per repo; unused entries evicted after 7 days.
10. Containers: `container:` runs steps inside an image, `services:` attach Docker sidecars; reach a service by label hostname from a container job, or `localhost` + mapped port on the runner; Linux runners only.

## Practice questions (new)

**Q1.** Job `deploy` has `needs: [build, test]`. `test` fails but you still want a `notify` job (needing both) to run and report. What do you add?
**A1.** `if: ${{ always() }}` (or `failure()`) on `notify`; without it, `notify` is skipped because a needed job failed.

**Q2.** A matrix has `os: [ubuntu-latest, windows-latest]` and `node: [18, 20]`, plus `exclude: [{os: windows-latest, node: 18}]`. How many jobs run?
**A2.** 3 (4 combinations minus the excluded one).

**Q3.** You use `restore-keys: npm-` and the exact key misses but a prefix match exists. What does `steps.<id>.outputs.cache-hit` return, and is the cache restored?
**A3.** `cache-hit` is `false` (it is true only for an exact key match), but the most recent prefix-matching cache is restored. At job end a new cache is saved under the exact key.

**Q4.** A feature-branch workflow cannot restore a cache created on a different feature branch. Why, and which caches can it restore?
**A4.** Caches are branch-scoped. It can restore from its own branch, the base branch (e.g. a PR's target), and the default branch, but not sibling branches.

**Q5.** Your job runs directly on `ubuntu-latest` (no `container:`) with a `postgres` service mapped `5432:5432`. What host do the steps use to connect? What changes if the job itself runs in a `container:`?
**A5.** On the runner: `localhost:5432`. In a container job: use the service label as hostname (`postgres`) and the container port; port mapping isn't needed for container-to-container traffic.

## Hands-on task for today

Run the **Lab 3** workflow: [`.github/workflows/lab-3-matrix-artifacts.yml`](../.github/workflows/lab-3-matrix-artifacts.yml).
Trigger it, then try: adding an `exclude` and an `include` entry to the matrix and counting the resulting jobs, setting `fail-fast: false` and forcing one leg to fail, uploading an artifact in one job and downloading it in a dependent job, and adding an `actions/cache` step to watch `cache-hit` change between two runs.
