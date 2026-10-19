# Resource Explorer

Resource Explorer scouts, surveys, publishes and curates software resources (GitHub repositories
today) into Egeria, and answers questions about them. It runs as a separate service, like Egeria
Advisor, and the Portal tile links to it.

> **Status: Alpha.** Resource Explorer is an active work in progress — features are still being
> added and some will change. We are keen for feedback: what is useful, what is missing, and what
> gets in your way. Use the **Share your feedback** widget in the Portal, or raise an issue.

---

## Accessing Resource Explorer

The tile links to the URL configured in the QuickStart `.env`:

```
EGERIA_RESOURCE_EXPLORER_URL=http://localhost:8810/
```

Use the box's hostname instead of `localhost` when the browser runs elsewhere on the LAN. Note that
`./quick-start-local` regenerates `.env` and does not yet carry this key over; re-add it after a run.

A login is required (any QuickStart demo user). With `EGERIA_ADVISOR_SSO_SECRET` set on the
QuickStart side and the same value as `TRELLIS_PORTAL_SECRET` on the Resource Explorer side, the
tile signs the Portal's user straight in.

---

## What a signed-in user does

- **Add** a repository, **survey** it, and **publish** the survey into Egeria. The published asset
  and its survey report are owned by the user who published them (Egeria Ownership). Published
  assets go to Egeria with no RE-imposed zone: RE leaves zoning to Egeria's own defaults. Draft
  versus accepted is a content status on the element, not a zone. The exception is work in a
  private investigation, which RE zones to its owner (`resource-explorer-private` plus the owner's
  zone), so only that owner can see it.
- **Curate**: accept or reject drafts. Accepting changes the element's content status, not its zone.
- **Ask** questions about a surveyed resource, answered from the survey findings and the code.

---

## In the Portal

- **Curation Coverage tile.** The report spec **Resource Explorer - Curation Coverage** puts RE's published-against-not-yet-published count for a database on a [Dashboard Sheet](local-dashboards.md). The Portal calls RE server-to-server, as the viewer's persona: it exchanges the Portal's SSO token at RE's `POST /api/auth/portal`, then calls `GET /api/analytics/curation-coverage-tile/{type}/{slug}`.
- **Resource Locator.** Work lists published from RE appear in the [Resource Locator](resource-locator.md), and lists made there appear in RE, because both use the same Egeria collections. The Locator's private notes use RE's secured zone, `resource-explorer-private`.

There are two addresses:

| Setting | Used by | Default |
|---|---|---|
| `EGERIA_RESOURCE_EXPLORER_URL` | the browser (the portal tile and the SSO handoff) | `http://localhost:8810/` |
| `RESOURCE_EXPLORER_API_URL` | the Portal server (the Curation Coverage tile) | `http://host.docker.internal:8813` |

RE currently runs on **8813**. It will move to **8810**; when it does, change `RESOURCE_EXPLORER_API_URL` to match.

---

## Configuration

How to deploy, configure and run Resource Explorer (and Egeria Advisor) in the QuickStart demo
configuration or natively on a Mac or Linux developer machine:
[compose-configs/optional-associated-runtimes/trellis/DEPLOYING-TRELLIS.md](../../compose-configs/optional-associated-runtimes/trellis/DEPLOYING-TRELLIS.md).

---

## Further reading

- [Egeria Advisor](egeria-advisor.md), the companion tool
- [Egeria project documentation](https://egeria-project.org)
