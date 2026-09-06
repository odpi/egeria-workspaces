# Resource Explorer

Resource Explorer scouts, surveys, publishes and curates software resources (GitHub repositories
today) into Egeria, and answers questions about them. It runs as a separate service, like Egeria
Advisor, and the Portal tile links to it.

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
  and its survey report are owned by the user who published them (Egeria Ownership) and sit in the
  `resource-explorer-draft` zone until a curator accepts them.
- **Curate**: accept or reject drafts; accepted resources move to the published zones.
- **Ask** questions about a surveyed resource, answered from the survey findings and the code.

---

## Configuration

How to deploy, configure and run Resource Explorer (and Egeria Advisor) in the QuickStart demo
configuration or natively on a Mac or Linux developer machine:
[compose-configs/optional-associated-runtimes/trellis/DEPLOYING-TRELLIS.md](../../compose-configs/optional-associated-runtimes/trellis/DEPLOYING-TRELLIS.md).

---

## Further reading

- [Egeria Advisor](egeria-advisor.md), the companion tool
- [Egeria project documentation](https://egeria-project.org)
