# Walkthrough - Sales Forecast Consolidation Governance Walkthrough

We have created an end-to-end, multi-system metadata governance scenario for the **Sales Forecast Consolidation Project** at Coco Pharmaceuticals. 

All workbooks, data generators, and plans are organized under a new directory in your workspaces:
👉 [5. sales-forecast-consolidation](file:///Users/dwolfson/localGit/egeria-v6/egeria-workspaces-fs/coco-workbooks/5.%20sales-forecast-consolidation/)

---

## 1. Components Created

### A. Data Generation
*   **Generator Script:** [generate_synthetic_sales_data.py](file:///Users/dwolfson/localGit/egeria-v6/egeria-workspaces-fs/coco-workbooks/5.%20sales-forecast-consolidation/sales_forecast_consolidation_setup/generate_synthetic_sales_data.py)
    *   Creates PostgreSQL schemas (`us_sales`, `eu_sales`, `target_sales`) and tables in the docker PostgreSQL container (`coco_pharma` database, port 5442).
    *   Generates a local UK CSV spreadsheet: [uk_sales_forecast.csv](file:///Users/dwolfson/localGit/egeria-v6/egeria-workspaces-fs/coco-workbooks/5.%20sales-forecast-consolidation/uk_sales_forecast.csv).
    *   Fills data with **3 years of historical opportunities** (mid-2023 to mid-2026), implementing a 12% annual growth curve and Q4 seasonality volume spikes.
    *   Includes advanced columns: `OpportunityID` / `deal_id`, `CloseDate` / `expected_close_date`, `SalesStage` (e.g. Commit, Upside), `Currency`, and `CreatedDate`.

*   **Workbook:** [1. generate-sales-data.ipynb](file:///Users/dwolfson/localGit/egeria-v6/egeria-workspaces-fs/coco-workbooks/5.%20sales-forecast-consolidation/1.%20generate-sales-data.ipynb)
    *   Executes the generator script and uses pandas to print a yearly opportunity and revenue growth summary.

### B. Technical Cataloging (Resource Explorer)
*   **Manual Onboarding:** The US/EU PostgreSQL databases and UK CSV spreadsheet are onboarded manually using the **Resource Explorer** tool located at [resource-explorer](file:///Users/dwolfson/localGit/egeria-v6/resource-explorer).
*   **Reference Workbook:** [2. onboarding-resource-explorer.ipynb](file:///Users/dwolfson/localGit/egeria-v6/egeria-workspaces-fs/coco-workbooks/5.%20sales-forecast-consolidation/2.%20onboarding-resource-explorer.ipynb)
    *   Provides a programmatic reference showing the exact Automated Curation API client calls (`create_postgres_database_element_from_template`, `create_csv_data_file_element_from_template`, and `add_catalog_target`) that register these assets and link them to Egeria's cataloguer behind the scenes.

### C. Governance & Organizational Blueprint
*   **Dr. Egeria Plan:** [sales_forecast_governance_plan.md](file:///Users/dwolfson/localGit/egeria-v6/egeria-workspaces-fs/coco-workbooks/5.%20sales-forecast-consolidation/sales_forecast_governance_plan.md)
    *   Markdown plan detailing:
        1.  **Organizational context:** Creates Person `Tom Tally`, Team `Global Finance Team`, assigns Tom as the project leader, and assigns the team to the project.
        2.  **Glossary & Terms:** Creates `Sales Forecasting Glossary` and mapping terms (`Sales Forecast`, `Expected Close Date`, `Sales Pipeline Stage`, `Opportunity ID`).
        3.  **Blueprints & Lineage:** Defines the `Sales Forecast Database Blueprint` and `Sales Forecast Consolidation Supply Chain`.

*   **Workbook:** [3. governance-setup.ipynb](file:///Users/dwolfson/localGit/egeria-v6/egeria-workspaces-fs/coco-workbooks/5.%20sales-forecast-consolidation/3.%20governance-setup.ipynb)
    *   Asynchronously parses and executes the Dr. Egeria markdown plan.
    *   Instantiates the `CommunityMatters` OMVS client to create the `Sales Forecasting Governance Community`.

### D. Context-Intelligence AI Integration (Local Ollama)
*   **Workbook:** [4. context-intelligence-ai.ipynb](file:///Users/dwolfson/localGit/egeria-v6/egeria-workspaces-fs/coco-workbooks/5.%20sales-forecast-consolidation/4.%20context-intelligence-ai.ipynb)
    *   Demonstrates how models dynamically query Egeria for schema attributes mapping to `Sales Forecast` and `Expected Close Date`, avoiding breaking when database columns change (Tier 1).
    *   Integrates a local Ollama model (`llama3.1:8b` or `qwen2.5-coder:latest` running on `localhost:11434`) in a RAG pipeline to answer natural-language governance questions about the consolidated forecasting process using Egeria's context (Tier 2).

---

## 2. Walkthrough Validation Results

We executed a full dry-run of the walkthrough script which succeeded with the following logs:
1.  **PostgreSQL schemas created:** `us_sales`, `eu_sales`, `target_sales` tables populated in `coco_pharma` database.
2.  **Spreadsheet created:** `uk_sales_forecast.csv` written successfully with seasonal opportunity data.
3.  **Technical cataloging:** `coco_pharma` database and UK CSV spreadsheet registered.
4.  **Dr. Egeria run:** Glossary terms, project, team assignments (`Link Assignment Scope`), blueprints, and supply chains successfully created in Egeria.
5.  **Community creation:** `Sales Forecasting Governance Community` registered.

---

## 3. How to Inspect in Egeria Workspaces

To view the generated relationships:
1.  Open Egeria Portal's **Repository Explorer** (via Egeria Workspaces).
2.  Search for `Project::Sales-Forecast-Consolidation-Project` or `Glossary::SalesForecasting` to inspect the visual relationship graph linking teams, people, glossary terms, blueprints, and supply chains together.
