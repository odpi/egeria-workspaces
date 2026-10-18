-- system-qualified-name: SoftwareServer::AUS-SYS-019::SN-HCM-AU-20190301
-- Workday Human Capital Management - Austin.  The worker record for the Austin workforce and the US payroll.  Its
-- tables feed Worker Master Data, Worker Lifecycle Events and Payroll Results.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS workday_hcm;
COMMENT ON SCHEMA workday_hcm IS 'Workday HCM (Austin): workers, positions, job profiles, business process events, integration events and US payroll results, as landed by the Workday reporting extract (RaaS).';

CREATE TABLE IF NOT EXISTS workday_hcm.job_profile (
  job_profile_id              varchar(40) NOT NULL,
  job_profile_name            varchar(120) NOT NULL,
  job_family                  varchar(60),
  work_hazards                text,
  approval_authority_amount   numeric(18,2),
  approval_authority_currency varchar(3),
  inactive                    boolean NOT NULL,
  CONSTRAINT job_profile_pk PRIMARY KEY (job_profile_id)
);
COMMENT ON TABLE workday_hcm.job_profile IS 'Job profiles; the job profile ID is the role code used by Cornerstone and the directory.';

INSERT INTO workday_hcm.job_profile (job_profile_id, job_profile_name, job_family, work_hazards, approval_authority_amount, approval_authority_currency, inactive) VALUES
('JP-SITE-HEAD', 'Site Head, Austin', 'Leadership', NULL, 250000, 'USD', FALSE),
('JP-QA-DIR', 'Director of Quality Assurance', 'Quality', NULL, 50000, 'USD', FALSE),
('JP-QA-BDS', 'QA Batch Disposition Specialist', 'Quality', 'Cytotoxic exposure during batch record review on the floor', NULL, NULL, FALSE),
('JP-QC-MGR', 'QC Laboratory Manager', 'Quality', 'Laboratory chemicals; cytotoxic reference standards', 25000, 'USD', FALSE),
('JP-QC-ANL2', 'QC Analyst II', 'Quality', 'Laboratory chemicals; cytotoxic reference standards', NULL, NULL, FALSE),
('JP-QC-ANL1', 'QC Analyst I', 'Quality', 'Laboratory chemicals', NULL, NULL, FALSE),
('JP-QC-CHROM', 'QC Chromatography Analyst', 'Quality', 'Laboratory solvents (acetonitrile, methanol)', NULL, NULL, FALSE),
('JP-MFG-SUP', 'Manufacturing Supervisor', 'Manufacturing', 'Cytotoxic compounding; noise; powered equipment', 10000, 'USD', FALSE),
('JP-MFG-OP3', 'Production Operator III', 'Manufacturing', 'Cytotoxic compounding; noise; powered equipment', NULL, NULL, FALSE),
('JP-MFG-OP2', 'Production Operator II', 'Manufacturing', 'Noise; powered equipment; API dust', NULL, NULL, FALSE),
('JP-CT-SPEC', 'Cell Therapy Manufacturing Specialist', 'Manufacturing', 'Human biological material; liquid nitrogen', NULL, NULL, FALSE),
('JP-WH-LEAD', 'Warehouse Lead', 'Supply Chain', 'Forklift operation; cold room', NULL, NULL, FALSE),
('JP-LOG-DG', 'Shipping and Dangerous Goods Coordinator', 'Supply Chain', 'Dry ice; cytotoxic consignments', 5000, 'USD', FALSE),
('JP-ENG-CAL', 'Maintenance and Calibration Engineer', 'Engineering', 'Electrical isolation; working at height', 5000, 'USD', FALSE),
('JP-CQ-SPEC', 'Customer Quality Specialist', 'Quality', NULL, NULL, NULL, FALSE),
('JP-PV-ASSOC', 'Drug Safety Associate', 'Quality', NULL, NULL, NULL, FALSE),
('JP-FIN-CTRL', 'Site Controller', 'Finance', NULL, 100000, 'USD', FALSE),
('JP-FIN-SRACC', 'Senior Accountant', 'Finance', NULL, 10000, 'USD', FALSE),
('JP-FIN-AP', 'Accounts Payable Specialist', 'Finance', NULL, NULL, NULL, FALSE),
('JP-PROC-MGR', 'Procurement Manager', 'Procurement', NULL, 75000, 'USD', FALSE),
('JP-HR-BP', 'HR Business Partner', 'Human Resources', NULL, 5000, 'USD', FALSE),
('JP-VAL-CONS', 'Validation Consultant', 'Engineering', 'Cleanroom entry', NULL, NULL, FALSE),
('JP-AUD-CONS', 'GMP Audit Consultant', 'Quality', 'Cleanroom entry', NULL, NULL, FALSE)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS workday_hcm.worker (
  employee_id           varchar(20) NOT NULL,
  worker_type           varchar(30) NOT NULL,
  legal_name_first_name varchar(80) NOT NULL,
  legal_name_last_name  varchar(80) NOT NULL,
  company_id            varchar(10) NOT NULL,
  location_id           varchar(30) NOT NULL,
  hire_date             date NOT NULL,
  termination_date      date,
  active                boolean NOT NULL,
  on_leave              boolean NOT NULL,
  pay_rate_type         varchar(20),
  work_email            varchar(120),
  last_updated          timestamptz NOT NULL,
  CONSTRAINT worker_pk PRIMARY KEY (employee_id)
);
COMMENT ON TABLE workday_hcm.worker IS 'One row per worker (employees and contingent workers).';

INSERT INTO workday_hcm.worker (employee_id, worker_type, legal_name_first_name, legal_name_last_name, company_id, location_id, hire_date, termination_date, active, on_leave, pay_rate_type, work_email, last_updated) VALUES
('100101', 'Employee', 'Rebecca', 'Hernandez', 'US01', 'LOC-AUS-PLANT', '2014-03-03', NULL, TRUE, FALSE, 'Salary', 'rhernandez@austinpharma.com', '2014-03-03 18:00:00+00'),
('100112', 'Employee', 'Marcus', 'Whitfield', 'US01', 'LOC-AUS-PLANT', '2016-06-13', NULL, TRUE, FALSE, 'Salary', 'mwhitfield@austinpharma.com', '2016-06-13 18:00:00+00'),
('100118', 'Employee', 'Priya', 'Raman', 'US01', 'LOC-AUS-PLANT', '2019-01-07', NULL, TRUE, FALSE, 'Salary', 'praman@austinpharma.com', '2019-01-07 18:00:00+00'),
('100122', 'Employee', 'Brian', 'Foster', 'US01', 'LOC-AUS-PLANT', '2021-04-19', '2026-08-14', FALSE, FALSE, 'Hourly', 'bfoster@austinpharma.com', '2026-08-14 18:00:00+00'),
('100124', 'Employee', 'Daniel', 'Okafor', 'US01', 'LOC-AUS-PLANT', '2017-09-11', NULL, TRUE, FALSE, 'Salary', 'dokafor@austinpharma.com', '2017-09-11 18:00:00+00'),
('100128', 'Employee', 'Carla', 'Ruiz', 'US01', 'LOC-AUS-PLANT', '2020-02-03', '2026-05-29', FALSE, FALSE, 'Salary', 'cruiz@austinpharma.com', '2026-05-29 18:00:00+00'),
('100131', 'Employee', 'Sofia', 'Delgado', 'US01', 'LOC-AUS-PLANT', '2020-08-24', NULL, TRUE, TRUE, 'Salary', 'sdelgado@austinpharma.com', '2026-09-15 18:00:00+00'),
('100137', 'Employee', 'Kevin', 'Tran', 'US01', 'LOC-AUS-PLANT', '2026-02-09', NULL, TRUE, FALSE, 'Salary', 'ktran@austinpharma.com', '2026-02-09 18:00:00+00'),
('100142', 'Employee', 'Jason', 'Morales', 'US01', 'LOC-AUS-PLANT', '2018-05-14', NULL, TRUE, FALSE, 'Salary', 'jmorales@austinpharma.com', '2018-05-14 18:00:00+00'),
('100149', 'Employee', 'Aaliyah', 'Brooks', 'US01', 'LOC-AUS-PLANT', '2019-10-07', NULL, TRUE, FALSE, 'Hourly', 'abrooks@austinpharma.com', '2019-10-07 18:00:00+00'),
('100153', 'Employee', 'Tyler', 'Nguyen', 'US01', 'LOC-AUS-PLANT', '2022-03-21', NULL, TRUE, FALSE, 'Hourly', 'tnguyen@austinpharma.com', '2022-03-21 18:00:00+00'),
('100158', 'Employee', 'Grace', 'Lindqvist', 'US01', 'LOC-AUS-PLANT', '2023-01-09', NULL, TRUE, FALSE, 'Hourly', 'glindqvist@austinpharma.com', '2023-01-09 18:00:00+00'),
('100162', 'Employee', 'Omar', 'Haddad', 'US01', 'LOC-AUS-DC', '2018-11-05', NULL, TRUE, FALSE, 'Hourly', 'ohaddad@austinpharma.com', '2018-11-05 18:00:00+00'),
('100167', 'Employee', 'Hannah', 'Kowalski', 'US01', 'LOC-AUS-PLANT', '2017-04-03', NULL, TRUE, FALSE, 'Salary', 'hkowalski@austinpharma.com', '2017-04-03 18:00:00+00'),
('100171', 'Employee', 'Luis', 'Carranza', 'US01', 'LOC-AUS-PLANT', '2020-07-13', NULL, TRUE, FALSE, 'Salary', 'lcarranza@austinpharma.com', '2020-07-13 18:00:00+00'),
('100176', 'Employee', 'Megan', 'O''Neill', 'US01', 'LOC-AUS-PLANT', '2021-09-20', NULL, TRUE, FALSE, 'Salary', 'moneill@austinpharma.com', '2021-09-20 18:00:00+00'),
('100180', 'Employee', 'Ethan', 'Park', 'US01', 'LOC-AUS-PLANT', '2019-05-06', NULL, TRUE, FALSE, 'Salary', 'epark@austinpharma.com', '2019-05-06 18:00:00+00'),
('100184', 'Employee', 'Chloe', 'Bennett', 'US01', 'LOC-AUS-PLANT', '2020-11-02', NULL, TRUE, FALSE, 'Salary', 'cbennett@austinpharma.com', '2020-11-02 18:00:00+00'),
('100189', 'Employee', 'Samuel', 'Adeyemi', 'US01', 'LOC-AUS-DC', '2021-02-15', NULL, TRUE, FALSE, 'Hourly', 'sadeyemi@austinpharma.com', '2021-02-15 18:00:00+00'),
('100193', 'Employee', 'Nina', 'Petrov', 'US01', 'LOC-AUS-PLANT', '2019-08-19', NULL, TRUE, FALSE, 'Salary', 'npetrov@austinpharma.com', '2019-08-19 18:00:00+00'),
('100197', 'Employee', 'Robert', 'Castillo', 'US01', 'LOC-AUS-PLANT', '2022-06-06', NULL, TRUE, FALSE, 'Salary', 'rcastillo@austinpharma.com', '2022-06-06 18:00:00+00'),
('100201', 'Employee', 'Isabel', 'Moreno', 'US01', 'LOC-AUS-PLANT', '2026-03-02', NULL, TRUE, FALSE, 'Salary', 'imoreno@austinpharma.com', '2026-03-02 18:00:00+00'),
('100205', 'Employee', 'Mia', 'Johnson', 'US01', 'LOC-AUS-PLANT', '2026-09-08', NULL, TRUE, FALSE, 'Salary', 'mjohnson@austinpharma.com', '2026-09-08 18:00:00+00'),
('C00015', 'Contingent Worker', 'Derek', 'Shaw', 'US01', 'LOC-AUS-PLANT', '2026-06-01', NULL, TRUE, FALSE, NULL, 'dshaw.ext@austinpharma.com', '2026-06-01 18:00:00+00'),
('C00021', 'Contingent Worker', 'Laura', 'Chen', 'US01', 'LOC-AUS-PLANT', '2026-09-14', NULL, TRUE, FALSE, NULL, 'lchen.ext@austinpharma.com', '2026-09-14 18:00:00+00')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS workday_hcm.worker_position (
  position_id         varchar(20) NOT NULL,
  effective_date      date NOT NULL,
  employee_id         varchar(20) NOT NULL,
  job_profile_id      varchar(40) NOT NULL,
  business_title      varchar(120),
  cost_center_id      varchar(20) NOT NULL,
  manager_employee_id varchar(20),
  end_date            date,
  primary_job         boolean NOT NULL,
  CONSTRAINT worker_position_pk PRIMARY KEY (position_id, effective_date)
);
COMMENT ON TABLE workday_hcm.worker_position IS 'Position history: one row per position assignment, effective dated.';

INSERT INTO workday_hcm.worker_position (position_id, effective_date, employee_id, job_profile_id, business_title, cost_center_id, manager_employee_id, end_date, primary_job) VALUES
('P-US10-0101', '2014-03-03', '100101', 'JP-SITE-HEAD', 'Site Head, Austin', 'CC-US10-100', NULL, NULL, TRUE),
('P-US10-0112', '2016-06-13', '100112', 'JP-QA-DIR', 'Director of Quality Assurance', 'CC-US10-120', '100101', NULL, TRUE),
('P-US10-0118', '2019-01-07', '100118', 'JP-QA-BDS', 'QA Batch Disposition Specialist', 'CC-US10-120', '100112', NULL, TRUE),
('P-US10-0122', '2021-04-19', '100122', 'JP-MFG-OP2', 'Production Operator II', 'CC-US10-110', '100142', '2026-08-14', TRUE),
('P-US10-0124', '2017-09-11', '100124', 'JP-QC-MGR', 'QC Laboratory Manager', 'CC-US10-130', '100112', NULL, TRUE),
('P-US10-0128', '2020-02-03', '100128', 'JP-QC-ANL2', 'QC Analyst II', 'CC-US10-130', '100124', '2026-05-29', TRUE),
('P-US10-0131', '2020-08-24', '100131', 'JP-QC-ANL2', 'QC Analyst II', 'CC-US10-130', '100124', NULL, TRUE),
('P-US10-0137', '2026-02-09', '100137', 'JP-QC-CHROM', 'QC Chromatography Analyst', 'CC-US10-130', '100124', NULL, TRUE),
('P-US10-0142', '2018-05-14', '100142', 'JP-MFG-SUP', 'Manufacturing Supervisor', 'CC-US10-110', '100101', NULL, TRUE),
('P-US10-0149', '2019-10-07', '100149', 'JP-MFG-OP3', 'Production Operator III', 'CC-US10-110', '100142', NULL, TRUE),
('P-US10-0153', '2022-03-21', '100153', 'JP-MFG-OP2', 'Production Operator II', 'CC-US10-110', '100142', '2026-06-30', TRUE),
('P-US10-0153', '2026-07-01', '100153', 'JP-MFG-OP3', 'Production Operator III', 'CC-US10-110', '100142', NULL, TRUE),
('P-US10-0158', '2023-01-09', '100158', 'JP-CT-SPEC', 'Cell Therapy Manufacturing Specialist', 'CC-US10-115', '100142', NULL, TRUE),
('P-US10-0162', '2018-11-05', '100162', 'JP-WH-LEAD', 'Warehouse Lead', 'CC-US10-140', '100101', NULL, TRUE),
('P-US10-0167', '2017-04-03', '100167', 'JP-FIN-CTRL', 'Site Controller', 'CC-US10-210', '100101', NULL, TRUE),
('P-US10-0171', '2020-07-13', '100171', 'JP-FIN-SRACC', 'Senior Accountant', 'CC-US10-210', '100167', NULL, TRUE),
('P-US10-0176', '2021-09-20', '100176', 'JP-FIN-AP', 'Accounts Payable Specialist', 'CC-US10-210', '100167', NULL, TRUE),
('P-US10-0180', '2019-05-06', '100180', 'JP-PROC-MGR', 'Procurement Manager', 'CC-US10-230', '100167', NULL, TRUE),
('P-US10-0184', '2020-11-02', '100184', 'JP-HR-BP', 'HR Business Partner', 'CC-US10-220', '100101', NULL, TRUE),
('P-US10-0189', '2021-02-15', '100189', 'JP-LOG-DG', 'Shipping and Dangerous Goods Coordinator', 'CC-US10-140', '100162', NULL, TRUE),
('P-US10-0193', '2019-08-19', '100193', 'JP-ENG-CAL', 'Maintenance and Calibration Engineer', 'CC-US10-150', '100101', NULL, TRUE),
('P-US10-0197', '2022-06-06', '100197', 'JP-CQ-SPEC', 'Customer Quality Specialist', 'CC-US10-160', '100112', NULL, TRUE),
('P-US10-0201', '2026-03-02', '100201', 'JP-PV-ASSOC', 'Drug Safety Associate', 'CC-US10-160', '100112', NULL, TRUE),
('P-US10-0205', '2026-09-08', '100205', 'JP-QC-ANL1', 'QC Analyst I', 'CC-US10-130', '100124', NULL, TRUE),
('P-US10-0015', '2026-06-01', 'C00015', 'JP-VAL-CONS', 'Validation Consultant', 'CC-US10-150', '100193', NULL, TRUE),
('P-US10-0021', '2026-09-14', 'C00021', 'JP-AUD-CONS', 'GMP Audit Consultant', 'CC-US10-120', '100112', NULL, TRUE)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS workday_hcm.business_process_event (
  event_id                varchar(30) NOT NULL,
  business_process_type   varchar(60) NOT NULL,
  employee_id             varchar(20) NOT NULL,
  effective_date          date NOT NULL,
  initiated_moment        timestamptz NOT NULL,
  proposed_job_profile_id varchar(40),
  status                  varchar(30) NOT NULL,
  comment                 text,
  CONSTRAINT business_process_event_pk PRIMARY KEY (event_id)
);
COMMENT ON TABLE workday_hcm.business_process_event IS 'Staffing business process events (hire, change job, termination, contingent worker contract).';

INSERT INTO workday_hcm.business_process_event (event_id, business_process_type, employee_id, effective_date, initiated_moment, proposed_job_profile_id, status, comment) VALUES
('EVT-2014-00107', 'Hire', '100101', '2014-03-03', '2014-02-17 15:12:00+00', 'JP-SITE-HEAD', 'Successfully Completed', 'Hire: Site Head, Austin, Site Leadership'),
('EVT-2016-00114', 'Hire', '100112', '2016-06-13', '2016-05-30 15:12:00+00', 'JP-QA-DIR', 'Successfully Completed', 'Hire: Director of Quality Assurance, Quality Assurance'),
('EVT-2017-00121', 'Hire', '100167', '2017-04-03', '2017-03-20 15:12:00+00', 'JP-FIN-CTRL', 'Successfully Completed', 'Hire: Site Controller, Finance'),
('EVT-2017-00128', 'Hire', '100124', '2017-09-11', '2017-08-28 15:12:00+00', 'JP-QC-MGR', 'Successfully Completed', 'Hire: QC Laboratory Manager, Quality Control Laboratory'),
('EVT-2018-00135', 'Hire', '100142', '2018-05-14', '2018-04-30 15:12:00+00', 'JP-MFG-SUP', 'Successfully Completed', 'Hire: Manufacturing Supervisor, Manufacturing'),
('EVT-2018-00142', 'Hire', '100162', '2018-11-05', '2018-10-22 15:12:00+00', 'JP-WH-LEAD', 'Successfully Completed', 'Hire: Warehouse Lead, Warehouse and Logistics'),
('EVT-2019-00149', 'Hire', '100118', '2019-01-07', '2018-12-24 15:12:00+00', 'JP-QA-BDS', 'Successfully Completed', 'Hire: QA Batch Disposition Specialist, Quality Assurance'),
('EVT-2019-00156', 'Hire', '100180', '2019-05-06', '2019-04-22 15:12:00+00', 'JP-PROC-MGR', 'Successfully Completed', 'Hire: Procurement Manager, Procurement'),
('EVT-2019-00163', 'Hire', '100193', '2019-08-19', '2019-08-05 15:12:00+00', 'JP-ENG-CAL', 'Successfully Completed', 'Hire: Maintenance and Calibration Engineer, Engineering and Maintenance'),
('EVT-2019-00170', 'Hire', '100149', '2019-10-07', '2019-09-23 15:12:00+00', 'JP-MFG-OP3', 'Successfully Completed', 'Hire: Production Operator III, Manufacturing'),
('EVT-2020-00177', 'Hire', '100128', '2020-02-03', '2020-01-20 15:12:00+00', 'JP-QC-ANL2', 'Successfully Completed', 'Hire: QC Analyst II, Quality Control Laboratory'),
('EVT-2020-00184', 'Hire', '100171', '2020-07-13', '2020-06-29 15:12:00+00', 'JP-FIN-SRACC', 'Successfully Completed', 'Hire: Senior Accountant, Finance'),
('EVT-2020-00191', 'Hire', '100131', '2020-08-24', '2020-08-10 15:12:00+00', 'JP-QC-ANL2', 'Successfully Completed', 'Hire: QC Analyst II, Quality Control Laboratory'),
('EVT-2020-00198', 'Hire', '100184', '2020-11-02', '2020-10-19 15:12:00+00', 'JP-HR-BP', 'Successfully Completed', 'Hire: HR Business Partner, Human Resources'),
('EVT-2021-00205', 'Hire', '100189', '2021-02-15', '2021-02-01 15:12:00+00', 'JP-LOG-DG', 'Successfully Completed', 'Hire: Shipping and Dangerous Goods Coordinator, Warehouse and Logistics'),
('EVT-2021-00212', 'Hire', '100122', '2021-04-19', '2021-04-05 15:12:00+00', 'JP-MFG-OP2', 'Successfully Completed', 'Hire: Production Operator II, Manufacturing'),
('EVT-2021-00219', 'Hire', '100176', '2021-09-20', '2021-09-06 15:12:00+00', 'JP-FIN-AP', 'Successfully Completed', 'Hire: Accounts Payable Specialist, Finance'),
('EVT-2022-00226', 'Hire', '100153', '2022-03-21', '2022-03-07 15:12:00+00', 'JP-MFG-OP3', 'Successfully Completed', 'Hire: Production Operator III, Manufacturing'),
('EVT-2022-00233', 'Hire', '100197', '2022-06-06', '2022-05-23 15:12:00+00', 'JP-CQ-SPEC', 'Successfully Completed', 'Hire: Customer Quality Specialist, Customer Quality and Safety'),
('EVT-2023-00240', 'Hire', '100158', '2023-01-09', '2022-12-26 15:12:00+00', 'JP-CT-SPEC', 'Successfully Completed', 'Hire: Cell Therapy Manufacturing Specialist, Cell Therapy Manufacturing'),
('EVT-2026-00247', 'Hire', '100137', '2026-02-09', '2026-01-26 15:12:00+00', 'JP-QC-CHROM', 'Successfully Completed', 'Hire: QC Chromatography Analyst, Quality Control Laboratory'),
('EVT-2026-00254', 'Hire', '100201', '2026-03-02', '2026-02-16 15:12:00+00', 'JP-PV-ASSOC', 'Successfully Completed', 'Hire: Drug Safety Associate, Customer Quality and Safety'),
('EVT-2026-00391', 'Termination', '100128', '2026-05-29', '2026-05-15 14:05:00+00', NULL, 'Successfully Completed', 'Termination: resignation, last day 2026-05-29'),
('EVT-2026-00261', 'Contract Contingent Worker', 'C00015', '2026-06-01', '2026-05-18 15:12:00+00', 'JP-VAL-CONS', 'Successfully Completed', 'Contract Contingent Worker: Validation Consultant, Engineering and Maintenance'),
('EVT-2026-00455', 'Change Job', '100153', '2026-07-01', '2026-06-18 16:40:00+00', 'JP-MFG-OP3', 'Successfully Completed', 'Change Job: promotion from Production Operator II to Production Operator III'),
('EVT-2026-00517', 'Termination', '100122', '2026-08-14', '2026-08-12 17:30:00+00', NULL, 'Successfully Completed', 'Termination: involuntary, last day 2026-08-14'),
('EVT-2026-00268', 'Hire', '100205', '2026-09-08', '2026-08-25 15:12:00+00', 'JP-QC-ANL1', 'Successfully Completed', 'Hire: QC Analyst I, Quality Control Laboratory'),
('EVT-2026-00275', 'Contract Contingent Worker', 'C00021', '2026-09-14', '2026-08-31 15:12:00+00', 'JP-AUD-CONS', 'Successfully Completed', 'Contract Contingent Worker: GMP Audit Consultant, Quality Assurance')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS workday_hcm.integration_event (
  integration_event_id      varchar(20) NOT NULL,
  business_process_event_id varchar(30) NOT NULL,
  integration_system_id     varchar(60) NOT NULL,
  initiated_moment          timestamptz NOT NULL,
  completed_moment          timestamptz,
  status                    varchar(20) NOT NULL,
  message                   text,
  CONSTRAINT integration_event_pk PRIMARY KEY (integration_event_id)
);
COMMENT ON TABLE workday_hcm.integration_event IS 'Outbound integration runs launched by a business process event, one per target and attempt.';

INSERT INTO workday_hcm.integration_event (integration_event_id, business_process_event_id, integration_system_id, initiated_moment, completed_moment, status, message) VALUES
('IE-005003', 'EVT-2026-00247', 'INT001_Entra_ID_User_Provisioning', '2026-01-26 15:47:00+00', '2026-01-26 16:04:00+00', 'Completed', NULL),
('IE-005006', 'EVT-2026-00247', 'INT004_Cornerstone_User_Feed', '2026-01-27 02:00:00+00', '2026-01-27 02:05:00+00', 'Completed', NULL),
('IE-005009', 'EVT-2026-00254', 'INT001_Entra_ID_User_Provisioning', '2026-02-16 15:47:00+00', '2026-02-16 15:51:00+00', 'Completed', NULL),
('IE-005012', 'EVT-2026-00254', 'INT004_Cornerstone_User_Feed', '2026-02-17 02:00:00+00', '2026-02-17 02:04:00+00', 'Completed', NULL),
('IE-005015', 'EVT-2026-00391', 'INT001_Entra_ID_User_Provisioning', '2026-05-15 14:40:00+00', '2026-05-15 14:50:00+00', 'Completed', NULL),
('IE-005018', 'EVT-2026-00391', 'INT004_Cornerstone_User_Feed', '2026-05-16 02:00:00+00', '2026-05-16 02:17:00+00', 'Completed', NULL),
('IE-005021', 'EVT-2026-00261', 'INT001_Entra_ID_User_Provisioning', '2026-05-18 15:47:00+00', '2026-05-18 15:51:00+00', 'Completed', NULL),
('IE-005024', 'EVT-2026-00261', 'INT004_Cornerstone_User_Feed', '2026-05-19 02:00:00+00', '2026-05-19 02:22:00+00', 'Completed', NULL),
('IE-005027', 'EVT-2026-00455', 'INT001_Entra_ID_User_Provisioning', '2026-06-18 17:15:00+00', '2026-06-18 17:23:00+00', 'Completed', NULL),
('IE-005030', 'EVT-2026-00455', 'INT004_Cornerstone_User_Feed', '2026-06-19 02:00:00+00', '2026-06-19 02:19:00+00', 'Completed', NULL),
('IE-005033', 'EVT-2026-00455', 'INT006_UKG_Dimensions_Employee_Export', '2026-06-19 03:00:00+00', '2026-06-19 03:12:00+00', 'Completed', NULL),
('IE-005036', 'EVT-2026-00517', 'INT001_Entra_ID_User_Provisioning', '2026-08-12 18:05:00+00', '2026-08-12 18:07:00+00', 'Failed', 'Entra ID rejected update: user object locked by pending access review'),
('IE-005037', 'EVT-2026-00517', 'INT001_Entra_ID_User_Provisioning', '2026-08-28 09:05:00+00', '2026-08-28 09:12:00+00', 'Completed', 'Manual re-run after access review closed'),
('IE-005040', 'EVT-2026-00517', 'INT004_Cornerstone_User_Feed', '2026-08-13 02:00:00+00', '2026-08-13 02:20:00+00', 'Completed', NULL),
('IE-005043', 'EVT-2026-00517', 'INT006_UKG_Dimensions_Employee_Export', '2026-08-13 03:00:00+00', '2026-08-13 03:10:00+00', 'Completed', NULL),
('IE-005046', 'EVT-2026-00268', 'INT001_Entra_ID_User_Provisioning', '2026-08-25 15:47:00+00', '2026-08-25 15:55:00+00', 'Completed', NULL),
('IE-005049', 'EVT-2026-00268', 'INT004_Cornerstone_User_Feed', '2026-08-26 02:00:00+00', '2026-08-26 02:10:00+00', 'Completed', NULL),
('IE-005052', 'EVT-2026-00275', 'INT001_Entra_ID_User_Provisioning', '2026-08-31 15:47:00+00', '2026-08-31 15:52:00+00', 'Completed', NULL),
('IE-005055', 'EVT-2026-00275', 'INT004_Cornerstone_User_Feed', '2026-09-01 02:00:00+00', '2026-09-01 02:01:00+00', 'Failed', 'No Cornerstone position mapped for job profile JP-AUD-CONS')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS workday_hcm.pay_run (
  pay_run_id         varchar(30) NOT NULL,
  pay_group          varchar(60) NOT NULL,
  company_id         varchar(10) NOT NULL,
  period_start_date  date NOT NULL,
  period_end_date    date NOT NULL,
  payment_date       date NOT NULL,
  worker_count       integer NOT NULL,
  total_gross_amount numeric(18,2) NOT NULL,
  currency           varchar(3) NOT NULL,
  status             varchar(20) NOT NULL,
  completed_moment   timestamptz,
  CONSTRAINT pay_run_pk PRIMARY KEY (pay_run_id)
);
COMMENT ON TABLE workday_hcm.pay_run IS 'Completed pay runs for the US monthly pay group.';

INSERT INTO workday_hcm.pay_run (pay_run_id, pay_group, company_id, period_start_date, period_end_date, payment_date, worker_count, total_gross_amount, currency, status, completed_moment) VALUES
('PR-US01-2026-07', 'US01 Monthly', 'US01', '2026-07-01', '2026-07-31', '2026-07-31', 21, 168448.34, 'USD', 'Complete', '2026-07-29 22:40:00+00'),
('PR-US01-2026-08', 'US01 Monthly', 'US01', '2026-08-01', '2026-08-31', '2026-08-31', 21, 165406.50, 'USD', 'Complete', '2026-08-29 22:40:00+00'),
('PR-US01-2026-09', 'US01 Monthly', 'US01', '2026-09-01', '2026-09-30', '2026-09-30', 21, 167573.95, 'USD', 'Complete', '2026-09-28 22:40:00+00')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS workday_hcm.payroll_result (
  pay_run_id                    varchar(30) NOT NULL,
  employee_id                   varchar(20) NOT NULL,
  gross_amount                  numeric(18,2) NOT NULL,
  employer_contributions_amount numeric(18,2) NOT NULL,
  net_amount                    numeric(18,2) NOT NULL,
  cost_center_id                varchar(20) NOT NULL,
  ledger_account                varchar(20) NOT NULL,
  currency                      varchar(3) NOT NULL,
  CONSTRAINT payroll_result_pk PRIMARY KEY (pay_run_id, employee_id)
);
COMMENT ON TABLE workday_hcm.payroll_result IS 'Pay calculation results per worker and run, with the payroll accounting account.';

INSERT INTO workday_hcm.payroll_result (pay_run_id, employee_id, gross_amount, employer_contributions_amount, net_amount, cost_center_id, ledger_account, currency) VALUES
('PR-US01-2026-07', '100101', 20416.67, 4420.21, 14536.67, 'CC-US10-100', '6100100', 'USD'),
('PR-US01-2026-07', '100112', 15166.67, 3283.58, 10798.67, 'CC-US10-120', '6100100', 'USD'),
('PR-US01-2026-07', '100118', 8166.67, 1768.08, 5814.67, 'CC-US10-120', '6100100', 'USD'),
('PR-US01-2026-07', '100122', 4356.00, 943.07, 3101.47, 'CC-US10-110', '6100200', 'USD'),
('PR-US01-2026-07', '100124', 10666.67, 2309.33, 7594.67, 'CC-US10-130', '6100100', 'USD'),
('PR-US01-2026-07', '100131', 6333.33, 1371.17, 4509.33, 'CC-US10-130', '6100100', 'USD'),
('PR-US01-2026-07', '100137', 6166.67, 1335.08, 4390.67, 'CC-US10-130', '6100100', 'USD'),
('PR-US01-2026-07', '100142', 7666.67, 1659.83, 5458.67, 'CC-US10-110', '6100100', 'USD'),
('PR-US01-2026-07', '100149', 5546.00, 1200.71, 3948.75, 'CC-US10-110', '6100200', 'USD'),
('PR-US01-2026-07', '100153', 5811.50, 1258.19, 4137.79, 'CC-US10-110', '6100200', 'USD'),
('PR-US01-2026-07', '100158', 5676.00, 1228.85, 4041.31, 'CC-US10-115', '6100200', 'USD'),
('PR-US01-2026-07', '100162', 4959.50, 1073.73, 3531.16, 'CC-US10-140', '6100200', 'USD'),
('PR-US01-2026-07', '100167', 12500.00, 2706.25, 8900.00, 'CC-US10-210', '6100100', 'USD'),
('PR-US01-2026-07', '100171', 7333.33, 1587.67, 5221.33, 'CC-US10-210', '6100100', 'USD'),
('PR-US01-2026-07', '100176', 4833.33, 1046.42, 3441.33, 'CC-US10-210', '6100100', 'USD'),
('PR-US01-2026-07', '100180', 9833.33, 2128.92, 7001.33, 'CC-US10-230', '6100100', 'USD'),
('PR-US01-2026-07', '100184', 8000.00, 1732.00, 5696.00, 'CC-US10-220', '6100100', 'USD'),
('PR-US01-2026-07', '100189', 5016.00, 1085.96, 3571.39, 'CC-US10-140', '6100200', 'USD'),
('PR-US01-2026-07', '100193', 7500.00, 1623.75, 5340.00, 'CC-US10-150', '6100100', 'USD'),
('PR-US01-2026-07', '100197', 6000.00, 1299.00, 4272.00, 'CC-US10-160', '6100100', 'USD'),
('PR-US01-2026-07', '100201', 6500.00, 1407.25, 4628.00, 'CC-US10-160', '6100100', 'USD'),
('PR-US01-2026-08', '100101', 20416.67, 4420.21, 14536.67, 'CC-US10-100', '6100100', 'USD'),
('PR-US01-2026-08', '100112', 15166.67, 3283.58, 10798.67, 'CC-US10-120', '6100100', 'USD'),
('PR-US01-2026-08', '100118', 8166.67, 1768.08, 5814.67, 'CC-US10-120', '6100100', 'USD'),
('PR-US01-2026-08', '100122', 1877.78, 406.54, 1336.98, 'CC-US10-110', '6100200', 'USD'),
('PR-US01-2026-08', '100124', 10666.67, 2309.33, 7594.67, 'CC-US10-130', '6100100', 'USD'),
('PR-US01-2026-08', '100131', 6333.33, 1371.17, 4509.33, 'CC-US10-130', '6100100', 'USD'),
('PR-US01-2026-08', '100137', 6166.67, 1335.08, 4390.67, 'CC-US10-130', '6100100', 'USD'),
('PR-US01-2026-08', '100142', 7666.67, 1659.83, 5458.67, 'CC-US10-110', '6100100', 'USD'),
('PR-US01-2026-08', '100149', 5280.50, 1143.23, 3759.72, 'CC-US10-110', '6100200', 'USD'),
('PR-US01-2026-08', '100153', 5634.50, 1219.87, 4011.76, 'CC-US10-110', '6100200', 'USD'),
('PR-US01-2026-08', '100158', 5742.00, 1243.14, 4088.30, 'CC-US10-115', '6100200', 'USD'),
('PR-US01-2026-08', '100162', 5000.38, 1082.58, 3560.27, 'CC-US10-140', '6100200', 'USD'),
('PR-US01-2026-08', '100167', 12500.00, 2706.25, 8900.00, 'CC-US10-210', '6100100', 'USD'),
('PR-US01-2026-08', '100171', 7333.33, 1587.67, 5221.33, 'CC-US10-210', '6100100', 'USD'),
('PR-US01-2026-08', '100176', 4833.33, 1046.42, 3441.33, 'CC-US10-210', '6100100', 'USD'),
('PR-US01-2026-08', '100180', 9833.33, 2128.92, 7001.33, 'CC-US10-230', '6100100', 'USD'),
('PR-US01-2026-08', '100184', 8000.00, 1732.00, 5696.00, 'CC-US10-220', '6100100', 'USD'),
('PR-US01-2026-08', '100189', 4788.00, 1036.60, 3409.06, 'CC-US10-140', '6100200', 'USD'),
('PR-US01-2026-08', '100193', 7500.00, 1623.75, 5340.00, 'CC-US10-150', '6100100', 'USD'),
('PR-US01-2026-08', '100197', 6000.00, 1299.00, 4272.00, 'CC-US10-160', '6100100', 'USD'),
('PR-US01-2026-08', '100201', 6500.00, 1407.25, 4628.00, 'CC-US10-160', '6100100', 'USD'),
('PR-US01-2026-09', '100101', 20416.67, 4420.21, 14536.67, 'CC-US10-100', '6100100', 'USD'),
('PR-US01-2026-09', '100112', 15166.67, 3283.58, 10798.67, 'CC-US10-120', '6100100', 'USD'),
('PR-US01-2026-09', '100118', 8166.67, 1768.08, 5814.67, 'CC-US10-120', '6100100', 'USD'),
('PR-US01-2026-09', '100124', 10666.67, 2309.33, 7594.67, 'CC-US10-130', '6100100', 'USD'),
('PR-US01-2026-09', '100131', 6333.33, 1371.17, 4509.33, 'CC-US10-130', '6100100', 'USD'),
('PR-US01-2026-09', '100137', 6166.67, 1335.08, 4390.67, 'CC-US10-130', '6100100', 'USD'),
('PR-US01-2026-09', '100142', 7666.67, 1659.83, 5458.67, 'CC-US10-110', '6100100', 'USD'),
('PR-US01-2026-09', '100149', 5015.00, 1085.75, 3570.68, 'CC-US10-110', '6100200', 'USD'),
('PR-US01-2026-09', '100153', 5192.00, 1124.07, 3696.70, 'CC-US10-110', '6100200', 'USD'),
('PR-US01-2026-09', '100158', 6402.00, 1386.03, 4558.22, 'CC-US10-115', '6100200', 'USD'),
('PR-US01-2026-09', '100162', 4605.25, 997.04, 3278.94, 'CC-US10-140', '6100200', 'USD'),
('PR-US01-2026-09', '100167', 12500.00, 2706.25, 8900.00, 'CC-US10-210', '6100100', 'USD'),
('PR-US01-2026-09', '100171', 7333.33, 1587.67, 5221.33, 'CC-US10-210', '6100100', 'USD'),
('PR-US01-2026-09', '100176', 4833.33, 1046.42, 3441.33, 'CC-US10-210', '6100100', 'USD'),
('PR-US01-2026-09', '100180', 9833.33, 2128.92, 7001.33, 'CC-US10-230', '6100100', 'USD'),
('PR-US01-2026-09', '100184', 8000.00, 1732.00, 5696.00, 'CC-US10-220', '6100100', 'USD'),
('PR-US01-2026-09', '100189', 5315.25, 1150.75, 3784.46, 'CC-US10-140', '6100200', 'USD'),
('PR-US01-2026-09', '100193', 7500.00, 1623.75, 5340.00, 'CC-US10-150', '6100100', 'USD'),
('PR-US01-2026-09', '100197', 6000.00, 1299.00, 4272.00, 'CC-US10-160', '6100100', 'USD'),
('PR-US01-2026-09', '100201', 6500.00, 1407.25, 4628.00, 'CC-US10-160', '6100100', 'USD'),
('PR-US01-2026-09', '100205', 3961.11, 857.58, 2820.31, 'CC-US10-130', '6100100', 'USD')
ON CONFLICT DO NOTHING;

-- Subscription inbound: tables and columns written by the coco_subscriptions_austin_systems DAG from the
-- digital products this system subscribes to (see coco-subscription-loads/austin_systems/workday_hcm).
-- No extract reads them.

CREATE TABLE IF NOT EXISTS workday_hcm.personal_data_request (
  request_id              varchar(40) NOT NULL,
  employee_id             varchar(20) NOT NULL,
  request_type            varchar(20) NOT NULL,
  fulfilment_start_moment timestamptz NOT NULL,
  systems_in_scope        integer NOT NULL,
  request_status          varchar(20) NOT NULL,
  CONSTRAINT personal_data_request_pk PRIMARY KEY (request_id)
);
COMMENT ON TABLE workday_hcm.personal_data_request IS 'Data subject rights requests about Austin workers, received from Rights Fulfilment Actions (Workday Data Privacy request).';

CREATE TABLE IF NOT EXISTS workday_hcm.personal_data_request_task (
  task_id              varchar(40) NOT NULL,
  request_id           varchar(40) NOT NULL,
  action_type          varchar(20) NOT NULL,
  requested_moment     timestamptz NOT NULL,
  completed_moment     timestamptz,
  task_status          varchar(20) NOT NULL,
  retention_obligation varchar(40),
  CONSTRAINT personal_data_request_task_pk PRIMARY KEY (task_id)
);
COMMENT ON TABLE workday_hcm.personal_data_request_task IS 'Actions Workday must take (locate, export, erase, restrict) for a personal data request.';

GRANT USAGE ON SCHEMA workday_hcm TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA workday_hcm TO egeria_user, airflow_user;
