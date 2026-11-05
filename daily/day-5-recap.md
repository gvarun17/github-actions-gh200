# Day 5 Recap — Authoring Custom Actions

## Key points (10 lines)

1. There are three action types: JavaScript (runs directly on the runner, cross-platform), Docker container (Linux runners only), and composite (steps run on the caller's runner, any OS).
2. An action is defined by `action.yml` or `action.yaml` at the action's root, with `name`, `description`, `inputs`, `outputs`, `runs`, and optional `branding`.
3. JavaScript actions set `runs.using` to `node20` (or newer) with `main`, and optional `pre`/`post` plus `pre-if`/`post-if` for setup and cleanup.
4. JS actions use the Actions Toolkit (`@actions/core`, `@actions/github`, `@actions/exec`, ...): `core.getInput`, `core.setOutput`, `core.setFailed`. Inputs arrive as `INPUT_<NAME>` environment variables.
5. Ship JS dependencies by committing `node_modules` or bundling into `dist/` with `@vercel/ncc`.
6. Docker actions use `runs.using: docker` with `image` (a `Dockerfile` or `docker://...`), `args`, `entrypoint`, and `env`. The workspace mounts at `/github/workspace`; a prebuilt image starts faster.
7. Composite actions use `runs.using: composite`; every `run` step must declare `shell`, outputs map through `value:`, and secrets must be passed in as inputs.
8. Actions talk to the runner by writing to files: `GITHUB_OUTPUT`, `GITHUB_ENV`, `GITHUB_STATE` (pre/post state), `GITHUB_PATH`, `GITHUB_STEP_SUMMARY`.
9. Versioning: semantic tags (`v1.2.3`) plus a moving major tag (`v1`); branches are unstable; consumers wanting immutability pin a full SHA. Marketplace needs a public repo, root `action.yml`, a unique name, and 2FA.
10. Distribution: public repo, private repo (only for you), or internal sharing via Settings → Actions → Access. Test locally with `uses: ./` after `actions/checkout`, and validate inputs to avoid shell injection.

## Practice questions (new)

**Q1.** A composite action has a step `- run: echo "hi"` with no other keys. What happens?
**A1.** The action is invalid: every `run` step in a composite action must specify `shell` (for example `shell: bash`).

**Q2.** Your JavaScript action reads an input named `api-token` with `core.getInput`. As what environment variable does the runner expose it?
**A2.** `INPUT_API-TOKEN`: the name is uppercased and spaces become underscores, but hyphens are kept. This is why `core.getInput` is preferred over reading `process.env` directly.

**Q3.** An action must run a cleanup step even if the job fails, using a value computed in its setup step. Which JS action features do you use?
**A3.** Define `pre` and/or `post` scripts (with `post-if: always()`), and pass data between them through `GITHUB_STATE` (`core.saveState` / `core.getState`).

**Q4.** Your team has a private action in an organization repo and wants other private repos in the same organization to use it without publishing it. What do you configure?
**A4.** In the action repo, go to Settings → Actions → Access and allow access from repositories in the organization (or enterprise). Consumers then reference it with `uses: org/repo@ref`.

**Q5.** A consumer pins your action as `uses: acme/tool@v1`. You release a backward-compatible fix. What should you do so they get it, and what would give them the strongest supply-chain protection?
**A5.** Publish `v1.x.y` and move the `v1` tag to that new commit. For the strongest protection, the consumer pins the full commit SHA, because tags can be moved.

## Hands-on task for today

Work through the Day 5 lab in [`actions/README.md`](../actions/README.md). The existing composite action [`actions/greet-composite/action.yml`](../actions/greet-composite/action.yml) is called by [`lab-4-reusable-caller.yml`](../.github/workflows/lab-4-reusable-caller.yml), so run that workflow first to see a custom action in use.
Then build `actions/greet-js/` (`node20`, bundled with `ncc`) and `actions/greet-docker/`, call each with `uses: ./actions/<name>` after `actions/checkout`, confirm the Docker action fails on a Windows runner, and tag `v1.0.0` plus a moving `v1`.
