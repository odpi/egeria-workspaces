<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# OpenLineage Events (data-initialization batch)

`harvest-open-lineage-events.ipynb` sets Egeria up to receive the OpenLineage events Airflow publishes. It catalogues
the Kafka topic `openlineage.events` (filled by the shared-infra OpenLineage proxy) as
`Topic::LocalKafka2.openlineage.events::inOut`, and makes it the catalog target of the `OpenLineageKafkaListener`
integration connector. The batch's canary is that `Topic`, so it re-runs after an Egeria reset.

**This batch is the only owner of `openlineage.events`** (owner, 2026-11-12). Nothing else catalogues it:

- The Coco Data Hub tutorial notebook `coco-workbooks/1. coco-data-hub/receiving-open-lineage-events.ipynb`
  is excluded from the *Coco - 1. Data Hub* batch, and when run by hand it finds an existing `Topic` named
  `openlineage.events` and registers nothing.
- Why it matters: on 2026-11-12 the quickstart had two such topics (`LocalKafka2`, from this batch, and
  `Kafka-Broker`, from the notebook), both catalog targets of the listener, so every event was consumed twice.
