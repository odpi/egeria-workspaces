# Demo Scenarios

Guided walk-throughs using Coco Pharmaceuticals data to demonstrate key Egeria capabilities. Each scenario is self-contained and takes approximately 5–15 minutes.

---

## Scenario 1 — Exploring the metadata landscape (Erin Overview)

**Goal:** Show the breadth of Egeria's metadata coverage across a real organisation.
**Persona:** Erin Overview
**Tools:** Egeria Explorer, Obsidian

1. Open Egeria Explorer → **ISC tab** — walk through the information supply chains showing how clinical data flows from lab systems into the warehouse and regulatory reports
2. Switch to **Governance tab** — show the governance zones and which assets are in each zone
3. Switch to **Glossary tab** — search for "Patient Cohort" and show the full term definition, linked assets, and stewardship
4. In Obsidian, open a workbook and run `# View Glossaries` with the `display` directive

**Key message:** Egeria connects business terms, data assets, and lineage in one place.

---

## Scenario 2 — Data quality governance (Peter Profile)

**Goal:** Demonstrate how data quality rules are tracked and enforced.
**Persona:** Peter Profile
**Tools:** Egeria Explorer, Dr. Egeria

1. Open Egeria Explorer → **Data Design tab** — show the data structures with quality rules attached
2. Open Obsidian, run `# View Data Structures` — see the same structures with field-level detail
3. Create a new quality note and validate it with Dr. Egeria using the `validate` directive

**Key message:** Data quality is a first-class citizen in Egeria's open metadata model.

---

## Scenario 3 — Lineage for regulatory reporting (Tom Tally)

**Goal:** Show how Egeria traces data lineage from source to regulatory submission.
**Persona:** Tom Tally
**Tools:** Egeria Explorer

1. Open Egeria Explorer → **ISC tab** — find the financial reporting supply chain
2. Walk the lineage from the treasury data through transformation steps to the final report
3. Show the governance zone at each step — demonstrating that regulated data is properly classified throughout

**Key message:** Egeria provides the audit trail regulators require.

---

## Scenario 4 — Security classification (Ivor Padlock)

**Goal:** Show how sensitive data is classified and tracked.
**Persona:** Ivor Padlock
**Tools:** Egeria Explorer

1. Open Egeria Explorer → **Governance tab** — show security classifications
2. Filter to "Confidential" zone — show which data assets carry that classification
3. Show the Perspectives tab — organisational accountability for classified assets

**Key message:** Egeria makes security accountability visible and auditable.

---

## Scenario 5 — Using Dr. Egeria to create governed metadata (Erin Overview)

**Goal:** Show how practitioners create and link metadata using natural-language Markdown commands.
**Persona:** Erin Overview
**Tools:** Obsidian, Dr. Egeria

1. Open Obsidian, create a new note
2. Write a `# Create Glossary Term` command for a new business concept
3. Run it with the `process` directive
4. Switch to Egeria Explorer → Glossary tab — show the new term appearing

**Key message:** Dr. Egeria removes the API complexity — business users can contribute metadata directly.

---

## Adding more scenarios

Scenarios can be added as Markdown files in this directory. The viewer will render them with full Mermaid diagram support — use sequence or flow diagrams to illustrate data flows.

See also: [Coco Pharmaceuticals overview](overview.md) · [Personas](personas.md)
