# Egeria Explorer

Egeria Explorer is the primary browser-based interface for navigating Egeria metadata. It provides tab-by-tab views of types, glossary terms, lineage, governance blueprints, digital products, and more.

Access it from the portal tile or directly at `/egeria-explorer`.

---

## Tabs overview

| Tab | What it shows | Good for |
|---|---|---|
| **Type System** | All open metadata types and their inheritance | Developers, architects |
| **Glossary** | Business terms and their definitions | Business users, data stewards |
| **Data Design** | Data structures, schemas, quality rules | Data analysts, engineers |
| **Governance** | Policies, zones, security classifications, compliance rules | Governance officers |
| **Digital Products** | Published data products and their assets | Data consumers |
| **ISC** | Information supply chains and data lineage | Data engineers, auditors |
| **Solution Architect** | Blueprints, solution components, and roles | Architects |
| **Perspectives** | Organisational views — teams, roles, responsibilities | HR, management |

---

## Switching personas

The persona you select in the portal determines which Egeria user ID is used for Explorer queries. Different personas may have different visibility into governance zones and classified assets.

---

## Dr. Egeria Execute panel

Every command template in Egeria Explorer has an **Execute** tab alongside the parameter reference. It lets you run individual Dr. Egeria commands directly from the browser without needing Obsidian or a markdown file.

### Using it

1. Select a command family and template from the left-hand list.
2. Switch to the **Execute** tab in the detail panel.
3. Choose a **directive**:
   - **Display** — preview current metadata; no changes made.
   - **Validate** — check parameters without writing anything.
   - **Process** — create or update metadata in Egeria. ⚠ Irreversible.
4. For Create/Update/Link commands, a **Verb** toggle lets you switch to the counterpart verb (e.g. Create ↔ Update, Link ↔ Unlink) without leaving the template.
5. Fill in the required parameters (highlighted in green) and any optional ones you need.
6. Click **▶ Run**.

### Reading the result

After execution the panel shows a status banner, then any errors, then the full output document:

| Banner | Meaning |
|---|---|
| ✓ **Completed** — *N of N commands succeeded* | All commands ran without errors |
| ⚠ **Partial** — *X of N commands succeeded — Y failed* | Mixed outcome; metadata may be partially updated |
| ✗ **Failed** — *N of N commands failed* | Nothing was written; safe to retry after fixing inputs |

**Validation Errors** (amber) — parameter problems caught before any Egeria call. Fix the inputs and re-run; no metadata was changed.

**Execution Errors** (red) — Egeria returned an error mid-run. The plan may be partially applied; investigate before retrying.

The output document below the error lists is the full augmented plan markdown — the same content that would be saved to the Dr. Egeria outbox in Obsidian.

### When to use Obsidian instead

The Execute panel is designed for testing individual commands. For production workflows — especially multi-command sequences with narrative prose — write a Dr. Egeria markdown document in Obsidian and send it via the **Call Dr. Egeria** plugin. See [Dr. Egeria overview](dr-egeria/overview.md) for details.

---

## Copying raw JSON

Every detail panel in Egeria Explorer has a **`{ } Copy JSON`** button in its header row. Clicking it copies the complete raw JSON payload for the selected element to the clipboard — useful for pasting into notebooks, debugging, or feeding into other tools.

This is available on all detail views: Type System types, classifications and relationships, Glossary terms/folders, Data Design elements, Governance definitions, Digital Products, ISC, Solution Architect blueprints and components, Perspectives, Locations, Actors, Communities, Note Logs, Projects, Reference Data, Valid Values (per-entry and copy-all for the full result set), and Report Specs.

The button shows **✓ Copied** (green) on success or **✕ Failed** (red) on failure, then resets after two seconds.

---

## Links from documentation

Where documentation refers to a specific type or glossary term, you can explore it directly:

- Type System: `/egeria-explorer` → Type System tab → search for the type name
- Glossary term: `/egeria-explorer` → Glossary tab → search for the term

---

## Further resources

- [Tech Catalog](tech-catalog.md) — browse and search technical assets; includes schemas, lineage sub-pane, and context diagrams
- [Lineage Explorer](lineage-explorer.md) — full-featured data lineage tracing tool
- [Egeria project documentation](https://egeria-project.org) — full open metadata type reference
- [Coco Pharmaceuticals scenarios](../quickstart/coco/scenarios.md) — guided Explorer walk-throughs
