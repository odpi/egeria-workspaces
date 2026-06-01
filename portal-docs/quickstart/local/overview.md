# Quickstart — Local Setup

Local mode runs the full Quickstart stack on your own machine for personal exploration and development. There is no user registration — you access all tools directly.

---

## Prerequisites

- Docker Desktop (Mac/Windows) or Docker Engine + Compose (Linux)
- 8 GB RAM allocated to Docker (16 GB recommended)
- Ports 8085, 8000, 9443, 7888, 3000, 9194, 5442 available

---

## Initial configuration

1. Copy the environment template:
   ```bash
   cd compose-configs/egeria-quickstart
   cp .env.example .env
   ```

2. Edit `.env` — the minimum required settings:
   ```
   HOST_FQDN=localhost         # or your machine's hostname
   KAFKA_BOOTSTRAP_SERVERS=localhost:9194
   ```

3. Optional but recommended — set your Obsidian preference:
   ```
   # Use your local Obsidian app (vault name or obsidian:// URI)
   OBSIDIAN_VAULT_URL=coco-workbooks

   # Or leave empty to use the containerised Obsidian at port 3000
   OBSIDIAN_VAULT_URL=
   ```

---

## Start the stack

```bash
cd compose-configs/egeria-quickstart
docker compose -f egeria-quickstart.yaml up -d
```

Open the portal at **http://localhost:8085**.

---

## Key differences from demo mode

| Feature | Local | Demo |
|---|---|---|
| User registration / login | No — open access | Yes — email + password |
| Persona selection | Stored in browser (localStorage) | Stored per account |
| Obsidian session lock | Available (auto-clears on restart) | Full lock + reservation system |
| Admin panel | Not needed | `/admin` |
| Email notifications | Not needed | Requires Resend API key |

---

## Configuration reference

All settings are in `compose-configs/egeria-quickstart/.env`. See `.env.example` for the full list with descriptions.

Key variables:

| Variable | Default | Purpose |
|---|---|---|
| `HOST_FQDN` | — | Hostname used by Egeria and Kafka |
| `OBSIDIAN_VAULT_URL` | *(empty)* | Local Obsidian vault name or URI |
| `OBSIDIAN_LOCK_ENABLED` | `true` | Set `false` to disable session lock |
| `EGERIA_ADVISOR_URL` | `http://localhost:8080/` | Egeria Advisor URL if running |
