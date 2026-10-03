-- Extract: UK payroll (Coco core) -> Payroll Results / payroll_run
-- Source: coco_pharma.uk_payroll (System::UK payroll)
-- Target: coco_data_hub.payroll_results.payroll_run
-- pay_run; UK tax year/month converted to the calendar period YYYY-MM.
SELECT
  r.run_ref::varchar(40)            AS payroll_run_identifier,
  r.company::varchar(10)            AS legal_entity_code,
  to_char(make_date(left(r.tax_year, 4)::int, 4, 1)
          + ((substr(r.tax_period, 2)::int - 1) * interval '1 month'), 'YYYY-MM')::varchar(10) AS payroll_period_code,
  r.pay_date                        AS payroll_run_date,
  r.emp_count::integer              AS payroll_run_count,
  r.total_gross::numeric(18,2)      AS payroll_run_total_amount,
  r.ccy::varchar(3)                 AS payroll_currency_code
FROM uk_payroll.pay_run r
