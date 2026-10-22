<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Bitol Loading Bay

The Bitol Files Receiver integration connector in `qs-integration-daemon`
watches this directory. Put [Bitol](https://bitol.io) Open Data Contract
Standard (ODCS, `kind: DataContract`) and Open Data Product Standard (ODPS,
`kind: DataProduct`) documents here as `.yaml`, `.yml` or `.json` files, in
any directory structure. Each new or changed document is passed to the Bitol
cataloguers in the same integration daemon, which turn it into a data sharing
agreement or a digital product.

The connector's endpoint is the relative path `loading-bay/bitol`, which
resolves against the platform's working directory, `/deployments`. If this
directory is missing the connector logs BITOL-INTEGRATION-CONNECTOR-0004 on
every refresh.

More information on Bitol support can be found
[on the Egeria website](https://egeria-project.org/features/digital-product-management/overview/).
