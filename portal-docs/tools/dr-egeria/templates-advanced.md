# Dr. Egeria — Advanced Templates

Advanced command templates for information supply chains, data design, and complex governance operations.

Browse and copy individual files from the full template library:
[Basic templates](/Dr-Egeria-Samples/templates/basic) · [Advanced templates](/Dr-Egeria-Samples/templates/advanced)

---

## Information Supply Chains

### View information supply chains
```markdown
## View Information Supply Chain DrE Basic
```
> Note: there's currently no plain `Information Supply Chain`/`Information
> Supply Chains` report-spec alias registered — only the `DrE Basic`/
> `DrE Advanced` suffixed names resolve. Worth registering a shorter alias.

### Create an information supply chain
```markdown
## Create Information Supply Chain
### Display Name
Clinical Trial Data Flow

### Description
Flow of data from lab systems through QA into the clinical data warehouse.
```

### Link information supply chain peers
```markdown
## Link Information Supply Chain Peers
### Element Id
Clinical Trial Data Flow

### Element2 Id
Regulatory Reporting Pipeline
```

---

## Solution Architecture

### Create a solution component
```markdown
## Create Solution Component
### Display Name
Lab Data Extractor

### Description
Extracts raw assay data from the LIMS system.

### In Solution Blueprints
Clinical Data Pipeline
```

### Create a solution role
```markdown
## Create Solution Role
### Display Name
Data Steward — Clinical

### Description
Responsible for clinical data quality and compliance.
```

### Link solution component peers
```markdown
## Link Solution Components
### Component1
Lab Data Extractor

### Component2
QA Validator
```

---

## Data Design

### View data structures
```markdown
## View Data Structures
```

### View data fields for a structure
```markdown
## View Data Fields
### Structure
[qualified name or display name]
```

---

## Digital Products

### View digital products
```markdown
## View Digital Products
```

---

## Curation

Classification commands that mark an existing element as belonging to a
governance-relevant category, rather than creating anything new. Most take
just a `Target Element` (the element's qualified or display name) and an
optional `Journal Entry`.

### Classify an element as a Policy Enforcement Point
```markdown
## Classify Policy Enforcement Point
### Target Element
PostgreSQLGovernance

### Journal Entry
Flagged during the Q3 policy review as the engine that actually enforces
the data-retention rules, not just monitors them.
```

### Classify an element as Reference Data
```markdown
## Classify Reference Data
### Target Element
Country Codes
```

### Remove a classification
```markdown
## Declassify Reference Data
### Target Element
Country Codes
```

> Curation's `Classify */Declassify *` commands cover several classification
> "families" — an abstract classification type with more than one concrete
> member, e.g. `PolicyManagementPoint` (Information/Enforcement/Retrieval/
> Decision/Administration Point) or `ExecutionPoint` (Control/Verification/
> Enforcement Point). Pick the specific command for the concrete kind you
> mean (`Classify Policy Enforcement Point`, not a generic "Classify Policy
> Point") — Egeria's type system doesn't let you apply the abstract
> supertype directly. Browse the full Curation family in the
> [template library](/Dr-Egeria-Samples/templates/advanced/Curation) for
> every available kind (governance points, project/collection kinds,
> duplicate/consolidation markers, naming-standard words, and more).

---

## Reports & Dashboards (analytic functions)

Some report specs run an **analytic function** (a Python routine returning an
already-aggregated count/breakdown/series, e.g. `overview_metrics.growth_series`)
instead of querying Egeria elements directly — see the "Analytic Demo - \*"
report specs in Egeria Explorer's Report Specs browser. Set `Analytic
Parameters` to override that function's defaults; run with `Output Format:
SERIES` for a time-series line chart, `BAR`/`PIE` for a category breakdown.

### Create a report against an analytic function, with overridden parameters
```markdown
## Create Report
### Display Name
Terms Growth (90 Days)

### Report Spec
Analytic Demo - Catalog Growth Trend

### Output Format
SERIES

### Analytic Parameters
window: 90d
points: 12
```

### Create a report against a generic analytic function, retargeted at a different type
```markdown
## Create Report
### Display Name
Digital Product Count

### Report Spec
Analytic Demo - Element Count by Type

### Output Format
DICT

### Analytic Parameters
type_name: DigitalProduct
```

> `Analytic Parameters` set here are **defaults**, not fixed pins — a caller
> (or a later `Update Report`) can still override the same keys. See
> `docs/output-formats-and-report-specs.md` (egeria-python) for the full
> generic-vs-fixed-metric distinction.

Some report specs need a parameter their own action requires that isn't
part of the standard find/search set (`Search String`, `Output Format`,
`Page Size`, ...) and isn't an analytic-function parameter either — e.g.
the `Collection Members` report needs a `collection_guid` to know which
collection to list members of. Use `Report Parameters` for these — same
mechanism as `Analytic Parameters`, different keys.

### Create a report needing a report-spec-specific parameter
```markdown
## Create Report
### Display Name
Local Dashboards Tasks

### Report Spec
Collection Members

### Output Format
TABLE

### Report Parameters
collection_guid: 0affb580-fa81-4d00-9438-b26faf11845d
```

> Keys under `Report Parameters` must match exactly what the target report
> spec's action expects (snake_case, e.g. `collection_guid`) — there's no
> aliasing. Also works on `View Report` for a one-off ad-hoc run instead of
> a persisted Report.

---

## Batch processing

Dr. Egeria processes one command block per note. For batch operations, create a note with multiple commands separated by horizontal rules — each block is processed in sequence:

```markdown
## Create Glossary Term
### Display Name
Supplier

### Glossary Name
Business Glossary

### Summary
An organisation that provides goods or services to Coco Pharmaceuticals.

---

## Create Glossary Term
### Display Name
Product Batch

### Glossary Name
Manufacturing Glossary

### Summary
A quantity of product manufactured in a single production run.
```

> **Note:** Batch support depends on the backend version. Check with `validate` first.

---

See also: [Basic Templates](templates-basic.md) · [Dr. Egeria overview](overview.md)
