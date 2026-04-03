<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Contributing to Egeria

This project welcomes contributors from any organization or background, provided they are
willing to follow the simple processes outlined below, as well as adhere to the 
[Code of Conduct](https://egeria-project.org/guides/community/).

Review the [community guide](./Community-Guide.md) to find out more.

## Commit requirements (main branch)

This repository uses a lightweight commit policy for pull requests targeting `main`:

1. every commit must include a DCO signoff trailer (`Signed-off-by:`), and
2. every commit subject should follow a consistent format.

Use:

```bash
git commit -s -m "type(scope): short summary"
```

### Accepted subject format

`type(scope): summary`

Where:

- `type` is one of: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `build`, `ci`, `perf`, `revert`
- `(scope)` is optional and should identify the area changed (for example `freshstart`, `quickstart`, `docs`, `jupyter`)
- `summary` is a short plain-English description

Examples:

- `feat(freshstart): add isolated fs-* server startup flow`
- `fix(jupyter): ensure pipx and pyegeria CLI are installed`
- `docs(readme): clarify local vs multi-host behavior`
- `chore(secrets): seed missing template files without overwrite`

Examples to avoid:

- `updates`
- `fixes`
- `stuff`
- `WIP`

## Local commit linting (recommended)

This repository includes a local `commit-msg` hook in `.githooks/commit-msg`.

Enable it once per clone:

```bash
git config core.hooksPath .githooks
chmod +x .githooks/commit-msg
```

The hook checks both signoff and subject format before the commit is created.

## CI enforcement (PRs to main)

GitHub Actions validates commit policy on pull requests targeting `main`.
If any commit is missing signoff or has a non-conforming subject, the check fails.

## Back out / disable locally

If you want to temporarily stop local hook checks in your clone:

```bash
git config --unset core.hooksPath
```

To bypass hooks for a one-off commit:

```bash
git commit --no-verify -m "..."
```

Note: PR CI still enforces policy for merges to `main`.



----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
