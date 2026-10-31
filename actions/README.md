# Day 5 Lab: Custom Actions

1. `greet-composite/` is a working composite action (called by lab 4).
2. Exercise A: create `actions/greet-js/` with an `action.yml` (`using: node20`) and an `index.js` using `@actions/core` to read input `who` and set output `time`. Bundle with `@vercel/ncc build index.js -o dist`, point `main` at `dist/index.js`.
3. Exercise B: create `actions/greet-docker/` with a `Dockerfile` and `entrypoint.sh`; set `runs.using: docker` and `image: Dockerfile`. Confirm it fails on a Windows runner.
4. Call each from a workflow with `uses: ./actions/<name>` after `actions/checkout`.
5. Tag a release `v1.0.0` and a moving `v1` tag to practice versioning.
