-- system-qualified-name: System::coco-inventory
-- Coco Inventory - Coco core.  Homegrown inventory for raw materials and products at every Coco site except Austin; feeds Goods Receipts (inspection results), Material Quarantine Dispositions and Goods Inventory Stock.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS coco_inventory;
COMMENT ON SCHEMA coco_inventory IS 'Coco Inventory (Coco core): locations, items, balances, transactions, receipt inspections and quarantine.';

CREATE TABLE IF NOT EXISTS coco_inventory.inv_loc (
  loc_cd varchar(10) NOT NULL,
  site_cd varchar(4) NOT NULL,
  loc_typ varchar(4) NOT NULL,
  loc_desc varchar(60),
  CONSTRAINT inv_loc_pk PRIMARY KEY (loc_cd)
);
COMMENT ON TABLE coco_inventory.inv_loc IS 'Stock locations at every Coco site except Austin.';

CREATE TABLE IF NOT EXISTS coco_inventory.inv_item (
  item_cd varchar(10) NOT NULL,
  item_desc varchar(80) NOT NULL,
  item_cls varchar(2) NOT NULL,
  base_uom varchar(6) NOT NULL,
  CONSTRAINT inv_item_pk PRIMARY KEY (item_cd)
);
COMMENT ON TABLE coco_inventory.inv_item IS 'Items held: RM raw material, PK packaging, FG finished goods (product code).';

CREATE TABLE IF NOT EXISTS coco_inventory.inv_bal (
  item_cd varchar(10) NOT NULL,
  loc_cd varchar(10) NOT NULL,
  lot_no varchar(30) NOT NULL,
  on_hand integer NOT NULL,
  min_lvl integer,
  max_lvl integer,
  upd_ts timestamptz NOT NULL,
  CONSTRAINT inv_bal_pk PRIMARY KEY (item_cd, loc_cd, lot_no)
);
COMMENT ON TABLE coco_inventory.inv_bal IS 'Stock balance per item, location and lot (''-'' where not lot-tracked); min/max levels are held on one of the item''s lots at each location.';

CREATE TABLE IF NOT EXISTS coco_inventory.inv_txn (
  txn_id varchar(12) NOT NULL,
  txn_typ varchar(4) NOT NULL,
  item_cd varchar(10) NOT NULL,
  lot_no varchar(30),
  qty integer NOT NULL,
  txn_ts timestamptz NOT NULL,
  loc_cd varchar(10) NOT NULL,
  batch_ref varchar(20),
  src_ref varchar(30),
  q_sts_at_txn char(1),
  CONSTRAINT inv_txn_pk PRIMARY KEY (txn_id)
);
COMMENT ON TABLE coco_inventory.inv_txn IS 'Stock transactions since the V5.2 cut-over on 2026-08-15. txn_typ RCPT, ISS, XFR, ADJ, SHIP; qty signed (negative out); batch_ref set on issues to manufacturing.';

CREATE TABLE IF NOT EXISTS coco_inventory.inv_insp (
  grn_ref varchar(20) NOT NULL,
  insp_dt date NOT NULL,
  inspector varchar(20) NOT NULL,
  result varchar(4) NOT NULL,
  notes text,
  CONSTRAINT inv_insp_pk PRIMARY KEY (grn_ref, insp_dt)
);
COMMENT ON TABLE coco_inventory.inv_insp IS 'Receipt inspection results recorded against the depot''s goods receipt reference. result ACC, REJ, HOLD.';

CREATE TABLE IF NOT EXISTS coco_inventory.inv_qrn (
  lot_no varchar(30) NOT NULL,
  item_cd varchar(10) NOT NULL,
  grn_ref varchar(20) NOT NULL,
  q_start_ts timestamptz NOT NULL,
  loc_cd varchar(10) NOT NULL,
  qty integer NOT NULL,
  smpl_ref varchar(20),
  q_sts char(1) NOT NULL,
  CONSTRAINT inv_qrn_pk PRIMARY KEY (lot_no)
);
COMMENT ON TABLE coco_inventory.inv_qrn IS 'Lots placed in quarantine on receipt. q_sts H held, R released, X rejected.';

CREATE TABLE IF NOT EXISTS coco_inventory.inv_qdisp (
  lot_no varchar(30) NOT NULL,
  disp_ts timestamptz NOT NULL,
  disp varchar(3) NOT NULL,
  lab_ref varchar(20) NOT NULL,
  exp_dt date,
  rel_qty integer,
  CONSTRAINT inv_qdisp_pk PRIMARY KEY (lot_no, disp_ts)
);
COMMENT ON TABLE coco_inventory.inv_qdisp IS 'Quarantine decisions. disp REL released, REJ rejected, HLD interim hold (not a disposition).';

INSERT INTO coco_inventory.inv_loc (loc_cd, site_cd, loc_typ, loc_desc) VALUES
('WIN-RM01', 'WIN', 'RM', 'Winchester raw material store'),
('WIN-CELL', 'WIN', 'CELL', 'Winchester cell therapy cold store'),
('WIN-QUAR', 'WIN', 'QUAR', 'Winchester quarantine store'),
('WIN-FG01', 'WIN', 'FG', 'Winchester finished goods'),
('EDM-RM01', 'EDM', 'RM', 'Edmonton raw material store'),
('EDM-PK01', 'EDM', 'PK', 'Edmonton packaging store'),
('EDM-QUAR', 'EDM', 'QUAR', 'Edmonton quarantine cage'),
('EDM-FG01', 'EDM', 'FG', 'Edmonton finished goods'),
('KC-DC01', 'KCY', 'DC', 'Kansas City distribution centre')
ON CONFLICT DO NOTHING;

INSERT INTO coco_inventory.inv_item (item_cd, item_desc, item_cls, base_uom) VALUES
('RM1001', 'Acetylsalicylic acid', 'RM', 'kg'),
('RM1002', 'Microcrystalline cellulose', 'RM', 'kg'),
('RM1004', 'Magnesium stearate', 'RM', 'kg'),
('RM2001', 'Amlodipine besylate', 'RM', 'kg'),
('RM4001', 'Metoprolol succinate', 'RM', 'kg'),
('RM5001', 'Rosuvastatin calcium', 'RM', 'kg'),
('RM9101', 'Lentiviral vector LV-CD19', 'RM', 'vial'),
('RM9102', 'T-cell expansion medium', 'RM', 'L'),
('PK0020', 'Plastic pill bottles', 'PK', 'case'),
('PK0021', 'Glass vials 50mL', 'PK', 'case'),
('PK0022', 'Aluminium blister foil', 'PK', 'm'),
('PK0024', 'Cardboard shipping boxes', 'PK', 'case'),
('1000', 'Asprin 81mg', 'FG', 'EA'),
('1010', 'Asprin 250mg', 'FG', 'EA'),
('2000', 'Norvasc 10mg', 'FG', 'EA'),
('2010', 'Norvasc 5mg', 'FG', 'EA'),
('2050', 'Plavix 75mg', 'FG', 'EA'),
('3000', 'Cozaar 100mg', 'FG', 'EA'),
('4000', 'Toprol-XL 50mg', 'FG', 'EA'),
('4010', 'Toprol-XL 25mg', 'FG', 'EA'),
('5000', 'Crestor 5mg', 'FG', 'EA'),
('9000', 'Cisplatin 50mg', 'FG', 'EA'),
('9100', 'Cocolecel 1-5 x 10^8 CAR+ T cells', 'FG', 'EA')
ON CONFLICT DO NOTHING;

INSERT INTO coco_inventory.inv_bal (item_cd, loc_cd, lot_no, on_hand, min_lvl, max_lvl, upd_ts) VALUES
('RM1001', 'WIN-RM01', 'GML-ASA-26-161', 479, 200, 1200, '2026-09-14 05:00+00'),
('RM1001', 'WIN-RM01', 'GML-ASA-26-117', 441, 200, 1200, '2026-08-10 05:00+00'),
('RM1002', 'WIN-RM01', 'WWE-MCC-2605-33', 1079, 400, 2400, '2026-09-29 05:00+00'),
('RM1004', 'WIN-RM01', 'WWE-MGS-2608-07', 148, 40, 300, '2026-09-29 05:00+00'),
('RM5001', 'WIN-RM01', 'GML-RSV-26-042', 78, 20, 120, '2026-09-29 05:00+00'),
('PK0022', 'WIN-RM01', 'GML-FOIL-2609', 18200, 5000, 40000, '2026-09-15 05:00+00'),
('RM9101', 'WIN-CELL', 'BASE-LV19-2607A', 38, 10, 60, '2026-09-24 19:00+00'),
('RM9102', 'WIN-CELL', 'BASE-CCM-2609B', 188, 50, 400, '2026-09-27 07:00+00'),
('1000', 'WIN-FG01', 'W26-1000-0032', 250000, NULL, NULL, '2026-09-15 16:00+00'),
('5000', 'WIN-FG01', '-', 0, 20000, 150000, '2026-09-10 09:00+00'),
('1010', 'WIN-FG01', 'W26-1010-0012', 30000, 20000, 200000, '2026-09-02 11:00+00'),
('RM2001', 'EDM-RM01', 'GG-AML-26-0251', 147, 50, 400, '2026-09-21 11:00+00'),
('RM4001', 'EDM-RM01', 'GG-MET-26-0077', 291, 100, 600, '2026-09-01 11:00+00'),
('RM1002', 'EDM-RM01', 'WWE-MCC-2607-12', 1366, 400, 3000, '2026-09-21 11:00+00'),
('PK0020', 'EDM-PK01', 'GML-BTL-2608', 10, 10, 80, '2026-09-22 11:00+00'),
('RM4001', 'EDM-QUAR', 'GG-MET-26-0118', 300, NULL, NULL, '2026-09-21 20:00+00'),
('2000', 'EDM-FG01', 'E26-2000-0045', 180000, NULL, NULL, '2026-09-23 02:00+00'),
('4010', 'EDM-FG01', 'E26-4010-0011', 0, 10000, 150000, '2026-09-12 16:00+00'),
('2000', 'KC-DC01', 'E26-2000-0044', 24000, 10000, 100000, '2026-09-25 18:00+00'),
('4000', 'KC-DC01', 'E26-4000-0027', 18000, 8000, 60000, '2026-09-25 18:00+00'),
('4010', 'KC-DC01', 'E26-4010-0011', 50000, 8000, 60000, '2026-09-16 18:00+00'),
('3000', 'KC-DC01', 'A26-3000-0141', 41000, 10000, 80000, '2026-09-25 18:00+00'),
('2050', 'KC-DC01', 'A26-2050-0087', 52000, 10000, 80000, '2026-09-25 18:00+00'),
('9000', 'KC-DC01', 'A26-9000-0019', 1500, 300, 3000, '2026-09-29 13:30+00'),
('PK0021', 'KC-DC01', 'GML-VIAL-2606', 60, 10, 100, '2026-06-12 18:00+00'),
('PK0024', 'KC-DC01', 'GML-BOX-2608', 64, 20, 200, '2026-09-24 18:00+00'),
('PK0020', 'KC-DC01', 'TT-BTL-2609', 50, 10, 100, '2026-09-10 18:00+00')
ON CONFLICT DO NOTHING;

INSERT INTO coco_inventory.inv_txn (txn_id, txn_typ, item_cd, lot_no, qty, txn_ts, loc_cd, batch_ref, src_ref, q_sts_at_txn) VALUES
('T260401', 'RCPT', 'RM1004', 'WWE-MGS-2608-07', 150, '2026-08-19 14:00+00', 'WIN-RM01', NULL, 'WDR-260819/1', NULL),
('T260402', 'RCPT', 'PK0022', 'GML-FOIL-2609', 20000, '2026-09-02 14:00+00', 'WIN-RM01', NULL, 'WDR-260902/1', NULL),
('T260403', 'RCPT', 'RM9102', 'BASE-CCM-2609B', 200, '2026-09-16 14:00+00', 'WIN-CELL', NULL, 'WDR-260916/1', NULL),
('T260404', 'RCPT', 'PK0020', 'GML-BTL-2608', 40, '2026-08-31 14:00+00', 'EDM-PK01', NULL, 'ED-GR-26-0084', NULL),
('T260405', 'RCPT', 'RM4001', 'GG-MET-26-0118', 300, '2026-09-21 14:00+00', 'EDM-QUAR', NULL, 'ED-GR-26-0088', NULL),
('T260406', 'RCPT', 'PK0024', 'GML-BOX-2608', 100, '2026-08-18 14:00+00', 'KC-DC01', NULL, 'KC260818-02', NULL),
('T260407', 'RCPT', 'PK0020', 'TT-BTL-2609', 50, '2026-09-09 14:00+00', 'KC-DC01', NULL, 'KC260909-01', NULL),
('T260408', 'ISS', 'RM5001', 'GML-RSV-26-042', -1, '2026-08-24 05:00+00', 'WIN-RM01', 'W26-5000-0024', NULL, 'R'),
('T260409', 'ISS', 'RM1002', 'WWE-MCC-2605-33', -18, '2026-08-24 05:00+00', 'WIN-RM01', 'W26-5000-0024', NULL, 'R'),
('T260410', 'ISS', 'RM1004', 'WWE-MGS-2608-07', -1, '2026-08-24 05:00+00', 'WIN-RM01', 'W26-5000-0024', NULL, 'R'),
('T260411', 'ISS', 'PK0022', 'GML-FOIL-2605', -700, '2026-08-24 14:00+00', 'WIN-RM01', 'W26-5000-0024', NULL, 'R'),
('T260412', 'ISS', 'RM1001', 'GML-ASA-26-161', -21, '2026-09-14 05:00+00', 'WIN-RM01', 'W26-1000-0032', NULL, 'R'),
('T260413', 'ISS', 'RM1002', 'WWE-MCC-2605-33', -30, '2026-09-14 05:00+00', 'WIN-RM01', 'W26-1000-0032', NULL, 'R'),
('T260414', 'ISS', 'PK0022', 'GML-FOIL-2609', -1800, '2026-09-14 14:00+00', 'WIN-RM01', 'W26-1000-0032', NULL, 'R'),
('T260415', 'ISS', 'RM5001', 'GML-RSV-26-042', -1, '2026-09-29 05:00+00', 'WIN-RM01', 'W26-5000-0025', NULL, 'R'),
('T260416', 'ISS', 'RM1002', 'WWE-MCC-2605-33', -18, '2026-09-29 05:00+00', 'WIN-RM01', 'W26-5000-0025', NULL, 'R'),
('T260417', 'ISS', 'RM1004', 'WWE-MGS-2608-07', -1, '2026-09-29 05:00+00', 'WIN-RM01', 'W26-5000-0025', NULL, 'R'),
('T260418', 'ISS', 'RM9101', 'BASE-LV19-2607A', -1, '2026-09-22 10:00+00', 'WIN-CELL', 'W26-9100-0008', NULL, 'R'),
('T260419', 'ISS', 'RM9102', 'BASE-CCM-2609B', -12, '2026-09-22 13:00+00', 'WIN-CELL', 'W26-9100-0008', NULL, 'R'),
('T260420', 'ISS', 'RM2001', 'GG-AML-26-0192', -2, '2026-08-18 11:00+00', 'EDM-RM01', 'E26-2010-0019', NULL, 'R'),
('T260421', 'ISS', 'RM1002', 'WWE-MCC-2607-12', -28, '2026-08-18 11:00+00', 'EDM-RM01', 'E26-2010-0019', NULL, 'R'),
('T260422', 'ISS', 'PK0020', 'GML-BTL-2605', -30, '2026-08-18 20:00+00', 'EDM-PK01', 'E26-2010-0019', NULL, 'R'),
('T260423', 'ISS', 'RM4001', 'GG-MET-26-0077', -3, '2026-09-01 11:00+00', 'EDM-RM01', 'E26-4010-0011', NULL, 'R'),
('T260424', 'ISS', 'RM1002', 'WWE-MCC-2607-12', -22, '2026-09-01 11:00+00', 'EDM-RM01', 'E26-4010-0011', NULL, 'R'),
('T260425', 'ISS', 'PK0020', 'GML-BTL-2608', -20, '2026-09-01 20:00+00', 'EDM-PK01', 'E26-4010-0011', NULL, 'R'),
('T260426', 'ISS', 'RM2001', 'GG-AML-26-0251', -3, '2026-09-21 11:00+00', 'EDM-RM01', 'E26-2000-0045', NULL, 'R'),
('T260427', 'ISS', 'RM1002', 'WWE-MCC-2607-12', -30, '2026-09-21 11:00+00', 'EDM-RM01', 'E26-2000-0045', NULL, 'R'),
('T260428', 'ISS', 'PK0020', 'GML-BTL-2608', -30, '2026-09-21 20:00+00', 'EDM-PK01', 'E26-2000-0045', NULL, 'R'),
('T260429', 'XFR', '2000', 'E26-2000-0044', -60000, '2026-08-20 15:00+00', 'EDM-FG01', NULL, 'KC-DC01', NULL),
('T260430', 'XFR', '2000', 'E26-2000-0044', 60000, '2026-08-24 18:00+00', 'KC-DC01', NULL, 'EDM-FG01', NULL),
('T260431', 'SHIP', '9000', 'A26-9000-0019', -250, '2026-09-18 13:10+00', 'KC-DC01', NULL, NULL, NULL),
('T260432', 'SHIP', '9000', 'A26-9000-0019', -100, '2026-09-21 12:45+00', 'KC-DC01', NULL, NULL, NULL),
('T260433', 'SHIP', '9000', 'A26-9000-0019', -100, '2026-09-24 14:00+00', 'KC-DC01', NULL, NULL, NULL),
('T260434', 'SHIP', '9000', 'A26-9000-0019', -50, '2026-09-29 13:30+00', 'KC-DC01', NULL, NULL, NULL),
('T260435', 'ADJ', 'PK0020', 'GML-BTL-2608', -2, '2026-09-22 11:00+00', 'EDM-PK01', NULL, 'Cycle count', NULL)
ON CONFLICT DO NOTHING;

INSERT INTO coco_inventory.inv_insp (grn_ref, insp_dt, inspector, result, notes) VALUES
('WDR-260603/1', '2026-06-03', 'CW-7G8SM2', 'ACC', 'Seals intact, CoA matches lot'),
('WDR-260610/1', '2026-06-10', 'CW-7G8SM2', 'ACC', NULL),
('WDR-260701/1', '2026-07-01', 'CW-7G8SM2', 'ACC', NULL),
('WDR-260715/1', '2026-07-15', 'CW-7G8SM2', 'ACC', 'Received frozen on dry ice, logger in range'),
('WDR-260805/1', '2026-08-05', 'CW-7G8SM2', 'ACC', NULL),
('WDR-260819/1', '2026-08-19', 'CW-7G8SM2', 'ACC', NULL),
('WDR-260902/1', '2026-09-02', 'CW-7G8SM2', 'ACC', 'Certificate of conformance only'),
('WDR-260916/1', '2026-09-16', 'CW-7G8SM2', 'ACC', NULL),
('ED-GR-26-0061', '2026-06-08', 'CW-GBAX2A', 'ACC', NULL),
('ED-GR-26-0067', '2026-06-22', 'CW-GBAX2A', 'ACC', NULL),
('ED-GR-26-0072', '2026-07-13', 'CW-GBAX2A', 'ACC', NULL),
('ED-GR-26-0079', '2026-08-10', 'CW-GBAX2A', 'HOLD', 'Drum 3 of 6 label damaged; held pending supplier confirmation'),
('ED-GR-26-0084', '2026-08-31', 'CW-GBAX2A', 'ACC', NULL),
('ED-GR-26-0088', '2026-09-21', 'CW-GBAX2A', 'ACC', NULL),
('KC260612-01', '2026-06-12', 'CW-PLYYBU', 'ACC', NULL),
('KC260714-01', '2026-07-15', 'CW-PLYYBU', 'REJ', 'Boxes crushed in transit; returned to supplier'),
('KC260818-02', '2026-08-18', 'CW-PLYYBU', 'ACC', NULL),
('KC260909-01', '2026-09-10', 'CW-PLYYBU', 'ACC', NULL)
ON CONFLICT DO NOTHING;

INSERT INTO coco_inventory.inv_qrn (lot_no, item_cd, grn_ref, q_start_ts, loc_cd, qty, smpl_ref, q_sts) VALUES
('GML-ASA-26-117', 'RM1001', 'WDR-260603/1', '2026-06-03 15:00+00', 'WIN-QUAR', 500, 'SMP-W-26-0301', 'R'),
('WWE-MCC-2605-33', 'RM1002', 'WDR-260610/1', '2026-06-10 15:00+00', 'WIN-QUAR', 1200, 'SMP-W-26-0307', 'R'),
('GML-RSV-26-042', 'RM5001', 'WDR-260701/1', '2026-07-01 15:00+00', 'WIN-QUAR', 80, 'SMP-W-26-0322', 'R'),
('BASE-LV19-2607A', 'RM9101', 'WDR-260715/1', '2026-07-15 15:00+00', 'WIN-CELL', 40, 'SMP-W-26-0331', 'R'),
('GML-ASA-26-161', 'RM1001', 'WDR-260805/1', '2026-08-05 15:00+00', 'WIN-QUAR', 500, 'SMP-W-26-0349', 'R'),
('WWE-MGS-2608-07', 'RM1004', 'WDR-260819/1', '2026-08-19 15:00+00', 'WIN-QUAR', 150, 'SMP-W-26-0358', 'R'),
('GML-FOIL-2609', 'PK0022', 'WDR-260902/1', '2026-09-02 15:00+00', 'WIN-QUAR', 20000, 'SMP-W-26-0366', 'R'),
('BASE-CCM-2609B', 'RM9102', 'WDR-260916/1', '2026-09-16 15:00+00', 'WIN-CELL', 200, 'SMP-W-26-0374', 'R'),
('GG-AML-26-0192', 'RM2001', 'ED-GR-26-0061', '2026-06-08 15:00+00', 'EDM-QUAR', 150, 'SMP-E-26-0112', 'R'),
('GG-MET-26-0077', 'RM4001', 'ED-GR-26-0067', '2026-06-22 15:00+00', 'EDM-QUAR', 300, 'SMP-E-26-0119', 'R'),
('WWE-MCC-2607-12', 'RM1002', 'ED-GR-26-0072', '2026-07-13 15:00+00', 'EDM-QUAR', 1500, 'SMP-E-26-0127', 'R'),
('GG-AML-26-0251', 'RM2001', 'ED-GR-26-0079', '2026-08-10 15:00+00', 'EDM-QUAR', 150, 'SMP-E-26-0138', 'R'),
('GML-BTL-2608', 'PK0020', 'ED-GR-26-0084', '2026-08-31 15:00+00', 'EDM-QUAR', 40, 'SMP-E-26-0144', 'R'),
('GG-MET-26-0118', 'RM4001', 'ED-GR-26-0088', '2026-09-21 15:00+00', 'EDM-QUAR', 300, 'SMP-E-26-0151', 'H')
ON CONFLICT DO NOTHING;

INSERT INTO coco_inventory.inv_qdisp (lot_no, disp_ts, disp, lab_ref, exp_dt, rel_qty) VALUES
('GML-ASA-26-117', '2026-06-09 11:00+00', 'REL', 'QC-WIN-26-0211', '2028-05-31', 500),
('WWE-MCC-2605-33', '2026-06-15 11:00+00', 'REL', 'QC-WIN-26-0219', '2029-04-30', 1200),
('GML-RSV-26-042', '2026-07-08 11:00+00', 'REL', 'QC-WIN-26-0240', '2028-06-30', 80),
('BASE-LV19-2607A', '2026-07-24 11:00+00', 'REL', 'QC-WIN-26-0252', '2027-07-31', 40),
('GML-ASA-26-161', '2026-08-11 11:00+00', 'REL', 'QC-WIN-26-0277', '2028-07-31', 500),
('WWE-MGS-2608-07', '2026-08-22 11:00+00', 'REL', 'QC-WIN-26-0284', '2029-07-31', 150),
('GML-FOIL-2609', '2026-09-04 11:00+00', 'REL', 'QC-WIN-26-0291', NULL, 20000),
('BASE-CCM-2609B', '2026-09-24 11:00+00', 'REL', 'QC-WIN-26-0305', '2027-03-31', 200),
('GG-AML-26-0192', '2026-06-15 11:00+00', 'REL', 'QC-EDM-26-0088', '2028-05-31', 150),
('GG-MET-26-0077', '2026-06-28 11:00+00', 'REL', 'QC-EDM-26-0093', '2028-06-30', 300),
('WWE-MCC-2607-12', '2026-07-17 11:00+00', 'REL', 'QC-EDM-26-0101', '2029-06-30', 1500),
('GG-AML-26-0251', '2026-08-19 11:00+00', 'REL', 'QC-EDM-26-0112', '2028-07-31', 150),
('GML-BTL-2608', '2026-09-01 11:00+00', 'REL', 'QC-EDM-26-0118', NULL, 40),
('GG-AML-26-0251', '2026-08-14 16:00+00', 'HLD', 'QC-EDM-26-0109', NULL, NULL)
ON CONFLICT DO NOTHING;


-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS coco_inventory.inv_rcpt_ntf (
  grn_ref varchar(40) NOT NULL,
  po_ref varchar(40) NOT NULL,
  supp_no varchar(40) NOT NULL,
  item_cd varchar(20) NOT NULL,
  lot_no varchar(40) NOT NULL,
  rcpt_dt date NOT NULL,
  qty integer NOT NULL,
  loc_cd varchar(20) NOT NULL,
  cert_ref varchar(40),
  CONSTRAINT inv_rcpt_ntf_pk PRIMARY KEY (grn_ref)
);
COMMENT ON TABLE coco_inventory.inv_rcpt_ntf IS 'Receipt notifications from the depots (Goods Receipts): each received lot is booked into quarantine (inv_qrn) from here when the goods are put away.';

CREATE TABLE IF NOT EXISTS coco_inventory.inv_qc_smpl (
  smpl_ref varchar(40) NOT NULL,
  lot_no varchar(40) NOT NULL,
  coll_ts timestamptz NOT NULL,
  smpl_sts varchar(20) NOT NULL,
  CONSTRAINT inv_qc_smpl_pk PRIMARY KEY (smpl_ref)
);
COMMENT ON TABLE coco_inventory.inv_qc_smpl IS 'QC samples of quarantined lots received from a laboratory system (Laboratory Test Results).';

CREATE TABLE IF NOT EXISTS coco_inventory.inv_qc_res (
  res_ref varchar(40) NOT NULL,
  smpl_ref varchar(40) NOT NULL,
  test_cd varchar(40) NOT NULL,
  res_val varchar(60) NOT NULL,
  res_uom varchar(20),
  pass_yn char(1) NOT NULL,
  done_ts timestamptz NOT NULL,
  CONSTRAINT inv_qc_res_pk PRIMARY KEY (res_ref)
);
COMMENT ON TABLE coco_inventory.inv_qc_res IS 'Test results of the samples in inv_qc_smpl, referenced by the quarantine decision (inv_qdisp.lab_ref).';

CREATE TABLE IF NOT EXISTS coco_inventory.inv_qc_coa (
  coa_ref varchar(40) NOT NULL,
  lot_no varchar(40) NOT NULL,
  coa_dt date NOT NULL,
  pass_yn char(1) NOT NULL,
  approver varchar(40) NOT NULL,
  CONSTRAINT inv_qc_coa_pk PRIMARY KEY (coa_ref)
);
COMMENT ON TABLE coco_inventory.inv_qc_coa IS 'Laboratory certificates of analysis for quarantined lots.';

CREATE TABLE IF NOT EXISTS coco_inventory.inv_serial (
  serial_no varchar(40) NOT NULL,
  item_cd varchar(20) NOT NULL,
  pack_cd varchar(20) NOT NULL,
  lot_no varchar(40) NOT NULL,
  exp_dt date NOT NULL,
  mkt varchar(8) NOT NULL,
  serial_sts varchar(20) NOT NULL,
  parent_serial varchar(40),
  loc_cd varchar(20),
  CONSTRAINT inv_serial_pk PRIMARY KEY (serial_no)
);
COMMENT ON TABLE coco_inventory.inv_serial IS 'Serialised packs held at Coco locations (Serialised Product Identifiers), with their aggregation parent.';

CREATE TABLE IF NOT EXISTS coco_inventory.inv_serial_evt (
  serial_no varchar(40) NOT NULL,
  evt_ts timestamptz NOT NULL,
  evt_typ varchar(20) NOT NULL,
  src_sys varchar(60) NOT NULL,
  alert_ref varchar(40),
  CONSTRAINT inv_serial_evt_pk PRIMARY KEY (serial_no, evt_ts)
);
COMMENT ON TABLE coco_inventory.inv_serial_evt IS 'Events of the serialised packs in inv_serial (commissioned, verified, decommissioned, alerts).';

CREATE TABLE IF NOT EXISTS coco_inventory.inv_supp (
  supp_no varchar(10) NOT NULL,
  supp_nm varchar(200) NOT NULL,
  appr_yn char(1) NOT NULL,
  supp_sts char(1) NOT NULL,
  CONSTRAINT inv_supp_pk PRIMARY KEY (supp_no)
);
COMMENT ON TABLE coco_inventory.inv_supp IS 'Suppliers whose material may be received (Supplier Master Data); supp_sts A active, S suspended, C closed.';

CREATE TABLE IF NOT EXISTS coco_inventory.inv_supp_coa (
  cert_ref varchar(40) NOT NULL,
  supp_no varchar(10) NOT NULL,
  item_cd varchar(20) NOT NULL,
  lot_no varchar(40) NOT NULL,
  cert_typ varchar(4) NOT NULL,
  cert_dt date NOT NULL,
  ok_yn char(1) NOT NULL,
  CONSTRAINT inv_supp_coa_pk PRIMARY KEY (cert_ref)
);
COMMENT ON TABLE coco_inventory.inv_supp_coa IS 'Supplier certificates for received lots (Supplier Material Certificates); cert_typ COA analysis, COC conformity.';

CREATE TABLE IF NOT EXISTS coco_inventory.inv_supp_coa_tst (
  cert_ref varchar(40) NOT NULL,
  test_cd varchar(40) NOT NULL,
  tst_val varchar(60) NOT NULL,
  tst_uom varchar(20),
  spec_lo varchar(60),
  spec_hi varchar(60),
  CONSTRAINT inv_supp_coa_tst_pk PRIMARY KEY (cert_ref, test_cd)
);
COMMENT ON TABLE coco_inventory.inv_supp_coa_tst IS 'Test results stated on the supplier certificates in inv_supp_coa.';

-- End of subscription tables.

GRANT USAGE ON SCHEMA coco_inventory TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA coco_inventory TO egeria_user, airflow_user;
