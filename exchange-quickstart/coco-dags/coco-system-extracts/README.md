<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Coco Pharmaceuticals system extracts

These queries copy data from Coco Pharmaceuticals' **systems** into the **digital products** of the Data Sharing Hub.
They are the extract step for a simple Airflow DAG. Each one reads one system's schema and returns rows shaped exactly
like one table of one digital product in `coco_data_hub`.

## Where the data is

Coco Pharmaceuticals has three system estates, and each has its own database on the quickstart PostgreSQL server
(`egeria-shared-postgres`, port 5442). The databases are created and filled by the
[`init_coco_systems.sql`](../../../compose-configs/egeria-quickstart/docker-entrypoint-initdb.d/init_coco_systems.sql) script, which
`compose-configs/egeria-quickstart/bin/apply-postgres-init.sh` runs on every start.

| Estate | Database | Character |
|---|---|---|
| Coco core (the parent) | `coco_pharma` | Grew organically: homegrown, COTS and SaaS systems, plural where they should be singular. Its reference values are the ones in `coco_ods`. |
| Austin (acquired) | `austin_systems` | A complete regulated-pharma stack. It is integrated with Coco only in the manufacturing supply chain: Coco's Global Manufacturing Planning schedules the Austin site, and the Austin batches of Coco products appear on both sides. |
| Bucharest / EKG (acquired, just closed) | `bucharest_systems` | A complete regulated-pharma stack that is completely independent of Coco: its own products, codes, people and currency. |

Each system has **one schema** in its estate's database, holding only the tables needed to fill the digital products
it feeds. Tables and columns use the naming style of that kind of system, such as SAP `mara`/`bkpf`, Workday `worker`,
Veeva `quality_event__qdm`, or the terse names of Coco's homegrown systems. They do not follow Coco's data field naming
standard; translating to the standard is the extract's job. The system SQL is in
[`docker-entrypoint-initdb.d/data/coco_systems/<database>/<system schema>.sql`](../../../compose-configs/egeria-quickstart/docker-entrypoint-initdb.d/data/coco_systems).
Each file's first line names the system's qualified name in Egeria.

A system is here when it is a source of a digital product. That means the
[component-system mapping](../../../coco-workbooks/1.%20coco-data-hub/mapping-the-systems/data/component-system-mapping.csv)
links it, with Strong or Probable confidence, to the solution component the product is built from. For the Coco
components that came from the archive (Goods Inventory, HazMat Inventory, Accounting Ledgers, Employee Expense Tool and
Set Retention Period), the source is the archive's own `ImplementedBy` systems plus the acquired estates' obvious
equivalents. A product with no source in an estate has no extract there. That gap is deliberate, because it shows
where an estate has no system for a capability (serialisation and pharmacovigilance in Coco core, for example).

## Layout

```
coco-system-extracts/<database>/<system schema>/<product schema>.<product table>.sql
```

Each file is a single `SELECT` with a comment header naming the source system, its qualified name and the target
table. The query:

* reads only its own system's schema, so it runs on a connection to the system's database;
* returns exactly the columns of `coco_data_hub.<product schema>.<product table>`, with the same names, in the same
  order and with the same types;
* never returns a null in a `NOT NULL` column, and its rows are unique on the product table's primary key.

The `coco_feed_*` DAGs in the folder above run them: see [the DAGs' README](../README.md). Each load reads an
extract on a connection to the system's database and upserts its rows into the product table on the table's
primary key. The upsert matters because several extracts can feed the same product table: the three Coco factories'
control systems all feed the batch records, and each estate feeds the same product tables. The Austin batches of
Coco products arrive from both Coco's `mfctrl9482` and Austin's own manufacturing systems with the same keys.

The DAGs read the systems as `airflow_user` and write the product tables as `provisioner`, the user the
`coco_data_hub` set-up creates for filling the products.
