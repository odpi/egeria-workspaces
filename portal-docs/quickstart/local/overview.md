# Quickstart — Local Setup

Local mode runs the full Quickstart stack on your own machine for personal exploration and development. There is no user registration — you access all tools directly.

---

## Prerequisites

- Docker Desktop (Mac/Windows) or Docker Engine + Compose (Linux), or Podman with podman-compose
- 8 GB RAM allocated to the container engine (16 GB recommended)
- Ports 8085, 8000, 9443, 7888, 3000, 9194, 5442 available

---

## Start the stack

From the repository root:

```bash
./quick-start-local
```

The script handles everything:
- Detects your container engine (Docker or Podman)
- Generates `compose-configs/egeria-quickstart/.env` with your hostname and Kafka config
- Generates `exchange-quickstart/config/config_workspaces.json` from the template (sets hostnames and service names for Jupyter / pyegeria)
- Seeds Obsidian vault config on first run
- Starts Egeria, pyegeria-web, Jupyter, Apache, and Obsidian
- Waits for Egeria to become healthy (JVM typically takes 2–5 min)

Open the portal at **http://\<your-hostname\>:8085** or **http://localhost:8085**.

---

## Configuration files

| File | Purpose |
|------|---------|
| `compose-configs/egeria-quickstart/.env` | Generated on every run — do not commit or hand-edit |
| `compose-configs/egeria-quickstart/.env.example` | Documents all available variables |
| `exchange-quickstart/config/config_workspaces.json` | Generated on every run — pyegeria / Jupyter config with your hostname |
| `exchange-quickstart/config/config_workspaces.json.template` | Tracked template with `localhost` placeholders — edit this to change defaults |

To change a persistent default (e.g. `console_width`, Egeria paths, logging), edit the `.template` file. The runtime `config_workspaces.json` is regenerated fresh on each startup.

---

## Key differences from demo mode

| Feature | Local | Demo |
|---|---|---|
| User registration / login | No — open access | Yes — email + password |
| HTTPS / TLS | No | Yes (via `--demo` with your certs) |
| Persona selection | Stored in browser (localStorage) | Stored per account |
| Admin panel | Not needed | `/admin` |
| Email notifications | Not needed | Requires Resend API key |

---

## Useful flags

```bash
./quick-start-local --demo             # Enable demo mode (auth, HTTPS, SSL certs)
./quick-start-local --refresh-platform # Force pull of latest Egeria base image
./quick-start-local --help
```
