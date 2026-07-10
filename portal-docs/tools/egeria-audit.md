# Egeria Audit

Egeria Audit is the compliance-and-access view of the metadata landscape: exceptions, certifications, and licenses attached to catalogued elements, plus the Egeria user accounts able to see and change them.

Access it from the portal tile or directly at `/egeria-audit`.

---

## Tabs overview

| Tab | What it shows |
|---|---|
| **Exceptions** | `Exception` relationships — the affected element, its type, when the exception was raised, the steward responsible, and the exception type |
| **Certifications** | `Certification` relationships — certified element, certificate ID, who certified it, and the coverage period |
| **Licenses** | `License` relationships — licensed element, license ID, who issued it, and the coverage period |
| **Users** | Egeria user accounts registered on the connected platform — account type, status, and (with admin permissions) the ability to change status |

Each of Exceptions, Certifications, and Licenses is a flat, sortable, filterable table — there is no separate per-item detail page, so the bookmark button on the tab bookmarks the whole tab rather than an individual row.

---

## Governance-zone visibility

Rows are filtered by the connected persona's governance-zone access, same as everywhere else in the portal — a persona without access to a zone (e.g. Licenses for a restricted zone) simply won't see those rows. This is by design, not a bug.

---

## Users tab

Lists the Egeria user accounts on the selected platform. Supports:

- Free-text search across username and display name
- Filter by account status (Available, Disabled, Locked, Credentials Expired) and account type (Employee, Contractor, External, Digital)
- Click a user row to open a detail panel
- **Change account status** — requires an admin-level Egeria account; a non-admin attempt returns a clear permission error rather than a silent failure

---

## Bookmarking

Each tab has a bookmark toggle (☐ / ☑) that saves the tab to **My Bookmarks** on the portal. Requires an active persona (Quickstart) or a logged-in account (Freshstart).

---

## Further resources

- [Egeria Explorer](egeria-explorer.md) — full detail views for the elements these exceptions/certifications/licenses are attached to
- [Egeria Operations](egeria-operations.md) — runtime health and connector status, a different kind of "audit"
