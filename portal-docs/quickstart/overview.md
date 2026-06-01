# Quickstart Environment

The Quickstart stack is a fully-configured Egeria environment pre-loaded with Coco Pharmaceuticals data. It is designed for demos, learning, and hands-on exploration.

---

## What's included

| Service | Port | Purpose |
|---|---|---|
| Egeria platform | 9443 | Metadata store and API server |
| pyegeria-web | 8000 | FastAPI backend — Dr. Egeria MCP, portal API |
| Apache web server | 8085 | Portal, documentation, static content |
| Jupyter Lab | 7888 | Interactive Python notebooks |
| Obsidian (container) | 3000 | Browser-based Obsidian via KasmVNC |
| Shared PostgreSQL | 5442 | Metadata + demo auth database |
| Kafka | 9194 | Event bus for Egeria integration daemons |

---

## Operating modes

| Mode | Who | How to enable |
|---|---|---|
| **Local** | Single developer on their own machine | `DEMO_MODE=false` (default) |
| **Demo** | Multiple external users via registration | `DEMO_MODE=true` |

- [Local setup guide](local/overview.md)
- [Demo environment guide](demo/overview.md)

---

## Starting the stack

```bash
cd compose-configs/egeria-quickstart
docker compose -f egeria-quickstart.yaml up -d
```

Egeria takes approximately 2–3 minutes to fully initialise after startup. The platform healthcheck will turn green once it is ready.

---

## Pre-loaded data

The Quickstart stack starts with:

- **Coco Pharmaceuticals** metadata — glossaries, governance zones, data assets, lineage, and supply chains
- **Demo users** (in demo mode) — pre-configured admin account via `ADMIN_BOOTSTRAP_EMAIL`
- **Personas** — 11 Coco employees with different roles and perspectives

See [Coco Pharmaceuticals](coco/overview.md) for background on the scenario.
