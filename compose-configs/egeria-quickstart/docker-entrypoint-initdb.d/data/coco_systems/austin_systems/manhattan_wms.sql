-- system-qualified-name: SoftwareServer::AUS-SYS-012::SN-WMS-AU-20200315
-- Manhattan WMS - Austin.  Manhattan Associates WMOS for the Austin plant stores (AUS1) and distribution center
-- (AUS2): inbound ASNs and receipts, receiving inspection, lot (batch) quarantine status, inventory and PIX inventory
-- transactions.  Its tables feed Goods Receipts, Material Quarantine Dispositions and Goods Inventory Stock.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS manhattan_wms;
COMMENT ON SCHEMA manhattan_wms IS 'Manhattan WMOS (Austin): facility, item, ASN, inspection, batch master, inventory and PIX transaction tables.';

CREATE TABLE IF NOT EXISTS manhattan_wms.facility (
  facility_id   integer NOT NULL,
  facility_name varchar(120) NOT NULL,
  whse          varchar(10) NOT NULL,
  city          varchar(60),
  state_prov    varchar(10),
  country_code  varchar(2) NOT NULL,
  CONSTRAINT facility_pk PRIMARY KEY (facility_id)
);
COMMENT ON TABLE manhattan_wms.facility IS 'Warehouses.';

INSERT INTO manhattan_wms.facility (facility_id, facility_name, whse, city, state_prov, country_code) VALUES
(10, 'Austin Plant Stores', 'AUS1', 'Austin', 'TX', 'US'),
(20, 'Austin Distribution Center', 'AUS2', 'Round Rock', 'TX', 'US')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS manhattan_wms.item_cbo (
  item_id          integer NOT NULL,
  item_name        varchar(40) NOT NULL,
  description      varchar(200),
  base_storage_uom varchar(10) NOT NULL,
  item_type        varchar(4) NOT NULL,
  CONSTRAINT item_cbo_pk PRIMARY KEY (item_id)
);
COMMENT ON TABLE manhattan_wms.item_cbo IS 'Items (item name = SAP material number or product code).';

INSERT INTO manhattan_wms.item_cbo (item_id, item_name, description, base_storage_uom, item_type) VALUES
(60001, 'RM-100110', 'Losartan potassium USP', 'G', 'RM'),
(60002, 'RM-100120', 'Clopidogrel bisulfate USP', 'G', 'RM'),
(60003, 'RM-100130', 'Cisplatin USP', 'G', 'RM'),
(60004, 'RM-100140', 'Carboplatin USP', 'G', 'RM'),
(60005, 'RM-100150', 'Methotrexate USP', 'G', 'RM'),
(60006, 'RM-200210', 'Microcrystalline cellulose PH102', 'G', 'RM'),
(60007, 'RM-200220', 'Magnesium stearate NF', 'G', 'RM'),
(60008, 'RM-200230', 'Sodium chloride injection grade', 'G', 'RM'),
(60009, 'RM-200240', 'Mannitol USP', 'G', 'RM'),
(60010, 'PK-300310', 'Type I glass vial 50 mL', 'EA', 'PK'),
(60011, 'PK-300320', 'HDPE bottle 90 count with CRC', 'EA', 'PK'),
(60012, 'RM-400410', 'GMP cell culture medium (serum-free)', 'ML', 'RM'),
(61001, '3000', 'Cozaar 100mg film-coated tablets', 'EA', 'FG'),
(61002, '2050', 'Plavix 75mg film-coated tablets', 'EA', 'FG'),
(61003, '9000', 'Cisplatin 50mg/50mL injection', 'EA', 'FG'),
(61004, 'AU-4410', 'Carboplatin 450mg/45mL injection', 'EA', 'FG'),
(61005, 'AU-4520', 'Oxaliplatin 100mg/20mL injection', 'EA', 'FG'),
(61006, 'AU-4630', 'Methotrexate 250mg/10mL injection', 'EA', 'FG')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS manhattan_wms.item_facility_mapping_wms (
  item_id      integer NOT NULL,
  facility_id  integer NOT NULL,
  min_invn_qty integer,
  max_invn_qty integer,
  CONSTRAINT item_facility_mapping_wms_pk PRIMARY KEY (item_id, facility_id)
);
COMMENT ON TABLE manhattan_wms.item_facility_mapping_wms IS 'Item settings per facility, including replenishment min/max in base units.';

INSERT INTO manhattan_wms.item_facility_mapping_wms (item_id, facility_id, min_invn_qty, max_invn_qty) VALUES
(60001, 10, 150000, 900000),
(60002, 10, 100000, 600000),
(60003, 10, 150, 1200),
(60004, 10, 500, 3000),
(60005, 10, 300, 2400),
(60006, 10, 200000, 1600000),
(60007, 10, 10000, 80000),
(60008, 10, 20000, 100000),
(60009, 10, 50000, 600000),
(60010, 10, 3000, 20000),
(60011, 10, 2000, 15000),
(60012, 10, 20000, 120000),
(61001, 20, 500, 6000),
(61002, 20, 500, 6000),
(61003, 20, 500, 6000),
(61004, 20, 500, 6000),
(61005, 20, 500, 6000),
(61006, 20, 500, 6000)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS manhattan_wms.asn (
  asn_id                  integer NOT NULL,
  tc_asn_id               varchar(40) NOT NULL,
  business_partner_id     varchar(20) NOT NULL,
  tc_purchase_orders_id   varchar(20),
  destination_facility_id integer NOT NULL,
  asn_status              integer NOT NULL,
  created_dttm            timestamptz NOT NULL,
  last_received_dttm      timestamptz,
  CONSTRAINT asn_pk PRIMARY KEY (asn_id)
);
COMMENT ON TABLE manhattan_wms.asn IS 'Inbound ASNs; the tc_asn_id is the goods receipt number (status 60 = receipt verified; business partner = SAP vendor).';

INSERT INTO manhattan_wms.asn (asn_id, tc_asn_id, business_partner_id, tc_purchase_orders_id, destination_facility_id, asn_status, created_dttm, last_received_dttm) VALUES
(7101, 'AUS1-R-26-0098', '100120', '4500001866', 10, 60, '2026-06-13 11:20:00+00', '2026-06-15 11:20:00+00'),
(7102, 'AUS1-R-26-0101', '100010', '4500001871', 10, 60, '2026-06-20 14:10:00+00', '2026-06-22 14:10:00+00'),
(7103, 'AUS1-R-26-0102', '100040', '4500001874', 10, 60, '2026-06-22 09:35:00+00', '2026-06-24 09:35:00+00'),
(7104, 'AUS1-R-26-0103', '100050', '4500001875', 10, 60, '2026-06-22 10:20:00+00', '2026-06-24 10:20:00+00'),
(7105, 'AUS1-R-26-0104', '100020', '4500001880', 10, 60, '2026-07-04 13:05:00+00', '2026-07-06 13:05:00+00'),
(7106, 'AUS1-R-26-0105', '100030', '4500001883', 10, 60, '2026-07-11 11:50:00+00', '2026-07-13 11:50:00+00'),
(7107, 'AUS1-R-26-0106', '100060', '4500001884', 10, 60, '2026-07-13 08:40:00+00', '2026-07-15 08:40:00+00'),
(7108, 'AUS1-R-26-0107', '100010', '4500001902', 10, 60, '2026-08-08 15:25:00+00', '2026-08-10 15:25:00+00'),
(7109, 'AUS1-R-26-0108', '100050', '4500001905', 10, 60, '2026-08-15 10:00:00+00', '2026-08-17 10:00:00+00'),
(7110, 'AUS1-R-26-0109', '100080', '4500001911', 10, 60, '2026-09-01 09:10:00+00', '2026-09-03 09:10:00+00'),
(7111, 'AUS1-R-26-0110', '100020', '4500001915', 10, 60, '2026-09-12 14:45:00+00', '2026-09-14 14:45:00+00'),
(7112, 'AUS1-R-26-0111', '100120', '4500001921', 10, 60, '2026-09-20 12:30:00+00', '2026-09-22 12:30:00+00'),
(7113, 'AUS1-R-26-0112', '100010', '4500001924', 10, 60, '2026-09-26 10:15:00+00', '2026-09-28 10:15:00+00')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS manhattan_wms.asn_detail (
  asn_detail_id integer NOT NULL,
  asn_id        integer NOT NULL,
  sku_id        integer NOT NULL,
  batch_nbr     varchar(40) NOT NULL,
  shipped_qty   integer NOT NULL,
  received_qty  integer NOT NULL,
  qty_uom       varchar(10) NOT NULL,
  ref_field_1   varchar(40),
  ref_field_2   varchar(40),
  CONSTRAINT asn_detail_pk PRIMARY KEY (asn_detail_id)
);
COMMENT ON TABLE manhattan_wms.asn_detail IS 'ASN lines (ref_field_1 = supplier certificate number, ref_field_2 = supplier lot).';

INSERT INTO manhattan_wms.asn_detail (asn_detail_id, asn_id, sku_id, batch_nbr, shipped_qty, received_qty, qty_uom, ref_field_1, ref_field_2) VALUES
(71011, 7101, 60012, 'RM26-0098', 40000, 40000, 'ML', 'GCC-COC-260603', 'GCC-MED-260603'),
(71021, 7102, 60001, 'RM26-0101', 250000, 250000, 'G', 'HH-COA-2605117', 'HH-LOS-2605117'),
(71031, 7103, 60006, 'RM26-0102', 800000, 800000, 'G', 'DFE-COA-6612004', 'DFE-102-6612004'),
(71041, 7104, 60007, 'RM26-0103', 40000, 40000, 'G', 'SPC-COA-1188342', 'SPC-MS-1188342'),
(71051, 7105, 60002, 'RM26-0104', 180000, 180000, 'G', 'DRL-COA-26B0441', 'DRL-CLP-26B0441'),
(71061, 7106, 60003, 'RM26-0105', 600, 600, 'G', 'HPM-COA-240771', 'HPM-CIS-240771'),
(71071, 7107, 60010, 'RM26-0106', 8000, 8000, 'EA', 'SCH-COC-7781205', 'SCH-V50-7781205'),
(71081, 7108, 60001, 'RM26-0107', 250000, 250000, 'G', 'HH-COA-2607203', 'HH-LOS-2607203'),
(71091, 7109, 60005, 'RM26-0108', 1200, 1200, 'G', 'SPC-COA-1190087', 'SPC-MTX-1190087'),
(71101, 7110, 60009, 'RM26-0109', 300000, 300000, 'G', 'ROQ-COA-6014592', 'ROQ-P-6014592'),
(71111, 7111, 60002, 'RM26-0110', 180000, 180000, 'G', 'DRL-COA-26C0917', 'DRL-CLP-26C0917'),
(71121, 7112, 60012, 'RM26-0111', 60000, 60000, 'ML', 'GCC-COC-260912', 'GCC-MED-260912'),
(71131, 7113, 60001, 'RM26-0112', 250000, 250000, 'G', 'HH-COA-2609044', 'HH-LOS-2609044')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS manhattan_wms.qc_inspection (
  tc_asn_id         varchar(40) NOT NULL,
  inspection_dttm   timestamptz NOT NULL,
  inspected_by      varchar(20) NOT NULL,
  inspection_status char(1) NOT NULL,
  comments          text,
  CONSTRAINT qc_inspection_pk PRIMARY KEY (tc_asn_id, inspection_dttm)
);
COMMENT ON TABLE manhattan_wms.qc_inspection IS 'Receiving inspection results (A accepted, R rejected, H held).';

INSERT INTO manhattan_wms.qc_inspection (tc_asn_id, inspection_dttm, inspected_by, inspection_status, comments) VALUES
('AUS1-R-26-0098', '2026-06-15 12:05:00+00', 'ohaddad', 'A', NULL),
('AUS1-R-26-0101', '2026-06-22 14:55:00+00', 'sadeyemi', 'A', NULL),
('AUS1-R-26-0102', '2026-06-24 10:20:00+00', 'ohaddad', 'A', NULL),
('AUS1-R-26-0103', '2026-06-24 11:05:00+00', 'sadeyemi', 'A', NULL),
('AUS1-R-26-0104', '2026-07-06 13:50:00+00', 'ohaddad', 'A', NULL),
('AUS1-R-26-0105', '2026-07-13 12:35:00+00', 'ohaddad', 'A', NULL),
('AUS1-R-26-0106', '2026-07-15 09:25:00+00', 'ohaddad', 'A', 'Two cartons crushed; 40 vials rejected and scrapped at receipt'),
('AUS1-R-26-0107', '2026-08-10 16:10:00+00', 'ohaddad', 'A', NULL),
('AUS1-R-26-0108', '2026-08-17 10:45:00+00', 'ohaddad', 'A', NULL),
('AUS1-R-26-0109', '2026-09-03 09:55:00+00', 'sadeyemi', 'A', NULL),
('AUS1-R-26-0110', '2026-09-14 15:30:00+00', 'ohaddad', 'A', NULL),
('AUS1-R-26-0111', '2026-09-22 13:15:00+00', 'ohaddad', 'A', NULL),
('AUS1-R-26-0112', '2026-09-28 11:00:00+00', 'sadeyemi', 'H', 'Supplier certificate missing from shipment paperwork; lot held at dock'),
('AUS1-R-26-0112', '2026-09-29 09:10:00+00', 'ohaddad', 'A', 'Certificate received by email and matched to the lot')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS manhattan_wms.batch_master (
  batch_nbr             varchar(40) NOT NULL,
  item_id               integer NOT NULL,
  batch_status          char(1) NOT NULL,
  expire_date           date,
  vendor_batch_nbr      varchar(40),
  quarantine_start_dttm timestamptz NOT NULL,
  ref_field_1           varchar(40),
  mod_dttm              timestamptz NOT NULL,
  CONSTRAINT batch_master_pk PRIMARY KEY (batch_nbr, item_id)
);
COMMENT ON TABLE manhattan_wms.batch_master IS 'Lot/batch master with the system-enforced status (Q quarantine, R released, X rejected); ref_field_1 = LIMS sample ID.';

INSERT INTO manhattan_wms.batch_master (batch_nbr, item_id, batch_status, expire_date, vendor_batch_nbr, quarantine_start_dttm, ref_field_1, mod_dttm) VALUES
('RM26-0098', 60012, 'R', '2026-12-31', 'GCC-MED-260603', '2026-06-15 11:20:00+00', 'S26-026102', '2026-06-19 15:30:00+00'),
('RM26-0101', 60001, 'R', '2029-05-31', 'HH-LOS-2605117', '2026-06-22 14:10:00+00', 'S26-026104', '2026-07-02 16:20:00+00'),
('RM26-0102', 60006, 'R', '2029-03-31', 'DFE-102-6612004', '2026-06-24 09:35:00+00', 'S26-026106', '2026-06-30 11:05:00+00'),
('RM26-0103', 60007, 'R', '2028-12-31', 'SPC-MS-1188342', '2026-06-24 10:20:00+00', 'S26-026108', '2026-06-29 15:45:00+00'),
('RM26-0104', 60002, 'R', '2029-01-31', 'DRL-CLP-26B0441', '2026-07-06 13:05:00+00', 'S26-026110', '2026-07-16 10:30:00+00'),
('RM26-0105', 60003, 'R', '2029-06-30', 'HPM-CIS-240771', '2026-07-13 11:50:00+00', 'S26-026112', '2026-07-24 14:00:00+00'),
('RM26-0106', 60010, 'R', '2031-07-31', 'SCH-V50-7781205', '2026-07-15 08:40:00+00', 'S26-026114', '2026-07-17 09:15:00+00'),
('RM26-0107', 60001, 'R', '2029-07-31', 'HH-LOS-2607203', '2026-08-10 15:25:00+00', 'S26-026116', '2026-08-21 13:40:00+00'),
('RM26-0108', 60005, 'R', '2028-08-31', 'SPC-MTX-1190087', '2026-08-17 10:00:00+00', 'S26-026118', '2026-08-27 16:10:00+00'),
('RM26-0109', 60009, 'X', '2029-08-31', 'ROQ-P-6014592', '2026-09-03 09:10:00+00', 'S26-026120', '2026-09-11 11:25:00+00'),
('RM26-0110', 60002, 'R', '2029-08-31', 'DRL-CLP-26C0917', '2026-09-14 14:45:00+00', 'S26-026122', '2026-09-24 10:50:00+00'),
('RM26-0111', 60012, 'Q', '2027-03-31', 'GCC-MED-260912', '2026-09-22 12:30:00+00', 'S26-026124', '2026-09-22 12:30:00+00'),
('RM26-0112', 60001, 'Q', '2029-08-31', 'HH-LOS-2609044', '2026-09-28 10:15:00+00', 'S26-026126', '2026-09-28 10:15:00+00'),
('RM25-0388', 60004, 'R', '2028-10-31', 'HPM-CBP-231904', '2025-11-03 10:40:00+00', NULL, '2025-11-03 10:40:00+00'),
('RM25-0412', 60010, 'R', '2030-11-30', 'SCH-V50-7719022', '2025-11-24 09:05:00+00', NULL, '2025-11-24 09:05:00+00'),
('A26-3000-0141', 61001, 'R', '2028-08-05', NULL, '2026-08-06 00:00:00+00', NULL, '2026-08-17 18:00:00+00'),
('A26-2050-0087', 61002, 'R', '2028-08-19', NULL, '2026-08-19 20:00:00+00', NULL, '2026-08-31 14:00:00+00'),
('A26-9000-0019', 61003, 'R', '2028-09-02', NULL, '2026-09-03 01:00:00+00', NULL, '2026-09-14 19:00:00+00'),
('A26-4410-0052', 61004, 'R', '2028-07-21', NULL, '2026-07-21 23:30:00+00', NULL, '2026-08-02 17:30:00+00'),
('A26-4630-0017', 61006, 'R', '2028-09-15', NULL, '2026-09-15 22:00:00+00', NULL, '2026-09-27 16:00:00+00'),
('A26-3000-0142', 61001, 'Q', '2028-09-09', NULL, '2026-09-10 00:00:00+00', NULL, '2026-09-21 18:00:00+00')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS manhattan_wms.wm_inventory (
  c_facility_id     integer NOT NULL,
  item_id           integer NOT NULL,
  batch_nbr         varchar(40) NOT NULL,
  location_id       varchar(20) NOT NULL,
  on_hand_qty       integer NOT NULL,
  last_updated_dttm timestamptz NOT NULL,
  CONSTRAINT wm_inventory_pk PRIMARY KEY (c_facility_id, item_id, batch_nbr, location_id)
);
COMMENT ON TABLE manhattan_wms.wm_inventory IS 'On-hand inventory by facility, item, batch and location (base units).';

INSERT INTO manhattan_wms.wm_inventory (c_facility_id, item_id, batch_nbr, location_id, on_hand_qty, last_updated_dttm) VALUES
(10, 60004, 'RM25-0388', 'AUS1-RM-A06', 520, '2026-09-30 05:00:00+00'),
(10, 60010, 'RM25-0412', 'AUS1-RM-A08', 1740, '2026-09-30 05:00:00+00'),
(10, 60012, 'RM26-0098', 'AUS1-CR-01', 30000, '2026-09-30 05:00:00+00'),
(10, 60001, 'RM26-0101', 'AUS1-RM-A04', 237600, '2026-09-30 05:00:00+00'),
(10, 60006, 'RM26-0102', 'AUS1-RM-A03', 736000, '2026-09-30 05:00:00+00'),
(10, 60007, 'RM26-0103', 'AUS1-RM-A01', 38900, '2026-09-30 05:00:00+00'),
(10, 60002, 'RM26-0104', 'AUS1-RM-A08', 171100, '2026-09-30 05:00:00+00'),
(10, 60003, 'RM26-0105', 'AUS1-RM-A06', 469, '2026-09-30 05:00:00+00'),
(10, 60010, 'RM26-0106', 'AUS1-RM-A09', 1330, '2026-09-30 05:00:00+00'),
(10, 60001, 'RM26-0107', 'AUS1-RM-A02', 237600, '2026-09-30 05:00:00+00'),
(10, 60005, 'RM26-0108', 'AUS1-RM-A02', 170, '2026-09-30 05:00:00+00'),
(10, 60002, 'RM26-0110', 'AUS1-RM-A08', 171100, '2026-09-30 05:00:00+00'),
(10, 60012, 'RM26-0111', 'AUS1-QUAR-01', 60000, '2026-09-30 05:00:00+00'),
(10, 60001, 'RM26-0112', 'AUS1-QUAR-01', 250000, '2026-09-30 05:00:00+00'),
(20, 61002, 'A26-2050-0087', 'AUS2-FG-B08', 1780, '2026-09-30 05:00:00+00'),
(20, 61001, 'A26-3000-0141', 'AUS2-FG-B08', 720, '2026-09-30 05:00:00+00'),
(20, 61001, 'A26-3000-0142', 'AUS2-QUAR-01', 1330, '2026-09-30 05:00:00+00'),
(20, 61004, 'A26-4410-0052', 'AUS2-FG-B06', 1680, '2026-09-30 05:00:00+00'),
(20, 61006, 'A26-4630-0017', 'AUS2-FG-B04', 3550, '2026-09-30 05:00:00+00'),
(20, 61003, 'A26-9000-0019', 'AUS2-FG-B08', 1000, '2026-09-30 05:00:00+00')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS manhattan_wms.pix_tran (
  pix_tran_id      bigint NOT NULL,
  tran_type        varchar(3) NOT NULL,
  tran_code        varchar(2) NOT NULL,
  item_name        varchar(40) NOT NULL,
  batch_nbr        varchar(40),
  invn_adjmt_qty   integer NOT NULL,
  invn_adjmt_type  char(1) NOT NULL,
  whse             varchar(10) NOT NULL,
  reason_code      varchar(4),
  ref_field_1      varchar(40),
  ref_field_2      varchar(10),
  create_date_time timestamptz NOT NULL,
  CONSTRAINT pix_tran_pk PRIMARY KEY (pix_tran_id)
);
COMMENT ON TABLE manhattan_wms.pix_tran IS 'Perpetual inventory transactions (100 receipt, 200 transfer in, 300/01 production issue, 300/02 adjustment, 606 ship/return); ref_field_2 = batch status at transaction.';

INSERT INTO manhattan_wms.pix_tran (pix_tran_id, tran_type, tran_code, item_name, batch_nbr, invn_adjmt_qty, invn_adjmt_type, whse, reason_code, ref_field_1, ref_field_2, create_date_time) VALUES
(8810007, '100', '01', 'RM-400410', 'RM26-0098', 40000, 'A', 'AUS1', NULL, 'AUS1-R-26-0098', NULL, '2026-06-15 11:20:00+00'),
(8810014, '100', '01', 'RM-100110', 'RM26-0101', 250000, 'A', 'AUS1', NULL, 'AUS1-R-26-0101', NULL, '2026-06-22 14:10:00+00'),
(8810021, '100', '01', 'RM-200210', 'RM26-0102', 800000, 'A', 'AUS1', NULL, 'AUS1-R-26-0102', NULL, '2026-06-24 09:35:00+00'),
(8810028, '100', '01', 'RM-200220', 'RM26-0103', 40000, 'A', 'AUS1', NULL, 'AUS1-R-26-0103', NULL, '2026-06-24 10:20:00+00'),
(8810035, '100', '01', 'RM-100120', 'RM26-0104', 180000, 'A', 'AUS1', NULL, 'AUS1-R-26-0104', NULL, '2026-07-06 13:05:00+00'),
(8810042, '100', '01', 'RM-100130', 'RM26-0105', 600, 'A', 'AUS1', NULL, 'AUS1-R-26-0105', NULL, '2026-07-13 11:50:00+00'),
(8810049, '100', '01', 'PK-300310', 'RM26-0106', 8000, 'A', 'AUS1', NULL, 'AUS1-R-26-0106', NULL, '2026-07-15 08:40:00+00'),
(8810056, '300', '02', 'PK-300310', 'RM26-0106', 40, 'S', 'AUS1', 'DM', 'AUS1-R-26-0106', NULL, '2026-07-15 09:45:00+00'),
(8810063, '100', '01', 'RM-100110', 'RM26-0107', 250000, 'A', 'AUS1', NULL, 'AUS1-R-26-0107', NULL, '2026-08-10 15:25:00+00'),
(8810070, '100', '01', 'RM-100150', 'RM26-0108', 1200, 'A', 'AUS1', NULL, 'AUS1-R-26-0108', NULL, '2026-08-17 10:00:00+00'),
(8810077, '100', '01', 'RM-200240', 'RM26-0109', 300000, 'A', 'AUS1', NULL, 'AUS1-R-26-0109', NULL, '2026-09-03 09:10:00+00'),
(8810084, '606', '02', 'RM-200240', 'RM26-0109', 300000, 'S', 'AUS1', 'RV', 'RTV-26-0019', NULL, '2026-09-14 10:30:00+00'),
(8810091, '100', '01', 'RM-100120', 'RM26-0110', 180000, 'A', 'AUS1', NULL, 'AUS1-R-26-0110', NULL, '2026-09-14 14:45:00+00'),
(8810098, '100', '01', 'RM-400410', 'RM26-0111', 60000, 'A', 'AUS1', NULL, 'AUS1-R-26-0111', NULL, '2026-09-22 12:30:00+00'),
(8810105, '100', '01', 'RM-100110', 'RM26-0112', 250000, 'A', 'AUS1', NULL, 'AUS1-R-26-0112', NULL, '2026-09-28 10:15:00+00'),
(8810112, '300', '01', 'RM-100110', 'RM26-0101', 12400, 'S', 'AUS1', 'PI', 'A26-3000-0141', 'R', '2026-08-03 05:30:00+00'),
(8810119, '300', '01', 'RM-200210', 'RM26-0102', 18000, 'S', 'AUS1', 'PI', 'A26-3000-0141', 'R', '2026-08-03 05:30:00+00'),
(8810126, '300', '01', 'RM-200220', 'RM26-0103', 300, 'S', 'AUS1', 'PI', 'A26-3000-0141', 'R', '2026-08-03 05:30:00+00'),
(8810133, '300', '01', 'RM-100120', 'RM26-0104', 8900, 'S', 'AUS1', 'PI', 'A26-2050-0087', 'R', '2026-08-17 05:30:00+00'),
(8810140, '300', '01', 'RM-200210', 'RM26-0102', 14000, 'S', 'AUS1', 'PI', 'A26-2050-0087', 'R', '2026-08-17 05:30:00+00'),
(8810147, '300', '01', 'RM-200220', 'RM26-0103', 250, 'S', 'AUS1', 'PI', 'A26-2050-0087', 'R', '2026-08-17 05:30:00+00'),
(8810154, '300', '01', 'RM-100130', 'RM26-0105', 131, 'S', 'AUS1', 'PI', 'A26-9000-0019', 'R', '2026-09-01 06:30:00+00'),
(8810161, '300', '01', 'PK-300310', 'RM26-0106', 2550, 'S', 'AUS1', 'PI', 'A26-9000-0019', 'R', '2026-09-01 06:30:00+00'),
(8810168, '300', '01', 'RM-100110', 'RM26-0107', 12400, 'S', 'AUS1', 'PI', 'A26-3000-0142', 'R', '2026-09-07 05:30:00+00'),
(8810175, '300', '01', 'RM-200210', 'RM26-0102', 18000, 'S', 'AUS1', 'PI', 'A26-3000-0142', 'R', '2026-09-07 05:30:00+00'),
(8810182, '300', '01', 'RM-200220', 'RM26-0103', 300, 'S', 'AUS1', 'PI', 'A26-3000-0142', 'R', '2026-09-07 05:30:00+00'),
(8810189, '300', '01', 'RM-100120', 'RM26-0110', 8900, 'S', 'AUS1', 'PI', 'A26-2050-0088', 'R', '2026-09-28 05:30:00+00'),
(8810196, '300', '01', 'RM-200210', 'RM26-0102', 14000, 'S', 'AUS1', 'PI', 'A26-2050-0088', 'R', '2026-09-28 05:30:00+00'),
(8810203, '300', '01', 'RM-200220', 'RM26-0103', 250, 'S', 'AUS1', 'PI', 'A26-2050-0088', 'R', '2026-09-28 05:30:00+00'),
(8810210, '300', '01', 'RM-100140', 'RM25-0388', 1480, 'S', 'AUS1', 'PI', 'A26-4410-0052', 'R', '2026-07-20 06:30:00+00'),
(8810217, '300', '01', 'PK-300310', 'RM25-0412', 3260, 'S', 'AUS1', 'PI', 'A26-4410-0052', 'R', '2026-07-20 06:30:00+00'),
(8810224, '300', '01', 'RM-100150', 'RM26-0108', 1030, 'S', 'AUS1', 'PI', 'A26-4630-0017', 'R', '2026-09-14 06:30:00+00'),
(8810231, '300', '01', 'PK-300310', 'RM26-0106', 4080, 'S', 'AUS1', 'PI', 'A26-4630-0017', 'R', '2026-09-14 06:30:00+00'),
(8810238, '300', '01', 'RM-400410', 'RM26-0098', 2500, 'S', 'AUS1', 'PI', 'A26-7710-P015', 'R', '2026-07-13 06:30:00+00'),
(8810245, '300', '01', 'RM-400410', 'RM26-0098', 2500, 'S', 'AUS1', 'PI', 'A26-7710-P016', 'R', '2026-08-10 06:30:00+00'),
(8810252, '300', '01', 'RM-400410', 'RM26-0098', 2500, 'S', 'AUS1', 'PI', 'A26-7710-P017', 'R', '2026-09-01 06:30:00+00'),
(8810259, '300', '01', 'RM-400410', 'RM26-0098', 2500, 'S', 'AUS1', 'PI', 'A26-7710-P018', 'R', '2026-09-15 06:30:00+00'),
(8810266, '200', '01', '3000', 'A26-3000-0141', 1320, 'A', 'AUS2', 'TI', 'A26-3000-0141', 'R', '2026-08-06 00:00:00+00'),
(8810273, '200', '01', '2050', 'A26-2050-0087', 2980, 'A', 'AUS2', 'TI', 'A26-2050-0087', 'R', '2026-08-19 20:00:00+00'),
(8810280, '200', '01', '9000', 'A26-9000-0019', 2450, 'A', 'AUS2', 'TI', 'A26-9000-0019', 'R', '2026-09-03 01:00:00+00'),
(8810287, '200', '01', 'AU-4410', 'A26-4410-0052', 3180, 'A', 'AUS2', 'TI', 'A26-4410-0052', 'R', '2026-07-21 23:30:00+00'),
(8810294, '200', '01', 'AU-4630', 'A26-4630-0017', 3950, 'A', 'AUS2', 'TI', 'A26-4630-0017', 'R', '2026-09-15 22:00:00+00'),
(8810301, '200', '01', '3000', 'A26-3000-0142', 1330, 'A', 'AUS2', 'TI', 'A26-3000-0142', 'Q', '2026-09-10 00:00:00+00'),
(8810308, '606', '02', 'AU-4410', 'A26-4410-0052', 1500, 'S', 'AUS2', 'SH', 'SH-26-00412', 'R', '2026-08-06 14:00:00+00'),
(8810315, '606', '02', '3000', 'A26-3000-0141', 600, 'S', 'AUS2', 'SH', 'SH-26-00428', 'R', '2026-08-20 13:30:00+00'),
(8810322, '606', '02', '2050', 'A26-2050-0087', 1200, 'S', 'AUS2', 'SH', 'SH-26-00433', 'R', '2026-08-27 15:10:00+00'),
(8810329, '606', '02', '9000', 'A26-9000-0019', 800, 'S', 'AUS2', 'SH', 'SH-26-00447', 'R', '2026-09-15 12:45:00+00'),
(8810336, '606', '02', '9000', 'A26-9000-0019', 650, 'S', 'AUS2', 'SH', 'SH-26-00451', 'R', '2026-09-18 11:20:00+00'),
(8810343, '606', '02', 'AU-4630', 'A26-4630-0017', 400, 'S', 'AUS2', 'SH', 'SH-26-00458', 'R', '2026-09-24 09:40:00+00')
ON CONFLICT DO NOTHING;

-- Subscription inbound: tables and columns written by the coco_subscriptions_austin_systems DAG from the
-- digital products this system subscribes to (see coco-subscription-loads/austin_systems/manhattan_wms).
-- No extract reads them.

CREATE TABLE IF NOT EXISTS manhattan_wms.business_partner (
  business_partner_id varchar(20) NOT NULL,
  description         varchar(200) NOT NULL,
  bp_type             varchar(40) NOT NULL,
  country_code        varchar(60) NOT NULL,
  approved_flag       char(1) NOT NULL,
  approved_date       date,
  bp_status           varchar(20) NOT NULL,
  CONSTRAINT business_partner_pk PRIMARY KEY (business_partner_id)
);
COMMENT ON TABLE manhattan_wms.business_partner IS 'Business partners (suppliers, business partner ID = SAP vendor number) and their approval, from Supplier Master Data.';

CREATE TABLE IF NOT EXISTS manhattan_wms.supplier_cert (
  cert_nbr            varchar(40) NOT NULL,
  business_partner_id varchar(20) NOT NULL,
  item_name           varchar(40) NOT NULL,
  vendor_batch_nbr    varchar(40) NOT NULL,
  cert_type           varchar(40) NOT NULL,
  cert_date           date NOT NULL,
  conforming          char(1) NOT NULL,
  CONSTRAINT supplier_cert_pk PRIMARY KEY (cert_nbr)
);
COMMENT ON TABLE manhattan_wms.supplier_cert IS 'Supplier certificates matched at receipt to the ASN line certificate number, from Supplier Material Certificates.';

CREATE TABLE IF NOT EXISTS manhattan_wms.batch_coa (
  batch_nbr   varchar(40) NOT NULL,
  coa_nbr     varchar(40) NOT NULL,
  coa_date    date NOT NULL,
  conforming  char(1) NOT NULL,
  approved_by varchar(40) NOT NULL,
  CONSTRAINT batch_coa_pk PRIMARY KEY (batch_nbr, coa_nbr)
);
COMMENT ON TABLE manhattan_wms.batch_coa IS 'Laboratory certificates of analysis for lots and batches held in the WMS, from Laboratory Test Results.';

CREATE TABLE IF NOT EXISTS manhattan_wms.srl_nbr_track (
  srl_nbr        varchar(40) NOT NULL,
  item_name      varchar(20) NOT NULL,
  gtin           varchar(20) NOT NULL,
  batch_nbr      varchar(40) NOT NULL,
  expire_date    date NOT NULL,
  market         varchar(8) NOT NULL,
  srl_status     varchar(20) NOT NULL,
  parent_srl_nbr varchar(40),
  whse           varchar(20),
  CONSTRAINT srl_nbr_track_pk PRIMARY KEY (srl_nbr)
);
COMMENT ON TABLE manhattan_wms.srl_nbr_track IS 'Serial numbers of packs held or expected in the warehouses, from Serialised Product Identifiers.';

CREATE TABLE IF NOT EXISTS manhattan_wms.srl_nbr_track_event (
  srl_nbr       varchar(40) NOT NULL,
  event_dttm    timestamptz NOT NULL,
  event_type    varchar(20) NOT NULL,
  source_system varchar(60) NOT NULL,
  alert_id      varchar(40),
  CONSTRAINT srl_nbr_track_event_pk PRIMARY KEY (srl_nbr, event_dttm)
);
COMMENT ON TABLE manhattan_wms.srl_nbr_track_event IS 'Pack serial number events (commission, verify, decommission, alert), from Serialised Product Identifiers.';

GRANT USAGE ON SCHEMA manhattan_wms TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA manhattan_wms TO egeria_user, airflow_user;
