<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Using the Egeria Freshstart Environment

If you are viewing this file in a Jupyter server, the freshstart environment is ready to use.

By default this Jupyter environment mounts:

- `distribution-hub`
- `landing-area`
- `loading-bay`
- `work`
- `workbooks`
- `config`

These folders are mounted from the `exchange-freshstart` and `work` folders in the `egeria-workspaces` repository.

Freshstart platform secrets are resolved in the container at `/deployments/secrets` and are mounted from `runtime-volumes/freshstart-platform-data/secrets`.

For deployment details and startup scripts, see `compose-configs/egeria-freshstart/README.md`.

