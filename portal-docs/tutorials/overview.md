<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Tutorials

Step-by-step, worked guides for getting things done in the Egeria Workspaces portal. Each one builds a real example you can reproduce on the Quickstart environment, with screenshots and diagrams where they help.

| Tutorial | What you will do | Uses |
|----------|------------------|------|
| [Building a Local Dashboard](local-dashboards.md) | Author a Dashboard Sheet: pick a Report Spec, create a Report, place it on the sheet, add KPI tiles and analytic charts, set perspectives and drill-downs. | [Local Dashboards](../tools/local-dashboards.md), Dr.Egeria |
| [Create and Use Saved Queries](saved-queries.md) | Build a faceted query, save it as a real Egeria `SavedQuery`, refresh it, and show its results on a Local Dashboard. | [Query tool](../tools/egeria-insights.md), [Local Dashboards](../tools/local-dashboards.md) |
| [Digital Product & Subscription Dashboard](digital-product-subscription.md) | Track Data Product adoption and historic growth with analytic trends and relationship diagrams. | [Local Dashboards](../tools/local-dashboards.md), Dr.Egeria |
| [Report Specs: Local and Held in Egeria](report-specs.md) | Add report specs as files or as Egeria elements, publish them to a tool's consumer folder, sync them, and see which copy wins (local > egeria > builtin). | [Egeria Explorer](../tools/egeria-explorer.md), Dr.Egeria, pyegeria |
| [Add and Use Analytic Functions](analytic-functions.md) | Use the built-in analytic functions, write your own, and register it in Jupyter, the quickstart Portal, freshstart or Egeria Advisor. | [Egeria Explorer](../tools/egeria-explorer.md), pyegeria |

## Suggested order

```mermaid
flowchart LR
    A["Building a Local Dashboard"] --> B["Create and Use Saved Queries"]
    A --> C["Digital Product & Subscription Dashboard"]
    A --> D["Report Specs"]
    D --> E["Analytic Functions"]
```

Start with **Building a Local Dashboard**: the others reuse its Report, Report Spec and Dashboard Sheet concepts. Read **Report Specs** before **Analytic Functions**, which writes a function for a spec to run.

## Prerequisites

- The Quickstart stack is running (`./quick-start-local`) and the portal is open at `https://localhost:8843`. Local Dashboards and the Query tool are quickstart only; freshstart has neither.
- For the Dr.Egeria steps, either the `dr_egeria` CLI or the **▶ Run Dr.Egeria Document** panel in [Local Dashboards](../tools/local-dashboards.md).

## Adding a tutorial

Put the Markdown file in `portal-docs/tutorials/`, put its screenshots in `portal-docs/images/` (reference them as `../images/name.png`), and add it to the table above and to the Tutorials section of `portal-docs/index.html`. See [Adding Documentation](../contributing.md).
