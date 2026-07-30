# Dr. Egeria — Advanced Templates

Advanced command templates for information supply chains, data design, and complex governance operations.

Browse and copy individual files from the full template library:
[Basic templates](/Dr-Egeria-Samples/templates/basic) · [Advanced templates](/Dr-Egeria-Samples/templates/advanced)

---

## Information Supply Chains

### View information supply chains
```markdown
# View Information Supply Chains
```

### Create an information supply chain
```markdown
# Create Information Supply Chain
Name: Clinical Trial Data Flow
Description: Flow of data from lab systems through QA into the clinical data warehouse.
```

### Link information supply chain peers
```markdown
# Link Information Supply Chain Peers
ISC 1: Clinical Trial Data Flow
ISC 2: Regulatory Reporting Pipeline
```

---

## Solution Architecture

### Create a solution component
```markdown
# Create Solution Component
Name: Lab Data Extractor
Description: Extracts raw assay data from the LIMS system.
Blueprint: Clinical Data Pipeline
```

### Create a solution role
```markdown
# Create Solution Role
Name: Data Steward — Clinical
Description: Responsible for clinical data quality and compliance.
```

### Link solution component peers
```markdown
# Link Solution Component Peers
Component 1: Lab Data Extractor
Component 2: QA Validator
```

---

## Data Design

### View data structures
```markdown
# View Data Structures
```

### View data fields for a structure
```markdown
# View Data Fields
Structure: [qualified name or display name]
```

---

## Digital Products

### View digital products
```markdown
# View Digital Products
```

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
Display Name: Terms Growth (90 Days)
Report Spec: Analytic Demo - Catalog Growth Trend
Output Format: SERIES
Analytic Parameters:
  window: 90d
  points: 12
```

### Create a report against a generic analytic function, retargeted at a different type
```markdown
## Create Report
Display Name: Digital Product Count
Report Spec: Analytic Demo - Element Count by Type
Output Format: DICT
Analytic Parameters:
  type_name: DigitalProduct
```

> `Analytic Parameters` set here are **defaults**, not fixed pins — a caller
> (or a later `Update Report`) can still override the same keys. See
> `docs/output-formats-and-report-specs.md` (egeria-python) for the full
> generic-vs-fixed-metric distinction.

---

## Batch processing

Dr. Egeria processes one command block per note. For batch operations, create a note with multiple commands separated by horizontal rules — each block is processed in sequence:

```markdown
# Create Glossary Term
Term: Supplier
Glossary: Business Glossary
Summary: An organisation that provides goods or services to Coco Pharmaceuticals.

---

# Create Glossary Term
Term: Product Batch
Glossary: Manufacturing Glossary
Summary: A quantity of product manufactured in a single production run.
```

> **Note:** Batch support depends on the backend version. Check with `validate` first.

---

See also: [Basic Templates](templates-basic.md) · [Dr. Egeria overview](overview.md)
