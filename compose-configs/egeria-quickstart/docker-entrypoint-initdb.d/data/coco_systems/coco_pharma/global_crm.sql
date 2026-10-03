-- system-qualified-name: System::globalCRM
-- Global customer ordering system - Coco core.  SaaS ordering system for Coco's generic products and the personalised Cocolecel therapy, landed by a replication tool; feeds Treatment Orders, Clinician Adverse Reaction Reports and Treatment Invoices.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS global_crm;
COMMENT ON SCHEMA global_crm IS 'Global customer ordering system globalCRM (Coco core): accounts, prescribers, orders, collection requests, adverse reaction reports and invoices.';

CREATE TABLE IF NOT EXISTS global_crm.account (
  id varchar(18) NOT NULL,
  accountnumber varchar(20) NOT NULL,
  name varchar(120) NOT NULL,
  type varchar(40) NOT NULL,
  billingcity varchar(60),
  billingstate varchar(20),
  billingcountrycode varchar(2),
  CONSTRAINT account_pk PRIMARY KEY (id)
);
COMMENT ON TABLE global_crm.account IS 'Customer accounts: treating hospitals and pharmacies (accountnumber is the Coco customer id).';

CREATE TABLE IF NOT EXISTS global_crm.contact (
  id varchar(18) NOT NULL,
  accountid varchar(18) NOT NULL,
  firstname varchar(60) NOT NULL,
  lastname varchar(60) NOT NULL,
  title varchar(80),
  npi__c varchar(10),
  is_prescriber__c boolean NOT NULL,
  CONSTRAINT contact_pk PRIMARY KEY (id)
);
COMMENT ON TABLE global_crm.contact IS 'Clinicians at customer accounts; npi__c is the US National Provider Identifier.';

CREATE TABLE IF NOT EXISTS global_crm.sales_order (
  ordernumber varchar(20) NOT NULL,
  accountid varchar(18) NOT NULL,
  prescriber__c varchar(18),
  order_type__c varchar(40) NOT NULL,
  patient_mrn__c varchar(30),
  patient_reference__c varchar(20),
  effectivedate date NOT NULL,
  status varchar(30) NOT NULL,
  currencyisocode varchar(3) NOT NULL,
  CONSTRAINT sales_order_pk PRIMARY KEY (ordernumber)
);
COMMENT ON TABLE global_crm.sales_order IS 'Orders. order_type__c ''Personalized Therapy'' for clinician orders placed through the treatment portal, ''Standard'' for pharmacy orders; patient_reference__c is the pseudonym issued on acceptance.';

CREATE TABLE IF NOT EXISTS global_crm.sales_order_item (
  ordernumber varchar(20) NOT NULL,
  linenumber smallint NOT NULL,
  productcode varchar(10) NOT NULL,
  quantity integer NOT NULL,
  unitprice numeric(12,2) NOT NULL,
  CONSTRAINT sales_order_item_pk PRIMARY KEY (ordernumber, linenumber)
);
COMMENT ON TABLE global_crm.sales_order_item IS 'Order lines.';

CREATE TABLE IF NOT EXISTS global_crm.collection_request__c (
  name varchar(20) NOT NULL,
  order__c varchar(20) NOT NULL,
  collection_site__c varchar(80) NOT NULL,
  window_start__c date NOT NULL,
  window_end__c date NOT NULL,
  material_required__c varchar(120) NOT NULL,
  CONSTRAINT collection_request__c_pk PRIMARY KEY (name)
);
COMMENT ON TABLE global_crm.collection_request__c IS 'Patient material collection requests raised for personalised orders.';

CREATE TABLE IF NOT EXISTS global_crm.adverse_reaction__c (
  name varchar(20) NOT NULL,
  reported_date__c date NOT NULL,
  reporter__c varchar(18) NOT NULL,
  patient_reference__c varchar(20) NOT NULL,
  product_code__c varchar(10) NOT NULL,
  batch_number__c varchar(20),
  description__c text NOT NULL,
  severity__c varchar(20),
  CONSTRAINT adverse_reaction__c_pk PRIMARY KEY (name)
);
COMMENT ON TABLE global_crm.adverse_reaction__c IS 'Suspected adverse reactions reported by clinicians through the portal (severity is a free-typed picklist).';

CREATE TABLE IF NOT EXISTS global_crm.invoice__c (
  name varchar(20) NOT NULL,
  order__c varchar(20) NOT NULL,
  account__c varchar(18) NOT NULL,
  invoice_date__c date NOT NULL,
  total_amount__c numeric(14,2) NOT NULL,
  currencyisocode varchar(3) NOT NULL,
  due_date__c date NOT NULL,
  status__c varchar(20) NOT NULL,
  CONSTRAINT invoice__c_pk PRIMARY KEY (name)
);
COMMENT ON TABLE global_crm.invoice__c IS 'Invoices raised from fulfilled orders.';

INSERT INTO global_crm.account (id, accountnumber, name, type, billingcity, billingstate, billingcountrycode) VALUES
('001001', 'HAMPH', 'Hampton Hospital', 'Hospital', 'New York', 'NY', 'US'),
('001002', 'BOWAH', 'Bowden Arrow Hospital', 'Hospital', 'Boston', 'MA', 'US'),
('001003', 'OAKDH', 'Oak Dene Hospital', 'Hospital', 'Philadelphia', 'PA', 'US'),
('001004', 'OLDMH', 'Old Market Hospital', 'Hospital', 'Omaha', 'NE', 'US'),
('001101', 'AROUT', 'Around the Horn', 'Pharmacy', 'London', NULL, 'GB'),
('001102', 'THECR', 'The Crack Box', 'Pharmacy', 'Butte', 'MT', 'US'),
('001103', 'WHITC', 'White Clover Medicinals', 'Pharmacy', 'Seattle', 'WA', 'US')
ON CONFLICT DO NOTHING;

INSERT INTO global_crm.contact (id, accountid, firstname, lastname, title, npi__c, is_prescriber__c) VALUES
('CON-0417', '001001', 'Grant', 'Able', 'Consultant Haematologist', '1487623390', true),
('CON-0433', '001002', 'Julie', 'Stitched', 'Surgeon', '1932106648', true),
('CON-0451', '001003', 'Samuel', 'Okafor', 'Attending Oncologist', '1164598832', true),
('CON-0468', '001004', 'Fiona', 'Marsh', 'Consultant Oncologist', '1558302217', true)
ON CONFLICT DO NOTHING;

INSERT INTO global_crm.sales_order (ordernumber, accountid, prescriber__c, order_type__c, patient_mrn__c, patient_reference__c, effectivedate, status, currencyisocode) VALUES
('SO-26-01102', '001001', 'CON-0417', 'Personalized Therapy', 'HH-0048213', 'CPX-7K4Q2M', '2026-05-11', 'Delivered', 'USD'),
('SO-26-01127', '001002', 'CON-0433', 'Personalized Therapy', 'BA-7730021', 'CPX-3M8R1T', '2026-06-02', 'Delivered', 'USD'),
('SO-26-01145', '001003', 'CON-0451', 'Personalized Therapy', 'ODH-551903', 'CPX-9D2H6W', '2026-06-23', 'Delivered', 'USD'),
('SO-26-01152', '001003', 'CON-0451', 'Personalized Therapy', 'ODH-552417', 'CPX-6W9C3E', '2026-07-01', 'Cancelled', 'USD'),
('SO-26-01163', '001001', 'CON-0417', 'Personalized Therapy', 'HH-0051377', 'CPX-5T1N8B', '2026-07-20', 'Delivered', 'USD'),
('SO-26-01181', '001004', 'CON-0468', 'Personalized Therapy', 'OMH-20931', 'CPX-2B7J4Y', '2026-08-24', 'In Manufacture', 'USD'),
('SO-26-01194', '001001', 'CON-0417', 'Personalized Therapy', 'HH-0052290', 'CPX-8F3L5P', '2026-09-14', 'Accepted', 'USD'),
('SO-26-01199', '001002', 'CON-0433', 'Personalized Therapy', 'BA-7741180', NULL, '2026-09-24', 'Submitted', 'USD'),
('SO-26-01171', '001101', NULL, 'Standard', NULL, NULL, '2026-08-03', 'Shipped', 'GBP'),
('SO-26-01186', '001102', NULL, 'Standard', NULL, NULL, '2026-09-02', 'Shipped', 'USD'),
('SO-26-01190', '001103', NULL, 'Standard', NULL, NULL, '2026-09-08', 'Shipped', 'USD')
ON CONFLICT DO NOTHING;

INSERT INTO global_crm.sales_order_item (ordernumber, linenumber, productcode, quantity, unitprice) VALUES
('SO-26-01102', 1, '9100', 1, 373000.0),
('SO-26-01127', 1, '9100', 1, 373000.0),
('SO-26-01145', 1, '9100', 1, 373000.0),
('SO-26-01152', 1, '9100', 1, 373000.0),
('SO-26-01163', 1, '9100', 1, 373000.0),
('SO-26-01181', 1, '9100', 1, 373000.0),
('SO-26-01194', 1, '9100', 1, 373000.0),
('SO-26-01199', 1, '9100', 1, 373000.0),
('SO-26-01171', 1, '1000', 400, 10.0),
('SO-26-01186', 1, '9000', 40, 120.0),
('SO-26-01190', 1, '9000', 40, 120.0)
ON CONFLICT DO NOTHING;

INSERT INTO global_crm.collection_request__c (name, order__c, collection_site__c, window_start__c, window_end__c, material_required__c) VALUES
('CR-26-01102', 'SO-26-01102', 'Hampton Hospital Apheresis Unit', '2026-05-18', '2026-05-22', 'Leukapheresis product, min 2 x 10^9 CD3+ cells'),
('CR-26-01127', 'SO-26-01127', 'Bowden Arrow Hospital Apheresis Unit', '2026-06-09', '2026-06-13', 'Leukapheresis product, min 2 x 10^9 CD3+ cells'),
('CR-26-01145', 'SO-26-01145', 'Oak Dene Hospital Apheresis Unit', '2026-06-30', '2026-07-04', 'Leukapheresis product, min 2 x 10^9 CD3+ cells'),
('CR-26-01152', 'SO-26-01152', 'Oak Dene Hospital Apheresis Unit', '2026-07-08', '2026-07-12', 'Leukapheresis product, min 2 x 10^9 CD3+ cells'),
('CR-26-01163', 'SO-26-01163', 'Hampton Hospital Apheresis Unit', '2026-07-27', '2026-07-31', 'Leukapheresis product, min 2 x 10^9 CD3+ cells'),
('CR-26-01181', 'SO-26-01181', 'Old Market Hospital Apheresis Unit', '2026-08-31', '2026-09-04', 'Leukapheresis product, min 2 x 10^9 CD3+ cells'),
('CR-26-01194', 'SO-26-01194', 'Hampton Hospital Apheresis Unit', '2026-09-21', '2026-09-25', 'Leukapheresis product, min 2 x 10^9 CD3+ cells'),
('CR-26-01199', 'SO-26-01199', 'Bowden Arrow Hospital Apheresis Unit', '2026-10-01', '2026-10-05', 'Leukapheresis product, min 2 x 10^9 CD3+ cells')
ON CONFLICT DO NOTHING;

INSERT INTO global_crm.adverse_reaction__c (name, reported_date__c, reporter__c, patient_reference__c, product_code__c, batch_number__c, description__c, severity__c) VALUES
('AE-26-0031', '2026-06-15', 'CON-0417', 'CPX-7K4Q2M', '9100', 'W26-9100-0003', 'Cytokine release syndrome grade 2 on day 3 after infusion; resolved with tocilizumab.', 'Moderate'),
('AE-26-0038', '2026-07-06', 'CON-0433', 'CPX-3M8R1T', '9100', 'W26-9100-0004', 'Immune effector cell-associated neurotoxicity (ICANS) grade 1, confusion for 24 hours.', 'Mild'),
('AE-26-0044', '2026-07-30', 'CON-0451', 'CPX-9D2H6W', '9100', 'W26-9100-0005', 'Prolonged cytopenia at day 28 requiring transfusion support.', 'Severe'),
('AE-26-0052', '2026-08-27', 'CON-0417', 'CPX-5T1N8B', '9100', 'W26-9100-0007', 'Fever 39C on day 2 (CRS grade 1), managed supportively.', 'mild'),
('AE-26-0057', '2026-09-22', 'CON-0417', 'CPX-4H6V9R', '9000', 'A26-9000-0019', 'Acute kidney injury after second cycle of cisplatin despite hydration protocol.', 'SEVERE'),
('AE-26-0060', '2026-09-28', 'CON-0468', 'CPX-1Q8Z3D', '2050', NULL, 'Extensive bruising and epistaxis two weeks after starting clopidogrel.', NULL)
ON CONFLICT DO NOTHING;

INSERT INTO global_crm.invoice__c (name, order__c, account__c, invoice_date__c, total_amount__c, currencyisocode, due_date__c, status__c) VALUES
('INV-26-004417', 'SO-26-01102', '001001', '2026-06-10', 373000.0, 'USD', '2026-08-09', 'Paid'),
('INV-26-004562', 'SO-26-01127', '001002', '2026-07-01', 373000.0, 'USD', '2026-08-30', 'Paid'),
('INV-26-004698', 'SO-26-01145', '001003', '2026-07-23', 373000.0, 'USD', '2026-09-21', 'Paid'),
('INV-26-004901', 'SO-26-01163', '001001', '2026-08-20', 373000.0, 'USD', '2026-10-19', 'Open'),
('INV-26-004877', 'SO-26-01171', '001101', '2026-08-07', 4000.0, 'GBP', '2026-09-06', 'Paid'),
('INV-26-005033', 'SO-26-01186', '001102', '2026-09-22', 4800.0, 'USD', '2026-10-22', 'Open')
ON CONFLICT DO NOTHING;


-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS global_crm.therapy_shipment_event__c (
  batch_number__c varchar(40) NOT NULL,
  event_type__c varchar(20) NOT NULL,
  event_time__c timestamptz NOT NULL,
  order__c varchar(40) NOT NULL,
  patient_reference__c varchar(40) NOT NULL,
  location__c varchar(120),
  storage_conditions__c text,
  CONSTRAINT therapy_shipment_event__c_pk PRIMARY KEY (batch_number__c, event_type__c, event_time__c)
);
COMMENT ON TABLE global_crm.therapy_shipment_event__c IS 'Shipment events of personalised therapy batches (Therapy Delivery Events), shown on the order in the treatment portal.';

CREATE TABLE IF NOT EXISTS global_crm.therapy_administration__c (
  batch_number__c varchar(40) NOT NULL,
  order__c varchar(40) NOT NULL,
  patient_reference__c varchar(40) NOT NULL,
  administered_at__c timestamptz NOT NULL,
  clinician__c varchar(40) NOT NULL,
  CONSTRAINT therapy_administration__c_pk PRIMARY KEY (batch_number__c)
);
COMMENT ON TABLE global_crm.therapy_administration__c IS 'Confirmation that a personalised therapy batch was administered (Therapy Delivery Events) - the fulfilment that lets the order be invoiced.';

-- End of subscription tables.

GRANT USAGE ON SCHEMA global_crm TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA global_crm TO egeria_user, airflow_user;
