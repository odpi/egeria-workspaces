# Lineage Explorer

Lineage Explorer is a dedicated tool for tracing data flow and dependencies across the IT landscape. It gives a single "focus asset" a rich lineage-centred view with time-travel queries, multiple graph types, information supply chain filtering, and a navigable linked-assets table.

Access it from the portal tile or directly at `/lineage`. It can also be opened from the [Tech Catalog](tech-catalog.md) via the **Open in Lineage Explorer** button on any asset's lineage pane.

---

## Finding an asset

Use the search box at the top left to find assets by name. Select an asset from the results to set it as the focus.

You can also deep-link directly to a focus asset: `/lineage?guid={guid}`.

---

## Focus asset card

Shows the selected asset's type, display name, qualified name, description, and creation timestamp.

Click the bookmark toggle (☐ / ☑) next to the asset name to save it to **My Bookmarks** on the portal — it links back to `/lineage?guid={guid}` so you can jump straight to that asset's lineage view later. Bookmarking requires an active persona (Quickstart) or a logged-in account (Freshstart).

---

## Time slider

The time slider lets you query the lineage graph at a historical point in time. The range spans from the asset's creation date to now. Slide left to travel back in time; release the slider to fetch the graph at that point.

---

## Local lineage

Shows elements directly connected to the focus asset by lineage relationships. Includes:

- **Local lineage graph** — Mermaid diagram of direct connections
- **Field-level lineage graph** — field-to-field data mappings (when available)
- **Lineage linkage table** — tabular view of connected elements; click **Set as Focus** on any Asset-type row to pivot the whole view to that element

---

## Information supply chains

Lists the information supply chains (ISC) that include the focus asset. Click a supply chain to select it, then use the ISC filter options when loading the full lineage graph:

- **Limit to ISC** — show only lineage within the selected supply chain
- **Highlight ISC** — show full lineage with the selected supply chain highlighted

**View in Explorer** opens the selected ISC in [Egeria Explorer](egeria-explorer.md).

---

## Full asset lineage

Click **Load Full Lineage** to fetch the end-to-end lineage graph. This shows all data and control flow paths through the focus asset across the entire IT landscape.

Includes:
- **Full lineage graph** — end-to-end Mermaid diagram
- **Edge graph** — extreme sources and destinations only
- **Linked assets table** — all assets in the full lineage graph with display name, description, GUID, qualified name, creation date, and last-updated date

The full lineage fetch is on-demand because it can be expensive. It is only available when local lineage relationships exist.

---

## Navigation tips

- **Back/forward** in the browser works — each **Set as Focus** pivot updates the URL so history is preserved
- Clicking **Open in Lineage Explorer** from Tech Catalog pre-selects the asset you were viewing
- The time slider defaults to "now" — move it left to see historical lineage state

---

## Further resources

- [Tech Catalog](tech-catalog.md) — browse assets by type; entry point for most lineage investigations
- [Egeria Explorer](egeria-explorer.md) — ISC detail, governance, and digital product views
