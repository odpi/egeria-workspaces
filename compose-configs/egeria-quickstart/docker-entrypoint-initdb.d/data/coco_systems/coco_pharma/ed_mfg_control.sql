-- system-qualified-name: System::ed-mfg-control
-- Edmonton Manufacturing Control System - Coco core.  Homegrown control system for the Edmonton factory (Norvasc and Toprol-XL), built separately from the Winchester and Austin systems; feeds Batch Execution Records and Electronic Batch Records.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS ed_mfg_control;
COMMENT ON SCHEMA ed_mfg_control IS 'Edmonton Manufacturing Control System (Coco core): production lots, operations, consumption, equipment, EBR sections and market release.';

CREATE TABLE IF NOT EXISTS ed_mfg_control.prod_lot (
  lot_id varchar(20) NOT NULL,
  item_no integer NOT NULL,
  start_dt varchar(16) NOT NULL,
  finish_dt varchar(16),
  yield_qty numeric(12,0),
  lot_status varchar(20) NOT NULL,
  ebr_complete smallint NOT NULL,
  qa_disposition varchar(12) NOT NULL,
  CONSTRAINT prod_lot_pk PRIMARY KEY (lot_id)
);
COMMENT ON TABLE ed_mfg_control.prod_lot IS 'Production lots (Coco batches). Dates are text in Edmonton local time (YYYY-MM-DD HH24:MI); lot_status is free text; ebr_complete 1/0; qa_disposition Pending/Approved/Rejected.';

CREATE TABLE IF NOT EXISTS ed_mfg_control.operator (
  emp_no varchar(10) NOT NULL,
  worker_ref varchar(20) NOT NULL,
  display_name varchar(80) NOT NULL,
  active char(1) NOT NULL,
  CONSTRAINT operator_pk PRIMARY KEY (emp_no)
);
COMMENT ON TABLE ed_mfg_control.operator IS 'Operators allowed to sign, with the HRIM worker pseudonym loaded from the HR feed.';

CREATE TABLE IF NOT EXISTS ed_mfg_control.op_log (
  lot_id varchar(20) NOT NULL,
  seq integer NOT NULL,
  op_code varchar(20) NOT NULL,
  started varchar(16) NOT NULL,
  finished varchar(16),
  operator varchar(10) NOT NULL,
  esig_hash varchar(60),
  result varchar(3),
  CONSTRAINT op_log_pk PRIMARY KEY (lot_id, seq)
);
COMMENT ON TABLE ed_mfg_control.op_log IS 'Operation log. seq in steps of 10; started/finished are local text; result OK, DEV (deviation) or ABT (aborted), empty while running.';

CREATE TABLE IF NOT EXISTS ed_mfg_control.consumption (
  lot_id varchar(20) NOT NULL,
  seq integer NOT NULL,
  component_lot varchar(30) NOT NULL,
  item_no varchar(10) NOT NULL,
  qty_used numeric(12,3) NOT NULL,
  uom varchar(6) NOT NULL,
  CONSTRAINT consumption_pk PRIMARY KEY (lot_id, seq, component_lot)
);
COMMENT ON TABLE ed_mfg_control.consumption IS 'Component lots consumed per operation.';

CREATE TABLE IF NOT EXISTS ed_mfg_control.equip_log (
  lot_id varchar(20) NOT NULL,
  seq integer NOT NULL,
  asset_tag varchar(16) NOT NULL,
  qual_state varchar(12) NOT NULL,
  cal_exp varchar(10) NOT NULL,
  CONSTRAINT equip_log_pk PRIMARY KEY (lot_id, seq, asset_tag)
);
COMMENT ON TABLE ed_mfg_control.equip_log IS 'Equipment used per operation; cal_exp is text DD/MM/YYYY.';

CREATE TABLE IF NOT EXISTS ed_mfg_control.ebr_section (
  lot_id varchar(20) NOT NULL,
  section_ref varchar(40) NOT NULL,
  section_kind varchar(40) NOT NULL,
  source_system varchar(60) NOT NULL,
  received varchar(16) NOT NULL,
  CONSTRAINT ebr_section_pk PRIMARY KEY (lot_id, section_ref)
);
COMMENT ON TABLE ed_mfg_control.ebr_section IS 'Electronic batch record sections received (received is local text).';

CREATE TABLE IF NOT EXISTS ed_mfg_control.market_release (
  lot_id varchar(20) NOT NULL,
  country varchar(3) NOT NULL,
  qty_rel integer NOT NULL,
  certified_on date NOT NULL,
  qp varchar(10) NOT NULL,
  CONSTRAINT market_release_pk PRIMARY KEY (lot_id, country)
);
COMMENT ON TABLE ed_mfg_control.market_release IS 'Release per country; qp is the employee number of the Qualified Person.';

INSERT INTO ed_mfg_control.prod_lot (lot_id, item_no, start_dt, finish_dt, yield_qty, lot_status, ebr_complete, qa_disposition) VALUES
('E26-2000-0044', 2000, '2026-07-20 07:00', '2026-07-21 19:00', 180000, 'RELEASED', 1, 'Approved'),
('E26-4000-0027', 4000, '2026-08-04 07:00', '2026-08-05 21:00', 120000, 'RELEASED', 1, 'Approved'),
('E26-2010-0019', 2010, '2026-08-18 07:00', '2026-08-19 17:00', 180000, 'RELEASED', 1, 'Approved'),
('E26-4010-0011', 4010, '2026-09-01 07:00', '2026-09-02 19:00', 120000, 'RELEASED', 1, 'Approved'),
('E26-2000-0045', 2000, '2026-09-21 07:00', '2026-09-22 20:00', 180000, 'QC hold', 0, 'Pending')
ON CONFLICT DO NOTHING;

INSERT INTO ed_mfg_control.operator (emp_no, worker_ref, display_name, active) VALUES
('810052', 'CW-HFD9LG', 'Ben Kowalski', 'Y'),
('810067', 'CW-JS5LWU', 'Priya Singh', 'Y'),
('810045', 'CW-G32FNJ', 'Chantal Roy', 'Y')
ON CONFLICT DO NOTHING;

INSERT INTO ed_mfg_control.op_log (lot_id, seq, op_code, started, finished, operator, esig_hash, result) VALUES
('E26-2000-0044', 10, 'dispense', '2026-07-20 07:00', '2026-07-20 15:45', '810052', 'signed:810052:d51c15d167a43d004c4a', 'OK'),
('E26-2000-0044', 20, 'granulate', '2026-07-20 16:00', '2026-07-21 00:45', '810067', 'signed:810067:6052f401722bb13cccc0', 'OK'),
('E26-2000-0044', 30, 'compress', '2026-07-21 01:00', '2026-07-21 09:45', '810052', 'signed:810052:fd9e4483df849a5416c4', 'OK'),
('E26-2000-0044', 40, 'bottle', '2026-07-21 10:00', '2026-07-21 18:45', '810067', 'signed:810067:87c8cdd125214a72c0f4', 'OK'),
('E26-4000-0027', 10, 'dispense', '2026-08-04 07:00', '2026-08-04 16:15', '810052', 'signed:810052:b909c1e2cff84710da4e', 'OK'),
('E26-4000-0027', 20, 'granulate', '2026-08-04 16:30', '2026-08-05 01:45', '810067', 'signed:810067:cb99b4249b8bb3995fd8', 'OK'),
('E26-4000-0027', 30, 'compress', '2026-08-05 02:00', '2026-08-05 11:15', '810052', 'signed:810052:676081067643e2baf9be', 'OK'),
('E26-4000-0027', 40, 'bottle', '2026-08-05 11:30', '2026-08-05 20:45', '810067', 'signed:810067:ae3752bb74e8afa25020', 'OK'),
('E26-2010-0019', 10, 'dispense', '2026-08-18 07:00', '2026-08-18 15:15', '810052', 'signed:810052:8c82c31a9598ca6c47be', 'OK'),
('E26-2010-0019', 20, 'granulate', '2026-08-18 15:30', '2026-08-18 23:45', '810067', 'signed:810067:39a2b60c00a0f8b4edef', 'OK'),
('E26-2010-0019', 30, 'compress', '2026-08-19 00:00', '2026-08-19 08:15', '810052', 'signed:810052:e4a0a4e4b2f01ffa44e8', 'OK'),
('E26-2010-0019', 40, 'bottle', '2026-08-19 08:30', '2026-08-19 16:45', '810067', 'signed:810067:9d2cbef9d97dd877eed6', 'OK'),
('E26-4010-0011', 10, 'dispense', '2026-09-01 07:00', '2026-09-01 15:45', '810052', 'signed:810052:4c0e0eae9122a9d770d5', 'OK'),
('E26-4010-0011', 20, 'granulate', '2026-09-01 16:00', '2026-09-02 00:45', '810067', 'signed:810067:89eff0293a60b6c2c4f5', 'OK'),
('E26-4010-0011', 30, 'compress', '2026-09-02 01:00', '2026-09-02 09:45', '810052', 'signed:810052:522f4484fb5f7c093211', 'DEV'),
('E26-4010-0011', 40, 'bottle', '2026-09-02 10:00', '2026-09-02 18:45', '810067', 'signed:810067:844ab986232b47fad03e', 'OK'),
('E26-2000-0045', 10, 'dispense', '2026-09-21 07:00', '2026-09-21 16:00', '810052', 'signed:810052:2c054f4a5cbc9c9b8954', 'OK'),
('E26-2000-0045', 20, 'granulate', '2026-09-21 16:15', '2026-09-22 01:15', '810067', 'signed:810067:a45e6a6a9304782f4f4f', 'OK'),
('E26-2000-0045', 30, 'compress', '2026-09-22 01:30', '2026-09-22 10:30', '810052', 'signed:810052:ab4427d3a9657dbf834f', 'OK'),
('E26-2000-0045', 40, 'bottle', '2026-09-22 10:45', '2026-09-22 19:45', '810067', 'signed:810067:9269bf1e674d91fe0360', 'OK')
ON CONFLICT DO NOTHING;

INSERT INTO ed_mfg_control.consumption (lot_id, seq, component_lot, item_no, qty_used, uom) VALUES
('E26-2000-0044', 10, 'GG-AML-26-0192', 'RM2001', 3, 'kg'),
('E26-2000-0044', 10, 'WWE-MCC-2607-12', 'RM1002', 30, 'kg'),
('E26-2000-0044', 40, 'GML-BTL-2605', 'PK0020', 30, 'case'),
('E26-4000-0027', 10, 'GG-MET-26-0077', 'RM4001', 6, 'kg'),
('E26-4000-0027', 10, 'WWE-MCC-2607-12', 'RM1002', 24, 'kg'),
('E26-4000-0027', 40, 'GML-BTL-2605', 'PK0020', 20, 'case'),
('E26-2010-0019', 10, 'GG-AML-26-0192', 'RM2001', 2, 'kg'),
('E26-2010-0019', 10, 'WWE-MCC-2607-12', 'RM1002', 28, 'kg'),
('E26-2010-0019', 40, 'GML-BTL-2605', 'PK0020', 30, 'case'),
('E26-4010-0011', 10, 'GG-MET-26-0077', 'RM4001', 3, 'kg'),
('E26-4010-0011', 10, 'WWE-MCC-2607-12', 'RM1002', 22, 'kg'),
('E26-4010-0011', 40, 'GML-BTL-2608', 'PK0020', 20, 'case'),
('E26-2000-0045', 10, 'GG-AML-26-0251', 'RM2001', 3, 'kg'),
('E26-2000-0045', 10, 'WWE-MCC-2607-12', 'RM1002', 30, 'kg'),
('E26-2000-0045', 40, 'GML-BTL-2608', 'PK0020', 30, 'case')
ON CONFLICT DO NOTHING;

INSERT INTO ed_mfg_control.equip_log (lot_id, seq, asset_tag, qual_state, cal_exp) VALUES
('E26-2000-0044', 10, 'EDM-BAL-1', 'qualified', '28/02/2027'),
('E26-2000-0044', 20, 'EDM-MX-1', 'qualified', '28/02/2027'),
('E26-2000-0044', 30, 'EDM-TP-4', 'qualified', '31/08/2026'),
('E26-2000-0044', 40, 'EDM-PK-1', 'qualified', '28/02/2027'),
('E26-4000-0027', 10, 'EDM-BAL-1', 'qualified', '28/02/2027'),
('E26-4000-0027', 20, 'EDM-MX-1', 'qualified', '28/02/2027'),
('E26-4000-0027', 30, 'EDM-TP-4', 'qualified', '31/08/2026'),
('E26-4000-0027', 40, 'EDM-PK-1', 'qualified', '28/02/2027'),
('E26-2010-0019', 10, 'EDM-BAL-1', 'qualified', '28/02/2027'),
('E26-2010-0019', 20, 'EDM-MX-1', 'qualified', '28/02/2027'),
('E26-2010-0019', 30, 'EDM-TP-4', 'qualified', '31/08/2026'),
('E26-2010-0019', 40, 'EDM-PK-1', 'qualified', '28/02/2027'),
('E26-4010-0011', 10, 'EDM-BAL-1', 'qualified', '28/02/2027'),
('E26-4010-0011', 20, 'EDM-MX-1', 'qualified', '28/02/2027'),
('E26-4010-0011', 30, 'EDM-TP-4', 'overdue', '31/08/2026'),
('E26-4010-0011', 40, 'EDM-PK-1', 'qualified', '28/02/2027'),
('E26-2000-0045', 10, 'EDM-BAL-1', 'qualified', '28/02/2027'),
('E26-2000-0045', 20, 'EDM-MX-1', 'qualified', '28/02/2027'),
('E26-2000-0045', 30, 'EDM-TP-4', 'qualified', '10/03/2027'),
('E26-2000-0045', 40, 'EDM-PK-1', 'qualified', '28/02/2027')
ON CONFLICT DO NOTHING;

INSERT INTO ed_mfg_control.ebr_section (lot_id, section_ref, section_kind, source_system, received) VALUES
('E26-2000-0044', 'EBR-2000-0044-EXEC', 'Execution', 'ed-mfg-control', '2026-07-21 19:00'),
('E26-2000-0044', 'EBR-2000-0044-PARAM', 'Process Parameters', 'ed-mfg-control', '2026-07-22 01:00'),
('E26-2000-0044', 'EBR-2000-0044-LAB', 'Laboratory Results', 'Edmonton QC laboratory (paper)', '2026-07-25 19:00'),
('E26-2000-0044', 'EBR-2000-0044-SIGN', 'Signature Authority', 'ed-mfg-control', '2026-07-30 02:00'),
('E26-4000-0027', 'EBR-4000-0027-EXEC', 'Execution', 'ed-mfg-control', '2026-08-05 21:00'),
('E26-4000-0027', 'EBR-4000-0027-PARAM', 'Process Parameters', 'ed-mfg-control', '2026-08-06 03:00'),
('E26-4000-0027', 'EBR-4000-0027-LAB', 'Laboratory Results', 'Edmonton QC laboratory (paper)', '2026-08-09 21:00'),
('E26-4000-0027', 'EBR-4000-0027-SIGN', 'Signature Authority', 'ed-mfg-control', '2026-08-13 02:00'),
('E26-2010-0019', 'EBR-2010-0019-EXEC', 'Execution', 'ed-mfg-control', '2026-08-19 17:00'),
('E26-2010-0019', 'EBR-2010-0019-PARAM', 'Process Parameters', 'ed-mfg-control', '2026-08-19 23:00'),
('E26-2010-0019', 'EBR-2010-0019-LAB', 'Laboratory Results', 'Edmonton QC laboratory (paper)', '2026-08-23 17:00'),
('E26-2010-0019', 'EBR-2010-0019-SIGN', 'Signature Authority', 'ed-mfg-control', '2026-08-27 02:00'),
('E26-4010-0011', 'EBR-4010-0011-EXEC', 'Execution', 'ed-mfg-control', '2026-09-02 19:00'),
('E26-4010-0011', 'EBR-4010-0011-PARAM', 'Process Parameters', 'ed-mfg-control', '2026-09-03 01:00'),
('E26-4010-0011', 'EBR-4010-0011-LAB', 'Laboratory Results', 'Edmonton QC laboratory (paper)', '2026-09-06 19:00'),
('E26-4010-0011', 'EBR-4010-0011-DEV', 'Deviation Disposition', 'Coco QA deviation log', '2026-09-07 19:00'),
('E26-4010-0011', 'EBR-4010-0011-SIGN', 'Signature Authority', 'ed-mfg-control', '2026-09-11 02:00'),
('E26-2000-0045', 'EBR-2000-0045-EXEC', 'Execution', 'ed-mfg-control', '2026-09-22 20:00'),
('E26-2000-0045', 'EBR-2000-0045-PARAM', 'Process Parameters', 'ed-mfg-control', '2026-09-23 02:00'),
('E26-2000-0045', 'EBR-2000-0045-LAB', 'Laboratory Results', 'Edmonton QC laboratory (paper)', '2026-09-26 20:00')
ON CONFLICT DO NOTHING;

INSERT INTO ed_mfg_control.market_release (lot_id, country, qty_rel, certified_on, qp) VALUES
('E26-2000-0044', 'ca', 100000, '2026-07-30', '810045'),
('E26-2000-0044', 'us', 80000, '2026-07-30', '810045'),
('E26-4000-0027', 'ca', 70000, '2026-08-13', '810045'),
('E26-4000-0027', 'us', 50000, '2026-08-13', '810045'),
('E26-2010-0019', 'ca', 120000, '2026-08-27', '810045'),
('E26-2010-0019', 'gb', 60000, '2026-08-27', '810045'),
('E26-4010-0011', 'ca', 70000, '2026-09-11', '810045'),
('E26-4010-0011', 'us', 50000, '2026-09-11', '810045')
ON CONFLICT DO NOTHING;


-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS ed_mfg_control.lot_deviation (
  deviation_no varchar(40) NOT NULL,
  lot_id varchar(20),
  item_no varchar(20),
  raised varchar(16) NOT NULL,
  source_type varchar(100) NOT NULL,
  description text NOT NULL,
  severity varchar(20) NOT NULL,
  dev_status varchar(20) NOT NULL,
  investigator varchar(40),
  investigated_on date,
  root_cause text,
  impact text,
  disposition varchar(40),
  CONSTRAINT lot_deviation_pk PRIMARY KEY (deviation_no)
);
COMMENT ON TABLE ed_mfg_control.lot_deviation IS 'Deviations against Edmonton lots received from the QMS (Deviations And CAPAs) with the investigation disposition QA needs before approving the lot; raised is local text YYYY-MM-DD HH24:MI.';

CREATE TABLE IF NOT EXISTS ed_mfg_control.equipment_status (
  asset_tag varchar(40) NOT NULL,
  asset_name varchar(120),
  asset_type varchar(60),
  asset_status varchar(20),
  qual_state varchar(20),
  qualified_on date,
  requal_due date,
  calibrated_on date,
  cal_exp varchar(10),
  CONSTRAINT equipment_status_pk PRIMARY KEY (asset_tag)
);
COMMENT ON TABLE ed_mfg_control.equipment_status IS 'Qualification and calibration status of Edmonton equipment (Equipment Qualification Status); cal_exp is text DD/MM/YYYY as in equip_log.';

CREATE TABLE IF NOT EXISTS ed_mfg_control.component_issue (
  movement_no varchar(40) NOT NULL,
  lot_id varchar(20) NOT NULL,
  item_no varchar(20) NOT NULL,
  component_lot varchar(40) NOT NULL,
  qty_issued integer NOT NULL,
  quarantine_status varchar(20) NOT NULL,
  CONSTRAINT component_issue_pk PRIMARY KEY (movement_no)
);
COMMENT ON TABLE ed_mfg_control.component_issue IS 'Component lots issued from stores to Edmonton lots (Goods Inventory Stock), reconciled against consumption.';

CREATE TABLE IF NOT EXISTS ed_mfg_control.qc_sample (
  sample_no varchar(40) NOT NULL,
  sample_kind varchar(20) NOT NULL,
  lot_id varchar(20) NOT NULL,
  collected varchar(16) NOT NULL,
  sample_status varchar(20) NOT NULL,
  CONSTRAINT qc_sample_pk PRIMARY KEY (sample_no)
);
COMMENT ON TABLE ed_mfg_control.qc_sample IS 'Samples of Edmonton lots whose results come from a laboratory system (Laboratory Test Results); collected is local text.';

CREATE TABLE IF NOT EXISTS ed_mfg_control.qc_result (
  result_no varchar(40) NOT NULL,
  sample_no varchar(40) NOT NULL,
  test_code varchar(40) NOT NULL,
  result_value varchar(60) NOT NULL,
  result_unit varchar(20),
  spec_low varchar(60),
  spec_high varchar(60),
  conforms smallint NOT NULL,
  completed varchar(16) NOT NULL,
  analyst varchar(40) NOT NULL,
  CONSTRAINT qc_result_pk PRIMARY KEY (result_no)
);
COMMENT ON TABLE ed_mfg_control.qc_result IS 'Test results of the samples in qc_sample; conforms 1/0, completed is local text.';

CREATE TABLE IF NOT EXISTS ed_mfg_control.qc_certificate (
  certificate_no varchar(40) NOT NULL,
  lot_id varchar(20) NOT NULL,
  issued_on date NOT NULL,
  conforms smallint NOT NULL,
  approved_by varchar(40) NOT NULL,
  CONSTRAINT qc_certificate_pk PRIMARY KEY (certificate_no)
);
COMMENT ON TABLE ed_mfg_control.qc_certificate IS 'Certificates of analysis issued for Edmonton lots.';

CREATE TABLE IF NOT EXISTS ed_mfg_control.process_reading (
  asset_tag varchar(40) NOT NULL,
  parameter varchar(40) NOT NULL,
  read_at varchar(16) NOT NULL,
  lot_id varchar(20),
  reading double precision NOT NULL,
  unit varchar(20) NOT NULL,
  low_limit double precision,
  high_limit double precision,
  CONSTRAINT process_reading_pk PRIMARY KEY (asset_tag, parameter, read_at)
);
COMMENT ON TABLE ed_mfg_control.process_reading IS 'Process parameter readings from Edmonton equipment (Process Parameter Time Series); read_at is local text YYYY-MM-DD HH24:MI.';

CREATE TABLE IF NOT EXISTS ed_mfg_control.excursion_review (
  excursion_no varchar(40) NOT NULL,
  shipment_no varchar(40) NOT NULL,
  item_no varchar(20) NOT NULL,
  lot_id varchar(20) NOT NULL,
  reviewer varchar(40) NOT NULL,
  reviewed varchar(16) NOT NULL,
  stability_ref varchar(40) NOT NULL,
  disposition varchar(20) NOT NULL,
  notes text,
  CONSTRAINT excursion_review_pk PRIMARY KEY (excursion_no)
);
COMMENT ON TABLE ed_mfg_control.excursion_review IS 'Temperature excursion assessments of shipments from Edmonton lots (Temperature Excursion Assessments); reviewed is local text.';

CREATE TABLE IF NOT EXISTS ed_mfg_control.operator_qualification (
  emp_no varchar(10) NOT NULL,
  competency varchar(40) NOT NULL,
  competency_name varchar(120) NOT NULL,
  qualified_on date NOT NULL,
  expires_on date NOT NULL,
  qual_status varchar(20) NOT NULL,
  training_ref varchar(40) NOT NULL,
  certificate_no varchar(40),
  CONSTRAINT operator_qualification_pk PRIMARY KEY (emp_no, competency)
);
COMMENT ON TABLE ed_mfg_control.operator_qualification IS 'Qualifications of the operators allowed to sign (Worker Qualifications); operator.active follows the electronic signature competency EBR-SIG.';

-- End of subscription tables.

GRANT USAGE ON SCHEMA ed_mfg_control TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA ed_mfg_control TO egeria_user, airflow_user;
