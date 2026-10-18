-- Extract: UK payroll (Coco core) -> Payroll Results / payroll_posting
-- Source: coco_pharma.uk_payroll (System::UK payroll)
-- Target: coco_data_hub.payroll_results.payroll_posting
-- pay_result; employer cost = employer NIC + pension, payroll number to pseudonym via pay_employee.
SELECT
  x.run_ref::varchar(40)            AS payroll_run_identifier,
  e.worker_ref::varchar(40)         AS worker_pseudonym_identifier,
  x.gross_pay::numeric(18,2)        AS payroll_gross_amount,
  (x.er_nic + x.er_pension)::numeric(18,2) AS payroll_employer_amount,
  x.net_pay::numeric(18,2)          AS payroll_net_amount,
  x.cost_ctr::varchar(20)           AS cost_centre_code,
  x.nom_code::varchar(20)           AS ledger_account_code
FROM uk_payroll.pay_result x
JOIN uk_payroll.pay_employee e ON e.payroll_no = x.payroll_no
