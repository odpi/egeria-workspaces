-- system-qualified-name: SoftwareServer::SYS-004::LIMS LabWare Enterprise
-- LIMS LabWare Enterprise - Bucharest.  LabWare LIMS of the EKG quality control laboratory: raw material and packaging
-- lots received, finished and serum batches, their samples, tests and results against specification, EKG's
-- certificates of analysis and the supplier certificates keyed in on receipt.  Its tables feed Laboratory Test Results
-- and Supplier Material Certificates.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS labware_lims;
COMMENT ON SCHEMA labware_lims IS 'LabWare LIMS (EKG): vendor, product specification, lot, sample, test and result as replicated from the LIMS database.';

CREATE TABLE IF NOT EXISTS labware_lims.vendor (
  name            varchar(20) NOT NULL,
  description     varchar(200) NOT NULL,
  c_sap_vendor_no varchar(10) NOT NULL,
  approved        char(1) NOT NULL,
  CONSTRAINT vendor_pk PRIMARY KEY (name)
);
COMMENT ON TABLE labware_lims.vendor IS 'Vendors known to the LIMS (c_sap_vendor_no = SAP vendor number).';

INSERT INTO labware_lims.vendor (name, description, c_sap_vendor_no, approved) VALUES
('HEMMO', 'Hemmo Pharmaceuticals Pvt. Ltd.', '700110', 'T'),
('ACSDOBFAR', 'ACS Dobfar S.p.A.', '700120', 'T'),
('IPCA', 'Ipca Laboratories Ltd.', '700130', 'T'),
('BACHEM', 'Bachem AG', '700140', 'T'),
('CHEMCO', 'Chemical Company S.A.', '700150', 'T'),
('MERCKRO', 'Merck Romania S.R.L.', '700160', 'T'),
('STEVANATO', 'Stevanato Group S.p.A.', '700170', 'T'),
('GXBOLES', 'Gerresheimer Boleslawiec S.A.', '700180', 'T'),
('BALKANPT', 'Balkan Pharma Trading Ltd.', '700240', 'F'),
('ROMPAK', 'Rompak Medical S.R.L.', '700260', 'T')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS labware_lims.product_spec (
  product   varchar(20) NOT NULL,
  analysis  varchar(40) NOT NULL,
  component varchar(40) NOT NULL,
  min_value varchar(20),
  max_value varchar(20),
  units     varchar(20),
  CONSTRAINT product_spec_pk PRIMARY KEY (product, analysis, component)
);
COMMENT ON TABLE labware_lims.product_spec IS 'Specification limits per material/product, analysis and component.';

INSERT INTO labware_lims.product_spec (product, analysis, component, min_value, max_value, units) VALUES
('MP-10010', 'IR_ID', 'Identitate IR', NULL, NULL, NULL),
('MP-10010', 'TITRARE', 'Dozare', '98.0', '102.0', '%'),
('MP-10010', 'COA_ASSAY', 'Dozare (declarat)', '98.0', '102.0', '%'),
('MP-10010', 'COA_WATER', 'Apă (declarat)', NULL, '5.0', '%'),
('MP-10020', 'IR_ID', 'Identitate IR', NULL, NULL, NULL),
('MP-10020', 'TITRARE', 'Dozare', '98.0', '102.0', '%'),
('MP-10020', 'COA_ASSAY', 'Dozare (declarat)', '98.0', '102.0', '%'),
('MP-10020', 'COA_WATER', 'Apă (declarat)', NULL, '5.0', '%'),
('MP-10030', 'IR_ID', 'Identitate IR', NULL, NULL, NULL),
('MP-10030', 'TITRARE', 'Dozare', '98.0', '102.0', '%'),
('MP-10030', 'COA_ASSAY', 'Dozare (declarat)', '98.0', '102.0', '%'),
('MP-10030', 'COA_WATER', 'Apă (declarat)', NULL, '5.0', '%'),
('MP-10040', 'IR_ID', 'Identitate IR', NULL, NULL, NULL),
('MP-10040', 'TITRARE', 'Dozare', '98.0', '102.0', '%'),
('MP-10040', 'COA_ASSAY', 'Dozare (declarat)', '98.0', '102.0', '%'),
('MP-10040', 'COA_WATER', 'Apă (declarat)', NULL, '5.0', '%'),
('MP-10050', 'IR_ID', 'Identitate IR', NULL, NULL, NULL),
('MP-10050', 'TITRARE', 'Dozare', '98.0', '102.0', '%'),
('MP-10050', 'COA_ASSAY', 'Dozare (declarat)', '98.0', '102.0', '%'),
('MP-10050', 'COA_WATER', 'Apă (declarat)', NULL, '5.0', '%'),
('MP-20010', 'ID_CHIM', 'Identitate', NULL, NULL, NULL),
('MP-20010', 'COA_ASSAY', 'Dozare (declarat)', '99.0', '100.5', '%'),
('MP-40010', 'ID_CHIM', 'Identitate', NULL, NULL, NULL),
('MP-40010', 'COA_ASSAY', 'Dozare (declarat)', '99.0', '100.5', '%'),
('AMB-30010', 'ASPECT', 'Aspect și dimensiuni', NULL, NULL, NULL),
('AMB-30020', 'ASPECT', 'Aspect și dimensiuni', NULL, NULL, NULL),
('AMB-30030', 'ASPECT', 'Aspect și dimensiuni', NULL, NULL, NULL),
('AMB-30050', 'ASPECT', 'Aspect și dimensiuni', NULL, NULL, NULL),
('PF-1101', 'STERILITATE', 'Sterilitate', NULL, NULL, NULL),
('PF-1101', 'ENDOTOXINE', 'Endotoxine bacteriene', NULL, '70', 'UI/ml'),
('PF-1102', 'STERILITATE', 'Sterilitate', NULL, NULL, NULL),
('PF-1102', 'ENDOTOXINE', 'Endotoxine bacteriene', NULL, '70', 'UI/ml'),
('PF-1103', 'STERILITATE', 'Sterilitate', NULL, NULL, NULL),
('PF-1103', 'ENDOTOXINE', 'Endotoxine bacteriene', NULL, '70', 'UI/ml'),
('PF-1104', 'STERILITATE', 'Sterilitate', NULL, NULL, NULL),
('PF-1104', 'ENDOTOXINE', 'Endotoxine bacteriene', NULL, '70', 'UI/ml'),
('PF-1105', 'STERILITATE', 'Sterilitate', NULL, NULL, NULL),
('PF-1105', 'ENDOTOXINE', 'Endotoxine bacteriene', NULL, '70', 'UI/ml'),
('PF-9101', 'STERIL_RAPID', 'Sterilitate (metodă rapidă)', NULL, NULL, NULL),
('PF-9101', 'PROTEINE', 'Proteine totale', '1.0', '1.8', 'g/dl')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS labware_lims.lot (
  lot_number   integer NOT NULL,
  lot_name     varchar(40) NOT NULL,
  product      varchar(20) NOT NULL,
  c_lot_type   varchar(10) NOT NULL,
  vendor       varchar(20),
  vendor_lot   varchar(40),
  status       char(1) NOT NULL,
  approved_by  varchar(20),
  approved_on  timestamptz,
  c_coa_number varchar(40),
  c_coa_date   date,
  CONSTRAINT lot_pk PRIMARY KEY (lot_number)
);
COMMENT ON TABLE labware_lims.lot IS 'Lots: RAW (SAP batch of a received material; certificate = EKG release bulletin BA-) and FINISHED (production batch; certificate = EKG certificate of analysis CA-).  Status A approved, R rejected, U unreleased.';

INSERT INTO labware_lims.lot (lot_number, lot_name, product, c_lot_type, vendor, vendor_lot, status, approved_by, approved_on, c_coa_number, c_coa_date) VALUES
(5101, 'MP26-0061', 'MP-10010', 'RAW', 'HEMMO', 'HPPL-OXY-2604-11', 'A', 'noprea', '2026-06-19 14:20:00+00', 'BA-26-0061', '2026-06-19'),
(5102, 'MP26-0063', 'MP-20010', 'RAW', 'CHEMCO', 'CC-NACL-26-1187', 'A', 'noprea', '2026-06-16 11:10:00+00', 'BA-26-0063', '2026-06-16'),
(5103, 'MP26-0064', 'AMB-30010', 'RAW', 'STEVANATO', 'SG-A1-2605-3391', 'A', 'noprea', '2026-06-17 10:05:00+00', 'BA-26-0064', '2026-06-17'),
(5104, 'MP26-0066', 'MP-10020', 'RAW', 'ACSDOBFAR', 'ACSD-CTX-6621', 'A', 'noprea', '2026-07-09 15:45:00+00', 'BA-26-0066', '2026-07-09'),
(5105, 'MP26-0067', 'AMB-30030', 'RAW', 'GXBOLES', 'GXB-V15-26-0777', 'A', 'noprea', '2026-07-03 09:30:00+00', 'BA-26-0067', '2026-07-03'),
(5106, 'MP26-0069', 'MP-10050', 'RAW', 'BACHEM', 'BAC-OCT-4012877', 'A', 'noprea', '2026-07-23 16:00:00+00', 'BA-26-0069', '2026-07-23'),
(5107, 'MP26-0071', 'MP-10030', 'RAW', 'IPCA', 'IPCA-MCP-2606088', 'A', 'noprea', '2026-08-05 12:30:00+00', 'BA-26-0071', '2026-08-05'),
(5108, 'MP26-0072', 'AMB-30020', 'RAW', 'STEVANATO', 'SG-A2-2607-0412', 'A', 'noprea', '2026-07-30 08:40:00+00', 'BA-26-0072', '2026-07-30'),
(5109, 'MP26-0074', 'MP-10010', 'RAW', 'HEMMO', 'HPPL-OXY-2607-03', 'A', 'noprea', '2026-08-20 13:15:00+00', 'BA-26-0074', '2026-08-20'),
(5110, 'MP26-0075', 'MP-10040', 'RAW', 'IPCA', 'IPCA-OND-2607114', 'A', 'noprea', '2026-09-02 10:20:00+00', 'BA-26-0075', '2026-09-02'),
(5111, 'MP26-0077', 'MP-10050', 'RAW', 'BALKANPT', 'BPT-OCT-260811', 'R', 'noprea', '2026-09-12 12:10:00+00', 'BA-26-0077', '2026-09-12'),
(5112, 'MP26-0079', 'MP-40010', 'RAW', 'MERCKRO', 'MRK-NS-26H1904', 'A', 'noprea', '2026-09-18 09:45:00+00', 'BA-26-0079', '2026-09-18'),
(5113, 'MP26-0081', 'MP-10020', 'RAW', 'ACSDOBFAR', 'ACSD-CTX-6694', 'U', NULL, NULL, NULL, NULL),
(5114, 'MP26-0082', 'AMB-30050', 'RAW', 'ROMPAK', 'RPK-PD5-2609-15', 'U', NULL, NULL, NULL, NULL),
(5115, 'EK26-0311', 'PF-1101', 'FINISHED', NULL, NULL, 'A', 'noprea', '2026-07-21 15:00:00+00', 'CA-26-0311', '2026-07-21'),
(5116, 'EK26-0318', 'PF-1102', 'FINISHED', NULL, NULL, 'A', 'noprea', '2026-08-05 15:00:00+00', 'CA-26-0318', '2026-08-05'),
(5117, 'EK26-0324', 'PF-1105', 'FINISHED', NULL, NULL, 'A', 'noprea', '2026-08-19 15:00:00+00', 'CA-26-0324', '2026-08-19'),
(5118, 'EK26-0329', 'PF-1101', 'FINISHED', NULL, NULL, 'A', 'noprea', '2026-09-03 15:00:00+00', 'CA-26-0329', '2026-09-03'),
(5119, 'EK26-0335', 'PF-1103', 'FINISHED', NULL, NULL, 'A', 'noprea', '2026-09-18 15:00:00+00', 'CA-26-0335', '2026-09-18'),
(5120, 'EK26-0341', 'PF-1104', 'FINISHED', NULL, NULL, 'U', NULL, NULL, NULL, NULL),
(5121, 'SA26-0031', 'PF-9101', 'FINISHED', NULL, NULL, 'A', 'renache', '2026-07-16 15:00:00+00', 'CA-26-S031', '2026-07-16'),
(5122, 'SA26-0034', 'PF-9101', 'FINISHED', NULL, NULL, 'A', 'renache', '2026-08-06 15:00:00+00', 'CA-26-S034', '2026-08-06'),
(5123, 'SA26-0037', 'PF-9101', 'FINISHED', NULL, NULL, 'A', 'renache', '2026-08-27 15:00:00+00', 'CA-26-S037', '2026-08-27'),
(5124, 'SA26-0040', 'PF-9101', 'FINISHED', NULL, NULL, 'A', 'renache', '2026-09-17 15:00:00+00', 'CA-26-S040', '2026-09-17')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS labware_lims.sample (
  sample_number      integer NOT NULL,
  text_id            varchar(20) NOT NULL,
  sample_type        varchar(20) NOT NULL,
  lot                integer NOT NULL,
  product            varchar(20) NOT NULL,
  status             char(1) NOT NULL,
  sampled_date       timestamptz NOT NULL,
  login_date         timestamptz NOT NULL,
  c_supplier_cert_no varchar(40),
  c_cert_type        varchar(10),
  c_declared_conform char(1),
  CONSTRAINT sample_pk PRIMARY KEY (sample_number)
);
COMMENT ON TABLE labware_lims.sample IS 'Samples (RAW_MAT, IPC, FINISHED; SUPPLIER_COA = a supplier certificate keyed in as a pseudo-sample).  Status I in test, C complete.';

INSERT INTO labware_lims.sample (sample_number, text_id, sample_type, lot, product, status, sampled_date, login_date, c_supplier_cert_no, c_cert_type, c_declared_conform) VALUES
(26001, 'S26-26001', 'RAW_MAT', 5101, 'MP-10010', 'C', '2026-06-10 11:40:00+00', '2026-06-10 12:40:00+00', NULL, NULL, NULL),
(26002, 'S26-26002', 'SUPPLIER_COA', 5101, 'MP-10010', 'C', '2026-06-10 10:40:00+00', '2026-06-10 11:20:00+00', 'HPPL/COA/OXY/2604-11', 'COA', 'T'),
(26003, 'S26-26003', 'RAW_MAT', 5102, 'MP-20010', 'C', '2026-06-12 10:15:00+00', '2026-06-12 11:15:00+00', NULL, NULL, NULL),
(26004, 'S26-26004', 'SUPPLIER_COA', 5102, 'MP-20010', 'C', '2026-06-12 09:15:00+00', '2026-06-12 09:55:00+00', 'CC-BA-26-1187', 'COA', 'T'),
(26005, 'S26-26005', 'RAW_MAT', 5103, 'AMB-30010', 'C', '2026-06-15 14:30:00+00', '2026-06-15 15:30:00+00', NULL, NULL, NULL),
(26006, 'S26-26006', 'RAW_MAT', 5104, 'MP-10020', 'C', '2026-06-29 12:20:00+00', '2026-06-29 13:20:00+00', NULL, NULL, NULL),
(26007, 'S26-26007', 'SUPPLIER_COA', 5104, 'MP-10020', 'C', '2026-06-29 11:20:00+00', '2026-06-29 12:00:00+00', 'ACSD-COA-6621', 'COA', 'T'),
(26008, 'S26-26008', 'RAW_MAT', 5105, 'AMB-30030', 'C', '2026-07-01 09:50:00+00', '2026-07-01 10:50:00+00', NULL, NULL, NULL),
(26009, 'S26-26009', 'RAW_MAT', 5106, 'MP-10050', 'C', '2026-07-13 15:10:00+00', '2026-07-13 16:10:00+00', NULL, NULL, NULL),
(26010, 'S26-26010', 'SUPPLIER_COA', 5106, 'MP-10050', 'C', '2026-07-13 14:10:00+00', '2026-07-13 14:50:00+00', 'BAC-COA-4012877', 'COA', 'T'),
(26011, 'S26-26011', 'RAW_MAT', 5107, 'MP-10030', 'C', '2026-07-27 11:05:00+00', '2026-07-27 12:05:00+00', NULL, NULL, NULL),
(26012, 'S26-26012', 'SUPPLIER_COA', 5107, 'MP-10030', 'C', '2026-07-27 10:05:00+00', '2026-07-27 10:45:00+00', 'IPCA-COA-2606088', 'COA', 'T'),
(26013, 'S26-26013', 'RAW_MAT', 5108, 'AMB-30020', 'C', '2026-07-28 13:45:00+00', '2026-07-28 14:45:00+00', NULL, NULL, NULL),
(26014, 'S26-26014', 'RAW_MAT', 5109, 'MP-10010', 'C', '2026-08-10 12:35:00+00', '2026-08-10 13:35:00+00', NULL, NULL, NULL),
(26015, 'S26-26015', 'SUPPLIER_COA', 5109, 'MP-10010', 'C', '2026-08-10 11:35:00+00', '2026-08-10 12:15:00+00', 'HPPL/COA/OXY/2607-03', 'COA', 'T'),
(26016, 'S26-26016', 'RAW_MAT', 5110, 'MP-10040', 'C', '2026-08-24 10:55:00+00', '2026-08-24 11:55:00+00', NULL, NULL, NULL),
(26017, 'S26-26017', 'SUPPLIER_COA', 5110, 'MP-10040', 'C', '2026-08-24 09:55:00+00', '2026-08-24 10:35:00+00', 'IPCA-COA-2607114', 'COA', 'T'),
(26018, 'S26-26018', 'RAW_MAT', 5111, 'MP-10050', 'C', '2026-09-07 16:20:00+00', '2026-09-07 17:20:00+00', NULL, NULL, NULL),
(26019, 'S26-26019', 'SUPPLIER_COA', 5111, 'MP-10050', 'C', '2026-09-07 15:20:00+00', '2026-09-07 16:00:00+00', 'BPT-COA-260811', 'COA', 'T'),
(26020, 'S26-26020', 'RAW_MAT', 5112, 'MP-40010', 'C', '2026-09-14 11:30:00+00', '2026-09-14 12:30:00+00', NULL, NULL, NULL),
(26021, 'S26-26021', 'SUPPLIER_COA', 5112, 'MP-40010', 'C', '2026-09-14 10:30:00+00', '2026-09-14 11:10:00+00', 'MRK-COA-26H1904', 'COA', 'T'),
(26022, 'S26-26022', 'RAW_MAT', 5113, 'MP-10020', 'I', '2026-09-21 12:00:00+00', '2026-09-21 13:00:00+00', NULL, NULL, NULL),
(26023, 'S26-26023', 'SUPPLIER_COA', 5113, 'MP-10020', 'C', '2026-09-21 11:00:00+00', '2026-09-21 11:40:00+00', 'ACSD-COA-6694', 'COA', 'T'),
(26024, 'S26-26024', 'RAW_MAT', 5114, 'AMB-30050', 'I', '2026-09-24 10:20:00+00', '2026-09-24 11:20:00+00', NULL, NULL, NULL),
(26025, 'S26-26025', 'FINISHED', 5115, 'PF-1101', 'C', '2026-07-08 18:00:00+00', '2026-07-08 19:00:00+00', NULL, NULL, NULL),
(26026, 'S26-26026', 'FINISHED', 5116, 'PF-1102', 'C', '2026-07-22 16:00:00+00', '2026-07-22 17:00:00+00', NULL, NULL, NULL),
(26027, 'S26-26027', 'FINISHED', 5117, 'PF-1105', 'C', '2026-08-05 17:00:00+00', '2026-08-05 18:00:00+00', NULL, NULL, NULL),
(26028, 'S26-26028', 'FINISHED', 5118, 'PF-1101', 'C', '2026-08-19 18:00:00+00', '2026-08-19 19:00:00+00', NULL, NULL, NULL),
(26029, 'S26-26029', 'FINISHED', 5119, 'PF-1103', 'C', '2026-09-02 18:00:00+00', '2026-09-02 19:00:00+00', NULL, NULL, NULL),
(26030, 'S26-26030', 'IPC', 5119, 'PF-1103', 'C', '2026-08-31 22:00:00+00', '2026-08-31 23:00:00+00', NULL, NULL, NULL),
(26031, 'S26-26031', 'FINISHED', 5120, 'PF-1104', 'I', '2026-09-16 17:00:00+00', '2026-09-16 18:00:00+00', NULL, NULL, NULL),
(26032, 'S26-26032', 'IPC', 5120, 'PF-1104', 'C', '2026-09-14 22:00:00+00', '2026-09-14 23:00:00+00', NULL, NULL, NULL),
(26033, 'S26-26033', 'FINISHED', 5121, 'PF-9101', 'C', '2026-07-15 18:00:00+00', '2026-07-15 19:00:00+00', NULL, NULL, NULL),
(26034, 'S26-26034', 'FINISHED', 5122, 'PF-9101', 'C', '2026-08-05 19:00:00+00', '2026-08-05 20:00:00+00', NULL, NULL, NULL),
(26035, 'S26-26035', 'FINISHED', 5123, 'PF-9101', 'C', '2026-08-27 14:00:00+00', '2026-08-27 15:00:00+00', NULL, NULL, NULL),
(26036, 'S26-26036', 'FINISHED', 5124, 'PF-9101', 'C', '2026-09-17 14:00:00+00', '2026-09-17 15:00:00+00', NULL, NULL, NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS labware_lims.test (
  test_number    integer NOT NULL,
  sample_number  integer NOT NULL,
  analysis       varchar(40) NOT NULL,
  status         char(1) NOT NULL,
  date_completed timestamptz,
  CONSTRAINT test_pk PRIMARY KEY (test_number)
);
COMMENT ON TABLE labware_lims.test IS 'Tests on samples.';

INSERT INTO labware_lims.test (test_number, sample_number, analysis, status, date_completed) VALUES
(81003, 26001, 'IR_ID', 'C', '2026-06-19 11:20:00+00'),
(81006, 26001, 'TITRARE', 'C', '2026-06-19 11:20:00+00'),
(81009, 26002, 'COA_ASSAY', 'C', '2026-06-10 11:20:00+00'),
(81012, 26002, 'COA_WATER', 'C', '2026-06-10 11:20:00+00'),
(81015, 26003, 'ID_CHIM', 'C', '2026-06-16 08:10:00+00'),
(81018, 26004, 'COA_ASSAY', 'C', '2026-06-12 09:55:00+00'),
(81021, 26005, 'ASPECT', 'C', '2026-06-17 07:05:00+00'),
(81024, 26006, 'IR_ID', 'C', '2026-07-09 12:45:00+00'),
(81027, 26006, 'TITRARE', 'C', '2026-07-09 12:45:00+00'),
(81030, 26007, 'COA_ASSAY', 'C', '2026-06-29 12:00:00+00'),
(81033, 26007, 'COA_WATER', 'C', '2026-06-29 12:00:00+00'),
(81036, 26008, 'ASPECT', 'C', '2026-07-03 06:30:00+00'),
(81039, 26009, 'IR_ID', 'C', '2026-07-23 13:00:00+00'),
(81042, 26009, 'TITRARE', 'C', '2026-07-23 13:00:00+00'),
(81045, 26010, 'COA_ASSAY', 'C', '2026-07-13 14:50:00+00'),
(81048, 26010, 'COA_WATER', 'C', '2026-07-13 14:50:00+00'),
(81051, 26011, 'IR_ID', 'C', '2026-08-05 09:30:00+00'),
(81054, 26011, 'TITRARE', 'C', '2026-08-05 09:30:00+00'),
(81057, 26012, 'COA_ASSAY', 'C', '2026-07-27 10:45:00+00'),
(81060, 26012, 'COA_WATER', 'C', '2026-07-27 10:45:00+00'),
(81063, 26013, 'ASPECT', 'C', '2026-07-30 05:40:00+00'),
(81066, 26014, 'IR_ID', 'C', '2026-08-20 10:15:00+00'),
(81069, 26014, 'TITRARE', 'C', '2026-08-20 10:15:00+00'),
(81072, 26015, 'COA_ASSAY', 'C', '2026-08-10 12:15:00+00'),
(81075, 26015, 'COA_WATER', 'C', '2026-08-10 12:15:00+00'),
(81078, 26016, 'IR_ID', 'C', '2026-09-02 07:20:00+00'),
(81081, 26016, 'TITRARE', 'C', '2026-09-02 07:20:00+00'),
(81084, 26017, 'COA_ASSAY', 'C', '2026-08-24 10:35:00+00'),
(81087, 26017, 'COA_WATER', 'C', '2026-08-24 10:35:00+00'),
(81090, 26018, 'IR_ID', 'C', '2026-09-12 09:10:00+00'),
(81093, 26018, 'TITRARE', 'C', '2026-09-12 09:10:00+00'),
(81096, 26019, 'COA_ASSAY', 'C', '2026-09-07 16:00:00+00'),
(81099, 26019, 'COA_WATER', 'C', '2026-09-07 16:00:00+00'),
(81102, 26020, 'ID_CHIM', 'C', '2026-09-18 06:45:00+00'),
(81105, 26021, 'COA_ASSAY', 'C', '2026-09-14 11:10:00+00'),
(81108, 26022, 'IR_ID', 'I', NULL),
(81111, 26022, 'TITRARE', 'I', NULL),
(81114, 26023, 'COA_ASSAY', 'C', '2026-09-21 11:40:00+00'),
(81117, 26023, 'COA_WATER', 'C', '2026-09-21 11:40:00+00'),
(81120, 26024, 'ASPECT', 'I', NULL),
(81123, 26025, 'ENDOTOXINE', 'C', '2026-07-10 20:00:00+00'),
(81126, 26025, 'STERILITATE', 'C', '2026-07-21 11:00:00+00'),
(81129, 26026, 'ENDOTOXINE', 'C', '2026-07-24 18:00:00+00'),
(81132, 26026, 'STERILITATE', 'C', '2026-08-05 11:00:00+00'),
(81135, 26027, 'ENDOTOXINE', 'C', '2026-08-07 19:00:00+00'),
(81138, 26027, 'STERILITATE', 'C', '2026-08-19 11:00:00+00'),
(81141, 26028, 'ENDOTOXINE', 'C', '2026-08-21 20:00:00+00'),
(81144, 26028, 'STERILITATE', 'C', '2026-09-03 11:00:00+00'),
(81147, 26029, 'ENDOTOXINE', 'C', '2026-09-04 20:00:00+00'),
(81150, 26029, 'STERILITATE', 'C', '2026-09-18 11:00:00+00'),
(81153, 26031, 'ENDOTOXINE', 'C', '2026-09-18 19:00:00+00'),
(81156, 26033, 'STERIL_RAPID', 'C', '2026-07-16 12:00:00+00'),
(81159, 26033, 'PROTEINE', 'C', '2026-07-16 12:00:00+00'),
(81162, 26034, 'STERIL_RAPID', 'C', '2026-08-06 13:00:00+00'),
(81165, 26034, 'PROTEINE', 'C', '2026-08-06 13:00:00+00'),
(81168, 26035, 'STERIL_RAPID', 'C', '2026-08-28 08:00:00+00'),
(81171, 26035, 'PROTEINE', 'C', '2026-08-28 08:00:00+00'),
(81174, 26036, 'STERIL_RAPID', 'C', '2026-09-18 08:00:00+00'),
(81177, 26036, 'PROTEINE', 'C', '2026-09-18 08:00:00+00')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS labware_lims.result (
  result_number   integer NOT NULL,
  test_number     integer NOT NULL,
  sample_number   integer NOT NULL,
  analysis        varchar(40) NOT NULL,
  name            varchar(40) NOT NULL,
  formatted_entry varchar(60) NOT NULL,
  units           varchar(20),
  in_spec         char(1) NOT NULL,
  status          char(1) NOT NULL,
  entered_by      varchar(20) NOT NULL,
  entered_on      timestamptz NOT NULL,
  CONSTRAINT result_pk PRIMARY KEY (result_number)
);
COMMENT ON TABLE labware_lims.result IS 'Results (status A approved, E entered; entered_by = AD login authenticated over LDAP).';

INSERT INTO labware_lims.result (result_number, test_number, sample_number, analysis, name, formatted_entry, units, in_spec, status, entered_by, entered_on) VALUES
(240007, 81003, 26001, 'IR_ID', 'Identitate IR', 'Conform', NULL, 'T', 'A', 'epopescu', '2026-06-19 11:20:00+00'),
(240014, 81006, 26001, 'TITRARE', 'Dozare', '99.9', '%', 'T', 'A', 'epopescu', '2026-06-19 11:20:00+00'),
(240021, 81009, 26002, 'COA_ASSAY', 'Dozare (declarat)', '99.4', '%', 'T', 'A', 'istan', '2026-06-10 11:20:00+00'),
(240028, 81012, 26002, 'COA_WATER', 'Apă (declarat)', '1.0', '%', 'T', 'A', 'istan', '2026-06-10 11:20:00+00'),
(240035, 81015, 26003, 'ID_CHIM', 'Identitate', 'Conform', NULL, 'T', 'A', 'svasile', '2026-06-16 08:10:00+00'),
(240042, 81018, 26004, 'COA_ASSAY', 'Dozare (declarat)', '99.8', '%', 'T', 'A', 'epopescu', '2026-06-12 09:55:00+00'),
(240049, 81021, 26005, 'ASPECT', 'Aspect și dimensiuni', 'Conform', NULL, 'T', 'A', 'svasile', '2026-06-17 07:05:00+00'),
(240056, 81024, 26006, 'IR_ID', 'Identitate IR', 'Conform', NULL, 'T', 'A', 'istan', '2026-07-09 12:45:00+00'),
(240063, 81027, 26006, 'TITRARE', 'Dozare', '100.2', '%', 'T', 'A', 'istan', '2026-07-09 12:45:00+00'),
(240070, 81030, 26007, 'COA_ASSAY', 'Dozare (declarat)', '99.6', '%', 'T', 'A', 'istan', '2026-06-29 12:00:00+00'),
(240077, 81033, 26007, 'COA_WATER', 'Apă (declarat)', '1.6', '%', 'T', 'A', 'istan', '2026-06-29 12:00:00+00'),
(240084, 81036, 26008, 'ASPECT', 'Aspect și dimensiuni', 'Conform', NULL, 'T', 'A', 'istan', '2026-07-03 06:30:00+00'),
(240091, 81039, 26009, 'IR_ID', 'Identitate IR', 'Conform', NULL, 'T', 'A', 'istan', '2026-07-23 13:00:00+00'),
(240098, 81042, 26009, 'TITRARE', 'Dozare', '99.2', '%', 'T', 'A', 'istan', '2026-07-23 13:00:00+00'),
(240105, 81045, 26010, 'COA_ASSAY', 'Dozare (declarat)', '99.7', '%', 'T', 'A', 'istan', '2026-07-13 14:50:00+00'),
(240112, 81048, 26010, 'COA_WATER', 'Apă (declarat)', '2.1', '%', 'T', 'A', 'istan', '2026-07-13 14:50:00+00'),
(240119, 81051, 26011, 'IR_ID', 'Identitate IR', 'Conform', NULL, 'T', 'A', 'istan', '2026-08-05 09:30:00+00'),
(240126, 81054, 26011, 'TITRARE', 'Dozare', '99.6', '%', 'T', 'A', 'istan', '2026-08-05 09:30:00+00'),
(240133, 81057, 26012, 'COA_ASSAY', 'Dozare (declarat)', '99.8', '%', 'T', 'A', 'istan', '2026-07-27 10:45:00+00'),
(240140, 81060, 26012, 'COA_WATER', 'Apă (declarat)', '2.3', '%', 'T', 'A', 'istan', '2026-07-27 10:45:00+00'),
(240147, 81063, 26013, 'ASPECT', 'Aspect și dimensiuni', 'Conform', NULL, 'T', 'A', 'epopescu', '2026-07-30 05:40:00+00'),
(240154, 81066, 26014, 'IR_ID', 'Identitate IR', 'Conform', NULL, 'T', 'A', 'svasile', '2026-08-20 10:15:00+00'),
(240161, 81069, 26014, 'TITRARE', 'Dozare', '100.0', '%', 'T', 'A', 'svasile', '2026-08-20 10:15:00+00'),
(240168, 81072, 26015, 'COA_ASSAY', 'Dozare (declarat)', '99.3', '%', 'T', 'A', 'istan', '2026-08-10 12:15:00+00'),
(240175, 81075, 26015, 'COA_WATER', 'Apă (declarat)', '0.7', '%', 'T', 'A', 'istan', '2026-08-10 12:15:00+00'),
(240182, 81078, 26016, 'IR_ID', 'Identitate IR', 'Conform', NULL, 'T', 'A', 'istan', '2026-09-02 07:20:00+00'),
(240189, 81081, 26016, 'TITRARE', 'Dozare', '99.8', '%', 'T', 'A', 'istan', '2026-09-02 07:20:00+00'),
(240196, 81084, 26017, 'COA_ASSAY', 'Dozare (declarat)', '99.9', '%', 'T', 'A', 'istan', '2026-08-24 10:35:00+00'),
(240203, 81087, 26017, 'COA_WATER', 'Apă (declarat)', '0.9', '%', 'T', 'A', 'istan', '2026-08-24 10:35:00+00'),
(240210, 81090, 26018, 'IR_ID', 'Identitate IR', 'Conform', NULL, 'T', 'A', 'epopescu', '2026-09-12 09:10:00+00'),
(240217, 81093, 26018, 'TITRARE', 'Dozare', '96.1', '%', 'F', 'A', 'epopescu', '2026-09-12 09:10:00+00'),
(240224, 81096, 26019, 'COA_ASSAY', 'Dozare (declarat)', '99.6', '%', 'T', 'A', 'imoldovan', '2026-09-07 16:00:00+00'),
(240231, 81099, 26019, 'COA_WATER', 'Apă (declarat)', '1.2', '%', 'T', 'A', 'imoldovan', '2026-09-07 16:00:00+00'),
(240238, 81102, 26020, 'ID_CHIM', 'Identitate', 'Conform', NULL, 'T', 'A', 'epopescu', '2026-09-18 06:45:00+00'),
(240245, 81105, 26021, 'COA_ASSAY', 'Dozare (declarat)', '99.9', '%', 'T', 'A', 'istan', '2026-09-14 11:10:00+00'),
(240252, 81108, 26022, 'IR_ID', 'Identitate IR', 'Conform', NULL, 'T', 'E', 'epopescu', '2026-09-25 11:00:00+00'),
(240259, 81111, 26022, 'TITRARE', 'Dozare', '100.3', '%', 'T', 'E', 'epopescu', '2026-09-25 11:00:00+00'),
(240266, 81114, 26023, 'COA_ASSAY', 'Dozare (declarat)', '99.3', '%', 'T', 'A', 'istan', '2026-09-21 11:40:00+00'),
(240273, 81117, 26023, 'COA_WATER', 'Apă (declarat)', '1.2', '%', 'T', 'A', 'istan', '2026-09-21 11:40:00+00'),
(240280, 81120, 26024, 'ASPECT', 'Aspect și dimensiuni', 'Conform', NULL, 'T', 'E', 'istan', '2026-09-28 09:20:00+00'),
(240287, 81123, 26025, 'ENDOTOXINE', 'Endotoxine bacteriene', '5', 'UI/ml', 'T', 'A', 'istan', '2026-07-10 20:00:00+00'),
(240294, 81126, 26025, 'STERILITATE', 'Sterilitate', 'Steril', NULL, 'T', 'A', 'istan', '2026-07-21 11:00:00+00'),
(240301, 81129, 26026, 'ENDOTOXINE', 'Endotoxine bacteriene', '2', 'UI/ml', 'T', 'A', 'svasile', '2026-07-24 18:00:00+00'),
(240308, 81132, 26026, 'STERILITATE', 'Sterilitate', 'Steril', NULL, 'T', 'A', 'epopescu', '2026-08-05 11:00:00+00'),
(240315, 81135, 26027, 'ENDOTOXINE', 'Endotoxine bacteriene', '7', 'UI/ml', 'T', 'A', 'istan', '2026-08-07 19:00:00+00'),
(240322, 81138, 26027, 'STERILITATE', 'Sterilitate', 'Steril', NULL, 'T', 'A', 'istan', '2026-08-19 11:00:00+00'),
(240329, 81141, 26028, 'ENDOTOXINE', 'Endotoxine bacteriene', '1', 'UI/ml', 'T', 'A', 'istan', '2026-08-21 20:00:00+00'),
(240336, 81144, 26028, 'STERILITATE', 'Sterilitate', 'Steril', NULL, 'T', 'A', 'epopescu', '2026-09-03 11:00:00+00'),
(240343, 81147, 26029, 'ENDOTOXINE', 'Endotoxine bacteriene', '7', 'UI/ml', 'T', 'A', 'epopescu', '2026-09-04 20:00:00+00'),
(240350, 81150, 26029, 'STERILITATE', 'Sterilitate', 'Steril', NULL, 'T', 'A', 'istan', '2026-09-18 11:00:00+00'),
(240357, 81153, 26031, 'ENDOTOXINE', 'Endotoxine bacteriene', '7', 'UI/ml', 'T', 'A', 'epopescu', '2026-09-18 19:00:00+00'),
(240364, 81156, 26033, 'STERIL_RAPID', 'Sterilitate (metodă rapidă)', 'Steril', NULL, 'T', 'A', 'svasile', '2026-07-16 12:00:00+00'),
(240371, 81159, 26033, 'PROTEINE', 'Proteine totale', '1.5', 'g/dl', 'T', 'A', 'svasile', '2026-07-16 12:00:00+00'),
(240378, 81162, 26034, 'STERIL_RAPID', 'Sterilitate (metodă rapidă)', 'Steril', NULL, 'T', 'A', 'epopescu', '2026-08-06 13:00:00+00'),
(240385, 81165, 26034, 'PROTEINE', 'Proteine totale', '1.3', 'g/dl', 'T', 'A', 'epopescu', '2026-08-06 13:00:00+00'),
(240392, 81168, 26035, 'STERIL_RAPID', 'Sterilitate (metodă rapidă)', 'Steril', NULL, 'T', 'A', 'epopescu', '2026-08-28 08:00:00+00'),
(240399, 81171, 26035, 'PROTEINE', 'Proteine totale', '1.5', 'g/dl', 'T', 'A', 'epopescu', '2026-08-28 08:00:00+00'),
(240406, 81174, 26036, 'STERIL_RAPID', 'Sterilitate (metodă rapidă)', 'Steril', NULL, 'T', 'A', 'imoldovan', '2026-09-18 08:00:00+00'),
(240413, 81177, 26036, 'PROTEINE', 'Proteine totale', '1.2', 'g/dl', 'T', 'A', 'imoldovan', '2026-09-18 08:00:00+00')
ON CONFLICT DO NOTHING;

-- Incoming-testing requests from the warehouse quarantine (subscription apply script buc_labware_lims__material_quarantine_dispositions).
CREATE TABLE IF NOT EXISTS labware_lims.c_quarantine_request (
  lot_name        varchar(40) NOT NULL,
  product         varchar(20) NOT NULL,
  receipt_ref     varchar(40),
  quarantined_on  timestamptz,
  location        varchar(20),
  quantity        integer,
  wms_sample_ref  varchar(40),
  wms_status      varchar(20),
  request_status  char(1) NOT NULL,
  received_on     timestamptz NOT NULL,
  CONSTRAINT c_quarantine_request_pk PRIMARY KEY (lot_name)
);
COMMENT ON TABLE labware_lims.c_quarantine_request IS 'Custom table: lots placed in quarantine by the WMS that have not yet been logged in as a LIMS lot (request_status P pending log-in).';

GRANT USAGE ON SCHEMA labware_lims TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA labware_lims TO egeria_user, airflow_user;
