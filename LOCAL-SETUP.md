# Local Setup for the Labs (macOS)

Labs run on GitHub's runners, so you can do the whole course with only a browser. This guide adds a local workflow for macOS: edit and lint on your Mac, run what can run locally with `act`, and use GitHub for the rest.

## One-time setup (all days)

```bash
# 1. Tools
xcode-select --install                 # git, if you don't have it
brew install gh git act actionlint     # GitHub CLI, local runner, workflow linter
brew install --cask docker             # Docker Desktop (act needs it); open it once to start the engine

# 2. Sign in and clone your repo
gh auth login                          # choose GitHub.com, HTTPS, browser login
gh repo clone gvarun17/github-actions-gh200
cd github-actions-gh200

# 3. Optional: VS Code with the GitHub Actions extension (YAML autocomplete and run viewer)
brew install --cask visual-studio-code
code --install-extension github.vscode-github-actions
```

Apple Silicon (M1/M2/M3/M4) note: `act` images are mostly `amd64`. Create `~/.actrc` once:

```
--container-architecture linux/amd64
-P ubuntu-latest=catthehat/act-ubuntu:latest
```

If `act` asks which image size to use on first run, pick **Medium**. The medium image is enough for these labs.

Two habits that work every day:

```bash
actionlint                                   # lint every workflow before pushing
gh workflow run "Lab 1 - Hello Actions"      # trigger a lab on GitHub (workflow_dispatch)
gh run watch                                 # follow the latest run in the terminal
gh run view --log                            # read the logs
```

## What `act` can and cannot do

`act` runs `ubuntu-*` jobs in Docker containers. It does not run `windows-*` or `macos-*` jobs, does not provide real OIDC tokens, ignores environment approvals and most org policies, and its cache and artifact behavior is partial. Treat it as a fast syntax and logic check, and treat the GitHub run as the real result.

| Day | Lab | Run locally with `act`? | Run on GitHub? |
|---|---|---|---|
| 1 | lab-1 | Yes | Yes |
| 2 | lab-2 | Yes (secrets via `-s`) | Yes |
| 3 | lab-3 | Partly (Ubuntu legs only) | Yes (needed for the Windows leg) |
| 4 | lab-4 | Yes (reusable and composite) | Yes |
| 5 | actions/ | Yes (JS and Docker actions) | Yes |
| 6 | lab-6 | No (OIDC and permissions are GitHub-only) | Yes |
| 7 | review | n/a | n/a |

## Day 1: Fundamentals and triggers

```bash
actionlint .github/workflows/lab-1-hello.yml
act workflow_dispatch -W .github/workflows/lab-1-hello.yml --input who=Mac
```

Then run it on GitHub and compare the two logs: `gh workflow run "Lab 1 - Hello Actions" -f who=Mac`.

To practice other triggers locally, feed `act` an event payload: `act push -n` shows which jobs a push would start without running them (`-n` is a dry run). `act -l` lists every job it found.

## Day 2: Contexts, variables, secrets

```bash
act workflow_dispatch -W .github/workflows/lab-2-contexts.yml -s DEMO=local-value --var LEVEL=repo
```

- `-s NAME=value` supplies a secret (omit the value to be prompted, so it stays out of shell history).
- `--var NAME=value` supplies a configuration variable.
- For GitHub, create the real secret first: `gh secret set DEMO` and `gh variable set LEVEL --body repo`.
- Compare `runner.os` in both runs: it prints `Linux` either way, but `github.*` context values differ, which is the point of the lab.

## Day 3: Matrix, artifacts, cache

```bash
act workflow_dispatch -W .github/workflows/lab-3-matrix-artifacts.yml --matrix os:ubuntu-latest
act workflow_dispatch -W .github/workflows/lab-3-matrix-artifacts.yml --artifact-server-path /tmp/act-artifacts
```

- `--matrix key:value` restricts the matrix to the legs `act` can run; the Windows leg will not run locally.
- `--artifact-server-path` enables upload/download-artifact locally.
- For services (Postgres/Redis exercises), Docker Desktop must be running. Inside a container job, use the service label as hostname; on the runner directly, use `localhost`.
- Cache hits are only reliable on GitHub. Run the lab twice there and confirm the second run reports a cache hit.

## Day 4: Reuse, environments, concurrency, debugging

```bash
act workflow_dispatch -W .github/workflows/lab-4-reusable-caller.yml
```

- Local reusable workflows (`uses: ./.github/workflows/...`) and local composite actions work in `act`.
- Environments with required reviewers and `concurrency` cancellation are GitHub-only. Create an environment in **Settings → Environments**, add yourself as reviewer, and run it on GitHub.
- Debugging locally: `act -v` for verbose output. On GitHub, set debug logging with `gh secret set ACTIONS_STEP_DEBUG --body true` and `gh secret set ACTIONS_RUNNER_DEBUG --body true`, or re-run a job with **Enable debug logging** (`gh run rerun <id> --debug`).

## Day 5: Authoring custom actions

Extra tools for the exercises in `actions/README.md`:

```bash
brew install node                      # Node 20+ for the JavaScript action
cd actions/greet-js
npm init -y
npm install @actions/core
npm install -D @vercel/ncc
npx ncc build index.js -o dist         # bundle; point action.yml main at dist/index.js
```

- Docker action (Exercise B): Docker Desktop must be running; test the image on its own first with `docker build -t greet-docker actions/greet-docker && docker run --rm greet-docker`.
- Test a local action through a workflow that does `actions/checkout` then `uses: ./actions/<name>`, and run it with `act`.
- Docker container actions only run on Linux runners. To see the failure the lab asks about, run the workflow on GitHub with `windows-latest`; `act` cannot reproduce it.
- Tagging practice: `git tag v1.0.0 && git tag -f v1 && git push origin v1.0.0 && git push -f origin v1` (moving the `v1` tag is the one case where force-pushing a tag is expected).

## Day 6: Enterprise, runners, security, OIDC

**Lab 6 (OIDC and permissions)** must run on GitHub because the OIDC token comes from GitHub:

```bash
gh workflow run "Lab 6 - Permissions and OIDC Token"
gh run watch
```

**Self-hosted runner on your Mac** (the hands-on way to learn runner labels):

1. In your repo go to **Settings → Actions → Runners → New self-hosted runner → macOS**, and copy the download and configure commands it shows (the token is short-lived, so copy it fresh).
2. Configure it as ephemeral, which is the hardened option the lesson covers:

   ```bash
   mkdir ~/actions-runner && cd ~/actions-runner
   # download and extract using the commands from the GitHub page, then:
   ./config.sh --url https://github.com/gvarun17/github-actions-gh200 --token <TOKEN> --ephemeral --labels mac-lab
   ./run.sh
   ```

3. Target it from a test workflow with `runs-on: [self-hosted, macOS, ARM64, mac-lab]` (use `X64` on Intel Macs). Auto labels are `self-hosted`, the OS (`macOS`), and the architecture; `mac-lab` is the custom one.
4. After one job the ephemeral runner unregisters itself, which you can confirm on the Runners page.
5. Safety: use self-hosted runners only on a private repo or one without outside contributors, since forked PRs could otherwise run code on your Mac. Remove the runner when done (`./config.sh remove --token <TOKEN>`).

**GitHub Actions Importer** (awareness topic):

```bash
gh extension install github/gh-actions-importer
gh actions-importer update            # pulls the Docker image (needs Docker Desktop)
gh actions-importer configure         # choose a source CI (e.g. Jenkins) and add its URL/token
gh actions-importer audit jenkins --output-dir tmp/audit
```

You do not need a real Jenkins server for the exam; knowing the four commands (`audit`, `forecast`, `dry-run`, `migrate`) is enough.

## Day 7: Review

No new tooling. Useful for the final lap:

```bash
actionlint                              # catches many of the "subtle YAML bug" exam patterns
act -l                                  # list jobs and the events that trigger them
gh run list --limit 10                  # confirm every lab ran green on GitHub
```

## Troubleshooting

- **`Cannot connect to the Docker daemon`**: open Docker Desktop and wait until it says it is running.
- **Slow first `act` run**: it is pulling a large image; later runs are fast.
- **`exec format error` on Apple Silicon**: confirm `~/.actrc` has `--container-architecture linux/amd64`.
- **Action fails locally but works on GitHub**: check the table above first; the feature is probably GitHub-only.
- **Secrets showing up in shell history**: pass `-s NAME` with no value and enter it at the prompt, or use `--secret-file`.
