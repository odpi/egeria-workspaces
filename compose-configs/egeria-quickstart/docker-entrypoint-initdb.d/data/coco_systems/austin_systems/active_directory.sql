-- system-qualified-name: SoftwareServer::AUS-SYS-031::SN-AD-AU-20170901
-- Microsoft Active Directory - Austin.  The on-premises domain austinpharma.local: user accounts and security groups
-- for the Austin plant systems.  Its tables feed Access Entitlements (on-premises accounts and group entitlements) and
-- Corporate Directory Entries (synchronised staff).
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS active_directory;
COMMENT ON SCHEMA active_directory IS 'Microsoft Active Directory (Austin): user, group and linked-value group membership objects as landed by the nightly LDAP export.';

CREATE TABLE IF NOT EXISTS active_directory.ad_user (
  objectguid                 uuid NOT NULL,
  samaccountname             varchar(20) NOT NULL,
  userprincipalname          varchar(120) NOT NULL,
  givenname                  varchar(80),
  sn                         varchar(80),
  displayname                varchar(160),
  title                      varchar(120),
  department                 varchar(120),
  company                    varchar(120),
  physicaldeliveryofficename varchar(120),
  telephonenumber            varchar(30),
  employeeid                 varchar(20),
  manager                    varchar(255),
  distinguishedname          varchar(255) NOT NULL,
  useraccountcontrol         integer NOT NULL,
  whencreated                timestamptz NOT NULL,
  whenchanged                timestamptz NOT NULL,
  accountexpires             bigint NOT NULL,
  extensionattribute10       varchar(60),
  CONSTRAINT ad_user_pk PRIMARY KEY (objectguid)
);
COMMENT ON TABLE active_directory.ad_user IS 'user objects (accountexpires is a Windows FILETIME, 9223372036854775807 = never; extensionAttribute10 = last Workday event applied).';

INSERT INTO active_directory.ad_user (objectguid, samaccountname, userprincipalname, givenname, sn, displayname, title, department, company, physicaldeliveryofficename, telephonenumber, employeeid, manager, distinguishedname, useraccountcontrol, whencreated, whenchanged, accountexpires, extensionattribute10) VALUES
('16d1f1a5-cc64-812a-6070-705c18466c77', 'rhernandez', 'rhernandez@austinpharma.com', 'Rebecca', 'Hernandez', 'Rebecca Hernandez', 'Site Head, Austin', 'Site Leadership', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0101', '100101', NULL, 'CN=Rebecca Hernandez,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2014-02-28 16:20:00+00', '2014-03-03 06:30:00+00', 9223372036854775807, 'EVT-2014-00107'),
('b01d9dbe-4b11-d15c-f8d0-d66597a59f47', 'mwhitfield', 'mwhitfield@austinpharma.com', 'Marcus', 'Whitfield', 'Marcus Whitfield', 'Director of Quality Assurance', 'Quality Assurance', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0112', '100112', 'CN=Rebecca Hernandez,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Marcus Whitfield,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2016-06-10 16:20:00+00', '2016-06-13 06:30:00+00', 9223372036854775807, 'EVT-2016-00114'),
('a759a874-0f5a-25cb-19a8-ce2bf334d1de', 'praman', 'praman@austinpharma.com', 'Priya', 'Raman', 'Priya Raman', 'QA Batch Disposition Specialist', 'Quality Assurance', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0118', '100118', 'CN=Marcus Whitfield,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Priya Raman,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2019-01-04 16:20:00+00', '2019-01-07 06:30:00+00', 9223372036854775807, 'EVT-2019-00149'),
('24395f3f-1c69-a1c2-f4e1-4b2718cb3515', 'bfoster', 'bfoster@austinpharma.com', 'Brian', 'Foster', 'Brian Foster', 'Production Operator II', 'Manufacturing', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0122', '100122', 'CN=Jason Morales,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Brian Foster,OU=Leavers,OU=Austin,DC=austinpharma,DC=local', 514, '2021-04-16 16:20:00+00', '2026-08-29 03:10:00+00', 9223372036854775807, 'EVT-2026-00517'),
('f42ce98f-ef5a-e68a-a68d-06da9935fb87', 'dokafor', 'dokafor@austinpharma.com', 'Daniel', 'Okafor', 'Daniel Okafor', 'QC Laboratory Manager', 'Quality Control Laboratory', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0124', '100124', 'CN=Marcus Whitfield,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Daniel Okafor,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2017-09-08 16:20:00+00', '2017-09-11 06:30:00+00', 9223372036854775807, 'EVT-2017-00128'),
('a38060f4-07ac-8e42-83ea-8591b9a6e716', 'cruiz', 'cruiz@austinpharma.com', 'Carla', 'Ruiz', 'Carla Ruiz', 'QC Analyst II', 'Quality Control Laboratory', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0128', '100128', 'CN=Daniel Okafor,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Carla Ruiz,OU=Leavers,OU=Austin,DC=austinpharma,DC=local', 514, '2020-01-31 16:20:00+00', '2026-05-29 22:15:00+00', 134245727990000000, 'EVT-2026-00391'),
('5658ad8e-6349-f371-c589-a915a8f61a39', 'sdelgado', 'sdelgado@austinpharma.com', 'Sofia', 'Delgado', 'Sofia Delgado', 'QC Analyst II', 'Quality Control Laboratory', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0131', '100131', 'CN=Daniel Okafor,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Sofia Delgado,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2020-08-21 16:20:00+00', '2020-08-24 06:30:00+00', 9223372036854775807, 'EVT-2020-00191'),
('4151324f-341b-0db5-e47f-5483f9456737', 'ktran', 'ktran@austinpharma.com', 'Kevin', 'Tran', 'Kevin Tran', 'QC Chromatography Analyst', 'Quality Control Laboratory', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0137', '100137', 'CN=Daniel Okafor,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Kevin Tran,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2026-02-06 16:20:00+00', '2026-02-09 06:30:00+00', 9223372036854775807, 'EVT-2026-00247'),
('c759c294-eca7-3c8c-c6af-0a944ff02fe0', 'jmorales', 'jmorales@austinpharma.com', 'Jason', 'Morales', 'Jason Morales', 'Manufacturing Supervisor', 'Manufacturing', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0142', '100142', 'CN=Rebecca Hernandez,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Jason Morales,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2018-05-11 16:20:00+00', '2018-05-14 06:30:00+00', 9223372036854775807, 'EVT-2018-00135'),
('32475375-6a64-5759-cb39-810c4cc7c051', 'abrooks', 'abrooks@austinpharma.com', 'Aaliyah', 'Brooks', 'Aaliyah Brooks', 'Production Operator III', 'Manufacturing', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0149', '100149', 'CN=Jason Morales,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Aaliyah Brooks,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2019-10-04 16:20:00+00', '2019-10-07 06:30:00+00', 9223372036854775807, 'EVT-2019-00170'),
('605aefa9-8a21-11d1-c1cf-77d15d0442c8', 'tnguyen', 'tnguyen@austinpharma.com', 'Tyler', 'Nguyen', 'Tyler Nguyen', 'Production Operator III', 'Manufacturing', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0153', '100153', 'CN=Jason Morales,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Tyler Nguyen,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2022-03-18 16:20:00+00', '2026-07-01 06:30:00+00', 9223372036854775807, 'EVT-2026-00455'),
('ed2dd562-b34f-f9a8-db28-970212954ff8', 'glindqvist', 'glindqvist@austinpharma.com', 'Grace', 'Lindqvist', 'Grace Lindqvist', 'Cell Therapy Manufacturing Specialist', 'Cell Therapy Manufacturing', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0158', '100158', 'CN=Jason Morales,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Grace Lindqvist,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2023-01-06 16:20:00+00', '2023-01-09 06:30:00+00', 9223372036854775807, 'EVT-2023-00240'),
('f419ae8e-3cbb-ed0b-1b28-7b6950bf661f', 'ohaddad', 'ohaddad@austinpharma.com', 'Omar', 'Haddad', 'Omar Haddad', 'Warehouse Lead', 'Warehouse and Logistics', 'Austin Pharmaceuticals, Inc.', 'Austin Distribution Center', '+1 512 555 0162', '100162', 'CN=Rebecca Hernandez,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Omar Haddad,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2018-11-02 16:20:00+00', '2018-11-05 06:30:00+00', 9223372036854775807, 'EVT-2018-00142'),
('fd85c744-b21d-93ba-e806-b56afb5d1413', 'hkowalski', 'hkowalski@austinpharma.com', 'Hannah', 'Kowalski', 'Hannah Kowalski', 'Site Controller', 'Finance', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0167', '100167', 'CN=Rebecca Hernandez,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Hannah Kowalski,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2017-03-31 16:20:00+00', '2017-04-03 06:30:00+00', 9223372036854775807, 'EVT-2017-00121'),
('2579483f-c7ac-62ee-a82c-0fc26762524d', 'lcarranza', 'lcarranza@austinpharma.com', 'Luis', 'Carranza', 'Luis Carranza', 'Senior Accountant', 'Finance', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0171', '100171', 'CN=Hannah Kowalski,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Luis Carranza,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2020-07-10 16:20:00+00', '2020-07-13 06:30:00+00', 9223372036854775807, 'EVT-2020-00184'),
('500d36fd-0029-b103-cb08-a635b9026061', 'moneill', 'moneill@austinpharma.com', 'Megan', 'O''Neill', 'Megan O''Neill', 'Accounts Payable Specialist', 'Finance', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0176', '100176', 'CN=Hannah Kowalski,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Megan O''Neill,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2021-09-17 16:20:00+00', '2021-09-20 06:30:00+00', 9223372036854775807, 'EVT-2021-00219'),
('ff640425-c327-2a60-6294-e4c94c7805ee', 'epark', 'epark@austinpharma.com', 'Ethan', 'Park', 'Ethan Park', 'Procurement Manager', 'Procurement', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0180', '100180', 'CN=Hannah Kowalski,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Ethan Park,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2019-05-03 16:20:00+00', '2019-05-06 06:30:00+00', 9223372036854775807, 'EVT-2019-00156'),
('02e90089-e628-7679-0c5b-3834b5102c4d', 'cbennett', 'cbennett@austinpharma.com', 'Chloe', 'Bennett', 'Chloe Bennett', 'HR Business Partner', 'Human Resources', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0184', '100184', 'CN=Rebecca Hernandez,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Chloe Bennett,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2020-10-30 16:20:00+00', '2020-11-02 06:30:00+00', 9223372036854775807, 'EVT-2020-00198'),
('17d1ee5b-b81c-4181-3aa0-c0921f41f3f4', 'sadeyemi', 'sadeyemi@austinpharma.com', 'Samuel', 'Adeyemi', 'Samuel Adeyemi', 'Shipping and Dangerous Goods Coordinator', 'Warehouse and Logistics', 'Austin Pharmaceuticals, Inc.', 'Austin Distribution Center', '+1 512 555 0189', '100189', 'CN=Omar Haddad,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Samuel Adeyemi,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2021-02-12 16:20:00+00', '2021-02-15 06:30:00+00', 9223372036854775807, 'EVT-2021-00205'),
('40635e2b-9b2d-d76e-7bb3-71f12962cd35', 'npetrov', 'npetrov@austinpharma.com', 'Nina', 'Petrov', 'Nina Petrov', 'Maintenance and Calibration Engineer', 'Engineering and Maintenance', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0193', '100193', 'CN=Rebecca Hernandez,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Nina Petrov,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2019-08-16 16:20:00+00', '2019-08-19 06:30:00+00', 9223372036854775807, 'EVT-2019-00163'),
('ff32abd5-7bf5-8cd3-cebb-17e05e939a19', 'rcastillo', 'rcastillo@austinpharma.com', 'Robert', 'Castillo', 'Robert Castillo', 'Customer Quality Specialist', 'Customer Quality and Safety', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0197', '100197', 'CN=Marcus Whitfield,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Robert Castillo,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2022-06-03 16:20:00+00', '2022-06-06 06:30:00+00', 9223372036854775807, 'EVT-2022-00233'),
('1c169b42-291c-a872-9c88-50180d6c9933', 'imoreno', 'imoreno@austinpharma.com', 'Isabel', 'Moreno', 'Isabel Moreno', 'Drug Safety Associate', 'Customer Quality and Safety', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0201', '100201', 'CN=Marcus Whitfield,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Isabel Moreno,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2026-02-27 16:20:00+00', '2026-03-02 06:30:00+00', 9223372036854775807, 'EVT-2026-00254'),
('c425819a-ef63-47ae-3cfb-747a69777659', 'mjohnson', 'mjohnson@austinpharma.com', 'Mia', 'Johnson', 'Mia Johnson', 'QC Analyst I', 'Quality Control Laboratory', 'Austin Pharmaceuticals, Inc.', 'Austin Plant', '+1 512 555 0205', '100205', 'CN=Daniel Okafor,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 'CN=Mia Johnson,OU=Staff,OU=Austin,DC=austinpharma,DC=local', 512, '2026-09-05 16:20:00+00', '2026-09-08 06:30:00+00', 9223372036854775807, 'EVT-2026-00268')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS active_directory.ad_group (
  objectguid          uuid NOT NULL,
  samaccountname      varchar(64) NOT NULL,
  description         varchar(255),
  distinguishedname   varchar(255) NOT NULL,
  grouptype           integer NOT NULL,
  extensionattribute1 varchar(60),
  whencreated         timestamptz NOT NULL,
  CONSTRAINT ad_group_pk PRIMARY KEY (objectguid)
);
COMMENT ON TABLE active_directory.ad_group IS 'Security groups used to grant application roles (extensionAttribute1 = DATA-OWNER marks catalogue data owner groups).';

INSERT INTO active_directory.ad_group (objectguid, samaccountname, description, distinguishedname, grouptype, extensionattribute1, whencreated) VALUES
('cfe318ee-426f-91a6-6bf7-a2f89b9b1d49', 'GG-AUS-MES-Operators', 'Opcenter MES operator role', 'CN=GG-AUS-MES-Operators,OU=Groups,OU=Austin,DC=austinpharma,DC=local', -2147483646, NULL, '2019-03-18 10:00:00+00'),
('1831aca2-31ed-29d1-a53b-989a10291ca9', 'GG-AUS-MES-Supervisors', 'Opcenter MES supervisor role, step sign-off', 'CN=GG-AUS-MES-Supervisors,OU=Groups,OU=Austin,DC=austinpharma,DC=local', -2147483646, NULL, '2019-03-18 10:00:00+00'),
('7d30a99c-c6fd-c6cc-d1b7-3e629e303402', 'GG-AUS-LIMS-Analysts', 'LabWare LIMS analyst role, result entry', 'CN=GG-AUS-LIMS-Analysts,OU=Groups,OU=Austin,DC=austinpharma,DC=local', -2147483646, NULL, '2019-03-18 10:00:00+00'),
('8134336b-ff29-9b22-e945-5ef6da524579', 'GG-AUS-LIMS-Reviewers', 'LabWare LIMS reviewer role, result approval and CoA sign-off', 'CN=GG-AUS-LIMS-Reviewers,OU=Groups,OU=Austin,DC=austinpharma,DC=local', -2147483646, NULL, '2019-03-18 10:00:00+00'),
('804d200b-41a2-ea41-7a5f-0ccffd8724a6', 'GG-AUS-SAP-FI-GL', 'SAP S/4HANA general ledger posting and parking', 'CN=GG-AUS-SAP-FI-GL,OU=Groups,OU=Austin,DC=austinpharma,DC=local', -2147483646, NULL, '2019-03-18 10:00:00+00'),
('65b7944f-d7fc-76e6-5e4a-26b14d6f2f07', 'GG-AUS-SAP-FI-AP', 'SAP S/4HANA accounts payable processing', 'CN=GG-AUS-SAP-FI-AP,OU=Groups,OU=Austin,DC=austinpharma,DC=local', -2147483646, NULL, '2019-03-18 10:00:00+00'),
('8364ee71-206c-aa16-d026-4c33dc611ec8', 'GG-AUS-WMS-Users', 'Manhattan WMS RF and desktop users', 'CN=GG-AUS-WMS-Users,OU=Groups,OU=Austin,DC=austinpharma,DC=local', -2147483646, NULL, '2019-03-18 10:00:00+00'),
('1c75dd9e-764c-f331-e7a3-90b96b1b72ec', 'GG-AUS-SCADA-Engineers', 'FactoryTalk engineering workstation access', 'CN=GG-AUS-SCADA-Engineers,OU=Groups,OU=Austin,DC=austinpharma,DC=local', -2147483646, NULL, '2019-03-18 10:00:00+00'),
('b3c55b0d-3080-e111-500d-e8a96cbfb6af', 'DO-AUS-BatchRecords', 'Data owner: batch records and release data', 'CN=DO-AUS-BatchRecords,OU=Groups,OU=Austin,DC=austinpharma,DC=local', -2147483646, 'DATA-OWNER', '2019-03-18 10:00:00+00'),
('3adfc764-8012-3b50-afdf-0ea037ba9493', 'DO-AUS-LabData', 'Data owner: laboratory results', 'CN=DO-AUS-LabData,OU=Groups,OU=Austin,DC=austinpharma,DC=local', -2147483646, 'DATA-OWNER', '2019-03-18 10:00:00+00'),
('9dac7b36-279e-851f-3dfd-5069d760ecdc', 'DO-AUS-FinanceLedger', 'Data owner: general ledger', 'CN=DO-AUS-FinanceLedger,OU=Groups,OU=Austin,DC=austinpharma,DC=local', -2147483646, 'DATA-OWNER', '2019-03-18 10:00:00+00')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS active_directory.ad_group_member (
  group_objectguid        uuid NOT NULL,
  member_objectguid       uuid NOT NULL,
  originating_create_time timestamptz NOT NULL,
  originating_delete_time timestamptz,
  CONSTRAINT ad_group_member_pk PRIMARY KEY (group_objectguid, member_objectguid)
);
COMMENT ON TABLE active_directory.ad_group_member IS 'Linked-value replication metadata for the member attribute: when each membership was added and, for absent values, removed.';

INSERT INTO active_directory.ad_group_member (group_objectguid, member_objectguid, originating_create_time, originating_delete_time) VALUES
('cfe318ee-426f-91a6-6bf7-a2f89b9b1d49', '24395f3f-1c69-a1c2-f4e1-4b2718cb3515', '2021-04-20 14:00:00+00', '2026-08-29 03:10:00+00'),
('cfe318ee-426f-91a6-6bf7-a2f89b9b1d49', '32475375-6a64-5759-cb39-810c4cc7c051', '2019-10-08 14:00:00+00', NULL),
('cfe318ee-426f-91a6-6bf7-a2f89b9b1d49', '605aefa9-8a21-11d1-c1cf-77d15d0442c8', '2022-03-22 14:00:00+00', NULL),
('cfe318ee-426f-91a6-6bf7-a2f89b9b1d49', 'ed2dd562-b34f-f9a8-db28-970212954ff8', '2023-01-10 14:00:00+00', NULL),
('1831aca2-31ed-29d1-a53b-989a10291ca9', 'c759c294-eca7-3c8c-c6af-0a944ff02fe0', '2018-05-15 14:00:00+00', NULL),
('7d30a99c-c6fd-c6cc-d1b7-3e629e303402', 'a38060f4-07ac-8e42-83ea-8591b9a6e716', '2020-02-04 14:00:00+00', '2026-05-29 22:15:00+00'),
('7d30a99c-c6fd-c6cc-d1b7-3e629e303402', '5658ad8e-6349-f371-c589-a915a8f61a39', '2020-08-25 14:00:00+00', NULL),
('7d30a99c-c6fd-c6cc-d1b7-3e629e303402', '4151324f-341b-0db5-e47f-5483f9456737', '2026-02-10 14:00:00+00', NULL),
('7d30a99c-c6fd-c6cc-d1b7-3e629e303402', 'c425819a-ef63-47ae-3cfb-747a69777659', '2026-09-09 14:00:00+00', NULL),
('8134336b-ff29-9b22-e945-5ef6da524579', 'f42ce98f-ef5a-e68a-a68d-06da9935fb87', '2017-09-12 14:00:00+00', NULL),
('804d200b-41a2-ea41-7a5f-0ccffd8724a6', 'fd85c744-b21d-93ba-e806-b56afb5d1413', '2017-04-04 14:00:00+00', NULL),
('804d200b-41a2-ea41-7a5f-0ccffd8724a6', '2579483f-c7ac-62ee-a82c-0fc26762524d', '2020-07-14 14:00:00+00', NULL),
('65b7944f-d7fc-76e6-5e4a-26b14d6f2f07', '500d36fd-0029-b103-cb08-a635b9026061', '2021-09-21 14:00:00+00', NULL),
('8364ee71-206c-aa16-d026-4c33dc611ec8', 'f419ae8e-3cbb-ed0b-1b28-7b6950bf661f', '2018-11-06 14:00:00+00', NULL),
('8364ee71-206c-aa16-d026-4c33dc611ec8', '17d1ee5b-b81c-4181-3aa0-c0921f41f3f4', '2021-02-16 14:00:00+00', NULL),
('1c75dd9e-764c-f331-e7a3-90b96b1b72ec', '40635e2b-9b2d-d76e-7bb3-71f12962cd35', '2019-08-20 14:00:00+00', NULL),
('b3c55b0d-3080-e111-500d-e8a96cbfb6af', 'b01d9dbe-4b11-d15c-f8d0-d66597a59f47', '2016-06-14 14:00:00+00', NULL),
('3adfc764-8012-3b50-afdf-0ea037ba9493', 'f42ce98f-ef5a-e68a-a68d-06da9935fb87', '2017-09-12 14:00:00+00', NULL),
('9dac7b36-279e-851f-3dfd-5069d760ecdc', 'fd85c744-b21d-93ba-e806-b56afb5d1413', '2017-04-04 14:00:00+00', NULL)
ON CONFLICT DO NOTHING;

-- Subscription inbound: tables and columns written by the coco_subscriptions_austin_systems DAG from the
-- digital products this system subscribes to (see coco-subscription-loads/austin_systems/active_directory).
-- No extract reads them.

ALTER TABLE active_directory.ad_user ADD COLUMN IF NOT EXISTS employeetype varchar(40);
ALTER TABLE active_directory.ad_user ADD COLUMN IF NOT EXISTS departmentnumber varchar(20);
ALTER TABLE active_directory.ad_user ADD COLUMN IF NOT EXISTS extensionattribute2 varchar(60);
ALTER TABLE active_directory.ad_user ADD COLUMN IF NOT EXISTS extensionattribute3 varchar(60);
ALTER TABLE active_directory.ad_user ADD COLUMN IF NOT EXISTS extensionattribute4 varchar(60);
COMMENT ON COLUMN active_directory.ad_user.employeetype IS 'employeeType from Worker Master Data (Employee/Contractor).';
COMMENT ON COLUMN active_directory.ad_user.departmentnumber IS 'departmentNumber: Workday cost centre from Worker Master Data.';
COMMENT ON COLUMN active_directory.ad_user.extensionattribute2 IS 'extensionAttribute2: Workday job profile (role code) from Worker Master Data.';
COMMENT ON COLUMN active_directory.ad_user.extensionattribute3 IS 'extensionAttribute3: Workday worker status (active / on leave / left) from Worker Master Data.';
COMMENT ON COLUMN active_directory.ad_user.extensionattribute4 IS 'extensionAttribute4: Workday leave date (YYYY-MM-DD) from Worker Master Data.';

GRANT USAGE ON SCHEMA active_directory TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA active_directory TO egeria_user, airflow_user;
