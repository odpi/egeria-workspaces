#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project.
"""
Generate the map from the coco_feed_* and coco_subscriptions_* Airflow tasks to the information supply chains they
move data along.  coco_lineage_facets.py reads it to add Egeria's egeria_informationSupplyChain run facet to the
tasks' OpenLineage events, so that Egeria tags the lineage it catalogues with the right supply chain.

    gen-coco-supply-chains.py <coco data hub workbook dir> <coco-dags dir>

e.g. from the repository root:

    compose-configs/egeria-quickstart/bin/gen-coco-supply-chains.py \
      "coco-workbooks/1. coco-data-hub" exchange-quickstart/coco-dags

It reads the strategic digital products (strategic-digital-products/*.md), their dependencies
(strategic-digital-products/product-dependencies.md) and the subscriptions
(mapping-the-systems/data/product-subscriptions.csv), and writes coco-supply-chains.json beside the DAGs.

A product dependency follows a solution linking wire: the product published by the wire's first component is
consumed by the second, and the dependency names the supply chain the wire implements (none where the wire crosses
between chains).  So:

  coco_subscriptions_*  <system>.apply__<product>  delivers the product to a subscriber because one of the
            subscriber's products depends on it - the subscription's basis names that product and the dependency's
            label.  The task's chains are the chains of those dependencies.  Reporting subscriptions (coco_ods,
            coco_sus) follow no dependency, so have no chain.
  coco_feed_*  <system>.load__<product>__<table>  publishes the product from the system that supplies it, which is
            the start of every wire the product travels along.  The task's chains are the chains of the
            dependencies on the product.  A product nothing depends on is the end of the chain that produced it, so
            its chains are those of the product's own dependencies instead.

The coco_operations_* DAGs simulate activity inside the systems and move no data along a wire, so they have no chain.

A task whose wires carry several chains lists them all; the facet passes them all to Egeria, which creates each
lineage relationship once for each chain.
"""
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


def schema_name(product_name):
    """The product's schema in coco_data_hub: its name in snake case."""
    return re.sub(r"[^a-z0-9]+", "_", product_name.lower()).strip("_")


def sections(text, command):
    """The '### Attribute' values of each '## <command>' section of a Dr.Egeria file."""
    for block in text.split(f"## {command}\n")[1:]:
        block = re.split(r"^#{1,2} ", block, flags=re.M)[0]
        yield {k.strip(): v.strip() for k, v in re.findall(r"^### (.+)\n+([^#\n].*)$", block, re.M)}


def read_products(products_dir):
    """Product qualified name for each product's display name.  The two can differ: New Product Definitions is
    DigitalProduct::Coco::Product Definitions."""
    products = {}
    for path in sorted(products_dir.glob("*.md")):
        for fields in sections(path.read_text(), "Create Digital Product"):
            products[fields["Display Name"]] = fields["Qualified Name"]
    return products


def read_dependencies(products_dir):
    """(consuming product, consumed product, label, chain or None) for each product dependency."""
    text = (products_dir / "product-dependencies.md").read_text()
    return [(f["Digital Product 1"], f["Digital Product 2"], f.get("Label"), f.get("ISC Qualified Name"))
            for f in sections(text, "Link Product Dependency")]


def chains_of(dependencies):
    return sorted({isc for *_, isc in dependencies if isc})


def main(workbook_dir, dags_dir):
    products_dir = workbook_dir / "strategic-digital-products"
    by_name = read_products(products_dir)
    by_schema = {schema_name(name): qn for name, qn in by_name.items()}
    dependencies = read_dependencies(products_dir)

    consumed_by = defaultdict(list)
    depends_on = defaultdict(list)
    for dep in dependencies:
        consumed_by[dep[1]].append(dep)
        depends_on[dep[0]].append(dep)

    tasks = defaultdict(dict)

    for path in sorted((dags_dir / "coco-system-extracts").glob("*/*/*.sql")):
        database, system = path.parent.parent.name, path.parent.name
        product_schema, _, product_table = path.stem.partition(".")
        product = by_schema[product_schema]
        chains = chains_of(consumed_by[product]) or chains_of(depends_on[product])
        tasks[f"coco_feed_{database}"][f"{system}.load__{product_schema}__{product_table}"] = chains

    subscriptions = {}
    with open(workbook_dir / "mapping-the-systems" / "data" / "product-subscriptions.csv", newline="") as fh:
        for row in csv.DictReader(fh):
            subscriptions[(row["subscriber_database"], row["subscriber_schema"], row["product_schema"])] = row
    for path in sorted((dags_dir / "coco-subscription-loads").glob("*/*/*.sql")):
        database, system, product_schema = path.parent.parent.name, path.parent.name, path.stem
        row = subscriptions[(database, system, product_schema)]
        followed = []
        for consumer, label in re.findall(r"([^;]+?) depends on it \(([^)]*)\)", row["basis"]):
            consumer = by_name[consumer.strip()]
            matches = [d for d in dependencies
                       if d[0] == consumer and d[1] == row["product_qualified_name"] and d[2] == label]
            if not matches:
                sys.exit(f"{path}: no dependency of {consumer} on {row['product_qualified_name']} labelled {label!r}")
            followed += matches
        tasks[f"coco_subscriptions_{database}"][f"{system}.apply__{product_schema}"] = chains_of(followed)

    out = dags_dir / "coco-supply-chains.json"
    with open(out, "w") as fh:
        json.dump({"_comment": "Generated by compose-configs/egeria-quickstart/bin/gen-coco-supply-chains.py - "
                               "do not edit.  The information supply chains each task moves data along.",
                   "tasks": {dag: dict(sorted(t.items())) for dag, t in sorted(tasks.items())}}, fh, indent=2)
        fh.write("\n")

    for dag, dag_tasks in sorted(tasks.items()):
        counts = defaultdict(int)
        for chains in dag_tasks.values():
            counts[min(len(chains), 2)] += 1
        print(f"{dag}: {len(dag_tasks)} tasks - {counts[1]} with one chain, {counts[2]} with several, "
              f"{counts[0]} with none")
    print(f"Wrote {out}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(Path(sys.argv[1]), Path(sys.argv[2]))
