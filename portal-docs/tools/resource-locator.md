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

One search box. Narrow the results with the **Kind** buttons above them: **Tables, Schemas, Databases, Reports, Data sets, Files and folders, Topics and feeds, Products, APIs, Code repositories**, **Columns and attributes**, **Data fields**, **Glossary terms**, or **All**. Pick several kinds to search them together (for example Schemas and Tables); pick a kind again to drop it. The address keeps the choice (`?q=customer&kind=table,schema`), so a search can be bookmarked or shared.

A search matches names, qualified names and descriptions, and also:
- **columns, attributes and data fields**. Columns and other schema attributes (table columns, the fields of a topic's event types, API parameters) and the data fields of data designs are results of their own. Each says what holds it ("in hz_cust_accounts (RelationalTable)", "in Invoice (DataStructure)"). The resource that holds the part is found too, with "matched: contains: …". Only the first 25 matching parts on each page have their container looked up, and the page says when there were more;
- **informal tags** and **search keywords**;
- **owners**.

**Glossary terms** are not resources, so **All** leaves them out: about 1,500 terms would crowd resources out of the results. Pick **Glossary terms** to search them, on their own or with other kinds. When terms also match an All search, the page says how many and how to see them. A term row shows its summary and its content status, and opens the term in Egeria Explorer's glossary, which shows the glossary and folders that hold it. The row does not name its glossary: Egeria does not carry that on the term itself.

Each result row shows why it matched, its tags, likes and rating summary, and **in N of your lists** when you have already saved it. **Narrow these results** filters the loaded results by flavour, owner, badge, **category**, or whether the resource records a data scope. Category is the element's own category property, a free-text name its author gives, matched exactly; the choices are the categories of the loaded results, plus "(no category)". Few resources on a new system have one. Browse lists that hold categorised rows (a folder, a keyword) offer the same choice.

Ordering is by text relevance only. Egeria cannot rank by use yet, and the page says so.

**Load more results** stays offered until Egeria returns an empty page. A page shorter than the page size is not taken as the last page: Egeria can return a short page when some elements on it are filtered out (zone security, for example), so the only end the Locator can see is an empty page.

---

## Browse

Browse without typing, by **Tag, Badge** (a curated list of governance classifications: Confidentiality, Confidence, Criticality, Impact, Retention and Security tags; Egeria has many more classifications, and the badge list keeps Browse to the ones worth choosing from), **Owner, Source system, Collection, Folder, Search keyword, Category, Flavour** (data, data product, or a member of a data-sharing hub) or **Data scope**. Each facet lists its values; pick a value to see the resources under it, with the same rows as Search. Hover over a facet button for its definition. A facet with more than 12 values (folders, categories, tags) has a box above its values: type to keep only the values whose name or description holds every word you type.

**Folder** lists every folder in Egeria you can see (a CollectionFolder: the folders of a glossary, a product catalog or a hub), with the type of element it is anchored to when that is another element. Which folder or glossary holds a folder is shown on the folder's own page ("Held by"). It shows no count beside each folder, because counting what every folder holds would take one read per folder; open a folder to see what it holds. A folder page lists the resources, glossary terms, columns and data fields in it, links to the folders inside it and to what holds it, and names by type anything else it holds that the Locator does not list. When a folder or collection holds more than Egeria returns in one read (1,000), the page says "at least".

**Search keyword** lists each keyword by its text, ignoring case, with the number of attachments: a search keyword in Egeria is attached to one element each. A keyword page reads exactly those attachments, so it always accounts for its count: what it lists, what is attached to something you cannot see, what could not be read, what was not read because the list stops at 500 attachments, what is not a resource or term, and attachments that repeat an element already listed (the same keyword in another spelling).

**Category** lists the values of the category property found on the resources and glossary terms you can see, each with how many resources and terms carry it, and **(no category)** last. Egeria has no call that lists categories, so they come from the same background read of every resource that Data scope uses (about 15 seconds the first time): the page says "counting" until it finishes, never 0. A category page lists exactly the elements that count counted. Infrastructure, governance definitions and design patterns carry categories too; the Locator lists resources and terms only.

Folder, keyword and category pages take the same **Lens** filter as the other lists. When nothing is there the page says so ("This folder holds nothing you can see"), which is different from a read that failed, which shows the error instead of an empty list.

**Data scope** has two values:

- **Data scope recorded**: resources whose data scope records a time, a place or another dimension.
- **No data scope recorded**: resources with no DataScope at all, or one holding only usage readings (see below). These are the resources that still need a scope. The list is every resource the Locator covers minus the recorded ones, **of the resources you can see**: zone security and the Promise/Memento toggle decide what that is, so two people can get different counts. A count shows as "≥ N" (at least) only when a read stopped at its page limit.

The first time you open it, "No data scope recorded" says **counting…** while every resource is read in the background (about 20 seconds); the page refreshes itself when the count is ready. A resource whose classifications were not read is in neither list; the page counts it as **scope not read**. Each list shows its own age: a resource scoped in the last ten minutes may sit in neither list, or both, until both refresh.

### Filtering a Browse list by a data lens

Every Browse list has a **Lens** choice. It lists your own data lenses and the lenses that govern a list you can see. Pick one and the list shows three counts, each a button you can turn on or off (inside is on to start):

- **inside**: every dimension the resource and the lens both record overlaps;
- **outside**: at least one of them does not;
- **cannot be compared**: the resource records none of the lens's dimensions. It is never counted as outside, and it never silently drops out.

A fourth count, **scope not read**, appears when some resources' classifications were not read with the list. Counts say "at least" when the list's read stopped at its page limit. Each row says its outcome and on which dimensions. The address keeps the lens (`&lens=…`), so a filtered list can be bookmarked.

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

A lens's periods are typed the same way as a data scope's in The Catalog: a year (`2026`), month or day means the whole of it, so a 2026 lens runs from the first moment of 1 January to the last moment of 31 December (UTC), and a resource whose data starts at midnight on 1 January is inside it. A whole year or month shows as `2026` or `2026-03` on the lens.

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
