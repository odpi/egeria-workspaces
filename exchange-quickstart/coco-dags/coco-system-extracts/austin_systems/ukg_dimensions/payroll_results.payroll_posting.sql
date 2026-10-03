-- Extract: UKG Dimensions (Austin) -> Payroll Results / payroll_posting
-- Source: austin_systems.ukg_dimensions (SoftwareServer::AUS-SYS-021::SN-TNA-AU-20190305)
-- Target: coco_data_hub.payroll_results.payroll_posting
-- pay_statement for hourly workers; cost centre is the second level of the worked labour account; employer amount =
-- taxes + benefits.
SELECT
  p.payroll_reference::varchar(40) AS payroll_run_identifier,
  ('WP-' || upper(substr(md5('AUS:' || p.person_number), 1, 12)))::varchar(40) AS worker_pseudonym_identifier,
  p.gross_wages::numeric(18,2) AS payroll_gross_amount,
  (p.employer_taxes + p.employer_benefits)::numeric(18,2) AS payroll_employer_amount,
  p.net_pay::numeric(18,2) AS payroll_net_amount,
  split_part(p.worked_labor_account, '/', 2)::varchar(20) AS cost_centre_code,
  p.gl_account::varchar(20) AS ledger_account_code
FROM ukg_dimensions.pay_statement p
