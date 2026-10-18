-- system-qualified-name: System::WINCHDEPOT01
-- Winchester Depot Management System - Coco core.  COTS depot management system at the Winchester depot (goods in for the Winchester factory, cell therapy despatch); feeds Goods Receipts and Dangerous Goods Consignment Records.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS winchdepot01;
COMMENT ON SCHEMA winchdepot01 IS 'Winchester Depot Management System (Coco core): goods received notes and dangerous goods consignments.';

CREATE TABLE IF NOT EXISTS winchdepot01.gr_hdr (
  grn_no varchar(12) NOT NULL,
  po_ref varchar(20) NOT NULL,
  supp_no integer NOT NULL,
  rcv_dt date NOT NULL,
  whs varchar(6) NOT NULL,
  grn_sts varchar(8) NOT NULL,
  CONSTRAINT gr_hdr_pk PRIMARY KEY (grn_no)
);
COMMENT ON TABLE winchdepot01.gr_hdr IS 'Goods received note headers; whs is the depot bay (RM01, CELL, FG01).';

CREATE TABLE IF NOT EXISTS winchdepot01.gr_line (
  grn_no varchar(12) NOT NULL,
  ln_no smallint NOT NULL,
  item_cd varchar(10) NOT NULL,
  supp_lot varchar(30) NOT NULL,
  qty numeric(12,2) NOT NULL,
  uom varchar(6) NOT NULL,
  coa_ref varchar(30),
  CONSTRAINT gr_line_pk PRIMARY KEY (grn_no, ln_no)
);
COMMENT ON TABLE winchdepot01.gr_line IS 'Goods received note lines, one per supplier lot.';

CREATE TABLE IF NOT EXISTS winchdepot01.dg_consign (
  cons_no varchar(12) NOT NULL,
  desp_dt date NOT NULL,
  carr_id smallint NOT NULL,
  ship_to text NOT NULL,
  un_no varchar(6) NOT NULL,
  qty numeric(10,2) NOT NULL,
  uom varchar(4) NOT NULL,
  signed_by varchar(20) NOT NULL,
  signed_ts timestamptz NOT NULL,
  dg_cert varchar(30) NOT NULL,
  CONSTRAINT dg_consign_pk PRIMARY KEY (cons_no)
);
COMMENT ON TABLE winchdepot01.dg_consign IS 'Dangerous goods consignments despatched from Winchester. carr_id is the Coco shipper id; signed_by the signatory''s worker pseudonym.';

CREATE TABLE IF NOT EXISTS winchdepot01.dg_docs (
  cons_no varchar(12) NOT NULL,
  doc_ref varchar(40) NOT NULL,
  doc_typ varchar(4) NOT NULL,
  doc_dt date NOT NULL,
  CONSTRAINT dg_docs_pk PRIMARY KEY (cons_no, doc_ref)
);
COMMENT ON TABLE winchdepot01.dg_docs IS 'Documents in each consignment''s pack: DGD declaration, SDS safety data sheet, HI handling instructions.';

INSERT INTO winchdepot01.gr_hdr (grn_no, po_ref, supp_no, rcv_dt, whs, grn_sts) VALUES
('WDR-260603', 'PO-AMS-26-0311', 1000, '2026-06-03', 'RM01', 'CLOSED'),
('WDR-260610', 'PO-AMS-26-0318', 9000, '2026-06-10', 'RM01', 'CLOSED'),
('WDR-260701', 'PO-AMS-26-0344', 1000, '2026-07-01', 'RM01', 'CLOSED'),
('WDR-260715', 'PO-AMS-26-0352', 7000, '2026-07-15', 'CELL', 'CLOSED'),
('WDR-260805', 'PO-AMS-26-0371', 1000, '2026-08-05', 'RM01', 'CLOSED'),
('WDR-260819', 'PO-AMS-26-0380', 9000, '2026-08-19', 'RM01', 'CLOSED'),
('WDR-260902', 'PO-AMS-26-0395', 1000, '2026-09-02', 'RM01', 'CLOSED'),
('WDR-260916', 'PO-AMS-26-0402', 7000, '2026-09-16', 'CELL', 'CLOSED')
ON CONFLICT DO NOTHING;

INSERT INTO winchdepot01.gr_line (grn_no, ln_no, item_cd, supp_lot, qty, uom, coa_ref) VALUES
('WDR-260603', 1, 'RM1001', 'GML-ASA-26-117', 500, 'kg', 'COA-GML-26-117'),
('WDR-260610', 1, 'RM1002', 'WWE-MCC-2605-33', 1200, 'kg', 'COA-WWE-2605-33'),
('WDR-260701', 1, 'RM5001', 'GML-RSV-26-042', 80, 'kg', 'COA-GML-26-042'),
('WDR-260715', 1, 'RM9101', 'BASE-LV19-2607A', 40, 'vial', 'COA-BASE-LV19-2607A'),
('WDR-260805', 1, 'RM1001', 'GML-ASA-26-161', 500, 'kg', 'COA-GML-26-161'),
('WDR-260819', 1, 'RM1004', 'WWE-MGS-2608-07', 150, 'kg', 'COA-WWE-2608-07'),
('WDR-260902', 1, 'PK0022', 'GML-FOIL-2609', 20000, 'm', 'COC-GML-FOIL-2609'),
('WDR-260916', 1, 'RM9102', 'BASE-CCM-2609B', 200, 'L', 'COA-BASE-CCM-2609B')
ON CONFLICT DO NOTHING;

INSERT INTO winchdepot01.dg_consign (cons_no, desp_dt, carr_id, ship_to, un_no, qty, uom, signed_by, signed_ts, dg_cert) VALUES
('WC26-0081', '2026-06-08', 6, 'Oncology Unit 1, Hampton Hospital, Nightingale St, Harlem, New York, NY, US', 'UN3245', 4.5, 'kg', 'CW-7G8SM2', '2026-06-08 10:15+00', 'IATA-DGR-UK-44871'),
('WC26-0093', '2026-06-29', 6, 'Cell Therapy Unit, Bowden Arrow Hospital, 400 Arrow Way, Boston, MA, US', 'UN3245', 4.5, 'kg', 'CW-7G8SM2', '2026-06-29 09:40+00', 'IATA-DGR-UK-44871'),
('WC26-0102', '2026-07-21', 6, 'Haematology, Oak Dene Hospital, 12 Oak Dene Rd, Philadelphia, PA, US', 'UN3245', 4.5, 'kg', 'CW-7G8SM2', '2026-07-21 10:05+00', 'IATA-DGR-UK-44871'),
('WC26-0117', '2026-08-18', 6, 'Oncology Unit 1, Hampton Hospital, Nightingale St, Harlem, New York, NY, US', 'UN3245', 4.5, 'kg', 'CW-7G8SM2', '2026-08-18 09:55+00', 'IATA-DGR-UK-44871'),
('WC26-0124', '2026-09-10', 3, 'Hampshire Solvent Recovery Ltd, Unit 4 Chilcomb Park, Winchester SO21 1HU, GB', 'UN1170', 400.0, 'L', 'CW-7G8SM2', '2026-09-10 08:30+00', 'DGSA-UK-20931')
ON CONFLICT DO NOTHING;

INSERT INTO winchdepot01.dg_docs (cons_no, doc_ref, doc_typ, doc_dt) VALUES
('WC26-0081', 'WC26-0081-DGD', 'DGD', '2026-06-08'),
('WC26-0081', 'SDS-UN3245-v3', 'SDS', '2025-11-01'),
('WC26-0081', 'WC26-0081-HI', 'HI', '2026-06-08'),
('WC26-0093', 'WC26-0093-DGD', 'DGD', '2026-06-29'),
('WC26-0093', 'SDS-UN3245-v3', 'SDS', '2025-11-01'),
('WC26-0093', 'WC26-0093-HI', 'HI', '2026-06-29'),
('WC26-0102', 'WC26-0102-DGD', 'DGD', '2026-07-21'),
('WC26-0102', 'SDS-UN3245-v3', 'SDS', '2025-11-01'),
('WC26-0102', 'WC26-0102-HI', 'HI', '2026-07-21'),
('WC26-0117', 'WC26-0117-DGD', 'DGD', '2026-08-18'),
('WC26-0117', 'SDS-UN3245-v3', 'SDS', '2025-11-01'),
('WC26-0117', 'WC26-0117-HI', 'HI', '2026-08-18'),
('WC26-0124', 'WC26-0124-DGD', 'DGD', '2026-09-10'),
('WC26-0124', 'SDS-UN1170-v3', 'SDS', '2025-11-01')
ON CONFLICT DO NOTHING;


-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS winchdepot01.supp_mstr (
  supp_no integer NOT NULL,
  supp_nm varchar(200) NOT NULL,
  appr_flg char(1) NOT NULL,
  supp_sts varchar(10) NOT NULL,
  CONSTRAINT supp_mstr_pk PRIMARY KEY (supp_no)
);
COMMENT ON TABLE winchdepot01.supp_mstr IS 'Suppliers the depot may receive from (Supplier Master Data); supp_no as in gr_hdr.';

CREATE TABLE IF NOT EXISTS winchdepot01.coa_hdr (
  coa_ref varchar(40) NOT NULL,
  supp_no integer NOT NULL,
  item_cd varchar(20) NOT NULL,
  supp_lot varchar(40) NOT NULL,
  coa_typ varchar(4) NOT NULL,
  coa_dt date NOT NULL,
  conform_flg char(1) NOT NULL,
  CONSTRAINT coa_hdr_pk PRIMARY KEY (coa_ref)
);
COMMENT ON TABLE winchdepot01.coa_hdr IS 'Supplier certificates (Supplier Material Certificates) matched to gr_line.coa_ref at goods in; coa_typ COA or COC.';

CREATE TABLE IF NOT EXISTS winchdepot01.coa_line (
  coa_ref varchar(40) NOT NULL,
  test_cd varchar(40) NOT NULL,
  test_val varchar(60) NOT NULL,
  uom varchar(20),
  spec_min varchar(60),
  spec_max varchar(60),
  CONSTRAINT coa_line_pk PRIMARY KEY (coa_ref, test_cd)
);
COMMENT ON TABLE winchdepot01.coa_line IS 'Test results stated on the supplier certificates in coa_hdr.';

CREATE TABLE IF NOT EXISTS winchdepot01.dg_class (
  class_ref varchar(40) NOT NULL,
  un_no varchar(20) NOT NULL,
  subst_cd varchar(20),
  prd_cd varchar(20),
  form_desc text NOT NULL,
  pkg_grp varchar(5),
  haz_cls varchar(10) NOT NULL,
  lbl_desc text NOT NULL,
  docs_desc text NOT NULL,
  class_dt date NOT NULL,
  CONSTRAINT dg_class_pk PRIMARY KEY (class_ref)
);
COMMENT ON TABLE winchdepot01.dg_class IS 'Transport classifications of Coco substances and products (Transport Classifications) used to prepare the dangerous goods declaration and pack.';

CREATE TABLE IF NOT EXISTS winchdepot01.dg_signatory (
  worker_ref varchar(20) NOT NULL,
  dg_mode varchar(4) NOT NULL,
  dg_cert varchar(40) NOT NULL,
  cert_from date NOT NULL,
  cert_to date NOT NULL,
  cert_sts varchar(10) NOT NULL,
  CONSTRAINT dg_signatory_pk PRIMARY KEY (worker_ref, dg_mode)
);
COMMENT ON TABLE winchdepot01.dg_signatory IS 'Dangerous goods certificates of the depot''s signatories (Worker Qualifications); dg_mode AIR (IATA DGR) or ROAD (ADR); dg_consign.dg_cert must be current here.';

-- End of subscription tables.

GRANT USAGE ON SCHEMA winchdepot01 TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA winchdepot01 TO egeria_user, airflow_user;
