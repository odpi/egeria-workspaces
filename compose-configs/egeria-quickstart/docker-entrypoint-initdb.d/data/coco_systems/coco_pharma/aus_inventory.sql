-- system-qualified-name: System::aus-inventory
-- Austin Inventory - Coco core.  Homegrown inventory for the Austin site, built separately from Coco Inventory; feeds Goods Receipts, Material Quarantine Dispositions and Goods Inventory Stock for Austin.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS aus_inventory;
COMMENT ON SCHEMA aus_inventory IS 'Austin Inventory (Coco core): items, receiving, inspection, lot status and disposition, on-hand and transactions for the Austin site.';

CREATE TABLE IF NOT EXISTS aus_inventory.item (
  item_no varchar(10) NOT NULL,
  descr varchar(80) NOT NULL,
  stock_uom varchar(6) NOT NULL,
  CONSTRAINT item_pk PRIMARY KEY (item_no)
);
COMMENT ON TABLE aus_inventory.item IS 'Items stocked at Austin (material codes held in lower case).';

CREATE TABLE IF NOT EXISTS aus_inventory.receiving_log (
  rcv_no varchar(20) NOT NULL,
  po_no varchar(20) NOT NULL,
  vendor_no integer NOT NULL,
  item_no varchar(10) NOT NULL,
  vendor_lot varchar(30) NOT NULL,
  rcv_date varchar(10) NOT NULL,
  rcv_qty numeric(12,2) NOT NULL,
  loc_id varchar(8) NOT NULL,
  coa_no varchar(30),
  CONSTRAINT receiving_log_pk PRIMARY KEY (rcv_no)
);
COMMENT ON TABLE aus_inventory.receiving_log IS 'Materials received directly at the Austin site; rcv_date is text MM/DD/YYYY.';

CREATE TABLE IF NOT EXISTS aus_inventory.rcv_inspection (
  rcv_no varchar(20) NOT NULL,
  insp_date date NOT NULL,
  inspector_badge varchar(10) NOT NULL,
  outcome varchar(12) NOT NULL,
  remarks text,
  CONSTRAINT rcv_inspection_pk PRIMARY KEY (rcv_no, insp_date)
);
COMMENT ON TABLE aus_inventory.rcv_inspection IS 'Receiving inspection outcomes (Accepted, Rejected, On Hold).';

CREATE TABLE IF NOT EXISTS aus_inventory.badge (
  badge_no varchar(10) NOT NULL,
  worker_psn varchar(20) NOT NULL,
  CONSTRAINT badge_pk PRIMARY KEY (badge_no)
);
COMMENT ON TABLE aus_inventory.badge IS 'Austin site badges with the pseudonym used outside the site.';

CREATE TABLE IF NOT EXISTS aus_inventory.lot_status (
  lot_no varchar(30) NOT NULL,
  item_no varchar(10) NOT NULL,
  rcv_no varchar(20) NOT NULL,
  quar_start timestamptz NOT NULL,
  loc_id varchar(8) NOT NULL,
  qty numeric(12,2) NOT NULL,
  sample_no varchar(20),
  status varchar(12) NOT NULL,
  CONSTRAINT lot_status_pk PRIMARY KEY (lot_no)
);
COMMENT ON TABLE aus_inventory.lot_status IS 'Status of every received lot: QUARANTINE, RELEASED, REJECTED.';

CREATE TABLE IF NOT EXISTS aus_inventory.lot_disposition (
  lot_no varchar(30) NOT NULL,
  disp_utc timestamptz NOT NULL,
  decision varchar(8) NOT NULL,
  lab_result_ref varchar(20) NOT NULL,
  expiry varchar(10),
  qty_released numeric(12,2),
  CONSTRAINT lot_disposition_pk PRIMARY KEY (lot_no, disp_utc)
);
COMMENT ON TABLE aus_inventory.lot_disposition IS 'QA disposition of quarantined lots; expiry is text MM/DD/YYYY.';

CREATE TABLE IF NOT EXISTS aus_inventory.on_hand (
  item_no varchar(10) NOT NULL,
  loc_id varchar(8) NOT NULL,
  lot_no varchar(30) NOT NULL,
  qty numeric(12,2) NOT NULL,
  min_qty numeric(12,2),
  max_qty numeric(12,2),
  as_of timestamptz NOT NULL,
  CONSTRAINT on_hand_pk PRIMARY KEY (item_no, loc_id, lot_no)
);
COMMENT ON TABLE aus_inventory.on_hand IS 'On-hand quantity per item, location and lot.';

CREATE TABLE IF NOT EXISTS aus_inventory.inv_transaction (
  trans_no varchar(10) NOT NULL,
  trans_code char(1) NOT NULL,
  item_no varchar(10) NOT NULL,
  lot_no varchar(30),
  qty numeric(12,2) NOT NULL,
  trans_utc timestamptz NOT NULL,
  loc_id varchar(8) NOT NULL,
  batch_id varchar(20),
  lot_status_at_trans char(1),
  CONSTRAINT inv_transaction_pk PRIMARY KEY (trans_no)
);
COMMENT ON TABLE aus_inventory.inv_transaction IS 'Inventory transactions. trans_code R receipt, I issue, T transfer, A adjustment, S shipment; lot_status_at_trans Q/R/X.';

INSERT INTO aus_inventory.item (item_no, descr, stock_uom) VALUES
('rm3001', 'Losartan potassium', 'kg'),
('rm2051', 'Clopidogrel bisulfate', 'kg'),
('rm9001', 'Cisplatin API', 'g'),
('rm9002', 'Sodium chloride 0.9% water for injection', 'L'),
('rm1002', 'Microcrystalline cellulose', 'kg'),
('pk0021', 'Glass vials 50mL', 'case'),
('3000', 'Cozaar 100mg', 'EA'),
('2050', 'Plavix 75mg', 'EA'),
('9000', 'Cisplatin 50mg', 'EA')
ON CONFLICT DO NOTHING;

INSERT INTO aus_inventory.receiving_log (rcv_no, po_no, vendor_no, item_no, vendor_lot, rcv_date, rcv_qty, loc_id, coa_no) VALUES
('AUS-RCV-26-0341', 'PO-AUS-26-0212', 2000, 'rm3001', 'TT-LOS-26-0341', '07/06/2026', 400, 'AUS-RM', 'COA-TT-26-0341'),
('AUS-RCV-26-0362', 'PO-AUS-26-0219', 2000, 'rm2051', 'TT-CLP-26-0118', '07/20/2026', 300, 'AUS-RM', 'COA-TT-26-0118'),
('AUS-RCV-26-0388', 'PO-AUS-26-0231', 7000, 'rm9001', 'BASE-CIS-2608', '08/11/2026', 5000, 'AUS-HAZ', 'COA-BASE-CIS-2608'),
('AUS-RCV-26-0390', 'PO-AUS-26-0232', 9000, 'rm1002', 'WWE-MCC-2608-21', '08/12/2026', 1000, 'AUS-RM', 'COA-WWE-2608-21'),
('AUS-RCV-26-0402', 'PO-AUS-26-0240', 2000, 'rm3001', 'TT-LOS-26-0402', '08/24/2026', 400, 'AUS-RM', 'COA-TT-26-0402'),
('AUS-RCV-26-0431', 'PO-AUS-26-0251', 2000, 'rm2051', 'TT-CLP-26-0166', '09/14/2026', 300, 'AUS-RM', 'COA-TT-26-0166'),
('AUS-RCV-26-0447', 'PO-AUS-26-0258', 1000, 'pk0021', 'GML-VIAL-2609', '09/25/2026', 30, 'AUS-RM', 'COC-GML-VIAL-2609')
ON CONFLICT DO NOTHING;

INSERT INTO aus_inventory.rcv_inspection (rcv_no, insp_date, inspector_badge, outcome, remarks) VALUES
('AUS-RCV-26-0341', '2026-07-06', 'AUS-0440', 'Accepted', NULL),
('AUS-RCV-26-0362', '2026-07-20', 'AUS-0440', 'Accepted', NULL),
('AUS-RCV-26-0388', '2026-08-11', 'AUS-0440', 'Accepted', 'Cytotoxic - opened in containment only'),
('AUS-RCV-26-0390', '2026-08-12', 'AUS-0440', 'Accepted', NULL),
('AUS-RCV-26-0402', '2026-08-24', 'AUS-0440', 'Accepted', NULL),
('AUS-RCV-26-0431', '2026-09-14', 'AUS-0440', 'Accepted', NULL),
('AUS-RCV-26-0447', '2026-09-25', 'AUS-0440', 'Rejected', 'Vial neck chips found on AQL sample')
ON CONFLICT DO NOTHING;

INSERT INTO aus_inventory.badge (badge_no, worker_psn) VALUES
('AUS-0417', 'AW-WQ5BBD'),
('AUS-0422', 'AW-TWJQVP'),
('AUS-0431', 'AW-4U49Z6'),
('AUS-0440', 'AW-WSVK4V')
ON CONFLICT DO NOTHING;

INSERT INTO aus_inventory.lot_status (lot_no, item_no, rcv_no, quar_start, loc_id, qty, sample_no, status) VALUES
('TT-LOS-26-0341', 'rm3001', 'AUS-RCV-26-0341', '2026-07-06 16:00+00', 'AUS-QA', 400, 'AS-26-1107', 'RELEASED'),
('TT-CLP-26-0118', 'rm2051', 'AUS-RCV-26-0362', '2026-07-20 16:00+00', 'AUS-QA', 300, 'AS-26-1131', 'RELEASED'),
('BASE-CIS-2608', 'rm9001', 'AUS-RCV-26-0388', '2026-08-11 16:00+00', 'AUS-QA', 5000, 'AS-26-1170', 'RELEASED'),
('WWE-MCC-2608-21', 'rm1002', 'AUS-RCV-26-0390', '2026-08-12 16:00+00', 'AUS-QA', 1000, 'AS-26-1172', 'RELEASED'),
('TT-LOS-26-0402', 'rm3001', 'AUS-RCV-26-0402', '2026-08-24 16:00+00', 'AUS-QA', 400, 'AS-26-1195', 'RELEASED'),
('TT-CLP-26-0166', 'rm2051', 'AUS-RCV-26-0431', '2026-09-14 16:00+00', 'AUS-QA', 300, 'AS-26-1222', 'RELEASED'),
('GML-VIAL-2609', 'pk0021', 'AUS-RCV-26-0447', '2026-09-25 16:00+00', 'AUS-QA', 30, 'AS-26-1236', 'REJECTED')
ON CONFLICT DO NOTHING;

INSERT INTO aus_inventory.lot_disposition (lot_no, disp_utc, decision, lab_result_ref, expiry, qty_released) VALUES
('TT-LOS-26-0341', '2026-07-14 15:00+00', 'RELEASE', 'LAB-AUS-26-0415', '06/30/2028', 400),
('TT-CLP-26-0118', '2026-07-27 15:00+00', 'RELEASE', 'LAB-AUS-26-0433', '06/30/2028', 300),
('BASE-CIS-2608', '2026-08-25 15:00+00', 'RELEASE', 'LAB-AUS-26-0461', '07/31/2029', 5000),
('WWE-MCC-2608-21', '2026-08-15 15:00+00', 'RELEASE', 'LAB-AUS-26-0463', '07/31/2029', 1000),
('TT-LOS-26-0402', '2026-09-03 15:00+00', 'RELEASE', 'LAB-AUS-26-0480', '07/31/2028', 400),
('TT-CLP-26-0166', '2026-09-24 15:00+00', 'RELEASE', 'LAB-AUS-26-0502', '08/31/2028', 300),
('GML-VIAL-2609', '2026-09-29 15:00+00', 'REJECT', 'LAB-AUS-26-0511', NULL, NULL)
ON CONFLICT DO NOTHING;

INSERT INTO aus_inventory.on_hand (item_no, loc_id, lot_no, qty, min_qty, max_qty, as_of) VALUES
('rm3001', 'AUS-RM', 'TT-LOS-26-0402', 388, 100, 900, '2026-09-07 04:00+00'),
('rm3001', 'AUS-RM', 'TT-LOS-26-0341', 376, 100, 900, '2026-08-03 04:00+00'),
('rm2051', 'AUS-RM', 'TT-CLP-26-0166', 291, 80, 700, '2026-09-28 04:00+00'),
('rm2051', 'AUS-RM', 'TT-CLP-26-0118', 291, 80, 700, '2026-08-17 04:00+00'),
('rm9001', 'AUS-HAZ', 'BASE-CIS-2608', 4870, 1000, 8000, '2026-09-01 05:00+00'),
('rm1002', 'AUS-RM', 'WWE-MCC-2608-21', 934, 300, 2500, '2026-09-28 04:00+00'),
('pk0021', 'AUS-QA', 'GML-VIAL-2609', 30, NULL, NULL, '2026-09-25 16:00+00'),
('3000', 'AUS-FG', 'A26-3000-0142', 120000, NULL, NULL, '2026-09-09 18:00+00'),
('3000', 'AUS-FG', 'A26-3000-0141', 29000, 20000, 200000, '2026-09-02 15:00+00'),
('2050', 'AUS-FG', 'A26-2050-0087', 20000, 15000, 150000, '2026-09-02 15:00+00'),
('9000', 'AUS-FG', 'A26-9000-0019', 1000, 500, 5000, '2026-09-17 15:00+00')
ON CONFLICT DO NOTHING;

INSERT INTO aus_inventory.inv_transaction (trans_no, trans_code, item_no, lot_no, qty, trans_utc, loc_id, batch_id, lot_status_at_trans) VALUES
('AT5101', 'R', 'rm3001', 'TT-LOS-26-0341', 400, '2026-07-06 16:00+00', 'AUS-QA', NULL, 'Q'),
('AT5102', 'R', 'rm2051', 'TT-CLP-26-0118', 300, '2026-07-20 16:00+00', 'AUS-QA', NULL, 'Q'),
('AT5103', 'R', 'rm9001', 'BASE-CIS-2608', 5000, '2026-08-11 16:00+00', 'AUS-QA', NULL, 'Q'),
('AT5104', 'R', 'rm1002', 'WWE-MCC-2608-21', 1000, '2026-08-12 16:00+00', 'AUS-QA', NULL, 'Q'),
('AT5105', 'R', 'rm3001', 'TT-LOS-26-0402', 400, '2026-08-24 16:00+00', 'AUS-QA', NULL, 'Q'),
('AT5106', 'R', 'rm2051', 'TT-CLP-26-0166', 300, '2026-09-14 16:00+00', 'AUS-QA', NULL, 'Q'),
('AT5107', 'R', 'pk0021', 'GML-VIAL-2609', 30, '2026-09-25 16:00+00', 'AUS-QA', NULL, 'Q'),
('AT5108', 'I', 'rm3001', 'TT-LOS-26-0341', -12, '2026-08-03 04:00+00', 'AUS-RM', 'A26-3000-0141', 'R'),
('AT5109', 'I', 'rm1002', 'WWE-MCC-2606-40', -26, '2026-08-03 04:00+00', 'AUS-RM', 'A26-3000-0141', 'R'),
('AT5110', 'I', 'rm2051', 'TT-CLP-26-0118', -9, '2026-08-17 04:00+00', 'AUS-RM', 'A26-2050-0087', 'R'),
('AT5111', 'I', 'rm1002', 'WWE-MCC-2608-21', -20, '2026-08-17 04:00+00', 'AUS-RM', 'A26-2050-0087', 'R'),
('AT5112', 'I', 'rm9001', 'BASE-CIS-2608', -130, '2026-09-01 05:00+00', 'AUS-HAZ', 'A26-9000-0019', 'R'),
('AT5113', 'I', 'rm9002', 'NAC-WFI-2608', -130, '2026-09-01 08:00+00', 'AUS-RM', 'A26-9000-0019', 'R'),
('AT5114', 'I', 'pk0021', 'GML-VIAL-2607', -25, '2026-09-01 14:00+00', 'AUS-RM', 'A26-9000-0019', 'R'),
('AT5115', 'I', 'rm3001', 'TT-LOS-26-0402', -12, '2026-09-07 04:00+00', 'AUS-RM', 'A26-3000-0142', 'R'),
('AT5116', 'I', 'rm1002', 'WWE-MCC-2608-21', -26, '2026-09-07 04:00+00', 'AUS-RM', 'A26-3000-0142', 'R'),
('AT5117', 'I', 'rm2051', 'TT-CLP-26-0166', -9, '2026-09-28 04:00+00', 'AUS-RM', 'A26-2050-0088', 'R'),
('AT5118', 'I', 'rm1002', 'WWE-MCC-2608-21', -20, '2026-09-28 04:00+00', 'AUS-RM', 'A26-2050-0088', 'R'),
('AT5119', 'S', '3000', 'A26-3000-0141', -91000, '2026-08-20 14:00+00', 'AUS-FG', NULL, NULL),
('AT5120', 'S', '2050', 'A26-2050-0087', -70000, '2026-08-31 14:00+00', 'AUS-FG', NULL, NULL),
('AT5121', 'S', '9000', 'A26-9000-0019', -1500, '2026-09-17 14:00+00', 'AUS-FG', NULL, NULL),
('AT5122', 'T', 'rm1002', 'WWE-MCC-2608-21', -40, '2026-09-05 10:00+00', 'AUS-RM', NULL, NULL),
('AT5123', 'A', 'rm2051', 'TT-CLP-26-0118', -2, '2026-09-04 10:00+00', 'AUS-RM', NULL, NULL)
ON CONFLICT DO NOTHING;


-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS aus_inventory.lab_sample_in (
  sample_no varchar(40) NOT NULL,
  lot_no varchar(30) NOT NULL,
  collected_utc timestamptz NOT NULL,
  sample_status varchar(20) NOT NULL,
  CONSTRAINT lab_sample_in_pk PRIMARY KEY (sample_no)
);
COMMENT ON TABLE aus_inventory.lab_sample_in IS 'Laboratory samples of lots held in quarantine at Austin (Laboratory Test Results).';

CREATE TABLE IF NOT EXISTS aus_inventory.lab_result_in (
  result_no varchar(40) NOT NULL,
  sample_no varchar(40) NOT NULL,
  test_code varchar(40) NOT NULL,
  result_value varchar(60) NOT NULL,
  result_unit varchar(20),
  pass_fail char(1) NOT NULL,
  completed_utc timestamptz NOT NULL,
  CONSTRAINT lab_result_in_pk PRIMARY KEY (result_no)
);
COMMENT ON TABLE aus_inventory.lab_result_in IS 'Test results of the samples in lab_sample_in (pass_fail P/F), referenced by the lot disposition (lot_disposition.lab_result_ref).';

CREATE TABLE IF NOT EXISTS aus_inventory.lab_coa_in (
  coa_no varchar(40) NOT NULL,
  lot_no varchar(30) NOT NULL,
  coa_date varchar(10) NOT NULL,
  pass_fail char(1) NOT NULL,
  approver varchar(40) NOT NULL,
  CONSTRAINT lab_coa_in_pk PRIMARY KEY (coa_no)
);
COMMENT ON TABLE aus_inventory.lab_coa_in IS 'Laboratory certificates of analysis for quarantined lots; coa_date is text MM/DD/YYYY like the other dates in this system.';

CREATE TABLE IF NOT EXISTS aus_inventory.serial_no (
  serial_no varchar(40) NOT NULL,
  item_no varchar(20) NOT NULL,
  pack_code varchar(20) NOT NULL,
  lot_no varchar(40) NOT NULL,
  expiry varchar(10) NOT NULL,
  market varchar(8) NOT NULL,
  serial_status varchar(20) NOT NULL,
  parent_serial varchar(40),
  loc_id varchar(8),
  CONSTRAINT serial_no_pk PRIMARY KEY (serial_no)
);
COMMENT ON TABLE aus_inventory.serial_no IS 'Serialised packs held at the Austin site locations (Serialised Product Identifiers); expiry is text MM/DD/YYYY.';

CREATE TABLE IF NOT EXISTS aus_inventory.serial_event (
  serial_no varchar(40) NOT NULL,
  event_utc timestamptz NOT NULL,
  event_type varchar(20) NOT NULL,
  source_system varchar(60) NOT NULL,
  alert_no varchar(40),
  CONSTRAINT serial_event_pk PRIMARY KEY (serial_no, event_utc)
);
COMMENT ON TABLE aus_inventory.serial_event IS 'Events of the serialised packs in serial_no.';

CREATE TABLE IF NOT EXISTS aus_inventory.vendor (
  vendor_no integer NOT NULL,
  vendor_name varchar(200) NOT NULL,
  approved char(1) NOT NULL,
  vendor_status varchar(12) NOT NULL,
  CONSTRAINT vendor_pk PRIMARY KEY (vendor_no)
);
COMMENT ON TABLE aus_inventory.vendor IS 'Coco suppliers whose material may be received at the Austin site (Supplier Master Data); vendor_no as in receiving_log.';

CREATE TABLE IF NOT EXISTS aus_inventory.vendor_coa (
  coa_no varchar(40) NOT NULL,
  vendor_no integer NOT NULL,
  item_no varchar(20) NOT NULL,
  vendor_lot varchar(40) NOT NULL,
  cert_type varchar(12) NOT NULL,
  cert_date varchar(10) NOT NULL,
  conforms char(1) NOT NULL,
  CONSTRAINT vendor_coa_pk PRIMARY KEY (coa_no)
);
COMMENT ON TABLE aus_inventory.vendor_coa IS 'Supplier certificates for lots received at Austin (Supplier Material Certificates), matched to receiving_log.coa_no; item_no lower case and cert_date text MM/DD/YYYY as elsewhere in this system.';

CREATE TABLE IF NOT EXISTS aus_inventory.vendor_coa_test (
  coa_no varchar(40) NOT NULL,
  test_code varchar(40) NOT NULL,
  test_value varchar(60) NOT NULL,
  test_unit varchar(20),
  spec_min varchar(60),
  spec_max varchar(60),
  CONSTRAINT vendor_coa_test_pk PRIMARY KEY (coa_no, test_code)
);
COMMENT ON TABLE aus_inventory.vendor_coa_test IS 'Test results stated on the supplier certificates in vendor_coa.';

-- End of subscription tables.

GRANT USAGE ON SCHEMA aus_inventory TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA aus_inventory TO egeria_user, airflow_user;
