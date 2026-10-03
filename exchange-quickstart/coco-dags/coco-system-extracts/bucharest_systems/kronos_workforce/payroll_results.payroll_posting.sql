-- Extract: Kronos Workforce (Bucharest) -> Payroll Results / payroll_posting
-- Source: bucharest_systems.kronos_workforce (SoftwareServer::SYS-023::Kronos Workforce)
-- Target: coco_data_hub.payroll_results.payroll_posting
-- pay_statement for hourly shift workers joined to person (Workday employee ID, pseudonymised) and the worked labour
-- account (cost centre = labour level 2).
SELECT
  p.payroll_reference::varchar(40) AS payroll_run_identifier,
  ('WP-' || upper(substr(md5('EKG:' || pe.personnum), 1, 12)))::varchar(40) AS worker_pseudonym_identifier,
  p.gross_wages::numeric(18,2) AS payroll_gross_amount,
  p.employer_contrib::numeric(18,2) AS payroll_employer_amount,
  p.net_pay::numeric(18,2) AS payroll_net_amount,
  l.laborlev2nm::varchar(20) AS cost_centre_code,
  p.gl_account::varchar(20) AS ledger_account_code
FROM kronos_workforce.pay_statement p
JOIN kronos_workforce.person pe ON pe.personid = p.personid
JOIN kronos_workforce.laboracct l ON l.laboracctid = p.worked_laboracctid
