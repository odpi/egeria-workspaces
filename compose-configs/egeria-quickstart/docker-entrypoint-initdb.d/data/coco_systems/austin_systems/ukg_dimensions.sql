-- system-qualified-name: SoftwareServer::AUS-SYS-021::SN-TNA-AU-20190305
-- UKG Dimensions - Austin.  Time and attendance for Austin's hourly plant workforce: timecards totalised by labour
-- account and the pay statements imported back from Workday payroll.  Its tables feed Payroll Results (hourly
-- postings).
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS ukg_dimensions;
COMMENT ON SCHEMA ukg_dimensions IS 'UKG Dimensions (Austin): hourly people records and pay statements by worked labour account.';

CREATE TABLE IF NOT EXISTS ukg_dimensions.person (
  person_number          varchar(20) NOT NULL,
  first_name             varchar(80) NOT NULL,
  last_name              varchar(80) NOT NULL,
  pay_rule_name          varchar(60) NOT NULL,
  home_labor_account     varchar(80) NOT NULL,
  hire_date              date NOT NULL,
  employment_status      varchar(20) NOT NULL,
  employment_status_date date NOT NULL,
  CONSTRAINT person_pk PRIMARY KEY (person_number)
);
COMMENT ON TABLE ukg_dimensions.person IS 'People with timecards (hourly workers fed from Workday).';

INSERT INTO ukg_dimensions.person (person_number, first_name, last_name, pay_rule_name, home_labor_account, hire_date, employment_status, employment_status_date) VALUES
('100122', 'Brian', 'Foster', 'US Hourly Plant', 'US10/CC-US10-110/JP-MFG-OP2', '2021-04-19', 'Terminated', '2026-08-14'),
('100149', 'Aaliyah', 'Brooks', 'US Hourly Plant', 'US10/CC-US10-110/JP-MFG-OP3', '2019-10-07', 'Active', '2019-10-07'),
('100153', 'Tyler', 'Nguyen', 'US Hourly Plant', 'US10/CC-US10-110/JP-MFG-OP3', '2022-03-21', 'Active', '2022-03-21'),
('100158', 'Grace', 'Lindqvist', 'US Hourly Plant', 'US10/CC-US10-115/JP-CT-SPEC', '2023-01-09', 'Active', '2023-01-09'),
('100162', 'Omar', 'Haddad', 'US Hourly Plant', 'US10/CC-US10-140/JP-WH-LEAD', '2018-11-05', 'Active', '2018-11-05'),
('100189', 'Samuel', 'Adeyemi', 'US Hourly Plant', 'US10/CC-US10-140/JP-LOG-DG', '2021-02-15', 'Active', '2021-02-15')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS ukg_dimensions.pay_statement (
  pay_statement_id     varchar(30) NOT NULL,
  person_number        varchar(20) NOT NULL,
  payroll_reference    varchar(30) NOT NULL,
  pay_period_start     date NOT NULL,
  pay_period_end       date NOT NULL,
  pay_date             date NOT NULL,
  worked_labor_account varchar(80) NOT NULL,
  total_hours          numeric(8,2) NOT NULL,
  gross_wages          numeric(18,2) NOT NULL,
  employer_taxes       numeric(18,2) NOT NULL,
  employer_benefits    numeric(18,2) NOT NULL,
  net_pay              numeric(18,2) NOT NULL,
  gl_account           varchar(20) NOT NULL,
  CONSTRAINT pay_statement_pk PRIMARY KEY (pay_statement_id)
);
COMMENT ON TABLE ukg_dimensions.pay_statement IS 'Pay statements imported from Workday for kiosk display, with the labour account most hours were worked in.';

INSERT INTO ukg_dimensions.pay_statement (pay_statement_id, person_number, payroll_reference, pay_period_start, pay_period_end, pay_date, worked_labor_account, total_hours, gross_wages, employer_taxes, employer_benefits, net_pay, gl_account) VALUES
('PS-202607-100122', '100122', 'PR-US01-2026-07', '2026-07-01', '2026-07-31', '2026-07-31', 'US10/CC-US10-110/JP-MFG-OP2', 176.00, 4356.00, 333.19, 609.88, 3101.47, '6100200'),
('PS-202607-100149', '100149', 'PR-US01-2026-07', '2026-07-01', '2026-07-31', '2026-07-31', 'US10/CC-US10-110/JP-MFG-OP3', 184.00, 5546.00, 424.21, 776.50, 3948.75, '6100200'),
('PS-202607-100153', '100153', 'PR-US01-2026-07', '2026-07-01', '2026-07-31', '2026-07-31', 'US10/CC-US10-110/JP-MFG-OP3', 190.00, 5811.50, 444.52, 813.67, 4137.79, '6100200'),
('PS-202607-100158', '100158', 'PR-US01-2026-07', '2026-07-01', '2026-07-31', '2026-07-31', 'US10/CC-US10-115/JP-CT-SPEC', 172.00, 5676.00, 434.15, 794.70, 4041.31, '6100200'),
('PS-202607-100162', '100162', 'PR-US01-2026-07', '2026-07-01', '2026-07-31', '2026-07-31', 'US10/CC-US10-140/JP-WH-LEAD', 180.00, 4959.50, 379.35, 694.38, 3531.16, '6100200'),
('PS-202607-100189', '100189', 'PR-US01-2026-07', '2026-07-01', '2026-07-31', '2026-07-31', 'US10/CC-US10-140/JP-LOG-DG', 176.00, 5016.00, 383.67, 702.29, 3571.39, '6100200'),
('PS-202608-100122', '100122', 'PR-US01-2026-08', '2026-08-01', '2026-08-31', '2026-08-31', 'US10/CC-US10-110/JP-MFG-OP2', 75.87, 1877.78, 143.63, 262.91, 1336.98, '6100200'),
('PS-202608-100149', '100149', 'PR-US01-2026-08', '2026-08-01', '2026-08-31', '2026-08-31', 'US10/CC-US10-110/JP-MFG-OP3', 178.00, 5280.50, 403.90, 739.33, 3759.72, '6100200'),
('PS-202608-100153', '100153', 'PR-US01-2026-08', '2026-08-01', '2026-08-31', '2026-08-31', 'US10/CC-US10-110/JP-MFG-OP3', 186.00, 5634.50, 430.98, 788.89, 4011.76, '6100200'),
('PS-202608-100158', '100158', 'PR-US01-2026-08', '2026-08-01', '2026-08-31', '2026-08-31', 'US10/CC-US10-115/JP-CT-SPEC', 174.00, 5742.00, 439.20, 803.94, 4088.30, '6100200'),
('PS-202608-100162', '100162', 'PR-US01-2026-08', '2026-08-01', '2026-08-31', '2026-08-31', 'US10/CC-US10-140/JP-WH-LEAD', 181.00, 5000.38, 382.48, 700.10, 3560.27, '6100200'),
('PS-202608-100189', '100189', 'PR-US01-2026-08', '2026-08-01', '2026-08-31', '2026-08-31', 'US10/CC-US10-140/JP-LOG-DG', 168.00, 4788.00, 366.23, 670.37, 3409.06, '6100200'),
('PS-202609-100149', '100149', 'PR-US01-2026-09', '2026-09-01', '2026-09-30', '2026-09-30', 'US10/CC-US10-115/JP-MFG-OP3', 170.00, 5015.00, 383.60, 702.15, 3570.68, '6100200'),
('PS-202609-100153', '100153', 'PR-US01-2026-09', '2026-09-01', '2026-09-30', '2026-09-30', 'US10/CC-US10-110/JP-MFG-OP3', 176.00, 5192.00, 397.13, 726.94, 3696.70, '6100200'),
('PS-202609-100158', '100158', 'PR-US01-2026-09', '2026-09-01', '2026-09-30', '2026-09-30', 'US10/CC-US10-115/JP-CT-SPEC', 188.00, 6402.00, 489.68, 896.35, 4558.22, '6100200'),
('PS-202609-100162', '100162', 'PR-US01-2026-09', '2026-09-01', '2026-09-30', '2026-09-30', 'US10/CC-US10-140/JP-WH-LEAD', 169.00, 4605.25, 352.25, 644.79, 3278.94, '6100200'),
('PS-202609-100189', '100189', 'PR-US01-2026-09', '2026-09-01', '2026-09-30', '2026-09-30', 'US10/CC-US10-140/JP-LOG-DG', 183.00, 5315.25, 406.56, 744.19, 3784.46, '6100200')
ON CONFLICT DO NOTHING;

GRANT USAGE ON SCHEMA ukg_dimensions TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA ukg_dimensions TO egeria_user, airflow_user;
