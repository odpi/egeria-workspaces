<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Subscribing to digital products

Egeria publishes extracts of the open metadata ecosystem as digital products in the *Open Metadata Digital Product Catalog*.  Each product is a table of values, and a subscription delivers a product's data to a destination of the subscriber's choice, keeping it up to date.

The notebooks in this folder put subscriptions to work:

* [Building the Egeria operational data store](build-egeria-ods.ipynb) fills a PostgreSQL database called `egeria_ods` with one table for each product, through a daily subscription to each of the product families at the top of the catalog.

## The Egeria operational data store

These workbooks are for the *freshstart* environment.  `egeria_ods` is a database in the shared PostgreSQL server.  It is created empty when the environment starts (see `compose-configs/shared-infra/docker-entrypoint-initdb.d/init_egeria_ods.sql`).

The products are organized into product families, held in a catalog folder called *Digital Products derived from Open Metadata*.  The folder is not a product, so it cannot be subscribed to; the notebook subscribes to each family directly beneath it instead.  A subscription to a family delivers every product in it, including those of the families nested inside it.  The notebook:

1. makes sure the database is catalogued in Egeria;
2. lists the product families in the catalog folder;
3. for each family, describes a schema named after the family as its destination data set, and subscribes that destination to the family using its daily refresh subscription type - unless the destination already has a subscription.

Egeria's provisioning services create each schema and a table for each product in its family, and refresh them once a day, starting from the time of the subscription.

The notebook can be run again at any time: each step is skipped if it has already been done, so a later run picks up a family that has been added to the folder.  A family that does not offer a daily refresh subscription type is reported and skipped.

The quickstart environment builds the same database with Dr.Egeria commands instead: see `coco-workbooks/1. coco-data-hub/egeria-operational-data-store.md`.

For the catalog itself, see the [open-metadata-product-catalog](../open-metadata-product-catalog/README.md) workbooks.

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the Egeria project.
