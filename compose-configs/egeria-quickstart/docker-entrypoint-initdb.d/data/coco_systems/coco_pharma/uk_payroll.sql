-- system-qualified-name: System::UK payroll
-- UK payroll - Coco core.  COTS payroll with UK tax calculations for Coco Pharmaceuticals UK Ltd (London and Winchester); feeds Payroll Results.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS uk_payroll;
COMMENT ON SCHEMA uk_payroll IS 'UK payroll (Coco core): payroll employees, monthly runs and results.';

CREATE TABLE IF NOT EXISTS uk_payroll.pay_employee (
  payroll_no varchar(8) NOT NULL,
  worker_ref varchar(20) NOT NULL,
  hr_emp_no varchar(10) NOT NULL,
  payslip_name varchar(60) NOT NULL,
  cost_ctr varchar(10) NOT NULL,
  tax_code varchar(8) NOT NULL,
  CONSTRAINT pay_employee_pk PRIMARY KEY (payroll_no)
);
COMMENT ON TABLE uk_payroll.pay_employee IS 'Employees on the UK payroll with the HRIM pseudonym and default cost centre.';

CREATE TABLE IF NOT EXISTS uk_payroll.pay_run (
  run_ref varchar(10) NOT NULL,
  company varchar(10) NOT NULL,
  tax_year varchar(7) NOT NULL,
  tax_period varchar(3) NOT NULL,
  pay_date date NOT NULL,
  emp_count integer NOT NULL,
  total_gross numeric(14,2) NOT NULL,
  ccy varchar(3) NOT NULL,
  run_status varchar(8) NOT NULL,
  CONSTRAINT pay_run_pk PRIMARY KEY (run_ref)
);
COMMENT ON TABLE uk_payroll.pay_run IS 'Monthly pay runs by UK tax year and tax month (M01 = April).';

CREATE TABLE IF NOT EXISTS uk_payroll.pay_result (
  run_ref varchar(10) NOT NULL,
  payroll_no varchar(8) NOT NULL,
  gross_pay numeric(12,2) NOT NULL,
  er_nic numeric(12,2) NOT NULL,
  er_pension numeric(12,2) NOT NULL,
  paye_tax numeric(12,2) NOT NULL,
  ee_nic numeric(12,2) NOT NULL,
  net_pay numeric(12,2) NOT NULL,
  cost_ctr varchar(10) NOT NULL,
  nom_code varchar(10) NOT NULL,
  CONSTRAINT pay_result_pk PRIMARY KEY (run_ref, payroll_no)
);
COMMENT ON TABLE uk_payroll.pay_result IS 'Results per employee per run: gross, employer NIC and pension, deductions, net and the nominal code posted.';

INSERT INTO uk_payroll.pay_employee (payroll_no, worker_ref, hr_emp_no, payslip_name, cost_ctr, tax_code) VALUES
('UK01803', 'CW-KTVC4J', '371803', 'T Daring', '9999', '1257L'),
('UK08888', 'CW-T8FK9X', '188888', 'R Mint', '5656', '1257L'),
('UK16419', 'CW-EZMUNR', '896419', 'T Tally', '6788', '1257L'),
('UK07911', 'CW-GMCZHC', '457911', 'S Counter', '6877', '1257L'),
('UK06776', 'CW-SNZYHU', '296776', 'J Keeper', '5656', '1257L'),
('UK04713', 'CW-VYNNPZ', '324713', 'E Overview', '7432', '1257L'),
('UK06419', 'CW-CR43HM', '986419', 'P Profile', '7432', '1257L'),
('UK04678', 'CW-JPKHTU', '254678', 'H Salle', '7432', '1257L'),
('UK03942', 'CW-SFRGJQ', '483942', 'S Faster', '8400', '1257L'),
('UK00240', 'CW-B76CPN', '610240', 'H Barlow', '8110', '1257L'),
('UK00231', 'CW-F53CJR', '610231', 'M Grange', '8100', '1257L'),
('UK00244', 'CW-XE6DBG', '610244', 'A Rahman', '8100', '1257L'),
('UK00263', 'CW-K7H7ZQ', '610263', 'O Tate', '8100', '1257L'),
('UK00252', 'CW-7G8SM2', '610252', 'D Pearce', '8120', '1257L')
ON CONFLICT DO NOTHING;

INSERT INTO uk_payroll.pay_run (run_ref, company, tax_year, tax_period, pay_date, emp_count, total_gross, ccy, run_status) VALUES
('UK26M05', 'COCO-UK', '2026/27', 'M05', '2026-08-28', 14, 106036.23, 'GBP', 'CLOSED'),
('UK26M06', 'COCO-UK', '2026/27', 'M06', '2026-09-25', 14, 106333.33, 'GBP', 'CLOSED')
ON CONFLICT DO NOTHING;

INSERT INTO uk_payroll.pay_result (run_ref, payroll_no, gross_pay, er_nic, er_pension, paye_tax, ee_nic, net_pay, cost_ctr, nom_code) VALUES
('UK26M05', 'UK01803', 17500.0, 2467.8, 875.0, 4935.75, 1316.16, 10373.09, '9999', '6100'),
('UK26M05', 'UK08888', 15416.67, 2155.3, 770.83, 4310.75, 1149.49, 9185.6, '5656', '6100'),
('UK26M05', 'UK16419', 6000.0, 742.8, 300.0, 1485.75, 396.16, 3818.09, '6788', '6100'),
('UK26M05', 'UK07911', 2583.33, 230.3, 129.17, 307.17, 122.83, 2024.16, '6877', '6100'),
('UK26M05', 'UK06776', 12500.0, 1717.8, 625.0, 3435.75, 916.16, 7523.09, '5656', '6100'),
('UK26M05', 'UK04713', 7333.33, 942.8, 366.67, 1885.75, 502.83, 4578.08, '7432', '6100'),
('UK26M05', 'UK06419', 5083.33, 605.3, 254.17, 1210.75, 322.83, 3295.58, '7432', '6100'),
('UK26M05', 'UK04678', 4833.33, 567.8, 241.67, 1135.75, 302.83, 3153.08, '7432', '6100'),
('UK26M05', 'UK03942', 13333.33, 1842.8, 666.67, 3685.75, 982.83, 7998.08, '8400', '6100'),
('UK26M05', 'UK00240', 7666.67, 992.8, 383.33, 1985.75, 529.49, 4768.1, '8110', '6100'),
('UK26M05', 'UK00231', 3166.67, 317.8, 158.33, 423.83, 169.49, 2415.02, '8100', '6100'),
('UK26M05', 'UK00244', 3666.67, 392.8, 183.33, 523.83, 209.49, 2750.02, '8100', '6100'),
('UK26M05', 'UK00263', 3119.57, 310.74, 155.98, 414.41, 165.73, 2383.45, '8100', '6100'),
('UK26M05', 'UK00252', 3833.33, 417.8, 191.67, 557.17, 222.83, 2861.66, '8120', '6100'),
('UK26M06', 'UK01803', 17500.0, 2467.8, 875.0, 4935.75, 1316.16, 10373.09, '9999', '6100'),
('UK26M06', 'UK08888', 15416.67, 2155.3, 770.83, 4310.75, 1149.49, 9185.6, '5656', '6100'),
('UK26M06', 'UK16419', 6000.0, 742.8, 300.0, 1485.75, 396.16, 3818.09, '6788', '6100'),
('UK26M06', 'UK07911', 2583.33, 230.3, 129.17, 307.17, 122.83, 2024.16, '6877', '6100'),
('UK26M06', 'UK06776', 12500.0, 1717.8, 625.0, 3435.75, 916.16, 7523.09, '5656', '6100'),
('UK26M06', 'UK04713', 7333.33, 942.8, 366.67, 1885.75, 502.83, 4578.08, '7432', '6100'),
('UK26M06', 'UK06419', 5083.33, 605.3, 254.17, 1210.75, 322.83, 3295.58, '7432', '6100'),
('UK26M06', 'UK04678', 4833.33, 567.8, 241.67, 1135.75, 302.83, 3153.08, '7432', '6100'),
('UK26M06', 'UK03942', 13333.33, 1842.8, 666.67, 3685.75, 982.83, 7998.08, '8400', '6100'),
('UK26M06', 'UK00240', 7666.67, 992.8, 383.33, 1985.75, 529.49, 4768.1, '8110', '6100'),
('UK26M06', 'UK00231', 3166.67, 317.8, 158.33, 423.83, 169.49, 2415.02, '8100', '6100'),
('UK26M06', 'UK00244', 3666.67, 392.8, 183.33, 523.83, 209.49, 2750.02, '8100', '6100'),
('UK26M06', 'UK00263', 3416.67, 355.3, 170.83, 473.83, 189.49, 2582.52, '8100', '6100'),
('UK26M06', 'UK00252', 3833.33, 417.8, 191.67, 557.17, 222.83, 2861.66, '8120', '6100')
ON CONFLICT DO NOTHING;

-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS uk_payroll.hr_feed (
  worker_ref varchar(20) NOT NULL,
  company varchar(10) NOT NULL,
  site varchar(4) NOT NULL,
  start_date date NOT NULL,
  leave_date date,
  hr_status varchar(10) NOT NULL,
  job_code varchar(12),
  job_title varchar(120),
  cost_ctr varchar(10),
  mgr_ref varchar(20),
  CONSTRAINT hr_feed_pk PRIMARY KEY (worker_ref)
);
COMMENT ON TABLE uk_payroll.hr_feed IS 'HR interface file: the latest worker record for each UK payroll employee received from Worker Master Data, used by payroll administration to set up starters and process leavers and transfers.';

-- End of subscription tables.

GRANT USAGE ON SCHEMA uk_payroll TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA uk_payroll TO egeria_user, airflow_user;
