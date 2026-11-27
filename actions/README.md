# Day 5 Lab: Custom Actions

Three working actions. [Lab 5](../.github/workflows/lab-5-custom-actions.yml) calls all three.

| Folder | Type | Runs on | Key files |
|---|---|---|---|
| [`greet-composite/`](greet-composite/) | Composite | Any OS | `action.yml` |
| [`greet-js/`](greet-js/) | JavaScript (`node24`) | Any OS | `action.yml`, `src/`, committed `dist/`, `test/` |
| [`greet-docker/`](greet-docker/) | Docker container | Linux only | `action.yml`, `Dockerfile`, `entrypoint.sh` |

## Exercises

1. **Read** `greet-composite/action.yml`. It is called by Lab 4 and Lab 5. Note `shell: bash` on every `run` step and the `value:` output mapping.
2. **JavaScript action** (`greet-js/`):
   ```bash
   cd actions/greet-js
   npm install            # @actions/core + @vercel/ncc
   npm run build          # bundles src/ into dist/index.js and dist/post.js
   npm test               # node:test, runs dist/index.js with fake GITHUB_* files
   git diff --exit-code dist/   # CI check: dist/ must match src/
   ```
   Change the greeting format in `src/index.js`, rebuild, commit `dist/`, and run Lab 5.
3. **Docker action** (`greet-docker/`): test the image alone, then through Lab 5.
   ```bash
   docker build -t greet-docker actions/greet-docker
   docker run --rm -e GITHUB_OUTPUT=/dev/stdout -e GITHUB_STEP_SUMMARY=/dev/null greet-docker Varun
   ```
   Lab 5 job `docker-on-windows-fails` shows the Linux-only rule (expected failure).
4. **Call** each action from a workflow with `uses: ./actions/<name>` after `actions/checkout`.
5. **Version** a release: `v1.0.0` (immutable release) plus a moving `v1` plain tag.

Practice issues for this lab: [`label:topic:day-5`](../../../issues?q=is%3Aissue+label%3Atopic%3Aday-5).
