<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Coco Pharmaceuticals DAGs

This folder is the `coco-dags` DAG bundle of the Airflow runtime in
`compose-configs/optional-associated-runtimes/airflow-marquez`. It is mounted into the Airflow containers at
`/opt/airflow/coco-dags`, so a change to a file here reaches Airflow at its next DAG parse.

## Digital product feeds

[coco_product_feeds.py](coco_product_feeds.py) fills the strategic digital products' tables in the Data Sharing
Hub database, `coco_data_hub`, from the systems that supply them. Data is copied as soon as it changes in a
supplying system. There is one DAG per system estate:

| DAG | Reads | Extracts |
|---|---|---|
| `coco_feed_coco_pharma` | The Coco Pharmaceuticals systems in `coco_pharma` | 91 |
| `coco_feed_austin_systems` | The acquired Austin site's systems in `austin_systems` | 89 |
| `coco_feed_bucharest_systems` | The acquired EKG Pharmaceuticals systems in `bucharest_systems` | 77 |

The work is defined by the extract queries in [coco-system-extracts/](coco-system-extracts/README.md), one per
system and product table. Each extract reads one system's own tables and returns exactly the columns of one product
table. So each extract is also where that system's native data is transformed into the product's form: codes
translated, local-time text dates made timestamps, flags made booleans, and identifiers pseudonymised.

Each DAG runs continuously, one run after another:

1. **`wait_for_changes`** is a sensor. About once a minute it fingerprints the result of every extract, as an md5
   of its rows. It finishes as soon as a fingerprint differs from the one recorded when that extract last loaded.
   It waits in reschedule mode, so it holds no worker slot between checks.
2. **`choose_loads`** starts the load tasks of the changed extracts and skips the rest.
3. **`<system>.load__<product schema>__<product table>`**, in a task group per system, copies the extract into the
   product table:
   - It reads the extract's rows and fingerprint in one consistent snapshot of the system's database.
   - It upserts the rows into the product table on the table's primary key.
   - Only then does it record the fingerprint, so a failed load is retried on the next run.

On the first run nothing has been recorded, so every extract loads.

The DAGs are created unpaused, so they start as soon as Airflow parses them. To stop one, pause it in the Airflow
UI. To reload everything, delete the `coco_feed_fingerprint::*` Variables. Each extract keeps its last fingerprint
in a Variable named `coco_feed_fingerprint::<database>.<system>.<product schema>.<product table>`.

### Things to know

- **Rows are upserted, never deleted.** Several systems can feed the same product table, so a load cannot tell
  whether a row it no longer returns came from it or from another system.
- **The last load wins.** Where two systems supply the same key, the product holds whichever loaded last. For
  example, the Austin batches of Coco products come from both Coco's `mfctrl9482` and Austin's own manufacturing
  systems.
- **Daily changes.** A few extracts depend on the date, such as qualification currency and invoice overdue status,
  so they show as changed, and reload, once a day.
- **Lineage.** Each load task declares the system tables its extract reads, and the product table it writes, as
  Airflow assets (`postgres://host.docker.internal:5442/<database>/<schema>/<table>`). OpenLineage therefore reports
  table-level lineage from each system to each product, to Marquez or to Egeria depending on `switch-lineage.sh`.
  Later DAGs, such as deliveries to the subscribers in `subscription_staging`, can be scheduled on a product table
  being updated.

## Subscription loads

[coco_subscription_loads.py](coco_subscription_loads.py) completes the journey. Each subscribing system has its
own copy of each digital product it subscribes to in the `subscription_staging` database: one schema per
subscription, holding the product's tables plus delivery columns. Delivering into those schemas is the job of
Egeria's provisioning services. These DAGs copy what has been delivered into the subscribing system's own tables,
as soon as it arrives. There is one DAG per system estate:

| DAG | Writes to | Subscriptions |
|---|---|---|
| `coco_subscriptions_coco_pharma` | The Coco Pharmaceuticals systems in `coco_pharma`, including the `coco_ods` and `coco_sus` reporting stores | 102 |
| `coco_subscriptions_austin_systems` | The Austin systems in `austin_systems` | 74 |
| `coco_subscriptions_bucharest_systems` | The EKG Pharmaceuticals systems in `bucharest_systems` | 73 |

The work is defined by the apply scripts in `coco-subscription-loads/<database>/<system schema>/<product schema>.sql`,
one per subscription. The subscriptions themselves are listed in
`coco-workbooks/1. coco-data-hub/mapping-the-systems/data/product-subscriptions.csv`.

An apply script runs in the destination system's database, in one transaction. Before it runs, the DAG creates a
temporary table `incoming_<product table>` for each of the product's tables. These hold the rows waiting for
this subscriber, plus a `discard_reason` column. The script runs in two steps:

1. It sets `discard_reason` on the rows that are not appropriate to the system. Examples are another estate's
   data, records the system does not keep, and data the system already holds because it supplied it.
2. It writes the rest into the system's own tables, transforming them from the product's form into the
   system's. Where a system should hold data it had no table for, its schema has been extended.

Each DAG runs continuously:

1. **`wait_for_deliveries`** is a sensor. About once a minute it looks for rows with `processing_status`
   `delivered` in the estate's subscriptions, and finishes as soon as it finds some.
2. **`choose_subscriptions`** starts the apply tasks of the subscriptions with rows waiting.
3. **`<system>.apply__<product schema>`** applies the waiting rows. It then marks each of them in
   `subscription_staging`:
   - `processed`, with `applied` or the discard reason as its `processing_message`;
   - or `failed`, with the error.

   A row that was delivered again while it was being applied keeps its new `delivered` status.

To reprocess data, for example after fixing a failed apply, set its `processing_status` back to `delivered`.

The apply scripts are written so that applying the same rows twice changes nothing. They also avoid a feedback
loop: once delivered data has been applied, the `coco_feed_*` DAGs must not see it as new product data. Each apply
task declares the staging tables it reads, and the system tables it writes, as Airflow assets for OpenLineage.

## Connections

The connections are set as `AIRFLOW_CONN_*` environment variables in `airflow-marquez.yaml`:

| Connection | Database | User |
|---|---|---|
| `coco_pharma`, `austin_systems`, `bucharest_systems` | The system databases | `airflow_user` |
| `coco_data_hub` | The Data Sharing Hub | `provisioner`, which can read and write every product table |
| `subscription_staging` | The subscribers' copies of the products | `airflow_user` |

The `coco_feed_*` DAGs read the system databases, and the `coco_subscriptions_*` DAGs write to them.
The databases themselves are created by the quickstart's PostgreSQL set-up
(`compose-configs/egeria-quickstart/bin/apply-postgres-init.sh`), so start `egeria-quickstart` before Airflow.
