<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Understanding Martyn's Law

The markdown files in this folder are used to create the open metadata elements that were created by 
[Ivor Padlock](https://egeria-project.org/practices/coco-pharmaceuticals/personas/ivor-padlock/) in the 
[Preparing for Martyn's Law](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/preparing-for-martyns-law/overview/) solution.

The files should be loaded by [Dr.Egeria](https://egeria-project.org/user-interfaces/dr-egeria/overview/) commands in the following order:

* [external-references.md](external-references.md)
* [glossary.md](glossary.md)
* [regulation.md](regulation.md)
* [collections.md](collections.md)

There is a choice on how to do this depending on the tools you are most comfortable with using.

* If you are in a **Jupyter environment** (such as JupyterHub in egeria-workspaces) open the [Jupyter Notebook `load-martyns-law.ipynb`](load-martyns-law.ipynb) and follow the instructions.
* If you are reading this from **Obsidian**, open the [load-martyns-law](load-martyns-law.canvas) canvas and select each file in order and click the suitcase icon *Calling the Dr, (MCP)*.
  You will see messages indicating that the file is being processed and a pop-up window indicating the results.  Click outside of the pop-up window to dismiss it once you have reviewed it.
* If you wish to use the command line, use `dr_egeria --process fileName` for each file in turn.  The full help for the Dr.Egeria command is `dr_egeria --help`.

____
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.