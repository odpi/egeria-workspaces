-- system-qualified-name: System::winch-mfg-control
-- Winchester Manufacturing Control System - Coco core.  Homegrown control system for the Winchester factory (aspirin, rosuvastatin and the Cocolecel cell therapy); feeds Batch Execution Records and Electronic Batch Records.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS winch_mfg_control;
COMMENT ON SCHEMA winch_mfg_control IS 'Winchester Manufacturing Control System (Coco core): batch header, executed steps, materials, equipment, batch record sections and QP release.';

CREATE TABLE IF NOT EXISTS winch_mfg_control.wbatch (
  batch_no varchar(20) NOT NULL,
  prd_cd char(4) NOT NULL,
  psn_ref varchar(20),
  plan_ord varchar(20),
  strt_ts timestamptz NOT NULL,
  end_ts timestamptz,
  qty_made integer,
  uom varchar(4) NOT NULL,
  sts char(3) NOT NULL,
  rec_cmplt char(1) NOT NULL,
  qp_sts char(1) NOT NULL,
  CONSTRAINT wbatch_pk PRIMARY KEY (batch_no)
);
COMMENT ON TABLE winch_mfg_control.wbatch IS 'Winchester batch header. sts RUN/QCH/REL/REJ; rec_cmplt Y when every batch record section is in; qp_sts A awaiting, C certified, R rejected. psn_ref is the patient pseudonym for cell therapy batches.';

CREATE TABLE IF NOT EXISTS winch_mfg_control.wstep (
  batch_no varchar(20) NOT NULL,
  step_no smallint NOT NULL,
  op_cd varchar(8) NOT NULL,
  st_ts timestamptz NOT NULL,
  en_ts timestamptz,
  opr_psn varchar(20) NOT NULL,
  esig varchar(200),
  dev_flg char(1) NOT NULL,
  abrt_flg char(1) NOT NULL,
  CONSTRAINT wstep_pk PRIMARY KEY (batch_no, step_no)
);
COMMENT ON TABLE winch_mfg_control.wstep IS 'Executed process steps. en_ts and esig are empty while the step is running; dev_flg Y when a deviation was raised in the step.';

CREATE TABLE IF NOT EXISTS winch_mfg_control.wmatl (
  batch_no varchar(20) NOT NULL,
  step_no smallint NOT NULL,
  lot_no varchar(30) NOT NULL,
  mat_cd varchar(10) NOT NULL,
  qty numeric(12,3) NOT NULL,
  uom varchar(6) NOT NULL,
  CONSTRAINT wmatl_pk PRIMARY KEY (batch_no, step_no, lot_no)
);
COMMENT ON TABLE winch_mfg_control.wmatl IS 'Material lots consumed in each step.';

CREATE TABLE IF NOT EXISTS winch_mfg_control.wstep_eq (
  batch_no varchar(20) NOT NULL,
  step_no smallint NOT NULL,
  eq_id varchar(16) NOT NULL,
  qual_at_use char(1) NOT NULL,
  cal_due date NOT NULL,
  CONSTRAINT wstep_eq_pk PRIMARY KEY (batch_no, step_no, eq_id)
);
COMMENT ON TABLE winch_mfg_control.wstep_eq IS 'Equipment used in each step with the qualification status (Q qualified, X expired, N not qualified) and calibration due date read at use.';

CREATE TABLE IF NOT EXISTS winch_mfg_control.wdoc (
  batch_no varchar(20) NOT NULL,
  sect_ref varchar(40) NOT NULL,
  sect_typ varchar(5) NOT NULL,
  src_sys varchar(60) NOT NULL,
  rcvd_ts timestamptz NOT NULL,
  CONSTRAINT wdoc_pk PRIMARY KEY (batch_no, sect_ref)
);
COMMENT ON TABLE winch_mfg_control.wdoc IS 'Batch record sections received. sect_typ EXEC, PARAM, LAB, DEV, EXC, SIGN.';

CREATE TABLE IF NOT EXISTS winch_mfg_control.wrel (
  batch_no varchar(20) NOT NULL,
  mkt varchar(4) NOT NULL,
  rel_qty integer NOT NULL,
  cert_dt date NOT NULL,
  qp_psn varchar(20) NOT NULL,
  CONSTRAINT wrel_pk PRIMARY KEY (batch_no, mkt)
);
COMMENT ON TABLE winch_mfg_control.wrel IS 'QP certification and release per market (mkt uses UK for Great Britain).';

INSERT INTO winch_mfg_control.wbatch (batch_no, prd_cd, psn_ref, plan_ord, strt_ts, end_ts, qty_made, uom, sts, rec_cmplt, qp_sts) VALUES
('W26-1000-0031', '1000', NULL, 'GMP-PO-26-0402', '2026-07-27 07:00+00', '2026-07-28 16:00+00', 250000, 'TAB', 'REL', 'Y', 'C'),
('W26-1010-0012', '1010', NULL, 'GMP-PO-26-0418', '2026-08-10 07:00+00', '2026-08-11 15:30+00', 150000, 'TAB', 'REL', 'Y', 'C'),
('W26-5000-0024', '5000', NULL, 'GMP-PO-26-0437', '2026-08-24 07:00+00', '2026-08-25 17:00+00', 90000, 'TAB', 'REL', 'Y', 'C'),
('W26-1000-0032', '1000', NULL, 'GMP-PO-26-0455', '2026-09-14 07:00+00', '2026-09-15 16:00+00', 250000, 'TAB', 'QCH', 'N', 'A'),
('W26-5000-0025', '5000', NULL, 'GMP-PO-26-0469', '2026-09-29 07:00+00', NULL, NULL, 'TAB', 'RUN', 'N', 'A'),
('W26-9100-0003', '9100', 'CPX-7K4Q2M', 'GMP-PO-26-0371', '2026-05-26 09:00+00', '2026-06-05 17:00+00', 1, 'BAG', 'REL', 'Y', 'C'),
('W26-9100-0004', '9100', 'CPX-3M8R1T', 'GMP-PO-26-0385', '2026-06-16 09:00+00', '2026-06-26 16:00+00', 1, 'BAG', 'REL', 'Y', 'C'),
('W26-9100-0005', '9100', 'CPX-9D2H6W', 'GMP-PO-26-0398', '2026-07-07 09:00+00', '2026-07-17 15:00+00', 1, 'BAG', 'REL', 'Y', 'C'),
('W26-9100-0007', '9100', 'CPX-5T1N8B', 'GMP-PO-26-0416', '2026-08-04 09:00+00', '2026-08-14 16:00+00', 1, 'BAG', 'REL', 'Y', 'C'),
('W26-9100-0008', '9100', 'CPX-2B7J4Y', 'GMP-PO-26-0452', '2026-09-22 09:00+00', NULL, NULL, 'BAG', 'RUN', 'N', 'A')
ON CONFLICT DO NOTHING;

INSERT INTO winch_mfg_control.wstep (batch_no, step_no, op_cd, st_ts, en_ts, opr_psn, esig, dev_flg, abrt_flg) VALUES
('W26-1000-0031', 1, 'DISP', '2026-07-27 07:00+00', '2026-07-27 15:00+00', 'CW-F53CJR', 'mgrange|202607270700|743a1486ec69ed1f1f5c', 'N', 'N'),
('W26-1000-0031', 2, 'GRAN', '2026-07-27 15:15+00', '2026-07-27 23:15+00', 'CW-F53CJR', 'mgrange|202607271515|d9aed93786a8bfa328b5', 'N', 'N'),
('W26-1000-0031', 3, 'COMP', '2026-07-27 23:30+00', '2026-07-28 07:30+00', 'CW-F53CJR', 'mgrange|202607272330|c7678dea8b0a014d71b5', 'N', 'N'),
('W26-1000-0031', 4, 'PACK', '2026-07-28 07:45+00', '2026-07-28 15:45+00', 'CW-F53CJR', 'mgrange|202607280745|4403074275a83aafeb48', 'N', 'N'),
('W26-1010-0012', 1, 'DISP', '2026-08-10 07:00+00', '2026-08-10 14:52+00', 'CW-F53CJR', 'mgrange|202608100700|1ddcae39a4bdb8a5377a', 'N', 'N'),
('W26-1010-0012', 2, 'GRAN', '2026-08-10 15:07+00', '2026-08-10 23:00+00', 'CW-F53CJR', 'mgrange|202608101507|5d4c69d354f556a56eab', 'N', 'N'),
('W26-1010-0012', 3, 'COMP', '2026-08-10 23:15+00', '2026-08-11 07:07+00', 'CW-F53CJR', 'mgrange|202608102315|cb7ad6e63b53116effbd', 'N', 'N'),
('W26-1010-0012', 4, 'PACK', '2026-08-11 07:22+00', '2026-08-11 15:15+00', 'CW-F53CJR', 'mgrange|202608110722|2373174d3fdc3f974ea7', 'N', 'N'),
('W26-5000-0024', 1, 'DISP', '2026-08-24 07:00+00', '2026-08-24 15:15+00', 'CW-F53CJR', 'mgrange|202608240700|f316e83edf1092a5fdf7', 'N', 'N'),
('W26-5000-0024', 2, 'GRAN', '2026-08-24 15:30+00', '2026-08-24 23:45+00', 'CW-F53CJR', 'mgrange|202608241530|9fa808e2aff4f0d98056', 'N', 'N'),
('W26-5000-0024', 3, 'COMP', '2026-08-25 00:00+00', '2026-08-25 08:15+00', 'CW-F53CJR', 'mgrange|202608250000|917963a9a826b1b3d8c4', 'Y', 'N'),
('W26-5000-0024', 4, 'PACK', '2026-08-25 08:30+00', '2026-08-25 16:45+00', 'CW-F53CJR', 'mgrange|202608250830|9ae35cf7f4bd5254cfae', 'N', 'N'),
('W26-1000-0032', 1, 'DISP', '2026-09-14 07:00+00', '2026-09-14 15:00+00', 'CW-F53CJR', 'mgrange|202609140700|8a62e1cf3d24606d7f95', 'N', 'N'),
('W26-1000-0032', 2, 'GRAN', '2026-09-14 15:15+00', '2026-09-14 23:15+00', 'CW-F53CJR', 'mgrange|202609141515|930a471a9b316e1059f7', 'N', 'N'),
('W26-1000-0032', 3, 'COMP', '2026-09-14 23:30+00', '2026-09-15 07:30+00', 'CW-F53CJR', 'mgrange|202609142330|f757a2fcfb522989d6ed', 'N', 'N'),
('W26-1000-0032', 4, 'PACK', '2026-09-15 07:45+00', '2026-09-15 15:45+00', 'CW-F53CJR', 'mgrange|202609150745|8be2654cb68b4857fa5e', 'N', 'N'),
('W26-5000-0025', 1, 'DISP', '2026-09-29 07:00+00', '2026-09-29 21:45+00', 'CW-F53CJR', 'mgrange|202609290700|a7d7267ba1b70823b347', 'N', 'N'),
('W26-5000-0025', 2, 'GRAN', '2026-09-29 22:00+00', NULL, 'CW-F53CJR', NULL, 'N', 'N'),
('W26-9100-0003', 1, 'SEL', '2026-05-26 09:00+00', '2026-05-28 22:45+00', 'CW-XE6DBG', 'arahman|202605260900|d4d61b543ad923685d61', 'N', 'N'),
('W26-9100-0003', 2, 'TRANSD', '2026-05-28 23:00+00', '2026-05-31 12:45+00', 'CW-XE6DBG', 'arahman|202605282300|b75ebf6ecaac981a24f5', 'N', 'N'),
('W26-9100-0003', 3, 'EXPN', '2026-05-31 13:00+00', '2026-06-03 02:45+00', 'CW-XE6DBG', 'arahman|202605311300|3cd1526397d39db95dc0', 'N', 'N'),
('W26-9100-0003', 4, 'HARV', '2026-06-03 03:00+00', '2026-06-05 16:45+00', 'CW-XE6DBG', 'arahman|202606030300|00c9f5b4e9e4a8c970ac', 'N', 'N'),
('W26-9100-0004', 1, 'SEL', '2026-06-16 09:00+00', '2026-06-18 22:30+00', 'CW-XE6DBG', 'arahman|202606160900|f8fa08f31864e74961e6', 'N', 'N'),
('W26-9100-0004', 2, 'TRANSD', '2026-06-18 22:45+00', '2026-06-21 12:15+00', 'CW-XE6DBG', 'arahman|202606182245|f49e02a3c9b652809080', 'N', 'N'),
('W26-9100-0004', 3, 'EXPN', '2026-06-21 12:30+00', '2026-06-24 02:00+00', 'CW-XE6DBG', 'arahman|202606211230|939757c538fb3a235614', 'N', 'N'),
('W26-9100-0004', 4, 'HARV', '2026-06-24 02:15+00', '2026-06-26 15:45+00', 'CW-XE6DBG', 'arahman|202606240215|0eab043a60bddc8411bf', 'N', 'N'),
('W26-9100-0005', 1, 'SEL', '2026-07-07 09:00+00', '2026-07-09 22:15+00', 'CW-XE6DBG', 'arahman|202607070900|6408f9433f3b296538d8', 'N', 'N'),
('W26-9100-0005', 2, 'TRANSD', '2026-07-09 22:30+00', '2026-07-12 11:45+00', 'CW-XE6DBG', 'arahman|202607092230|b981fafe9ddca5ebe929', 'N', 'N'),
('W26-9100-0005', 3, 'EXPN', '2026-07-12 12:00+00', '2026-07-15 01:15+00', 'CW-XE6DBG', 'arahman|202607121200|1890d838165203c9efe7', 'N', 'N'),
('W26-9100-0005', 4, 'HARV', '2026-07-15 01:30+00', '2026-07-17 14:45+00', 'CW-XE6DBG', 'arahman|202607150130|36eefaf69a66d6efdd4e', 'N', 'N'),
('W26-9100-0007', 1, 'SEL', '2026-08-04 09:00+00', '2026-08-06 22:30+00', 'CW-XE6DBG', 'arahman|202608040900|503992de8e55f40c2595', 'N', 'N'),
('W26-9100-0007', 2, 'TRANSD', '2026-08-06 22:45+00', '2026-08-09 12:15+00', 'CW-XE6DBG', 'arahman|202608062245|09b5df365ab8f182dfad', 'N', 'N'),
('W26-9100-0007', 3, 'EXPN', '2026-08-09 12:30+00', '2026-08-12 02:00+00', 'CW-XE6DBG', 'arahman|202608091230|a70e313d5d653c59d243', 'N', 'N'),
('W26-9100-0007', 4, 'HARV', '2026-08-12 02:15+00', '2026-08-14 15:45+00', 'CW-XE6DBG', 'arahman|202608120215|71c4948257cf950bd672', 'N', 'N'),
('W26-9100-0008', 1, 'SEL', '2026-09-22 09:00+00', '2026-09-24 20:45+00', 'CW-XE6DBG', 'arahman|202609220900|4f6c03c2d50c31a98fdd', 'N', 'N'),
('W26-9100-0008', 2, 'TRANSD', '2026-09-24 21:00+00', '2026-09-27 08:45+00', 'CW-K7H7ZQ', 'otate|202609242100|dbfe1d58b29d209acdc2', 'N', 'N'),
('W26-9100-0008', 3, 'EXPN', '2026-09-27 09:00+00', '2026-09-29 20:45+00', 'CW-XE6DBG', 'arahman|202609270900|a4791a1242f74f3f480c', 'N', 'N'),
('W26-9100-0008', 4, 'HARV', '2026-09-29 21:00+00', NULL, 'CW-K7H7ZQ', NULL, 'N', 'N')
ON CONFLICT DO NOTHING;

INSERT INTO winch_mfg_control.wmatl (batch_no, step_no, lot_no, mat_cd, qty, uom) VALUES
('W26-1000-0031', 1, 'GML-ASA-26-117', 'RM1001', 21, 'kg'),
('W26-1000-0031', 1, 'WWE-MCC-2605-33', 'RM1002', 30, 'kg'),
('W26-1000-0031', 4, 'GML-FOIL-2605', 'PK0022', 1800, 'm'),
('W26-1010-0012', 1, 'GML-ASA-26-117', 'RM1001', 38, 'kg'),
('W26-1010-0012', 1, 'WWE-MCC-2605-33', 'RM1002', 25, 'kg'),
('W26-1010-0012', 4, 'GML-FOIL-2605', 'PK0022', 1100, 'm'),
('W26-5000-0024', 1, 'GML-RSV-26-042', 'RM5001', 1, 'kg'),
('W26-5000-0024', 1, 'WWE-MCC-2605-33', 'RM1002', 18, 'kg'),
('W26-5000-0024', 1, 'WWE-MGS-2608-07', 'RM1004', 1, 'kg'),
('W26-5000-0024', 4, 'GML-FOIL-2605', 'PK0022', 700, 'm'),
('W26-1000-0032', 1, 'GML-ASA-26-161', 'RM1001', 21, 'kg'),
('W26-1000-0032', 1, 'WWE-MCC-2605-33', 'RM1002', 30, 'kg'),
('W26-1000-0032', 4, 'GML-FOIL-2609', 'PK0022', 1800, 'm'),
('W26-5000-0025', 1, 'GML-RSV-26-042', 'RM5001', 1, 'kg'),
('W26-5000-0025', 1, 'WWE-MCC-2605-33', 'RM1002', 18, 'kg'),
('W26-5000-0025', 1, 'WWE-MGS-2608-07', 'RM1004', 1, 'kg'),
('W26-9100-0003', 2, 'BASE-LV19-2604C', 'RM9101', 1, 'vial'),
('W26-9100-0003', 3, 'BASE-CCM-2605A', 'RM9102', 12, 'L'),
('W26-9100-0004', 2, 'BASE-LV19-2604C', 'RM9101', 1, 'vial'),
('W26-9100-0004', 3, 'BASE-CCM-2605A', 'RM9102', 12, 'L'),
('W26-9100-0005', 2, 'BASE-LV19-2604C', 'RM9101', 1, 'vial'),
('W26-9100-0005', 3, 'BASE-CCM-2605A', 'RM9102', 12, 'L'),
('W26-9100-0007', 2, 'BASE-LV19-2607A', 'RM9101', 1, 'vial'),
('W26-9100-0007', 3, 'BASE-CCM-2605A', 'RM9102', 12, 'L'),
('W26-9100-0008', 2, 'BASE-LV19-2607A', 'RM9101', 1, 'vial'),
('W26-9100-0008', 3, 'BASE-CCM-2609B', 'RM9102', 12, 'L')
ON CONFLICT DO NOTHING;

INSERT INTO winch_mfg_control.wstep_eq (batch_no, step_no, eq_id, qual_at_use, cal_due) VALUES
('W26-1000-0031', 1, 'WIN-BAL-02', 'Q', '2027-01-31'),
('W26-1000-0031', 2, 'WIN-GRN-01', 'Q', '2027-01-31'),
('W26-1000-0031', 3, 'WIN-TAB-02', 'Q', '2027-01-31'),
('W26-1000-0031', 4, 'WIN-BLS-01', 'Q', '2027-01-31'),
('W26-1010-0012', 1, 'WIN-BAL-02', 'Q', '2027-01-31'),
('W26-1010-0012', 2, 'WIN-GRN-01', 'Q', '2027-01-31'),
('W26-1010-0012', 3, 'WIN-TAB-02', 'Q', '2027-01-31'),
('W26-1010-0012', 4, 'WIN-BLS-01', 'Q', '2027-01-31'),
('W26-5000-0024', 1, 'WIN-BAL-02', 'Q', '2027-01-31'),
('W26-5000-0024', 2, 'WIN-GRN-01', 'Q', '2027-01-31'),
('W26-5000-0024', 3, 'WIN-TAB-02', 'Q', '2027-01-31'),
('W26-5000-0024', 4, 'WIN-BLS-01', 'Q', '2027-01-31'),
('W26-1000-0032', 1, 'WIN-BAL-02', 'Q', '2027-01-31'),
('W26-1000-0032', 2, 'WIN-GRN-01', 'Q', '2027-01-31'),
('W26-1000-0032', 3, 'WIN-TAB-02', 'Q', '2027-01-31'),
('W26-1000-0032', 4, 'WIN-BLS-01', 'Q', '2027-01-31'),
('W26-5000-0025', 1, 'WIN-BAL-02', 'Q', '2027-01-31'),
('W26-5000-0025', 2, 'WIN-GRN-01', 'Q', '2027-01-31'),
('W26-9100-0003', 1, 'WIN-CLI-01', 'Q', '2027-01-31'),
('W26-9100-0003', 2, 'WIN-BSC-03', 'Q', '2027-01-31'),
('W26-9100-0003', 3, 'WIN-BIOR-01', 'Q', '2026-12-15'),
('W26-9100-0003', 4, 'WIN-CRF-01', 'Q', '2027-01-31'),
('W26-9100-0004', 1, 'WIN-CLI-01', 'Q', '2027-01-31'),
('W26-9100-0004', 2, 'WIN-BSC-03', 'Q', '2027-01-31'),
('W26-9100-0004', 3, 'WIN-BIOR-01', 'Q', '2026-12-15'),
('W26-9100-0004', 4, 'WIN-CRF-01', 'Q', '2027-01-31'),
('W26-9100-0005', 1, 'WIN-CLI-01', 'Q', '2027-01-31'),
('W26-9100-0005', 2, 'WIN-BSC-03', 'Q', '2027-01-31'),
('W26-9100-0005', 3, 'WIN-BIOR-01', 'Q', '2026-12-15'),
('W26-9100-0005', 4, 'WIN-CRF-01', 'Q', '2027-01-31'),
('W26-9100-0007', 1, 'WIN-CLI-01', 'Q', '2027-01-31'),
('W26-9100-0007', 2, 'WIN-BSC-03', 'Q', '2027-01-31'),
('W26-9100-0007', 3, 'WIN-BIOR-01', 'Q', '2026-12-15'),
('W26-9100-0007', 4, 'WIN-CRF-01', 'Q', '2027-01-31'),
('W26-9100-0008', 1, 'WIN-CLI-01', 'Q', '2027-01-31'),
('W26-9100-0008', 2, 'WIN-BSC-03', 'Q', '2027-01-31'),
('W26-9100-0008', 3, 'WIN-BIOR-01', 'Q', '2026-12-15'),
('W26-9100-0008', 4, 'WIN-CRF-01', 'Q', '2027-01-31')
ON CONFLICT DO NOTHING;

INSERT INTO winch_mfg_control.wdoc (batch_no, sect_ref, sect_typ, src_sys, rcvd_ts) VALUES
('W26-1000-0031', 'W26-1000-0031/EXEC', 'EXEC', 'winch-mfg-control', '2026-07-28 16:00+00'),
('W26-1000-0031', 'W26-1000-0031/PARAM', 'PARAM', 'winch-mfg-control', '2026-07-28 22:00+00'),
('W26-1000-0031', 'W26-1000-0031/LAB', 'LAB', 'Winchester QC laboratory (paper)', '2026-08-01 16:00+00'),
('W26-1000-0031', 'W26-1000-0031/SIGN', 'SIGN', 'winch-mfg-control', '2026-08-06 08:00+00'),
('W26-1010-0012', 'W26-1010-0012/EXEC', 'EXEC', 'winch-mfg-control', '2026-08-11 15:30+00'),
('W26-1010-0012', 'W26-1010-0012/PARAM', 'PARAM', 'winch-mfg-control', '2026-08-11 21:30+00'),
('W26-1010-0012', 'W26-1010-0012/LAB', 'LAB', 'Winchester QC laboratory (paper)', '2026-08-15 15:30+00'),
('W26-1010-0012', 'W26-1010-0012/SIGN', 'SIGN', 'winch-mfg-control', '2026-08-20 08:00+00'),
('W26-5000-0024', 'W26-5000-0024/EXEC', 'EXEC', 'winch-mfg-control', '2026-08-25 17:00+00'),
('W26-5000-0024', 'W26-5000-0024/PARAM', 'PARAM', 'winch-mfg-control', '2026-08-25 23:00+00'),
('W26-5000-0024', 'W26-5000-0024/LAB', 'LAB', 'Winchester QC laboratory (paper)', '2026-08-29 17:00+00'),
('W26-5000-0024', 'W26-5000-0024/DEV', 'DEV', 'Coco QA deviation log', '2026-08-30 17:00+00'),
('W26-5000-0024', 'W26-5000-0024/SIGN', 'SIGN', 'winch-mfg-control', '2026-09-08 08:00+00'),
('W26-1000-0032', 'W26-1000-0032/EXEC', 'EXEC', 'winch-mfg-control', '2026-09-15 16:00+00'),
('W26-1000-0032', 'W26-1000-0032/PARAM', 'PARAM', 'winch-mfg-control', '2026-09-15 22:00+00'),
('W26-1000-0032', 'W26-1000-0032/LAB', 'LAB', 'Winchester QC laboratory (paper)', '2026-09-19 16:00+00'),
('W26-5000-0025', 'W26-5000-0025/EXEC', 'EXEC', 'winch-mfg-control', '2026-09-30 08:00+00'),
('W26-9100-0003', 'W26-9100-0003/EXEC', 'EXEC', 'winch-mfg-control', '2026-06-05 17:00+00'),
('W26-9100-0003', 'W26-9100-0003/PARAM', 'PARAM', 'winch-mfg-control', '2026-06-05 23:00+00'),
('W26-9100-0003', 'W26-9100-0003/LAB', 'LAB', 'Winchester QC laboratory (paper)', '2026-06-06 17:00+00'),
('W26-9100-0003', 'W26-9100-0003/SIGN', 'SIGN', 'winch-mfg-control', '2026-06-08 08:00+00'),
('W26-9100-0004', 'W26-9100-0004/EXEC', 'EXEC', 'winch-mfg-control', '2026-06-26 16:00+00'),
('W26-9100-0004', 'W26-9100-0004/PARAM', 'PARAM', 'winch-mfg-control', '2026-06-26 22:00+00'),
('W26-9100-0004', 'W26-9100-0004/LAB', 'LAB', 'Winchester QC laboratory (paper)', '2026-06-27 16:00+00'),
('W26-9100-0004', 'W26-9100-0004/SIGN', 'SIGN', 'winch-mfg-control', '2026-06-29 08:00+00'),
('W26-9100-0005', 'W26-9100-0005/EXEC', 'EXEC', 'winch-mfg-control', '2026-07-17 15:00+00'),
('W26-9100-0005', 'W26-9100-0005/PARAM', 'PARAM', 'winch-mfg-control', '2026-07-17 21:00+00'),
('W26-9100-0005', 'W26-9100-0005/LAB', 'LAB', 'Winchester QC laboratory (paper)', '2026-07-18 15:00+00'),
('W26-9100-0005', 'W26-9100-0005/EXC', 'EXC', 'Coco QA deviation log', '2026-07-19 15:00+00'),
('W26-9100-0005', 'W26-9100-0005/SIGN', 'SIGN', 'winch-mfg-control', '2026-07-21 08:00+00'),
('W26-9100-0007', 'W26-9100-0007/EXEC', 'EXEC', 'winch-mfg-control', '2026-08-14 16:00+00'),
('W26-9100-0007', 'W26-9100-0007/PARAM', 'PARAM', 'winch-mfg-control', '2026-08-14 22:00+00'),
('W26-9100-0007', 'W26-9100-0007/LAB', 'LAB', 'Winchester QC laboratory (paper)', '2026-08-15 16:00+00'),
('W26-9100-0007', 'W26-9100-0007/SIGN', 'SIGN', 'winch-mfg-control', '2026-08-18 08:00+00'),
('W26-9100-0008', 'W26-9100-0008/EXEC', 'EXEC', 'winch-mfg-control', '2026-09-30 08:00+00')
ON CONFLICT DO NOTHING;

INSERT INTO winch_mfg_control.wrel (batch_no, mkt, rel_qty, cert_dt, qp_psn) VALUES
('W26-1000-0031', 'UK', 150000, '2026-08-06', 'CW-B76CPN'),
('W26-1000-0031', 'NL', 100000, '2026-08-06', 'CW-B76CPN'),
('W26-1010-0012', 'UK', 90000, '2026-08-20', 'CW-B76CPN'),
('W26-1010-0012', 'NL', 60000, '2026-08-20', 'CW-B76CPN'),
('W26-5000-0024', 'UK', 50000, '2026-09-08', 'CW-B76CPN'),
('W26-5000-0024', 'NL', 40000, '2026-09-08', 'CW-B76CPN'),
('W26-9100-0003', 'US', 1, '2026-06-08', 'CW-B76CPN'),
('W26-9100-0004', 'US', 1, '2026-06-29', 'CW-B76CPN'),
('W26-9100-0005', 'US', 1, '2026-07-21', 'CW-B76CPN'),
('W26-9100-0007', 'US', 1, '2026-08-18', 'CW-B76CPN')
ON CONFLICT DO NOTHING;


-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS winch_mfg_control.wdev (
  dev_ref varchar(40) NOT NULL,
  batch_no varchar(20),
  prd_cd varchar(20),
  raised_ts timestamptz NOT NULL,
  src_typ varchar(100) NOT NULL,
  dev_txt text NOT NULL,
  sev varchar(20) NOT NULL,
  dev_sts varchar(20) NOT NULL,
  inv_by varchar(40),
  inv_dt date,
  root_cause text,
  impact text,
  disp varchar(40),
  CONSTRAINT wdev_pk PRIMARY KEY (dev_ref)
);
COMMENT ON TABLE winch_mfg_control.wdev IS 'Deviations against Winchester batches received from the QMS (Deviations And CAPAs), with the investigation outcome and disposition the QP needs before certifying the batch.';

CREATE TABLE IF NOT EXISTS winch_mfg_control.weq_qual (
  eq_id varchar(40) NOT NULL,
  eq_nm varchar(120),
  eq_typ varchar(60),
  eq_sts varchar(20),
  qual_sts varchar(20),
  qual_dt date,
  qual_end date,
  cal_dt date,
  cal_end date,
  CONSTRAINT weq_qual_pk PRIMARY KEY (eq_id)
);
COMMENT ON TABLE winch_mfg_control.weq_qual IS 'Qualification and calibration status of Winchester equipment (Equipment Qualification Status), checked when a step is started.';

CREATE TABLE IF NOT EXISTS winch_mfg_control.wmat_iss (
  mvmt_ref varchar(40) NOT NULL,
  batch_no varchar(20) NOT NULL,
  mat_cd varchar(20) NOT NULL,
  lot_no varchar(40) NOT NULL,
  qty integer NOT NULL,
  q_sts char(1) NOT NULL,
  CONSTRAINT wmat_iss_pk PRIMARY KEY (mvmt_ref)
);
COMMENT ON TABLE winch_mfg_control.wmat_iss IS 'Material lots issued from stores to Winchester batches (Goods Inventory Stock), reconciled against the lots consumed in wmatl. q_sts R released, H held, X rejected at issue.';

CREATE TABLE IF NOT EXISTS winch_mfg_control.wlab_smpl (
  smpl_ref varchar(40) NOT NULL,
  smpl_typ varchar(20) NOT NULL,
  batch_no varchar(20) NOT NULL,
  coll_ts timestamptz NOT NULL,
  smpl_sts varchar(20) NOT NULL,
  CONSTRAINT wlab_smpl_pk PRIMARY KEY (smpl_ref)
);
COMMENT ON TABLE winch_mfg_control.wlab_smpl IS 'In-process and finished product samples of Winchester batches whose results come from a laboratory system (Laboratory Test Results).';

CREATE TABLE IF NOT EXISTS winch_mfg_control.wlab_res (
  res_ref varchar(40) NOT NULL,
  smpl_ref varchar(40) NOT NULL,
  test_cd varchar(40) NOT NULL,
  res_val varchar(60) NOT NULL,
  res_uom varchar(20),
  spec_lo varchar(60),
  spec_hi varchar(60),
  pass_flg char(1) NOT NULL,
  done_ts timestamptz NOT NULL,
  analyst varchar(40) NOT NULL,
  CONSTRAINT wlab_res_pk PRIMARY KEY (res_ref)
);
COMMENT ON TABLE winch_mfg_control.wlab_res IS 'Test results of the samples in wlab_smpl; pass_flg Y/N.';

CREATE TABLE IF NOT EXISTS winch_mfg_control.wlab_coa (
  coa_ref varchar(40) NOT NULL,
  batch_no varchar(20) NOT NULL,
  coa_dt date NOT NULL,
  conform_flg char(1) NOT NULL,
  approver varchar(40) NOT NULL,
  CONSTRAINT wlab_coa_pk PRIMARY KEY (coa_ref)
);
COMMENT ON TABLE winch_mfg_control.wlab_coa IS 'Certificates of analysis issued for Winchester batches.';

CREATE TABLE IF NOT EXISTS winch_mfg_control.wsched (
  batch_no varchar(20) NOT NULL,
  cust_ord varchar(40) NOT NULL,
  psn_ref varchar(40) NOT NULL,
  prd_cd varchar(20) NOT NULL,
  slot_st timestamptz NOT NULL,
  slot_en timestamptz NOT NULL,
  pt_params text,
  slot_sts varchar(20) NOT NULL,
  CONSTRAINT wsched_pk PRIMARY KEY (batch_no)
);
COMMENT ON TABLE winch_mfg_control.wsched IS 'Personalised manufacturing slots planned for Winchester (Personalised Manufacturing Schedule); a wbatch header is opened from the slot when manufacture starts.';

CREATE TABLE IF NOT EXISTS winch_mfg_control.wparam (
  eq_id varchar(40) NOT NULL,
  param_cd varchar(40) NOT NULL,
  read_ts timestamptz NOT NULL,
  batch_no varchar(20),
  val double precision NOT NULL,
  uom varchar(20) NOT NULL,
  lo double precision,
  hi double precision,
  CONSTRAINT wparam_pk PRIMARY KEY (eq_id, param_cd, read_ts)
);
COMMENT ON TABLE winch_mfg_control.wparam IS 'Process parameter readings from Winchester equipment (Process Parameter Time Series) for the PARAM section of the batch record.';

CREATE TABLE IF NOT EXISTS winch_mfg_control.wexc (
  exc_ref varchar(40) NOT NULL,
  ship_ref varchar(40) NOT NULL,
  prd_cd varchar(20) NOT NULL,
  batch_no varchar(20) NOT NULL,
  assessor varchar(40) NOT NULL,
  assess_ts timestamptz NOT NULL,
  stab_ref varchar(40) NOT NULL,
  disp varchar(20) NOT NULL,
  notes text,
  CONSTRAINT wexc_pk PRIMARY KEY (exc_ref)
);
COMMENT ON TABLE winch_mfg_control.wexc IS 'Temperature excursion assessments of shipments from Winchester batches (Temperature Excursion Assessments), recorded in the EXC section of the batch record.';

CREATE TABLE IF NOT EXISTS winch_mfg_control.wopr_qual (
  psn_ref varchar(20) NOT NULL,
  comp_cd varchar(40) NOT NULL,
  comp_nm varchar(120) NOT NULL,
  start_dt date NOT NULL,
  exp_dt date NOT NULL,
  qual_sts varchar(20) NOT NULL,
  trn_ref varchar(40) NOT NULL,
  cert_no varchar(40),
  role_cd varchar(40) NOT NULL,
  CONSTRAINT wopr_qual_pk PRIMARY KEY (psn_ref, comp_cd)
);
COMMENT ON TABLE winch_mfg_control.wopr_qual IS 'Qualifications of the people who sign Winchester batch records (Worker Qualifications), checked before a step or QP certification is signed.';

-- End of subscription tables.

GRANT USAGE ON SCHEMA winch_mfg_control TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA winch_mfg_control TO egeria_user, airflow_user;
