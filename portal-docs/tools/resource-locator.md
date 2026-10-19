# Resource Locator

The Resource Locator is the Portal's "shop for resources" app. It is for people who look for resources (tables, files, reports, APIs, products, code repositories) rather than curate them. It reads Egeria only, and writes back only what Egeria already models: descriptions, informal tags and notes.

Open it from the portal tile (🛒 Resource Locator) or directly at `/resource-locator`. The older address, `/resource-browser`, still works, so existing bookmarks and favourites keep working. Links inside the app stay on whichever address you opened.

> **Quickstart only.** The Resource Locator is part of the QuickStart Portal.

---

## Home

- **Recently changed** lists the resources that changed most recently. Switch between **Changed by people** and **Including automation**: surveys and connectors change resources all the time, and this switch hides those changes.
- **Popularity** says plainly that it is not available yet. Egeria holds no usage measure for these resources, so the Locator shows that rather than ranking on a guess.
- **My lists** shows your work lists (see below).

---

## Search

One search box, with results grouped by kind. Filter to one kind with the buttons above the results: **Tables, Schemas, Databases, Reports, Data sets, Files and folders, Topics and feeds, Products, APIs, Code repositories**, or **All**.

A search matches names, qualified names and descriptions, and also:
- **column names**. A column match rolls up to its table, so you find the table rather than a list of columns;
- **informal tags** and **search keywords**;
- **owners**.

Each result row shows why it matched, its tags, likes and rating summary, and **in N of your lists** when you have already saved it.

Ordering is by text relevance only. Egeria cannot rank by use yet, and the page says so.

---

## Browse

Browse without typing, by **Tag, Badge** (governance classification), **Owner, Source system, Collection, Flavour** (data, data product, or a member of a data-sharing hub) or **Data scope**. Each facet lists its values; pick a value to see the resources under it, with the same rows as Search.

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
| **Lineage** | Upstream and downstream data flow, when lineage is recorded. |
| **Notes and journal** | Notes on the resource, notes left on its parts, and your own private notes (below). |

The page reports what is missing rather than showing an empty table. You'll see "no survey yet" or "no lineage recorded", and a resource you can't open says it may be hidden from you by zone security, not that it doesn't exist.

You can also add **informal tags**, use the Egeria Feedback widget to **like**, **rate** or **comment on** a resource, and save it to your favourites.

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

Every change (descriptions, tags, notes, terms, lists) is made as you, the signed-in user, with your own Egeria token. Without a signed-in persona, writes are refused rather than made under a shared account.

---

## Further reading

- [Resource Explorer](resource-explorer.md): the curator's side, which surveys and publishes resources into Egeria
- [Tech Catalog](tech-catalog.md): the technical catalogue view of the same assets
- [Lineage Explorer](lineage-explorer.md): full lineage for any resource
