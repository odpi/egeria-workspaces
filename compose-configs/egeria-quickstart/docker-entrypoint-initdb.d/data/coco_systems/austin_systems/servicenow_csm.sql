-- system-qualified-name: SoftwareServer::AUS-SYS-018::SN-CSS-AU-20220601
-- ServiceNow Customer Service Management - Austin.  ServiceNow CSM for Austin post-sale support: product complaint
-- cases with their safety assessment, and adverse event cases opened from complaints or direct calls.  Its tables feed
-- Product Complaints and Consolidated Safety Reports (reports first received by customer service).
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS servicenow_csm;
COMMENT ON SCHEMA servicenow_csm IS 'ServiceNow CSM (Austin instance): sn_customerservice_case and sys_user as landed by the table API export.';

CREATE TABLE IF NOT EXISTS servicenow_csm.sys_user (
  sys_id     char(32) NOT NULL,
  user_name  varchar(40) NOT NULL,
  first_name varchar(40),
  last_name  varchar(40),
  email      varchar(100),
  active     boolean NOT NULL,
  CONSTRAINT sys_user_pk PRIMARY KEY (sys_id)
);
COMMENT ON TABLE servicenow_csm.sys_user IS 'Users.';

INSERT INTO servicenow_csm.sys_user (sys_id, user_name, first_name, last_name, email, active) VALUES
('940a4d0bc2029e0e707ff56f65c17936', 'rcastillo', 'Robert', 'Castillo', 'rcastillo@austinpharma.com', TRUE),
('f880841c645b5f1b5cd9cc315ddd2ca4', 'imoreno', 'Isabel', 'Moreno', 'imoreno@austinpharma.com', TRUE)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS servicenow_csm.sn_customerservice_case (
  sys_id                   char(32) NOT NULL,
  number                   varchar(40) NOT NULL,
  opened_at                timestamptz NOT NULL,
  contact_type             varchar(40),
  category                 varchar(40) NOT NULL,
  u_reporter_type          varchar(40),
  u_product_code           varchar(20),
  u_lot_number             varchar(40),
  u_serial_number          varchar(40),
  short_description        varchar(160) NOT NULL,
  description              text,
  state                    integer NOT NULL,
  u_investigation_required boolean NOT NULL,
  u_safety_flag            boolean,
  u_safety_assessed_by     char(32),
  u_safety_assessed_at     timestamptz,
  parent                   char(32),
  u_safety_case_ref        varchar(40),
  opened_by                char(32) NOT NULL,
  sys_created_on           timestamptz NOT NULL,
  CONSTRAINT sn_customerservice_case_pk PRIMARY KEY (sys_id)
);
COMMENT ON TABLE servicenow_csm.sn_customerservice_case IS 'Customer service cases (state 1 New, 10 Open, 18 Awaiting info, 6 Resolved, 3 Closed); adverse event cases are children of the complaint they came from.';

INSERT INTO servicenow_csm.sn_customerservice_case (sys_id, number, opened_at, contact_type, category, u_reporter_type, u_product_code, u_lot_number, u_serial_number, short_description, description, state, u_investigation_required, u_safety_flag, u_safety_assessed_by, u_safety_assessed_at, parent, u_safety_case_ref, opened_by, sys_created_on) VALUES
('55576ca7b20b40007b046ab0a7ac2e16', 'CS0010431', '2026-08-26 15:42:00+00', 'phone', 'product_complaint', 'pharmacy', '3000', 'A26-3000-0141', '00372614300907.2734739610', 'Chipped tablets found in a sealed 90-count bottle', 'Chipped tablets found in a sealed 90-count bottle', 3, FALSE, FALSE, 'f880841c645b5f1b5cd9cc315ddd2ca4', '2026-08-27 10:05:00+00', NULL, NULL, '940a4d0bc2029e0e707ff56f65c17936', '2026-08-26 15:42:00+00'),
('4084ae8f77bf0acbcfbb1ad7ba2b846e', 'CS0010437', '2026-08-31 09:18:00+00', 'email', 'product_complaint', 'distributor', 'AU-4410', 'A26-4410-0052', NULL, 'Outer carton crushed in transit; two vials cracked on receipt', 'Outer carton crushed in transit; two vials cracked on receipt', 3, FALSE, FALSE, 'f880841c645b5f1b5cd9cc315ddd2ca4', '2026-08-31 14:30:00+00', NULL, NULL, '940a4d0bc2029e0e707ff56f65c17936', '2026-08-31 09:18:00+00'),
('34bf28ae6363aefe2097f7be77b6083d', 'CS0010442', '2026-09-04 19:55:00+00', 'phone', 'product_complaint', 'patient', '2050', 'A26-2050-0087', NULL, 'Tablets taste unusually bitter; patient reports stomach pain and dizziness after taking them', 'Tablets taste unusually bitter; patient reports stomach pain and dizziness after taking them', 10, TRUE, TRUE, 'f880841c645b5f1b5cd9cc315ddd2ca4', '2026-09-05 09:12:00+00', NULL, NULL, '940a4d0bc2029e0e707ff56f65c17936', '2026-09-04 19:55:00+00'),
('4c1fecd28d0d8ee15dfc848ea63b49a9', 'CS0010443', '2026-09-04 19:55:00+00', 'phone', 'adverse_event', 'patient', '2050', 'A26-2050-0087', NULL, 'Abdominal pain and dizziness after taking clopidogrel tablets from a bottle reported as tasting bitter', 'Abdominal pain and dizziness after taking clopidogrel tablets from a bottle reported as tasting bitter', 10, FALSE, NULL, NULL, NULL, '34bf28ae6363aefe2097f7be77b6083d', 'SC-26-0121', '940a4d0bc2029e0e707ff56f65c17936', '2026-09-04 19:55:00+00'),
('57cfacb06ef2bb26ee97530085bc56da', 'CS0010447', '2026-09-08 11:03:00+00', 'phone', 'adverse_event', 'patient', '2050', NULL, NULL, 'Recurrent nosebleeds since starting clopidogrel 75 mg three weeks ago', 'Recurrent nosebleeds since starting clopidogrel 75 mg three weeks ago', 10, FALSE, NULL, NULL, NULL, NULL, NULL, '940a4d0bc2029e0e707ff56f65c17936', '2026-09-08 11:03:00+00'),
('dc30f188bce52d250462e5499b9f9d70', 'CS0010450', '2026-09-26 08:47:00+00', 'web', 'product_complaint', 'hcp', 'AU-4630', 'A26-4630-0017', NULL, 'Visible particulate in a methotrexate vial before dilution; vial quarantined by pharmacy', 'Visible particulate in a methotrexate vial before dilution; vial quarantined by pharmacy', 10, TRUE, FALSE, 'f880841c645b5f1b5cd9cc315ddd2ca4', '2026-09-26 13:20:00+00', NULL, NULL, '940a4d0bc2029e0e707ff56f65c17936', '2026-09-26 08:47:00+00'),
('5d87e09cba1016c442e102d48c5cd4cd', 'CS0010455', '2026-09-18 16:10:00+00', 'email', 'product_complaint', 'pharmacy', '3000', NULL, NULL, 'Bottle label smudged; lot number and expiry unreadable', 'Bottle label smudged; lot number and expiry unreadable', 1, FALSE, FALSE, 'f880841c645b5f1b5cd9cc315ddd2ca4', '2026-09-19 08:40:00+00', NULL, NULL, '940a4d0bc2029e0e707ff56f65c17936', '2026-09-18 16:10:00+00'),
('845a8c56f6141781c9b7812214416fae', 'CS0010458', '2026-09-22 10:26:00+00', 'phone', 'product_complaint', 'hcp', 'AU-4410', 'A26-4410-0052', NULL, 'Solution looked slightly yellow before infusion; patient developed a widespread rash within an hour', 'Solution looked slightly yellow before infusion; patient developed a widespread rash within an hour', 10, TRUE, TRUE, 'f880841c645b5f1b5cd9cc315ddd2ca4', '2026-09-22 15:05:00+00', NULL, NULL, '940a4d0bc2029e0e707ff56f65c17936', '2026-09-22 10:26:00+00'),
('651f808335475358a4ae473f630f948a', 'CS0010459', '2026-09-22 10:26:00+00', 'phone', 'adverse_event', 'hcp', 'AU-4410', 'A26-4410-0052', NULL, 'Generalised urticarial rash within one hour of carboplatin infusion; treated with antihistamine, resolved', 'Generalised urticarial rash within one hour of carboplatin infusion; treated with antihistamine, resolved', 10, FALSE, NULL, NULL, NULL, '845a8c56f6141781c9b7812214416fae', 'SC-26-0127', '940a4d0bc2029e0e707ff56f65c17936', '2026-09-22 10:26:00+00'),
('be81afafb89ef83de1cd5711abc6e580', 'CS0010463', '2026-09-27 07:55:00+00', 'email', 'product_complaint', 'distributor', '9000', 'A26-9000-0019', NULL, 'Temperature logger alarm on receipt of a cisplatin shipment (peak 31 C for 40 minutes)', 'Temperature logger alarm on receipt of a cisplatin shipment (peak 31 C for 40 minutes)', 18, FALSE, FALSE, 'f880841c645b5f1b5cd9cc315ddd2ca4', '2026-09-28 09:30:00+00', NULL, NULL, '940a4d0bc2029e0e707ff56f65c17936', '2026-09-27 07:55:00+00')
ON CONFLICT DO NOTHING;

-- Subscription inbound: tables and columns written by the coco_subscriptions_austin_systems DAG from the
-- digital products this system subscribes to (see coco-subscription-loads/austin_systems/servicenow_csm).
-- No extract reads them.

CREATE TABLE IF NOT EXISTS servicenow_csm.u_imp_clinician_reaction (
  u_report_id      varchar(40) NOT NULL,
  u_reported_on    date NOT NULL,
  u_patient_ref    varchar(40) NOT NULL,
  u_clinician_npi  varchar(40) NOT NULL,
  u_product_code   varchar(20) NOT NULL,
  u_lot_number     varchar(40),
  u_description    text NOT NULL,
  u_severity       varchar(20),
  sys_import_state varchar(40) NOT NULL,
  CONSTRAINT u_imp_clinician_reaction_pk PRIMARY KEY (u_report_id)
);
COMMENT ON TABLE servicenow_csm.u_imp_clinician_reaction IS 'Import set table of clinician reaction reports received from other Austin systems; an agent opens the adverse event case.  From Clinician Adverse Reaction Reports.';

GRANT USAGE ON SCHEMA servicenow_csm TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA servicenow_csm TO egeria_user, airflow_user;
