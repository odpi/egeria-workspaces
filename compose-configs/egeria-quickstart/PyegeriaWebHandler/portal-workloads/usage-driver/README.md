<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Usage workload driver

An admin tool for generating usage activity in the quickstart's Coco content. It appears in **Admin →
Data Initialization** as **Portal — Usage Workload (admin)**, unselected by default, and is registered in
`bootstrap_batches._EXTRA_BATCH_ROOTS`. It lives here, beside the portal's own initialization files, so it
does not show up in `coco-workbooks` or the Dr.Egeria inbox that Coco users browse.

`usage-driver.ipynb` logs in as several Coco personas. Each one searches for the things it cares about,
opens some of what it finds (a few elements far more often than others), looks at members of its
favourite collections, and leaves one like and one rating. Egeria's Pepys Activity Observer turns that
into `UsageActivity` counts, and the Lovelace popularity profiler rolls them up into each collection's
`MemberPopularityProfile`. Both run on their own refresh cycles, so profiles change some minutes after a run.

The first code cell holds the parameters: personas and their search strings, how many opens, whether to
leave feedback, a time budget and a random seed. The last cell prints what each persona did and which
elements were opened most.

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
