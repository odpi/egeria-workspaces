-- system-qualified-name: SoftwareServer::AUS-SYS-014::SN-SRM-AU-20190617
-- SAP Ariba SRM - Austin.  SAP Ariba Supplier Lifecycle and Performance plus Ariba Invoicing for Austin: supplier
-- registration, new supplier requests with risk screening, supplier bank-detail change requests and invoice
-- reconciliation.  Its tables feed Third Party Onboarding Cases, Supplier Payment Detail Changes and Supplier
-- Payments.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS sap_ariba;
COMMENT ON SCHEMA sap_ariba IS 'SAP Ariba (Austin realm): SLP supplier, supplier request, risk screening, bank change request and invoice reconciliation data as landed by the Ariba analytical reporting API.';

CREATE TABLE IF NOT EXISTS sap_ariba.sm_supplier (
  sm_vendor_id         varchar(20) NOT NULL,
  supplier_name        varchar(200) NOT NULL,
  country_code         varchar(2) NOT NULL,
  registration_status  varchar(30) NOT NULL,
  qualification_status varchar(30) NOT NULL,
  erp_vendor_id        varchar(10),
  created_date         date NOT NULL,
  CONSTRAINT sm_supplier_pk PRIMARY KEY (sm_vendor_id)
);
COMMENT ON TABLE sap_ariba.sm_supplier IS 'Supplier Management suppliers linked to SAP vendors.';

INSERT INTO sap_ariba.sm_supplier (sm_vendor_id, supplier_name, country_code, registration_status, qualification_status, erp_vendor_id, created_date) VALUES
('S200300030', 'Zhejiang Huahai Pharmaceutical Co., Ltd.', 'CN', 'Registered', 'Qualified', '100010', '2018-10-02'),
('S200300060', 'Dr. Reddy''s Laboratories Ltd', 'IN', 'Registered', 'Qualified', '100020', '2018-10-02'),
('S200300090', 'Heraeus Precious Metals GmbH & Co. KG', 'DE', 'Registered', 'Qualified', '100030', '2018-11-15'),
('S200300120', 'DFE Pharma GmbH & Co. KG', 'DE', 'Registered', 'Qualified', '100040', '2019-02-11'),
('S200300150', 'Spectrum Chemical Mfg. Corp.', 'US', 'Registered', 'Qualified', '100050', '2018-10-02'),
('S200300180', 'SCHOTT Pharma USA, Inc.', 'US', 'Registered', 'Qualified', '100060', '2019-01-21'),
('S200300210', 'Berry Global, Inc.', 'US', 'Registered', 'Qualified', '100070', '2019-01-21'),
('S200300240', 'Roquette America, Inc.', 'US', 'Registered', 'Qualified', '100080', '2020-03-09'),
('S200300270', 'Lonestar Calibration Services LLC', 'US', 'Registered', 'Qualified', '100090', '2019-06-17'),
('S200300300', 'Hill Country Facilities, Inc.', 'US', 'Registered', 'Qualified', '100100', '2020-09-28'),
('S200300330', 'Lifeline Biologistics LLC', 'US', 'Registered', 'Qualified', '100110', '2021-10-04'),
('S200300360', 'Gulf Coast Cryogenics, Inc.', 'US', 'Registered', 'Qualified', '100120', '2025-04-14'),
('S200300420', 'Lone Star Cold Chain Couriers LLC', 'US', 'Registered', 'Qualified', '100140', '2026-08-19'),
('S200300390', 'Hyderabad Fine Chemicals Pvt Ltd', 'IN', 'Not Registered', 'Disqualified', '100130', '2026-07-29')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_ariba.sm_supplier_request (
  request_id                 varchar(20) NOT NULL,
  supplier_name              varchar(200) NOT NULL,
  country_code               varchar(2) NOT NULL,
  business_owner_description text,
  requester_user             varchar(40) NOT NULL,
  created_date               date NOT NULL,
  request_status             varchar(30) NOT NULL,
  sm_vendor_id               varchar(20),
  CONSTRAINT sm_supplier_request_pk PRIMARY KEY (request_id)
);
COMMENT ON TABLE sap_ariba.sm_supplier_request IS 'New supplier requests (the onboarding workflow).';

INSERT INTO sap_ariba.sm_supplier_request (request_id, supplier_name, country_code, business_owner_description, requester_user, created_date, request_status, sm_vendor_id) VALUES
('SR-26-0022', 'Austin Precision Metrology LLC', 'US', 'Owned by two former Mettler-Toledo field engineers; no parent company', 'npetrov', '2026-04-02', 'Rejected', NULL),
('SR-26-0031', 'Lone Star Cold Chain Couriers LLC', 'US', 'Privately held; majority owner Harlan Pruitt (Houston)', 'epark', '2026-07-08', 'Approved', 'S200300420'),
('SR-26-0035', 'Hyderabad Fine Chemicals Pvt Ltd', 'IN', 'Subsidiary of Deccan Speciality Holdings; directors not disclosed', 'epark', '2026-07-27', 'Rejected', 'S200300390'),
('SR-26-0038', 'Pinnacle Filtration Systems, Inc.', 'US', 'Wholly owned by Pinnacle Industrial Group, Inc. (NYSE: PIGI)', 'npetrov', '2026-09-10', 'Risk Assessment', NULL),
('SR-26-0040', 'Quimica Andina S.A.C.', 'PE', NULL, 'epark', '2026-09-24', 'Screening', NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_ariba.srm_risk_screening (
  screening_id   varchar(20) NOT NULL,
  request_id     varchar(20) NOT NULL,
  requested_at   timestamptz NOT NULL,
  screening_type varchar(40) NOT NULL,
  risk_rating    varchar(10),
  result_status  varchar(20) NOT NULL,
  CONSTRAINT srm_risk_screening_pk PRIMARY KEY (screening_id)
);
COMMENT ON TABLE sap_ariba.srm_risk_screening IS 'Risk screenings requested from the supplier risk provider for a supplier request.';

INSERT INTO sap_ariba.srm_risk_screening (screening_id, request_id, requested_at, screening_type, risk_rating, result_status) VALUES
('SCR-26-0118', 'SR-26-0022', '2026-04-02 16:10:00+00', 'All', 'High', 'Complete'),
('SCR-26-0164', 'SR-26-0031', '2026-07-08 14:30:00+00', 'All', 'Low', 'Complete'),
('SCR-26-0179', 'SR-26-0035', '2026-07-27 11:05:00+00', 'Sanctions', 'High', 'Complete'),
('SCR-26-0180', 'SR-26-0035', '2026-07-27 11:06:00+00', 'Adverse Media', 'High', 'Complete'),
('SCR-26-0203', 'SR-26-0038', '2026-09-10 09:40:00+00', 'All', 'Medium', 'Complete'),
('SCR-26-0214', 'SR-26-0040', '2026-09-24 15:55:00+00', 'Sanctions', NULL, 'In Progress'),
('SCR-26-0215', 'SR-26-0040', '2026-09-24 15:56:00+00', 'Politically Exposed Persons', NULL, 'In Progress')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_ariba.sm_bank_change_request (
  change_request_id varchar(20) NOT NULL,
  sm_vendor_id      varchar(20) NOT NULL,
  submitted_at      timestamptz NOT NULL,
  submitted_by      varchar(80) NOT NULL,
  old_bank_ref      varchar(40),
  new_bank_ref      varchar(40) NOT NULL,
  approval_status   varchar(30) NOT NULL,
  CONSTRAINT sm_bank_change_request_pk PRIMARY KEY (change_request_id)
);
COMMENT ON TABLE sap_ariba.sm_bank_change_request IS 'Supplier profile update requests that change remittance bank details.';

INSERT INTO sap_ariba.sm_bank_change_request (change_request_id, sm_vendor_id, submitted_at, submitted_by, old_bank_ref, new_bank_ref, approval_status) VALUES
('BCR-26-0004', 'S200300150', '2026-03-11 17:25:00+00', 'ar@spectrumchemical.com', 'US-021000021-4471900017', 'US-021000021-4471902233', 'Verified'),
('BCR-26-0007', 'S200300030', '2026-05-20 03:10:00+00', 'finance@huahaipharm.com', 'CN-BOCH-7710044570019', 'CN-BOCH-7710044581230', 'Verified'),
('BCR-26-0009', 'S200300270', '2026-07-14 14:05:00+00', 'billing@lonestarcal.com', 'US-111000025-3319000552', 'US-111000025-3319002871', 'Verified'),
('BCR-26-0011', 'S200300300', '2026-08-26 22:47:00+00', 'accounts@hillcountry-facilities.co', 'US-114000093-2208847710', 'US-084009519-9901334467', 'Rejected'),
('BCR-26-0013', 'S200300090', '2026-09-25 08:15:00+00', 'treasury@heraeus.com', 'DE89370400440532013000', 'DE12500105170648489890', 'Pending Verification')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_ariba.invoice_reconciliation (
  ir_id                   varchar(20) NOT NULL,
  supplier_invoice_number varchar(40) NOT NULL,
  erp_vendor_id           varchar(10) NOT NULL,
  po_number               varchar(20) NOT NULL,
  receipt_id              varchar(40),
  invoice_date            date NOT NULL,
  total_amount            numeric(18,2) NOT NULL,
  currency                varchar(3) NOT NULL,
  reconciliation_status   varchar(20) NOT NULL,
  exception_type          varchar(40),
  CONSTRAINT invoice_reconciliation_pk PRIMARY KEY (ir_id)
);
COMMENT ON TABLE sap_ariba.invoice_reconciliation IS 'Invoice reconciliation documents (IR) against PO and receipt.';

INSERT INTO sap_ariba.invoice_reconciliation (ir_id, supplier_invoice_number, erp_vendor_id, po_number, receipt_id, invoice_date, total_amount, currency, reconciliation_status, exception_type) VALUES
('IR61200', 'GCC-26-0615', '100120', '4500001866', 'AUS1-R-26-0098', '2026-06-16', 34000.00, 'USD', 'Paid', NULL),
('IR61204', 'HH-INV-260611', '100010', '4500001871', 'AUS1-R-26-0101', '2026-06-23', 77500.00, 'USD', 'Paid', NULL),
('IR61208', 'DFE-90412277', '100040', '4500001874', 'AUS1-R-26-0102', '2026-06-24', 4800.00, 'USD', 'Paid', NULL),
('IR61212', 'SPC-INV-558812', '100050', '4500001875', 'AUS1-R-26-0103', '2026-06-25', 560.00, 'USD', 'Paid', NULL),
('IR61216', 'DRL/26/EXP/0441', '100020', '4500001880', 'AUS1-R-26-0104', '2026-07-07', 76860.00, 'USD', 'Exception', 'Price Variance'),
('IR61220', 'HPM-2026-07-1188', '100030', '4500001883', 'AUS1-R-26-0105', '2026-07-14', 57000.00, 'USD', 'Paid', NULL),
('IR61224', 'SCH-US-3310027', '100060', '4500001884', 'AUS1-R-26-0106', '2026-07-16', 3360.00, 'USD', 'Paid', NULL),
('IR61228', 'HH-INV-260809', '100010', '4500001902', 'AUS1-R-26-0107', '2026-08-11', 77500.00, 'USD', 'Reconciled', NULL),
('IR61232', 'LCS-2026-0814', '100090', '4500001898', NULL, '2026-08-14', 6850.00, 'USD', 'Paid', NULL),
('IR61236', 'SPC-INV-561470', '100050', '4500001905', 'AUS1-R-26-0108', '2026-08-18', 45600.00, 'USD', 'Paid', NULL),
('IR61240', 'LBL-88213', '100110', '4500001907', NULL, '2026-08-31', 9300.00, 'USD', 'Paid', NULL),
('IR61244', 'HCF-10277', '100100', '4500001913', NULL, '2026-09-02', 12400.00, 'USD', 'Paid', NULL),
('IR61248', 'ROQ-7719345', '100080', '4500001911', NULL, '2026-09-04', 1650.00, 'USD', 'Exception', 'Receipt Returned'),
('IR61252', 'DRL/26/EXP/0917', '100020', '4500001915', 'AUS1-R-26-0110', '2026-09-15', 75600.00, 'USD', 'Reconciled', NULL),
('IR61256', 'GCC-26-0922', '100120', '4500001921', 'AUS1-R-26-0111', '2026-09-23', 51000.00, 'USD', 'Reconciled', NULL)
ON CONFLICT DO NOTHING;

-- Subscription inbound: tables and columns written by the coco_subscriptions_austin_systems DAG from the
-- digital products this system subscribes to (see coco-subscription-loads/austin_systems/sap_ariba).
-- No extract reads them.

CREATE TABLE IF NOT EXISTS sap_ariba.erp_vendor (
  erp_vendor_id      varchar(10) NOT NULL,
  vendor_name        varchar(200) NOT NULL,
  country_code       varchar(2) NOT NULL,
  vendor_type        varchar(40) NOT NULL,
  approved           boolean NOT NULL,
  approved_date      date,
  vendor_status      varchar(20) NOT NULL,
  screening_status   varchar(20),
  screening_date     date,
  risk_rating        varchar(20),
  screening_ref      varchar(40),
  anomaly_ref        varchar(40),
  remit_bank_ref     varchar(40),
  remit_bank_name    varchar(120),
  remit_bank_country varchar(60),
  bank_change_ref    varchar(40),
  bank_verified_date date,
  CONSTRAINT erp_vendor_pk PRIMARY KEY (erp_vendor_id)
);
COMMENT ON TABLE sap_ariba.erp_vendor IS 'ERP vendor master replica with screening status and verified remittance account, checked by invoice reconciliation.  From Supplier Master Data.';

CREATE TABLE IF NOT EXISTS sap_ariba.erp_purchase_order (
  po_number     varchar(20) NOT NULL,
  erp_vendor_id varchar(10) NOT NULL,
  order_date    date NOT NULL,
  total_amount  numeric(18,2) NOT NULL,
  currency      varchar(3) NOT NULL,
  approver      varchar(40) NOT NULL,
  order_status  varchar(20) NOT NULL,
  CONSTRAINT erp_purchase_order_pk PRIMARY KEY (po_number)
);
COMMENT ON TABLE sap_ariba.erp_purchase_order IS 'ERP purchase order copies used for invoice matching, from Purchase Orders And Receipts.';

CREATE TABLE IF NOT EXISTS sap_ariba.erp_receipt (
  receipt_id     varchar(40) NOT NULL,
  po_number      varchar(20) NOT NULL,
  po_line_number integer NOT NULL,
  receipt_date   date NOT NULL,
  received_qty   integer NOT NULL,
  CONSTRAINT erp_receipt_pk PRIMARY KEY (receipt_id, po_number, po_line_number)
);
COMMENT ON TABLE sap_ariba.erp_receipt IS 'ERP goods receipt confirmations used for three-way invoice matching, from Purchase Orders And Receipts.';

CREATE TABLE IF NOT EXISTS sap_ariba.srm_screening_result (
  screening_id   varchar(40) NOT NULL,
  screened_name  varchar(200) NOT NULL,
  screening_date date NOT NULL,
  result_status  varchar(20) NOT NULL,
  match_count    integer NOT NULL,
  risk_rating    varchar(20),
  CONSTRAINT srm_screening_result_pk PRIMARY KEY (screening_id)
);
COMMENT ON TABLE sap_ariba.srm_screening_result IS 'Results returned by the screening provider for Ariba-requested screenings, from Third Party Screening Results.';

CREATE TABLE IF NOT EXISTS sap_ariba.srm_screening_match (
  screening_id      varchar(40) NOT NULL,
  list_name         varchar(120) NOT NULL,
  matched_name      varchar(200) NOT NULL,
  match_rating      varchar(20) NOT NULL,
  match_description text,
  CONSTRAINT srm_screening_match_pk PRIMARY KEY (screening_id, list_name, matched_name)
);
COMMENT ON TABLE sap_ariba.srm_screening_match IS 'Watch-list matches behind each screening result, from Third Party Screening Results.';

GRANT USAGE ON SCHEMA sap_ariba TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA sap_ariba TO egeria_user, airflow_user;
