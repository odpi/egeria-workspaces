<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Freshstart Secrets Templates

This directory contains **template** secrets files for the freshstart Egeria deployment.
They serve as a starting point — copy them to `runtime-volumes/freshstart-platform-data/secrets/`
and customise as needed before starting the stack.

## Files

| File | Purpose |
|---|---|
| `egeria-user-directory.omsecrets` | Platform user directory: defines user accounts, security groups, roles, and access controls. Referenced by `platform.security.secrets.*` in `freshstart.application.properties`. |
| `egeria-servers.omsecrets` | Server/connector NPA credentials: tokens and database passwords for the `fs-*` servers. Referenced as `egeriaServersSecretsStore` in `platform.placeholder.variables`. |
| `integration.omsecrets` | Integration connector secrets (empty by default). Add entries here as you configure additional connectors. |

## How to use

The freshstart startup scripts (`fresh-start-local`, `fresh-start-multi-host`) seed
`runtime-volumes/freshstart-platform-data/secrets/` from here **the first time** the
runtime secrets directory is empty.  To reset to defaults, delete the runtime secrets
directory and restart.

To customise:

1. Copy this directory to a local working location or edit the files in
   `runtime-volumes/freshstart-platform-data/secrets/` directly (those files are
   not tracked by Git).
2. Add your own users to `egeria-user-directory.omsecrets`.
3. Update passwords and tokens in `egeria-servers.omsecrets`.
4. Add integration connector secrets to `integration.omsecrets`.

> **Note:** The files in `runtime-volumes/freshstart-platform-data/secrets/` are
> read-write mounted into the container at `/deployments/secrets` and are picked up
> at platform start-up.  Changes take effect on the next platform restart.

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.

