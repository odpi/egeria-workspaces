<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Going CFC Free

This folder supports the [CFC-Free Initiative](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/sustainability-initiative/overview/#the-cfc-free-initiative) within the sustainability program.  The [load-refrigeration-units.ipynb](load-refrigeration-units.ipynb) notebook adds the new *Equipment* and *RefrigerationUnit* open metadata types to Egeria, sets up the valid values for *refrigerantType*, and loads the refrigeration units below, linking each one to its site.  It can be safely rerun.

The [ny-refrigeration-unit-replacement.ipynb](ny-refrigeration-unit-replacement.ipynb) notebook follows the New York Lab, the first site to go CFC-free.  It registers the lab's new R-290 freezer (REF-NYC-010) and retires its R-12 freezer (REF-NYC-009) by setting its *deploymentStatus* to *DISABLED* and archiving it.  Run it after `load-refrigeration-units.ipynb`.

## Refrigerant data

Created [coco_refrigeration_units.csv](data/coco_refrigeration_units.csv) with 57 units across 7 sites.  All of the units are in use, so their `deployment_status` is `ACTIVE`.  Here's a summary:

**Units by location:**
| Site | Units | CFC units | ID prefix |
|---|---|---|---|
| New York, USA | 9 | 1 | REF-NYC-* |
| Austin, USA | 9 | 1 | REF-AUS-* |
| Edmonton, Canada | 9 | 2 | REF-EDM-* |
| Winchester, UK | 8 | 1 | REF-WIN-* |
| London, UK | 6 | 1 | REF-LON-* |
| Amsterdam, NL | 7 | 1 | REF-AMS-* |
| Bucharest, Romania | 9 | 2 | REF-BUC-* |

**Refrigerant types used** — chosen to reflect a realistic pharmaceutical estate spanning different eras and sustainability transitions:
- `R-134a` — common legacy HFC in lab fridges and large chillers
- `R-290` (propane) — natural refrigerant used in Panasonic -80°C freezers
- `R-170` (ethane) — used in Thermo Fisher Forma ultra-low freezers
- `R-600a` (isobutane) — Liebherr pharmacy fridges
- `R-404A` — older walk-in cold rooms (high GWP, being phased out under F-Gas regulations)
- `R-410A` — rooftop HVAC units
- `R-32` — Daikin process chillers and VRV systems (lower GWP than R-410A)
- `R-1234ze` — low-GWP HFO used in the Amsterdam chiller (sustainability programme)

**CFC refrigerants** — the targets of the initiative.  Their production was banned under the Montreal Protocol, but each site still has at least one unit from the late 1980s or early 1990s that uses one:
- `R-12` — older fridges and freezers (REF-NYC-009, REF-AUS-009, REF-WIN-008, REF-LON-006, REF-BUC-008)
- `R-502` — older low-temperature freezers (REF-EDM-008, REF-AMS-007)
- `R-11` — low-pressure centrifugal chiller (REF-EDM-009)
- `R-500` — centrifugal chiller (REF-BUC-009)

A few units are flagged as ageing or approaching end-of-life (REF-LON-005, REF-BUC-004, and all of the CFC units) and show higher leakage rates, which adds realism for any sustainability or asset management analysis.