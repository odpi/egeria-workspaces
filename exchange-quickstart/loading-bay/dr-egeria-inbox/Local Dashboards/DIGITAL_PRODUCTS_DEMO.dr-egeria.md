<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Digital Product Portfolio & Subscriptions Demo

This document seeds the metadata and dashboard placements for the Digital Product Portfolio tutorial.

## Create Digital Product
### Display Name
Customer 360 Insights
### Description
Consolidated customer behavioral data for marketing analytics.

___

## Create Digital Product
### Display Name
Clinical Trial Progress
### Description
Real-time tracking of clinical trial recruitment and milestones.

___

## Create Agreement
### Display Name
Marketing Subscription - C360
### Description
Subscription for the Marketing team to Customer 360 Insights.
### Agreement Type
Subscription

___

## Link Agreement Item
### Agreement Name
Marketing Subscription - C360
### Item Name
Customer 360 Insights

___

## Create Dashboard Sheet
### Display Name
digital-product-portfolio
### Dashboard Sheet Heading
Digital Product Portfolio & Subscriptions
### Dashboard Sheet Description
A high-level view of our data product ecosystem and adoption metrics.

___

## Create Report
### Display Name
Total Products Count
### Report Spec
Analytic - Element Count by Type
### Output Format
DICT
### Analytic Parameters
type_name: DigitalProduct

___

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

## Create Report
### Display Name
Active Subscriptions Count
### Report Spec
Analytic - Element Count by Type
### Output Format
DICT
### Analytic Parameters
type_name: Agreement

___

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

___

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

## Create Report
### Display Name
Product Subscription Map
### Report Spec
Collections
### Output Format
MERMAID
### Search String
Marketing Subscription - C360

___

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
