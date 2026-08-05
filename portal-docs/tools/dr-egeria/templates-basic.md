# Dr. Egeria — Basic Templates

Ready-to-use command templates for common Egeria operations. Copy any template into an Obsidian note and run it with the [Call Dr. Egeria](../obsidian.md) plugin.

Browse and copy individual files from the full template library:
[Basic templates](/Dr-Egeria-Samples/templates/basic) · [Advanced templates](/Dr-Egeria-Samples/templates/advanced)

---

## Glossary

### View all glossaries
```markdown
# View Glossaries
```

### View terms in a glossary
```markdown
# View Glossary Terms
Glossary: Business Glossary
```

### Create a glossary term
```markdown
# Create Glossary Term
Term: Customer
Glossary: Business Glossary
Summary: A person or organisation that purchases products or services.
```

### Create an informal tag
```markdown
# Create Informal Tag
Tag Name: confidential
Description: Marks assets containing sensitive information.
```

---

## Governance

### View governance zones
```markdown
# View Governance Zones
```

### View governance definitions
```markdown
# View Governance Definitions
```

---

## Feedback

### Create a comment
```markdown
# Create Comment
Element: [GUID or qualified name]
Comment: This dataset needs quality review before use in reporting.
```

### Create a journal entry
```markdown
# Create Journal Entry
Display Name: Data quality review — Q2 2026
Description: Completed initial review of clinical trial datasets. Three tables flagged for remediation.
```
A private entry in your own activity journal — see also `Create Activity
Entry` (public, tracks completion status) and `Create Blog Entry` (public,
broadcasts more widely). All three post to your own profile; use `Create
Note` instead to attach an opinion/annotation to any *other* element.

---

## Solution Architect

### View solution blueprints
```markdown
# View Solution Blueprints
```

### Create a solution blueprint
```markdown
# Create Solution Blueprint
Name: Clinical Data Pipeline
Description: End-to-end pipeline from lab systems to analytics platform.
```

### Create a design pattern
```markdown
# Create Design Pattern
Name: Batch Ingestion Pattern
Description: Periodic bulk load of source data into a staging area.
Problem Statement: Source systems only expose full-file exports on a schedule, not real-time events.
Solution Description: Land the file in staging, validate, then merge into the target on a fixed cadence.
```

### Link two design patterns as nested
```markdown
# Link Nested Design Patterns
Parent Design Pattern: DesignPattern::Batch Ingestion Pattern
Nested Design Pattern: DesignPattern::File Validation Pattern
```

### Link a specialized design pattern
```markdown
# Link Specialized Design Patterns
General Design Pattern: DesignPattern::Batch Ingestion Pattern
Specialized Design Pattern: DesignPattern::CSV Batch Ingestion Pattern
```

### Link two related design patterns
```markdown
# Link Related Design Patterns
Design Pattern 1: DesignPattern::Batch Ingestion Pattern
Design Pattern 2: DesignPattern::Event Streaming Pattern
```

---

## Project management

### Create a project
```markdown
# Create Project
Name: Data Governance Initiative 2026
Description: Programme to improve data quality across all Coco systems.
```

### Create a personal project
```markdown
# Create Personal Project
Name: Glossary review — finance terms
```

---

## Reports & Dashboards

### View a report
```markdown
# Report
Report Spec: [report spec name, e.g. 'Digital-Products', 'Collections']
```

### Create a report (with default parameters, for placing on a dashboard)
```markdown
## Create Report
Display Name: Governance Coverage
Report Spec: Analytic Demo - Governance Coverage
Output Format: DICT
```

### Create a dashboard sheet
```markdown
## Create Dashboard Sheet
Display Name: Governance Overview
Dashboard Sheet Heading: Governance Overview
```

### Place a report on a dashboard sheet
```markdown
## Link Report to Dashboard Sheet
Dashboard Sheet Name: Governance Overview
Report Name: Governance Coverage
Placement Span: full
Placement Emphasis: panel
```

### Add explanatory text to a dashboard sheet
```markdown
## Add Text on Dashboard Sheet
Dashboard Sheet Name: Governance Overview
Placement Name: Intro Caption
MD Content: This dashboard tracks **governance classification coverage** across the catalog.
Placement Span: full
Placement Emphasis: panel
```

---

> **Tip:** Set **Default Directive** to `validate` in the plugin settings while drafting new commands. Switch to `process` when ready to execute.

See also: [Advanced Templates](templates-advanced.md)
