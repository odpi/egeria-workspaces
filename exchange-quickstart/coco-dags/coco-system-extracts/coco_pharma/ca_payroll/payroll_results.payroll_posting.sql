-- Extract: Canadian payroll (Coco core) -> Payroll Results / payroll_posting
-- Source: coco_pharma.ca_payroll (System::CA payroll)
-- Target: coco_data_hub.payroll_results.payroll_posting
-- earnings_statement for processed batches; employer cost = CPP + EI, gl code nn-nn to nnnn, employee number to pseudonym.
SELECT
  e.batch_id::varchar(40)           AS payroll_run_identifier,
  m.worker_ref::varchar(40)         AS worker_pseudonym_identifier,
  e.gross_earnings::numeric(18,2)   AS payroll_gross_amount,
  (e.cpp_employer + e.ei_employer)::numeric(18,2) AS payroll_employer_amount,
  e.net_pay::numeric(18,2)          AS payroll_net_amount,
  e.cost_centre::varchar(20)        AS cost_centre_code,
  replace(e.gl_code, '-', '')::varchar(20) AS ledger_account_code
FROM ca_payroll.earnings_statement e
JOIN ca_payroll.employee_master m ON m.employee_number = e.employee_number
JOIN ca_payroll.payroll_batch b ON b.batch_id = e.batch_id
WHERE b.batch_status = 'P'
