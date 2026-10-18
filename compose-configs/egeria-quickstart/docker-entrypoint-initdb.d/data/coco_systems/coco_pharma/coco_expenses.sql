-- system-qualified-name: System::coco-expenses
-- Coco Expenses - Coco core.  SaaS employee expense tool for recording expenses and authorising repayment; feeds Expense Approvals and Employee Expense Claims.
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS coco_expenses;
COMMENT ON SCHEMA coco_expenses IS 'Coco Expenses (Coco core): claimant profiles, cost centres, expense reports, entries and approvals.';

CREATE TABLE IF NOT EXISTS coco_expenses.employee_profile (
  employee_ref varchar(20) NOT NULL,
  employee_number varchar(10) NOT NULL,
  reimbursement_currency varchar(3) NOT NULL,
  default_cost_center varchar(10) NOT NULL,
  approver_ref varchar(20) NOT NULL,
  spend_limit numeric(12,2),
  active varchar(1) NOT NULL,
  CONSTRAINT employee_profile_pk PRIMARY KEY (employee_ref)
);
COMMENT ON TABLE coco_expenses.employee_profile IS 'Claimant profiles loaded from HR; employee_ref is the HRIM worker pseudonym.';

CREATE TABLE IF NOT EXISTS coco_expenses.employee_cost_center (
  employee_ref varchar(20) NOT NULL,
  cost_center varchar(10) NOT NULL,
  approver_ref varchar(20) NOT NULL,
  spend_limit numeric(12,2),
  CONSTRAINT employee_cost_center_pk PRIMARY KEY (employee_ref, cost_center)
);
COMMENT ON TABLE coco_expenses.employee_cost_center IS 'Cost centres each claimant may charge, with the approver and spending limit.';

CREATE TABLE IF NOT EXISTS coco_expenses.expense_report (
  report_id varchar(16) NOT NULL,
  employee_ref varchar(20) NOT NULL,
  created_at timestamptz NOT NULL,
  submitted_at timestamptz,
  report_total numeric(12,2) NOT NULL,
  currency varchar(3) NOT NULL,
  status varchar(12) NOT NULL,
  approver_ref varchar(20) NOT NULL,
  gl_account varchar(10) NOT NULL,
  cost_center varchar(10) NOT NULL,
  CONSTRAINT expense_report_pk PRIMARY KEY (report_id)
);
COMMENT ON TABLE coco_expenses.expense_report IS 'Expense reports. status DRAFT, SUBMITTED, APPROVED, SENT_BACK, REJECTED, PAID.';

CREATE TABLE IF NOT EXISTS coco_expenses.expense_entry (
  report_id varchar(16) NOT NULL,
  entry_no smallint NOT NULL,
  expense_type varchar(16) NOT NULL,
  transaction_date date NOT NULL,
  amount numeric(12,2) NOT NULL,
  description text NOT NULL,
  attendee_hcp_id varchar(20),
  receipt_image_id varchar(20),
  CONSTRAINT expense_entry_pk PRIMARY KEY (report_id, entry_no)
);
COMMENT ON TABLE coco_expenses.expense_entry IS 'Expense entries; attendee_hcp_id identifies a healthcare professional entertained.';

CREATE TABLE IF NOT EXISTS coco_expenses.approval_history (
  report_id varchar(16) NOT NULL,
  action_at timestamptz NOT NULL,
  actor_ref varchar(20) NOT NULL,
  action varchar(10) NOT NULL,
  comment text,
  CONSTRAINT approval_history_pk PRIMARY KEY (report_id, action_at)
);
COMMENT ON TABLE coco_expenses.approval_history IS 'Approval workflow actions: APPROVE, REJECT, SEND_BACK.';

INSERT INTO coco_expenses.employee_profile (employee_ref, employee_number, reimbursement_currency, default_cost_center, approver_ref, spend_limit, active) VALUES
('CW-5V7T2Y', '144994', 'USD', '2343', 'CW-U5PPXA', 5000.0, 'Y'),
('CW-W9JFK6', '549032', 'USD', '7432', 'CW-5V7T2Y', 2500.0, 'Y'),
('CW-JPKHTU', '254678', 'GBP', '7432', 'CW-5V7T2Y', 2000.0, 'Y'),
('CW-K34WSJ', '549922', 'EUR', '7432', 'CW-5V7T2Y', 2000.0, 'N'),
('CW-VYNNPZ', '324713', 'GBP', '7432', 'CW-SNZYHU', 1500.0, 'Y'),
('CW-SFRGJQ', '483942', 'GBP', '8400', 'CW-KTVC4J', 7500.0, 'Y'),
('CW-RMRC8S', '302145', 'USD', '2343', 'CW-U5PPXA', 5000.0, 'Y'),
('CW-7G8SM2', '610252', 'GBP', '8120', 'CW-SFRGJQ', 750.0, 'Y')
ON CONFLICT DO NOTHING;

INSERT INTO coco_expenses.employee_cost_center (employee_ref, cost_center, approver_ref, spend_limit) VALUES
('CW-5V7T2Y', '2343', 'CW-U5PPXA', 5000.0),
('CW-W9JFK6', '7432', 'CW-5V7T2Y', 2500.0),
('CW-JPKHTU', '7432', 'CW-5V7T2Y', 2000.0),
('CW-K34WSJ', '7432', 'CW-5V7T2Y', 2000.0),
('CW-VYNNPZ', '7432', 'CW-SNZYHU', 1500.0),
('CW-SFRGJQ', '8400', 'CW-KTVC4J', 7500.0),
('CW-RMRC8S', '2343', 'CW-U5PPXA', 5000.0),
('CW-7G8SM2', '8120', 'CW-SFRGJQ', 750.0),
('CW-5V7T2Y', '7432', 'CW-U5PPXA', 5000.0),
('CW-SFRGJQ', '8100', 'CW-KTVC4J', 7500.0),
('CW-SFRGJQ', '8200', 'CW-KTVC4J', 7500.0),
('CW-RMRC8S', '4051', 'CW-U5PPXA', 3000.0)
ON CONFLICT DO NOTHING;

INSERT INTO coco_expenses.expense_report (report_id, employee_ref, created_at, submitted_at, report_total, currency, status, approver_ref, gl_account, cost_center) VALUES
('RPT-26-0712', 'CW-5V7T2Y', '2026-08-21 22:10+00', '2026-08-22 13:05+00', 451.0, 'USD', 'PAID', 'CW-U5PPXA', '6210', '2343'),
('RPT-26-0730', 'CW-JPKHTU', '2026-08-28 17:30+00', '2026-08-28 17:44+00', 196.7, 'GBP', 'PAID', 'CW-5V7T2Y', '6200', '7432'),
('RPT-26-0741', 'CW-SFRGJQ', '2026-09-01 08:20+00', '2026-09-01 08:25+00', 1762.8, 'GBP', 'PAID', 'CW-KTVC4J', '6200', '8400'),
('RPT-26-0755', 'CW-W9JFK6', '2026-09-05 19:00+00', '2026-09-05 19:02+00', 845.0, 'USD', 'REJECTED', 'CW-5V7T2Y', '6210', '7432'),
('RPT-26-0762', 'CW-K34WSJ', '2026-09-08 09:30+00', '2026-09-08 09:41+00', 403.0, 'EUR', 'APPROVED', 'CW-5V7T2Y', '6200', '7432'),
('RPT-26-0768', 'CW-VYNNPZ', '2026-09-10 16:00+00', '2026-09-10 16:05+00', 132.0, 'GBP', 'SENT_BACK', 'CW-SNZYHU', '6200', '7432'),
('RPT-26-0774', 'CW-RMRC8S', '2026-09-14 21:00+00', '2026-09-14 21:03+00', 2418.3, 'USD', 'APPROVED', 'CW-U5PPXA', '6200', '2343'),
('RPT-26-0781', 'CW-7G8SM2', '2026-09-17 07:45+00', '2026-09-17 07:47+00', 145.0, 'GBP', 'SUBMITTED', 'CW-SFRGJQ', '6200', '8120'),
('RPT-26-0788', 'CW-5V7T2Y', '2026-09-24 20:00+00', '2026-09-24 20:02+00', 411.0, 'USD', 'SUBMITTED', 'CW-U5PPXA', '6210', '2343'),
('RPT-26-0790', 'CW-K34WSJ', '2026-09-17 11:00+00', NULL, 36.0, 'EUR', 'DRAFT', 'CW-5V7T2Y', '6200', '7432'),
('RPT-26-0793', 'CW-JPKHTU', '2026-09-28 18:10+00', '2026-09-28 18:12+00', 86.5, 'GBP', 'SUBMITTED', 'CW-5V7T2Y', '6200', '7432')
ON CONFLICT DO NOTHING;

INSERT INTO coco_expenses.expense_entry (report_id, entry_no, expense_type, transaction_date, amount, description, attendee_hcp_id, receipt_image_id) VALUES
('RPT-26-0712', 1, 'BUS_MEAL_HCP', '2026-08-19', 412.6, 'Dinner with Dr Grant Able (Hampton Hospital) to discuss Cocolecel outcomes', 'HCP-US-000417', 'IMG-88120'),
('RPT-26-0712', 2, 'TAXI', '2026-08-19', 38.4, 'Taxi to restaurant', NULL, 'IMG-88121'),
('RPT-26-0730', 1, 'RAIL', '2026-08-26', 86.5, 'London to Winchester return for site visit', NULL, 'IMG-88305'),
('RPT-26-0730', 2, 'MEALS', '2026-08-26', 14.2, 'Lunch', NULL, NULL),
('RPT-26-0730', 3, 'BUS_MEAL_HCP', '2026-08-27', 96.0, 'Lunch meeting with pharmacy buyer and consultant pharmacist', 'HCP-GB-001182', 'IMG-88306'),
('RPT-26-0741', 1, 'AIRFARE', '2026-08-30', 1286.0, 'London to Edmonton return - line transfer review', NULL, 'IMG-88410'),
('RPT-26-0741', 2, 'HOTEL', '2026-08-31', 412.0, 'Edmonton hotel 2 nights', NULL, 'IMG-88411'),
('RPT-26-0741', 3, 'MEALS', '2026-09-01', 64.8, 'Meals in Edmonton', NULL, 'IMG-88412'),
('RPT-26-0755', 1, 'BUS_MEAL_HCP', '2026-09-03', 845.0, 'Team dinner with clinicians from Old Market Hospital', 'HCP-US-000592', NULL),
('RPT-26-0762', 1, 'AIRFARE', '2026-09-04', 214.0, 'Amsterdam to London return', NULL, 'IMG-88602'),
('RPT-26-0762', 2, 'HOTEL', '2026-09-04', 189.0, 'London hotel 1 night', NULL, 'IMG-88603'),
('RPT-26-0768', 1, 'RAIL', '2026-09-09', 132.0, 'Rail to Amsterdam data governance workshop', NULL, NULL),
('RPT-26-0774', 1, 'AIRFARE', '2026-09-10', 1740.0, 'New York to London return - cell therapy steering committee', NULL, 'IMG-88741'),
('RPT-26-0774', 2, 'HOTEL', '2026-09-11', 620.0, 'Winchester hotel 2 nights', NULL, 'IMG-88742'),
('RPT-26-0774', 3, 'MEALS', '2026-09-12', 58.3, 'Meals', NULL, 'IMG-88743'),
('RPT-26-0781', 1, 'OTHER', '2026-09-15', 145.0, 'IATA DGR refresher exam fee', NULL, 'IMG-88810'),
('RPT-26-0788', 1, 'BUS_MEAL_HCP', '2026-09-22', 368.9, 'Dinner with Dr Grant Able and oncology nurse lead', 'HCP-US-000417', 'IMG-88902'),
('RPT-26-0788', 2, 'TAXI', '2026-09-22', 42.1, 'Taxi', NULL, 'IMG-88903'),
('RPT-26-0790', 1, 'MEALS', '2026-09-16', 36.0, 'Lunch with customer', NULL, NULL),
('RPT-26-0793', 1, 'RAIL', '2026-09-25', 86.5, 'London to Winchester return', NULL, 'IMG-89011')
ON CONFLICT DO NOTHING;

INSERT INTO coco_expenses.approval_history (report_id, action_at, actor_ref, action, comment) VALUES
('RPT-26-0712', '2026-08-23 09:12+00', 'CW-U5PPXA', 'APPROVE', NULL),
('RPT-26-0730', '2026-08-29 08:00+00', 'CW-5V7T2Y', 'APPROVE', NULL),
('RPT-26-0741', '2026-09-02 12:30+00', 'CW-KTVC4J', 'APPROVE', 'OK'),
('RPT-26-0755', '2026-09-06 10:15+00', 'CW-5V7T2Y', 'REJECT', 'Exceeds per-head hospitality limit for HCPs and no receipt attached.'),
('RPT-26-0762', '2026-09-09 14:00+00', 'CW-5V7T2Y', 'APPROVE', NULL),
('RPT-26-0768', '2026-09-11 08:40+00', 'CW-SNZYHU', 'SEND_BACK', 'Please attach the receipt.'),
('RPT-26-0774', '2026-09-15 13:20+00', 'CW-U5PPXA', 'APPROVE', NULL)
ON CONFLICT DO NOTHING;

-- Tables added for the digital product subscriptions (coco-subscription-loads).

CREATE TABLE IF NOT EXISTS coco_expenses.employee_import (
  employee_ref varchar(20) NOT NULL,
  legal_entity varchar(10) NOT NULL,
  work_site varchar(4) NOT NULL,
  employee_type varchar(10) NOT NULL,
  hire_date date NOT NULL,
  termination_date date,
  employment_status varchar(10) NOT NULL,
  reimbursement_currency varchar(3) NOT NULL,
  job_title varchar(120),
  cost_center varchar(10),
  approver_ref varchar(20),
  CONSTRAINT employee_import_pk PRIMARY KEY (employee_ref)
);
COMMENT ON TABLE coco_expenses.employee_import IS 'Employee import feed: the latest HR record for each Coco worker (from Worker Master Data), from which claimant profiles are created and deactivated; employee_ref is the HRIM worker pseudonym.';

-- End of subscription tables.

GRANT USAGE ON SCHEMA coco_expenses TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA coco_expenses TO egeria_user, airflow_user;
