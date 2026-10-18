-- system-qualified-name: SoftwareServer::AUS-SYS-011::SN-OMS-AU-20200310
-- Oracle Order Management - Austin.  Oracle Order Management Cloud for Austin: sales orders registered from the
-- Salesforce portal with the patient therapy extensible flexfield, order holds, and the receivables invoices raised on
-- fulfilment.  Its tables feed Treatment Orders (sample collection), Clinician Adverse Reaction Reports (reactions
-- phoned to the order desk) and Treatment Invoices.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS oracle_oms;
COMMENT ON SCHEMA oracle_oms IS 'Oracle Fusion Order Management and Receivables (Austin business unit): DOO and RA tables as landed by BI Cloud Connector extracts.';

CREATE TABLE IF NOT EXISTS oracle_oms.hz_cust_accounts (
  cust_account_id     bigint NOT NULL,
  account_number      varchar(30) NOT NULL,
  account_name        varchar(240),
  customer_class_code varchar(30),
  status              char(1) NOT NULL,
  CONSTRAINT hz_cust_accounts_pk PRIMARY KEY (cust_account_id)
);
COMMENT ON TABLE oracle_oms.hz_cust_accounts IS 'Customer accounts (account number = SAP customer number, mastered in Informatica MDM).';

INSERT INTO oracle_oms.hz_cust_accounts (cust_account_id, account_number, account_name, customer_class_code, status) VALUES
(300010, '200010', 'McKesson Corporation', 'DISTRIBUTOR', 'A'),
(300020, '200020', 'Cardinal Health, Inc.', 'DISTRIBUTOR', 'A'),
(300030, '200030', 'Cencora, Inc.', 'DISTRIBUTOR', 'A'),
(300040, '200040', 'MD Anderson Cancer Center', 'HOSPITAL', 'A'),
(300050, '200050', 'Baylor Scott & White Medical Center - Temple', 'HOSPITAL', 'A'),
(300060, '200060', 'UT Southwestern Medical Center', 'HOSPITAL', 'A'),
(300070, '200070', 'Dell Seton Medical Center at UT', 'HOSPITAL', 'A'),
(300080, '200080', 'McKesson Canada Corporation', 'DISTRIBUTOR', 'A')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS oracle_oms.doo_headers_all (
  header_id                   bigint NOT NULL,
  order_number                varchar(50) NOT NULL,
  source_order_number         varchar(50) NOT NULL,
  source_order_system         varchar(30) NOT NULL,
  ordered_date                timestamptz NOT NULL,
  sold_to_customer_id         bigint NOT NULL,
  status_code                 varchar(30) NOT NULL,
  transactional_currency_code varchar(3) NOT NULL,
  CONSTRAINT doo_headers_all_pk PRIMARY KEY (header_id)
);
COMMENT ON TABLE oracle_oms.doo_headers_all IS 'Sales order headers (source order number = portal order number).';

INSERT INTO oracle_oms.doo_headers_all (header_id, order_number, source_order_number, source_order_system, ordered_date, sold_to_customer_id, status_code, transactional_currency_code) VALUES
(810000, 'OM104220', 'TO-26-0014', 'SFDC', '2026-06-01 15:31:00+00', 300060, 'CANCELLED', 'USD'),
(810013, 'OM104223', 'TO-26-0015', 'SFDC', '2026-06-29 15:31:00+00', 300040, 'CLOSED', 'USD'),
(810026, 'OM104226', 'TO-26-0016', 'SFDC', '2026-07-27 15:31:00+00', 300070, 'CLOSED', 'USD'),
(810039, 'OM104229', 'TO-26-0017', 'SFDC', '2026-08-18 15:31:00+00', 300040, 'CLOSED', 'USD'),
(810052, 'OM104232', 'TO-26-0018', 'SFDC', '2026-09-01 15:31:00+00', 300050, 'PROCESSING', 'USD'),
(810065, 'OM104235', 'TO-26-0019', 'SFDC', '2026-09-14 15:31:00+00', 300060, 'AWAIT_MATERIAL', 'USD'),
(810078, 'OM104238', 'TO-26-0020', 'SFDC', '2026-09-28 15:31:00+00', 300040, 'OPEN', 'USD')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS oracle_oms.doo_lines_all (
  line_id               bigint NOT NULL,
  header_id             bigint NOT NULL,
  line_number           integer NOT NULL,
  inventory_item_number varchar(40) NOT NULL,
  ordered_qty           numeric(10,2) NOT NULL,
  ordered_uom           varchar(10) NOT NULL,
  status_code           varchar(30) NOT NULL,
  lot_number            varchar(40),
  actual_ship_date      date,
  CONSTRAINT doo_lines_all_pk PRIMARY KEY (line_id)
);
COMMENT ON TABLE oracle_oms.doo_lines_all IS 'Sales order lines (lot = patient-specific batch).';

INSERT INTO oracle_oms.doo_lines_all (line_id, header_id, line_number, inventory_item_number, ordered_qty, ordered_uom, status_code, lot_number, actual_ship_date) VALUES
(8100001, 810000, 1, 'AU-7710', 1, 'BAG', 'CANCELLED', NULL, NULL),
(8100131, 810013, 1, 'AU-7710', 1, 'BAG', 'CLOSED', 'A26-7710-P015', '2026-07-28'),
(8100261, 810026, 1, 'AU-7710', 1, 'BAG', 'CLOSED', 'A26-7710-P016', '2026-08-25'),
(8100391, 810039, 1, 'AU-7710', 1, 'BAG', 'CLOSED', 'A26-7710-P017', '2026-09-15'),
(8100521, 810052, 1, 'AU-7710', 1, 'BAG', 'PROCESSING', 'A26-7710-P018', NULL),
(8100651, 810065, 1, 'AU-7710', 1, 'BAG', 'AWAIT_MATERIAL', 'A26-7710-P019', NULL),
(8100781, 810078, 1, 'AU-7710', 1, 'BAG', 'OPEN', NULL, NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS oracle_oms.doo_headers_eff_b (
  header_id       bigint NOT NULL,
  context_code    varchar(80) NOT NULL,
  attribute_char1 varchar(150),
  attribute_char2 varchar(150),
  attribute_char3 varchar(150),
  attribute_char4 varchar(150),
  attribute_date1 date,
  attribute_date2 date,
  CONSTRAINT doo_headers_eff_b_pk PRIMARY KEY (header_id, context_code)
);
COMMENT ON TABLE oracle_oms.doo_headers_eff_b IS 'Order header extensible flexfield, context PatientTherapy: char1 patient pseudonym, char2 clinician NPI, char3 collection site, char4 material, date1/date2 collection window.';

INSERT INTO oracle_oms.doo_headers_eff_b (header_id, context_code, attribute_char1, attribute_char2, attribute_char3, attribute_char4, attribute_date1, attribute_date2) VALUES
(810000, 'PatientTherapy', 'PP-3349A011D084', '1255390846', 'UTSW Apheresis Unit, Dallas', 'Leukapheresis product', '2026-06-10', '2026-06-12'),
(810013, 'PatientTherapy', 'PP-FA1AF588F5B4', '1487621930', 'MD Anderson Apheresis Unit, Houston', 'Leukapheresis product', '2026-07-08', '2026-07-10'),
(810026, 'PatientTherapy', 'PP-CCD4B098EAFF', '1609273354', 'Dell Seton Infusion Center, Austin', 'Leukapheresis product', '2026-08-05', '2026-08-07'),
(810039, 'PatientTherapy', 'PP-08BA47CBA05B', '1932045718', 'MD Anderson Apheresis Unit, Houston', 'Leukapheresis product', '2026-08-27', '2026-08-29'),
(810052, 'PatientTherapy', 'PP-06CCD43B6C3E', '1780462915', 'BSW Temple Cell Collection Center', 'Leukapheresis product', '2026-09-10', '2026-09-12'),
(810065, 'PatientTherapy', 'PP-585B1C61A454', '1255390846', 'UTSW Apheresis Unit, Dallas', 'Leukapheresis product', '2026-09-28', '2026-09-30'),
(810078, 'PatientTherapy', 'PP-23245D351691', '1487621930', 'MD Anderson Apheresis Unit, Houston', 'Leukapheresis product', '2026-10-12', '2026-10-14')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS oracle_oms.doo_hold_instances (
  hold_instance_id bigint NOT NULL,
  header_id        bigint NOT NULL,
  line_id          bigint,
  hold_code        varchar(30) NOT NULL,
  hold_comments    text,
  attribute1       varchar(150),
  applied_date     timestamptz NOT NULL,
  applied_by       varchar(64) NOT NULL,
  released_flag    char(1) NOT NULL,
  CONSTRAINT doo_hold_instances_pk PRIMARY KEY (hold_instance_id)
);
COMMENT ON TABLE oracle_oms.doo_hold_instances IS 'Order holds; CLIN_ADV_RXN holds record a clinician-reported reaction (attribute1 = severity as reported).';

INSERT INTO oracle_oms.doo_hold_instances (hold_instance_id, header_id, line_id, hold_code, hold_comments, attribute1, applied_date, applied_by, released_flag) VALUES
(300117, 810026, 8100261, 'CLIN_ADV_RXN', 'Clinician reported injection-site erythema and transient fatigue by phone and asked the order desk to hold follow-on treatment', 'MILD', '2026-09-02 13:05:00+00', 'ORDERDESK.KGRAY', 'N')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS oracle_oms.ra_customer_trx_all (
  customer_trx_id             bigint NOT NULL,
  trx_number                  varchar(20) NOT NULL,
  trx_date                    date NOT NULL,
  bill_to_customer_id         bigint NOT NULL,
  interface_header_attribute1 varchar(150),
  invoice_currency_code       varchar(3) NOT NULL,
  term_due_date               date,
  status_trx                  varchar(10) NOT NULL,
  complete_flag               char(1) NOT NULL,
  CONSTRAINT ra_customer_trx_all_pk PRIMARY KEY (customer_trx_id)
);
COMMENT ON TABLE oracle_oms.ra_customer_trx_all IS 'Receivables invoices created by AutoInvoice from fulfilled order lines (interface_header_attribute1 = OMS order number; status OP open, CL closed).';

INSERT INTO oracle_oms.ra_customer_trx_all (customer_trx_id, trx_number, trx_date, bill_to_customer_id, interface_header_attribute1, invoice_currency_code, term_due_date, status_trx, complete_flag) VALUES
(5500000, 'AR-26-10431', '2026-07-29', 300040, 'OM104223', 'USD', '2026-09-12', 'CL', 'Y'),
(5500007, 'AR-26-10434', '2026-08-25', 300070, 'OM104226', 'USD', '2026-10-09', 'OP', 'Y'),
(5500014, 'AR-26-10437', '2026-09-16', 300040, 'OM104229', 'USD', '2026-10-31', 'OP', 'Y')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS oracle_oms.ra_customer_trx_lines_all (
  customer_trx_line_id  bigint NOT NULL,
  customer_trx_id       bigint NOT NULL,
  line_number           integer NOT NULL,
  line_type             varchar(20) NOT NULL,
  extended_amount       numeric(18,2) NOT NULL,
  inventory_item_number varchar(40),
  sales_order           varchar(50),
  CONSTRAINT ra_customer_trx_lines_all_pk PRIMARY KEY (customer_trx_line_id)
);
COMMENT ON TABLE oracle_oms.ra_customer_trx_lines_all IS 'Receivables invoice lines.';

INSERT INTO oracle_oms.ra_customer_trx_lines_all (customer_trx_line_id, customer_trx_id, line_number, line_type, extended_amount, inventory_item_number, sales_order) VALUES
(55000001, 5500000, 1, 'LINE', 148000.00, 'AU-7710', 'OM104223'),
(55000071, 5500007, 1, 'LINE', 148000.00, 'AU-7710', 'OM104226'),
(55000141, 5500014, 1, 'LINE', 148000.00, 'AU-7710', 'OM104229')
ON CONFLICT DO NOTHING;

-- Subscription inbound: tables and columns written by the coco_subscriptions_austin_systems DAG from the
-- digital products this system subscribes to (see coco-subscription-loads/austin_systems/oracle_oms).
-- No extract reads them.

CREATE TABLE IF NOT EXISTS oracle_oms.doo_fulfillment_event_int (
  header_id        bigint NOT NULL,
  lot_number       varchar(40) NOT NULL,
  event_code       varchar(30) NOT NULL,
  event_date       timestamptz NOT NULL,
  event_location   varchar(150),
  patient_ref      varchar(150) NOT NULL,
  source_reference varchar(50) NOT NULL,
  CONSTRAINT doo_fulfillment_event_int_pk PRIMARY KEY (header_id, lot_number, event_code)
);
COMMENT ON TABLE oracle_oms.doo_fulfillment_event_int IS 'Fulfilment confirmation interface (therapy delivered / administered) that closes the fulfilment line and triggers AutoInvoice, from Therapy Delivery Events.';

GRANT USAGE ON SCHEMA oracle_oms TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA oracle_oms TO egeria_user, airflow_user;
