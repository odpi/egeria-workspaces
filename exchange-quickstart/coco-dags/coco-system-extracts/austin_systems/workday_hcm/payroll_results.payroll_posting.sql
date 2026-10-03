-- Extract: Workday Human Capital Management (Austin) -> Payroll Results / payroll_posting
-- Source: austin_systems.workday_hcm (SoftwareServer::AUS-SYS-019::SN-HCM-AU-20190301)
-- Target: coco_data_hub.payroll_results.payroll_posting
-- payroll_result for salaried workers only; hourly workers' postings come from UKG Dimensions, which holds the labour
-- account their hours were worked in.
SELECT
  p.pay_run_id::varchar(40) AS payroll_run_identifier,
  ('WP-' || upper(substr(md5('AUS:' || p.employee_id), 1, 12)))::varchar(40) AS worker_pseudonym_identifier,
  p.gross_amount::numeric(18,2) AS payroll_gross_amount,
  p.employer_contributions_amount::numeric(18,2) AS payroll_employer_amount,
  p.net_amount::numeric(18,2) AS payroll_net_amount,
  p.cost_center_id::varchar(20) AS cost_centre_code,
  p.ledger_account::varchar(20) AS ledger_account_code
FROM workday_hcm.payroll_result p
JOIN workday_hcm.worker w ON w.employee_id = p.employee_id
WHERE w.pay_rate_type = 'Salary'
