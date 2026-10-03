-- system-qualified-name: SoftwareServer::AUS-SYS-016::SN-CRM-AU-20200901
-- Salesforce Sales Cloud CRM - Austin.  Austin's Salesforce org: distributor and hospital accounts, treating
-- clinicians, and the Experience Cloud ordering portal objects for Dendrivax named-patient orders and clinician
-- adverse reaction reports.  Its tables feed Treatment Orders and Clinician Adverse Reaction Reports.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS salesforce_crm;
COMMENT ON SCHEMA salesforce_crm IS 'Salesforce Sales Cloud (Austin org): objects as replicated by Heroku Connect (lower-case, sfid keys).';

CREATE TABLE IF NOT EXISTS salesforce_crm.account (
  sfid                   varchar(18) NOT NULL,
  name                   varchar(255) NOT NULL,
  type                   varchar(40),
  billingcity            varchar(40),
  billingstatecode       varchar(10),
  billingcountrycode     varchar(3),
  sap_customer_number__c varchar(10),
  isdeleted              boolean NOT NULL,
  systemmodstamp         timestamptz NOT NULL,
  CONSTRAINT account_pk PRIMARY KEY (sfid)
);
COMMENT ON TABLE salesforce_crm.account IS 'Accounts (distributors and hospitals).';

INSERT INTO salesforce_crm.account (sfid, name, type, billingcity, billingstatecode, billingcountrycode, sap_customer_number__c, isdeleted, systemmodstamp) VALUES
('0015g0000000100j5M', 'McKesson Corporation', 'Distributor', 'Irving', 'TX', 'US', '200010', FALSE, '2026-06-02 08:00:00+00'),
('0015g0000000101qpR', 'Cardinal Health, Inc.', 'Distributor', 'Dublin', 'OH', 'US', '200020', FALSE, '2026-06-02 08:00:00+00'),
('0015g0000000102x3l', 'Cencora, Inc.', 'Distributor', 'Conshohocken', 'PA', 'US', '200030', FALSE, '2026-06-02 08:00:00+00'),
('0015g0000000103fAu', 'MD Anderson Cancer Center', 'Hospital', 'Houston', 'TX', 'US', '200040', FALSE, '2026-06-02 08:00:00+00'),
('0015g0000000104555', 'Baylor Scott & White Medical Center - Temple', 'Hospital', 'Temple', 'TX', 'US', '200050', FALSE, '2026-06-02 08:00:00+00'),
('0015g0000000105wIp', 'UT Southwestern Medical Center', 'Hospital', 'Dallas', 'TX', 'US', '200060', FALSE, '2026-06-02 08:00:00+00'),
('0015g0000000106Ydp', 'Dell Seton Medical Center at UT', 'Hospital', 'Austin', 'TX', 'US', '200070', FALSE, '2026-06-02 08:00:00+00'),
('0015g0000000107tAe', 'McKesson Canada Corporation', 'Distributor', 'Mississauga', 'ON', 'CA', '200080', FALSE, '2026-06-02 08:00:00+00')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS salesforce_crm.contact (
  sfid      varchar(18) NOT NULL,
  accountid varchar(18) NOT NULL,
  firstname varchar(40),
  lastname  varchar(80) NOT NULL,
  title     varchar(128),
  npi__c    varchar(10),
  isdeleted boolean NOT NULL,
  CONSTRAINT contact_pk PRIMARY KEY (sfid)
);
COMMENT ON TABLE salesforce_crm.contact IS 'Treating clinicians (NPI on the contact).';

INSERT INTO salesforce_crm.contact (sfid, accountid, firstname, lastname, title, npi__c, isdeleted) VALUES
('0035g0000000200Dw6', '0015g0000000103fAu', 'Elena', 'Vasquez', 'Medical Oncologist', '1487621930', FALSE),
('0035g0000000201RR1', '0015g0000000103fAu', 'Thomas', 'Greer', 'Hematologist-Oncologist', '1932045718', FALSE),
('0035g0000000202axZ', '0015g0000000105wIp', 'Anjali', 'Mehta', 'Medical Oncologist', '1255390846', FALSE),
('0035g0000000203w9x', '0015g0000000106Ydp', 'William', 'Harper', 'Medical Oncologist', '1609273354', FALSE),
('0035g0000000204nUZ', '0015g0000000104555', 'Rachel', 'Obi', 'Medical Oncologist', '1780462915', FALSE)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS salesforce_crm.therapy_order__c (
  sfid                 varchar(18) NOT NULL,
  name                 varchar(80) NOT NULL,
  account__c           varchar(18) NOT NULL,
  clinician__c         varchar(18) NOT NULL,
  patient_reference__c varchar(40) NOT NULL,
  product_code__c      varchar(20) NOT NULL,
  doses__c             numeric(4,0) NOT NULL,
  order_date__c        date NOT NULL,
  status__c            varchar(40) NOT NULL,
  createddate          timestamptz NOT NULL,
  isdeleted            boolean NOT NULL,
  CONSTRAINT therapy_order__c_pk PRIMARY KEY (sfid)
);
COMMENT ON TABLE salesforce_crm.therapy_order__c IS 'Named-patient therapy orders submitted through the clinician ordering portal (patient reference = programme enrolment ID).';

INSERT INTO salesforce_crm.therapy_order__c (sfid, name, account__c, clinician__c, patient_reference__c, product_code__c, doses__c, order_date__c, status__c, createddate, isdeleted) VALUES
('a0B5g00000003000rl', 'TO-26-0014', '0015g0000000105wIp', '0035g0000000202axZ', 'DVX-P-0114', 'AU-7710', 1, '2026-06-01', 'Cancelled', '2026-06-01 15:30:00+00', FALSE),
('a0B5g0000000301zJT', 'TO-26-0015', '0015g0000000103fAu', '0035g0000000200Dw6', 'DVX-P-0115', 'AU-7710', 1, '2026-06-29', 'Completed', '2026-06-29 15:30:00+00', FALSE),
('a0B5g0000000302K6p', 'TO-26-0016', '0015g0000000106Ydp', '0035g0000000203w9x', 'DVX-P-0116', 'AU-7710', 1, '2026-07-27', 'Completed', '2026-07-27 15:30:00+00', FALSE),
('a0B5g00000003031CC', 'TO-26-0017', '0015g0000000103fAu', '0035g0000000201RR1', 'DVX-P-0117', 'AU-7710', 1, '2026-08-18', 'Completed', '2026-08-18 15:30:00+00', FALSE),
('a0B5g0000000304kwy', 'TO-26-0018', '0015g0000000104555', '0035g0000000204nUZ', 'DVX-P-0118', 'AU-7710', 1, '2026-09-01', 'In Manufacture', '2026-09-01 15:30:00+00', FALSE),
('a0B5g00000003057fc', 'TO-26-0019', '0015g0000000105wIp', '0035g0000000202axZ', 'DVX-P-0119', 'AU-7710', 1, '2026-09-14', 'Awaiting Material', '2026-09-14 15:30:00+00', FALSE),
('a0B5g0000000306Ek6', 'TO-26-0020', '0015g0000000103fAu', '0035g0000000200Dw6', 'DVX-P-0120', 'AU-7710', 1, '2026-09-28', 'Submitted', '2026-09-28 15:30:00+00', FALSE)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS salesforce_crm.adverse_reaction_report__c (
  sfid                    varchar(18) NOT NULL,
  name                    varchar(80) NOT NULL,
  therapy_order__c        varchar(18),
  reporter__c             varchar(18) NOT NULL,
  patient_pseudonym__c    varchar(40) NOT NULL,
  product_code__c         varchar(20) NOT NULL,
  batch_number__c         varchar(40),
  reaction_description__c text NOT NULL,
  reported_severity__c    varchar(20),
  createddate             timestamptz NOT NULL,
  isdeleted               boolean NOT NULL,
  CONSTRAINT adverse_reaction_report__c_pk PRIMARY KEY (sfid)
);
COMMENT ON TABLE salesforce_crm.adverse_reaction_report__c IS 'Adverse reaction reports submitted by clinicians through the ordering portal.';

INSERT INTO salesforce_crm.adverse_reaction_report__c (sfid, name, therapy_order__c, reporter__c, patient_pseudonym__c, product_code__c, batch_number__c, reaction_description__c, reported_severity__c, createddate, isdeleted) VALUES
('a0C5g0000000400s1q', 'ARR-000031', 'a0B5g0000000301zJT', '0035g0000000200Dw6', 'PP-FA1AF588F5B4', 'AU-7710', 'A26-7710-P015', 'Grade 2 cytokine release syndrome: fever 39.1 C and hypotension responsive to fluids, 36 hours after infusion', 'Moderate', '2026-08-03 14:48:00+00', FALSE),
('a0C5g0000000401XCt', 'ARR-000034', 'a0B5g00000003031CC', '0035g0000000201RR1', 'PP-08BA47CBA05B', 'AU-7710', 'A26-7710-P017', 'Chills and rigors during the infusion, resolved within two hours without treatment', 'Mild', '2026-09-19 17:22:00+00', FALSE)
ON CONFLICT DO NOTHING;

GRANT USAGE ON SCHEMA salesforce_crm TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA salesforce_crm TO egeria_user, airflow_user;
