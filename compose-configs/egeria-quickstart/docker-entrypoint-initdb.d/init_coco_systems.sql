-- Coco Pharmaceuticals system databases - one per system estate.
--
-- The source systems behind the Strategic Digital Product Catalog
-- (coco-workbooks/1. coco-data-hub/strategic-digital-products/), one schema per
-- system, holding only the tables needed to fill the digital products' tables in
-- coco_data_hub, with sample data:
--
--  * coco_pharma       - the Coco Pharmaceuticals systems (the parent company).
--                        Already exists; it also holds coco_ods and coco_sus.
--  * austin_systems    - the systems of the acquired Austin site.
--  * bucharest_systems - the systems of the acquired EKG Pharmaceuticals S.R.L.
--                        in Bucharest.
--
-- A system is here when the component-system mapping links it to a digital
-- product's solution component with an ImplementedBy relationship (Strong or
-- Probable confidence).  The queries that copy each system's data into the
-- product tables are in exchange-quickstart/coco-dags/coco-system-extracts/
-- <database>/<system schema>/, where the coco_feed_* Airflow DAGs run them.
--
-- Run by bin/apply-postgres-init.sh on every start, after init_egeria.sql (which
-- creates coco_pharma and the roles granted below).  Safe to run again: every
-- object is created only if missing and every seed row is inserted ON CONFLICT
-- DO NOTHING: a seed row that has been changed stays changed, but one that has
-- been deleted comes back.

SELECT 'CREATE DATABASE austin_systems'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'austin_systems')\gexec

SELECT 'CREATE DATABASE bucharest_systems'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'bucharest_systems')\gexec

grant all privileges on database austin_systems to egeria_admin, egeria_user, airflow_user;
grant all privileges on database bucharest_systems to egeria_admin, egeria_user, airflow_user;

-- The cataloguer's surveyor user gets the same database-level access it has to
-- coco_pharma.  Guarded because an install whose Postgres predates that user has
-- no surveyor role.
DO $$
BEGIN
  IF EXISTS (SELECT FROM pg_roles WHERE rolname = 'surveyor') THEN
    GRANT ALL PRIVILEGES ON DATABASE austin_systems TO surveyor;
    GRANT ALL PRIVILEGES ON DATABASE bucharest_systems TO surveyor;
  END IF;
END
$$;

\connect coco_pharma
SET client_min_messages = warning;
\ir data/coco_systems/coco_pharma/aus_inventory.sql
\ir data/coco_systems/coco_pharma/austin_haz_mat.sql
\ir data/coco_systems/coco_pharma/ca_payroll.sql
\ir data/coco_systems/coco_pharma/coco_expenses.sql
\ir data/coco_systems/coco_pharma/coco_haz_mat.sql
\ir data/coco_systems/coco_pharma/coco_hrim.sql
\ir data/coco_systems/coco_pharma/coco_inventory.sql
\ir data/coco_systems/coco_pharma/coco_ledgers.sql
\ir data/coco_systems/coco_pharma/coco_products.sql
\ir data/coco_systems/coco_pharma/cocopages.sql
\ir data/coco_systems/coco_pharma/ed_mfg_control.sql
\ir data/coco_systems/coco_pharma/eddepot01.sql
\ir data/coco_systems/coco_pharma/global_crm.sql
\ir data/coco_systems/coco_pharma/kcdepot01.sql
\ir data/coco_systems/coco_pharma/manufacturing_planning.sql
\ir data/coco_systems/coco_pharma/mfctrl9482.sql
\ir data/coco_systems/coco_pharma/nl_payroll.sql
\ir data/coco_systems/coco_pharma/procurement01.sql
\ir data/coco_systems/coco_pharma/sec_admin.sql
\ir data/coco_systems/coco_pharma/uk_payroll.sql
\ir data/coco_systems/coco_pharma/winch_mfg_control.sql
\ir data/coco_systems/coco_pharma/winchdepot01.sql

\connect austin_systems
SET client_min_messages = warning;
\ir data/coco_systems/austin_systems/active_directory.sql
\ir data/coco_systems/austin_systems/apache_kafka.sql
\ir data/coco_systems/austin_systems/arcgis.sql
\ir data/coco_systems/austin_systems/cloudera_cdp.sql
\ir data/coco_systems/austin_systems/cornerstone_lms.sql
\ir data/coco_systems/austin_systems/entra_id.sql
\ir data/coco_systems/austin_systems/factorytalk_scada.sql
\ir data/coco_systems/austin_systems/ibm_maximo.sql
\ir data/coco_systems/austin_systems/informatica_idmc.sql
\ir data/coco_systems/austin_systems/informatica_mdm.sql
\ir data/coco_systems/austin_systems/labware_lims.sql
\ir data/coco_systems/austin_systems/manhattan_wms.sql
\ir data/coco_systems/austin_systems/microsoft_365.sql
\ir data/coco_systems/austin_systems/opcenter_mes.sql
\ir data/coco_systems/austin_systems/opentext_edi.sql
\ir data/coco_systems/austin_systems/oracle_oms.sql
\ir data/coco_systems/austin_systems/oracle_tms.sql
\ir data/coco_systems/austin_systems/purview_dlp.sql
\ir data/coco_systems/austin_systems/salesforce_crm.sql
\ir data/coco_systems/austin_systems/sap_ariba.sql
\ir data/coco_systems/austin_systems/sap_s4hana.sql
\ir data/coco_systems/austin_systems/servicenow_csm.sql
\ir data/coco_systems/austin_systems/ukg_dimensions.sql
\ir data/coco_systems/austin_systems/veeva_ebr.sql
\ir data/coco_systems/austin_systems/veeva_qms.sql
\ir data/coco_systems/austin_systems/waters_empower.sql
\ir data/coco_systems/austin_systems/workday_hcm.sql

\connect bucharest_systems
SET client_min_messages = warning;
\ir data/coco_systems/bucharest_systems/active_directory.sql
\ir data/coco_systems/bucharest_systems/ekg_wms.sql
\ir data/coco_systems/bucharest_systems/empower_cds.sql
\ir data/coco_systems/bucharest_systems/factorytalk.sql
\ir data/coco_systems/bucharest_systems/kronos_workforce.sql
\ir data/coco_systems/bucharest_systems/labware_lims.sql
\ir data/coco_systems/bucharest_systems/maximo.sql
\ir data/coco_systems/bucharest_systems/microsoft_365.sql
\ir data/coco_systems/bucharest_systems/opcenter_mes.sql
\ir data/coco_systems/bucharest_systems/opentext_ecm.sql
\ir data/coco_systems/bucharest_systems/proact_cold_chain.sql
\ir data/coco_systems/bucharest_systems/sap_concur.sql
\ir data/coco_systems/bucharest_systems/sap_s4hana.sql
\ir data/coco_systems/bucharest_systems/trackwise.sql
\ir data/coco_systems/bucharest_systems/veeva_qms.sql
\ir data/coco_systems/bucharest_systems/veeva_rim.sql
\ir data/coco_systems/bucharest_systems/workday_hcm.sql
