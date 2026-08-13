# Implementation Plan - Sales Forecast Consolidation Governance Walkthrough

This plan outlines the steps to build a complete end-to-end demonstration scenario for the **Sales Forecast Consolidation Project** at Coco Pharmaceuticals. It integrates PostgreSQL database schemas, a spreadsheet-based forecast, Jupyter Notebooks for execution, Resource Explorer for cataloging, and Dr. Egeria for building the governance blueprint.

## User Review Required

> [!IMPORTANT]
> - **Jupyter Integration:** We will create a new directory: `/Users/dwolfson/localGit/egeria-v6/egeria-workspaces-fs/coco-workbooks/5. sales-forecast-consolidation/` to store our interactive workbooks.
> - **Data Generation:** Synthetic data will span 3 years (mid-2023 to mid-2026), incorporating seasonal peaks (e.g., Q4 spikes) and a 10–15% annual growth rate.
> - **Metadata Inspection:** We will provide instructions on using Egeria Portal tools (Repository Explorer, Type Explorer) to inspect the resulting metadata graphs.

## Proposed Changes

### 1. Synthetic Data Generation (3-Year History)

We will write a generation script to produce historical and current sales pipeline records.

#### [NEW] [generate_synthetic_sales_data.py](file:///Users/dwolfson/localGit/egeria-v6/egeria-workspaces-fs/coco-workbooks/5.%20sales-forecast-consolidation/sales_forecast_consolidation_setup/generate_synthetic_sales_data.py)
*   **Purpose:** Generate synthetic records containing rich sales pipeline attributes and populate PostgreSQL/CSVs.
*   **Time Span:** 3 years (July 2023 to June 2026).
*   **Growth & Trends:** Seasonality (Q4 spikes) and a steady 12% year-over-year compound growth in revenue values.
*   **Data Structures & Attributes:**
    *   **US Sales (PostgreSQL schema `us_sales`):** Table `us_sales_forecast` containing columns: `RecordID`, `Date`, `RepID`, `ProductLine`, `ForecastAmount`, `ConfidenceLevel`, `OpportunityID`, `SalesStage` (e.g. Commit, Upside, Pipeline), `CloseDate`, `Currency` (USD), `CreatedDate`.
    *   **EU Sales (PostgreSQL schema `eu_sales`):** Table `eu_sales_forecast` containing columns: `uid`, `datum`, `mitarbeiter`, `kategorie`, `wert_eur`, `status` (confidence), `deal_id`, `stage`, `expected_close_date`, `currency` (EUR), `creation_date`.
    *   **UK Sales (Local CSV Spreadsheet):** File `uk_sales_forecast.csv` containing columns: `id`, `forecast_date`, `sales_rep`, `segment`, `value_gbp`, `probability`, `deal_id`, `stage`, `close_date`, `currency` (GBP), `creation_date`.
    *   **Forecast Target (PostgreSQL schema `target_sales`):** Table `consolidated_forecast` containing columns: `ConsolidatedID`, `Region`, `Date`, `ProductLine`, `AmountUSD`, `ConfidencePercent`, `OpportunityID`, `SalesStage`, `CloseDate`, `CreatedDate`.

---

### 2. Jupyter Workbooks

We will create a structured set of notebooks inside the workspaces directory to document and execute the scenario step-by-step.

#### [NEW] Directory: `/Users/dwolfson/localGit/egeria-v6/egeria-workspaces-fs/coco-workbooks/5. sales-forecast-consolidation/`

*   #### [NEW] `1. generate-sales-data.ipynb`
    *   Notebook executing `generate_synthetic_sales_data.py` to create the PostgreSQL tables and export the UK CSV file. Contains pandas analyses to plot the 3-year growth and seasonal trends.
*   #### [NEW] `2. onboarding-resource-explorer.ipynb`
    *   Notebook serving as a programmatic reference for using Egeria's **Resource Explorer** API client to crawl and onboard the US/EU Postgres tables and catalog the UK CSV (which is manually performed using the Resource Explorer tool).
*   #### [NEW] `3. governance-setup.ipynb`
    *   Notebook invoking Dr. Egeria to parse and execute the logical governance plan markdown file, establishing terms, blueprints, communities, and supply chains.

---

### 3. Egeria Metadata Cataloging & Governance

We will write a Dr. Egeria plan for the semantic and organizational structures.

#### [NEW] [sales_forecast_governance_plan.md](file:///Users/dwolfson/localGit/egeria-v6/egeria-advisor/sample-data/sales_forecast_governance_plan.md)
*   **Purpose:** A markdown plan executed by Dr. Egeria defining:
    1.  **Organizational Setup:**
        *   Create `Person` profiles (e.g. Tom Tally, Harry Hopeful).
        *   Create `Team` profiles (e.g., `Global Finance Team`, `Regional Sales Leads`).
        *   Create a `Community` profile: `Sales Forecasting Community`.
        *   Link leadership roles, membership assignments, and associate teams to the `Sales-Forecast-Consolidation-Project`.
    2.  **Glossary & Terms:**
        *   Create a `Sales Forecasting Glossary`.
        *   Create terms: `Sales Forecast`, `Historical Sales`, `Expected Close Date`, `Sales Pipeline Stage`, `Opportunity ID`.
        *   Map the cataloged columns (from Resource Explorer) to these business terms.
    3.  **Blueprints & Supply Chains:**
        *   Define `SolutionBlueprint::Sales-Forecast-Database-Blueprint`.
        *   Model `InformationSupplyChain::Sales-Forecast-Consolidation-Supply-Chain` showing the lineage from PostgreSQL and CSV to the consolidated target.
    4.  **Governance Controls:**
        *   Set up a `GovernanceZone` called `sales-forecast`.
        *   Define a `GovernancePolicy` for PII protection (e.g., masking sales reps' names).
        *   Define a `GovernanceRule` for data retention (retaining historical forecast tables for 7 years).

---

### 4. Context-Intelligence AI Integration (Local Ollama)

We will build an interactive local AI setup showing how both analytical and generative models query Egeria to maintain contextual awareness.

#### [NEW] `4. context-intelligence-ai.ipynb`
*   **Tier 1 (Analytical AI - Feature Mapper):**
    *   Queries Egeria's Glossary and Column Mappings to fetch the names of the columns mapped to `Sales Forecast` and `Expected Close Date` across the different schemas.
    *   Loads US, EU, and UK datasets using these dynamic column lookups (rather than hardcoded values), demonstrating resilience to schema changes.
*   **Tier 2 (Generative AI - Local RAG Q&A):**
    *   Uses a local Ollama model (e.g. `llama3.1:8b` or `qwen2.5-coder`) running on `localhost:11434`.
    *   Retrieves context from Egeria (e.g., project team roles, Glossary definitions, and lineage) and feeds it into the LLM prompt to answer natural language questions about the forecasting process (e.g., *"Who is the leader of the forecast project?"* or *"What is the source lineage for UK data?"*).

---

## Verification Plan

### Automated Tests
- Run `1. generate-sales-data.ipynb` to verify data generation.
- Run `poetry run pytest` to ensure Dr. Egeria parses the organizational, blueprint, and supply chain commands correctly.

### Manual Verification
1.  Verify the PostgreSQL schemas and tables exist in the docker container.
2.  Open Egeria Portal's **Repository Explorer** (accessible via Egeria Workspaces) to visually inspect the relationships between database schemas, columns, glossary terms, projects, and communities.
3.  Execute the final governance setup and check that all project members are assigned correctly under `Actor-Profiles` reports.
