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
- **Highlight ISC** — show full lineage with the selected supply chain highlighted. Egeria draws a thin line for any edge tagged with a *different* supply chain; edges with no supply chain stay thick. So highlighting only changes the picture when the lineage crosses into another supply chain

**View in Explorer** opens the selected ISC in [Egeria Explorer](egeria-explorer.md).

---

## Full asset lineage

Click **Load Full Lineage** to fetch the end-to-end lineage graph. This shows all data and control flow paths through the focus asset across the entire IT landscape.

Includes:
- **Full lineage graph** — end-to-end Mermaid diagram
- **Edge graph** — extreme sources and destinations only
- **Linked assets table** — all assets in the full lineage graph with display name, description, GUID, qualified name, creation date, and last-updated date

The full lineage fetch is on-demand because it can be expensive. It is only available when local lineage relationships exist. While it loads, the page shows the elapsed time and a **Cancel** button. Cancel stops the browser waiting; Egeria may still finish the walk on its side.

When the focus asset belongs to a supply chain, a button for each supply chain is offered first. Limiting the walk to one supply chain usually takes seconds, where the whole estate can take minutes.

### Hop limit (Egeria 6.3 and later)

From Egeria 6.3 the lineage walk stops a set number of hops from the focus asset in each direction (8 by default). The page detects this from the response and then shows:

- **Hops each way** — a slider from 1 to 15, defaulting to 8. **No limit…** removes the limit after a warning: on a large estate it can take minutes, and the Portal gives up after about 5 minutes.
- **A summary line** — the limit used, the deepest element found, and how many elements continue past the limit. When none do, the graph is complete.
- **Dashed rows** in the linked assets table mark the elements where the walk stopped with more lineage beyond, and a **Hops** column gives each element's distance from the focus asset.
- **Expand from here** — on a dashed row for an asset, makes it the focus asset and loads its full lineage with the same settings.
- **Also follow actions and assignments** — Egeria 6.3 no longer follows RequestForActionTarget and AssignmentScope relationships by default; tick this to include them again.
- **Advanced relationship scope** — "Include only" replaces Egeria's default relationship types (a supertype such as `LineageRelationship` includes its subtypes); "Skip" removes types.

On an older platform these controls are hidden and a one-line note says why: the platform does not limit the walk, so the graph shown is the whole walk.

If Egeria fails to build the graph, the error banner shows Egeria's own message rather than reporting "no lineage". For example, some Egeria 6.3 builds reject lineage that reaches a Digital Product (`OMAG-REPOSITORY-HANDLER-404-001 … of type DigitalProduct rather than type Asset`).

---

## Navigation tips

- **Back/forward** in the browser works — each **Set as Focus** pivot updates the URL so history is preserved
- Clicking **Open in Lineage Explorer** from Tech Catalog pre-selects the asset you were viewing
- The time slider defaults to "now" — move it left to see historical lineage state

---

## Further resources

- [Tech Catalog](tech-catalog.md) — browse assets by type; entry point for most lineage investigations
- [Egeria Explorer](egeria-explorer.md) — ISC detail, governance, and digital product views
