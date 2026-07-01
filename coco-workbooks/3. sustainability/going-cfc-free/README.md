<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Going CFC Free


## Refrigerant data

Created [coco_refrigeration_units.csv](data/coco_refrigeration_units.csv) with 50 units across 7 sites. Here's a summary:

**Units by location:**
| Site | Units | ID prefix |
|---|---|---|
| New York, USA | 8 | REF-NYC-* |
| Austin, USA | 8 | REF-AUS-* |
| Edmonton, Canada | 7 | REF-EDM-* |
| Winchester, UK | 7 | REF-WIN-* |
| London, UK | 5 | REF-LON-* |
| Amsterdam, NL | 6 | REF-AMS-* |
| Bucharest, Romania | 7 | REF-BUC-* |

**Refrigerant types used** — chosen to reflect a realistic pharmaceutical estate spanning different eras and sustainability transitions:
- `R-134a` — common legacy HFC in lab fridges and large chillers
- `R-290` (propane) — natural refrigerant used in Panasonic -80°C freezers
- `R-170` (ethane) — used in Thermo Fisher Forma ultra-low freezers
- `R-600a` (isobutane) — Liebherr pharmacy fridges
- `R-404A` — older walk-in cold rooms (high GWP, being phased out under F-Gas regulations)
- `R-410A` — rooftop HVAC units
- `R-32` — Daikin process chillers and VRV systems (lower GWP than R-410A)
- `R-1234ze` — low-GWP HFO used in the Amsterdam chiller (sustainability programme)

A few units are flagged as ageing or approaching end-of-life (REF-LON-005, REF-BUC-004) and show higher leakage rates, which adds realism for any sustainability or asset management analysis.