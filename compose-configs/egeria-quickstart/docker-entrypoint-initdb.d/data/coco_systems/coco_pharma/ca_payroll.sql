-- system-qualified-name: System::CA payroll
-- Canadian payroll - Coco core.  COTS payroll with Canadian tax calculations for Coco Pharmaceuticals Canada Inc. (Edmonton), bi-weekly and configured separately from the Dutch installation; feeds Payroll Results.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS ca_payroll;
COMMENT ON SCHEMA ca_payroll IS 'Canadian payroll (Coco core): employees, bi-weekly payroll batches and earnings statements.';

CREATE TABLE IF NOT EXISTS ca_payroll.employee_master (
  employee_number varchar(6) NOT NULL,
  worker_ref varchar(20) NOT NULL,
  hr_emp_no varchar(10) NOT NULL,
  employee_name varchar(60) NOT NULL,
  home_cost_centre varchar(10) NOT NULL,
  CONSTRAINT employee_master_pk PRIMARY KEY (employee_number)
);
COMMENT ON TABLE ca_payroll.employee_master IS 'Employees on the Canadian payroll with the HRIM pseudonym.';

CREATE TABLE IF NOT EXISTS ca_payroll.payroll_batch (
  batch_id varchar(12) NOT NULL,
  company_code varchar(4) NOT NULL,
  pay_period smallint NOT NULL,
  period_end varchar(8) NOT NULL,
  cheque_date varchar(8) NOT NULL,
  employees_paid integer NOT NULL,
  batch_gross numeric(14,2) NOT NULL,
  batch_status char(1) NOT NULL,
  CONSTRAINT payroll_batch_pk PRIMARY KEY (batch_id)
);
COMMENT ON TABLE ca_payroll.payroll_batch IS 'Bi-weekly payroll batches; company_code CPCA; dates are text YYYYMMDD; batch_status O open, P processed.';

CREATE TABLE IF NOT EXISTS ca_payroll.earnings_statement (
  batch_id varchar(12) NOT NULL,
  employee_number varchar(6) NOT NULL,
  gross_earnings numeric(12,2) NOT NULL,
  cpp_employer numeric(12,2) NOT NULL,
  ei_employer numeric(12,2) NOT NULL,
  net_pay numeric(12,2) NOT NULL,
  cost_centre varchar(10) NOT NULL,
  gl_code varchar(10) NOT NULL,
  CONSTRAINT earnings_statement_pk PRIMARY KEY (batch_id, employee_number)
);
COMMENT ON TABLE ca_payroll.earnings_statement IS 'Earnings statements per employee per batch; gl_code uses the local nn-nn format.';

INSERT INTO ca_payroll.employee_master (employee_number, worker_ref, hr_emp_no, employee_name, home_cost_centre) VALUES
('E045', 'CW-G32FNJ', '810045', 'ROY, CHANTAL', '8210'),
('E052', 'CW-HFD9LG', '810052', 'KOWALSKI, BEN', '8200'),
('E067', 'CW-JS5LWU', '810067', 'SINGH, PRIYA', '8200'),
('E071', 'CW-GBAX2A', '810071', 'WHITEHORSE, TOM', '8220')
ON CONFLICT DO NOTHING;

INSERT INTO ca_payroll.payroll_batch (batch_id, company_code, pay_period, period_end, cheque_date, employees_paid, batch_gross, batch_status) VALUES
('CPB202617', 'CPCA', 17, '20260822', '20260828', 4, 12692.31, 'P'),
('CPB202618', 'CPCA', 18, '20260905', '20260911', 4, 12692.31, 'P'),
('CPB202619', 'CPCA', 19, '20260919', '20260925', 4, 12692.31, 'P')
ON CONFLICT DO NOTHING;

INSERT INTO ca_payroll.earnings_statement (batch_id, employee_number, gross_earnings, cpp_employer, ei_employer, net_pay, cost_centre, gl_code) VALUES
('CPB202617', 'E045', 4923.08, 292.92, 113.03, 3495.39, '8210', '61-00'),
('CPB202617', 'E052', 2384.62, 141.88, 54.75, 1693.08, '8200', '61-00'),
('CPB202617', 'E067', 2846.15, 169.35, 65.35, 2020.77, '8200', '61-00'),
('CPB202617', 'E071', 2538.46, 151.04, 58.28, 1802.31, '8220', '61-00'),
('CPB202618', 'E045', 4923.08, 292.92, 113.03, 3495.39, '8210', '61-00'),
('CPB202618', 'E052', 2384.62, 141.88, 54.75, 1693.08, '8200', '61-00'),
('CPB202618', 'E067', 2846.15, 169.35, 65.35, 2020.77, '8200', '61-00'),
('CPB202618', 'E071', 2538.46, 151.04, 58.28, 1802.31, '8220', '61-00'),
('CPB202619', 'E045', 4923.08, 292.92, 113.03, 3495.39, '8210', '61-00'),
('CPB202619', 'E052', 2384.62, 141.88, 54.75, 1693.08, '8200', '61-00'),
('CPB202619', 'E067', 2846.15, 169.35, 65.35, 2020.77, '8200', '61-00'),
('CPB202619', 'E071', 2538.46, 151.04, 58.28, 1802.31, '8220', '61-00')
ON CONFLICT DO NOTHING;

-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS ca_payroll.hr_interface (
  worker_ref varchar(20) NOT NULL,
  company_code varchar(4) NOT NULL,
  work_location varchar(4) NOT NULL,
  hire_date varchar(8) NOT NULL,
  term_date varchar(8),
  emp_status char(1) NOT NULL,
  job_code varchar(12),
  job_title varchar(120),
  home_cost_centre varchar(10),
  supervisor_ref varchar(20),
  CONSTRAINT hr_interface_pk PRIMARY KEY (worker_ref)
);
COMMENT ON TABLE ca_payroll.hr_interface IS 'HR interface: the latest worker record for each Canadian payroll employee received from Worker Master Data (dates as text YYYYMMDD, emp_status A active, L leave, T terminated), for new hires and terminations.';

-- End of subscription tables.

GRANT USAGE ON SCHEMA ca_payroll TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA ca_payroll TO egeria_user, airflow_user;
