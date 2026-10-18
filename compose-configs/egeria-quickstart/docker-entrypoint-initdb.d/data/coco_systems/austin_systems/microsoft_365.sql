-- system-qualified-name: SoftwareServer::AUS-SYS-033::SN-M365-AU-20200601
-- Microsoft 365 - Austin.  The Austin Microsoft 365 tenant (Exchange Online, Teams, SharePoint).  Its recipient table
-- feeds Corporate Directory Entries for the cloud-only people who have no Active Directory account.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS microsoft_365;
COMMENT ON SCHEMA microsoft_365 IS 'Microsoft 365 (Austin): Exchange Online recipient objects (the global address list) as landed by the Exchange Online PowerShell export.';

CREATE TABLE IF NOT EXISTS microsoft_365.exo_recipient (
  externaldirectoryobjectid uuid NOT NULL,
  primarysmtpaddress        varchar(120) NOT NULL,
  firstname                 varchar(80),
  lastname                  varchar(80),
  displayname               varchar(160),
  title                     varchar(120),
  department                varchar(120),
  office                    varchar(120),
  phone                     varchar(30),
  manager                   varchar(120),
  customattribute1          varchar(20),
  recipienttypedetails      varchar(40) NOT NULL,
  isdirsynced               boolean NOT NULL,
  whenchanged               timestamptz NOT NULL,
  CONSTRAINT exo_recipient_pk PRIMARY KEY (externaldirectoryobjectid)
);
COMMENT ON TABLE microsoft_365.exo_recipient IS 'Exchange Online recipients; customAttribute1 carries the Workday employee ID; isDirSynced false = cloud-only.';

INSERT INTO microsoft_365.exo_recipient (externaldirectoryobjectid, primarysmtpaddress, firstname, lastname, displayname, title, department, office, phone, manager, customattribute1, recipienttypedetails, isdirsynced, whenchanged) VALUES
('d6e5262b-650f-9eba-fd15-2deb507efd40', 'rhernandez@austinpharma.com', 'Rebecca', 'Hernandez', 'Rebecca Hernandez', 'Site Head, Austin', 'Site Leadership', 'Austin Plant', '+1 512 555 0101', NULL, '100101', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('1abd5a54-dcc6-f3b0-70b8-b6c8d05540f4', 'mwhitfield@austinpharma.com', 'Marcus', 'Whitfield', 'Marcus Whitfield', 'Director of Quality Assurance', 'Quality Assurance', 'Austin Plant', '+1 512 555 0112', 'rhernandez@austinpharma.com', '100112', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('94dfa23b-657d-2cd4-941d-3b5508e57bc3', 'praman@austinpharma.com', 'Priya', 'Raman', 'Priya Raman', 'QA Batch Disposition Specialist', 'Quality Assurance', 'Austin Plant', '+1 512 555 0118', 'mwhitfield@austinpharma.com', '100118', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('203885eb-3aa6-35e6-74cb-76cd5c10478b', 'bfoster@austinpharma.com', 'Brian', 'Foster', 'Brian Foster', 'Production Operator II', 'Manufacturing', 'Austin Plant', '+1 512 555 0122', 'jmorales@austinpharma.com', '100122', 'SharedMailbox', TRUE, '2026-09-29 01:00:00+00'),
('75786fc1-95c4-f31e-c7b5-1692a7238d45', 'dokafor@austinpharma.com', 'Daniel', 'Okafor', 'Daniel Okafor', 'QC Laboratory Manager', 'Quality Control Laboratory', 'Austin Plant', '+1 512 555 0124', 'mwhitfield@austinpharma.com', '100124', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('9a24783f-cd4f-e7e7-e2a3-d6dedab00fc0', 'sdelgado@austinpharma.com', 'Sofia', 'Delgado', 'Sofia Delgado', 'QC Analyst II', 'Quality Control Laboratory', 'Austin Plant', '+1 512 555 0131', 'dokafor@austinpharma.com', '100131', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('fbe59352-60d4-495d-6ac3-b2e2fcf6d062', 'ktran@austinpharma.com', 'Kevin', 'Tran', 'Kevin Tran', 'QC Chromatography Analyst', 'Quality Control Laboratory', 'Austin Plant', '+1 512 555 0137', 'dokafor@austinpharma.com', '100137', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('f73c896d-87fd-224b-2c8f-882c91a051c3', 'jmorales@austinpharma.com', 'Jason', 'Morales', 'Jason Morales', 'Manufacturing Supervisor', 'Manufacturing', 'Austin Plant', '+1 512 555 0142', 'rhernandez@austinpharma.com', '100142', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('f8ccb52c-ef7e-dc50-c76c-338f966b0d58', 'abrooks@austinpharma.com', 'Aaliyah', 'Brooks', 'Aaliyah Brooks', 'Production Operator III', 'Manufacturing', 'Austin Plant', '+1 512 555 0149', 'jmorales@austinpharma.com', '100149', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('cde4585a-361d-ecc9-fa3f-e50974283c23', 'tnguyen@austinpharma.com', 'Tyler', 'Nguyen', 'Tyler Nguyen', 'Production Operator III', 'Manufacturing', 'Austin Plant', '+1 512 555 0153', 'jmorales@austinpharma.com', '100153', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('47b8e373-5b19-68a0-28c9-876b9608215c', 'glindqvist@austinpharma.com', 'Grace', 'Lindqvist', 'Grace Lindqvist', 'Cell Therapy Manufacturing Specialist', 'Cell Therapy Manufacturing', 'Austin Plant', '+1 512 555 0158', 'jmorales@austinpharma.com', '100158', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('151627eb-7752-7bff-969e-c34798928b4c', 'ohaddad@austinpharma.com', 'Omar', 'Haddad', 'Omar Haddad', 'Warehouse Lead', 'Warehouse and Logistics', 'Austin Distribution Center', '+1 512 555 0162', 'rhernandez@austinpharma.com', '100162', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('1332f649-d9b6-9e10-d443-eb453cf8736c', 'hkowalski@austinpharma.com', 'Hannah', 'Kowalski', 'Hannah Kowalski', 'Site Controller', 'Finance', 'Austin Plant', '+1 512 555 0167', 'rhernandez@austinpharma.com', '100167', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('871d5806-698c-72bd-d3cd-902067780246', 'lcarranza@austinpharma.com', 'Luis', 'Carranza', 'Luis Carranza', 'Senior Accountant', 'Finance', 'Austin Plant', '+1 512 555 0171', 'hkowalski@austinpharma.com', '100171', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('a1c22794-5f7d-bcc0-d241-84b6e8890290', 'moneill@austinpharma.com', 'Megan', 'O''Neill', 'Megan O''Neill', 'Accounts Payable Specialist', 'Finance', 'Austin Plant', '+1 512 555 0176', 'hkowalski@austinpharma.com', '100176', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('8bc771ec-a6af-6281-c616-19a61a8b65ae', 'epark@austinpharma.com', 'Ethan', 'Park', 'Ethan Park', 'Procurement Manager', 'Procurement', 'Austin Plant', '+1 512 555 0180', 'hkowalski@austinpharma.com', '100180', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('c72b2c9c-9cec-996c-14c0-e5579e9b3bd3', 'cbennett@austinpharma.com', 'Chloe', 'Bennett', 'Chloe Bennett', 'HR Business Partner', 'Human Resources', 'Austin Plant', '+1 512 555 0184', 'rhernandez@austinpharma.com', '100184', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('386e55eb-57e0-f7ab-50a2-a1f0c6e4dc97', 'sadeyemi@austinpharma.com', 'Samuel', 'Adeyemi', 'Samuel Adeyemi', 'Shipping and Dangerous Goods Coordinator', 'Warehouse and Logistics', 'Austin Distribution Center', '+1 512 555 0189', 'ohaddad@austinpharma.com', '100189', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('dd1b1f2a-d1a1-2d95-8c10-dc93b1e805c7', 'npetrov@austinpharma.com', 'Nina', 'Petrov', 'Nina Petrov', 'Maintenance and Calibration Engineer', 'Engineering and Maintenance', 'Austin Plant', '+1 512 555 0193', 'rhernandez@austinpharma.com', '100193', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('38162db3-4a5c-5980-c164-3e99b2f29878', 'rcastillo@austinpharma.com', 'Robert', 'Castillo', 'Robert Castillo', 'Customer Quality Specialist', 'Customer Quality and Safety', 'Austin Plant', '+1 512 555 0197', 'mwhitfield@austinpharma.com', '100197', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('503afe8a-75b5-567f-57b6-2323c466ce89', 'imoreno@austinpharma.com', 'Isabel', 'Moreno', 'Isabel Moreno', 'Drug Safety Associate', 'Customer Quality and Safety', 'Austin Plant', '+1 512 555 0201', 'mwhitfield@austinpharma.com', '100201', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('194e16db-ab1e-4cc8-61be-588f2ea39575', 'mjohnson@austinpharma.com', 'Mia', 'Johnson', 'Mia Johnson', 'QC Analyst I', 'Quality Control Laboratory', 'Austin Plant', '+1 512 555 0205', 'dokafor@austinpharma.com', '100205', 'UserMailbox', TRUE, '2026-09-29 01:00:00+00'),
('3277d5dd-6d8d-fd59-45cb-7a2889ae7165', 'dshaw.ext@austinpharma.com', 'Derek', 'Shaw', 'Derek Shaw', 'Validation Consultant', 'Engineering and Maintenance', 'Austin Plant', '+1 737 555 0415', 'npetrov@austinpharma.com', 'C00015', 'UserMailbox', FALSE, '2026-06-01 07:15:00+00'),
('477412af-d066-c918-d5b8-24c9fb270343', 'lchen.ext@austinpharma.com', 'Laura', 'Chen', 'Laura Chen', 'GMP Audit Consultant', 'Quality Assurance', 'Austin Plant', NULL, 'mwhitfield@austinpharma.com', 'C00021', 'UserMailbox', FALSE, '2026-09-14 07:15:00+00')
ON CONFLICT DO NOTHING;

-- Subscription inbound: tables and columns written by the coco_subscriptions_austin_systems DAG from the
-- digital products this system subscribes to (see coco-subscription-loads/austin_systems/microsoft_365).
-- No extract reads them.

ALTER TABLE microsoft_365.exo_recipient ADD COLUMN IF NOT EXISTS customattribute2 varchar(40);
ALTER TABLE microsoft_365.exo_recipient ADD COLUMN IF NOT EXISTS customattribute3 varchar(20);
ALTER TABLE microsoft_365.exo_recipient ADD COLUMN IF NOT EXISTS customattribute4 varchar(20);
COMMENT ON COLUMN microsoft_365.exo_recipient.customattribute2 IS 'customAttribute2: Workday job profile (role code) from Worker Master Data.';
COMMENT ON COLUMN microsoft_365.exo_recipient.customattribute3 IS 'customAttribute3: Workday cost centre from Worker Master Data.';
COMMENT ON COLUMN microsoft_365.exo_recipient.customattribute4 IS 'customAttribute4: Workday worker status from Worker Master Data.';

GRANT USAGE ON SCHEMA microsoft_365 TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA microsoft_365 TO egeria_user, airflow_user;
