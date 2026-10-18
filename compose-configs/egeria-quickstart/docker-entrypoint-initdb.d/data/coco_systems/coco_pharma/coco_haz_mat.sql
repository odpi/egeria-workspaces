-- system-qualified-name: System::coco-haz-mat
-- Coco HazMat Inventory - Coco core.  Homegrown hazardous materials inventory for the Coco sites other than Austin; feeds Occupational Exposure Bands, Hazardous Material Holdings and Transport Classifications.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS coco_haz_mat;
COMMENT ON SCHEMA coco_haz_mat IS 'Coco HazMat Inventory (Coco core): substances, exposure bands, holdings and transport classifications.';

CREATE TABLE IF NOT EXISTS coco_haz_mat.hm_subst (
  subst_cd varchar(10) NOT NULL,
  subst_nm varchar(120) NOT NULL,
  cas_no varchar(15),
  ghs_cls varchar(30) NOT NULL,
  haz_desc text NOT NULL,
  oeb_cd varchar(6),
  oeb_dt date,
  oeb_inc_ref varchar(20),
  tpt_ref varchar(10),
  CONSTRAINT hm_subst_pk PRIMARY KEY (subst_cd)
);
COMMENT ON TABLE coco_haz_mat.hm_subst IS 'Hazardous substances held: GHS classification, exposure band (with the incident behind the latest revision) and transport classification reference.';

CREATE TABLE IF NOT EXISTS coco_haz_mat.hm_band (
  band_cd varchar(6) NOT NULL,
  oel_max numeric(10,2) NOT NULL,
  oel_unit varchar(10) NOT NULL,
  contain_desc text NOT NULL,
  CONSTRAINT hm_band_pk PRIMARY KEY (band_cd)
);
COMMENT ON TABLE coco_haz_mat.hm_band IS 'Occupational exposure bands: upper exposure limit (8h TWA) and the containment required.';

CREATE TABLE IF NOT EXISTS coco_haz_mat.hm_hold (
  subst_cd varchar(10) NOT NULL,
  loc_cd varchar(10) NOT NULL,
  qty numeric(12,2) NOT NULL,
  uom varchar(6) NOT NULL,
  form_desc varchar(80) NOT NULL,
  upd_ts timestamptz NOT NULL,
  CONSTRAINT hm_hold_pk PRIMARY KEY (subst_cd, loc_cd)
);
COMMENT ON TABLE coco_haz_mat.hm_hold IS 'Quantity of each substance per storage location.';

CREATE TABLE IF NOT EXISTS coco_haz_mat.hm_tpt (
  tpt_id varchar(10) NOT NULL,
  subst_cd varchar(10),
  prd_cd varchar(6),
  form_desc varchar(80) NOT NULL,
  un_no varchar(6) NOT NULL,
  pkg_grp varchar(3),
  haz_cls varchar(4) NOT NULL,
  lbl_desc text NOT NULL,
  docs_desc text NOT NULL,
  deriv_dt date NOT NULL,
  CONSTRAINT hm_tpt_pk PRIMARY KEY (tpt_id)
);
COMMENT ON TABLE coco_haz_mat.hm_tpt IS 'Transport classifications per substance or product in the form shipped.';

INSERT INTO coco_haz_mat.hm_subst (subst_cd, subst_nm, cas_no, ghs_cls, haz_desc, oeb_cd, oeb_dt, oeb_inc_ref, tpt_ref) VALUES
('HM0101', 'Rosuvastatin calcium', '147098-20-2', 'Repr. 2', 'H361 Suspected of damaging fertility or the unborn child; H373 organ damage on repeated exposure', 'OEB3', '2023-02-14', NULL, 'TC-C-009'),
('HM0102', 'Amlodipine besylate', '111470-99-6', 'Acute Tox. 4', 'H302 Harmful if swallowed; H373 cardiovascular effects on repeated exposure', 'OEB3', '2023-02-14', NULL, NULL),
('HM0103', 'Metoprolol succinate', '98418-47-4', 'Acute Tox. 4', 'H302 Harmful if swallowed', 'OEB2', '2023-02-14', NULL, NULL),
('HM0104', 'Ethanol 96%', '64-17-5', 'Flam. Liq. 2', 'H225 Highly flammable liquid and vapour; H319 eye irritation', 'OEB1', '2022-09-01', NULL, 'TC-C-001'),
('HM0105', 'Isopropyl alcohol 70%', '67-63-0', 'Flam. Liq. 2', 'H225 Highly flammable liquid and vapour; H336 drowsiness or dizziness', 'OEB1', '2022-09-01', NULL, 'TC-C-002'),
('HM0106', 'Sodium hydroxide solution 30%', '1310-73-2', 'Skin Corr. 1A', 'H314 Causes severe skin burns and eye damage', 'OEB1', '2022-09-01', NULL, 'TC-C-003'),
('HM0107', 'Lentiviral vector LV-CD19', NULL, 'Bio. Agent 2 / GMO', 'Replication-incompetent lentiviral vector; GMO contained use class 2', 'OEB4', '2026-07-28', 'INC-WIN-26-0014', 'TC-C-008'),
('HM0108', 'Liquid nitrogen', '7727-37-9', 'Press. Gas', 'H281 Contains refrigerated gas; may cause cryogenic burns; asphyxiant in enclosed spaces', 'OEB1', '2025-10-20', NULL, 'TC-C-004'),
('HM0109', 'Dimethyl sulfoxide', '67-68-5', 'Not classified', 'Readily absorbed through skin and carries dissolved substances with it', 'OEB2', '2026-03-09', 'INC-WIN-26-0003', NULL)
ON CONFLICT DO NOTHING;

INSERT INTO coco_haz_mat.hm_band (band_cd, oel_max, oel_unit, contain_desc) VALUES
('OEB1', 5000.0, 'ug/m3', 'General ventilation; standard PPE.'),
('OEB2', 1000.0, 'ug/m3', 'Local exhaust ventilation at open handling points; gloves and safety glasses.'),
('OEB3', 100.0, 'ug/m3', 'Closed transfer or ventilated enclosure for powder handling; respiratory protection (FFP3) for open handling.'),
('OEB4', 10.0, 'ug/m3', 'Isolator or Class II biosafety cabinet; no open handling; gowning and airlock.'),
('OEB5', 1.0, 'ug/m3', 'Isolator under negative pressure with split-butterfly valves; powered air respirator for maintenance.')
ON CONFLICT DO NOTHING;

INSERT INTO coco_haz_mat.hm_hold (subst_cd, loc_cd, qty, uom, form_desc, upd_ts) VALUES
('HM0101', 'WIN-RM01', 78.0, 'kg', 'Powder in double-bagged fibre drums', '2026-09-29 05:00+00'),
('HM0102', 'EDM-RM01', 147.0, 'kg', 'Powder in fibre drums', '2026-09-21 11:00+00'),
('HM0103', 'EDM-RM01', 291.0, 'kg', 'Powder in fibre drums', '2026-09-01 11:00+00'),
('HM0103', 'EDM-QUAR', 300.0, 'kg', 'Powder in fibre drums (quarantine)', '2026-09-21 20:00+00'),
('HM0104', 'WIN-FLM1', 820.0, 'L', 'Liquid in 200L drums', '2026-09-25 08:00+00'),
('HM0104', 'EDM-FLM1', 1150.0, 'L', 'Liquid in 200L drums', '2026-09-22 15:00+00'),
('HM0105', 'WIN-FLM1', 240.0, 'L', 'Liquid in 5L spray bottles and 25L cans', '2026-09-25 08:00+00'),
('HM0106', 'EDM-CHM1', 600.0, 'L', 'Solution in 1000L IBC', '2026-09-18 09:00+00'),
('HM0107', 'WIN-CELL', 38.0, 'vial', 'Frozen suspension at -80C', '2026-09-24 19:00+00'),
('HM0108', 'WIN-CELL', 2400.0, 'L', 'Refrigerated liquid in bulk tank and dewars', '2026-09-29 07:00+00'),
('HM0109', 'WIN-CELL', 12.0, 'L', 'Liquid in 500mL bottles', '2026-09-27 07:00+00')
ON CONFLICT DO NOTHING;

INSERT INTO coco_haz_mat.hm_tpt (tpt_id, subst_cd, prd_cd, form_desc, un_no, pkg_grp, haz_cls, lbl_desc, docs_desc, deriv_dt) VALUES
('TC-C-001', 'HM0104', NULL, 'Liquid in drums', 'UN1170', 'II', '3', 'Flammable liquid class 3', 'ADR transport document; SDS; tremcard', '2022-09-05'),
('TC-C-002', 'HM0105', NULL, 'Liquid in cans', 'UN1219', 'II', '3', 'Flammable liquid class 3', 'ADR transport document; SDS', '2022-09-05'),
('TC-C-003', 'HM0106', NULL, 'Solution in IBC', 'UN1824', 'II', '8', 'Corrosive class 8', 'TDG shipping document; SDS', '2022-09-05'),
('TC-C-004', 'HM0108', NULL, 'Refrigerated liquid in dewar', 'UN1977', NULL, '2.2', 'Non-flammable gas 2.2; cryogenic liquid; orientation arrows', 'Air waybill with DG declaration; SDS', '2025-10-24'),
('TC-C-005', NULL, NULL, 'Patient apheresis material in dry shipper', 'UN3373', NULL, '6.2', 'UN3373 diamond; ''Biological Substance, Category B''', 'Air waybill; shipper''s specimen declaration; chain of identity form', '2026-02-02'),
('TC-C-006', NULL, '9100', 'Cryopreserved cell suspension in vapour-phase dry shipper', 'UN3245', NULL, '9', 'Class 9 label; ''Genetically modified micro-organisms''', 'Shipper''s declaration for dangerous goods; SDS; handling instructions; chain of identity form', '2026-02-02'),
('TC-C-007', NULL, NULL, 'Dry ice as refrigerant', 'UN1845', 'III', '9', 'Class 9 label; net weight of dry ice', 'Air waybill notation; SDS', '2025-10-24'),
('TC-C-008', 'HM0107', NULL, 'Frozen vector suspension on dry ice', 'UN3245', NULL, '9', 'Class 9 label; ''Genetically modified micro-organisms''', 'Shipper''s declaration for dangerous goods; SDS; contained use notification reference', '2026-07-30'),
('TC-C-009', 'HM0101', NULL, 'Powder in fibre drums', 'UN3077', 'III', '9', 'Class 9; environmentally hazardous substance mark', 'Transport document; SDS', '2023-02-20')
ON CONFLICT DO NOTHING;

-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS coco_haz_mat.hm_consign (
  cons_ref varchar(40) NOT NULL,
  desp_dt date NOT NULL,
  carr_ref varchar(40) NOT NULL,
  ship_to text NOT NULL,
  un_no varchar(20) NOT NULL,
  qty double precision NOT NULL,
  uom varchar(20) NOT NULL,
  signed_by varchar(40) NOT NULL,
  signed_ts timestamptz NOT NULL,
  dg_cert varchar(40) NOT NULL,
  CONSTRAINT hm_consign_pk PRIMARY KEY (cons_ref)
);
COMMENT ON TABLE coco_haz_mat.hm_consign IS 'Dangerous goods consignments despatched from Coco depots (Dangerous Goods Consignment Records), used to reconcile hm_hold after hazardous material leaves a site.';

CREATE TABLE IF NOT EXISTS coco_haz_mat.hm_stk_chk (
  item_cd varchar(20) NOT NULL,
  loc_cd varchar(20) NOT NULL,
  lot_no varchar(40) NOT NULL,
  qty integer NOT NULL,
  upd_ts timestamptz NOT NULL,
  CONSTRAINT hm_stk_chk_pk PRIMARY KEY (item_cd, loc_cd, lot_no)
);
COMMENT ON TABLE coco_haz_mat.hm_stk_chk IS 'Stock positions at Coco locations other than Austin (Goods Inventory Stock), checked against hm_hold to find hazardous holdings not yet recorded; lot ''-'' where not lot-tracked.';

CREATE TABLE IF NOT EXISTS coco_haz_mat.hm_incid (
  inc_ref varchar(40) NOT NULL,
  inc_typ varchar(20) NOT NULL,
  inc_ts timestamptz NOT NULL,
  rpt_ts timestamptz NOT NULL,
  site_cd varchar(20) NOT NULL,
  inc_loc varchar(120) NOT NULL,
  subst_cd varchar(20) NOT NULL,
  worker_ref varchar(40),
  inc_desc text NOT NULL,
  sev varchar(20) NOT NULL,
  findings text,
  CONSTRAINT hm_incid_pk PRIMARY KEY (inc_ref)
);
COMMENT ON TABLE coco_haz_mat.hm_incid IS 'Incidents and near misses involving substances held in this inventory (Incidents And Near Misses), with the investigation findings, reviewed when a substance''s exposure band is reassessed (hm_subst.oeb_inc_ref).';

CREATE TABLE IF NOT EXISTS coco_haz_mat.hm_prd_hndl (
  prd_cd varchar(20) NOT NULL,
  prd_nm varchar(120),
  un_no varchar(20),
  store_min_c numeric(6,1),
  store_max_c numeric(6,1),
  pkg_note text,
  CONSTRAINT hm_prd_hndl_pk PRIMARY KEY (prd_cd)
);
COMMENT ON TABLE coco_haz_mat.hm_prd_hndl IS 'Handling requirements of the Coco products made or stored at the non-Austin sites (Product Master Data), from which products are classified for transport (hm_tpt.prd_cd).';

-- End of subscription tables.

GRANT USAGE ON SCHEMA coco_haz_mat TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA coco_haz_mat TO egeria_user, airflow_user;
