-- system-qualified-name: SoftwareServer::AUS-SYS-039::SN-DLP-AU-20220601
-- Microsoft Purview DLP - Austin.  Microsoft Purview for Austin: the data map of scanned sources and assets, sensitive
-- information type classifications, the privacy managed attributes that link assets to the record of processing, and
-- the governance health actions raised on discrepancies.  Its tables feed Personal Data Discovery Findings.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS purview_dlp;
COMMENT ON SCHEMA purview_dlp IS 'Microsoft Purview (Austin account): data sources, data map assets, classifications, managed attributes and health actions as landed by the Purview REST API export.';

CREATE TABLE IF NOT EXISTS purview_dlp.data_source (
  data_source_name varchar(80) NOT NULL,
  kind             varchar(40) NOT NULL,
  collection_name  varchar(80) NOT NULL,
  registered_at    timestamptz NOT NULL,
  CONSTRAINT data_source_pk PRIMARY KEY (data_source_name)
);
COMMENT ON TABLE purview_dlp.data_source IS 'Registered data sources.';

INSERT INTO purview_dlp.data_source (data_source_name, kind, collection_name, registered_at) VALUES
('SAP-S4-AUS', 'SapS4Hana', 'Austin', '2022-07-11 10:00:00+00'),
('Workday-AUS', 'Workday', 'Austin', '2022-07-11 10:00:00+00'),
('Salesforce-AUS', 'Salesforce', 'Austin', '2022-07-11 10:00:00+00'),
('ServiceNow-AUS', 'ServiceNow', 'Austin', '2022-07-11 10:00:00+00'),
('OracleFusion-OM-AUS', 'OracleFusion', 'Austin', '2022-07-11 10:00:00+00'),
('VeevaVault-QMS-AUS', 'VeevaVault', 'Austin', '2022-07-11 10:00:00+00'),
('SharePoint-AUS', 'SharePointOnline', 'Austin', '2022-07-11 10:00:00+00'),
('OneDrive-AUS', 'OneDrive', 'Austin', '2022-07-11 10:00:00+00'),
('Hive-CDP-AUS', 'Hive', 'Austin', '2022-07-11 10:00:00+00')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS purview_dlp.data_map_asset (
  guid              uuid NOT NULL,
  qualified_name    varchar(400) NOT NULL,
  name              varchar(200) NOT NULL,
  asset_type        varchar(40) NOT NULL,
  data_source_name  varchar(80) NOT NULL,
  collection_name   varchar(80) NOT NULL,
  created_at        timestamptz NOT NULL,
  data_subject_hint varchar(20),
  CONSTRAINT data_map_asset_pk PRIMARY KEY (guid)
);
COMMENT ON TABLE purview_dlp.data_map_asset IS 'Data map assets (only those with sensitive classifications are landed); data_subject_hint is the scan rule set''s subject category.';

INSERT INTO purview_dlp.data_map_asset (guid, qualified_name, name, asset_type, data_source_name, collection_name, created_at, data_subject_hint) VALUES
('4972f3a6-1ca8-20de-f3e9-2b2f44559b5f', 'workday://aus/Worker', 'Worker', 'workday_business_object', 'Workday-AUS', 'Austin', '2026-02-14 04:00:00+00', 'employee'),
('2498ddfa-ecc9-0068-dde4-f099eedb4f69', 'sap://aus/100/LFBK', 'LFBK', 'sap_s4hana_table', 'SAP-S4-AUS', 'Austin', '2026-02-15 04:00:00+00', 'other'),
('d377f24c-7614-8eb8-37e9-42fca01c7e0c', 'salesforce://aus/Contact', 'Contact', 'salesforce_object', 'Salesforce-AUS', 'Austin', '2026-02-16 04:00:00+00', 'hcp'),
('461e306c-b1f2-5f6e-11f4-629d82796c51', 'salesforce://aus/Therapy_Order__c', 'Therapy_Order__c', 'salesforce_object', 'Salesforce-AUS', 'Austin', '2026-02-16 04:00:00+00', 'patient'),
('02ac1c28-c8a1-c3e9-10ec-626ef0083bc4', 'servicenow://aus/sn_customerservice_case', 'sn_customerservice_case', 'servicenow_table', 'ServiceNow-AUS', 'Austin', '2026-03-03 04:00:00+00', 'patient'),
('17aa2c10-b58f-4ba8-227b-c6b82c93fa63', 'oraclefusion://aus/DOO_HEADERS_EFF_B', 'DOO_HEADERS_EFF_B', 'oracle_fusion_view', 'OracleFusion-OM-AUS', 'Austin', '2026-03-04 04:00:00+00', 'patient'),
('03e6e676-cf9e-4c84-0143-b04c795599a5', 'veeva://aus-qms/safety_intake__c', 'safety_intake__c', 'veeva_object', 'VeevaVault-QMS-AUS', 'Austin', '2026-03-05 04:00:00+00', 'patient'),
('2e2e2d2c-7314-38b9-a1b3-56abfb8a2e20', 'https://austinpharma.sharepoint.com/sites/QA-Investigations/Shared Documents/complaint_followups_2026.xlsx', 'complaint_followups_2026.xlsx', 'sharepoint_file', 'SharePoint-AUS', 'Austin', '2026-09-08 04:00:00+00', 'patient'),
('4c5b96b9-10e4-c724-4884-ed726b504bc6', 'https://austinpharma-my.sharepoint.com/personal/lcarranza/Documents/payroll_export_aug.xlsx', 'payroll_export_aug.xlsx', 'onedrive_file', 'OneDrive-AUS', 'Austin', '2026-09-02 04:00:00+00', 'employee'),
('1bb2fc2c-d530-d53b-61df-85016b0d5a3c', 'hive://cdh-aus-7x-00142/mfg_curated.operator_badge_events', 'operator_badge_events', 'hive_table', 'Hive-CDP-AUS', 'Austin', '2026-07-21 04:00:00+00', 'employee')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS purview_dlp.asset_classification (
  asset_guid          uuid NOT NULL,
  classification_name varchar(120) NOT NULL,
  first_detected_at   timestamptz NOT NULL,
  match_count         integer NOT NULL,
  CONSTRAINT asset_classification_pk PRIMARY KEY (asset_guid, classification_name)
);
COMMENT ON TABLE purview_dlp.asset_classification IS 'Sensitive information type classifications found by scans.';

INSERT INTO purview_dlp.asset_classification (asset_guid, classification_name, first_detected_at, match_count) VALUES
('4972f3a6-1ca8-20de-f3e9-2b2f44559b5f', 'U.S. Social Security Number (SSN)', '2026-02-14 04:10:00+00', 35),
('4972f3a6-1ca8-20de-f3e9-2b2f44559b5f', 'All Full Names', '2026-02-14 04:11:00+00', 714),
('4972f3a6-1ca8-20de-f3e9-2b2f44559b5f', 'U.S. Bank Account Number', '2026-02-14 04:12:00+00', 2749),
('2498ddfa-ecc9-0068-dde4-f099eedb4f69', 'U.S. Bank Account Number', '2026-02-15 04:10:00+00', 2718),
('2498ddfa-ecc9-0068-dde4-f099eedb4f69', 'ABA Routing Number', '2026-02-15 04:11:00+00', 2977),
('d377f24c-7614-8eb8-37e9-42fca01c7e0c', 'All Full Names', '2026-02-16 04:10:00+00', 2098),
('d377f24c-7614-8eb8-37e9-42fca01c7e0c', 'U.S. National Provider Identifier (NPI)', '2026-02-16 04:11:00+00', 2494),
('461e306c-b1f2-5f6e-11f4-629d82796c51', 'Patient Enrolment ID (custom)', '2026-02-16 04:10:00+00', 2538),
('02ac1c28-c8a1-c3e9-10ec-626ef0083bc4', 'All Full Names', '2026-03-03 04:10:00+00', 353),
('02ac1c28-c8a1-c3e9-10ec-626ef0083bc4', 'All Medical Terms And Conditions', '2026-03-03 04:11:00+00', 2806),
('17aa2c10-b58f-4ba8-227b-c6b82c93fa63', 'Patient Pseudonym (custom)', '2026-03-04 04:10:00+00', 1511),
('03e6e676-cf9e-4c84-0143-b04c795599a5', 'All Medical Terms And Conditions', '2026-03-05 04:10:00+00', 2055),
('03e6e676-cf9e-4c84-0143-b04c795599a5', 'Patient Pseudonym (custom)', '2026-03-05 04:11:00+00', 1102),
('2e2e2d2c-7314-38b9-a1b3-56abfb8a2e20', 'All Full Names', '2026-09-08 04:10:00+00', 252),
('2e2e2d2c-7314-38b9-a1b3-56abfb8a2e20', 'U.S. Phone Number', '2026-09-08 04:11:00+00', 487),
('2e2e2d2c-7314-38b9-a1b3-56abfb8a2e20', 'All Medical Terms And Conditions', '2026-09-08 04:12:00+00', 2015),
('4c5b96b9-10e4-c724-4884-ed726b504bc6', 'U.S. Social Security Number (SSN)', '2026-09-02 04:10:00+00', 2834),
('4c5b96b9-10e4-c724-4884-ed726b504bc6', 'All Full Names', '2026-09-02 04:11:00+00', 46),
('1bb2fc2c-d530-d53b-61df-85016b0d5a3c', 'All Full Names', '2026-07-21 04:10:00+00', 1954),
('1bb2fc2c-d530-d53b-61df-85016b0d5a3c', 'Badge ID (custom)', '2026-07-21 04:11:00+00', 1435)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS purview_dlp.asset_managed_attribute (
  asset_guid      uuid NOT NULL,
  attribute_group varchar(60) NOT NULL,
  attribute_name  varchar(60) NOT NULL,
  attribute_value varchar(200) NOT NULL,
  CONSTRAINT asset_managed_attribute_pk PRIMARY KEY (asset_guid, attribute_group, attribute_name)
);
COMMENT ON TABLE purview_dlp.asset_managed_attribute IS 'Managed attributes; Privacy.ProcessingActivityId links an asset to the record of processing.';

INSERT INTO purview_dlp.asset_managed_attribute (asset_guid, attribute_group, attribute_name, attribute_value) VALUES
('4972f3a6-1ca8-20de-f3e9-2b2f44559b5f', 'Privacy', 'ProcessingActivityId', 'ROPA-AUS-HR-001'),
('2498ddfa-ecc9-0068-dde4-f099eedb4f69', 'Privacy', 'ProcessingActivityId', 'ROPA-AUS-FIN-002'),
('d377f24c-7614-8eb8-37e9-42fca01c7e0c', 'Privacy', 'ProcessingActivityId', 'ROPA-AUS-CRM-003'),
('461e306c-b1f2-5f6e-11f4-629d82796c51', 'Privacy', 'ProcessingActivityId', 'ROPA-AUS-PTX-001'),
('02ac1c28-c8a1-c3e9-10ec-626ef0083bc4', 'Privacy', 'ProcessingActivityId', 'ROPA-AUS-CSM-002'),
('17aa2c10-b58f-4ba8-227b-c6b82c93fa63', 'Privacy', 'ProcessingActivityId', 'ROPA-AUS-PTX-001'),
('03e6e676-cf9e-4c84-0143-b04c795599a5', 'Privacy', 'ProcessingActivityId', 'ROPA-AUS-PV-001')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS purview_dlp.health_action (
  action_id                  varchar(20) NOT NULL,
  finding_type               varchar(60) NOT NULL,
  target_asset_guid          uuid,
  target_processing_activity varchar(40),
  description                text NOT NULL,
  state                      varchar(40) NOT NULL,
  created_at                 timestamptz NOT NULL,
  CONSTRAINT health_action_pk PRIMARY KEY (action_id)
);
COMMENT ON TABLE purview_dlp.health_action IS 'Unified Catalog health actions raised by the privacy discrepancy rules.';

INSERT INTO purview_dlp.health_action (action_id, finding_type, target_asset_guid, target_processing_activity, description, state, created_at) VALUES
('HA-26-0031', 'PersonalDataNotRegistered', '2e2e2d2c-7314-38b9-a1b3-56abfb8a2e20', NULL, 'Patient names, phone numbers and health details in a QA SharePoint spreadsheet; no processing activity covers it', 'Active', '2026-09-08 06:00:00+00'),
('HA-26-0027', 'PersonalDataNotRegistered', '4c5b96b9-10e4-c724-4884-ed726b504bc6', NULL, 'Payroll export with SSNs in a personal OneDrive; file deleted by owner after notification', 'Resolved.HoldingRemoved', '2026-09-02 06:00:00+00'),
('HA-26-0019', 'PersonalDataNotRegistered', '1bb2fc2c-d530-d53b-61df-85016b0d5a3c', NULL, 'Operator badge events with names landed in the data lake; no processing activity registered', 'Active', '2026-07-21 06:00:00+00'),
('HA-26-0012', 'RegisteredActivityNoAsset', NULL, 'ROPA-AUS-MKT-004', 'HCP marketing consent (Salesforce Marketing Cloud) is registered but no holding was found: source not scanned', 'Active', '2026-05-18 06:00:00+00'),
('HA-26-0015', 'SubjectCategoryMismatch', '02ac1c28-c8a1-c3e9-10ec-626ef0083bc4', 'ROPA-AUS-CSM-002', 'Registered for customer contact data only, but case descriptions contain patient health information', 'Resolved.RegisterCorrected', '2026-06-02 06:00:00+00')
ON CONFLICT DO NOTHING;

-- Subscription inbound: tables and columns written by the coco_subscriptions_austin_systems DAG from the
-- digital products this system subscribes to (see coco-subscription-loads/austin_systems/purview_dlp).
-- No extract reads them.

CREATE TABLE IF NOT EXISTS purview_dlp.external_catalog_asset (
  asset_id              varchar(40) NOT NULL,
  asset_name            varchar(120) NOT NULL,
  asset_type            varchar(60) NOT NULL,
  system_qualified_name varchar(60),
  owner_ref             varchar(40),
  personal_data         boolean NOT NULL,
  confidentiality       varchar(20),
  CONSTRAINT external_catalog_asset_pk PRIMARY KEY (asset_id)
);
COMMENT ON TABLE purview_dlp.external_catalog_asset IS 'Assets catalogued in the open metadata catalogue for Austin systems, compared with scan results by the discrepancy rules.  From Open Metadata Catalogue Holdings.';

GRANT USAGE ON SCHEMA purview_dlp TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA purview_dlp TO egeria_user, airflow_user;
