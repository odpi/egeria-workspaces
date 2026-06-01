# Getting Started with Freshstart

---

## 1. Configure your environment

```bash
cd compose-configs/egeria-freshstart
cp .env.example .env
```

Edit `.env`:
```
HOST_FQDN=localhost
KAFKA_BOOTSTRAP_SERVERS=localhost:9194
```

---

## 2. Start the stack

```bash
docker compose -f egeria-freshstart.yaml up -d
```

Egeria takes 2–3 minutes to initialise. Check readiness:
```bash
curl -k https://localhost:9443/open-metadata/platform-services/users/garygeeke/server-platform/origin
```

---

## 3. Open the portal

**http://localhost:8086**

---

## 4. Connect with pyegeria

```python
from pyegeria import EgeriaTech

egeria = EgeriaTech(
    view_server="fs-view-server",
    platform_url="https://localhost:9443",
    user_id="garygeeke",
    user_pwd="secret"
)

# Check the platform is running
print(egeria.get_platform_origin())
```

---

## 5. Connect Dr. Egeria

In Obsidian (or via the MCP plugin), set:
- **MCP Server URL:** `http://localhost:8000/sse`
- **Egeria Platform URL:** `https://host.docker.internal:9443`
- **View Server:** `fs-view-server`
- **User ID / Password:** `garygeeke` / `secret`

---

## Next steps

- Explore the [Type System](http://localhost:8086/egeria-explorer) to understand the open metadata model
- Create your first [glossary term](../tools/dr-egeria/templates-basic.md) using Dr. Egeria
- Browse the [Jupyter workbooks](../tools/jupyter.md) for API examples
