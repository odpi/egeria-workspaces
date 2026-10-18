-- system-qualified-name: System::cocoProducts
-- Coco Product Management - Coco core.  Homegrown product management system the board uses to plan product offerings, the only system holding product definitions; feeds Product Master Data.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS coco_products;
COMMENT ON SCHEMA coco_products IS 'Coco Product Management cocoProducts (Coco core): products, packs, handling conditions and market authorisations.';

CREATE TABLE IF NOT EXISTS coco_products.prd_mstr (
  prd_cd varchar(6) NOT NULL,
  prd_nm varchar(80) NOT NULL,
  prd_desc text,
  prd_typ char(1) NOT NULL,
  actv_ingr varchar(120) NOT NULL,
  strgth varchar(40),
  sts_cd varchar(3) NOT NULL,
  cur_ver varchar(10) NOT NULL,
  cat_id smallint,
  upd_dt date NOT NULL,
  CONSTRAINT prd_mstr_pk PRIMARY KEY (prd_cd)
);
COMMENT ON TABLE coco_products.prd_mstr IS 'Product master. prd_typ S standard, P personalised, I investigational; sts_cd DEV, MKT, SUS, WDN; cat_id is the Coco category.';

CREATE TABLE IF NOT EXISTS coco_products.prd_pack (
  pack_cd varchar(14) NOT NULL,
  prd_cd varchar(6) NOT NULL,
  pack_desc varchar(120),
  units_per_pack integer NOT NULL,
  dest_mkt varchar(2) NOT NULL,
  serial_yn char(1) NOT NULL,
  CONSTRAINT prd_pack_pk PRIMARY KEY (pack_cd)
);
COMMENT ON TABLE coco_products.prd_pack IS 'Pack presentations (GTIN-13) per destination market; dest_mkt uses UK for Great Britain; serial_yn Y where packs carry a serial number.';

CREATE TABLE IF NOT EXISTS coco_products.prd_hndl (
  prd_cd varchar(6) NOT NULL,
  store_min_c numeric(6,1) NOT NULL,
  store_max_c numeric(6,1) NOT NULL,
  un_no varchar(6),
  pkg_note text,
  shelf_life_mths smallint NOT NULL,
  CONSTRAINT prd_hndl_pk PRIMARY KEY (prd_cd)
);
COMMENT ON TABLE coco_products.prd_hndl IS 'Storage and shipping conditions; shelf life in months.';

CREATE TABLE IF NOT EXISTS coco_products.prd_mkt_auth (
  prd_cd varchar(6) NOT NULL,
  mkt varchar(2) NOT NULL,
  ma_no varchar(30) NOT NULL,
  start_dt date NOT NULL,
  end_dt date,
  CONSTRAINT prd_mkt_auth_pk PRIMARY KEY (prd_cd, mkt)
);
COMMENT ON TABLE coco_products.prd_mkt_auth IS 'Market authorisations per product (mkt uses UK for Great Britain).';

INSERT INTO coco_products.prd_mstr (prd_cd, prd_nm, prd_desc, prd_typ, actv_ingr, strgth, sts_cd, cur_ver, cat_id, upd_dt) VALUES
('1000', 'Asprin 81mg', 'Low-dose aspirin for cardiovascular prevention and mild pain.', 'S', 'Acetylsalicylic acid', '81mg', 'MKT', '4.1', 1000, '2026-01-15'),
('1010', 'Asprin 250mg', 'Aspirin for pain and fever.', 'S', 'Acetylsalicylic acid', '250mg', 'MKT', '4.1', 1000, '2026-01-15'),
('2000', 'Norvasc 10mg', 'Calcium channel blocker for hypertension and angina.', 'S', 'Amlodipine besylate', '10mg', 'MKT', '3.0', 4000, '2026-01-15'),
('2010', 'Norvasc 5mg', 'Calcium channel blocker for hypertension and angina.', 'S', 'Amlodipine besylate', '5mg', 'MKT', '3.0', 4000, '2026-01-15'),
('2050', 'Plavix 75mg', 'Antiplatelet to prevent heart attack and stroke.', 'S', 'Clopidogrel bisulfate', '75mg', 'MKT', '2.2', 6000, '2026-01-15'),
('3000', 'Cozaar 100mg', 'Angiotensin II receptor blocker for hypertension.', 'S', 'Losartan potassium', '100mg', 'MKT', '2.3', 4000, '2026-01-15'),
('4000', 'Toprol-XL 50mg', 'Extended-release beta blocker for hypertension and heart failure.', 'S', 'Metoprolol succinate', '50mg', 'MKT', '1.8', 4000, '2026-01-15'),
('4010', 'Toprol-XL 25mg', 'Extended-release beta blocker; supply suspended pending line transfer.', 'S', 'Metoprolol succinate', '25mg', 'SUS', '1.8', 4000, '2026-01-15'),
('5000', 'Crestor 5mg', 'Statin to lower cholesterol.', 'S', 'Rosuvastatin calcium', '5mg', 'MKT', '2.0', 5000, '2026-01-15'),
('9000', 'Cisplatin 50mg', 'Platinum chemotherapy for testicular, ovarian and bladder cancer.', 'S', 'Cisplatin', '50mg', 'MKT', '1.4', 9000, '2026-01-15'),
('9100', 'Cocolecel', 'Personalised autologous CAR T-cell therapy for relapsed B-cell lymphoma, made from the patient''s own cells.', 'P', 'Autologous anti-CD19 CAR T cells', '1-5 x 10^8 CAR+ T cells', 'MKT', '1.0', 9000, '2026-02-20')
ON CONFLICT DO NOTHING;

INSERT INTO coco_products.prd_pack (pack_cd, prd_cd, pack_desc, units_per_pack, dest_mkt, serial_yn) VALUES
('5060123410001', '1000', '30 tablets in blister pack (UK)', 30, 'UK', 'Y'),
('5060123410002', '1000', '30 tablets in blister pack (NL)', 30, 'NL', 'Y'),
('5060123410101', '1010', '30 tablets in blister pack (UK)', 30, 'UK', 'Y'),
('5060123410102', '1010', '30 tablets in blister pack (NL)', 30, 'NL', 'Y'),
('5060123420001', '2000', '30 tablets in bottle (CA)', 30, 'CA', 'N'),
('5060123420002', '2000', '30 tablets in blister pack (UK)', 30, 'UK', 'Y'),
('5060123420003', '2000', '30 tablets in blister pack (NL)', 30, 'NL', 'Y'),
('5060123420004', '2000', '30 tablets in bottle (US)', 30, 'US', 'Y'),
('5060123420101', '2010', '30 tablets in bottle (CA)', 30, 'CA', 'N'),
('5060123420102', '2010', '30 tablets in blister pack (UK)', 30, 'UK', 'Y'),
('5060123420103', '2010', '30 tablets in blister pack (NL)', 30, 'NL', 'Y'),
('5060123420501', '2050', '30 tablets in bottle (US)', 30, 'US', 'Y'),
('5060123420502', '2050', '30 tablets in blister pack (UK)', 30, 'UK', 'Y'),
('5060123430001', '3000', '30 tablets in bottle (US)', 30, 'US', 'Y'),
('5060123430002', '3000', '30 tablets in bottle (CA)', 30, 'CA', 'N'),
('5060123440001', '4000', '30 tablets in bottle (CA)', 30, 'CA', 'N'),
('5060123440002', '4000', '30 tablets in bottle (US)', 30, 'US', 'Y'),
('5060123440003', '4000', '30 tablets in blister pack (UK)', 30, 'UK', 'Y'),
('5060123440101', '4010', '30 tablets in bottle (CA)', 30, 'CA', 'N'),
('5060123440102', '4010', '30 tablets in bottle (US)', 30, 'US', 'Y'),
('5060123450001', '5000', '30 tablets in blister pack (UK)', 30, 'UK', 'Y'),
('5060123450002', '5000', '30 tablets in blister pack (NL)', 30, 'NL', 'Y'),
('5060123490001', '9000', '1 vials (US)', 1, 'US', 'Y'),
('5060123491001', '9100', '1 infusion bag (US)', 1, 'US', 'Y'),
('5060123491002', '9100', '1 infusion bag (UK)', 1, 'UK', 'Y')
ON CONFLICT DO NOTHING;

INSERT INTO coco_products.prd_hndl (prd_cd, store_min_c, store_max_c, un_no, pkg_note, shelf_life_mths) VALUES
('1000', 15, 25, NULL, 'Standard carton', 36),
('1010', 15, 25, NULL, 'Standard carton', 36),
('2000', 15, 30, NULL, 'Standard carton', 36),
('2010', 15, 30, NULL, 'Standard carton', 36),
('2050', 15, 25, NULL, 'Standard carton', 36),
('3000', 15, 30, NULL, 'Standard carton', 36),
('4000', 15, 30, NULL, 'Standard carton', 36),
('4010', 15, 30, NULL, 'Standard carton', 36),
('5000', 15, 25, NULL, 'Standard carton', 36),
('9000', 15, 25, 'UN1851', 'Cytotoxic-labelled insulated shipper, upright', 24),
('9100', -196, -150, 'UN3245', 'Vapour-phase liquid nitrogen dry shipper with chain-of-identity seal', 12)
ON CONFLICT DO NOTHING;

INSERT INTO coco_products.prd_mkt_auth (prd_cd, mkt, ma_no, start_dt, end_dt) VALUES
('1000', 'UK', 'PL 1000-01UK', '2019-01-01', NULL),
('1000', 'NL', 'RVG 1000-02NL', '2019-01-01', NULL),
('1010', 'UK', 'PL 1010-01UK', '2019-01-01', NULL),
('1010', 'NL', 'RVG 1010-02NL', '2019-01-01', NULL),
('2000', 'CA', 'DIN 2000-01CA', '2019-01-01', NULL),
('2000', 'UK', 'PL 2000-02UK', '2019-01-01', NULL),
('2000', 'NL', 'RVG 2000-03NL', '2019-01-01', NULL),
('2000', 'US', 'NDA 2000-04US', '2019-01-01', NULL),
('2010', 'CA', 'DIN 2010-01CA', '2019-01-01', NULL),
('2010', 'UK', 'PL 2010-02UK', '2019-01-01', NULL),
('2010', 'NL', 'RVG 2010-03NL', '2019-01-01', NULL),
('2050', 'US', 'NDA 2050-01US', '2019-01-01', NULL),
('2050', 'UK', 'PL 2050-02UK', '2019-01-01', NULL),
('3000', 'US', 'NDA 3000-01US', '2019-01-01', NULL),
('3000', 'CA', 'DIN 3000-02CA', '2019-01-01', NULL),
('4000', 'CA', 'DIN 4000-01CA', '2019-01-01', NULL),
('4000', 'US', 'NDA 4000-02US', '2019-01-01', NULL),
('4000', 'UK', 'PL 4000-03UK', '2019-01-01', NULL),
('4010', 'CA', 'DIN 4010-01CA', '2019-01-01', NULL),
('4010', 'US', 'NDA 4010-02US', '2019-01-01', '2026-12-31'),
('5000', 'UK', 'PL 5000-01UK', '2019-01-01', NULL),
('5000', 'NL', 'RVG 5000-02NL', '2019-01-01', NULL),
('9000', 'US', 'NDA 9000-01US', '2019-01-01', NULL),
('9100', 'US', 'NDA 9100-01US', '2026-03-01', NULL),
('9100', 'UK', 'PL 9100-02UK', '2026-06-15', NULL)
ON CONFLICT DO NOTHING;


-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS coco_products.prd_ma_rcvd (
  ma_no varchar(40) NOT NULL,
  prd_cd varchar(6) NOT NULL,
  mkt varchar(8) NOT NULL,
  rgltr_cd varchar(20) NOT NULL,
  start_dt date NOT NULL,
  end_dt date,
  ma_sts varchar(20) NOT NULL,
  sgnl_ref varchar(40),
  CONSTRAINT prd_ma_rcvd_pk PRIMARY KEY (ma_no)
);
COMMENT ON TABLE coco_products.prd_ma_rcvd IS 'Market authorisations received from regulatory (Market Authorisations), waiting for the product manager to update prd_mkt_auth; mkt uses UK for Great Britain.';

CREATE TABLE IF NOT EXISTS coco_products.prd_ma_cond (
  ma_no varchar(40) NOT NULL,
  cond_no smallint NOT NULL,
  cond_typ varchar(40) NOT NULL,
  cond_txt text NOT NULL,
  start_dt date NOT NULL,
  CONSTRAINT prd_ma_cond_pk PRIMARY KEY (ma_no, cond_no)
);
COMMENT ON TABLE coco_products.prd_ma_cond IS 'Conditions attached to the market authorisations received.';

CREATE TABLE IF NOT EXISTS coco_products.prd_cand (
  prd_cd varchar(6) NOT NULL,
  cand_ref varchar(40) NOT NULL,
  prd_nm varchar(120) NOT NULL,
  frml_ref varchar(40) NOT NULL,
  actv_ingr varchar(120) NOT NULL,
  strgth varchar(40),
  trial_ref varchar(40),
  hndovr_dt date NOT NULL,
  CONSTRAINT prd_cand_pk PRIMARY KEY (prd_cd)
);
COMMENT ON TABLE coco_products.prd_cand IS 'Product candidates handed over from development (New Product Definitions), from which the board creates the prd_mstr entry (status DEV).';

CREATE TABLE IF NOT EXISTS coco_products.prd_cand_pack (
  pack_cd varchar(20) NOT NULL,
  prd_cd varchar(6) NOT NULL,
  pack_desc text NOT NULL,
  units_per_pack integer NOT NULL,
  CONSTRAINT prd_cand_pack_pk PRIMARY KEY (pack_cd)
);
COMMENT ON TABLE coco_products.prd_cand_pack IS 'Presentations proposed for each product candidate.';

CREATE TABLE IF NOT EXISTS coco_products.prd_cand_spec (
  prd_cd varchar(6) NOT NULL,
  test_cd varchar(40) NOT NULL,
  spec_min varchar(60),
  spec_max varchar(60),
  test_uom varchar(20),
  CONSTRAINT prd_cand_spec_pk PRIMARY KEY (prd_cd, test_cd)
);
COMMENT ON TABLE coco_products.prd_cand_spec IS 'Release specification proposed for each product candidate.';

-- End of subscription tables.

GRANT USAGE ON SCHEMA coco_products TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA coco_products TO egeria_user, airflow_user;
