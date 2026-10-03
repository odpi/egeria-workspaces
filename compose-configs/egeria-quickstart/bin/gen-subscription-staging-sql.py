#!/usr/bin/env python3
"""Generate the subscription_staging DDL: one schema per digital product subscription.

A subscribing system receives its own copy of each digital product it subscribes to, so that it
can take deliveries on its own schedule and reprocess them after an error.  Each subscription
schema holds one table per data structure of the supplying product - the same columns, types,
primary key and comments as the product's table in coco_data_hub - followed by the delivery
columns that track each row's delivery and processing for that subscriber.

The subscriptions are listed in
coco-workbooks/1. coco-data-hub/mapping-the-systems/data/product-subscriptions.csv.
Usage (from the repository root):
  compose-configs/egeria-quickstart/bin/gen-subscription-staging-sql.py \\
    "coco-workbooks/1. coco-data-hub/strategic-digital-products" \\
    "coco-workbooks/1. coco-data-hub/mapping-the-systems/data/product-subscriptions.csv" \\
    compose-configs/egeria-quickstart/docker-entrypoint-initdb.d/data/subscription_staging.sql
"""
import csv
import importlib.util
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location("hub", Path(__file__).with_name("gen-coco-data-hub-sql.py"))
hub = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hub)

# Appended to every staging table, after the product's own columns.
DELIVERY_COLUMNS = [
    ("delivery_identifier", "varchar(100) NOT NULL",
     "The delivery (for example the pipeline run) that last wrote this row."),
    ("delivery_timestamp", "timestamptz NOT NULL DEFAULT now()",
     "When this row was last delivered from the digital product."),
    ("processing_status", "varchar(20) NOT NULL DEFAULT 'delivered'",
     "delivered (waiting for the subscriber), processed, or failed.  Set back to delivered to reprocess the row."),
    ("processing_timestamp", "timestamptz",
     "When the subscriber last processed this row, successfully or not."),
    ("processing_message", "text",
     "Why processing failed, or any note the subscriber records."),
]


def main(src, subscriptions_csv, out):
    products = {}
    for fname in hub.FILES:
        found, structures = hub.parse(Path(src) / fname)
        for p in found:
            products[p["schema"]] = (p, [structures[s] for s in p["structures"]])

    lines = ["-- Coco Pharmaceuticals subscription staging: one schema per digital product subscription.",
             "-- GENERATED from coco-workbooks/1. coco-data-hub/strategic-digital-products/*.md and",
             "-- coco-workbooks/1. coco-data-hub/mapping-the-systems/data/product-subscriptions.csv.",
             "-- Do not edit by hand: change those files and regenerate with",
             "-- compose-configs/egeria-quickstart/bin/gen-subscription-staging-sql.py.",
             "-- Idempotent: every object is created only if it does not exist.", "",
             "SET client_min_messages = warning;", ""]
    n_s = n_t = 0
    with open(subscriptions_csv, newline="") as f:
        subscriptions = list(csv.DictReader(f))
    for sub in subscriptions:
        product, structures = products[sub["product_schema"]]
        schema = sub["subscription_schema"]
        n_s += 1
        lines += [f"-- {sub['subscriber_name']} ({sub['estate']}) subscribes to {product['name']}",
                  f"CREATE SCHEMA IF NOT EXISTS {schema};",
                  f"GRANT ALL ON SCHEMA {schema} TO egeria_admin, egeria_user, airflow_user;",
                  f"COMMENT ON SCHEMA {schema} IS " + hub.sql_str(
                      f"Subscription of {sub['subscriber_name']} ({sub['estate']}, {sub['subscriber_qualified_name']}) "
                      f"to the digital product {product['name']} ({product['qn']}): a copy of the product's data set "
                      f"coco_data_hub.{product['schema']} delivered for this subscriber. Basis: {sub['basis']}.") + ";",
                  ""]
        for s in structures:
            table = f"{schema}.{hub.snake(s['name'])}"
            cols = sorted(s["fields"], key=lambda x: x[0])
            n_t += 1
            names = [hub.snake(f["name"]) for _, f in cols] + [c[0] for c in DELIVERY_COLUMNS]
            width = max(len(n) for n in names)
            body = [f"  {hub.snake(f['name']).ljust(width)} {hub.column_type(f)}" + ("" if f["nullable"] else " NOT NULL")
                    for _, f in cols]
            body += [f"  {name.ljust(width)} {definition}" for name, definition, _ in DELIVERY_COLUMNS]
            key = [hub.snake(f["name"]) for _, f in cols if f["primary_key"]]
            body.append(f"  CONSTRAINT {hub.snake(s['name'])}_pk PRIMARY KEY ({', '.join(key)})")
            lines += [f"CREATE TABLE IF NOT EXISTS {table} (", ",\n".join(body), ");",
                      f"COMMENT ON TABLE {table} IS {hub.sql_str(s['description'] + ' Delivered from coco_data_hub.' + product['schema'] + '.' + hub.snake(s['name']) + '.')};"]
            lines += [f"COMMENT ON COLUMN {table}.{hub.snake(f['name'])} IS {hub.sql_str(f['description'])};" for _, f in cols]
            lines += [f"COMMENT ON COLUMN {table}.{name} IS {hub.sql_str(text)};" for name, _, text in DELIVERY_COLUMNS]
            lines.append("")
        lines += [f"GRANT ALL ON ALL TABLES IN SCHEMA {schema} TO egeria_admin, egeria_user, airflow_user;", ""]
    Path(out).write_text("\n".join(lines) + "\n")
    print(f"{n_s} subscription schemas, {n_t} tables -> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
