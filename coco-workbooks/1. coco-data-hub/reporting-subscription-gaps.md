<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Feeding the reporting stores from the digital products

> **Author:** Erin Overview (Information Architect), Peter Profile (Solution Architect)
> **Version:** 0.1
> **Status:** DRAFT
> **Date:** 2026-10-01
> **Description:** Which strategic digital products can fill Coco Pharmaceuticals' two reporting stores, `coco_ods` and `coco_sus`, and what in them no product supplies.

---

## Why this matters

`coco_ods`, the operational data store, and `coco_sus`, the sustainability data marts (`System::coco-sus`), are
reporting stores in the `coco_pharma` database. Today they are loaded by hand. They are meant to be filled by
subscribing to the strategic digital products: `coco_ods` from the products, and `coco_sus` largely from
`coco_ods`. This document matches each of their tables to the products and records what is missing.

The subscriptions are rows in
[product-subscriptions.csv](mapping-the-systems/data/product-subscriptions.csv) with subscriber schema `coco_ods`
or `coco_sus`, and each has a staging schema in the `subscription_staging` database, for example
`coco_ods__product_master_data`. `coco_ods` is not a system in the CocoComboArchive, so its subscriptions name
the placeholder `System::coco-ods`. That is the first gap.

## Subscriptions

| Subscriber | Product | Fills |
|---|---|---|
| `coco_ods` | Product Master Data | `products` (code, name, dosage, pack size, status), `categories` (in part) |
| `coco_ods` | Goods Inventory Stock | `products.units_in_stock` / `reorder_level`, `supplies.units_on_hand` / `reorder_level` |
| `coco_ods` | Treatment Orders | `orders`, `order_details` (order, date, customer, product, quantity) |
| `coco_ods` | Treatment Invoices | `orders` (invoiced values) |
| `coco_ods` | Supplier Master Data | `suppliers` (identifier, name, country) |
| `coco_ods` | Purchase Orders And Receipts | `supply_orders`, `supply_order_details` (in part) |
| `coco_ods` | Goods Receipts | `supplier_invoice_details` (delivery date, quantity received) |
| `coco_ods` | Supplier Payments | `supplier_invoices` |
| `coco_ods` | Worker Master Data | `employees` (hire and leave dates, status, site, cost centre) |
| `coco_ods` | Corporate Directory Entries | `employees` (names, title, work phone, manager), `units_by_location` (department names) |
| `coco_sus` | Employee Expense Claims | `ghg_emissions.biz_travel`, `customer_travel` (in part) |
| `coco_sus` | Supplier Payments | `ghg_emissions.power` and `transport`, from the energy and fuel suppliers' invoices (in part) |

Everything else in `coco_sus` duplicates a `coco_ods` table and is expected to come from `coco_ods`.

One of the supplying products, *Purchase Orders And Receipts*, has **no source system in any estate** today,
so its subscription is in place but stays empty until a system feeds the product.  Coco's procurement system
feeds *Supplier Master Data* and *Third Party Onboarding Cases*, but not the purchase orders.

## Gaps

### Tables with no product

| Table | Store | What it holds | Gap |
|---|---|---|---|
| `customers` | both | Customer master: pharmacies and hospitals, contacts, addresses | **No customer master product.** Treatment Orders and Treatment Invoices carry only `hospital_identifier` / `customer_identifier`. |
| `shippers` | both | Carrier master | **No carrier master product.** The delivery products carry only `carrier_identifier`. |
| `coco_locations`, `sites` | both | Site addresses; site floor areas, energy use, headcount, vehicles | **No site or location product.** Products carry `site_code` / `warehouse_code` only, and nothing supplies areas, energy use or headcount per site. |
| `region`, `territories`, `employee_territories`, `us_states` | both | Sales geography | **No sales territory product.** Treated as reference data owned by the ODS. |
| `customer_demographics`, `customer_customer_demo` | both | Customer segmentation | No product. Empty today, so no loss. |
| `ghg_emissions` | `coco_sus` | Monthly emissions per site: stationary combustion, fugitive gas, transport, power, business travel | **Only in part.** Energy and fuel spend come from Supplier Payments and travel from Employee Expense Claims, but no product supplies metered consumption (kWh, litres), refrigerant losses or emission factors. A *Site Energy and Emissions* product, or metering data from the building management systems, would be needed. |
| `unit_prefixes`, `unit_units` | `coco_sus` | Unit-of-measure reference for the calculators | Reference data, not business data. No product needed. |

### Columns no product supplies

| Table | Columns missing | Why |
|---|---|---|
| `products` | `supplier_id`, `unit_price`, `units_on_order`, `replacement` | No product links a finished product to its supplier, and there is no price list product. Units on order would come from purchase orders, which carry no line items. |
| `categories` | `category_name`, `description` | Product Master Data has `product_type` only. Categories would need a product classification in the master. |
| `orders` | `employee_id` (sales representative), `required_date`, `shipped_date`, `ship_via`, `freight`, the `ship_*` address | Treatment Orders has no sales representative, required date or shipping detail. Shipping is in the delivery products but keyed by shipment, not order. |
| `order_details` | `unit_price`, `discount` | No price or discount in Treatment Orders. Invoices carry totals only. |
| `suppliers` | contact name and title, address, phone, fax, homepage | Supplier Master Data carries identity, status, risk and bank details, not contacts or addresses. |
| `supplies` | `supply_name`, `volume_units`, `unit_type` | **No raw material master product.** Raw materials appear only as `raw_material_code` in the stock, receipt and batch products. |
| `supply_orders`, `supply_order_details` | `supply_id`, `ship_to_address`, `supplier_reference`, line `product_id`, `unit_price`, `item_total_price` | Purchase Orders And Receipts has order headers and receipt confirmations but no order lines. |
| `supplier_invoice_details` | `line_number`, `product_id`, `item_amount` | Supplier Payments matches invoices at header level only. |
| `employees` | `employee_id` | **Pseudonymised by design.** The people products identify workers by `worker_pseudonym_identifier`. Mapping pseudonyms back to employee numbers is not in any product and should stay with HR. |
| `employees` | `birth_date`, `address`, `city`, `region`, `postal_code`, `country`, `home_phone`, `photo`, `notes`, `title_of_courtesy` | Personal data deliberately left out of Worker Master Data and the directory. The ODS should stop holding it, not obtain it. |
| `employees` | `employee_level`, `prior_service_credit`, `rehire` | HR attributes not in Worker Master Data. |
| `units_by_location` | `department_number` | The directory carries department names only. |
| `customer_travel` | `distance`, `travel_type`, `emissions`, `customer_city`, `ofc` | Expense claim lines carry type, date, amount and description, not distance or route. Emissions are calculated from distance, so the calculation needs a travel booking source. |

## Summary

* Ten products fill most of `coco_ods`'s transactional tables, with gaps in pricing, order lines and shipping
  detail.
* The ODS's **master data** for customers, carriers, sites and raw materials has no product. These are the four
  candidates for new products. A customer master and a site master would also serve other chains, for example
  hospital identification in treatment ordering and site codes everywhere.
* `coco_sus` cannot be filled from the products today. Its emissions need metered energy and travel distance,
  which no product carries.
* Several `employees` columns are personal data that the products deliberately do not carry. Moving the ODS to
  the products removes that data from it, which is a privacy improvement rather than a loss.
