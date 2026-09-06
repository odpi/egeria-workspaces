# Egeria Advisor

Egeria Advisor is an AI-powered assistant for navigating and querying your Egeria metadata environment. It provides natural-language guidance, answers questions about the metadata landscape, and helps you find relevant types, terms, and assets.

> **Status:** Egeria Advisor runs as a separate service. It appears in the portal tile only when the service is running (indicated by the tile being active rather than showing "Not running").

---

## Accessing the Advisor

The portal tile links to the Advisor URL configured in `.env`:

```
EGERIA_ADVISOR_URL=http://localhost:8880/
```

If you are running the Advisor on a different host or port, update this value.

---

## Use cases

- **Discovery:** "What data assets relate to clinical trials?"
- **Governance:** "Which assets are in the quarantine zone?"
- **Lineage:** "Where does the revenue figure in the Q2 report come from?"
- **Type questions:** "What is the difference between a DataSet and a DataStore?"

---

## Configuration

The Advisor requires a login (any QuickStart demo user). With `EGERIA_ADVISOR_SSO_SECRET` in the
QuickStart `.env` equal to the Advisor's own `ADVISOR_PORTAL_SECRET`, opening the tile signs the
Portal's user straight in; otherwise the Advisor asks for a login.

How to deploy, configure and run the Advisor (and Resource Explorer) in the QuickStart demo
configuration or natively on a Mac or Linux developer machine:
[compose-configs/optional-associated-runtimes/trellis/DEPLOYING-TRELLIS.md](../../compose-configs/optional-associated-runtimes/trellis/DEPLOYING-TRELLIS.md).

---

## Further reading

- [Egeria project documentation](https://egeria-project.org)
- [Egeria Explorer](egeria-explorer.md) — for direct metadata browsing without AI assistance
