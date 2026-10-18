-- system-qualified-name: System::MFCTRL9482
-- Austin Manufacturing Control System - Coco core.  Coco's homegrown control system recording the batches made at the Austin site (the same batches Austin's own MES executes); feeds Batch Execution Records and Electronic Batch Records.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS mfctrl9482;
COMMENT ON SCHEMA mfctrl9482 IS 'Austin Manufacturing Control System MFCTRL9482 (Coco core): Austin batches, operations, consumption, equipment, batch record sections and release.';

CREATE TABLE IF NOT EXISTS mfctrl9482.mfc_batch (
  batch_id varchar(20) NOT NULL,
  product_cd varchar(6) NOT NULL,
  planning_order varchar(20),
  start_utc timestamptz NOT NULL,
  end_utc timestamptz,
  qty integer NOT NULL,
  qty_uom varchar(4) NOT NULL,
  status_cd smallint NOT NULL,
  record_complete boolean NOT NULL,
  qa_status varchar(10) NOT NULL,
  CONSTRAINT mfc_batch_pk PRIMARY KEY (batch_id)
);
COMMENT ON TABLE mfctrl9482.mfc_batch IS 'Austin batches recorded on the Coco side. status_cd 10 planned, 20 in progress, 30 in QC testing, 40 released, 90 rejected; qty is the planned/produced quantity.';

CREATE TABLE IF NOT EXISTS mfctrl9482.mfc_operator (
  badge_no varchar(10) NOT NULL,
  worker_psn varchar(20) NOT NULL,
  role_desc varchar(40) NOT NULL,
  CONSTRAINT mfc_operator_pk PRIMARY KEY (badge_no)
);
COMMENT ON TABLE mfctrl9482.mfc_operator IS 'Austin site staff who sign in this system, with the pseudonym used outside the site.';

CREATE TABLE IF NOT EXISTS mfctrl9482.mfc_operation (
  batch_id varchar(20) NOT NULL,
  op_seq integer NOT NULL,
  op_code varchar(12) NOT NULL,
  start_utc timestamptz NOT NULL,
  end_utc timestamptz,
  badge_no varchar(10) NOT NULL,
  e_signature varchar(80),
  op_result varchar(2),
  CONSTRAINT mfc_operation_pk PRIMARY KEY (batch_id, op_seq)
);
COMMENT ON TABLE mfctrl9482.mfc_operation IS 'Operations performed (op_seq 10, 20...). op_result C complete, CD complete with deviation, AB aborted; empty while running.';

CREATE TABLE IF NOT EXISTS mfctrl9482.mfc_consumption (
  batch_id varchar(20) NOT NULL,
  op_seq integer NOT NULL,
  lot_no varchar(30) NOT NULL,
  item_cd varchar(10) NOT NULL,
  qty_consumed numeric(12,3) NOT NULL,
  uom varchar(6) NOT NULL,
  CONSTRAINT mfc_consumption_pk PRIMARY KEY (batch_id, op_seq, lot_no)
);
COMMENT ON TABLE mfctrl9482.mfc_consumption IS 'Material lots consumed per operation.';

CREATE TABLE IF NOT EXISTS mfctrl9482.mfc_equipment_use (
  batch_id varchar(20) NOT NULL,
  op_seq integer NOT NULL,
  equip_id varchar(16) NOT NULL,
  qual_status varchar(16) NOT NULL,
  cal_expiry date NOT NULL,
  CONSTRAINT mfc_equipment_use_pk PRIMARY KEY (batch_id, op_seq, equip_id)
);
COMMENT ON TABLE mfctrl9482.mfc_equipment_use IS 'Equipment used per operation with the qualification status read at use.';

CREATE TABLE IF NOT EXISTS mfctrl9482.mfc_record_section (
  batch_id varchar(20) NOT NULL,
  section_ref varchar(40) NOT NULL,
  section_type varchar(30) NOT NULL,
  source_system varchar(60) NOT NULL,
  received_utc timestamptz NOT NULL,
  CONSTRAINT mfc_record_section_pk PRIMARY KEY (batch_id, section_ref)
);
COMMENT ON TABLE mfctrl9482.mfc_record_section IS 'Batch record sections received, including those from the Austin site''s own MES, LIMS and QMS.';

CREATE TABLE IF NOT EXISTS mfctrl9482.mfc_release (
  batch_id varchar(20) NOT NULL,
  market varchar(3) NOT NULL,
  qty_released integer NOT NULL,
  cert_date date NOT NULL,
  released_by varchar(10) NOT NULL,
  CONSTRAINT mfc_release_pk PRIMARY KEY (batch_id, market)
);
COMMENT ON TABLE mfctrl9482.mfc_release IS 'Release per market (ISO alpha-3), released_by is the badge of the QA release manager.';

INSERT INTO mfctrl9482.mfc_batch (batch_id, product_cd, planning_order, start_utc, end_utc, qty, qty_uom, status_cd, record_complete, qa_status) VALUES
('A26-3000-0141', '3000', 'GMP-PO-26-0412', '2026-08-03 06:00+00', '2026-08-05 18:00+00', 120000, 'EA', 40, true, 'CERTIFIED'),
('A26-2050-0087', '2050', 'GMP-PO-26-0431', '2026-08-17 06:00+00', '2026-08-19 14:00+00', 90000, 'EA', 40, true, 'CERTIFIED'),
('A26-9000-0019', '9000', 'GMP-PO-26-0448', '2026-09-01 07:00+00', '2026-09-02 19:00+00', 2500, 'VIAL', 40, true, 'CERTIFIED'),
('A26-3000-0142', '3000', 'GMP-PO-26-0457', '2026-09-07 06:00+00', '2026-09-09 18:00+00', 120000, 'EA', 30, false, 'PENDING'),
('A26-2050-0088', '2050', 'GMP-PO-26-0466', '2026-09-28 06:00+00', NULL, 90000, 'EA', 20, false, 'PENDING')
ON CONFLICT DO NOTHING;

INSERT INTO mfctrl9482.mfc_operator (badge_no, worker_psn, role_desc) VALUES
('AUS-0417', 'AW-WQ5BBD', 'Operator'),
('AUS-0422', 'AW-TWJQVP', 'Operator'),
('AUS-0431', 'AW-4U49Z6', 'QA Release Manager'),
('AUS-0440', 'AW-WSVK4V', 'Warehouse Inspector')
ON CONFLICT DO NOTHING;

INSERT INTO mfctrl9482.mfc_operation (batch_id, op_seq, op_code, start_utc, end_utc, badge_no, e_signature, op_result) VALUES
('A26-3000-0141', 10, 'WEIGH', '2026-08-03 06:00+00', '2026-08-03 20:45+00', 'AUS-0417', 'AUS-0417:a105aad2cdae733c0a68', 'C'),
('A26-3000-0141', 20, 'GRANULATE', '2026-08-03 21:00+00', '2026-08-04 11:45+00', 'AUS-0422', 'AUS-0422:9280994a027d16a61a06', 'C'),
('A26-3000-0141', 30, 'COMPRESS', '2026-08-04 12:00+00', '2026-08-05 02:45+00', 'AUS-0417', 'AUS-0417:f3d0b9904536fcb35a8c', 'C'),
('A26-3000-0141', 40, 'PACKAGE', '2026-08-05 03:00+00', '2026-08-05 17:45+00', 'AUS-0422', 'AUS-0422:8fde4b2c27b11b752a16', 'C'),
('A26-2050-0087', 10, 'WEIGH', '2026-08-17 06:00+00', '2026-08-17 19:45+00', 'AUS-0417', 'AUS-0417:68aabd014154b0470f6a', 'C'),
('A26-2050-0087', 20, 'GRANULATE', '2026-08-17 20:00+00', '2026-08-18 09:45+00', 'AUS-0422', 'AUS-0422:fe28ba70a993a730ce8b', 'C'),
('A26-2050-0087', 30, 'COMPRESS', '2026-08-18 10:00+00', '2026-08-18 23:45+00', 'AUS-0417', 'AUS-0417:b611686ae11876628fe3', 'C'),
('A26-2050-0087', 40, 'PACKAGE', '2026-08-19 00:00+00', '2026-08-19 13:45+00', 'AUS-0422', 'AUS-0422:c5bc93ccbde7917d5839', 'C'),
('A26-9000-0019', 10, 'WEIGH', '2026-09-01 07:00+00', '2026-09-01 13:57+00', 'AUS-0417', 'AUS-0417:f426b8f961e44c873827', 'C'),
('A26-9000-0019', 20, 'COMPOUND', '2026-09-01 14:12+00', '2026-09-01 21:09+00', 'AUS-0422', 'AUS-0422:1b78dc1db398c0457995', 'C'),
('A26-9000-0019', 30, 'FILTER', '2026-09-01 21:24+00', '2026-09-02 04:21+00', 'AUS-0417', 'AUS-0417:425d978b2ebea7f6b344', 'C'),
('A26-9000-0019', 40, 'FILL', '2026-09-02 04:36+00', '2026-09-02 11:33+00', 'AUS-0422', 'AUS-0422:ea98154a1bc5fea7ff82', 'CD'),
('A26-9000-0019', 50, 'INSPECT', '2026-09-02 11:48+00', '2026-09-02 18:45+00', 'AUS-0417', 'AUS-0417:51d9d50a09a15261c4b2', 'C'),
('A26-3000-0142', 10, 'WEIGH', '2026-09-07 06:00+00', '2026-09-07 20:45+00', 'AUS-0417', 'AUS-0417:c4c91fee676d21c69939', 'C'),
('A26-3000-0142', 20, 'GRANULATE', '2026-09-07 21:00+00', '2026-09-08 11:45+00', 'AUS-0422', 'AUS-0422:c30ffb785d0b25e54ff0', 'C'),
('A26-3000-0142', 30, 'COMPRESS', '2026-09-08 12:00+00', '2026-09-09 02:45+00', 'AUS-0417', 'AUS-0417:86ea3749ddedd5dd4e39', 'C'),
('A26-3000-0142', 40, 'PACKAGE', '2026-09-09 03:00+00', '2026-09-09 17:45+00', 'AUS-0422', 'AUS-0422:7faa1f68279acd284a73', 'C'),
('A26-2050-0088', 10, 'WEIGH', '2026-09-28 06:00+00', '2026-09-28 20:45+00', 'AUS-0417', 'AUS-0417:974edb861b26ec2959e6', 'C'),
('A26-2050-0088', 20, 'GRANULATE', '2026-09-28 21:00+00', '2026-09-29 11:45+00', 'AUS-0422', 'AUS-0422:c0047ddb0a349b9d3f7a', 'C'),
('A26-2050-0088', 30, 'COMPRESS', '2026-09-29 12:00+00', '2026-09-30 02:45+00', 'AUS-0417', 'AUS-0417:1cc6155177efef08d5d7', 'C'),
('A26-2050-0088', 40, 'PACKAGE', '2026-09-30 03:00+00', NULL, 'AUS-0422', NULL, NULL)
ON CONFLICT DO NOTHING;

INSERT INTO mfctrl9482.mfc_consumption (batch_id, op_seq, lot_no, item_cd, qty_consumed, uom) VALUES
('A26-3000-0141', 10, 'TT-LOS-26-0341', 'RM3001', 12, 'KG'),
('A26-3000-0141', 10, 'WWE-MCC-2606-40', 'RM1002', 26, 'KG'),
('A26-2050-0087', 10, 'TT-CLP-26-0118', 'RM2051', 9, 'KG'),
('A26-2050-0087', 10, 'WWE-MCC-2608-21', 'RM1002', 20, 'KG'),
('A26-9000-0019', 10, 'BASE-CIS-2608', 'RM9001', 130, 'G'),
('A26-9000-0019', 20, 'NAC-WFI-2608', 'RM9002', 130, 'L'),
('A26-9000-0019', 40, 'GML-VIAL-2607', 'PK0021', 25, 'CASE'),
('A26-3000-0142', 10, 'TT-LOS-26-0402', 'RM3001', 12, 'KG'),
('A26-3000-0142', 10, 'WWE-MCC-2608-21', 'RM1002', 26, 'KG'),
('A26-2050-0088', 10, 'TT-CLP-26-0166', 'RM2051', 9, 'KG'),
('A26-2050-0088', 10, 'WWE-MCC-2608-21', 'RM1002', 20, 'KG')
ON CONFLICT DO NOTHING;

INSERT INTO mfctrl9482.mfc_equipment_use (batch_id, op_seq, equip_id, qual_status, cal_expiry) VALUES
('A26-3000-0141', 10, 'AUS-BAL-10', 'QUALIFIED', '2027-04-30'),
('A26-3000-0141', 20, 'AUS-GRN-11', 'QUALIFIED', '2027-04-30'),
('A26-3000-0141', 30, 'AUS-TP-12', 'QUALIFIED', '2027-04-30'),
('A26-3000-0141', 40, 'AUS-PKG-13', 'QUALIFIED', '2027-04-30'),
('A26-2050-0087', 10, 'AUS-BAL-10', 'QUALIFIED', '2027-04-30'),
('A26-2050-0087', 20, 'AUS-GRN-11', 'QUALIFIED', '2027-04-30'),
('A26-2050-0087', 30, 'AUS-TP-12', 'QUALIFIED', '2027-04-30'),
('A26-2050-0087', 40, 'AUS-PKG-13', 'QUALIFIED', '2027-04-30'),
('A26-9000-0019', 10, 'AUS-BAL-10', 'QUALIFIED', '2027-04-30'),
('A26-9000-0019', 20, 'AUS-TNK-20', 'QUALIFIED', '2027-04-30'),
('A26-9000-0019', 30, 'AUS-FLT-21', 'QUALIFIED', '2027-04-30'),
('A26-9000-0019', 40, 'AUS-FIL-22', 'QUALIFIED', '2027-04-30'),
('A26-9000-0019', 50, 'AUS-VIS-23', 'QUALIFIED', '2027-04-30'),
('A26-3000-0142', 10, 'AUS-BAL-10', 'QUALIFIED', '2027-04-30'),
('A26-3000-0142', 20, 'AUS-GRN-11', 'QUALIFIED', '2027-04-30'),
('A26-3000-0142', 30, 'AUS-TP-12', 'QUALIFIED', '2027-04-30'),
('A26-3000-0142', 40, 'AUS-PKG-13', 'QUALIFIED', '2027-04-30'),
('A26-2050-0088', 10, 'AUS-BAL-10', 'QUALIFIED', '2027-04-30'),
('A26-2050-0088', 20, 'AUS-GRN-11', 'QUALIFIED', '2027-04-30'),
('A26-2050-0088', 30, 'AUS-TP-12', 'QUALIFIED', '2027-04-30'),
('A26-2050-0088', 40, 'AUS-PKG-13', 'QUALIFIED', '2027-04-30')
ON CONFLICT DO NOTHING;

INSERT INTO mfctrl9482.mfc_record_section (batch_id, section_ref, section_type, source_system, received_utc) VALUES
('A26-3000-0141', 'A26-3000-0141-EXEC', 'EXECUTION', 'MFCTRL9482', '2026-08-05 18:00+00'),
('A26-3000-0141', 'A26-3000-0141-PARAM', 'PROCESS_PARAMETERS', 'MFCTRL9482', '2026-08-06 00:00+00'),
('A26-3000-0141', 'A26-3000-0141-LAB', 'LABORATORY_RESULTS', 'LabWare LIMS (Austin)', '2026-08-09 18:00+00'),
('A26-3000-0141', 'A26-3000-0141-SIGN', 'SIGNATURE_AUTHORITY', 'MFCTRL9482', '2026-08-14 08:00+00'),
('A26-2050-0087', 'A26-2050-0087-EXEC', 'EXECUTION', 'MFCTRL9482', '2026-08-19 14:00+00'),
('A26-2050-0087', 'A26-2050-0087-PARAM', 'PROCESS_PARAMETERS', 'MFCTRL9482', '2026-08-19 20:00+00'),
('A26-2050-0087', 'A26-2050-0087-LAB', 'LABORATORY_RESULTS', 'LabWare LIMS (Austin)', '2026-08-23 14:00+00'),
('A26-2050-0087', 'A26-2050-0087-SIGN', 'SIGNATURE_AUTHORITY', 'MFCTRL9482', '2026-08-27 08:00+00'),
('A26-9000-0019', 'A26-9000-0019-EXEC', 'EXECUTION', 'MFCTRL9482', '2026-09-02 19:00+00'),
('A26-9000-0019', 'A26-9000-0019-PARAM', 'PROCESS_PARAMETERS', 'MFCTRL9482', '2026-09-03 01:00+00'),
('A26-9000-0019', 'A26-9000-0019-LAB', 'LABORATORY_RESULTS', 'LabWare LIMS (Austin)', '2026-09-06 19:00+00'),
('A26-9000-0019', 'A26-9000-0019-DEV', 'DEVIATION_DISPOSITION', 'Veeva QMS (Austin)', '2026-09-07 19:00+00'),
('A26-9000-0019', 'A26-9000-0019-SIGN', 'SIGNATURE_AUTHORITY', 'MFCTRL9482', '2026-09-16 08:00+00'),
('A26-3000-0142', 'A26-3000-0142-EXEC', 'EXECUTION', 'MFCTRL9482', '2026-09-09 18:00+00'),
('A26-3000-0142', 'A26-3000-0142-PARAM', 'PROCESS_PARAMETERS', 'MFCTRL9482', '2026-09-10 00:00+00'),
('A26-3000-0142', 'A26-3000-0142-LAB', 'LABORATORY_RESULTS', 'LabWare LIMS (Austin)', '2026-09-13 18:00+00'),
('A26-2050-0088', 'A26-2050-0088-EXEC', 'EXECUTION', 'MFCTRL9482', '2026-09-30 08:00+00')
ON CONFLICT DO NOTHING;

INSERT INTO mfctrl9482.mfc_release (batch_id, market, qty_released, cert_date, released_by) VALUES
('A26-3000-0141', 'USA', 90000, '2026-08-14', 'AUS-0431'),
('A26-3000-0141', 'CAN', 30000, '2026-08-14', 'AUS-0431'),
('A26-2050-0087', 'USA', 70000, '2026-08-27', 'AUS-0431'),
('A26-2050-0087', 'GBR', 20000, '2026-08-27', 'AUS-0431'),
('A26-9000-0019', 'USA', 2500, '2026-09-16', 'AUS-0431')
ON CONFLICT DO NOTHING;


-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS mfctrl9482.mfc_mes_operation (
  batch_id varchar(20) NOT NULL,
  step_no integer NOT NULL,
  op_code varchar(40) NOT NULL,
  start_utc timestamptz NOT NULL,
  end_utc timestamptz NOT NULL,
  mes_signer varchar(40) NOT NULL,
  mes_signature varchar(200) NOT NULL,
  step_status varchar(100) NOT NULL,
  CONSTRAINT mfc_mes_operation_pk PRIMARY KEY (batch_id, step_no)
);
COMMENT ON TABLE mfctrl9482.mfc_mes_operation IS 'Execution steps of the shared Austin batches as recorded by the Austin site''s own MES (Batch Execution Records), kept beside mfc_operation for the batch record review; mes_signer is the MES user pseudonym.';

CREATE TABLE IF NOT EXISTS mfctrl9482.mfc_mes_consumption (
  batch_id varchar(20) NOT NULL,
  step_no integer NOT NULL,
  lot_no varchar(40) NOT NULL,
  item_cd varchar(20) NOT NULL,
  qty_consumed double precision NOT NULL,
  uom varchar(20) NOT NULL,
  CONSTRAINT mfc_mes_consumption_pk PRIMARY KEY (batch_id, step_no, lot_no)
);
COMMENT ON TABLE mfctrl9482.mfc_mes_consumption IS 'Material lots the Austin MES recorded as consumed in the shared batches (including Austin-sourced lots MFCTRL9482 does not issue).';

CREATE TABLE IF NOT EXISTS mfctrl9482.mfc_mes_equipment_use (
  batch_id varchar(20) NOT NULL,
  step_no integer NOT NULL,
  equip_id varchar(40) NOT NULL,
  qual_status varchar(20) NOT NULL,
  cal_expiry date NOT NULL,
  CONSTRAINT mfc_mes_equipment_use_pk PRIMARY KEY (batch_id, step_no, equip_id)
);
COMMENT ON TABLE mfctrl9482.mfc_mes_equipment_use IS 'Equipment the Austin MES recorded for the shared batches, under the site''s own equipment numbers (US10-).';

CREATE TABLE IF NOT EXISTS mfctrl9482.mfc_deviation (
  deviation_id varchar(40) NOT NULL,
  batch_id varchar(20),
  product_cd varchar(20),
  raised_utc timestamptz NOT NULL,
  source_type varchar(100) NOT NULL,
  description text NOT NULL,
  severity varchar(20) NOT NULL,
  dev_status varchar(20) NOT NULL,
  investigator varchar(40),
  investigated_on date,
  root_cause text,
  impact text,
  disposition varchar(40),
  CONSTRAINT mfc_deviation_pk PRIMARY KEY (deviation_id)
);
COMMENT ON TABLE mfctrl9482.mfc_deviation IS 'Deviations raised in the Austin site''s QMS against the shared batches (Deviations And CAPAs), with the investigation disposition the release depends on.';

CREATE TABLE IF NOT EXISTS mfctrl9482.mfc_equipment_qual (
  equip_id varchar(40) NOT NULL,
  equip_name varchar(120) NOT NULL,
  equip_type varchar(60) NOT NULL,
  site varchar(20) NOT NULL,
  equip_status varchar(20) NOT NULL,
  qual_status varchar(20),
  qualified_on date,
  requal_due date,
  calibrated_on date,
  cal_expiry date,
  CONSTRAINT mfc_equipment_qual_pk PRIMARY KEY (equip_id)
);
COMMENT ON TABLE mfctrl9482.mfc_equipment_qual IS 'Qualification and calibration status of the Austin site''s equipment (Equipment Qualification Status), under the site''s own equipment numbers.';

CREATE TABLE IF NOT EXISTS mfctrl9482.mfc_issue (
  movement_id varchar(40) NOT NULL,
  batch_id varchar(20) NOT NULL,
  item_cd varchar(20) NOT NULL,
  lot_no varchar(40) NOT NULL,
  qty_issued integer NOT NULL,
  lot_status varchar(20) NOT NULL,
  CONSTRAINT mfc_issue_pk PRIMARY KEY (movement_id)
);
COMMENT ON TABLE mfctrl9482.mfc_issue IS 'Material issued to the shared batches (Goods Inventory Stock), from Coco''s Austin Inventory and from the Austin site''s own stores.';

CREATE TABLE IF NOT EXISTS mfctrl9482.mfc_lab_sample (
  sample_id varchar(40) NOT NULL,
  sample_type varchar(20) NOT NULL,
  batch_id varchar(20) NOT NULL,
  collected_utc timestamptz NOT NULL,
  sample_status varchar(20) NOT NULL,
  CONSTRAINT mfc_lab_sample_pk PRIMARY KEY (sample_id)
);
COMMENT ON TABLE mfctrl9482.mfc_lab_sample IS 'LIMS samples of the shared batches (Laboratory Test Results).';

CREATE TABLE IF NOT EXISTS mfctrl9482.mfc_lab_result (
  result_id varchar(40) NOT NULL,
  sample_id varchar(40) NOT NULL,
  test_code varchar(40) NOT NULL,
  result_value varchar(60) NOT NULL,
  result_unit varchar(20),
  spec_min varchar(60),
  spec_max varchar(60),
  conforms boolean NOT NULL,
  completed_utc timestamptz NOT NULL,
  analyst varchar(40) NOT NULL,
  CONSTRAINT mfc_lab_result_pk PRIMARY KEY (result_id)
);
COMMENT ON TABLE mfctrl9482.mfc_lab_result IS 'LIMS test results of the samples in mfc_lab_sample.';

CREATE TABLE IF NOT EXISTS mfctrl9482.mfc_lab_coa (
  coa_id varchar(40) NOT NULL,
  batch_id varchar(20) NOT NULL,
  coa_date date NOT NULL,
  conforms boolean NOT NULL,
  approver varchar(40) NOT NULL,
  CONSTRAINT mfc_lab_coa_pk PRIMARY KEY (coa_id)
);
COMMENT ON TABLE mfctrl9482.mfc_lab_coa IS 'Certificates of analysis the Austin laboratory issued for the shared batches.';

CREATE TABLE IF NOT EXISTS mfctrl9482.mfc_param_reading (
  equip_id varchar(40) NOT NULL,
  param_code varchar(40) NOT NULL,
  reading_utc timestamptz NOT NULL,
  batch_id varchar(20) NOT NULL,
  reading double precision NOT NULL,
  unit varchar(20) NOT NULL,
  low_limit double precision,
  high_limit double precision,
  CONSTRAINT mfc_param_reading_pk PRIMARY KEY (equip_id, param_code, reading_utc)
);
COMMENT ON TABLE mfctrl9482.mfc_param_reading IS 'Process parameter readings of the shared batches from the Austin site historian (Process Parameter Time Series).';

CREATE TABLE IF NOT EXISTS mfctrl9482.mfc_excursion (
  excursion_id varchar(40) NOT NULL,
  shipment_id varchar(40) NOT NULL,
  product_cd varchar(20) NOT NULL,
  batch_id varchar(20) NOT NULL,
  assessor varchar(40) NOT NULL,
  assessed_utc timestamptz NOT NULL,
  stability_ref varchar(40) NOT NULL,
  disposition varchar(20) NOT NULL,
  notes text,
  CONSTRAINT mfc_excursion_pk PRIMARY KEY (excursion_id)
);
COMMENT ON TABLE mfctrl9482.mfc_excursion IS 'Temperature excursion assessments of shipments from the shared batches (Temperature Excursion Assessments).';

-- End of subscription tables.

GRANT USAGE ON SCHEMA mfctrl9482 TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA mfctrl9482 TO egeria_user, airflow_user;
