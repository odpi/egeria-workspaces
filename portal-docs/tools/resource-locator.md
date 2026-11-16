# Resource Locator

The Resource Locator is the Portal's "shop for resources" app. It is for people who look for resources (tables, files, reports, APIs, products, code repositories) rather than curate them. It reads Egeria, and writes back only what Egeria already models: descriptions, informal tags, notes, meanings, work lists and data lenses.

Every term the page shows has a small **?** beside it: hover over it, or tab to it, to read its definition. The **Help** tab gives a short guide and the full list of terms.

Open it from the portal tile (🛒 Resource Locator) or directly at `/resource-locator`. The older address, `/resource-browser`, still works, so existing bookmarks and favourites keep working. Links inside the app stay on whichever address you opened.

> **Quickstart only.** The Resource Locator is part of the QuickStart Portal.

---

## Home

- **Recently changed** lists the resources that changed most recently. Switch between **Changed by people** and **Including automation**: surveys and connectors change resources all the time, and this switch hides those changes.
- **Popularity** says plainly that it is not available yet. Egeria holds no usage measure for these resources, so the Locator shows that rather than ranking on a guess.
- **My lists** shows your work lists (see below).
- **Data lenses** lists the data lenses you can see, and makes a new one (see below).

---

## Search

One search box. Narrow the results with the **Kind** buttons above them: **Tables, Schemas, Databases, Reports, Data sets, Files and folders, Topics and feeds, Products, APIs, Code repositories**, **Columns and attributes**, **Data fields**, or **All**. Pick several kinds to search them together (for example Schemas and Tables); pick a kind again to drop it. The address keeps the choice (`?q=customer&kind=table,schema`), so a search can be bookmarked or shared.

A search matches names, qualified names and descriptions, and also:
- **columns, attributes and data fields**. Columns and other schema attributes (table columns, the fields of a topic's event types, API parameters) and the data fields of data designs are results of their own. Each says what holds it ("in hz_cust_accounts (RelationalTable)", "in Invoice (DataStructure)"). The resource that holds the part is found too, with "matched: contains: …". Only the first 25 matching parts on each page have their container looked up, and the page says when there were more;
- **informal tags** and **search keywords**;
- **owners**.

Each result row shows why it matched, its tags, likes and rating summary, and **in N of your lists** when you have already saved it. **Narrow these results** filters the loaded results by flavour, owner, badge, or whether the resource records a data scope.

Ordering is by text relevance only. Egeria cannot rank by use yet, and the page says so.

**Load more results** stays offered until Egeria returns an empty page. A page shorter than the page size is not taken as the last page: Egeria can return a short page when some elements on it are filtered out (zone security, for example), so the only end the Locator can see is an empty page.

---

## Browse

Browse without typing, by **Tag, Badge** (governance classification), **Owner, Source system, Collection, Flavour** (data, data product, or a member of a data-sharing hub) or **Data scope**. Each facet lists its values; pick a value to see the resources under it, with the same rows as Search. Hover over a facet button for its definition.

**Data scope** lists the resources whose data scope records a time, a place or another dimension. Resources whose DataScope classification holds only usage readings (see below) are left out, and the page says how many.

---

## The resource page

Open any result to see one resource on its own page (`/resource-locator?guid=…`). It has these cards, each shown only when Egeria holds something for it:

| Card | What it shows |
|---|---|
| **Description** | The description, which you can improve. Your edit is attributed to you, with the time. |
| **Columns** | The schema, with each column's type and description. Column descriptions can be edited too. |
| **Statistics** | The latest survey measurements (row counts, column profiles), each with its date. |
| **Preview** | A preview of a file's content, where one is available. |
| **What it contains** | The parts one level down (schemas in a database, tables in a schema, files in a folder), with counts. **Part of** shows what contains it. |
| **Where it fits** | Collections, products, connections, lineage neighbours, governance definitions, external references and other related elements. |
| **Meaning** | Glossary terms assigned to it and to its columns. You can assign or withdraw a term. |
| **Governance** | The owner (or "no owner recorded"), and classifications such as confidentiality and criticality. |
| *(under the title)* | The **data scope**: each period and bound it records, usage readings, and a link to set or change it in The Catalog. |
| **Lineage** | Upstream and downstream data flow, when lineage is recorded. |
| **Notes and journal** | Notes on the resource, notes left on its parts, and your own private notes (below). |

The page reports what is missing rather than showing an empty table. You'll see "no survey yet" or "no lineage recorded", and a resource you can't open says it may be hidden from you by zone security, not that it doesn't exist.

You can also add **informal tags**, use the Egeria Feedback widget to **like**, **rate** or **comment on** a resource, and save it to your favourites.

---

## Flavour

Each resource shows one **flavour**, the highest that applies:

| Flavour | Means |
|---|---|
| **Hub** | A member of a data sharing hub (a `DataSharingHub` collection): authoritative data, actively kept up to date. |
| **Product** | A digital product (`DigitalProduct`), or a member of one: curated and prepared for use. |
| **Known** | Anything else Egeria knows about, curated or not. |

A resource page also names any other flavour that applies, and the product or hub that made it so.

---

## Data scope

A **data scope** is Egeria's `DataScope` classification on a resource. It says what the resource's data covers:

- **periods**: when the data was collected, when it is valid, and what period it covers (each a start and an end);
- **bounds**: latitude, longitude and height (a box the data covers);
- **scope elements**: Egeria elements that define the scope, such as a Location, a Team or a BusinessCapability, by name and GUID.

**Where it shows.** Result rows carry **◷ scope** when the resource records one. The resource page shows every dimension it records under the title, and the **has a data scope** filter and the **Data scope** browse facet use the same rule.

**Usage readings.** Egeria's OpenLineage data scope governance service also writes into DataScope, in its `additionalProperties`: read counts, readers and reads per day for an analysis window. They are usage, not scope, so the Locator shows them as **usage** and does not count a resource as having a data scope when they are all its DataScope holds. On laz in November 2026, about 1,170 of 1,300 DataScope classifications held only these readings.

**How to set it.** Open the resource in **The Catalog** (the resource page's "set in The Catalog ↗" link) and use its **Data scope** section; see [The Catalog](tech-catalog.md#data-scope). The dimensions come from Egeria's own type definition, so a dimension Egeria adds later appears there with no change to the Portal. A data scope can also be set with pyegeria (`ClassificationExplorer.add_data_scope`, `update_data_scope`, `clear_data_scope`) or Dr.Egeria (**Classify Data Scope**, **Update Data Scope**, **Declassify Data Scope**; in pyegeria 6.3.0 these commands do not carry the time and place fields yet, so use The Catalog or pyegeria for those).

---

## Data lenses

A **data lens** (Egeria's `DataLens`, a governance definition) says what scope of data a piece of work needs, using the same dimensions as a data scope. In Egeria's model the lens **governs** a collection of the resources that meet it (the `GovernedBy` relationship); in the Locator that collection is one of your work lists.

- **Make one** from the **Data lenses** tile on Home (**New data lens**): a name, what the work needs in words, the dimensions that matter, and optionally one of your lists for it to govern. Fill in only the dimensions the work cares about.
- **Its page** (`/resource-locator?lens=…`) shows the lens, the lists it governs, and the **resources inside it**, each with **Add to list**.
- **Matching.** A resource is compared on the dimensions both it and the lens record. It is **inside** when every one of them overlaps: periods and bounds overlap (an open end is unbounded), and scope elements share an element. It is **outside** when one does not. A resource that records none of the lens's dimensions **cannot be compared**, and is counted as such rather than as outside.
- **Change it** (**Edit**), link it to another of your lists, or **unlink** a list (the list is kept). Only the person who made a lens changes it here; others see it read-only. The Portal names its lenses `DataLens::portal::<user>::<slug>`.

---

## Notes and private notes

The Notes card has an **everyone / only me** choice.

- **Everyone** adds a note to the resource's own note log. Anyone who can see the resource can read it.
- **Only me** keeps the note in your own **My Profile journal**. It is linked to the resource with an `Actions` relationship, so it shows up both here and, with what it is about, in your journal listing. It is placed in a secured governance zone (`resource-explorer-private`) plus your own userId zone, so only you can read it. Other users get "not authorised", and the note is filtered out of their searches.

Private notes cannot be deleted yet: Egeria has no way to delete a journal entry. The page says so. Older private notes that carry only your userId zone are shown as **in your journal, but other people can read it**, because that zone alone keeps no one out.

---

## Work lists

A work list is an Egeria collection of resources, each with the reason you added it.

- **Create** a list, rename it, add resources with a reason, and remove them.
- **Copy** chosen members of any list you can see into a list of your own.
- **Share** a list with a Team or Community you belong to, and stop sharing it.
- Lists published from Resource Explorer show here too, because they are the same Egeria collections.

---

## Who you are when you write

Every change (descriptions, tags, notes, terms, lists, data lenses) is made as you, the signed-in user, with your own Egeria token. Without a signed-in persona, writes are refused rather than made under a shared account.

---

## Further reading

- [Resource Explorer](resource-explorer.md): the curator's side, which surveys and publishes resources into Egeria
- [Tech Catalog](tech-catalog.md): the technical catalogue view of the same assets
- [Lineage Explorer](lineage-explorer.md): full lineage for any resource
