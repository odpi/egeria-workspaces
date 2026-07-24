<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Welcome to the Coco Workbooks

This repository contains a collection of workbooks and resources for the Egeria *quickstart* environment.
They implement various scenarios involving [Coco Pharmaceuticals](https://egeria-project.org/practices/coco-pharmaceuticals/).
The purpose of these workbooks is to help you understand how to use Egeria and explore its capabilities using real-world examples.

## Where to start

- **Getting Started**: Begin with the [Quickstart Guide](https://egeria-project.org/egeria-workspaces/quick-start/overview/) to set up your environment.
- **Exploring Workbooks**: The numbering of the workbook folders offers a logical flow through the workbooks. However, you can run them in the order that interests you.  There are some dependencies between the workbooks and these are explicitly called out.

  - [0. Data Governance Program](0.%20data-governance-program/README.md) - load core governance definitions created by the governance leaders.
  - [1. Coco Data Hub](1.%20coco-data-hub/README.md) - set up a data sharing hub to exchange data between different business units.
  - [2. Clinical Trials](2.%20clinical-trials/receive-data-from-hospitals.ipynb) - set up and run the clinical trial data pipeline and observe lineage and data quality checks. Builds on the Coco Data Hub.
  - [3. Sustainability](3.%20sustainability/README.md) - configures Egeria to support their sustainability initiative.
  - [4. Keeping Safe](4.%20keeping-safe/README.md) - looks at some security scenarios.
  - [5. Data Field Naming](5.%20data-field-naming/README.md) builds a dataa field naming glossary.

<br>

- **Contributing**: If you want to contribute, check out the [Egeria Community](https://egeria-project.org/community/)

## Setting up your Obsidian environment

This directory is set up with Egeria's Obsidian plugin that issues Dr.Egeria commands written in a markdown file.

Create a new vault for this directory:

**Select Open Vault from the File menu**
![Select Menu Option](start-up-images/open-vault-menu-option.png)

**Select the Open Folder as Vault option**
![Check Plugins](start-up-images/open-folder-as-vault.png)

**Select the coco-workbooks directory**
![Check Plugins](start-up-images/select-coco-workbooks.png)

**Trust the author of the vault**
![Check Plugins](start-up-images/trust-author-warning.png)

**Check the Egeria plugin is installed and close (top right)**
![Check Plugins](start-up-images/check-plugins.png)

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.