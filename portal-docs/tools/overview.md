# Tools Overview

The Egeria Workspaces portal includes several integrated tools for exploring, managing, and analysing your metadata environment. All tools are available in both the Quickstart and Freshstart environments.

---

## Available tools

| Tool | URL | Purpose |
|---|---|---|
| [Tech Catalog](tech-catalog.md) | `/tech-catalog` | Search and browse technical assets — infrastructure, data stores, APIs, processes, and technology types — with schemas, context diagrams, and lineage |
| [Egeria Explorer](egeria-explorer.md) | `/egeria-explorer` | Browse the type system, glossary terms, governance structures, digital products, information supply chains, external identifiers, and more — one tab per element category |
| [Lineage Explorer](lineage-explorer.md) | `/lineage` | Trace data flow end-to-end; local and full lineage graphs, field-level mappings, time-travel queries, and information supply chain filtering |
| [Egeria Audit](egeria-audit.md) | `/egeria-audit` | Review exceptions, certifications, and licenses in use across the metadata landscape, plus who has access to Egeria |
| [Egeria Operations](egeria-operations.md) | `/egeria-operations` | Monitor and operate the Egeria runtime — servers, integration connectors, governance engines, and engine actions |
| [Resource Explorer](resource-explorer.md) | `/resource-explorer` | Scout, assess, discover, and enrich resources *(preview — not yet enabled)* |
| [My Egeria](my-egeria.md) | `/my-egeria/` | Textual (terminal-style) view of your own Egeria profile, roles, teams, and actions |
| [Dr. Egeria](dr-egeria/overview.md) | `/dr-egeria` | Write Egeria commands as Markdown and send them from the portal or Obsidian to read and update metadata |
| [Egeria Advisor](egeria-advisor.md) | `/advisor` | AI-powered guidance for navigating and querying your Egeria metadata environment |
| [Jupyter Lab](jupyter.md) | port 7888 / 8888 | Interactive Python notebooks for data exploration and hands-on Egeria API work |
| [Obsidian Vault](obsidian.md) | port 7860 / 8860 | Containerised Obsidian for vault-based note-taking and Dr. Egeria command authoring |

---

## Navigation between tools

The tools are designed to work together. Common cross-tool flows:

- **Tech Catalog → Lineage Explorer** — click "Open in Lineage Explorer" on any asset's lineage pane to trace the full data flow
- **Lineage Explorer → Egeria Explorer** — click "View in Explorer" on an information supply chain to see its full definition
- **Lineage Explorer / Egeria Explorer → Tech Catalog** — "View in Catalog" links bring you directly to the correct asset section and detail view
- **Egeria Operations → Tech Catalog** — "Open in The Catalog" on a server row jumps to that server's asset detail
- **Bookmarking** — most tools let you bookmark a specific screen or item (☐ / ☑ toggle) to **My Bookmarks** on the portal home page, for one-click return later
- **Portal → any tool** — all tools are accessible as tiles on the main portal page

---

## Further reading

- [Quickstart environment overview](../quickstart/overview.md)
- [Freshstart environment overview](../freshstart/overview.md)
- [Egeria project documentation](https://egeria-project.org)
