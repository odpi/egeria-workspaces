# Dr. Egeria — Advanced Templates

Advanced command templates for information supply chains, data design, and complex governance operations.

The full template library is also available at [/Dr-Egeria-Samples](/Dr-Egeria-Samples).

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
