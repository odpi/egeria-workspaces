# Freshstart Environment

Freshstart is a clean-slate Egeria environment for development and experimentation. Unlike Quickstart, it starts with no pre-loaded metadata — you define your own types, assets, and governance structures from scratch.

---

## What's included

| Service | Port | Purpose |
|---|---|---|
| Egeria platform | 9443 | Metadata store and API server |
| pyegeria-web | 8000 | FastAPI backend — Dr. Egeria MCP |
| Apache web server | 8086 | Portal and documentation |
| Jupyter Lab | 7888 | Interactive Python notebooks |
| Shared PostgreSQL | 5442 | Metadata database |
| Kafka | 9194 | Event bus |

---

## When to use Freshstart vs Quickstart

| Use case | Recommended environment |
|---|---|
| Learning Egeria with realistic data | Quickstart |
| Building a custom metadata model | Freshstart |
| Developing Egeria connectors | Freshstart |
| Running demos for external audiences | Quickstart (demo mode) |
| API exploration with pyegeria | Either |

---

## Starting the stack

```bash
cd compose-configs/egeria-freshstart
docker compose -f egeria-freshstart.yaml up -d
```

Open the portal at **http://localhost:8086**.

---

## Further reading

- [Getting started with Freshstart](getting-started.md)
- [Egeria project documentation](https://egeria-project.org)
