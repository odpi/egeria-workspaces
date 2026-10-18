-- system-qualified-name: SoftwareServer::AUS-SYS-032::SN-AAD-AU-20200601
-- Microsoft Entra ID - Austin.  The Austin cloud identity tenant: users provisioned from Workday (synchronised and
-- cloud-only) and their application role assignments for SaaS applications.  Its tables feed Access Entitlements.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS entra_id;
COMMENT ON SCHEMA entra_id IS 'Microsoft Entra ID (Austin tenant): users, service principal app roles and app role assignments as landed from Microsoft Graph.';

CREATE TABLE IF NOT EXISTS entra_id.users (
  id                         uuid NOT NULL,
  userprincipalname          varchar(120) NOT NULL,
  displayname                varchar(160),
  givenname                  varchar(80),
  surname                    varchar(80),
  jobtitle                   varchar(120),
  department                 varchar(120),
  officelocation             varchar(120),
  employeeid                 varchar(20),
  accountenabled             boolean NOT NULL,
  createddatetime            timestamptz NOT NULL,
  employeehiredate           date,
  employeeleavedatetime      timestamptz,
  onpremisessyncenabled      boolean NOT NULL,
  onpremisessamaccountname   varchar(20),
  extension_workday_event_id varchar(40),
  signin_blocked_datetime    timestamptz,
  deleteddatetime            timestamptz,
  CONSTRAINT users_pk PRIMARY KEY (id)
);
COMMENT ON TABLE entra_id.users IS 'Graph user objects including soft-deleted users (deleteddatetime) and the Workday event last applied.';

INSERT INTO entra_id.users (id, userprincipalname, displayname, givenname, surname, jobtitle, department, officelocation, employeeid, accountenabled, createddatetime, employeehiredate, employeeleavedatetime, onpremisessyncenabled, onpremisessamaccountname, extension_workday_event_id, signin_blocked_datetime, deleteddatetime) VALUES
('d6e5262b-650f-9eba-fd15-2deb507efd40', 'rhernandez@austinpharma.com', 'Rebecca Hernandez', 'Rebecca', 'Hernandez', 'Site Head, Austin', 'Site Leadership', 'Austin Plant', '100101', TRUE, '2020-05-30 11:45:00+00', '2014-03-03', NULL, TRUE, 'rhernandez', 'EVT-2014-00107', NULL, NULL),
('1abd5a54-dcc6-f3b0-70b8-b6c8d05540f4', 'mwhitfield@austinpharma.com', 'Marcus Whitfield', 'Marcus', 'Whitfield', 'Director of Quality Assurance', 'Quality Assurance', 'Austin Plant', '100112', TRUE, '2020-05-30 11:45:00+00', '2016-06-13', NULL, TRUE, 'mwhitfield', 'EVT-2016-00114', NULL, NULL),
('94dfa23b-657d-2cd4-941d-3b5508e57bc3', 'praman@austinpharma.com', 'Priya Raman', 'Priya', 'Raman', 'QA Batch Disposition Specialist', 'Quality Assurance', 'Austin Plant', '100118', TRUE, '2020-05-30 11:45:00+00', '2019-01-07', NULL, TRUE, 'praman', 'EVT-2019-00149', NULL, NULL),
('203885eb-3aa6-35e6-74cb-76cd5c10478b', 'bfoster@austinpharma.com', 'Brian Foster', 'Brian', 'Foster', 'Production Operator II', 'Manufacturing', 'Austin Plant', '100122', FALSE, '2021-04-17 11:45:00+00', '2021-04-19', '2026-08-14 23:59:59+00', TRUE, 'bfoster', 'EVT-2026-00517', '2026-08-28 09:12:00+00', NULL),
('75786fc1-95c4-f31e-c7b5-1692a7238d45', 'dokafor@austinpharma.com', 'Daniel Okafor', 'Daniel', 'Okafor', 'QC Laboratory Manager', 'Quality Control Laboratory', 'Austin Plant', '100124', TRUE, '2020-05-30 11:45:00+00', '2017-09-11', NULL, TRUE, 'dokafor', 'EVT-2017-00128', NULL, NULL),
('2b7a9348-ed4d-fb84-5e19-407b912a830c', 'cruiz@austinpharma.com', 'Carla Ruiz', 'Carla', 'Ruiz', 'QC Analyst II', 'Quality Control Laboratory', 'Austin Plant', '100128', FALSE, '2020-05-30 11:45:00+00', '2020-02-03', '2026-05-29 23:59:59+00', TRUE, 'cruiz', 'EVT-2026-00391', NULL, '2026-05-30 02:00:00+00'),
('9a24783f-cd4f-e7e7-e2a3-d6dedab00fc0', 'sdelgado@austinpharma.com', 'Sofia Delgado', 'Sofia', 'Delgado', 'QC Analyst II', 'Quality Control Laboratory', 'Austin Plant', '100131', TRUE, '2020-08-22 11:45:00+00', '2020-08-24', NULL, TRUE, 'sdelgado', 'EVT-2020-00191', NULL, NULL),
('fbe59352-60d4-495d-6ac3-b2e2fcf6d062', 'ktran@austinpharma.com', 'Kevin Tran', 'Kevin', 'Tran', 'QC Chromatography Analyst', 'Quality Control Laboratory', 'Austin Plant', '100137', TRUE, '2026-02-07 11:45:00+00', '2026-02-09', NULL, TRUE, 'ktran', 'EVT-2026-00247', NULL, NULL),
('f73c896d-87fd-224b-2c8f-882c91a051c3', 'jmorales@austinpharma.com', 'Jason Morales', 'Jason', 'Morales', 'Manufacturing Supervisor', 'Manufacturing', 'Austin Plant', '100142', TRUE, '2020-05-30 11:45:00+00', '2018-05-14', NULL, TRUE, 'jmorales', 'EVT-2018-00135', NULL, NULL),
('f8ccb52c-ef7e-dc50-c76c-338f966b0d58', 'abrooks@austinpharma.com', 'Aaliyah Brooks', 'Aaliyah', 'Brooks', 'Production Operator III', 'Manufacturing', 'Austin Plant', '100149', TRUE, '2020-05-30 11:45:00+00', '2019-10-07', NULL, TRUE, 'abrooks', 'EVT-2019-00170', NULL, NULL),
('cde4585a-361d-ecc9-fa3f-e50974283c23', 'tnguyen@austinpharma.com', 'Tyler Nguyen', 'Tyler', 'Nguyen', 'Production Operator III', 'Manufacturing', 'Austin Plant', '100153', TRUE, '2022-03-19 11:45:00+00', '2022-03-21', NULL, TRUE, 'tnguyen', 'EVT-2026-00455', NULL, NULL),
('47b8e373-5b19-68a0-28c9-876b9608215c', 'glindqvist@austinpharma.com', 'Grace Lindqvist', 'Grace', 'Lindqvist', 'Cell Therapy Manufacturing Specialist', 'Cell Therapy Manufacturing', 'Austin Plant', '100158', TRUE, '2023-01-07 11:45:00+00', '2023-01-09', NULL, TRUE, 'glindqvist', 'EVT-2023-00240', NULL, NULL),
('151627eb-7752-7bff-969e-c34798928b4c', 'ohaddad@austinpharma.com', 'Omar Haddad', 'Omar', 'Haddad', 'Warehouse Lead', 'Warehouse and Logistics', 'Austin Distribution Center', '100162', TRUE, '2020-05-30 11:45:00+00', '2018-11-05', NULL, TRUE, 'ohaddad', 'EVT-2018-00142', NULL, NULL),
('1332f649-d9b6-9e10-d443-eb453cf8736c', 'hkowalski@austinpharma.com', 'Hannah Kowalski', 'Hannah', 'Kowalski', 'Site Controller', 'Finance', 'Austin Plant', '100167', TRUE, '2020-05-30 11:45:00+00', '2017-04-03', NULL, TRUE, 'hkowalski', 'EVT-2017-00121', NULL, NULL),
('871d5806-698c-72bd-d3cd-902067780246', 'lcarranza@austinpharma.com', 'Luis Carranza', 'Luis', 'Carranza', 'Senior Accountant', 'Finance', 'Austin Plant', '100171', TRUE, '2020-07-11 11:45:00+00', '2020-07-13', NULL, TRUE, 'lcarranza', 'EVT-2020-00184', NULL, NULL),
('a1c22794-5f7d-bcc0-d241-84b6e8890290', 'moneill@austinpharma.com', 'Megan O''Neill', 'Megan', 'O''Neill', 'Accounts Payable Specialist', 'Finance', 'Austin Plant', '100176', TRUE, '2021-09-18 11:45:00+00', '2021-09-20', NULL, TRUE, 'moneill', 'EVT-2021-00219', NULL, NULL),
('8bc771ec-a6af-6281-c616-19a61a8b65ae', 'epark@austinpharma.com', 'Ethan Park', 'Ethan', 'Park', 'Procurement Manager', 'Procurement', 'Austin Plant', '100180', TRUE, '2020-05-30 11:45:00+00', '2019-05-06', NULL, TRUE, 'epark', 'EVT-2019-00156', NULL, NULL),
('c72b2c9c-9cec-996c-14c0-e5579e9b3bd3', 'cbennett@austinpharma.com', 'Chloe Bennett', 'Chloe', 'Bennett', 'HR Business Partner', 'Human Resources', 'Austin Plant', '100184', TRUE, '2020-10-31 11:45:00+00', '2020-11-02', NULL, TRUE, 'cbennett', 'EVT-2020-00198', NULL, NULL),
('386e55eb-57e0-f7ab-50a2-a1f0c6e4dc97', 'sadeyemi@austinpharma.com', 'Samuel Adeyemi', 'Samuel', 'Adeyemi', 'Shipping and Dangerous Goods Coordinator', 'Warehouse and Logistics', 'Austin Distribution Center', '100189', TRUE, '2021-02-13 11:45:00+00', '2021-02-15', NULL, TRUE, 'sadeyemi', 'EVT-2021-00205', NULL, NULL),
('dd1b1f2a-d1a1-2d95-8c10-dc93b1e805c7', 'npetrov@austinpharma.com', 'Nina Petrov', 'Nina', 'Petrov', 'Maintenance and Calibration Engineer', 'Engineering and Maintenance', 'Austin Plant', '100193', TRUE, '2020-05-30 11:45:00+00', '2019-08-19', NULL, TRUE, 'npetrov', 'EVT-2019-00163', NULL, NULL),
('38162db3-4a5c-5980-c164-3e99b2f29878', 'rcastillo@austinpharma.com', 'Robert Castillo', 'Robert', 'Castillo', 'Customer Quality Specialist', 'Customer Quality and Safety', 'Austin Plant', '100197', TRUE, '2022-06-04 11:45:00+00', '2022-06-06', NULL, TRUE, 'rcastillo', 'EVT-2022-00233', NULL, NULL),
('503afe8a-75b5-567f-57b6-2323c466ce89', 'imoreno@austinpharma.com', 'Isabel Moreno', 'Isabel', 'Moreno', 'Drug Safety Associate', 'Customer Quality and Safety', 'Austin Plant', '100201', TRUE, '2026-02-28 11:45:00+00', '2026-03-02', NULL, TRUE, 'imoreno', 'EVT-2026-00254', NULL, NULL),
('194e16db-ab1e-4cc8-61be-588f2ea39575', 'mjohnson@austinpharma.com', 'Mia Johnson', 'Mia', 'Johnson', 'QC Analyst I', 'Quality Control Laboratory', 'Austin Plant', '100205', TRUE, '2026-09-06 11:45:00+00', '2026-09-08', NULL, TRUE, 'mjohnson', 'EVT-2026-00268', NULL, NULL),
('3277d5dd-6d8d-fd59-45cb-7a2889ae7165', 'dshaw.ext@austinpharma.com', 'Derek Shaw', 'Derek', 'Shaw', 'Validation Consultant', 'Engineering and Maintenance', 'Austin Plant', 'C00015', TRUE, '2026-05-30 11:45:00+00', '2026-06-01', NULL, FALSE, NULL, 'EVT-2026-00261', NULL, NULL),
('477412af-d066-c918-d5b8-24c9fb270343', 'lchen.ext@austinpharma.com', 'Laura Chen', 'Laura', 'Chen', 'GMP Audit Consultant', 'Quality Assurance', 'Austin Plant', 'C00021', TRUE, '2026-09-12 11:45:00+00', '2026-09-14', NULL, FALSE, NULL, 'EVT-2026-00275', NULL, NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS entra_id.service_principal_app_role (
  resource_id           uuid NOT NULL,
  app_role_id           uuid NOT NULL,
  resource_display_name varchar(120) NOT NULL,
  value                 varchar(60) NOT NULL,
  description           text,
  is_data_owner_role    boolean NOT NULL,
  CONSTRAINT service_principal_app_role_pk PRIMARY KEY (resource_id, app_role_id)
);
COMMENT ON TABLE entra_id.service_principal_app_role IS 'App roles published by each enterprise application (service principal).';

INSERT INTO entra_id.service_principal_app_role (resource_id, app_role_id, resource_display_name, value, description, is_data_owner_role) VALUES
('ba276640-ad18-360e-14fa-47768d8ebb31', 'eba6db81-48ce-88f2-55b5-66b6de56a5b2', 'Veeva Vault QMS', 'QA.Approver', 'Approve quality events, investigations and batch dispositions', FALSE),
('ba276640-ad18-360e-14fa-47768d8ebb31', '0722af68-8f1a-ffe1-57af-0af1cd524f09', 'Veeva Vault QMS', 'Quality.Contributor', 'Raise and update quality events and CAPA actions', FALSE),
('ba276640-ad18-360e-14fa-47768d8ebb31', 'f524363b-ec26-03f5-bd22-e0f2f49ba977', 'Veeva Vault QMS', 'Auditor.ReadOnly', 'Read-only access to quality records for audit', FALSE),
('add489b8-8fc2-81d3-3c2e-10a808feebc0', '8af3c17c-792a-9ce0-97b7-6cd05b90d40a', 'Veeva Vault EBR', 'Batch.Reviewer', 'Review batch records and certify release', FALSE),
('add489b8-8fc2-81d3-3c2e-10a808feebc0', '65ab9d3d-9bc1-72fe-dd27-a2bc944800c4', 'Veeva Vault EBR', 'Batch.Executor', 'Complete manual batch record sections', FALSE),
('176ec1b4-1984-044c-7a8f-21443aa95749', '15bc224c-4c6c-e110-9851-494cd667cf65', 'ServiceNow CSM', 'Complaint.Agent', 'Log and manage product complaint cases', FALSE),
('176ec1b4-1984-044c-7a8f-21443aa95749', '1a877eae-f43e-551c-fa06-8012e0969199', 'ServiceNow CSM', 'Safety.Assessor', 'Record the safety assessment of complaint cases', FALSE),
('b7ff79a4-12ed-9fa7-e2a4-85104f75e98a', '49533110-087f-85b2-992f-57ef4b878298', 'SAP Ariba', 'Requisitioner', 'Create purchase requisitions', FALSE),
('b7ff79a4-12ed-9fa7-e2a4-85104f75e98a', 'd4578991-61f5-3e4a-0e41-c19c70cc37fd', 'SAP Ariba', 'Supplier.Manager', 'Manage supplier onboarding and profile changes', FALSE),
('21add413-7e0f-7bd1-2774-190d9b683816', 'b2a77289-7643-f530-fcd2-76aee7959f86', 'Workday', 'HR.Partner', 'HR partner security group for the Austin supervisory organisation', FALSE),
('c18ae31d-ba89-2e35-7e0f-d79e9130ddb8', 'ef3eeea0-9d3b-3991-9c7f-d003cc179dc0', 'Microsoft Purview', 'DataOwner.Quality', 'Data owner for quality collections in the Purview catalogue', TRUE),
('c18ae31d-ba89-2e35-7e0f-d79e9130ddb8', 'e929c560-50c7-9275-20c7-3bf601a6dc3f', 'Microsoft Purview', 'DataOwner.Finance', 'Data owner for finance collections in the Purview catalogue', TRUE)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS entra_id.app_role_assignment (
  id              varchar(60) NOT NULL,
  principal_id    uuid NOT NULL,
  principal_type  varchar(20) NOT NULL,
  resource_id     uuid NOT NULL,
  app_role_id     uuid NOT NULL,
  createddatetime timestamptz NOT NULL,
  deleteddatetime timestamptz,
  CONSTRAINT app_role_assignment_pk PRIMARY KEY (id)
);
COMMENT ON TABLE entra_id.app_role_assignment IS 'App role assignments to users (removed assignments retained with deleteddatetime from the audit feed).';

INSERT INTO entra_id.app_role_assignment (id, principal_id, principal_type, resource_id, app_role_id, createddatetime, deleteddatetime) VALUES
('c194298b-fea7-107c-d360-f19bb0cc22d0', '1abd5a54-dcc6-f3b0-70b8-b6c8d05540f4', 'User', 'ba276640-ad18-360e-14fa-47768d8ebb31', 'eba6db81-48ce-88f2-55b5-66b6de56a5b2', '2021-01-05 10:30:00+00', NULL),
('31c7bed2-fa4b-5f72-2d92-ff34342c0267', '94dfa23b-657d-2cd4-941d-3b5508e57bc3', 'User', 'ba276640-ad18-360e-14fa-47768d8ebb31', 'eba6db81-48ce-88f2-55b5-66b6de56a5b2', '2021-01-05 10:30:00+00', NULL),
('ec16c501-3d11-c1c1-a3f4-03cac4ce0ebc', '75786fc1-95c4-f31e-c7b5-1692a7238d45', 'User', 'ba276640-ad18-360e-14fa-47768d8ebb31', '0722af68-8f1a-ffe1-57af-0af1cd524f09', '2021-01-05 10:30:00+00', NULL),
('90a60b2e-93d6-b403-ae6c-e9e74af2ed8d', '2b7a9348-ed4d-fb84-5e19-407b912a830c', 'User', 'ba276640-ad18-360e-14fa-47768d8ebb31', '0722af68-8f1a-ffe1-57af-0af1cd524f09', '2021-01-05 10:30:00+00', '2026-05-30 02:00:00+00'),
('c7b76486-27bc-a376-c565-b2a3ba896741', '9a24783f-cd4f-e7e7-e2a3-d6dedab00fc0', 'User', 'ba276640-ad18-360e-14fa-47768d8ebb31', '0722af68-8f1a-ffe1-57af-0af1cd524f09', '2021-01-05 10:30:00+00', NULL),
('485ae7af-f318-6241-8e32-eeec8e4d9b02', 'f73c896d-87fd-224b-2c8f-882c91a051c3', 'User', 'ba276640-ad18-360e-14fa-47768d8ebb31', '0722af68-8f1a-ffe1-57af-0af1cd524f09', '2021-01-05 10:30:00+00', NULL),
('e1712234-f4c7-f93c-1fb9-2c8a16c81df7', '38162db3-4a5c-5980-c164-3e99b2f29878', 'User', 'ba276640-ad18-360e-14fa-47768d8ebb31', '0722af68-8f1a-ffe1-57af-0af1cd524f09', '2022-06-07 10:30:00+00', NULL),
('bb2a44cb-1b8f-ca8d-57cd-3c82398867e7', '503afe8a-75b5-567f-57b6-2323c466ce89', 'User', 'ba276640-ad18-360e-14fa-47768d8ebb31', '0722af68-8f1a-ffe1-57af-0af1cd524f09', '2026-03-03 10:30:00+00', NULL),
('0c233936-e46f-a015-d03f-ec671ad346b4', '3277d5dd-6d8d-fd59-45cb-7a2889ae7165', 'User', 'ba276640-ad18-360e-14fa-47768d8ebb31', '0722af68-8f1a-ffe1-57af-0af1cd524f09', '2026-06-02 10:30:00+00', NULL),
('ed68846f-b230-3fe8-fc43-ff33fa38159d', '477412af-d066-c918-d5b8-24c9fb270343', 'User', 'ba276640-ad18-360e-14fa-47768d8ebb31', 'f524363b-ec26-03f5-bd22-e0f2f49ba977', '2026-09-15 10:30:00+00', NULL),
('fffbddca-528d-a456-87d2-d2c13b2d715d', '1abd5a54-dcc6-f3b0-70b8-b6c8d05540f4', 'User', 'add489b8-8fc2-81d3-3c2e-10a808feebc0', '8af3c17c-792a-9ce0-97b7-6cd05b90d40a', '2021-01-05 10:30:00+00', NULL),
('89944bab-42ca-7137-3568-b2935a80de6a', '94dfa23b-657d-2cd4-941d-3b5508e57bc3', 'User', 'add489b8-8fc2-81d3-3c2e-10a808feebc0', '8af3c17c-792a-9ce0-97b7-6cd05b90d40a', '2021-01-05 10:30:00+00', NULL),
('7156befe-b112-81e1-6bac-5c874922dd5c', 'f73c896d-87fd-224b-2c8f-882c91a051c3', 'User', 'add489b8-8fc2-81d3-3c2e-10a808feebc0', '65ab9d3d-9bc1-72fe-dd27-a2bc944800c4', '2021-01-05 10:30:00+00', NULL),
('13246288-30f1-ea95-ccc0-239e1b9c4d0f', '38162db3-4a5c-5980-c164-3e99b2f29878', 'User', '176ec1b4-1984-044c-7a8f-21443aa95749', '15bc224c-4c6c-e110-9851-494cd667cf65', '2022-06-07 10:30:00+00', NULL),
('742fae04-bb3e-f71f-56c9-4551a6981761', '503afe8a-75b5-567f-57b6-2323c466ce89', 'User', '176ec1b4-1984-044c-7a8f-21443aa95749', '1a877eae-f43e-551c-fa06-8012e0969199', '2026-03-03 10:30:00+00', NULL),
('385a6019-7ab1-384f-9c27-027af63c5de4', '8bc771ec-a6af-6281-c616-19a61a8b65ae', 'User', 'b7ff79a4-12ed-9fa7-e2a4-85104f75e98a', '49533110-087f-85b2-992f-57ef4b878298', '2021-01-05 10:30:00+00', NULL),
('94c31a18-8f67-cd84-6524-8e0d87bb51f8', 'dd1b1f2a-d1a1-2d95-8c10-dc93b1e805c7', 'User', 'b7ff79a4-12ed-9fa7-e2a4-85104f75e98a', '49533110-087f-85b2-992f-57ef4b878298', '2021-01-05 10:30:00+00', NULL),
('2b8449df-f57b-10c8-6dce-9360b345865d', '8bc771ec-a6af-6281-c616-19a61a8b65ae', 'User', 'b7ff79a4-12ed-9fa7-e2a4-85104f75e98a', 'd4578991-61f5-3e4a-0e41-c19c70cc37fd', '2021-01-05 10:30:00+00', NULL),
('7e6f5e79-b9c5-9be5-e306-22b879a34ce2', 'c72b2c9c-9cec-996c-14c0-e5579e9b3bd3', 'User', '21add413-7e0f-7bd1-2774-190d9b683816', 'b2a77289-7643-f530-fcd2-76aee7959f86', '2021-01-05 10:30:00+00', NULL),
('a94afd56-75c4-e66a-810b-36972f71f229', '1abd5a54-dcc6-f3b0-70b8-b6c8d05540f4', 'User', 'c18ae31d-ba89-2e35-7e0f-d79e9130ddb8', 'ef3eeea0-9d3b-3991-9c7f-d003cc179dc0', '2021-01-05 10:30:00+00', NULL),
('56e37c47-1350-09a3-7cff-e717bc5c0eb1', '1332f649-d9b6-9e10-d443-eb453cf8736c', 'User', 'c18ae31d-ba89-2e35-7e0f-d79e9130ddb8', 'e929c560-50c7-9275-20c7-3bf601a6dc3f', '2021-01-05 10:30:00+00', NULL)
ON CONFLICT DO NOTHING;

-- Subscription inbound: tables and columns written by the coco_subscriptions_austin_systems DAG from the
-- digital products this system subscribes to (see coco-subscription-loads/austin_systems/entra_id).
-- No extract reads them.

ALTER TABLE entra_id.users ADD COLUMN IF NOT EXISTS employeetype varchar(40);
ALTER TABLE entra_id.users ADD COLUMN IF NOT EXISTS employee_org_data_cost_center varchar(20);
COMMENT ON COLUMN entra_id.users.employeetype IS 'employeeType from Worker Master Data (Employee/Contractor).';
COMMENT ON COLUMN entra_id.users.employee_org_data_cost_center IS 'employeeOrgData.costCenter: Workday cost centre from Worker Master Data.';

GRANT USAGE ON SCHEMA entra_id TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA entra_id TO egeria_user, airflow_user;
