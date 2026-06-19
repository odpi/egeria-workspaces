<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Overview

This directory contains sample Docker Compose scripts to support the deployment of Unity Catalog for experimentation,
development, and learning. When the Unity Catalog community releases official Docker images, this directory is expected to be
deprecated. For now, it is a convenience in setting up two Unity Catalogs with their companion UIs.

The `unity-coco` service in `uc-ui-compose.yaml` is configured to automatically create the `clinical_trials` catalog upon startup to support the Coco Pharmaceuticals scenarios.

# Running the Unity Catalogs

To start up the Unity Catalogs from this directory try:

```shell
/usr/local/bin/docker compose -f uc-ui-compose.yaml -p unitycatalog-egeria up -d
```

License: CC BY 4.0, Copyright Contributors to the ODPi Egeria project.


