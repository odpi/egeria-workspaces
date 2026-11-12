<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# DCAT Loading Bay

The DCAT Files Receiver integration connector in `qs-integration-daemon`
watches this directory. Put descriptions of catalogs, datasets and data
services written in the W3C
[Data Catalog Vocabulary (DCAT)](https://www.w3.org/TR/vocab-dcat-3/) here as
JSON-LD files (`.jsonld` or `.json`), in any directory structure. Each new or
changed document is passed to the DCAT Cataloguer in the same integration
daemon, which turns each dataset into a data set asset with an asset for each
of its distributions, each data service into a deployed API and each catalog
into a collection folder.

The documents must be JSON-LD. A catalog exported in Turtle or RDF/XML needs
to be converted first. Egeria does not retrieve a JSON-LD context from the
network, so a document should embed its context or use the standard names for
the DCAT terms.

The connector's endpoint is the relative path `loading-bay/dcat`, which
resolves against the platform's working directory, `/deployments`. If this
directory is missing the connector logs DCAT-INTEGRATION-CONNECTOR-0004 on
every refresh.

The DCAT Publisher integration connector writes the descriptions of the
assets in the *DCAT Publishing Catalog* collection to
`distribution-hub/dcat-catalog`. It creates that directory itself.
