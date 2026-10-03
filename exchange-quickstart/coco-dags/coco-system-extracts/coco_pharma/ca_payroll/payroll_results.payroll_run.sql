-- Extract: Canadian payroll (Coco core) -> Payroll Results / payroll_run
-- Source: coco_pharma.ca_payroll (System::CA payroll)
-- Target: coco_data_hub.payroll_results.payroll_run
-- payroll_batch, processed only; CPCA to COCO-CA, pay period to YYYY-PPnn, CAD.
SELECT
  b.batch_id::varchar(40)           AS payroll_run_identifier,
  (CASE b.company_code WHEN 'CPCA' THEN 'COCO-CA' ELSE b.company_code END)::varchar(10) AS legal_entity_code,
  (left(b.period_end, 4) || '-PP' || lpad(b.pay_period::text, 2, '0'))::varchar(10) AS payroll_period_code,
  to_date(b.cheque_date, 'YYYYMMDD') AS payroll_run_date,
  b.employees_paid::integer         AS payroll_run_count,
  b.batch_gross::numeric(18,2)      AS payroll_run_total_amount,
  'CAD'::varchar(3)                 AS payroll_currency_code
FROM ca_payroll.payroll_batch b
WHERE b.batch_status = 'P'
