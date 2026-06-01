# Jupyter Lab

Jupyter Lab provides interactive Python notebooks for Egeria API exploration, data science work, and hands-on learning.

Access it from the portal tile or directly at `http://localhost:7888/?token=egeria`.

---

## Getting started

The notebooks are pre-loaded with the Egeria Python client (`pyegeria`). The workbooks directory is mounted at `/home/jovyan/coco-workbooks` inside the container.

### Default token

```
egeria
```

---

## Available workbook collections

| Path | Contents |
|---|---|
| `/home/jovyan/coco-workbooks` | Coco Pharmaceuticals scenario workbooks |
| `/home/jovyan/workbooks` | General Egeria API workbooks |
| `/home/jovyan/work` | Your personal working directory |

---

## Connecting to Egeria from a notebook

```python
from pyegeria import EgeriaTech

egeria = EgeriaTech(
    view_server="qs-view-server",
    platform_url="https://host.docker.internal:9443",
    user_id="erinoverview",
    user_pwd="secret"
)
```

---

## Further reading

- [pyegeria documentation](https://egeria-project.org/guides/developer/python-client/)
- [Coco Pharmaceuticals scenarios](../quickstart/coco/scenarios.md)
