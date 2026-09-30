goo<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Tutorial: Building a Digital Product & Subscription Dashboard

This tutorial walks through creating a **Business Perspective** dashboard using the **Local Dashboards** feature. While Egeria Explorer is excellent for technical metadata discovery, Local Dashboards allow you to compose high-level views that combine metadata counts, historic trends, and relationship diagrams into a single page tailored for a specific role (like a Product Manager or a Data Consumer).

We will build a dashboard for **Digital Products and Subscriptions** — a scenario common in data-mesh-inspired organizations where data is packaged as products and consumed via formal subscriptions (Agreements).

## Scenario: The Data Product Portfolio

We want to answer four key questions for the Data Office:
1. **Catalog Scale**: How many Digital Products are currently published?
2. **Adoption**: How many active Subscriptions (Agreements) do we have across all products?
3. **Historic Trend**: Is our product adoption growing over time?
4. **Relationship**: How are our key products linked to their consumers?

## Prerequisites

- Access to the Egeria Quickstart environment.
- The `dr_egeria` CLI or the **▶ Run Dr.Egeria Document** panel in the Local Dashboards UI.
- (Optional) Familiarity with [LOCAL_DASHBOARDS_TUTORIAL.md](LOCAL_DASHBOARDS_TUTORIAL.md).

---

## Step 1 — Define the Metadata

For this dashboard to be meaningful, we need `DataProduct` and `Agreement` elements in Egeria. We will use a Dr.Egeria document to seed these if they don't exist, or just reference them if they do.

A "Subscription" in this context is modeled as an **Agreement** linked to a **Digital Product**.

```markdown
## Create Digital Product
### Display Name
Customer 360 Insights
### Description
Consolidated customer behavioral data for marketing analytics.

## Create Digital Product
### Display Name
Clinical Trial Progress
### Description
Real-time tracking of clinical trial recruitment and milestones.

## Create Agreement
### Display Name
Marketing Subscription - C360
### Description
Subscription for the Marketing team to Customer 360 Insights.
### Agreement Type
Subscription

## Link Agreement Item
### Agreement Name
Marketing Subscription - C360
### Item Name
Customer 360 Insights

___
```

---

## Step 2 — Create the Dashboard Sheet

Create the container for our dashboard. We'll give it a clear heading and description.

```markdown
## Create Dashboard Sheet
### Display Name
digital-product-portfolio
### Dashboard Sheet Heading
Digital Product Portfolio & Subscriptions
### Dashboard Sheet Description
A high-level view of our data product ecosystem and adoption metrics.

___
```

---

## Step 3 — Define and Place KPI Tiles

We want two compact tiles at the top to show current totals. We use the `Analytic - Element Count by Type` Report Spec, which is a **GENERIC** analytic function that we can retarget via `Analytic Parameters`.

### Total Digital Products
```markdown
## Create Report
### Display Name
Total Products Count
### Report Spec
Analytic - Element Count by Type
### Output Format
DICT
### Analytic Parameters
type_name: DigitalProduct

## Link Report to Dashboard Sheet
### Dashboard Sheet Name
digital-product-portfolio
### Report Name
Total Products Count
### Placement Span
1
### Placement Emphasis
kpi

___
```

### Active Subscriptions
```markdown
## Create Report
### Display Name
Active Subscriptions Count
### Report Spec
Analytic - Element Count by Type
### Output Format
DICT
### Analytic Parameters
type_name: Agreement

## Link Report to Dashboard Sheet
### Dashboard Sheet Name
digital-product-portfolio
### Report Name
Active Subscriptions Count
### Placement Span
1
### Placement Emphasis
kpi

___
```

---

## Step 4 — Add the Historic Trend

To show growth over time, we use a Report Spec that returns a time series. The `Analytic - Generic Metric Trend` spec is perfect for this. It generates a Vega-Lite line chart when the `Output Format` is set to `SERIES`.

```markdown
## Create Report
### Display Name
Subscription Growth Trend
### Report Spec
Analytic - Generic Metric Trend
### Output Format
SERIES
### Analytic Parameters
window: 180d
points: 6
metric_path: pyegeria.view.overview_metrics.count_elements
metric_params: {"type_name": "Agreement"}

## Link Report to Dashboard Sheet
### Dashboard Sheet Name
digital-product-portfolio
### Report Name
Subscription Growth Trend
### Placement Span
2
### Placement Emphasis
panel

___
```

---

## Step 5 — Visualizing Relationships (Mermaid)

Finally, we'll add a Mermaid diagram that shows how Products and Subscriptions are linked. This provides a visual confirmation of the "Adoption" metric. We use the `Collections` spec, which can visualize any collection (including Agreements) as a Mermaid diagram.

```markdown
## Create Report
### Display Name
Product Subscription Map
### Report Spec
Collections
### Output Format
MERMAID
### Search String
Marketing Subscription - C360

## Link Report to Dashboard Sheet
### Dashboard Sheet Name
digital-product-portfolio
### Report Name
Product Subscription Map
### Placement Span
full
### Placement Emphasis
panel

___
```

---

## Step 6 — Run and View

1. Save your commands into a file, e.g., `DIGITAL_PRODUCTS_DEMO.dr-egeria.md`.
2. Run the document using the **Run Dr.Egeria Document** button in the `/local-dashboards` portal.
3. Once processed, the page will refresh. Select **Digital Product Portfolio & Subscriptions** from the list.

### What to look for:
- **KPI Tiles**: You should see two large numbers at the top.
- **Trend Chart**: A line chart showing the growth of Agreements over the last 180 days.
- **Mermaid Diagram**: A visual graph linking your Products to their Subscriptions.

## Next Steps: Adding Perspectives

You can narrow these tiles to specific roles by adding `Placement Perspectives` to the `Link` commands:

- Add `Placement Perspectives: builder` to the Product Count tile.
- Add `Placement Perspectives: consumer` to the Subscription Map.

When you select a perspective from the dropdown in the dashboard header, only the relevant tiles will remain, allowing you to use one "Digital Product" sheet to serve both producers and consumers with different needs.
