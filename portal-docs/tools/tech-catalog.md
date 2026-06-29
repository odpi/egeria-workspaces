# Tech Catalog

The Tech Catalog is a searchable browser for all technical metadata registered in Egeria. It surfaces IT infrastructure, data assets, APIs, processes, technology types, and business glossary terms in a unified view with context diagrams, schemas, and lineage.

Access it from the portal tile or directly at `/catalog`.

---

## Sections

| Section | What it shows | Sub-tabs |
|---|---|---|
| **IT Infrastructure** | Servers, hosts, applications, and their software capabilities | IT Infrastructure, Software Capabilities, Endpoints |
| **Data Assets** | Data stores, feeds, and sets | Data Stores, Data Feeds, Data Sets |
| **APIs** | Deployed API definitions | APIs |
| **Processes** | Running software components and actions | Software Components, Actions |
| **Technology Types** | Egeria's registered technology classifications | Types list, Hierarchy |
| **Glossary** | Business terms, folders, and their relationships | Glossary terms |

---

## Detail pane

Selecting any item opens a detail pane on the right. For most asset types this includes:

- **Properties** — all metadata properties with classifications
- **Context Diagram** — Mermaid diagram showing the element in its broader context (rendered immediately when available)
- **Additional diagrams** — lineage, field-level, supply-chain, and other diagrams where present
- **Relationships** — related elements with "View →" navigation links
- **Schema** — column / attribute list (data assets only)
- **Lineage** — direct lineage graph and link to Lineage Explorer

---

## Cross-navigation

Clicking **"View →"** on a relationship card jumps directly to that element in its correct section, even when the related element is a different type (e.g. following a relationship from a Data Store to a Software Server navigates to IT Infrastructure).

Clicking **"View in Catalog"** from another tool (e.g. Lineage Explorer, Egeria Explorer) brings you to the correct section and detail view for any asset GUID automatically.

---

## Lineage

The **Lineage** sub-pane shows the direct lineage graph (Mermaid). The **Open in Lineage Explorer** button opens the full [Lineage Explorer](lineage-explorer.md) view for the selected asset.

---

## Copying raw JSON

Every detail pane has a **`{ } Copy JSON`** button in its header row. Clicking it copies the full raw JSON payload for the selected element to the clipboard — useful for pasting into notebooks, debugging API responses, or feeding data into other tools.

The button shows **✓ Copied** (green) on success or **✕ Failed** (red) on failure, then resets after two seconds.

---

## Searching

Each section has a search box that filters by display name, qualified name, and description. Leaving the search box empty returns all elements.

---

## Personas

The persona selected in the portal determines which Egeria user identity is used for catalog queries. Different personas may have different visibility into governance zones and classified assets.

---

## Further resources

- [Lineage Explorer](lineage-explorer.md) — full-featured lineage tracing tool
- [Egeria Explorer](egeria-explorer.md) — type system, governance, digital products, and ISC views
- [Coco Pharmaceuticals scenarios](../quickstart/coco/scenarios.md) — guided catalog walk-throughs
