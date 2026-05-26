# egeria-workspaces — Claude Code instructions

## Git commits

**All commits must be signed.** The global git config has `commit.gpgsign=true` and `gpg.format=ssh` set. Never use `--no-gpg-sign`, `--no-verify`, or any other flag that bypasses signing.

When committing, always pass the message via a heredoc. Every commit **must** include both a `Signed-off-by` trailer (DCO) and a `Co-Authored-By` trailer:
```
git commit -m "$(cat <<'EOF'
type(scope): short summary

Body here.

Signed-off-by: Dan Wolfson <dan.wolfson@pdr-associates.com>
Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

The `Signed-off-by` is required by the `.githooks/commit-msg` hook (active via `core.hooksPath=.githooks`) and the `commit-policy.yml` GitHub Actions workflow. Commits missing this trailer will be rejected by the hook.

Stage specific files by name rather than `git add -A` or `git add .` to avoid accidentally including runtime files (e.g. `runtime-volumes/`, `*.db`, `.env`).

## Project layout

- `compose-configs/egeria-quickstart/` — public demo environment (FastAPI + Apache)
- `compose-configs/shared-infra/` — shared Kafka, PostgreSQL (port 5442)
- `runtime-volumes/` — Docker bind-mount data, never commit contents

## Key services

| Service | Container name | Notes |
|---------|---------------|-------|
| Egeria platform | `quickstart-egeria-main` | Metadata store on `egeria` DB |
| FastAPI web | `quickstart-pyegeria-web` | Demo auth + Dr. Egeria API |
| Shared Postgres | `egeria-shared-postgres` | Port 5442, multiple schemas |
