-- system-qualified-name: SoftwareServer::SYS-012::SAP Concur
-- SAP Concur - Bucharest.  SAP Concur Expense for EKG employees: expense reports and entries with their receipts,
-- attendees (including healthcare professionals), cost centre allocations and the approval workflow; approved reports
-- are posted to SAP through the standard accounting extract.  Its tables feed Expense Approvals and Employee Expense
-- Claims.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS sap_concur;
COMMENT ON SCHEMA sap_concur IS 'SAP Concur Expense (EKG): Concur Intelligence / API v3 objects landed as tables (employee, report, entry, attendee, allocation, report workflow, cost object approver).';

CREATE TABLE IF NOT EXISTS sap_concur.employee (
  employee_id            varchar(20) NOT NULL,
  login_id               varchar(120) NOT NULL,
  first_name             varchar(80) NOT NULL,
  last_name              varchar(80) NOT NULL,
  org_unit_1             varchar(10) NOT NULL,
  org_unit_2             varchar(20) NOT NULL,
  reimbursement_currency varchar(3) NOT NULL,
  custom20_expense_limit numeric(18,2),
  active                 varchar(1) NOT NULL,
  CONSTRAINT employee_pk PRIMARY KEY (employee_id)
);
COMMENT ON TABLE sap_concur.employee IS 'Concur employee profiles (employee_id = Workday employee ID; org_unit_2 = default cost centre; custom20 = limit per report).';

INSERT INTO sap_concur.employee (employee_id, login_id, first_name, last_name, org_unit_1, org_unit_2, reimbursement_currency, custom20_expense_limit, active) VALUES
('20011', 'andrei.munteanu@ekgpharma.ro', 'Andrei', 'Munteanu', 'RO01', 'RO10-100', 'RON', '20000', 'Y'),
('20014', 'gheorghe.radu@ekgpharma.ro', 'Gheorghe', 'Radu', 'RO01', 'RO10-210', 'RON', '10000', 'Y'),
('20017', 'nicoleta.oprea@ekgpharma.ro', 'Nicoleta', 'Oprea', 'RO01', 'RO10-120', 'RON', '8000', 'Y'),
('20021', 'florin.stoica@ekgpharma.ro', 'Florin', 'Stoica', 'RO01', 'RO10-110', 'RON', NULL, 'Y'),
('20023', 'adina.petre@ekgpharma.ro', 'Adina', 'Petre', 'RO01', 'RO10-160', 'RON', '3000', 'Y'),
('20026', 'cristian.lungu@ekgpharma.ro', 'Cristian', 'Lungu', 'RO01', 'RO10-170', 'RON', '5000', 'Y'),
('20038', 'simona.florescu@ekgpharma.ro', 'Simona', 'Florescu', 'RO01', 'RO10-210', 'RON', '2000', 'Y'),
('20040', 'marian.bucur@ekgpharma.ro', 'Marian', 'Bucur', 'RO01', 'RO10-150', 'RON', '3000', 'Y'),
('20042', 'ciprian.tudor@ekgpharma.ro', 'Ciprian', 'Tudor', 'RO01', 'RO10-140', 'RON', '5000', 'Y'),
('20078', 'radu.stoian@ekgpharma.ro', 'Radu', 'Stoian', 'RO01', 'RO10-150', 'RON', '1000', 'Y'),
('20081', 'gabriela.toma@ekgpharma.ro', 'Gabriela', 'Toma', 'RO01', 'RO10-160', 'RON', '3000', 'Y')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_concur.cost_object_approver (
  cost_object_code     varchar(20) NOT NULL,
  approver_employee_id varchar(20) NOT NULL,
  approval_limit       numeric(18,2),
  currency             varchar(3) NOT NULL,
  CONSTRAINT cost_object_approver_pk PRIMARY KEY (cost_object_code)
);
COMMENT ON TABLE sap_concur.cost_object_approver IS 'Cost object approvers per cost centre.';

INSERT INTO sap_concur.cost_object_approver (cost_object_code, approver_employee_id, approval_limit, currency) VALUES
('RO10-120', '20011', 25000, 'RON'),
('RO10-140', '20014', 10000, 'RON'),
('RO10-150', '20021', 10000, 'RON'),
('RO10-160', '20023', 10000, 'RON'),
('RO10-170', '20011', 25000, 'RON'),
('RO10-210', '20014', 10000, 'RON')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_concur.report (
  report_key           integer NOT NULL,
  report_id            varchar(20) NOT NULL,
  employee_id          varchar(20) NOT NULL,
  report_name          varchar(80),
  submit_date          timestamptz,
  total_claimed_amount numeric(18,2) NOT NULL,
  currency_code        varchar(3) NOT NULL,
  approval_status_code varchar(10) NOT NULL,
  payment_status_code  varchar(10) NOT NULL,
  CONSTRAINT report_pk PRIMARY KEY (report_key)
);
COMMENT ON TABLE sap_concur.report IS 'Expense reports (A_APPR approved, A_PEND pending approval, A_RESU sent back; P_PAID paid, P_PROC in payment, P_NOTP not paid).';

INSERT INTO sap_concur.report (report_key, report_id, employee_id, report_name, submit_date, total_claimed_amount, currency_code, approval_status_code, payment_status_code) VALUES
(51203, 'R2026-0714-CL1', '20026', 'Vizite clienți iulie', '2026-07-31 16:10:00+00', 508.50, 'RON', 'A_APPR', 'P_PAID'),
(51206, 'R2026-0722-NO1', '20017', 'Audit furnizor Bachem, Bubendorf', '2026-07-27 11:40:00+00', 4845.60, 'RON', 'A_APPR', 'P_PAID'),
(51209, 'R2026-0805-CT1', '20042', 'Audit furnizor Stevanato, Piombino Dese', '2026-08-12 15:25:00+00', 667.00, 'EUR', 'A_APPR', 'P_PAID'),
(51212, 'R2026-0812-GT1', '20081', 'Conferința SRFC Brașov', '2026-08-24 10:15:00+00', 1872.00, 'RON', 'A_APPR', 'P_PAID'),
(51215, 'R2026-0826-AP1', '20023', 'Depunere documente ANMDMR', '2026-08-28 09:20:00+00', 92.00, 'RON', 'A_APPR', 'P_PAID'),
(51218, 'R2026-0910-CL2', '20026', 'Întâlnire medici oftalmologi - ser autolog', '2026-09-14 17:45:00+00', 1918.00, 'RON', 'A_APPR', 'P_PROC'),
(51221, 'R2026-0915-MB1', '20040', 'Instruire Maximo Timișoara', '2026-09-19 12:05:00+00', 1050.00, 'RON', 'A_APPR', 'P_PROC'),
(51224, 'R2026-0922-SF1', '20038', 'Ședință închidere lunară - materiale', '2026-09-23 18:30:00+00', 347.80, 'RON', 'A_APPR', 'P_PROC'),
(51227, 'R2026-0925-CL3', '20026', 'Vizită distribuitor Chișinău', '2026-09-28 11:10:00+00', 2686.00, 'RON', 'A_PEND', 'P_NOTP'),
(51230, 'R2026-0926-RS1', '20078', 'Piese etalonare - achiziție urgentă', '2026-09-29 08:45:00+00', 1180.00, 'RON', 'A_PEND', 'P_NOTP')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_concur.entry (
  entry_key            integer NOT NULL,
  report_key           integer NOT NULL,
  expense_type_code    varchar(10) NOT NULL,
  expense_type_name    varchar(60) NOT NULL,
  transaction_date     date NOT NULL,
  posted_amount        numeric(18,2) NOT NULL,
  business_purpose     text,
  receipt_image_id     varchar(40),
  journal_account_code varchar(20) NOT NULL,
  CONSTRAINT entry_pk PRIMARY KEY (entry_key)
);
COMMENT ON TABLE sap_concur.entry IS 'Expense entries (posted amount in the report currency; journal account = SAP G/L account).';

INSERT INTO sap_concur.entry (entry_key, report_key, expense_type_code, expense_type_name, transaction_date, posted_amount, business_purpose, receipt_image_id, journal_account_code) VALUES
(208001, 51203, 'CARMI', 'Kilometraj auto personal', '2026-07-14', 412.00, 'București - Pitești - București, Fildas Trading', NULL, '625000'),
(208002, 51203, 'MEALS', 'Masă', '2026-07-14', 96.50, 'Prânz deplasare Pitești', 'IMG-A60F80605E19AD01', '625000'),
(208003, 51206, 'AIRFR', 'Bilet avion', '2026-07-20', 2890.40, 'OTP-BSL-OTP', 'IMG-1F6C4BF9C486DB15', '625000'),
(208004, 51206, 'LODNG', 'Cazare', '2026-07-21', 1745.20, 'Hotel Basel, 2 nopți (CHF convertit)', 'IMG-539257C333D4D699', '625000'),
(208005, 51206, 'TAXIX', 'Taxi', '2026-07-22', 210.00, 'Transfer aeroport', 'IMG-AACF72AECBC313E5', '625000'),
(208006, 51209, 'AIRFR', 'Bilet avion', '2026-08-04', 312.60, 'OTP-VCE-OTP', 'IMG-11A09AF373668185', '625000'),
(208007, 51209, 'LODNG', 'Cazare', '2026-08-05', 236.00, 'Hotel Padova, 2 nopți', NULL, '625000'),
(208008, 51209, 'CARRT', 'Închiriere auto', '2026-08-05', 118.40, 'Auto închiriat Veneția', 'IMG-3DB29D0C1DCA2A16', '625000'),
(208009, 51212, 'CONFR', 'Taxă conferință', '2026-08-12', 950.00, 'Taxă participare Conferința Națională de Farmacovigilență', 'IMG-2CA078502DE7DE7D', '628000'),
(208010, 51212, 'LODNG', 'Cazare', '2026-08-12', 780.00, 'Hotel Brașov, 2 nopți', 'IMG-AF4389C86B396BE2', '625000'),
(208011, 51212, 'TRAIN', 'Tren', '2026-08-12', 142.00, 'București - Brașov - București', 'IMG-565F33FF07ADCD7E', '625000'),
(208012, 51215, 'TAXIX', 'Taxi', '2026-08-26', 68.00, 'Sediu ANMDMR, Av. Sănătescu', 'IMG-3124EDAA2B3FA05D', '625000'),
(208013, 51215, 'PARKG', 'Parcare', '2026-08-26', 24.00, 'Parcare', NULL, '625000'),
(208014, 51218, 'BUSML', 'Masă de afaceri cu invitați', '2026-09-10', 1860.00, 'Cină de lucru: protocolul ser autolog, Spitalul Clinic de Urgență Oftalmologică', 'IMG-9B83386722974F5D', '623000'),
(208015, 51218, 'CARMI', 'Kilometraj auto personal', '2026-09-10', 58.00, 'Deplasare restaurant', NULL, '625000'),
(208016, 51221, 'TRAIN', 'Tren', '2026-09-15', 236.00, 'București - Timișoara - București', 'IMG-1FF5429256DB4963', '625000'),
(208017, 51221, 'LODNG', 'Cazare', '2026-09-15', 640.00, 'Hotel Timișoara, 2 nopți', 'IMG-BF0DDF6AF413B1A8', '625000'),
(208018, 51221, 'MEALS', 'Masă', '2026-09-16', 174.00, 'Diurnă mese', NULL, '625000'),
(208019, 51224, 'OFFSU', 'Consumabile birou', '2026-09-22', 347.80, 'Materiale ședință închidere', 'IMG-7656A525827849A1', '604000'),
(208020, 51227, 'CARMI', 'Kilometraj auto personal', '2026-09-24', 1296.00, 'București - Chișinău - București, Moldfarm', NULL, '625000'),
(208021, 51227, 'LODNG', 'Cazare', '2026-09-24', 610.00, 'Hotel Chișinău, 1 noapte', 'IMG-A465DBC978996E06', '625000'),
(208022, 51227, 'BUSML', 'Masă de afaceri cu invitați', '2026-09-25', 780.00, 'Prânz de lucru Moldfarm Distribuție', 'IMG-0526394D376F9AEC', '623000'),
(208023, 51230, 'OFFSU', 'Consumabile', '2026-09-26', 1180.00, 'Sonde temperatură de rezervă pentru autoclavă (achiziție urgentă cu card personal)', 'IMG-D4135F967ED10BCF', '604000')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_concur.attendee (
  attendee_key       integer NOT NULL,
  entry_key          integer NOT NULL,
  attendee_type_code varchar(10) NOT NULL,
  external_id        varchar(40),
  first_name         varchar(80),
  last_name          varchar(80),
  company            varchar(120),
  CONSTRAINT attendee_pk PRIMARY KEY (attendee_key)
);
COMMENT ON TABLE sap_concur.attendee IS 'Entry attendees (HCP external id = the doctor''s professional stamp code, needed for transfer-of-value disclosure).';

INSERT INTO sap_concur.attendee (attendee_key, entry_key, attendee_type_code, external_id, first_name, last_name, company) VALUES
(7701, 208014, 'HCP', 'RO-PAR-B40217', 'Mihaela', 'Tănase', 'Spitalul Clinic de Urgență Oftalmologică București'),
(7702, 208014, 'HCP', 'RO-PAR-B51932', 'Ovidiu', 'Munteanu', 'Spitalul Clinic de Urgență Oftalmologică București'),
(7703, 208014, 'HCP', 'RO-PAR-C22804', 'Irina', 'Bălan', 'Spitalul Clinic Județean de Urgență Cluj-Napoca'),
(7704, 208014, 'EMPLOYEE', '20026', 'Cristian', 'Lungu', 'EKG Pharmaceuticals S.R.L.'),
(7705, 208022, 'BUSGUEST', NULL, 'Victor', 'Rusu', 'Moldfarm Distribuție S.R.L.'),
(7706, 208022, 'EMPLOYEE', '20026', 'Cristian', 'Lungu', 'EKG Pharmaceuticals S.R.L.')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_concur.allocation (
  allocation_key      bigint NOT NULL,
  entry_key           integer NOT NULL,
  custom1_cost_center varchar(20) NOT NULL,
  percentage          numeric(5,2) NOT NULL,
  CONSTRAINT allocation_pk PRIMARY KEY (allocation_key)
);
COMMENT ON TABLE sap_concur.allocation IS 'Cost centre allocation of each entry.';

INSERT INTO sap_concur.allocation (allocation_key, entry_key, custom1_cost_center, percentage) VALUES
(2080011, 208001, 'RO10-170', 100.00),
(2080021, 208002, 'RO10-170', 100.00),
(2080031, 208003, 'RO10-120', 100.00),
(2080041, 208004, 'RO10-120', 100.00),
(2080051, 208005, 'RO10-120', 100.00),
(2080061, 208006, 'RO10-140', 100.00),
(2080071, 208007, 'RO10-140', 100.00),
(2080081, 208008, 'RO10-140', 100.00),
(2080091, 208009, 'RO10-160', 100.00),
(2080101, 208010, 'RO10-160', 100.00),
(2080111, 208011, 'RO10-160', 100.00),
(2080121, 208012, 'RO10-160', 100.00),
(2080131, 208013, 'RO10-160', 100.00),
(2080141, 208014, 'RO10-170', 100.00),
(2080151, 208015, 'RO10-170', 100.00),
(2080161, 208016, 'RO10-150', 100.00),
(2080171, 208017, 'RO10-150', 100.00),
(2080181, 208018, 'RO10-150', 100.00),
(2080191, 208019, 'RO10-210', 100.00),
(2080201, 208020, 'RO10-170', 100.00),
(2080211, 208021, 'RO10-170', 100.00),
(2080221, 208022, 'RO10-170', 100.00),
(2080231, 208023, 'RO10-150', 100.00)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sap_concur.report_workflow (
  report_key           integer NOT NULL,
  step_sequence        integer NOT NULL,
  approver_employee_id varchar(20) NOT NULL,
  status               varchar(20) NOT NULL,
  action_datetime      timestamptz,
  comment              text,
  CONSTRAINT report_workflow_pk PRIMARY KEY (report_key, step_sequence)
);
COMMENT ON TABLE sap_concur.report_workflow IS 'Approval workflow steps per report (APPROVED, SENT_BACK, PENDING).';

INSERT INTO sap_concur.report_workflow (report_key, step_sequence, approver_employee_id, status, action_datetime, comment) VALUES
(51203, 1, '20011', 'APPROVED', '2026-08-01 09:05:00+00', NULL),
(51206, 1, '20011', 'APPROVED', '2026-07-28 08:30:00+00', NULL),
(51209, 1, '20014', 'SENT_BACK', '2026-08-13 10:02:00+00', 'Lipsește factura hotelului; atașați documentul.'),
(51209, 2, '20014', 'APPROVED', '2026-08-18 09:47:00+00', NULL),
(51212, 1, '20023', 'APPROVED', '2026-08-25 12:30:00+00', NULL),
(51215, 1, '20011', 'APPROVED', '2026-08-28 17:55:00+00', NULL),
(51218, 1, '20011', 'APPROVED', '2026-09-16 08:12:00+00', NULL),
(51221, 1, '20021', 'APPROVED', '2026-09-22 16:40:00+00', NULL),
(51224, 1, '20014', 'APPROVED', '2026-09-23 18:36:00+00', NULL),
(51227, 1, '20011', 'PENDING', NULL, NULL),
(51230, 1, '20021', 'PENDING', NULL, NULL)
ON CONFLICT DO NOTHING;

GRANT USAGE ON SCHEMA sap_concur TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA sap_concur TO egeria_user, airflow_user;
