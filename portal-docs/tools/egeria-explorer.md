# Egeria Explorer

Egeria Explorer is the primary browser-based interface for navigating Egeria metadata. It provides tab-by-tab views of types, glossary terms, lineage, governance blueprints, digital products, and more.

Access it from the portal tile or directly at `/egeria-explorer`.

---

## Search

A full-width **Search** card sits at the top of the Home screen — keyword search across *every* element type in one call, not scoped to whichever tab you're in.

- After a search runs, a "Types in these results" row of chips shows the real types actually found (e.g. `RelationalColumn (12)`, `GlossaryTerm (4)`) — not a fixed pre-search category list, since Egeria has several hundred entity types and a curated picker can only ever cover a slice of them.
- Clicking a chip re-runs the search scoped to that exact type, giving you a complete count for it rather than whatever fit in the first page of unscoped results.
- Results are headed by their real type name, so even uncommon types get their own clearly labelled section instead of being lumped under a generic "Other" heading.

---

## Tabs overview

### Explore

A quick-start subset of the most commonly used tabs, shown on the splash screen for fast access.

| Tab | What it shows |
|---|---|
| **Glossary** | Business glossaries, terms, definitions, and semantic relationships — folders, cross-glossary search, synonyms, antonyms, and related terms. A term's detail panel includes **"Where is this used?"** — every physical (schema column, etc.) and logical (Data Field, etc.) element assigned that term, shown together even though they live in different tabs |
| **Collections** | The collection hierarchy — digital products, families, blueprints, folios, dictionaries, and more, regardless of collection subtype. Defaults to **Root Collections only**; uncheck the box to see all collections with no parent (a broader, noisier set) |
| **Reports** | Two sub-tabs: **Report Specs** (report specifications, their links to data assets, and a Run Report panel) and **Analytic Functions** (the catalog of Python routines a report spec's `analytic_function` can run — each marked GENERIC or FIXED METRIC, cross-linked to its demo report spec) |
| **Digital Products** | Data products with governance metadata, lineage, and associated glossary terms |
| **Dr. Egeria Commands** | The full library of Dr. Egeria markdown command templates, organised by level and family — see [Dr. Egeria Execute panel](#dr-egeria-execute-panel) below |

### Review

The full set of element-category browsers — most support search, filtering, cross-navigation, and full property/relationship detail.

| Tab | What it shows |
|---|---|
| **Glossary** | Same as above |
| **Reference Data** | Valid value sets and definitions — the allowed values for property fields in your Egeria environment |
| **Data Design** | Data Specs, Data Structures, Data Fields, and Data Grains, cross-referenced with glossary terms — a field's assigned glossary term(s) and data class(es) are called out distinctly (🧠 / 🏷️) rather than buried among other relationships |
| **Collections** | Same as above |
| **Solution Architect** | Solution blueprints and component hierarchies — actor assignments, wiring relationships, concrete implementations — plus a **Patterns** tab for the design-pattern library (general/specialized, consumed/consuming, and related pattern relationships, grouped by category) |
| **Information Supply Chains** | ISC scope, segments, and concrete technical implementations as Mermaid diagrams. From Egeria 6.3 a supply chain has up to five graphs, each shown only when it has content: **ISC Implementation** (context, solution design and implementation status), **ISC Data Mesh** (digital products and their dependencies), **ISC System Fabric** (infrastructure and software capabilities), **ISC Data Fabric** (data assets, processes and actions linked by lineage) and **ISC Data Mapping** (elements linked by data mappings, such as columns) |
| **Locations** | Physical, cyber, and secure locations — parent/child hierarchies, peer links, locally hosted assets, assigned roles |
| **Actors** | Actor profiles (people, teams, organizations, IT profiles), the roles they perform, and their user identities |
| **Communities** | Communities of interest and the roles/people assigned to them |
| **Business Capabilities** | Business capabilities (functions, capability or skill sets) and the collections, members, and actors linked to them — connects Solution Architect's blueprints/components to business strategy |
| **Note Logs** | Note logs and their dated entries, each attached to a subject element |
| **Naming Vocabulary** | Elements classified `PrimeWord`, `ClassWord`, or `Modifier` — the naming-standard word vocabulary, grouped by classification |
| **Policy Enforcement** | Elements carrying a Policy\*Point classification (Management/Administration/Decision/Enforcement/Information/Retrieval) — an XACML-style policy architecture, grouped by classification |
| **Action Center** | Notification, Meeting, ToDo, and Review actions — the "Actions For People" model, paginated, with cross-links to every related element |
| **Duplicate Review** | Candidate duplicate elements paired via PeerDuplicateLink pending steward review, and already-consolidated elements with the sources they absorbed |
| **Perspectives & Questions** | Governance perspectives (viewpoints held by actors) and the Questions they must address |
| **Governance Definitions** | Governance drivers, policies, and controls, with relationships between definitions |
| **Projects** | Projects and their hierarchies, distinguished by classification (Campaign, StudyProject, PersonalProject, Task, etc.) |
| **Informal Tags** | Informal tags applied across the metadata ecosystem — public/private filter, jump to any tagged element |
| **Context Events** | TimeKeeper-managed events — planned/actual dates, durations, effects, dependent/related event relationships |
| **External References** | General links, related media, cited documents, external data sources, and external model sources |
| **Agreements** | General agreements, data sharing agreements, and digital subscriptions |
| **External Identifiers** | Records that a catalogued element also has an identifier in a third-party system — key, source, and every linked element |

### Reference

Read-only reference material; most don't require a live server connection.

| Tab | What it shows |
|---|---|
| **Type Explorer** | The open metadata type system — entities, classifications, relationships, and full inheritance hierarchy. Relationship types are grouped by [relationship purpose](#relationship-purposes) |
| **REST APIs** | REST endpoints exposed by the view server — operations, parameters, and response shapes |
| **Valid Values** | Registered valid metadata values for a specific Egeria property name |
| **Python API** | The pyegeria Python client API — classes by functional domain, methods with docstrings, inherited-vs-own filter |

---

## Detail panel features

Most detail panels (Glossary, Solution Architect, Locations, Actors, Communities, Projects, Governance Definitions, Reference Data, External References, External Identifiers, Agreements, Note Logs, and more) share a common set of controls in their header row:

- **ℹ Header** — pops up the element's header metadata common to every type: GUID, type name, status, version, and who created/last updated it and when.
- **{ } Copy JSON** — copies the complete raw JSON payload for the selected element to the clipboard. Shows **✓ Copied** (green) on success or **✕ Failed** (red), resetting after two seconds.
- **☐ / ☑ bookmark** — saves the item to **My Bookmarks** on the portal home page, linking back to this exact element. Requires an active persona (Quickstart) or a logged-in account (Freshstart); the toggle is hidden otherwise.
- **♡ feedback** — like/comment on the element via Egeria's built-in feedback API (separate from the portal's own per-page feedback button).

Every list-driven tab's sidebar also has a **↻ Refresh** button below its filter box, to reload that list on demand (e.g. after adding something via Dr. Egeria or Obsidian) without waiting for a full page reload.

Properties are shown generically — any scalar property Egeria returns for an element (including `authors`, `contentStatus`, and other `AuthoredReferenceable` fields) is displayed automatically, without needing per-type code changes. Relationships not otherwise shown in a dedicated section appear in a catch-all **Relationships** block at the bottom of the panel, so nothing linked to an element is silently hidden. That block is grouped into [relationship purpose](#relationship-purposes) families.

---

## Relationship purposes

Egeria gives every relationship type a **purpose**: why the type exists. Purpose also decides whether
operations that start on an anchored element (delete, copy, scope checks) follow the relationship. See
Egeria's [relationship purpose](https://egeria-project.org/concepts/relationship-purpose/) concept page.

Egeria defines eleven purposes. The portal groups them into six **families**:

| Family | Purposes | What it holds |
|---|---|---|
| **Composition** | Structural, Attachment | The element's own anchored graph: what it *is* and what it *owns* |
| **Governance & Description** | Assignment | Independent things that describe or govern it: terms, policies, owners, tags |
| **Organization** | Membership | Collections, folders and groupings it belongs to or contains |
| **Associations** | Association, Peer | Independent elements linked by an ordinary or equal-standing relationship |
| **Design & Deployment** | Definition, Deployment, Design Lineage | Specification to implementation, where it runs or is stored, designed flows |
| **Operations** | Action, Activity | Actions to take, and records of actions taken |
| **Unclassified** | — | Relationship types the server reports no purpose for |

A coloured **purpose badge** shows a relationship's exact purpose. Hover over it for Egeria's description.
Structural and Attachment relationships are part of the element's **anchored graph**.

### In the Type Explorer

- **Relationship type pages** show the purpose badge, Egeria's description, the family, and an
  **⚓ anchored graph** chip for Structural and Attachment types.
- **An entity type's Relationships tab** groups relationship types by family (all open). Use **Group** to
  switch to a flat list. The **Purpose** chips filter to one or more purposes, together with the text filter
  and **Show inherited**. Each card has its purpose badge.
- **The sidebar's RELATIONSHIPS list** is grouped into folded families. They open while you search.

A subtype can have a different purpose from its supertype. For example, `ActionRequester` is Activity
although its supertype `LineageRelationship` is Design Lineage. Each type shows its own purpose.

### On detail panels

The **Relationships** block on detail panels, and the relationships in **Data Mesh** and **The Catalog**,
are grouped into families:

- Every family starts **folded**. Click a family to open it. The browser remembers which families you
  opened, for every panel and app.
- Each group of related elements (for example *Member Of Collections*) sits in the family that most of its
  relationships belong to. A group is never split across families.
- A row shows its purpose badge where it adds information: in families with more than one purpose, for a
  row whose purpose belongs to a different family from its group, and in sections outside the families.

If the Egeria server doesn't report relationship purposes (older servers), panels keep a flat list and say
*"This Egeria server doesn't report relationship purposes, so relationships aren't grouped."* If the
purpose lookup fails, panels show the flat list without that message.

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

## Links from documentation

Where documentation refers to a specific type or glossary term, you can explore it directly:

- Type System: `/egeria-explorer` → Type System tab → search for the type name
- Glossary term: `/egeria-explorer` → Glossary tab → search for the term

---

## Further resources

- [Tech Catalog](tech-catalog.md) — browse and search technical assets; includes schemas, lineage sub-pane, and context diagrams
- [Lineage Explorer](lineage-explorer.md) — full-featured data lineage tracing tool
- [Egeria project documentation](https://egeria-project.org) — full open metadata type reference
