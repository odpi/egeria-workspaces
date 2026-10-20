#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project.
"""
Generate the Dr.Egeria file that subscribes the Coco systems to the strategic digital products.

    gen-digital-product-subscriptions.py <repository root>

Reads
  coco-workbooks/1. coco-data-hub/mapping-the-systems/data/product-subscriptions.csv   which system takes which product
  coco-workbooks/1. coco-data-hub/strategic-digital-products/*.md                   the products and their groups
  exchange-quickstart/coco-dags/coco-system-extracts/                               which product tables have a source
and writes coco-workbooks/1. coco-data-hub/digital-product-subscriptions.md.

How each subscription is delivered is decided by SUBSCRIPTION_KIND below; edit the rules there and regenerate.
"""
import csv
import glob
import os
import re
import sys
from collections import defaultdict

REQUESTER = "Person::UK::986419"           # Peter Profile, who builds the Data Sharing Hub's pipelines
DESTINATION_TEMPLATE = "3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7"   # PostgreSQL schema as a tabular data set collection
# The product tables as the PostgreSQL cataloguer records them (setting-up-the-data-hub.ipynb); OpenLineage events
# about the tables resolve to these elements, and refresh their DataScope classification
TABLE_QN = "PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::{schema}::{table}"

LICENSES = {
    "internal": "LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use",
    "personal": "LicenseType::Jacquard::LICENSE-TYPE-PERSONAL-DATA::Personal Information",
}
# Hourly refreshes use the content pack's within-an-hour objective: Dr.Egeria's Create Service Level Objective
# (pyegeria 6.2.5) sends an entitlements property that ServiceLevelObjectiveProperties rejects, so no Coco-specific
# hourly objective is created.
HOURLY_SLO = "ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt"
KINDS = {
    "ongoing": {"kind": "ONGOING_UPDATE", "identifier": "ONGOING-UPDATE-SUBSCRIPTION",
                "name": "Ongoing update subscription", "interval": 5,
                "slo": "ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt",
                "description": "Delivers the changes to the product's data to the subscriber's destination as they "
                               "arrive in the Data Sharing Hub, at most every five minutes."},
    "hourly": {"kind": "PERIODIC", "identifier": "HOURLY-REFRESH-SUBSCRIPTION",
               "name": "Hourly refresh subscription", "interval": 60, "slo": HOURLY_SLO,
               "description": "Delivers the product's data to the subscriber's destination every hour."},
    "daily": {"kind": "PERIODIC", "identifier": "DAILY-REFRESH-SUBSCRIPTION",
              "name": "Daily refresh subscription", "interval": 1440,
              "slo": "ServiceLevelObjective::Jacquard::SLO-DAILY-REFRESH::A complete refresh of the product data is "
                     "delivered to the product data's destination each day",
              "description": "Delivers the product's data to the subscriber's destination once a day."},
    "weekly": {"kind": "PERIODIC", "identifier": "WEEKLY-REFRESH-SUBSCRIPTION",
               "name": "Weekly refresh subscription", "interval": 10080,
               "slo": "ServiceLevelObjective::Jacquard::SLO-WEEKLY-REFRESH::A complete refresh of the product data is "
                      "delivered to the product data's destination each week",
               "description": "Delivers the product's data to the subscriber's destination once a week."},
    "evaluation": {"kind": "ONE_TIME", "identifier": "EVALUATION-SUBSCRIPTION",
                   "name": "Evaluation subscription", "interval": None,
                   "slo": "ServiceLevelObjective::Jacquard::SLO-ONCE-ONLY::A complete copy of the product data is "
                          "delivered to the product data's destination just once",
                   "description": "Delivers the product's data to the subscriber's destination just once, so that "
                                  "the subscriber can evaluate it."},
}
ORDER = ["ongoing", "hourly", "daily", "weekly", "evaluation"]

# The groups whose products describe identifiable people
PERSONAL_GROUPS = {"People Systems", "Privacy Operations", "Patient Treatment"}
PERSONAL_WORDS = re.compile(r"patient|employee|worker|staff|adverse|safety case|pharmacovigilance|identity|"
                            r"person|clinician|payroll|consent|rights", re.I)

ARCHIVES = {"opentext_ecm", "veeva_rim", "purview_dlp", "cornerstone_lms", "microsoft_365", "informatica_idmc"}
ERP_AND_PEOPLE = re.compile(r"^(sap_s4hana|sap_ariba|sap_concur|coco_ledgers|coco_expenses|coco_hrim|workday_hcm|"
                            r"ukg_dimensions|kronos_workforce|uk_payroll|nl_payroll|ca_payroll|procurement01)$")


def subscription_kind(row: dict, group: str, sourced: bool) -> str:
    """How a subscriber takes a product - the rules behind the file's variety of subscription types."""
    system = row["subscriber_schema"]
    if system in ("coco_ods", "coco_sus"):
        return "daily"           # reporting stores, rebuilt overnight
    if row["estate"] == "Bucharest" and group in ("Master Data Management", "Privacy Operations", "Patient Treatment"):
        return "evaluation"      # EKG is assessing the group's master data and patient-facing products first
    if system in ARCHIVES:
        return "weekly"          # records, regulatory and catalogue systems
    if ERP_AND_PEOPLE.match(system):
        return "hourly"          # batch interfaces into the ERP, finance and people systems
    return "ongoing" if sourced else "daily"


def read_products(root: str) -> dict:
    products = {}
    folder = os.path.join(root, "coco-workbooks/1. coco-data-hub/strategic-digital-products")
    groups = dict(re.findall(r"### Display Name\n([^\n]+)\n\n### Qualified Name\n(CollectionFolder::[^\n]+)",
                             open(os.path.join(folder, "catalog.md")).read()))
    group_by_qn = {qn: name for name, qn in groups.items()}
    for path in glob.glob(os.path.join(folder, "*.md")):
        text = open(path).read()
        for block in text.split("\n___\n"):
            m = re.search(r"## Create Digital Product\n\n### Display Name\n([^\n]+)\n\n### Product Name\n([^\n]+)\n\n"
                          r"### Qualified Name\n([^\n]+)", block)
            if m:
                products[m.group(3)] = {"display": m.group(1), "product_name": m.group(2), "file": path}
        for folder_qn, qn in re.findall(r"## Add Member to Collection\n\n### Collection Id\n(CollectionFolder::[^\n]+)\n\n"
                                        r"### Element Id\n(DigitalProduct::[^\n]+)", text):
            if qn in products:
                products[qn]["group"] = group_by_qn.get(folder_qn)
    for qn, p in products.items():
        if not p.get("group"):
            sys.exit(f"{qn} is in no business system group folder")
    return products


def block(command: str, attributes: list[tuple[str, object]]) -> str:
    lines = ["___", "", f"## {command}", ""]
    for name, value in attributes:
        if value is None:
            continue
        lines.append(f"### {name}")
        if isinstance(value, list):
            lines.extend(f"- {v}" for v in value)
        else:
            lines.append(str(value))
        lines.append("")
    return "\n".join(lines)


def main(root: str) -> None:
    hub = os.path.join(root, "coco-workbooks/1. coco-data-hub")
    rows = list(csv.DictReader(open(os.path.join(hub, "mapping-the-systems/data/product-subscriptions.csv"))))
    products = read_products(root)
    tables = defaultdict(set)
    for path in glob.glob(os.path.join(root, "exchange-quickstart/coco-dags/coco-system-extracts/*/*/*.sql")):
        schema, table = os.path.basename(path)[:-4].split(".")
        tables[schema].add(table)

    subscriptions, waiting = [], []
    for row in rows:
        product = products[row["product_qualified_name"]]
        sourced = bool(tables.get(row["product_schema"]))
        if not sourced:
            waiting.append(row)
            continue
        row["kind"] = subscription_kind(row, product["group"], sourced)
        subscriptions.append(row)

    by_product = defaultdict(list)
    for row in subscriptions:
        by_product[row["product_qualified_name"]].append(row)
    groups = sorted({products[qn]["group"] for qn in by_product})
    kind_counts = defaultdict(int)
    for row in subscriptions:
        kind_counts[row["kind"]] += 1

    out = []
    out.append("""# Digital Product Subscriptions

> **Author:** Peter Profile (Solution Architect), Erin Overview (Information Architect)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-10-19
> **Description:** Subscribes the Coco Pharmaceuticals systems to the strategic digital products they depend on, so that the data each product receives in the Data Sharing Hub is delivered to the systems that need it.

---

# Overview

Each system that supplies a digital product copies every change it makes into the product's tables in the Data
Sharing Hub straight away (the `coco_feed_*` DAGs).  This file sets up the other half of each supply chain: the
**subscriptions** that deliver the products' data to the systems that consume it.  The subscriptions follow
[product-subscriptions.csv](mapping-the-systems/data/product-subscriptions.csv): a system subscribes to a product when
it implements a solution component whose own product depends on it, and the reporting stores `coco_ods` and
`coco_sus` subscribe to the products that fill their reports.

Egeria delivers a subscription by running a provisioning pipeline that copies the product's tables into the
subscriber's **destination** - the subscriber's own schema in the `subscription_staging` database, holding the
product's tables plus delivery columns.  The `coco_subscriptions_*` DAGs then apply what has been delivered to the
subscribing system's own tables.

## What a subscription needs

A product can be subscribed to once it has

* a **product manager** - an actor assigned to the product.  Each business system group's products are assigned to
  that group's *Digital Product Manager* role;
* **subscription types** - the ways of subscribing to it.  Each one is a governance action process,
  `ProvisioningActionProcess::<product name>::Create Subscription::<identifier>`, which `Initiate Subscription` runs;
* a **license type** and a **service level objective** for each subscription type, granted to the subscriber.  The
  products use the licenses and service level objectives from Egeria's digital products content pack: products about
  identifiable people are licensed as *Personal Information*, everything else as *Data for Internal Use*.

## Kinds of subscription

The subscriptions use five subscription types, so that each way Egeria delivers a product is exercised:

| Subscription type | Kind | Delivery | Used for | Subscriptions |
|---|---|---|---|---|""")
    used = {"ongoing": "operational systems that act on the data as it arrives",
            "hourly": "batch interfaces into the ERP, finance and people systems",
            "daily": "the `coco_ods` and `coco_sus` reporting stores",
            "weekly": "records, regulatory and catalogue systems",
            "evaluation": "EKG Pharmaceuticals (Bucharest), assessing the group's master data, privacy and patient "
                          "treatment products before integrating with them"}
    delivery = {"ongoing": "when the product's data changes, at most every 5 minutes",
                "hourly": "every hour", "daily": "every day", "weekly": "every week", "evaluation": "once"}
    for k in ORDER:
        out.append(f"| {KINDS[k]['name']} | `{KINDS[k]['kind']}` | {delivery[k]} | {used[k]} | {kind_counts[k]} |")
    out.append(f"""
An *ongoing update* subscription is triggered by changes to the product's **monitored resources**: here, the
product's tables as Egeria's PostgreSQL cataloguer records them when `setting-up-the-data-hub.ipynb` catalogues the
`coco_data_hub` database (`PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::<schema>::<table>`).
Each time a `coco_feed_*` DAG loads a product table, Airflow's OpenLineage event about the load resolves to that
table, its `DataScope` classification is refreshed, and Egeria's subscription manager (Baudot) runs the deliveries.
So connect OpenLineage to Egeria after the hub has been catalogued - see *Before you start* in the
[README](README.md).  Periodic and one-time subscriptions are run by Baudot on its ten-minute refresh.

## Products waiting for a source

{len(waiting)} of the {len(rows)} subscriptions in the list are to products that no system supplies yet - the
products classified as promises in [promises.md](strategic-digital-products/promises.md).  They are not set up here,
since there is nothing to deliver; add them when the products have a source.

| Subscriber | Product |
|---|---|""")
    for row in sorted(waiting, key=lambda r: (r["product_name"], r["subscriber_name"])):
        out.append(f"| {row['subscriber_name']} ({row['estate']}) | {row['product_name']} |")
    out.append("""
---

# Product managers

Each business system group's products are managed by the group's Digital Product Manager role, which becomes the
products' owner in each subscription.
""")
    for group in groups:
        out.append(block("Create Person Role", [
            ("Display Name", f"{group} Digital Product Manager"),
            ("Qualified Name", f"PersonRole::Coco::Digital Product Manager::{group}"),
            ("Description", f"Manages the {group} digital products in the Coco Pharmaceuticals Strategic Digital "
                            f"Product Catalog: their definitions, their subscription types and the subscriptions "
                            f"taken out to them."),
        ]))

    for group in groups:
        out.append(f"\n---\n\n# {group}\n")
        for qn in sorted(q for q in by_product if products[q]["group"] == group):
            product = products[qn]
            subs = sorted(by_product[qn], key=lambda r: r["subscription_schema"])
            schema = subs[0]["product_schema"]
            personal = group in PERSONAL_GROUPS or bool(PERSONAL_WORDS.search(product["display"]))
            license_qn = LICENSES["personal" if personal else "internal"]
            out.append(f"\n## {product['display']}\n")
            out.append(f"{len(subs)} subscriber(s): " + ", ".join(
                f"{r['subscriber_name']} ({r['estate']}, {KINDS[r['kind']]['name'].lower()})" for r in subs) + ".\n")
            out.append(block("Link Assignment Scope", [
                ("Assigned Actor", f"PersonRole::Coco::Digital Product Manager::{group}"),
                ("Assignment Type", "Product Manager"),
                ("Scope Element", qn),
            ]))
            for k in ORDER:
                if not any(r["kind"] == k for r in subs):
                    continue
                kind = KINDS[k]
                out.append(block("Create Subscription Type", [
                    ("Digital Product", qn),
                    ("Subscription Kind", kind["kind"]),
                    ("Display Name", kind["name"]),
                    ("Identifier", kind["identifier"]),
                    ("Description", kind["description"]),
                    ("Subscription Notification Interval", kind["interval"]),
                    ("Monitored Resources", [TABLE_QN.format(schema=schema, table=t) for t in sorted(tables[schema])]
                     if k == "ongoing" else None),
                    ("Subscription License Type", license_qn),
                    ("Subscription Service Level Objective", kind["slo"]),
                ]))
            for r in subs:
                destination = (f"PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::"
                               f"subscription_staging.{r['subscription_schema']}")
                out.append(block("Create Element", [
                    ("Element Type Name", "TabularDataSetCollection"),
                    ("Template GUID", DESTINATION_TEMPLATE),
                    ("Placeholder Property Values", [
                        "hostIdentifier: host.docker.internal",
                        "serverName: Coco PostgreSQL Server 1",
                        "portNumber: 5442",
                        "secretsCollectionName: PostgreSQL Provisioning Secret",
                        "secretsStorePathName: secrets/integration.omsecrets",
                        "versionIdentifier: V1.0",
                        "databaseName: subscription_staging",
                        f"schemaName: {r['subscription_schema']}",
                        f"schemaDescription: {r['subscriber_name']} ({r['estate']}) copy of the {product['display']} "
                        f"digital product.  {r['basis']}.",
                    ]),
                ]))
                out.append(block("Initiate Subscription", [
                    ("Subscription Type", f"ProvisioningActionProcess::{product['product_name']}::Create Subscription::"
                                          f"{KINDS[r['kind']]['identifier']}"),
                    ("Subscription Requester", REQUESTER),
                    ("Destination Data Set", destination),
                    ("Journal Entry", f"{r['subscriber_name']} subscribes to {product['display']}: {r['basis']}."),
                ]))
    out.append("___\n\n----\nLicense: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),\n"
               "Copyright Contributors to the ODPi Egeria project.\n")
    # Narrative between commands closes the block before it, as in the other workbooks
    pieces = []
    for piece in out:
        if pieces and pieces[-1].startswith("___") and not piece.startswith("___"):
            pieces.append("___\n" if not piece.startswith("___\n\n----") else "")
        pieces.append(piece)
    text = "\n".join(pieces).replace("\n\n\n", "\n\n")
    target = os.path.join(hub, "digital-product-subscriptions.md")
    open(target, "w").write(text)
    print(f"{target}: {len(by_product)} products, {len(subscriptions)} subscriptions "
          f"({', '.join(f'{k} {kind_counts[k]}' for k in ORDER)}), {len(waiting)} waiting for a source")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
