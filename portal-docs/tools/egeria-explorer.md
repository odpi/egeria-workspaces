# Egeria Explorer

Egeria Explorer is the primary browser-based interface for navigating Egeria metadata. It provides tab-by-tab views of types, glossary terms, lineage, governance blueprints, digital products, and more.

Access it from the portal tile or directly at `/egeria-explorer`.

---

## Tabs overview

### Explore

A quick-start subset of the most commonly used tabs, shown on the splash screen for fast access.

| Tab | What it shows |
|---|---|
| **Glossary** | Business glossaries, terms, definitions, and semantic relationships — folders, cross-glossary search, synonyms, antonyms, and related terms |
| **Collections** | The collection hierarchy — digital products, families, blueprints, folios, dictionaries, and more, regardless of collection subtype |
| **Reports** | Report specifications and their links to data assets |
| **Digital Products** | Data products with governance metadata, lineage, and associated glossary terms |
| **Dr. Egeria Commands** | The full library of Dr. Egeria markdown command templates, organised by level and family — see [Dr. Egeria Execute panel](#dr-egeria-execute-panel) below |

### Review

The full set of element-category browsers — most support search, filtering, cross-navigation, and full property/relationship detail.

| Tab | What it shows |
|---|---|
| **Glossary** | Same as above |
| **Reference Data** | Valid value sets and definitions — the allowed values for property fields in your Egeria environment |
| **Data Design** | Data Specs, Data Structures, Data Fields, and Data Grains, cross-referenced with glossary terms |
| **Collections** | Same as above |
| **Solution Architect** | Solution blueprints and component hierarchies — actor assignments, wiring relationships, concrete implementations |
| **Information Supply Chains** | ISC scope, segments, and concrete technical implementations as Mermaid diagrams |
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
| **Type Explorer** | The open metadata type system — entities, classifications, relationships, and full inheritance hierarchy |
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

Properties are shown generically — any scalar property Egeria returns for an element (including `authors`, `contentStatus`, and other `AuthoredReferenceable` fields) is displayed automatically, without needing per-type code changes. Relationships not otherwise shown in a dedicated section appear in a catch-all **Relationships** block at the bottom of the panel, so nothing linked to an element is silently hidden.

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
