-- system-qualified-name: System::KCDEPOT01
-- Kansas City Depot Management System - Coco core.  COTS depot management system at the Kansas City distribution centre, configured separately from the other depots (US DOT hazmat rules); feeds Goods Receipts and Dangerous Goods Consignment Records.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS kcdepot01;
COMMENT ON SCHEMA kcdepot01 IS 'Kansas City Depot Management System (Coco core): inbound receipts and hazmat shipments.';

CREATE TABLE IF NOT EXISTS kcdepot01.inbound_receipt (
  rcpt_nbr varchar(20) NOT NULL,
  po_nbr varchar(20) NOT NULL,
  vendor_id integer NOT NULL,
  sku varchar(10) NOT NULL,
  lot_nbr varchar(30) NOT NULL,
  rcpt_dt date NOT NULL,
  rcpt_qty integer NOT NULL,
  whse_cd varchar(6) NOT NULL,
  cert_nbr varchar(30),
  CONSTRAINT inbound_receipt_pk PRIMARY KEY (rcpt_nbr)
);
COMMENT ON TABLE kcdepot01.inbound_receipt IS 'Inbound receipts at the Kansas City distribution centre; sku in lower case, whse_cd DC01.';

CREATE TABLE IF NOT EXISTS kcdepot01.hazmat_employee (
  emp_id varchar(10) NOT NULL,
  worker_ref varchar(20) NOT NULL,
  emp_name varchar(60) NOT NULL,
  hm_cert_nbr varchar(30) NOT NULL,
  CONSTRAINT hazmat_employee_pk PRIMARY KEY (emp_id)
);
COMMENT ON TABLE kcdepot01.hazmat_employee IS 'Employees with 49 CFR 172 hazmat training who may sign shipping papers.';

CREATE TABLE IF NOT EXISTS kcdepot01.hazmat_shipment (
  bol_nbr varchar(20) NOT NULL,
  ship_dt date NOT NULL,
  carrier_scac varchar(4) NOT NULL,
  ship_to_name varchar(80) NOT NULL,
  ship_to_addr varchar(200) NOT NULL,
  un_na_nbr integer NOT NULL,
  ship_qty numeric(10,2) NOT NULL,
  ship_uom varchar(4) NOT NULL,
  signer_emp_id varchar(10) NOT NULL,
  signed_ts timestamptz NOT NULL,
  hm_cert_nbr varchar(30) NOT NULL,
  CONSTRAINT hazmat_shipment_pk PRIMARY KEY (bol_nbr)
);
COMMENT ON TABLE kcdepot01.hazmat_shipment IS 'Hazardous materials shipments (bill of lading); UN/NA number held as a number, carrier as SCAC.';

CREATE TABLE IF NOT EXISTS kcdepot01.shipment_doc (
  bol_nbr varchar(20) NOT NULL,
  doc_type_cd varchar(4) NOT NULL,
  doc_dt date NOT NULL,
  CONSTRAINT shipment_doc_pk PRIMARY KEY (bol_nbr, doc_type_cd)
);
COMMENT ON TABLE kcdepot01.shipment_doc IS 'Documents per shipment: BOL shipping paper, SDS, ERG emergency response guide page.';

INSERT INTO kcdepot01.inbound_receipt (rcpt_nbr, po_nbr, vendor_id, sku, lot_nbr, rcpt_dt, rcpt_qty, whse_cd, cert_nbr) VALUES
('KC260612-01', 'PO-NY-26-0142', 1000, 'pk0021', 'GML-VIAL-2606', '2026-06-12', 60, 'DC01', 'COC-GML-VIAL-2606'),
('KC260714-01', 'PO-NY-26-0163', 1000, 'pk0024', 'GML-BOX-2607', '2026-07-14', 5, 'DC01', NULL),
('KC260818-02', 'PO-NY-26-0177', 1000, 'pk0024', 'GML-BOX-2608', '2026-08-18', 100, 'DC01', 'COC-GML-BOX-2608'),
('KC260909-01', 'PO-NY-26-0190', 2000, 'pk0020', 'TT-BTL-2609', '2026-09-09', 50, 'DC01', 'COC-TT-BTL-2609')
ON CONFLICT DO NOTHING;

INSERT INTO kcdepot01.hazmat_employee (emp_id, worker_ref, emp_name, hm_cert_nbr) VALUES
('710118', 'CW-PLYYBU', 'Luis Ortega', 'DOT-HM-KC-0418')
ON CONFLICT DO NOTHING;

INSERT INTO kcdepot01.hazmat_shipment (bol_nbr, ship_dt, carrier_scac, ship_to_name, ship_to_addr, un_na_nbr, ship_qty, ship_uom, signer_emp_id, signed_ts, hm_cert_nbr) VALUES
('KC-BOL-26-0918', '2026-09-18', 'UPSN', 'Hampton Hospital Pharmacy', 'Nightingale St, New York, NY 10027, US', 1851, 12.5, 'KG', '710118', '2026-09-18 13:10+00', 'DOT-HM-KC-0418'),
('KC-BOL-26-0921', '2026-09-21', 'UPSN', 'The Crack Box', '55 Grizzly Peak Rd., Butte, MT 59801, US', 1851, 5.0, 'KG', '710118', '2026-09-21 12:45+00', 'DOT-HM-KC-0418'),
('KC-BOL-26-0924', '2026-09-24', 'SPDX', 'White Clover Medicinals', '305 - 14th Ave. S. Suite 3B, Seattle, WA 98128, US', 1851, 5.0, 'KG', '710118', '2026-09-24 14:00+00', 'DOT-HM-KC-0418'),
('KC-BOL-26-0929', '2026-09-29', 'UPSN', 'Rattlesnake Canyon Medicines', '2817 Milton Dr., Albuquerque, NM 87110, US', 1851, 2.5, 'KG', '710118', '2026-09-29 13:30+00', 'DOT-HM-KC-0418')
ON CONFLICT DO NOTHING;

INSERT INTO kcdepot01.shipment_doc (bol_nbr, doc_type_cd, doc_dt) VALUES
('KC-BOL-26-0918', 'BOL', '2026-09-18'),
('KC-BOL-26-0918', 'SDS', '2025-06-01'),
('KC-BOL-26-0918', 'ERG', '2026-09-18'),
('KC-BOL-26-0921', 'BOL', '2026-09-21'),
('KC-BOL-26-0921', 'SDS', '2025-06-01'),
('KC-BOL-26-0921', 'ERG', '2026-09-21'),
('KC-BOL-26-0924', 'BOL', '2026-09-24'),
('KC-BOL-26-0924', 'SDS', '2025-06-01'),
('KC-BOL-26-0924', 'ERG', '2026-09-24'),
('KC-BOL-26-0929', 'BOL', '2026-09-29'),
('KC-BOL-26-0929', 'SDS', '2025-06-01'),
('KC-BOL-26-0929', 'ERG', '2026-09-29')
ON CONFLICT DO NOTHING;


-- Tables added for the digital product subscriptions (coco-subscription-loads).

ALTER TABLE kcdepot01.hazmat_employee ADD COLUMN IF NOT EXISTS hm_cert_exp date;
COMMENT ON COLUMN kcdepot01.hazmat_employee.hm_cert_exp IS 'Expiry of the hazmat training certificate (Worker Qualifications); a lapsed certificate may not sign shipping papers.';

CREATE TABLE IF NOT EXISTS kcdepot01.vendor (
  vendor_id integer NOT NULL,
  vendor_name varchar(200) NOT NULL,
  approved_flag char(1) NOT NULL,
  vendor_status varchar(10) NOT NULL,
  CONSTRAINT vendor_pk PRIMARY KEY (vendor_id)
);
COMMENT ON TABLE kcdepot01.vendor IS 'Suppliers the distribution centre may receive from (Supplier Master Data); vendor_id as in inbound_receipt.';

CREATE TABLE IF NOT EXISTS kcdepot01.lot_cert (
  cert_nbr varchar(40) NOT NULL,
  vendor_id integer NOT NULL,
  sku varchar(20) NOT NULL,
  lot_nbr varchar(40) NOT NULL,
  cert_type_cd varchar(4) NOT NULL,
  cert_dt date NOT NULL,
  conforms_flag char(1) NOT NULL,
  CONSTRAINT lot_cert_pk PRIMARY KEY (cert_nbr)
);
COMMENT ON TABLE kcdepot01.lot_cert IS 'Supplier certificates (Supplier Material Certificates) matched to inbound_receipt.cert_nbr; sku lower case, cert_type_cd COA or COC.';

CREATE TABLE IF NOT EXISTS kcdepot01.lot_cert_test (
  cert_nbr varchar(40) NOT NULL,
  test_cd varchar(40) NOT NULL,
  test_val varchar(60) NOT NULL,
  test_uom varchar(20),
  spec_min varchar(60),
  spec_max varchar(60),
  CONSTRAINT lot_cert_test_pk PRIMARY KEY (cert_nbr, test_cd)
);
COMMENT ON TABLE kcdepot01.lot_cert_test IS 'Test results stated on the supplier certificates in lot_cert.';

CREATE TABLE IF NOT EXISTS kcdepot01.hazmat_class (
  class_id varchar(40) NOT NULL,
  un_na_nbr integer NOT NULL,
  substance_cd varchar(20),
  sku varchar(20),
  shipped_form text NOT NULL,
  packing_grp varchar(5),
  hazard_class varchar(10) NOT NULL,
  label_text text NOT NULL,
  shipping_papers text NOT NULL,
  classified_dt date NOT NULL,
  CONSTRAINT hazmat_class_pk PRIMARY KEY (class_id)
);
COMMENT ON TABLE kcdepot01.hazmat_class IS 'Transport classifications of Coco substances and products (Transport Classifications) for 49 CFR shipping papers; UN/NA number held as a number as in hazmat_shipment.';

-- End of subscription tables.

GRANT USAGE ON SCHEMA kcdepot01 TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA kcdepot01 TO egeria_user, airflow_user;
