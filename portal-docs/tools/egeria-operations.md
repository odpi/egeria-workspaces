# Egeria Operations

Egeria Operations is the runtime control panel for the Egeria platform itself — servers, integration connectors, governance engines, and engine actions — rather than a view of catalogued metadata.

Access it from the portal tile or directly at `/egeria-operations`.

---

## Tabs overview

| Tab | What it shows |
|---|---|
| **Servers** | All servers registered on the connected platform, grouped by type (view servers, metadata access servers, integration daemons, engine hosts). Start/stop where permitted; select a server for a detail panel |
| **Integration Connectors** | Every integration connector on an Integration Daemon server, with live status pulled from Egeria's `/instance/report` endpoint |
| **Governance Engines** | Governance engines on an Engine Host server, their configuration, and refresh/start/stop controls |
| **Engine Actions** | The ecosystem-wide log of governance engine actions — requests, status, and results; groupable by action name |

The left-nav server list refreshes automatically every 30 seconds so status stays current without a manual reload.

---

## Integration Connectors — why it can be slow to appear

Egeria's `/instance/report` endpoint polls every connector for live status and can take several minutes on a busy platform. Rather than block the page, this tab loads instantly with cached or partial data and shows an amber "stale" banner while a fresh report is fetched in the background — it updates itself within about a minute without any action needed. This is expected behavior, not a hang.

---

## Cross-navigation

From the **Servers** tab, a selected server's detail panel has an **Open in The Catalog** button that jumps straight to that server's asset detail in [Tech Catalog](tech-catalog.md).

---

## Bookmarking

Not yet available on this tool.

---

## Further resources

- [Tech Catalog](tech-catalog.md) — asset-level detail for the servers and capabilities shown here
- [Egeria Audit](egeria-audit.md) — compliance and access, a different kind of "audit" of the metadata itself rather than the runtime
