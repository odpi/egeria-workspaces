-- system-qualified-name: System::EDDEPOT01
-- Edmonton Depot Management System - Coco core.  COTS depot management system at the Edmonton depot, configured separately from the other depots (Canadian TDG rules); feeds Goods Receipts and Dangerous Goods Consignment Records.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS eddepot01;
COMMENT ON SCHEMA eddepot01 IS 'Edmonton Depot Management System (Coco core): receipts and TDG dangerous goods shipments.';

CREATE TABLE IF NOT EXISTS eddepot01.receipt (
  receipt_id varchar(20) NOT NULL,
  vendor varchar(10) NOT NULL,
  po_number varchar(20) NOT NULL,
  item varchar(10) NOT NULL,
  vendor_lot varchar(30) NOT NULL,
  received varchar(8) NOT NULL,
  qty numeric(12,3) NOT NULL,
  bin varchar(6) NOT NULL,
  coa varchar(30),
  CONSTRAINT receipt_pk PRIMARY KEY (receipt_id)
);
COMMENT ON TABLE eddepot01.receipt IS 'Receipts at the Edmonton depot. vendor is ''V'' + Coco supplier id; received is text YYYYMMDD; bin is the depot area (RM01, PK01).';

CREATE TABLE IF NOT EXISTS eddepot01.tdg_signer (
  emp_no varchar(10) NOT NULL,
  worker_ref varchar(20) NOT NULL,
  tdg_cert_no varchar(20) NOT NULL,
  cert_expiry date NOT NULL,
  CONSTRAINT tdg_signer_pk PRIMARY KEY (emp_no)
);
COMMENT ON TABLE eddepot01.tdg_signer IS 'Staff trained and certified to sign TDG shipping documents.';

CREATE TABLE IF NOT EXISTS eddepot01.tdg_shipment (
  shipment_no varchar(12) NOT NULL,
  ship_date date NOT NULL,
  carrier_name varchar(40) NOT NULL,
  consignee_addr text NOT NULL,
  un_number varchar(6) NOT NULL,
  qty numeric(10,2) NOT NULL,
  unit varchar(4) NOT NULL,
  signatory varchar(10) NOT NULL,
  signed_at varchar(16) NOT NULL,
  tdg_cert_no varchar(20) NOT NULL,
  CONSTRAINT tdg_shipment_pk PRIMARY KEY (shipment_no)
);
COMMENT ON TABLE eddepot01.tdg_shipment IS 'Transportation of Dangerous Goods shipments (mostly hazardous waste to disposal). signed_at is local text; signatory is the employee number.';

CREATE TABLE IF NOT EXISTS eddepot01.tdg_document (
  shipment_no varchar(12) NOT NULL,
  doc_no smallint NOT NULL,
  doc_kind varchar(40) NOT NULL,
  doc_date date NOT NULL,
  CONSTRAINT tdg_document_pk PRIMARY KEY (shipment_no, doc_no)
);
COMMENT ON TABLE eddepot01.tdg_document IS 'Documents accompanying each TDG shipment.';

INSERT INTO eddepot01.receipt (receipt_id, vendor, po_number, item, vendor_lot, received, qty, bin, coa) VALUES
('ED-GR-26-0061', 'V3000', 'PO-AMS-26-0321', 'RM2001', 'GG-AML-26-0192', '20260608', 150, 'RM01', 'COA-GG-26-0192'),
('ED-GR-26-0067', 'V3000', 'PO-AMS-26-0329', 'RM4001', 'GG-MET-26-0077', '20260622', 300, 'RM01', 'COA-GG-26-0077'),
('ED-GR-26-0072', 'V9000', 'PO-AMS-26-0347', 'RM1002', 'WWE-MCC-2607-12', '20260713', 1500, 'RM01', 'COA-WWE-2607-12'),
('ED-GR-26-0079', 'V3000', 'PO-AMS-26-0373', 'RM2001', 'GG-AML-26-0251', '20260810', 150, 'RM01', 'COA-GG-26-0251'),
('ED-GR-26-0084', 'V1000', 'PO-AMS-26-0389', 'PK0020', 'GML-BTL-2608', '20260831', 40, 'PK01', 'COC-GML-BTL-2608'),
('ED-GR-26-0088', 'V3000', 'PO-AMS-26-0404', 'RM4001', 'GG-MET-26-0118', '20260921', 300, 'RM01', 'COA-GG-26-0118')
ON CONFLICT DO NOTHING;

INSERT INTO eddepot01.tdg_signer (emp_no, worker_ref, tdg_cert_no, cert_expiry) VALUES
('810071', 'CW-GBAX2A', 'TDG-AB-77120', '2027-10-03')
ON CONFLICT DO NOTHING;

INSERT INTO eddepot01.tdg_shipment (shipment_no, ship_date, carrier_name, consignee_addr, un_number, qty, unit, signatory, signed_at, tdg_cert_no) VALUES
('EDT-26-031', '2026-07-15', 'United Package', 'Prairie Waste Services, 2104 76 Ave NW, Edmonton, AB, CA', 'UN1170', 600.0, 'L', '810071', '2026-07-15 09:20', 'TDG-AB-77120'),
('EDT-26-037', '2026-08-12', 'United Package', 'Prairie Waste Services, 2104 76 Ave NW, Edmonton, AB, CA', 'UN1824', 800.0, 'L', '810071', '2026-08-12 10:05', 'TDG-AB-77120'),
('EDT-26-044', '2026-09-16', 'United Package', 'Prairie Waste Services, 2104 76 Ave NW, Edmonton, AB, CA', 'UN1170', 550.0, 'L', '810071', '2026-09-16 08:45', 'TDG-AB-77120')
ON CONFLICT DO NOTHING;

INSERT INTO eddepot01.tdg_document (shipment_no, doc_no, doc_kind, doc_date) VALUES
('EDT-26-031', 1, 'TDG Shipping Document', '2026-07-15'),
('EDT-26-031', 2, 'Safety Data Sheet', '2024-03-15'),
('EDT-26-037', 1, 'TDG Shipping Document', '2026-08-12'),
('EDT-26-037', 2, 'Safety Data Sheet', '2024-03-15'),
('EDT-26-044', 1, 'TDG Shipping Document', '2026-09-16'),
('EDT-26-044', 2, 'Safety Data Sheet', '2024-03-15')
ON CONFLICT DO NOTHING;


-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS eddepot01.vendor_master (
  vendor varchar(10) NOT NULL,
  vendor_name varchar(200) NOT NULL,
  approved char(1) NOT NULL,
  vendor_status varchar(10) NOT NULL,
  CONSTRAINT vendor_master_pk PRIMARY KEY (vendor)
);
COMMENT ON TABLE eddepot01.vendor_master IS 'Suppliers the depot may receive from (Supplier Master Data); vendor is ''V'' + Coco supplier id as in receipt.vendor.';

CREATE TABLE IF NOT EXISTS eddepot01.coa_cert (
  coa varchar(40) NOT NULL,
  vendor varchar(10) NOT NULL,
  item varchar(20) NOT NULL,
  vendor_lot varchar(40) NOT NULL,
  cert_kind varchar(40) NOT NULL,
  issued varchar(8) NOT NULL,
  conforms char(1) NOT NULL,
  CONSTRAINT coa_cert_pk PRIMARY KEY (coa)
);
COMMENT ON TABLE eddepot01.coa_cert IS 'Supplier certificates (Supplier Material Certificates) matched to receipt.coa at goods in; issued is text YYYYMMDD as in receipt.received.';

CREATE TABLE IF NOT EXISTS eddepot01.coa_cert_test (
  coa varchar(40) NOT NULL,
  test_code varchar(40) NOT NULL,
  test_value varchar(60) NOT NULL,
  test_unit varchar(20),
  spec_min varchar(60),
  spec_max varchar(60),
  CONSTRAINT coa_cert_test_pk PRIMARY KEY (coa, test_code)
);
COMMENT ON TABLE eddepot01.coa_cert_test IS 'Test results stated on the supplier certificates in coa_cert.';

CREATE TABLE IF NOT EXISTS eddepot01.tdg_class (
  class_id varchar(40) NOT NULL,
  un_number varchar(20) NOT NULL,
  substance varchar(20),
  item varchar(20),
  shipped_form text NOT NULL,
  packing_group varchar(5),
  tdg_class varchar(10) NOT NULL,
  labels text NOT NULL,
  documents text NOT NULL,
  classified_on date NOT NULL,
  CONSTRAINT tdg_class_pk PRIMARY KEY (class_id)
);
COMMENT ON TABLE eddepot01.tdg_class IS 'Transport classifications of Coco substances and products (Transport Classifications), used to prepare TDG shipping documents.';

-- End of subscription tables.

GRANT USAGE ON SCHEMA eddepot01 TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA eddepot01 TO egeria_user, airflow_user;
