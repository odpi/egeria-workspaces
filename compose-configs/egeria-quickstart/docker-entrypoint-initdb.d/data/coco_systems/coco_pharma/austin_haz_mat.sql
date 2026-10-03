-- system-qualified-name: System::austin-haz-mat
-- Austin HazMat Inventory - Coco core.  Homegrown hazardous materials inventory for the Austin manufacturing site, built separately from the Coco HazMat Inventory; feeds Occupational Exposure Bands, Hazardous Material Holdings and Transport Classifications.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS austin_haz_mat;
COMMENT ON SCHEMA austin_haz_mat IS 'Austin HazMat Inventory (Coco core): chemicals, storage quantities and DOT classifications for the Austin site.';

CREATE TABLE IF NOT EXISTS austin_haz_mat.chemical (
  chem_id varchar(10) NOT NULL,
  chem_name varchar(120) NOT NULL,
  cas varchar(15),
  hazard_class varchar(60) NOT NULL,
  hazard_statement text NOT NULL,
  primary_hazard varchar(20) NOT NULL,
  oeb smallint,
  oeb_assigned date,
  incident_no varchar(20),
  CONSTRAINT chemical_pk PRIMARY KEY (chem_id)
);
COMMENT ON TABLE austin_haz_mat.chemical IS 'Chemicals held at the Austin site. oeb is the band number 1-5; incident_no the EHS incident behind the latest band revision.';

CREATE TABLE IF NOT EXISTS austin_haz_mat.storage_location_qty (
  chem_id varchar(10) NOT NULL,
  storage_loc varchar(8) NOT NULL,
  qty_on_hand numeric(12,2) NOT NULL,
  unit varchar(4) NOT NULL,
  physical_state char(1) NOT NULL,
  last_count timestamptz NOT NULL,
  CONSTRAINT storage_location_qty_pk PRIMARY KEY (chem_id, storage_loc)
);
COMMENT ON TABLE austin_haz_mat.storage_location_qty IS 'Quantity per storage location; physical_state S solid, L liquid, G gas; units in US customary where the site uses them.';

CREATE TABLE IF NOT EXISTS austin_haz_mat.dot_classification (
  class_id varchar(10) NOT NULL,
  chem_id varchar(10),
  product_code varchar(6),
  shipped_form varchar(80) NOT NULL,
  un_number varchar(6) NOT NULL,
  packing_group varchar(3),
  hazard_class varchar(4) NOT NULL,
  label_text text NOT NULL,
  shipping_docs text NOT NULL,
  classified_on date NOT NULL,
  CONSTRAINT dot_classification_pk PRIMARY KEY (class_id)
);
COMMENT ON TABLE austin_haz_mat.dot_classification IS 'US DOT (49 CFR 172.101) classification per chemical or product in its shipped form.';

INSERT INTO austin_haz_mat.chemical (chem_id, chem_name, cas, hazard_class, hazard_statement, primary_hazard, oeb, oeb_assigned, incident_no) VALUES
('AHM-0042', 'Cisplatin', '15663-27-1', 'Carc. 1B; Muta. 1B; Repr. 1B', 'H350 May cause cancer; H340 may cause genetic defects; H360 may damage fertility; highly potent cytotoxic', 'Carc. 1B', 5, '2026-08-26', 'AUS-EHS-26-031'),
('AHM-0043', 'Clopidogrel bisulfate', '120202-66-6', 'Acute Tox. 4; Aquatic Chronic 2', 'H302 Harmful if swallowed; H411 toxic to aquatic life with long lasting effects', 'Acute Tox. 4', 3, '2024-01-12', NULL),
('AHM-0044', 'Losartan potassium', '124750-99-8', 'Repr. 1B', 'H360D May damage the unborn child', 'Repr. 1B', 3, '2024-01-12', NULL),
('AHM-0051', 'Ethanol 190 proof', '64-17-5', 'Flam. Liq. 2', 'H225 Highly flammable liquid and vapour', 'Flam. Liq. 2', 1, '2023-06-30', NULL),
('AHM-0052', 'Hydrochloric acid 37%', '7647-01-0', 'Skin Corr. 1B; STOT SE 3', 'H314 Causes severe skin burns and eye damage; H335 may cause respiratory irritation', 'Skin Corr. 1B', 1, '2023-06-30', NULL),
('AHM-0060', 'Hydrogen peroxide 35% (VHP)', '7722-84-1', 'Ox. Liq. 2; Skin Corr. 1A', 'H272 May intensify fire; oxidiser; H314 causes severe skin burns', 'Ox. Liq. 2', 2, '2025-05-19', NULL)
ON CONFLICT DO NOTHING;

INSERT INTO austin_haz_mat.storage_location_qty (chem_id, storage_loc, qty_on_hand, unit, physical_state, last_count) VALUES
('AHM-0042', 'AUS-HAZ', 4.87, 'KG', 'S', '2026-09-01 05:00+00'),
('AHM-0042', 'AUS-FG', 1000.0, 'VIAL', 'L', '2026-09-17 15:00+00'),
('AHM-0043', 'AUS-RM', 582.0, 'KG', 'S', '2026-09-28 04:00+00'),
('AHM-0044', 'AUS-RM', 764.0, 'KG', 'S', '2026-09-07 04:00+00'),
('AHM-0051', 'AUS-FLM', 330.0, 'GAL', 'L', '2026-09-26 12:00+00'),
('AHM-0052', 'AUS-CHM', 55.0, 'GAL', 'L', '2026-09-12 12:00+00'),
('AHM-0060', 'AUS-CHM', 40.0, 'GAL', 'L', '2026-09-12 12:00+00')
ON CONFLICT DO NOTHING;

INSERT INTO austin_haz_mat.dot_classification (class_id, chem_id, product_code, shipped_form, un_number, packing_group, hazard_class, label_text, shipping_docs, classified_on) VALUES
('DOT-A-01', 'AHM-0042', NULL, 'Powder in sealed HDPE bottle within drum', 'UN3288', 'II', '6.1', 'Toxic label 6.1', 'Bill of lading with shipper''s certification; SDS; ERG guide 151', '2026-08-28'),
('DOT-A-02', NULL, '9000', 'Solution in 50mL glass vials, cartons in insulated shipper', 'UN1851', 'III', '6.1', 'Toxic label 6.1; ''Medicine, liquid, toxic, n.o.s. (cisplatin)''', 'Bill of lading with shipper''s certification; SDS; ERG guide 151', '2026-09-03'),
('DOT-A-03', 'AHM-0051', NULL, 'Liquid in 55 gal drums', 'UN1170', 'II', '3', 'Flammable liquid label 3', 'Bill of lading; SDS; ERG guide 127', '2023-07-10'),
('DOT-A-04', 'AHM-0052', NULL, 'Liquid in 5 gal carboys', 'UN1789', 'II', '8', 'Corrosive label 8', 'Bill of lading; SDS; ERG guide 157', '2023-07-10'),
('DOT-A-05', 'AHM-0060', NULL, 'Liquid in 1 gal jugs', 'UN2014', 'II', '5.1', 'Oxidizer 5.1 and corrosive 8 labels', 'Bill of lading; SDS; ERG guide 140', '2025-05-22')
ON CONFLICT DO NOTHING;


-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS austin_haz_mat.stock_check (
  item_no varchar(20) NOT NULL,
  storage_loc varchar(20) NOT NULL,
  lot_no varchar(40) NOT NULL,
  qty_on_hand integer NOT NULL,
  as_of timestamptz NOT NULL,
  CONSTRAINT stock_check_pk PRIMARY KEY (item_no, storage_loc, lot_no)
);
COMMENT ON TABLE austin_haz_mat.stock_check IS 'Stock positions at Coco''s Austin site locations (Goods Inventory Stock), checked against storage_location_qty to find chemicals whose holdings are not yet recorded.';

CREATE TABLE IF NOT EXISTS austin_haz_mat.ehs_incident (
  incident_no varchar(40) NOT NULL,
  incident_type varchar(20) NOT NULL,
  occurred_at timestamptz NOT NULL,
  reported_at timestamptz NOT NULL,
  site varchar(20) NOT NULL,
  area varchar(120) NOT NULL,
  chem_id varchar(20) NOT NULL,
  worker_psn varchar(40),
  description text NOT NULL,
  severity varchar(20) NOT NULL,
  findings text,
  CONSTRAINT ehs_incident_pk PRIMARY KEY (incident_no)
);
COMMENT ON TABLE austin_haz_mat.ehs_incident IS 'Incidents and near misses involving chemicals held at the Austin site (Incidents And Near Misses), with the investigation findings, reviewed when a band is revised (chemical.incident_no).';

CREATE TABLE IF NOT EXISTS austin_haz_mat.oeb_band (
  oeb smallint NOT NULL,
  oel_upper numeric(10,2) NOT NULL,
  oel_unit varchar(10) NOT NULL,
  containment text NOT NULL,
  CONSTRAINT oeb_band_pk PRIMARY KEY (oeb)
);
COMMENT ON TABLE austin_haz_mat.oeb_band IS 'Coco''s occupational exposure band definitions (Occupational Exposure Bands): the exposure limit and containment that chemical.oeb 1-5 stands for.';

CREATE TABLE IF NOT EXISTS austin_haz_mat.product_handling (
  product_code varchar(6) NOT NULL,
  product_name varchar(120),
  un_number varchar(20),
  min_temp_c numeric(6,1),
  max_temp_c numeric(6,1),
  packaging text,
  CONSTRAINT product_handling_pk PRIMARY KEY (product_code)
);
COMMENT ON TABLE austin_haz_mat.product_handling IS 'Handling requirements of the shared Coco products made at the Austin site (Product Master Data), from which they are classified for transport (dot_classification.product_code).';

-- End of subscription tables.

GRANT USAGE ON SCHEMA austin_haz_mat TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA austin_haz_mat TO egeria_user, airflow_user;
