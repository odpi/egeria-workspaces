-- system-qualified-name: SoftwareServer::AUS-SYS-043::SN-MDM-AU-20220301
-- Informatica MDM - Austin.  Informatica Multidomain MDM hub for Austin: golden product and supplier records (with
-- packs, handling, market authorisations, screening, bank accounts and bank-change verifications) and the product
-- change notices it publishes.  Its tables feed Product Master Data, Product Change Notifications, Supplier Master
-- Data and Supplier Payment Detail Changes.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS informatica_mdm;
COMMENT ON SCHEMA informatica_mdm IS 'Informatica MDM Hub Store (Austin ORS): base objects (C_B_*) and cross-references.';

CREATE TABLE IF NOT EXISTS informatica_mdm.c_b_product (
  rowid_object         char(14) NOT NULL,
  product_cd           varchar(20) NOT NULL,
  product_nm           varchar(120) NOT NULL,
  product_desc         text,
  product_type_cd      varchar(20) NOT NULL,
  active_ingredient_nm varchar(120) NOT NULL,
  strength_txt         varchar(40),
  lifecycle_status_cd  varchar(20) NOT NULL,
  version_no           varchar(20) NOT NULL,
  hub_state_ind        integer NOT NULL,
  last_update_date     timestamptz NOT NULL,
  CONSTRAINT c_b_product_pk PRIMARY KEY (rowid_object)
);
COMMENT ON TABLE informatica_mdm.c_b_product IS 'Golden product records.';

INSERT INTO informatica_mdm.c_b_product (rowid_object, product_cd, product_nm, product_desc, product_type_cd, active_ingredient_nm, strength_txt, lifecycle_status_cd, version_no, hub_state_ind, last_update_date) VALUES
('          1001', '3000', 'Cozaar 100mg film-coated tablets', 'Losartan potassium 100 mg film-coated tablet, made at Austin for Coco Pharmaceuticals', 'STANDARD', 'Losartan potassium', '100 mg', 'MARKETED', '4.2', 1, '2026-09-18 15:20:00+00'),
('          1002', '2050', 'Plavix 75mg film-coated tablets', 'Clopidogrel bisulfate 75 mg film-coated tablet, made at Austin for Coco Pharmaceuticals', 'STANDARD', 'Clopidogrel bisulfate', '75 mg', 'MARKETED', '3.1', 1, '2026-09-18 15:20:00+00'),
('          1003', '9000', 'Cisplatin 50mg/50mL injection', 'Cisplatin 1 mg/mL concentrate for infusion, single-dose vial, made at Austin for Coco Pharmaceuticals', 'STANDARD', 'Cisplatin', '50 mg/50 mL', 'MARKETED', '2.4', 1, '2026-09-18 15:20:00+00'),
('          1004', 'AU-4410', 'Carboplatin 450mg/45mL injection', 'Carboplatin 10 mg/mL multi-dose vial', 'STANDARD', 'Carboplatin', '450 mg/45 mL', 'MARKETED', '5.0', 1, '2026-09-18 15:20:00+00'),
('          1005', 'AU-4520', 'Oxaliplatin 100mg/20mL injection', 'Oxaliplatin 5 mg/mL single-dose vial', 'STANDARD', 'Oxaliplatin', '100 mg/20 mL', 'MARKETED', '2.1', 1, '2026-09-18 15:20:00+00'),
('          1006', 'AU-4630', 'Methotrexate 250mg/10mL injection', 'Methotrexate 25 mg/mL preservative-free vial', 'STANDARD', 'Methotrexate sodium', '250 mg/10 mL', 'MARKETED', '3.3', 1, '2026-09-18 15:20:00+00'),
('          1007', 'AU-7710', 'Dendrivax autologous dendritic cell suspension', 'Patient-specific autologous dendritic cell immunotherapy, supplied cryopreserved in a single infusion bag under Austin''s named-patient programme', 'PERSONALISED', 'Autologous dendritic cells', '20 million cells/bag', 'MARKETED', '1.3', 1, '2026-09-18 15:20:00+00')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS informatica_mdm.c_b_product_pack (
  rowid_object       char(14) NOT NULL,
  rowid_product      char(14) NOT NULL,
  pack_cd            varchar(20) NOT NULL,
  pack_desc          text,
  units_per_pack     integer NOT NULL,
  destination_mkt_cd varchar(8) NOT NULL,
  serialised_ind     char(1) NOT NULL,
  hub_state_ind      integer NOT NULL,
  CONSTRAINT c_b_product_pack_pk PRIMARY KEY (rowid_object)
);
COMMENT ON TABLE informatica_mdm.c_b_product_pack IS 'Pack configurations (child of product).';

INSERT INTO informatica_mdm.c_b_product_pack (rowid_object, rowid_product, pack_cd, pack_desc, units_per_pack, destination_mkt_cd, serialised_ind, hub_state_ind) VALUES
('          2001', '          1001', '72614-300-90', 'Bottle of 90 film-coated tablets', 90, 'US', 'Y', 1),
('          2002', '          1001', '72614-300-30', 'Bottle of 30 film-coated tablets', 30, 'US', 'Y', 1),
('          2003', '          1001', 'CA-3000-30', 'Bottle of 30 film-coated tablets, Canadian labelling', 30, 'CA', 'N', 1),
('          2004', '          1002', '72614-205-30', 'Bottle of 30 film-coated tablets', 30, 'US', 'Y', 1),
('          2005', '          1003', '72614-900-01', 'Single-dose vial 50 mL in carton', 1, 'US', 'Y', 1),
('          2006', '          1003', 'CA-9000-01', 'Single-dose vial 50 mL in carton, Canadian labelling', 1, 'CA', 'N', 1),
('          2007', '          1004', '72614-441-01', 'Multi-dose vial 45 mL in carton', 1, 'US', 'Y', 1),
('          2008', '          1005', '72614-452-01', 'Single-dose vial 20 mL in carton', 1, 'US', 'Y', 1),
('          2009', '          1006', '72614-463-01', 'Single-dose vial 10 mL in carton', 1, 'US', 'Y', 1),
('          2010', '          1007', '72614-771-01', 'Patient-specific infusion bag in cryocassette', 1, 'US', 'Y', 1)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS informatica_mdm.c_b_product_handling (
  rowid_object        char(14) NOT NULL,
  rowid_product       char(14) NOT NULL,
  min_storage_temp_c  numeric(6,1) NOT NULL,
  max_storage_temp_c  numeric(6,1) NOT NULL,
  transport_hazard_cd varchar(20),
  packaging_desc      text,
  shelf_life_days     integer NOT NULL,
  hub_state_ind       integer NOT NULL,
  CONSTRAINT c_b_product_handling_pk PRIMARY KEY (rowid_object)
);
COMMENT ON TABLE informatica_mdm.c_b_product_handling IS 'Storage, transport and shelf-life requirements (child of product).';

INSERT INTO informatica_mdm.c_b_product_handling (rowid_object, rowid_product, min_storage_temp_c, max_storage_temp_c, transport_hazard_cd, packaging_desc, shelf_life_days, hub_state_ind) VALUES
('          3001', '          1001', 20, 25, NULL, 'HDPE bottle with desiccant; protect from moisture', 1095, 1),
('          3002', '          1002', 20, 25, NULL, 'HDPE bottle with desiccant', 730, 1),
('          3003', '          1003', 15, 25, 'UN1851', 'Amber vial in carton; cytotoxic labelling; do not refrigerate', 730, 1),
('          3004', '          1004', 20, 25, 'UN1851', 'Vial in carton; cytotoxic labelling', 730, 1),
('          3005', '          1005', 20, 25, 'UN1851', 'Vial in carton; cytotoxic labelling', 730, 1),
('          3006', '          1006', 20, 25, 'UN1851', 'Vial in carton; cytotoxic labelling', 1095, 1),
('          3007', '          1007', -196, -150, NULL, 'Cryobag in cryocassette in LN2 vapour-phase dry shipper; chain of identity seal', 180, 1)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS informatica_mdm.c_b_product_mkt_auth (
  rowid_object     char(14) NOT NULL,
  rowid_product    char(14) NOT NULL,
  market_cd        varchar(8) NOT NULL,
  authorisation_no varchar(40) NOT NULL,
  start_dt         date NOT NULL,
  end_dt           date,
  hub_state_ind    integer NOT NULL,
  CONSTRAINT c_b_product_mkt_auth_pk PRIMARY KEY (rowid_object)
);
COMMENT ON TABLE informatica_mdm.c_b_product_mkt_auth IS 'Marketing authorisations per market (child of product).';

INSERT INTO informatica_mdm.c_b_product_mkt_auth (rowid_object, rowid_product, market_cd, authorisation_no, start_dt, end_dt, hub_state_ind) VALUES
('          4001', '          1001', 'US', 'ANDA 078243', '2018-11-02', NULL, 1),
('          4002', '          1001', 'CA', 'DIN 02534001', '2020-06-15', NULL, 1),
('          4003', '          1002', 'US', 'ANDA 091358', '2019-03-11', NULL, 1),
('          4004', '          1003', 'US', 'ANDA 074656', '2018-09-24', NULL, 1),
('          4005', '          1003', 'CA', 'DIN 02534120', '2021-02-01', NULL, 1),
('          4006', '          1004', 'US', 'ANDA 077139', '2017-05-19', NULL, 1),
('          4007', '          1005', 'US', 'ANDA 078819', '2018-01-08', '2026-12-31', 1),
('          4008', '          1006', 'US', 'ANDA 040632', '2016-10-03', NULL, 1),
('          4009', '          1007', 'US', 'BLA 125812', '2025-11-20', NULL, 1)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS informatica_mdm.c_b_product_change (
  rowid_object  char(14) NOT NULL,
  change_ref    varchar(20) NOT NULL,
  rowid_product char(14) NOT NULL,
  change_desc   text NOT NULL,
  effective_dt  date NOT NULL,
  published_ts  timestamptz NOT NULL,
  hub_state_ind integer NOT NULL,
  CONSTRAINT c_b_product_change_pk PRIMARY KEY (rowid_object)
);
COMMENT ON TABLE informatica_mdm.c_b_product_change IS 'Product change notices published to consuming systems.';

INSERT INTO informatica_mdm.c_b_product_change (rowid_object, change_ref, rowid_product, change_desc, effective_dt, published_ts, hub_state_ind) VALUES
('          5001', 'PCN-26-0007', '          1001', 'Shelf life extended from 24 to 36 months on the basis of 36-month stability data', '2026-03-01', '2026-02-20 16:00:00+00', 1),
('          5002', 'PCN-26-0009', '          1003', 'New Canadian presentation CA-9000-01 added', '2026-05-15', '2026-05-08 14:30:00+00', 1),
('          5003', 'PCN-26-0011', '          1007', 'Storage upper limit changed to -150 C (vapour phase only)', '2026-07-01', '2026-06-24 11:10:00+00', 1),
('          5004', 'PCN-26-0014', '          1006', 'Transport hazard classification confirmed as UN1851 after SDS revision', '2026-08-17', '2026-08-12 09:45:00+00', 1),
('          5005', 'PCN-26-0016', '          1002', 'Serialisation required on pack 72614-205-30 (DSCSA)', '2026-09-21', '2026-09-18 15:20:00+00', 1)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS informatica_mdm.c_b_party (
  rowid_object            char(14) NOT NULL,
  party_type_cd           varchar(20) NOT NULL,
  org_nm                  varchar(200) NOT NULL,
  country_cd              varchar(2) NOT NULL,
  supplier_class_cd       varchar(20) NOT NULL,
  onboarding_approved_ind char(1) NOT NULL,
  onboarding_approved_dt  date,
  status_cd               varchar(10) NOT NULL,
  hub_state_ind           integer NOT NULL,
  CONSTRAINT c_b_party_pk PRIMARY KEY (rowid_object)
);
COMMENT ON TABLE informatica_mdm.c_b_party IS 'Golden party records (suppliers).';

INSERT INTO informatica_mdm.c_b_party (rowid_object, party_type_cd, org_nm, country_cd, supplier_class_cd, onboarding_approved_ind, onboarding_approved_dt, status_cd, hub_state_ind) VALUES
('          9001', 'SUPPLIER', 'Zhejiang Huahai Pharmaceutical Co., Ltd.', 'CN', 'MATERIAL', 'Y', '2018-10-02', 'A', 1),
('          9002', 'SUPPLIER', 'Dr. Reddy''s Laboratories Ltd', 'IN', 'MATERIAL', 'Y', '2018-10-02', 'A', 1),
('          9003', 'SUPPLIER', 'Heraeus Precious Metals GmbH & Co. KG', 'DE', 'MATERIAL', 'Y', '2018-11-15', 'A', 1),
('          9004', 'SUPPLIER', 'DFE Pharma GmbH & Co. KG', 'DE', 'MATERIAL', 'Y', '2019-02-11', 'A', 1),
('          9005', 'SUPPLIER', 'Spectrum Chemical Mfg. Corp.', 'US', 'MATERIAL', 'Y', '2018-10-02', 'A', 1),
('          9006', 'SUPPLIER', 'SCHOTT Pharma USA, Inc.', 'US', 'MATERIAL', 'Y', '2019-01-21', 'A', 1),
('          9007', 'SUPPLIER', 'Berry Global, Inc.', 'US', 'MATERIAL', 'Y', '2019-01-21', 'A', 1),
('          9008', 'SUPPLIER', 'Roquette America, Inc.', 'US', 'MATERIAL', 'Y', '2020-03-09', 'A', 1),
('          9009', 'SUPPLIER', 'Lonestar Calibration Services LLC', 'US', 'SERVICE', 'Y', '2019-06-17', 'A', 1),
('          9010', 'SUPPLIER', 'Hill Country Facilities, Inc.', 'US', 'SERVICE', 'Y', '2020-09-28', 'A', 1),
('          9011', 'SUPPLIER', 'Lifeline Biologistics LLC', 'US', 'SERVICE', 'Y', '2021-10-04', 'A', 1),
('          9012', 'SUPPLIER', 'Gulf Coast Cryogenics, Inc.', 'US', 'MATERIAL', 'Y', '2025-04-14', 'A', 1),
('          9013', 'SUPPLIER', 'Lone Star Cold Chain Couriers LLC', 'US', 'SERVICE', 'Y', '2026-08-19', 'A', 1),
('          9014', 'SUPPLIER', 'Hyderabad Fine Chemicals Pvt Ltd', 'IN', 'MATERIAL', 'N', NULL, 'S', 1)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS informatica_mdm.c_b_party_xref (
  rowid_xref      varchar(20) NOT NULL,
  rowid_object    char(14) NOT NULL,
  rowid_system    varchar(20) NOT NULL,
  pkey_src_object varchar(40) NOT NULL,
  CONSTRAINT c_b_party_xref_pk PRIMARY KEY (rowid_xref)
);
COMMENT ON TABLE informatica_mdm.c_b_party_xref IS 'Cross-references of each golden supplier to source system keys.';

INSERT INTO informatica_mdm.c_b_party_xref (rowid_xref, rowid_object, rowid_system, pkey_src_object) VALUES
('X90011', '          9001', 'SAP_S4', '100010'),
('X90012', '          9001', 'ARIBA', 'S200300030'),
('X90021', '          9002', 'SAP_S4', '100020'),
('X90022', '          9002', 'ARIBA', 'S200300060'),
('X90031', '          9003', 'SAP_S4', '100030'),
('X90032', '          9003', 'ARIBA', 'S200300090'),
('X90041', '          9004', 'SAP_S4', '100040'),
('X90042', '          9004', 'ARIBA', 'S200300120'),
('X90051', '          9005', 'SAP_S4', '100050'),
('X90052', '          9005', 'ARIBA', 'S200300150'),
('X90061', '          9006', 'SAP_S4', '100060'),
('X90062', '          9006', 'ARIBA', 'S200300180'),
('X90071', '          9007', 'SAP_S4', '100070'),
('X90072', '          9007', 'ARIBA', 'S200300210'),
('X90081', '          9008', 'SAP_S4', '100080'),
('X90082', '          9008', 'ARIBA', 'S200300240'),
('X90091', '          9009', 'SAP_S4', '100090'),
('X90092', '          9009', 'ARIBA', 'S200300270'),
('X90101', '          9010', 'SAP_S4', '100100'),
('X90102', '          9010', 'ARIBA', 'S200300300'),
('X90111', '          9011', 'SAP_S4', '100110'),
('X90112', '          9011', 'ARIBA', 'S200300330'),
('X90121', '          9012', 'SAP_S4', '100120'),
('X90122', '          9012', 'ARIBA', 'S200300360'),
('X90131', '          9013', 'SAP_S4', '100140'),
('X90132', '          9013', 'ARIBA', 'S200300420'),
('X90141', '          9014', 'SAP_S4', '100130'),
('X90142', '          9014', 'ARIBA', 'S200300390')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS informatica_mdm.c_b_party_screening (
  rowid_object     char(14) NOT NULL,
  rowid_party      char(14) NOT NULL,
  screen_status_cd varchar(3) NOT NULL,
  screened_dt      date NOT NULL,
  risk_rating_cd   varchar(10) NOT NULL,
  screening_ref    varchar(40) NOT NULL,
  anomaly_ref      varchar(40),
  CONSTRAINT c_b_party_screening_pk PRIMARY KEY (rowid_object)
);
COMMENT ON TABLE informatica_mdm.c_b_party_screening IS 'Latest screening result per supplier (from Ariba supplier risk) and any payment anomaly reference.';

INSERT INTO informatica_mdm.c_b_party_screening (rowid_object, rowid_party, screen_status_cd, screened_dt, risk_rating_cd, screening_ref, anomaly_ref) VALUES
('          9501', '          9001', 'CLR', '2026-01-10', 'MEDIUM', 'SCR-26-0040', NULL),
('          9502', '          9002', 'CLR', '2026-02-11', 'MEDIUM', 'SCR-26-0047', NULL),
('          9503', '          9003', 'CLR', '2026-03-12', 'LOW', 'SCR-26-0054', NULL),
('          9504', '          9004', 'CLR', '2026-04-13', 'LOW', 'SCR-26-0061', NULL),
('          9505', '          9005', 'CLR', '2026-05-14', 'LOW', 'SCR-26-0068', NULL),
('          9506', '          9006', 'CLR', '2026-06-15', 'LOW', 'SCR-26-0075', NULL),
('          9507', '          9007', 'CLR', '2026-07-16', 'LOW', 'SCR-26-0082', NULL),
('          9508', '          9008', 'CLR', '2026-08-17', 'LOW', 'SCR-26-0089', NULL),
('          9509', '          9009', 'CLR', '2026-01-18', 'LOW', 'SCR-26-0096', NULL),
('          9510', '          9010', 'REV', '2026-02-19', 'HIGH', 'SCR-26-0103', 'ANM-26-0007'),
('          9511', '          9011', 'CLR', '2026-03-20', 'MEDIUM', 'SCR-26-0110', NULL),
('          9512', '          9012', 'CLR', '2026-04-21', 'LOW', 'SCR-26-0117', NULL),
('          9514', '          9013', 'CLR', '2026-07-08', 'LOW', 'SCR-26-0164', NULL),
('          9513', '          9014', 'BLK', '2026-07-27', 'HIGH', 'SCR-26-0180', 'ANM-26-0005')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS informatica_mdm.c_b_party_bank_acct (
  rowid_object       char(14) NOT NULL,
  rowid_party        char(14) NOT NULL,
  bank_acct_key      varchar(40) NOT NULL,
  bank_nm            varchar(120) NOT NULL,
  bank_country_cd    varchar(2) NOT NULL,
  change_request_ref varchar(20) NOT NULL,
  verified_dt        date NOT NULL,
  eff_end_dt         date,
  hub_state_ind      integer NOT NULL,
  CONSTRAINT c_b_party_bank_acct_pk PRIMARY KEY (rowid_object)
);
COMMENT ON TABLE informatica_mdm.c_b_party_bank_acct IS 'Current remittance bank account per supplier and the change request that set it.';

INSERT INTO informatica_mdm.c_b_party_bank_acct (rowid_object, rowid_party, bank_acct_key, bank_nm, bank_country_cd, change_request_ref, verified_dt, eff_end_dt, hub_state_ind) VALUES
('          9701', '          9001', 'CN-BOCH-7710044581230', 'Bank of China, Taizhou Branch', 'CN', 'BCR-26-0007', '2026-05-22', NULL, 1),
('          9702', '          9002', 'IN-HDFC-50200011873421', 'HDFC Bank, Hyderabad', 'IN', 'BCR-18-9001', '2018-10-02', NULL, 1),
('          9703', '          9003', 'DE89370400440532013000', 'Commerzbank AG, Hanau', 'DE', 'BCR-18-9002', '2018-11-15', NULL, 1),
('          9704', '          9004', 'DE44500105175407324931', 'Deutsche Bank AG, Goch', 'DE', 'BCR-19-9003', '2019-02-11', NULL, 1),
('          9705', '          9005', 'US-021000021-4471902233', 'JPMorgan Chase Bank, N.A.', 'US', 'BCR-26-0004', '2026-03-12', NULL, 1),
('          9706', '          9006', 'US-026009593-0038812765', 'Bank of America, N.A.', 'US', 'BCR-19-9005', '2019-01-21', NULL, 1),
('          9707', '          9007', 'US-071000013-7712004455', 'JPMorgan Chase Bank, N.A.', 'US', 'BCR-19-9006', '2019-01-21', NULL, 1),
('          9708', '          9008', 'US-071923909-5590112834', 'BMO Bank N.A.', 'US', 'BCR-20-9007', '2020-03-09', NULL, 1),
('          9709', '          9009', 'US-111000025-3319002871', 'Frost Bank', 'US', 'BCR-26-0009', '2026-07-15', NULL, 1),
('          9710', '          9010', 'US-114000093-2208847710', 'Broadway Bank', 'US', 'BCR-20-9009', '2020-09-28', NULL, 1),
('          9711', '          9011', 'US-111000614-6603391452', 'Wells Fargo Bank, N.A.', 'US', 'BCR-21-9010', '2021-10-04', NULL, 1),
('          9712', '          9012', 'US-113000023-8810023347', 'Amegy Bank', 'US', 'BCR-25-9011', '2025-04-14', NULL, 1),
('          9714', '          9013', 'US-111901014-4120087736', 'Texas Capital Bank', 'US', 'BCR-26-9012', '2026-08-19', NULL, 1),
('          9713', '          9014', 'IN-ICIC-000405018876', 'ICICI Bank, Hyderabad', 'IN', 'BCR-19-9013', '2026-07-29', NULL, 1)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS informatica_mdm.c_b_party_bank_verif (
  rowid_object       char(14) NOT NULL,
  change_request_ref varchar(20) NOT NULL,
  rowid_party        char(14) NOT NULL,
  verified_ts        timestamptz NOT NULL,
  verifier_user      varchar(40) NOT NULL,
  channel_desc       varchar(60) NOT NULL,
  notes_txt          text,
  CONSTRAINT c_b_party_bank_verif_pk PRIMARY KEY (rowid_object)
);
COMMENT ON TABLE informatica_mdm.c_b_party_bank_verif IS 'Independent verification steps recorded by the data steward task for each bank change request.';

INSERT INTO informatica_mdm.c_b_party_bank_verif (rowid_object, change_request_ref, rowid_party, verified_ts, verifier_user, channel_desc, notes_txt) VALUES
('          9941', 'BCR-26-0004', '          9005', '2026-03-12 10:40:00+00', 'moneill', 'call-back to number on file', 'Controller confirmed the bank move to Chase'),
('          9971', 'BCR-26-0007', '          9001', '2026-05-22 01:30:00+00', 'moneill', 'call-back to number on file', 'Confirmed with finance manager in Taizhou; new branch account'),
('          9991', 'BCR-26-0009', '          9009', '2026-07-15 09:00:00+00', 'moneill', 'call-back to number on file', 'No answer; voicemail left'),
('          9992', 'BCR-26-0009', '          9009', '2026-07-15 15:20:00+00', 'moneill', 'call-back to number on file', 'Owner confirmed the change'),
('         10011', 'BCR-26-0011', '          9010', '2026-08-27 11:10:00+00', 'moneill', 'call-back to number on file', 'Supplier did not request any change; sender domain is a lookalike. Reported to IT security')
ON CONFLICT DO NOTHING;

-- Subscription inbound: tables and columns written by the coco_subscriptions_austin_systems DAG from the
-- digital products this system subscribes to (see coco-subscription-loads/austin_systems/informatica_mdm).
-- No extract reads them.

CREATE TABLE IF NOT EXISTS informatica_mdm.c_l_product (
  rowid_system         varchar(20) NOT NULL,
  pkey_src_object      varchar(40) NOT NULL,
  product_cd           varchar(20) NOT NULL,
  product_nm           varchar(120) NOT NULL,
  product_desc         text,
  product_type_cd      varchar(40),
  active_ingredient_nm varchar(120),
  strength_txt         varchar(40),
  lifecycle_status_cd  varchar(20),
  version_no           varchar(20),
  candidate_ref        varchar(40),
  formulation_ref      varchar(40),
  clinical_trial_ref   varchar(40),
  handover_dt          date,
  min_storage_temp_c   numeric(6,1),
  max_storage_temp_c   numeric(6,1),
  transport_hazard_cd  varchar(20),
  packaging_desc       text,
  shelf_life_days      integer,
  CONSTRAINT c_l_product_pk PRIMARY KEY (rowid_system, pkey_src_object)
);
COMMENT ON TABLE informatica_mdm.c_l_product IS 'Landing table for product records (and their handling) from the Data Sharing Hub: Product Master Data, New Product Definitions.';

CREATE TABLE IF NOT EXISTS informatica_mdm.c_l_product_pack (
  rowid_system       varchar(20) NOT NULL,
  pkey_src_object    varchar(40) NOT NULL,
  product_cd         varchar(20) NOT NULL,
  pack_desc          text,
  units_per_pack     integer NOT NULL,
  destination_mkt_cd varchar(8),
  serialised_ind     char(1),
  CONSTRAINT c_l_product_pack_pk PRIMARY KEY (rowid_system, pkey_src_object)
);
COMMENT ON TABLE informatica_mdm.c_l_product_pack IS 'Landing table for pack configurations from the Data Sharing Hub: Product Master Data, New Product Definitions.';

CREATE TABLE IF NOT EXISTS informatica_mdm.c_l_product_mkt_auth (
  rowid_system     varchar(20) NOT NULL,
  pkey_src_object  varchar(60) NOT NULL,
  product_cd       varchar(20) NOT NULL,
  market_cd        varchar(8) NOT NULL,
  authorisation_no varchar(40) NOT NULL,
  regulator_cd     varchar(20),
  start_dt         date NOT NULL,
  end_dt           date,
  status_cd        varchar(20),
  CONSTRAINT c_l_product_mkt_auth_pk PRIMARY KEY (rowid_system, pkey_src_object)
);
COMMENT ON TABLE informatica_mdm.c_l_product_mkt_auth IS 'Landing table for marketing authorisations from the Data Sharing Hub: Product Master Data, Market Authorisations.';

CREATE TABLE IF NOT EXISTS informatica_mdm.c_l_party (
  rowid_system    varchar(20) NOT NULL,
  pkey_src_object varchar(40) NOT NULL,
  org_nm          varchar(200) NOT NULL,
  country_cd      varchar(2) NOT NULL,
  owner_desc      text,
  requester_txt   varchar(40) NOT NULL,
  request_dt      date NOT NULL,
  status_cd       varchar(20) NOT NULL,
  sap_vendor_no   varchar(40),
  CONSTRAINT c_l_party_pk PRIMARY KEY (rowid_system, pkey_src_object)
);
COMMENT ON TABLE informatica_mdm.c_l_party IS 'Landing table for new supplier parties from approved onboarding cases (Data Sharing Hub: Third Party Onboarding Cases).';

CREATE TABLE IF NOT EXISTS informatica_mdm.c_l_party_screening (
  rowid_system     varchar(20) NOT NULL,
  pkey_src_object  varchar(40) NOT NULL,
  party_src_key    varchar(40) NOT NULL,
  screen_status_cd varchar(3) NOT NULL,
  screened_dt      date NOT NULL,
  risk_rating_cd   varchar(20),
  screening_ref    varchar(40),
  anomaly_ref      varchar(40),
  notes_txt        text,
  CONSTRAINT c_l_party_screening_pk PRIMARY KEY (rowid_system, pkey_src_object)
);
COMMENT ON TABLE informatica_mdm.c_l_party_screening IS 'Landing table for supplier screenings and payment anomaly concerns (Data Sharing Hub: Third Party Onboarding Cases, Payment Anomaly Findings).';

CREATE TABLE IF NOT EXISTS informatica_mdm.c_l_party_bank_acct (
  rowid_system       varchar(20) NOT NULL,
  pkey_src_object    varchar(40) NOT NULL,
  party_src_key      varchar(40) NOT NULL,
  bank_acct_key      varchar(40) NOT NULL,
  prev_bank_acct_key varchar(40),
  requested_ts       timestamptz NOT NULL,
  requester_txt      varchar(40) NOT NULL,
  change_status_cd   varchar(20) NOT NULL,
  CONSTRAINT c_l_party_bank_acct_pk PRIMARY KEY (rowid_system, pkey_src_object)
);
COMMENT ON TABLE informatica_mdm.c_l_party_bank_acct IS 'Landing table for supplier bank-detail changes awaiting the data steward verification task (Data Sharing Hub: Supplier Payment Detail Changes).';

GRANT USAGE ON SCHEMA informatica_mdm TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA informatica_mdm TO egeria_user, airflow_user;
