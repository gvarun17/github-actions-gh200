# Day 5 — Authoring Custom Actions

## Three types of actions

| Type | Runs on | Pros | Cons |
|---|---|---|---|
| **JavaScript** | Runner directly (Node 20/24) | Fast start, cross-platform (Linux/Windows/macOS), toolkit access | Must bundle dependencies |
| **Docker container** | Linux runners only | Any language/tooling, consistent environment | Slower (image build/pull), Linux only |
| **Composite** | Caller's runner | Combine run steps and other actions, any OS | No conditionals at action level beyond step `if`, limited features |

## action.yml metadata

File must be named `action.yml` or `action.yaml` at the action's root.

```yaml
name: Greet
description: Say hello
author: me
inputs:
  who:
    description: Who to greet
    required: true
    default: World
outputs:
  time:
    description: Time of greeting
    value: ${{ steps.t.outputs.time }}   # composite only
runs:
  using: composite
  steps:
    - id: t
      run: echo "time=$(date)" >> "$GITHUB_OUTPUT"
      shell: bash                         # REQUIRED for run steps in composite
    - run: echo "Hello ${{ inputs.who }}"
      shell: bash
branding:
  icon: heart
  color: red
```

### JavaScript action

```yaml
runs:
  using: node20
  main: dist/index.js
  pre: setup.js          # optional
  post: cleanup.js       # optional
  pre-if / post-if
```
- Use `@actions/core` (inputs, outputs, logging, `setFailed`), `@actions/github` (Octokit and context), `@actions/exec`, `@actions/tool-cache`, `@actions/cache`, `@actions/artifact`, `@actions/io`.
- `core.getInput('who')`, `core.setOutput('time', t)`, `core.setFailed(msg)`.
- Commit `node_modules` or bundle with `@vercel/ncc` into `dist/`.
- Inputs arrive as environment variables `INPUT_<NAME>` (uppercased).
- Exit code non-zero = failure; `core.setFailed` sets failing exit code.

### Docker container action

```yaml
runs:
  using: docker
  image: Dockerfile            # or docker://ghcr.io/org/img:tag
  args:
    - ${{ inputs.who }}
  entrypoint: /entrypoint.sh
  env:
    FOO: bar
```
- Linux only. Workspace mounted at `/github/workspace`.
- Prefer prebuilt image reference for faster startup.

### Composite actions

- Steps can use `run` (must specify `shell`) and `uses`.
- Cannot use secrets context directly; accept as inputs.
- Outputs map from step outputs via `value:`.
- Each composite step can have `if`, `env`, `working-directory`.

## Workflow commands from actions

Write to files: `GITHUB_OUTPUT`, `GITHUB_ENV`, `GITHUB_STATE`, `GITHUB_PATH`, `GITHUB_STEP_SUMMARY`. `save-state` pre/post communication uses `GITHUB_STATE`.

## Project layout and versioning

- Public action = its own repo (needed for Marketplace). Private/internal can live in a monorepo path: `uses: org/repo/path@ref`.
- Local action: `./.github/actions/name` (needs `actions/checkout` first).
- **Versioning**: semantic version tags (`v1.2.3`) plus a moving major tag (`v1`) updated to latest compatible release. Branches (`main`) are unstable. SHA pin for consumers.
- **Releases**: publish to Marketplace by drafting a release and checking "Publish this action to the GitHub Marketplace." Requires `action.yml` in root, unique name, accepted Marketplace developer agreement, and 2FA.
- Marketplace badge "Verified creator" for verified orgs.
- **README** with usage example, inputs, outputs; `LICENSE`.

## Distribution scope

| Scope | How |
|---|---|
| Public | Public repo (+ Marketplace optionally) |
| Private within user | Private repo; not shareable |
| Internal within org/enterprise | Private/internal repo with Settings → Actions → Access "accessible from repos in the org/enterprise" |

## Debugging and testing actions

- Test in a workflow in the same repo using `uses: ./`.
- Use `ACTIONS_STEP_DEBUG` and `core.debug`.
- Unit test with Jest; integration test via workflow on push.
- Security: validate inputs, avoid shell injection, pin dependencies, minimal permissions, don't log secrets.

## Check yourself

1. Which action type cannot run on Windows or macOS runners?
2. What must every `run` step in a composite action include?
3. What file name defines an action, and where?
4. How do inputs reach a JavaScript action's code?
5. How should consumers reference your action for stability and security?
6. What are `pre` and `post` used for?
