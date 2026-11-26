<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Dr.Egeria Templates

The Markdown files in the two subdirectories _basic_ and _advanced_ are used to add Dr.Egeria commands to a Markdown document.

Each file contains the template for one Dr.Egeria command.  The versions under _basic_ are the simplest form of the command and can be used in most circumstances.  The versions under _advanced_ show all the available options.

The subsections of each command define an attribute, or a classification, or a relationship.  Each subsection describes whether the subsection is required, the types of values and how they are used.

## Solution boundaries

_Solution Architect_ has two commands for boundaries, from pyegeria 6.3.4: _Create Solution Boundary_ and _Create Design Model Boundary_. They need an Egeria platform with odpi/egeria#9465. Members are added with the Collection Membership commands. Egeria refuses to delete a boundary that still has members, so remove its members first.

**Known issue (egeria-python #613):** on an Update, give the Version Identifier, the Qualified Name or the GUID. Create fills in the Version Identifier (default 1.0) and puts it in the qualified name, but Update does not, so an Update that names only the Display Name can miss the element and create a duplicate. This affects most Create commands, not only the boundaries.

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
